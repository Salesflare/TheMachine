// Routines (routines.py): work The Machine does on its own, on a rhythm; it only reads. Not a recurring to-do.
// Suggested: old OpenClaw jobs that fit, or patterns in what the owner does (routine_patterns.py, with
// why: what was seen, on the rhythm line), each with the result of one real run; Add or No thanks.
// A new one shows a test run first (routine_try, dry: nothing sent or kept): Add, Change or Cancel. Edit's Try it, too.
// Advanced (the card's ...): script steps. Get data's output goes to the run; Check gets the result.
let routinesData=null,routinesAt=0,rtForm=null,rtTimer=0,rtStale=false,rtMissed=0;
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
  <div class="actions">${paused?html`<button type="button" class="ghost" data-rt-do="resume">${t('Resume')}</button>`:html`<button type="button" class="ghost" data-rt-do="now"${last?.state==='running'?html` disabled`:''}>${t('Run now')}</button>`}<details class="more-actions"><summary aria-label="${t('More actions')}" title="${t('More actions')}">${DOTS}</summary><div class="more-menu" role="group" aria-label="${t('More actions')}"><button type="button" data-rt-do="edit">${t('Edit')}</button><button type="button" data-rt-do="when">${t('Change when')}</button>${paused?'':html`<button type="button" data-rt-do="pause">${t('Pause')}</button>`}<button type="button" data-rt-do="steps">${t('Advanced: script steps')}</button><button type="button" class="danger" data-rt-do="stop">${t('Stop')}</button></div></details></div></article>`}
// What a suggestion from the owner's activity saw (routine_patterns.py), at the end of its rhythm line
const RT_SEEN={ask:['Asked {} times in a row'],sent:['Sent {} times in a row'],mail:['{} senders every week'],slack:['About {} messages a week'],
 forward:['Forwarded {} mails to {} in {} weeks','n','to','weeks'],reply:['Answered the same request from {} {} times in a row','to','n']};
const rtSeen=w=>{const [k,...a]=w&&RT_SEEN[w.kind]||[];return k?html` · <span class="rt-seen">${t(k,...(a[0]?a:['n']).map(x=>w[x]))}</span>`:''};
const rtSuggested=r=>html`<article class="rt rt-s" data-rt="${r.id}"><h3>${r.name}</h3><p class="rt-when">${rtWhen(r)}${rtSeen(r.why)}</p>${r.instructions?html`<p class="rt-what rt-short">${r.instructions}</p>`:''}${rtStepLine(r)}${r.runs[0]?rtBody(r,rtRun(r.runs[0]),0,true):''}
 <div class="actions"><button type="button" class="primary" data-rt-do="accept">${t('Add')}</button><button type="button" class="quiet" data-rt-do="no">${t('No thanks')}</button></div></article>`;
const rtTrying=r=>html`<article class="rt rt-s rt-try" data-rt="${r.id}"><h3>${r.name}</h3><p class="rt-when">${rtWhen(r)}</p>${r.instructions?html`<p class="rt-what">${r.instructions}</p>`:''}${rtStepLine(r)}${r.test?rtBody(r,rtRun(r.test,1),1+rtRows(r.test.result||r.test.why)):''}
 <div class="actions"><button type="button" class="primary" data-rt-do="accept">${t('Add')}</button><button type="button" class="quiet" data-rt-do="change">${t('Change')}</button><button type="button" class="quiet" data-rt-do="no">${t('Cancel')}</button></div></article>`;
// Templates (routine_templates.py): ready-made routines, one tap to add; an added one leaves the list
const rtTemplate=x=>html`<article class="rt rt-tpl"><div><h3>${x.name}</h3><p class="rt-what">${x.what}</p></div><button type="button" class="ghost" data-rt-tpl="${x.key}">${t('Add')}</button></article>`;
const rtSection=(name,label,cards,fine)=>html`<section class="rt-sec rt-${name}" aria-label="${label}"><h2>${label}</h2>${fine?html`<p class="fine">${fine}</p>`:''}${cards}</section>`;
// A refresh while Edit, Change or Change when is open only patches that card's test run (rtPatch): the page is rebuilt
// when the form closes. A rebuild keeps what is on screen in place (rtKeep).
function routinesRender(){const box=$('#routines-view'),list=routinesData?.routines;if(!box||!list)return;
 if(!(rtForm&&rtPatch(box)))rtKeep(box,()=>rtFull(box,list));
 rtReveal(box);rtLook(4000)}
// A routine's link opened (rtWant, openRoutineLink in shell-page-head.js): that routine in view, marked for a moment. One
// gone since says so.
function rtReveal(box){if(!rtWant)return;const a=box.querySelector(`article[data-rt="${CSS.escape(rtWant)}"]`);rtWant='';if(!a){toast(t('That routine is gone'),true);return}
 a.tabIndex=-1;a.scrollIntoView({block:'center'});a.focus({preventScroll:true});a.classList.add('rt-found');setTimeout(()=>a.classList.remove('rt-found'),2400)}
// A run in progress: look again in a few seconds (slower after a failed look), so its result shows in the card when ready
function rtLook(ms){const d=routinesData;clearTimeout(rtTimer);if([...d.routines,...d.suggested||[],...d.trying||[]].some(r=>r.runs[0]?.state==='running'||r.test?.state==='running'))rtTimer=setTimeout(()=>$('#routines-view')?.offsetParent?routinesView(true):routinesAt=0,ms)}
function rtFull(box,list){rtStale=false;const typed=$('#rt-words')?.value||'',sugg=routinesData.suggested||[],trying=routinesData.trying||[],on=list.filter(r=>r.state!=='paused'),off=list.filter(r=>r.state==='paused'),tpl=(routinesData.templates||[]).filter(x=>!x.added),
  fo=document.activeElement,typing=fo?.id==='rt-words'&&[fo.selectionStart,fo.selectionEnd];
 setHTML(box,html`<form class="rt-new"><textarea id="rt-words" class="rt-grow" rows="1" spellcheck="true" autocapitalize="sentences" placeholder="${t('Every Monday, sum up my deals')}" aria-label="${t('New routine')}"></textarea><button class="primary">${t('Add')}</button></form>
  <p class="fine">${t('Routines only read. Any change waits for your OK on a to-do.')}</p>${trying.map(rtTrying)}${sugg.length?rtSection('sugg',t('Suggested'),sugg.map(rtSuggested),t(sugg.every(r=>r.from_openclaw)?'From your OpenClaw jobs. Each one ran once to show you.':'Each one ran once to show you.')):''}${
  on.length||!off.length?rtSection('mine',t('Your routines'),on.length?on.map(rtCard):html`<p class="rt-empty">${t('No routines yet')}</p>`):''}${off.length?rtSection('paused',t('Paused'),off.map(rtCard)):''}${tpl.length?rtSection('templates',t('Templates'),tpl.map(rtTemplate)):''}`);
 const w=Object.assign($('#rt-words'),{value:typed});rtGrow(w);if(typing){w.focus({preventScroll:true});w.setSelectionRange(...typing)}
 const card=rtForm&&box.querySelector(`[data-rt="${rtForm.id}"]`);if(card)rtOpen(card,rtForm.kind,rtForm.words,box.contains(fo)&&!!fo.closest('.rt-form')&&(fo.dataset.step||true));else rtForm=null}
// The open form's card, in place: its test run and Try it; false when the cards themselves changed (a rebuild then)
function rtPatch(box){const all=[...routinesData.routines,...routinesData.suggested||[],...routinesData.trying||[]],r=all.find(x=>x.id===rtForm.id),
  card=box.querySelector(`[data-rt="${rtForm.id}"]`),f=card?.querySelector('.rt-form');
 if(!r||!f||[...box.querySelectorAll('article[data-rt]')].map(a=>a.dataset.rt).sort().join()!==all.map(x=>x.id).sort().join())return false;
 if(r.state==='trying'){const b=card.querySelector('.rt-body');if(b&&r.test)setHTML(b,rtRun(r.test,1))}
 else if(rtForm.kind==='edit'&&rtForm.tried&&r.test){const old=f.querySelector('.rt-run'),h=document.createElement('template');setHTML(h,rtRun(r.test,1));if(old)old.replaceWith(h.content);else f.querySelector('.rt-form-acts').before(h.content)}
 for(const b of f.querySelectorAll('[data-rt-try]'+(rtForm.kind==='change'?',.primary':'')))b.disabled=r.test?.state==='running';
 rtStale=true;return true}
// The card being edited (else the first one on screen) stays where it was on screen; the page never shrinks meanwhile
function rtKeep(box,rebuild){const cards=[...box.querySelectorAll('article[data-rt]')],at=(rtForm&&cards.find(a=>a.dataset.rt===rtForm.id&&a.getBoundingClientRect().bottom>0))||cards.find(a=>a.getBoundingClientRect().bottom>0),
  id=at?.dataset.rt,top=at?.getBoundingClientRect().top;
 box.style.minHeight=box.offsetHeight+'px';try{rebuild()}finally{box.style.minHeight=''}
 const now=id&&box.querySelector(`[data-rt="${id}"]`),d=now?now.getBoundingClientRect().top-top:0;if(d)(rtScroller(box)||window).scrollBy(0,d)}
function rtScroller(box){for(let e=box.parentElement;e&&e!==document.body;e=e.parentElement){const o=getComputedStyle(e).overflowY;if((o==='auto'||o==='scroll')&&e.scrollHeight>e.clientHeight)return e}return null}
// Grows with its words, up to six lines (routines-page.css). It scrolls only once it is at its tallest: a height a fraction
// of a pixel short of its text (150% display scaling) showed a classic scrollbar (Windows) in an empty field.
function rtGrow(x){const p=x.parentElement;p.style.minHeight=p.offsetHeight+'px';x.style.height='';x.style.overflowY='';const want=x.scrollHeight+x.offsetHeight-x.clientHeight;
 x.style.height=want+'px';if(want>parseFloat(getComputedStyle(x).maxHeight)+1)x.style.overflowY='auto';p.style.minHeight=''}
async function routinesLoad(force){if(!force&&Date.now()-routinesAt<20000&&routinesData){routinesRender();return}
 try{routinesData=await request('api/routines');routinesAt=Date.now();rtMissed=0;routinesRender()}
 catch(e){errCaught(e);if(force&&routinesData)rtLook(Math.min(3e4,4e3*2**++rtMissed));else toast(e.message,true)}}
const rtPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
async function rtDo(action,args,b,done){if(b)b.disabled=true;try{routinesData={...routinesData,...await rtPost(action,args)};routinesAt=Date.now();routinesRender();if(done)toast(done);return true}catch(e){errCaught(e);toast(e.message,true);if(b)b.disabled=false;return false}}
// Edit and Change when: one at a time, under the card's text, with Save and Cancel (Esc, or a click outside on a computer).
// Edit's Try it shows a test run of the new words in the form; Change on a new one tries its new words.
// Script steps: shown when set or opened from Advanced (rtForm.open), no placeholders; typed text stays (rtForm.steps)
const rtStepsFlat=s=>({get:s?.get?.command||'',cwd:s?.get?.cwd||'',timeout:s?.get?.timeout?String(s.get.timeout):'',check:s?.check?.command||''});
const rtField=(k,label,v,more='')=>html`<label class="rt-field${more}">${label}<input data-step="${k}" value="${v}" autocomplete="off" autocapitalize="off" spellcheck="false"${k==='timeout'?html` inputmode="numeric"`:''}></label>`;
// The Machine's own recipe (routine_recipe.py), read-only
const rtRecipe=l=>l?.length?html`<p class="rt-note">${t('Your Machine wrote these reads itself. It runs them before each run; they only read.')}</p><ul class="rt-recipe">${l.map(x=>html`<li><code>${x}</code>`)}</ul>`:'';
const rtStepsForm=(s,recipe)=>html`<fieldset class="rt-steps"><legend>${t('Advanced: script steps')}</legend><p class="rt-note">${t('Runs on this Machine. Get data feeds the routine; Check tests the result.')}</p>
 ${rtField('get',t('Get data'),s.get)}<div class="rt-step-row">${rtField('cwd',t('Folder'),s.cwd)}${rtField('timeout',t('Seconds'),s.timeout,' rt-secs')}</div>${rtField('check',t('Check'),s.check)}${rtRecipe(recipe)}</fieldset>`;
function rtStepsOf(f){const d=f.querySelector('.rt-steps');if(!d)return;const v=k=>d.querySelector(`[data-step="${k}"]`).value.trim(),s={};
 if(v('get'))s.get={command:v('get'),cwd:v('cwd'),...(v('timeout')?{timeout:v('timeout')}:{})};if(v('check'))s.check={command:v('check')};return s}
// Edit's name (rtForm.name) sits in the title's place (routines-page.css), Change's too on a new one; the words are the form's own field.
// A template's routine (routine_templates.py) edits like any; once its words changed, Back to the template puts them back
const rtWordsIn=f=>[...f.elements].find(x=>x.matches('textarea,input:not(.rt-name):not([data-step])'));
function rtOpen(card,kind,words,focus=true){const adv=kind==='steps';if(adv){kind='edit';focus='get'}const id=card.dataset.rt,r=[...routinesData.routines,...routinesData.trying||[]].find(x=>x.id===id),same=rtForm?.id===id&&rtForm.kind===kind,tried=rtForm?.id===id&&rtForm.tried,busy=r?.test?.state==='running';
 const steps=same&&rtForm.steps||rtStepsFlat(r?.steps),open=adv||(same?rtForm.open:!!(steps.get||steps.check));
 $('#routines-view .rt-form')?.remove();card.querySelector('.more-actions')?.removeAttribute('open');rtForm={id,kind,words:words??(kind==='when'?'':r?.instructions||''),name:same&&rtForm.name!=null?rtForm.name:r?.name||'',tried,steps,open};
 card.querySelector('.actions').insertAdjacentHTML('beforebegin',html`<form class="rt-form" data-rt-form="${kind}">${kind==='when'?html`<input autocomplete="off" placeholder="${t('Every weekday at 8')}" aria-label="${t('Change when')}">`:html`${kind!=='when'?html`<input class="rt-name" maxlength="80" autocomplete="off" spellcheck="true" autocapitalize="sentences" aria-label="${t('Name')}">`:''}<textarea class="rt-grow" rows="1" spellcheck="true" autocapitalize="sentences" aria-label="${t('Edit')}"></textarea>${open?rtStepsForm(steps,r?.recipe):''}`}${kind==='edit'&&tried&&r.test?rtRun(r.test,1):''}<p class="rt-form-acts">${kind==='change'?html`<button class="primary"${busy?html` disabled`:''}>${t('Try it')}</button>`:html`<button class="primary">${t('Save')}</button>${kind==='edit'?html`<button type="button" class="ghost" data-rt-try${busy?html` disabled`:''}>${t('Try it')}</button>`:''}`}<button type="button" class="quiet" data-rt-cancel>${t('Cancel')}</button>${kind==='edit'&&r?.edited?html`<button type="button" class="quiet rt-back" data-rt-back>${t('Back to the template')}</button>`:''}</p></form>`.s);
 const fm=card.querySelector('.rt-form'),x=rtWordsIn(fm),nm=fm.querySelector('.rt-name');x.value=rtForm.words;if(nm)nm.value=rtForm.name;if(kind!=='when')rtGrow(x);if(focus){const y=card.querySelector(`.rt-form [data-step="${focus}"]`)||x;y.focus({preventScroll:true});y.setSelectionRange?.(y.value.length,y.value.length)}}
function rtShut(back){const f=$('#routines-view .rt-form');rtForm=null;if(!f)return;const id=f.closest('[data-rt]')?.dataset.rt;f.remove();if(rtStale)routinesRender();
 if(back)$(`#routines-view [data-rt="${id}"] .more-actions>summary`)?.focus({preventScroll:true})}
document.addEventListener('pointerdown',e=>{const f=$('#routines-view .rt-form');if(f&&!f.contains(e.target)&&matchMedia('(pointer:fine)').matches&&!e.target.closest?.('[data-rt-do="edit"],[data-rt-do="when"],[data-rt-do="change"],[data-rt-do="steps"]'))rtShut()});
$('#routines-view').addEventListener('submit',e=>{e.preventDefault();const f=e.target,input=rtWordsIn(f),words=input.value.trim(),b=f.querySelector('.primary'),steps=rtStepsOf(f);if(!words&&!steps?.get)return;
 if(input.id==='rt-words'){rtDo('routine_try',{words},b).then(ok=>{if(ok)rtGrow(Object.assign($('#rt-words'),{value:''}))});return}
 const id=f.closest('[data-rt]').dataset.rt,kind=f.dataset.rtForm,nm=f.querySelector('.rt-name'),name=nm?.value.trim(),was=[...routinesData.routines,...routinesData.trying||[]].find(r=>r.id===id)?.name;
 rtDo(kind==='change'?'routine_try':kind==='edit'?'routine_edit':'routine_when',{id,words,...(steps?{steps}:{}),...(nm&&name!==was?{name}:{})},b).then(ok=>{if(ok)rtShut()})});
// As the chat box: Enter adds or saves, Shift+Enter or a phone's Enter is a new line
$('#routines-view').addEventListener('input',e=>{if(e.target.matches('.rt-grow'))rtGrow(e.target);if(rtForm&&e.target.closest('.rt-form')){const k=e.target.dataset.step;if(k)rtForm.steps[k]=e.target.value;else if(e.target.matches('.rt-name'))rtForm.name=e.target.value;else rtForm.words=e.target.value}});
$('#routines-view').addEventListener('keydown',e=>{const x=e.target,f=x.form;if(!f)return;if(e.key==='Escape'&&f.matches('.rt-form')){e.preventDefault();e.stopPropagation();rtShut(true);return}
 if(x.tagName!=='TEXTAREA'||e.key!=='Enter'||e.isComposing||e.keyCode===229||e.altKey)return;
 if(!(e.ctrlKey||e.metaKey)&&(e.shiftKey||matchMedia('(pointer: coarse)').matches))return;e.preventDefault();e.stopPropagation();f.requestSubmit()});
$('#routines-view').addEventListener('click',e=>{if(e.target.closest('[data-rt-cancel]')){rtShut(true);return}
 const bk=e.target.closest('[data-rt-back]');if(bk){rtDo('routine_edit',{id:rtForm.id,back:true},bk).then(ok=>{if(ok)rtShut()});return}
 const tr=e.target.closest('[data-rt-try]');if(tr){const words=rtWordsIn(tr.form).value.trim(),steps=rtStepsOf(tr.form);if(words||steps?.get){rtForm.tried=true;rtDo('routine_try',{id:rtForm.id,words,steps},tr)}return}
 const m=e.target.closest('[data-more]');if(m){const key=m.dataset.more,open=!expandedBodies.has(key);open?expandedBodies.add(key):expandedBodies.delete(key);m.previousElementSibling.classList.toggle('clamp',!open);m.setAttribute('aria-expanded',open);m.textContent=t(open?'Show less':'Show more');return}
 const tp=e.target.closest('[data-rt-tpl]');if(tp){rtDo('routine_template',{key:tp.dataset.rtTpl},tp,t('Routine added'));return}
 const old=e.target.closest('[data-rt-old]');if(old){const choice=old.dataset.rtOld;rtDo('routine_old_job',{id:old.closest('[data-rt]').dataset.rt,choice},old,choice==='off'?t('Old job turned off'):'');return}
 const b=e.target.closest('[data-rt-do]');if(!b)return;const card=b.closest('[data-rt]'),id=card.dataset.rt,what=b.dataset.rtDo;
 if(what==='accept')rtDo('routine_accept',{id},b,t('Routine added'));
 else if(what==='no')rtDo('routine_state',{id,to:'stop'},b);
 else if(what==='now')rtDo('routine_run_now',{id},b,t('Running it now'));
 else if(what==='edit'||what==='when'||what==='change'||what==='steps')rtOpen(card,what);
 else if(what==='stop'&&!b.dataset.sure){e.stopPropagation();b.dataset.sure='1';b.textContent=t('Stop for good?');setTimeout(()=>{if(b.isConnected){delete b.dataset.sure;b.textContent=t('Stop')}},4000)}
 else rtDo('routine_state',{id,to:what},b,what==='stop'?t('Routine stopped'):'')});
