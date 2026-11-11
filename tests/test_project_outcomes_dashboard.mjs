import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Outcomes for every project (project_success.py, 2026-11-11): a project on no board has Done when and Proof in its
// dialog and its Done when box on its page; work that isn't a deal ends Done (outcome 'won' underneath), a deal Won or
// Lost; a proof that marked it done shows under Recent changes with Undo, which reopens it. A board without values is
// not a pipeline: its tiles end Done too. Made-up names. PO_SHOT=<dir> writes screenshots at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const stages=[{name:'Contacted'},{name:'Agreed'},{name:'Live'},{name:'Stalled or declined',side:true}];
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const boards=[{id:1,name:'Partner listings',stages,default:true,stuck:0,maybes:[],
 projects:[{id:'project:1',name:'Paperkite listing',stage:'Agreed',reason:'they agreed',by:'review',at:day(2),event_id:101,days:2,no_reply_days:0,org:{name:'Paperkite',logo:null}}]}];
const when='Lee confirms the guest post is published';
const projects={
 'project:9':{name:'Bramblebox guest post',value:null,outcome:null,
  success:{condition:when,proof:'message',by:'owner',done:false,done_by:null,evidence:null,not_proven:null,
   blocker:{kind:'no_reply',days:12,event_id:7,follow_ups:false,todo:{id:'c9',title:'Nudge Bramblebox guest post: no reply in 12 days'}}},log:[]},
 'project:10':{name:'Tealpond reseller',value:4000,outcome:'won',outcome_reason:'Sam sent the signed agreement',
  success:{condition:'Sam sends the signed agreement',proof:'message',by:'review',done:true,done_by:'evidence',evidence:{event_id:55,url:null,at:day(1)},not_proven:null,blocker:null},
  log:[{kind:'done',at:day(0),deal:true,act:{reopen:'project:10'},source:{type:'event',id:55,via:'email',from:'Sam'}}]},
 'project:11':{name:'Fernwave interview',value:null,outcome:'won',outcome_reason:'Lee says it is published',
  success:{condition:'The interview is published',proof:'message',by:'review',done:true,done_by:'evidence',evidence:{event_id:56,url:null,at:day(1)},not_proven:null,blocker:null},
  log:[{kind:'done',at:day(0),deal:false,act:{reopen:'project:11'},source:{type:'event',id:56,via:'email',from:'Lee'}}]}};
const detail=id=>{if(id==='project:1')return {id,kind:'project',name:'Paperkite listing',strength:1,last_at:day(2),signals:3,state:'open',ids:[],links:[],recent:[],around:[],open:{},
  project:{node_id:id,name:'Paperkite listing',board_id:1,stage:'Agreed',org:null,value:null,notes:'',people:[],archived:false,outcome:null,outcome_reason:null,deal:false},
  board:{board:'Partner listings',stage:'Agreed',next:null,moves:[],stages:stages.map(s=>s.name)}};
 const p=projects[id];
 return {id,kind:'project',name:p.name,strength:1,last_at:day(2),signals:3,state:'active',ids:[],links:[],recent:[],around:[],open:{},log:p.log,board:null,success:p.success,
  project:{node_id:id,name:p.name,board_id:null,stage:null,org:null,value:p.value,close_date:null,notes:'',people:[],archived:false,outcome:p.outcome,outcome_reason:p.outcome_reason||null,
   deal:p.value!=null,condition:p.success.condition,proof:p.success.proof}}};
let calls=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');res.end(JSON.stringify(n?detail(n):{projects:[],people:[],quiet:[],new:[],orgs:[],boards,person_names:[],project_names:[]}));return}
 if(req.method!=='GET'&&!url.pathname.startsWith('/brand/'))calls.push(JSON.parse(body||'{}'));
 if(url.pathname==='/api/action'){const c=JSON.parse(body||'{}');
  res.end(JSON.stringify(c.action==='project_save'?{node_id:c.args.node_id,name:c.args.name,created:false}:c.action==='project_outcome'?{node_id:c.args.node_id,outcome:c.args.outcome,deal:projects[c.args.node_id]?.value!=null}:{}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const open=async(width,height,scheme='light')=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-GB',colorScheme:scheme});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));await page.goto(base);
 await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());await page.locator('#people-view').waitFor({state:'attached'});
 await page.evaluate(()=>document.querySelector('[data-graph-sub="projects"]').click());
 await page.locator('#people-view .proj-board:not([hidden]) .pboard').waitFor();return {context,page}};
const project=async(page,id)=>{await page.evaluate(id=>graphOpen(id),id);await page.locator(`.graph-detail .name-row h3`).waitFor();
 await page.waitForFunction(name=>document.querySelector('.graph-detail .name-row h3')?.textContent===name,id==='project:1'?'Paperkite listing':projects[id].name)};
const fits=(page,where)=>page.evaluate(()=>({page:document.documentElement.scrollWidth,vw:innerWidth})).then(s=>assert.ok(s.page<=s.vw,`${where}: wider than the screen ${JSON.stringify(s)}`));
const shots=process.env.PO_SHOT;
const editor=async page=>{await page.locator('.graph-detail [data-proj-edit]').first().click();await page.locator('#project-dialog[open]').waitFor()};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [w,h] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){const {context,page}=await open(w,h,scheme);
  // A project on no board: its Done when box, with what holds it up and its to-do
  await project(page,'project:9');const box=page.locator('.graph-detail .ps-box');
  assert.match(await page.locator('.graph-detail .graph-sub').first().textContent(),/^Steady · /);
  assert.equal(await box.locator('.ps-when').textContent(),'Done when: '+when);
  assert.equal(await box.locator('.ps-block').textContent(),'No reply in 12 days · To-do');
  await fits(page,`${w} ${scheme} page`);
  if(shots){await box.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/page-no-board-${w}-${scheme}.png`})}
  // Its editor: Done when and Proof without a board; it isn't a deal, so it ends Done
  await editor(page);
  assert.equal(await page.locator('#project-form [name=board]').inputValue(),'');
  assert.equal(await page.locator('#project-form [name=condition]').inputValue(),when);
  assert.equal(await page.locator('#project-form [name=proof]').inputValue(),'message');
  assert.deepEqual(await page.locator('#project-form .pj-end button').allTextContents(),['Done','Archive','Delete…']);
  await fits(page,`${w} ${scheme} editor`);
  if(shots){await page.evaluate(()=>document.querySelector('#project-form [name=condition]').scrollIntoView({block:'center'}));await page.locator('#project-dialog').screenshot({path:`${shots}/editor-no-board-${w}-${scheme}.png`})}
  await page.locator('#project-form [data-pj-close]').first().click();
  // Marked done by its proof: the page says so, and Recent changes has Undo
  await project(page,'project:11');
  assert.match(await page.locator('.graph-detail .ps-proof.ok').textContent(),/^Proven /);
  assert.match(await page.locator('.graph-detail .graph-sub').first().textContent(),/^Done · last signal /);
  assert.equal(await page.locator('.graph-detail .proj-facts b').count(),0,'the proof box says it once');
  await page.locator('.record-log summary').first().click();
  assert.equal(await page.locator('.record-log .rc-text').first().textContent(),'Project marked done');
  await fits(page,`${w} ${scheme} done page`);
  if(shots){await page.locator('.record-log').scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/page-marked-done-${w}-${scheme}.png`})}
  await context.close()}
 {const {context,page}=await open(1440,900);
  // Saving a condition on a project on no board sends it
  await project(page,'project:9');calls=[];await editor(page);
  await page.locator('#project-form [name=condition]').fill('The guest post is live');await page.locator('#project-form [name=proof]').selectOption('link');
  await page.locator('#project-form button.primary').click();await page.locator('#project-dialog[open]').waitFor({state:'detached'});
  const saved=calls.find(c=>c.action==='project_save').args;assert.deepEqual([saved.board_id,saved.condition,saved.proof],[null,'The guest post is live','link']);
  // Done by hand: "Mark it done", outcome won underneath
  calls=[];await editor(page);await page.locator('#project-form [data-pj-outcome="won"]').click();
  assert.equal(await page.locator('#project-dialog-title').textContent(),'Done');
  assert.equal(await page.locator('#project-form button.primary').textContent(),'Mark it done');
  if(process.env.PO_SHOT)await page.locator('#project-dialog').screenshot({path:`${shots}/editor-mark-done-1440-light.png`});
  await page.locator('#project-form [name=reason]').fill('It went live');await page.locator('#project-form button.primary').click();
  await page.locator('#project-dialog[open]').waitFor({state:'detached'});
  assert.deepEqual(calls.find(c=>c.action==='project_outcome').args,{node_id:'project:9',outcome:'won',reason:'It went live'});
  assert.equal(await page.locator('#toast').textContent(),'Project marked done.');
  // A deal on no board (it has a value) ends Won, and its Undo reopens it
  await project(page,'project:10');
  assert.match(await page.locator('.graph-detail .graph-sub').first().textContent(),/^Won · /);
  await page.locator('.record-log summary').first().click();
  assert.equal(await page.locator('.record-log .rc-text').first().textContent(),'Marked won');
  calls=[];await page.locator('.record-log .rc-menu summary').first().click();await page.locator('.record-log [data-rc-reopen]').click();
  await page.waitForFunction(()=>document.querySelector('#toast')?.textContent==='Reopened.');
  assert.deepEqual(calls.find(c=>c.action==='project_outcome').args,{node_id:'project:10',outcome:null,reason:''});
  // A board without values isn't a pipeline: its tiles and pages end Done, not Won or Lost
  await page.evaluate(()=>document.querySelector('[data-crumb="projects"]')?.click());await page.locator('#people-view .pboard').waitFor();
  const menu=page.locator('.tile[data-node="project:1"] .tile-menu');await menu.locator('summary').click();
  const items=await menu.locator('[data-proj-outcome]').allTextContents();assert.deepEqual(items,['Done']);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('project outcomes dashboard ok');
}finally{await browser?.close();server.close()}
