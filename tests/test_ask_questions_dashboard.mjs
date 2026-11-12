import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do whose run stopped on several questions: each is answered on its own (its quick picks, or a short field with
// the run's suggestion in it), and one Answer sends them all as one message, a line per question with its answer. One
// left without an answer is marked and nothing goes. The same in the to-do's chat. SHOT_DIR: screenshots at 390 and
// 1440, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),t0=Date.now()-600000;
const one='How many tickets should I order? Last time it was two.',two='Which room should I book? Last time it was Room B.';
const id='b2b2b2b2b2b2b2b2';
const cards=[{id,title:'Order the tickets for the spring workshop',body:'Found last year’s order and the booking form.',status:'instructions',scope:'personal',created_at:now,event_ids:[1],
 preparation_status:'blocked',preparation_reason:'This year’s order needs two details from you.',
 preparation_questions:[{question:one,options:['1','2','3','None']},{question:two,suggestion:'Room B'}]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const history={session:true,status:'blocked',active:false,cursor:'k1',items:[
 {kind:'steps',count:4,steps:[{line:['Read your mail'],n:4}],at:t0+1000}]};
const posts=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'&&req.method==='POST'){const a=JSON.parse(body||'{}');if(a.action==='card_chat'){res.end(JSON.stringify(history));return}posts.push(a);res.end('{"status":"instructions"}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const decided=async page=>{for(let i=0;i<100&&!posts.some(p=>p.action==='decide');i++)await page.waitForTimeout(50);return posts.find(p=>p.action==='decide')};
const fits=page=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth&&[...document.querySelectorAll('.ask-line *')].every(n=>{const r=n.getBoundingClientRect(),b=n.closest('.ask-line').getBoundingClientRect();return !r.width||r.right<=b.right+1}));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  posts.length=0;
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+id).waitFor();
  const card=page.locator('#task-'+id),q=i=>card.locator(`.ask-q[data-q="${i}"]`);
  // Each question its own: picks for the first, a field with the suggestion for the second; Answer under them, once
  assert.deepEqual(await card.locator('.ask-q > p').allTextContents(),[one,two]);
  assert.deepEqual(await q(0).locator('.pick').allTextContents(),['1','2','3','None']);
  assert.equal(await q(0).locator('.ask-field').count(),0);
  assert.equal(await q(1).locator('.ask-field').inputValue(),'Room B');
  assert.equal(await q(1).locator('.pick').count(),0);
  assert.equal(await card.locator('[data-choice="answer"]').count(),0);
  assert.deepEqual(await card.locator('.ask-send button.primary').allTextContents(),['Answer']);
  assert.ok(await fits(page),'nothing runs off the to-do');
  if(process.env.SHOT_DIR)await card.screenshot({path:`${process.env.SHOT_DIR}/ask-questions-${width}-${scheme}.png`});
  // The first without a pick, the second emptied: both marked, nothing sent, the first is where to go
  await q(1).locator('.ask-field').fill('');
  await card.locator('[data-choice="ask-send"]').click();
  assert.deepEqual(await card.locator('.ask-need').allTextContents(),['Needs an answer','Needs an answer']);
  assert.equal(posts.filter(p=>p.action==='decide').length,0);
  assert.equal(await page.evaluate(()=>document.activeElement?.dataset.pick),'1');
  assert.ok(await fits(page),'the marks fit too');
  if(process.env.SHOT_DIR)await card.screenshot({path:`${process.env.SHOT_DIR}/ask-questions-missing-${width}-${scheme}.png`});
  // A pick answers the first (its mark goes); another pick replaces it; typing answers the second
  await q(0).locator('.pick[data-pick="3"]').click();await q(0).locator('.pick[data-pick="2"]').click();
  assert.deepEqual(await q(0).locator('.pick').evaluateAll(b=>b.map(x=>x.getAttribute('aria-pressed'))),['false','true','false','false']);
  assert.equal(await card.locator('.ask-need').count(),1);
  await q(1).locator('.ask-field').fill('Room C');
  assert.equal(await card.locator('.ask-need').count(),0);
  // A redraw keeps both answers
  await page.evaluate(()=>render());
  assert.equal(await q(0).locator('.pick[aria-pressed="true"]').textContent(),'2');
  assert.equal(await q(1).locator('.ask-field').inputValue(),'Room C');
  // Ctrl+Enter in the field sends them all: one message, a line per question with its answer, the Change way
  await q(1).locator('.ask-field').press('Control+Enter');
  const sent=await decided(page);
  assert.deepEqual([sent?.args.suggestion_id,sent?.args.choice,sent?.args.feedback],[id,'other',one+' 2\n'+two+' Room C']);
  assert.ok(!sent.args.decision_id.startsWith('chat-'));
  await page.waitForFunction(()=>/carry on/.test(document.querySelector('#toast')?.textContent||''));
  // In the chat: the same questions, picks and field; Answer sends them as a message of the chat
  posts.length=0;
  await page.goto('http://127.0.0.1:'+server.address().port+'/#chat='+id);
  const ask=page.locator('.chat-ask .ask-line');await ask.waitFor();
  assert.deepEqual(await ask.locator('.ask-q > p').allTextContents(),[one,two]);
  assert.equal(await ask.locator('.ask-field').inputValue(),'Room B');
  await ask.locator('.pick[data-pick="None"]').click();
  assert.equal(await page.locator('#chat-input').inputValue(),'','a pick no longer fills the message box');
  assert.ok(await fits(page),'nothing runs off the chat');
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/ask-questions-chat-${width}-${scheme}.png`});
  await ask.locator('[data-choice="ask-send"]').click();
  const said=await decided(page);
  assert.deepEqual([said?.args.choice,said?.args.feedback],['other',one+' None\n'+two+' Room B']);
  assert.ok(said.args.decision_id.startsWith('chat-'));
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ask questions dashboard ok');
