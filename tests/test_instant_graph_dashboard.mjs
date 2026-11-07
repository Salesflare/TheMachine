import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Graph answers at once. A board's "could belong here" Add and Leave out take the row away before the Machine
// answers (board_fit goes behind it, then the overview reloads quietly); a refused one brings the row back with the
// error. A person's row fetches its page when the pointer rests on it (graphPeekStart) or a finger lands on it, so the
// click opens it without asking again; a finger that scrolls calls it off, and a change sent to the Machine forgets what
// was fetched ahead. Back to a list that answers fast never shows a loading line. INSTANT_SHOT=<dir>
// writes screenshots.
const dashboard=await dashboardPage();
const stages=[{name:'Discovery'},{name:'Demo'},{name:'Won'},{name:'Stalled or declined',side:true}];
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const proj=(i,name,stage)=>({id:'project:'+i,name,stage,reason:'a made-up reason',by:'review',at:day(i),event_id:100+i,days:i,no_reply_days:0,org:{name,logo:null}});
const fresh=()=>[{id:1,name:'Demos and trials',stages,default:true,stuck:0,projects:[proj(1,'Paperkite','Demo'),proj(2,'Bramblebox','Won')],
 maybes:[{id:'org:tinkerlane.example',name:'Tinker Lane',why:'asked about pricing once'},{id:'org:puffin.example',name:'Puffin Metrics',why:'an intro call, no demo yet'},
  {id:'project:10',name:'Saffron Sync',why:'a partner, maybe a trial'}]}];
const person={id:'email:mara@northwind.example',kind:'person',name:'Mara Ellison',strength:4,closeness:'close',last_at:day(1),signals:12,ids:['mara@northwind.example'],
 role:null,org:null,side:'work',edited:[],phones:[],emails:[{value:'mara@northwind.example',by:'messages'}],joined:[],links:[],recent:[],around:[],open:{}};
let boards=fresh(),fitDelay=0,refuse=false,answered=0;const nodeAsks=[],fits=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');if(n){nodeAsks.push(n);res.end(JSON.stringify(person));return}
  res.end(JSON.stringify({projects:[],people:[person],quiet:[],new:[],orgs:[],boards,person_names:[],project_names:[]}));return}
 if(url.pathname==='/api/action'){const c=JSON.parse(body||'{}'),a=c.args||{};
  if(c.action==='board_fit'){fits.push(a);await new Promise(ok=>setTimeout(ok,fitDelay));res.on('finish',()=>answered++);if(refuse){res.statusCode=400;res.end(JSON.stringify({error:'That board changed meanwhile'}));return}
   const ids=a.node_ids||[a.node_id];boards[0].maybes=boards[0].maybes.filter(m=>!ids.includes(m.id));
   res.end(JSON.stringify({added:!!a.add,decided:ids.length,projects:a.add?ids.length:0,skipped:0,undo:'tok'}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const shot=async(page,name)=>{if(process.env.INSTANT_SHOT)await page.screenshot({path:`${process.env.INSTANT_SHOT}/${name}.png`,fullPage:false})};
const summary=page=>page.locator('.board-fits summary').textContent();
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]){
  boards=fresh();fitDelay=0;refuse=false;fits.length=0;nodeAsks.length=0;const mobile=width<600,tag=`${width}-${scheme}`;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(tag+': '+e.message));await page.goto(base);
  await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());await page.locator('#people-view').waitFor({state:'attached'});
  // A person's row: resting the pointer on it fetches the page once; the click opens it from that
  if(!mobile){const row=page.locator(`#people-view [data-node="${person.id}"]`).first();await row.waitFor();
   await row.hover();await page.waitForTimeout(300);await row.hover({position:{x:4,y:4}});await page.waitForTimeout(200);
   assert.deepEqual(nodeAsks,[person.id],'fetched once ahead');
   await row.click();await page.locator('#people.graph-on-node').waitFor();await page.locator('#people-view',{hasText:'Mara Ellison'}).waitFor();
   assert.deepEqual(nodeAsks,[person.id],'the click used it');
   // a change sent to the Machine forgets what was fetched ahead
   await page.evaluate(id=>graphPeekStart(id),'email:other@example.org');await page.waitForTimeout(100);
   await page.evaluate(()=>graphPost('noop',{}));assert.equal(await page.evaluate(()=>graphPeek.size),0)}
  else{const row=page.locator(`#people-view [data-node="${person.id}"]`).first();await row.waitFor();
   const touch=(type,dx=0)=>row.evaluate((el,[type,dx])=>{const r=el.getBoundingClientRect();el.dispatchEvent(new PointerEvent(type,{bubbles:true,pointerType:'touch',clientX:r.left+20+dx,clientY:r.top+10}))},[type,dx]);
   const ahead=()=>page.evaluate(id=>graphPeek.has(id),person.id);
   // a finger over a row is no hover: nothing is fetched ahead
   await touch('pointerover');await page.waitForTimeout(300);assert.deepEqual(nodeAsks,[],'no fetch on a touch hover');
   // a finger that moves is a scroll: the fetch it started is called off
   await touch('pointerdown');assert.ok(await ahead(),'started on touch');await touch('pointermove',30);assert.ok(!await ahead(),'called off on a scroll');
   await touch('pointerdown');await touch('pointercancel');assert.ok(!await ahead(),'called off when the browser scrolls');
   // a tap: the fetch starts as the finger lands, and the click opens the page from it
   await page.waitForTimeout(100);nodeAsks.length=0;await touch('pointerdown');assert.ok(await ahead());await touch('pointerup');
   await row.evaluate(el=>el.click());await page.locator('#people.graph-on-node').waitFor();await page.locator('#people-view',{hasText:'Mara Ellison'}).waitFor();
   assert.deepEqual(nodeAsks,[person.id],'the tap used the fetch from touching it')}
  // From the page back to a list: no loading line in the first 100 ms (a fast answer never shows one), the page stays up
  await page.evaluate(()=>{graphKept=null;window.sawLoading=null;new MutationObserver(()=>{if(window.sawLoading==null&&document.querySelector('#people-view .pager-loading'))window.sawLoading=performance.now()-window.t0}).observe(document.querySelector('#people-view'),{childList:true,subtree:true});
   window.t0=performance.now();showTab('people','people');return !!document.querySelector('#people-view .person-head')}).then(up=>assert.ok(up,'the page stays up meanwhile'));
  await page.locator('#people:not(.graph-on-node) [data-graph-panel="people"]').waitFor();
  const saw=await page.evaluate(()=>window.sawLoading);assert.ok(saw==null||saw>=100,'no loading line within 100 ms: '+saw);
  await page.evaluate(()=>document.querySelector('[data-graph-sub="projects"]').click());
  await page.locator('#people-view .proj-board:not([hidden]) .pboard').waitFor();
  await page.locator('.board-fits summary').click();assert.match(await summary(page),/3 projects could belong here/);
  await page.locator('.board-fits').scrollIntoViewIfNeeded();await shot(page,`board-fits-${tag}`);
  // Add, the Machine slow: the row leaves at once and the count follows; the toast comes once it landed
  fitDelay=3000;const n0=answered;await page.locator('[data-fit-add="org:tinkerlane.example"]').click();
  assert.match(await summary(page),/2 projects could belong here/);assert.equal(await page.locator('[data-fit-add="org:tinkerlane.example"]').count(),0);
  assert.equal(answered,n0,'before the save landed');assert.equal(await page.locator('.board-fits[open]').count(),1,'stays open');
  await page.waitForFunction(()=>document.querySelector('#toast.show')?.textContent.includes('Added to the board.'),null,{timeout:10000});
  assert.deepEqual(fits,[{board_id:1,node_id:'org:tinkerlane.example',add:true}]);
  await page.waitForTimeout(300);assert.match(await summary(page),/2 projects could belong here/,'the reload agrees');
  // A refused Leave out: the row comes back, with the error
  fitDelay=300;refuse=true;await page.locator('[data-fit-skip="org:puffin.example"]').click();
  assert.equal(await page.locator('[data-fit-skip="org:puffin.example"]').count(),0,'left at once');
  await page.waitForFunction(()=>document.querySelector('#toast.error')?.textContent.includes('That board changed meanwhile'),null,{timeout:10000});
  await page.locator('[data-fit-skip="org:puffin.example"]').waitFor();assert.match(await summary(page),/2 projects could belong here/);
  // the last ones: the fold goes at once
  refuse=false;fitDelay=800;await page.locator('[data-fit-bulk="skip"]').click();
  assert.equal(await page.locator('.board-fits:not([hidden])').count(),0,'the fold went at once');
  await page.waitForFunction(()=>document.querySelector('#toast.show')?.textContent.includes('Left out 2.'),null,{timeout:10000});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('instant graph dashboard ok');
}finally{await browser?.close();server.close()}
