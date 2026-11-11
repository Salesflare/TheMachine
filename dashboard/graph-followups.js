// Automated follow-ups (follow_ups.py) on the to-do list: a board's grouped to-do, its progress while a batch goes out,
// and what a tap on them does. A project's page, a board's "Follow-ups on" line and their settings are in the Graph's
// part (graph-followups-settings.js); the grouped to-do's fast review is in graph-followups-review.js (LAZY
// 'followups'): both load when first needed (dashboard_parts.LAZY).
// The board's follow-ups as last loaded for the Graph (fuLoad): an edit clears them (graphPost).
let fuKept=null;
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
// The fast review's state (graph-followups-review.js): set only once its part is in and it opened.
let fr=null;
const frDraft=s=>taskActions(s).find(a=>DRAFT_KINDS.includes(a.kind)&&draftText(a));
// The project's name without the board's in front (follow_ups.short_name): the title names the board already
const frName=f=>f.name||f.project;
// A tap on a group's Review opens it at once when its part is in, else once it is.
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-fu-review]');if(!b)return;e.preventDefault();e.stopPropagation();const g=b.dataset.fuReview;lazyRun('followups',()=>frOpen(g))},true);
document.addEventListener('click',e=>{const w=e.target.closest?.('[data-fu-card]');if(w){e.preventDefault();e.stopPropagation();fuShow(w.dataset.fuCard);return}});
// A board's follow-ups still being written: back to the to-do list, at their to-do
function fuShow(g){if(chatId)location.hash='';document.querySelector('nav [data-tab="inbox"]')?.click();folded.delete('foryou');render();
 const c=document.getElementById('fu-'+g.replace(':','-'));if(!c)return;c.scrollIntoView({block:'center',behavior:'smooth'});c.classList.remove('flash');void c.offsetWidth;c.classList.add('flash')}
