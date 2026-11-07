import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A web push's quick buttons (machine/delivery/push.py QUICK): Snooze 2h, Snooze and Mark done. A browser can't ask for
// an unlock first, so sw.js never runs them itself: it keeps the tapped button under a random id (quickKeep) and opens
// the dashboard at #quick=<id>; the page takes it from the worker once and does it, with Undo. A #quick= link the worker
// didn't make, an old one or one used twice does nothing; a to-do handled meanwhile opens as it is. Here the worker's
// quickKeep is played by putting its entry in the cache, as it does. All to-dos are made up.
// SHOT_DIR=<folder> also saves screenshots.
const dashboard=await dashboardPage();
const root=new URL('..',import.meta.url);
const sw=await readFile(new URL('sw.js',root),'utf8');
const now=new Date().toISOString(),A='a1'.repeat(8),B='b2'.repeat(8),C='c3'.repeat(8);
const cards=[{id:A,title:'Answer the school about the trip',body:'They need a yes by Friday.',status:'pending',scope:'personal',created_at:now,event_ids:[1]},
 {id:B,title:'Find the train times to Ghent',body:'For Saturday morning.',status:'prepared',preparation_status:'ok',scope:'personal',created_at:now,event_ids:[2]},
 {id:C,title:'Renew the passport',body:'It runs out in May.',status:'completed',scope:'personal',created_at:now,event_ids:[3]}];
const decides=[];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/sw.js'){res.setHeader('Content-Type','text/javascript');res.end(sw);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  if(r.action==='decide'){const a=r.args,s=cards.find(x=>x.id===a.suggestion_id);decides.push([a.suggestion_id,a.choice,a.snooze_option||'']);
   if(a.choice==='snooze'){s.status='snoozed';s.snoozed_until=new Date(Date.now()+2*36e5).toISOString();res.end(JSON.stringify({status:'snoozed',snoozed_until:s.snoozed_until}));return}
   if(a.choice==='complete'){s.status='completed';res.end(JSON.stringify({status:'completed'}));return}
   if(a.choice==='accept'){s.status='pending';delete s.snoozed_until;res.end(JSON.stringify({status:'pending'}));return}}
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k',items:[]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.SHOT_DIR||'';
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);await page.locator('#task-'+A).waitFor();
 await page.evaluate(async()=>{await navigator.serviceWorker.register('sw.js');await navigator.serviceWorker.ready});
 await page.reload();await page.waitForFunction(()=>!!navigator.serviceWorker.controller);await page.locator('#task-'+A).waitFor();
 // what sw.js quickKeep does when a quick button is tapped
 let n=0;const keep=(tag,action,age=0)=>page.evaluate(async([tag,action,age,id])=>{
  await (await caches.open('tm-share')).put(new URL('quick/'+id,location.origin+'/').href,
   new Response(JSON.stringify({tag,action}),{headers:{'Content-Type':'application/json','X-At':String(Date.now()-age)}}));return id},[tag,action,age,'k_'+String(++n).padStart(16,'0')]);
 const tap=async id=>{await page.evaluate(id=>{location.hash='quick='+id},id);await page.waitForFunction(()=>!location.hash.startsWith('#quick='))};
 const toast=()=>page.locator('#toast.show');
 const quiet=async()=>{await page.waitForTimeout(800);return decides.length};

 // Snooze 2h: snoozed from the page, said, with Undo that puts it back
 let id=await keep(A,'snooze2h');await tap(id);
 await page.waitForFunction(()=>/Snoozed\./.test(document.querySelector('#toast.show')?.textContent||''));
 assert.deepEqual(decides,[[A,'snooze','2h']]);
 assert.equal(await toast().locator('[data-quick-undo]').textContent(),'Undo');
 assert.equal(new URL(page.url()).hash,'',`the #quick= link is gone from the address`);
 if(shots)await page.screenshot({path:shots+'/web-quick-snoozed.png'});
 await toast().locator('[data-quick-undo]').click();
 await page.waitForFunction(()=>/Unsnoozed it/.test(document.querySelector('#toast.show')?.textContent||''));
 assert.deepEqual(decides.at(-1),[A,'accept','']);
 // the same button again (a second tap, the back button): taken once, nothing more
 let before=decides.length;await tap(id);assert.equal(await quiet(),before);

 // Mark done: done, with the list's own Undo
 id=await keep(B,'done');await tap(id);
 await page.waitForFunction(()=>/Marked done/.test(document.querySelector('#toast.show')?.textContent||''));
 assert.deepEqual(decides.at(-1),[B,'complete','']);
 if(shots)await page.screenshot({path:shots+'/web-quick-done.png'});

 // Snooze (tomorrow) from a reminder
 cards[1].status='prepared';await page.reload();await page.locator('#task-'+B).waitFor();await page.waitForFunction(()=>!!navigator.serviceWorker.controller);
 id=await keep(B,'snooze');await tap(id);
 await page.waitForFunction(()=>/Snoozed\./.test(document.querySelector('#toast.show')?.textContent||''));
 assert.deepEqual(decides.at(-1),[B,'snooze','tomorrow']);

 // a link the worker didn't make, an old button, a button for a send: nothing runs
 before=decides.length;
 await tap('k_'+'f'.repeat(16));
 await tap(await keep(A,'done',6*6e4));
 await tap(await keep(A,'send'));
 assert.equal(await quiet(),before);

 // a to-do done meanwhile: opens as it is, nothing runs
 await tap(await keep(C,'done'));
 await page.waitForFunction(c=>location.hash==='#chat='+c,C);assert.equal(await quiet(),before);

 // a tap that starts the page: done once the to-dos are in
 cards[0].status='pending';id=await keep(A,'done');
 await page.goto(base+'#quick='+id);
 await page.waitForFunction(()=>/Marked done/.test(document.querySelector('#toast.show')?.textContent||''));
 assert.deepEqual(decides.at(-1),[A,'complete','']);
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('quick buttons dashboard ok');
