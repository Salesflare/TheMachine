import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The open lists' order (openOrder): a to-do overdue or due by tomorrow first, then the rest newest first by the time
// each one shows (created_at), whatever its people weight or a deadline weeks away. Same-moment to-dos (one review)
// go by weight. For you mixes prepared and needs-you to-dos: what is due soon first whichever it is, then the prepared
// ones, then the ones that need a decision. The sidebar lists them in the same order. Made-up data.
// SHOTS=<folder> saves screenshots at 1440x900 and 390x844 (before the checks, so a page without the fix can be shot
// too: PAGE=<another dashboard.html>).
const dashboard=await dashboardPage(process.env.PAGE);
const NOW=Date.UTC(2026,10,5,10,0,0),h=n=>new Date(NOW-n*3600e3).toISOString(),day=n=>new Date(NOW+n*864e5).toISOString().slice(0,10);
const card=(id,title,status,created_at,more={})=>({id:id.repeat(16).slice(0,16),title,body:'Made-up to-do.',status,scope:'work',event_ids:[],created_at,...more});
const cards=[
 card('a','Send the venue the final count','prepared',h(24*13),{due:day(-13),weight:13.5}),  // overdue: on top
 card('b','Book the train for the offsite','prepared',h(24*9),{weight:22.9}),                 // old, close people: no longer above newer ones
 card('c','Reply to Sam about the pilot','prepared',h(2),{weight:0}),                          // the newest
 card('d','Answer the supplier about pallets','prepared',h(24*3),{due:day(90),weight:0}),      // a deadline months away: by its time
 card('e','Confirm the dentist','prepared',h(26),{due:day(1),weight:0}),                       // due tomorrow: on top
 card('f','Share the slides with Robin','prepared',h(5),{weight:1}),                           // same review as g
 card('g','Thank Alex for the intro','prepared',h(5),{weight:9}),
 card('h','Pick a date for the board call','pending',h(24*6),{weight:20}),
 card('i','Approve the new logo','pending',h(1),{weight:0}),
 card('j','Sign the lease renewal','pending',h(48),{due:day(-1),weight:0})];                // overdue, needs a decision: with e and a
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){readFile(new URL('../'+(url.pathname.startsWith('/brand/fonts/')?url.pathname.slice(1):'brand/app-icon-192.png'),import.meta.url)).then(b=>{res.setHeader('Content-Type',url.pathname.endsWith('.woff2')?'font/woff2':'image/png');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,errors=[],shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const id=c=>'task-'+c.repeat(16).slice(0,16);
const FOR_YOU=['e','j','a','c','g','f','d','b','i','h'].map(id);
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){
  const context=await browser.newContext({viewport:{width,height},timezoneId:'Europe/Brussels',locale:'en-US'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));await page.clock.setFixedTime(NOW);await page.goto(base+'/');
  await page.locator('#section-foryou').waitFor();
  if(shots){await page.screenshot({path:`${shots}/order-${width}x${height}.png`});if(width===390)await page.screenshot({path:`${shots}/order-${width}x${height}-full.png`,fullPage:true})}
  const list=await page.locator('#suggestions article[id^="task-"]').evaluateAll(a=>a.map(x=>x.id));
  assert.deepEqual(list,FOR_YOU,'due soon first, then prepared, then the rest; each newest first, a tie by weight');
  if(width===1440){
   const side=await page.locator('#side-cards a[href^="#chat="]').evaluateAll(a=>a.map(x=>'task-'+x.getAttribute('href').slice(6)));
   assert.deepEqual(side,FOR_YOU.slice(0,8),'the sidebar in the same order (its first 8)');
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('open order ok');
}finally{await browser?.close();server.close()}
