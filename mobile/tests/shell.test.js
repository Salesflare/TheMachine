// The app's own JavaScript: which addresses count as the owner's Machine, the start page's words, and what runs in
// the Machine's page (www/inject.js). Run: cd mobile && npm test (tests/test_mobile_shell.py runs it too).
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const MachineUrl = require('../www/machine-url.js');

const www = path.join(__dirname, '..', 'www');

test('a hosted Machine is reached through sign-in, whatever was typed', () => {
  for (const t of ['app.themachine.computer', 'https://app.themachine.computer/x', 'sam.app.themachine.computer']) {
    assert.deepEqual(MachineUrl.parse(t), {url: 'https://app.themachine.computer/', kind: 'hosted'});
  }
});

test('a Machine of their own is a Tailscale or its own https address', () => {
  assert.deepEqual(MachineUrl.parse('machine.tail1234.ts.net'), {url: 'https://machine.tail1234.ts.net/', kind: 'own'});
  assert.deepEqual(MachineUrl.parse(' https://Machine.tail1234.ts.net/dash '), {url: 'https://machine.tail1234.ts.net/dash/', kind: 'own'});
  // 443 and 8443 (a self-hosted Machine's default port) only
  assert.deepEqual(MachineUrl.parse('machine.tail1234.ts.net:8443'), {url: 'https://machine.tail1234.ts.net:8443/', kind: 'own'});
  assert.deepEqual(MachineUrl.parse('https://machine.tail1234.ts.net:443/'), {url: 'https://machine.tail1234.ts.net/', kind: 'own'});
  // A dashboard on its own https domain (one the cloud knows, or one the owner set up), on 443 or 8443
  assert.deepEqual(MachineUrl.parse('my.themachine.computer'), {url: 'https://my.themachine.computer/', kind: 'own'});
  assert.deepEqual(MachineUrl.parse('example.com'), {url: 'https://example.com/', kind: 'own'});
  assert.deepEqual(MachineUrl.parse('https://Desk.Example.co.uk:8443/assistant'), {url: 'https://desk.example.co.uk:8443/assistant/', kind: 'own'});
  assert.deepEqual(MachineUrl.parse('localhost'), {error: 'address'});
  assert.deepEqual(MachineUrl.parse(''), {error: 'address'});
  for (const bad of ['http://machine.tail1234.ts.net', 'https://machine.tail1234.ts.net:8080', 'https://machine.tail1234.ts.net:444',
    'https://alex.app.themachine.computer:8443',
    'https://u:p@machine.tail1234.ts.net', 'https://tail1234.ts.net', 'javascript:alert(1)',
    'https://machine.tail1234.ts.net/a%2f..',
    // no plain http, user, other port, IP address, bare name or hosted name on its own
    'http://my.example.com', 'https://u@my.example.com', 'https://my.example.com:8080', 'https://my.example.com:444',
    'https://192.168.1.10', 'https://10.0.0.1:8443', 'https://[fd7a::1]', 'https://100.64.0.1', 'https://desk', 'https://desk.local1',
    'https://a.b.sam.app.themachine.computer', 'https://-x.example.com', 'https://x_y.example.com', 'https://my.example.com/a b']) {
    assert.ok(MachineUrl.parse(bad).error, bad);
  }
});

test('only a Machine\'s own manifest (or its refusal) counts as a Machine', () => {
  const manifest = JSON.stringify({name: 'The Machine', start_url: '.', icons: []});
  assert.ok(MachineUrl.isMachine(200, manifest));
  assert.ok(MachineUrl.isMachine(403, JSON.stringify({error: 'Use the owner-authenticated Tailscale dashboard'})));
  for (const [status, body] of [[200, '<html>Welcome</html>'], [200, JSON.stringify({name: 'Other app', start_url: '.', icons: []})],
    [200, JSON.stringify({name: 'The Machine'})], [200, 'null'], [200, ''], [404, manifest], [403, JSON.stringify({error: 'Forbidden'})],
    [302, manifest], [500, manifest]]) {
    assert.ok(!MachineUrl.isMachine(status, body), `${status} ${body}`);
  }
});

test('only a normal saved address opens', () => {
  assert.ok(MachineUrl.valid('https://my.themachine.computer/'));
  assert.ok(MachineUrl.valid('https://my.example.com:8443/assistant/'));
  assert.ok(!MachineUrl.valid('https://my.example.com'));
  assert.ok(MachineUrl.valid('https://sam.app.themachine.computer/'));
  assert.ok(MachineUrl.valid('https://machine.tail1234.ts.net/'));
  assert.ok(MachineUrl.valid('https://machine.tail1234.ts.net:8443/'));
  assert.ok(!MachineUrl.valid('https://machine.tail1234.ts.net:8080/'));
  assert.ok(!MachineUrl.valid('https://sam.app.themachine.computer/x'));
  assert.ok(!MachineUrl.valid('https://app.themachine.computer/'));
  assert.ok(!MachineUrl.valid('https://machine.tail1234.ts.net'));
  assert.ok(!MachineUrl.valid('https://a.b.sam.app.themachine.computer/'));
  assert.ok(!MachineUrl.valid(null));
});

test('a sign-in only comes back to a hosted Machine\'s own handoff', () => {
  const t = 'A'.repeat(32);
  assert.deepEqual(MachineUrl.signinTarget(`https://sam.app.themachine.computer/_machine/auth?t=${t}&to=app`),
    {auth: `https://sam.app.themachine.computer/_machine/auth?t=${t}&to=app`, machine: 'https://sam.app.themachine.computer/'});
  for (const bad of [`https://evil.com/_machine/auth?t=${t}`, `https://sam.app.themachine.computer/other?t=${t}`,
    'https://sam.app.themachine.computer/_machine/auth?t=short', `http://sam.app.themachine.computer/_machine/auth?t=${t}`]) {
    assert.equal(MachineUrl.signinTarget(bad), null, bad);
  }
});

test('every start page word is in every language, and the pages use only known words', () => {
  const ctx = {};
  vm.runInNewContext(fs.readFileSync(path.join(www, 'strings.js'), 'utf8'), ctx);
  const {S, pick} = ctx.MachineStrings;
  assert.deepEqual(Object.keys(S).sort(), ['de', 'en', 'es', 'fr', 'it', 'nl', 'pt-BR']);
  const keys = Object.keys(S.en).sort();
  for (const [lang, words] of Object.entries(S)) {
    assert.deepEqual(Object.keys(words).sort(), keys, lang);
    for (const [k, v] of Object.entries(words)) {
      assert.ok(v.trim(), `${lang}.${k}`);
      assert.ok(!v.includes('—'), `${lang}.${k} has an em dash`);
    }
  }
  for (const page of ['index.html', 'offline.html']) {
    for (const [, k] of fs.readFileSync(path.join(www, page), 'utf8').matchAll(/data-t="([^"]+)"/g)) assert.ok(k in S.en, `${page}: ${k}`);
  }
  for (const k of fs.readFileSync(path.join(www, 'app.js'), 'utf8').matchAll(/\bT\.(\w+)/g)) assert.ok(k[1] in S.en, k[1]);
  assert.equal(pick(['pt-PT']), 'pt-BR');
  assert.equal(pick(['nl-BE', 'en']), 'nl');
  assert.equal(pick(['ja']), 'en');
});

test('no sign-up, plans or prices on the start pages (accounts are made and paid for on the web)', () => {
  const ctx = {};
  vm.runInNewContext(fs.readFileSync(path.join(www, 'strings.js'), 'utf8'), ctx);
  const all = JSON.stringify(ctx.MachineStrings.S.en).toLowerCase() + fs.readFileSync(path.join(www, 'index.html'), 'utf8').toLowerCase();
  for (const word of ['sign up', 'subscribe', 'price', 'trial', 'upgrade', 'buy', '€', '$']) assert.ok(!all.includes(word), word);
  assert.ok(!/href="https?:/.test(fs.readFileSync(path.join(www, 'index.html'), 'utf8')), 'no links out of the start page');
});

test('the start page\'s mascot blinks with the dashboard\'s frames, never with reduced motion', async () => {
  const brand = path.join(__dirname, '..', '..', 'brand');
  assert.ok(fs.readFileSync(path.join(www, 'img', 'machine.png')).equals(fs.readFileSync(path.join(brand, 'app-icon-192.png'))));
  assert.ok(fs.readFileSync(path.join(www, 'img', 'machine-blink.png')).equals(fs.readFileSync(path.join(brand, 'avatar-blink.png'))));
  for (const page of ['index.html', 'offline.html']) {
    const html = fs.readFileSync(path.join(www, page), 'utf8');
    assert.ok(html.includes('<script src="blink.js"></script>'), page);
    for (const [img] of html.matchAll(/<img class="avatar[^>]*>/g)) assert.match(img, /data-blink="img\/machine-blink\.png"/, page);
  }
  const run = async reduced => {
    const timers = [], srcs = [];
    const img = {dataset: {blink: 'img/machine-blink.png'}, isConnected: true, attrs: {src: 'img/machine.png'},
      getAttribute(k) { return this.attrs[k]; }, setAttribute(k, v) { this.attrs[k] = v; srcs.push(v); },
      getBoundingClientRect: () => ({width: 132}), closest: () => null};
    const ctx = {window: {matchMedia: true}, matchMedia: () => ({matches: reduced, addEventListener() {}}), Math, Promise, Map,
      document: {hidden: false, querySelectorAll: () => [img], addEventListener() {}},
      Image: class { decode() { return Promise.resolve(); } }, setTimeout: (f, ms) => { timers.push([f, ms]); return timers.length; }, clearTimeout() {}};
    vm.runInNewContext(fs.readFileSync(path.join(www, 'blink.js'), 'utf8'), ctx);
    await new Promise(r => setTimeout(r, 0));
    for (let i = 0; i < 4 && timers.length; i++) timers.shift()[0]();
    return srcs;
  };
  const blinked = await run(false);
  assert.deepEqual(blinked.slice(0, 2), ['img/machine-blink.png', 'img/machine.png']);
  assert.deepEqual(await run(true), []);
});

// www/inject.js in a fake Machine page
function page(href, {sessionOk = true, share = false, files = false} = {}) {
  const calls = [];
  const store = new Map();
  const clicks = [], posted = [], toasts = [];
  const win = {
    location: {href, hash: ''},
    localStorage: {getItem: k => store.get(k) ?? null, setItem: (k, v) => store.set(k, v)},
    fetch: async (url, opts = {}) => {
      calls.push({url, method: opts.method || 'GET', headers: opts.headers || {}, body: opts.body && JSON.parse(opts.body)});
      if (url.endsWith('api/session')) return {ok: sessionOk, status: sessionOk ? 200 : 401, json: async () => ({csrf: 'c1'})};
      if (url.includes('/api/action')) return {ok: true, status: 200, json: async () => ({ok: true, registered: true, id: 'dev_1'})};
      if (url.includes('missing')) return {ok: false, status: 404};
      const sent = url.includes('chat-file') ? 'attachment; filename="notes.txt"' : '';
      return {ok: true, status: 200, headers: {get: k => k === 'Content-Disposition' ? sent : null}, blob: async () => ({size: 2, type: 'text/plain', b64: 'aGk='})};
    },
    setTimeout, atob: s => Buffer.from(s, 'base64').toString('binary'), File: class { constructor(parts, name, o) { Object.assign(this, {parts, name, type: o.type}); } },
    Uint8Array, JSON, Date, URL, String, Error, Promise, Array,
  };
  if (share) win.machineShare = d => { win.shared = d; return true; };
  if (files) Object.assign(win, {
    MachineFiles: {postMessage: m => posted.push(JSON.parse(m))},
    document: {addEventListener: (type, f) => { if (type === 'click') clicks.push(f); }},
    HTMLAnchorElement: class { click() {} },
    FileReader: class { readAsDataURL(b) { this.result = 'data:text/plain;base64,' + b.b64; this.onload(); } },
    toast: (text, bad) => toasts.push([text, bad]),
    decodeURIComponent,
  });
  const run = vm.runInNewContext('(' + fs.readFileSync(path.join(www, 'inject.js'), 'utf8') + ')', Object.assign(win, {window: win}));
  // a tap on a link, as the page's own click listener sees it
  const tap = async attrs => {
    const a = {href: attrs.href, target: attrs.target || '', textContent: attrs.text || '', title: '', isConnected: true,
      hasAttribute: n => n in attrs, getAttribute: n => (n in attrs ? attrs[n] : null), closest: () => a};
    const e = {target: a, defaultPrevented: false, preventDefault() { this.defaultPrevented = true; }};
    clicks.forEach(f => f(e));
    await new Promise(r => setTimeout(r, 0));
    return e.defaultPrevented;
  };
  return {win, calls, store, run, posted, toasts, tap};
}

test('inject: does nothing outside the saved Machine', async () => {
  const p = page('https://evil.com/');
  assert.equal(Object.keys(await p.run({base: 'https://sam.app.themachine.computer/', push: {platform: 'fcm', token: 'x'.repeat(30)}})).length, 0);
  assert.equal(p.calls.length, 0);
});

test('inject: registers the push token once a week, with the page\'s own sign-in', async () => {
  const p = page('https://sam.app.themachine.computer/');
  const payload = {base: 'https://sam.app.themachine.computer/', push: {platform: 'fcm', token: 'x'.repeat(30), label: 'Pixel'}};
  assert.equal((await p.run(payload)).push, 'registered');
  const post = p.calls.find(c => c.method === 'POST');
  assert.equal(post.url, 'https://sam.app.themachine.computer/api/action');
  assert.equal(post.headers['X-CSRF-Token'], 'c1');
  assert.deepEqual(post.body, {action: 'app_push_register', args: {platform: 'fcm', token: 'x'.repeat(30), sandbox: false, label: 'Pixel', fetch: false}});
  p.calls.length = 0;
  assert.equal((await p.run(payload)).push, undefined);
  assert.equal(p.calls.length, 0);
});

test('inject: the Machine\'s browser on its own gets a floating close back to the dashboard', async () => {
  const made = [];
  const fake = href => { const p = page(href); Object.assign(p.win, {
    history: {length: 1, back() { p.win.wentBack = true; }},
    document: {referrer: '', body: {appendChild: el => made.push(el)}, documentElement: {}, getElementById: id => made.find(el => el.id === id) || null,
      addEventListener() {},
      createElement: () => { const el = {style: {}, attrs: {}, on: {}, setAttribute(k, v) { this.attrs[k] = v; }, addEventListener(k, f) { this.on[k] = f; }}; return el; }},
  }); p.win.location.replace = u => { p.win.replaced = u; }; return p; };
  const base = 'https://sam.app.themachine.computer/';
  const v = fake(base + 'browser/?autoconnect=1');
  await v.run({base});
  assert.equal(made.length, 1);
  assert.equal(made[0].attrs['aria-label'], 'Close the browser');
  assert.match(made[0].style.cssText, /width:44px;height:44px/);
  assert.match(made[0].style.cssText, /safe-area-inset-top/);
  made[0].on.click();
  assert.equal(v.win.replaced, base);
  await v.run({base});
  assert.equal(made.length, 1, 'once');
  made.length = 0;
  await fake(base).run({base});
  assert.equal(made.length, 0, 'not on the dashboard');
});

test('inject: a failed sign-in leaves the token for next time', async () => {
  const p = page('https://sam.app.themachine.computer/', {sessionOk: false});
  assert.equal((await p.run({base: 'https://sam.app.themachine.computer/', push: {platform: 'fcm', token: 'y'.repeat(30)}})).push, 'failed');
  assert.equal(p.store.size, 0);
});

test('inject: a share opens New to-do filled in, or adds the text as a to-do on an older dashboard', async () => {
  const share = {text: 'Look at this https://example.com', files: [{name: 'a.txt', type: 'text/plain', data: Buffer.from('hi').toString('base64')}]};
  const p = page('https://sam.app.themachine.computer/', {share: true});
  assert.equal((await p.run({base: 'https://sam.app.themachine.computer/', share})).share, 'opened');
  assert.equal(p.win.shared.text, share.text);
  assert.equal(p.win.shared.files[0].name, 'a.txt');
  const old = page('https://sam.app.themachine.computer/');
  assert.equal((await old.run({base: 'https://sam.app.themachine.computer/', share})).share, 'added');
  assert.equal(old.calls.find(c => c.method === 'POST').body.action, 'card_new');
});

test('inject: a tapped notification opens its to-do, and only a plain id', async () => {
  const p = page('https://sam.app.themachine.computer/');
  await p.run({base: 'https://sam.app.themachine.computer/', tag: 'abc_12'});
  assert.equal(p.win.location.hash, 'chat=abc_12');
  const q = page('https://sam.app.themachine.computer/');
  await q.run({base: 'https://sam.app.themachine.computer/', tag: 'x"><script>'});
  assert.equal(q.win.location.hash, '');
});

test('inject: an app that shows the notification itself says so, and registers again at once after the update', async () => {
  const p = page('https://sam.app.themachine.computer/');
  const base = 'https://sam.app.themachine.computer/', token = 'x'.repeat(30);
  assert.equal((await p.run({base, push: {platform: 'fcm', token}})).push, 'registered');
  p.calls.length = 0;
  // The same token, now with fetch (the new app): not "fresh", so the Machine hears it within the week
  assert.equal((await p.run({base, push: {platform: 'fcm', token, fetch: true}})).push, 'registered');
  assert.equal(p.calls.find(c => c.method === 'POST').body.args.fetch, true);
  p.calls.length = 0;
  assert.equal((await p.run({base, push: {platform: 'fcm', token, fetch: true}})).push, undefined);
  assert.equal(p.calls.length, 0);
});

test('inject: keeps the phone\'s id with the token, for Settings to tell this phone', async () => {
  const p = page('https://sam.app.themachine.computer/');
  await p.run({base: 'https://sam.app.themachine.computer/', push: {platform: 'fcm', token: 'z'.repeat(30)}});
  assert.equal(JSON.parse(p.store.get('machine-app-push')).id, 'dev_1');
});

test('inject: a download on the Machine goes to the app; a linked file opens there; another site\'s is left alone', async () => {
  const base = 'https://sam.app.themachine.computer/';
  const p = page(base, {files: true});
  await p.run({base});
  assert.equal(await p.tap({href: base + 'api/chat-file?id=1', download: 'list.csv'}), true);
  assert.equal(await p.tap({href: base + 'api/chat-file?id=2', target: '_blank', text: 'shown name'}), true);
  assert.equal(await p.tap({href: 'https://example.com/a.pdf', download: 'a.pdf'}), false);
  assert.equal(await p.tap({href: base + '#settings', target: '_blank'}), false);
  await new Promise(r => setTimeout(r, 5));
  assert.deepEqual(p.posted.map(x => [x.name, x.open, x.data]), [['list.csv', false, 'aGk='], ['notes.txt', true, 'aGk=']]);
});

test('inject: a file that can\'t be fetched says so', async () => {
  const base = 'https://sam.app.themachine.computer/';
  const p = page(base, {files: true});
  await p.run({base});
  await p.tap({href: base + 'api/agent-file?path=missing.md', target: '_blank'});
  await new Promise(r => setTimeout(r, 5));
  assert.equal(p.posted.length, 0);
  assert.deepEqual(p.toasts, [['That file couldn’t be read.', true]]);
});

test('inject: no file hook without the app\'s own bridge', async () => {
  const p = page('https://sam.app.themachine.computer/');
  await p.run({base: 'https://sam.app.themachine.computer/'});
  assert.equal(p.win.__machineFiles, undefined);
});

// the app's MachinePhone in a fake Machine page: the phone's answers, as Android gives them
function phone(p, answers) {
  const asked = [];
  p.win.MachinePhone = {postMessage: m => {
    const q = JSON.parse(m);
    asked.push(q.ask);
    setTimeout(() => p.win.MachinePhone.onmessage({data: JSON.stringify({id: q.id, ...answers[q.ask]})}), 0);
  }};
  return asked;
}

test('inject: the phone asks about the microphone and notifications; Open settings only once it won\'t ask again', async () => {
  const base = 'https://sam.app.themachine.computer/', device = {platform: 'fcm', label: 'Pixel'};
  const p = page(base), asked = phone(p, {mic: {state: 'blocked'}, push: {state: 'blocked'}, pushOn: {state: 'blocked'}, settings: {state: 'ok'}});
  await p.run({base, device});
  assert.equal(await p.win.machinePhone.state('mic'), 'blocked');
  assert.equal(await p.win.machinePhone.state('push'), 'blocked');
  assert.equal(await p.win.machinePhone.pushOn(), 'blocked');
  await p.win.machinePhone.settings();
  assert.deepEqual(asked, ['mic', 'push', 'pushOn', 'settings']);
  assert.equal(p.calls.length, 0);

  const q = page(base);
  phone(q, {pushOn: {state: 'on', token: 'f'.repeat(40)}});
  await q.run({base, device});
  assert.equal(await q.win.machinePhone.pushOn(), 'on');
  const post = q.calls.find(c => c.method === 'POST');
  assert.deepEqual(post.body, {action: 'app_push_register', args: {platform: 'fcm', token: 'f'.repeat(40), sandbox: false, label: 'Pixel', fetch: false}});
  assert.equal(JSON.parse(q.store.get('machine-app-push')).id, 'dev_1');

  const old = page(base);
  await old.run({base, device});
  assert.equal(old.win.machinePhone, undefined);  // no app bridge on this address: nothing to ask with
});

test('Android keeps the keyboard\'s own suggestions and autocorrect', () => {
  // captureInput swaps the WebView's input for a bare one, which turns off the keyboard's suggestions in every field
  const config = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'capacitor.config.json'), 'utf8'));
  assert.notEqual(config.android && config.android.captureInput, true);
});
