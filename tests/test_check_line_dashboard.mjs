import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The To-dos head's line next to Check now (dashboard/todos-check.js) calls the periodic pass a check, never a review:
// "Checked 21:10 · next by 21:26 · 2 new", and while one runs the robot's own words, the same in the head and under it.
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
 // checkNow: the one state everything shows (the head's line, the robot and its line), and when the head says it.
 const now=(c,worker)=>page.evaluate(([c,worker])=>{state.check=c;state.review_health={worker};const n=checkNow();return [n.kind,n.line.replace(/ /g,' ')]},[c,worker]);
 assert.deepEqual(await now({reviewed:at(-2),waiting:2,next_review:at(14)}),['ok',''],'a check on time says nothing');
 assert.deepEqual(await now({reviewed:at(-2),waiting:0},{status:'ok'}),['ok','']);
 assert.ok(['Snooping around your messages…','Rummaging through the new stuff…'].includes((await now({phase:'reviewing',reviewed:at(-2)}))[1]));
 assert.deepEqual(await now({phase:'reading',reviewed:at(-2),waiting:7}),['busy','Nosing through 7 new messages…']);
 assert.deepEqual(await now({reviewing:true,reviewed:at(-2),waiting:1}),['busy','Nosing through 1 new message…'],'a review the button did not start is busy too');
 assert.deepEqual(await now({waiting:3,next_review:at(14)}),['first','Next check by 21:26 · 3 new']);
 assert.deepEqual(await now({reviewed:at(-30),waiting:0},{status:'error',review_saved:false}),['failed','The last check failed.']);
 assert.deepEqual(await now({reviewed:at(-30),waiting:0},{status:'recovering'}),['ok',''],'a pause that retries by itself is not a failure');
 assert.deepEqual(await now({reviewed:at(-40),waiting:5,next_review:at(-15)}),['late','Last checked 20:32. The next check is late.']);
 assert.deepEqual(await now({reviewed:at(-20),waiting:5,next_review:at(-5)}),['ok',''],'a few minutes over is not late');
 assert.deepEqual(errors,[]);
 console.log('ok: the check line says checked, never reviewed');
}finally{await browser?.close();server.close()}
