// Talk live (talk_live.py): a spoken conversation with The Machine about the open to-do, with OpenAI's Realtime voice.
// The Machine starts the session (the OpenAI sign-in and the session's secret never come here) and hands on this page's
// WebRTC offer; the audio then goes directly between this page and OpenAI. The owner can talk over it (OpenAI stops
// and listens). The voice gets this page's tools: two that read, through the Machine, and `ask_chat`, which hands a
// request to the to-do's chat the way a typed message goes (decideOrWait), so the chat's own rules hold: it can change
// the draft or snooze, never send. Sending by voice: `ask_to_send` only works for the draft shown in this chat (on a
// phone or with the screen off the voice reads it out first) and gets the confirm question; `send_answer` lets the
// Machine judge the owner's next words itself. A clear yes approves that one draft, held a few seconds with Undo in the
// chat ("Approved by voice"). What both sides say goes into the chat. At most 10 minutes, with a warning a minute before.
// The session itself (talkStart and what runs while one is open) is todos-chat-talk-live.js, which loads when first
// needed (dashboard_parts.LAZY): what runs without a session open stays here.
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
 talkAfterDrawer(()=>{talkGoView();lazyRun('talk',()=>talkStart(true,first))})}
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
 $('#open-settings')?.setAttribute('aria-current','false');lazyRun('talk',()=>{talkViewPaint();talkPaint()});talkSide();scrollTo(0,0);talkFit();requestAnimationFrame(talkFit)}
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
addEventListener('hashchange',e=>{if(location.hash==='#talk'){if(talk?.main||talkLog.length)talkViewShow();else history.replaceState(null,'',location.pathname+location.search)}
 else if(/#talk$/.test(e.oldURL)&&!/^#chat=/.test(location.hash))talkLeave()});
// "Open the chat" stays in the page, also when the page's base is another path
$('#talk-view')?.addEventListener('click',e=>{const b=e.target.closest('[data-talk-event]');if(b){const title=b.textContent;if('meeting' in b.dataset)openMeeting(b.dataset.talkEvent,title);else openEvent(b.dataset.talkEvent,title);return}
 const a=e.target.closest('a[href^="#chat="]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey)return;e.preventDefault();chatGo(a.getAttribute('href').slice(6))});
if(location.hash==='#talk')history.replaceState(null,'',location.pathname+location.search);  // a reload: the conversation ended with the page
{const sec=document.getElementById('talk-view');if(sec)new MutationObserver(()=>{talkSide();if(!sec.hidden)return;if(location.hash==='#talk')history.replaceState(null,'',location.pathname+location.search);if(talk)talkPaint()}).observe(sec,{attributes:true,attributeFilter:['hidden']})}
function talkClose(v){clearInterval(v.tick);v.closed=true;talkWake(v);talkMedia(v);try{v.dc?.close()}catch{}try{v.pc?.close()}catch{}try{v.stream?.getTracks().forEach(x=>x.stop())}catch{}
 if(v.audio){v.audio.srcObject=null;v.audio.remove()}if(v.id&&!v.ended){v.ended=true;micPost('talk_end',{id:v.id}).catch(()=>{})}}
let talkLimitToast='';  // the limit's toast is about that session only: cleared when another starts or ends
function talkToastClear(){const t=$('#toast');if(talkLimitToast&&t?.textContent===talkLimitToast)t.classList.remove('show');talkLimitToast=''}
function talkEnd(){const v=talk;if(!v)return;talk=null;talkToastClear();talkClose(v);document.querySelectorAll('.chat-compose>.talk,.talk-foot>.talk').forEach(x=>x.remove());$('#talk-dock')?.remove();document.body.style.removeProperty('--talk-dock-h');talkSide();talkViewPaint()}
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
 if(b.hasAttribute('data-talk')){if(talk)talkEnd();else lazyRun('talk',()=>talkStart());return}
 if(b.hasAttribute('data-talk-end')||b.hasAttribute('data-talk-close')){talkEnd();return}
 const v=talk;if(!v)return;
 if(b.hasAttribute('data-talk-mute'))talkMute(v,!v.muted)});
