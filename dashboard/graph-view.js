$('#people-view').addEventListener('click',async e=>{const b=e.target.closest('[data-fleet-ask]');if(!b)return;b.disabled=true;
 try{await fleetPost('fleet_ask',{kind:'relationships',question:{about:b.dataset.fleetAsk}});toast('Asked your Fleet. The answers show in the Fleet tab.')}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
// Graph and Fleet tab link to each other: a member's person in the Graph, a person's place in the Fleet tab.
$('#people-view').addEventListener('click',async e=>{const keep=e.target.closest('[data-fleet-keep]');
 if(keep){keep.disabled=true;try{await graphPost('graph_rename',{node_id:graphNode,name:keep.dataset.fleetKeep});toast('Kept. It stays if they leave.');await people(graphNode,true)}catch(err){errCaught(err);keep.disabled=false;toast(err.message,true)}return}
 const b=e.target.closest('[data-fleet-member],[data-fleet-free]');if(!b)return;document.querySelector('nav [data-tab="fleet"]')?.click();await fleetShown;
 const el=b.dataset.fleetMember?document.getElementById('fleet-m-'+b.dataset.fleetMember):document.querySelector(`.fleet-free-form[data-fleet="${CSS.escape(b.dataset.fleetFree)}"]`);if(!el)return;
 fleetReveal(el);el.scrollIntoView({block:'center',behavior:'smooth'});if(b.dataset.fleetFree)el.querySelector('input')?.focus({preventScroll:true});else{el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash')}});
$('#fleet-view').addEventListener('click',e=>{const b=e.target.closest('[data-graph-open]');if(!b)return;e.preventDefault();graphNode=b.dataset.graphOpen;document.querySelector('nav [data-tab="people"]')?.click()});
// A name or address cut off with an ellipsis shows in full on hover or long-press.
document.addEventListener('pointerover',e=>{const el=e.target.closest?.('.ct,.ell,.fleet-people strong,.fleet-people small');if(el&&!el.title&&el.scrollWidth>el.clientWidth)el.title=el.textContent.trim()});
// Graph tab: projects heating up or cooling, who's closest, who has gone quiet; tap one for its links and events.
const day=v=>v?new Date(String(v).length<=10?v+'T12:00':v).toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'}):t('never');
// An organization's logo from enrichment (https only, no referrer, lazy, fixed size); its initial shows until it loads and when it can't.
const LOGO_URL=/^https:\/\/[^\s"'<>\\]+$/;
const orgPic=(n,big)=>{const l=n.profile?.logo||'',u=LOGO_URL.test(l)||/^api\/person-photo\?p=[0-9a-f]{32}$/.test(l)?l:'',px=big?36:22;return `<span class="org-pic${big?' big':''}" aria-hidden="true">${esc((String(n.name||'').trim()[0]||'?').toUpperCase())}${u?`<img src="${esc(u)}" alt="" width="${px}" height="${px}" loading="lazy" decoding="async" referrerpolicy="no-referrer">`:''}</span>`};
// A person's photo from enrichment, the same way: https only, no referrer, lazy; their initials until it loads and when it can't.
const initials=name=>{const w=String(name||'').trim().split(/\s+/).filter(x=>/^\p{L}/u.test(x));return((w[0]?.[0]||'?')+(w.length>1?w.at(-1)[0]:'')).toUpperCase()};
const PHOTO_URL=/^api\/person-photo\?p=[0-9a-f]{32}$/;  // only photos saved on this Machine, never the service's own link
const personPic=(n,big)=>{const u=PHOTO_URL.test(n.profile?.photo||'')?n.profile.photo:'',px=big?44:26;return `<span class="person-pic${big?' big':''}" aria-hidden="true">${esc(initials(n.name))}${u?`<img src="${esc(u)}" alt="" width="${px}" height="${px}" loading="lazy" decoding="async" referrerpolicy="no-referrer">`:''}</span>`};
document.addEventListener('error',e=>{const t=e.target;if(t?.tagName==='IMG'&&t.parentElement?.matches('.org-pic,.person-pic'))t.remove()},true);
// The owner changes a person's or organization's picture from its page; a teammate's record shows theirs as it is.
const picEdit=(n,pic)=>n.team_only?pic:`<button type="button" class="pic-edit" data-pic-edit="${esc(n.id)}" title="Change picture" aria-label="Change picture">${pic}</button>`;
const nodeButton=n=>`<button class="node" data-node="${esc(n.id)}" title="${esc(n.name)}">${esc(n.name)}</button>`;
const PROJECT_COLOR={'heating up':'var(--amber)','active':'var(--mint)','cooling':'var(--lavender)','dormant':'var(--faint)'};
// A project's activity against two weeks ago (graph.project_state), in plain words; the title says what it compares
const PROJECT_HEAT={'heating up':['Busier lately','More messages and meetings than two weeks ago'],active:['Steady','About as busy as two weeks ago'],
 cooling:['Quieter lately','Fewer messages and meetings than two weeks ago'],dormant:['Quiet','No recent messages or meetings']};
const heatLabel=s=>t(PROJECT_HEAT[s]?.[0]||s);
const heatChip=s=>s?`<span class="chip" style="--c:${PROJECT_COLOR[s]||'var(--muted)'}" title="${esc(t(PROJECT_HEAT[s]?.[1]||''))}">${esc(heatLabel(s))}</span>`:'';
const bar=n=>`<span class="graph-bar" title="${esc(n.closeness?t(n.closeness[0].toUpperCase()+n.closeness.slice(1)+' (a closeness)'):'')}"><i style="width:${Math.min(100,Math.round(100*Math.log1p(n.strength)/Math.log1p(12)))}%"></i></span>`;
const cap=t=>t?t[0].toUpperCase()+t.slice(1):t;
const CLOSENESS_UI={close:'Close (a closeness)',regular:'Regular (a closeness)',occasional:'Occasional (a closeness)',faint:'Faint (a closeness)'};
const personSub=p=>[p.profile?.title,p.role?t(cap(p.role)):CLOSENESS_UI[p.closeness]?t(CLOSENESS_UI[p.closeness]):cap(p.closeness),t(p.seen_only?'last seen {}':'last contact {}',day(p.last_at)),p.usual_gap_days?(Math.round(p.usual_gap_days)<=1?t('usually daily'):t('usually every {} days',Math.round(p.usual_gap_days))):'',p.next_meeting?t('meeting {}',day(p.next_meeting)):''].filter(Boolean).join(' · ');
const graphItem=n=>n.kind==='me'?`<article class="tap person-item about-you-row" data-node="me"><div class="graph-row one">${personPic({name:'You'})}${nodeButton({id:'me',name:'About you'})}</div><p class="graph-sub">Your own addresses and numbers</p></article>`
 :n.kind==='project'?`<article class="tap" data-node="${esc(n.id)}"><div class="graph-row">${nodeButton(n)}${tagMini(n)}${heatChip(n.state)}</div><p class="graph-sub" style="white-space:normal">${n.team_only?'':`${n.last_at?esc(t('Last signal {}',day(n.last_at)))+' · ':''}${esc(t(['{} signal','{} signals'],n.signals))}${n.next_meeting?' · '+esc(t('next meeting {}',day(n.next_meeting))):''}`}${n.org_node?' · '+orgLink(n.org_node):''}${n.people?.length?' · '+esc(n.people.join(', ')):''}${n.via?`<span class="via">${n.team_only?'':' · '}${esc(n.via)}</span>`:''}</p></article>`
 :n.kind==='org'?`<article class="tap" data-node="${esc(n.id)}"><div class="graph-row">${orgPic(n)}${nodeButton(n)}${tagMini(n)}<small>${n.role?esc(t(cap(n.role)))+' · ':''}${n.profile?.industry?esc(n.profile.industry)+' · ':''}${n.team_only?'':esc(t(['{} person','{} people'],n.signals))+' · '}${esc(t('last contact {}',day(n.last_at)))}${n.via?' · <span class="via">'+esc(n.via)+'</span>':''}</small></div></article>`
 :`<article class="tap person-item" data-node="${esc(n.id)}"><div class="graph-row one">${personPic(n)}${nodeButton(n)}${tagMini(n)}${fleetChip(n)}${n.quiet?`<span class="chip" style="--c:var(--orange)">${t('gone quiet')}</span>`:''}${bar(n)}</div><p class="graph-sub" title="${esc(personSub(n)+(n.ids?.length?' · '+n.ids.slice(0,2).join(', '):''))}">${n.via?'<span class="via">'+esc(n.via)+'</span> · ':''}${n.fleet?.machine?t('Has a Machine')+' · ':''}${esc(personSub(n))}${n.org_name&&n.team_only?' · '+esc(n.org_name):''}${n.ids?.length?' · <span class="mono">'+esc(n.ids.slice(0,2).join(', '))+'</span>'+bounceNote(n.ids.slice(0,2).map(i=>n.bounced?.[String(i).replace(/^email:/,'').toLowerCase()]).find(Boolean)):''}</p></article>`;
// Each Graph page's lists are tabs that filter (with their counts; an empty one is not shown) and a quiet menu sets the
// order; every pair is one list on the Machine, loaded a page at a time. The pick is kept per page, also after a person.
const GRAPH_TABS={people:{label:'People',tabs:[['people','All'],['quiet','Gone quiet'],['new','New this week'],['work','Work'],['personal','Personal']],sorts:[['closest','Closest'],['last','Last contact'],['name','Name A–Z'],['value','Value'],['close','Close date']],
  notes:{people:'From your messages, meetings and to-dos. Fades over about two months.',quiet:'People you talk with regularly, silent for much longer than usual.',new:'First seen this week.',work:'Work contacts.',personal:'Personal contacts.'},empty:'Nobody here yet.'},
 orgs:{label:'Organizations',tabs:[['orgs','All'],['warmup','Warm up']],sorts:[['closest','Closest'],['last','Last contact'],['name','Name A–Z'],['value','Value'],['close','Close date']],
  notes:{orgs:'The ones you are most in touch with first.',warmup:'Mail from email warm-up tools, kept out of your Graph.'},empty:'No organizations yet.'},
 projects:{label:'Projects',tabs:[['projects','Open'],['projects_done','Done']],sorts:[['last','Last activity'],['name','Name A–Z'],['stage','Stage'],['value','Value'],['close','Close date']],
  notes:{projects:'Named by the reviews and your to-dos. Busier or quieter compares the last two weeks.',projects_done:'Closed projects.'},empty:'No projects yet.'}};
// A Graph page with nothing on it yet still opens: a short line says how it fills, and its head keeps + New.
const graphEmpty=(pane,team)=>{const [title,how]={people:['Nothing mapped yet.','People appear as messages and meetings come in.'],orgs:['No organizations yet.','They come from the people you’re in touch with.'],projects:['No projects yet.','Reviews name them from your messages and to-dos.']}[pane];
 return `<div class="empty all-clear graph-empty"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>${title}</strong>${team?'':`<span class="poke-line">${how}</span>`}</div></div>`};
const TEAM_NOTES={people:'Everyone your team shares, the closest first.',orgs:'The ones your team is most in touch with.',projects:'Your team’s open projects.'};
const graphPick=(pane,what,fallback)=>{try{return localStorage.getItem(`graph-${what}-${pane}`)||fallback}catch{return fallback}};
const graphKeep=(pane,what,v)=>{try{localStorage.setItem(`graph-${what}-${pane}`,v)}catch{}};
// While a search shows, the list it covers is kept as it was (tab, sort, pages loaded, scroll): emptying the box brings it back at once.
let graphKept=null;
function graphStash(view){if(view.dataset.mode!=='list'||!view.firstChild)return;const scroll=scrollY,f=document.createDocumentFragment();f.append(...view.childNodes);graphKept={f,scroll}}
function graphUnstash(view){if(!graphKept)return false;const k=graphKept;graphKept=null;view.replaceChildren(k.f);view.dataset.mode='list';
 for(const el of view.querySelectorAll('[data-pager]')){const p=pagers.get(el.dataset.pager);if(p&&el.querySelectorAll('.pager-rows>*').length!==p.items.length)el.replaceChildren()}pagerMount(view);  /* rows a page brought in meanwhile */
 notice('');requestAnimationFrame(()=>{if(view.querySelector(`[data-graph-panel="${CSS.escape(graphPane)}"]`))showGraphPane(graphPane);scrollTo(0,k.scroll)});return true}  /* the layout waits for the frame, still before it paints */
let graphLists={},graphLocal=null,graphListsTeam=false;  // a Machine from before the paged lists sends them whole in the overview: they are sorted here
const GRAPH_STAGE={active:0,cooling:1,dormant:2};
const graphSorted=(items,sort)=>[...items].sort(sort==='name'?(a,b)=>(a.name||'').localeCompare(b.name||'',undefined,{sensitivity:'base'}):sort==='last'?(a,b)=>String(b.last_at||'').localeCompare(String(a.last_at||'')):sort==='stage'?(a,b)=>(GRAPH_STAGE[a.state]??3)-(GRAPH_STAGE[b.state]??3)||(b.strength||0)-(a.strength||0):(a,b)=>(b.strength||0)-(a.strength||0));
const warmRow=w=>`<div class="graph-sub relation"><span>${esc(w.name||w.domain)}${w.name&&w.name!==w.domain?` <span class="muted">${esc(w.domain)}</span>`:''}</span><button class="ghost" data-warmup-undo="${esc(w.domain)}">Undo</button></div>`;
// A list's first page comes from the device at first (cachedGet); the live one, when different, redraws the Graph quietly
const graphFresh=()=>{pagerDrop('graph');if(!$('#people').hidden&&!graphNode)people(graphNode,true)};
function graphListPager(list,sort){const fq=graphLocal?'':crmQuery(list),p=pager(crmKey(list,sort),cursor=>graphLocal?Promise.resolve({items:graphSorted(teamKept(list),list==='warmup'?'name':sort),next:null}):(path=>cursor==='0'?cachedGet(path,graphFresh):request(path))(`api/graph/list?list=${list}&sort=${sort}${fq}&cursor=${encodeURIComponent(cursor)}`).then(r=>({items:r.items,next:r.next,total:r.total})),list==='warmup'?warmRow:graphItem);
 if(graphLocal&&!p.items.length&&p.next==='0'){p.items=graphSorted(teamKept(list),list==='warmup'?'name':sort);p.html=p.items.map(p.row).join('');p.next=null}return p}
// The tabs, the order menu and the list sit in their own box, so a tab or order change repaints only them (a Projects
// pane also holds the board)
function graphTabs(pane){const h=graphTabsInner(pane);return h&&`<div data-graph-box="${pane}">${h}</div>`}
function graphTabsInner(pane){const g=GRAPH_TABS[pane],shown=g.tabs.filter(([id])=>graphLists[id]>0&&!(graphListsTeam&&id==='warmup'));if(!shown.length)return'';
 const tab=shown.some(([id])=>id===graphPick(pane,'tab',''))?graphPick(pane,'tab',''):shown[0][0],sort=g.sorts.some(([id])=>id===graphPick(pane,'sort',''))?graphPick(pane,'sort',''):g.sorts[0][0];
 graphListPager(tab,sort);const label=g.sorts.find(([id])=>id===sort)[1];
 const menu=tab==='warmup'?'':`<details class="graph-sort"><summary aria-label="Order: ${esc(label)}">${esc(label)} <span aria-hidden="true">▾</span></summary><div class="graph-sort-list" role="menu">${g.sorts.map(([id,t])=>`<button type="button" role="menuitemradio" aria-checked="${id===sort}" data-graph-sort="${id}">${esc(t)}</button>`).join('')}<hr><button type="button" role="menuitem" data-graph-csv="${tab}" data-sort="${sort}">Download CSV</button>${graphLocal?'':`<button type="button" role="menuitem" data-crm-import="${pane}">Import CSV…</button>${graphLastImport?`<button type="button" role="menuitem" data-crm-undo-import="${graphLastImport.id}">Undo last import</button>`:''}`}</div></details>`;
 return `<div class="graph-tabbar" data-graph-tabs="${pane}">${subTabs(g.label,'data-graph-list',shown.map(([id,t])=>({id,label:t})),tab)}${tab==='warmup'||graphLocal&&!graphListsTeam?'':crmTools(pane,tab)}${menu}</div>${tab==='warmup'||graphLocal&&!graphListsTeam?'':crmActive(pane)}${(graphListsTeam?TEAM_NOTES[tab]:g.notes[tab])?`<p class="graph-note muted">${esc(graphListsTeam?TEAM_NOTES[tab]:g.notes[tab])}</p>`:''}${pagerSlot(crmKey(tab,sort),crmCount(pane)?'Nothing matches these filters.':g.empty,'graph-list')}`}
function graphTabsPaint(pane){const box=document.querySelector(`[data-graph-panel="${pane}"] [data-graph-box]`);if(!box)return;box.innerHTML=graphTabsInner(pane);pagerMount(box);tabsShow(box.querySelector('.sub-tabs'))}
$('#people-view').addEventListener('click',e=>{const c=e.target.closest('[data-graph-csv]');if(c){c.closest('details').open=false;graphCsv(c.dataset.graphCsv,c.dataset.sort).catch(err=>toast(err.message,true));return}});
// A list as a spreadsheet (CSV): every row of the tab, in its order, a page at a time from the Machine. A cell that
// starts like a formula gets a ' so a spreadsheet shows it as text.
const csvCell=v=>{let t=String(v??'');if(/^[=+\-@\t\r]/.test(t))t="'"+t;return /[",\n\r]/.test(t)?'"'+t.replace(/"/g,'""')+'"':t};
async function graphCsv(list,sort){const rows=[];let cursor='0';toast('Getting the list ready…');
 while(cursor!=null&&rows.length<20000){const r=graphLocal?{items:graphSorted(teamKept(list),sort),next:null}:await request(`api/graph/list?list=${list}&sort=${sort}${crmQuery(list)}&cursor=${encodeURIComponent(cursor)}`);rows.push(...(r.items||[]));cursor=r.next??null}
 const orgOf=n=>n.org_name||String(n.org||'').replace(/^org:(named:)?/,''),list_=v=>(v||[]).map(x=>x.value??x).join('; ');
 const cols=list.startsWith('projects')?[['Name',n=>n.name],['Board',n=>n.board],['Stage',n=>n.stage],['Value',n=>n.value],['Expected close',n=>n.close_date],['Organization',n=>n.org_domain||orgOf(n)],['Owner',n=>n.owner_name],['People',n=>(n.people||[]).join('; ')],['State',n=>n.state],['Last activity',n=>n.last_at]]
  :list==='orgs'?[['Name',n=>n.name],['Website',n=>n.profile?.website||n.domain],['Industry',n=>n.profile?.industry],['Size',n=>n.profile?.size||n.profile?.employees],['Location',n=>n.profile?.location],['To you',n=>n.role],['People',n=>n.signals],['Last contact',n=>n.last_at]]
  :[['Name',n=>n.name],['Email',n=>list_(n.emails)||(n.ids||[]).filter(i=>i.startsWith('email:')).map(i=>i.slice(6)).join('; ')],['Phone',n=>list_(n.phones)],['Title',n=>n.profile?.title],['Organization',orgOf],['To you',n=>n.role],['Type',n=>n.side],['Last contact',n=>n.last_at]];
 cols.push(['Tags',n=>(n.tags||[]).join('; ')]);
 const csv=[cols.map(c=>c[0]),...rows.map(n=>cols.map(c=>c[1](n)))].map(r=>r.map(csvCell).join(',')).join('\r\n')+'\r\n';
 const a=document.createElement('a');a.href=URL.createObjectURL(new Blob(['\ufeff'+csv],{type:'text/csv;charset=utf-8'}));a.download=`${list}-${new Date().toISOString().slice(0,10)}.csv`;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),10000);toast(`Downloaded ${rows.length} ${rows.length===1?'row':'rows'}.`)}
$('#people-view').addEventListener('click',e=>{const t=e.target.closest('[data-graph-list]'),o=e.target.closest('[data-graph-sort]'),pane=e.target.closest('[data-graph-tabs]')?.dataset.graphTabs;if(!pane||!t&&!o)return;
 if(t)graphKeep(pane,'tab',t.dataset.graphList);if(o)graphKeep(pane,'sort',o.dataset.graphSort);graphTabsPaint(pane);if(o)document.querySelector(`[data-graph-panel="${pane}"] .graph-sort summary`)?.focus()});
document.addEventListener('click',e=>{for(const d of document.querySelectorAll('.graph-sort[open]'))if(!d.contains(e.target))d.open=false});
document.addEventListener('keydown',e=>{if(e.key!=='Escape')return;const d=document.querySelector('.graph-sort[open],details.fact-menu[open],details.board-menu[open],details.tile-menu[open]');if(d){d.open=false;d.querySelector('summary').focus()}});
document.addEventListener('toggle',e=>{const d=e.target;if(!(d instanceof HTMLDetailsElement)||!d.open)return;const l=d.querySelector(':scope>:is(.fact-menu-list,.graph-sort-list)');if(!l)return;l.style.left=l.style.right=l.style.top=l.style.bottom='';
 // A menu stays on screen: it moves in from an edge, and opens upward when there's no room under its button but there is above it
 let r=l.getBoundingClientRect();if(r.right>innerWidth-8){l.style.left='auto';l.style.right='0';r=l.getBoundingClientRect()}if(r.left<8){l.style.right='auto';l.style.left=(8-d.getBoundingClientRect().left)+'px'}
 const s=d.querySelector(':scope>summary')?.getBoundingClientRect();if(s&&r.bottom>innerHeight-8&&s.top-r.height-8>8){l.style.top='auto';l.style.bottom='calc(100% + 4px)'}},true);
const graphSection=(title,note,items)=>items?.length?`<div class="section-head"><h2>${title}</h2><span class="count">${items.length}</span>${note?`<p>${note}</p>`:''}</div><div class="graph-list">${items.map(graphItem).join('')}</div>`:'';
// Projects as a board: projects of one kind in stages (graph.boards), a view of Graph › Projects next to the list. Board by
// default when there is a board; the choice is remembered on this device. Moves come from what the messages mean; the owner
// drags a tile (or picks a stage from its menu) and that stands until a newer message moves it. Nothing here sends anything.
let graphBoards=[],boardShown=sideStore.get('board-shown')||'',boardStage={},boardOpen=new Set(),fitsOpen=new Set(),fitsPicked=new Map();
const projView=()=>graphBoards.length?(sideStore.get('projects-view')==='list'?'list':'board'):'list';
const shortDay=v=>v?new Date(String(v).length<=10?v+'T12:00':v).toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'}):'';  /* Fri, Oct 23 */
const boardNow=()=>{const fb=graphBoards[0]&&!graphBoards[0].team&&crmF('projects').board;return (fb&&graphBoards.find(b=>String(b.id)===String(fb)))||graphBoards.find(b=>b.name===boardShown)||graphBoards[0]};
const tileWhy=(p,side)=>{const last=p.last_at?' · '+(p.last_event_id?`<button type="button" class="link" data-quote-event="${p.last_event_id}" title="Read its latest message">${esc(shortDay(p.last_at))}</button>`:esc(shortDay(p.last_at))):'';
 if(p.sort_failed)return `<p class="tile-why failed">${esc(p.sort_failed)}${last}</p>`;
 if(p.sort_note)return `<p class="tile-why">Not sorted: ${esc(p.sort_note)}${last}</p>`;
 if(p.outcome)return `<p class="tile-why ${p.outcome}">${p.outcome==='won'?'Won':'Lost'}${p.reason?': '+esc(p.reason):''}${p.at?' · '+esc(shortDay(p.at)):''}</p>`;
 if(p.sorting)return '<p class="tile-why sorting">Sorting from its messages…</p>';const when=p.at?(p.event_id?`<button type="button" class="link" data-quote-event="${p.event_id}" title="Read the message">${esc(shortDay(p.at))}</button>`:esc(shortDay(p.at))):'';
 const what=p.by==='owner'?`Moved to ${esc(p.stage)} by hand`:p.reason?esc(p.first?t('Added: {}',p.reason):t('Moved to {}: {}',p.stage,p.reason)):'';
 return what||when?`<p class="tile-why">${what}${what&&when?' · ':''}${when}</p>`:''};
const stuckDays=p=>p.stage!==boardSide()&&(p.no_reply_days||0)>=10?p.no_reply_days:0;
const boardSide=()=>(boardNow()?.stages||[]).find(s=>s.side)?.name;
// A teammate's project: what happened last, as on its owner's board. Its newest shared timeline line, else why it moved,
// else its stage and when (all of it what the Team Graph shares already). The owner's name only when the column has more than one.
const teamWhy=p=>{const what=p.line||(p.by==='owner'?t('Moved to {} by hand',p.stage):p.reason?t('Moved to {}',p.stage)+': '+p.reason:p.at?t('Moved to {}',p.stage):''),at=p.line?p.line_at:p.at;
 return what?`<p class="tile-why">${esc(what)}${at?' · '+esc(shortDay(at)):''}</p>`:''};
const tile=(p,b,oneOwner)=>{const stuck=stuckDays(p),age=p.days+'d';  /* under a day the move's date below says it */
 const owner=p.owner_name&&!oneOwner?`<p class="tile-owner" title="${p.owner_hand?'Owner':'Closest to them'}">${esc(p.owner_name)}</p>`:'';
 if(p.team_only)return `<article class="tile team${p.yours?' yours':''}" data-node="${esc(p.id)}" data-stage="${esc(p.stage)}" tabindex="0" aria-label="${esc(p.name)}, ${esc(p.stage)}"><div class="tile-row">${orgPic({name:p.org?.name||p.name,profile:{}})}<span class="tile-name" title="${esc(p.name)}">${esc(p.name)}</span></div>${p.next?`<p class="tile-next">${esc(p.next)}</p>`:''}${teamWhy(p)}${owner}</article>`;
 const menu=`<details class="tile-menu"><summary aria-label="More for ${esc(p.name)}" title="Edit or move">⋯</summary><div class="fact-menu-list" role="menu"><button type="button" role="menuitem" data-proj-edit="${esc(p.id)}">Edit</button>${p.outcome==='won'?'':`<button type="button" role="menuitem" data-proj-outcome="won" data-proj-node="${esc(p.id)}">Won</button>`}${p.outcome==='lost'?'':`<button type="button" role="menuitem" data-proj-outcome="lost" data-proj-node="${esc(p.id)}">Lost</button>`}<button type="button" role="menuitem" data-proj-archive="${esc(p.id)}">Archive</button><button type="button" role="menuitem" data-fu-open="${esc(p.id)}">Follow-ups…</button><hr><p>Move to</p>${b.stages.map(s=>`<button type="button" role="menuitem" data-stage-to="${esc(s.name)}" data-stage-node="${esc(p.id)}"${s.name===p.stage?' aria-current="true" disabled':''}>${esc(s.name)}</button>`).join('')}</div></details>`;
 return `<article class="tile" data-node="${esc(p.id)}" data-stage="${esc(p.stage)}" draggable="true" tabindex="0" aria-label="${esc(p.name)}, ${esc(p.stage)}"><div class="tile-row">${orgPic({name:p.org?.name||p.name,profile:{logo:p.org?.logo}})}<span class="tile-name" title="${esc(p.name)}">${esc(p.name).replace(/([a-z])([A-Z])/g,'$1<wbr>$2')}</span>${stuck||!p.days?'':`<span class="tile-age" title="In this stage for ${p.days===0?'less than a day':p.days+(p.days===1?' day':' days')}">${age}</span>`}${menu}</div>`
  +(p.org?.node_id&&p.org.name.toLowerCase()!==p.name.toLowerCase()?`<p class="tile-org">${orgLink({id:p.org.node_id,name:p.org.name})}</p>`:'')
  +(p.value!=null||p.close_date?`<p class="tile-val">${p.value!=null?`<span title="Value">${esc(money(p.value))}</span>`:''}${p.value!=null&&p.close_date?' · ':''}${p.close_date?`<span title="Expected close">closes ${esc(closeDay(p.close_date))}</span>`:''}</p>`:'')+(p.next?`<p class="tile-next">${esc(p.next)}</p>`:'')+(b.team&&!p.mine?teamWhy(p):tileWhy(p))+fuTile(p.follow_up)
  +(p.todos&&!(stuck&&p.card&&p.todos===1)?`<p class="tile-todos">${p.todos===1?'1 to-do':p.todos+' to-dos'}</p>`:'')+(stuck?`<div class="tile-chips"><span class="chip">No reply in ${stuck} days</span>${p.card?`<a class="tile-card" href="#card=${esc(p.card.id)}" title="${esc(p.card.title)}">To-do: ${esc(p.card.title)}</a>`:''}</div>`:'')+(p.owner_name&&!oneOwner?`<p class="tile-owner" title="Owner">${esc(p.owner_name)}</p>`:'')+'</article>'};
const closeDay=v=>{const d=new Date(v+'T12:00');return isNaN(d)?v:d.toLocaleDateString(DL,{day:'numeric',month:'short',...(d.getFullYear()!==new Date().getFullYear()?{year:'numeric'}:{})})};
// Project values in the owner's currency (config "currency", EUR when not set): short on tiles, in full where there is room.
var graphCurrency='EUR';
const moneyFormat=(v,o)=>{try{return new Intl.NumberFormat(undefined,{style:'currency',currency:graphCurrency,...o}).format(v)}catch{return new Intl.NumberFormat(undefined,o).format(v)}};
const money=v=>moneyFormat(v,{notation:v>=10000?'compact':'standard',maximumFractionDigits:v>=10000?1:0});
const moneyFull=v=>moneyFormat(v,{maximumFractionDigits:0});
const LANE_ROWS=()=>matchMedia('(max-width:560px)').matches?6:8;
// A shared board (the Team view) shows Mine, Needs me or All: Mine is what this Machine's owner is on (a thread, owner,
// in their own Graph or a to-do of theirs), Needs me what waits on them (an open to-do, or a thread's newest message is to
// them). It opens on Mine when the board has some of theirs. The rest of a stage folds into "Show N more". Look-alike
// projects of one kind ("Acme CRM evaluation", "Bolt CRM evaluation": three or more alike in a stage) fold into one row.
let boardTeamPick=sideStore.get('board-team-pick')||'',groupOpen=new Set();
const teamPickOf=items=>{const v=boardTeamPick||(items.some(p=>p.yours)?'mine':'all');return v==='needs'||v==='mine'?v:'all'};
const teamPick=b=>teamPickOf(b.projects);
const teamHit=(p,v)=>v==='all'||(v==='mine'?p.yours:p.needs_you);
// Alike: the same last two words ("… CRM evaluation"), else the same first two ("Pilot review: …"), on three or more
const alikeKeys=n=>{const w=String(n||'').trim().split(/\s+/);return w.length>2?[w.slice(-2).join(' '),w.slice(0,2).join(' ').replace(/[:\-–]+$/,'')]:[]};
function teamRows(list){const count={},keys=p=>p.yours?[]:alikeKeys(p.name);for(const p of list)for(const k of keys(p))count[k.toLowerCase()]=(count[k.toLowerCase()]||0)+1;
 const rows=[],at={};for(const p of list){const k=keys(p).find(k=>count[k.toLowerCase()]>=3),id=k?.toLowerCase();if(k){if(at[id]==null){at[id]=rows.length;rows.push({group:k,items:[]})}rows[at[id]].items.push(p)}else rows.push(p)}
 return rows}
const rowSize=r=>r.group?r.items.length:1;
const groupRow=(b,s,r,oneOwner)=>{const key=b.name+'|'+s.name+'|'+r.group.toLowerCase(),last=r.items.map(p=>({p,at:p.line?p.line_at:p.at})).filter(x=>x.at).sort((x,y)=>String(y.at).localeCompare(String(x.at)))[0];
 return `<details class="tile-group" data-group="${esc(key)}"${groupOpen.has(key)?' open':''}><summary><span class="tile-name">${esc(r.group)}</span><span class="badge" title="${esc(t(['{} project','{} projects'],r.items.length))}">${r.items.length}</span>${last?`<span class="tile-why">${esc(t('Newest: {}',last.p.name))} · ${esc(shortDay(last.at))}</span>`:''}</summary><div class="tiles">${r.items.map(p=>tile(p,b,oneOwner)).join('')}</div></details>`};
const lane=(b,s,items,on)=>{const key=b.name+'|'+s.name,oneOwner=items.length>1&&items.every(p=>(p.owner_name||'')===(items[0].owner_name||''));
 if(b.team){const v=teamPick(b),open=boardOpen.has(key),first=[...items.filter(p=>p.yours),...items.filter(p=>!p.yours)],hit=first.filter(p=>teamHit(p,v)),list=v==='all'||open?[...hit,...first.filter(p=>!teamHit(p,v))]:hit;
  const rows=teamRows(list),wide=s.side&&!matchMedia('(max-width:560px)').matches,cut=v==='all'&&!open&&!wide?LANE_ROWS():rows.length,shown=rows.slice(0,cut),more=items.length-shown.reduce((n,r)=>n+rowSize(r),0);
  return `<section class="lane${s.side?' side':''}${on?' on':''}" data-lane="${esc(s.name)}" aria-label="${esc(s.name)}"><div class="lane-h"><h4>${esc(s.name)}</h4><span>${v==='all'?items.length:`${hit.length}/${items.length}`}</span></div>`
   +`<div class="tiles">${shown.length?shown.map(r=>r.group?groupRow(b,s,r,oneOwner):tile(r,b,oneOwner)).join(''):more>0?'':'<p class="lane-empty">Nothing here yet</p>'}</div>${more>0?`<button type="button" class="lane-more" data-lane-more="${esc(key)}">Show ${more} more</button>`:''}</section>`}
 const all=boardOpen.has(key)||s.side&&!matchMedia('(max-width:560px)').matches,shown=all?items:items.slice(0,LANE_ROWS()),stuck=items.filter(stuckDays).length;
 return `<section class="lane${s.side?' side':''}${on?' on':''}" data-lane="${esc(s.name)}" aria-label="${esc(s.name)}"><div class="lane-h"><h4>${esc(s.name)}</h4><span>${items.length}</span>${items.some(p=>p.value!=null)?`<span class="lane-total" title="Total value">${esc(money(items.reduce((t,p)=>t+(p.value||0),0)))}</span>`:''}</div>${s.hint?`<p class="lane-hint">${esc(s.hint)}</p>`:''}${stuck?`<p class="lane-sum"><button type="button" class="link" data-crm-waiting aria-pressed="${!!crmF('projects').waiting}" title="${crmF('projects').waiting?'Show all':'Show only these'}">${stuck} with no reply in 10+ days</button>${fuNudge(b,s)}</p>`:''}`
  +`<div class="tiles">${items.length?shown.map(p=>tile(p,b,oneOwner)).join(''):'<p class="lane-empty">Nothing here yet</p>'}</div>${items.length>shown.length?`<button type="button" class="lane-more" data-lane-more="${esc(key)}">Show ${items.length-shown.length} more</button>`:''}${b.team||s.side?'':`<button type="button" class="lane-add" data-proj-new data-proj-stage="${esc(s.name)}" aria-label="Add a project to ${esc(s.name)}">+ Add</button>`}</section>`};
// A new board looks through the history once: "Looking through your history…", then what it found (graph.backfill_view)
// "N projects could belong here": Add or Leave out one, or tick some (or Select all) and do them at once. A project that bundles several
// counterparts says so and becomes one project per counterpart. The fold stays open (and in place) until nothing is left.
const fitsBulkText=(b,picked)=>{const n=picked.size;return n?[`Add ${n}`,`Leave out ${n}`]:['Add all','Leave out all']};
function fitsReview(b){const ids=new Set(b.maybes.map(m=>m.id)),picked=new Set([...(fitsPicked.get(b.id)||[])].filter(i=>ids.has(i)));fitsPicked.set(b.id,picked);
 const [add,skip]=fitsBulkText(b,picked),all=picked.size===b.maybes.length,n=b.maybes.length;
 return `<details class="board-fits" data-fits-board="${b.id}"${fitsOpen.has(b.id)?' open':''}><summary><b>${n} project${n===1?'':'s'} could belong here</b> · Review</summary>`
 +(n>1?`<div class="fits-bulk"><label class="fit-pick"><input type="checkbox" data-fit-all="${b.id}"${all?' checked':''} aria-label="Select all"><span>Select all</span></label><span class="fit-acts"><button type="button" class="ghost" data-fit-bulk="add" data-fit-board="${b.id}">${add}</button><button type="button" class="ghost" data-fit-bulk="skip" data-fit-board="${b.id}">${skip}</button></span></div>`:'')
 +`<ul>${b.maybes.map(m=>`<li>${n>1?`<label class="fit-pick"><input type="checkbox" data-fit-pick="${esc(m.id)}" data-fit-board="${b.id}"${picked.has(m.id)?' checked':''} aria-label="Select ${esc(m.name)}"></label>`:''}<span class="fit-text">${esc(m.name)}${m.split?`<small>Splits into ${m.split} projects, one per counterpart</small>`:m.why?`<small>${esc(m.why)}</small>`:''}</span><span class="fit-acts"><button type="button" class="ghost" data-fit-add="${esc(m.id)}" data-fit-board="${b.id}"${m.split?` aria-label="Add as ${m.split} projects"`:''}>${m.split?`Add as ${m.split}`:'Add'}</button><button type="button" class="ghost" data-fit-skip="${esc(m.id)}" data-fit-board="${b.id}">Leave out</button></span></li>`).join('')}</ul></details>`}
function fitsBulkSync(box){const b=+box.dataset.fitsBoard,picked=fitsPicked.get(b)||new Set(),boxes=[...box.querySelectorAll('[data-fit-pick]')],all=box.querySelector('[data-fit-all]');
 if(all){all.checked=boxes.length>0&&picked.size===boxes.length;all.indeterminate=picked.size>0&&picked.size<boxes.length}
 const [add,skip]=fitsBulkText(null,picked),bs=box.querySelectorAll('[data-fit-bulk]');if(bs.length){bs[0].textContent=add;bs[1].textContent=skip}}
document.addEventListener('toggle',e=>{const d=e.target;if(d?.classList?.contains('board-fits')){const b=+d.dataset.fitsBoard;d.open?fitsOpen.add(b):fitsOpen.delete(b)}},true);
document.addEventListener('change',e=>{const c=e.target.closest?.('[data-fit-pick],[data-fit-all]'),box=c?.closest('.board-fits');if(!box)return;const b=+box.dataset.fitsBoard,picked=fitsPicked.get(b)||new Set();fitsPicked.set(b,picked);
 if(c.dataset.fitAll){for(const x of box.querySelectorAll('[data-fit-pick]')){x.checked=c.checked;c.checked?picked.add(x.dataset.fitPick):picked.delete(x.dataset.fitPick)}}else c.checked?picked.add(c.dataset.fitPick):picked.delete(c.dataset.fitPick);
 fitsBulkSync(box)});
async function fitsDecide(t,board,ids,add){const box=t.closest('.board-fits');fitsOpen.add(board);for(const b of box?.querySelectorAll('button')||[])b.disabled=true;const y=scrollY;
 const r=await graphPost('board_fit',ids.length===1&&!t.dataset.fitBulk?{board_id:board,node_id:ids[0],add}:{board_id:board,node_ids:ids,add});
 const picked=fitsPicked.get(board);if(picked)for(const i of ids)picked.delete(i);
 const n=r.projects||0,done=r.decided??1;
 toastFitUndo((add?(n>1?`Added ${n} projects.`:n===1?'Added to the board.':'Nothing new to add.'):done>1?`Left out ${done}.`:'Left out.')+(r.skipped?` ${r.skipped} could not be decided.`:''),r.undo,board);
 graphMineBoards=null;await people('',true);scrollTo({top:y})}
function toastFitUndo(text,token,board){toast(text);if(token){$('#toast').insertAdjacentHTML('beforeend',` <button type="button" data-fit-undo="${esc(token)}" data-fit-board="${board}">Undo</button>`);clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),10000)}}
// Share board… and Share with… on a thread: chosen teammates of the Work Fleet get it, sealed to their Machines only.
// Personal, other companies' accounts and automated mail never go, also on a shared board (shared_graph.Scope.granted).
let sp=null;
function spDraw(){const f=$('#share-people-form'),key=p=>p.fleet+'|'+p.member,team=sp.people||graphTeammates,names=team.filter(p=>sp.on.has(key(p))).map(p=>p.name);
 f.innerHTML=`<div class="snooze-heading"><h2 id="share-people-title">${esc(sp.title)}</h2><button type="button" data-sp-close aria-label="Close">×</button></div>`
  +`<fieldset class="sp-people"><legend>Who gets it</legend>${team.map(p=>`<label><input type="checkbox" value="${esc(key(p))}"${sp.on.has(key(p))?' checked':''}> ${esc(p.name)}</label>`).join('')}</fieldset>`
  +`<p class="sp-line" role="status">${esc(names.length?sp.line(namesLine(names),names.length>1):sp.was?'Nobody else. It goes back to Only you.':'Choose who gets it.')}</p>`
  +'<p class="fleet-fine">Encrypted for their Machines only. Taking someone off removes it from their Machine.</p>'
  +`<p class="ed-note warn" data-sp-error role="alert" hidden></p><div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-sp-close>Cancel</button><button class="primary"${names.length||sp.was?'':' disabled'}>${names.length||!sp.was?'Share':'Stop sharing'}</button></div>`}
function spOpen(o){sp={...o,on:new Set(o.chosen.map(p=>p.fleet+'|'+p.member)),was:o.chosen.length>0};spDraw();const d=$('#share-people');if(!d.open)d.showModal();d.querySelector('.sp-people input')?.focus()}
function boardShareOpen(b){if(!b)return;const n=b.projects.filter(p=>p.visibility!=='only_you').length;
 spOpen({title:'Share '+b.name,action:'graph_board_share',args:{board_id:b.id},chosen:b.visibility==='people'?b.shared_with||[]:[],
  line:(who,many)=>`${who} ${many?'get':'gets'} ${n===1?'this project with its full timeline':`these ${n} projects with their full timelines`}, deals too. Personal and other companies never go.`,
  done:(who)=>who?`Shared with ${who}.`:'Back to Only you. Taken back from their Machines.'})}
function threadShareOpen(eventId,people){spOpen({title:'Share this thread',action:'graph_thread_share',args:{event_id:Number(eventId)},
 chosen:graphTeammates.filter(p=>(people||[]).includes(p.name)),line:(who,many)=>`${who} ${many?'get':'gets'} this thread, also if it is sensitive. Personal never goes.`,
 done:(who)=>who?`Shared with ${who}.`:'Taken back from their Machines.'})}
$('#share-people-form').addEventListener('change',e=>{const i=e.target;if(!sp||i.type!=='checkbox')return;i.checked?sp.on.add(i.value):sp.on.delete(i.value);spDraw();$('#share-people-form').querySelector(`input[value="${CSS.escape(i.value)}"]`)?.focus()});
$('#share-people-form').addEventListener('click',e=>{if(e.target.closest('[data-sp-close]'))$('#share-people').close()});
$('#share-people-form').addEventListener('submit',async e=>{e.preventDefault();if(!sp)return;const btn=e.submitter||$('#share-people-form button.primary'),err=$('#share-people-form [data-sp-error]');
 const chosen=[...sp.on].map(k=>{const [fleet,member]=k.split('|');return {fleet,member}}),who=namesLine((sp.people||graphTeammates).filter(p=>sp.on.has(p.fleet+'|'+p.member)).map(p=>p.name)),after=sp.after;btn.disabled=true;
 try{await graphPost(sp.action,{...sp.args,people:chosen});const msg=sp.done(who);$('#share-people').close();toast(msg);await (after?after():people(graphNode,true))}catch(x){errCaught(x);err.textContent=x.message;err.hidden=false}finally{btn.disabled=false}});
$('#share-people').addEventListener('close',()=>{sp=null});
const backfillNote=f=>f.state==='running'?'<span class="backfill-run">Looking through your history…</span>':f.added?`${f.added} added from your history${f.review?` · ${f.review} to review`:''}`:f.review?`${f.review} from your history to review`:'Nothing more in your history';
// A board's stage filter: the stages it shows, kept per board on this device; none picked shows them all.
const boardStagesAll=()=>{try{return JSON.parse(sideStore.get('board-stages')||'{}')||{}}catch{return{}}};
const boardStagesOf=b=>{const p=boardStagesAll()[b.name];return Array.isArray(p)&&p.some(n=>b.stages.some(s=>s.name===n))?p:null};
function boardStagesSet(name,list){const all=boardStagesAll();if(list?.length)all[name]=list;else delete all[name];sideStore.set('board-stages',JSON.stringify(all));boardRedraw()}
function boardFilterOpen(){const b=boardNow();if(!b)return;const pick=boardStagesOf(b);crm={mode:'board-stages',board:b.name};
 $('#crm-form').innerHTML=crmHead('Stages to show')+`<fieldset class="board-stage-pick" aria-label="Stages of ${esc(b.name)}">${b.stages.map(s=>`<label class="ed-check"><input type="checkbox" name="stage" value="${esc(s.name)}"${!pick||pick.includes(s.name)?' checked':''}> ${esc(s.side?'Stalled':s.name)} <span class="muted">${b.projects.filter(p=>p.stage===s.name).length}</span></label>`).join('')}</fieldset>`
  +crmFoot('Show','<button type="button" class="ghost" data-crm-clear-all>Show all</button>');crmShow()}
document.addEventListener('click',e=>{if(e.target.closest('[data-board-filter]')){e.preventDefault();return boardFilterOpen()}if(e.target.closest('[data-board-filter-clear]')){e.preventDefault();const b=boardNow();if(!b)return;const all=boardStagesAll();delete all[b.name];sideStore.set('board-stages',JSON.stringify(all));crmSet('projects',{})}});  /* both: the filters and the stages; crmSet draws the List and the Board */
// The Board shows the List's filters (crmF('projects'), one set for both). On the Mine tab the Machine says which
// projects they keep (api/graph/list?ids=1, the List's own query), a Board filter picks the board and a Stage filter its
// column; on the Team tab they go by who shared it and its state, with Mine, Needs me or All.
let boardIds={q:null,ids:null,seq:0};
function boardKeep(b){if(b.team){const f=teamFilters.projects||{};return f.by||f.state?p=>(!f.by||viaNames(p).includes(f.by))&&(!f.state||(p.state||'active')===f.state):null}
 const q=crmQuery('projects');if(!q)return null;if(boardIds.q===q&&boardIds.ids)return p=>boardIds.ids.has(p.id);
 if(boardIds.want!==q){const seq=++boardIds.seq;boardIds.want=q;request('api/graph/list?list=projects&ids=1'+q).then(r=>{if(seq!==boardIds.seq)return;boardIds={...boardIds,q,ids:new Set(r.ids||[])};boardRedraw()},err=>{if(seq===boardIds.seq){boardIds.want=null;toast(err.message,true)}})}
 return boardIds.ids?p=>boardIds.ids.has(p.id):null}  /* the last answer until the new one is in */
const boardActive=(b,pick,stages)=>{const chips=crmChips('projects')+(pick?`<span class="chip">${esc(t('Stages: {}',stages.map(s=>s.side?'Stalled':s.name).join(', ')))}</span>`:'');
 return chips?`<p class="graph-active board-active">${chips}<button type="button" class="link" data-board-filter-clear>Clear</button></p>`:''};
function boardView(){const b0=boardNow();if(!b0)return '<div class="empty all-clear"><div><strong>No boards yet.</strong>Projects of one kind show here in stages, as your messages move them.</div></div>';
 const keep=boardKeep(b0),b=keep?{...b0,projects:b0.projects.filter(keep)}:b0,fs=!b0.team&&crmF('projects').stage;
 const pick=boardStagesOf(b),picked=pick?b.stages.filter(s=>pick.includes(s.name)):b.stages,one=fs&&picked.filter(s=>s.name.toLowerCase()===String(fs).toLowerCase()),stages=one?.length?one:picked;
 const by=s=>b.projects.filter(p=>p.stage===s.name),main=stages.filter(s=>!s.side),hits=s=>b.team?by(s).filter(p=>teamHit(p,teamPick(b))).length:by(s).length,firstFull=(stages.find(hits)||stages.find(s=>by(s).length))?.name||stages[0].name;
 const on=stages.some(s=>s.name===boardStage[b.name])?boardStage[b.name]:firstFull;
 return `<div class="board-head"><div><div class="board-name-row">${graphBoards.length>1?`<select class="board-pick" aria-label="Board">${graphBoards.map(x=>`<option${x.name===b.name?' selected':''}>${esc(x.name)}</option>`).join('')}</select>`:''}<h3 class="board-title" title="${esc(b.name)}">${esc(b.name)}</h3>${b.team?'':`<details class="board-menu"><summary aria-label="Board options" title="Board options">${DOTS}</summary><div class="fact-menu-list" role="menu"><button type="button" role="menuitem" data-board-edit="${b.id}">Edit board</button><button type="button" role="menuitem" data-fu-open="board:${b.id}">Follow-ups…</button>${graphTeammates.length?`<button type="button" role="menuitem" data-board-share="${b.id}">Share board…</button>`:''}${b.default||graphBoards.length<2?'':`<button type="button" role="menuitem" data-board-default="${b.id}">Open on this board</button>`}<button type="button" role="menuitem" data-board-new>New board</button></div></details>`}</div><p class="board-sub">${b.visibility==='only_you'||b.visibility==='people'?seenBy(b.visibility,(b.shared_with||[]).map(x=>x.name))+' · ':''}${b0.projects.length} project${b0.projects.length===1?'':'s'}${b0.stuck?` · ${b0.stuck} waiting on a reply`:''}${b.sorting?` · sorting ${b.sorting}`:''}${b.team?'':fuBoardLine(b)}${b.team&&boardOwner(b)?' · '+esc(t('Owner: {}',boardOwner(b))):''} · ${!b.team&&b.backfill?backfillNote(b.backfill):`a review moves them as ${b.team?'the team\'s':'your'} messages come in`}</p></div>`
  +(graphBoards.length>1?`<div class="board-chips" role="group" aria-label="Boards">${graphBoards.map(x=>`<button type="button" data-board="${esc(x.name)}" aria-pressed="${x.name===b.name}">${esc(x.name)}</button>`).join('')}</div>`:'')
  +`<div class="board-tools">${b.team?teamPicker(b):''}${crmFilterButton('projects','board-mine board-filter')}<button type="button" class="board-mine board-filter" data-board-filter aria-haspopup="dialog" aria-pressed="${!!pick}" title="Show only some stages"><svg class="board-stages-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5v14M12 5v9M19 5v6"/></svg>Stages${pick?` <span class="badge">${picked.length}</span>`:''}</button>`+(b.team?'':'<button type="button" class="board-new" data-proj-new>+ New project</button>')+'</div></div>'
  +(!b.team&&b.maybes?.length?fitsReview(b):'')+(b.team?teamEmpty(b):'')+pipeline(b)
  +boardActive(b,pick,picked)
  +`<div class="sub-tabs stage-tabs" role="tablist" aria-label="Stages">${stages.map(s=>`<button type="button" role="tab" data-stage-tab="${esc(s.name)}" aria-selected="${s.name===on}"><span class="ell">${esc(s.side?'Stalled':s.name)}</span> <span class="badge">${hits(s)}</span></button>`).join('')}</div>`
  +`<div class="pboard-wrap"><div class="pboard" style="--lanes:${Math.max(1,main.length)}">${stages.map(s=>lane(b,s,by(s),s.name===on)).join('')}</div></div>`}
const teamPicker=b=>teamSeg(b.projects);
const teamSeg=items=>{const v=teamPickOf(items),n=k=>items.filter(p=>teamHit(p,k)).length;
 return `<div class="board-seg" role="group" aria-label="Show">${[['mine','Mine'],['needs','Needs me'],['all','All']].map(([k,label])=>`<button type="button" data-board-team="${k}" aria-pressed="${k===v}"><span>${label}</span>${k==='all'?'':` <span class="badge">${n(k)}</span>`}</button>`).join('')}</div>`};
const boardOwner=b=>{const o=b.projects[0]?.owner_name;return o&&b.projects.length>1&&b.projects.every(p=>p.owner_name===o)?o:''};
const teamEmpty=b=>{const v=teamPick(b);return v!=='all'&&!b.projects.some(p=>teamHit(p,v))?`<p class="graph-active board-active">${v==='mine'?'None of these are yours yet.':'Nothing here needs you now.'}</p>`:''};
// Which board shows: the Team view keeps its own, so it opens on the board with most of the owner's projects (listed first)
const boardKey=()=>graphBoards[0]?.team?'team-board-shown':'board-shown';
const projectsPane=g=>{graphBoards=g.boards||[];boardShown=sideStore.get(boardKey())||'';graphSuggest=g.board_suggestions||[];graphProjNames=g.project_names||[];if(!g.team){graphMineBoards=graphBoards;graphPeopleNames=g.person_names||graphPeopleNames}const v=projView();
 if(!graphBoards.length){const list=graphTabs('projects');return list||graphSuggest.length?suggestBox()+(graphSuggest.length?'':'<p class="board-start"><button type="button" class="ghost" data-board-new>Start a board</button></p>')+list:graphEmpty('projects',g.team)}  /* no projects yet: the pane still opens */
 return suggestBox()+`<div class="proj-list"${v==='list'?'':' hidden'}>${graphTabs('projects')}</div><div class="proj-board"${v==='board'?'':' hidden'}>${boardView()}</div>`};
function boardRedraw(){const el=$('#people-view .proj-board');if(el){const x=el.querySelector('.pboard')?.scrollLeft||0;el.innerHTML=boardView();const nb=el.querySelector('.pboard');if(nb)nb.scrollLeft=x;tabsShow(el.querySelector('.stage-tabs'))}}
function projectsViewSet(v){sideStore.set('projects-view',v);const view=$('#people-view');view.querySelector('.proj-list')?.toggleAttribute('hidden',v!=='list');view.querySelector('.proj-board')?.toggleAttribute('hidden',v!=='board');pageHead();tabsShow(view.querySelector('.stage-tabs'))}
async function boardMove(node,stage){const b=boardNow(),p=b?.projects.find(x=>x.id===node);if(!p||p.stage===stage)return;const was=p.stage;
 Object.assign(p,{stage,by:'owner',at:new Date().toISOString(),event_id:null,days:0});boardRedraw();
 try{await graphPost('graph_stage',{node_id:node,stage});toast('Moved to '+stage+'.');await people('',true)}catch(err){errCaught(err);Object.assign(p,{stage:was});boardRedraw();toast(err.message,true)}}
$('#page-head').addEventListener('click',e=>{const b=e.target.closest('[data-proj-view]');if(b)projectsViewSet(b.dataset.projView)});
// Mine, Needs me or All: one choice for the team's List and Board
function teamPickSet(v){boardTeamPick=v;sideStore.set('board-team-pick',v);graphTabsPaint('projects');boardRedraw()}
$('#people-view').addEventListener('click',e=>{const pick=e.target.closest('.proj-list [data-board-team]');if(!pick)return;e.stopPropagation();teamPickSet(pick.dataset.boardTeam)},true);
$('#people-view').addEventListener('click',e=>{if(!e.target.closest('.proj-board'))return;
 const chip=e.target.closest('[data-board]');if(chip){e.stopPropagation();boardPick(chip.dataset.board);return}
 const pick=e.target.closest('[data-board-team]');if(pick){e.stopPropagation();teamPickSet(pick.dataset.boardTeam);return}
 const st=e.target.closest('[data-stage-tab]');if(st){e.stopPropagation();boardStage[boardNow().name]=st.dataset.stageTab;boardRedraw();return}
 const more=e.target.closest('[data-lane-more]');if(more){e.stopPropagation();boardOpen.add(more.dataset.laneMore);boardRedraw();return}
 const to=e.target.closest('[data-stage-to]');if(to){e.stopPropagation();to.closest('details').open=false;boardMove(to.dataset.stageNode,to.dataset.stageTo);return}
 if(e.target.closest('.tile-menu,.tile a[href]'))e.stopPropagation()},true);
$('#people-view').addEventListener('change',e=>{if(!e.target.matches?.('.board-pick'))return;boardPick(e.target.value)});
function boardPick(name){boardShown=name;sideStore.set(boardKey(),boardShown);const f=crmF('projects'),to=graphBoards.find(b=>b.name===name);
 if(f.board&&to&&!to.team){const next={...f,board:String(to.id)};delete next.stage;return crmSet('projects',next)}boardRedraw()}  /* a Board filter follows the board picked; its Stage was another board's */
document.addEventListener('toggle',e=>{const d=e.target;if(d?.classList?.contains('tile-group'))d.open?groupOpen.add(d.dataset.group):groupOpen.delete(d.dataset.group)},true);
$('#people-view').addEventListener('keydown',e=>{const t=e.target.closest?.('.tile');if(t&&e.target===t&&(e.key==='Enter'||e.key===' ')){e.preventDefault();graphOpen(t.dataset.node)}});
// Boards the owner makes. A review suggests one for a group of projects of one kind ("Start a board for Hiring?"): Save,
// Edit or Not now; nothing is a board until it's saved. The same editor makes a new board and edits one from its ⋯
// menu: the name, the stages (rename, reorder, add, remove), the Stalled row, which projects belong and the projects
// on it. After a save, reviews place its projects by their messages. Deleting a board keeps its projects.
let graphSuggest=[],graphProjNames=[],ed=null;
const seenBy=(v,names)=>v==='only_you'?`<span class="seen-by">${LOCK}Only you</span>`:v==='people'?`<span class="seen-by">${LOCK}${names?.length?'Shared with '+esc(namesLine(names)):'Chosen teammates'}</span>`:'<span class="seen-by">Team</span>';
const namesLine=n=>n.length<3?n.join(' and '):n.slice(0,-1).join(', ')+' and '+n[n.length-1];
const suggestBox=()=>graphSuggest.slice(0,3).map(s=>
 `<article class="board-suggest" data-suggest="${s.id}"><div class="board-suggest-text"><p class="board-suggest-title">Start a board for ${esc(s.name)}?</p><p class="board-suggest-sub">${seenBy(s.visibility)} · ${s.projects.length} projects${s.reason?' · '+esc(s.reason):''}</p><ol class="stage-flow" aria-label="Stages">${s.stages.map(x=>`<li>${esc(x.name)}</li>`).join(' ')}</ol></div>`
  +`<div class="board-suggest-actions"><button type="button" class="primary" data-suggest-save>Save</button><button type="button" class="ghost" data-suggest-edit>Edit</button><button type="button" class="ghost" data-suggest-dismiss>Not now</button></div></article>`).join('');
const boardSavedToast=(r,name)=>{const moved=(r.moved||[]).map(m=>m.to?`${m.count} from ${m.from} moved to ${m.to}.`:`${m.count} stalled left the board.`).join(' ');
 toast(`Saved ${name}.${r.added?' A review sorts its projects in a few minutes.':''}${moved?' '+moved:''}`)};
async function boardSave(args){const r=await graphPost('board_save',args);boardShown=r.name;sideStore.set('board-shown',boardShown);sideStore.set('projects-view','board');boardSavedToast(r,r.name);await people('',true);return r}
function edOpen(from){const b=from?.board,s=from?.suggestion;
 ed=b?{id:b.id,name:b.name,stages:b.stages.filter(x=>!x.side).map(x=>({name:x.name,was:x.name,...(x.hint?{hint:x.hint}:{})})),side:b.side!==false,about:b.about||'',visibility:b.visibility||'team',on:new Set(b.visibility==='people'?(b.shared_with||[]).map(x=>x.fleet+'|'+x.member):[]),was:b.visibility==='people',projects:b.projects.map(p=>({id:p.id,name:p.name})),counts:Object.fromEntries(b.stages.map(x=>[x.name,b.projects.filter(p=>p.stage===x.name).length]))}
  :s?{suggestion:s.id,name:s.name,stages:s.stages.map(x=>({...x})),side:true,about:s.about||'',visibility:s.visibility||'team',projects:s.projects.map(p=>({...p})),counts:{}}
  :{name:'',stages:[{name:'Started'},{name:'In progress'},{name:'Done'}],side:true,about:'',visibility:'team',projects:[],counts:{}};
 edDraw();const d=$('#board-dialog');if(!d.open)d.showModal();d.querySelector('[name="name"]')?.focus()}
function edGone(){if(!ed?.id)return '';const names=ed.stages.map(x=>x.was).filter(Boolean),old=Object.keys(ed.counts).filter(n=>n!==STALLED_ROW);
 const notes=old.filter(n=>!names.includes(n)&&ed.counts[n]).map(n=>{const i=old.indexOf(n),earlier=old.slice(0,i).filter(x=>names.includes(x)),to=earlier.length?ed.stages.find(x=>x.was===earlier.at(-1)).name:ed.stages[0]?.name;return `${ed.counts[n]} in ${n} go to ${to||'the first stage'}.`});
 if(!ed.side&&ed.counts[STALLED_ROW])notes.push(`${ed.counts[STALLED_ROW]} stalled leave the board.`);return notes.length?`<p class="ed-note warn" role="status">${esc(notes.join(' '))}</p>`:''}
const STALLED_ROW='Stalled or declined';
function edDraw(){const e=ed,f=$('#board-form'),last=e.stages.length-1,pick=graphProjNames.filter(p=>!e.projects.some(x=>x.id===p.id));
 f.innerHTML=`<div class="snooze-heading"><h2 id="board-dialog-title">${e.id?'Edit board':e.suggestion?'Start a board':'New board'}</h2><button type="button" data-ed-close aria-label="Close">×</button></div>`
  +`<label class="ed-field">Name<input name="name" maxlength="60" value="${esc(e.name)}" placeholder="e.g. Partner listings" autocomplete="off"></label>`
  +`<fieldset class="ed-stages"><legend>Stages, in order</legend><ol>${e.stages.map((x,i)=>`<li><input data-ed-stage="${i}" maxlength="30" value="${esc(x.name)}" aria-label="Stage ${i+1}" autocomplete="off"><button type="button" class="icon" data-ed-up="${i}" aria-label="Move ${esc(x.name||'this stage')} up"${i?'':' disabled'}>↑</button><button type="button" class="icon" data-ed-down="${i}" aria-label="Move ${esc(x.name||'this stage')} down"${i<last?'':' disabled'}>↓</button><button type="button" class="icon" data-ed-del="${i}" aria-label="Remove ${esc(x.name||'this stage')}"${last?'':' disabled'}>×</button></li>`).join('')}</ol>`
  +`${e.stages.length<8?'<button type="button" class="ghost" data-ed-add>Add stage</button>':''}<label class="ed-check"><input type="checkbox" name="side"${e.side?' checked':''}> A “Stalled or declined” row</label></fieldset>`
  +`<label class="ed-field">Which projects belong<textarea name="about" rows="2" maxlength="200" placeholder="e.g. Partners we list our app with, one per partner">${esc(e.about)}</textarea></label>`
  +edSeen(e)
  +`<fieldset class="ed-projects"><legend>Projects<span class="count">${e.projects.length}</span></legend><ul>${e.projects.map(p=>`<li><span title="${esc(p.name)}">${esc(p.name)}</span><button type="button" class="icon" data-ed-drop="${esc(p.id)}" aria-label="Take ${esc(p.name)} off">×</button></li>`).join('')||'<li class="muted">None yet. Reviews add the ones that fit.</li>'}</ul>`
  +`<input name="add" list="board-dialog-names" placeholder="Add a project" aria-label="Add a project" autocomplete="off"><datalist id="board-dialog-names">${pick.slice(0,500).map(p=>`<option value="${esc(p.name)}"></option>`).join('')}</datalist></fieldset>`
  +edGone()+'<p class="ed-note">After you save, The Machine sorts its projects into stages from your messages.</p>'
  +`<p class="ed-note warn" data-ed-error role="alert" hidden></p><div class="ed-actions">${e.id?`<button type="button" class="ghost danger" data-ed-delete>${e.sure?'Delete? Its projects stay':'Delete board'}</button>`:''}<span class="grow"></span><button type="button" class="ghost" data-ed-close>Cancel</button><button class="primary">Save</button></div>`}
/* Who sees it: Only you, Chosen people (the Share board… picker, inline) or Your team. Chosen people goes through
   graph_board_share, so the editor and the share sheet always say the same */
const edKey=p=>p.fleet+'|'+p.member,edChosen=e=>graphTeammates.filter(p=>e.on?.has(edKey(p)));
function edSeen(e){const v=e.visibility||'team',r=(val,label)=>`<label><input type="radio" name="visibility" value="${val}"${v===val?' checked':''}> ${label}</label>`,names=edChosen(e).map(p=>p.name);
 return `<fieldset class="ed-seen"><legend>Who sees it</legend>${r('only_you','Only you')}${graphTeammates.length||v==='people'?r('people','Chosen people'):''}${r('team','Your team')}</fieldset>`
  +(v==='people'?`<fieldset class="sp-people ed-people"><legend>Who gets it</legend>${graphTeammates.map(p=>`<label><input type="checkbox" name="person" value="${esc(edKey(p))}"${e.on?.has(edKey(p))?' checked':''}> ${esc(p.name)}</label>`).join('')}</fieldset>`
   +`<p class="sp-line" role="status">${esc(names.length?`Shared with ${namesLine(names)}, encrypted for their Machines only.`:'Choose who gets it.')}</p>`:'')}
const edFocus=sel=>{const before=document.activeElement;requestAnimationFrame(()=>{if(document.activeElement===before)$('#board-form').querySelector(sel)?.focus()})};  /* don't steal focus from a field the owner chose meanwhile */
$('#board-form').addEventListener('input',e=>{const t=e.target;if(!ed)return;if(t.name==='name')ed.name=t.value;else if(t.name==='about')ed.about=t.value;else if(t.dataset.edStage)ed.stages[+t.dataset.edStage].name=t.value;
 else if(t.name==='add'){const p=graphProjNames.find(x=>x.name.toLowerCase()===t.value.trim().toLowerCase());if(p&&!ed.projects.some(x=>x.id===p.id)){ed.projects.push({id:p.id,name:p.name});edDraw();edFocus('[name="add"]')}}});
$('#board-form').addEventListener('change',e=>{const t=e.target;if(!ed)return;if(t.name==='visibility'||t.name==='person'){edSync();if(t.name==='visibility')ed.visibility=t.value;else{ed.on??=new Set();t.checked?ed.on.add(t.value):ed.on.delete(t.value)}
  edDraw();edFocus(`input[name="${t.name}"][value="${CSS.escape(t.value)}"]`);return}if(e.target.name==='side'&&ed){ed.side=e.target.checked;edDraw();edFocus('[name="side"]')}});
$('#board-form').addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.name==='add'){e.preventDefault()}});
const edSync=()=>{const f=$('#board-form');if(!ed)return;ed.name=f.elements.name?.value??ed.name;ed.about=f.elements.about?.value??ed.about;for(const i of f.querySelectorAll('[data-ed-stage]'))if(ed.stages[+i.dataset.edStage])ed.stages[+i.dataset.edStage].name=i.value};  /* what is typed counts, also when no input event came */
$('#board-form').addEventListener('click',async e=>{const b=e.target.closest('button');if(!b||!ed)return;edSync();const st=ed.stages;
 if(b.hasAttribute('data-ed-close')){$('#board-dialog').close();return}
 if(b.dataset.edUp){const i=+b.dataset.edUp;[st[i-1],st[i]]=[st[i],st[i-1]];edDraw();edFocus(`[data-ed-up="${i-1}"]:not(:disabled),[data-ed-down="${i-1}"]`);return}
 if(b.dataset.edDown){const i=+b.dataset.edDown;[st[i+1],st[i]]=[st[i],st[i+1]];edDraw();edFocus(`[data-ed-down="${i+1}"]:not(:disabled),[data-ed-up="${i+1}"]`);return}
 if(b.dataset.edDel){st.splice(+b.dataset.edDel,1);edDraw();edFocus('[data-ed-add],[data-ed-stage]');return}
 if(b.hasAttribute('data-ed-add')){st.push({name:''});edDraw();edFocus(`[data-ed-stage="${st.length-1}"]`);return}
 if(b.dataset.edDrop){ed.projects=ed.projects.filter(p=>p.id!==b.dataset.edDrop);edDraw();edFocus('[name="add"]');return}
 if(b.hasAttribute('data-ed-delete')){if(!ed.sure){ed.sure=true;edDraw();edFocus('[data-ed-delete]');return}
  try{const r=await graphPost('board_delete',{board_id:ed.id});$('#board-dialog').close();boardShown='';sideStore.set('board-shown','');toast(r.projects===1?t('Deleted {}. Its project stays.',r.deleted):t('Deleted {}. Its {} projects stay.',r.deleted,r.projects));await people('',true)}catch(err){errCaught(err);toast(err.message,true)}}});
$('#board-form').addEventListener('submit',async e=>{e.preventDefault();if(!ed)return;edSync();const err=$('#board-form [data-ed-error]'),say=t=>{err.textContent=t;err.hidden=false};
 const stages=ed.stages.map(x=>({...x,name:x.name.trim()})).filter(x=>x.name);if(!ed.name.trim())return say('Give the board a name.');if(!stages.length)return say('Add a stage.');
 if(new Set(stages.map(x=>x.name.toLowerCase())).size<stages.length)return say('Each stage needs its own name.');
 const chosen=ed.visibility==='people'?edChosen(ed).map(p=>({fleet:p.fleet,member:p.member})):[];if(ed.visibility==='people'&&!chosen.length)return say('Choose who gets it.');
 const btn=e.submitter||$('#board-form button.primary');btn.disabled=true;
 try{if(ed.was&&ed.visibility!=='people')await graphPost('graph_board_share',{board_id:ed.id,people:[]});  /* taken back from their Machines first */
  const r=await boardSave({...(ed.id?{board_id:ed.id}:{}),...(ed.suggestion?{suggestion_id:ed.suggestion}:{}),name:ed.name.trim(),stages,side:ed.side,about:ed.about.trim(),visibility:ed.visibility==='people'?(ed.was?'people':'only_you'):ed.visibility,projects:ed.projects.map(p=>p.id)});
  if(!ed.id){ed.id=r.board_id;delete ed.suggestion}  /* saved: a retry after a failed share edits it, never makes a second one */
  if(chosen.length){await graphPost('graph_board_share',{board_id:r.board_id,people:chosen});await people('',true)}
  $('#board-dialog').close()}catch(x){errCaught(x);say(x.message)}finally{btn.disabled=false}});
$('#board-dialog').addEventListener('close',e=>{if(!e.currentTarget.open)ed=null});
$('#people-view').addEventListener('click',async e=>{const t=e.target.closest('[data-suggest-save],[data-suggest-edit],[data-suggest-dismiss],[data-board-new],[data-board-edit],[data-board-share]');if(!t)return;e.stopPropagation();
 t.closest('details')?.removeAttribute('open');const s=graphSuggest.find(x=>String(x.id)===t.closest('[data-suggest]')?.dataset.suggest);
 try{if(t.hasAttribute('data-board-new'))edOpen();else if(t.dataset.boardEdit)edOpen({board:graphBoards.find(b=>String(b.id)===t.dataset.boardEdit)});
  else if(t.dataset.boardShare)boardShareOpen(graphBoards.find(b=>String(b.id)===t.dataset.boardShare));
  else if(t.hasAttribute('data-suggest-edit'))edOpen({suggestion:s});
  else if(t.hasAttribute('data-suggest-save')){t.disabled=true;await boardSave({suggestion_id:s.id,name:s.name,stages:s.stages,side:true,about:s.about||'',projects:s.projects.map(p=>p.id),visibility:s.visibility||'team'})}
  else if(t.hasAttribute('data-suggest-dismiss')){await graphPost('board_dismiss',{suggestion_id:s.id});toast('Not now. It won’t be suggested again.');await people('',true)}}catch(err){errCaught(err);t.disabled=false;toast(err.message,true)}},true);
document.addEventListener('click',e=>{for(const m of document.querySelectorAll('.tile-menu[open],.board-menu[open]'))if(!m.contains(e.target))m.open=false});
{let dragged='';const view=$('#people-view'),laneOf=e=>e.target.closest?.('.proj-board .lane');
 view.addEventListener('dragstart',e=>{const t=e.target.closest?.('.tile');if(!t)return;dragged=t.dataset.node;e.dataTransfer.effectAllowed='move';e.dataTransfer.setData('text/plain',dragged);t.classList.add('dragging')});
 view.addEventListener('dragend',()=>{dragged='';view.querySelectorAll('.tile.dragging,.lane.drop').forEach(x=>x.classList.remove('dragging','drop'))});
 view.addEventListener('dragover',e=>{const l=laneOf(e);if(!l||!dragged)return;e.preventDefault();e.dataTransfer.dropEffect='move';view.querySelectorAll('.lane.drop').forEach(x=>x!==l&&x.classList.remove('drop'));l.classList.add('drop')});
 view.addEventListener('dragleave',e=>{const l=laneOf(e);if(l&&!l.contains(e.relatedTarget))l.classList.remove('drop')});
 view.addEventListener('drop',e=>{const l=laneOf(e);if(!l||!dragged)return;e.preventDefault();const node=dragged;dragged='';l.classList.remove('drop');boardMove(node,l.dataset.lane)})}
// Projects by hand, like a deal in any CRM: make one (from the board, a stage, a person or an organization), edit its
// name, board and stage, organization, value, people and notes, mark it Won or Lost with why, archive or delete it.
// A move by hand stands until a newer message moves it. Reviews also add projects that fit a board; the ones they're
// unsure about wait under the board header ("2 projects could belong here") for Add or Leave out.
let graphMineBoards=null,graphPeopleNames=[],pj=null;
const projActions=c=>`<span class="org-actions"><button class="ghost" data-proj-edit="${esc(c.node_id)}">Edit</button><details class="fact-menu"><summary aria-label="More for this project" title="More">⋯</summary><div class="fact-menu-list" role="menu"><button type="button" role="menuitem" data-card-here>New to-do</button>`
 +(c.outcome?`<button type="button" role="menuitem" data-proj-reopen="${esc(c.node_id)}">Reopen</button>`:`<button type="button" role="menuitem" data-proj-outcome="won" data-proj-node="${esc(c.node_id)}">Won</button><button type="button" role="menuitem" data-proj-outcome="lost" data-proj-node="${esc(c.node_id)}">Lost</button>`)
 +`<button type="button" role="menuitem" data-proj-archive="${esc(c.node_id)}"${c.archived?' data-restore':''}>${c.archived?'Restore':'Archive'}</button><button type="button" role="menuitem" class="danger" data-proj-delete="${esc(c.node_id)}">Delete…</button></div></details></span>`;
const orgLink=o=>o?.id?`<button type="button" class="inline-node" data-node="${esc(o.id)}" title="${esc(o.name)}">${esc(o.name)}</button>`:esc(o?.name||'');
const projFacts=n=>{const c=n.project;if(!c)return '';const o=c.org_node||(c.org?{name:c.org}:null),bits=[c.value!=null?t('Value {}',moneyFull(c.value)):'',c.close_date?t('Expected close {}',closeDay(c.close_date)):''].filter(Boolean);
 return `<div class="proj-facts">${c.archived?'<p class="muted">Archived</p>':''}${c.outcome?`<p><b>${c.outcome==='won'?'Won':'Lost'}</b>${c.outcome_reason?': '+esc(c.outcome_reason):''}</p>`:''}${o?`<p class="proj-org">${orgPic({name:o.name,profile:{logo:o.logo}})}${orgLink(o)}</p>`:''}${bits.length?`<p class="detail-sub">${esc(bits.join(' · '))}</p>`:''}${c.notes?`<p class="proj-notes">${esc(c.notes)}</p>`:''}${n.board?'':`<p><button type="button" class="link" data-proj-edit="${esc(c.node_id)}">Put it on a board</button></p>`}${graphOwners.length&&!n.team_only?ownerRow(n):''}</div>`};
async function pjData(){if(graphMineBoards)return;const g=await request('api/graph');graphMineBoards=(g.boards||[]).filter(b=>!b.team);graphPeopleNames=g.person_names||[]}
async function pjOpen(o={}){try{await pjData();
 if(o.node){const n=await request('api/graph?node='+encodeURIComponent(o.node)),c=n.project;if(!c)throw new Error('Couldn’t open that project.');pj={...c,people:c.people||[],mode:o.mode||'edit'}}
 else{const shown=boardNow(),here=shown&&!shown.team&&graphMineBoards.some(x=>x.id===shown.id)?shown.id:graphMineBoards[0]?.id;
  pj={node_id:'',name:'',board_id:o.board??here??null,stage:o.stage||'',org_node:o.org||null,orgSet:!!o.org,value:null,close_date:'',notes:'',people:o.person?[o.person]:[],mode:'new',from:o.from||''}}
 pj.orgq='';pj.orgHits=[];
 pjDraw();const d=$('#project-dialog');if(!d.open)d.showModal();pjFocus(pj.mode==='won'||pj.mode==='lost'?'[name="reason"]':pj.mode==='delete'?'[data-pj-delete]':'[name="name"]')}catch(err){errCaught(err);toast(err.message,true)}}
// A project's organization: one from the Graph (search as you type) or a new one, like the people on it. "From its
// people" says the Machine set it; the owner's pick stays.
const pjOrgField=p=>{const o=p.org_node,q=(p.orgq||'').trim(),exact=(p.orgHits||[]).some(x=>x.name.toLowerCase()===q.toLowerCase());
 return `<fieldset class="ed-projects ed-org"><legend>Organization</legend>`+(o?`<ul><li><span title="${esc(o.name)}">${esc(o.name)}</span>${!p.orgSet&&['auto','backfill','review'].includes(o.by)?'<small class="muted">From its people</small>':''}<button type="button" class="icon" data-pj-org-drop aria-label="Take ${esc(o.name)} off">×</button></li></ul>`
  :`<input name="orgq" value="${esc(p.orgq||'')}" list="project-dialog-orgs" placeholder="Search or add one" aria-label="Organization" autocomplete="off"><datalist id="project-dialog-orgs">${(p.orgHits||[]).map(x=>`<option value="${esc(x.name)}">${esc(x.domain||'')}</option>`).join('')}</datalist>`
  +(q&&!exact?`<button type="button" class="link pj-org-new" data-pj-org-new>Add “${esc(q)}” as new</button>`:''))+'</fieldset>'};
async function pjOrgFind(q){const seq=pjOrgFind.seq=(pjOrgFind.seq||0)+1;let hits=[];
 if(q.length>=2){try{const r=await request('api/graph?q='+encodeURIComponent(q));hits=(r.found||[]).filter(n=>n.kind==='org').slice(0,8).map(n=>({id:n.id,name:n.name,domain:n.domain||''}))}catch{}}
 if(seq!==pjOrgFind.seq||!pj||pj.org_node)return;pj.orgHits=hits;const f=$('#project-form'),i=f.elements.orgq;if(!i)return;
 f.querySelector('#project-dialog-orgs').innerHTML=hits.map(x=>`<option value="${esc(x.name)}">${esc(x.domain)}</option>`).join('');pjOrgNew()}
const pjOrgNew=()=>{const f=$('#project-form'),i=f.elements.orgq;if(!i||!pj)return;const q=i.value.trim(),exact=pj.orgHits.some(x=>x.name.toLowerCase()===q.toLowerCase());let b=f.querySelector('[data-pj-org-new]');
 if(!q||exact){b?.remove();return}if(!b){b=document.createElement('button');b.type='button';b.className='link pj-org-new';b.dataset.pjOrgNew='';i.closest('fieldset').append(b)}b.textContent=`Add “${q}” as new`};
const pjOrgPick=o=>{pjSync();pj.org_node=o;pj.orgSet=true;pj.orgq='';pj.orgHits=[];pjDraw()};
const pjFocus=sel=>$('#project-form').querySelector(sel)?.focus();  /* at once: a later focus would take the field the owner went on to */
const pjHead=t=>`<div class="snooze-heading"><h2 id="project-dialog-title">${esc(t)}</h2><button type="button" data-pj-close aria-label="Close">×</button></div>`;
const pjErr='<p class="ed-note warn" data-pj-error role="alert" hidden></p>';
function pjDraw(){const p=pj,f=$('#project-form'),boards=graphMineBoards||[],b=boards.find(x=>String(x.id)===String(p.board_id));
 if(p.mode==='won'||p.mode==='lost'){const won=p.mode==='won';
  f.innerHTML=pjHead(won?'Won':'Lost')+`<p class="ed-note">${esc(won?(b?t('{} moves to {}',p.name,b.stages.filter(s=>!s.side).at(-1)?.name||''):p.name):b&&!b.side?p.name:t('{} moves to Stalled or declined',p.name))}</p><label class="ed-field">${won?'Why it was won':'Why it was lost'}<input name="reason" maxlength="160" placeholder="${won?'e.g. Signed the yearly plan':'e.g. Chose another tool'}" autocomplete="off"></label>`
   +pjErr+`<div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-pj-close>Cancel</button><button class="primary">${won?'Mark won':'Mark lost'}</button></div>`;return}
 if(p.mode==='delete'){f.innerHTML=pjHead('Delete project')+`<p>${esc(p.name)} goes for good, with its moves. Its messages and people stay.</p>`+pjErr+`<div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-pj-close>Cancel</button><button type="button" class="primary danger" data-pj-delete>Delete</button></div>`;return}
 const picked=new Set(p.people.map(x=>x.id)),pick=graphPeopleNames.filter(x=>!picked.has(x.id));
 f.innerHTML=pjHead(p.node_id?'Edit project':'New project')
  +`<label class="ed-field">Name<input name="name" maxlength="60" value="${esc(p.name)}" placeholder="e.g. Acme rollout" autocomplete="off"></label>`+(p.node_id?'':'<div class="ed-dupes" data-rec-dupes role="status" hidden></div>')
  +`<div class="ed-row"><label class="ed-field">Board<select name="board"><option value="">No board</option>${boards.map(x=>`<option value="${x.id}"${String(x.id)===String(p.board_id)?' selected':''}>${esc(x.name)}</option>`).join('')}</select></label>`
  +(b?`<label class="ed-field">Stage<select name="stage">${b.stages.map(s=>`<option${s.name===p.stage?' selected':''}>${esc(s.name)}</option>`).join('')}</select></label>`:'<span></span>')+'</div>'
  +pjOrgField(p)
  +`<div class="ed-row"><label class="ed-field">Value<input name="value" value="${p.value??''}" placeholder="e.g. 12000" autocomplete="off" inputmode="decimal"></label><label class="ed-field">Expected close<input name="close_date" type="date" value="${esc(p.close_date||'')}"></label></div>`
  +`<fieldset class="ed-projects"><legend>People</legend><ul>${p.people.map(x=>`<li><span title="${esc(x.name)}">${esc(x.name)}</span><button type="button" class="icon" data-pj-drop="${esc(x.id)}" aria-label="Take ${esc(x.name)} off">×</button></li>`).join('')}</ul>`
  +`<input name="person" list="project-dialog-people" placeholder="Add a person" aria-label="Add a person" autocomplete="off"><datalist id="project-dialog-people">${pick.slice(0,1500).map(x=>`<option value="${esc(x.name)}"></option>`).join('')}</datalist></fieldset>`
  +`<label class="ed-field">Notes<textarea name="notes" rows="3" maxlength="4000">${esc(p.notes||'')}</textarea></label>`
  +(p.node_id?`<div class="pj-end" role="group" aria-label="End it">${p.outcome?`<button type="button" class="ghost" data-pj-reopen>Reopen</button>`:'<button type="button" class="ghost" data-pj-outcome="won">Won</button><button type="button" class="ghost" data-pj-outcome="lost">Lost</button>'}<button type="button" class="ghost" data-pj-archive>${p.archived?'Restore':'Archive'}</button><button type="button" class="ghost danger" data-pj-ask-delete>Delete…</button></div>`:'')
  +(p.node_id?'':'<p class="ed-note">A move by hand stands until a newer message moves it.</p>')
  +pjErr+`<div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-pj-close>Cancel</button><button class="primary">${p.node_id?'Save':'Add project'}</button></div>`}
const pjSync=()=>{const f=$('#project-form').elements;if(!pj||!f.name)return;pj.name=f.name.value;if(f.orgq)pj.orgq=f.orgq.value;pj.value=f.value.value;pj.close_date=f.close_date.value;pj.notes=f.notes.value;if(f.stage)pj.stage=f.stage.value};
async function pjDone(r,say){$('#project-dialog').close();graphMineBoards=null;toast(say);
 if(graphNode&&r?.deleted){graphNode='';history.replaceState(null,'','#graph=projects');await people('');return}
 await people(graphNode,true);if(!graphNode)boardRedraw()}
async function pjEnd(node,outcome,reason){const r=await graphPost('project_outcome',{node_id:node,outcome,reason});return r}
async function pjArchive(node,archived){const r=await graphPost('project_archive',{node_id:node,archived});toast(archived?'Archived. A new message about it brings it back.':'Restored.');graphMineBoards=null;await people(graphNode,true);return r}
$('#project-form').addEventListener('change',e=>{if(!pj)return;const t=e.target;
 if(t.name==='board'){pjSync();pj.board_id=t.value?+t.value:null;const b=(graphMineBoards||[]).find(x=>x.id===pj.board_id);pj.stage=b?.stages[0]?.name||'';pjDraw();pjFocus('[name="board"]')}});
$('#project-form').addEventListener('input',e=>{if(pj&&e.target.name==='orgq'){const q=e.target.value.trim(),x=pj.orgHits.find(x=>x.name.toLowerCase()===q.toLowerCase());
  if(x&&e.inputType!=='insertText'){pjOrgPick(x);pjFocus('[data-pj-org-drop]');return}pjOrgNew();clearTimeout(pjOrgFind.t);pjOrgFind.t=setTimeout(()=>pjOrgFind(q),200);return}
 if(pj&&!pj.node_id&&e.target.name==='name')recDupesSoon($('#project-form'),'project');if(!pj||e.target.name!=='person')return;const v=e.target.value.trim().toLowerCase(),x=graphPeopleNames.find(x=>x.name.toLowerCase()===v);
 if(x&&!pj.people.some(y=>y.id===x.id)){pjSync();pj.people.push({id:x.id,name:x.name});pjDraw();pjFocus('[name="person"]')}});
$('#project-form').addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.name==='person')e.preventDefault();
 if(e.key==='Enter'&&e.target.name==='orgq'&&pj){e.preventDefault();const q=e.target.value.trim(),x=pj.orgHits.find(x=>x.name.toLowerCase()===q.toLowerCase())||(pj.orgHits.length===1?pj.orgHits[0]:null);if(x){pjOrgPick(x);pjFocus('[data-pj-org-drop]')}}});
$('#project-form').addEventListener('click',async e=>{const b=e.target.closest('button');if(!b||!pj)return;pjSync();
 const err=$('#project-form [data-pj-error]'),say=t=>{if(err){err.textContent=t;err.hidden=false}};
 try{if(b.hasAttribute('data-pj-close')){$('#project-dialog').close();return}
  if(b.dataset.pjDrop){pj.people=pj.people.filter(x=>x.id!==b.dataset.pjDrop);pjDraw();pjFocus('[name="person"]');return}
  if(b.hasAttribute('data-pj-org-drop')){pj.org_node=null;pj.orgSet=true;pj.orgHits=[];pjDraw();pjFocus('[name="orgq"]');return}
  if(b.hasAttribute('data-pj-org-new')){const q=(pj.orgq||'').trim(),site=/^[^\s@]+\.[a-z]{2,}$/i.test(q)?q:'';if(!q)return;b.disabled=true;
   const r=await graphPost('graph_new',{kind:'org',name:site?cap(site.replace(/^(https?:\/\/)?(www\.)?/i,'').split('.')[0]):q,website:site});graphMineBoards=null;pjOrgPick({id:r.node_id,name:r.name});pjFocus('[data-pj-org-drop]');return}
  if(b.dataset.pjOutcome){pj.mode=b.dataset.pjOutcome;pjDraw();pjFocus('[name="reason"]');return}
  if(b.hasAttribute('data-pj-ask-delete')){pj.mode='delete';pjDraw();pjFocus('[data-pj-delete]');return}
  if(b.hasAttribute('data-pj-reopen')){await pjEnd(pj.node_id,null,'');pjDone(null,'Reopened.');return}
  if(b.hasAttribute('data-pj-archive')){const was=pj.archived;$('#project-dialog').close();await pjArchive(pj.node_id,!was);return}
  if(b.hasAttribute('data-pj-delete')){b.disabled=true;const r=await graphPost('project_delete',{node_id:pj.node_id});pjDone(r,`Deleted ${r.deleted}.`)}}catch(x){errCaught(x);b.disabled=false;say(x.message)}});
$('#project-form').addEventListener('submit',async e=>{e.preventDefault();if(!pj)return;const err=$('#project-form [data-pj-error]'),say=t=>{err.textContent=t;err.hidden=false};
 const btn=e.submitter||$('#project-form button.primary');btn.disabled=true;
 try{if(pj.mode==='won'||pj.mode==='lost'){const reason=$('#project-form').elements.reason.value.trim(),r=await pjEnd(pj.node_id,pj.mode,reason);pjDone(r,pj.mode==='won'?'Marked won.':'Marked lost.');return}
  pjSync();if(!pj.name.trim())return say('Give the project a name.');
  const r=await graphPost('project_save',{...(pj.node_id?{node_id:pj.node_id}:{}),name:pj.name.trim(),board_id:pj.board_id||null,stage:pj.board_id?pj.stage:'',...(pj.orgSet?{org:pj.org_node?.id||''}:{}),value:String(pj.value??'').trim(),close_date:pj.close_date||'',notes:pj.notes,people:pj.people.map(x=>x.id)});
  if(r.created&&pj.board_id){const b=(graphMineBoards||[]).find(x=>x.id===pj.board_id);if(b){boardShown=b.name;sideStore.set('board-shown',b.name)}}
  if(r.created&&pj.from!=='board'){$('#project-dialog').close();graphMineBoards=null;toast(`Added ${r.name}.`);return recShow(r.node_id)}
  pjDone(r,r.created?`Added ${r.name}.`:'Saved.')}catch(x){errCaught(x);say(x.message)}finally{btn.disabled=false}});
$('#project-dialog').addEventListener('close',e=>{if(!e.currentTarget.open)pj=null});
// New person and New organization: a short form (a name; for a person their email and organization, for an
// organization its website). Ones already in the Graph that look like what is typed show as "Already in your Graph?",
// each a link that opens it; the Machine also hands back the one there for the same address or website. Saving opens
// the new page. "Same person as…" on a person's page uses the same dialog to merge two people.
let rec=null;
const REC={person:{title:'New person',add:'Add person',fields:[['name','Name','e.g. Ada Lovelace'],['email','Email','ada@example.com'],['org','Organization','e.g. Acme']]},
 org:{title:'New organization',add:'Add organization',fields:[['name','Name','e.g. Acme'],['website','Website','acme.com']]},
 same:{title:'Same person as…',add:'Merge',fields:[['name','Who else is it?','A name from your Graph']]}};
async function recOpen(kind,o={}){const d=$('#record-dialog'),f=$('#record-form'),r=REC[kind];if(!r)return;rec={kind,seq:0,...o};
 if(kind==='same'){try{await pjData()}catch{}}
 f.innerHTML=`<div class="snooze-heading"><h2 id="record-dialog-title">${esc(r.title)}</h2><button type="button" data-rec-close aria-label="Close">×</button></div>`
  +(kind==='same'?`<p class="ed-note">${esc(o.name||'')} and the person you pick become one, with all their messages. Undo is under Joined on the page.</p>`:'')
  +r.fields.map(([k,label,ph],i)=>`<label class="ed-field">${esc(label)}${i?' <span class="muted">(optional)</span>':''}<input name="${k}" placeholder="${esc(ph)}" autocomplete="off"${k==='email'?' type="email" inputmode="email"':k==='website'?' inputmode="url"':''}${i?'':' maxlength="100"'}${kind==='same'?' list="record-dialog-people"':''}></label>`).join('')
  +(kind==='same'?`<datalist id="record-dialog-people">${graphPeopleNames.filter(x=>x.id!==o.id).slice(0,1500).map(x=>`<option value="${esc(x.name)}"></option>`).join('')}</datalist>`:'')
  +`<div class="ed-dupes" data-rec-dupes role="status" hidden></div><p class="ed-note warn" data-rec-error role="alert" hidden></p><div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-rec-close>Cancel</button><button class="primary">${esc(r.add)}</button></div>`;
 if(!d.open)d.showModal();f.elements.name.focus()}
// Open a page in the Graph from anywhere (a dialog, the "+" menu on another tab)
const recShow=id=>{if($('#people').hidden)location.hash=graphHash(id);else graphOpen(id)};
const DUPE_KIND={person:'person',org:'org',project:'project'};
function recDupesSoon(f,kind){clearTimeout(recDupesSoon.t);recDupesSoon.t=setTimeout(()=>recDupes(f,kind),250)}
async function recDupes(f,kind){const box=f.querySelector('[data-rec-dupes]');if(!box||!DUPE_KIND[kind])return;const seq=recDupes.seq=(recDupes.seq||0)+1;
 const asks=[f.elements.email?.value,f.elements.website?.value,f.elements.name?.value].map(v=>String(v||'').trim()).filter(v=>v.length>=3);let hits=[];
 for(const q of asks){try{const r=await request('api/graph?q='+encodeURIComponent(q));hits.push(...(r.found||[]).filter(n=>n.kind===DUPE_KIND[kind]||kind==='person'&&n.kind==='me'&&q.includes('@')))}catch{}}
 if(seq!==recDupes.seq||!box.isConnected)return;hits=[...new Map(hits.map(n=>[n.id,n])).values()].slice(0,3);
 const sub=n=>n.kind==='person'?((n.ids||[]).find(i=>i.startsWith('email:'))||'').slice(6):n.kind==='org'?n.domain||'':n.state||'';
 box.innerHTML=hits.some(n=>n.kind==='me')?'<p>That’s your own address.</p><button type="button" class="link" data-rec-open="me">About you</button>':hits.length?`<p>Already in your Graph?</p>${hits.map(n=>`<button type="button" class="link" data-rec-open="${esc(n.id)}">${esc(n.name)}${sub(n)?`<small>${esc(sub(n))}</small>`:''}</button>`).join('')}`:'';box.hidden=!hits.length}
$('#record-form').addEventListener('input',e=>{const er=e.currentTarget.querySelector('[data-rec-error]');if(er)er.hidden=true;if(rec&&rec.kind!=='same'&&['name','email','website'].includes(e.target.name))recDupesSoon($('#record-form'),rec.kind)});
for(const id of ['#record-form','#project-form'])$(id).addEventListener('click',e=>{const o=e.target.closest('[data-rec-open]');if(!o)return;e.preventDefault();e.target.closest('dialog').close();recShow(o.dataset.recOpen)});
$('#record-form').addEventListener('click',e=>{if(e.target.closest('[data-rec-close]'))$('#record-dialog').close()});
$('#record-form').addEventListener('submit',async e=>{e.preventDefault();if(!rec)return;const f=e.target,err=f.querySelector('[data-rec-error]'),say=t=>{err.textContent=t;err.hidden=false},btn=f.querySelector('button.primary');
 const v=k=>String(f.elements[k]?.value||'').trim();if(!v('name'))return say(rec.kind==='same'?'Pick someone from the list.':'Give them a name.');
 btn.disabled=true;err.hidden=true;
 try{if(rec.kind==='same'){const other=graphPeopleNames.find(x=>x.name.toLowerCase()===v('name').toLowerCase()&&x.id!==rec.id);if(!other)return say('Pick someone from the list.');
   await graphPost('graph_same',{a:rec.id,b:other.id,same:true});$('#record-dialog').close();toast('Merged.');graphMineBoards=null;return people(graphNode,true)}
  const r=await graphPost('graph_new',{kind:rec.kind,...Object.fromEntries(REC[rec.kind].fields.map(([k])=>[k,v(k)]))});
  $('#record-dialog').close();graphMineBoards=null;toast(r.yours?'That’s your own address. It’s in About you.':r.existing?`${r.name} is in your Graph already.`:`Added ${r.name}.`);recShow(r.node_id)}
 catch(x){errCaught(x);say(x.message)}finally{btn.disabled=false}});
$('#record-dialog').addEventListener('close',e=>{if(!e.currentTarget.open)rec=null});  // a close event comes later: the dialog may be open again by then
// New person, organization or project from a Graph page's head; New card, Same person as… and Delete on a page
document.addEventListener('click',async e=>{const n=e.target.closest('[data-graph-new]');if(n){e.preventDefault();return n.dataset.graphNew==='project'?pjOpen({}):recOpen(n.dataset.graphNew)}
 const t=e.target.closest('[data-card-here],[data-same-as],[data-org-delete]');if(!t||!t.closest('#people-view'))return;e.preventDefault();t.closest('details')?.removeAttribute('open');
 const name=$('#people-view .graph-detail>.name-row h3')?.textContent||'';
 if(t.hasAttribute('data-card-here'))return ncOpen({about:[{id:graphNode,name}]});
 if(t.hasAttribute('data-same-as'))return recOpen('same',{id:graphNode,name});
 if(!confirm(`Delete ${name}? Its notes and details go too.`))return;t.disabled=true;
 try{await graphPost('graph_org_delete',{node_id:graphNode});toast(`Deleted ${name}.`);graphBack('orgs')}catch(err){errCaught(err);t.disabled=false;toast(err.message,true)}});
// Everywhere a project can be made or changed: the board, a lane's + Add, a tile's ⋯, the list, a project's page, a person or organization
document.addEventListener('click',async e=>{const t=e.target.closest('[data-proj-new],[data-proj-new-here],[data-proj-edit],[data-proj-outcome],[data-proj-archive],[data-proj-reopen],[data-proj-delete],[data-board-default],[data-fit-add],[data-fit-skip],[data-fit-bulk]');
 if(!t||!t.closest('#people-view,#page-head'))return;e.stopPropagation();e.preventDefault();t.closest('details:not(.board-fits)')?.removeAttribute('open');  // a menu closes; the review list stays open
 try{if(t.hasAttribute('data-proj-new'))return pjOpen({stage:t.dataset.projStage||'',from:t.closest('.proj-board')?'board':''});
  if(t.hasAttribute('data-proj-new-here')){const n=graphNode||'',name=$('#people-view .person-head h3')?.textContent||'';return pjOpen(n.startsWith('org:')?{org:{id:n,name}}:{person:{id:n,name}})}
  if(t.dataset.projEdit)return pjOpen({node:t.dataset.projEdit});
  if(t.dataset.projOutcome)return pjOpen({node:t.dataset.projNode,mode:t.dataset.projOutcome});
  if(t.dataset.projDelete)return pjOpen({node:t.dataset.projDelete,mode:'delete'});
  if(t.dataset.projReopen){await pjEnd(t.dataset.projReopen,null,'');toast('Reopened.');return people(graphNode,true)}
  if(t.dataset.projArchive)return pjArchive(t.dataset.projArchive,!t.hasAttribute('data-restore'));
  if(t.dataset.boardDefault){await graphPost('board_default',{board_id:+t.dataset.boardDefault});toast('Projects opens on this board now.');return people('',true)}
  if(t.dataset.fitAdd||t.dataset.fitSkip)return fitsDecide(t,+t.dataset.fitBoard,[t.dataset.fitAdd||t.dataset.fitSkip],!!t.dataset.fitAdd);
  if(t.dataset.fitBulk){const box=t.closest('.board-fits'),b=+t.dataset.fitBoard,picked=fitsPicked.get(b),ids=picked?.size?[...picked]:[...box.querySelectorAll('[data-fit-add]')].map(x=>x.dataset.fitAdd);if(ids.length)return fitsDecide(t,b,ids,t.dataset.fitBulk==='add')}}
 catch(err){errCaught(err);t.disabled=false;toast(err.message,true)}},true);
// A tile from the keyboard: Enter opens it, E edits it
$('#people-view').addEventListener('keydown',e=>{const t=e.target.closest?.('.proj-board .tile:not(.team)');if(t&&e.target===t&&(e.key==='e'||e.key==='E')&&!e.metaKey&&!e.ctrlKey&&!e.altKey){e.preventDefault();pjOpen({node:t.dataset.node})}});
// A project's page: its board and stage, its next step, and the latest moves with the message each came from.
const stageBox=n=>{const b=n.board;if(!b)return '';const moves=(b.moves||[]).map(m=>`<li>${esc(shortDay(m.at))} · ${m.source==='owner'?`Moved to ${esc(m.stage)} by hand`:`${esc(m.stage)}: ${esc(m.source==='follow_up'?fuMoveReason(m,n):m.reason||'')}`}${m.event_id?` <button type="button" class="link" data-quote-event="${m.event_id}">Read</button>`:''}</li>`).join('');
 const seen=n.team_only?'':`<label class="seen-pick">Who sees it<select data-project-seen="${esc(n.id)}"><option value=""${b.visibility?'':' selected'}>Like its board (${b.board_visibility==='only_you'?'only you':b.board_visibility==='people'?'chosen teammates':'team'})</option><option value="only_you"${b.visibility==='only_you'?' selected':''}>Only you</option><option value="team"${b.visibility==='team'?' selected':''}>Your team</option></select></label>`;
 return `<div class="graph-stage"><p><b>${esc(b.stage||'')}</b> <span class="muted">on ${esc(b.board)}</span>${['only_you','people'].includes(b.visibility||b.board_visibility)?' '+seenBy(b.visibility||b.board_visibility):''}</p>${b.next?`<p>Next: ${esc(b.next)}</p>`:''}${moves?`<ol aria-label="Moves">${moves}</ol>`:''}${n.team_only?'':fuBox(n)}${seen}</div>`};
document.addEventListener('change',async e=>{const t=e.target.closest?.('[data-project-seen]');if(!t)return;t.disabled=true;
 try{await graphPost('project_visibility',{node_id:t.dataset.projectSeen,visibility:t.value||null});toast(t.value==='only_you'?'Only you see this project now.':t.value==='team'?'Your team sees this project now.':'It follows its board now.');await people('',true)}catch(err){errCaught(err);toast(err.message,true)}finally{t.disabled=false}});
// Automated follow-ups (follow_ups.py): their settings for a board or one project (a project's own wins over its board's),
// the board's "Follow-ups on" line, a project's "Next follow-up", and a board's grouped to-do with its fast review:
// one follow-up at a time or the whole list, Send, Edit or Skip each, keys to move, Send all checked.
const FU_CHANNELS={email:'Email',linkedin:'LinkedIn',whatsapp:'WhatsApp',slack:'Slack',telegram:'Telegram',intercom:'Intercom'};
const fuDay=v=>{if(!v)return '';const d=new Date(v),n=new Date();if(d<=n||localDay(d)===localDay(n))return t('today');return (d-n)/864e5<6?d.toLocaleDateString(DL,{weekday:'short'}):d.toLocaleDateString(DL,{day:'numeric',month:'short'})};
const fuNoReply=n=>n?t(['No reply after {} follow-up','No reply after {} follow-ups'],n):t('Follow-ups stopped');
const fuTile=f=>!f?'':f.reason==='bounced'?`<p class="tile-fu quiet">${esc(t('Email bounced'))}</p>`:f.end?`<p class="tile-fu quiet">${esc(fuNoReply(f.end.n))}</p>`:f.state==='open'?`<p class="tile-fu">${esc(t('Follow-up ready'))}</p>`:['due','waiting'].includes(f.state)&&f.next_at?`<p class="tile-fu">${esc(t('Next follow-up: {}',fuDay(f.next_at)))}</p>`:'';
// On or off, the board's line says so and opens its settings; a stage with no-reply projects on a board with follow-ups off
// offers "Follow them up" (the owner's own boards only: a Team board isn't theirs to change)
const fuBoardLine=b=>b.follow_ups?` · <button type="button" class="link fu-state${b.follow_ups.on?'':' off'}" data-fu-open="board:${b.id}">${esc(!b.follow_ups.on?t('Follow-ups off'):b.follow_ups.next_at?t('Follow-ups on, next {}',fuDay(b.follow_ups.next_at)):t('Follow-ups on'))}</button>`:'';
const fuNudge=(b,s)=>b.team||!b.follow_ups||b.follow_ups.on?'':` · <button type="button" class="fu-nudge" data-fu-open="board:${b.id}" data-fu-for="${esc(s.name)}">${esc(t('Follow them up'))}</button>`;
const fuAct=a=>{const ch=FU_CHANNELS[a.channel]||a.channel;return a.why==='bounced'?t('Follow-up {} bounced',a.n):a.state==='sent'?(a.auto?t('Follow-up {} sent automatically ({})',a.n,ch):t('Follow-up {} sent ({})',a.n,ch)):a.state==='open'?t('Follow-up {} ready to review',a.n):a.state==='skipped'?t('Follow-up {} skipped',a.n):a.why==='owner'?t('Follow-ups stopped at follow-up {}',a.n):a.why==='replied'?t('They replied before follow-up {}',a.n):t('Follow-up {} not needed',a.n)};
const fuBox=n=>{const f=n.follow_up;if(!f)return '';const end=f.ends?.[0];
 const line=f.reason==='bounced'?t('Email bounced'):!f.on?t('Follow-ups off'):f.state==='open'?t('Follow-up ready'):f.next_at?t('Next follow-up: {}',fuDay(f.next_at)):end&&f.state==='stopped'?fuNoReply(end.n):t('Follow-ups on');
 const acts=(f.activity||[]).slice(0,4).map(a=>`<li>${esc(shortDay(a.closed_at||a.created_at))} · ${esc(fuAct(a))}${a.back?` · <button type="button" class="link" data-fu-back="${esc(a.back)}">${esc(t('Bring back'))}</button>`:''}</li>`).join('');
 return `<div class="graph-fu"><p><span>${esc(line)}</span> <button type="button" class="link" data-fu-open="${esc(n.id)}">${esc(t('Follow-ups…'))}</button></p>${acts?`<ol aria-label="${esc(t('Follow-ups'))}">${acts}</ol>`:''}</div>`};
const fuMoveReason=(m,n)=>{const end=(n.follow_up?.ends||[]).find(e=>String(e.at).slice(0,16)===String(m.at).slice(0,16));return end?fuNoReply(end.n):m.reason||''};
let fu=null;
// From a stage's "Follow them up": on is ticked, and that stage too when it isn't on already (nothing is saved before Save)
async function fuOpen(ref,stage){const i=ref.indexOf(':'),scope=ref.slice(0,i),id=ref.slice(i+1);
 try{const r=await graphPost('follow_up_settings',{scope,id});fu={...r,s:{...r.settings,stages:{...(r.settings.stages||{})}},custom:Object.keys(r.settings.stages||{}).length>0,mode:r.scope==='project'?(r.own?(r.settings.on?'on':'off'):r.board?'board':'off'):''};
  const st=stage&&scope==='board'&&fu.stages?.find(x=>x.name===stage);if(stage&&scope==='board'){fu.s.on=true;if(st&&!(fu.s.stages[st.name]?.on??st.open)){fu.custom=true;fu.s.stages[st.name]={...fu.s.stages[st.name],on:true}}}
  fuDraw();const d=$('#fu-dialog');if(!d.open)d.showModal();d.querySelector('input:not(:disabled)')?.focus()}catch(e){errCaught(e);toast(e.message,true)}}
function fuDraw(){const f=$('#fu-form'),s=fu.s,proj=fu.scope==='project',on=proj?fu.mode==='on':s.on,stagesOn=fu.stages?.filter(x=>(s.stages[x.name]?.on??x.open)).length;
 const num=(name,v,min,max,label)=>`<input type="number" inputmode="numeric" name="${name}" value="${esc(v)}" min="${min}" max="${max}" aria-label="${esc(label)}">`;
 const radio=(name,v,cur,label)=>`<label class="fu-radio"><input type="radio" name="${name}" value="${v}"${cur===v?' checked':''}> ${esc(label)}</label>`;
 const top=proj?`<fieldset class="fu-mode"><legend>${esc(t('For this project'))}</legend>${fu.board?radio('mode','board',fu.mode,fu.board.on?t('Like its board (on)'):t('Like its board (off)')):''}${radio('mode','on',fu.mode,t('On'))}${radio('mode','off',fu.mode,t('Off'))}</fieldset>`
  :`<label class="fu-chk fu-main"><input type="checkbox" name="on"${s.on?' checked':''}> ${esc(t('Follow up when there’s no reply'))}</label>`;
 const stages=!proj&&fu.stages?.length?`<div class="fu-line"><span>${esc(t('Stages'))}</span><span class="muted">${esc(fu.custom?t(['{} stage on','{} stages on'],stagesOn):t('All open stages'))}</span>${fu.custom?'':`<button type="button" class="link" data-fu-custom>${esc(t('Customize'))}</button>`}</div>`
  +(fu.custom?`<ul class="fu-stages">${fu.stages.map((x,i)=>`<li><label class="fu-chk"><input type="checkbox" data-fu-stage="${i}"${s.stages[x.name]?.on??x.open?' checked':''}> <span title="${esc(x.name)}">${esc(x.name)}</span></label><input type="number" inputmode="numeric" data-fu-sdays="${i}" min="1" max="60" value="${esc(s.stages[x.name]?.days??'')}" placeholder="${esc(s.days)}" aria-label="${esc(t('Days to wait in {}',x.name))}"></li>`).join('')}</ul><p class="fu-note">${esc(t('Days to wait per stage; empty uses the shortest wait.'))}</p>`:''):'';
 const allowed=c=>!s.channels||s.channels.includes(c);
 const channels=fu.channels.length?`<fieldset class="fu-ch"><legend>${esc(t('Channels'))}</legend>${fu.channels.map(c=>`<label class="fu-chk"><input type="checkbox" name="ch" value="${c}"${allowed(c)?' checked':''}> ${esc(FU_CHANNELS[c])}</label>`).join('')}<p class="fu-note">${esc(t('Same channel as the last message.'))}</p>${fu.channels.length>1?`<label class="fu-chk"><input type="checkbox" name="switch"${s.switch?' checked':''}> ${esc(t('Switch channel if there’s no reply'))}</label>`:''}</fieldset>`
  :`<p class="fu-note warn">${esc(t('Connect a channel that can send first.'))}</p>`;
 const stall=fu.stalled?`<label class="fu-chk"><input type="checkbox" name="stall"${s.stall!==false?' checked':''}> ${esc(t('Move to Stalled or declined after the last one'))}</label>`:'';
 const send=`<fieldset class="fu-send"><legend>${esc(t('Sending'))}</legend>${radio('auto','ask',s.auto&&!fu.careful?'auto':'ask',t('Ask me before sending'))}<label class="fu-radio"><input type="radio" name="auto" value="auto"${s.auto&&!fu.careful?' checked':''}${fu.careful?' disabled':''}> ${esc(t('Send without asking'))}</label>`
  +`<p class="fu-note">${esc(fu.careful?t('Careful mode is on, so it always asks.'):s.auto?t('Anything unusual still waits for you.'):t('Drafts wait in your to-dos.'))}</p></fieldset>`;
 f.innerHTML=`<div class="snooze-heading"><h2 id="fu-dialog-title">${esc(t('Follow-ups'))}</h2><button type="button" data-fu-close aria-label="${esc(t('Close'))}">×</button></div><p class="fu-for" title="${esc(fu.name)}">${esc(fu.name)}</p>${top}`
  +`<fieldset class="fu-body"${on?'':' disabled'}><p class="fu-row">${t('Wait {} to {} days without a reply',num('days',s.days,1,60,t('Shortest wait in days')),num('max_days',s.max_days,1,60,t('Longest wait in days')))}</p>`
  +`<p class="fu-row">${t('Follow up at least {} and at most {} times',num('min',s.min,0,5,t('At least')),num('max',s.max,1,5,t('At most')))}</p><p class="fu-note">${esc(t('Past the minimum, it only follows up when that still makes sense.'))}</p>`
  +stages+channels+stall+send+`</fieldset><p class="ed-note warn" data-fu-error role="alert" hidden></p><div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-fu-close>${esc(t('Cancel'))}</button><button class="primary">${esc(t('Save'))}</button></div>`}
function fuRead(){const f=$('#fu-form'),s=fu.s,n=name=>{const v=f.elements[name]?.value;return v===''||v==null?undefined:+v};
 if(fu.scope==='project'){const m=f.querySelector('[name=mode]:checked');if(m)fu.mode=m.value}else s.on=!!f.elements.on?.checked;
 for(const k of ['days','max_days','min','max']){const v=n(k);if(v!==undefined)s[k]=v}
 const ch=[...f.querySelectorAll('[name=ch]')];if(ch.length)s.channels=ch.every(x=>x.checked)?null:ch.filter(x=>x.checked).map(x=>x.value);
 if(f.elements.switch)s.switch=f.elements.switch.checked;if(f.elements.stall)s.stall=f.elements.stall.checked;
 const a=f.querySelector('[name=auto]:checked');if(a)s.auto=a.value==='auto';
 for(const x of f.querySelectorAll('[data-fu-stage]')){const st=fu.stages[+x.dataset.fuStage],d=f.querySelector(`[data-fu-sdays="${x.dataset.fuStage}"]`)?.value;s.stages[st.name]={on:x.checked,...(d?{days:+d}:{})}}}
$('#fu-form').addEventListener('change',e=>{if(!fu)return;fuRead();if(e.target.name==='mode'||e.target.name==='on'||e.target.name==='auto'||e.target.dataset.fuStage!=null)fuDraw()});
$('#fu-form').addEventListener('click',e=>{if(!fu)return;if(e.target.closest('[data-fu-close]')){$('#fu-dialog').close();return}if(e.target.closest('[data-fu-custom]')){fuRead();fu.custom=true;fuDraw();$('#fu-form [data-fu-stage]')?.focus()}});
$('#fu-form').addEventListener('submit',async e=>{e.preventDefault();if(!fu)return;fuRead();const s=fu.s,err=$('#fu-form [data-fu-error]'),btn=$('#fu-form button.primary');
 const settings=fu.scope==='project'&&fu.mode==='board'?{inherit:true}:{...s,on:fu.scope==='project'?fu.mode==='on':s.on,stages:fu.custom?s.stages:{}};
 btn.disabled=true;try{await graphPost('follow_up_save',{scope:fu.scope,id:fu.id,settings});$('#fu-dialog').close();toast(t('Follow-ups saved.'));if(!$('#people').hidden)await people(graphNode,true);refresh().catch(()=>{})}
 catch(x){errCaught(x);err.textContent=x.message;err.hidden=false}finally{btn.disabled=false}});
$('#fu-dialog').addEventListener('close',()=>{fu=null});
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-fu-open]');if(!b)return;e.preventDefault();e.stopPropagation();b.closest('details')?.removeAttribute('open');fuOpen(b.dataset.fuOpen,b.dataset.fuFor)},true);
// The board's follow-ups as one to-do: "8 follow-ups ready for <board>", in Ready once one is written, else in Preparing
// as "Follow-ups for <board>". Each is in it from the start, also alone: never a to-do of its own in any list, so a board
// with follow-ups on is one to-do to review, not one per email. While drafts are written it says "Writing 3 follow-ups…".
// One that got stuck (needs the owner's help) stays a to-do of its own. A project's own follow-up (not grouped) is a
// normal to-do. Follow-ups on their way in a batch (spaced 30-45 s per mailbox) show as one progress to-do per board
// instead (fuSendingCard).
// Queued or on its way: out of the ready to-do at once. A follow-up's draft can sit in a menu, so its own state counts too.
const fuBusy=s=>sendBusy(s.action_status)||taskActions(s).some(a=>DRAFT_KINDS.includes(a.kind)&&sendBusy(a.state));
function fuSplit(ready,needs,preparing){fuGroups.clear();const groups={},member=s=>typeof s!=='string'&&s.follow_up?.group&&s.follow_up.state==='open'&&!fuBusy(s)&&!needsDecision(s);
 const batch=new Set((state.follow_up_progress||[]).filter(p=>p.going).map(p=>p.group||'own')),inBatch=s=>s.follow_up&&fuBusy(s)&&batch.has(s.follow_up.group||'own');
 for(const s of [...ready,...needs,...preparing])if(member(s))(groups[s.follow_up.group]??=[]).push(s);
 const grouped=new Set(Object.values(groups).flat().map(s=>s.id)),cards=Object.entries(groups).map(([g,l])=>[l.some(s=>s.status==='prepared'),fuGroupCard(g,l)]);
 const out=list=>list.filter(s=>typeof s==='string'||!grouped.has(s.id));
 return {ready:[...cards.filter(([r])=>r).map(([,c])=>c),...out(ready).filter(s=>!inBatch(s))],needs:out(needs),preparing:[...cards.filter(([r])=>!r).map(([,c])=>c),...out(preparing)]}}
// The sidebar lists a board's group as one row that opens the review
const fuGroups=new Map();
function fuSide(items){return items.map(x=>typeof x==='string'&&fuGroups.has(x)?fuGroups.get(x):x)}
function fuGroupCard(g,all){const list=all.filter(s=>s.status==='prepared'),writing=all.length-list.length,board=all[0].follow_up.board||'',names=all.map(s=>s.follow_up.name||s.follow_up.project),first=names.slice(0,3);
 const title=list.length?t(['{} follow-up ready for {}','{} follow-ups ready for {}'],list.length,board):t('Follow-ups for {}',board);
 const card=`<h3>${list.length?`<button type="button" class="title-link fu-title" data-fu-review="${esc(g)}"><span translate="no">${esc(title)}</span></button>`:`<span translate="no">${esc(title)}</span>`}</h3>`
  +`<div class="meta"><div class="card-badges"><span class="meta-side">${time(all.map(s=>s.created_at).sort().pop(),true)}</span></div></div>`
  +(writing?`<p class="fu-progress" role="status">${esc(t(['Writing {} follow-up…','Writing {} follow-ups…'],writing))}</p>`:'')
  +`<p class="fu-names">${esc(names.length>3?t('{}, {}, {} and {} more',...first,names.length-3):namesLine(first))}</p>`
  +(list.length?`<div class="actions"><button class="primary" data-fu-review="${esc(g)}">${esc(t('Review'))}</button></div>`:'')+'</article>';
 const html=`<article class="card todo ${list.length?'t-mint':'t-lavender'} fu-group" id="fu-${esc(g.replace(':','-'))}" data-status="${list.length?'prepared':'accepted'}">`+card;  // see fuSide
 fuGroups.set(html,{id:'fu-'+g,fuGroup:g,title,created_at:all[0].created_at,scope:all[0].scope,writing:!list.length});return html}
// "Sending 3 of 8…" while a batch goes out, then "Sent 8" (or "Sent 7 of 8": the one that failed is back as a to-do that asks).
// One held right before it went (a new message in the thread since the draft, or the thread couldn't be checked): "Sent 7 · 1 held (new message)".
// Stop sending: "Stopped. 1 sent, 11 kept as drafts." (the one going out when it was pressed still goes, and counts once sent)
const fuSendingLine=p=>p.stopped?(p.stopped===1?t('Stopped. {} sent, 1 kept as a draft.',p.sent):t('Stopped. {} sent, {} kept as drafts.',p.sent,p.stopped)):p.going?t('Sending {} of {}…',Math.min(p.done+1,p.total),p.total):p.held?(p.held_new===p.held?t('Sent {} · {} held (new message)',p.sent,p.held):t('Sent {} · {} held',p.sent,p.held)):p.sent===p.total?t('Sent {}',p.total):t('Sent {} of {}',p.sent,p.total);
const fuSendingCard=p=>{const going=p.going&&!p.stopped;return `<article class="card todo t-mint fu-sending" id="fu-sending-${esc((p.group||'own').replace(':','-'))}" data-status="prepared"><h3><span translate="no">${esc(p.board?t('Follow-ups for {}',p.board):t('Follow-ups'))}</span>${!p.going&&p.batch?`<button type="button" class="fu-x" data-fu-dismiss="${esc(p.batch)}" aria-label="${esc(t('Dismiss'))}" title="${esc(t('Dismiss'))}">×</button>`:''}</h3>`
 +`<p class="fu-progress${going||p.held?'':' ok'}" role="status">${esc(fuSendingLine(p))}</p>${going?`<p class="fu-spaced">${esc(p.done_at?t('Spaced out so they don’t look automated · done around {}',fmtHM(p.done_at)):t('Spaced out so they don’t look automated'))}</p>`:''}${going?`<div class="fu-bar" aria-hidden="true"><i style="width:${Math.round(100*p.done/p.total)}%"></i></div>`:''}`
 +(going&&p.batch?`<div class="actions"><button type="button" data-fu-stop="${esc(p.batch)}">${esc(t('Stop sending'))}</button></div>`:'')+'</article>'};
const fuSendingCards=()=>scopeFilter==='personal'?'':fuShownProgress().map(fuSendingCard).join('');
// A finished batch's card ("Sent 13") can be dismissed with its ×; it stays hidden after a reload (this browser), and
// still goes by itself a few minutes after the last send. Never while sending.
const FU_GONE='fu-dismissed-batches';
const fuGone=()=>{try{return JSON.parse(localStorage.getItem(FU_GONE)||'[]')}catch{return []}};
const fuShownProgress=()=>{const gone=new Set(fuGone());return (state.follow_up_progress||[]).filter(p=>p.going||!p.batch||!gone.has(p.batch))};
// Bring back: a skipped follow-up is ready to review again, with its draft (follow_ups.bring_back)
document.addEventListener('click',async e=>{const b=e.target.closest?.('[data-fu-back]');if(!b)return;e.preventDefault();e.stopPropagation();b.disabled=true;
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'follow_up_bring_back',args:{id:b.dataset.fuBack}})});
  toast(t('Back to review.'));await refresh();if(graphNode&&!$('#people').hidden)await people(graphNode,true)}
 catch(x){errCaught(x);toast(x.message,true);b.disabled=false}},true);
// Stop sending: the ones not gone yet are canceled on the Machine and their drafts are back in the review (follow_ups.stop)
document.addEventListener('click',async e=>{const b=e.target.closest?.('[data-fu-stop]');if(!b)return;e.preventDefault();b.disabled=true;
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'follow_up_stop',args:{batch:b.dataset.fuStop}})});await refresh()}
 catch(x){errCaught(x);toast(x.message);b.disabled=false}});
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-fu-dismiss]');if(!b)return;e.preventDefault();
 try{localStorage.setItem(FU_GONE,JSON.stringify([...fuGone().filter(x=>x!==b.dataset.fuDismiss),b.dataset.fuDismiss].slice(-50)))}catch{}
 b.closest('.fu-sending')?.remove();render()});
let fr=null;
const frDraft=s=>taskActions(s).find(a=>DRAFT_KINDS.includes(a.kind)&&draftText(a));
// A draft the review's Change is rewriting stays in the list while its to-do is back at work, and so does one that
// couldn't be changed (its "try again" is here)
const frList=()=>state.suggestions.filter(s=>s.follow_up?.group===fr.g&&s.follow_up.state==='open'&&!fr.gone.has(s.id)&&!fuBusy(s)
 &&(s.status==='prepared'||(fr.changing.has(s.id)||fr.failed.has(s.id))&&['instructions','accepted'].includes(s.status)))
 .sort((a,b)=>fr.skipped.has(a.id)-fr.skipped.has(b.id));  // skipped ones wait at the bottom until the review closes
// Every draft shows in full and the list is the only thing that scrolls; moving (j/k, a click) changes the current one
// in place and scrolls it into view smoothly, a poll redraws only the drafts that changed and keeps where the list is
const frPhase=s=>fr.skipped.has(s.id)?'skip':fr.changing.has(s.id)?'run':fr.failed.has(s.id)?'fail':fr.undo.has(s.id)?'done':'';
const frItemSig=s=>s.id+':'+(frDraft(s)?.revision||'')+':'+s.status+':'+frPhase(s)+':'+(s.action_status?.error||'')+':'+(s.follow_up?.advice||'');
const frSig=list=>list.map(s=>s.id).join();
const frReady=s=>s.status==='prepared'&&!fr.changing.has(s.id)&&!fr.skipped.has(s.id);
// Held right before it went because the thread got a new message (follow_ups.HELD): left out of Send all checked until the
// owner ticks it again, and its Send is a plain one. "Couldn’t check the thread" stays checked: trying again is the point.
const frStale=s=>s.action_status?.status==='blocked'&&s.action_status.error==='Not sent: new message in the thread.';
// The Machine would stop here (follow_ups.advise): the draft is there, unchecked, and the owner decides
const frAdvised=s=>!!s.follow_up?.advice;
// The project's name without the board's in front (follow_ups.short_name): the title names the board already
const frName=f=>f.name||f.project;
function frOpen(g){fr={g,at:0,cur:null,checked:null,editing:null,gone:new Set(),sent:0,busy:false,box:null,changing:new Map(),failed:new Map(),undo:new Map(),shown:new Map(),skipped:new Map()};
 const list=frList();fr.checked=new Set(list.filter(s=>!frStale(s)&&!frAdvised(s)).map(s=>s.id));fr.seen=new Set(list.map(s=>s.id));
 const d=$('#fu-review');d.innerHTML='';frDraw();const ol=d.querySelector('.fr-list');if(!ol)return;if(!d.open)d.showModal();ol.scrollTop=0;d.querySelector('.fr-item.on')?.focus({preventScroll:true})}
// A draft's text exactly as it goes out: every line and every blank line (the one between "Regards," and the name
// too), only blank lines at its very start and end left out
const frBody=text=>esc(String(text).replace(/^(?:[ \t]*\n)+|\s+$/g,''));
function frState(s){const ph=frPhase(s);
 if(ph==='skip')return `<p class="fr-state skip">${esc(t('Skipped'))}<button type="button" class="link" data-fr-unskip="${esc(s.id)}">${esc(t('Undo'))}</button></p>`;
 if(ph==='run')return `<p class="fr-state run" role="status"><i class="fr-spin" aria-hidden="true"></i>${esc(t('Rewriting…'))}</p>`;
 if(ph==='fail')return `<p class="fr-state fail" role="status">${esc(t('Couldn’t change this one, try again'))}<button type="button" class="link" data-fr-retry="${esc(s.id)}">${esc(t('Try again'))}</button></p>`;
 if(ph==='done')return `<p class="fr-state done"><button type="button" class="link" data-fr-undo="${esc(s.id)}">${esc(t('Undo change'))}</button></p>`;
 return ''}
function frItem(s,i){const a=frDraft(s),f=s.follow_up,on=i===fr.at,edit=fr.editing===s.id;fr.shown.set(s.id,a?.revision);const to=a?[movedLine(a)||(a.to_name||(a.to||[]).join(', ')?t('To {}',a.to_name||(a.to||[]).join(', ')):''),a.from_options?.length>1&&a.from?t('From {}',a.from):''].filter(Boolean).join(' · '):'',ready=frReady(s);
 const skip=fr.skipped.has(s.id);
 return `<li class="fr-item${on?' on':''}${fr.changing.has(s.id)?' rewriting':''}${skip?' skipped':''}" data-fr="${esc(s.id)}" data-fr-at="${i}" tabindex="${on?0:-1}" aria-current="${on}" aria-busy="${fr.changing.has(s.id)}"><div class="fr-head"><input type="checkbox" data-fr-check="${esc(s.id)}"${fr.checked.has(s.id)?' checked':''}${skip?' disabled':''} aria-label="${esc(t('Include {}',frName(f)))}"><b title="${esc(f.project)}">${esc(frName(f))}</b><span class="fr-meta">${esc(t('Follow-up {} of {}',f.n,f.max))} · ${esc(FU_CHANNELS[f.channel]||f.channel)}</span></div>`
  +`<div class="fr-sub"><p class="fr-to" title="${esc(to)}">${esc(to)}</p><div class="fr-actions">${edit?`<button type="button" class="primary" data-fr-save="${esc(s.id)}">${esc(t('Save'))}</button><button type="button" class="ghost" data-fr-cancel>${esc(t('Cancel'))}</button>`:`<button type="button" class="${frStale(s)||frAdvised(s)?'fr-plain':'primary'}" data-fr-send="${esc(s.id)}"${a&&ready&&!fr.box?'':' disabled'}>${esc(t('Send'))}</button><button type="button" class="ghost" data-fr-edit="${esc(s.id)}"${a&&ready?'':' disabled'}>${esc(t('Edit'))}</button><button type="button" class="ghost" data-fr-skip="${esc(s.id)}"${fr.changing.has(s.id)||skip?' disabled':''}>${esc(t('Skip'))}</button>`}</div></div>`
  +(s.action_status?.status==='blocked'&&s.action_status.error&&!fr.changing.has(s.id)?`<p class="fr-held" role="status">${esc(heldLine(s.action_status.error))}</p>`:'')+frState(s)
  +(frAdvised(s)&&!skip?`<p class="fr-advice"><span>${esc(t('The Machine would stop here: {}',f.advice))}</span><button type="button" class="link" data-fr-end="${esc(s.id)}"${fr.box?' disabled':''}>${esc(t('Stop follow-ups here'))}</button></p>`:'')
  +(a?(edit?`<textarea class="fr-edit" data-fr-text="${esc(s.id)}" rows="6" aria-label="${esc(t('Follow-up text'))}">${esc(plainDraft(draftText(a)))}</textarea>`:`<div class="fr-body">${frBody(plainDraft(draftText(a)))}</div>`):`<p class="muted fr-none">${esc(t('No draft yet.'))}</p>`)+'</li>'}
// Change: what should change, for all checked drafts or only the current one (the c key opens it)
function frBox(list){if(!fr.box)return '';const n=list.filter(s=>fr.checked.has(s.id)&&frReady(s)).length,one=list.find(s=>s.id===fr.box.one)||list[fr.at];
 if(!n&&fr.box.scope==='all')fr.box.scope='one';
 return `<div class="fr-change" role="group" aria-labelledby="fr-change-q"><label class="fr-change-q" id="fr-change-q" for="fr-change-text">${esc(t('What should change?'))}</label>`
  +`<div class="mic-wrap"><textarea id="fr-change-text" rows="2" maxlength="2000" enterkeyhint="send">${esc(fr.box.text)}</textarea>${micBtn()}</div>`
  +`<div class="fr-scope"><label class="fu-radio"><input type="radio" name="fr-scope" value="all"${fr.box.scope==='all'?' checked':''}${n?'':' disabled'}><span>${esc(t('All checked ({})',n))}</span></label>`
  +`<label class="fu-radio"><input type="radio" name="fr-scope" value="one"${fr.box.scope==='one'?' checked':''}><span class="fr-one" translate="no">${esc(t('Only this one: {}',one?frName(one.follow_up):''))}</span></label></div>`
  +`<div class="fr-change-actions"><button type="button" class="ghost" data-fr-box-cancel>${esc(t('Cancel'))}</button><button type="button" class="primary" data-fr-box-go>${esc(t('Rewrite'))}</button></div></div>`}// The control that has focus, as a selector that finds it again after a redraw
const frFocusSel=d=>{const a=document.activeElement;if(!a||!d.contains(a))return null;if(a.id==='fr-change-text')return '#fr-change-text';if(a.name==='fr-scope')return `[name=fr-scope][value=${a.value}]`;
 for(const k of ['frCheck','frSend','frEdit','frSkip','frUnskip','frUndo','frRetry'])if(a.dataset?.[k])return `[data-${k.replace(/[A-Z]/g,c=>'-'+c.toLowerCase())}="${CSS.escape(a.dataset[k])}"]`;
 if(a.matches('.fr-item'))return `.fr-item[data-fr="${CSS.escape(a.dataset.fr)}"]`;return null};
function frDraw(reveal){const d=$('#fu-review'),list=frList();if(!list.length){if(d.open)d.close();if(fr.sent)toast(t(['{} follow-up on its way','{} follow-ups on their way'],fr.sent));return}
 const was=list.findIndex(s=>s.id===fr.cur);if(was>=0)fr.at=was;fr.at=Math.max(0,Math.min(fr.at,list.length-1));fr.cur=list[fr.at].id;fr.sig=frSig(list);fr.item=new Map(list.map(s=>[s.id,frItemSig(s)]));
 const n=list.filter(s=>fr.checked.has(s.id)&&frReady(s)).length,board=list[0].follow_up.board||'',keep=d.querySelector('.fr-list')?.scrollTop,back=frFocusSel(d);
 d.innerHTML=`<div class="snooze-heading"><h2 id="fu-review-title" title="${esc(board)}">${esc(t(['{} follow-up for {}','{} follow-ups for {}'],list.length,board))}</h2><button type="button" data-fr-close aria-label="${esc(t('Close'))}">×</button></div>`
  +`<p class="fu-keys">${esc(t('Keys: j and k move, Enter sends, e edits, s skips, c changes.'))}</p><ol class="fr-list">${list.map(frItem).join('')}</ol>${frBox(list)}<p class="ed-note warn" data-fr-error role="alert" hidden></p>`
  +`<div class="ed-actions fr-main"${fr.box?' hidden':''}><button type="button" class="ghost" data-fr-change aria-expanded="${!!fr.box}">${esc(t('Change…'))}</button><span class="grow"></span><button type="button" class="ghost" data-fr-close>${esc(t('Close'))}</button><button type="button" class="primary" data-fr-all${n&&!fr.changing.size?'':' disabled'}>${esc(t('Send all checked ({})',n))}</button></div>`;
 if(keep)d.querySelector('.fr-list').scrollTop=keep;const on=d.querySelector('.fr-item.on');
 if(fr.editing)d.querySelector('.fr-edit')?.focus({preventScroll:true});else (back&&d.querySelector(back)||on)?.focus({preventScroll:true});
 if(reveal)frReveal(on)}
// One draft drawn again where it is (a rewrite came back, Undo, a failure): the rest of the list, its scroll and focus stay
function frPatch(s){const d=$('#fu-review'),el=d.querySelector(`.fr-item[data-fr="${CSS.escape(s.id)}"]`);if(!el)return false;
 const back=el.contains(document.activeElement)?frFocusSel(d):null,i=+el.dataset.frAt,box=document.createElement('template');box.innerHTML=frItem(s,i);
 // the draft at the top of the view stays where it is, also when one above it got shorter or longer
 const ol=el.closest('.fr-list'),top=ol.getBoundingClientRect().top,pin=[...ol.children].find(x=>x.getBoundingClientRect().bottom>top),pinId=pin?.dataset.fr,pinAt=pin?.getBoundingClientRect().top;
 el.replaceWith(box.content.firstElementChild);
 if(pinId){const n=ol.querySelector(`.fr-item[data-fr="${CSS.escape(pinId)}"]`),dy=n?n.getBoundingClientRect().top-pinAt:0;if(Math.abs(dy)>=1)ol.scrollTop+=dy}fr.item.set(s.id,frItemSig(s));if(back)(d.querySelector(back)||d.querySelector(`.fr-item[data-fr="${CSS.escape(s.id)}"]`))?.focus({preventScroll:true});return true}
// Bring the current draft into view: nothing when it's already in view; a tall one lines up its top (for a click, only
// when it isn't in view at all, so a click never pulls the text away from under the pointer)
function frReveal(el,click){const ol=el?.closest('.fr-list');if(!ol)return;const v=ol.getBoundingClientRect(),r=el.getBoundingClientRect(),pad=8,fits=r.height<=v.height-2*pad;let dy=0;
 if(fits){if(r.top<v.top+pad)dy=r.top-v.top-pad;else if(r.bottom>v.bottom-pad)dy=r.bottom-v.bottom+pad}
 else if(!click||r.bottom<v.top||r.top>v.bottom)dy=r.top-v.top-pad;
 if(Math.abs(dy)>1)ol.scrollBy({top:dy,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})}
function frMove(i,click){const d=$('#fu-review'),items=[...d.querySelectorAll('.fr-item')];if(!items.length)return;i=Math.max(0,Math.min(i,items.length-1));
 fr.at=i;fr.cur=items[i].dataset.fr;items.forEach((el,j)=>{const on=j===i;el.classList.toggle('on',on);el.tabIndex=on?0:-1;el.setAttribute('aria-current',on)});
 if(fr.box){fr.box.one=fr.cur;const s=frList().find(x=>x.id===fr.cur),one=d.querySelector('.fr-one');if(s&&one)one.textContent=t('Only this one: {}',frName(s.follow_up))}
 if(!items[i].contains(document.activeElement))items[i].focus({preventScroll:true});frReveal(items[i],click)}
// One row of buttons at a time: while the Change box is open its Cancel and Rewrite are the only ones (the Send row is
// hidden and no draft sends), and while a rewrite runs nothing is sent all at once
function frModes(){const d=$('#fu-review'),main=d.querySelector('.fr-main');if(main)main.hidden=!!fr.box;
 for(const b of d.querySelectorAll('[data-fr-send]')){const s=state.suggestions.find(x=>x.id===b.dataset.frSend);b.disabled=!!fr.box||!s||!frDraft(s)||!frReady(s)}
 for(const b of d.querySelectorAll('[data-fr-end]'))b.disabled=!!fr.box}
function frCount(){const list=frList(),n=list.filter(s=>fr.checked.has(s.id)&&frReady(s)).length,all=$('#fu-review [data-fr-all]');if(all){all.textContent=t('Send all checked ({})',n);all.disabled=!n||!!fr.changing.size}frModes();
 const scope=$('#fu-review [name=fr-scope][value=all]');if(scope){scope.disabled=!n;scope.nextElementSibling.textContent=t('All checked ({})',n);if(!n&&scope.checked){scope.checked=false;fr.box.scope='one';$('#fu-review [name=fr-scope][value=one]').checked=true}}}
// Where each rewrite stands, from the to-do itself: a new draft revision is done (the old text kept for Undo change); its
// run stuck, or a reply that left the draft as it was, couldn't change it. A to-do that closed meanwhile leaves the list.
function frTrack(){for(const [id,c] of fr.changing){const s=state.suggestions.find(x=>x.id===id);
  if(!s||s.follow_up?.state!=='open'||['completed','rejected','snoozed'].includes(s.status)){fr.changing.delete(id);fr.gone.add(id);continue}
  if(s.status!=='prepared')c.seen=true;const a=frDraft(s);
  if(s.status==='prepared'&&a&&a.revision!==c.from){fr.changing.delete(id);fr.undo.set(id,{body:c.body,subject:c.subject})}
  else if(c.seen&&(s.status==='prepared'||s.preparation_status==='blocked')){fr.changing.delete(id);fr.failed.set(id,c.text)}}}
// A poll: new drafts join (checked), sent or changed ones update in place; the draft being edited is left as it is
function frRefresh(){const d=$('#fu-review');if(!fr||!d.open||fr.busy)return;frTrack();const list=frList();
 for(const s of list)if(!fr.seen.has(s.id)){fr.seen.add(s.id);if(!frStale(s)&&!frAdvised(s))fr.checked.add(s.id)}
 if(frSig(list)===fr.sig){let n=0;for(const s of list)if(s.id!==fr.editing&&fr.item.get(s.id)!==frItemSig(s)&&frPatch(s))n++;if(n)frCount();return}
 if(!fr.editing)frDraw()}
const frSay=x=>{const p=$('#fu-review [data-fr-error]');if(p){p.textContent=x;p.hidden=!x}};
// Only the text the owner sees goes: a draft that changed since it was drawn (a rewrite, an edit elsewhere) is drawn again
// instead, to read first; nothing sends while the Change box is open or its draft is being rewritten
async function frSend(id,quiet){const s=state.suggestions.find(x=>x.id===id),a=s&&frDraft(s);if(!a||!frReady(s)||fr.box)return false;
 if(a.revision!==fr.shown.get(id)){frPatch(s);return 'changed'}
 if(a.to_options?.length){if(quiet)return false;$('#fu-review').close();openSend(id,a.revision);return false}  /* who gets it is the owner's pick: the send dialog asks; the From is the draft's own (shown in the list) */
 await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'confirm_action',args:{suggestion_id:id,revision:a.revision,approval_id:crypto.randomUUID()}})});
 fr.gone.add(id);fr.undo.delete(id);fr.shown.delete(id);fr.sent++;return true}
// The Change box opens and closes in place: the drafts, their scroll and any rewrite under way stay as they are
function frBoxOpen(){const d=$('#fu-review');if(!fr.box){const n=frList().filter(s=>fr.checked.has(s.id)&&frReady(s)).length;fr.box={text:'',scope:n?'all':'one',one:fr.cur}}
 if(!d.querySelector('.fr-change'))d.querySelector('[data-fr-error]')?.insertAdjacentHTML('beforebegin',frBox(frList()));d.querySelector('[data-fr-change]')?.setAttribute('aria-expanded','true');frModes();
 const box=$('#fr-change-text');box?.focus({preventScroll:true});box?.closest('.fr-change')?.scrollIntoView({block:'nearest'})}
// Rewrite: each draft in scope goes through its to-do's chat path (follow_up_change), at most a few at once on the
// Machine; each shows "Rewriting…" where it is until its new text is back. Nothing is sent.
function frBoxClose(){const d=$('#fu-review');fr.box=null;d.querySelector('.fr-change')?.remove();d.querySelector('[data-fr-change]')?.setAttribute('aria-expanded','false');frModes();
 d.querySelector('.fr-item.on')?.focus({preventScroll:true})}
async function frChange(ids,text){const list=frList(),pick=list.filter(s=>ids.includes(s.id)&&(frReady(s)||fr.failed.has(s.id)));if(!pick.length||!text)return;
 const before=new Map(pick.map(s=>{const a=frDraft(s);return [s.id,{from:a?.revision,body:a?draftText(a):'',subject:a?.subject,text,seen:false}]}));
 const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'follow_up_change',args:{ids:pick.map(s=>s.id),text}})});
 for(const c of r.changing||[]){const b=before.get(c.id);if(!b)continue;fr.changing.set(c.id,{...b,from:c.revision});fr.failed.delete(c.id);fr.undo.delete(c.id)}
 for(const id of r.skipped||[])if(before.has(id))fr.failed.set(id,text);
 for(const s of list)if(before.has(s.id))frPatch(s);frCount();sendWatch()}
// Skip: the draft stays in the list, unchecked, dimmed and at the bottom, marked Skipped with an Undo; it is skipped for
// good (decide reject: that waiting point is handled) only when the review closes. The next draft becomes the current one.
function frSkip(id){const list=frList(),i=list.findIndex(s=>s.id===id);if(i<0||fr.skipped.has(id))return;
 fr.skipped.set(id,fr.checked.has(id));fr.checked.delete(id);fr.editing=fr.editing===id?null:fr.editing;
 const next=list.slice(i+1).find(s=>!fr.skipped.has(s.id))||list.slice(0,i).reverse().find(s=>!fr.skipped.has(s.id));fr.cur=(next||list[i]).id;frDraw(true)}
function frUnskip(id){if(!fr.skipped.has(id))return;if(fr.skipped.get(id))fr.checked.add(id);fr.skipped.delete(id);fr.cur=id;frDraw(true)}
// Everything left is skipped after a send: the review is done
function frDoneIfSkipped(){const d=$('#fu-review'),list=frList();if(d.open&&fr.sent&&list.length&&list.every(s=>fr.skipped.has(s.id))){toast(t(['{} follow-up on its way','{} follow-ups on their way'],fr.sent));d.close()}}
async function frAct(b){const d=$('#fu-review');frSay('');fr.busy=true;try{
 if(b.dataset.frSend){b.disabled=true;const r=await frSend(b.dataset.frSend);if(d.open)frDraw(true);if(r==='changed')frSay(t('This draft changed: read it, then send.'));else frDoneIfSkipped()}
 else if(b.dataset.frSkip)frSkip(b.dataset.frSkip)
 else if(b.dataset.frUnskip)frUnskip(b.dataset.frUnskip)
 else if(b.dataset.frEnd){const id=b.dataset.frEnd;b.disabled=true;  // Stop follow-ups here: this round ends, nothing sent (follow_ups.stop_here)
  await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'follow_up_end',args:{id}})});
  fr.gone.add(id);fr.checked.delete(id);fr.skipped.delete(id);toast(t('Follow-ups stopped here.'));frDraw(true)}
 else if(b.dataset.frEdit){fr.editing=fr.cur=b.dataset.frEdit;frDraw(true)}
 else if(b.hasAttribute('data-fr-cancel')){fr.editing=null;frDraw()}
 else if(b.dataset.frSave){const id=b.dataset.frSave,s=state.suggestions.find(x=>x.id===id),a=frDraft(s),text=d.querySelector('.fr-edit').value;b.disabled=true;
  const body=unplainDraft(text,draftText(a)),r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'revise_draft',args:{suggestion_id:id,revision:a.revision,body}})});
  Object.assign(a,{revision:r.revision,body:r.body??body});fr.editing=null;fr.undo.delete(id);frDraw()}
 else if(b.hasAttribute('data-fr-change')){if(fr.box)frBoxClose();else frBoxOpen()}
 else if(b.hasAttribute('data-fr-box-cancel'))frBoxClose()
 else if(b.hasAttribute('data-fr-box-go')){const text=($('#fr-change-text')?.value||'').trim();if(!text){$('#fr-change-text')?.focus();return}
  const scope=d.querySelector('[name=fr-scope]:checked')?.value||'one',list=frList(),ids=scope==='all'?list.filter(s=>fr.checked.has(s.id)&&frReady(s)).map(s=>s.id):[fr.box.one||fr.cur];
  b.disabled=true;await frChange(ids,text);frBoxClose()}
 else if(b.dataset.frRetry){const id=b.dataset.frRetry;b.disabled=true;await frChange([id],fr.failed.get(id)||'')}
 else if(b.dataset.frUndo){const id=b.dataset.frUndo,s=state.suggestions.find(x=>x.id===id),a=s&&frDraft(s),was=fr.undo.get(id);if(!a||!was)return;b.disabled=true;
  const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'revise_draft',args:{suggestion_id:id,revision:a.revision,body:was.body,...(was.subject&&a.subject!==was.subject?{subject:was.subject}:{})}})});
  Object.assign(a,{revision:r.revision,body:r.body??was.body,...(r.subject?{subject:r.subject}:{})});fr.undo.delete(id);frPatch(s)}
 else if(b.hasAttribute('data-fr-all')){if(fr.box||fr.changing.size)return;b.disabled=true;let left=0,moved=0;for(const s of frList().filter(s=>fr.checked.has(s.id)&&frReady(s))){const r=await frSend(s.id,true);if(r==='changed')moved++;else if(!r)left++}
  frDraw();frDoneIfSkipped();if(d.open)frSay([moved?t(['{} draft changed: read it, then send.','{} drafts changed: read them, then send.'],moved):'',left?t(['{} needs you to pick who gets it: send it on its own.','{} need you to pick who gets them: send them on their own.'],left):''].filter(Boolean).join(' '))}
 else if(b.hasAttribute('data-fr-close'))d.close()}catch(x){errCaught(x);frSay(x.message);b.disabled=false}finally{if(fr)fr.busy=false}}
$('#fu-review').addEventListener('click',e=>{const b=e.target.closest('button');if(b){frAct(b);return}const item=e.target.closest('[data-fr-at]');if(item&&!e.target.closest('input,textarea')&&fr.at!==+item.dataset.frAt)frMove(+item.dataset.frAt,true)});
$('#fu-review').addEventListener('change',e=>{if(e.target.name==='fr-scope'&&fr.box){fr.box.scope=e.target.value;return}const c=e.target.closest('[data-fr-check]');if(!c)return;c.checked?fr.checked.add(c.dataset.frCheck):fr.checked.delete(c.dataset.frCheck);frCount()});
$('#fu-review').addEventListener('input',e=>{if(e.target.id==='fr-change-text'&&fr?.box)fr.box.text=e.target.value});
$('#fu-review').addEventListener('keydown',e=>{if(!fr||e.isComposing||e.altKey||e.metaKey)return;const d=$('#fu-review'),list=frList(),cur=list[fr.at];
 if(e.target.id==='fr-change-text'){if(e.key==='Escape'){e.preventDefault();frBoxClose()}else if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();d.querySelector('[data-fr-box-go]')?.click()}return}
 if(e.target.matches('textarea')){if(e.key==='Escape'){e.preventDefault();fr.editing=null;frDraw()}else if(e.key==='Enter'&&e.ctrlKey){e.preventDefault();d.querySelector('[data-fr-save]')?.click()}return}
 if(e.ctrlKey||e.target.matches('input[type=text]'))return;const k=e.key;
 if(k==='j'||k==='ArrowDown'){e.preventDefault();frMove(fr.at+1)}
 else if(k==='k'||k==='ArrowUp'){e.preventDefault();frMove(fr.at-1)}
 else if(k==='Enter'&&cur&&!fr.box&&!e.target.matches('button')){e.preventDefault();d.querySelector(`[data-fr-send="${CSS.escape(cur.id)}"]`)?.click()}
 else if(k==='e'&&cur&&frReady(cur)){e.preventDefault();fr.editing=cur.id;frDraw(true)}
 else if(k==='s'&&cur){e.preventDefault();fr.skipped.has(cur.id)?frUnskip(cur.id):frSkip(cur.id)}
 else if(k==='c'){e.preventDefault();frBoxOpen()}
 else if(k==='x'&&cur){e.preventDefault();const on=!fr.checked.has(cur.id);on?fr.checked.add(cur.id):fr.checked.delete(cur.id);const c=$(`#fu-review [data-fr-check="${CSS.escape(cur.id)}"]`);if(c)c.checked=on;frCount()}});
$('#fu-review').addEventListener('close',()=>{const skip=[...(fr?.skipped.keys()||[])],sent=fr?.sent||fr?.gone.size||fr?.changing.size;fr=null;
 if(skip.length)Promise.all(skip.map(id=>decidePost(id,{choice:'reject',feedback:'',decision_id:crypto.randomUUID()}).catch(errCaught))).finally(()=>refresh().catch(()=>{}));else if(sent)refresh().catch(()=>{})});
document.addEventListener('click',e=>{const w=e.target.closest?.('[data-fu-card]');if(w){e.preventDefault();e.stopPropagation();fuShow(w.dataset.fuCard);return}});
// A board's follow-ups still being written: back to the to-do list, at their to-do
function fuShow(g){if(chatId)location.hash='';document.querySelector('nav [data-tab="inbox"]')?.click();folded.delete('preparing');render();
 const c=document.getElementById('fu-'+g.replace(':','-'));if(!c)return;c.scrollIntoView({block:'center',behavior:'smooth'});c.classList.remove('flash');void c.offsetWidth;c.classList.add('flash')}
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-fu-review]');if(!b)return;e.preventDefault();e.stopPropagation();frOpen(b.dataset.fuReview)},true);
// What someone (or an organization) is to you: said by you, or read by a review in a message, shown with the line it came from.
// ✓ makes a review's role yours; Edit sets it in your words.
const quoteLine=(id,quote,event)=>quote?`<span class="role-why">“${esc(quote)}”${event?` <button class="link" data-quote-event="${event}">Read</button>`:''}</span>`:'';
const confirmButton=(id,role)=>`<button class="ghost" data-role-confirm="${esc(id)}" data-role="${esc(role)}" aria-label="Right: ${esc(role)}">✓ Right</button>`;
// Where someone works: from their work email, or as a source stated it (their LinkedIn headline, a signature, their own words), with that line.
const orgSaid=n=>n.org_by==='email'?'from their work email':n.org_by==='owner'?'you set it':n.org_by==='review'?`from ${n.org_via==='LinkedIn headline'?'their LinkedIn headline':'their '+esc(n.org_via||'message')}${n.org_at?', '+esc(day(n.org_at)):''}`:'';
// The owner's own details for an organization: they win over the service's, and "Wrong company" drops a bad match for good.
const ORG_FIELDS=[['name','Name',100],['website','Website',200],['linkedin_url','LinkedIn',200],['industry','Industry',120],['size','Size (people)',40],['location','Location',120],['founded','Founded',4],['about','About',600],['notes','Notes',4000]];
// The owner's own notes on a person or organization, as typed (lines kept).
const notesSection=t=>t?`<section class="detail-section record-notes"><h4>Notes</h4><p>${esc(t)}</p></section>`:'';
// No maxlength or pattern on the fields: a looked-up value can be longer than the owner may type, and the browser
// would then block Save without a word. Only what the owner changed is checked, by orgCheck, with the error under its field.
const ORG_GROUPS=[['Profile',['name','industry','size','location','founded','about']],['Contact',['website','linkedin_url']],['Notes',['notes']]];
const ORG_WIDTH={industry:'w-mid',size:'w-mid',location:'w-mid',founded:'w-short'};
const orgField=(k,t,v)=>`<label class="pf-field ${ORG_WIDTH[k]||''}"><span>${t}</span>${k==='about'||k==='notes'?`<textarea name="${k}" rows="4" aria-describedby="org-err-${k}"${k==='notes'?' aria-label="Notes"':''}>${esc(v||'')}</textarea>`:`<input name="${k}" value="${esc(v??'')}" aria-describedby="org-err-${k}" autocomplete="off"${k==='founded'?' inputmode="numeric"':''}${k==='name'?' placeholder="Leave empty to use the name from their messages"':''}>`}<small class="field-error" id="org-err-${k}"></small></label>`;
const orgForm=n=>{const p=n.profile||{},v={...p,name:n.name,size:p.size||(p.employees?String(p.employees):'')},label=Object.fromEntries(ORG_FIELDS.map(([k,t])=>[k,t]));
 return `<form class="org-form pf-form" id="org-form" data-node-id="${esc(n.id)}" novalidate hidden>${ORG_GROUPS.map(([g,ks])=>`<fieldset><legend>${g}</legend>${ks.map(k=>orgField(k,label[k],v[k])).join('')}</fieldset>`).join('')}<fieldset><legend>With you</legend><label class="pf-field w-mid"><span>What it is to you</span><input name="role" value="${esc(n.role||'')}" placeholder="e.g. accounting firm, customer" aria-describedby="org-err-role" autocomplete="off"><small class="field-error" id="org-err-role"></small></label></fieldset><p class="graph-sub muted pf-note">Your edits stay. Empty a field to use the looked-up value again.</p>${n.profile&&Object.keys(n.profile).some(k=>k!=='website')&&!n.wrong?'<p class="org-buttons"><button type="button" class="ghost" data-org-wrong>Wrong company, clear details</button></p>':''}</form>`};
const orgActions=n=>`<span class="org-actions"><button class="ghost" data-proj-new-here>New project</button><button class="ghost" data-org-edit>Edit</button><button type="button" class="ghost" data-org-cancel>Cancel</button><button type="submit" form="org-form" class="primary" data-org-save>Save</button><details class="fact-menu person-menu"><summary aria-label="More for this organization" title="More">⋯</summary><div class="fact-menu-list" role="menu"><button type="button" role="menuitem" data-card-here>New to-do</button><button type="button" role="menuitem" data-org-same>Same organization as…</button><button type="button" role="menuitem" data-org-site>Add a website…</button>${n.manual?'<button type="button" role="menuitem" class="danger" data-org-delete>Delete…</button>':''}</div></details></span>`;
// What the server would refuse, for the fields the owner changed only: [field, message] pairs.
const orgCheck=changed=>ORG_FIELDS.flatMap(([k,,max])=>{const t=changed[k];if(!t)return[];
 if(k==='founded')return /^(1[5-9]\d\d|20\d\d)$/.test(t)?[]:[[k,'A year, like 2014']];return t.length>max?[[k,`Up to ${max} characters (now ${t.length})`]]:[]});
const orgOpen=(f,open)=>{const a=f.closest('.graph-detail');f.hidden=!open;if(a){const cs=getComputedStyle(a);a.style.setProperty('--org-pt',cs.paddingTop);a.style.setProperty('--org-px',cs.paddingLeft);a.classList.toggle('org-editing',open)}if(!open){f.reset();f.matches('.person-form')?personErrors(f,[]):orgErrors(f,[])}orgStuck()};
// The editing header, once stuck under the top bar: square corners and a solid backing behind the bar, so nothing scrolled under it shows.
const orgStuck=()=>{const h=document.querySelector('#people-view .graph-detail.org-editing>.name-row');if(h)h.classList.toggle('stuck',h.getBoundingClientRect().top<=parseFloat(getComputedStyle(h).top)+1)};
addEventListener('scroll',orgStuck,{passive:true});
// A field's error goes as soon as the owner edits it, not only on the next Save
const pfErrClear=el=>{const list=el.closest('.pf-list-field');  /* a list of phones or emails shares one error */
 if(list){for(const i of list.querySelectorAll('[aria-invalid]'))i.removeAttribute('aria-invalid');const m=list.querySelector('.field-error');if(m)m.textContent='';return}
 el.removeAttribute('aria-invalid');for(const id of (el.getAttribute('aria-describedby')||'').split(' ')){const m=id&&document.getElementById(id);if(m)m.textContent=''}};
document.addEventListener('input',e=>{const el=e.target;if(el.getAttribute?.('aria-invalid')==='true'&&el.closest('.pf-form'))pfErrClear(el)});
const orgErrors=(f,errs)=>{for(const k of [...ORG_FIELDS.map(([k])=>k),'role']){const el=f.elements[k];if(!el)continue;const m=errs.find(([x])=>x===k);if(m)el.setAttribute('aria-invalid','true');else el.removeAttribute('aria-invalid');f.querySelector('#org-err-'+k).textContent=m?m[1]:''}
 const first=errs.length&&f.elements[errs[0][0]];if(first){first.focus({preventScroll:true});first.scrollIntoView({block:'center'})}};
// A person's page. Header: photo, name, title · organization, where they are, and one plain line on how you're in touch.
// Then Contact, With you and Related as their own sections, and how identities were joined as a quiet disclosure.
// Edit (in the header, as on an organization's page) opens one form for everything; the owner's word wins over a
// look-up and later automatic updates, and stays through merges and Undo (graph.person_edit).
const COUNTRY=c=>{try{return /^[A-Z]{2}$/.test(c)?new Intl.DisplayNames([],{type:'region'}).of(c):c}catch{return c}};
const personPlace=n=>{const p=n.profile||{};return p.location||[p.city,COUNTRY(p.country)].filter(Boolean).join(', ')};
// Facts their connectors read (their own Slack, X or LinkedIn profile, a contact, the CRM) come first; hover says where from.
const FACT_FROM=p=>{const s=Object.values(p.sources||{}).map(x=>x.from);return s.length?'From '+[...new Set(s)].join(', '):''};
const localTime=tz=>{try{if(!tz)return'';const at=z=>fmtHM(Date.now(),{timeZone:z}),theirs=at(tz);return theirs===at(undefined)?'':t('{} their time',theirs)}catch{return''}};  /* only when their clock differs from the owner's */
const personJob=n=>{if(n.kind!=='person')return'';const p=n.profile||{},org=n.org&&n.org_name?`<button class="node" data-node="${esc(n.org)}" title="${esc(n.org_name)}">${esc(n.org_name)}</button>`:p.company?esc(p.company):'';
 const title=p.title||(!org&&n.headline)||'',job=[title?esc(title):'',org].filter(Boolean).join(' · '),place=[personPlace(n),localTime(p.timezone)].filter(Boolean).join(' · '),from=FACT_FROM(p);
 return `${job?`<p class="person-job">${job}</p>`:''}${place?`<p class="person-place"${from?` title="${esc(from)}"`:''}>${esc(place)}</p>`:''}`};
const talkEvery=g=>{const d=Math.round(g);return d<=1?'Talk daily':d<=4?'Talk every few days':d<=10?'Talk weekly':d<=20?'Talk every couple of weeks':d<=45?'Talk monthly':'Talk now and then'};
const relLine=n=>cap([n.quiet?'Gone quiet':n.usual_gap_days?talkEvery(n.usual_gap_days):'',n.last_at?(n.seen_only?'seen ':'last ')+day(n.last_at):'',n.next_meeting?'next meeting '+day(n.next_meeting):''].filter(Boolean).join(' · '));
// Phones and emails as the server lists them (the messages', less what the owner took off, plus what they added).
const personContacts=n=>({phones:n.phones||(n.ids||[]).filter(i=>/^\+\d/.test(i)).map(value=>({value,by:'messages'})),emails:n.emails||(n.ids||[]).filter(i=>i.includes('@')).map(value=>({value,by:'messages'}))});
// A phone number grouped for reading: the country code (ITU zones), then the national number in short groups. One that
// already has spaces is shown as written. Tap and Copy use the number as stored.
const PHONE_CC2=/^(2[07]|3[0-469]|4[013-9]|5[1-8]|6[0-6]|8[1246]|9[0-58])/;
function phoneShown(v){const t=String(v||'').trim();if(!/^\+\d{8,15}$/.test(t))return t;const d=t.slice(1),cc=/^[17]/.test(d)?d[0]:PHONE_CC2.test(d)?d.slice(0,2):d.slice(0,3),n=d.slice(cc.length);
 const g=cc==='1'&&n.length===10?[n.slice(0,3),n.slice(3,6),n.slice(6)]:cc==='32'&&n.length===9?[n.slice(0,3),n.slice(3,5),n.slice(5,7),n.slice(7)]:cc==='32'&&n.length===8?[n.slice(0,1),n.slice(1,4),n.slice(4,6),n.slice(6)]
  :cc==='31'&&n.length===9?[n.slice(0,1),n.slice(1,5),n.slice(5)]:cc==='44'&&n.length===10?[n.slice(0,4),n.slice(4)]:cc==='33'&&n.length===9?[n.slice(0,1),...n.slice(1).match(/\d{2}/g)]
  :n.replace(/\B(?=(\d{3})+(?!\d))/g,' ').split(' ');
 return '+'+cc+' '+g.join(' ')}
const breakable=t=>esc(t).replace(/@/g,'@<wbr>');
// An address that bounced (bounces.py): "Bounced Oct 28", muted, beside it; never struck through, so it stays readable.
const bounceDay=v=>new Date(v).toLocaleDateString(DL,{day:'numeric',month:'short'});
const bounceNote=at=>at?`<span class="bounce-note">${esc(t('Bounced {}',bounceDay(at)))}</span>`:'';
const kv=(k,v,acts='',cls='')=>`<div class="kv${cls?' '+cls:''}"><span class="k">${k}</span><span class="v">${v}</span>${acts?`<span class="acts">${acts}</span>`:''}</div>`;
const copyBtn=(t,what)=>`<button type="button" class="ghost" data-copy-command="${esc(t)}" aria-label="Copy ${what}">Copy</button>`;
const liShort=u=>u.replace(/^https?:\/\/(www\.)?/,'').replace(/\/$/,'');
function personContact(n){const c=personContacts(n),p=n.profile||{};
 const rows=[...c.phones.map(x=>kv('Phone',`<a href="tel:${esc(x.value.replace(/[^\d+]/g,''))}">${esc(phoneShown(x.value))}</a>`,copyBtn(x.value,'phone number'))),
  ...c.emails.map(x=>kv('Email',`<a href="mailto:${esc(x.value)}">${breakable(x.value)}</a>${bounceNote(x.bounced_at)}`,copyBtn(x.value,'email address')))];
 if(/^https:\/\/([a-z]{2,3}\.)?linkedin\.com\//.test(p.linkedin_url||''))rows.push(kv('LinkedIn',`<a href="${esc(p.linkedin_url)}" target="_blank" rel="noreferrer">${breakable(liShort(p.linkedin_url))} ↗</a>`));
 if(/^[A-Za-z0-9_]{1,15}$/.test(p.x||''))rows.push(kv('X',`<a href="https://x.com/${esc(p.x)}" target="_blank" rel="noreferrer">@${esc(p.x)} ↗</a>`));
 if(/^https?:\/\/[^\s]+$/.test(p.website||''))rows.push(kv('Website',`<a href="${esc(p.website)}" target="_blank" rel="noreferrer">${breakable(liShort(p.website))} ↗</a>`));
 const also=[...new Set((n.ids||[]).filter(i=>!i.includes('@')&&!/^\+\d/.test(i)&&!(p.x&&i==='@'+p.x)))];const slack=n.slack_links||[];if(also.length)rows.push(kv('Also on',also.map(a=>a==='Slack'&&slack.length?slack.map(l=>`<a href="${esc(l.url)}" target="_blank" rel="noreferrer" title="Open in Slack">${esc(l.label)} ↗</a>`).join(' · '):esc(a)).join(' · ')));
 return rows.length?`<section class="detail-section person-contact"><h4>Contact</h4>${rows.join('')}</section>`:''}
function personAbout(n){const rows=[],f=n.fleet,work=f?.in?.find(x=>x.kind==='work');
 rows.push(kv('To you',n.role?`<b>${esc(cap(n.role))}</b>${n.role_by==='review'?`<span class="sub">A review read it in your messages${n.role_quote?`: ${quoteLine(n.id,n.role_quote,n.role_event_id)}`:''}</span>`:''}`:'<span class="muted">Not known yet</span>',n.role_by==='review'?confirmButton(n.id,n.role):'','kv-role'));
 if(n.side)rows.push(kv('Type',n.side==='work'?'Work contact':'Personal contact'));
 if(f?.in?.length)rows.push(kv('Network',`<span class="fleet-mark">${esc([...new Set(f.in.map(x=>x.kind==='work'&&x.fleet_name?`${x.label} (${x.fleet_name})`:x.label)),f.machine?'Has a Machine':''].filter(Boolean).join(' · '))}</span>`,`<button type="button" class="ghost" data-fleet-member="${esc(f.in[0].member_id)}">See in Fleet</button>${work?`<button type="button" class="ghost" data-fleet-free="${esc(work.fleet)}">Ask your Fleet</button>`:''}`));
 if(f?.named)rows.push(kv('Name',`<span class="fleet-named">From your ${work?'Fleet':f.in[0].kind==='family'?'Family':'Friends'}. Your messages say “${esc(n.name_from_messages||'')}”.</span>`,`<button type="button" class="ghost" data-fleet-keep="${esc(n.name)}">Keep</button>`));
 if(graphOwners.length)rows.push(ownerRow(n));
 return `<section class="detail-section person-about"><h4>With you</h4>${rows.join('')}</section>`}
// People, Projects and Organizations linked to a page, each its own section (person and organization pages alike).
const detailGroups=(n,group)=>`${n.relations?.length?`<section class="detail-section"><h4>How they’re related</h4><div class="relations">${n.relations.map(r=>`<div class="graph-sub relation"><span>${esc(r.a_name)} is ${esc(r.relation)} ${esc(r.b_name)}</span><button class="ghost" data-unrelate="${esc(r.a)}" data-related-to="${esc(r.b)}">Remove</button></div>`).join('')}</div></section>`:''}`
 +[['person','People'],['project','Projects'],['org','Organizations']].map(([k,t])=>group(k).length?`<section class="detail-section"><h4>${t}</h4><div class="graph-links">${group(k).map(nodeButton).join('')}</div></section>`:'').join('');
// A person's ⋯ menu: Delete permanently… (rarely needed), which opens its own confirm step under the header.
const personMenu='<details class="fact-menu person-menu"><summary aria-label="More for this person" title="More">⋯</summary><div class="fact-menu-list" role="menu"><button type="button" role="menuitem" data-proj-new-here>New project</button><button type="button" role="menuitem" data-card-here>New to-do</button><button type="button" role="menuitem" data-same-as>Same person as…</button><button type="button" role="menuitem" class="danger" data-person-delete>Delete permanently…</button></div></details>';
const personActions=`<span class="org-actions"><button class="ghost" data-org-edit>Edit</button><button type="button" class="ghost" data-org-cancel>Cancel</button><button type="submit" form="org-form" class="primary" data-org-save>Save</button>${personMenu}</span>`;
// The edit form: fields as long as what goes in them, grouped as the page is. Only what the owner changed is sent.
const PERSON_LIMITS={name:100,title:120,org:100,location:120,linkedin_url:200,role:60,notes:4000};
const pfField=(k,label,value,{hint='',placeholder='',cls='',type='text',mode=''}={})=>`<label class="pf-field ${cls}"><span>${label}</span><input name="${k}" type="${type}" value="${esc(value||'')}"${placeholder?` placeholder="${esc(placeholder)}"`:''}${mode?` inputmode="${mode}"`:''} aria-describedby="pe-err-${k}" autocomplete="off">${hint?`<small class="muted">${hint}</small>`:''}<small class="field-error" id="pe-err-${k}"></small></label>`;
const pfItem=(kind,v)=>`<div class="pf-item"><input name="${kind}" type="${kind==='phones'?'tel':'email'}" value="${esc(v)}" aria-label="${kind==='phones'?'Phone':'Email'}"${kind==='phones'?' inputmode="tel"':''} autocomplete="off"><button type="button" class="ghost" data-pf-remove aria-label="Remove">✕</button></div>`;
const pfList=(kind,label,items)=>`<div class="pf-field pf-list-field ${kind==='phones'?'w-phone':'w-email'}"><span>${label}</span><div class="pf-list" data-kind="${kind}" data-was="${esc(items.join('\n'))}">${items.map(v=>pfItem(kind,v)).join('')}</div><button type="button" class="ghost pf-add" data-pf-add="${kind}">+ Add ${kind==='phones'?'phone':'email'}</button><small class="field-error" id="pe-err-${kind}"></small></div>`;
function personForm(n){const p=n.profile||{},c=personContacts(n),said=orgSaid(n),side=n.side||'';
 return `<form class="org-form pf-form person-form" id="org-form" data-node-id="${esc(n.id)}" novalidate hidden>
 <fieldset><legend>Profile</legend>${pfField('name','Name',n.name,{placeholder:'Leave empty to use the name from their messages'})}${pfField('title','Title',p.title)}${pfField('org','Organization',n.org_name||'',{hint:said?cap(said.replace(/<[^>]+>/g,''))+(n.org_by==='review'&&n.org_quote?`: “${esc(n.org_quote)}”`:''):'',placeholder:'Where do they work? e.g. Acme',cls:'w-mid'})}${pfField('location','Location',p.location||personPlace(n),{placeholder:'e.g. Ghent, Belgium',cls:'w-mid'})}${pfField('linkedin_url','LinkedIn',p.linkedin_url,{placeholder:'linkedin.com/in/…',type:'url'})}</fieldset>
 <fieldset><legend>Contact</legend>${pfList('phones','Phone',c.phones.map(x=>x.value))}${pfList('emails','Email',c.emails.map(x=>x.value))}</fieldset>
 <fieldset><legend>With you</legend>${pfField('role','What they are to you',n.role||'',{placeholder:'e.g. accountant, sister, investor',cls:'w-mid'})}<div class="pf-field"><span id="pf-side-l">Type</span><div class="pf-seg" role="radiogroup" aria-labelledby="pf-side-l" data-was="${esc(side)}">${[['work','Work'],['personal','Personal']].map(([v,t])=>`<label><input type="radio" name="side" value="${v}"${side===v?' checked':''}><span>${t}</span></label>`).join('')}</div><small class="field-error" id="pe-err-side"></small></div><label class="pf-field"><span>Notes</span><textarea name="notes" rows="4" aria-describedby="pe-err-notes">${esc(n.notes||'')}</textarea><small class="field-error" id="pe-err-notes"></small></label></fieldset>
 <p class="graph-sub muted pf-note">Your edits stay, also when their details are looked up again. Empty a field to use the looked-up value again.</p></form>`}
const pfValues=(f,kind)=>[...f.querySelectorAll(`.pf-list[data-kind="${kind}"] input`)].map(i=>i.value.trim()).filter(Boolean);
// What the owner changed, as the server takes it: {field: value}. Lists are sent whole, as they are now.
function personChanged(f){const out={};for(const k of Object.keys(PERSON_LIMITS)){const el=f.elements[k];if(el&&el.value.trim()!==el.defaultValue.trim())out[k]=el.value.trim()}
 for(const kind of ['phones','emails']){const now=pfValues(f,kind),was=f.querySelector(`.pf-list[data-kind="${kind}"]`).dataset.was.split('\n').filter(Boolean);if(now.join('\n')!==was.join('\n'))out[kind]=now}
 const side=f.querySelector('input[name=side]:checked')?.value||'',seg=f.querySelector('.pf-seg');if(side!==seg.dataset.was)out.side=side;return out}
const PHONE_RE=/^\+?[\d\s().-]{6,40}$/,EMAIL_RE=/^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const personCheck=ch=>Object.entries(ch).flatMap(([k,v])=>k==='phones'?v.filter(x=>!PHONE_RE.test(x)).slice(0,1).map(x=>[k,`${x} is not a phone number`]):k==='emails'?v.filter(x=>!EMAIL_RE.test(x)).slice(0,1).map(x=>[k,`${x} is not an email address`]):PERSON_LIMITS[k]&&v.length>PERSON_LIMITS[k]?[[k,`Up to ${PERSON_LIMITS[k]} characters (now ${v.length})`]]:[]);
function personErrors(f,errs){for(const el of f.querySelectorAll('.field-error')){const k=el.id.slice(7),m=errs.find(([x])=>x===k);el.textContent=m?m[1]:'';
  for(const i of f.querySelectorAll(k==='phones'||k==='emails'?`.pf-list[data-kind="${k}"] input`:`[name="${k}"]`))m?i.setAttribute('aria-invalid','true'):i.removeAttribute('aria-invalid')}
 const first=errs.length&&f.querySelector(`[name="${errs[0][0]}"][aria-invalid]`);if(first){first.focus({preventScroll:true});first.scrollIntoView({block:'center'})}}
// Which field a server message is about.
const personErrField=m=>/^Notes/.test(m)?'notes':/phone/i.test(m)?'phones':/email/i.test(m)?'emails':/Work or Personal/.test(m)?'side':/LinkedIn/.test(m)?'linkedin_url':/^Title/.test(m)?'title':/^Location/.test(m)?'location':/role/i.test(m)?'role':/^org\b|organi[sz]ation/i.test(m)?'org':/name/i.test(m)?'name':'';
// About you: the owner's own record. Their addresses (aliases too) and numbers, never a person in the Graph: a search, a
// New person or an import with one of them comes here. Not shared as a record, so no Keep private.
function aboutYouPage(n){const rows=[...(n.phones||[]).map(x=>kv('Phone',`<a href="tel:${esc(x.value.replace(/[^\d+]/g,''))}">${esc(phoneShown(x.value))}</a>`)),
  ...(n.emails||[]).map(x=>kv('Email',`${breakable(x.value)}${x.by?`<span class="sub">${esc(x.by)}</span>`:''}`))];
 return `<div class="graph-crumbs" role="navigation" aria-label="Breadcrumb"><a href="#graph" data-crumb="">Graph</a><span aria-hidden="true">›</span><span aria-current="page">About you</span></div>`
 +`<article class="graph-detail person-page about-you"><div class="name-row">${personPic({name:n.owner_name||'You'},true)}<div class="person-head"><h3>About you</h3>${n.owner_name?`<p class="person-job">${esc(n.owner_name)}</p>`:''}</div></div>`
 +`<div class="person-view"><p class="graph-sub person-bio">Your own addresses and numbers. They’re always you, never someone in your Graph.</p>${rows.length?`<section class="detail-section person-contact"><h4>Yours</h4>${rows.join('')}</section>`:''}`
 +`<p class="graph-sub role-row"><button type="button" class="link" data-about-addresses>Change them in Settings</button>${n.can_share?'<button type="button" class="ghost" data-contact-share="me">Share my contact</button>':''}</p></div></article>`}
document.addEventListener('click',e=>{if(!e.target.closest('[data-about-addresses]'))return;e.preventDefault();showSettings('account');requestAnimationFrame(()=>$('#settings-addresses')?.scrollIntoView({block:'start'}))});
function personPage(n,group,sub){return `<article class="graph-detail person-page"><div class="name-row">${picEdit(n,personPic(n,true))}<div class="person-head"><h3 title="${esc(n.name)}">${esc(n.name)}</h3>${personJob(n)}</div>${personActions}</div>${personForm(n)}${deleteRow(n)}<div class="person-view">${n.bio?.text?`<p class="graph-sub person-bio" title="${esc('From '+n.bio.from+', '+n.bio.at)}">${esc(n.bio.text)}</p>`:''}${relLine(n)?`<p class="person-rel detail-sub">${esc(relLine(n))}</p>`:''}${notesSection(n.notes)}${personContact(n)}${personAbout(n)}${crmFieldsSection(n)}${detailGroups(n,group)}${fleetAskRow(n)}${sameAsk(n)}${joinedRow(n)}</div></article>`}
const orgSite=n=>{const w=n.profile?.website;return /^https?:\/\/[^\s]+$/.test(w||'')?w:/^[a-z0-9.-]+\.[a-z]{2,}$/i.test(n.domain||'')?'https://'+n.domain:''};
const hostOf=u=>{try{return new URL(u).hostname.replace(/^www\./,'')}catch{return liShort(u)}};
function orgContact(n){const p=n.profile||{},site=orgSite(n),rows=[];
 if(site)rows.push(kv('Website',`<a href="${esc(site)}" target="_blank" rel="noreferrer" title="${esc(site)}">${esc(hostOf(site))} ↗</a>`));
 if(/^https:\/\/([a-z]{2,3}\.)?linkedin\.com\//.test(p.linkedin_url||''))rows.push(kv('LinkedIn',`<a href="${esc(p.linkedin_url)}" target="_blank" rel="noreferrer">${breakable(liShort(p.linkedin_url))} ↗</a>`));
 return rows.length?`<section class="detail-section person-contact"><h4>Contact</h4>${rows.join('')}</section>`:''}
const orgAbout=n=>`<section class="detail-section person-about"><h4>With you</h4>${kv('To you',n.role?`<b>${esc(cap(n.role))}</b>${n.role_by==='review'?`<span class="sub">A review read it in your messages${n.role_quote?`: ${quoteLine(n.id,n.role_quote,n.role_event_id)}`:''}</span>`:''}`:'<span class="muted">Not known yet</span>',n.role_by==='review'?confirmButton(n.id,n.role):'','kv-role')}${graphOwners.length?ownerRow(n):''}</section>`;
const orgRel=n=>[n.signals?t(['{} person','{} people'],n.signals):'',n.last_at?t('last contact {}',day(n.last_at)):''].filter(Boolean).join(' · ');
function orgPage(n,group){const p=n.profile||{};return `<article class="graph-detail person-page org-page"><div class="name-row">${picEdit(n,orgPic(n,true))}<div class="person-head"><h3 title="${esc(n.name)}">${esc(n.name)}</h3>${n.about?`<p class="person-job">${esc(n.about)}</p>`:''}</div>${orgActions(n)}</div>${orgForm(n)}<div class="person-view">${p.about?`<p class="graph-sub person-bio org-about">${esc(p.about)}</p>`:''}${orgRel(n)?`<p class="person-rel detail-sub">${esc(cap(orgRel(n)))}</p>`:''}${orgWrongRow(n)}${orgDoubleAsk(n)}${notesSection(n.profile?.notes)}${orgContact(n)}${orgSites(n)}${orgAbout(n)}${orgProjects(n)}${crmFieldsSection(n)}${detailGroups(n,group)}${fleetAskRow(n)}</div></article>`}
// An organization's projects, open ones first, each with where it stands
const orgProjects=n=>n.projects?.length?`<section class="detail-section org-projects"><h4>Projects</h4><ul>${n.projects.map(p=>`<li${p.open?'':' class="done"'}><button type="button" class="inline-node" data-node="${esc(p.id)}" title="${esc(p.name)}">${esc(p.name)}</button><small class="muted">${esc(p.outcome==='won'?'Won':p.outcome==='lost'?'Lost':p.archived?'Archived':p.stage?p.stage+(p.board?' on '+p.board:''):'No board')}</small></li>`).join('')}</ul></section>`:'';
const deleteRow=n=>n.kind!=='person'?'':`<div class="person-delete"><div class="person-delete-confirm" hidden><p>Delete ${esc(n.name)} and everything The Machine knows about them? This can’t be undone.</p><p class="muted">Won’t be added again.</p><div class="row"><button class="danger-solid" data-person-delete-yes>Delete</button><button class="ghost" data-person-delete-no>Cancel</button></div></div></div>`;
const orgWrongRow=n=>n.wrong?`<p class="graph-sub role-row"><span class="muted">Looked-up details cleared: they were another company’s.</span><button class="ghost" data-org-lookup>Look it up again</button></p>`:'';
const whosWho=(items,total)=>items?.length?`<div class="section-head"><h2>Who’s who</h2><span class="count">${total||items.length}</span><p>Roles your Machine picked up. Confirm or edit; it learns from your edits.</p></div>${items.length>1?`<p class="role-all"><button class="ghost" data-role-all>✓ All ${items.length} are right</button></p>`:''}<div class="graph-list">${items.map(w=>`<article class="whos" data-whos="${esc(w.id)}"><div class="graph-row">${nodeButton(w)}<span class="chip role-chip" style="--c:var(--lavender)"><span class="ell">${esc(w.role)}</span></span></div>${w.quote?`<p class="graph-sub">${quoteLine(w.id,w.quote,w.event_id)}</p>`:''}<p class="graph-sub role-row">${confirmButton(w.id,w.role)}<button class="ghost" data-role-edit-for="${esc(w.id)}">Edit</button></p></article>`).join('')}</div>`:'';
// Same person? The graph joins identities only on strong evidence (the same name on one message, the same LinkedIn
// profile, their number in their own mail); a likely match is a quiet question here and in People: Merge or Not the
// same, which is remembered. Joined identities list why, each with Undo (it splits them for good).
const sameAsk=n=>(n.same||[]).filter(s=>s.name).map(s=>`<div class="same-ask"><p class="graph-sub">Same person as ${nodeButton({id:s.id,name:s.name})}?<br><span class="muted">${esc(sameWhy(s.why))}</span></p><p class="graph-sub role-row"><button data-same="1" data-a="${esc(n.id)}" data-b="${esc(s.id)}">Merge</button><button class="ghost" data-same="0" data-a="${esc(n.id)}" data-b="${esc(s.id)}">Not the same</button></p></div>`).join('');
const joinedRow=n=>n.joined?.length?`<details class="joined"><summary class="graph-sub">Joined from ${n.ids?.length||n.joined.length+1} identities</summary>${n.joined.map(j=>`<div class="graph-sub relation"><span><span class="mono">${esc(j.a_shown)}</span> and <span class="mono">${esc(j.b_shown)}</span> · <span class="muted">${esc(j.why)}</span></span><button class="ghost" data-same="0" data-a="${esc(j.a)}" data-b="${esc(j.b)}" data-split>Undo</button></div>`).join('')}</details>`:'';
const sameList=items=>contactsInList()+(items?.length?`<div class="section-head"><h2>Same person?</h2><span class="count">${items.length}</span>${items.length>1?`<button type="button" class="ghost same-all" data-same-all="${esc(JSON.stringify(items.map(s=>[s.a.id,s.b.id])))}">Merge all</button>`:''}<p>Possible doubles. Merge them or keep them apart.</p></div><div class="graph-list">${items.map(s=>`<article class="same-pair"><div class="graph-row">${personPic(s.a)}${nodeButton(s.a)}<span class="muted">and</span>${personPic(s.b)}${nodeButton(s.b)}</div><p class="graph-sub">${esc(s.why)} · <span class="mono">${esc([s.a.ids?.[0],s.b.ids?.[0]].filter(Boolean).join(', '))}</span></p><p class="graph-sub role-row"><button data-same="1" data-a="${esc(s.a.id)}" data-b="${esc(s.b.id)}">Merge</button><button class="ghost" data-same="0" data-a="${esc(s.a.id)}" data-b="${esc(s.b.id)}">Not the same</button></p></article>`).join('')}</div>`:'');
// Sharing a contact (contact_share.py): from a person's page (⋯, Share contact…) or About you (Share my contact), to one
// teammate, friend or Family member. Pick the fields, look at exactly what goes, then Send. A Personal or private
// contact needs one more tick. Contacts shared here wait under People: Add (or add to the person you have) or Dismiss.
let cs=null,graphContactsIn=[];
const csFields=o=>[...o.emails.map(v=>['emails',v,'Email']),...o.phones.map(v=>['phones',v,'Phone']),...(o.org?[['org',o.org,'Organization']]:[]),...(o.role?[['role',o.role,'Role']]:[])];
const csPick=()=>{const f=$('#contact-share-form'),pick={emails:[],phones:[]};for(const i of f.querySelectorAll('[data-cs-field]:checked')){const k=i.dataset.csField;k==='org'||k==='role'?pick[k]=true:pick[k].push(i.value)}return pick};
const csWhere=t=>t.kind==='work'?`${t.where}`:t.where;
const csLands=k=>k==='work'?'It shows in their Graph, marked shared by you, for them to add or dismiss.':'It shows as a suggestion to add, for them to add or dismiss.';
function csDraw(){const f=$('#contact-share-form'),o=cs.options,t=o.targets,head=`<div class="snooze-heading"><h2 id="contact-share-title">${esc(cs.own?'Share my contact':'Share '+o.name)}</h2><button type="button" data-cs-close aria-label="Close">×</button></div>`;
 if(cs.preview){const p=cs.preview;f.innerHTML=head+`<p class="sp-line">${esc(p.to)} gets exactly this:</p><div class="cs-card">${p.rows.map(r=>kv(esc(r.label),r.label==='Note'?`“${esc(r.value)}”`:esc(r.value))).join('')}</div>`
  +`<p class="fleet-fine">${esc(csLands(p.kind))} Encrypted for their Machine only.</p><p class="ed-note warn" data-cs-error role="alert" hidden></p><div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-cs-back>Back</button><button class="primary">Send</button></div>`;return}
 const sent=(cs.sent||[]).slice(0,3).map(s=>`${s.name}: ${s.state}`).join(' · ');
 f.innerHTML=head+`<label class="ed-field">To<select data-cs-to>${t.map((x,i)=>`<option value="${i}"${i===cs.to?' selected':''}>${esc(x.name)} · ${esc(csWhere(x))}</option>`).join('')}</select></label>`
  +`<fieldset class="sp-people cs-fields"><legend>What goes</legend><label><input type="checkbox" checked disabled> <span class="cs-row"><span class="muted">Name</span><span class="cs-v">${esc(o.name)}</span></span></label>${csFields(o).map(([k,v,l])=>`<label><input type="checkbox" data-cs-field="${k}" value="${esc(v)}"${cs.on.has(k+'|'+v)?' checked':''}> <span class="cs-row"><span class="muted">${l}</span><span class="cs-v">${esc(v)}</span></span></label>`).join('')}</fieldset>`
  +`<label class="ed-field">Why you two should talk <small>(optional)</small><input data-cs-note maxlength="300" value="${esc(cs.note)}" placeholder="You both work on onboarding"></label>`
  +(o.confirm?`<label class="cs-confirm"><input type="checkbox" data-cs-confirm${cs.confirmed?' checked':''}> <span>${o.confirm==='personal'?'This is a Personal contact. Share it anyway.':'You keep this contact private. Share it anyway.'}</span></label>`:'')
  +(sent?`<p class="fleet-fine">Shared before: ${esc(sent)}</p>`:'')
  +`<p class="ed-note warn" data-cs-error role="alert" hidden></p><div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-cs-close>Cancel</button><button class="primary"${o.confirm&&!cs.confirmed?' disabled':''}>Preview</button></div>`}
async function csOpen(source){try{const o=await graphPost('fleet_contact_options',{node:source});if(!o.targets.length){toast('Join a Fleet or add a friend first.',true);return}
 cs={source,own:!!o.own,options:o,sent:o.sent,to:0,note:'',confirmed:false,preview:null,on:new Set(o.emails.slice(0,1).map(v=>'emails|'+v).concat(o.org?['org|'+o.org]:[]))};
 csDraw();const d=$('#contact-share');if(!d.open)d.showModal();d.querySelector('select')?.focus()}catch(e){errCaught(e);toast(e.message,true)}}
function csSync(){const f=$('#contact-share-form');if(!cs||cs.preview)return;cs.to=+f.querySelector('[data-cs-to]').value;cs.note=f.querySelector('[data-cs-note]').value;cs.confirmed=!!f.querySelector('[data-cs-confirm]')?.checked;
 cs.on=new Set([...f.querySelectorAll('[data-cs-field]:checked')].map(i=>i.dataset.csField+'|'+i.value));const b=f.querySelector('button.primary');if(b)b.disabled=!!cs.options.confirm&&!cs.confirmed}
$('#contact-share-form').addEventListener('change',csSync);$('#contact-share-form').addEventListener('input',csSync);
$('#contact-share-form').addEventListener('click',e=>{if(e.target.closest('[data-cs-close]'))$('#contact-share').close();if(e.target.closest('[data-cs-back]')){cs.preview=null;csDraw()}});
$('#contact-share-form').addEventListener('submit',async e=>{e.preventDefault();if(!cs)return;const f=e.currentTarget,btn=f.querySelector('button.primary'),err=f.querySelector('[data-cs-error]'),t=cs.options.targets[cs.to];btn.disabled=true;
 const args={node:cs.source,fleet:t.fleet,member_id:t.member_id,note:cs.note};
 try{if(!cs.preview){cs.pick=csPick();cs.preview=await graphPost('fleet_contact_preview',{...args,pick:cs.pick});csDraw();f.querySelector('button.primary').focus();return}
  const r=await graphPost('fleet_contact_send',{...args,pick:cs.pick,shown:cs.preview.digest,confirmed:cs.confirmed});$('#contact-share').close();toast(`Sent to ${r.to}.`)}
 catch(x){errCaught(x);err.textContent=x.message;err.hidden=false;btn.disabled=false}});
$('#contact-share').addEventListener('close',()=>{cs=null});
document.addEventListener('click',e=>{const b=e.target.closest('[data-contact-share]');if(!b)return;b.closest('details')?.removeAttribute('open');if(b.dataset.contactShare)csOpen(b.dataset.contactShare)});
// On a person's page: Share contact… in ⋯ when someone can get it, and "Shared by" when a share made or joined them.
function contactMarks(view,n){const list=view.querySelector('.person-page .person-menu .fact-menu-list');if(list&&n.can_share&&!list.querySelector('[data-contact-share]')){const item=document.createElement('button');item.type='button';item.setAttribute('role','menuitem');item.dataset.contactShare=n.id;item.textContent='Share contact…';list.prepend(item)}const m=n.shared_by,pv=view.querySelector('.person-page .person-view');
 if(m&&pv&&!pv.querySelector('.person-shared'))pv.insertAdjacentHTML('afterbegin',`<p class="graph-sub person-shared">${m.kind==='work'?'Shared by':'Suggested by'} ${esc(m.by)}${m.note?`: “${esc(m.note)}”`:''}</p>`)}
// Shared with you: at the top of People, until Add or Dismiss.
const contactsInList=()=>graphContactsIn.length?`<div class="section-head"><h2>Shared with you</h2><span class="count">${graphContactsIn.length}</span><p>Contacts sent to you. Add them to your Graph or dismiss them.</p></div><div class="graph-list contacts-in">${graphContactsIn.map(c=>`<article class="contact-in"><div class="graph-row">${personPic({name:c.card.name})}<strong>${esc(c.card.name)}</strong></div>`
 +`<p class="graph-sub">${c.kind==='work'?`Shared by ${esc(c.from)}`:`${esc(c.from)} suggests you add ${c.card.own?'them':'this contact'}`}${c.card.own?' · their own contact':''} · ${esc(c.where)}</p>`
 +`<p class="graph-sub muted">${esc(c.rows.filter(r=>!['Name','Note'].includes(r.label)).map(r=>r.value).join(' · ')||'Name only')}</p>${c.card.note?`<p class="graph-sub">“${esc(c.card.note)}”</p>`:''}`
 +`${c.existing?`<p class="graph-sub muted">You have ${esc(c.existing.name)}. Add puts what’s new on their page.</p>`:''}<p class="graph-sub role-row"><button data-contact-in="add" data-id="${esc(c.id)}">Add</button><button class="ghost" data-contact-in="dismiss" data-id="${esc(c.id)}">Dismiss</button></p></article>`).join('')}</div>`:'';
document.addEventListener('click',async e=>{const b=e.target.closest('[data-contact-in]');if(!b)return;b.disabled=true;try{const r=await graphPost('fleet_contact_decide',{id:b.dataset.id,choice:b.dataset.contactIn});
 graphContactsIn=graphContactsIn.filter(c=>c.id!==b.dataset.id);toast(r.status==='dismissed'?'Dismissed.':r.status==='merged'?`Added to ${r.name}.`:`Added ${r.name}.`);await people(graphNode,true)}catch(x){errCaught(x);b.disabled=false;toast(x.message,true)}});
// Domains a review read as an email warm-up tool's traffic: out of the graph, listed here with Undo.
const warmupList=items=>items?.length?`<details class="warmup"><summary class="graph-sub">Hidden as warm-up (${items.length})</summary><p class="graph-sub muted">Mail from email warm-up tools, kept out of your Graph.</p>${items.map(w=>`<div class="graph-sub relation"><span>${esc(w.name||w.domain)}${w.name&&w.name!==w.domain?` <span class="muted">${esc(w.domain)}</span>`:''}</span><button class="ghost" data-warmup-undo="${esc(w.domain)}">Undo</button></div>`).join('')}</details>`:'';
const openBetween=n=>{const o=n.open||{},row=(label,p)=>`<div class="promise"><span class="grow">${label}: <a class="promise-link" href="${promiseHref(p)}">${esc(p.what)}</a>${p.due?`<small>due ${esc(day(p.due))}</small>`:''}</span><button data-promise="${p.id}" data-close="kept">Done</button><button class="ghost" data-promise="${p.id}" data-close="dropped">Drop</button></div>`;
 const rows=[...(o.you_promised||[]).map(p=>row('You promised',p)),...(o.they_promised||[]).map(p=>row(n.kind==='person'?'They promised':esc(p.who)+' promised',p)),
  ...(o.cards||[]).map(c=>`<div class="promise"><span class="grow">To-do: <a href="#card=${esc(c.id)}" translate="no">${esc(c.title)}</a>${c.due?`<small>due ${esc(day(c.due))}</small>`:''}</span></div>`)];
 return rows.length?`<div class="section-head"><h2>Open between you</h2><span class="count">${rows.length}</span></div><article class="graph-open">${rows.join('')}</article>`:''};
// What the owner told that is about them (a fact's subject, never who sent the message it came up in), quietly, each
// with a menu: Not about them takes only this link away, Forget deletes the fact everywhere.
const shortName=n=>n.kind==='person'?String(n.name||'').split(/\s+/)[0]||n.name:n.name;
const knownAbout=n=>{const k=n.open?.known||[],who=esc(shortName(n));return k.length?`<div class="section-head graph-known-head"><h2>Known about ${who}</h2></div><ul class="graph-known">${k.map(f=>`<li><span>${esc(f.text)}</span><details class="fact-menu"><summary aria-label="Options for this fact" title="Options">⋯</summary><div class="fact-menu-list" role="menu"><button type="button" role="menuitem" data-fact-unlink="${f.id}">Not about ${who}<small>Only takes it off this page</small></button><button type="button" role="menuitem" class="danger" data-fact-forget="${f.id}" data-who="${who}">Forget<small>Deletes it everywhere</small></button></div></details></li>`).join('')}</ul>`:''};
// The timeline on a person, project or organization: every source in one list by day, each row its source, who wrote it,
// when, and the start of the text; cards, promises and project moves among them. Filter by source; Show more loads more.
const GRAPH_SOURCE={docs:'<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/>',intercom:'<path d="M5 5h14v10H9l-4 4z"/>',zoom:'<rect x="3" y="7" width="12" height="10" rx="2"/><path d="m15 11 6-3v8l-6-3z"/>',
 telegram:'<path d="m3 11 18-7-3 16-6-5-3 4v-6z"/>',card:'<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 9h8M8 13h5"/>',
 promise:'<path d="m5 12 4 4 10-10"/>',move:'<path d="M4 12h14M13 6l6 6-6 6"/>'};
const graphSource=k=>k==='salesflare.email'?'gmail':k==='salesflare.meeting'?'calendar':kindService(k);
const sourceIcon=(k,type)=>{const s=type&&type!=='event'?type:graphSource(k);return GRAPH_SOURCE[s]?`<span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24">${GRAPH_SOURCE[s]}</svg></span>`:icon(s)};
const SOURCE_NAME={gmail:'Email',salesflare:'Email',calendar:'Calendar',whatsapp:'WhatsApp',slack:'Slack',intercom:'Intercom',linkedin:'LinkedIn',android:'Phone',x:'X',github:'GitHub',stripe:'Stripe',zoom:'Zoom',telegram:'Telegram',docs:'Docs'};
const TL_SOURCES={email:'Email',meetings:'Meetings',intercom:'Intercom',chats:'Chats',cards:'To-dos',projects:'Projects',other:'Other'};
const dayLabel=d=>{const t=new Date(),y=new Date(t),m=new Date(t);y.setDate(t.getDate()-1);m.setDate(t.getDate()+1);const same=(a,b)=>a.toDateString()===b.toDateString();return same(d,t)?'Today':same(d,y)?'Yesterday':same(d,m)?'Tomorrow':d.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short',...(d.getFullYear()!==t.getFullYear()?{year:'numeric'}:{})})};
// A run of chat messages in one conversation (same thread, same day, under half an hour apart) is one row.
const GRAPH_GAP=30*6e4,GRAPH_ROWS=15;
const graphRuns=rows=>{const out=[];for(const e of rows){const run=out[out.length-1],prev=run?.at(-1);
  if(e.thread&&prev?.thread===e.thread&&new Date(prev.occurred_at).toDateString()===new Date(e.occurred_at).toDateString()&&Math.abs(Date.parse(prev.occurred_at)-Date.parse(e.occurred_at))<GRAPH_GAP)run.push(e);else out.push([e])}return out};
const graphTime=d=>fmtHM(d);
// The page's timeline as loaded so far: its source filter, the rows shown and the cursor of the next page.
let graphTl={node:'',source:'',shown:GRAPH_ROWS,next:null,sources:null,items:null,loading:false};
const PROMISE_STATE={open:'Open',carded:'Open',kept:'Done',dropped:'Dropped',answered:'Done'};
const tlRow=(n,e,later)=>{const d=new Date(e.occurred_at),t=`<time datetime="${esc(e.occurred_at)}">${esc(graphTime(d))}</time>`,mark=(label,c)=>`<span class="chip ge-state" style="--c:var(${c})">${esc(label)}</span>`;
 if(e.type==='card')return `<article class="graph-event ge-item" data-tl="card" tabindex="0" aria-label="To-do: ${esc(e.title)}"${later}>${sourceIcon('',e.type)}<div class="ge-main"><div class="ge-head"><h4 title="${esc(e.title)}" translate="no"><a href="#card=${esc(e.id)}">${esc(e.title)}</a></h4>${mark(e.done?'Done':'Open',e.done?'--faint':'--mint')}${t}</div><p class="ge-preview">To-do</p></div></article>`;
 if(e.type==='promise'){const who=e.mine?'You promised':n.kind==='person'?'They promised':`${shortName({kind:'person',name:e.who})||'They'} promised`;
  return `<article class="graph-event ge-item" data-tl="promise" tabindex="0" aria-label="${esc(who)}: ${esc(e.what)}"${later}>${sourceIcon('',e.type)}<div class="ge-main"><div class="ge-head"><h4>${esc(who)}</h4>${mark(PROMISE_STATE[e.status]||'Open',PROMISE_STATE[e.status]==='Open'||!PROMISE_STATE[e.status]?'--mint':'--faint')}${t}</div><p class="ge-preview"><a class="promise-link" href="${promiseHref(e)}">${esc(e.what)}</a></p></div></article>`}
 if(e.type==='move')return `<article class="graph-event ge-item" data-tl="move" tabindex="0" aria-label="${esc(e.project)}: ${esc(e.stage)}"${later}>${sourceIcon('',e.type)}<div class="ge-main"><div class="ge-head"><h4 title="${esc(e.project)}"><a href="${graphHash(e.project_id)}">${esc(e.project)}</a></h4>${t}</div><p class="ge-preview">Moved to ${esc(e.stage)}</p></div></article>`;
 return ''};
const tlLink=e=>/^docs\./.test(e.kind||'')&&e.source_url?`<a class="ge-link" href="${esc(e.source_url)}" target="_blank" rel="noopener">Open the doc</a>`:e.kind==='intercom.conversation'&&e.source_url?`<a class="ge-link" href="${esc(e.source_url)}" target="_blank" rel="noopener">Open in Intercom</a>`:e.kind==='zoom.summary'&&e.source_url?`<a class="ge-link" href="${esc(e.source_url)}" target="_blank" rel="noopener">Summary</a>`:'';
// A meeting opens in its details (openMeeting); one with notes or a transcript says so on its row
const meetingAttr=e=>e.kind==='calendar.event'?' data-meeting':e.meeting_id?` data-meeting="${esc(e.meeting_id)}"`:'';
const meetingMarks=e=>e.kind==='calendar.event'?[e.notes&&'Notes',e.transcript&&'Transcript'].filter(Boolean).map(x=>`<span class="chip ge-mark">${esc(t(x))}</span>`).join(''):'';
// A meeting still to come, compact: its day and time (All day for an all-day one), who else is on it.
const GE_SOON=3;
const soonRow=(n,e,later)=>{if(e.type&&e.type!=='event')return tlRow(n,e,later);const d=new Date(e.occurred_at),src=SOURCE_NAME[graphSource(e.kind)]||'';
 return `<article class="graph-event" data-event="${e.id}"${meetingAttr(e)} tabindex="0" aria-label="${esc(src?t(src)+': ':'')}${esc(e.title)}"${later}>${sourceIcon(e.kind)}<div class="ge-main"><div class="ge-head"><h4 title="${esc(e.title)}" translate="no">${esc(e.title)}</h4><time datetime="${esc(e.occurred_at)}">${esc(dayLabel(d)+' · '+(e.all_day?'All day':graphTime(d)))}</time></div>${e.preview||meetingMarks(e)?`<p class="ge-preview">${meetingMarks(e)}${esc(e.preview||'')}</p>`:''}</div></article>`};
const graphEvents=(n,title='Timeline')=>{const soon=Date.now(),tl=n.timeline,all=[...(n.recent||[]).map(e=>e.occurred_at?e:{...e,occurred_at:e.at}),...(tl?.source?[]:(n.changes||[]).map(c=>({change:changeText(c),occurred_at:c.at})))].sort((a,b)=>Date.parse(b.occurred_at)-Date.parse(a.occurred_at)).filter(e=>!(Date.parse(e.occurred_at)>soon));
 /* Coming up apart, soonest first; the timeline itself strictly back in time from now */
 const up=[...(tl?.upcoming||[]),...(n.recent||[]).filter(e=>Date.parse(e.occurred_at||e.at)>soon&&!(tl?.upcoming||[]).some(u=>u.id===e.id))].map(e=>e.occurred_at?e:{...e,occurred_at:e.at}).sort((a,b)=>Date.parse(a.occurred_at)-Date.parse(b.occurred_at));
 const chips=tl?.sources&&Object.keys(tl.sources).length>1?subTabs('Show','data-tl-source',[{id:'',label:'All'},...Object.keys(TL_SOURCES).filter(k=>tl.sources[k]).map(k=>({id:k,label:TL_SOURCES[k]}))],tl.source||''):'';
 const head=count=>`<div class="section-head"><h2>${esc(title)}</h2>${count?`<span class="count">${count}</span>`:''}</div>`;
 const soonBox=up.length?`<div class="ge-soon"><h3 class="ge-day">Coming up</h3><div class="ge-group">${up.map((e,i)=>soonRow(n,e,i>=GE_SOON?' hidden':'')).join('')}</div>${up.length>GE_SOON?'<button type="button" class="ghost ge-more" data-ge-soon>Show all upcoming</button>':''}</div>`:'';
 if(!all.length)return tl||up.length?`<section class="graph-timeline">${head(0)}${chips}${soonBox}${all.length||up.length?'':'<p class="graph-sub muted ge-empty">Nothing here yet.</p>'}</section>`:'';
 let last='',h='';const shown=tl?Math.max(GRAPH_ROWS,tl.shown||0):GRAPH_ROWS;
 const runs=graphRuns(all);
 runs.forEach((run,i)=>{const e=run[0],d=new Date(e.occurred_at),label=dayLabel(d),later=i>=shown?' hidden':'';
  if(label!==last){h+=(last?'</div>':'')+`<h3 class="ge-day"${later}>${esc(label)}</h3><div class="ge-group">`;last=label}
  if(e.change){h+=`<article class="graph-event ge-change"${later}><span class="ge-dot" aria-hidden="true">•</span><div class="ge-main"><div class="ge-head"><h4>${esc(e.change)}</h4><time datetime="${esc(e.occurred_at)}">${esc(graphTime(d))}</time></div></div></article>`;return}
  if(e.type&&e.type!=='event'){h+=tlRow(n,e,later);return}
  const chat=e.dm||e.title===n.name&&e.from,src=SOURCE_NAME[graphSource(e.kind)]||'';
  if(e.thread&&(run.length>1||chat||e.title!==n.name)){  /* a conversation, newest first: e is the last message, run.at(-1) the first */
   const first=new Date(run.at(-1).occurred_at),many=run.length>1,span=graphTime(first)===graphTime(d)?graphTime(d):rangeText(graphTime(first),graphTime(d));
   const own=chat&&!e.place&&n.kind==='person';  /* one to one with this page's person: no title, the page says who */
   const with_=t('{} with {} (a chat)',t(src||'Chat'),shortName(n.kind==='person'?n:{kind:'person',name:e.from_me?run.find(m=>!m.from_me)?.from||e.title:e.from||e.title})),head=e.place||(chat?with_:e.title);
   const said=m=>`<b>${esc(m.from_me?'You':shortName({kind:'person',name:m.from||(n.kind==='person'?n.name:'')})||'Them')}: </b>${esc(m.preview||'')}`,lines=run.slice(0,2).reverse().map(m=>`<li>${said(m)}</li>`).join('');
   const meta=`<span class="ge-meta"><time datetime="${esc(first.toISOString())}">${many?`${run.length} messages · `:''}${esc(span)}</time></span>`;
   h+=`<article class="graph-event" data-event="${e.id}"${many?` data-events="${run.map(m=>m.id).reverse().join(',')}" data-title="${esc(head)}" data-src="${esc(src)}"${own?'':' data-group'}`:''} tabindex="0" aria-label="${esc(own?with_:(src?t(src)+': ':'')+t(head))}${many?', '+esc(t(['{} message','{} messages'],run.length)):''}"${later}>${sourceIcon(e.kind)}<div class="ge-main"><div class="ge-head">${own?'':`<h4 title="${esc(e.title)}">${esc(head)}</h4>`}${meta}${shareChip(e)}</div>${many?`<ul class="ge-lines">${lines}</ul>`:e.preview?`<p class="ge-preview">${said(e)}</p>`:''}${run.some(m=>m.probable)?'<p class="ge-note">Probably part of it</p>':''}</div></article>`;return}
  const head=e.place||(chat?(e.from_me?'You':e.from||(n.kind==='person'?n.name:e.title)):e.title);
  const by=!chat&&e.from&&!['calendar.event','zoom.summary','meeting.notes'].includes(e.kind)?(e.from_me?'You':e.from)+': ':'';
  const state=e.state?`<span class="chip ge-state" style="--c:var(${e.state==='open'?'--mint':'--faint'})">${e.state==='open'?'Open':'Closed'}</span>`:'';
  h+=`<article class="graph-event" data-event="${e.id}"${meetingAttr(e)} tabindex="0" aria-label="${esc(src?t(src)+': ':'')}${esc(t(head))}"${later}>${sourceIcon(e.kind)}<div class="ge-main"><div class="ge-head"><h4 title="${esc(e.title)}">${esc(head)}</h4>${state}<time datetime="${esc(e.occurred_at)}">${esc(e.all_day?'All day':graphTime(d))}</time>${shareChip(e)}</div>${e.preview||meetingMarks(e)?`<p class="ge-preview">${meetingMarks(e)}${by?`<b>${esc(by)}</b>`:''}${esc(e.preview||'')}</p>`:''}${tlLink(e)?`<p class="ge-note">${tlLink(e)}</p>`:''}${e.probable?'<p class="ge-note">Probably part of it</p>':''}</div></article>`});
 const more=runs.length>shown||tl?.next;
 return `<section class="graph-timeline">${head(tl?(tl.source?tl.sources?.[tl.source]:tl.total)||runs.length:runs.length)}${chips}${soonBox}<div class="graph-events">${h}</div></div>${more?'<button type="button" class="ghost ge-more" data-ge-more>Show more</button>':''}</section>`};
// Show more: the rows already here first, then the next page; a source chip reloads the list for that source.
async function graphTlLoad(source,more){const n=graphTl.page;if(!n||graphTl.loading)return;graphTl.loading=true;
 try{const tl=n.timeline||{};const cursor=more?tl.next:'';const got=await request('api/graph/timeline?node='+encodeURIComponent(n.id)+'&source='+encodeURIComponent(source)+(cursor?'&cursor='+encodeURIComponent(cursor):''));
  if(graphTl.page!==n)return;n.recent=more?[...n.recent,...got.items]:got.items;n.timeline={...tl,next:got.next,sources:got.sources,total:got.total,upcoming:more?tl.upcoming:(got.upcoming||[]),source,shown:more?(tl.shown||GRAPH_ROWS)+30:GRAPH_ROWS};graphTlDraw()}
 catch(err){errCaught(err);toast(err.message,true)}finally{graphTl.loading=false}}
function graphTlDraw(){const box=$('#people-view .graph-timeline'),n=graphTl.page;if(!box||!n)return;const tmp=document.createElement('div');tmp.innerHTML=graphEvents(n);box.replaceWith(tmp.firstElementChild);
 for(const p of $('#people-view').querySelectorAll('.graph-timeline .ge-preview'))p.classList.toggle('fade',p.scrollHeight>p.clientHeight+1)}
// The Shared Graph (shared_graph.py): Mine or Team, "via <name>", a thread's Team or Only you, Keep private and Ask <name>.
// Teammates' records and threads are theirs, shown as text, never acted on. Nothing here goes outside the Fleet.
let graphTeam=sideStore.get('graph-team')==='team',graphSharing=[],graphTeammates=[];
const teamOn=()=>graphSharing.some(s=>s.confirmed);
const teamMode=()=>teamOn()&&graphTeam;
const shareChip=e=>{const s=e.share;if(!s)return '';const t=s.share==='team'?'Team':s.people?.length?s.people[0]+(s.people.length>1?' +'+(s.people.length-1):''):'Only you';
 return `<button type="button" class="share-chip${s.share==='team'||s.people?.length?' on':''}" data-share-event="${e.id}" data-share="${esc(JSON.stringify({share:s.share,fixed:!!s.fixed,why:s.why||'',people:s.people||[]}))}" title="${esc(s.why)}" aria-haspopup="dialog" aria-label="${t}: ${esc(s.why)}">${t}</button>`};
const shareNote=list=>(list||[]).filter(s=>s.confirmed).map(s=>`<p class="share-note muted">${s.off==='off'?`Your Work isn't shared with ${esc(s.name)} now.`:s.teammates===0?`Sharing starts once ${s.admin?'you OK':'an admin OKs'} a teammate's Machine. Personal never.`:!s.started?`Work goes to ${esc(s.name)} within the hour. Personal never.`:`Work is shared with ${esc(s.name)}. Personal never.`} <a href="#shared=${esc(s.fleet)}">See what's shared</a></p>`).join('');
const privateRow=n=>n.keep_private===undefined||n.team_only?'':`<div class="keep-private"><button type="button" class="ghost" data-keep-private="${esc(n.id)}" data-private="${n.keep_private?'0':'1'}">${n.keep_private?'Share with the team again':'Keep private'}</button><small class="muted">${n.keep_private?'Only you see this and its threads.':n.shared_with_team?'Shared with your team.':'Not shared with your team yet.'}</small></div>`;
const askForm=(p,about)=>`<details class="team-ask"><summary>Ask ${esc(p.name||'them')}</summary><form class="team-ask-form" data-fleet="${esc(p.fleet)}" data-member="${esc(p.member)}" data-about="${esc(about)}"><textarea name="note" rows="2" maxlength="1000" aria-label="What to ask ${esc(p.name||'them')}">Can you tell me where things stand with ${esc(about)}?</textarea><button class="primary">Ask</button></form></details>`;
function teamBlock(n){const t=n.team;if(!t)return '';
 const people=t.people.filter(p=>!p.left);
 const lines=t.timeline.map(x=>`<li><span>${esc(x.line)}</span><small class="muted">${esc(shortDay(x.at))} · ${esc(x.via)}</small></li>`).join('');
 const threads=t.threads.map(x=>`<details class="team-thread" data-team-thread="${esc(x.id)}"><summary><span class="tt"><span class="ell">${esc(x.subject||'(no subject)')}</span><small class="muted">${x.kind==='meetings'?'Meeting':`${{intercom:'Intercom · ',chats:'Chat · '}[x.kind]||''}${x.messages} message${x.messages===1?'':'s'}`} · ${esc(shortDay(x.at))} · ${esc(x.via)}</small></span></summary><div class="team-thread-body"></div></details>`).join('');
 return `<section class="team-block"><div class="section-head"><h2>From the team</h2><p>${esc(t.via)}</p></div>${lines?`<ul class="team-lines">${lines}</ul>`:''}${threads?`<div class="team-threads">${threads}</div>`:''}${people.length?`<div class="team-asks">${people.slice(0,3).map(p=>askForm(p,n.name)).join('')}</div>`:''}</section>`}
const teamDetail=n=>{const [paneId,paneName]=GRAPH_KIND_PANE[n.kind]||GRAPH_KIND_PANE.person;
 const sub=[n.role&&t(cap(n.role)),n.org_name,n.kind==='project'&&n.stage?n.board+': '+t(n.stage):'',n.last_at?t('last contact {}',day(n.last_at)):''].filter(Boolean).join(' · ');
 return `<div class="graph-crumbs" role="navigation" aria-label="Breadcrumb"><a href="#graph" data-crumb="">Graph</a><span aria-hidden="true">›</span><a href="#graph=${paneId}" data-crumb="${paneId}">${paneName}</a><span aria-hidden="true">›</span><span aria-current="page">${esc(n.name)}</span></div><article class="graph-detail"><div class="name-row"><h3>${esc(n.name)}</h3></div><p class="graph-sub">${esc(sub)}</p>${n.next?`<p class="graph-sub">Next: ${esc(n.next)}</p>`:''}${crmFieldsSection(n)}</article>`+teamBlock(n)};
const heldPane=items=>items?.length?`<div class="section-head"><h2>Held back this week</h2><span class="count">${items.length}</span><p>Your team sees only that these exist, or nothing.</p></div><div class="graph-list">${items.map(x=>`<article class="held-row"><div class="graph-row"><span class="ell" title="${esc(x.title)}">${esc(x.title||'(no subject)')}</span>${shareChip({id:x.event_id,share:{share:'only_you',fixed:false,why:x.why}})}</div><p class="graph-sub">${esc([x.with,shortDay(x.at),x.why].filter(Boolean).join(' · '))}</p></article>`).join('')}</div>`:'<div class="empty all-clear"><div><strong>Nothing held back this week.</strong>Work went to your team as usual.</div></div>';
$('#people-view').addEventListener('click',async e=>{
 const chip=e.target.closest('[data-share-event]');if(chip){e.stopPropagation();e.preventDefault();if($('#share-pop')?.dataset.for===chip.dataset.shareEvent)return sharePopClose();sharePop(chip);$('#share-pop').dataset.for=chip.dataset.shareEvent;return}
 const kp=e.target.closest('[data-keep-private]');if(kp){kp.disabled=true;const on=kp.dataset.private==='1';try{await graphPost('graph_private',{node_id:kp.dataset.keepPrivate,private:on});toast(on?'Kept private.':'Shared with your team again.');await people(graphNode,true)}catch(err){errCaught(err);kp.disabled=false;toast(err.message,true)}return}
},true);
$('#people-view').addEventListener('toggle',async e=>{const d=e.target;if(!d.matches?.('[data-team-thread]')||!d.open||d.dataset.loaded)return;d.dataset.loaded='1';const body=d.querySelector('.team-thread-body');
 try{const t=await request('api/graph?thread='+encodeURIComponent(d.dataset.teamThread));
  body.innerHTML=(t.messages||[]).map(m=>`<div class="team-msg"><p class="muted">${esc(m.from||'')} · ${esc(shortDay(m.at))}</p><p class="team-msg-text">${esc(m.body||'')}</p>${m.attachments?.length?`<ul class="team-files">${m.attachments.map(x=>`<li>${x.file&&!x.waiting?`<a href="api/team-file?thread=${encodeURIComponent(d.dataset.teamThread)}&file=${esc(x.file)}" download>${esc(x.name)}</a>`:`<span>${esc(x.name)}</span>`}<small class="muted">${x.not_shared?'not shared (Careful)':x.too_large?'too large to share':x.waiting?'on its way':fileSize(x.size)}</small></li>`).join('')}</ul>`:''}</div>`).join('')||'<p class="muted">Empty.</p>'}catch(err){errCaught(err);body.innerHTML=`<p class="muted">${esc(err.message)}</p>`;delete d.dataset.loaded}},true);
$('#people-view').addEventListener('submit',async e=>{const f=e.target.closest('.team-ask-form');if(!f)return;e.preventDefault();e.stopPropagation();const b=f.querySelector('button');b.disabled=true;
 try{await graphPost('graph_ask',{fleet:f.dataset.fleet,member_id:f.dataset.member,about:f.dataset.about,note:f.elements.note.value});toast('Asked.');f.closest('details').open=false}catch(err){errCaught(err);toast(err.message,true)}finally{b.disabled=false}},true);
$('#page-head').addEventListener('click',e=>{const b=e.target.closest('[data-graph-team]');if(!b)return;graphTeam=b.dataset.graphTeam==='team';sideStore.set('graph-team',graphTeam?'team':'mine');pageHead();people('')});
// A promise's own page (#promise/<id>), laid out like a person's: who promised what to whom and by when, where it
// stands, the message it came from, who and what it is about, its card as a link, and what happened since.
const promiseHref=p=>'#promise/'+encodeURIComponent(p.id);
const promiseFirst=who=>String(who||'').split(/\s+/)[0]||who;
const PROMISE_SAID={'gmail.message':'an email','slack.message':'Slack','whatsapp.message':'WhatsApp','telegram.message':'Telegram','linkedin.message':'LinkedIn','x.message':'X','intercom.message':'Intercom','calendar.event':'a meeting'};
function promiseState(p){const late=p.due&&p.due<localDay(new Date());
 return p.state==='open'?(p.direction==='theirs'&&!p.together?['Waiting on '+promiseFirst(p.who),'var(--lavender)']:[late?'Past its date':'Open',late?'var(--orange)':'var(--mint)']):p.state==='card'?['Now a to-do','var(--amber)']
  :p.state==='kept'?['Kept','var(--muted)']:p.state==='answered'?['They wrote again','var(--muted)']:['Not needed','var(--muted)']}
function promiseLine(p,h){const via=PROMISE_SAID[h.detail]||'a message';
 return {said:p.together?t('Planned together in {}',via):p.direction==='mine'?t('Promised to {} in {}',p.who,via):t('{} promised it in {}',p.who,via),noted:'Noted by a review',due:t('Date moved to {}',day(h.detail)),
  kept:'Marked done',dropped:'Marked not needed',answered:'They wrote again',carded:'Became a to-do',together:'Both sides said it: one plan',merged:'The same as another promise'}[h.kind]||''}
async function promisePage(id){const p=await request('api/promise?id='+encodeURIComponent(id)),[state,color]=promiseState(p),person=(p.links||[]).find(l=>l.kind==='person');
 const who=p.together?'With '+p.who:p.direction==='mine'?'Promised to '+p.who:p.who+' promised',when=p.due?'due '+day(p.due):'no date';
 const actions=p.state==='open'?`<div class="promise-actions"><button class="ghost" data-promise="${p.id}" data-close="kept">Done</button><button class="ghost" data-promise-due>Change date</button><button class="ghost" data-promise="${p.id}" data-close="dropped">Not needed</button></div><form class="promise-due-form" data-promise-id="${p.id}" hidden><input type="date" name="due" value="${esc(p.due||'')}" aria-label="New date" required><button>Save</button></form>`:'';
 const note=p.state!=='open'&&p.note&&!/\(you\)$/.test(p.note)?`<p class="graph-sub muted">${esc(p.note)}</p>`:'';
 const src=p.source?.[0],from=src?graphEvents({recent:p.source,name:p.who,kind:'promise'},'Came from').replace(/<span class="count">\d+<\/span>/,''):'';
 const open=src&&/^https:\/\//.test(src.source_url||'')?`<p class="graph-sub"><a href="${esc(src.source_url)}" target="_blank" rel="noreferrer">Open in ${esc(SOURCE_NAME[graphSource(src.kind)]||'its app')} ↗</a></p>`:'';
 const kinds=[['person','People'],['org','Organization'],['project','Project']].map(([k,t])=>[t,(p.links||[]).filter(l=>l.kind===k)]).filter(([,l])=>l.length);
 const about=kinds.length?`<div class="section-head"><h2>About</h2></div><div class="promise-about">${kinds.map(([t,l])=>`<p class="graph-sub"><span class="muted">${t}</span> ${l.map(nodeButton).join('')}</p>`).join('')}</div>`:'';
 const card=p.card?`<div class="section-head"><h2>To-do</h2></div><p class="graph-sub promise-card"><a href="#card=${esc(p.card.id)}">${esc(p.card.title)}</a></p>`:'';
 const hist=p.history.map(h=>[promiseLine(p,h),h.at]).filter(([t])=>t);
 return `<div class="graph-crumbs" role="navigation" aria-label="Breadcrumb">${person?`<a href="${graphHash(person.id)}" data-node="${esc(person.id)}">${esc(person.name)}</a>`:'<a href="#graph" data-crumb="">Graph</a>'}<span aria-hidden="true">›</span><span aria-current="page">Promise</span></div>`+
  `<article class="graph-detail person-page promise-page"><div class="name-row"><div class="person-head"><h3>${esc(cap(p.what))}</h3><p class="person-job">${esc(who)} · ${esc(when)}</p></div></div>`+
  `<p class="graph-sub promise-state"><span class="chip" style="--c:${color}">${esc(state)}</span></p>${note}${actions}${from}${open}${about}${card}`+
  (hist.length?`<div class="section-head"><h2>History</h2></div><ul class="promise-history">${hist.map(([t,at])=>`<li><span>${esc(t)}</span><time datetime="${esc(at)}">${esc(day(at))}</time></li>`).join('')}</ul>`:'')+'</article>'}
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
const subTabs=(label,attr,panes,current)=>`<div class="sub-tabs" role="tablist" aria-label="${esc(label)}">${panes.map(p=>`<button type="button" role="tab" ${attr}="${esc(p.id)}" aria-selected="${p.id===current}"><span class="ell">${esc(p.label)}</span>${p.badge?` <span class="badge${p.warn?' warn':''}">${p.badge}</span>`:''}</button>`).join('')}</div>`;
function tabsFade(row){const max=row.scrollWidth-row.clientWidth;row.classList.toggle('more-left',row.scrollLeft>2);row.classList.toggle('more-right',row.scrollLeft<max-2)}
function tabsShow(row){if(!row)return;const t=row.querySelector('[aria-selected="true"]');if(t&&row.scrollWidth>row.clientWidth)row.scrollLeft=Math.max(0,t.offsetLeft-row.offsetLeft-(row.clientWidth-t.offsetWidth)/2);tabsFade(row)}
const allTabsFade=()=>document.querySelectorAll('.fleet-tabs,.sub-tabs').forEach(tabsFade);
document.addEventListener('scroll',e=>{if(e.target.matches?.('.fleet-tabs,.sub-tabs'))tabsFade(e.target)},{capture:true,passive:true});addEventListener('resize',allTabsFade);
new MutationObserver(()=>document.querySelectorAll(':is(.fleet-tabs,.sub-tabs):not([data-faded])').forEach(r=>{r.dataset.faded='';tabsShow(r)})).observe(document.querySelector('main'),{childList:true,subtree:true});
// Graph: People (closest, gone quiet, new), Who's who (roles to confirm), Projects and Organizations.
const GRAPH_PANES=['people','roles','projects','orgs'];
function showGraphPane(id){graphPane=id;localStorage.setItem('graph-pane',id);graphShown=id;graphHashSync();graphSubSync();const view=$('#people-view');if(!view.querySelector(`[data-graph-panel="${CSS.escape(id)}"]`)){if(!graphNode&&!$('#people-query').value.trim())return;$('#people-query').value='';people('');return}
 for(const b of view.querySelectorAll('[data-graph-pane]'))b.setAttribute('aria-selected',b.dataset.graphPane===id);for(const p of view.querySelectorAll('[data-graph-panel]'))p.hidden=p.dataset.graphPanel!==id;tabsShow(view.querySelector('.sub-tabs'));tabsShow(view.querySelector(`[data-graph-panel="${CSS.escape(id)}"] .sub-tabs`))}
async function people(node=graphNode,quiet=false){const was=graphNode;graphNode=node;if(was!==node&&!$('#people').hidden)graphSubSync();  /* the head names the page's section; + New … is for the lists, not a page */const version=++graphRequest,view=$('#people-view'),oldHtml=view.innerHTML;const draw=(html,mode='list')=>{if(version!==graphRequest||quiet&&([...view.querySelectorAll('form:not([hidden])')].some(f=>f.checkVisibility())||view.querySelector('.team-thread[open],.tile-menu[open],.tile.dragging,.tile:active,.lane.drop,.board-menu[open],.graph-sort[open],.tag-add input:focus')))return;  /* a refresh never closes what the owner is typing or reading */const back=quiet&&foldsKeep(view);view.innerHTML=html;view.dataset.mode=mode;pagerMount(view);if(back)back();if(graphDrawn!==graphNode){graphDrawn=graphNode;if(!$('#people').hidden)pageHead()}};  /* the head changes with the page it names, not before it has loaded */  /* the rows a list already loaded come with it, so the page keeps its height and the reader keeps their place (placeKeep) */try{
 if(node&&/^promise:\d+$/.test(node)){const html=await promisePage(node.slice(8));draw(html,'node');if(version!==graphRequest)return;graphKept=null;$('#people').classList.add('graph-on-node');pageHead();if(!quiet)scrollTo({top:0});return}
 if(node){let n;try{n=await request('api/graph?node='+encodeURIComponent(node))}catch(e){errCaught(e);if(version!==graphRequest||quiet&&oldHtml)return;  /* a page that didn't load says so, with Try again; a quiet refresh keeps what is shown */
   draw('<div class="empty graph-load-failed" role="alert"><div><strong>Couldn’t load this page.</strong></div><button type="button" data-graph-retry>Try again</button></div>','node');$('#people').classList.add('graph-on-node');return}
  if(n.owners)graphOwners=n.owners;if(n.timeline){const was=graphTl.page;if(quiet&&was?.id===n.id&&was.timeline?.source){n.recent=was.recent;n.timeline={...n.timeline,...was.timeline}}else n.timeline.shown=GRAPH_ROWS;graphTl.page=n}const group=k=>n.links.filter(l=>l.kind===k&&l.id!==n.org);
  if(n.team_only){draw(teamDetail(n));if(version!==graphRequest)return;$('#people').classList.add('graph-on-node');if(!quiet)scrollTo({top:0});return}
  if(n.kind==='me'){graphNode='me';draw(aboutYouPage(n),'node');if(version!==graphRequest)return;graphKept=null;docTitle();$('#people').classList.add('graph-on-node');if(location.hash!==graphHash('me')&&!$('#people').hidden)history.replaceState(null,'',graphHash('me'));if(!quiet)scrollTo({top:0});return}
  const sub=n.kind==='person'?personSub({...n,role:null,profile:null})+(n.quiet?' · '+t('gone quiet'):''):n.kind==='project'?(heatLabel(n.state)+' · '+t('last signal {}',day(n.last_at))+(n.probable_signals?' · '+t('{} probably part of it',n.probable_signals):'')):(t(['{} person','{} people'],n.signals)+' · '+t('last contact {}',day(n.last_at)));
  const [paneId,paneName]=GRAPH_KIND_PANE[n.kind]||GRAPH_KIND_PANE.person;
  draw(`<div class="graph-crumbs" role="navigation" aria-label="Breadcrumb"><a href="#graph" data-crumb="">Graph</a><span aria-hidden="true">›</span><a href="#graph=${paneId}" data-crumb="${paneId}">${paneName}</a><span aria-hidden="true">›</span><span aria-current="page">${esc(n.name)}</span></div>${n.kind==='person'?personPage(n,group,sub):n.kind==='org'?orgPage(n,group):`<article class="graph-detail"><div class="name-row"><h3 title="${esc(n.name)}">${esc(n.name)}</h3>${n.project?projActions(n.project):'<button class="ghost" data-name-edit>Rename</button>'}</div><form class="name-form inline-edit" data-node-id="${esc(n.id)}" hidden><input name="newname" maxlength="60" value="${esc(n.name)}" placeholder="Project name" aria-label="Name"><button>Save</button></form><p class="graph-sub detail-sub">${esc(sub)}</p>${stageBox(n)}${projFacts(n)}${crmFieldsSection(n)}${detailGroups(n,group)}</article>`}`+privateRow(n)+teamBlock(n)+projectTodos(n)+openBetween(n)+knownAbout(n)+graphEvents(n));
  if(version!==graphRequest)return;
  view.dataset.mode='node';graphKept=null;docTitle();$('#people').classList.add('graph-on-node');if(location.hash!==graphHash(n.id)&&!$('#people').hidden)history.replaceState(null,'',graphHash(n.id));
  for(const p of view.querySelectorAll('.ge-preview'))p.classList.toggle('fade',p.scrollHeight>p.clientHeight+1);
  if(n.kind==='person')contactMarks(view,n);
  if(editRole===node){editRole=false;const pf=view.querySelector('#org-form');if(pf?.elements.role){orgOpen(pf,true);pf.elements.role.focus({preventScroll:true});pf.elements.role.select();pf.elements.role.scrollIntoView({block:'center'})}}
  if(!quiet)scrollTo({top:0});return}
 $('#people').classList.remove('graph-on-node');
 const q=$('#people-query').value.trim();
 if(!q&&graphUnstash(view))return;if(!q&&view.dataset.mode==='search')draw('<p class="pager-loading" role="status">Loading…</p>');
 if(q){const key='gsearch:'+q,p=pager(key,cursor=>request('api/graph?q='+encodeURIComponent(q)+'&cursor='+encodeURIComponent(cursor)).then(r=>({items:r.found,next:r.next})),graphItem);
  graphStash(view);if(!p.items.length&&p.next!=null){if(view.dataset.mode!=='search'||!view.querySelector('.graph-found'))draw('<p class="pager-loading" role="status">Searching…</p>','search');await pagerMore(key)}
  if(version!==graphRequest||$('#people-query').value.trim()!==q)return;  /* a late answer to an older search changes nothing */
  if(p.failed&&!p.items.length)throw new Error('Couldn’t search. Try again.');
  draw(p.items.length?`<div class="graph-found"><div class="section-head"><h2>Found</h2></div>${pagerSlot(key,'','graph-list')}</div>`:'<div class="empty all-clear graph-found"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>Nobody by that name.</strong>Try part of a name, an address or a company.</div></div>','search');pagerMount(view);return}
 const forTeam=graphTeam;let g=await cachedGet(graphTeam||graphPane==='held'?'api/graph?view=team':'api/graph',graphFresh);graphSharing=g.sharing||graphSharing;graphTeammates=g.teammates||graphTeammates;if(g.team&&!teamOn())g=await request('api/graph');
 if(forTeam!==graphTeam)return;  // Mine or Team changed while this loaded: the newer load draws
 if(!g.team)graphContactsIn=g.contacts_in||[];
 const team=!!g.team&&(graphTeam||graphPane==='held'),waiting=g.waiting??g.whos_who?.length??0;$('#badge-people').textContent=waiting||'';const start=team?shareNote(g.sharing):'';
 if(!team){graphOwners=g.owners||[];graphLastImport=g.last_import||null;graphFields=g.crm_fields||[];graphTags=g.tags||[];if(g.currency)graphCurrency=g.currency;tagsPaint()}
 const back=graphScroll;  /* back from a person: a quiet refresh that wins the race restores it too */const lc=!team&&g.list_counts||Object.fromEntries(['people','quiet','new','orgs','warmup','projects','projects_done'].map(k=>[k,(g[k]||[]).length]));graphLocal=!team&&g.list_counts?null:g;  /* the team's lists come whole */
 const had=quiet&&new Map([...pagers].filter(([k,p])=>k.startsWith('graph:')&&p.items.length).map(([k,p])=>[k,p.items.length]));
 if(team||graphListsTeam||JSON.stringify(lc)!==JSON.stringify(graphLists)||!g.list_counts){pagerDrop('graph');graphLists=lc}graphListsTeam=team;
 const panes=team?[{id:'people',label:'People',html:start+(graphTabs('people')||'<div class="empty all-clear"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>Nothing from the team yet.</strong></div></div>')},
  {id:'projects',label:'Projects',html:projectsPane(g)},
  {id:'orgs',label:'Organizations',html:graphTabs('orgs')||graphEmpty('orgs',true)},
  {id:'roles',label:'Who’s who',badge:waiting,html:whosWho(g.whos_who,waiting)},
  ...(g.held?.length||graphPane==='held'?[{id:'held',label:'Held back',html:heldPane(g.held)}]:[])].filter(p=>p.html)
 :[{id:'people',label:'People',html:sameList(g.same_person)+(graphTabs('people')||graphEmpty('people'))},
  {id:'projects',label:'Projects',html:projectsPane(g)},
  {id:'orgs',label:'Organizations',html:orgDoubles(g.org_doubles)+(graphTabs('orgs')||graphEmpty('orgs'))},
  {id:'roles',label:'Who’s who',badge:waiting,html:whosWho(g.whos_who,waiting)}].filter(p=>p.html);
 const current=(panes.find(p=>p.id===graphPane)||panes.find(p=>p.id==='people')||panes[0])?.id;graphCountsSet(g.counts);if(version===graphRequest){graphShown=current||'';graphHashSync();graphSubSync()}
 // A refresh that starts the lists over loads as many rows as were there before it draws, so the page keeps its height
 if(had)for(const [k,n] of had){const p=pagers.get(k);if(!p||p.items.length||p.busy)continue;for(let i=0;i<10&&p.items.length<n&&p.next!=null&&!p.failed;i++){p.pending=pagerLoad(k,p,false);await p.pending}}
 if(version!==graphRequest)return;
 rolesRow(panes.some(p=>p.id==='roles'),waiting);draw((panes.length?panes.map(p=>`<div class="sub-pane" role="tabpanel" data-graph-panel="${p.id}"${p.id===current?'':' hidden'}>${p.html}</div>`).join(''):'')
  ||'<div class="empty all-clear"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>Nothing mapped yet.</strong>People appear as messages and meetings come in.</div></div>');
 if(version===graphRequest){graphAt=Date.now();pagerMount(view);if(back!=null&&version===graphRequest){graphScroll=null;scrollTo(0,back)}}if(!quiet)notice('')}catch(e){errCaught(e);if(version===graphRequest&&(!quiet||!oldHtml))notice(e.message,true)}}
const graphPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
// The Graph as a CRM (crm.py, crm_import.py). Filter by each list (owner, board, stage, organization, value,
// close date; done on the Machine, a page at a time), an owner from the Work Fleet on each record, one organization
// with several websites (Same organization as…, Add a website…, Split off, Same organization?), and a CSV import with
// a preview and Undo. Filters are kept per list on this device.
var graphOwners=[],graphLastImport=null,crmFilters=(()=>{try{return JSON.parse(localStorage.getItem('graph-filters')||'{}')||{}}catch{return{}}})();
const crmPaneOf=list=>String(list).startsWith('projects')?'projects':list==='orgs'||list==='warmup'?'orgs':'people';
// The Team lists come whole, so their filters (who shared it, organization, state) work here, kept apart from Mine's.
var teamFilters=(()=>{try{return JSON.parse(localStorage.getItem('graph-team-filters')||'{}')||{}}catch{return{}}})();
const crmTeam=()=>!!(graphLocal&&graphListsTeam);
const crmF=pane=>(crmTeam()?teamFilters:crmFilters)[pane]||{};
const viaNames=n=>String(n.via||'').replace(/^via\s+/i,'').split(/,\s*|\s+and\s+/).map(x=>x.trim()).filter(Boolean);
const teamSharers=()=>[...new Set(['people','orgs','projects','projects_done'].flatMap(k=>(graphLocal?.[k]||[]).flatMap(viaNames)))].sort((a,b)=>a.localeCompare(b));
function teamKept(list){const items=graphLocal?.[list]||[];if(!crmTeam()||list==='warmup')return items;const f=crmF(crmPaneOf(list)),v=list==='projects'?teamPickOf(items):'all';
 return items.filter(n=>(!f.by||viaNames(n).includes(f.by))&&(!f.org||String(n.org_name||n.org||'').toLowerCase().includes(f.org.toLowerCase()))&&(!f.state||n.state===f.state)&&teamHit(n,v))}
const crmQuery=list=>list==='warmup'?'':Object.entries(crmF(crmPaneOf(list))).filter(([,v])=>v!==''&&v!=null).map(([k,v])=>`&${k}=${encodeURIComponent(v)}`).join('');
const crmKey=(list,sort)=>`graph:${list}:${sort}${crmQuery(list)?':'+crmQuery(list):''}${crmTeam()&&list==='projects'?':'+teamPickOf(graphLocal?.projects||[]):''}`;  /* the team's Mine / Needs me / All is its own page */
const crmCount=pane=>Object.values(crmF(pane)).filter(v=>v!==''&&v!=null).length;
const crmSet=(pane,f)=>{const team=crmTeam(),all=team?teamFilters:crmFilters;all[pane]=Object.fromEntries(Object.entries(f).filter(([,v])=>v!==''&&v!=null));try{localStorage.setItem(team?'graph-team-filters':'graph-filters',JSON.stringify(all))}catch{}graphTabsPaint(pane);if(pane==='projects')boardRedraw()};
const crmBoards=()=>(graphMineBoards||graphBoards||[]).filter(b=>!b.team);
const ownerName=id=>id==='me'?'you':graphOwners.find(m=>m.id===id)?.name||'a teammate';
// The Mine tab is the owner's own Graph, so it has no Mine button (Filter has Owner). The Team tab's projects have
// Mine, Needs me and All, the same choice on the List and the Board.
const crmFilterButton=(pane,cls='')=>{const n=crmCount(pane);return `<button type="button"${cls?` class="${cls}"`:''} data-crm-filter="${pane}" aria-haspopup="dialog" aria-label="Filter"><svg class="crm-funnel" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16l-6 7.5V19l-4-2v-4.5z"/></svg><span class="crm-word">Filter</span>${n?` <span class="badge">${n}</span>`:''}</button>`};
const crmTools=(pane,tab)=>`<div class="graph-tools">${pane==='projects'&&tab==='projects'&&crmTeam()&&(graphLocal?.projects||[]).length?teamSeg(graphLocal.projects):''}${crmFilterButton(pane)}</div>`;
const CRM_STATE={'heating up':'Busier lately',active:'Steady',cooling:'Quieter lately',dormant:'Quiet'};
const CRM_LABEL={waiting:()=>t('No reply in 10+ days'),by:v=>t('Shared by {}',v),state:v=>t('State: {}',t(CRM_STATE[v]||v)),owner:v=>t('Owner: {}',ownerName(v)),tag:v=>t('Tag: {}',v),board:v=>t('Board: {}',crmBoards().find(b=>String(b.id)===String(v))?.name||v),stage:v=>t('Stage: {}',v),org:v=>t('Organization: {}',v),
 value_min:v=>t('Value from {}',money(+v)),value_max:v=>t('Value up to {}',money(+v)),close_from:v=>t('Closes from {}',closeDay(v)),close_to:v=>t('Closes by {}',closeDay(v))};
const crmChips=pane=>Object.entries(crmF(pane)).filter(([k,v])=>CRM_LABEL[k]&&v!=='').map(([k,v])=>`<span class="chip">${esc(CRM_LABEL[k](v))}</span>`).join('');
const crmActive=pane=>{const on=crmChips(pane);return on?`<p class="graph-active">${on}<button type="button" class="link" data-crm-clear="${pane}">Clear</button></p>`:''};
const ownerRow=n=>kv('Owner',`<label class="owner-pick"><select data-owner-pick="${esc(n.id)}" aria-label="Owner of ${esc(n.name)}"><option value="me"${n.owner?'':' selected'}>You</option>${graphOwners.map(m=>`<option value="${esc(m.id)}"${n.owner===m.id?' selected':''}>${esc(m.name)}</option>`).join('')}${n.owner&&!graphOwners.some(m=>m.id===n.owner)?`<option value="${esc(n.owner)}" selected>${esc(n.owner_name||'Not in your Fleet now')}</option>`:''}</select></label>`);
const changeText=c=>c.field==='owner'?`Owner set to ${c.new?.id==='me'?'you':c.new?.name||'a teammate'}`:c.field==='merged'?`Merged in ${c.new?.name||''}`:c.field==='split'?`Split off ${c.new?.name||''}`:'Changed';
const aliasName=a=>a.startsWith('org:named:')?a.slice(10).replace(/-/g,' '):a.slice(4);
const orgSites=n=>n.aliases?.length?`<section class="detail-section org-sites"><h4>Websites</h4><ul>${n.domain?`<li><span>${esc(n.domain)}</span></li>`:''}${n.aliases.map(a=>`<li><span>${esc(aliasName(a))}${a.startsWith('org:named:')?' <small class="muted">(no website)</small>':''}</span><button type="button" class="ghost" data-org-split="${esc(a)}">Split off</button></li>`).join('')}</ul></section>`:'';
const orgDoubleAsk=n=>(n.doubles||[]).slice(0,2).map(d=>{const o=d.a.id===n.id?d.b:d.a;return `<div class="same-ask"><p class="graph-sub">Same organization as ${nodeButton(o)}?<br><span class="muted">${esc(d.why)}${o.domain?' · '+esc(o.domain):''}</span></p><p class="graph-sub role-row"><button data-org-merge="${esc(o.id)}" data-org-into="${esc(n.id)}">Same</button><button class="ghost" data-org-apart="${esc(n.id)}" data-org-b="${esc(o.id)}">Not the same</button></p></div>`}).join('');
const orgDoubles=items=>items?.length?`<div class="section-head"><h2>Same organization?</h2><span class="count">${items.length}</span><p>Possible doubles. Merge them or keep them apart.</p></div><div class="graph-list">${items.map(s=>`<article class="same-pair"><div class="graph-row">${orgPic(s.a)}${nodeButton(s.a)}<span class="muted">and</span>${orgPic(s.b)}${nodeButton(s.b)}</div><p class="graph-sub">${esc(s.why)}${s.a.domain||s.b.domain?` · <span class="mono">${esc([s.a.domain,s.b.domain].filter(Boolean).join(', '))}</span>`:''}</p><p class="graph-sub role-row"><button data-org-merge="${esc(s.b.id)}" data-org-into="${esc(s.a.id)}">Merge</button><button class="ghost" data-org-apart="${esc(s.a.id)}" data-org-b="${esc(s.b.id)}">Not the same</button></p></article>`).join('')}</div>`:'';
// One dialog for the filter sheet, the import and an organization's Same as… and Add a website…
let crm=null;
const crmHead=t=>`<div class="snooze-heading"><h2 id="crm-dialog-title">${esc(t)}</h2><button type="button" data-crm-close aria-label="Close">×</button></div>`;
const crmFoot=(ok,extra='')=>`<p class="ed-note warn" data-crm-error role="alert" hidden></p><div class="ed-actions">${extra}<span class="grow"></span><button type="button" class="ghost" data-crm-close>Cancel</button><button class="primary">${esc(ok)}</button></div>`;
const crmShow=(wide,tall)=>{const d=$('#crm-dialog');d.classList.toggle('wide',!!wide);d.classList.toggle('tall',!!tall);if(!d.open)d.showModal()};
const crmSay=t=>{const er=$('#crm-form [data-crm-error]');if(er){er.textContent=t;er.hidden=!t}};
const opt=(v,t,on)=>`<option value="${esc(v)}"${on?' selected':''}>${esc(t)}</option>`;
function crmStages(board,current){const bs=crmBoards(),pick=bs.find(b=>String(b.id)===String(board)),names=[...new Set((pick?[pick]:bs).flatMap(b=>(b.stages||[]).map(s=>s.name)))];return opt('','Any stage',!current)+names.map(s=>opt(s,s,s===current)).join('')}
function crmFilterOpen(pane){const f=crmF(pane);crm={mode:'filter',pane};const by=pane!=='projects';
 if(crmTeam()){$('#crm-form').innerHTML=crmHead(t('Filter the team’s {}',i18nLower(t(GRAPH_TABS[pane].label))))
  +`<label class="ed-field">Shared by<select name="by">${opt('','Anyone',!f.by)}${teamSharers().map(m=>opt(m,m,f.by===m)).join('')}</select></label>`
  +(pane==='people'?`<label class="ed-field">Organization<input name="org" value="${esc(f.org||'')}" placeholder="Name or website" autocomplete="off"></label>`:'')
  +(pane==='projects'?`<label class="ed-field">State<select name="state">${opt('','Any state',!f.state)}${Object.entries(CRM_STATE).map(([k,t])=>opt(k,t,f.state===k)).join('')}</select></label>`:'')
  +crmFoot('Show results','<button type="button" class="ghost" data-crm-clear-all>Clear all</button>');return crmShow()}
 $('#crm-form').innerHTML=crmHead(t('Filter {}',i18nLower(t(GRAPH_TABS[pane].label))))
  +(graphOwners.length?`<label class="ed-field">Owner<select name="owner">${opt('','Anyone',!f.owner)}${opt('me','You',f.owner==='me')}${graphOwners.map(m=>opt(m.id,m.name,f.owner===m.id)).join('')}</select></label>`:'')
  +(crmBoards().length?`<div class="ed-row3"><label class="ed-field">Board<select name="board">${opt('','Any board',!f.board)}${crmBoards().map(b=>opt(b.id,b.name,String(f.board)===String(b.id))).join('')}</select></label><label class="ed-field">Stage<select name="stage">${crmStages(f.board,f.stage)}</select></label></div>`:'')
  +(graphTags.length?`<label class="ed-field">Tag<select name="tag">${opt('','Any tag',!f.tag)}${graphTags.map(t=>opt(t.tag,t.tag,(f.tag||'').toLowerCase()===t.tag.toLowerCase())).join('')}</select></label>`:'')
  +(pane==='orgs'?'':`<label class="ed-field">Organization<input name="org" value="${esc(f.org||'')}" placeholder="Name or website" autocomplete="off"></label>`)
  +`<div class="ed-row3"><label class="ed-field">Value from<input name="value_min" inputmode="decimal" value="${esc(f.value_min??'')}" placeholder="Any" autocomplete="off"></label><label class="ed-field">Value up to<input name="value_max" inputmode="decimal" value="${esc(f.value_max??'')}" placeholder="Any" autocomplete="off"></label></div>`
  +`<div class="ed-row3"><label class="ed-field">Closes from<input name="close_from" type="date" value="${esc(f.close_from||'')}"></label><label class="ed-field">Closes by<input name="close_to" type="date" value="${esc(f.close_to||'')}"></label></div>`
  +(pane==='projects'?`<label class="ed-check"><input type="checkbox" name="waiting" value="1"${f.waiting?' checked':''}> No reply in 10+ days</label>`:'')
  +(by?'<p class="ed-note">Board, stage, value and close date go by their open projects.</p>':'')
  +crmFoot('Show results','<button type="button" class="ghost" data-crm-clear-all>Clear all</button>');
 crmShow()}
async function crmImportOpen(pane){crm={mode:'import',kind:pane==='projects'?'project':pane==='orgs'?'org':'person',text:'',name:'',mapping:null,seen:null,check:null,own:false,typeOff:new Set(),fixOff:new Set(),fixOpen:false};crmImportDraw()}
const CRM_FIX_TYPES=['spaces','case','split','email','phone','website','date','value','tags','stage','merge'];
const crmFixArgs=c=>({fixes:{types:c.typeOff.size?CRM_FIX_TYPES.filter(t=>!c.typeOff.has(t)):'all',off:[...c.fixOff]},...(c.check?.state==='done'?{ai_run:c.check.id}:{})});
function crmKept(s,c){const on=(s.fix_types||[]).filter(t=>!c.typeOff.has(t.type));return on.reduce((n,t)=>n+t.count,0)-(s.fixes||[]).filter(f=>c.fixOff.has(f.id)&&!c.typeOff.has(f.type)).length}
function crmFixesHtml(s,c){const by={};for(const f of s.fixes||[])(by[f.type]=by[f.type]||[]).push(f);
 return `<fieldset><legend>Fixes</legend><div class="crm-fixes">${(s.fix_types||[]).map(t=>`<details class="crm-fixtype"${c.fixOpen===t.type?' open':''} data-type="${t.type}"><summary><input type="checkbox" data-crm-fixtype="${t.type}" aria-label="${esc(t.name)}"${c.typeOff.has(t.type)?'':' checked'}><span>${esc(t.name)} <small>${t.count}</small></span></summary><ul>${(by[t.type]||[]).map(f=>`<li><label><input type="checkbox" data-crm-fix="${esc(f.id)}"${c.typeOff.has(t.type)?' disabled':''}${c.fixOff.has(f.id)?'':' checked'}><span class="ba"><s>${esc(f.before)}</s> → ${esc(f.after)}</span><small>Line ${f.line}${f.field==='row'?'':' · '+esc(f.field_name)}${f.ai?' · your model':''}${f.why?': '+esc(f.why):''}</small></label></li>`).join('')}${(by[t.type]||[]).length<t.count?`<li><small>and ${t.count-(by[t.type]||[]).length} more like these</small></li>`:''}</ul></details>`).join('')}</div></fieldset>`}
function crmImportDraw(){const c=crm,s=c.seen,n=s?s.counts.new+s.counts.match:0,STATUS={new:'New',match:'Matches',skip:'Skipped'},kept=s?crmKept(s,c):0,ck=c.check?.state;
 $('#crm-form').innerHTML=crmHead('Import CSV')
  +`<div class="ed-row3"><label class="ed-field">What is in it<select name="kind">${opt('person','People',c.kind==='person')}${opt('org','Organizations',c.kind==='org')}${opt('project','Projects',c.kind==='project')}</select></label><div class="ed-field">File<label class="crm-file"><input name="file" type="file" accept=".csv,.tsv,.txt,text/csv"><span class="crm-file-name">${c.name?esc(c.name):'Choose file'}</span>${c.name?'<span class="crm-file-change">· <u>Change</u></span>':''}</label></div></div>`
  +(c.name?'':'<p class="ed-note">A spreadsheet saved as CSV, with a row of headers. It stays on your Machine.</p>')
  +(ck==='checking'?'<p class="crm-ai run" role="status">Your model is checking the columns…</p>':ck==='done'&&s?.ai?'<p class="crm-ai" role="status">Checked by your model. Change anything below.</p>':ck==='failed'?'<p class="crm-ai" role="status">Your model couldn’t check it this time; the columns are guessed from their headers.</p>':'')
  +(s?(s.problem?(ck==='checking'?'':`<p class="crm-problem">${esc(s.problem)}.</p>`):`<p class="crm-count"><b>${s.counts.new}</b> new · <b>${s.counts.match}</b> match existing · <b>${s.counts.skip}</b> skipped</p>`)
   +(s.fix_total?`<p class="crm-fixline"><span><b>${s.fix_total} ${s.fix_total===1?'fix':'fixes'} suggested</b>${kept!==s.fix_total?`, ${kept} kept`:''}</span>·<button type="button" class="link" data-crm-fixes aria-expanded="${!!c.fixOpen}">${c.fixOpen?'Hide':'Review'}</button></p>`+(c.fixOpen?crmFixesHtml(s,c):''):'')
   +`<fieldset><legend>Columns</legend><div class="crm-cols">${s.columns.map(col=>`<div class="crm-col"><span><b title="${esc(col.header)}">${esc(col.header)}</b><small>${esc(col.samples.join(' · ')||'empty')}</small></span><select data-crm-col="${col.index}" aria-label="${esc(col.header)} goes to">${opt('','Skip',!col.field)}${s.fields.map(f=>opt(f.id,f.name,col.field===f.id)).join('')}</select>${col.reason?`<small class="crm-why">${esc(col.reason)}</small>`:''}</div>`).join('')}</div></fieldset>`
   +(s.problem?'':`<fieldset><legend>Rows${s.total>s.rows.length?` (first ${s.rows.length} of ${s.total})`:''}</legend><ul class="crm-rows">${s.rows.map(r=>`<li><span class="n">${esc(r.record.name||r.record.email||'(no name)')}</span><span class="st ${r.status}">${STATUS[r.status]}${r.status==='match'&&r.match_name?' '+esc(r.match_name):''}${r.status==='skip'?': '+esc(r.why||''):''}</span></li>`).join('')}</ul></fieldset>`)
   +'<p class="ed-note">Matches get what the file says; empty cells change nothing. You can undo the last import.</p>':'')
  +crmFoot(s?(n?`Import ${n}${kept?` with ${kept} ${kept===1?'fix':'fixes'}`:''}`:'Nothing to import'):'Import');
 const ok=$('#crm-form button.primary');ok.disabled=!n;crmShow(!!(s||c.name),!!c.name)}
const crmUpload=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf,'X-Upload':'graph-import'},body:JSON.stringify({action,args})});
async function crmPreview(){const c=crm;if(!c?.text)return;crmSay('');const seq=c.seq=(c.seq||0)+1;
 try{const s=await crmUpload('graph_import_preview',{kind:c.kind,text:c.text,...(c.mapping?{mapping:c.mapping}:{}),...crmFixArgs(c)});if(crm===c&&seq===c.seq){c.seen=s;crmImportDraw()}}catch(x){errCaught(x);if(seq!==c.seq)return;c.seen=null;crmImportDraw();crmSay(x.message)}}
// The owner's own model looks at the columns and the cells the rules can't read (headers and a few values, on their
// Machine); the rules' guess shows meanwhile, and stays when the model can't run now.
async function crmCheck(){const c=crm;if(!c?.text)return;c.check=null;const key=c.kind+c.text;
 try{const r=await crmUpload('graph_import_ai',{kind:c.kind,text:c.text});if(crm!==c||c.kind+c.text!==key||!r.ai)return;c.check={id:r.run_id,state:'checking'};crmImportDraw();
  for(let i=0;i<120&&crm===c&&c.check?.id===r.run_id;i++){await new Promise(ok=>setTimeout(ok,i<10?1500:3000));if(crm!==c||c.check?.id!==r.run_id)return;
   const st=await graphPost('graph_import_ai_status',{run_id:r.run_id});if(st.status==='starting'||st.status==='running')continue;
   c.check.state=st.status==='ok'?'done':'failed';if(c.check.state==='done'&&!c.own)c.mapping=null;return c.check.state==='done'?crmPreview():crmImportDraw()}
  if(crm===c&&c.check?.id===r.run_id){c.check.state='failed';crmImportDraw()}}catch{if(crm===c&&c.check?.state==='checking'){c.check.state='failed';crmImportDraw()}}}
function crmOrgOpen(mode){const name=$('#people-view .graph-detail>.name-row h3')?.textContent||'';crm={mode,id:graphNode,name,found:new Map()};
 $('#crm-form').innerHTML=mode==='org-same'?crmHead('Same organization as…')+`<p class="ed-note">${esc(name)} and the one you pick become one organization, with their people, projects and notes. Split off undoes it.</p><label class="ed-field">Which organization?<input name="q" list="crm-orgs" placeholder="A name from your Graph" autocomplete="off" maxlength="100"></label><datalist id="crm-orgs"></datalist>`+crmFoot('Merge')
  :crmHead('Add a website')+`<p class="ed-note">One more website of ${esc(name)}, like its .io next to its .com. People with an address there join it.</p><label class="ed-field">Website<input name="website" inputmode="url" placeholder="acme.io" autocomplete="off" maxlength="200"></label>`+crmFoot('Add');
 crmShow();$('#crm-form input').focus()}
async function crmOrgSearch(q){const seq=crmOrgSearch.seq=(crmOrgSearch.seq||0)+1;if(q.length<2)return;try{const r=await request('api/graph?q='+encodeURIComponent(q));if(seq!==crmOrgSearch.seq||!crm)return;
 const orgs=(r.found||[]).filter(n=>n.kind==='org'&&n.id!==crm.id);for(const o of orgs)crm.found.set(o.name.toLowerCase(),o.id);$('#crm-orgs').innerHTML=orgs.map(o=>`<option value="${esc(o.name)}">${esc(o.domain||'')}</option>`).join('')}catch{}}
const crmAfter=async(id)=>{graphMineBoards=null;pagerDrop('graph');if(id&&graphNode&&id!==graphNode)return graphOpen(id);await people(graphNode,true)};
$('#crm-form').addEventListener('click',e=>{if(e.target.closest('[data-crm-close]'))$('#crm-dialog').close();
 if(e.target.closest('[data-crm-fixes]')&&crm?.mode==='import'){crm.fixOpen=!crm.fixOpen;crmImportDraw()}
 const sum=e.target.closest('.crm-fixtype>summary');if(sum&&crm?.mode==='import'&&!e.target.closest('input')){e.preventDefault();const t=sum.parentElement.dataset.type;crm.fixOpen=crm.fixOpen===t?true:t;crmImportDraw()}
 if(e.target.closest('[data-crm-clear-all]')&&crm?.mode==='filter'){crmSet(crm.pane,{});$('#crm-dialog').close()}
 if(e.target.closest('[data-crm-clear-all]')&&crm?.mode==='board-stages'){const n=crm.board;$('#crm-dialog').close();boardStagesSet(n,null)}});
$('#crm-form').addEventListener('change',e=>{const c=crm;if(!c)return;
 if(c.mode==='filter'&&e.target.name==='board'){const st=$('#crm-form select[name=stage]');if(st)st.innerHTML=crmStages(e.target.value,'')}
 if(c.mode!=='import')return;
 const fresh=()=>{c.mapping=null;c.own=false;c.check=null;c.typeOff.clear();c.fixOff.clear();crmPreview();crmCheck()};
 if(e.target.name==='kind'){c.kind=e.target.value;return fresh()}
 if(e.target.name==='file'){const file=e.target.files?.[0];if(!file)return;if(file.size>8*1024*1024)return crmSay('That file is too big: up to 8 MB.');
  const r=new FileReader();r.onload=()=>{c.text=String(r.result||'');c.name=file.name;fresh()};r.onerror=()=>crmSay('Couldn’t read that file.');r.readAsText(file);return}
 if(e.target.dataset.crmFixtype){c.typeOff[e.target.checked?'delete':'add'](e.target.dataset.crmFixtype);return crmPreview()}
 if(e.target.dataset.crmFix){c.fixOff[e.target.checked?'delete':'add'](e.target.dataset.crmFix);return crmPreview()}
 if(e.target.dataset.crmCol!=null){c.own=true;c.mapping=Object.fromEntries([...$('#crm-form').querySelectorAll('[data-crm-col]')].map(s=>[s.dataset.crmCol,s.value]).filter(([,v])=>v));crmPreview()}});
$('#crm-form').addEventListener('input',e=>{if(crm&&e.target.type!=='file')crmSay('');  /* an error goes once the owner changes what it was about */
 if(crm?.mode==='org-same'&&e.target.name==='q')crmOrgSearch(e.target.value.trim())});
$('#crm-form').addEventListener('submit',async e=>{e.preventDefault();const c=crm,f=e.target;if(!c)return;const v=k=>String(f.elements[k]?.value||'').trim(),btn=f.querySelector('button.primary');crmSay('');
 if(c.mode==='picture')return;
 if(c.mode==='board-stages'){const on=[...f.querySelectorAll('input[name=stage]:checked')].map(x=>x.value);if(!on.length)return crmSay('Pick at least one stage.');const all=f.querySelectorAll('input[name=stage]').length;$('#crm-dialog').close();return boardStagesSet(c.board,on.length===all?null:on)}
 if(c.mode==='fields'){btn.disabled=true;try{await crmFieldsSave(c)}catch(x){errCaught(x);crmSay(x.message)}finally{btn.disabled=false}return}
 if(c.mode==='filter'){const next=Object.fromEntries(['by','state','owner','tag','board','stage','org','value_min','value_max','close_from','close_to'].map(k=>[k,v(k)]));next.waiting=f.elements.waiting?.checked?'1':'';
  for(const k of ['value_min','value_max'])if(next[k]&&!/^\d+([.,]\d+)?$/.test(next[k].replace(/[\s€$£]/g,'')))return crmSay('Value: a number, like 12000.');
  crmSet(c.pane,next);$('#crm-dialog').close();return}
 btn.disabled=true;
 try{if(c.mode==='import'){const r=await crmUpload('graph_import_run',{kind:c.kind,text:c.text,name:c.name,...(c.mapping?{mapping:c.mapping}:{...(c.seen?{mapping:Object.fromEntries(c.seen.columns.filter(x=>x.field).map(x=>[x.index,x.field]))}:{})}),...crmFixArgs(c)});$('#crm-dialog').close();
   toast(`Imported: ${r.new} new, ${r.updated} updated${r.skipped?`, ${r.skipped} skipped`:''}.`);$('#toast').insertAdjacentHTML('beforeend',` <button data-crm-undo-import="${r.import_id}" data-now>Undo</button>`);clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),15000);
   return crmAfter()}
  if(c.mode==='org-same'){const id=c.found.get(v('q').toLowerCase());if(!id)return crmSay('Pick an organization from the list.');
   const r=await graphPost('graph_org_merge',{node_id:c.id,into:id});$('#crm-dialog').close();toast('Merged. Split off undoes it.');return crmAfter(r.node_id)}
  if(c.mode==='org-site'){if(!v('website'))return crmSay('Type a website, like acme.io.');const r=await graphPost('graph_org_merge',{node_id:c.id,website:v('website')});$('#crm-dialog').close();toast('Added.');return crmAfter(r.node_id)}}
 catch(x){errCaught(x);crmSay(x.message)}finally{btn.disabled=false}});
$('#crm-dialog').addEventListener('close',e=>{if(!e.currentTarget.open)crm=null});
document.addEventListener('click',async e=>{const t=e.target.closest('[data-crm-filter],[data-crm-clear],[data-crm-import],[data-crm-undo-import],[data-org-split],[data-org-merge],[data-org-apart],[data-org-same],[data-org-site],[data-crm-waiting]');if(!t)return;
 e.preventDefault();e.stopPropagation();t.closest('details')?.removeAttribute('open');
 if(t.dataset.crmFilter)return crmFilterOpen(t.dataset.crmFilter);
 if(t.dataset.crmClear)return crmSet(t.dataset.crmClear,{});
 if(t.dataset.crmImport)return crmImportOpen(t.dataset.crmImport);
 if(t.hasAttribute('data-crm-waiting')){const f={...crmF('projects')};if(f.waiting)delete f.waiting;else f.waiting='1';return crmSet('projects',f)}
 if(t.hasAttribute('data-org-same'))return crmOrgOpen('org-same');
 if(t.hasAttribute('data-org-site'))return crmOrgOpen('org-site');
 t.disabled=true;
 try{if(t.dataset.crmUndoImport){if(!t.hasAttribute('data-now')&&!confirm('Undo the last import? What it added goes, and what it changed goes back.'))return;$('#toast').classList.remove('show');
   await graphPost('graph_import_undo',{import_id:+t.dataset.crmUndoImport});toast('Import undone.');return crmAfter()}
  if(t.dataset.orgSplit){await graphPost('graph_org_split',{alias:t.dataset.orgSplit});toast('Split off.');return crmAfter()}
  if(t.dataset.orgMerge){const r=await graphPost('graph_org_merge',{node_id:t.dataset.orgMerge,into:t.dataset.orgInto});toast('Merged. Split off undoes it.');return crmAfter(graphNode?r.node_id:null)}
  if(t.dataset.orgApart){await graphPost('graph_org_apart',{a:t.dataset.orgApart,b:t.dataset.orgB});toast('Kept apart.');return crmAfter()}}
 catch(err){errCaught(err);toast(err.message,true)}finally{t.disabled=false}},true);
document.addEventListener('change',async e=>{const t=e.target.closest?.('[data-owner-pick]');if(!t)return;t.disabled=true;
 try{await graphPost('graph_owner',{node_id:t.dataset.ownerPick,owner:t.value});toast(t.value==='me'?'You own it.':`${ownerName(t.value)} owns it.`);graphMineBoards=null;await people(graphNode,true)}catch(err){errCaught(err);toast(err.message,true)}finally{t.disabled=false}});

// Pipeline on a board: what is open per stage and what is expected to close per month, from each project's value and
// expected close date (the projects on the board as shown, so Mine counts only the owner's own). One series, so one
// color; every bar carries its label and value as text.
const pipeMonth=k=>{const d=new Date(Math.floor(k/12),k%12,1),y=d.getFullYear()!==new Date().getFullYear();return d.toLocaleDateString(DL,{month:'short',...(y?{year:'numeric'}:{})})};
const pipeRow=(label,value,n,max,cls='')=>`<div class="pipe-row${cls}" title="${esc(label)}: ${esc(moneyFull(value))} in ${n} project${n===1?'':'s'}"><span class="pipe-k ell">${esc(label)}</span><span class="pipe-bar" aria-hidden="true">${value>0?`<i style="width:${Math.max(2,Math.round(value/max*100))}%"></i>`:''}</span><span class="pipe-v">${esc(money(value))} <small>${n}</small></span></div>`;
function pipeline(b){if(!b.projects.some(p=>p.value!=null))return '';
 // Open is what can still close: not won or lost, not in the last stage (where Won puts it) nor Stalled or declined
 const main=b.stages.filter(s=>!s.side),wonStage=main.length>1?main.at(-1).name:null,side=new Set(b.stages.filter(s=>s.side).map(s=>s.name));
 const won=p=>p.outcome==='won'||p.stage===wonStage,ps=b.projects.filter(p=>!p.outcome&&!won(p)&&!side.has(p.stage));
 const sum=a=>a.reduce((t,p)=>t+(p.value||0),0),total=sum(ps),now=new Date(),m0=now.getFullYear()*12+now.getMonth();
 const key=d=>{const [y,m]=String(d).split('-').map(Number);return y*12+m-1};
 const wonNow=b.projects.filter(p=>won(p)&&p.value!=null&&p.at&&key(String(p.at).slice(0,7))===m0);
 const stages=main.filter(s=>s.name!==wonStage).map(s=>{const it=ps.filter(p=>p.stage===s.name);return [s.name,sum(it),it.length]});
 const months=new Map(),over=[0,0],none=[0,0],later=[0,0];
 for(const p of ps){const v=p.value||0;if(p.value==null)continue;if(!p.close_date){none[0]+=v;none[1]++;continue}const k=key(p.close_date);
  if(k<m0){over[0]+=v;over[1]++}else if(k>m0+11){later[0]+=v;later[1]++}else{const x=months.get(k)||[0,0];x[0]+=v;x[1]++;months.set(k,x)}}
 const last=Math.max(m0+2,...months.keys()),monthRows=[];for(let k=m0;k<=last;k++){const x=months.get(k)||[0,0];monthRows.push([pipeMonth(k),x[0],x[1]])}
 const max1=Math.max(1,...stages.map(s=>s[1])),max2=Math.max(1,over[0],later[0],...monthRows.map(m=>m[1]));
 return `<details class="pipeline"${sideStore.get('board-pipeline')==='0'?'':' open'}><summary><b>Pipeline</b> <span>${esc(money(total))} open in ${ps.filter(p=>p.value!=null).length} with a value</span> `
  +`${wonNow.length?`<span class="pipe-won">Won this month: ${esc(money(sum(wonNow)))} in ${wonNow.length}</span>`:''}</summary><div class="pipe-grid">`
  +`<div class="pipe-block"><h5>Open by stage</h5>${stages.map(s=>pipeRow(s[0],s[1],s[2],max1)).join('')}</div>`
  +`<div class="pipe-block"><h5>Expected to close</h5>${over[1]?pipeRow('Overdue',over[0],over[1],max2,' over'):''}${monthRows.map(m=>pipeRow(m[0],m[1],m[2],max2)).join('')}${later[1]?pipeRow('Later',later[0],later[1],max2):''}`
  +`${none[1]?`<p class="pipe-note">No close date: ${esc(money(none[0]))} in ${none[1]}</p>`:''}</div></div></details>`}
document.addEventListener('click',e=>{const d=e.target.closest?.('.pipeline>summary')?.parentElement;if(d)sideStore.set('board-pipeline',d.open?'0':'1')});  /* the owner's pick, not a redraw's */

// Fields and tags (crm_fields.py): the owner's own fields per record type (text, number, date, a choice) and tags.
var graphFields=[],graphTags=[];
const FIELD_KIND={person:'people',org:'organizations',project:'projects'};
const fieldShow=f=>f.value==null||f.value===''?'<span class="muted">Not set</span>':f.type==='number'?esc(new Intl.NumberFormat().format(+f.value)):f.type==='date'?esc(closeDay(f.value)):esc(f.value);
const tagMini=n=>n.tags?.length?`<span class="tag-mini">${n.tags.slice(0,3).map(t=>`<span class="chip tag-chip">${esc(t)}</span>`).join('')}${n.tags.length>3?`<span class="muted">+${n.tags.length-3}</span>`:''}</span>`:'';
const tagChips=(tags,node)=>(tags||[]).map(t=>`<span class="chip tag-chip">${esc(t)}${node?`<button type="button" data-tag-remove="${esc(t)}" data-tag-node="${esc(node)}" aria-label="Remove the tag ${esc(t)}">×</button>`:''}</span>`).join('');
const tagsPaint=()=>{const l=$('#crm-tag-list');if(l)l.innerHTML=graphTags.map(t=>`<option value="${esc(t.tag)}"></option>`).join('')};
function crmFieldsSection(n){if(n.team_only)return (n.team_fields?.length||n.tags?.length)?`<section class="detail-section crm-fields"><h4>Fields</h4>${(n.team_fields||[]).map(f=>kv(esc(f.name),fieldShow(f))).join('')}${n.tags?.length?kv('Tags',`<span class="tag-list">${tagChips(n.tags)}</span>`):''}</section>`:'';
 const fs=n.fields||[],mine=new Set(fs.filter(f=>f.value!=null).map(f=>f.name.toLowerCase())),team=(n.team?.fields||[]).filter(f=>!mine.has(String(f.name).toLowerCase()));
 fieldsOf.set(n.id,fs);
 return `<section class="detail-section crm-fields"><h4>Fields</h4>${fs.map(f=>kv(esc(f.name),`<button type="button" class="field-val" data-field-edit="${f.id}" data-field-node="${esc(n.id)}" title="Change ${esc(f.name)}">${fieldShow(f)}</button>`)).join('')}${team.map(f=>kv(esc(f.name),fieldShow(f)+'<span class="sub">From your team</span>')).join('')}`
  +kv('Tags',`<span class="tag-list">${tagChips(n.tags,n.id)}<span class="tag-add" data-tag-node="${esc(n.id)}"><input name="tag" list="crm-tag-list" placeholder="+ Tag" maxlength="40" aria-label="Add a tag" enterkeyhint="done" autocomplete="off"></span></span>`)
  +`<p class="graph-sub"><button type="button" class="link" data-fields-edit="${esc(n.id)}">${fs.length?'Manage fields':'Add a field'}</button></p></section>`}
const fieldInput=(f,v)=>f.type==='choice'?`<select name="f${f.id}">${opt('','Not set',v==null||v==='')}${(f.choices||[]).map(c=>opt(c,c,c===v)).join('')}</select>`
 :f.type==='date'?`<input name="f${f.id}" type="date" value="${esc(v||'')}">`
 :f.type==='number'?`<input name="f${f.id}" inputmode="decimal" value="${esc(v??'')}" autocomplete="off">`
 :`<input name="f${f.id}" value="${esc(v??'')}" maxlength="500" autocomplete="off">`;
async function crmFieldsOpen(node,keep){const n=await request('api/graph?node='+encodeURIComponent(node));const c={mode:'fields',node:n.id,kind:n.kind,name:n.name,fields:n.fields||[],draft:keep||{}};crm=c;
 const fs=c.fields,val=f=>f.id in c.draft?c.draft[f.id]:f.value;
 $('#crm-form').innerHTML=crmHead(t('Fields of {}',n.name))
  +(fs.length?fs.map(f=>`<div class="crm-field-row"><label class="ed-field">${esc(f.name)}${fieldInput(f,val(f))}</label><button type="button" class="link" data-nf-remove="${f.id}" aria-label="Remove the field ${esc(f.name)}">Remove</button></div>`).join('')
   :`<p class="ed-note">No fields for ${FIELD_KIND[n.kind]} yet. A field you add shows on every one of them.</p>`)
  +`<details class="crm-newfield"${fs.length?'':' open'}><summary>New field for ${FIELD_KIND[n.kind]}</summary><div class="ed-row3"><label class="ed-field">Name<input name="nf_name" maxlength="40" autocomplete="off" placeholder="Renewal date"></label><label class="ed-field">Type<select name="nf_type">${opt('text','Text',1)}${opt('number','Number')}${opt('date','Date')}${opt('choice','Choice')}</select></label></div>`
  +`<label class="ed-field" data-nf-choices hidden>Choices<textarea name="nf_choices" rows="3" placeholder="One per line"></textarea></label><p><button type="button" class="ghost" data-nf-add>Add field</button></p></details>`
  +crmFoot('Save');crmShow()}
const crmDraft=()=>Object.fromEntries(((crm?.fields)||[]).map(f=>[f.id,String($('#crm-form').elements['f'+f.id]?.value??'')]));
$('#crm-form').addEventListener('click',async e=>{const c=crm;if(c?.mode!=='fields')return;const add=e.target.closest('[data-nf-add]'),rm=e.target.closest('[data-nf-remove]');if(!add&&!rm)return;e.preventDefault();
 const f=$('#crm-form'),draft=crmDraft();crmSay('');
 try{if(add){add.disabled=true;await graphPost('graph_field_save',{kind:c.kind,name:f.elements.nf_name.value,type:f.elements.nf_type.value,choices:f.elements.nf_choices.value})}
  else{const field=c.fields.find(x=>String(x.id)===rm.dataset.nfRemove);if(!confirm(`Remove the field ${field?.name||''} from every one of your ${FIELD_KIND[c.kind]}? What it holds goes too.`))return;await graphPost('graph_field_delete',{id:+rm.dataset.nfRemove});delete draft[rm.dataset.nfRemove]}
  graphFieldsStale=true;await crmFieldsOpen(c.node,draft)}catch(x){errCaught(x);crmSay(x.message);if(add)add.disabled=false}});
$('#crm-form').addEventListener('change',e=>{if(crm?.mode==='fields'&&e.target.name==='nf_type')$('#crm-form [data-nf-choices]').hidden=e.target.value!=='choice'});
var graphFieldsStale=false;
// A field's value changes in place: click it, change it, Enter or Save keeps it, Escape puts it back, Remove empties it.
const fieldsOf=new Map();
function fieldEditOpen(b){const f=(fieldsOf.get(b.dataset.fieldNode)||[]).find(x=>String(x.id)===b.dataset.fieldEdit);if(!f)return;
 const w=document.createElement('span');w.className='field-inline';w.dataset.fieldNode=b.dataset.fieldNode;w.dataset.fieldId=f.id;
 w.innerHTML=fieldInput(f,f.value)+'<button type="button" class="primary" data-field-save>Save</button><button type="button" class="ghost" data-field-cancel>Cancel</button>'+(f.value==null||f.value===''?'':'<button type="button" class="link" data-field-clear>Remove</button>');
 b.replaceWith(w);const i=w.querySelector('input,select');i.setAttribute('aria-label',f.name);i.focus();i.select?.()}
async function fieldEditSave(w,value){if(w.dataset.busy)return;const f=(fieldsOf.get(w.dataset.fieldNode)||[]).find(x=>String(x.id)===w.dataset.fieldId);const v=String(value??'').trim();
 if(f&&v===String(f.value??''))return people(graphNode,true);w.dataset.busy='1';w.querySelectorAll('button,input,select').forEach(x=>x.disabled=true);
 try{await graphPost('graph_field_set',{node_id:w.dataset.fieldNode,field_id:+w.dataset.fieldId,value:v});pagerDrop('graph');await people(graphNode,true)}
 catch(x){errCaught(x);delete w.dataset.busy;w.querySelectorAll('button,input,select').forEach(x=>x.disabled=false);toast(x.message,true)}}
document.addEventListener('click',e=>{const b=e.target.closest('[data-field-edit]');if(b){e.preventDefault();return fieldEditOpen(b)}
 const w=e.target.closest('.field-inline');if(!w)return;
 if(e.target.closest('[data-field-save]'))return fieldEditSave(w,w.querySelector('input,select').value);
 if(e.target.closest('[data-field-clear]'))return fieldEditSave(w,'');
 if(e.target.closest('[data-field-cancel]'))return people(graphNode,true)});
document.addEventListener('keydown',e=>{const w=e.target.closest?.('.field-inline');if(!w||e.isComposing)return;
 if(e.key==='Enter'&&e.target.matches('input')){e.preventDefault();fieldEditSave(w,e.target.value)}else if(e.key==='Escape'){e.preventDefault();e.stopPropagation();people(graphNode,true)}},true);
document.addEventListener('change',e=>{const w=e.target.closest?.('.field-inline');if(w&&e.target.matches('select'))fieldEditSave(w,e.target.value)});
// The picture: upload one (made small here, before it leaves the browser), pick one found for them, or remove it.
const picSmall=src=>new Promise((ok,no)=>{const im=new Image();im.onload=()=>{const k=Math.min(1,256/Math.max(im.naturalWidth,im.naturalHeight)),c=document.createElement('canvas');c.width=Math.max(1,Math.round(im.naturalWidth*k));c.height=Math.max(1,Math.round(im.naturalHeight*k));
 const g=c.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,c.width,c.height);g.drawImage(im,0,0,c.width,c.height);let q=.85,u=c.toDataURL('image/jpeg',q);while(u.length>60000&&q>.3)u=c.toDataURL('image/jpeg',q-=.15);ok(u)};im.onerror=()=>no(new Error('That isn’t a picture this browser can read.'));im.src=src});
async function picOpen(node){const org=String(node).startsWith('org:'),pic=$('#people-view .graph-detail>.name-row .pic-edit')?.innerHTML||'';crm={mode:'picture',node,org};
 $('#crm-form').innerHTML=crmHead('Picture')+`<div class="pic-now">${pic}</div>`
  +`<div class="pic-pick"><label class="crm-file"><input name="pic" type="file" accept="image/png,image/jpeg,image/webp,image/gif"><span class="crm-file-name">Upload a picture</span></label></div>`
  +`<fieldset class="pic-found" hidden><legend>Found for ${org?'it':'them'}</legend><div class="pic-grid" data-pic-found></div></fieldset>`
  +`<p class="ed-note warn" data-crm-error role="alert" hidden></p><div class="ed-actions">${/<img/.test(pic)?'<button type="button" class="ghost danger" data-pic-remove>Remove picture</button>':''}<span class="grow"></span><button type="button" class="ghost" data-crm-close>Close</button></div>`;
 crmShow();
 try{const r=await graphPost('graph_pictures_found',{node_id:node});if(crm?.node!==node||!r.found?.length)return;const box=$('#crm-form [data-pic-found]');
  box.innerHTML=r.found.map((u,i)=>`<button type="button" class="pic-option" data-pic-found-i="${i}" aria-label="Use this picture"><img src="${esc(u)}" alt="" width="56" height="56"></button>`).join('');crm.found=r.found;box.parentElement.hidden=false}catch{}}
async function picSave(args,done){const c=crm;if(!c)return;crmSay('');$('#crm-form').querySelectorAll('button,input').forEach(x=>x.disabled=true);
 try{await graphPost('graph_picture',{node_id:c.node,...args});$('#crm-dialog').close();toast(done);pagerDrop('graph');await people(graphNode,true)}
 catch(x){errCaught(x);crmSay(x.message);$('#crm-form').querySelectorAll('button,input').forEach(x=>x.disabled=false)}}
document.addEventListener('click',e=>{const b=e.target.closest('[data-pic-edit]');if(!b)return;e.preventDefault();picOpen(b.dataset.picEdit)});
$('#crm-form').addEventListener('click',async e=>{const c=crm;if(c?.mode!=='picture')return;
 if(e.target.closest('[data-pic-remove]')){e.preventDefault();return picSave({remove:true},'Removed.')}
 const o=e.target.closest('[data-pic-found-i]');if(o){e.preventDefault();try{picSave({data:await picSmall(c.found[+o.dataset.picFoundI])},'Saved.')}catch(x){errCaught(x);crmSay(x.message)}}});
$('#crm-form').addEventListener('change',e=>{const c=crm;if(c?.mode!=='picture'||e.target.name!=='pic')return;const file=e.target.files?.[0];if(!file)return;
 if(file.size>15*1024*1024)return crmSay('That picture is too big: up to 15 MB.');const r=new FileReader();r.onload=async()=>{try{picSave({data:await picSmall(r.result)},'Saved.')}catch(x){errCaught(x);crmSay(x.message)}};r.readAsDataURL(file)});
async function crmFieldsSave(c){for(const f of c.fields){const now=String($('#crm-form').elements['f'+f.id]?.value??'').trim();if(now===String(f.value??''))continue;
  await graphPost('graph_field_set',{node_id:c.node,field_id:f.id,value:now})}
 $('#crm-dialog').close();toast('Saved.');graphFieldsStale=false;await people(graphNode,true)}
$('#crm-dialog').addEventListener('close',()=>{if(graphFieldsStale){graphFieldsStale=false;people(graphNode,true)}});
document.addEventListener('keydown',async e=>{const i=e.target.closest?.('.tag-add input');if(!i||e.key!=='Enter'||e.isComposing)return;e.preventDefault();const f=i.parentElement,t=i.value.trim();if(!t)return;i.disabled=true;i.blur();
 try{await graphPost('graph_tag',{node_id:f.dataset.tagNode,tag:t,add:true});if(!graphTags.some(x=>x.tag.toLowerCase()===t.toLowerCase())){graphTags.push({tag:t,count:1});tagsPaint()}pagerDrop('graph');await people(graphNode,true)}catch(err){errCaught(err);toast(err.message,true);i.disabled=false}},true);
document.addEventListener('click',async e=>{const t=e.target.closest('[data-tag-remove],[data-fields-edit]');if(!t)return;e.preventDefault();e.stopPropagation();
 try{if(t.dataset.fieldsEdit)return await crmFieldsOpen(t.dataset.fieldsEdit);t.disabled=true;await graphPost('graph_tag',{node_id:t.dataset.tagNode,tag:t.dataset.tagRemove,add:false});pagerDrop('graph');await people(graphNode,true)}catch(err){errCaught(err);toast(err.message,true);t.disabled=false}},true);
$('#people-view').onclick=async e=>{const tab=e.target.closest('[data-graph-pane]');if(tab){showGraphPane(tab.dataset.graphPane);return}if(e.target.closest('[data-ge-more]')){const n=graphTl.page,box=e.target.closest('.graph-timeline'),hidden=box?box.querySelectorAll('.graph-events .graph-event[hidden]').length:0;
  if(n?.timeline&&box){if(n.timeline.next&&hidden<30)graphTlLoad(n.timeline.source||'',true);else{n.timeline.shown=(n.timeline.shown||GRAPH_ROWS)+30;graphTlDraw()}}
  else{for(const x of $('#people-view').querySelectorAll('.graph-events [hidden]'))x.hidden=false;e.target.closest('[data-ge-more]').remove()}return}
 const soonAll=e.target.closest('[data-ge-soon]');if(soonAll){for(const x of soonAll.closest('.ge-soon').querySelectorAll('[hidden]'))x.hidden=false;soonAll.remove();return}
 const tlChip=e.target.closest('[data-tl-source]');if(tlChip){graphTlLoad(tlChip.dataset.tlSource,false);return}if(openEventFrom(e))return;
 const q=e.target.closest('[data-quote-event]');if(q){openEvent(q.dataset.quoteEvent,'');return}
 const all=e.target.closest('[data-role-all]');if(all){const each=[...document.querySelectorAll('.whos [data-role-confirm]')];if(!each.length||!confirm(`Mark all ${each.length} roles as right?`))return;all.disabled=true;let done=0;try{for(const b of each){await graphPost('graph_role',{node_id:b.dataset.roleConfirm,role:b.dataset.role});done++}toast(`Confirmed ${done} roles.`)}catch(err){errCaught(err);toast((done?`Confirmed ${done}, then: `:'')+err.message,true)}await people(graphNode,true);return}
 const undo=e.target.closest('[data-warmup-undo]');if(undo){undo.disabled=true;try{await graphPost('graph_warmup',{domain:undo.dataset.warmupUndo,warmup:false});toast(t('Back in your Graph: {}.',undo.dataset.warmupUndo));await people(graphNode,true)}catch(err){errCaught(err);undo.disabled=false;toast(err.message,true)}return}
 const ok=e.target.closest('[data-role-confirm]');if(ok){ok.disabled=true;try{await graphPost('graph_role',{node_id:ok.dataset.roleConfirm,role:ok.dataset.role});toast(t('Confirmed: {}.',ok.dataset.role));await people(graphNode,true)}catch(err){errCaught(err);ok.disabled=false;toast(err.message,true)}return}
 const ed=e.target.closest('[data-role-edit-for]');if(ed){editRole=ed.dataset.roleEditFor;graphOpen(ed.dataset.roleEditFor);return}
 const sameAll=e.target.closest('[data-same-all]');if(sameAll){const pairs=JSON.parse(sameAll.dataset.sameAll);if(!confirm(`Merge ${pairs.length} pairs?`))return;sameAll.disabled=true;
  try{const said=await graphPost('graph_same_all',{pairs});toastUnmerge(said.merged===1?'Merged 1 pair.':`Merged ${said.merged} pairs.`,said.batch);await people(graphNode,true)}catch(err){errCaught(err);sameAll.disabled=false;toast(err.message,true)}return}
 const same=e.target.closest('[data-same]');if(same){const yes=same.dataset.same==='1';same.disabled=true;try{await graphPost('graph_same',{a:same.dataset.a,b:same.dataset.b,same:yes});toast(yes?'Merged.':same.matches('[data-split]')?'Split. Won’t be joined again.':'Kept apart.');await people(graphNode,true)}catch(err){errCaught(err);same.disabled=false;toast(err.message,true)}return}
 const un=e.target.closest('[data-unrelate]');if(un){un.disabled=true;try{await graphPost('graph_relation',{node_id:un.dataset.unrelate,related_to:un.dataset.relatedTo,relation:''});toast('Removed.');await people(graphNode,true)}catch(err){errCaught(err);un.disabled=false;toast(err.message,true)}return}const del=e.target.closest('[data-person-delete],[data-person-delete-no],[data-person-delete-yes]');if(del){const ask=$('#people-view .person-delete-confirm');
  if(del.matches('[data-person-delete]')){del.closest('details').open=false;const nf=$('#people-view .name-form');if(nf)nf.hidden=true;ask.hidden=false;ask.querySelector('[data-person-delete-no]').focus();return}
  if(del.matches('[data-person-delete-no]')){ask.hidden=true;return}
  del.disabled=true;try{await graphPost('graph_person_delete',{node_id:graphNode});toast('Deleted. Won’t be added again.');graphBack('people')}catch(err){errCaught(err);del.disabled=false;toast(err.message,true)}return}const wrong=e.target.closest('[data-org-wrong],[data-org-lookup]');if(wrong){const w=wrong.matches('[data-org-wrong]');if(w&&!confirm('Clear the looked-up details? This domain won’t be looked up again until you ask.'))return;wrong.disabled=true;try{await graphPost('graph_org_wrong',{node_id:graphNode,wrong:w});const of=$('#people-view .org-form');if(of)orgOpen(of,false);toast(w?'Cleared.':'It will be looked up again soon.');await people(graphNode,true)}catch(err){errCaught(err);wrong.disabled=false;toast(err.message,true)}return}
 const add=e.target.closest('[data-pf-add]');if(add){const list=add.previousElementSibling;list.insertAdjacentHTML('beforeend',pfItem(add.dataset.pfAdd,''));list.lastElementChild.querySelector('input').focus();return}
 const rm=e.target.closest('[data-pf-remove]');if(rm){if(rm.closest('.pf-list-field')?.querySelector('[aria-invalid]'))pfErrClear(rm);const item=rm.closest('.pf-item'),next=item.nextElementSibling||item.previousElementSibling;item.remove();(next?.querySelector('input')||e.target.closest('.pf-list-field')?.querySelector('[data-pf-add]'))?.focus();return}
 if(e.target.closest('[data-org-cancel]')){const f=$('#people-view .org-form');orgOpen(f,false);if(f.matches('.person-form'))people(graphNode,true);return}
 if(e.target.closest('[data-org-edit]')){const f=$('#people-view .org-form');orgOpen(f,true);f.querySelector('input,textarea').focus({preventScroll:true});return}
 if(e.target.closest('[data-name-edit]')){const f=$('#people-view .name-form');f.hidden=!f.hidden;if(!f.hidden){f.elements[0].focus();f.elements[0].select()}return}const crumb=e.target.closest('[data-crumb]');if(crumb){e.preventDefault();graphBack(crumb.dataset.crumb);return}
 const unlink=e.target.closest('[data-fact-unlink]');if(unlink){unlink.disabled=true;try{await graphPost('graph_fact_unlink',{fact_id:Number(unlink.dataset.factUnlink),node_id:graphNode});toast('Taken off this page. Still in what I’ve learned.');await people(graphNode,true)}catch(err){errCaught(err);unlink.disabled=false;toast(err.message,true)}return}
 const forget=e.target.closest('[data-fact-forget]');if(forget){const text=forget.closest('li')?.querySelector('span')?.textContent||'';if(!confirm(`Forget this everywhere?\n\n“${text}”\n\nIt is deleted from this page and from everything your Machine has learned, for good. To only take it off this page, choose Not about ${forget.dataset.who} instead.`))return;forget.disabled=true;try{await graphPost('forget_fact',{id:Number(forget.dataset.factForget)});toast('Forgotten everywhere.');await people(graphNode,true)}catch(err){errCaught(err);forget.disabled=false;toast(err.message,true)}return}
 const b=e.target.closest('[data-node]');if(b&&b.dataset.node)graphOpen(b.dataset.node)};
$('#people-view').onsubmit=async e=>{const pf=e.target.closest('.person-form');if(pf){e.preventDefault();const b=$('#people-view [data-org-save]'),fields=personChanged(pf);
  const errs=personCheck(fields);personErrors(pf,errs);if(errs.length)return;if(!Object.keys(fields).length){orgOpen(pf,false);return}
  if(b)b.disabled=true;try{await graphPost('graph_person_edit',{node_id:pf.dataset.nodeId,fields});orgOpen(pf,false);toast('Saved.');await people(graphNode,true)}
  catch(err){errCaught(err);const k=personErrField(err.message);if(k&&k in fields)personErrors(pf,[[k,err.message]]);else toast(err.message,true)}finally{if(b?.isConnected)b.disabled=false}return}
 const o=e.target.closest('.org-form');if(o){e.preventDefault();const b=$('#people-view [data-org-save]');const changed=Object.fromEntries(ORG_FIELDS.map(([k])=>o.elements[k]).filter(f=>f.value.trim()!==f.defaultValue.trim()).map(f=>[f.name,f.value.trim()]));const {name,...fields}=changed;  /* only what the owner changed becomes theirs */
  const r=o.elements.role,role=r&&r.value.trim()!==r.defaultValue.trim()?r.value.trim():undefined;
  const errs=[...orgCheck(changed),...(role&&role.length>60?[['role',`Up to 60 characters (now ${role.length})`]]:[])];orgErrors(o,errs);if(errs.length)return;if(!Object.keys(changed).length&&role===undefined){orgOpen(o,false);return}
  if(b)b.disabled=true;try{if(Object.keys(changed).length)await graphPost('graph_org_edit',{node_id:o.dataset.nodeId,fields,...(name!==undefined?{name}:{})});if(role!==undefined)await graphPost('graph_role',{node_id:o.dataset.nodeId,role});orgOpen(o,false);toast('Saved.');await people(graphNode,true)}
  catch(err){errCaught(err);const k=ORG_FIELDS.find(([k,t])=>new RegExp('^('+t.split(' ')[0]+'|'+k.replace('_url','').replace('_',' ')+')\\b','i').test(err.message))?.[0];if(k&&k in changed)orgErrors(o,[[k,err.message]]);else toast(err.message,true)}finally{if(b?.isConnected)b.disabled=false}return}
 const n=e.target.closest('.name-form');if(n){e.preventDefault();const b=n.querySelector('button');b.disabled=true;try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'graph_rename',args:{node_id:n.dataset.nodeId,name:n.newname.value.trim()}})});n.hidden=true;toast(r.merged?'Joined '+r.name+'.':'Renamed.');await people(r.node_id||graphNode,true)}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}return}};
// Typing searches after a short pause, Enter and Find at once; an empty box is the list again, with no wait.
let graphTyping=0;const graphFind=()=>{clearTimeout(graphTyping);people('')};
$('#people-find').onclick=graphFind;$('#people-query').onkeydown=e=>{if(e.key==='Enter')graphFind()};
$('#people-query').oninput=()=>{clearTimeout(graphTyping);if(!$('#people-query').value.trim()){graphFind();return}graphTyping=setTimeout(()=>people(''),150)};
