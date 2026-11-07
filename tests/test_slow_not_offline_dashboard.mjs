import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Slow is not offline (shell-network.js, netSlow). A busy Machine can take 15 to 30 seconds for a call while it is
// reachable the whole time. A call that waited long and then broke, or a gateway's 504, while the Machine answered
// lately or its host answers, shows at most the quiet "Your Machine is slow to answer" line: no Offline banner, no
// "Offline · updated", no "Can’t reach" and no Report a bug, and what is on screen stays. A Machine really away (calls
// failing at once, the host not answering) still says Offline and Can’t reach.
const raw=await dashboardPage(),sw=await readFile(new URL('../sw.js',import.meta.url),'utf8');
const SCOPE='c3'.repeat(16),iso=new Date().toISOString(),SLOW=/Your Machine is slow to answer\./;
const card=(id,title)=>({id,title,body:'Robin asked for the numbers.',status:'pending',scope:'work',created_at:iso,event_ids:[1]});
let title='Reply to Robin about the plan';
const status=()=>({suggestions:[card('1'.repeat(16),title)],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false},ui_version:'v1'});
const page=()=>raw.replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__',SCOPE);
// How the next api/status calls go ('cut': 9 s, then the link breaks; 'gw': 9 s, then a gateway's 504; 'wait': 9 s,
// then the answer); fails counts how many. action: the same for api/action. gone: the Machine and its host away
// (every call breaks at once).
let mode='ok',fails=0,action='ok',gone=false;
const later=ms=>new Promise(r=>setTimeout(r,ms));
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Cache-Control','no-store');
 // a fresh connection each call, so the browser never resends a call whose link broke (as it may on a kept-alive one)
 res.setHeader('Connection','close');
 if(gone&&url.pathname!=='/'&&url.pathname!=='/sw.js'){req.socket.destroy();return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page());return}
 if(url.pathname==='/sw.js'){res.setHeader('Content-Type','text/javascript');res.end(sw);return}
 if(url.pathname==='/manifest.webmanifest'){res.setHeader('Content-Type','application/manifest+json');res.end('{}');return}
 res.setHeader('Content-Type','application/json');
 const how=url.pathname==='/api/status'&&fails>0?mode:url.pathname==='/api/action'&&body.includes('graph_org_merge')?action:'ok';
 if(how!=='ok'){if(url.pathname==='/api/status')fails--;else action='ok';await later(9000);
  if(how==='cut'){req.socket.destroy();return}
  if(how==='gw'){res.statusCode=504;res.setHeader('Content-Type','text/html');res.end('<h1>504 Gateway Timeout</h1>');return}}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:SCOPE}));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const until=async(p,fn,arg,label,timeout=15000)=>{try{await p.waitForFunction(fn,arg,{timeout})}catch{throw Error('timed out: '+label)}};
// Every moment something alarming showed (a glimpse counts too), and whether the quiet line showed
const watch=p=>p.addInitScript(()=>{window.__seen=[];const seen=()=>{const b=document.querySelector('#offline-bar'),n=document.querySelector('#stale-note'),u=document.querySelector('#updated'),
  s=document.querySelector('#toast'),c=document.querySelector('#suggestions');
  if(b&&!b.hidden&&/Offline/.test(b.textContent))__seen.push('banner: '+b.textContent);
  for(const x of [n&&!n.hidden&&n,u])if(x&&/Offline|reach/i.test(x.textContent))__seen.push('line: '+x.textContent);
  if(s?.classList.contains('show')&&(s.classList.contains('error')||/reach/i.test(s.textContent)))__seen.push('toast: '+s.textContent);
  if(c&&/can’t reach/i.test(c.textContent))__seen.push('empty: '+c.textContent);
  if(n&&!n.hidden&&/slow to answer/.test(n.textContent))__seen.push('quiet');};
 new MutationObserver(seen).observe(document,{subtree:true,childList:true,attributes:true,characterData:true})});
const seen=p=>p.evaluate(()=>{const a=__seen;window.__seen=[];return [...new Set(a)]});
const alarms=list=>list.filter(x=>x!=='quiet');
const resume=p=>p.evaluate(()=>{let hidden=true;Object.defineProperty(document,'hidden',{configurable:true,get:()=>hidden});document.dispatchEvent(new Event('visibilitychange'));
 hidden=false;document.dispatchEvent(new Event('visibilitychange'))});
const act=p=>p.evaluate(()=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrfLive},body:JSON.stringify({action:'graph_org_merge',args:{}})})
 .then(()=>'ok',e=>{toast(e.message,true);return {slow:!!e.slow,offline:!!e.offline}}));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const tab=await context.newPage();tab.on('pageerror',e=>errors.push(e.message));await watch(tab);
 await tab.goto(base);await tab.locator('#suggestions article[id]').first().waitFor();
 for(let n=0;!(await tab.evaluate(async()=>!!(await localCache.read('status'))));n++){assert.ok(n<150,'the to-dos are kept on the device');await tab.waitForTimeout(100)}
 assert.deepEqual(await seen(tab),[],'online: nothing shows');

 // 1. Reopened while the Machine is busy: the first call waits 9 s and then breaks (or the gateway gives up, 504).
 // The to-dos stay, the quiet line shows, never Offline, and the retry brings the live view.
 for(const how of ['cut','gw']){
  mode=how;fails=1;title='Live after a slow '+how;await resume(tab);
  await until(tab,()=>!document.querySelector('#stale-note').hidden&&/slow to answer/.test(document.querySelector('#stale-note').textContent),null,how+': the quiet line',15000);
  assert.ok(await tab.locator('#suggestions article[id]').count()>0,how+': the to-dos stay on screen');
  await until(tab,t=>document.querySelector('#suggestions').innerText.includes(t),title,how+': the retry brings the live view',25000);
  await until(tab,()=>document.querySelector('#stale-note').hidden,null,how+': the quiet line goes once it answers');
  const s=await seen(tab);assert.deepEqual(alarms(s),[],how+': nothing alarming');assert.ok(s.includes('quiet'),how+': the quiet line showed');
  assert.equal(await tab.evaluate(()=>netOut||netSlow),false,how+': live again')}

 // 2. A read still waiting after 8 s: the quiet line while it waits, gone once it answers
 mode='wait';fails=1;title='Live after a long wait';await resume(tab);
 await until(tab,()=>/slow to answer/.test(document.querySelector('#stale-note').textContent)&&!document.querySelector('#stale-note').hidden,null,'waiting: the quiet line',12000);
 await until(tab,t=>document.querySelector('#suggestions').innerText.includes(t)&&document.querySelector('#stale-note').hidden,title,'waiting: live, the line gone',15000);
 assert.deepEqual(alarms(await seen(tab)),[],'waiting: nothing alarming');

 // 3. A change that takes long and then breaks (a merge on a busy Machine): a quiet note, no Report a bug
 action='cut';assert.deepEqual(await act(tab),{slow:true,offline:true},'a slow change is slow (and still waits like offline)');
 assert.match(await tab.locator('#toast').textContent(),SLOW);
 assert.equal(await tab.locator('#toast [data-bug-report]').count(),0,'no Report a bug for slowness');
 assert.equal(await tab.locator('#toast').evaluate(n=>n.classList.contains('error')),false,'not an error toast');
 assert.deepEqual(alarms(await seen(tab)),[],'slow change: nothing alarming');
 await tab.evaluate(()=>refresh());await until(tab,()=>!netSlow&&document.querySelector('#stale-note').hidden,null,'slow change: the line goes on the next answer');

 // 4. A cold start from the device's copy with a slow first call: the kept to-dos at once, then live, nothing alarming
 mode='cut';fails=1;title='Live after a slow cold start';await tab.reload();await tab.locator('#suggestions article[id]').first().waitFor({timeout:3000});
 await until(tab,t=>document.querySelector('#suggestions').innerText.includes(t),title,'cold start: live after the retry',30000);
 assert.deepEqual(alarms(await seen(tab)),[],'cold start: nothing alarming');

 // 5. Really away (every call breaks at once, the host too): Offline shows, and a change says Can’t reach with Report a bug
 gone=true;await resume(tab);
 await until(tab,()=>{const b=document.querySelector('#offline-bar');return !b.hidden&&/^Offline\./.test(b.textContent)},null,'really offline: the banner',15000);
 assert.equal(await tab.evaluate(()=>netSlow),false,'really offline is not slow');
 assert.deepEqual(await act(tab),{slow:false,offline:true});
 assert.match(await tab.locator('#toast').textContent(),/Can’t reach your Machine/);
 assert.equal(await tab.locator('#toast [data-bug-report]').count(),1,'a real failure keeps Report a bug');
 gone=false;await seen(tab);
 await tab.evaluate(()=>document.querySelector('#offline-bar [data-net-retry]').click());
 await until(tab,()=>document.querySelector('#offline-bar').hidden,null,'back online');

 assert.deepEqual(errors,[]);
 console.log('slow not offline dashboard ok');
}finally{await browser?.close();server.close()}
