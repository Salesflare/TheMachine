import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Go through (dashboard/todos-clear.js), on made-up data: the For you header says "about 5 min" (the owner's
// pace from the status) and, from two on, offers Go through, prepared and needs-you to-dos in one run. The run shows one to-do at a time with its title, who it
// goes to and the whole draft; Enter sends exactly the revision on screen through the send dialog's own confirm, → skips
// (nothing posted), S snoozes, Esc closes. A draft that needs a choice (who gets it) opens the send dialog instead. A
// send that fails keeps that to-do on screen with the error. A draft that changed after it was shown never goes: the
// run shows the new one first, and only then can it go. It ends with "2 replies out in 0:05" and goes back to the list.
// Nothing reaches anyone: the server here is a fixture that records the posts.
const dashboard=await dashboardPage();
const at=h=>new Date(Date.now()-h*36e5).toISOString();
const id=n=>(n+'').padStart(2,'0').repeat(8);
const LONG=Array.from({length:30},(_,i)=>`Line ${i+1} of the agreement notes.`).join('\n')+'\nLast line: thanks, Sam';
const base=()=>[
 {id:id(1),title:'Send Northfield the editable agreements',body:'Drafted a reply.',status:'prepared',scope:'work',created_at:at(1),event_ids:[1],
  next_actions:[{kind:'email',label:'Send reply',revision:'aa11bb22cc33',to:['dana.reyes@northfield.example'],to_name:'Dana Reyes',subject:'Agreements',body:LONG}]},
 {id:id(2),title:'Answer #support about duplicate reminders',body:'Drafted a reply.',status:'prepared',scope:'work',created_at:at(2),event_ids:[2],
  next_actions:[{kind:'slack',label:'Send reply',revision:'bb22cc33dd44',to_name:'Robin Hale',body:'Fixed in the next release.'}]},
 {id:id(3),title:'Reply to the venue about Friday',body:'Drafted a reply.',status:'prepared',scope:'work',created_at:at(3),event_ids:[3],
  next_actions:[{kind:'email',label:'Send reply',revision:'cc33dd44ee55',to_options:['events@venue.example','hello@venue.example'],to:[],subject:'Friday',body:'Friday works for us.'}]},
 {id:id(4),title:'Tell Lee the invoice is paid',body:'Drafted a reply.',status:'prepared',scope:'work',created_at:at(4),event_ids:[4],
  next_actions:[{kind:'email',label:'Send reply',revision:'dd44ee55ff66',to:['lee@ledger.example'],to_name:'Lee Park',subject:'Invoice',body:'Hi Lee, it is paid.'}]},
 {id:id(5),title:'Book the dentist',body:'Find a slot next week before noon.',status:'pending',scope:'personal',created_at:at(5),event_ids:[5]},
 {id:id(6),title:'Pick a paint color for the hallway',body:'Three samples are in the hallway.',status:'pending',scope:'personal',created_at:at(6),event_ids:[6]}];
let cards,posts,failSlack;
const reset=()=>{cards=base();posts=[];failSlack=true};
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},done_counts:{all:0},clear_pace:45});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:[],next:null,total:0}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({counts:{}}));return}
 if(url.pathname==='/api/events'){res.end('[]');return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body),a=r.args||{};
  if(r.action==='confirm_action'){posts.push(['send',a.suggestion_id,a.revision]);const c=cards.find(x=>x.id===a.suggestion_id);
   if(c.next_actions[0].kind==='slack'&&failSlack){res.statusCode=400;res.end(JSON.stringify({error:'Slack is not answering. Try again.'}));return}
   Object.assign(c,{status:'completed',closed_at:new Date().toISOString()});res.end('{}');return}
  if(r.action==='decide'){posts.push(['decide',a.suggestion_id,a.choice]);const c=cards.find(x=>x.id===a.suggestion_id);if(a.choice==='accept')c.status='accepted';res.end(JSON.stringify({status:c.status}));return}
  res.end(JSON.stringify(r.action==='card_chat'?{session:true,status:'ok',active:false,cursor:'k1',items:[]}:{}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const run=page=>page.locator('#clear-run');
const pos=page=>run(page).locator('.cr-pos').textContent();
const posted=n=>{const t0=Date.now();return new Promise((ok,no)=>{const w=()=>posts.length>=n?ok():Date.now()-t0>10000?no(Error('no post: '+JSON.stringify(posts))):setTimeout(w,50);w()})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){reset();const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+id(1)).waitFor();
  // The header: how long, at the owner's pace (6 × 45 s), without saying the count again, and the button; a tap on it doesn't fold the list.
  // Title, count and Go through on one row, the time and "Nothing goes out" on one line under it, at every width
  const head=page.locator('#section-foryou');
  assert.equal(await head.locator('.clear-time').textContent(),'about 5 min');
  for(const key of ['foryou'])assert.deepEqual(await page.locator('#section-'+key).evaluate(h=>{const mid=e=>{const r=e.getBoundingClientRect();return Math.round(r.top+r.height/2)},t=mid(h.querySelector('h2')),go=mid(h.querySelector('.clear-go')),time=mid(h.querySelector('.clear-time')),note=h.querySelector('.section-note');
   return [Math.abs(go-t)<=6,time>go,!note||mid(note)===time]}),[true,true,true],key+' at '+width);
  assert.deepEqual(await page.locator('[data-clear-run]').allTextContents(),['Go through'],'one Go through, for For you');
  await head.locator('[data-clear-run]').click();
  await run(page).waitFor({state:'visible'});
  assert.equal(await head.getAttribute('aria-expanded'),'true');
  const box=await run(page).boundingBox();
  if(mobile)assert.deepEqual([box.x,box.y,box.width,box.height],[0,0,390,844]);
  else assert.ok(Math.abs(box.x+box.width/2-720)<=16&&box.width<=680,'centered: '+JSON.stringify(box));  // as the other dialogs (a scrollbar's gutter aside)
  assert.equal(await run(page).locator('.cr-key').first().isVisible(),!mobile);  // the keys only where there's a keyboard
  // One at a time: its title, who it goes to, the whole draft (no Show more), Send with the card's actions
  assert.equal(await pos(page),'1 of 6');
  assert.equal(await run(page).locator('.cr-title').textContent(),'Send Northfield the editable agreements');
  assert.match(await run(page).locator('.draft .dm').textContent(),/To: Dana Reyes · Agreements/);
  assert.match(await run(page).locator('.draft .db').innerText(),/Line 30 of the agreement notes\.\s+Last line: thanks, Sam/);
  assert.equal(await run(page).locator('.cr-draft .more').isVisible(),false);
  assert.deepEqual(await run(page).locator('.cr-acts:not([hidden]) button').evaluateAll(b=>b.map(x=>x.firstChild.textContent)),['Send','Ask for changes','Snooze','Skip']);
  // Send (Enter on a computer, the button on a phone): the revision on screen, once, and on to the next
  if(mobile)await run(page).locator('[data-cr="go"]').click();else await page.keyboard.press('Enter');
  await page.waitForFunction(()=>document.querySelector('#clear-run .cr-pos')?.textContent==='2 of 6');
  assert.deepEqual(posts,[['send',id(1),'aa11bb22cc33']]);
  // A send that fails: the to-do stays, with the error
  await run(page).locator('[data-cr="go"]').click();await posted(2);
  await page.waitForFunction(()=>/Slack is not answering/.test(document.querySelector('#clear-run .cr-error')?.textContent||''));
  assert.equal(await pos(page),'2 of 6');
  // Skip: nothing posted
  if(mobile)await run(page).locator('[data-cr="skip"]').click();else await page.keyboard.press('ArrowRight');
  await page.waitForFunction(()=>document.querySelector('#clear-run .cr-pos')?.textContent==='3 of 6');
  assert.equal(posts.length,2);
  // A draft that needs a choice (who gets it) opens the send dialog; canceling it keeps the to-do in the run
  await run(page).locator('[data-cr="go"]').click();
  await page.locator('#send-dialog').waitFor({state:'visible'});
  assert.equal(posts.length,2);
  await page.keyboard.press('Escape');await page.locator('#send-dialog').waitFor({state:'hidden'});assert.ok(await run(page).isVisible());
  await page.waitForTimeout(300);assert.equal(await pos(page),'3 of 6');
  await run(page).locator('[data-cr="skip"]').click();
  await page.waitForFunction(()=>document.querySelector('#clear-run .cr-pos')?.textContent==='4 of 6');
  // Not displayed, never sent: the draft changes after the run showed it; Send posts nothing and shows the new one
  cards[3].next_actions[0]={...cards[3].next_actions[0],revision:'ee55ff66aa77',body:'Hi Lee, it is paid. The receipt is attached.'};
  await page.evaluate(()=>refresh());
  assert.match(await run(page).locator('.draft .db').innerText(),/it is paid\.$/);  // still the one it showed
  await run(page).locator('[data-cr="go"]').click();
  await page.waitForFunction(()=>/That draft changed/.test(document.querySelector('#clear-run .cr-error')?.textContent||''));
  await page.waitForTimeout(300);
  assert.equal(posts.length,2,'nothing went out for a draft that was not on screen: '+JSON.stringify(posts));
  assert.match(await run(page).locator('.draft .db').innerText(),/The receipt is attached\./);
  assert.equal(await run(page).locator('[data-cr="go"]').getAttribute('data-rev'),'ee55ff66aa77');
  // Now it was on screen: it goes, that revision
  await run(page).locator('[data-cr="go"]').click();await posted(3);
  assert.deepEqual(posts[2],['send',id(4),'ee55ff66aa77']);
  // Then the ones that need a decision, in the same run: Do it on a decision
  await page.waitForFunction(()=>document.querySelector('#clear-run .cr-pos')?.textContent==='5 of 6');
  assert.equal(await run(page).locator('.cr-title').textContent(),'Book the dentist');
  assert.equal(await run(page).locator('[data-cr="go"]').evaluate(b=>b.firstChild.textContent),'Do it');
  if(mobile)await run(page).locator('[data-cr="go"]').click();else await page.keyboard.press('Enter');
  await posted(4);assert.deepEqual(posts[3],['decide',id(5),'accept']);
  await page.waitForFunction(()=>document.querySelector('#clear-run .cr-pos')?.textContent==='6 of 6');
  // The end: how many went out and how long it took, then back to the list
  await run(page).locator('[data-cr="skip"]').click();
  await run(page).locator('.cr-done').waitFor();
  assert.match(await run(page).locator('.cr-done').textContent(),/^2 replies out in \d+:\d\d$/);
  await run(page).locator('[data-cr="close"]').click();
  await run(page).waitFor({state:'hidden'});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  // Esc closes a run mid-way; what it didn't reach stays as it was
  await head.locator('[data-clear-run]').click();await run(page).waitFor({state:'visible'});
  await page.keyboard.press('Escape');await run(page).waitFor({state:'hidden'});
  assert.equal(posts.length,4);assert.equal(cards[5].status,'pending');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('clear ready dashboard ok');
}finally{await browser?.close();server.close()}
