import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's chat the Machine can't read (every card_chat answers an error) isn't asked again every 4 seconds while it
// stays open: each failed read waits twice as long as the one before, up to a minute. Once a read works again, the
// chat is read at its usual pace.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),T0=Date.parse('2026-11-13T12:00:00Z');
const cards=[{id:'a1a1a1a1a1a1a1a1',title:'Check the payroll is ready',body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]}});
let reads=0,broken=true;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);
  if(r.action==='card_chat'){reads++;
   if(broken){res.statusCode=400;res.end(JSON.stringify({error:'That didn’t work. Try again in a moment.'}));return}
   res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k',items:[{kind:'reply',text:'The payroll is ready.',at:T0}]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.clock.install({time:T0});
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
 await page.locator('#task-a1a1a1a1a1a1a1a1 .card-foot a.card-chat-link').click();
 await page.locator('.chat-layout[data-chat="a1a1a1a1a1a1a1a1"]').waitFor();
 const run=async ms=>{for(let t=0;t<ms;t+=500){await page.clock.runFor(500);await page.waitForTimeout(5)}};
 await run(1000);reads=0;
 // Two minutes: every 4 s would be 30 reads; backing off (4, 8, 16, 32, 60 s) is a handful
 await run(120000);
 assert.ok(reads>=2&&reads<=6,`failed reads back off (${reads} in two minutes)`);
 // Working again: the next read gets the chat, and the reads after it come at the usual pace (every 10 s)
 broken=false;await run(61000);
 await page.locator('#chat-log .chat-msg').first().waitFor();
 reads=0;await run(30000);
 assert.ok(reads>=2&&reads<=4,`a chat read again reads at its usual pace (${reads} in 30 s)`);
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
