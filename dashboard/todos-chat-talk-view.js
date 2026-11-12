// A lazy part (dashboard_parts.LAZY 'talk'): what draws a Talk session (its bar and Talk's view). A session only runs
// once 'talk' is in (todos-chat-talk-live.js), so todos-chat-talk.js calls these only while one is open.
function talkDraftHtml(s){const a=s.status==='prepared'?(s.next_actions||[]).find(a=>a.revision&&(['email','linkedin','slack','x','whatsapp','telegram','signal','intercom','doc_reply'].includes(a.kind)&&a.body||a.kind==='doc_write')):null;if(!a)return '';
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
// A record the voice opened (open_record): a small card in the transcript, opening its own page or the meeting
const TALK_KIND={person:'Person',organization:'Organization',project:'Project',meeting:'Meeting',message:'Message',promise:'Promise'};
function talkRecordHtml(c){const title=(c.title||''),go=c.node?html`<a href="${graphHash(c.node)}">${title}</a>`:c.promise?html`<a href="${promiseHref({id:c.promise})}">${title}</a>`
  :c.event?html`<button type="button" class="talk-record-open" data-talk-event="${String(c.event)}"${c.kind==='meeting'?html` data-meeting`:''}>${title}</button>`:title;
 return html`<div class="talk-record"><span class="talk-record-kind">${t(TALK_KIND[c.kind]||'Message')}</span><strong translate="no">${go}</strong>${c.line?html`<small translate="no">${c.line}</small>`:''}</div>`}
function talkMute(v,on){if(talk!==v||v.state!=='live')return;v.muted=on;v.stream?.getAudioTracks().forEach(x=>{x.enabled=!on});talkMedia(v);talkPaint()}
