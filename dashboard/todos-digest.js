// A lazy part (dashboard_parts.LAZY 'digest'): the Daily digest (reading_digest.py). On its to-do (todos-cards.js, through
// lazyIn('digest')): each pick with why it matters, its mail to open (the original, read only), More or Less like this.
// On its routine's card (routines-page.js): what it picks for, a short list the owner sees and edits.
function digestRow(s,i){const fb=(to,label)=>html`<button type="button" data-dg="${s.id}" data-dg-n="${i.n}" data-dg-to="${to}" aria-pressed="${i.feedback===to}">${t(label)}</button>`;
 const what=html`<small translate="no">${i.from}</small><b translate="no">${i.title}</b>`;
 return html`<li class="dg-row">${i.event?html`<button type="button" class="dg-what dg-open" data-dg-open="${i.event}" data-dg-title="${i.title||i.from}">${what}</button>`:html`<div class="dg-what">${what}</div>`}
  <p class="dg-why">${i.why}</p><p class="dg-acts">${closed(s)?'':html`<span class="dg-fb" role="group" aria-label="${i.title}">${fb('more','More like this')}${fb('less','Less like this')}</span>`}${i.url?html`<a class="dg-out" href="${safeURL(i.url)}" target="_blank" rel="noreferrer">${t('Open in your mail')} ↗</a>`:''}</p></li>`}
function digestBox(s){return html`<p class="dg-lead">${String(s.body||'').split('\n\n')[0]}</p><ol class="dg-list">${s.digest.items.map(i=>digestRow(s,i))}</ol>`}
// The routine's card: More of and Less of, each topic with its remove; one field adds to either
const dgChip=x=>html`<span class="dg-chip${x.source==='learned'?html` learned`:''}" translate="no"${x.source==='learned'?html` title="${t('Learned from what you read')}"`:''}>${x.topic}<button type="button" data-dg-drop="${x.topic}" aria-label="${t('Remove {}',x.topic)}">×</button></span>`;
function digestInterests(r){const l=r.interests||{more:[],less:[]},line=(k,label)=>l[k].length?html`<p class="dg-line"><span>${t(label)}</span>${l[k].map(dgChip)}</p>`:'';
 return html`<div class="dg-int">${line('more','More of')}${line('less','Less of')}${l.more.length||l.less.length?'':html`<p class="dg-line"><span>${t('It learns from what you read.')}</span></p>`}
  <p class="dg-add"><input class="dg-add-in" maxlength="40" placeholder="${t('Add a topic')}" aria-label="${t('Add a topic')}"><select class="dg-add-kind" aria-label="${t('List')}"><option value="more">${t('More of')}</option><option value="less">${t('Less of')}</option></select><button type="button" class="ghost" data-dg-add>${t('Add')}</button></p></div>`}
async function dgPost(action,args){return request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})})}
function dgShow(interests){const r=(routinesData?.routines||[]).find(x=>x.template==='digest');if(r){r.interests=interests;routinesRender()}}
async function dgInterest(args,b){if(b)b.disabled=true;try{dgShow((await dgPost('digest_interest',args)).interests);return true}catch(err){errCaught(err);toast(err.message,true);if(b)b.disabled=false;return false}}
document.addEventListener('click',async e=>{const o=e.target.closest('[data-dg-open]');if(o){e.preventDefault();openEvent(o.dataset.dgOpen,o.dataset.dgTitle);return}
 const d=e.target.closest('[data-dg-drop]');if(d){dgInterest({topic:d.dataset.dgDrop,remove:true},d);return}
 const a=e.target.closest('[data-dg-add]');if(a){const box=a.closest('.dg-add'),input=box.querySelector('.dg-add-in'),topic=input.value.trim();if(!topic){input.focus();return}
  if(await dgInterest({topic,kind:box.querySelector('.dg-add-kind').value},a))$('#routines-view .dg-add-in')?.focus();return}
 const b=e.target.closest('[data-dg]');if(!b)return;e.preventDefault();const s=(state.suggestions||[]).find(x=>x.id===b.dataset.dg),i=s?.digest?.items.find(x=>x.n===+b.dataset.dgN);if(!i)return;
 const was=i.feedback,to=was===b.dataset.dgTo?'':b.dataset.dgTo;i.feedback=to||null;render();  // shown at once, back if it didn't save
 try{await dgPost('digest_feedback',{suggestion_id:s.id,item:i.n,feedback:to});if(to)toast(t(to==='more'?'More like this from now on':'Less like this from now on'))}catch(err){i.feedback=was;render();errCaught(err);toast(err.message,true)}});
document.addEventListener('keydown',e=>{if(e.key!=='Enter'||e.isComposing||!e.target.matches?.('.dg-add-in'))return;e.preventDefault();e.target.closest('.dg-add').querySelector('[data-dg-add]').click()});
