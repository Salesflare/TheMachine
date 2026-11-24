// A sent message in a to-do's chat, when the to-do stays open for the work it promised: one line says it went, to whom
// and when (the time shows on a phone too), and the to-do's buttons sit under that line, never inside the sent message,
// where Do it read as sending it again. A reply with one of its two messages still to send keeps its buttons as they
// were. Made-up data, a local fixture server, nothing sent. SHOTS=<folder> saves screenshots.
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

const dashboard=await dashboardPage(),t0=Date.now()-600000,now=new Date(t0).toISOString(),sentAt=t0+60000;
const body='Hi Robin,\n\nThanks for the nudge. I’ll check what’s ready and confirm the timing shortly.\n\nSam',other='Hi Casey,\n\nThe dates are in the sheet.\n\nSam';
const mail=(revision,to_name,text,extra)=>({kind:'email',label:'Send to '+to_name,revision,account_id:'mail',from:'sam@acme.example',to:[to_name.toLowerCase()+'@north.example'],to_name,cc:[],bcc:[],subject:'Re: Launch screens',body:text,...extra});
const draft=(to,text)=>({kind:'email',to:[to],subject:'Re: Launch screens',body:text,reply:true});
const OWED='1111111111111111',LIVE='2222222222222222',HALF='3333333333333333';
const base={scope:'work',created_at:now,event_ids:[1]};
const cards=[{...base,id:OWED,title:'Send Robin the launch screens',body:'Replied to Robin on Nov 20. The work is still to do.',status:'pending',next_actions:[]},
 // The same send while its outbox state is still on the to-do
 {...base,id:LIVE,title:'Answer Robin',body:'Drafted a reply.',status:'prepared',next_actions:[mail('r1','Robin',body,{state:{status:'sent',sent_at:new Date(sentAt).toISOString()}})]},
 {...base,id:HALF,title:'Answer Robin and Casey',body:'Drafted two replies.',status:'prepared',outcome:JSON.stringify({state:'needs_you',needs:'Check the two emails and send them'}),
  next_actions:[mail('r1','Robin',body,{state:{status:'sent',sent_at:new Date(sentAt).toISOString()}}),mail('r2','Casey',other)]}];
const asked={kind:'you',text:'Draft a short holding reply',at:t0-5000},wrote={kind:'event',text:'Sent to Robin',sent:body,mine:true,at:sentAt};
const items={[OWED]:[asked,{kind:'reply',text:'A short holding reply to Robin.',drafts:[draft('Robin',body)],at:t0},wrote,{kind:'event',text:'Kept open for the work the reply promised',at:sentAt+1}],
 [LIVE]:[asked,{kind:'reply',text:'A short holding reply to Robin.',drafts:[draft('Robin',body)],at:t0},wrote],
 [HALF]:[asked,{kind:'reply',text:'A reply to each.',drafts:[draft('Robin',body),draft('Casey',other)],at:t0},wrote]};
const errors=[];
const server=createServer(async(req,res)=>{let text='';for await(const c of req)text+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{prepared:2,pending:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(text||'{}');
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'done',active:false,cursor:'k',items:items[r.args.suggestion_id]||[]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/api/')?200:404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme,touch] of [[1440,900,'light',false],[390,844,'dark',true]]){
  const context=await browser.newContext({viewport:{width,height},locale:'en-GB',colorScheme:scheme,hasTouch:touch,isMobile:touch}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+OWED).waitFor();
  const chatOf=async(id,name)=>{await page.evaluate(id=>{location.hash='chat='+id},id);await page.locator('#chat-log .chat-draft').first().waitFor();await page.waitForTimeout(150);
   if(shots)await page.screenshot({path:`${shots}/${name}-${width}.png`})};
  const order=()=>page.locator('#chat-log').evaluate(l=>[...l.children].map(n=>n.matches('.chat-result')?'draft':n.querySelector('.chat-options')?'buttons':n.matches('.chat-event')?n.querySelector('.chat-when')?'sent':'line':'').filter(Boolean));
  const when=await page.evaluate(t=>chatHM(t),sentAt),line=page.locator('#chat-log .chat-event',{hasText:'Sent to'});
  for(const [id,name,want] of [[OWED,'kept-open',['draft','sent','line','buttons']],[LIVE,'live',['draft','sent','buttons']]]){
   await chatOf(id,name);
   assert.deepEqual(await order(),want,name);
   assert.equal(await page.locator('#chat-log .chat-result button:not(.link)').count(),0,'no button in the sent message');
   // One record: sent, to whom, when; the message itself only carries its mark
   assert.equal(await line.count(),1);
   assert.equal((await line.textContent()).trim(),'Sent to Robin · '+when);
   assert.ok(await line.locator('.chat-when').isVisible());
   assert.equal(await page.locator('#chat-log .chat-sendstate').count(),0);
   assert.deepEqual(await page.locator('#chat-log .went-tag').allTextContents(),['Sent']);
  }
  // Nothing taken away: the work left is still Do it, under what was sent
  await chatOf(OWED,'kept-open');
  assert.deepEqual((await page.locator('#chat-log .chat-options button').allTextContents()).map(t=>t.trim()),['Do it','Snooze','Mark done']);
  // Two messages, one still to send: its Send is on it, the buttons don't move
  await chatOf(HALF,'half');
  assert.equal(await page.locator('#chat-log .chat-result [data-smart="r2"]').count(),1);
  assert.equal(await page.locator('#chat-log > .chat-msg > .chat-options').count(),0);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'fits at '+width);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('sent record dashboard ok');
