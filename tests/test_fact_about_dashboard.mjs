import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Learning: a fact says who it is about, with Remove link (fact_links.py), and the one-time link of the facts
// already there is one entry under Changes, with Undo. All mocked; SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const t=d=>`2026-10-${String(d).padStart(2,'0')}T09:00:00+00:00`;
let facts,changes,posts;
const reset=()=>{posts=[];facts=[
 {id:9,kind:'fact',text:'Ann Example wants invoices as a PDF.',fact_kind:'preference',created_at:t(25),merged:0,about:[{id:'email:ann@example.com',name:'Ann Example'}]},
 {id:8,kind:'fact',text:'Acme Labs closes its books on the 5th.',created_at:t(24),merged:0,about:[{id:'org:acme.example',name:'Acme Labs'}]},
 {id:7,kind:'fact',text:'Vendor newsletters never need a to-do.',created_at:t(23),merged:0,about:[]}];
 changes=[{id:4,at:t(25),kind:'about',channel:null,text:'2',line:['Facts that name one person, organization or project: {}',2],before:null,why:'',undone:false}]};
reset();
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],
  voices:[],facts,learning_changes:changes}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='graph_fact_unlink'){facts=facts.map(f=>f.id===args.fact_id?{...f,about:f.about.filter(a=>a.id!==args.node_id)}:f);res.end(JSON.stringify({ok:true}));return}
  if(action==='learning_undo'){changes=changes.map(c=>({...c,undone:true}));facts=facts.map(f=>({...f,about:[]}));res.end(JSON.stringify({undone:args.id}));return}}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[],shots=process.env.SHOTS;let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  reset();
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');
  await navClick(page.locator('[data-tab="feedback"]').first());
  const list=page.locator('#facts');await list.locator('#learned-9').waitFor();
  // who a fact is about, under its text; a fact about no one says nothing
  assert.match(await list.locator('#learned-9').textContent(),/About Ann Example · Remove link/);
  assert.match(await list.locator('#learned-8').textContent(),/About Acme Labs · Remove link/);
  assert.equal(await list.locator('#learned-7 [data-not-about]').count(),0);
  assert.doesNotMatch(await list.locator('#learned-7').textContent(),/About/);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
  if(shots){await page.evaluate(()=>document.fonts.ready);await page.locator('#learn-pane-learned').screenshot({path:`${shots}/about-learned-${width}-${scheme}.png`})}
  // Remove link takes only the link away: the fact stays
  await list.locator('#learned-9 [data-not-about]').click();
  await page.locator('#toast',{hasText:'Link removed. The fact stays.'}).waitFor({state:'attached'});
  assert.deepEqual(posts.at(-1),{action:'graph_fact_unlink',args:{fact_id:9,node_id:'email:ann@example.com'}});
  await list.locator('#learned-9 [data-not-about]').waitFor({state:'detached'});
  assert.match(await list.locator('#learned-9').textContent(),/Ann Example wants invoices as a PDF\./);
  // the one-time link: one entry under Changes, and Undo takes every link it made away
  await page.locator('#learn-tab-changes').click();
  const block=page.locator('#learn-changes');await block.locator('.change-row').first().waitFor();
  assert.deepEqual(await block.locator('.change-row strong').allTextContents(),['Facts linked']);
  assert.match(await block.locator('.change-row').textContent(),/Facts that name one person, organization or project: 2/);
  if(shots)await page.locator('#learn-pane-changes').screenshot({path:`${shots}/about-changes-${width}-${scheme}.png`});
  await block.locator('[data-learn-undo="4"]').click();
  await block.locator('.change-row.undone').waitFor();
  assert.deepEqual(posts.at(-1),{action:'learning_undo',args:{id:4}});
  await page.locator('#learn-tab-learned').click();
  await list.locator('#learned-8').waitFor();
  await list.locator('#learned-8 [data-not-about]').waitFor({state:'detached'});
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('fact about dashboard ok');
}finally{await browser?.close();server.close()}
