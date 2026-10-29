import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A preparing card on the browser shows that tab live (right of its steps, below them on a phone; larger on a click,
// gone when the run is off the browser). Cards on screen read their email ahead, once each. Connections, Add sets a
// source up right there: its questions one at a time, a key in a password field. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const icon=(await readFile(new URL('../brand/app-icon-192.png',import.meta.url))).toString('base64');
const now=new Date().toISOString();
const card=(id,i,extra={})=>({id,status:'pending',title:'Card '+i,body:'A useful suggestion with enough words to take a few lines on a card. '.repeat(8),created_at:now,source_line:'Source: email from Ann',event_ids:[i],...extra});
const suggestions=[card('prep',0,{status:'accepted',preparation_status:'running',preparation_started_at:new Date(Date.now()-90000).toISOString(),title:'Download the invoice'}),
 ...Array.from({length:12},(_,i)=>card('c'+i,i+1))];
let peek=true,peekCalls=0,session=null;
const hits={originals:{},email:{}};
const posts=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions,promises:[],connectors:[{id:'mail',service:'gmail',display_name:'mail',email:'owner@example.org',boundary:'work',last_success:now,state:'{}'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/progress'){res.end(JSON.stringify({status:'running',started_at:now,steps:[{title:'Opening the supplier portal'},{title:'Using the browser'}],browser:null,peek}));return}
 if(url.pathname==='/api/peek'){peekCalls++;res.end(JSON.stringify(peek?{on:true,image:'data:image/png;base64,'+icon}:{on:false}));return}
 if(url.pathname==='/api/originals'){const id=url.searchParams.get('id');hits.originals[id]=(hits.originals[id]||0)+1;res.end(JSON.stringify({originals:[{kind:'email',from:'Ann <ann@example.org>',to:'',cc:'',title:'Invoice',occurred_at:now,body:'Plain',event_id:7,attachments:[]}]}));return}
 if(url.pathname==='/api/email'){const id=url.searchParams.get('id');hits.email[id]=(hits.email[id]||0)+1;res.end(JSON.stringify({html:'<p id=hello>Hello</p>',images:{}}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:null,sources:[{name:'gmail',service:'gmail',label:'Gmail',connected:1,broker:false},{name:'crm',service:'salesflare',label:'Salesflare CRM',connected:0,broker:false},{name:'github',service:'github',label:'GitHub',connected:0,broker:false,what:'Review requests and mentions.'}]}));return}
  if(action==='connect_start'){session={session:'s1',state:'running',label:'Salesflare CRM',source:args.name,lines:['Salesflare: create an API key in Salesflare’s settings (API keys).'],question:{id:1,kind:'secret',prompt:'Salesflare API key',default:''}};res.end(JSON.stringify(session));return}
  if(action==='connect_poll'){res.end(JSON.stringify(session));return}
  if(action==='connect_answer'){session={...session,question:null,state:'done',account:'acme-crm',restarting:true,lines:[...session.lines,'Salesflare: owner@example.org','✓ Salesflare CRM connected']};res.end(JSON.stringify(session));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const wait=async(f,what)=>{for(const end=Date.now()+20000;Date.now()<end;){if(await f())return;await new Promise(r=>setTimeout(r,25))}throw Error('timed out: '+what)};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1280,900],[390,844]]){
  peek=true;
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);
  const thumb=page.locator('#task-prep .peek-thumb img');
  await thumb.waitFor({timeout:15000});
  // Emails of the cards on screen were read ahead, each once; one opens at once.
  await wait(async()=>Object.keys(hits.email).length>=1,'prefetch');
  await page.waitForTimeout(400);
  assert.ok(Object.values(hits.originals).every(n=>n===1)&&Object.values(hits.email).every(n=>n===1),JSON.stringify(hits));
  const below=await page.evaluate(()=>[...document.querySelectorAll('article[id^="task-"]')].filter(e=>e.getBoundingClientRect().top>innerHeight+150).map(e=>e.id.slice(5)));
  assert.ok(below.length&&below.every(id=>!hits.email[id]),'cards far below the screen wait');
  const box=await page.locator('#task-prep .peek-thumb').boundingBox(),steps=await page.locator('#task-prep .steps').boundingBox();
  if(width>600)assert.ok(box.x>steps.x+steps.width-1&&Math.abs(box.y-steps.y)<20,'right of the steps');
  else assert.ok(box.y>=steps.y+steps.height-1&&box.width>300,'below the steps, full width');
  if(shots)await page.locator('#task-prep').screenshot({path:`${shots}/peek-${width}.png`});
  await page.locator('#task-prep .peek-thumb').click();
  await page.locator('#peek-dialog[open] #peek-image').waitFor();
  if(shots)await page.screenshot({path:`${shots}/peek-open-${width}.png`});
  // Off the browser: the picture and its larger view go.
  peek=false;
  await wait(async()=>!(await page.locator('#peek-dialog[open]').count())&&!(await page.locator('#task-prep .peek-thumb').count()),'the look closes');
  // Let reading ahead settle first (shorter cards put more of them on screen).
  for(let last='';last!==JSON.stringify(hits);){last=JSON.stringify(hits);await page.waitForTimeout(500)}
  const seen=Object.keys(hits.email)[0];
  // Only the opened card counts: reading ahead may still pick up a card that scrolled into view.
  const of=id=>JSON.stringify([hits.originals[id],hits.email[id]]),before=of(seen);
  await page.locator(`#task-${seen} .card-foot [data-details]`).click();await page.locator(`#task-${seen} .read-original`).click();
  await page.frameLocator('#email-dialog iframe').locator('#hello').waitFor();
  assert.equal(of(seen),before,'opened from what was read ahead');
  await page.keyboard.press('Escape');
  for(const k of Object.keys(hits))hits[k]={};
  // Connections, Add.
  await page.goto(base+'/#connections=add');
  await page.locator('#connect-add [data-connect="crm"]').waitFor();
  assert.deepEqual(await page.locator('#connect-add .connect-source b').allInnerTexts(),['Gmail','Salesflare CRM','GitHub']);
  assert.equal(await page.locator('#connectors>article:not([hidden])').count(),0);
  if(shots)await page.screenshot({path:`${shots}/add-${width}.png`});
  await page.locator('#connect-add [data-connect="crm"]').click();
  await page.locator('#connect-answer[type=password]').waitFor();
  assert.match(await page.locator('#connect-add .connect-lines').innerText(),/API key/);
  if(shots)await page.screenshot({path:`${shots}/add-key-${width}.png`});
  await page.locator('#connect-answer').fill('fake-key');
  await page.locator('#connect-add .connect-form button').click();
  await page.locator('#connect-add .sent-ok').waitFor();
  assert.match(await page.locator('#connect-add').innerText(),/Connected\. Restarting to start reading it/);
  if(shots)await page.screenshot({path:`${shots}/add-done-${width}.png`});
  const answer=posts.find(p=>p.action==='connect_answer');
  assert.deepEqual(answer.args,{session:'s1',question:1,value:'fake-key'});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('peek, prefetch and add dashboard ok');
}finally{await browser?.close();server.close()}
