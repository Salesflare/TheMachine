import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A project's description (project_about.py) sits under its name line: one or two sentences The Machine keeps up to
// date, with when it was updated and Edit. Save makes it the owner's ("Edited by you"), with Keep it updated to hand it
// back. No description: nothing shows, and Edit description in the ⋯ menu opens the field. Made-up names.
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
  assert.equal(await box.locator('.about-meta').textContent(),`Updated ${updated} · Edit`);
  assert.equal(await box.locator('.about-form').isVisible(),false);
  await fits(page,tag);await shot(page,`project-about-${tag}`);
  // Edit: the text in one field; Cancel sends nothing
  await box.locator('[data-about-edit]').click();
  const ta=box.locator('textarea[name=text]');await ta.waitFor();
  assert.equal(await ta.inputValue(),TEXT);
  assert.equal(await box.locator('.proj-about-text').isVisible(),false,'the text steps aside while editing');
  await fits(page,tag+' editing');await shot(page,`project-about-edit-${tag}`);
  await box.locator('[data-about-cancel]').click();assert.equal(calls.length,0);
  assert.ok(await box.locator('.proj-about-text').isVisible());
  // Save makes it the owner's; it then offers Keep it updated
  await box.locator('[data-about-edit]').click();
  await ta.fill('  Pilot at the first plant only.  ');
  await box.locator('.about-form button:not([type])').click();
  await card.locator('.proj-about [data-about-op="auto"]').first().waitFor();
  assert.deepEqual(calls[0],{action:'project_about',args:{node_id:'project:7',op:'edit',text:'Pilot at the first plant only.'}});
  const mine=card.locator('.proj-about');
  assert.equal(await mine.locator('.proj-about-text').textContent(),'Pilot at the first plant only.');
  assert.equal(await mine.locator('.about-meta').textContent(),'Edited by you · Edit · Keep it updated');
  await fits(page,tag+' owner');await shot(page,`project-about-owner-${tag}`);
  await mine.locator('.about-meta [data-about-op="auto"]').click();
  await card.locator('.proj-about .about-meta [data-about-op="auto"]').waitFor({state:'detached'});
  assert.deepEqual(calls[1],{action:'project_about',args:{node_id:'project:7',op:'auto'}});
  // None: nothing shows; Edit description in the ⋯ menu opens the field
  node=fresh(null);await page.evaluate(()=>people(graphNode,true));
  await card.locator('.proj-about-text').waitFor({state:'detached'});
  assert.equal(await card.locator('.proj-about').isVisible(),false,'no empty section');
  await card.locator('.name-row .fact-menu summary').click();
  await card.locator('[data-about-write]').click();
  await card.locator('.proj-about textarea[name=text]').waitFor();
  assert.equal(await card.locator('.proj-about textarea[name=text]').inputValue(),'');
  await fits(page,tag+' new');await shot(page,`project-about-new-${tag}`);
  assert.deepEqual(errors,[]);await context.close();
 }
 console.log('project about dashboard ok');
}finally{await browser?.close();server.close()}
