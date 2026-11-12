import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A handoff that ran out: the to-do's prepared result still waits on the teammate and leads with Review handoff. Do it
// myself makes it the owner's own (fleet_handoff_mine, Store.handoff_mine_card): it leaves Waiting on others for For you,
// and its own buttons lead (Mark done), not the handoff. At 390 and 1440, light and dark; SHOTS=<dir> for screenshots.
// No network beyond this fake server; made-up data only.
const dashboard=await dashboardPage();
const handoff={kind:'handoff',label:'Hand off to Kim',revision:'h00000000001',to_email:'kim@acme.example',to_name:'Kim Doe',body:'Can you log the export bug and link the issue?'};
const fresh=()=>({id:'c1',title:'Waiting on Kim: log the export bug',body:'Prepared a short handoff to Kim through The Machine.',status:'prepared',event_ids:[1],scope:'work',
 created_at:new Date().toISOString(),outcome:JSON.stringify({state:'waiting',waiting_on:'Kim Doe'}),next_actions:[handoff],fleet_handoff:{name:'Kim Doe',stage:'expired',back:true}});
let card;
const state={get suggestions(){return [card]},connectors:[],suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}};
const view={on:true,kinds:{handoff:'handoffs'},ask_meetings:false,fleets:[],waiting:[],asked:[],intro_offers:[],splits:[],log:[],notices:[]};
const calls=[];
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify(state));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  // what the service does now: the handoff note stays, the result no longer waits on them, the handoff step goes
  if(call.action==='fleet_handoff_mine')Object.assign(card,{fleet_handoff:{...card.fleet_handoff,back:false},outcome:null,next_actions:[]});
  res.end(JSON.stringify({ok:true}));return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(view));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 for(const [width,height] of [[390,844],[1440,900]])for(const scheme of ['light','dark']){
  card=fresh();
  const page=await (await browser.newContext({viewport:{width,height},colorScheme:scheme})).newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#waiting-list').waitFor();
  await page.locator('#waiting-head').click();
  const before=page.locator('#waiting-list #task-c1');await before.waitFor();
  assert.match(await before.innerText(),/Kim Doe didn’t answer in time\./);
  await before.locator('[data-handoff-mine]').click();
  await page.waitForFunction(()=>!document.querySelector('#waiting-list #task-c1')&&document.querySelector('#suggestions #task-c1'));
  assert.equal(calls.at(-1).action,'fleet_handoff_mine');
  assert.equal(await page.locator('#waiting-list').count(),0);  // nothing left waiting on others
  assert.ok(await page.locator('#section-foryou').count(),'For you shows');
  const c=page.locator('#suggestions #task-c1');
  const primary=c.locator('.actions>button.primary');
  assert.equal(await primary.count(),1);
  assert.equal(await primary.innerText(),'Mark done');  // its own to-do button leads
  assert.equal(await c.locator('[data-fleet-handoff].primary,[data-handoff-mine]').count(),0);  // no Review handoff, no Do it myself again
  assert.doesNotMatch(await c.innerText(),/Waiting on: /);
  assert.match(await c.innerText(),/Kim Doe didn’t answer in time\./);  // the note stays
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'scrolls sideways');
  if(process.env.SHOTS){await c.scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.SHOTS}/do-it-myself-${width}-${scheme}.png`})}
  assert.deepEqual(errors,[]);
  await page.context().close();
 }
 console.log('handoff do it myself dashboard: ok');
}finally{await browser.close();server.close()}
