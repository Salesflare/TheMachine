import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The To-dos head's line next to Check now (dashboard/todos-check.js) calls the periodic pass a check, never a review:
// "Checked 21:10 · next by 21:26 · 2 new", "Checking messages…" while one runs, and the same words in every state.
const dashboard=await dashboardPage();
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const NOW=Date.parse('2026-11-06T21:12:00Z'),at=m=>new Date(NOW+m*6e4).toISOString();
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},locale:'en-GB',timezoneId:'UTC'}),page=await context.newPage();
 await context.clock.setFixedTime(NOW);
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof checkLine==='function');
 await page.evaluate(()=>applyLocale({date_locale:'en-GB',hour12:false}));
 const line=c=>page.evaluate(c=>checkLine(c).replace(/ /g,' '),c);
 assert.equal(await line({reviewed:at(-2),waiting:2,next_review:at(14)}),'Checked 21:10 · next by 21:26 · 2 new');
 assert.equal(await line({reviewed:at(-2),waiting:2,soon:true}),'Checked 21:10 · next soon · 2 new');
 assert.equal(await line({reviewed:at(-2),waiting:0}),'Checked 21:10');
 assert.equal(await line({waiting:3,next_review:at(14)}),'Next check by 21:26 · 3 new');
 assert.equal(await line({waiting:1}),'Next check soon · 1 new');
 assert.equal(await line({phase:'reviewing',reviewed:at(-2),waiting:2}),'Checking messages…');
 assert.equal(await line({phase:'reading'}),'Reading sources…');
 assert.deepEqual(errors,[]);
 console.log('ok: the check line says checked, never reviewed');
}finally{await browser?.close();server.close()}
