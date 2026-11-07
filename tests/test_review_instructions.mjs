// A review always gets its instructions (AGENTS.md, the parts for reviews). A trial's reviews ran without them and left
// out dedupe_key on every to-do: their Gateway loaded the bridge before the service wrote its config, so AGENTS.md was
// read from a folder that didn't exist, silently. A Machine slow to answer review_context lost them too: a prompt hook
// past its time limit is dropped whole. Its own fixture (no tools/personal-assistant in the workspace, no config yet).
import assert from 'node:assert/strict';
import {mkdtempSync, mkdirSync, writeFileSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const FIXTURE = mkdtempSync(join(tmpdir(), 'assistant-instructions-'));
const W = join(FIXTURE, 'workspace'), config = join(FIXTURE, 'config', 'config.json');
mkdirSync(W, {recursive: true});
writeFileSync(join(W, 'USER.md'), '# USER.md\nThe owner prefers short answers.\n');
process.env.OPENCLAW_WORKSPACE = W;
process.env.ASSISTANT_CONFIG = config;  // not written yet: the service hasn't started
process.on('exit', () => { try { rmSync(FIXTURE, {recursive: true, force: true}); } catch {} });

const {registerReviewRecovery, appDir, REVIEW_CONTEXT_MS} = await import('../openclaw-plugin/review-recovery.ts');
const hooks = {}, options = {};
let answer = async () => ({review: null});
registerReviewRecovery({on(name, fn, opts) { hooks[name] = fn; options[name] = opts; }}, (action, args) => answer(action, args));
const ctx = {agentId: 'main', sessionKey: 'agent:main:assistant-review-signals-' + 'a'.repeat(32), runId: 'run-1', messageProvider: 'telegram'};
const instructions = text => text.includes('## Assistant instructions') && text.includes('## Reviewing signals');

// No config and no tools/personal-assistant: the plugin's own checkout
assert.equal(appDir(), ROOT);
assert.ok(instructions((await hooks.before_prompt_build({}, ctx)).prependSystemContext));
// The config the service writes after the Gateway started: read at the turn, not at load
mkdirSync(join(FIXTURE, 'app'));
writeFileSync(join(FIXTURE, 'app', 'AGENTS.md'), '# AGENTS.md\n\n## Reviewing signals\nFrom the configured install.\n');
mkdirSync(dirname(config), {recursive: true});
writeFileSync(config, JSON.stringify({app_dir: join(FIXTURE, 'app')}));
assert.equal(appDir(), join(FIXTURE, 'app'));
assert.ok((await hooks.before_prompt_build({}, {...ctx, runId: 'run-2'})).prependSystemContext.includes('From the configured install.'));
writeFileSync(config, JSON.stringify({app_dir: ROOT}));

// A service that never answers review_context: the instructions still come, well within the hook's time limit
assert.ok(options.before_prompt_build.timeoutMs >= REVIEW_CONTEXT_MS + 5000);
answer = action => action === 'review_context' ? new Promise(() => {}) : Promise.resolve({});
let started = Date.now();
const slow = await hooks.before_prompt_build({}, {...ctx, runId: 'run-3'});
assert.ok(instructions(slow.prependSystemContext));
assert.equal(slow.prependContext, undefined);
assert.ok(Date.now() - started < REVIEW_CONTEXT_MS + 1000);
// One that fails: the same, without the resume hint
answer = action => action === 'review_context' ? Promise.reject(new Error('busy')) : Promise.resolve({});
assert.ok(instructions((await hooks.before_prompt_build({}, {...ctx, runId: 'run-4'})).prependSystemContext));
// One that answers in time with an unfinished review: the hint comes along
answer = async action => action === 'review_context' ? {review: {id: 'r1', last_error: 'ai_timeout'}} : {};
const resumed = await hooks.before_prompt_build({}, {...ctx, runId: 'run-5'});
assert.ok(instructions(resumed.prependSystemContext));
assert.ok(resumed.prependContext.includes('Unfinished review r1'));
console.log('review instructions ok');
