import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The first look's ending (state.first_look_done): the header never says "All clear" while it still looks; once it is
// done with nothing for the owner, the list says what it read in counts with one or two next steps (not the sleepy
// "Nothing to report"); with to-dos, one line above them says what it read and found. Made-up fixtures, nothing sent.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const card={id:'ab'.repeat(8),title:'Reply to Robin about the garden plan',body:'Robin asked for the dates.',status:'pending',scope:'personal',created_at:now,event_ids:[1]};
let run={run_id:'r1',status:'running',started_at:now,preview:1,auto:1,window_hours:168,planned:8,done_count:0,claimed_count:8,account_ids:['work'],steps:[]};
let done=null,cards=[],model=null;
const live=()=>({runs:run?[run]:[],queue:null,first_look:null});
const state=()=>({suggestions:cards,promises:[],connectors:[{id:'work',display_name:'Work mail',service:'outlook'},{id:'work-cal',display_name:'Work calendar',service:'outlook_calendar'}],
 suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:run?{}:{last_completed:now},review_runs:[],reviews_on:true,greeting:{name:'Robin'},
 review_live:live(),first_look_done:done,...(model?{model_status:model}:{})});
const errors=[],plain=s=>s.replace(/\u00a0/g,' ');  // a count keeps its word on the same line (a non-breaking space)
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/reviews/live'){res.end(JSON.stringify(live()));return}
 if(url.pathname==='/api/action'){res.end(JSON.stringify({sources:[]}));return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.locator('#suggestions .first-look-empty').waitFor();
 // While it looks: the hello, never "All clear" in the header
 assert.equal(await page.locator('#page-head .page-title').innerText(),'Hi Robin');
 assert.ok(!/All clear/.test(await page.locator('#page-head').innerText()),await page.locator('#page-head').innerText());
 // Done, nothing for the owner: what it read, in counts, and the next steps that fit (one mailbox; Talk can't run here)
 run=null;done={at:now,days:7,kinds:{email:8},read:{newsletters:5,notifications:3},todos:0,acted:false,next:['inbox']};
 await page.evaluate(async()=>{await refresh()});
 const end=page.locator('#suggestions .first-look-end');
 await end.waitFor();
 assert.equal(plain(await end.locator('.fl-read').innerText()),'Read 8 emails from the past week: 5 newsletters and 3 notifications.');
 assert.ok((await end.innerText()).includes('New mail gets a look as it comes in.'));
 assert.deepEqual(await end.locator('[data-fl-next]').allInnerTexts(),['Add another inbox','Give me a to-do']);
 assert.equal(await page.locator('#suggestions img.sleepy').count(),0);
 assert.ok(!/Nothing to report|Back to my nap|All quiet/.test(await page.locator('#suggestions').innerText()));
 // Add another inbox leads to Connections, + Add
 await end.locator('[data-fl-next="inbox"]').click();
 await page.waitForFunction(()=>!document.querySelector('#health').hidden);
 // No groups from the reviewer: the counts by kind alone; a calendar missing comes first
 done={...done,kinds:{email:8,meeting:2},read:{},next:['calendar','inbox']};
 await page.evaluate(async()=>{document.querySelector('nav button[data-tab="inbox"]').click();await refresh()});
 await page.waitForFunction(()=>/meetings/.test(document.querySelector('#suggestions .fl-read')?.textContent||''));
 assert.equal(plain(await end.locator('.fl-read').innerText()),'Read 8 emails and 2 meetings from the past week.');
 assert.deepEqual(await end.locator('[data-fl-next]').allInnerTexts(),['Connect your calendar','Add another inbox']);
 // A service that mails the owner often and isn't connected (first_look_connect) comes first, as a concrete offer
 done={...done,connect:[{service:'slack',label:'Slack'}],next:['calendar']};
 await page.evaluate(async()=>{await refresh()});
 await page.waitForFunction(()=>/Slack/.test(document.querySelector('#suggestions .fl-next')?.textContent||''));
 assert.deepEqual(await end.locator('.fl-next button').allInnerTexts(),['Connect Slack','Connect your calendar']);
 assert.equal(await end.locator('[data-connect-open="slack"]').count(),1);
 // Nothing to connect, with a model: one question to ask instead of an empty "Give me a to-do"; it fills Search's ask
 done={...done,connect:[],next:[]};model={ok:true};
 await page.evaluate(async()=>{await refresh()});
 await page.waitForFunction(()=>/Ask what changed/.test(document.querySelector('#suggestions .fl-next')?.textContent||''));
 assert.deepEqual(await end.locator('.fl-next button').allInnerTexts(),['Ask what changed this week']);
 await end.locator('[data-fl-next="ask"]').click();
 await page.waitForFunction(()=>document.querySelector('#palette')?.open);
 assert.equal(await page.locator('#pal-q').inputValue(),'what changed this week?');
 await page.keyboard.press('Escape');model=null;
 // Done with to-dos: one line above them, gone once the owner acted on one
 cards=[card];done={...done,todos:1,next:[]};
 await page.evaluate(async()=>{await refresh()});
 const note=page.locator('#suggestions .first-look-note');
 await note.waitFor();
 assert.equal(plain(await note.innerText()),'Read 8 emails and 2 meetings from the past week and found 1 to-do.');
 assert.equal(await end.count(),0);
 done={...done,todos:3};await page.evaluate(async()=>{await refresh()});
 assert.equal(plain(await note.innerText()),'Read 8 emails and 2 meetings from the past week and found 3 to-dos.');
 done={...done,acted:true};await page.evaluate(async()=>{await refresh()});
 assert.equal(await note.count(),0);
 // Past its day: the usual All clear again
 cards=[];done=null;await page.evaluate(async()=>{await refresh()});
 await page.locator('#suggestions img.sleepy').waitFor();
 assert.equal(await page.locator('#page-head .page-sub').count(),0,'the sections carry the counts');
 assert.ok((await page.locator('#suggestions .all-clear .poke-line').innerText()).length>0,'the robot says all clear');
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
