import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A phone scrolled down a board picks a stage with fewer projects: the page gets shorter than where the reader was, so it
// keeps its height a moment (placeKeep), then lets go and settles at its real bottom. Once settled it stays there: a mascot
// blink or a quiet refresh later never holds the height again, so the page doesn't jump up and back every few seconds.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const stages=[{name:'Reported'},{name:'Investigating'},{name:'Waiting on customer'},{name:'Resolved'},{name:'Stalled or declined',side:true}];
const counts=[5,2,16,30,2],projects=[];let n=0;
stages.forEach((s,k)=>{for(let j=0;j<counts[k];j++){n++;projects.push({id:'project:'+n,name:'Case '+n,stage:s.name,reason:'the export question is still open',by:'review',at:day(2),event_id:100+n,next:'Answer the remaining questions',days:2,no_reply_days:0,org:{name:'Org '+n,logo:null}})}});
const boards=[{id:1,name:'Support cases',stages,stuck:0,projects},{id:2,name:'Trials',stages,projects:projects.slice(0,3)}];
const suggest=[{id:3,name:'Onboarding',projects:[{id:'project:1',name:'Case 1'},{id:'project:2',name:'Case 2'}],reason:'Customers that move from setup to live.',stages:[{name:'Introduced'},{name:'Setup'},{name:'Live'}],visibility:'team'}];
const status={suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]}};
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({projects:[],people:[],quiet:[],new:[],orgs:[],boards,board_suggestions:suggest}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,colorScheme:'dark'});
 await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/');
 await page.evaluate(()=>{document.querySelector('nav [data-tab="people"]').click();document.querySelector('[data-graph-sub="projects"]').click()});
 await page.locator('.proj-board:not([hidden]) .board-head').waitFor();
 // A long stage, scrolled by the reader so the board's head sits under the top bar
 await page.locator('[data-stage-tab="Waiting on customer"]').tap();await page.waitForTimeout(200);
 const d=await page.evaluate(()=>document.querySelector('.proj-board .board-head').getBoundingClientRect().top-document.querySelector('.topbar').getBoundingClientRect().bottom-8);
 await page.mouse.move(200,600);await page.mouse.wheel(0,Math.round(d));await page.waitForTimeout(500);
 // A stage with two projects: the page is now shorter than where the reader was, and holds its height a moment
 await page.locator('[data-stage-tab="Investigating"]').tap();await page.waitForTimeout(100);
 const held=await page.evaluate(()=>({mh:document.body.style.minHeight,max:document.documentElement.scrollHeight-innerHeight}));
 assert.ok(held.mh,'a page made shorter keeps its height a moment');
 // The hold runs out (at most a few seconds) and the page settles at its real bottom
 await page.evaluate(()=>{place.holdEnd=Date.now();placeLetGo()});await page.waitForTimeout(300);
 const settled=await page.evaluate(()=>({y:scrollY,max:document.documentElement.scrollHeight-innerHeight,mh:document.body.style.minHeight}));
 assert.equal(settled.mh,'','the held height goes');assert.ok(settled.max<held.max,'the page is shorter once let go');
 // Then nothing holds it again: a mascot blink, a quiet board refresh, another blink
 await page.evaluate(()=>{window.holds=[];new MutationObserver(()=>{if(document.body.style.minHeight)holds.push(document.body.style.minHeight)}).observe(document.body,{attributes:true,attributeFilter:['style']});
  window.shifts=0;new PerformanceObserver(l=>{for(const e of l.getEntries())shifts+=e.value}).observe({type:'layout-shift'})});
 const blink=()=>page.evaluate(()=>{const m=document.querySelector('#topbar img');m.classList.add('blinking');m.setAttribute('src',m.getAttribute('src'));return new Promise(r=>setTimeout(()=>{m.classList.remove('blinking');r()},150))});
 await blink();await page.waitForTimeout(200);
 await page.evaluate(()=>people(graphNode,true));await page.waitForTimeout(200);
 await blink();await page.waitForTimeout(1800);
 const after=await page.evaluate(()=>({y:scrollY,holds,shifts}));
 assert.deepEqual(after.holds,[],'a blink or a refresh after the hold never holds the height again');
 assert.equal(Math.round(after.y),Math.round(settled.y),'the settled page stays where it is');
 assert.ok(after.shifts<0.001,`nothing on screen moves (CLS ${after.shifts})`);
 await context.close();
 assert.deepEqual(errors,[]);
 console.log('place hold dashboard ok');
}finally{await browser?.close();server.close()}
