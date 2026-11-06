// The owner asks a to-do's chat to run what Claude Code or Codex prepared ("push it live"): the job's work folder
// sits inside the data folder (agent-jobs/<id>/work), and that folder is otherwise off-limits as credentials. The
// chat reads and runs the job's files there; the rest of the data folder (config, tokens, the job's own transcript
// and git folder, a link in the work folder out to it) stays refused, and the refusal says where the job's files are.
import {FIXTURE} from './test-env.mjs';
import assert from 'node:assert/strict';
import {mkdirSync, writeFileSync, symlinkSync} from 'node:fs';
import {join} from 'node:path';

// The data folder as on an install: config.json beside the database, the jobs in agent-jobs/.
const DATA = join(FIXTURE, 'data');
const JOB = join(DATA, 'agent-jobs', 'aj_2ec3c49846bb402e'), WORK = join(JOB, 'work');
mkdirSync(WORK, {recursive: true});
writeFileSync(join(DATA, 'config.json'), JSON.stringify({telegram_owner: '1000001', credentials: {}, accounts: [], database: join(DATA, 'events.sqlite')}));
writeFileSync(join(DATA, 'owner-token'), 'x');
writeFileSync(join(WORK, 'publish.sh'), '#!/bin/sh\necho published\n');
writeFileSync(join(JOB, 'turn-1.jsonl'), '{}');
symlinkSync(DATA, join(WORK, 'data'));
process.env.ASSISTANT_CONFIG = join(DATA, 'config.json');
const {registerReviewRecovery, jobWorkPath} = await import('../openclaw-plugin/review-recovery.ts');

const ctx = {agentId: 'main', sessionKey: 'agent:main:assistant-review-preparation-' + 'a'.repeat(32), runId: 'run', toolCallId: 'call'};
const hooks = {}; registerReviewRecovery({on(name, fn) { hooks[name] = fn; }}, async () => ({active: true}));
const run = (params, toolName = 'exec') => hooks.before_tool_call({toolName, params}, ctx);

// The job's prepared files: read, list, edit and run, by absolute path or from the folder itself.
assert.equal(jobWorkPath(join(WORK, 'publish.sh')), true);
assert.equal(await run({path: join(WORK, 'publish.sh')}, 'read'), undefined);
assert.equal(await run({path: join(WORK, 'RELEASE.md'), content: 'x'}, 'write'), undefined);
assert.equal(await run({command: `cat ${WORK}/publish.sh && ${WORK}/publish.sh`}), undefined);
assert.equal(await run({command: `cd ${WORK} && ./publish.sh`}), undefined);
assert.equal(await run({command: './publish.sh', cwd: WORK}), undefined);
assert.equal(await run({command: 'cat publish.sh', workdir: WORK}), undefined);

// The rest of the data folder is still refused, also through the job folder.
for (const path of [join(DATA, 'config.json'), join(DATA, 'owner-token'), join(JOB, 'turn-1.jsonl'), join(WORK, 'data', 'owner-token'),
  join(WORK, '..', '..', '..', 'owner-token'), join(DATA, 'agent-jobs', 'aj_nothex', 'work', 'x')])
  assert.ok((await run({path}, 'read'))?.block, path);
assert.ok((await run({path: join(WORK, 'data', 'new'), content: 'x'}, 'write'))?.block);
for (const command of [`cat ${DATA}/owner-token`, `cat ${WORK}/../../../owner-token`, `cat ${WORK}/publish.sh ${DATA}/config.json`,
  `cat ${WORK}/data/owner-token`, 'cat ../../owner-token'])
  assert.ok((await run({command, cwd: WORK}))?.block, command);

// The refusal says where a job's files can be read, so the turn can tell the owner what happened.
assert.match((await run({path: join(JOB, 'turn-1.jsonl')}, 'read')).blockReason, /work folder/);
assert.doesNotMatch((await run({path: join(DATA, 'config.json')}, 'read')).blockReason, /work folder/);
console.log('Preparations read and run an agent job\'s prepared files; the rest of the data folder stays refused.');
