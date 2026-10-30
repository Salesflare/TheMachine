import assert from 'node:assert/strict';
import {dashboardPage} from './dashboard-page.mjs';
// A service's own 5xx or 429 on a connection reads as the service busy, by its full name (google_meet, not google).
const html=await dashboardPage();
const block=html.slice(html.indexOf('const syncError='),html.indexOf('const label='));
const t=(s,...a)=>a.reduce((x,v)=>x.replace('{}',v),Array.isArray(s)?s[0]:s);
const syncError=new Function('t',block+';return syncError')(t);
assert.equal(syncError('google_meet_http:HTTP_503'),'Google Meet had a problem on its side');
assert.equal(syncError('trello_http:HTTP_502'),'Trello had a problem on its side');
assert.equal(syncError('salesflare:HTTP_500'),'Salesflare CRM had a problem on its side');
assert.equal(syncError('shortcut_http:HTTP_429'),'Shortcut asked to slow down');
assert.equal(syncError('mystery_http:HTTP_503'),'The source had a problem on its side');
assert.ok(!/side|slow down/.test(syncError('google_meet_http:HTTP_403')),'a permission error is not the service being busy');
console.log('sync busy ok');
