import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Opening or reopening the phone app: the first call often fails (the link or a VPN still waking, a busy Machine's
// gateway timing out) while the Machine is fine. The device's copy then shows quietly and refreshes by itself: no
// "Offline" banner and no "Offline · updated" line for one failed or slow call. "Offline" shows only once it really is:
// the device without a network, or the Machine failing a few calls over several seconds (shell-network.js, netOut).
const raw=await dashboardPage(),sw=await readFile(new URL('../sw.js',import.meta.url),'utf8');
const SCOPE='b2'.repeat(16),iso=new Date().toISOString();
const card=(id,title)=>({id,title,body:'Robin asked for the numbers.',status:'pending',scope:'work',created_at:iso,event_ids:[1]});
let title='Reply to Robin about the plan';
const status=()=>({suggestions:[card('1'.repeat(16),title)],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false},ui_version:'v1'});
const page=()=>raw.replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__',SCOPE);
// What the next api/status calls do: 'drop' (the link breaks mid-answer), 'slow' (a gateway that waits
// 3 s and then times out, 504), 'down' (every call 502); fails counts how many more calls fail that way
let mode='ok',fails=0;
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Cache-Control','no-store');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page());return}
 if(url.pathname==='/sw.js'){res.setHeader('Content-Type','text/javascript');res.end(sw);return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/status'&&mode!=='ok'&&(mode==='down'||fails>0)){fails--;
  if(mode==='drop'){res.writeHead(200,{'Content-Type':'application/json','Content-Length':'4000'});res.write('{"suggestions":[');setTimeout(()=>res.destroy(),50);return}
  if(mode==='slow'){await new Promise(r=>setTimeout(r,3000));res.statusCode=504;res.setHeader('Content-Type','text/html');res.end('<h1>504 Gateway Timeout</h1>');return}
  res.statusCode=502;res.end('{"error":"down"}');return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:SCOPE}));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const until=async(p,fn,arg,label,timeout=15000)=>{try{await p.waitForFunction(fn,arg,{timeout})}catch{throw Error('timed out: '+label)}};
// Every moment the banner or the offline line showed, watched in the page itself (a glimpse counts too)
const watch=p=>p.addInitScript(()=>{window.__alarms=[];const seen=()=>{const b=document.querySelector('#offline-bar'),n=document.querySelector('#stale-note');
  if(b&&!b.hidden)__alarms.push('banner: '+b.textContent);if(n&&!n.hidden)__alarms.push('line: '+n.textContent)};
 new MutationObserver(seen).observe(document,{subtree:true,childList:true,attributes:true,characterData:true})});
const alarms=p=>p.evaluate(()=>{const a=__alarms;window.__alarms=[];return [...new Set(a)]});
// The app goes to the background and comes back (visibilitychange, as Android's WebView sends it)
const resume=p=>p.evaluate(()=>{let hidden=true;Object.defineProperty(document,'hidden',{configurable:true,get:()=>hidden});document.dispatchEvent(new Event('visibilitychange'));
 hidden=false;document.dispatchEvent(new Event('visibilitychange'))});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const tab=await context.newPage();tab.on('pageerror',e=>errors.push(e.message));await watch(tab);
 await tab.goto(base);await tab.locator('#suggestions article[id]').first().waitFor();
 for(let n=0;!(await tab.evaluate(async()=>!!(await localCache.read('status'))));n++){assert.ok(n<150,'the to-dos are kept on the device');await tab.waitForTimeout(100)}
 assert.deepEqual(await alarms(tab),[],'online: nothing alarming');

 // 1. Reopened, the first call's connection breaks: no banner, and the retry a moment later brings the new to-dos
 for(const how of ['drop','slow']){
  mode=how;fails=1;title='Updated by the '+how+' retry';await resume(tab);
  await until(tab,t=>document.querySelector('#suggestions').innerText.includes(t),title,how+': the retry brings the live to-dos',20000);
  assert.deepEqual(await alarms(tab),[],how+': one failed call on resume shows nothing alarming');
  assert.equal(await tab.evaluate(()=>netDown||netOut),false,how+': live again')}

 // 2. Opened from the device's copy (the app was closed), the first call fails: the kept to-dos, quietly, then live
 mode='drop';fails=1;title='Live after a cold start';await tab.reload();await tab.locator('#suggestions article[id]').first().waitFor();
 await until(tab,t=>document.querySelector('#suggestions').innerText.includes(t),title,'cold start: live after the retry',20000);
 assert.deepEqual(await alarms(tab),[],'cold start: nothing alarming');

 // 3. The Machine really away: quiet for the first seconds, then the banner with since when
 mode='down';const t0=Date.now();await resume(tab);
 await tab.waitForTimeout(2500);assert.deepEqual(await alarms(tab),[],'quiet for the first seconds');
 await until(tab,()=>{const b=document.querySelector('#offline-bar');return !b.hidden&&/^Offline\. Showing what was here at \d\d:\d\d\./.test(b.textContent)},null,'the banner once it is really offline',15000);
 const took=Date.now()-t0;assert.ok(took>=3500&&took<12000,`the banner after a few failed calls over several seconds (${took} ms)`);
 mode='ok';await tab.click('#offline-bar [data-net-retry]');
 await until(tab,()=>document.querySelector('#offline-bar').hidden&&document.querySelector('#stale-note').hidden,null,'gone once live again');
 await alarms(tab);

 // 4. The device without a network: said within a couple of seconds
 const t1=Date.now();await context.setOffline(true);
 await until(tab,()=>!document.querySelector('#offline-bar').hidden,null,'device offline: the banner',8000);
 assert.ok(Date.now()-t1<5000,'device offline shows soon');
 await context.setOffline(false);  // the online event refreshes by itself
 await until(tab,()=>document.querySelector('#offline-bar').hidden,null,'back online');

 assert.deepEqual(errors,[]);
 console.log('offline resume dashboard ok');
}finally{await browser?.close();server.close()}
