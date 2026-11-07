import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A first look whose tries fail: after one failure the line under its bar says it tries again shortly; from the third in
// a row it says the tries keep failing, instead of "Nothing for you yet. Reading on." for hours (2026-10-27: a hosted
// first look failed, and nothing on the dashboard said so). A batch running again shows its progress as usual. Also
// with reviews off, where the first look waits for its retry. Made-up fixtures, nothing sent.
const dashboard=await dashboardPage(),shots=process.env.FIRST_LOOK_FAILING_SHOTS;
const now=new Date().toISOString(),KEEPS='The last tries did not finish. Still trying.',ONCE='The last try did not finish; it tries again shortly.';
let run=null,dig=null,look=null,reviewsOn=true;
const live=()=>({runs:run?[run]:[],queue:null,first_look:look,first_dig:dig});
const state=()=>({suggestions:[],promises:[],connectors:[{id:'work',display_name:'Work mail',service:'gmail'}],
 suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],reviews_on:reviewsOn,
 review_live:live(),first_look_done:null});
const errors=[];
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/reviews/live'){res.end(JSON.stringify(live()));return}
 if(url.pathname==='/api/action'){res.end(JSON.stringify({sources:[]}));return}
 if(shots&&/^\/brand\/[\w.-]+\.(webp|png)$/.test(url.pathname)){readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url)).then(b=>{res.setHeader('Content-Type','image/'+url.pathname.split('.').pop());res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of shots?[[390,844],[1440,900]]:[[390,844]]){
  reviewsOn=true;look=null;run=null;dig={read:20,total:64,todos:0,goal:3,days:7,pace:1,failing:1};
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const empty=()=>page.locator('#suggestions .first-look-empty').innerText();
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#suggestions .first-look-empty .fl-count').waitFor();
  // One failure, between batches: it tries again shortly, the count kept
  assert.ok((await empty()).includes(ONCE),await empty());
  assert.ok(!(await empty()).includes('Reading on'));
  // The third failure in a row: one honest line that the tries keep failing
  dig={...dig,failing:3};await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(k=>document.querySelector('#suggestions .first-look-empty')?.textContent.includes(k),KEEPS);
  assert.ok(!(await empty()).includes(ONCE));
  assert.match(await empty(),/20 of 64 signals/);
  assert.ok(!/All clear/.test(await page.locator('#page-head').innerText()));
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(shots)await page.screenshot({path:`${shots}/failing-${width}.png`});
  // A try running again: its progress, not the failure line
  run={run_id:'n'+width,status:'running',started_at:now,preview:0,auto:1,window_hours:null,promising:1,planned:40,done_count:0,claimed_count:40,duration_seconds:3,account_ids:['work'],steps:[]};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(k=>!document.querySelector('#suggestions .first-look-empty')?.textContent.includes(k),KEEPS);
  // It went well: the usual line again
  run=null;dig={...dig,read:60,failing:0};await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(()=>/Reading on/.test(document.querySelector('#suggestions .first-look-empty')?.textContent||''));
  // Reviews off: the first look waits for its retry; from the third failure the same line, also on Connections
  reviewsOn=false;dig=null;look={state:'waiting',why:'retry',retry_at:new Date(Date.now()+6e5).toISOString(),failing:1,waiting:20,days:7,quick:true,hours:168};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(k=>document.querySelector('#suggestions .first-look-empty')?.textContent.includes(k),ONCE);
  look={...look,failing:4};await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(k=>document.querySelector('#suggestions .first-look-empty')?.textContent.includes(k),KEEPS);
  assert.ok((await page.locator('#review-live').innerText()).includes(KEEPS));
  if(shots)await page.screenshot({path:`${shots}/failing-off-${width}.png`});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('first look failing dashboard ok');
