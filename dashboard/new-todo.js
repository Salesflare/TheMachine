// New to-do's ways in: the sidebar row, the "+" menu, N, Search and a share from the phone. The dialog itself
// (new-todo-dialog.js) loads when first needed (dashboard_parts.LAZY 'newtodo'): each way in opens it through lazyRun.
// The sheet sits on the phone's keyboard: the keyboard's height, from the visual viewport.
function ncKeyboard(){const v=window.visualViewport;if(!v)return;for(const d of document.querySelectorAll('#new-card,#help-panel'))d.style.setProperty('--nc-kb',(d.open?Math.max(0,Math.round(innerHeight-v.height-v.offsetTop)):0)+'px')}  // and Help's
window.visualViewport?.addEventListener('resize',ncKeyboard);window.visualViewport?.addEventListener('scroll',ncKeyboard);
// Share to The Machine from a phone's share sheet: the mobile app calls this with what was shared. It opens New to-do
// with the text and files in it, for the owner to check and add; nothing is added by itself. Before the dashboard has
// loaded (still signing in), it waits for it, up to ten minutes.
window.machineShare=function(d,tries=0){if(!(Array.isArray(state?.suggestions)&&csrfLive)){if(tries<1200)setTimeout(()=>machineShare(d,tries+1),500);return true}
 const text=String(d?.text||'').trim().slice(0,2000),files=[...(d?.files||[])].filter(f=>f instanceof File);if(!text&&!files.length)return true;
 lazyRun('newtodo',()=>{ncOpen();const x=$('#nc-text');if(text){x.value=((x.value.trim()?x.value.trim()+'\n':'')+text).slice(0,2000);x.dispatchEvent(new Event('input'))}if(files.length)ncAddFiles(files)});return true};
// Share to The Machine from the installed web app (manifest.webmanifest share_target): sw.js keeps what was shared and
// opens the dashboard at #share=<id>; the page asks the worker for it, once, and opens New to-do with it, as above.
{const m=/^#share=(s_[a-f0-9]{16})$/.exec(location.hash);if(m){history.replaceState(null,'',location.pathname+location.search);
 navigator.serviceWorker?.ready.then(r=>new Promise((ok,no)=>{const ch=new MessageChannel();ch.port1.onmessage=e=>ok(e.data);setTimeout(()=>no(Error('timeout')),15000);
  (navigator.serviceWorker.controller||r.active).postMessage({share:m[1]},[ch.port2])})).then(d=>{if(d)machineShare({text:d.text,files:d.files})}).catch(()=>{})}}
// Entry points: a row under Search on a computer, "+" in the top bar on a phone, C, and the palette (Ctrl/⌘K) then "new".
{const row=document.createElement('button');row.type='button';row.className='side-new';row.id='side-new';row.dataset.newCard='';row.title='New to-do (N)';row.setAttribute('aria-label','New to-do');
 setHTML(row,html`${NC_PLUS}<span>New to-do</span><kbd>N</kbd>`);$('#side-search').after(row);
 // Talk: the main live conversation, through what needs the owner (shows once this Machine can talk live)
 const talkRow=document.createElement('button');talkRow.type='button';talkRow.className='side-new side-talk';talkRow.id='side-talk';talkRow.dataset.talkMain='';talkRow.hidden=true;
 talkRow.title='Talk (T)';talkRow.setAttribute('aria-label','Talk');talkRow.setAttribute('aria-pressed','false');setHTML(talkRow,html`${WAVE}<span>Talk</span><kbd>T</kbd>`);row.after(talkRow);
 const plus=document.createElement('button');plus.type='button';plus.className='head-link settings-link new-card-link';plus.id='new-card-top';plus.dataset.newMenu='';plus.title='New';plus.setAttribute('aria-label','New');plus.setAttribute('aria-haspopup','menu');plus.setAttribute('aria-expanded','false');
 // With the phone drawer (#topbar), the sidebar row shows in the drawer and the "+" sits on the right of the top bar.
 const top=$('#topbar');if(top){plus.className='topbar-menu new-card-top';setHTML(plus,NC_PLUS);top.append(plus);document.documentElement.classList.add('nc-drawer')}
 else{setHTML(plus,html`${NC_PLUS}<span class="lbl">New</span>`);$('#open-settings').before(plus)}}
// Opens New to-do once its dialog is in (at once when it is). byPointer: opened by a tap or click, not a key.
const newTodo=(o,byPointer)=>lazyRun('newtodo',()=>{ncOpen(o);if(byPointer!=null)nc.byPointer=byPointer});
document.addEventListener('click',e=>{if(e.target.closest('[data-new-card]')){e.preventDefault();if(typeof drawerClose==='function')drawerClose();newTodo(undefined,e.detail>0)}});
// "+" in the top bar: what to make. A card, a person, an organization, a project or an event (first on the Calendar).
const NEW_WHAT=[['card','New to-do'],['person','New person'],['org','New organization'],['project','New project']];
const newWhatList=()=>$('#calendar')?.hidden===false?[['event','New event'],...NEW_WHAT]:[...NEW_WHAT,['event','New event']];
function newMenu(open){const b=$('#new-card-top');let m=$('#new-menu');if(!open){if(m&&!m.hidden){m.hidden=true;b?.setAttribute('aria-expanded','false')}return}
 if(!m){m=document.createElement('div');m.id='new-menu';m.className='fact-menu-list new-menu';m.setAttribute('role','menu');m.setAttribute('aria-label','New');document.body.append(m)}
 setHTML(m,html`${newWhatList().map(([k,t])=>html`<button type="button" role="menuitem" data-new-what="${k}">${t}</button>`)}`);
 const r=b.getBoundingClientRect();m.style.top=Math.round(r.bottom+6)+'px';m.style.right=Math.max(8,Math.round(innerWidth-r.right))+'px';m.hidden=false;b.setAttribute('aria-expanded','true');m.querySelector('button').focus({preventScroll:true})}
const newWhat=(k,byPointer)=>{if(k==='card')newTodo(undefined,byPointer);else if(k==='event')lazyRun('calendar',()=>calNew());else if(k==='project')lazyRun('graph',()=>pjOpen({}));else lazyRun('graph',()=>recOpen(k))};
document.addEventListener('click',e=>{const plus=e.target.closest('[data-new-menu]');if(plus){e.preventDefault();newMenu($('#new-menu')?.hidden!==false);return}
 const w=e.target.closest('[data-new-what]');if(w){newMenu(false);if(typeof drawerClose==='function')drawerClose();newWhat(w.dataset.newWhat,e.detail>0);return}
 if(!e.target.closest('#new-menu'))newMenu(false)});
document.addEventListener('keydown',e=>{const m=$('#new-menu');if(!m||m.hidden)return;if(e.key==='Escape'){e.preventDefault();newMenu(false);$('#new-card-top')?.focus();return}
 if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const all=[...m.querySelectorAll('button')],i=all.indexOf(document.activeElement);all[(i+(e.key==='ArrowDown'?1:all.length-1))%all.length].focus()}});
addEventListener('resize',()=>newMenu(false));
const ncTyping=t=>t?.closest?.('input,textarea,select,[contenteditable=""],[contenteditable="true"],dialog[open]');
// C, Ctrl/⌘K and the other keys: the action registry and the palette at the end of this script.
const ncAsked=()=>{const q=$('#side-find').value.trim().toLowerCase();return q.length>=2&&(q==='+'||('new to-do'.startsWith(q)||'new card'.startsWith(q)))};
$('#side-find').addEventListener('input',()=>$('#side-new').classList.toggle('hit',ncAsked()));
$('#side-find').addEventListener('keydown',e=>{if(e.key==='Enter'&&ncAsked()){e.preventDefault();e.stopImmediatePropagation();e.target.value='';sideCards();$('#side-new').classList.remove('hit');newTodo()}},true);

