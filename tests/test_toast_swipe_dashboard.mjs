import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A toast can be swiped away on a phone (touch) and dragged away with a mouse: sideways, or up when it sits at the top.
// Going that way is the same as timing out: no Undo is sent and the change stays. A short drag settles back and the toast
// stays; a tap on Undo still undoes. On a phone a swipe that starts on the toast doesn't open the drawer. With reduced
// motion it still goes. A plain toast ("Saved.") swipes away too, and takes only its own box. SHOTS=<dir>: mid-swipe and after, at 390 and 1440, light and dark. No network beyond this server.
const dashboard=await dashboardPage();
const shots=process.env.SHOTS||'';
const now=new Date().toISOString(),A='a1'.repeat(8);
const card={id:A,title:'Book the car service',body:'A made-up to-do.',status:'rejected',closed_at:now,scope:'personal',created_at:now,event_ids:[1]};
const status=()=>({suggestions:[card],promises:[],connectors:[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}],
 suggestion_counts:{pending:0},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],reminders:{}});
const decides=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');if(r.action==='decide'){decides.push(r.args.choice);if(r.args.choice==='undo')card.status='pending'}res.end(JSON.stringify({status:card.status,undone:true}));return}
 if(/^\/brand\/[\w.-]+\.(png|webp|woff2)$/.test(url.pathname)){try{const f=await readFile(new URL('..'+url.pathname,import.meta.url));res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':url.pathname.endsWith('.webp')?'image/webp':'font/woff2');res.end(f)}catch{res.statusCode=404;res.end()}return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const shown=page=>page.evaluate(()=>document.querySelector('#toast').classList.contains('show'));
const center=page=>page.evaluate(()=>{const r=document.querySelector('#toast').getBoundingClientRect();return {x:r.left+r.width*.3,y:r.top+r.height/2,top:r.top,left:r.left}});
const say=async(page,top=false)=>{await page.evaluate(([id,top])=>{toast('Marked not needed',false,id);const t=document.querySelector('#toast');if(top){t.style.top='70px';t.style.bottom='auto'}},[A,top]);
 await page.waitForFunction(()=>{const t=document.querySelector('#toast');return t.classList.contains('show')&&getComputedStyle(t).opacity==='1'})};
// A drag in steps, by touch (through the browser's touch input, as a phone sends it) or by mouse; held: stop before letting go
async function drag(page,cdp,from,dx,dy,{held=false,steps=8}={}){
 if(cdp){const pt=(x,y)=>[{x,y,id:1,radiusX:4,radiusY:4,force:1}];
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:pt(from.x,from.y)});
  for(let i=1;i<=steps;i++){await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:pt(from.x+dx*i/steps,from.y+dy*i/steps)});await page.waitForTimeout(16)}
  return async()=>cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]})}
 await page.mouse.move(from.x,from.y);await page.mouse.down();
 for(let i=1;i<=steps;i++){await page.mouse.move(from.x+dx*i/steps,from.y+dy*i/steps);await page.waitForTimeout(16)}
 return async()=>page.mouse.up()}
const go=async(page,cdp,dx,dy,o)=>{const end=await drag(page,cdp,await center(page),dx,dy,o);await end()};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,motion] of [[390,844,'no-preference'],[1440,900,'no-preference'],[390,844,'reduce']]){const phone=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:phone,hasTouch:phone,reducedMotion:motion,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  const cdp=phone?await context.newCDPSession(page):null,at=`${width} ${motion}`;
  await page.goto(base);await page.waitForFunction(()=>typeof toast==='function'&&document.querySelector('#toast'));
  // Swiped away sideways: gone, no Undo sent
  decides.length=0;await say(page);await go(page,cdp,-width*.4,0);
  await page.waitForFunction(()=>!document.querySelector('#toast').classList.contains('show'),null,{timeout:2000});
  await page.waitForTimeout(300);assert.deepEqual(decides,[],at+': a swipe sends no Undo');
  assert.equal(await page.evaluate(()=>document.querySelector('#toast').style.transform),'',at+': nothing left over after it went');
  if(phone)assert.notEqual(await page.evaluate(()=>document.documentElement.dataset.drawer),'open',at+': no drawer from a swipe on the toast');
  // To the right too
  await say(page);await go(page,cdp,width*.4,0);await page.waitForFunction(()=>!document.querySelector('#toast').classList.contains('show'),null,{timeout:2000});
  // At the top: up takes it away
  await say(page,true);await go(page,cdp,0,-60);await page.waitForFunction(()=>!document.querySelector('#toast').classList.contains('show'),null,{timeout:2000});
  // A short drag settles back and it stays, then times out as usual
  await say(page);const before=await center(page);await go(page,cdp,30,0,{steps:6});
  await page.waitForTimeout(400);assert.ok(await shown(page),at+': a short drag leaves it');
  const after=await center(page);assert.ok(Math.abs(after.left-before.left)<1,at+': back where it was');
  assert.deepEqual(decides,[],at+': a short drag sends no Undo');
  // A tap on Undo still undoes
  card.status='rejected';const b=await page.locator('#toast [data-undo]').boundingBox();
  if(phone)await page.touchscreen.tap(b.x+b.width/2,b.y+b.height/2);else await page.mouse.click(b.x+b.width/2,b.y+b.height/2);
  await page.waitForFunction(()=>!document.querySelector('#toast [data-undo]'),null,{timeout:5000});
  assert.deepEqual(decides,['undo'],at+': Undo still works');
  // Undo's own button, dragged far: a swipe, not a tap
  decides.length=0;await say(page);const u=await page.locator('#toast [data-undo]').boundingBox();
  await (await drag(page,cdp,{x:u.x+u.width/2,y:u.y+u.height/2},-width*.4,0))();
  await page.waitForFunction(()=>!document.querySelector('#toast').classList.contains('show'),null,{timeout:2000});await page.waitForTimeout(300);
  assert.deepEqual(decides,[],at+': a swipe that starts on Undo sends no Undo');
  // A plain toast (no button) swipes away too; a click just beside it still reaches the page
  await page.evaluate(()=>toast('Saved.'));await page.waitForFunction(()=>getComputedStyle(document.querySelector('#toast')).opacity==='1');
  assert.deepEqual(await page.locator('#toast').evaluate(t=>{const r=t.getBoundingClientRect(),y=r.top+r.height/2;return [t.contains(document.elementFromPoint(r.left-2,y)),t.contains(document.elementFromPoint(r.right+2,y))]}),[false,false],at+': beside a toast is the page');
  await go(page,cdp,width*.4,0);await page.waitForFunction(()=>!document.querySelector('#toast').classList.contains('show'),null,{timeout:2000});
  await context.close()}
 if(shots)for(const [width,height] of [[390,844],[1440,900]])for(const scheme of ['light','dark']){const phone=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:phone,hasTouch:phone,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage(),cdp=phone?await context.newCDPSession(page):null;
  await page.goto(base);await page.waitForFunction(()=>typeof toast==='function');await page.waitForTimeout(800);
  await say(page);await page.screenshot({path:`${shots}/toast-swipe-${width}-${scheme}-1-before.png`});
  const end=await drag(page,cdp,await center(page),-Math.min(110,width*.25),0);await page.screenshot({path:`${shots}/toast-swipe-${width}-${scheme}-2-mid.png`});
  await end();await page.waitForTimeout(400);await page.screenshot({path:`${shots}/toast-swipe-${width}-${scheme}-3-after.png`});
  if(phone&&scheme==='light'){await page.evaluate(()=>toast('Saved.'));await page.waitForFunction(()=>getComputedStyle(document.querySelector('#toast')).opacity==='1');
   const e2=await drag(page,cdp,await center(page),-45,0);await page.screenshot({path:`${shots}/toast-swipe-plain-${width}-${scheme}-mid.png`});await e2()}
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('toast swipe dashboard ok');
}finally{await browser?.close();server.close()}
