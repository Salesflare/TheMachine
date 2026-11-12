import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's buttons on a phone never leave the … alone on a line of its own (2026-11-04: a preparing to-do showed
// Mark done and Snooze side by side and a full-height … on a second row). Without a lead row, Mark done, Snooze and the
// … share one line; with one (Do it, Review and send…), the rest share the line under it. When that line has no room,
// Snooze tops the … instead. The … is as tall as the buttons beside it, never taller. Every state (preparing, prepared
// with and without a draft, not prepared yet, a step only the owner can do) at 320, 360, 390 and 430px, light and dark.
// SHOTS=<folder> saves each to-do at each size.
const dashboard=await dashboardPage();
const en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const now=new Date().toISOString(),ago=new Date(Date.now()-94000).toISOString();
const cards=[
 {id:'g1',title:'Find another venue for the December 13 birthday party',body:'The venue has no rooms available on December 13. Alternatives for 20 to 24 children, around 90 m² with a kitchenette.',
  status:'accepted',early:true,scope:'personal',created_at:now,event_ids:[1],preparation_status:'running',preparation_started_at:ago},
 {id:'g2',title:'Look up the train times for Saturday',body:'Checking the connections.',status:'accepted',scope:'work',created_at:now,event_ids:[2],preparation_status:'running',preparation_started_at:ago},
 {id:'p1',title:'Reply to Priya about the pricing for forty seats',body:'Priya asked what forty seats would cost per year.',status:'pending',scope:'work',created_at:now,event_ids:[3]},
 {id:'v1',title:'Pick up the parcel at the post office',body:'It waits there until Friday.',status:'pending',scope:'personal',owner_step:1,created_at:now,event_ids:[4]},
 {id:'r1',title:'Send Noor the contract',body:'Draft ready.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[5],
  next_actions:[{kind:'email',revision:'v1',label:'Send to Noor',to:['noor@example.com'],to_name:'Noor',subject:'Contract',body:'Hi Noor, the contract is attached.'}]},
 {id:'r2',title:'The summary of the board notes is ready',body:'Three decisions and two open questions.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[6]}];
const server=createServer(async(req,res)=>{for await(const c of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){readFile(new URL('../'+(url.pathname.startsWith('/brand/fonts/')?url.pathname.slice(1):'brand/app-icon-192.png'),import.meta.url)).then(b=>{res.setHeader('Content-Type',url.pathname.endsWith('.woff2')?'font/woff2':'image/png');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/en.json'){res.end(en);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]}}));return}
 if(url.pathname==='/api/progress'){res.end(JSON.stringify({status:'running',steps:[{title:'Working'}]}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['dark','light'])for(const width of [320,360,390,430]){
  const context=await browser.newContext({viewport:{width,height:844},colorScheme:scheme,isMobile:true,hasTouch:true});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-g1 .actions').waitFor();await page.evaluate(()=>document.fonts.ready);
  for(const {id} of cards){
   const at=`${id} at ${width}px ${scheme}`;
   // What is in sight in the row, the line each sits on (0 is the first), its height, and whether it stays inside the to-do
   const row=async()=>page.locator(`#task-${id} .actions`).evaluate(a=>{const card=a.closest('.card').getBoundingClientRect();
    const kids=[...a.children].filter(x=>x.matches('button,a.open,.more-actions')&&getComputedStyle(x).display!=='none');
    const tops=[...new Set(kids.map(x=>Math.round(x.getBoundingClientRect().top)))].sort((p,q)=>p-q);
    return kids.map(x=>{const r=x.getBoundingClientRect();return {name:x.tagName==='DETAILS'?'More':x.textContent.trim(),line:tops.indexOf(Math.round(r.top)),h:Math.round(r.height),inside:r.left>=card.left-0.5&&r.right<=card.right+0.5}})});
   let items=await row();
   for(let i=0;i<20&&items.some(x=>x.line>1);i++){await page.waitForTimeout(50);items=await row()}  // a row folds before its next paint
   const say=items.map(x=>`${x.name}@${x.line}:${x.h}`).join(' ');
   const lead=await page.locator(`#task-${id} .actions.two-rows`).count();
   assert.ok(items.every(x=>x.line<=(lead?1:0)),`${at}: the row runs onto another line: ${say}`);
   assert.ok(items.every(x=>x.inside),`${at}: a button sticks out of the to-do: ${say}`);
   const more=items.find(x=>x.name==='More');
   if(more){const beside=items.filter(x=>x!==more&&x.line===more.line);
    assert.ok(beside.length,`${at}: the … sits alone on its line: ${say}`);
    assert.ok(beside.every(x=>Math.abs(x.h-more.h)<=1),`${at}: the … is not as tall as the buttons beside it: ${say}`)}
   if(shots)await page.locator(`#task-${id}`).screenshot({path:`${shots}/row-${id}-${width}-${scheme}.png`});
  }
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`page wider than ${width}px`);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('card row phone dashboard ok');
