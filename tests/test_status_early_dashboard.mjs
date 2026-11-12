import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The to-dos are what a page load waits on: the page's head asks for api/status before its own script has run (that
// script asks for the theme's colors, api/omarchy-theme, as it starts), and the script's first status read takes that
// answer instead of asking again.
// An early request that fails (the connection cut) is asked again, and the to-dos still show.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[{id:'a1a1a1a1a1a1a1a1',title:'Check the payroll is ready',body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]}});
let asked=[],cutNext=false;
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');asked.push(url.pathname);res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){if(cutNext){cutNext=false;req.socket.destroy();return}res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 const origin='http://127.0.0.1:'+server.address().port;
 // 1. A load: one status request, asked before the page's script runs
 await page.goto(origin);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
 const status=asked.filter(p=>p==='/api/status').length,first=asked.indexOf('/api/status'),theme=asked.indexOf('/api/omarchy-theme');
 assert.equal(status,1,'the status is asked once: '+asked.join(' '));
 assert.ok(theme>0&&first<theme,'the status is asked before the page’s script runs: '+asked.join(' '));
 // 2. The early request cut off: asked again, and the to-dos show
 asked=[];cutNext=true;
 await page.reload();await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
 assert.equal(asked.filter(p=>p==='/api/status').length,2,'asked again after the cut: '+asked.join(' '));
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
