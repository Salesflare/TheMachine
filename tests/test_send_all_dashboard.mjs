// A to-do whose run prepared two emails (one to each party): the chat's one Send reviews them both, one after the other,
// and its last step sends both, never only the first. Each draft in the chat says Sent only when its own send went:
// one sent and the other not yet (or failed) never shows the other as Sent. A refused second send says how many went and
// Send again sends only the rest. Light and dark, 390 and 1440 wide. Made-up data, a local fixture server, nothing sent.
// SHOTS=<folder> saves screenshots.
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

const dashboard=await dashboardPage();
const now=new Date().toISOString(),t0=Date.now()-600000,sentAt=new Date(t0+120000).toISOString();
const bodyA='Hi Robin!\n\nHere is the invoice for the shared data in October.\n\nSam',bodyB='Hi Casey!\n\nHere is the invoice for the shared data in October.\n\nSam';
const mail=(revision,to,to_name,body)=>({kind:'email',label:'Send to '+to_name,revision,account_id:'mail',from:'sam@acme.example',to,cc:[],bcc:[],subject:'Invoice: shared data October',body,signature:true});
const a=mail('aaaaaaaaaaa1',['robin@north.example'],'Robin',bodyA),b=mail('bbbbbbbbbbb2',['casey@south.example','alex@south.example'],'Casey',bodyB);
const card=(id,title,actions)=>({id,title,body:'Made both invoices and drafted the two emails.',status:'prepared',scope:'work',origin:'owner',created_at:now,event_ids:[1],
 outcome:JSON.stringify({state:'needs_you',needs:'Check the two emails and send them'}),next_action:{kind:'menu',actions},next_actions:actions});
const READY='1111111111111111',HALF='2222222222222222',FAILED='3333333333333333';
const cards=[card(READY,'Send the October invoices',[a,b]),
 // The reported case: the first went, the second has no send yet. It must not read as Sent.
 card(HALF,'Send the September invoices',[{...a,state:{status:'sent',sent_at:sentAt}},b]),
 // The second was tried and refused: Didn't go out, with Try again, never Sent
 card(FAILED,'Send the August invoices',[{...a,state:{status:'sent',sent_at:sentAt}},{...b,state:{status:'failed',error:'The mail server refused it.'}}])];
const draft=x=>({kind:'email',to:x.to,subject:x.subject,body:x.body,reply:false});
const reply={kind:'reply',text:'Both invoices are ready. Two emails, one to each party.',drafts:[draft(a),draft(b)],at:t0};
const items={[READY]:[reply],
 [HALF]:[reply,{kind:'event',text:'Sent to robin@north.example',sent:bodyA,mine:true,at:t0+120000}],
 [FAILED]:[reply,{kind:'event',text:'Sent to robin@north.example',sent:bodyA,mine:true,at:t0+120000},{kind:'event',text:'Didn’t go out to casey@south.example, alex@south.example',mine:false,at:t0+130000}]};
const calls=[],errors=[];let refuse=0;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{prepared:3},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]}}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'done',active:false,cursor:'k',items:items[r.args.suggestion_id]||[]}));return}
  if(r.action==='confirm_action'){calls.push(r.args);if(refuse&&r.args.revision===b.revision){refuse--;res.statusCode=400;res.end(JSON.stringify({error:'The mail server is busy. Try again.'}));return}res.end(JSON.stringify({status:'queued'}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/api/')?200:404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const until=async(page,ok)=>{for(let i=0;i<150&&!ok();i++)await page.waitForTimeout(20)};
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]){
  const context=await browser.newContext({viewport:{width,height},locale:'en-GB',colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+READY).waitFor();
  const name=`${scheme}-${width}`,chatOf=async id=>{await page.evaluate(id=>{location.hash='chat='+id},id);await page.locator('#chat-log .chat-draft').first().waitFor();await page.waitForTimeout(150)};
  // Two drafts ready: one Send under the newest, for both. Neither draft says Sent.
  await chatOf(READY);
  const lead=page.locator('#chat-log .chat-draft.current [data-send-all]');
  assert.equal(await lead.count(),1);assert.equal((await lead.innerText()).trim(),'Review and send 2 emails');
  assert.equal(await page.locator('#chat-log .chat-sendstate.ok, #chat-log .went-tag').count(),0);
  if(shots)await page.screenshot({path:`${shots}/1-chat-two-drafts-${name}.png`});
  // Step 1 of 2: the first email in full, Next. Nothing goes out yet.
  await lead.click();await page.locator('#send-dialog').waitFor({state:'visible'});
  assert.equal(await page.locator('#send-step').innerText(),'1 of 2');
  assert.equal((await page.locator('#send-confirm').innerText()).trim(),'Next');
  assert.ok((await page.locator('#send-head').innerText()).includes('robin@north.example'));
  assert.ok((await page.locator('#send-dialog').innerText()).includes('Hi Robin!'));
  if(shots)await page.screenshot({path:`${shots}/2-confirm-step1-${name}.png`});
  await page.locator('#send-confirm').click();await page.waitForTimeout(100);
  assert.equal(calls.length,0,'Next sends nothing');
  // Step 2 of 2: the second email in full; its Send sends both, in order, each exactly as seen
  assert.equal(await page.locator('#send-step').innerText(),'2 of 2');
  assert.equal((await page.locator('#send-confirm').innerText()).trim(),'Send 2 emails');
  assert.ok((await page.locator('#send-head').innerText()).includes('casey@south.example, alex@south.example'));
  assert.ok((await page.locator('#send-dialog').innerText()).includes('Hi Casey!'));
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'fits at '+width);
  if(shots)await page.screenshot({path:`${shots}/3-confirm-step2-${name}.png`});
  await page.locator('#send-confirm').click();await until(page,()=>calls.length>=2);
  assert.deepEqual(calls.map(c=>[c.suggestion_id,c.revision]),[[READY,a.revision],[READY,b.revision]]);
  assert.notEqual(calls[0].approval_id,calls[1].approval_id);
  await page.locator('#send-dialog').waitFor({state:'hidden'});calls.length=0;
  // Cancel (×) on step 2 sends nothing at all
  await lead.click();await page.locator('#send-confirm').click();await page.locator('#send-dialog [aria-label="Cancel send"]').click();await page.locator('#send-dialog').waitFor({state:'hidden'});await page.waitForTimeout(100);
  assert.equal(calls.length,0);
  // The second refused: says how many went; Send again asks for both again (the server answers the first as the
  // same send, never a second email: Store.confirm_action) and the second goes
  refuse=1;await lead.click();await page.locator('#send-confirm').click();await page.locator('#send-confirm').click();
  await page.waitForFunction(()=>document.querySelector('#send-error').textContent.includes('Sent 1 of 2.'));
  assert.ok((await page.locator('#send-error').innerText()).includes('The mail server is busy.'));
  assert.deepEqual(calls.map(c=>c.revision),[a.revision,b.revision]);
  await page.locator('#send-confirm').click();await until(page,()=>calls.length>=4);await page.locator('#send-dialog').waitFor({state:'hidden'});
  assert.deepEqual(calls.map(c=>c.revision),[a.revision,b.revision,a.revision,b.revision]);calls.length=0;
  // The first went, the second has no send: only the first says Sent; the second is the one to review, alone
  await chatOf(HALF);
  const boxes=page.locator('#chat-log .chat-draft');
  assert.match(await boxes.nth(0).innerText(),/Sent to robin@north\.example by email · \d\d:\d\d/);
  assert.equal(await boxes.nth(1).locator('.chat-sendstate.ok, .went-tag').count(),0,'the unsent email never reads as Sent');
  assert.equal(await page.locator('#chat-log [data-send-all]').count(),0);
  assert.equal(await boxes.nth(1).locator(`[data-smart="${b.revision}"]`).count(),1);
  if(shots)await page.screenshot({path:`${shots}/4-after-one-sent-${name}.png`});
  // The second failed: Didn't go out, never Sent; the event lines name each recipient
  await chatOf(FAILED);
  assert.match(await boxes.nth(0).innerText(),/Sent to robin@north\.example by email · \d\d:\d\d/);
  assert.equal(await boxes.nth(1).locator('.chat-sendstate.ok').count(),0);
  assert.match(await boxes.nth(1).innerText(),/Didn’t go out\. The mail server refused it\./);
  const log=await page.locator('#chat-log').innerText();
  assert.ok(log.includes('Sent to robin@north.example')&&log.includes('Didn’t go out to casey@south.example, alex@south.example'));
  if(shots)await page.screenshot({path:`${shots}/5-after-second-failed-${name}.png`});
  if(process.env.VERBOSE)console.log('ok at',name);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('send all dashboard ok');
