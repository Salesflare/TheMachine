// A board's follow-ups as one to-do, its fast review: one follow-up at a time or the whole list, Send, Edit or Skip
// each, keys to move, Send all checked. A part that loads when first needed (dashboard_parts.LAZY 'followups'):
// graph-followups.js opens it through lazyRun('followups'); fr, frDraft and frName are there.
// A draft the review's Change is rewriting stays in the list while its to-do is back at work, and so does one that
// couldn't be changed (its "try again" is here)
const frList=()=>state.suggestions.filter(s=>s.follow_up?.group===fr.g&&s.follow_up.state==='open'&&!fr.gone.has(s.id)&&!fuBusy(s)
 &&(s.status==='prepared'||(fr.changing.has(s.id)||fr.failed.has(s.id))&&['instructions','accepted'].includes(s.status)))
 .sort((a,b)=>fr.skipped.has(a.id)-fr.skipped.has(b.id));  // skipped ones wait at the bottom until the review closes
// Every draft shows in full and the list is the only thing that scrolls; moving (j/k, a click) changes the current one
// in place and scrolls it into view smoothly, a poll redraws only the drafts that changed and keeps where the list is
const frPhase=s=>fr.skipped.has(s.id)?'skip':fr.changing.has(s.id)?'run':fr.failed.has(s.id)?'fail':fr.undo.has(s.id)?'done':'';
const frItemSig=s=>s.id+':'+(frDraft(s)?.revision||'')+':'+s.status+':'+frPhase(s)+':'+(s.action_status?.error||'')+':'+(s.follow_up?.advice||'');
const frSig=list=>list.map(s=>s.id).join();
const frReady=s=>s.status==='prepared'&&!fr.changing.has(s.id)&&!fr.skipped.has(s.id);
// Held right before it went because the thread got a new message (follow_ups.HELD): left out of Send all checked until the
// owner ticks it again, and its Send is a plain one. "Couldn’t check the thread" stays checked: trying again is the point.
const frStale=s=>s.action_status?.status==='blocked'&&s.action_status.error==='Not sent: new message in the thread.';
// The Machine would stop here (follow_ups.advise): the draft is there, unchecked, and the owner decides
const frAdvised=s=>!!s.follow_up?.advice;
function frOpen(g){fr={g,at:0,cur:null,checked:null,editing:null,gone:new Set(),sent:0,busy:false,box:null,changing:new Map(),failed:new Map(),undo:new Map(),shown:new Map(),skipped:new Map()};
 const list=frList();fr.checked=new Set(list.filter(s=>!frStale(s)&&!frAdvised(s)).map(s=>s.id));fr.seen=new Set(list.map(s=>s.id));
 const d=$('#fu-review');d.replaceChildren();frDraw();const ol=d.querySelector('.fr-list');if(!ol)return;if(!d.open)d.showModal();ol.scrollTop=0;d.querySelector('.fr-item.on')?.focus({preventScroll:true})}
// A draft's text exactly as it goes out: every line and every blank line (the one between "Regards," and the name
// too), only blank lines at its very start and end left out
const frBody=text=>String(text).replace(/^(?:[ \t]*\n)+|\s+$/g,'');
function frState(s){const ph=frPhase(s);
 if(ph==='skip')return html`<p class="fr-state skip">${t('Skipped')}<button type="button" class="link" data-fr-unskip="${s.id}">${t('Undo')}</button></p>`;
 if(ph==='run')return html`<p class="fr-state run" role="status"><i class="fr-spin" aria-hidden="true"></i>${t('Rewriting…')}</p>`;
 if(ph==='fail')return html`<p class="fr-state fail" role="status">${t('Couldn’t change this one, try again')}<button type="button" class="link" data-fr-retry="${s.id}">${t('Try again')}</button></p>`;
 if(ph==='done')return html`<p class="fr-state done"><button type="button" class="link" data-fr-undo="${s.id}">${t('Undo change')}</button></p>`;
 return ''}
function frItem(s,i){const a=frDraft(s),f=s.follow_up,on=i===fr.at,edit=fr.editing===s.id;fr.shown.set(s.id,a?.revision);const to=a?[movedLine(a)||(a.to_name||(a.to||[]).join(', ')?t('To {}',a.to_name||(a.to||[]).join(', ')):''),a.from_options?.length>1&&a.from?t('From {}',a.from):''].filter(Boolean).join(' · '):'',ready=frReady(s);
 const skip=fr.skipped.has(s.id);
 return html`<li class="fr-item${on?html` on`:''}${fr.changing.has(s.id)?html` rewriting`:''}${skip?html` skipped`:''}" data-fr="${s.id}" data-fr-at="${i}" tabindex="${on?0:-1}" aria-current="${on}" aria-busy="${fr.changing.has(s.id)}"><div class="fr-head"><input type="checkbox" data-fr-check="${s.id}"${fr.checked.has(s.id)?html` checked`:''}${skip?html` disabled`:''} aria-label="${t('Include {}',frName(f))}"><b title="${f.project}">${frName(f)}</b><span class="fr-meta">${t('Follow-up {} of {}',f.n,f.max)} · ${FU_CHANNELS[f.channel]||f.channel}</span></div><div class="fr-sub"><p class="fr-to" title="${to}">${to}</p><div class="fr-actions">${edit?html`<button type="button" class="primary" data-fr-save="${s.id}">${t('Save')}</button><button type="button" class="ghost" data-fr-cancel>${t('Cancel')}</button>`:html`<button type="button" class="${frStale(s)||frAdvised(s)?'fr-plain':'primary'}" data-fr-send="${s.id}"${a&&ready&&!fr.box?'':html` disabled`}>${t('Send')}</button><button type="button" class="ghost" data-fr-edit="${s.id}"${a&&ready?'':html` disabled`}>${t('Edit')}</button><button type="button" class="ghost" data-fr-skip="${s.id}"${fr.changing.has(s.id)||skip?html` disabled`:''}>${t('Skip')}</button>`}</div></div>${s.action_status?.status==='blocked'&&s.action_status.error&&!fr.changing.has(s.id)?html`<p class="fr-held" role="status">${heldLine(s.action_status.error)}</p>`:''}${frState(s)}${frAdvised(s)&&!skip?html`<p class="fr-advice"><span>${t('The Machine would stop here: {}',f.advice)}</span><button type="button" class="link" data-fr-end="${s.id}"${fr.box?html` disabled`:''}>${t('Stop follow-ups here')}</button></p>`:''}${a?(edit?html`<textarea class="fr-edit" spellcheck="true" autocapitalize="sentences" data-fr-text="${s.id}" rows="6" aria-label="${t('Follow-up text')}">${plainDraft(draftText(a))}</textarea>`:html`<div class="fr-body">${frBody(plainDraft(draftText(a)))}</div>`):html`<p class="muted fr-none">${t('No draft yet.')}</p>`}</li>`}
// Change: what should change, for all checked drafts or only the current one (the c key opens it)
function frBox(list){if(!fr.box)return '';const n=list.filter(s=>fr.checked.has(s.id)&&frReady(s)).length,one=list.find(s=>s.id===fr.box.one)||list[fr.at];
 if(!n&&fr.box.scope==='all')fr.box.scope='one';
 return html`<div class="fr-change" role="group" aria-labelledby="fr-change-q"><label class="fr-change-q" id="fr-change-q" for="fr-change-text">${t('What should change?')}</label><div class="mic-wrap"><textarea id="fr-change-text" spellcheck="true" autocapitalize="sentences" rows="2" maxlength="2000" enterkeyhint="send">${fr.box.text}</textarea>${micBtn()}</div><div class="fr-scope"><label class="fu-radio"><input type="radio" name="fr-scope" value="all"${fr.box.scope==='all'?html` checked`:''}${n?'':html` disabled`}><span>${t('All checked ({})',n)}</span></label><label class="fu-radio"><input type="radio" name="fr-scope" value="one"${fr.box.scope==='one'?html` checked`:''}><span class="fr-one" translate="no">${t('Only this one: {}',one?frName(one.follow_up):'')}</span></label></div><div class="fr-change-actions"><button type="button" class="ghost" data-fr-box-cancel>${t('Cancel')}</button><button type="button" class="primary" data-fr-box-go>${t('Rewrite')}</button></div></div>`}// The control that has focus, as a selector that finds it again after a redraw
const frFocusSel=d=>{const a=document.activeElement;if(!a||!d.contains(a))return null;if(a.id==='fr-change-text')return '#fr-change-text';if(a.name==='fr-scope')return `[name=fr-scope][value=${a.value}]`;
 for(const k of ['frCheck','frSend','frEdit','frSkip','frUnskip','frUndo','frRetry'])if(a.dataset?.[k])return `[data-${k.replace(/[A-Z]/g,c=>'-'+c.toLowerCase())}="${CSS.escape(a.dataset[k])}"]`;
 if(a.matches('.fr-item'))return `.fr-item[data-fr="${CSS.escape(a.dataset.fr)}"]`;return null};
function frDraw(reveal){const d=$('#fu-review'),list=frList();if(!list.length){if(d.open)d.close();if(fr.sent)toast(t(['{} follow-up on its way','{} follow-ups on their way'],fr.sent));return}
 const was=list.findIndex(s=>s.id===fr.cur);if(was>=0)fr.at=was;fr.at=Math.max(0,Math.min(fr.at,list.length-1));fr.cur=list[fr.at].id;fr.sig=frSig(list);fr.item=new Map(list.map(s=>[s.id,frItemSig(s)]));
 const n=list.filter(s=>fr.checked.has(s.id)&&frReady(s)).length,board=list[0].follow_up.board||'',keep=d.querySelector('.fr-list')?.scrollTop,back=frFocusSel(d);
 setHTML(d,html`<div class="snooze-heading"><h2 id="fu-review-title" title="${board}">${t(['{} follow-up for {}','{} follow-ups for {}'],list.length,board)}</h2><button type="button" data-fr-close aria-label="${t('Close')}">×</button></div><p class="fu-keys">${t('Keys: j and k move, Enter sends, e edits, s skips, c changes.')}</p><ol class="fr-list">${list.map(frItem)}</ol>${frBox(list)}<p class="ed-note warn" data-fr-error role="alert" hidden></p><div class="ed-actions fr-main"${fr.box?html` hidden`:''}><button type="button" class="ghost" data-fr-change aria-expanded="${!!fr.box}">${t('Ask for changes…')}</button><span class="grow"></span><button type="button" class="ghost" data-fr-close>${t('Close')}</button><button type="button" class="primary" data-fr-all${n&&!fr.changing.size?'':html` disabled`}>${t('Send all checked ({})',n)}</button></div>`);
 if(keep)d.querySelector('.fr-list').scrollTop=keep;const on=d.querySelector('.fr-item.on');
 if(fr.editing)d.querySelector('.fr-edit')?.focus({preventScroll:true});else (back&&d.querySelector(back)||on)?.focus({preventScroll:true});
 if(reveal)frReveal(on)}
// One draft drawn again where it is (a rewrite came back, Undo, a failure): the rest of the list, its scroll and focus stay
function frPatch(s){const d=$('#fu-review'),el=d.querySelector(`.fr-item[data-fr="${CSS.escape(s.id)}"]`);if(!el)return false;
 const back=el.contains(document.activeElement)?frFocusSel(d):null,i=+el.dataset.frAt,box=document.createElement('template');setHTML(box,frItem(s,i));
 // the draft at the top of the view stays where it is, also when one above it got shorter or longer
 const ol=el.closest('.fr-list'),top=ol.getBoundingClientRect().top,pin=[...ol.children].find(x=>x.getBoundingClientRect().bottom>top),pinId=pin?.dataset.fr,pinAt=pin?.getBoundingClientRect().top;
 el.replaceWith(box.content.firstElementChild);
 if(pinId){const n=ol.querySelector(`.fr-item[data-fr="${CSS.escape(pinId)}"]`),dy=n?n.getBoundingClientRect().top-pinAt:0;if(Math.abs(dy)>=1)ol.scrollTop+=dy}fr.item.set(s.id,frItemSig(s));if(back)(d.querySelector(back)||d.querySelector(`.fr-item[data-fr="${CSS.escape(s.id)}"]`))?.focus({preventScroll:true});return true}
// Bring the current draft into view: nothing when it's already in view; a tall one lines up its top (for a click, only
// when it isn't in view at all, so a click never pulls the text away from under the pointer)
function frReveal(el,click){const ol=el?.closest('.fr-list');if(!ol)return;const v=ol.getBoundingClientRect(),r=el.getBoundingClientRect(),pad=8,fits=r.height<=v.height-2*pad;let dy=0;
 if(fits){if(r.top<v.top+pad)dy=r.top-v.top-pad;else if(r.bottom>v.bottom-pad)dy=r.bottom-v.bottom+pad}
 else if(!click||r.bottom<v.top||r.top>v.bottom)dy=r.top-v.top-pad;
 if(Math.abs(dy)>1)ol.scrollBy({top:dy,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})}
function frMove(i,click){const d=$('#fu-review'),items=[...d.querySelectorAll('.fr-item')];if(!items.length)return;i=Math.max(0,Math.min(i,items.length-1));
 fr.at=i;fr.cur=items[i].dataset.fr;items.forEach((el,j)=>{const on=j===i;el.classList.toggle('on',on);el.tabIndex=on?0:-1;el.setAttribute('aria-current',on)});
 if(fr.box){fr.box.one=fr.cur;const s=frList().find(x=>x.id===fr.cur),one=d.querySelector('.fr-one');if(s&&one)one.textContent=t('Only this one: {}',frName(s.follow_up))}
 if(!items[i].contains(document.activeElement))items[i].focus({preventScroll:true});frReveal(items[i],click)}
// One row of buttons at a time: while the Change box is open its Cancel and Rewrite are the only ones (the Send row is
// hidden and no draft sends), and while a rewrite runs nothing is sent all at once
function frModes(){const d=$('#fu-review'),main=d.querySelector('.fr-main');if(main)main.hidden=!!fr.box;
 for(const b of d.querySelectorAll('[data-fr-send]')){const s=state.suggestions.find(x=>x.id===b.dataset.frSend);b.disabled=!!fr.box||!s||!frDraft(s)||!frReady(s)}
 for(const b of d.querySelectorAll('[data-fr-end]'))b.disabled=!!fr.box}
function frCount(){const list=frList(),n=list.filter(s=>fr.checked.has(s.id)&&frReady(s)).length,all=$('#fu-review [data-fr-all]');if(all){all.textContent=t('Send all checked ({})',n);all.disabled=!n||!!fr.changing.size}frModes();
 const scope=$('#fu-review [name=fr-scope][value=all]');if(scope){scope.disabled=!n;scope.nextElementSibling.textContent=t('All checked ({})',n);if(!n&&scope.checked){scope.checked=false;fr.box.scope='one';$('#fu-review [name=fr-scope][value=one]').checked=true}}}
// Where each rewrite stands, from the to-do itself: a new draft revision is done (the old text kept for Undo change); its
// run stuck, or a reply that left the draft as it was, couldn't change it. A to-do that closed meanwhile leaves the list.
function frTrack(){for(const [id,c] of fr.changing){const s=state.suggestions.find(x=>x.id===id);
  if(!s||s.follow_up?.state!=='open'||['completed','rejected','snoozed'].includes(s.status)){fr.changing.delete(id);fr.gone.add(id);continue}
  if(s.status!=='prepared')c.seen=true;const a=frDraft(s);
  if(s.status==='prepared'&&a&&a.revision!==c.from){fr.changing.delete(id);fr.undo.set(id,{body:c.body,subject:c.subject})}
  else if(c.seen&&(s.status==='prepared'||s.preparation_status==='blocked')){fr.changing.delete(id);fr.failed.set(id,c.text)}}}
// A poll: new drafts join (checked), sent or changed ones update in place; the draft being edited is left as it is
function frRefresh(){const d=$('#fu-review');if(!fr||!d.open||fr.busy)return;frTrack();const list=frList();
 for(const s of list)if(!fr.seen.has(s.id)){fr.seen.add(s.id);if(!frStale(s)&&!frAdvised(s))fr.checked.add(s.id)}
 if(frSig(list)===fr.sig){let n=0;for(const s of list)if(s.id!==fr.editing&&fr.item.get(s.id)!==frItemSig(s)&&frPatch(s))n++;if(n)frCount();return}
 if(!fr.editing)frDraw()}
const frSay=x=>{const p=$('#fu-review [data-fr-error]');if(p){p.textContent=x;p.hidden=!x}};
// Only the text the owner sees goes: a draft that changed since it was drawn (a rewrite, an edit elsewhere) is drawn again
// instead, to read first; nothing sends while the Change box is open or its draft is being rewritten
async function frSend(id,quiet){const s=state.suggestions.find(x=>x.id===id),a=s&&frDraft(s);if(!a||!frReady(s)||fr.box)return false;
 if(a.revision!==fr.shown.get(id)){frPatch(s);return 'changed'}
 if(a.to_options?.length){if(quiet)return false;$('#fu-review').close();openSend(id,a.revision);return false}  /* who gets it is the owner's pick: the send dialog asks; the From is the draft's own (shown in the list) */
 await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'confirm_action',args:{suggestion_id:id,revision:a.revision,approval_id:crypto.randomUUID()}})});
 fr.gone.add(id);fr.undo.delete(id);fr.shown.delete(id);fr.sent++;return true}
// The Change box opens and closes in place: the drafts, their scroll and any rewrite under way stay as they are
function frBoxOpen(){const d=$('#fu-review');if(!fr.box){const n=frList().filter(s=>fr.checked.has(s.id)&&frReady(s)).length;fr.box={text:'',scope:n?'all':'one',one:fr.cur}}
 if(!d.querySelector('.fr-change'))d.querySelector('[data-fr-error]')?.before(htmlNodes(frBox(frList())));d.querySelector('[data-fr-change]')?.setAttribute('aria-expanded','true');frModes();
 const box=$('#fr-change-text');box?.focus({preventScroll:true});box?.closest('.fr-change')?.scrollIntoView({block:'nearest'})}
// Rewrite: each draft in scope goes through its to-do's chat path (follow_up_change), at most a few at once on the
// Machine; each shows "Rewriting…" where it is until its new text is back. Nothing is sent.
function frBoxClose(){const d=$('#fu-review');fr.box=null;d.querySelector('.fr-change')?.remove();d.querySelector('[data-fr-change]')?.setAttribute('aria-expanded','false');frModes();
 d.querySelector('.fr-item.on')?.focus({preventScroll:true})}
async function frChange(ids,text){const list=frList(),pick=list.filter(s=>ids.includes(s.id)&&(frReady(s)||fr.failed.has(s.id)));if(!pick.length||!text)return;
 const before=new Map(pick.map(s=>{const a=frDraft(s);return [s.id,{from:a?.revision,body:a?draftText(a):'',subject:a?.subject,text,seen:false}]}));
 const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'follow_up_change',args:{ids:pick.map(s=>s.id),text}})});
 for(const c of r.changing||[]){const b=before.get(c.id);if(!b)continue;fr.changing.set(c.id,{...b,from:c.revision});fr.failed.delete(c.id);fr.undo.delete(c.id)}
 for(const id of r.skipped||[])if(before.has(id))fr.failed.set(id,text);
 for(const s of list)if(before.has(s.id))frPatch(s);frCount();sendWatch()}
// Skip: the draft stays in the list, unchecked, dimmed and at the bottom, marked Skipped with an Undo; it is skipped for
// good (decide reject: that waiting point is handled) only when the review closes. The next draft becomes the current one.
function frSkip(id){const list=frList(),i=list.findIndex(s=>s.id===id);if(i<0||fr.skipped.has(id))return;
 fr.skipped.set(id,fr.checked.has(id));fr.checked.delete(id);fr.editing=fr.editing===id?null:fr.editing;
 const next=list.slice(i+1).find(s=>!fr.skipped.has(s.id))||list.slice(0,i).reverse().find(s=>!fr.skipped.has(s.id));fr.cur=(next||list[i]).id;frDraw(true)}
function frUnskip(id){if(!fr.skipped.has(id))return;if(fr.skipped.get(id))fr.checked.add(id);fr.skipped.delete(id);fr.cur=id;frDraw(true)}
// Everything left is skipped after a send: the review is done
function frDoneIfSkipped(){const d=$('#fu-review'),list=frList();if(d.open&&fr.sent&&list.length&&list.every(s=>fr.skipped.has(s.id))){toast(t(['{} follow-up on its way','{} follow-ups on their way'],fr.sent));d.close()}}
async function frAct(b){const d=$('#fu-review');frSay('');fr.busy=true;try{
 if(b.dataset.frSend){b.disabled=true;const r=await frSend(b.dataset.frSend);if(d.open)frDraw(true);if(r==='changed')frSay(t('This draft changed: read it, then send.'));else frDoneIfSkipped()}
 else if(b.dataset.frSkip)frSkip(b.dataset.frSkip)
 else if(b.dataset.frUnskip)frUnskip(b.dataset.frUnskip)
 else if(b.dataset.frEnd){const id=b.dataset.frEnd;b.disabled=true;  // Stop follow-ups here: this round ends, nothing sent (follow_ups.stop_here)
  await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'follow_up_end',args:{id}})});
  fr.gone.add(id);fr.checked.delete(id);fr.skipped.delete(id);toast(t('Follow-ups stopped here.'));frDraw(true)}
 else if(b.dataset.frEdit){fr.editing=fr.cur=b.dataset.frEdit;frDraw(true)}
 else if(b.hasAttribute('data-fr-cancel')){fr.editing=null;frDraw()}
 else if(b.dataset.frSave){const id=b.dataset.frSave,s=state.suggestions.find(x=>x.id===id),a=frDraft(s),text=d.querySelector('.fr-edit').value;b.disabled=true;
  const body=unplainDraft(text,draftText(a)),r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'revise_draft',args:{suggestion_id:id,revision:a.revision,body}})});
  Object.assign(a,{revision:r.revision,body:r.body??body});fr.editing=null;fr.undo.delete(id);frDraw()}
 else if(b.hasAttribute('data-fr-change')){if(fr.box)frBoxClose();else frBoxOpen()}
 else if(b.hasAttribute('data-fr-box-cancel'))frBoxClose()
 else if(b.hasAttribute('data-fr-box-go')){const text=($('#fr-change-text')?.value||'').trim();if(!text){$('#fr-change-text')?.focus();return}
  const scope=d.querySelector('[name=fr-scope]:checked')?.value||'one',list=frList(),ids=scope==='all'?list.filter(s=>fr.checked.has(s.id)&&frReady(s)).map(s=>s.id):[fr.box.one||fr.cur];
  b.disabled=true;await frChange(ids,text);frBoxClose()}
 else if(b.dataset.frRetry){const id=b.dataset.frRetry;b.disabled=true;await frChange([id],fr.failed.get(id)||'')}
 else if(b.dataset.frUndo){const id=b.dataset.frUndo,s=state.suggestions.find(x=>x.id===id),a=s&&frDraft(s),was=fr.undo.get(id);if(!a||!was)return;b.disabled=true;
  const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'revise_draft',args:{suggestion_id:id,revision:a.revision,body:was.body,...(was.subject&&a.subject!==was.subject?{subject:was.subject}:{})}})});
  Object.assign(a,{revision:r.revision,body:r.body??was.body,...(r.subject?{subject:r.subject}:{})});fr.undo.delete(id);frPatch(s)}
 else if(b.hasAttribute('data-fr-all')){if(fr.box||fr.changing.size)return;b.disabled=true;let left=0,moved=0;for(const s of frList().filter(s=>fr.checked.has(s.id)&&frReady(s))){const r=await frSend(s.id,true);if(r==='changed')moved++;else if(!r)left++}
  frDraw();frDoneIfSkipped();if(d.open)frSay([moved?t(['{} draft changed: read it, then send.','{} drafts changed: read them, then send.'],moved):'',left?t(['{} needs you to pick who gets it: send it on its own.','{} need you to pick who gets them: send them on their own.'],left):''].filter(Boolean).join(' '))}
 else if(b.hasAttribute('data-fr-close'))d.close()}catch(x){errCaught(x);frSay(x.message);b.disabled=false}finally{if(fr)fr.busy=false}}
$('#fu-review').addEventListener('click',e=>{const b=e.target.closest('button');if(b){frAct(b);return}const item=e.target.closest('[data-fr-at]');if(item&&!e.target.closest('input,textarea')&&fr.at!==+item.dataset.frAt)frMove(+item.dataset.frAt,true)});
$('#fu-review').addEventListener('change',e=>{if(e.target.name==='fr-scope'&&fr.box){fr.box.scope=e.target.value;return}const c=e.target.closest('[data-fr-check]');if(!c)return;c.checked?fr.checked.add(c.dataset.frCheck):fr.checked.delete(c.dataset.frCheck);frCount()});
$('#fu-review').addEventListener('input',e=>{if(e.target.id==='fr-change-text'&&fr?.box)fr.box.text=e.target.value});
$('#fu-review').addEventListener('keydown',e=>{if(!fr||e.isComposing||e.altKey||e.metaKey)return;const d=$('#fu-review'),list=frList(),cur=list[fr.at];
 if(e.target.id==='fr-change-text'){if(e.key==='Escape'){e.preventDefault();frBoxClose()}else if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();d.querySelector('[data-fr-box-go]')?.click()}return}
 if(e.target.matches('textarea')){if(e.key==='Escape'){e.preventDefault();fr.editing=null;frDraw()}else if(e.key==='Enter'&&e.ctrlKey){e.preventDefault();d.querySelector('[data-fr-save]')?.click()}return}
 if(e.ctrlKey||e.target.matches('input[type=text]'))return;const k=e.key;
 if(k==='j'||k==='ArrowDown'){e.preventDefault();frMove(fr.at+1)}
 else if(k==='k'||k==='ArrowUp'){e.preventDefault();frMove(fr.at-1)}
 else if(k==='Enter'&&cur&&!fr.box&&!e.target.matches('button')){e.preventDefault();d.querySelector(`[data-fr-send="${CSS.escape(cur.id)}"]`)?.click()}
 else if(k==='e'&&cur&&frReady(cur)){e.preventDefault();fr.editing=cur.id;frDraw(true)}
 else if(k==='s'&&cur){e.preventDefault();fr.skipped.has(cur.id)?frUnskip(cur.id):frSkip(cur.id)}
 else if(k==='c'){e.preventDefault();frBoxOpen()}
 else if(k==='x'&&cur){e.preventDefault();const on=!fr.checked.has(cur.id);on?fr.checked.add(cur.id):fr.checked.delete(cur.id);const c=$(`#fu-review [data-fr-check="${CSS.escape(cur.id)}"]`);if(c)c.checked=on;frCount()}});
$('#fu-review').addEventListener('close',()=>{const skip=[...(fr?.skipped.keys()||[])],sent=fr?.sent||fr?.gone.size||fr?.changing.size;fr=null;
 if(skip.length)Promise.all(skip.map(id=>decidePost(id,{choice:'reject',feedback:'',decision_id:crypto.randomUUID()}).catch(errCaught))).finally(()=>refresh().catch(()=>{}));else if(sent)refresh().catch(()=>{})});
