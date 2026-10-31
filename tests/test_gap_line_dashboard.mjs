import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// What we don't know (gap_note.py): a to-do about someone shows one quiet line when the last word with them is old or
// was the owner's own with no reply, and the channels they may have answered on that aren't synced. The service sends
// `gap` only when it helps; a to-do without it, a snoozed or done one, or one waiting on a handoff shows no line.
// Also in Dutch. SHOTS=<folder> saves screenshots at 1440x900 and 390x844.
const dashboard=await dashboardPage();
const cats={};for(const l of ['en','nl'])cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const now=new Date().toISOString();
const cards=[
 {id:'g1',title:'Prep the call with Ann',body:'Call on Monday at 10. Ann asked about pricing for 40 seats.',status:'prepared',early:1,scope:'work',created_at:now,event_ids:[1],
  people:[{id:'email:ann@client.example',name:'Ann Example'}],gap:{name:'Ann Example',days:12,channel:'email',wrote_last:false,unsynced:[]}},
 {id:'g2',title:'Follow up with Kim about the contract',body:'Kim said they would sign this week.',status:'pending',scope:'work',created_at:now,event_ids:[2],
  people:[{id:'email:kim@corp.example',name:'Kim Lee'}],gap:{name:'Kim Lee',days:5,channel:'email',wrote_last:true,unsynced:['WhatsApp','LinkedIn']}},
 {id:'g3',title:'Answer Noor about the invoice',body:'Noor asked for a copy.',status:'pending',scope:'work',created_at:now,event_ids:[3],people:[{id:'email:noor@x.example',name:'Noor'}]},
 {id:'g4',title:'Check in with Jo',body:'Jo is back next week.',status:'snoozed',snoozed_until:new Date(Date.now()+864e5).toISOString(),scope:'work',created_at:now,event_ids:[4],
  gap:{name:'Jo',days:30,channel:'Slack',wrote_last:false,unsynced:[]}},
 {id:'g5',title:'Thank Sam for the intro',body:'Sent.',status:'completed',scope:'work',created_at:now,event_ids:[5],gap:{name:'Sam',days:20,channel:'email',wrote_last:false,unsynced:[]}}];
let language='en';
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){readFile(new URL('../'+(url.pathname.startsWith('/brand/fonts/')?url.pathname.slice(1):'brand/app-icon-192.png'),import.meta.url)).then(b=>{res.setHeader('Content-Type',url.pathname.endsWith('.woff2')?'font/woff2':'image/png');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const cat=/^\/i18n\/(\w\w)\.json$/.exec(url.pathname);if(cat){res.end(cats[cat[1]]||'{}');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],
  review_health:{},review_runs:[],review_live:{runs:[]},fleet:{on:false,fleets:[]},locale:{locale:'en-BE',region:'BE',language,language_set:true,clock:'auto',hour12:false,auto_hour12:false,
  date_locale:language==='en'?'en-US':'nl-BE',languages:{en:'English',nl:'Nederlands'},saveable:true}}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const open=async({width=1440,height=900,scheme='light'}={})=>{
 const context=await browser.newContext({viewport:{width,height},timezoneId:'UTC',locale:'en-US',colorScheme:scheme}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));await page.goto(base+'/');await page.locator('#task-g1').waitFor();
 if(language==='nl')await page.waitForFunction(()=>document.documentElement.lang==='nl');
 return [context,page]};
const line=(page,id)=>page.locator(`#task-${id} .gap-line`).evaluateAll(n=>n.map(x=>x.textContent.trim()));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){
  const [context,page]=await open({width,height});
  assert.deepEqual(await line(page,'g1'),['Last contact 12 days ago by email; nothing since.']);
  assert.deepEqual(await line(page,'g2'),['Your last message: 5 days ago by email; no reply since. They may have replied on WhatsApp or LinkedIn (not synced).']);
  assert.deepEqual(await line(page,'g3'),[],'no gap: no line');
  // One line, under the body, never wider than the to-do
  const fits=await page.locator('#task-g2 .gap-line').evaluate(n=>n.scrollWidth<=n.clientWidth+1&&n.getBoundingClientRect().right<=n.closest('.card').getBoundingClientRect().right+1);
  assert.ok(fits,'the line wraps inside the to-do at '+width);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'no sideways scroll at '+width);
  if(shots)await page.locator('#task-g2').screenshot({path:`${shots}/gap-line-${width}x${height}.png`});
  if(shots)await page.screenshot({path:`${shots}/gap-page-${width}x${height}.png`});
  await context.close();
 }
 // Snoozed and done ones say nothing, wherever they show
 {const [context,page]=await open();
  await page.evaluate(()=>{state.suggestions.find(s=>s.id==='g2').status='snoozed';render()});
  assert.deepEqual(await line(page,'g2'),[]);await context.close()}
 // Dutch
 language='nl';
 {const [context,page]=await open({width:390,height:844});
  assert.deepEqual(await line(page,'g1'),['Laatste contact 12 dagen geleden via e-mail; niets sindsdien.']);
  assert.deepEqual(await line(page,'g2'),['Je laatste bericht: 5 dagen geleden via e-mail; nog geen antwoord. Misschien hebben ze geantwoord via WhatsApp of LinkedIn (niet gesynchroniseerd).']);
  if(shots)await page.locator('#task-g2').screenshot({path:`${shots}/gap-line-nl-390x844.png`});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('gap line ok');
}finally{await browser?.close();server.close()}
