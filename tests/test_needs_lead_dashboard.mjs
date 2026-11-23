import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdir} from 'node:fs/promises';
import {dashboardPage} from './dashboard-page.mjs';
import {waitForAction} from './page-calls.mjs';
const {chromium}=await import('./browser.mjs');

// A result whose run left a need of the owner's and nothing on the to-do that settles it (needs_owner) is not finished:
// Answer leads, question or not, and what they say makes it carry on; Mark done is in sight beside it. A step they settle
// by doing it themselves (owner_step: the to-do's, or the one its run saved) has Mark done lead, and so has a file to read,
// a draft has its send, a link its Open (test_open_link_leads_dashboard.mjs), a teammate's one Check in now. Same rule as
// result_ask() in machine/cards.py. Made-up data. SHOTS=<folder> saves the list at 1440 and 390, light and dark.
const dashboard=await dashboardPage(process.env.PAGE),now=new Date().toISOString();
const todo=(id,title,needs,extra={})=>({id,title,body:'Looked through your mail and the shared folder.',status:'prepared',scope:'work',created_at:now,event_ids:[1],
 outcome:JSON.stringify({state:'needs_you',needs,...extra.outcome}),...(extra.owes===false?{}:{needs_owner:needs}),...extra.row});
const cards=[
 todo('say','Send Kim the insurance papers','confirm which policy covers the new office'),
 todo('ask','Pick a date for the fire drill','Which Thursday suits you best?'),
 todo('errand','Pay the workshop deposit','pay the deposit in your bank',{outcome:{owner_step:true}}),
 todo('visit','Bring the keys to the notary','bring the keys to the notary',{row:{owner_step:1}}),
 todo('read','Compare the two leases','read the comparison',{owes:false,row:{result_files:[{index:0,name:'leases.md',size:10}]}}),
 todo('send','Reply to Noor about the lease','check the draft and send it',{owes:false,row:{next_actions:[{kind:'email',revision:'v1',label:'Send to Noor',to:['noor@example.com'],subject:'Lease',body:'Hi Noor,\n\nThe lease is signed.'}]}}),
 todo('mate','Get the meter readings','confirm the readings',{row:{fleet_handoff:{stage:'asked',name:'Ann Baker'}}}),
 todo('gone','Renew the parking permit','confirm the plate number',{owes:false,row:{handled_hint:JSON.stringify({reason:'It was renewed this morning',event_ids:[],at:now})}})];
const posts=[];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'&&req.method==='POST'){posts.push(JSON.parse(body||'{}'));res.end('{"status":"instructions"}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[],shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){
  posts.length=0;
  const context=await browser.newContext({viewport:{width,height}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-say').waitFor();
  const lead=id=>page.locator(`#task-${id} .actions .primary`).allTextContents();
  const row=id=>page.locator(`#task-${id} .actions > button:not([hidden])`).allTextContents();
  // A statement asks like a question does: never Mark done in front, as if it were finished
  for(const id of ['say','ask']){
   assert.deepEqual(await lead(id),['Answer'],id);
   assert.deepEqual((await row(id)).slice(0,2),['Answer','Mark done'],id);
   assert.equal(await page.locator(`#task-${id} .card-badges .chip`).first().textContent(),'Needs you');
   assert.equal(await page.locator(`#task-${id} [data-choice="complete"]`).count(),1,id);
  }
  // Theirs to do, a file to read, a draft, one a teammate has: their own lead; one handled elsewhere asks nothing
  for(const id of ['errand','visit','read'])assert.deepEqual(await lead(id),['Mark done'],id);
  assert.deepEqual(await lead('send'),['Review and send to Noor']);
  assert.deepEqual(await lead('mate'),['Check in now']);
  for(const id of ['errand','visit','read','send','mate','gone'])assert.equal(await page.locator(`#task-${id} [data-choice="answer"]`).count(),0,id);
  // The row fits, on one line under the lead
  assert.ok(await page.locator('#task-say .actions').evaluate(a=>[...a.children].every(c=>c.getBoundingClientRect().right<=a.closest('article').getBoundingClientRect().right+1)));
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(shots)for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});await page.evaluate(async()=>{for(let i=0;i<2;i++)await new Promise(r=>requestAnimationFrame(r));await Promise.all(document.getAnimations().map(x=>x.finished))});
   await page.screenshot({path:`${shots}/list-${width}-${scheme}.png`,fullPage:true});await page.locator('#task-say').screenshot({path:`${shots}/statement-${width}-${scheme}.png`})}
  await page.emulateMedia({colorScheme:'light'});
  // The answer goes the Change way, so it carries on with it
  await page.locator('#task-say [data-choice="answer"]').click();
  assert.equal(await page.locator('#task-say .answer-editor label').textContent(),'Your answer');
  await page.locator('#feedback-say').fill('The second one, it covers both floors.');await page.locator('#task-say [data-choice="other"]').click();
  const sent=await waitForAction(posts,'decide');
  assert.deepEqual([sent.args.suggestion_id,sent.args.choice,sent.args.feedback],['say','other','The second one, it covers both floors.']);
  // Go through (one tap per to-do) leaves out what waits on an answer
  assert.equal(await page.evaluate(()=>crKind(state.suggestions.find(s=>s.id==='say'))),'');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('needs lead ok');
}finally{await browser?.close();server.close()}
