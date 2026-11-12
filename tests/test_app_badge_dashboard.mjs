import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The installed app's icon badge is the To-dos count in the sidebar: what needs the owner now. Not every open to-do: one
// that looks done, one waiting on others, a snoozed one and one in Personal while Work is shown don't count. Work or
// Personal alone leave the badge as All has it; nothing left clears it.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),soon=new Date(Date.now()+864e5).toISOString();
const cards=[
 {id:'r1',title:'Reply to Noor about the contract',body:'Drafted a short reply.',status:'prepared',scope:'work',created_at:now,event_ids:[1],
  next_actions:[{kind:'email',revision:'v1',label:'Send to Noor',to:['noor@example.com'],to_name:'Noor',subject:'Contract',body:'Hi Noor'}]},
 {id:'p1',title:'Decide on the partnership call',body:'They want a call next week.',status:'pending',scope:'work',created_at:now,event_ids:[2]},
 {id:'p2',title:'Pick a date for the dentist',body:'Two dates are open.',status:'pending',scope:'personal',created_at:now,event_ids:[3]},
 {id:'d1',title:'Fix the signup form error',body:'Merged and deployed.',status:'prepared',scope:'work',created_at:now,event_ids:[4],outcome:JSON.stringify({state:'already_done'}),looks_done_at:now},
 {id:'w1',title:'Hotfix waiting on review',body:'The hotfix waits on review.',status:'prepared',scope:'work',created_at:now,event_ids:[5],outcome:JSON.stringify({state:'waiting',waiting_on:'the review'})},
 {id:'s1',title:'Renew the domain',body:'It runs out next month.',status:'snoozed',scope:'work',created_at:now,snoozed_until:soon,event_ids:[6]},
 {id:'c1',title:'Send the quote',body:'Sent.',status:'completed',scope:'work',created_at:now,closed_at:now,event_ids:[7]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 // The badge calls, as the installed app gets them (a plain tab has no badge to set)
 await context.addInitScript(()=>{window.badgeCalls=[];
  Object.defineProperty(Navigator.prototype,'setAppBadge',{configurable:true,value:n=>{window.badgeCalls.push(n);return Promise.resolve()}});
  Object.defineProperty(Navigator.prototype,'clearAppBadge',{configurable:true,value:()=>{window.badgeCalls.push(0);return Promise.resolve()}})});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 const badge=()=>page.evaluate(()=>window.badgeCalls.at(-1));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-r1').waitFor();
 // 6 open ones, 3 of them need the owner: the sidebar says 3 and so does the badge
 assert.equal(await page.locator('#badge-inbox').textContent(),'3');
 await page.waitForFunction(()=>window.badgeCalls.length>0);
 assert.equal(await badge(),3);
 assert.ok(await page.evaluate(()=>!window.badgeCalls.includes(6)&&!window.badgeCalls.includes(5)));
 // Work alone: the sidebar says 2, the badge keeps All's 3
 await page.locator('[data-scope="work"]').first().click();
 await page.waitForFunction(()=>document.querySelector('#badge-inbox').textContent==='2');
 assert.equal(await badge(),3);
 await page.locator('[data-scope="all"]').first().click();
 await page.waitForFunction(()=>document.querySelector('#badge-inbox').textContent==='3');
 // Handled elsewhere (another tab, the phone): the next refresh brings the badge down with the count, and clears it at 0
 cards.find(c=>c.id==='r1').status='completed';
 await page.reload();await page.locator('#task-p1').waitFor();
 await page.waitForFunction(()=>window.badgeCalls.at(-1)===2);
 for(const id of ['p1','p2'])cards.find(c=>c.id===id).status='rejected';
 await page.reload();
 await page.waitForFunction(()=>document.querySelector('#badge-inbox').textContent===''&&window.badgeCalls.at(-1)===0);
 assert.ok(await page.evaluate(()=>window.badgeCalls.every(n=>n===0)));
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('app badge dashboard ok');
