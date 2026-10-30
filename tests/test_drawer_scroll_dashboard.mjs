import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');
// On a phone, opening the menu drawer leaves the page behind it exactly where it was: the same scroll position, the top
// bar and the page header still at the top (also scrolled down, on Suggestions, Calendar and a Graph page), and the same
// after it closes. The drawer's top takes the safe area (a notch, a camera cutout in the installed app) and no more: its
// ✕ sits where the menu button was.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const card=n=>({id:(n+'').padStart(2,'0').repeat(8),title:'Card number '+n,body:'Some text for card '+n+'.',status:n%3?'pending':'prepared',scope:n%2?'work':'personal',created_at:now,event_ids:[n+1]});
const cards=Array.from({length:30},(_,n)=>card(n));
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/graph'){const n=i=>({id:'person:'+i,kind:'person',name:'Person '+i,strength:2,last_at:now,signals:9,ids:[]});
  res.end(JSON.stringify({counts:{person:40,org:0,project:0},people:Array.from({length:40},(_,i)=>n(i)),quiet:[],new:[],projects:[],orgs:[],whos_who:[],waiting:0}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const still=page=>page.waitForFunction(()=>!document.getAnimations().some(a=>a.playState==='running'));
const where=page=>page.evaluate(()=>{const top=q=>{const e=document.querySelector(q);return e&&e.offsetParent?Math.round(e.getBoundingClientRect().top):null};
 return {y:Math.round(scrollY),bar:top('#topbar'),head:top('#page-head')}});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,inset] of [[390,844,0],[430,932,59]]){
  const context=await browser.newContext({viewport:{width,height},isMobile:true,hasTouch:true,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  // the installed app on a phone with a notch: the safe area at the top (where this Chromium can emulate it)
  let safe=0;if(inset){try{const cdp=await context.newCDPSession(page);await cdp.send('Emulation.setSafeAreaInsetsOverride',{insets:{top:inset,bottom:34,left:0,right:0}});safe=inset}catch{}}
  await page.goto(base);await page.locator('#task-'+cards[0].id).waitFor();
  for(const tab of ['inbox','calendar','people'])for(const y of [0,600]){
   const label=`${width}x${height} ${tab} at ${y}`;
   await page.evaluate(t=>showTab(t),tab);await page.waitForTimeout(150);
   await page.evaluate(y=>{const s=[...document.querySelectorAll('main>section')].find(x=>!x.hidden);
    if(!s.querySelector('.scroll-probe')){const d=document.createElement('div');d.className='scroll-probe';d.style.height='3000px';s.append(d)}scrollTo(0,y)},y);
   await page.waitForTimeout(100);
   const before=await where(page);assert.equal(before.y,y,'the page scrolls '+label);assert.equal(before.bar,0,'the top bar is at the top '+label);
   for(const close of ['scrim','escape']){
    await page.click('#drawer-open');await page.waitForFunction(()=>document.documentElement.dataset.drawer==='open');await still(page);
    assert.deepEqual(await where(page),before,'with the drawer open the page, its top bar and header stay put '+label);
    if(close==='scrim')await page.click('#drawer-scrim',{position:{x:width-16,y:height/2}});else await page.keyboard.press('Escape');
    await page.waitForFunction(()=>!document.documentElement.dataset.drawer);await still(page);
    assert.deepEqual(await where(page),before,'after the drawer closes ('+close+') everything is where it was '+label)}}
  // the drawer's top: the safe area plus the room that puts its ✕ on the menu button's spot
  await page.click('#drawer-open');await still(page);
  const d=await page.evaluate(()=>{const r=q=>document.querySelector(q).getBoundingClientRect();return {pad:parseFloat(getComputedStyle(document.querySelector('#app-side')).paddingTop),x:r('#side-toggle'),menu:r('#drawer-open')}});
  assert.equal(d.pad,safe+4,`the drawer's top is the safe area and no more (${width}, safe ${safe})`);
  assert.ok(Math.abs((d.x.top+d.x.bottom)/2-(d.menu.top+d.menu.bottom)/2)<=1,`the ✕ sits where the menu button was (${width}): `+JSON.stringify(d));
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('drawer scroll dashboard ok');
}finally{await browser?.close();server.close()}
