// model-run-service.mjs: the same Gateway call `openclaw infer model run --gateway` makes (agent, modelRun, no prompt of
// its own, a one-off session; the admin scope only with a model override, as the CLI), checked requests, several turns
// at once over one process, and an exit when its input closes or it sits idle. The Gateway is stubbed.
import assert from 'node:assert/strict';
import {PassThrough} from 'node:stream';
import {call, request, serve, text} from '../model-run-service.mjs';

// Requests: a prompt, an optional provider/model and level; anything else is nothing
assert.equal(request({id: 'a1', prompt: '  '}), null);
assert.equal(request({id: 'a b', prompt: 'Hi'}), null);
assert.equal(request({id: 'a1', prompt: 'Hi', model: 'not a model'}), null);
assert.equal(request({id: 'a1', prompt: 'Hi', thinking: 'very high!'}), null);
assert.equal(request({id: 'a1', prompt: 'x'.repeat(200001)}), null);
assert.deepEqual(request({id: 'a1', prompt: 'Hi', model: 'openai/gpt-5.5', thinking: 'low', timeout_ms: 5}),
  {id: 'a1', prompt: 'Hi', provider: 'openai', model: 'gpt-5.5', thinking: 'low', timeout: 1000});
assert.equal(request({id: 'a1', prompt: 'Hi', timeout_ms: 10 ** 9}).timeout, 300000);

// The call: as the CLI's, a new session each time
const [plain, plainExtra] = call(request({id: 'a1', prompt: 'Hi'}));
assert.equal(plain.agentId, 'main');
assert.match(plain.sessionId, /^model-run-[0-9a-f-]{36}$/);
assert.equal(plain.sessionKey, `agent:main:explicit:${plain.sessionId}`);
assert.equal(plain.message, 'Hi');
assert.equal(plain.modelRun, true);
assert.equal(plain.promptMode, 'none');
assert.equal(plain.cleanupBundleMcpOnRunEnd, true);
assert.equal(plain.provider, undefined);
assert.equal('thinking' in plain, false);
assert.deepEqual(plainExtra, {expectFinal: true, timeoutMs: 60000, progress: false});  // the CLI's own client and scopes
const [picked, pickedExtra] = call(request({id: 'a2', prompt: 'Hi', model: 'openai/gpt-5.5', thinking: 'low'}));
assert.equal(picked.provider, 'openai');
assert.equal(picked.model, 'gpt-5.5');
assert.equal(picked.thinking, 'low');
assert.notEqual(picked.sessionId, plain.sessionId);
assert.deepEqual(pickedExtra, {expectFinal: true, timeoutMs: 60000, progress: false, clientName: 'gateway-client', mode: 'backend', scopes: ['operator.admin']});

// The reply's text, as the CLI joins it
assert.equal(text({result: {payloads: [{text: 'One'}, {mediaUrl: 'x'}, {text: 'two '}]}}), 'One\ntwo');
assert.equal(text({result: {payloads: []}}), null);

// One process, several turns at once, each answered by its id; a failure or timeout is said, never its text
const input = new PassThrough(), output = new PassThrough();
const calls = [];
let exited = null;
const runtime = async () => ({callGatewayFromCli: async (method, opts, params, extra) => {
  calls.push([method, opts, params, extra]);
  if (params.message === 'slow') await new Promise(done => setTimeout(done, 50));
  if (params.message === 'fail') throw new Error('gateway closed (1006) secret detail');
  if (params.message === 'late') throw new Error('gateway timeout after 1000ms');
  return {result: {payloads: [{text: 'Said: ' + params.message}]}};
}});
const lines = [];
output.on('data', chunk => lines.push(...chunk.toString().split('\n').filter(Boolean).map(l => JSON.parse(l))));
await serve({runtime, input, output, exit: code => { exited = code; }, idleMs: 60000});
for (const [id, prompt] of [['s1', 'slow'], ['s2', 'quick'], ['s3', 'fail'], ['s4', 'late']]) input.write(JSON.stringify({id, prompt}) + '\n');
input.write('not json\n');
input.write(JSON.stringify({id: 's5', prompt: ''}) + '\n');
await new Promise(done => setTimeout(done, 150));
assert.deepEqual(lines[0], {ready: true});
const by = Object.fromEntries(lines.slice(1).map(l => [l.id, l]));
assert.deepEqual(by.s1, {id: 's1', ok: true, text: 'Said: slow'});
assert.deepEqual(by.s2, {id: 's2', ok: true, text: 'Said: quick'});
assert.deepEqual(by.s3, {id: 's3', error: 'unavailable'});
assert.deepEqual(by.s4, {id: 's4', error: 'timeout'});
assert.deepEqual(by.s5, {id: 's5', error: 'unavailable'});
assert.ok(lines.findIndex(l => l.id === 's2') < lines.findIndex(l => l.id === 's1'), 'a quick turn does not wait for a slow one');
assert.equal(calls.length, 4);
assert.ok(calls.every(([method, opts]) => method === 'agent' && opts.json === true));
input.end();
await new Promise(done => setTimeout(done, 20));
assert.equal(exited, 0, 'it exits when the service closes its input');

// Idle: it exits on its own
let idleExit = null;
await serve({runtime, input: new PassThrough(), output: new PassThrough(), exit: code => { idleExit = code; }, idleMs: 20});
await new Promise(done => setTimeout(done, 60));
assert.equal(idleExit, 0);
console.log('model-run-service ok');
