// A lazy part (dashboard_parts.LAZY 'areadigest'): the To-dos digest. The row at the top of the list (digestEntry,
// todos-learned.js) opens the last digest sent (as below), or today's so far, "Today so far": each area's done today
// and still open (notify.area_digest, the area_digest action), Work
// and Personal or the filter's one, as plain text with Copy. An area
// with nothing in it isn't shown. Read from the Machine each time it opens, so it is never older than the list.
// A tapped morning or evening digest notification, or its email's link (#digest=morning|evening, openDigestLink),
// opens that digest as it went (the digest_sent action) with Copy per area; none kept: today's, as above.
let adText=null,adSent=null;
const adAreas=()=>scopeFilter==='work'||scopeFilter==='personal'?[scopeFilter]:['work','personal'];
function adDialog(){let d=$('#area-digest');if(d)return d;
 d=document.createElement('dialog');d.id='area-digest';d.setAttribute('aria-labelledby','area-digest-title');document.body.append(d);
 d.addEventListener('click',async e=>{if(e.target===d||e.target.closest('[data-ad-close]')){d.close();return}
  const b=e.target.closest('[data-ad-copy]'),text=b&&(adSent?adSentCopy(b.dataset.adCopy):adText?.[b.dataset.adCopy]);if(!text)return;
  try{await navigator.clipboard.writeText(text);toast(t('Copied.'))}catch(err){errCaught(err);toast(t('Couldn’t copy automatically. Select the text to copy it.'),true)}});
 return d}
const adSentCopy=k=>k==='all'?adSent.title+'\n\n'+adSent.text:adSent.sections.find(s=>s.area===k)?.copy;
function adDraw(){const d=adDialog();if(adSent)return adSentDraw(d);const areas=adAreas(),one=areas.length===1,shown=adText?areas.filter(a=>adText[a]):[];
 const title=digestName('today');  // the row's own name for it (todos-learned.js)
 const copy=a=>one?t('Copy'):a==='work'?t('Copy Work'):t('Copy Personal');
 setHTML(d,html`<div class="snooze-heading"><h2 id="area-digest-title">${title}</h2><button type="button" data-ad-close aria-label="${t('Close')}">×</button></div>
 ${!adText?html`<p class="ad-fine">${t('Loading…')}</p>`:!shown.length?html`<p class="ad-fine">${t('Nothing to list yet.')}</p>`
 :shown.map(a=>html`<section class="ad-part">${one?'':html`<div class="ad-head"><h3>${a==='work'?t('Work'):t('Personal')}</h3><button type="button" class="ad-copy" data-ad-copy="${a}">${copy(a)}</button></div>`}<pre class="ad-text">${adText[a]}</pre></section>`)}
 ${one&&shown.length?html`<div class="actions"><button type="button" class="primary" data-ad-copy="${areas[0]}">${copy(areas[0])}</button></div>`:''}`)}
// Its lines drawn as they read (notify.read_blocks): an area a heading, Done today and Open for tomorrow under it, the
// to-dos a list whose "+N more" and meetings count close it, muted ('more'). Copy keeps the plain text.
function adBlocks(blocks){const out=[];let li=[];const flush=()=>{if(li.length)out.push(html`<ul class="ad-list">${li.map(([k,x])=>html`<li class="${k==='more'?'ad-more':''}">${x}</li>`)}</ul>`);li=[]};
 for(const [k,x] of blocks){if(k==='li'||k==='more'){li.push([k,x]);continue}flush();
  if(k==='h')out.push(html`<h3 class="ad-area">${x}</h3>`);else if(k==='sub')out.push(html`<h4 class="ad-sub">${x}</h4>`);
  else if(k!=='gap')out.push(html`<p class="${k==='meet'?'ad-meet':'ad-p'}">${x}</p>`)}
 flush();return html`<div class="ad-read">${out}</div>`}
// A hyphenated word ("to-dos") kept on one line, so a narrow headline never breaks it as "to-" and "dos"
const adKeep=s=>String(s||'').split(/(\S+-\S+)/).map((x,i)=>i%2?html`<span class="ad-nw">${x}</span>`:x);
// The digest as it went: which one by when it went ("Yesterday evening's digest", the row's name; its headline when
// that's unknown), when, its text, then Copy for each area it has (Copy Work, Copy Personal), else one Copy
function adSentDraw(d){const s=adSent,parts=s.sections.filter(x=>x.copy&&/^(work|personal)$/.test(x.area));
 setHTML(d,html`<div class="snooze-heading"><h2 id="area-digest-title">${s.at&&/^(morning|evening)$/.test(s.kind)?digestName(s.kind,s.at):adKeep(s.title)}</h2><button type="button" data-ad-close aria-label="${t('Close')}">×</button></div>
 ${s.at?html`<p class="ad-fine ad-when">${localeDate(s.at,DL,{weekday:'short',day:'numeric',month:'short',hour:'numeric',minute:'2-digit',hour12:H12})}</p>`:''}
 ${s.blocks?.length?adBlocks(s.blocks):html`<pre class="ad-text">${s.text}</pre>`}<div class="actions">${parts.length?parts.map(x=>html`<button type="button" class="ad-copy" data-ad-copy="${x.area}">${x.area==='work'?t('Copy Work'):t('Copy Personal')}</button>`)
 :html`<button type="button" class="primary" data-ad-copy="all">${t('Copy')}</button>`}</div>`)}
async function areaDigestOpen(sent){adText=adSent=null;adDraw();const d=$('#area-digest');if(!d.open)d.showModal();
 const ask=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
 try{const got=sent&&await ask('digest_sent',{kind:sent});if(got?.title)adSent={...got,sections:got.sections||[]};else adText=await ask('area_digest',{})}
 catch(err){errCaught(err);d.close();toast(err.message,true);return}
 if(d.open){adDraw();d.querySelector('[data-ad-copy]')?.focus()}}
