import assert from 'node:assert/strict';
import {OPENCLAW} from '../openclaw-root.mjs';
import {fixtureServer} from './click-speed.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A phone's first to-dos come in fast (vision: instant). While the page draws them, the part that keeps the reader's place
// (dashboard/shell-place.js) watches every change; asking the browser where the page is scrolled on each one made it lay out
// the half-drawn page again and again: 19 forced layouts, about 450 ms on a phone. At the very top it asks nothing until a
// scroll. This loads the made-up data (tests/click-speed-fixture.json) at 390x844 with the CPU 4x slower, records a trace
// up to the first painted to-do, and counts the style and layout work that shell-place's keeper forced in that time.
// Counted, not timed, so a busy test computer can't fail it.
const server=await fixtureServer();
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'en-US'});
 await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 await context.addInitScript(()=>{new MutationObserver((m,o)=>{if(document.querySelector('#suggestions article.card')){o.disconnect();
  requestAnimationFrame(()=>setTimeout(()=>{window.firstPainted=true}))}}).observe(document,{childList:true,subtree:true})});
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 const cdp=await context.newCDPSession(page);await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
 const events=[];cdp.on('Tracing.dataCollected',d=>events.push(...d.value));
 await cdp.send('Tracing.start',{categories:'devtools.timeline,disabled-by-default-devtools.timeline.stack',transferMode:'ReportEvents'});
 await page.goto(server.url);await page.waitForFunction(()=>window.firstPainted,null,{timeout:60000});
 const done=new Promise(r=>cdp.once('Tracing.tracingComplete',r));await cdp.send('Tracing.end');await done;
 // Style and layout a script asked for (it carries the script's stack), by the keeper's own functions
 const forced=events.filter(e=>e.ph==='X'&&['UpdateLayoutTree','Layout'].includes(e.name)).map(e=>(e.args?.beginData||e.args?.data||{}).stackTrace||[])
  .filter(stack=>stack.some(f=>['placeKeep','placeNote'].includes(f.functionName)));
 assert.ok(events.some(e=>e.name==='UpdateLayoutTree'),'the trace records style work');
 assert.ok(forced.length<=3,`the keeper forced ${forced.length} layouts while the first to-dos drew (at most 3)`);
 assert.deepEqual(errors,[]);
}finally{await browser?.close();await server.close()}
console.log('first draw layout dashboard ok');
