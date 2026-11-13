// A lazy part (dashboard_parts.LAZY 'routinetodos'): todos-cards.js draws a cleanup to-do through lazyIn('routinetodos'),
// its plain text until this part is in. Its to-do has no Do it or Ask for changes (todos-cards.js choices).
// A routine template's cleanup (mail_cleanup.py): a row per newsletter or spam mail with Keep or Unsubscribe (Not spam or
// Spam), kept here until the one confirm; nothing changes before it. Then each row says how it went, and the "Pick …"
// lead gives way to the to-do's Finished line (todos-cards.js cleanupSettled).
const cleanupPicks=new Map();
const CLEAN_DONE={one_click:'Unsubscribed',mailto:'Unsubscribed',junk:'Moved to Junk',spam:'Marked as spam'};
const cleanupOut=(href,label)=>html`<a class="cl-end" href="${safeURL(href)}" target="_blank" rel="noreferrer">${t(label)} ↗</a>`;
function cleanupRow(s,news,i){const p=(cleanupPicks.get(s.id)||{})[i.n]||'',pick=(to,label)=>html`<button type="button" data-cl="${s.id}" data-cl-n="${i.n}" data-cl-to="${to}" aria-pressed="${p===to}">${t(label)}</button>`;
 const end=i.state==='open'&&!closed(s)?html`<span class="cl-pick" role="group" aria-label="${i.from}">${pick('keep',news?'Keep':'Not spam')}${pick('go',news?'Unsubscribe':'Spam')}</span>`
  :i.state==='done'?html`<span class="cl-end ok">${t(CLEAN_DONE[i.how]||'Done')}</span>`:i.state==='kept'?html`<span class="cl-end">${t(news?'Kept':'Not spam')}</span>`
  :i.state==='yours'&&i.link?cleanupOut(i.link,'Open unsubscribe page')
  :i.state==='failed'?html`<span class="cl-end bad">${t('Didn’t work')}</span>`:i.state==='unknown'?html`<span class="cl-end">${t('Sent, not confirmed')}</span>`:i.state==='working'?html`<span class="cl-end">${t('Working…')}</span>`:'';
 const what=html`<b translate="no">${i.from}</b>${i.count>1?html` <small>×${i.count}</small>`:''}<span class="cl-sub" translate="no">${i.why||i.title}</span>`;
 // sender and subject open its kept mail in the viewer, read only
 return html`<li class="cl-row">${i.event?html`<button type="button" class="cl-what cl-open" data-cl-open="${i.event}"${news?'':html` data-cl-local`} data-cl-title="${i.title||i.from}">${what}</button>`:html`<div class="cl-what">${what}</div>`}${end}</li>`}
function cleanupBox(s){const c=s.cleanup,news=c.kind==='newsletters',picks=cleanupPicks.get(s.id)||{},go=Object.values(picks).filter(v=>v==='go').length,open=!closed(s)&&c.items.some(i=>i.state==='open');
 const lead=String(s.body||'').split('\n\n')[0];
 return html`${open?html`<p class="cl-lead">${lead}</p>`:''}<ul class="cl-list">${c.items.map(i=>cleanupRow(s,news,i))}</ul>${open?html`<p class="fine cl-fine">${t(news?'Unsubscribe uses the list’s own link or unsubscribe email.':'Spam moves it to your spam folder.')}</p>
  <p class="cl-acts"><button type="button" class="primary" data-cl-go="${s.id}"${Object.keys(picks).length?'':html` disabled`}>${go?t(news?'Unsubscribe from {}':'Mark {} as spam',go):t('Save picks')}</button>${c.items.filter(i=>i.state==='open').length>1&&c.items.some(i=>i.state==='open'&&!picks[i.n])?html`<button type="button" class="link" data-cl-all="${s.id}">${t(news?'Unsubscribe from all':'Mark all as spam')}</button>`:''}</p>`:''}`}
document.addEventListener('click',async e=>{const o=e.target.closest('[data-cl-open]');if(o){e.preventDefault();openEvent(o.dataset.clOpen,o.dataset.clTitle,'clLocal' in o.dataset);return}  // spam: no remote images
 const b=e.target.closest('[data-cl],[data-cl-go],[data-cl-all]');if(!b)return;e.preventDefault();
 const id=b.dataset.cl||b.dataset.clGo||b.dataset.clAll,s=(state.suggestions||[]).find(x=>x.id===id);if(!s?.cleanup)return;const picks=cleanupPicks.get(id)||{};
 if(!b.dataset.clGo){if(b.dataset.clAll)s.cleanup.items.filter(i=>i.state==='open').forEach(i=>picks[i.n]='go');else if(picks[b.dataset.clN]===b.dataset.clTo)delete picks[b.dataset.clN];else picks[b.dataset.clN]=b.dataset.clTo;
  cleanupPicks.set(id,picks);render();return}
 b.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'routine_cleanup',args:{suggestion_id:id,picks}})});cleanupPicks.delete(id);await refresh()}
 catch(err){errCaught(err);toast(err.message,true);b.disabled=false}});
