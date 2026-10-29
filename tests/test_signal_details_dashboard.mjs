import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {dashboardPage} from './dashboard-page.mjs';
// The Details toggle in a card's originals only shows when it has something: headers, or a signal's technical part.
const html=await dashboardPage();
const block=html.slice(html.indexOf('const KIND_LABEL='),html.indexOf('async function fillMessage('));
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>`&#${c.charCodeAt(0)};`),sender=s=>s,safeURL=()=>true,fileSize=n=>n+' B',t=s=>s;
const fmt=html.slice(html.indexOf("let DL='en-US'"),html.indexOf('\n',html.indexOf('const fmtDHM=')));  // dates and times (locale_prefs.py)
const messageHTML=new Function('esc','sender','safeURL','fileSize','t',fmt+'\n'+block+';return messageHTML')(esc,sender,safeURL,fileSize,t);
const at='2026-10-20T20:04:00Z';
const bare=messageHTML({kind:'signal',from:'',occurred_at:at,title:'A signal',body:'Something happened'},'s1',1);
assert.ok(!bare.includes('<summary>Details</summary>'),'no empty toggle');
assert.ok(bare.includes('<strong>Signal</strong>'),'a source nobody sent is named by its kind label');
const fault=messageHTML({kind:'signal',from:'The Machine',occurred_at:at,title:'The Machine: ValueError in call',body:'Talking with your Fleet failed.',
  details:'Where (innermost last):\n  fleet.py:255 in call\n\nCode version: <abc>'},'s1',1);
assert.match(fault,/<details class="email-headers"><summary>Details<\/summary><div><span>From<\/span> The Machine<\/div><pre class="email-tech">Where \(innermost last\):\n  fleet\.py:255 in call/);
assert.ok(fault.includes('Code version: &#60;abc&#62;'),'escaped');
const mail=messageHTML({kind:'email',from:'Sam <sam@example.com>',to:'owner@example.com',occurred_at:at,title:'Hi',body:'x'},'s1',1);
assert.match(mail,/<summary>Details<\/summary><div><span>From<\/span>/);
console.log('signal details ok');
