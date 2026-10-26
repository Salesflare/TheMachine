import {readFile} from 'node:fs/promises';
import {readFileSync} from 'node:fs';
import {dirname, resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {homedir} from 'node:os';

const HOME = homedir();
const CONFIG_PATH = process.env.ASSISTANT_CONFIG || `${HOME}/.local/share/personal-assistant/config.json`;
function assistantConfig(): any {
  try { return JSON.parse(readFileSync(CONFIG_PATH, 'utf8')); } catch { return {}; }
}
// The owner's private Telegram chat (config `telegram_owner`). Empty means nothing matches.
const ownerChat = () => String(assistantConfig().telegram_owner || '');
const sameChat = (value: any) => { const owner = ownerChat(); return !!owner && String(value).replace(/^telegram:/, '') === owner; };
// Review turns are started by the service in isolated assistant-review sessions; these hooks
// bind ownership, remind retries and release claims. No source inference here.
export function privateReviewContext(ctx: any) {
  return ctx.agentId === 'main' &&
    (ctx.sessionKey === 'agent:main:main' || /^agent:main:assistant-review[-:]/.test(ctx.sessionKey || '')) &&
    (!ctx.channel || ctx.channel === 'telegram') &&
    (!ctx.messageProvider || ctx.messageProvider === 'telegram') &&
    (!ctx.senderId || sameChat(ctx.senderId)) &&
    (!ctx.chatId || sameChat(ctx.chatId));
}

// A conservative last-mile guard, not a general notification/content filter.
// Only known review bookkeeping sentences in a host-proven background run
// qualify; a mixed reply containing a real alert must remain deliverable.
export function processingOnlyReviewSummary(text: string) {
  const sentences = String(text || '').trim().split(/\n+|(?<=[.!?])\s+/).filter(Boolean);
  return sentences.length > 0 && sentences.every(sentence =>
    /^(?:Resumed and finished (?:the|an) (?:interrupted|unfinished) review(?:, then (?:completed|committed) (?:one|two|three|1|2|3) (?:more )?batch(?:es)?)?(?:: \d+ of \d+ signal slots assessed)?|(?:Reviewed|Assessed|Processed|Checked) \d+ signals|\d+ of \d+ signal slots assessed(?:; no new suggestion was warranted)?|Saved (?:one|two|three|\d+) [\w -]*suggestions?|No (?:new|useful) suggestion was warranted|The (?:empty|incomplete) [\w -]+ remain(?:s)? pending|The service.s review-budget gate stopped further claims; this was not a complete inbox review|This was (?:not a complete inbox review|a bounded review, not a complete inbox or history check))[.]?$/i.test(sentence));
}

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || `${HOME}/.openclaw/workspace`;
// Where this project is installed (AGENTS.md, PREPARATION.md, the service code). Config `app_dir`.
const APP_DIR = resolve(String(assistantConfig().app_dir || `${WORKSPACE}/tools/personal-assistant`).replace(/^~(?=\/|$)/, HOME));
// Review turns may only read: the signals tool, memory lookups and read-only file access.
// Works on any runtime: OpenClaw tool calls pass this hook on the embedded runtime (where file
// and shell access are OpenClaw tools too) and on Codex app-server (whose own built-in shell
// does not). A per-turn toolsAllow would also trim the prompt, but Codex rejects it, and a
// review can run on either runtime, so the guard is applied at call time instead.
export const REVIEW_TOOLS = new Set(['assistant_signals', 'memory_search', 'memory_get', 'read', 'file_fetch', 'dir_list', 'dir_fetch', 'ls']);
const reviewSession = (key: string) => /^agent:main:assistant-review-signals-/.test(key || '');
// Code Mode calls plugin tools through a namespace, and the hook sees e.g. "openclawassistant_signals"
// or "openclaw__assistant_signals". Compare on the plain tool name.
export const plainToolName = (name: string) => String(name || '').replace(/^openclaw_*/, '');
const codeModeRunner = (event: any, ctx: any) => event.toolKind === 'code_mode_exec' || ctx.toolKind === 'code_mode_exec';
const preparationSession = (key: string) => /^agent:main:assistant-review-preparation-/.test(key || '');
// assistant profile: one read-only turn that drafts USER.md lines from the owner's own messages.
const profileSession = (key: string) => /^agent:main:assistant-review-profile-/.test(key || '');
// Find my skills (Settings > Skills > Import): reads the owner's claude.ai and chatgpt.com skills in the Machine's
// browser and reports them with assistant_signals skills_found. The browser and read-only tools; no shell, no writes.
const skillsSession = (key: string) => /^agent:main:assistant-review-skills-/.test(key || '');
export const SKILLS_TOOLS = new Set([...REVIEW_TOOLS, 'browser']);

// Preparations are the main agent working on an accepted task, with as few restrictions as
// possible: OpenClaw cannot show an approval prompt for these background
// runs ("no approval-capable initiating surface"), so asking was the same as refusing. Everything
// runs, browser clicks and typing included, except a short hard-block list: sending messages
// (drafts go out via the reviewed Send button), credentials, destructive/system commands, writes
// to Google or GitHub (except filing and commenting on issues), and edits to the assistant's own code and config. Guardrails against
// mistakes, not a sandbox.
const SECRET_PATHS = [`${HOME}/.local/share/personal-assistant`, `${HOME}/.openclaw/secrets`, `${HOME}/.openclaw/credentials`,
  `${HOME}/.config/gogcli`, `${HOME}/.ssh`, `${HOME}/.gnupg`, ...configuredSecretDirs()];
// Some service credentials (the gog keyring password, API env files) live in Private/ folders.
function configuredSecretDirs() {
  try {
    const config = JSON.parse(readFileSync(CONFIG_PATH, 'utf8'));
    return [dirname(CONFIG_PATH), ...Object.values(config.credentials || {}).map(path => dirname(String(path)))];
  } catch { return []; }
}
// This policy, the Gateway config and service units.
const PROTECTED_PATHS = [APP_DIR, `${HOME}/.openclaw/openclaw.json`, `${HOME}/.openclaw/extensions`, `${HOME}/.config/systemd`];
const WRITE_TOOLS = new Set(['write', 'edit', 'apply_patch', 'multi_edit']);
const SHELL_TOOLS = new Set(['exec', 'bash', 'shell', 'shell_command', 'exec_command', 'local_shell']);

const absolute = (path: string) => resolve(WORKSPACE, String(path).replace(/^~(?=\/|$)/, HOME));
const under = (dirs: string[]) => (path: string) => dirs.some(dir => absolute(path) === dir || absolute(path).startsWith(dir + '/'));
const secretPath = under(SECRET_PATHS), protectedPath = under(PROTECTED_PATHS);
const pathParams = (params: any) => ['path', 'file_path', 'filePath', 'file', 'dir', 'directory', 'target']
  .map(key => params?.[key]).filter(value => typeof value === 'string');
function patchPaths(params: any) {
  const text = [params?.patch, params?.input, params?.command, params?.content].find(v => typeof v === 'string' && v.includes('*** ')) || '';
  return [...String(text).matchAll(/^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)$/gm)].map(m => m[1].trim());
}
// Reading contents under a parent folder (rg token ~) would also print credentials.
// Listing names there (find, ls, du) is fine.
const coversSecret = (word: string, cwd: string) => {
  const path = resolve(cwd, word.replace(/^~(?=\/|$)/, HOME));
  return SECRET_PATHS.some(dir => path === dir || path.startsWith(dir + '/') || dir.startsWith(path === '/' ? '/' : path + '/'));
};
const CONTENT_READERS = /(?:^|[\s|;&(])(?:rg|grep|egrep|ag|ack|cat|tar|zip|cp|rsync|scp)\s/;

// Sending mail or chat directly is never allowed; it belongs on the reviewed Send button.
const OWNER_SERVICE = /owner-token|X-Assistant-Owner|confirm_action/i;

export function commandText(params: any) {
  const command = params?.command ?? params?.cmd;
  return Array.isArray(command) ? command.join(' ') : String(command ?? '');
}

// Small shell lexer: keep quoted arguments together, but check every separate command.
// This catches ordinary mistakes; Python and other legitimate tools remain available.
export function commandStages(text: string) {
  const tokens = text.match(/(?:"(?:\\.|[^"\\])*"|'[^']*'|\\.|[^\s;&|<>])+|&&|\|\||[;&|<>]+/g) || [];
  const stages: string[][] = [[]];
  for (const token of tokens) {
    if (/^[;&|]+$/.test(token)) stages.push([]);
    else stages.at(-1)!.push(token.replace(/^(['"])(.*)\1$/, '$2'));
  }
  return stages.filter(s => s.length);
}
function protectedOutput(stage: string[], cwd: string) {
  const paths: string[] = [];
  for (let i=0;i<stage.length;i++) {
    const t=stage[i];
    if (/^(?:\d*)>>?$/.test(t) || ['-o','--output','--output-file','--dump-header','-D','--out'].includes(t)) paths.push(stage[i+1]||'');
    if (/^(?:--output(?:-file)?|--dump-header|--out)=/.test(t)) paths.push(t.slice(t.indexOf('=')+1));
  }
  const command=stage.findIndex(t=>/^(?:sort|uniq|tee|cp|mv|install)$/.test(t));
  if (command>=0) {
    const args=stage.slice(command+1).filter(t=>!t.startsWith('-'));
    if (['cp','mv','install'].includes(stage[command])) paths.push(args.at(-1)||'');
    else if (stage[command]==='uniq' && args.length>1) paths.push(args[1]);
    else if (stage[command]==='tee') paths.push(...args);
  }
  return paths.some(p=>p && PROTECTED_PATHS.some(dir=>resolve(cwd,p.replace(/^~(?=\/|$)/,HOME))===dir || resolve(cwd,p.replace(/^~(?=\/|$)/,HOME)).startsWith(dir+'/')));
}

export function preparationReadOnly(event: any) {
  const name=plainToolName(event.toolName);
  if (REVIEW_TOOLS.has(name)) return name!=='assistant_signals' || ['status','events','preparation_history'].includes(event.params?.action);
  return name==='web_search' || name==='web_fetch';
}

// Keep HTTP journal records below the service's 64 KB envelope. Full oversized
// outputs remain in the retained agent transcript; a missing suffix is never
// treated as a negative receipt or permission to replay an operation.
function journalValue(value:any) {
  const text=JSON.stringify(value ?? null);
  return Buffer.byteLength(text,'utf8')<=22000 ? value ?? null : {clipped:true,preview:text.slice(0,5000),full:'retained session transcript'};
}

// undefined = run; {block} = refused, with the reason shown to the agent.
// Loose on purpose: when the owner asks or confirms, the agent does it. Only reading
// credentials and rewriting the assistant/Gateway mid-run are refused.
export function preparationToolPolicy(event: any, ctx: any): undefined | {block: string} {
  const name = plainToolName(event.toolName), params = event.params || {};
  if (codeModeRunner(event, ctx)) return undefined;
  if (pathParams(params).some(secretPath)) return {block: 'Preparations do not read credentials.'};
  if (WRITE_TOOLS.has(name)) {
    const paths = [...pathParams(params), ...patchPaths(params)];
    if (paths.some(secretPath)) return {block: 'Preparations do not touch credentials.'};
    if (paths.some(protectedPath)) return {block: 'Preparations do not edit the running assistant or Gateway. For The Machine, fix a git clone under its fix folder and offer a merge (PREPARATION.md); otherwise describe the fix in the result.'};
    return undefined;
  }
  if (!SHELL_TOOLS.has(name)) return undefined;
  const text = commandText(params), cwd = absolute(params.cwd || params.workdir || WORKSPACE);
  if (OWNER_SERVICE.test(text) || SECRET_PATHS.some(dir => text.includes(dir)) || /\bgog\s+auth\b/.test(text))
    return {block: 'Preparations do not use credentials or owner approvals.'};
  for (const stage of commandStages(text)) {
    if (protectedOutput(stage,cwd)) return {block: 'Preparations do not edit the running assistant or Gateway. For The Machine, fix a git clone under its fix folder and offer a merge (PREPARATION.md); otherwise describe the fix in the result.'};
  }
  if (CONTENT_READERS.test(text) && text.split(/[\s|;&()'"=]+/).some(word => /^[\/~.]/.test(word) && coversSecret(word, cwd)))
    return {block: 'That path includes credential folders. Search a narrower folder (e.g. ~/Documents, ~/Downloads or the workspace).'};
  return undefined;
}

// Reviews and preparations never need the service or account credentials.
const readsSecret = (event: any) => pathParams(event.params || {}).some(secretPath);

// USER.md is not loaded into isolated sessions by default; reviews and preparations need it.
// The only files a review or preparation context reads, by name; nothing else can become a path here.
const USER_MD = resolve(WORKSPACE, 'USER.md');
const PREPARATION_MD = resolve(APP_DIR, 'PREPARATION.md');
const AGENTS_MD = resolve(APP_DIR, 'AGENTS.md');
const readContextFile = (name: string) => {
  switch (name) {
    case 'USER': return readFile(USER_MD, 'utf8');
    case 'PREPARATION': return readFile(PREPARATION_MD, 'utf8');
    case 'AGENTS': return readFile(AGENTS_MD, 'utf8');
    default: return Promise.reject(new Error(`not a context file: ${name}`));
  }
};
export async function contextFile(name: string, heading: string, limit = 20000, only = (text: string) => text) {
  try {
    const text = only((await readContextFile(name)).trim()).trim();
    return `\n\n## ${heading}\n${text.length > limit ? text.slice(0, limit) + '\n[…shortened]' : text}`;
  } catch { return ''; }
}
export const ownerContext = () => contextFile('USER', 'About the owner (USER.md)');
// Standing Do it rules; prepended here because the runner caps the job message at 20000 characters.
const preparationRules = () => contextFile('PREPARATION', 'Preparation rules (tools/personal-assistant/PREPARATION.md)', 30000);  // the whole file: every rule applies to each Do it
// A review gets AGENTS.md without the sections for other work: Do it turns get theirs from PREPARATION.md, and operations,
// repository and security maintenance are for people and agents working on The Machine. Each review step resends this
// context, so what a review never uses costs on every step. Its lessons and everything about reviewing stay.
export const NOT_FOR_REVIEWS = ['Preparing accepted suggestions', 'Operations', 'Public repository hygiene', 'Security maintenance'];
export const forReviews = (text: string) => text.split(/^(?=## )/m)
  .filter(part => !NOT_FOR_REVIEWS.some(title => part.startsWith(`## ${title}\n`) || part.trim() === `## ${title}`)).join('');
const assistantInstructions = () => contextFile('AGENTS', 'Assistant instructions (tools/personal-assistant/AGENTS.md, the parts for reviews)', 50000, forReviews);

// The review run that currently owns each session, recorded by the prompt hook. The tool's own
// execute() reads it to bind ownership. The hook must not rewrite tool parameters: Codex
// app-server refuses a tool call whose parameters a hook rewrote (seen live on October 11).
const sessionRuns = new Map<string, string>();
export const currentReviewRun = (sessionKey: string) => sessionRuns.get(sessionKey);

export function registerReviewRecovery(api: any, call: (action: string, args?: any) => Promise<any>) {
  const runs = new Map<string, {session: string; started: number; reviewTouched: boolean}>();
  const background = (ctx: any) => privateReviewContext(ctx) && !!ctx.runId &&
    ctx.inputProvenance?.kind !== 'external_user' &&
    !/^agent:main:assistant-review-(?:preparation|profile|skills)-/.test(ctx.sessionKey || '') &&
    (/^agent:main:assistant-review[-:]/.test(ctx.sessionKey || '') ||
      (ctx.inputProvenance?.kind === 'internal_system' && ctx.inputProvenance?.sourceTool === 'notifications-event'));
  const eligible = (ctx: any) => privateReviewContext(ctx) && !!ctx.runId &&
    !/^agent:main:assistant-review-(?:preparation|profile|skills)-/.test(ctx.sessionKey || '') &&
    /^agent:main:assistant-review[-:]/.test(ctx.sessionKey || '');
  const quietInstruction = 'Keep background processing silent. Save review counts, recovery, skipped/deferred signals, backlog and completion notes only through finish_analysis for the dashboard. A saved suggestion is delivered by the independent service, not by this reply. When there is no separate genuinely useful alert requiring the owner, end with exactly NO_REPLY, even after saving a new suggestion or completing a review. Do not announce starting, resuming, working, finishing or no new suggestions. Genuine actionable alerts and authorized preparation results/reminders remain enabled.';
  const instruction = 'This turn reviews the personal-assistant signals inbox. Resume an unfinished review through assistant_signals begin_analysis with the same explicit accounts, then finish_analysis after a real conclusion. Do not switch to unrelated old main-chat tasks after a provider retry. Follow the assistant instructions below; they are the parts of tools/personal-assistant/AGENTS.md for reviews, so do not read that file again. Claim once with begin_analysis limit 120 and read every page with analysis_page; finish within about fifteen minutes. The service balances accounts, oldest backlog and newer signals. For body_clipped=true read the rest with events, event_ids and body_offset. Defer only what you expect to judge better later; pass the rest as finish_analysis reviewed_ids. Publish only genuinely useful distinct suggestions; no quota or duplicate direct Telegram send. Quiet hours limit delivery, not private review. Do not claim a complete review when only a preview was assessed. ' + quietInstruction;
  api.on('before_prompt_build', async (_event: any, ctx: any) => {
    if (preparationSession(ctx.sessionKey) && privateReviewContext(ctx)) {
      if (ctx.runId) sessionRuns.set(ctx.sessionKey,ctx.runId);
      const context = ((await ownerContext()) + (await preparationRules())).trim();
      return context ? {prependContext: context} : undefined;
    }
    if (profileSession(ctx.sessionKey) && privateReviewContext(ctx)) {
      const context = (await ownerContext()).trim();
      return context ? {prependContext: context} : undefined;
    }
    if (!background(ctx)) return;
    if (!runs.has(ctx.runId)) runs.set(ctx.runId, {session: ctx.sessionKey, started: Date.now(), reviewTouched: false});
    if (runs.size > 100) runs.delete(runs.keys().next().value!);
    sessionRuns.set(ctx.sessionKey, ctx.runId);
    if (sessionRuns.size > 100) sessionRuns.delete(sessionRuns.keys().next().value!);
    // Notification continuations are not a new review schedule: do not make
    // every phone event start a review or redirect unrelated background work.
    if (!eligible(ctx)) return {prependContext: quietInstruction};
    const state = await call('review_context', {owner_session: ctx.sessionKey, owner_run: ctx.runId});
    const hint = state.review ? ` Unfinished review ${state.review.id}; ${state.review.last_error || 'completion not committed'}. Resume it before claiming another batch.` : '';
    const context = reviewSession(ctx.sessionKey) ? (await ownerContext()) + (await assistantInstructions()) : '';
    return {prependContext: instruction + hint + context};
  }, {timeoutMs: 5000});

  // Gate review tools and note which run touched a review. Ownership itself is bound in the
  // tool's execute() from host-owned context; this hook only ever blocks, never rewrites.
  api.on('before_tool_call', async (event: any, ctx: any) => {
    // Code Mode's script runner is allowed: every tool the script calls passes this hook on its own.
    if ((reviewSession(ctx.sessionKey) || profileSession(ctx.sessionKey)) && !codeModeRunner(event, ctx) &&
        (!REVIEW_TOOLS.has(plainToolName(event.toolName)) || readsSecret(event))) {
      return {block: true, blockReason: 'Signal reviews and profile drafts only read: use assistant_signals, memory lookups or read-only file tools.'};
    }
    if (skillsSession(ctx.sessionKey) && !codeModeRunner(event, ctx) && (!SKILLS_TOOLS.has(plainToolName(event.toolName)) || readsSecret(event))) {
      return {block: true, blockReason: 'Find my skills reads the owner\'s accounts in the browser and reports with assistant_signals skills_found; nothing else.'};
    }
    const policy = preparationSession(ctx.sessionKey) ? preparationToolPolicy(event, ctx) : undefined;
    if (policy && 'block' in policy) return {block: true, blockReason: policy.block};
    if (preparationSession(ctx.sessionKey) && !codeModeRunner(event,ctx)) {
      const job_id=ctx.runId || event.runId || sessionRuns.get(ctx.sessionKey);
      if (job_id) {
        const admitted=await call('preparation_tool_intent',{job_id,call_id:ctx.toolCallId || event.toolCallId || `${event.toolName}:${JSON.stringify(event.params)}`,
          tool:plainToolName(event.toolName),tool_action:typeof event.params?.action==='string' ? event.params.action : null,
          params:journalValue(event.params),read_only:preparationReadOnly(event)});
        if (!admitted.active) return {block:true,blockReason:admitted.reason || 'This task is no longer running. End this turn.'};
      }
    }
    const owner = runs.get(ctx.runId || event.runId);
    if (owner && owner.session === ctx.sessionKey && plainToolName(event.toolName) === 'assistant_signals' &&
        ['begin_analysis', 'finish_analysis'].includes(event.params?.action)) owner.reviewTouched = true;
  });

  api.on('after_tool_call',async (event:any,ctx:any)=>{
    if (!preparationSession(ctx.sessionKey) || codeModeRunner(event,ctx)) return;
    const job_id=ctx.runId || event.runId || sessionRuns.get(ctx.sessionKey);
    if (job_id) await call('preparation_tool_result',{job_id,call_id:ctx.toolCallId || event.toolCallId || `${event.toolName}:${JSON.stringify(event.params)}`,
      result:journalValue(event.result),error:event.error?.slice(0,2000)});
  },{timeoutMs:5000});

  api.on('reply_payload_sending', async (event: any, ctx: any) => {
    const owner = runs.get(event.runId);
    if (!owner?.reviewTouched || owner.session !== event.sessionKey ||
        ctx.channelId !== 'telegram' || ctx.accountId !== String(assistantConfig().telegram_account || 'default') ||
        !sameChat(ctx.conversationId || '') ||
        event.kind !== 'final' || event.payload?.mediaUrl || event.payload?.mediaUrls?.length ||
        !processingOnlyReviewSummary(event.payload?.text)) return;
    // This is the maintained outbound-payload hook, not before_agent_reply
    // (which runs before model execution and cannot inspect the final text).
    return {cancel: true, reason: 'assistant_review_processing_only'};
  });

  // A host-classified notification continuation may resume an actual review.
  // Give that claim the same cleanup/finish protection, but do not make an
  // unrelated notification turn start a review or touch lifecycle state.
  const reviewRun = (ctx: any) => background(ctx) &&
    runs.get(ctx.runId)?.session === ctx.sessionKey &&
    (eligible(ctx) || runs.get(ctx.runId)?.reviewTouched);
  api.on('model_call_ended', async (event: any, ctx: any) => {
    if (!reviewRun(ctx) || event.outcome !== 'error') return;
    const reason = ({connection_reset:'ai_connection_reset',connection_closed:'ai_connection_closed',terminated:'ai_connection_closed',timeout:'ai_timeout'} as any)[event.failureKind] || 'ai_request_failed';
    await call('review_failed', {owner_session:ctx.sessionKey, owner_run:ctx.runId, reason});
  }, {timeoutMs: 5000});

  api.on('before_agent_finalize', async (_event: any, ctx: any) => {
    if (!reviewRun(ctx)) return;
    const state = await call('review_context', {owner_session:ctx.sessionKey, owner_run:ctx.runId});
    if (!state.review || state.review.owner_run !== ctx.runId) return;
    return {action:'revise', reason:'The signal review is still unfinished.', retry:{
      instruction:'Resume the claimed signal review with begin_analysis. Commit a real conclusion with finish_analysis before ending. If some signals cannot be assessed, pass only the genuinely reviewed IDs in reviewed_ids; leave the rest pending. Do not invent a review or switch tasks. ' + quietInstruction,
      idempotencyKey:'assistant-review-finish', maxAttempts:2}};
  }, {timeoutMs: 5000});

  api.on('agent_end', async (event: any, ctx: any) => {
    if (!reviewRun(ctx)) return;
    // Even a NO_REPLY final bypassing the host's finalization hook cannot leave
    // an uncommitted claim blocking the next tick for an hour.
    await call('review_failed', {owner_session:ctx.sessionKey, owner_run:ctx.runId,
      reason:event.success ? 'review_not_finished' : 'run_interrupted', terminal:true});
  }, {timeoutMs: 5000});
}
