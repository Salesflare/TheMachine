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
document.addEventListener('click',e=>{const b=e.target.closest('[data-promise-due]');if(!b)return;const f=$('#people-view .promise-due-form');if(f){f.hidden=!f.hidden;if(!f.hidden)f.elements.due.focus()}});
document.addEventListener('submit',async e=>{const f=e.target.closest('.promise-due-form');if(!f)return;e.preventDefault();const b=f.querySelector('button');b.disabled=true;
 try{await graphPost('promise_due',{id:Number(f.dataset.promiseId),due:f.elements.due.value});f.hidden=true;toast('Date moved.');await people(graphNode,true)}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
function graphOpen(id){if(!graphNode&&!$('#people').hidden)graphScroll=scrollY;if(location.hash!==graphHash(id))history.pushState(null,'',graphHash(id));people(id)}
function graphBack(pane){if(pane){graphPane=pane;localStorage.setItem('graph-pane',pane)}if(/^#graph\//.test(location.hash))history.pushState(null,'',location.pathname+location.search+'#graph='+(graphPane||'people'));people('')}
document.addEventListener('click',e=>{if(e.target.closest('[data-graph-retry]'))people(graphNode)});
document.addEventListener('click',e=>{const item=e.target.closest('.person-menu [role=menuitem]');if(item)item.closest('details').open=false});
function showGraphPane(id){graphPane=id;localStorage.setItem('graph-pane',id);graphShown=id;graphHashSync();graphSubSync();const view=$('#people-view');if(!view.querySelector(`[data-graph-panel="${CSS.escape(id)}"]`)){if(!graphNode&&!$('#people-query').value.trim())return;$('#people-query').value='';people('');return}
 for(const b of view.querySelectorAll('[data-graph-pane]'))b.setAttribute('aria-selected',b.dataset.graphPane===id);for(const p of view.querySelectorAll('[data-graph-panel]'))p.hidden=p.dataset.graphPanel!==id;tabsShow(view.querySelector('.sub-tabs'));tabsShow(view.querySelector(`[data-graph-panel="${CSS.escape(id)}"] .sub-tabs`))}
// A record opens from what was fetched when the pointer rested on its link (80 ms) or the link got focus: kept 30 s, the
// last 8, each used once. A finger starts it on touching the link, never on a scroll; a node already on its way is not
// asked again. Any change sent to the Machine (request, not a GET) forgets them, so a page never opens older than
// what was just saved; a quiet refresh always asks the Machine.
const PEEK_MS=30000,PEEK_MAX=8;  // graphPeek: shell-network.js, which forgets it on a change
const peekFresh=node=>{const hit=graphPeek.get(node);return hit&&Date.now()-hit.at<PEEK_MS?hit:null};
function graphPeekTake(node){const hit=peekFresh(node);graphPeek.delete(node);if(hit)return hit.p;
 const p=request('api/graph?node='+encodeURIComponent(node));graphPeek.set(node,{at:Date.now(),p,taken:true});const off=()=>{if(graphPeek.get(node)?.p===p)graphPeek.delete(node)};p.then(off,off);return p}
function graphPeekStart(node,ctl){if(!node||/^promise:/.test(node)||node===graphNode&&!$('#people').hidden||peekFresh(node))return null;
 const p=request('api/graph?node='+encodeURIComponent(node),ctl?{signal:ctl.signal}:undefined),hit={at:Date.now(),p,ctl};graphPeek.set(node,hit);p.catch(()=>{if(graphPeek.get(node)?.p===p)graphPeek.delete(node)});
 while(graphPeek.size>PEEK_MAX)graphPeek.delete(graphPeek.keys().next().value);return hit}
{const PEEK_LINK='[data-node],a[href^="#graph/"]',peekNode=el=>{if(el.dataset.node)return el.dataset.node;try{return decodeURIComponent(el.getAttribute('href').slice(7))}catch{return ''}};let timer=0,on=null;
 document.addEventListener('pointerover',e=>{if(e.pointerType==='touch')return;const el=e.target.closest?.(PEEK_LINK);if(el===on)return;clearTimeout(timer);on=el;if(el)timer=setTimeout(()=>graphPeekStart(peekNode(el)),80)},{passive:true});
 document.addEventListener('pointerout',e=>{if(on&&!on.contains(e.relatedTarget)){clearTimeout(timer);on=null}},{passive:true});
 document.addEventListener('focusin',e=>{const el=e.target.closest?.(PEEK_LINK);if(el)graphPeekStart(peekNode(el))});
 // A finger: the fetch starts as it touches the link, so it is about 100 ms ahead of the click. A finger that moves
 // (more than 10 px) or that the browser takes for a scroll (pointercancel) was no tap: that fetch is called off,
 // unless the click already took it.
 let press=null;const off=()=>{if(!press)return;const {node,hit}=press;press=null;if(hit&&graphPeek.get(node)===hit){graphPeek.delete(node);hit.ctl.abort()}};
 document.addEventListener('pointerdown',e=>{if(e.pointerType!=='touch')return;off();const el=e.target.closest?.(PEEK_LINK);if(!el)return;const node=peekNode(el);
  press={node,x:e.clientX,y:e.clientY,hit:graphPeekStart(node,new AbortController())}},{passive:true});
 document.addEventListener('pointermove',e=>{if(press&&e.pointerType==='touch'&&Math.hypot(e.clientX-press.x,e.clientY-press.y)>10)off()},{passive:true});
 document.addEventListener('pointercancel',off,{passive:true});document.addEventListener('touchcancel',off,{passive:true});
 document.addEventListener('pointerup',e=>{if(e.pointerType==='touch')press=null},{passive:true})}
async function people(node=graphNode,quiet=false){graphLoadedAt=Date.now();if(!quiet)pairsForget();  /* answered pairs keep their place only while the owner taps through */const was=graphNode;graphNode=node;if(was!==node&&!$('#people').hidden)graphSubSync();  /* the head names the page's section; + New … is for the lists, not a page */const version=++graphRequest,view=$('#people-view'),oldHtml=view.innerHTML;let headShown=false;const draw=(body,mode='list')=>{if(version!==graphRequest||(quiet||headShown)&&([...view.querySelectorAll('form:not([hidden])')].some(f=>f.checkVisibility())||view.querySelector('.team-thread[open],.tile-menu[open],.tile.dragging,.tile:active,.lane.drop,.board-menu[open],.graph-sort[open],.tag-add input:focus')))return;  /* a refresh never closes what the owner is typing or reading */const back=(quiet||headShown)&&foldsKeep(view);setHTML(view,body);view.dataset.mode=mode;pagerMount(view);if(back)back();if(graphDrawn!==graphNode){graphDrawn=graphNode;if(!$('#people').hidden)pageHead()}};  /* the head changes with the page it names, not before it has loaded */  /* the rows a list already loaded come with it, so the page keeps its height and the reader keeps their place (placeKeep) */
 function nodeDraw(n){const head=n.head_only,again=!head&&headShown;  /* the whole page after its head: keeps the reader's place */
  if(n.owners)graphOwners=n.owners;if(n.timeline){const was=graphTl.page;if(quiet&&was?.id===n.id&&was.timeline?.source){n.recent=was.recent;n.timeline={...n.timeline,...was.timeline}}else n.timeline.shown=GRAPH_ROWS;graphTl.page=n}const group=k=>n.links.filter(l=>l.kind===k&&l.id!==n.org);
  if(n.team_only){draw(teamDetail(n));if(version!==graphRequest)return;$('#people').classList.add('graph-on-node');if(!quiet)scrollTo({top:0});return}
  if(n.kind==='me'){graphNode='me';draw(aboutYouPage(n),'node');if(version!==graphRequest)return;graphKept=null;docTitle();$('#people').classList.add('graph-on-node');if(location.hash!==graphHash('me')&&!$('#people').hidden)history.replaceState(null,'',graphHash('me'));if(!quiet)scrollTo({top:0});return}
  const sub=n.kind==='person'?personSub({...n,role:null,profile:null})+(n.quiet?' · '+t('gone quiet'):''):n.kind==='project'?(heatLabel(n.state)+' · '+t('last signal {}',day(n.last_at))+(n.probable_signals?' · '+t('{} probably part of it',n.probable_signals):'')):(t(['{} person','{} people'],n.signals)+' · '+t('last contact {}',day(n.last_at)));
  const [paneId,paneName]=GRAPH_KIND_PANE[n.kind]||GRAPH_KIND_PANE.person;
  draw(html`${html`<div class="graph-crumbs" role="navigation" aria-label="Breadcrumb"><a href="#graph" data-crumb="">Graph</a><span aria-hidden="true">›</span><a href="#graph=${paneId}" data-crumb="${paneId}">${paneName}</a><span aria-hidden="true">›</span><span aria-current="page">${n.name}</span></div>${n.kind==='person'?personPage(n,group,sub):n.kind==='org'?orgPage(n,group):html`<article class="graph-detail"><div class="name-row"><h3 title="${n.name}">${n.name}</h3>${n.project?projActions(n.project):html`<button class="ghost" data-name-edit>Rename</button>`}</div><form class="name-form inline-edit" data-node-id="${n.id}" hidden><input name="newname" maxlength="60" value="${n.name}" placeholder="Project name" aria-label="Name"><button>Save</button></form><p class="graph-sub detail-sub">${sub}</p>${stageBox(n)}${projFacts(n)}${crmFieldsSection(n)}${detailGroups(n,group)}</article>`}`}${privateRow(n)}${teamBlock(n)}${projectTodos(n)}${openBetween(n)}${knownAbout(n)}${recentLog(n)}${graphEvents(n)}`);
  if(version!==graphRequest)return;if(head)headShown=true;
  view.dataset.mode='node';graphKept=null;docTitle();$('#people').classList.add('graph-on-node');if(location.hash!==graphHash(n.id)&&!$('#people').hidden)history.replaceState(null,'',graphHash(n.id));
  for(const p of view.querySelectorAll('.ge-preview'))p.classList.toggle('fade',p.scrollHeight>p.clientHeight+1);
  if(n.kind==='person'){contactMarks(view,n);friendMarks(view,n)}
  if(editRole===node&&!head){editRole=false;const pf=view.querySelector('#org-form');if(pf?.elements.role){orgOpen(pf,true);pf.elements.role.focus({preventScroll:true});pf.elements.role.select();pf.elements.role.scrollIntoView({block:'center'})}}
  if(!quiet&&!again)scrollTo({top:0})}
 try{
 if(node&&/^promise:\d+$/.test(node)){const body=await promisePage(node.slice(8));draw(body,'node');if(version!==graphRequest)return;graphKept=null;$('#people').classList.add('graph-on-node');pageHead();if(!quiet)scrollTo({top:0});return}
 if(node){let n,whole=false;const peeked=!quiet&&!!peekFresh(node),page=(quiet?request('api/graph?node='+encodeURIComponent(node)):graphPeekTake(node)).finally(()=>{whole=true});  /* a record's head first (part=head, no timeline), the whole page when it comes */if(!quiet&&!peeked&&!node.startsWith('team:'))request('api/graph?node='+encodeURIComponent(node)+'&part=head').then(h=>{if(!whole&&version===graphRequest&&h.head_only&&h.kind!=='me'&&!h.team_only)nodeDraw(h)}).catch(()=>{});try{n=await page}catch(e){errCaught(e);if(version!==graphRequest||quiet&&oldHtml)return;  /* a page that didn't load says so, with Try again; a quiet refresh keeps what is shown */
   draw(html`<div class="empty graph-load-failed" role="alert"><div><strong>Couldn’t load this page.</strong></div><button type="button" data-graph-retry>Try again</button></div>`,'node');$('#people').classList.add('graph-on-node');return}
  nodeDraw(n);return}
 $('#people').classList.remove('graph-on-node');
 const q=$('#people-query').value.trim();
 if(!q&&graphUnstash(view))return;if(!q&&view.dataset.mode==='search')lateShow(()=>{if(version===graphRequest&&view.dataset.mode==='search')draw(html`<p class="pager-loading" role="status">Loading…</p>`)});
 if(q){const key='gsearch:'+q,p=pager(key,cursor=>request('api/graph?q='+encodeURIComponent(q)+'&cursor='+encodeURIComponent(cursor)).then(r=>({items:r.found,next:r.next})),graphItem);
  graphStash(view);if(!p.items.length&&p.next!=null){const stop=view.dataset.mode!=='search'||!view.querySelector('.graph-found')?lateShow(()=>{if(version===graphRequest)draw(html`<p class="pager-loading" role="status">Searching…</p>`,'search')}):null;await pagerMore(key);stop?.()}
  if(version!==graphRequest||$('#people-query').value.trim()!==q)return;  /* a late answer to an older search changes nothing */
  if(p.failed&&!p.items.length)throw new Error('Couldn’t search. Try again.');
  draw(p.items.length?html`<div class="graph-found"><div class="section-head"><h2>Found</h2></div>${pagerSlot(key,'','graph-list')}</div>`:html`<div class="empty all-clear graph-found"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>Nobody by that name.</strong>Try part of a name, an address or a company.</div></div>`,'search');pagerMount(view);return}
 const forTeam=graphTeam;let g=await cachedGet(graphTeam||graphPane==='held'?'api/graph?view=team':'api/graph',graphFresh);graphSharing=g.sharing||graphSharing;graphTeammates=g.teammates||graphTeammates;if(g.team&&!teamOn())g=await request('api/graph');
 if(forTeam!==graphTeam)return;  // Mine or Team changed while this loaded: the newer load draws
 if(!g.team)graphContactsIn=g.contacts_in||[];
 const team=!!g.team&&(graphTeam||graphPane==='held'),whos=rolesLeft(g.whos_who),waiting=Math.max(0,(g.waiting??g.whos_who?.length??0)-((g.whos_who?.length||0)-whos.length));whosLast={items:g.whos_who,waiting:g.waiting};$('#badge-people').textContent=waiting||'';const start=team?shareNote(g.sharing):'';
 if(!team){graphOwners=g.owners||[];graphLastImport=g.last_import||null;graphFields=g.crm_fields||[];graphTags=g.tags||[];if(g.currency)graphCurrency=g.currency;tagsPaint()}
 const back=graphScroll;  /* back from a person: a quiet refresh that wins the race restores it too */const lc=!team&&g.list_counts||Object.fromEntries(['people','quiet','new','orgs','warmup','projects','projects_done'].map(k=>[k,(g[k]||[]).length]));graphLocal=!team&&g.list_counts?null:g;  /* the team's lists come whole */
 const had=quiet&&new Map([...pagers].filter(([k,p])=>k.startsWith('graph:')&&p.items.length).map(([k,p])=>[k,p.items.length]));
 if(team||graphListsTeam||JSON.stringify(lc)!==JSON.stringify(graphLists)||!g.list_counts){pagerDrop('graph');graphLists=lc}graphListsTeam=team;
 const panes=team?[{id:'people',label:'People',html:html`${start}${graphTabs('people')||html`<div class="empty all-clear"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>Nothing from the team yet.</strong></div></div>`}`},
  {id:'projects',label:'Projects',html:projectsPane(g)},
  {id:'orgs',label:'Organizations',html:graphTabs('orgs')||graphEmpty('orgs',true)},
  {id:'roles',label:'Who’s who',badge:waiting,html:whosWho(whos,waiting)},
  ...(g.held?.length||graphPane==='held'?[{id:'held',label:'Held back',html:heldPane(g.held)}]:[])].filter(p=>p.html)
 :[{id:'people',label:'People',html:html`${sameList(g.same_person)}${graphTabs('people')||graphEmpty('people',false,g.read)}${hiddenSenders(g.hidden_senders)}`},
  {id:'projects',label:'Projects',html:projectsPane(g)},
  {id:'orgs',label:'Organizations',html:html`${orgDoubles(g.org_doubles)}${graphTabs('orgs')||graphEmpty('orgs')}`},
  {id:'roles',label:'Who’s who',badge:waiting,html:whosWho(whos,waiting)}].filter(p=>p.html);
 const current=(panes.find(p=>p.id===graphPane)||panes.find(p=>p.id==='people')||panes[0])?.id;graphCountsSet(g.counts);if(version===graphRequest){graphShown=current||'';graphHashSync();graphSubSync()}
 // A refresh that starts the lists over loads as many rows as were there before it draws, so the page keeps its height
 if(had)for(const [k,n] of had){const p=pagers.get(k);if(!p||p.items.length||p.busy)continue;for(let i=0;i<10&&p.items.length<n&&p.next!=null&&!p.failed;i++){p.pending=pagerLoad(k,p,false);await p.pending}}
 if(version!==graphRequest)return;
 rolesRow(panes.some(p=>p.id==='roles'),waiting);draw((panes.length?html`${panes.map(p=>html`<div class="sub-pane" role="tabpanel" data-graph-panel="${p.id}"${p.id===current?'':html` hidden`}>${p.html}</div>`)}`:'')
  ||html`<div class="empty all-clear"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>Nothing mapped yet.</strong>People appear as messages and meetings come in.</div></div>`);
 if(version===graphRequest&&!team&&graphBoards.length&&!graphBoards.some(b=>'follow_ups'in b))fuLoad(version);
 if(version===graphRequest){graphAt=Date.now();pagerMount(view);if(back!=null&&version===graphRequest){graphScroll=null;scrollTo(0,back)}}if(!quiet)notice('')}catch(e){errCaught(e);if(version===graphRequest&&(!quiet||!oldHtml))notice(e.message,true)}}
