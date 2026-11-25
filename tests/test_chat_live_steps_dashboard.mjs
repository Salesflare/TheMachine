import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do chat's run says its status once while it works. A run whose own steps reach the chat (ChatGPT, API keys,
// Azure: OpenClaw's own runtime) shows them in its "Checked N things", with the dots and "Working on it…" above the
// message box, and no row of its latest step. A run that gives none (Claude Code; the service then sends `step`,
// CardChatApp.card_chat) shows that step above the dots and nothing above the message box, without the conversation
// moving when it comes. A new turn never shows a step of the one before.
// SHOT_DIR=<folder> also saves screenshots (mid-turn and done, light and dark).
const dashboard=await dashboardPage(process.env.DASHBOARD);
const now=new Date().toISOString(),t0=Date.now()-60000,ID='d1d1d1d1d1d1d1d1';
const card={id:ID,title:'Book the venue for the team day',body:'They asked for a date.',status:'instructions',scope:'work',created_at:now,event_ids:[1],preparation_status:'running'};
const state=()=>({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const asked=[{kind:'source',from:'Sam Lee',via:'email',title:'Team day',text:'Can we do Tuesday instead of Monday?',mine:false,at:t0-5000},
 {kind:'you',text:'Check the calendar and draft a reply',at:t0}];
const done=[{kind:'steps',count:4,steps:[{line:['Checked the calendar'],n:2},{line:['Searched messages'],n:2}],at:t0+1000},
 {kind:'reply',text:'Tuesday is free. Here is a short reply that says so.',at:t0+2000}];
const fold=n=>({kind:'steps',count:n,steps:[{text:'Find the booking page',n:1},{text:'Check for a free date',n:1}],at:t0+500});
let phase='running',step=null,own=0,live=null,reads=0;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/progress'){  // the card's Preparing line: never the chat's
  res.end(JSON.stringify({status:phase==='running'?'running':'prepared',started_at:now,steps:[{title:'Working on it',at:now}],browser:null,peek:false}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);
  if(r.action==='card_chat'){reads++;const active=phase!=='done';
   res.end(JSON.stringify({session:true,status:active?phase:'prepared',active,cursor:null,items:!active?[...asked,...done]:own?[...asked,fold(own)]:asked,
    live:active?live:null,step:phase==='running'&&!own?step:null}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,tag,scheme] of [[1440,900,'desktop','light'],[390,844,'phone','light'],[1440,900,'desktop','dark'],[390,844,'phone','dark']]){
  phase='running';card.preparation_status='running';card.status='instructions';step=null;own=0;live=null;
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',hasTouch:tag==='phone',isMobile:tag==='phone',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const shot=async n=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/${n}-${tag}-${scheme}.png`})};
  // The chat read its run again, and painted it: the read after the one that brought it has been asked for
  const readAgain=async()=>{const n=reads;for(let i=0;reads<n+3;i++){assert.ok(i<150,'the chat stopped reading its run');await new Promise(r=>setTimeout(r,100))}};
  const now_=()=>page.evaluate(()=>({row:document.querySelector('#chat-log .chat-live .steps')?.textContent||'',above:document.querySelector('#chat-status').textContent,
   said:document.querySelectorAll('#chat-log [role=status]').length,fold:document.querySelector('#chat-log .chat-steps summary')?.textContent||'',
   you:document.querySelector('#chat-log .chat-msg.you').getBoundingClientRect().top,box:document.querySelector('.chat-box').getBoundingClientRect().top}));
  const until=async(what,row,above)=>{await page.waitForFunction(([row,above])=>(document.querySelector('#chat-log .chat-live .steps')?.textContent||'')===row&&document.querySelector('#chat-status').textContent===above,[row,above],{timeout:9000}).catch(()=>{});
   const s=await now_();assert.deepEqual([s.row,s.above],[row,above],what);return s};
  await page.goto('http://127.0.0.1:'+server.address().port+'/#chat='+ID);
  await page.locator('#chat-log .chat-live .typing').waitFor();
  // Before the first step, on any run: the dots, and the line above the message box
  const start=await until('before the first step','','Working on it…');assert.equal(start.said,1);
  // Its own steps reach the chat (ChatGPT, API keys, Azure): no row, also where the step would read as the line does
  step={title:'Working on it',at:now};own=3;
  await page.locator('#chat-log .chat-steps').waitFor({timeout:9000});
  const gpt=await until('a run that shows its own steps','','Working on it…');
  assert.match(gpt.fold,/Checked 3 things/);assert.equal(gpt.box,start.box);assert.equal(await page.locator('#chat-log [data-steps]').count(),0);
  // Opened and between steps too; and while the answer is written
  await page.locator('#chat-log .chat-steps summary').click();own=12;
  await page.locator('#chat-log .chat-steps summary',{hasText:'Checked 12 things'}).waitFor({timeout:9000});
  assert.equal(await page.locator('#chat-log .chat-steps[open] li').count(),2,'the fold stays open');
  await readAgain();await until('the opened fold, some reads later','','Working on it…');
  await shot('own-steps');
  live={text:'Tuesday is free'};await page.locator('#chat-log .chat-live .bubble',{hasText:'Tuesday is free'}).waitFor({timeout:9000});
  await until('writing the answer','','Working on it…');live=null;
  // A run that shows none of its own (Claude Code): its latest step above the dots, nothing above the message box
  own=0;step=null;await page.locator('#chat-log .chat-steps').waitFor({state:'detached',timeout:9000});await page.locator('#chat-log .chat-live .typing').waitFor();
  const before=await until('no step yet','','Working on it…');
  step={title:'Reading the mail',at:now};
  const row=await until('a step','Reading the mail','');
  assert.ok(Math.abs(row.you-before.you)<1,'the conversation stays where it was: '+(row.you-before.you));assert.equal(row.box,before.box);
  assert.equal(row.said,0,'the step is what a screen reader hears, the dots are not said too');
  assert.equal(await page.locator('#chat-log').getAttribute('aria-live'),'polite');
  const order=await page.locator('#chat-log .chat-live').evaluate(n=>[...n.children].map(c=>c.className));
  assert.deepEqual(order,['steps','bubble typing'],order.join());
  // The line fits the chat: no wider than the log, on a phone too
  const fits=await page.locator('#chat-log .chat-live .steps').evaluate(n=>n.getBoundingClientRect().right<=n.closest('#chat-log').getBoundingClientRect().right+0.5);
  assert.ok(fits,'the step stays inside the chat');
  // A newer step replaces it; one with no name of its own is still said once
  step={title:'Opening a page',at:now};assert.equal((await until('a newer step','Opening a page','')).you,row.you);
  step={title:'Working on it',at:now};await until('a step with no name','Working on it','');
  await shot('mid-turn');
  // The reply lands: the live line goes, and nothing is left above the message box
  phase='done';card.preparation_status=null;card.status='prepared';
  await page.locator('#chat-log .chat-steps').waitFor({timeout:9000});
  await page.locator('#chat-log .chat-live').waitFor({state:'detached',timeout:9000});
  await until('done','','');
  await shot('done');
  // A new turn: queued first, then running without steps yet: nothing of the last run shows
  phase='queued';card.status='instructions';card.preparation_status='queued';step=null;
  await page.evaluate(()=>{chat={...chat,active:true,status:'queued',cursor:null};paintChat();chatPoll()});
  await page.locator('#chat-log .chat-live .typing').waitFor();
  await until('queued','','Working on it…');
  phase='running';card.preparation_status='running';await readAgain();
  await until('no step from the run before','','Working on it…');
  // A read that failed mid-run keeps what is shown, once
  step={title:'Reading the mail',at:now};await until('a step again','Reading the mail','');
  await page.evaluate(()=>{chat={...chat,stale:true};paintChat()});await until('after a failed read','Reading the mail','');
  // Stopped: no status left, in neither place
  phase='done';card.preparation_status='blocked';card.preparation_error='stopped';
  await page.evaluate(()=>{const c=cardOf(chatId);Object.assign(c,{preparation_status:'blocked',preparation_error:'stopped'});chat={...chat,active:false,live:null,cursor:null};paintChat()});
  await until('stopped','','');delete card.preparation_error;
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('ok - a run in the chat says its status once: its own steps, or its latest step where it gives none');
}finally{await browser?.close();server.close()}
