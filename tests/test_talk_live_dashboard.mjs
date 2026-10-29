import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Talk live (talk_live.py): the wave next to the mic in a to-do's chat starts a spoken conversation. The bar shows Live,
// the clock, Mute and End; a minute before 10 minutes it warns, and at 10 it ends. What both sides say lands in the chat.
// What it is asked to do goes to the chat as a typed message would. A spoken yes sends only the draft on screen, after
// the voice asked about it, and only when the Machine (talk_send, stubbed here) judged it a yes. OpenAI is a
// stand-in here: a fake microphone, RTCPeerConnection and data channel (window.__dc), and the Machine's answers are
// the fixture server's, so the test never needs a microphone, a key or the network.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString(),id='c1c1c1c1c1c1c1c1';
const cards=[{id,title:'Reply to Lotte about the paint order',body:'Lotte asked when the order can be picked up.',status:'prepared',scope:'personal',created_at:now,event_ids:[1]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const DRAFT={kind:'email',label:'Reply to Lotte',to:['lotte@example.com'],to_name:'Lotte',from:'me@example.com',subject:'Re: Paint order',body:'Hi Lotte, Thursday after two works. See you then.',revision:'r1',account_id:'mail'};
const actions=[],lines=[],asked=[],sends=[];let running=false,ready=true,askedQ=null,verdict='queued',perUse=true,demo=false,startFails=false,hold=null;
const TOOLS=[{type:'function',name:'todo_details'},{type:'function',name:'find_todos'},{type:'function',name:'ask_chat'}];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);const a=r.args||{};
  if(demo&&r.action.startsWith('talk_')){res.end(JSON.stringify({ok:true,demo:true}));return}
  const answer={
   talk_status:()=>({ready,limit:600,warn:540}),
   talk_start:()=>startFails?null:{id:'feedfeedfeedfeed',via:perUse?'key':'signin',per_use:perUse,limit:600,warn:540,tools:TOOLS,instructions:'You are The Machine, talking live.',ask_note:'Drafts wait for Approve.',notes:{queued:'Joins the last request.',done:'The chat finished. Its answer: "{answer}" Tell the owner now.',stopped:'The chat stopped.'},ready:true},
   talk_offer:()=>({sdp:'v=0\r\nanswer\r\n'}),
   talk_line:()=>{lines.push({kind:a.role==='user'?'you':'reply',text:a.text,via:'live',at:Date.now()});return {ok:true}},
   talk_tool:()=>({output:{title:cards[0].title,messages:[{from:'Lotte',text:'When can I pick it up?'}]}}),
   talk_end:()=>({ok:true}),
   // The Machine's side of a voice approval: the question it keeps, and its verdict on the owner's answer
   talk_ask_send:()=>{askedQ=a.revision;return {question:'Send this reply to Lotte by email?',read_aloud:a.read_aloud,draft:{to:'Lotte',how:'by email',subject:'',text:cards[0].next_actions?.[0]?.body},say:'Ask exactly this: Send this reply to Lotte by email?'}},
   talk_send:()=>{if(!askedQ)return {status:'not_asked',say:'No confirm question is open.'};const q=askedQ;askedQ=null;
    if(verdict!=='queued')return {status:verdict,say:'Not sent.'};
    sends.push({kind:'event',text:'Approved by voice',mine:true,undo_voice:'voice:1',undo_until:Date.now()+10000,at:Date.now()},{kind:'event',text:'Sending to Lotte…',mine:true,at:Date.now()+1});
    return {status:'queued',approval_id:'voice:1',revision:q,undo_seconds:10,say:'Approved.'}},
   talk_undo:()=>{sends.splice(0,sends.length,{kind:'event',text:'Send canceled',mine:true,at:Date.now()});return {status:'cancelled'}},
   // As the chat does: a hand-off from Talk live (chat-talk-…) never shows as the owner's message; the turn runs
   // until the test finishes it (done())
   decide:()=>{if(!String(a.decision_id).startsWith('chat-talk-'))asked.push({kind:'you',text:a.feedback,at:Date.now()});running=true;return {ok:true}},
   card_chat:()=>({session:true,status:running?'running':'done',active:running,cursor:'k',items:[{kind:'reply',text:'Lotte asked when the order can be picked up. Want me to answer her?',at:Date.now()-60000},...lines,...asked,...sends].sort((x,y)=>x.at-y.at)}),
  }[r.action];
  if(r.action==='talk_offer'&&hold)await hold;
  if(r.action==='talk_start'&&startFails){res.statusCode=400;res.end(JSON.stringify({error:'Talk live couldn’t start. Check OpenAI in OpenClaw, then try again.'}));return}
  res.end(JSON.stringify(answer?answer():{}));return}
 if(/^\/brand\/[\w.-]+\.(png|webp|woff2|svg)$/.test(url.pathname)){try{const f=await readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url));res.setHeader('Content-Type',{png:'image/png',webp:'image/webp',woff2:'font/woff2',svg:'image/svg+xml'}[url.pathname.split('.').pop()]);res.end(f)}catch{res.statusCode=404;res.end()}return}
 res.statusCode=200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const SHOTS=process.env.SHOT_DIR;

// A microphone, a peer connection and its data channel that need no device and no OpenAI. __say(event) is OpenAI
// talking on the data channel; __dc.sent is what the page told it. Date.now can be moved on (__skew) to the limit.
const FAKE_RTC=()=>{const real=Date.now;window.__skew=0;Date.now=()=>real()+window.__skew;window.__mic={mode:'ok'};
 navigator.mediaDevices.getUserMedia=async()=>{if(window.__mic.mode==='denied')throw new DOMException('Permission denied','NotAllowedError');
  const ac=new AudioContext(),osc=ac.createOscillator(),dest=ac.createMediaStreamDestination();osc.connect(dest);osc.start();window.__stream=dest.stream;return dest.stream};
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
  const base='http://127.0.0.1:'+server.address().port+'/';
  actions.length=0;lines.length=0;asked.length=0;sends.length=0;askedQ=null;running=false;verdict='queued';perUse=true;delete cards[0].next_actions;
  await page.goto(base+'#chat='+id);await page.locator('#chat-input').waitFor();
  const tag=`${w}-${scheme}`,shot=async n=>{if(SHOTS)await page.screenshot({path:`${SHOTS}/${n}-${tag}.png`})};
  const tap=sel=>phone?page.locator(sel).tap():page.locator(sel).click();
  const sent=()=>actions.filter(a=>a.action==='decide').length;
  const wave='.chat-compose [data-talk]',bar='.chat-compose .talk';

  // Idle: the wave sits next to the mic once the Machine says Talk live can start
  await page.waitForSelector(wave+':not([hidden])');
  const t=await page.locator(wave).boundingBox(),m=await page.locator('.chat-compose [data-mic]').boundingBox();
  assert.ok(t.width>=32&&t.x>m.x&&Math.abs(t.y-m.y)<2,'the wave is where Send goes, after the mic: '+JSON.stringify({t,m}));
  assert.equal(await page.locator('.chat-compose [data-chat-send]').isVisible(),false,'an empty box: the wave instead of Send');
  await page.locator('#chat-input').fill('A typed question');
  assert.ok(await page.locator('.chat-compose [data-chat-send]').isVisible(),'something typed: Send is back');
  assert.equal(await page.locator(wave).isVisible(),false);
  await page.locator('#chat-input').fill('');
  await shot('t1-idle');

  // Tap: Connecting… while the Machine hands the offer on, then Live with the clock
  let release;hold=new Promise(r=>release=r);
  await tap(wave);await page.waitForSelector(bar+' .talk-bar');
  await page.waitForFunction(()=>document.querySelector('.chat-compose .talk-live strong')?.textContent==='Connecting…');
  await shot('t2-connecting');release();hold=null;
  await page.waitForFunction(()=>document.querySelector('.chat-compose .talk-live strong')?.textContent==='Live');
  const start=actions.find(a=>a.action==='talk_start');assert.deepEqual(start.args,{suggestion_id:id});
  assert.equal(actions.find(a=>a.action==='talk_offer').args.sdp,'v=0\r\noffer\r\n');
  const setup=await page.evaluate(()=>window.__dc.sent[0]);
  assert.equal(setup.type,'session.update');
  assert.deepEqual(setup.session.tools.map(x=>x.name),['todo_details','find_todos','ask_chat'],'the page sets its own tools');
  assert.equal(setup.session.instructions,'You are The Machine, talking live.');
  assert.ok(setup.session.audio.input.transcription.model,'what the owner says is written down');
  assert.ok(await page.locator(bar+' .talk-cost').isVisible(),'an API key: the cost note shows');

  // What both sides say lands in the chat, as normal messages: the voice's once its response is done
  await page.evaluate(()=>{__say({type:'conversation.item.input_audio_transcription.completed',item_id:'i1',transcript:'When can Lotte pick up the paint?'});
   __say({type:'response.created',response:{id:'r2'}});__say({type:'response.output_audio_transcript.done',response_id:'r2',item_id:'i2',transcript:'She can pick it up on Thursday after two.'});
   __say({type:'response.done',response:{id:'r2',status:'completed'}})});
  await page.waitForFunction(()=>document.querySelector('#chat-log').textContent.includes('Thursday after two'));
  for(let i=0;i<50&&actions.filter(a=>a.action==='talk_line').length<2;i++)await page.waitForTimeout(20);
  assert.deepEqual(actions.filter(a=>a.action==='talk_line').map(a=>a.args.role),['user','assistant']);
  await page.evaluate(()=>{__say({type:'response.output_audio_transcript.done',response_id:'r2b',item_id:'i2',transcript:'She can pick it up on Thursday after two.'});__say({type:'response.done',response:{id:'r2b',status:'completed'}})});
  await page.waitForTimeout(100);assert.equal(actions.filter(a=>a.action==='talk_line').length,2,'each line once');
  // Talked over: what the voice had started to say is dropped, never a stray half line in the chat
  await page.evaluate(()=>{__say({type:'response.output_audio_transcript.done',response_id:'r2c',item_id:'i2c',transcript:'The chat is on'});__say({type:'response.done',response:{id:'r2c',status:'cancelled'}})});
  await page.waitForTimeout(100);assert.equal(actions.filter(a=>a.action==='talk_line').length,2,'a response cut short is not kept');
  assert.ok(!(await page.locator('#chat-log').textContent()).includes('The chat is on'));

  // A read tool: through the Machine, and its answer goes back to the voice
  await page.evaluate(()=>__say({type:'response.function_call_arguments.done',call_id:'call1',name:'todo_details',arguments:'{}'}));
  await page.waitForFunction(()=>window.__dc.sent.some(x=>x.item?.call_id==='call1'));
  assert.deepEqual(actions.find(a=>a.action==='talk_tool').args,{id:'feedfeedfeedfeed',name:'todo_details',args:{}});
  assert.equal(await page.evaluate(()=>window.__dc.sent.at(-1).type),'response.create');
  await page.waitForTimeout(300);await shot('t3-live');

  // Asking the chat: a hand-off (a decision 'other', chat-talk-…), never shown as the owner's own message
  const ask=async(n,request)=>{await page.evaluate(([n,request])=>__say({type:'response.function_call_arguments.done',call_id:n,name:'ask_chat',arguments:JSON.stringify({request})}),[n,request]);
   await page.waitForFunction(n=>window.__dc.sent.some(x=>x.item?.call_id===n),n);return page.evaluate(n=>JSON.parse(window.__dc.sent.find(x=>x.item?.call_id===n).item.output),n)};
  const told=()=>page.evaluate(()=>window.__dc.sent.filter(x=>x.type==='conversation.item.create'&&x.item?.type==='message').map(x=>x.item.content[0].text));
  const done=(text,draft)=>{running=false;if(draft)cards[0].next_actions=[DRAFT];asked.push({kind:'reply',text,...(draft?{drafts:[{kind:'email',to:['Lotte'],subject:DRAFT.subject,body:DRAFT.body,reply:true}]}:{}),at:Date.now()})};
  assert.deepEqual(await ask('call2','Reply to Lotte that Thursday after two works'),{ok:true,waiting:false,note:'Drafts wait for Approve.'});
  let decided=actions.filter(a=>a.action==='decide');
  assert.equal(decided.length,1);assert.equal(decided[0].args.choice,'other');assert.match(decided[0].args.decision_id,/^chat-talk-/);
  assert.equal(decided[0].args.feedback,'Reply to Lotte that Thursday after two works');
  assert.equal(actions.filter(a=>a.action==='talk_tool').length,1,'ask_chat never reaches the Machine as a tool');
  await page.waitForTimeout(300);
  assert.ok(!(await page.locator('#chat-log').textContent()).includes('Reply to Lotte that'),'the hand-off is not a bubble');
  await shot('t3b-looking-it-up');
  // A second ask while the chat is on the first: it waits, it never stops the running turn
  assert.deepEqual(await ask('call2b','Also ask if she wants it delivered'),{ok:true,queued:true,note:'Joins the last request.'});
  assert.equal(actions.filter(a=>a.action==='decide').length,1,'no new decision while the turn runs');
  // The turn ends: its answer goes straight to the voice, which says it (no checking back); then the waiting ask goes
  done('Drafted a reply to Lotte: Thursday after two works. Tap Approve to send it.',true);
  await page.waitForFunction(()=>window.__dc.sent.some(x=>x.item?.type==='message'),null,{timeout:8000});
  assert.deepEqual(await told(),['The chat finished. Its answer: "Drafted a reply to Lotte: Thursday after two works. Tap Approve to send it." Tell the owner now.']);
  assert.equal(await page.evaluate(()=>window.__dc.sent.at(-1).type),'response.create','and it speaks it at once');
  await page.waitForFunction(()=>document.querySelector('#chat-log').textContent.includes('Tap Approve to send it'));
  for(let i=0;i<50&&actions.filter(a=>a.action==='decide').length<2;i++)await page.waitForTimeout(50);
  decided=actions.filter(a=>a.action==='decide');
  assert.equal(decided.length,2,'the waiting ask goes once the turn is done');assert.equal(decided[1].args.feedback,'Also ask if she wants it delivered');
  // Its answer waits while the voice is still talking, and comes right after
  await page.evaluate(()=>__say({type:'response.created',response:{id:'r3'}}));
  done('Added a line asking if she wants it delivered.',false);
  await page.waitForTimeout(1600);assert.equal((await told()).length,1,'not while the voice talks');
  await page.evaluate(()=>__say({type:'response.done',response:{id:'r3',status:'completed'}}));
  assert.match((await told())[1],/Added a line asking if she wants it delivered/);
  await page.evaluate(()=>__say({type:'response.done',response:{id:'r4',status:'completed'}}));
  // The draft it made shows in the chat with its Approve control, like one made from a typed message
  await page.locator('#chat-log .chat-draft.current [data-smart]').waitFor();
  assert.ok((await page.locator('#chat-log .chat-draft.current').textContent()).includes('Thursday after two works'));
  await page.waitForTimeout(400);
  if(!phone)assert.equal(await page.locator(bar+' .talk-hint').textContent(),'Say yes to send what’s on screen.');
  await shot('t4-asked-chat');
  const said=(n,text,role='user')=>page.evaluate(([n,text,role])=>{if(role==='user'){__say({type:'conversation.item.input_audio_transcription.completed',item_id:n,transcript:text});return}
   __say({type:'response.output_audio_transcript.done',response_id:'r'+n,item_id:n,transcript:text});__say({type:'response.done',response:{id:'r'+n,status:'completed'}})},[n,text,role]);
  const call=async(n,name)=>{await page.evaluate(([n,name])=>__say({type:'response.function_call_arguments.done',call_id:n,name,arguments:'{}'}),[n,name]);
   await page.waitForFunction(n=>window.__dc.sent.some(x=>x.item?.call_id===n),n);return page.evaluate(n=>JSON.parse(window.__dc.sent.find(x=>x.item?.call_id===n).item.output),n)};

  // The question: only for the draft on screen (its revision), read out first on a phone
  const q=await call('call3','ask_to_send');
  assert.equal(q.question,'Send this reply to Lotte by email?');
  const asking=actions.filter(a=>a.action==='talk_ask_send').at(-1).args;
  assert.equal(asking.revision,'r1');assert.equal(asking.read_aloud,phone,'a phone: the voice reads the draft out first');
  await said('i3','Send this reply to Lotte by email?','assistant');
  await page.waitForTimeout(150);await shot('t4b-confirm-question');

  // A clear yes: what was said is kept first, then the Machine judges it and the draft goes, with Undo for a few seconds
  await said('i4','Yes, send it.');
  const ok=await call('call4','send_answer');
  assert.equal(ok.status,'queued');
  const at=actions.findLastIndex(a=>a.action==='talk_send'),line=actions.findIndex(a=>a.action==='talk_line'&&a.args.text==='Yes, send it.');
  assert.ok(line>=0&&line<at,'the answer is kept before the Machine judges it');
  await page.locator('#chat-log [data-voice-undo]').waitFor();
  assert.match(await page.locator('#chat-log .chat-event',{hasText:'Approved by voice'}).textContent(),/^Approved by voice · Undo/);
  assert.equal(actions.filter(a=>a.action==='confirm_action').length,0,'the page never approves by itself');
  await page.waitForTimeout(200);await shot('t4c-approved-by-voice');
  await tap('#chat-log [data-voice-undo]');
  await page.waitForFunction(()=>document.querySelector('#chat-log').textContent.includes('Send canceled'));
  assert.deepEqual(actions.find(a=>a.action==='talk_undo').args,{suggestion_id:id,approval_id:'voice:1'});
  assert.equal(await page.locator('#chat-log [data-voice-undo]').count(),0);
  sends.length=0;

  // A yes with no confirm question before it sends nothing
  await said('i5','Yes, send it now.');
  assert.equal((await call('call5','send_answer')).status,'not_asked');
  assert.equal(sends.length,0);

  // The draft changes between the question and the yes: it doesn't count, the voice asks again
  await call('call6','ask_to_send');await said('i6','Send this reply to Lotte by email?','assistant');
  cards[0].next_actions=[{...DRAFT,body:'Hi Lotte, Friday after two works.',revision:'r2'}];await page.evaluate(()=>refresh());
  await page.waitForFunction(()=>document.querySelector('#chat-log .chat-draft.current [data-smart]')?.dataset.smart==='r2');
  const sentBefore=actions.filter(a=>a.action==='talk_send').length;
  await said('i7','Yes.');
  const changed=await call('call7','send_answer');
  assert.equal(changed.status,'changed');assert.match(changed.say,/ask_to_send again/);
  assert.equal(actions.filter(a=>a.action==='talk_send').length,sentBefore,'nothing asked of the Machine for a changed draft');

  // An unclear answer, or a no: the Machine says so, nothing goes
  for(const [n,v,text] of [[8,'unclear','Hmm, what did it say again?'],[9,'no','No, wait.']]){
   await call('call'+n+'a','ask_to_send');assert.equal(actions.filter(a=>a.action==='talk_ask_send').at(-1).args.revision,'r2');
   await said('i'+n+'a','Send this reply to Lotte by email?','assistant');
   verdict=v;await said('i'+n,text);
   assert.equal((await call('call'+n,'send_answer')).status,v);
   assert.equal(sends.length,0)}
  verdict='queued';

  // Mute: the microphone track is off
  await tap(bar+' [data-talk-mute]');
  assert.equal(await page.evaluate(()=>window.__stream.getAudioTracks()[0].enabled),false);
  assert.equal(await page.locator(bar+' [data-talk-mute]').textContent(),'Unmute');
  await tap(bar+' [data-talk-mute]');assert.equal(await page.evaluate(()=>window.__stream.getAudioTracks()[0].enabled),true);

  // A minute before 10 minutes it warns; at 10 it ends by itself
  await page.evaluate(()=>{window.__skew=545000});
  await page.waitForFunction(()=>document.querySelector('.chat-compose .talk-live.near'));
  assert.match(await page.locator(bar+' .talk-time').textContent(),/^0:[0-5]\d left$/);
  await shot('t5-one-minute-left');
  await page.evaluate(()=>{window.__skew=601000});
  await page.waitForFunction(()=>!document.querySelector('.chat-compose .talk'));await page.waitForTimeout(300);
  assert.equal(actions.filter(a=>a.action==='talk_end').length,1,'it ends at the Machine too');
  assert.equal(await page.evaluate(()=>window.__closed),1);
  await page.evaluate(()=>{window.__skew=0});

  if(scheme==='light'){
   // End, with a ChatGPT sign-in (no cost note)
   perUse=false;await tap(wave);await page.waitForFunction(()=>document.querySelector('.chat-compose .talk-live strong')?.textContent==='Live');
   assert.equal(await page.locator(bar+' .talk-cost').count(),0,'a ChatGPT sign-in: no cost note');
   await tap(bar+' [data-talk-end]');await page.waitForFunction(()=>!document.querySelector('.chat-compose .talk'));await page.waitForTimeout(300);
   assert.equal(actions.filter(a=>a.action==='talk_end').length,2);

   // The microphone is blocked, or the Machine can't start it: it says so
   await page.evaluate(()=>{window.__mic.mode='denied'});await tap(wave);
   await page.waitForSelector(bar+' .talk-err');assert.match(await page.locator(bar+' .talk-err').textContent(),/microphone is blocked/);
   await tap(bar+' [data-talk-close]');await page.evaluate(()=>{window.__mic.mode='ok'});
   startFails=true;await tap(wave);
   await page.waitForSelector(bar+' .talk-err');assert.match(await page.locator(bar+' .talk-err').textContent(),/Check OpenAI in OpenClaw/);
   await shot('t6-error');await tap(bar+' [data-talk-close]');startFails=false;

   // Leaving the chat ends it
   await tap(wave);await page.waitForFunction(()=>document.querySelector('.chat-compose .talk-live strong')?.textContent==='Live');
   const ends=actions.filter(a=>a.action==='talk_end').length;
   await page.goto(base+'#');await page.waitForTimeout(400);
   assert.ok(actions.filter(a=>a.action==='talk_end').length>ends||await page.evaluate(()=>!window.talk),'leaving the chat ends it');
  }
  assert.equal(sent(),2,'only the two requests to the chat');
  await context.close()}

 // Without OpenAI, and in the site's demo: no wave
 for(const [r,d] of [[false,false],[true,true]]){ready=r;demo=d;
  const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'en-US'});
  await context.addInitScript(FAKE_RTC);const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#chat='+id);await page.locator('#chat-input').waitFor();await page.waitForTimeout(800);
  assert.equal(await page.locator('.chat-compose [data-talk]').isVisible(),false,d?'the demo has no wave':'no OpenAI, no wave');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('talk live dashboard ok');
}finally{await browser?.close();server.close()}
