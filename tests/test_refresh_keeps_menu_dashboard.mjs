import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The status poll (every 30 s) redraws the page. A ⋯ menu someone has open stays open and where it opened, with the
// item they are on still focused, also when the row it sits in changed and was drawn again: on a promise, a to-do,
// a Graph page and a routine. Before, a poll could close the menu under the pointer. SHOT_DIR=… saves shots.
const dashboard=await dashboardPage();
const day=n=>{const d=new Date();d.setDate(d.getDate()+n);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')};
const made=new Date(Date.now()-2*864e5).toISOString(),check=new Date(Date.now()+864e5).toISOString(),now=new Date(Date.now()-90e3).toISOString();
const promises=[
 {id:1,direction:'mine',who:'Alex Morgan',what:'send the Q3 deck',due:day(0),state:'open',made_at:made,check_at:check},
 {id:2,direction:'theirs',who:'Sam Lee',what:'send the signed contract',due:day(-1),state:'open',made_at:made,check_at:check},
 {id:3,direction:'theirs',who:'Kim',what:'get back about the pilot',due:null,state:'open',made_at:made,check_at:check}];
const CARD='a1a1a1a1a1a1a1a1';let cardTitle='Reply to Robin about the plan';
const card=()=>({id:CARD,title:cardTitle,body:'They asked for the numbers by Friday.',status:'pending',scope:'work',created_at:now,event_ids:[1]});
const status=()=>({suggestions:[card()],promises,connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},fleet:{on:false}});
const person={id:'email:rowan@example.com',kind:'person',name:'Rowan Hale',strength:2,closeness:'close',last_at:now,signals:4,ids:['rowan@example.com'],quiet:false,
 recent:[],around:[],open:{},links:[]};
const RT='d4'.repeat(16);let rtName='Shipped this week';
const routines=()=>({routines:[{id:RT,name:rtName,instructions:'Check what shipped and write a short post',rule:{unit:'week',n:1},anchor:day(3),at:'16:00',state:'on',next_due:day(3),
 runs:[{id:'r1',state:'ready',started_at:now,result:'Three things shipped.'}]}],suggested:[],trying:[]});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')?person:{projects:[],people:[person],quiet:[],new:[],orgs:[]}));return}
 if(url.pathname==='/api/routines'){res.end(JSON.stringify(routines()));return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOT_DIR;if(shots)await mkdir(shots,{recursive:true});
// What a menu shows now: open, where its list sits on the screen, and the item that has focus
const look=(page,sel)=>page.evaluate(sel=>{const d=document.querySelector(sel),l=d?.querySelector(':scope>[role=menu],:scope>[role=group],:scope>.fact-menu-list,:scope>.more-menu'),r=l?.getBoundingClientRect(),f=document.activeElement;
 return {open:!!d?.open,at:d?.open&&r?[Math.round(r.top),Math.round(r.left)]:null,focus:d&&d.contains(f)?(f.textContent||'').replace(/\s+/g,' ').trim().slice(0,40):null}},sel);
const poll=page=>page.evaluate(async()=>{graphLoadedAt=0;await refresh(true)});
// Open a menu and wait until the page has placed it: the placement (under its ⋯, or above it when there's no room
// under it) runs on the toggle event, a task of its own that can come after [open] is set and after the next steps
// here. Measured before it, a menu reads as under its ⋯ and then "moves" by itself. This listener comes after the
// page's own, so the menu has its place once it has seen the event.
const openMenu=async(page,sel)=>{
 await page.evaluate(()=>{window.__placed=null;window.__onToggle??=e=>{if(e.target.open)window.__placed=e.target};document.addEventListener('toggle',window.__onToggle,true)});
 await page.locator(sel+'>summary').click();await page.waitForFunction(sel=>{const d=document.querySelector(sel);return !!d?.open&&window.__placed===d},sel)};
const errors=[],results=[],lost=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]])for(const scheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const port=server.address().port,tag=`${width} ${scheme}`;
  // Each case: open the menu, put focus on an item, poll; change what the row shows, poll again (the row is drawn again,
  // except on a Graph page, which waits with its redraw while a menu is open). Then close it and change the row back:
  // focus stays on its ⋯ through that redraw too.
  const check=async(name,sel,row,open,change,back)=>{
   await openMenu(page,sel);
   await page.locator(sel).locator('button').nth(1).focus();
   const before=await look(page,sel);assert.ok(before.open&&before.focus,`${name} ${tag}: the menu is open with focus on an item`);
   await poll(page);await open?.();
   const kept=await look(page,sel);if(JSON.stringify(kept)!==JSON.stringify(before))lost.push(`${name} ${tag}: a poll closed or moved it ${JSON.stringify([before,kept])}`);
   if(row)await page.evaluate(row=>{window.__row=document.querySelector(row)},row);
   await change();await poll(page);await open?.();
   if(row)assert.equal(await page.evaluate(row=>document.querySelector(row)!==window.__row,row),true,`${name} ${tag}: the change draws its row again`);
   const redrawn=await look(page,sel);if(JSON.stringify(redrawn)!==JSON.stringify(before))lost.push(`${name} ${tag}: a poll that redrew its row closed or moved it ${JSON.stringify([before,redrawn])}`);
   if(shots)await page.screenshot({path:`${shots}/${name}-${width}-${scheme}.png`});
   await page.keyboard.press('Escape');await page.locator(sel+'>summary').focus();
   await back();await poll(page);await open?.();
   if(!await page.evaluate(sel=>document.activeElement===document.querySelector(sel+'>summary'),sel))lost.push(`${name} ${tag}: a poll that redrew its row took focus off its ⋯`);
   results.push([name,tag])};

  // Promises on the To-dos page: the last row's menu, which opens upward on a phone
  await page.goto(`http://127.0.0.1:${port}/`);await page.locator('#promises-list').waitFor();
  await page.locator('#promises-head').click();
  const last=page.locator('#promises-list .promise').last();await last.scrollIntoViewIfNeeded();
  const PROMISE='#promises-list>div.promise:last-of-type>details.promise-menu';
  await check('promise',PROMISE,'#promise-row-3',null,async()=>{promises[2]={...promises[2],due:day(2)}},async()=>{promises[2]={...promises[2],due:null}});
  // The page moved after the menu opened under its ⋯ and there's no room under it now: a poll that draws its row again
  // keeps it under its ⋯, where it opened. Before, the menu drawn again was placed anew and flipped above it.
  const side=()=>page.evaluate(sel=>{const d=document.querySelector(sel),s=d.querySelector(':scope>summary').getBoundingClientRect(),l=d.querySelector(':scope>.fact-menu-list').getBoundingClientRect();
   return {open:d.open,below:l.top>=s.bottom}},PROMISE);
  const room=await page.addStyleTag({content:'#promises-list{margin-bottom:100vh}'});
  await page.evaluate(sel=>scrollBy(0,document.querySelector(sel+'>summary').getBoundingClientRect().top-60),PROMISE);
  await openMenu(page,PROMISE);
  assert.deepEqual(await side(),{open:true,below:true},`promise ${tag}: with room under it, the menu opens under its ⋯`);
  await page.evaluate(sel=>scrollBy(0,document.querySelector(sel+'>summary').getBoundingClientRect().bottom-innerHeight+20),PROMISE);
  await page.evaluate(()=>{window.__row=document.querySelector('#promise-row-3')});
  promises[2]={...promises[2],due:day(2)};await poll(page);
  assert.equal(await page.evaluate(()=>document.querySelector('#promise-row-3')!==window.__row),true,`promise ${tag}: the change draws its row again`);
  const moved=await side();if(!moved.open||!moved.below)lost.push(`promise ${tag}: after the page moved, a poll that redrew its row flipped or closed it ${JSON.stringify(moved)}`);
  await page.keyboard.press('Escape');promises[2]={...promises[2],due:null};await poll(page);
  await room.evaluate(n=>n.remove());await page.evaluate(()=>scrollTo(0,0));

  // A to-do's More actions
  await page.locator(`#task-${CARD}`).scrollIntoViewIfNeeded();
  await check('todo',`#task-${CARD} details.more-actions`,`#task-${CARD}`,null,async()=>{cardTitle='Reply to Robin about the new plan'},async()=>{cardTitle='Reply to Robin about the plan'});

  // A Graph page's ⋯ (a person's More)
  await page.goto(`http://127.0.0.1:${port}/#graph/${encodeURIComponent(person.id)}`);await page.locator('#people-view .person-page details.person-menu').waitFor();
  await check('graph','#people-view details.person-menu',null,null,async()=>{person.signals++},async()=>{person.signals--});

  // A routine's More actions
  await page.goto(`http://127.0.0.1:${port}/#routines`);const rt=`[data-rt="${RT}"] details.more-actions`;await page.locator(rt).waitFor();
  await check('routine',rt,`[data-rt="${RT}"]`,()=>page.evaluate(()=>routinesView(true)),async()=>{rtName='Shipped this week, in short'},async()=>{rtName='Shipped this week'});
  await context.close();
 }
 assert.deepEqual(lost,[],'every menu stays open, in place, with its item focused, and focus stays on its ⋯');
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({kept:results.length}));
}finally{await browser?.close();server.close()}
