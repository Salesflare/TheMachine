// Ask to review (fleet_reviews.py): the owner asks one person in the matching Fleet (Work to-dos to the Work Fleet,
// Personal ones to the Family) to look at this to-do's draft or result. The reviewer gets a to-do of their own to
// approve, comment on, edit or decline. Their changes come back as tracked changes the owner accepts (all, some) or
// ignores; accepting only changes the draft. Sending stays the owner's own tap on Send. Nothing here sends anything.
const reviewing=new Map(),reviewViews=new Map(),reviewDrafts=new Map();
// Offered where a Fleet of this to-do's side (Work, or the Family for Personal) carries reviews and has someone in it.
const canReview=s=>!closed(s)&&s.status!=='snoozed'&&!!state?.fleet?.on&&(state.fleet.reviews||[]).includes(s.scope==='work'?'work':'personal')&&!s.review?.open&&!s.review_in&&!reviewing.has(s.id);
const reviewMore=s=>canReview(s)?`<button type="button" class="ghost" data-review-ask="${esc(s.id)}">${esc(t('Ask to review'))}</button>`:'';
const reviewChip=(v,n,d)=>d.dropped?.includes(n)?'':`<span class="agent-get"><i class="via-ico via-${v.kind==='email'?'mail':'chat'}" aria-hidden="true"></i>${esc(v.label)}<button type="button" class="chip-x" data-review-drop="${n}" aria-label="${esc(t('Leave out {}',v.label))}" title="${esc(t('Leave out'))}">×</button></span>`;
// The picker: who (one person), what goes (the draft or the to-do's text, shown as it is), its sources as chips, a note.
function reviewEditor(s){const d=reviewing.get(s.id);if(!d||closed(s))return'';const id=esc(s.id);
 const who=d.fleets.flatMap(f=>f.members.map(m=>[f.id+'|'+m.member_id,d.fleets.length>1?`${m.name} (${f.name})`:m.name,m.name]));
 const pick=who.length<=4?`<span class="agent-switch" role="radiogroup" aria-label="${esc(t('Ask to review'))}">${who.map(([v,n])=>`<label><input type="radio" name="to" value="${esc(v)}"${d.to===v?' checked':''}><span>${esc(n)}</span></label>`).join('')}</span>`
  :`<select name="to" class="review-pick" aria-label="${esc(t('Ask to review'))}">${who.map(([v,n])=>`<option value="${esc(v)}"${d.to===v?' selected':''}>${esc(n)}</option>`).join('')}</select>`;
 const name=firstName((who.find(([v])=>v===d.to)||[])[2]||'');
 const chips=(d.sources||[]).map((v,n)=>reviewChip(v,n,d)).join('');
 const what=d.what==='draft'?`<div class="review-what"><p class="review-label">${esc(t('Your draft'))}</p>${d.subject?`<p class="review-subject" translate="no">${esc(d.subject)}</p>`:''}<div class="review-text" translate="no">${esc(d.body)}</div></div>`
  :`<div class="review-what"><p class="review-label">${esc(t('This to-do'))}</p><div class="review-text" translate="no">${esc(d.body)}</div></div>`;
 return`<form class="review-form agent-sheet" data-card="${id}"><div class="agent-sheet-head"><span class="agent-sheet-title">${esc(t('Ask to review'))}</span>${pick}</div>${what}
 ${chips?`<div class="agent-gets" aria-label="${esc(t('Goes along'))}">${chips}</div>`:''}
 <textarea name="note" class="agent-note" rows="1" maxlength="300" placeholder="${esc(t('Add a note for {}',name||t('them')))}" aria-label="${esc(t('Add a note for {}',name||t('them')))}">${esc(d.note||'')}</textarea>
 <p class="agent-what">${esc(t('Only this to-do goes. {} can suggest changes; nothing is sent until you send it.',name||t('They')))}</p>
 <div class="agent-sheet-foot"><button type="button" class="ghost" data-review-cancel="${id}">${esc(t('Cancel'))}</button><button class="primary">${esc(t('Ask'))}</button></div></form>`}
const reviewWords=w=>w.map(([k,x])=>k==='='?esc(x):k==='-'?`<del>${esc(x)}</del>`:`<ins>${esc(x)}</ins>`).join('');
// The owner's tracked changes: who and when, their comment, each change with a box (all ticked), then Accept or Ignore.
function reviewChanges(s,v){const who=firstName(v.name);
 const rows=v.hunks.map(h=>`<li class="review-hunk"><label><input type="checkbox" name="pick" value="${esc(h.id)}" checked><span class="review-diff" translate="no">${h.field==='subject'?`<span class="review-field">${esc(t('Subject'))}</span> `:''}${reviewWords(h.words)}</span></label></li>`).join('');
 return`<form class="review-changes" data-card="${esc(s.id)}" aria-label="${esc(t('{}’s changes',who))}"><p class="review-by">${esc(t('{}’s changes',who))} · ${time(v.at,true)}</p>
 ${v.changed_since?`<p class="note">${esc(t('The draft changed since. Changes go in where they still fit.'))}</p>`:''}<ul class="review-hunks">${rows}</ul>
 <p class="muted review-after">${esc(t('Accepting changes the draft only. Send it yourself after.'))}</p>
 <div class="actions"><button class="primary" data-review-apply="all">${esc(t('Accept all'))}</button>${v.hunks.length>1?`<button class="ghost" data-review-apply="some">${esc(t('Accept selected'))}</button>`:''}<button class="ghost" data-review-apply="ignore">${esc(t('Ignore'))}</button><button type="button" class="quiet" data-review-hide="${esc(s.id)}">${esc(t('Hide'))}</button></div></form>`}
// On the owner's to-do: how the review goes, the reviewer's comment, and Withdraw or See changes.
function reviewOwner(s){const r=s.review;if(!r)return'';const pending=r.stage==='changes'&&!r.decided&&r.changes>0;
 const comment=r.comment?`<blockquote class="review-comment" translate="no">${esc(r.comment)}</blockquote>`:'';
 const tools=closed(s)?'':r.open?`<button type="button" class="link" data-review-withdraw="${esc(s.id)}">${esc(t('Withdraw'))}</button>`:pending&&!reviewViews.has(s.id)?`<button type="button" class="link" data-review-see="${esc(s.id)}">${esc(t('See changes'))}</button>`:'';
 return`<p class="note fleet review-line${r.open||pending?'':' handled'}" role="status">${esc(r.line)}${tools?' · '+tools:''}</p>${comment}${pending&&reviewViews.has(s.id)&&!closed(s)?reviewChanges(s,reviewViews.get(s.id)):''}`}
// On the reviewer's review to-do: what they were sent, editable in place, a comment, and Approve / Send changes / Decline.
function reviewIn(s){const r=s.review_in;if(!r||!r.open||closed(s))return'';const who=firstName(r.from);  // their note is in the to-do's text
 const d=reviewDrafts.get(s.id)||{},subject=d.subject??r.subject??'',body=d.body??r.body,changed=(r.what==='draft'&&subject!==(r.subject||''))||body!==r.body;
 return`<form class="review-in agent-sheet" data-card="${esc(s.id)}"><div class="agent-sheet-head"><span class="agent-sheet-title">${esc(r.what==='draft'?t('{}’s draft',who):t('{}’s to-do',who))}</span>${changed?`<span class="chip review-edited">${esc(t('Edited'))}</span>`:''}</div>
 ${r.what==='draft'?`<input name="subject" class="review-subject-in" maxlength="300" value="${esc(subject)}" aria-label="${esc(t('Subject'))}" translate="no">`:''}
 <textarea name="body" class="review-body-in" rows="6" maxlength="8000" aria-label="${esc(t('Edit the text'))}" translate="no">${esc(body)}</textarea>
 <textarea name="comment" class="agent-note" rows="1" maxlength="1000" placeholder="${esc(t('Add a comment for {}',who))}" aria-label="${esc(t('Add a comment for {}',who))}">${esc(d.comment||'')}</textarea>
 <p class="agent-what">${esc(t('Edits go back to {} as suggestions. Nothing is sent from here.',who))}</p>
 <div class="agent-sheet-foot"><button type="button" class="quiet" data-review-reply="declined">${esc(t('Decline'))}</button>${changed?`<button class="primary" data-review-reply="changes">${esc(t('Send changes'))}</button>`:`<button type="button" class="ghost" data-review-reply="commented">${esc(t('Send comment'))}</button><button class="primary" data-review-reply="approved">${esc(t('Approve'))}</button>`}</div></form>`}
const reviewBlock=s=>reviewOwner(s)+reviewIn(s);
// A review to-do that is still open keeps its own buttons (above); the card's usual ones would do nothing useful there.
const reviewHolds=s=>!!(s.review_in?.open&&!closed(s));
$('#suggestions').addEventListener('click',async e=>{
 const c=e.target.closest('[data-review-cancel]');if(c){reviewing.delete(c.dataset.reviewCancel);render();return}
 const h=e.target.closest('[data-review-hide]');if(h){reviewViews.delete(h.dataset.reviewHide);render();return}
 const drop=e.target.closest('[data-review-drop]'),dd=drop&&reviewing.get(drop.closest('form').dataset.card);
 if(dd){dd.dropped=[...(dd.dropped||[]),+drop.dataset.reviewDrop];render();return}
 const ask=e.target.closest('[data-review-ask]');
 if(ask){ask.disabled=true;ask.closest('details')?.removeAttribute('open');
  try{const d=await fleetPost('fleet_review_options',{suggestion_id:ask.dataset.reviewAsk});const f=d.fleets[0],m=f?.members[0];
   reviewing.set(d.suggestion_id,{...d,to:m?f.id+'|'+m.member_id:''});render()}catch(err){errCaught(err);ask.disabled=false;toast(err.message,true)}return}
 const w=e.target.closest('[data-review-withdraw]');
 if(w){w.disabled=true;try{await fleetPost('fleet_review_withdraw',{suggestion_id:w.dataset.reviewWithdraw});toast(t('Review request withdrawn.'));await refresh()}catch(err){errCaught(err);w.disabled=false;toast(err.message,true)}return}
 const see=e.target.closest('[data-review-see]');
 if(see){see.disabled=true;try{reviewViews.set(see.dataset.reviewSee,await fleetPost('fleet_review_view',{suggestion_id:see.dataset.reviewSee}));render()}catch(err){errCaught(err);see.disabled=false;toast(err.message,true)}return}
 const ap=e.target.closest('[data-review-apply]');
 if(ap){e.preventDefault();const form=ap.closest('form'),id=form.dataset.card,how=ap.dataset.reviewApply;
  const picks=how==='some'?[...form.querySelectorAll('input[name=pick]:checked')].map(x=>x.value):how;
  if(Array.isArray(picks)&&!picks.length){toast(t('Pick a change first.'),true);return}
  ap.disabled=true;try{const r=await fleetPost('fleet_review_apply',{suggestion_id:id,picks});reviewViews.delete(id);
   toast(how==='ignore'?t('Changes ignored.'):r.missed?t('Accepted {} changes. {} no longer fit.',r.applied,r.missed):t('Accepted. Read the draft, then send it yourself.'));await refresh()}catch(err){errCaught(err);ap.disabled=false;toast(err.message,true)}return}
 const rp=e.target.closest('[data-review-reply]');
 if(rp){e.preventDefault();const form=rp.closest('form'),id=form.dataset.card,stage=rp.dataset.reviewReply;
  const args={suggestion_id:id,stage,comment:form.elements.comment.value.trim(),body:form.elements.body.value,...(form.elements.subject?{subject:form.elements.subject.value}:{})};
  rp.disabled=true;try{await fleetPost('fleet_review_reply',args);reviewDrafts.delete(id);toast(stage==='declined'?t('Declined.'):t('Sent back. Nothing else goes anywhere.'));await refresh()}catch(err){errCaught(err);rp.disabled=false;toast(err.message,true)}}});
$('#suggestions').addEventListener('input',e=>{const f=e.target.closest('.review-form');const d=f&&reviewing.get(f.dataset.card);
 if(d){const moved=d.to!==f.elements.to.value;Object.assign(d,{to:f.elements.to.value,note:f.elements.note.value});if(moved)render();return}
 const r=e.target.closest('.review-in');if(!r)return;const id=r.dataset.card,had=reviewDrafts.get(id)||{};
 const s=(state?.suggestions||[]).find(x=>x.id===id),was=s?.review_in;if(!was)return;
 const now={subject:r.elements.subject?r.elements.subject.value:undefined,body:r.elements.body.value,comment:r.elements.comment.value};reviewDrafts.set(id,now);
 const edited=x=>(was.what==='draft'&&(x.subject??was.subject??'')!==(was.subject||''))||(x.body??was.body)!==was.body;
 if(edited(had)!==edited(now)){const at=e.target,pos=at.selectionStart;render();const back=document.querySelector(`.review-in[data-card="${CSS.escape(id)}"] [name="${at.name}"]`);if(back){back.focus();try{back.setSelectionRange(pos,pos)}catch{}}}});
$('#suggestions').addEventListener('submit',async e=>{const f=e.target;if(f.classList.contains('review-in')||f.classList.contains('review-changes')){e.preventDefault();return}
 if(!f.classList.contains('review-form'))return;e.preventDefault();const d=reviewing.get(f.dataset.card)||{},[fleet,member_id]=f.elements.to.value.split('|');
 const btn=f.querySelector('button.primary');btn.disabled=true;
 try{await fleetPost('fleet_review_ask',{suggestion_id:f.dataset.card,fleet,member_id,note:f.elements.note.value.trim(),sources:(d.sources||[]).map((_,n)=>n).filter(n=>!d.dropped?.includes(n))});
  reviewing.delete(f.dataset.card);toast(t('Asked for a review. The to-do shows how it goes.'));await refresh()}catch(err){errCaught(err);btn.disabled=false;toast(err.message,true)}});
