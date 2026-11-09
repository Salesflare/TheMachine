import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The first look's progress (review_live.first_dig): one count over the week of what its batches saved (never a guess
// ahead of that), a line that names the batch in hand, a bar that moves while the batch reads (not still, then all at
// its end), all of it up between batches instead of the sleepy All clear, and an ending with what it read. 2026-11-04: a small mailbox showed "0 of 20 signals", then "Nothing to report" while it still dug.
// Made-up fixtures, nothing sent.
const dashboard=await dashboardPage(),shots=process.env.FIRST_LOOK_SHOTS;
const now=new Date().toISOString();
const quick=id=>({run_id:id,status:'running',started_at:now,preview:0,auto:1,window_hours:168,planned:20,done_count:0,claimed_count:20,duration_seconds:0,account_ids:['work'],steps:[]});
let run=null,dig={read:0,total:64,todos:0,goal:3,days:7,pace:1},done=null;
const live=()=>({runs:run?[run]:[],queue:null,first_look:null,first_dig:dig});
const state=()=>({suggestions:[],promises:[],connectors:[{id:'work',display_name:'Work mail',service:'outlook'}],
 suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],reviews_on:true,greeting:{name:'Robin'},
 review_live:live(),first_look_done:done});
const errors=[],line=page=>page.locator('#suggestions .fl-count').innerText();
const bar=page=>page.evaluate(()=>{const b=document.querySelector('#suggestions .fl-bar');return [parseFloat(b.firstChild.style.width)||0,+b.getAttribute('aria-valuenow')]});
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
  run=quick('r'+width);dig={read:0,total:64,todos:0,goal:3,days:7,pace:1};done=null;
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#suggestions .first-look-empty .fl-count').waitFor();
  // The first batch: the line names it over the whole week, the number is what was read (nothing yet), the bar moves
  assert.equal(await line(page),'Reading the first 20 of 64 messages…');
  const [a,read]=await bar(page);
  // Nothing got focus by itself: Done / dismissed has no ring on a page nobody pressed a key on yet
  const ringless=()=>page.evaluate(()=>!document.querySelector('#suggestions .kb-on')&&document.activeElement?.id!=='finished-head');
  assert.ok(await ringless(),'no focus on Done / dismissed');
  assert.equal(read,0);
  await page.waitForFunction(w=>parseFloat(document.querySelector('#suggestions .fl-bar i')?.style.width)>w,a,{timeout:8000});
  const [b,still]=await bar(page);assert.ok(b>a&&b<=Math.round(100*19/64),`${b} > ${a}`);
  assert.deepEqual([still,await line(page)],[0,'Reading the first 20 of 64 messages…']);
  assert.ok(!/All clear/.test(await page.locator('#page-head').innerText()));
  if(shots)await page.screenshot({path:`${shots}/reading-${width}.png`});
  // Between batches, nothing found yet: still looking, the count kept, never the sleepy All clear
  run=null;dig={...dig,read:20};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(()=>/Reading on/.test(document.querySelector('#suggestions .first-look-empty')?.textContent||''));
  assert.equal(await line(page),'Reading 20 of 64 messages…');
  const [c,saved]=await bar(page);assert.ok(saved===20&&c>=b,String(c));
  assert.ok((await page.locator('#suggestions').innerText()).includes('Nothing for you yet. Reading on.'));
  assert.equal(await page.locator('#suggestions img.sleepy').count(),0);
  assert.ok(!/All clear/.test(await page.locator('#page-head').innerText()));
  // The next batch (one of the most promising): on from there, never back
  run={run_id:'n'+width,status:'running',started_at:now,preview:0,auto:1,window_hours:null,promising:1,planned:40,done_count:0,claimed_count:40,duration_seconds:3,account_ids:['work'],steps:[]};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForTimeout(1500);
  assert.equal(await line(page),'Read 20 of 64 messages. Reading the next 40…');
  const [d,kept]=await bar(page);assert.ok(kept===20&&d>c&&d<Math.round(100*60/64),String(d));
  if(shots)await page.screenshot({path:`${shots}/digging-${width}.png`});
  // In Connections it is the first look, not "Checking new messages"
  assert.ok((await page.locator('#review-live').innerText()).includes('First look: your last 7 days'));
  // Done, nothing worth a to-do: the ending says what it read, not "Nothing to report"
  run=null;dig=null;done={at:now,days:7,kinds:{email:64},read:{newsletters:50,notifications:14},todos:0,acted:false,next:['calendar','inbox']};
  await page.evaluate(async()=>{await refresh()});
  await page.locator('#suggestions .first-look-end').waitFor();
  assert.equal(await page.locator('#suggestions img.sleepy').count(),0);
  assert.ok(!/Nothing to report/.test(await page.locator('#suggestions').innerText()));
  assert.ok(await ringless(),'no focus on Done / dismissed after the ending');
  if(shots)await page.screenshot({path:`${shots}/ending-${width}.png`});
  // A tap on Done / dismissed, then a redraw: it keeps focus for the keys, but a tap never shows the ring
  await page.locator('#finished-head').click();await page.locator('#finished-head').click();
  await page.evaluate(async()=>{await refresh()});
  await page.waitForTimeout(200);
  assert.equal(await page.locator('#suggestions .kb-on').count(),0);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
