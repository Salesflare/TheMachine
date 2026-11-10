import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do shows an organization only when it is about it (2026-11-10): the review named it (org_node), or its project is
// with it (one the owner or a review set). A Personal to-do from the owner's partner about the house painting showed the partner's employer, only because
// they work there; that chip is gone. A Work to-do no review has judged yet (from before) keeps its person's organization.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const partner={id:'email:pat@bigcorp.example',name:'Pat Example',org:{id:'org:bigcorp.example',name:'Bigcorp'}};
const painting={node_id:'project:1',name:'Home painting'};
const card=(id,title,extra)=>({id,title,body:'The painter can’t come on Wednesday and will confirm another day.',status:'pending',created_at:now,event_ids:[1],
 people:[partner],source_line:'Source: WhatsApp from Pat Example',...extra});
const cards=[
 card('a1a1a1a1a1a1a1a1','Wait for the painter’s new date',{scope:'personal',project_node:painting,project:painting.name,org_said:true}),
 card('b1b1b1b1b1b1b1b1','Pat’s question about the hallway',{scope:'personal'}),
 card('c1c1c1c1c1c1c1c1','Accept the Brushworks quote',{scope:'personal',org_said:true,org_node:{id:'org:brushworks.example',name:'Brushworks'}}),
 card('d1d1d1d1d1d1d1d1','Pay the painting deposit',{scope:'personal',org_said:true,project:'Hallway painting',
  project_node:{node_id:'project:2',name:'Hallway painting',org:{id:'org:brushworks.example',name:'Brushworks'}}}),
 card('e1e1e1e1e1e1e1e1','Send Pat the renewal terms',{scope:'work'}),
 card('f1f1f1f1f1f1f1f1','Thank Pat for the intro',{scope:'work',org_said:true})];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{pending:cards.length},decisions:[],analyses:[],deliveries:[],
  review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1280,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
 const org=async id=>{const chip=page.locator(`#task-${id} .card-badges a.chip.who.org`);return await chip.count()?[(await chip.innerText()).trim(),await chip.getAttribute('href')]:null};
 // Who it is with still shows; the partner's employer doesn't
 assert.equal((await page.locator('#task-a1a1a1a1a1a1a1a1 a.chip.who:not(.org) .who-full').innerText()).trim(),'Pat Example');
 assert.equal(await org('a1a1a1a1a1a1a1a1'),null);
 assert.equal(await org('b1b1b1b1b1b1b1b1'),null);  // Personal, never judged: no employer either
 // The organization the review named, and the project's own one
 assert.deepEqual(await org('c1c1c1c1c1c1c1c1'),['Brushworks','#graph/'+encodeURIComponent('org:brushworks.example')]);
 assert.deepEqual(await org('d1d1d1d1d1d1d1d1'),['Brushworks','#graph/'+encodeURIComponent('org:brushworks.example')]);
 // Work: an older to-do keeps its person's organization; one the review said is about none shows none
 assert.deepEqual(await org('e1e1e1e1e1e1e1e1'),['Bigcorp','#graph/'+encodeURIComponent('org:bigcorp.example')]);
 assert.equal(await org('f1f1f1f1f1f1f1f1'),null);
 await context.close();
 assert.deepEqual(errors,[]);
 console.log('To-dos: an organization only when the to-do is about it.');
}finally{await browser?.close();server.close()}
