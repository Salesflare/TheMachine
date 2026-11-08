import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A page's first drawing puts the to-dos on screen first: the parts out of sight (Learning, Connections, the other
// tabs, the Updated line) are drawn just after that first paint, not before it. Then they are all there, and a later
// refresh draws everything at once as before.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[{id:'a1a1a1a1a1a1a1a1',title:'Check the payroll is ready',body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 // What the page holds when the first to-do comes in, and in the frame after it
 await context.addInitScript(()=>{window.seen=null;new MutationObserver((m,o)=>{if(document.querySelector('#suggestions article.card')){o.disconnect();
  const look=()=>({updated:document.querySelector('#updated')?.textContent||''});window.seen={at:look()};requestAnimationFrame(()=>setTimeout(()=>{window.seen.after=look()},50))}}).observe(document,{childList:true,subtree:true})});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
 await page.waitForFunction(()=>window.seen?.after);
 const seen=await page.evaluate(()=>window.seen);
 assert.doesNotMatch(seen.at.updated,/Updated/,'the to-dos are drawn before the rest: '+JSON.stringify(seen));
 assert.match(seen.after.updated,/Updated/,'the rest follows right after: '+JSON.stringify(seen));
 // A refresh after that draws it all at once again
 await page.evaluate(()=>{document.querySelector('#updated').textContent=''});
 await page.evaluate(()=>refresh());
 assert.match(await page.locator('#updated').textContent(),/Updated/,'a refresh draws the rest with the to-dos');
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
