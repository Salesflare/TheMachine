import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The first look's line while a batch is being read. A batch saves what it read at its end (2026-11-09: the first 20
// took 98 s), so in between the line used to count a guess, a signal every few seconds ("Reading 11 of 132" with
// nothing read yet, over a sliver of a bar that looked stuck). Now the number is what its batches saved, the line names
// the batch in hand ("Reading the first 20 of 132 messages…", then "Read 20 of 132 messages. Reading the next 40…"),
// and only the bar moves with the time the batch has taken: from its first seconds, never back, never ahead in the
// number, never full before the work is done. The ending says the real count. Made-up fixtures, nothing sent.
// FIRST_LOOK_READING_SHOTS=<dir> also saves screenshots at 390 and 1440, light and dark: early and midway in a batch.
const dashboard=await dashboardPage(),shots=process.env.FIRST_LOOK_READING_SHOTS;
const at=m=>new Date(Date.now()+m*6e4).toISOString();
const batch=(id,planned,more={})=>({run_id:id,status:'running',started_at:at(0),preview:0,auto:1,window_hours:168,promising:1,planned,done_count:0,claimed_count:planned,duration_seconds:0,account_ids:['work'],steps:[],...more});
const card=(id,title)=>({id,title,body:'Made-up message.',status:'pending',event_ids:[1],scope:'work',created_at:at(-1)});
let run=null,dig=null,done=null,cards=[];
const live=()=>({runs:run?[run]:[],queue:null,first_look:null,first_dig:dig,first_eta:cards.length?null:2,cards:{count:cards.length,newest:cards.length?at(-1):null}});
const state=()=>({suggestions:cards,promises:[],connectors:[{id:'work',display_name:'Work mail',service:'gmail'},{id:'chat',display_name:'Team chat',service:'slack'}],
 suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],reviews_on:true,greeting:{name:'Robin'},
 review_live:live(),first_look_done:done});
const errors=[];
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/reviews/live'){res.end(JSON.stringify(live()));return}
 if(shots&&/^\/brand\/[\w.-]+\.(webp|png)$/.test(url.pathname)){readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url)).then(b=>{res.setHeader('Content-Type','image/'+url.pathname.split('.').pop());res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const sizes=shots?[[390,844],[1440,900]]:[[390,844]],schemes=shots?['light','dark']:['dark'];
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of sizes)for(const scheme of schemes){
  const id=n=>n+width+scheme;
  // The first batch, just started: 20 of the week's 132 are with the model, none read yet
  cards=[];done=null;run=batch(id('a'),20);dig={read:0,total:132,todos:0,goal:3,days:7,pace:1,unit:'message',names:[],first:null};
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  const shot=async name=>{if(shots)await page.screenshot({path:`${shots}/${name}-${width}-${scheme}.png`})};
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  // What the page shows: the line, the bar's width in percent, the value it gives for what was read, and whether it sweeps
  const seen=box=>page.evaluate(sel=>{const b=document.querySelector(sel+' .fl-bar');return{text:document.querySelector(sel+' .fl-count')?.textContent||'',
   width:parseFloat(b?.firstChild.style.width)||0,px:b?.firstChild.getBoundingClientRect().width||0,now:+b?.getAttribute('aria-valuenow'),on:!!b?.classList.contains('fl-on')}},box);
  const empty='#suggestions .first-look-empty',strip='#first-look';
  await page.locator(empty+' .fl-count').waitFor();
  const first=await seen(empty);
  assert.equal(first.text,'Reading the first 20 of 132 messages…');
  assert.ok(first.on&&first.px>=5,'at work from its first second: the track sweeps and the bar shows');
  assert.equal(first.now,0);
  // Within the batch the bar moves, a second at a time and never back; the line stays what is true
  const widths=[first.width];
  for(let n=0;n<10;n++){await page.waitForTimeout(500);const s=await seen(empty);widths.push(s.width);
   assert.equal(s.text,'Reading the first 20 of 132 messages…');assert.equal(s.now,0,'nothing read yet: no number runs ahead')}
  assert.ok(widths.every((w,n)=>!n||w>=widths[n-1]),'never back: '+widths);
  assert.ok(widths.at(-1)>widths[0],'it moves within the first batch: '+widths);
  // A batch that takes longer than the earlier ones: the bar waits one short of the batch, never at the total
  run={...run,duration_seconds:600};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(sel=>parseFloat(document.querySelector(sel+' .fl-bar i')?.style.width)>=14,empty);
  const late=await seen(empty);
  assert.deepEqual([late.text,late.width,late.now],['Reading the first 20 of 132 messages…',Math.round(100*19/132),0]);
  // It saved: 20 read, two to-dos, and the next 40 are with the model
  cards=[card('c1','Reply to Mila about the launch date'),card('c2','Check the parking payment')];
  run=batch(id('b'),40);dig={...dig,read:20,todos:2,names:['Mila']};
  await page.evaluate(async()=>{await refresh()});
  await page.locator(strip+' .fl-count').waitFor();
  const next=await seen(strip);
  assert.equal(next.text,'Read 20 of 132 messages. Reading the next 40…');
  assert.equal(next.now,20);
  assert.ok(next.on&&next.width>=late.width,'never back as a batch saves');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'the longer line fits the page');
  // A look that comes back with an older count (a copy from before the batch saved): the line and the bar stay
  dig={...dig,read:0};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForTimeout(1100);
  const stale=await seen(strip);
  assert.equal(stale.text,'Read 20 of 132 messages. Reading the next 40…');
  assert.ok(stale.width>=next.width);
  // Between two batches: what was read, and no sweep while nothing is with the model
  run=null;dig={...dig,read:60};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(sel=>document.querySelector(sel+' .fl-count')?.textContent==='Reading 60 of 132 messages…',strip);
  const between=await seen(strip);
  assert.deepEqual([between.now,between.on,between.width],[60,false,Math.round(100*60/132)]);
  // The last batch, part of it saved: its rest is what it reads next
  run=batch(id('c'),40,{done_count:10});dig={...dig,read:70};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(sel=>document.querySelector(sel+' .fl-count')?.textContent==='Read 70 of 132 messages. Reading the next 30…',strip);
  // The ending: the strip goes and the line says the real count, whatever the bar had reached
  cards=[...cards,card('c3','Book the birthday party')];run=null;dig=null;
  done={at:at(0),days:7,kinds:{email:61,message:19,meeting:4},read:{},todos:3,acted:false,next:[]};
  await page.evaluate(async()=>{await refresh()});
  await page.locator('#suggestions .first-look-note').waitFor();
  assert.ok(await page.locator(strip).isHidden());
  const ending=(await page.locator('#suggestions .first-look-note').innerText()).replaceAll(' ',' ');
  assert.equal(ending,'Read 61 emails, 4 meetings, and 19 messages from the past week and found 3 to-dos. See what I’ve learned');
  // Every way the line reads: emails when every source is mail, one batch that is the whole week, a single message
  const lines=await page.evaluate(()=>[{read:0,done:0,batch:20,total:284,unit:'email'},{read:20,done:25,batch:40,total:284,unit:'email'},{read:60,done:60,batch:0,total:284,unit:'email'},
   {read:0,done:3,batch:12,total:12},{read:0,done:0,batch:1,total:1,unit:'email'},{read:0,done:0,batch:0,total:1320},{done:3,total:8},{read:9,done:3,batch:50,total:8}].map(flCount));
  assert.deepEqual(lines,['Reading the first 20 of 284 emails…','Read 20 of 284 emails. Reading the next 40…','Reading 60 of 284 emails…',
   'Reading 12 messages…','Reading 1 email…','Reading 1,320 messages…','Reading 3 of 8 messages…','Read 3 of 8 messages. Reading the next 5…']);
  if(shots){
   // Early in the first batch (a few seconds in) and midway (half of what the batch is expected to take), no to-dos yet
   cards=[];done=null;run=batch(id('s1'),20,{duration_seconds:8});dig={read:0,total:132,todos:0,goal:3,days:7,pace:6,unit:'message',names:[],first:null};
   await page.evaluate(async()=>{flPeak=flRead=flTotal=0;await refresh()});
   await page.locator(empty+' .fl-count').waitFor();await page.waitForTimeout(600);await shot('early-first');
   run=batch(id('s2'),20,{duration_seconds:62});dig={...dig,names:['Mila','Acme Freight']};
   await page.evaluate(async()=>{flNamesAt=Date.now()-1e4;await refresh()});
   await page.waitForTimeout(600);await shot('midway-first');
   // The same in the second batch, with the first to-dos on the page
   cards=[card('c1','Reply to Mila about the launch date'),card('c2','Check the parking payment')];
   run=batch(id('s3'),40,{duration_seconds:8});dig={...dig,read:20,todos:2,pace:3};
   await page.evaluate(async()=>{await refresh()});
   await page.locator(strip+' .fl-count').waitFor();await page.waitForTimeout(600);await shot('early-next');
   run=batch(id('s4'),40,{duration_seconds:62});
   await page.evaluate(async()=>{await refresh()});
   await page.waitForTimeout(600);await shot('midway-next');
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
