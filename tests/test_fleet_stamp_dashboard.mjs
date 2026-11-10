import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Fleet's to-dos come from api/fleet (some 80 KB on a busy Machine), which the to-do list fetched on every redraw at
// most every 20 seconds. Off the Fleet tab it is fetched again only when the status's marker (fleet.stamp) changed; a
// status without one (an older Machine) fetches as before, and so does the Fleet tab while it is open.
const dashboard=await dashboardPage();
const FL='fl_'+'d'.repeat(16);
const ask=(id,name)=>({id,fleet:FL,kind:'relationships',name,question:'Do we know anyone at client.example?',at:new Date().toISOString(),status:'waiting'});
const fleet={on:true,kinds:{relationships:'Relationships'},kind_rules:{},no_details:[],scoped:[],scopes:{},waiting:[ask('q1','Pat Lane')],asked:[],log:[],notices:[],
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:['relationships'],people:[],members:[],rules:{},exceptions:{}}]};
let stamp='1.2026111014';
const state=()=>({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
 fleet:{on:true,waiting:fleet.waiting.length,...(stamp==null?{}:{stamp})}});
const asked=[];
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');asked.push(url.pathname);res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status')return res.end(JSON.stringify(state()));
 if(url.pathname==='/api/fleet')return res.end(JSON.stringify(fleet));
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const fleets=()=>asked.filter(p=>p==='/api/fleet').length;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 const origin='http://127.0.0.1:'+server.address().port;
 // a status poll 20 seconds on (the wait between fetches let go), and its redraws done
 const poll=async()=>{await page.evaluate(async()=>{fleetAt=0;await refresh(true);render();await (fleetLoading||Promise.resolve())});await page.waitForTimeout(150)};
 // 1. A load: the Fleet's to-dos come once
 await page.goto(origin);await page.locator('#fleet-q1').waitFor();
 assert.equal(fleets(),1,'once on a load: '+asked.join(' '));
 // 2. Polls and redraws with the same marker: no new fetch (each was one before)
 for(let i=0;i<3;i++)await poll();
 assert.equal(fleets(),1,'the same marker: not fetched again: '+asked.join(' '));
 // 3. The marker changed (a teammate asked): fetched once, and the new item shows
 fleet.waiting.push(ask('q2','Kim Ito'));stamp='2.2026111014';
 await poll();await page.locator('#fleet-q2').waitFor();
 assert.equal(fleets(),2,'a new marker: fetched once');
 await poll();assert.equal(fleets(),2);
 // 4. A status without a marker (an older Machine): every 20 seconds, as before
 stamp=null;await poll();await poll();
 assert.equal(fleets(),4,'no marker: fetched each time');
 // 5. On the Fleet tab: fetched as before, whatever the marker says
 stamp='3.2026111014';await poll();const before=fleets();
 await page.evaluate(()=>document.querySelector('nav [data-tab="fleet"]').click());await page.waitForTimeout(500);
 assert.ok(fleets()>before,'opening the Fleet tab fetches it');
 const open=fleets();await poll();
 assert.ok(fleets()>open,'the open Fleet tab keeps fetching');
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
