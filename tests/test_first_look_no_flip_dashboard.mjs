import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A fresh hosted signup while ChatGPT connects (2026-11-04): the screen went "Taking a first look… 0 of 102 signals",
// then back to "Connecting ChatGPT…" the same minute, and the count's total went 82, then 102. Once the first look
// showed on this device it never goes back to Connecting, and its total only grows. No "Nothing is sent." on these
// empty states. Made-up fixtures, nothing sent.
const dashboard=await dashboardPage(),shots=process.env.FIRST_LOOK_SHOTS;
const now=new Date().toISOString(),manage='https://control.example/setup';
const connecting={look:{state:'waiting',why:'model',days:7,waiting:102},ai:{name:'ChatGPT',since:now},runs:[],dig:null};
let at=connecting,kept=null;
const live=()=>({runs:at.runs,queue:null,first_look:at.look,first_dig:at.dig,ai_connecting:at.ai});
const state=()=>({suggestions:[],promises:[],connectors:[{id:'work',display_name:'Work mail',service:'gmail'}],suggestion_counts:{},decisions:[],analyses:[],
 deliveries:[],review_health:{},review_runs:[],reviews_on:false,reviews_auto:true,manage_url:manage,greeting:{name:'Robin'},review_live:live(),first_look_done:null});
const errors=[];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(kept||state()));return}
 if(url.pathname==='/api/reviews/live'){res.end(JSON.stringify(kept?kept.review_live:live()));return}
 if(shots&&/^\/brand\/[\w.-]+\.(webp|png)$/.test(url.pathname)){readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url)).then(b=>{res.setHeader('Content-Type','image/'+url.pathname.split('.').pop());res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of shots?[[390,844],[1440,900]]:[[390,844]]){
  at=connecting;kept=null;
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const box=page.locator('#suggestions .first-look-empty');
  await page.goto('http://127.0.0.1:'+server.address().port);
  // Connecting: the line under it is only that to-dos show up here
  await box.filter({hasText:'Connecting ChatGPT…'}).waitFor();
  assert.equal(await box.locator('small').innerText(),'To-dos show up here as they come.');
  assert.ok(!/Nothing is sent/.test(await page.locator('#suggestions').innerText()));
  if(shots)await page.screenshot({path:`${shots}/connecting-${width}.png`});
  // The first look starts
  const run={run_id:'q'+width,status:'running',started_at:now,preview:1,auto:1,window_hours:168,planned:20,done_count:0,claimed_count:20,duration_seconds:0,account_ids:['work'],steps:[]};
  at={look:null,ai:{name:'ChatGPT',since:now},runs:[run],dig:{read:0,total:102,todos:0,goal:3,days:7,pace:30}};
  await page.evaluate(async()=>{await refresh()});
  await box.filter({hasText:'Taking a first look at your last 7 days'}).waitFor();
  assert.ok((await box.innerText()).includes('of 102 messages'));
  assert.ok(!/Nothing is sent/.test(await page.locator('#suggestions').innerText()));
  if(shots)await page.screenshot({path:`${shots}/first-look-${width}.png`});
  // A smaller total for a moment: the count keeps its total
  at={...at,dig:{...at.dig,total:82}};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForTimeout(1200);
  assert.ok((await box.innerText()).includes('of 102 messages'),await box.innerText());
  // Back to the connecting state for a moment (a restart as reviews turn on): still the first look, not Connecting
  at=connecting;
  await page.evaluate(async()=>{await refresh()});
  await page.waitForTimeout(300);
  assert.ok((await box.innerText()).includes('Taking a first look at your last 7 days'),await box.innerText());
  assert.ok(!(await page.locator('#suggestions').innerText()).includes('Connecting ChatGPT'));
  // A reload that draws an older copy first: the same
  kept=state();await page.reload();
  await box.waitFor();await page.waitForTimeout(300);
  assert.ok((await box.innerText()).includes('Taking a first look at your last 7 days'),await box.innerText());
  if(shots)await page.screenshot({path:`${shots}/after-flip-${width}.png`});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
