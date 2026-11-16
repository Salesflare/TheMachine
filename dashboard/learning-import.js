// A lazy part (dashboard_parts.LAZY 'memimport'): Import from another AI (memory_import.py). Opened through
// memoryImportOpen() (setup-card.js) from the setup to-do's row, the first look's quiet button and Learning.
// Two steps in one dialog: pick ChatGPT, Claude or Gemini, Copy prompt, paste its answer, Review; then the lines to
// keep, each ticked and editable, a contradiction next to the current fact (the current one picked until the owner
// picks the new one), and what was left out (already known, secrets, permissions). Import keeps what is ticked. The
// paste never leaves the dialog but for the review; nothing is saved before Import.
const MI_AREAS={about:'About you',preferences:'Preferences',people:'People',work:'Work',routines:'Routines'};
let mi={from:'chatgpt',prompt:'',text:'',review:null,ticked:new Set(),edits:{},pick:{},busy:false,error:''};
function miDialog(){let d=$('#memory-import');if(d)return d;
 d=document.createElement('dialog');d.id='memory-import';d.setAttribute('aria-labelledby','memory-import-title');document.body.append(d);
 d.addEventListener('click',miClick);d.addEventListener('input',miInput);d.addEventListener('change',miChange);
 d.addEventListener('close',()=>{mi.review=null;mi.error=''});return d}
const miPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
const miHead=title=>html`<div class="snooze-heading"><h2 id="memory-import-title">${title}</h2><button type="button" data-mi-close aria-label="${t('Close')}">×</button></div>`;
function miPaste(){const name=AI_NAMES[mi.from];
 return html`${miHead(t('Import from another AI'))}<p class="mi-fine">${t('Bring in what another assistant knows about you. You pick what stays.')}</p>
<div class="mi-from" role="radiogroup" aria-label="${t('Import from')}">${Object.entries(AI_NAMES).map(([k,n])=>html`<label class="mi-pill"><input type="radio" name="mi-from" value="${k}"${k===mi.from?html` checked`:''}><span>${n}</span></label>`)}</div>
<ol class="mi-steps"><li><span class="mi-step">${t('Copy this prompt and send it in {}.',name)}</span><pre class="mi-prompt" tabindex="0">${mi.prompt}</pre><button type="button" class="mi-copy" data-mi-copy${mi.prompt?'':html` disabled`}>${t('Copy prompt')}</button></li>
<li><label class="mi-step" for="mi-text">${t('Paste its answer here.')}</label><textarea id="mi-text" rows="6" maxlength="40000" placeholder="${t('Paste the answer from {}',name)}">${mi.text}</textarea></li></ol>
${mi.error?html`<p class="mi-error error" role="alert">${mi.error}</p>`:''}<div class="actions"><button type="button" class="ghost" data-mi-close>${t('Cancel')}</button><button type="button" class="primary" data-mi-review${mi.busy||!mi.text.trim()?html` disabled`:''}>${mi.busy?t('Reviewing…'):t('Review')}</button></div>`}
function miRow(i){const on=mi.ticked.has(i.n),text=mi.edits[i.n]??i.text,area=MI_AREAS[i.area]?t(MI_AREAS[i.area]):'';
 if(i.conflict){const p=mi.pick[i.n]||'keep';
  return html`<li class="mi-row mi-conflict"><span class="mi-label">${t('These disagree. Pick one.')}</span><div class="mi-sides" role="radiogroup" aria-label="${t('Pick one')}">
<label class="mi-side${p==='keep'?' on':''}"><input type="radio" name="mi-pick-${i.n}" value="keep" data-mi-pick="${i.n}"${p==='keep'?html` checked`:''}><span><small>${t('Now')}</small>${i.conflict.text}</span></label>
<label class="mi-side${p==='new'?' on':''}"><input type="radio" name="mi-pick-${i.n}" value="new" data-mi-pick="${i.n}"${p==='new'?html` checked`:''}><span><small>${t('From {}',AI_NAMES[mi.review.from])}</small>${text}</span></label></div></li>`}
 return html`<li class="mi-row${on?'':' off'}"><input type="checkbox" data-mi-tick="${i.n}"${on?html` checked`:''} aria-label="${t('Keep: {}',text)}"><span class="mi-line"><textarea class="mi-text" data-mi-edit="${i.n}" maxlength="240" rows="1" aria-label="${t('Edit: {}',i.text)}">${text}</textarea>${area?html`<small>${area}</small>`:''}</span></li>`}
function miPicked(){const r=mi.review;if(!r)return 0;return r.items.filter(i=>i.conflict?mi.pick[i.n]==='new':mi.ticked.has(i.n)).length}
function miReviewHTML(){const r=mi.review,left=[];
 if(r.known)left.push(t(['{} you already told me','{} you already told me'],r.known));
 if(r.secrets)left.push(t(['{} looked like a password or number','{} looked like passwords or numbers'],r.secrets));
 if(r.permissions)left.push(t(['{} tried to grant a permission','{} tried to grant permissions'],r.permissions));
 const n=miPicked();
 return html`${miHead(t('Review what to import'))}<p class="mi-fine">${t('Imported lines are context, never permission. Edit one to make it your own.')}</p>
${left.length?html`<p class="mi-left"><strong>${t('Left out')}</strong> ${left.join(' · ')}</p>`:''}${r.more?html`<p class="mi-left">${t('Only the first {} lines are shown.',r.items.length)}</p>`:''}
${r.items.length?html`<ul class="mi-list">${r.items.map(miRow)}</ul>`:html`<p class="mi-empty">${t('Nothing new to import.')}</p>`}
${mi.error?html`<p class="mi-error error" role="alert">${mi.error}</p>`:''}<div class="actions"><button type="button" class="ghost" data-mi-back>${t('Back')}</button><button type="button" class="primary" data-mi-save${mi.busy||!n?html` disabled`:''}>${mi.busy?t('Importing…'):n?t(['Import {} line','Import {} lines'],n):t('Import')}</button></div>`}
// A review line's box is as tall as its text, so a long line reads whole on a phone
const miFit=el=>{el.style.height='auto';el.style.height=el.scrollHeight+2+'px'};
function miDraw(){const d=miDialog(),focus=document.activeElement?.closest?.('#memory-import')?document.activeElement:null,key=focus&&(focus.dataset.miEdit||focus.id),pos=focus?.selectionStart;
 setHTML(d,mi.review?miReviewHTML():miPaste());for(const x of d.querySelectorAll('.mi-text'))miFit(x);
 if(key){const el=d.querySelector(`[data-mi-edit="${CSS.escape(key)}"]`)||d.querySelector('#'+CSS.escape(key));if(el){el.focus();if(pos!=null&&el.setSelectionRange)el.setSelectionRange(pos,pos)}}}
async function memoryImportShow(){const d=miDialog();mi.review=null;mi.error='';mi.busy=false;miDraw();if(!d.open)d.showModal();
 if(!mi.prompt)try{const r=await miPost('memory_import_prompt',{});mi.prompt=String(r.prompt||'');miDraw()}catch(e){errCaught(e);mi.error=e.message;miDraw()}
 d.querySelector('#mi-text')?.focus()}
function miInput(e){const el=e.target;
 if(el.id==='mi-text'){mi.text=el.value;const b=$('#memory-import [data-mi-review]');if(b)b.disabled=mi.busy||!mi.text.trim();return}
 if(el.dataset.miEdit){mi.edits[el.dataset.miEdit]=el.value;miFit(el);const i=mi.review?.items.find(x=>String(x.n)===el.dataset.miEdit);if(i&&!i.conflict&&!mi.ticked.has(i.n)&&el.value.trim()){mi.ticked.add(i.n);const box=el.closest('.mi-row')?.querySelector('[data-mi-tick]');if(box)box.checked=true;el.closest('.mi-row')?.classList.remove('off')}miCount()}}
function miCount(){const b=$('#memory-import [data-mi-save]'),n=miPicked();if(b&&!mi.busy){b.disabled=!n;b.textContent=n?t(['Import {} line','Import {} lines'],n):t('Import')}}
function miChange(e){const el=e.target;
 if(el.name==='mi-from'){mi.from=el.value;miDraw();return}
 if(el.dataset.miTick){const n=Number(el.dataset.miTick);el.checked?mi.ticked.add(n):mi.ticked.delete(n);el.closest('.mi-row')?.classList.toggle('off',!el.checked);miCount();return}
 if(el.dataset.miPick){mi.pick[el.dataset.miPick]=el.value;for(const s of el.closest('.mi-sides').querySelectorAll('.mi-side'))s.classList.toggle('on',s.contains(el)&&el.checked);miCount()}}
async function miClick(e){const b=e.target.closest('button');if(!b)return;const d=miDialog();
 if(b.matches('[data-mi-close]')){d.close();return}
 if(b.matches('[data-mi-copy]')){try{await navigator.clipboard.writeText(mi.prompt);toast(t('Copied. Paste it in {}.',AI_NAMES[mi.from]))}catch(err){errCaught(err);toast(t('Couldn’t copy automatically. Select the prompt and copy it.'),true)}return}
 if(b.matches('[data-mi-back]')){mi.review=null;mi.error='';miDraw();return}
 if(b.matches('[data-mi-review]')){mi.busy=true;mi.error='';miDraw();
  try{const r=await miPost('memory_import_review',{from:mi.from,text:mi.text});mi.review=r;mi.ticked=new Set(r.items.filter(i=>!i.conflict).map(i=>i.n));mi.edits={};mi.pick={}}
  catch(err){errCaught(err);mi.error=err.message}
  mi.busy=false;miDraw();d.querySelector('[data-mi-tick],[data-mi-pick]')?.focus();return}
 if(b.matches('[data-mi-save]')){const r=mi.review;if(!r)return;
  const picks=r.items.filter(i=>i.conflict?mi.pick[i.n]==='new':mi.ticked.has(i.n)).map(i=>({n:i.n,text:String(mi.edits[i.n]??i.text).replace(/\s+/g,' ').trim(),kind:i.kind,...(i.conflict?{replace:true}:{})}));
  if(!picks.length)return;mi.busy=true;mi.error='';miDraw();
  try{const done=await miPost('memory_import_save',{from:r.from,token:r.token,picks});mi.busy=false;mi.text='';d.close();
   toast(done.saved?t(['Imported {} line. It’s in Learning.','Imported {} lines. They’re in Learning.'],done.saved):t('Nothing new to import.'));refresh()}
  catch(err){errCaught(err);mi.busy=false;mi.error=err.message;miDraw()}}}
