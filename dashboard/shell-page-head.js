// The Routines page loads when first needed (routines-page.js, dashboard_parts.LAZY): it draws once its part is in.
const routinesView=force=>lazyRun('routines',()=>routinesLoad(force));
// A to-do a routine made says "From your routine X" (todos-cards.js routineSource), X a link to #routines/<id>: the
// Routines page with that routine in view (routines-page.js rtReveal).
let rtWant='';
function openRoutineLink(){const m=/^#routines\/([a-f0-9]{32})$/.exec(location.hash);if(!m)return false;
 history.replaceState(null,'',location.pathname+location.search+'#routines');rtWant=m[1];if($('#routines').hidden)showTab('routines');else routinesView();return true}
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#routines/"]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey||e.defaultPrevented)return;
 e.preventDefault();history.replaceState(null,'',location.pathname+location.search+a.getAttribute('href'));openRoutineLink()});
$('nav').addEventListener('click',e=>{const t=e.target.closest('button')?.dataset.tab;if(t==='routines')routinesView();if(t==='feedback')lazyRun('learning',()=>{});
 if(t==='calendar')lazyRun('calendar',()=>{if(!calRouting&&(e.isTrusted||!/^#calendar\?/.test(location.hash))){calSetAll(calDay(0));calFrom=calDay(0);calTo=calDay(7);calMoreFailed={};calUp=false;calPush(true);scrollTo({top:0})}calendarView(true)});
 else if(t&&/^#calendar\?/.test(location.hash))history.replaceState(null,'',location.pathname+location.search)});
DESK.addEventListener?.('change',()=>{if(!$('#calendar').hidden&&lazyIn('calendar')){calPush(true);calShowNow()}});
addEventListener('hashchange',()=>{if(lazyIn('calendar')&&calReturn&&!/^#chat=/.test(location.hash)&&!chatId){calReturn=false;showTab('calendar')}});
// A title over the main area on a computer: the tagline on To-dos, else the tab's name
// The footer's Help: the help article for what's on screen (themachine.computer/help, the articles in docs/help/)
const HELP='https://themachine.computer/help/',HELP_FOR={account:'plans-and-billing',inbox:'cards',calendar:'calendar',routines:'routines',events:'dashboard',people:'graph',fleet:'fleet',feedback:'dashboard',health:'connections',general:'settings',notify:'notifications',security:'security-levels',writing:'writing',skills:'skills',apps:'ai-connections',model:'model'};
const GRAPH_HELP={people:'people',orgs:'organizations',projects:'projects'};  // the Graph's Help link: the page of the list it shows
function helpLink(tab){const a=$('#help-link'),slug=(tab==='people'&&GRAPH_HELP[graphShown])||HELP_FOR[tab==='settings'?settingsNow:tab]||'';if(a&&a.href!==HELP+slug)a.href=HELP+slug}
const PAGE_TITLES={calendar:'Calendar',routines:'Routines',events:'Messages',people:'Graph',fleet:'Fleet',feedback:'Learning',health:'Connections',settings:'Settings'};
// The Graph's title is the pane on screen, with Graph as a quiet crumb and the same count as its row in the sidebar
// A page's section, as its breadcrumb says: an organization opened from a project is under Organizations
const graphNodePane=id=>id==='me'?'people':/^(team:)?org:/.test(id)?'orgs':/^(team:)?project:/.test(id)?'projects':'people';  /* team:…: a record only teammates have */
function graphHead(){if(/^promise:/.test(graphDrawn||''))return html`<div><p class="page-crumb">Graph</p><h2 class="page-title">Promise</h2></div>`;const name=GRAPH_SUBS[graphDrawn?graphNodePane(graphDrawn):graphShown];if(!name)return html`<h2 class="page-title">Graph</h2>`;const c=graphCounts||{},n={people:c.person,orgs:c.org,projects:c.project}[graphShown];
 const words={people:['{} person','{} people'],orgs:['{} organization','{} organizations'],projects:['{} open project','{} open projects']}[graphShown];
 const mode=graphShown==='projects'&&!graphDrawn&&graphBoards.length?html`<div class="view-mode" role="group" aria-label="View">${[['list','List'],['board','Board']].map(([v,t])=>html`<button type="button" data-proj-view="${v}" aria-pressed="${projView()===v}">${t}</button>`)}</div>`:'';
 const team=!graphDrawn&&['people','orgs','projects'].includes(graphShown)&&teamOn()?html`<div class="view-mode" role="group" aria-label="Whose">${[['mine','Mine'],['team','Team']].map(([v,t])=>html`<button type="button" data-graph-team="${v}" aria-pressed="${(v==='team')===graphTeam}">${t}</button>`)}</div>`:'';
 const made={people:['person','New person'],orgs:['org','New organization'],projects:['project','New project']}[graphShown];  /* a board has its own + New project */
 const add=made&&!graphDrawn&&!(graphShown==='projects'&&projView()==='board')?html`<button type="button" class="ghost head-new" data-graph-new="${made[0]}">+ ${t(made[1])}</button>`:'';
 return html`<div><p class="page-crumb">Graph</p><h2 class="page-title">${name}</h2>${n&&!graphDrawn&&words?html`<p class="page-sub">${t(words,n)}</p>`:''}</div>${team||mode||add?html`<div class="head-modes">${team}${mode}${add}</div>`:''}`}
// The browser tab's title follows the page: the card in a chat, the person or pane on the Graph, else the tab's name
function docTitle(tab=[...document.querySelectorAll('main>section')].find(x=>!x.hidden)?.id||'inbox'){
 const node=tab==='people'&&graphNode?document.querySelector('#people-view .graph-crumbs [aria-current]')?.textContent:'',card=tab==='inbox'&&chatId?(state?.suggestions||[]).find(s=>s.id===chatId)?.title:'';
 const title='The Machine · '+(card||node||t(tab==='inbox'?'To-dos':tab==='people'?GRAPH_SUBS[graphShown]||'Graph':PAGE_TITLES[tab]||'To-dos'));if(document.title!==title)document.title=title}
// The hello on a new owner's first views (Store.greeting): their first name, and who has waited longest on them, from
// their own Machine, linked to that to-do. Just the name while nothing is ready; gone after their first day or to-do.
function helloLine(g){const d=g?.line&&new Date(g.line.since);if(!d||isNaN(d))return '';const n=new Date(),p=g.line.person,
 days=Math.round((new Date(n.getFullYear(),n.getMonth(),n.getDate())-new Date(d.getFullYear(),d.getMonth(),d.getDate()))/864e5);
 return days<=0?t('{} has been waiting on your reply since earlier today.',p):days===1?t('{} has been waiting on your reply since yesterday.',p)
 :days<7?t('{} has been waiting on your reply since {}.',p,localeDate(d,DL,{weekday:'long'})):t('{} has been waiting on your reply for over a week.',p)}
function pageHead(){const h=$('#page-head'),tab=[...document.querySelectorAll('main>section')].find(x=>!x.hidden)?.id||'inbox';helpLink(tab);docTitle(tab);needsYouPlace();
 if(tab==='inbox'&&chatId){h.hidden=true;return}
 // A Graph page (person, org, project, promise) keeps the section's head; its breadcrumb under it leads back to the list
 const c=sideCounts,busy=[[c.foryou,['{} to-do for you','{} to-dos for you']],[c.preparing,'{} preparing']].filter(([k])=>k).map(([k,key])=>t(key,k)),known=!!state.suggestions&&!(shownCached&&!busy.length),sub=!known||!busy.length&&scopeFilter!=='all'?'':busy.join(' · ');  // with nothing open the sections below carry the counts
 const g=tab==='inbox'&&state.greeting,hi=g?.name?t('Hi {}',g.name):'',line=g?helloLine(g):'';
 const head=tab==='inbox'?html`<img class="page-avatar" src="brand/avatar.png" data-blink="brand/avatar-blink.png" alt="" width="40" height="40"><div><h2 class="page-title">${hi||$('#tagline').textContent}</h2>${line?html`<p class="page-hello"><a href="#card=${g.line.card}">${line}</a></p>`:''}${sub?html`<p class="page-sub">${sub}</p>`:''}</div>${checkHead()}`:tab==='people'?(()=>{try{return graphHead()}catch{return html`<h2 class="page-title">Graph</h2>`}})():tab==='calendar'&&lazyIn('calendar')?calHead():tab==='events'?html`<div><h2 class="page-title">${t('Messages')}</h2><p class="page-sub">${t('Everything I read, found by meaning or by words.')}</p></div>`:html`<h2 class="page-title">${PAGE_TITLES[tab]||''}</h2>`;
 h.classList.toggle('greet',tab==='inbox');h.classList.toggle('hello',!!(hi||line));h.classList.toggle('busy',tab==='inbox'&&busy.length>0);
 // A mascot mid-blink is the same head: comparing it as open keeps it (a rebuild would cut its blink short)
 if(h.innerHTML.replace(/<img class="page-avatar[^"]*" src="[^"]*"/,'<img class="page-avatar" src="brand/avatar.png"')!==head.s)setHTML(h,head);h.hidden=false}
{const o=new MutationObserver(()=>graphSubSync());document.querySelectorAll('main>section').forEach(x=>o.observe(x,{attributes:true,attributeFilter:['hidden']}));o.observe($('#tagline'),{childList:true,characterData:true,subtree:true})}
$('#suggestions').oninput=e=>{if(e.target.tagName==='TEXTAREA')e.target.classList.toggle('filled',!!e.target.value)};
// Mark done, Not needed and Snooze answer at once: the to-do leaves the list in this frame, its message (with Undo)
// shows, and the save goes behind it. A refusal puts the to-do back as it was, with the error. Undo tapped before the
// save landed waits for it, then undoes. Only while the Machine is reachable: a change that has to wait offline shows
// on the to-do instead (decideOrWait). said: the message at once, or, called with the answer, once it landed (Snooze
// says when it comes back, which a preset only knows then).
const atOnceSaving=new Map();
const atOnceOK=id=>!atOnceSaving.has(id)&&state.suggestions.some(s=>s.id===id&&!closed(s))&&!outbox.items.length&&navigator.onLine!==false&&!(netDown&&!csrfLive);
async function decideAtOnce(id,step,said){const s=state.suggestions.find(x=>x.id===id),before={status:s.status,closed_at:s.closed_at,snoozed_until:s.snoozed_until};let landed=false,end,saved;
 // The card goes and the toast shows in this frame; the lists redraw just after it is painted (a long list takes a moment)
 const cards=()=>document.querySelectorAll(`#suggestions article#task-${CSS.escape(id)}`),back=()=>{Object.assign(s,before);localEdits++;for(const n of cards())n.style.display='';focusKept(render)};
 sentWatch.delete(id);  // closed by hand: no "Sent. Moved to Done." over this toast
 atOnceSaving.set(id,new Promise(r=>end=r));
 Object.assign(s,step.choice==='snooze'?{status:'snoozed',snoozed_until:step.snoozed_until||s.snoozed_until||null}:{status:step.choice==='reject'?'rejected':'completed',closed_at:new Date().toISOString()});
 localEdits++;for(const n of cards())n.style.display='none';if(typeof said==='string')toast(said,false,id);
 const going=decideOrWait(id,[{...step,decision_id:crypto.randomUUID()}],step.choice);requestAnimationFrame(()=>setTimeout(()=>focusKept(render)));
 try{saved=await going;landed=!saved?.waiting;if(!landed){if(typeof said==='string')$('#toast').classList.remove('show');back();return saved}}
 catch(err){back();refresh().catch(()=>{});throw err}
 finally{atOnceSaving.delete(id);end(landed)}
 if(typeof said==='function')said(saved);
 await refresh();return saved}
// Do it on a to-do that waits for it (no note being typed for it): it shows as being prepared, with its toast, in the
// frame after the click (the to-dos only; the rest of the page follows once the Machine has it). Should the Machine not
// take it, it goes back as it was and the error shows.
async function acceptAtOnce(id,feedback){const s=state.suggestions.find(x=>x.id===id),before=s.status;
 s.status='accepted';localEdits++;focusKept(()=>render('view'));toast('I’ll prepare it.');
 let saved;try{saved=await decidePost(id,{choice:'accept',feedback,decision_id:crypto.randomUUID()})}
 catch(err){s.status=before;localEdits++;focusKept(render);refresh().catch(()=>{});throw err}
 if(/^(pe|ac|pr|in|sn)/.test(saved?.status))s.status=saved.status;localEdits++;focusKept(render);refresh().catch(()=>{});
 if(saved?.already)toast({done:'Already done. See the to-do.',closed:'Nothing is waiting to try again here.'}[saved.already]||'Already carrying on with it.')}
async function saveDecision(id,choice,feedback='',answer=false){
if(choice==='undo'&&atOnceSaving.has(id)&&!await atOnceSaving.get(id))return;  // the change it undoes never landed: nothing to undo
if(['complete','reject'].includes(choice)&&atOnceOK(id)){await decideAtOnce(id,{choice,feedback},choice==='complete'?'Marked done':'Marked not needed');return}
if(choice==='accept'&&!changing.has(id)&&atOnceOK(id)&&state.suggestions.find(s=>s.id===id).status==='pending'){await acceptAtOnce(id,feedback);return}
let saved;try{const args={choice,feedback,decision_id:crypto.randomUUID()};saved=OUTBOX_CHOICES.includes(choice)?await decideOrWait(id,[args],choice):await decidePost(id,args)}
catch(err){refresh().catch(()=>{});throw err}  // the card may be stale: redraw it
// Offline: it waits on the device, so the editor closes
if(saved?.waiting){changing.delete(id);dismissing.delete(id);focusKept(render);return}
// Its new status shows with the toast; the full status follows
changing.delete(id);const s=/^(pe|ac|pr|in|sn)/.test(saved?.status)&&state.suggestions.find(x=>x.id===id);if(s)s.status=saved.status;
localEdits++;focusKept(render);refresh().catch(()=>{});
// Try again on a to-do that already carried on: say so.
if(saved?.already){toast({done:'Already done. See the to-do.',closed:'Nothing is waiting to try again here.'}[saved.already]||'Already carrying on with it.');return}
// A Change stays on the card (its "You asked" note has See in chat ›); the chat never opens by itself.
if(['complete','reject'].includes(choice))toast(saved?.status==='completed'?'Marked done':'Marked not needed',false,id);else toast(answer?'Thanks. I’ll carry on.':({accept:'I’ll prepare it.',other:'Changes saved.',retry:'Trying again.',undo:'Reopened.',reopen:'Reopened.'})[choice]||'Saved.');
}
document.addEventListener('click',e=>{for(const m of document.querySelectorAll('.more-actions[open]'))if(!m.contains(e.target)||e.target.closest('.more-menu button:not([data-mm-open],[data-mm-back])'))m.open=false});
$('#suggestions').onclick=async e=>{const b=e.target.closest('button');if(!b||b.dataset.browserFocus)return;const id=b.dataset.id;
if(b.dataset.tipDone){tipDone(b.dataset.tipDone);render();return}
if(b.dataset.ldExpand){const k=b.dataset.ldExpand;lookExpanded.has(k)?lookExpanded.delete(k):lookExpanded.add(k);render();return}
if(b.dataset.ldNot){lookNotDone(b);return}
if(['change','reject'].includes(b.dataset.choice))tipDone('change');if(b.dataset.smart)tipDone('send');
if(b.dataset.unmerge){b.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'undo_merge',args:{suggestion_id:id,approval_id:crypto.randomUUID()}})});toast('Undoing the merge…');await refresh()}catch(e){errCaught(e);toast(e.message,true)}finally{b.disabled=false}return}
if(b.dataset.smart){const a=taskActions(state.suggestions.find(s=>s.id===id)).find(a=>a.revision===b.dataset.smart);if(!a){toast('That result changed. Use its current buttons.',true);return}if(['email','email_demo','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply','merge','finish','calendar','doc_write'].includes(a.kind)){openSend(id,b.dataset.smart);return}b.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'confirm_action',args:{suggestion_id:id,revision:b.dataset.smart,approval_id:crypto.randomUUID()}})});toast('I’ll prepare that next.');await refresh()}catch(e){errCaught(e);toast(e.message,true)}finally{b.disabled=false}return}
if(b.dataset.original){openEmail(id).catch(e=>toast(e.message,true));return}
if(b.dataset.heldRead){openEvent(b.dataset.heldRead,'');return}
// Redo for this message: Ask for changes, with the ask already written (they can add to it before it goes)
if(b.dataset.heldRedo!=null){changing.add(id);dismissing.delete(id);render();const f=$('#feedback-'+id);if(f&&!f.value.trim()){f.value=b.dataset.heldRedo?t('Redo the draft for the new message from {}.',b.dataset.heldRedo):t('Redo the draft for the new message.');f.classList.add('filled')}f?.focus();return}
if(b.dataset.result){try{if(b.dataset.result==='copy')await copyResult(id);else await openResult(id,b.dataset.file?{name:b.dataset.fileName||'',path:b.dataset.file}:undefined)}catch(e){errCaught(e);toast(e.message,true)}return}
// A Fleet item among the to-dos (Share, Not now: data-choice too) is not a to-do: its own handler (fleetOn) answers it
if(!b.dataset.choice||b.closest('.fleet-card'))return;const choice=b.dataset.choice;
if(choice==='send'){openSend(id);return}
if(choice==='pick'){const s=state.suggestions.find(x=>x.id===id),q=s?.preparation_questions?.[+b.dataset.q];if(!q)return;
 if(!changing.has(id)){changing.add(id);dismissing.delete(id);render()}
 // Only the answer goes in the box (the Machine keeps which question it answers): a pick for the same question replaces that question's earlier pick
 const t=$('#feedback-'+id);if(!t)return;const picked=askPicks.get(id)||{},lines=t.value.split('\n').filter(l=>l.trim()),was=lines.indexOf(picked[b.dataset.q]);
 if(was>=0)lines.splice(was,1,b.dataset.pick);else lines.push(b.dataset.pick);askPicks.set(id,{...picked,[b.dataset.q]:b.dataset.pick});
 t.value=lines.join('\n');t.classList.add('filled');
 for(const x of document.querySelectorAll(`#task-${CSS.escape(id)} .pick[data-q="${b.dataset.q}"]`))x.setAttribute('aria-pressed',String(x.dataset.pick===b.dataset.pick));t.focus();return}
if(choice==='change'||choice==='answer'){changing.add(id);dismissing.delete(id);render();$('#feedback-'+id)?.focus();return}
if(choice==='cancel-change'){changing.delete(id);render();return}
if(choice==='reject'){dismissing.add(id);changing.delete(id);render();return}
if(choice==='cancel-dismiss'){dismissing.delete(id);render();return}
if(choice==='dismiss-pick'){const on=b.getAttribute('aria-pressed')!=='true';for(const r of b.parentElement.children)r.setAttribute('aria-pressed','false');b.setAttribute('aria-pressed',String(on));return}
if(choice==='dismiss-typed'){const card=b.closest('.dismiss-editor'),why=[card?.querySelector('.reason[aria-pressed="true"]')?.dataset.reason,($('#dismiss-'+id)?.value||'').trim()].filter(Boolean).join(': ');
 b.disabled=true;const stop=lateShow(()=>{b.setAttribute('aria-busy','true');b.textContent='Saving…'});try{await saveDecision(id,'reject',why);dismissing.delete(id);focusKept(render)}catch(e){errCaught(e);toast(e.message,true)}finally{stop();b.disabled=false;b.removeAttribute('aria-busy');b.textContent='Confirm not needed'}return}
if(choice==='snooze'){openSnooze(id);return}
const feedback=$('#feedback-'+id)?.value||'';if(choice==='other'&&!feedback.trim()){$('#feedback-'+id)?.focus();toast(b.dataset.answer?'Type your answer first.':'Tell me what to change first.',true);return}
b.disabled=true;try{await saveDecision(id,choice,feedback,!!b.dataset.answer)}catch(e){errCaught(e);toast(e.message,true)}finally{b.disabled=false}};
