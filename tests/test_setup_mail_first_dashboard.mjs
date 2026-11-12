import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A Machine without mail reads nothing and makes no to-dos (dashboard/setup-card.js, setupMailFirst): before anything
// else, the top of To-dos is one first step, "Connect your mail to get your first to-dos.", with Gmail and Outlook, each
// straight to its own sign-in under Connections, + Add. No ×. On a self-hosted Machine that isn't paired, that sign-in
// says to pair first, with "Use your own app" open beside it, never folded away. Once mail is in, the calendar comes
// next as the setup to-do's first row; once that is in too, the row is gone. A hosted Machine still on its setup page
// has the Needs you line instead, and a frame shows nothing. SHOTS=<folder> saves screenshots (390 and 1440, light and dark).
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const MAIL={id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'};
const CAL={id:'cal',service:'calendar',email:'owner@example.org',display_name:'Calendar',status:'ok'};
const TODO={id:'ab'.repeat(8),title:'Reply to Robin about the garden plan',body:'Robin asked for the dates.',status:'pending',scope:'personal',created_at:now,event_ids:[1]};
let connectors=[],suggestions=[],manage=null,paired=false,reviewsOn=true,live={runs:[]},setup={};
const fresh=()=>({closed:false,dismissed:[],phones:0,whatsapp:false,calendar:connectors.some(c=>c.service==='calendar'),
 mail_accounts:connectors.filter(c=>['gmail','outlook'].includes(c.service)).length,add:'google',more:false,since:now});
const status=()=>({suggestions,promises:[],connectors,suggestion_counts:{pending:suggestions.length},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
 review_live:live,reviews_on:reviewsOn,setup_card:setup,...(manage?{manage_url:manage,reviews_auto:true}:{})});
const SOURCES=[['gmail','Gmail','gmail','google'],['calendar','Google Calendar','calendar','google'],['outlook','Outlook','outlook','microsoft'],['outlook_calendar','Outlook Calendar','outlook_calendar','microsoft']]
 .map(([name,label,service,signin])=>({name,label,service,what:'Yours.',connected:0,form:{fields:[]},signin}));
const actions=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'||url.pathname==='/frame'){res.setHeader('Content-Type','text/html');res.end(url.pathname==='/'?dashboard:'<!doctype html><iframe src="/" style="width:1200px;height:800px"></iframe>');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r.action);
  if(r.action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:null,paired,pair_url:'https://app.example.test/pair',sources:SOURCES}));return}
  res.end('{}');return}
 if(/^\/brand\/[\w.-]+\.(png|webp|woff2)$/.test(url.pathname)){try{const f=await readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url));res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':url.pathname.endsWith('.webp')?'image/webp':'font/woff2');res.end(f)}catch{res.statusCode=404;res.end()}return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const reset=(o={})=>{connectors=o.connectors||[];suggestions=o.suggestions||[];manage=o.manage||null;paired=!!o.paired;reviewsOn=o.reviewsOn??true;live=o.live||{runs:[]};setup=fresh();actions.length=0};
const open=async({width=1440,height=900,scheme='light',url=base}={})=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await context.addInitScript(()=>{try{sessionStorage.setItem('device-session',String(Date.now()-120000))}catch{}});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.goto(url);if(url===base)await page.waitForFunction(()=>typeof state!=='undefined'&&state?.suggestions);await page.waitForTimeout(150);return {context,page}};
const card=page=>page.evaluate(()=>{const el=document.querySelector('#setup-card');const shown=!!el&&!el.hidden&&el.getBoundingClientRect().height>0;
 return {shown,first:!!el?.classList.contains('mail-first'),head:shown?el.querySelector('.setup-head').innerText.replace(/\s+/g,' ').trim():'',
  buttons:shown?[...el.querySelectorAll('.setup-mail button')].map(b=>[b.textContent,b.dataset.connectOpen]):[],close:!!el?.querySelector('.setup-x'),
  rows:shown?[...el.querySelectorAll('.setup-row')].map(r=>r.dataset.step):[]}});
const shot=async(page,name)=>{if(shots){await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(150);await page.screenshot({path:`${shots}/${name}.png`})}};
const signin=page=>page.evaluate(()=>{const p=document.querySelector('#connect-add .connect-signin');return p?{head:p.querySelector('h3')?.textContent,text:p.innerText.replace(/\s+/g,' '),
 other:p.querySelector('details.connect-other')?.open??null,primary:p.querySelector('button.primary')?.textContent}:null});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});

 // A brand-new self-hosted Machine, not paired, nothing connected: the one first step, above the empty list, at every size.
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){reset();
  const {context,page}=await open({width,height,scheme});
  const c=await card(page);
  assert.deepEqual(c,{shown:true,first:true,head:'Connect your mail to get your first to-dos.',buttons:[['Gmail','gmail'],['Outlook','outlook'],['Other email','imap']],close:false,rows:[]});
  assert.ok(await page.evaluate(()=>{const n=document.querySelector('#setup-card').getBoundingClientRect(),e=document.querySelector('#suggestions').getBoundingClientRect();
   return n.bottom<=e.top+1&&document.documentElement.scrollWidth<=innerWidth&&n.left>=0&&n.right<=innerWidth}),'above the list, fits the screen');
  // nothing to check without mail: no robot, no line, no Check now under the card
  assert.equal(await page.evaluate(()=>[...document.querySelectorAll('#suggestions .all-clear,#suggestions [data-check-now]')].some(e=>e.getClientRects().length>0)),false,'the empty state hides');
  await shot(page,`mail-first-${width}-${scheme}`);
  if(width===1440&&scheme==='light'){
   // Gmail: straight to Google's sign-in; not paired, so pairing first with the other way open beside it
   await page.locator('[data-connect-open="gmail"]').click();await page.locator('#connect-add .connect-signin').waitFor();
   const s=await signin(page);assert.equal(s.head,'Google');assert.equal(s.primary,'Pair this Machine');assert.equal(s.other,true,'Use your own app is open');
   assert.match(s.text,/Use your own app/);await shot(page,'mail-first-gmail-unpaired-1440-light');}
  await context.close()}

 // Paired: Outlook goes straight to Sign in with Microsoft, its other way folded.
 {reset({paired:true});const {context,page}=await open();
  await page.locator('[data-connect-open="outlook"]').click();await page.locator('#connect-add .connect-signin').waitFor();
  const s=await signin(page);assert.equal(s.head,'Microsoft');assert.equal(s.primary,'Sign in with Microsoft');assert.equal(s.other,false);
  await shot(page,'mail-first-outlook-paired-1440-light');await context.close()}

 // Mail in, no calendar: the first step is gone and the calendar comes next, the setup to-do's first row.
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){reset({connectors:[MAIL],suggestions:[TODO],paired:true});
  const {context,page}=await open({width,height,scheme});await page.locator('#task-'+TODO.id).waitFor();
  const c=await card(page);assert.equal(c.first,false);assert.equal(c.rows[0],'calendar');
  assert.equal(await page.locator('[data-step="calendar"] .setup-label').textContent(),'Connect your calendar');
  await shot(page,`calendar-next-${width}-${scheme}`);
  if(width===1440&&scheme==='light'){await page.locator('[data-setup-go="calendar"]').click();await page.locator('#connect-add .connect-signin').waitFor();
   assert.equal((await signin(page)).primary,'Sign in with Google')}
  await context.close()}

 // Mail and calendar in: no calendar row.
 {reset({connectors:[MAIL,CAL],suggestions:[TODO]});const {context,page}=await open();await page.locator('#task-'+TODO.id).waitFor();
  assert.ok(!(await card(page)).rows.includes('calendar'));await context.close()}

 // A chat already brings messages in (WhatsApp here): it reads something, so no first step that can't be closed.
 {reset({connectors:[{id:'wa',service:'whatsapp',display_name:'WhatsApp',status:'ok'}]});const {context,page}=await open();
  assert.equal((await card(page)).first,false);
  assert.equal(await page.evaluate(()=>document.querySelector('#inbox').classList.contains('mail-first')),false,'the empty state is back');await context.close()}

 // A hosted Machine still on its setup page: the Needs you line says it, not a second card.
 {reset({manage:'https://app.example.test/setup',reviewsOn:false,live:{runs:[],first_look:{why:'sources'}}});const {context,page}=await open();
  assert.equal((await card(page)).shown,false);
  assert.match(await page.locator('#needs-you').innerText(),/Connect your mail to get your first to-dos\./);await context.close()}

 // In a frame: nothing.
 {reset();const {context,page}=await open({url:base+'frame'});const frame=page.frames().find(f=>f!==page.mainFrame());
  await frame.waitForFunction(()=>typeof state!=='undefined'&&state?.suggestions);await frame.waitForTimeout(150);
  assert.equal(await frame.evaluate(()=>!document.querySelector('#setup-card')||document.querySelector('#setup-card').hidden),true);await context.close()}

 assert.deepEqual(errors,[]);
 console.log('setup mail first dashboard ok');
}finally{await browser?.close();server.close()}
