import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Opening or closing a to-do's chat redraws only what it changes (the to-do list, the sidebar, the chat): Learning,
// the Updated line and the rest of the page stay as they are drawn, when the data is the same. New data from a
// refresh still redraws all of it.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),t0=Date.now()-60000;
const cards=[
 {id:'a1a1a1a1a1a1a1a1',title:'Check the payroll is ready',body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1]},
 {id:'b2b2b2b2b2b2b2b2',title:'Renew the passport',body:'It runs out in May.',status:'pending',scope:'personal',created_at:now,event_ids:[2]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k',items:[{kind:'reply',text:'The payroll is ready.',at:t0}]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
 // The Updated line is drawn on each whole render: its node is marked, and a redraw replaces it
 const mark=()=>page.evaluate(()=>{document.querySelector('#updated').firstChild.marked=true});
 const kept=()=>page.evaluate(()=>!!document.querySelector('#updated').firstChild?.marked);
 await mark();
 await page.locator('#task-a1a1a1a1a1a1a1a1 .card-foot a.card-chat-link').click();
 await page.locator('.chat-layout[data-chat="a1a1a1a1a1a1a1a1"] #chat-log .chat-msg').first().waitFor();
 assert.ok(await kept(),'opening a chat leaves the rest of the page as drawn');
 await page.locator('nav [data-tab="inbox"]').click();
 await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
 assert.ok(await kept(),'closing it too');
 assert.equal(await page.locator('#suggestions article.card').count(),2,'the to-do list is back');
 // New data: a refresh redraws the whole page, and a chat opened after it still shows the new to-do
 cards.push({id:'c3c3c3c3c3c3c3c3',title:'Book the venue',body:'Two options.',status:'pending',scope:'work',created_at:now,event_ids:[3]});
 await page.evaluate(()=>refresh());
 await page.locator('#task-c3c3c3c3c3c3c3c3').waitFor();
 assert.ok(!await kept(),'a refresh with new data redraws it');
 await mark();
 // A tap within 250 ms of a scroll doesn't open a chat (it stops a fling): the link is scrolled to first, then tapped
 await page.locator('#task-c3c3c3c3c3c3c3c3 .card-foot a.card-chat-link').scrollIntoViewIfNeeded();await page.waitForTimeout(300);
 await page.locator('#task-c3c3c3c3c3c3c3c3 .card-foot a.card-chat-link').click();
 await page.locator('.chat-layout[data-chat="c3c3c3c3c3c3c3c3"]').waitFor();
 assert.match(await page.locator('.chat-layout').textContent(),/Book the venue/);
 assert.ok(await kept(),'and the next chat open leaves it again');
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
