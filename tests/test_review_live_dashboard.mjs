import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Reviews while they happen: a running review sits at the top of Connections with its progress and its own steps
// (latest visible, earlier ones folded), updates live, and once finished becomes the review's own row (a run that saved
// its review cleanly is not repeated under Recent runs). The first look is the Suggestions empty state while no cards exist. Nothing is sent anywhere: the fixture server answers everything.
const dashboard=await dashboardPage();
const started=new Date(Date.now()-3*60e3).toISOString();
let run={run_id:'r1',status:'running',started_at:started,preview:1,auto:1,planned:40,done_count:12,claimed_count:20,account_ids:['gmail'],
 steps:[{title:'Suggesting: Reply to Globex about the renewal',at:started},{title:'Reading 20 emails',at:started}]};
let live=()=>({runs:run?[run]:[],queue:null,first_look:null});
const state=()=>({suggestions:[],promises:[],connectors:[{id:'gmail',display_name:'Work mail',service:'gmail'}],suggestion_counts:{},decisions:[],
 analyses:run?[{status:'running',items:'[]',started_at:started,attempts:1}]:[{status:'complete',items:'[{"id":1}]',started_at:started,attempts:1,checked_count:40,summary:'Done.'}],
 deliveries:[],review_health:{},review_runs:[{...run,run_id:'r1',status:run?'running':'ok',review_saved:!run,checked_count:40,pending_count:0,duration_seconds:300}],
 review_live:live()});
const errors=[];let polls=0;
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/reviews/live'){polls++;res.end(JSON.stringify(live()));return}
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
 const banner=page.locator('#suggestions .first-look-empty');
 await banner.waitFor();
 assert.match(await banner.textContent(),/Taking a first look at your last 7 days.*12 of 40 signals.*Nothing is sent/);
 assert.equal(await page.locator('#suggestions').textContent().then(t=>t.includes('All clear')),false);
 assert.equal(await page.locator('#first-look').isHidden(),true);
 const top=page.locator('#review-live .review-live');
 assert.equal(await top.count(),1);
 const text=await top.textContent();
 assert.ok(text.includes('First look: your last 7 days')&&text.includes('12 of 40')&&text.includes('Work mail'),text);
 assert.equal(await top.locator(':scope > ul.steps li').allTextContents().then(x=>x.join('|')),'Suggesting: Reply to Globex about the renewal');
 assert.equal(await top.locator('details.earlier-steps').evaluate(d=>d.open),false);
 assert.deepEqual(await top.locator('details.earlier-steps li').allTextContents(),['Reading 20 emails']);
 assert.equal(await page.locator('#review-runs > div:not(.muted)').count(),0);  // running: only at the top, not under Recent runs
 assert.equal(await page.locator('#analyses > div:not(.muted)').count(),0);
 // Live: a new step and more progress arrive without a full refresh
 run={...run,done_count:24,steps:[{title:'3 suggestions so far',at:started},...run.steps]};
 for(let i=0;i<80&&!(await top.textContent()).includes('24 of 40');i++)await page.waitForTimeout(100);
 assert.ok((await top.textContent()).includes('24 of 40'));
 assert.equal(await top.locator(':scope > ul.steps li').textContent(),'3 suggestions so far');
 // Finished: it leaves the top and becomes the normal row below
 run=null;
 for(let i=0;i<80&&await page.locator('#review-live .review-live').count();i++)await page.waitForTimeout(100);
 assert.equal(await page.locator('#review-live .review-live').count(),0);
 assert.equal(await page.locator('#review-runs > div:not(.muted)').count(),0);  // saved cleanly: only the review row
 assert.ok((await page.locator('#analyses').textContent()).includes('Reviewed'));
 assert.equal(await banner.count(),0);
 assert.ok((await page.locator('#suggestions').textContent()).includes('All clear'));
 // Waiting: the next review and the first look say when they start
 live=()=>({runs:[],queue:{waiting:23,planned:23,starts_at:new Date(Date.now()+9*60e3).toISOString(),why:'gap'},first_look:null});
 await page.evaluate(()=>refresh());
 assert.match(await page.locator('#review-live').textContent(),/23 messages waiting for the next review.*Starts in 9 minutes/);
 // A new mailbox: the first review waits for its import, then starts at once
 live=()=>({runs:[],queue:{waiting:12,planned:12,starts_at:null,why:'mail',first:true},first_look:null});
 await page.evaluate(()=>refresh());
 assert.match(await page.locator('#review-live').textContent(),/First review starts when your mail is in.*12 messages so far/);
 assert.match(await page.locator('#review-summary').textContent(),/The first one starts when your mail is in\./);
 live=()=>({runs:[],queue:{waiting:0,planned:0,starts_at:null,why:'mail',first:false},first_look:null});
 await page.evaluate(()=>refresh());
 assert.match(await page.locator('#review-live').textContent(),/Next review starts when your new mail is in.*Importing your mail/);
 live=()=>({runs:[],queue:{waiting:2,planned:2,starts_at:new Date().toISOString(),why:'mail_in',first:true},first_look:null});
 await page.evaluate(()=>refresh());
 assert.match(await page.locator('#review-live').textContent(),/2 messages waiting for their first review.*Your mail is in\. Starting now/);
 live=()=>({runs:[],queue:null,first_look:{state:'waiting',why:'settling',days:7,waiting:30}});
 await page.evaluate(()=>refresh());
 assert.ok((await page.locator('#review-live').textContent()).includes('once the first import settles'));
 assert.ok((await banner.textContent()).includes('starts soon')&&(await banner.textContent()).includes('first import settles'));
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({live_polls:polls,page_errors:errors}));
}finally{
 await browser?.close();server.close();
}
