import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A link to a to-do (a notification's #card=, the app's tap) opened on a page whose list was read before the to-do
// moved: a page back from the background, before its next read. It lands on the to-do where the page still has it;
// the next read must not leave it folded away somewhere with nothing picked out (cardLandAgain, todos-chat-thread.js):
// done, it opens its chat as the link says (&or=chat); snoozed, Coming back later opens on it, highlighted. One that
// didn't move stays as it landed, never pulled to again.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),ID='d0d0d0d0d0d0d0d0';
const open=Array.from({length:12},(_,i)=>({id:(i+1).toString(16).padStart(16,'a'),title:'Open to-do '+i,body:'Something to do.',status:'new',scope:'work',created_at:now,event_ids:[1]}));
const done=Array.from({length:35},(_,i)=>({id:(i+1).toString(16).padStart(16,'c'),title:'Earlier done '+i,body:'Done.',status:'completed',scope:'work',created_at:now,event_ids:[1]}));
const card={id:ID,title:'Book the train',body:'Ready to book.',status:'new',scope:'work',created_at:now,event_ids:[1]};
const cards=[card,...open,...done];
const waiting=()=>{for(const k of ['done_report','snoozed_until'])delete card[k];card.status='new'};
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[]});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k',items:[{kind:'reply',text:'Booked it.',at:Date.now()}]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.CARD_LINK_SHOTS||'';
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [label,viewport] of [['phone',{width:390,height:844}],['desktop',{width:1440,height:900}]]){
  const context=await browser.newContext({viewport,locale:'en-US',...(label==='phone'?{isMobile:true,hasTouch:true}:{})});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const onScreen=(sel,why)=>page.waitForFunction(s=>{const el=document.querySelector(s);if(!el||el.closest('[hidden]'))return false;const r=el.getBoundingClientRect();return r.height>0&&r.bottom>0&&r.top<innerHeight},sel,{timeout:15000}).catch(()=>assert.fail(`${label} ${why}: ${sel} not on screen`));
  // the page reads the list with the to-do still waiting, then the Machine moves it, then the link comes in
  const stale=async(move,hash)=>{waiting();await page.goto(base);await page.locator('#task-'+ID).first().waitFor();move();
   await page.evaluate(h=>{location.hash=h},hash);await onScreen(`#task-${ID}.flash`,'lands where the page has it');assert.equal(new URL(page.url()).hash,'')};
  // done: the next read opens its chat, as &or=chat says for one no longer in the list as shown
  await stale(()=>{card.status='completed';card.done_report=now},'card='+ID+'&or=chat');
  await page.evaluate(()=>refresh());await onScreen(`.chat-layout[data-chat="${ID}"] .chat-title`,'done: its chat');
  if(shots)await page.screenshot({path:`${shots}/${label}-done.png`});
  // snoozed: Coming back later opens on it, in view and highlighted
  await stale(()=>{card.status='snoozed';card.snoozed_until=new Date(Date.now()+864e5).toISOString()},'card='+ID);
  await page.evaluate(()=>refresh());await onScreen(`#later-list[open] #task-${ID}.flash`,'snoozed: in Coming back later');
  assert.equal(await page.locator('.chat-layout').count(),0,`${label} snoozed: no chat`);
  if(shots)await page.screenshot({path:`${shots}/${label}-snoozed.png`});
  // unchanged: the next read leaves the page as it is (no second landing, no address)
  await stale(()=>{},'card='+ID+'&or=chat');await page.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));const y=await page.evaluate(()=>scrollY);
  await page.evaluate(()=>refresh());  // the read and its redraw are done when it returns
  assert.equal(new URL(page.url()).hash,'',`${label} unchanged: no link again`);assert.equal(await page.locator('.chat-layout').count(),0);
  assert.ok(Math.abs(await page.evaluate(()=>scrollY)-y)<2,`${label} unchanged: not pulled back to it`);
  // A "Done: …" notification tapped while the page sat in the background (its list a minute old, nothing read since):
  // the page reads the list at once and opens the to-do's chat by itself. The phone app's tap (mobile/www/inject.js
  // listen, as the app runs it) and the web push's (sw.js hands an open page the link, which sets its address).
  const INJECT=readFileSync(new URL('../mobile/www/inject.js',import.meta.url),'utf8');
  for(const [via,tap] of [['app',()=>page.evaluate(id=>window.__tap({notification:{data:{tag:id}}}),ID)],['web push',()=>page.evaluate(id=>{location.hash='card='+id+'&or=chat'},ID)]]){
   waiting();await page.goto(base);await page.locator('#task-'+ID).first().waitFor();
   await page.evaluate(()=>{window.Capacitor={Plugins:{PushNotifications:{addListener:(name,f)=>{if(name==='pushNotificationActionPerformed')window.__tap=f}}}}});
   await page.evaluate(`(${INJECT})(${JSON.stringify({base,listen:true})})`);
   card.status='completed';card.done_report=now;await page.evaluate(()=>{shownAt-=6e4});
   await tap();await onScreen(`.chat-layout[data-chat="${ID}"] .chat-title`,`${via}: the done to-do's chat, from a page in the background`);
   if(shots&&via==='app')await page.screenshot({path:`${shots}/${label}-push-done.png`})}
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('card link stale dashboard ok');
