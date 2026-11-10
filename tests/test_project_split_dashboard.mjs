import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Split up (project_split.py) on a project's page: Split up… in its ⋯ asks for a proposal (one call), the preview shows
// each proposed project with its name, its line and its items, each with where it goes; the owner renames one, moves an
// item, takes one off and confirms. The page then says what it was split into, with Undo. Made-up names.
// At 390 and 1440, light and dark. SHOT_DIR=… saves screenshots.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const stages=[{name:'Contacted'},{name:'Pilot'},{name:'Live'},{name:'Stalled or declined',side:true}];
const fresh=()=>({id:'project:7',kind:'project',name:'Mixed bag',strength:1,last_at:day(1),signals:9,state:'active',ids:[],links:[],recent:[],around:[],open:{},
 about:{text:'The alloy pilot with Northwind, plus settings routes and sidebar entries.',by:'machine',at:day(1)},split:null,
 project:{node_id:'project:7',name:'Mixed bag',board_id:1,stage:'Pilot',org:null,value:null,close_date:null,notes:'',people:[],archived:false,outcome:null,outcome_reason:null},
 board:{board:'Customers',stage:'Pilot',next:null,moves:[],stages:stages.map(s=>s.name)}});
const PROPOSAL={node_id:'project:7',name:'Mixed bag',parts:[
 {name:'Northwind pilot',about:'The alloy pilot with Northwind: legal and the order form.',items:['h:11','h:12','t:s1','p:person:mara']},
 {name:'Settings pages',about:'Routes and sidebar entries for the settings pages.',items:['h:13','t:s2']}],
 items:{'h:11':{kind:'thread',label:'Pilot kickoff',sub:'Mara',at:day(9),count:2},'h:12':{kind:'thread',label:'Contract review',sub:'Mara',at:day(4)},
  'h:13':{kind:'thread',label:'Settings routes moved under /settings',sub:'Ivo',at:day(2)},'q:14':{kind:'thread',label:'Weekly digest',sub:'news@example.net',at:day(1),probable:true},
  't:s1':{kind:'todo',label:'Send Northwind the order form'},'t:s2':{kind:'todo',label:'Fix the sidebar entry'},
  'p:person:mara':{kind:'person',label:'Mara Quill',sub:'Northwind'},'p:person:ivo':{kind:'person',label:'Ivo Brandt',sub:''}}};
let node=fresh();const calls=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')?node:{projects:[],people:[],quiet:[],new:[],orgs:[],boards:[{id:1,name:'Customers',stages,default:true,stuck:0,maybes:[],projects:[]}]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);const a=call.args;
  if(a.op==='propose'){await new Promise(r=>setTimeout(r,300));res.end(JSON.stringify(PROPOSAL));return}
  if(a.op==='apply'){const projects=a.parts.map((p,i)=>({node_id:'project:'+(20+i),name:p.name}));node={...node,split:{id:5,at:day(0),into:projects}};res.end(JSON.stringify({split_id:5,projects,archived:false}));return}
  if(a.op==='undo'){node={...node,split:null};res.end(JSON.stringify({undone:5,node_id:'project:7',name:'Mixed bag'}));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 if(process.env.SHOT_DIR)await mkdir(process.env.SHOT_DIR,{recursive:true});
 const shot=async(page,name,full)=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/${name}.png`,fullPage:!!full})};
 const fits=(page,tag)=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth).then(ok=>assert.ok(ok,'no sideways scroll at '+tag));
 for(const [width,height,scheme] of [[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]){
  node=fresh();calls.length=0;const tag=`${width}x${height}-${scheme}`;
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,deviceScaleFactor:width<500?2:1,timezoneId:'America/New_York'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#graph/'+encodeURIComponent(node.id));
  const card=page.locator('#people-view .graph-detail');await card.locator('.proj-about').waitFor();
  // The ⋯ offers Split up…
  await card.locator('.name-row .fact-menu > summary').click();
  const item=card.locator('[data-proj-split="project:7"]');await item.waitFor();
  assert.equal((await item.textContent()).trim(),'Split up…');
  await shot(page,`split-menu-${tag}`);
  await item.click();
  const dialog=page.locator('#split-dialog'),form=dialog.locator('#split-form');
  await form.locator('.psplit-wait').waitFor();
  await form.locator('.psplit-part').first().waitFor();
  assert.deepEqual(calls.map(c=>c.args.op),['propose'],'one call per click');
  assert.equal(await form.locator('.psplit-part:not(.psplit-rest)').count(),2);
  assert.deepEqual(await form.locator('[name="split-name"]').evaluateAll(a=>a.map(i=>i.value)),['Northwind pilot','Settings pages']);
  assert.equal((await form.locator('.psplit-rest h3').textContent()).trim(),'Stays on Mixed bag');
  assert.equal(await form.locator('[data-split-item="q:14"] option[value="drop"]').count(),0,'a probable thread is never taken off, only left');
  assert.equal((await form.locator('button.primary').textContent()).trim(),'Split into 2 projects');
  await fits(page,tag+' preview');await shot(page,`split-preview-${tag}`);
  // Rename one, move a to-do, take Ivo off
  await form.locator('[name="split-name"]').nth(1).fill('Settings and sidebar');
  assert.equal(await form.locator('[data-split-item="h:11"] option[value="p1"]').textContent(),'Settings and sidebar','the menus follow the new name');
  await form.locator('[data-split-item="t:s1"]').selectOption('p1');
  await form.locator('[data-split-item="p:person:ivo"]').selectOption('drop');
  assert.equal((await form.locator('.psplit-rest h3').last().textContent()).trim(),'Taken off');
  await fits(page,tag+' changed');await shot(page,`split-preview-changed-${tag}`);
  await form.locator('button.primary').click();await dialog.waitFor({state:'hidden'});
  const apply=calls.at(-1);
  assert.equal(apply.args.op,'apply');
  assert.deepEqual(apply.args.parts.map(p=>p.name),['Northwind pilot','Settings and sidebar']);
  assert.deepEqual(apply.args.parts[1].items,['h:13','t:s2','t:s1']);
  assert.deepEqual(apply.args.drop,['p:person:ivo']);
  // The page says what it was split into, each a link, with Undo; the toast too
  const line=card.locator('.psplit-line');await line.waitFor();
  assert.match(await line.textContent(),/Split up on .*: Northwind pilot, Settings and sidebar · Undo/);
  assert.equal(await line.locator('.inline-node').count(),2);
  assert.equal(await page.locator('#toast [data-split-undo="5"]').count(),1);
  await fits(page,tag+' split');await shot(page,`split-result-${tag}`);
  await line.locator('[data-split-undo]').click();await line.waitFor({state:'detached'});
  assert.deepEqual(calls.at(-1),{action:'project_split',args:{op:'undo',split_id:5}});
  assert.deepEqual(errors,[]);await context.close();
 }
 console.log('project split dashboard ok');
}finally{await browser?.close();server.close()}
