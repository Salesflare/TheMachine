import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
import {callAfter,settled} from './page-calls.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// First-use tips (firstTip): one quiet line under the buttons of the to-do it is about, one at a time. The ready draft's
// tip first; the first open to-do's names its real buttons (Do it differently or Ask for changes, Not needed), which
// work like the buttons themselves. Using a button or × closes the tip on the Machine (tip_done); an existing person
// (first_tips empty) sees none.
const dashboard=await dashboardPage();
const now=new Date().toISOString();let tips=['change','send'];
const cards=[{id:'p1',title:'Reply to Sam about pricing',body:'Sam asked for pricing.',status:'pending',scope:'work',created_at:now,event_ids:[1]},
 {id:'p2',title:'Book the venue',body:'Two options.',status:'pending',scope:'work',created_at:now,event_ids:[2]},
 {id:'r1',title:'Send Noor the contract',body:'Draft ready.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[3],
  next_actions:[{kind:'email',revision:'v1',label:'Send to Noor',to:['noor@example.com'],to_name:'Noor',subject:'Contract',body:'Hi Noor'}]}];
const state=()=>({suggestions:cards,first_tips:tips,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);
  if(b.action==='tip_done'){tips=tips.filter(x=>x!==b.args.tip);res.end(JSON.stringify({first_tips:tips}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,scheme] of [[1100,'light'],[390,'dark']]){
  tips=['change','send'];
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-p1').waitFor();
  const shown=()=>page.locator('.first-tip').evaluateAll(n=>n.map(x=>[x.closest('article').id,x.dataset.tip,x.querySelector('.tip-text').textContent]));
  // The ready draft's tip, alone, under that to-do's buttons
  assert.deepEqual(await shown(),[['task-r1','send','You can edit it before it goes. It only goes out when you press Send.']]);
  assert.ok(await page.locator('#task-r1 .first-tip').evaluate(e=>e.previousElementSibling.classList.contains('actions')));
  // One line on a wide screen, never wider than the page
  if(width>600)assert.ok(await page.locator('#task-r1 .first-tip').evaluate(e=>e.getBoundingClientRect().height<30));
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  // × closes it on the Machine; then the first open to-do in the list gets the other one, with that to-do's own labels
  assert.deepEqual(await callAfter(page,'tip_done',()=>page.locator('#task-r1 .tip-x').click()),{action:'tip_done',args:{tip:'send'}});
  await settled(shown,[['task-r1','change','Not quite right? Ask for changes tells me what to change. Not needed clears it.']]);
  // A list of decisions only: the first one's tip says Do it differently
  cards.unshift(cards.pop());const ready=cards.shift();await page.evaluate(()=>refresh());
  await settled(shown,[['task-p1','change','Not quite right? Do it differently tells me what to change. Not needed clears it.']]);
  cards.push(ready);
  // Its button names work like the buttons: Do it differently opens the editor, and the tip is gone for good
  assert.deepEqual(await callAfter(page,'tip_done',()=>page.locator('#task-p1 .first-tip [data-choice="change"]').click()),{action:'tip_done',args:{tip:'change'}});
  await page.locator('#feedback-p1').waitFor();
  await settled(shown,[]);
  await page.locator('#task-p1 [data-choice="cancel-change"]').click();
  assert.deepEqual(await shown(),[]);
  await page.reload();await page.locator('#task-p1').waitFor();assert.deepEqual(await shown(),[]);
  await context.close();
 }
 // Someone who already used to-dos: no tips anywhere; Review and send, when used first, also closes the send tip
 {tips=[];const context=await browser.newContext({viewport:{width:1100,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-p1').waitFor();
  assert.equal(await page.locator('.first-tip').count(),0);
  tips=['send'];await page.reload();await page.locator('#task-r1 .first-tip').waitFor();
  assert.deepEqual(await callAfter(page,'tip_done',()=>page.locator('#task-r1 [data-smart="v1"]').click()),{action:'tip_done',args:{tip:'send'}});
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('first tips ok');
