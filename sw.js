// The installed dashboard app: push notifications, and a copy of the page itself (the app shell) so the app opens at
// once. The shell holds no data and never its CSRF token; the last cards, chats and Graph lists are kept by the page,
// encrypted (docs/architecture.md, "On the device"). Brand images and fonts are kept too, all of them up front. Nothing else is cached.
// A new ASSETS name drops the kept brand files once (2: the moods became stickers, not the app icon).
const SHELL = 'tm-shell-2', ASSETS = 'tm-assets-2', SHARE = 'tm-share', SHELL_AGE = 7 * 864e5;
// The server no longer puts the token in the page (api/session has it); an older page still may, and it is taken out.
const CSRF = /(\bconst csrf=')(?:[0-9a-f]{64})?(')/;
const scopeUrl = () => new URL(self.registration.scope);

// Every brand image and font the page can show (assistant.py BRAND_ASSETS), kept up front, so the app offline looks the
// same as online: the robot, its moods and the typefaces, also ones this device hasn't shown yet.
const BRAND = ['avatar.png', 'avatar-blink.png', 'favicon-32.png', 'favicon-512.png', 'sleepy.webp', 'sad.webp', 'thinking.webp', 'wave.webp',
  'wave-blink.webp', 'wave-look.webp', 'wave-hand.webp', 'laugh.webp', 'party.webp', 'app-icon-192.png', 'app-icon-maskable-192.png', 'app-icon-maskable-512.png', 'app-icon-badge-96.png', 'serif.woff2', 'sans.woff2'];
const brandOk = r => r.status === 200 && r.type === 'basic' && /^(image|font)\//.test(r.headers.get('Content-Type') || '');
async function warm() {
  const cache = await caches.open(ASSETS);
  await Promise.all(BRAND.map(async name => {
    const href = new URL('brand/' + name, scopeUrl()).href;
    if (await cache.match(href)) return;
    try { const r = await fetch(href, {credentials: 'same-origin', signal: AbortSignal.timeout(15e3)}); if (brandOk(r)) await cache.put(href, r); } catch {}
  }));
}

// Error reports (error_feed.py): this worker's own errors and a failed shell update go to an open dashboard page, which
// sends them on with its own (source "sw"): the type, the message (normalized again by the service) and the place, never
// a page's address or what it holds. At most 10 wait for a page; with none open they wait in memory and are lost when the
// worker stops. Not a failed update: no answer at all (offline) or a sign-in, which is the session, not a bug.
const swErrors = [];
function swPlace(stack) {
  for (const l of String(stack || '').split('\n')) {
    const m = l.match(/^\s*(?:at\s+(?:(.*?)\s+\()?|(.*?)@)(\S+?):(\d+):\d+\)?\s*$/);
    if (m && /\/sw\.js(?:[?#]|$)/.test(m[3]) && m[3].startsWith(self.location.origin)) return {function: String(m[1] || m[2] || '<anonymous>').split(/[\s.]/).pop().slice(0, 60) || '<anonymous>', line: +m[4]};
  }
  return null;
}
async function swFlush() {
  if (!swErrors.length) return;
  const pages = await self.clients.matchAll({type: 'window'});
  if (pages.length) for (const item of swErrors.splice(0)) pages[0].postMessage({swError: item});
}
function swError(kind, message, place) {
  if (!place || swErrors.length >= 10) return;
  swErrors.push({kind: String(kind || 'Error').slice(0, 60), message: String(message || '').slice(0, 500), ...place});
  swFlush().catch(() => {});
}
function swReport(e, where) {
  try { if (e instanceof Error && e.name !== 'AbortError') swError(e.name, e.message, swPlace(e.stack) || (where ? {function: where, line: 0} : null)); } catch {}
}
self.addEventListener('error', e => swReport(e.error));
self.addEventListener('unhandledrejection', e => swReport(e.reason));

// The page asks for warm() once this worker is ready: a slow brand file never holds up the install.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => event.waitUntil((async () => {
  for (const name of await caches.keys()) if (name.startsWith('tm-') && ![SHELL, ASSETS, SHARE].includes(name)) await caches.delete(name);
  await self.clients.claim();
})()));

// Keep a page answer as the shell: only a whole, current dashboard page whose CSRF token can be taken out.
async function keepShell(response) {
  if (response.status !== 200 || response.type !== 'basic' || !/text\/html/i.test(response.headers.get('Content-Type') || '')) return;
  const text = await response.text();
  if (!CSRF.test(text)) return;
  const headers = {'Content-Type': 'text/html; charset=utf-8', 'X-Shell-At': String(Date.now())};
  if (response.headers.get('ETag')) headers.ETag = response.headers.get('ETag');
  await (await caches.open(SHELL)).put(scopeUrl().href, new Response(text.replace(CSRF, '$1$2'), {headers}));
}

// The session is gone (the sign-in page, or refused): drop the shell and tell the open pages to drop their data.
async function signedOut() {
  await caches.delete(SHELL);
  await caches.delete(ASSETS);
  await caches.delete(SHARE);
  for (const c of await self.clients.matchAll({type: 'window', includeUncontrolled: true})) c.postMessage({cache: 'signed-out'});
}

// Open the app: ask the Machine for the page first, with the kept copy's ETag, and wait a moment for its answer. Not
// changed (304): the kept copy. A new page (a release): that page, kept for next time, so the first start after an
// update is already the new version, never the old one again. No answer in time (offline, a slow link): the kept copy
// at once, and the answer, when it comes, replaces it (the page then sees the new release and loads it).
const SHELL_WAIT = 1500;
async function shell(event) {
  const cached = await (await caches.open(SHELL)).match(scopeUrl().href);
  const fresh = cached && Date.now() - +cached.headers.get('X-Shell-At') < SHELL_AGE ? cached : null;
  const etag = fresh?.headers.get('ETag');
  // Always the page itself on this origin (the scope), never another address.
  const asked = fetch(scopeUrl().href, {headers: etag ? {'If-None-Match': etag} : {}, redirect: 'manual', cache: 'no-store', credentials: 'same-origin'});
  event.waitUntil(asked.then(r => {
    if (r.type === 'opaqueredirect' || r.status === 401 || r.status === 403) return signedOut();
    if (r.status >= 500) return swError('ShellUpdateFailed', 'HTTP ' + r.status, {function: 'shell', line: 0});
    if (r.status === 200) return keepShell(r.clone()).catch(e => swReport(e, 'keepShell'));
  }).catch(() => {}));
  if (!fresh) return asked;
  if (self.navigator.onLine === false) return fresh;
  const r = await Promise.race([asked.catch(() => null), new Promise(ok => setTimeout(ok, SHELL_WAIT, null))]);
  return r && r.status !== 304 && r.status < 500 ? r : fresh;
}

async function asset(event, name) {
  // Only a brand file of this app, by its plain name: the address is built here, not taken from the request.
  const href = new URL('brand/' + name, scopeUrl()).href;
  const cache = await caches.open(ASSETS), cached = await cache.match(href);
  const fresh = fetch(href, {credentials: 'same-origin'}).then(r => {
    if (brandOk(r)) return cache.put(href, r.clone()).then(() => r);
    return r;
  });
  if (cached) { event.waitUntil(fresh.catch(() => {})); return cached; }
  return fresh;
}

// Share to The Machine (manifest.webmanifest share_target): what another app shared, kept on this device until the
// dashboard asks for it (#share=<id>, new-todo.js), then gone; at most SHARE_AGE, and gone on sign-out. New to-do shows
// it for the owner to check: nothing reaches the Machine until they add files there. Up to 5 files of 10 MB each, the
// Machine checks their kinds and sizes again as for any upload.
const SHARE_AGE = 10 * 6e4, SHARE_FILES = 5, SHARE_BYTES = 10 * 1048576, SHARE_ID = /^s_[a-f0-9]{16}$/;
async function shareIn(event) {
  const form = await event.request.formData(), scope = scopeUrl();
  const parts = ['title', 'text', 'url'].map(k => form.get(k)).map(v => typeof v === 'string' ? v.trim() : '').filter(Boolean);
  const text = parts.filter((v, i) => parts.indexOf(v) === i && !parts.some(w => w !== v && w.includes(v))).join('\n').slice(0, 2000);
  const files = form.getAll('files').filter(f => f instanceof File && f.size > 0 && f.size <= SHARE_BYTES).slice(0, SHARE_FILES);
  const id = 's_' + [...crypto.getRandomValues(new Uint8Array(8))].map(b => b.toString(16).padStart(2, '0')).join('');
  const cache = await caches.open(SHARE), at = String(Date.now());
  for (const key of await cache.keys()) if (Date.now() - +((await cache.match(key))?.headers.get('X-At') || 0) > SHARE_AGE) await cache.delete(key);
  const base = new URL('share/' + id + '/', scope).href;
  for (const [i, f] of files.entries()) await cache.put(base + i, new Response(f, {headers: {'Content-Type': f.type || 'application/octet-stream', 'X-At': at}}));
  await cache.put(base + 'meta', new Response(JSON.stringify({text, files: files.map(f => ({name: f.name, type: f.type}))}), {headers: {'Content-Type': 'application/json', 'X-At': at}}));
  return Response.redirect(scope.href + '#share=' + id, 303);
}
async function shareOut(id) {
  const cache = await caches.open(SHARE), base = new URL('share/' + id + '/', scopeUrl()).href;
  const meta = await cache.match(base + 'meta');
  if (!meta || Date.now() - +meta.headers.get('X-At') > SHARE_AGE) return null;
  const kept = await meta.json(), files = [];
  for (const [i, f] of (kept.files || []).entries()) {
    const r = await cache.match(base + i);
    if (r) files.push(new File([await r.blob()], String(f.name || 'file'), {type: String(f.type || '')}));
  }
  for (const key of await cache.keys()) if (key.url.startsWith(base)) await cache.delete(key);
  return {text: String(kept.text || ''), files};
}

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method === 'POST') {
    const url = new URL(req.url), scope = scopeUrl();
    if (url.origin === scope.origin && url.pathname === scope.pathname + 'share-target' && !url.search)
      event.respondWith(shareIn(event).catch(e => { swReport(e, 'shareIn'); return Response.redirect(scope.href, 303); }));
    return;
  }
  if (req.method !== 'GET') return;
  const url = new URL(req.url), scope = scopeUrl();
  if (url.origin !== scope.origin) return;
  if (req.mode === 'navigate' && url.pathname === scope.pathname && !url.search) return event.respondWith(shell(event));
  const name = url.pathname.startsWith(scope.pathname + 'brand/') && !url.search && url.pathname.slice(scope.pathname.length + 6);
  if (name && /^(fonts\/)?[\w.-]+\.(png|svg|webp|jpg|woff2?)$/.test(name)) return event.respondWith(asset(event, name));
});

// The page asks: drop the shell (a new release, or signing out), or keep the brand files (each start, after a sign-out dropped them).
self.addEventListener('message', event => {
  if (event.data?.cache === 'drop') event.waitUntil(Promise.all([caches.delete(SHELL), caches.delete(ASSETS)]));
  if (event.data?.cache === 'warm') event.waitUntil(warm().catch(() => {}));
  if (event.data?.errors === 'flush') event.waitUntil(swFlush().catch(() => {}));
  // A page of this dashboard asks for what was shared to it (shareIn): handed over once, to that page only
  const port = event.ports?.[0], id = event.data?.share;
  if (port && typeof id === 'string' && SHARE_ID.test(id) && event.source?.url?.startsWith(scopeUrl().href))
    event.waitUntil(shareOut(id).then(d => port.postMessage(d), e => { swReport(e, 'shareOut'); port.postMessage(null); }));
  // A notification's quick button (quickKeep): handed over once, to a page of this dashboard only
  const quick = event.data?.quick;
  if (port && typeof quick === 'string' && QUICK_ID.test(quick) && event.source?.url?.startsWith(scopeUrl().href))
    event.waitUntil(quickTake(quick).then(d => port.postMessage(d), e => { swReport(e, 'quickTake'); port.postMessage(null); }));
});

self.addEventListener('push', event => {
  let data = {};
  try { data = event.data ? event.data.json() : {}; } catch { data = {title: event.data?.text() || ''}; }
  // The app icon's badge: how many to-dos need the owner, as the Machine counted when it sent this.
  if (Number.isInteger(data.badge) && self.navigator.setAppBadge) (data.badge ? self.navigator.setAppBadge(data.badge) : self.navigator.clearAppBadge()).catch(() => {});
  event.waitUntil(self.registration.showNotification(data.title || 'The Machine', {
    body: data.body || '', tag: data.tag || undefined, renotify: !!data.tag && !data.silent, silent: !!data.silent,
    icon: 'brand/app-icon-192.png', badge: 'brand/app-icon-badge-96.png',
    data: {url: new URL(data.url || '.', self.registration.scope).href},
    // Quick buttons (machine/delivery/push.py QUICK), at most two. Fleet questions: Answer once and Decline open the
    // dashboard at the question, which asks to confirm.
    actions: Array.isArray(data.actions) ? data.actions.slice(0, 2) : [],
  }).catch(e => swReport(e, 'push')));
});

// A to-do's Snooze (2 hours, or tomorrow on a reminder) or Mark done: a browser can't ask for an unlock first, so it never runs from here. The
// dashboard opens and does it, with Undo (openQuickLink in todos-list.js). It takes the button from this worker only,
// once and within QUICK_AGE, by a random id (#quick=): a link from anywhere else can't make it do anything.
const QUICK = ['snooze2h', 'snooze', 'done'], QUICK_ID = /^k_[a-f0-9]{16}$/, QUICK_AGE = 5 * 6e4;
async function quickKeep(tag, action) {
  const id = 'k_' + [...crypto.getRandomValues(new Uint8Array(8))].map(b => b.toString(16).padStart(2, '0')).join('');
  await (await caches.open(SHARE)).put(new URL('quick/' + id, scopeUrl()).href,
    new Response(JSON.stringify({tag, action}), {headers: {'Content-Type': 'application/json', 'X-At': String(Date.now())}}));
  return id;
}
async function quickTake(id) {
  const cache = await caches.open(SHARE), href = new URL('quick/' + id, scopeUrl()).href, kept = await cache.match(href);
  if (!kept) return null;
  await cache.delete(href);
  return Date.now() - +kept.headers.get('X-At') > QUICK_AGE ? null : kept.json();
}

self.addEventListener('notificationclick', event => {
  event.notification.close();
  let url = event.notification.data?.url || self.registration.scope;
  if (['once', 'decline'].includes(event.action) && /#fleet=q_[a-f0-9]{16}$/.test(url)) url += '&choice=' + event.action;
  // Open draft: the to-do in the list, where its draft shows in full (its chat keeps it behind Review)
  if (event.action === 'draft') url = url.replace(/#chat=([a-f0-9]{16})$/, '#card=$1');
  const tag = event.notification.tag, quick = QUICK.includes(event.action) && /^[a-f0-9]{16}$/.test(tag || '');
  event.waitUntil((async () => {
    if (quick) url = new URL('#quick=' + await quickKeep(tag, event.action), scopeUrl()).href;
    const open = await self.clients.matchAll({type: 'window', includeUncontrolled: true});
    const client = open.find(c => c.url.startsWith(self.registration.scope));
    // An open dashboard shows the link itself (only its # part changes): never navigate it, which reloads the page.
    if (client) { client.postMessage({open: url}); return client.focus().catch(() => {}); }
    return self.clients.openWindow(url);
  })());
});
