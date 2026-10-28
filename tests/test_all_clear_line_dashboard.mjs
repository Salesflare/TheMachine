import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The line under the sleeping robot on an empty list is one short line in the robot's voice with when it last
// looked ("Peeked at everything 52 minutes ago. All quiet."), no signal or pending counts. The wording changes per
// day, not per render. Before any review it says "I’ll add something when it’s useful.". Also in Dutch.
// SHOTS=<folder> saves screenshots at 1440x900 and 390x844, light and dark.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const cats={};for(const l of ['en','nl'])cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const DAY=Date.UTC(2026,9,28,12,0,0);
let reviewHealth,language;
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){readFile(new URL('../'+(url.pathname.startsWith('/brand/fonts/')?url.pathname.slice(1):'brand/app-icon-192.png'),import.meta.url)).then(b=>{res.setHeader('Content-Type',url.pathname.endsWith('.woff2')?'font/woff2':'image/png');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const cat=/^\/i18n\/(\w\w)\.json$/.exec(url.pathname);if(cat){res.end(cats[cat[1]]||'{}');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],
  review_health:reviewHealth,review_runs:[],locale:{locale:'en-BE',region:'BE',language,language_set:true,clock:'auto',hour12:false,auto_hour12:false,
  date_locale:language==='en'?'en-US':'nl-BE',languages:{en:'English',nl:'Nederlands'},saveable:true}}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const open=async({width=1440,height=900,scheme='light',time=DAY}={})=>{
 const context=await browser.newContext({viewport:{width,height},timezoneId:'UTC',locale:'en-US',colorScheme:scheme}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));await page.clock.setFixedTime(time);await page.goto(base+'/');
 await page.locator('#suggestions .all-clear .poke-line').waitFor();
 if(language==='nl')await page.waitForFunction(()=>document.documentElement.lang==='nl');
 return [context,page]};
const line=page=>page.locator('#suggestions .all-clear .poke-line').innerText();
const EN=[/^Peeked at everything 52 minutes ago\. All quiet\.$/,/^Last snooped around 52 minutes ago\. Nothing to report\.$/,/^Checked in 52 minutes ago\. Back to my nap\.$/];
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // Before any review: the fallback.
 language='en';reviewHealth={total:0,pending:3};
 let [context,page]=await open();
 assert.equal(await line(page),'I’ll add something when it’s useful.');
 await context.close();
 // After one: one short line with the time, no counts; the same line all day, another one the next day.
 reviewHealth={total:10817,pending:9,last_completed:new Date(DAY-52*60000).toISOString()};
 const seen=new Set();
 for(let d=0;d<3;d++){
  [context,page]=await open({time:DAY+d*864e5});reviewHealth.last_completed=new Date(DAY+d*864e5-52*60000).toISOString();
  await page.evaluate(()=>refresh());
  const text=await line(page);
  assert.ok(EN.some(r=>r.test(text)),text);assert.doesNotMatch(text,/signal|10,808|wait/);
  await page.evaluate(()=>refresh());assert.equal(await line(page),text,'same wording within a day');
  seen.add(text);await context.close();
 }
 assert.equal(seen.size,3,'a different line on each of three days');
 // Dutch.
 language='nl';reviewHealth.last_completed=new Date(DAY-52*60000).toISOString();
 [context,page]=await open();
 assert.match(await line(page),/52 minuten geleden/);assert.doesNotMatch(await line(page),/signal|wacht/);
 await context.close();
 if(shots){language='en';
  for(const scheme of ['light','dark'])for(const [width,height] of [[1440,900],[390,844]]){
   [context,page]=await open({width,height,scheme});await page.screenshot({path:`${shots}/all-clear-${width}x${height}-${scheme}.png`});await context.close()}}
 assert.deepEqual(errors,[]);
 console.log('all-clear line ok');
}finally{await browser?.close();server.close()}
