$('nav').addEventListener('click',e=>{const t=e.target.closest('button')?.dataset.tab;
 if(t==='calendar'){if(!calRouting&&(e.isTrusted||!/^#calendar\?/.test(location.hash))){calSetAll(calDay(0));calFrom=calDay(0);calTo=calDay(7);calMoreFailed={};calUp=false;calPush(true);scrollTo({top:0})}calendarView(true)}
 else if(t&&/^#calendar\?/.test(location.hash))history.replaceState(null,'',location.pathname+location.search)});
DESK.addEventListener?.('change',()=>{if(!$('#calendar').hidden){calPush(true);calShowNow()}});
addEventListener('hashchange',()=>{if(calReturn&&!/^#chat=/.test(location.hash)&&!chatId){calReturn=false;showTab('calendar')}});
// A title over the main area on a computer: the tagline on To-dos, else the tab's name
// The footer's Help: the help article for what's on screen (themachine.computer/help, the articles in docs/help/)
const HELP='https://themachine.computer/help/',HELP_FOR={account:'plans-and-billing',inbox:'cards',calendar:'calendar',events:'dashboard',people:'graph',fleet:'fleet',feedback:'dashboard',health:'connections',general:'settings',notify:'notifications',security:'security-levels',writing:'writing',skills:'skills',model:'model'};
function helpLink(tab){const a=$('#help-link'),slug=HELP_FOR[tab==='settings'?settingsNow:tab]||'';if(a&&a.href!==HELP+slug)a.href=HELP+slug}
const PAGE_TITLES={calendar:'Calendar',events:'Messages',people:'Graph',fleet:'Fleet',feedback:'Learning',health:'Connections',settings:'Settings'};
// The Graph's title is the pane on screen, with Graph as a quiet crumb and the same count as its row in the sidebar
// A page's section, as its breadcrumb says: an organization opened from a project is under Organizations
const graphNodePane=id=>id==='me'?'people':/^org:/.test(id)?'orgs':/^project:/.test(id)?'projects':'people';
function graphHead(){if(/^promise:/.test(graphDrawn||''))return html`<div><p class="page-crumb">Graph</p><h2 class="page-title">Promise</h2></div>`;const name=GRAPH_SUBS[graphDrawn?graphNodePane(graphDrawn):graphShown];if(!name)return html`<h2 class="page-title">Graph</h2>`;const c=graphCounts||{},n={people:c.person,orgs:c.org,projects:c.project,roles:rolesWaiting}[graphShown];
 const words={people:['{} person','{} people'],orgs:['{} organization','{} organizations'],projects:['{} open project','{} open projects'],roles:['{} role to confirm','{} roles to confirm']}[graphShown];
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
 :days<7?t('{} has been waiting on your reply since {}.',p,d.toLocaleDateString(DL,{weekday:'long'})):t('{} has been waiting on your reply for over a week.',p)}
function pageHead(){const h=$('#page-head'),tab=[...document.querySelectorAll('main>section')].find(x=>!x.hidden)?.id||'inbox';helpLink(tab);docTitle(tab);needsYouPlace();
 if(tab==='inbox'&&chatId){h.hidden=true;return}
 // A Graph page (person, org, project, promise) keeps the section's head; its breadcrumb under it leads back to the list
 const c=sideCounts,busy=[[c.ready,'{} ready for you'],[c.needs,'{} to decide'],[c.preparing,'{} preparing']].filter(([k])=>k).map(([k,key])=>t(key,k)),known=!!state.suggestions&&!(shownCached&&!busy.length),sub=!known||!busy.length&&scopeFilter!=='all'?'':(busy.length?busy:startsByItself()||firstLookInfo(state.review_live||{})?[]:[t('All clear'),c.later&&t('{} coming back later',c.later),c.promises&&t(['{} promise kept track of','{} promises kept track of'],c.promises)].filter(Boolean)).join(' · ');
 const g=tab==='inbox'&&state.greeting,hi=g?.name?t('Hi {}',g.name):'',line=g?helloLine(g):'';
 const head=tab==='inbox'?html`<img class="page-avatar" src="brand/avatar.png" data-blink="brand/avatar-blink.png" alt="" width="40" height="40"><div><h2 class="page-title">${hi||$('#tagline').textContent}</h2>${line?html`<p class="page-hello"><a href="#card=${g.line.card}">${line}</a></p>`:''}${sub?html`<p class="page-sub">${sub}</p>`:''}</div>${checkHead()}`:tab==='people'?(()=>{try{return graphHead()}catch{return html`<h2 class="page-title">Graph</h2>`}})():tab==='calendar'?calHead():tab==='events'?html`<div><h2 class="page-title">${t('Messages')}</h2><p class="page-sub">${t('Everything I read, found by meaning or by words.')}</p></div>`:html`<h2 class="page-title">${PAGE_TITLES[tab]||''}</h2>`;
 h.classList.toggle('greet',tab==='inbox');h.classList.toggle('hello',!!(hi||line));h.classList.toggle('busy',tab==='inbox'&&busy.length>0);
 // A mascot mid-blink is the same head: comparing it as open keeps it (a rebuild would cut its blink short)
 if(h.innerHTML.replace(/<img class="page-avatar[^"]*" src="[^"]*"/,'<img class="page-avatar" src="brand/avatar.png"')!==head.s)setHTML(h,head);h.hidden=false}
{const o=new MutationObserver(()=>graphSubSync());document.querySelectorAll('main>section').forEach(x=>o.observe(x,{attributes:true,attributeFilter:['hidden']}));o.observe($('#tagline'),{childList:true,characterData:true,subtree:true})}
$('#suggestions').oninput=e=>{if(e.target.tagName==='TEXTAREA')e.target.classList.toggle('filled',!!e.target.value)};
async function saveDecision(id,choice,feedback='',answer=false){
let saved;try{const args={choice,feedback,decision_id:crypto.randomUUID()};saved=OUTBOX_CHOICES.includes(choice)?await decideOrWait(id,[args],choice):await decidePost(id,args)}
catch(err){await refresh().catch(()=>{});throw err}  // the card was drawn before something changed it: show it as it is now
// Offline: it waits on the device and says so on the to-do; the typed note is on its way, so the editor closes
if(saved?.waiting){changing.delete(id);dismissing.delete(id);focusKept(render);return}
changing.delete(id);await refresh();
// Try again or Continue on a card drawn before it carried on by itself (its sign-in was seen): nothing new, say so.
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
 const t=$('#feedback-'+id);if(!t)return;const head=sentence(q.question)+' ';
 t.value=[...t.value.split('\n').filter(l=>l.trim()&&!l.startsWith(head)),head+b.dataset.pick].join('\n');t.classList.add('filled');
 for(const x of document.querySelectorAll(`#task-${CSS.escape(id)} .pick[data-q="${b.dataset.q}"]`))x.setAttribute('aria-pressed',String(x.dataset.pick===b.dataset.pick));t.focus();return}
if(choice==='change'||choice==='answer'){changing.add(id);dismissing.delete(id);render();$('#feedback-'+id)?.focus();return}
if(choice==='cancel-change'){changing.delete(id);render();return}
if(choice==='reject'){dismissing.add(id);changing.delete(id);render();return}
if(choice==='cancel-dismiss'){dismissing.delete(id);render();return}
if(choice==='dismiss-pick'){const on=b.getAttribute('aria-pressed')!=='true';for(const r of b.parentElement.children)r.setAttribute('aria-pressed','false');b.setAttribute('aria-pressed',String(on));return}
if(choice==='dismiss-typed'){const card=b.closest('.dismiss-editor'),why=[card?.querySelector('.reason[aria-pressed="true"]')?.dataset.reason,($('#dismiss-'+id)?.value||'').trim()].filter(Boolean).join(': ');
 b.disabled=true;b.setAttribute('aria-busy','true');b.textContent='Saving…';try{await saveDecision(id,'reject',why);dismissing.delete(id)}catch(e){errCaught(e);toast(e.message,true)}finally{b.disabled=false;b.removeAttribute('aria-busy');b.textContent='Confirm not needed'}return}
if(choice==='snooze'){openSnooze(id);return}
const feedback=$('#feedback-'+id)?.value||'';if(choice==='other'&&!feedback.trim()){$('#feedback-'+id)?.focus();toast(b.dataset.answer?'Type your answer first.':'Tell me what to change first.',true);return}
b.disabled=true;try{await saveDecision(id,choice,feedback,!!b.dataset.answer)}catch(e){errCaught(e);toast(e.message,true)}finally{b.disabled=false}};
