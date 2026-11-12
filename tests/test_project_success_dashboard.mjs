import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Done when (project_success.py) on a project's page: the success condition, the proof that met it (the message and
// the live page) or "Marked done by hand", why a review's "done" isn't proven yet, and the blocker with its one to-do.
// The project dialog edits the condition and its proof, and posts them only when they changed. Made-up names.
// PS_SHOT=<dir> writes screenshots at 390 and 1280, light and dark.
const dashboard=await dashboardPage();
const stages=[{name:'Contacted'},{name:'Agreed'},{name:'In review'},{name:'Live'},{name:'Stalled or declined',side:true}];
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const proj=(i,name,stage,extra={})=>({id:'project:'+i,name,stage,reason:'they agreed',by:'review',at:day(2),event_id:100+i,days:2,no_reply_days:0,org:{name,logo:null},...extra});
const boards=[{id:1,name:'Partner listings',stages,default:true,stuck:0,maybes:[],
 projects:[proj(1,'Paperkite listing','In review',{no_reply_days:12}),proj(2,'Bramblebox listing','Live'),proj(3,'Fernwave listing','Live',{by:'owner'})]}];
const when='Listing is live with a link to us';
const success={
 'project:1':{condition:when,proof:'link',by:'review',done:false,done_by:null,evidence:null,not_proven:'unlinked',
  blocker:{kind:'no_reply',days:12,event_id:7,follow_ups:false,todo:{id:'c1',title:'Nudge Paperkite listing: no reply in 12 days'}}},
 'project:2':{condition:when,proof:'link',by:'review',done:true,done_by:'evidence',evidence:{event_id:42,url:'https://blog.bramblebox.example/best-crm-tools',at:day(1)},not_proven:null,blocker:null},
 'project:3':{condition:'Lee confirms it is published',proof:'message',by:'owner',done:true,done_by:'owner',evidence:null,not_proven:null,blocker:null}};
const detail=id=>{const p=boards[0].projects.find(x=>x.id===id),s=success[id];
 return {id,kind:'project',name:p.name,strength:1,last_at:day(2),signals:3,state:'open',ids:[],links:[],recent:[],around:[],open:{},
  project:{node_id:id,name:p.name,board_id:1,stage:p.stage,org:null,value:null,notes:'',people:[],archived:false,outcome:null,outcome_reason:null,...(s.condition?{condition:s.condition,proof:s.proof}:{})},
  board:{board:'Partner listings',stage:p.stage,next:id==='project:1'?'Ask Kai to add the link':null,moves:[{stage:p.stage,reason:'Kai says it is live',source:'review',at:day(1),event_id:42}],stages:stages.map(s=>s.name),success:s}}};
let calls=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');res.end(JSON.stringify(n?detail(n):{projects:[],people:[],quiet:[],new:[],orgs:[],boards,person_names:[],project_names:[]}));return}
 if(req.method!=='GET'&&!url.pathname.startsWith('/brand/'))calls.push(JSON.parse(body||'{}'));
 if(url.pathname==='/api/action'){const c=JSON.parse(body||'{}');res.end(JSON.stringify(c.action==='project_save'?{node_id:c.args.node_id,name:c.args.name,created:false}:{}));return}
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
const project=async(page,id)=>{await page.evaluate(id=>document.querySelector(`.tile[data-node="${id}"] .tile-name`).click(),id);await page.locator('.graph-detail .ps-box').waitFor()};
const fits=(page,where)=>page.evaluate(()=>({page:document.documentElement.scrollWidth,vw:innerWidth})).then(s=>assert.ok(s.page<=s.vw,`${where}: wider than the screen ${JSON.stringify(s)}`));
const shot=async(page,name)=>{if(process.env.PS_SHOT){await page.locator('.graph-detail .graph-stage').scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.PS_SHOT}/${name}.png`})}};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [w,h] of [[1280,800],[390,844]])for(const scheme of ['light','dark']){const {context,page}=await open(w,h,scheme);
  // Not proven yet, and what's in the way with its to-do
  await project(page,'project:1');const box=page.locator('.graph-detail .ps-box');
  assert.equal(await box.locator('.ps-when').textContent(),'Done when: '+when);
  assert.equal(await box.locator('.ps-proof.warn').textContent(),'Not proven yet: The page doesn’t link to you yet');
  assert.equal(await box.locator('.ps-block').textContent(),'No reply in 12 days · To-do');
  assert.equal(await box.locator('.ps-block a').getAttribute('href'),'#card=c1');
  await fits(page,`${w} ${scheme} not proven`);await shot(page,`project-blocked-${w}-${scheme}`);
  // Proven: when, the page, and its message to read
  await page.evaluate(()=>document.querySelector('[data-crumb="projects"]')?.click());await page.locator('#people-view .pboard').waitFor();
  await project(page,'project:2');
  const proof=page.locator('.graph-detail .ps-proof.ok');assert.match(await proof.textContent(),/^Proven .+ · blog\.bramblebox\.example\/best-crm-tools Read$/);
  assert.equal(await proof.locator('a').getAttribute('href'),'https://blog.bramblebox.example/best-crm-tools');
  assert.equal(await proof.locator('[data-quote-event]').getAttribute('data-quote-event'),'42');
  assert.equal(await page.locator('.graph-detail .ps-block').count(),0);
  await fits(page,`${w} ${scheme} proven`);await shot(page,`project-proven-${w}-${scheme}`);
  // Done by hand
  await page.evaluate(()=>document.querySelector('[data-crumb="projects"]')?.click());await page.locator('#people-view .pboard').waitFor();
  await project(page,'project:3');assert.equal(await page.locator('.graph-detail .ps-proof').textContent(),'Marked done by hand');
  await context.close()}
 // The dialog: Done when and Proof, posted only when changed
 {const {context,page}=await open(1280,800);await project(page,'project:1');
  calls=[];await page.locator('.graph-detail [data-proj-edit]').first().click();await page.locator('#project-dialog[open]').waitFor();
  assert.equal(await page.locator('#project-form [name=condition]').inputValue(),when);
  assert.equal(await page.locator('#project-form [name=proof]').inputValue(),'link');
  if(process.env.PS_SHOT)await page.locator('#project-dialog').screenshot({path:`${process.env.PS_SHOT}/project-dialog-1280-light.png`});
  await page.locator('#project-form button.primary').click();await page.locator('#project-dialog[open]').waitFor({state:'detached'});
  assert.ok(!('condition' in calls.find(c=>c.action==='project_save').args),'unchanged: not sent');
  calls=[];await page.locator('.graph-detail [data-proj-edit]').first().click();await page.locator('#project-dialog[open]').waitFor();
  await page.locator('#project-form [name=condition]').fill('Kai confirms it is published');await page.locator('#project-form [name=proof]').selectOption('message');
  await page.locator('#project-form button.primary').click();await page.locator('#project-dialog[open]').waitFor({state:'detached'});
  const saved=calls.find(c=>c.action==='project_save').args;assert.deepEqual([saved.condition,saved.proof],['Kai confirms it is published','message']);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('project success dashboard ok');
}finally{await browser?.close();server.close()}
