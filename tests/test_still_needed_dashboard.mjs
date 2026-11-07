import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Still needed? on the dashboard (dashboard/todos-rows.js, still_needed.py): a to-do untouched for a week asks once
// with Not needed and Keep, on the to-do and in its chat. Not needed is the to-do's own (with Undo), Keep posts recap_decide. One with
// no answer for another week sits folded in Coming back later, under its own heading, and leaves the open lists. Made up.
const dashboard=await dashboardPage();
const day=864e5,at=n=>new Date(Date.now()-n*day).toISOString(),posts=[];
const ASK='a1'.repeat(8),FOLD='b2'.repeat(8),FRESH='c3'.repeat(8),SNOOZE='d4'.repeat(8);
let cards;
const reset=()=>{cards=[
 {id:ASK,title:'Send Ayla the quote',body:'She asked for the annual price.',status:'pending',scope:'work',created_at:at(9),event_ids:[1],still_needed:{id:'sn_ask',since:at(9),folded:false}},
 {id:FOLD,title:'Pick a paint color for the hallway',body:'Before the painter comes.',status:'pending',scope:'personal',created_at:at(16),event_ids:[2],still_needed:{id:'sn_fold',since:at(16),folded:true}},
 {id:FRESH,title:'Book the venue',body:'',status:'pending',scope:'work',created_at:at(1),event_ids:[3]},
 {id:'e5'.repeat(8),title:'Order the badges',body:'',status:'pending',scope:'work',created_at:at(10),event_ids:[5],still_needed:{id:'sn_seen',since:at(1),folded:false}},
 {id:SNOOZE,title:'Review the redlines',body:'',status:'snoozed',scope:'work',created_at:at(2),snoozed_until:new Date(Date.now()+2*day).toISOString(),event_ids:[4]}]};
reset();
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='recap_decide'){const c=cards.find(x=>x.still_needed?.id===b.args.id);if(c)delete c.still_needed;res.end(JSON.stringify({status:'kept'}));return}
  if(b.action==='decide'){const c=cards.find(x=>x.id===b.args.suggestion_id);if(c&&b.args.choice==='reject')c.status='rejected';res.end(JSON.stringify({status:c?.status}));return}
  if(b.action==='card_chat'){res.end(JSON.stringify({session:false,active:false,status:null,items:[],cursor:null}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const sent=name=>posts.filter(p=>p.action===name);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  posts.length=0;reset();
  const context=await browser.newContext({viewport:{width,height:900},timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+ASK).waitFor();
  // The question on the to-do untouched for a week, and on no other
  const q=page.locator('#task-'+ASK+' .still-needed');
  assert.match((await q.innerText()).replace(/\s+/g,' '),/^Still needed\? Untouched for 9 days Not needed Keep$/);
  assert.equal(await page.locator('#task-'+FRESH+' .still-needed').count(),0);
  // Touched since it asked (opened, say): the question stays, without the untouched days
  assert.match((await page.locator('#task-'+'e5'.repeat(8)+' .still-needed').innerText()).replace(/\s+/g,' '),/^Still needed\? Not needed Keep$/);
  if(width<600){const box=await page.locator('#task-'+ASK).boundingBox(),qb=await q.boundingBox();assert.ok(qb.x+qb.width<=box.x+box.width+1,'it fits the to-do at phone width')}
  // No answer for another week: out of the open lists, folded in Coming back later under its own heading, still asking
  const open=await page.locator('#suggestions>article[id], #suggestions>.section-head~article[id]').evaluateAll(n=>n.map(x=>x.id));
  assert.ok(!open.includes('task-'+FOLD),'not among the open to-dos');
  const later=page.locator('#later-list');assert.equal(await later.getAttribute('open'),null,'folded');
  assert.match(await page.locator('#later-head').innerText(),/2$/);
  await page.locator('#later-head').click();
  assert.deepEqual(await later.locator('.day-head').evaluateAll(n=>n.map(x=>x.textContent)),[await later.locator('.day-head').first().innerText(),'Still needed?']);
  const order=await later.locator('article[id]').evaluateAll(n=>n.map(x=>x.id));assert.deepEqual(order,['task-'+SNOOZE,'task-'+FOLD],'after the snoozed ones');
  assert.equal(await page.locator('#task-'+FOLD+' .still-needed').count(),1);
  // Keep: recap_decide on its question, and it asks no more
  await page.locator('#task-'+ASK+' [data-still="keep"]').click();await q.waitFor({state:'detached'});
  assert.deepEqual(sent('recap_decide').map(({decision_id,...p})=>p),[{action:'recap_decide',id:'sn_ask',choice:'keep'}]);
  await page.getByText('Kept',{exact:true}).waitFor();
  // Not needed: the dashboard's own Not needed, with its Undo
  await page.locator('#task-'+FOLD+' [data-still="drop"]').click();
  await page.waitForFunction(()=>document.querySelector('#toast')?.textContent.includes('Marked not needed'));
  assert.deepEqual(sent('decide').map(p=>[p.suggestion_id,p.choice,p.feedback]),[[FOLD,'reject','No longer needed']]);
  assert.equal(await page.locator('#toast [data-undo]').count(),1);
  // In the to-do's chat the same question shows
  reset();await page.evaluate(()=>refresh());await page.evaluate(id=>{location.hash='chat='+id},ASK);
  await page.locator('#chat-log').waitFor();await page.locator('.chat-panel .still-needed').first().waitFor();
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('still needed dashboard ok');
}finally{await browser?.close();server.close()}
