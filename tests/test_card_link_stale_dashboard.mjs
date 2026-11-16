import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A tapped notification about a to-do lands on the to-do itself in the To-dos list, wherever it is now, scrolled into
// view and highlighted, never its chat: done (Just done at the top, or in Done, which opens with its row drawn),
// snoozed (Coming back later opens on it) or still open. Links sent before with &or=chat land there too. A tap that
// reaches a page sitting in the background (its list read before the to-do moved) reads the list first and lands where
// the to-do is now (cardLandAgain, todos-chat-thread.js); one that didn't move stays as it landed, never pulled to again.
// Through the phone app (mobile/www/inject.js, as the app runs it), the web push (sw.js's notificationclick, the real
// worker) and a link that starts the page. The landing on the list from before starts a glide there; the second landing
// stops it, or a tap on a to-do now in Just done ended up far below it. CARD_LINK_SHOTS=<folder> saves the landed rows.
const dashboard=await dashboardPage();
const INJECT=readFileSync(new URL('../mobile/www/inject.js',import.meta.url),'utf8');
const SW=readFileSync(new URL('../sw.js',import.meta.url),'utf8');
const now=new Date().toISOString(),ID='d0d0d0d0d0d0d0d0';
const open=Array.from({length:12},(_,i)=>({id:(i+1).toString(16).padStart(16,'a'),title:'Open to-do '+i,body:'Something to do.',status:'new',scope:'work',created_at:now,event_ids:[1]}));
const done=Array.from({length:35},(_,i)=>({id:(i+1).toString(16).padStart(16,'c'),title:'Earlier done '+i,body:'Done.',status:'completed',scope:'work',created_at:now,event_ids:[1]}));
const card={id:ID,title:'Book the train',body:'Ready to book.',status:'new',scope:'work',created_at:now,event_ids:[1]};
const cards=[...open,card,...done];
const waiting=()=>{for(const k of ['done_report','snoozed_until'])delete card[k];card.status='new'};
const MOVES={
 'done, in Just done':{move:()=>{card.status='completed';card.done_report=now},where:`#section-just-done ~ #task-${ID}`},
 'done, in Done':{move:()=>{card.status='completed'},where:`#finished-list[open] #task-${ID}`},
 snoozed:{move:()=>{card.status='snoozed';card.snoozed_until=new Date(Date.now()+864e5).toISOString()},where:`#later-list[open] #task-${ID}`},
 open:{move:()=>{},where:`#task-${ID}`}};
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/sw.js'){res.setHeader('Content-Type','text/javascript');res.end(SW);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:[],next:null,total:0}));return}
 if(url.pathname==='/api/action'){res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.CARD_LINK_SHOTS||'';
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [label,viewport] of [['phone',{width:390,height:844}],['desktop',{width:1440,height:900}]]){
  const context=await browser.newContext({viewport,locale:'en-US',...(label==='phone'?{isMobile:true,hasTouch:true}:{})});
  await context.grantPermissions(['notifications'],{origin:base.slice(0,-1)});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));  await page.goto(base);await page.evaluate(async()=>{await navigator.serviceWorker.register('sw.js');await navigator.serviceWorker.ready});
  const worker=context.serviceWorkers()[0]||await context.waitForEvent('serviceworker');
  // the to-do itself: on screen, highlighted, in its list; no chat, nothing left in the address
  // whole and settled: the scroll to it has ended (the same place on three checks in a row)
  const landed=async(sel,why)=>{await page.waitForFunction(s=>{const el=document.querySelector(s);if(!el||el.closest('[hidden]')||!el.classList.contains('flash'))return false;const r=el.getBoundingClientRect();
    const whole=r.height>0&&r.top>=0&&r.bottom<=innerHeight,key=s+Math.round(r.top);window.__settle=whole&&window.__settle?.key===key?{key,n:window.__settle.n+1}:{key,n:0};return whole&&window.__settle.n>=2},sel,{timeout:15000,polling:100}).catch(async()=>assert.fail(`${label} ${why}: ${sel} not whole on screen and highlighted `+JSON.stringify(await page.evaluate(s=>[...document.querySelectorAll(s)].map(el=>({r:el.getBoundingClientRect().toJSON(),flash:el.classList.contains('flash'),ih:innerHeight,y:scrollY})),sel))));
   assert.equal(await page.locator('.chat-layout').count(),0,`${label} ${why}: no chat`);assert.equal(new URL(page.url()).hash,'',`${label} ${why}: the link is taken off the address`)};
  const TAPS={
   // the phone app's tap on a page it has open (inject.js listen), as an older app sends it (&or=chat)
   app:async()=>{await page.evaluate(()=>{window.Capacitor={Plugins:{PushNotifications:{addListener:(name,f)=>{if(name==='pushNotificationActionPerformed')window.__tap=f}}}}});
    await page.evaluate(`(${INJECT})(${JSON.stringify({base,listen:true})})`);return ()=>page.evaluate(id=>window.__tap({notification:{data:{tag:id}}}),ID)},
   // the web push: sw.js's own notificationclick hands the open page the notification's link
   'web push':async()=>{await page.waitForFunction(()=>!!navigator.serviceWorker.controller);return ()=>worker.evaluate(async([id,url])=>{
    await self.registration.showNotification('Done: Book the train',{tag:id,data:{url}});const [n]=await self.registration.getNotifications({tag:id});
    const w=ExtendableEvent.prototype.waitUntil;ExtendableEvent.prototype.waitUntil=function(p){if(this.isTrusted)return w.call(this,p);self.__last=Promise.resolve(p)};
    self.dispatchEvent(new NotificationEvent('notificationclick',{notification:n}));await self.__last},[ID,base+'#card='+ID])}};
  for(const [via,arm] of Object.entries(TAPS))for(const [what,{move,where}] of Object.entries(MOVES)){
   // the page read the list while the to-do still waited, then sat in the background; the Machine moved it since
   waiting();await page.goto(base);await page.locator('#task-'+ID).first().waitFor();const tap=await arm();
   move();await page.evaluate(()=>{shownAt-=6e4});await tap();await landed(where,`${via}, ${what}`);
   if(shots&&via==='app')await page.screenshot({path:`${shots}/${label}-${what.toLowerCase().replace(/[^a-z]+/g,'-')}.png`})}
  // a link that starts the page (the app from cold, an email's Open), with &or=chat from before: the to-do too
  for(const [what,{move,where}] of Object.entries(MOVES)){waiting();move();await page.goto('about:blank');await page.goto(base+'#card='+ID+'&or=chat');await landed(where,`cold, ${what}`)}
  // unchanged: the next read leaves the page as it is (no second landing, no scroll back to it)
  waiting();await page.goto(base);await page.locator('#task-'+ID).first().waitFor();await page.evaluate(id=>{location.hash='card='+id},ID);await landed(`#task-${ID}`,'unchanged');
  await page.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));const y=await page.evaluate(()=>scrollY);
  await page.evaluate(()=>refresh());  // the read and its redraw are done when it returns
  assert.equal(new URL(page.url()).hash,'',`${label} unchanged: no link again`);
  assert.ok(Math.abs(await page.evaluate(()=>scrollY)-y)<2,`${label} unchanged: not pulled back to it`);
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('card link stale dashboard ok');
