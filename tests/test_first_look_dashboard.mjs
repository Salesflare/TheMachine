import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The first look once cards exist: a slim strip under the counters, not loose text above the filters. Its row on
// Connections names each account once. A running review never sits next to
// "No reviews yet", and the summary says it once: "0 waiting · 0 reviewed · last not yet".
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const started=new Date(Date.now()-60e3).toISOString();
const run={run_id:'r1',status:'running',started_at:started,preview:1,auto:1,planned:67,done_count:5,account_ids:['gmail','calendar'],steps:[]};
let runs=[],cards=[];
const live=()=>({runs,queue:null,first_look:null});
const card={id:'c1',title:'Send Sam the pricing',body:'Sam asked for pricing.',status:'pending',event_ids:[1],scope:'work',created_at:new Date().toISOString()};
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:live(),
 connectors:[{id:'gmail',email:'pat@example.com',service:'gmail'},{id:'calendar',email:'pat@example.com',service:'calendar'}]});
const errors=[];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/reviews/live'){res.end(JSON.stringify(live()));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 // Nothing running yet: "No reviews yet" and the plain summary
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.locator('#analyses .no-reviews').waitFor({state:'attached'});
 assert.equal(await page.locator('#analyses .no-reviews').evaluate(e=>e.hidden),false);  // Connections is another tab: check the attribute
 assert.equal(await page.locator('#review-summary').textContent(),'0 waiting · 0 reviewed · last not yet. Next one when new messages come in.');
 // A running first look: no "No reviews yet" beside it, the accounts named once
 runs=[run];await page.evaluate(()=>refresh());
 assert.equal(await page.locator('#review-live .review-live').count(),1);
 assert.equal(await page.locator('#analyses .no-reviews:not([hidden])').count(),0);
 const row=await page.locator('#review-live .review-live').textContent();
 assert.equal(row.split('pat@example.com').length-1,1,row);
 // With cards: the strip sits under the counters, after the filters
 cards=[card];await page.evaluate(()=>refresh());
 const strip=page.locator('#first-look');
 assert.equal(await strip.isVisible(),true);
 assert.match(await strip.textContent(),/Taking a first look at your last 7 days.*5 of 67 signals/);
 assert.equal(await page.locator('#suggestions .first-look-empty').count(),0);
 const order=await page.evaluate(()=>['#suggestion-summary','#suggestion-stats','#first-look'].map(s=>[...document.querySelectorAll('#inbox > *')].indexOf(document.querySelector(s))));
 assert.ok(order[0]<order[1]&&order[1]<order[2],String(order));
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('first look dashboard ok');
