import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
import {trackRequests} from './page-calls.mjs';
const {chromium}=await import('./browser.mjs');

// Settings, General, Voice input reads voice_status once when General opens, not with every change under Settings.
// settingsSync follows every change there (this list's own render among them); it used to ask again each time past
// 30 s, and right away after a failed answer, which made thousands of asks a minute with Settings idle. Now: one ask
// per opening, every 2 s while OpenAI's answer is still out (for 30 s at most), 30 s after a failed ask, none when idle.
// The page's clock is a fake one, so a minute takes a moment.
const dashboard=await dashboardPage();
let mode='ok';
const view=()=>({engine:'auto',model:'small',language:'',local:{state:'ready'},openai:mode==='checking'?null:false,in_use:'local',use:'local',
 talk_voice:'cedar',max_seconds:120,languages:['en'],models:['small','base'],talk:{ready:mode==='checking'?null:true,limit:600,warn:540}});
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
let asks=0;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'&&JSON.parse(body).action==='voice_status'){asks++;
  if(mode==='fail'){res.statusCode=500;res.end(JSON.stringify({error:'Voice isn’t available.'}));return}
  res.end(JSON.stringify(view()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 const open=trackRequests(page);
 // Until what the page started has been answered (a call of its own, made after, has come back) and no request is in
 // flight, or the asks run away, as they did
 const settled=async from=>{await page.evaluate(()=>fetch('ping').then(r=>r.text()));
  for(const end=Date.now()+5000;Date.now()<end&&asks-from<200;){if(!open())return;await new Promise(r=>setTimeout(r,20))}};
 // A minute of Settings sitting open, a second at a time: the asks it made
 const minute=async()=>{const from=asks;for(let s=0;s<60&&asks-from<200;s++){await page.clock.runFor(1000);await settled(from)}return asks-from};
 const asked=async run=>{const from=asks;await run();await settled(from);return asks-from};
 await page.clock.install();
 await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
 assert.equal(asks,0,'no Settings, no voice_status');

 // 1. Opening General asks once; a minute idle asks nothing, nor do changes under Settings or status polls
 assert.equal(await asked(()=>page.evaluate(()=>showSettings('general'))),1,'one ask on opening');
 await page.locator('#dictation-engine').waitFor();
 assert.equal(await minute(),0,'none in an idle minute');
 assert.equal(await asked(async()=>{await page.clock.runFor(31000);await page.evaluate(async()=>{const p=document.createElement('p');$('#settings').append(p);await refresh(true);p.remove()})}),0,
  'a change under Settings asks nothing');

 // 2. Back to General from another tab, or Settings opened again: one ask each
 assert.equal(await asked(()=>page.evaluate(()=>showSettings('writing'))),0);
 assert.equal(await asked(()=>page.evaluate(()=>showSettings('general'))),1,'General again: one ask');
 assert.equal(await asked(()=>page.evaluate(()=>document.querySelector('nav button[data-tab]').click())),0);
 assert.equal(await asked(()=>page.evaluate(()=>showSettings('general'))),1,'Settings again: one ask');
 assert.equal(await minute(),0);

 // 3. A failed ask: again after 30 s while General is open, never in a loop
 mode='fail';await page.evaluate(()=>document.querySelector('nav button[data-tab]').click());
 assert.equal(await asked(()=>page.evaluate(()=>showSettings('general'))),1);
 const failed=await minute();assert.ok(failed<=2,`at most every 30 s after a failure, asked ${failed} times in a minute`);

 // 4. OpenAI's answer still out: every 2 s, for 30 s, then it waits for the next opening
 mode='checking';await page.evaluate(()=>document.querySelector('nav button[data-tab]').click());
 assert.equal(await asked(()=>page.evaluate(()=>showSettings('general'))),1);
 const checking=await minute();assert.ok(checking>=10&&checking<=16,`every 2 s for 30 s while checking, asked ${checking} times`);
 assert.equal(await minute(),0,'then none');
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
