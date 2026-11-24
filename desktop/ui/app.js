// The dashboard's window while it has no dashboard to show: to sign in, or when the Machine can't be reached (src/dash.rs).
(function () {
  'use strict';
  const {core: {invoke}, event: {listen}} = window.__TAURI__;
  const t = window.MachineText, $ = id => document.getElementById(id);
  let view = '', byAddress = false, busy = false;
  const words = e => t.errors[e] || (typeof e === 'string' && e) || t.errors.failed;
  const fill = (text, v) => text.replace('{}', () => v);

  async function show() {
    const s = await invoke('app_state');
    const same = s.view === view;
    view = s.view;
    if (!same) { byAddress = false; $('error').textContent = ''; }
    $('panel').hidden = view === 'blank';
    if (view === 'blank') return;
    const host = s.machine ? new URL(s.machine).host : '', off = view === 'offline';
    $('title').textContent = off ? fill(t.offline, host) : t.robot;
    $('line').textContent = off ? t.offlineHint : view === 'signedout' && host ? fill(t.signedOutOf, host) : view === 'moved' ? t.moved : t.signInWindow;
    $('go').textContent = off ? t.retry : t.signIn;
    by(byAddress);
  }
  function by(address) {
    byAddress = address;
    $('go').hidden = address;
    $('by-address').hidden = !address;
    $('other').hidden = view === 'offline';
    $('other').textContent = address ? t.account : t.own;
    (address ? $('address') : $('go')).focus();
  }
  $('address').placeholder = t.address;
  $('address').setAttribute('aria-label', t.address);
  $('connect').textContent = t.connect;
  $('other').addEventListener('click', () => { $('error').textContent = ''; by(!byAddress); });
  $('go').addEventListener('click', async () => {
    $('error').textContent = '';
    if (view === 'offline') return invoke('app_retry');
    try { await invoke('sign_in'); $('line').textContent = t.waitingBrowser; } catch (e) { $('error').textContent = words(e); }
  });
  $('by-address').addEventListener('submit', async e => {
    e.preventDefault();
    if (busy || !$('address').value.trim()) return;
    busy = $('connect').disabled = true;
    $('connect').textContent = t.connecting;
    $('error').textContent = '';
    try { await invoke('connect', {address: $('address').value}); } catch (x) { $('error').textContent = words(x); } // the dashboard comes
    busy = $('connect').disabled = false;
    $('connect').textContent = t.connect;
  });
  listen('signin', async e => { if (e.payload) { await show(); $('error').textContent = words(e.payload); } });
  listen('view', show).then(show);
  addEventListener('contextmenu', e => { if (!e.target.closest('input')) e.preventDefault(); });
  // Nothing is dropped here: the window would open it
  for (const name of ['dragover', 'drop']) addEventListener(name, e => e.preventDefault());
})();
