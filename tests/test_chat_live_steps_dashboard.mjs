import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do chat's turn shows its latest step while it runs, as the to-do's card does while it prepares (api/progress):
// above the typing dots, also on Claude Code, whose reply shows only once the run ends. When the reply lands, the
// steps fold into the run's own line above it and the live line goes. A new turn never shows a step of the one before.
// SHOT_DIR=<folder> also saves screenshots (mid-turn and done, light and dark).
const dashboard=await dashboardPage(process.env.DASHBOARD);
const now=new Date().toISOString(),t0=Date.now()-60000,ID='d1d1d1d1d1d1d1d1';
const card={id:ID,title:'Book the venue for the team day',body:'They asked for a date.',status:'instructions',scope:'work',created_at:now,event_ids:[1],preparation_status:'running'};
const state=()=>({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const asked=[{kind:'source',from:'Sam Lee',via:'email',title:'Team day',text:'Can we do Tuesday instead of Monday?',mine:false,at:t0-5000},
 {kind:'you',text:'Check the calendar and draft a reply',at:t0}];
const done=[{kind:'steps',count:4,steps:[{line:['Checked the calendar'],n:2},{line:['Searched messages'],n:2}],at:t0+1000},
 {kind:'reply',text:'Tuesday is free. Here is a short reply that says so.',at:t0+2000}];
let phase='running',progress=[];const polls=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/progress'){polls.push(url.searchParams.get('id'));
  res.end(JSON.stringify({status:phase==='running'?'running':'prepared',started_at:now,steps:phase==='running'?progress:[],browser:null,peek:false}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);
  if(r.action==='card_chat'){const active=phase!=='done';
   // Claude Code's turn: nothing of the reply streams, so the chat has no live text until the run ends
   res.end(JSON.stringify({session:true,status:active?phase:'prepared',active,cursor:null,items:active?asked:[...asked,...done],live:null}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,tag,scheme] of [[1440,900,'desktop','light'],[390,844,'phone','light'],[1440,900,'desktop','dark'],[390,844,'phone','dark']]){
  phase='running';card.preparation_status='running';progress=[{title:'Checking the calendar',at:now},{title:'Reading the mail',at:now}];polls.length=0;
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',hasTouch:tag==='phone',isMobile:tag==='phone',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const shot=async n=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/${n}-${tag}-${scheme}.png`})};
  await page.goto('http://127.0.0.1:'+server.address().port+'/#chat='+ID);
  await page.locator('#chat-log .chat-live .typing').waitFor();
  // The latest step, as the card says it, above the dots; the dots stay
  const live=page.locator('#chat-log .chat-live .steps li');
  await live.waitFor({timeout:9000});
  assert.deepEqual(await live.allTextContents(),['Reading the mail']);
  assert.ok(polls.includes(ID),'the chat asks for its run\'s progress');
  const order=await page.locator('#chat-log .chat-live').evaluate(n=>[...n.children].map(c=>c.className));
  assert.deepEqual(order,['steps','bubble typing'],order.join());
  assert.equal(await page.locator('#chat-log .chat-steps').count(),0,'nothing folded yet');
  // The line fits the chat: no wider than the log, on a phone too
  const fits=await page.locator('#chat-log .chat-live .steps').evaluate(n=>n.getBoundingClientRect().right<=n.closest('#chat-log').getBoundingClientRect().right+0.5);
  assert.ok(fits,'the step stays inside the chat');
  // A newer step replaces it on the next look
  progress=[...progress,{title:'Opening a page',at:now}];
  await page.locator('#chat-log .chat-live .steps li',{hasText:'Opening a page'}).waitFor({timeout:9000});
  await shot('mid-turn');
  // The reply lands: the live line goes and the run's steps are folded above the reply
  phase='done';card.preparation_status=null;card.status='prepared';
  await page.locator('#chat-log .chat-steps').waitFor({timeout:9000});
  await page.locator('#chat-log .chat-live').waitFor({state:'detached',timeout:9000});
  assert.equal(await page.locator('#chat-log [data-steps]').count(),0);
  await shot('done');
  // A new turn: queued first (no step line), then running without steps yet: nothing of the last run shows
  phase='queued';card.status='instructions';card.preparation_status='queued';progress=[];
  await page.evaluate(()=>{chat={...chat,active:true,status:'queued',cursor:null};paintChat();chatPoll()});
  await page.locator('#chat-log .chat-live .typing').waitFor();
  assert.equal(await page.locator('#chat-log .chat-live .steps').count(),0,'no step line while queued');
  phase='running';card.preparation_status='running';
  await page.locator('#chat-log .chat-live .steps').waitFor({state:'attached',timeout:9000});
  assert.equal(await page.locator('#chat-log .chat-live .steps li').count(),0,'no step from the run before');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('ok - a chat turn shows its latest step while it runs, then folds it with the reply');
}finally{await browser?.close();server.close()}
