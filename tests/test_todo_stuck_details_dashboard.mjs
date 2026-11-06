import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A stuck to-do whose prepared-ahead run timed out: Try again leads (not Do it), and its technical details sit under the
// to-do's one Details, never a second Details toggle. A long project name is whole on a phone, or in its tooltip.
const dashboard=await dashboardPage();
const ago=h=>new Date(Date.now()-h*3600e3).toISOString();
const project={node_id:'proj:billing',name:'Northwind billing correction for the October invoices'};
const cards=[
 {id:'s1s1s1s1s1s1s1s1',title:'Mark the Acme Sync and Beta Bridge apps as trusted clients',body:'Promised Sam Lee on Tue, Nov 3. Nothing shows it done yet.',status:'pending',scope:'work',
  created_at:ago(2),event_ids:[1],dedupe_key:'promise:1',source_line:'Slack DM with Sam Lee · Tue 3 Nov',preparation_status:'blocked',preparation_cause:'prepare_ahead',
  preparation_reason:'The client settings could not be read because the browser timed out; try again when browser access is working.',preparation_questions:[],preparation_no_questions:true,
  preparation_details:'Opened the client settings in its own tab. The page snapshot timed out twice. Closed the tab. Nothing was changed.'},
 {id:'p1p1p1p1p1p1p1p1',title:'Answer the question about the card updates',body:'Robin asks why the refund was declined after the payment card changed.',status:'pending',scope:'work',
  created_at:ago(15),event_ids:[2],project_node:project,project:project.name,people:[{id:'p:robin',name:'Robin Example'}]}];
const posts=[];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'&&req.method==='POST'){posts.push(JSON.parse(body||'{}'));res.end('{"status":"accepted","retrying":true}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[1440,700],[390,844]]){
  posts.length=0;
  const context=await browser.newContext({viewport:{width,height},colorScheme:'dark'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-s1s1s1s1s1s1s1s1').waitFor();
  const stuck=page.locator('#task-s1s1s1s1s1s1s1s1');
  assert.match(await stuck.innerText(),/Stuck/);
  // Try again leads; no Do it beside it
  assert.deepEqual(await stuck.locator('.actions button.primary').allTextContents(),['Try again']);
  assert.equal(await stuck.locator('[data-choice="accept"]').count(),0);
  // One Details on the to-do: the run's technical details are under it, folded
  assert.equal(await stuck.getByText('Details',{exact:true}).count(),1);
  assert.equal(await stuck.locator('details.tech').count(),0);
  assert.ok(!(await stuck.innerText()).includes('snapshot timed out'));
  if(process.env.SHOTS_DIR)await stuck.screenshot({path:`${process.env.SHOTS_DIR}/stuck-${width}x${height}.png`});
  await stuck.locator('.details-toggle').click();
  assert.equal(await stuck.locator('.card-details .tech-head').textContent(),'Technical details');
  assert.match(await stuck.locator('.card-details .tech-log pre').textContent(),/snapshot timed out twice/);
  if(process.env.SHOTS_DIR)await stuck.screenshot({path:`${process.env.SHOTS_DIR}/stuck-details-${width}x${height}.png`});
  await stuck.locator('[data-choice="retry"]').click();
  for(let i=0;i<100&&!posts.some(p=>p.action==='decide');i++)await page.waitForTimeout(50);
  assert.deepEqual([posts.find(p=>p.action==='decide')?.args.suggestion_id,posts.find(p=>p.action==='decide')?.args.choice],['s1s1s1s1s1s1s1s1','retry']);
  // The project chip: its whole name in its tooltip, and whole on the line when it fits the to-do's width
  const chip=page.locator('#task-p1p1p1p1p1p1p1p1 a.chip.project-link');
  assert.equal(await chip.getAttribute('title'),project.name);
  assert.ok(await chip.evaluate(a=>{const s=a.querySelector('span');return s.scrollWidth<=s.clientWidth+1}),'the project name is whole');
  if(process.env.SHOTS_DIR)await page.locator('#task-p1p1p1p1p1p1p1p1').screenshot({path:`${process.env.SHOTS_DIR}/project-chip-${width}x${height}.png`});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('stuck to-do details: ok');
