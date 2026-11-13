// The Machine slow to answer (shell-network.js, slowErr) is not a failure: said quietly, without Report a bug
function toast(text,error=false,undoId=null){if(error&&text===NET_SLOW_TEXT)error=false;const t=$('#toast');delete t.dataset.about;t.replaceChildren(undoId||error?text+' ':text,undoId?make('button',{'data-undo':undoId},'Undo'):error?make('button',{type:'button','data-bug-report':''},'Report a bug'):'');t.classList.toggle('error',error);t.classList.add('show');toastLift(t);clearTimeout(toastLiftTimer);toastLiftTimer=setTimeout(()=>{if(t.classList.contains('show'))toastLift(t)},700);  /* again once what the action changed has drawn */clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.classList.remove('show'),undoId?15000:text.length>90?9000:error?6000:2500)}
// "Hidden. {} can show it again.": {} is Settings, a link to that setting (id in SETTINGS_OF)
function toastSettings(key,id){toast(t(key,t('Settings')));
 $('#toast').replaceChildren(htmlNodes(htmlT(key,html`<a href="#settings/${SETTINGS_OF[id]}" data-settings-at="${id}">${t('Settings')}</a>`)));
 clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),8000)}
// A notice about one to-do (Sent. Moved to Done., Marked done, Snoozed: the ones with Open or Undo for it, or marked
// with data-about) goes when another to-do opens: it names no to-do, so over another one it would read as being about that one.
function toastNotAbout(id){const t=$('#toast'),b=t.querySelector('[data-toast-open],[data-undo],[data-unsnooze],[data-quick-undo],[data-move-undo]'),d=b?.dataset,about=t.dataset.about||d&&(d.toastOpen||d.undo||d.unsnooze||d.quickUndo||d.id);
 if(about&&about!==id&&!about.includes(','))t.classList.remove('show')}
async function manualRefresh(){if(manualBusy)return;manualBusy=true;newTagline();document.querySelectorAll('.refresh-tap').forEach(e=>e.classList.add('busy'));const ok=await refresh();document.querySelectorAll('.refresh-tap').forEach(e=>e.classList.remove('busy'));manualBusy=false;toast(ok?'Up to date':netSlow?NET_SLOW_TEXT:'Couldn’t refresh. Try again in a moment.',!ok)}
document.querySelectorAll('.refresh-tap').forEach(e=>{e.addEventListener('click',manualRefresh);e.addEventListener('keydown',k=>{if(k.key==='Enter'||k.key===' '){k.preventDefault();manualRefresh()}})});
// The mascot blinks now and then: its closed-eyes frame for 150ms every 4 to 9 seconds, sometimes twice. Every robot
// image whose pose has one blinks (SHUT; data-blink names it for the image's first pose), also one drawn later or that
// changes pose (the all-clear robot follows the check): the frame is looked up at each blink. Sleepy and the other moods
// have none (their eyes are shut already, or the face is the point).
// Each mascot (sidebar, phone top bar, over the cards, the empty states) on its own timer, never two at once. Not with reduced motion, in a hidden tab, while busy (refreshing) or mid-move (a hop, glance or wave below).
(()=>{const still=matchMedia('(prefers-reduced-motion: reduce)'),seen=new Map(),ready=new Map();let until=0;
 const SHUT={'brand/avatar.png':'brand/avatar-blink.png','brand/wave.webp':'brand/wave-blink.webp','brand/wave-look.webp':'brand/wave-blink.webp'};
 const off=()=>still.matches||document.hidden;
 const busy=el=>{if(el.classList.contains('busy')||el.matches('.m-hop,.m-look,.m-wave')||el.closest('[data-blink-off]'))return true;const r=el.getBoundingClientRect();return !r.width||r.bottom<=0||r.top>=innerHeight||r.right<=0||r.left>=innerWidth};  // busy, or out of sight (a closed drawer)
 // A frame is used once it has loaded (no empty flash); one that can't load is left out
 const load=src=>{if(!ready.has(src)){ready.set(src,false);const im=new Image();im.src=src;im.decode().then(()=>ready.set(src,true),()=>ready.set(src,null))}return ready.get(src)===true};
 const frameOf=(el,s,src)=>src===s.first&&el.dataset.blink||SHUT[src]||'';
 // Eyes open again only if the closed frame still shows (a redraw or a pose swap in between keeps what is there)
 const shut=(el,on)=>{const s=seen.get(el),src=el.getAttribute('src');
  if(on){const f=frameOf(el,s,src);if(!f||!load(f))return false;s.open=src;s.shut=f;el.setAttribute('src',f)}
  else if(s.shut&&src===s.shut)el.setAttribute('src',s.open);
  el.classList.toggle('blinking',on);return true};
 const plan=(el,first)=>{const s=seen.get(el);clearTimeout(s.t);if(!el.isConnected){seen.delete(el);return}if(!off())s.t=setTimeout(()=>blink(el),first?1500+Math.random()*6000:4000+Math.random()*5000)};
 const blink=el=>{if(!el.isConnected){seen.delete(el);return}const s=seen.get(el),now=performance.now();
  if(now<until+600){s.t=setTimeout(()=>blink(el),until+600-now+Math.random()*900);return}  // never two at once
  if(off()||busy(el)||!shut(el,true)){plan(el);return}
  const twice=Math.random()<.2;until=now+(twice?430:150);
  s.t=setTimeout(()=>{shut(el,false);if(!twice||off())return plan(el);s.t=setTimeout(()=>{if(off()||busy(el)||!shut(el,true))return plan(el);s.t=setTimeout(()=>{shut(el,false);plan(el)},150)},130)},150)};
 const add=el=>{if(seen.has(el))return;const src=el.getAttribute('src');seen.set(el,{first:src,open:src,shut:'',t:0});const f=frameOf(el,seen.get(el),src);if(f)load(f);plan(el,true)};
 const all=()=>{for(const [el,s] of seen){if(off()){clearTimeout(s.t);if(el.isConnected)shut(el,false)}else plan(el,true)}};
 document.addEventListener('visibilitychange',all);still.addEventListener('change',all);
 // Any robot image: one in another pose now may change into one with a frame later
 const scan=()=>document.querySelectorAll('img[data-blink],img[src^="brand/"]:not([src^="brand/app-icon"])').forEach(add);
 let queued=false;scan();new MutationObserver(()=>{if(!queued){queued=true;queueMicrotask(()=>{queued=false;scan()})}}).observe(document.body,{childList:true,subtree:true})})();
// The mascot while it works (data-look, data-hand: the first look, setting up) does one small thing every 15 to 30 seconds,
// never the same twice in a row: a hop, a glance aside (eyes and a slight tilt) or a wave (the hand's lines move, a little
// rock). One timer for the page, so a list redrawn under it does not reset it. Not with reduced motion, in a hidden tab or
// out of sight; never mid-blink.
(()=>{const still=matchMedia('(prefers-reduced-motion: reduce)'),ready=new Map();let last='',t=0,queued=false;
 // A frame that can't load (a page without it) leaves that move out, without asking for it again
 const load=src=>{if(ready.has(src))return ready.get(src);ready.set(src,false);const im=new Image();im.src=src;im.decode().then(()=>ready.set(src,true),()=>ready.set(src,null));return false};
 const pick=()=>[...document.querySelectorAll('img[data-look][data-hand]')].find(el=>{const r=el.getBoundingClientRect();return r.width&&r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth});
 // A frame goes back only if it is still showing (a redraw or a blink in between keeps what is there)
 const frame=(el,from,to)=>{if(el.isConnected&&el.getAttribute('src')===from)el.setAttribute('src',to)};
 const move=(el,kind)=>{const open=el.getAttribute('src');if(el.classList.contains('blinking')||open.includes('-blink'))return false;
  if(kind==='hop'){el.classList.add('m-hop');setTimeout(()=>el.classList.remove('m-hop'),650);return true}
  const src=el.dataset[kind==='look'?'look':'hand'];if(!load(src))return false;  // its frame loads first; the move comes a moment later
  if(kind==='look'){frame(el,open,src);el.classList.add('m-look');setTimeout(()=>{el.classList.remove('m-look');frame(el,src,open)},1100);return true}
  el.classList.add('m-wave');frame(el,open,src);setTimeout(()=>frame(el,open,src),440);for(const ms of [220,660])setTimeout(()=>frame(el,src,open),ms);
  setTimeout(()=>el.classList.remove('m-wave'),900);return true};
 const plan=ms=>{clearTimeout(t);t=setTimeout(tick,ms)};
 const tick=()=>{t=0;if(still.matches||document.hidden)return;const el=pick();if(!el)return;  // none in sight: the next redraw wakes it
  const kinds=['hop','look','wave'].filter(k=>k!==last&&(k==='hop'||ready.get(el.dataset[k==='look'?'look':'hand'])!==null)),kind=kinds[Math.random()*kinds.length|0];
  if(!kind){last='';return plan(15000)}if(!move(el,kind))return plan(2500);last=kind;plan(15000+Math.random()*15000)};
 const wake=()=>{if(t||still.matches||document.hidden)return;const el=pick();if(!el)return;load(el.dataset.look);load(el.dataset.hand);plan(6000+Math.random()*6000)};
 const reset=()=>{clearTimeout(t);t=0;wake()};
 document.addEventListener('visibilitychange',reset);still.addEventListener('change',reset);
 new MutationObserver(()=>{if(!t&&!queued){queued=true;queueMicrotask(()=>{queued=false;wake()})}}).observe(document.body,{childList:true,subtree:true});wake()})();$('#toast').onclick=async e=>{const f=e.target.closest('[data-fit-undo]');if(f){f.disabled=true;try{const y=scrollY;await graphPost('board_fit',{board_id:+f.dataset.fitBoard,undo:f.dataset.fitUndo});toast('Undone.');fitsOpen.add(+f.dataset.fitBoard);fitsGoing.clear();graphMineBoards=null;if(!$('#people').hidden){await graphPeople('',true);scrollTo({top:y})}}catch(err){errCaught(err);toast(err.message,true)}return}const u=e.target.closest('[data-unmerge]');if(u){u.disabled=true;try{await graphPost('graph_same_all',{undo:u.dataset.unmerge});toast('Split again.');if(!$('#people').hidden)await graphPeople(graphNode,true)}catch(err){errCaught(err);toast(err.message,true)}return}const un=e.target.closest('[data-unsnooze]');if(un){un.disabled=true;try{await unsnooze(un.dataset.unsnooze)}catch(err){errCaught(err);toast(err.message,true)}return}const b=e.target.closest('[data-undo]');if(!b)return;b.disabled=true;const ids=b.dataset.undo.split(',');
 try{if(ids.length===1)await saveDecision(ids[0],'undo');else{for(const id of ids)await decidePost(id,{choice:'undo',feedback:'',decision_id:crypto.randomUUID()});await refresh();toast('Reopened.')}}catch(e){errCaught(e);toast(e.message,true)}};
document.addEventListener('toggle',e=>{const id=e.target.dataset?.tech;if(id)e.target.open?openTech.add(id):openTech.delete(id)},true);
setInterval(()=>document.querySelectorAll('.elapsed[data-since]').forEach(x=>x.textContent=elapsed(x.dataset.since)),1000);
setInterval(async()=>{if(document.hidden)return;for(const id of [...new Set([...document.querySelectorAll('[data-steps],[data-peek]')].map(n=>n.dataset.steps||n.dataset.peek))].slice(0,3)){const list=document.querySelector(`[data-steps="${CSS.escape(id)}"]`);try{const p=await request('api/progress?id='+encodeURIComponent(id));if(!['starting','running'].includes(p.status)){peeks.delete(id);paintPeek(id);refresh();return}steps.set(id,p.steps);if(p.peek)peeks.set(id,{image:null,...peeks.get(id),on:true});else if(peeks.has(id)){peeks.get(id).on=false;paintPeek(id)}if(list)putIfChanged(list,stepNodes(p.steps));const slot=document.querySelector(`[data-browser="${CSS.escape(id)}"]`);if(slot)putIfChanged(slot,browserNodes(id,p.browser))}catch{}}},4000);
/* A toast can be swiped away (touch) or dragged away (mouse): sideways, or toward the edge it sits nearer (up when it
   sits at the top, down at the bottom). It follows the pointer, leaves past a third of its width (or most of its height,
   or a quick flick) and settles back when let go sooner. Going this way is the same as timing out: no Undo, the change
   stays as it is. A tap (under 8px of movement) stays a tap, so Undo and the other buttons work as before. Every toast
   on show takes the pointer on its own box (plain ones like "Saved." too, so they can be swiped); the rest of the screen
   stays as it was, and on a phone toastLift keeps it off buttons. With reduced motion it still follows the pointer, then goes or settles without the
   slide. */
function toastSwipeReset(t){t.classList.remove('dragging','leaving');t.style.transform='';t.style.opacity=''}
(()=>{const t=$('#toast'),still=matchMedia('(prefers-reduced-motion: reduce)');let d=null,swallow=0;
 // On a phone the page doesn't scroll under it (touch-action), and the drawer's edge swipe, the calendar's day swipe
 // and a row's long press don't see a swipe that starts on it
 for(const ev of ['touchstart','touchmove','touchend'])t.addEventListener(ev,e=>e.stopPropagation(),{passive:true});
 const place=(dx,out)=>{const w=t.offsetWidth||1,h=t.offsetHeight||1;t.style.transform=`translate(calc(-50% + ${dx}px),${d.top?-out:out}px)`;
  t.style.opacity=String(Math.max(.15,1-Math.max(Math.abs(dx)/w,Math.max(out,0)/(h*2))))};
 const settle=()=>{toastSwipeReset(t);clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.classList.remove('show'),t.querySelector('button')?8000:2500)};
 const leave=(dx,out)=>{clearTimeout(toastTimer);t.classList.remove('dragging');t.classList.add('leaving');const r=t.getBoundingClientRect();
  if(Math.abs(dx)>=out)t.style.transform=`translate(calc(-50% + ${Math.sign(dx)*(innerWidth/2+r.width)}px),${d.top?-Math.max(out,0):Math.max(out,0)}px)`;
  else t.style.transform=`translate(calc(-50% + ${dx}px),${d.top?-(r.bottom+16):innerHeight-r.top+16}px)`;
  t.style.opacity='0';setTimeout(()=>{if(!t.classList.contains('leaving'))return;t.classList.remove('show');toastSwipeReset(t)},still.matches?0:210)};  // a new toast meanwhile stays
 t.addEventListener('pointerdown',e=>{d=null;if(!t.classList.contains('show')||t.classList.contains('leaving')||e.button>0||!e.isPrimary)return;
  const r=t.getBoundingClientRect();d={id:e.pointerId,x:e.clientX,y:e.clientY,on:false,top:r.top+r.height/2<innerHeight/2,dx:0,out:0,v:0,at:e.timeStamp}});
 // moves and the release are followed on the whole page: a quick mouse drag leaves the toast before it counts as one
 addEventListener('pointermove',e=>{if(!d||e.pointerId!==d.id)return;const dx=e.clientX-d.x,dy=e.clientY-d.y;
  if(!d.on){if(Math.hypot(dx,dy)<8)return;d.on=true;try{t.setPointerCapture(e.pointerId)}catch{}t.classList.add('dragging');clearTimeout(toastTimer)}
  e.preventDefault();const raw=d.top?-dy:dy,out=raw>0?raw:raw*.2,dt=Math.max(1,e.timeStamp-d.at);  // toward its own edge freely; the other way only a little
  d.v=Math.max(Math.abs(dx-d.dx),out-d.out)/dt;d.dx=dx;d.out=out;d.at=e.timeStamp;place(dx,out)},true);
 const up=e=>{if(!d||e.pointerId!==d.id)return;const g=d;if(!g.on){d=null;return}swallow=e.timeStamp;  // the click after a drag is no tap
  const w=t.offsetWidth,h=t.offsetHeight,far=Math.abs(g.dx)>w/3||g.out>h*.8,flick=g.v>.6&&(Math.abs(g.dx)>24||g.out>16);
  if(e.type!=='pointercancel'&&(far||flick))leave(g.dx,g.out);else settle();d=null};
 addEventListener('pointerup',up,true);addEventListener('pointercancel',up,true);
 // a new toast while one is leaving or held shows as usual, in its place
 new MutationObserver(()=>{if(t.classList.contains('leaving')||d?.on){d=null;toastSwipeReset(t)}}).observe(t,{childList:true});
 addEventListener('click',e=>{if(swallow&&e.timeStamp-swallow<400){e.stopImmediatePropagation();e.preventDefault()}swallow=0},true)})();
