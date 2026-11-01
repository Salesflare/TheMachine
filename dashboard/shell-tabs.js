// Links to a tab or a sub-tab: #todos, #messages (also #events), #graph, #graph=roles, #learning=changes (also
// #feedback), #connections, #connections=chat (and the tabs' own ids).
const TAB_LINKS={inbox:'inbox',todos:'inbox',suggestions:'inbox',calendar:'calendar',events:'events',messages:'events',graph:'people',people:'people',learning:'feedback',feedback:'feedback',connections:'health',health:'health'};
// A Graph sub-page (People, Organizations, Projects, Who's who) shows at once: its pane is drawn already, or the page
// says it's loading; the Graph's quiet refresh comes after. The switch never waits for the Machine's answer.
function showTab(tab,pane){if(tab==='people'&&pane){graphPane=pane;localStorage.setItem('graph-pane',pane);const view=$('#people-view'),was=graphNode;graphNode='';$('#people-query').value='';
  if(view.querySelector(`[data-graph-panel="${CSS.escape(pane)}"]`)&&view.dataset.mode==='list'&&!was){showGraphPane(pane);graphSkip=!$('#people').hidden&&Date.now()-graphAt<60000}  /* the lists on screen are a minute old at most: no reload */
  else if(was&&!graphKept){view.dataset.mode='loading';view.innerHTML='<p class="pager-loading" role="status">Loading…</p>';$('#people').classList.remove('graph-on-node')}}
 if(tab==='health'&&pane){healthPane=pane==='phone'?'other':pane;healthPicked=true}if(tab==='feedback'&&LEARN_PANES.some(([id])=>id===pane)){learnPane=pane;try{localStorage.setItem('learn-pane',pane)}catch{}}
 document.querySelector(`nav [data-tab="${tab}"]`)?.click();if(tab==='health')renderHealthTabs();if(tab==='feedback')learnTabs()}
function openTabLink(){const st=/^#settings(?:[/=]([a-z]+))?$/.exec(location.hash);if(st){if($('#settings').hidden||st[1]&&st[1]!==settingsNow)showSettings(st[1]);return}const m=/^#([a-z]+)(?:=([a-z]+))?$/.exec(location.hash);if(!m||!TAB_LINKS[m[1]])return;
 const tab=TAB_LINKS[m[1]];if(tab==='people'&&GRAPH_PANES.includes(m[2])){if(!$('#people').hidden&&!graphNode&&graphShown===m[2])return;showTab(tab,m[2]);return}
 history.replaceState(null,'',location.pathname+location.search);showTab(tab,m[2])}
window.addEventListener('hashchange',()=>{openChatLink();openSnoozeLink();openResultLink();openCardLink();openFleetLink();openSharedLink();openTabLink();openConnectLink()});
function noteSplit(n){if(!n)return'';const parts=[['style','style'],['fact','missing facts'],['continue','keep going'],['new_ask','new asks'],['unsorted','not sorted']].filter(([k])=>n[k]);
return parts.length?`<div class="notes-split"><span>What your Change notes asked for</span><div>${parts.map(([k,t])=>`<span class="chip t-${{style:'lavender',fact:'amber',continue:'orange',new_ask:'mint',unsorted:'muted'}[k]}">${n[k]} ${t}</span>`).join('')}</div></div>`:''}
// How it's going (Learning): the last 30 days in four numbers, each saying what it counts (assistant.py quality():
// Worth it = acted on (Do it, Send or Done) of those decided, dismissed ones being the rest; First try and Finished count
// to-dos started with Do it; Sent as is = drafts sent without an edit, a Change or Try again first). Higher is better for
// all four. Then Worth it week by week (8 weeks, each bar its own %), the Change notes by kind, and Worth it per source.
const qPct=(a,b)=>b?Math.round(100*a/b):null;
function qWas(v,prev){if(v==null||prev==null)return'';return `<small class="q-was">${esc(v>prev?t('Up from {}% the 30 days before',prev):v<prev?t('Down from {}% the 30 days before',prev):t('Same as the 30 days before'))}</small>`}
function qTile(value,name,means,was=''){return `<div class="q-tile"><span class="q-name">${esc(t(name))}</span><b>${value==null?'–':value+'%'}</b><small class="q-means">${esc(means)}</small>${was}</div>`}
function qualityHTML(q){if(!q||!q.cards)return `<p class="q-empty">${esc(t('Not enough to-dos yet. These numbers start once you decide on a few.'))}</p>`;
 const decided=q.worth_it+q.dismissed,sent=(q.sent_as_written||0)+(q.sent_edited||0),few=t('Not enough to-dos yet');
 const tiles=[qTile(q.hit_rate,'Worth it',decided?t(['Of {} to-do you decided: acted on, not dismissed','Of {} to-dos you decided: acted on, not dismissed'],decided):few,qWas(q.hit_rate,q.previous?.hit_rate)),
  qTile(q.first_time_rate,'First try',q.do_it?t(['Of {} to-do started with Do it: no correction needed','Of {} to-dos started with Do it: no correction needed'],q.do_it):few,qWas(q.first_time_rate,q.previous?.first_time_rate)),
  qTile(q.finished_rate,'Finished',q.do_it?t(['Of {} to-do started with Do it: finished without a nudge','Of {} to-dos started with Do it: finished without a nudge'],q.do_it):few,qWas(q.finished_rate,q.previous?.finished_rate)),
  qTile(qPct(q.sent_as_written||0,sent),'Sent as is',sent?t(['Of {} draft sent: no edit or Change first','Of {} drafts sent: no edit or Change first'],sent):t('No drafts sent yet'))];
 const src=Object.entries(q.by_source||{}).sort((a,b)=>(b[1].worth_it+b[1].dismissed)-(a[1].worth_it+a[1].dismissed));
 const srcRow=([k,n])=>{const d=n.worth_it+n.dismissed;return `<div${SOURCE_TIPS[k]?` title="${esc(SOURCE_TIPS[k])}"`:''}><span class="grow">${esc(k)}${SOURCE_TIPS[k]?`<small>${esc(SOURCE_TIPS[k])}</small>`:''}</span><span class="q-n">${d?esc(t('{} of {}',n.worth_it,d))+` <b>${qPct(n.worth_it,d)}%</b>`:esc(t('None decided yet'))}</span></div>`};
 return `<p class="learn-intro">${esc(t('Last 30 days. Higher is better.'))}</p><div class="q-tiles">${tiles.join('')}</div>${trendChart(q.trend)}${noteSplit(q.notes)}`
  +(src.length?`<h3 class="q-h">${esc(t('Worth it per source'))}</h3><p class="learn-intro">${esc(t('Where to-dos came from, and how many you acted on of those you decided.'))}</p><div class="list quality-sources"><div class="q-head"><span class="grow">${esc(t('Source'))}</span><span>${esc(t('Acted on'))}</span></div>${src.map(srcRow).join('')}</div>`:'')}
// Worth it week by week: one bar per week, its height and the number above it that week's %, the week under it and how
// many to-dos were decided. Shown once two weeks have decided to-dos.
function trendChart(trend){const rows=trend?.weekly||[];if(rows.filter(r=>r.worth_it+r.dismissed).length<2)return '';
 const wk=r=>new Date(r.start+'T12:00').toLocaleDateString(DL,{day:'numeric',month:'short'}),marks=rows.some(r=>r.changes?.length);
 const col=r=>{const n=r.worth_it+r.dismissed,label=n?t('Week of {}: {}% worth it, {} decided',wk(r),r.hit_rate,n):t('Week of {}: nothing decided',wk(r));
  return `<div role="listitem" aria-label="${esc(label)}" title="${esc([label,...r.changes||[]].join('\n'))}"><small class="v">${n?r.hit_rate+'%':'–'}</small><span class="bar"><em${n?` style="height:${Math.max(2,r.hit_rate)}%"`:' class="none"'}></em></span><span class="w">${esc(wk(r))}${r.changes?.length?'<i class="mark" aria-hidden="true">◆</i>':''}</span><span class="n">${n?esc(t('{} decided',n)):''}</span></div>`};
 return `<figure class="trend"><figcaption><strong>${esc(t('Worth it, week by week'))}</strong><small>${esc(t('Last 8 weeks. Each bar is that week’s Worth it.'))}</small></figcaption><div class="bars" role="list">${rows.map(col).join('')}</div>${marks?`<p class="trend-legend"><i class="mark" aria-hidden="true">◆</i>${esc(t('Rules changed that week'))}</p>`:''}</figure>`}
let refreshes=0;
// A redraw keeps the field someone is in: focus and caret back on the same field (by id) when the redraw replaced it
function focusKept(draw){const a=document.activeElement,id=a&&a!==document.body&&a.id,sel=id&&a.matches?.(TYPED)?[a.selectionStart,a.selectionEnd]:null;draw();
 if(!id||document.activeElement?.id===id)return;const b=document.getElementById(id);if(!b||b.offsetParent===null)return;b.focus({preventScroll:true});if(sel)try{b.setSelectionRange(...sel)}catch{}}
// A release reaches pages that stayed open, but never under someone using the page: the new version waits until the
// page is hidden, or nothing was touched for a few minutes with nothing typed and no dialog open. Until then a small
// "Update ready" pill loads it at a press. A restart of the Machine alone serves the same page: it just reconnects.
const UPDATE_IDLE=3*60e3,UPDATE_AWAY=45e3,pageAt=Date.now();let lastInput=0,lastTouch=0,updateWaiting=false;
// Coming back to the page counts too: the update never lands right as someone returns to it.
for(const ev of ['pointerdown','pointermove','keydown','wheel','touchstart','input','scroll','focus'])addEventListener(ev,()=>{lastInput=Date.now()},{capture:true,passive:true});
// Doing something on the page (a click, a key, a scroll by hand), unlike a window that opens under the pointer, gets
// the focus, or has the pointer pass over it
for(const ev of ['pointerdown','keydown','wheel','touchstart','input'])addEventListener(ev,()=>{lastTouch=Date.now()},{capture:true,passive:true});
// Typed and not saved yet: a text field (also in a folded card or another tab) that differs from what the page drew
// there. A closed panel never counts: what it still holds (a sent email's subject and body, a draft the page filled in)
// is not typing, and an open panel holds the update back by itself.
const TYPED='textarea,input:not([type]),input[type=text],input[type=search],input[type=email],input[type=url],input[type=tel],input[type=number]';
const inClosedPanel=el=>!!el.closest('dialog:not([open])');
const typedSomewhere=()=>[...document.querySelectorAll(TYPED)].some(t=>t.value&&t.value!==t.defaultValue&&!inClosedPanel(t))||[...document.querySelectorAll('[contenteditable=""],[contenteditable=true]')].some(t=>t.textContent.trim()&&!inClosedPanel(t));
const pageInUse=()=>typedSomewhere()||!localCache.on&&outbox.items.length>0||!!document.querySelector('dialog[open]')||placeBusy();
// Safe to load the new version now: nothing typed or open, and the page is hidden, idle for a few minutes, only just
// opened (an older copy the app started with, before anything was done on it), or a window in the background (another
// window has the focus, as a desktop app's window often does for days) that nobody did anything in for a bit
function updateSafe(){if(pageInUse())return false;if(document.hidden)return true;if(!lastTouch&&Date.now()-pageAt<20e3)return true;
 if(!document.hasFocus()&&Date.now()-Math.max(lastTouch,pageAt)>=UPDATE_AWAY)return true;return Date.now()-Math.max(lastInput,pageAt)>=UPDATE_IDLE}
function updateNow(){try{sessionStorage.setItem('tm-update-view',JSON.stringify({at:Date.now(),tab:document.querySelector('nav button[data-tab].active')?.dataset.tab||'',y:Math.round(scrollY)}))}catch{}
 shellDrop().finally(()=>location.reload())}
// Never in a loop: when the page that came back is still not the server's (a copy kept somewhere on the way), only the pill
function updateMaybe(){if(!updateWaiting||!updateSafe())return false;let last=0;try{last=+sessionStorage.getItem('tm-update-at')||0}catch{}if(Date.now()-last<6e4)return false;
 try{sessionStorage.setItem('tm-update-at',String(Date.now()))}catch{}updateWaiting=false;updateNow();return true}
function uiVersionCheck(){if(!state.ui_version||UI_VERSION.startsWith('__')||state.ui_version===UI_VERSION)return false;
 if(!updateWaiting){updateWaiting=true;for(const b of document.querySelectorAll('[data-update-ready]'))b.hidden=false}return updateMaybe()}
// After a quiet update: back on the tab and at the place the page was
function updateViewBack(){let v=null;try{v=JSON.parse(sessionStorage.getItem('tm-update-view')||'null');sessionStorage.removeItem('tm-update-view')}catch{}if(!v||!(Date.now()-v.at<6e4))return;
 if(v.tab&&!location.hash)document.querySelector(`nav button[data-tab="${CSS.escape(v.tab)}"]`)?.click();requestAnimationFrame(()=>scrollTo(0,+v.y||0))}
// A new release: the app's copy of the page goes, so the reload gets the new one from the Machine
async function shellDrop(){try{for(const k of await caches.keys())if(k.startsWith('tm-shell'))await caches.delete(k)}catch{}}
// A snooze whose time has passed is back, even before the service's next wake-up reaches this page: never show a past
// "Snoozed until", and refresh again right when the next one ends
let wakeTimer=null;
// The quiet Browser pill beside Settings: the Machine's browser view in a new tab, only when this Machine has one
function browserPill(st){const u=String(st?.browser_link||''),ok=/^https?:\/\//i.test(u),p=$('#settings-browser');for(const a of [$('#open-browser'),p?.querySelector('a')]){if(!a)continue;if(ok)a.href=u;else a.removeAttribute('href')}$('#open-browser').hidden=!ok;if(p)p.hidden=!ok}
function wakeSnoozed(st){const now=Date.now();let next=Infinity;for(const s of st?.suggestions||[]){if(s.status!=='snoozed'||!s.snoozed_until)continue;const at=Date.parse(s.snoozed_until);
  if(at<=now)Object.assign(s,{status:['pending','accepted','prepared','instructions'].includes(s.resume_status)?s.resume_status:'pending',snoozed_until:null,resume_status:null});else next=Math.min(next,at)}
 clearTimeout(wakeTimer);if(next<Infinity&&next-now<864e5)wakeTimer=setTimeout(()=>refresh(),next-now+3000);return st}
// Follow-ups going out spaced (30-45 s apart) are watched every 5 s: their progress to-do moves on without a 2 s poll for minutes.
let sendTimer=null;const sendWatch=()=>{clearTimeout(sendTimer);const busy=s=>chatSends(s).some(x=>['queued','sending'].includes(x.st.status)),batch=(state.follow_up_progress||[]).some(p=>p.going);
 const quick=(state.suggestions||[]).some(s=>busy(s)&&!(batch&&s.follow_up)),rewriting=fr?.changing.size>0;  // the review's Change: every 3 s until each rewrite is back
 if(quick||batch||rewriting)sendTimer=setTimeout(()=>{refreshWhenReady();if(chatId)chatPoll()},quick?2000:rewriting?3000:5000)};
// A status read that started before an edit shown at once (a rename) is older than the screen: read again instead of
// putting the old value back for a moment.
let localEdits=0;
// The session is gone (signed out elsewhere, run out) or another owner: nothing of the old one stays on this device.
// Reload once so the sign-in gate takes over, never in a loop.
async function cacheGone(reload){await localCache.wipe();if(reload==='owner')return location.reload();if(!reload)return;let last=0;try{last=+sessionStorage.getItem('cache-gone-reload')||0;sessionStorage.setItem('cache-gone-reload',String(Date.now()))}catch{}if(Date.now()-last>6e4)location.reload()}
let statusSaved=0,statusSig='';  // the kept copy: on any change in the cards, else at most every 15 s
// Who this page is for, asked once: the CSRF token a page copy lacks, and whether this device keeps data for this owner
let sessionAsked=false;
async function sessionCheck(){if(sessionAsked||!localCache.on&&csrfLive)return;sessionAsked=true;
 try{const s=await request('api/session',{redirect:'manual'});if(s.csrf&&!csrfLive){csrfLive=s.csrf;csrfSet?.()}
  if(localCache.on&&s.cache_scope&&s.cache_scope!==CACHE_SCOPE)await cacheGone('owner')}
 catch(e){sessionAsked=false;if(e.sessionGone||e.status===401||e.status===403)await cacheGone(!!e.sessionGone)}}
async function refresh(){refreshes++;try{const edits=localEdits,next=wakeSnoozed(await request('api/status',{redirect:'manual'}));if(edits!==localEdits)return await refresh();
 sessionCheck();shownCached=false;shownAt=Date.now();if(localCache.on){const sig=(next.suggestions||[]).map(x=>x.id+x.status).join();if(sig!==statusSig||Date.now()-statusSaved>15000){statusSaved=Date.now();statusSig=sig;localCache.put('status',next)}}
 state=next;netSet(false);cardsMerge();browserPill(state);if(state.source_url)$('#source-code').href=state.source_url;if(uiVersionCheck())return;focusKept(render);frRefresh();deviceRender();sendWatch();openChatLink(true);openSnoozeLink();openResultLink();openSendLink();openCardLink();openFleetLink();openSharedLink();openTabLink();openConnectLink();if(!$('#people').hidden)await people(graphNode,true);try{if(!$('#calendar').hidden)calendarView();else calBadge()}catch(e){errCaught(e);console.error(e)}if(refreshFailed){notice('');refreshFailed=false}retryIn=0;clearTimeout(retryTimer);if(outbox.items.length)outboxFlush();return true}catch(e){errCaught(e);refreshFailed=true;if(e.sessionGone||e.status===401||e.status===403)await cacheGone(!!e.sessionGone);if(e.offline){notice('');clearTimeout(retryTimer);retryIn=e.retryAfter||Math.min(30000,(retryIn||2500)*2);retryTimer=setTimeout(refreshWhenReady,e.retryAfter?retryIn:retryIn*(.8+Math.random()*.4));netSet(true,e.restarting)}else notice(e.message,true);staleLine(e.restarting?'Restarting · retrying':shownAt?t('Offline · updated {}',hhmm(shownAt)):'Unavailable');if(!state?.suggestions)$('#suggestions').innerHTML='<div class="empty all-clear"><img class="sticker" src="brand/sad.webp" alt=""><div><strong>I can’t reach the assistant.</strong>I’ll keep trying every 30 seconds.</div></div>',notice('');return false}finally{refreshes--}}
$('nav').onclick=e=>{const t=e.target.closest('button');if(!t?.dataset.tab)return;for(const b of document.querySelectorAll('nav button[data-tab]')){b.classList.toggle('active',b===t);b.setAttribute('aria-current',b===t?'page':'false')}for(const s of document.querySelectorAll('main>section'))s.hidden=s.id!==t.dataset.tab;if(t.dataset.tab==='people'&&!graphSkip)people(graphNode,!!$('#people-view').innerHTML&&$('#people-view').dataset.mode!=='loading');graphSkip=false;if(t.dataset.tab==='health')savedLogins();if(t.dataset.tab==='events'&&!$('#results').innerHTML){$('#results').innerHTML='<p class="muted">Loading…</p>';search()}if(t.dataset.tab==='fleet')fleetShown=fleetView(true);requestAnimationFrame(()=>{document.querySelectorAll('.fleet-tabs,.sub-tabs').forEach(tabsShow);kbLand()})};
// The desktop sidebar (from 1024px): the cards as a quiet list under the tabs, by section, each section folds (Done
// starts folded) and the fold is remembered; a filter on the titles; the whole sidebar folds to icons.
const sideStore={get:k=>{try{return localStorage.getItem(k)}catch{return null}},set:(k,v)=>{try{localStorage.setItem(k,v)}catch{}}};
const sideFolded=(()=>{try{const v=JSON.parse(sideStore.get('side-folded'));if(Array.isArray(v))return new Set(v)}catch{}return new Set(['done'])})();
// Look done starts folded like Done, also where folds were saved before it existed: its saved state is that it's open
const sideOpen=k=>['lookdone','waiting'].includes(k)?sideFolded.has(k+':open'):!sideFolded.has(k);
const CHEVRON='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>';
let sideGroups=[],sideCounts={},sideHTML='';
// The sidebar's groups show the first few (Done 10, an active group 8) and a quiet Show more adds 20 per tap; folding a
// group starts it over. Done counts every done card and loads the next ones from the Machine as it goes. A search shows
// every match, done cards too, also those not loaded yet.
const SIDE_STEP=20,sideShown={},sideFirst=k=>k==='done'?10:8;
const titleHas=(x,q)=>String(x.title||'').toLowerCase().includes(q);
function sideAll(items,key,q=''){let all=q?items.filter(x=>titleHas(x,q)):items;if(key!=='done')return all;
 const extra=[...pagers.get(doneKey())?.items||[],...q&&doneFound.q===q?doneFound.items:[]];if(!extra.length)return all;const seen=new Set(all.map(x=>x.id));
 return [...all,...extra.filter(x=>!seen.has(x.id)&&(!q||titleHas(x,q)))].sort((a,b)=>closedAt(b).localeCompare(closedAt(a)))}
function sideList(items,key){const each=sideAll(items,key),all=key==='done'?doneFold(each):each,n=sideShown[key]||sideFirst(key),total=key==='done'?Math.max(each.length,state?.done_counts?.[scopeFilter]??0):each.length;
 return {list:all.slice(0,n),more:all.length>n||total>each.length&&pagers.get(doneKey())?.next!=null,count:total}}
const sideMoreRow=key=>`<button type="button" class="side-more" data-side-more="${key}">Show more</button>`;
async function sideMore(key){sideShown[key]=(sideShown[key]||sideFirst(key))+SIDE_STEP;
 if(key==='done'){const items=sideGroups.find(g=>g[2]==='done')?.[0]||[],p=donePager();for(let i=0;i<10&&doneFold(sideAll(items,'done')).length<sideShown.done&&p.next!=null&&!p.failed;i++)await pagerMore(doneKey())}
 sideCards();if(chatOpen())render()}
document.addEventListener('click',e=>{const b=e.target.closest('[data-side-more]');if(!b)return;e.preventDefault();sideMore(b.dataset.sideMore)});
// A search also asks the Machine for done cards beyond the ones loaded
const doneFound={q:'',items:[]};let doneAsk=0;
function doneSearch(q){if(!q||doneFound.q===q||(state?.done_counts?.[scopeFilter]??0)<=sideAll(sideGroups.find(g=>g[2]==='done')?.[0]||[],'done').length)return;const n=++doneAsk;
 clearTimeout(doneSearch.t);doneSearch.t=setTimeout(async()=>{try{const r=await request(`api/cards/done?limit=50&q=${encodeURIComponent(q)}${scopeFilter==='all'?'':'&scope='+scopeFilter}`);if(n!==doneAsk)return;
  for(const c of r.cards)doneExtra.set(c.id,c);cardsMerge();doneFound.q=q;doneFound.items=r.cards;sideCards()}catch{}},250)}
function sideCards(groups){if(groups)sideGroups=groups;const q=$('#side-find').value.trim().toLowerCase(),box=$('#side-cards');doneSearch(q);
 const parts=sideGroups.map(([items,title,key])=>{const open=!!q||sideOpen(key),cut=q?{list:sideAll(items,key,q),more:false}:sideList(items,key),count=q?cut.list.length:cut.count;if(!count)return'';
  return `<div class="side-group${['done','later','lookdone','waiting'].includes(key)?' quiet':''}"><button type="button" class="side-head" data-side-fold="${key}" aria-expanded="${open}">${CHEVRON}<span>${title}</span><span class="count">${count}</span></button>${open?cut.list.map(x=>sideRow(x,chatId)).join('')+(cut.more?sideMoreRow(key):''):''}</div>`}).join('');
 const html=`<div class="side-label" role="group" aria-label="To-dos">${[['all','All'],['work','Work'],['personal','Personal']].map(([v,t])=>`<button type="button" data-scope="${v}" aria-pressed="${scopeFilter===v}">${t}</button>`).join('')}</div>${parts||`<p class="side-empty">${q?'No to-dos match.':'No to-dos yet.'}</p>`}`;
 if(html!==sideHTML){sideHTML=html;const back=sideKeep(box);box.innerHTML=html;back();requestAnimationFrame(chatFades)}}
// The card list scrolls in its own box (the computer's sidebar, the phone's drawer): a new card above keeps the rows in view where they were
function sideKeep(box){const sc=[box,box.closest('.app-side')].find(x=>x&&x.scrollTop>0);if(!sc)return()=>{};const edge=sc.getBoundingClientRect().top,key=n=>n.getAttribute('href')||n.dataset.sideFold||n.dataset.sideMore||n.dataset.doneFold;
 const row=[...box.querySelectorAll('a[href],[data-side-fold],[data-side-more],[data-done-fold]')].find(n=>n.getBoundingClientRect().bottom>edge);if(!row)return()=>{};const k=key(row),top=row.getBoundingClientRect().top;
 return()=>{const n=[...box.querySelectorAll('a[href],[data-side-fold],[data-side-more],[data-done-fold]')].find(x=>key(x)===k);if(n){const d=n.getBoundingClientRect().top-top;if(Math.abs(d)>=1)sc.scrollTop+=d}}}
$('#side-find').addEventListener('input',()=>sideCards());
$('#side-find').addEventListener('keydown',e=>{if(e.key==='Escape'){e.target.value='';sideCards()}if(e.key==='Enter'){const a=$('#side-cards a');if(a)a.click()}});
$('#side-cards').addEventListener('click',e=>{const f=e.target.closest('[data-side-fold]');
 if(f){const k=['lookdone','waiting'].includes(f.dataset.sideFold)?f.dataset.sideFold+':open':f.dataset.sideFold;sideFolded.has(k)?sideFolded.delete(k):sideFolded.add(k);delete sideShown[k];sideStore.set('side-folded',JSON.stringify([...sideFolded]));sideCards();return}
 const sc=e.target.closest('[data-scope]');if(sc){scopeSet(sc.dataset.scope);return}
 const a=e.target.closest('a[href^="#chat="]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey)return;e.preventDefault();const id=a.getAttribute('href').slice(6);
 if(id===chatId){showTab('inbox');return}chatGo(id)});
// Suggestions in the sidebar while a chat is open goes back to the overview
$('nav').addEventListener('click',e=>{if(!e.isTrusted||!chatId||$('#inbox').hidden||!e.target.closest('[data-tab="inbox"]'))return;history.replaceState(null,'',location.pathname+location.search);chatPushed=false;openChatLink();scrollTo(0,0)});
function sideSet(folded,save=true){document.documentElement.dataset.side=folded?'collapsed':'open';if(save)sideStore.set('side',folded?'collapsed':'open');
 const b=$('#side-toggle'),label=folded?'Expand sidebar':'Collapse sidebar';b.setAttribute('aria-expanded',String(!folded));b.setAttribute('aria-label',label);b.setAttribute('aria-keyshortcuts',SIDE_KEY_ARIA);b.title=label+' ('+SIDE_KEY+')';sideTipHide();requestAnimationFrame(chatFades)}
// Folded to icons, every row says what it is: a tooltip to its right (after a moment on hover, at once on keyboard focus),
// with its count in words, and the same words as its accessible name. Ctrl/⌘+B folds and unfolds.
const SIDE_MAC=/Mac|iPhone|iPad/.test(navigator.platform||navigator.userAgent),SIDE_KEY=SIDE_MAC?'⌘B':'Ctrl+B',SIDE_KEY_ARIA=SIDE_MAC?'Meta+B':'Control+B';
const sideTip=document.createElement('div');sideTip.id='side-tip';sideTip.setAttribute('role','tooltip');sideTip.hidden=true;document.body.append(sideTip);
let sideTipTimer=0,sideTipFor=null;
function sideTipText(el){if(el.id==='side-toggle')return el.getAttribute('aria-label')+' · '+SIDE_KEY;if(el.id==='side-search')return 'Find a to-do';if(el.id==='live')return $('#updated').textContent.trim()||'Refresh';
 if(el.matches('.app-side .head-side>.settings-link'))return (el.querySelector('.lbl')?.textContent.trim()||el.getAttribute('aria-label')||'')+(el.dataset.keys?' · '+el.dataset.keys:'');
 return (el.getAttribute('aria-label')||'')+(el.dataset.keys?' · '+el.dataset.keys:'')}
function sideLabels(){for(const b of document.querySelectorAll('.app-side nav [data-tab]')){const name=b.querySelector('.nl')?.textContent.trim()||'',n=+(b.querySelector('.badge')?.textContent||0),t=b.dataset.tab,c=sideCounts||{};
  const tr=window.t,more=t==='inbox'?[[c.ready,'{} ready'],[c.needs,'{} to decide']].filter(([k])=>k).map(([k,w])=>tr(w,k)).join(' · ')||(n?tr('{} waiting',n):''):!n?'':t==='health'?tr(['{} needs a look','{} need a look'],n):t==='people'?tr('{} waiting',n):t==='calendar'?tr('{} today',n):String(n);
  const label=more?name+' · '+more:name;if(b.getAttribute('aria-label')!==label)b.setAttribute('aria-label',label)}
 const live=$('#live'),u=$('#updated').textContent.trim();if(u&&live.getAttribute('aria-label')!==u)live.setAttribute('aria-label',u)}
function sideTipHide(){clearTimeout(sideTipTimer);if(sideTipFor){if(sideTipFor.dataset.tipTitle!==undefined){sideTipFor.title=sideTipFor.dataset.tipTitle;delete sideTipFor.dataset.tipTitle}sideTipFor=null}sideTip.hidden=true}
function sideTipShow(el){if(document.documentElement.dataset.side!=='collapsed'||!matchMedia('(min-width:1024px)').matches)return;sideLabels();const text=sideTipText(el);if(!text)return;
 if(el.title){el.dataset.tipTitle=el.title;el.title=''}  /* no second, native tooltip */
 sideTipFor=el;sideTip.textContent=text;const r=el.getBoundingClientRect(),side=$('#app-side').getBoundingClientRect();sideTip.style.left=Math.round(side.right+8)+'px';sideTip.style.top=Math.round(r.top+r.height/2)+'px';sideTip.hidden=false}
const SIDE_TIP_ON='.app-side nav [data-tab],.side-sub a,#side-toggle,#side-search,.app-side .head-side>.settings-link,#live';
$('#app-side').addEventListener('pointerover',e=>{const el=e.target.closest(SIDE_TIP_ON);if(!el||el===sideTipFor||e.pointerType==='touch')return;sideTipHide();sideTipTimer=setTimeout(()=>sideTipShow(el),300)});
$('#app-side').addEventListener('pointerout',e=>{const el=e.target.closest(SIDE_TIP_ON);if(el&&!el.contains(e.relatedTarget))sideTipHide()});
$('#app-side').addEventListener('focusin',e=>{const el=e.target.closest(SIDE_TIP_ON);sideTipHide();if(el&&el.matches(':focus-visible'))sideTipShow(el)});
$('#app-side').addEventListener('focusout',sideTipHide);$('#app-side').addEventListener('click',sideTipHide);addEventListener('scroll',sideTipHide,{passive:true});
addEventListener('keydown',e=>{if(e.key==='Escape')sideTipHide();if(!(e.ctrlKey||e.metaKey)||e.altKey||e.shiftKey||e.key.toLowerCase()!=='b'||!matchMedia('(min-width:1024px)').matches||e.target.closest?.('textarea,input,select,[contenteditable]'))return;
 e.preventDefault();sideSet(document.documentElement.dataset.side!=='collapsed')});
{const o=new MutationObserver(()=>sideLabels());o.observe($('.app-side nav'),{subtree:true,childList:true,characterData:true});o.observe($('#updated'),{subtree:true,childList:true,characterData:true})}
sideSet(document.documentElement.dataset.side==='collapsed',false);
$('#side-toggle').onclick=()=>sideSet(document.documentElement.dataset.side!=='collapsed');
$('#side-search').addEventListener('click',()=>{if(document.documentElement.dataset.side==='collapsed'&&matchMedia('(min-width:1024px)').matches){sideSet(false);$('#side-find').focus()}});
// Below 1024px the sidebar is a drawer: the menu button, a swipe from the left edge or All tasks in a chat opens it; ✕,
// the shade, Esc, a swipe to the left and the back button close it, and so does picking a row in it. While it is open
// the rest of the page is inert, so focus stays in it.
const DESK=matchMedia('(min-width:1024px)'),drawerIs=()=>document.documentElement.dataset.drawer==='open';
let drawerInert=[],drawerPopping=false,drawerStep=false,drawerFrom=null;
function drawerShow(on){const root=document.documentElement;if(on)root.dataset.drawer='open';else delete root.dataset.drawer;$('#drawer-open').setAttribute('aria-expanded',String(on));
 for(const el of drawerInert)el.inert=false;drawerInert=[];
 if(on)for(const el of document.body.children)if(!['app-side','drawer-scrim','side-tip'].includes(el.id)&&el.tagName!=='DIALOG'&&el.tagName!=='SCRIPT'&&!el.inert){el.inert=true;drawerInert.push(el)}}
function drawerOpen(){if(DESK.matches||drawerIs())return;drawerFrom=document.activeElement;sideTipHide();drawerShow(true);if(!history.state?.drawer)history.pushState({drawer:1},'',location.href);
 requestAnimationFrame(()=>$('#side-toggle').focus({preventScroll:true}))}
// visual only: a row that navigates takes the drawer's place on the history itself
function drawerHide(){if(!drawerIs())return;const back=document.activeElement&&$('#app-side').contains(document.activeElement);drawerShow(false);if(back&&!chatId)(drawerFrom?.isConnected&&drawerFrom.offsetParent?drawerFrom:$('#drawer-open')).focus({preventScroll:true})}
function drawerClose(){if(!drawerIs())return;drawerHide();if(history.state?.drawer){drawerPopping=true;history.back()}}
// back closes it; back onto the entry it pushed (it closed some other way meanwhile) steps over that entry; back from
// #graph=… to the plain page leaves the Graph for Suggestions
// (a step that only opened or closed the drawer is no navigation: drawerStep tells the other back handlers to sit it out)
addEventListener('popstate',()=>{const step=()=>{drawerStep=true;setTimeout(()=>{drawerStep=false})};if(drawerPopping){drawerPopping=false;step();return}if(drawerIs()&&!history.state?.drawer){drawerHide();step();return}
 if(history.state?.drawer&&!drawerIs()){drawerPopping=true;step();history.back();return}
 if(!location.hash&&!$('#people').hidden&&!graphNode)showTab('inbox')});
$('#drawer-open').onclick=drawerOpen;$('#topbar-title').onclick=e=>{e.preventDefault();scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})};$('#drawer-scrim').onclick=drawerClose;
// Search on a phone: the top bar's search icon opens the palette (defined with the action registry below)
$('#find-open').onclick=()=>palOpen();
$('#side-toggle').addEventListener('click',e=>{if(DESK.matches)return;e.stopImmediatePropagation();drawerClose()},true);
addEventListener('keydown',e=>{if(e.key==='Escape'&&drawerIs()&&!document.querySelector('dialog[open]')){e.preventDefault();drawerClose()}});
DESK.addEventListener('change',()=>{if(DESK.matches&&drawerIs()){drawerShow(false);if(history.state?.drawer)history.replaceState(null,'',location.href)}});
// picking a tab, a card, a Graph row, Settings or Browser closes it
$('#app-side').addEventListener('click',e=>{if(!drawerIs()||!e.isTrusted)return;const t=e.target.closest('nav button[data-tab],.side-cards a,.side-sub a,#open-settings,#open-browser');if(!t||e.ctrlKey||e.metaKey||e.shiftKey)return;
 drawerHide();setTimeout(()=>{if(history.state?.drawer){drawerPopping=true;history.back()}})},true);
// swipe: from the left edge to open, to the left on the drawer to close
{let sw=null;
 addEventListener('touchstart',e=>{if(DESK.matches||e.touches.length!==1)return;const t=e.touches[0],open=drawerIs();
  if(!open&&t.clientX>24||document.querySelector('dialog[open]'))return;if(open&&!$('#app-side').contains(e.target)&&e.target.id!=='drawer-scrim')return;sw={x:t.clientX,y:t.clientY,open,dx:0,lock:null}},{passive:true});
 addEventListener('touchmove',e=>{if(!sw)return;const t=e.touches[0],dx=t.clientX-sw.x,dy=t.clientY-sw.y;
  if(sw.lock===null&&Math.hypot(dx,dy)>8)sw.lock=Math.abs(dx)>Math.abs(dy)*1.3?'x':'y';if(sw.lock!=='x'){if(sw.lock==='y')sw=null;return}
  sw.dx=dx;const side=$('#app-side'),w=side.offsetWidth;side.classList.add('dragging');
  if(sw.open)side.style.transform=`translateX(${Math.min(0,dx)}px)`;else{if(!drawerIs()){document.documentElement.dataset.drawer='open';side.style.transform=`translateX(-${w}px)`}side.style.transform=`translateX(${Math.min(0,dx-w)}px)`}},{passive:true});
 addEventListener('touchend',()=>{if(!sw)return;const {open,dx,lock}=sw,side=$('#app-side');sw=null;side.classList.remove('dragging');side.style.transform='';if(lock!=='x')return;
  if(open){if(dx<-60)drawerClose()}else{delete document.documentElement.dataset.drawer;if(dx>60)drawerOpen()}});
 addEventListener('touchcancel',()=>{if(!sw)return;const side=$('#app-side');side.classList.remove('dragging');side.style.transform='';if(!sw.open&&!drawerInert.length)delete document.documentElement.dataset.drawer;sw=null})}
// The menu button wears a dot when a connection needs a look
new MutationObserver(()=>{$('#drawer-dot').hidden=!$('#badge-health').textContent.trim()}).observe($('#badge-health'),{childList:true,characterData:true,subtree:true});
