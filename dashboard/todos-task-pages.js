// Task pages (task_pages.py): offered after a handoff by email, approved here with a preview of exactly what the page
// shows, then one line in the draft. Answers from the page show quoted: their words, never instructions.
const pageApprove=new Map(),TP_SAID={on:'I’m on it',done:'Done',cant:'Can’t do this'};
const tpDay=d=>/^\d{4}-\d{2}-\d{2}/.test(d||'')?localeDate(new Date(d.slice(0,10)+'T12:00:00Z'),DL,{weekday:'short',day:'numeric',month:'short',timeZone:'UTC'}):'';
const TP_LOCK=html`<svg width="14" height="14" viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="7" width="10" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>`;
function taskPageBlock(s){const p=s.task_page,id=s.id;if(!p)return'';
 if(p.state==='offered'){const a=pageApprove.get(s.id);
  if(!a)return html`<div class="tp-suggest"><p>Add a task page? They see the status and answer there, no account needed.</p><div class="btns"><button type="button" data-tp-add="${id}">Add a task page</button><button type="button" class="quiet" data-tp-skip="${id}">No thanks</button></div></div>`;
  const v=p.preview||{},part=(k,body)=>{const off=a.leave.has(k);return html`<div class="tp-part${off?html` off`:''}">${body}${k==='summary'&&p.repeats?html`<small>Repeats the email</small>`:html`<button type="button" data-tp-leave="${id}" data-part="${k}">${off?'Put back':'Leave out'}</button>`}</div>`};
  return html`<section class="tp-approve" aria-label="Task page"><p class="tp-lede">They see this page</p><div class="tp-mini"><p class="tp-from">${t('{} shared a task with you',v.from)}</p><p class="tp-title">${v.title}</p>${v.due?part('due',html`<p>${t('Due {}',tpDay(v.due))}</p>`):''}${v.summary?part('summary',html`<p>${v.summary}</p>`):''}</div><p class="tp-never">${TP_LOCK}${t('Never shared: the email thread, your notes or other to-dos.')}</p><p class="tp-expiry">Link works for <span class="tp-days" role="radiogroup" aria-label="How long the link works">${(p.choices||[7,14,30]).map(d=>html`<button type="button" role="radio" aria-checked="${d===a.days}" data-tp-days="${id}" data-days="${d}">${d}</button>`)}</span> days</p><div class="actions"><button class="primary" data-tp-share="${id}">Add to email</button><button type="button" class="quiet" data-tp-cancel="${id}">Cancel</button></div></section>`}
 const until=tpDay(p.until),led=taskPageSent(s,taskActions(s))&&p.lead,earlier=(p.answers||[]).slice(0,led?-1:undefined);
 const answers=html`${earlier.reverse().map(x=>html`<div class="tp-reply"><b>Reply on the task page:</b> ${TP_SAID[x.answer]||''}${x.note?html`<q>${x.note}</q>`:''}<small>${tpDay(x.at)}</small></div>`)}`;
 const stop=html`<span class="tp-dot" aria-hidden="true">·</span><button type="button" class="tp-stop" data-tp-stop="${id}">Stop sharing</button>`;
 // The page as they see it: opens outside the dashboard (a new tab; the phone app hands it to the browser)
 const name=safeURL(p.link)?html`<a class="tp-open" href="${p.link}" target="_blank" rel="noreferrer">Task page<span aria-hidden="true"> ↗</span></a>`:html`<b>Task page</b>`;
 const line=p.state==='shared'?html`<span class="tp-what"><span class="tp-name">${name}</span> until <span class="tp-nw">${until}</span></span>${stop}`
  :p.state==='done'?html`<span class="tp-what"><span class="tp-name">${name}</span> ends <span class="tp-nw">${until}</span></span>${stop}`
  :html`<span>${p.state==='stopped'?'Task page stopped. The link no longer works.':'Task page ended.'}</span>`;
 return html`<div class="tp-shared">${line}</div>${answers}`}
// Once the email went out, it folds into one quiet line that opens to the email itself.
function taskPageSent(s,smart){const p=s.task_page;if(!p||p.state==='offered')return null;return smart.find(a=>a.kind==='email'&&(a.state||s.action_status)?.status==='sent')||null}
function taskPageSentLine(s,a){const at=tpDay((a.state||s.action_status)?.sent_at);return html`<details class="tp-sent"><summary>${t('Sent to {}',(a.to||[]).join(', '))}${at?html` · <span class="tp-nw">${at}</span>`:''}<span class="tp-chev" aria-hidden="true">›</span></summary>${draftBox(s,a,'')}</details>`}
$('#suggestions').addEventListener('click',async e=>{const b=e.target.closest('[data-tp-add],[data-tp-skip],[data-tp-leave],[data-tp-days],[data-tp-cancel],[data-tp-share],[data-tp-stop]');if(!b)return;
 const d=b.dataset,s=(state.suggestions||[]).find(x=>x.id===d.tpAdd);
 if(d.tpAdd){const p=s?.task_page||{};pageApprove.set(d.tpAdd,{leave:new Set(p.repeats?['summary']:[]),days:p.days||14});render();return}
 if(d.tpLeave){const a=pageApprove.get(d.tpLeave);if(a){a.leave.has(d.part)?a.leave.delete(d.part):a.leave.add(d.part);render()}return}
 if(d.tpDays){const a=pageApprove.get(d.tpDays);if(a){a.days=+d.days;render()}return}
 if(d.tpCancel){pageApprove.delete(d.tpCancel);render();return}
 b.disabled=true;
 try{if(d.tpShare){const a=pageApprove.get(d.tpShare);await fleetPost('task_page_share',{suggestion_id:d.tpShare,leave_out:[...(a?.leave||[])],days:a?.days||14});pageApprove.delete(d.tpShare);toast('Added to the email. It goes out when you send it.')}
  else if(d.tpSkip)await fleetPost('task_page_dismiss',{suggestion_id:d.tpSkip});
  else if(d.tpStop){await fleetPost('task_page_stop',{suggestion_id:d.tpStop});toast('Stopped. The link no longer works.')}
  await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#suggestions').addEventListener('click',async e=>{const b=e.target.closest('[data-handoff-not-mine]');if(!b)return;b.disabled=true;
 try{await fleetPost('fleet_handoff_not_mine',{suggestion_id:b.dataset.handoffNotMine});toast('Undone. Your teammate is told it isn’t yours.');await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
// Check in now: a short nudge to the teammate where it was asked, drafted on the to-do like any Do it (nothing is sent
// from here: the owner reads it and taps Send). With nothing connected to message them on, the to-do's chat opens and
// says so, calmly; something to say about this to-do is said on it (handoffNotes), never in a toast over another one.
$('#suggestions').addEventListener('click',async e=>{const b=e.target.closest('[data-handoff-checkin]');if(!b)return;e.preventDefault();const id=b.dataset.handoffCheckin;b.disabled=true;
 try{const r=await fleetPost('fleet_handoff_checkin',{suggestion_id:id});handoffNotes.delete(id);
  if(r.chat){location.hash='chat='+id;toast(r.why);$('#toast').dataset.about=id}
  await refresh()}catch(err){errCaught(err);handoffNotes.set(id,err.message);b.disabled=false;render()}});
$('#suggestions').addEventListener('click',async e=>{const b=e.target.closest('[data-handoff-take-back]');if(!b)return;b.disabled=true;
 try{await fleetPost('fleet_handoff_take_back',{suggestion_id:b.dataset.handoffTakeBack});toast('Taken back. It’s yours again.');await refresh()}catch(err){errCaught(err);toast(err.message,true)}finally{b.disabled=false}});  // a redraw may keep this button: it is free again either way
$('#suggestions').addEventListener('click',async e=>{const b=e.target.closest('[data-handoff-mine]');if(!b)return;b.disabled=true;
 try{await fleetPost('fleet_handoff_mine',{suggestion_id:b.dataset.handoffMine});toast(t('Moved to For you.'));await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#suggestions').addEventListener('click',async e=>{const b=e.target.closest('[data-fleet-take]');if(!b)return;b.disabled=true;
 try{await fleetPost('fleet_take',{suggestion_id:b.dataset.fleetTake});toast('It’s yours now. Your teammates’ Machines will see that.');await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
