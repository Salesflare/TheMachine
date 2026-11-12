// A lazy part (dashboard_parts.LAZY 'voice'): recording and writing out what the mic heard. todos-chat-voice.js starts
// it through micStart() on a tap of the mic; nothing here runs before that.
// The first tap gets the Machine's own engine ready while the owner talks (a download the first time only).
// What a tap does is asked once: OpenAI or this Machine; on Automatic while this Machine's own isn't ready yet, the
// browser's own speech recognition (it never waits on a download); with On this Machine picked, the recording waits.
// Each tap also has the Machine load the engine in use (warm) while the owner talks, so Done doesn't wait for it.
async function micPrep(){if(micPrepped){micPost('voice_status',{warm:true}).then(s=>{if(s.use)micUse=s.use}).catch(()=>{});return}
 micPrepped=true;try{const s=await micPost('voice_status',{warm:true});if(s.demo)micDemo=true;micUse=s.use||''}catch{micPrepped=false}}
const micSR=()=>window.SpeechRecognition||window.webkitSpeechRecognition;
const MIC_BCP={de:'de-DE',en:'en-US',es:'es-ES',fr:'fr-FR',it:'it-IT',nl:'nl-NL',pt:'pt-BR'};
// The browser's own speech recognition, while this Machine's own engine isn't ready: what it hears is kept as it goes
function micBrowser(v){const SR=micSR(),sr=new SR(),code=(state.dictation?.language||document.documentElement.lang||'en').slice(0,2);
 Object.assign(sr,{lang:MIC_BCP[code]||'en-US',continuous:true,interimResults:true});v.sr=sr;v.heard=[];v.interim='';v.browser=true;
 sr.onresult=e=>{let now='';for(let i=e.resultIndex;i<e.results.length;i++){const r=e.results[i];if(r.isFinal)v.heard.push(r[0].transcript.trim());else now+=r[0].transcript}v.interim=now.trim()};
 sr.onerror=e=>{if(mic!==v||e.error==='no-speech'||e.error==='aborted')return;v.srFailed=e.error==='not-allowed'||e.error==='service-not-allowed'?'blocked':'other'};
 // Chrome stops after a pause: it goes on until Done, the cross or 2 minutes
 sr.onend=()=>{if(mic!==v)return;if(v.state==='rec'&&!v.srFailed){try{sr.start()}catch{}return}
  if(v.state==='work'){const text=[...v.heard,v.interim].filter(Boolean).join(' ');v.sr=null;
   if(!text&&v.srFailed){micFail(v,v.srFailed==='blocked'?micBlocked():t('Your browser’s speech recognition didn’t answer. Try again.'));return}micDone(v,text)}}
 sr.start()}
function micPaint(v){if(!v.box.isConnected){const box=document.getElementById(v.input)?.closest('.chat-box,.mic-wrap');if(!box){micCancel();return}v.box=box}
 let bar=v.box.querySelector(':scope>.mic-bar');if(!bar){bar=document.createElement('div');bar.className='mic-bar';bar.setAttribute('role','status');v.box.append(bar)}v.box.classList.add('mic-on');
 const x=html`<button type="button" class="mic-x" data-mic-cancel aria-label="Cancel" title="Cancel">×</button>`,rec=v.state==='rec'||v.state==='start';
 // Drawn once per state, so a button never changes under a finger; the clock, the level and the progress update in place
 const key=v.state+'|'+(v.error||'')+'|'+!!v.wav+'|'+!!v.capped;
 if(bar.dataset.k!==key){bar.dataset.k=key;setHTML(bar,rec?html`${x}<span class="mic-live"><i class="mic-dot" aria-hidden="true"></i><span class="mic-time">0:00</span><span class="mic-wave" aria-hidden="true">${v.levels.map(()=>html`<i></i>`)}</span><span class="mic-hint">${t(v.state==='start'?'Starting the microphone…':v.browser?'Your browser writes this one down.':'Listening…')}</span></span><button type="button" class="chat-send mic-done" data-mic-stop aria-label="Done" title="Done"${v.state==='start'?html` disabled`:''}>${CHECK}</button>`
  :v.state==='error'?html`${x}<span class="mic-live mic-err">${v.error}</span>${v.wav?html`<button type="button" class="mic-retry" data-mic-retry>${t('Try again')}</button>`:v.settings?SETTINGS_BTN('mic-retry'):''}`
  :html`${x}<span class="mic-live"><i class="mic-spin" aria-hidden="true"></i><span class="mic-hint"></span></span><span class="mic-prog" aria-hidden="true"${v.state==='prep'?'':html` hidden`}><i></i></span>`)}
 if(rec){const left=MIC_MAX-v.secs,near=v.state==='rec'&&left<=15,live=bar.querySelector('.mic-live');live.classList.toggle('near',near);
  bar.querySelector('.mic-time').textContent=near?t('{} left',micClock(Math.ceil(left))):micClock(v.secs);
  bar.querySelectorAll('.mic-wave i').forEach((el,i)=>{el.style.height=Math.round(3+v.levels[i]*19)+'px'});
  const heard=micHeard(v);if(heard&&v.state==='rec'){const h=bar.querySelector('.mic-hint');h.classList.add('mic-heard');h.textContent=micTail(heard,matchMedia('(max-width:420px)').matches?26:48)}}
 else if(v.state!=='error'){bar.querySelector('.mic-hint').textContent=v.state==='wait'?t('Kept until you’re back online.'):v.state==='prep'?(v.left!=null?(v.left<=1?t('Getting voice ready… about a minute left'):t('Getting voice ready… about {} minutes left',v.left)):v.pct!=null?t('Getting voice ready… {}%',v.pct):t('Getting voice ready… This takes a few minutes.')):v.capped?t('Stopped at 2 minutes. Writing it down…'):t('Writing it down…');
  const p=bar.querySelector('.mic-prog');p.hidden=v.state!=='prep';p.firstChild.style.width=(v.pct||0)+'%';p.classList.toggle('busy',v.pct==null)}}
function micFail(v,msg){v.state='error';v.error=msg;micRelease(v);micPaint(v)}
async function micStart(btn,down){if(mic)return;const box=btn.closest('.chat-box,.mic-wrap'),input=box?.querySelector('textarea');if(!input)return;
 const v=mic={box,input:input.id,state:'start',chunks:[],levels:Array(18).fill(0),secs:0,down};
 if(!micOk()){micFail(v,t('Voice input doesn’t work in this browser.'));return}
 if(micDemo){micFail(v,t(MIC_DEMO));return}
 micPaint(v);const prep=micPrep();
 let stream;try{stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,channelCount:1}})}
 catch(e){await prep;if(mic!==v)return;const no=!micDemo&&(e?.name==='NotAllowedError'||e?.name==='SecurityError');
  if(no){const d=await micDenied();if(mic!==v)return;if(!d){micCancel();return}v.settings=!!d.settings;micFail(v,d.msg);return}
  micFail(v,micDemo?t(MIC_DEMO):e?.name==='NotFoundError'||e?.name==='OverconstrainedError'?t('No microphone found. Connect one and try again.'):t('The microphone couldn’t start. Try again.'));return}
 if(mic!==v){stream.getTracks().forEach(x=>x.stop());return}  // canceled while the browser asked
 await prep;if(mic!==v){stream.getTracks().forEach(x=>x.stop());return}
 if(micUse==='browser'&&micSR()){try{micBrowser(v)}catch{v.browser=false}
  if(v.browser){Object.assign(v,{stream,state:'rec',t0:Date.now()});micMeter(v,stream);v.tick=setInterval(()=>micTick(v),100);micPaint(v);return}}
 const type=['audio/webm;codecs=opus','audio/mp4','audio/webm','audio/ogg;codecs=opus'].find(x=>MediaRecorder.isTypeSupported?.(x))||'';
 let rec;try{rec=new MediaRecorder(stream,type?{mimeType:type,audioBitsPerSecond:32000}:{})}catch{micFail(v,t('The microphone couldn’t start. Try again.'));stream.getTracks().forEach(x=>x.stop());return}
 Object.assign(v,{stream,rec,state:'rec',t0:Date.now()});
 rec.ondataavailable=e=>{if(e.data?.size)v.chunks.push(e.data)};rec.onstop=()=>micStopped(v);rec.start(1000);
 micMeter(v,stream);if(micUse==='openai'||micUse==='local')micTap(v);v.tick=setInterval(()=>micTick(v),100);micPaint(v)}
// While the owner talks, what they said so far goes to the Machine at each pause (a part, at least MIC_PART.min seconds;
// at most MIC_PART.max without a pause), so after Done only the last few seconds are left to write down. What comes
// back shows in the bar as they talk. If a part fails, the whole clip goes as one, as it does without parts.
const MIC_PART={min:6,max:25,pause:0.7,quiet:0.012};
function micTap(v){const ac=v.meter;if(!ac?.createScriptProcessor)return;
 try{const src=ac.createMediaStreamSource(v.stream),node=ac.createScriptProcessor(4096,1,1);Object.assign(v,{tap:node,pcm:[],pcmLen:0,rate:ac.sampleRate,quiet:0,parts:[],sentTo:0});
  node.onaudioprocess=e=>{if(mic!==v||v.state!=='rec')return;const d=e.inputBuffer.getChannelData(0);v.pcm.push(new Float32Array(d));v.pcmLen+=d.length;
   let sum=0;for(let i=0;i<d.length;i++)sum+=d[i]*d[i];v.quiet=Math.sqrt(sum/d.length)>MIC_PART.quiet?0:v.quiet+d.length;
   const unsent=(v.pcmLen-v.sentTo)/v.rate;if(unsent>=MIC_PART.max||unsent>=MIC_PART.min&&v.quiet/v.rate>=MIC_PART.pause)micPart(v,v.pcmLen)};
  src.connect(node);node.connect(ac.destination)}catch{v.tap=null;v.parts=null}}
function micSlice(v,from,to){const out=new Float32Array(to-from);let at=0;for(const c of v.pcm){const a=Math.max(from-at,0),b=Math.min(to-at,c.length);if(b>a)out.set(c.subarray(a,b),at+a-from);at+=c.length;if(at>=to)break}return out}
function micPart(v,to){const from=v.sentTo,part={text:null};v.sentTo=to;v.parts.push(part);const n=v.parts.length;
 part.done=(async()=>{const wav=await micWavOf(micSlice(v,from,Math.max(to,from+Math.ceil(v.rate*0.35))),v.rate);  // a short last bit gets a little silence
  const r=await micPost('voice_transcribe',{data:micB64(wav),part:n,...(v.lang?{language:v.lang}:{})},true);
  if(r.pending||r.demo||typeof r.text!=='string')throw Error('whole');part.text=r.text;if(!v.lang&&r.language)v.lang=r.language})().catch(()=>{part.failed=true})}
// The end of what it heard, from a word's start, so the newest words show
const micTail=(text,n)=>text.length<=n?text:'…'+(text.slice(-n).match(/\s(\S.*)$/)?.[1]||text.slice(-n));
const micHeard=v=>(v.parts||[]).map(p=>p.text).filter(Boolean).join(' ');
function micMeter(v,stream){try{const ac=new (window.AudioContext||window.webkitAudioContext)(),an=ac.createAnalyser();an.fftSize=512;ac.createMediaStreamSource(stream).connect(an);v.meter=ac;v.analyser=an;v.wave=new Uint8Array(an.fftSize)}catch{}}
function micTick(v){if(mic!==v||v.state!=='rec')return;v.secs=(Date.now()-v.t0)/1000;
 if(v.analyser){v.analyser.getByteTimeDomainData(v.wave);let sum=0;for(const x of v.wave)sum+=((x-128)/128)**2;v.levels=[...v.levels.slice(1),Math.min(1,Math.sqrt(sum/v.wave.length)*4)]}
 if(v.secs>=MIC_MAX){v.capped=true;micStop();return}micPaint(v)}
function micStop(){const v=mic;if(!v||v.state!=='rec')return;v.state='work';micRelease(v);const tail=v.pcmLen-v.sentTo;if(v.parts?.length&&tail>0&&(tail/v.rate>=0.3||v.quiet<tail))micPart(v,v.pcmLen);if(v.sr){try{v.sr.stop()}catch{v.sr.onend?.()}micPaint(v);return}try{v.rec.stop()}catch{micStopped(v)}micPaint(v)}
async function micStopped(v){if(mic!==v)return;const blob=new Blob(v.chunks,{type:v.rec?.mimeType||'audio/webm'});v.chunks=[];
 if((Date.now()-v.t0)<500||!blob.size){micFail(v,t('That was too short. Talk a little longer.'));return}
 if(v.parts?.length){const parts=v.parts;v.parts=null;await Promise.all(parts.map(p=>p.done));if(mic!==v)return;
  if(parts.every(p=>!p.failed)){v.pcm=[];micDone(v,parts.map(p=>p.text).filter(Boolean).join(' '));return}}
 try{v.wav=await micWav(blob)}catch{if(mic===v)micFail(v,t('That recording couldn’t be read. Try again.'));return}micSend(v)}
// MediaRecorder's clip (WebM/Opus, or MP4/AAC on Safari) as 16 kHz mono 16-bit WAV, the one format the Machine takes
async function micWav(blob){const ac=new (window.AudioContext||window.webkitAudioContext)();
 try{return await micWav16(await ac.decodeAudioData(await blob.arrayBuffer()))}finally{try{ac.close()}catch{}}}
// A part: the samples the page heard, at the microphone's own rate
async function micWavOf(samples,rate){const buf=new AudioBuffer({length:Math.max(1,samples.length),numberOfChannels:1,sampleRate:rate});buf.copyToChannel(samples,0);return micWav16(buf)}
async function micWav16(buf){const off=new OfflineAudioContext(1,Math.max(1,Math.ceil(buf.duration*16000)),16000),src=off.createBufferSource();src.buffer=buf;src.connect(off.destination);src.start();
  const pcm=(await off.startRendering()).getChannelData(0),out=new DataView(new ArrayBuffer(44+pcm.length*2)),w=(o,s)=>[...s].forEach((c,i)=>out.setUint8(o+i,c.charCodeAt(0)));
  w(0,'RIFF');out.setUint32(4,36+pcm.length*2,true);w(8,'WAVE');w(12,'fmt ');out.setUint32(16,16,true);out.setUint16(20,1,true);out.setUint16(22,1,true);out.setUint32(24,16000,true);out.setUint32(28,32000,true);out.setUint16(32,2,true);out.setUint16(34,16,true);w(36,'data');out.setUint32(40,pcm.length*2,true);
  for(let i=0;i<pcm.length;i++){const s=Math.max(-1,Math.min(1,pcm[i]));out.setInt16(44+i*2,s<0?s*0x8000:s*0x7fff,true)}return out.buffer}
const micB64=buf=>{const u=new Uint8Array(buf);let s='';for(let i=0;i<u.length;i+=0x8000)s+=String.fromCharCode.apply(null,u.subarray(i,i+0x8000));return btoa(s)};
async function micSend(v){if(mic!==v)return;v.state='work';v.error='';micPaint(v);
 try{const r=await micPost('voice_transcribe',{data:micB64(v.wav)},true);if(mic!==v)return;
  if(r.demo){micDemo=true;micFail(v,t(MIC_DEMO));return}
  if(r.pending){await micReady(v,r.voice);if(mic===v)micSend(v);return}
  micDone(v,r.text||'')}
 catch(err){errCaught(err);if(mic!==v)return;
  // Offline: the clip waits here with the offline bar, and goes when the Machine answers again (or on its Try now)
  if(err.offline){netSet(true,err.restarting);v.state='wait';micPaint(v);return}
  v.state='error';v.error=err.message;micPaint(v)}}
// The Machine's own engine is getting ready (the first time only): its progress, then the clip goes again
async function micReady(v,s){for(;;){if(mic!==v)return;const l=s?.local||{};
  if(l.state==='ready')return;if(l.state==='failed')throw Error(l.error||t('Getting voice ready failed. Try again later.'));
  if(l.state==='missing')await micPost('voice_prepare');
  v.state='prep';v.pct=l.step==='model'&&l.total?Math.min(99,Math.round(100*l.done/l.total)):null;
  // Minutes left from the download's own pace (once it has gone a few seconds), plus about a minute to start it
  if(l.step==='model'&&l.total){const now=Date.now();v.seen=v.seen||{at:now,done:l.done};const secs=(now-v.seen.at)/1000,rate=secs>=4?(l.done-v.seen.done)/secs:0;
   v.left=rate>0?Math.max(1,Math.ceil(((l.total-l.done)/rate+60)/60)):null}else v.left=null;micPaint(v);
  await new Promise(r=>setTimeout(r,1500));s=await micPost('voice_status')}}
function micDone(v,text){const input=document.getElementById(v.input);micClose(v);if(!input)return;text=text.trim();
 if(!text){toast(t('I didn’t catch anything. Try again.'),true);return}
 const a=input.selectionStart??input.value.length,b=input.selectionEnd??a,before=input.value.slice(0,a),after=input.value.slice(b),gap=before&&!/\s$/.test(before)?' ':'',room=input.maxLength>0?input.maxLength-before.length-after.length-gap.length:text.length;
 const put=text.slice(0,Math.max(0,room));input.value=before+gap+put+(after&&!/^\s/.test(after)?' ':'')+after;const at=(before+gap+put).length;
 try{input.setSelectionRange(at,at)}catch{}input.dispatchEvent(new Event('input',{bubbles:true}));if(matchMedia('(pointer:fine)').matches)input.focus({preventScroll:true})}
