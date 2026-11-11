import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// There is no Preparing list: a to-do the Machine works on sits in For you with a Preparing… chip, among the Prepared
// and Needs you ones. It keeps its place in the list when a run starts (Do it on a Needs you one, Ask for changes on a
// Prepared one, a first run prepared ahead) and when it ends (Prepared, or stuck and Needs you), on a refresh and after
// a reload: the order reads only the to-do's own fields (due, created_at, weight), never what the page saw before.
// No Preparing tile, sidebar group or header count. Made-up data.
// SHOTS=<folder> saves the list at 1440x900 and 390x844, light and dark, mid-run (PAGE=<another dashboard.html> for a before).
const dashboard=await dashboardPage(process.env.PAGE);
const NOW=Date.UTC(2026,10,5,10,0,0),h=n=>new Date(NOW-n*3600e3).toISOString(),day=n=>new Date(NOW+n*864e5).toISOString().slice(0,10);
const card=(id,title,status,created_at,more={})=>({id:id.repeat(16).slice(0,16),title,body:'Made-up to-do.',status,scope:'work',event_ids:[],created_at,...more});
const running={preparation_status:'running',preparation_started_at:h(0.02)};
// Each stage is what the Machine says at that moment: before, while preparing, after.
const STAGES={
 before:{d:['pending'],a:['prepared'],n:['accepted',{early:1,...running}],s:['accepted',{early:1,...running}]},
 during:{d:['accepted',running],a:['instructions',running],n:['accepted',{early:1,...running}],s:['accepted',{early:1,...running}]},
 after:{d:['prepared'],a:['prepared'],n:['prepared',{early:1}],s:['accepted',{early:1,preparation_status:'blocked',preparation_reason:'Which address should it go to?'}]}};
let stage='before';
const cards=()=>{const st=STAGES[stage],c=(k,title,at,more={})=>card(k,title,st[k][0],at,{...more,...(st[k][1]||{})});return [
 card('e','Confirm the dentist','prepared',h(26),{due:day(1)}),          // due tomorrow: on top
 c('n','Plan the team offsite',h(1)),                                       // the newest: prepared ahead, its first run
 card('i','Approve the new logo','pending',h(2)),
 c('a','Reply about the pilot',h(3)),                                      // Ask for changes
 card('c','Send the venue the count','prepared',h(4)),
 c('d','Pick a date for the board call',h(5)),                              // Do it on a Needs you one
 c('s','Book the hotel',h(6)),                                              // its first run gets stuck
 card('b','Book the train','prepared',h(24*3))]};
const state=()=>({suggestions:cards(),promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){readFile(new URL('../'+(url.pathname.startsWith('/brand/fonts/')?url.pathname.slice(1):'brand/app-icon-192.png'),import.meta.url)).then(b=>{res.setHeader('Content-Type',url.pathname.endsWith('.woff2')?'font/woff2':'image/png');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,errors=[],shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const id=c=>'task-'+c.repeat(16).slice(0,16);
const ORDER=['e','n','i','a','c','d','s','b'].map(id);  // due soon, then newest first, whatever each one's chip says
const list=page=>page.locator('#suggestions article[id^="task-"]').evaluateAll(a=>a.map(x=>x.id));
const chipOf=(page,c)=>page.locator('#'+id(c)+' .card-badges .chip').first().textContent();
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){
  stage='before';
  const context=await browser.newContext({viewport:{width,height},timezoneId:'Europe/Brussels',locale:'en-US'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));await page.clock.setFixedTime(NOW);
  const load=async()=>{await page.goto(base+'/');await page.locator('#section-foryou').waitFor()};
  await load();
  for(const s of ['before','during','after']){
   stage=s;await page.evaluate(()=>refresh());await page.waitForTimeout(100);
   assert.deepEqual(await list(page),ORDER,s+': the same place on a refresh');
   await load();
   assert.deepEqual(await list(page),ORDER,s+': the same place after a reload');
   if(s==='during'){
    for(const c of ['d','a','n','s'])assert.equal(await chipOf(page,c),'Preparing…',c+' says Preparing…');
    assert.equal(await chipOf(page,'i'),'Needs you');assert.equal(await chipOf(page,'c'),'Prepared');
    if(shots)for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});await page.screenshot({path:`${shots}/list-${width}-${scheme}.png`})}
    await page.emulateMedia({colorScheme:'light'});
   }
  }
  assert.equal(await page.locator('#section-preparing').count(),0,'no Preparing list');
  assert.equal(await page.locator('#suggestion-stats [data-fold-tile="preparing"]').count(),0,'no Preparing tile');
  assert.equal(await page.locator('#section-foryou .count').textContent(),String(ORDER.length));
  if(width===1440){
   assert.equal(await page.locator('#side-cards [data-side-fold="preparing"]').count(),0,'no Preparing group in the sidebar');
   stage='during';await load();
   const side=await page.locator('#side-cards a[href^="#chat="]').evaluateAll(a=>a.map(x=>'task-'+x.getAttribute('href').slice(6)));
   assert.deepEqual(side,ORDER,'the sidebar in the same order');
   assert.ok(!/preparing/i.test(await page.locator('#page-head').textContent()),'the header counts For you only');
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('preparing in place ok');
}finally{await browser?.close();server.close()}
