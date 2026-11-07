const showNote=r=>r.shown?(r.opened?'Opened it again in your Machine’s browser.':'It’s in front in your Machine’s browser.'):r.unknown?'I don’t know which page this task used.':r.error||'I couldn’t reach the browser.';
document.addEventListener('click',async e=>{const b=e.target.closest('[data-browser-show]');if(!b)return;const link=state.browser_link;if(!link||!(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)&&browserPane())e.preventDefault();try{const r=await browserShow(b.dataset.browserShow);if(!link||!r.shown)toast(showNote(r),!r.shown)}catch(err){errCaught(err);toast(err.message,true)}});
{const m=/^#browser-for=([a-f0-9]{16})$/.exec(location.hash);if(m){history.replaceState(null,'',location.pathname);browserShow(m[1]).then(r=>{if(r.view&&r.shown){if(!browserPane())location.assign(r.view)}else toast(showNote(r),!r.shown)},err=>toast(err.message,true))}}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-browser-focus]');if(!b)return;if(b.href&&!(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)&&browserPane())e.preventDefault();  /* on a computer: the Browser pane, as the sign-in dialog's Open the browser */b.disabled=true;try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'browser_focus',args:b.dataset.task?{suggestion_id:b.dataset.task}:{page:b.dataset.page||null}})});if(!('quiet' in b.dataset)||!r.shown)toast(r.shown?'The browser is in front now.':r.unknown?'I don’t know which tab this task uses; find it in the browser.':'I couldn’t reach the browser on this computer.',!r.shown)}catch(err){errCaught(err);if(!('quiet' in b.dataset))toast(err.message,true)}finally{b.disabled=false}});
const canRefresh=()=>!document.hidden&&!document.querySelector('textarea:focus')&&!$('#snooze-dialog').open&&!$('#result-dialog').open&&!$('#email-dialog').open&&!$('#send-dialog').open;
const refreshWhenReady=()=>{if(placeBusy()){clearTimeout(refreshWhenReady.t);refreshWhenReady.t=setTimeout(refreshWhenReady,800);return}if(canRefresh()&&!refreshes)refresh(true)};  // not under a moving finger; a poll, so the Graph tab redraws at most once a minute (GRAPH_POLL_MS)
// Return from another app, a suspended phone tab or an outage: update connection warnings immediately.
document.addEventListener('visibilitychange',()=>{if(document.hidden)updateMaybe();else{lastInput=Date.now();refreshWhenReady()}});setInterval(updateMaybe,15e3);
for(const b of document.querySelectorAll('[data-update-ready]'))b.addEventListener('click',()=>{updateWaiting=false;updateNow()});
addEventListener('pageshow',e=>{if(e.persisted)refreshWhenReady()});  // back from the page cache only: the first load has its own refresh, and a second one could undo a change made meanwhile
addEventListener('online',refreshWhenReady);
// A tapped notification's view opens at once, before the status comes in (that can take a while): the Calendar, To-dos and
// the Fleet tab load their own data. Then the cards this device kept last time (if any) while the live ones load.
if(openPushLink()){openTabLink();openFleetLink()}  // only a notification's own view: other links wait for the status as before
sessionCheck();
if(localCache.on)localCache.read('status').then(hit=>{if(!hit||state.suggestions)return;state=wakeSnoozed(hit.value);shownCached=true;shownAt=hit.at;
 try{cardsMerge();render();openChatLink();openTabLink()}catch(e){errCaught(e);console.error(e)}});
refresh().then(()=>{newTagline();updateViewBack();if(localCache.on&&'serviceWorker' in navigator)navigator.serviceWorker.register('sw.js').then(()=>navigator.serviceWorker.ready).then(r=>r.active?.postMessage({cache:'warm'})).catch(e=>{if(navigator.onLine!==false&&e?.name!=='SecurityError'&&e?.name!=='AbortError')errSw({kind:e?.name,message:e?.message,function:'register'})})});setInterval(refreshWhenReady,30000);
// Sign out clears this device first; the service worker says when the Machine no longer knows this session
document.addEventListener('submit',e=>{const f=e.target;if(!f.matches?.('form[action$="/_machine/logout"]')||f.dataset.wiped)return;e.preventDefault();f.dataset.wiped='1';localCache.wipe().finally(()=>f.submit())},true);
navigator.serviceWorker?.addEventListener('message',e=>{if(e.data?.cache==='signed-out')cacheGone(false)});
navigator.serviceWorker?.controller?.postMessage({errors:'flush'});  // what the worker kept for the error reports while no page was open (errSw)
// The Machine's browser in the main area on a computer, next to the sidebar (from 1024px) or under the top bar (a
// narrower window, like a desktop app tiled half the screen): Browser shows the viewer (state.browser_embed, on the
// dashboard's own address) there instead of a new tab, which in the installed app would be a second app window. The
// frame stays loaded while another view is open, so the session keeps running. Back and close return to the view
// before. Full size covers the whole window with it (Esc or the same button goes back). A phone's browser keeps the
// tab; the mobile app shows the pane, as it has no tabs (a new tab there would replace the dashboard).
// browserPane() shows it from anywhere (true), or says to use a tab (false: a phone, or no viewer on this address).
let browserPane=()=>false;
const bpPhone=()=>!matchMedia('(min-width:1024px)').matches&&(DEV.mobile||matchMedia('(hover:none) and (pointer:coarse)').matches)&&!DEV.phoneApp;  // the mobile app has no tabs: the pane, full size
{let bpBack='inbox',pushed=false,from='',quiet=false;const pane=$('#browser-pane'),row=$('#open-browser'),wide=()=>!bpPhone();
 const full=on=>{const root=document.documentElement;if(on)root.dataset.bpFull='';else delete root.dataset.bpFull;const b=$('#bp-full');b.setAttribute('aria-pressed',String(!!on));b.textContent=on?'Exit full size':'Full size'};
 $('#bp-full').onclick=()=>full(!('bpFull' in document.documentElement.dataset));
 addEventListener('keydown',e=>{if(e.key==='Escape'&&'bpFull' in document.documentElement.dataset&&!pane.hidden&&!document.querySelector('dialog[open]')){e.preventDefault();full(false)}});
 $('#bp-tab').hidden=inApp()||DEV.phoneApp;  // the installed app would open it as a second app window; the mobile app in place of the dashboard
 const show=()=>{const src=state?.browser_embed;if(!src||!wide())return false;
  if(pane.hidden)bpBack=!$('#settings').hidden?'settings':document.querySelector('nav button.active')?.dataset.tab||'inbox';
  for(const x of document.querySelectorAll('main>section'))x.hidden=x!==pane;
  for(const b of document.querySelectorAll('nav button')){b.classList.remove('active');b.setAttribute('aria-current','false')}
  $('#open-settings').setAttribute('aria-current','false');row.setAttribute('aria-current','page');
  const f=$('#bp-frame');if(f.dataset.src!==src){f.dataset.src=src;f.src=src}
  $('#bp-tab').href=row.getAttribute('href')||src;pane.dataset.shown='1';
  if(location.hash!=='#browser'){from=location.hash;history.pushState(null,'',location.pathname+location.search+'#browser');pushed=true}return true};
 browserPane=show;
 // Stop: what the browser shows a to-do's run doing (api/browser-now: the one on the tab in front first) ends at once,
 // with the chat's own stop (chat_stop), said in that to-do's chat. Looked at every few seconds while the pane is open.
 let bpJob=null,bpTimer=0;const stopBtn=$('#bp-stop'),jobEl=$('#bp-job');
 const bpPaint=()=>{const w=bpJob;stopBtn.hidden=!w;jobEl.hidden=!w;jobEl.textContent=w?w.title:'';if(w){stopBtn.title=t('Stop “{}”',w.title);stopBtn.setAttribute('aria-label',stopBtn.title)}};
 const bpNow=async()=>{clearTimeout(bpTimer);if(pane.hidden)return;
  try{const r=await request('api/browser-now');const w=Array.isArray(r?.working)?r.working.find(x=>/^[a-f0-9]{16}$/.test(x?.id||'')):null;
   if((w&&w.id)!==(bpJob&&bpJob.id))stopBtn.disabled=false;bpJob=w||null;bpPaint()}catch{}
  if(!pane.hidden)bpTimer=setTimeout(bpNow,document.hidden?15000:3000)};
 stopBtn.onclick=async()=>{const w=bpJob;if(!w)return;stopBtn.disabled=true;
  try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'chat_stop',args:{suggestion_id:w.id,via:'browser'}})});
   if(bpJob?.id===w.id){bpJob=null;bpPaint()}toast(r?.stopped?t('Stopped “{}”',w.title):t('“{}” had already finished.',w.title));refresh()}
  catch(err){errCaught(err);toast(err.message,true);stopBtn.disabled=false}};
 new MutationObserver(()=>{if(!pane.hidden)bpNow();else{clearTimeout(bpTimer);bpJob=null;bpPaint()}}).observe(pane,{attributes:true,attributeFilter:['hidden']});
 const leave=()=>{if(pane.hidden)return;if(bpBack==='settings')showSettings();else document.querySelector(`nav [data-tab="${bpBack}"]`)?.click()};
 row.addEventListener('click',e=>{if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||e.button)return;if(show())e.preventDefault()});
 // Settings from the pane goes on top of it, so Back shows the pane again (Settings itself replaces the address)
 $('#open-settings').addEventListener('click',()=>{if(!pane.hidden&&location.hash==='#browser')history.pushState(null,'',location.pathname+location.search+'#browser')},true);
 $('#bp-close').onclick=()=>{if(pushed&&location.hash==='#browser'){pushed=false;history.back()}else leave()};
 new MutationObserver(()=>{if(!pane.hidden)return;full(false);if(pane.dataset.shown){delete pane.dataset.shown;signinClosed()}row.setAttribute('aria-current','false');if(location.hash!=='#browser')return;
  if(pushed&&!from){pushed=false;quiet=true;history.back()}else history.replaceState(null,'',location.pathname+location.search+(chatId&&!$('#inbox').hidden?'#chat='+chatId:''))}).observe(pane,{attributes:true,attributeFilter:['hidden']});
 matchMedia('(min-width:1024px)').addEventListener('change',()=>{if(!wide())leave()});  // a phone or tablet turned narrow: back to the view before
 addEventListener('hashchange',e=>{if(quiet){quiet=false;return}if(location.hash==='#browser')show();else if(e.oldURL.endsWith('#browser')){pushed=false;leave()}});
 if(location.hash==='#browser'){const t=Date.now(),wait=()=>location.hash!=='#browser'||show()||Date.now()-t>8000||setTimeout(wait,200);wait()}}
