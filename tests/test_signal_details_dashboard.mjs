import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {dashboardPage} from './dashboard-page.mjs';
// The Details toggle in a card's originals only shows when it has something: headers, or a signal's technical part.
const html=await dashboardPage();
const block=html.slice(html.indexOf('const KIND_LABEL='),html.indexOf('async function fillMessage('));
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>`&#${c.charCodeAt(0)};`),sender=s=>s,safeURL=()=>true,fileSize=n=>n+' B',t=s=>s;
const fmt=html.slice(html.indexOf("let DL='en-US'"),html.indexOf('\n',html.indexOf('const fmtDHM=')));  // dates and times (locale_prefs.py)
const tag=html.slice(html.indexOf('class SafeHTML'),html.indexOf('\n',html.indexOf('const setHTML=')));  // html``, escaping with the esc above
const built=new Function('esc','sender','safeURL','fileSize','t','groupSender',fmt+'\n'+tag+'\n'+block+';return messageHTML')(esc,sender,safeURL,fileSize,t,s=>s),messageHTML=(...a)=>String(built(...a));
const at='2026-10-20T20:04:00Z';
const bare=messageHTML({kind:'signal',from:'',occurred_at:at,title:'A signal',body:'Something happened'},'s1',1);
assert.ok(!bare.includes('<summary>Details</summary>'),'no empty toggle');
assert.ok(bare.includes('<strong translate="no">Signal</strong>'),'a source nobody sent is named by its kind label');
const fault=messageHTML({kind:'signal',from:'The Machine',occurred_at:at,title:'The Machine: ValueError in call',body:'Talking with your Fleet failed.',
  details:'Where (innermost last):\n  fleet.py:255 in call\n\nCode version: <abc>'},'s1',1);
// Details holds only what isn't shown already: the sender is in the header, so only the technical part
assert.match(fault,/<details class="email-headers"><summary>Details<\/summary><pre class="email-tech">Where \(innermost last\):\n  fleet\.py:255 in call/);
assert.ok(fault.includes('Code version: &#60;abc&#62;'),'escaped');
// A To by name has its address under Details; a bare address is shown whole on the to-line, so no Details
const mail=messageHTML({kind:'email',from:'Sam <sam@example.com>',to:'Dana Reyes <dana@example.com>',occurred_at:at,title:'Hi',body:'x'},'s1',1);
assert.match(mail,/<summary>Details<\/summary><div><span>To<\/span> Dana Reyes &#60;dana@example\.com&#62;<\/div>/);
const plain=messageHTML({kind:'email',from:'Sam <sam@example.com>',to:'owner@example.com',occurred_at:at,title:'Hi',body:'x'},'s1',1);
assert.ok(!plain.includes('<summary>Details</summary>'),'nothing to add, no toggle');
console.log('signal details ok');
