import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A fresh hosted signup (reviews_auto): reviews turn on by themselves once the AI and mail are connected, so the
// dashboard never says "Reviews are off" or offers "Turn on reviews". While it connects and reads, one progress line;
// "All clear" only after the first read. A step that is really missing is a Needs you line with a link to that step.
const dashboard=await dashboardPage();
const manage='https://control.example/setup',outlook=[{id:'work-outlook',service:'outlook',display_name:'Outlook'}];
let on=false,conns=outlook,look={state:'waiting',why:'sources',days:7},runs=[];
const live=()=>({runs,queue:null,first_look:look});
const state=()=>({suggestions:[],promises:[],connectors:conns,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},
 review_runs:[],review_live:live(),reviews_on:on,reviews_auto:!on,manage_url:manage});
const errors=[];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/reviews/live'){res.end(JSON.stringify(live()));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const open=async()=>{const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#suggestions .first-look-empty, #suggestions .all-clear').first().waitFor();return page};
 const everything=page=>page.evaluate(()=>document.body.innerText);
 const LINE='Reading your mail, first to-dos in a few minutes';
 // Connecting and reading: no source in yet, its first page still coming, settling after it
 for(const why of ['sources','mail','settling']){
  look={state:'waiting',why,days:7};const page=await open();
  const text=await everything(page);
  assert.ok(!/Reviews are off|Turn on reviews|All clear/.test(text),why+': '+text);
  assert.ok((await page.locator('#suggestions').textContent()).includes(LINE),why);
  assert.equal((await page.locator('#suggestions').textContent()).split(LINE).length,2,why+': said once');
  assert.equal(await page.locator('#needs-you').isHidden(),true,why);
  assert.ok((await page.locator('#review-live').textContent()).includes(LINE),why);
  await page.close();
 }
 look=null;let page=await open();  // between the first read and reviews turning on: still not "All clear"
 assert.ok(!/Reviews are off|Turn on reviews|All clear/.test(await everything(page)));
 await page.close();
 // Really missing: the exact step, with a link straight to it, and nothing about reviews
 conns=[];look={state:'waiting',why:'sources',days:7};page=await open();
 assert.equal(await page.locator('#needs-you a',{hasText:'Connect mail'}).getAttribute('href'),manage+'#google');
 assert.ok((await page.locator('#suggestions').textContent()).includes('Your first to-dos show up here'));
 assert.ok(!/Reviews are off|Turn on reviews/.test(await everything(page)));
 await page.close();conns=outlook;
 look={state:'waiting',why:'model',days:7};page=await open();
 assert.equal(await page.locator('#needs-you a',{hasText:'Pick your AI'}).getAttribute('href'),manage+'#model');
 assert.ok(!/Reviews are off|Turn on reviews/.test(await everything(page)));
 await page.close();
 // Reviews on: the normal page again
 on=true;look=null;page=await open();
 assert.ok((await page.locator('#suggestions').textContent()).includes('All clear'));
 assert.ok(!(await everything(page)).includes(LINE));
 await page.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('reviews start by themselves dashboard ok');
