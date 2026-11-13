import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A web push's quick buttons (machine/delivery/push.py QUICK): Snooze (2 hours, or tomorrow on a reminder) and Mark done. A browser can't ask for
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
 {id:B,title:'Find the train times to Ghent',body:'For Saturday morning. The 8:14 and the 9:14 both stop in Ghent, and the later one has a direct connection to the coast, which is what the weekend plan needs.',next_actions:[{kind:'email',to:['sam@example.invalid'],to_name:'Sam',subject:'Train times',revision:1,body:'Hi Sam,\n\nThe 8:14 gets to Ghent at 9:05.\nThe 9:14 gets there at 10:05.\nBoth run on Saturday.\nThe later one connects to the coast.\nTickets are cheaper before 9.\nI can book either one.\nTell me which you like.\n\nTalk soon'}],status:'prepared',preparation_status:'ok',scope:'personal',created_at:now,event_ids:[2]},
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
  if(r.action==='card_chat'&&!cards.some(x=>x.id===r.args.suggestion_id)){res.statusCode=400;res.end(JSON.stringify({error:'Unknown suggestion'}));return}
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
 await context.grantPermissions(['notifications'],{origin:base.slice(0,-1)});
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

 // Snooze (2 hours): snoozed from the page, said, with Undo that puts it back
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

 // a to-do that isn't there anymore (deleted, or merged away): one short line on the list, never a blank chat
 const G='d4'.repeat(8);
 for(const go of [()=>page.evaluate(g=>{location.hash='chat='+g},G),async()=>tap(await keep(G,'done'))]){
  await go();
  await page.waitForFunction(()=>/That to-do isn’t here anymore\./.test(document.querySelector('#toast.show')?.textContent||''));
  assert.equal(new URL(page.url()).hash,'');assert.equal(await page.locator(`.chat-layout[data-chat="${G}"]`).count(),0);
  await page.evaluate(()=>document.querySelector('#toast').classList.remove('show'))}
 assert.equal(await quiet(),before);
 // a chat opened from a list kept since before (a phone back from the background) on a to-do removed meanwhile: the
 // next refresh closes it with the same line, never leaves the old to-do up
 const R='e5'.repeat(8);cards.push({id:R,title:'Water the plants',body:'Before the weekend.',status:'pending',scope:'personal',created_at:now,event_ids:[4]});
 await page.evaluate(()=>refresh());await page.locator('#task-'+R).waitFor();
 await page.evaluate(r=>{location.hash='chat='+r},R);await page.waitForFunction(r=>chatId===r,R);
 cards.pop();await page.evaluate(()=>refresh());
 await page.waitForFunction(()=>/That to-do isn’t here anymore\./.test(document.querySelector('#toast.show')?.textContent||''));
 assert.equal(await page.evaluate(()=>chatId),null);assert.equal(new URL(page.url()).hash,'');
 await page.evaluate(()=>document.querySelector('#toast').classList.remove('show'));
 // and a notification tapped on such a list: the Machine says the to-do is unknown, so the chat closes with the line at
 // once, never "couldn't load my replies" with live buttons on a to-do that is gone
 cards.push({...cards.at(-1),id:'f6'.repeat(8),title:'Feed the cat'});await page.evaluate(()=>refresh());await page.locator('#task-'+'f6'.repeat(8)).waitFor();
 cards.pop();await page.evaluate(()=>{location.hash='chat='+'f6'.repeat(8)});
 await page.waitForFunction(()=>/That to-do isn’t here anymore\./.test(document.querySelector('#toast.show')?.textContent||''),null,{timeout:4000});
 assert.equal(await page.evaluate(()=>chatId),null);assert.equal(new URL(page.url()).hash,'');
 await page.evaluate(()=>document.querySelector('#toast').classList.remove('show'));

 // Open draft, through sw.js's own notificationclick: the to-do in the list (#card=), where its draft shows in full
 Object.assign(cards[1],{status:'prepared'});delete cards[1].snoozed_until;await page.evaluate(()=>refresh());await page.locator(`#task-${B} .draft`).waitFor();
 const worker=context.serviceWorkers()[0]||await context.waitForEvent('serviceworker');
 await worker.evaluate(async([B,url])=>{const w=ExtendableEvent.prototype.waitUntil;ExtendableEvent.prototype.waitUntil=function(p){if(this.isTrusted)return w.call(this,p);self.__last=Promise.resolve(p)};
  await self.registration.showNotification('Ready: Find the train times',{tag:B,data:{url},actions:[{action:'draft',title:'Open draft'}]});
  const [n]=await self.registration.getNotifications({tag:B});self.dispatchEvent(new NotificationEvent('notificationclick',{notification:n,action:'draft'}));await self.__last},[B,base+'#chat='+B]);
 await page.waitForFunction(b=>document.getElementById('task-'+b)?.classList.contains('flash'),B);  // #card= scrolls it into view and flashes it
 // and shows it whole: the summary and the draft, nothing behind Show more
assert.equal(await page.locator(`#task-${B} .clamp`).count(),0);assert.ok(await page.locator(`#task-${B} .draft`).isVisible());
 assert.ok(/Talk soon/.test(await page.locator(`#task-${B} .draft`).innerText()));
 if(shots)await page.screenshot({path:shots+'/open-draft-whole.png'});
 assert.equal(await page.locator(`.chat-layout[data-chat="${B}"]`).count(),0);assert.equal(await quiet(),before);
 // A tap on the notification itself: the to-do in the list too, never its chat; one shown before with a #chat= url too
 for(const url of [base+'#card='+B+'&or=chat',base+'#chat='+B]){
  await page.evaluate(()=>{for(const c of document.querySelectorAll('.flash'))c.classList.remove('flash');history.replaceState(null,'',location.pathname)});
  await worker.evaluate(async([B,url])=>{await self.registration.showNotification('Ready: Find the train times',{tag:B,data:{url}});
   const [n]=await self.registration.getNotifications({tag:B});self.dispatchEvent(new NotificationEvent('notificationclick',{notification:n}));await self.__last},[B,url]);
  await page.waitForFunction(b=>document.getElementById('task-'+b)?.classList.contains('flash'),B);
  assert.equal(await page.locator(`.chat-layout[data-chat="${B}"]`).count(),0,url)}

 // a tap that starts the page: done once the to-dos are in
 cards[0].status='pending';id=await keep(A,'done');
 await page.goto(base+'#quick='+id);
 await page.waitForFunction(()=>/Marked done/.test(document.querySelector('#toast.show')?.textContent||''));
 assert.deepEqual(decides.at(-1),[A,'complete','']);
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('quick buttons dashboard ok');
