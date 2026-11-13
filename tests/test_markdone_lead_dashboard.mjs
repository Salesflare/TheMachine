import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do with nothing left to lead (every row of a cleanup decided, a send already out, a result to take in) has Mark
// done as its lead, in sight on the to-do, never only in the … beside a lone Snooze (todos-cards.js cardActions). A
// cleanup with every row decided also stops saying "Needs you" and "Pick …": it reads like any finished result.
// While something still waits (a pick, a row being worked on, a prepared send), Mark done doesn't lead.
const dashboard=await dashboardPage(),now=new Date().toISOString();
const row=(n,state,extra={})=>({n,from:'Sender '+n,address:`s${n}@example.com`,title:'Issue '+n,count:1,state,...extra});
const PICK='Pick Keep or Unsubscribe for each one, then confirm. Nothing changes before that.';
const cleanup=(id,items)=>({id,title:items.length+' newsletters: keep or unsubscribe?',status:'pending',scope:'personal',created_at:now,event_ids:[1],body:PICK+'\n\n- Sender 1: Issue 1',
 cleanup:{kind:'newsletters',items}});
const cards=[
 cleanup('cl-done',[row(1,'kept'),row(2,'done',{how:'one_click'}),row(3,'yours',{link:'https://lists.example/unsubscribe'})]),
 cleanup('cl-open',[row(1,'open',{plan:'one_click'}),row(2,'kept')]),
 cleanup('cl-work',[row(1,'working'),row(2,'kept')]),
 {id:'sent',title:'Reply about the listings',body:'Sent the reply.',status:'prepared',scope:'work',created_at:now,event_ids:[2],outcome:JSON.stringify({state:'done'}),
  next_actions:[{kind:'email',revision:'v1',label:'Send',to:['a@example.com'],subject:'Listings',body:'Hi',state:{status:'sent',sent_at:now}}]},
 {id:'sending',title:'Reply about the invoice',body:'Sending the reply.',status:'prepared',scope:'work',created_at:now,event_ids:[3],
  next_actions:[{kind:'email',revision:'v2',label:'Send',to:['b@example.com'],subject:'Invoice',body:'Hi',state:{status:'sending'}}]},
 {id:'res',title:'Look up the venue hours',body:'Open 9 to 5 on weekdays.',status:'prepared',scope:'work',created_at:now,event_ids:[4],outcome:JSON.stringify({state:'done'})},
 {id:'pend',title:'Book the dentist',body:'Find a slot next week.',status:'pending',scope:'personal',created_at:now,event_ids:[5]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  const context=await browser.newContext({viewport:{width,height:900},...(width<500?{isMobile:true,hasTouch:true}:{})});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#todos');
  await page.locator('#task-cl-done .cl-row').first().waitFor();
  const card=id=>page.locator('#task-'+id);
  const lead=async id=>(await card(id).locator('.actions').first().locator(':scope>button.primary,:scope>a.primary').allInnerTexts()).map(x=>x.trim());
  const menu=async id=>(await card(id).locator('.more-menu [data-choice]').evaluateAll(b=>b.map(x=>x.dataset.choice)));
  const why=`at ${width}`;
  // Nothing left to lead: Mark done leads, in sight, and isn't in the … as well
  for(const id of ['cl-done','sent','res']){
   assert.deepEqual(await lead(id),['Mark done'],`${id}: Mark done leads ${why}`);
   assert.ok(!(await menu(id)).includes('complete'),`${id}: Mark done is not only in the … ${why}`)}
  // Every row decided: the finished line, no "Needs you" and no "Pick …"
  const done=card('cl-done');
  assert.equal((await done.locator('.status-line').innerText()).trim(),'Finished. Mark it done if it looks right.');
  assert.equal(await done.locator('.cl-lead').count(),0,'no "Pick …" once every row is decided');
  assert.ok(!(await done.locator('.card-badges').innerText()).includes('Needs you'),'no Needs you once every row is decided');
  assert.equal(await done.getAttribute('class').then(c=>/\bt-amber\b/.test(c)),false,'it no longer looks like it needs the owner');
  // Still waiting on something: Mark done doesn't lead
  assert.deepEqual(await lead('cl-open'),[],'a pick still open: the cleanup’s own confirm leads, in its box');
  assert.equal(await card('cl-open').locator('.cl-lead').innerText(),PICK);
  assert.ok((await card('cl-open').locator('.card-badges').innerText()).includes('Needs you'));
  assert.equal(await card('cl-open').locator('.status-line').count(),0);
  assert.deepEqual(await lead('cl-work'),[],'a row being worked on: nothing to mark done yet');
  assert.ok(!(await lead('sending')).includes('Mark done'),'a send on its way: Mark done doesn’t lead');
  assert.deepEqual(await lead('pend'),['Do it'],'a decision: Do it leads');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('mark done lead dashboard ok');
}finally{await browser?.close();server.close()}
