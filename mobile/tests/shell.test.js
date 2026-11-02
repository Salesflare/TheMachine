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

test('a Machine of their own is a Tailscale https address', () => {
  assert.deepEqual(MachineUrl.parse('machine.tail1234.ts.net'), {url: 'https://machine.tail1234.ts.net/', kind: 'own'});
  assert.deepEqual(MachineUrl.parse(' https://Machine.tail1234.ts.net/dash '), {url: 'https://machine.tail1234.ts.net/dash/', kind: 'own'});
  assert.deepEqual(MachineUrl.parse('example.com'), {error: 'tailnet'});
  assert.deepEqual(MachineUrl.parse('localhost'), {error: 'address'});
  assert.deepEqual(MachineUrl.parse(''), {error: 'address'});
  for (const bad of ['http://machine.tail1234.ts.net', 'https://machine.tail1234.ts.net:8443',
    'https://u:p@machine.tail1234.ts.net', 'https://tail1234.ts.net', 'javascript:alert(1)',
    'https://machine.tail1234.ts.net/a%2f..', 'https://evil.com/.ts.net']) {
    assert.ok(MachineUrl.parse(bad).error, bad);
  }
});

test('only a normal saved address opens', () => {
  assert.ok(MachineUrl.valid('https://sam.app.themachine.computer/'));
  assert.ok(MachineUrl.valid('https://machine.tail1234.ts.net/'));
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

// www/inject.js in a fake Machine page
function page(href, {sessionOk = true, share = false} = {}) {
  const calls = [];
  const store = new Map();
  const win = {
    location: {href, hash: ''},
    localStorage: {getItem: k => store.get(k) ?? null, setItem: (k, v) => store.set(k, v)},
    fetch: async (url, opts = {}) => {
      calls.push({url, method: opts.method || 'GET', headers: opts.headers || {}, body: opts.body && JSON.parse(opts.body)});
      if (url.endsWith('api/session')) return {ok: sessionOk, status: sessionOk ? 200 : 401, json: async () => ({csrf: 'c1'})};
      return {ok: true, status: 200, json: async () => ({ok: true})};
    },
    setTimeout, atob: s => Buffer.from(s, 'base64').toString('binary'), File: class { constructor(parts, name, o) { Object.assign(this, {parts, name, type: o.type}); } },
    Uint8Array, JSON, Date, URL, String, Error, Promise, Array,
  };
  if (share) win.machineShare = d => { win.shared = d; return true; };
  const run = vm.runInNewContext('(' + fs.readFileSync(path.join(www, 'inject.js'), 'utf8') + ')', Object.assign(win, {window: win}));
  return {win, calls, store, run};
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
  assert.deepEqual(post.body, {action: 'app_push_register', args: {platform: 'fcm', token: 'x'.repeat(30), sandbox: false, label: 'Pixel'}});
  p.calls.length = 0;
  assert.equal((await p.run(payload)).push, undefined);
  assert.equal(p.calls.length, 0);
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
