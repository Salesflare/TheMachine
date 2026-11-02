// Run by the app's native side in the owner's Machine page after it loads, as `(<this file>)(payload)`. One copy for
// iOS and Android. It only uses what the dashboard already offers a signed-in owner:
//  - push: hands the phone's push token to the Machine (action app_push_register), which registers it with the
//    account's push relay. The Machine then asks the relay for content-free wakeups ("New to-do"); the text a
//    notification opens is fetched from the Machine, never carried by the push.
//    Once a week per token is enough (kept in this page's own storage on the Machine's address).
//  - share: what was shared to the app (text, links, files) opens the dashboard's New to-do, filled in, for the
//    owner to check and add (window.machineShare). A dashboard from before that only gets the text, as a new to-do.
//  - tag: a tapped notification's to-do opens (#chat=<id>); listen: the same for taps while this page is open (iOS).
// payload: {base, push?: {platform, token, sandbox, label}, share?: {text, files: [{name, type, data(base64)}]},
//           tag?, listen?}
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
        location.hash = typeof tag === 'string' && /^[A-Za-z0-9_-]{1,64}$/.test(tag) ? 'chat=' + tag : '';
      });
    }
  }

  if (typeof payload.tag === 'string' && /^[A-Za-z0-9_-]{1,64}$/.test(payload.tag)) location.hash = 'chat=' + payload.tag;

  const KEY = 'machine-app-push', WEEK = 7 * 24 * 3600 * 1000;
  let last = null;
  try { last = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { last = null; }
  const fresh = last && last.token === (payload.push && payload.push.token) && Date.now() - last.at < WEEK;
  if (payload.push && payload.push.token && !fresh) {
    try {
      await action('app_push_register', {platform: payload.push.platform, token: payload.push.token,
        sandbox: !!payload.push.sandbox, label: String(payload.push.label || '').slice(0, 60)});
      out.push = 'registered';
      try { localStorage.setItem(KEY, JSON.stringify({token: payload.push.token, at: Date.now()})); } catch (e) { /* next time */ }
    } catch (e) { out.push = 'failed'; }
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
