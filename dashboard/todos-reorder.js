// A lazy part (dashboard_parts.LAZY 'reorder'): a Reorders to-do (reorder.py, reorder_app.py), through lazyIn('reorder')
// in todos-cards.js: the item, its store, the last price, when it was last bought and how often, and a link that opens
// it at the store (s.reorder.way: 'open'). Nothing is bought here; the to-do's own buttons are Mark done, Snooze and
// Not needed.
const roMoney=(v,c)=>{try{return new Intl.NumberFormat(DL,{style:'currency',currency:c}).format(+v)}catch{return v+' '+c}};
const roDay=d=>{const[y,m,x]=String(d).split('-').map(Number);return Intl.DateTimeFormat(DL,{day:'numeric',month:'short',...(y!==new Date().getFullYear()?{year:'numeric'}:{})}).format(new Date(y,m-1,x))};
const roEvery=n=>n>=14?t('Every {} weeks',Math.round(n/7)):t('Every {} days',n);
function reorderBox(s){const r=s.reorder,url=r.way?.kind==='open'?safeURL(r.way.url):'',fact=(k,v)=>html`<div><dt>${k}</dt><dd>${v}</dd></div>`;
 return html`<p class="ro-item"><b translate="no">${r.title}</b>${r.variant?html`<span class="ro-sub" translate="no">${r.variant}</span>`:''}</p>
 <dl class="ro-facts">${fact(t('Store'),html`<span translate="no">${r.store_name||r.store}</span>`)}${fact(t('Last price'),roMoney(r.price,r.currency))}${fact(t('Last bought'),roDay(r.last_on))}${fact(t('Usually'),roEvery(r.usual))}</dl>
 ${url&&!closed(s)?html`<a class="ro-open open" href="${url}" target="_blank" rel="noreferrer">${t('Open at the store')} ↗</a>`:''}`}
