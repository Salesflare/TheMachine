import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Go through's end counts as cleared only the to-dos that closed. Do it and Ask for changes start a preparation: the
// end said "3 to-dos cleared" while they were still being prepared. Here one Do it finishes at once (closed), one stays
// preparing and one gets Ask for changes: "1 to-do cleared", "2 to-dos are being prepared." With none closed it never
// says cleared. All made up; nothing is sent. SHOTS=<folder> saves screenshots, light and dark.
const dashboard=await dashboardPage();
const at=h=>new Date(Date.now()-h*36e5).toISOString();
const id=n=>(n+'').padStart(2,'0').repeat(8);
const base=()=>[
 {id:id(1),title:'Renew the parking permit',body:'It runs out at the end of the month.',status:'pending',scope:'personal',created_at:at(1),event_ids:[1]},
 {id:id(2),title:'Book a table for Friday',body:'Four people, around eight.',status:'pending',scope:'personal',created_at:at(2),event_ids:[2]},
 {id:id(3),title:'Order printer paper',body:'The office is almost out.',status:'pending',scope:'work',created_at:at(3),event_ids:[3]}];
let cards,posts,finishes;
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},done_counts:{all:0},clear_pace:45});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:[],next:null,total:0}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({counts:{}}));return}
 if(url.pathname==='/api/events'){res.end('[]');return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body),a=r.args||{};
  if(r.action==='decide'){posts.push([a.suggestion_id,a.choice]);const c=cards.find(x=>x.id===a.suggestion_id);
   // the first Do it finishes at once (closed); the others start a preparation
   Object.assign(c,a.choice==='accept'?(finishes.has(c.id)?{status:'completed',closed_at:new Date().toISOString()}:{status:'accepted'}):{status:'instructions'});
   res.end(JSON.stringify({status:c.status}));return}
  res.end(JSON.stringify(r.action==='card_chat'?{session:true,status:'ok',active:false,cursor:'k1',items:[]}:{}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[1440,900,'light'],[390,844,'dark'],...shots?[[1440,900,'dark'],[390,844,'light']]:[]]){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  const run=page.locator('#clear-run'),go=()=>run.locator('[data-cr="go"]').click();
  const at=n=>page.waitForFunction(n=>document.querySelector('#clear-run .cr-pos')?.textContent===n+' of 3',n);
  const open=async()=>{await page.locator('#section-foryou [data-clear-run]').click();await run.waitFor({state:'visible'})};
  // one Do it that finishes, one that stays preparing, one Ask for changes
  cards=base();posts=[];finishes=new Set([id(1)]);
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+id(1)).waitFor();
  await open();await at(1);await go();
  await at(2);await go();
  await at(3);await run.locator('[data-cr="ask"]').click();await run.locator('#cr-ask').fill('Only the recycled kind.');await run.locator('[data-cr="ask-save"]').click();
  await run.locator('.cr-done').waitFor();
  assert.deepEqual(posts,[[id(1),'accept'],[id(2),'accept'],[id(3),'other']]);
  assert.match(await run.locator('.cr-done').textContent(),/^1 to-do cleared in \d+:\d\d$/);
  assert.equal(await run.locator('.cr-end p:not(.cr-done)').textContent(),'2 to-dos are being prepared.');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  if(shots)await page.screenshot({path:`${shots}/go-through-end-${width}-${scheme}.png`});
  await run.locator('[data-cr="close"]').click();await run.waitFor({state:'hidden'});
  // all still preparing: nothing is cleared, and the end says so plainly
  cards=base();posts=[];finishes=new Set();
  await page.reload();await page.locator('#task-'+id(1)).waitFor();
  await open();await at(1);await go();await at(2);await go();await at(3);await run.locator('[data-cr="skip"]').click();
  await run.locator('.cr-done').waitFor();
  assert.equal(await run.locator('.cr-done').textContent(),'2 to-dos are being prepared.');
  assert.doesNotMatch(await run.innerText(),/cleared/);
  if(shots)await page.screenshot({path:`${shots}/go-through-preparing-${width}-${scheme}.png`});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
