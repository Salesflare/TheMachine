import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Do it, Ask for changes and the other choices on a to-do (saveDecision): the toast shows as
// soon as the Machine answers the choice, not after the whole status that follows it (a slow /api/status here). A choice
// the Machine refuses changes nothing on the card, keeps the typed note's editor open and says why at once.
const raw=await dashboardPage(process.env.DASHBOARD_PAGE||undefined);
const CSRF='c'.repeat(64),SCOPE='a1'.repeat(16),iso=new Date().toISOString(),A='1'.repeat(16),B='2'.repeat(16);
const card=(id,title)=>({id,title,body:'Robin asked for the numbers.',status:'pending',scope:'work',created_at:iso,event_ids:[1]});
let cards=[card(A,'Reply to Robin about the plan'),card(B,'Book the venue')],statusDelay=0,refuse=false;
const STATUS_MS=+(process.env.STATUS_MS||1500);
const page=()=>raw.replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__',SCOPE);
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page());return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:CSRF,cache_scope:SCOPE}));return}
 if(url.pathname==='/api/status'){const out=JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_runs:[],connectors:[],fleet:{on:false},ui_version:'v1'});
  if(statusDelay)await new Promise(r=>setTimeout(r,statusDelay));res.end(out);return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  if(r.action==='decide'){if(refuse){res.statusCode=400;res.end(JSON.stringify({error:'That to-do changed. Use its current buttons.'}));return}
   const status={accept:'accepted',other:'pending'}[r.args.choice]||'pending';
   cards=cards.map(c=>c.id===r.args.suggestion_id?{...c,status}:c);res.end(JSON.stringify({status,snoozed_until:null}));return}
  res.end('{"ok":true}');return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
// Starts the choice and measures until the toast shows (ms), with the card's status and the toast's text at that moment
const choose=(tab,id,choice,feedback='')=>tab.evaluate(async([id,choice,feedback])=>{const toastEl=document.querySelector('#toast');toastEl.classList.remove('show');toastEl.textContent='';
 const t0=performance.now();let failed='';const going=saveDecision(id,choice,feedback).catch(e=>{failed=e.message;toast(e.message,true)});
 while(!toastEl.classList.contains('show')&&performance.now()-t0<10000)await new Promise(r=>requestAnimationFrame(r));
 const out={ms:Math.round(performance.now()-t0),text:toastEl.textContent.trim(),status:state.suggestions.find(x=>x.id===id)?.status,changing:changing.has(id)};
 await going;return {...out,failed}},[id,choice,feedback]);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const tab=await context.newPage();tab.on('pageerror',e=>errors.push(e.message));
 await tab.goto(base);await tab.locator('#suggestions article[id]').first().waitFor();
 statusDelay=STATUS_MS;

 // 1. Do it: the toast shows with the answer, while the status is still on its way; the to-do follows with it
 const done=await choose(tab,A,'accept');
 if(process.env.TIMINGS)console.log('accept toast ms',done.ms);
 assert.equal(done.text,'I’ll prepare it.');
 assert.ok(done.ms<STATUS_MS/2,`the toast came after ${done.ms} ms, not before the slow status (${STATUS_MS} ms)`);
 await tab.waitForFunction(id=>state.suggestions.find(x=>x.id===id)?.status==='accepted'&&!document.querySelector('#toast.show.error'),A);

 // 2. Ask for changes: the editor closes and the toast says so, before the status
 await tab.evaluate(id=>{changing.add(id);render()},B);
 const asked=await choose(tab,B,'other','Use the March numbers');
 if(process.env.TIMINGS)console.log('change toast ms',asked.ms);
 assert.equal(asked.text,'Changes saved.');assert.equal(asked.changing,false);
 assert.ok(asked.ms<STATUS_MS/2,`the toast came after ${asked.ms} ms`);

 // 3. Refused: nothing changes on the card, the editor stays open with the note, and the reason shows at once
 await tab.waitForTimeout(STATUS_MS+300);  // the background status from step 2 is in
 refuse=true;await tab.evaluate(id=>{changing.add(id);render()},B);
 const no=await choose(tab,B,'accept');
 assert.equal(no.failed,'That to-do changed. Use its current buttons.');
 assert.match(no.text,/^That to-do changed\. Use its current buttons\./);  // an error toast also offers Report a bug
 assert.equal(no.status,'pending','a refused choice changes nothing on the card');
 assert.equal(no.changing,true,'the editor stays open');
 assert.ok(no.ms<STATUS_MS/2,`the reason came after ${no.ms} ms`);

 assert.deepEqual(errors,[]);
 console.log('decide toast dashboard ok');
}finally{await browser?.close();server.close()}
