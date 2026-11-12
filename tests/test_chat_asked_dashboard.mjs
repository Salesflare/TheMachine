import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's chat after the owner answered the question its run stopped on: the question is a small event line ("Asked:
// …", The Machine's, in the middle like "Checked 6 things"), and the owner's bubble holds only their answer. The to-do's
// own note says "Your answer" for it. SHOT_DIR: screenshots at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),t0=Date.now()-600000;
const question='Should I send the October invoice now, or wait for November?';
const id='a1a1a1a1a1a1a1a1';
const cards=[{id,title:'Invoice the partner',body:'Preparing the October invoice.',status:'instructions',scope:'work',created_at:now,event_ids:[1],preparation_status:'running',
 preparation_started_at:now,latest_feedback:{choice:'other',feedback:'October now',asked:[question],created_at:now}}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const history={session:true,status:'running',active:false,cursor:'k1',items:[
 {kind:'source',from:'Robin Lee',via:'email',title:'Invoice',text:'Can you send last month’s invoice?',mine:false,at:t0},
 {kind:'steps',count:6,steps:[{line:['Read your mail'],n:4},{line:['Used the browser on example.com'],n:2}],at:t0+1000},
 {kind:'event',text:'Renamed',mine:true,at:t0+60000},
 {kind:'event',text:'Asked: '+question,asked:true,at:t0+119999},
 {kind:'you',text:'October now',via:'dashboard',at:t0+120000},
 {kind:'steps',count:3,steps:[{line:['Read your mail'],n:3}],at:t0+150000},
 {kind:'reply',text:'Preparing the October invoice now. I’ll put the PDF in Drive.',drafts:[],files:[],at:t0+180000}]};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'&&JSON.parse(body||'{}').action==='card_chat'){res.end(JSON.stringify(history));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+id).waitFor();
  // The to-do's note is the answer, named as one
  assert.equal(await page.locator(`#task-${id} .saved-feedback strong`).textContent(),'Your answer');
  assert.equal(await page.locator(`#task-${id} .saved-feedback blockquote`).textContent(),'October now');
  if(process.env.SHOT_DIR){await page.locator(`#task-${id}`).getByText('Details',{exact:true}).first().click();await page.locator(`#task-${id} .saved-feedback`).waitFor()}
  if(process.env.SHOT_DIR)await page.locator('#task-'+id).screenshot({path:`${process.env.SHOT_DIR}/todo-your-answer-${width}-${scheme}.png`});
  await page.goto('http://127.0.0.1:'+server.address().port+'/#chat='+id);await page.locator('#chat-log .chat-msg.you:not(.chat-source)').waitFor();
  // The question: a quiet line of The Machine's, like the run's own line; the owner's bubble: the answer alone
  const asked=page.locator('#chat-log .chat-event',{hasText:'Asked:'});
  assert.equal(await asked.count(),1);
  assert.match(await asked.textContent(),/^Asked: Should I send the October invoice now, or wait for November\?/);
  assert.ok(!(await asked.evaluate(n=>n.classList.contains('mine'))));
  assert.equal(await page.locator('#chat-log .chat-msg.you:not(.chat-source) .bubble').textContent(),'October now');
  // In that order, and the line is as small as the other event lines
  const order=await page.locator('#chat-log>*').evaluateAll(ns=>ns.map(n=>n.classList.contains('chat-event')?n.textContent.slice(0,6):n.classList.contains('you')?'you':''));
  assert.ok(order.indexOf('Asked:')>=0&&order.indexOf('Asked:')<order.lastIndexOf('you'));
  const size=s=>page.locator(s).first().evaluate(n=>getComputedStyle(n).fontSize);
  assert.equal(await size('#chat-log .chat-event:has-text("Asked:")'),await size('#chat-log .chat-event:has-text("Renamed")'));
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  if(process.env.SHOT_DIR){await page.locator('#chat-log .chat-msg.machine').last().scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.SHOT_DIR}/chat-asked-${width}-${scheme}.png`})}
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok chat asked');
