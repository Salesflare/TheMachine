import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {chromium} from './browser.mjs';
import {dashboardPage} from './dashboard-page.mjs';

// The footer's line of the day jokes from the owner's side, never about who made the app: "© 2026 The Machine. No inboxes
// were harmed." reads in every language, in at most two lines on a phone beside the stacked Help and other links.
const dashboard=await dashboardPage(),LANGS=['en','de','es','fr','it','nl','pt-BR'],cats={};
for(const l of LANGS)cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const LINE='No inboxes were harmed.';
for(const l of LANGS)assert.ok(JSON.parse(cats[l])[LINE],`${l} has the footer line`);
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid'),m=url.pathname.match(/^\/i18n\/([A-Za-z-]+)\.json$/);
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');
 if(m&&cats[m[1]]){res.end(cats[m[1]]);return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,DAY=864e5;
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const seen=new Set();
 // Every day of the rotation: the year and The Machine, then one line, never the one about its makers
 for(let d=0;d<8;d++){
  const context=await browser.newContext({viewport:{width:1440,height:900}}),page=await context.newPage();
  await page.clock.setFixedTime(Date.UTC(2026,10,12,12)+d*DAY);await page.goto(base+'/');await page.waitForFunction(()=>typeof showTab==='function');
  const text=await page.locator('#copyright').textContent();
  assert.match(text,/^© 2026 The Machine\. \S/,text);assert.doesNotMatch(text,/robot|handcrafted/i,text);seen.add(text);
  await context.close();
 }
 assert.ok(seen.has('© 2026 The Machine. '+LINE),[...seen].join(' | '));
 // The day it shows, on a phone, in each language: translated, and one line
 const day=Math.floor(Date.UTC(2026,10,12,12)/DAY);let at=0;
 for(let d=0;d<8;d++){const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();
  await page.clock.setFixedTime((day+d)*DAY+12*36e5);await page.goto(base+'/');await page.waitForFunction(()=>typeof showTab==='function');
  const text=await page.locator('#copyright').textContent();await context.close();if(text.endsWith(LINE)){at=(day+d)*DAY+12*36e5;break}}
 assert.ok(at,'a day shows the line');
 for(const l of LANGS){
  const context=await browser.newContext({viewport:{width:390,height:844},colorScheme:'light'}),page=await context.newPage();
  await page.clock.setFixedTime(at);await page.goto(base+'/');await page.waitForFunction(()=>typeof showTab==='function');
  await page.evaluate(lang=>i18nLoad(lang),l);
  const got=await page.evaluate(()=>{const p=document.querySelector('#copyright'),lh=parseFloat(getComputedStyle(p).lineHeight);
   return {text:p.textContent,lines:Math.round(p.getBoundingClientRect().height/lh),page:document.documentElement.scrollWidth}});
  assert.equal(got.text,'© 2026 The Machine. '+JSON.parse(cats[l])[LINE],l);
  assert.ok(got.lines<=2,`${l}: "${got.text}" on at most two lines at 390 (${got.lines})`);
  assert.ok(got.page<=390,`${l}: no sideways scroll`);
  await context.close();
 }
 console.log('footer line dashboard ok');
}finally{await browser?.close();server.close()}
