import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The to-do list a chat takes the place of is kept aside and put back when the chat closes: the same cards, not built
// again. What changed while the chat was open is new (a to-do's new title, one that came in, one that went).
const dashboard=await dashboardPage();
const now=new Date().toISOString(),t0=Date.now()-60000;
const cards=[
 {id:'a1a1a1a1a1a1a1a1',title:'Check the payroll is ready',body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1]},
 {id:'b2b2b2b2b2b2b2b2',title:'Renew the passport',body:'It runs out in May.',status:'pending',scope:'personal',created_at:now,event_ids:[2]},
 {id:'c3c3c3c3c3c3c3c3',title:'Book the venue',body:'Two options.',status:'pending',scope:'work',created_at:now,event_ids:[3]}];
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
 const mark=()=>page.evaluate(()=>{for(const c of document.querySelectorAll('#suggestions article.card'))c.marked=true});
 const kept=()=>page.evaluate(()=>Object.fromEntries([...document.querySelectorAll('#suggestions article.card')].map(c=>[c.id.slice(5,9),!!c.marked])));
 // A tap within 250 ms of a scroll doesn't open a chat (it stops a fling): the link is scrolled to first, then tapped
 const open=async id=>{const link=page.locator(`#task-${id} .card-foot a.card-chat-link`);await link.scrollIntoViewIfNeeded();await page.waitForTimeout(300);await link.click();await page.locator(`.chat-layout[data-chat="${id}"]`).waitFor()};
 const back=async()=>{await page.locator('nav [data-tab="inbox"]').click();await page.locator('#suggestions article.card').first().waitFor()};
 await mark();
 // 1. Open and close: the same cards are back
 await open('a1a1a1a1a1a1a1a1');
 assert.equal(await page.locator('#suggestions article.card').count(),0,'the chat takes the list’s place');
 await back();
 assert.deepEqual(await kept(),{a1a1:true,b2b2:true,c3c3:true},'the cards are the ones drawn before');
 // 2. A refresh while the chat is open: a new title, a new to-do and one gone show once it closes; the rest is kept
 await open('a1a1a1a1a1a1a1a1');
 cards[1].title='Renew the passport before May';cards.splice(2,1);
 cards.push({id:'d4d4d4d4d4d4d4d4',title:'Send the invoice',body:'It is due.',status:'pending',scope:'work',created_at:now,event_ids:[4]});
 await page.evaluate(()=>refresh());
 await page.locator('.chat-layout[data-chat="a1a1a1a1a1a1a1a1"]').waitFor();
 await back();
 await page.locator('#task-d4d4d4d4d4d4d4d4').waitFor();
 assert.equal(await page.locator('#task-c3c3c3c3c3c3c3c3').count(),0,'the one that went is gone');
 assert.match(await page.locator('#task-b2b2b2b2b2b2b2b2').textContent(),/before May/,'the new title shows');
 const after=await kept();
 assert.equal(after.a1a1,true,'an unchanged card is kept');
 assert.equal(after.d4d4,false,'the new one is drawn');
 // 3. A chat opened and closed again still works on the list put back
 await open('d4d4d4d4d4d4d4d4');await back();
 assert.equal(await page.locator('#suggestions article.card').count(),3);
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
