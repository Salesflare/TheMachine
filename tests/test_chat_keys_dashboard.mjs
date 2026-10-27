import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Every way to send in a chat sends the message the same way: Enter, Ctrl+Enter, Cmd+Enter and the Send button each
// post the text (decide other), show it as a bubble and empty the box, also while a reply runs (steering). Shift+Enter
// is a new line. Ctrl+Enter used to fall through to the page-wide shortcut, which clicked the card's Do it under the
// chat: the Machine started working while the text stayed in the box and no bubble showed. On a phone Enter is a new
// line and Ctrl+Enter (a keyboard on a tablet) still sends. The Help chat asks on Enter and Ctrl+Enter too.
// SHOT_DIR=<folder> also saves screenshots; DASHBOARD=<file> runs another dashboard.html (for before shots).
const dashboard=await readFile(process.env.DASHBOARD||new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString(),t0=Date.now()-60000,ID='c1c1c1c1c1c1c1c1',BUSY='c2c2c2c2c2c2c2c2';
let cards,said,running,actions;
const reset=()=>{cards=[{id:ID,title:'Prepare for the demo with the venue',body:'Thursday at 14:00. They want to see reminders.',status:'pending',scope:'work',created_at:now,event_ids:[1]},
 {id:BUSY,title:'Reply to the venue about the dates',body:'They asked for a date.',status:'instructions',scope:'work',created_at:now,event_ids:[2],preparation_status:'running'}];
 said={[ID]:[],[BUSY]:[{kind:'you',text:'Draft a reply that says Tuesday works',at:t0}]};running=true;actions=[]};
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);const id=r.args?.suggestion_id;
  if(r.action==='card_chat'){const busy=id===BUSY&&running;res.end(JSON.stringify({session:said[id]?.length>0,status:busy?'running':'blocked',active:busy,cursor:null,items:said[id]||[],live:busy?{text:'Here is a reply: Hi Sam'}:null}));return}
  if(r.action==='chat_stop'){running=false;res.end('{"stopped":true}');return}
  if(r.action==='decide'){const c=cards.find(x=>x.id===id);if(r.args.choice==='other'){said[id].push({kind:'you',text:r.args.feedback,at:Date.now()})}else c.status='accepted';res.end(JSON.stringify({status:c.status}));return}
  if(r.action==='help_ask'){res.end(JSON.stringify({answer:'Press Snooze.',sources:[]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const decides=()=>actions.filter(a=>a.action==='decide');
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,tag] of [[1440,900,'desktop'],[1440,700,'short'],[390,844,'phone']]){
  const phone=tag==='phone';
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',hasTouch:phone,isMobile:phone});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const shot=async n=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/${n}-${tag}.png`})};
  const open=async id=>{await page.goto('http://127.0.0.1:'+server.address().port+'/#chat='+id);await page.locator('#chat-input').waitFor();await page.waitForTimeout(400)};
  const bubbles=()=>page.locator('#chat-log .chat-msg.you .bubble').allTextContents();
  // One key combo in the card chat: the text goes out as a message, shows as a bubble, and the box is empty
  const sends=async(combo,text,id=ID)=>{const before=decides().length;await page.locator('#chat-input').fill(text);
   if(combo==='button')await page.locator('[data-chat-send]').click();else await page.locator('#chat-input').press(combo);
   await page.waitForFunction(t=>[...document.querySelectorAll('#chat-log .chat-msg.you .bubble')].some(b=>b.textContent.includes(t)),text,{timeout:5000}).catch(()=>{});
   const d=decides().slice(before);
   assert.deepEqual(d.map(a=>[a.args.suggestion_id,a.args.choice,a.args.feedback]),[[id,'other',text]],`${combo} (${tag}) sends the message, nothing else`);
   assert.equal(await page.locator('#chat-input').inputValue(),'',`${combo} (${tag}) empties the box`)};
  // Each combo on a fresh card, with its Do it right there in the chat under the box: the key that sends must never press it
  const doIt=()=>page.locator('.chat-main button.primary',{hasText:'Do it'});
  const combos=[...(phone?[]:[['Enter','Bring the pricing sheet']]),['Control+Enter','Ask Elif which inboxes they share'],['Meta+Enter','And what time zone they are in'],['button','Keep it short']];
  for(const [combo,text] of combos){reset();await open(ID);assert.ok(await doIt().isVisible(),'the card shows Do it in the chat');await sends(combo,text);
   assert.equal(decides().filter(a=>a.args.choice!=='other').length,0,combo+': Do it was never pressed');assert.equal((await bubbles()).filter(t=>t===text).length,1,combo+': one bubble');
   if(combo==='Control+Enter')await shot('sent')}
  // Shift+Enter: a new line, nothing sent; on a phone Enter is a new line too (the keyboard's Send key is the button)
  reset();await open(ID);
  await page.locator('#chat-input').fill('First line');await page.locator('#chat-input').press('Shift+Enter');await page.locator('#chat-input').type('second line');
  assert.equal(await page.locator('#chat-input').inputValue(),'First line\nsecond line');assert.equal(decides().length,0,'Shift+Enter only adds a line');
  if(phone){await page.locator('#chat-input').press('Enter');assert.equal(await page.locator('#chat-input').inputValue(),'First line\nsecond line\n');assert.equal(decides().length,0)}
  // An empty box: Ctrl+Enter does nothing at all (not Do it either)
  await page.locator('#chat-input').fill('');await page.locator('#chat-input').press('Control+Enter');await page.waitForTimeout(300);assert.equal(decides().length,0);assert.ok(await doIt().isVisible());

  // While a reply runs: Stop sits where Send was; typing brings Send back and every key combo steers the run
  await open(BUSY);
  assert.ok(await page.locator('[data-chat-stop]').isVisible());assert.ok(!(await page.locator('[data-chat-send]').isVisible()));
  await page.locator('#chat-input').press('Control+Enter');await page.waitForTimeout(300);
  assert.equal(actions.filter(a=>a.action==='chat_stop'||a.action==='decide'&&a.args.suggestion_id===BUSY).length,0,'Ctrl+Enter in an empty box neither stops nor sends');
  if(!phone)await sends('Enter','Make it Wednesday instead',BUSY);
  await sends('Control+Enter','And cc the team',BUSY);
  await sends('Meta+Enter','Sign it with my first name',BUSY);
  await shot('steered');
  // Stop: with an empty box the round button stops the run
  await page.locator('[data-chat-stop]').waitFor();await page.locator('[data-chat-stop]').click();
  await page.waitForFunction(()=>!document.querySelector('[data-chat-send]').hidden);
  assert.deepEqual(actions.filter(a=>a.action==='chat_stop').map(a=>a.args),[{suggestion_id:BUSY}]);

  // The Help chat: Enter (also on a phone) and Ctrl+Enter ask, Shift+Enter is a new line
  await page.evaluate(()=>document.querySelector('#open-help').click());await page.waitForSelector('#help-panel[open]');
  const asks=()=>actions.filter(a=>a.action==='help_ask').map(a=>a.args.question);
  await page.fill('#help-q','How do I');await page.press('#help-q','Shift+Enter');assert.equal(await page.inputValue('#help-q'),'How do I\n');assert.equal(asks().length,0);
  for(const [combo,q] of [['Enter','How do I snooze?'],['Control+Enter','How do I share a to-do?'],['Meta+Enter','How do I stop a run?']]){
   await page.fill('#help-q',q);await page.press('#help-q',combo);
   await page.waitForFunction(q=>[...document.querySelectorAll('#help-log .chat-msg.you .bubble')].some(b=>b.textContent===q),q);
   assert.equal(asks().at(-1),q,combo+' asks Help');assert.equal(await page.inputValue('#help-q'),'',combo+' empties the Help box')}
  assert.equal(asks().length,3);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('chat keys dashboard: ok');
}finally{await browser?.close();server.close()}
