// A lazy part (dashboard_parts.LAZY 'areadigest'): the To-dos digest. Digest at the top of the list (digestEntry,
// todos-learned.js) opens it: each area's done today and still open (notify.area_digest, the area_digest action), Work
// and Personal or the filter's one, as plain text with Copy, the same text the morning digest's email carries. An area
// with nothing in it isn't shown. Read from the Machine each time it opens, so it is never older than the list.
let adText=null;
const adAreas=()=>scopeFilter==='work'||scopeFilter==='personal'?[scopeFilter]:['work','personal'];
function adDialog(){let d=$('#area-digest');if(d)return d;
 d=document.createElement('dialog');d.id='area-digest';d.setAttribute('aria-labelledby','area-digest-title');document.body.append(d);
 d.addEventListener('click',async e=>{if(e.target===d||e.target.closest('[data-ad-close]')){d.close();return}
  const b=e.target.closest('[data-ad-copy]');if(!b||!adText?.[b.dataset.adCopy])return;
  try{await navigator.clipboard.writeText(adText[b.dataset.adCopy]);toast(t('Copied.'))}catch(err){errCaught(err);toast(t('Couldn’t copy automatically. Select the text to copy it.'),true)}});
 return d}
function adDraw(){const d=adDialog(),areas=adAreas(),one=areas.length===1,shown=adText?areas.filter(a=>adText[a]):[];
 const title=one?(areas[0]==='work'?t('Work digest'):t('Personal digest')):t('Digest');
 const copy=a=>one?t('Copy'):a==='work'?t('Copy Work'):t('Copy Personal');
 setHTML(d,html`<div class="snooze-heading"><h2 id="area-digest-title">${title}</h2><button type="button" data-ad-close aria-label="${t('Close')}">×</button></div>
 ${!adText?html`<p class="ad-fine">${t('Loading…')}</p>`:!shown.length?html`<p class="ad-fine">${t('Nothing to list yet.')}</p>`
 :shown.map(a=>html`<section class="ad-part">${one?'':html`<div class="ad-head"><h3>${a==='work'?t('Work'):t('Personal')}</h3><button type="button" class="ad-copy" data-ad-copy="${a}">${copy(a)}</button></div>`}<pre class="ad-text">${adText[a]}</pre></section>`)}
 ${one&&shown.length?html`<div class="actions"><button type="button" class="primary" data-ad-copy="${areas[0]}">${copy(areas[0])}</button></div>`:''}`)}
async function areaDigestOpen(){adText=null;adDraw();const d=$('#area-digest');if(!d.open)d.showModal();
 try{adText=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'area_digest',args:{}})})}
 catch(err){errCaught(err);d.close();toast(err.message,true);return}
 if(d.open){adDraw();d.querySelector('[data-ad-copy]')?.focus()}}
