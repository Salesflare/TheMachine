import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do whose moment passed closed by itself (Store.expire_passed): it sits in Done with "No longer needed" and when
// that was, said from the stored time on the day it is read (today, yesterday, or the date), with Undo while it lasts,
// and never Overdue. SHOTS=<folder> saves screenshots, light and dark, at 1440 and 390 wide.
const dashboard=await dashboardPage();
const day=(n,h,m)=>{const d=new Date();d.setDate(d.getDate()+n);d.setHours(h,m,0,0);return d.toISOString()};
const now=new Date().toISOString(),later=new Date(Date.now()+20*3600e3).toISOString();
const expired=(id,title,n,what,undo)=>({id,title,body:'The meeting with Kevin is in your calendar, 13:30 to 15:00. The room is confirmed.',status:'completed',scope:'work',
 created_at:day(n-1,9,0),event_ids:[1],due:day(n,12,0).slice(0,10),expires_at:day(n,13,30),expires_what:what,expired_at:now,undo_until:undo?later:null,closed_at:now});
const cards=[expired('y1','Angular migration with Kevin at the office',-1,'the meeting with Kevin',true),
 expired('t1','Call with Sam',0,'the call with Sam',true),expired('o1','Demo with Noor',-4,'the demo with Noor',false),
 {id:'p1',title:'Reply to Kim about the invoice',body:'Kim asks for the invoice again.',status:'pending',scope:'work',created_at:now,event_ids:[2]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
let posted=null;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/decision'||url.pathname==='/api/action'){try{posted=JSON.parse(body)}catch{}}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const width of [1440,390]){
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#finished-head').click();await page.locator('#task-y1').waitFor();
  const line=id=>page.locator(`#task-${id} .status-line`).textContent();
  assert.equal((await line('y1')).trim(),'No longer needed: the meeting with Kevin was yesterday at 13:30.');
  assert.equal((await line('t1')).trim(),'No longer needed: the call with Sam was today at 13:30.');
  assert.match((await line('o1')).trim(),/^No longer needed: the demo with Noor was on \w{3}, \w{3} \d{1,2} at 13:30\.$/);
  for(const id of ['y1','t1','o1'])assert.ok(!(await page.locator('#task-'+id).innerText()).includes('Overdue'),id);
  // Closed by itself, not by them: the chip says Not needed, never Done
  for(const id of ['y1','t1','o1'])assert.equal((await page.locator(`#task-${id} .card-badges .chip`).first().innerText()).trim(),'Not needed',id);
  // Undo while it lasts, Reopen after
  assert.equal(await page.locator('#task-y1 [data-choice="undo"]').count(),1);
  assert.equal(await page.locator('#task-y1 [data-choice="reopen"]').count(),0);
  assert.equal(await page.locator('#task-o1 [data-choice="undo"]').count(),0);
  assert.equal(await page.locator('#task-o1 [data-choice="reopen"]').count(),1);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(process.env.SHOTS){await page.locator('#task-y1').scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.SHOTS}/expired-${width}-${scheme}.png`});
   await page.locator('#task-y1').screenshot({path:`${process.env.SHOTS}/expired-card-${width}-${scheme}.png`})}
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('moment to-dos dashboard ok');
