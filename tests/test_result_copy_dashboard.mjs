import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Read result's Copy draft shows only beside something to copy: a message draft or a text file, as the card's own
// Copy draft link. A result that only explains what it found (nothing drafted, no file) or has only a PDF offers no
// Copy draft: there is no draft. Made-up data. SHOTS=<folder> saves the dialog at 1440x900 and 390x844, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const DRAFT={kind:'email',label:'Send reply',account_id:'work',to:['pat@example.com'],subject:'Re: Pilot',body:'Hi Pat,\n\nThursday works.\n\nAlex',revision:'r1'};
const card=(id,title,more)=>({id:id.repeat(16),title,status:'prepared',scope:'work',created_at:now,event_ids:[1],
 body:'The deadline passed and no delivery was found. Still open: scope, price and a new date. No message was drafted or sent.',
 outcome:JSON.stringify({state:'answered'}),...more});
const cards=[card('a','Confirm the delivery date with the client',{}),
 card('b','Reply to Pat about the pilot',{outcome:JSON.stringify({state:'needs_you',needs:'check the draft and send it'}),next_actions:[DRAFT]}),
 card('c','Write the practice plan',{outcome:JSON.stringify({state:'done'}),result_files:[{name:'plan.md',path:'memory/assistant/plan.md'}]}),
 card('d','Fill in the tax form',{outcome:JSON.stringify({state:'done'}),result_files:[{name:'form.pdf',path:'memory/assistant/form.pdf'}]})];
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/result'){res.end(JSON.stringify(url.searchParams.get('file').endsWith('.pdf')?{pdf:true}:{text:'# Practice plan\n\nThree schedules.'}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[],shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+'a'.repeat(16)).waitFor();
  const copy=page.locator('#result-copy');
  const open=async c=>{await page.evaluate(id=>openResult(id),c.repeat(16));await page.locator('#result-dialog[open]').waitFor()};
  const close=()=>page.evaluate(()=>document.querySelector('#result-dialog').close());
  // Only an explanation: nothing to copy, no Copy draft (and none on the card either)
  await open('a');
  assert.match(await page.locator('#result-content').innerText(),/No message was drafted or sent/);
  assert.equal(await copy.isVisible(),false,'no draft: no Copy draft');
  assert.equal(await page.locator('#task-'+'a'.repeat(16)+' [data-result="copy"]').count(),0);
  if(shots)await page.screenshot({path:`${shots}/result-explained-${width}-${scheme}.png`});
  await close();
  // A message draft, or a text file: Copy draft is there
  await open('b');assert.equal(await copy.isVisible(),true,'a draft: Copy draft');
  if(shots)await page.screenshot({path:`${shots}/result-draft-${width}-${scheme}.png`});
  await close();
  await open('c');assert.equal(await copy.isVisible(),true,'a text file: Copy draft');await close();
  // Only a PDF: nothing to copy as text
  await open('d');assert.equal(await copy.isVisible(),false,'a PDF only: no Copy draft');await close();
  // and back to a draft after one without: it shows again
  await open('b');assert.equal(await copy.isVisible(),true);await close();
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('result copy ok');
}finally{await browser?.close();await new Promise(r=>server.close(r))}
