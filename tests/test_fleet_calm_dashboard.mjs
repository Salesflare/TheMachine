import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The Fleet tab stays calm: one primary button per box, a Machine's safety number folded away (never a raw code in
// the open), "To-dos" never broken at its hyphen, one way into What's shared, a "who knows" question said once with
// each answer under it, no keyboard ring on a plain open, and a ring that shows whole when a key brings it.
// FLEET_SHOTS=<dir> saves the Fleet view at each size.
const dashboard=await dashboardPage();
const FL='fl_'+'a'.repeat(16),at='2026-10-20T08:00:00+00:00',FP='6196 c6b8 45f5 22b7 76d0 68fa';
const view={on:true,ask_meetings:false,kinds:{},kind_rules:{},no_details:[],scoped:[],scopes:{},
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:[],
   people:[{member_id:'m',name:'Sam Doe',role:'owner',me:true,email:'sam@acme.example'},{member_id:'p',name:'Pat Lee',role:'member',email:'pat@acme.example'},{member_id:'k',name:'Kim Ray',role:'admin',email:'kim@acme.example'}],
   members:[{member_id:'p',name:'Pat Lee',rules:{}},{member_id:'k',name:'Kim Ray',rules:{}}],rules:{},exceptions:{}}],
 shared:{prompts:[
   {id:'s1',fleet:FL,kind:'optout',name:'Pat Lee',email:'pat@acme.example',fp:FP},
   {id:'s2',fleet:FL,kind:'member',name:'Kim Ray',email:'kim@acme.example',fp:FP,fleet_name:'Acme'},
   {id:'s3',fleet:FL,kind:'successor',name:'Kim Ray',email:'kim@acme.example',fp:FP,fleet_name:'Acme'},
   {id:'s4',fleet:FL,kind:'recipient',name:'Pat Lee',email:'pat@acme.example',fp:FP,service:'intercom'}],
  graph:[{fleet:FL,confirmed:true,paused:true,teammates:2,admin:true,new_devices:[{member:'p',name:'Pat Lee',fp:FP,from:at}]}],
  shares:[],accounts:[],can_share:[]},
 intro_offers:[{ask_id:'a1',fleet:FL,member_id:'p',name:'Pat Lee',about:'globex.example',label:'Globex'},{ask_id:'a2',fleet:FL,member_id:'k',name:'Kim Ray',about:'globex.example',label:'Globex'}],
 waiting:[],free:[],log:[],notices:[],
 asked:[{id:'a1',fleet:FL,name:'Pat Lee',question:'Who knows someone at Globex?',status:'answered',answer:'knows 2 people'},
  {id:'a2',fleet:FL,name:'Kim Ray',question:'Who knows someone at Globex?',status:'answered',answer:'knows 1 person'}]};
const server=createServer((req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify({suggestions:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}}));return}
 if(req.url==='/api/action'){res.end('{"ok":true}');return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(view));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const shots=process.env.FLEET_SHOTS;
try{
 for(const [scheme,width] of [['light',390],['dark',390],['light',1440],['dark',1440]]){
  const page=await (await browser.newContext({viewport:{width,height:900},colorScheme:scheme})).newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  // A plain open of #fleet: no keyboard ring on the first ask
  await page.goto(`http://127.0.0.1:${server.address().port}/#fleet`);
  const pane=page.locator('.fleet-pane:not([hidden])');await pane.locator('.fleet-box').first().waitFor();await page.waitForTimeout(400);
  const tag=`${scheme} ${width}px`;
  assert.equal(await page.locator('#fleet-view .kb-on').count(),0,`${tag}: a ring on a plain open`);
  // One primary per box
  const primaries=await pane.locator('.fleet-box').evaluateAll(bs=>bs.map(b=>[b.querySelector('h3')?.textContent,[...b.querySelectorAll('button.primary')].filter(x=>x.checkVisibility()).length]));
  for(const [h,n] of primaries)assert.ok(n<=1,`${tag}: ${n} primaries in ${h}`);
  assert.deepEqual(primaries.filter(([,n])=>n).map(([h])=>h),['Team Graph','Shared connections','Who knows someone?']);
  // The safety number: folded under its name, the code itself out of sight
  const fps=pane.locator('details.share-fp');
  assert.equal(await fps.count(),4);
  for(const d of await fps.all()){assert.equal(await d.evaluate(e=>e.open),false);assert.equal(await d.locator('summary').innerText(),"Their Machine's safety number")}
  assert.equal(await pane.getByText(FP).filter({visible:true}).count(),0,`${tag}: a raw safety number in the open`);
  await fps.first().locator('summary').click();assert.equal(await fps.first().locator('.mono').innerText(),FP);
  // "To-dos" on one line, whatever the width
  const word=page.locator('.fleet-todo .nobr',{hasText:'To-dos'});
  assert.equal(await word.count(),1);
  assert.equal(await word.evaluate(e=>e.getClientRects().length),1,`${tag}: To-dos broke at its hyphen`);
  // One way into What's shared: the Choose connections button, no second link
  const team=pane.locator('.fleet-box',{hasText:'Team Graph'});
  assert.equal(await team.locator('a[href^="#shared="]').count(),0);
  assert.equal(await team.locator('[data-shared-open]').count(),1);
  // Who knows: the question once, each answer under it
  const who=pane.locator('.fleet-box',{hasText:'Who knows someone?'});
  assert.equal(await who.getByText('Who knows someone at Globex?',{exact:true}).count(),1);
  // One list: Ask for an intro folded under the answer that offers it, no second block per person; the company by
  // name, never its domain, while the intro ask still carries the domain
  assert.match(await who.locator('.list article',{hasText:'Who knows someone at'}).innerText(),/Pat Lee · knows 2 people\s+Ask for an intro\s+Kim Ray · knows 1 person\s+Ask for an intro/);
  assert.doesNotMatch(await who.innerText(),/knows someone at Globex\.|globex\.example/);
  const intro=who.locator('details.fleet-intro');assert.equal(await intro.count(),2);
  assert.equal(await intro.first().locator('input').isVisible(),false);
  await intro.first().locator('summary').click();assert.ok(await intro.first().locator('input').isVisible());
  const form=intro.first().locator('.fleet-intro-form');
  assert.deepEqual([await form.getAttribute('data-about'),await form.getAttribute('data-member')],['globex.example','p']);
  await intro.first().locator('summary').click();
  // Every ask: its button at its own width, then Not now as text beside it, on one line
  for(const a of await pane.locator('.fleet-yn').all()){
   const r=await a.evaluate(e=>[...e.children].filter(b=>b.checkVisibility()).map(b=>{const x=b.getBoundingClientRect();return [Math.round((x.top+x.bottom)/2),x.width,e.getBoundingClientRect().width,getComputedStyle(b).backgroundColor]}));
   assert.equal(new Set(r.map(x=>x[0])).size,1,`${tag}: an ask's buttons on two lines`);assert.ok(r[0][1]<r[0][2]*0.6,`${tag}: a full-width ask button`);
   for(const x of r.slice(1))assert.equal(x[3],'rgba(0, 0, 0, 0)',`${tag}: Not now with a fill`)}
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${tag}: scrolls sideways`);
  if(shots){await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:`${shots}/fleet-calm-${width}-${scheme}.png`,fullPage:true})}
  // Keys pressed earlier (Escape) still land without a ring; j brings it, whole, not clipped to a line by its list
  await page.evaluate(()=>{location.hash='#todos'});await page.waitForTimeout(200);await page.keyboard.press('Escape');
  await page.evaluate(()=>{location.hash='#fleet'});await page.waitForTimeout(2500);
  assert.equal(await page.locator('#fleet-view .kb-on').count(),0,`${tag}: a ring after an earlier key`);
  await page.keyboard.press('j');const ring=page.locator('#fleet-view .kb-on');await ring.first().waitFor({timeout:5000});
  assert.equal(await ring.first().evaluate(e=>getComputedStyle(e.parentElement).overflow),'visible');
  assert.deepEqual(errors,[]);
  await page.context().close();
 }
 console.log('fleet calm dashboard: ok');
}finally{await browser.close();server.close()}
