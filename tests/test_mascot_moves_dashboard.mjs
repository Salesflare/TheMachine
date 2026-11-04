import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The waving mascot while the Machine works (the first look, setting up) is alive: it blinks every few seconds and,
// every 15 to 30 seconds, does one small thing (a hop, a glance aside, a wave), never the same twice in a row, never
// mid-blink, with no layout shift. Nothing moves with reduced motion or in a hidden tab, and the sleeping All clear
// stays still. Made-up fixtures, nothing sent.
const dashboard=await dashboardPage();
let digging=true;
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
 reviews_on:true,greeting:{name:'Robin'},connectors:[{id:'work',display_name:'Work mail',service:'outlook'}],fleet:{on:false,fleets:[]},
 review_live:{runs:[],queue:null,first_look:null,first_dig:digging?{read:1,total:104,todos:0,goal:3,days:7,pace:6}:null}});
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(/^\/brand\/[\w.-]+\.(webp|png)$/.test(url.pathname)){try{const b=await readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url));
  res.setHeader('Content-Type','image/'+url.pathname.split('.').pop());res.end(b)}catch{res.statusCode=404;res.end()}return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/reviews/live'){res.end(JSON.stringify(state().review_live));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;const T0=Date.UTC(2026,10,4,9);
const open=async(opts={})=>{const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,
  reducedMotion:opts.still?'reduce':'no-preference',colorScheme:opts.light?'light':'dark'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.clock.install({time:T0});await page.clock.pauseAt(T0+1000);await page.goto(base);
 // The clock only moves in run(); every frame and move of the working mascot is logged with its time and size
 // (a redraw of the list puts a new one in its place: each has its own id; the size is its layout box, not a tilt)
 await page.evaluate(()=>{window.log=[];const ids=new WeakMap();new MutationObserver(ms=>{for(const m of ms){const el=m.target;if(!el.matches('#suggestions img.sticker'))continue;
  if(!ids.has(el))ids.set(el,ids.n=(ids.n|0)+1);const src=el.getAttribute('src').replace('brand/','');
  log.push({id:ids.get(el),at:performance.now(),src,cls:[...el.classList].filter(c=>c.startsWith('m-')).join(' '),w:el.offsetWidth,h:el.offsetHeight})}})
  .observe(document.body,{attributes:true,attributeFilter:['src','class'],subtree:true})});
 return {context,page}};
const run=async(page,ms)=>{for(let t=0;t<ms;t+=250)await page.clock.runFor(250);return page.evaluate(()=>log.splice(0))};
const kinds=log=>{const out=[];for(const e of log){const k=e.cls.includes('m-hop')?'hop':e.src==='wave-look.webp'?'look':e.src==='wave-hand.webp'?'wave':'';
 if(k&&out.at(-1)?.k!==k||k&&e.at-out.at(-1).at>2000)out.push({k,at:e.at})}return out};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 {const {context,page}=await open();
  await page.locator('#suggestions .first-look-empty img.sticker').waitFor();
  assert.match(await page.locator('#suggestions .first-look-empty').innerText(),/Taking a first look at your last 7 days/);
  const log=await run(page,125000);
  assert.ok(log.filter(e=>e.src==='wave-blink.webp').length>=8,'it blinks every few seconds');
  const moves=kinds(log);
  assert.ok(moves.length>=4&&moves.length<=9,'one small move every 15 to 30 seconds: '+moves.map(m=>m.k));
  for(let i=1;i<moves.length;i++){assert.notEqual(moves[i].k,moves[i-1].k,'never the same move twice in a row');
   const gap=moves[i].at-moves[i-1].at;assert.ok(gap>=14000&&gap<=34000,'15 to 30 seconds apart: '+gap)}
  assert.ok(moves[0].at<20000,'the first one comes soon after it shows');
  // Never a blink mid-move: the eyes close only from the open frame, and every move ends on it
  for(let i=1;i<log.length;i++)if(log[i].src==='wave-blink.webp'&&log[i-1].src!=='wave-blink.webp'&&log[i-1].id===log[i].id)assert.ok(log[i-1].src==='wave.webp'&&!log[i-1].cls&&!log[i].cls,'a blink starts from the still mascot, never mid-move');
  assert.equal(await page.locator('#suggestions img.sticker').getAttribute('src'),'brand/wave.webp');
  assert.equal(new Set(log.map(e=>e.w+'x'+e.h)).size,1,'no layout shift');
  // A hidden tab: nothing moves, and it comes back once the tab shows
  await page.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))});
  await run(page,1000);assert.equal((await run(page,40000)).length,0,'still in a hidden tab');
  await page.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});document.dispatchEvent(new Event('visibilitychange'))});
  assert.ok(kinds(await run(page,20000)).length>=1,'moves again once the tab shows');
  await context.close()}
 // Reduced motion: no blinks, no moves
 {const {context,page}=await open({still:true});
  await page.locator('#suggestions .first-look-empty img.sticker').waitFor();
  assert.equal((await run(page,70000)).length,0,'no motion with reduced motion');
  await context.close()}
 // The sleeping All clear is not a working state: it stays as it was
 {digging=false;const {context,page}=await open();
  await page.locator('#suggestions .all-clear img.sleepy').waitFor();
  assert.equal(await page.locator('#suggestions img[data-look]').count(),0,'the sleepy mascot has no moves');
  digging=true;await context.close()}
 assert.deepEqual(errors,[]);
 console.log('mascot moves dashboard ok');
}finally{await browser?.close();server.close()}
