import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's row of actions is measured (does Snooze still fit, actionsSize) when it is drawn anew, when something in
// it changes and when its width does: not every row on each change anywhere in the page, nor a list put back after a
// chat at the width it had. Each measuring is a forced layout.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),t0=Date.now()-60000;
const cards=Array.from({length:6},(_,i)=>({id:String(i+1).repeat(16),title:'To-do number '+(i+1),body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[i+1]}));
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k',items:[{kind:'reply',text:'Ready.',at:t0}]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-1111111111111111').waitFor();
 const rows=await page.locator('#suggestions .card .actions[data-fit]').count();
 assert.ok(rows>=6,'each to-do’s row is fitted: '+rows);
 // Count the measurings from here on (actionsSize is a page-wide function, so the observers call this one)
 await page.evaluate(()=>{window.sized=[];const was=actionsSize;window.actionsSize=a=>{sized.push(a.closest('article')?.id);was(a)}});
 const settle=()=>page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(r,50)))));
 const take=()=>page.evaluate(()=>sized.splice(0));
 await settle();await take();
 // 1. A change elsewhere in the page measures no row
 await page.evaluate(()=>{const p=document.createElement('p');p.textContent='elsewhere';document.body.append(p);p.textContent='changed'});
 await settle();
 assert.deepEqual(await take(),[],'a change outside the rows measures none');
 // 2. A change in one row measures that row only
 await page.evaluate(()=>{const b=document.querySelector('#task-3333333333333333 .actions button');b.append(document.createTextNode(''))});
 await settle();
 assert.deepEqual([...new Set(await take())],['task-3333333333333333'],'a change in a row measures that row');
 // 3. A chat's open and close puts the rows back at their width: none measured
 await page.locator('#task-1111111111111111 .card-foot a.card-chat-link').click();
 await page.locator('.chat-layout[data-chat="1111111111111111"]').waitFor();
 await page.locator('nav [data-tab="inbox"]').click();await page.locator('#task-1111111111111111').waitFor();
 await settle();
 assert.deepEqual(await take(),[],'a list put back measures no row');
 // 4. A new width measures them all again, and a row that no longer fits folds its Snooze into the menu
 await page.setViewportSize({width:390,height:900});await settle();
 assert.ok((await take()).length>=6,'a narrower page measures every row');
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
