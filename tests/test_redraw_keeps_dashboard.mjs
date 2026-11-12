import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The list redraws on every poll (every 30 s, and when the Fleet's asks come in). A redraw swaps only the to-dos whose
// data changed: the rest stay the same nodes, so a text selection, focus, an open menu, a button's in-flight state and
// the scroll survive it. A to-do under a pointer that's still down isn't swapped until it's let go, so the click lands.
const raw=await dashboardPage();
const now=new Date(Date.now()-90e3).toISOString(),ids=['a1a1a1a1a1a1a1a1','b2b2b2b2b2b2b2b2','c3c3c3c3c3c3c3c3'];
const titles={[ids[0]]:'Reply to Robin about the plan',[ids[1]]:'Send Kai the signed contract',[ids[2]]:'Book the venue for the offsite'};
const card=id=>({id,title:titles[id],body:'They asked for the numbers by Friday.',status:'pending',scope:'work',created_at:now,event_ids:[1]});
const status=()=>({suggestions:ids.map(card),promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(raw.replace('__CSRF__','c'.repeat(64)).replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__','s'.repeat(32)));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:'s'.repeat(32)}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:500},locale:'en-US',timezoneId:'Europe/Brussels'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/');
 for(const id of ids)await page.locator(`#task-${id}`).waitFor({timeout:8000});
 const [A,B,C]=ids.map(id=>`#task-${id}`);
 const mark=()=>page.evaluate(sel=>{window.__nodes=sel.map(s=>document.querySelector(s))},[A,B,C]);
 const same=()=>page.evaluate(sel=>sel.map((s,i)=>document.querySelector(s)===window.__nodes[i]),[A,B,C]);
 const redraw=()=>page.evaluate(async()=>{await refresh();render()});

 // 1. Nothing new: every to-do stays the same node, with the selection, focus, open menu, busy button and scroll
 await mark();
 await page.evaluate(([a,b])=>{const r=document.createRange();r.selectNodeContents(document.querySelector(b+' h3'));getSelection().removeAllRanges();getSelection().addRange(r);
  document.querySelector(a+' details.more-actions').open=true;const busy=document.querySelector(b+' .actions button');busy.disabled=true;busy.setAttribute('aria-busy','true');scrollTo(0,120)},[A,B]);
 const selected=await page.evaluate(()=>getSelection().toString());assert.equal(selected,titles[ids[1]],'the title is selected');
 const scrolled=await page.evaluate(()=>scrollY);assert.ok(scrolled>0,'the page scrolls at this height');
 await redraw();await redraw();
 assert.deepEqual(await same(),[true,true,true],'a redraw with nothing new keeps every to-do');
 assert.equal(await page.evaluate(()=>getSelection().toString()),selected,'the selection survives');
 assert.equal(await page.evaluate(()=>scrollY),scrolled,'the scroll stays');

 // 2. One to-do changed: only that one is swapped; the others keep their state
 titles[ids[2]]='Book the bigger venue for the offsite';await redraw();
 assert.deepEqual(await same(),[true,true,false],'only the changed to-do is swapped');
 assert.equal(await page.locator(C+' h3').innerText(),titles[ids[2]],'the changed to-do shows its new data');
 assert.equal(await page.evaluate(()=>getSelection().toString()),selected,'the selection in another to-do survives');
 assert.equal(await page.evaluate(a=>document.querySelector(a+' details.more-actions').open,A),true,'the open menu stays open');
 assert.equal(await page.evaluate(b=>document.querySelector(b+' [aria-busy="true"]')?.disabled,B),true,'the in-flight button stays in flight');
 assert.equal(await page.evaluate(()=>scrollY),scrolled,'the scroll stays');
 await page.evaluate(([a,b])=>{document.querySelector(a+' details.more-actions').open=false;const x=document.querySelector(b+' [aria-busy="true"]');x.disabled=false;x.removeAttribute('aria-busy');getSelection().removeAllRanges()},[A,B]);

 // 3. Focus stays on a button without an id (focusKept only finds fields by id)
 await page.evaluate(b=>document.querySelector(b+' .actions button').focus(),B);
 await redraw();
 assert.equal(await page.evaluate(b=>document.activeElement===document.querySelector(b+' .actions button'),B),true,'focus stays');

 // 4. A click that lands during a redraw: the pointer goes down on the menu, the to-do changes and redraws, the pointer
 //    comes up. The click lands, and the change shows right after.
 await mark();await page.evaluate(()=>scrollTo(0,0));
 const menu=page.locator(A+' details.more-actions > summary');const box=await menu.boundingBox();
 await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();
 titles[ids[0]]='Reply to Robin about the new plan';await redraw();
 assert.deepEqual(await same(),[true,true,true],'a to-do under a pressed pointer is not swapped');
 await page.mouse.up();
 await page.locator(A+' h3',{hasText:titles[ids[0]]}).waitFor({timeout:3000});
 assert.equal(await page.evaluate(a=>document.querySelector(a+' details.more-actions').open,A),true,'the click opened the menu');
 assert.equal(await page.evaluate(b=>document.querySelector(b)===window.__nodes[1],B),true,'the other to-dos stay');

 // 5. A text selection dragged during a redraw: the pointer is down in a to-do's text while it changes
 await page.locator(B+' .body p').scrollIntoViewIfNeeded();await mark();const h=await page.locator(B+' .body p').boundingBox();
 await page.mouse.move(h.x+2,h.y+h.height/2);await page.mouse.down();
 titles[ids[1]]='Send Kai the countersigned contract';await redraw();
 await page.mouse.move(h.x+120,h.y+h.height/2,{steps:4});
 assert.equal(await page.evaluate(b=>document.querySelector(b)===window.__nodes[1],B),true,'a to-do being selected in is not swapped');
 const dragged=await page.evaluate(()=>getSelection().toString());assert.ok(dragged.length>3,'the drag selects text');
 await page.mouse.up();
 await page.locator(B+' h3',{hasText:titles[ids[1]]}).waitFor({timeout:3000});
 assert.deepEqual(errors,[]);
 console.log('Redraw keeps: unchanged to-dos, selection, focus, open menu, busy button, scroll, and a click during a redraw passed.');
}finally{await browser?.close();server.close()}
