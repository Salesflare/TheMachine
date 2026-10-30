import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A Fleet item among the to-dos ("Rae Moss joined Acme. Share the team's Graph with them?"): Share and Not now carry
// data-choice like a to-do's buttons, and the to-dos' own click handler once took them for a to-do decision too. It
// posted decide without a to-do, which failed as "Invalid request" while the share itself went through. Now only the
// Fleet's action goes, and the owner sees the share's own line, no error. Optional SHOT_DIR: a screenshot after Share.
const dashboard=await dashboardPage(process.env.DASHBOARD_FILE&&new URL(process.env.DASHBOARD_FILE,import.meta.url));
const FL='fl_'+'d'.repeat(16),SHOTS=process.env.SHOT_DIR||'';
const prompts=()=>[{id:'p0',kind:'member',fleet:FL,fleet_name:'Acme',name:'Rae Moss',email:'rae@acme.example',fp:'ab12 cd34 ef56 ab12 cd34 ef56'},
 {id:'p1',kind:'member',fleet:FL,fleet_name:'Acme',name:'Andi Vale',email:'andi@acme.example',fp:'ab12 cd34 ef56 ab12 cd34 ef57'}];
const graph={fleet:FL,name:'Acme',admin:true,confirmed:true,prompts:[],off:null,waiting:0,week:null,teammates:2,started:true,paused:null,require:[],connections:[],people:[],new_devices:[],sending:0};
const fleet={on:true,kinds:{},kind_rules:{},no_details:[],scoped:[],scopes:{},waiting:[],asked:[],log:[],notices:[],
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:[],people:[{member_id:'me',name:'Olive Park',role:'owner',me:true,email:'olive@acme.example'}],members:[],rules:{},exceptions:{}}],
 shared:{prompts:prompts(),shares:[],accounts:[],can_share:[],graph:[graph]}};
const calls=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status')return res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:fleet.shared.prompts.length}}));
 if(url.pathname==='/api/graph')return res.end(JSON.stringify({projects:[],quiet:[],new:[],orgs:[],boards:[],people:[],sharing:[graph]}));
 if(url.pathname==='/api/fleet')return res.end(JSON.stringify(fleet));
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='fleet_share_ok'){fleet.shared.prompts=fleet.shared.prompts.filter(p=>p.id!==call.args.id);return res.end(JSON.stringify({ok:true,done:call.args.choice==='yes'}))}
  if(call.action==='decide'&&!call.args.suggestion_id){res.statusCode=400;return res.end(JSON.stringify({error:'Invalid request'}))}  // what the server did
  return res.end('{"ok":true}')}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 for(const [width,height] of [[1440,900],[390,844]]){
  fleet.shared.prompts=prompts();calls.length=0;
  const context=await browser.newContext({viewport:{width,height},serviceWorkers:'block'});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');
  const card=page.locator('#suggestions #fleet-share-p0');await card.waitFor();
  assert.match(await card.locator('h3').textContent(),/Rae Moss joined Acme/);
  await card.locator('[data-share-ok="p0"][data-choice="yes"]').click();
  await page.locator('#toast',{hasText:'Done. Their Machine gets it next.'}).waitFor();
  await page.waitForTimeout(400);  // a second handler's request would have gone by now
  if(SHOTS)await page.screenshot({path:`${SHOTS}/fleet-card-share-${width}x${height}.png`});
  assert.deepEqual(calls.map(c=>c.action),['fleet_share_ok']);
  assert.deepEqual(calls[0].args,{id:'p0',choice:'yes'});
  assert.equal(await page.locator('#toast.error').count(),0);
  // Not now on the other one: also only the Fleet's answer
  calls.length=0;
  await page.locator('#suggestions [data-share-ok="p1"][data-choice="no"]').click();
  await page.locator('#toast',{hasText:'Okay.'}).waitFor();
  await page.waitForTimeout(400);
  assert.deepEqual(calls.map(c=>c.action),['fleet_share_ok']);
  assert.equal(await page.locator('#toast.error').count(),0);
  assert.deepEqual(errors,[]);
  await context.close();
 }
 console.log('fleet card to-do dashboard ok');
}finally{await browser.close();server.close()}
