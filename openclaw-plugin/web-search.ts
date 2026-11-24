// One web search on the owner's ChatGPT sign-in, for the briefing before a first meeting. Set aside: nothing calls it, since
// a result's address can't be told to come from the search. A single request of its own: OpenAI's hosted search as the only
// tool, no session, no other tool, nothing of the owner's in it. OpenClaw makes the request and holds the sign-in.
// OpenClaw's own setting for hosted search (tools.web.search.openaiCodex.enabled) is never used: it adds the search to
// every turn on the model. Here the tool is put into this one request's body, so no chat, review or Do it carries it.
// OpenClaw's completion keeps the reply's text only: not the search's sources, not its citations.
import {readFileSync} from 'node:fs';
import {homedir} from 'node:os';

const CONFIG_PATH = process.env.ASSISTANT_CONFIG || `${homedir()}/.local/share/personal-assistant/config.json`;
export const METHOD = 'assistant.web_search';
const PROMPT_CHARS = 2000;
const SECONDS = 75;
const CHATGPT = 'openai-chatgpt-responses';

function on(): boolean {
  try { return JSON.parse(readFileSync(CONFIG_PATH, 'utf8')).meeting_prep_signin_search === true; } catch { return false; }
}

// The request's body with that one tool and nothing else callable. From OpenAI's index, no page is opened live
// (external_web_access). Required: an answer from memory has no source.
export function searchBody(body: any): any {
  return {...body, tools: [{type: 'web_search', external_web_access: false, search_context_size: 'low'}], tool_choice: 'required',
    parallel_tool_calls: false};
}

async function runtime(): Promise<any> { return await import('openclaw/plugin-sdk/simple-completion-runtime'); }

export async function webSearch(api: any, params: any, sdk: () => Promise<any> = runtime): Promise<{ok: boolean; text?: string; reason?: string}> {
  const prompt = typeof params?.prompt === 'string' ? params.prompt.trim() : '';
  const modelRef = typeof params?.model === 'string' && /^openai\/[A-Za-z0-9._:-]{1,120}$/.test(params.model) ? params.model : undefined;
  if (!prompt || prompt.length > PROMPT_CHARS) return {ok: false, reason: 'invalid'};
  if (!on()) return {ok: false, reason: 'off'};
  try {
    const {prepareSimpleCompletionModelForAgent, completeWithPreparedSimpleCompletionModel} = await sdk();
    const cfg = api.runtime.config.current(), signal = AbortSignal.timeout(SECONDS * 1000);
    const prepared = await prepareSimpleCompletionModelForAgent({cfg, agentId: 'main', ...(modelRef ? {modelRef} : {}), signal});
    if (prepared?.error) return {ok: false, reason: 'model'};
    // Only a ChatGPT sign-in: an API key or another provider has its own search to set up
    if (prepared.model?.api !== CHATGPT) return {ok: false, reason: 'sign-in'};
    const reply = await completeWithPreparedSimpleCompletionModel({model: prepared.model, auth: prepared.auth, cfg,
      context: {messages: [{role: 'user', content: prompt, timestamp: Date.now()}]},
      options: {signal, reasoning: 'low', onPayload: searchBody}});
    if (reply?.stopReason !== 'stop') return {ok: false, reason: 'failed'};
    const text = (Array.isArray(reply.content) ? reply.content : []).filter((part: any) => part?.type === 'text').map((part: any) => String(part.text || '')).join('');
    return text.trim() ? {ok: true, text: text.slice(0, 8000)} : {ok: false, reason: 'empty'};
  } catch { return {ok: false, reason: 'failed'}; }  // also an OpenClaw without these helpers: no search, no error text
}

export function registerWebSearch(api: any) {
  if (typeof api.registerGatewayMethod !== 'function') return;
  api.registerGatewayMethod(METHOD, async ({params, respond}: any) => { respond(true, await webSearch(api, params), undefined); }, {scope: 'operator.write'});
}
