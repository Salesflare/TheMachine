import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The chat's ⋯ in every state of a to-do: never an empty box. A done one has its Reopen there (and on the status line);
// one that looks done (by its state: an already_done outcome or a handled hint, never its text) is like a done one:
// "Looks done · Reopen", the same menu, and Reopen puts it back on the list (not_done). Mark done stays as the one pick.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),id=n=>String(n).repeat(16),j=JSON.stringify;
const cards=[
 {id:id(1),title:'Pending one',body:'b',status:'pending',scope:'work',created_at:now,event_ids:[1]},
 {id:id(2),title:'Done one',body:'b',status:'completed',scope:'work',created_at:now,event_ids:[2]},
 {id:id(3),title:'Looks done by outcome',body:'b',status:'prepared',outcome:j({state:'already_done'}),scope:'work',created_at:now,event_ids:[3]},
 {id:id(4),title:'Looks done by hint',body:'b',status:'pending',handled_hint:j({reason:'they replied'}),scope:'work',created_at:now,event_ids:[4]},
 {id:id(5),title:'Snoozed one',body:'b',status:'snoozed',snoozed_until:new Date(Date.now()+864e5).toISOString(),scope:'work',created_at:now,event_ids:[5]},
 {id:id(6),title:'Prepared one',body:'b',status:'prepared',outcome:j({state:'done'}),scope:'work',created_at:now,event_ids:[6]},
 {id:id(7),title:'Blocked one',body:'b',status:'accepted',preparation_status:'blocked',preparation_reason:'x',scope:'work',created_at:now,event_ids:[7]},
 {id:id(8),title:'Preparing one',body:'b',status:'accepted',preparation_status:'running',scope:'work',created_at:now,event_ids:[8]},
 {id:id(9),title:'Not needed one',body:'b',status:'rejected',undo_until:new Date(Date.now()+3e5).toISOString(),scope:'work',created_at:now,event_ids:[9]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const decided=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(j(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);
  if(r.action==='card_chat'){res.end(j({session:true,status:'ok',active:false,cursor:'k',items:[{kind:'reply',text:'Done it.',at:Date.now()-60000}]}));return}
  if(r.action==='decide')decided.push([r.args.suggestion_id,r.args.choice])}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
// A condition the page reaches after a request: checked until it holds, for at most 5 s
const until=async(ok,ms=5000)=>{for(const end=Date.now()+ms;!ok();){if(Date.now()>end)return;await new Promise(r=>setTimeout(r,50))}};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1280,390]){
  const context=await browser.newContext({viewport:{width,height:844},locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForTimeout(500);
  // The thread comes from its own request after the title: wait for it (bounded) before reading the ⋯, the status or the picks
  const open=async c=>{await page.evaluate(i=>{location.hash='#chat='+i},c.id);await page.locator('h2.chat-title',{hasText:c.title}).waitFor();
   await page.locator('#chat-log .chat-msg.machine',{hasText:'Done it.'}).first().waitFor({timeout:5000});
   await page.locator('#chat-menu').evaluate(n=>{n.open=false});await page.locator('#chat-menu>summary').click();
   return page.evaluate(()=>({menu:[...document.querySelectorAll('.chat-menu-list>*')].filter(n=>n.getClientRects().length).map(n=>n.textContent.trim()).filter(x=>x!=='All tasks'),
    status:document.querySelector('#chat-status').textContent.trim()}))};
  const at=' at '+width;
  for(const c of cards){const r=await open(c);assert.ok(r.menu.length,'something behind the ⋯ for '+c.title+at)}
  const done=await open(cards[1]);
  assert.deepEqual(done.menu,['Reopen'],'a done to-do: Reopen in the ⋯'+at);assert.equal(done.status,'Done·Reopen','and on the status line'+at);
  for(const c of [cards[2],cards[3]]){const r=await open(c);
   assert.deepEqual(r.menu,done.menu,c.title+': the same ⋯ as a done one'+at);assert.equal(r.status,'Looks done·Reopen',c.title+at);
   await page.locator('#chat-log .chat-options button').first().waitFor({timeout:5000});
   assert.deepEqual(await page.locator('#chat-log .chat-options button').allTextContents(),['Mark done'],c.title+': Mark done is the one pick'+at)}
  const snoozed=await open(cards[4]);assert.equal(snoozed.menu[0],'Unsnooze','the way back first in the ⋯'+at);
  if(width===1280){
   await open(cards[2]);await page.locator('.chat-menu-list [data-ld-not]').click();await until(()=>decided.some(d=>d[0]===id(3)));
   await open(cards[1]);await page.locator('.chat-menu-list [data-choice="reopen"]').click();await until(()=>decided.some(d=>d[0]===id(2)));
   assert.deepEqual(decided.filter(d=>[id(2),id(3)].includes(d[0])),[[id(3),'not_done'],[id(2),'reopen']],'Reopen from the ⋯: not_done for looks done, reopen for done')}
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('chat menu states dashboard ok');
}finally{await browser?.close();server.close()}
