import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Talk (talk_live.py, the main conversation): Talk in the sidebar (the drawer on a phone) starts one live conversation
// about whatever needs the owner. Its bar floats at the bottom of the page, and sits in a to-do's chat when one is open.
// The voice lists every open to-do with its state (what needs the owner first), opens one (the screen follows), and works on the one on screen: the
// Machine is told which (talk_focus), and the send rules are those of a to-do's own Talk live. A to-do that comes in is
// mentioned at a pause, never while someone talks. OpenAI and the Machine are stand-ins, as in test_talk_live_dashboard.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),M='a7a7a7a7a7a7a7a7',D='d8d8d8d8d8d8d8d8',X='e9e9e9e9e9e9e9e9',A='a1a1a1a1a1a1a1a1',B='b2b2b2b2b2b2b2b2',C='c3c3c3c3c3c3c3c3',P='d4d4d4d4d4d4d4d4',Z='e5e5e5e5e5e5e5e5',N='f6f6f6f6f6f6f6f6';
const DRAFT={kind:'email',label:'Reply to Lotte',to:['lotte@example.com'],to_name:'Lotte',from:'me@example.com',subject:'Re: Paint order',body:'Hi Lotte, Thursday after two works. See you then.',revision:'r1',account_id:'mail'};
let cards;
const reset=()=>{cards=[{id:A,title:'Reply to Lotte about the paint order',body:'Lotte asked when the order can be picked up.',status:'prepared',scope:'personal',created_at:now,event_ids:[1],people:[{id:'p1',name:'Lotte'}],next_actions:[DRAFT]},
 {id:B,title:'Decide on the offsite venue',body:'Two venues offered.',status:'pending',scope:'personal',created_at:now,event_ids:[2]},
 {id:P,title:'Find a rug and table for the living room',body:'Looking at three shops.',status:'accepted',scope:'personal',created_at:now,event_ids:[4],people:[{id:'p3',name:'Juliana'}]},
 {id:D,title:'Pay the paint invoice',body:'Paid.',status:'completed',scope:'personal',created_at:now,event_ids:[6]},
 {id:Z,title:'Renew the parking permit',body:'Back on Monday.',status:'snoozed',snoozed_until:new Date(Date.now()+3*864e5).toISOString(),scope:'personal',created_at:now,event_ids:[5]}]};
let talkReady=true;
const state=()=>({talk_ready:talkReady,suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const actions=[],lines=[],sends=[],replies=[],relayed=[],voiced=[];let askedQ=null,focus=null,running=false;
const MAIN_TOOLS=['list_todos','open_todo','todo_details','find_todos','search','open_record','calendar','machine_status','ask_chat','create_todo','todo_action','ask_machine','ask_to_send','send_answer'].map(name=>({type:'function',name}));
// The Machine's read tools (talk_tool): what search, open_record and calendar answer
const LOOKUP={
 search:x=>x.kind==='meeting'?{found:[{id:'event:7',kind:'meeting',title:'Pilot review with Dana',what:'Calendar'}]}:{found:[{id:'email:dana@client.example',kind:'person',name:'Dana Reyes',about:'Head of Events at Client Example',last:'Tue 27 Oct 15:00'}]},
 open_record:x=>x.id==='event:7'?{id:'event:7',kind:'meeting',title:'Pilot review with Dana',when:'Thu 29 Oct 14:30',until:'15:15',where:'Zoom',with:['Dana Reyes'],card:{kind:'meeting',title:'Pilot review with Dana',line:'Thu 29 Oct 14:30 · Zoom',event:7}}
  :{id:x.id,kind:'person',name:'Dana Reyes',about:'Head of Events at Client Example',recent:['Asked about the offsite dates'],card:{kind:'person',title:'Dana Reyes',line:'Head of Events at Client Example',node:'email:dana@client.example'}},
 calendar:()=>({meetings:[{id:'event:7',title:'Pilot review with Dana',when:'Thu 29 Oct 14:30',until:'15:15',where:'Zoom',with:['Dana Reyes']}],from:'2026-10-29',days:1,count:1})};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);const a=r.args||{};
  const answer={
   talk_status:()=>({ready:true,limit:600,warn:540}),
   talk_start:()=>({id:'feedfeedfeedfeed',via:'signin',per_use:false,limit:a.main?1800:600,warn:a.main?1740:540,tools:MAIN_TOOLS,main:!!a.main,instructions:'You are The Machine, going through the to-dos.',voice:'cedar',speed:1.1,turn:{type:'semantic_vad',eagerness:'low'},turn:{type:'semantic_vad',eagerness:'low',create_response:true,interrupt_response:true},
    ask_note:'Drafts wait for Approve.',notes:{queued:'Joins.',done:'Done: "{answer}"',stopped:'Stopped.',new:'A new to-do needs the owner: "{title}" (from: {from}). At a natural pause, mention it.',ready:'A to-do that was preparing is ready now: "{title}" (from: {from}).'},ready:true}),
   card_new:()=>{const id=cards.some(c=>c.id===N)?M:N,made={id,title:a.text.split('\n')[0],body:a.text,status:'accepted',origin:'owner',scope:a.scope||'personal',created_at:new Date().toISOString(),event_ids:[9]};cards.push(made);return {id}},
   talk_offer:()=>({sdp:'v=0\r\nanswer\r\n'}),
   talk_focus:()=>{if(![...cards,{id:X}].some(c=>c.id===a.suggestion_id))return {__status:400,error:'Unknown suggestion'};focus=a.suggestion_id;askedQ=null;return {ok:true}},
   talk_line:()=>{lines.push({sid:focus,kind:a.role==='user'?'you':'reply',text:a.text,via:'live',at:Date.now()});return {ok:true}},
   talk_tool:()=>(LOOKUP[a.name]?{output:LOOKUP[a.name](a.args)}:focus===X?{output:{title:'Order the new desk chair',state:'dismissed',messages:[],drafts:[]}}:{output:focus?{title:cards.find(c=>c.id===focus).title,drafts:focus===A?[{kind:'email',to:DRAFT.to,subject:DRAFT.subject,body:DRAFT.body}]:[]}:{error:'No to-do is open. Call open_todo first.'}}),
   talk_end:()=>({ok:true}),
   talk_ask_send:()=>{if(focus!==A)return {error:'No draft ready to send by voice.'};askedQ=a.revision||'r1';return {question:'Send this reply to Lotte by email?',revision:askedQ,draft:{to:['Lotte'],how:'by email',subject:DRAFT.subject,text:DRAFT.body},say:'First read the draft below out in full. Ask exactly this: Send this reply to Lotte by email?'}},
   talk_send:()=>{if(!askedQ)return {status:'not_asked',say:'No confirm question is open.'};askedQ=null;
    sends.push({kind:'event',text:'Approved by voice',mine:true,undo_voice:'voice:1',undo_until:Date.now()+10000,at:Date.now()});
    return {status:'queued',approval_id:'voice:1',undo_seconds:10,say:'Approved.'}},
   decide:()=>{if(String(a.decision_id).startsWith('chat-talk-')){relayed.push({sid:a.suggestion_id,text:a.feedback});running=true}
    // ask_machine: its own new to-do's chat answers (the owner's words, shown as theirs)
    else if(String(a.decision_id).startsWith('chat-voice-')){voiced.push({sid:a.suggestion_id,text:a.feedback});replies.push({sid:a.suggestion_id,kind:'reply',text:'Trattoria Roma is open Friday until eleven.',at:Date.now()})}
    return a.choice==='snooze'?{ok:true,snoozed_until:'2026-10-30T08:00:00Z'}:{ok:true}},
   card_rename:()=>({ok:true}),
   card_chat:()=>({session:true,status:running&&a.suggestion_id!==M?'running':'done',active:running&&a.suggestion_id!==M,cursor:'k',items:[...replies.filter(x=>x.sid===a.suggestion_id),...(a.suggestion_id===M?[]:[{kind:'reply',text:'Ready for you.',...(a.suggestion_id===A?{drafts:[{kind:'email',to:['Lotte'],subject:DRAFT.subject,body:DRAFT.body,reply:true}]}:{}),at:Date.now()-60000}]),...lines.filter(l=>l.sid===a.suggestion_id),...(a.suggestion_id===A?sends:[])].sort((x,y)=>x.at-y.at)}),
  }[r.action];
  const out=answer?answer():{};if(out?.__status){res.statusCode=out.__status;delete out.__status}res.end(JSON.stringify(out));return}
 if(/^\/brand\/[\w.-]+\.(png|webp|woff2|svg)$/.test(url.pathname)){try{const f=await readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url));res.setHeader('Content-Type',{png:'image/png',webp:'image/webp',woff2:'font/woff2',svg:'image/svg+xml'}[url.pathname.split('.').pop()]);res.end(f)}catch{res.statusCode=404;res.end()}return}
 res.statusCode=200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const SHOTS=process.env.SHOT_DIR;

const FAKE_RTC=()=>{const real=Date.now;window.__skew=0;Date.now=()=>real()+window.__skew;
 navigator.mediaDevices.getUserMedia=async()=>{const ac=new AudioContext(),osc=ac.createOscillator(),dest=ac.createMediaStreamDestination();osc.connect(dest);osc.start();window.__stream=dest.stream;return dest.stream};
 window.RTCPeerConnection=class{constructor(){this.connectionState='new';window.__pc=this}
  addTrack(track){this.track=track}
  createDataChannel(label){const dc=window.__dc={label,readyState:'connecting',sent:[],send(x){this.sent.push(JSON.parse(x))},close(){this.readyState='closed'}};this.dc=dc;return dc}
  async createOffer(){return {type:'offer',sdp:'v=0\r\noffer\r\n'}}
  async setLocalDescription(d){this.local=d}
  async setRemoteDescription(d){this.remote=d;setTimeout(()=>{this.connectionState='connected';this.dc.readyState='open';this.dc.onopen?.()},60)}
  close(){this.connectionState='closed';window.__closed=(window.__closed||0)+1}};
 window.__say=e=>window.__dc.onmessage({data:JSON.stringify(e)})};

const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']});
 for(const [w,h,scheme] of [[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]){
  const phone=w<500,context=await browser.newContext({viewport:{width:w,height:h},isMobile:phone,hasTouch:phone,deviceScaleFactor:2,colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.addInitScript(FAKE_RTC);
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  reset();actions.length=0;lines.length=0;sends.length=0;replies.length=0;relayed.length=0;voiced.length=0;running=false;askedQ=null;focus=null;
  await page.goto('http://127.0.0.1:'+server.address().port+'/#');await page.waitForTimeout(400);
  const tag=`${w}-${scheme}`,shot=async n=>{if(SHOTS)await page.screenshot({path:`${SHOTS}/${n}-${tag}.png`})};
  const tap=sel=>phone?page.locator(sel).tap():page.locator(sel).click();
  const call=async(n,name,args={})=>{await page.evaluate(([n,name,args])=>__say({type:'response.function_call_arguments.done',call_id:n,name,arguments:JSON.stringify(args)}),[n,name,args]);
   await page.waitForFunction(n=>window.__dc.sent.some(x=>x.item?.call_id===n),n,{timeout:8000});return page.evaluate(n=>JSON.parse(window.__dc.sent.find(x=>x.item?.call_id===n).item.output),n)};
  const said=(item,text,role='user')=>page.evaluate(([item,text,role])=>{if(role==='user')__say({type:'conversation.item.input_audio_transcription.completed',item_id:item,transcript:text});
   else{__say({type:'response.created',response:{id:'r'+item}});__say({type:'response.output_audio_transcript.done',response_id:'r'+item,item_id:item,transcript:text});__say({type:'response.done',response:{id:'r'+item,status:'completed'}})}},[item,text,role]);
  const told=()=>page.evaluate(()=>window.__dc.sent.filter(x=>x.type==='conversation.item.create'&&x.item?.type==='message').map(x=>x.item.content[0].text));
  const dockBar='#talk-dock .talk',chatBar='.chat-compose .talk';

  const viewBar='#talk-view .talk-foot .talk',live=sel=>page.waitForFunction(sel=>document.querySelector(sel+' .talk-live strong')?.textContent==='Live',sel);
  const inView=()=>page.waitForFunction(()=>location.hash==='#talk'&&!document.querySelector('#talk-view').hidden);
  const ends=n=>page.waitForFunction(n=>window.__ends>=n,n).catch(()=>{});const ended=()=>actions.filter(a=>a.action==='talk_end').length;
  const until=async(f,ms=4000)=>{for(let i=0;i<ms/50&&!f();i++)await page.waitForTimeout(50);assert.ok(f())};

  // Talk shows in the sidebar once this Machine can talk live (in the drawer on a phone); it opens Talk's own view
  if(phone)await page.evaluate(()=>drawerOpen());
  await page.waitForSelector('#side-talk:not([hidden])');await page.waitForTimeout(300);
  await shot('m0-talk-in-the-sidebar');
  await tap('#side-talk');await inView();await live(viewBar);
  assert.equal(actions.find(a=>a.action==='talk_start').args.main,true);
  const setup=await page.evaluate(()=>window.__dc.sent[0]);
  assert.deepEqual(setup.session.tools.map(x=>x.name),MAIN_TOOLS.map(x=>x.name));
  assert.deepEqual(setup.session.audio.input.turn_detection,{type:'semantic_vad',eagerness:'low',create_response:true,interrupt_response:true});
  assert.equal(await page.locator('#side-talk').getAttribute('aria-pressed'),'true');
  assert.match(await page.locator('#talk-view .talk-log').textContent(),/Say something to start\./);
  await page.waitForTimeout(200);await shot('m1-talk-view');

  // Another page: the bar floats there, with End; Talk in the sidebar goes back to the view (it doesn't end)
  await page.evaluate(()=>document.querySelector('nav [data-tab="inbox"]').click());await live(dockBar);
  assert.notEqual(await page.evaluate(()=>location.hash),'#talk');
  await page.evaluate(()=>window.scrollTo(0,document.documentElement.scrollHeight));await page.waitForTimeout(200);
  const gap=await page.evaluate(()=>{const cards=[...document.querySelectorAll('#inbox .card')].filter(c=>c.checkVisibility()),dock=document.querySelector('#talk-dock').getBoundingClientRect();
   return [cards.at(-1),document.querySelector('.site-footer')].filter(Boolean).map(x=>dock.top-x.getBoundingClientRect().bottom)});
  for(const g of gap)assert.ok(g>=12,`the page ends ${g}px above the floating bar, under it`);
  await shot('m1b-talk-floating-scrolled');
  if(phone)await page.evaluate(()=>drawerOpen());
  await tap('#side-talk');await inView();await live(viewBar);assert.equal(ended(),0);

  // What needs the owner, in the dashboard's order: Ready first, then To decide
  // Every open to-do the lists show, with its state in plain words: what needs the owner first, then Preparing, Later
  const listed=await call('l1','list_todos');
  assert.deepEqual(listed.todos.map(x=>[x.id,x.state]),[[A,'ready'],[B,'to decide'],[P,'preparing'],[Z,'snoozed']]);
  assert.deepEqual(listed.counts,{ready:1,'to decide':1,preparing:1,snoozed:1});assert.equal(listed.count,4);
  assert.equal(listed.todos[0].from,'Lotte');
  // No send question yet: the bar has no "say yes" hint
  assert.equal(await page.locator(viewBar+' .talk-hint').textContent(),'');
  assert.match((await call('l2','ask_to_send')).error,/open_todo first/);
  // The voice opens one: the Machine is told, Talk's view shows it with its draft, the page stays where it is
  const opened=await call('o1','open_todo',{id:A});
  assert.equal(opened.title,'Reply to Lotte about the paint order');assert.equal(opened.drafts[0].body,DRAFT.body);
  assert.deepEqual(actions.find(a=>a.action==='talk_focus').args,{id:'feedfeedfeedfeed',suggestion_id:A});
  await page.waitForSelector('#talk-view .talk-about h3');
  assert.equal(await page.evaluate(()=>location.hash),'#talk','no jump into the to-do\'s chat');
  assert.equal(await page.locator('#talk-view .talk-about h3').textContent(),'Reply to Lotte about the paint order');
  assert.equal(await page.locator('#talk-view .talk-about [data-smart]').getAttribute('data-smart'),'r1');
  assert.match(await page.locator('#talk-view .talk-about .chat-draft').textContent(),/Thursday after two works/);
  assert.equal(await page.locator('.chat-compose .talk').count(),0);
  assert.match((await call('o2','open_todo',{id:'ffffffffffffffff'})).error,/No to-do with that id/);
  // One transcript, in Talk's view; the lines are kept for the to-do too
  await said('s1','Lotte wants to know when to pick up the paint. I drafted a reply. Want to hear it?','assistant');
  await said('s1b','Read it to me.');
  await page.waitForFunction(()=>document.querySelector('#talk-view .talk-log').textContent.includes('Read it to me.'));
  await until(()=>lines.length>=2);assert.equal(lines.at(-1).sid,A);
  assert.equal(await page.locator(viewBar+' .talk-hint').textContent(),'','a draft on screen, but nothing asked yet');
  await page.waitForTimeout(300);await shot('m2-talk-about-a-todo');
  if(phone){await page.evaluate(()=>drawerOpen());await page.waitForTimeout(400);await shot('m2a-the-lists-talk-sees');await page.evaluate(()=>drawerClose());await page.waitForTimeout(300)}

  // Sending by voice, from Talk's view: the same rules, about the draft it shows
  const q=await call('q1','ask_to_send');
  assert.equal(q.question,'Send this reply to Lotte by email?');
  await page.waitForFunction(sel=>document.querySelector(sel+' .talk-hint').textContent==='Say yes to send it.',viewBar);  // asked: the hint, until answered
  assert.equal(actions.find(a=>a.action==='talk_ask_send').args.revision,'r1');
  await said('s2','Send this reply to Lotte by email?','assistant');await said('s3','Yes, send it.');
  assert.equal((await call('q2','send_answer')).status,'queued');
  assert.equal(sends.length,1);assert.equal(await page.evaluate(()=>location.hash),'#talk');
  await page.waitForFunction(sel=>document.querySelector(sel+' .talk-hint').textContent==='',viewBar);

  // A change goes through the to-do's chat, which isn't open: its answer still comes back to the voice
  const asked=await call('c1','ask_chat',{request:'Make it Friday instead.'});
  assert.equal(asked.ok,true);await until(()=>relayed.length===1);assert.deepEqual(relayed[0],{sid:A,text:'Make it Friday instead.'});
  await page.waitForTimeout(1800);running=false;replies.push({sid:A,kind:'reply',text:'Changed it to Friday.',at:Date.now()});
  await page.waitForFunction(()=>window.__dc.sent.some(x=>x.item?.type==='message'&&x.item.content[0].text.includes('Changed it to Friday.')),null,{timeout:8000});
  await page.evaluate(()=>{__say({type:'response.created',response:{id:'told1'}});__say({type:'response.done',response:{id:'told1',status:'completed'}})});  // the voice told it

  // A new to-do comes in: a heads-up at the next pause, not while the owner talks
  const toldBefore=(await told()).length;
  await page.evaluate(()=>__say({type:'input_audio_buffer.speech_started'}));
  cards.push({id:C,title:'Pieter asks about pricing',body:'Pricing for 10 seats?',status:'pending',scope:'personal',created_at:new Date().toISOString(),event_ids:[3],people:[{id:'p2',name:'Pieter'}]});
  await page.evaluate(()=>refresh());await page.waitForTimeout(1200);
  assert.equal((await told()).length,toldBefore,'never while the owner talks');
  await page.evaluate(()=>__say({type:'input_audio_buffer.speech_stopped'}));
  await page.waitForFunction(n=>window.__dc.sent.filter(x=>x.type==='conversation.item.create'&&x.item?.type==='message').length>n,toldBefore,{timeout:6000});
  assert.deepEqual((await told()).slice(toldBefore),['A new to-do needs the owner: "Pieter asks about pricing" (from: Pieter). At a natural pause, mention it.']);
  await page.waitForTimeout(800);assert.equal((await told()).length,toldBefore+1,'once');

  // The one that was preparing is ready now: told once, as ready (not as a new one), and never again
  await page.evaluate(()=>{__say({type:'response.created',response:{id:'told2'}});__say({type:'response.done',response:{id:'told2',status:'completed'}})});  // the voice told it
  cards.find(c=>c.id===P).status='prepared';await page.evaluate(()=>refresh());
  await page.waitForFunction(n=>window.__dc.sent.filter(x=>x.type==='conversation.item.create'&&x.item?.type==='message').length>n,toldBefore+1,{timeout:6000});
  assert.deepEqual((await told()).slice(toldBefore+1),['A to-do that was preparing is ready now: "Find a rug and table for the living room" (from: Juliana).']);
  await page.evaluate(()=>refresh());await page.waitForTimeout(800);assert.equal((await told()).length,toldBefore+2,'once');

  // Something new while a to-do is in focus: a new to-do (New to-do's own card_new), not that to-do's chat
  const relayedBefore=relayed.length;
  const made=await call('n1','create_todo',{title:'Plan a trip to Antwerp',note:'A reminder'});
  assert.equal(made.ok,true);assert.equal(made.id,N);
  assert.deepEqual(actions.find(a=>a.action==='card_new').args,{text:'Plan a trip to Antwerp\nA reminder',scope:null,due:null,due_at:null,about:[],attach:[]});
  assert.equal(relayed.length,relayedBefore,'nothing handed to the to-do in focus');
  assert.equal(focus,A,'the focus stays');
  await page.waitForFunction(()=>[...document.querySelectorAll('#talk-view .talk-mark')].some(x=>x.textContent==='Added a to-do: Plan a trip to Antwerp'));
  assert.equal(await page.locator('#talk-view .talk-about h3').textContent(),'Reply to Lotte about the paint order');
  await page.evaluate(()=>refresh());await page.waitForTimeout(800);assert.equal((await told()).length,toldBefore+2,'the one it made is not announced');
  assert.match((await call('n2','create_todo',{title:'  '})).error,/Say what the to-do is/);
  await page.waitForTimeout(300);await shot('m2b-added-a-todo');

  // The rest of the Machine: a person and a meeting looked up and opened show as cards in the transcript; the to-do in
  // focus stays the same
  const focusBefore=actions.filter(a=>a.action==='talk_focus').length;
  assert.equal((await call('w1','search',{words:'Dana'})).found[0].id,'email:dana@client.example');
  const person=await call('w2','open_record',{id:'email:dana@client.example'});
  assert.equal(person.name,'Dana Reyes');assert.equal(person.card,undefined,'the card is the page\'s, not the voice\'s');
  await page.waitForSelector('#talk-view .talk-record a[href*="dana"]');
  assert.equal(await page.locator('#talk-view .talk-record').last().locator('.talk-record-kind').textContent(),'Person');
  await said('s4','Dana runs events at Client Example. You last talked on Tuesday.','assistant');
  await page.waitForTimeout(300);await shot('m5-looked-up-a-person');
  const day=await call('w3','calendar',{});assert.equal(day.meetings[0].id,'event:7');
  await call('w4','open_record',{id:'event:7'});
  await page.waitForSelector('#talk-view .talk-record [data-talk-event="7"][data-meeting]');
  assert.match(await page.locator('#talk-view .talk-record').last().textContent(),/^Meeting.*Pilot review with Dana.*Zoom/);
  await said('s5','Your pilot review with Dana is today at half past two, on Zoom.','assistant');
  await page.waitForTimeout(300);await shot('m6-looked-up-a-meeting');
  assert.equal(actions.filter(a=>a.action==='talk_focus').length,focusBefore,'the focus stays');
  assert.equal(await page.locator('#talk-view .talk-about h3').textContent(),'Reply to Lotte about the paint order');
  const status=await call('w5','machine_status');
  assert.deepEqual(Object.keys(status),['connections','reviews','needs_owner']);

  // Anything else: ask_machine makes its own to-do, hands the request to that chat (chat-voice-), and its answer
  // comes back to the voice; never the to-do in focus
  const toldNow=(await told()).length;
  const machine=await call('w6','ask_machine',{request:'Which Italian place near the office is open Friday night?'});
  assert.equal(machine.ok,true);
  assert.equal(actions.filter(a=>a.action==='card_new').at(-1).args.text,'Which Italian place near the office is open Friday night?');
  await until(()=>voiced.length===1);assert.deepEqual(voiced[0],{sid:M,text:'Which Italian place near the office is open Friday night?'});
  assert.equal(relayed.length,relayedBefore,'nothing handed to the to-do in focus');
  await page.waitForFunction(n=>window.__dc.sent.filter(x=>x.type==='conversation.item.create'&&x.item?.type==='message').length>n,toldNow,{timeout:8000});
  assert.equal((await told()).at(-1),'Done: "Trattoria Roma is open Friday until eleven."');
  await page.evaluate(()=>{__say({type:'response.created',response:{id:'told3'}});__say({type:'response.done',response:{id:'told3',status:'completed'}})});

  // A to-do's own buttons by voice (todo_action): the same decide and card_rename actions, never a send
  const decided=()=>actions.filter(a=>a.action==='decide').at(-1).args;
  assert.equal((await call('t1','todo_action',{action:'unsnooze',id:Z})).ok,true);assert.deepEqual([decided().suggestion_id,decided().choice],[Z,'accept']);
  assert.equal((await call('t2','todo_action',{action:'snooze',id:B,snooze:'3d'})).until,'2026-10-30T08:00:00Z');
  assert.deepEqual([decided().choice,decided().snooze_option],['snooze','3d']);
  await call('t3','todo_action',{action:'mark_done',id:B});assert.deepEqual([decided().suggestion_id,decided().choice],[B,'complete']);
  await call('t4','todo_action',{action:'dismiss',id:B,why:'Already booked'});assert.deepEqual([decided().choice,decided().feedback],['reject','Already booked']);
  await call('t5','todo_action',{action:'reopen',id:D});assert.deepEqual([decided().suggestion_id,decided().choice],[D,'reopen']);
  assert.match((await call('t6','todo_action',{action:'unsnooze',id:B})).error,/isn’t snoozed/);
  assert.match((await call('t7','todo_action',{action:'mark_done',id:D})).error,/closed/);
  await call('t8','todo_action',{action:'rename',title:'Reply to Lotte about the paint'});
  assert.deepEqual((({suggestion_id,title})=>({suggestion_id,title}))(actions.filter(a=>a.action==='card_rename').at(-1).args),{suggestion_id:A,title:'Reply to Lotte about the paint'});
  // A dismissed one the page hasn't loaded: it opens, and Reopen goes the Done / dismissed list's way
  const gone=await call('t9','open_todo',{id:X});assert.equal(gone.state,'dismissed');
  await page.waitForFunction(()=>[...document.querySelectorAll('#talk-view .talk-mark')].some(x=>x.textContent==='Order the new desk chair'));
  await call('t10','todo_action',{action:'reopen'});assert.deepEqual([decided().suggestion_id,decided().choice],[X,'reopen']);
  assert.equal(actions.filter(a=>a.action==='confirm_action').length,0,'never a send');
  await call('t11','open_todo',{id:A});

  // The to-do's own chat has what was said, decided and sent about it (Open the chat on the card); Back returns to Talk
  await tap('#talk-view .talk-about a[href^="#chat="]');
  await page.waitForFunction(id=>location.hash==='#chat='+id,A);await live('.chat-compose');
  await page.waitForFunction(()=>document.querySelector('#chat-log')?.textContent.includes('Approved by voice'));
  assert.match(await page.locator('#chat-log').textContent(),/Read it to me\./);
  assert.equal(ended(),0);
  await page.evaluate(()=>history.back());await inView();await live(viewBar);

  // The voice moves on to another to-do: the card changes, the page doesn't
  await call('o3','open_todo',{id:B});
  await page.waitForFunction(()=>document.querySelector('#talk-view .talk-about h3')?.textContent==='Decide on the offsite venue');
  assert.equal(await page.evaluate(()=>location.hash),'#talk');
  assert.equal(actions.filter(a=>a.action==='talk_focus').at(-1).args.suggestion_id,B);
  assert.equal(await page.locator('#talk-view .talk-mark',{hasText:'Decide on the offsite venue'}).count(),1);
  assert.equal(await page.locator('#talk-view .talk-about [data-smart]').count(),0,'no draft, nothing a yes could send');

  // Its own limit, on another page: a warning a minute before 30 minutes, then it ends
  await page.evaluate(()=>document.querySelector('nav [data-tab="inbox"]').click());await live(dockBar);
  await page.evaluate(()=>{window.__skew=1745000});
  await page.waitForFunction(()=>document.querySelector('#talk-dock .talk-live.near'));
  await shot('m3-one-minute-left');
  await page.evaluate(()=>{window.__skew=1801000});
  await page.waitForFunction(()=>!document.querySelector('#talk-dock'));
  // its toast, kept up so starting again is what clears it
  await page.waitForFunction(()=>{const t=document.getElementById('toast');if(!t.classList.contains('show')||!t.textContent.includes('Talk ends after 30 minutes'))return false;clearTimeout(toastTimer);return true});
  await until(()=>ended()===1);
  await page.evaluate(()=>{window.__skew=0});

  // The limit's toast is about that session only: gone once Talk starts again
  const limitToast=()=>page.evaluate(()=>{const t=document.getElementById('toast');return t.classList.contains('show')&&t.textContent.includes('30 minutes')});
  assert.equal(await limitToast(),true);
  if(phone)await page.evaluate(()=>drawerOpen());
  await tap('#side-talk');await inView();await live(viewBar);
  assert.equal(await limitToast(),false,'no limit toast once Talk starts again');

  // A goodbye ends it by itself (end_talk) once it has been heard; the goodbye stays in the transcript, no limit toast
  await said('s9','Thanks, that was all.');await page.waitForFunction(()=>document.querySelector('#talk-view .talk-log').textContent.includes('that was all'));
  await page.evaluate(()=>{__say({type:'response.created',response:{id:'bye'}});__say({type:'output_audio_buffer.started'});
   __say({type:'response.output_audio_transcript.done',response_id:'bye',item_id:'bye1',transcript:'Bye for now.'})});
  await call('e1','end_talk');await page.evaluate(()=>__say({type:'response.done',response:{id:'bye',status:'completed'}}));
  await page.waitForTimeout(1700);assert.equal(await page.locator(viewBar+' .talk-live strong').textContent(),'Live','not while the goodbye plays');
  await page.evaluate(()=>__say({type:'output_audio_buffer.stopped'}));
  await page.waitForFunction(()=>!document.querySelector('#talk-view .talk'));await until(()=>ended()===2);
  assert.equal(await page.locator('#side-talk').getAttribute('aria-pressed'),'false');
  assert.match(await page.locator('#talk-view .talk-log').textContent(),/that was all\..*Bye for now\..*Talk ended\./s);
  assert.equal(await limitToast(),false,'a goodbye is not the limit');
  const again=page.locator('#talk-view .talk-again-btn');
  assert.ok(await again.evaluate(b=>parseFloat(getComputedStyle(b).borderTopWidth)>0&&getComputedStyle(b).borderRadius!=='0px'),'Start again looks like a button');
  await page.waitForTimeout(200);await shot('m4-talk-ended');

  // Start again; End from Talk's view: the transcript stays, with Start again, and no limit toast
  await tap('#talk-view [data-talk-main]');await live(viewBar);
  await tap(viewBar+' [data-talk-end]');await page.waitForFunction(()=>!document.querySelector('#talk-view .talk'));
  await until(()=>ended()===3);
  assert.match(await page.locator('#talk-view .talk-log').textContent(),/Talk ended\./);
  assert.equal(await limitToast(),false,'End is not the limit');

  // T, like N for New to-do: shown on the row on a computer (not in the phone drawer), starts Talk, and ends it while live
  if(phone){await page.evaluate(()=>drawerOpen());assert.equal(await page.locator('#side-talk kbd').isVisible(),false,'no key hint on a phone');await page.evaluate(()=>drawerClose())}
  else{assert.equal(await page.locator('#side-talk kbd').textContent(),'T');assert.equal(await page.locator('#side-talk kbd').isVisible(),true)
   await page.evaluate(()=>document.querySelector('nav [data-tab="inbox"]').click());
   const starts=()=>actions.filter(a=>a.action==='talk_start').length,n=starts();
   await page.locator('#side-find').focus();await page.keyboard.press('t');await page.waitForTimeout(200);
   assert.equal(starts(),n,'T while typing types a t');assert.equal(await page.locator('#side-find').inputValue(),'t');
   await page.locator('#side-find').fill('');await page.evaluate(()=>document.activeElement.blur());
   for(const k of ['Control+t','Alt+t'])await page.keyboard.press(k);await page.waitForTimeout(200);assert.equal(starts(),n,'not with Ctrl or Alt held');
   await page.keyboard.press('t');await inView();await live(viewBar);
   assert.equal(actions.filter(a=>a.action==='talk_start').at(-1).args.main,true);
   await page.keyboard.press('t');await page.waitForFunction(()=>!document.querySelector('#talk-view .talk'));
   await until(()=>ended()===4);}
  await context.close()}
 // In the background (a phone's lock screen, another tab): the screen stays on, the lock screen has Mute and End, and
 // what timers did runs on the voice's own events, so slowed-down timers don't hold it up. Back on screen it checks the
 // connection is still there; one that went away while hidden ends cleanly and says so.
 {const BACKGROUND=()=>{window.__wakes=[];Object.defineProperty(navigator,'wakeLock',{value:{request:async kind=>{const l={kind,released:false,release:async()=>{l.released=true}};window.__wakes.push(l);return l}}});
   const ms={handlers:{},metadata:null,playbackState:'none',setActionHandler(n,f){if(n==='hangup'||n==='togglemicrophone')throw new TypeError('not supported here');if(f)this.handlers[n]=f;else delete this.handlers[n]},setMicrophoneActive(on){this.mic=on}};
   Object.defineProperty(navigator,'mediaSession',{value:ms});window.__hidden=false;
   Object.defineProperty(document,'hidden',{get:()=>window.__hidden});Object.defineProperty(document,'visibilityState',{get:()=>window.__hidden?'hidden':'visible'});
   window.__show=hidden=>{window.__hidden=hidden;document.dispatchEvent(new Event('visibilitychange'))};
   // throttled timers: while frozen, nothing a timer would do happens
   const si=window.setInterval,st=window.setTimeout;window.setInterval=(f,ms,...a)=>si(()=>{if(!window.__frozen)f(...a)},ms);
   window.setTimeout=(f,ms,...a)=>st(function run(){if(window.__frozen)return st(run,50);if(typeof f==='function')f(...a)},ms)};
  reset();actions.length=0;focus=null;
  const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.addInitScript(FAKE_RTC);await context.addInitScript(BACKGROUND);
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#');await page.waitForTimeout(400);
  const live=()=>page.waitForFunction(()=>document.querySelector('#talk-view .talk-live strong')?.textContent==='Live');
  const start=async()=>{await page.evaluate(()=>talkMain());await live()};
  const ended=()=>page.waitForFunction(()=>!document.querySelector('#talk-view .talk'),null,{timeout:3000});
  await start();
  assert.deepEqual(await page.evaluate(()=>window.__wakes.map(l=>[l.kind,l.released])),[['screen',false]],'the screen stays on while live');
  const media=()=>page.evaluate(()=>({title:navigator.mediaSession.metadata?.title,artist:navigator.mediaSession.metadata?.artist,art:navigator.mediaSession.metadata?.artwork?.[0]?.src||'',
   state:navigator.mediaSession.playbackState,mic:navigator.mediaSession.mic,handlers:Object.keys(navigator.mediaSession.handlers).sort()}));
  let m=await media();
  assert.deepEqual([m.title,m.artist,m.state,m.mic,m.handlers],['Talk','The Machine','playing',true,['pause','play','stop']]);assert.match(m.art,/app-icon-192\.png$/);
  assert.equal(await page.evaluate(()=>talk.audio.isConnected&&talk.audio.autoplay),true,'an audio element plays the voice');
  // The lock screen's pause is Mute, play unmutes; the bar follows
  await page.evaluate(()=>navigator.mediaSession.handlers.pause());
  assert.equal(await page.evaluate(()=>window.__stream.getAudioTracks()[0].enabled),false);m=await media();assert.deepEqual([m.state,m.mic],['paused',false]);
  assert.equal(await page.locator('#talk-view [data-talk-mute]').textContent(),'Unmute');
  await page.evaluate(()=>navigator.mediaSession.handlers.play());assert.equal(await page.evaluate(()=>window.__stream.getAudioTracks()[0].enabled),true);
  // Hidden and back: the wake lock the browser let go is taken again
  await page.evaluate(()=>{__show(true);window.__wakes[0].released=true;__show(false)});
  await page.waitForFunction(()=>window.__wakes.length===2);
  // Timers frozen: a goodbye still ends it once heard, on the voice's own events
  await page.evaluate(()=>{window.__frozen=true;__say({type:'response.created',response:{id:'bye'}});__say({type:'output_audio_buffer.started'});
   __say({type:'response.output_audio_transcript.done',response_id:'bye',item_id:'bye1',transcript:'Bye for now.'});
   __say({type:'response.function_call_arguments.done',call_id:'e1',name:'end_talk',arguments:'{}'});
   __say({type:'response.done',response:{id:'bye',status:'completed'}})});
  await page.waitForTimeout(400);assert.equal(await page.locator('#talk-view .talk').count(),1,'not while the goodbye plays');
  await page.evaluate(()=>__say({type:'output_audio_buffer.stopped'}));await ended();
  m=await media();assert.deepEqual([m.title,m.state,m.handlers],[undefined,'none',[]]);
  assert.equal(await page.evaluate(()=>window.__wakes.every(l=>l.released)),true,'the screen lock is let go');
  // Timers frozen: the 30 minutes count from the clock, checked on the next event or when the page shows again
  await page.evaluate(()=>{window.__frozen=false});await start();
  await page.evaluate(()=>{window.__frozen=true;__show(true);window.__skew=1801000;__show(false)});await ended();
  await page.waitForFunction(()=>document.getElementById('toast').textContent.includes('Talk ends after 30 minutes'));
  await page.evaluate(()=>{window.__frozen=false;window.__skew=0});await start();
  await page.evaluate(()=>{window.__frozen=true;window.__skew=1801000;__say({type:'response.done',response:{id:'x',status:'completed'}})});await ended();
  // The connection went away while hidden: back on screen it ends cleanly, says so, with Start again
  await page.evaluate(()=>{window.__frozen=false;window.__skew=0});await start();
  await page.evaluate(()=>{__show(true);window.__pc.connectionState='failed'});await page.waitForTimeout(200);
  assert.equal(await page.locator('#talk-view .talk').count(),1);
  await page.evaluate(()=>__show(false));await ended();
  await page.waitForFunction(()=>document.getElementById('toast').textContent==='Talk stopped while in the background.');
  assert.equal(await page.locator('#talk-view .talk-again-btn').count(),1,'Start again');
  // An iPhone stops the microphone when the app leaves the screen: the same clean end
  await start();
  await page.evaluate(()=>{__show(true);window.__stream.getAudioTracks()[0].dispatchEvent(new Event('ended'))});await ended();
  await page.evaluate(()=>__show(false));
  await page.waitForFunction(()=>document.getElementById('toast').textContent==='Talk stopped while in the background.');
  if(SHOTS)await page.screenshot({path:`${SHOTS}/m7-stopped-in-the-background-390-light.png`});
  await context.close()}
 // Without OpenAI (the page's status says so): no Talk
 talkReady=false;reset();actions.length=0;
 {const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});await context.addInitScript(FAKE_RTC);
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#');await page.waitForTimeout(800);
  assert.equal(await page.locator('#side-talk').isVisible(),false,'no OpenAI, no Talk');
  assert.equal(actions.filter(a=>a.action==='talk_status').length,0,'known from the page status, never asked separately');
  await page.keyboard.press('t');await page.waitForTimeout(400);
  assert.equal(actions.filter(a=>a.action==='talk_start').length,0,'T does nothing without Talk live');
  assert.equal(await page.locator('#talk-dock').count(),0,'and no floating bar');
  if(SHOTS)await page.screenshot({path:`${SHOTS}/m4-no-talk-live-1440-light.png`});
  // Talk live becomes ready: Talk shows with the page's next status, no reload
  talkReady=true;await page.evaluate(()=>refresh());await page.waitForSelector('#side-talk:not([hidden])');
  assert.equal(await page.locator('#side-talk kbd').isVisible(),true);
  await page.keyboard.press('t');await page.waitForFunction(()=>document.querySelector('#talk-view .talk-live strong')?.textContent==='Live');
  await page.keyboard.press('t');await page.waitForFunction(()=>!document.querySelector('#talk-view .talk'));
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('talk main dashboard ok');
}finally{await browser?.close();server.close()}
