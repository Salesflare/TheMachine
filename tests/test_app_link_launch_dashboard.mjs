import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A link the installed desktop app catches (the morning summary's Open, #card=<id>&or=chat) shows that to-do, with the
// app closed (it opens with the link) and open (launch_handler focus-existing hands the link to the open page through
// launchQueue). Also: the same link again, any other # link (a chat, a promise), and a release waiting for a quiet
// moment: the update never reloads the page under a link that just came in, and after an update's reload the
// browser's own scroll restore never lands over the linked to-do.
const raw=await dashboardPage();
const now=new Date().toISOString(),id=n=>n.toString(16).padStart(16,'a');
let served='v1',current='v1',staleOnce=null;
// holdOnLoad: the next page load's status waits for release() (a Machine slow to answer right after an update)
let holdOnLoad=false,statusHeld=null,release=()=>{};
const cards=()=>Array.from({length:14},(_,n)=>({id:id(n),title:'Another to-do '+n,body:'Some words. '.repeat(30),status:'pending',scope:'work',created_at:now,event_ids:[n+2]}));
const status=()=>({suggestions:cards(),promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false},ui_version:current});
const hits={page:0};
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');
 if(url.pathname==='/'){hits.page++;if(holdOnLoad){holdOnLoad=false;statusHeld=new Promise(r=>{release=()=>{statusHeld=null;r()}})}const v=staleOnce||served;staleOnce=null;res.setHeader('Content-Type','text/html');res.end(raw.replace('__CSRF__','c'.repeat(64)).replaceAll('__UI_VERSION__',v).replace('__BASE__','/').replace('__CACHE_SCOPE__','s'.repeat(32)));return}
 if(url.pathname==='/api/status'){if(statusHeld)await statusHeld;res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:'s'.repeat(32)}));return}
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:[],next:null,total:0}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',link=n=>base+'#card='+id(n)+'&or=chat';
const errors=[];let browser,page;
// where the page is, for a failure's message
const at=()=>page?.evaluate(()=>JSON.stringify({hash:location.hash,linked:linkedCardId,y:Math.round(scrollY),chat:chatId})).catch(e=>e.message);
const until=async(fn,label,ms=10000)=>{const t=Date.now();while(!(await Promise.resolve().then(fn).catch(()=>false))){if(Date.now()-t>ms)throw Error('timed out: '+label+' '+await at());await new Promise(r=>setTimeout(r,100))}};
// The to-do is the one the link picked out and it is on screen
const shown=(page,n)=>page.evaluate(i=>{const r=document.getElementById('task-'+i)?.getBoundingClientRect();return linkedCardId===i&&!!r&&r.top>=0&&r.bottom<=innerHeight},id(n));
// Chrome hands the launch to the page: the one that opened it first (its own address), later ones as they come
const launch=(page,url)=>page.evaluate(u=>launchQueue.deliver(u),url);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1290,height:900},locale:'en-US',timezoneId:'Europe/Brussels'});
 // launchQueue as Chrome's: launches before setConsumer wait for it; a page opened by a launch gets that launch first
 await context.addInitScript(()=>{const waiting=[location.href];let consumer=null;
  Object.defineProperty(window,'launchQueue',{value:{setConsumer(f){consumer=f;for(const u of waiting.splice(0))f({targetURL:u,files:[]})},deliver(u){consumer?consumer({targetURL:u,files:[]}):waiting.push(u)}}})});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const newPage=async()=>{const p=await context.newPage();p.on('pageerror',e=>errors.push(e.message));return p};

 // 1. Cold: the app opens with the link; the same link again later (after scrolling away) shows it again
 page=await newPage();await page.goto(link(11));
 await until(()=>shown(page,11),'cold: the linked to-do');
 await page.waitForTimeout(1000);await page.evaluate(()=>{scrollTo(0,0);linkedCardId=null});await until(()=>page.evaluate(()=>scrollY===0),'scrolled away');
 await launch(page,link(11));await until(()=>shown(page,11),'the same link again');
 // 2. Warm: other links go where they point; a promise's link passes through as it is
 await launch(page,link(3));await until(()=>shown(page,3),'warm: another to-do');
 await launch(page,base+'#chat='+id(5));await until(()=>page.evaluate(i=>chatId===i,id(5)),'warm: a chat');
 await launch(page,link(12));await until(()=>shown(page,12),'from a chat: the to-do');
 await page.evaluate(()=>{window.__hashes=[];addEventListener('hashchange',e=>__hashes.push(new URL(e.newURL).hash))});
 await launch(page,base+'#promise/7');await until(()=>page.evaluate(()=>__hashes.includes('#promise/7')),'a promise link');
 await page.close();

 // 3. A release waiting in a window in the background: a link that comes in is use, so no reload under it
 page=await newPage();await page.clock.install();await page.goto(base);await page.locator('#task-'+id(0)).waitFor();
 await page.evaluate(()=>{document.hasFocus=()=>false;window.__same=1});await page.clock.fastForward(40e3);
 served=current='v2';await page.evaluate(()=>refresh());
 await launch(page,link(10));await until(()=>shown(page,10),'the to-do, a release waiting');
 await page.clock.fastForward(20e3);await page.evaluate(()=>refresh());await page.clock.runFor(16e3);
 assert.equal(await page.evaluate(()=>window.__same),1,'no reload right after the link');
 assert.ok(await shown(page,10),'the to-do stays on screen');
 // later, left alone in the background, the update loads; a link that comes in while it still loads its to-dos shows its
 // to-do, never the place from before the update put back over it
 holdOnLoad=true;const loaded=page.waitForEvent('load');await page.clock.fastForward(60e3);await page.evaluate(()=>refresh()).catch(()=>{});await page.clock.runFor(16e3);await loaded;
 await page.clock.resume();await launch(page,link(13));await page.waitForTimeout(300);release();
 await page.locator('#task-'+id(0)).waitFor();assert.equal(await page.evaluate(()=>UI_VERSION),'v2');
 await until(()=>shown(page,13),'after the update, a link while it loaded: the to-do');
 await page.waitForTimeout(1500);assert.ok(await shown(page,13),'the place from before the update does not come back over it');
 // and a link once it has loaded still shows its to-do
 await page.evaluate(()=>{scrollTo(0,0);linkedCardId=null});await launch(page,link(12));await until(()=>shown(page,12),'after the update: the to-do');
 await page.waitForTimeout(1500);assert.ok(await shown(page,12),'the browser restoring the old place does not land over it');
 await page.close();

 // 4. Cold with an older copy of the page (the app's cache from before a release): the update loads with the link kept
 page=await newPage();staleOnce='v2';served=current='v3';const pages=hits.page;
 await page.goto(link(11));await until(()=>hits.page===pages+2,'the update loaded');
 await until(()=>page.evaluate(()=>UI_VERSION==='v3'),'the new version runs');
 await until(()=>shown(page,11),'cold, older copy: the linked to-do');
 await page.waitForTimeout(1500);assert.ok(await shown(page,11),'still on screen');
 await page.close();

 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('app link launch dashboard ok');
