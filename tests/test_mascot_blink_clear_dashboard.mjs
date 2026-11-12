import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Every mascot with a closed-eyes frame blinks, also one that is drawn later or changes pose: the To-dos all-clear robot
// (a phone, dark theme) while a check runs ("Rummaging through the new stuff…", the waving pose glancing aside) blinks
// within about 10 seconds, again after the list is redrawn, and again after a pose swap (check over, then a new one). The
// sleepy pose has no frame (its eyes are shut already). The first look's end and the calendar's empty robot blink too. Not
// with reduced motion.
const dashboard=await dashboardPage();
const brand={'/brand/avatar.png':'brand/app-icon-192.png','/brand/avatar-blink.png':'brand/avatar-blink.png'};
for(const f of ['wave','wave-blink','wave-look','wave-hand','sleepy','sad','thinking'])brand[`/brand/${f}.webp`]=`brand/${f}.webp`;
const state={suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},
 check:{reviewing:true,reviewed:'2026-10-23T08:50:00Z'}};
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(brand[url.pathname]){res.setHeader('Content-Type',url.pathname.endsWith('.webp')?'image/webp':'image/png');res.end(await readFile(new URL('../'+brand[url.pathname],import.meta.url)));return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;const T0=Date.UTC(2026,9,23,9);
const ROBOT='#suggestions .all-clear img.sleepy';
const open=async(opts={})=>{const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,colorScheme:'dark',reducedMotion:opts.still?'reduce':'no-preference'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.clock.install({time:T0});await page.clock.pauseAt(T0+1000);await page.goto(base);await page.locator(ROBOT).waitFor();
 // Log every frame swap of an image in the to-dos list, with the (fake) time
 await page.evaluate(()=>{window.swaps=[];new MutationObserver(ms=>{for(const m of ms)if(m.target.closest('#suggestions,#more-robots'))swaps.push({el:m.target,src:m.target.getAttribute('src'),at:performance.now()})})
  .observe(document.body,{attributes:true,attributeFilter:['src'],subtree:true})});
 return {context,page}};
const run=async(page,ms)=>{for(let t=0;t<ms;t+=250)await page.clock.runFor(250);return page.evaluate(()=>swaps.splice(0).map(s=>({src:s.src,at:s.at,robot:s.el===document.querySelector('#suggestions .all-clear img.sleepy'),more:!!s.el.closest('#more-robots')})))};
// A blink: the closed-eyes frame, then the pose it had, about 150ms later
const blinks=(swaps,open,shut)=>{const n=[];for(let i=0;i+1<swaps.length;i++)if(swaps[i].robot&&swaps[i].src===shut&&swaps[i+1].src===open){
 const closed=swaps[i+1].at-swaps[i].at;assert.ok(closed>=120&&closed<=170,'eyes closed for about 150ms: '+closed);n.push(swaps[i])}return n};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 {const {context,page}=await open();
  assert.equal(await page.locator(ROBOT).getAttribute('src'),'brand/wave-look.webp','checking: the waving robot, glancing aside');
  assert.match(await page.locator('#suggestions .all-clear .poke-line').textContent(),/Rummaging|Snooping/);
  assert.ok(blinks(await run(page,10000),'brand/wave-look.webp','brand/wave-blink.webp').length>=1,'the all-clear robot blinks within 10 seconds');
  // A redraw puts a new robot in its place: that one blinks too. Like a real redraw it is drawn in its pose (clearPose),
  // never as a copy of the old one, which may be mid-blink (eyes shut, a frame with no blink of its own)
  await page.evaluate(()=>{const i=document.querySelector('#suggestions .all-clear img.sleepy'),n=i.cloneNode();n.classList.remove('blinking');n.setAttribute('src',clearPose());i.replaceWith(n)});
  await run(page,500);
  assert.ok(blinks(await run(page,10000),'brand/wave-look.webp','brand/wave-blink.webp').length>=1,'the redrawn robot blinks');
  // The check ends: sleepy (its eyes are shut already, no blink); a new check: the same robot blinks again
  await page.evaluate(()=>{state.check={reviewed:'2026-10-23T09:00:00Z'};checkDraw()});
  assert.equal(await page.locator(ROBOT).getAttribute('src'),'brand/sleepy.webp');
  assert.ok((await run(page,15000)).every(s=>!s.src.includes('blink')),'the sleepy robot does not blink');
  await page.evaluate(()=>{state.check={reviewing:true,reviewed:'2026-10-23T09:00:00Z'};checkDraw()});
  assert.ok(blinks(await run(page,10000),'brand/wave-look.webp','brand/wave-blink.webp').length>=1,'blinks again in its checking pose');
  // Poked awake: the plain waving pose blinks with the same frame
  await page.evaluate(()=>{const i=document.querySelector('#suggestions .all-clear img.sleepy');pokeAwake=true;i.src='brand/wave.webp'});
  assert.ok(blinks(await run(page,10000),'brand/wave.webp','brand/wave-blink.webp').length>=1,'the poked robot blinks');
  await context.close()}
 // Other robots with a closed-eyes frame: the first look's end and the calendar's empty state
 {const {context,page}=await open();
  // (on a layer of their own, so a status redraw doesn't take them away)
  await page.evaluate(()=>{const d=document.createElement('div');d.id='more-robots';d.style.cssText='position:fixed;top:120px;left:16px;z-index:9';
   d.innerHTML='<div class="empty all-clear first-look-end"><img class="sticker" src="brand/wave.webp" alt=""></div><div class="all-clear cal-clear"><img src="brand/avatar.png" alt="" width="64" height="64"></div>';document.body.append(d)});
  await run(page,250);
  const seen=new Set();for(let i=0;i<6&&seen.size<2;i++)for(const s of await run(page,10000))if(s.more&&s.src.includes('blink'))seen.add(s.src);
  assert.deepEqual([...seen].sort(),['brand/avatar-blink.png','brand/wave-blink.webp'],'both blink');
  await context.close()}
 // Reduced motion: never blinks
 {const {context,page}=await open({still:true});
  assert.equal((await run(page,30000)).filter(s=>s.src.includes('blink')).length,0,'no blinking with reduced motion');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('mascot blink clear dashboard ok');
}finally{await browser?.close();server.close()}
