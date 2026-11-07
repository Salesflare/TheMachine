function toast(text,error=false,undoId=null){const t=$('#toast');t.replaceChildren(undoId||error?text+' ':text,undoId?make('button',{'data-undo':undoId},'Undo'):error?make('button',{type:'button','data-bug-report':''},'Report a bug'):'');t.classList.toggle('error',error);t.classList.add('show');toastLift(t);clearTimeout(toastLiftTimer);toastLiftTimer=setTimeout(()=>{if(t.classList.contains('show'))toastLift(t)},700);  /* again once what the action changed has drawn */clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.classList.remove('show'),undoId?15000:text.length>90?9000:error?6000:2500)}
async function manualRefresh(){if(manualBusy)return;manualBusy=true;newTagline();document.querySelectorAll('.refresh-tap').forEach(e=>e.classList.add('busy'));const ok=await refresh();document.querySelectorAll('.refresh-tap').forEach(e=>e.classList.remove('busy'));manualBusy=false;toast(ok?'Up to date':'Couldn’t refresh. Try again in a moment.',!ok)}
document.querySelectorAll('.refresh-tap').forEach(e=>{e.addEventListener('click',manualRefresh);e.addEventListener('keydown',k=>{if(k.key==='Enter'||k.key===' '){k.preventDefault();manualRefresh()}})});
// The mascot blinks now and then: its closed-eyes frame (data-blink) for 150ms every 4 to 9 seconds, sometimes twice.
// Each mascot (sidebar, phone top bar, over the cards) on its own timer, never two at once. Not with reduced motion, in a hidden tab, while busy (refreshing) or mid-move (a hop, glance or wave below).
(()=>{const still=matchMedia('(prefers-reduced-motion: reduce)'),seen=new Map();let until=0;
 const off=()=>still.matches||document.hidden;
 const busy=el=>{if(el.classList.contains('busy')||el.matches('.m-hop,.m-look,.m-wave')||el.closest('[data-blink-off]'))return true;const r=el.getBoundingClientRect();return !r.width||r.bottom<=0||r.top>=innerHeight||r.right<=0||r.left>=innerWidth};  // busy, or out of sight (a closed drawer)
 const shut=(el,on)=>{const s=seen.get(el);if(s.shut){const src=el.getAttribute('src');if(on&&src!==s.open)return false;if(src===(on?s.open:s.shut))el.setAttribute('src',on?s.shut:s.open)}el.classList.toggle('blinking',on);return true};
 const plan=(el,first)=>{const s=seen.get(el);clearTimeout(s.t);if(!el.isConnected){seen.delete(el);return}if(!off())s.t=setTimeout(()=>blink(el),first?1500+Math.random()*6000:4000+Math.random()*5000)};
 const blink=el=>{if(!el.isConnected){seen.delete(el);return}const s=seen.get(el),now=performance.now();
  if(now<until+600){s.t=setTimeout(()=>blink(el),until+600-now+Math.random()*900);return}  // never two at once
  if(off()||busy(el)||!shut(el,true)){plan(el);return}
  const twice=Math.random()<.2;until=now+(twice?430:150);
  s.t=setTimeout(()=>{shut(el,false);if(!twice||off())return plan(el);s.t=setTimeout(()=>{if(off()||busy(el)||!shut(el,true))return plan(el);s.t=setTimeout(()=>{shut(el,false);plan(el)},150)},130)},150)};
 const add=el=>{if(seen.has(el))return;const shutSrc=el.dataset.blink,s={open:el.getAttribute('src'),shut:shutSrc||'',t:0};seen.set(el,s);
  if(!shutSrc)return plan(el,true);const im=new Image();im.src=shutSrc;im.decode().then(()=>{s.ready=true;plan(el,true)},()=>{})};
 const all=()=>{for(const [el,s] of seen)if(!s.shut||s.ready){if(off()){clearTimeout(s.t);if(el.isConnected)shut(el,false)}else plan(el,true)}};
 document.addEventListener('visibilitychange',all);still.addEventListener('change',all);
 const scan=()=>document.querySelectorAll('[data-blink]').forEach(add);
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
  el.classList.add('m-wave');for(const ms of [0,440])setTimeout(()=>frame(el,open,src),ms);for(const ms of [220,660])setTimeout(()=>frame(el,src,open),ms);
  setTimeout(()=>el.classList.remove('m-wave'),900);return true};
 const plan=ms=>{clearTimeout(t);t=setTimeout(tick,ms)};
 const tick=()=>{t=0;if(still.matches||document.hidden)return;const el=pick();if(!el)return;  // none in sight: the next redraw wakes it
  const kinds=['hop','look','wave'].filter(k=>k!==last&&(k==='hop'||ready.get(el.dataset[k==='look'?'look':'hand'])!==null)),kind=kinds[Math.random()*kinds.length|0];
  if(!kind){last='';return plan(15000)}if(!move(el,kind))return plan(2500);last=kind;plan(15000+Math.random()*15000)};
 const wake=()=>{if(t||still.matches||document.hidden)return;const el=pick();if(!el)return;load(el.dataset.look);load(el.dataset.hand);plan(6000+Math.random()*6000)};
 const reset=()=>{clearTimeout(t);t=0;wake()};
 document.addEventListener('visibilitychange',reset);still.addEventListener('change',reset);
 new MutationObserver(()=>{if(!t&&!queued){queued=true;queueMicrotask(()=>{queued=false;wake()})}}).observe(document.body,{childList:true,subtree:true});wake()})();$('#toast').onclick=async e=>{const f=e.target.closest('[data-fit-undo]');if(f){f.disabled=true;try{const y=scrollY;await graphPost('board_fit',{board_id:+f.dataset.fitBoard,undo:f.dataset.fitUndo});toast('Undone.');fitsOpen.add(+f.dataset.fitBoard);graphMineBoards=null;if(!$('#people').hidden){await people('',true);scrollTo({top:y})}}catch(err){errCaught(err);toast(err.message,true)}return}const u=e.target.closest('[data-unmerge]');if(u){u.disabled=true;try{await graphPost('graph_same_all',{undo:u.dataset.unmerge});toast('Split again.');if(!$('#people').hidden)await people(graphNode,true)}catch(err){errCaught(err);toast(err.message,true)}return}const un=e.target.closest('[data-unsnooze]');if(un){un.disabled=true;try{await unsnooze(un.dataset.unsnooze)}catch(err){errCaught(err);toast(err.message,true)}return}const b=e.target.closest('[data-undo]');if(!b)return;b.disabled=true;const ids=b.dataset.undo.split(',');
 try{if(ids.length===1)await saveDecision(ids[0],'undo');else{for(const id of ids)await decidePost(id,{choice:'undo',feedback:'',decision_id:crypto.randomUUID()});await refresh();toast('Reopened.')}}catch(e){errCaught(e);toast(e.message,true)}};
document.addEventListener('toggle',e=>{const id=e.target.dataset?.tech;if(id)e.target.open?openTech.add(id):openTech.delete(id)},true);
setInterval(()=>document.querySelectorAll('.elapsed[data-since]').forEach(x=>x.textContent=elapsed(x.dataset.since)),1000);
setInterval(async()=>{if(document.hidden)return;for(const id of [...new Set([...document.querySelectorAll('[data-steps],[data-peek]')].map(n=>n.dataset.steps||n.dataset.peek))].slice(0,3)){const list=document.querySelector(`[data-steps="${CSS.escape(id)}"]`);try{const p=await request('api/progress?id='+encodeURIComponent(id));if(!['starting','running'].includes(p.status)){peeks.delete(id);paintPeek(id);refresh();return}steps.set(id,p.steps);if(p.peek)peeks.set(id,{image:null,...peeks.get(id),on:true});else if(peeks.has(id)){peeks.get(id).on=false;paintPeek(id)}if(list)putIfChanged(list,stepNodes(p.steps));const slot=document.querySelector(`[data-browser="${CSS.escape(id)}"]`);if(slot)putIfChanged(slot,browserNodes(id,p.browser))}catch{}}},4000);
