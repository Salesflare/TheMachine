import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Every card leads with one status line under its title: where it stands and what's left to do. A sign that it's
// handled replaces the result's own line, a result that found it already done shows once, "Ready to approve" only
// appears when there is something to approve, and a long body folds to a few lines. Another open card named by its
// title links to it.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString(),long='The run checked every source and wrote down what it found in detail. '.repeat(8);
const hint=reason=>JSON.stringify({reason,event_ids:[9],at:now});
const cards=[
 {id:'d1',title:'Join the product demo with Sam',body:'The demo took place: Sam’s stand-up lists it under Yesterday. Your follow-up is in Test the new build and send feedback.',status:'prepared',early:1,scope:'work',created_at:now,event_ids:[1],
  outcome:JSON.stringify({state:'already_done'}),handled_hint:hint('Sam’s stand-up lists the demo under Yesterday')},
 {id:'f1',title:'Test the new build and send feedback',body:'Try the new build and send Sam your notes.',status:'pending',scope:'work',created_at:now,event_ids:[2]},
 {id:'n1',title:'Answer Kim about the invoice',body:long,status:'prepared',scope:'work',created_at:now,event_ids:[3],
  outcome:JSON.stringify({state:'needs_you',needs:'Give another address for Kim.'}),handled_hint:hint('You replied to Kim and closed the conversation')},
 {id:'a1',title:'Reply to Noor about the contract',body:'Drafted a short reply.',status:'prepared',early:1,scope:'work',created_at:now,event_ids:[4],
  next_actions:[{kind:'email',revision:'v1',label:'Send to Noor',to:['noor@example.com'],to_name:'Noor',subject:'Contract',body:'Hi Noor'}]},
 {id:'q1',title:'Release the mobile apps',body:'I would bump the version, build both apps and submit them for review.',status:'prepared',scope:'work',created_at:now,event_ids:[6],
  outcome:JSON.stringify({state:'answered'}),latest_feedback:{choice:'other',feedback:'What would you do when I tap Do it?',created_at:now}},
 {id:'s1',title:'Reply to Corey about the listings',body:'Adapted the reply.',status:'prepared',scope:'work',created_at:now,event_ids:[7],outcome:JSON.stringify({state:'needs_you',needs:'Approve sending the reply to Corey.'}),
  next_actions:[{kind:'email',revision:'v2',label:'Send',to:['corey@example.com'],subject:'Listings',body:'Hi Corey',state:{status:'sent',sent_at:now}}]},
 {id:'b1',title:'Look up the venue hours',body:'Open 9 to 5 on weekdays.',status:'prepared',early:1,scope:'work',created_at:now,event_ids:[5],outcome:JSON.stringify({state:'done'})}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1280,390]){
  const context=await browser.newContext({viewport:{width,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-d1').waitFor();
  const notes=id=>page.locator(`#task-${id} .note`).evaluateAll(n=>n.map(x=>x.textContent.trim()));
  const text=id=>page.locator('#task-'+id).innerText();
  // Already done: one line, no second "Looks handled", no "approve", and Mark done leads
  assert.deepEqual(await notes('d1'),['Looks done already. Mark it done if that’s right.']);
  for(const gone of ['approve','Nothing was sent','Looks handled'])assert.ok(!(await text('d1')).includes(gone),gone);
  assert.equal(await page.locator('#task-d1 .actions button.primary').first().textContent(),'Mark done');
  assert.equal(await page.locator('#task-d1 [data-result="copy"]').count(),0);assert.equal(await page.locator('#task-a1 [data-result="copy"]').count(),1);
  // The other card, named by its title, links to it
  assert.equal(await page.locator('#task-d1 a.card-link').getAttribute('href'),'#card=f1');
  // The status line sits right under the title, above the body
  assert.equal(await page.locator('#task-d1 h3 + .status-line').count(),1);
  // Handled wins over the result's needs line; the long body folds
  assert.deepEqual(await notes('n1'),['Looks handled: You replied to Kim and closed the conversation']);
  assert.equal(await page.locator('#task-n1 .body.clamp').count(),1);
  assert.equal(await page.locator('#task-n1 button.more').textContent(),'Show more');
  // Prepared ahead with a draft: the one line says nothing goes out until you approve
  assert.deepEqual(await notes('a1'),['Ready to approve. Nothing goes out until you do.']);
  // Once the reply went out, the old needs line is gone; the sent line says it
  assert.ok(!(await text('s1')).includes('Needs you'));
  // Prepared ahead, nothing to approve: no approve line, just finished
  assert.deepEqual(await notes('b1'),['Finished. Mark it done if it looks right.']);
  // Only answered: says nothing is done yet, never Finished, and Do it leads
  assert.deepEqual(await notes('q1'),['Answered. Nothing done yet.']);
  assert.ok(!(await text('q1')).includes('Finished'));
  assert.equal(await page.locator('#task-q1 .actions button.primary').first().textContent(),'Do it');
  // Not needed: Confirm stays full strength while it saves
  {await page.locator('#task-q1 .more-actions>summary').click().catch(()=>{});await page.locator('#task-q1 [data-choice="reject"]').click();
   await page.locator('#dismiss-q1').fill('I release the apps myself.');
   const confirm=page.locator('#task-q1 [data-choice="dismiss-typed"]');
   assert.equal(await confirm.evaluate(e=>getComputedStyle(e).opacity),'1');
   await confirm.evaluate(e=>{e.disabled=true;e.setAttribute('aria-busy','true')});
   assert.equal(await confirm.evaluate(e=>getComputedStyle(e).opacity),'1');
   await page.locator('#task-q1 [data-choice="cancel-dismiss"]').click()}
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.locator('#task-d1').screenshot({path:`/tmp/card-status-${width}.png`});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('card status dashboard ok');
