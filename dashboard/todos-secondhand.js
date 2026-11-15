// A lazy part (dashboard_parts.LAZY 'secondhand'): a Second-hand finds to-do (secondhand.py, secondhand_app.py), through
// lazyIn('secondhand') in todos-cards.js: the listings found so far, newest on top, each with its photo, title, price and
// verdict; or a search the site stopped (its Open leads the to-do's buttons, todos-cards.js). Its setup and search on the
// Routines page are routines-page.js's. The Machine never contacts a seller, bids or buys: a listing opens for the owner.
// A row per listing, its photo first. A photo the site won't serve leaves its place empty (sh-nopic). Its photo and
// title open the listing in The Machine's browser (data-sh-url), like Open.
const shRow=s=>i=>{const href=safeURL(i.url),open=html` href="${state.browser_link||href}" target="_blank" rel="noreferrer" data-sh-open="${s.id}" data-sh-url="${href}"`;
 return html`<li class="sh-row"><a class="sh-pic"${open} tabindex="-1" aria-hidden="true">${i.photo?html`<img src="${i.photo}" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer">`:''}</a>
 <div class="sh-text"><a class="sh-title"${open} translate="no">${i.title||t('Listing')}</a>${i.price_text?html`<b class="sh-price" translate="no">${i.price_text}</b>`:''}<p class="sh-verdict">${i.verdict}</p></div></li>`};
function secondhandBox(s){const x=s.secondhand,search=safeURL(x.url);
 if(x.blocked)return html`<p class="sh-lead">${String(s.body||'').split('\n\n')[0]}</p>`;
 return html`<ul class="sh-list">${x.items.map(shRow(s))}</ul>${search?html`<p class="sh-more"><a href="${search}" target="_blank" rel="noreferrer">${t('The whole search on {}',x.site||x.search)} ↗</a></p>`:''}`}
document.addEventListener('error',e=>{const i=e.target;if(i?.tagName==='IMG'&&i.parentElement?.classList.contains('sh-pic')){i.parentElement.classList.add('sh-nopic');i.remove()}},true);
// Open, or a listing: in front in The Machine's browser; on a computer its Browser pane, elsewhere the browser's own
// link in a new tab (opened in the tap itself, so it is never blocked)
document.addEventListener('click',async e=>{const o=e.target.closest('[data-sh-open]');if(!o)return;e.preventDefault();
 if(o.getAttribute('aria-disabled'))return;if(state.browser_link&&!browserPane())window.open(state.browser_link,'_blank','noopener');o.setAttribute('aria-disabled','true');
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'secondhand_open',args:{suggestion_id:o.dataset.shOpen,...(o.dataset.shUrl?{url:o.dataset.shUrl}:{})}})});
  if(!r.shown)toast(r.error||t('I couldn’t reach the browser on this computer.'),true);else if(!state.browser_link||browserPane())toast(t('The browser is in front now.'))}
 catch(err){errCaught(err);toast(err.message,true)}finally{o.removeAttribute('aria-disabled')}});
