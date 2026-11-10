import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do working in the browser keeps its live picture on the card and in its chat between browser steps (the model
// thinking, a command in between, a moment with no new picture): the last picture stays, at the same place and size,
// and never blinks out. It goes once the run is done (ready for review), from both at once. Made-up fixtures only.
// SHOTS=<folder> saves the card and the chat during a gap at 1440 and 390, light and dark.
const dashboard=await dashboardPage();
const png=async f=>'data:image/png;base64,'+(await readFile(new URL('../brand/'+f,import.meta.url))).toString('base64');
const frame=await png('app-icon-192.png');
const ID='e2e2e2e2e2e2e2e2',t0=Date.now()-600000;
let phase='browser',peekCalls=0;
const STEPS={browser:[{title:'Opening the invoicing page'},{title:'Using the browser'}],gap:[{title:'Using the browser'},{title:'Running a command'}]};
const card=()=>({id:ID,title:'Draft the monthly invoices',body:'Three invoices for this month.',scope:'work',created_at:new Date(t0).toISOString(),event_ids:[1],
 ...(phase==='done'?{status:'prepared',preparation_status:'ready',body:'Three invoices are drafted and ready to check.'}:{status:'accepted',preparation_status:'running',preparation_started_at:new Date(Date.now()-60000).toISOString()})});
const state=()=>({suggestions:[card()],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},browser_link:base+'/viewer'});
const items=()=>[{kind:'you',text:'Draft this month’s invoices.',at:t0},{kind:'event',text:'Do it',mine:true,at:t0+60000},{kind:'steps',steps:STEPS[phase==='done'?'gap':phase].map(s=>s.title),at:t0+120000}];
let base;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 // Between browser steps the run still works in its tab (run_tab): peek stays true; the picture may not change
 if(url.pathname==='/api/progress'){res.end(JSON.stringify(phase==='done'?{status:'ready',steps:[]}:{status:'running',started_at:new Date(t0).toISOString(),steps:STEPS[phase],browser:null,peek:true}));return}
 if(url.pathname==='/api/peek'){peekCalls++;res.end(JSON.stringify(phase==='done'?{on:false}:phase==='gap'?{on:true,image:null}:{on:true,image:frame}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:phase==='done'?'ok':'running',active:phase!=='done',cursor:null,items:items(),live:null}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
// Watches the picture in the page every 50 ms: how often it was missing, hidden or swapped for another element
const watch=(page,sel)=>page.evaluate(sel=>{const first=document.querySelector(sel);window.__peek={lost:0,swapped:0,boxes:new Set()};
 window.__peekTimer=setInterval(()=>{const i=document.querySelector(sel),w=window.__peek;if(!i||!i.offsetHeight){w.lost++;return}if(i!==first)w.swapped++;const b=i.getBoundingClientRect();w.boxes.add([b.width,b.height].map(Math.round).join('x'))},50)},sel);
const watched=page=>page.evaluate(()=>{clearInterval(window.__peekTimer);const w=window.__peek;return {lost:w.lost,swapped:w.swapped,boxes:[...w.boxes]}});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,tag] of [[1440,900,'1440'],[390,844,'390']])for(const scheme of ['light','dark']){
  const phone=width<600;phase='browser';
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',colorScheme:scheme,hasTouch:phone,isMobile:phone});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const list=await context.newPage(),chat=await context.newPage();
  for(const p of [list,chat])p.on('pageerror',e=>errors.push(e.message));
  await list.goto(base+'/');await chat.goto(base+'/#chat='+ID);
  const cardImg=`#task-${ID} .prep .peek-thumb img`,chatImg='.chat-panel .chat-peek .peek-thumb img';
  // On a browser step: the picture on the card and in the chat (this run isn't waiting on the browser, so no link first)
  await list.locator(cardImg).waitFor({timeout:20000});await chat.locator(chatImg).waitFor({timeout:20000});
  // The gap: a command after the browser step, and no new picture for a while. Both keep the last one, steady.
  await watch(list,cardImg);await watch(chat,chatImg);
  phase='gap';const calls=peekCalls;
  await list.waitForTimeout(6500);
  assert.ok(peekCalls>calls,'still asked for a picture during the gap');
  for(const [page,what] of [[list,'card'],[chat,'chat']]){const w=await watched(page);
   assert.equal(w.lost,0,what+': the picture never left during the gap');assert.equal(w.swapped,0,what+': the same picture, not redrawn');assert.equal(w.boxes.length,1,what+': one size '+w.boxes)}
  assert.equal(await list.locator(`#task-${ID} .steps`).innerText().then(s=>/Running a command/.test(s)),true,'the card shows the step in between');
  assert.ok(await chat.locator(chatImg).isVisible());
  for(const p of [list,chat])assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  if(shots){await list.locator(`#task-${ID}`).screenshot({path:`${shots}/gap-card-${tag}-${scheme}.png`});await list.screenshot({path:`${shots}/gap-list-${tag}-${scheme}.png`});await chat.screenshot({path:`${shots}/gap-chat-${tag}-${scheme}.png`})}
  // Done with the browser (ready for review): gone from both, and the chat's empty slot leaves no space behind
  phase='done';
  await list.locator(`#task-${ID} .peek-thumb`).waitFor({state:'detached',timeout:20000});
  await chat.locator('.chat-peek .peek-thumb').waitFor({state:'detached',timeout:20000});
  if(shots){await list.screenshot({path:`${shots}/done-list-${tag}-${scheme}.png`});await chat.screenshot({path:`${shots}/done-chat-${tag}-${scheme}.png`})}
  await context.close();
 }
 // A run that never uses the browser: the chat shows nothing for it (its slot takes no room)
 {phase='browser';const context=await browser.newContext({viewport:{width:1440,height:900}});const chat=await context.newPage();chat.on('pageerror',e=>errors.push(e.message));
  await context.route('**/api/peek*',route=>route.fulfill({contentType:'application/json',body:JSON.stringify({on:false})}));
  await context.route('**/api/progress*',route=>route.fulfill({contentType:'application/json',body:JSON.stringify({status:'running',steps:[{title:'Reading your mail'}],browser:null,peek:false})}));
  await chat.goto(base+'/#chat='+ID);await chat.locator('#chat-input').waitFor();await chat.waitForTimeout(5000);
  assert.equal(await chat.locator('.chat-peek .peek-thumb, .chat-peek .browser-link').count(),0);
  assert.equal(await chat.locator('.chat-panel').evaluate(n=>getComputedStyle(n).display),'none','no empty space where a picture would be');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('steady peek dashboard ok');
}finally{await browser?.close();server.close()}
