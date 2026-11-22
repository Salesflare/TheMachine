import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A page's first drawing puts the to-dos on screen first: the parts out of sight (Learning, Connections, the other
// tabs, the Updated line, the Done list, Settings' notifications) are drawn just after that first paint, not before it. Then they are all there, and a later
// refresh draws everything at once as before.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[{id:'a1a1a1a1a1a1a1a1',title:'Check the payroll is ready',body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1]},
 {id:'b2b2b2b2b2b2b2b2',title:'Book the room',body:'Booked.',status:'completed',scope:'work',created_at:now,updated_at:now,event_ids:[2]},
 {id:'c3c3c3c3c3c3c3c3',title:'Renew the lease',body:'Next month.',status:'snoozed',snoozed_until:new Date(Date.now()+864e5*3).toISOString(),scope:'work',created_at:now,event_ids:[3]},
 {id:'d4d4d4d4d4d4d4d4',title:'Hear back on the quote',body:'Asked.',status:'prepared',outcome:JSON.stringify({state:'waiting'}),scope:'work',created_at:now,event_ids:[4]},
 // more For you to-dos than a screen shows
 ...Array.from({length:11},(_,i)=>({id:'e5e5e5e5e5e5e5'+String(i).padStart(2,'0'),title:'Answer the note '+i,body:'Drafted.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[10+i]}))];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 // What the page holds when the first to-do comes in, and in the frame after it
 await context.addInitScript(()=>{window.seen=null;new MutationObserver((m,o)=>{if(document.querySelector('#suggestions article.card')){o.disconnect();
  const look=()=>({updated:document.querySelector('#updated')?.textContent||'',done:document.querySelectorAll('#task-b2b2b2b2b2b2b2b2').length,
   later:document.querySelectorAll('#task-c3c3c3c3c3c3c3c3').length,waiting:document.querySelectorAll('#task-d4d4d4d4d4d4d4d4').length,
   foryou:document.querySelectorAll('#suggestions > article.card').length,foryouCount:document.querySelector('#section-foryou .count')?.textContent,
   folds:[...document.querySelectorAll('#later-head .count,#waiting-head .count')].map(c=>c.textContent)});const seen=window.seen={at:look()};requestAnimationFrame(()=>setTimeout(()=>{seen.after=look()},50))}}).observe(document,{childList:true,subtree:true})});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
 await page.waitForFunction(()=>window.seen?.after);
 const seen=await page.evaluate(()=>window.seen);
 assert.doesNotMatch(seen.at.updated,/Updated/,'the to-dos are drawn before the rest: '+JSON.stringify(seen));
 assert.match(seen.after.updated,/Updated/,'the rest follows right after: '+JSON.stringify(seen));
 assert.equal(seen.at.done,0,'the Done list waits for the first paint too');assert.equal(seen.after.done,0,'folded, nor after it');
 // Done opens with its rows at once (its first page, drawn as it opens)
 assert.ok(await page.evaluate(()=>{document.querySelector('#finished-head').click();const r=!!document.querySelector('#finished-list[open] #task-b2b2b2b2b2b2b2b2');document.querySelector('#finished-head').click();return r}),'Done opened, its rows at once');
 // Folded lists show their heads and counts at once; their rows (out of sight) follow right after too
 assert.deepEqual(seen.at.folds,['1','1'],'the folds and their counts are there at once');
 assert.deepEqual([seen.at.later,seen.at.waiting],[0,0],'a folded list\'s rows wait for the first paint');
 assert.deepEqual([seen.after.later,seen.after.waiting],[0,0],'nor after it: they are drawn as the list opens');
 // For you: the first screen's worth at once (its count says all 12), the rest right after, in order
 assert.deepEqual([seen.at.foryou,seen.at.foryouCount],[8,'12'],'the first For you to-dos that fit a screen, and the full count');
 assert.equal(seen.after.foryou,12,'the rest follow right after');
 const order=()=>page.evaluate(()=>[...document.querySelectorAll('#suggestions > article.card')].map(c=>c.id).join());const drawn=await order();
 // opening it draws its rows in the same task as the click: the first frame that shows it open has them
 assert.ok(await page.evaluate(()=>{document.querySelector('#later-head').click();return !!document.querySelector('#later-list[open] #task-c3c3c3c3c3c3c3c3')}),'opened, its rows at once');
 assert.ok(await page.locator('#task-c3c3c3c3c3c3c3c3').isVisible(),'opened, Later shows its to-do');
 // Waiting on others by keyboard (→ on its head) the same
 assert.ok(await page.evaluate(()=>{kbFold(document.querySelector('#waiting-head'),true);return document.querySelector('#waiting-list').open&&document.querySelectorAll('#waiting-list article.card').length>0}),'opened by key, its rows at once');
 // At the very top nothing is held (shell-place.js), so a change there measures nothing: a first draw is all at the top
 const measured=await page.evaluate(()=>{scrollTo(0,0);let n=0;const f=Element.prototype.getBoundingClientRect;Element.prototype.getBoundingClientRect=function(){n++;return f.call(this)};
  try{placeNote()}finally{Element.prototype.getBoundingClientRect=f}return n});
 assert.equal(measured,0,'nothing measured at the top');
 // A refresh after that draws it all at once again
 await page.evaluate(()=>{document.querySelector('#updated').textContent=''});
 await page.evaluate(()=>refresh());
 assert.match(await page.locator('#updated').textContent(),/Updated/,'a refresh draws the rest with the to-dos');
 assert.equal(await order(),drawn,'For you in the same order as a drawing all at once');
 // A reload (the browser takes the page back to where it was, further down) draws For you whole at once
 await page.evaluate(()=>{window.seen=null});await page.reload();await page.waitForFunction(()=>window.seen?.after);
 assert.equal((await page.evaluate(()=>window.seen)).at.foryou,12,'a reload draws all of For you at once');
 // A phone's screen holds fewer: its first drawing has four, the rest right after, in the same order
 await page.setViewportSize({width:390,height:844});await page.evaluate(()=>{window.seen=null});
 await page.goto('http://127.0.0.1:'+server.address().port+'/?phone');await page.waitForFunction(()=>window.seen?.after);
 const phone=await page.evaluate(()=>window.seen);
 assert.deepEqual([phone.at.foryou,phone.at.foryouCount,phone.after.foryou],[4,'12',12],'a phone draws four first: '+JSON.stringify(phone));
 assert.equal(await order(),drawn,'For you in the same order on a phone');
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
