import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from './openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Share with all in the Team Graph box (shared_connectors.member_oks): every ask goes at once and one line says
// "Sharing with 4…" while the request signs them and the round after it seals the Graph for them (graph_soon); then
// "Shared with 4." and the line is gone. A single Share says "Sharing…" at once. A member's link to their page in the
// owner's own Graph reads Profile, not "In Graph", so it isn't read as being in the team's Graph. Optional SHOT_DIR:
// screenshots of the box at 390, light and dark.
const dashboard=await readFile(new URL(process.env.DASHBOARD_FILE||'./dashboard.html',import.meta.url),'utf8');
const FL='fl_'+'d'.repeat(16),SHOTS=process.env.SHOT_DIR||'';
const names=['Rae Moss','Andi Vale','Yuki Bay','Sam Doe (test@acme.example)'];
const prompts=()=>names.map((name,i)=>({id:'p'+i,kind:'member',fleet:FL,fleet_name:'Acme',name,email:`m${i}@acme.example`,fp:'ab12 cd34 ef56 ab12 cd34 ef5'+i}));
const graph={fleet:FL,name:'Acme',admin:true,confirmed:true,prompts:[],off:null,waiting:0,week:null,teammates:2,started:true,paused:null,require:[],connections:[],people:[],new_devices:[],sending:0};
const fleet={on:true,kinds:{},kind_rules:{},no_details:[],scoped:[],scopes:{},waiting:[],asked:[],log:[],notices:[],
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:[],people:[{member_id:'me',name:'Olive Park',role:'owner',me:true,email:'olive@acme.example'},
  {member_id:'m2',name:'Yuki Bay',role:'member',email:'m2@acme.example',graph_node:'email:m2@acme.example'}],members:[],rules:{},exceptions:{}}],
 shared:{prompts:prompts(),shares:[],accounts:[],can_share:[],graph:[graph]}};
const calls=[];let release=null,polls=0;
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status')return res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}}));
 if(url.pathname==='/api/graph')return res.end(JSON.stringify({projects:[],quiet:[],new:[],orgs:[],boards:[],people:[],sharing:[graph]}));
 if(url.pathname==='/api/fleet'){if(graph.sending&&++polls>=2)graph.sending=0;return res.end(JSON.stringify(fleet))}  // the round ends after a poll
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='graph_share_all'){await new Promise(r=>release=r);const done=fleet.shared.prompts.length;fleet.shared.prompts=[];graph.sending=done;return res.end(JSON.stringify({ok:true,done}))}
  if(call.action==='fleet_share_ok'){await new Promise(r=>release=r);fleet.shared.prompts=fleet.shared.prompts.filter(p=>p.id!==call.args.id);graph.sending=1;return res.end(JSON.stringify({ok:true,done:true}))}
  return res.end('{"ok":true}')}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const shoot=async(page,path)=>{if(!SHOTS)return;await page.evaluate(()=>{const y=document.querySelector('.fleet-people li:last-child');window.scrollTo(0,y.getBoundingClientRect().top+scrollY-80)});await page.waitForTimeout(150);await page.screenshot({path:`${SHOTS}/${path}`})};
const waitRelease=async()=>{for(let i=0;i<100&&!release;i++)await new Promise(r=>setTimeout(r,50));assert.ok(release,'the request went');const r=release;release=null;r()};
try{
 for(const scheme of ['light','dark']){
  fleet.shared.prompts=prompts();graph.sending=0;polls=0;calls.length=0;
  const context=await browser.newContext({viewport:{width:390,height:900},colorScheme:scheme,serviceWorkers:'block'});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');
  await navClick(page.locator('nav [data-tab="fleet"]'));
  const box=page.locator('.fleet-box',{hasText:'Team Graph'});await box.waitFor();
  // The member list: a link to their own page, not a status that reads like the Team Graph
  const yuki=page.locator('.fleet-people li',{hasText:'Yuki Bay'});
  assert.equal(await yuki.locator('.fp-graph').textContent(),'Profile');
  assert.equal(await page.getByText('In Graph',{exact:true}).count(),0);
  assert.equal(await box.locator('[data-graph-all]').textContent(),'Share with all 4');
  await shoot(page,`box-${scheme}-1-asks.png`);
  // Share with all: every ask hidden and one line at once, before the request returns
  await box.locator('[data-graph-all]').click();
  await box.locator('.graph-sending',{hasText:'Sharing with 4…'}).waitFor();
  assert.equal(await box.locator('[data-share-ok][data-kind="member"]:visible').count(),0);
  assert.equal(await box.locator('[data-graph-all]').count(),0);
  await shoot(page,`box-${scheme}-2-sharing.png`);
  await waitRelease();
  assert.deepEqual(calls.filter(c=>c.action==='graph_share_all'),[{action:'graph_share_all',args:{fleet:FL}}]);
  assert.equal(calls.filter(c=>c.action==='fleet_share_ok').length,0);  // one request for all, not one per person
  // Sealing runs after the request: the line stays while the Machine says it is sending, then "Shared with 4."
  await page.locator('#toast',{hasText:'Shared with 4.'}).waitFor({timeout:15000});
  await box.locator('.graph-sending').waitFor({state:'detached'});
  assert.equal(await box.locator('[data-share-ok]').count(),0);
  await shoot(page,`box-${scheme}-3-done.png`);
  // A single Share: "Sharing…" at once, the ask gone when it's signed
  fleet.shared.prompts=prompts().slice(0,1);polls=0;await page.evaluate(()=>fleetView(true));
  const one=box.locator('[data-share-ok="p0"][data-choice="yes"]');await one.click();
  assert.equal(await one.textContent(),'Sharing…');assert.ok(await one.isDisabled());
  await waitRelease();
  await box.locator('#share-p0').waitFor({state:'detached'});
  await box.locator('.graph-sending',{hasText:'Sharing with 1…'}).waitFor();
  await box.locator('.graph-sending').waitFor({state:'detached',timeout:15000});
  // no sideways scroll
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  assert.deepEqual(errors,[]);
  await context.close();
 }
 console.log('share all dashboard ok');
}finally{await browser.close();server.close()}
