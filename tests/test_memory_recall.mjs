// memory-recall-run.mjs (knowledge.recall): memory_search only, in Talk's main session, one call per corpus at once,
// with a short timeout; its answer cut to excerpts without paths; anything else is nothing. The Gateway is stubbed.
import assert from 'node:assert/strict';
import {merge, recall, request, shape, SESSION} from '../memory-recall-run.mjs';

const answer = results => ({ok: true, toolName: 'memory_search', output: {content: [{type: 'text', text: JSON.stringify({results})}]}});
const SAID = [
  {path: 'sessions/main/abc.jsonl', snippet: 'Owner: Ghent it is.\n\nSource: sessions/main/abc.jsonl#L4-L9', source: 'sessions', corpus: 'sessions',
   provenance: {originClass: 'owner', observedAt: 1792000000000}, score: 0.6},
];
const NOTES = [
  {path: 'memory/My Notes/offsite plan.md', snippet: 'Venue shortlist.\n\nSource: memory/My Notes/offsite plan.md#L1-L5', source: 'memory',
   provenance: {originClass: 'weird'}, score: 0.7},
  {path: 'memory/empty.md', snippet: '   ', source: 'memory', score: 0.9},
];
let calls = [];
const runtime = replies => async () => ({callGatewayFromCli: async (...args) => {
  calls.push(args);
  const reply = replies[args[2].args.corpus];
  if (reply instanceof Error) throw reply;
  return reply;
}});

const got = await recall({query: '  the offsite\n decision ', max_results: 50, timeout_ms: 60000}, runtime({sessions: answer(SAID), memory: answer(NOTES)}));
assert.equal(calls.length, 2);
for (const [method, options, params, scope] of calls) {
  assert.equal(method, 'tools.invoke');
  assert.equal(params.name, 'memory_search');
  assert.equal(params.sessionKey, SESSION);
  assert.deepEqual({...params.args, corpus: undefined}, {query: 'the offsite decision', maxResults: 8, corpus: undefined});
  assert.equal(options.timeout, '8000');            // never longer than this, whatever was asked
  assert.deepEqual(scope, {scopes: ['operator.write']});
}
assert.deepEqual(calls.map(c => c[2].args.corpus).sort(), ['memory', 'sessions']);
assert.equal(SESSION, 'agent:main:assistant-talk-main');
assert.deepEqual(got, {results: [
  {source: 'memory', text: 'Venue shortlist.', at: null, origin: 'unknown'},
  {source: 'sessions', text: 'Owner: Ghent it is.', at: 1792000000000, origin: 'owner'},
]});
assert.doesNotMatch(JSON.stringify(got), /abc\.jsonl|My Notes|score/);   // never a path

// Transcripts not indexed (that call refused): the notes still come back
calls = [];
const notesOnly = await recall({query: 'offsite'}, runtime({sessions: {ok: false, error: {code: 'invalid'}}, memory: answer(NOTES)}));
assert.deepEqual(notesOnly.results.map(r => r.source), ['memory']);
// Conversations get up to half the places even when the notes score higher
const row = (source, score) => ({source, text: source + score, at: null, origin: 'agent', score});
const mixed = merge({results: [row('sessions', 0.2), row('sessions', 0.1), row('sessions', 0.05)]},
                    {results: [row('memory', 0.9), row('memory', 0.8), row('memory', 0.7), row('memory', 0.6)]}, 4);
assert.deepEqual(mixed.results.map(r => r.text), ['memory0.9', 'memory0.8', 'sessions0.2', 'sessions0.1']);
assert.deepEqual(merge({results: [row('sessions', 0.2)]}, {results: [row('memory', 0.9), row('memory', 0.8)]}, 3).results.length, 3);

// Off, refused, broken or away: an error the service turns into nothing
assert.deepEqual(await recall({query: ''}, runtime({})), {error: 'invalid_request'});
assert.equal(request({query: 7}), null);
assert.deepEqual(request({query: 'x'}), {query: 'x', limit: 5, timeout: 5000});
assert.deepEqual(shape({ok: false, error: {code: 'not_found'}}), {error: 'unavailable'});
assert.deepEqual(shape({ok: true, output: {isError: true, content: []}}), {error: 'unavailable'});
assert.deepEqual(shape({ok: true, output: {content: [{type: 'text', text: '{"disabled":true}'}]}}), {error: 'off'});
assert.deepEqual(shape({ok: true, output: {content: [{type: 'text', text: 'not json'}]}}), {error: 'unavailable'});
const away = new Error('gateway closed (1006) ws://127.0.0.1:18789 token=abc');
assert.deepEqual(await recall({query: 'x'}, runtime({sessions: away, memory: away})), {error: 'unavailable'});
assert.deepEqual(await recall({query: 'x'}, async () => { throw away; }), {error: 'unavailable'});
console.log('memory recall helper: one read tool, both corpora, short timeout, no paths, nothing on failure.');
