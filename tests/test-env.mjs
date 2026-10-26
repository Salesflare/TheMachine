// Shared fixture for the Node tests: a temporary OpenClaw workspace and assistant config, so
// tests never read the real ~/.openclaw or ~/.local/share/personal-assistant. Import it first.
import {mkdtempSync, mkdirSync, writeFileSync, symlinkSync, rmSync} from 'node:fs';
import {tmpdir, homedir} from 'node:os';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';

export const H = homedir();
export const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
export const FIXTURE = mkdtempSync(join(tmpdir(), 'assistant-test-'));
export const W = join(FIXTURE, 'workspace');
export const OWNER = '1000001';
mkdirSync(join(W, 'tools'), {recursive: true});
symlinkSync(ROOT, join(W, 'tools', 'personal-assistant'));
writeFileSync(join(W, 'USER.md'), '# USER.md\nThe owner prefers short answers.\n');
const config = join(FIXTURE, 'config', 'config.json');
mkdirSync(dirname(config), {recursive: true});
writeFileSync(config, JSON.stringify({telegram_owner: OWNER, credentials: {}, accounts: []}));
process.env.OPENCLAW_WORKSPACE = W;
process.env.ASSISTANT_CONFIG = config;
process.on('exit', () => { try { rmSync(FIXTURE, {recursive: true, force: true}); } catch {} });
