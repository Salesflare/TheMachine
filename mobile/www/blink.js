// The mascot blinks now and then, as on the dashboard (dashboard.html, the same closed-eyes frame from
// brand/avatar-blink.png): 150ms every 4 to 9 seconds, sometimes twice. Not with reduced motion or while out of sight.
(function () {
  'use strict';
  const still = window.matchMedia ? matchMedia('(prefers-reduced-motion: reduce)') : {matches: false, addEventListener() {}};
  const off = () => still.matches || document.hidden;
  const shown = el => { const r = el.getBoundingClientRect(); return el.isConnected && r.width > 0 && !el.closest('[hidden]'); };
  const timers = new Map();
  const plan = (el, first) => {
    clearTimeout(timers.get(el));
    if (!off()) timers.set(el, setTimeout(() => blink(el), first ? 1500 + Math.random() * 6000 : 4000 + Math.random() * 5000));
  };
  const shut = (el, on) => { el.setAttribute('src', on ? el.dataset.blink : el.dataset.open); };
  const blink = el => {
    if (off() || !shown(el)) { plan(el); return; }
    const twice = Math.random() < 0.2;
    shut(el, true);
    timers.set(el, setTimeout(() => {
      shut(el, false);
      if (!twice || off()) { plan(el); return; }
      timers.set(el, setTimeout(() => {
        shut(el, true);
        timers.set(el, setTimeout(() => { shut(el, false); plan(el); }, 150));
      }, 130));
    }, 150));
  };
  const all = () => document.querySelectorAll('img[data-blink]').forEach(el => {
    if (off()) { clearTimeout(timers.get(el)); shut(el, false); } else plan(el, true);
  });
  document.querySelectorAll('img[data-blink]').forEach(el => {
    el.dataset.open = el.getAttribute('src');
    const im = new Image();
    im.src = el.dataset.blink;  // ready before the first blink, so it never flashes empty
    (im.decode ? im.decode() : Promise.resolve()).then(() => plan(el, true), () => {});
  });
  document.addEventListener('visibilitychange', all);
  if (still.addEventListener) still.addEventListener('change', all);
})();
