import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Talk (talk_live.py) hears the owner in their own languages: the session is set up with them (transcription), noise
// reduction and low-eagerness turns; a transcript that is noise (marks only, another script, an unsure short line) is
// left out of the transcript, out of the voice's memory, and the voice's reply to it is stopped and dropped. A Dutch
// sentence still counts. The voice's lines lose their em dashes. The "Talking about" card shows a whole email draft:
// its lines never overlap and it is tall enough to read on a phone, with room left for the transcript.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),A='a1a1a1a1a1a1a1a1';
const BODY=['Hi Sam,','','Thanks for the note about the comparison article. We don’t usually do link insertions, but we have a policy for the kind we do accept, and this one could fit.',
 '','If the placement is relevant and not spammy, we can consider including it and draft a listing for your guide in return. If you prefer an insertion, could you point to the exact paragraph and explain why it’s editorially relevant?',
 '','Regards,','Robin'].join('\n');
const DRAFT={kind:'email',label:'Reply to Sam',to:['sam@example.com'],to_name:'Sam',from:'me@example.com',subject:'Re: Link insertion',body:BODY,revision:'r1',account_id:'mail'};
const cards=[{id:A,title:'Sam proposes link insertions for the guide exchange',body:'Sam asked about link insertions.',status:'prepared',scope:'work',created_at:now,event_ids:[1],people:[{id:'p1',name:'Sam'}],next_actions:[DRAFT]}];
const state=()=>({talk_ready:true,suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const actions=[],lines=[];
const TRANSCRIPTION={model:'gpt-4o-mini-transcribe',prompt:'One person talking with their assistant in English or Dutch.'};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);const a=r.args||{};
  const answer={
   talk_status:()=>({ready:true,limit:600,warn:540}),
   talk_start:()=>({id:'feedfeedfeedfeed',via:'signin',per_use:false,limit:1800,warn:1740,tools:[{type:'function',name:'open_todo'}],main:true,instructions:'Talk.',voice:'cedar',speed:1.1,
    turn:{type:'semantic_vad',eagerness:'low',create_response:true,interrupt_response:true},noise:{type:'far_field'},transcription:TRANSCRIPTION,languages:['en','nl'],ask_note:'',notes:{},ready:true}),
   talk_offer:()=>({sdp:'v=0\r\nanswer\r\n'}),
   talk_focus:()=>({ok:true}),
   talk_line:()=>{lines.push({role:a.role,text:a.text});return {ok:true}},
   talk_tool:()=>({output:{title:cards[0].title,drafts:[DRAFT]}}),
   talk_end:()=>({ok:true}),
  }[r.action];
  res.end(JSON.stringify(answer?answer():{}));return}
 if(/^\/brand\/[\w.-]+\.(png|webp|woff2|svg)$/.test(url.pathname)){try{const f=await readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url));res.setHeader('Content-Type',{png:'image/png',webp:'image/webp',woff2:'font/woff2',svg:'image/svg+xml'}[url.pathname.split('.').pop()]);res.end(f)}catch{res.statusCode=404;res.end()}return}
 res.statusCode=200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const SHOTS=process.env.SHOT_DIR;

const FAKE_RTC=()=>{
 navigator.mediaDevices.getUserMedia=async()=>{const ac=new AudioContext(),osc=ac.createOscillator(),dest=ac.createMediaStreamDestination();osc.connect(dest);osc.start();return dest.stream};
 window.RTCPeerConnection=class{constructor(){this.connectionState='new'}
  addTrack(){}
  createDataChannel(label){const dc=window.__dc={label,readyState:'connecting',sent:[],send(x){this.sent.push(JSON.parse(x))},close(){this.readyState='closed'}};this.dc=dc;return dc}
  async createOffer(){return {type:'offer',sdp:'v=0\r\noffer\r\n'}}
  async setLocalDescription(){}
  async setRemoteDescription(){setTimeout(()=>{this.connectionState='connected';this.dc.readyState='open';this.dc.onopen?.()},60)}
  close(){this.connectionState='closed'}};
 window.__say=e=>window.__dc.onmessage({data:JSON.stringify(e)})};

// Line boxes of the draft's text: every rendered line (Range client rects), none overlapping another
const LINE_BOXES=()=>{const box=document.querySelector('#talk-view .talk-about .chat-clamp');const out=[];
 const walk=document.createTreeWalker(box,NodeFilter.SHOW_TEXT);for(let n;(n=walk.nextNode());){if(!n.textContent.trim())continue;const r=document.createRange();r.selectNodeContents(n);
  for(const b of r.getClientRects())if(b.width>0&&b.height>0)out.push({top:b.top,bottom:b.bottom,left:b.left,right:b.right,text:n.textContent.slice(0,30)})}
 const c=box.getBoundingClientRect();return {lines:out,box:{top:c.top,bottom:c.bottom,height:c.height,scroll:box.scrollHeight}}};

const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']});
 for(const [w,h,scheme] of [[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]){
  const phone=w<500,context=await browser.newContext({viewport:{width:w,height:h},isMobile:phone,hasTouch:phone,deviceScaleFactor:2,colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.addInitScript(FAKE_RTC);
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  actions.length=0;lines.length=0;
  await page.goto('http://127.0.0.1:'+server.address().port+'/#');await page.waitForTimeout(400);
  const tag=`${w}-${scheme}`,shot=async n=>{if(SHOTS)await page.screenshot({path:`${SHOTS}/${n}-${tag}.png`})};
  const until=async(f,ms=4000)=>{for(let i=0;i<ms/50&&!f();i++)await page.waitForTimeout(50);assert.ok(f())};
  const say=e=>page.evaluate(e=>__say(e),e);
  if(phone)await page.evaluate(()=>drawerOpen());
  await page.waitForSelector('#side-talk:not([hidden])');await page.waitForTimeout(300);
  await (phone?page.locator('#side-talk').tap():page.locator('#side-talk').click());
  await page.waitForFunction(()=>document.querySelector('#talk-view .talk-live strong')?.textContent==='Live');

  // The browser's languages go along; the session hears in the owner's languages, with noise reduction and calm turns
  assert.ok(Array.isArray(actions.find(a=>a.action==='talk_start').args.languages));
  const [setup,extra]=await page.evaluate(()=>window.__dc.sent.slice(0,2));
  assert.deepEqual(setup.session.audio.input.transcription,TRANSCRIPTION);
  assert.deepEqual(setup.session.audio.input.noise_reduction,{type:'far_field'});
  assert.equal(setup.session.audio.input.turn_detection.eagerness,'low');
  assert.equal(setup.session.audio.output.speed,1.1);
  assert.deepEqual(extra.session.include,['item.input_audio_transcription.logprobs']);

  // What counts as noise
  const noise=await page.evaluate(()=>[['음력?'],['แก'],['...'],['  '],['Ladnialok.',[{logprob:-2.4},{logprob:-1.9},{logprob:-3.1}]],['Softer.'],['Yes.',[{logprob:-0.01}]],
   ['Ja, stuur maar.'],['Kun je het wat korter maken, en de laatste zin weglaten?'],['Привет'],['Café crème, s’il vous plaît.'],['Tuesday at 3.'],['One person talking with their assistant in English or Dutch.']]
   .map(([t,lp])=>talkNoise(t,lp,'One person talking with their assistant in English or Dutch.')));
  assert.deepEqual(noise,[true,true,true,true,true,false,false,false,false,true,false,false,true]);

  // The voice opens the to-do: the card shows its draft
  await say({type:'response.function_call_arguments.done',call_id:'o1',name:'open_todo',arguments:JSON.stringify({id:A})});
  await page.waitForSelector('#talk-view .talk-about .chat-draft');
  // A real turn: committed, written down, answered; the dash goes
  await say({type:'input_audio_buffer.committed',item_id:'u1'});
  await say({type:'response.created',response:{id:'r1'}});
  await say({type:'conversation.item.input_audio_transcription.completed',item_id:'u1',transcript:'And in this deal we get a real listing, so I’m willing to do it.'});
  await say({type:'response.output_audio_transcript.done',response_id:'r1',item_id:'a1',transcript:'Okay, that helps—let’s shape a reply around your policy.'});
  await say({type:'response.done',response:{id:'r1',status:'completed'}});
  // A noise: the reply to it was already going. It's stopped, the line and the reply both dropped, the item forgotten
  await say({type:'input_audio_buffer.committed',item_id:'u2'});
  await say({type:'response.created',response:{id:'r2'}});
  await say({type:'conversation.item.input_audio_transcription.completed',item_id:'u2',transcript:'음력?'});
  await say({type:'response.output_audio_transcript.done',response_id:'r2',item_id:'a2',transcript:'Right.'});
  await say({type:'response.done',response:{id:'r2',status:'cancelled'}});
  // A noise written down only after its reply ended: the reply waited, and is dropped too
  await say({type:'input_audio_buffer.committed',item_id:'u3'});
  await say({type:'response.created',response:{id:'r3'}});
  await say({type:'response.output_audio_transcript.done',response_id:'r3',item_id:'a3',transcript:'Sure.'});
  await say({type:'response.done',response:{id:'r3',status:'completed'}});
  await say({type:'conversation.item.input_audio_transcription.completed',item_id:'u3',transcript:'แก'});
  // Dutch counts
  await say({type:'input_audio_buffer.committed',item_id:'u4'});
  await say({type:'response.created',response:{id:'r4'}});
  await say({type:'response.output_audio_transcript.done',response_id:'r4',item_id:'a4',transcript:'Goed, ik maak hem korter.'});
  await say({type:'response.done',response:{id:'r4',status:'completed'}});
  await say({type:'conversation.item.input_audio_transcription.completed',item_id:'u4',transcript:'Kun je het wat korter maken?'});
  await until(()=>lines.length>=4);await page.waitForTimeout(300);
  assert.deepEqual(lines,[{role:'user',text:'And in this deal we get a real listing, so I’m willing to do it.'},{role:'assistant',text:'Okay, that helps, let’s shape a reply around your policy.'},
   {role:'user',text:'Kun je het wat korter maken?'},{role:'assistant',text:'Goed, ik maak hem korter.'}]);
  const log=await page.locator('#talk-view .talk-log').textContent();
  for(const gone of ['음력','แก','Right.','Sure.','—'])assert.ok(!log.includes(gone),gone);
  const sent=await page.evaluate(()=>window.__dc.sent);
  assert.deepEqual(sent.filter(x=>x.type==='conversation.item.delete').map(x=>x.item_id),['u2','u3']);
  assert.deepEqual(sent.filter(x=>x.type==='response.cancel').map(x=>x.response_id),['r2']);

  // The card: the whole draft readable, no line on top of another, room left for the transcript
  await page.waitForTimeout(300);await shot('h1-talking-about-a-draft');
  const noOverlap=async()=>{const m=await page.evaluate(LINE_BOXES);assert.ok(m.lines.length>=6,`${m.lines.length} lines`);
   const shown=m.lines.filter(l=>l.bottom>m.box.top+1&&l.top<m.box.bottom-1);assert.ok(shown.length>=3,`${shown.length} lines in sight`);
   for(let i=0;i<shown.length;i++)for(let j=i+1;j<shown.length;j++){const a=shown[i],b=shown[j];
    const overlap=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>2&&Math.min(a.right,b.right)-Math.max(a.left,b.left)>2;
    assert.ok(!overlap,`"${a.text}" and "${b.text}" overlap`)}
   return m};
  const m=await noOverlap();
  // Scrolled to its end (where "Regards," landed on top of a line): still no overlap, the last line in sight
  await page.evaluate(()=>{const b=document.querySelector('#talk-view .talk-about .chat-clamp');b.scrollTop=b.scrollHeight});await page.waitForTimeout(150);
  await shot('h2-draft-scrolled-to-the-end');
  const end=await noOverlap();assert.ok(end.lines.some(l=>l.text.startsWith('Robin')&&l.bottom<=end.box.bottom+1),'the signature shows at the end');
  assert.ok(m.box.height>=Math.min(phone?260:300,m.box.scroll-1),`the draft is ${m.box.height}px tall`);  // tall enough, or all of it
  const room=await page.evaluate(()=>innerHeight-document.querySelector('#talk-view .talk-foot').offsetHeight-document.querySelector('#talk-view .talk-about').getBoundingClientRect().bottom);  // the bar sits at the bottom once the transcript is long
  assert.ok(room>=(phone?200:250),`${room}px left for the transcript`);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('talk hearing dashboard ok');
}finally{await browser?.close();server.close()}
