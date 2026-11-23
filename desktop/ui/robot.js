// The robot: a click opens or closes the box, a drag moves it, a right click or Menu key opens the box on its menu. A dot while
// something is new since the person last looked. Hidden, a click brings it back. It blinks now and then, as in the phone app (mobile/www/blink.js), never with reduced motion.
(function () {
  'use strict';
  const {core: {invoke}, event: {listen}} = window.__TAURI__;
  const robot = document.getElementById('robot'), face = document.getElementById('face'), dot = document.getElementById('dot');
  const t = window.MachineText;
  const FAR = 6; // pixels before a press is a drag
  let press = null, dragged = false, frame = 0, hidden = false, fresh = false;

  function show(news, away) {
    fresh = news;
    dot.hidden = !fresh;
    hidden = away;
    robot.setAttribute('aria-label', away ? t.robotHidden : fresh ? t.robotDot : t.robot);
    robot.title = away ? t.robotHidden : '';
  }
  show(false, false);
  listen('dot', e => show(e.payload === true, hidden));
  listen('hidden', e => show(fresh, e.payload === true));
  listen('box', e => robot.setAttribute('aria-expanded', String(e.payload === true)));
  invoke('robot_state').then(s => show(s.dot, s.hidden));

  // The dashboard's list (list.js), from what the Machine answered
  let list = new window.ForYou(), of = null;
  async function news() {
    const {news, added} = await invoke('robot_take');
    for (const n of news) {
      if (n.machine !== of) { of = n.machine; list = new window.ForYou(); }
      const fits = list.take(n), all = fits ? list.list() : [];
      await invoke('robot_list', {machine: of, todos: fits ? all.slice(0, 3) : null, marks: all.map(x => x.mark), name: fits ? list.name() : '', hour12: fits && list.hour12(), added: fits ? list.added(added, all) : []});
    }
  }
  let turn = Promise.resolve();
  const take = () => { turn = turn.then(news).catch(() => {}); };
  listen('news', take).then(take);

  robot.addEventListener('pointerdown', e => {
    dragged = false;
    if (e.button !== 0) return;
    press = {x: e.clientX, y: e.clientY};
    robot.setPointerCapture(e.pointerId);
  });
  robot.addEventListener('pointermove', async e => {
    const p = press;
    if (!p || hidden) return; // a hidden one comes back with a click
    if (!dragged) {
      if (Math.hypot(e.clientX - p.x, e.clientY - p.y) < FAR) return;
      dragged = true;
      // True: a picture of it goes along (windows::carry), and the robot itself isn't shown until it is dropped
      if (await invoke('robot_grab', {x: p.x, y: p.y}) && press === p) face.classList.add('carried');
    }
    if (!frame) frame = requestAnimationFrame(() => { frame = 0; if (press === p) invoke('robot_drag'); });
  });
  const up = async () => {
    const was = press && dragged;
    press = null;
    if (!was) return;
    await invoke('robot_drop');
    face.classList.remove('carried');
  };
  robot.addEventListener('pointerup', up);
  robot.addEventListener('pointercancel', up);
  robot.addEventListener('click', () => {
    if (dragged) { dragged = false; return; }
    invoke('robot_click');
  });
  addEventListener('contextmenu', e => { e.preventDefault(); invoke('robot_menu'); });
  robot.addEventListener('keydown', e => { if (e.key === 'F10') { e.preventDefault(); invoke('robot_menu'); } });

  // Dropped on it: the box opens with it
  const {takes, dropped, base64, MAX_FILES, MAX_BYTES} = window.Parts;
  const over = on => robot.classList.toggle('over', on);
  addEventListener('dragover', e => { if (!takes(e.dataTransfer)) return; e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; over(true); });
  addEventListener('dragleave', e => { if (!e.relatedTarget) over(false); });
  addEventListener('drop', async e => {
    e.preventDefault();
    over(false);
    const {text, files} = dropped(e.dataTransfer), kept = [];
    let error = files.length > MAX_FILES ? 'files' : null;
    for (const f of files.slice(0, MAX_FILES)) {
      if (f.size > MAX_BYTES) { error = 'size'; continue; }
      try { kept.push({name: f.name || 'image.png', kind: f.type, data: await base64(f)}); } catch { error = 'file'; } // a folder
    }
    if (text || kept.length || error) invoke('robot_given', {given: {text, files: kept, error}});
  });

  const still = matchMedia('(prefers-reduced-motion: reduce)');
  function blink() {
    if (!still.matches && !document.hidden) {
      face.src = 'img/machine-blink.png';
      setTimeout(() => { face.src = 'img/machine.png'; }, 150);
    }
    setTimeout(blink, 4000 + Math.random() * 5000);
  }
  new Image().src = 'img/machine-blink.png';
  setTimeout(blink, 3000);
})();
