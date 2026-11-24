import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Prepared or Needs you: a to-do says Prepared only with a draft or result to approve. One whose run ended needing the
// owner, with nothing ready (needs_owner in its view, machine/cards.py), says Needs you in amber, with what it needs on
// its status line (no "Needs you:" again), and the list's "Nothing goes out until you approve it." note leaves it out.
// A Prepared one's line beside its draft is plain: amber and "Needs you" belong to Needs you ones. Work that can't be used
// before they answer (needs_first true) is a Needs you one too: the question as its line, Answer in front, what it made
// still on it; work that can go as it is (false) says what is ready before its question, Send in front. Made-up data.
// SHOTS=<folder> saves the list at 1440x900 and 390x844, light and dark.
const dashboard=await dashboardPage(process.env.PAGE);
const NOW=Date.UTC(2026,10,5,10,0,0),h=n=>new Date(NOW-n*3600e3).toISOString();
const card=(id,title,status,created_at,more={})=>({id:id.repeat(16).slice(0,16),title,body:'Made-up to-do.',status,scope:'work',event_ids:[],created_at,...more});
const DRAFT={kind:'email',label:'Send reply',account_id:'work',to:['pat@example.com'],subject:'Re: Pilot',body:'Hi Pat,\n\nThursday works.\n\nAlex',revision:'r1'};
const NEED='Which of the two quotes should it accept?',PRICE='What price, scope and VAT should it quote?',TONE='Should it mention the spring dates too?';
const FILES=[{index:0,name:'proposal.md',size:900}],PROPOSAL='The proposal draft is written, without a price. [Proposal](memory/assistant/261105-proposal.md)';
let ready=true;
const cards=()=>[
 card('q','Pick a quote for the new printer','prepared',h(1),{outcome:JSON.stringify({state:'needs_you',needs:NEED}),needs_owner:NEED}),
 // a run that only answered, with nothing ready: the task is still to do, so Needs you, with Do it first
 card('a','Confirm the delivery date with the client','prepared',h(3),{outcome:JSON.stringify({state:'answered'}),needs_owner:'Answered. Nothing done yet.'}),
 ...(ready?[card('r','Reply to Pat about the pilot','prepared',h(2),{outcome:JSON.stringify({state:'needs_you',needs:'check the draft and send it'}),next_actions:[DRAFT]}),
 card('f','Write the proposal for Kestrel','prepared',h(4),{body:PROPOSAL,outcome:JSON.stringify({state:'needs_you',needs:PRICE,needs_first:true}),needs_owner:PRICE,result_files:FILES}),
 // an earlier run's, which didn't say: the server's needs_owner makes it ask
 card('e','Write the proposal for Fjord','prepared',h(5),{body:PROPOSAL,outcome:JSON.stringify({state:'needs_you',needs:PRICE}),needs_owner:PRICE,result_files:FILES}),
 card('b','Send Kim the quote','prepared',h(6),{outcome:JSON.stringify({state:'needs_you',needs:PRICE,needs_first:true}),needs_owner:PRICE,next_actions:[{...DRAFT,revision:'r2',to:['kim@example.com'],to_name:'Kim',label:'Send to Kim',body:'Hi Kim,\n\nOur price is [price].\n\nAlex'}]}),
 card('c','Reply to Noor about the open day','prepared',h(7),{outcome:JSON.stringify({state:'needs_you',needs:TONE,needs_first:false}),next_actions:[{...DRAFT,revision:'r3',to:['noor@example.com'],to_name:'Noor',label:'Send to Noor',body:'Hi Noor,\n\nWe will be there on Saturday.\n\nAlex'}]}),
 card('d','Write the speech for Saturday','prepared',h(8),{body:'The draft is written. [Speech](memory/assistant/261105-speech.md)',outcome:JSON.stringify({state:'needs_you',needs:TONE,needs_first:false}),result_files:[{index:0,name:'speech.md',size:900}]})]:[])];
const state=()=>({suggestions:cards(),promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){readFile(new URL('../'+(url.pathname.startsWith('/brand/fonts/')?url.pathname.slice(1):'brand/app-icon-192.png'),import.meta.url)).then(b=>{res.setHeader('Content-Type',url.pathname.endsWith('.woff2')?'font/woff2':'image/png');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,errors=[],shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const sel=c=>'#task-'+c.repeat(16).slice(0,16);
const chip=(page,c)=>page.locator(sel(c)+' .card-badges .chip').first();
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){
  ready=true;
  const context=await browser.newContext({viewport:{width,height},timezoneId:'Europe/Brussels',locale:'en-US'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));await page.clock.setFixedTime(NOW);
  await page.goto(base+'/');await page.locator('#section-foryou').waitFor();
  // Needs you: the chip, its amber tone, and the reason from the run's own outcome
  assert.equal(await chip(page,'q').textContent(),'Needs you');
  assert.match(await page.locator(sel('q')).getAttribute('class'),/\bt-amber\b/);
  assert.equal(await page.locator(sel('q')+' .status-line.outcome').textContent(),NEED);
  assert.equal(await chip(page,'a').textContent(),'Needs you');
  assert.equal(await page.locator(sel('a')+' .status-line').textContent(),'Answered. Nothing done yet.');
  assert.doesNotMatch(await page.locator(sel('a')).textContent(),/Prepared/);
  // Prepared: a ready draft keeps its label and tone
  assert.equal(await chip(page,'r').textContent(),'Prepared');
  assert.doesNotMatch(await page.locator(sel('r')).getAttribute('class'),/\bt-amber\b/);
  assert.equal(await page.locator(sel('r')+' .status-line').textContent(),'Check the draft and send it.');
  assert.equal(await page.locator(sel('r')+' .status-line.outcome').count(),0,'a plain line, not amber');
  assert.doesNotMatch(await page.locator(sel('r')).textContent(),/Needs you/);
  assert.equal(await page.locator('#section-foryou .section-note').count(),1,'one ready draft: the approve note shows');
  // It can't be used before they answer: the question is the line, Answer leads, what it made stays a tap away
  const lead=c=>page.locator(sel(c)+' .actions .primary').allTextContents();
  for(const c of ['f','e','b']){
   assert.equal(await chip(page,c).textContent(),'Needs you',c);
   assert.equal(await page.locator(sel(c)+' .status-line.outcome').textContent(),PRICE,c);
   assert.deepEqual(await lead(c),['Answer'],c);
   assert.equal(await page.locator(sel(c)+' .foot-links [data-result="read"]').count(),1,c);
   assert.equal(await page.locator(sel(c)+' .foot-links [data-result="copy"]').count(),1,c);
   assert.equal(await page.evaluate(id=>crKind(state.suggestions.find(s=>s.id===id)),c.repeat(16)),'',c+': not one to go through at a tap');
   assert.doesNotMatch(await page.locator(sel(c)).textContent(),/This can’t be sent from here|Prepared/,c);
  }
  assert.match(await page.locator(sel('b')).textContent(),/Our price is \[price\]/,'the partial draft shows');
  assert.equal(await page.locator(sel('b')+' .more-actions [data-smart]').count(),1,'its Send is in the …');
  // It can go as it is: Prepared, what is ready before the question, Send (or Copy draft) in front
  for(const [c,line,first] of [['c','The draft is ready. One question: '+TONE,'Review and send to Noor'],['d','The draft is ready. One question: '+TONE,'Copy draft']]){
   assert.equal(await chip(page,c).textContent(),'Prepared',c);
   assert.equal(await page.locator(sel(c)+' .status-line').textContent(),line);
   assert.equal(await page.locator(sel(c)+' .status-line.outcome').count(),0,c);
   assert.deepEqual(await lead(c),[first],c);
   assert.equal(await page.locator(sel(c)+' [data-choice="answer"]').count(),0,c);
  }
  assert.equal(await page.evaluate(id=>crKind(state.suggestions.find(s=>s.id===id)),'c'.repeat(16)),'send');
  if(shots)for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});await page.evaluate(async()=>{for(let i=0;i<2;i++)await new Promise(r=>requestAnimationFrame(r));await Promise.all(document.getAnimations().map(x=>x.finished))});await page.screenshot({path:`${shots}/needs-you-${width}-${scheme}.png`});for(const c of ['f','b','c','d'])await page.locator(sel(c)).screenshot({path:`${shots}/todo-${c}-${width}-${scheme}.png`})}
  await page.emulateMedia({colorScheme:'light'});
  // Only a Needs you one left: nothing to approve, so no approve note
  ready=false;await page.evaluate(()=>refresh());await page.locator(sel('r')).waitFor({state:'detached'});
  assert.equal(await page.locator(sel('r')).count(),0);
  assert.equal(await page.locator('#section-foryou .section-note').count(),0,'nothing ready: no approve note');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('needs owner ok');
}finally{await browser?.close();server.close()}
