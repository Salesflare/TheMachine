import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A test run's result shows even when a look at it fails (dashboard/routines-page.js routinesView): the 4 s looks while a
// run is in progress keep going, slower, after a reading that failed, without a toast. One lost reading (a connection that
// timed out after 30 s, the Machine heard just before) left the card on Running… with its result already saved.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),ID='d4'.repeat(16);
let test=null,fail=0,reads=0;const held=[];
const mine=()=>({id:ID,name:'Shipped this week',instructions:'Check what shipped in the project repository and write a short post',rule:{unit:'week',n:1},
 anchor:'2026-11-13',at:'16:00',state:'on',next_due:'2026-11-13',runs:[{id:'r1',state:'ready',started_at:now,result:'**Three things shipped**.'}],test});
const all=()=>JSON.stringify({routines:[mine()],suggested:[],trying:[]});
const state={suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/routines'){reads++;if(fail>0){fail--;held.push(res);return}res.end(all());return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);if(b.action==='routine_try')test={id:'t1',state:'running',started_at:now,trial:b.args.words};res.end(all());return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.clock.install();
 await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
 const card=page.locator(`[data-rt="${ID}"]`);await card.waitFor();
 await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="edit"]').click();
 await card.locator('.rt-form textarea').fill('Check what shipped in the project repository and write a short, playful post');
 await card.locator('[data-rt-try]').click();await card.locator('.rt-form .rt-run').waitFor();
 assert.match(await card.locator('.rt-form .rt-run-head').innerText(),/^Test run\s+Running…$/);
 // The next two looks hang for 30 s and then time out, then the run is ready: its result still shows, with no toast
 fail=2;test={...test,state:'ready',result:'**Two things shipped** this week.'};
 const before=reads,drop=async()=>{for(let i=0;i<40&&!held.length;i++){await page.clock.runFor(1000);await page.waitForTimeout(20)}
  await page.clock.runFor(31000);const r=held.shift();r?.writeHead(504);r?.end(JSON.stringify({error:'Timed out'}));await page.waitForTimeout(150)};
 await drop();await drop();
 assert.equal(fail,0,'it looked again after a failed look');
 await page.clock.runFor(16000);await card.locator('.rt-form .rt-result strong').waitFor({timeout:5000});
 assert.ok(reads-before>=3,'looked again until it read the result');
 assert.equal(await page.locator('.toast').filter({hasText:/\S/}).count(),0,'a failed background look shows no toast');
 // Ready now: no more looks
 const after=reads;await page.clock.runFor(60000);await page.waitForTimeout(150);
 assert.equal(reads,after,'stops looking once nothing runs');
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
