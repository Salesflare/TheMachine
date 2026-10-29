import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A project's organization: its page, its board card and its row link to it; the Edit form picks one from the Graph
// (search as you type) or adds a new one, says when the Machine set it, and only sends org when the owner changed
// it; an organization's page lists its projects. At 390 and 1440 nothing is wider than the screen.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const stages=[{name:'Discovery'},{name:'Demo'},{name:'Won'},{name:'Stalled or declined',side:true}];
const umicore={node_id:'org:umicore.example',name:'Umicore',logo:null,domain:'umicore.example'};
const tile=(i,name,extra={})=>({id:'project:'+i,name,stage:'Demo',reason:'asked for a demo',by:'review',at:day(2),event_id:100+i,days:2,no_reply_days:0,org:umicore,...extra});
const boards=[{id:1,name:'CRM evaluations',stages,default:true,stuck:0,projects:[tile(1,'Rollout'),tile(2,'Umicore',{org:{...umicore}})],maybes:[]}];
const card={node_id:'project:1',name:'Rollout',board_id:1,stage:'Demo',org:'umicore.example',org_node:{id:'org:umicore.example',name:'Umicore',domain:'umicore.example',by:'auto'},
 value:null,close_date:null,notes:null,people:[],archived:false,outcome:null,outcome_reason:null};
const project={id:'project:1',kind:'project',name:'Rollout',strength:1,last_at:day(2),signals:3,state:'active',ids:[],links:[],recent:[],around:[],open:{},project:card,
 board:{board:'CRM evaluations',stage:'Demo',moves:[],board_visibility:'team'}};
const org={id:'org:umicore.example',kind:'org',name:'Umicore',domain:'umicore.example',strength:1,last_at:day(1),signals:1,profile:{},links:[],recent:[],around:[],open:{},people_roles:[],
 projects:[{id:'project:1',name:'Rollout',board:'CRM evaluations',stage:'Demo',open:true},{id:'project:8',name:'Old pilot',board:null,stage:null,open:false,outcome:'won'}]};
const found=[{id:'org:umicore.example',kind:'org',name:'Umicore',domain:'umicore.example'},{id:'org:inkwell.example',kind:'org',name:'Inkwell',domain:'inkwell.example'}];
let calls=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node'),q=url.searchParams.get('q');
  if(q!=null){res.end(JSON.stringify({found:found.filter(o=>o.name.toLowerCase().includes(q.toLowerCase()))}));return}
  res.end(JSON.stringify(n?(n.startsWith('org:')?org:project):{projects:[{id:'project:1',kind:'project',name:'Rollout',strength:1,last_at:day(2),signals:3,org_node:{id:'org:umicore.example',name:'Umicore'}}],
   people:[],quiet:[],new:[],orgs:[],boards,person_names:[],project_names:[]}));return}
 if(req.method!=='GET'&&!url.pathname.startsWith('/brand/'))calls.push(JSON.parse(body||'{}'));
 if(url.pathname==='/api/action'){const c=JSON.parse(body||'{}'),a=c.args||{};
  if(c.action==='graph_new'){res.end(JSON.stringify({node_id:'org:named:newco',name:a.name,created:true}));return}
  if(c.action==='project_save'){res.end(JSON.stringify({node_id:a.node_id,name:a.name,created:false}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const fits=(page,where)=>page.evaluate(()=>({page:document.documentElement.scrollWidth,vw:innerWidth})).then(s=>assert.ok(s.page<=s.vw,`${where}: wider than the screen ${JSON.stringify(s)}`));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440]){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height:mobile?844:900},isMobile:mobile,hasTouch:mobile,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  // The board card names its organization and links there; a project named like its organization doesn't repeat it
  await page.goto(base+'#graph=projects');await page.locator('#people-view .proj-board:not([hidden]) .pboard').waitFor();
  assert.equal(await page.locator('.tile[data-node="project:1"] .tile-org [data-node="org:umicore.example"]').textContent(),'Umicore');
  assert.equal(await page.locator('.tile[data-node="project:2"] .tile-org').count(),0);
  await fits(page,width+' board');
  await page.locator('.tile[data-node="project:1"] .tile-org button').click();
  await page.locator('#people-view .org-page').waitFor();
  // The organization lists its projects, each with where it stands, and each opens
  assert.deepEqual(await page.locator('.org-projects li').allTextContents(),['RolloutDemo on CRM evaluations','Old pilotWon']);
  await fits(page,width+' organization');
  await page.locator('.org-projects [data-node="project:1"]').click();
  // The project page links its organization
  await page.locator('#people-view .proj-org [data-node="org:umicore.example"]').waitFor();
  await fits(page,width+' project');
  // Edit: the Machine's pick says so; Save without touching it sends no org
  await page.locator('#people-view [data-proj-edit]').first().click();const d=page.locator('#project-dialog[open]');await d.waitFor();
  assert.match(await d.locator('.ed-org li').textContent(),/Umicore\s*From its people/);
  calls=[];await d.locator('button.primary').click();await page.locator('#project-dialog[open]').waitFor({state:'detached'});
  assert.equal(calls.filter(c=>c.action==='project_save').length,1);assert.ok(!('org' in calls[0].args),'an untouched organization is not sent');
  // Take it off, search, pick one from the Graph
  await page.locator('#people-view [data-proj-edit]').first().click();await d.waitFor();
  await d.locator('[data-pj-org-drop]').click();const q=d.locator('input[name="orgq"]');await q.fill('ink');
  await page.waitForFunction(()=>document.querySelectorAll('#project-dialog-orgs option').length===1);
  assert.equal(await d.locator('[data-pj-org-new]').textContent(),'Add “ink” as new');
  await q.press('Enter');assert.match(await d.locator('.ed-org li').textContent(),/^Inkwell/);
  assert.equal(await d.locator('.ed-org li small').count(),0);await fits(page,width+' edit');
  calls=[];await d.locator('button.primary').click();await page.locator('#project-dialog[open]').waitFor({state:'detached'});
  assert.equal(calls.find(c=>c.action==='project_save').args.org,'org:inkwell.example');
  // Or add a new one: it is made first, then picked
  await page.locator('#people-view [data-proj-edit]').first().click();await d.waitFor();
  await d.locator('[data-pj-org-drop]').click();await d.locator('input[name="orgq"]').fill('Newco');
  calls=[];await d.locator('[data-pj-org-new]').click();await d.locator('.ed-org li',{hasText:'Newco'}).waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args]),[['graph_new',{kind:'org',name:'Newco',website:''}]]);
  calls=[];await d.locator('button.primary').click();await page.locator('#project-dialog[open]').waitFor({state:'detached'});
  assert.equal(calls.find(c=>c.action==='project_save').args.org,'org:named:newco');
  // Taken off and saved: an empty pick is sent, so it stays off
  await page.locator('#people-view [data-proj-edit]').first().click();await d.waitFor();await d.locator('[data-pj-org-drop]').click();
  calls=[];await d.locator('button.primary').click();await page.locator('#project-dialog[open]').waitFor({state:'detached'});
  assert.equal(calls.find(c=>c.action==='project_save').args.org,'');
  // The list row links the organization too
  await page.goto(base+'#graph=projects');await page.reload();
  await page.locator('#people-view article[data-node="project:1"] [data-node="org:umicore.example"]').first().waitFor({state:"attached"});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('project organization dashboard ok');
}finally{await browser?.close();server.close()}
