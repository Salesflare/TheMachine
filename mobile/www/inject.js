// Run by the app's native side in the owner's Machine page after it loads, as `(<this file>)(payload)`. One copy for
// iOS and Android. It only uses what the dashboard already offers a signed-in owner:
//  - push: hands the phone's push token to the Machine (action app_push_register), which registers it with the
//    account's push relay. The Machine then asks the relay for content-free wakeups ("New to-do"); the text a
//    notification opens is fetched from the Machine, never carried by the push. With device.fetch (Android) the app
//    shows the notification itself, with the to-do's line it asks the Machine for (MachinePushService).
//    Once a week per token is enough (kept in this page's own storage on the Machine's address).
//  - share: what was shared to the app (text, links, files) opens the dashboard's New to-do, filled in, for the
//    owner to check and add (window.machineShare). A dashboard from before that only gets the text, as a new to-do.
//  - tag: a tapped notification's to-do opens (#chat=<id>), or with card (Open draft) its place in the list, where
//    the draft shows in full (#card=<id>); listen: the same for taps while this page is open (iOS).
//  - files: a download (a link with `download`, an export) goes to the app (MachineFiles on Android, machineFiles on
//    iOS, both only there on the Machine's own address), which saves it on the phone. A WebView has no downloads.
//    A file linked in a new tab (a to-do's files) goes the same way, for the phone to open in an app. A file the page
//    made goes to the phone's share sheet (window.__machineShareFile; a WebView has no Web Share).
//  The phone's id from app_push_register is kept with the token, so Settings can tell this phone's notifications.
//  - phone: window.machinePhone, the phone's own questions (the microphone, notifications) and its settings page.
// payload: {base, device: {platform, sandbox, label, fetch?}, push?: {platform, token, sandbox, label, fetch?},
//           share?: {text, files: [{name, type, data(base64)}]}, tag?, card?, listen?}
// Returns a promise of {push: 'registered'|'failed'|undefined, share: 'opened'|'added'|'failed'|undefined}.
(async function machineInject(payload) {
  'use strict';
  const out = {};
  const base = String(payload && payload.base || '');
  if (!base || !location.href.startsWith(base)) return out;  // only the Machine the app was set up with
  const api = path => new URL(path, base).href;
  let csrf = null;
  const session = async () => {
    if (csrf) return csrf;
    const r = await fetch(api('api/session'), {credentials: 'same-origin', cache: 'no-store'});
    if (!r.ok) throw new Error('session ' + r.status);
    csrf = (await r.json()).csrf;
    return csrf;
  };
  const action = async (name, args) => {
    const r = await fetch(api('api/action'), {method: 'POST', credentials: 'same-origin',
      headers: {'Content-Type': 'application/json', 'X-CSRF-Token': await session()},
      body: JSON.stringify({action: name, args})});
    if (!r.ok) throw new Error(name + ' ' + r.status);
    return r.json();
  };

  if (payload.listen && !window.__machineListen) {
    window.__machineListen = true;
    const push = window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.PushNotifications;
    if (push && push.addListener) {
      push.addListener('pushNotificationActionPerformed', event => {
        const tag = event && event.notification && event.notification.data && event.notification.data.tag;
        location.hash = typeof tag === 'string' && /^[A-Za-z0-9_-]{1,64}$/.test(tag) ? (event.actionId === 'draft' ? 'card=' : 'chat=') + tag : '';
      });
    }
  }

  // close: the Machine's browser opened on its own (a dashboard from before its in-app Browser pane, a link straight
  // to it) fills the whole app with the stream. A floating X over it, top right, goes back to the dashboard.
  const here = new URL(location.href).pathname.slice(new URL(base).pathname.length - 1);
  if (/^\/browser(?:\/|$)/.test(here) && typeof document !== 'undefined' && !document.getElementById('machine-close')) {
    const x = document.createElement('button');
    x.id = 'machine-close';
    x.type = 'button';
    x.setAttribute('aria-label', 'Close the browser');
    x.textContent = '×';
    x.style.cssText = 'position:fixed;z-index:2147483647;top:calc(env(safe-area-inset-top) + 8px);right:calc(env(safe-area-inset-right) + 8px);' +
      'width:44px;height:44px;margin:0;padding:0;border:0;border-radius:50%;background:rgba(20,20,20,.72);color:#fff;' +
      'font:300 30px/44px system-ui,sans-serif;text-align:center;cursor:pointer;box-shadow:0 1px 6px rgba(0,0,0,.35);-webkit-tap-highlight-color:transparent';
    x.addEventListener('click', () => {
      if (history.length > 1 && document.referrer.startsWith(base)) history.back();
      else location.replace(base);
    });
    (document.body || document.documentElement).appendChild(x);
  }

  if (typeof payload.tag === 'string' && /^[A-Za-z0-9_-]{1,64}$/.test(payload.tag)) location.hash = (payload.card === true ? 'card=' : 'chat=') + payload.tag;

  const KEY = 'machine-app-push', WEEK = 7 * 24 * 3600 * 1000;
  let last = null;
  try { last = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { last = null; }
  // An app that now shows the notification itself (fetch) registers again at once, for the push to leave it to the app
  const fresh = last && last.token === (payload.push && payload.push.token) && Date.now() - last.at < WEEK && 'id' in last &&
    !!last.fetch === !!(payload.push && payload.push.fetch);
  const register = async (device, token) => {
    const fetch = !!device.fetch;
    const done = await action('app_push_register', {platform: device.platform, token,
      sandbox: !!device.sandbox, label: String(device.label || '').slice(0, 60), fetch});
    const id = done && done.registered && typeof done.id === 'string' ? done.id : null;
    try { localStorage.setItem(KEY, JSON.stringify({token, at: Date.now(), id, fetch})); } catch (e) { /* next time */ }
  };
  if (payload.push && payload.push.token && !fresh) {
    try { await register(payload.push, payload.push.token); out.push = 'registered'; } catch (e) { out.push = 'failed'; }
  }

  // phone: the phone's own questions (the microphone, notifications). The phone asks them itself; once it won't ask
  // again, the dashboard shows Open settings, the app's own page in the phone's settings (window.machinePhone). The
  // app's MachinePhone (Android) or machinePhone (iOS) is only there on the Machine's own address.
  const android = window.MachinePhone, ios = window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.machinePhone;
  if ((android || ios) && !window.machinePhone) {
    const waiting = new Map();
    let next = 0;
    if (android) android.onmessage = e => {
      let r = null;
      try { r = JSON.parse(e.data); } catch (err) { return; }
      const done = r && waiting.get(r.id);
      if (done) { waiting.delete(r.id); done(r); }
    };
    // {state: 'granted'|'prompt'|'blocked'|'on'|'off'|'ok', token?}
    const ask = what => ios ? ios.postMessage({ask: what}) : new Promise(resolve => {
      const id = String(++next);
      waiting.set(id, resolve);
      android.postMessage(JSON.stringify({id, ask: what}));
    });
    window.machinePhone = {
      state: async kind => (await ask(kind === 'mic' ? 'mic' : 'push')).state,  // 'granted', 'prompt' or 'blocked'
      settings: () => ask('settings'),
      // Notifications on for this phone: the phone's question, then its token to the Machine. 'on', 'blocked' or 'off'
      pushOn: async () => {
        const r = await ask('pushOn');
        if (r.state !== 'on' || !r.token || !payload.device) return r.state === 'blocked' ? 'blocked' : 'off';
        await register(payload.device, r.token);
        return 'on';
      },
    };
    try { window.dispatchEvent(new Event('machinephone')); } catch (e) { /* a page that doesn't listen */ }  // Settings shows it
  }

  const native = window.MachineFiles || (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.machineFiles);
  if (native && !window.__machineFiles) {
    const origin = new URL(base).origin, LIMIT = 25 * 1024 * 1024;
    const ours = href => { try { const u = new URL(href, location.href); return u.origin === origin && /^(?:https|blob):$/.test(u.protocol); } catch (e) { return false; } };
    const said = () => { try { if (typeof window.toast === 'function') window.toast(typeof window.t === 'function' ? window.t('That file couldn’t be read.') : 'That file couldn’t be read.', true); } catch (e) { /* no toast */ } };
    // A file to the app. open: the phone shows it in an app; share: the phone's share sheet; else saved on the phone
    const post = async (blob, name, how) => {
      if (blob.size > LIMIT) return false;
      const data = await new Promise((resolve, reject) => {
        const f = new FileReader();
        f.onload = () => resolve(String(f.result).replace(/^data:[^,]*,/, ''));
        f.onerror = reject;
        f.readAsDataURL(blob);
      });
      native.postMessage(JSON.stringify({name: String(name || 'file').slice(0, 200), type: blob.type || '', data, open: how === 'open', share: how === 'share'}));
      return true;
    };
    const give = async (href, name, open) => {
      try {
        const r = await fetch(href, {credentials: 'same-origin'});
        if (!r.ok) { said(); return; }
        const sent = /filename\*?=(?:UTF-8'')?"?([^";]+)"?/i.exec(r.headers.get('Content-Disposition') || '');
        if (sent && (open || !name)) { try { name = decodeURIComponent(sent[1]); } catch (e) { name = sent[1]; } }
        if (!await post(await r.blob(), name, open ? 'open' : 'save')) said();
      } catch (e) { said(); }
    };
    window.__machineFiles = (href, name) => { if (ours(href)) give(href, name); };
    // A file the page made (a milestone's image) to the phone's share sheet, where a WebView has no Web Share.
    // Resolves true once the app has it; the page says so itself when it doesn't.
    window.__machineShareFile = async (blob, name) => { try { return await post(blob, name, 'share'); } catch (e) { return false; } };
    const take = a => {
      if (!a || !a.hasAttribute('download') || !ours(a.href)) return false;
      give(a.href, a.getAttribute('download') || decodeURIComponent(new URL(a.href).pathname.split('/').pop() || '') || 'file');
      return true;
    };
    // A file the dashboard links to in a new tab (a to-do's files, a chat's pictures): a WebView has no tabs, and
    // in place it would leave the dashboard; the phone opens it in an app instead
    const fileLink = a => { try { const u = new URL(a.href); return a.target === '_blank' && u.origin === origin && u.pathname.indexOf('/api/') >= 0; } catch (e) { return false; } };
    const linkName = a => { try { const u = new URL(a.href); return u.searchParams.get('name') || (u.searchParams.get('path') || '').split('/').pop() || (a.title || a.textContent || '').trim(); } catch (e) { return ''; } };
    document.addEventListener('click', e => {
      const a = e.target && e.target.closest && e.target.closest('a[href]');
      if (!a || e.defaultPrevented) return;
      if (take(a)) e.preventDefault();
      else if (fileLink(a)) { e.preventDefault(); give(a.href, linkName(a), true); }
    }, true);
    const click = HTMLAnchorElement.prototype.click;  // an export clicks a link that isn't on the page
    HTMLAnchorElement.prototype.click = function () { if (!this.isConnected && take(this)) return; return click.call(this); };
  }

  if (payload.share) {
    const share = payload.share;
    const files = (share.files || []).map(f => {
      const bytes = Uint8Array.from(atob(f.data), c => c.charCodeAt(0));
      return new File([bytes], f.name || 'file', {type: f.type || 'application/octet-stream'});
    });
    const text = String(share.text || '').trim();
    try {
      // The dashboard may still be starting: give it a moment to define machineShare
      for (let i = 0; i < 40 && typeof window.machineShare !== 'function'; i++) await new Promise(r => setTimeout(r, 100));
      if (typeof window.machineShare === 'function' && window.machineShare({text, files}) !== false) out.share = 'opened';
      else if (text) { await action('card_new', {text, scope: null, due: null, due_at: null, about: [], attach: []}); out.share = 'added'; }
      else out.share = 'failed';
    } catch (e) { out.share = 'failed'; }
  }
  return out;
})
