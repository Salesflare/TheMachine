// The page's own script came (dashboard.html shows "The page didn’t load" otherwise), also when it came late
self.appStarted=true;document.getElementById('load-failed')?.setAttribute('hidden','');
// Dates and times follow Settings, General (locale_prefs.py): DL is the date locale (Sat, Oct 24 or Sat 24 Oct), H12 the
// clock (2:05 PM or 14:05). A Machine without a region keeps US dates and 24-hour times.
let DL='en-US',H12=false;
const applyLocale=l=>{if(!l)return;DL=l.date_locale||'en-US';H12=!!l.hour12;if(typeof i18nApply==='function')i18nApply(l)};
// toLocaleDateString and toLocaleTimeString make a new formatter on every call (a fraction of a millisecond each, and a
// list stamps hundreds of times): localeDate and localeTime give the same text from one kept formatter per locale and
// options, with the same defaults (a date with no date part shows year, month and day; a time hour, minute and second).
const LOCALE_FMT=new Map(),LOCALE_DATE=['weekday','year','month','day'],LOCALE_TIME=['dayPeriod','hour','minute','second','fractionalSecondDigits'];
function localeFmt(v,loc,o,time){const d=v instanceof Date?v:new Date(v);if(isNaN(d))return String(d);  /* the browser's own words for a date that isn't one */o=o||{};
 if(!o.dateStyle&&!o.timeStyle&&!(time?LOCALE_TIME:LOCALE_DATE).some(k=>o[k]!==undefined))o={...o,...(time?{hour:'numeric',minute:'numeric',second:'numeric'}:{year:'numeric',month:'numeric',day:'numeric'})};
 const key=(loc||'')+'|'+JSON.stringify(o);let f=LOCALE_FMT.get(key);if(!f){if(LOCALE_FMT.size>500)LOCALE_FMT.clear();f=new Intl.DateTimeFormat(loc,o);LOCALE_FMT.set(key,f)}return f.format(d)}
const localeDate=(v,loc,o)=>localeFmt(v,loc,o,false),localeTime=(v,loc,o)=>localeFmt(v,loc,o,true);
const fmtHM=(v,o)=>localeTime(v,H12?'en-US':'en-GB',{...(H12?{hour:'numeric',minute:'2-digit',hour12:true}:{hour:'2-digit',minute:'2-digit',hourCycle:'h23'}),...o});
const fmtDHM=(v,d,o)=>localeDate(v,DL,{...d,...o})+', '+fmtHM(v,o);  // Sat, Oct 24, 14:05
let snoozeId=null,snoozeDay=null,snoozeMonth=null,lastOk=0,refreshFailed=false;
const localDay=d=>[d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-');
let state={};  // csrf, UI_VERSION and CACHE_SCOPE: the page's own script before this one (dashboard.html)
// Selectors an older browser rejects with a SyntaxError (:modal, :focus-visible): asked here, with a fallback.
const modalOpen=()=>{try{return!!document.querySelector('dialog[open]:modal')}catch{return!!document.querySelector('dialog[open]')}};
const focusVisible=el=>{try{return el.matches(':focus-visible')}catch{return el.matches(':focus')}};
// Error reports (error_feed.py): an error in this page's own code goes to the service as its type, message and place
// (function and line); the service normalizes it again and keeps only a signature. Never what the page shows. A repeat
// within a minute only counts once, at most 20 a page, and nothing when the owner turned reports off in Settings.
// Three ways in: what reaches window.onerror or goes unhandled; a bug in this page's code that a try caught and showed
// as a toast or notice (errCaught: most of the page runs inside one, so without it a render bug was never reported);
// and from the service worker (sw.js), its own errors and a failed shell update. And a failed API call as a signature
// of its own (errApi): the endpoint (and the action's name), a 5xx the Machine answered or a timeout, never the query
// or what was sent. Not reported: the Machine being away, restarting or signed out, and a 4xx (a refusal, not a bug).
const errSeen=new Map();let errQueue=[],errTimer=0,errCount=0;
function errPlace(stack){for(const l of String(stack||'').split('\n')){const m=l.match(/^\s*(?:at\s+(?:(.*?)\s+\()?|(.*?)@)(\S+?):(\d+):\d+\)?\s*$/);
 if(!m||!m[3].startsWith(location.origin))continue;return{file:/\/sw\.js(?:[?#]|$)/.test(m[3])?'sw.js':'dashboard.html',function:String(m[1]||m[2]||'<anonymous>').split(/[\s.]/).pop().slice(0,60)||'<anonymous>',line:+m[4]}}return null}
function errPush(item,key){if(errCount>=20||state.team_learnings?.errors===false)return;const now=Date.now();
 if(now-(errSeen.get(key)||0)<60000)return;errSeen.set(key,now);errCount++;errQueue.push(item);
 clearTimeout(errTimer);errTimer=setTimeout(()=>{const errors=errQueue.splice(0,10);if(errors.length)request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'client_error',args:{errors}})}).catch(()=>{})},2000)}
function errReport(e,kind){try{if(!(e instanceof Error)||e.offline||e.sessionGone||e.status||e.name==='AbortError')return;const at=errPlace(e.stack);if(!at)return;
 const item={kind:String(kind||e.name||'Error').slice(0,60),message:String(e.message||'').slice(0,500),...at};errPush(item,item.kind+'|'+item.function+'|'+item.line+'|'+item.message)}catch{}}
// A caught error is a bug only as one of these (a selector the page built wrong is a DOMException named SyntaxError);
// a thrown Error is the page's own message to the owner, and a fetch that failed is the network.
const ERR_BUGS=/^(?:Type|Reference|Range|Syntax|URI|Eval|Internal)Error$/;
function errCaught(e){try{if(e instanceof Error&&ERR_BUGS.test(e.name)&&!/^(Failed to fetch|NetworkError|Load failed)/.test(e.message))errReport(e)}catch{}}
function errApi(path,options,status){try{const p=String(path||'').split(/[?#]/)[0].replace(/^\.?\//,'');if(!p.startsWith('api/'))return;let action='';
 if(p==='api/action')try{action=String(JSON.parse(options?.body||'{}').action||'').slice(0,60)}catch{}
 if(action==='client_error')return;errPush({api:p.slice(4,124),action,status},'api|'+p+'|'+action+'|'+status)}catch{}}
function errSw(x){try{if(x&&typeof x==='object')errPush({kind:String(x.kind||'Error').slice(0,60),message:String(x.message||'').slice(0,500),file:'sw.js',function:String(x.function||'<anonymous>').slice(0,60),line:+x.line||0},
 'sw|'+x.kind+'|'+x.function+'|'+x.message)}catch{}}
addEventListener('error',e=>errReport(e.error));
addEventListener('unhandledrejection',e=>errReport(e.reason,e.reason instanceof Error?e.reason.name:''));
navigator.serviceWorker?.addEventListener('message',e=>errSw(e.data?.swError));
const $=s=>document.querySelector(s);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
// An element built from parts, never parsed from markup: text children become text nodes, attributes are set one by
// one (`class`, or `style` as an object). Empty, null and false children are left out; an array's items are children.
const make=(tag,attrs={},...kids)=>{const e=document.createElement(tag);for(const [k,v] of Object.entries(attrs))k==='class'?e.className=v:k==='style'?Object.assign(e.style,v):e.setAttribute(k,v);
 for(const k of kids.flat())if(k!==''&&k!=null&&k!==false)e.appendChild(k instanceof Node?k:document.createTextNode(String(k)));return e};
// Puts nodes in el only when `key` (what they say) changed since the last time, so a redraw keeps focus and open state
const putOnce=(el,key,nodes)=>{if(el.dataset.shown!==key){el.replaceChildren(...nodes());el.dataset.shown=key}};
// Puts nodes in el only when they differ from what it shows, so a poll that brings the same thing changes nothing
const putIfChanged=(el,nodes)=>{const w=make('div',{},nodes);if(el.innerHTML!==w.innerHTML)el.replaceChildren(...w.childNodes)};
// Markup that escapes by construction: in html`...` every ${} is escaped (as esc() does) unless it is itself an html``
// result, or raw() of a vetted constant (raw() is for constants in this file only, never for data); an array's items
// are joined the same way. setHTML is the one innerHTML write for it and takes nothing else, so a forgotten esc() can no
// longer put someone's text into the page as markup. Escaping doesn't make a link safe: every href and src that comes
// from data goes through safeHref. htmlT is t() for a sentence whose {} holds markup (a <time>, a button).
class SafeHTML{constructor(s){this.s=s}toString(){return this.s}}
const raw=s=>new SafeHTML(String(s));
const htmlPart=v=>v instanceof SafeHTML?v.s:Array.isArray(v)?v.map(htmlPart).join(''):esc(v);
const html=(parts,...vals)=>new SafeHTML(parts.reduce((o,p,i)=>o+htmlPart(vals[i-1])+p));
const setHTML=(el,h)=>{if(h==='')return el.replaceChildren();if(!(h instanceof SafeHTML))throw new TypeError('setHTML takes html`` results only');el.innerHTML=h.s};  // '' empties it
// A loading line or busy label shows only for an answer that takes a moment: lateShow(fn) runs fn after 120 ms, and
// the returned function, called when the answer is in, cancels it (what was on screen stays meanwhile).
const LOADING_MS=120,lateShow=fn=>{const t=setTimeout(fn,LOADING_MS);return ()=>clearTimeout(t)};
const htmlNodes=h=>{const t=document.createElement('template');setHTML(t,h);return t.content};  // for append, before, replaceWith
// setHTML for a list that redraws on every poll: a node whose markup is the same as last time stays, keyed by its id
// (else by its place), so focus, a text selection, an open menu, a button's in-flight state and the scroll all stay.
// Only what changed is swapped. A <details> list is kept and its rows go the same way. A time that only says
// "2 minutes ago" now is updated in place. A node under a pointer or key that's still down isn't swapped or removed
// until it's let go, so the click lands; then `again` draws once more.
const drawnHTML=new WeakMap(),agoFree=s=>s.replace(/(<(?:time|span class="elapsed")\b[^>]*>)[^<]*/g,'$1');
let pressedNode=null,pressedAgain=null;
addEventListener('pointerdown',e=>{pressedNode=e.target},true);
addEventListener('keydown',e=>{if((e.key===' '||e.key==='Enter')&&e.target.closest?.('button,summary,a,[role=button]'))pressedNode=e.target},true);
const pressLetGo=()=>{pressedNode=null;const again=pressedAgain;pressedAgain=null;if(again)setTimeout(again)};  // after the click it makes
for(const type of ['pointerup','pointercancel','keyup','dragend'])addEventListener(type,pressLetGo,true);
addEventListener('blur',e=>{if(e.target===window)pressLetGo()});
const pressedIn=(node,again)=>{if(!pressedNode||!node.contains?.(pressedNode))return false;pressedAgain=again;return true};
function drawKept(box,h,again){if(h==='')h=html``;keptKids(box,htmlNodes(h),again)}
// A <details> list drawn new: its rows are marked as drawn too, so the next redraw keeps the ones that stayed the same
function drawnMark(n,src){drawnHTML.set(n,src);if(n.tagName==='DETAILS')for(const c of n.children)drawnMark(c,c.outerHTML)}
// What someone has open or in hand in a node a redraw swaps goes over to the new one: its open menus, where they opened,
// and the focused control. Each is found again in the new node as the same thing (its kind, its label or its words, the
// how-many-th of those), so a chip or line that came or went next to it doesn't matter. Focus in a menu stays on its item.
const MENUS='details.fact-menu,details.more-actions,details.tile-menu,details.board-menu,details.graph-sort';
const MENUS_OPEN=MENUS.split(',').map(m=>m+'[open]').join(',');
const keptSig=x=>x.tagName+'.'+x.className+'|'+(x.matches('details')?x.querySelector(':scope>summary')?.getAttribute('aria-label'):x.textContent.trim());
const keptAll=(n,x)=>{const sig=keptSig(x),all=[...n.querySelectorAll(x.tagName)];if(n.tagName===x.tagName)all.unshift(n);return all.filter(y=>keptSig(y)===sig)};  // its kind in n, in order
// withMenus=false: only the focus, and not on an item in a menu (a page drawn again after a menu's action: that menu is done)
function heldTake(o,withMenus=true){if(o?.nodeType!==1)return null;const f=document.activeElement,menus=withMenus?[...o.querySelectorAll(MENUS_OPEN)]:[];if(withMenus&&o.matches(MENUS_OPEN))menus.unshift(o);
 const focus=f&&f!==o&&o.contains(f)&&(withMenus||f.matches('summary')||!f.closest(MENUS))?f:null;if(!menus.length&&!focus)return null;
 return {menus:menus.map(d=>({d,nth:keptAll(o,d).indexOf(d),style:d.querySelector(':scope>:not(summary)')?.getAttribute('style')})),focus,fnth:focus&&keptAll(o,focus).indexOf(focus)}}
// A menu opened again here keeps the side it opened on: menuKept tells the toggle handler (graph-shared.js) not to place
// it anew from the page as it is now, which flipped it above its ⋯ when the page had moved since it opened.
const menuKept=new WeakSet();
function heldPut(n,h){if(!h||n?.nodeType!==1)return;
 for(const m of h.menus){const d=keptAll(n,m.d)[m.nth];if(!d)continue;const l=d.querySelector(':scope>:not(summary)');if(l&&m.style)l.setAttribute('style',m.style);if(!d.open){menuKept.add(d);d.open=true}}
 const x=h.focus&&keptAll(n,h.focus)[h.fnth];if(x)x.focus({preventScroll:true})}
function keptKids(box,from,again){const kids=[...from.childNodes],ids=new Set(kids.map(n=>n.id).filter(Boolean)),byId=new Map(),used=new Set();
 for(const o of box.children)if(o.id&&!byId.has(o.id))byId.set(o.id,o);
 const stays=o=>!o.id||ids.has(o.id)&&byId.get(o.id)===o&&!used.has(o);  // a node with an id the new markup doesn't have goes: never moved around
 let at=box.firstChild;
 for(const n of kids){const el=n.nodeType===1,src=el?n.outerHTML:null;while(at&&!stays(at))at=at.nextSibling;
  let o=el&&n.id?byId.get(n.id):null;if(o&&(used.has(o)||o.tagName!==n.tagName))o=null;
  if(!o&&at&&!(at.nodeType===1&&at.id)&&!(el&&n.id)&&at.nodeType===n.nodeType&&(el?drawnHTML.get(at)===src:at.nodeValue===n.nodeValue))o=at;  // no id: the same thing in the same place
  let put=n;
  if(o){const was=drawnHTML.get(o);
   if(!el||was===src)put=o;
   else if(was!=null&&agoFree(was)===agoFree(src)){const fresh=n.querySelectorAll('time,.elapsed');o.querySelectorAll('time,.elapsed').forEach((x,i)=>{const y=fresh[i];if(y&&x.textContent!==y.textContent&&(x.getAttribute('datetime')||x.dataset.since)===(y.getAttribute('datetime')||y.dataset.since))x.textContent=y.textContent});drawnHTML.set(o,src);put=o}
   else if(n.tagName==='DETAILS'){for(const a of [...o.attributes])if(!n.hasAttribute(a.name))o.removeAttribute(a.name);for(const a of n.attributes)if(o.getAttribute(a.name)!==a.value)o.setAttribute(a.name,a.value);
    drawnHTML.set(o,src);keptKids(o,n,again);put=o}
   else if(typedKept(o,n,src))put=o
   else if(pressedIn(o,again))put=o}  // swapped once it's let go
  if(put===n&&el)drawnMark(n,src);
  if(o&&put===n){const h=heldTake(o);o.replaceWith(n);heldPut(n,h);if(at===o)at=n}  // swapped where it stood, so nothing after it moves
  used.add(put);if(put===at)at=at.nextSibling;else box.insertBefore(put,at)}
 for(const o of [...box.childNodes])if(!used.has(o)&&!pressedIn(o,again))o.remove()}
// The field someone is typing in is never swapped for a copy, even when what's around it changed (a status line, a
// note): on a phone a new field starts a new keyboard session, and spell check and suggestions drop out for a moment.
// Everything around it is redrawn from the new markup; the field itself (text, caret, keyboard state) stays. Only when
// the new markup has the same field (same id and tag) on the same path; otherwise the node is swapped as before.
function typedKept(o,n,src){const f=document.activeElement;if(!f?.id||f===o||!o.contains(f)||!f.matches(TYPED))return false;
 const g=n.querySelector('#'+CSS.escape(f.id));if(!g||g.tagName!==f.tagName)return false;
 const up=(x,top)=>{const p=[];for(;x!==top;x=x.parentNode)p.push(x);return p},fs=up(f,o),gs=up(g,n);
 if(fs.length!==gs.length||fs.some((x,i)=>x.tagName!==gs[i].tagName))return false;
 const attrs=(x,y)=>{for(const a of [...x.attributes])if(!y.hasAttribute(a.name))x.removeAttribute(a.name);for(const a of y.attributes)if(x.getAttribute(a.name)!==a.value)x.setAttribute(a.name,a.value)};
 attrs(o,n);for(let i=fs.length-1;i>=0;i--){const x=fs[i],y=gs[i],xp=fs[i+1]||o,yp=gs[i+1]||n;
  for(const c of [...xp.childNodes])if(c!==x)c.remove();const ys=[...yp.childNodes],at=ys.indexOf(y);x.before(...ys.slice(0,at));x.after(...ys.slice(at+1));
  if(x!==f)attrs(x,y)}
 drawnHTML.set(o,src);return true}
// A change to built markup goes through the DOM: the parsed copy, changed with DOM calls, written back by the browser.
const htmlEdit=(h,f)=>{const t=document.createElement('template');setHTML(t,h);f(t.content);return new SafeHTML(t.innerHTML)};
// Nodes already on the page or parsed from html``, written out again by the browser (an element whole, a text node escaped)
const nodeHTML=(...ns)=>new SafeHTML(ns.map(n=>!n?'':n.nodeType===1?n.outerHTML:n.nodeType===3?esc(n.data):'').join(''));
const orEmpty=h=>String(h)?h:'';  // '' stays falsy
// A setting this Machine can't save (it runs without a settings file): plain words first, the file and its key under
// Show more for whoever wants them
const CANT_SAVE='This can’t be changed on this Machine.';
const cantSaveMore=key=>html`<details class="tech cant-save"><summary>Show more</summary><p>${t('Set in config.json ({}) on this computer.',key)}</p></details>`;
const htmlT=(key,...a)=>{const tok=i=>`\u0000${i}\u0000`;let s=esc(t(key,...a.map((v,i)=>v instanceof SafeHTML?tok(i):v)));a.forEach((v,i)=>{if(v instanceof SafeHTML)s=s.split(tok(i)).join(v.s)});return new SafeHTML(s)};
// A link from data: web, mail and phone links and this page's own (relative or same origin) stay; anything else
// (javascript:, data:, a broken address) becomes '#'. safeURL in todos-cards.js is stricter: http(s) only, '' otherwise.
const safeHref=(u,base=location.href)=>{const v=String(u??'').trim();if(!v)return '#';try{const x=new URL(v,base);return ['http:','https:','mailto:','tel:'].includes(x.protocol)?v:'#'}catch{return '#'}};
const date=v=>v?fmtDHM(v,{month:'short',day:'numeric',year:'numeric'}):t('Not yet');
// Parts that load when first needed (dashboard_parts.py LAZY), named in LAZY_FILES. The page is drawn without them;
// once drawn whole and idle after the load event, lazySoon() fetches them one at a time, each once the browser is idle
// again, so they never slow the start (all at once, they took the connections the page's data waited for). A tab
// opened before its part is in asks for it at once (lazyPart). A page with every part inline (tests, the demo) has none
// to load. lazyPart(group): its file, loaded once (a failed load is tried again on the next call). lazyIn(group): it's
// there (or has no file). lazyRun(group,fn): fn now when it's there, else once it is, and once only: each to-do that
// needs a part asks for a redraw on every draw, which queued 60 to 80 whole redraws on a first load.
const lazyLoads={},lazyDone={},lazyWait={};let lazyAllRun=null,lazySoonRun=false;
function lazyPart(group){const file=self.LAZY_FILES?.[group];if(!file||lazyDone[group])return Promise.resolve();
 // a load that fails while the Machine restarts (seconds: unreachable or a 502-504) is tried again for a while before it says Offline
 return lazyLoads[group]??=new Promise((ok,fail)=>{const until=Date.now()+45000,no=()=>{delete lazyLoads[group];fail(new Error(t('Offline.')))},
  again=()=>navigator.onLine!==false&&Date.now()<until?setTimeout(load,3000):no(),
  load=()=>{const s=document.createElement('script');s.src=file;s.onload=()=>{lazyDone[group]=true;ok()};
  s.onerror=()=>{s.remove();fetch(file,{cache:'no-store'}).then(r=>r.status>=502&&r.status<=504?again():no(),again)};document.head.append(s)};load()})}
const lazyIdle=()=>new Promise(r=>self.requestIdleCallback?requestIdleCallback(r,{timeout:3000}):setTimeout(r,200));
const lazyAll=()=>lazyAllRun??=(async()=>{for(const group of Object.keys(self.LAZY_FILES||{})){await lazyIdle();await lazyPart(group).catch(()=>{})}})();
function lazySoon(){if(lazySoonRun||!self.LAZY_FILES)return;lazySoonRun=true;let gone=false;
 const go=()=>{if(gone)return;gone=true;self.requestIdleCallback?requestIdleCallback(()=>lazyAll(),{timeout:2000}):setTimeout(lazyAll,200)};
 if(document.readyState==='complete')go();else{addEventListener('load',go,{once:true});setTimeout(go,5000)}}
addEventListener('popstate',e=>backPop(e));  // shell-back.js
const lazyIn=group=>!self.LAZY_FILES?.[group]||!!lazyDone[group];
function lazyRun(group,fn){if(lazyIn(group))return fn();const w=lazyWait[group]??=new Set;if(w.has(fn))return;w.add(fn);lazyPart(group).then(fn,e=>toast(e.message,true)).finally(()=>w.delete(fn))}
