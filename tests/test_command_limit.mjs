import {H} from './test-env.mjs';
import assert from 'node:assert/strict';
import {registerReviewRecovery, COMMAND_SECONDS, COMMANDS_HERE, commandLimit} from '../openclaw-plugin/review-recovery.ts';

// One slow command never holds a background run: an awaited command without a limit of its own gets one.
const prep = {agentId: 'main', sessionKey: 'agent:main:assistant-review-preparation-' + 'a'.repeat(32), runId: 'run', toolCallId: 'call'};
const routine = {...prep, sessionKey: 'agent:main:assistant-review-routine-' + 'b'.repeat(32)};
const install = (reply, api = {}) => {
  const hooks = {}, calls = [];
  registerReviewRecovery({...api, on(name, fn) { hooks[name] = fn; }}, async (action, args) => { calls.push({action, args}); return reply; });
  return {calls, hooks, run: (params, ctx = prep, event = {}) => hooks.before_tool_call({toolName: 'exec', params, ...event}, ctx)};
};
const asked = install({active: true}), ahead = install({active: true, ahead: true});
const slow = {command: 'find ' + H + ' -name "*invoice*"', awaitResults: true};

// The whole call is kept; only the limit is added. Work prepared ahead gets the short one, Do it the longer one.
assert.deepEqual(await ahead.run(slow), {params: {...slow, timeoutSeconds: COMMAND_SECONDS.ahead}});
assert.deepEqual(await asked.run(slow), {params: {...slow, timeoutSeconds: COMMAND_SECONDS.asked}});
assert.deepEqual(COMMAND_SECONDS, {ahead: 120, asked: 600});
assert.equal(ahead.calls.at(-1).args.awaited, true);
assert.deepEqual(ahead.calls.at(-1).args.params, slow);  // journaled as the run asked it
assert.deepEqual(slow, {command: slow.command, awaitResults: true});  // the event itself isn't changed
// Code Mode names the same tool through its namespace.
assert.equal((await ahead.run(slow, prep, {toolName: 'openclaw__exec'})).params.timeoutSeconds, 120);
// A routine only reads (gh and git), so it always has the short limit.
assert.equal((await asked.run({command: 'git ls-remote https://github.com/example/app', awaitResults: true}, routine)).params.timeoutSeconds, 120);

// Left as it is: its own limit (0 included), not awaited, in the background, and everything that isn't a command.
for (const params of [{...slow, timeoutSeconds: 900}, {...slow, timeoutSeconds: 0}, {...slow, timeout: 900}, {command: 'ls'}, {command: 'ls', awaitResults: false},
  {command: 'npm run build', background: true}, {command: 'npm run build', yieldMs: 60000}]) {
  assert.equal(await ahead.run(params), undefined, JSON.stringify(params));
  assert.equal(ahead.calls.at(-1).args.awaited, undefined);
}
assert.equal(await ahead.run({code: 'tools.exec({command:"ls"})', awaitResults: true}, prep, {toolKind: 'code_mode_exec'}), undefined);
assert.equal(await ahead.run({ids: ['x'], awaitResults: true}, prep, {toolName: 'agents_wait'}), undefined);
// Codex's own shell has no awaitResults: its calls are never rewritten (Codex refuses a rewritten one).
assert.equal(await ahead.run({command: 'find ' + H}, prep, {toolName: 'exec_command'}), undefined);
// The owner's own chat with the agent, and any session that isn't a Machine run.
for (const sessionKey of ['agent:main:main', 'agent:main:telegram:direct:1', 'agent:main:subagent:x']) assert.equal(await ahead.run(slow, {...prep, sessionKey}), undefined);

// A limit the owner set in OpenClaw stands, whichever it is, for every agent or for this one.
for (const config of [{tools: {exec: {timeoutSeconds: 3600}}}, {tools: {exec: {timeoutSeconds: 30}}},
  {agents: {entries: {main: {tools: {exec: {timeoutSeconds: 60}}}}}}, {agents: {list: [{id: 'main', tools: {exec: {timeoutSec: 60}}}]}}]) {
  assert.equal(await install({active: true, ahead: true}, {config}).run(slow), undefined, JSON.stringify(config));
  assert.equal(await install({active: true, ahead: true}, {runtime: {config: {current: () => config}}}).run(slow), undefined);
}
for (const config of [{}, {tools: {exec: {notifyOnExit: false}}}, {agents: {entries: {other: {tools: {exec: {timeoutSeconds: 60}}}}}}])
  assert.equal((await install({active: true, ahead: true}, {config}).run(slow)).params.timeoutSeconds, 120, JSON.stringify(config));

// The browser lease's own wait (the job message's exact command, 10 minutes) fits inside the limit.
const lease = wait => ({command: `python3 integrations/browser-lease.py claim --owner assistant-1a2b3c4d --minutes 30${wait}`, awaitResults: true});
assert.equal((await ahead.run(lease(' --wait 10'))).params.timeoutSeconds, 720);
assert.equal((await asked.run(lease(' --wait=10'))).params.timeoutSeconds, 1200);
assert.equal(commandLimit(lease(''), true), 120);
assert.equal(commandLimit({command: 'echo claim; find ' + H + ' --wait 10'}, true), 120);

// Nothing is allowed that wasn't, nothing refused that was allowed.
assert.equal((await ahead.run({command: 'cat ' + H + '/.ssh/id_rsa', awaitResults: true})).block, true);
assert.equal((await asked.run({command: 'git push', awaitResults: true}, routine)).block, true);
assert.equal((await install({active: false}).run(slow)).block, true);
assert.equal((await asked.run({command: 'npm run deploy', awaitResults: true})).block, undefined);

// A preparation is told, in its cached system context; a routine (gh and git only) has no need to be.
assert.ok((await asked.hooks.before_prompt_build({}, prep)).prependSystemContext.includes(COMMANDS_HERE));
assert.ok(!(await asked.hooks.before_prompt_build({}, routine)).prependContext.includes(COMMANDS_HERE));
assert.ok(COMMANDS_HERE.length < 300);
console.log('Command limit: an awaited command without its own limit is bounded in background runs, and nothing else changes.');
