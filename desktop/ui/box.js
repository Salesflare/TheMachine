// The box at the robot: sign in, a new to-do (with files or a screenshot), a question, and the first of For you, each with
// the quick buttons of its notification. There is no Send and no Approve here: a to-do opens in the dashboard, where its
// draft is read first.
(function () {
  'use strict';
  const t = window.MachineText, native = window.Native;
  const $ = id => document.getElementById(id);
  const MAX_FILES = 5, MAX_BYTES = 10 * 1024 * 1024, MAX_IMAGE = 5 * 1024 * 1024;
  let kind = 'todo', busy = false, byAddress = false, files = [], draft = '', connected = false, machine = null, hidden = false, notice = false, fresh = false, written = null, snip = false, shooting = false;

  for (const [id, text] of Object.entries({
    'signin-intro': t.signInIntro, 'signin-go': t.signIn, 'notice-text': t.hidden, 'notice-ok': t.ok, connect: t.connect, 'kind-todo': t.todo, 'kind-ask': t.ask,
  })) $(id).textContent = text;
  for (const [id, text] of Object.entries({close: t.close, more: t.menu, address: t.address, kinds: t.kind})) $(id).setAttribute('aria-label', text);
  $('close').title = t.close;
  $('more').title = t.menu;
  $('address').placeholder = t.address;

  const words = e => t.errors[e] || (typeof e === 'string' && e) || t.errors.failed;
  const fill = (text, v) => text.replace('{}', () => v);
  const el = (tag, set, ...kids) => { const e = Object.assign(document.createElement(tag), set); e.append(...kids); return e; };

  const fit = () => native.fit(Math.ceil($('panel').getBoundingClientRect().height));
  new ResizeObserver(fit).observe($('panel'));

  // Pictures by path, as the dashboard's
  const ICONS = {
    prepare: 'M5 3.2l7.5 4.8L5 12.8z', done: 'M3 8.4l3.3 3.3L13 5', snooze: 'M8 2.2a5.8 5.8 0 1 0 0 11.6A5.8 5.8 0 0 0 8 2.2M8 5v3.2l2.1 1.3',
    file: 'M13 7.5l-4.9 4.9a3 3 0 0 1-4.3-4.3l5.3-5.2a2 2 0 0 1 2.8 2.8L6.7 11a1 1 0 0 1-1.4-1.4l4.6-4.6', shot: 'M2 5.2V3.5A1.5 1.5 0 0 1 3.5 2h1.7M10.8 2h1.7A1.5 1.5 0 0 1 14 3.5v1.7M14 10.8v1.7a1.5 1.5 0 0 1-1.5 1.5h-1.7M5.2 14H3.5A1.5 1.5 0 0 1 2 12.5v-1.7M8 5.6a2.4 2.4 0 1 0 0 4.8 2.4 2.4 0 0 0 0-4.8',
  };
  ICONS.snooze2h = ICONS.snooze;
  function icon(name) {
    const at = 'http://www.w3.org/2000/svg', svg = document.createElementNS(at, 'svg'), path = document.createElementNS(at, 'path');
    svg.setAttribute('viewBox', '0 0 16 16');
    svg.setAttribute('aria-hidden', 'true');
    path.setAttribute('d', ICONS[name]);
    svg.append(path);
    return svg;
  }

  async function show() {
    const s = await native.state();
    const was = connected;
    machine = s.machine;
    hidden = s.hidden;
    snip = s.snip;
    notice = s.notice; // until the box is closed
    $('notice').hidden = !notice;
    connected = !!machine && s.problem !== 'notowner';
    head(s);
    $('signin').hidden = connected || notice;
    $('compose').hidden = !connected || notice;
    if (!connected || notice) $('answer').hidden = true;
    if (was && !machine) { $('text').value = ''; files = []; draft = ''; mine = []; went.clear(); $('live').textContent = ''; showFiles(); } // signed out
    showReady(connected && !notice ? s.waiting : {todos: [], count: 0});
    if (was && !connected) signinBy(byAddress);
    ready();
    return s;
  }
  // What is known at once, then what the Machine says now
  async function load() {
    const s = await show();
    if (s.menu) menu(true); else focus();
    if (!machine) return;
    const before = connected;
    buttons();
    await native.look().catch(() => {});
    await show();
    if (connected !== before && !s.menu) focus();
  }
  const focus = () => setTimeout(() => (notice ? $('notice-ok') : connected ? $('text') : byAddress ? $('address') : $('signin-go')).focus(), 30);

  // One line: the greeting by this computer's clock, or that nothing is for them. A name too long for it is left out.
  function head(s) {
    const line = $('state'), {count, name, known} = s.waiting, hour = new Date().getHours();
    line.classList.toggle('error', !!s.problem);
    line.classList.toggle('greeting', !!s.machine && !s.problem);
    if (!s.machine || s.problem) {
      line.textContent = !s.machine ? t.signedOut : fill(s.problem === 'notowner' ? t.notIn : t.cantReach, new URL(s.machine).host);
      return;
    }
    const [plain, named] = known && !count ? t.nothing : t.hello[hour >= 5 && hour < 12 ? 'morning' : hour >= 12 && hour < 18 ? 'afternoon' : 'evening'];
    line.textContent = name ? fill(named, name) : plain;
    if (line.scrollWidth > line.clientWidth) line.textContent = plain;
  }
  // A row that was decided says so a while, in its place
  let rows = [], shown = {todos: [], count: 0}, mine = []; // mine: what was just added here, the newest first
  const went = new Map(), quick = new Map();
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
    const focused = document.activeElement?.closest?.('.todos li')?.dataset.id;
    rows = todos;
    $('todos').replaceChildren(...todos.map(x => row(x)), ...(more > 0 ? [el('li', {}, el('button', {type: 'button', className: 'name more', textContent: fill(t.more, more), onclick: () => native.openDashboard().catch(fail)}))] : []));
    if (focused) document.querySelector(`.todos li[data-id="${CSS.escape(focused)}"] button`)?.focus();
  }
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
    const name = el('button', {type: 'button', className: 'name', onclick: () => x.id !== undefined && native.openDashboard(x.id).catch(fail)});
    const title = el('span', {textContent: x.title}), sub = x.since && [named || !x.id ? '' : t.justAdded, x.state].filter(Boolean).join(' · ');
    name.append(title, ...(sub ? [el('span', {className: 'sub', textContent: sub})] : []));
    name.onpointerenter = name.onfocus = () => { name.title = title.scrollWidth > title.clientWidth ? x.title : ''; }; // only what is cut off
    li.append(name);
    const buttons = x.id && quick.get(x.id)?.buttons || [];
    if (buttons.length) li.append(el('span', {className: 'quick'}, ...buttons.map(b => {
      const button = el('button', {type: 'button', className: 'icon', title: b.name, onclick: () => decide(x, b)}, icon(b.act));
      button.setAttribute('aria-label', b.name + ': ' + x.title);
      button.dataset.act = b.act;
      return button;
    })));
    return li;
  }
  // The buttons the Machine names for each, as it is now
  async function buttons() {
    const ids = [...new Set([...mine, ...shown.todos].map(x => x.id).filter(Boolean))];
    await Promise.all(ids.map(async id => { quick.set(id, {buttons: await native.quick(id).catch(() => [])}); }));
    for (const id of quick.keys()) if (!ids.includes(id)) quick.delete(id);
    showReady(shown);
  }
  // As the notification's button on the phone. "Snoozed it · tomorrow 9:00"
  async function decide(x, b) {
    say('');
    went.set(x.id, {title: x.title, at: Math.max(0, rows.findIndex(r => r.id === x.id)), busy: true});
    showReady(shown);
    try {
      const done = await native.decide(x.id, b.act), undo = b.act !== 'prepare' && b.act;
      const line = [b.said, when(done?.snoozed_until)].filter(Boolean).join(' · ');
      Object.assign(went.get(x.id) || {}, {busy: false, line, undo, act: b.act});
      $('live').textContent = line;
      const m = mine.find(m => m.id === x.id);
      if (m) follow(m);
      setTimeout(() => { if (went.get(x.id)?.line === line) gone(x.id); }, undo ? 15000 : 4000);
    } catch (e) {
      went.delete(x.id);
      fail(e);
    }
    showReady(shown);
    if (went.get(x.id)?.undo) document.querySelector(`.todos li[data-id="${CSS.escape(x.id)}"] button`)?.focus();
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
  function when(until) {
    const at = until ? new Date(until) : null;
    if (!at || isNaN(at)) return '';
    const day = v => new Date(v).setHours(0, 0, 0, 0), days = Math.round((day(at) - day(Date.now())) / 864e5);
    const time = at.toLocaleTimeString([], {hour: 'numeric', minute: '2-digit'});
    return days <= 0 ? time : days === 1 ? fill(t.tomorrow, time) : at.toLocaleDateString([], {weekday: 'long'}) + ' ' + time;
  }

  // Sign-in
  function signinBy(address) {
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
    try { await native.signIn(); $('signin-intro').textContent = t.waitingBrowser; } catch (e) { $('signin-error').textContent = words(e); }
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
    fresh = true; // the box opens on it
    say(t.welcome);
    load();
  });

  // The menu, also a right click on the robot
  function menu(open) {
    $('menu').hidden = !open;
    $('more').setAttribute('aria-expanded', String(open));
    if (!open) return;
    const items = [...(machine ? ['dashboard'] : []), hidden ? 'show' : 'hide', ...(machine ? ['signout'] : []), 'quit'];
    const names = {dashboard: t.dashboard, hide: t.hide, show: t.show, signout: t.signOut, quit: t.quit};
    const where = machine && connected ? [el('li', {className: 'where', textContent: fill(t.signedIn, new URL(machine).host)})] : [];
    $('menu').replaceChildren(...where, ...items.map(id => el('li', {}, el('button', {type: 'button', className: 'name', id: 'menu-' + id, textContent: names[id], onclick: () => (id === 'dashboard' ? native.openDashboard().catch(fail) : native.menuItem(id))}))));
    $('menu').querySelector('button').focus();
  }
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
  const fail = e => say(words(e), true);
  $('text').addEventListener('input', () => { say(''); grow(); ready(); });
  $('text').addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); $('compose').requestSubmit(); }
  });
  document.querySelectorAll('[name=kind]').forEach(r => r.addEventListener('change', () => {
    kind = r.value;
    $('answer').hidden = true;
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
        const a = await native.ask(text);
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
    const m = {title: text || with_[0].name, state: t.adding, since: Date.now(), listed: null};
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
      Object.assign(m, {id: String(made.id), title: made.title || m.title, state: made.status === 'prepared' ? '' : t.needsYou, since: Date.now()});
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
    follow(m);
  }
  // How it goes: at once, soon after, and as long as the Machine is on it
  async function follow(m) {
    if (m.followed) return;
    m.followed = true;
    for (const wait of [0, 2000, 4000, ...Array(60).fill(5000)]) {
      await new Promise(ok => setTimeout(ok, wait));
      const s = await native.state();
      if (!s.open || !mine.includes(m) || wait === 5000 && !m.working) break;
      await native.look().catch(() => {});
      if (!wait) buttons();
    }
    m.followed = false;
  }

  // Files: they go up at once under this to-do's own key, and join it when it is added (as in New to-do, chat_files.py)
  const base64 = f => new Promise((ok, no) => {
    const r = new FileReader();
    r.onload = () => ok(String(r.result).split(',')[1] || '');
    r.onerror = no;
    r.readAsDataURL(f);
  });
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
  addEventListener('dragover', e => { e.preventDefault(); if (connected) $('panel').classList.add('drop'); });
  addEventListener('dragleave', e => { if (!e.relatedTarget) $('panel').classList.remove('drop'); });
  addEventListener('drop', e => {
    e.preventDefault();
    $('panel').classList.remove('drop');
    const f = [...(e.dataTransfer?.files || [])];
    if (f.length && connected) { toTodo(); add(f); }
  });
  function toTodo() { if (kind !== 'todo') document.querySelector('[name=kind][value=todo]').click(); }

  const close = () => native.close();
  $('close').addEventListener('click', close);
  $('notice-ok').addEventListener('click', close);
  addEventListener('keydown', e => { 
    if (e.key !== 'Escape') return;
    if (!$('adds').hidden) { adds(false); return $('plus').focus(); }
    if ($('menu').hidden) return native.close();
    menu(false);
    $('more').focus();
  });
  addEventListener('contextmenu', e => { if (!e.target.closest('input,textarea,#answer')) e.preventDefault(); });
  native.onFailed(fail);
  native.onListed(() => native.state().then(s => {
    head(s);
    showReady(connected && !notice ? s.waiting : {todos: [], count: 0});
    buttons();
  }));
  native.onOpened(() => { say(fresh ? t.welcome : ''); fresh = false; menu(false); adds(false); if (!shooting) { went.clear(); mine = []; } load(); });
  signinBy(false);
  load();
})();
