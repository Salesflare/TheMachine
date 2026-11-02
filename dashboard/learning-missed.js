// Missed to-dos (Learning, How it's going): the weekly check of messages that got no to-do (missed_work.py). One
// number (the share that likely needed one, with its range), the misses it found to check (each opens the message and
// takes the owner's Real miss or Not a miss, kept on this Machine).
const MW_CHANNEL={email:'Email',message:'Message',meeting:'Meeting'};
const mwPct=v=>v==null?null:Math.round(100*v);
const mwUrl=u=>typeof u==='string'&&/^https:\/\//.test(u)?u:null;  // only https links open, like the server keeps them
function missedHTML(m){if(!m)return'';const est=m.adjusted||m.raw;if(!est||est.rate==null)return'';
 const day=new Date(m.at).toLocaleDateString(DL,{day:'numeric',month:'short'});
 const row=x=>{const url=mwUrl(x.url),id=Number(x.event_id);return`<div class="mw-row"><span class="grow"><small>${esc(t(MW_CHANNEL[x.channel]||'Message'))} · ${esc(x.area==='Personal'?t('Personal'):x.area)}</small>${esc(x.reason||'')}</span>`
  +`<span class="mw-acts">${url?`<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(t('Open'))}</a>`:''}`
  +`<button type="button" data-mw-label="real" data-mw-id="${id}" aria-pressed="${x.label==='real'}">${esc(t('Real miss'))}</button>`
  +`<button type="button" data-mw-label="not" data-mw-id="${id}" aria-pressed="${x.label==='not'}">${esc(t('Not a miss'))}</button></span></div>`};

 return `<h3 class="q-h">${esc(t('Missed to-dos'))}</h3><p class="learn-intro">${esc(t('Each week I check a sample of messages that got no to-do. Last check {}.',day))}</p>`
  +`<div class="q-tiles mw-tiles">${qTile(mwPct(est.rate),'Likely missed',t(['Of {} message with no to-do','Of {} messages with no to-do'],Number(m.population||0).toLocaleString(DL)),`<small class="q-was">${esc(t('Between {}% and {}%',mwPct(est.low),mwPct(est.high)))}</small>`)}</div>`
  +(m.misses?.length?`<div class="list mw-list">${m.misses.map(row).join('')}</div>`:'')}
$('#quality').addEventListener('click',async e=>{const b=e.target.closest('[data-mw-label]');if(!b)return;const on=b.getAttribute('aria-pressed')==='true';b.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'missed_work_label',args:{event_id:Number(b.dataset.mwId),label:on?'':b.dataset.mwLabel}})});
  state.missed_work=r.missed_work;$('#quality').innerHTML=qualityHTML(state.quality)+missedHTML(state.missed_work)}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
