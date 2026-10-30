import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// To-dos that look done already (a run found it done, or a later message suggests it's handled) don't sit as full
// to-dos between real work: one folded "Look done" group right above Done, a short line each (title and what shows it)
// with Not done and Done, and Mark all done with one line and Undo. Never Overdue, never in the counts. Nothing closes
// without the owner. The sidebar has the same group above Done, folded too.
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
  for(const id of ['d1','d2','h1','h2'])assert.equal(await page.locator('#task-'+id).count(),0,id);
  assert.equal(await page.locator('#badge-inbox').textContent(),'2');
  assert.equal(await page.locator('#task-r1 .chip').filter({hasText:'Overdue'}).count(),1);  // real work can still be late
  // A step still open on someone else's side: nothing is ready for them, so its own folded group, not counted
  assert.equal(await page.locator('#section-ready #task-w1, #suggestions>.section-head~#task-w1').count(),0);
  assert.equal(await page.locator('#waiting-list').evaluate(d=>d.open),false);
  assert.equal(await page.locator('#waiting-head .count').textContent(),'1');
  await page.locator('#waiting-head').click();
  assert.equal(await page.locator('#waiting-list #task-w1 .status-line').textContent().then(x=>x.includes('Waiting on: the hotfix review')),true);
  await page.locator('#waiting-head').click();
  // One folded group right above Done
  const order=await page.locator('#suggestions>details[id]').evaluateAll(d=>d.map(x=>x.id));
  assert.deepEqual(order.slice(-3),['waiting-list','lookdone-list','finished-list']);
  assert.equal(await page.locator('#lookdone-list').evaluate(d=>d.open),false);
  assert.equal(await page.locator('#lookdone-head .count').textContent(),'4');
  await page.locator('#lookdone-head').click();
  const rows=page.locator('#lookdone-list .ld-row');assert.equal(await rows.count(),4);
  const line=id=>page.locator(`[data-ld="${id}"] .ld-why`).textContent();
  assert.equal(await line('d1'),'PR #3451 merged, deployed Oct 27');
  assert.equal(await line('d2'),'Alex already sent it on Monday');
  assert.equal(await line('h1'),'Elif confirmed it herself on Tuesday');
  assert.equal(await page.locator('#lookdone-list').getByText('Overdue').count(),0);
  // A row opens to the full to-do, which is never late either
  await page.locator('[data-ld-expand="h1"]').click();
  assert.equal(await page.locator('#task-h1').isVisible(),true);
  assert.equal(await page.locator('#task-h1 .chip').filter({hasText:'Overdue'}).count(),0);
  // one set of buttons: the row's Not done and Done, not the to-do's own action row too
  assert.equal(await page.locator('#task-h1>.actions').isVisible(),false);
  assert.equal(await page.locator('[data-ld="h1"] .ld-acts').isVisible(),true);
  await page.locator('[data-ld-expand="h1"]').click();assert.equal(await page.locator('#task-h1').count(),0);
  // The sidebar: the same group above Done, folded
  if(width>=1024){const heads=await page.locator('#side-cards .side-head').evaluateAll(b=>b.map(x=>x.dataset.sideFold));
   assert.deepEqual(heads.slice(-3),['waiting','lookdone','done']);
   assert.equal(await page.locator('#side-cards [data-side-fold="waiting"]').getAttribute('aria-expanded'),'false');
   assert.equal(await page.locator('#side-cards [data-side-fold="lookdone"]').getAttribute('aria-expanded'),'false')}
  // Not done: it is a normal to-do again (and the review learns from the decision)
  posts.length=0;await page.locator('[data-ld-not="d1"]').click();await page.locator('#task-d1').waitFor();
  assert.deepEqual(posts.map(p=>[p.suggestion_id,p.choice]),[['d1','not_done']]);
  assert.equal(await page.locator('[data-ld="d1"]').count(),0);
  // Mark all done: one line, with Undo that brings them all back
  posts.length=0;await page.locator('[data-ld-all]').click();
  await page.locator('#toast').getByText('Marked 3 done').waitFor();
  assert.deepEqual(posts.map(p=>p.choice),['complete','complete','complete']);
  assert.equal(await page.locator('#lookdone-list').count(),0);
  posts.length=0;await page.locator('#toast [data-undo]').click();await page.locator('#lookdone-list').waitFor();
  assert.deepEqual(posts.map(p=>p.choice),['undo','undo','undo']);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  // back as it was for the next width
  const d1=cards.find(c=>c.id==='d1');Object.assign(d1,{status:'prepared',outcome:JSON.stringify({state:'already_done'})});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('look done dashboard ok');
