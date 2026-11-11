// Part of the Graph's part that loads when first needed (dashboard_parts.LAZY 'graph'): a project's follow-ups and
// Done when, a board's follow-ups line and the follow-up settings dialog, which only the Graph's pages open.
// A project's page: its board and stage, its next step, and the latest moves with the message each came from.
// Done when (project_success.py): the project's success condition, the proof that met it (the message, and the live page
// when the condition asks for one) or that it was marked done by hand, why a review's "done" isn't proven yet, and what
// stands in its way with its one to-do.
const PS_WHY={'unlinked':'The page doesn’t link to you yet','unloaded':'The page didn’t load','unsaid':'The link isn’t in their message',
 'no_url':'No link to the page yet','from_owner':'It needs a message from them','no_message':'No message shows it yet'};
const psBlock=x=>x.kind==='no_reply'?t('No reply in {} days',x.days)+(x.follow_ups?' · '+t('Follow-ups are on'):''):x.kind==='promise_theirs'?t('Waiting on {}: {}, due {}',x.who,x.what,shortDay(x.due)):t('Overdue for {}: {}, due {}',x.who,x.what,shortDay(x.due));
const successBox=s=>{if(!s)return '';const ev=s.evidence;
 const proof=s.done?(s.done_by==='evidence'&&ev?html`<p class="ps-proof ok">${t('Proven {}',shortDay(ev.at))}${ev.url?html` · <a href="${safeHref(ev.url)}" target="_blank" rel="noopener noreferrer" translate="no">${ev.url.replace(/^https:\/\/(www\.)?/,'').replace(/\/$/,'')}</a>`:''} <button type="button" class="link" data-quote-event="${ev.event_id}">Read</button></p>`:html`<p class="ps-proof">${t('Marked done by hand')}</p>`)
  :s.not_proven?html`<p class="ps-proof warn">${t('Not proven yet: {}',t(PS_WHY[s.not_proven]||s.not_proven))}</p>`:'';
 const block=!s.done&&s.blocker?html`<p class="ps-block">${psBlock(s.blocker)}${s.blocker.todo?html` · <a href="#card=${s.blocker.todo.id}" title="${s.blocker.todo.title}">${t('To-do')}</a>`:''}</p>`:'';
 return html`<div class="ps-box">${s.condition?html`<p class="ps-when">${t('Done when: {}',s.condition)}</p>`:''}${proof}${block}</div>`};
const stageBox=n=>{const b=n.board;if(!b)return '';const moves=orEmpty(html`${(b.moves||[]).map(m=>html`<li>${shortDay(m.at)} · ${m.source==='owner'?`Moved to ${m.stage} by hand`:`${m.stage}: ${(m.source==='follow_up'?fuMoveReason(m,n):m.reason||'')}`}${m.event_id?html` <button type="button" class="link" data-quote-event="${m.event_id}">Read</button>`:''}</li>`)}`);
 const seen=n.team_only?'':html`<label class="seen-pick">Who sees it<select data-project-seen="${n.id}"><option value=""${b.visibility?'':html` selected`}>Like its board (${b.board_visibility==='only_you'?'only you':b.board_visibility==='people'?'chosen teammates':'team'})</option><option value="only_you"${b.visibility==='only_you'?html` selected`:''}>Only you</option><option value="team"${b.visibility==='team'?html` selected`:''}>Your team</option></select></label>`;
 return html`<div class="graph-stage"><p><b>${b.stage||''}</b> <span class="muted">on ${b.board}</span>${['only_you','people'].includes(b.visibility||b.board_visibility)?html`${' '}${seenBy(b.visibility||b.board_visibility)}`:''}</p>${b.next?html`<p>Next: ${b.next}</p>`:''}${successBox(b.success)}${moves?html`<ol aria-label="Moves">${moves}</ol>`:''}${n.team_only?'':fuBox(n)}${seen}</div>`};
document.addEventListener('change',async e=>{const t=e.target.closest?.('[data-project-seen]');if(!t)return;t.disabled=true;
 try{await graphPost('project_visibility',{node_id:t.dataset.projectSeen,visibility:t.value||null});toast(t.value==='only_you'?'Only you see this project now.':t.value==='team'?'Your team sees this project now.':'It follows its board now.');await graphPeople('',true)}catch(err){errCaught(err);toast(err.message,true)}finally{t.disabled=false}});
// Automated follow-ups (follow_ups.py): their settings for a board or one project (a project's own wins over its board's),
// the board's "Follow-ups on" line, a project's "Next follow-up", and a board's grouped to-do with its fast review:
// one follow-up at a time or the whole list, Send, Edit or Skip each, keys to move, Send all checked.
const FU_CHANNELS={email:'Email',linkedin:'LinkedIn',whatsapp:'WhatsApp',slack:'Slack',telegram:'Telegram',intercom:'Intercom'};
const fuDay=v=>{if(!v)return '';const d=new Date(v),n=new Date();if(d<=n||localDay(d)===localDay(n))return t('today');return (d-n)/864e5<6?localeDate(d,DL,{weekday:'short'}):localeDate(d,DL,{day:'numeric',month:'short'})};
const fuNoReply=n=>n?t(['No reply after {} follow-up','No reply after {} follow-ups'],n):t('Follow-ups stopped');
// Paused (follow_ups.pause): a small chip where the follow-up status shows; nothing is drafted, sent or ended meanwhile
const fuChip=()=>html`<span class="fu-chip">${t('Paused')}</span>`;
const fuTile=f=>!f?'':f.state==='paused'?html`<p class="tile-fu quiet">${fuChip()}</p>`:f.reason==='bounced'?html`<p class="tile-fu quiet">${t('Email bounced')}</p>`:f.end?html`<p class="tile-fu quiet">${fuNoReply(f.end.n)}</p>`:f.state==='open'?html`<p class="tile-fu">${t('Follow-up ready')}</p>`:['due','waiting'].includes(f.state)&&f.next_at?html`<p class="tile-fu">${t('Next follow-up: {}',fuDay(f.next_at))}</p>`:'';
// On or off, the board's line says so and opens its settings; a stage with no-reply projects on a board with follow-ups off
// offers "Follow them up" (the owner's own boards only: a Team board isn't theirs to change)
// The board's follow-ups come after the board (api/graph/follow-ups): working them out held up the whole Graph tab
// (kept a minute: the quiet refresh that redraws the Graph tab on every poll uses the last answer; a change clears it)
// A refresh with the last answer still kept puts it on the boards before they draw (fuKeptOn, projectsPane): the board drew
// twice on every quiet refresh, once without its follow-ups and once with them (some 60 ms per poll on a big board)
const fuFresh=()=>fuKept&&Date.now()-fuKept.at<6e4?fuKept.f:null;
const fuOn=f=>{for(const b of graphBoards){b.follow_ups=f.boards?.[b.id]||{on:false,next_at:null};for(const p of b.projects||[]){if(f.projects?.[p.id])p.follow_up=f.projects[p.id];else delete p.follow_up}}};
const fuKeptOn=()=>{const f=fuFresh();if(f)fuOn(f)};
async function fuLoad(version){let f=fuFresh();if(!f){try{f=await request('api/graph/follow-ups')}catch{return}if(!f?.boards)return;fuKept={at:Date.now(),f}}if(version!==graphRequest)return;
 fuOn(f);if(lazyIn('graph'))boardRedraw()}
const fuBoardLine=b=>b.follow_ups?html` · <button type="button" class="link fu-state${b.follow_ups.on?'':html` off`}" data-fu-open="board:${b.id}">${!b.follow_ups.on?t('Follow-ups off'):b.follow_ups.pause?t('Follow-ups on'):b.follow_ups.next_at?t('Follow-ups on, next {}',fuDay(b.follow_ups.next_at)):t('Follow-ups on')}</button>${b.follow_ups.on&&b.follow_ups.pause?html`${' '}${fuChip()}`:''}`:'';
const fuNudge=(b,s)=>b.team||!b.follow_ups||b.follow_ups.on?'':html` · <button type="button" class="fu-nudge" data-fu-open="board:${b.id}" data-fu-for="${s.name}">${t('Follow them up')}</button>`;
const fuAct=a=>{const ch=FU_CHANNELS[a.channel]||a.channel;return a.why==='bounced'?t('Follow-up {} bounced',a.n):a.state==='sent'?(a.auto?t('Follow-up {} sent automatically ({})',a.n,ch):t('Follow-up {} sent ({})',a.n,ch)):a.state==='open'?t('Follow-up {} ready to review',a.n):a.state==='skipped'?t('Follow-up {} skipped',a.n):a.why==='owner'?t('Follow-ups stopped at follow-up {}',a.n):a.why==='replied'?t('They replied before follow-up {}',a.n):t('Follow-up {} not needed',a.n)};
const fuBox=n=>{const f=n.follow_up;if(!f)return '';const end=f.ends?.[0];
 const line=f.reason==='bounced'?t('Email bounced'):!f.on?t('Follow-ups off'):f.state==='open'?t('Follow-up ready'):f.pause?t('Follow-ups on'):f.next_at?t('Next follow-up: {}',fuDay(f.next_at)):end&&f.state==='stopped'?fuNoReply(end.n):t('Follow-ups on');
 const acts=orEmpty(html`${(f.activity||[]).slice(0,4).map(a=>html`<li>${shortDay(a.closed_at||a.created_at)} · ${fuAct(a)}${a.back?html` · <button type="button" class="link" data-fu-back="${a.back}">${t('Bring back')}</button>`:''}</li>`)}`);
 return html`<div class="graph-fu"><p><span>${line}</span>${f.on&&f.pause?html`${' '}${fuChip()}`:''} <button type="button" class="link" data-fu-open="${n.id}">${t('Follow-ups…')}</button></p>${acts?html`<ol aria-label="${t('Follow-ups')}">${acts}</ol>`:''}</div>`};
const fuMoveReason=(m,n)=>{const end=(n.follow_up?.ends||[]).find(e=>String(e.at).slice(0,16)===String(m.at).slice(0,16));return end?fuNoReply(end.n):m.reason||''};
let fu=null;
// From a stage's "Follow them up": on is ticked, and that stage too when it isn't on already (nothing is saved before Save)
async function fuOpen(ref,stage){const i=ref.indexOf(':'),scope=ref.slice(0,i),id=ref.slice(i+1);
 try{const r=await graphPost('follow_up_settings',{scope,id});fu={...r,s:{...r.settings,stages:{...(r.settings.stages||{})}},custom:Object.keys(r.settings.stages||{}).length>0,mode:r.scope==='project'?(r.own?(r.settings.on?'on':'off'):r.board?'board':'off'):''};
  const st=stage&&scope==='board'&&fu.stages?.find(x=>x.name===stage);if(stage&&scope==='board'){fu.s.on=true;if(st&&!(fu.s.stages[st.name]?.on??st.open)){fu.custom=true;fu.s.stages[st.name]={...fu.s.stages[st.name],on:true}}}
  fuDraw();const d=$('#fu-dialog');if(!d.open)d.showModal();d.querySelector('input:not(:disabled)')?.focus()}catch(e){errCaught(e);toast(e.message,true)}}
function fuDraw(){const f=$('#fu-form'),s=fu.s,proj=fu.scope==='project',on=proj?fu.mode==='on':s.on,stagesOn=fu.stages?.filter(x=>(s.stages[x.name]?.on??x.open)).length;
 const num=(name,v,min,max,label)=>html`<input type="number" inputmode="numeric" name="${name}" value="${v}" min="${min}" max="${max}" aria-label="${label}">`;
 const radio=(name,v,cur,label)=>html`<label class="fu-radio"><input type="radio" name="${name}" value="${v}"${cur===v?html` checked`:''}> ${label}</label>`;
 const top=proj?html`<fieldset class="fu-mode"><legend>${t('For this project')}</legend>${fu.board?radio('mode','board',fu.mode,fu.board.on?t('Like its board (on)'):t('Like its board (off)')):''}${radio('mode','on',fu.mode,t('On'))}${radio('mode','off',fu.mode,t('Off'))}</fieldset>`
  :html`<label class="fu-chk fu-main"><input type="checkbox" name="on"${s.on?html` checked`:''}> ${t('Follow up when there’s no reply')}</label>`;
 const pause=fuPauseRow();
 const stages=!proj&&fu.stages?.length?html`<div class="fu-line"><span>${t('Stages')}</span><span class="muted">${fu.custom?t(['{} stage on','{} stages on'],stagesOn):t('All open stages')}</span>${fu.custom?'':html`<button type="button" class="link" data-fu-custom>${t('Customize')}</button>`}</div>${fu.custom?html`<ul class="fu-stages">${fu.stages.map((x,i)=>html`<li><label class="fu-chk"><input type="checkbox" data-fu-stage="${i}"${s.stages[x.name]?.on??x.open?html` checked`:''}> <span title="${x.name}">${x.name}</span></label><input type="number" inputmode="numeric" data-fu-sdays="${i}" min="1" max="60" value="${s.stages[x.name]?.days??''}" placeholder="${s.days}" aria-label="${t('Days to wait in {}',x.name)}"></li>`)}</ul><p class="fu-note">${t('Days to wait per stage; empty uses the shortest wait.')}</p>`:''}`:'';
 const allowed=c=>!s.channels||s.channels.includes(c);
 const channels=fu.channels.length?html`<fieldset class="fu-ch"><legend>${t('Channels')}</legend>${fu.channels.map(c=>html`<label class="fu-chk"><input type="checkbox" name="ch" value="${c}"${allowed(c)?html` checked`:''}> ${FU_CHANNELS[c]}</label>`)}<p class="fu-note">${t('Same channel as the last message.')}</p>${fu.channels.length>1?html`<label class="fu-chk"><input type="checkbox" name="switch"${s.switch?html` checked`:''}> ${t('Switch channel if there’s no reply')}</label>`:''}</fieldset>`
  :html`<p class="fu-note warn">${t('Connect a channel that can send first.')}</p>`;
 const stall=fu.stalled?html`<label class="fu-chk"><input type="checkbox" name="stall"${s.stall!==false?html` checked`:''}> ${t('Move to Stalled or declined after the last one')}</label>`:'';
 const send=html`<fieldset class="fu-send"><legend>${t('Sending')}</legend>${radio('auto','ask',s.auto&&!fu.careful?'auto':'ask',t('Ask me before sending'))}<label class="fu-radio"><input type="radio" name="auto" value="auto"${s.auto&&!fu.careful?html` checked`:''}${fu.careful?html` disabled`:''}> ${t('Send without asking')}</label><p class="fu-note">${fu.careful?t('Careful mode is on, so it always asks.'):s.auto?t('Anything unusual still waits for you.'):t('Drafts wait in your to-dos.')}</p></fieldset>`;
 setHTML(f,html`<div class="snooze-heading"><h2 id="fu-dialog-title">${t('Follow-ups')}</h2><button type="button" data-fu-close aria-label="${t('Close')}">×</button></div><p class="fu-for" title="${fu.name}">${fu.name}</p>${top}${pause}<fieldset class="fu-body"${on?'':html` disabled`}><p class="fu-row">${htmlT('Wait {} to {} days without a reply',num('days',s.days,1,60,t('Shortest wait in days')),num('max_days',s.max_days,1,60,t('Longest wait in days')))}</p><div><label class="fu-chk"><input type="checkbox" name="workdays"${s.workdays??fu.workdays_default??true?html` checked`:''}> ${t('Only on work days')}</label><p class="fu-note"><a class="link" href="#settings/hours" data-fu-hours>${t('Work days from your work hours')}</a></p></div><p class="fu-row">${htmlT('Follow up at least {} and at most {} times',num('min',s.min,0,5,t('At least')),num('max',s.max,1,5,t('At most')))}</p><p class="fu-note">${t('Past the minimum, it only follows up when that still makes sense.')}</p>${stages}${channels}${stall}${send}</fieldset><p class="ed-note warn" data-fu-error role="alert" hidden></p><div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-fu-close>${t('Cancel')}</button><button class="primary">${t('Save')}</button></div>`)}
// Pause / Resume (follow_up_pause): only where follow-ups are on as saved. Applies at once, apart from Save; a project held
// by its board's pause says so and resumes on the board.
function fuPauseRow(){const p=fu.pause,on=!!fu.settings?.on;if(!on&&!p)return '';
 const until=p?.until?localeDate(new Date(p.until),DL,{weekday:'short',day:'numeric',month:'short'}):'';
 if(p)return html`<div class="fu-pause" role="group" aria-label="${t('Pause')}">${fuChip()}<span class="fu-pause-when">${fu.scope==='project'&&p.scope==='board'?t('With its board'):until?t('Until {}',until):t('Until you resume')}</span>${fu.scope==='project'&&p.scope==='board'?'':html`<button type="button" data-fu-resume>${t('Resume')}</button>`}</div>`;
 return html`<div class="fu-pause" role="group" aria-label="${t('Pause')}"><button type="button" data-fu-pause>${t('Pause')}</button><label class="fu-until">${t('Resume on')} <input type="date" name="fu-until" min="${localDay(new Date(Date.now()+864e5))}"></label></div><p class="fu-note">${t('No new follow-ups or sends while paused. Open to-dos stay. No date: until you resume.')}</p>`}
async function fuPauseSet(paused){if(!fu)return;fuRead();const f=$('#fu-form'),err=f.querySelector('[data-fu-error]'),day=f.elements['fu-until']?.value;
 const b=f.querySelector('[data-fu-pause],[data-fu-resume]');if(b)b.disabled=true;
 try{const r=await graphPost('follow_up_pause',{scope:fu.scope,id:fu.id,paused,...(paused&&day?{until:new Date(day+'T00:00').toISOString()}:{})});if(!fu)return;fu.pause=r.pause;fuDraw();
  toast(paused?t('Follow-ups paused.'):t('Follow-ups resumed.'));if(!$('#people').hidden)graphPeople(graphNode,true).catch(()=>{});refresh().catch(()=>{})}
 catch(x){errCaught(x);if(b)b.disabled=false;if(err){err.textContent=x.message;err.hidden=false}}}
function fuRead(){const f=$('#fu-form'),s=fu.s,n=name=>{const v=f.elements[name]?.value;return v===''||v==null?undefined:+v};
 if(fu.scope==='project'){const m=f.querySelector('[name=mode]:checked');if(m)fu.mode=m.value}else s.on=!!f.elements.on?.checked;
 for(const k of ['days','max_days','min','max']){const v=n(k);if(v!==undefined)s[k]=v}
 const ch=[...f.querySelectorAll('[name=ch]')];if(ch.length)s.channels=ch.every(x=>x.checked)?null:ch.filter(x=>x.checked).map(x=>x.value);
 if(f.elements.switch)s.switch=f.elements.switch.checked;if(f.elements.stall)s.stall=f.elements.stall.checked;if(f.elements.workdays)s.workdays=f.elements.workdays.checked;
 const a=f.querySelector('[name=auto]:checked');if(a)s.auto=a.value==='auto';
 for(const x of f.querySelectorAll('[data-fu-stage]')){const st=fu.stages[+x.dataset.fuStage],d=f.querySelector(`[data-fu-sdays="${x.dataset.fuStage}"]`)?.value;s.stages[st.name]={on:x.checked,...(d?{days:+d}:{})}}}
$('#fu-form').addEventListener('change',e=>{if(!fu)return;fuRead();if(e.target.name==='mode'||e.target.name==='on'||e.target.name==='auto'||e.target.dataset.fuStage!=null)fuDraw()});
// Work days from your work hours: Settings at Notifications (#settings/hours), scrolled to the Work hours section
function fuHours(){$('#fu-dialog').close();if(location.hash==='#settings/hours')showSettings('hours');else location.hash='#settings/hours';
 requestAnimationFrame(()=>requestAnimationFrame(()=>{const h=$('#hours');(h?.previousElementSibling?.classList.contains('section-head')?h.previousElementSibling:h)?.scrollIntoView({block:'start'})}))}
$('#fu-form').addEventListener('click',e=>{if(!fu)return;if(e.target.closest('[data-fu-hours]')){e.preventDefault();fuHours();return}if(e.target.closest('[data-fu-close]')){$('#fu-dialog').close();return}if(e.target.closest('[data-fu-pause]')){fuPauseSet(true);return}if(e.target.closest('[data-fu-resume]')){fuPauseSet(false);return}if(e.target.closest('[data-fu-custom]')){fuRead();fu.custom=true;fuDraw();$('#fu-form [data-fu-stage]')?.focus()}});
$('#fu-form').addEventListener('submit',async e=>{e.preventDefault();if(!fu)return;fuRead();const s=fu.s,err=$('#fu-form [data-fu-error]'),btn=$('#fu-form button.primary');
 const settings=fu.scope==='project'&&fu.mode==='board'?{inherit:true}:{...s,on:fu.scope==='project'?fu.mode==='on':s.on,stages:fu.custom?s.stages:{}};
 btn.disabled=true;try{await graphPost('follow_up_save',{scope:fu.scope,id:fu.id,settings});$('#fu-dialog').close();toast(t('Follow-ups saved.'));if(!$('#people').hidden)await graphPeople(graphNode,true);refresh().catch(()=>{})}
 catch(x){errCaught(x);err.textContent=x.message;err.hidden=false}finally{btn.disabled=false}});
$('#fu-dialog').addEventListener('close',()=>{fu=null});
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-fu-open]');if(!b)return;e.preventDefault();e.stopPropagation();b.closest('details')?.removeAttribute('open');fuOpen(b.dataset.fuOpen,b.dataset.fuFor)},true);
