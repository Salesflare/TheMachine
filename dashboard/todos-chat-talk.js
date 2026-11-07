// Talk live (talk_live.py): a spoken conversation with The Machine about the open to-do, with OpenAI's Realtime voice.
// The Machine starts the session (the OpenAI sign-in and the session's secret never come here) and hands on this page's
// WebRTC offer; the audio then goes directly between this page and OpenAI. The owner can talk over it (OpenAI stops
// and listens). The voice gets this page's tools: two that read, through the Machine, and `ask_chat`, which hands a
// request to the to-do's chat the way a typed message goes (decideOrWait), so the chat's own rules hold: it can change
// the draft or snooze, never send. Sending by voice: `ask_to_send` only works for the draft shown in this chat (on a
// phone or with the screen off the voice reads it out first) and gets the confirm question; `send_answer` lets the
// Machine judge the owner's next words itself. A clear yes approves that one draft, held a few seconds with Undo in the
// chat ("Approved by voice"). What both sides say goes into the chat. At most 10 minutes, with a warning a minute before.
const WAVE=html`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 10v4M8 7v10M12 4v16M16 7v10M20 10v4"/></svg>`;
let talk=null,talkInfo={at:0,ready:null,busy:false},talkTodos=[];  // the one open conversation; whether this Machine can talk live (asked every 10 minutes); what Talk goes through
const talkOk=()=>talkInfo.ready===true&&!!(window.RTCPeerConnection&&navigator.mediaDevices?.getUserMedia);
const talkBtn=()=>html`<button type="button" class="chat-mic chat-talk" data-talk aria-label="Talk live" title="Talk live"${talkOk()?'':html` hidden`}>${WAVE}</button>`;
async function talkLoad(){if(talkInfo.busy||Date.now()-talkInfo.at<600000)return;talkInfo.busy=true;
 let later=false;try{const r=await micPost('talk_status');talkInfo.ready=r.demo?false:r.ready===true;later=!r.demo&&r.ready==null}catch{}finally{talkInfo.busy=false;talkInfo.at=later?0:Date.now()}
 if(later&&!talkInfo.retry)talkInfo.retry=setTimeout(()=>{talkInfo.retry=null;if(chatOpen())talkLoad()},3000);  // the Machine is still asking OpenClaw
 chatSendState();talkSide()}
// Talk in the sidebar (and the phone drawer): the main conversation, about whatever needs the owner
// Whether this Machine can talk live also comes with the page's status (talk_ready), so Talk shows without asking
function talkFromStatus(){if(typeof state.talk_ready==='boolean'&&talkInfo.ready!==state.talk_ready&&!talkInfo.busy){talkInfo.ready=state.talk_ready;talkSide()}}
// Talk in the sidebar, or T: starts the main conversation, or ends it while it's live (the same as End)
function talkMain(){const was=talk?.main,first=chatOpen()?.id||null;if(talk)talkEnd();if(was||!talkOk())return;talkLog=[];
 talkAfterDrawer(()=>{talkGoView();talkStart(true,first)})}
// The phone drawer closes with a step back in history: Talk's view goes on after that, or that step would undo it
function talkAfterDrawer(go){if(typeof drawerPopping!=='undefined'&&drawerPopping)addEventListener('popstate',()=>setTimeout(go),{once:true});else go()}
function talkSide(){const b=$('#side-talk');if(b){b.hidden=!talkOk()&&!talk?.main;b.setAttribute('aria-pressed',String(!!talk?.main));b.setAttribute('aria-current',talkViewOn()?'page':'false')}}
// Talk's own view (#talk): one transcript for the whole conversation, the to-do it is about now (with its draft: the one
// a spoken yes can send) and the bar. The voice opening a to-do changes that card, never the page the owner is on.
// Each to-do's chat still gets what was said about it, what was decided and what was sent.
let talkLog=[];  // this page's transcript of the main conversation: {role,text}, and {about,title} where the to-do changes
const talkViewOn=()=>!!$('#talk-view')&&!$('#talk-view').hidden;
let talkBack='inbox';
function talkGoView(){if(location.hash==='#talk')talkViewShow();else location.hash='#talk'}
function talkViewShow(){const sec=$('#talk-view');if(sec.hidden)talkBack=!$('#settings').hidden?'settings':document.querySelector('nav button.active')?.dataset.tab||'inbox';
 for(const x of document.querySelectorAll('main>section'))x.hidden=x!==sec;
 for(const b of document.querySelectorAll('nav button')){b.classList.remove('active');b.setAttribute('aria-current','false')}
 $('#open-settings')?.setAttribute('aria-current','false');talkViewPaint();talkPaint();talkSide();scrollTo(0,0);talkFit();requestAnimationFrame(talkFit)}
// Talk's view is as tall as the window below the header: the page doesn't scroll, the transcript and the to-do do
function talkFit(){const sec=$('#talk-view');if(!sec||sec.hidden)return;const log=sec.querySelector('.talk-log'),end=!log||talkAtEnd(log);
 const vh=visualViewport?.height||innerHeight,m=getComputedStyle(sec.parentElement),below=(parseFloat(m.paddingBottom)||0)+(parseFloat(m.marginBottom)||0);
 sec.style.setProperty('--talk-h',Math.max(300,Math.floor(vh-(sec.getBoundingClientRect().top+scrollY)-below))+'px');
 if(log&&end)log.scrollTop=log.scrollHeight;talkMore(sec.querySelector('.talk-about .chat-clamp'))}
const talkAtEnd=el=>el.scrollTop+el.clientHeight>=el.scrollHeight-40;
// The card's draft scrolls inside it: a fade at its bottom while there is more below. Read to its end, it stays there
// when the card gains a row (Send, once the draft was seen). Its text can still lay out later, so the seen tick rechecks it.
const talkMore=c=>{if(!c)return;if(c._end)c.scrollTop=c.scrollHeight;c.classList.toggle('fade-more',c.scrollHeight-c.scrollTop-c.clientHeight>2)};
addEventListener('resize',()=>requestAnimationFrame(talkFit));visualViewport?.addEventListener('resize',()=>requestAnimationFrame(talkFit));
function talkLeave(){if(!talkViewOn())return;if(talkBack==='settings')showSettings();else document.querySelector(`nav [data-tab="${talkBack}"]`)?.click()}
function talkDraftHtml(s){const a=s.status==='prepared'?(s.next_actions||[]).find(a=>a.revision&&(['email','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply'].includes(a.kind)&&a.body||a.kind==='doc_write')):null;if(!a)return '';
 if(a.kind==='doc_write')return html`<div class="chat-draft current"><span hidden data-smart="${a.revision}"></span><div class="chat-draft-head"><span>${docHead(a)}</span></div><div class="chat-clamp dw">${docWriteHtml(a)}</div></div>`;
 const to=a.to_name||(Array.isArray(a.to)?a.to.join(', '):a.to||''),mail=a.kind==='email';
 return html`<div class="chat-draft current"><span hidden data-smart="${a.revision}"></span>${to?html`<div class="chat-draft-head"><span>${t('To: {}',to)}</span></div>`:''}${a.subject&&!a.reply&&!/^re:/i.test(a.subject)?html`<div class="chat-draft-subject">${a.subject}</div>`:''}<div class="chat-clamp${mail?html` mail-text`:''}">${mail?mailHtml(a.body):chatMarkdown(a.body)}</div></div>`}
// Once its send went out (or didn't), Talk's card says so instead of showing the draft: "Sent to Sam · 11:42"
function talkSentHtml(v,s){const sent=(s.next_actions||[]).find(a=>a.state?.status==='sent'),d=v?.done?.[s.id]||(sent?{state:'sent',at:sent.state.sent_at,to:sent.to_name||(Array.isArray(sent.to)?sent.to.join(', '):sent.to||'')}:null);if(!d)return '';
 if(d.state==='sent'){const time=d.at?fmtHM(d.at):'';return html`<p class="talk-about-sent" role="status">${d.to&&time?t('Sent to {} · {}',d.to,time):time?t('Sent at {}',time):d.to?t('Sent to {}',d.to):t('Sent')}</p>`}
 return html`<p class="talk-about-sent failed" role="alert">${t('Didn’t go out.')}${d.why?' '+d.why:''}</p>`}
function talkViewPaint(){const sec=$('#talk-view');if(!sec||sec.hidden)return;const v=talk,live=!!v?.main;
 if(!sec.firstElementChild)setHTML(sec,html`<div class="talk-head"><h2></h2></div><div class="talk-about-slot"></div><div class="chat-log talk-log" aria-live="polite"></div><div class="talk-foot"><div class="talk-again"></div></div>`);
 sec.querySelector('h2').textContent=t('Talk');
 // Ended: where the bar was, "Talk ended." and Start again
 const again=live?'':html`<p class="talk-mark">${t('Talk ended.')}</p>${talkOk()?html`<button type="button" class="talk-again-btn" data-talk-main>${t('Start again')}</button>`:''}`,ag=sec.querySelector('.talk-again');if(ag.innerHTML!==String(again))setHTML(ag,again);ag.hidden=live;
 const s=live&&v.sid?state.suggestions?.find(x=>x.id===v.sid)||(v.done?.[v.sid]?{id:v.sid,title:v.done[v.sid].title}:null):null;
 const about=s?html`<div class="talk-about" data-about="${s.id}"><div class="talk-about-top"><span>${t('Talking about')}</span><a href="#chat=${s.id}">${t('Open the chat')}</a></div><h3 translate="no">${s.title}</h3>${talkSentHtml(v,s)||talkDraftHtml(s)}</div>`:'';
 // At the end of the transcript, it stays there when the card changes (a draft that became "Sent to…" is much shorter)
 const slot=sec.querySelector('.talk-about-slot'),log=sec.querySelector('.talk-log');
 // The newest line stays in view as lines come and the card changes, unless the owner scrolled up to read back
 if(slot.dataset.k!==String(about)){const end=talkAtEnd(log);slot.dataset.k=about;setHTML(slot,about);const c=slot.querySelector('.chat-clamp');if(c){c.scrollTop=0;c.addEventListener('scroll',()=>{c._end=c.scrollTop>0&&c.scrollHeight-c.scrollTop-c.clientHeight<=2;talkMore(c)},{passive:true});new ResizeObserver(()=>talkMore(c)).observe(c)}requestAnimationFrame(()=>talkMore(c));if(end)log.scrollTop=log.scrollHeight}
 const key=talkLog.length+'|'+live;if(log.dataset.k===key)return;const end=!log.dataset.k||talkAtEnd(log);log.dataset.k=key;
 setHTML(log,html`${talkLog.map(x=>x.record?talkRecordHtml(x.record):x.made?html`<p class="talk-mark talk-made">${t('Added a to-do: {}',x.title)}</p>`:x.about?html`<p class="talk-mark" translate="no">${x.title}</p>`:html`<div class="chat-msg ${x.role==='user'?'you':'machine'}"><div class="bubble" translate="no">${x.text}</div></div>`)}${!talkLog.length&&live?html`<p class="talk-mark">${t('Say something to start.')}</p>`:''}`);
 if(end)log.scrollTop=log.scrollHeight}
addEventListener('hashchange',e=>{if(location.hash==='#talk'){if(talk?.main||talkLog.length)talkViewShow();else history.replaceState(null,'',location.pathname+location.search)}
 else if(/#talk$/.test(e.oldURL)&&!/^#chat=/.test(location.hash))talkLeave()});
// "Open the chat" stays in the page, also when the page's base is another path
$('#talk-view')?.addEventListener('click',e=>{const b=e.target.closest('[data-talk-event]');if(b){const title=b.textContent;if('meeting' in b.dataset)openMeeting(b.dataset.talkEvent,title);else openEvent(b.dataset.talkEvent,title);return}
 const a=e.target.closest('a[href^="#chat="]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey)return;e.preventDefault();chatGo(a.getAttribute('href').slice(6))});
if(location.hash==='#talk')history.replaceState(null,'',location.pathname+location.search);  // a reload: the conversation ended with the page
{const sec=document.getElementById('talk-view');if(sec)new MutationObserver(()=>{talkSide();if(!sec.hidden)return;if(location.hash==='#talk')history.replaceState(null,'',location.pathname+location.search);if(talk)talkPaint()}).observe(sec,{attributes:true,attributeFilter:['hidden']})}
// The bar sits above the chat's message box; Talk's own floats at the bottom of the page when no chat is open
// Who Talk's yes sends to, on its Undo bar: "Sending to Sam in 10 s", then "Sent to Sam"; several, "Sending 3 emails in 10 s"
function talkSendingText(x,wait){const items=x.items||[],n=items.length,mail=items.every(i=>i.kind==='email'),to=n===1?String(items[0].to||''):'';
 if(wait==null){const time=n===1&&x.results?.[0]?.at?fmtHM(x.results[0].at):'';
  return n>1?t(mail?'Sent {} emails':'Sent {} messages',n):to&&time?t('Sent to {} · {}',to,time):to?t('Sent to {}',to):time?t('Sent at {}',time):t('Sent')}
 return (n>1?t(mail?'Sending {} emails in {} s':'Sending {} messages in {} s',n,wait):to?t('Sending to {} in {} s',to,wait):t('Sending in {} s',wait)).replace(/(\S+) (\d+) s\b/,'$1\u00a0$2\u00a0s')}
// A send by voice after its Undo window: followed in the Machine's outbox (send_status) until it went out or didn't,
// then the bar and Talk's card say so, and the voice is told once ("Sent."). Never a guess from the clock.
const TALK_SETTLED=['sent','failed','blocked','canceled','none'];
async function talkSentWatch(v,x){if(x.watching)return;x.watching=true;
 for(let n=0;n<80&&talk===v&&!x.undone;n++){
  const out=await Promise.all(x.items.map(i=>micPost('talk_tool',{id:v.id,name:'send_status',args:{id:i.suggestion_id,approval_id:i.approval_id}}).then(r=>r.output||{}).catch(()=>({}))));
  if(talk!==v||x.undone)return;
  if(out.every(o=>TALK_SETTLED.includes(o.state))){x.results=out;x.settledAt=Date.now();
   for(const [k,i] of x.items.entries())(v.done||={})[i.suggestion_id]={...out[k],title:String(state.suggestions?.find(s=>s.id===i.suggestion_id)?.title||v.done?.[i.suggestion_id]?.title||'')};
   const bad=out.filter(o=>o.state!=='sent'),what=x.items.map(i=>i.to).filter(Boolean).join(', ')||'the draft';
   const note=(bad.length?v.notes.not_sent:v.notes.sent)||'';   // the voice's words come from the Machine (talk_live.py)
   if(note)talkTell(v,note.replace('{what}',what).replace('{at}',out[0].time||'').replace('{why}',bad.map(o=>o.why||o.say||'').join(' ').trim()));
   talkPaint();talkViewPaint();refresh().catch(()=>{});if(chatOpen())chatPoll();return}
  await new Promise(ok=>setTimeout(ok,n<10?1000:3000))}
 x.watching=false}
function talkPaint(){const v=talk;if(!v)return;const box=v.main&&talkViewOn()?$('#talk-view .talk-foot'):document.querySelector('.chat-compose');
 if(!box&&!v.main){talkEnd();return}
 let host=box,bar=box?.querySelector(':scope>.talk');
 if(!box){host=$('#talk-dock');if(!host){host=document.createElement('div');host.id='talk-dock';document.body.append(host)}bar=host.querySelector('.talk')}
 document.querySelectorAll('.talk').forEach(x=>{if(x!==bar&&!x.closest('#settings'))x.remove()});if(box)$('#talk-dock')?.remove();
 if(!bar){bar=document.createElement('div');bar.className='talk';if(box)box.insertBefore(bar,box.querySelector('.chat-box'));else host.append(bar)}
 if(!box&&!host.dataset.ro){host.dataset.ro=1;new ResizeObserver(()=>document.body.style.setProperty('--talk-dock-h',host.offsetHeight+'px')).observe(host)}
 const key=v.state+'|'+v.muted+'|'+(v.error||'');
 if(bar.dataset.k!==key){bar.dataset.k=key;
  setHTML(bar,v.state==='error'?html`<div class="talk-bar talk-err" role="alert"><span class="grow">${v.error}</span>${v.settings?SETTINGS_BTN('talk-end'):''}<button type="button" class="talk-end" data-talk-close>${t('Close')}</button></div>`
   :html`<div class="talk-bar" role="status"><span class="talk-live"><i class="talk-dot${v.state==='live'?'':html` wait`}" aria-hidden="true"></i><strong>${t(v.state==='live'?'Live':'Connecting…')}</strong><span class="talk-time"></span></span><span class="talk-hint"></span><button type="button" class="talk-mute" data-talk-mute aria-pressed="${v.muted}"${v.state==='live'?'':html` disabled`}>${t(v.muted?'Unmute':'Mute')}</button><button type="button" class="talk-end" data-talk-end>${t('End')}</button></div>${v.per_use?html`<small class="talk-cost">${t('OpenAI charges your API key per minute of talk.')}</small>`:''}`)}
 if(v.state==='error')return;
 const left=v.limit-v.secs,near=v.state==='live'&&left<=v.limit-v.warn;
 bar.querySelector('.talk-time').textContent=near?t('{} left',micClock(Math.max(0,Math.ceil(left)))):v.state==='live'?micClock(v.secs):'';
 bar.querySelector('.talk-hint').textContent=v.muted?t('Muted'):v.state==='live'&&talkAsking(v)?t('Say yes to send it.'):'';
 // A send by voice waits UNDO_SECONDS with Undo here (tap, or say "undo"), then says Sent for a moment
 const x=v.sent,wait=x?Math.ceil((x.until-Date.now())/1000):0,ok=x?.results?.every(o=>o.state==='sent'),
  kind=x&&!x.undone&&wait>0?'undo':x&&!x.undone&&!x.results?'going':x?.results&&Date.now()-x.settledAt<6000?(ok?'sent':'failed'):x?.undone&&wait>-3?'undone':'';
 if(kind==='going')talkSentWatch(v,x);
 let u=bar.querySelector('.talk-undo');if(!u){u=document.createElement('div');u.className='talk-undo';bar.querySelector('.talk-bar')?.after(u)}
 if(u.dataset.kind!==kind){u.dataset.kind=kind;  // the button stays the same element while the count goes down, so a tap never misses
  setHTML(u,kind==='undo'?html`<span class="talk-sending" role="status"></span><button type="button" class="talk-undo-btn" data-talk-undo>${t('Undo')}</button>`
   :kind==='sent'?html`<span class="talk-sending sent" role="status">${talkSendingText(x)}</span>`:kind==='going'?html`<span class="talk-sending" role="status">${t('Sending…')}</span>`
   :kind==='failed'?html`<span class="talk-sending failed" role="alert">${t('Didn’t go out.')}</span>`:kind==='undone'?html`<span class="talk-sending" role="status">${t('Canceled. It won’t be sent.')}</span>`:'')}
 if(kind==='undo'){const c=u.querySelector('.talk-sending'),text=talkSendingText(x,wait);if(c.textContent!==text)c.textContent=text}
 u.hidden=!kind;
 bar.querySelector('.talk-live').classList.toggle('near',near)}
function talkFail(v,msg){if(talk!==v)return;talkClose(v);v.state='error';v.error=msg;talk=v;talkPaint()}
function talkClose(v){clearInterval(v.tick);v.closed=true;talkWake(v);talkMedia(v);try{v.dc?.close()}catch{}try{v.pc?.close()}catch{}try{v.stream?.getTracks().forEach(x=>x.stop())}catch{}
 if(v.audio){v.audio.srcObject=null;v.audio.remove()}if(v.id&&!v.ended){v.ended=true;micPost('talk_end',{id:v.id}).catch(()=>{})}}
let talkLimitToast='';  // the limit's toast is about that session only: cleared when another starts or ends
function talkToastClear(){const t=$('#toast');if(talkLimitToast&&t?.textContent===talkLimitToast)t.classList.remove('show');talkLimitToast=''}
function talkEnd(){const v=talk;if(!v)return;talk=null;talkToastClear();talkClose(v);document.querySelectorAll('.chat-compose>.talk,.talk-foot>.talk').forEach(x=>x.remove());$('#talk-dock')?.remove();document.body.style.removeProperty('--talk-dock-h');talkSide();talkViewPaint()}
async function talkStart(main,first=null){const s=main?null:chatOpen();if(talk||!main&&!s||main&&!talkOk())return;talkToastClear();micCancel();
 const v=talk={main:!!main,sid:s?.id||null,state:'start',muted:false,secs:0,limit:600,warn:540,per_use:false,said:new Set(),posting:Promise.resolve(),queue:[],relay:null,heard:{},responding:false,tell:[],pending:new Set(),dropped:new Set(),respFor:{},after:{},known:new Set(talkNeeds().map(x=>x.id)),prep:new Set(),sent:null,last:null,told:new Set(),lastUser:''};talkPaint();talkSide();talkViewPaint();
 try{v.stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,channelCount:1}})}
 catch(e){if(e?.name==='NotAllowedError'||e?.name==='SecurityError'){const d=await micDenied();if(talk!==v)return;if(!d){talkEnd();return}
   v.settings=!!d.settings;talkFail(v,d.msg);return}
  talkFail(v,e?.name==='NotFoundError'||e?.name==='OverconstrainedError'?t('No microphone found. Connect one and try again.'):t('The microphone couldn’t start. Try again.'));return}
 if(talk!==v){v.stream.getTracks().forEach(x=>x.stop());return}
 try{const r=await micPost('talk_start',{...(main?{main:true}:{suggestion_id:s.id}),languages:[...(navigator.languages||[])].slice(0,8)});if(talk!==v){micPost('talk_end',{id:r.id}).catch(()=>{});return}
  Object.assign(v,{id:r.id,limit:r.limit||600,warn:r.warn||540,per_use:!!r.per_use,tools:r.tools||[],instructions:r.instructions||'',note:r.ask_note||'',notes:r.notes||{},voice:r.voice||'',speed:r.speed||0,turn:r.turn||null,noise:r.noise||null,transcription:r.transcription||null,transcriptionNext:r.transcription_next||null,languages:r.languages||['en']});talkPaint();
  if(v.main&&(first||chatOpen()))talkFocus(v,first||chatOpen().id);  // started from a to-do's chat: that one first
  const pc=v.pc=new RTCPeerConnection();v.audio=document.createElement('audio');v.audio.autoplay=true;v.audio.hidden=true;document.body.append(v.audio);
  pc.ontrack=e=>{v.audio.srcObject=e.streams[0];v.audio.play?.().catch(()=>{})};pc.addTrack(v.stream.getAudioTracks()[0],v.stream);
  pc.onconnectionstatechange=()=>{if(talk===v&&['failed','disconnected'].includes(pc.connectionState))talkLost(v)};
  v.stream.getAudioTracks()[0]?.addEventListener('ended',()=>talkLost(v));  // iPhone stops the mic when the app leaves the screen
  const dc=v.dc=pc.createDataChannel('oai-events');dc.onopen=()=>talkReady(v);dc.onmessage=e=>talkEvent(v,e.data);
  const offer=await pc.createOffer();await pc.setLocalDescription(offer);
  const a=await micPost('talk_offer',{id:v.id,sdp:offer.sdp});if(talk!==v)return;await pc.setRemoteDescription({type:'answer',sdp:a.sdp})}
 catch(err){if(err.offline)netSet(true,err.restarting);talkFail(v,err.offline&&!err.slow?t('Offline. Start it again when you’re back online.'):err.message||t('Talk live couldn’t start. Try again.'))}}
// The voice's own setup: this page's instructions and tools (never the Gateway's agent), and what the owner says written down
function talkReady(v){if(talk!==v)return;v.state='live';v.t0=Date.now();talkWake(v);talkMedia(v);
 v.dc.send(JSON.stringify({type:'session.update',session:{type:'realtime',instructions:v.instructions,tools:v.tools,tool_choice:'auto',audio:{input:{transcription:v.transcription||{model:'gpt-4o-mini-transcribe'},...(v.noise?{noise_reduction:v.noise}:{}),...(v.turn?{turn_detection:v.turn}:{})},output:{...(v.voice?{voice:v.voice}:{}),...(v.speed?{speed:v.speed}:{})}}}}));
 v.dc.send(JSON.stringify({type:'session.update',session:{type:'realtime',include:['item.input_audio_transcription.logprobs']}}));
 if(v.transcriptionNext)v.dc.send(JSON.stringify({type:'session.update',session:{type:'realtime',audio:{input:{transcription:v.transcriptionNext}}}}));  // the newer model with every language pinned; refused, the one above stays  // how sure the transcript is (talkNoise); alone, so a refusal changes nothing else
 v.tick=setInterval(()=>talkTick(v),250);talkPaint()}
function talkTick(v){if(talk!==v)return;if(!v.main&&chatOpen()?.id!==v.sid){talkEnd();return}
 if(talkDue(v))return;
 if(v.relay&&!chat?.active&&Date.now()-v.relay.at>20000)talkTurnDone();  // a turn that ended between two looks
 if(v.main)talkNew(v);
 talkPaint()}
// What has to happen at a moment, from the clock (wall time since it went live), not from counting ticks: timers
// slow down in the background, so this also runs on the voice's events and when the page shows again (talkTick is
// the backstop). end_talk ends once its goodbye has been heard; the limit ends it; a waiting note goes when it can.
function talkDue(v,flush=true){if(talk!==v||v.state!=='live')return false;v.secs=(Date.now()-v.t0)/1000;
 if(v.ending&&(Date.now()-v.ending>10000||!v.playing&&!v.responding&&(v.byeHeard||Date.now()-v.ending>1500))){talkEnd();return true}
 if(v.secs>=v.limit){talkEnd();talkLimitToast=v.main?t('Talk ends after 30 minutes. Start it again to go on.'):t('Talk live ends after 10 minutes. Start it again to go on.');toast(talkLimitToast);return true}
 if(flush)talkTellNext(v);return false}
// The connection or the microphone went away. In the background (a phone's lock screen, an iPhone leaving the app)
// it ends cleanly and says so, with Start again; on screen it shows the error.
function talkLost(v){if(talk!==v||v.closed)return;if(document.hidden||v.hiddenAt){talkEnd();toast(t('Talk stopped while in the background.'))}
 else talkFail(v,t('Talk live lost its connection. Start it again to go on.'))}
// Keeps going in the background: the screen stays on while it is live (Wake Lock, taken again when the page shows),
// and the lock screen or notification shows it with Mute and End (Media Session). Where a browser has neither,
// nothing happens.
async function talkWake(v){const on=talk===v&&v.state==='live'&&!v.closed&&!document.hidden;
 if(!on){const w=v.wake;v.wake=null;try{await w?.release()}catch{}return}
 if(v.wake&&!v.wake.released||!navigator.wakeLock?.request)return;
 try{v.wake=await navigator.wakeLock.request('screen');if(talk!==v||v.closed){v.wake.release().catch(()=>{});v.wake=null}}catch{}}
function talkMedia(v){const m=navigator.mediaSession;if(!m)return;const on=talk===v&&v.state==='live'&&!v.closed;
 const handle=(name,fn)=>{try{m.setActionHandler(name,on?fn:null)}catch{}};
 try{m.metadata=on&&typeof MediaMetadata==='function'?new MediaMetadata({title:t('Talk'),artist:'The Machine',artwork:[{src:new URL('brand/app-icon-192.png',document.baseURI).href,sizes:'192x192',type:'image/png'}]}):null}catch{}
 handle('pause',()=>talkMute(v,true));handle('play',()=>talkMute(v,false));handle('stop',()=>talkEnd());handle('hangup',()=>talkEnd());
 handle('togglemicrophone',()=>talkMute(v,!v.muted));
 try{m.playbackState=on?v.muted?'paused':'playing':'none'}catch{}
 // A promise: Chrome refuses an unmute without a tap on the page (talkReady runs when the connection opens, the lock
 // screen's play is no tap). The microphone itself started from the tap on Talk; only the browser's indicator waits.
 try{if(on)m.setMicrophoneActive?.(!v.muted)?.catch?.(()=>{})}catch{}}
document.addEventListener('visibilitychange',()=>{const v=talk;if(!v)return;
 if(document.hidden){v.hiddenAt=Date.now();return}
 v.hiddenAt=0;if(v.state!=='live')return;
 // Back on screen: is it still there? A connection or microphone that went away while hidden ends cleanly.
 const mic=v.stream?.getAudioTracks()[0];
 if(['failed','closed','disconnected'].includes(v.pc?.connectionState)||v.dc&&v.dc.readyState!=='open'||mic?.readyState==='ended'){v.hiddenAt=1;talkLost(v);return}
 if(!talkDue(v)){talkWake(v);talkPaint()}});
// Talk works on the to-do on screen: the one the voice opens, or the one the owner opens. A send question about another is dropped.
function talkFocus(v,id){if(talk!==v||v.sid===id)return v.focusing;v.sid=id;v.asked=null;v.askedAt=0;v.queue=[];v.relay=null;talkEager(v,false);
 if(v.main){talkLog.push({about:id,title:String(state.suggestions?.find(x=>x.id===id)?.title||'').slice(0,200)});talkViewPaint()}
 return v.focusing=micPost('talk_focus',{id:v.id,suggestion_id:id}).catch(()=>{})}
// Every open to-do, in the order the dashboard shows them, each with its state in plain words (talk_live.STATES; one that
// looks done sits in Done and isn't here):
// what needs the owner (Ready, To decide) first. At most 30; counts has them all.
const talkWho=s=>String((s.people||[])[0]?.name||'').slice(0,80);
const TALK_STATE={ready:'ready',needs:'to decide',preparing:'preparing',waiting:'waiting on others',later:'snoozed'};
const talkNeeds=()=>talkTodos.filter(([,l])=>l==='ready'||l==='needs').map(([s])=>s);
function talkList(){const counts={};for(const [,l] of talkTodos)counts[TALK_STATE[l]]=(counts[TALK_STATE[l]]||0)+1;
 return {todos:talkTodos.slice(0,30).map(([s,l])=>({id:s.id,state:TALK_STATE[l],title:String(s.title||'').slice(0,200),...(talkWho(s)?{from:talkWho(s)}:{}),...(s.handoff_still?.name?{with:String(s.handoff_still.name).slice(0,80)}:{})})),count:talkTodos.length,counts}}
async function talkOpen(v,id){if(!/^[a-f0-9]{16}$/.test(id))return {error:'No to-do with that id. Use list_todos or find_todos.'};  // a closed one too (Done / dismissed)
 const known=state.suggestions?.some(s=>s.id===id);
 if(!known)try{await micPost('talk_focus',{id:v.id,suggestion_id:id})}catch{return {error:'No to-do with that id. Use list_todos or find_todos.'}}
 if(chatOpen()&&chatOpen().id!==id)talkGoView();await talkFocus(v,id);
 try{const out=(await micPost('talk_tool',{id:v.id,name:'todo_details',args:{}})).output;
  const mark=talkLog.findLast(x=>x.about===id);if(mark&&!mark.title&&out?.title){mark.title=String(out.title).slice(0,200);const l=$('#talk-view .talk-log');if(l)l.dataset.k='';talkViewPaint()}  // one the page hasn't loaded
  return out}catch(err){return {error:err.message}}}
// A new to-do, by voice: the same as New to-do (card_new, Work or Personal as the list shows), never sent anywhere.
// The voice stays on the to-do in focus; the transcript gets a mark, and it isn't announced as new.
async function talkCreate(v,args){const title=String(args.title||'').replace(/\s+/g,' ').trim().slice(0,200),note=String(args.note||'').trim().slice(0,1500);
 if(!title)return {error:'Say what the to-do is.'};
 try{const made=await micPost('card_new',{text:title+(note?'\n'+note:''),scope:scopeFilter==='work'||scopeFilter==='personal'?scopeFilter:null,due:null,due_at:null,about:[],attach:[]});
  v.known.add(made.id);if(talk===v&&v.main){talkLog.push({made:made.id,title});talkViewPaint()}refresh().catch(()=>{});
  return {ok:true,id:made.id,title,note:'Added to their list. Say so in a few words. The to-do in focus is still the same.'}}
 catch(err){return {error:err.message||'Couldn’t add the to-do.'}}}
// A to-do's own buttons, by voice (todo_action): the same decide and card_rename actions the card and the Done /
// dismissed list use, offered only where the page offers them. Never a send.
const talkGo=(id,choice,extra={},feedback='')=>{const step={choice,feedback,decision_id:crypto.randomUUID(),...extra};
 return OUTBOX_CHOICES.includes(choice)?decideOrWait(id,[step],choice):decidePost(id,step)};
// What Talk did last (undo_last_action takes it back on that to-do). A to-do Talk closes or snoozes takes what its chat
// was still on with it: no answer, no "the chat stopped" later.
function talkDid(v,id,act,s){if(act==='reopen'||act==='unsnooze')v.told.delete('quiet:'+id);v.last={id,act,title:String(s?.title||'').slice(0,200),at:Date.now()};if(['mark_done','dismiss','snooze'].includes(act))talkDrop(v,id)}
function talkDrop(v,id){if(v.relay?.sid===id)v.relay=null;if(v.sid===id)v.queue=[];v.told.add('quiet:'+id)}
// A snooze by voice, for any time the owner says: minutes from now, or a local time the Machine reads in the owner's
// time zone (a time without an offset is theirs, never UTC), or a preset. The time said back is local there too.
function talkSnoozeWhen(args){const m=Math.round(Number(args.snooze_minutes)),until=String(args.snooze_until||'').trim();
 if(m>0)return {snoozed_until:new Date(Date.now()+Math.min(m,525600)*60000).toISOString()};
 if(until)return {snoozed_until:until};
 return {snooze_option:['2h','tomorrow','3d','1w'].includes(args.snooze)?args.snooze:'tomorrow'}}
const talkZone=()=>state?.hours?.timezone||Intl.DateTimeFormat().resolvedOptions().timeZone;
function talkLocal(v){const tz=talkZone(),d=new Date(v);try{return d.toLocaleString('en-US',{timeZone:tz,weekday:'long',month:'long',day:'numeric',hour:'numeric',minute:'2-digit'})}catch{return d.toLocaleString('en-US')}}
async function talkDo(v,args){const id=String(args.id||v.sid||''),act=String(args.action||''),s=state.suggestions?.find(x=>x.id===id);
 if(!/^[a-f0-9]{16}$/.test(id))return {error:'Say which to-do: open it first, or give its id.'};
 const say=(text,extra={})=>{refresh().catch(()=>{});talkDid(v,id,act,s);return {ok:true,...extra,note:text}};
 const go=(choice,extra={},feedback='')=>talkGo(id,choice,extra,feedback);
 const open=s&&!closed(s);
 try{
  if(act==='rename'){const title=String(args.title||'').replace(/\s+/g,' ').trim().slice(0,200);if(!title)return {error:'Say the new title.'};
   await micPost('card_rename',{suggestion_id:id,title,reset:false,decision_id:crypto.randomUUID()});return say('Renamed. Say so in a few words.',{title})}
  if(act==='reopen'){const undo=s?.undo_until&&Date.parse(s.undo_until)>Date.now();
   if(s&&!closed(s))return {error:'It is open already.'};
   if(s?.status==='rejected'&&!undo||!s&&args.dismissed)return {error:'It was dismissed too long ago to bring back. Offer to add it again with create_todo.'};
   if(s){await go(s.status==='completed'&&!(undo&&s.expired_at)?'reopen':'undo');return say('Reopened. Say so in a few words.')}
   try{await go('reopen')}catch{try{await go('undo')}catch{return {error:'It was dismissed too long ago to bring back. Offer to add it again with create_todo.'}}}
   return say('Reopened. Say so in a few words.')}
  if(!open)return {error:s?'It is closed. Reopen it first.':'No open to-do with that id. Use list_todos or find_todos.'};
  if(act==='mark_done'){await go('complete');return say('Marked done. Say so in a few words.')}
  if(act==='dismiss'){await go('reject',{},String(args.why||'').trim().slice(0,1000));return say('Marked not needed. Say so in a few words.')}
  if(act==='snooze'){const r=await go('snooze',talkSnoozeWhen(args));
   return r?.snoozed_until?say('Snoozed until {until}, the owner’s local time. Say so in a few words.'.replace('{until}',talkLocal(r.snoozed_until)),{until:talkLocal(r.snoozed_until),time_zone:talkZone()}):say('Snoozed. Say so in a few words.')}
  if(act==='unsnooze'){if(s.status!=='snoozed')return {error:'It isn’t snoozed.'};await go('accept');return say('Back on the list. Say so in a few words.')}
  if(act==='try_again'){if(s.preparation_status!=='blocked')return {error:'Nothing is stuck there.'};await go('retry');return say('Trying again. Say so in a few words.')}
  if(act==='not_done'){if(!looksDone(s))return {error:'It doesn’t look done.'};await go('not_done');return say('Back on the list. Say so in a few words.')}
  return {error:'Unknown action.'}}
 catch(err){refresh().catch(()=>{});return {error:err.message||'That didn’t work.'}}}
// The to-do's Do it, by voice (do_it): the same accept the button sends, where the page offers it (waiting for a decision,
// or a result that only answered). The Machine's job does the work, browser included, and shows on the to-do. "Continue"
// on one that is already running lets it run.
const talkRunning=s=>['queued','starting','running'].includes(s.preparation_status)||['queued','starting','running'].includes(s.agent?.status);
const talkAnswered=s=>{try{return s.status==='prepared'&&JSON.parse(s.outcome||'{}').state==='answered'}catch{return false}};
async function talkDoIt(v,args={}){const id=String(args.id||v.sid||''),s=state.suggestions?.find(x=>x.id===id);
 if(!/^[a-f0-9]{16}$/.test(id)||!s)return {error:'Say which to-do: open it first, or give its id.'};
 if(closed(s))return {error:'It is closed. Reopen it first (todo_action reopen).'};
 if(talkRunning(s))return {ok:true,running:true,note:'It is already running. Let it run: say so in a few words, and that they can follow it on the to-do.'};
 if(s.status==='snoozed')return {error:'It is snoozed. Bring it back first (todo_action unsnooze).'};
 if(s.status==='prepared'&&!talkAnswered(s)&&s.preparation_status!=='blocked')return {error:'It has a draft ready. Sending goes through ask_to_send; changes through ask_chat.'};
 if(s.status!=='pending'&&!talkAnswered(s)&&s.preparation_status!=='blocked')return {error:'There is nothing to start on it.'};
 try{await talkGo(id,s.preparation_status==='blocked'&&s.status!=='pending'?'retry':'accept');s.preparation_status='queued';refresh().catch(()=>{});talkDid(v,id,'do_it',s);  // started: a second "do it" before the refresh lets it run
  return {ok:true,started:true,note:'The Machine started on it, browser work included. Say so in a few words, and that they can follow it on the to-do.'}}
 catch(err){refresh().catch(()=>{});return {error:err.message||'That didn’t work.'}}}
// A correction right after an action (undo_last_action): taken back on the to-do that action touched, which opens again
const TALK_UNDO={mark_done:['reopen','Marked done'],dismiss:['reopen','Marked not needed'],snooze:['unsnooze','Snoozed'],rename:['rename','Renamed']};
async function talkUndoLast(v){const l=v.last;if(!l||Date.now()-l.at>600000)return {error:'Nothing you did is left to undo.'};
 const how=TALK_UNDO[l.act];if(!how)return {error:l.act==='do_it'?'The Machine’s job has started; it can be stopped on the to-do itself.':'That can’t be undone from here.'};
 const r=await talkDo(v,{id:l.id,action:how[0],...(l.act==='rename'?{title:l.title}:{})});v.last=null;if(r.error)return r;
 if(v.main)await talkOpen(v,l.id);
 return {ok:true,undid:how[1],id:l.id,title:l.title,note:`Undid "${how[1]}" on "${l.title}" and opened it again. Say what you undid in a few words, then do what the owner meant on this to-do.`}}
// Undo, by voice or on the bar: every send still waiting from Talk's last yes (talk_undo, as the chat's Undo)
async function talkUndoSend(v){const x=v.sent;if(!x||x.undone||Date.now()>x.until)return {error:'Nothing is waiting to send any more.'};x.undone=true;talkPaint();let n=0;
 for(const item of x.items)try{await micPost('talk_undo',{suggestion_id:item.suggestion_id,approval_id:item.approval_id});n++}catch{}
 refresh().catch(()=>{});if(chatOpen())chatPoll();
 return n?{ok:true,canceled:n,note:'Canceled. Nothing was sent. Say so in a few words.'}:{error:'It was already on its way.'}}
// Report a bug, by voice (report_bug): the same report Help's Report a bug sends, with what the owner agreed to add
async function talkBug(v,args={}){const summary=String(args.summary||'').trim().slice(0,3000);if(!summary)return {error:'Say what went wrong first.'};
 if(typeof bugHosted!=='function'||!bugHosted()&&!state.fleet)return {error:'This Machine isn’t linked to an account, so the report can’t go from here. Say they can email support@themachine.computer.'};
 const s=v.sid&&state.suggestions?.find(x=>x.id===v.sid),parts=[`From Talk: ${summary}`];
 if(args.context===true){if(s)parts.push(`To-do in focus: ${String(s.title||'').slice(0,200)}`);if(v.recent?.length)parts.push('Last lines in Talk:\n'+v.recent.join('\n'))}
 const body={description:parts.join('\n\n').slice(0,8000),screenshot:null},diag=args.support_report===true;
 const saved={ok:true,status:'saved',note:'Saved, it goes out by itself soon. Say exactly that in a few words, nothing more.'};
 try{const r=bugHosted()?await bugHostedKeep(body,diag):await bugAction('bug_send',{...body,diagnostics:diag});
  if(r?.queued)return saved;
  if(r?.completed){const done=await Promise.race([r.completed,new Promise(ok=>setTimeout(()=>ok({later:true}),10000))]);
   if(done.error)return {error:`The report didn’t go out: ${String(done.error.message||'').slice(0,200)}`};if(done.later||done.sent?.queued)return saved}
  return {ok:true,status:'sent',note:'Say only: "Sent the bug report." Don’t say it is being looked into or fixed.'}}
 catch(err){return {error:err.message||'The report didn’t go out.'}}}
// How the Machine is doing, as Connections and Needs you show it (machine_status)
function talkStatus(){const rh=state.review_health||{};
 return {connections:(state.connectors||[]).slice(0,30).map(c=>{const h=connectorHealth(c);return {name:String(c.display_name||c.email||c.id).slice(0,80),source:service(c.service),state:String(h.text||'Connected').slice(0,120),...(h.tone==='orange'?{needs_owner:true}:{})}}),
  reviews:{on:state.reviews_on!==false,waiting:rh.pending||0,...(rh.last_completed?{last:rh.last_completed}:{})},
  needs_owner:[...document.querySelectorAll('#needs-you li>span')].map(x=>x.textContent.trim()).filter(Boolean).slice(0,8)}}
// Anything else, by voice (ask_machine): a new to-do the way New to-do makes one, with the request handed to its chat
// (talk_live.ASK_PREFIX: the chat's own rules, it never sends). Its turn is followed here; the answer goes to the voice.
async function talkMachine(v,req){
 try{const made=await micPost('card_new',{text:req,scope:scopeFilter==='work'||scopeFilter==='personal'?scopeFilter:null,due:null,due_at:null,about:[],attach:[]});v.known.add(made.id);
  if(talk===v){talkLog.push({made:made.id,title:req.split('\n')[0].slice(0,200)});talkViewPaint()}
  const r=await decideOrWait(made.id,[{choice:'other',feedback:req,decision_id:'chat-voice-'+crypto.randomUUID()}],'other');
  refresh().catch(()=>{});talkWatch(v,made.id,req);
  return {ok:true,waiting:!!r?.waiting,note:v.note}}
 catch(err){return {error:err.message||'Couldn’t add the to-do.'}}}
// Its answer is the chat's reply; a turn that ended without one, or never started in two minutes, says it stopped.
async function talkWatch(v,id,req=''){const at=Date.now();let busy=false;
 for(let n=0;n<400&&talk===v;n++){await new Promise(ok=>setTimeout(ok,1500));if(talk!==v)return;
  const r=await talkChatRead(id);if(!r||r.unavailable)continue;if(r.active){busy=true;continue}
  const said=talkReplies(r.items||[]).map(i=>String(i.text||'').trim()).filter(Boolean);
  if(said.length||busy||Date.now()-at>120000){await refresh().catch(()=>{});talkChatSaid(v,id,said.join(' ').slice(0,3000),req);return}}}
// A record the voice opened (open_record): a small card in the transcript, opening its own page or the meeting
const TALK_KIND={person:'Person',organization:'Organization',project:'Project',meeting:'Meeting',message:'Message',promise:'Promise'};
function talkRecordHtml(c){const title=(c.title||''),go=c.node?html`<a href="${graphHash(c.node)}">${title}</a>`:c.promise?html`<a href="${promiseHref({id:c.promise})}">${title}</a>`
  :c.event?html`<button type="button" class="talk-record-open" data-talk-event="${String(c.event)}"${c.kind==='meeting'?html` data-meeting`:''}>${title}</button>`:title;
 return html`<div class="talk-record"><span class="talk-record-kind">${t(TALK_KIND[c.kind]||'Message')}</span><strong translate="no">${go}</strong>${c.line?html`<small translate="no">${c.line}</small>`:''}</div>`}
// A to-do that comes to need the owner while Talk is open (Ready or To decide): a short heads-up at the next pause
// (talkTellNext waits while either side talks), once. One that was preparing says it's ready now (notes.ready).
function talkNew(v){if(!v.dc||v.state!=='live')return;for(const [s,l] of talkTodos)if(l==='preparing')v.prep.add(s.id);
 for(const s of talkNeeds())if(!v.known.has(s.id)){v.known.add(s.id);const note=v.prep.has(s.id)&&v.notes.ready||v.notes.new||'{title}';
  talkTell(v,note.replace('{title}',String(s.title||'').slice(0,200)).replace('{from}',talkWho(s)||'unknown'))}}
// What the voice says is kept once its response is done, unless the owner talked over it (OpenAI stops it): a cut-off start
// ("The chat is on…") never lands in the chat.
async function talkEvent(v,data){if(talk!==v)return;let e;try{e=JSON.parse(data)}catch{return}
 if(e.type==='input_audio_buffer.speech_started')v.speaking=true;
 else if(e.type==='input_audio_buffer.speech_stopped'){v.speaking=false;setTimeout(()=>talkTellNext(v),1200)}
 else if(e.type==='input_audio_buffer.committed'){v.lastItem=e.item_id;if(e.item_id)v.pending.add(e.item_id)}
 else if(e.type==='conversation.item.input_audio_transcription.completed')talkHeard(v,e);
 else if(e.type==='conversation.item.input_audio_transcription.failed')talkHeard(v,{item_id:e.item_id,transcript:'',failed:true,error:e.error});
 else if(e.type==='response.created'){v.responding=true;if(e.response?.id&&v.lastItem)v.respFor[e.response.id]=v.lastItem;v.lastItem=null}
 else if(e.type==='response.output_audio_transcript.done')(v.heard[e.response_id]||=[]).push([e.transcript,e.item_id]);
 else if(e.type==='response.done'){v.responding=false;const id=e.response?.id,said=v.heard[id]||[],to=v.respFor[id];delete v.heard[id];delete v.respFor[id];
  if(e.response?.status!=='cancelled'&&!v.dropped.has(to)){const keep=()=>said.forEach(([text,item])=>talkLine(v,'assistant',text,item));
   if(to&&v.pending.has(to)){(v.after[to]||=[]).push(keep);setTimeout(()=>talkHeard(v,{item_id:to,transcript:null}),4000)}else keep()}  // a reply to words not yet written down waits for them
  talkTellNext(v)}
 else if(e.type==='output_audio_buffer.started')v.playing=true;
 else if(e.type==='output_audio_buffer.stopped'||e.type==='output_audio_buffer.cleared')v.playing=false;
 else if(e.type==='response.function_call_arguments.done')talkTool(v,e);
 if(v.ending&&e.type==='output_audio_buffer.stopped')v.byeHeard=true;
 talkDue(v,false)}  // every event of the voice's: the goodbye heard, the limit (a waiting note goes on response.done)
// What the owner said, once written down. A noise, a sound or a few words in a script the owner's languages don't use
// (gpt-realtime heard "음력?" or "แก" in a rustle) isn't kept, and the voice's reply to it is stopped and dropped too.
// transcript null: the transcript never came (a reply waiting on it is kept).
function talkHeard(v,e){const item=e.item_id;if(!v.pending.has(item)&&e.transcript==null)return;v.pending.delete(item);
 const heardIn=Array.isArray(e.languages)?e.languages.map(talkLang).filter(Boolean):[],mine=(v.languages||['en']).map(talkLang);
 const noise=e.transcript!=null&&talkNoise(e.transcript,e.logprobs,v.transcription?.prompt),foreign=!noise&&e.transcript!=null&&!talkShort(e.transcript)&&(talkForeign(e.transcript,v.languages)||heardIn.length>0&&!heardIn.some(l=>mine.includes(l)));  // gpt-transcribe says which language it heard
 if(noise||foreign){v.dropped.add(item);if(v.dc?.readyState==='open'){
   if(item)v.dc.send(JSON.stringify({type:'conversation.item.delete',item_id:item}));  // out of what the voice remembers
   for(const [id,to] of Object.entries(v.respFor))if(to===item&&v.responding){v.dc.send(JSON.stringify({type:'response.cancel',response_id:id}));v.dc.send(JSON.stringify({type:'output_audio_buffer.clear'}))}}
  if(e.failed&&e.error)console.warn('Talk: transcription failed',e.error?.code||'',e.error?.message||'');
  if(foreign||e.failed)talkMiss(v,e.failed)}
 else if(e.transcript){v.misses=0;v.unheardTold=false;v.lastUser=String(e.transcript).trim();talkLine(v,'user',e.transcript,item)}
 const after=v.after[item]||[];delete v.after[item];if(!noise&&!foreign)after.forEach(f=>f())}
// Words that didn't come through (another language, or a transcription that failed): the first time "Sorry, say that
// again?" (notes.again). Twice in a row, or a failed transcription, says once what's wrong instead (notes.unheard: it
// can't make out their words, check the microphone or type), then stays quiet until a line comes through, never a loop.
function talkMiss(v,failed){v.misses=(v.misses||0)+1;
 if(v.unheardTold)return;
 if(!failed&&v.misses<2){talkTell(v,v.notes.again||'');return}
 v.unheardTold=true;talkTell(v,v.notes.unheard||v.notes.again||'')}
// A language gpt-transcribe says it heard: [{code:'fr'}] in its events, an ISO 639-1 code ('fr', 'pt-BR') or a 639-3
// one ('fra'); a plain string too. Read as 'fr', or as the 639-3 code when the app has no such language.
const TALK_ISO3={eng:'en',nld:'nl',dut:'nl',deu:'de',ger:'de',fra:'fr',fre:'fr',spa:'es',ita:'it',por:'pt'};
const talkLang=x=>{const c=String((x&&typeof x==='object'?x.code??x.language:x)??'').trim().toLowerCase().split(/[-_]/)[0];
 return /^[a-z]{2,3}$/.test(c)?TALK_ISO3[c]||c:''};
// The short answers and commands Talk listens for (yes, no, ok, send it, stop, undo, next…, in the app's languages): never
// taken for noise, however unsure the transcript is (talk_live.YES has the same yes words)
const TALK_SHORT=new Set(`yes yeah yep yup ok okay sure send it go ahead no nope nah stop undo wait cancel next previous back skip done dismiss snooze again please now do them all both ja jawel jep oke okee nee neen niet doe maar verstuur stuur hoor prima goed klopt wacht volgende vorige terug klaar nein jawohl klar genau gut bitte oui non daccord si vale claro sim nao certo bye goodbye thanks thank cheers doei dag bedankt tschuss danke merci ciao grazie adios gracias tchau obrigado`.split(' '));
const talkWords=text=>String(text||'').toLowerCase().normalize('NFKD').replace(/\p{M}/gu,'').replace(/[’']/g,'').match(/[\p{L}\p{N}]+/gu)||[];
const talkShort=text=>{const w=talkWords(text);return w.length>0&&w.length<=3&&w.every(x=>TALK_SHORT.has(x))};
// Whether a transcript is noise rather than words: nothing but marks, mostly letters of another script than Latin (the
// app's languages all write in it), the transcription prompt itself, or a short line the model was unsure of (its
// average logprob, when OpenAI sends them). A short answer or command ("yes", "ja", "send it", "undo") is never noise.
function talkNoise(text,logprobs,prompt){const s=String(text||'').normalize('NFC').trim();
 const letters=s.match(/\p{L}/gu)||[];if(!letters.length&&!/\p{N}/u.test(s))return true;
 const latin=letters.filter(c=>/\p{Script=Latin}/u.test(c)).length;if(latin*2<letters.length)return true;
 if(talkShort(s))return false;
 const flat=x=>String(x||'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim();if(prompt&&flat(s)&&flat(prompt).includes(flat(s))&&flat(s).split(' ').length>2)return true;
 const lp=(Array.isArray(logprobs)?logprobs:[]).map(x=>+x?.logprob).filter(Number.isFinite);
 return lp.length>0&&s.split(/\s+/).length<=3&&lp.reduce((a,b)=>a+b,0)/lp.length<-1.2}
// A few words in a language the owner doesn't speak ("Ja, liebe den Movon.", "Nun liebt's." when they speak English and
// Dutch): the transcription guessed from noise or a mumble. Words only one app language uses tell; shared ones ("ja") don't.
const TALK_MARK={en:'the and you this that what with have please thanks yes yeah okay next send would could should',
 nl:'het een ik niet wat dat maar voor ook nog wel toch goed doe stuur volgende graag hoor alsjeblieft bedankt zeker jij',
 de:'ich nicht und ist das nun auch wir mit auf fur aber noch schon sehr bitte danke liebe liebt gibt doch kein keine jetzt mich dich uns euch haben habe hat wird gut endet ein eine einen dem',
 fr:'je tu nous vous est le la les une oui mais avec pour cest merci tres ca qui que quoi dans sur du des au aux il elle',
 es:'el los las una por para con pero muy gracias esta yo usted hola bueno como porque tambien',
 it:'lo gli che sono non ma grazie ciao molto questo questa perche anche',
 pt:'nao sim obrigado obrigada voce uma isso estou tudo bem tambem'};
const talkMarks=(()=>{const seen={},out={};for(const [l,w] of Object.entries(TALK_MARK))for(const x of w.split(' '))(seen[x]||=new Set()).add(l);
 for(const [x,ls] of Object.entries(seen))if(ls.size===1)out[x]=[...ls][0];return out})();
// Letters with marks each app language writes; one none of the owner's languages has ("Güzel." for English and Dutch,
// Turkish from a mumble) tells too, unless a word of their own is in the line ("send it to José").
const TALK_LETTERS={en:'',nl:'éëïèóáêöç',de:'äöüß',fr:'éèêàâçëïîôûùœÿ',es:'áéíóúñü',it:'àèéìòù',pt:'áâãàçéêíóôõú'};
function talkForeign(text,languages){const mine=new Set((languages||['en']).map(x=>String(x).slice(0,2))),w=talkWords(text);if(!w.length||w.length>10||talkShort(text))return false;
 const langs=w.map(x=>talkMarks[x]).filter(Boolean);if(langs.some(l=>mine.has(l)))return false;if(langs.length)return true;
 const ok=new Set([...mine].map(l=>TALK_LETTERS[l]||'').join('')),odd=[...String(text).toLowerCase().normalize('NFC')].filter(c=>/\p{L}/u.test(c)&&!/[a-z]/.test(c));
 return w.length<=4&&odd.some(c=>!ok.has(c))}
// What one side said goes into the chat as an ordinary message (and is kept by the Machine, talk_line)
const talkNoDash=text=>String(text||'').replace(/\s*\u2014\s*|\s+\u2013\s+/g,', ').replace(/,\s*([.,!?])/g,'$1').replace(/^,\s*/,'');
function talkLine(v,role,text,item){text=talkNoDash(String(text||'').trim());  // spoken style: no dashes, either side
 const key=role+':'+(item||text);if(!text||v.said.has(key))return;v.said.add(key);
 v.posting=Promise.all([v.posting,micPost('talk_line',{id:v.id,role,text}).catch(()=>{})]);  // kept before the Machine judges an answer
 (v.recent||=[]).push((role==='user'?'Owner: ':'Talk: ')+text.slice(0,300));v.recent=v.recent.slice(-8);
 if(v.main){talkLog.push({role,text});talkViewPaint()}
 if(chat&&chatOpen()?.id===v.sid){chat={...chat,items:[...(chat.items||[]),{kind:role==='user'?'you':'reply',text,via:'live',at:Date.now()}]};paintChat();chatToEnd()}}
// Before anything that changes something: the owner's latest words must be words. A noise dropped after their last line,
// or one odd word ("azk" taken as "ask"), gets "Sorry, say that again?" and nothing is done.
const TALK_CHANGES=['create_todo','todo_action','do_it','undo_last_action','report_bug','ask_machine'];
const talkUnclear=(v,e)=>v.dropped.has(v.respFor[e.response_id])||!!v.lastUser&&talkWords(v.lastUser).length===1&&!talkShort(v.lastUser);
async function talkTool(v,e){let args={},output;try{args=JSON.parse(e.arguments||'{}')}catch{}
 // The owner said they're done: it ends the way End does, once its goodbye has been heard (talkTick)
 if(e.name==='end_talk'&&talkUnclear(v,e)){if(v.dc?.readyState==='open'){v.dc.send(JSON.stringify({type:'conversation.item.create',item:{type:'function_call_output',call_id:e.call_id,output:JSON.stringify({error:'What the owner said wasn’t clear, so Talk goes on.',note:v.notes.again||'Say only: "Sorry, say that again?"'})}}));v.dc.send(JSON.stringify({type:'response.create'}))}return}
 if(e.name==='end_talk'){v.ending=Date.now();if(v.dc?.readyState==='open')v.dc.send(JSON.stringify({type:'conversation.item.create',item:{type:'function_call_output',call_id:e.call_id,output:JSON.stringify({ok:true})}}));return}
 if(TALK_CHANGES.includes(e.name)&&talkUnclear(v,e))output={error:'What the owner said wasn’t clear, so nothing was done.',note:v.notes.again||'Say only: "Sorry, say that again?"'};
 else if(e.name==='ask_chat'){const req=String(args.request||'').trim().slice(0,2000);output=req?await talkAsk(v,req):{error:'Say what to ask.'};if(output.ok&&!output.note)output.note=output.queued?v.notes.queued||v.note:v.note}
 else if(e.name==='list_todos'&&v.main)output=talkList();
 else if(e.name==='create_todo')output=await talkCreate(v,args);
 else if(e.name==='machine_status'&&v.main)output=talkStatus();
 else if(e.name==='todo_action')output=await talkDo(v,v.main?args:{...args,id:v.sid});  // a to-do's own Talk: that to-do only
 else if(e.name==='do_it'&&v.main)output=await talkDoIt(v,args);
 else if(e.name==='undo_last_action')output=await talkUndoLast(v);
 else if(e.name==='undo_send')output=await talkUndoSend(v);
 else if(e.name==='report_bug')output=await talkBug(v,args);
 else if(e.name==='ask_machine'&&v.main){const req=String(args.request||'').trim().slice(0,2000);output=req?await talkMachine(v,req):{error:'Say what to ask.'}}
 else if(e.name==='open_todo'&&v.main)output=await talkOpen(v,String(args.id||''));
 else if(e.name==='ask_to_send_all'&&v.main)output=await talkAskSend(v,{ids:Array.isArray(args.ids)?args.ids.map(String).slice(0,8):[]});
 else if(v.main&&!v.sid&&['ask_chat','read_draft','ask_to_send'].includes(e.name))output={error:'No to-do is open. Call open_todo first.'};
 else if(e.name==='read_draft')output=await talkAskSend(v,{...args,read:true});
 else if(e.name==='ask_to_send')output=await talkAskSend(v,args);
 else if(e.name==='send_answer')output=await talkAnswer(v);
 else try{output=(await micPost('talk_tool',{id:v.id,name:e.name,args})).output}catch(err){output={error:err.message}}
 if(output?.card){const card=output.card;delete output.card;if(talk===v&&v.main){talkLog.push({record:card});talkViewPaint()}}  // open_record: shown in the transcript
 if(talk!==v||v.dc?.readyState!=='open')return;
 v.dc.send(JSON.stringify({type:'conversation.item.create',item:{type:'function_call_output',call_id:e.call_id,output:JSON.stringify(output)}}));
 v.dc.send(JSON.stringify({type:'response.create'}))}
// The draft the voice may ask to send: the current one in this chat, on screen (scrolled into view). On a phone or with
// the screen off, the owner may not see it, so the voice reads it out in full before the question.
const talkShown=v=>$('#send-dialog')?.open?null:chatOpen()?.id===v.sid?document.querySelector('#chat-log .chat-draft.current [data-smart]')
 :v.main&&v.sid&&talkViewOn()?document.querySelector(`#talk-view .talk-about[data-about="${CSS.escape(v.sid)}"] .chat-draft.current [data-smart]`):null;
// A send question is open: asked, not yet answered, and not too old
const talkAsking=v=>!!v.asked&&Date.now()-(v.askedAt||0)<180000;  // the Machine's question is open (talk_live.ASK_SECONDS)
// The voice reads the whole draft out, so the screen isn't needed (a phone in a pocket, another page). When this
// to-do's draft shows (Talk's card, its chat), that one is asked about; else the Machine picks it (its only one, or the
// number the voice gives). The Machine pins the revision; a changed draft is asked about again.
async function talkAskSend(v,args={}){const b=args.ids?null:talkShown(v);b?.closest('.chat-draft')?.scrollIntoView({block:'nearest'});
 try{const r=await micPost('talk_ask_send',{id:v.id,...(args.ids?{ids:args.ids}:{}),...(b?{revision:b.dataset.smart}:{}),...(Number.isInteger(args.draft)?{draft:args.draft}:{}),...(args.read?{read:true}:{})});
  if(r.question){v.asked=r.revision||'all';v.askedAt=Date.now();talkEager(v,true)}return r}
 catch(err){return {error:err.message}}}
// While a yes or no is expected, the turn ends sooner after a short answer (semantic_vad's high eagerness): a lone "yes"
// isn't left waiting for more, so the owner doesn't say it twice. Otherwise Talk waits patiently (low).
function talkEager(v,on){if(!v.turn||v.dc?.readyState!=='open'||!!v.eager===on)return;v.eager=on;
 v.dc.send(JSON.stringify({type:'session.update',session:{type:'realtime',audio:{input:{turn_detection:on?{...v.turn,eagerness:'high'}:v.turn}}}}))}
// The owner answered: what was said is kept first, then the Machine judges it (its own record, not the voice's word).
// The answer can still be on its way from OpenAI, so it asks again for a few seconds.
async function talkAnswer(v){let r={status:'not_asked'};
 for(let i=0,tries=v.asked?14:1;i<tries&&talk===v;i++){  // the owner's words can still be on their way from OpenAI (up to ~10 s)
  await v.posting;try{r=await micPost('talk_send',{id:v.id})}catch(err){return {error:err.message}}
  if(!['no_answer','not_asked'].includes(r.status))break;await new Promise(ok=>setTimeout(ok,700))}
 if(r.status==='queued'){v.asked=null;v.sent={items:r.sent||[{suggestion_id:v.sid,approval_id:r.approval_id}],until:Date.now()+(r.undo_ms??(r.undo_seconds||10)*1000)};talkPaint();await refresh();if(chatOpen()?.id===v.sid)chatPoll()}
 else if(!['no_answer','not_asked','unclear'].includes(r.status))v.asked=null;
 if(!v.asked)talkEager(v,false);
 return r}
// What the voice asks the chat goes the way a typed message does (chatSubmit's decideOrWait, so it can wait offline
// too), as a hand-off (talk_live.RELAY_PREFIX): the chat doesn't show it as the owner's message (what they said is
// there already), and its drafts wait for their Approve. A request while the chat is still on one never stops it:
// it waits and goes when that turn ends. Then the chat's answer goes straight to the voice, which tells the owner.
// Talk's own commands never go to a chat: moving between to-dos, stopping, leaving it ("next one" once had the payroll
// chat research the next to-do). "Continue" on one whose Do it hasn't started is its Do it; on a running one, nothing.
const TALK_NAV=/^(?:(?:ok(?:ay)?|oké|ja|yes|so|alright|right|and|en)[,.!]?\s+)?(?:let'?s\s+|laten we\s+)?(?:(?:go\s+(?:to\s+)?)?(?:the\s+)?next(?:\s+one)?|move\s+on(?:\s+to\s+(?:the\s+)?next(?:\s+one)?)?|skip(?:\s+(?:it|this(?:\s+one)?))?|(?:the\s+)?previous(?:\s+one)?|go\s+back|back|stop|leave\s+it|never\s?mind|(?:de\s+)?volgende|ga\s+(?:maar\s+)?door(?:\s+naar\s+de\s+volgende)?|vorige|terug|overslaan|laat\s+(?:het|maar)(?:\s+maar)?|stop\s+maar)(?:\s+(?:please|now|then|maar|dan|alsjeblieft))*[.!]?$/i;
const TALK_GO_ON=/^(?:(?:ok(?:ay)?|ja|yes)[,.!]?\s+)?(?:(?:please\s+)?(?:continue|carry\s+on|let\s+it\s+(?:continue|run|go\s+on)|go\s+on\s+with\s+it|ga\s+verder|doorgaan|laat\s+(?:het|hem)\s+(?:maar\s+)?(?:verder\s+gaan|doorgaan|lopen)))(?:\s+(?:please|now|maar))?[.!]?$/i;
async function talkAsk(v,req){const s=state.suggestions?.find(x=>x.id===v.sid);if(!s)return {error:'This to-do is gone.'};
 if(TALK_NAV.test(req.trim()))return {error:'That is for you, not the chat: move between to-dos with list_todos and open_todo, and for "stop" or "leave it" do nothing more. Nothing was asked.'};
 if(TALK_GO_ON.test(req.trim())&&v.main){const r=await talkDoIt(v,{id:s.id});return r.error&&!talkRunning(s)?{error:`Nothing to continue there. ${r.error}`}:r}
 if(v.relay||chat?.active&&chatOpen()?.id===s.id){v.queue.push(req);return {ok:true,queued:true}}
 return talkRelay(v,s,[req])}
const talkReplies=(items=chat?.items||[])=>items.filter(i=>i.kind==='reply'&&i.via!=='live');
const talkChatRead=id=>micPost('card_chat',{suggestion_id:id}).catch(()=>null);
async function talkRelay(v,s,reqs){const here=chatOpen()?.id===s.id,seen=here?null:await talkChatRead(s.id);if(talk!==v||v.sid!==s.id)return {error:'This to-do is no longer open.'};
 const relay=v.relay={at:Date.now(),replies:talkReplies(here?undefined:seen?.items||[]).length,sid:s.id,request:reqs.join(' ').slice(0,300)};
 const steps=[...(s.status==='completed'?[{choice:'reopen',feedback:'',decision_id:crypto.randomUUID()}]:[]),{choice:'other',feedback:reqs.join('\n'),decision_id:'chat-talk-'+crypto.randomUUID()}];
 try{const r=await decideOrWait(s.id,steps,'other');
  if(chatOpen()?.id===s.id){chat={...(chat||{}),active:!r?.waiting,cursor:null};changing.delete(s.id)}
  if(!r?.waiting){await refresh();if(chatOpen()?.id===s.id){paintChat();chatToEnd();chatPoll()}else talkFollow(v,relay)}
  return {ok:true,waiting:!!r?.waiting}}
 catch(err){v.relay=null;return {error:err.message}}}
// The chat's turn ended: its answer goes to the voice at once (no checking back), then what waited goes
// The chat isn't on screen (Talk's own view, another page): its turn is followed here, the way an open chat polls it
async function talkFollow(v,relay){let busy=false;
 for(let n=0;n<400&&talk===v&&v.relay===relay;n++){await new Promise(ok=>setTimeout(ok,1500));if(talk!==v||v.relay!==relay||chatOpen()?.id===relay.sid)return;  // an open chat takes over
  const r=await talkChatRead(relay.sid);if(!r||r.unavailable||talk!==v||v.relay!==relay)continue;if(r.active){busy=true;continue}
  if(busy||talkReplies(r.items||[]).length>relay.replies||Date.now()-relay.at>20000){await refresh().catch(()=>{});talkTurnDone(r.items||[]);return}}}
function talkTurnDone(items){const v=talk;if(!v||talk.state!=='live')return;if(!items){if(chatOpen()?.id!==v.sid)return;items=chat?.items||[]}
 if(v.relay){const relay=v.relay,said=talkReplies(items).slice(relay.replies).map(i=>String(i.text||'').trim()).filter(Boolean).join(' ').slice(0,3000);v.relay=null;
  talkChatSaid(v,relay.sid,said,relay.request)}
 if(v.queue.length){const s=state.suggestions?.find(x=>x.id===v.sid),reqs=v.queue;v.queue=[];if(s)talkRelay(v,s,reqs)}}
// What a chat Talk asked came back with, told about that to-do (its title, so an answer never passes for another one's).
// A to-do that was closed or snoozed meanwhile (by Talk or on screen) says nothing; a chat that stopped on its own is
// told once per to-do, with what was asked, so "ask again" asks that again.
function talkChatSaid(v,id,said,request){const s=state.suggestions?.find(x=>x.id===id);
 if(!s||closed(s)||s.status==='snoozed'||v.told.has('quiet:'+id))return;
 const title=String(s.title||'').slice(0,200);
 if(said){v.told.delete('stop:'+id);talkTell(v,(v.notes.done||'{answer}').replace('{title}',title).replace('{answer}',said));return}
 if(v.told.has('stop:'+id))return;v.told.add('stop:'+id);
 talkTell(v,(v.notes.stopped||'').replace('{title}',title).replace('{request}',String(request||'').slice(0,300)))}
// Seen on screen: a draft shown in full (on its to-do, in its chat or on Talk's card) for a moment is told to the Machine
// (draft_seen) with the text it showed. A send by voice then only asks its question; a changed draft counts as new.
// Cut short (Show more, Show all) isn't seen; a draft in its own scroll box is seen once scrolled from top to end.
const draftSeen={done:new Set(),seen:new Map()};
function draftSeenBoxes(){const out=[],c=chatOpen();
 for(const box of document.querySelectorAll('article.card .draft[data-rev]')){const id=(box.closest('article')?.id||'').replace(/^task-/,'');if(id)out.push([box,id,box.dataset.rev,box.querySelector('.db')])}
 if(c)for(const box of document.querySelectorAll('#chat-log .chat-draft.current')){const r=box.querySelector('[data-smart]')?.dataset.smart;if(r)out.push([box,c.id,r,box.querySelector('.chat-clamp')])}
 for(const box of document.querySelectorAll('#talk-view .talk-about .chat-draft.current')){const id=box.closest('[data-about]')?.dataset.about,r=box.querySelector('[data-smart]')?.dataset.smart;if(id&&r)out.push([box,id,r,box.querySelector('.chat-clamp')])}
 return out}
function draftSeenTick(){talkMore(document.querySelector('#talk-view .talk-about .chat-clamp'));if(document.hidden||!state.suggestions)return;const now=Date.now(),H=innerHeight;
 for(const [box,id,rev,text] of draftSeenBoxes()){const s=state.suggestions.find(x=>x.id===id),a=s?.status==='prepared'&&(s.next_actions||[]).find(x=>x.revision===rev);
  if(!a||a.kind==='doc_write'||!Array.isArray(a.to))continue;const body=String(a.body??a.message??''),key=id+'|'+rev+'|'+body;if(draftSeen.done.has(key))continue;
  const r=box.getBoundingClientRect(),el=text||box;if(!r.height||r.bottom<=0||r.top>=H||box.classList.contains('clamp')||box.closest('details:not([open])'))continue;
  const over=el.scrollHeight>el.clientHeight+2,scrolls=over&&/auto|scroll/.test(getComputedStyle(el).overflowY);if(over&&!scrolls)continue;
  let k=draftSeen.seen.get(key);if(!k)draftSeen.seen.set(key,k={top:false,end:false,ms:0,last:now,from:!scrolls,to:!scrolls});
  if(now-k.last<2000)k.ms+=now-k.last;k.last=now;if(r.top>=0)k.top=true;if(r.bottom<=H)k.end=true;
  if(scrolls){if(el.scrollTop<4)k.from=true;if(el.scrollTop+el.clientHeight>=el.scrollHeight-4)k.to=true}
  if(k.top&&k.end&&k.from&&k.to&&k.ms>=1500){draftSeen.done.add(key);micPost('draft_seen',{suggestion_id:id,revision:rev,to:a.to.map(String),subject:String(a.subject||''),body}).catch(()=>{})}}}
setInterval(draftSeenTick,500);
// A note for the voice, as a message it answers aloud; while it is talking, after that
function talkTell(v,text){if(!text)return;v.tell.push(text);talkTellNext(v)}
function talkTellNext(v){if(talk!==v||v.responding||v.speaking||!v.tell.length||v.dc?.readyState!=='open')return;const text=v.tell.shift();v.responding=true;
 v.dc.send(JSON.stringify({type:'conversation.item.create',item:{type:'message',role:'system',content:[{type:'input_text',text}]}}));
 v.dc.send(JSON.stringify({type:'response.create'}))}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-voice-undo]');if(!b)return;e.preventDefault();b.disabled=true;
 try{await micPost('talk_undo',{suggestion_id:b.dataset.sid,approval_id:b.dataset.voiceUndo});toast(t('Canceled. It won’t be sent.'))}catch(err){errCaught(err);toast(err.message,true)}
 await refresh();if(chatOpen())chatPoll()});
document.addEventListener('click',e=>{if(e.target.closest('[data-talk-undo]')&&talk){e.preventDefault();talkUndoSend(talk).then(r=>{if(r.error)toast(t('It was already on its way.'),true)});return}
 const b=e.target.closest('[data-talk],[data-talk-main],[data-talk-end],[data-talk-close],[data-talk-mute]');if(!b)return;e.preventDefault();
 if(b.hasAttribute('data-talk-main')){if(typeof drawerClose==='function')drawerClose();if(talk?.main&&!talkViewOn()&&b.id==='side-talk'){talkAfterDrawer(talkGoView);return}talkMain();return}  // live, from another page: back to Talk
 if(b.hasAttribute('data-talk')){if(talk)talkEnd();else talkStart();return}
 if(b.hasAttribute('data-talk-end')||b.hasAttribute('data-talk-close')){talkEnd();return}
 const v=talk;if(!v)return;
 if(b.hasAttribute('data-talk-mute'))talkMute(v,!v.muted)});
function talkMute(v,on){if(talk!==v||v.state!=='live')return;v.muted=on;v.stream?.getAudioTracks().forEach(x=>{x.enabled=!on});talkMedia(v);talkPaint()}
