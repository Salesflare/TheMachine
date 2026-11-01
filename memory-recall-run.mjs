// Recall (knowledge.recall): OpenClaw's memory search, for what the owner said in earlier conversations. It searches
// what OpenClaw indexed for its main agent: the memory files and, where the owner turned it on, past conversation
// transcripts (memory.search sources memory and sessions). By meaning where the Machine has embeddings, by keywords on
// small hosted Machines.
//
// One tool: memory_search through the Gateway's tools.invoke, in Talk's main session, with a short timeout so a voice
// never waits long. Two calls at once, one per corpus (past conversations, the notes): in one mixed search a large
// notes folder crowds the conversations out. Where transcripts aren't indexed that call fails and the notes stay.
// Nothing else can be invoked from here: the tool name and the arguments are fixed, the query is plain text.
// tools.invoke needs operator.write; memory_search itself only reads. The Gateway's own memory.search (operator.read)
// doesn't reach transcripts, which need a session to check visibility against.
//
// Prints {results: [{source, text, at, origin}]}, or {error} when memory search is off, unavailable or slow: the service
// then answers nothing, quietly. Never the path of a file or transcript.
import {gatewayRuntime} from './openclaw-root.mjs';

export const SESSION = 'agent:main:assistant-talk-main';
export const MAX_QUERY = 300;
export const MAX_RESULTS = 8;
export const MAX_TEXT = 1200;
const MAX_TIMEOUT = 8000;

// The request from the service, checked: a query of plain text, how many, and how long to wait
export function request(input) {
  const query = typeof input?.query === 'string' ? input.query.replace(/\s+/g, ' ').trim().slice(0, MAX_QUERY) : '';
  const limit = Math.max(1, Math.min(MAX_RESULTS, Number.parseInt(input?.max_results, 10) || 5));
  const timeout = Math.max(1000, Math.min(MAX_TIMEOUT, Number.parseInt(input?.timeout_ms, 10) || 5000));
  return query ? {query, limit, timeout} : null;
}

// memory_search's answer, as the service takes it: the excerpt, where it came from (an earlier conversation or the
// notes), when, and who wrote it as OpenClaw knows it (owner, agent, untrusted)
export function shape(result) {
  if (!result?.ok || result.output?.isError) return {error: 'unavailable'};
  const text = (result.output?.content || []).find(c => c?.type === 'text')?.text;
  let found;
  try { found = JSON.parse(text || 'null'); } catch { return {error: 'unavailable'}; }
  if (!Array.isArray(found?.results)) return {error: found?.disabled ? 'off' : 'unavailable'};
  return {results: found.results.filter(r => typeof r?.snippet === 'string' && r.snippet.trim()).slice(0, MAX_RESULTS).map(r => ({
    source: r.source === 'sessions' || r.corpus === 'sessions' ? 'sessions' : 'memory',
    text: r.snippet.replace(/\n*Source: [^\n]*\s*$/, '').trim().slice(0, MAX_TEXT),
    at: Number.isFinite(r.provenance?.observedAt) ? r.provenance.observedAt : null,
    origin: ['owner', 'agent', 'untrusted'].includes(r.provenance?.originClass) ? r.provenance.originClass : 'unknown',
    score: Number.isFinite(r.score) ? r.score : 0,
  }))};
}

// Both corpora's answers as one list: up to half from past conversations (they are what recall is for), the rest from
// the notes, best first. An error only when neither answered.
export function merge(conversations, notes, limit) {
  const said = conversations.results || [], kept = notes.results || [];
  if (!conversations.results && !notes.results) return notes.error === 'off' || conversations.error === 'off' ? {error: 'off'} : {error: 'unavailable'};
  const first = said.slice(0, Math.max(Math.ceil(limit / 2), limit - kept.length));
  const rest = kept.slice(0, limit - first.length);
  return {results: [...first, ...rest].sort((a, b) => b.score - a.score).map(({score, ...r}) => r)};
}

export async function recall(input, runtime = gatewayRuntime) {
  const asked = request(input);
  if (!asked) return {error: 'invalid_request'};
  let callGatewayFromCli;
  try {
    ({callGatewayFromCli} = await runtime());
  } catch {
    return {error: 'unavailable'};
  }
  const search = corpus => callGatewayFromCli('tools.invoke', {timeout: String(asked.timeout)}, {
    name: 'memory_search', args: {query: asked.query, maxResults: asked.limit, corpus}, sessionKey: SESSION,
  }, {scopes: ['operator.write']}).then(shape, () => ({error: 'unavailable'}));  // away or slow: no protocol text
  const [conversations, notes] = await Promise.all([search('sessions'), search('memory')]);
  return merge(conversations, notes, asked.limit);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  let input = '';
  for await (const chunk of process.stdin) input += chunk;
  let parsed = null;
  try { parsed = JSON.parse(input); } catch {}
  process.stdout.write(JSON.stringify(await recall(parsed)));
  process.exit(0);  // the Gateway client may keep a socket open
}
