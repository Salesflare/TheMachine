import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Talk's own actions (dashboard/todos-chat.js), with OpenAI and the Machine as stand-ins:
// - "do it" is the to-do's Do it (accept, browser work included), never Mark done; one already running is left to run;
// - a correction right after an action takes it back on the to-do that action touched, which opens again;
// - "next one", "stop" never go to a to-do's chat; "let it continue" on one not started is its Do it;
// - a chat that stops after its to-do was dismissed says nothing; one that stops on its own is told once, with its title;
// - one odd word ("Azk.") changes nothing; a short "yes" is never noise; a few German words are "say that again";
// - report_bug sends the same report as Help's Report a bug, with context only when the owner agreed;
// - a send by voice shows Undo with its countdown in Talk; tapping it (or undo_send) cancels every send of that yes.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),A='a1a1a1a1a1a1a1a1',B='b2b2b2b2b2b2b2b2',C='c3c3c3c3c3c3c3c3',E='e5e5e5e5e5e5e5e5',F='f6f6f6f6f6f6f6f6',G='a7a7a7a7a7a7a7a7',H='b8b8b8b8b8b8b8b8';
const DRAFT=(to,rev)=>({kind:'email',label:'Reply',to:[to+'@example.com'],to_name:to,from:'me@example.com',subject:'Re: Thursday',body:`Hi ${to}, Thursday works. See you then.`,revision:rev,account_id:'mail'});
let cards;
const reset=()=>{cards=[
 {id:A,title:'Reply to Dana about Thursday',body:'Dana asked about Thursday.',status:'prepared',scope:'personal',created_at:now,event_ids:[1],next_actions:[DRAFT('Dana','r1')]},
 {id:H,title:'Reply to Sam about Thursday',body:'Sam asked about Thursday.',status:'prepared',scope:'personal',created_at:now,event_ids:[8],next_actions:[DRAFT('Sam','r2')]},
 {id:B,title:'Book the train tickets on the rail site',body:'Two seats to Paris on Friday.',status:'pending',scope:'personal',created_at:now,event_ids:[2]},
 {id:C,title:'Compare the three venues',body:'Working on it.',status:'accepted',preparation_status:'running',scope:'personal',created_at:now,event_ids:[3]},
 {id:E,title:'Pay the plumber',body:'Invoice came in.',status:'pending',scope:'personal',created_at:now,event_ids:[5]},
 {id:F,title:'Check the payroll export',body:'Export for October.',status:'pending',scope:'personal',created_at:now,event_ids:[6]},
 {id:G,title:'Find the insurance policy number',body:'For the claim.',status:'pending',scope:'personal',created_at:now,event_ids:[7]}]};
const state=()=>({talk_ready:true,suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const actions=[],outbox=[];let focus=null,asked=null;const polls={};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);const a=r.args||{},card=cards.find(c=>c.id===a.suggestion_id);
  const answer={
   talk_start:()=>({id:'feedfeedfeedfeed',via:'signin',limit:1800,warn:1740,main:!!a.main,tools:[],instructions:'You are The Machine.',languages:['en','nl'],turn:{type:'semantic_vad',eagerness:'low',create_response:true,interrupt_response:true},
    notes:{queued:'Joins.',done:'The chat of the to-do "{title}" finished what you asked. Its answer: "{answer}"',stopped:'The chat of the to-do "{title}" stopped before it answered "{request}".',again:'AGAIN: Say only: "Sorry, say that again?"',sent:'The Machine’s outbox confirms it went out ({what}, at {at}). Say only: "Sent."',not_sent:'Not sent ({what}): {why}'}}),
   talk_status:()=>({ready:true,limit:600,warn:540}),
   talk_offer:()=>({sdp:'v=0\r\nanswer\r\n'}),
   talk_focus:()=>{focus=a.suggestion_id;asked=null;return {ok:true}},
   talk_line:()=>({ok:true}),
   // send_status: the Machine's outbox, here the send went out at 11:42 UTC (12:42 in Brussels)
   talk_tool:()=>({output:a.name==='send_status'?(outbox.push(a.args),{state:'sent',to:'Dana',at:'2026-10-31T11:42:00+00:00',time:'12:42',say:'Sent to Dana at 12:42.'}):{title:cards.find(c=>c.id===focus)?.title||'',drafts:[]}}),
   talk_end:()=>({ok:true}),
   card_new:()=>{const id='c0c0c0c0c0c0c0c0';cards.push({id,title:a.text.split('\n')[0],body:a.text,status:'accepted',origin:'owner',scope:'personal',created_at:now,event_ids:[9]});return {id}},
   decide:()=>{if(!card)return {ok:true};const was=card.status;
    if(a.choice==='accept'){card.status='accepted';card.preparation_status='running'}
    else if(a.choice==='complete'){card.was=was;card.status='completed';card.undo_until=new Date(Date.now()+60000).toISOString()}
    else if(a.choice==='reject'){card.was=was;card.status='rejected';card.undo_until=new Date(Date.now()+60000).toISOString()}
    else if(a.choice==='reopen'||a.choice==='undo'){card.status=card.was||'pending';delete card.undo_until}
    return {ok:true}},
   // G's and E's chats: busy for one look, then done without a word (it stopped on its own)
   card_chat:()=>{const n=polls[a.suggestion_id]=(polls[a.suggestion_id]||0)+1;const busy=n===2;return {session:true,status:busy?'running':'done',active:busy,cursor:'k',items:[]}},
   talk_ask_send:()=>{if(a.ids){asked='all';return {question:'Send both, to Dana and Sam?',revision:'all',say:'Ask exactly this.'}}
    asked='r1';return {question:'Send it to Dana?',revision:'r1',say:'Ask exactly this.'}},
   talk_send:()=>{if(!asked)return {status:'not_asked'};const all=asked==='all';asked=null;
    return {status:'queued',approval_id:'voice:1',undo_ms:10000,undo_seconds:10,sent:all?[{suggestion_id:A,approval_id:'voice:1',to:'Dana',kind:'email'},{suggestion_id:H,approval_id:'voice:2',to:'Sam',kind:'email'}]:[{suggestion_id:A,approval_id:'voice:1',to:'Dana',kind:'email'}],say:'Queued.'}},
   talk_undo:()=>({ok:true}),
   bug_send:()=>({ok:true,sent:true}),
  }[r.action];
  res.end(JSON.stringify(answer?answer():{}));return}
 if(/^\/brand\/[\w.-]+\.(png|webp|woff2|svg)$/.test(url.pathname)){try{const f=await readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url));res.setHeader('Content-Type',{png:'image/png',webp:'image/webp',woff2:'font/woff2',svg:'image/svg+xml'}[url.pathname.split('.').pop()]);res.end(f)}catch{res.statusCode=404;res.end()}return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const SHOTS=process.env.SHOT_DIR;

const FAKE_RTC=()=>{const real=Date.now;window.__skew=0;Date.now=()=>real()+window.__skew;
 navigator.mediaDevices.getUserMedia=async()=>{const ac=new AudioContext(),osc=ac.createOscillator(),dest=ac.createMediaStreamDestination();osc.connect(dest);osc.start();return dest.stream};
 window.RTCPeerConnection=class{constructor(){this.connectionState='new'}
  addTrack(){}
  createDataChannel(label){const dc=window.__dc={label,readyState:'connecting',sent:[],send(x){this.sent.push(JSON.parse(x))},close(){this.readyState='closed'}};this.dc=dc;return dc}
  async createOffer(){return {type:'offer',sdp:'v=0\r\noffer\r\n'}}
  async setLocalDescription(){}
  async setRemoteDescription(){setTimeout(()=>{this.connectionState='connected';this.dc.readyState='open';this.dc.onopen?.()},60)}
  close(){this.connectionState='closed'}};
 window.__say=e=>window.__dc.onmessage({data:JSON.stringify(e)})};

const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']});
 for(const [w,h,scheme] of [[1440,900,'light'],[390,844,'light'],[390,844,'dark'],[1440,900,'dark']]){
  const phone=w<500,full=w===1440&&scheme==='light',context=await browser.newContext({viewport:{width:w,height:h},isMobile:phone,hasTouch:phone,deviceScaleFactor:2,colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.addInitScript(FAKE_RTC);
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  reset();actions.length=0;focus=null;asked=null;for(const k in polls)delete polls[k];
  await page.goto('http://127.0.0.1:'+server.address().port+'/#');await page.waitForTimeout(400);
  const tag=`${w}-${scheme}`,shot=async n=>{if(SHOTS)await page.screenshot({path:`${SHOTS}/${n}-${tag}.png`})};
  const tap=sel=>phone?page.locator(sel).tap():page.locator(sel).click();
  let n=0;const call=async(name,args={},response)=>{const id='c'+(++n);
   await page.evaluate(([id,name,args,response])=>__say({type:'response.function_call_arguments.done',call_id:id,name,arguments:JSON.stringify(args),...(response?{response_id:response}:{})}),[id,name,args,response]);
   await page.waitForFunction(id=>window.__dc.sent.some(x=>x.item?.call_id===id),id,{timeout:20000});return page.evaluate(id=>JSON.parse(window.__dc.sent.find(x=>x.item?.call_id===id).item.output),id)};
  const heard=(item,text,logprobs)=>page.evaluate(([item,text,logprobs])=>{__say({type:'input_audio_buffer.committed',item_id:item});
   __say({type:'conversation.item.input_audio_transcription.completed',item_id:item,transcript:text,...(logprobs?{logprobs}:{})})},[item,text,logprobs]);
  const told=()=>page.evaluate(()=>window.__dc.sent.filter(x=>x.type==='conversation.item.create'&&x.item?.type==='message').map(x=>x.item.content[0].text));
  const decided=id=>actions.filter(x=>x.action==='decide'&&(!id||x.args.suggestion_id===id)).map(x=>x.args.choice);
  const log=()=>page.locator('#talk-view .talk-log').textContent();
  const until=async(f,ms=6000)=>{for(let i=0;i<ms/50&&!f();i++)await page.waitForTimeout(50);assert.ok(f())};
  const viewBar='#talk-view .talk-foot .talk';

  if(phone)await page.evaluate(()=>drawerOpen());
  await page.waitForSelector('#side-talk:not([hidden])');await tap('#side-talk');
  await page.waitForFunction(sel=>document.querySelector(sel+' .talk-live strong')?.textContent==='Live',viewBar);

  if(full){
   // "Do it" on a to-do waiting for a decision: its Do it (accept), browser work included; never Mark done
   await call('open_todo',{id:B});
   const did=await call('do_it',{});assert.equal(did.started,true);assert.match(did.note,/browser work included/);assert.match(did.note,/follow it on the to-do/);
   assert.deepEqual(decided(B),['accept'],'Do it, not complete');
   // One already running: left to run, nothing posted
   const was=actions.length,run=await call('do_it',{id:C});assert.equal(run.running,true);
   assert.equal(actions.slice(was).filter(x=>x.action==='decide').length,0);
   // A draft waiting: Do it doesn't send it
   assert.match((await call('do_it',{id:A})).error,/ask_to_send/);

   // A correction right after Mark done: taken back on that to-do (not the one in focus), which opens again
   await call('open_todo',{id:G});
   assert.equal((await call('todo_action',{action:'mark_done',id:E})).ok,true);assert.deepEqual(decided(E),['complete']);
   await page.evaluate(()=>refresh());
   const undid=await call('undo_last_action');assert.equal(undid.id,E);assert.match(undid.note,/Undid "Marked done" on "Pay the plumber"/);
   assert.deepEqual(decided(E),['complete','reopen']);
   assert.equal(actions.filter(x=>x.action==='talk_focus').at(-1).args.suggestion_id,E,'the corrected to-do is in focus');
   assert.match((await call('undo_last_action')).error,/Nothing/,'once');

   // Talk's own commands never reach a chat; "let it continue" on one not started is its Do it
   await call('open_todo',{id:F});
   for(const req of ['Next one.','Okay, move on to the next one.','Stop.','Leave it.','Ga maar door naar de volgende.']){
    const r=await call('ask_chat',{request:req});assert.match(r.error,/not the chat/,req)}
   assert.equal(actions.filter(x=>x.action==='decide'&&String(x.args.decision_id).startsWith('chat-talk-')).length,0,'nothing relayed');
   const go=await call('ask_chat',{request:'Let it continue.'});assert.equal(go.started,true);assert.deepEqual(decided(F),['accept']);
   const still=await call('ask_chat',{request:'Let it continue.'});assert.equal(still.running,true);assert.deepEqual(decided(F),['accept'],'running: left alone');

   // A chat asked, then its to-do dismissed: when the chat stops, nothing is said about it (and not after a reopen either)
   await call('open_todo',{id:G});
   assert.equal((await call('ask_chat',{request:'Find the policy number in my email.'})).ok,true);
   assert.equal((await call('todo_action',{action:'dismiss',id:G})).ok,true);
   await page.waitForTimeout(4500);
   assert.ok(!(await told()).some(x=>/stopped/.test(x)),'a dismissed to-do says nothing');
   // One that stops on its own is told once, with its title and what was asked
   await call('open_todo',{id:E});
   assert.equal((await call('ask_chat',{request:'When is the invoice due?'})).ok,true);
   await page.waitForFunction(()=>window.__dc.sent.some(x=>x.item?.content?.[0]?.text?.includes('stopped before')),null,{timeout:12000});
   const stops=(await told()).filter(x=>/stopped before/.test(x));assert.equal(stops.length,1);assert.match(stops[0],/"Pay the plumber" stopped before it answered "When is the invoice due\?"/);

   // One odd word ("azk"): nothing changes, "say that again"; a clear request does
   await heard('u1','Azk.');await page.evaluate(()=>{__say({type:'response.created',response:{id:'ra'}})});
   const odd=await call('create_todo',{title:'Re-ask the question'},'ra');assert.match(odd.error,/wasn’t clear/);assert.match(odd.note,/say that again/);
   await page.evaluate(()=>__say({type:'response.done',response:{id:'ra',status:'completed'}}));
   assert.equal(actions.filter(x=>x.action==='card_new').length,0);
   await heard('u2','Add a to-do to call the plumber.');
   assert.equal((await call('create_todo',{title:'Call the plumber'})).ok,true);assert.equal(actions.filter(x=>x.action==='card_new').length,1);
   // A short "yes" the transcription was unsure of is kept; a few German words are dropped with "say that again"
   await heard('u3','Yes.',[{logprob:-3.5}]);await page.waitForFunction(()=>document.querySelector('#talk-view .talk-log').textContent.includes('Yes.'));
   await heard('u4','Ja, liebe den Movon.');await page.waitForFunction(()=>window.__dc.sent.some(x=>x.type==='conversation.item.delete'&&x.item_id==='u4'));
   assert.doesNotMatch(await log(),/Movon/);await page.waitForFunction(()=>window.__dc.sent.some(x=>x.item?.content?.[0]?.text?.startsWith('AGAIN:')),null,{timeout:5000});
   await heard('u5','Ja, doe maar.');await page.waitForFunction(()=>document.querySelector('#talk-view .talk-log').textContent.includes('doe maar'));
   // No dashes in what either side said
   await page.evaluate(()=>{__say({type:'response.created',response:{id:'rd'}});__say({type:'response.output_audio_transcript.done',response_id:'rd',item_id:'d1',transcript:'Dismissed—it’s gone.'});__say({type:'response.done',response:{id:'rd',status:'completed'}})});
   await page.waitForFunction(()=>document.querySelector('#talk-view .talk-log').textContent.includes('Dismissed, it’s gone.'));

   // Report a bug: Help's report (bug_send), what the owner said; the to-do and recent lines only when they agreed
   const bug=await call('report_bug',{summary:'Talk read the draft twice.'});assert.equal(bug.status,'sent');assert.match(bug.note,/Sent the bug report/);
   let sent=actions.filter(x=>x.action==='bug_send').at(-1).args;assert.equal(sent.description,'From Talk: Talk read the draft twice.');assert.equal(sent.diagnostics,false);
   await call('report_bug',{summary:'Talk read the draft twice.',context:true,support_report:true});
   sent=actions.filter(x=>x.action==='bug_send').at(-1).args;assert.match(sent.description,/To-do in focus: Pay the plumber/);assert.match(sent.description,/Last lines in Talk:\nOwner: /);assert.equal(sent.diagnostics,true);
   assert.equal(actions.filter(x=>x.action==='card_new').length,1,'a bug report is no to-do');
  }

  // A send by voice: Undo with its countdown in Talk; tapping Undo cancels every send of that yes
  await call('ask_to_send_all',{ids:[A,H]});
  assert.ok(await page.evaluate(()=>window.__dc.sent.some(x=>x.type==='session.update'&&x.session?.audio?.input?.turn_detection?.eagerness==='high')),'a lone yes ends the turn sooner');
  const queued=await call('send_answer');assert.equal(queued.status,'queued',JSON.stringify(queued));
  await page.waitForSelector(viewBar+' .talk-undo-btn');
  assert.match(await page.locator(viewBar+' .talk-sending').textContent(),/^Sending 2 emails in\u00a0\d+\u00a0s$/,'a batch: how many');
  const box=await page.locator(viewBar+' .talk-undo-btn').boundingBox();assert.ok(box.x>=0&&box.x+box.width<=w&&box.y>=0&&box.y+box.height<=h,'Undo on screen');
  assert.ok(box.height>=(phone?36:28),'a button to tap');
  await page.waitForTimeout(300);await shot('a1-talk-undo');
  await tap(viewBar+' .talk-undo-btn');
  await until(()=>actions.filter(x=>x.action==='talk_undo').length===2);
  assert.deepEqual(actions.filter(x=>x.action==='talk_undo').map(x=>x.args),[{suggestion_id:A,approval_id:'voice:1'},{suggestion_id:H,approval_id:'voice:2'}]);
  await page.waitForFunction(sel=>document.querySelector(sel+' .talk-sending')?.textContent==='Canceled. It won’t be sent.',viewBar);
  await shot('a2-talk-undone');
  if(full||SHOTS){   // every size and theme when taking screenshots
   // Said instead of tapped: undo_send; and once the time is up, Sent
   await call('open_todo',{id:A});const q1=await call('ask_to_send');const a1=await call('send_answer');assert.equal(a1.status,'queued',JSON.stringify([q1,a1]));
   const u=await call('undo_send');assert.equal(u.canceled,1);assert.equal(actions.filter(x=>x.action==='talk_undo').length,3);
   assert.match((await call('undo_send')).error,/Nothing is waiting/);
   await call('ask_to_send');assert.equal((await call('send_answer')).status,'queued');
   await page.waitForFunction(sel=>/^Sending to Dana in\u00a0\d+\u00a0s$/.test(document.querySelector(sel+' .talk-sending')?.textContent||''),viewBar);
   await shot('a4-talk-undo-one');
   await page.evaluate(()=>{window.__skew=11000});
   // After the window: Sending… until the outbox says it went out, then "Sent to Dana · 12:42" on the bar and the card,
   // and the voice is told once to say "Sent." (never the clock's guess)
   await page.waitForFunction(sel=>document.querySelector(sel+' .talk-sending.sent')?.textContent==='Sent to Dana · 12:42'&&!document.querySelector(sel+' .talk-undo-btn'),viewBar);
   assert.deepEqual(outbox.at(-1),{id:A,approval_id:'voice:1'});
   await page.waitForFunction(()=>document.querySelector('#talk-view .talk-about-sent')?.textContent==='Sent to Dana · 12:42');
   await page.waitForFunction(()=>window.__dc.sent.some(x=>x.item?.type==='message'&&/outbox confirms it went out \(Dana, at 12:42\)\. Say only: "Sent\."/.test(x.item.content[0].text)));
   await shot('a3-talk-sent');
   assert.match((await call('undo_send')).error,/Nothing is waiting/);
   await page.evaluate(()=>{window.__skew=0});
  }
  if(full){
   // A to-do's own Talk (the wave in its chat), Jeroen's payroll to-do: "mark this as done" heard as "Güzel." was taken
   // for a wrap-up. A word in a language the owner doesn't speak is dropped ("say that again"), is never a goodbye, and
   // "mark this as done" marks that to-do done itself; the chat stays open, with Talk.
   await tap(viewBar+' [data-talk-end]');await page.waitForFunction(()=>!document.querySelector('#talk-view .talk'));
   await page.evaluate(id=>{location.hash='#chat='+id},E);await page.waitForSelector('.chat-compose [data-talk]');
   await tap('.chat-compose [data-talk]');await page.waitForFunction(()=>document.querySelector('.chat-compose .talk .talk-live strong')?.textContent==='Live');
   await heard('g1','Güzel.');await page.evaluate(()=>__say({type:'response.created',response:{id:'rg'}}));
   await page.waitForFunction(()=>window.__dc.sent.some(x=>x.type==='conversation.item.delete'&&x.item_id==='g1'));
   const bye=await call('end_talk',{},'rg');assert.match(bye.error,/wasn’t clear/);
   await page.evaluate(()=>__say({type:'response.done',response:{id:'rg',status:'cancelled'}}));
   await page.waitForTimeout(600);assert.equal(await page.locator('.chat-compose .talk .talk-live strong').textContent(),'Live','still talking');
   assert.doesNotMatch(await page.locator('#chat-log').textContent(),/Güzel/);
   assert.deepEqual(await page.evaluate(()=>['Güzel.','Teşekkürler.','Send it to José.','Ja, dat is goed.','Thanks.'].map(x=>talkForeign(x,['en','nl']))),[true,true,false,false,false]);
   assert.equal(await page.evaluate(()=>talkForeign('Güzel.',['de'])),false,'ü is German');
   await heard('g2','Mark this as done.');
   const n0=decided(E).length,done=await call('todo_action',{action:'mark_done'});assert.equal(done.ok,true);
   assert.equal(decided(E).at(-1),'complete');assert.equal(decided(E).length,n0+1);
   await page.evaluate(()=>refresh());await page.waitForTimeout(500);
   assert.equal(await page.evaluate(()=>location.hash),'#chat='+E,'the chat stays open');
   assert.equal(await page.locator('.chat-compose .talk .talk-live strong').textContent(),'Live');
   const back=await call('undo_last_action');assert.equal(back.ok,true);assert.equal(decided(E).at(-1),'reopen');
  }
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('talk actions dashboard ok')}
finally{await browser?.close();server.close()}
