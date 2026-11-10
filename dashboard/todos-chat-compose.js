// On open: the latest at the bottom, nothing cut off under the header; a short chat just sits under the header.
// The thread scrolls in its own box (on a phone too, so the message box never moves); a page without that layout scrolls itself.
const chatScroller=()=>{const l=$('#chat-log');return l&&getComputedStyle(l).overflowY!=='visible'?l:null};
const chatToEnd=()=>{const l=chatScroller();if(l)l.scrollTop=l.scrollHeight;else scrollTo(0,document.documentElement.scrollHeight)};
function chatScrollStart(){const log=$('#chat-log');if(!log)return;if(chatScroller())return chatToEnd();scrollTo(0,document.documentElement.scrollHeight);
 // The first item under the header starts whole when only a little of it is hidden; otherwise it fades under the header.
 const head=$('.chat-head')?.getBoundingClientRect().bottom||0,cut=[...log.children].find(n=>{const b=n.getBoundingClientRect();return b.top<head-1&&b.bottom>head+1});
 if(cut&&head-cut.getBoundingClientRect().top<=12)scrollBy(0,-(head-cut.getBoundingClientRect().top))}
// Make el's children match html, replacing only the ones that changed (same position, same item), so expanded parts,
// hovers and the scroll position stay as they are.
function chatPatch(el,body){const t=document.createElement('template');setHTML(t,body);const fresh=[...t.content.childNodes].filter(n=>n.nodeType===1||n.textContent.trim()),old=[...el.childNodes].filter(n=>n.nodeType===1||n.textContent.trim());
 fresh.forEach((n,i)=>{const o=old[i];if(!o)el.append(n);else if(!o.isEqualNode(n))o.replaceWith(n)});old.slice(fresh.length).forEach(n=>n.remove())}
// Around an update of the thread: at the end (within 40px) it stays at the end; otherwise the item in view stays where it is.
function chatKeepPlace(fn){const log=$('#chat-log');if(!log)return fn();const l=chatScroller(),end=chatEndNow(40);
 const top=l?l.getBoundingClientRect().top:($('.chat-head')?.getBoundingClientRect().bottom||0),kids=[...log.children];
 const at=kids.findIndex(n=>n.getBoundingClientRect().bottom>top+1),y=at>=0?kids[at].getBoundingClientRect().top:0,keep=l?.scrollTop;fn();
 if(end&&chat?.items?.length){chatToEnd();return}if(l)l.scrollTop=keep;const n=at>=0?$('#chat-log').children[at]:null;if(!n)return;
 const d=n.getBoundingClientRect().top-y;if(Math.abs(d)>.5){if(l)l.scrollTop+=d;else scrollBy(0,d)}}
// Long names fade out at the edge instead of wrapping; the full name is in their tooltip.
function chatFades(){document.querySelectorAll('.chat-side a,.chat-title,.side-cards a').forEach(n=>{const cut=n.scrollHeight>n.clientHeight+1;n.classList.toggle('fade',n.scrollWidth>n.clientWidth+1||cut);
 // A title cut after its second line ends where its last whole word does, often well before the edge: fade out there
 if(!cut||!n.firstChild||n.firstChild.nodeType!==3){n.style.removeProperty('--fade-x');return}
 const box=n.getBoundingClientRect(),r=document.createRange(),txt=n.firstChild;let lo=0,hi=txt.length;
 while(lo<hi){const m=(lo+hi+1)>>1;r.setStart(txt,m-1);r.setEnd(txt,m);const q=r.getBoundingClientRect();if(q.bottom<=box.bottom+1)lo=m;else hi=m-1}
 while(lo>1&&/\s/.test(txt.data[lo-1]))lo--;r.setStart(txt,Math.max(0,lo-1));r.setEnd(txt,lo);n.style.setProperty('--fade-x',Math.round(r.getBoundingClientRect().right-box.left)+'px')})}
addEventListener('resize',()=>chatFades());
// A scrolled box shows its thin thumb while it moves
// Fonts that arrive late change the widths: measure the fades again then
document.fonts?.ready.then(()=>requestAnimationFrame(chatFades));document.fonts?.addEventListener?.('loadingdone',()=>requestAnimationFrame(chatFades));
document.addEventListener('scroll',e=>{const b=e.target;if(!b.matches?.('.chat-log,.chat-side,.side-cards'))return;b.classList.add('scrolling');clearTimeout(b._scrolling);b._scrolling=setTimeout(()=>b.classList.remove('scrolling'),900)},{capture:true,passive:true});
// A result file shown in the thread (a copy-only draft): read once, then kept while the page is open
const chatFiles=new Map();
// A saved draft file as the card shows it: only the draft (the quoted text under its heading, unquoted), never the
// sources section after it; its name from its heading ("X: draft internal answer for Andrea" is "Internal answer for Andrea")
function draftFile(text){const lines=String(text||'').replace(/\r/g,'').split('\n');let head='';if(/^#\s/.test(lines[0]||''))head=lines.shift().replace(/^#\s+/,'').trim();
 const end=lines.findIndex(l=>/^#{1,6}\s/.test(l)),part=(end<0?lines:lines.slice(0,end));const quoted=part.filter(l=>/^\s*>/.test(l));
 const body=(quoted.length?quoted.map(l=>l.replace(/^\s*>\s?/,'')):part).join('\n').replace(/\n{3,}/g,'\n\n').trim();
 let name=head.includes(':')?head.slice(head.lastIndexOf(':')+1).trim():head;name=name.replace(/^(?:a\s+)?draft(?:ed)?\s+(?:of\s+)?/i,'');
 return {name:name?name[0].toUpperCase()+name.slice(1):'',body,sources:end>=0}}
async function chatPreviews(){for(const n of document.querySelectorAll('#chat-log [data-preview]')){const key=n.dataset.preview;if(chatFiles.has(key))continue;chatFiles.set(key,null);
 const [id,path]=key.split('|');try{const d=await request('api/result?id='+id+'&file='+encodeURIComponent(path));chatFiles.set(key,d.pdf?'':String(d.text||''))}catch{chatFiles.set(key,'')}paintChat()}}
// A refresh while the chat is open updates the thread, list and header in place and keeps the message box itself,
// so a field you are typing in never loses its focus, text or caret.
// The to-do list a chat takes the place of is kept aside, and put back when the chat closes: drawn over again (drawKept),
// only what changed meanwhile is new, so going back costs no list built and laid out anew.
var listKept=null;  // var and function: a render before this part has run finds nothing kept
function listBack(){if(!listKept)return;$('#suggestions').replaceChildren(listKept);listKept=null}
function chatMount(id,body){const box=$('#suggestions'),cur=box.querySelector(':scope>.chat-layout');
 if(!cur&&box.firstChild){listKept=document.createDocumentFragment();listKept.append(...box.childNodes)}
 if(!cur||cur.dataset.chat!==id||!cur.querySelector('#chat-input')){setHTML(box,body);requestAnimationFrame(chatFades);return}
 const t=document.createElement('template');setHTML(t,body);const nu=t.content.querySelector('.chat-layout');cur.className=nu.className;
 const swap=sel=>{const a=cur.querySelector(sel),b=nu.querySelector(sel);if(!a||!b||a.isEqualNode(b))return;a.replaceWith(b)};
 const side=cur.querySelector('.chat-side'),top=side?.scrollTop;if(side)chatPatch(side,nodeHTML(...nu.querySelector('.chat-side').childNodes));if(side)side.scrollTop=top;
 swap('.chat-panel');chatKeepPlace(()=>chatPatch(cur.querySelector('#chat-log'),nodeHTML(...nu.querySelector('#chat-log').childNodes)));
 if(!cur.querySelector('#chat-menu')?.open)swap('.chat-head');swap('#chat-status');swap('#chat-picks');{const typing=document.activeElement?.matches('textarea,input[type=text]')&&cur.querySelector('#chat-sheet')?.contains(document.activeElement);if(!typing||!nu.querySelector('#chat-sheet')?.children.length)swap('#chat-sheet')}chatFades()}
// On a phone the chat column is exactly the visible part of the window (--vv-h, --vv-top): where the browser doesn't
// shrink the page for the on-screen keyboard (iOS Safari) that part shrinks and slides instead, and the message box
// rides on the keyboard; Android Chrome resizes the page itself (interactive-widget=resizes-content). Zoomed in with
// two fingers, the column keeps the window's size. Keep the latest message in view when you were at the end.
let chatAtEnd=false;
const chatEndNow=(gap=80)=>{const l=chatScroller();return l?l.scrollTop+l.clientHeight>=l.scrollHeight-gap:innerHeight+scrollY>=document.documentElement.scrollHeight-gap};
function chatKeyboard(){const v=window.visualViewport;if(!v)return;const kb=Math.max(0,Math.round(innerHeight-v.height-v.offsetTop)),typing=document.activeElement?.id==='chat-input',zoomed=Math.abs((v.scale||1)-1)>.01,r=document.documentElement.style;
 r.setProperty('--vv-h',(zoomed?innerHeight:v.height)+'px');r.setProperty('--vv-top',(zoomed?0:Math.max(0,v.offsetTop))+'px');document.body.classList.toggle('kb-open',typing&&(kb>0||innerHeight<screen.height*.6));
 if(typing&&chatAtEnd)requestAnimationFrame(chatToEnd)}
window.visualViewport?.addEventListener('resize',chatKeyboard);window.visualViewport?.addEventListener('scroll',chatKeyboard);addEventListener('resize',chatKeyboard);chatKeyboard();
function paintChat(){const log=$('#chat-log'),s=chatOpen();if(!log||!s)return;chatKeepPlace(()=>chatPatch(log,chatLog(s)));
 const st=$('#chat-status'),sh=chatStatus(s);if(st&&st.innerHTML!==String(sh))setHTML(st,sh);const menu=$('#chat-menu');if(menu&&!menu.open){const rest=chatParts(s).rest;menu.toggleAttribute('data-empty',!rest);setHTML(menu.querySelector('.chat-menu-list'),html`${rest}<button type="button" class="ghost" data-chat-drawer aria-expanded="${chatDrawer}">All tasks</button>`);}
 const picks=$('#chat-picks');if(picks){const ph=chatPicks(s);if(picks.innerHTML!==String(ph))setHTML(picks,ph);picks.hidden=!chatPicksShown()}
 chatSendState();chatFades();chatPreviews();cmPaint('chat')}
// The chat this device kept for the card: shown at once while the live one loads (that one replaces it in place)
async function chatKept(id){const hit=await localCache.read('chat:'+id);if(!hit||id!==chatId||chat&&!(chat.unavailable&&!chat.items?.length))return;chat={...hit.value,cursor:null,active:false};paintChat();requestAnimationFrame(chatScrollStart)}
async function chatPoll(){clearTimeout(chatTimer);const id=chatId;if(!id)return;
 if(!document.hidden&&!$('#inbox').hidden)try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'card_chat',args:{suggestion_id:id,...(chat?.cursor&&chat.items?{cursor:chat.cursor}:{})}})});
  if(id!==chatId)return;const was=chat?.active,first=!chat;
  // A read that failed while the chat was already on screen changes nothing but whether the run still goes: what was
  // shown stays (with the live answer), quietly, and the next ask catches up
  if(r.unavailable&&chat?.items?.length&&!chat.unavailable)chat={...chat,active:r.active,status:r.status,live:r.active?chat.live:null,stale:true};
  else{const keep=r.unchanged;chat={...r,items:keep?chat.items:r.items,cursor:(keep?chat.cursor:r.cursor)||null}}paintChat();if(!r.unchanged&&!r.unavailable)localCache.put('chat:'+id,{...chat,cursor:null});if(first){requestAnimationFrame(chatScrollStart);setTimeout(chatScrollStart,150)}if(was&&!r.active){refresh();talkTurnDone()}}catch(e){errCaught(e);if(id===chatId&&!chat){chat={items:[],unavailable:true};paintChat()}
  // the to-do is gone from the Machine (a list kept from before): the fresh list closes its chat with the line, at once
  if(id===chatId&&e.status===400&&/^Unknown suggestion/.test(e.message||''))refresh()}
 if(id===chatId)chatTimer=setTimeout(chatPoll,chat?.active?1000:chat?.unavailable||chat?.stale?4000:10000)}
// Whether this page put the open chat on the history (so back can take it off again instead of adding an entry)
let chatPushed=false;
let chatGone=null;
function openChatLink(refreshed){if(!state.suggestions||location.hash==='#browser')return;  // the browser pane over a chat keeps that chat for Back
const m=/^#chat=([a-f0-9]{16})$/.exec(location.hash),id=m&&state.suggestions.some(s=>s.id===m[1])?m[1]:null;
 // A link to a to-do that isn't here (an old notification, the to-do removed or long done): once the Machine's latest
 // list says so too, one short line on the list instead of a blank page
 const gone=()=>{history.replaceState(null,'',location.pathname+location.search);openChatLink();toast(t('That to-do isn’t here anymore.'))};  // and a chat open on it closes
 // right after a refresh the list is the Machine's latest already: a chat open on it (from a list kept since before) closes with the line
 // a done one past those the status sends: asked for first, and the chat opens when it comes (doneFetch)
 if(m&&!id&&doneFetch(m[1],()=>{if(location.hash==='#chat='+m[1])openChatLink(refreshed)}))return;
 if(m&&!id&&refreshed){gone();return}
 if(m&&!id&&!chatGone){chatGone=m[1];refresh().then(()=>{if(location.hash==='#chat='+chatGone&&!state.suggestions.some(s=>s.id===chatGone))gone()}).finally(()=>{chatGone=null});return}
 if(m&&!id)return;
 // Only a link or a step back closes the chat on screen, never a refresh (a sent message, a job that starts or moves the
 // to-do to another list): an address that lost the chat's link on the way gets it back
 if(refreshed&&!location.hash&&chatId&&!$('#inbox').hidden&&chatOpen()){history.replaceState(history.state,'',location.pathname+location.search+'#chat='+chatId);return}
 if(id===chatId)return;if(id)toastNotAbout(id);const was=chatId;chatId=id;chat=null;if(talk?.main){if(id&&talk.sid!==id)talkFocus(talk,id)}else if(talk&&talk.sid!==id)talkEnd();if(id)talkLoad();chatDrawer=false;chatDropFiles();chatOpenSet.clear();clearTimeout(chatTimer);if(!id)chatPushed=false;
 if(id){document.querySelector('nav [data-tab="inbox"]').click();render('view');scrollTo(0,0);chatKept(id);chatDraftBack(id);chatPoll();if(kbKeyed()&&matchMedia('(pointer:fine)').matches)$('#chat-input')?.focus({preventScroll:true})}else{render('view');const c=was&&document.getElementById('task-'+was);if(c){for(let d=c.parentElement;d;d=d.parentElement)if(d.tagName==='DETAILS')d.open=true;c.scrollIntoView({block:'center'});const a=document.activeElement;if(!a||a===document.body||!a.isConnected)kbFocus(c)}}}
// A chat opens only on a real tap: not on the tap that stops a fling, nor on one that ends a scroll or a drag.
let chatScrolledAt=0,chatDown=null;
addEventListener('scroll',()=>{chatScrolledAt=Date.now()},{passive:true});
document.addEventListener('pointerdown',e=>{chatDown={x:e.clientX,y:e.clientY,at:Date.now(),scrolled:Date.now()-chatScrolledAt<250}},{passive:true,capture:true});
const chatRealTap=e=>!(chatDown&&(chatDown.scrolled||Math.hypot(e.clientX-chatDown.x,e.clientY-chatDown.y)>8));
function chatGo(id){if(history.state?.drawer){history.replaceState(null,'',location.pathname+location.search+'#chat='+id);chatPushed=true}else if(!chatId){history.pushState(null,'',location.pathname+location.search+'#chat='+id);chatPushed=true}else history.replaceState(null,'',location.pathname+location.search+'#chat='+id);openChatLink()}
// In-page links, also when the page's base is another path; the "You asked" note opens the chat too.
$('#suggestions').addEventListener('click',e=>{const a=e.target.closest('a[href^="#chat="],a[href^="#card="]'),note=!a&&e.target.closest('[data-chat-open]');
 if(note&&!e.target.closest('a,button')){if(chatRealTap(e))chatGo(note.dataset.chatOpen);return}
 if(!a||e.ctrlKey||e.metaKey||e.shiftKey)return;e.preventDefault();const href=a.getAttribute('href');
 if(a.hasAttribute('data-chat-back')){if(chatPushed){history.back();return}history.replaceState(null,'',location.pathname+location.search+href);openChatLink();openCardLink();return}
 if(href.startsWith('#chat=')){if(chatRealTap(e)||chatId)chatGo(href.slice(6));return}
 location.hash=href});
$('#suggestions').addEventListener('toggle',e=>{const k=e.target.dataset?.foldKey;if(k==null||!e.target.closest('#chat-log'))return;e.target.open?chatOpenSet.add(k):chatOpenSet.delete(k)},true);
$('#suggestions').addEventListener('input',e=>{if(e.target.id==='chat-input'){chatGrow(e.target);chatDraftKeep(chatId,e.target.value)}});
$('#suggestions').addEventListener('focusin',e=>{if(e.target.id!=='chat-input')return;chatAtEnd=chatEndNow();if($('#chat-picks'))$('#chat-picks').hidden=false;chatKeyboard();setTimeout(chatKeyboard,350)});
$('#suggestions').addEventListener('focusout',e=>{if(e.target.id!=='chat-input')return;setTimeout(chatKeyboard,0);setTimeout(()=>{const p=$('#chat-picks');if(p&&!p.contains(document.activeElement))p.hidden=!chatPicksShown()},150)});
// Enter sends with a keyboard; on a touch screen Enter is a new line and the button sends.
$('#suggestions').addEventListener('change',e=>{if(e.target.id!=='chat-file')return;chatAddFiles([...e.target.files]);e.target.value=''});
// A pasted screenshot or file joins the message; pasted text stays text (an Office copy carries both: the text wins)
$('#suggestions').addEventListener('paste',e=>{if(e.target.id!=='chat-input')return;const files=[...(e.clipboardData?.files||[])];if(!files.length||e.clipboardData.getData('text/plain'))return;e.preventDefault();chatAddFiles(files)});
{let depth=0;const dragged=e=>chatId&&[...(e.dataTransfer?.types||[])].includes('Files')&&e.target.closest?.('.chat-layout');
 const mark=on=>$('#suggestions .chat-layout')?.classList.toggle('chat-drop',on);
 $('#suggestions').addEventListener('dragenter',e=>{if(!dragged(e))return;e.preventDefault();depth++;mark(true)});
 $('#suggestions').addEventListener('dragover',e=>{if(!dragged(e))return;e.preventDefault();e.dataTransfer.dropEffect='copy'});
 $('#suggestions').addEventListener('dragleave',e=>{if(!dragged(e))return;if(--depth<=0){depth=0;mark(false)}});
 $('#suggestions').addEventListener('drop',e=>{if(!dragged(e))return;e.preventDefault();depth=0;mark(false);chatAddFiles([...e.dataTransfer.files])})}
// Enter sends (on a phone it's a new line, the keyboard's Send key sends), Shift+Enter is a new line, Ctrl/Cmd+Enter
// always sends. Every way goes through chatSubmit, the Send button's own path, and is handled here so the page-wide
// Ctrl+Enter (it clicks the nearest primary button) never reaches the card's Do it under the box.
$('#suggestions').addEventListener('keydown',e=>{if(e.target.id!=='chat-input'||e.key!=='Enter'||e.isComposing||e.keyCode===229||e.altKey)return;const mod=e.ctrlKey||e.metaKey;
 if(!mod&&(e.shiftKey||matchMedia('(pointer: coarse)').matches))return;e.preventDefault();chatSubmit()});
// Sends what's in the message box (and its files). A message sent while the one before it is still being saved goes
// right after it (the box is free again at once, so a quick second message is never lost or sent twice).
let chatSaving=null;
async function chatSubmit(){while(chatSaving)await chatSaving.catch(()=>{});const run=chatSubmitNow();chatSaving=run;try{await run}finally{if(chatSaving===run)chatSaving=null}}
async function chatSubmitNow(){const b=$('[data-chat-send]'),input=$('#chat-input');if(!b||b.disabled)return;const s=chatOpen(),text=input?.value.trim(),sending=chatPending.filter(f=>f.state==='ok'&&f.sid===s?.id);
 if(!s||!text&&!sending.length||chatPending.some(f=>f.state==='up')){input?.focus();return}b.disabled=true;
 // "repeat this every month", "stop repeating": set at once (todos-repeat.js), not a turn of the chat
 if(!sending.length){const rp=await repeatFromChat(s,text);if(rp){b.disabled=false;if(rp===true){input.value='';chatGrow(input);chatDraftKeep(s.id,'')}chatSendState();return}}
 const decide=args=>decidePost(s.id,args);
 // Without files a message can wait on the device while offline (decideOrWait); with files it needs the Machine now
 const steps=[...(s.status==='completed'?[{choice:'reopen',feedback:'',decision_id:crypto.randomUUID()}]:[]),{choice:'other',feedback:text,decision_id:'chat-'+crypto.randomUUID()}];
 // A message without files shows in the chat at once, while the Machine saves it; should it not take it, the message
 // goes back in the box
 const mine={kind:'you',text,at:Date.now()},drop=()=>{if(chat?.items?.includes(mine))chat={...chat,items:chat.items.filter(i=>i!==mine)}};
 if(!sending.length){input.value='';chatGrow(input);chatDraftKeep(s.id,'');chat={...(chat||{}),items:[...(chat?.items||[]),mine]};paintChat();chatToEnd()}
 try{if(!sending.length){const r=await decideOrWait(s.id,steps,'other');if(r?.waiting){drop();b.disabled=false;chatSendState();paintChat();chatToEnd();return}}
  else{for(const a of steps.slice(0,-1))await decide(a);await decide({...steps.at(-1),files:sending.map(f=>f.id)})}
  const files=sending.map(f=>({id:f.id,name:f.name,type:f.type,size:f.size}));chatDropFiles();chatTray();chatFileError('');
  if(sending.length){input.value='';chatGrow(input);chatDraftKeep(s.id,'')}drop();chat={...(chat||{}),items:[...(chat?.items||[]),{...mine,...(files.length?{files}:{})}],active:true,cursor:null};changing.delete(s.id);await refresh();paintChat();chatToEnd();chatPoll()}
 catch(err){errCaught(err);if(!sending.length){drop();const box=$('#chat-input');if(box&&!box.value){box.value=text;chatGrow(box);chatDraftKeep(s.id,text)}paintChat()}toast(err.message,true);b.disabled=false}}
// Edit on a repeating to-do's "Saved how to do this next time": its words saved in place (recurring_method_edit)
$('#suggestions').addEventListener('submit',async e=>{const f=e.target.closest('[data-recipe-form]');if(!f||!chatId)return;e.preventDefault();const b=f.querySelector('[type=submit]');b.disabled=true;
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'recurring_method_edit',args:{suggestion_id:chatId,text:f.elements.text.value}})});recipeEdit=null;toast(window.t('Saved. The next one follows it.'));if(chat)chat.cursor=null;await chatPoll()}
 catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#suggestions').addEventListener('click',async e=>{if(!chatId)return;
 const layout=e.target.closest('.chat-layout');if(e.target===layout&&chatDrawer){chatDrawer=false;layout.classList.remove('drawer');return}
 if(e.target.closest('[data-chat-drawer]')){e.target.closest('details')?.removeAttribute('open');drawerOpen();return}
 if(e.target.closest('.chat-menu-list button'))setTimeout(()=>$('#chat-menu')?.removeAttribute('open'));
 const scope=e.target.closest('.chat-side [data-scope]');if(scope){e.stopPropagation();scopeSet(scope.dataset.scope);return}
 const lg=e.target.closest('[data-learned-go],[data-learned-edit]');if(lg?.dataset.learnedNode){e.stopPropagation();recordFactShow(lg.dataset.learnedNode,Number(lg.dataset.learnedEdit)||null);return}if(lg){e.stopPropagation();const v=lg.dataset.learnedGo;lazyRun('learning',()=>lg.dataset.learnedEdit?learnedShow(Number(lg.dataset.learnedEdit),'fact',true):learnedShow(Number(v)||null,lg.dataset.what));return}
 const fu=e.target.closest('[data-fixed-undo]');if(fu){e.stopPropagation();fu.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'learning_undo',args:{id:Number(fu.dataset.fixedUndo)}})});toast(window.t('Undone.'));if(chat)chat.cursor=null;await chatPoll();refresh()}catch(err){errCaught(err);fu.disabled=false;toast(err.message,true)}return}
 const lu=e.target.closest('[data-learned-undo]');if(lu){e.stopPropagation();lu.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'forget_fact',args:{id:Number(lu.dataset.learnedUndo),undo:true}})});toast('Removed from what I’ve learned.');if(chat)chat.cursor=null;await chatPoll();refresh()}catch(err){errCaught(err);lu.disabled=false;toast(err.message,true)}return}
 if(e.target.closest('[data-recipe-edit]')){e.stopPropagation();recipeEdit=chatId;paintChat();const box=$('#recipe-text');box?.focus();box?.setSelectionRange(box.value.length,box.value.length);return}
 if(e.target.closest('[data-recipe-cancel]')){e.stopPropagation();recipeEdit=null;paintChat();return}
 const ru=e.target.closest('[data-recipe-undo]');if(ru){e.stopPropagation();ru.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'recurring_method_undo',args:{suggestion_id:chatId}})});toast(window.t('Undone.'));if(chat)chat.cursor=null;await chatPoll()}catch(err){errCaught(err);ru.disabled=false;toast(err.message,true)}return}
 const un=e.target.closest('[data-unclamp]');if(un){e.stopPropagation();const k=un.dataset.unclamp;chatOpenSet.has(k)?chatOpenSet.delete(k):chatOpenSet.add(k);paintChat();return}
 const b=e.target.closest('button');const input=$('#chat-input');
 // A quick pick or a suggestion fills the message box.
 if(b&&(b.dataset.choice==='pick'||b.dataset.chatSay!=null)&&input){e.stopPropagation();input.value=b.dataset.pick??b.dataset.chatSay;chatGrow(input);input.focus();return}
 if(e.target.closest('[data-chat-attach]')){e.stopPropagation();$('#chat-file')?.click();return}
 const rm=e.target.closest('[data-att-remove]');if(rm){e.stopPropagation();const f=chatPending.find(x=>x.key===rm.dataset.attRemove);chatPending=chatPending.filter(x=>x!==f);
  if(f?.id)request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'chat_file_remove',args:{suggestion_id:f.sid,id:f.id}})}).catch(()=>{});chatFileError('');chatTray();input?.focus();return}
 if(b?.hasAttribute('data-chat-stop')){e.stopPropagation();const s=chatOpen();if(!s)return;b.disabled=true;
  try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'chat_stop',args:{suggestion_id:s.id}})});
   if(chat)chat={...chat,active:false,live:null,cursor:null};await refresh();paintChat();chatPoll()}catch(err){errCaught(err);toast(err.message,true);b.disabled=false}return}
 if(!b?.hasAttribute('data-chat-send'))return;e.stopPropagation();chatSubmit()},true);
