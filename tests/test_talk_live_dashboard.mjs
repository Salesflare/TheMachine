import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Talk live (talk_live.py): the wave next to the mic in a to-do's chat starts a spoken conversation. The bar shows Live,
// the clock, Mute and End; a minute before 10 minutes it warns, and at 10 it ends. What both sides say lands in the chat.
// A proposal shows above the bar and goes to the chat only on a tap; a spoken "yes" sends nothing. OpenAI is a
// stand-in here: a fake microphone, RTCPeerConnection and data channel (window.__dc), and the Machine's answers are
// the fixture server's, so the test never needs a microphone, a key or the network.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString(),id='c1c1c1c1c1c1c1c1';
const cards=[{id,title:'Reply to Lotte about the paint order',body:'Lotte asked when the order can be picked up.',status:'prepared',scope:'personal',created_at:now,event_ids:[1]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const actions=[],lines=[];let ready=true,perUse=true,demo=false,startFails=false,hold=null;
const TOOLS=[{type:'function',name:'todo_details'},{type:'function',name:'find_todos'},{type:'function',name:'propose'}];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);const a=r.args||{};
  if(demo&&r.action.startsWith('talk_')){res.end(JSON.stringify({ok:true,demo:true}));return}
  const answer={
   talk_status:()=>({ready,limit:600,warn:540}),
   talk_start:()=>startFails?null:{id:'feedfeedfeedfeed',via:perUse?'key':'signin',per_use:perUse,limit:600,warn:540,tools:TOOLS,instructions:'You are The Machine, talking live.',propose_note:'Only their tap sends it.',ready:true},
   talk_offer:()=>({sdp:'v=0\r\nanswer\r\n'}),
   talk_line:()=>{lines.push({kind:a.role==='user'?'you':'reply',text:a.text,via:'live',at:Date.now()});return {ok:true}},
   talk_tool:()=>({output:{title:cards[0].title,messages:[{from:'Lotte',text:'When can I pick it up?'}]}}),
   talk_end:()=>({ok:true}),
   card_chat:()=>({session:true,status:'done',active:false,cursor:'k',items:[{kind:'reply',text:'Lotte asked when the order can be picked up. Want me to answer her?',at:Date.now()-60000},...lines]}),
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
  actions.length=0;lines.length=0;perUse=true;
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
  assert.deepEqual(setup.session.tools.map(x=>x.name),['todo_details','find_todos','propose'],'the page sets its own tools');
  assert.equal(setup.session.instructions,'You are The Machine, talking live.');
  assert.ok(setup.session.audio.input.transcription.model,'what the owner says is written down');
  assert.ok(await page.locator(bar+' .talk-cost').isVisible(),'an API key: the cost note shows');

  // What both sides say lands in the chat, as normal messages
  await page.evaluate(()=>{__say({type:'conversation.item.input_audio_transcription.completed',item_id:'i1',transcript:'When can Lotte pick up the paint?'});
   __say({type:'response.output_audio_transcript.done',item_id:'i2',transcript:'She can pick it up on Thursday after two.'})});
  await page.waitForFunction(()=>document.querySelector('#chat-log').textContent.includes('Thursday after two'));
  for(let i=0;i<50&&actions.filter(a=>a.action==='talk_line').length<2;i++)await page.waitForTimeout(20);
  assert.deepEqual(actions.filter(a=>a.action==='talk_line').map(a=>a.args.role),['user','assistant']);
  await page.evaluate(()=>{__say({type:'response.output_audio_transcript.done',item_id:'i2',transcript:'She can pick it up on Thursday after two.'})});
  await page.waitForTimeout(100);assert.equal(actions.filter(a=>a.action==='talk_line').length,2,'each line once');

  // A read tool: through the Machine, and its answer goes back to the voice
  await page.evaluate(()=>__say({type:'response.function_call_arguments.done',call_id:'call1',name:'todo_details',arguments:'{}'}));
  await page.waitForFunction(()=>window.__dc.sent.some(x=>x.item?.call_id==='call1'));
  assert.deepEqual(actions.find(a=>a.action==='talk_tool').args,{id:'feedfeedfeedfeed',name:'todo_details',args:{}});
  assert.equal(await page.evaluate(()=>window.__dc.sent.at(-1).type),'response.create');
  await page.waitForTimeout(300);await shot('t3-live');

  // A proposal: it shows, and a spoken "yes" afterwards sends nothing
  await page.evaluate(()=>{__say({type:'response.function_call_arguments.done',call_id:'call2',name:'propose',arguments:JSON.stringify({request:'Reply to Lotte that Thursday after two works'})});
   __say({type:'conversation.item.input_audio_transcription.completed',item_id:'i3',transcript:'Yes, send it.'})});
  await page.waitForSelector(bar+' .talk-prop');
  assert.equal(await page.locator(bar+' .talk-prop-text').textContent(),'Reply to Lotte that Thursday after two works');
  const out=await page.evaluate(()=>JSON.parse(window.__dc.sent.find(x=>x.item?.call_id==='call2').item.output));
  assert.equal(out.note,'Only their tap sends it.');
  await page.waitForTimeout(300);assert.equal(sent(),0,'a spoken yes sends nothing');
  assert.equal(actions.filter(a=>a.action==='talk_tool').length,1,'propose never reaches the Machine as a tool');
  await shot('t4-proposal');

  // Mute: the microphone track is off
  await tap(bar+' [data-talk-mute]');
  assert.equal(await page.evaluate(()=>window.__stream.getAudioTracks()[0].enabled),false);
  assert.equal(await page.locator(bar+' [data-talk-mute]').textContent(),'Unmute');
  await tap(bar+' [data-talk-mute]');assert.equal(await page.evaluate(()=>window.__stream.getAudioTracks()[0].enabled),true);

  // The tap: the proposal goes to the chat as the owner's message, the normal way (it then drafts for Approve)
  await tap(bar+' [data-talk-send]');
  await page.waitForFunction(()=>!document.querySelector('.chat-compose .talk-prop'));
  await page.waitForTimeout(300);
  const decided=actions.filter(a=>a.action==='decide');
  assert.equal(decided.length,1);assert.equal(decided[0].args.choice,'other');
  assert.equal(decided[0].args.feedback,'Reply to Lotte that Thursday after two works');

  // A minute before 10 minutes it warns; at 10 it ends by itself
  await page.evaluate(()=>{window.__skew=545000});
  await page.waitForFunction(()=>document.querySelector('.chat-compose .talk-live.near'));
  assert.match(await page.locator(bar+' .talk-time').textContent(),/^0:5\d left$/);
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
  assert.equal(sent(),1,'only the one tapped proposal was ever sent');
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
