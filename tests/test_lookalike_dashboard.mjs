import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Lookalike senders (lookalike.py): a to-do about a message from a domain that only looks like one the owner deals
// with says so plainly under its body: "This isn’t Sam Lee. It came from acme-corp.example, not acmecorp.example."
// With nobody on record by that name, it names the domains only. Someone genuine: no line. Also in Dutch.
// SHOTS=<folder> saves the to-dos at 390x844 and 1440x900, light and dark.
const dashboard=await dashboardPage();
const cats={};for(const l of ['en','nl'])cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const now=new Date().toISOString();
const like=(name,address,sender)=>({from:'acme-corp.example',domain:'acmecorp.example',name,node:name?'email:sam@acmecorp.example':null,address,sender});
const cards=[
 {id:'l1',title:'Check the new bank details with Sam',body:'Sam says the invoices now go to a new account.',status:'pending',scope:'work',created_at:now,event_ids:[1],
  // As the server sends it (views.py, graph.card_people): their own address in the source line and as their name
  source_line:'Source: email from sam@acme-corp.example · Wed 11 Nov',people:[{id:'email:sam@acme-corp.example',name:'sam@acme-corp.example',
   lookalike:like('Sam Lee','sam@acmecorp.example','sam@acme-corp.example')}]},
 {id:'l2',title:'Answer Kai about the order',body:'Kai asks to confirm the order today.',status:'pending',scope:'work',created_at:now,event_ids:[2],
  source_line:'Source: email from kai@acme-corp.example · Wed 11 Nov',people:[{id:'email:kai@acme-corp.example',name:'kai@acme-corp.example',
   lookalike:like(null,null,'kai@acme-corp.example')}]},
 {id:'l3',title:'Reply to Noor',body:'Noor asked about the plan.',status:'pending',scope:'work',created_at:now,event_ids:[3],
  source_line:'Source: email from Noor · Tue 10 Nov',people:[{id:'email:noor@acmecorp.example',name:'Noor'}]}];
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
 page.on('pageerror',e=>errors.push(e.message));await page.goto(base+'/');await page.locator('#task-l1').waitFor();
 if(language==='nl')await page.waitForFunction(()=>document.documentElement.lang==='nl');
 return [context,page]};
const line=(page,id)=>page.locator(`#task-${id} .note.lookalike`).evaluateAll(n=>n.map(x=>x.textContent.replace(/\s+/g,' ').replace(/‑/g,'-').trim()));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  const [context,page]=await open({width,height,scheme});
  assert.deepEqual(await line(page,'l1'),['This isn’t Sam Lee. It came from acme-corp.example, not acmecorp.example.']);
  assert.deepEqual(await line(page,'l2'),['Lookalike address: this came from acme-corp.example, not acmecorp.example.']);
  assert.deepEqual(await line(page,'l3'),[],'someone genuine: no line');
  // The chip and the source line: their own address, never the contact's name, picture or page
  for(const [id,address] of [['l1','sam@acme-corp.example'],['l2','kai@acme-corp.example']]){
   assert.deepEqual(await page.locator(`#task-${id} .chip.who`).allInnerTexts(),[address]);
   assert.equal(await page.locator(`#task-${id} a.chip.who, #task-${id} .chip.who .chip-av`).count(),0,'no link, no picture');
   const text=await page.locator('#task-'+id).innerText();
   assert.match(text,new RegExp('from '+address.replace(/[.]/g,'\\.'),'i'));
   assert.doesNotMatch(text.replace(/This isn’t Sam Lee\./,''),/Sam Lee|Kai Moss/,'the borrowed name shows only in the warning');
  }
  assert.equal(await page.locator('#task-l3 a.chip.who').count(),1,'someone genuine keeps their chip');
  const chipFits=await page.locator('#task-l1 .chip.who').evaluate(n=>n.getBoundingClientRect().right<=n.closest('.card').getBoundingClientRect().right+1);
  assert.ok(chipFits,'the address chip fits at '+width);
  const order=await page.locator('#task-l1').evaluate(c=>{const y=s=>c.querySelector(s)?.getBoundingClientRect().top??-1;return [y('.body'),y('.note.lookalike')]});
  assert.ok(order[0]<order[1],'under the body: '+order);
  const fits=await page.locator('#task-l1 .note.lookalike').evaluate(n=>n.getBoundingClientRect().right<=n.closest('.card').getBoundingClientRect().right+1);
  assert.ok(fits,'inside the to-do at '+width);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'no sideways scroll at '+width);
  if(shots)for(const id of ['l1','l2'])await page.locator('#task-'+id).screenshot({path:`${shots}/lookalike-${id}-${width}-${scheme}.png`});
  await context.close();
 }
 language='nl';
 {const [context,page]=await open({width:390,height:844});
  assert.deepEqual(await line(page,'l1'),['Dit is niet Sam Lee. Het kwam van acme-corp.example, niet van acmecorp.example.']);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('lookalike ok');
}finally{await browser?.close();server.close()}
