import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's body never repeats its title (todos-cards.js bodyAfterTitle, machine/text.py body_after_title): one the
// owner just made (New to-do) whose body is their words again shows none, also with other case, spacing or a final
// period; one whose first line is the title (Talk's title, then a note) shows only the note; a body that goes on in
// the same sentence, or under a title cut short (…), shows whole. Stored before the fix, they show clean too.
const dashboard=await dashboardPage();
const NOW=Date.parse('2026-10-22T10:30:00+02:00'),now=new Date(NOW).toISOString();
const id=n=>(n+'').padStart(2,'0').repeat(8);
const own={status:'pending',scope:'work',created_at:now,origin:'owner'};
const cards=[
 {...own,id:id(1),title:'Read the product review against the vision',body:'Read the product review against the vision',event_ids:[1]},
 {...own,id:id(2),title:'Call the plumber',body:'call the plumber.',event_ids:[2]},
 {...own,id:id(3),title:'Plan a trip to Antwerp',body:'Plan a trip to Antwerp\nA weekend in May, two nights.',event_ids:[3]},
 {...own,id:id(4),title:'Book the dentist',body:'Book the dentist before the end of the month',event_ids:[4]},
 {...own,id:id(5),title:'Write the long report about the quarter for the board and…',body:'Write the long report about the quarter for the board and the investors',event_ids:[5]},
 {id:id(6),title:'Send Sam the signed contract',body:'Sam asked on Monday.',status:'pending',scope:'work',created_at:now,event_ids:[6]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.clock.install({time:NOW});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto(base);await page.locator('#task-'+id(6)+' .body').waitFor();
  const body=n=>page.locator('#task-'+id(n)+' .body').evaluateAll(b=>b.map(x=>x.innerText.trim()));
  assert.deepEqual(await body(1),[],'a body that only repeats the title shows none');
  assert.deepEqual(await body(2),[],'other case and a final period still repeat it');
  assert.deepEqual(await body(3),['A weekend in May, two nights.'],'a first line that is the title: only the note');
  assert.deepEqual(await body(4),['Book the dentist before the end of the month'],'the same sentence going on shows whole');
  assert.deepEqual(await body(5),['Write the long report about the quarter for the board and the investors'],'a title cut short keeps the whole body');
  assert.deepEqual(await body(6),['Sam asked on Monday.']);
  for(const n of [1,2,3])assert.equal(await page.locator('#task-'+id(n)+' h3').innerText(),cards[n-1].title);
  if(process.env.SHOT_DIR){await page.locator('#task-'+id(1)).scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.SHOT_DIR}/after-${width}-${scheme}.png`})}
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
