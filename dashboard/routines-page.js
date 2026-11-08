// Routines (routines.py): work The Machine does on its own, on a rhythm; it only reads. Not a recurring to-do.
// Suggested: old OpenClaw jobs that fit, or patterns in what the owner does (routine_patterns.py, with
// why: what was seen, on the rhythm line), each with the result of one real run; Add or No thanks.
// A new one shows a test run first (routine_try, dry: nothing sent or kept): Add, Change or Cancel. Edit's Try it, too.
// Script steps (Edit): Get data runs a command first and its output goes to the run; Check gets the result.
let routinesData=null,routinesAt=0,rtForm=null,rtTimer=0;
const RT_STATE={ready:'Ready',nothing:'Nothing new',failed:'Didn’t work',running:'Running…'};
const rtTime=at=>localeTime(new Date('2000-01-01T'+at),DL,{hour:'numeric',minute:'2-digit'});
const rtDay=v=>localeDate(v,DL,{weekday:'short',day:'numeric',month:'short'});
function rtRhythm(r){const u=r.rule.unit,d=rpDate(r.anchor),wd=rpWeekday(d);if((r.rule.n||1)>1)return repeatText(r.rule,r.anchor);
 return u==='day'?t('Daily'):u==='weekday'?t('Weekdays'):u==='week'?t('Weekly on {}',wd):u==='year'?t('Yearly on {}',rpMonthDay(d)):r.rule.nth!=null?t(REPEAT_NTH_OPTION[r.rule.nth],wd):t('Monthly on day {}',d.getDate())}
const rtWhen=r=>[rtRhythm(r),rtTime(r.at),r.state==='paused'?t('Paused'):r.next_due?t('Next {}',rtDay(rpDate(r.next_due))):''].filter(Boolean).join(' · ');
// A test run wears its own chip and says nothing was sent or saved; a result is Markdown, as in the chat (lists, bold, headings), its ISO dates as the owner reads dates; Used: the owner's skills it followed
const rtDates=v=>String(v||'').replace(/\b(\d{4})-(\d{2})-(\d{2})\b/g,(m,y,mo,d)=>localeDate(new Date(+y,mo-1,+d),DL,{day:'numeric',month:'short'}));
const rtRun=(x,test)=>html`<div class="rt-run"><p class="rt-run-head">${test?html`<span class="rt-state rt-test">${t('Test run')}</span><small>${x.state==='running'?t('Running…'):t('Nothing sent or saved')}${x.got?html` · <span class="rt-nowrap">${t('Got data')}</span>`:''}</small>`:html`<span class="rt-state rt-${x.state}">${t(RT_STATE[x.state]||'')}</span><small>${rtDay(new Date(x.started_at))}</small>`}</p>${
 x.state==='ready'?html`<div class="rt-result">${chatMarkdown(rtDates(x.result))}</div>`:x.why?html`<p class="rt-why">${x.state==='failed'?t(x.why):x.why}</p>${x.detail?html`<pre class="rt-detail">${x.detail}</pre>`:''}`:''}${x.used?.length?html`<p class="rt-used">${t('Used: {}',x.used.join(', '))}</p>`:''}</div>`;
const rtStepLine=r=>['get','check'].map(k=>r.steps?.[k]?html`<p class="rt-step"><span>${t(k==='get'?'Get data':'Check')}</span> <code>${r.steps[k].command}</code></p>`:'');
// Long ones fold like a to-do's text (todos-cards.js): a short preview, Show more for the rest
const rtRows=s=>String(s||'').split('\n').reduce((n,l)=>n+(l.trim()?Math.ceil(l.length/56):1),0);
function rtBody(r,inner,rows,always){const key='rt-'+r.id,fold=always||rows>3,open=expandedBodies.has(key);
 return html`<div class="rt-body${fold&&!open?html` clamp`:''}">${inner}</div>${fold?html`<button type="button" class="more" data-more="${key}" aria-expanded="${open}">${t(open?'Show less':'Show more')}</button>`:''}`}
function rtCard(r){const [last,...older]=r.runs,paused=r.state==='paused',what=r.instructions!==r.name&&r.instructions;
 return html`<article class="rt${paused?html` paused`:''}" data-rt="${r.id}"><h3>${r.name}</h3><p class="rt-when">${rtWhen(r)}</p>${what?html`<p class="rt-what rt-short">${what}</p>`:''}${rtStepLine(r)}${rtBody(r,html`${last?rtRun(last):html`<p class="rt-why">${t('No result yet.')}</p>`}${older.length?html`<details class="rt-earlier"><summary>${t('Earlier')}</summary>${older.map(x=>rtRun(x))}</details>`:''}`,last?1+rtRows(last.result||last.why):1,paused&&rtRows(last?.result||last?.why)>1)}
  ${r.old_job?html`<div class="rt-old"><p>${t('Turn off the old OpenClaw job?')}</p><button type="button" class="ghost" data-rt-old="off">${t('Turn it off')}</button><button type="button" class="quiet" data-rt-old="keep">${t('Keep it')}</button></div>`:''}
  <div class="actions">${paused?html`<button type="button" class="ghost" data-rt-do="resume">${t('Resume')}</button>`:html`<button type="button" class="ghost" data-rt-do="now"${last?.state==='running'?html` disabled`:''}>${t('Run now')}</button>`}<details class="more-actions"><summary aria-label="${t('More actions')}" title="${t('More actions')}">${DOTS}</summary><div class="more-menu" role="group" aria-label="${t('More actions')}"><button type="button" data-rt-do="edit">${t('Edit')}</button><button type="button" data-rt-do="when">${t('Change when')}</button>${paused?'':html`<button type="button" data-rt-do="pause">${t('Pause')}</button>`}<button type="button" class="danger" data-rt-do="stop">${t('Stop')}</button></div></details></div></article>`}
// What a suggestion from the owner's activity saw (routine_patterns.py), at the end of its rhythm line
const RT_SEEN={ask:'Asked {} times in a row',sent:'Sent {} times in a row',mail:'{} senders every week',slack:'About {} messages a week'};
const rtSeen=w=>w&&RT_SEEN[w.kind]?html` · <span class="rt-seen">${t(RT_SEEN[w.kind],w.n)}</span>`:'';
const rtSuggested=r=>html`<article class="rt rt-s" data-rt="${r.id}"><h3>${r.name}</h3><p class="rt-when">${rtWhen(r)}${rtSeen(r.why)}</p>${r.instructions?html`<p class="rt-what rt-short">${r.instructions}</p>`:''}${rtStepLine(r)}${r.runs[0]?rtBody(r,rtRun(r.runs[0]),0,true):''}
 <div class="actions"><button type="button" class="primary" data-rt-do="accept">${t('Add')}</button><button type="button" class="quiet" data-rt-do="no">${t('No thanks')}</button></div></article>`;
const rtTrying=r=>html`<article class="rt rt-s rt-try" data-rt="${r.id}"><h3>${r.name}</h3><p class="rt-when">${rtWhen(r)}</p>${r.instructions?html`<p class="rt-what">${r.instructions}</p>`:''}${rtStepLine(r)}${r.test?rtBody(r,rtRun(r.test,1),1+rtRows(r.test.result||r.test.why)):''}
 <div class="actions"><button type="button" class="primary" data-rt-do="accept">${t('Add')}</button><button type="button" class="quiet" data-rt-do="change">${t('Change')}</button><button type="button" class="quiet" data-rt-do="no">${t('Cancel')}</button></div></article>`;
const rtSection=(name,label,cards,fine)=>html`<section class="rt-sec rt-${name}" aria-label="${label}"><h2>${label}</h2>${fine?html`<p class="fine">${fine}</p>`:''}${cards}</section>`;
function routinesRender(){const box=$('#routines-view'),list=routinesData?.routines;if(!box||!list)return;const typed=$('#rt-words')?.value||'',sugg=routinesData.suggested||[],trying=routinesData.trying||[],on=list.filter(r=>r.state!=='paused'),off=list.filter(r=>r.state==='paused'),
  fo=document.activeElement,typing=fo?.id==='rt-words'&&[fo.selectionStart,fo.selectionEnd];
 box.innerHTML=html`<form class="rt-new"><textarea id="rt-words" class="rt-grow" rows="1" spellcheck="true" autocapitalize="sentences" placeholder="${t('Every Monday, sum up my deals')}" aria-label="${t('New routine')}"></textarea><button class="primary">${t('Add')}</button></form>
  <p class="fine">${t('Routines only read. They don’t send or change anything.')}</p>${trying.map(rtTrying)}${sugg.length?rtSection('sugg',t('Suggested'),sugg.map(rtSuggested),t(sugg.every(r=>r.from_openclaw)?'From your OpenClaw jobs. Each one ran once to show you.':'Each one ran once to show you.')):''}${
  on.length||!off.length?rtSection('mine',t('Your routines'),on.length?on.map(rtCard):html`<p class="rt-empty">${t('No routines yet')}</p>`):''}${off.length?rtSection('paused',t('Paused'),off.map(rtCard)):''}`.s;
 const w=Object.assign($('#rt-words'),{value:typed});rtGrow(w);if(typing){w.focus({preventScroll:true});w.setSelectionRange(...typing)}
 const card=rtForm&&box.querySelector(`[data-rt="${rtForm.id}"]`);if(card)rtOpen(card,rtForm.kind,rtForm.words,box.contains(fo)&&!!fo.closest('.rt-form')&&(fo.dataset.step||true));else rtForm=null;
 // A run in progress: look again in a few seconds, so its result shows in the card when it is ready
 clearTimeout(rtTimer);if([...list,...sugg,...trying].some(r=>r.runs[0]?.state==='running'||r.test?.state==='running'))rtTimer=setTimeout(()=>box.offsetParent?routinesView(true):routinesAt=0,4000)}
// Grows with its words, up to six lines (routines-page.css)
function rtGrow(x){x.style.height='';x.style.height=x.scrollHeight+x.offsetHeight-x.clientHeight+'px'}
async function routinesView(force){if(!force&&Date.now()-routinesAt<20000&&routinesData){routinesRender();return}
 try{routinesData=await request('api/routines');routinesAt=Date.now();routinesRender()}catch(e){errCaught(e);toast(e.message,true)}}
const rtPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
async function rtDo(action,args,b,done){if(b)b.disabled=true;try{routinesData={...routinesData,...await rtPost(action,args)};routinesAt=Date.now();routinesRender();if(done)toast(done);return true}catch(e){errCaught(e);toast(e.message,true);if(b)b.disabled=false;return false}}
// Edit and Change when: one at a time, under the card's text, with Save and Cancel (Esc, or a click outside on a computer).
// Edit's Try it shows a test run of the new words in the form; Change on a new one tries its new words.
// Script steps: fold open when it has one; what's typed stays across a re-render (rtForm.steps)
const rtStepsFlat=s=>({get:s?.get?.command||'',cwd:s?.get?.cwd||'',timeout:s?.get?.timeout?String(s.get.timeout):'',check:s?.check?.command||''});
const rtField=(k,label,v,hint,more='')=>html`<label class="rt-field${more}">${label}<input data-step="${k}" value="${v}" placeholder="${hint}" autocomplete="off" autocapitalize="off" spellcheck="false"${k==='timeout'?html` inputmode="numeric"`:''}></label>`;
const rtStepsForm=(s,open)=>html`<details class="rt-steps"${open?html` open`:''}><summary>${t('Script steps')}</summary><p class="rt-note">${t('Runs on this Machine. Get data feeds the routine; Check tests the result.')}</p>
 ${rtField('get',t('Get data'),s.get,t('python3 ~/scripts/deals.py'))}<div class="rt-step-row">${rtField('cwd',t('Folder'),s.cwd,'~')}${rtField('timeout',t('Seconds'),s.timeout,'60',' rt-secs')}</div>${rtField('check',t('Check'),s.check,t('python3 ~/scripts/check.py'))}</details>`;
function rtStepsOf(f){const d=f.querySelector('.rt-steps');if(!d)return;const v=k=>d.querySelector(`[data-step="${k}"]`).value.trim(),s={};
 if(v('get'))s.get={command:v('get'),cwd:v('cwd'),...(v('timeout')?{timeout:v('timeout')}:{})};if(v('check'))s.check={command:v('check')};return s}
function rtOpen(card,kind,words,focus=true){const id=card.dataset.rt,r=[...routinesData.routines,...routinesData.trying||[]].find(x=>x.id===id),same=rtForm?.id===id&&rtForm.kind===kind,tried=rtForm?.id===id&&rtForm.tried,busy=r?.test?.state==='running';
 const steps=same&&rtForm.steps||rtStepsFlat(r?.steps),open=same&&rtForm.open!=null?rtForm.open:!!(steps.get||steps.check);
 $('#routines-view .rt-form')?.remove();card.querySelector('.more-actions')?.removeAttribute('open');rtForm={id,kind,words:words??(kind==='when'?'':r?.instructions||''),tried,steps,open};
 card.querySelector('.actions').insertAdjacentHTML('beforebegin',html`<form class="rt-form" data-rt-form="${kind}">${kind==='when'?html`<input autocomplete="off" placeholder="${t('Every weekday at 8')}" aria-label="${t('Change when')}">`:html`<textarea class="rt-grow" rows="1" spellcheck="true" autocapitalize="sentences" aria-label="${t('Edit')}"></textarea>${rtStepsForm(steps,open)}`}${kind==='edit'&&tried&&r.test?rtRun(r.test,1):''}<p class="rt-form-acts">${kind==='change'?html`<button class="primary"${busy?html` disabled`:''}>${t('Try it')}</button>`:html`<button class="primary">${t('Save')}</button>${kind==='edit'?html`<button type="button" class="ghost" data-rt-try${busy?html` disabled`:''}>${t('Try it')}</button>`:''}`}<button type="button" class="quiet" data-rt-cancel>${t('Cancel')}</button></p></form>`.s);
 const x=card.querySelector('.rt-form').elements[0];x.value=rtForm.words;if(kind!=='when')rtGrow(x);if(focus){const y=card.querySelector(`.rt-form [data-step="${focus}"]`)||x;y.focus({preventScroll:true});y.setSelectionRange?.(y.value.length,y.value.length)}}
function rtShut(back){const f=$('#routines-view .rt-form');rtForm=null;if(!f)return;const s=f.closest('[data-rt]')?.querySelector('.more-actions>summary');f.remove();if(back)s?.focus({preventScroll:true})}
document.addEventListener('pointerdown',e=>{const f=$('#routines-view .rt-form');if(f&&!f.contains(e.target)&&matchMedia('(pointer:fine)').matches&&!e.target.closest?.('[data-rt-do="edit"],[data-rt-do="when"],[data-rt-do="change"]'))rtShut()});
$('#routines-view').addEventListener('submit',e=>{e.preventDefault();const f=e.target,input=f.elements[0],words=input.value.trim(),b=f.querySelector('.primary'),steps=rtStepsOf(f);if(!words&&!steps?.get)return;
 if(input.id==='rt-words'){rtDo('routine_try',{words},b).then(ok=>{if(ok)rtGrow(Object.assign($('#rt-words'),{value:''}))});return}
 const id=f.closest('[data-rt]').dataset.rt,kind=f.dataset.rtForm;rtDo(kind==='change'?'routine_try':kind==='edit'?'routine_edit':'routine_when',{id,words,...(steps?{steps}:{})},b).then(ok=>{if(ok)rtShut()})});
// As the chat box: Enter adds or saves, Shift+Enter or a phone's Enter is a new line
$('#routines-view').addEventListener('input',e=>{if(e.target.matches('.rt-grow'))rtGrow(e.target);if(rtForm&&e.target.closest('.rt-form')){const k=e.target.dataset.step;if(k)rtForm.steps[k]=e.target.value;else rtForm.words=e.target.value}});
$('#routines-view').addEventListener('keydown',e=>{const x=e.target,f=x.form;if(!f)return;if(e.key==='Escape'&&f.matches('.rt-form')){e.preventDefault();e.stopPropagation();rtShut(true);return}
 if(x.tagName!=='TEXTAREA'||e.key!=='Enter'||e.isComposing||e.keyCode===229||e.altKey)return;
 if(!(e.ctrlKey||e.metaKey)&&(e.shiftKey||matchMedia('(pointer: coarse)').matches))return;e.preventDefault();e.stopPropagation();f.requestSubmit()});
$('#routines-view').addEventListener('click',e=>{if(e.target.closest('[data-rt-cancel]')){rtShut(true);return}
 const tr=e.target.closest('[data-rt-try]');if(tr){const words=tr.form.elements[0].value.trim(),steps=rtStepsOf(tr.form);if(words||steps?.get){rtForm.tried=true;rtDo('routine_try',{id:rtForm.id,words,steps},tr)}return}
 const sum=e.target.closest('.rt-steps>summary');if(sum&&rtForm){rtForm.open=!sum.parentElement.open;return}
 const m=e.target.closest('[data-more]');if(m){const key=m.dataset.more,open=!expandedBodies.has(key);open?expandedBodies.add(key):expandedBodies.delete(key);m.previousElementSibling.classList.toggle('clamp',!open);m.setAttribute('aria-expanded',open);m.textContent=t(open?'Show less':'Show more');return}
 const old=e.target.closest('[data-rt-old]');if(old){const choice=old.dataset.rtOld;rtDo('routine_old_job',{id:old.closest('[data-rt]').dataset.rt,choice},old,choice==='off'?t('Old job turned off'):'');return}
 const b=e.target.closest('[data-rt-do]');if(!b)return;const card=b.closest('[data-rt]'),id=card.dataset.rt,what=b.dataset.rtDo;
 if(what==='accept')rtDo('routine_accept',{id},b,t('Routine added'));
 else if(what==='no')rtDo('routine_state',{id,to:'stop'},b);
 else if(what==='now')rtDo('routine_run_now',{id},b,t('Running it now'));
 else if(what==='edit'||what==='when'||what==='change')rtOpen(card,what);
 else if(what==='stop'&&!b.dataset.sure){e.stopPropagation();b.dataset.sure='1';b.textContent=t('Stop for good?');setTimeout(()=>{if(b.isConnected){delete b.dataset.sure;b.textContent=t('Stop')}},4000)}
 else rtDo('routine_state',{id,to:what},b,what==='stop'?t('Routine stopped'):'')});
