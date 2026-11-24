import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// What someone typed in New to-do, Ask for changes, Answer, the ask boxes of Go through and the follow-ups' review, and a
// review's note and edits (dashboard/todos-kept-box.js, over todos-kept.js) comes back after Esc, a closed sheet, another
// page and a reload: kept only, never posted, readable in storage or in the address. Cancel and Discard end it (with Undo),
// and so does asking, answering or adding; another question or another review doesn't get it.
const raw=await dashboardPage(),CSRF='c'.repeat(64),now=new Date().toISOString(),shots=process.env.SHOTS||'';
const page=()=>raw.replace('__CSRF__',CSRF).replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__','a1'.repeat(16));
const [P,Q,N,V,W,U]=['1','2','3','4','5','6'].map(x=>x.repeat(16)),rev=n=>n.repeat(12);
const card=(id,title,x)=>({id,title,body:'Text.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[1],...x});
const fresh=()=>[
 card(P,'Book a table',{status:'pending',preparation_status:null}),
 card(Q,'Send the invoice',{status:'instructions',preparation_status:'blocked',preparation_reason:'I need to know where the invoice goes.'}),
 card(N,'Finish the listing',{status:'instructions',preparation_status:'blocked',preparation_reason:'Two things.',preparation_questions:[{question:'What did you notice?'},{question:'Which room?',suggestion:'Room B'}]}),
 card(V,'Review the reply',{status:'pending',review_in:{id:'q_1',from:'Owner Example',what:'draft',subject:'Pricing',to:'sam@client.example',note:'Ok?',body:'Hi Sam, 40 per seat.',stage:'open',open:true,reply:null}}),
 card(W,'Order paper',{status:'pending',preparation_status:null}),
 card(U,'Follow up',{next_action:{kind:'email',revision:rev('d'),label:'Send',to:['lee@client.example'],to_name:'Lee',from:'me@acme.example',subject:'Pilot',body:'Hi Lee, any news?'},follow_up:{project:'Pilot',project_id:'project:1',board:'Testers',group:'board:1',n:1,max:3,channel:'email',auto:false,state:'open'}})];
let cards=fresh(),posts=[],fail='';
const server=createServer(async(req,res)=>{let b='';for await(const x of req)b+=x;const u=new URL(req.url,'http://x');res.setHeader('Content-Type','application/json');
 if(u.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page());return}
 if(u.pathname==='/api/session'){res.end(JSON.stringify({csrf:CSRF,cache_scope:'a1'.repeat(16)}));return}
 if(u.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},fleet:{on:true,fleets:[],reviews:['work']},done_counts:{all:0},clear_pace:45}));return}
 if(u.pathname==='/api/fleet'){res.end(JSON.stringify({on:true,kinds:{},fleets:[],waiting:[],asked:[],intro_offers:[],splits:[],log:[],notices:[]}));return}
 if(u.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:[],next:null,total:0}));return}
 if(u.pathname==='/api/action'){const a=JSON.parse(b||'{}'),c=cards.find(x=>x.id===a.args?.suggestion_id);posts.push(a);if(fail===a.action){res.statusCode=400;res.end('{"error":"Not now."}');return}
  if(a.action==='decide'){if(a.args.choice!=='undo')c.status='instructions';if(c.status==='instructions')c.preparation_status='running';res.end(JSON.stringify({status:c.status}));return}
  if(a.action==='card_new'){res.end(JSON.stringify({id:'7'.repeat(16)}));return}
  if(a.action==='fleet_review_options'){res.end(JSON.stringify({suggestion_id:c.id,scope:'work',what:'todo',title:c.title,body:c.body,fleets:[{id:'fl_'+'a'.repeat(16),name:'Acme',members:[{member_id:'pat1',name:'Pat Doe'}]}],sources:[],open:null}));return}
  if(a.action==='fleet_review_reply'){c.status='completed';c.review_in.open=false}
  res.end(JSON.stringify(a.action==='card_chat'?{session:true,status:'blocked',active:false,cursor:'k',items:[{kind:'steps',count:4,steps:[{line:['Read your mail'],n:4}],at:Date.now()}]}:{ok:true}));return}
 res.statusCode=u.pathname.startsWith('/brand/')||u.pathname==='/sw.js'?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',errors=[];
const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
// Asked again from here: waitForFunction takes an async function's promise itself for a yes
const kept=(p,ok,what)=>(async()=>{const end=Date.now()+10000;for(let v;;await new Promise(r=>setTimeout(r,100))){v=await p.evaluate(async()=>(await localCache.read('kept'))?.value||[]);
 if(ok(v))return;assert.ok(Date.now()<end,what+': '+JSON.stringify(v))}})();
const stored=(p,n)=>kept(p,v=>v.length===n,n+' kept');
const toast=(p,text)=>p.locator('#toast.show',{hasText:text}).waitFor();
const shot=async(p,name,sel)=>{if(!shots)return;if(sel)await p.locator(sel).first().scrollIntoViewIfNeeded();await p.screenshot({path:`${shots}/${name}-${p.viewportSize().width}.png`,animations:'disabled'})};
const sent=action=>posts.filter(x=>x.action===action).map(x=>x.args);
try{
 for(const [w,h] of [[1440,900],[390,844]]){
  cards=fresh();posts=[];const c=await b.newContext({viewport:{width:w,height:h},hasTouch:w<500,isMobile:w<500});
  await c.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
  const p=await c.newPage();p.setDefaultTimeout(15000);p.on('pageerror',e=>errors.push(w+': '+e.message+' '+e.stack));
  const open=async()=>{await p.goto(base);await p.locator('#task-'+P).waitFor()},again=async()=>{await p.evaluate(()=>typeof ktRun==='undefined'||ktRun);await p.reload();await p.locator('#task-'+P).waitFor()};
  const value=(sel,v)=>p.waitForFunction(([sel,v])=>document.querySelector(sel)?.value===v,[sel,v]);
  await open();
  // New to-do, typed in before anything else loaded: Esc keeps it, with its chips, and says so
  await p.evaluate(()=>newTodo());await p.locator('#new-card[open]').waitFor();await p.locator('#nc-text').pressSequentially('Call the venue');
  await p.locator('[data-nc=personal]').click();await p.evaluate(()=>{nc.due=ncQuick('tomorrow');nc.about=[{id:'person:1',name:'Robin'}];ncChips()});await p.locator('#nc-text').pressSequentially(' today');await stored(p,1);
  await p.keyboard.press('Escape');await toast(p,'Kept, not added.');await shot(p,'1-new-kept');
  await p.evaluate(()=>newTodo());await value('#nc-text','Call the venue today');await p.keyboard.press('Escape');
  await again();await p.evaluate(()=>newTodo());await value('#nc-text','Call the venue today');
  assert.deepEqual(await p.evaluate(()=>[nc.scope,nc.due.timed,nc.due.getHours(),nc.about[0].name,document.querySelector('#nc-add').disabled]),['personal',true,9,'Robin',false]);await shot(p,'2-new-back');
  // Discard, Undo, and what is shared from the phone comes after it
  await p.keyboard.press('Escape');await p.locator('#toast button',{hasText:'Discard'}).click();await toast(p,'Discarded.');await stored(p,0);await p.locator('#toast button',{hasText:'Undo'}).click();await stored(p,1);
  await p.evaluate(()=>machineShare({text:'https://venue.example/'}));await value('#nc-text','Call the venue today\nhttps://venue.example/');
  // A failed Add keeps it, Add ends it
  fail='card_new';await p.locator('#nc-add').click();await p.locator('#nc-error',{hasText:/./}).waitFor();fail='';await stored(p,1);
  await p.locator('#nc-add').click();await p.locator('#new-card[open]').waitFor({state:'hidden'});await stored(p,0);assert.equal(sent('card_new').at(-1).about[0],'person:1');
  await p.evaluate(()=>newTodo());assert.equal(await p.locator('#nc-text').inputValue(),'');await p.keyboard.press('Escape');

  // Ask for changes on a to-do: after another page and a reload its box is open with the text
  await open();await p.locator(`#task-${P} [data-choice=change]`).first().evaluate(x=>x.click());await p.locator('#feedback-'+P).pressSequentially('Somewhere quieter');await stored(p,1);
  await p.goto(base+'#calendar');await p.goto(base);await again();await value('#feedback-'+P,'Somewhere quieter');await shot(p,'3-changes-back','#feedback-'+P);
  assert.deepEqual(await p.evaluate(()=>[JSON.stringify(localStorage)+JSON.stringify(sessionStorage)+location.href].filter(x=>/quieter/.test(x))),[],'sealed');assert.ok(!posts.some(x=>/quieter/.test(JSON.stringify(x))),'never posted');
  // Cancel discards it, Undo brings it back, and Go through has the same text
  await p.locator(`#task-${P} [data-choice=cancel-change]`).click();await toast(p,'Discarded.');await stored(p,0);assert.equal(await p.locator('#feedback-'+P).count(),0);
  await p.locator('#toast button',{hasText:'Undo'}).click();await value('#feedback-'+P,'Somewhere quieter');await stored(p,1);
  // An Undo of something else on the to-do leaves it
  await p.evaluate(id=>saveDecision(id,'undo'),P);await stored(p,1);await again();await value('#feedback-'+P,'Somewhere quieter');
  await p.locator('[data-clear-run]').first().evaluate(x=>x.click());await p.locator('#clear-run[open]').waitFor();
  while(await p.locator('#clear-run .cr-title').innerText()!=='Book a table')await p.locator('#clear-run [data-cr=skip]').click();
  await p.locator('#clear-run [data-cr=ask]').click();await value('#cr-ask','Somewhere quieter');await p.locator('#cr-ask').pressSequentially(', by the sea');await shot(p,'4-go-through');
  await p.keyboard.press('Escape');await toast(p,'Kept, not sent.');await again();await value('#feedback-'+P,'Somewhere quieter, by the sea');
  fail='decide';await p.locator(`#task-${P} [data-choice=other]`).click();await toast(p,'Not now.');fail='';await stored(p,1);
  await p.locator(`#task-${P} [data-choice=other]`).click();await stored(p,0);assert.equal(sent('decide').at(-1).feedback,'Somewhere quieter, by the sea');
  await again();assert.equal(await p.locator('#feedback-'+P).count(),0);

  // Answer: comes back when Answer is opened; another question gets its own
  await p.locator(`#task-${Q} [data-choice=answer]`).first().evaluate(x=>x.click());await p.locator('#feedback-'+Q).pressSequentially('To Sam');await stored(p,1);
  await again();await p.locator(`#task-${Q} [data-choice=answer]`).first().evaluate(x=>x.click());await value('#feedback-'+Q,'To Sam');await shot(p,'5-answer-back','#feedback-'+Q);
  cards[1].preparation_reason='Which month is it for?';await again();await p.locator(`#task-${Q} [data-choice=answer]`).first().evaluate(x=>x.click());assert.equal(await p.locator('#feedback-'+Q).inputValue(),'');
  cards[1].preparation_reason='I need to know where the invoice goes.';await again();await p.locator(`#task-${Q} [data-choice=answer]`).first().evaluate(x=>x.click());await value('#feedback-'+Q,'To Sam');
  await p.locator(`#task-${Q} .answer-editor [data-choice=other]`).click();await stored(p,0);
  // Named questions: each on its own, in the to-do and in its chat
  await p.locator(`#ask-${N}-0`).fill('It is slow');await p.locator(`#ask-${N}-1`).fill('Room C');await stored(p,2);await again();await value(`#ask-${N}-0`,'It is slow');await value(`#ask-${N}-1`,'Room C');await shot(p,'6-questions-back',`#ask-${N}-0`);
  await p.goto(base+'#chat='+N);await p.reload();await p.waitForFunction(()=>document.querySelector('.chat-ask [data-q="0"] textarea')?.value==='It is slow');
  await open();await value(`#ask-${N}-1`,'Room C');await p.locator(`#task-${N} [data-choice=ask-send]`).click();await stored(p,0);assert.match(sent('decide').at(-1).feedback,/It is slow\n.*Room C/);

  // A review: its edits and comment come back, another review of it starts clean
  const inF=n=>`#task-${V} .review-in [name=${n}]`;
  await p.locator(inF('subject')).fill('Pricing for 40');await p.locator(inF('body')).fill('Hi Sam, 38 per seat.');await p.locator(inF('comment')).fill('Shorter');await stored(p,3);
  await again();await value(inF('body'),'Hi Sam, 38 per seat.');await value(inF('subject'),'Pricing for 40');await value(inF('comment'),'Shorter');await p.locator(`#task-${V} .review-edited`).waitFor();await shot(p,'7-review-back',inF('body'));
  cards[3].review_in.id='q_2';await again();assert.equal(await p.locator(inF('body')).inputValue(),'Hi Sam, 40 per seat.');
  cards[3].review_in.id='q_1';await again();await value(inF('body'),'Hi Sam, 38 per seat.');
  await p.locator(`#task-${V} [data-review-reply=changes]`).click();await stored(p,0);assert.deepEqual(sent('fleet_review_reply').map(x=>[x.subject,x.body,x.comment]),[['Pricing for 40','Hi Sam, 38 per seat.','Shorter']]);
  // Asking for one: the note
  const ask=()=>p.locator(`#task-${W} [data-review-ask]`).first().evaluate(x=>x.click()),note=`#task-${W} .review-form [name=note]`;
  await ask();await p.locator(note).fill('Is it enough?');await stored(p,1);await again();await ask();await value(note,'Is it enough?');await shot(p,'8-note-back',note);
  await p.locator(`#task-${W} [data-review-cancel]`).click();await toast(p,'Discarded.');await stored(p,0);await p.locator('#toast button',{hasText:'Undo'}).click();await stored(p,1);
  await ask();await value(note,'Is it enough?');await p.locator(`#task-${W} .review-form .primary`).click();await stored(p,0);assert.equal(sent('fleet_review_ask')[0].note,'Is it enough?');

  // The follow-ups' Change box: Esc, the review closed, a reload
  const review=async()=>{await p.locator('[data-fu-review="board:1"]').last().evaluate(x=>x.click());await p.locator('#fu-review[open] [data-fr-change]').click()};
  await review();await p.locator('#fr-change-text').pressSequentially('Warmer');await stored(p,1);await p.keyboard.press('Escape');await p.locator('[data-fr-change]').click();await value('#fr-change-text','Warmer');
  await p.evaluate(()=>document.querySelector('#fu-review').close());await toast(p,'Kept, not sent.');await again();await review();await value('#fr-change-text','Warmer');await shot(p,'9-follow-ups-back');
  await p.locator('[data-fr-box-cancel]').click();await toast(p,'Discarded.');await stored(p,0);await p.locator('[data-fr-change]').click();assert.equal(await p.locator('#fr-change-text').inputValue(),'');
  await p.locator('#fr-change-text').pressSequentially('Shorter');await stored(p,1);await p.locator('[data-fr-box-go]').click();await stored(p,0);
  await c.close()}

 // Two tabs: an untouched box follows, what is typed in one stays on its screen
 cards=fresh();const c=await b.newContext({viewport:{width:1440,height:900}});await c.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 const tab=async()=>{const p=await c.newPage();p.setDefaultTimeout(15000);p.on('pageerror',e=>errors.push('tabs: '+e.message));await p.goto(base);await p.locator('#task-'+P).waitFor();return p},one=await tab(),two=await tab();
 await two.evaluate(()=>lazyPart('keptbox').then(()=>lazyPart('kept')).then(()=>ktReady));
 await one.locator(`#ask-${N}-0`).fill('From one');await two.waitForFunction(x=>document.querySelector(`#ask-${x}-0`).value==='From one',N);
 await two.locator(`#ask-${N}-0`).fill('From two');await stored(one,1);assert.equal(await one.locator(`#ask-${N}-0`).inputValue(),'From one');
 await c.close();
 assert.deepEqual(errors,[]);console.log('ok kept boxes');
}finally{await b.close();server.close()}
