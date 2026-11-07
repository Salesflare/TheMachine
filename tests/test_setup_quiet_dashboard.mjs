import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A daily owner's To-dos: past the first day with to-dos (setup_card.since), the setup to-do is one quiet line above
// Ready, "2 steps left · Continue", which opens the card on a tap and folds again with its chevron; on the first day it
// is the full card. The banners above the to-dos (Fixed, Needs you) stack into one box, so on a phone the first to-do's
// button is on the first screen. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),hoursAgo=h=>new Date(Date.now()-h*36e5).toISOString();
const CARD='ab'.repeat(8);
let setup,banners;
const status=()=>({suggestions:[{id:CARD,title:'Reply to Robin about the garden plan',body:'Robin asked for the dates.',status:'pending',scope:'personal',created_at:now,event_ids:[1]}],
 promises:[],connectors:[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}],suggestion_counts:{pending:1},decisions:[],analyses:[],deliveries:[],
 review_health:{},review_runs:[],review_live:{runs:[]},setup_hints:[],phone_app_store:{ios:'https://apps.example.test/ios',android:'https://play.example.test/android'},setup_card:setup,
 ...(banners?{fixed:[{id:'fix-1',text:'Fixed: the Projects tab now opens when it’s empty.'}],skills:{waiting:2}}:{})});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const UA={chrome:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
 iphone:'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1'};
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const open=async({width=1440,height=900,scheme='light'}={})=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,userAgent:UA[mobile?'iphone':'chrome'],colorScheme:scheme,locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await context.addInitScript(()=>{try{sessionStorage.setItem('device-session',String(Date.now()-120000))}catch{}});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.goto(base);await page.locator('#task-'+CARD).waitFor();await page.locator('#setup-card').waitFor();await page.waitForTimeout(300);return {context,page}};
const look=page=>page.evaluate(()=>{const el=document.querySelector('#setup-card'),r=el.getBoundingClientRect(),ready=document.querySelector('#suggestions .section-head').getBoundingClientRect();
 const btn=document.querySelector('#suggestions article.card button.primary')?.getBoundingClientRect();
 return {quiet:el.classList.contains('quiet'),line:el.querySelector('[data-setup-open]')?.innerText.replace(/\s+/g,' ').trim()||'',rows:el.querySelectorAll('.setup-row').length,
  height:Math.round(r.height),above:r.bottom<=ready.top,button:btn?Math.round(btn.bottom):null}});
const shot=async(page,name)=>{if(shots)await page.screenshot({path:`${shots}/${name}.png`})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const FRESH={closed:false,dismissed:[],phones:0,whatsapp:false,mail_accounts:1,add:'google',more:false};

 // The first day: the full card, as before.
 {setup={...FRESH,since:hoursAgo(3)};banners=false;const {context,page}=await open();
  const c=await look(page);assert.equal(c.quiet,false);assert.equal(c.line,'');assert.ok(c.rows>=3,'the rows: '+c.rows);
  await context.close()}

 // After it, at 1440 and 390, light and dark: one line above Ready that opens the card and folds it again.
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){setup={...FRESH,since:hoursAgo(72)};banners=true;
  const {context,page}=await open({width,height,scheme});
  let c=await look(page);
  assert.equal(c.quiet,true,'folded');assert.match(c.line,/^\d steps left · Continue$/);assert.equal(c.rows,0);
  assert.ok(c.height<=40,'one line: '+c.height);assert.ok(c.above,'above Ready');
  assert.ok(c.button&&c.button<=height,`the first to-do's button on the first screen: ${c.button} of ${height}`);
  // The banners: one box, a hairline between, not a card each
  const stack=await page.evaluate(()=>{const s=document.querySelector('#banners'),n=document.querySelector('#needs-you'),f=document.querySelector('#fixed-notice .notice-card');
   const cs=e=>getComputedStyle(e);return {fixed:!document.querySelector('#fixed-notice').hidden,needs:!n.hidden,box:cs(s).borderTopWidth,shadow:[cs(n).boxShadow,cs(f).boxShadow],line:cs(n).borderTopWidth}});
  assert.deepEqual(stack,{fixed:true,needs:true,box:'1px',shadow:['none','none'],line:'1px'});
  await shot(page,`setup-quiet-${width}-${scheme}`);
  await page.locator('[data-setup-open]').click();
  c=await look(page);assert.equal(c.quiet,false);assert.ok(c.rows>=2,'opened: '+c.rows);
  assert.equal(await page.evaluate(()=>document.activeElement?.matches('[data-setup-fold]')),true,'focus on the fold');
  await shot(page,`setup-quiet-open-${width}-${scheme}`);
  await page.locator('[data-setup-fold]').click();
  c=await look(page);assert.equal(c.quiet,true,'folded again');
  assert.equal(await page.evaluate(()=>document.activeElement?.matches('[data-setup-open]')),true,'focus on the line');
  await context.close()}

 assert.deepEqual(errors,[]);
 console.log('setup quiet dashboard: ok');
}finally{await browser?.close();server.close()}
