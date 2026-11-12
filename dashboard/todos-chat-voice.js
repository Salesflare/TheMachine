// Voice input (voice_input.py): the mic in a message box. Tap to talk and tap again to stop, or hold it while talking.
// The clip becomes 16 kHz mono WAV here and goes to the Machine, which writes it out (on the Machine itself, or with the
// owner's OpenAI key when they picked that in Settings). The text lands in the box to read and edit: nothing is sent. The
// clip stays only in this page's memory until its text is back. Never the browser's own speech recognition: in Chrome
// that sends the audio to Google, and Firefox has none.
const MIC=html`<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="3" width="6" height="11.5" rx="3"/><path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3"/></svg>`;
const CHECK=html`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>`;
const MIC_MAX=120,MIC_HOLD=600;
const micBtn=()=>html`<button type="button" class="chat-mic" data-mic aria-label="Talk" title="Talk">${raw(MIC)}</button>`;
let mic=null,micPrepped=false,micDemo=false,micUse='';  // the one recording at a time; whether this page asked the Machine; the site's demo (it answers {demo:true}); what a tap does now (voice_view's use)
const MIC_DEMO='Voice input works on your own Machine. This demo can’t listen.';
// In the mobile app the phone asks itself (window.machinePhone, mobile/www/inject.js): a No there just stops, and only
// when the phone won't ask again is there one line with Open settings. An app from before that: the old line.
const micBlocked=()=>document.documentElement.classList.contains('in-app')?t('The microphone is blocked. Allow it for The Machine in the phone’s settings.'):t('The microphone is blocked. Allow it for this site in your browser’s settings.');
async function micDenied(){const p=window.machinePhone;if(!p)return {msg:micBlocked()};let s='';try{s=await p.state('mic')}catch{}
 return s==='blocked'?{msg:t('The microphone is off for The Machine.'),settings:true}:null}
// A No for good comes back at once, while the finger that tapped the microphone is still down: that tap's click
// doesn't open settings
let settingsShown=0;
const SETTINGS_BTN=cls=>{settingsShown=Date.now();return html`<button type="button" class="${cls}" data-phone-settings>${t('Open settings')}</button>`};
document.addEventListener('click',e=>{if(!e.target.closest('[data-phone-settings]'))return;e.preventDefault();e.stopPropagation();if(Date.now()-settingsShown<600)return;
 window.machinePhone?.settings().catch(()=>{});micCancel();if(talk?.state==='error')talkEnd()},true);
const micOk=()=>!!(window.isSecureContext&&navigator.mediaDevices?.getUserMedia&&window.MediaRecorder&&window.OfflineAudioContext);
const micClock=s=>`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
const micPost=(action,args={},upload=false)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf,...(upload?{'X-Upload':'voice'}:{})},body:JSON.stringify({action,args})});
function micClose(v){if(v.box){v.box.classList.remove('mic-on');v.box.querySelector(':scope>.mic-bar')?.remove()}if(mic===v)mic=null}
function micRelease(v){clearInterval(v.tick);v.tick=null;try{v.stream?.getTracks().forEach(x=>x.stop())}catch{}try{v.meter?.close()}catch{}v.meter=null}
function micCancel(){const v=mic;if(!v)return;mic=null;if(v.sr){try{v.sr.abort()}catch{}v.sr=null}if(v.rec){v.rec.onstop=null;try{if(v.rec.state!=='inactive')v.rec.stop()}catch{}}micRelease(v);micClose(v);document.getElementById(v.input)?.focus({preventScroll:true})}
// The Machine is back (or Try now was tapped): a clip that waited goes now. Safe to call before this part of the page has run.
// Recording itself (micStart, micStop, micSend) is the lazy 'voice' part (todos-chat-voice-rec.js): there whenever mic is set.
function micResume(){try{if(mic?.state==='wait')micSend(mic)}catch{}}
document.addEventListener('pointerdown',e=>{const b=e.target.closest('[data-mic]');if(!b||e.button>0||b.disabled)return;e.preventDefault();const at=Date.now();lazyRun('voice',()=>micStart(b,at));
 addEventListener('pointerup',()=>{const v=mic;if(v&&v.down===at&&v.state==='rec'&&Date.now()-at>=MIC_HOLD)micStop()},{once:true})});  // held: let go to stop
document.addEventListener('click',e=>{const b=e.target.closest('[data-mic],[data-mic-stop],[data-mic-cancel],[data-mic-retry]');if(!b)return;e.preventDefault();e.stopPropagation();
 if(b.hasAttribute('data-mic')){if(e.detail===0)lazyRun('voice',()=>micStart(b,0));return}  // pointerdown started it; a key press (Enter, Space) has no pointer
 if(b.hasAttribute('data-mic-stop'))micStop();else if(b.hasAttribute('data-mic-cancel'))micCancel();else if(mic?.wav)micSend(mic)},true);
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&mic){e.preventDefault();e.stopPropagation();micCancel()}},true);  // before a dialog closes on it
document.addEventListener('close',e=>{if(mic&&e.target.contains?.(mic.box))micCancel()},true);
