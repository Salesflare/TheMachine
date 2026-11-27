import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Learning, How it's going on a new Machine: until enough to-dos are decided (quality.enough) one empty state with the
// mascot says what the page will show and how far along it is, with no tiles of dashes and no per-source table; the
// Change notes by kind show when there are any. With enough, the four numbers and the per-source table as before.
// All mocked; SHOTS=dir saves screenshots of both states at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const trend={first:null,daily:[],weekly:[]};
const none={confirmed:0,owner_done:0,elsewhere:0,not_needed:0,expired:0,open:0,reopened:0};
const EARLY={cards:4,worth_it:1,dismissed:0,open:3,hit_rate:100,do_it:0,settled:0,done:0,done_rate:null,first_time:0,first_time_rate:null,outcomes:none,sent_as_written:0,sent_edited:0,enough:3,
 previous:{hit_rate:null,done_rate:null,first_time_rate:null,cards:0},notes:{},by_source:{Email:{worth_it:1,dismissed:0,open:3}},trend};
// Three Do it to-dos, two closed (one sent, one dismissed) and one still being prepared: too few closed for a share
const FULL={cards:12,worth_it:6,dismissed:2,open:4,hit_rate:75,do_it:3,settled:2,done:1,done_rate:null,first_time:1,first_time_rate:null,
 outcomes:{...none,confirmed:1,not_needed:1,open:1},sent_as_written:2,sent_edited:1,enough:3,
 previous:{hit_rate:null,done_rate:null,first_time_rate:null,cards:0},notes:{style:1},
 by_source:{Email:{worth_it:6,dismissed:2,open:3},WhatsApp:{worth_it:0,dismissed:0,open:1}},trend};
// Enough closed for shares: 4 of 5 done (one dismissed), one still open, compared with the 30 days before
const DONE={...FULL,do_it:6,settled:5,done:4,done_rate:80,first_time:3,first_time_rate:75,
 outcomes:{...none,confirmed:2,owner_done:1,elsewhere:1,not_needed:1,open:1},previous:{hit_rate:70,done_rate:60,first_time_rate:75,cards:10}};
let quality;
const status=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],quality});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/thinking.webp':'brand/thinking.webp','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('webp')?'image/webp':'font/woff2');try{res.end(await readFile(new URL('../'+asset,import.meta.url)))}catch{res.statusCode=404;res.end()}return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[],shots=process.env.SHOTS;let browser;
const open=async(q,width=1440,height=900,scheme='light')=>{quality=q;
 const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US'}),page=await context.newPage();
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/#learning=going');
 await navClick(page.locator('[data-tab="feedback"]').first());await page.locator('#quality > *').first().waitFor();
 return {context,page,pane:page.locator('#quality')}};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // Early: one empty state with the mascot, what it will show and when, and how far along; no tiles, no source table
 {const {context,page,pane}=await open(EARLY);
  const wait=pane.locator('.q-wait');await wait.waitFor();
  assert.equal(await wait.locator('img.sticker').getAttribute('src'),'brand/thinking.webp');
  const text=await wait.innerText();
  assert.match(text,/Too early for numbers\./);
  assert.match(text,/After 3 decided to-dos, this shows how many were worth it, done, right the first try and sent as is\./);
  assert.match(text,/1 of 3 to-dos decided/);
  const bar=wait.locator('[role="progressbar"]');
  assert.deepEqual([await bar.getAttribute('aria-valuenow'),await bar.getAttribute('aria-valuemax')],['1','3']);
  assert.equal(await pane.locator('.q-tiles').count(),0,'no tiles of dashes');
  assert.doesNotMatch(await pane.innerText(),/Worth it per source|None decided yet|Not enough to-dos yet|–/);
  await context.close()}
 // Nothing at all yet (no report, or no to-do): 0 of 3; the Change notes by kind are real already, so they show
 {const {context,pane}=await open({cards:0,worth_it:0,dismissed:0,by_source:{},previous:{},notes:{unsorted:2},trend,enough:3});
  assert.match(await pane.innerText(),/0 of 3 to-dos decided/);
  assert.match(await pane.innerText(),/What your Change notes asked for\s+2 not sorted/);
  await context.close()}
 {const {context,pane}=await open(undefined);
  assert.match(await pane.innerText(),/Too early for numbers\.[\s\S]*0 of 3 to-dos decided/);
  await context.close()}
 // Enough decided: the page as it was, the four numbers and the per-source table
 {const {context,pane}=await open(FULL);
  await pane.locator('.q-tiles').waitFor();
  assert.equal(await pane.locator('.q-wait').count(),0);
  assert.equal(await pane.locator('.q-tile').count(),4);
  const text=await pane.innerText();
  assert.match(text,/Worth it\s+75%\s+Of 8 to-dos you decided: acted on, not dismissed/);
  // Too few Do it to-dos closed: no share yet, and the one still open is named, never counted as done
  assert.match(text,/Done\s+–\s+Not enough to-dos yet\s+1 still open/);
  assert.match(text,/First try\s+–\s+Not enough to-dos yet/);
  assert.match(text,/Worth it per source[\s\S]*Email\s+6 of 8 75%/);
  await context.close()}
 {const {context,pane}=await open(DONE);
  await pane.locator('.q-tiles').waitFor();
  const text=await pane.innerText();
  assert.match(text,/Done\s+80%\s+Of 5 to-dos closed after Do it: done\s+Up from 60% the 30 days before\s+1 still open/);
  assert.match(text,/First try\s+75%\s+Of 4 to-dos done after Do it: no correction needed\s+Same as the 30 days before/);
  await context.close()}
 // ...and without any source decided (a report with no per-source counts), no table
 {const {context,pane}=await open({...FULL,by_source:{Email:{worth_it:0,dismissed:0,open:2}}});
  await pane.locator('.q-tiles').waitFor();
  assert.doesNotMatch(await pane.innerText(),/Worth it per source/);
  await context.close()}
 // Both states fit a phone and a computer, light and dark, with no sideways scroll
 for(const [width,height] of [[390,844],[1440,900]])for(const scheme of ['light','dark'])for(const [name,q] of [['empty',EARLY],['populated',FULL],['done',DONE]]){
  const {context,page}=await open(q,width,height,scheme);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${name} ${width} ${scheme}: no sideways scroll`);
  if(shots){await page.waitForTimeout(300);await page.screenshot({path:`${shots}/learning-${name}-${width}-${scheme}.png`})}
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok quality wait dashboard');
}finally{await browser?.close();server.close()}
