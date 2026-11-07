import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
import {settled} from './page-calls.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Ask from search (search_ask.py) in the palette, on made-up data: the usual results show at once; a question gets a
// short answer above them that comes in a few words at a time, with its messages as rows that open the message;
// keywords get nothing; it asks for the area in view; a failure says so in one line; without a model it stops asking.
// SEARCH_ASK_SHOTS=dir saves shots at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const now=new Date(),ago=d=>new Date(now-d*864e5).toISOString();
const id=n=>(n+'').padStart(2,'0').repeat(8);
const MSGS=[
 {id:41,account_id:'work',kind:'gmail.message',title:'Pilot timing',occurred_at:ago(2),body:'The pilot moves to March.',metadata:{from:'Kim Vale <kim@initech.example>'}},
 {id:42,account_id:'work',kind:'slack.message',title:'#pilot',occurred_at:ago(1),body:'Budget stays as it is.',metadata:{channel_name:'pilot',sender_display:'Lee Park'}}];
const ANSWER='Kim said the pilot moves to March, and Lee confirmed the budget stays the same. Nothing changes for the kickoff on the 4th.';
let asks,mode,release;
const reset=()=>{asks=[];mode='answer';release=null};reset();
const state=()=>({suggestions:[{id:id(1),title:'Send Kim the pilot plan',body:'',status:'pending',scope:'work',created_at:ago(0),event_ids:[41]}],promises:[],suggestion_counts:{},
 decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.has('q')?{found:[]}:{counts:{}}));return}
 if(url.pathname==='/api/events'){res.end(JSON.stringify(MSGS));return}
 if(url.pathname==='/api/originals'){const m=MSGS.find(x=>String(x.id)===url.searchParams.get('event'));
  res.end(JSON.stringify({originals:m?[{event_id:m.id,kind:'email',from:m.metadata.from,occurred_at:m.occurred_at,subject:m.title,body:m.body}]:[]}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  if(r.action==='search_ask'){asks.push(r.args);
   if(release)await release;
   const q=r.args.query;
   res.end(JSON.stringify(mode==='off'?{off:true}:mode==='error'?{error:true}:/^(what|did|how|wat)\b/i.test(q)?{answer:ANSWER,sources:[
    {id:41,kind:'gmail.message',title:'Pilot timing',from:'Kim Vale',at:MSGS[0].occurred_at},{id:42,kind:'slack.message',title:'#pilot',from:'Lee Park',at:MSGS[1].occurred_at}]}:{none:true}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.SEARCH_ASK_SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const open=async(width,height,colorScheme='light')=>{const mobile=width<600;reset();
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels',colorScheme});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.goto(base);await page.locator('#task-'+id(1)).waitFor();return {context,page}};
const groups=page=>page.locator('#pal-list .pal-group').allTextContents();
const labels=page=>page.locator('#pal-list .pal-item .pal-label').allTextContents();
const palOpenNow=async(page,width)=>{if(width<600)await page.locator('#find-open').click();else await page.keyboard.press('Control+k');await page.locator('#palette').waitFor()};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // The flow, once at desktop size
 {const {context,page}=await open(1440,900);
  await palOpenNow(page,1440);
  // Keywords: the results at once; asked, nothing back, nothing shown
  await page.keyboard.type('pilot march kickoff');
  await page.locator('#pal-list .pal-group',{hasText:'Messages'}).waitFor();
  await settled(()=>asks.length===1,true,'keywords are asked once typing rests');
  await page.evaluate(()=>new Promise(r=>setTimeout(r,50)));
  assert.ok(!(await groups(page)).includes('Answer'),'no answer for keywords');
  // A question: the results first, Looking… (it ends in ?), then the answer above them, a few words at a time
  let go;release=new Promise(r=>go=r);
  await page.locator('#pal-q').fill('what did kim say about the pilot?');
  await page.locator('#pal-list .pal-group',{hasText:'Messages'}).waitFor();
  await page.locator('#pal-answer',{hasText:'Looking…'}).waitFor();
  assert.equal((await groups(page))[0],'Answer');
  assert.ok((await labels(page)).length>0,'the results are there while it answers');
  const selBefore=await page.locator('#pal-list [aria-selected="true"] .pal-label').textContent();
  go();
  await page.waitForFunction(t=>document.querySelector('#pal-answer')?.textContent===t,ANSWER);
  const lastAsk=asks.at(-1);assert.equal(lastAsk.query,'what did kim say about the pilot?');assert.equal(lastAsk.area,null);
  assert.deepEqual((await labels(page)).slice(0,2),['Pilot timing','#pilot'],'its messages under it');
  assert.equal(await page.locator('#pal-list [aria-selected="true"] .pal-label').textContent(),selBefore,'the keyboard stays where it was');
  // The answer streams in: part of it shows before all of it (checked with a fresh answer)
  await page.locator('#pal-q').fill('');await page.locator('#pal-q').fill('how is the pilot going?');
  const partial=await page.waitForFunction(t=>{const p=document.querySelector('#pal-answer');const s=p&&!p.classList.contains('muted')?p.textContent:'';return s&&s.length<t.length?s:null},ANSWER,{polling:5});
  assert.ok(ANSWER.startsWith(await partial.jsonValue()));
  await page.waitForFunction(t=>document.querySelector('#pal-answer')?.textContent===t,ANSWER);
  // A source opens the message where messages open
  await page.locator('#pal-list .pal-item',{hasText:'Pilot timing'}).first().click();  // the answer's own row
  await page.locator('#email-dialog[open]').waitFor();assert.equal(await page.locator('#email-title').textContent(),'Pilot timing');
  await page.keyboard.press('Escape');
  // The area in view goes with it
  await page.evaluate(()=>{scopeFilter='work'});await palOpenNow(page,1440);await page.keyboard.type('what about the pilot budget');
  await settled(()=>asks.at(-1)?.query==='what about the pilot budget',true,'asked');assert.equal(asks.at(-1).area,'work');
  await page.keyboard.press('Escape');
  // A failure: one short line, nothing else changes
  mode='error';await palOpenNow(page,1440);await page.keyboard.type('did the pilot move?');
  await page.locator('#pal-answer',{hasText:'Couldn’t answer that right now.'}).waitFor();
  assert.ok((await groups(page)).includes('Messages'));
  await page.keyboard.press('Escape');
  // No model: nothing shows, and it stops asking for this page
  mode='off';await palOpenNow(page,1440);await page.keyboard.type('what did lee say?');
  await settled(()=>asks.at(-1)?.query==='what did lee say?',true,'asked once');await page.evaluate(()=>new Promise(r=>setTimeout(r,50)));
  assert.ok(!(await groups(page)).includes('Answer'));const n=asks.length;
  await page.locator('#pal-q').fill('what did kim say then?');await page.evaluate(()=>new Promise(r=>setTimeout(r,1200)));
  assert.equal(asks.length,n,'no model: not asked again');
  await context.close()}
 // Shots: 390 and 1440, light and dark
 for(const colorScheme of ['light','dark'])for(const [w,h] of [[390,844],[1440,900]]){
  const {context,page}=await open(w,h,colorScheme);await palOpenNow(page,w);
  await page.keyboard.type('what did kim say about the pilot?');
  await page.waitForFunction(t=>document.querySelector('#pal-answer')?.textContent===t,ANSWER);
  // the answer reads in full and fits the palette, never wider than the screen
  const box=await page.locator('#pal-answer').boundingBox();assert.ok(box.x>=0&&box.x+box.width<=w,'fits '+w);
  if(shots)await page.screenshot({path:`${shots}/search-ask-${w}-${colorScheme}.png`});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('search ask dashboard ok');
}finally{await browser?.close();server.close()}
