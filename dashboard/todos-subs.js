// A lazy part (dashboard_parts.LAZY 'subs'): Subscriptions and trials (subscriptions.py). On its to-do (todos-cards.js,
// through lazyIn('subs')) a row per subscription: its price per month or year in the merchant's currency, its next
// charge, a trial's end or a price going up, and Keep or Cancel. Keep is saved at once and remembered. Cancel only shows
// the way out: the merchant's cancel page to open, and a draft to them that opens in the send dialog (todos-compose.js)
// and goes only on the owner's Send. Nothing here sends or changes anything.
const subsDrafts=new Map();
const sbMoney=(v,c)=>{try{return new Intl.NumberFormat(DL,{style:'currency',currency:c}).format(+v)}catch{return v+' '+c}};
const sbDay=d=>{const[y,m,x]=String(d).split('-').map(Number),at=new Date(y,m-1,x);return Intl.DateTimeFormat(DL,{day:'numeric',month:'short',...(y!==new Date().getFullYear()?{year:'numeric'}:{})}).format(at)};
function subsRow(s,r){const k=s.id+':'+r.n,d=subsDrafts.get(k),price=sbMoney(r.amount,r.currency),c=r.change||{};
 const pick=(to,label)=>html`<button type="button" data-sb="${s.id}" data-sb-n="${r.n}" data-sb-to="${to}">${label}</button>`;
 const what=html`<b translate="no">${r.name}</b><span class="sb-sub">${c.kind==='trial'?r.period==='year'?t('{} a year after the trial',price):t('{} a month after the trial',price):html`${r.period==='year'?t('{} a year',price):t('{} a month',price)} · ${t('Next charge {}',sbDay(r.next))}`}</span>${c.kind==='trial'?html`<span class="sb-flag">${t('Trial ends {}',sbDay(r.next))}</span>`:c.kind==='up'?html`<span class="sb-flag">${c.on&&c.on!==r.next?t('Price going up from {} to {} on {}',sbMoney(c.from,r.currency),price,sbDay(c.on)):t('Price going up from {} to {}',sbMoney(c.from,r.currency),price)}</span>`:''}`;
 const end=r.choice==='keep'?html`<span class="sb-end">${t('Kept')}${closed(s)?'':html` <button type="button" class="link" data-sb="${s.id}" data-sb-n="${r.n}" data-sb-to="">${t('Undo')}</button>`}</span>`
  :r.choice==='cancel'?html`<span class="sb-end">${t('Canceling')}${closed(s)?'':html` <button type="button" class="link" data-sb="${s.id}" data-sb-n="${r.n}" data-sb-to="">${t('Undo')}</button>`}</span>`
  :closed(s)?'':html`<span class="sb-pick" role="group" aria-label="${r.name}">${pick('keep',t('Keep'))}${pick('cancel',t('Cancel it'))}</span>`;
 const way=r.choice==='cancel'&&!closed(s)?d?html`<div class="sb-draft">${d.to?html`<p>${t('A draft to {} asks them to cancel it. It goes only when you send it.',d.to)}</p>`:''}<p class="sb-acts">${d.to?html`<button type="button" class="primary" data-sb-write="${k}">${t('Review and send')}</button>`:''}${d.link?html`<a href="${safeURL(d.link)}" target="_blank" rel="noreferrer">${t('Open their cancel page')} ↗</a>`:''}</p>${d.to||d.link?'':html`<p>${t('Cancel it in their app or on their site.')}</p>`}</div>`
  :html`<p class="sb-acts"><button type="button" class="link" data-sb="${s.id}" data-sb-n="${r.n}" data-sb-to="cancel">${t('Show how to cancel')}</button></p>`:'';
 return html`<li class="sb-row"><div class="sb-line">${r.event?html`<button type="button" class="sb-what sb-open" data-sb-open="${r.event}" data-sb-title="${r.name}">${what}</button>`:html`<div class="sb-what">${what}</div>`}${end}</div>${way}</li>`}
function subsBox(s){const rows=s.subs.rows,open=rows.some(r=>!r.choice);
 return html`<p class="sb-lead">${open||closed(s)?String(s.body||'').split('\n\n')[0]:t('All decided. Mark it done when you’re ready.')}</p><ul class="sb-list">${rows.map(r=>subsRow(s,r))}</ul>`}
document.addEventListener('click',async e=>{const o=e.target.closest('[data-sb-open]');if(o){e.preventDefault();openEvent(o.dataset.sbOpen,o.dataset.sbTitle);return}
 const w=e.target.closest('[data-sb-write]');if(w){e.preventDefault();const d=subsDrafts.get(w.dataset.sbWrite);if(d)lazyRun('compose',()=>openCompose(d.to,d.subject,'mailto:'+d.to+'?subject='+encodeURIComponent(d.subject)+'&body='+encodeURIComponent(d.body),d.body));return}
 const b=e.target.closest('[data-sb]');if(!b)return;e.preventDefault();const s=(state.suggestions||[]).find(x=>x.id===b.dataset.sb),r=s?.subs?.rows.find(x=>x.n===+b.dataset.sbN);if(!r)return;
 const was=r.choice,to=b.dataset.sbTo||null;b.disabled=true;
 try{const got=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'subs_pick',args:{suggestion_id:s.id,item:r.n,choice:to}})});
  r.choice=to;if(got.draft)subsDrafts.set(s.id+':'+r.n,got.draft);else subsDrafts.delete(s.id+':'+r.n);render();if(to==='keep')toast(t('Kept. It isn’t asked about again unless the price changes.'))}
 catch(err){r.choice=was;b.disabled=false;errCaught(err);toast(err.message,true)}});
