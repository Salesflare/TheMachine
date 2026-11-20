// A Teams chat reply on a to-do (teams_send.py): Send opens a dialog that says who it goes to, Send now confirms that
// revision only, and a sent to-do says "Teams message sent". Made-up data, a local fixture server, nothing sent.
// 390 and 1440; SHOT_DIR=<folder> saves screenshots.
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
import {waitForAction} from './page-calls.mjs';
const {chromium}=await import('./browser.mjs');

const dashboard=await dashboardPage();
const sid='1234567890abcdef',done='0011223344556677',revision='1234567890ab';
const body='Yes, the quote goes out by noon today.';
const reply={kind:'teams',label:'Send',revision,account_id:'teams',chat_id:'19:a1b2c3@unq.gbl.spaces',to_name:'Sam Sender',max_length:8000,body};
const sentReply={...reply,revision:'555555555555',state:{status:'sent',message_id:'teams:19:a1b2c3@unq.gbl.spaces:m2',sent_at:new Date().toISOString()}};
const card=(id,title,a,extra={})=>({id,title,body:'Drafted the reply.',status:'prepared',event_ids:[1],next_action:a,next_actions:[a],
  outcome:JSON.stringify({state:'needs_you',needs:'Check the reply and send it'}),scope:'work',created_at:new Date().toISOString(),...extra});
const state=()=>({suggestions:[card(sid,'Answer Sam about the quote',reply),card(done,'Sam asked about the deck',sentReply,{status:'completed',outcome:null})],
  connectors:[],suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]});
const calls=[],errors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){let b='';for await(const c of req)b+=c;calls.push(JSON.parse(b));res.end(JSON.stringify({status:'queued'}));return}
 res.end(url.pathname==='/api/events'?'[]':'{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOT_DIR;if(shots)await mkdir(shots,{recursive:true});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440]){
  const context=await browser.newContext({viewport:{width,height:900}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.evaluate(()=>refresh());
  const task=page.locator(`#task-${sid}`);
  await task.waitFor();
  assert.equal(await task.locator('.draft .db').textContent(),body);
  if(shots)await task.screenshot({path:`${shots}/teams-todo-${width}.png`});
  // Send opens the review: to whom and the exact text. Nothing goes out before Send now.
  await task.locator(`[data-smart="${revision}"]`).click();
  await page.locator('#send-dialog').waitFor({state:'visible'});
  assert.equal(await page.locator('#send-title').textContent(),'Send this Teams message?');
  assert.equal(await page.locator('#send-preview').textContent(),body);
  assert.ok((await page.locator('#send-head').textContent()).includes('Sam Sender'));
  assert.ok(await page.locator('#send-subject-label').isHidden());
  assert.equal(calls.filter(c=>c.action==='confirm_action').length,0);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll at '+width);
  if(shots)await page.locator('#send-dialog').screenshot({path:`${shots}/teams-send-dialog-${width}.png`});
  await page.locator('#send-confirm').click();
  const confirm=await waitForAction(calls,'confirm_action');
  assert.equal(confirm.args.suggestion_id,sid);assert.equal(confirm.args.revision,revision);
  calls.length=0;
  // A sent one says where it went, without "You"
  await page.evaluate(()=>{const d=$('#finished-list');if(d&&!d.open){d.open=true;listShow(d)}});
  const text=await page.locator(`#task-${done}`).evaluate(n=>n.textContent);
  assert.match(text,/Teams message sent/);
  assert.ok(!/\bYou (sent|replied|posted)/.test(text));
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('ok');
}finally{await browser?.close();server.close()}
