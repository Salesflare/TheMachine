// One web search on a ChatGPT sign-in (openclaw-plugin/web-search.ts): the hosted search goes into that one request only.
import './test-env.mjs';
import assert from 'node:assert/strict';
import {mkdtemp, readFile, readdir, writeFile, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';

const folder = await mkdtemp(join(tmpdir(), 'web-search-test-'));
const config = join(folder, 'config.json');
process.env.ASSISTANT_CONFIG = config;
try {
  const {METHOD, searchBody, webSearch, registerWebSearch} = await import('../openclaw-plugin/web-search.ts');
  const cfg = {agents: {}};
  const api = {runtime: {config: {current: () => cfg}}};
  const calls = [];
  let reply = {stopReason: 'stop', content: [{type: 'thinking', thinking: 'x'}, {type: 'text', text: '{"results":'}, {type: 'text', text: '[]}'}]};
  let prepared = {model: {api: 'openai-chatgpt-responses'}, auth: {mode: 'oauth'}};
  const sdk = async () => ({
    prepareSimpleCompletionModelForAgent: async params => { calls.push(['prepare', params]); return prepared; },
    completeWithPreparedSimpleCompletionModel: async params => { calls.push(['complete', params]); return reply; },
  });
  const search = params => webSearch(api, params, sdk);

  // Off unless the owner's config says so: nothing is even prepared.
  assert.deepEqual(await search({prompt: 'x'}), {ok: false, reason: 'off'});
  await writeFile(config, '{"meeting_prep_signin_search":"true"}');
  assert.deepEqual(await search({prompt: 'x'}), {ok: false, reason: 'off'});
  assert.equal(calls.length, 0);
  await writeFile(config, '{"meeting_prep_signin_search":true}');
  for (const prompt of ['', '  ', 'x'.repeat(2001), 5, undefined]) assert.equal((await search({prompt})).reason, 'invalid');

  // One request: the prompt alone, one tool, no session; the model asked for, or the main one.
  assert.deepEqual(await search({prompt: 'Search once.', model: 'openai/gpt-6.1-sol'}), {ok: true, text: '{"results":[]}'});
  assert.equal(calls.length, 2);
  assert.equal(calls[0][1].modelRef, 'openai/gpt-6.1-sol');
  const {context, options, cfg: passed} = calls[1][1];
  assert.equal(passed, cfg);  // never a changed copy: the setting for hosted search stays as it is
  assert.deepEqual(Object.keys(context), ['messages']);
  assert.deepEqual(context.messages.map(m => [m.role, m.content]), [['user', 'Search once.']]);
  const body = options.onPayload({model: 'm', input: [], tools: [{type: 'function', name: 'exec'}], tool_choice: 'auto'});
  assert.deepEqual(body.tools, [{type: 'web_search', external_web_access: false, search_context_size: 'low'}]);
  assert.equal(body.tool_choice, 'required');
  await search({prompt: 'Search once.', model: 'evil/../x'});
  assert.ok(!('modelRef' in calls[2][1]));

  // Only a ChatGPT sign-in, and no answer is no result.
  for (const apiName of ['openai-responses', 'azure-openai-responses', 'anthropic-messages', undefined]) {
    prepared = {model: {api: apiName}, auth: {}};
    calls.length = 0;
    assert.deepEqual(await search({prompt: 'x'}), {ok: false, reason: 'sign-in'});
    assert.equal(calls.length, 1);
  }
  prepared = {error: 'no model'};
  assert.equal((await search({prompt: 'x'})).reason, 'model');
  prepared = {model: {api: 'openai-chatgpt-responses'}, auth: {}};
  reply = {stopReason: 'error', content: [{type: 'text', text: 'half'}]};
  assert.equal((await search({prompt: 'x'})).reason, 'failed');
  reply = {stopReason: 'stop', content: []};
  assert.equal((await search({prompt: 'x'})).reason, 'empty');
  assert.deepEqual(await webSearch(api, {prompt: 'x'}, async () => { throw new Error('secret detail'); }), {ok: false, reason: 'failed'});

  // Only the Gateway's own operator clients, no agent tool; an older Gateway goes without.
  const methods = [];
  registerWebSearch({...api, registerGatewayMethod: (...args) => methods.push(args)});
  assert.equal(methods.length, 1);
  assert.equal(methods[0][0], METHOD);
  assert.deepEqual(methods[0][2], {scope: 'operator.write'});
  registerWebSearch({});

  // It can't leak into another turn: nothing else of ours puts the hosted search into a request, and nothing turns on
  // OpenClaw's setting that adds it to every turn (a review, a routine, the profile, a preparation, a chat).
  const root = new URL('..', import.meta.url);
  const sources = async (path, ends) => (await readdir(new URL(path, root), {recursive: true, withFileTypes: true}))
    .filter(f => f.isFile() && ends.some(e => f.name.endsWith(e)) && !/node_modules|__pycache__/.test(f.parentPath)).map(f => join(f.parentPath, f.name));
  const files = [...await sources('openclaw-plugin', ['.ts']), ...await sources('machine', ['.py', '.mjs']),
    ...(await readdir(root)).filter(n => /\.(py|mjs)$/.test(n)).map(n => new URL(n, root).pathname)];
  for (const file of files) {
    const text = await readFile(file, 'utf8');
    if (!file.endsWith('openclaw-plugin/web-search.ts')) {
      assert.ok(!/external_web_access|type['"]?\s*:\s*['"]web_search/.test(text), `${file} puts the hosted search into a request`);
      assert.ok(!/openaiCodex['"]?\]?\s*[:=]/.test(text), `${file} sets OpenClaw's hosted search`);
    }
    if (!/openclaw-plugin\/(web-search|index)\.ts$/.test(file)) assert.ok(!/webSearch\(api|searchBody|['"]assistant\.web_search['"]/.test(text), `${file} uses the search`);
  }
  assert.equal(searchBody({a: 1}).a, 1);
  console.log('ok');
} finally { await rm(folder, {recursive: true, force: true}); }
