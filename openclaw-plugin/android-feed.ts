// Reuse the Gateway's existing phone feed. No calls to the phone, and never a drain of the whole queue.
import * as systemEvents from 'openclaw/plugin-sdk/system-event-runtime';
import { DatabaseSync } from 'node:sqlite';
import { createHash, createHmac, randomBytes } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';

// A notification's text waits in android_inbox sealed with the app's message key (message_seal.py, INBOX), unless
// message protection is off or the key isn't made yet. Read each time: tiny, and the app may make it after we start.
export function messageKey(config: any): Buffer | null {
  if (config?.message_protection === false || !config?.database) return null;
  try {
    const key = Buffer.from(readFileSync(join(dirname(config.database), 'message-content.key'), 'utf8').trim(), 'base64');
    return key.length === 32 ? key : null;
  } catch { return null; }
}

export function sealText(key: Buffer, text: string): string {
  if (!text) return text;
  const derive = (name: string) => createHmac('sha256', key).update(name).digest();
  const nonce = randomBytes(16), data = Buffer.from(text, 'utf8');
  const stream = createHash('shake256', {outputLength: data.length}).update(derive('mc1-inbox-seal')).update(nonce).digest();
  const sealed = Buffer.from(data.map((b, i) => b ^ stream[i]));
  const tag = createHmac('sha256', derive('mc1-inbox-mac')).update('mci1:').update(nonce).update(sealed).digest().subarray(0, 16);
  return 'mci1:' + Buffer.concat([nonce, sealed, tag]).toString('base64');
}

// nodeId: the paired phone's OpenClaw node id (the Android account's `node_id` in config).
export function notificationEnvelope(entry: any, nodeId: string) {
  if (!entry?.contextKey?.startsWith('notification:') || !entry.id || !Number.isFinite(entry.ts)) return null;
  const match = /^Notification (posted|removed) \(node=([a-f0-9]+) key=(.*?)(?: package=([^ )]+))?\)(?:: ([\s\S]*))?$/.exec(entry.text || '');
  if (!match || !nodeId || match[2] !== nodeId || match[4] === 'ai.openclaw.app') return null;
  let text = match[5] || '';
  const sensitive = /verification code|security code|one.time (?:code|password)|\bOTP\b|verificatiecode/i.test(text);
  if (sensitive) text = '[One-time security code omitted]';
  return { id: entry.id, at_ms: entry.ts, change: match[1], package_name: match[4] || 'unknown',
    notification_key_hash: createHash('sha256').update(match[3]).digest('hex'),
    text, security_code_omitted: sensitive };
}

// The main session's event queue holds at most 20 events, and the Gateway drops a phone notification that arrives while
// it is full. Only a main-session turn empties it, and with OpenClaw's heartbeat off (QUIET_OPENCLAW in installer.py)
// that is only when the owner writes in the main chat: a few hours of notifications filled it and every later one was
// lost. So once more than ROOM events wait, the oldest phone notifications this feed has saved leave the queue, one by
// one, until ROOM are left. The rest stay for the main chat (or a heartbeat the owner turned on) to see, and other
// events (other plugins', exec results) are never touched. No model turn, no phone call.
export const ROOM = 10;
const MAIN = 'agent:main:main';

export function savedToRelease(queue: any[], saved: Set<string>, room = ROOM) {
  const over = queue.length - room;
  if (over <= 0) return [];
  return queue.filter(e => e?.id && saved.has(e.id) && e.contextKey?.startsWith('notification:'))
    .sort((a, b) => a.ts - b.ts).slice(0, over);
}

function releaseSaved(saved: Set<string>) {
  // Older Gateways without targeted removal keep the earlier behavior: peek only.
  const consume = (systemEvents as any).consumeSelectedSystemEventEntries;
  if (typeof consume !== 'function') return;
  const release = savedToRelease(systemEvents.peekSystemEventEntries(MAIN, 'main'), saved);
  if (release.length) consume(MAIN, release.map(e => ({id: e.id})));
}

export function registerAndroidFeed(api: any) {
  let timer: ReturnType<typeof setInterval> | undefined;
  let stopped = true, busy = false;
  let generation = 0;
  let report: any;
  let config: any;
  let lastRecorded: string | null = null;
  let lastHealth = 0;
  const saved = new Set<string>();
  async function capture() {
    if (stopped || busy) return;
    const captureGeneration = generation;
    busy = true;
    try {
      if (!config) {
        const loaded = JSON.parse(await readFile(process.env.ASSISTANT_CONFIG || join(homedir(), '.local/share/personal-assistant/config.json'), 'utf8'));
        if (stopped || captureGeneration !== generation) return;
        config = loaded;
      }
      if (stopped || captureGeneration !== generation) return;
      const account = config.accounts.find((a: any) => a.transport === 'openclaw-feed' && a.node_id);
      if (!account) return;
      const entries = systemEvents.peekSystemEventEntries(MAIN, 'main').map((e: any) => notificationEnvelope(e, account.node_id)).filter(e => e && !saved.has(e.id));
      if (!entries.length && Date.now() - lastHealth < 30000) { releaseSaved(saved); return; }
      const db = new DatabaseSync(config.database, {timeout: 2000});
      try {
        db.exec('PRAGMA busy_timeout=2000; BEGIN IMMEDIATE');
        db.exec('CREATE TABLE IF NOT EXISTS android_receipts(id TEXT PRIMARY KEY,account_id TEXT NOT NULL,processed_at TEXT NOT NULL)');
        const insert = db.prepare('INSERT OR IGNORE INTO android_inbox(id,payload,received_at) SELECT ?,?,? WHERE NOT EXISTS (SELECT 1 FROM android_receipts WHERE id=? AND account_id=?)');
        const key = entries.length ? messageKey(config) : null;
        for (const entry of entries) insert.run(entry.id, JSON.stringify(key ? {...entry, text: sealText(key, entry.text)} : entry), new Date().toISOString(), entry.id, account.id);
        const meta = db.prepare('INSERT INTO android_feed_health(id,last_checked,last_recorded,error) VALUES(1,?,?,NULL) ON CONFLICT(id) DO UPDATE SET last_checked=excluded.last_checked,last_recorded=coalesce(excluded.last_recorded,android_feed_health.last_recorded),error=NULL');
        if (entries.length) lastRecorded = new Date(Math.max(...entries.map((e: any) => e.at_ms))).toISOString();
        meta.run(new Date().toISOString(), lastRecorded);
        db.exec('COMMIT');
        for (const entry of entries) saved.add(entry.id);
        if (saved.size > 1000) { const keep=[...saved].slice(-500); saved.clear(); for(const id of keep)saved.add(id); }
        lastHealth=Date.now();
      } catch (error) { try {db.exec('ROLLBACK')} catch {} throw error; }
      finally { db.close(); }
      // Only after the commit: a notification leaves the queue once it is safely in the database.
      releaseSaved(saved);
      report?.clearFailure();
    } catch {
      // Private notification data and raw errors are never logged.
      if (config?.database && !stopped && captureGeneration === generation) {
        let db;
        try {
          db = new DatabaseSync(config.database, {timeout: 2000});
          db.prepare("UPDATE android_feed_health SET error='android_feed_capture_failed' WHERE id=1").run();
        } catch {} finally { db?.close(); }
      }
      report?.reportFailure(new Error('android_feed_capture_failed'));
    } finally { busy = false; }
  }
  api.registerService({id:'personal-assistant-android-feed',
    start(ctx: any) { generation++; stopped=false; report=ctx.serviceHealth; void capture(); timer=setInterval(()=>void capture(),250); timer.unref(); },
    stop() { generation++; stopped=true; config=undefined; if(timer)clearInterval(timer); timer=undefined; }
  });
  // Capture on the existing heartbeat path before its pending events are consumed.
  api.on('heartbeat_prompt_contribution', async (event: any) => {
    if (event.agentId === 'main' && event.sessionKey === MAIN) await capture();
  });
  // Only peek the authenticated runtime queue. Never interpret user-supplied
  // prompt text as a phone notification when it has already been drained.
  api.on('before_prompt_build', async (_event: any, ctx: any) => {
    if (ctx.agentId === 'main' && ctx.sessionKey === MAIN) await capture();
  });
}
