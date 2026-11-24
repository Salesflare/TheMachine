import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// What someone typed to send and didn't send yet (dashboard/todos-kept.js): it survives Esc, the ×, the phone's Back, another
// page and a reload, for a new email, every draft in the send dialog (its Ask for changes too) and a follow-up in its
// review, with the subject, From and who gets it. It is sealed in this browser, never posted, in the address or readable in
// storage, and gone on sign-out and for another owner. It never sends by itself, and nothing sends the draft without it. A
// draft that changed meanwhile and another tab's typing are never replaced: both stay. Discard (with Undo) and a send end
// it for good, also a send from another device or one whose answer was lost.
const raw=await dashboardPage(),CSRF='c'.repeat(64),A1='a1'.repeat(16),B2='b2'.repeat(16),now=new Date().toISOString(),shots=process.env.SHOTS||'';
let scope=A1;const page=()=>raw.replace('__CSRF__',CSRF).replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__',scope);
const E='1'.repeat(16),S='2'.repeat(16),F='3'.repeat(16),U='4'.repeat(16),T='5'.repeat(16),R='6'.repeat(16);
const rev=n=>n.repeat(12),card=(id,title,x)=>({id,title,body:'Text.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[1],...x});
const fresh=()=>[
 card(E,'Reply to Sam',{next_actions:[{kind:'email',revision:rev('a'),label:'Send',to:['sam@client.example'],to_name:'Sam',from:'me@acme.example',from_options:['me@acme.example','hello@acme.example'],subject:'Plan',body:'Hi Sam,\n\nHere is the plan.\n\nAlex'}]}),
 card(S,'Answer in Slack',{next_actions:[{kind:'slack',revision:rev('b'),label:'Send',to_name:'Robin',channel:'D1',body:'On it.'}]}),
 card(F,'Post the answer',{next_actions:[{kind:'finish',revision:rev('c'),label:'Post',message:'Thanks, done.',preview:'Post',to_name:'Support',url:'https://x.example/'}]}),
 card(U,'Follow up',{next_action:{kind:'email',revision:rev('d'),label:'Send',to:['lee@client.example'],to_name:'Lee',from:'me@acme.example',subject:'Pilot',body:'Hi Lee, any news?'},follow_up:{project:'Pilot',project_id:'project:1',board:'Testers',group:'board:1',n:1,max:3,channel:'email',auto:false,state:'open'}}),
 card(R,'Invite the team',{next_actions:[{kind:'email',revision:rev('e'),label:'Send',to:[],to_options:['jo@team.example','max@team.example'],from:'me@acme.example',subject:'Invite',body:'Hi all.'}]}),
 card(T,'Ask Robin',{status:'pending',body:'Robin runs it: [robin@venue.example](mailto:robin@venue.example).'})];
let cards=fresh(),posts=[],fail='';
const server=createServer(async(req,res)=>{let b='';for await(const x of req)b+=x;const u=new URL(req.url,'http://x');res.setHeader('Content-Type','application/json');
 if(u.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page());return}
 if(u.pathname==='/frame'){res.setHeader('Content-Type','text/html');res.end('<!doctype html><iframe src="/" style="width:1300px;height:800px"></iframe>');return}
 if(u.pathname==='/api/session'){res.end(JSON.stringify({csrf:CSRF,cache_scope:scope}));return}
 if(u.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},fleet:{on:false,fleets:[]}}));return}
 if(u.pathname==='/api/action'){const a=JSON.parse(b||'{}');posts.push(a);if(fail===a.action){res.statusCode=502;res.end('{}');return}
  if(a.action==='compose_from'){res.end(JSON.stringify({from:[{account_id:'w',from:'me@acme.example',area:'Work'},{account_id:'h',from:'me@home.example',area:'Personal'}],default:'me@acme.example',to_name:'Robin'}));return}
  if(a.action==='compose_email'){res.end(JSON.stringify({suggestion_id:'7'.repeat(16),revision:rev('7'),from_options:[]}));return}
  if(a.action==='revise_draft'){const s=cards.find(x=>x.id===a.args.suggestion_id),d=(s.next_actions||[s.next_action]).find(x=>x.revision===a.args.revision);
   if(!d){res.statusCode=409;res.end('{"error":"This draft changed."}');return}d.revision=rev('f');d.body=a.args.body;if(a.args.subject)d.subject=a.args.subject;res.end(JSON.stringify({revision:d.revision,body:d.body,subject:d.subject}));return}
  if(a.action==='card_chat'){res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k',items:[]}));return}}
 res.statusCode=u.pathname.startsWith('/brand/')||u.pathname==='/sw.js'?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',errors=[];
const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const context=async(w,h)=>{const c=await b.newContext({viewport:{width:w,height:h},hasTouch:w<500,isMobile:w<500});await c.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());return c};
const tab=async c=>{const p=await c.newPage();p.setDefaultTimeout(15000);p.on('pageerror',e=>errors.push(e.message));return p};
// The page had its chance to open the kept message by itself (ktBack): every request it would have made is answered
const settled=p=>p.evaluate(async()=>{await ktReady;ktBack();await navigator.locks.query();await fetch('/api/session')});
const ready=p=>p.locator('#suggestions article[id]').first().waitFor();
const shot=async(p,name)=>{if(shots)await p.screenshot({path:`${shots}/${name}-${p.viewportSize().width}.png`,animations:'disabled'})};
const smart=async(p,id)=>{await p.evaluate(x=>openSend(x,taskActions(state.suggestions.find(s=>s.id===x))[0].revision),id);await p.locator('#send-dialog[open]').waitFor()};
const typeIn=async(p,sel,text)=>{await p.locator(sel).click();await p.keyboard.press('Control+End');await p.keyboard.type(text)};
const from=async(p,v)=>{await p.locator('#send-from').click();const m=p.locator('#cm-menu');await m.waitFor({state:'visible'});await m.getByText(v,{exact:true}).click();await m.waitFor({state:'hidden'});await p.locator('#send-from',{hasText:v}).waitFor()};
const text=p=>p.locator('#send-rich-body').innerText();
// Asked again from here: waitForFunction takes an async function's promise itself for a yes
const kept=(p,ok,what)=>(async()=>{const end=Date.now()+10000;for(let v;;await new Promise(r=>setTimeout(r,100))){v=await p.evaluate(async()=>(await localCache.read('kept'))?.value||[]);
 if(ok(v))return;assert.ok(Date.now()<end,what+': '+JSON.stringify(v))}})();
const stored=(p,n)=>kept(p,v=>v.length===n,n+' kept');
const shut=async p=>{await p.locator('#send-dialog[open]').waitFor({state:'hidden'});await p.evaluate(()=>ktRun)};  // closed, and what was typed is written
const sends=()=>posts.filter(x=>/^(confirm_action|compose_email|revise_draft)$/.test(x.action));
const newEmail=async p=>{await p.goto(base+'#card='+T);await p.locator('a[href="mailto:robin@venue.example"]').first().click();await p.locator('#send-dialog[open]').waitFor()};
try{
 for(const [w,h] of [[1440,900],[390,844]]){
  cards=fresh();posts=[];scope=A1;const phone=w<500,c=await context(w,h),p=await tab(c);
  // 1. A new email: Esc keeps it, a row over the to-dos says so, Continue brings it back
  await newEmail(p);await p.fill('#send-subject','The room');await typeIn(p,'#send-rich-body','Is the room free on Friday?');
  await from(p,'me@home.example');
  assert.equal(await p.locator('#send-cancel').innerText(),'Discard');assert.ok(await p.locator('#send-cancel').isVisible(),'Discard shows, on a phone too');
  await shot(p,'1-typing');
  await p.keyboard.press('Escape');await shut(p);await p.locator('#toast',{hasText:'Kept, not sent.'}).waitFor();await stored(p,1);
  await p.goto(base);await ready(p);const row=p.locator('.kept-row');await row.filter({hasText:'Unsent email to Robin'}).waitFor();await shot(p,'2-row-after-esc');
  assert.equal(await p.locator('#send-dialog[open]').count(),0,'closed stays closed on the next start');
  await row.locator('[data-kept-go]').click();await p.locator('#send-dialog[open]').waitFor();await p.waitForFunction(()=>document.querySelector('#send-subject').value==='The room');
  assert.equal((await text(p)).trim(),'Is the room free on Friday?');assert.match(await p.locator('#send-head').innerText(),/me@home\.example/);await shot(p,'3-restored-after-esc');
  // Where they left it: typing goes on at the end
  await p.locator('#send-rich-body').focus();if(!phone)await p.keyboard.type(' Or Monday?');else await typeIn(p,'#send-rich-body',' Or Monday?');
  assert.equal((await text(p)).trim(),'Is the room free on Friday? Or Monday?');
  // 2. A reload (or a killed phone app) with the composer open: it opens again as it was
  await kept(p,v=>/Monday/.test(JSON.stringify(v)),'Monday kept');
  await p.reload();await p.locator('#send-dialog[open]').waitFor();await p.waitForFunction(()=>/Monday/.test(document.querySelector('#send-rich-body').innerText));
  assert.equal(await p.locator('#send-subject').inputValue(),'The room');await shot(p,'4-restored-after-reload');
  // Sealed here: not in plain storage, the address or anything the page posted
  assert.deepEqual(await p.evaluate(()=>[JSON.stringify(localStorage)+JSON.stringify(sessionStorage)+location.href].filter(x=>/room|robin/i.test(x))),[]);
  assert.equal(posts.filter(x=>/room/i.test(JSON.stringify(x))).length,0,'never posted');assert.deepEqual(sends(),[]);
  // A second tab doesn't open it too
  const p2=await tab(c);await p2.goto(base);await ready(p2);await p2.locator('.kept-row').waitFor();posts=[];await settled(p2);assert.ok(!posts.some(x=>x.action==='compose_from'));assert.equal(await p2.locator('#send-dialog[open]').count(),0);await p2.close();
  // 3. Discard: gone, with Undo
  await p.locator('#send-cancel').click();await shut(p);await p.locator('#toast',{hasText:'Discarded.'}).waitFor();await stored(p,0);await shot(p,'5-discarded');
  await p.locator('#toast button',{hasText:'Undo'}).click();await p.locator('#send-dialog[open]').waitFor();await p.waitForFunction(()=>/Monday/.test(document.querySelector('#send-rich-body').innerText));
  // 4. Sent: gone for good
  await p.locator('#send-confirm').click();await shut(p);await stored(p,0);
  assert.deepEqual(sends().map(x=>x.action),['compose_email','confirm_action']);assert.match(sends()[0].args.body,/Or Monday\?/);assert.equal(sends()[0].args.account_id,'h');
  await p.reload();await ready(p);posts=[];await settled(p);assert.ok(!posts.some(x=>x.action==='compose_from'));assert.equal(await p.locator('.kept-row,#send-dialog[open]').count(),0);
  // A row's own Discard, and one whose answer was lost: its to-do is there, so the row goes
  await newEmail(p);await p.fill('#send-subject','Keys');await p.keyboard.press('Escape');await shut(p);await stored(p,1);await p.goto(base);await p.locator('.kept-row [data-kept-drop]').click();await p.locator('.kept-row').waitFor({state:'detached'});await stored(p,0);
  await newEmail(p);await p.fill('#send-subject','Keys');await p.keyboard.press('Escape');await shut(p);await stored(p,1);
  cards.push(card('8'.repeat(16),'Keys',{created_at:new Date(Date.now()+5000).toISOString(),next_actions:[{kind:'email',revision:rev('8'),to:['robin@venue.example'],from:'me@acme.example',subject:'Keys',body:'x'}]}));
  await p.goto(base);await ready(p);await stored(p,0);assert.equal(await p.locator('.kept-row').count(),0);
  // 5. A prepared email: ×, with its subject and From; its to-do says so
  await smart(p,E);await p.fill('#send-subject','The plan');await typeIn(p,'#send-rich-body',' PS see you.');await from(p,'hello@acme.example');await p.locator('#send-dialog .snooze-heading button').click();await shut(p);await stored(p,1);
  await p.locator(`#task-${E} .kept-mark`,{hasText:'Edited, not sent.'}).waitFor();await p.locator(`#task-${E}`).scrollIntoViewIfNeeded();await p.locator(`#task-${E} .kept-mark`).scrollIntoViewIfNeeded();await shot(p,'6-mark-on-draft');
  await p.goto(base);await p.locator(`#task-${E} [data-kept-go]`).click();await p.waitForFunction(()=>/PS see you/.test(document.querySelector('#send-rich-body').innerText));
  assert.equal(await p.locator('#send-subject').inputValue(),'The plan');assert.match(await p.locator('#send-head').innerText(),/hello@acme\.example/);
  // Typed back to the draft as it was: nothing to keep
  await p.fill('#send-subject','Plan');await p.evaluate(()=>{mailLoad(draftText(sendDraft));cmLists.from.pick('me@acme.example');document.querySelector('#send-rich-body').dispatchEvent(new Event('input',{bubbles:true}))});
  assert.equal(await p.locator('#send-cancel').textContent(),'Cancel');await stored(p,0);await p.keyboard.press('Escape');await shut(p);
  // Who gets it
  await smart(p,R);await p.locator('#send-recipients input').nth(1).check();await p.locator('#send-recipients input').nth(0).uncheck();await stored(p,1);
  await p.keyboard.press('Escape');await shut(p);await p.goto(base);await smart(p,R);await p.waitForFunction(()=>document.querySelectorAll('#send-recipients input')[1].checked);assert.deepEqual(await p.evaluate(()=>sendRecipients()),['max@team.example']);await p.locator('#send-cancel').click();await shut(p);await stored(p,0);
  // 6. Every channel: Slack, a final step's message (its editor opens, so Confirm never posts the old words), Ask for changes
  await smart(p,S);await typeIn(p,'#send-body',' Tomorrow.');
  if(phone)await p.evaluate(()=>window.machineBack());else await p.keyboard.press('Escape');await shut(p);await p.goto(base);await smart(p,S);await p.waitForFunction(()=>document.querySelector('#send-body').value==='On it. Tomorrow.');await p.keyboard.press('Escape');await shut(p);
  await smart(p,F);await p.locator('#send-edit').click();await typeIn(p,'#send-body',' Bye.');await p.keyboard.press('Escape');await shut(p);await p.goto(base);await smart(p,F);await p.waitForFunction(()=>document.querySelector('#send-body').value==='Thanks, done. Bye.');assert.ok(await p.locator('#send-body').isVisible());await p.keyboard.press('Escape');await shut(p);
  await smart(p,E);await p.locator('#send-ask-open').click();await p.fill('#send-ask-text','Shorter please');await p.keyboard.press('Escape');await shut(p);await stored(p,3);assert.equal(await p.locator(`#task-${E} .kept-mark`).count(),0,'an unsent instruction is no edit of the draft');
  await p.goto(base);await ready(p);await smart(p,E);await p.waitForFunction(()=>document.querySelector('#send-ask-text').value==='Shorter please');assert.ok(await p.locator('#send-ask-text').isVisible());
  await p.locator('#send-ask-save').click();await shut(p);await stored(p,2);
  // 7. The draft changed on the Machine meanwhile: the new one shows, the typed one waits, and neither goes without a tap
  await smart(p,E);await typeIn(p,'#send-rich-body',' PS bring the sheet.');await p.keyboard.press('Escape');await shut(p);await stored(p,3);
  Object.assign(cards[0].next_actions[0],{revision:rev('9'),body:'Hi Sam,\n\nThe plan moved to Tuesday.\n\nAlex'});
  await p.goto(base);await p.locator(`#task-${E} .kept-mark`,{hasText:'This draft changed. What was typed is kept.'}).waitFor();await smart(p,E);await p.locator('#kept-note').waitFor();
  assert.match(await text(p),/moved to Tuesday/);await shot(p,'7-draft-changed');
  await p.locator('[data-kept-use]').click();assert.match(await text(p),/PS bring the sheet/);await p.locator('#kept-note',{hasText:'Showing what was typed.'}).waitFor();await shot(p,'8-draft-changed-use-it');
  await p.locator('[data-kept-use]').click();assert.match(await text(p),/moved to Tuesday/);await p.locator('#kept-note',{hasText:'What was typed is kept.'}).waitFor();
  await p.keyboard.press('Escape');await shut(p);await p.goto(base);await smart(p,E);await p.locator('#kept-note').waitFor();await p.locator('[data-kept-use]').click();posts=[];
  await p.locator('#send-confirm').click();await shut(p);assert.deepEqual(sends().map(x=>[x.action,x.args.revision]),[['revise_draft',rev('9')],['confirm_action',rev('f')]]);assert.match(sends()[0].args.body,/PS bring the sheet/);await stored(p,2);
  // 8. Saved on the Machine but the send failed: the saved words are the draft now, and nothing older comes back
  fail='confirm_action';await smart(p,S);await p.waitForFunction(()=>document.querySelector('#send-body').value==='On it. Tomorrow.');await p.locator('#send-confirm').click();await p.waitForFunction(()=>document.querySelector('#send-error').textContent);fail='';
  await p.keyboard.press('Escape');await shut(p);await stored(p,1);await p.waitForFunction(x=>taskActions(state.suggestions.find(s=>s.id===x))[0].body==='On it. Tomorrow.',S);await smart(p,S);assert.equal(await p.locator('#send-body').inputValue(),'On it. Tomorrow.');assert.equal(await p.locator('#kept-note').count(),0);
  // Sent from another device meanwhile: gone here
  await typeIn(p,'#send-body',' Soon.');await p.keyboard.press('Escape');await shut(p);await stored(p,2);
  Object.assign(cards[1].next_actions[0],{state:{status:'sent',sent_at:new Date(Date.now()+5000).toISOString()}});await p.goto(base);await ready(p);await stored(p,1);assert.equal(await p.locator(`#task-${S} .kept-mark`).count(),0);
  // 9. A follow-up in its review: Esc keeps it, and Send and Send all don't send the draft without it
  await p.locator('[data-fu-review]').last().click();await p.locator('[data-fr-edit]').click();await p.locator('.fr-edit').fill('Hi Lee, how is the pilot?');assert.equal(await p.locator('[data-fr-cancel]').innerText(),'Discard');await p.keyboard.press('Escape');
  await p.locator('.fr-item .kept-mark',{hasText:'Edited, not sent.'}).waitFor();await shot(p,'9-follow-up');posts=[];
  await p.locator('[data-fr-all]').click();await p.locator('[data-fr-error]',{hasText:'1 draft changed'}).waitFor();assert.deepEqual(sends(),[]);
  await p.goto(base);await ready(p);await p.locator('[data-fu-review]').last().click();await p.locator('[data-fr-send]').click();assert.equal(await p.locator('.fr-edit').inputValue(),'Hi Lee, how is the pilot?');assert.deepEqual(sends(),[]);
  await p.locator('[data-fr-save]').click();await p.locator('[data-fr-send]').waitFor();assert.equal(sends()[0].args.body,'Hi Lee, how is the pilot?');await stored(p,1);assert.equal(await p.locator('.fr-item .kept-mark').count(),0);
  await p.locator('[data-fr-edit]').click();await p.locator('.fr-edit').fill('Hello');await p.locator('[data-fr-cancel]').click();assert.match(await p.locator('.fr-body').innerText(),/how is the pilot/);await stored(p,1);await p.locator('[data-fr-close]').first().click();
  // Go through opens the send dialog for a draft with typed text: it never sends around it
  const goes=()=>p.evaluate(x=>crKind(state.suggestions.find(y=>y.id===x)),U);assert.equal(await goes(),'send');
  await smart(p,U);await typeIn(p,'#send-rich-body',' Thanks.');await p.keyboard.press('Escape');await shut(p);
  assert.equal(await goes(),'dialog');await p.evaluate(x=>ktDrop(ktList.find(e=>e.id===x).k),U);assert.equal(await goes(),'send');await stored(p,1);
  // 10. Sign-out and another owner: gone
  await newEmail(p);await p.fill('#send-subject','Mine');await p.keyboard.press('Escape');await shut(p);await stored(p,2);
  scope=B2;await p.goto(base);await ready(p);await stored(p,0);assert.equal(await p.locator('.kept-row').count(),0);scope=A1;await p.goto(base);await ready(p);assert.equal(await p.locator('.kept-row').count(),0,'another owner’s start wiped it');
  await newEmail(p);await p.fill('#send-subject','Mine');await p.keyboard.press('Escape');await shut(p);await stored(p,1);
  await p.evaluate(()=>localCache.wipe());assert.equal(await p.evaluate(()=>localStorage.kept??null),null);await p.goto(base);await ready(p);await stored(p,0);
  await c.close()}

 // 11. Two tabs with the same draft: an untouched one follows, one typed in keeps both, and Discard in one leaves the other's
 cards=fresh();posts=[];const c=await context(1440,900),a=await tab(c),z=await tab(c);await a.goto(base);await z.goto(base);await ready(a);await ready(z);
 await smart(a,E);await smart(z,E);await typeIn(a,'#send-rich-body',' From one.');await z.waitForFunction(()=>/From one/.test(document.querySelector('#send-rich-body').innerText));
 await typeIn(z,'#send-rich-body',' And two.');await a.waitForFunction(()=>document.querySelector('#kept-note')||/And two/.test(document.querySelector('#send-rich-body').innerText));
 await typeIn(a,'#send-rich-body',' More one.');await z.locator('#kept-note',{hasText:'Also edited in another tab.'}).waitFor();await shot(z,'10-two-tabs');
 assert.match(await text(z),/And two/);await z.locator('[data-kept-use]').click();assert.match(await text(z),/More one/);await z.locator('[data-kept-use]').click();assert.match(await text(z),/And two/);
 assert.deepEqual(sends(),[]);await c.close();

 // 12. Where nothing can be sealed (a frame, as the site's demo): kept while the page is open
 cards=fresh();const f=await context(1440,900),g=await tab(f);await g.goto(base+'frame');const fr=g.frames()[1];await fr.locator('#suggestions article[id]').first().waitFor();
 const reply=()=>fr.evaluate(x=>openSend(x,'a'.repeat(12)),E);await reply();await fr.locator('#send-rich-body').click();await g.keyboard.type('In a frame. ');await g.keyboard.press('Escape');await fr.locator('#send-dialog[open]').waitFor({state:'hidden'});
 await reply();await fr.waitForFunction(()=>/In a frame/.test(document.querySelector('#send-rich-body').innerText));await fr.locator('#send-cancel').click();await reply();assert.doesNotMatch(await fr.locator('#send-rich-body').innerText(),/In a frame/);
 assert.equal(await fr.evaluate(()=>localCache.on),false);
 assert.deepEqual(errors,[]);
}finally{await b.close();server.close()}
console.log('kept text ok');
