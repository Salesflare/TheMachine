import {W} from './test-env.mjs';
import assert from 'node:assert/strict';
import {readFileSync, writeFileSync} from 'node:fs';
import {registerReviewRecovery, REVIEW_TOOLS, GBRAIN_READ_TOOLS, reviewTools, gbrainOn} from '../openclaw-plugin/review-recovery.ts';

// GBrain (gbrain.py) is optional and off by default: a review's tools and prompt stay exactly as they were until the
// owner turned it on and agreed; then only GBrain's read tools are added, never a write.
const CONFIG = process.env.ASSISTANT_CONFIG, base = JSON.parse(readFileSync(CONFIG, 'utf8'));
const setGbrain = value => writeFileSync(CONFIG, JSON.stringify(value === undefined ? base : {...base, gbrain: value}));
const hooks = {};
registerReviewRecovery({on(name, fn) { hooks[name] = fn; }}, async action => action === 'review_context' ? {review: null} : {recorded: true, active: true});
const review = {agentId: 'main', sessionKey: 'agent:main:assistant-review-signals-' + 'a'.repeat(32), runId: 'run-1', messageProvider: 'telegram',
  senderId: '1000001', chatId: '1000001'};
const profile = {...review, sessionKey: 'agent:main:assistant-review-profile-' + 'b'.repeat(32), runId: 'run-2'};
const blocked = async (toolName, ctx = review) => (await hooks.before_tool_call({toolName, params: {}}, ctx))?.block === true;
const prompt = async () => (await hooks.before_prompt_build({}, review)).prependContext;
const BEFORE = new Set(['assistant_signals', 'memory_search', 'memory_get', 'read', 'file_fetch', 'dir_list', 'dir_fetch', 'ls']);

// Off (no `gbrain` key, turned off, or on without consent): nothing changes
setGbrain(undefined);
const offPrompt = await prompt();
for (const state of [undefined, {on: false}, {on: true}, {on: true, consent_at: ''}, {on: 'yes', consent_at: '2026-10-28T08:00:00Z'}]) {
  setGbrain(state);
  assert.equal(gbrainOn(), false, JSON.stringify(state));
  assert.deepEqual([...reviewTools()].sort(), [...BEFORE].sort());
  assert.deepEqual([...REVIEW_TOOLS].sort(), [...BEFORE].sort());
  for (const name of ['gbrain__search', 'gbrain__get_page', 'openclawgbrain__search']) assert.equal(await blocked(name), true, name);
  assert.equal(await blocked('read'), false);
  assert.equal(await prompt(), offPrompt, 'the review prompt is unchanged while GBrain is off');
  assert.ok(!offPrompt.includes('GBrain'));
}

// On, with consent: GBrain's read tools, also under Code Mode names; its writes stay blocked
setGbrain({on: true, consent_at: '2026-10-28T08:00:00Z', linked: 'machine'});
assert.equal(gbrainOn(), true);
for (const name of GBRAIN_READ_TOOLS) {
  assert.equal(await blocked('gbrain__' + name), false, name);
  assert.equal(await blocked('openclawgbrain__' + name), false, name);
}
for (const name of ['put_page', 'put_pages', 'remember', 'forget', 'delete_page', 'edit_page', 'append_page', 'capture', 'add_link',
  'add_timeline_entry', 'submit_job', 'sync_brain', 'think', 'synthesize', 'fetch', 'file_upload', 'sources_add'])
  assert.equal(await blocked('gbrain__' + name), true, name);
assert.equal(await blocked('browser'), true);
assert.equal(await blocked('exec'), true);
assert.ok((await prompt()).includes('gbrain__search'));
// Only reviews: a profile draft keeps its own read-only list
assert.equal(await blocked('gbrain__search', profile), true);
// The read list never names a write (the same list as gbrain.py READ_TOOLS)
for (const name of GBRAIN_READ_TOOLS) assert.doesNotMatch(name, /put|remember|forget|delete|edit|append|capture|add_|remove|submit|sync|upload|purge|revert/);
const py = readFileSync(new URL('../gbrain.py', import.meta.url), 'utf8');
const listed = /READ_TOOLS = \(([^)]*)\)/s.exec(py)[1].match(/'([a-z_]+)'/g).map(x => x.slice(1, -1));
assert.deepEqual(listed, GBRAIN_READ_TOOLS);
setGbrain(undefined);
console.log('gbrain review gate ok');
