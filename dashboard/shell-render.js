const mailCheckSlot=()=>state?.mail_check?.emails?lazyIn('mailcheck')?mailCheckBlock():(lazyRun('mailcheck',render),''):'';
const learnedSlot=()=>state?.first_look_learned?lazyIn('learned')?learnedCard():(lazyRun('learned',render),''):'';
const SKELETON=nodeHTML($('#suggestions .skeleton'));  // the page's own loading outline
// Where a decision came from, in the page's language ("on the dashboard", not "via dashboard"). Unknown sources: "via <source>".
const DECISION_VIA={auto_follow_up:'by automated follow-ups',dashboard:'on the dashboard',telegram:'on Telegram',assistant:'automatically',fleet:'from the Fleet','owner-chat':'in the chat',voice:'by voice',signed_in:'after a sign-in',agent:'by an agent',elsewhere:'elsewhere'};
const decisionVia=source=>DECISION_VIA[source]?t(DECISION_VIA[source]):t('via {}',source);
// Whether Coming back later, Promises and Done are open, kept while a chat stands in for the lists, so closing the chat
// brings back the list the to-do is in as it was (Esc from a to-do in Coming back later lands on that to-do, list open).
const listOpenKept={};const listOpen=id=>{const d=document.getElementById(id);if(d)listOpenKept[id]=d.open;return !!listOpenKept[id]};
// Feedback's rows name where the to-dos came from (assistant.py TODO_SOURCE); the ones that need it say a little more
const SOURCE_TIPS={'Added by you':'Made with New to-do','The Machine itself':'Problems in The Machine, like an error','Phone notifications':'Texts and alerts on your phone','Other':'The source is gone or unknown'};
// render('view'): only what opening or closing a chat changes (the to-do list, the sidebar, the chat), when the data is
// the same as at the last whole render; Learning, Connections and the rest stay as they are drawn (a chat's open or
// close redrew them all, some 40 ms of each).
let drawnWhole=null;
// The app icon's badge: the To-dos count in the sidebar (what needs the owner now), set on each render from the Machine's
// own data, cleared at 0. Work or Personal alone leaves it as All has it; a push sets it the same way (sw.js, waiting_count).
function appBadge(n){try{if(navigator.setAppBadge)(n?navigator.setAppBadge(n):navigator.clearAppBadge()).catch(()=>{})}catch{}}
function render(view){const first=!drawnWhole&&!view&&/^(#todos|#chat=[a-f0-9]{16})?$/.test(location.hash);  // a page's first drawing on To-dos (below)
scopeSync(state.locale);try{talkFromStatus();talkViewPaint()}catch{}applyLocale(state.locale);renderNeedsYou();if(!first)renderNotify();fixedLoad();try{palAskShow()}catch{}
const finishedOpen=listOpen('finished-list'),laterOpen=listOpen('later-list'),promisesOpen=listOpen('promises-list'),waitOpen=listOpen('waiting-list');
const drafts=Object.fromEntries([...document.querySelectorAll('#suggestions textarea,#suggestions .fleet-card input[id]')].filter(t=>t.value).map(t=>[t.id,t.value]));
const moreOpen=[...document.querySelectorAll('#suggestions article[id] .more-actions[open]')].map(d=>d.closest('article[id]').id);  // a refresh keeps an opened More menu open
const shown=state.suggestions.filter(s=>scopeFilter==='all'||s.scope===scopeFilter);
const outstanding=shown.filter(s=>!closed(s)&&s.status!=='snoozed').sort(openOrder),later=shown.filter(s=>s.status==='snoozed'),finished=shown.filter(closed);
const lookDone=outstanding.filter(looksDone),waitingOn=outstanding.filter(waitsOnOthers),open=outstanding.filter(s=>!looksDone(s)&&!waitsOnOthers(s)&&!setAside(s));
later.push(...outstanding.filter(setAside));  // Still needed? without an answer: folded into Coming back later, under its own heading
const fleetCards=scopeFilter==='personal'?[]:fleetCardsOf(fleetData);
const needs=[...fleetCards,...open.filter(s=>placeOf(s)==='needs')],preparing=open.filter(s=>placeOf(s)==='preparing'),ready=open.filter(s=>placeOf(s)==='ready');
// A new owner's first view leads with the to-do their hello names (Store.greeting): first in its list, its list first
const leadId=state.greeting?.line?.card,leadIn=leadId&&[['foryou',[...ready,...needs]],['preparing',preparing]].find(([,l])=>l.some(s=>s.id===leadId));
const leadFirst=l=>{const i=leadIn?l.findIndex(s=>s?.id===leadId):-1;if(i>0)l.unshift(...l.splice(i,1));return l};
leadFirst(preparing);
const fuv=fuSplit(ready,needs,preparing);  // a board's follow-ups are one to-do (fuGroupCard)
fuv.foryou=leadFirst(forYouList(fuv.ready,fuv.needs));
// What Talk sees: every open to-do the lists show, in their order (For you, Preparing, Waiting on others, Later).
// One that looks done sits in Done, so it isn't here (find_todos still finds it)
talkTodos=[...leadFirst(forYouList(ready,needs)).filter(s=>plainTodo(s)&&state.suggestions.includes(s)).map(s=>[s,ready.includes(s)?'ready':'needs']),...preparing.map(s=>[s,'preparing']),
 ...waitingOn.map(s=>[s,'waiting']),...later.map(s=>[s,'later'])];
{const tips=firstTips(),own=new Set(shown.map(s=>s.id));tipSend=tips.includes('send')&&fuv.foryou.find(s=>plainTodo(s)&&own.has(s.id)&&sendTipFits(s))?.id||'';tipChange=!tipSend&&tips.includes('change')?'next':''}
const fuHidden=ready.length+needs.length+preparing.length-fuv.ready.length-fuv.needs.length-fuv.preparing.length;
// What the list shows (a board's follow-ups are one to-do, a batch going out one progress line): All clear only when nothing is
const anyShown=fuv.foryou.length+fuv.preparing.length+(scopeFilter==='personal'?0:fuShownProgress().length);
// Open cards: due soon first, then newest first (openOrder).
// Later: in the order they come back, with a heading per day, then the ones Still needed? set aside. Done: the last 7 days.
later.sort((a,b)=>(setAside(a)-setAside(b))||(a.snoozed_until||'').localeCompare(b.snoozed_until||''));

const recent=finished.sort((a,b)=>closedAt(b).localeCompare(closedAt(a))),doneTotal=state.done_counts?.[scopeFilter]??recent.length;
{const seen=doneTotal+':'+recent.slice(0,30).map(s=>s.id).join(',');if(seen!==doneSeen){doneSeen=seen;pagerDrop('done')}}if(!first)donePager();
putIfChanged($('#suggestion-summary'),make('div',{class:'summary-row'},make('div',{class:'scope-filter',role:'group','aria-label':'Show'},[['all','All'],['work','Work'],['personal','Personal']].map(([v,label])=>make('button',{type:'button','data-scope':v,'aria-pressed':scopeFilter===v},label)))));
putIfChanged($('#suggestion-stats'),make('div',{class:'stats'},[[fuv.foryou,'For you','mint','foryou'],[fuv.preparing,'Preparing','lavender','preparing'],[later,'Later','lavender','later']].map(([items,title,tone,key])=>make('button',{type:'button',class:`stat t-${tone}${items.length?'':' zero'}`,'data-fold-tile':key,'aria-expanded':!!items.length&&(key==='later'?laterOpen:!folded.has(key)),
 'aria-label':items.length?t('{} {}, tap to show or hide',items.length,t(title)):items.length+' '+t(title),...(items.length?{}:{disabled:''})},make('b',{},items.length),make('span',{},title)))));
$('#badge-inbox').textContent=(open.length-fuHidden+(fleetData?fleetCards.length:scopeFilter==='personal'?0:state.fleet?.waiting||0))||'';if(scopeFilter==='all'&&!shownCached)appBadge(+$('#badge-inbox').textContent||0);$('#tab-fleet').hidden=!state.fleet?.on;$('#badge-fleet').textContent='';
// "All clear" only when the Machine itself just said so: a copy from the device keeps the loading outline instead
if(!shownCached)try{localStorage.setItem('skeleton-cards',String(Math.min(4,outstanding.length+fleetCards.length)))}catch{}
const loading=shownCached&&!outstanding.length&&!fleetCards.length;$('#suggestions').toggleAttribute('aria-busy',loading);
const foldsBack=foldsKeep($('#suggestions'));
// Snoozed cards are out of the way by choice: folded by default, open state kept across refreshes. Waiting on others too.
if(!chatOpen())listBack(),drawKept($('#suggestions'),html`${repeatOfferLine()}${mailCheckSlot()}${justDoneList(justDone(finished))}${scopeNote(!anyShown&&!loading)}${firstLookNote(anyShown)}${anyShown?'':loading?SKELETON:scopeFilter!=='all'?'':orEmpty(firstLookEmpty(firstLookInfo(state.review_live||{})))||orEmpty(firstLookEnd())||html`<div class="empty all-clear"><button class="poke" type="button" aria-label="Poke the robot" title="Poke me"><img class="sleepy" src="${pokeAwake?'brand/wave.webp':clearPose()}" alt="${checkBusy()?'The Machine checking':'The Machine resting'}"></button><div><strong>All clear.</strong><button type="button" class="clear-more" data-clear-more aria-expanded="${clearOpen}"><span class="poke-line">${pokeLine||clearLine()}</span></button></div><div class="clear-check">${clearCheck()}</div>${pokes>=PLAY_AFTER?PLAY_BUTTON:''}</div>`}${fuSendingCards()}${[[fuv.foryou,'For you','foryou'],[fuv.preparing,'Preparing','preparing']].sort((a,b)=>(b[2]===leadIn?.[0])-(a[2]===leadIn?.[0])).filter(([items])=>items.length).map(([items,title,key])=>html`<div class="section-head" id="section-${key}" data-fold="${key}" role="button" tabindex="0" aria-expanded="${!folded.has(key)}"><h2>${title}</h2><span class="count">${items.length}</span>${clearHead(key,fuv)}${sectionNote(key,items)}</div>${folded.has(key)?'':items.map(s=>typeof s==='string'||s instanceof SafeHTML?s:suggestionCard(s,title))}`)}${learnedSlot()}${waitingOn.length?html`<details id="waiting-list" ${waitOpen?'open':''}><summary id="waiting-head"><span>${t('Waiting on others')}</span><span class="count">${waitingOn.length}</span></summary>${waitingOn.map(s=>suggestionCard(s,'Waiting on others'))}</details>`:''}${later.length?html`<details id="later-list" ${laterOpen?'open':''}><summary id="later-head"><span>Coming back later</span><span class="count">${later.length}</span></summary>${laterCards(later)}</details>`:''}${promisesList(promisesOpen)}<details id="finished-list" ${finishedOpen?'open':''}><summary id="finished-head"><span>Done / dismissed</span><span class="count">${doneTotal+lookDone.length}</span></summary>${(()=>{const l=recent.find(s=>s.id===linkedCardId);return l&&!pagers.get(doneKey())?.items.some(x=>x.id===l.id)?suggestionCard(l):''})()}${pagerSlot(doneKey(),lookDone.length?'':'Nothing finished or dismissed yet.')}</details>`,()=>focusKept(render));if(!chatOpen())pagerMount($('#suggestions'));firstLookFill();
// For you in the sidebar: the same items as its count, the header and the section, a Fleet item as its row (fleetSide)
const sideRows=l=>fuSide(l).map(x=>x?.side||x).filter(plainTodo),sideForYou=sideRows(fuv.foryou);
sideCounts={foryou:sideForYou.length,preparing:fuv.preparing.length,later:later.length,promises:(state.promises||[]).filter(p=>['open','card'].includes(p.state)).length};sideCards([[sideForYou,'For you','foryou'],[sideRows(fuv.preparing),'Preparing','preparing'],[waitingOn,'Waiting on others','waiting'],[later,'Later','later'],[[...lookDone,...recent],'Done','done']]);
{const c=chatOpen();document.body.classList.toggle('chat-open',!!c);if(c)chatMount(c.id,chatView(c,[[sideForYou,'For you','foryou'],[sideRows(fuv.preparing),'Preparing','preparing'],[waitingOn,'Waiting on others','waiting'],[later,'Later','later'],[[...lookDone,...recent],'Done','done']]))}pageHead();
for(const[id,v]of Object.entries(drafts)){const t=document.getElementById(id);if(t&&t.value!==v){t.value=v;t.classList.add('filled')}}
for(const id of moreOpen){const menu=document.getElementById(id)?.querySelector('.more-actions');if(menu)menu.open=true}foldsBack();
fleetSync();
// A page's first drawing on To-dos (the device's copy, else the Machine's first answer): the to-dos, the sidebar and a chat now,
// and the rest (the Done list, Learning, Connections, Settings, the other tabs' parts) just after that first paint, not before it.
// A link to another tab or part (#settings/notify) draws it all at once, since that part is the one it opens on
if(first){const later=()=>{if(drawnWhole)return;try{render('whole')}catch(e){errCaught(e);console.error(e)}};  // caught as in refresh, where it ran before
requestAnimationFrame(()=>setTimeout(later));setTimeout(later,300);return}
if(view==='view'&&drawnWhole===state)return;drawnWhole=state;lazySoon();  // the parts that load when first needed come after (shell-core.js)
const choiceTone={accept:'mint',complete:'mint',reject:'muted',snooze:'lavender',other:'amber',reopen:'lavender',undo:'lavender',retry:'lavender',update:'lavender'};
// One decision on Learning: the to-do, what was chosen, through what and when, and the note that came with it
const DECISION_LABEL={accept:'Accepted',reject:'Not needed',snooze:'Saved for later',other:'Instructions',complete:'Done',send:'Approved send',reopen:'Reopened',undo:'Reopened',retry:'Trying again',update:'Updated',prepare_ahead:'Prepared ahead',bounced:'Email bounced'};
const decisionRow=d=>{const a=make('article',{},make('h3',{},d.title||state.suggestions.find(s=>s.id===d.suggestion_id)?.title||t('To-do')),
  make('div',{class:'row'},chipNode(d.source==='auto_follow_up'&&d.choice==='send'?'Sent automatically':DECISION_LABEL[d.choice]||d.choice,choiceTone[d.choice]||'muted'),make('small',{},decisionVia(d.source)),make('small',{},timeNode(d.created_at,true))),
  d.annotation?make('p',{class:'note'},'Earlier message was matched incorrectly. The correction is recorded.'):'',d.feedback?make('blockquote',{},d.feedback):'');
 a.style.setProperty('--c',`var(--${({mint:'mint',muted:'faint',lavender:'lavender',amber:'amber'})[choiceTone[d.choice]||'muted']})`);return a};
// Learning's own parts are drawn when its file is in (learning-missed.js draws them then)
const learnIn=lazyIn('learning'),settingsIn=lazyIn('settings'),connIn=lazyIn('connections');if(learnIn)renderQuality();
if(learnIn&&learnEdit==null)setHTML($('#facts'),learnedList());if(learnIn)setHTML($('#learn-changes'),learnChanges());renderShare();renderVotes();  // an open editor keeps what was typed until Save or Cancel
$('#decisions').replaceChildren(...clipNodes('decisions',clipRows(state.decisions,decisionRow),()=>[make('p',{class:'muted'},'No decisions yet.')],5));if(learnIn)learnTabs();
if(connIn)drawConnectors();
if(state.manage_url){$('#manage').href=state.manage_url;$('#manage').hidden=false;$('#sign-out').hidden=false;$('#report-problem').href=new URL('/support',state.manage_url).href;$('#report-problem').removeAttribute('target');$('#connect-more').replaceChildren(make('div',{class:'connect-pills'},make('a',{class:'manage',href:'#connect=google'},'Connect Google'),make('a',{class:'manage',href:'#connect=microsoft'},'Connect Microsoft'),
 make('a',{class:'manage',href:'#connections=add'},'Add another source')),make('a',{class:'connect-ask',href:new URL('/connectors',state.manage_url).href},'Missing a source? Ask for it.'))}
// drawn once, so an open disclosure stays open (and the page stays put) through each refresh
else if($('#connect-more .connect-cli')?.dataset.lang!==I18N.lang){const cmds=['assistant connect gmail','assistant connect outlook','assistant connect'],line=t('On this Machine, run {} for Google, {} for Microsoft, or {} for more.','\u0001','\u0002','\u0003');
 $('#connect-more').replaceChildren(make('details',{class:'connect-cli','data-lang':I18N.lang},make('summary',{},'For developers: set up from the terminal'),make('p',{},line.split(/([\u0001-\u0003])/).map(x=>x.length===1&&x<'\u0004'&&x>'\u0000'?make('code',{},cmds[x.charCodeAt(0)-1]):x))))}
// Connections' badge: only sources that need the owner (orange); amber ones retry or catch up by themselves
const issues=state.connectors.filter(c=>connectorTone(c)==='orange').length;$('#badge-health').textContent=issues||'';if(connIn)renderHealthTabs();
const expandedReview=new Set([...document.querySelectorAll('#analyses details[open]')].map(d=>d.id));
renderModelUsage();const rh=state.review_health||{},wk=rh.worker;const pend=rh.pending||0;$('#review-summary').textContent=`${t('{} waiting',pend.toLocaleString(DL))}${rh.set_aside?` · ${t('{} set aside',rh.set_aside.toLocaleString(DL))}`:''} · ${t('{} checked',((rh.total||0)-pend).toLocaleString(DL))} · ${rh.last_completed?t('last {}',ago(rh.last_completed)):t('last not yet')}. ${t(wk?.status==='recovering'?'Paused for a moment; it retries by itself.':['starting','running'].includes(wk?.status)?t('Checking now (started {}).',ago(wk.started_at)):wk&&!wk.review_saved&&wk.status!=='ok'?t('Last run {} {}; it retries.',t(wk.status.replace('_',' ')),ago(wk.finished_at)):state.review_live?.queue?.why==='mail'?(state.review_live.queue.first?'The first one starts when your mail is in.':'Next one when your new mail is in.'):pend?'Next one shortly.':'Next one when new messages come in.')}`.trim();
const reviewError=v=>({ai_connection_reset:'The AI connection dropped.',ai_connection_closed:'The AI connection closed.',ai_timeout:'The AI request timed out.',ai_request_failed:'The AI request failed.',review_not_finished:'The run ended before saving its check.',run_interrupted:'The run stopped before saving its check.'}[v]||'The check did not save a conclusion.');
const runFailure=r=>({model_idle_timeout:'The AI stopped responding.',bridge_error:'A tool connection failed.',rate_limited:'The AI service asked us to wait.',usage_limited:'The AI usage limit was reached.',connection_error:'Briefly interrupted.',runtime_timeout:'The run timed out.',runtime_aborted:'The run was stopped.',runtime_lost:'The run could not be found after recovery.',runtime_error:'The runtime reported an error.'}[r.error||r.last_error]||(['error','aborted','lost','timed_out'].includes(r.status)?'The runtime reported a failure; its original explanation was not retained.':''));
// limitNote and resetAction as nodes, for the runs list
const resetActionNode=m=>{if(!m)return '';if(m.can_reset)return make('button',{type:'button',class:'ghost','data-model-reset':''},'Use a reset');
 const href=safeURL(m.usage_page);return href?make('a',{class:'head-link',href,target:'_blank',rel:'noopener'},m.resets?'Open ChatGPT':'See resets in ChatGPT'):''};
const limitNoteNode=m=>{if(!m?.limit_reached)return '';const r=resetActionNode(m);
 return make('p',{class:'limit-note'},make('strong',{},t(m.chatgpt?'ChatGPT limit reached':'Model limit reached')),(m.limit_resets_at?t(', resets at {}',clockAt(m.limit_resets_at)):'')+(r?' · ':''),r)};
$('#review-runs').replaceChildren(...clipNodes('review-runs',clipRows((state.review_runs||[]).filter(r=>!REVIEW_ACTIVE.includes(r.status)&&!(r.review_saved&&!runFailure(r))),r=>{
const active=['starting','running','recovering'].includes(r.status),saved=r.review_saved;
const label=saved?'Check saved':active?'In progress':r.pending_count?'Retry needed':r.status==='ok'?'Finished':'Run ended';
const outcome=saved?`${r.checked_count} signal versions saved.${r.pending_count?` ${r.pending_count} still waiting.`:''}`:r.pending_count?t(['{} message still to check. Nothing is lost.','{} messages still to check. Nothing is lost.'],r.pending_count):r.claimed_count?'Nothing remains waiting from this run.':'No signals claimed.';
const seconds=r.duration_seconds||0,duration=seconds<60?`${seconds}s`:`${Math.floor(seconds/60)}m ${seconds%60}s`;
const phase=({runtime:'runtime',model:'AI response',bridge:'tool connection',connection:'connection',queue:'waiting to start',provider:'AI service',tool:'tool execution',gateway_draining:'Gateway restarting'})[r.error_phase||r.last_error_phase];
const failure=runFailure(r),limited=['rate_limited','usage_limited'].includes(r.error||r.last_error)&&state.model_status?.limit_reached;
return make('div',{},chipNode(label,saved?'mint':active?'amber':r.pending_count?'orange':''),timeNode(r.started_at,true),make('p',{},outcome),make('small',{},t('Duration {}',duration)+' · '+t(['{} start attempt','{} start attempts'],r.attempts||1)),
 failure?make('p',{},failure+(saved?' The check was saved; saved signal versions will not be replayed.':'')):'',limited?limitNoteNode(state.model_status):'',phase?make('small',{},t('Where: {}',t(phase))+(r.error_at?' · '+ago(r.error_at):'')):'',r.retry_at?make('small',{},t('Next check: {}',date(r.retry_at))):'');
}),()=>[make('div',{class:'muted'},'No runs that ended without a check.')]));

renderReviewLive();$('#analyses').replaceChildren(...clipNodes('analyses',clipRows(state.analyses.filter(a=>a.status!=='running'||!(state.review_live?.runs||[]).length),a=>{const id='review-'+a.started_at,complete=a.status==='complete',running=a.status==='running',recovered=!complete&&a.remaining_count===0;const count=complete?(a.checked_count??JSON.parse(a.items||'[]').length):JSON.parse(a.items||'[]').length;const status=complete?'Checked':running?'Checking':recovered?'Recovered':'Retry needed';const detail=complete?(a.summary||'Check saved.'):`${a.last_error?reviewError(a.last_error):running?'Check in progress.':reviewError(null)} ${recovered?'These signals were checked in a later run.':!running?`${a.remaining_count??count} still waiting; the review worker will retry them.`:''}`;return make('div',{},chipNode(status,complete||recovered?'mint':running?'amber':'orange'),make('span',{class:'grow'},complete?t('{} messages checked',count):running?t('{} messages being checked',count):t('{} signals in the original check',count)),timeNode(a.started_at),
 a.attempts>1?make('small',{},t(['Resumed {} time','Resumed {} times'],a.attempts-1)):'',complete&&a.last_error?make('small',{},t('{} Check recovered and saved.',reviewError(a.last_error))):'',(()=>{const x=make('details',{id},make('summary',{},'Check notes'),make('p',{},detail));if(expandedReview.has(id))x.open=true;return x})())}),()=>$('#review-live').firstChild?[]:[make('div',{class:'muted no-reviews'},'No checks yet.')]));
const deliveryTone=s=>({sent:'mint',delivered:'mint',queued:'lavender',pending:'lavender',uncertain:'amber',failed:'orange'}[s]||'muted');
// One delivery on Connections: what happened, to which to-do, when, and why it waits
const DELIVERY_LABEL={sent:'Sent',queued:'Waiting to send',uncertain:'Checking delivery',cancelled:'Canceled',previewed:'Preview, not sent'};
const DELIVERY_ERROR={gateway_preflight_failed:'Couldn’t send yet. It retries.',delivery_not_admitted:'This send was held back. It retries.',delivery_outcome_unknown:'Not sure it arrived. Checking before it resends.',interrupted_delivery:'Send interrupted. Checking before it resends.'};
const deliveryRow=d=>make('div',{},chipNode(DELIVERY_LABEL[d.status]||d.status,deliveryTone(d.status)),make('span',{class:'grow'},state.suggestions.find(s=>s.id===d.suggestion_id)?.title||d.suggestion_id),timeNode(d.updated_at),
 d.error?make('small',{class:'error'},DELIVERY_ERROR[d.error]||d.error):'',d.needs_edit?make('small',{},'Telegram update pending'):'');
$('#deliveries').replaceChildren(...clipNodes('deliveries',clipRows(state.deliveries,deliveryRow),()=>[make('div',{class:'muted'},'No deliveries yet.')]));if(settingsIn){renderHours();renderLocale();renderAgents();renderSignatures();renderLookups();renderAddresses();renderSecurity()}renderShareOffer();if(settingsIn){renderVoices();renderSkills()};
if(!shownCached&&!netDown){lastOk=Date.now();$('#live').classList.remove('stale');$('#stale-note').hidden=true}if(!shownCached&&!kbLanded){kbLanded=true;requestAnimationFrame(()=>setTimeout(()=>kbLand()))}/* the page's first focus, once the to-dos are in and painted: its focus forced a layout before the first paint */if(netOut)liveLine();else $('#updated').replaceChildren(make('span',{class:'lbl'},'Updated '),hhmm(shownAt||Date.now()));
for(const c of state.connectors.filter(c=>![...$('#account').options].some(o=>o.value===c.id))){let o=new Option((c.display_name||c.email)+' · '+service(c.service),c.id);$('#account').add(o)}
}
