import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The first look stops digging once it has its to-dos (first_look_done) while its last batch is still reading. That
// batch is no new count: 2026-11-09 a new owner saw "Reading 30 of 132 messages…" turn into "Reading 9 of 40 messages…"
// under "Read 14 emails and 6 meetings… found 3 to-dos". Now the strip goes and the ending's line says what it read. A
// review that starts after it stopped (a preview by hand) still shows its own count. Made-up fixtures, nothing sent.
// FIRST_LOOK_STOPS_SHOTS=<dir> also saves screenshots at 390 and 1440, light and dark.
const dashboard=await dashboardPage(),shots=process.env.FIRST_LOOK_STOPS_SHOTS;
const at=m=>new Date(Date.now()+m*6e4).toISOString();
const batch=(id,started)=>({run_id:id,status:'running',started_at:started,preview:0,auto:1,window_hours:null,promising:1,planned:40,done_count:0,claimed_count:40,duration_seconds:9,account_ids:['work'],steps:[]});
const card=(id,title)=>({id,title,body:'Made-up message.',status:'pending',event_ids:[1],scope:'work',created_at:at(-2)});
let run=null,dig=null,done=null,cards=[];
const live=()=>({runs:run?[run]:[],queue:null,first_look:null,first_dig:dig,cards:{count:cards.length,newest:cards.length?at(-1):null}});
const state=()=>({suggestions:cards,promises:[],connectors:[{id:'work',display_name:'Work mail',service:'gmail'},{id:'cal',display_name:'Calendar',service:'calendar'}],
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
  // Digging: two to-dos shown, one count over the week
  cards=[card('c1','Reply to Mila about the launch date'),card('c2','Check the parking payment')];
  run=batch('r'+width+scheme,at(-1));dig={read:30,total:132,todos:2,goal:3,days:7,pace:6,unit:'message',names:['Mila'],first:null};done=null;
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  const shot=async name=>{if(shots)await page.screenshot({path:`${shots}/${name}-${width}-${scheme}.png`})};
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  const strip=page.locator('#first-look');
  await page.waitForFunction(()=>/Reading \d+ of 132 messages…/.test(document.querySelector('#first-look .fl-count')?.textContent||''),null,{timeout:8000});
  await shot('digging');
  // The third to-do: it stopped digging, its last batch (started before that) still reads. No "of 40", no strip.
  cards=[...cards,card('c3','Book the birthday party')];dig=null;
  done={at:at(0),days:7,kinds:{email:14,meeting:6},read:{},todos:3,acted:false,next:[]};
  await page.evaluate(async()=>{await refresh()});
  await page.locator('#suggestions .first-look-note').waitFor();
  await page.waitForTimeout(1200);  // a tick of the count, were it still there
  assert.ok(await strip.isHidden(),'the strip goes once it stopped digging');
  const text=await page.locator('#inbox').innerText();
  assert.ok(!/of 40/.test(text),text);
  assert.ok(text.includes('Read 14 emails and 6 meetings from the past week and found 3 to-dos.'),text);
  await shot('stopped');
  // A review that starts after that is its own: it shows its count
  run={...batch('p'+width+scheme,at(1)),preview:1,auto:0,promising:0,planned:12,claimed_count:12};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(()=>/Reading \d+ of 12 messages…/.test(document.querySelector('#first-look .fl-count')?.textContent||''),null,{timeout:8000});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
