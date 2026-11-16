import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A first load doesn't jump when the to-dos come in, on a phone and on a computer: while the loading outline shows, the
// head over the to-dos already has its place (shell-sidebar.css, .ph-wait), the outline starts right under it, as the
// list does, and the footer stays out of sight. So the list starts where it did, and the page has no layout shift
// (CLS) from the to-dos coming in.
// What stands over the list only for some owners keeps its place from the last load on that kind of screen
// (shell-main.html, skeleton-*): a new owner's hello in the head, the setup to-do (here its quiet line, with a step left),
// and the sidebar's New to-do (in the markup), Talk and Fleet. The second load of such a page doesn't move either.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),daysAgo=d=>new Date(Date.now()-d*864e5).toISOString();
const cards=Array.from({length:12},(_,i)=>({id:'e5e5e5e5e5e5e5'+String(i).padStart(2,'0'),title:'Answer the note '+i,body:'Drafted.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[10+i]}));
let extra={};
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]},...extra});
const KEPT={greeting:{name:'Sam'},setup_card:{since:daysAgo(3),mail_accounts:1,calendar:true,phones:0,more:false,memory:true,dismissed:[]},
 connectors:[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}],fleet:{on:true,fleets:[]},talk_ready:true};
let release=null,held=null;
const frames=page=>page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(r)))));  // what's drawn is painted
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){await held;res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/fleet'){res.end(JSON.stringify({on:true,fleets:[],cards:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname==='/sw.js'?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
// One load with the status held back until the outline is painted: where things are while loading and once drawn, and the shifts
async function load(page,width,height,isMobile,how){
 held=new Promise(r=>release=r);
 await page.evaluate(()=>{window.shifts=[]}).catch(()=>{});
 if(how==='reload')await page.reload();else await page.goto('http://127.0.0.1:'+server.address().port);
 await page.locator('#suggestions .skeleton').waitFor();await frames(page);
 const top=s=>page.evaluate(s=>{const e=document.querySelector(s);return e&&!e.hidden?Math.round(e.getBoundingClientRect().top):null},s);
 const loading={inbox:await top('#inbox'),line:await top('#suggestions .skeleton .sk-head'),footer:await top('.site-footer'),nav:await top('#app-side nav')};
 assert.equal(await page.locator('#page-head').isVisible(),false,width+': the head waits unseen for its first drawing');
 assert.ok(loading.footer>=height,width+': the footer is out of sight while loading: '+JSON.stringify(loading));
 // the to-dos in, then the rest drawn after the first paint (the Updated line comes with it) and laid out
 release();await page.locator('#suggestions article.card').first().waitFor();await page.waitForFunction(()=>/Updated/.test(document.querySelector('#updated')?.textContent||''));await frames(page);
 const drawn={inbox:await top('#inbox'),list:await top('#suggestions'),nav:await top('#app-side nav')};
 const shifts=await page.evaluate(()=>window.shifts),cls=shifts.reduce((a,s)=>a+s.value,0);
 return {loading,drawn,shifts,cls}}
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,isMobile] of [[390,844,true],[1440,900,false]]){
  const context=await browser.newContext({viewport:{width,height},isMobile,hasTouch:isMobile,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.addInitScript(()=>{window.shifts=[];new PerformanceObserver(l=>{for(const e of l.getEntries())window.shifts.push({value:e.value,at:Math.round(e.startTime),
   moved:e.sources.map(s=>(s.node?.id||s.node?.className||s.node?.nodeName||'?')+' '+Math.round(s.previousRect.y)+'->'+Math.round(s.currentRect.y))})}).observe({type:'layout-shift',buffered:true})});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  extra={};
  const plain=await load(page,width,height,isMobile);
  assert.ok(await page.locator('#page-head').isVisible()||isMobile,width+': the head is drawn');
  assert.ok(Math.abs(plain.drawn.inbox-plain.loading.inbox)<=1,width+': the list starts where it did: '+JSON.stringify(plain));
  assert.ok(plain.cls<0.01,width+': no layout shift from the to-dos coming in: '+JSON.stringify(plain.shifts));
  if(!isMobile)assert.equal(plain.drawn.nav,plain.loading.nav,width+': New to-do is in the sidebar from the first paint');
  // A new owner with a setup step left, Talk and the Fleet: the first load in this browser can't know them; the next one keeps their place
  extra=KEPT;
  await load(page,width,height,isMobile,'reload');
  assert.equal(await page.locator('#setup-card .setup-line').isVisible(),true,width+': the quiet setup line shows');
  assert.equal(await page.locator('#page-head.hello').isVisible(),true,width+': the hello shows');
  const kept=await load(page,width,height,isMobile,'reload');
  assert.ok(Math.abs(kept.drawn.list-kept.loading.line)<=1,width+': the list starts where its outline was: '+JSON.stringify(kept));
  assert.ok(kept.cls<0.01,width+': no layout shift on the next load either: '+JSON.stringify(kept.shifts));
  if(!isMobile){assert.equal(kept.drawn.nav,kept.loading.nav,width+': Talk keeps its place in the sidebar');
   assert.equal(await page.locator('#side-talk').isVisible(),true,width+': Talk shows');assert.equal(await page.locator('#tab-fleet').isVisible(),true,width+': the Fleet shows')}
  // and the setup line still opens the card (its click is wired on the page's own element)
  await page.locator('#setup-card [data-setup-open]').click();await page.locator('#setup-card .setup-row').first().waitFor();
  // Back to a plain owner: the kept places go with the next answer (the page draws as the Machine says)
  extra={};
  const after=await load(page,width,height,isMobile,'reload');
  assert.equal(await page.locator('#setup-card').isVisible(),false,width+': no setup to-do once nothing is left');
  assert.equal(await page.locator('#page-head.hello').count(),0,width+': no hello');
  const again=await load(page,width,height,isMobile,'reload');
  assert.ok(again.cls<0.01,width+': and the load after that is still: '+JSON.stringify(again.shifts));
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('first paint no shift dashboard: ok');
}finally{await browser?.close();server.close()}
