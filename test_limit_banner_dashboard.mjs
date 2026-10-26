import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from './openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A usage limit reached (state.model_pause) shows one short line at the top of the dashboard: which limit, when it
// resets in the viewer's time, and that nothing is lost. No reset known drops that sentence; null hides the line.
// It fits a phone without a sideways scroll.
const dashboard=await readFile(new URL('./dashboard.html',import.meta.url),'utf8');
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
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
  const show=p=>page.evaluate(p=>{state.model_pause=p;renderLimitBanner();const b=document.querySelector('#limit-banner');
   return {shown:!b.hidden&&b.getBoundingClientRect().height>0,text:b.textContent,wide:document.documentElement.scrollWidth>innerWidth}},p);
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
  r=await show(null);assert.ok(!r.shown,'gone when model_pause is null');
  await context.close()}
 assert.ok(dashboard.includes("usage_limited:'The AI usage limit was reached.'"),'a run that hit the limit says so');
 assert.deepEqual(errors,[]);
 console.log('limit banner dashboard ok');
}finally{await browser?.close();server.close()}
