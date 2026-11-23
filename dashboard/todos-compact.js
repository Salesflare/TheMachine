// One to-do on its own: <machine>/?compact=1#card=<id>, for a small window another app draws a frame around (the desktop
// robot's box). The to-do is the dashboard's own (suggestionCard, its chat, its dialogs and their checks); only the page
// around it is left out. What leads out of the to-do opens the whole dashboard, in a new window the app sends where it wants.
// The page's title says how the to-do stands, never translated: "<state>: <title>", with state one of open, done, snoozed,
// gone, offline or signed-out (GET api/session has "compact": 1). Escape closes what is open here; with nothing open it is
// left to the app. A page opened without ?compact=1 runs none of this.
let oneId='',oneKnown='',oneOut=false,oneSeen='',oneLeft=['',0];
const oneOwn=h=>h==='#card='+oneId||h==='#chat='+oneId;
const oneBack=()=>history.replaceState(history.state,'',location.pathname+location.search+(chatId===oneId?'#chat=':'#card=')+oneId);
// The whole dashboard at this address, in a new window (one per tap: a link can come by here more than once)
function oneLeave(h){const now=Date.now();if(h===oneLeft[0]&&now-oneLeft[1]<800)return;oneLeft=[h,now];open(new URL(h,document.baseURI).href,'_blank','noopener')}
function oneTitle(){const s=cardOf(oneId),down=netOut||!state.suggestions;if(!s&&!oneOut&&!down&&oneKnown!==oneId)return;
 const is=oneOut?'signed-out':down?'offline':!s?'gone':closed(s)?'done':s.status==='snoozed'?'snoozed':'open',title=is+':'+(s?' '+s.title:'');if(document.title!==title)document.title=title}
const oneLine=text=>setHTML($('#suggestions'),html`<p class="one-line" role="status">${text}</p>`);
// In place of render: the one to-do, or its chat. No list, sidebar, badge, tip, notice, presence or stored shape.
function oneDraw(){if(!state.suggestions)return;
 state.whats_new=state.notify=null;oneOut=false;scopeSync(state.locale);applyLocale(state.locale);
 const box=$('#suggestions'),s=cardOf(oneId),chat=chatOpen(),keptBack=redrawKeep();
 // Not in the list the page has: the Machine's own list first (a kept one is on screen), then an older done one
 if(!s){if(shownCached)return;if(oneId&&oneKnown!==oneId){if(doneFetch(oneId,()=>{oneKnown=oneId;render()}))return;oneKnown=oneId}}
 // Shown whole, as a link to it shows it: its summary and its draft, never behind Show more
 else if(oneSeen!==oneId){oneSeen=oneKnown=oneId;expandedBodies.add(oneId);for(const a of s.next_actions||[])expandedBodies.add('draft-'+oneId+'-'+a.revision)}
 document.body.classList.toggle('chat-open',!!chat);
 if(chat)chatMount(oneId,chatView(chat,[]));
 else{listBack();if(s)drawKept(box,looksDone(s)?lookDoneCard(s):suggestionCard(s,''));else oneLine(t('That to-do isn’t here anymore.'))}
 box.removeAttribute('aria-busy');pageMarks();keptBack();if(!oneOwn(location.hash))oneBack();oneTitle();
 if(s&&!kbLanded){kbLanded=true;requestAnimationFrame(()=>setTimeout(()=>kbLand()))}}
// What Escape closes before it is the app's: a dialog, a menu, a picker
const ONE_OPEN=['dialog[open]','.more-actions[open]','#chat-menu[open]','.row-menu','.project-picker','#share-pop','#cm-menu:not([hidden])'].join();
function oneShut(d){if(d.matches('dialog'))backCancel(d);else if('open' in d)d.open=false;else if(d.id==='cm-menu')d.hidden=true;else if(d.id==='share-pop')sharePopClose();else d.remove()}
function oneStart(){const root=document.documentElement;oneId=/^#(?:card|chat)=([a-f0-9]{16})\b/.exec(location.hash)?.[1]||'';
 root.classList.remove('compact');root.classList.add('one-todo');document.querySelector('base').target='_blank';
 render=oneDraw;pageHead=()=>{};docTitle=oneTitle;browserPane=()=>false;showSettings=tab=>oneLeave('#settings'+(tab?'/'+tab:''));
 showTab=(tab,pane)=>{if(tab!=='inbox')oneLeave('#'+tab+(pane?'='+pane:''))};
 {const go=chatGo;chatGo=id=>id===oneId?go(id):oneLeave('#chat='+id)}
 // Signed out: one line, never a sign-in page in the small window
 {const wipe=cacheGone;cacheGone=async how=>{if(how==='owner')return wipe(how);await wipe(false);oneOut=true;setTimeout(()=>{oneLine(t('Signed out. Sign in again to see your Machine.'));oneTitle()})}}
 // A link out of the to-do goes by the base's target; one to its own chat from elsewhere on the page opens it here
 addEventListener('click',e=>{const a=e.target.closest?.('a[href^="#"]'),h=a?.getAttribute('href');if(!a||h==='#')return;
  if(!oneOwn(h)){e.stopImmediatePropagation();return}
  if(a.closest('#suggestions'))return;e.preventDefault();e.stopImmediatePropagation();for(const d of document.querySelectorAll('dialog[open]'))backCancel(d);location.hash=h},true);
 // An address set by a script, or by the app: another to-do's #card= shows that one here, anything else opens outside
 const moved=e=>{const h=location.hash,m=/^#card=([a-f0-9]{16})$/.exec(h);if(oneOwn(h)||!h)return;
  if(m){for(const d of document.querySelectorAll('dialog[open]'))backCancel(d);oneId=m[1];oneOut=false;scrollTo(0,0);setTimeout(()=>render('view'));return}
  e.stopImmediatePropagation();oneBack();oneLeave(h)};
 addEventListener('popstate',moved,true);addEventListener('hashchange',moved,true);
 // A view opened by a script in place of the to-do: the same
 new MutationObserver(()=>{const inbox=$('#inbox');if(!inbox.hidden)return;const now=[...document.querySelectorAll('main>section')].find(x=>!x.hidden);
  const h=oneOwn(location.hash)||!location.hash?'#'+(now?.id||'todos'):location.hash;for(const x of document.querySelectorAll('main>section'))x.hidden=x!==inbox;oneBack();oneLeave(h)}).observe($('#inbox'),{attributes:true,attributeFilter:['hidden']});
 new MutationObserver(oneTitle).observe($('#offline-bar'),{attributes:true,attributeFilter:['hidden']});
 new MutationObserver(()=>{if(!state.suggestions&&$('#suggestions .empty'))oneTitle()}).observe($('#suggestions'),{childList:true});
 // Keys: this to-do's own (S, D, E, R) and Escape. Search, New to-do, the lists and the tabs are the whole dashboard's
 let had=false;
 addEventListener('keydown',e=>{if(e.isComposing)return;had=!!document.querySelector(ONE_OPEN);const k=e.key.toLowerCase(),mod=e.ctrlKey||e.metaKey,typing=ncTyping(e.target);
  if(mod?!e.altKey&&(k==='k'||k==='b'&&!typing):!e.altKey&&k.length===1&&!' sder'.includes(k)&&!typing)e.stopImmediatePropagation()},true);
 addEventListener('keydown',e=>{if(e.key!=='Escape'||e.isComposing||e.defaultPrevented)return;const d=[...document.querySelectorAll(ONE_OPEN)].pop(),f=e.target;
  if(d){e.preventDefault();oneShut(d)}else if(had)e.preventDefault();
  else if(f.matches?.('textarea,input')&&f.value.trim()){e.preventDefault();f.blur()}});
 render()}
if(self.COMPACT)oneStart();
