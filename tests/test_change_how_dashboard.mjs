import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do that isn't prepared yet has Change how in sight, right after its lead (Do it, Prepare), like Ask for changes on a
// ready one; a step only the owner can do keeps it out of sight. The row never runs onto a third line on a phone: when a
// long label (French here) leaves no room, Snooze moves to the top of the … and Change how stays. A wider row takes it back.
// SHOTS=<folder> saves screenshots at 1440x900 and 390x844, light and dark.
const dashboard=await dashboardPage();
const cats={};for(const l of ['en','fr'])cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const now=new Date().toISOString();let language='en';
const cards=[{id:'p1',title:'Reply to Priya about the pricing for forty seats',body:'Priya asked what forty seats would cost per year.',status:'pending',scope:'work',created_at:now,event_ids:[1]},
 {id:'p2',title:'Book a table for the team dinner',body:'Dana suggested Thursday at 19:00.',status:'pending',scope:'work',labels:{accept:'Prepare'},created_at:now,event_ids:[2]},
 {id:'v1',title:'Pick up the parcel at the post office',body:'It waits there until Friday.',status:'pending',scope:'personal',owner_step:1,created_at:now,event_ids:[3]},
 {id:'r1',title:'Send Noor the contract',body:'Draft ready.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[4],
  next_actions:[{kind:'email',revision:'v1',label:'Send to Noor',to:['noor@example.com'],to_name:'Noor',subject:'Contract',body:'Hi Noor, the contract is attached.'}]}];
const server=createServer(async(req,res)=>{for await(const c of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){readFile(new URL('../'+(url.pathname.startsWith('/brand/fonts/')?url.pathname.slice(1):'brand/app-icon-192.png'),import.meta.url)).then(b=>{res.setHeader('Content-Type',url.pathname.endsWith('.woff2')?'font/woff2':'image/png');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const cat=/^\/i18n\/(\w\w)\.json$/.exec(url.pathname);if(cat){res.end(cats[cat[1]]||'{}');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
  locale:{locale:'en-US',region:'US',language,language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English',fr:'Français'},saveable:true}}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const open=async(width,scheme='light')=>{const context=await browser.newContext({viewport:{width,height:width>600?900:844},colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-p1').waitFor();await page.evaluate(()=>document.fonts.ready);return {context,page}};
 // What is in sight in a to-do's row, and on which line each sits (0 is the first)
 const row=(page,id)=>page.locator(`#task-${id} .actions`).evaluate(a=>{const kids=[...a.children].filter(x=>x.matches('button,a.open,.more-actions')&&getComputedStyle(x).display!=='none'),tops=[...new Set(kids.map(x=>Math.round(x.getBoundingClientRect().top)))].sort((p,q)=>p-q);
  return kids.map(x=>(x.tagName==='DETAILS'?'More':x.textContent.trim())+'@'+tops.indexOf(Math.round(x.getBoundingClientRect().top)))});
 const menu=(page,id)=>page.locator(`#task-${id} .more-menu>button`).evaluateAll(n=>n.filter(x=>getComputedStyle(x).display!=='none').map(x=>x.textContent.trim()));
 for(const scheme of ['light','dark'])for(const width of [1440,390]){
  language='en';const {context,page}=await open(width,scheme);
  const line=width>600?0:1;  // on a phone the lead has a row of its own
  assert.deepEqual(await row(page,'p1'),['Do it@0',`Change how@${line}`,`Snooze@${line}`,`More@${line}`]);
  assert.deepEqual(await row(page,'p2'),['Prepare@0',`Change how@${line}`,`Snooze@${line}`,`More@${line}`]);
  assert.deepEqual(await row(page,'r1'),['Review and send to Noor@0',`Ask for changes@${line}`,`Snooze@${line}`,`More@${line}`]);
  assert.ok(!(await row(page,'v1')).some(x=>x.startsWith('Change how')),'a step only the owner can do keeps Change how out of sight');
  assert.ok(!(await menu(page,'p1')).includes('Snooze'),'Snooze is not in the … while it fits in the row');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(shots){await page.screenshot({path:`${shots}/change-how-${width>600?'desktop':'phone'}-${scheme}.png`});await page.locator('#task-p1').screenshot({path:`${shots}/change-how-card-${width>600?'desktop':'phone'}-${scheme}.png`})}
  // Change how opens the editor that asks how to do it instead
  await page.locator('#task-p1 .actions>[data-choice="change"]').click();
  await page.locator('#task-p1').getByText('How should I do it instead?').waitFor();
  await page.locator('#task-p1 [data-choice="cancel-change"]').click();
  await page.locator('#task-p1 .actions>[data-choice="change"]').waitFor();
  await context.close();
 }
 // French on a phone: Faire, then Changer d’approche and the …; Mettre en attente tops the …. On a wide screen it is back in the row.
 for(const scheme of ['light','dark']){
  language='fr';const {context,page}=await open(390,scheme);
  await page.locator('#task-p1 .actions>[data-choice="change"]',{hasText:'Changer d’approche'}).waitFor();
  const fr=async()=>{for(let i=0;i<40&&(await row(page,'p1')).length!==3;i++)await page.waitForTimeout(50);return row(page,'p1')};
  assert.deepEqual(await fr(),['Faire@0','Changer d’approche@1','More@1']);
  for(const id of ['p1','p2','r1'])assert.ok((await row(page,id)).every(x=>/@[01]$/.test(x)),id+' runs onto a third line: '+(await row(page,id)).join(' '));
  assert.equal((await menu(page,'p1'))[0],'Mettre en attente');
  if(shots){await page.screenshot({path:`${shots}/change-how-fr-phone-${scheme}.png`});await page.locator('#task-p1').screenshot({path:`${shots}/change-how-fr-card-phone-${scheme}.png`})}
  // The … one opens the snooze picker for this to-do
  await page.locator('#task-p1 .more-actions>summary').click();
  if(shots)await page.screenshot({path:`${shots}/change-how-fr-menu-phone-${scheme}.png`});
  await page.locator('#task-p1 .more-menu>[data-choice="snooze"]').click();
  assert.equal(await page.locator('#snooze-dialog').evaluate(d=>d.open),true);
  await page.keyboard.press('Escape');
  await page.setViewportSize({width:1440,height:900});
  for(let i=0;i<40&&(await row(page,'p1')).length!==4;i++)await page.waitForTimeout(50);
  assert.deepEqual(await row(page,'p1'),['Faire@0','Changer d’approche@0','Mettre en attente@0','More@0']);
  assert.ok(!(await menu(page,'p1')).includes('Mettre en attente'));
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('change how dashboard ok');
