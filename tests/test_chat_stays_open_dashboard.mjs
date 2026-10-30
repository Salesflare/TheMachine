import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// An open to-do chat stays open while its to-do moves: a message to a paused job, Do it, a message that restarts a
// done one. Each moves the to-do to Preparing with a job that starts shortly, and the chat follows it there (its
// status line says Preparing) instead of the page jumping back to the lists. Only a link or a step back closes the
// chat, never a refresh (also not a voice turn's): the Browser pane left through the to-do's own row in the sidebar keeps the chat's address, and
// an address that lost the link on the way gets it back. Suggestions in the sidebar still goes back to the lists.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),t0=Date.now()-60000;
const cards=[
 {id:'a1a1a1a1a1a1a1a1',title:'Check the payroll is ready',body:'Paused.',status:'prepared',preparation_status:'ok',browser_open:true,scope:'work',created_at:now,event_ids:[1]},
 {id:'b2b2b2b2b2b2b2b2',title:'Renew the passport',body:'It runs out in May.',status:'pending',scope:'personal',created_at:now,event_ids:[2]},
 {id:'c3c3c3c3c3c3c3c3',title:'Book the venue',body:'Booked.',status:'completed',scope:'work',created_at:now,event_ids:[3]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]},browser_link:'https://cp.example/open?to=browser',browser_embed:'/browser/'});
const decided=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/browser/'){res.setHeader('Content-Type','text/html');res.end('<body><p id="viewer">viewer</p></body>');return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body),c=cards.find(x=>x.id===r.args?.suggestion_id);
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k',items:[
   {kind:'reply',text:'Blocked on the sign-in. The login tab is open; sign in there.',at:t0},{kind:'reply',text:'Paused. Go ahead, I’m listening.',at:t0+1000}]}));return}
  // The Machine's answer to each: the to-do moves to Preparing with a job queued
  if(r.action==='decide'){decided.push([c.id,r.args.choice]);if(r.args.choice==='reopen')Object.assign(c,{status:'prepared'});
   else Object.assign(c,{status:r.args.choice==='accept'?'accepted':'instructions',preparation_status:'queued'});res.end(JSON.stringify({status:c.status}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
 const hash=()=>new URL(page.url()).hash;
 const open=async id=>{await page.locator(`#task-${id} .card-foot a.card-chat-link`).click();await page.locator(`.chat-layout[data-chat="${id}"] #chat-log .chat-msg`).first().waitFor()};
 // Still on the chat a while after the change: the refreshes and polls that follow it never take the page away
 const stays=async(id,why)=>{for(let n=0;n<3;n++){await page.waitForTimeout(700);
  assert.equal(await page.locator(`.chat-layout[data-chat="${id}"]`).count(),1,why+': the chat is still open');
  assert.equal(await page.locator('#suggestions article.card').count(),0,why+': no lists instead');
  assert.equal(hash(),'#chat='+id,why+': the address names the chat')}
  assert.match(await page.locator('.chat-status').textContent(),/Preparing/,why+': the chat shows the job that starts')};
 const send=async text=>{await page.locator('#chat-input').fill(text);await page.locator('[data-chat-send]').click()};

 // 1. The job asked for a sign-in: the Browser pane from the chat, back through the to-do's row in the sidebar, then a
 // long message to the paused job (typed while the box has focus, so no refresh runs in between)
 await open('a1a1a1a1a1a1a1a1');
 await page.locator('#chat-log [data-browser-show]').click();await page.locator('#browser-pane').waitFor();
 assert.equal(hash(),'#browser');
 await page.locator('#side-cards a[href="#chat=a1a1a1a1a1a1a1a1"]').click();
 await page.locator('#browser-pane').waitFor({state:'hidden'});
 assert.equal(hash(),'#chat=a1a1a1a1a1a1a1a1','back on the chat, its address is the chat’s again');
 await send('Every last working day I do the payroll. Go ahead and enter the vacation days; I’ll watch.');
 await stays('a1a1a1a1a1a1a1a1','a message to a paused job');
 assert.deepEqual(decided.at(-1),['a1a1a1a1a1a1a1a1','other']);

 // 2. Do it from the chat, after something took the chat's link off the address
 await page.locator('#side-cards a[href="#chat=b2b2b2b2b2b2b2b2"]').click();await page.locator('.chat-layout[data-chat="b2b2b2b2b2b2b2b2"]').waitFor();
 await page.evaluate(()=>history.replaceState(null,'',location.pathname));
 await page.locator('.chat-layout [data-choice="accept"]').first().click();
 await stays('b2b2b2b2b2b2b2b2','Do it');
 assert.deepEqual(decided.at(-1),['b2b2b2b2b2b2b2b2','accept']);

 // 3. A message on a done to-do reopens it and starts a job
 await page.locator('[data-side-fold="done"]').click();
 await page.locator('#side-cards a[href="#chat=c3c3c3c3c3c3c3c3"]').click();await page.locator('.chat-layout[data-chat="c3c3c3c3c3c3c3c3"]').waitFor();
 await page.evaluate(()=>history.replaceState(null,'',location.pathname));
 await send('Check it once more, the date moved.');
 await stays('c3c3c3c3c3c3c3c3','a message that restarts a job');
 assert.deepEqual(decided.slice(-2),[['c3c3c3c3c3c3c3c3','reopen'],['c3c3c3c3c3c3c3c3','other']]);

 // 4. A reply that offers to wrap up (Mark done, Snooze, Not needed) after a voice turn that added a new to-do and
 // started it: the page's refreshes keep the chat it is on
 cards.push({id:'d4d4d4d4d4d4d4d4',title:'Write down the payroll steps',body:'Added by voice.',status:'accepted',preparation_status:'queued',scope:'work',created_at:now,event_ids:[4]});
 Object.assign(cards[2],{status:'prepared',preparation_status:'ok'});
 await page.evaluate(()=>history.replaceState(null,'',location.pathname));
 await page.evaluate(()=>refresh());
 for(let n=0;n<2;n++){await page.waitForTimeout(500);assert.equal(await page.locator('.chat-layout[data-chat="c3c3c3c3c3c3c3c3"]').count(),1,'a voice turn keeps the chat');assert.equal(hash(),'#chat=c3c3c3c3c3c3c3c3')}
 assert.ok(await page.locator('.chat-layout [data-choice="complete"]').count()>0,'its wrap-up buttons show in the chat');

 // 5. Suggestions in the sidebar still leaves the chat for the lists, from the chat and from the Browser pane over it
 await page.locator('nav [data-tab="inbox"]').click();
 await page.locator('#task-c3c3c3c3c3c3c3c3').waitFor();
 assert.equal(await page.locator('.chat-layout').count(),0);assert.equal(hash(),'');
 await page.locator('#side-cards a[href="#chat=a1a1a1a1a1a1a1a1"]').click();await page.locator('.chat-layout[data-chat="a1a1a1a1a1a1a1a1"] #chat-log .chat-msg').first().waitFor();
 await page.locator('#chat-log [data-browser-show]').click();await page.locator('#browser-pane').waitFor();
 await page.locator('nav [data-tab="inbox"]').click();
 await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
 assert.equal(await page.locator('.chat-layout').count(),0);assert.equal(hash(),'');
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
