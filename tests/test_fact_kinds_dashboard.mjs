import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Feedback, What I've learned: a fact's sort and end day sit quietly under it ("Temporary · Until Nov 14"), a plain fact
// shows neither, and facts past their end day are under Ended, each with Bring back. All mocked; FACT_SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const year=new Date().getFullYear(),t=d=>`${year}-10-${String(d).padStart(2,'0')}T09:00:00+00:00`;
const facts=[
 {id:4,kind:'fact',fact_kind:'event',valid_until:`${year}-11-14`,text:'Is at a trade fair in Lisbon this month.',created_at:t(22),merged:0},
 {id:3,kind:'fact',fact_kind:'preference',text:'Prefers calls after 10am.',created_at:t(21),merged:0},
 {id:2,kind:'fact',fact_kind:'commitment',valid_until:`${year}-12-31`,text:'Sends the board update every first Monday.',created_at:t(20),merged:0},
 {id:1,kind:'fact',fact_kind:'fact',text:'Quotes go out in EUR, excluding VAT.',created_at:t(19),merged:0},
 {id:8,kind:'draft',text:'Put the order number in the subject.',created_at:t(18),merged:0}];
let ended=[{id:9,fact_kind:'event',valid_until:`${year}-10-20`,text:'Is off on a team trip this week.',removed_at:t(21)}];
const posts=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],moved:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],voices:[],facts,facts_ended:ended}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='unmerge_fact'){ended=ended.filter(f=>f.id!==args.expired);res.end(JSON.stringify({restored:1}));return}}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;const shots=process.env.FACT_SHOTS;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[1440,700],[390,844]]){
  ended=[{id:9,fact_kind:'event',valid_until:`${year}-10-20`,text:'Is off on a team trip this week.',removed_at:t(21)}];
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#feedback');
  await navClick(page.locator('[data-tab="feedback"]').first());
  const learned=page.locator('#facts');await learned.locator('.learn-group').first().waitFor();
  assert.deepEqual(await learned.locator('.learn-group').evaluateAll(g=>g.map(x=>x.dataset.group)),['facts','rules','ended']);
  const meta=text=>learned.locator('.fact-row',{hasText:text}).locator('.fact-meta');
  assert.equal(await meta('Lisbon').textContent(),'Temporary · Until Nov 14');
  assert.equal(await meta('Prefers calls').textContent(),'Preference');
  assert.equal(await meta('board update').textContent(),'Commitment · Until Dec 31');
  assert.equal(await meta('Quotes go out').count(),0);  // a plain fact without an end shows nothing extra
  assert.equal(await meta('order number').count(),0);
  assert.equal(await learned.locator('[data-group="ended"] .learn-head h3').textContent(),'Ended 1');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
  if(shots){await page.evaluate(()=>document.fonts.ready);await learned.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/facts-${width}x${height}.png`,fullPage:true})}
  await learned.locator('[data-fact-back="9"]').click();
  await learned.locator('[data-group="ended"]').waitFor({state:'detached'});
  assert.deepEqual(posts.at(-1),{action:'unmerge_fact',args:{expired:9}});
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('fact kinds dashboard ok');
}finally{await browser?.close();server.close()}
