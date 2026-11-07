// A promise's own page (#promise/<id>), laid out like a person's: who promised what to whom and by when, where it
// stands, the message it came from, who and what it is about, its card as a link, and what happened since.
const promiseHref=p=>'#promise/'+encodeURIComponent(p.id);
const promiseFirst=who=>String(who||'').split(/\s+/)[0]||who;
const PROMISE_SAID={'gmail.message':'an email','slack.message':'Slack','teams.message':'Teams','whatsapp.message':'WhatsApp','telegram.message':'Telegram','linkedin.message':'LinkedIn','x.message':'X','intercom.message':'Intercom','calendar.event':'a meeting'};
function promiseState(p){const late=p.due&&p.due<localDay(new Date());
 return p.state==='open'?(p.direction==='theirs'&&!p.together?['Waiting on '+promiseFirst(p.who),'var(--lavender)']:[late?'Past its date':'Open',late?'var(--orange)':'var(--mint)']):p.state==='card'?['Now a to-do','var(--amber)']
  :p.state==='kept'?['Kept','var(--muted)']:p.state==='answered'?['They wrote again','var(--muted)']:['Not needed','var(--muted)']}
function promiseLine(p,h){const via=PROMISE_SAID[h.detail]||'a message';
 return {said:p.together?t('Planned together in {}',via):p.direction==='mine'?t('Promised to {} in {}',p.who,via):t('{} promised it in {}',p.who,via),noted:'Noted by a check',due:t('Date moved to {}',day(h.detail)),
  kept:'Marked done',dropped:'Dropped',answered:'They wrote again',carded:'Became a to-do',together:'Both sides said it: one plan',merged:'The same as another promise',seen:'The Machine saw it done'}[h.kind]||''}
async function promisePage(id){const p=await request('api/promise?id='+encodeURIComponent(id)),[state,color]=promiseState(p),person=(p.links||[]).find(l=>l.kind==='person');
 const who=p.together?'With '+p.who:p.direction==='mine'?'Promised to '+p.who:p.who+' promised',when=p.due?'due '+day(p.due):'no date';
 const actions=p.state==='card'?html`<div class="promise-actions"><button class="ghost" data-promise="${p.id}" data-close="kept">Mark done</button><button class="ghost" data-promise="${p.id}" data-close="dropped">Drop</button></div>`:p.state==='open'?html`<div class="promise-actions"><button class="ghost" data-promise="${p.id}" data-close="kept">Mark done</button><button class="ghost" data-promise-due>Change date</button><button class="ghost" data-promise="${p.id}" data-close="dropped">Drop</button></div><form class="promise-due-form" data-promise-id="${p.id}" hidden><input type="date" name="due" value="${p.due||''}" aria-label="New date" required><button>Save</button></form>`:'';
 const note=p.state!=='open'&&p.note&&!/\(you\)$/.test(p.note)?html`<p class="graph-sub muted">${p.note}</p>`:'';
 const src=p.source?.[0],from=src?htmlEdit(graphEvents({recent:p.source,name:p.who,kind:'promise'},'Came from'),c=>[...c.querySelectorAll('span.count')].find(n=>n.attributes.length===1&&/^\d+$/.test(n.textContent))?.remove()):'';
 const open=src&&/^https:\/\//.test(src.source_url||'')?html`<p class="graph-sub"><a href="${safeHref(src.source_url)}" target="_blank" rel="noreferrer">Open in ${SOURCE_NAME[graphSource(src.kind)]||'its app'} ↗</a></p>`:'';
 const kinds=[['person','People'],['org','Organization'],['project','Project']].map(([k,t])=>[t,(p.links||[]).filter(l=>l.kind===k)]).filter(([,l])=>l.length);
 const about=kinds.length?html`<div class="section-head"><h2>About</h2></div><div class="promise-about">${kinds.map(([t,l])=>html`<p class="graph-sub"><span class="muted">${t}</span> ${l.map(nodeButton)}</p>`)}</div>`:'';
 const card=p.card?html`<div class="section-head"><h2>To-do</h2></div><p class="graph-sub promise-card"><a href="#card=${p.card.id}">${p.card.title}</a></p>`:'';
 const hist=p.history.map(h=>[promiseLine(p,h),h.at]).filter(([t])=>t);
 return html`<div class="graph-crumbs" role="navigation" aria-label="Breadcrumb">${person?html`<a href="${graphHash(person.id)}" data-node="${person.id}">${person.name}</a>`:html`<a href="#graph" data-crumb="">Graph</a>`}<span aria-hidden="true">›</span><span aria-current="page">Promise</span></div><article class="graph-detail person-page promise-page"><div class="name-row"><div class="person-head"><h3>${cap(p.what)}</h3><p class="person-job">${who} · ${when}</p></div></div><p class="graph-sub promise-state"><span class="chip" style="--c:${color}">${state}</span></p>${note}${actions}${from}${open}${about}${card}${hist.length?html`<div class="section-head"><h2>History</h2></div><ul class="promise-history">${hist.map(([t,at])=>html`<li><span>${t}</span><time datetime="${at}">${day(at)}</time></li>`)}</ul>`:''}</article>`}
// Promise links, and card links on Graph pages, stay in the page, also when the page's base is another path.
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#promise/"],#people-view a[href^="#card="]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey||e.defaultPrevented)return;e.preventDefault();const href=a.getAttribute('href');if(location.hash===href)graphRoute();else location.hash=href});
document.addEventListener('click',e=>{const b=e.target.closest('[data-promise-due]');if(!b)return;const f=$('#people-view .promise-due-form');if(f){f.hidden=!f.hidden;if(!f.hidden)f.elements.due.focus()}});
document.addEventListener('submit',async e=>{const f=e.target.closest('.promise-due-form');if(!f)return;e.preventDefault();const b=f.querySelector('button');b.disabled=true;
 try{await graphPost('promise_due',{id:Number(f.dataset.promiseId),due:f.elements.due.value});f.hidden=true;toast('Date moved.');await people(graphNode,true)}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
// Graph links: #graph/<node id> opens a person, project or organization; the browser's back goes to where you were.
const GRAPH_KIND_PANE={person:['people','People'],project:['projects','Projects'],org:['orgs','Organizations']};
const graphHash=id=>'#graph/'+encodeURIComponent(id);
function graphOpen(id){if(!graphNode&&!$('#people').hidden)graphScroll=scrollY;if(location.hash!==graphHash(id))history.pushState(null,'',graphHash(id));people(id)}
function graphBack(pane){if(pane){graphPane=pane;localStorage.setItem('graph-pane',pane)}if(/^#graph\//.test(location.hash))history.pushState(null,'',location.pathname+location.search+'#graph='+(graphPane||'people'));people('')}
function graphRoute(){const pm=/^#promise\/(\d+)$/.exec(location.hash),m=/^#graph\/(.+)$/.exec(location.hash);let id=pm?'promise:'+pm[1]:'';try{id=id||(m?decodeURIComponent(m[1]):'')}catch{}
 if(id){if($('#people').hidden){graphNode=id;document.querySelector('nav [data-tab="people"]')?.click()}else if(graphNode!==id)people(id);return}
 if(!$('#people').hidden&&graphNode)people('')}
// Back or Forward onto an entry the app pushed (Settings, a card's chat) fires popstate but no hashchange, so a tab link
// like #graph=people is opened here too, not only at the next refresh.
// A hash link fires popstate and then hashchange, which opens it; so wait a tick and open it only when none came.
let hashSeen=0;addEventListener('hashchange',()=>{hashSeen++},true);
addEventListener('popstate',()=>{if(drawerStep)return;graphRoute();const seen=hashSeen;setTimeout(()=>{if(hashSeen===seen)openTabLink()})});addEventListener('hashchange',graphRoute);setTimeout(graphRoute);
document.addEventListener('click',e=>{for(const m of document.querySelectorAll('.fact-menu[open]'))if(!m.contains(e.target))m.open=false});
document.addEventListener('click',e=>{if(e.target.closest('[data-graph-retry]'))people(graphNode)});
document.addEventListener('click',e=>{const item=e.target.closest('.person-menu [role=menuitem]');if(item)item.closest('details').open=false});
$('nav').addEventListener('click',e=>{const t=e.target.closest('button');if(t?.dataset.tab&&t.dataset.tab!=='people'&&/^#graph[/=]/.test(location.hash))history.replaceState(null,'',location.pathname+location.search);graphSubSync()});
let graphSkip=false,graphAt=0,graphScroll=null,graphShown='',graphNode='',graphDrawn='',graphRequest=0,editRole=false,graphPane=localStorage.getItem('graph-pane')||'';
// Sub-tabs, as in Fleet: a pill row over panes that are all drawn at once and shown one at a time. A badge only
// counts what needs the owner (a source with a problem, roles to confirm, friend requests), never a total.
const subTabs=(label,attr,panes,current)=>html`<div class="sub-tabs" role="tablist" aria-label="${label}">${panes.map(p=>html`<button type="button" role="tab" ${attr}="${p.id}" aria-selected="${p.id===current}"><span class="ell">${p.label}</span>${p.badge?html` <span class="badge${p.warn?html` warn`:''}">${p.badge}</span>`:''}</button>`)}</div>`;
function tabsFade(row){const max=row.scrollWidth-row.clientWidth;row.classList.toggle('more-left',row.scrollLeft>2);row.classList.toggle('more-right',row.scrollLeft<max-2)}
function tabsShow(row){if(!row)return;const t=row.querySelector('[aria-selected="true"]');if(t&&row.scrollWidth>row.clientWidth)row.scrollLeft=Math.max(0,t.offsetLeft-row.offsetLeft-(row.clientWidth-t.offsetWidth)/2);tabsFade(row)}
const allTabsFade=()=>document.querySelectorAll('.fleet-tabs,.sub-tabs').forEach(tabsFade);
document.addEventListener('scroll',e=>{if(e.target.matches?.('.fleet-tabs,.sub-tabs'))tabsFade(e.target)},{capture:true,passive:true});addEventListener('resize',allTabsFade);
new MutationObserver(()=>document.querySelectorAll('.fleet-tabs:not([data-faded]),.sub-tabs:not([data-faded])').forEach(r=>{r.dataset.faded='';tabsShow(r)})).observe(document.querySelector('main'),{childList:true,subtree:true});
// Graph: People (closest, gone quiet, new), Who's who (roles to confirm), Projects and Organizations.
const GRAPH_PANES=['people','roles','projects','orgs'];
function showGraphPane(id){graphPane=id;localStorage.setItem('graph-pane',id);graphShown=id;graphHashSync();graphSubSync();const view=$('#people-view');if(!view.querySelector(`[data-graph-panel="${CSS.escape(id)}"]`)){if(!graphNode&&!$('#people-query').value.trim())return;$('#people-query').value='';people('');return}
 for(const b of view.querySelectorAll('[data-graph-pane]'))b.setAttribute('aria-selected',b.dataset.graphPane===id);for(const p of view.querySelectorAll('[data-graph-panel]'))p.hidden=p.dataset.graphPanel!==id;tabsShow(view.querySelector('.sub-tabs'));tabsShow(view.querySelector(`[data-graph-panel="${CSS.escape(id)}"] .sub-tabs`))}
// A record opens from what was fetched when the pointer rested on its link (80 ms) or the link got focus: kept 30 s, the
// last 8, each used once. Never on touch (a finger scrolling over a list is no hover), and a node already on its way is
// not asked again. Any change sent to the Machine (request, not a GET) forgets them, so a page never opens older than
// what was just saved; a quiet refresh always asks the Machine.
const PEEK_MS=30000,PEEK_MAX=8;  // graphPeek: shell-network.js, which forgets it on a change
const peekFresh=node=>{const hit=graphPeek.get(node);return hit&&Date.now()-hit.at<PEEK_MS?hit:null};
function graphPeekTake(node){const hit=peekFresh(node);graphPeek.delete(node);if(hit)return hit.p;
 const p=request('api/graph?node='+encodeURIComponent(node));graphPeek.set(node,{at:Date.now(),p,taken:true});const off=()=>{if(graphPeek.get(node)?.p===p)graphPeek.delete(node)};p.then(off,off);return p}
function graphPeekStart(node){if(!node||/^promise:/.test(node)||node===graphNode&&!$('#people').hidden||peekFresh(node))return;
 const p=request('api/graph?node='+encodeURIComponent(node));graphPeek.set(node,{at:Date.now(),p});p.catch(()=>{if(graphPeek.get(node)?.p===p)graphPeek.delete(node)});
 while(graphPeek.size>PEEK_MAX)graphPeek.delete(graphPeek.keys().next().value)}
{const PEEK_LINK='[data-node],a[href^="#graph/"]',peekNode=el=>{if(el.dataset.node)return el.dataset.node;try{return decodeURIComponent(el.getAttribute('href').slice(7))}catch{return ''}};let timer=0,on=null;
 document.addEventListener('pointerover',e=>{if(e.pointerType==='touch')return;const el=e.target.closest?.(PEEK_LINK);if(el===on)return;clearTimeout(timer);on=el;if(el)timer=setTimeout(()=>graphPeekStart(peekNode(el)),80)},{passive:true});
 document.addEventListener('pointerout',e=>{if(on&&!on.contains(e.relatedTarget)){clearTimeout(timer);on=null}},{passive:true});
 document.addEventListener('focusin',e=>{const el=e.target.closest?.(PEEK_LINK);if(el)graphPeekStart(peekNode(el))})}
async function people(node=graphNode,quiet=false){const was=graphNode;graphNode=node;if(was!==node&&!$('#people').hidden)graphSubSync();  /* the head names the page's section; + New … is for the lists, not a page */const version=++graphRequest,view=$('#people-view'),oldHtml=view.innerHTML;const draw=(body,mode='list')=>{if(version!==graphRequest||quiet&&([...view.querySelectorAll('form:not([hidden])')].some(f=>f.checkVisibility())||view.querySelector('.team-thread[open],.tile-menu[open],.tile.dragging,.tile:active,.lane.drop,.board-menu[open],.graph-sort[open],.tag-add input:focus')))return;  /* a refresh never closes what the owner is typing or reading */const back=quiet&&foldsKeep(view);setHTML(view,body);view.dataset.mode=mode;pagerMount(view);if(back)back();if(graphDrawn!==graphNode){graphDrawn=graphNode;if(!$('#people').hidden)pageHead()}};  /* the head changes with the page it names, not before it has loaded */  /* the rows a list already loaded come with it, so the page keeps its height and the reader keeps their place (placeKeep) */try{
 if(node&&/^promise:\d+$/.test(node)){const body=await promisePage(node.slice(8));draw(body,'node');if(version!==graphRequest)return;graphKept=null;$('#people').classList.add('graph-on-node');pageHead();if(!quiet)scrollTo({top:0});return}
 if(node){let n;try{n=await(quiet?request('api/graph?node='+encodeURIComponent(node)):graphPeekTake(node))}catch(e){errCaught(e);if(version!==graphRequest||quiet&&oldHtml)return;  /* a page that didn't load says so, with Try again; a quiet refresh keeps what is shown */
   draw(html`<div class="empty graph-load-failed" role="alert"><div><strong>Couldn’t load this page.</strong></div><button type="button" data-graph-retry>Try again</button></div>`,'node');$('#people').classList.add('graph-on-node');return}
  if(n.owners)graphOwners=n.owners;if(n.timeline){const was=graphTl.page;if(quiet&&was?.id===n.id&&was.timeline?.source){n.recent=was.recent;n.timeline={...n.timeline,...was.timeline}}else n.timeline.shown=GRAPH_ROWS;graphTl.page=n}const group=k=>n.links.filter(l=>l.kind===k&&l.id!==n.org);
  if(n.team_only){draw(teamDetail(n));if(version!==graphRequest)return;$('#people').classList.add('graph-on-node');if(!quiet)scrollTo({top:0});return}
  if(n.kind==='me'){graphNode='me';draw(aboutYouPage(n),'node');if(version!==graphRequest)return;graphKept=null;docTitle();$('#people').classList.add('graph-on-node');if(location.hash!==graphHash('me')&&!$('#people').hidden)history.replaceState(null,'',graphHash('me'));if(!quiet)scrollTo({top:0});return}
  const sub=n.kind==='person'?personSub({...n,role:null,profile:null})+(n.quiet?' · '+t('gone quiet'):''):n.kind==='project'?(heatLabel(n.state)+' · '+t('last signal {}',day(n.last_at))+(n.probable_signals?' · '+t('{} probably part of it',n.probable_signals):'')):(t(['{} person','{} people'],n.signals)+' · '+t('last contact {}',day(n.last_at)));
  const [paneId,paneName]=GRAPH_KIND_PANE[n.kind]||GRAPH_KIND_PANE.person;
  draw(html`${html`<div class="graph-crumbs" role="navigation" aria-label="Breadcrumb"><a href="#graph" data-crumb="">Graph</a><span aria-hidden="true">›</span><a href="#graph=${paneId}" data-crumb="${paneId}">${paneName}</a><span aria-hidden="true">›</span><span aria-current="page">${n.name}</span></div>${n.kind==='person'?personPage(n,group,sub):n.kind==='org'?orgPage(n,group):html`<article class="graph-detail"><div class="name-row"><h3 title="${n.name}">${n.name}</h3>${n.project?projActions(n.project):html`<button class="ghost" data-name-edit>Rename</button>`}</div><form class="name-form inline-edit" data-node-id="${n.id}" hidden><input name="newname" maxlength="60" value="${n.name}" placeholder="Project name" aria-label="Name"><button>Save</button></form><p class="graph-sub detail-sub">${sub}</p>${stageBox(n)}${projFacts(n)}${crmFieldsSection(n)}${detailGroups(n,group)}</article>`}`}${privateRow(n)}${teamBlock(n)}${projectTodos(n)}${openBetween(n)}${knownAbout(n)}${graphEvents(n)}`);
  if(version!==graphRequest)return;
  view.dataset.mode='node';graphKept=null;docTitle();$('#people').classList.add('graph-on-node');if(location.hash!==graphHash(n.id)&&!$('#people').hidden)history.replaceState(null,'',graphHash(n.id));
  for(const p of view.querySelectorAll('.ge-preview'))p.classList.toggle('fade',p.scrollHeight>p.clientHeight+1);
  if(n.kind==='person'){contactMarks(view,n);friendMarks(view,n)}
  if(editRole===node){editRole=false;const pf=view.querySelector('#org-form');if(pf?.elements.role){orgOpen(pf,true);pf.elements.role.focus({preventScroll:true});pf.elements.role.select();pf.elements.role.scrollIntoView({block:'center'})}}
  if(!quiet)scrollTo({top:0});return}
 $('#people').classList.remove('graph-on-node');
 const q=$('#people-query').value.trim();
 if(!q&&graphUnstash(view))return;if(!q&&view.dataset.mode==='search')draw(html`<p class="pager-loading" role="status">Loading…</p>`);
 if(q){const key='gsearch:'+q,p=pager(key,cursor=>request('api/graph?q='+encodeURIComponent(q)+'&cursor='+encodeURIComponent(cursor)).then(r=>({items:r.found,next:r.next})),graphItem);
  graphStash(view);if(!p.items.length&&p.next!=null){if(view.dataset.mode!=='search'||!view.querySelector('.graph-found'))draw(html`<p class="pager-loading" role="status">Searching…</p>`,'search');await pagerMore(key)}
  if(version!==graphRequest||$('#people-query').value.trim()!==q)return;  /* a late answer to an older search changes nothing */
  if(p.failed&&!p.items.length)throw new Error('Couldn’t search. Try again.');
  draw(p.items.length?html`<div class="graph-found"><div class="section-head"><h2>Found</h2></div>${pagerSlot(key,'','graph-list')}</div>`:html`<div class="empty all-clear graph-found"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>Nobody by that name.</strong>Try part of a name, an address or a company.</div></div>`,'search');pagerMount(view);return}
 const forTeam=graphTeam;let g=await cachedGet(graphTeam||graphPane==='held'?'api/graph?view=team':'api/graph',graphFresh);graphSharing=g.sharing||graphSharing;graphTeammates=g.teammates||graphTeammates;if(g.team&&!teamOn())g=await request('api/graph');
 if(forTeam!==graphTeam)return;  // Mine or Team changed while this loaded: the newer load draws
 if(!g.team)graphContactsIn=g.contacts_in||[];
 const team=!!g.team&&(graphTeam||graphPane==='held'),waiting=g.waiting??g.whos_who?.length??0;$('#badge-people').textContent=waiting||'';const start=team?shareNote(g.sharing):'';
 if(!team){graphOwners=g.owners||[];graphLastImport=g.last_import||null;graphFields=g.crm_fields||[];graphTags=g.tags||[];if(g.currency)graphCurrency=g.currency;tagsPaint()}
 const back=graphScroll;  /* back from a person: a quiet refresh that wins the race restores it too */const lc=!team&&g.list_counts||Object.fromEntries(['people','quiet','new','orgs','warmup','projects','projects_done'].map(k=>[k,(g[k]||[]).length]));graphLocal=!team&&g.list_counts?null:g;  /* the team's lists come whole */
 const had=quiet&&new Map([...pagers].filter(([k,p])=>k.startsWith('graph:')&&p.items.length).map(([k,p])=>[k,p.items.length]));
 if(team||graphListsTeam||JSON.stringify(lc)!==JSON.stringify(graphLists)||!g.list_counts){pagerDrop('graph');graphLists=lc}graphListsTeam=team;
 const panes=team?[{id:'people',label:'People',html:html`${start}${graphTabs('people')||html`<div class="empty all-clear"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>Nothing from the team yet.</strong></div></div>`}`},
  {id:'projects',label:'Projects',html:projectsPane(g)},
  {id:'orgs',label:'Organizations',html:graphTabs('orgs')||graphEmpty('orgs',true)},
  {id:'roles',label:'Who’s who',badge:waiting,html:whosWho(g.whos_who,waiting)},
  ...(g.held?.length||graphPane==='held'?[{id:'held',label:'Held back',html:heldPane(g.held)}]:[])].filter(p=>p.html)
 :[{id:'people',label:'People',html:html`${sameList(g.same_person)}${graphTabs('people')||graphEmpty('people',false,g.read)}`},
  {id:'projects',label:'Projects',html:projectsPane(g)},
  {id:'orgs',label:'Organizations',html:html`${orgDoubles(g.org_doubles)}${graphTabs('orgs')||graphEmpty('orgs')}`},
  {id:'roles',label:'Who’s who',badge:waiting,html:whosWho(g.whos_who,waiting)}].filter(p=>p.html);
 const current=(panes.find(p=>p.id===graphPane)||panes.find(p=>p.id==='people')||panes[0])?.id;graphCountsSet(g.counts);if(version===graphRequest){graphShown=current||'';graphHashSync();graphSubSync()}
 // A refresh that starts the lists over loads as many rows as were there before it draws, so the page keeps its height
 if(had)for(const [k,n] of had){const p=pagers.get(k);if(!p||p.items.length||p.busy)continue;for(let i=0;i<10&&p.items.length<n&&p.next!=null&&!p.failed;i++){p.pending=pagerLoad(k,p,false);await p.pending}}
 if(version!==graphRequest)return;
 rolesRow(panes.some(p=>p.id==='roles'),waiting);draw((panes.length?html`${panes.map(p=>html`<div class="sub-pane" role="tabpanel" data-graph-panel="${p.id}"${p.id===current?'':html` hidden`}>${p.html}</div>`)}`:'')
  ||html`<div class="empty all-clear"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>Nothing mapped yet.</strong>People appear as messages and meetings come in.</div></div>`);
 if(version===graphRequest){graphAt=Date.now();pagerMount(view);if(back!=null&&version===graphRequest){graphScroll=null;scrollTo(0,back)}}if(!quiet)notice('')}catch(e){errCaught(e);if(version===graphRequest&&(!quiet||!oldHtml))notice(e.message,true)}}
const graphPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
