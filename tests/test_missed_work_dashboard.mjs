import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Learning, How it's going, Missed to-dos (missed_work.py): the weekly check's one number with its range, the misses to
// check (each opens the message, Real miss or Not a miss), how often the check is right; nothing before the first
// check. All mocked; SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const QUALITY={cards:12,worth_it:9,dismissed:3,open:2,hit_rate:75,do_it:4,first_time_rate:75,finished_rate:100,sent_as_written:3,sent_edited:1,
 previous:{hit_rate:60,first_time_rate:75,finished_rate:null},notes:{},by_source:{Email:{worth_it:8,dismissed:2}},trend:{first:null,daily:[],weekly:[]}};
let missed,posts;
const reset=()=>{posts=[];missed={at:'2026-11-02T08:00:00+00:00',population:2894,sampled:40,flagged:2,raw:{rate:.031,low:0,high:.127},adjusted:{rate:.031,low:0,high:.127},
 precision:1,recall:1,labeled:0,made_up:22,more:0,misses:[
  {event_id:41,channel:'message',area:'Personal',what:'reply',reason:'A partner suggests a meeting and waits for an answer',label:null,url:'https://mail.example/41'},
  {event_id:42,channel:'email',area:'Acme',what:'deadline',reason:'An invoice is due this week',label:'real',url:null}]}};
reset();
const status=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],
 quality:QUALITY,missed_work:missed});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='missed_work_label'){missed={...missed,misses:missed.misses.map(m=>m.event_id===args.event_id?{...m,label:args.label||null}:m)};res.end(JSON.stringify({missed_work:missed}));return}}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[],shots=process.env.SHOTS;let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1280,800],[390,844]])for(const scheme of ['light','dark']){
  reset();
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#learning=going');
  await navClick(page.locator('[data-tab="feedback"]').first());
  const pane=page.locator('#quality');await pane.locator('.mw-list').waitFor();
  assert.match(await pane.locator('h3.q-h').last().textContent(),/Missed to-dos/);
  const tile=pane.locator('.mw-tiles .q-tile');
  assert.match(await tile.textContent(),/Likely missed\s*3%/);
  assert.match(await tile.textContent(),/Of 2,894 messages with no to-do/);
  assert.match(await tile.textContent(),/Between 0% and 13%/);
  assert.equal(await pane.locator('.mw-row').count(),2);
  assert.equal(await pane.locator('.mw-row a').first().getAttribute('href'),'https://mail.example/41');
  assert.equal(await pane.locator('.mw-row').nth(1).locator('a').count(),0);  // no link when the source has none
  assert.equal(await pane.locator('[data-mw-id="42"][data-mw-label="real"]').getAttribute('aria-pressed'),'true');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
  if(scheme==='light'){
   await pane.locator('[data-mw-id="41"][data-mw-label="not"]').click();
   await pane.locator('[data-mw-id="41"][data-mw-label="not"][aria-pressed="true"]').waitFor();
   assert.deepEqual(posts.at(-1),{action:'missed_work_label',args:{event_id:41,label:'not'}});
   await pane.locator('[data-mw-id="42"][data-mw-label="real"]').click();  // pressed again: the label goes
   await pane.locator('[data-mw-id="42"][data-mw-label="real"][aria-pressed="false"]').waitFor();
   assert.deepEqual(posts.at(-1),{action:'missed_work_label',args:{event_id:42,label:''}});
   reset();
  }
  if(shots){await page.evaluate(()=>document.fonts.ready);await page.locator('#learn-pane-going').screenshot({path:`${shots}/missed-work-${width}-${scheme}.png`})}
  await context.close();
 }
 {// before the first check: nothing about it
  missed=null;const context=await browser.newContext({viewport:{width:1280,height:800}}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#learning=going');
  await navClick(page.locator('[data-tab="feedback"]').first());
  await page.locator('#quality .q-tiles').waitFor();
  assert.equal(await page.locator('#quality .mw-tiles').count(),0);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('missed work dashboard ok');
}finally{await browser?.close();server.close()}
