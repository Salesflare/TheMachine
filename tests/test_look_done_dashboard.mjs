import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// To-dos that look done already (a run found it done, or a later message suggests it's handled) don't sit as full
// to-dos between real work, and have no section of their own: they lead Done / dismissed, each like a done one there
// (Looks done for Done, what shows it as its line, Details, Chat, Reopen), and Reopen puts it back on the list. Never Overdue, never in the
// open counts, never closed by themselves. The sidebar has them at the top of Done too.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),late=new Date(Date.now()-3*864e5).toISOString().slice(0,10);
const hint=reason=>JSON.stringify({reason,event_ids:[9],at:now});
const done=(id,title,body,extra={})=>({id,title,body,status:'prepared',scope:'work',created_at:now,event_ids:[1],due:late,outcome:JSON.stringify({state:'already_done'}),...extra});
const cards=[
 {id:'r1',title:'Reply to Noor about the contract',body:'Drafted a short reply.',status:'prepared',scope:'work',created_at:now,event_ids:[4],due:late,
  next_actions:[{kind:'email',revision:'v1',label:'Send to Noor',to:['noor@example.com'],to_name:'Noor',subject:'Contract',body:'Hi Noor'}]},
 done('d1','Fix the signup form error','PR #3451 merged, deployed Oct 27. Nothing is left to do.'),
 done('d2','Send the signed order form','**Alex** already sent it on [Monday](https://example.com/x). It is in the drive.'),
 {id:'h1',title:'Answer Elif about the invoice address',body:'Elif asks where to send the invoice.',status:'pending',scope:'work',created_at:now,event_ids:[2],due:late,handled_hint:hint('Elif confirmed it herself on Tuesday')},
 {id:'h2',title:'Book the venue',body:'Find a venue for the offsite.',status:'prepared',scope:'work',created_at:now,event_ids:[3],handled_hint:hint('The booking confirmation came in')},
 {id:'p1',title:'Decide on the partnership call',body:'They want a call next week.',status:'pending',scope:'work',created_at:now,event_ids:[5]},
 {id:'w1',title:'Hotfix waiting on review',body:'The hotfix PR is open and waits on review.',status:'prepared',scope:'work',created_at:now,event_ids:[7],outcome:JSON.stringify({state:'waiting',waiting_on:'the hotfix review'})},
 {id:'c9',title:'Send the quote',body:'Sent.',status:'completed',scope:'work',created_at:now,event_ids:[6]}];
const posts=[];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'&&req.method==='POST'){const a=JSON.parse(body);if(a.action==='decide'){posts.push(a.args);const c=cards.find(x=>x.id===a.args.suggestion_id);
   if(a.args.choice==='complete'){c.was=c.status;c.status='completed';c.undo_until=new Date(Date.now()+3e5).toISOString()}
   if(a.args.choice==='undo'){c.status=c.was}
   if(a.args.choice==='not_done'){c.handled_hint=null;if(c.status==='prepared'){c.status='pending';c.outcome=null}}
   res.end(JSON.stringify({status:c.status}));return}}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  for(const c of cards){if(c.was){c.status=c.was;delete c.was}}
  const context=await browser.newContext({viewport:{width,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-r1').waitFor();
  // Not between real work, and not counted: Ready has the real one, To decide the real one
  for(const id of ['d1','d2','h1','h2'])assert.equal(await page.locator('#task-'+id+':not(#finished-list>.looks-done)').count(),0,id);
  assert.equal(await page.locator('#badge-inbox').textContent(),'2');
  assert.equal(await page.locator('#task-r1 .chip').filter({hasText:'Overdue'}).count(),1);  // real work can still be late
  // A step still open on someone else's side: nothing is ready for them, so its own folded group, not counted
  assert.equal(await page.locator('#section-ready #task-w1, #suggestions>.section-head~#task-w1').count(),0);
  assert.equal(await page.locator('#waiting-list').evaluate(d=>d.open),false);
  assert.equal(await page.locator('#waiting-head .count').textContent(),'1');
  await page.locator('#waiting-head').click();
  assert.equal(await page.locator('#waiting-list #task-w1 .status-line').textContent().then(x=>x.includes('Waiting on: the hotfix review')),true);
  await page.locator('#waiting-head').click();
  // No group of their own: they lead the folded Done list, counted with it
  const order=await page.locator('#suggestions>details[id]').evaluateAll(d=>d.map(x=>x.id));
  assert.deepEqual(order.slice(-2),['waiting-list','finished-list']);
  assert.equal(await page.locator('#lookdone-list').count(),0);
  assert.equal(await page.locator('#finished-list').evaluate(d=>d.open),false);
  assert.equal(await page.locator('#finished-head .count').textContent(),'5');  // 4 that look done and the done one
  await page.locator('#finished-head').click();
  // Each like a done one there: Looks done where that says Done, what shows it as its line, Details, Chat and Reopen
  const ld=page.locator('#finished-list>article.looks-done');assert.equal(await ld.count(),4);
  assert.deepEqual(await page.locator('#finished-list article').evaluateAll(n=>n.slice(0,5).map(x=>x.id)),['task-d1','task-d2','task-h1','task-h2','task-c9']);
  const card=id=>page.locator('#finished-list #task-'+id);
  assert.equal(await card('d1').locator('.card-badges .chip').first().textContent(),'Looks done');
  assert.equal(await card('c9').locator('.card-badges .chip').first().textContent(),'Done');
  assert.equal(await card('d1').locator('.body').innerText(),'PR #3451 merged, deployed Oct 27');
  assert.equal(await card('d2').locator('.body').innerText(),'Alex already sent it on Monday');
  assert.equal(await card('h1').locator('.body').innerText(),'Elif confirmed it herself on Tuesday');
  assert.equal(await card('h1').evaluate(n=>n.className),await card('c9').evaluate(n=>n.className)+' looks-done');  // the same look
  for(const id of ['d1','h1']){
   assert.deepEqual(await card(id).locator('.actions button').evaluateAll(b=>b.map(x=>x.textContent)),['Reopen']);
   assert.equal(await card(id).locator('.card-chat-link').count(),1);
   await card(id).locator('[data-details]').click();
   assert.deepEqual(await card(id).locator('button:visible').evaluateAll(b=>b.map(x=>x.textContent).filter(x=>/Mark done|Snooze|Not needed|More/.test(x))),[])}
  assert.equal(await page.locator('#finished-list').getByText('Overdue').count(),0);
  // The sidebar: no group of their own, at the top of Done with the tag
  if(width>=1024){const heads=await page.locator('#side-cards .side-head').evaluateAll(b=>b.map(x=>x.dataset.sideFold));
   assert.deepEqual(heads.slice(-2),['waiting','done']);
   assert.equal(await page.locator('#side-cards [data-side-fold="done"] .count').textContent(),'5');
   await page.locator('#side-cards [data-side-fold="done"]').click();
   assert.deepEqual(await page.locator('#side-cards a.side-ld').evaluateAll(a=>a.map(x=>x.getAttribute('href'))),['#chat=d1','#chat=d2','#chat=h1','#chat=h2']);
   assert.equal(await page.locator('#side-cards a.side-ld small').first().textContent(),'Looks done');
   await page.locator('#side-cards [data-side-fold="done"]').click()}
  // Not done: it is a normal to-do again (and the review learns from the decision)
  posts.length=0;await card('d1').locator('[data-ld-not]').click();await page.locator('#task-d1:not(.looks-done)').waitFor();
  assert.deepEqual(posts.map(p=>[p.suggestion_id,p.choice]),[['d1','not_done']]);
  assert.equal(await card('d1').count(),0);
  assert.equal(await page.locator('#badge-inbox').textContent(),'3');
  // nothing else was closed
  assert.equal(await ld.count(),3);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  // back as it was for the next width
  const d1=cards.find(c=>c.id==='d1');Object.assign(d1,{status:'prepared',outcome:JSON.stringify({state:'already_done'})});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('look done dashboard ok');
