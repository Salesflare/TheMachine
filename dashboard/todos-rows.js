// Merge offer on an owner's card: the review thought it is the same as another card. Only the owner's tap merges.
function mergeOther(s){if(s.origin!=='owner'||!s.merge_offer||closed(s))return null;try{const o=JSON.parse(s.merge_offer);return o.kept?null:(state.suggestions||[]).find(x=>x.id===o.card_id&&!closed(x))||null}catch{return null}}
function mergeOffer(s){const o=mergeOther(s);return o?`<div class="merge-offer"><span>Looks like the same as “${esc(o.title)}”. Merge?</span><button type="button" class="ghost" data-merge="yes" data-card="${esc(s.id)}">Merge</button><button type="button" class="quiet" data-merge="no" data-card="${esc(s.id)}">Keep both</button></div>`:''}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-merge]');if(!b)return;e.preventDefault();b.disabled=true;const id=b.dataset.card,merge=b.dataset.merge==='yes';
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'card_merge',args:{suggestion_id:id,merge,decision_id:crypto.randomUUID()}})});
  toast(merge?'Merged':'Kept both');if(merge&&chatId===id&&r?.merged)chatGo(r.id);await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});

// Rename: the owner's title is kept over the generated one, on every surface. An input opens over the title in the
// sidebar (the ⋯ on hover, a double click, a right click, a long press on a phone), the chat's header (a click, or
// Rename in its menu) and the card (Rename in More; a click on the title on a computer). Enter saves, Esc cancels,
// empty puts the old title back. Saved at once on screen; the chat gets a quiet "Renamed" line.
const fine=()=>matchMedia('(hover:hover) and (pointer:fine)').matches;
const ROWS='#side-cards a[href^="#chat="],.chat-side a[href^="#chat="]';
const rowId=a=>a?.getAttribute('href')?.slice(6)||'';
const cardOf=id=>(state.suggestions||[]).find(s=>s.id===id);
let renaming=null;
function renameClose(){document.querySelector('.rename-box')?.remove();renaming=null}
// The input stays over the title while the page scrolls (a phone's keyboard opening scrolls it too).
function renamePlace(){if(!renaming)return;let el=renaming.el;if(!el?.isConnected)el=renaming.el=titleEl(renaming.id,renaming.prefer);if(!el)return;
 const r=el.getBoundingClientRect(),h=renaming.h,b=renaming.box;b.style.left=Math.max(8,r.left-4)+'px';b.style.top=Math.max(8,r.top+(r.height-h)/2)+'px'}
function renameAt(id,el,prefer){const s=cardOf(id);if(!s||!el)return;renameClose();rowMenuClose();
 let r=el.getBoundingClientRect();if(r.top<64||r.bottom>innerHeight-64){el.scrollIntoView({block:'center'});r=el.getBoundingClientRect()}
 const box=document.createElement('div');box.className='rename-box';
 const wide=(el.closest('h3')||el).getBoundingClientRect(),h=Math.max(30,Math.min(44,r.height)),w=Math.max(200,Math.min(wide.width,innerWidth-r.left-12));
 Object.assign(box.style,{left:Math.max(8,r.left-4)+'px',top:Math.max(8,r.top+(r.height-h)/2)+'px',width:w+8+'px'});
 box.innerHTML=`<input type="text" maxlength="200" aria-label="To-do title" style="height:${h}px;font-size:${getComputedStyle(el).fontSize};font-weight:${getComputedStyle(el).fontWeight}">${s.title_suggested?'<button type="button" class="rename-reset">Reset to suggested title</button>':''}`;
 document.body.append(box);const input=box.querySelector('input');input.value=s.title;input.focus();input.select();renaming={id,box,el,h,prefer};
 let done=false;const finish=(save,reset=false)=>{if(done)return;done=true;const v=input.value;renameClose();if(save)renameSave(id,v,reset)};
 input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.isComposing){e.preventDefault();finish(true)}else if(e.key==='Escape'){e.preventDefault();e.stopPropagation();finish(false)}});
 input.addEventListener('blur',()=>setTimeout(()=>{if(!done&&!box.contains(document.activeElement))finish(true)},0));
 const reset=box.querySelector('.rename-reset');if(reset){reset.addEventListener('mousedown',e=>e.preventDefault());reset.onclick=()=>finish(true,true)}}
async function renameSave(id,value,reset=false){const s=cardOf(id);if(!s)return;const title=String(value||'').replace(/\s+/g,' ').trim().slice(0,200),before={title:s.title,title_suggested:s.title_suggested};
 if(!reset&&(!title||title===s.title))return; // empty puts the old title back
 if(reset){if(!s.title_suggested)return;Object.assign(s,{title:s.title_suggested,title_suggested:null})}
 else Object.assign(s,{title,title_suggested:title===(s.title_suggested??null)?null:s.title_suggested??before.title});
 localEdits++;render();
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'card_rename',args:{suggestion_id:id,title:reset?null:title,reset,decision_id:crypto.randomUUID()}})});
  await refresh();if(chatId===id)chatPoll()}
 catch(e){errCaught(e);Object.assign(s,before);localEdits++;render();toast(e.message||'Couldn’t rename the to-do',true)}}
// Where the title of card id is on screen now: the chat header, the card's heading, or its sidebar row.
const shownEl=sel=>[...document.querySelectorAll(sel)].find(n=>n.getClientRects().length)||null;
function titleEl(id,prefer){const css=CSS.escape(id);return(prefer==='row'?shownEl(`#side-cards a[href="#chat=${css}"],.chat-side a[href="#chat=${css}"]`):null)
 ||(chatId===id?document.querySelector('.chat-title'):null)||document.querySelector(`#task-${css} h3 .title-link,#task-${css} h3`)||document.querySelector(`#side-cards a[href="#chat=${css}"]`)}
// The ⋯ on a sidebar row (on hover), and its small menu (also on a right click or a long press).
const rowMore=document.createElement('button');rowMore.type='button';rowMore.className='row-more';rowMore.hidden=true;rowMore.setAttribute('aria-label','More for this to-do');rowMore.title='More';rowMore.innerHTML=DOTS;document.body.append(rowMore);
let rowHover=null;
document.addEventListener('mouseover',e=>{if(e.target.closest('.row-more'))return;const a=e.target.closest(ROWS);if(a===rowHover)return;rowHover=a;
 if(!a||!fine()){rowMore.hidden=true;return}const r=a.getBoundingClientRect();Object.assign(rowMore.style,{left:r.right-28+'px',top:r.top+(r.height-24)/2+'px'});rowMore.dataset.id=rowId(a);rowMore.hidden=false});
document.addEventListener('scroll',()=>{rowMore.hidden=true;rowHover=null;rowMenuClose();renamePlace()},true);addEventListener('resize',()=>renamePlace());
function rowMenuClose(){document.querySelector('.row-menu')?.remove()}
function rowMenu(id,x,y){rowMenuClose();const m=document.createElement('div');m.className='row-menu';m.setAttribute('role','menu');
 m.innerHTML=`<button type="button" role="menuitem" data-row-rename="${esc(id)}">Rename</button><button type="button" role="menuitem" data-row-open="${esc(id)}">Open</button>`;document.body.append(m);
 const r=m.getBoundingClientRect();Object.assign(m.style,{left:Math.max(8,Math.min(x,innerWidth-r.width-8))+'px',top:Math.max(8,Math.min(y,innerHeight-r.height-8))+'px'});m.querySelector('button').focus()}
rowMore.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();const r=rowMore.getBoundingClientRect();rowMenu(rowMore.dataset.id,r.left,r.bottom+4)});
document.addEventListener('click',e=>{const rn=e.target.closest('[data-row-rename]'),op=e.target.closest('[data-row-open]');
 if(rn){e.preventDefault();const id=rn.dataset.rowRename;rowMenuClose();renameAt(id,titleEl(id,'row'),'row');return}
 if(op){e.preventDefault();rowMenuClose();chatGo(op.dataset.rowOpen);return}
 if(!e.target.closest('.row-menu'))rowMenuClose()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.querySelector('.row-menu')){rowMenuClose();e.stopPropagation()}},true);
document.addEventListener('contextmenu',e=>{const a=e.target.closest(ROWS);if(!a)return;e.preventDefault();rowMenu(rowId(a),e.clientX,e.clientY)});
document.addEventListener('dblclick',e=>{const a=e.target.closest(ROWS);if(!a)return;e.preventDefault();const id=rowId(a);requestAnimationFrame(()=>renameAt(id,titleEl(id,'row'),'row'))});
// A long press on a row on a phone opens the same menu; the tap that ends it doesn't open the card.
{let timer=null,pressed=false,start=null;
 document.addEventListener('touchstart',e=>{const a=e.target.closest(ROWS);if(!a||e.touches.length!==1)return;pressed=false;const t=e.touches[0];start=[t.clientX,t.clientY];
  clearTimeout(timer);timer=setTimeout(()=>{pressed=true;navigator.vibrate?.(10);rowMenu(rowId(a),start[0],start[1]+8)},500)},{passive:true});
 document.addEventListener('touchmove',e=>{if(timer&&start&&Math.hypot(e.touches[0].clientX-start[0],e.touches[0].clientY-start[1])>8){clearTimeout(timer);timer=null}},{passive:true});
 document.addEventListener('touchend',()=>{clearTimeout(timer);timer=null},{passive:true});
 document.addEventListener('click',e=>{if(pressed&&e.target.closest(ROWS)){e.preventDefault();e.stopImmediatePropagation();pressed=false}},true)}
// Rename in a card's More menu (and so in the chat header's menu); a click on the chat's title; on a computer, a click
// on a card's title. A tap on a phone still opens the card.
document.addEventListener('click',e=>{const b=e.target.closest('[data-rename]');if(b){e.preventDefault();e.stopPropagation();b.closest('details')?.removeAttribute('open');const id=b.dataset.rename;requestAnimationFrame(()=>renameAt(id,titleEl(id)));return}
 const ct=e.target.closest('.chat-title');if(ct&&chatId){e.preventDefault();renameAt(chatId,ct);return}
 const tl=e.target.closest('.card h3 .title-link');if(tl&&fine()&&!e.ctrlKey&&!e.metaKey&&!e.shiftKey){const id=tl.closest('article')?.id.replace(/^task-/,'');if(cardOf(id)){e.preventDefault();e.stopPropagation();renameAt(id,tl)}}},true);
document.addEventListener('mouseover',e=>{const t=e.target.closest('.card h3 .title-link');if(t&&fine()&&!t.classList.contains('chat-title'))t.title='Click to rename'});
