import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Someone with no contact at all (only a to-do made about them) shows no last contact on People, on their page and
// on their organization's row: never "last contact never" or a made-up day. Someone with contact keeps theirs. SHOT_DIR=… saves screenshots.
const dashboard=await dashboardPage();
const day=new Date(Date.now()-3*864e5).toISOString().slice(0,10);
const person=(id,name,extra={})=>({id:'email:'+id,kind:'person',name,strength:0.02,closeness:'faint',last_at:null,signals:0,ids:[id],usual_gap_days:null,
 quiet:false,role:null,org:'org:'+id.split('@')[1],org_by:'email',seen_only:true,profile:null,links:[],recent:[],around:[],open:{},...extra});
const people=[
 person('ann@client.example','Ann Example',{strength:2.4,closeness:'regular',last_at:day,signals:5,seen_only:false,usual_gap_days:6}),
 person('lee@prospect.example','Lee Parker'),
 person('rae@prospect.example','Rae Quinn'),
];
const orgs=[{id:'org:prospect.example',kind:'org',name:'Prospect',strength:0.04,last_at:null,signals:2,domain:'prospect.example',profile:null,links:[],recent:[],around:[],open:{}}];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const node=url.searchParams.get('node');res.end(JSON.stringify(node?[...people,...orgs].find(p=>p.id===node):{projects:[],people,quiet:[],new:[],orgs}));return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const runs=process.env.SHOT_DIR?[[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]:[[390,844,'light']];
 if(process.env.SHOT_DIR)await mkdir(process.env.SHOT_DIR,{recursive:true});
 for(const [width,height,scheme] of runs){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,deviceScaleFactor:width<500?2:1}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await navClick(page.locator('nav [data-tab="people"]'));
  await navClick(page.locator('.side-sub a[data-graph-sub="people"]'));
  const row=id=>page.locator(`#people-view article[data-node="email:${id}"]`);
  await row('lee@prospect.example').waitFor();
  assert.match(await row('ann@client.example').textContent(),/last contact/);
  const lee=await row('lee@prospect.example').textContent();
  assert.doesNotMatch(lee,/last (contact|seen)|never/i);
  assert.match(lee,/Faint/);
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/people-${width}-${scheme}.png`});
  await navClick(page.locator('.side-sub a[data-graph-sub="orgs"]'));
  const org=page.locator('#people-view article[data-node="org:prospect.example"]');
  await org.waitFor();
  const orgText=await org.textContent();
  assert.match(orgText,/2 people/);
  assert.doesNotMatch(orgText,/last contact|never/i);
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/orgs-${width}-${scheme}.png`});
  await navClick(page.locator('.side-sub a[data-graph-sub="people"]'));
  await row('lee@prospect.example').waitFor();
  await row('lee@prospect.example').locator('button.node').click();
  await page.locator('#people.graph-on-node').waitFor({state:'attached'});await page.waitForFunction(()=>document.querySelector('#people-view').textContent.includes('Lee Parker')&&!document.querySelector('#people-view article[data-node]'));
  assert.doesNotMatch(await page.locator('#people-view').textContent(),/last contact never|last seen never/i);
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/person-${width}-${scheme}.png`});
  assert.deepEqual(errors,[]);
  await context.close();
 }
}finally{
 await browser?.close();
 server.close();
}
