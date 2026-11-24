// Part of the Graph's part that loads when first needed (dashboard_parts.LAZY 'graph'): a project's follow-ups and
// Done when, and a board's follow-ups line; their links open the follow-up settings dialog (graph-followups-dialog.js).
// A project's page: its board and stage, its next step, and the latest moves with the message each came from.
// Done when (project_success.py): the project's success condition, the proof that met it (the message, and the live page
// when the condition asks for one) or that it was marked done by hand, why a review's "done" isn't proven yet, and what
// stands in its way with its one to-do. On no board, the box alone.
const PS_WHY={'unlinked':'The page doesn’t link to you yet','unloaded':'The page didn’t load','unsaid':'The link isn’t in their message',
 'no_url':'No link to the page yet','from_owner':'It needs a message from them','no_message':'No message shows it yet'};
const psBlock=x=>x.kind==='no_reply'?t('No reply in {} days',x.days)+(x.follow_ups?' · '+t('Follow-ups are on'):''):x.kind==='promise_theirs'?t('Waiting on {}: {}, due {}',x.who,x.what,shortDay(x.due)):t('Overdue for {}: {}, due {}',x.who,x.what,shortDay(x.due));
const successBox=s=>{if(!s)return '';const ev=s.evidence;
 const proof=s.done?(s.done_by==='evidence'&&ev?html`<p class="ps-proof ok">${t('Proven {}',shortDay(ev.at))}${ev.url?html` · <a href="${safeHref(ev.url)}" target="_blank" rel="noopener noreferrer" translate="no">${ev.url.replace(/^https:\/\/(www\.)?/,'').replace(/\/$/,'')}</a>`:''} <button type="button" class="link" data-quote-event="${ev.event_id}">Read</button></p>`:html`<p class="ps-proof">${t('Marked done by hand')}</p>`)
  :s.not_proven?html`<p class="ps-proof warn">${t('Not proven yet: {}',t(PS_WHY[s.not_proven]||s.not_proven))}</p>`:'';
 const block=!s.done&&s.blocker?html`<p class="ps-block">${psBlock(s.blocker)}${s.blocker.todo?html` · <a href="#card=${s.blocker.todo.id}" title="${s.blocker.todo.title}">${t('To-do')}</a>`:''}</p>`:'';
 return html`<div class="ps-box">${s.condition?html`<p class="ps-when">${t('Done when: {}',s.condition)}</p>`:''}${proof}${block}</div>`};
const stageBox=n=>{const b=n.board;if(!b)return n.success&&!n.team_only?html`<div class="graph-stage">${successBox(n.success)}</div>`:'';const moves=orEmpty(html`${(b.moves||[]).map(m=>html`<li>${shortDay(m.at)} · ${m.source==='owner'?`Moved to ${m.stage} by hand`:`${m.stage}: ${(m.source==='follow_up'?fuMoveReason(m,n):m.reason||'')}`}${m.event_id?html` <button type="button" class="link" data-quote-event="${m.event_id}">Read</button>`:''}</li>`)}`);
 const seen=n.team_only?'':html`<label class="seen-pick">Who sees it<select data-project-seen="${n.id}"><option value=""${b.visibility?'':html` selected`}>Like its board (${b.board_visibility==='only_you'?'only you':b.board_visibility==='people'?'chosen teammates':'team'})</option><option value="only_you"${b.visibility==='only_you'?html` selected`:''}>Only you</option><option value="team"${b.visibility==='team'?html` selected`:''}>Your team</option></select></label>`;
 return html`<div class="graph-stage"><p><b>${b.stage||''}</b> <span class="muted">on ${b.board}</span>${['only_you','people'].includes(b.visibility||b.board_visibility)?html`${' '}${seenBy(b.visibility||b.board_visibility)}`:''}</p>${b.next?html`<p>Next: ${b.next}</p>`:''}${successBox(b.success)}${moves?html`<ol aria-label="Moves">${moves}</ol>`:''}${n.team_only?'':fuBox(n)}${seen}</div>`};
document.addEventListener('change',async e=>{const t=e.target.closest?.('[data-project-seen]');if(!t)return;t.disabled=true;
 try{await graphPost('project_visibility',{node_id:t.dataset.projectSeen,visibility:t.value||null});toast(t.value==='only_you'?'Only you see this project now.':t.value==='team'?'Your team sees this project now.':'It follows its board now.');await graphPeople('',true)}catch(err){errCaught(err);toast(err.message,true)}finally{t.disabled=false}});
// Automated follow-ups (follow_ups.py): their settings for a board or one project (a project's own wins over its board's),
// the board's "Follow-ups on" line, a project's "Next follow-up", and a board's grouped to-do with its fast review:
// one follow-up at a time or the whole list, Send, Edit or Skip each, keys to move, Send all checked.
const fuDay=v=>{if(!v)return '';const d=new Date(v),n=new Date();if(d<=n||localDay(d)===localDay(n))return t('today');return (d-n)/864e5<6?localeDate(d,DL,{weekday:'short'}):localeDate(d,DL,{day:'numeric',month:'short'})};
const fuNoReply=n=>n?t(['No reply after {} follow-up','No reply after {} follow-ups'],n):t('Follow-ups stopped');
// Paused (follow_ups.pause): a small chip where the follow-up status shows; nothing is drafted, sent or ended meanwhile
// A project page's state: how it ended, else how busy it is
const projState=n=>{const c=n.project;return c?.outcome?endWord(c.outcome,c.deal):heatLabel(n.state)};
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
// The follow-up settings dialog loads when first opened (graph-followups-dialog.js, dashboard_parts.LAZY 'fudialog')
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-fu-open]');if(!b)return;e.preventDefault();e.stopPropagation();b.closest('details')?.removeAttribute('open');const{fuOpen:ref,fuFor:stage}=b.dataset;lazyRun('fudialog',()=>fuOpen(ref,stage))},true);
