import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A project's description (project_about.py) sits under its name line: one or two sentences The Machine keeps up to
// date, with when it was updated. The project's own Edit changes it (a Description field under the name, with the
// form's Save); then it is the owner's ("Edited by you · Keep it updated"). No description: nothing shows, no gap, and
// Edit offers the empty field. Made-up names.
// At 390 and 1440, light and dark. SHOT_DIR=… saves screenshots.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const TEXT='Rollout of the alloy line at Northwind’s first plant. Legal reviews the contract; you owe Mara the signed order form by Friday.';
const stages=[{name:'Contacted'},{name:'Agreed'},{name:'Live'},{name:'Stalled or declined',side:true}];
const fresh=(about={text:TEXT,by:'machine',at:day(1)})=>({id:'project:7',kind:'project',name:'Northwind rollout',strength:1,last_at:day(1),signals:9,state:'active',
 ids:[],links:[],recent:[],around:[],open:{},about,
 project:{node_id:'project:7',name:'Northwind rollout',board_id:1,stage:'Agreed',org:null,value:24000,close_date:null,notes:'',people:[],archived:false,outcome:null,outcome_reason:null},
 board:{board:'Customers',stage:'Agreed',next:null,moves:[{stage:'Agreed',reason:'Mara confirmed the pilot',source:'review',at:day(3),event_id:42}],stages:stages.map(s=>s.name)}});
let node=fresh();const calls=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')?node:{projects:[],people:[],quiet:[],new:[],orgs:[],boards:[{id:1,name:'Customers',stages,default:true,stuck:0,maybes:[],projects:[]}]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);const a=call.args;
  if(call.action==='project_about')node={...node,about:a.op==='edit'?{text:a.text,by:'owner',at:day(0)}:{...node.about,by:'machine'}};
  if(call.action==='project_save'){res.end(JSON.stringify({node_id:a.node_id,name:a.name}));return}
  res.end(JSON.stringify({about:node.about}));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 if(process.env.SHOT_DIR)await mkdir(process.env.SHOT_DIR,{recursive:true});
 const shot=async(page,name)=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/${name}.png`})};
 const fits=(page,tag)=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth).then(ok=>assert.ok(ok,'no sideways scroll at '+tag));
 for(const [width,height,scheme] of [[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]){
  node=fresh();calls.length=0;const tag=`${width}x${height}-${scheme}`;
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,deviceScaleFactor:width<500?2:1,timezoneId:'America/New_York'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#graph/'+encodeURIComponent(node.id));
  const card=page.locator('#people-view .graph-detail');await card.locator('.proj-about').waitFor();
  const box=card.locator('.proj-about');
  // Right under the name line, before the board; the model's words are never machine-translated
  assert.equal(await box.evaluate(e=>e.previousElementSibling?.classList.contains('detail-sub')),true,tag);
  assert.equal(await box.locator('.proj-about-text').textContent(),TEXT);
  assert.equal(await box.locator('.proj-about-text[translate="no"]').count(),1);
  const updated=await page.evaluate(d=>shortDay(d),node.about.at);
  assert.equal(await box.locator('.about-meta').textContent(),`Updated ${updated}`);
  assert.equal(await card.locator('[data-about-edit],.about-form,[data-about-write]').count(),0,'one Edit: the project\'s');
  await fits(page,tag);await shot(page,`project-about-${tag}`);
  // Edit: the Description field under the name, filled; Save is the form's primary button
  const dialog=page.locator('#project-dialog');
  await card.locator('.name-row [data-proj-edit]').click();
  const ta=dialog.locator('textarea[name=about]');await ta.waitFor();
  assert.equal(await ta.inputValue(),TEXT);
  assert.equal(await dialog.locator('.pj-about').evaluate(e=>e.previousElementSibling?.querySelector('[name=name]')!=null),true,'right under the name');
  assert.equal(await dialog.locator('[data-pj-about-auto]').count(),0);
  assert.equal(await dialog.locator('button.primary').count(),1);
  await fits(page,tag+' editing');await shot(page,`project-about-edit-${tag}`);
  // Saved unchanged: no description call
  await dialog.locator('button.primary').click();await dialog.waitFor({state:'hidden'});
  assert.deepEqual(calls.map(c=>c.action),['project_save']);
  // Changed: the owner's, with Keep it updated
  await card.locator('.name-row [data-proj-edit]').click();await ta.waitFor();
  await ta.fill('  Pilot at the first plant only.  ');
  await dialog.locator('button.primary').click();await dialog.waitFor({state:'hidden'});
  assert.deepEqual(calls.at(-1),{action:'project_about',args:{node_id:'project:7',op:'edit',text:'Pilot at the first plant only.'}});
  const mine=card.locator('.proj-about');await mine.locator('[data-about-op="auto"]').waitFor();
  assert.equal(await mine.locator('.proj-about-text').textContent(),'Pilot at the first plant only.');
  assert.equal(await mine.locator('.about-meta').textContent(),'Edited by you · Keep it updated');
  await fits(page,tag+' owner');await shot(page,`project-about-owner-${tag}`);
  // The form says so too, and Keep it updated works there
  await card.locator('.name-row [data-proj-edit]').click();await ta.waitFor();
  assert.equal((await dialog.locator('.pj-about-note').textContent()).trim(),'Edited by you · Keep it updated');
  await shot(page,`project-about-owner-edit-${tag}`);
  await dialog.locator('[data-pj-about-auto]').click();await dialog.locator('[data-pj-about-auto]').waitFor({state:'detached'});
  assert.deepEqual(calls.at(-1),{action:'project_about',args:{node_id:'project:7',op:'auto'}});
  await dialog.locator('[data-pj-close]').first().click();await dialog.waitFor({state:'hidden'});
  // Keep it updated on the page
  node={...node,about:{text:'Ours.',by:'owner',at:day(0)}};await page.evaluate(()=>people(graphNode,true));
  await card.locator('.proj-about [data-about-op="auto"]').click();
  await card.locator('.proj-about [data-about-op="auto"]').waitFor({state:'detached'});
  assert.deepEqual(calls.at(-1),{action:'project_about',args:{node_id:'project:7',op:'auto'}});
  // None: nothing between the name line and the stage box; Edit offers the empty field
  node=fresh(null);await page.evaluate(()=>people(graphNode,true));
  await card.locator('.proj-about').waitFor({state:'detached'});
  assert.equal(await card.locator('.graph-sub.detail-sub').first().evaluate(e=>e.nextElementSibling?.classList.contains('graph-stage')||e.nextElementSibling?.className),true,'the stage box right under the name line: no gap or placeholder');
  await fits(page,tag+' new');await shot(page,`project-about-none-${tag}`);
  await card.locator('.name-row [data-proj-edit]').click();await ta.waitFor();
  assert.equal(await ta.inputValue(),'');
  assert.equal(await ta.getAttribute('placeholder'),'What it is and where it stands');
  await shot(page,`project-about-new-${tag}`);
  await dialog.locator('[data-pj-close]').first().click();await dialog.waitFor({state:'hidden'});
  // The To-dos heading counts the open ones; only done ones: no count at all (never an empty pill)
  const head=page.locator('.section-head:has(h2:text-is("To-dos"))');
  node={...fresh(),todos:[{id:'s1',title:'Send the order form',status:'completed',done:true}]};await page.evaluate(()=>people(graphNode,true));
  await head.waitFor();assert.equal(await head.locator('.count').count(),0,'no count when none is open');
  await shot(page,`project-todos-done-${tag}`);
  node={...fresh(),todos:[{id:'s2',title:'Book the plant visit',status:'pending',done:false},{id:'s1',title:'Send the order form',status:'completed',done:true}]};
  await page.evaluate(()=>people(graphNode,true));await head.locator('.count').waitFor();
  assert.equal(await head.locator('.count').textContent(),'1');
  await shot(page,`project-todos-open-${tag}`);
  assert.deepEqual(errors,[]);await context.close();
 }
 console.log('project about dashboard ok');
}finally{await browser?.close();server.close()}
