import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The setup to-do's one suggestion with its reason (setup_card.nudge, machine/app/setup_nudge.py): it leads the card in
// the place of the row it is about (a WhatsApp suggestion: no plain Connect WhatsApp row), the folded line says it
// instead of "2 steps left · Continue", its button goes to that connect, and its × closes it like any row. Without one,
// the rows stay as they were. And the first look's ending with its connect offers shows after one to-do too, once the
// list is empty. Fake data only. SHOTS=<folder> saves screenshots at 1440 and 390, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),hoursAgo=h=>new Date(Date.now()-h*36e5).toISOString();
const CARD='cd'.repeat(8);
const NUDGE={id:'nudge-whatsapp',title:'Connect WhatsApp? 5 emails mention it.',button:'Connect',href:'#connect=whatsapp',icon:'whatsapp',replaces:'whatsapp',nudge:true};
const FRESH={closed:false,dismissed:[],phones:0,whatsapp:false,calendar:true,mail_accounts:1,add:'google',more:false,memory:true};
let setup,todos=true,ending=null;
const posted=[];
const status=()=>({suggestions:todos?[{id:CARD,title:'Reply to Robin about the garden plan',body:'Robin asked for the dates.',status:'pending',scope:'personal',created_at:now,event_ids:[1]}]:[],
 promises:[],connectors:[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}],suggestion_counts:{pending:todos?1:0},decisions:[],analyses:[],deliveries:[],
 review_health:{},review_runs:[],review_live:{runs:[]},reviews_on:true,setup_hints:[],manage_url:'https://app.example.test/setup',
 phone_app_store:{ios:'https://apps.example.test/ios',android:'https://play.example.test/android'},setup_card:setup,first_look_done:ending});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){const a=JSON.parse(body||'{}');posted.push(a);
  if(a.action==='connect_sources'){res.end(JSON.stringify({sources:[],suggested:[],manage_url:'https://app.example.test/setup'}));return}
  if(a.action==='setup_dismiss'){setup={...setup,dismissed:[...setup.dismissed,a.args.step],nudge:null};res.end(JSON.stringify({setup_card:setup}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const UA={chrome:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
 iphone:'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1'};
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const open=async({width=1440,height=900,scheme='light'}={},ready='#setup-card')=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,userAgent:UA[mobile?'iphone':'chrome'],colorScheme:scheme,locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await context.addInitScript(()=>{try{sessionStorage.setItem('device-session',String(Date.now()-120000))}catch{}});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.goto(base);await page.locator(ready).first().waitFor();if(ready==='#setup-card')await page.waitForFunction(()=>document.querySelector('#setup-card [data-setup-open],#setup-card .setup-row'));return {context,page}};
const look=page=>page.evaluate(()=>{const el=document.querySelector('#setup-card');
 return {quiet:el.classList.contains('quiet'),line:el.querySelector('[data-setup-open]')?.innerText.replace(/\s+/g,' ').trim()||'',
  rows:[...el.querySelectorAll('.setup-row')].map(r=>r.dataset.step),first:el.querySelector('.setup-row .setup-label')?.innerText.trim()||''}});
const shot=async(page,name)=>{if(shots)await page.screenshot({path:`${shots}/${name}.png`})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});

 // Without a suggestion: the rows as they were, WhatsApp among them
 {setup={...FRESH,since:hoursAgo(3)};const {context,page}=await open();
  const c=await look(page);assert.ok(c.rows.includes('whatsapp'),c.rows.join());assert.ok(!c.rows.some(r=>r.startsWith('hint-nudge')));
  await context.close()}

 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  // The first day: the full card, the suggestion first, no plain Connect WhatsApp row
  {setup={...FRESH,since:hoursAgo(3),nudge:NUDGE};todos=true;ending=null;const {context,page}=await open({width,height,scheme});
   const c=await look(page);assert.equal(c.quiet,false);assert.equal(c.rows[0],'hint-nudge-whatsapp');assert.equal(c.first,NUDGE.title);
   assert.ok(!c.rows.includes('whatsapp'),'replaced: '+c.rows.join());assert.ok(c.rows.includes('connect'),'the others stay: '+c.rows.join());
   const fits=await page.evaluate(()=>{const r=document.querySelector('#setup-card .setup-row').getBoundingClientRect();return r.right<=innerWidth&&document.documentElement.scrollWidth<=innerWidth});
   assert.ok(fits,'no sideways scroll');
   await shot(page,`nudge-card-${width}-${scheme}`);await context.close()}
  // Folded: the line is the suggestion, a tap opens the card with it first
  {setup={...FRESH,since:hoursAgo(72),nudge:NUDGE};const {context,page}=await open({width,height,scheme});
   let c=await look(page);assert.equal(c.quiet,true);assert.equal(c.line,NUDGE.title);
   const h=await page.evaluate(()=>Math.round(document.querySelector('#setup-card').getBoundingClientRect().height));assert.ok(h<=(width<600?56:40),'short: '+h);
   await shot(page,`nudge-folded-${width}-${scheme}`);
   await page.locator('[data-setup-open]').click();c=await look(page);assert.equal(c.rows[0],'hint-nudge-whatsapp');
   await context.close()}
  // The first look found one to-do, since done: its ending with its connect offers, not All clear
  {setup={...FRESH,since:hoursAgo(30),nudge:NUDGE};todos=false;
   ending={at:hoursAgo(2),days:7,kinds:{email:42},read:{people:12,newsletters:22,notifications:8},todos:1,acted:true,next:['calendar'],connect:[{service:'slack',label:'Slack'}]};
   const {context,page}=await open({width,height,scheme},'.first-look-end');
   const e=await page.evaluate(()=>({line:document.querySelector('.first-look-end .fl-read')?.innerText,next:[...document.querySelectorAll('.first-look-end .fl-next button')].map(b=>b.innerText)}));
   assert.match(e.line,/^Read 42\semails from the past week/);assert.deepEqual(e.next,['Connect Slack','Connect your calendar']);
   await shot(page,`first-look-one-todo-${width}-${scheme}`);await context.close()}
 }

 // Two to-dos from the first look: no ending, the list's own empty state
 {setup={...FRESH,since:hoursAgo(30)};todos=false;ending={at:hoursAgo(2),days:7,kinds:{email:42},read:{},todos:2,acted:true,next:[],connect:[]};
  const {context,page}=await open({},'#suggestions .all-clear');assert.equal(await page.locator('.first-look-end').count(),0);await context.close()}

 // The button goes to that connect; its × closes it for good, and the row it stood for comes back
 {setup={...FRESH,since:hoursAgo(3),nudge:NUDGE};todos=true;ending=null;const {context,page}=await open();
  await page.evaluate(()=>addEventListener('hashchange',e=>{window.sawIt??=new URL(e.newURL).hash}));
  await page.locator('[data-setup-go="hint-nudge-whatsapp"]').click();
  assert.equal(await (await page.waitForFunction(()=>window.sawIt)).jsonValue(),'#connect=whatsapp');await context.close()}
 {const {context,page}=await open();
  await Promise.all([page.waitForResponse(r=>(r.request().postData()||'').includes('setup_dismiss')),page.locator('[data-setup-dismiss="hint-nudge-whatsapp"]').click()]);await page.waitForFunction(()=>!document.querySelector('[data-step="hint-nudge-whatsapp"]'));
  assert.deepEqual(posted.filter(p=>p.action==='setup_dismiss').map(p=>p.args.step),['hint-nudge-whatsapp']);
  const c=await look(page);assert.ok(!c.rows.includes('hint-nudge-whatsapp'));assert.ok(c.rows.includes('whatsapp'),c.rows.join());
  await context.close()}

 assert.deepEqual(errors,[]);
 console.log('setup nudge dashboard: ok');
}finally{await browser?.close();server.close()}
