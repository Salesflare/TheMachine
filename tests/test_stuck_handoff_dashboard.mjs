import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do whose run got stuck, then handed to Codex from its chat. While the job runs the server shows its preparation as
// working (agent_jobs.shown_preparation): the chip and the chat's status line both say Working…, never Stuck, and Try
// again goes. Once the job's result is in (handed) nothing runs: never Preparing…, never Stuck. A to-do that is
// still stuck says Stuck in both places.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),since=new Date(Date.now()-288e3).toISOString();
const job={id:'aj_'+'1'.repeat(16),tool:'codex',name:'Codex',place:'local',turns:1,created_at:since,updated_at:since,started_at:since,files:[],links:[],has_diff:false,
 url:'codex://threads/01a16539-9d4a-7d83-9620-9203de5acb75',app_name:'Codex',app:'Open in Codex'};
const cards=[
 {id:'a1a1a1a1a1a1a1a1',title:'Find out why saving the workflow fails',body:'Looked into the error.',status:'prepared',scope:'work',created_at:now,event_ids:[1],
  preparation_status:'working',preparation_error:null,preparation_reason:null,agent_job:{...job,status:'running',progress:'Changed investigation.md'}},
 {id:'b2b2b2b2b2b2b2b2',title:'Check the import log',body:'x',status:'accepted',scope:'work',created_at:now,event_ids:[2],
  preparation_status:'working',preparation_error:null,preparation_reason:null,agent_job:{...job,id:'aj_'+'2'.repeat(16),status:'running'}},
 {id:'c3c3c3c3c3c3c3c3',title:'Fix the export',body:'x',status:'accepted',scope:'work',created_at:now,event_ids:[3],
  preparation_status:'handed',preparation_error:null,preparation_reason:null,agent_job:{...job,id:'aj_'+'3'.repeat(16),status:'result',summary:'Found the cause.',finished_at:now}},
 {id:'d4d4d4d4d4d4d4d4',title:'Order the cable',body:'x',status:'accepted',scope:'work',created_at:now,event_ids:[4],
  preparation_status:'blocked',preparation_reason:'This didn’t finish, also on the second try.',preparation_error:'completion_unconfirmed'}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],
 agent_tools:[{id:'codex',name:'Codex',place:'local'}]});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/agent-jobs'){res.end(JSON.stringify({jobs:Object.fromEntries(cards.filter(c=>c.agent_job).map(c=>[c.id,c.agent_job]))}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'idle',active:false,cursor:'k',items:[{kind:'you',text:'Can Codex look into this?',at:Date.now()-300e3}]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  const context=await browser.newContext({viewport:{width,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
  const card=id=>page.locator('#task-'+id),chip=async id=>(await card(id).locator('.card-badges .chip').first().textContent()).trim();
  // Working while Codex is on it, whether the to-do was prepared before or not; no Try again
  for(const id of ['a1a1a1a1a1a1a1a1','b2b2b2b2b2b2b2b2']){
   assert.equal(await chip(id),'Working…',id);
   assert.equal(await card(id).locator('[data-choice="retry"]').count(),0,id)}
  // The job's result is in: nothing runs, so neither Preparing… nor Stuck
  assert.ok(!['Preparing…','Stuck','Working…'].includes(await chip('c3c3c3c3c3c3c3c3')),await chip('c3c3c3c3c3c3c3c3'));
  // Still stuck, with nothing handed off: Stuck and Try again
  assert.equal(await chip('d4d4d4d4d4d4d4d4'),'Stuck');
  assert.equal(await card('d4d4d4d4d4d4d4d4').locator('[data-choice="retry"]').count(),1);
  // The chat's status line says what the chip says
  for(const [id,want] of [['a1a1a1a1a1a1a1a1','Working…'],['b2b2b2b2b2b2b2b2','Working…'],['c3c3c3c3c3c3c3c3',''],['d4d4d4d4d4d4d4d4','Stuck']]){
   await page.evaluate(id=>{location.hash='chat='+id},id);
   await page.locator(`.chat-layout[data-chat="${id}"] #chat-status`).waitFor({state:'attached'});await page.waitForFunction(()=>document.querySelector('#chat-log .chat-msg,#chat-log .chat-you,#chat-log > *'));
   const status=(await page.locator('#chat-status').textContent()).trim();
   assert.equal(status,want,id);assert.ok(!/Preparing/.test(status),id)}
  await context.close()}
 assert.deepEqual(errors,[])}
finally{await browser?.close();server.close()}
console.log('stuck handoff ok');
