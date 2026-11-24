// A browser tells its Machine that it showed a notification (sw.js), so the email about it stays out: only after it
// showed, only with the name its own push carried, and never in the way of the notification.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';

const sw = await readFile(new URL('../sw.js', import.meta.url), 'utf8');
async function push(data, {show = async () => {}, answer = async () => new Response('{}')} = {}) {
  const asked = [], waits = [], listeners = {};
  const self = {location: {origin: 'https://m.example'}, navigator: {onLine: true}, addEventListener: (t, f) => (listeners[t] = f),
    registration: {scope: 'https://m.example/assistant/', showNotification: show}, clients: {matchAll: async () => [], claim: async () => {}}};
  vm.runInContext(sw, vm.createContext({self, URL, Response, Headers, Promise, Date, String, Error, setTimeout, AbortSignal, encodeURIComponent,
    caches: {open: async () => ({match: async () => null, put: async () => {}}), keys: async () => [], delete: async () => true},
    fetch: async (url, init) => { asked.push([url, init.credentials]); return answer(); }}), {filename: 'https://m.example/sw.js'});
  listeners.push({data: {json: () => data, text: () => ''}, waitUntil: p => waits.push(p)});
  await Promise.all(waits);
  return asked;
}
const data = {title: 'Reply', body: 'b', tag: '0123456789abcdef', shown: 'f'.repeat(32)};
assert.deepEqual(await push(data), [['https://m.example/assistant/api/notice?tag=0123456789abcdef&shown=' + 'f'.repeat(32), 'same-origin']]);
assert.deepEqual(await push(data, {show: async () => { throw new TypeError('No notification permission'); }}), [], 'permission off: nothing was shown');
assert.deepEqual(await push({...data, shown: undefined}), [], 'a push from before this: nothing to say back');
assert.deepEqual(await push({...data, tag: undefined}), []);
assert.equal((await push(data, {answer: async () => { throw new TypeError('offline'); }})).length, 1, 'offline: the notification stands');
console.log('service worker says what it showed ok');
