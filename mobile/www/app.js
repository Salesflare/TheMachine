// The app's start: open the owner's Machine, or set one up once (Sign in for a hosted Machine, its Tailscale address
// for one of their own). The Machine's dashboard is always loaded from the Machine itself, so a new web release reaches
// the app at once; this page only exists to get there, and to come back to when the Machine can't be reached.
(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const lang = MachineStrings.pick(navigator.languages || [navigator.language]);
  const T = MachineStrings.S[lang];
  document.documentElement.lang = lang;
  for (const el of document.querySelectorAll('[data-t]')) el.textContent = T[el.dataset.t];

  const plugins = (window.Capacitor && window.Capacitor.Plugins) || {};
  const shell = plugins.MachineShell;  // mobile/android, mobile/ios: MachineShellPlugin
  const push = plugins.PushNotifications;

  function show(id) {
    for (const s of document.querySelectorAll('main > section')) s.hidden = s.id !== id;
    const focus = document.querySelector('#' + id + ' input');  // a field only: a ring on a button looks like a bug
    if (focus) focus.focus({preventScroll: true});
  }

  // The push token, when this phone allows notifications. Asked for once, right after the first connect, so the
  // system question comes when it makes sense. Never blocks opening the Machine for long.
  async function pushToken(ask) {
    if (!push || !shell) return;
    try {
      const info = await shell.info();
      if (!info.pushReady) return;
      let state = (await push.checkPermissions()).receive;
      if (state === 'prompt' && ask) state = (await push.requestPermissions()).receive;
      if (state !== 'granted') return;
      await new Promise(resolve => {
        const done = setTimeout(resolve, 2500);
        push.addListener('registration', async t => { clearTimeout(done); await shell.pushToken({token: t.value}); resolve(); });
        push.addListener('registrationError', () => { clearTimeout(done); resolve(); });
        push.register();
      });
    } catch (e) { /* the Machine still opens; notifications can be turned on later */ }
  }

  // A Machine of their own, before it is saved: does it answer as one? 'machine', 'other' or 'unreachable'. The
  // native side fetches its manifest (the start page's own origin can't read another site's answer).
  async function check(url) {
    try {
      const r = await shell.check({url});
      return r.machine === true ? 'machine' : 'other';
    } catch (e) { return 'unreachable'; }
  }

  async function open(url, first) {
    show('busy');
    $('busy-text').textContent = '';
    if (MachineUrl.parse(url).kind === 'own') {
      const found = await check(url);
      if (found !== 'machine') {
        $('address').value = new URL(url).host + new URL(url).pathname.replace(/\/$/, '');
        $('own-error').textContent = found === 'other' ? T.errNotMachine : T.errUnreachable;
        $('own-error').hidden = false;
        show('own-form');
        return;
      }
    }
    await pushToken(first);
    await shell.setMachine({url});
    location.replace(url);
  }

  // Tailscale not on the phone: one line with where to get it (a Machine of their own is only reached through it)
  async function tailscaleNote(own) {
    if (!shell || !own) return;
    const info = await shell.info().catch(() => ({}));
    if (info.tailscale !== false) return;
    for (const p of document.querySelectorAll('.ts')) {
      p.hidden = false;
      p.querySelector('a').href = info.platform === 'ios' ? 'https://apps.apple.com/app/tailscale/id1470499037'
        : 'https://play.google.com/store/apps/details?id=com.tailscale.ipn';
    }
  }

  async function start() {
    if (!shell) { show('welcome'); return; }  // a plain browser (development): the screens only
    const state = await shell.get();
    tailscaleNote(document.body.dataset.page === 'offline' ? state.machine && MachineUrl.parse(state.machine).kind === 'own' : true);
    if (state.connect) {  // a scanned or tapped link to a Machine of their own: ask first, it changes where the app goes
      const parsed = MachineUrl.parse(state.connect);
      if (parsed.kind === 'own') {
        $('confirm-host').textContent = new URL(parsed.url).host;
        $('confirm-yes').onclick = () => open(parsed.url, true);
        $('confirm-no').onclick = () => { shell.clearConnect(); show('welcome'); };
        show('confirm');
        return;
      }
    }
    if (state.signin === 'stopped') {
      $('signin-error').textContent = T.signinStopped;
      $('signin-error').hidden = false;
    }
    if (document.body.dataset.page === 'offline') return;
    if (state.machine && MachineUrl.valid(state.machine) && state.signin !== 'stopped') {
      await pushToken(false);
      location.replace(state.machine);
      return;
    }
    show('welcome');
  }

  async function signIn() {
    $('signin-error').hidden = true;
    show('busy');
    $('busy-text').textContent = T.signingIn;
    await pushToken(true);
    try { await shell.signIn(); }  // the account's sign-in, in the system browser; it comes back to the Machine
    catch (e) {
      $('signin-error').textContent = T.signinStopped;
      $('signin-error').hidden = false;
      show('welcome');
    }
  }

  if ($('signin')) {
    $('signin').onclick = signIn;
    $('own').onclick = () => { $('own-error').hidden = true; show('own-form'); };
    $('own-back').onclick = () => show('welcome');
    $('own-connect').onsubmit = e => {
      e.preventDefault();
      const parsed = MachineUrl.parse($('address').value);
      if (parsed.kind === 'hosted') { signIn(); return; }
      if (parsed.error) {
        $('own-error').textContent = T.errAddress;
        $('own-error').hidden = false;
        $('address').focus();
        return;
      }
      open(parsed.url, true);
    };
  }
  if ($('retry')) {
    $('retry').onclick = async () => {
      const state = shell ? await shell.get() : {};
      if (state.machine && MachineUrl.valid(state.machine)) location.replace(state.machine);
      else location.replace('index.html');
    };
    // Tried again by itself once the device is online or the app is in front again (a computer that just woke up),
    // at most every few seconds: a Machine still away brings this page back, never a blank one.
    let tried = 0;
    const again = () => {
      if (Date.now() - tried < 5000 || navigator.onLine === false) return;
      tried = Date.now();
      $('retry').onclick();
    };
    window.addEventListener('online', again);
    document.addEventListener('visibilitychange', () => { if (!document.hidden) again(); });
    $('other').onclick = async () => { if (shell) await shell.forget(); location.replace('index.html'); };
  }
  start();
})();
