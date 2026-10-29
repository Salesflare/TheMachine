// Talk live (talk_live.py): the Gateway side of a live voice conversation in a to-do's chat. The Gateway holds the
// OpenAI credentials (an API key, or a ChatGPT sign-in) and makes a short-lived, single-use session; this helper hands
// the browser's WebRTC offer on to it and the answer back. The secret stays here and in the service: never the browser.
//
// Only operator.read and operator.talk are asked for, never operator.write: if the Gateway's own agent were ever asked
// from this session, it could only read (OpenClaw's "safe-read-only" policy). The dashboard sets its own tools anyway.
// Methods: status (talk.catalog), start (talk.client.create), offer (the SDP), end (talk.client.close). Nothing else.
import {gatewayRuntime} from './openclaw-root.mjs';
import {readFileSync} from 'node:fs';
import {homedir} from 'node:os';

const SESSION = /^agent:main:assistant-talk-[a-f0-9]{16}$/;
const SCOPE = {scopes: ['operator.read', 'operator.talk']};
// Where an offer may go: OpenAI's own Realtime endpoint (with an API key) or the Gateway's (with a ChatGPT sign-in)
const OPENAI_CALLS = 'https://api.openai.com/v1/realtime/calls';
const GATEWAY_CALLS = '/plugins/openai/realtime/calls';
const MAX_SDP = 262144;
const VOICE = /^[a-z]{2,12}$/;   // the owner's pick in Settings (voice_input.TALK_VOICES)
// OpenAI's GA Realtime model, not GPT-Live: with GPT-Live the Gateway owns the conversation's tools, and the
// dashboard's own read-only tools and on-screen proposals (talk_live.py) wouldn't apply. GA works with an API key and,
// where the account has access, with a ChatGPT sign-in (through the Gateway's offer broker).
const REALTIME_MODEL = 'gpt-realtime-2.1';

const parsed = text => { try { return JSON.parse(text); } catch { return null; } };
function gatewayPort() {
  const config = parsed((() => { try { return readFileSync(process.env.OPENCLAW_CONFIG_PATH || `${homedir()}/.openclaw/openclaw.json`, 'utf8'); } catch { return ''; } })()) || {};
  return Number(process.env.OPENCLAW_GATEWAY_PORT || config.gateway?.port || 18789);
}

async function call(method, params) {
  const {callGatewayFromCli} = await gatewayRuntime();
  return await callGatewayFromCli(method, {timeout: '20000'}, params, SCOPE);
}

// The OpenAI provider, when the Gateway can open a browser session with it; how it pays shows in Settings
async function status() {
  const catalog = await call('talk.catalog', {});
  const openai = (catalog?.realtime?.providers || []).find(p => p?.id === 'openai');
  return {ready: !!(openai?.configured && openai?.supportsBrowserSession), model: openai?.defaultModel || ''};
}

async function start(request) {
  const made = await call('talk.client.create', {sessionKey: request.session_key, mode: 'realtime', transport: 'webrtc',
    brain: 'agent-consult', provider: 'openai', model: REALTIME_MODEL, ...(VOICE.test(request.voice || '') ? {voice: request.voice} : {})});
  if (made?.transport !== 'webrtc' || typeof made.clientSecret !== 'string') return {error: 'unavailable', reason: 'other'};
  const url = made.offerUrl || OPENAI_CALLS;
  if (url !== OPENAI_CALLS && url !== GATEWAY_CALLS) return {error: 'unavailable', reason: 'other'};
  const headers = Object.fromEntries(Object.entries(made.offerHeaders || {}).filter(([k, v]) => /^[a-z0-9-]{1,64}$/i.test(k) && typeof v === 'string'));
  return {secret: made.clientSecret, offer_url: url, offer_headers: headers, voice_session_id: made.voiceSessionId,
          model: made.model || '', expires_at: made.expiresAt || 0, via: url === GATEWAY_CALLS ? 'signin' : 'key'};
}

async function offer(request) {
  if (typeof request.sdp !== 'string' || !request.sdp.startsWith('v=0') || request.sdp.length > MAX_SDP) return {error: 'invalid_request'};
  if (request.offer_url !== OPENAI_CALLS && request.offer_url !== GATEWAY_CALLS) return {error: 'invalid_request'};
  const url = request.offer_url === GATEWAY_CALLS ? `http://127.0.0.1:${gatewayPort()}${GATEWAY_CALLS}` : OPENAI_CALLS;
  const response = await fetch(url, {method: 'POST', body: request.sdp, signal: AbortSignal.timeout(30000),
    headers: {...(request.offer_headers || {}), 'Content-Type': 'application/sdp', Authorization: `Bearer ${request.secret}`}});
  const answer = await response.text();
  if (!response.ok || !answer.startsWith('v=0') || answer.length > MAX_SDP) return {error: 'unavailable', reason: response.status === 401 || response.status === 403 ? 'auth' : 'other'};
  return {sdp: answer};
}

async function end(request) {
  if (request.voice_session_id) await call('talk.client.close', {sessionKey: request.session_key, voiceSessionId: request.voice_session_id});
  return {ok: true};
}

let input = '';
for await (const chunk of process.stdin) input += chunk;
const request = parsed(input) || {};
const methods = {status, start, offer, end};
if (!methods[request.method] || (request.method !== 'status' && !SESSION.test(request.session_key || ''))) {
  process.stdout.write(JSON.stringify({error: 'invalid_request'}));
  process.exit(1);
}
let result;
try {
  result = await methods[request.method](request);
} catch (error) {
  // Never pass on raw Gateway or provider errors (they can name paths, settings or the secret): a fixed word only
  const m = String(error?.message || '');
  result = {error: 'unavailable', reason: /timeout|abort/i.test(m) ? 'timeout' : /auth|key|sign|credential|platform/i.test(m) ? 'auth' : /ECONNREFUSED|closed|socket/i.test(m) ? 'offline' : 'other'};
}
process.stdout.write(JSON.stringify(result), () => process.exit(0));
