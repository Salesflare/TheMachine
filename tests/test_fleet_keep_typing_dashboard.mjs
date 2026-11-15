import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {callAfter,quiet} from './page-calls.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Fleet › Sharing: someone typing in a rule's field while an earlier save's redraw comes in (a wide rule's answer draws
// the Fleet view again from api/fleet) keeps what they typed, its fold stays open and focus stays in it. Then leaving the
// field saves it. The redraw used to replace the field: the words went, and with them the save.
const dashboard=await dashboardPage();
const FL='fl_'+'a'.repeat(16);
const rules=()=>({relationships:{rule:'ask',details:false},meeting:{rule:'always',details:true},handling:{rule:'ask',details:false},brief:{rule:'never',details:false}});
const view={on:true,kinds:{relationships:'who knows someone',meeting:'meeting context',handling:'who handles shared emails',brief:'brief facts'},ask_meetings:false,
 kind_rules:{relationships:['ask','always','never'],meeting:['ask','always','never'],handling:['ask','always','never'],brief:['ask','always','never']},
 no_details:['handling','brief'],scoped:['relationships','meeting','handling'],scopes:{[FL]:{'*':{relationships:{only:['acme.com'],never:['initech'],work_only:true}}}},
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:['relationships','meeting'],
  people:[{member_id:'m',name:'Sam Doe',role:'owner',me:true,answers_with:'Self-hosted: Desk',email:'sam@acme.example'}],
  members:[{member_id:'q',name:'Alex Lee',rules:rules()}],rules:rules(),exceptions:{}}],
 waiting:[],asked:[],log:[],notices:[]};
let held=null;  // the Fleet view's answer waits for the test while set
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify({suggestions:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}}));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;const a=JSON.parse(body).args,w=view.fleets[0];
  if(a.rule)w.rules[a.kind].rule=a.rule;
  const scope=a.scope?{only:String(a.scope.only).split(',').map(x=>x.trim()).filter(Boolean),never:String(a.scope.never).split(',').map(x=>x.trim()).filter(Boolean),work_only:a.scope.work_only}:(view.scopes[FL]['*'][a.kind]||{only:[],never:[],work_only:true});
  if(a.scope)view.scopes[FL]['*'][a.kind]=scope;
  res.end(JSON.stringify({...w.rules[a.kind],scope}));return}
 if(req.url.startsWith('/api/fleet')){await held;res.end(JSON.stringify(view));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 for(const width of [390,1000]){
  const page=await (await browser.newContext({viewport:{width,height:900}})).newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await navClick(page.locator('nav [data-tab="fleet"]'));await page.locator('.fleet-pane-head h2',{hasText:/^Acme$/}).waitFor();
  await page.locator('[data-fleet-pane="sharing"]').click();await page.locator('.fleet-rules-head').waitFor();
  const R=k=>page.locator(`.fleet-rule[data-member="*"][data-kind="${k}"]`);
  // A wide rule saved: its answer asks for the Fleet view again, which is held while the next rule is typed in
  let release;held=new Promise(r=>release=r);
  const asked=page.waitForRequest(r=>new URL(r.url()).pathname==='/api/fleet');
  await callAfter(page,'fleet_rule',()=>R('handling').locator('[data-fleet-rule][value="always"]').check({force:true}));
  await asked;
  await R('relationships').locator('.fleet-scope summary').click();
  const never=R('relationships').locator('[data-scope="never"]');
  await never.fill('Globex, rival.example');
  const redrawn=page.waitForResponse(r=>new URL(r.url()).pathname==='/api/fleet');
  release();held=null;await redrawn;await quiet(page);
  // Drawn again, the field still has the words, its fold is open and focus is in it
  assert.equal(await never.inputValue(),'Globex, rival.example',width+': what was typed stays');
  assert.ok(await R('relationships').locator('.fleet-scope').evaluate(d=>d.open),width+': its fold stays open');
  assert.ok(await never.evaluate(e=>e===document.activeElement),width+': focus stays in it');
  // and leaving it saves it
  const call=await callAfter(page,c=>c.action==='fleet_rule'&&!!c.args.scope,()=>never.press('Tab'));
  assert.deepEqual(call.args,{fleet:FL,member_id:'*',kind:'relationships',scope:{only:'acme.com',never:'Globex, rival.example',work_only:true}});
  assert.deepEqual(errors,[]);
  view.scopes[FL]['*'].relationships={only:['acme.com'],never:['initech'],work_only:true};view.fleets[0].rules=rules();
  await page.context().close();
 }
 console.log('fleet keep typing dashboard: ok');
}finally{await browser.close();server.close()}
