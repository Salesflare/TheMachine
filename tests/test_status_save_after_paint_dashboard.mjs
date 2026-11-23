import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The device's copy of the status (localCache, docs/architecture.md "On the device") is a pass over the whole status
// (copied without secrets, sealed), so on a page's first drawing it is saved just after the to-dos are painted, not
// before they are drawn. It is still saved, and once the page is whole a newer status is saved right away.
const raw=await dashboardPage();
const SCOPE='a1'.repeat(16),iso=new Date().toISOString();
const cards=[{id:'1'.repeat(16),title:'Check the payroll is ready',body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:iso,event_ids:[1]}];
let extra=[];
const status=()=>({suggestions:[...cards,...extra],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]},ui_version:'v1'});
const page=()=>raw.replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__',SCOPE);
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page());return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:SCOPE}));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname==='/sw.js'?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base=`http://127.0.0.1:${server.address().port}/`;
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 // The save's other way, a timer for a page whose frames don't come (a background tab), is held back until asked for: a
 // slow computer's first frame can take longer than it
 await context.addInitScript(()=>{const timer=self.setTimeout,held=[];self.setTimeout=(f,ms,...a)=>ms===300&&/^\(\)=>\{if\(!saved/.test(String(f))?(held.push(f),0):timer(f,ms,...a);self.heldTimers=held});
 // When the first to-do is in the page, the first frame after that (painted next), each copy of the status made for
 // the device (the device store's own JSON.stringify, called from its put) and each write to the device's store
 await context.addInitScript(()=>{self.seen={card:null,frame:null,copies:[],saves:[]};
  const put=IDBObjectStore.prototype.put;IDBObjectStore.prototype.put=function(v,k){if(k==='status')self.seen.saves.push(performance.now());return put.apply(this,arguments)};
  const str=JSON.stringify;JSON.stringify=function(v){if(v&&Array.isArray(v.suggestions)&&/\bput\b/.test(new Error().stack))self.seen.copies.push(performance.now());return str.apply(this,arguments)};
  new MutationObserver((_,o)=>{if(document.querySelector('#suggestions article.card')){o.disconnect();self.seen.card=performance.now();requestAnimationFrame(()=>{self.seen.frame=performance.now()})}})
   .observe(document,{subtree:true,childList:true})});
 const p=await context.newPage();p.on('pageerror',e=>errors.push(e.message));await p.goto(base);
 await p.waitForFunction(()=>typeof drawnWhole!=='undefined'&&drawnWhole&&self.seen.saves.length>0,null,{timeout:15000});
 const seen=await p.evaluate(()=>self.seen);
 assert.ok(seen.card!=null&&seen.frame!=null,`the to-dos were drawn ${JSON.stringify(seen)}`);
 assert.equal(seen.copies.length,1,`copied once ${JSON.stringify(seen)}`);assert.equal(seen.saves.length,1,`saved once ${JSON.stringify(seen)}`);
 assert.ok(seen.copies[0]>seen.frame,`copied after the to-dos were painted, not before ${JSON.stringify(seen)}`);
 assert.equal(await p.evaluate(async()=>(await localCache.read('status'))?.value?.suggestions?.length),1,'the saved copy has the to-dos');
 assert.ok(await p.evaluate(()=>heldTimers.length)>0,'a timer saves it on a page whose frames do not come');
 await p.evaluate(()=>heldTimers.forEach(f=>f()));assert.equal(await p.evaluate(()=>self.seen.copies.length),1,'and not again once it is saved');
 // Once whole, a changed status is saved in the same refresh
 extra=[{...cards[0],id:'2'.repeat(16),title:'Book the room'}];
 // (the store's put comes once the copy is sealed, a moment after the call: no paint is waited for)
 await p.evaluate(async()=>{const was=localCache.put;let called=0;localCache.put=(...a)=>{if(a[0]==='status')called++;return was(...a)};await refresh();localCache.put=was;self.seen.called=called});
 assert.equal(await p.evaluate(()=>self.seen.called),1,'a newer status saved in the same refresh');
 await p.waitForFunction(()=>self.seen.saves.length===2);
 assert.equal(await p.evaluate(async()=>(await localCache.read('status'))?.value?.suggestions?.length),2,'the newer copy');
 await p.close();
 assert.deepEqual(errors,[]);
 console.log('ok: the status is saved on the device just after the first drawing is painted');
}finally{await browser?.close();server.close()}
