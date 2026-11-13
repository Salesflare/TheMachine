import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do The Machine raised itself ("The Machine · Thu 12 Nov": a crash, a fault, its health) shows The Machine's own
// mark on its source line, whatever account carried it (events-email.js cardViaIcon); it once wore the Gmail mark of the
// account it came in on. A source the line doesn't name takes its account's mark only when every account agrees, so it
// never wears another source's brand. Named sources keep theirs.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const card=(id,source_line,account_ids)=>({id,title:'To-do '+id,body:'Something to look at.',status:'pending',scope:'work',created_at:now,event_ids:[1],source_line,account_ids});
const cards=[card('m1','Source: The Machine · Thu 12 Nov',['g1']),card('m2','Source: The Machine · Thu 12 Nov',[]),
 card('u1','Source: shared file · Thu 12 Nov',['g1','s1']),card('u2','Source: shared file · Thu 12 Nov',['s1']),
 card('e1','Source: email from Robin Example · Thu 12 Nov',['g1']),card('k1','Source: Slack from Robin Example · Thu 12 Nov',['g1'])];
const state={suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[{id:'g1',service:'gmail'},{id:'s1',service:'slack'}],fleet:{on:false,fleets:[]}};
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-k1').waitFor();
 const mark=id=>page.locator(`#task-${id} .read-original`).first().evaluate(e=>({via:[...e.classList].find(c=>c.startsWith('via-')),
  ico:getComputedStyle(e,'::before').getPropertyValue('mask-image')||getComputedStyle(e,'::before').getPropertyValue('-webkit-mask-image')}));
 for(const id of ['m1','m2']){const m=await mark(id);assert.equal(m.via,'via-gateway',id);assert.match(m.ico,/mono\/gateway\.svg/,id)}
 assert.deepEqual(await Promise.all(['u1','u2','e1','k1'].map(async id=>(await mark(id)).via)),['via-chat','via-slack','via-gmail','via-slack']);
 console.log('Source marks: The Machine\'s own to-dos show its mark; unnamed sources never take another brand.');
}finally{await browser?.close();server.close()}
