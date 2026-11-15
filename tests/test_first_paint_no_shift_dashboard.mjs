import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A first load doesn't jump when the to-dos come in, on a phone and on a computer: while the loading outline shows, the
// head over the to-dos already has its place (shell-sidebar.css, .ph-wait), the outline starts right under it, as the
// list does, and the footer stays out of sight. So the list starts where it did, and the page has no layout shift
// (CLS) from the to-dos coming in.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=Array.from({length:12},(_,i)=>({id:'e5e5e5e5e5e5e5'+String(i).padStart(2,'0'),title:'Answer the note '+i,body:'Drafted.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[10+i]}));
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]}});
let release=null,held=null;
const frames=page=>page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(r)))));  // what's drawn is painted
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){await held;res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname==='/sw.js'?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,isMobile] of [[390,844,true],[1440,900,false]]){
  const context=await browser.newContext({viewport:{width,height},isMobile,hasTouch:isMobile,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.addInitScript(()=>{window.shifts=[];new PerformanceObserver(l=>{for(const e of l.getEntries())window.shifts.push({value:e.value,at:Math.round(e.startTime),
   moved:e.sources.map(s=>(s.node?.id||s.node?.className||s.node?.nodeName||'?')+' '+Math.round(s.previousRect.y)+'->'+Math.round(s.currentRect.y))})}).observe({type:'layout-shift',buffered:true})});
  held=new Promise(r=>release=r);
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#suggestions .skeleton').waitFor();await frames(page);
  const top=s=>page.evaluate(s=>Math.round(document.querySelector(s).getBoundingClientRect().top),s);
  const loading={inbox:await top('#inbox'),line:await top('#suggestions .skeleton .sk-head'),footer:await top('.site-footer')};
  assert.equal(await page.locator('#page-head').isVisible(),false,width+': the head waits unseen for its first drawing');
  assert.ok(loading.footer>=height,width+': the footer is out of sight while loading: '+JSON.stringify(loading));
  // the to-dos in, then the rest drawn after the first paint (the Updated line comes with it) and laid out
  release();await page.locator('#suggestions article.card').first().waitFor();await page.waitForFunction(()=>/Updated/.test(document.querySelector('#updated')?.textContent||''));await frames(page);
  assert.ok(await page.locator('#page-head').isVisible()||isMobile,width+': the head is drawn');
  const drawn={inbox:await top('#inbox')};
  assert.ok(Math.abs(drawn.inbox-loading.inbox)<=1,width+': the list starts where it did: '+JSON.stringify({loading,drawn}));
  const shifts=await page.evaluate(()=>window.shifts),cls=shifts.reduce((a,s)=>a+s.value,0);
  assert.ok(cls<0.01,width+': no layout shift from the to-dos coming in: '+JSON.stringify(shifts));
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('first paint no shift dashboard: ok');
}finally{await browser?.close();server.close()}
