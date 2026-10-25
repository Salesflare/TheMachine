import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from './openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// On a phone the side bar's "Offline · updated 10:42" is out of sight, so the same line shows at the top of every
// view (Suggestions, Calendar, Events, Graph, Fleet, Connections, Feedback, Settings), not only Suggestions. On a desktop the
// side bar says it and the line stays hidden. Live again, it goes.
const dashboard=await readFile(new URL('./dashboard.html',import.meta.url),'utf8');
const shots=process.env.SHOTS||'';
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440]){
  const phone=width<1024,context=await browser.newContext({viewport:{width,height:844},isMobile:width<600,hasTouch:width<600}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof staleLine==='function');
  await page.evaluate(()=>staleLine('Offline · updated 10:42'));
  for(const tab of ['inbox','calendar','events','people','fleet','health','feedback','settings']){
   await page.evaluate(t=>t==='settings'?showSettings():document.querySelector(`nav [data-tab="${t}"]`).click(),tab);await page.waitForTimeout(150);
   const r=await page.evaluate(()=>{const n=document.querySelector('#stale-note'),b=n.getBoundingClientRect(),bar=document.querySelector('#topbar')?.getBoundingClientRect();return {shown:!!n.offsetParent&&b.height>0,text:n.textContent,top:b.top,bar:bar?.bottom||0}});
   if(phone){assert.ok(r.shown,`${width} ${tab}: the offline line shows`);assert.equal(r.text,'Offline · updated 10:42');assert.ok(r.top>=r.bar-1&&r.top<r.bar+160,`${width} ${tab}: at the top of the view ${JSON.stringify(r)}`)}
   else assert.ok(!r.shown,`${width} ${tab}: the side bar says it`);
   if(shots)await page.screenshot({path:`${shots}/stale-${tab}-${width}.png`})}
  await page.evaluate(()=>{shownCached=false;lastOk=Date.now();document.querySelector('#live').classList.remove('stale');document.querySelector('#stale-note').hidden=true});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('stale note dashboard ok');
}finally{await browser?.close();server.close()}
