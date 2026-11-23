import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do waiting to be prepared ahead (its turn, or the usage budget holding it) shows Do it: a press starts it now
// (Store._decide). One already running, or prepared, doesn't get it again. While a usage limit holds every run, the
// press says so at once (decide_action's held) instead of a plain "I'll prepare it."
const dashboard=await dashboardPage();
const now=new Date().toISOString(),until=Math.floor(Date.now()/1000)+3600;
const card=(id,extra)=>({id,title:'Reply about the venue '+id,body:'I can draft the reply.',status:'accepted',early:1,scope:'work',created_at:now,event_ids:[1],...extra});
const cards=[card('wait',{preparation_status:'queued',preparation_hold:{why:'budget'}}),card('turn',{preparation_status:'queued'}),
 card('run',{preparation_status:'running',preparation_started_at:now}),card('none',{})];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const posted=[];let hold=null;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){if(hold)await hold;res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const a=JSON.parse(body||'{}');if(a.action==='decide'){posted.push(a.args);res.end(JSON.stringify({status:'accepted',held:{why:'limit',until}}));return}}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1280,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-wait').waitFor();
 const doIt=id=>page.locator(`#task-${id} button[data-choice="accept"]`);
 for(const id of ['wait','turn','none']){
  assert.equal(await doIt(id).count(),1,id+' shows Do it');
  assert.equal((await doIt(id).textContent()).trim(),'Do it');
  assert.match(await doIt(id).getAttribute('class'),/primary/,id+': Do it leads');
 }
 // Waiting, it says so once: its chip isn't Preparing… yet, and only the wait line explains it
 const wait=await page.locator('#task-wait').textContent();
 assert.match(wait,/Saving usage for now/);assert.doesNotMatch(wait,/Preparing/);
 assert.equal((await page.locator('#task-wait .chip').first().textContent()).trim(),'Not started yet');
 assert.match(await page.locator('#task-run').textContent(),/Preparing this ahead, so it arrives ready/);  // once it runs, as before
 assert.equal(await doIt('run').count(),0,'a run under way has no Do it');
 // Pressed, its button goes with the press's own answer, not with the next status (still on its way here): it can't be
 // pressed again and again
 let go;hold=new Promise(r=>go=r);
 await doIt('wait').click();
 await page.waitForFunction(()=>!document.querySelector('#task-wait button[data-choice="accept"]'));
 assert.equal((await page.locator('#task-wait .chip').first().textContent()).trim(),'Preparing…');
 go();hold=null;
 await page.waitForFunction(()=>/Waiting for the usage limit to reset/.test(document.querySelector('#toast')?.textContent||''));
 assert.deepEqual(posted.map(a=>[a.suggestion_id,a.choice]),[['wait','accept']]);
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('do it ahead dashboard ok');
