// Talk live (talk_live.py): the Gateway side of a live voice conversation in a to-do's chat. The Gateway holds the
// OpenAI credentials (an API key, or a ChatGPT sign-in) and makes a short-lived, single-use session; this helper hands
// the browser's WebRTC offer on to it and the answer back. The secret stays here and in the service: never the browser.
//
// Only operator.read and operator.talk are asked for, never operator.write: if the Gateway's own agent were ever asked
// from this session, it could only read (OpenClaw's "safe-read-only" policy). The dashboard sets its own tools anyway.
//
// Two ways to run:
// - one request in, one answer out: status (talk.catalog), or an offer on its own.
// - `--hold`: one conversation. JSON lines in, one line out for each: start (talk.client.create), offer (the SDP),
//   end (talk.client.close). The Gateway ties a session to the connection that made it and drops it when that
//   connection closes (OpenClaw 2026.11), so this process keeps its one connection open from start to end. The
//   conversation ends when the service says end or closes stdin, or when the Gateway closes the connection.
import {gatewayRuntime} from './openclaw-root.mjs';
import {readFileSync} from 'node:fs';
import {homedir} from 'node:os';
import {createInterface} from 'node:readline';

console.log = console.info = console.warn = console.error;   // OpenClaw's own notes go to stderr: stdout is the answers
const SESSION = /^agent:main:assistant-talk-(?:[a-f0-9]{16}|main)$/;   // a to-do's conversation, or the main one
const SCOPES = ['operator.read', 'operator.talk'];
const SCOPE = {scopes: SCOPES};
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
const openclawConfig = () => parsed((() => { try { return readFileSync(process.env.OPENCLAW_CONFIG_PATH || `${homedir()}/.openclaw/openclaw.json`, 'utf8'); } catch { return ''; } })()) || {};
function gatewayPort(config = openclawConfig()) {
  return Number(process.env.OPENCLAW_GATEWAY_PORT || config.gateway?.port || 18789);
}

async function call(method, params) {
  const {callGatewayFromCli} = await gatewayRuntime();
  return await callGatewayFromCli(method, {timeout: '20000'}, params, SCOPE);
}

// One Gateway connection kept open for a whole conversation: the same local Gateway, credentials and operator device
// the CLI uses (as callGatewayFromCli), with the same two scopes. `lost` runs once if the Gateway closes it.
async function connect(lost) {
  const {GatewayClient} = await gatewayRuntime();
  const config = openclawConfig(), auth = config.gateway?.auth || {};
  const secret = key => typeof auth[key] === 'string' && auth[key] ? auth[key] : undefined;
  let ready = false, connected, failed;
  const hello = new Promise((ok, fail) => { connected = ok; failed = fail; });
  const client = new GatewayClient({
    url: `ws://127.0.0.1:${gatewayPort(config)}`,
    token: process.env.OPENCLAW_GATEWAY_TOKEN || secret('token'), password: process.env.OPENCLAW_GATEWAY_PASSWORD || secret('password'),
    clientName: 'cli', mode: 'cli', role: 'operator', scopes: SCOPES,
    onHelloOk: () => { ready = true; connected(); },
    onConnectError: error => failed(error),
    onClose: () => { if (ready) lost(); else failed(new Error('gateway closed')); },
  });
  const timer = setTimeout(() => failed(new Error('connect timeout')), 20000);
  client.start();
  try {
    await hello;
  } catch (error) {
    client.stop();
    throw error;
  } finally {
    clearTimeout(timer);
  }
  return {request: (method, params) => client.request(method, params, {timeoutMs: 20000}), stop: () => client.stop()};
}

// The OpenAI provider, when the Gateway can open a browser session with it; how it pays shows in Settings
async function status() {
  const catalog = await call('talk.catalog', {});
  const openai = (catalog?.realtime?.providers || []).find(p => p?.id === 'openai');
  return {ready: !!(openai?.configured && openai?.supportsBrowserSession), model: openai?.defaultModel || ''};
}

async function start(gateway, request) {
  const made = await gateway.request('talk.client.create', {sessionKey: request.session_key, mode: 'realtime', transport: 'webrtc',
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
  if (!response.ok || !answer.startsWith('v=0') || answer.length > MAX_SDP) return refused(request.offer_url === GATEWAY_CALLS, response.status, answer);
  return {sdp: answer};
}

// Why an offer didn't get an answer, in fixed words and numbers only (the service logs them, so support can tell why):
// OpenAI's own status, and whether it turned the sign-in down (auth). With a ChatGPT sign-in the Gateway's broker hands
// the offer on and answers 502 with OpenAI's status in its text ("OpenAI Realtime call creation failed (403)"): only that
// number is kept. The broker's own 401 is its one-use session gone (expired or unknown), not OpenAI saying no.
const UPSTREAM = /call creation failed \((\d{3})\)/;
function refused(viaGateway, status, text) {
  const openai = viaGateway ? Number(UPSTREAM.exec(String(text || '').slice(0, 2000))?.[1] || 0) : status;
  const reason = openai === 401 || openai === 403 ? 'auth' : viaGateway && status === 401 ? 'session' : 'other';
  return {error: 'unavailable', reason, status, openai};
}

async function end(gateway, request) {
  if (request.voice_session_id) await gateway.request('talk.client.close', {sessionKey: request.session_key, voiceSessionId: request.voice_session_id});
  return {ok: true};
}

// Never pass on raw Gateway or provider errors (they can name paths, settings or the secret): a fixed word only
function failure(error) {
  const m = String(error?.message || '');
  return {error: 'unavailable', reason: /timeout|abort/i.test(m) ? 'timeout' : /auth|key|sign|credential|platform/i.test(m) ? 'auth' : /ECONNREFUSED|closed|socket/i.test(m) ? 'offline' : 'other'};
}
const say = value => new Promise(done => process.stdout.write(JSON.stringify(value) + '\n', done));
const quit = () => process.stdout.write('', () => process.exit(0));

// --hold: one conversation on one connection. The first line must be its start; every line names the same session.
async function hold() {
  let gateway, session, stopping = false;
  const finish = async (answer = false) => {
    if (stopping) return;
    stopping = true;
    let ended = {ok: true};
    try {
      if (gateway && session?.voice_session_id) await end(gateway, session);
    } catch (error) {
      ended = failure(error);
    }
    if (answer) await say(ended);
    gateway?.stop();
    quit();
  };
  for await (const line of createInterface({input: process.stdin, crlfDelay: Infinity})) {
    const request = parsed(line) || {};
    const known = ['start', 'offer', 'end'].includes(request.method) && SESSION.test(request.session_key || '') &&
      (request.method === 'start' ? !gateway : gateway && request.session_key === session.session_key);
    if (!known) {
      await say({error: 'invalid_request'});
      continue;
    }
    if (request.method === 'end') return await finish(true);
    try {
      if (request.method === 'start') {
        session = {session_key: request.session_key};
        gateway = await connect(() => { if (!stopping) { stopping = true; gateway.stop(); quit(); } });
        const made = await start(gateway, request);
        session.voice_session_id = made.voice_session_id;
        await say(made);
        if (made.error) return await finish();
      } else {
        await say(await offer(request));
      }
    } catch (error) {
      await say(failure(error));
      if (request.method === 'start') return await finish();
    }
  }
  await finish();   // the service closed stdin: the conversation is over
}

async function once() {
  let input = '';
  for await (const chunk of process.stdin) input += chunk;
  const request = parsed(input) || {};
  const methods = {status, offer};
  if (!methods[request.method] || (request.method !== 'status' && !SESSION.test(request.session_key || ''))) {
    process.stdout.write(JSON.stringify({error: 'invalid_request'}));
    process.exit(1);
  }
  let result;
  try {
    result = await methods[request.method](request);
  } catch (error) {
    result = failure(error);
  }
  process.stdout.write(JSON.stringify(result), () => process.exit(0));
}

await (process.argv.includes('--hold') ? hold() : once());
