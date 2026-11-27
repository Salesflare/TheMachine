// Settings (src/settings.rs). A switch shows what is so: one that didn't work goes back, with why.
(function () {
  'use strict';
  const {core: {invoke}, event: {listen}} = window.__TAURI__;
  const t = window.MachineText, $ = id => document.getElementById(id);
  const names = {'robot-name': t.setRobot, 'robot-hint': t.setRobotHint, 'notify-name': t.setNotify, 'notify-hint': t.setNotifyHint, 'browser-name': t.setBrowser, 'browser-hint': t.setBrowserHint, 'browser-yes': t.setBrowserYes, 'browser-no': t.setBrowserNo, 'login-name': t.setLogin, 'quits-name': t.setClose, keep: t.setKeep, quit: t.setQuit, update: t.setUpdate, signout: t.signOut};
  for (const [id, text] of Object.entries(names)) $(id).textContent = text;
  document.title = t.settings;
  const SETS = ['robot', 'notify', 'login'];
  const SYSTEM = ['Mac', 'Windows'].find(s => navigator.userAgent.includes(s)) || 'Linux';
  const words = e => (e === 'login' && t.errors.login[SYSTEM]) || t.errors[e] || t.errors.failed;

  async function show() {
    const s = await invoke('settings_state');
    $('robot').checked = s.robot;
    $('notify').checked = s.notify;
    $('notify-row').hidden = s.robot;
    $('notify-hint').textContent = s.blocked ? t.setNotifyBlocked[SYSTEM] : t.setNotifyHint;
    $('notify-hint').classList.toggle('warn', s.blocked);
    $('browser-row').hidden = !s.browser;
    $('login').checked = s.login === 'on';
    $('quits').value = s.quits ? '1' : '';
    $('update-name').textContent = t.setVersion.replace('{}', s.version);
    const out = s.out && t.setOut[s.out.how];
    $('update-hint').textContent = s.update ? t.setUpdateHint.replace('{}', () => s.update) : out ? out.replace('{}', () => s.out.version) : '';
    $('update').textContent = s.update ? t.setUpdate : t.setGet;
    $('update').hidden = !s.update && !out;
    $('account').hidden = !s.machine;
    if (s.machine) $('where').textContent = t.signedIn.replace('{}', () => new URL(s.machine).host);
  }
  async function set(id, on) {
    $('error').textContent = '';
    for (const x of SETS) $(x).disabled = true;
    try { await invoke('settings_set', {id, on}); } catch (e) { $('error').textContent = words(e); }
    for (const x of SETS) $(x).disabled = false;
    await show();
    $(id).focus();
  }
  for (const id of SETS) $(id).addEventListener('change', () => set(id, $(id).checked));
  const answer = async on => {
    $('error').textContent = '';
    try { await invoke('settings_set', {id: 'browser', on}); } catch (e) { $('error').textContent = words(e); }
    await show();
    if ($('browser-row').hidden) $('robot').focus();
  };
  $('browser-yes').addEventListener('click', () => answer(true));
  $('browser-no').addEventListener('click', () => answer(false));
  $('update').addEventListener('click', async () => {
    $('error').textContent = '';
    $('update').disabled = true;
    const opens = $('update').textContent === t.setGet; // a package's file, in the browser: it stays
    try { await invoke('update_apply'); if (opens) $('update').disabled = false; } catch { $('error').textContent = t.errors.update; $('update').disabled = false; }
  });
  $('quits').addEventListener('change', () => set('quits', !!$('quits').value));
  $('signout').addEventListener('click', async () => { await invoke('menu_item', {id: 'signout'}); });
  const fit = () => invoke('settings_fit', {height: Math.ceil($('panel').getBoundingClientRect().height)});
  listen('settings', show).then(show).then(() => { fit(); new ResizeObserver(fit).observe($('panel')); }); // that one may wait until it is shown
  addEventListener('focus', show); // the system's own switches may have changed
  addEventListener('contextmenu', e => e.preventDefault());
})();
