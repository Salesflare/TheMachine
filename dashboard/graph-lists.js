// When something last happened, as people say it (last contact, last signal; with ago()'s relativeFmt): just now, 5 minutes ago, 3 hours ago (the
// same day), yesterday, 3 days ago, then a short date (Oct 29 or 29 Oct, with the year when it isn't this one), in the
// owner's date locale. A day without a time of day (2026-11-10) never claims hours: today. sinceTime is the same as a
// <time> whose hover has the exact date.
const sinceAt=v=>{const s=String(v||''),only=s.length<=10,d=new Date(only?s+'T12:00':s);return !v||isNaN(d)?null:{d,only}};
const sinceWhen=v=>{const p=sinceAt(v);if(!p)return v?String(v):t('never');const {d,only}=p,now=new Date(),f=relativeFmt(DL),s=(now-d)/1000,
  days=Math.round((new Date(localDay(now)+'T12:00')-new Date(localDay(d)+'T12:00'))/864e5);
 if(!only&&s>-60&&s<3600)return s<60?t('just now'):f.format(-Math.floor(s/60),'minute');
 if(!only&&days===0&&s>0)return f.format(-Math.floor(s/3600),'hour');
 if(days>=0&&days<7)return f.format(-days||0,'day');  // today, yesterday, 3 days ago
 return localeDate(d,DL,{day:'numeric',month:'short',...(d.getFullYear()!==now.getFullYear()?{year:'numeric'}:{})})};
const sinceTitle=v=>{const p=sinceAt(v);if(!p)return '';const o={weekday:'long',day:'numeric',month:'long',year:'numeric'};return p.only?localeDate(p.d,DL,o):fmtDHM(p.d,o)};
const sinceTime=v=>sinceAt(v)?html`<time datetime="${v}" title="${sinceTitle(v)}">${sinceWhen(v)}</time>`:sinceWhen(v);
$('#people-view').addEventListener('click',async e=>{const b=e.target.closest('[data-fleet-ask]');if(!b)return;b.disabled=true;
 try{await fleetPost('fleet_ask',{kind:'relationships',question:{about:b.dataset.fleetAsk}});toast('Asked your Fleet. The answers show in the Fleet tab.')}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
// Graph and Fleet tab link to each other: a member's person in the Graph, a person's place in the Fleet tab.
$('#people-view').addEventListener('click',async e=>{const keep=e.target.closest('[data-fleet-keep]');
 if(keep){keep.disabled=true;try{await graphPost('graph_rename',{node_id:graphNode,name:keep.dataset.fleetKeep});toast('Kept. It stays if they leave.');await people(graphNode,true)}catch(err){errCaught(err);keep.disabled=false;toast(err.message,true)}return}
 const b=e.target.closest('[data-fleet-member],[data-fleet-free]');if(!b)return;document.querySelector('nav [data-tab="fleet"]')?.click();await fleetShown;
 const el=b.dataset.fleetMember?document.getElementById('fleet-m-'+b.dataset.fleetMember):document.querySelector(`.fleet-free-form[data-fleet="${CSS.escape(b.dataset.fleetFree)}"]`);if(!el)return;
 fleetReveal(el);el.scrollIntoView({block:'center',behavior:'smooth'});if(b.dataset.fleetFree)el.querySelector('input')?.focus({preventScroll:true});else{el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash')}});
$('#fleet-view').addEventListener('click',e=>{const b=e.target.closest('[data-graph-open]');if(!b)return;e.preventDefault();graphNode=b.dataset.graphOpen;document.querySelector('nav [data-tab="people"]')?.click()});
// orgPic and personPic (with their initials, ring and fallbacks) are the to-do chips' own (todos-cards.js).
// The owner changes a person's or organization's picture from its page; a teammate's record shows theirs as it is.
const picEdit=(n,pic)=>n.team_only?pic:html`<button type="button" class="pic-edit" data-pic-edit="${n.id}" title="Change picture" aria-label="Change picture">${pic}</button>`;
const nodeButton=n=>html`<button class="node" data-node="${n.id}" title="${n.name}">${n.name}</button>`;
const PROJECT_COLOR={'heating up':'var(--amber)','active':'var(--mint)','cooling':'var(--lavender)','dormant':'var(--faint)'};
// A project's activity against two weeks ago (graph.project_state), in plain words; the title says what it compares
const PROJECT_HEAT={'heating up':['Busier lately','More messages and meetings than two weeks ago'],active:['Steady','About as busy as two weeks ago'],
 cooling:['Quieter lately','Fewer messages and meetings than two weeks ago'],dormant:['Quiet','No recent messages or meetings']};
const heatLabel=s=>t(PROJECT_HEAT[s]?.[0]||s);
const heatChip=s=>s?html`<span class="chip" style="--c:${PROJECT_COLOR[s]||'var(--muted)'}" title="${t(PROJECT_HEAT[s]?.[1]||'')}">${heatLabel(s)}</span>`:'';
const bar=n=>html`<span class="graph-bar" title="${n.closeness?t(n.closeness[0].toUpperCase()+n.closeness.slice(1)+' (a closeness)'):''}"><i style="width:${Math.min(100,Math.round(100*Math.log1p(n.strength)/Math.log1p(12)))}%"></i></span>`;
const CLOSENESS_UI={close:'Close (a closeness)',regular:'Regular (a closeness)',occasional:'Occasional (a closeness)',faint:'Faint (a closeness)'};
// A person's line: plain text for a hover (text), else with the last contact as a <time> whose hover has its exact date
const personSub=(p,text)=>{const last=p.seen_only?'last seen {}':'last contact {}',parts=[p.profile?.title,p.role?t(cap(p.role)):CLOSENESS_UI[p.closeness]?t(CLOSENESS_UI[p.closeness]):cap(p.closeness),!p.last_at?'':text?t(last,sinceWhen(p.last_at)):htmlT(last,sinceTime(p.last_at)),p.usual_gap_days?(Math.round(p.usual_gap_days)<=1?t('usually daily'):t('usually every {} days',Math.round(p.usual_gap_days))):'',p.next_meeting?t('meeting {}',day(p.next_meeting)):''].filter(Boolean);
 return text?parts.join(' · '):html`${parts.map((x,i)=>html`${i?' · ':''}${x}`)}`};
// What The Machine updated today (graph_updates.py): a quiet dot on each row it changed, and one line on top of each
// list that opens what changed. A name there opens its page with Recent changes open. Nothing moves or counts up.
let graphToday=null;
const TODAY_LINE={people:['Updated {} person today','Updated {} people today'],orgs:['Updated {} organization today','Updated {} organizations today'],projects:['Updated {} project today','Updated {} projects today']};
const todayMark=n=>n.updated_at?html`<span class="today-mark" role="img" aria-label="${t('Updated today')}" title="${t('Updated today')}"></span>`:'';
const todayLine=pane=>{const d=graphToday?.[pane];if(!d?.count)return'';
 return html`<details class="graph-today"><summary><span class="today-mark" aria-hidden="true"></span><span>${t(TODAY_LINE[pane],d.count)}</span></summary><ul class="today-list">${d.items.map(x=>html`<li><button type="button" class="link" data-today-open="${x.id}">${x.name}</button><span class="today-what">${rcText({},x.change)}</span></li>`)}</ul></details>`};
$('#people-view').addEventListener('click',e=>{const b=e.target.closest('[data-today-open]');if(!b)return;rcOpen=b.dataset.todayOpen;graphOpen(b.dataset.todayOpen)});
const graphItem=n=>n.kind==='me'?html`<article class="tap person-item about-you-row" data-node="me"><div class="graph-row one">${personPic({name:'You'})}${nodeButton({id:'me',name:'About you'})}</div><p class="graph-sub">Your own addresses and numbers</p></article>`
 :n.kind==='project'?html`<article class="tap" data-node="${n.id}"><div class="graph-row">${nodeButton(n)}${todayMark(n)}${tagMini(n)}${heatChip(n.state)}</div><p class="graph-sub" style="white-space:normal">${n.team_only?'':html`${n.last_at?html`${htmlT('Last signal {}',sinceTime(n.last_at))} · `:''}${t(['{} signal','{} signals'],n.signals)}${n.next_meeting?' · '+t('next meeting {}',day(n.next_meeting)):''}`}${n.org_node?html`${' · '}${orgLink(n.org_node)}`:''}${n.people?.length?' · '+n.people.join(', '):''}${n.via?html`<span class="via">${n.team_only?'':' · '}${n.via}</span>`:''}</p></article>`
 :n.kind==='org'?html`<article class="tap" data-node="${n.id}"><div class="graph-row">${orgPic(n)}${nodeButton(n)}${todayMark(n)}${tagMini(n)}<small>${n.role?t(cap(n.role))+' · ':''}${n.profile?.industry?n.profile.industry+' · ':''}${[n.team_only?'':t(['{} person','{} people'],n.signals),n.last_at?htmlT('last contact {}',sinceTime(n.last_at)):''].filter(Boolean).map((x,i)=>html`${i?' · ':''}${x}`)}${n.via?html` · <span class="via">${n.via}</span>`:''}</small></div></article>`
 :html`<article class="tap person-item" data-node="${n.id}"><div class="graph-row one">${personPic(n)}${nodeButton(n)}${todayMark(n)}${tagMini(n)}${fleetChip(n,'row')}${n.quiet?html`<span class="chip" style="--c:var(--orange)">${t('gone quiet')}</span>`:''}${bar(n)}</div><p class="graph-sub" title="${personSub(n,true)+(n.ids?.length?' · '+n.ids.slice(0,2).join(', '):'')}">${fleetChip(n,'sub')}${n.via?html`<span class="via">${n.via}</span> · `:''}${n.fleet?.machine?t('Has a Machine')+' · ':''}${personSub(n)}${n.org_name&&n.team_only?' · '+n.org_name:''}${n.ids?.length?html`${' · '}${n.ids.slice(0,2).join(', ')}${bounceNote(n.ids.slice(0,2).map(i=>n.bounced?.[String(i).replace(/^email:/,'').toLowerCase()]).find(Boolean))}`:''}</p></article>`;
// Each Graph page's lists are tabs that filter (with their counts; an empty one is not shown) and a quiet menu sets the
// order; every pair is one list on the Machine, loaded a page at a time. The pick is kept per page, also after a person.
const GRAPH_TABS={people:{label:'People',tabs:[['people','All'],['quiet','Gone quiet'],['new','New this week'],['work','Work'],['personal','Personal']],sorts:[['closest','Closest'],['last','Newest contact'],['last_old','Oldest contact'],['name','Name A–Z']],
  notes:{people:'From your messages, meetings and to-dos. Fades over about two months.',quiet:'People you talk with regularly, silent for much longer than usual.',new:'First seen this week.',work:'Work contacts.',personal:'Personal contacts.'},empty:'Nobody here yet.'},
 orgs:{label:'Organizations',tabs:[['orgs','All'],['warmup','Warm up']],sorts:[['closest','Closest'],['last','Newest contact'],['last_old','Oldest contact'],['name','Name A–Z'],['size','Size']],
  notes:{orgs:'The ones you are most in touch with first.',warmup:'Mail from email warm-up tools, kept out of your Graph.'},empty:'No organizations yet.'},
 projects:{label:'Projects',tabs:[['projects','Open'],['projects_done','Done']],sorts:[['last','Last activity'],['name','Name A–Z'],['stage','Stage'],['value','Value'],['close','Close date']],
  notes:{projects:'Named by the checks and your to-dos. Busier or quieter compares the last two weeks.',projects_done:'Closed projects.'},empty:'No projects yet.'}};
// A Graph page with nothing on it yet still opens: a short line says how it fills, and its head keeps + New.
// People with nobody yet says what the graph read (g.read): all of it automated, so people come with real conversations.
const GRAPH_READ=[['email',['{} email','{} emails']],['meeting',['{} meeting','{} meetings']],['message',['{} message','{} messages']]];
function graphReadLine(read){const parts=GRAPH_READ.filter(([k])=>(+read?.[k]|0)>0).map(([k,w])=>t(w,+read[k]|0).replace(/^(\d+) /,'$1\u00a0'));if(!parts.length)return '';
 let list;try{list=new Intl.ListFormat(I18N.lang||'en',{type:'conjunction'}).format(parts)}catch{list=parts.join(', ')}return t('Read {}, all automated.',list)+' '+t('People show up as real conversations come in.')}
const graphEmpty=(pane,team,read)=>{const w=team?[]:teamWaits(graphSharing);if(w.length)return html`<div class="empty all-clear graph-empty team-wait"><img class="sticker" src="brand/thinking.webp" alt=""><div>${w.map(s=>html`<strong>${teamWaitLine(s)}</strong>`)}<span class="poke-line">${t('The team\'s records show here then.')}</span></div></div>`;  /* before an admin's OK: whose OK, in place of how it fills */
 const [title,how]={people:['Nothing mapped yet.',graphReadLine(read)||'People appear as messages and meetings come in.'],orgs:['No organizations yet.','They come from the people you’re in touch with.'],projects:['No projects yet.','Your Machine finds them in your messages and to-dos.']}[pane];
 return html`<div class="empty all-clear graph-empty"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>${title}</strong>${team?'':html`<span class="poke-line">${how}</span>`}</div></div>`};
const TEAM_NOTES={people:'Everyone your team shares, the closest first.',orgs:'The ones your team is most in touch with.',projects:'Your team’s open projects.'};
const graphPick=(pane,what,fallback)=>{try{return localStorage.getItem(`graph-${what}-${pane}`)||fallback}catch{return fallback}};
const graphKeep=(pane,what,v)=>{try{localStorage.setItem(`graph-${what}-${pane}`,v)}catch{}};
function graphStash(view){if(view.dataset.mode!=='list'||!view.firstChild)return;const scroll=scrollY,f=document.createDocumentFragment();f.append(...view.childNodes);graphKept={f,scroll}}
function graphUnstash(view){if(!graphKept)return false;const k=graphKept;graphKept=null;view.replaceChildren(k.f);view.dataset.mode='list';
 for(const el of view.querySelectorAll('[data-pager]')){const p=pagers.get(el.dataset.pager);if(p&&el.querySelectorAll('.pager-rows>*').length!==p.items.length)el.replaceChildren()}pagerMount(view);  /* rows a page brought in meanwhile */
 notice('');requestAnimationFrame(()=>{if(view.querySelector(`[data-graph-panel="${CSS.escape(graphPane)}"]`))showGraphPane(graphPane,true);if(!$('#people').hidden)scrollTo(0,k.scroll)});return true}  /* the layout waits for the frame, still before it paints; another tab on screen meanwhile keeps its own place */
let graphLists={},graphLocal=null,graphListsTeam=false;  // a Machine from before the paged lists sends them whole in the overview: they are sorted here
const GRAPH_STAGE={active:0,cooling:1,dormant:2};
const crmHeads=n=>+n.profile?.employees||parseInt(n.profile?.size)||0;
const graphSorted=(items,sort)=>[...items].sort(sort==='name'?(a,b)=>(a.name||'').localeCompare(b.name||'',undefined,{sensitivity:'base'}):sort==='last'?(a,b)=>String(b.last_at||'').localeCompare(String(a.last_at||'')):sort==='last_old'?(a,b)=>!a.last_at-!b.last_at||String(a.last_at).localeCompare(String(b.last_at)):sort==='size'?(a,b)=>crmHeads(b)-crmHeads(a):sort==='stage'?(a,b)=>(GRAPH_STAGE[a.state]??3)-(GRAPH_STAGE[b.state]??3)||(b.strength||0)-(a.strength||0):(a,b)=>(b.strength||0)-(a.strength||0));
const warmRow=w=>html`<div class="graph-sub relation"><span>${w.name||w.domain}${w.name&&w.name!==w.domain?html` <span class="muted">${w.domain}</span>`:''}</span><button class="ghost" data-warmup-undo="${w.domain}">Undo</button></div>`;
// A list's first page comes from the device at first (cachedGet); the live one, when different, redraws the Graph quietly
const graphFresh=()=>{pagerDrop('graph');if(!$('#people').hidden&&!graphNode)people(graphNode,true)};
function graphListPager(list,sort){const fq=graphLocal?'':crmQuery(list),p=pager(crmKey(list,sort),cursor=>graphLocal?Promise.resolve({items:graphSorted(teamKept(list),list==='warmup'?'name':sort),next:null}):(path=>cursor==='0'?cachedGet(path,graphFresh):request(path))(`api/graph/list?list=${list}&sort=${sort}${fq}&cursor=${encodeURIComponent(cursor)}`).then(r=>({items:r.items,next:r.next,total:r.total})),list==='warmup'?warmRow:graphItem);
 if(graphLocal&&!p.items.length&&p.next==='0'){p.items=graphSorted(teamKept(list),list==='warmup'?'name':sort);p.html=html`${p.items.map(p.row)}`;p.next=null}return p}
// The tabs, the order menu and the list sit in their own box, so a tab or order change repaints only them (a Projects
// pane also holds the board)
function graphTabs(pane){const h=graphTabsInner(pane);return h&&html`<div data-graph-box="${pane}">${h}</div>`}
function graphTabsInner(pane){const g=GRAPH_TABS[pane],shown=g.tabs.filter(([id])=>graphLists[id]>0&&!(graphListsTeam&&id==='warmup'));if(!shown.length)return'';
 const tab=shown.some(([id])=>id===graphPick(pane,'tab',''))?graphPick(pane,'tab',''):shown[0][0],sort=g.sorts.some(([id])=>id===graphPick(pane,'sort',''))?graphPick(pane,'sort',''):g.sorts[0][0];
 graphListPager(tab,sort);const label=g.sorts.find(([id])=>id===sort)[1];
 const menu=tab==='warmup'?'':html`<details class="graph-sort"><summary aria-label="Order: ${label}">${label} <span aria-hidden="true">▾</span></summary><div class="graph-sort-list" role="menu">${g.sorts.map(([id,t])=>html`<button type="button" role="menuitemradio" aria-checked="${id===sort}" data-graph-sort="${id}">${t}</button>`)}<hr><button type="button" role="menuitem" data-graph-csv="${tab}" data-sort="${sort}">Download CSV</button>${graphLocal?'':html`<button type="button" role="menuitem" data-crm-import="${pane}">Import CSV…</button>${graphLastImport?html`<button type="button" role="menuitem" data-crm-undo-import="${graphLastImport.id}">Undo last import</button>`:''}`}</div></details>`;
 return html`<div class="graph-tabbar" data-graph-tabs="${pane}">${subTabs(g.label,'data-graph-list',shown.map(([id,t])=>({id,label:t})),tab)}${tab==='warmup'||graphLocal&&!graphListsTeam?'':crmTools(pane,tab)}${menu}</div>${tab==='warmup'||graphLocal&&!graphListsTeam?'':crmActive(pane)}${(graphListsTeam?TEAM_NOTES[tab]:g.notes[tab])?html`<p class="graph-note muted">${graphListsTeam?TEAM_NOTES[tab]:g.notes[tab]}</p>`:''}${pagerSlot(crmKey(tab,sort),crmCount(pane)?'Nothing matches these filters.':g.empty,'graph-list')}`}
function graphTabsPaint(pane){const box=document.querySelector(`[data-graph-panel="${pane}"] [data-graph-box]`);if(!box)return;setHTML(box,graphTabsInner(pane));pagerMount(box);tabsShow(box.querySelector('.sub-tabs'))}
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
const graphSection=(title,note,items)=>items?.length?html`<div class="section-head"><h2>${title}</h2><span class="count">${items.length}</span>${note?html`<p>${note}</p>`:''}</div><div class="graph-list">${items.map(graphItem)}</div>`:'';
// Why two people look like one (graph.py likely_same): its parts, each in the language
const sameWhy=w=>String(w||'').split(', ').map(x=>{const m=/^both at (.+)$/.exec(x);return m?t('both at {}',m[1]):t(x)}).join(', ');
const fleetGroups=n=>[...new Set((n.fleet?.in||[]).map(x=>({work:'Fleet',family:'Family',friends:'Friend'})[x.kind]||x.label))].join(' · ');
const fleetLine=n=>[n.fleet?.machine?'Has a Machine':'',...(n.fleet?.in||[]).map(x=>x.kind==='work'&&x.fleet_name?`${x.label} (${x.fleet_name})`:x.label)].filter(Boolean).join(' · ');
const fleetChip=(n,where)=>n.fleet?.in?.length?html`<span class="chip fleet-chip${where?' fleet-chip-'+where:''}" style="--c:var(--mint)" title="${fleetLine(n)}"><span class="ct">${fleetGroups(n)}</span></span>`:'';
function fleetAskRow(n){if(!state?.fleet?.on||!['person','org'].includes(n.kind)||n.fleet?.in?.some(x=>x.kind==='work'))return'';const about=n.kind==='org'?(n.domain||n.name):/^email:/.test(n.id)?n.id.slice(6):n.name;
 return html`<p class="graph-sub detail-fleet-ask"><button type="button" class="link" data-fleet-ask="${about}">Ask the Fleet who knows ${n.name||about}</button></p>`}
function sharePop(chip){const s=JSON.parse(chip.dataset.share||'{}'),on=graphSharing.find(x=>x.confirmed),fleet=on?.fleet,before=on?.started===false;const team=s.share==='team';
 sharePopAt(chip,html`<p class="share-pop-why">${s.why||(team?'Shared with your team':'Only you')}</p>${s.people?.length?html`<p class="share-pop-why">Shared with ${namesLine(s.people)}</p>`:''}${s.fixed?'':html`<div class="actions"><button type="button" class="${team?'ghost':'primary'}" data-pop-set="${chip.dataset.shareEvent}" data-share="${team?'only_you':'team'}"${before?html` data-before="1"`:''}>${team?(before?'Keep private':'Unshare'):'Share with the team'}</button>${!team&&graphTeammates.length?html`<button type="button" class="ghost" data-pop-people="${chip.dataset.shareEvent}">Share with…</button>`:''}</div>`}${team&&!s.fixed&&!before?html`<p class="fleet-fine muted">Unsharing deletes teammates' copies. Someone may have read it already.</p>`:''}${fleet?html`<p class="fleet-fine"><a href="#shared=${fleet}">See what's shared</a></p>`:''}`)}
// A summary chip's sources: chats as conversations, the rest folded.
async function openSources(ids,title){const dialog=$('#email-dialog'),box=$('#email-content');$('#email-title').textContent=title||t('Original');setHTML(box,html`<p class="muted">Loading…</p>`);if(!dialog.open)dialog.showModal();
let list;try{[{originals:list}]=await Promise.all([request('api/originals?events='+encodeURIComponent(ids)),lazyPart('msgview')])}catch(e){errCaught(e);setHTML(box,html`<p class="muted">${e.message}</p>`);return}
if(!list.length){setHTML(box,html`<p class="muted">The messages are no longer available.</p>`);return}
const rest=list.filter(o=>!isChat(o));
setHTML(box,html`${chatThreads(list).map(c=>chatThreadHTML(c))}${rest.map(o=>emailRow(o,list.indexOf(o)))}`);
box.querySelectorAll('details.email').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)fillMessage(d,list[+d.dataset.msg],'')}));}
