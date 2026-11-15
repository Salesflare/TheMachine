import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do whose last step books a call (kind finish): its chat shows what goes out (the invitation's title, time,
// guests and the Meet link to be added) above the step's button, so the owner sees it before the tap. Before, the chat
// showed only the run's text and the button. Synthetic data, a local fixture server, nothing sent.
// SHOT_DIR: screenshots at 390 and 1440, light. FINAL_STEP_PAGE=<another dashboard.html> with FINAL_STEP_BEFORE=1:
// only the screenshots, with the chat as the service gave it before (no draft for the step).
const before=!!process.env.FINAL_STEP_BEFORE,dashboard=await dashboardPage(process.env.FINAL_STEP_PAGE||undefined);
const now=new Date().toISOString(),t0=Date.now()-600000,id='f1f1f1f1f1f1f1f1';
const preview='Intro call: Example Studio and Robin Lee\nTue 17 Nov, 10:00-10:30 (Europe/Brussels)\nGuests: Robin Lee <robin@example.invalid>\nA Google Meet link is added when the event is made.';
const step={kind:'finish',label:'Book intro call',revision:'b00c0011aa22',instructions:'Create the event with these values and send the invitation.',preview,url:'https://calendar.google.com/'};
const cards=[{id,title:'Arrange an intro call with Robin',body:'The invitation is ready to send.',status:'prepared',scope:'work',created_at:now,event_ids:[1],
 next_action:step,next_actions:[step],outcome:JSON.stringify({state:'needs_you',needs:'Book the call'})}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const draft={kind:'finish',to:[],subject:'',label:step.label,body:preview,reply:false};
const history={session:true,status:'idle',active:false,cursor:'k1',items:[
 {kind:'source',from:'Robin Lee',via:'email',title:'Intro call',text:'Tuesday 10:00 works. Could you send an invite?',mine:false,at:t0},
 {kind:'event',text:'Chose Do it',mine:true,at:t0+60000},
 {kind:'steps',count:9,steps:[{line:['Read your mail'],n:5},{line:['Checked your calendar'],n:4}],at:t0+90000},
 {kind:'reply',text:'The invitation is ready to send.',drafts:before?[]:[draft],files:[],at:t0+120000}]};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'&&JSON.parse(body||'{}').action==='card_chat'){res.end(JSON.stringify(history));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]]){
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:'light'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#chat='+id);await page.locator('#chat-log .chat-msg, #chat-log .chat-result').last().waitFor();
  if(!before){
   // What goes out, whole, in the chat's result, with the step's button under it
   const box=page.locator('#chat-log .chat-draft');
   assert.equal(await box.count(),1);
   assert.equal((await box.locator('.chat-draft-head').textContent()).trim(),'What goes out');
   const text=await box.textContent();
   for(const part of ['Intro call: Example Studio and Robin Lee','10:00-10:30 (Europe/Brussels)','Guests: Robin Lee','Google Meet link is added'])assert.ok(text.includes(part),part);
   // whole, never clamped: the last line (the Meet link) shows without a tap
   const shown=box.locator('.chat-clamp');
   assert.ok(await shown.evaluate(n=>n.classList.contains('open')&&n.scrollHeight<=n.clientHeight+1),'the whole preview shows');
   const button=box.getByRole('button',{name:'Book intro call'});
   assert.ok(await button.isVisible());
   const [b,d]=await Promise.all([button.boundingBox(),shown.boundingBox()]);
   assert.ok(b.y>=d.y+d.height-1,'the button comes after what goes out');
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  }
  if(process.env.SHOT_DIR){await page.locator('#chat-log>*').last().scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.SHOT_DIR}/chat-final-step-${before?'before':'after'}-${width}.png`})}
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok chat final step');
