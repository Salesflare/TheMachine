// Task pages (task_pages.py): offered after a handoff by email, approved here with a preview of exactly what the page
// shows, then one line in the draft. Answers from the page show quoted: their words, never instructions.
const pageApprove=new Map(),TP_SAID={on:'I’m on it',done:'Done',cant:'Can’t do this'};
const tpDay=d=>/^\d{4}-\d{2}-\d{2}/.test(d||'')?new Date(d.slice(0,10)+'T12:00:00Z').toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short',timeZone:'UTC'}):'';
const TP_LOCK='<svg width="14" height="14" viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="7" width="10" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>';
function taskPageBlock(s){const p=s.task_page,id=esc(s.id);if(!p)return'';
 if(p.state==='offered'){const a=pageApprove.get(s.id);
  if(!a)return`<div class="tp-suggest"><p>Add a task page? They see the status and answer there, no account needed.</p><div class="btns"><button type="button" data-tp-add="${id}">Add a task page</button><button type="button" class="quiet" data-tp-skip="${id}">No thanks</button></div></div>`;
  const v=p.preview||{},part=(k,html)=>{const off=a.leave.has(k);return`<div class="tp-part${off?' off':''}">${html}${k==='summary'&&p.repeats?'<small>Repeats the email</small>':`<button type="button" data-tp-leave="${id}" data-part="${k}">${off?'Put back':'Leave out'}</button>`}</div>`};
  return`<section class="tp-approve" aria-label="Task page"><p class="tp-lede">They see this page</p><div class="tp-mini"><p class="tp-from">${esc(t('{} shared a task with you',v.from))}</p><p class="tp-title">${esc(v.title)}</p>${v.due?part('due',`<p>${esc(t('Due {}',tpDay(v.due)))}</p>`):''}${v.summary?part('summary',`<p>${esc(v.summary)}</p>`):''}</div><p class="tp-never">${TP_LOCK}${esc(t('Never shared: the email thread, your notes or other to-dos.'))}</p><p class="tp-expiry">Link works for <span class="tp-days" role="radiogroup" aria-label="How long the link works">${(p.choices||[7,14,30]).map(d=>`<button type="button" role="radio" aria-checked="${d===a.days}" data-tp-days="${id}" data-days="${d}">${d}</button>`).join('')}</span> days</p><div class="actions"><button class="primary" data-tp-share="${id}">Add to email</button><button type="button" class="quiet" data-tp-cancel="${id}">Cancel</button></div></section>`}
 const until=tpDay(p.until),led=taskPageSent(s,taskActions(s))&&p.lead,earlier=(p.answers||[]).slice(0,led?-1:undefined);
 const answers=earlier.reverse().map(x=>`<div class="tp-reply"><b>Reply on the task page:</b> ${esc(TP_SAID[x.answer]||'')}${x.note?`<q>${esc(x.note)}</q>`:''}<small>${esc(tpDay(x.at))}</small></div>`).join('');
 const stop=`<span class="tp-dot" aria-hidden="true">·</span><button type="button" class="tp-stop" data-tp-stop="${id}">Stop sharing</button>`;
 const line=p.state==='shared'?`<span class="tp-what"><b>Task page</b> until <span class="tp-nw">${esc(until)}</span></span>${stop}`
  :p.state==='done'?`<span class="tp-what"><b>Task page</b> ends <span class="tp-nw">${esc(until)}</span></span>${stop}`
  :`<span>${p.state==='stopped'?'Task page stopped. The link no longer works.':'Task page ended.'}</span>`;
 return`<div class="tp-shared">${line}</div>${answers}`}
// Once the email went out, it folds into one quiet line that opens to the email itself.
function taskPageSent(s,smart){const p=s.task_page;if(!p||p.state==='offered')return null;return smart.find(a=>a.kind==='email'&&(a.state||s.action_status)?.status==='sent')||null}
function taskPageSentLine(s,a){const at=tpDay((a.state||s.action_status)?.sent_at);return`<details class="tp-sent"><summary>${esc(t('Sent to {}',(a.to||[]).join(', ')))}${at?` · <span class="tp-nw">${esc(at)}</span>`:''}<span class="tp-chev" aria-hidden="true">›</span></summary>${draftBox(s,a,'')}</details>`}
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
// Check in now: the to-do's chat, to ask the teammate how it goes (nothing is sent from here)
$('#suggestions').addEventListener('click',e=>{const b=e.target.closest('[data-handoff-checkin]');if(!b)return;e.preventDefault();location.hash='chat='+b.dataset.handoffCheckin});
$('#suggestions').addEventListener('click',async e=>{const b=e.target.closest('[data-handoff-take-back]');if(!b)return;b.disabled=true;
 try{await fleetPost('fleet_handoff_take_back',{suggestion_id:b.dataset.handoffTakeBack});toast('Taken back. It’s yours again.');await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#suggestions').addEventListener('click',async e=>{const b=e.target.closest('[data-handoff-mine]');if(!b)return;b.disabled=true;
 try{await fleetPost('fleet_handoff_mine',{suggestion_id:b.dataset.handoffMine});toast('It’s yours. The to-do keeps its usual buttons.');await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#suggestions').addEventListener('click',async e=>{const b=e.target.closest('[data-fleet-take]');if(!b)return;b.disabled=true;
 try{await fleetPost('fleet_take',{suggestion_id:b.dataset.fleetTake});toast('It’s yours now. Your teammates’ Machines will see that.');await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
