// The box at the robot: sign in, a new to-do (with files or a screenshot), a question, and the first of For you, each with
// the quick buttons of its notification. There is no Send and no Approve here: a to-do opens as the dashboard shows it,
// where its draft is read first.
(function () {
  'use strict';
  const t = window.MachineText, native = window.Native, {icon, when, fill, takes, dropped, base64, MAX_FILES, MAX_BYTES} = window.Parts;
  const $ = id => document.getElementById(id);
  const MAX_IMAGE = 5 * 1024 * 1024, LONGEST = 2000;
  let kind = 'todo', busy = false, byAddress = false, files = [], draft = '', connected = false, machine = null, hidden = false, notice = false, fresh = false, written = null, snip = false, settings = false, shooting = false, speaks = 'always';

  for (const [id, text] of Object.entries({
    'signin-intro': t.signInIntro, 'signin-go': t.signIn, 'notice-text': t.hidden, 'notice-ok': t.ok, connect: t.connect, 'kind-todo': t.todo, 'kind-ask': t.ask,
    'card-back-name': t.back, 'card-opening': t.opening,
  })) $(id).textContent = text;
  for (const [id, text] of Object.entries({close: t.close, 'card-close': t.close, 'card-app': t.openApp, more: t.menu, address: t.address, kinds: t.kind})) $(id).setAttribute('aria-label', text);
  $('close').title = $('card-close').title = t.close;
  $('card-app').title = t.openApp;
  $('more').title = t.menu;
  $('address').placeholder = t.address;

  const words = e => t.errors[e] || (typeof e === 'string' && e) || t.errors.failed;
  const el = (tag, set, ...kids) => { const e = Object.assign(document.createElement(tag), set); e.append(...kids); return e; };

  // With its menu open it may be taller than there is room: then the menu comes in the rows' place
  const fit = async () => {
    const height = Math.ceil($('panel').getBoundingClientRect().height), room = await native.fit(height);
    if (!$('menu').hidden && height > room) $('panel').classList.add('crowded');
  };
  new ResizeObserver(fit).observe($('panel'));

  async function show() {
    const s = await native.state();
    const was = connected;
    machine = s.machine;
    hidden = s.hidden;
    snip = s.snip;
    settings = s.settings;
    speaks = s.speaks;
    notice = s.notice; // until the box is closed
    $('notice').hidden = !notice;
    connected = !!machine && s.problem !== 'notowner';
    head(s);
    $('signin').hidden = connected || notice;
    $('compose').hidden = !connected || notice;
    if (!connected || notice) $('answer').hidden = true;
    if (!connected) asked = []; // of who was signed in
    if (was && !machine) { $('text').value = ''; files = []; draft = ''; mine = []; went.clear(); seenWorking.clear(); $('live').textContent = ''; showFiles(); } // signed out
    showReady(connected && !notice ? s.waiting : {todos: [], count: 0});
    if (was && !connected) signinBy(byAddress);
    ready();
    return s;
  }
  // What is known at once, then what the Machine says now
  async function load() {
    const s = await show();
    if (s.wanted && connected && !notice) openTodo({id: s.wanted});
    else if (s.menu) menu(true); else focus();
    if (!machine) return;
    const before = connected;
    await take();
    buttons();
    await native.look().catch(() => {});
    await show();
    if (connected !== before) { await take(); if (!s.menu) focus(); }
  }
  async function take() {
    const g = connected && !notice ? await native.given() : null;
    if (g) given({text: g.text, files: g.files.map(f => new File([bytes(f.data)], f.name, {type: f.kind}))});
    if (g?.error) fail(g.error);
  }
  const focus = () => setTimeout(() => (notice ? $('notice-ok') : connected ? $('text') : byAddress ? $('address') : $('signin-go')).focus(), 30);

  // One line: the greeting by this computer's clock, or that nothing is for them. A name too long for it is left out.
  function head(s) {
    const line = $('state'), {count, name, known} = s.waiting, hour = new Date().getHours();
    line.classList.toggle('error', !!s.problem);
    line.classList.toggle('greeting', !!s.machine && !s.problem);
    if (!s.machine || s.problem) {
      line.textContent = !s.machine ? t.signedOut : fill({notowner: t.notIn, off: t.isOff}[s.problem] || t.cantReach, new URL(s.machine).host);
      return;
    }
    const [plain, named] = known && !count ? t.nothing : t.hello[hour >= 5 && hour < 12 ? 'morning' : hour >= 12 && hour < 18 ? 'afternoon' : 'evening'];
    line.textContent = name ? fill(named, name) : plain;
    if (line.scrollWidth > line.clientWidth) line.textContent = plain;
  }
  // A row that was decided says so a while, in its place
  let asked = []; // what was asked and answered, while the answer is there: the next question goes on from it
  let rows = [], shown = {todos: [], count: 0}, mine = []; // mine: what was just added here, the newest first
  const went = new Map(), quick = new Map(), seenWorking = new Set();
  function showReady(waiting) {
    shown = waiting;
    for (const x of waiting.added || []) Object.assign(mine.find(m => m.id === x.id) || {}, {title: x.title, state: x.state, working: x.working, listed: x.listed});
    // First what was just added, unless the dashboard has it elsewhere: that has its own heading, and isn't counted
    const out = m => (m.listed === false || !waiting.count) && !went.has(m.id);
    const first = mine.filter(m => !out(m)), own = new Set(mine.map(m => m.id));
    const held = [...went].filter(([id]) => !own.has(id)).map(([id, w]) => ({id, title: w.title, at: w.at}));
    const rest = waiting.todos.filter(x => !own.has(x.id) && !went.has(x.id)).slice(0, Math.max(0, 3 - held.length - first.length));
    const todos = [...first, ...rest], count = waiting.count;
    for (const h of held.sort((a, b) => a.at - b.at)) todos.splice(h.at, 0, h);
    const gone = waiting.todos.filter(x => went.has(x.id) && !own.has(x.id)).length;
    const more = count - gone - rest.length - first.filter(m => m.listed).length;
    const here = $('answer').hidden, elsewhere = mine.filter(out);
    $('added').hidden = !elsewhere.length || !here;
    $('added-name').textContent = t.justAdded;
    $('added-todos').replaceChildren(...elsewhere.map(x => row(x, true)));
    $('ready').hidden = !todos.length || !here;
    $('ready-name').hidden = !count;
    $('ready-name').textContent = fill(t.ready, count);
    const at = document.activeElement, focused = at?.closest?.('.todos li')?.dataset.id;
    const active = at?.dataset.act ? `[data-act="${at.dataset.act}"]` : at?.dataset.until ? `[data-until="${at.dataset.until}"]` : '';
    rows = todos;
    if (!todos.concat(elsewhere).some(x => x.id === snooze)) snooze = null;
    $('todos').replaceChildren(...todos.map(x => row(x)), ...(more > 0 ? [el('li', {}, el('button', {type: 'button', className: 'name more', textContent: fill(t.more, more), onclick: () => native.openDashboard().catch(fail)}))] : []));
    if (focused) rowOf(focused, active)?.focus();
    if (working()) follow();
  }
  const rowOf = (id, part = '') => {
    const li = document.querySelector(`.todos li[data-id="${CSS.escape(id)}"]`);
    return li && (part && li.querySelector(part) || li.querySelector('button'));
  };
  function row(x, named) {
    const w = went.get(x.id), li = el('li', {});
    if (x.id) li.dataset.id = x.id;
    const since = x.since ? Date.now() - x.since : Infinity;
    if (since < 3000) { li.classList.add('new'); li.style.animationDelay = -since + 'ms'; }
    if (w?.line) {
      const undo = w.undo && el('button', {type: 'button', className: 'link', textContent: t.undo, onclick: () => unDo(x.id)});
      li.append(el('div', {className: 'went'}, el('span', {textContent: w.line}), ...(undo ? [undo] : [])));
      return li;
    }
    li.classList.toggle('busy', !!w);
    const name = el('button', {type: 'button', className: 'name', onclick: () => x.id !== undefined && openTodo(x)});
    // Its state, on one that was just added or that the Machine is on, and what came of it while the box is open
    if (x.working) seenWorking.add(x.id);
    const sub = x.since ? [named || !x.id ? '' : t.justAdded, x.state] : seenWorking.has(x.id) ? [x.state] : [];
    const title = el('span', {textContent: x.title}), says = sub.filter(Boolean).join(' · ');
    name.append(title, ...(says ? [el('span', {className: 'sub'}, ...(x.working ? [el('span', {className: 'turning'})] : []), says)] : []));
    name.onpointerenter = name.onfocus = () => { name.title = title.scrollWidth > title.clientWidth ? x.title : ''; }; // only what is cut off
    li.append(name);
    let buttons = x.id && quick.get(x.id)?.buttons || [];
    // It is at it: Do it stays where it was, off, so a press more does nothing
    if (x.id && x.working) buttons = [{act: 'prepare', name: x.state, off: true}, ...buttons.filter(b => b.act !== 'prepare')];
    if (buttons.length) li.append(el('span', {className: 'quick'}, ...buttons.map(b => {
      const picks = isSnooze(b) && x.snooze?.length;
      const button = el('button', {type: 'button', className: 'icon', title: b.name, disabled: !!b.off, onclick: () => (picks ? snoozing(snooze === x.id ? null : x.id) : decide(x, b))}, icon(b.act));
      button.setAttribute('aria-label', b.name + ': ' + x.title);
      if (picks) button.setAttribute('aria-expanded', String(snooze === x.id));
      button.dataset.act = b.act;
      return button;
    })));
    // The dashboard's own choices (todos-snooze.js): its last one, a date, is picked there
    const b = snooze !== null && snooze === x.id && x.snooze?.length && buttons.find(isSnooze);
    if (b) {
      const choice = (until, text, run) => { const c = el('button', {type: 'button', className: 'name', textContent: text, onclick: run}); c.dataset.until = until; return c; };
      const list = el('div', {className: 'choices'}, ...x.snooze.map(([until, text]) => choice(until, text, () => { snooze = null; decide(x, b, until); })),
        choice('date', t.chooseDate, () => { snooze = null; openTodo(x); }));
      list.setAttribute('role', 'group');
      list.setAttribute('aria-label', t.snoozeUntil + ': ' + x.title);
      list.onkeydown = e => {
        const step = {ArrowDown: 1, ArrowUp: -1}[e.key], all = [...list.querySelectorAll('button')];
        if (!step) return;
        e.preventDefault();
        all[(all.indexOf(document.activeElement) + step + all.length) % all.length].focus();
      };
      li.classList.add('open');
      li.append(list);
    }
    return li;
  }
  const isSnooze = b => b.act.startsWith('snooze');
  let snooze = null; // whose choices are open
  function snoozing(id) {
    const was = snooze;
    snooze = id;
    showReady(shown);
    if (id) rowOf(id, '.choices button')?.focus();
    else if (was) rowOf(was, '[data-act^=snooze]')?.focus();
  }
  // The buttons the Machine names for each, as it is now. Only the last ask counts: an earlier one that ends later knows
  // an older list, and would take the buttons of a to-do that came back meanwhile
  let buttonsAsked = 0;
  async function buttons() {
    const turn = ++buttonsAsked, ids = [...new Set(listed().map(x => x.id).filter(Boolean))];
    const got = await Promise.all(ids.map(async id => [id, await native.quick(id).catch(() => [])]));
    if (turn !== buttonsAsked) return;
    quick.clear();
    for (const [id, b] of got) quick.set(id, {buttons: b});
    showReady(shown);
  }
  // As the notification's button on the phone. "Snoozed it · tomorrow 9:00"
  async function decide(x, b, until) {
    if (went.has(x.id)) return; // once
    say('');
    if (b.act === 'prepare') return prepare(x, b);
    went.set(x.id, {title: x.title, at: Math.max(0, rows.findIndex(r => r.id === x.id)), busy: true});
    showReady(shown);
    try {
      const done = await native.decide(x.id, b.act, until), undo = b.act;
      const line = [b.said, when(done?.snoozed_until, shown.hour12)].filter(Boolean).join(' · ');
      Object.assign(went.get(x.id) || {}, {busy: false, line, undo, act: b.act});
      $('live').textContent = line;
      if (mine.some(m => m.id === x.id)) follow(true);
      setTimeout(() => { if (went.get(x.id)?.line === line) gone(x.id); }, 15000);
    } catch (e) {
      went.delete(x.id);
      fail(e);
    }
    showReady(shown);
    if (went.get(x.id)?.undo) rowOf(x.id)?.focus();
  }
  // Do it: its row stays, and says how it goes
  async function prepare(x, b) {
    went.set(x.id, {title: x.title, at: Math.max(0, rows.findIndex(r => r.id === x.id)), busy: true});
    showReady(shown);
    let error = null;
    try {
      await native.decide(x.id, b.act);
      $('live').textContent = b.said;
      const working = {state: t.preparing, working: true};
      for (const r of [...mine, ...shown.todos]) if (r.id === x.id) Object.assign(r, working);
    } catch (e) { error = e; }
    went.delete(x.id);
    if (error) fail(error);
    showReady(shown);
    if (!error) rowOf(x.id)?.focus();
    follow(true); // also when it was refused: something else is so by now
    buttons();
  }
  // Its line goes; the to-do itself is out of the list, unless the Machine still has it there
  function gone(id) {
    if (!went.delete(id)) return;
    mine = mine.filter(m => m.id !== id || m.listed); // done with
    native.state().then(s => { showReady(s.waiting); buttons(); });
  }
  async function unDo(id) {
    const w = went.get(id);
    w.undo = null;
    showReady(shown);
    try { await native.undo(id, w.act); $('live').textContent = t.undone; } catch (e) { fail(e); }
    await native.look().catch(() => {});
    gone(id);
  }
  // Sign-in
  let waits = 0;
  function waiting(on) {
    clearTimeout(waits);
    $('signin-go').textContent = t.signIn;
    if (on) waits = setTimeout(() => { $('signin-intro').textContent = t.nothingBack; $('signin-go').textContent = t.retry; }, 20000);
  }
  function signinBy(address) {
    waiting(false);
    byAddress = address;
    $('by-account').hidden = address;
    $('by-address').hidden = !address;
    $('signin-other').textContent = address ? t.account : t.own;
    $('signin-error').textContent = '';
    $('signin-intro').textContent = t.signInIntro;
  }
  $('signin-other').addEventListener('click', () => { signinBy(!byAddress); focus(); });
  $('signin-go').addEventListener('click', async () => {
    $('signin-error').textContent = '';
    try { await native.signIn(); $('signin-intro').textContent = t.waitingBrowser; waiting(true); } catch (e) { $('signin-error').textContent = words(e); }
  });
  $('signin').addEventListener('submit', async e => {
    e.preventDefault();
    if (busy || !byAddress || !$('address').value.trim()) return;
    busy = true;
    $('connect').disabled = true;
    $('connect').textContent = t.connecting;
    $('signin-error').textContent = '';
    try { await native.connect($('address').value); } catch (x) { $('signin-error').textContent = words(x); }
    busy = false;
    $('connect').disabled = false;
    $('connect').textContent = t.connect;
    if (!$('signin-error').textContent) { say(t.welcome); load(); }
  });
  native.onSignIn(error => {
    if (error) { signinBy(false); $('signin-error').textContent = words(error); return; }
    waiting(false);
    fresh = true; // the box opens on it
    say(t.welcome);
    load();
  });

  // The menu, also a right click on the robot
  function menu(open) {
    $('menu').hidden = !open;
    $('more').setAttribute('aria-expanded', String(open));
    if (!open) return $('panel').classList.remove('crowded');
    const items = [...(machine ? ['dashboard'] : []), hidden ? 'show' : 'hide', ...(settings ? ['settings'] : []), ...(machine ? ['signout'] : []), 'quit'];
    const names = {dashboard: t.dashboard, hide: t.hide, show: t.show, settings: t.settings + '…', signout: t.signOut, quit: t.quit};
    const where = machine && connected ? [el('li', {className: 'where', textContent: fill(t.signedIn, new URL(machine).host)})] : [];
    $('menu').replaceChildren(...where, ...items.map(id => el('li', {}, el('button', {type: 'button', className: 'name', id: 'menu-' + id, textContent: names[id], onclick: () => (id === 'dashboard' ? native.openDashboard().catch(fail) : native.menuItem(id))}))));
    if (machine) $('menu-dashboard').parentElement.after(el('li', {id: 'menu-speak', role: 'radiogroup', ariaLabel: t.speak, title: t.speakHint}, el('span', {className: 'where', textContent: t.speak}),
      ...Object.entries(t.speaks).filter(([when]) => when !== 'calm' || !mac).map(([when, name]) => el('button', {type: 'button', className: 'name', id: 'speak-' + when, role: 'radio', onclick: () => setSpeaks(when)}, name, icon('done')))));
    showSpeaks();
    $('menu').querySelector('button').focus();
  }
  const mac = navigator.platform.startsWith('Mac'); // which doesn't tell whether a Focus is on
  function showSpeaks() {
    for (const b of document.querySelectorAll('#menu-speak button')) b.setAttribute('aria-checked', String(b.id === 'speak-' + speaks));
  }
  function setSpeaks(when) { speaks = when; native.setSpeaks(when).catch(fail); showSpeaks(); }
  $('more').addEventListener('click', () => menu($('menu').hidden));

  // Writing
  const blank = () => !$('text').value.trim();
  function ready() {
    const up = files.some(f => !f.id);
    $('go').disabled = busy || up || (kind === 'todo' ? blank() && !files.length : blank());
    $('go').setAttribute('aria-label', kind === 'todo' ? t.addTodo : t.askSend);
    $('go').title = kind === 'todo' ? t.addTodo : t.askSend;
    $('text').placeholder = kind === 'todo' ? t.todoHint : t.askHint;
    $('text').setAttribute('aria-label', $('text').placeholder);
    $('plus').hidden = kind !== 'todo';
    const plus = snip ? t.add : t.addFile;
    $('plus').title = snip ? '' : plus; // its menu says it
    $('plus').setAttribute('aria-label', plus);
    if (kind !== 'todo') adds(false);
    $('files').hidden = kind !== 'todo' || !files.length;
    const there = !blank() || !!files.length;
    if (there !== written) native.draft(written = there);
  }
  function grow() {
    const x = $('text');
    x.style.height = 'auto';
    x.style.height = Math.min(x.scrollHeight, 120) + 'px';
  }
  const say = (text, error) => { $('said').replaceChildren(text); $('said').classList.toggle('error', !!error); };
  // That it can't be reached, or isn't signed in, is the line at the top: once
  async function fail(e) {
    if (machine && ['unreachable', 'notowner', 'off'].includes(e)) {
      say('');
      await native.look().catch(() => {});
      if ((await show()).problem) return;
    }
    say(words(e), true);
  }
  $('text').addEventListener('input', () => { say(''); grow(); ready(); });
  $('text').addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); $('compose').requestSubmit(); }
  });
  document.querySelectorAll('[name=kind]').forEach(r => r.addEventListener('change', () => {
    kind = r.value;
    $('answer').hidden = true;
    asked = [];
    say('');
    ready();
    native.state().then(s => showReady(s.waiting));
  }));
  $('kinds').addEventListener('click', e => { if (e.detail) focus(); }); // by the pointer: on to writing

  $('compose').addEventListener('submit', async e => {
    e.preventDefault();
    if ($('go').disabled) return;
    const text = $('text').value.trim(), asking = kind === 'ask';
    busy = asking; // the next to-do needn't wait for this one
    ready();
    try {
      if (!asking) {
        await addTodo(text, files, draft);
      } else {
        $('text').value = '';
        answer(text, t.thinking, true);
        const a = await native.ask(text, asked.slice(-3));
        if (connected && kind === 'ask') asked = [...asked, text].slice(-3);
        answer(text, a.answer || (a.off ? t.askOff : a.error ? t.errors.failed : t.noAnswer));
      }
    } catch (x) {
      if (asking) { $('answer').hidden = true; showReady(shown); }
      $('text').value = [text, $('text').value].filter(Boolean).join('\n'); // it comes back
      fail(x);
    }
    if (asking) busy = false;
    grow();
    ready();
    $('text').focus();
  });
  function answer(to, text, looking) {
    $('ready').hidden = $('added').hidden = true;
    $('answer').hidden = false;
    $('answer').classList.toggle('looking', !!looking);
    $('answer').setAttribute('aria-busy', String(!!looking));
    $('answer-to').textContent = $('answer-to').title = to;
    $('answer-text').textContent = text;
  }
  // Its row is there at once, the first of the list, and stays there while the box is open
  async function addTodo(text, with_, key) {
    const m = {title: text || with_[0].name, state: t.adding, working: true, since: Date.now(), listed: null};
    mine.unshift(m);
    files = [];
    draft = '';
    $('text').value = '';
    say('');
    showFiles();
    showReady(shown);
    grow();
    try {
      const made = await native.addTodo(m.title, key, with_.map(f => f.id));
      if (!made?.id) throw 'failed';
      Object.assign(m, {id: String(made.id), title: made.title || m.title, state: made.status === 'prepared' ? '' : t.needsYou, working: false, since: Date.now()});
    } catch (e) {
      mine = mine.filter(x => x !== m);
      files = [...with_, ...files];
      draft = key;
      showFiles();
      showReady(shown);
      throw e;
    }
    $('live').textContent = t.added;
    showReady(shown);
    follow(true);
  }
  // How it goes, while the box is open: at once and soon after something was done here, then as long as the Machine is on
  // one of them. Past five minutes the robot's own look will do.
  const listed = () => [...mine, ...shown.todos], working = () => listed().some(x => x.id && x.working);
  let soon = [], following = 0, followers = 0;
  async function follow(done) {
    if (done) soon = [0, 2000, 4000];
    else if (following) return;
    const me = ++followers, until = Date.now() + 300000;
    following = me;
    for (;;) {
      const wait = soon.length ? soon.shift() : working() && Date.now() < until ? 5000 : null;
      if (wait === null) break;
      await new Promise(ok => setTimeout(ok, wait));
      if (following !== me || !(await native.state()).open) break;
      await native.look().catch(() => {});
    }
    if (following === me) following = 0;
  }

  // Files: they go up at once under this to-do's own key, and join it when it is added (as in New to-do, chat_files.py)
  const key = () => [...crypto.getRandomValues(new Uint8Array(8))].map(b => b.toString(16).padStart(2, '0')).join('');
  function showFiles() {
    $('files').replaceChildren(...files.map(f => el('li', {className: f.id ? '' : 'up'}, ...(f.image ? [el('img', {src: f.image, alt: ''})] : []), el('span', {textContent: f.name}), el('button', {
      type: 'button', className: 'icon', textContent: '×', ariaLabel: fill(t.removeFile, f.name), onclick: () => { files = files.filter(x => x !== f); forget(f); showFiles(); },
    }))));
    ready();
  }
  // Taken back from the Machine too
  const forget = f => { if (f.id) native.removeFile(f.draft, f.id).catch(() => {}); };
  async function add(list) {
    say('');
    for (const f of list) {
      if (files.length >= MAX_FILES) { fail('files'); break; }
      if (f.size > MAX_BYTES) { fail('size'); continue; }
      const item = {name: f.name || 'image.png', id: null, draft: draft = draft || key()};
      files.push(item);
      showFiles();
      try {
        const data = await base64(f);
        if (/^image\/(png|jpeg|gif|webp)$/.test(f.type)) { item.image = `data:${f.type};base64,${data}`; showFiles(); }
        item.id = (await native.addFile(item.draft, item.name, data)).id;
        if (!files.includes(item)) forget(item); // removed meanwhile
      } catch (x) { files = files.filter(y => y !== item); fail(x); }
      showFiles();
    }
    $('text').focus();
  }
  // The + : its menu where a screenshot can be taken
  function adds(open) {
    $('adds').hidden = !open;
    $('plus').setAttribute('aria-expanded', String(open));
    if (!open) return;
    const items = [['file', t.addFile, () => $('pick').click()], ['shot', t.takeShot, shot]];
    $('adds').replaceChildren(...items.map(([id, name, run]) => el('li', {}, el('button', {type: 'button', className: 'name', id: 'add-' + id, onclick: () => { adds(false); run(); }}, icon(id), name))));
    $('adds').querySelector('button').focus();
  }
  $('plus').addEventListener('click', () => (snip ? adds($('adds').hidden) : $('pick').click()));
  const bytes = data => Uint8Array.from(atob(data), c => c.charCodeAt(0));
  async function shot() {
    if (files.length >= MAX_FILES) return fail('files');
    say('');
    let data = null, error = null;
    shooting = true;
    try { data = await native.screenshot(); } catch (e) { error = e; }
    await new Promise(ok => setTimeout(ok, 200)); // the box is open again
    shooting = false;
    if (error) return fail(error);
    if (!data) return focus();
    const type = data.startsWith('/9j/') ? 'image/jpeg' : 'image/png';
    let file = new File([bytes(data)], t.shotName + (type === 'image/png' ? '.png' : '.jpg'), {type});
    if (file.size > MAX_IMAGE) file = await smaller(file);
    add([file]);
  }
  // A large screen's: the Machine takes images up to 5 MB
  async function smaller(file) {
    const image = await createImageBitmap(file), canvas = el('canvas', {width: image.width, height: image.height});
    canvas.getContext('2d').drawImage(image, 0, 0);
    const jpeg = await new Promise(ok => canvas.toBlob(ok, 'image/jpeg', 0.85));
    return jpeg ? new File([jpeg], t.shotName + '.jpg', {type: 'image/jpeg'}) : file;
  }
  $('pick').addEventListener('change', () => { add([...$('pick').files]); $('pick').value = ''; });
  addEventListener('paste', e => { const f = [...(e.clipboardData?.files || [])]; if (f.length && connected) { e.preventDefault(); toTodo(); add(f); } });
  for (const on of ['dragenter', 'dragover']) addEventListener(on, e => { if (!takes(e.dataTransfer)) return; e.preventDefault(); if (connected) $('panel').classList.add('drop'); }); // robot.js
  addEventListener('dragleave', e => { if (!e.relatedTarget) $('panel').classList.remove('drop'); });
  addEventListener('drop', e => {
    e.preventDefault();
    $('panel').classList.remove('drop');
    if (connected) given(dropped(e.dataTransfer));
  });
  // Dropped here or on the robot: it is in the box, and goes nowhere before a tap. Files go up as those of + do
  function given({text, files: f}) {
    if (card) cardBack();
    const all = [$('text').value.trim(), text].filter(Boolean).join('\n');
    if (text) { $('text').value = all.slice(0, LONGEST); grow(); ready(); }
    if (f.length) { toTodo(); add(f); } else say('');
    if (all.length > LONGEST) fail('long');
    focus();
  }
  function toTodo() { if (kind !== 'todo') document.querySelector('[name=kind][value=todo]').click(); }

  // One to-do in the box, by its Machine's own dashboard; where that has no page for it, the app or the browser
  const LEAST = 340, ALL = 9999;
  let card = null, most = 0, own = 0, over = 0;
  async function openTodo(x) {
    if (!x.id) return native.openDashboard().catch(fail);
    say('');
    try {
      const tall = await native.cardOpen(x.id);
      if (!tall) return await native.openDashboard(x.id);
      card = x;
      most = tall;
      own = Math.min(LEAST, most);
      $('panel').style.height = own + 'px';
      $('panel').classList.add('card');
      $('card').hidden = false;
      $('card-back').focus();
      over = setTimeout(() => cardSaid('failed'), 15000);
      cardFit();
    } catch (e) { fail(e); }
  }
  // As tall as its page, and never less tall again while it is open: what is in it stays where it is. A dialog may have
  // more room while it is there.
  function cardTall(tall) {
    if (!card) return;
    const wanted = Math.min(most, $('panel').offsetHeight - $('card-place').offsetHeight + tall);
    if (tall < ALL) own = Math.max(own, wanted);
    $('panel').style.height = (tall < ALL ? own : most) + 'px';
  }
  function cardFit() {
    const r = $('card-place').getBoundingClientRect();
    if (card) native.cardPlace(r.top, r.height);
  }
  new ResizeObserver(cardFit).observe($('card-place'));
  // Closed by the person, or a while after it was done there
  function cardBack() {
    if (!card) return;
    const id = card.id;
    card = null;
    clearTimeout(over);
    native.cardClose();
    $('card').hidden = true;
    $('panel').classList.remove('card');
    $('panel').style.height = '';
    (rowOf(id) || $('text')).focus();
    native.look().catch(() => {});
  }
  function cardSaid(state) {
    if (!card) return;
    clearTimeout(over);
    const id = card.id;
    if (state === 'done' || state === 'snoozed') over = setTimeout(cardBack, 8000);
    if (['back', 'gone', 'offline'].includes(state)) cardBack();
    if (state === 'failed' || state === 'signed-out') { cardBack(); native.openDashboard(id).catch(fail); }
  }
  native.onCard(cardSaid);
  native.onTall(cardTall);
  $('card-back').addEventListener('click', cardBack);
  $('card-app').addEventListener('click', () => card && native.openDashboard(card.id).catch(fail));

  const close = () => native.close();
  $('close').addEventListener('click', close);
  $('card-close').addEventListener('click', close);
  $('notice-ok').addEventListener('click', close);
  addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    if (card) return cardBack();
    if (snooze !== null) return snoozing(null);
    if (!$('adds').hidden) { adds(false); return $('plus').focus(); }
    if ($('menu').hidden) return native.close();
    menu(false);
    $('more').focus();
  });
  addEventListener('contextmenu', e => { if (!e.target.closest('input,textarea,#answer')) e.preventDefault(); });
  native.onFailed(fail);
  native.onGiven(take);
  native.onListed(() => show().then(buttons));
  native.onOpened(() => { say(fresh ? t.welcome : ''); fresh = false; menu(false); adds(false); cardBack(); snooze = null; if (!shooting) { went.clear(); seenWorking.clear(); mine = []; } load(); });
  signinBy(false);
  load();
})();
