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
let fuKept=null;
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
// The board's follow-ups as one to-do: "8 follow-ups ready for <board>" once one is written, else
// "Follow-ups for <board>", in For you either way. Each is in it from the start, also alone: never a to-do of its own in any list, so a board
// with follow-ups on is one to-do to review, not one per email. While drafts are written it says "Writing 3 follow-ups…".
// One that got stuck (needs the owner's help) stays a to-do of its own. A project's own follow-up (not grouped) is a
// normal to-do. Follow-ups on their way in a batch (spaced 30-45 s per mailbox) show as one progress to-do per board
// instead (fuSendingCard).
// Queued or on its way: out of the ready to-do at once. A follow-up's draft can sit in a menu, so its own state counts too.
const fuBusy=s=>sendBusy(s.action_status)||taskActions(s).some(a=>DRAFT_KINDS.includes(a.kind)&&sendBusy(a.state));
function fuSplit(ready,needs){fuGroups.clear();const groups={},member=s=>typeof s!=='string'&&!(s instanceof SafeHTML)&&s.follow_up?.group&&s.follow_up.state==='open'&&!fuBusy(s)&&!needsDecision(s);
 const batch=new Set((state.follow_up_progress||[]).filter(p=>p.going).map(p=>p.group||'own')),inBatch=s=>s.follow_up&&fuBusy(s)&&batch.has(s.follow_up.group||'own');
 for(const s of [...ready,...needs])if(member(s))(groups[s.follow_up.group]??=[]).push(s);
 const grouped=new Set(Object.values(groups).flat().map(s=>s.id)),cards=Object.entries(groups).map(([g,l])=>[l.some(s=>s.status==='prepared'),fuGroupCard(g,l)]);
 const out=list=>list.filter(s=>typeof s==='string'||s instanceof SafeHTML||!grouped.has(s.id));
 return {ready:[...cards.filter(([r])=>r).map(([,c])=>c),...cards.filter(([r])=>!r).map(([,c])=>c),...out(ready).filter(s=>!inBatch(s))],needs:out(needs)}}
// The sidebar lists a board's group as one row that opens the review
const fuGroups=new Map();
function fuSide(items){return items.map(x=>fuGroups.has(x)?fuGroups.get(x):x)}
function fuGroupCard(g,all){const list=all.filter(s=>s.status==='prepared'),writing=all.length-list.length,board=all[0].follow_up.board||'',names=all.map(s=>s.follow_up.name||s.follow_up.project),first=names.slice(0,3);
 const title=list.length?t(['{} follow-up ready for {}','{} follow-ups ready for {}'],list.length,board):t('Follow-ups for {}',board);
 const card=html`<h3>${list.length?html`<button type="button" class="title-link fu-title" data-fu-review="${g}"><span translate="no">${title}</span></button>`:html`<span translate="no">${title}</span>`}</h3><div class="meta"><div class="card-badges"><span class="meta-side">${time(all.map(s=>s.created_at).sort().pop(),true)}</span></div></div>${writing?html`<p class="fu-progress" role="status">${t(['Writing {} follow-up…','Writing {} follow-ups…'],writing)}</p>`:''}<p class="fu-names">${names.length>3?t('{}, {}, {} and {} more',...first,names.length-3):namesLine(first)}</p>${list.length?html`<div class="actions"><button class="primary" data-fu-review="${g}">${t('Review')}</button></div>`:''}</article>`;
 const body=html`<article class="card todo ${list.length?'t-mint':'t-lavender'} fu-group" id="fu-${g.replace(':','-')}" data-status="${list.length?'prepared':'accepted'}">${card}`;  // see fuSide
 fuGroups.set(body,{id:'fu-'+g,fuGroup:g,title,created_at:all[0].created_at,scope:all[0].scope,writing:!list.length});return body}
// "Sending 3 of 8…" while a batch goes out, then "Sent 8" (or "Sent 7 of 8": the one that failed is back as a to-do that asks).
// One held right before it went (a new message in the thread since the draft, or the thread couldn't be checked): "Sent 7 · 1 held (new message)".
// Stop sending: "Stopped. 1 sent, 11 kept as drafts." (the one going out when it was pressed still goes, and counts once sent)
const fuSendingLine=p=>p.stopped?(p.stopped===1?t('Stopped. {} sent, 1 kept as a draft.',p.sent):t('Stopped. {} sent, {} kept as drafts.',p.sent,p.stopped)):p.going?t('Sending {} of {}…',Math.min(p.done+1,p.total),p.total):p.held?(p.held_new===p.held?t('Sent {} · {} held (new message)',p.sent,p.held):t('Sent {} · {} held',p.sent,p.held)):p.sent===p.total?t('Sent {}',p.total):t('Sent {} of {}',p.sent,p.total);
const fuSendingCard=p=>{const going=p.going&&!p.stopped;return html`<article class="card todo t-mint fu-sending" id="fu-sending-${(p.group||'own').replace(':','-')}" data-status="prepared"><h3><span translate="no">${p.board?t('Follow-ups for {}',p.board):t('Follow-ups')}</span>${!p.going&&p.batch?html`<button type="button" class="fu-x" data-fu-dismiss="${p.batch}" aria-label="${t('Dismiss')}" title="${t('Dismiss')}">×</button>`:''}</h3><p class="fu-progress${going||p.held?'':html` ok`}" role="status">${fuSendingLine(p)}${p.paused?html`${' '}${fuChip()}`:''}</p>${going?html`<p class="fu-spaced">${p.done_at?t('Spaced out so they don’t look automated · done around {}',fmtHM(p.done_at)):t('Spaced out so they don’t look automated')}</p>`:''}${going?html`<div class="fu-bar" aria-hidden="true"><i style="width:${Math.round(100*p.done/p.total)}%"></i></div>`:''}${going&&p.batch?html`<div class="actions"><button type="button" data-fu-stop="${p.batch}">${t('Stop sending')}</button></div>`:''}</article>`};
const fuSendingCards=()=>scopeFilter==='personal'?'':html`${fuShownProgress().map(fuSendingCard)}`;
// A finished batch's card ("Sent 13") can be dismissed with its ×; it stays hidden after a reload (this browser), and
// still goes by itself a few minutes after the last send. Never while sending.
const FU_GONE='fu-dismissed-batches';
const fuGone=()=>{try{return JSON.parse(localStorage.getItem(FU_GONE)||'[]')}catch{return []}};
const fuShownProgress=()=>{const gone=new Set(fuGone());return (state.follow_up_progress||[]).filter(p=>p.going||!p.batch||!gone.has(p.batch))};
// Bring back: a skipped follow-up is ready to review again, with its draft (follow_ups.bring_back)
document.addEventListener('click',async e=>{const b=e.target.closest?.('[data-fu-back]');if(!b)return;e.preventDefault();e.stopPropagation();b.disabled=true;
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'follow_up_bring_back',args:{id:b.dataset.fuBack}})});
  toast(t('Back to review.'));await refresh();if(graphNode&&!$('#people').hidden)await graphPeople(graphNode,true)}
 catch(x){errCaught(x);toast(x.message,true);b.disabled=false}},true);
// Stop sending: the ones not gone yet are canceled on the Machine and their drafts are back in the review (follow_ups.stop)
document.addEventListener('click',async e=>{const b=e.target.closest?.('[data-fu-stop]');if(!b)return;e.preventDefault();b.disabled=true;
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'follow_up_stop',args:{batch:b.dataset.fuStop}})});await refresh()}
 catch(x){errCaught(x);toast(x.message);b.disabled=false}});
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-fu-dismiss]');if(!b)return;e.preventDefault();
 try{localStorage.setItem(FU_GONE,JSON.stringify([...fuGone().filter(x=>x!==b.dataset.fuDismiss),b.dataset.fuDismiss].slice(-50)))}catch{}
 b.closest('.fu-sending')?.remove();render()});
let fr=null;
const frDraft=s=>taskActions(s).find(a=>DRAFT_KINDS.includes(a.kind)&&draftText(a));
// A draft the review's Change is rewriting stays in the list while its to-do is back at work, and so does one that
// couldn't be changed (its "try again" is here)
const frList=()=>state.suggestions.filter(s=>s.follow_up?.group===fr.g&&s.follow_up.state==='open'&&!fr.gone.has(s.id)&&!fuBusy(s)
 &&(s.status==='prepared'||(fr.changing.has(s.id)||fr.failed.has(s.id))&&['instructions','accepted'].includes(s.status)))
 .sort((a,b)=>fr.skipped.has(a.id)-fr.skipped.has(b.id));  // skipped ones wait at the bottom until the review closes
// Every draft shows in full and the list is the only thing that scrolls; moving (j/k, a click) changes the current one
// in place and scrolls it into view smoothly, a poll redraws only the drafts that changed and keeps where the list is
const frPhase=s=>fr.skipped.has(s.id)?'skip':fr.changing.has(s.id)?'run':fr.failed.has(s.id)?'fail':fr.undo.has(s.id)?'done':'';
const frItemSig=s=>s.id+':'+(frDraft(s)?.revision||'')+':'+s.status+':'+frPhase(s)+':'+(s.action_status?.error||'')+':'+(s.follow_up?.advice||'');
const frSig=list=>list.map(s=>s.id).join();
const frReady=s=>s.status==='prepared'&&!fr.changing.has(s.id)&&!fr.skipped.has(s.id);
// Held right before it went because the thread got a new message (follow_ups.HELD): left out of Send all checked until the
// owner ticks it again, and its Send is a plain one. "Couldn’t check the thread" stays checked: trying again is the point.
const frStale=s=>s.action_status?.status==='blocked'&&s.action_status.error==='Not sent: new message in the thread.';
// The Machine would stop here (follow_ups.advise): the draft is there, unchecked, and the owner decides
const frAdvised=s=>!!s.follow_up?.advice;
// The project's name without the board's in front (follow_ups.short_name): the title names the board already
const frName=f=>f.name||f.project;
function frOpen(g){fr={g,at:0,cur:null,checked:null,editing:null,gone:new Set(),sent:0,busy:false,box:null,changing:new Map(),failed:new Map(),undo:new Map(),shown:new Map(),skipped:new Map()};
 const list=frList();fr.checked=new Set(list.filter(s=>!frStale(s)&&!frAdvised(s)).map(s=>s.id));fr.seen=new Set(list.map(s=>s.id));
 const d=$('#fu-review');d.replaceChildren();frDraw();const ol=d.querySelector('.fr-list');if(!ol)return;if(!d.open)d.showModal();ol.scrollTop=0;d.querySelector('.fr-item.on')?.focus({preventScroll:true})}
// A draft's text exactly as it goes out: every line and every blank line (the one between "Regards," and the name
// too), only blank lines at its very start and end left out
const frBody=text=>String(text).replace(/^(?:[ \t]*\n)+|\s+$/g,'');
function frState(s){const ph=frPhase(s);
 if(ph==='skip')return html`<p class="fr-state skip">${t('Skipped')}<button type="button" class="link" data-fr-unskip="${s.id}">${t('Undo')}</button></p>`;
 if(ph==='run')return html`<p class="fr-state run" role="status"><i class="fr-spin" aria-hidden="true"></i>${t('Rewriting…')}</p>`;
 if(ph==='fail')return html`<p class="fr-state fail" role="status">${t('Couldn’t change this one, try again')}<button type="button" class="link" data-fr-retry="${s.id}">${t('Try again')}</button></p>`;
 if(ph==='done')return html`<p class="fr-state done"><button type="button" class="link" data-fr-undo="${s.id}">${t('Undo change')}</button></p>`;
 return ''}
function frItem(s,i){const a=frDraft(s),f=s.follow_up,on=i===fr.at,edit=fr.editing===s.id;fr.shown.set(s.id,a?.revision);const to=a?[movedLine(a)||(a.to_name||(a.to||[]).join(', ')?t('To {}',a.to_name||(a.to||[]).join(', ')):''),a.from_options?.length>1&&a.from?t('From {}',a.from):''].filter(Boolean).join(' · '):'',ready=frReady(s);
 const skip=fr.skipped.has(s.id);
 return html`<li class="fr-item${on?html` on`:''}${fr.changing.has(s.id)?html` rewriting`:''}${skip?html` skipped`:''}" data-fr="${s.id}" data-fr-at="${i}" tabindex="${on?0:-1}" aria-current="${on}" aria-busy="${fr.changing.has(s.id)}"><div class="fr-head"><input type="checkbox" data-fr-check="${s.id}"${fr.checked.has(s.id)?html` checked`:''}${skip?html` disabled`:''} aria-label="${t('Include {}',frName(f))}"><b title="${f.project}">${frName(f)}</b><span class="fr-meta">${t('Follow-up {} of {}',f.n,f.max)} · ${FU_CHANNELS[f.channel]||f.channel}</span></div><div class="fr-sub"><p class="fr-to" title="${to}">${to}</p><div class="fr-actions">${edit?html`<button type="button" class="primary" data-fr-save="${s.id}">${t('Save')}</button><button type="button" class="ghost" data-fr-cancel>${t('Cancel')}</button>`:html`<button type="button" class="${frStale(s)||frAdvised(s)?'fr-plain':'primary'}" data-fr-send="${s.id}"${a&&ready&&!fr.box?'':html` disabled`}>${t('Send')}</button><button type="button" class="ghost" data-fr-edit="${s.id}"${a&&ready?'':html` disabled`}>${t('Edit')}</button><button type="button" class="ghost" data-fr-skip="${s.id}"${fr.changing.has(s.id)||skip?html` disabled`:''}>${t('Skip')}</button>`}</div></div>${s.action_status?.status==='blocked'&&s.action_status.error&&!fr.changing.has(s.id)?html`<p class="fr-held" role="status">${heldLine(s.action_status.error)}</p>`:''}${frState(s)}${frAdvised(s)&&!skip?html`<p class="fr-advice"><span>${t('The Machine would stop here: {}',f.advice)}</span><button type="button" class="link" data-fr-end="${s.id}"${fr.box?html` disabled`:''}>${t('Stop follow-ups here')}</button></p>`:''}${a?(edit?html`<textarea class="fr-edit" spellcheck="true" autocapitalize="sentences" data-fr-text="${s.id}" rows="6" aria-label="${t('Follow-up text')}">${plainDraft(draftText(a))}</textarea>`:html`<div class="fr-body">${frBody(plainDraft(draftText(a)))}</div>`):html`<p class="muted fr-none">${t('No draft yet.')}</p>`}</li>`}
// Change: what should change, for all checked drafts or only the current one (the c key opens it)
function frBox(list){if(!fr.box)return '';const n=list.filter(s=>fr.checked.has(s.id)&&frReady(s)).length,one=list.find(s=>s.id===fr.box.one)||list[fr.at];
 if(!n&&fr.box.scope==='all')fr.box.scope='one';
 return html`<div class="fr-change" role="group" aria-labelledby="fr-change-q"><label class="fr-change-q" id="fr-change-q" for="fr-change-text">${t('What should change?')}</label><div class="mic-wrap"><textarea id="fr-change-text" spellcheck="true" autocapitalize="sentences" rows="2" maxlength="2000" enterkeyhint="send">${fr.box.text}</textarea>${micBtn()}</div><div class="fr-scope"><label class="fu-radio"><input type="radio" name="fr-scope" value="all"${fr.box.scope==='all'?html` checked`:''}${n?'':html` disabled`}><span>${t('All checked ({})',n)}</span></label><label class="fu-radio"><input type="radio" name="fr-scope" value="one"${fr.box.scope==='one'?html` checked`:''}><span class="fr-one" translate="no">${t('Only this one: {}',one?frName(one.follow_up):'')}</span></label></div><div class="fr-change-actions"><button type="button" class="ghost" data-fr-box-cancel>${t('Cancel')}</button><button type="button" class="primary" data-fr-box-go>${t('Rewrite')}</button></div></div>`}// The control that has focus, as a selector that finds it again after a redraw
const frFocusSel=d=>{const a=document.activeElement;if(!a||!d.contains(a))return null;if(a.id==='fr-change-text')return '#fr-change-text';if(a.name==='fr-scope')return `[name=fr-scope][value=${a.value}]`;
 for(const k of ['frCheck','frSend','frEdit','frSkip','frUnskip','frUndo','frRetry'])if(a.dataset?.[k])return `[data-${k.replace(/[A-Z]/g,c=>'-'+c.toLowerCase())}="${CSS.escape(a.dataset[k])}"]`;
 if(a.matches('.fr-item'))return `.fr-item[data-fr="${CSS.escape(a.dataset.fr)}"]`;return null};
function frDraw(reveal){const d=$('#fu-review'),list=frList();if(!list.length){if(d.open)d.close();if(fr.sent)toast(t(['{} follow-up on its way','{} follow-ups on their way'],fr.sent));return}
 const was=list.findIndex(s=>s.id===fr.cur);if(was>=0)fr.at=was;fr.at=Math.max(0,Math.min(fr.at,list.length-1));fr.cur=list[fr.at].id;fr.sig=frSig(list);fr.item=new Map(list.map(s=>[s.id,frItemSig(s)]));
 const n=list.filter(s=>fr.checked.has(s.id)&&frReady(s)).length,board=list[0].follow_up.board||'',keep=d.querySelector('.fr-list')?.scrollTop,back=frFocusSel(d);
 setHTML(d,html`<div class="snooze-heading"><h2 id="fu-review-title" title="${board}">${t(['{} follow-up for {}','{} follow-ups for {}'],list.length,board)}</h2><button type="button" data-fr-close aria-label="${t('Close')}">×</button></div><p class="fu-keys">${t('Keys: j and k move, Enter sends, e edits, s skips, c changes.')}</p><ol class="fr-list">${list.map(frItem)}</ol>${frBox(list)}<p class="ed-note warn" data-fr-error role="alert" hidden></p><div class="ed-actions fr-main"${fr.box?html` hidden`:''}><button type="button" class="ghost" data-fr-change aria-expanded="${!!fr.box}">${t('Ask for changes…')}</button><span class="grow"></span><button type="button" class="ghost" data-fr-close>${t('Close')}</button><button type="button" class="primary" data-fr-all${n&&!fr.changing.size?'':html` disabled`}>${t('Send all checked ({})',n)}</button></div>`);
 if(keep)d.querySelector('.fr-list').scrollTop=keep;const on=d.querySelector('.fr-item.on');
 if(fr.editing)d.querySelector('.fr-edit')?.focus({preventScroll:true});else (back&&d.querySelector(back)||on)?.focus({preventScroll:true});
 if(reveal)frReveal(on)}
// One draft drawn again where it is (a rewrite came back, Undo, a failure): the rest of the list, its scroll and focus stay
function frPatch(s){const d=$('#fu-review'),el=d.querySelector(`.fr-item[data-fr="${CSS.escape(s.id)}"]`);if(!el)return false;
 const back=el.contains(document.activeElement)?frFocusSel(d):null,i=+el.dataset.frAt,box=document.createElement('template');setHTML(box,frItem(s,i));
 // the draft at the top of the view stays where it is, also when one above it got shorter or longer
 const ol=el.closest('.fr-list'),top=ol.getBoundingClientRect().top,pin=[...ol.children].find(x=>x.getBoundingClientRect().bottom>top),pinId=pin?.dataset.fr,pinAt=pin?.getBoundingClientRect().top;
 el.replaceWith(box.content.firstElementChild);
 if(pinId){const n=ol.querySelector(`.fr-item[data-fr="${CSS.escape(pinId)}"]`),dy=n?n.getBoundingClientRect().top-pinAt:0;if(Math.abs(dy)>=1)ol.scrollTop+=dy}fr.item.set(s.id,frItemSig(s));if(back)(d.querySelector(back)||d.querySelector(`.fr-item[data-fr="${CSS.escape(s.id)}"]`))?.focus({preventScroll:true});return true}
// Bring the current draft into view: nothing when it's already in view; a tall one lines up its top (for a click, only
// when it isn't in view at all, so a click never pulls the text away from under the pointer)
function frReveal(el,click){const ol=el?.closest('.fr-list');if(!ol)return;const v=ol.getBoundingClientRect(),r=el.getBoundingClientRect(),pad=8,fits=r.height<=v.height-2*pad;let dy=0;
 if(fits){if(r.top<v.top+pad)dy=r.top-v.top-pad;else if(r.bottom>v.bottom-pad)dy=r.bottom-v.bottom+pad}
 else if(!click||r.bottom<v.top||r.top>v.bottom)dy=r.top-v.top-pad;
 if(Math.abs(dy)>1)ol.scrollBy({top:dy,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})}
function frMove(i,click){const d=$('#fu-review'),items=[...d.querySelectorAll('.fr-item')];if(!items.length)return;i=Math.max(0,Math.min(i,items.length-1));
 fr.at=i;fr.cur=items[i].dataset.fr;items.forEach((el,j)=>{const on=j===i;el.classList.toggle('on',on);el.tabIndex=on?0:-1;el.setAttribute('aria-current',on)});
 if(fr.box){fr.box.one=fr.cur;const s=frList().find(x=>x.id===fr.cur),one=d.querySelector('.fr-one');if(s&&one)one.textContent=t('Only this one: {}',frName(s.follow_up))}
 if(!items[i].contains(document.activeElement))items[i].focus({preventScroll:true});frReveal(items[i],click)}
// One row of buttons at a time: while the Change box is open its Cancel and Rewrite are the only ones (the Send row is
// hidden and no draft sends), and while a rewrite runs nothing is sent all at once
function frModes(){const d=$('#fu-review'),main=d.querySelector('.fr-main');if(main)main.hidden=!!fr.box;
 for(const b of d.querySelectorAll('[data-fr-send]')){const s=state.suggestions.find(x=>x.id===b.dataset.frSend);b.disabled=!!fr.box||!s||!frDraft(s)||!frReady(s)}
 for(const b of d.querySelectorAll('[data-fr-end]'))b.disabled=!!fr.box}
function frCount(){const list=frList(),n=list.filter(s=>fr.checked.has(s.id)&&frReady(s)).length,all=$('#fu-review [data-fr-all]');if(all){all.textContent=t('Send all checked ({})',n);all.disabled=!n||!!fr.changing.size}frModes();
 const scope=$('#fu-review [name=fr-scope][value=all]');if(scope){scope.disabled=!n;scope.nextElementSibling.textContent=t('All checked ({})',n);if(!n&&scope.checked){scope.checked=false;fr.box.scope='one';$('#fu-review [name=fr-scope][value=one]').checked=true}}}
// Where each rewrite stands, from the to-do itself: a new draft revision is done (the old text kept for Undo change); its
// run stuck, or a reply that left the draft as it was, couldn't change it. A to-do that closed meanwhile leaves the list.
function frTrack(){for(const [id,c] of fr.changing){const s=state.suggestions.find(x=>x.id===id);
  if(!s||s.follow_up?.state!=='open'||['completed','rejected','snoozed'].includes(s.status)){fr.changing.delete(id);fr.gone.add(id);continue}
  if(s.status!=='prepared')c.seen=true;const a=frDraft(s);
  if(s.status==='prepared'&&a&&a.revision!==c.from){fr.changing.delete(id);fr.undo.set(id,{body:c.body,subject:c.subject})}
  else if(c.seen&&(s.status==='prepared'||s.preparation_status==='blocked')){fr.changing.delete(id);fr.failed.set(id,c.text)}}}
// A poll: new drafts join (checked), sent or changed ones update in place; the draft being edited is left as it is
function frRefresh(){const d=$('#fu-review');if(!fr||!d.open||fr.busy)return;frTrack();const list=frList();
 for(const s of list)if(!fr.seen.has(s.id)){fr.seen.add(s.id);if(!frStale(s)&&!frAdvised(s))fr.checked.add(s.id)}
 if(frSig(list)===fr.sig){let n=0;for(const s of list)if(s.id!==fr.editing&&fr.item.get(s.id)!==frItemSig(s)&&frPatch(s))n++;if(n)frCount();return}
 if(!fr.editing)frDraw()}
const frSay=x=>{const p=$('#fu-review [data-fr-error]');if(p){p.textContent=x;p.hidden=!x}};
// Only the text the owner sees goes: a draft that changed since it was drawn (a rewrite, an edit elsewhere) is drawn again
// instead, to read first; nothing sends while the Change box is open or its draft is being rewritten
async function frSend(id,quiet){const s=state.suggestions.find(x=>x.id===id),a=s&&frDraft(s);if(!a||!frReady(s)||fr.box)return false;
 if(a.revision!==fr.shown.get(id)){frPatch(s);return 'changed'}
 if(a.to_options?.length){if(quiet)return false;$('#fu-review').close();openSend(id,a.revision);return false}  /* who gets it is the owner's pick: the send dialog asks; the From is the draft's own (shown in the list) */
 await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'confirm_action',args:{suggestion_id:id,revision:a.revision,approval_id:crypto.randomUUID()}})});
 fr.gone.add(id);fr.undo.delete(id);fr.shown.delete(id);fr.sent++;return true}
// The Change box opens and closes in place: the drafts, their scroll and any rewrite under way stay as they are
function frBoxOpen(){const d=$('#fu-review');if(!fr.box){const n=frList().filter(s=>fr.checked.has(s.id)&&frReady(s)).length;fr.box={text:'',scope:n?'all':'one',one:fr.cur}}
 if(!d.querySelector('.fr-change'))d.querySelector('[data-fr-error]')?.before(htmlNodes(frBox(frList())));d.querySelector('[data-fr-change]')?.setAttribute('aria-expanded','true');frModes();
 const box=$('#fr-change-text');box?.focus({preventScroll:true});box?.closest('.fr-change')?.scrollIntoView({block:'nearest'})}
// Rewrite: each draft in scope goes through its to-do's chat path (follow_up_change), at most a few at once on the
// Machine; each shows "Rewriting…" where it is until its new text is back. Nothing is sent.
function frBoxClose(){const d=$('#fu-review');fr.box=null;d.querySelector('.fr-change')?.remove();d.querySelector('[data-fr-change]')?.setAttribute('aria-expanded','false');frModes();
 d.querySelector('.fr-item.on')?.focus({preventScroll:true})}
async function frChange(ids,text){const list=frList(),pick=list.filter(s=>ids.includes(s.id)&&(frReady(s)||fr.failed.has(s.id)));if(!pick.length||!text)return;
 const before=new Map(pick.map(s=>{const a=frDraft(s);return [s.id,{from:a?.revision,body:a?draftText(a):'',subject:a?.subject,text,seen:false}]}));
 const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'follow_up_change',args:{ids:pick.map(s=>s.id),text}})});
 for(const c of r.changing||[]){const b=before.get(c.id);if(!b)continue;fr.changing.set(c.id,{...b,from:c.revision});fr.failed.delete(c.id);fr.undo.delete(c.id)}
 for(const id of r.skipped||[])if(before.has(id))fr.failed.set(id,text);
 for(const s of list)if(before.has(s.id))frPatch(s);frCount();sendWatch()}
// Skip: the draft stays in the list, unchecked, dimmed and at the bottom, marked Skipped with an Undo; it is skipped for
// good (decide reject: that waiting point is handled) only when the review closes. The next draft becomes the current one.
function frSkip(id){const list=frList(),i=list.findIndex(s=>s.id===id);if(i<0||fr.skipped.has(id))return;
 fr.skipped.set(id,fr.checked.has(id));fr.checked.delete(id);fr.editing=fr.editing===id?null:fr.editing;
 const next=list.slice(i+1).find(s=>!fr.skipped.has(s.id))||list.slice(0,i).reverse().find(s=>!fr.skipped.has(s.id));fr.cur=(next||list[i]).id;frDraw(true)}
function frUnskip(id){if(!fr.skipped.has(id))return;if(fr.skipped.get(id))fr.checked.add(id);fr.skipped.delete(id);fr.cur=id;frDraw(true)}
// Everything left is skipped after a send: the review is done
function frDoneIfSkipped(){const d=$('#fu-review'),list=frList();if(d.open&&fr.sent&&list.length&&list.every(s=>fr.skipped.has(s.id))){toast(t(['{} follow-up on its way','{} follow-ups on their way'],fr.sent));d.close()}}
async function frAct(b){const d=$('#fu-review');frSay('');fr.busy=true;try{
 if(b.dataset.frSend){b.disabled=true;const r=await frSend(b.dataset.frSend);if(d.open)frDraw(true);if(r==='changed')frSay(t('This draft changed: read it, then send.'));else frDoneIfSkipped()}
 else if(b.dataset.frSkip)frSkip(b.dataset.frSkip)
 else if(b.dataset.frUnskip)frUnskip(b.dataset.frUnskip)
 else if(b.dataset.frEnd){const id=b.dataset.frEnd;b.disabled=true;  // Stop follow-ups here: this round ends, nothing sent (follow_ups.stop_here)
  await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'follow_up_end',args:{id}})});
  fr.gone.add(id);fr.checked.delete(id);fr.skipped.delete(id);toast(t('Follow-ups stopped here.'));frDraw(true)}
 else if(b.dataset.frEdit){fr.editing=fr.cur=b.dataset.frEdit;frDraw(true)}
 else if(b.hasAttribute('data-fr-cancel')){fr.editing=null;frDraw()}
 else if(b.dataset.frSave){const id=b.dataset.frSave,s=state.suggestions.find(x=>x.id===id),a=frDraft(s),text=d.querySelector('.fr-edit').value;b.disabled=true;
  const body=unplainDraft(text,draftText(a)),r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'revise_draft',args:{suggestion_id:id,revision:a.revision,body}})});
  Object.assign(a,{revision:r.revision,body:r.body??body});fr.editing=null;fr.undo.delete(id);frDraw()}
 else if(b.hasAttribute('data-fr-change')){if(fr.box)frBoxClose();else frBoxOpen()}
 else if(b.hasAttribute('data-fr-box-cancel'))frBoxClose()
 else if(b.hasAttribute('data-fr-box-go')){const text=($('#fr-change-text')?.value||'').trim();if(!text){$('#fr-change-text')?.focus();return}
  const scope=d.querySelector('[name=fr-scope]:checked')?.value||'one',list=frList(),ids=scope==='all'?list.filter(s=>fr.checked.has(s.id)&&frReady(s)).map(s=>s.id):[fr.box.one||fr.cur];
  b.disabled=true;await frChange(ids,text);frBoxClose()}
 else if(b.dataset.frRetry){const id=b.dataset.frRetry;b.disabled=true;await frChange([id],fr.failed.get(id)||'')}
 else if(b.dataset.frUndo){const id=b.dataset.frUndo,s=state.suggestions.find(x=>x.id===id),a=s&&frDraft(s),was=fr.undo.get(id);if(!a||!was)return;b.disabled=true;
  const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'revise_draft',args:{suggestion_id:id,revision:a.revision,body:was.body,...(was.subject&&a.subject!==was.subject?{subject:was.subject}:{})}})});
  Object.assign(a,{revision:r.revision,body:r.body??was.body,...(r.subject?{subject:r.subject}:{})});fr.undo.delete(id);frPatch(s)}
 else if(b.hasAttribute('data-fr-all')){if(fr.box||fr.changing.size)return;b.disabled=true;let left=0,moved=0;for(const s of frList().filter(s=>fr.checked.has(s.id)&&frReady(s))){const r=await frSend(s.id,true);if(r==='changed')moved++;else if(!r)left++}
  frDraw();frDoneIfSkipped();if(d.open)frSay([moved?t(['{} draft changed: read it, then send.','{} drafts changed: read them, then send.'],moved):'',left?t(['{} needs you to pick who gets it: send it on its own.','{} need you to pick who gets them: send them on their own.'],left):''].filter(Boolean).join(' '))}
 else if(b.hasAttribute('data-fr-close'))d.close()}catch(x){errCaught(x);frSay(x.message);b.disabled=false}finally{if(fr)fr.busy=false}}
$('#fu-review').addEventListener('click',e=>{const b=e.target.closest('button');if(b){frAct(b);return}const item=e.target.closest('[data-fr-at]');if(item&&!e.target.closest('input,textarea')&&fr.at!==+item.dataset.frAt)frMove(+item.dataset.frAt,true)});
$('#fu-review').addEventListener('change',e=>{if(e.target.name==='fr-scope'&&fr.box){fr.box.scope=e.target.value;return}const c=e.target.closest('[data-fr-check]');if(!c)return;c.checked?fr.checked.add(c.dataset.frCheck):fr.checked.delete(c.dataset.frCheck);frCount()});
$('#fu-review').addEventListener('input',e=>{if(e.target.id==='fr-change-text'&&fr?.box)fr.box.text=e.target.value});
$('#fu-review').addEventListener('keydown',e=>{if(!fr||e.isComposing||e.altKey||e.metaKey)return;const d=$('#fu-review'),list=frList(),cur=list[fr.at];
 if(e.target.id==='fr-change-text'){if(e.key==='Escape'){e.preventDefault();frBoxClose()}else if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();d.querySelector('[data-fr-box-go]')?.click()}return}
 if(e.target.matches('textarea')){if(e.key==='Escape'){e.preventDefault();fr.editing=null;frDraw()}else if(e.key==='Enter'&&e.ctrlKey){e.preventDefault();d.querySelector('[data-fr-save]')?.click()}return}
 if(e.ctrlKey||e.target.matches('input[type=text]'))return;const k=e.key;
 if(k==='j'||k==='ArrowDown'){e.preventDefault();frMove(fr.at+1)}
 else if(k==='k'||k==='ArrowUp'){e.preventDefault();frMove(fr.at-1)}
 else if(k==='Enter'&&cur&&!fr.box&&!e.target.matches('button')){e.preventDefault();d.querySelector(`[data-fr-send="${CSS.escape(cur.id)}"]`)?.click()}
 else if(k==='e'&&cur&&frReady(cur)){e.preventDefault();fr.editing=cur.id;frDraw(true)}
 else if(k==='s'&&cur){e.preventDefault();fr.skipped.has(cur.id)?frUnskip(cur.id):frSkip(cur.id)}
 else if(k==='c'){e.preventDefault();frBoxOpen()}
 else if(k==='x'&&cur){e.preventDefault();const on=!fr.checked.has(cur.id);on?fr.checked.add(cur.id):fr.checked.delete(cur.id);const c=$(`#fu-review [data-fr-check="${CSS.escape(cur.id)}"]`);if(c)c.checked=on;frCount()}});
$('#fu-review').addEventListener('close',()=>{const skip=[...(fr?.skipped.keys()||[])],sent=fr?.sent||fr?.gone.size||fr?.changing.size;fr=null;
 if(skip.length)Promise.all(skip.map(id=>decidePost(id,{choice:'reject',feedback:'',decision_id:crypto.randomUUID()}).catch(errCaught))).finally(()=>refresh().catch(()=>{}));else if(sent)refresh().catch(()=>{})});
document.addEventListener('click',e=>{const w=e.target.closest?.('[data-fu-card]');if(w){e.preventDefault();e.stopPropagation();fuShow(w.dataset.fuCard);return}});
// A board's follow-ups still being written: back to the to-do list, at their to-do
function fuShow(g){if(chatId)location.hash='';document.querySelector('nav [data-tab="inbox"]')?.click();folded.delete('foryou');render();
 const c=document.getElementById('fu-'+g.replace(':','-'));if(!c)return;c.scrollIntoView({block:'center',behavior:'smooth'});c.classList.remove('flash');void c.offsetWidth;c.classList.add('flash')}
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-fu-review]');if(!b)return;e.preventDefault();e.stopPropagation();frOpen(b.dataset.fuReview)},true);
