import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do's chat shows its Do it run's browser live, as its card does (peekHTML): where the Open the browser link was,
// a new picture every few seconds at one fixed size, so the thread never moves; a click opens the Browser pane, as the
// link does; gone when the run ends. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage(process.env.DASHBOARD);
const png=async f=>'data:image/png;base64,'+(await readFile(new URL('../brand/'+f,import.meta.url))).toString('base64');
const frames=[await png('app-icon-192.png'),await png('app-icon-maskable-512.png')];
const ID='d1d1d1d1d1d1d1d1',t0=Date.now()-3600000;
let running,peekCalls,base;const actions=[];
const items=()=>[...Array.from({length:14},(_,i)=>i%2?{kind:'reply',text:'Checked the payroll portal step '+i+'. '+'The totals match last month. '.repeat(3),at:t0+i*60000}:{kind:'you',text:'And step '+i+'?',at:t0+i*60000}),
 {kind:'event',text:'Do it',mine:true,at:t0+15*60000},{kind:'steps',steps:['Opening the payroll portal','Using the browser'],at:t0+16*60000}];
const card=()=>({id:ID,title:'Check October payroll is ready to submit',body:'Payroll closes Friday.',status:'accepted',scope:'work',created_at:new Date(t0).toISOString(),event_ids:[1],
 ...(running?{preparation_status:'running',preparation_started_at:new Date(Date.now()-60000).toISOString(),preparation_browser:{link:base+'/viewer#p1',page:'p1'}}:{preparation_status:'ready'})});
const state=()=>({suggestions:[card()],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},browser_embed:'/viewer',browser_link:base+'/viewer'});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/viewer'){res.setHeader('Content-Type','text/html');res.end('<!doctype html><title>Viewer</title><p id="viewer">The browser</p>');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/progress'){res.end(JSON.stringify(running?{status:'running',started_at:new Date(t0).toISOString(),steps:[{title:'Using the browser'}],browser:card().preparation_browser,peek:true}:{status:'ok',steps:[]}));return}
 if(url.pathname==='/api/peek'){peekCalls++;res.end(JSON.stringify(running?{on:true,image:frames[peekCalls%2]}:{on:false}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:running?'running':'ok',active:running,cursor:null,items:items(),live:null}));return}
  if(r.action==='browser_focus'){res.end(JSON.stringify({shown:true}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,tag] of [[1440,900,'desktop'],[390,844,'phone']]){
  const phone=tag==='phone';running=true;peekCalls=0;actions.length=0;
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',hasTouch:phone,isMobile:phone});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#chat='+ID);await page.locator('#chat-input').waitFor();
  // Before the first picture: the link, where the picture comes
  await page.locator('.chat-panel .chat-peek .browser-link').waitFor();
  const thumb=page.locator('.chat-panel .chat-peek .peek-thumb img');
  await thumb.waitFor({timeout:15000});
  assert.equal(await page.locator('.chat-panel .chat-peek .browser-link').count(),0,'the picture takes the link’s place');
  assert.ok(await thumb.isVisible(),'the picture shows in the chat');
  const box=await thumb.boundingBox(),log=await page.locator('#chat-log').boundingBox(),compose=await page.locator('.chat-compose').boundingBox();
  assert.ok(box.y>=log.y+log.height-1&&box.y+box.height<=compose.y+1,'between the thread and the message box');
  assert.ok(box.width>=200&&box.height>=100,'big enough to see: '+JSON.stringify(box));
  // At the end: it stays at the end while the picture comes and refreshes
  const end=()=>page.evaluate(()=>{const l=document.querySelector('#chat-log');return l.scrollTop+l.clientHeight>=l.scrollHeight-2});
  assert.ok(await end(),'at the end after the picture came');
  if(shots)await page.screenshot({path:`${shots}/chat-peek-${tag}.png`});
  // Scrolled up: refreshes (another picture each time) never move the thread
  await page.evaluate(()=>{document.querySelector('#chat-log').scrollTop=300});
  const at=()=>page.evaluate(()=>[document.querySelector('#chat-log').scrollTop,document.querySelector('#chat-log').children[4].getBoundingClientRect().top]);
  const before=await at(),src=await thumb.getAttribute('src'),calls=peekCalls;
  await page.waitForFunction(([s])=>document.querySelector('.chat-peek img')?.getAttribute('src')!==s,[src],{timeout:15000});
  assert.ok(peekCalls>calls,'refreshed from api/peek');
  assert.deepEqual(await at(),before,'a refresh keeps the thread where it was');
  assert.equal(await thumb.boundingBox().then(b=>[b.width,b.height].join()),[box.width,box.height].join(),'one fixed size');
  // A click opens the Browser pane (a phone: the viewer in a tab), as the link does
  if(phone){const [tab]=await Promise.all([context.waitForEvent('page'),page.locator('.chat-peek .peek-thumb').click()]);assert.match(tab.url(),/\/viewer/);await tab.close()}
  else{await page.locator('.chat-peek .peek-thumb').click();await page.locator('#browser-pane:not([hidden])').waitFor();
   assert.match(await page.locator('#bp-frame').getAttribute('src'),/\/viewer/);if(shots)await page.screenshot({path:`${shots}/chat-peek-pane-${tag}.png`});
   await page.locator('#bp-close').click();await page.locator('#browser-pane').waitFor({state:'hidden'});await page.locator('.chat-peek img').waitFor()}
  for(const until=Date.now()+5000;!actions.some(a=>a.action==='browser_focus')&&Date.now()<until;)await page.waitForTimeout(50);
  assert.deepEqual(actions.find(a=>a.action==='browser_focus')?.args,{suggestion_id:ID},'brings the run’s tab to the front');
  // The run ends: the picture goes, as on the card
  running=false;
  await page.locator('.chat-peek').waitFor({state:'detached',timeout:20000});
  if(shots)await page.screenshot({path:`${shots}/chat-peek-ended-${tag}.png`});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('chat peek dashboard ok');
}finally{await browser?.close();server.close()}
