import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A custom property changed on <html> restyles every element of the page, so the ones the page keeps there change only
// when their value does: the visible part of the window (--vv-h, --vv-top) is set before the page's own script runs and
// isn't written again while it stays the same, and the usage-limit bar's height (--chat-banner-h) is only there while
// the bar sits over a chat on a phone.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[{id:'a1a1a1a1a1a1a1a1',title:'Check the payroll is ready',body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base=`http://127.0.0.1:${server.address().port}/`;
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 // Each write of a viewport or banner property on <html>, and whether the page's own script had started then
 await context.addInitScript(()=>{self.rootWrites=[];const seen={};new MutationObserver(()=>{const r=document.documentElement.style;
  for(const k of ['--vv-h','--vv-top','--chat-banner-h']){const v=r.getPropertyValue(k);if(v!==(seen[k]??'')){seen[k]=v;self.rootWrites.push({k,v,started:!!self.appStarted})}}})
  .observe(document,{subtree:true,attributes:true,attributeFilter:['style']})});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(base);
 await page.waitForFunction(()=>typeof drawnWhole!=='undefined'&&drawnWhole);
 const settle=()=>page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>r()))));
 await settle();
 const writes=()=>page.evaluate(()=>self.rootWrites);
 const first=await writes();
 assert.deepEqual(first.map(w=>[w.k,w.started]),[['--vv-h',false],['--vv-top',false]],`the viewport set once, before the page's script ${JSON.stringify(first)}`);
 assert.equal(first[0].v,'844px');
 // The same viewport again (a resize, a scroll of the visual viewport): nothing written
 const styled=()=>page.evaluate(()=>document.documentElement.getAttribute('style')||'');
 const before=await styled();
 await page.evaluate(()=>{dispatchEvent(new Event('resize'));visualViewport.dispatchEvent(new Event('resize'));visualViewport.dispatchEvent(new Event('scroll'));chatKeyboard()});await settle();
 assert.equal(await styled(),before,'the same viewport leaves <html> as it was');
 assert.equal((await writes()).length,2,'no write for the same viewport');
 // A smaller window: the new height, written once
 await page.setViewportSize({width:390,height:600});await page.waitForFunction(()=>document.documentElement.style.getPropertyValue('--vv-h')==='600px');
 await page.evaluate(()=>chatKeyboard());await settle();
 assert.deepEqual((await writes()).slice(2).map(w=>[w.k,w.v]),[['--vv-h','600px']],'one write for the new height');
 // The usage-limit bar: its height only while it sits over a chat, gone again after
 assert.equal(await page.evaluate(()=>document.documentElement.style.getPropertyValue('--chat-banner-h')),'','no bar, no height');
 await page.evaluate(id=>{history.replaceState(null,'','#chat='+id);openChatLink();$('#limit-banner').hidden=false;$('#limit-banner').textContent='Paused until 3 PM'},cards[0].id);
 await page.waitForFunction(()=>parseFloat(document.documentElement.style.getPropertyValue('--chat-banner-h'))>0);
 const h=await page.evaluate(()=>[document.documentElement.style.getPropertyValue('--chat-banner-h'),$('#banners').offsetHeight+'px']);
 assert.equal(h[0],h[1],'the bar\'s height');
 const n=(await writes()).length;
 await page.evaluate(()=>{$('#limit-banner').textContent='Paused until 3 PM.'});await settle();await settle();
 assert.equal((await writes()).length,n,'the same height again: nothing written');
 await page.evaluate(()=>{$('#limit-banner').hidden=true});
 await page.waitForFunction(()=>document.documentElement.style.getPropertyValue('--chat-banner-h')==='');
 await page.close();
 assert.deepEqual(errors,[]);
 console.log('ok: the page writes its properties on <html> only when they change');
}finally{await browser?.close();server.close()}
