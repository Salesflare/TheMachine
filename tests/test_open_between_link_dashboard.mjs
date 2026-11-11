import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do link in a record's "Open between you" (a person, an organization, a project) lands on that to-do in To-dos
// and stays there: the list drawn in again a moment later (its first paint's late parts, the next refresh) never takes
// the view away. A to-do with no row in the list (one that looks done sits in Done) opens its chat instead of nothing.
// OPEN_LINK_SHOT=<dir> also writes screenshots at 390, light and dark.
process.env.TZ='Europe/Brussels';
const dashboard=await dashboardPage();
const brand={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'};
const ago=d=>new Date(Date.now()-d*864e5).toISOString(),ahead=d=>new Date(Date.now()+d*864e5).toISOString();
const id=c=>c.repeat(16);
const card=(c,title,extra={})=>({id:id(c),title,body:'Made-up to-do with a few lines of text so the list is long enough to scroll on a phone.',status:'snoozed',
 snoozed_until:ahead(1),preparation_status:'ok',scope:'personal',created_at:ago(2),event_ids:[1],...extra});
const LATER=[...'0123456789'].map((c,i)=>card(c,'Later to-do number '+(i+1)));
const TARGET=card('a','Wait for the painter to pick another date',{due:new Date().toISOString().slice(0,10)});
// looks done since days, past Done's first page (newer done ones fill it): no row anywhere in To-dos
const DONEISH=card('b','Calendar clash: a family dinner',{status:'prepared',snoozed_until:null,outcome:'{"state":"already_done"}',created_at:ago(9)});
const DONE=[...'cdef'].map((c,i)=>card(c,'Done to-do number '+(i+1),{status:'completed',snoozed_until:null,closed_at:ago(i*.1),created_at:ago(1)}));
const status=()=>({suggestions:[...LATER.slice(0,6),TARGET,...LATER.slice(6),DONEISH],done_milestone:{count:250},done_counts:{all:250,work:100,personal:150},
 promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const open={cards:[{id:TARGET.id,title:TARGET.title,status:'snoozed',due:TARGET.due},{id:DONEISH.id,title:DONEISH.title,status:'prepared'}]};
const nodes={'email:robin@example.test':{id:'email:robin@example.test',kind:'person',name:'Robin Vale',strength:2,signals:4,ids:['robin@example.test'],links:[],open,recent:[]},
 'org:harborline':{id:'org:harborline',kind:'org',name:'Harborline',signals:4,links:[],open,recent:[]},
 'project:harborline-pilot':{id:'project:harborline-pilot',kind:'project',name:'Harborline pilot',signals:4,links:[],open,todos:[],recent:[]}};
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(brand[url.pathname]){res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+brand[url.pathname],import.meta.url)));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');res.end(JSON.stringify(n?nodes[n]||{}:{people:[nodes['email:robin@example.test']],projects:[],orgs:[],quiet:[],new:[]}));return}
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:url.searchParams.get('id')?[]:DONE,next:'more',total:250}));return}
 if(url.pathname==='/api/card_chat'||url.pathname==='/api/cards/chat'){res.end(JSON.stringify({messages:[],steps:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[],shots=process.env.OPEN_LINK_SHOT;let browser;
// where the target sits on screen: its top, in view or not
const where=page=>page.evaluate(i=>{const c=document.getElementById('task-'+i);if(!c||!c.getClientRects().length)return {shown:false,y:scrollY};const r=c.getBoundingClientRect();
 return {shown:r.bottom>0&&r.top<innerHeight,top:Math.round(r.top),y:Math.round(scrollY),tab:document.querySelector('nav button[data-tab].active')?.dataset.tab}},TARGET.id);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [node,scheme] of [['email:robin@example.test','dark'],['email:robin@example.test','light'],['org:harborline','dark'],['project:harborline-pilot','dark']]){
  const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(node+': '+e.message));
  // as the owner goes: Graph > People, a row in the list, then the record (the list's place is kept for Back)
  const toRecord=async()=>{await page.goto(base);await page.waitForFunction(()=>!!state?.suggestions);
   await page.evaluate(()=>{location.hash='#graph=people'});await page.locator('#people-view [data-node]').first().waitFor();
   if(node.startsWith('email:'))await page.locator('#people-view [data-node]').first().tap();else await page.evaluate(n=>graphOpen(n),node);
   await page.locator('#people-view .graph-open').waitFor()};
  await toRecord();
  const link=page.locator(`#people-view .graph-open a[href="#card=${TARGET.id}"]`);
  await link.scrollIntoViewIfNeeded();await link.tap();
  // landed: in To-dos, the to-do on screen once the page stopped gliding
  await page.waitForFunction(i=>{const c=document.getElementById('task-'+i);return !!c&&c.getClientRects().length>0&&!document.querySelector('#inbox').hidden},TARGET.id,{timeout:8000});
  let y=-1;for(let i=0;i<40;i++){const now=await page.evaluate(()=>scrollY);if(now===y)break;y=now;await page.waitForTimeout(150)}
  const first=await where(page);assert.ok(first.shown&&first.tab==='inbox',`${node}: lands on the to-do in To-dos ${JSON.stringify(first)}`);
  assert.equal(await page.evaluate(i=>document.getElementById('task-'+i).classList.contains('flash'),TARGET.id),true,`${node}: the to-do is highlighted`);
  // the late parts of the first paint (the milestone, fonts) and the next refresh tick: the to-do stays where it is
  await page.waitForTimeout(2500);
  const settled=await where(page);
  await page.evaluate(()=>refresh());await page.waitForTimeout(600);
  const after=await where(page);
  for(const [what,w] of [['a moment later',settled],['after the next refresh',after]])
   assert.ok(w.shown&&Math.abs(w.top-first.top)<40,`${node}: the to-do stays in view ${what}: ${JSON.stringify({first,w})}`);
  if(shots&&node.startsWith('email:'))await page.screenshot({path:`${shots}/open-between-${scheme}-390.png`});
  // the one with no row in the list: its chat opens
  await toRecord();
  const other=page.locator(`#people-view .graph-open a[href="#card=${DONEISH.id}"]`);await other.waitFor();await other.scrollIntoViewIfNeeded();await other.tap();
  await page.waitForFunction(i=>chatOpen()?.id===i,DONEISH.id,{timeout:8000});
  if(shots&&node.startsWith('email:'))await page.screenshot({path:`${shots}/open-between-no-row-${scheme}-390.png`});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
