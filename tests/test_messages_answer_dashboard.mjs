import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
import {settled} from './page-calls.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Messages search, on made-up data: an English question about a booking whose code is in a Dutch mail. The results
// keep the search's order (best match first, not newest first, and no Coming up split); the question gets a short
// answer above them, from Ask (search_ask), with the message it read to open; keywords, one account, an answer that
// cites nothing or no model show no answer at all.
// MESSAGES_ANSWER_SHOTS=dir saves shots at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const now=new Date(),ago=d=>new Date(now-d*864e5).toISOString();
const id=n=>(n+'').padStart(2,'0').repeat(8);
const QUESTION='what’s the regenboog discount code?';
const MARKUP='<img src=x onerror="window.__pwned=1">';
const ANSWER='The code is FEEST10: 10% off a kids’ party at Speelpark de Regenboog, entered at the last step before paying.';
const BOOKING={id:51,account_id:'home',kind:'gmail.message',title:'Bevestiging van je jaarabonnement',occurred_at:ago(80),
 body:'Bedankt voor je bestelling. 10% korting op een kinderfeestje bij Speelpark de Regenboog. Gebruik de kortingscode FEEST10 bij het afrekenen.',metadata:{from:'Speelpark de Regenboog <info@regenboog.example>'}};
const ROWS=[BOOKING,  // best match first, as the search ranked it, though older than the rest
 {id:52,account_id:'chat',kind:'whatsapp.message',title:'Family group',occurred_at:ago(1),body:'Party at Regenboog on the 16th, who is coming?',metadata:{from_me:true}},
 {id:53,account_id:'phone',kind:'android.notification',title:'Planner',occurred_at:ago(0.5),body:'Which party at Regenboog: adventure or bowling?',metadata:{app_name:'Planner'}},
 {id:54,account_id:'home',kind:'calendar.event',title:'Party at Regenboog',occurred_at:new Date(+now+20*864e5).toISOString(),body:'',metadata:{}}];
let asks,mode;const reset=()=>{asks=[];mode='answer'};reset();
const state=()=>({suggestions:[{id:id(1),title:'Plan the party',body:'',status:'pending',scope:'personal',created_at:ago(0),event_ids:[]}],promises:[],suggestion_counts:{},
 decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[{id:'home',display_name:'Home mail'},{id:'chat',display_name:'WhatsApp'}],fleet:{on:false,fleets:[]},model_status:{model:'acme/lm-2'}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/events'){res.end(JSON.stringify(url.searchParams.get('q')?ROWS:[...ROWS].reverse()));return}
 if(url.pathname==='/api/originals'){const m=ROWS.find(x=>String(x.id)===url.searchParams.get('event'));
  res.end(JSON.stringify({originals:m?[{event_id:m.id,kind:'email',from:m.metadata.from,occurred_at:m.occurred_at,subject:m.title,body:m.body}]:[]}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  if(r.action==='search_ask'){asks.push(r.args);
   res.end(JSON.stringify(mode==='off'?{off:true}:mode==='markup'?{answer:MARKUP,sources:[{id:51,kind:'gmail.message',title:MARKUP,at:BOOKING.occurred_at}]}:mode==='unanswered'?{answer:'These messages don’t say.',sources:[]}:
    {answer:ANSWER,sources:[{id:51,kind:'gmail.message',title:BOOKING.title,from:'Speelpark de Regenboog',at:BOOKING.occurred_at}]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.MESSAGES_ANSWER_SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const open=async(width,height,colorScheme='light')=>{const mobile=width<600;reset();
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels',colorScheme});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.goto(base+'#messages');await page.locator('#query').waitFor();return {context,page}};
const searchFor=async(page,q)=>{await page.locator('#query').fill(q);await page.locator('#query').press('Enter');
 await page.waitForFunction(()=>document.querySelectorAll('#results article').length>0)};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 {const {context,page}=await open(1440,900);
  // Keywords: no answer asked, results newest first without words, in the search's order with words
  await searchFor(page,'regenboog');
  assert.equal(asks.length,0,'one word is never asked');assert.ok(await page.locator('#ev-answer').isHidden());
  // the list before the search (newest first) can still be the one shown when the first result appears: wait for the search's
  await settled(()=>page.locator('#results article').evaluateAll(a=>a.map(x=>+x.dataset.event)),[51,52,53,54],'best match first, the meeting to come in its place');
  assert.equal(await page.locator('#results .ev-soon').count(),0,'no Coming up split in a search');
  // A question: the answer above the results, with the message it read, which opens
  await searchFor(page,QUESTION);
  // the answer, not the Looking… line that shows while it works
  await page.locator('#ev-answer p:not([role=status])').waitFor();
  assert.deepEqual(asks.at(-1),{query:QUESTION,area:'all'});
  assert.equal(await page.locator('#ev-answer p').textContent(),ANSWER);
  assert.equal(await page.locator('#ev-answer .ge-day').textContent(),'Answer');
  assert.match(await page.locator('#ev-answer .ev-src').textContent(),/^Bevestiging van je jaarabonnement · /);
  const box=await page.locator('#ev-answer').boundingBox(),first=await page.locator('#results article').first().boundingBox();
  assert.ok(box.y+box.height<=first.y,'above the results');
  await page.locator('#ev-answer .ev-src').click();
  await page.locator('#email-dialog[open]').waitFor();assert.equal(await page.locator('#email-title').textContent(),BOOKING.title);
  await page.keyboard.press('Escape');
  // An answer that cites nothing (the messages don't say): nothing shows
  mode='unanswered';await searchFor(page,'what did the venue say about parking?');
  await settled(()=>asks.length===2,true,'asked');await page.evaluate(()=>new Promise(r=>setTimeout(r,80)));
  assert.ok(await page.locator('#ev-answer').isHidden(),'quality or nothing');
  // One account picked: the answer would read every account, so it isn't asked
  mode='answer';await page.locator('#account').evaluate(s=>{s.add(new Option('Home mail','home'));s.value='home';s.dispatchEvent(new Event('change'))});
  await page.waitForFunction(()=>document.querySelectorAll('#results article').length>0);await page.evaluate(()=>new Promise(r=>setTimeout(r,80)));
  assert.equal(asks.length,2,'not asked for one account');assert.ok(await page.locator('#ev-answer').isHidden());
  mode='off';await page.locator('#account').selectOption('all');await settled(()=>asks.length===3,true,'asked');
  await page.evaluate(()=>new Promise(r=>setTimeout(r,80)));assert.ok(await page.locator('#ev-answer').isHidden(),'no model: nothing');
  // An answer or a source title with markup in it shows as text: nothing in it runs or becomes an element
  mode='markup';await searchFor(page,'what did the mail with the image say?');await page.locator('#ev-answer p:not([role=status])').waitFor();
  assert.equal(await page.locator('#ev-answer p').textContent(),MARKUP);assert.match(await page.locator('#ev-answer .ev-src').textContent(),/^<img /);
  assert.equal(await page.locator('#ev-answer img').count(),0);assert.equal(await page.evaluate(()=>window.__pwned),undefined);
  await context.close()}
 for(const [w,h] of [[390,844],[1440,900]])for(const scheme of ['light','dark']){const {context,page}=await open(w,h,scheme);
  await searchFor(page,QUESTION);await page.locator('#ev-answer p:not([role=status])').waitFor();
  const over=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);assert.ok(over<=0,`${w}: no sideways scroll`);
  const a=await page.locator('#ev-answer').boundingBox();assert.ok(a.x>=8&&a.x+a.width<=w-8,`${w}: the answer fits`);
  if(shots)await page.screenshot({path:`${shots}/messages-answer-${w}-${scheme}.png`});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok messages answer dashboard');
}finally{await browser?.close();server.close()}
