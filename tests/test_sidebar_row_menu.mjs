import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The sidebar row's ⋯ menu (hover ⋯, right click, the menu key, a long press on a phone): Rename and Open, then the
// to-do's own Mark done, Snooze and Not needed, named as the to-do's buttons name them. Each answers like the to-do's
// own button: the decide action with that choice, the row leaves at once, the same message with Undo. A done to-do has
// Rename and Open only. Arrows move in the menu, Esc closes it and the keyboard stays on the list.
const dashboard=await dashboardPage();
const NOW=Date.parse('2026-10-22T10:30:00+02:00'),now=new Date(NOW).toISOString();
const id=n=>(n+'').padStart(2,'0').repeat(8);
const base0=()=>[
 {id:id(1),title:'Send the signed contract',body:'They asked on Monday.',status:'pending',scope:'work',created_at:now,event_ids:[1]},
 {id:id(2),title:'Book the dentist',body:'',status:'prepared',scope:'personal',created_at:now,event_ids:[2]},
 {id:id(3),title:'Pay the invoice',body:'The invoice is due Friday.',status:'pending',scope:'work',created_at:now,event_ids:[3]},
 {id:id(4),title:'Plan the offsite',body:'',status:'pending',scope:'work',created_at:now,event_ids:[4]},
 {id:id(5),title:'Order the cake',body:'',status:'completed',scope:'personal',created_at:now,closed_at:now,event_ids:[5]}];
let cards,actions;const reset=()=>{cards=base0();actions=[]};reset();
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);if(r.action!=='card_chat')actions.push(r);
  if(r.action==='decide'){const c=cards.find(x=>x.id===r.args.suggestion_id),ch=r.args.choice;
   if(ch==='complete')Object.assign(c,{status:'completed',closed_at:now});else if(ch==='reject')Object.assign(c,{status:'rejected',closed_at:now});
   else if(ch==='snooze')Object.assign(c,{status:'snoozed',snoozed_until:new Date(NOW+864e5).toISOString()});else Object.assign(c,{status:'pending',closed_at:null,snoozed_until:null});
   res.end(JSON.stringify({id:c.id,status:c.status,snoozed_until:c.snoozed_until}));return}
  res.end(JSON.stringify(r.action==='card_chat'?{session:true,status:'ok',active:false,cursor:'k1',items:[]}:{}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const open=async(width,height)=>{const mobile=width<600;reset();
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:process.env.SHOT_SCHEME||'light'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await context.clock.install({time:NOW});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.goto(base);await page.locator('#task-'+id(1)).waitFor();return {context,page}};
const decided=()=>actions.filter(a=>a.action==='decide').map(a=>[a.args.suggestion_id,a.args.choice]);
const shot=async(page,what)=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/${what}-${page.viewportSize().width}-${process.env.SHOT_SCHEME||'light'}.png`})};
const until=async(f,what)=>{for(let i=0;i<80;i++){if(await f())return;await new Promise(r=>setTimeout(r,60))}assert.fail('timed out: '+what)};
const items=page=>page.locator('.row-menu [role="menuitem"]').allInnerTexts();
const fits=async page=>{const b=await page.locator('.row-menu').boundingBox(),v=page.viewportSize();assert.ok(b.x>=0&&b.y>=0&&b.x+b.width<=v.width&&b.y+b.height<=v.height,'the menu fits on screen: '+JSON.stringify(b))};
// The to-do's own labels for the same choices, as its card draws them (hidden ones too)
const cardLabels=(page,n)=>page.evaluate(i=>{const out=[];for(const c of ['complete','snooze','reject']){const b=document.querySelector(`#task-${i} .actions [data-choice="${c}"]`);if(b)out.push((b.dataset.full||b.textContent).trim())}return out},id(n));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 {const {context,page}=await open(1440,900);
  const row=n=>page.locator(`#side-cards a[href="#chat=${id(n)}"]`);
  // A decision: Mark done (under its card's …), Snooze, Not needed
  await row(1).hover();await page.locator('.row-more').waitFor();await page.locator('.row-more').click();
  assert.deepEqual(await items(page),['Rename','Open','Mark done','Snooze','Not needed']);
  assert.deepEqual((await items(page)).slice(2),await cardLabels(page,1),'the same labels as the to-do');await fits(page);await shot(page,'menu');
  // Not needed: closes at once with the to-do's own message and Undo
  await page.locator('.row-menu [data-row-act="reject"]').click();await until(()=>decided().length===1,'not needed');
  assert.deepEqual(decided()[0],[id(1),'reject']);assert.equal(await page.locator('.row-menu').count(),0);
  await until(async()=>!(await row(1).isVisible()),'the row leaves');assert.match(await page.locator('#toast').textContent(),/^Marked not needed Undo$/);
  await page.locator('#toast [data-undo]').click();await until(()=>decided().length===2,'undo');assert.deepEqual(decided()[1],[id(1),'undo']);await row(1).waitFor();
  // Mark done on a ready one, from a right click
  await row(2).click({button:'right'});assert.deepEqual((await items(page)).slice(2),await cardLabels(page,2));
  await page.locator('.row-menu [data-row-act="complete"]').click();await until(()=>decided().length===3,'done');assert.deepEqual(decided()[2],[id(2),'complete']);
  assert.match(await page.locator('#toast').textContent(),/^Marked done Undo$/);
  // Snooze opens the to-do's own Snooze, its preset snoozes it
  await row(3).click({button:'right'});await page.locator('.row-menu [data-row-act="snooze"]').click();await page.locator('#snooze-dialog').waitFor();
  await page.locator('#snooze-dialog [data-snooze]').first().click();await until(()=>decided().length===4,'snooze');assert.deepEqual(decided()[3],[id(3),'snooze']);
  await until(async()=>/^Snoozed\. .* Undo\b/.test(await page.locator('#toast').textContent()),'the Snooze message with Undo, once it landed');
  // A done to-do: Rename and Open only
  await page.locator('[data-side-fold="done"]').click();await row(5).click({button:'right'});assert.deepEqual(await items(page),['Rename','Open']);await page.keyboard.press('Escape');
  // Keyboard: the menu key on a focused row opens it under the row, arrows move, Esc closes and the row keeps focus
  await row(4).focus();await page.keyboard.press('Shift+F10');await page.locator('.row-menu').waitFor();
  {const m=await page.locator('.row-menu').boundingBox(),r=await row(4).boundingBox();assert.ok(m.y>=r.y+r.height-1,'under the row')}
  assert.equal(await page.evaluate(()=>document.activeElement.dataset.rowRename!=null),true);
  await page.keyboard.press('End');assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Not needed');
  await page.keyboard.press('ArrowDown');assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Rename','wraps');
  await page.keyboard.press('ArrowUp');await page.keyboard.press('ArrowUp');assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Snooze');
  await page.keyboard.press('Escape');assert.equal(await page.locator('.row-menu').count(),0);
  assert.equal(await page.evaluate(()=>document.activeElement.getAttribute('href')),'#chat='+id(4),'focus back on the row');
  // Enter on Mark done: done, and the keyboard stays in the list (on the row after it, or before)
  // Opened again straight after Esc: the row's late refocus (after the list redraws) doesn't take focus from the menu
  await page.keyboard.press('Shift+F10');await page.waitForTimeout(300);
  assert.equal(await page.evaluate(()=>document.activeElement.dataset.rowRename!=null),true,'the menu keeps focus');
  await page.keyboard.press('ArrowDown');await page.keyboard.press('ArrowDown');
  assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Mark done');await page.keyboard.press('Enter');
  await until(()=>decided().length===5,'keyboard done');assert.deepEqual(decided()[4],[id(4),'complete']);
  await until(()=>page.evaluate(()=>!!document.activeElement.closest('#side-cards')),'focus in the list');
  await context.close()}
 // Phone: a long press opens the menu in the drawer; it fits the 390 px screen and its items take a tap
 {const {context,page}=await open(390,844);
  await page.locator('#drawer-open').tap();const link=page.locator(`#side-cards a[href="#chat=${id(3)}"]`);await link.waitFor();await page.waitForTimeout(500);
  const box=await link.boundingBox(),cdp=await context.newCDPSession(page),touch=(type,points)=>cdp.send('Input.dispatchTouchEvent',{type,touchPoints:points});
  // Low on the screen the menu opens over the finger: the tap that ends the press picks nothing
  await touch('touchStart',[{x:box.x+box.width-20,y:box.y+box.height/2}]);await page.waitForTimeout(650);await touch('touchEnd',[]);await page.locator('.row-menu').waitFor();
  await page.waitForTimeout(300);assert.equal(await page.locator('.row-menu').count(),1,'still open');assert.equal(await page.locator('.rename-box').count(),0);assert.deepEqual(decided(),[]);
  assert.deepEqual(await items(page),['Rename','Open','Mark done','Snooze','Not needed']);await fits(page);
  {const m=await page.locator('.row-menu').boundingBox();assert.ok(m.y+m.height<=box.y+1||m.y>=box.y+box.height-1,'the pressed row stays in sight')}
  for(const b of await page.locator('.row-menu [role="menuitem"]').all())assert.ok((await b.boundingBox()).height>=40,'a finger-sized row');
  await shot(page,'menu');
  await page.locator('.row-menu [data-row-act="reject"]').tap();await until(()=>decided().length===1,'phone not needed');assert.deepEqual(decided()[0],[id(3),'reject']);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'nothing wider than the screen');
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('sidebar row menu ok');
