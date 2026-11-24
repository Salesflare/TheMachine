// The other boxes someone types in to ask, answer or add keep their text too, with todos-kept.js (its store, its rules, its
// Discard with Undo). data-keep is the box's key: New to-do ('new'), Ask for changes and Answer on a to-do, also in Go
// through ('ask|' its id '|' what it asked), the follow-ups review's ('fr|' its group), a review's note and edits ('rev|'
// its id '|' …). The text comes back as the box is drawn or opened; Ask for changes opens by itself while something is kept
// for it. Cancel is Discard; Esc, a closed sheet and another page keep it. The last typed wins. Files aren't kept.
// An entry: k, at, by, and x: the text, and New to-do's chips. A lazy part (dashboard_parts.LAZY 'keptbox'); kept fetches it.
const ktBoxes=(d=document)=>[...d.querySelectorAll('[data-keep]')];
function ktBox(el){const k=el.dataset.keep,x=el.value.trim()?[el.value,...k==='new'?[nc.scope,nc.due&&+nc.due,nc.due?.timed,nc.repeat,nc.about,nc.attach]:[]]:null;
 if(!ktSame(ktGet(k)?.x||null,x))ktWrite(k,()=>x&&{k,id:k,at:Date.now(),by:ktTab,o:[],x});return x}
function ktPut(el){const x=ktGet(el.dataset.keep)?.x;if(!x||el.value!==el.defaultValue||el.value===x[0])return;
 if(x.length>1){const [,scope,due,timed,repeat,about,attach]=x;Object.assign(nc,{scope,due:due&&Object.assign(new Date(due),{timed}),repeat,attach},nc.about.length?{}:{about});ncChips()}
 el.value=x[0];el.classList.add('filled');el.dispatchEvent(new Event('input',{bubbles:true}))}
function keptBoxes(){setTimeout(()=>ktBoxes().forEach(ktPut))}
function ktAsks(){for(const e of ktList){const m=/^ask\|(\w+)\|$/.exec(e.k);if(m)changing.add(m[1])}}
// Sent, asked or added
function keptBoxGone(p){for(const e of ktList)if(e.k.startsWith(p))ktWrite(e.k,()=>null)}
lazyRun('kept',()=>ktReady.then(()=>{
 for(const el of ktBoxes())if(el.value!==el.defaultValue&&!ktGet(el.dataset.keep))ktBox(el);  // typed before this was in
 if(ktList.length)ktDraw();
 document.addEventListener('focusin',e=>{if(e.target.dataset.keep)ktPut(e.target)});
 document.addEventListener('input',e=>{if(e.target.dataset?.keep)ktBox(e.target)});
 // New to-do's chips change without typing
 addEventListener('click',()=>{for(const el of document.querySelectorAll('#new-card[open] [data-keep]'))ktBox(el)});
 document.addEventListener('click',e=>{let b=e.target.closest?.('[data-choice=cancel-change],[data-fr-box-cancel],[data-review-cancel]'),k;
  for(;b&&!k;b=b.parentElement)k=b.querySelector('[data-keep]')?.dataset.keep;
  if(k&&ktGet(k))ktDrop(k)},true);
 document.addEventListener('close',e=>{if(!e.target.open)for(const {dataset:{keep:k}} of ktBoxes(e.target))if(ktGet(k))ktTell(k==='new'?t('Kept, not added.'):t('Kept, not sent.'),t('Discard'),()=>{ktDrop(k);ktDraw()})},true)}));
