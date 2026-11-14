// Graph's state, links and helpers that the rest of the page uses too (To-dos, chat, Calendar, Fleet, Settings): its
// routes (#graph/<id>, #promise/<id>), sub-tabs, menus and labels. The Graph's own pages (graph-lists, -boards, -record,
// -tabs and -crm) load when first needed (dashboard_parts.LAZY); calls into them from here go through graphPeople()
// or lazyRun('graph', ...).
// A name or address cut off with an ellipsis shows in full on hover or long-press.
document.addEventListener('pointerover',e=>{const el=e.target.closest?.('.ct,.ell,.fleet-people strong,.fleet-people small');if(el&&!el.title&&el.scrollWidth>el.clientWidth)el.title=el.textContent.trim()});
// Graph tab: projects heating up or cooling, who's closest, who has gone quiet; tap one for its links and events.
const day=v=>v?localeDate(new Date(String(v).length<=10?v+'T12:00':v),DL,{weekday:'short',day:'numeric',month:'short'}):t('never');
const cap=t=>t?t[0].toUpperCase()+t.slice(1):t;
// While a search shows, the list it covers is kept as it was (tab, sort, pages loaded, scroll): emptying the box brings it back at once.
let graphKept=null;
document.addEventListener('keydown',e=>{if(e.key!=='Escape')return;const d=document.querySelector('.graph-sort[open],details.fact-menu[open],details.board-menu[open],details.tile-menu[open]');if(d){d.open=false;d.querySelector('summary').focus()}});
document.addEventListener('toggle',e=>{const d=e.target;if(!(d instanceof HTMLDetailsElement)||menuKept.delete(d)||!d.open)return;const l=d.querySelector(':scope>.fact-menu-list,:scope>.graph-sort-list');if(!l)return;l.style.left=l.style.right=l.style.top=l.style.bottom='';
 // A menu stays on screen: it moves in from an edge, and opens upward when there's no room under its button but there is above it
 let r=l.getBoundingClientRect();if(r.right>innerWidth-8){l.style.left='auto';l.style.right='0';r=l.getBoundingClientRect()}if(r.left<8){l.style.right='auto';l.style.left=(8-d.getBoundingClientRect().left)+'px'}
 const s=d.querySelector(':scope>summary')?.getBoundingClientRect();if(s&&r.bottom>innerHeight-8&&s.top-r.height-8>8){l.style.top='auto';l.style.bottom='calc(100% + 4px)'}},true);
// Projects as a board: projects of one kind in stages (graph.boards), a view of Graph › Projects next to the list. Board by
// default when there is a board; the choice is remembered on this device. Moves come from what the messages mean; the owner
// drags a tile (or picks a stage from its menu) and that stands until a newer message moves it. Nothing here sends anything.
let graphBoards=[],boardShown=sideStore.get('board-shown')||'',boardStage={},boardOpen=new Set(),fitsOpen=new Set(),fitsPicked=new Map(),fitsGoing=new Set();
const projView=()=>graphBoards.length?(sideStore.get('projects-view')==='list'?'list':'board'):'list';
const shortDay=v=>v?localeDate(new Date(String(v).length<=10?v+'T12:00':v),DL,{weekday:'short',day:'numeric',month:'short'}):'';  /* Fri, Oct 23 */
const seenBy=(v,names)=>v==='only_you'?html`<span class="seen-by">${LOCK}Only you</span>`:v==='people'?html`<span class="seen-by">${LOCK}${names?.length?'Shared with '+namesLine(names):'Chosen teammates'}</span>`:html`<span class="seen-by">Team</span>`;
const namesLine=n=>n.length<3?n.join(' and '):n.slice(0,-1).join(', ')+' and '+n[n.length-1];
// Projects by hand, like a deal in any CRM: make one (from the board, a stage, a person or an organization), edit its
// name, board and stage, organization, value, people and notes, mark it Won or Lost with why, archive or delete it.
// A move by hand stands until a newer message moves it. Reviews also add projects that fit a board; the ones they're
// unsure about wait under the board header ("2 projects could belong here") for Add or Leave out.
let graphMineBoards=null,graphPeopleNames=[],pj=null;
// A phone number grouped for reading: the country code (ITU zones), then the national number in short groups. One that
// already has spaces is shown as written. Tap and Copy use the number as stored.
const PHONE_CC2=/^(2[07]|3[0-469]|4[013-9]|5[1-8]|6[0-6]|8[1246]|9[0-58])/;
function phoneShown(v){const t=String(v||'').trim();if(!/^\+\d{8,15}$/.test(t))return t;const d=t.slice(1),cc=/^[17]/.test(d)?d[0]:PHONE_CC2.test(d)?d.slice(0,2):d.slice(0,3),n=d.slice(cc.length);
 const g=cc==='1'&&n.length===10?[n.slice(0,3),n.slice(3,6),n.slice(6)]:cc==='32'&&n.length===9?[n.slice(0,3),n.slice(3,5),n.slice(5,7),n.slice(7)]:cc==='32'&&n.length===8?[n.slice(0,1),n.slice(1,4),n.slice(4,6),n.slice(6)]
  :cc==='31'&&n.length===9?[n.slice(0,1),n.slice(1,5),n.slice(5)]:cc==='44'&&n.length===10?[n.slice(0,4),n.slice(4)]:cc==='33'&&n.length===9?[n.slice(0,1),...n.slice(1).match(/\d{2}/g)]
  :n.replace(/\B(?=(\d{3})+(?!\d))/g,' ').split(' ');
 return '+'+cc+' '+g.join(' ')}
// An address that bounced (bounces.py): "Bounced Oct 28", muted, beside it; never struck through, so it stays readable.
const bounceDay=v=>localeDate(new Date(v),DL,{day:'numeric',month:'short'});
const bounceNote=at=>at?html`<span class="bounce-note">${t('Bounced {}',bounceDay(at))}</span>`:'';
// A meeting still to come, compact: its day and time (All day for an all-day one), who else is on it.
const GE_SOON=3;
// The Shared Graph (shared_graph.py): Mine or Team, "via <name>", a thread's Team or Only you, Keep private and Ask <name>.
// Teammates' records and threads are theirs, shown as text, never acted on. Nothing here goes outside the Fleet.
let graphTeam=sideStore.get('graph-team')==='team',graphSharing=[],graphTeammates=[];
const teamOn=()=>graphSharing.some(s=>s.confirmed);
// Before an admin's OK: whose OK (s.admins); the Graph and Fleet look again every 5 s
const teamWaits=l=>(l||[]).filter(s=>!s.confirmed&&!s.paused);let graphFleetStamp=null;
const teamWaitLine=s=>{const n=s.admins||[];return n.length?t('Waiting for {} to share the team\'s data with you.',n.length>1?t('{} or {}',n.slice(0,-1).join(', '),n.at(-1)):n[0]):t('Waiting for an admin to share the team\'s data with you.')};
const graphWaiting=()=>teamWaits(graphSharing).length+teamWaits(fleetData?.shared?.graph).length>0;
setInterval(()=>{if(graphWaiting()&&!document.hidden&&(!$('#people').hidden||!$('#fleet').hidden))refreshWhenReady()},5e3);
// A fact's sort and end day, quietly under it: "Temporary · Until Nov 14". A plain fact without an end shows nothing.
// Its source: a connected AI, the owner's notes file, or the owner's own words it was found in (quote, cut short).
const FACT_SORT={event:'Temporary',commitment:'Commitment',preference:'Preference'};
const factQuote=q=>'“'+(q.length>60?(q.slice(0,60).replace(/\s+\S*$/,'')||q.slice(0,59))+'…':q)+'”';
const factUntil=d=>localeDate(new Date(d+'T12:00:00'),DL,{day:'numeric',month:'short',...(d.slice(0,4)!==String(new Date().getFullYear())?{year:'numeric'}:{})});
function factMeta(f){const bits=[FACT_SORT[f.fact_kind]?t(FACT_SORT[f.fact_kind]):'',f.valid_until?t('Until {}',factUntil(f.valid_until)):'',String(f.source||'').startsWith('ai:')?t('AI: {}',f.source.slice(3)):String(f.source||'').startsWith('notes:')?t('From {}',f.source.slice(6)):f.quote?t('From {}',factQuote(f.quote)):''].filter(Boolean);return bits.length?html`<small class="fact-meta">${bits.join(' · ')}</small>`:''}
// A promise's own page (#promise/<id>), laid out like a person's: who promised what to whom and by when, where it
// stands, the message it came from, who and what it is about, its card as a link, and what happened since.
const promiseHref=p=>'#promise/'+encodeURIComponent(p.id);
// Promise links, and card links on Graph pages, stay in the page, also when the page's base is another path.
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#promise/"],#people-view a[href^="#card="]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey||e.defaultPrevented)return;e.preventDefault();const href=a.getAttribute('href');if(location.hash===href)graphRoute();else location.hash=href});
// Graph links: #graph/<node id> opens a person, project or organization; the browser's back goes to where you were.
const GRAPH_KIND_PANE={person:['people','People'],project:['projects','Projects'],org:['orgs','Organizations']};
const graphHash=id=>'#graph/'+encodeURIComponent(id);
// A fact that lives on a record's page (a to-do chat's Saved line): that page, with the fact's editor open on Edit
let knownEdit=null;
function recordFactShow(node,edit){if(chatId){history.pushState(null,'',location.pathname+location.search);openChatLink()}knownEdit=edit;location.hash=graphHash(node)}
// A link out of a record's page (a to-do in its Open between you: #card=, #chat=) opens To-dos itself: the Graph stays on
// that page, so Back finds it there, and nothing redrawn in the Graph meanwhile moves the view the link opened.
function graphRoute(){const pm=/^#promise\/(\d+)$/.exec(location.hash),m=/^#graph\/(.+)$/.exec(location.hash);let id=pm?'promise:'+pm[1]:'';try{id=id||(m?decodeURIComponent(m[1]):'')}catch{}
 if(id){if($('#people').hidden){graphNode=id;document.querySelector('nav [data-tab="people"]')?.click()}else if(graphNode!==id)lazyRun('graph',()=>people(id));return}
 if(!$('#people').hidden&&graphNode&&!/^#(card|chat)=/.test(location.hash))lazyRun('graph',()=>people(''))}
// Back or Forward onto an entry the app pushed (Settings, a card's chat) fires popstate but no hashchange, so a tab link
// like #graph=people is opened here too, not only at the next refresh.
// A hash link fires popstate and then hashchange, which opens it; so wait a tick and open it only when none came.
let hashSeen=0;addEventListener('hashchange',()=>{hashSeen++},true);
addEventListener('popstate',()=>{if(drawerStep)return;graphRoute();const seen=hashSeen;setTimeout(()=>{if(hashSeen===seen)openTabLink()})});addEventListener('hashchange',graphRoute);setTimeout(graphRoute);
document.addEventListener('click',e=>{for(const m of document.querySelectorAll('.fact-menu[open]'))if(!m.contains(e.target))m.open=false});
$('nav').addEventListener('click',e=>{const t=e.target.closest('button');if(t?.dataset.tab&&t.dataset.tab!=='people'&&/^#graph[/=]/.test(location.hash))history.replaceState(null,'',location.pathname+location.search);graphSubSync()});
// The status poll (refresh(true)) redraws the Graph tab at most once a minute (GRAPH_POLL_MS): each redraw reads the whole
// Graph again on the Machine, and doing that on every poll kept it busy, so a Merge or a save waited behind it. The
// owner's own changes redraw it at once (people() or refresh() after each), and opening a record or list always loads it.
const GRAPH_POLL_MS=60000;let graphLoadedAt=0;
let graphSkip=false,graphAt=0,graphScroll=null,graphShown='',graphNode='',graphDrawn='',graphRequest=0,graphPane=localStorage.getItem('graph-pane')||'';
// Sub-tabs, as in Fleet: a pill row over panes that are all drawn at once and shown one at a time. A badge only
// counts what needs the owner (a source with a problem, friend requests), never a total.
const subTabs=(label,attr,panes,current)=>html`<div class="sub-tabs" role="tablist" aria-label="${label}">${panes.map(p=>html`<button type="button" role="tab" ${attr}="${p.id}" aria-selected="${p.id===current}"><span class="ell">${p.label}</span>${p.badge?html` <span class="badge${p.warn?html` warn`:''}">${p.badge}</span>`:''}</button>`)}</div>`;
function tabsFade(row){const max=row.scrollWidth-row.clientWidth;row.classList.toggle('more-left',row.scrollLeft>2);row.classList.toggle('more-right',row.scrollLeft<max-2)}
function tabsShow(row){if(!row)return;const t=row.querySelector('[aria-selected="true"]');if(t&&row.scrollWidth>row.clientWidth)row.scrollLeft=Math.max(0,t.offsetLeft-row.offsetLeft-(row.clientWidth-t.offsetWidth)/2);tabsFade(row)}
const allTabsFade=()=>document.querySelectorAll('.fleet-tabs,.sub-tabs').forEach(tabsFade);
document.addEventListener('scroll',e=>{if(e.target.matches?.('.fleet-tabs,.sub-tabs'))tabsFade(e.target)},{capture:true,passive:true});addEventListener('resize',allTabsFade);
new MutationObserver(()=>document.querySelectorAll('.fleet-tabs:not([data-faded]),.sub-tabs:not([data-faded])').forEach(r=>{r.dataset.faded='';tabsShow(r)})).observe(document.querySelector('main'),{childList:true,subtree:true});
// people() lives in the Graph's own part: callers outside it that await the redraw go through here.
const graphPeople=(...a)=>lazyIn('graph')?people(...a):lazyPart('graph').then(()=>people(...a));
// Graph: People (closest, gone quiet, new), Projects and Organizations.
const GRAPH_PANES=['people','projects','orgs'];
const graphPost=(action,args)=>(fuKept=null,request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})}).then(r=>(pagerDrop('gsearch'),r)));  // an edit: the board's follow-ups are asked again, and a search asks the Machine again (a merged pair showed twice there)
