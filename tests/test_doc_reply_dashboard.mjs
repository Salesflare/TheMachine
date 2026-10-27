// A doc comment reply on a card, and the Docs connection card: Review and post opens a dialog that says whose comment
// and which doc, Post now confirms that revision only, a posted card says "Reply posted in the doc", and the Docs card
// says what it reads and asks for its own consent. Synthetic data, a local fixture server, nothing posted.
import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const sid='1234567890abcdef',done='0011223344556677',revision='1234567890ab';
const body='Yes, renewals before December keep the old seat price. I will add it to section 3.';
const reply={kind:'doc_reply',label:'Post reply',revision,account_id:'docs',comment_id:'c1',file_id:'f1',to_name:'Casey Customer',doc_title:'Q4 pricing',max_length:4000,body};
const sentReply={...reply,revision:'555555555555',state:{status:'sent',message_id:'doc:c1:r2',sent_at:new Date().toISOString()}};
const docs=(extra)=>({id:'docs',display_name:'Work docs',service:'docs',transport:'broker',boundary:'work',events:3,recent_events:3,last_success:new Date().toISOString(),docs_provider:'google',docs_replies:true,...extra});
let connectors=[docs()];
const card=(id,title,a,extra={})=>({id,title,body:'Drafted the reply.',status:'prepared',event_ids:[1],next_action:a,next_actions:[a],
  outcome:JSON.stringify({state:'needs_you',needs:'Check the reply and send it'}),scope:'work',created_at:new Date().toISOString(),...extra});
const state=()=>({suggestions:[card(sid,'Answer Casey on Q4 pricing',reply),card(done,'Casey asked about the trial',sentReply,{status:'completed',outcome:null})],
  connectors,suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]});
const calls=[],errors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){let b='';for await(const c of req)b+=c;const call=JSON.parse(b);calls.push(call);res.end(JSON.stringify({status:'queued'}));return}
 res.statusCode=url.pathname.startsWith('/api/')?200:404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOT_DIR;if(shots)await mkdir(shots,{recursive:true});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [320,390,1280]){
  const context=await browser.newContext({viewport:{width,height:900}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.evaluate(()=>refresh());
  const task=page.locator(`#task-${sid}`);
  await task.waitFor();
  // The card shows the exact reply
  assert.equal(await task.locator('.draft .db').textContent(),body);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll at '+width);
  if(shots)await task.screenshot({path:`${shots}/reply-card-${width}.png`});
  // Send opens the review: to whom, as whom, the exact text. Nothing goes out before Send now.
  await task.locator(`[data-smart="${revision}"]`).click();
  await page.locator('#send-dialog').waitFor({state:'visible'});
  assert.equal(await task.locator(`[data-smart="${revision}"]`).count(),1);
  assert.equal(await page.locator('#send-title').textContent(),'Post this reply in the doc?');
  assert.equal(await page.locator('#send-confirm').textContent(),'Post now');
  assert.equal(await page.locator('#send-preview').textContent(),body);
  const head=await page.locator('#send-head').textContent();
  assert.ok(head.includes('Casey Customer')&&head.includes('Q4 pricing'),head);
  assert.ok(await page.locator('#send-subject-label').isHidden());
  assert.equal(calls.filter(c=>c.action==='confirm_action').length,0);
  if(shots)await page.locator('#send-dialog').screenshot({path:`${shots}/reply-dialog-${width}.png`});
  await page.locator('#send-confirm').click();
  for(let i=0;i<100&&!calls.some(c=>c.action==='confirm_action');i++)await page.waitForTimeout(20);
  const confirm=calls.find(c=>c.action==='confirm_action');
  assert.equal(confirm.args.suggestion_id,sid);assert.equal(confirm.args.revision,revision);
  calls.length=0;
  // A posted reply says where it went, without "You"
  const sent=page.locator(`#task-${done}`);
  const text=await sent.evaluate(n=>n.textContent);
  assert.match(text,/Reply posted in the doc( at \d\d:\d\d)?\./);
  assert.ok(!/\bYou (sent|replied|posted)/.test(text));
  // The Docs card: what it reads and writes, then the consent it waits for
  await page.evaluate(()=>document.querySelector('nav [data-tab="health"]').click());
  await page.evaluate(()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.textContent.trim()==='Other sources')?.click());
  let health=await page.locator('#health, main').first().textContent();
  assert.ok(health.includes('Posts a reply only after you press Post.'),'docs card copy');
  connectors=[docs({error:'docs_not_connected',docs_replies:false,connect_name:'docs'})];
  await page.evaluate(()=>refresh());await page.waitForTimeout(200);
  health=await page.locator('#health, main').first().textContent();
  assert.ok(health.includes('Waiting for your OK to read docs')&&health.includes('Connect Google Docs')&&health.includes('Never writes.'),'docs consent');
  connectors=[docs({error:'docs_not_connected',docs_provider:'microsoft',docs_replies:false,connect_name:'docs'})];
  await page.evaluate(()=>refresh());await page.waitForTimeout(200);
  health=await page.locator('#health, main').first().textContent();
  assert.ok(health.includes('Connect Microsoft documents')&&health.includes('Replies stay drafts'),'microsoft docs');
  connectors=[docs()];
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
