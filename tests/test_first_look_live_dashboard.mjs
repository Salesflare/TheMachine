import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The live first look: while a new owner waits for their first to-dos, the robot says how far it read ("Read 20 of
// 284 emails. Reading the next 20…"), a few of the people and organizations it bumped into (first_dig.names, one more every few seconds),
// and the first to-do's title the moment it is saved, while it reads on. Names and a to-do title only, never a word of
// a message. Made-up fixtures, nothing sent. FIRST_LOOK_LIVE_SHOTS=<dir> also saves screenshots at 390 and 1440, light
// and dark: early, names-appearing, first-todo.
const dashboard=await dashboardPage(),shots=process.env.FIRST_LOOK_LIVE_SHOTS;
const now=new Date().toISOString();
const batch=(id,done=0)=>({run_id:id,status:'running',started_at:now,preview:0,auto:1,window_hours:168,planned:20,done_count:done,claimed_count:20,duration_seconds:0,account_ids:['work'],steps:[]});
const card={id:'c1',title:'Send Mila the signed pricing sheet',body:'Mila asked for the signed sheet before Friday.',status:'pending',event_ids:[1],scope:'work',created_at:now};
let run=null,dig=null,cards=[];
const live=()=>({runs:run?[run]:[],queue:null,first_look:null,first_dig:dig,cards:{count:cards.length,newest:cards.length?now:null}});
const state=()=>({suggestions:cards,promises:[],connectors:[{id:'work',display_name:'Work mail',service:'gmail'}],
 suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],reviews_on:true,greeting:{name:'Robin'},
 review_live:live(),first_look_done:null});
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
  const shot=async name=>{if(shots)await page.screenshot({path:`${shots}/${name}-${width}-${scheme}.png`})};
  run=batch('q'+width+scheme);dig={read:0,total:284,todos:0,goal:3,days:7,pace:1,unit:'email',names:[],first:null};cards=[];
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  const box=page.locator('#suggestions .first-look-empty');
  // Early: the batch it reads, in the robot's words, emails when every source is mail; no names yet
  await page.waitForFunction(()=>/^Reading the first 20 of 284 emails…$/.test(document.querySelector('#suggestions .fl-count')?.textContent||''),null,{timeout:8000});
  assert.equal(await box.locator('.fl-names').count(),0);
  await shot('early');
  // Names appearing: the first one at once, one more every few seconds, three at most
  run=batch('q'+width+scheme,0);dig={...dig,read:20,names:['Mila','Acme Freight','Jonah','Caspian']};
  await page.evaluate(async()=>{await refresh()});
  await box.locator('.fl-names').waitFor();
  assert.equal(await box.locator('.fl-names').innerText(),'Bumped into Mila so far.');
  await page.waitForFunction(()=>/Mila and Acme Freight/.test(document.querySelector('#suggestions .fl-names')?.textContent||''),null,{timeout:6000});
  if(shots)await page.evaluate(()=>{flNamesAt=Date.now()-1e4;firstLookTick()});else await page.waitForTimeout(4200);
  await page.waitForFunction(()=>document.querySelector('#suggestions .fl-names')?.textContent==='Bumped into Mila, Acme Freight, and Jonah so far.',null,{timeout:3000});
  assert.ok(!/Caspian/.test(await box.innerText()),'three names at most');
  assert.ok(!/All clear/.test(await page.locator('#page-head').innerText()));
  await shot('names');
  // The first to-do: its card shows at once, and the strip above it names it while it reads on
  cards=[card];dig={...dig,read:40,todos:1,first:{id:'c1',title:card.title}};run=batch('n'+width+scheme,0);
  await page.evaluate(async()=>{await refresh()});
  const strip=page.locator('#first-look');
  await strip.waitFor();
  assert.equal(await box.count(),0);
  const text=await strip.innerText();
  assert.match(text,/Taking a first look at your last 7 days/);
  assert.match(text,/Read 40 of 284 emails\. Reading the next 20…/);
  assert.ok(text.includes('First one’s in: Send Mila the signed pricing sheet. Still reading…'),text);
  assert.ok(text.includes('Bumped into Mila'),text);
  assert.ok(!text.includes(card.body),'never a word of a message');
  await shot('first-todo');
  // A second to-do: the count of them, no title
  dig={...dig,todos:2};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(()=>/Found 2 to-dos\. Reading on\./.test(document.querySelector('#first-look')?.textContent||''));
  // A source that is not mail: messages
  dig={...dig,unit:'message'};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(()=>/Read 40 of 284 messages\. Reading the next 20…/.test(document.querySelector('#first-look .fl-count')?.textContent||''));
  // Names that are no text never reach the page
  dig={...dig,names:[{x:1},'',null,'<b>Ann</b>']};
  await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(()=>/<b>Ann<\/b>/.test(document.querySelector('#first-look .fl-names')?.textContent||''));
  assert.equal(await strip.locator('b').count(),0);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
