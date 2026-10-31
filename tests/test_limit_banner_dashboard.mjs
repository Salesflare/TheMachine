import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A usage limit reached (state.model_pause) shows one short line at the top of the dashboard: which limit, when it
// resets in the viewer's time, and that nothing is lost. No reset known drops that sentence; null hides the line.
// It fits a phone without a sideways scroll. Reviews waiting for the budget (state.review_pause) say until when, with
// Review now, which posts the owner's review_now; a usage limit reached goes first. With a working fallback answering
// meanwhile, the line only says so.
const dashboard=await dashboardPage();
const posted=[];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/api/action'){let body='';req.on('data',c=>body+=c);req.on('end',()=>{posted.push(JSON.parse(body));res.setHeader('Content-Type','application/json');res.end('{"asked":true}')});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440]){
  const context=await browser.newContext({viewport:{width,height:844},isMobile:width<600,hasTouch:width<600,locale:'en-US',timezoneId:'America/New_York'}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof renderLimitBanner==='function');await page.evaluate(()=>applyLocale({date_locale:'en-US',hour12:true}));
  const show=(p,q=null)=>page.evaluate(([p,q])=>{state.model_pause=p;state.review_pause=q;renderLimitBanner();const b=document.querySelector('#limit-banner');
   return {shown:!b.hidden&&b.getBoundingClientRect().height>0,text:b.textContent,wide:document.documentElement.scrollWidth>innerWidth}},[p,q]);
  const soon=(Date.now()/1000|0)+3600;
  const later=await page.evaluate(()=>{const d=new Date();d.setDate(d.getDate()+3);d.setHours(9,0,0,0);return d.getTime()/1000|0});
  const weekday=await page.evaluate(t=>new Date(t*1000).toLocaleDateString('en-US',{weekday:'short'}),later);
  let r=await show({window:'5h',until:soon,name:'ChatGPT'});
  assert.ok(r.shown,'shown');assert.ok(!r.wide,`${width}: no sideways scroll`);
  assert.match(r.text,/^ChatGPT 5-hour limit reached\. Resets (at|\w{3}) \d{1,2}:\d\d [AP]M\. Nothing is lost: The Machine picks up where it left off\.$/);
  r=await show({window:'week',until:later,name:'Claude'});
  assert.equal(r.text,`Claude weekly limit reached. Resets ${weekday} 9:00 AM. Nothing is lost: The Machine picks up where it left off.`);
  r=await show({window:'limit',until:null,name:'ChatGPT'});
  assert.equal(r.text,'ChatGPT usage limit reached. Nothing is lost: The Machine picks up where it left off.');
  r=await show({window:'limit',until:null,name:null});
  assert.equal(r.text,'AI usage limit reached. Nothing is lost: The Machine picks up where it left off.');
  r=await show({window:'5h',until:Date.now()/1000-60,name:'ChatGPT'});
  assert.ok(!/Resets/.test(r.text),'a reset in the past is not shown');
  r=await show({window:'limit',until:soon,name:'ChatGPT',fallback:true});  // a working fallback answers meanwhile
  assert.ok(r.shown&&!r.wide,`${width}: the fallback line fits`);
  assert.equal(r.text,'ChatGPT limit reached, using your fallback.');
  r=await show(null);assert.ok(!r.shown,'gone when model_pause is null');
  const seven=await page.evaluate(()=>{const d=new Date();d.setHours(23,45,0,0);return d.getTime()/1000|0});
  r=await show(null,{window:'week',until:seven,name:'ChatGPT'});
  assert.ok(r.shown&&!r.wide,`${width}: the review pause fits`);
  assert.equal(r.text,'Reviews wait until 11:45 PM to save your ChatGPT week.Review now');
  r=await show(null,{window:'5h',until:null,name:null});
  assert.equal(r.text,'Reviews wait to save your AI 5-hour limit.Review now');
  r=await show({window:'5h',until:soon,name:'ChatGPT'},{window:'week',until:seven,name:'ChatGPT'});
  assert.match(r.text,/^ChatGPT 5-hour limit reached/,'a usage limit reached goes first');
  await show(null,{window:'week',until:seven,name:'ChatGPT'});
  await page.click('[data-review-now]');
  await page.waitForFunction(()=>document.querySelector('#limit-banner').hidden);
  assert.deepEqual(posted.pop(),{action:'review_now',args:{}});
  await context.close()}
 assert.ok(dashboard.includes("usage_limited:'The AI usage limit was reached.'"),'a run that hit the limit says so');
 assert.deepEqual(errors,[]);
 console.log('limit banner dashboard ok');
}finally{await browser?.close();server.close()}
