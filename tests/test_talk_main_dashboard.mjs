import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Talk (talk_live.py, the main conversation): Talk in the sidebar (the drawer on a phone) starts one live conversation
// about whatever needs the owner. Its bar floats at the bottom of the page, and sits in a to-do's chat when one is open.
// The voice lists what's Ready and To decide, opens one (the screen follows), and works on the one on screen: the
// Machine is told which (talk_focus), and the send rules are those of a to-do's own Talk live. A to-do that comes in is
// mentioned at a pause, never while someone talks. OpenAI and the Machine are stand-ins, as in test_talk_live_dashboard.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString(),A='a1a1a1a1a1a1a1a1',B='b2b2b2b2b2b2b2b2',C='c3c3c3c3c3c3c3c3';
const DRAFT={kind:'email',label:'Reply to Lotte',to:['lotte@example.com'],to_name:'Lotte',from:'me@example.com',subject:'Re: Paint order',body:'Hi Lotte, Thursday after two works. See you then.',revision:'r1',account_id:'mail'};
let cards;
const reset=()=>{cards=[{id:A,title:'Reply to Lotte about the paint order',body:'Lotte asked when the order can be picked up.',status:'prepared',scope:'personal',created_at:now,event_ids:[1],people:[{id:'p1',name:'Lotte'}],next_actions:[DRAFT]},
 {id:B,title:'Decide on the offsite venue',body:'Two venues offered.',status:'pending',scope:'personal',created_at:now,event_ids:[2]}]};
let talkReady=true;
const state=()=>({talk_ready:talkReady,suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const actions=[],lines=[],sends=[];let askedQ=null,focus=null;
const MAIN_TOOLS=['list_todos','open_todo','todo_details','find_todos','ask_chat','ask_to_send','send_answer'].map(name=>({type:'function',name}));
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);const a=r.args||{};
  const answer={
   talk_status:()=>({ready:true,limit:600,warn:540}),
   talk_start:()=>({id:'feedfeedfeedfeed',via:'signin',per_use:false,limit:a.main?1800:600,warn:a.main?1740:540,tools:MAIN_TOOLS,main:!!a.main,instructions:'You are The Machine, going through the to-dos.',voice:'cedar',speed:0.95,
    ask_note:'Drafts wait for Approve.',notes:{queued:'Joins.',done:'Done: "{answer}"',stopped:'Stopped.',new:'A new to-do needs the owner: "{title}" (from: {from}). At a natural pause, mention it.'},ready:true}),
   talk_offer:()=>({sdp:'v=0\r\nanswer\r\n'}),
   talk_focus:()=>{focus=a.suggestion_id;askedQ=null;return {ok:true}},
   talk_line:()=>{lines.push({sid:focus,kind:a.role==='user'?'you':'reply',text:a.text,via:'live',at:Date.now()});return {ok:true}},
   talk_tool:()=>({output:focus?{title:cards.find(c=>c.id===focus).title,drafts:focus===A?[{kind:'email',to:DRAFT.to,subject:DRAFT.subject,body:DRAFT.body}]:[]}:{error:'No to-do is open. Call open_todo first.'}}),
   talk_end:()=>({ok:true}),
   talk_ask_send:()=>{if(focus!==A)return {error:'No draft ready to send by voice.'};askedQ=a.revision;return {question:'Send this reply to Lotte by email?',read_aloud:a.read_aloud,say:'Ask exactly this: Send this reply to Lotte by email?'}},
   talk_send:()=>{if(!askedQ)return {status:'not_asked',say:'No confirm question is open.'};askedQ=null;
    sends.push({kind:'event',text:'Approved by voice',mine:true,undo_voice:'voice:1',undo_until:Date.now()+10000,at:Date.now()});
    return {status:'queued',approval_id:'voice:1',undo_seconds:10,say:'Approved.'}},
   card_chat:()=>({session:true,status:'done',active:false,cursor:'k',items:[{kind:'reply',text:'Ready for you.',...(a.suggestion_id===A?{drafts:[{kind:'email',to:['Lotte'],subject:DRAFT.subject,body:DRAFT.body,reply:true}]}:{}),at:Date.now()-60000},...lines.filter(l=>l.sid===a.suggestion_id),...(a.suggestion_id===A?sends:[])].sort((x,y)=>x.at-y.at)}),
  }[r.action];
  res.end(JSON.stringify(answer?answer():{}));return}
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
  reset();actions.length=0;lines.length=0;sends.length=0;askedQ=null;focus=null;
  await page.goto('http://127.0.0.1:'+server.address().port+'/#');await page.waitForTimeout(400);
  const tag=`${w}-${scheme}`,shot=async n=>{if(SHOTS)await page.screenshot({path:`${SHOTS}/${n}-${tag}.png`})};
  const tap=sel=>phone?page.locator(sel).tap():page.locator(sel).click();
  const call=async(n,name,args={})=>{await page.evaluate(([n,name,args])=>__say({type:'response.function_call_arguments.done',call_id:n,name,arguments:JSON.stringify(args)}),[n,name,args]);
   await page.waitForFunction(n=>window.__dc.sent.some(x=>x.item?.call_id===n),n,{timeout:8000});return page.evaluate(n=>JSON.parse(window.__dc.sent.find(x=>x.item?.call_id===n).item.output),n)};
  const said=(item,text,role='user')=>page.evaluate(([item,text,role])=>{if(role==='user')__say({type:'conversation.item.input_audio_transcription.completed',item_id:item,transcript:text});
   else{__say({type:'response.created',response:{id:'r'+item}});__say({type:'response.output_audio_transcript.done',response_id:'r'+item,item_id:item,transcript:text});__say({type:'response.done',response:{id:'r'+item,status:'completed'}})}},[item,text,role]);
  const told=()=>page.evaluate(()=>window.__dc.sent.filter(x=>x.type==='conversation.item.create'&&x.item?.type==='message').map(x=>x.item.content[0].text));
  const dockBar='#talk-dock .talk',chatBar='.chat-compose .talk';

  // Talk shows in the sidebar once this Machine can talk live (in the drawer on a phone)
  if(phone)await page.evaluate(()=>drawerOpen());
  await page.waitForSelector('#side-talk:not([hidden])');await page.waitForTimeout(300);
  await shot('m0-talk-in-the-sidebar');
  await tap('#side-talk');
  await page.waitForFunction(()=>document.querySelector('#talk-dock .talk-live strong')?.textContent==='Live');
  assert.deepEqual(actions.find(a=>a.action==='talk_start').args,{main:true});
  const setup=await page.evaluate(()=>window.__dc.sent[0]);
  assert.deepEqual(setup.session.tools.map(x=>x.name),MAIN_TOOLS.map(x=>x.name));
  assert.equal(await page.locator('#side-talk').getAttribute('aria-pressed'),'true');
  await page.waitForTimeout(200);await shot('m1-talk-floating');

  // What needs the owner, in the dashboard's order: Ready first, then To decide
  const listed=await call('l1','list_todos');
  assert.deepEqual(listed.todos.map(x=>[x.id,x.list]),[[A,'Ready'],[B,'To decide']]);
  assert.equal(listed.todos[0].from,'Lotte');
  // Before one is open, nothing can be asked or sent
  assert.match((await call('l2','ask_to_send')).error,/open_todo first/);
  // The voice opens one: the screen follows, the Machine is told, the bar moves into that chat
  const opened=await call('o1','open_todo',{id:A});
  assert.equal(opened.title,'Reply to Lotte about the paint order');assert.equal(opened.drafts[0].body,DRAFT.body);
  await page.waitForFunction(id=>location.hash==='#chat='+id,A);
  assert.deepEqual(actions.find(a=>a.action==='talk_focus').args,{id:'feedfeedfeedfeed',suggestion_id:A});
  await page.waitForSelector(chatBar+' .talk-bar');assert.equal(await page.locator('#talk-dock').count(),0);
  assert.match((await call('o2','open_todo',{id:'ffffffffffffffff'})).error,/No to-do with that id/);
  // Lines are kept for the to-do on screen
  await said('s1','Lotte wants to know when to pick up the paint. I drafted a reply. Want to hear it?','assistant');
  await page.waitForFunction(()=>document.querySelector('#chat-log').textContent.includes('Want to hear it?'));
  assert.equal(lines.at(-1).sid,A);
  await page.waitForTimeout(300);await shot('m2-the-todo-on-screen');

  // Sending by voice: the same rules, about the draft on screen
  await page.waitForSelector('#chat-log .chat-draft.current [data-smart]');
  const q=await call('q1','ask_to_send');
  assert.equal(q.question,'Send this reply to Lotte by email?');
  assert.equal(actions.find(a=>a.action==='talk_ask_send').args.revision,'r1');
  await said('s2','Send this reply to Lotte by email?','assistant');await said('s3','Yes, send it.');
  assert.equal((await call('q2','send_answer')).status,'queued');
  await page.waitForFunction(()=>document.querySelector('#chat-log').textContent.includes('Approved by voice'));
  assert.equal(sends.length,1);

  // A new to-do comes in: a heads-up at the next pause, not while the owner talks
  await page.evaluate(()=>__say({type:'input_audio_buffer.speech_started'}));
  cards.push({id:C,title:'Pieter asks about pricing',body:'Pricing for 10 seats?',status:'pending',scope:'personal',created_at:new Date().toISOString(),event_ids:[3],people:[{id:'p2',name:'Pieter'}]});
  await page.evaluate(()=>refresh());await page.waitForTimeout(1200);
  assert.equal((await told()).length,0,'never while the owner talks');
  await page.evaluate(()=>__say({type:'input_audio_buffer.speech_stopped'}));
  await page.waitForFunction(()=>window.__dc.sent.some(x=>x.item?.type==='message'),null,{timeout:6000});
  assert.deepEqual(await told(),['A new to-do needs the owner: "Pieter asks about pricing" (from: Pieter). At a natural pause, mention it.']);
  await page.waitForTimeout(800);assert.equal((await told()).length,1,'once');

  // The owner opens another to-do themselves: Talk follows (it doesn't end)
  await page.evaluate(id=>chatGo(id),B);
  await page.waitForFunction(()=>document.querySelector('.chat-compose .talk-live strong')?.textContent==='Live');
  assert.equal(actions.filter(a=>a.action==='talk_focus').at(-1).args.suggestion_id,B);
  assert.equal(actions.filter(a=>a.action==='talk_end').length,0);
  // Leaving the chat: the bar floats again, still live
  await page.evaluate(()=>history.replaceState(null,'','#'));await page.evaluate(()=>dispatchEvent(new HashChangeEvent('hashchange')));
  await page.waitForSelector(dockBar+' .talk-bar');
  assert.equal(actions.filter(a=>a.action==='talk_end').length,0);

  // Its own limit: a warning a minute before 30 minutes, then it ends
  await page.evaluate(()=>{window.__skew=1745000});
  await page.waitForFunction(()=>document.querySelector('#talk-dock .talk-live.near'));
  await shot('m3-one-minute-left');
  await page.evaluate(()=>{window.__skew=1801000});
  await page.waitForFunction(()=>!document.querySelector('#talk-dock'));
  await page.waitForFunction(()=>document.body.textContent.includes('Talk ends after 30 minutes'));
  for(let i=0;i<40&&actions.filter(a=>a.action==='talk_end').length<1;i++)await page.waitForTimeout(50);
  assert.equal(actions.filter(a=>a.action==='talk_end').length,1);
  await page.evaluate(()=>{window.__skew=0});

  // Talk again, and End from the floating bar
  if(phone)await page.evaluate(()=>drawerOpen());
  await tap('#side-talk');await page.waitForFunction(()=>document.querySelector('#talk-dock .talk-live strong')?.textContent==='Live');
  await tap(dockBar+' [data-talk-end]');await page.waitForFunction(()=>!document.querySelector('#talk-dock'));
  for(let i=0;i<40&&actions.filter(a=>a.action==='talk_end').length<2;i++)await page.waitForTimeout(50);
  assert.equal(actions.filter(a=>a.action==='talk_end').length,2);
  assert.equal(await page.locator('#side-talk').getAttribute('aria-pressed'),'false');
  await context.close()}
 // Without OpenAI (the page's status says so): no Talk
 talkReady=false;reset();actions.length=0;
 {const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});await context.addInitScript(FAKE_RTC);
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#');await page.waitForTimeout(800);
  assert.equal(await page.locator('#side-talk').isVisible(),false,'no OpenAI, no Talk');
  assert.equal(actions.filter(a=>a.action==='talk_status').length,0,'known from the page status, never asked separately');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('talk main dashboard ok');
}finally{await browser?.close();server.close()}
