import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Voice input (voice_input.py): the mic in the to-do chat's box, New to-do and Help. Tap to talk and tap Done, or hold
// it; the recording bar shows Cancel, the clock and Done; the clip goes to the Machine as 16 kHz mono WAV; the text
// lands in the box and nothing is sent. The first time, the Machine gets its engine ready while the page waits. The
// browser's microphone and MediaRecorder are stand-ins here (window.__mic decides what the microphone does), so the
// test never needs a real one; the Machine's answers are the fixture server's.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString(),id='c1c1c1c1c1c1c1c1';
const cards=[{id,title:'Reply to Lotte about the paint order',body:'Lotte asked when the order can be picked up.',status:'prepared',scope:'personal',created_at:now,event_ids:[1]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const actions=[];let local={state:'ready'},hold=null,drop=0,demo=false,said='Tell her Thursday after two works.';
const voiceView=()=>({engine:'local',model:'small',language:'',local,openai:false,max_seconds:120,languages:['de','en','es','fr','it','nl','pt'],models:['small','base']});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push({...r,upload:req.headers['x-upload']||''});
  if(demo&&r.action.startsWith('voice_')){res.end(JSON.stringify({ok:true,demo:true}));return}  // the site's demo answers what it doesn't know so
  if(r.action==='voice_status'){res.end(JSON.stringify(voiceView()));return}
  if(r.action==='voice_prepare'){if(local.state!=='ready')local={state:'preparing',step:'packages',done:0,total:0};res.end(JSON.stringify(voiceView()));return}
  if(r.action==='voice_prefs'){res.end(JSON.stringify({...voiceView(),...r.args}));return}
  if(r.action==='voice_transcribe'){
   if(drop>0){drop--;res.statusCode=502;res.setHeader('Content-Type','text/html');res.end('<h1>502</h1>');return}  // the Machine can't be reached (its proxy answers)
   if(hold)await hold;
   if(local.state!=='ready'){res.end(JSON.stringify({pending:true,voice:voiceView()}));return}
   res.end(JSON.stringify({text:said,language:'en'}));return}
  res.end(JSON.stringify(r.action==='card_chat'?{session:true,status:'done',active:false,cursor:'k',items:[{kind:'reply',text:'Lotte asked when the order can be picked up. Want me to answer her?',at:Date.now()-60000}]}:{}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const SHOTS=process.env.SHOT_DIR;

// A microphone and recorder that need no device: the recorder hands over a 1.5 s 48 kHz stereo WAV (what a phone's
// recorder would give, in a format Chromium decodes), and Date.now can be moved on (__skew) to reach the 2-minute limit.
const FAKE_MIC=()=>{window.__mic={mode:'ok',started:0,stopped:0};const real=Date.now;window.__skew=0;Date.now=()=>real()+window.__skew;
 const wav=()=>{const rate=48000,n=rate*1.5,ch=2,v=new DataView(new ArrayBuffer(44+n*ch*2)),w=(o,s)=>[...s].forEach((c,i)=>v.setUint8(o+i,c.charCodeAt(0)));
  w(0,'RIFF');v.setUint32(4,36+n*ch*2,true);w(8,'WAVE');w(12,'fmt ');v.setUint32(16,16,true);v.setUint16(20,1,true);v.setUint16(22,ch,true);v.setUint32(24,rate,true);v.setUint32(28,rate*ch*2,true);v.setUint16(32,ch*2,true);v.setUint16(34,16,true);w(36,'data');v.setUint32(40,n*ch*2,true);
  for(let i=0;i<n;i++)for(let c=0;c<ch;c++)v.setInt16(44+(i*ch+c)*2,Math.round(Math.sin(i/rate*2*Math.PI*220)*8000),true);return new Blob([v.buffer],{type:'audio/wav'})};
 navigator.mediaDevices.getUserMedia=async()=>{const m=window.__mic.mode;
  if(m==='denied')throw new DOMException('Permission denied','NotAllowedError');if(m==='none')throw new DOMException('Requested device not found','NotFoundError');
  const ac=new AudioContext(),osc=ac.createOscillator(),dest=ac.createMediaStreamDestination();osc.connect(dest);osc.start();return dest.stream};
 window.MediaRecorder=class extends EventTarget{constructor(stream,opts){super();this.stream=stream;this.mimeType=opts?.mimeType||'audio/webm';this.state='inactive'}
  static isTypeSupported(t){return t==='audio/webm;codecs=opus'}
  start(){this.state='recording';window.__mic.started++}
  stop(){if(this.state==='inactive')return;this.state='inactive';window.__mic.stopped++;setTimeout(()=>{this.ondataavailable?.({data:wav()});this.onstop?.()},20)}}};

const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']});
 for(const [w,h,scheme] of [[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]){
  const phone=w<500,context=await browser.newContext({viewport:{width:w,height:h},isMobile:phone,hasTouch:phone,deviceScaleFactor:2,colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.addInitScript(FAKE_MIC);
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const base='http://127.0.0.1:'+server.address().port+'/';
  await page.goto(base+'#chat='+id);await page.locator('#chat-input').waitFor();await page.waitForTimeout(600);
  const tag=`${w}-${scheme}`,shot=async n=>{if(SHOTS)await page.screenshot({path:`${SHOTS}/${n}-${tag}.png`})};
  const box='.chat-compose .chat-box',mic=box+' [data-mic]';
  const tap=sel=>phone?page.locator(sel).tap():page.locator(sel).click();
  const sent=()=>actions.filter(a=>a.action==='decide'||a.action==='card_chat_send').length;
  // Idle: the mic sits next to Send, the same size, inside the box
  const m=await page.locator(mic).boundingBox(),b=await page.locator(box).boundingBox();
  assert.ok(m&&m.width>=32&&m.x>=b.x&&m.x+m.width<=b.x+b.width&&m.y>=b.y&&m.y+m.height<=b.y+b.height,'the mic is in the box: '+JSON.stringify({m,b}));
  await shot('1-idle');

  // Tap: it records, with a clock and Done; Cancel throws it away and nothing goes to the Machine
  await page.locator('#chat-input').fill('Sure.');actions.length=0;
  await tap(mic);await page.waitForSelector(box+'.mic-on .mic-time');await page.waitForTimeout(1300);
  assert.match(await page.locator(box+' .mic-time').textContent(),/^0:0[1-9]$/,'the clock runs');
  assert.ok(await page.locator(box+' [data-mic-stop]').isEnabled(),'Done is there');
  await shot('2-recording');
  await tap(box+' [data-mic-cancel]');await page.waitForSelector(box+':not(.mic-on)');
  assert.equal(await page.locator('#chat-input').inputValue(),'Sure.','Cancel leaves the text as it was');
  assert.equal(actions.filter(a=>a.action==='voice_transcribe').length,0,'a canceled clip never goes to the Machine');

  // Tap, talk, Done: "Writing it down…", then the words join what was typed. Not sent.
  let release;hold=new Promise(r=>release=r);
  await tap(mic);await page.waitForSelector(box+' .mic-time');await page.waitForTimeout(700);await tap(box+' [data-mic-stop]');
  await page.waitForFunction(()=>document.querySelector('.chat-compose .mic-hint')?.textContent==='Writing it down…');
  await shot('3-transcribing');release();hold=null;
  await page.waitForFunction(()=>!document.querySelector('.chat-compose .mic-bar'));
  assert.equal(await page.locator('#chat-input').inputValue(),'Sure. '+said,'the text lands after what was typed');
  assert.ok(await page.locator('[data-chat-send]').isEnabled(),'Send is ready for the owner to press');
  assert.equal(sent(),0,'nothing is sent');
  const clip=actions.find(a=>a.action==='voice_transcribe');assert.equal(clip.upload,'voice');
  const wav=Buffer.from(clip.args.data,'base64');
  assert.equal(wav.toString('latin1',0,4)+wav.toString('latin1',8,12),'RIFFWAVE');
  assert.deepEqual([wav.readUInt16LE(22),wav.readUInt32LE(24),wav.readUInt16LE(34)],[1,16000,16],'16 kHz mono 16-bit');
  assert.ok(Math.abs(wav.readUInt32LE(40)/32000-1.5)<0.05,'the whole clip, resampled');

  if(scheme==='light'){
   // Hold: let go to stop
   await page.locator('#chat-input').fill('');actions.length=0;
   const mb=await page.locator(mic).boundingBox();await page.mouse.move(mb.x+mb.width/2,mb.y+mb.height/2);await page.mouse.down();
   await page.waitForSelector(box+' .mic-time');await page.waitForTimeout(900);await page.mouse.up();
   await page.waitForFunction(()=>document.querySelector('#chat-input').value.length>0);
   assert.equal(await page.locator('#chat-input').inputValue(),said,'held and let go: it stops and writes');

   // The first time: the Machine gets voice ready (packages, then the model with a percentage), then writes it
   local={state:'missing'};await page.locator('#chat-input').fill('');actions.length=0;
   await page.evaluate(()=>{micPrepped=false});
   await tap(mic);await page.waitForSelector(box+' .mic-time');await page.waitForTimeout(600);await tap(box+' [data-mic-stop]');
   await page.waitForFunction(()=>/Getting voice ready/.test(document.querySelector('.chat-compose .mic-hint')?.textContent||''));
   assert.ok(actions.some(a=>a.action==='voice_prepare'),'the first tap asks the Machine to get ready');
   local={state:'preparing',step:'model',done:42,total:100};
   await page.waitForFunction(()=>document.querySelector('.chat-compose .mic-hint')?.textContent==='Getting voice ready… 42%');
   await shot('4-getting-ready');
   local={state:'ready'};
   await page.waitForFunction(()=>document.querySelector('#chat-input').value.length>0,null,{timeout:8000});
   assert.equal(await page.locator('#chat-input').inputValue(),said,'then it writes it');

   // The Machine can't be reached: the clip is kept and Try again sends it
   await page.locator('#chat-input').fill('');drop=1;
   await tap(mic);await page.waitForSelector(box+' .mic-time');await page.waitForTimeout(600);await tap(box+' [data-mic-stop]');
   await page.waitForSelector(box+' .mic-err');assert.match(await page.locator(box+' .mic-err').textContent(),/Can’t reach your Machine/);
   await shot('5-offline');
   await tap(box+' [data-mic-retry]');await page.waitForFunction(()=>document.querySelector('#chat-input').value.length>0);
   assert.equal(await page.locator('#chat-input').inputValue(),said);

   // The microphone is blocked, or there is none: it says so, and × closes it
   await page.locator('#chat-input').fill('');
   for(const [mode,text] of [['denied',/microphone is blocked/],['none',/No microphone found/]]){
    await page.evaluate(m=>{window.__mic.mode=m},mode);await tap(mic);await page.waitForSelector(box+' .mic-err');
    assert.match(await page.locator(box+' .mic-err').textContent(),text);
    assert.ok(await page.evaluate(()=>{const b=document.querySelector('.chat-compose .mic-bar'),e=b.querySelector('.mic-err').getBoundingClientRect(),r=b.getBoundingClientRect();return e.top>=r.top&&e.bottom<=r.bottom}),'the whole message shows');if(mode==='denied')await shot('6-blocked');
    await tap(box+' [data-mic-cancel]');await page.waitForSelector(box+':not(.mic-on)')}
   await page.evaluate(()=>{window.__mic.mode='ok'});

   // The 2-minute limit: the last 15 seconds count down, then it stops by itself and writes what it has
   await page.locator('#chat-input').fill('');
   await tap(mic);await page.waitForSelector(box+' .mic-time');await page.evaluate(()=>{window.__skew=110000});
   await page.waitForFunction(()=>/left$/.test(document.querySelector('.chat-compose .mic-time')?.textContent||''));
   assert.ok(await page.locator(box+' .mic-live.near').count(),'the clock turns orange near the limit');
   await shot('7-near-limit');
   await page.evaluate(()=>{window.__skew=121000});
   await page.waitForFunction(()=>document.querySelector('#chat-input').value.length>0);
   assert.equal(await page.evaluate(()=>window.__mic.stopped>0),true,'it stopped by itself');
   await page.evaluate(()=>{window.__skew=0});
   assert.equal(sent(),0,'still nothing sent');
  }

  // New to-do: the mic next to Add; the text lands in the box and Add waits for the owner
  await page.goto(base);await page.waitForTimeout(600);
  await page.evaluate(()=>ncOpen());
  await page.locator('#new-card[open] #nc-text').waitFor();
  await tap('#new-card [data-mic]');await page.waitForSelector('#new-card .mic-time');await page.waitForTimeout(700);
  await shot('8-new-todo-recording');
  await tap('#new-card [data-mic-stop]');await page.waitForFunction(()=>document.querySelector('#nc-text').value.length>0);
  assert.equal(await page.locator('#nc-text').inputValue(),said);assert.ok(await page.locator('#nc-add').isEnabled(),'Add is ready');
  assert.ok(await page.locator('#new-card[open]').count(),'the to-do waits for Add');
  await shot('9-new-todo-text');
  await page.keyboard.press('Escape');

  // Help: the same in the question box
  await page.evaluate(()=>helpOpen('ask'));await page.locator('#help-panel[open] #help-q').waitFor();
  await tap('#help-panel [data-mic]');await page.waitForSelector('#help-panel .mic-time');await page.waitForTimeout(600);
  await tap('#help-panel [data-mic-stop]');await page.waitForFunction(()=>document.querySelector('#help-q').value.length>0);
  assert.equal(await page.locator('#help-q').inputValue(),said);assert.ok(await page.locator('#help-go').isEnabled());
  assert.equal(actions.filter(a=>a.action==='help_ask').length,0,'the question waits for Ask');
  await shot('10-help');
  await page.evaluate(()=>document.querySelector('#help-panel').close());

  // Settings, General, Voice input
  await page.evaluate(()=>showSettings('general'));await page.waitForSelector('#settings-dictation:not([hidden]) #dictation-engine');
  assert.equal(await page.locator('#dictation-engine option[value="openai"]').isDisabled(),true,'With OpenAI needs a key');
  await page.locator('#settings-dictation').scrollIntoViewIfNeeded();await shot('11-settings');
  actions.length=0;await page.selectOption('#dictation-language','nl');await page.waitForFunction(()=>true);
  await page.waitForTimeout(200);assert.deepEqual(actions.find(a=>a.action==='voice_prefs')?.args,{language:'nl'});
  await context.close()}

 // The site's demo (a sealed frame: no microphone, and {demo:true} for the voice actions): it says where voice works
 demo=true;
 for(const [w,h] of [[390,844],[1440,900]]){
  const phone=w<500,context=await browser.newContext({viewport:{width:w,height:h},isMobile:phone,hasTouch:phone,deviceScaleFactor:2,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.addInitScript(FAKE_MIC);await context.addInitScript(()=>{window.__mic.mode='denied'});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#chat='+id);await page.locator('#chat-input').waitFor();await page.waitForTimeout(600);
  const box='.chat-compose .chat-box';actions.length=0;
  await (phone?page.locator(box+' [data-mic]').tap():page.locator(box+' [data-mic]').click());
  await page.waitForSelector(box+' .mic-err');
  assert.equal(await page.locator(box+' .mic-err').textContent(),'Voice input works on your own Machine. This demo can’t listen.');
  if(SHOTS)await page.screenshot({path:`${SHOTS}/12-demo-${w}-light.png`});
  await page.locator(box+' [data-mic-cancel]').click();
  await page.evaluate(()=>showSettings('general'));await page.waitForSelector('#settings-dictation:not([hidden])');
  await page.waitForFunction(()=>/This demo can’t listen/.test(document.querySelector('#dictation-list').textContent));
  assert.equal(actions.filter(a=>a.action==='voice_transcribe').length,0);
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('voice input dashboard ok');
