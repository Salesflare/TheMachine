import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// When one person learns, everyone does: a Work to-do whose draft followed a team learning says so in one line in its
// Details, with Remove, which takes the learning out for the whole Fleet (fleet_learning_remove) and the line off the
// to-do. Its text stays text, never markup. SHOTS=<folder> saves screenshots at 1440x900, 1440x700 and 390x844.
const dashboard=await dashboardPage();
const FL='fl_'+'a'.repeat(16),FP='b'.repeat(32),TEXT='Refunds go out from the support inbox <b>with</b> the refund template.';
const email={kind:'email',label:'Send reply',revision:'e00000000001',account_id:'work',from:'owner@acme.example',to:['sam@client.example'],subject:'Your refund',body:'Hi Sam,\n\nThe refund is on its way.\n\nCheers,\n\nAlex'};
const card={id:'c1',title:'Answer the refund request',status:'prepared',event_ids:[1],scope:'work',created_at:new Date().toISOString(),
 body:'Drafted the refund reply.',next_actions:[email],team_learnings_used:[{fleet:FL,fp:FP,text:TEXT}]};
const state={suggestions:[card],connectors:[],suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}};
const calls=[];
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify(state));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='fleet_learning_remove')delete card.team_learnings_used;  // gone for the Fleet: no longer usable, so not shown
  res.end('{"ok":true,"result":{"removed":true}}');return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify({on:true,fleets:[],waiting:[],asked:[],log:[],notices:[]}));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const shots=process.env.SHOTS;
try{
 for(const [w,h] of shots?[[1440,900],[1440,700],[390,844]]:[[390,844]]){
  card.team_learnings_used=[{fleet:FL,fp:FP,text:TEXT}];calls.length=0;
  const page=await (await browser.newContext({viewport:{width:w,height:h}})).newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#task-c1 [data-details="c1"]').click();
  const line=page.locator('#task-c1 .card-details .fleet-learn-used');await line.waitFor();
  assert.equal(await line.count(),1);
  assert.equal(await line.innerText(),'Used a team learning: '+TEXT+' Remove');
  assert.equal(await line.locator('b').count(),0);  // text, never markup
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth)<=0,true);
  if(shots){await line.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/learning-used-${w}x${h}.png`})}
  await line.locator('[data-fleet-learn-remove]').click();
  await page.locator('#toast',{hasText:'Removed for the whole team.'}).waitFor();
  const removed=calls.find(c=>c.action==='fleet_learning_remove');
  assert.deepEqual(removed.args,{fleet:FL,fp:FP});
  await page.locator('#task-c1 .fleet-learn-used').waitFor({state:'detached'});
  assert.deepEqual(errors,[]);
  await page.context().close();
 }
 console.log('fleet learning used dashboard: ok');
}finally{await browser.close();server.close()}
