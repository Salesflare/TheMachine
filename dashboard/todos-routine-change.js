// A lazy part (dashboard_parts.LAZY 'routinetodos', with todos-cleanup.js): todos-cards.js draws it through
// lazyIn('routinetodos'), nothing until it's in.
// Also change the routine (routine_changes.py): what changes in its words; saved only on Change it. On the card, and in
// its chat under the reply that made it (todos-chat-thread.js chatLog).
const routineChangeOpen=new Set(),routineChangePart=(k,w,gone)=>w?html`<p class="rt-part"><span>${k}</span>${gone?html`<del translate="no">${w}</del>`:html`<ins translate="no">${w}</ins>`}</p>`:'';
const routineChangeBlock=(s,c=s.routine_change)=>!c||closed(s)?'':routineChangeOpen.has(s.id)?html`<div class="change-editor" role="group" aria-label="${t('Change the routine {}?',c.name)}"><p>${htmlT('Change the routine {}?',html`<b translate="no">${c.name}</b>`)}</p>${routineChangePart(t('Now'),c.old,1)}${routineChangePart(t('New'),c.new)}<div class="actions"><button class="primary" data-rt-change="${s.id}" data-save="1">${t('Change it')}</button><button class="ghost" data-rt-change="${s.id}" data-save="">${t('Keep it as is')}</button></div></div>`
 :html`<button class="ghost rt-offer" data-rt-change="${s.id}">${t('Also change the routine')}</button>`;
document.addEventListener('click',async e=>{const b=e.target.closest('[data-rt-change]'),id=b?.dataset.rtChange;if(!b)return;e.preventDefault();
 if(!('save' in b.dataset)){routineChangeOpen.add(id);render();$(`[data-rt-change="${id}"][data-save="1"]`)?.focus();return}
 b.disabled=true;try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:b.dataset.save?'routine_change_save':'routine_change_keep',args:{suggestion_id:id}})});
  routineChangeOpen.delete(id);await refresh();if(b.dataset.save)toast(r.line);if(chat&&chatId===id){chat.cursor=null;chatPoll()}}catch(err){errCaught(err);toast(err.message,true);b.disabled=false}});
// In the to-do's chat (todos-chat-thread.js chatLog): the same offer, under the reply of the run that made it (its
// `at`), before the owner's next message
function routineChangeRow(s,rows){const c=s.routine_change;if(!c||closed(s))return;let n=rows.findIndex(i=>i.kind==='you'&&(i.at||0)>(c.at||0));if(n<0)n=rows.length;
 const r=rows.slice(0,n).findLastIndex(i=>i.kind==='reply');if(r>=0)n=r+1;rows.splice(n,0,{kind:'rc',at:rows[n-1]?.at||c.at,html:html`<div class="chat-event chat-routine-change">${routineChangeBlock(s)}</div>`})}
