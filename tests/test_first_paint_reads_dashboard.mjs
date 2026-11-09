import assert from 'node:assert/strict';
import {OPENCLAW} from '../openclaw-root.mjs';
import {fixtureServer} from './click-speed.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A cold open draws the first to-do without reading the layout for things that can wait for its paint: the sidebar's
// scroll keeper reads nothing until the sidebar has scrolled (at its top there is nothing to keep), and the page's first
// focus lands on the first to-do just after a painted frame, not inside one (on a phone at 4x CPU these reads forced
// ~350 ms of layout before the first to-do showed). The keyboard still lands on the same to-do, and a scrolled sidebar
// still keeps its place (tests/test_no_jumps_dashboard.mjs). Made-up data (tests/click-speed-fixture.json), nothing sent.
const fixture=await fixtureServer(),errors=[];
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]]){
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await context.addInitScript(()=>{const w=window.__reads={side:0,focus:null};
   // scrollTop read on the sidebar's boxes before anything scrolled them
   const d=Object.getOwnPropertyDescriptor(Element.prototype,'scrollTop');
   Object.defineProperty(Element.prototype,'scrollTop',{configurable:true,get(){if(this.matches('#side-cards,.app-side'))w.side++;return d.get.call(this)},set(v){d.set.call(this,v)}});
   // whether the first focus on a to-do ran inside an animation frame's callbacks (before that frame's paint)
   const raf=window.requestAnimationFrame;let inFrame=0;
   window.requestAnimationFrame=cb=>raf.call(window,t=>{inFrame++;try{return cb(t)}finally{inFrame--}});
   const focus=HTMLElement.prototype.focus;
   HTMLElement.prototype.focus=function(o){if(!w.focus&&this.matches('#suggestions article.card'))w.focus={id:this.id,inFrame:inFrame>0};return focus.call(this,o)}});
  await page.goto(fixture.url);
  await page.locator('#suggestions article.card').first().waitFor();
  await page.waitForFunction(()=>window.__reads.focus&&document.querySelector('.kb-on'),null,{timeout:10000});
  const r=await page.evaluate(()=>({...window.__reads,first:document.querySelector('#suggestions article.card').id,on:document.querySelector('.kb-on').id,active:document.activeElement.id}));
  assert.equal(r.side,0,`${width}: the sidebar's scroll was read before it scrolled`);
  assert.equal(r.focus.inFrame,false,`${width}: the first focus ran inside a frame, before its paint`);
  assert.equal(r.on,r.first,`${width}: the keyboard lands on the first to-do`);assert.equal(r.active,r.first);
  // Scrolled, the keeper reads again: a redraw keeps the row in view where it was
  if(width===1440){await page.evaluate(()=>{const s=document.querySelector('.app-side');s.scrollTop=s.scrollHeight});await page.waitForTimeout(200);
   await page.evaluate(()=>{window.__reads.side=0;sideHTML='';sideCards()});
   assert.ok(await page.evaluate(()=>window.__reads.side)>0,'a scrolled sidebar is read again')}
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();await fixture.close()}
console.log('first paint reads dashboard ok');
