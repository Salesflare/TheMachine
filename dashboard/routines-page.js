// Routines (routines.py): work The Machine does on its own, on a rhythm; it only reads. Not a recurring to-do.
// Suggested: old OpenClaw jobs that fit, each with the result of one real run (routine_imports.py); Add or No thanks.
let routinesData=null,routinesAt=0;
const RT_STATE={ready:'Ready',nothing:'Nothing new',failed:'Didn’t work',running:'Running…'};
const rtTime=at=>localeTime(new Date('2000-01-01T'+at),DL,{hour:'numeric',minute:'2-digit'});
const rtDay=v=>localeDate(v,DL,{weekday:'short',day:'numeric',month:'short'});
function rtRhythm(r){const u=r.rule.unit,d=rpDate(r.anchor),wd=rpWeekday(d);if((r.rule.n||1)>1)return repeatText(r.rule,r.anchor);
 return u==='day'?t('Daily'):u==='weekday'?t('Weekdays'):u==='week'?t('Weekly on {}',wd):u==='year'?t('Yearly on {}',rpMonthDay(d)):r.rule.nth!=null?t(REPEAT_NTH_OPTION[r.rule.nth],wd):t('Monthly on day {}',d.getDate())}
const rtWhen=r=>[rtRhythm(r),rtTime(r.at),r.state==='paused'?t('Paused'):r.next_due?t('Next {}',rtDay(rpDate(r.next_due))):''].filter(Boolean).join(' · ');
// A result is Markdown, as in the chat (lists, bold, headings), its ISO dates as the owner reads dates
const rtDates=v=>String(v||'').replace(/\b(\d{4})-(\d{2})-(\d{2})\b/g,(m,y,mo,d)=>localeDate(new Date(+y,mo-1,+d),DL,{day:'numeric',month:'short'}));
const rtRun=x=>html`<div class="rt-run"><p class="rt-run-head"><span class="rt-state rt-${x.state}">${t(RT_STATE[x.state]||'')}</span><small>${rtDay(new Date(x.started_at))}</small></p>${
 x.state==='ready'?html`<div class="rt-result">${chatMarkdown(rtDates(x.result))}</div>`:x.why?html`<p class="rt-why">${x.state==='failed'?t(x.why):x.why}</p>`:''}</div>`;
// Long ones fold like a to-do's text (todos-cards.js): a short preview, Show more for the rest
const rtRows=s=>String(s||'').split('\n').reduce((n,l)=>n+(l.trim()?Math.ceil(l.length/56):1),0);
function rtBody(r,inner,rows,always){const key='rt-'+r.id,fold=always||rows>3,open=expandedBodies.has(key);
 return html`<div class="rt-body${fold&&!open?html` clamp`:''}">${inner}</div>${fold?html`<button type="button" class="more" data-more="${key}" aria-expanded="${open}">${t(open?'Show less':'Show more')}</button>`:''}`}
function rtCard(r){const [last,...older]=r.runs,paused=r.state==='paused',what=r.instructions!==r.name&&r.instructions;
 return html`<article class="rt${paused?html` paused`:''}" data-rt="${r.id}"><h3>${r.name}</h3><p class="rt-when">${rtWhen(r)}</p>${what?html`<p class="rt-what rt-short">${what}</p>`:''}${rtBody(r,html`${last?rtRun(last):html`<p class="rt-why">${t('No result yet.')}</p>`}${older.length?html`<details class="rt-earlier"><summary>${t('Earlier')}</summary>${older.map(rtRun)}</details>`:''}`,last?1+rtRows(last.result||last.why):1,paused&&rtRows(last?.result||last?.why)>1)}
  ${r.old_job?html`<div class="rt-old"><p>${t('Turn off the old OpenClaw job?')}</p><button type="button" class="ghost" data-rt-old="off">${t('Turn it off')}</button><button type="button" class="quiet" data-rt-old="keep">${t('Keep it')}</button></div>`:''}
  <div class="actions">${paused?html`<button type="button" class="ghost" data-rt-do="resume">${t('Resume')}</button>`:html`<button type="button" class="ghost" data-rt-do="now"${last?.state==='running'?html` disabled`:''}>${t('Run now')}</button>`}<details class="more-actions"><summary aria-label="${t('More actions')}" title="${t('More actions')}">${DOTS}</summary><div class="more-menu" role="group" aria-label="${t('More actions')}"><button type="button" data-rt-do="edit">${t('Edit')}</button><button type="button" data-rt-do="when">${t('Change when')}</button>${paused?'':html`<button type="button" data-rt-do="pause">${t('Pause')}</button>`}<button type="button" class="danger" data-rt-do="stop">${t('Stop')}</button></div></details></div></article>`}
const rtSuggested=r=>html`<article class="rt rt-s" data-rt="${r.id}"><h3>${r.name}</h3><p class="rt-when">${rtWhen(r)}</p><p class="rt-what rt-short">${r.instructions}</p>${r.runs[0]?rtBody(r,rtRun(r.runs[0]),0,true):''}
 <div class="actions"><button type="button" class="primary" data-rt-do="accept">${t('Add')}</button><button type="button" class="quiet" data-rt-do="no">${t('No thanks')}</button></div></article>`;
const rtSection=(name,label,cards,fine)=>html`<section class="rt-sec rt-${name}" aria-label="${label}"><h2>${label}</h2>${fine?html`<p class="fine">${fine}</p>`:''}${cards}</section>`;
function routinesRender(){const box=$('#routines-view'),list=routinesData?.routines;if(!box||!list)return;const typed=$('#rt-words')?.value||'',sugg=routinesData.suggested||[],on=list.filter(r=>r.state!=='paused'),off=list.filter(r=>r.state==='paused');
 box.innerHTML=html`<form class="rt-new"><textarea id="rt-words" class="rt-grow" rows="1" spellcheck="true" autocapitalize="sentences" placeholder="${t('Every Monday, sum up my deals')}" aria-label="${t('New routine')}"></textarea><button class="primary">${t('Add')}</button></form>
  <p class="fine">${t('Routines only read. They don’t send or change anything.')}</p>${sugg.length?rtSection('sugg',t('Suggested'),sugg.map(rtSuggested),t('From your OpenClaw jobs. Each one ran once to show you.')):''}${
  on.length||!off.length?rtSection('mine',t('Your routines'),on.length?on.map(rtCard):html`<p class="rt-empty">${t('No routines yet')}</p>`):''}${off.length?rtSection('paused',t('Paused'),off.map(rtCard)):''}`.s;
 rtGrow(Object.assign($('#rt-words'),{value:typed}))}
// Grows with its words, up to six lines (routines-page.css)
function rtGrow(x){x.style.height='';x.style.height=x.scrollHeight+x.offsetHeight-x.clientHeight+'px'}
async function routinesView(force){if(!force&&Date.now()-routinesAt<20000&&routinesData){routinesRender();return}
 try{routinesData=await request('api/routines');routinesAt=Date.now();routinesRender()}catch(e){errCaught(e);toast(e.message,true)}}
const rtPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
async function rtDo(action,args,b,done){if(b)b.disabled=true;try{routinesData={...routinesData,...await rtPost(action,args)};routinesAt=Date.now();routinesRender();if(done)toast(done);return true}catch(e){errCaught(e);toast(e.message,true);if(b)b.disabled=false;return false}}
// Edit and Change when: one at a time, under the card's text, with Save and Cancel (Esc, or a click outside on a computer)
function rtOpen(card,kind){rtShut();card.querySelector('.more-actions').open=false;const r=routinesData.routines.find(x=>x.id===card.dataset.rt);
 card.querySelector('.actions').insertAdjacentHTML('beforebegin',html`<form class="rt-form" data-rt-form="${kind}">${kind==='edit'?html`<textarea class="rt-grow" rows="1" spellcheck="true" autocapitalize="sentences" aria-label="${t('Edit')}">${r?.instructions||''}</textarea>`:html`<input autocomplete="off" placeholder="${t('Every weekday at 8')}" aria-label="${t('Change when')}">`}<p class="rt-form-acts"><button class="primary">${t('Save')}</button><button type="button" class="quiet" data-rt-cancel>${t('Cancel')}</button></p></form>`.s);
 const x=card.querySelector('.rt-form').elements[0];if(kind==='edit')rtGrow(x);x.focus();x.setSelectionRange(x.value.length,x.value.length)}
function rtShut(back){const f=$('#routines-view .rt-form');if(!f)return;const s=f.closest('[data-rt]')?.querySelector('.more-actions>summary');f.remove();if(back)s?.focus({preventScroll:true})}
document.addEventListener('pointerdown',e=>{const f=$('#routines-view .rt-form');if(f&&!f.contains(e.target)&&matchMedia('(pointer:fine)').matches&&!e.target.closest?.('[data-rt-do="edit"],[data-rt-do="when"]'))rtShut()});
$('#routines-view').addEventListener('submit',e=>{e.preventDefault();const f=e.target,input=f.querySelector('textarea,input'),words=input.value.trim(),b=f.querySelector('.primary');if(!words)return;
 if(input.id==='rt-words')rtDo('routine_new',{words},b,t('Routine added')).then(ok=>{if(ok)rtGrow(Object.assign($('#rt-words'),{value:''}))});
 else rtDo(f.dataset.rtForm==='edit'?'routine_edit':'routine_when',{id:f.closest('[data-rt]').dataset.rt,words},b)});
// As the chat box: Enter adds or saves, Shift+Enter or a phone's Enter is a new line
$('#routines-view').addEventListener('input',e=>{if(e.target.matches('.rt-grow'))rtGrow(e.target)});
$('#routines-view').addEventListener('keydown',e=>{const x=e.target,f=x.form;if(!f)return;if(e.key==='Escape'&&f.matches('.rt-form')){e.preventDefault();e.stopPropagation();rtShut(true);return}
 if(x.tagName!=='TEXTAREA'||e.key!=='Enter'||e.isComposing||e.keyCode===229||e.altKey)return;
 if(!(e.ctrlKey||e.metaKey)&&(e.shiftKey||matchMedia('(pointer: coarse)').matches))return;e.preventDefault();e.stopPropagation();f.requestSubmit()});
$('#routines-view').addEventListener('click',e=>{if(e.target.closest('[data-rt-cancel]')){rtShut(true);return}
 const m=e.target.closest('[data-more]');if(m){const key=m.dataset.more,open=!expandedBodies.has(key);open?expandedBodies.add(key):expandedBodies.delete(key);m.previousElementSibling.classList.toggle('clamp',!open);m.setAttribute('aria-expanded',open);m.textContent=t(open?'Show less':'Show more');return}
 const old=e.target.closest('[data-rt-old]');if(old){const choice=old.dataset.rtOld;rtDo('routine_old_job',{id:old.closest('[data-rt]').dataset.rt,choice},old,choice==='off'?t('Old job turned off'):'');return}
 const b=e.target.closest('[data-rt-do]');if(!b)return;const card=b.closest('[data-rt]'),id=card.dataset.rt,what=b.dataset.rtDo;
 if(what==='accept')rtDo('routine_accept',{id},b,t('Routine added'));
 else if(what==='no')rtDo('routine_state',{id,to:'stop'},b);
 else if(what==='now')rtDo('routine_run_now',{id},b,t('Running it now'));
 else if(what==='edit'||what==='when')rtOpen(card,what);
 else if(what==='stop'&&!b.dataset.sure){e.stopPropagation();b.dataset.sure='1';b.textContent=t('Stop for good?');setTimeout(()=>{if(b.isConnected){delete b.dataset.sure;b.textContent=t('Stop')}},4000)}
 else rtDo('routine_state',{id,to:what},b,what==='stop'?t('Routine stopped'):'')});
