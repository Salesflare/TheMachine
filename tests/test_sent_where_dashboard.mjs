import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do just acted on is easy to find again (made-up data). Once a send went out, a short toast says where the to-do
// is now, with Open to go to it there: "Sent. Moved to Done." or, handed to someone, "Sent. Moved to Later until Mon."
// Done reads newest first by when each closed, and a done card says when ("Done just now"), not when it came in: a
// to-do made two days ago and sent now leads Done. The search finds to-dos by title and by who they went to, open,
// later and done alike, and its line says where each one is.
const dashboard=await dashboardPage();
const at=h=>new Date(Date.now()-h*36e5).toISOString();
const id=n=>(n+'').padStart(2,'0').repeat(8);
const base0=()=>[
 {id:id(1),title:'Send Northfield the editable agreements',body:'Drafted a reply with both files.',status:'prepared',scope:'work',created_at:at(50),event_ids:[1],
  next_actions:[{kind:'email',label:'Send reply',revision:'aa11bb22cc33',to:['dana.reyes@northfield.example'],to_name:'Dana Reyes',subject:'Agreements',body:'Hi Dana, both files attached.',snooze_days:3}]},
 {id:id(2),title:'Hand the venue booking to Robin',body:'Robin books venues.',status:'prepared',scope:'work',created_at:at(5),event_ids:[2],
  next_actions:[{kind:'email',label:'Send to Robin',revision:'dd44ee55ff66',to:['robin@studio.example'],to_name:'Robin Hale',subject:'Venue',body:'Hi Robin, could you book it?',delegate:true,wait_days:3}]},
 {id:id(3),title:'Answer Lee about the invoice',body:'Answered.',status:'completed',scope:'work',created_at:at(3),closed_at:at(1),event_ids:[3]},
 {id:id(4),title:'Book the dentist',body:'',status:'pending',scope:'personal',created_at:at(1),event_ids:[4]},
 {id:id(5),title:'Confirm the workshop date',body:'Drafted a reply.',status:'prepared',scope:'work',created_at:at(4),event_ids:[5],
  next_actions:[{kind:'email',label:'Send reply',revision:'ab12cd34ef56',to:['sam@harbor.example'],to_name:'Sam Okoro',subject:'Workshop',body:'Hi Sam, the 12th works.'}]},
 {id:id(6),title:'Thank the printer',body:'Drafted a reply.',status:'prepared',scope:'work',created_at:at(4),event_ids:[6],
  next_actions:[{kind:'email',label:'Send reply',revision:'ba21dc43fe65',to:['kim@press.example'],to_name:'Kim Vale',subject:'Thanks',body:'Hi Kim, thanks.'}]}];
let cards,going;
const reset=()=>{cards=base0();going=new Map()};reset();
// A send takes a moment: the next status read still says sending, the one after it shows where the to-do went
function settle(){for(const [cid,n] of going){const c=cards.find(x=>x.id===cid),a=c.next_actions[0];if(n>0){a.state={status:'sending'};going.set(cid,n-1);continue}going.delete(cid);a.state={status:'sent'};
 if(a.delegate)Object.assign(c,{status:'snoozed',snoozed_until:new Date(Date.now()+3*864e5).toISOString(),resume_status:'prepared',awaiting:JSON.stringify({delegated:true,name:a.to_name})});
 else Object.assign(c,{status:'completed',closed_at:new Date().toISOString()})}}
const state=()=>{settle();return {suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},done_counts:{all:cards.filter(c=>c.status==='completed').length}}};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:[],next:null,total:cards.filter(c=>c.status==='completed').length}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('q')==null?{counts:{}}:{found:[]}));return}
 if(url.pathname==='/api/events'){res.end('[]');return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);
  if(r.action==='confirm_action'){going.set(r.args.suggestion_id,1);res.end('{}');return}
  if(r.action==='revise_draft'){res.end(JSON.stringify({revision:r.args.revision,body:r.args.body}));return}
  res.end(JSON.stringify(r.action==='card_chat'?{session:true,status:'ok',active:false,cursor:'k1',items:[]}:{}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const send=async(page,cid,rev)=>{await page.locator(`#task-${cid} [data-smart="${rev}"]`).click();await page.locator('#send-dialog').waitFor({state:'visible'});await page.locator('#send-confirm').click()};
const toastText=page=>page.locator('#toast.show').textContent();
const palFind=async(page,q,width)=>{if(width<1024)await page.locator('#find-open').click();else await page.keyboard.press('Control+k');await page.locator('#palette #pal-q').waitFor();
 await page.locator('#pal-q').fill(q);await page.waitForFunction(()=>!/Looking…/.test(document.querySelector('#pal-list')?.textContent||''));
 return page.locator('#pal-list').evaluate(l=>{const out=[];let g='';for(const n of l.children){if(n.classList.contains('pal-group'))g=n.textContent;else if(n.classList.contains('pal-item'))out.push([g,n.querySelector('.pal-label').textContent,n.querySelector('small')?.textContent||''])}return out.filter(([g,label])=>g!=='Messages'&&!label.startsWith('See all results'))})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){reset();const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+id(1)).waitFor();
  // Send: while it goes, the usual line; once it went, where it is now
  await send(page,id(1),'aa11bb22cc33');
  await page.waitForFunction(()=>/Moved to/.test(document.querySelector('#toast.show')?.textContent||''),null,{timeout:15000});
  assert.equal(await toastText(page),'Sent. Moved to Done. Open');
  // Open: Done opens on it, and it leads Done though it came in two days ago
  await page.locator('#toast [data-toast-open]').click();
  await page.waitForFunction(i=>document.querySelector('#finished-list')?.open&&document.querySelector('#finished-list #task-'+i),id(1));
  assert.deepEqual(await page.locator('#finished-list article').evaluateAll(n=>n.map(x=>x.id)),['task-'+id(1),'task-'+id(3)]);
  assert.equal(await page.locator(`#finished-list #task-${id(1)} .card-badges .chip`).first().textContent(),'Done just now');
  assert.equal(await page.locator(`#finished-list #task-${id(3)} .card-badges .chip`).first().textContent(),'Done 1 hour ago');
  assert.equal(await page.locator(`#finished-list #task-${id(1)} .meta-side time`).count(),0);  // not "2 days ago", when it came in
  // Handed to someone: in Later until they reply, and the toast says until when
  await send(page,id(2),'dd44ee55ff66');
  await page.waitForFunction(()=>/Later/.test(document.querySelector('#toast.show')?.textContent||''),null,{timeout:15000});
  const day=new Date(Date.now()+3*864e5).toLocaleDateString('en-US',{weekday:'short',timeZone:'Europe/Brussels'});  // the page's time zone, not the runner's
  assert.equal(await toastText(page),`Sent. Moved to Later until ${day}. Open`);
  await page.locator('#toast [data-toast-open]').click();
  await page.waitForFunction(i=>document.querySelector('#later-list')?.open&&document.querySelector('#later-list #task-'+i),id(2));
  assert.match(await page.locator(`#later-list #task-${id(2)}`).innerText(),/Sent to Robin Hale\. Waiting for their reply; it closes when they answer\./);
  // The search finds them by title and by who they went to, done and later alike, each saying where it is
  assert.deepEqual(await palFind(page,'dana',width),[['Done','Send Northfield the editable agreements','Done just now · Work']]);
  await page.keyboard.press('Escape');
  assert.deepEqual(await palFind(page,'robin@studio',width),[['To-dos','Hand the venue booking to Robin','Later · Work']]);
  await page.keyboard.press('Escape');
  assert.deepEqual((await palFind(page,'northfield',width)).slice(0,1),[['Done','Send Northfield the editable agreements','Done just now · Work']]);
  await page.keyboard.press('Escape');
  // The notice is about the to-do that went: it goes when another to-do opens, so it never reads as being about that one
  await send(page,id(5),'ab12cd34ef56');
  await page.waitForFunction(()=>/Moved to Done/.test(document.querySelector('#toast.show')?.textContent||''),null,{timeout:15000});
  await page.evaluate(i=>{location.hash='#chat='+i},id(4));
  await page.waitForFunction(()=>!document.querySelector('#toast.show'),null,{timeout:2000});
  // A send that lands while another to-do is open says nothing over it, and says where it went once that one closes
  await page.evaluate(()=>{location.hash=''});await page.locator('#task-'+id(6)).waitFor();
  await send(page,id(6),'ba21dc43fe65');await page.evaluate(i=>{location.hash='#chat='+i},id(4));
  await page.waitForFunction(()=>!document.querySelector('#toast.show'));
  await page.evaluate(async()=>{await refresh();await refresh()});
  assert.equal(cards.find(c=>c.id===id(6)).status,'completed');
  assert.doesNotMatch(await page.evaluate(()=>document.querySelector('#toast.show')?.textContent||''),/Sent/);
  await page.evaluate(async()=>{location.hash='';await new Promise(r=>setTimeout(r,50));await refresh()});
  await page.waitForFunction(()=>/Moved to Done/.test(document.querySelector('#toast.show')?.textContent||''),null,{timeout:15000});
  assert.equal(await page.locator('#toast [data-toast-open]').getAttribute('data-toast-open'),id(6));
  // Its own to-do opening keeps it
  await page.evaluate(i=>{location.hash='#chat='+i},id(6));await page.waitForFunction(i=>chatId===i,id(6));
  assert.equal(await toastText(page),'Sent. Moved to Done. Open');
  await page.evaluate(()=>{location.hash=''});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('sent where dashboard ok');
