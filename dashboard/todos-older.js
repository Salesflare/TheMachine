// A lazy part (dashboard_parts.LAZY 'older'): Older's rows, drawn while it is open (shell-render.js draws its head and
// isOlder in todos-rows.js picks them), with Dismiss all over them. Dismiss all asks once in place, then each to-do is
// marked Not needed as its own Not needed and Still needed? do it (a reject decision, "No longer needed": the same
// learning), all out of the list at once; the toast's Undo reopens them all (shell-toast.js), and they stay in Older.
let olderAsk=false,olderIds=[];
function olderRows(l){olderIds=l.map(s=>s.id);
 return html`<div class="merge-offer older-bar">${olderAsk?html`<span>${t('Dismiss {} to-dos?',l.length)}</span><span class="still-acts"><button type="button" class="ghost" data-older-all="go">${t('Dismiss')}</button><button type="button" class="quiet" data-older-all="">${t('Cancel')}</button></span>`
  :html`<span class="older-why">${t('Nothing new on these for a week.')}</span><span class="still-acts"><button type="button" class="ghost" data-older-all="ask">${t('Dismiss all')}</button></span>`}</div>${l.map(s=>suggestionCard(s,'Older'))}`}
async function olderAll(){const l=state.suggestions.filter(s=>olderIds.includes(s.id)&&!closed(s)),at=new Date().toISOString();olderAsk=false;if(!l.length){render();return}
 for(const s of l)Object.assign(s,{status:'rejected',closed_at:at});localEdits++;render();
 const r=await Promise.allSettled(l.map(s=>decidePost(s.id,{choice:'reject',feedback:'No longer needed',decision_id:crypto.randomUUID()}))),done=l.filter((s,i)=>r[i].status==='fulfilled'),bad=r.find(x=>x.status==='rejected');
 if(bad){errCaught(bad.reason);toast(bad.reason.message,true)}else toast(t('Marked not needed'),false,done.map(s=>s.id).join(','));
 refresh().catch(()=>{})}
// Still needed? on a to-do (todos-rows.js stillLine asks for it): how long nothing touched it, Not needed and Keep
function stillNeeded(s){const days=Math.floor((Date.now()-Date.parse(s.still_needed.since))/864e5);  // touched since it asked: the question alone
 return html`<div class="merge-offer still-needed"><span><strong>${t('Still needed?')}</strong> ${days>=7?html`<small>${t('Untouched for {} days',days)}</small>`:''}</span><span class="still-acts"><button type="button" class="ghost" data-still="drop" data-card="${s.id}">${t('Not needed')}</button><button type="button" class="quiet" data-still="keep" data-card="${s.id}" data-ask="${s.still_needed.id}">${t('Keep')}</button></span></div>`}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-still]');if(!b)return;e.preventDefault();b.disabled=true;const id=b.dataset.card;
 try{if(b.dataset.still==='drop'){await saveDecision(id,'reject','No longer needed');return}
  await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'recap_decide',args:{id:b.dataset.ask,choice:'keep',decision_id:crypto.randomUUID()}})});
  toast(t('Kept'));await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
document.addEventListener('click',e=>{const b=e.target.closest('[data-older-all]');if(!b)return;e.preventDefault();const v=b.dataset.olderAll;
 if(v==='go'){b.disabled=true;olderAll();return}
 olderAsk=v==='ask';render();if(olderAsk)$('#older-list [data-older-all="go"]')?.focus()});
