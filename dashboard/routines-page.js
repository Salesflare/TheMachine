// Routines (routines.py): work The Machine does on its own, on a rhythm; it only reads. Not a recurring to-do.
// Suggested: old OpenClaw jobs that fit, each with the result of one real run (routine_imports.py); Add or No thanks.
let routinesData=null,routinesAt=0;
const RT_STATE={ready:'Ready',nothing:'Nothing new',failed:'Didn’t work',running:'Running…'};
const rtTime=at=>localeTime(new Date('2000-01-01T'+at),DL,{hour:'numeric',minute:'2-digit'});
const rtDay=v=>localeDate(v,DL,{weekday:'short',day:'numeric',month:'short'});
function rtRhythm(r){const u=r.rule.unit,d=rpDate(r.anchor),wd=rpWeekday(d);if((r.rule.n||1)>1)return repeatText(r.rule,r.anchor);
 return u==='day'?t('Daily'):u==='weekday'?t('Weekdays'):u==='week'?t('Weekly on {}',wd):u==='year'?t('Yearly on {}',rpMonthDay(d)):r.rule.nth!=null?t(REPEAT_NTH_OPTION[r.rule.nth],wd):t('Monthly on day {}',d.getDate())}
const rtWhen=r=>[rtRhythm(r),rtTime(r.at),r.state==='paused'?t('Paused'):r.next_due?t('Next {}',rtDay(rpDate(r.next_due))):''].filter(Boolean).join(' · ');
const rtRun=x=>html`<div class="rt-run"><p class="rt-run-head"><span class="rt-state rt-${x.state}">${t(RT_STATE[x.state]||'')}</span><small>${rtDay(new Date(x.started_at))}</small></p>${
 x.state==='ready'?html`<div class="rt-result">${format(x.result,true)}</div>`:x.why?html`<p class="rt-why">${x.state==='failed'?t(x.why):x.why}</p>`:''}</div>`;
function rtCard(r){const [last,...older]=r.runs,paused=r.state==='paused';
 return html`<article class="rt${paused?html` paused`:''}" data-rt="${r.id}"><h3>${r.name}</h3><p class="rt-when">${rtWhen(r)}</p>${r.instructions!==r.name?html`<p class="rt-what">${r.instructions}</p>`:''}
  ${last?rtRun(last):html`<p class="rt-why">${t('No result yet.')}</p>`}${older.length?html`<details class="rt-earlier"><summary>${t('Earlier')}</summary>${older.map(rtRun)}</details>`:''}
  ${r.old_job?html`<div class="rt-old"><p>${t('Turn off the old OpenClaw job?')}</p><button type="button" class="ghost" data-rt-old="off">${t('Turn it off')}</button><button type="button" class="quiet" data-rt-old="keep">${t('Keep it')}</button></div>`:''}
  <div class="actions"><button type="button" class="ghost" data-rt-do="now"${last?.state==='running'?html` disabled`:''}>${t('Run now')}</button><details class="more-actions"><summary aria-label="${t('More actions')}" title="${t('More actions')}">${DOTS}</summary><div class="more-menu" role="group" aria-label="${t('More actions')}"><button type="button" data-rt-do="when">${t('Change when')}</button><button type="button" data-rt-do="${paused?'resume':'pause'}">${t(paused?'Resume':'Pause')}</button><button type="button" class="danger" data-rt-do="stop">${t('Stop')}</button></div></details></div></article>`}
const rtSuggested=r=>html`<article class="rt rt-s" data-rt="${r.id}"><h3>${r.name}</h3><p class="rt-when">${rtWhen(r)}</p><p class="rt-what">${r.instructions}</p>${r.runs[0]?rtRun(r.runs[0]):''}
 <div class="actions"><button type="button" class="primary" data-rt-do="accept">${t('Add')}</button><button type="button" class="quiet" data-rt-do="no">${t('No thanks')}</button></div></article>`;
function routinesRender(){const box=$('#routines-view'),list=routinesData?.routines;if(!box||!list)return;const typed=$('#rt-words')?.value||'';
 box.innerHTML=html`<form class="rt-new"><input id="rt-words" autocomplete="off" placeholder="${t('Every Monday, sum up my deals')}" aria-label="${t('New routine')}"><button class="primary">${t('Add')}</button></form>
  <p class="fine">${t('Routines only read. They don’t send or change anything.')}</p>${routinesData.suggested?.length?html`<section class="rt-sugg" aria-label="${t('Suggested')}"><h2>${t('Suggested')}</h2><p class="fine">${t('From your OpenClaw jobs. Each one ran once to show you.')}</p>${routinesData.suggested.map(rtSuggested)}</section>`:''}${list.length?list.map(rtCard):html`<p class="rt-empty">${t('No routines yet')}</p>`}`.s;
 $('#rt-words').value=typed}
async function routinesView(force){if(!force&&Date.now()-routinesAt<20000&&routinesData){routinesRender();return}
 try{routinesData=await request('api/routines');routinesAt=Date.now();routinesRender()}catch(e){errCaught(e);toast(e.message,true)}}
const rtPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
async function rtDo(action,args,b,done){if(b)b.disabled=true;try{routinesData={...routinesData,...await rtPost(action,args)};routinesAt=Date.now();routinesRender();if(done)toast(done);return true}catch(e){errCaught(e);toast(e.message,true);if(b)b.disabled=false;return false}}
$('#routines-view').addEventListener('submit',e=>{e.preventDefault();const f=e.target,input=f.querySelector('input'),words=input.value.trim();if(!words)return;
 if(f.classList.contains('rt-new'))rtDo('routine_new',{words},f.querySelector('button'),t('Routine added')).then(ok=>{if(ok)$('#rt-words').value=''});
 else rtDo('routine_when',{id:f.closest('[data-rt]').dataset.rt,words},f.querySelector('button'))});
$('#routines-view').addEventListener('click',e=>{const old=e.target.closest('[data-rt-old]');if(old){const choice=old.dataset.rtOld;rtDo('routine_old_job',{id:old.closest('[data-rt]').dataset.rt,choice},old,choice==='off'?t('Old job turned off'):'');return}
 const b=e.target.closest('[data-rt-do]');if(!b)return;const card=b.closest('[data-rt]'),id=card.dataset.rt,what=b.dataset.rtDo;
 if(what==='accept')rtDo('routine_accept',{id},b,t('Routine added'));
 else if(what==='no')rtDo('routine_state',{id,to:'stop'},b);
 else if(what==='now')rtDo('routine_run_now',{id},b,t('Running it now'));
 else if(what==='when'){card.querySelector('.rt-when-form')?.remove();card.querySelector('.actions').insertAdjacentHTML('beforebegin',html`<form class="rt-new rt-when-form"><input autocomplete="off" placeholder="${t('Every weekday at 8')}" aria-label="${t('Change when')}"><button class="primary">${t('Save')}</button></form>`.s);card.querySelector('.rt-when-form input').focus()}
 else if(what==='stop'&&!b.dataset.sure){e.stopPropagation();b.dataset.sure='1';b.textContent=t('Stop for good?');setTimeout(()=>{if(b.isConnected){delete b.dataset.sure;b.textContent=t('Stop')}},4000)}
 else rtDo('routine_state',{id,to:what},b,what==='stop'?t('Routine stopped'):'')});
