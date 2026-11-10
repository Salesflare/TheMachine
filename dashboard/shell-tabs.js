// Links to a tab or a sub-tab: #todos, #messages (also #events), #graph, #graph=orgs, #learning=changes (also
// #feedback), #connections, #connections=chat (and the tabs' own ids).
const TAB_LINKS={inbox:'inbox',todos:'inbox',suggestions:'inbox',calendar:'calendar',routines:'routines',events:'events',messages:'events',graph:'people',people:'people',learning:'feedback',feedback:'feedback',connections:'health',health:'health'};
// A Graph sub-page (People, Organizations, Projects) shows at once: its pane is drawn already, or the page
// says it's loading; the Graph's quiet refresh comes after. The switch never waits for the Machine's answer.
function showTab(tab,pane){if(tab==='people'&&pane){graphPane=pane;localStorage.setItem('graph-pane',pane);const view=$('#people-view'),was=graphNode;graphNode='';$('#people-query').value='';
  if(view.querySelector(`[data-graph-panel="${CSS.escape(pane)}"]`)&&view.dataset.mode==='list'&&!was){lazyRun('graph',()=>showGraphPane(pane));graphSkip=!$('#people').hidden&&Date.now()-graphAt<60000}  /* the lists on screen are a minute old at most: no reload */
  else if(was&&!graphKept){view.dataset.mode='loading';lateShow(()=>{if(view.dataset.mode!=='loading')return;view.innerHTML='<p class="pager-loading" role="status">Loading…</p>';$('#people').classList.remove('graph-on-node')})}}  /* the page stays up for a fast answer */
 if(tab==='health'&&pane){healthPane=pane==='phone'?'other':pane;healthPicked=true}if(tab==='feedback'&&pane==='team')pane='shared';if(tab==='feedback'&&LEARN_PANES.some(([id])=>id===pane)){learnPane=pane;try{localStorage.setItem('learn-pane',pane)}catch{}}
 document.querySelector(`nav [data-tab="${tab}"]`)?.click();if(tab==='health')lazyRun('connections',()=>renderHealthTabs());if(tab==='feedback')lazyRun('learning',()=>learnTabs())}
function openTabLink(){if(openRoutineLink())return;const st=/^#settings(?:[/=]([a-z]+))?$/.exec(location.hash);if(st){if($('#settings').hidden||st[1]&&st[1]!==settingsNow)showSettings(st[1]);return}const m=/^#([a-z]+)(?:=([a-z]+))?$/.exec(location.hash);if(!m||!TAB_LINKS[m[1]])return;
 const tab=TAB_LINKS[m[1]];if(tab==='people'&&GRAPH_PANES.includes(m[2])){if(!$('#people').hidden&&!graphNode&&graphShown===m[2])return;showTab(tab,m[2]);return}
 // a tab's own link stays in the address, so a reload lands there again; a refresh with the tab on screen leaves it be.
 // A link that does something there (#connections=add) goes once handled, so the same link works again.
 if(!m[2]){if($('#'+tab).hidden)showTab(tab);return}history.replaceState(null,'',location.pathname+location.search);showTab(tab,m[2])}
// Another tab tapped (or opened by the app): a link to some other tab leaves the address
$('nav').addEventListener('click',e=>{const t=e.target.closest('button')?.dataset.tab,m=/^#([a-z]+)(?:[=/][\w-]+)?$/.exec(location.hash),was=m&&(m[1]==='fleet'?'fleet':TAB_LINKS[m[1]]);
 if(t&&was&&was!==t)history.replaceState(null,'',location.pathname+location.search)});
// A tapped phone notification opens #chat=<its tag> (mobile/www/inject.js, and every app out there): a to-do's id is
// its chat; the other tags (assistant.py push_send, app_wake) and a bare kind (several at once) open their own view.
function pushRoute(tag){let m;if(/^[a-f0-9]{16}$/.test(tag))return '#chat='+tag;
 if(tag==='digest')return '#calendar?view=agenda';  // the morning: today's meetings and what's due
 if((m=/^fleet-brief(?:-(fl_[0-9a-f]{16}))?$/.exec(tag)))return '#fleet-brief'+(m[1]?'='+m[1]:'');
 if((m=/^fleet-((?:q|fn)_[a-f0-9]{16})$/.exec(tag)))return '#fleet='+m[1];
 if(tag==='fleet'||tag.startsWith('fleet-'))return '#fleet';
 return '#todos'}  // the week's recap, a test, new to-dos, results and reminders together
function openPushLink(changed){const m=/^#chat=([A-Za-z0-9_-]{1,64})$/.exec(location.hash);if(!m||/^[a-f0-9]{16}$/.test(m[1]))return false;
 history.replaceState(null,'',location.pathname+location.search+pushRoute(m[1]));if(!changed&&location.hash.startsWith('#calendar?'))lazyRun('calendar',()=>calRoute());return true}  // a hash change reaches calRoute itself
window.addEventListener('hashchange',()=>{openPushLink(true);openChatLink();openSnoozeLink();openQuickLink();openResultLink();openCardLink();openFleetLink();openSharedLink();openTabLink();openConnectLink()});
function noteSplit(n){if(!n)return'';const parts=[['style','style'],['fact','missing facts'],['continue','keep going'],['new_ask','new asks'],['unsorted','not sorted']].filter(([k])=>n[k]);
return parts.length?make('div',{class:'notes-split'},make('span',{},'What your Change notes asked for'),make('div',{},parts.map(([k,t])=>make('span',{class:`chip t-${{style:'lavender',fact:'amber',continue:'orange',new_ask:'mint',unsorted:'muted'}[k]}`},`${n[k]} ${t}`)))):''}
// How it's going (Learning): the last 30 days in four numbers, each saying what it counts (assistant.py quality():
// Worth it = acted on (Do it, Send or Done) of those decided, dismissed ones being the rest; First try and Finished count
// to-dos started with Do it; Sent as is = drafts sent without an edit, a Change or Try again first). Higher is better for
// all four. Then Worth it week by week (8 weeks, each bar its own %), the Change notes by kind, and Worth it per source.
const qPct=(a,b)=>b?Math.round(100*a/b):null;
function qWas(v,prev){if(v==null||prev==null)return'';return make('small',{class:'q-was'},v>prev?t('Up from {}% the 30 days before',prev):v<prev?t('Down from {}% the 30 days before',prev):t('Same as the 30 days before'))}
function qTile(value,name,means,was=''){return make('div',{class:'q-tile'},make('span',{class:'q-name'},t(name)),make('b',{},value==null?'–':value+'%'),make('small',{class:'q-means'},means),was)}
function qualityNodes(q){if(!q||!q.cards)return [make('p',{class:'q-empty'},t('Not enough to-dos yet. These numbers start once you decide on a few.'))];
 const decided=q.worth_it+q.dismissed,sent=(q.sent_as_written||0)+(q.sent_edited||0),few=t('Not enough to-dos yet');
 const tiles=[qTile(q.hit_rate,'Worth it',decided?t(['Of {} to-do you decided: acted on, not dismissed','Of {} to-dos you decided: acted on, not dismissed'],decided):few,qWas(q.hit_rate,q.previous?.hit_rate)),
  qTile(q.first_time_rate,'First try',q.do_it?t(['Of {} to-do started with Do it: no correction needed','Of {} to-dos started with Do it: no correction needed'],q.do_it):few,qWas(q.first_time_rate,q.previous?.first_time_rate)),
  qTile(q.finished_rate,'Finished',q.do_it?t(['Of {} to-do started with Do it: finished without a nudge','Of {} to-dos started with Do it: finished without a nudge'],q.do_it):few,qWas(q.finished_rate,q.previous?.finished_rate)),
  qTile(qPct(q.sent_as_written||0,sent),'Sent as is',sent?t(['Of {} draft sent: no edit or Change first','Of {} drafts sent: no edit or Change first'],sent):t('No drafts sent yet'))];
 const src=Object.entries(q.by_source||{}).sort((a,b)=>(b[1].worth_it+b[1].dismissed)-(a[1].worth_it+a[1].dismissed));
 const srcRow=([k,n])=>{const d=n.worth_it+n.dismissed;return make('div',SOURCE_TIPS[k]?{title:SOURCE_TIPS[k]}:{},make('span',{class:'grow'},k,SOURCE_TIPS[k]?make('small',{},SOURCE_TIPS[k]):''),make('span',{class:'q-n'},d?[t('{} of {}',n.worth_it,d)+' ',make('b',{},qPct(n.worth_it,d)+'%')]:t('None decided yet')))};
 return [make('p',{class:'learn-intro'},t('Last 30 days. Higher is better.')),make('div',{class:'q-tiles'},tiles),trendChart(q.trend),noteSplit(q.notes),
  ...src.length?[make('h3',{class:'q-h'},t('Worth it per source')),make('p',{class:'learn-intro'},t('Where to-dos came from, and how many you acted on of those you decided.')),make('div',{class:'list quality-sources'},make('div',{class:'q-head'},make('span',{class:'grow'},t('Source')),make('span',{},t('Acted on'))),src.map(srcRow))]:[]].filter(x=>x!=='')}
// Worth it over time, from the first decided to-do on, never empty periods before it: under 14 days one bar per day,
// then one per week from the first week, at most the last 8. Each bar's height and the number above it are that period's %,
// the day or week under it; how many were decided is under it on a computer, and always in the hover and aria label.
// An empty period inside the range is a thin baseline. Fewer than two periods with decisions: one plain line instead.
function trendChart(trend){const first=trend?.first,today=trend?.daily?.at(-1)?.start;if(!first||!today)return '';
 const at=s=>new Date(s+'T12:00'),ymdOf=d=>`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`,age=Math.round((at(today)-at(first))/864e5)+1,byDay=age<14;
 const monday=ymdOf((d=>{d.setDate(d.getDate()-(d.getDay()+6)%7);return d})(at(first)));
 const all=byDay?trend.daily:trend.weekly,rows=all.filter(r=>r.start>=(byDay?first:monday)),dated=n=>rows.filter(r=>r.worth_it+r.dismissed).length>=n;
 if(!dated(2))return make('p',{class:'trend-wait'},t('The chart starts after a few more days.'));
 const full=r=>localeDate(at(r.start),DL,byDay?{weekday:'short',day:'numeric',month:'short'}:{day:'numeric',month:'short'});
 // The label under a bar stays on one line: a weekday and date ("Mon 26", stacked on a phone), or a week's date with its
 // month only where it starts or changes ("Sep 7", "14", "21", "Oct 5")
 // A first week that starts mid-week shows its first day, as "Since" says ("20 Sept", not "14 Sept")
 const from=(r,i)=>at(!byDay&&!i&&r.start<first?first:r.start);
 const label=(r,i)=>{const d=from(r,i);if(byDay)return [make('span',{},localeDate(d,DL,{weekday:'short'})),' ',make('span',{},localeDate(d,DL,{day:'numeric'}))];
  return i&&from(rows[i-1],i-1).getMonth()===d.getMonth()?localeDate(d,DL,{day:'numeric'}):localeDate(d,DL,{day:'numeric',month:'short'})};
 const col=(r,i)=>{const n=r.worth_it+r.dismissed,name=byDay?full(r):t('Week of {}',full({start:ymdOf(from(r,i))})),tip=n?t('{}: {}% worth it, {} decided',name,r.hit_rate,n):t('{}: nothing decided',name);
  return make('div',{role:'listitem','aria-label':tip,title:tip},make('small',{class:'v'},n?r.hit_rate+'%':''),make('span',{class:'bar'},make('em',n?{style:{height:Math.max(2,r.hit_rate)+'%'}}:{class:'none'})),make('span',{class:'w'},label(r,i)),make('span',{class:'n'},n?t('{} decided',n):''))};
 const since=rows[0].start<=first,sub=byDay?t('Since {}. Each bar is that day’s Worth it.',full({start:first})):since?t('Since {}. Each bar is that week’s Worth it.',localeDate(at(first),DL,{day:'numeric',month:'short'})):t('Last 8 weeks. Each bar is that week’s Worth it.');
 return make('figure',{class:'trend'},make('figcaption',{},make('strong',{},t(byDay?'Worth it, day by day':'Worth it, week by week')),make('small',{},sub)),make('div',{class:'bars'+(byDay?' days':''),role:'list'},rows.map(col)))}
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
// After a quiet update: back on the tab and at the place the page was, unless it opened with a link (that link's view
// stays, also one that left the address once handled)
const linkAtLoad=!!location.hash;
function updateViewBack(){let v=null;try{v=JSON.parse(sessionStorage.getItem('tm-update-view')||'null');sessionStorage.removeItem('tm-update-view')}catch{}if(!v||!(Date.now()-v.at<6e4))return;
 if(v.tab&&!location.hash&&!linkAtLoad)document.querySelector(`nav button[data-tab="${CSS.escape(v.tab)}"]`)?.click();requestAnimationFrame(()=>scrollTo(0,+v.y||0))}
// A new release: the app's copy of the page goes, so the reload gets the new one from the Machine
async function shellDrop(){try{for(const k of await caches.keys())if(k.startsWith('tm-shell'))await caches.delete(k)}catch{}}
// A snooze whose time has passed is back, even before the service's next wake-up reaches this page: never show a past
// "Snoozed until", and refresh again right when the next one ends
let wakeTimer=null;
// The quiet Browser pill beside Settings: the Machine's browser view in a new tab, only when this Machine has one
function browserPill(st){const u=String(st?.browser_link||''),ok=/^https?:\/\//i.test(u),p=$('#settings-browser');for(const a of [$('#open-browser'),p?.querySelector('a')]){if(!a)continue;if(ok)a.href=u;else a.removeAttribute('href')}$('#open-browser').hidden=!ok;if(p)p.hidden=!ok}
function wakeSnoozed(st){const now=Date.now();let next=Infinity;for(const s of st?.suggestions||[]){if(s.status!=='snoozed'||!s.snoozed_until)continue;const at=Date.parse(s.snoozed_until);
  if(at<=now)Object.assign(s,{status:['pending','accepted','prepared','instructions'].includes(s.resume_status)?s.resume_status:'pending',snoozed_until:null,resume_status:null});else next=Math.min(next,at)}
 clearTimeout(wakeTimer);if(next<Infinity&&next-now<864e5)wakeTimer=setTimeout(()=>refresh(true),next-now+3000);return st}
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
// api/status as the changes since the answer this page holds (machine/web/status_delta.py): a part left out is the
// same, a row {"=":id} is that row as before. statusRaw stays as the server sent it; the page works on a copy.
let statusRaw=null;
const statusRow=x=>x&&typeof x==='object'&&!Array.isArray(x)&&Object.keys(x).length===1&&'='in x;
function statusMerge(r){if(!r._since){statusRaw=r;return JSON.parse(JSON.stringify(r))}if(!statusRaw||r._since!==statusRaw._token)return null;
 const out={...statusRaw};for(const k of r._gone||[])delete out[k];
 for(const[k,v]of Object.entries(r)){if(k==='_since'||k==='_gone')continue;
  if(Array.isArray(v)&&v.some(statusRow)){const was=new Map((statusRaw[k]||[]).map(x=>[typeof x?.id+':'+x?.id,x]));out[k]=v.map(x=>statusRow(x)?was.get(typeof x['=']+':'+x['=']):x);if(out[k].includes(undefined))return null}
  else out[k]=v}
 statusRaw=out;return JSON.parse(JSON.stringify(out))}
// What only Settings shows: not in the status, Settings fetches them (loadSettingsViews)
const SETTINGS_ONLY=['agents_settings','signatures','lookups','own_addresses'];
async function statusGet(){const since=statusRaw?._token,got=statusMerge(await request('api/status'+(since?'?since='+encodeURIComponent(since):''),{redirect:'manual'}));
 if(got)return got;statusRaw=null;return statusMerge(await request('api/status',{redirect:'manual'}))}
// What's new (state.whats_new, machine/store/whats_new.py): one small notice, tried once per opening of the dashboard, a
// moment after a live status. Never over a dialog, an open to-do, Talk or the hello, or while typing: then it waits for
// the next opening. The dialog is a lazy part (shell-whats-new.js), loaded only when there is something to tell.
let wnTried=false;
const wnQuiet=()=>!document.hidden&&!!state?.whats_new&&!document.querySelector('dialog[open]')&&!chatId&&!talk&&!talkViewOn()&&!state.greeting&&!document.activeElement?.closest?.('input,textarea,select,[contenteditable]');
function whatsNewMaybe(){if(wnTried||document.hidden||!state?.whats_new?.entries?.length)return;wnTried=true;setTimeout(()=>{if(wnQuiet())lazyRun('whatsnew',()=>{if(wnQuiet())whatsNewOpen(state.whats_new)})},600)}
async function refresh(poll=false){refreshes++;try{const edits=localEdits,next=wakeSnoozed(await statusGet());if(edits!==localEdits)return await refresh(poll);
 for(const k of SETTINGS_ONLY)if(!(k in next)&&k in state)next[k]=state[k];  // Settings' own (api/settings) stay until it fetches them again
 sessionCheck();shownCached=false;shownAt=Date.now();if(localCache.on){const sig=(next.suggestions||[]).map(x=>x.id+x.status).join();if(sig!==statusSig||Date.now()-statusSaved>15000){statusSaved=Date.now();statusSig=sig;localCache.put('status',next)}}
 state=next;netSet(false);cardsMerge();browserPill(state);if(state.source_url)$('#source-code').href=state.source_url;if(uiVersionCheck())return;focusKept(render);frRefresh();deviceRender();sendWatch();sentWhere();openPushLink();openChatLink(true);openSnoozeLink();openQuickLink();openResultLink();openSendLink();openCardLink();openFleetLink();openSharedLink();openTabLink();openConnectLink();whatsNewMaybe();if(lazyIn('graph')&&!$('#people').hidden&&(!poll||Date.now()-graphLoadedAt>=GRAPH_POLL_MS))await people(graphNode,true);if(lazyIn('calendar'))try{if(!$('#calendar').hidden)calendarView();else calBadge()}catch(e){errCaught(e);console.error(e)}if(refreshFailed){notice('');refreshFailed=false}retryIn=0;clearTimeout(retryTimer);if(outbox.items.length)outboxFlush();return true}catch(e){errCaught(e);refreshFailed=true;if(e.sessionGone||e.status===401||e.status===403)await cacheGone(!!e.sessionGone);if(e.offline){notice('');clearTimeout(retryTimer);retryIn=e.retryAfter||Math.min(30000,(retryIn||2500)*2);retryTimer=setTimeout(refreshWhenReady,e.retryAfter?retryIn:retryIn*(.8+Math.random()*.4));netSet(true,e.restarting)}else notice(e.message,true);staleLine(e.restarting?(netSetup?t('Setting up…'):t('Restarting · retrying')):shownAt?t('Offline · updated {}',hhmm(shownAt)):'Unavailable');if(!state?.suggestions)$('#suggestions').innerHTML=e.restarting?'<div class="empty all-clear first-look-empty restarting"><img class="sticker" src="brand/wave.webp" alt=""><div><strong class="backfill-run">'+(netSetup?t('Setting up your Machine…'):t('Your Machine is restarting.'))+'</strong><small>'+t('Back in a moment.')+'</small></div></div>':e.slow?'<div class="empty all-clear"><img class="sticker" src="brand/wave.webp" alt=""><div><strong>'+t(NET_SLOW_TEXT)+'</strong><small>'+t('Back in a moment.')+'</small></div></div>':'<div class="empty all-clear"><img class="sticker" src="brand/sad.webp" alt=""><div><strong>I can’t reach the assistant.</strong>I’ll keep trying every 30 seconds.</div></div>',notice('');return false}finally{refreshes--}}
$('nav').onclick=e=>{const t=e.target.closest('button');if(!t?.dataset.tab)return;for(const b of document.querySelectorAll('nav button[data-tab]')){b.classList.toggle('active',b===t);b.setAttribute('aria-current',b===t?'page':'false')}for(const s of document.querySelectorAll('main>section'))s.hidden=s.id!==t.dataset.tab;if(t.dataset.tab==='people'&&!graphSkip){const again=!!$('#people-view').innerHTML&&$('#people-view').dataset.mode!=='loading';lazyRun('graph',()=>{pairsSettle();people(graphNode,again)})}graphSkip=false;if(t.dataset.tab==='health')savedLogins();if(t.dataset.tab==='events'&&!$('#results').innerHTML){$('#results').innerHTML='<p class="muted">Loading…</p>';search()}if(t.dataset.tab==='fleet')fleetShown=fleetView(true);requestAnimationFrame(()=>{document.querySelectorAll('.fleet-tabs,.sub-tabs').forEach(tabsShow);kbLand()})};
// The desktop sidebar (from 1024px): the cards as a quiet list under the tabs, by section, each section folds (Done
// starts folded) and the fold is remembered; a filter on the titles; the whole sidebar folds to icons.
const sideStore={get:k=>{try{return localStorage.getItem(k)}catch{return null}},set:(k,v)=>{try{localStorage.setItem(k,v)}catch{}}};
const sideFolded=(()=>{try{const v=JSON.parse(sideStore.get('side-folded'));if(Array.isArray(v))return new Set(v)}catch{}return new Set(['done'])})();
// Waiting on others starts folded like Done, also where folds were saved before it existed: its saved state is that it's open
const sideOpen=k=>k==='waiting'?sideFolded.has(k+':open'):!sideFolded.has(k);
const CHEVRON='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>';
let sideGroups=[],sideCounts={},sideHTML='';
// The sidebar's groups show the first few (Done 10, an active group 8) and a quiet Show more adds 20 per tap; folding a
// group starts it over. Done counts every done card and loads the next ones from the Machine as it goes. A search shows
// every match, done cards too, also those not loaded yet. Done is newest first, the to-dos that look done among the
// closed ones by when they started to (doneAt).
const SIDE_STEP=20,sideShown={},sideFirst=k=>k==='done'?10:8;
const titleHas=(x,q)=>(String(x.title||'')+' '+cardWho(x)).toLowerCase().includes(q);  // its title or who it went to
function sideAll(items,key,q=''){let all=q?items.filter(x=>titleHas(x,q)):items;if(key!=='done')return all;
 const extra=[...pagers.get(doneKey())?.items||[],...q&&doneFound.q===q?doneFound.items:[]],seen=new Set(all.map(x=>x.id));
 return [...all,...extra.filter(x=>!seen.has(x.id)&&(!q||titleHas(x,q)))].sort((a,b)=>doneAt(b).localeCompare(doneAt(a)))}
function sideList(items,key){const each=sideAll(items,key),all=key==='done'?doneFold(each):each,n=sideShown[key]||sideFirst(key),total=key==='done'?Math.max(each.length,(state?.done_counts?.[scopeFilter]??0)+each.filter(looksDone).length):each.length;
 return {list:all.slice(0,n),more:all.length>n||total>each.length&&pagers.get(doneKey())?.next!=null,count:total}}
const sideMoreRow=key=>html`<button type="button" class="side-more" data-side-more="${key}">Show more</button>`;
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
  return html`<div class="side-group${['done','later','waiting'].includes(key)?' quiet':''}"><button type="button" class="side-head" data-side-fold="${key}" aria-expanded="${open}">${raw(CHEVRON)}<span>${title}</span><span class="count">${count}</span></button>${open?[cut.list.map(x=>sideRow(x,chatId)),cut.more?sideMoreRow(key):'']:''}</div>`}).filter(Boolean);
 const side=html`<div class="side-label" role="group" aria-label="To-dos">${[['all','All'],['work','Work'],['personal','Personal']].map(([v,t])=>html`<button type="button" data-scope="${v}" aria-pressed="${scopeFilter===v}">${t}</button>`)}</div>${parts.length?parts:html`<p class="side-empty">${q?'No to-dos match.':'No to-dos yet.'}</p>`}`;
 if(String(side)!==sideHTML){sideHTML=String(side);const back=sideKeep(box),focus=sideFocus(box);setHTML(box,side);back();focus();requestAnimationFrame(chatFades)}}
// A redraw (a reply from the Machine, whenever it lands) keeps the keyboard on the row or heading it was on.
function sideFocus(box){const f=document.activeElement,key=n=>n.getAttribute('href')||n.dataset.sideFold||n.dataset.sideMore||n.dataset.doneFold||n.dataset.scope;
 const k=f&&f!==box&&box.contains(f)&&key(f);if(!k)return()=>{};
 return()=>{const a=document.activeElement;if(a&&a!==document.body&&!box.contains(a))return;[...box.querySelectorAll('a[href],button')].find(n=>key(n)===k)?.focus({preventScroll:true})}}
// The card list scrolls in its own box (the computer's sidebar, the phone's drawer): a new card above keeps the rows in view where they were.
// Until the sidebar has scrolled (or taken focus, which can scroll it) it is at its top and there is nothing to keep: reading
// scrollTop while the page is still drawing forced a layout of the whole page before the first to-do was painted.
var sideMoved=false;for(const t of ['scroll','focusin'])document.addEventListener(t,e=>{if(!sideMoved&&e.target.closest?.('.app-side'))sideMoved=true},{capture:true,passive:true});
function sideKeep(box){const sc=sideMoved&&[box,box.closest('.app-side')].find(x=>x&&x.scrollTop>0);if(!sc)return()=>{};const edge=sc.getBoundingClientRect().top,key=n=>n.getAttribute('href')||n.dataset.sideFold||n.dataset.sideMore||n.dataset.doneFold;
 const row=[...box.querySelectorAll('a[href],[data-side-fold],[data-side-more],[data-done-fold]')].find(n=>n.getBoundingClientRect().bottom>edge);if(!row)return()=>{};const k=key(row),top=row.getBoundingClientRect().top;
 return()=>{const n=[...box.querySelectorAll('a[href],[data-side-fold],[data-side-more],[data-done-fold]')].find(x=>key(x)===k);if(n){const d=n.getBoundingClientRect().top-top;if(Math.abs(d)>=1)sc.scrollTop+=d}}}
$('#side-find').addEventListener('input',()=>sideCards());
$('#side-find').addEventListener('keydown',e=>{if(e.key==='Escape'){e.target.value='';sideCards()}if(e.key==='Enter'){const a=$('#side-cards a');if(a)a.click()}});
$('#side-cards').addEventListener('click',e=>{const f=e.target.closest('[data-side-fold]');
 if(f){const k=f.dataset.sideFold==='waiting'?f.dataset.sideFold+':open':f.dataset.sideFold;sideFolded.has(k)?sideFolded.delete(k):sideFolded.add(k);delete sideShown[k];sideStore.set('side-folded',JSON.stringify([...sideFolded]));sideCards();return}
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
function sideTipText(el){if(el.id==='side-toggle')return el.getAttribute('aria-label')+' · '+SIDE_KEY;if(el.id==='side-search')return 'Search';if(el.id==='live')return $('#updated').textContent.trim()||'Refresh';
 if(el.matches('.app-side .head-side>.settings-link'))return (el.querySelector('.lbl')?.textContent.trim()||el.getAttribute('aria-label')||'')+(el.dataset.keys?' · '+el.dataset.keys:'');
 return (el.getAttribute('aria-label')||'')+(el.dataset.keys?' · '+el.dataset.keys:'')}
function sideLabels(){for(const b of document.querySelectorAll('.app-side nav [data-tab]')){const name=b.querySelector('.nl')?.textContent.trim()||'',n=+(b.querySelector('.badge')?.textContent||0),t=b.dataset.tab,c=sideCounts||{};
  const tr=window.t,more=t==='inbox'?(c.foryou?tr('{} for you',c.foryou):'')||(n?tr('{} waiting',n):''):!n?'':t==='health'?tr(['{} needs a look','{} need a look'],n):t==='people'?tr('{} waiting',n):t==='calendar'?tr('{} today',n):String(n);
  const label=more?name+' · '+more:name;if(b.getAttribute('aria-label')!==label)b.setAttribute('aria-label',label)}
 const live=$('#live'),u=$('#updated').textContent.trim();if(u&&live.getAttribute('aria-label')!==u)live.setAttribute('aria-label',u)}
function sideTipHide(){clearTimeout(sideTipTimer);if(sideTipFor){if(sideTipFor.dataset.tipTitle!==undefined){sideTipFor.title=sideTipFor.dataset.tipTitle;delete sideTipFor.dataset.tipTitle}sideTipFor=null}sideTip.hidden=true}
function sideTipShow(el){if(document.documentElement.dataset.side!=='collapsed'||!matchMedia('(min-width:1024px)').matches)return;sideLabels();const text=sideTipText(el);if(!text)return;
 if(el.title){el.dataset.tipTitle=el.title;el.title=''}  /* no second, native tooltip */
 sideTipFor=el;sideTip.textContent=text;const r=el.getBoundingClientRect(),side=$('#app-side').getBoundingClientRect();sideTip.style.left=Math.round(side.right+8)+'px';sideTip.style.top=Math.round(r.top+r.height/2)+'px';sideTip.hidden=false}
const SIDE_TIP_ON='.app-side nav [data-tab],.side-sub a,#side-toggle,#side-search,.app-side .head-side>.settings-link,#live';
$('#app-side').addEventListener('pointerover',e=>{const el=e.target.closest(SIDE_TIP_ON);if(!el||el===sideTipFor||e.pointerType==='touch')return;sideTipHide();sideTipTimer=setTimeout(()=>sideTipShow(el),300)});
$('#app-side').addEventListener('pointerout',e=>{const el=e.target.closest(SIDE_TIP_ON);if(el&&!el.contains(e.relatedTarget))sideTipHide()});
$('#app-side').addEventListener('focusin',e=>{const el=e.target.closest(SIDE_TIP_ON);sideTipHide();if(el&&focusVisible(el))sideTipShow(el)});
$('#app-side').addEventListener('focusout',sideTipHide);$('#app-side').addEventListener('click',sideTipHide);addEventListener('scroll',sideTipHide,{passive:true});
addEventListener('keydown',e=>{if(e.key==='Escape')sideTipHide();if(!(e.ctrlKey||e.metaKey)||e.altKey||e.shiftKey||e.key.toLowerCase()!=='b'||!matchMedia('(min-width:1024px)').matches||e.target.closest?.('textarea,input,select,[contenteditable]'))return;
 e.preventDefault();sideSet(document.documentElement.dataset.side!=='collapsed')});
{const o=new MutationObserver(()=>sideLabels());o.observe($('.app-side nav'),{subtree:true,childList:true,characterData:true});o.observe($('#updated'),{subtree:true,childList:true,characterData:true})}
sideSet(document.documentElement.dataset.side==='collapsed',false);
$('#side-toggle').onclick=()=>sideSet(document.documentElement.dataset.side!=='collapsed');
// Search, folded to its icon: opens the palette as the box does (shell-keys.js), the sidebar stays folded
$('#side-search').addEventListener('click',e=>{if(document.documentElement.dataset.side==='collapsed'&&matchMedia('(min-width:1024px)').matches){e.preventDefault();palOpen({todos:true})}});
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
