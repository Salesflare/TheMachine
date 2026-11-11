import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A tap on a folded text opens it, the same as its Show more: a to-do's text, a ready draft, and a long message in a
// to-do's chat (its More). An open text stays open on a tap (Show less folds it), a link in the text opens its link and
// nothing else, and a text selection or a drag opens nothing. Show more stays the keyboard's and screen reader's control.
// Checked at 1440 and 390 wide (a phone taps), light and dark. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const long=('They cannot come on the eleventh, and they ask when the painter can come instead. The painter already promised to confirm '+
 'another day; there is no replacement date yet, so the painting waits until they answer and the room stays as it is for now. ').repeat(3).trim();
const mail=(id,body)=>({kind:'email',revision:'r-'+id,label:'Send',to:['robin@example.invalid'],to_name:'Robin',subject:'Re: Painting',body});
const cards=[
 {id:'a1b2c3d4e5f60718',title:'Wait for the painting date',body:long,status:'pending',scope:'personal',created_at:now,event_ids:[1]},
 {id:'linkbody',title:'Ask about the other room',body:'See Wait for the painting date first. '+long,status:'pending',scope:'personal',created_at:now,event_ids:[2]},
 {id:'tapdraft',title:'Reply about the painting',body:'They asked for a new date.',status:'prepared',scope:'personal',created_at:now,event_ids:[3],next_actions:[mail('tapdraft',(long+'\n\n').repeat(3).trim())]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const items=[{kind:'source',at:now,from:'Robin',via:'email',text:long}];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'&&JSON.parse(body||'{}').action==='card_chat'){res.end(JSON.stringify({session:false,status:'ok',active:false,cursor:'k',items}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const look=(page,id)=>page.locator('#task-'+id).evaluate(c=>({more:[...c.querySelectorAll('button.more')].filter(b=>b.checkVisibility()).map(b=>b.textContent),
 folded:[...c.querySelectorAll('[data-clamp]')].some(e=>e.classList.contains('clamp')),cursor:getComputedStyle(c.querySelector('[data-clamp]')).cursor}));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){const mobile=width<600,why=`${width} ${scheme}`;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(why+': '+e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-tapdraft').waitFor();await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(200);
  // The card's own click handlers see the text's tap once at most: count what reaches the list
  await page.evaluate(()=>{window._listClicks=0;document.querySelector('#suggestions').addEventListener('click',()=>window._listClicks++)});
  const tap=async loc=>{await loc.scrollIntoViewIfNeeded();const b=await loc.boundingBox();const x=b.x+b.width/2,y=b.y+Math.min(b.height/2,12);mobile?await page.touchscreen.tap(x,y):await page.mouse.click(x,y)};
  const shot=async n=>{if(shots)await page.locator('#task-a1b2c3d4e5f60718').screenshot({path:`${shots}/tap-${n}-${width}-${scheme}.png`})};
  // Folded: Show more, the fade, and a pointer over the text
  assert.deepEqual(await look(page,'a1b2c3d4e5f60718'),{more:['Show more'],folded:true,cursor:'pointer'},why+': folded');
  await shot('collapsed');
  // A tap on the text opens it, as Show more does; the tap reaches nothing under it on its own
  await tap(page.locator('#task-a1b2c3d4e5f60718 .body'));
  assert.deepEqual(await look(page,'a1b2c3d4e5f60718'),{more:['Show less'],folded:false,cursor:'auto'},why+': a tap opens it');
  assert.equal(await page.evaluate(()=>window._listClicks),1,why+': the list sees only the Show more press');
  await shot('expanded');
  // A tap on the open text leaves it open; Show less still folds it
  await tap(page.locator('#task-a1b2c3d4e5f60718 .body'));
  assert.deepEqual(await look(page,'a1b2c3d4e5f60718'),{more:['Show less'],folded:false,cursor:'auto'},why+': an open text stays open');
  await page.locator('#task-a1b2c3d4e5f60718 button.more').click();
  assert.deepEqual(await look(page,'a1b2c3d4e5f60718'),{more:['Show more'],folded:true,cursor:'pointer'},why+': Show less folds it');
  // A selection over the folded text (a drag, or a long press to copy) opens nothing
  if(!mobile){const b=await page.locator('#task-a1b2c3d4e5f60718 .body').boundingBox();
   await page.mouse.move(b.x+4,b.y+6);await page.mouse.down();await page.mouse.move(b.x+b.width/2,b.y+8,{steps:6});await page.mouse.up();
   assert.ok(await page.evaluate(()=>!getSelection().isCollapsed),why+': text selected');
   assert.deepEqual(await look(page,'a1b2c3d4e5f60718'),{more:['Show more'],folded:true,cursor:'pointer'},why+': a drag opens nothing');
   await page.evaluate(()=>getSelection().removeAllRanges())}
  // A link in the folded text opens its link and leaves the text folded
  const link=page.locator('#task-linkbody .body a.card-link');assert.equal(await link.count(),1,why+': the text has a link');
  await page.evaluate(()=>{window._hashes=[];addEventListener('hashchange',()=>window._hashes.push(location.hash))});
  await tap(link);await page.waitForFunction(()=>window._hashes.length>0);
  assert.deepEqual(await look(page,'linkbody'),{more:['Show more'],folded:true,cursor:'pointer'},why+': a link tap opens nothing');
  // A ready draft opens on a tap too, with its summary
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-tapdraft .draft').waitFor();await page.waitForTimeout(200);
  assert.equal((await look(page,'tapdraft')).folded,true,why+': draft folded');
  await tap(page.locator('#task-tapdraft .draft .db'));
  assert.deepEqual((await look(page,'tapdraft')).more,['Show less'],why+': a tap opens the draft');
  assert.equal((await look(page,'tapdraft')).folded,false,why+': the draft is whole');
  // A long message in the to-do's chat opens on a tap, as its More does, and stays open on the next
  await page.goto('about:blank');await page.goto(`http://127.0.0.1:${server.address().port}/#chat=a1b2c3d4e5f60718`);const say=page.locator('#chat-log .chat-source .chat-clamp');await say.waitFor();
  assert.equal(await page.locator('#chat-log .chat-source .chat-more').innerText(),'More',why+': chat folded');
  assert.equal(await say.evaluate(e=>getComputedStyle(e).cursor),'pointer');
  await tap(say);await page.waitForFunction(()=>document.querySelector('#chat-log .chat-source .chat-more')?.textContent==='Less');
  await tap(page.locator('#chat-log .chat-source .chat-clamp'));await page.waitForTimeout(150);
  assert.equal(await page.locator('#chat-log .chat-source .chat-more').innerText(),'Less',why+': an open chat text stays open');
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
