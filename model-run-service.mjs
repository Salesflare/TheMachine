// One-shot model turns for answers someone waits on (search answers, Help), from one long-running process instead of
// a new `openclaw infer model run --gateway` per turn: that CLI loads OpenClaw on every turn, seconds before the turn
// starts. This process loads it once and makes the same Gateway call the CLI makes (`agent` with modelRun, no prompt
// of its own, its own one-off session), with the same client identity and scopes, so nothing about access changes.
//
// The service writes requests as JSON lines on stdin: {id, prompt, model?, thinking?, timeout_ms?}. Each answer is one
// JSON line on stdout: {id, ok: true, text} or {id, error: 'timeout' | 'unavailable'}. Several can run at once. It
// exits when stdin closes, or after IDLE_MS without a request (the service starts it again when needed).
import {randomUUID} from 'node:crypto';
import {createInterface} from 'node:readline';
import {gatewayRuntime} from './openclaw-root.mjs';

export const MAX_PROMPT = 200000;
export const MAX_TIMEOUT = 300000;
export const IDLE_MS = 10 * 60 * 1000;
const REF = /^([a-z0-9-]{1,40})\/([A-Za-z0-9._:/-]{1,120})$/;
const LEVEL = /^[a-z]{2,10}$/;

// The request, checked: a prompt, an optional provider/model and thinking level, a timeout in bounds. null otherwise.
export function request(input) {
  if (!input || typeof input !== 'object' || typeof input.id !== 'string' || !/^[A-Za-z0-9-]{1,64}$/.test(input.id)) return null;
  const prompt = typeof input.prompt === 'string' ? input.prompt : '';
  if (!prompt.trim() || prompt.length > MAX_PROMPT) return null;
  const ref = input.model == null || input.model === '' ? null : REF.exec(String(input.model));
  if (input.model && !ref) return null;
  if (input.thinking && !LEVEL.test(String(input.thinking))) return null;
  const timeout = Math.max(1000, Math.min(MAX_TIMEOUT, Number.parseInt(input.timeout_ms, 10) || 60000));
  return {id: input.id, prompt, provider: ref?.[1], model: ref?.[2], thinking: input.thinking || undefined, timeout};
}

// The Gateway call `openclaw infer model run --gateway` makes for this request: [params, client options]. A model
// override goes as the backend client with the admin scope, as the CLI sends it; otherwise as the CLI.
export function call(req) {
  const sessionId = `model-run-${randomUUID()}`;
  const params = {
    agentId: 'main', sessionId, sessionKey: `agent:main:explicit:${sessionId}`, message: req.prompt,
    provider: req.provider, model: req.model, ...(req.thinking ? {thinking: req.thinking} : {}),
    modelRun: true, promptMode: 'none', cleanupBundleMcpOnRunEnd: true, idempotencyKey: randomUUID(),
  };
  const override = Boolean(req.provider || req.model);
  const extra = {expectFinal: true, timeoutMs: req.timeout, progress: false,
                 ...(override ? {clientName: 'gateway-client', mode: 'backend', scopes: ['operator.admin']} : {})};
  return [params, extra];
}

// The reply's text, as the CLI's --json outputs join it; null when there is none.
export function text(response) {
  const texts = (response?.result?.payloads || []).map(p => p?.text).filter(t => typeof t === 'string');
  return texts.length ? texts.join('\n').trim() : null;
}

// Answer requests from `input` on `output` until input closes (exit) or nothing comes for IDLE_MS. runtime: OpenClaw's
// Gateway runtime (a stub in tests).
export async function serve({runtime = gatewayRuntime, input = process.stdin, output = process.stdout, exit = code => process.exit(code), idleMs = IDLE_MS} = {}) {
  const {callGatewayFromCli} = await runtime();
  const write = line => output.write(JSON.stringify(line) + '\n');
  let idle;
  const rest = () => { clearTimeout(idle); idle = setTimeout(() => exit(0), idleMs); };
  rest();
  write({ready: true});
  const lines = createInterface({input});
  lines.on('line', async line => {
    rest();
    let given;
    try { given = JSON.parse(line); } catch { return; }
    const req = request(given);
    if (!req) { if (typeof given?.id === 'string') write({id: given.id, error: 'unavailable'}); return; }
    const [params, extra] = call(req);
    try {
      const said = text(await callGatewayFromCli('agent', {json: true}, params, extra));
      write(said ? {id: req.id, ok: true, text: said} : {id: req.id, error: 'unavailable'});
    } catch (error) {
      write({id: req.id, error: /timeout|timed out/i.test(String(error?.message || '')) ? 'timeout' : 'unavailable'});
    }
  });
  lines.on('close', () => { clearTimeout(idle); exit(0); });
}

if (import.meta.url === `file://${process.argv[1]}`) await serve();
