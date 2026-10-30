import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The dashboard with the keyboard only, the way someone without a mouse walks it. Suggestions lands on the first to-do;
// J/K and ↓ ↑ go through the to-dos and the heads of the folded lists, so a page with everything folded is still
// explorable (Enter or → opens a list, ← folds it); Enter opens a to-do's chat with the box to type in focused, Esc
// leaves the box and closes the chat, and the to-do gets focus back. Esc closes New to-do, the shortcut sheet and the
// palette and focus goes back to where it was. The ring shows on whatever has focus. Nothing is sent from a key.
// SHOT_DIR=<folder> also saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),soon=new Date(Date.now()+86400000).toISOString();
const card=(id,title,status,more={})=>({id,title,body:'A short note about it.',status,scope:'work',created_at:now,event_ids:[1],...more});
const cards=[card('a1a1a1a1a1a1a1a1','Reply to the venue about the dates','prepared',{preparation_status:'done'}),
 card('a2a2a2a2a2a2a2a2','Send the deck to the board','prepared',{preparation_status:'done'}),
 card('b1b1b1b1b1b1b1b1','Decide on the new office lease','pending'),
 card('c1c1c1c1c1c1c1c1','Renew the domain','snoozed',{snoozed_until:soon})];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const actions=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/cards/done'){res.end('{"cards":[],"total":0}');return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r.action);
  if(r.action==='card_chat'){res.end(JSON.stringify({session:false,status:'blocked',active:false,cursor:null,items:[]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const run=async(folded,check)=>{const context=await browser.newContext({viewport:{width:1280,height:900},locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  if(folded)await context.addInitScript(()=>{try{localStorage.setItem('folded-sections',JSON.stringify(['ready','needs','preparing']))}catch{}});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator(folded?'#section-ready':'#task-a1a1a1a1a1a1a1a1').waitFor();
  try{await check(page)}finally{await context.close()}};
 const focus=page=>page.evaluate(()=>{const a=document.activeElement;return a===document.body?'body':a.id||a.tagName.toLowerCase()});
 const press=async(page,...keys)=>{for(const k of keys){await page.keyboard.press(k);await page.waitForTimeout(60)}};
 const ring=page=>page.evaluate(()=>{const a=document.activeElement,s=getComputedStyle(a);return s.outlineStyle!=='none'&&parseFloat(s.outlineWidth)>0||s.boxShadow!=='none'});

 // Every list open: the first to-do has focus and the ring, J/K and ↓ ↑ walk the to-dos and the heads
 await run(false,async page=>{
  await page.waitForFunction(()=>document.activeElement?.id==='task-a1a1a1a1a1a1a1a1');
  assert.ok(await ring(page),'the first to-do shows the ring');
  if(process.env.SHOT_DIR)await page.screenshot({path:process.env.SHOT_DIR+'/keys-landing.png'});
  await press(page,'j');assert.equal(await focus(page),'task-a2a2a2a2a2a2a2a2');
  await press(page,'ArrowDown');assert.equal(await focus(page),'section-needs','a list head is a stop');
  await press(page,'ArrowDown');assert.equal(await focus(page),'task-b1b1b1b1b1b1b1b1');
  await press(page,'ArrowUp','k');assert.equal(await focus(page),'task-a2a2a2a2a2a2a2a2');
  // Coming back later is folded: → opens it, ↓ goes in, ← on the head folds it again
  await press(page,'j','j','j');assert.equal(await focus(page),'later-head');
  assert.equal(await page.locator('#later-list').evaluate(d=>d.open),false);
  await press(page,'ArrowRight');assert.equal(await page.locator('#later-list').evaluate(d=>d.open),true);
  await press(page,'ArrowDown');assert.equal(await focus(page),'task-c1c1c1c1c1c1c1c1');
  await press(page,'ArrowUp','ArrowLeft');assert.equal(await page.locator('#later-list').evaluate(d=>d.open),false);assert.equal(await focus(page),'later-head');
  // Enter on a to-do opens its chat with the box focused; Esc with words leaves the box, the next Esc closes the chat
  await press(page,'k');assert.equal(await focus(page),'task-b1b1b1b1b1b1b1b1');
  await press(page,'Enter');await page.locator('#chat-input').waitFor();
  await page.waitForFunction(()=>document.activeElement?.id==='chat-input');
  await page.keyboard.type('half a thought');await press(page,'Escape');
  assert.equal(await focus(page),'body');assert.ok(await page.locator('#chat-input').isVisible(),'still in the chat');
  await press(page,'Escape');await page.locator('#chat-input').waitFor({state:'detached'});
  await page.waitForFunction(()=>document.activeElement?.id==='task-b1b1b1b1b1b1b1b1');
  assert.ok(await ring(page),'back on the to-do, with the ring');
  // What was typed is still there when the chat opens again (kept on the device); with an empty box one Esc closes the chat
  await press(page,'Enter');await page.waitForFunction(()=>document.activeElement?.id==='chat-input');
  await page.waitForFunction(()=>document.querySelector('#chat-input')?.value==='half a thought');
  await page.fill('#chat-input','');await press(page,'Escape');await page.waitForFunction(()=>document.activeElement?.id==='task-b1b1b1b1b1b1b1b1');
  // New to-do (N), the shortcut sheet (?) and the palette (Ctrl K) close on Esc and give focus back
  await press(page,'n');await page.locator('#new-card[open]').waitFor();assert.equal(await focus(page),'nc-text');
  await press(page,'Escape');await page.locator('#new-card').waitFor({state:'hidden'});assert.equal(await focus(page),'task-b1b1b1b1b1b1b1b1');
  await press(page,'Shift+?');await page.locator('#keys-sheet[open]').waitFor();
  const sheet=await page.locator('#keys-sheet').innerText();
  for(const s of ['Close a chat or dialog','Open a folded list','Fold it again','↓','↑'])assert.ok(sheet.includes(s),'the sheet lists '+s);
  assert.deepEqual(await page.locator('#keys-sheet p').filter({hasText:/^New to-do/}).locator('kbd').allInnerTexts(),['N'],'New to-do is N in the sheet');
  assert.equal(await page.locator('#keys-sheet p').filter({hasText:/^Talk/}).count(),0,'no Talk in the sheet while this Machine can’t talk live');
  await press(page,'Escape');await page.locator('#keys-sheet').waitFor({state:'hidden'});
  // Where Talk works, the sheet lists it under General as T, not on the Calendar (there T is Today)
  await page.evaluate(()=>{talkInfo.ready=true;talkInfo.at=Date.now()});assert.ok(await page.evaluate(()=>talkOk()),'Talk is available here');
  await press(page,'Shift+?');await page.locator('#keys-sheet[open]').waitFor();
  const keysOf=label=>page.locator('#keys-sheet p').filter({has:page.locator('span:first-child',{hasText:new RegExp('^'+label.replace(/[()]/g,'\\$&')+'$')})}).locator('kbd').allInnerTexts();
  assert.deepEqual(await keysOf('Talk (not on the Calendar)'),['T']);assert.deepEqual(await keysOf('Today'),['T']);
  assert.ok(await page.locator('#keys-sheet h3',{hasText:'General'}).locator('xpath=..').getByText('Talk (not on the Calendar)').isVisible(),'Talk sits in General');
  if(process.env.SHOT_DIR)await page.screenshot({path:process.env.SHOT_DIR+'/keys-sheet.png'});
  await press(page,'Escape');await page.locator('#keys-sheet').waitFor({state:'hidden'});assert.equal(await focus(page),'task-b1b1b1b1b1b1b1b1');
  await press(page,'Control+k');await page.locator('#palette[open]').waitFor();
  await press(page,'Escape');await page.locator('#palette').waitFor({state:'hidden'});assert.equal(await focus(page),'task-b1b1b1b1b1b1b1b1');
  // Another page and back: Suggestions lands on its first to-do again
  await press(page,'g','e');await page.locator('#events').waitFor();
  await press(page,'g','s');await page.waitForFunction(()=>document.activeElement?.id==='task-a1a1a1a1a1a1a1a1');
  // Tab into a to-do's buttons: the ring follows, and ↓ there doesn't take over
  await press(page,'Tab');assert.ok(await ring(page),'a button shows the ring');
  const btn=await focus(page);await press(page,'ArrowDown');assert.equal(await focus(page),btn);
 });

 // Everything folded (what the owner saw): the first list head has focus, Enter opens it, ↓ goes to its first to-do
 await run(true,async page=>{
  await page.waitForFunction(()=>document.activeElement?.id==='section-ready');
  assert.ok(await ring(page),'the head shows the ring');
  if(process.env.SHOT_DIR)await page.screenshot({path:process.env.SHOT_DIR+'/keys-folded.png'});
  assert.equal(await page.locator('#suggestions article.card:visible').count(),0);
  await press(page,'j');assert.equal(await focus(page),'section-needs');
  await press(page,'k','Enter');await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
  assert.equal(await focus(page),'section-ready','the head keeps focus after it opens');
  await press(page,'ArrowDown');assert.equal(await focus(page),'task-a1a1a1a1a1a1a1a1');
  await press(page,'ArrowUp','ArrowLeft');await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor({state:'detached'});assert.equal(await focus(page),'section-ready');
  // A to-do in Coming back later (the owner's page: all clear, one snoozed): open the list, its to-do, its chat. One Esc
  // in the empty box closes the chat, and the list is still open with focus back on that to-do, not on the page.
  for(let i=0;i<6&&await focus(page)!=='later-head';i++)await press(page,'j');assert.equal(await focus(page),'later-head');
  await press(page,'Enter');assert.equal(await page.locator('#later-list').evaluate(d=>d.open),true);
  await press(page,'ArrowDown');assert.equal(await focus(page),'task-c1c1c1c1c1c1c1c1');
  await press(page,'Enter');await page.waitForFunction(()=>document.activeElement?.id==='chat-input');
  assert.equal(await page.locator('#later-list').count(),0,'the chat stands in for the lists');
  await press(page,'Escape');await page.locator('#chat-input').waitFor({state:'detached'});
  await page.waitForFunction(()=>document.activeElement?.id==='task-c1c1c1c1c1c1c1c1');
  assert.equal(await page.locator('#later-list').evaluate(d=>d.open),true,'Coming back later stays open');
  assert.ok(await ring(page),'back on the to-do, with the ring');
  if(process.env.SHOT_DIR)await page.screenshot({path:process.env.SHOT_DIR+'/keys-later-esc.png'});
  // With words in the box: the first Esc leaves the box (the chat stays), the next closes it, same landing
  await press(page,'Enter');await page.waitForFunction(()=>document.activeElement?.id==='chat-input');
  await page.keyboard.type('half a thought');await press(page,'Escape');
  assert.equal(await focus(page),'body');assert.ok(await page.locator('#chat-input').isVisible(),'still in the chat');
  await press(page,'Escape');await page.waitForFunction(()=>document.activeElement?.id==='task-c1c1c1c1c1c1c1c1');
  assert.equal(await page.locator('#later-list').evaluate(d=>d.open),true);
 });
 assert.deepEqual(actions.filter(a=>/confirm|send|decide/.test(a)),[],'nothing sent or decided from a key');
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('keyboard walk ok');
