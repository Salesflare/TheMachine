import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Leaving Organizations (hundreds of them) for People, Projects or Who's who shows that page at once: its pane is drawn
// already, so the switch never waits for the Graph's answer (slow here, as on a busy Machine). From an organization's
// page, the list it goes to says it's loading right away instead of leaving the old page up.
const dashboard=await dashboardPage();
const day=new Date().toISOString().slice(0,10),SLOW=2500;
const person=i=>({id:'email:p'+i+'@example.org',kind:'person',name:'Person '+i,strength:3-i/1000,closeness:'regular',last_at:day,signals:4,ids:['p'+i+'@example.org']});
const org=i=>({id:'org:co'+i+'.example',kind:'org',name:'Company '+i,signals:2,last_at:day,domain:'co'+i+'.example'});
const graph={people:Array.from({length:300},(_,i)=>person(i)),quiet:[],new:[],orgs:Array.from({length:760},(_,i)=>org(i)),warmup:[],
 projects:Array.from({length:60},(_,i)=>({id:'project:'+i,kind:'project',name:'Project '+i,state:'active',last_at:day,signals:3,people:[]})),
 whos_who:[{...person(1),role:'finance lead',quote:null,event_id:null}]};
let graphCalls=0;
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({graph_waiting:1,suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'&&url.searchParams.get('node')){setTimeout(()=>res.end(JSON.stringify({...org(3),links:[],people:[],timeline:null})),50);return}
 if(url.pathname==='/api/graph'){graphCalls++;setTimeout(()=>res.end(JSON.stringify(graph)),graphCalls===1?0:SLOW);return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const shown=(page,pane)=>page.evaluate(p=>{const el=document.querySelector(`#people-view [data-graph-panel="${p}"]`);return !!el&&!el.hidden&&el.offsetHeight>0},pane);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){graphCalls=0;
  const phone=width<600,context=await browser.newContext({viewport:{width,height},isMobile:phone,hasTouch:phone}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#graph=orgs');
  await page.waitForFunction(()=>{const el=document.querySelector('#people-view [data-graph-panel="orgs"]');return el&&!el.hidden});
  const go=pane=>page.evaluate(p=>{const a=document.querySelector(`#graph-sub a[data-graph-sub="${p}"]`);if(a&&a.offsetParent)a.click();else{location.hash='#graph='+p}},pane);
  for(const pane of ['people','orgs','projects','orgs','roles']){
   const t0=Date.now();await go(pane);await page.waitForFunction(p=>{const el=document.querySelector(`#people-view [data-graph-panel="${p}"]`);return el&&!el.hidden&&el.offsetHeight>0},pane,{timeout:SLOW-500});
   assert.ok(Date.now()-t0<SLOW-500,`${width}: ${pane} shows before the Graph answers`);
   assert.equal(await page.evaluate(()=>location.hash),'#graph='+pane)}
  // From an organization's page: the list says Loading at once, then shows
  await page.evaluate(()=>graphOpen('org:co3.example'));await page.waitForSelector('#people.graph-on-node');
  await go('projects');
  await page.waitForSelector('#people-view .pager-loading',{timeout:500});
  await page.waitForFunction(()=>{const el=document.querySelector('#people-view [data-graph-panel="projects"]');return el&&!el.hidden},null,{timeout:SLOW+3000});
  assert.equal(await shown(page,'projects'),true);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('graph switch dashboard: ok');
}finally{await browser?.close();server.close()}
