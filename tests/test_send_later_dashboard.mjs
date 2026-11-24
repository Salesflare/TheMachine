import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');
process.env.TZ='Europe/Brussels';  // the browser's zone too: its picker shows the hours the to-dos below have

// Send later, at 390 and 1440: the quiet button beside Send (not on LinkedIn), the Snooze picker with its own times, the
// scheduled to-do under Later with Send now, Change time and Cancel (also in its chat), the line when its mail can't be
// read yet, and the reason when it was taken back or asked for being late. Snooze's own picker is as before afterwards.
// SHOTS=<folder> writes a screenshot of each. No network beyond this fake server; nothing is sent.
const dashboard=await dashboardPage(),shots=process.env.SHOTS;
const now=new Date().toISOString(),MAIL='a1'.repeat(8),LATER='b2'.repeat(8),BACK='c3'.repeat(8),LATE='d4'.repeat(8),UNREAD='e5'.repeat(8),LINK='f6'.repeat(8),TWO='a7'.repeat(8);
const email=(revision,to_name,subject,body,extra={})=>({kind:'email',revision,to:[to_name.toLowerCase()+'@north.example'],to_name,from:'owner@example.org',subject,body,label:'Email '+to_name,...extra});
const draft=email('r'+'1'.repeat(11),'Robin','Re: Garden plan','Hi Robin,\n\nThe garden plan is ready. Can you confirm the dates?\n\nBest,\nAlex');
const day=(n,h)=>{const d=new Date();d.setDate(d.getDate()+n);d.setHours(h,30,0,0);return d.toISOString()};
const cards={};
const reset=()=>{for(const k of Object.keys(cards))delete cards[k];
 const card=(id,title,action,x={})=>cards[id]={id,title,body:'A made-up to-do.',status:'prepared',scope:'work',created_at:now,event_ids:[1],next_action:action,next_actions:[action],...x};
 card(MAIL,'Reply to Robin about the garden plan',draft);
 card(LATER,'Send Casey the paint colors',email('r'+'2'.repeat(11),'Casey','Paint colors','Hi Casey,\n\nHere are the colors for the hallway.\n\nBest,\nAlex'),
  {status:'snoozed',snoozed_until:day(2,9),resume_status:'prepared',send_later:{send_at:day(2,9),n:1,revisions:['r'+'2'.repeat(11)],until:day(2,10)}});
 const back=email('r'+'3'.repeat(11),'Noor','Workshop','Hi Noor,\n\nShall we plan the workshop?\n\nBest,\nAlex'),held={status:'blocked',error:'Not sent: Noor Vale wrote first.',held_by:{from:'Noor Vale',at:now,snippet:'Can we move the workshop to May?',event_id:7}};
 card(BACK,'Plan the workshop with Noor',{...back,state:held},{action_status:held});
 const late=email('r'+'4'.repeat(11),'Sam','Roof','Hi Sam,\n\nThe roofer comes on Monday.\n\nBest,\nAlex'),asked={status:'blocked',error:'Not sent: it was more than an hour late.'};
 card(LATE,'Tell Sam when the roofer comes',{...late,state:asked},{action_status:asked});
 const wait=email('r'+'5'.repeat(11),'Kim','Keys','Hi Kim,\n\nThe keys are at the desk.\n\nBest,\nAlex'),queued={status:'queued'};
 card(UNREAD,'Tell Kim where the keys are',{...wait,state:queued},{action_status:queued,send_later:{send_at:now,n:1,revisions:['r'+'5'.repeat(11)],until:day(0,23),due:true,unread:true}});
 card(LINK,'Answer Lee on LinkedIn',{kind:'linkedin',revision:'r'+'6'.repeat(11),to_name:'Lee',body:'Thanks, Lee.',label:'LinkedIn message'});
 const one=email('r'+'7'.repeat(11),'Ada','Quote','Hi Ada,\n\nThe quote.\n\nBest,\nAlex'),two=email('r'+'8'.repeat(11),'Max','Quote','Hi Max,\n\nThe quote.\n\nBest,\nAlex');
 card(TWO,'Send both quotes',{kind:'menu',revision:'r'+'9'.repeat(11),actions:[one,two]},{next_actions:[one,two]})};
const calls=[];
const status=()=>({suggestions:Object.values(cards),promises:[],connectors:[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}],
 suggestion_counts:{pending:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],reminders:{telegram:true,push:0},hours:{timezone:'Europe/Brussels',morning:'09:00'}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/chat'){res.end(JSON.stringify({items:[{kind:'reply',id:1,at:Date.now()-6e4,text:'Here is the email.',drafts:[{kind:'email',to:['casey@north.example'],subject:'Paint colors',body:cards[LATER].next_action.body}]}],active:null}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body),a=r.args,s=cards[a.suggestion_id];
  if(!/^(confirm_action|send_later_|revise_draft|decide|compose_)/.test(r.action)){res.end('{}');return}
  calls.push([r.action,a]);
  if(r.action==='compose_from'){res.end(JSON.stringify({from:[{from:'owner@example.org',account_id:'mail',area:'work'}],default:'owner@example.org',to_name:''}));return}
  if(r.action==='compose_email'){res.end(JSON.stringify({suggestion_id:MAIL,revision:draft.revision}));return}
  if(r.action==='confirm_action'&&a.later||r.action==='send_later_move'){const at=a.later;
   Object.assign(s,{status:'snoozed',snoozed_until:at,resume_status:'prepared',send_later:{send_at:at,n:(s.send_later?.n||0)+(r.action==='confirm_action'?1:0)||1,revisions:[a.revision||draft.revision],until:at}});res.end(JSON.stringify({status:'scheduled',send_at:at}));return}
  if(r.action==='send_later_cancel'){Object.assign(s,{status:'prepared',snoozed_until:null});delete s.send_later;res.end(JSON.stringify({status:'canceled'}));return}
  if(r.action==='send_later_now'){res.statusCode=400;res.end(JSON.stringify({error:'It’s already on its way.'}));return}
  res.end('{}');return}
 if(/^\/brand\/[\w.-]+\.(png|webp|woff2)$/.test(url.pathname)){try{const f=await readFile(new URL('..'+url.pathname,import.meta.url));res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':url.pathname.endsWith('.webp')?'image/webp':'font/woff2');res.end(f);return}catch{}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const toast=(page,text)=>page.waitForFunction(x=>document.querySelector('#toast').textContent.replace(/\s+/g,' ').includes(x),text);
const last=()=>calls.at(-1);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){reset();calls.length=0;const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:'light',locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  const shot=async(name,el)=>{if(shots)await (el||page).screenshot({path:`${shots}/${name}-${width}.png`,animations:'disabled'})};
  const opened=async id=>{await page.evaluate(id=>{location.hash='#card='+id},id);await page.waitForFunction(id=>{const r=document.querySelector('#task-'+id)?.getBoundingClientRect(),was=window.atTop;window.atTop=r?.top;return r?.height&&r.top>=0&&r.top<innerHeight/2&&was===r.top},id,{polling:200})};
  const send=async(id,revision)=>{await page.evaluate(([id,r])=>openSend(id,r),[id,revision]);await page.locator('#send-dialog').waitFor()};
  await page.goto(base);await page.locator('#task-'+MAIL).waitFor();

  // LinkedIn has no Send later; an email has it, and Send itself needs no extra step
  await send(LINK,cards[LINK].next_action.revision);assert.equal(await page.locator('#send-later').isVisible(),false);
  await page.evaluate(()=>document.querySelector('#send-dialog').close());
  await send(MAIL,draft.revision);assert.equal(await page.locator('#send-later').innerText(),'Send later');
  assert.equal(await page.locator('#send-act .primary').innerText(),'Send now');
  await shot('1-send');
  await page.locator('#send-later').click();await page.locator('#snooze-dialog').waitFor();
  assert.equal(await page.locator('#snooze-title').innerText(),'Send later');
  assert.match(await page.locator('#later-note').innerText(),/^If they write first, it waits for you\. If The Machine is off then, it goes when it’s back, up to an hour late\. After that it asks\.$/);
  assert.match((await page.locator('#snooze-dialog [data-snooze]').allInnerTexts()).join('|'),/^In 2 hours\|Tomorrow · 0?9:00( AM)?(\|Monday · 0?9:00( AM)?)?$/);
  await shot('2-pick');
  await page.locator('#snooze-custom').click();await shot('3-pick-date');
  // A time the clock skips is refused here, as in Snooze; nothing is approved yet
  await page.evaluate(()=>{snoozeDay='2027-03-28';document.querySelector('#snooze-time').value='02:30'});
  await page.locator('#snooze-save').click();assert.equal(await page.locator('#snooze-error').innerText(),'That time is skipped by the clock change. Choose another time.');
  await page.evaluate(()=>{snoozeDay=localDay(new Date());document.querySelector('#snooze-time').value='00:00'});
  await page.locator('#snooze-save').click();assert.equal(await page.locator('#snooze-error').innerText(),'Choose a time that hasn’t passed.');
  assert.deepEqual(calls,[]);
  // The last night of summer time: the picked 09:00 is that day's 09:00
  await page.evaluate(()=>{snoozeDay='2027-03-28';document.querySelector('#snooze-time').value='09:00'});
  await page.locator('#snooze-save').click();await page.locator('#send-dialog').waitFor({state:'hidden'});
  assert.equal(last()[0],'confirm_action');assert.equal(last()[1].later,'2027-03-28T07:00:00.000Z');assert.equal(last()[1].revision,draft.revision);
  await toast(page,'Sends ');
  // Canceled from the to-do: the draft is back
  await page.locator('#later-head').evaluate(h=>h.click());
  const act=(id,c)=>page.locator(`#task-${id} [data-choice="${c}"]`).first().evaluate(b=>b.click());
  await act(MAIL,'send-cancel');await toast(page,'Canceled. The draft waits in the to-do.');
  assert.deepEqual(last(),['send_later_cancel',{suggestion_id:MAIL}]);
  await page.waitForFunction(id=>!document.querySelector(`#task-${id} [data-choice="send-cancel"]`),MAIL);

  // Under Later: when it goes, its draft, and the three choices, never Unsnooze
  const text=async id=>(await page.locator('#task-'+id).first().evaluate(n=>n.textContent)).replace(/\s+/g,' ');
  assert.match(await text(LATER),/Sends \w+, \w+ \d+, \d/);assert.match(await text(LATER),/Here are the colors for the hallway\./);
  assert.doesNotMatch(await text(LATER),/Unsnooze|Back \w+,/);
  for(const c of ['send-now','send-time','send-cancel'])assert.equal(await page.locator(`#task-${LATER} [data-choice="${c}"]`).count(),1,c);
  await act(LATER,'send-now');await toast(page,'It’s already on its way.');
  await act(LATER,'send-time');await page.locator('#snooze-dialog').waitFor();
  assert.equal(await page.locator('#snooze-title').innerText(),'Change time');assert.equal(await page.locator('#snooze-time').inputValue(),'09:30');
  await shot('4-change-time');
  await page.evaluate(()=>{document.querySelector('#snooze-time').value='16:00'});await page.locator('#snooze-save').click();
  await toast(page,'Sends ');assert.equal(last()[0],'send_later_move');assert.equal(last()[1].later,new Date(new Date(day(2,9)).setHours(16,0,0,0)).toISOString());
  // Snooze's picker is its own again
  await page.evaluate(id=>openSnooze(id),BACK);assert.equal(await page.locator('#snooze-title').innerText(),'Snooze');
  assert.equal(await page.locator('#later-note').count(),0);assert.equal(await page.locator('#snooze-dialog [data-snooze]').first().getAttribute('data-snooze'),'2h');
  await page.evaluate(()=>document.querySelector('#snooze-dialog').close());

  // Can't be read yet; taken back; late: each says so on its to-do
  assert.match(await text(UNREAD),/Couldn’t check for a new message yet\. Trying until /);assert.doesNotMatch(await text(UNREAD),/Sending your approved draft/);
  assert.equal(await page.locator(`#task-${UNREAD} [data-choice="send-cancel"]`).count(),1);
  assert.match(await text(BACK),/Not sent: Noor Vale wrote first\./);assert.match(await text(BACK),/Can we move the workshop to May\?/);
  assert.match(await text(LATE),/Not sent: it was more than an hour late\./);
  for(const [id,name] of [[BACK,'6-taken-back'],[LATE,'7-late'],[UNREAD,'8-unread']])if(shots){await opened(id);await shot(name)}

  // Its chat: when it goes, with the same three choices
  await page.evaluate(id=>{location.hash='#chat='+id},LATER);await page.locator('#chat-status [data-choice="send-cancel"]').waitFor();
  assert.match((await page.locator('#chat-status').innerText()).replace(/\s+/g,' '),/^Sends .+ · Send now · Change time · Cancel$/);
  await shot('9-chat');
  await page.locator('#chat-status [data-choice="send-cancel"]').click();await toast(page,'Canceled.');
  await page.evaluate(()=>{location.hash=''});

  // Two emails in one to-do: Send later is on the last one, and both wait for the same time
  const [one,two]=cards[TWO].next_actions;calls.length=0;
  await page.evaluate(id=>openSendAll(id),TWO);await page.locator('#send-dialog').waitFor();assert.equal(await page.locator('#send-later').isVisible(),false);
  await page.locator('#send-confirm').click();await page.waitForFunction(()=>!document.querySelector('#send-later').hidden);
  await page.locator('#send-later').click();await page.locator('#snooze-dialog [data-snooze]').nth(1).click();await page.locator('#send-dialog').waitFor({state:'hidden'});
  assert.deepEqual(calls.map(([n,a])=>[n,a.revision]),[['confirm_action',one.revision],['confirm_action',two.revision]]);
  assert.ok(calls[0][1].later);assert.equal(calls[0][1].later,calls[1][1].later);

  // A new email: a missing subject is asked for first, then it is drafted and scheduled
  calls.length=0;await page.evaluate(()=>openCompose('robin@north.example','','mailto:robin@north.example','Hi Robin'));await page.locator('#send-dialog').waitFor();
  await page.locator('#send-subject').fill('Plan');await page.locator('#send-rich-body').fill('Hi Robin, see you Monday.');
  await page.locator('#send-later').click();await page.locator('#snooze-dialog [data-snooze]').first().click();await page.locator('#send-dialog').waitFor({state:'hidden'});
  assert.deepEqual(calls.map(c=>c[0]),['compose_from','compose_email','confirm_action']);assert.ok(last()[1].later);

  if(shots){reset();await page.goto(base+'#inbox');await page.reload();await page.locator('#task-'+MAIL).waitFor();await opened(LATER);await shot('5-scheduled')}
  if(process.env.VERBOSE)console.log('ok at',width);
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('send later dashboard ok');
