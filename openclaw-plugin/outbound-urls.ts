// Web addresses a run nobody is watching may open (SECURITY.md, "Pages a run opens by itself").
//
// A to-do prepared ahead and a routine read messages and pages, and any of those can carry instructions meant for the
// model. Opening a page sends its address to whoever runs that site, so an address the model put together could carry
// what it read (https://site.example/?d=<a private line>) without a send or an approval. These runs open an address
// when it can't carry anything the model added:
// - it was written, as is, in what the run read: a message, a search result, a page, the owner's words (seen);
// - or it is a plain page address: no query, no user name, short ordinary words in the host and path (plain);
// - or it goes to a well-known service where nobody else reads what is asked: a search, map, encyclopedia, weather or
//   profile lookup, or the owner's own account in a big web app (Google, Microsoft, Stripe, Zapier, Slack, GitHub ...),
//   or to the owner's own company's sites (the domains of the addresses they connected).
// Anything else is refused with a hint to search for it instead. A Do it run, the owner's to-do chat and their own
// chats are not checked here: the owner asked for that work.

const KEEP_URLS = 4000;  // addresses remembered per run's session, newest kept
const KEEP_SESSIONS = 100;
const seenBySession = new Map<string, Set<string>>();

// Tools whose results are what the run read: messages, search results, pages, memory, files, and what a command printed
// (mail read with gog, gh). Never a Code Mode script's own output (it prints whatever the script put together; the
// tools it calls are read one by one), and never an address the call was given itself (ownUrls).
const READ_TOOLS = new Set(['web_search', 'web_fetch', 'browser', 'assistant_signals', 'memory_search', 'memory_get', 'read',
  'file_fetch', 'dir_fetch', 'process']);
const SHELL_TOOLS = new Set(['exec', 'bash', 'shell', 'shell_command', 'exec_command', 'local_shell']);
const args = (params: any) => { if (typeof params !== 'string') return params; try { return JSON.parse(params); } catch { return {}; } };
export const readTool = (name: string, params?: any) => READ_TOOLS.has(name) || name.startsWith('gbrain__') ||
  (SHELL_TOOLS.has(name) && (typeof args(params)?.command === 'string' || Array.isArray(args(params)?.command) || typeof args(params)?.cmd === 'string'));

const URL_IN_TEXT = /https?:\/\/[^\s"'<>`\\|{}\[\]]+/gi;
const LINK_IN_TEXT = /(?:\]\(|href\s*=\s*["']?)([^\s"'<>)]+)/gi;  // a Markdown link's target or an href, maybe relative
const TRAILING = /[.,;:!?'")\]}>*_]+$/;

function texts(value: any, out: string[] = [], depth = 0): string[] {
  if (depth > 12 || out.length > 5000) return out;
  if (typeof value === 'string') out.push(value);
  else if (Array.isArray(value)) for (const item of value) texts(item, out, depth + 1);
  else if (value && typeof value === 'object') for (const item of Object.values(value)) texts(item, out, depth + 1);
  return out;
}

const decode = (text: string) => text.replace(/&amp;/gi, '&').replace(/\\u0026/gi, '&').replace(/\\\//g, '/');

function parsed(raw: string, base?: string): URL | undefined {
  try {
    const url = base ? new URL(raw, base) : new URL(raw);
    return /^https?:$/.test(url.protocol) ? url : undefined;
  } catch { return undefined; }
}
const withoutFragment = (url: URL) => { const copy = new URL(url.href); copy.hash = ''; return copy.href; };

// Every web address written in these values, as it was written (a trailing period or bracket left off) and without
// its #fragment. Links relative to `base` (a fetched page's own address) are read too.
export function urlsIn(value: any, base?: string): Set<string> {
  const found = new Set<string>();
  const add = (raw: string, from?: string) => {
    for (const candidate of [raw, raw.replace(TRAILING, '')]) {
      const url = parsed(candidate, from);
      if (url) { found.add(url.href); found.add(withoutFragment(url)); }
    }
  };
  for (const text of texts(value).map(decode)) {
    for (const match of text.matchAll(URL_IN_TEXT)) add(match[0]);
    if (base) for (const match of text.matchAll(LINK_IN_TEXT)) add(match[1], base);
  }
  return found;
}

function remember(session: string, urls: Iterable<string>) {
  let seen = seenBySession.get(session);
  if (!seen) {
    seen = new Set();
    seenBySession.set(session, seen);
    if (seenBySession.size > KEEP_SESSIONS) seenBySession.delete(seenBySession.keys().next().value!);
  }
  for (const url of urls) { seen.delete(url); seen.add(url); }
  while (seen.size > KEEP_URLS) seen.delete(seen.values().next().value!);
}

// What a tool returned, less any address the call itself was given (a search result that repeats its query, a page
// that repeats its own address): those are the model's words coming back, not something it read.
export function noteToolResult(session: string, toolName: string, params: any, result: any) {
  remember(session, resultUrls(toolName, params, result));
}
function resultUrls(toolName: string, params: any, result: any): string[] {
  toolName = String(toolName || '').replace(/^openclaw_*/, '');
  params = args(params);
  if (!readTool(toolName, params) || result == null) return [];
  const own = ownUrls(params);
  const asked = [params?.url, params?.targetUrl].find(value => typeof value === 'string');
  const page = typeof result === 'object' ? (result.finalUrl || result.details?.finalUrl || result.url) : undefined;
  const base = toolName === 'web_fetch' || toolName === 'browser' ? String(page || asked || '') || undefined : undefined;
  return [...urlsIn(result, base)].filter(url => !own(url));
}

const undo = (text: string) => { try { return decodeURIComponent(text.replace(/\+/g, ' ')); } catch { return text; } };
// Whether an address is in a call's own arguments, also inside another address's query (?q=https%3A%2F%2F...): a page
// that shows it back (a search for it) is the model's words, not something it read.
function ownUrls(params: any) {
  const said: string[] = [];
  for (const text of texts(params)) {
    let decoded = decode(text);
    said.push(decoded);
    for (let i = 0; i < 3; i++) { const next = undo(decoded); if (next === decoded) break; said.push(decoded = next); }
  }
  const all = said.join('\n');
  return (url: string) => [url, undo(url)].flatMap(v => [v, v.replace(/\/$/, '')]).some(v => v.length > 10 && all.includes(v));
}

// The run's prompt (the job, its evidence, the owner's words) and its session so far: what people and tools wrote,
// never the model's own messages or tool calls.
export function notePrompt(session: string, event: any) {
  const urls: string[] = [...urlsIn([event?.prompt, event?.currentUserMessage])];
  const calls = new Map<string, {name: string; args: any}>();
  const messages = Array.isArray(event?.messages) ? event.messages : [];
  for (const message of messages) {
    if (message?.role !== 'assistant' || !Array.isArray(message.content)) continue;
    for (const part of message.content)
      if (part?.type === 'toolCall' && part.id) calls.set(String(part.id), {name: String(part.name || ''), args: part.arguments});
  }
  for (const message of messages) {
    if (message?.role === 'user') urls.push(...urlsIn(message.content));
    if (message?.role === 'toolResult' && !message.isError) {
      const call = calls.get(String(message.toolCallId || ''));
      urls.push(...resultUrls(message.toolName || call?.name, call?.args, {content: message.content, details: message.details}));
    }
    // A tool a Code Mode script called: its name, what it was given and what it returned, kept beside the script's call.
    const nested = message?.role === 'custom' && message.customType === 'openclaw.nested-tool.v1' ? message.details : undefined;
    if (nested && !nested.isError) urls.push(...resultUrls(nested.toolName, nested.input, nested.result));
  }
  remember(session, urls);
}

export const forgetSession = (session: string) => seenBySession.delete(session);

// --- an address that can't carry anything ------------------------------------------------------------------------

// One host label, path segment or fragment: short ordinary words (an article's slug, a @handle), no address, no long
// code or number that could spell out something read.
function plainPart(part: string) {
  let text = part;
  try { text = decodeURIComponent(part); } catch { return false; }
  if (text.length > 100 || /[=&?\s/\\]/.test(text) || /.@/.test(text)) return false;
  return text.replace(/^@/, '').split(/[-_.~+,:;!()'*$]+/).every(word => word.length <= 30 &&
    !(word.length >= 12 && /\d/.test(word) && /[A-Za-z]/.test(word)) &&
    !(word.length >= 16 && /[a-z]/.test(word) && /[A-Z]/.test(word) && !/^(?:[A-Z]?[a-z]{2,})+$/.test(word)) &&  // CamelCase words, not noise
    !(/^[0-9a-f]{16,}$/i.test(word) && !/^\d{1,20}$/.test(word)) && !/^\d{21,}$/.test(word));
}

export function plainAddress(url: URL, fragmentSent: boolean) {
  if (url.username || url.password || url.search.length > 1) return false;
  if (fragmentSent && url.hash.length > 1 && !plainPart(url.hash.slice(1))) return false;
  const segments = url.pathname.split('/').filter(Boolean);
  // The site's own name is fixed; only labels in front of it (sub.site.example) could be made up per request.
  const labels = url.hostname.split('.');
  const site = /^(?:co|com|org|net|gov|ac|edu)$/.test(labels.at(-2) || '') && labels.length > 2 ? 3 : 2;
  return segments.length <= 8 && segments.every(plainPart) && labels.slice(0, -site).every(plainPart);
}

// --- lookups and signed-in apps on well-known services -------------------------------------------------------------

// Hosts where only the service itself sees what is asked (a search, a map, an article, a forecast, a profile, the
// owner's own account in a big web app), with the paths a query or an id may go to. Never a host anyone can publish on
// or collect with (sites.google.com, script.google.com, storage buckets, hooks.zapier.com, hooks.slack.com, a form's
// formResponse), and never a path that sends the browser on to another site (google.com/url, linkedin.com/redir).
const ANY = /^\//;
const SERVICES: [RegExp, RegExp, RegExp?][] = [
  [/^(?:www\.)?google\.[a-z.]{2,6}$/, /^\/(?:search|maps(?:\/.*)?)$/],
  [/^(?:maps|mail|calendar|drive|meet|contacts|photos|keep|chat|console\.cloud|admin|myaccount|analytics|ads|search|play|support|business|merchants|tagmanager|lookerstudio|translate|news|scholar|books|trends)\.google\.com$/, ANY],
  [/^docs\.google\.com$/, ANY, /^\/forms\/.*\/formResponse\b/],
  [/^(?:www\.)?bing\.com$/, /^\/(?:search|maps)$/],
  [/^(?:html\.|lite\.)?duckduckgo\.com$/, /^\/(?:html\/?)?$/],
  [/^search\.brave\.com$/, /^\/search$/],
  [/^[a-z-]{2,12}\.(?:m\.)?wikipedia\.org$/, /^\/(?:wiki\/[^/]+|w\/index\.php)$/],
  [/^(?:www\.)?wikidata\.org$/, /^\/(?:wiki\/[^/]+|w\/index\.php|w\/api\.php)$/],
  [/^(?:www\.)?openstreetmap\.org$/, /^\/(?:search)?$/],
  [/^nominatim\.openstreetmap\.org$/, /^\/(?:search|reverse|lookup)(?:\.php)?$/],
  [/^(?:api|geocoding-api|air-quality-api|marine-api)\.open-meteo\.com$/, /^\/v1\/[a-z-]+$/],
  [/^wttr\.in$/, /^\/[^/]*$/],
  [/^(?:www\.)?linkedin\.com$/, ANY, /^\/(?:redir|slink)\b/],
  [/^(?:www\.|m\.)?youtube\.com$/, ANY, /^\/(?:redirect|attribution_link)\b/],
  [/^api\.github\.com$/, ANY],
  [/^(?:outlook\.office|outlook\.office365|outlook\.live|teams\.microsoft|admin\.microsoft|portal\.azure)\.com$/, ANY],
  [/^dashboard\.stripe\.com$/, ANY],
  [/^(?:www\.)?zapier\.com$/, ANY],
  [/^app\.slack\.com$/, ANY],
  [/^business\.facebook\.com$/, ANY],
  [/^apps\.apple\.com$/, ANY],
  [/^(?:www\.)?amazon\.(?:com|[a-z]{2}|co\.[a-z]{2}|com\.[a-z]{2})$/, ANY, /^\/gp\/redirect\b/],
  [/^(?:www\.)?(?:x|twitter)\.com$/, ANY],
  [/^wise\.com$/, ANY],
  [/^app\.aikido\.dev$/, ANY],
  [/^[a-z0-9]+\.documents\.adobe\.com$/, ANY],
];
// github.com: a search, or a repository's pages with a commit id in them; GitHub shows a repository's owner its most
// visited paths, so the rest of a path stays plain words.
const githubPage = (url: URL) => /^(?:www\.)?github\.com$/.test(url.hostname) &&
  url.pathname.split('/').filter(Boolean).every(part => /^[0-9a-f]{7,40}$/.test(part) || /^[0-9a-f]{7,40}\.\.\.?[0-9a-f]{7,40}$/.test(part) || plainPart(part));
// Mail providers: an owner address there doesn't make the provider's other hosts the owner's.
const MAIL_PROVIDERS = /^(?:g(?:oogle)?mail\.com|outlook\.[a-z.]+|hotmail\.[a-z.]+|live\.[a-z.]+|msn\.com|yahoo\.[a-z.]+|icloud\.com|me\.com|mac\.com|aol\.com|proton(?:mail)?\.[a-z.]+|pm\.me|gmx\.[a-z.]+|web\.de|zoho\.com|yandex\.[a-z.]+|mail\.[a-z.]+|fastmail\.[a-z.]+|hey\.com|skynet\.be|telenet\.be)$/;
export function serviceAddress(url: URL, ownerDomains: string[] = []) {
  if (url.username || url.password || url.protocol !== 'https:') return false;
  const host = url.hostname.toLowerCase();
  // The owner's own company's sites (the domain of an address they connected): what they ask there stays theirs.
  if (ownerDomains.some(domain => domain && !MAIL_PROVIDERS.test(domain) && (host === domain || host.endsWith('.' + domain)))) return true;
  return githubPage(url) || SERVICES.some(([hosts, paths, never]) => hosts.test(host) && paths.test(url.pathname) && !never?.test(url.pathname));
}

// --- the check -------------------------------------------------------------------------------------------------------

// --- shell commands that reach the network ----------------------------------------------------------------------------

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

// The Machine's own service and anything else on this computer: nothing leaves it.
const LOCAL_HOST = /^(?:localhost|.*\.localhost|127(?:\.\d{1,3}){3}|\[?::1\]?|0\.0\.0\.0)$/i;
const localUrl = (url: URL) => LOCAL_HOST.test(url.hostname);
const base = (token: string) => token.replace(/^.*\//, '');
// Programs that send a request to an address on their command line: curl, wget, HTTPie and its kin, raw sockets.
const HTTP_CLIENTS = /^(?:curl|wget2?|https?|xh|xhs|curlie)$/;
const SOCKET_CLIENTS = /^(?:nc|ncat|netcat|socat|telnet)$/;
const INTERPRETERS = /^(?:python[\d.]*|node|nodejs|deno|bun|ruby|perl|php)$/;
// Options that send something besides the address (a body, a header, a cookie, a user name, another method, an upload,
// a config or proxy that changes where it goes), as one letter (curl -d, wget -U) or long (--data, --post-data).
const SENDS_SHORT = /^-[a-zA-Z]*[dFTHAebuKxXU]/;
const SENDS_LONG = /^--(?:data|form|upload|header|user-agent|referer|cookie|load-cookies|user|password|json|request|method|post|body|config|proxy|socks|preproxy|resolve|connect-to|url-query|variable|input-file|execute|raw|multipart|auth)/;
// In inline code: a scheme with no address after it (the code puts the address together), and text joined or formatted
// onto a written address, or a named argument (a body, params, headers) handed over next to it.
const BUILT_ADDRESS = /[a-z][a-z0-9+.-]*:\/\/(?=["'`{\s$]|$)/i;
const AFTER_ADDRESS = /^(?:[{$%]|["'`]\s*(?:[+%.]|,\s*\w+\s*=(?!=)))/;

// What a shell command reaches: the addresses it names (urls), those it sends more to than the address (sends: a
// body, headers, a cookie, or text the code adds), and refuse when it names one that can't be read from the command
// (a $variable, an address the code builds, a raw connection off this computer).
export function shellReach(params: any): {urls: string[]; sends: string[]; refuse: boolean} {
  const text = commandText(args(params));
  const urls: string[] = [], sends: string[] = [];
  let refuse = false;
  const target = (token: string) => {
    if (/[$`]/.test(token)) { refuse = true; return; }  // made while it runs: can't be checked
    const raw = /^[a-z][a-z0-9+.-]*:\/\//i.test(token) ? token : `https://${token}`;
    const url = parsed(raw);
    if (!url) { refuse = true; return; }
    urls.push(url.href);
  };
  for (const stage of commandStages(text)) {
    stage.forEach((token, at) => {
      const program = base(token), rest = stage.slice(at + 1);
      if (HTTP_CLIENTS.test(program)) {
        const named = rest.filter(arg => !arg.startsWith('-') && (/^[a-z][a-z0-9+.-]*:\/\//i.test(arg) || /^[\w.-]+\.[a-z]{2,}(?::\d+)?(?:[/?#]|$)/i.test(arg) || /^localhost\b/.test(arg) || /^[$`]/.test(arg)));
        named.forEach(target);
        const more = rest.some(arg => SENDS_SHORT.test(arg) || SENDS_LONG.test(arg)) ||
          (/^(?:https?|xhs?)$/.test(program) && rest.some(arg => !arg.startsWith('-') && !named.includes(arg) && /[=:@]/.test(arg)));
        if (more) sends.push(...urls.slice(urls.length - named.length));
      } else if (SOCKET_CLIENTS.test(program)) {
        // A raw connection sends whatever it is given: only to this computer.
        for (const arg of rest.filter(arg => !arg.startsWith('-'))) {
          const host = arg.replace(/^(?:tcp|udp|ssl|openssl|tcp4|tcp6)[^:]*:/i, '').replace(/:\d+$/, '');
          if (/[$`]/.test(host) || (/[a-z]/i.test(host) && /\./.test(host) && !LOCAL_HOST.test(host)) || (/^\d{1,3}(?:\.\d{1,3}){3}$/.test(host) && !LOCAL_HOST.test(host))) refuse = true;
        }
      } else if (INTERPRETERS.test(program) && at === stage.findIndex(t => INTERPRETERS.test(base(t)))) {
        // Inline code (-c, -e, a heredoc): every address written in it gets the same check. An address the code puts
        // together, or hands over with more next to it, can't be checked unless it stays on this computer.
        const inline = rest.some(arg => /^-[a-zA-Z]*[ceEr]$/.test(arg) || arg === '-') || text.includes('<<');
        if (!inline) return;
        const code = decode(text);
        if (BUILT_ADDRESS.test(code)) refuse = true;
        for (const match of code.matchAll(URL_IN_TEXT)) {
          const written = match[0].replace(TRAILING, ''), url = parsed(written);
          if (!url) continue;
          if (AFTER_ADDRESS.test(code.slice(match.index! + match[0].length))) sends.push(url.href);
          urls.push(url.href);
        }
      }
    });
  }
  return {urls, sends, refuse};
}

// The addresses a call opens: web_fetch's url, the browser's (or computer's) open or navigate address.
export function addressesOf(toolName: string, params: any): string[] {
  params = args(params) || {};
  if (toolName === 'web_fetch') return [params.url].filter(value => typeof value === 'string');
  if (SHELL_TOOLS.has(toolName)) return shellReach(params).urls;
  if (toolName !== 'browser' && toolName !== 'computer') return [];
  const request = params.request && typeof params.request === 'object' ? params.request : {};
  return [params.url, params.targetUrl, request.url, request.targetUrl].filter(value => typeof value === 'string' && value.trim());
}

// The way on is one this Machine has: web_search where a search provider is set up, else a search page in the browser
// (its result links count as read). The same two in preparation_state.py (unread_address).
export const blockedAddress = (webSearch: boolean) => 'This run only opens an address it read (in a message, a search result or a page) or a plain page ' +
  `address without a query. Search for it ${webSearch ? 'with web_search' : 'on a search page in the browser'} and open a result, or open the address exactly as it was written.`;
export const BLOCKED_ADDRESS = blockedAddress(false);

// Whether OpenClaw has a search provider set up, so a run has web_search (it leaves the tool out otherwise): one chosen,
// or a provider with its key in the config or the environment. Asked only when an address is refused. Not sure: false,
// since the search page works on every Machine.
export async function webSearchSetUp(api: any): Promise<boolean> {
  try {
    const config = api.runtime?.config?.current?.() ?? api.config ?? {};
    const search = config.tools?.web?.search ?? {};
    if (search.enabled === false) return false;
    if (String(search.provider || '').trim()) return true;
    const providers = await api.runtime?.webSearch?.listProvidersAsync?.({config}) ?? [];
    return providers.some((p: any) => p.requiresCredential !== false &&
      (p.getConfiguredCredentialValue?.(config) || p.envVars?.some((name: string) => process.env[name])));
  } catch { return false; }
}

// undefined: the call may open its addresses; else why not (for the agent).
export function outboundCheck(session: string, toolName: string, params: any, ownerDomains: string[] = []): undefined | string {
  const seen = seenBySession.get(session) || new Set<string>();
  if (SHELL_TOOLS.has(toolName)) {
    // Shell: an address it makes while it runs can't be checked; what it sends besides the address goes only to this
    // computer, the owner's own domains or a known service.
    const reach = shellReach(params);
    if (reach.refuse) return BLOCKED_ADDRESS;
    for (const raw of reach.sends) {
      const url = parsed(raw);
      if (url && !localUrl(url) && !serviceAddress(url, ownerDomains)) return BLOCKED_ADDRESS;
    }
  }
  for (const raw of addressesOf(toolName, params)) {
    const url = parsed(raw.trim());
    if (!url || localUrl(url)) continue;  // about:blank, a file, this computer: nothing leaves it
    const fragmentSent = toolName === 'browser' || toolName === 'computer';  // only a page's script reads #fragment
    if (seen.has(fragmentSent ? url.href : withoutFragment(url))) continue;
    if (plainAddress(url, fragmentSent) || serviceAddress(url, ownerDomains)) continue;
    return BLOCKED_ADDRESS;
  }
  return undefined;
}
