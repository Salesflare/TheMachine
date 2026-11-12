import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The sidebar's People, Organizations and Projects counts come with the status (graph_counts): a page load never asks for
// the Graph overview (some 600 KB on a busy Machine, its biggest answer) just for them; opening Graph does, as before.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[{id:'a1a1a1a1a1a1a1a1',title:'Check the payroll is ready',body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1]}];
let counts={person:12,org:3,project:2};
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]},graph_counts:counts});
const asked=[];
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');asked.push(url.pathname);res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({people:[],orgs:[],projects:[],quiet:[],new:[],whos_who:[],waiting:[],warmup:[],counts,list_counts:{}}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 const origin='http://127.0.0.1:'+server.address().port;
 // 1. A load: the counts show from the status, and the Graph overview is never asked (it was, 1.5 s after the load)
 await page.goto(origin);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
 await page.waitForFunction(()=>document.querySelector('#count-people')?.textContent==='12');
 assert.equal(await page.locator('#count-orgs').textContent(),'3');
 assert.equal(await page.locator('#count-projects').textContent(),'2');
 await page.waitForTimeout(2500);
 assert.equal(asked.filter(p=>p==='/api/graph').length,0,'no Graph overview on a load: '+asked.join(' '));
 // 2. New counts in a later status: the rows follow
 counts={person:13,org:3,project:1};
 await page.evaluate(()=>refresh());
 await page.waitForFunction(()=>document.querySelector('#count-people')?.textContent==='13');
 assert.equal(await page.locator('#count-projects').textContent(),'1');
 assert.equal(asked.filter(p=>p==='/api/graph').length,0,'still none: '+asked.join(' '));
 // 3. Opening Graph asks for the overview, as before
 await page.goto(origin+'/#graph=people');
 await page.waitForFunction(()=>!document.querySelector('#people')?.hidden);
 await page.waitForTimeout(500);
 assert.ok(asked.includes('/api/graph'),'Graph open asks for its overview: '+asked.join(' '));
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
