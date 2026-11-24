// What the robot says: a to-do's notification, with its quick buttons and the one that opens it. There is no Send and no
// Approve here: a to-do opens in the dashboard, where its draft is read first. It goes by itself, not under the pointer.
(function () {
  'use strict';
  const {core: {invoke}, event: {listen}} = window.__TAURI__;
  const t = window.MachineText, {icon, when, minutes, said} = window.Parts;
  const kept = {}; // what is said takes the place of some, and they come back
  const $ = id => (kept[id] ??= document.getElementById(id));
  const STAYS = 12000, AFTER = 4000, UNDO = 8000;
  let say = null, hour12 = false, over = false, left = 0, since = 0, timer = 0, busy = false, picks = false;

  $('close').append(icon('close'));
  $('close').title = t.dismiss;
  $('close').setAttribute('aria-label', t.dismiss);
  const words = e => t.errors[e] || (typeof e === 'string' && e) || t.errors.failed;
  const button = (name, run, first) => Object.assign(document.createElement('button'), {type: 'button', textContent: name, onclick: run, className: first ? 'first' : ''});

  const fit = () => { if (say) invoke('bubble_fit', {height: Math.ceil($('panel').getBoundingClientRect().height)}); };
  new ResizeObserver(fit).observe($('panel'));
  setInterval(fit, 10000); // its window knows this page still is there
  // As long as it isn't hovered
  function stay(ms) { left = ms; since = Date.now(); clearTimeout(timer); if (!over && !busy) timer = setTimeout(done, ms); }
  function done() { clearTimeout(timer); say = null; $('panel').hidden = true; invoke('bubble_done'); }
  function hovered(on) {
    if (on === over) return;
    over = on;
    clearTimeout(timer);
    if (on) left = Math.max(2000, left - (Date.now() - since));
    else stay(left);
  }
  let told = false; // by its window (Linux)
  $('panel').addEventListener('pointerenter', () => told || hovered(true));
  $('panel').addEventListener('pointerleave', () => told || hovered(false));
  listen('over', e => { told = true; hovered(e.payload); });

  async function show() {
    const s = await invoke('bubble_state');
    if (!s.say) return;
    say = s.say;
    if (say.meeting && !(minutes(say.meeting.at) > -2)) return done(); // it waited for the box to close
    hour12 = s.hour12;
    busy = over = picks = false;
    $('panel').hidden = false;
    $('panel').classList.toggle('below', s.below);
    $('tail').style.left = s.tail + 'px';
    $('said').className = '';
    $('open').hidden = $('close').hidden = false;
    $('said').replaceChildren($('open'));
    const [title, line] = said(say);
    $('title').textContent = title;
    $('line').textContent = line;
    $('open').setAttribute('aria-label', [title, line].filter(Boolean).join('. '));
    $('buttons').hidden = false;
    drawn();
    stay(STAYS);
  }
  const isSnooze = q => q.act.startsWith('snooze') && say.snooze.length;
  // Snooze's choices under the buttons, as in the box
  function drawn() {
    const buttons = [button(say.meeting ? t.openBrief : say.opens, open, true), ...(say.meeting?.join ? [Object.assign(button(t.join, join), {id: 'join'})] : []), ...say.quick.map(q => {
      const b = button(q.name, () => (isSnooze(q) ? pick(!picks) : decide(q)));
      if (isSnooze(q)) b.setAttribute('aria-expanded', String(picks));
      b.dataset.act = q.act;
      return b;
    })];
    $('buttons').replaceChildren(...buttons);
    const q = picks && say.quick.find(isSnooze);
    const choice = (until, name, run) => { const b = Object.assign(button(name, run), {className: 'name'}); b.dataset.until = until; return b; };
    $('choices').replaceChildren(...(q ? [...say.snooze.map(([until, name]) => choice(until, name, () => decide(q, until))), choice('date', t.chooseDate, open)] : []));
    $('choices').hidden = !q;
    fit();
  }
  function pick(on) { picks = on; drawn(); stay(STAYS); }
  async function open() {
    try { await invoke('bubble_open', {todo: say.id}); done(); } catch (e) { fail(e); }
  }
  async function join() {
    try { await invoke('bubble_join', {todo: say.id}); done(); } catch (e) { fail(e); }
  }
  // As the notification's button on the phone
  async function decide(q, until) {
    const of = say;
    hold();
    try {
      const made = await invoke('todo_decide', {todo: of.id, act: q.act, until: until ?? null});
      if (say !== of) return;
      if (q.act === 'prepare') return went(t.preparing);
      went([q.said, when(made?.snoozed_until, hour12)].filter(Boolean).join(' · '), (async () => {
        hold();
        try { await invoke('todo_undo', {todo: of.id, act: q.act}); if (say === of) went(t.undone); } catch (e) { if (say === of) fail(e); }
      }));
    } catch (e) { if (say === of) fail(e); }
  }
  function hold() { busy = true; clearTimeout(timer); invoke('bubble_hold'); $('panel').querySelectorAll('#buttons button,#choices button').forEach(b => { b.disabled = true; }); }
  function went(line, undo) {
    busy = false;
    $('said').className = 'went';
    const turning = Object.assign(document.createElement('i'), {className: 'turning'});
    $('said').replaceChildren(...(line === t.preparing ? [turning] : []), Object.assign(document.createElement('span'), {textContent: line}), ...(undo ? [Object.assign(button(t.undo, undo), {className: 'link'})] : []));
    $('buttons').hidden = $('close').hidden = $('choices').hidden = true;
    fit();
    stay(undo ? UNDO : AFTER);
  }
  function fail(e) {
    busy = false;
    $('said').className = 'error';
    $('said').replaceChildren($('open'));
    $('line').textContent = words(e);
    picks = false;
    drawn();
    stay(STAYS);
  }
  $('open').addEventListener('click', open);
  $('close').addEventListener('click', done);
  addEventListener('contextmenu', e => e.preventDefault());
  addEventListener('keydown', e => { if (e.key === 'Escape') { if (picks) pick(false); else done(); } });
  listen('say', show).then(show);
})();
