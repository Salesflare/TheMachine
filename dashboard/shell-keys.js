// Command palette and keyboard shortcuts. One registry for both: a page or feature adds its actions with actionAdd()
// ({id, group, label, keywords, keys, run, when}, or each(ctx) for one action per item), and the palette (Ctrl/⌘K, or /)
// and the single-key shortcuts read it, so a new feature gets both. `when` reads the same thing the page shows (a hidden
// tab, a button a card doesn't have), so the palette only lists what the page itself offers. Hard rule: nothing that
// sends, approves or posts outside the Machine runs from here. Such an action is `review:true`: it only opens the review
// (the Send dialog, the brief sheet), where the content is read and confirmed there, and it never gets a key.
const KB_MAC=SIDE_MAC,KB_PAL=KB_MAC?'⌘K':'Ctrl K',ACTIONS=[];
function actionAdd(...list){for(const a of list){const i=ACTIONS.findIndex(x=>x.id===a.id);if(i>=0)ACTIONS[i]=a;else ACTIONS.push(a)}}
const kbPart=k=>k==='mod'?(KB_MAC?'⌘':'Ctrl'):k==='enter'?'Enter':k==='esc'?'Esc':k.length===1?k.toUpperCase():k;
const kbKeys=keys=>keys?keys.split(' ').map((k,i,all)=>(k.startsWith('mod+')?`<kbd>${KB_MAC?'⌘':'Ctrl'}</kbd><kbd>${esc(kbPart(k.slice(4)))}</kbd>`:`<kbd>${esc(kbPart(k))}</kbd>`)+(i<all.length-1&&all[0]==='g'?'<span class="then">then</span>':'')).join(''):'';
const kbText=keys=>keys?keys.split(' ').map(k=>k.startsWith('mod+')?(KB_MAC?'⌘':'Ctrl+')+kbPart(k.slice(4)):kbPart(k)).join(keys.startsWith('g ')?' then ':' '):'';
const kbAria=keys=>keys?keys.split(' ').map(k=>k.startsWith('mod+')?(KB_MAC?'Meta+':'Control+')+k.slice(4).toUpperCase():k===','?'Comma':k.length===1?k.toUpperCase():k).join(' '):'';
const kbHas=el=>!!el&&!el.hidden;
// What the shortcuts act on: the open chat's card, else the card picked with J/K (or holding focus) in the list.
let kbSel=null;
// A redraw replaces the card: the pick follows it by id.
function kbLive(){if(!kbSel||kbSel.isConnected||!kbSel.id)return;const el=document.getElementById(kbSel.id);if(!el){kbSel=null;return}const had=document.activeElement===document.body;kbSel=el;el.classList.add('kb-on');if(!el.hasAttribute('tabindex'))el.tabIndex=-1;if(had)el.focus({preventScroll:true})}
function kbCtx(){kbLive();const open=chatId&&!$('#inbox').hidden?cardOf(chatId):null;let card=open;
 if(!card){const el=document.activeElement?.closest?.('#suggestions article.card')||(kbSel?.isConnected?kbSel:null);const id=el?.id?.startsWith('task-')?el.id.slice(5):'';card=id?cardOf(id)||null:null}
 return {card,id:card?.id||'',chat:!!open}}
const kbBtn=(c,sel)=>c.id?document.querySelector(`#suggestions [data-id="${CSS.escape(c.id)}"]${sel}`):null;
function actsFor(ctx,keyed){const out=[];for(const a of ACTIONS){if(a.alias&&!keyed)continue;try{if(a.each){for(const x of a.each(ctx)||[])out.push({group:a.group,...x})}else if(!a.when||a.when(ctx))out.push(a)}catch{}}return out}
const actLabel=(a,ctx)=>typeof a.label==='function'?a.label(ctx):a.label;
function actRun(a,ctx){if(typeof drawerClose==='function')drawerClose();try{const r=a.run(ctx);if(r?.catch)r.catch(e=>toast(e.message,true))}catch(e){errCaught(e);toast(e.message||'That didn’t work',true)}}
// Go to
const kbNav=sel=>()=>{const el=$(sel);if(!el)return;if(chatId&&el.dataset.tab==='inbox'&&!$('#inbox').hidden){history.replaceState(null,'',location.pathname+location.search);chatPushed=false;openChatLink();scrollTo(0,0);return}el.click()};
// The Calendar's own keys, while it is on show: t Today, k j the period before or after (← → too), a Agenda, w Week, m Month
{const onCal=()=>!$('#calendar').hidden;actionAdd(
 {id:'cal-today',group:'Calendar',label:'Today',keywords:'calendar now this week',keys:'t',when:onCal,run:()=>calGo(0)},
 {id:'cal-prev',group:'Calendar',label:'Previous',keywords:'calendar earlier back',keys:'k',when:onCal,run:()=>calGo(-1)},
 {id:'cal-next',group:'Calendar',label:'Next',keywords:'calendar later on',keys:'j',when:onCal,run:()=>calGo(1)},
 {id:'cal-agenda',group:'Calendar',label:'Agenda',keywords:'calendar list',keys:'a',when:onCal,run:()=>calSetMode('agenda')},
 {id:'cal-week',group:'Calendar',label:'Week',keywords:'calendar grid',keys:'w',when:onCal,run:()=>calSetMode('week')},
 {id:'cal-month',group:'Calendar',label:'Month',keywords:'calendar grid',keys:'m',when:onCal,run:()=>calSetMode('month')})}
actionAdd(
 {id:'go-todos',group:'Go to',label:'To-dos',keywords:'todos suggestions cards home inbox',keys:'g t',run:kbNav('nav [data-tab="inbox"]')},
 {id:'go-suggestions',group:'Go to',alias:true,keys:'g s',run:kbNav('nav [data-tab="inbox"]')},  // the old key, still working, not listed
 {id:'go-calendar',group:'Go to',label:'Calendar',keywords:'meetings today agenda',keys:'g c',run:kbNav('nav [data-tab="calendar"]')},
 {id:'go-events',group:'Go to',label:'Messages',keywords:'events signals search mail emails everything read',keys:'g e',run:()=>msgSearch('')},
 {id:'go-people',group:'Go to',label:'People',keywords:'graph contacts',keys:'g p',run:kbNav('.side-sub a[data-graph-sub="people"]')},
 {id:'go-orgs',group:'Go to',label:'Organizations',keywords:'graph companies organizations',keys:'g o',run:kbNav('.side-sub a[data-graph-sub="orgs"]')},
 {id:'go-projects',group:'Go to',label:'Projects',keywords:'graph',keys:'g j',run:kbNav('.side-sub a[data-graph-sub="projects"]')},
 {id:'go-roles',group:'Go to',label:'Who’s who',keywords:'graph roles',keys:'g w',when:()=>kbHas($('.side-sub a[data-graph-sub="roles"]')),run:kbNav('.side-sub a[data-graph-sub="roles"]')},
 {id:'go-fleet',group:'Go to',label:'Fleet',keywords:'team teammates',keys:'g f',when:()=>kbHas($('#tab-fleet')),run:kbNav('#tab-fleet')},
 {id:'go-learning',group:'Go to',label:'Learning',keywords:'feedback quality learned decided changes how it is going',keys:'g l',run:kbNav('nav [data-tab="feedback"]')},
 {id:'go-feedback',group:'Go to',alias:true,keys:'g b',run:kbNav('nav [data-tab="feedback"]')},  // the old key, still working, not listed
 {id:'go-connections',group:'Go to',label:'Connections',keywords:'sources health accounts',keys:'g n',run:kbNav('nav [data-tab="health"]')},
 {id:'go-settings',group:'Go to',label:'Settings',keywords:'preferences',keys:'g ,',run:()=>showSettings()},
 {id:'go-settings-tabs',group:'Go to',each:()=>SETTINGS_TABS.filter(([t])=>{const b=document.querySelector(`[data-settings-tab="${t}"]`);return b&&!b.hidden}).map(([t,l])=>({id:'go-settings-'+t,label:window.t('Settings: {}',window.t(l)),keywords:'settings '+t,run:()=>showSettings(t)}))},
 // Projects as a board or a list, once there is a board; a new board from its editor (the page shows it only to the owner)
 {id:'go-projects-view',group:'Go to',each:()=>graphBoards.length?[['board','Board'],['list','List']].map(([v,t])=>({id:'go-projects-'+v,label:window.t(v==='board'?'Projects: board view':'Projects: list view'),keywords:'projects board list kanban stages',run:()=>{const go=()=>projectsViewSet(v);if(!$('#people').hidden&&graphShown==='projects'&&!graphNode)go();else{sideStore.set('projects-view',v);kbNav('.side-sub a[data-graph-sub="projects"]')()}}})):[]},
 {id:'board-new',group:'Actions',label:'New board',keywords:'projects board stages kanban',when:()=>!$('#people').hidden&&graphShown==='projects'&&!!document.querySelector('#people-view [data-board-new]'),run:()=>edOpen()},
 {id:'event-new',group:'Actions',label:'New event',keywords:'event meeting calendar appointment add create invite',run:()=>calNew()},
 {id:'project-new',group:'Actions',label:'New project',keywords:'project deal opportunity add create crm',run:()=>pjOpen()},
 {id:'person-new',group:'Actions',label:'New person',keywords:'person contact add create crm people',run:()=>recOpen('person')},
 {id:'org-new',group:'Actions',label:'New organization',keywords:'organisation organization company account add create crm',run:()=>recOpen('org')},
 {id:'project-edit',group:'Actions',label:'Edit this project',keywords:'project rename value notes people stage',when:()=>!$('#people').hidden&&/^project:/.test(graphNode||''),run:()=>pjOpen({node:graphNode})},
 {id:'project-won',group:'Actions',label:'Mark this project won',keywords:'project won close deal',when:()=>!$('#people').hidden&&/^project:/.test(graphNode||''),run:()=>pjOpen({node:graphNode,mode:'won'})},
 {id:'project-lost',group:'Actions',label:'Mark this project lost',keywords:'project lost close deal',when:()=>!$('#people').hidden&&/^project:/.test(graphNode||''),run:()=>pjOpen({node:graphNode,mode:'lost'})},
 {id:'board-edit',group:'Actions',label:'Edit this board',keywords:'board stages rename',when:()=>!$('#people').hidden&&graphShown==='projects'&&!!document.querySelector('#people-view [data-board-edit]'),run:()=>document.querySelector('#people-view [data-board-edit]').click()},
 {id:'go-boards',group:'Go to',each:()=>(graphMineBoards||graphBoards).filter(b=>!b.team).map(b=>({id:'go-board-'+b.id,label:t('Board: {}',b.name),keywords:'projects board kanban '+b.name,run:()=>{boardShown=b.name;sideStore.set('board-shown',b.name);sideStore.set('projects-view','board');if(!$('#people').hidden&&graphShown==='projects'&&!graphNode){projectsViewSet('board');boardRedraw()}else kbNav('.side-sub a[data-graph-sub="projects"]')()}}))},
 {id:'go-connections-reviews',group:'Go to',label:'Connections: Reviews',keywords:'signal reviews runs delivery',run:()=>showTab('health','reviews')});
// Actions
actionAdd(
 {id:'new-card',group:'Actions',label:'New to-do',keywords:'add task todo card create',keys:'n',run:()=>ncOpen()},
 {id:'talk',group:'Actions',label:'Talk',keywords:'talk live voice speak conversation',keys:'t',when:()=>talkOk()||!!talk?.main,run:()=>talkMain()},  // on the Calendar, T stays Today (it comes first)
 {id:'add-connection',group:'Actions',label:'Add a connection',keywords:'connect source account gmail slack',run:()=>{showTab('health','add');$('#connect-add')?.scrollIntoView({block:'start'})}},
 {id:'open-browser',group:'Actions',label:'Open the browser',keywords:'browser /browser chrome',when:()=>kbHas($('#open-browser'))&&!!$('#open-browser').getAttribute('href'),run:()=>$('#open-browser').click()},
 {id:'theme',group:'Actions',label:()=>document.documentElement.dataset.theme==='light'?'Switch to dark mode':'Switch to light mode',keywords:'theme light dark mode appearance',run:()=>$('#theme-toggle').click()},
 {id:'sidebar',group:'Actions',label:()=>document.documentElement.dataset.side==='collapsed'?'Expand the sidebar':'Collapse the sidebar',keywords:'sidebar fold icons',keys:'mod+b',bound:true,when:()=>DESK.matches,run:()=>sideSet(document.documentElement.dataset.side!=='collapsed')},
 {id:'refresh',group:'Actions',label:'Refresh',keywords:'reload update',run:()=>refresh()},
 {id:'shortcuts',group:'Actions',label:'Keyboard shortcuts',keywords:'keys help hotkeys',keys:'?',run:()=>keysOpen()});
// This device (Settings, General): install the app, turn on notifications, a test notification to this device only.
const DEVICE_WORDS={'install-app':'install app pwa taskbar dock home screen pin','push-on':'notifications push bell alerts enable','push-test':'test notification push ping'};
actionAdd(...DEVICE_ACTIONS.map(a=>({id:a.id,group:'Actions',label:a.label,keywords:DEVICE_WORDS[a.id],when:()=>a.available(),run:a.run})));
// This card: only what the card itself offers (its own button is there), on the open chat's card or the picked one.
const SEND_KINDS=['email','email_demo','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply','merge','finish','calendar','doc_write'];
const SEND_WORD={email:'the email',email_demo:'the email',linkedin:'the LinkedIn message',slack:'the Slack message',x:'the post',whatsapp:'the WhatsApp message',telegram:'the Telegram message',intercom:'the Intercom reply',merge:'the fix',finish:'the last step',calendar:'the calendar change'};
const kbChatInput=id=>{if(chatId!==id)chatGo(id);let n=0;const go=()=>{const i=$('#chat-input');if(i){i.focus();return}if(++n<40)setTimeout(go,50)};go()};
actionAdd(
 {id:'card-open',group:'This to-do',label:'Open the chat',keywords:'to-do card chat open',when:c=>c.card&&!c.chat,run:c=>chatGo(c.id)},
 {id:'card-chat',group:'This to-do',label:'Write in the chat',keywords:'message reply ask composer',keys:'r',when:c=>!!c.card,run:c=>kbChatInput(c.id)},
 {id:'card-rename',group:'This to-do',label:'Rename',keywords:'edit title',keys:'e',when:c=>!!c.card,run:c=>renameAt(c.id,titleEl(c.id))},
 {id:'card-project',group:'This to-do',label:'Put on a project',keywords:'project board link change',when:c=>!!c.card,run:c=>cardProjectPick(c.id,document.getElementById('task-'+c.id)||document.body)},
 {id:'card-snooze',group:'This to-do',label:'Snooze',keywords:'later remind',keys:'s',when:c=>!!kbBtn(c,'[data-choice="snooze"]'),run:c=>openSnooze(c.id)},
 {id:'card-done',group:'This to-do',label:'Mark done',keywords:'complete finish',keys:'d',when:c=>!!kbBtn(c,'[data-choice="complete"]'),run:c=>kbBtn(c,'[data-choice="complete"]').click()},
 {id:'card-change',group:'This to-do',label:'Change…',keywords:'edit feedback',when:c=>!!kbBtn(c,'[data-choice="change"]'),run:c=>kbBtn(c,'[data-choice="change"]').click()},
 {id:'card-reject',group:'This to-do',label:'Not needed…',keywords:'dismiss reject',when:c=>!!kbBtn(c,'[data-choice="reject"]'),run:c=>kbBtn(c,'[data-choice="reject"]').click()},
 {id:'card-handoff',group:'This to-do',label:'Hand off…',keywords:'teammate fleet delegate',review:true,when:c=>!!c.id&&!!document.querySelector(`#suggestions [data-fleet-handoff="${CSS.escape(c.id)}"]`),run:c=>document.querySelector(`#suggestions [data-fleet-handoff="${CSS.escape(c.id)}"]`).click()},
 // Hand to Codex / Claude Code: opens the brief sheet to read and edit; only its own Send there hands it over.
 {id:'card-agent',group:'This to-do',review:true,each:c=>c.card&&canAgent(c.card)?agentTools().map(t=>({id:'card-agent-'+t.id,label:window.t('Hand to {}',t.name)+'…',keywords:'agent codex claude code',review:true,run:()=>agentHand(c.id,t.id)})):[]},
 {id:'card-agent-open',group:'This to-do',each:c=>{const j=c.card?.agent_job;return j?.url&&/^(https:\/\/|codex:\/\/threads\/)/.test(j.url)?[{id:'card-agent-open',label:agentApp(j),keywords:'codex claude open thread',run:()=>j.opens_later?toast(t(AGENT_LATER)):window.open(agentHref(j),'_blank','noopener,noreferrer')}]:[]}},
 // Sends: only the Send dialog with the draft to read, its recipients and its own Send now.
 {id:'card-review-send',group:'This to-do',review:true,each:c=>c.card?.status==='prepared'?taskActions(c.card).filter(a=>SEND_KINDS.includes(a.kind)&&!a.state?.status).map(a=>({id:'card-review-'+a.kind,label:t('Review {}',t(SEND_WORD[a.kind]||'the draft'))+'…',keywords:'send draft review',review:true,run:()=>openSend(c.id,a.revision)})):[]});

// Fuzzy match: the whole query in the label (at the start best, then at a word), else every word in order as letters.
function palScore(q,text){q=q.trim().toLowerCase();const t=String(text||'').toLowerCase();if(!q)return 1;if(!t)return -1;
 const at=t.indexOf(q);if(at===0)return 100-t.length/1000;if(at>0)return(/[\s\-:·/(]/.test(t[at-1])?85:70)-at/1000;
 let total=0;for(const w of q.split(/\s+/)){const i=t.indexOf(w);if(i>=0){total+=i===0||/[\s\-:·/(]/.test(t[i-1])?50:40;continue}
  let j=0,prev=-2,s=0;for(const ch of w){const k=t.indexOf(ch,j);if(k<0)return -1;s+=k===prev+1?3:k===0||/[\s\-:·/(]/.test(t[k-1])?2:.5;prev=k;j=k+1}total+=Math.min(35,s/(w.length*3)*35)}
 return total/q.split(/\s+/).length}
// Keywords count for whole words only ("mode" finds the theme); letters in order only on the label itself.
const palMatch=(q,a,label)=>{const l=palScore(q,label),w=q.trim().toLowerCase(),k=a.keywords&&w.split(/\s+/).every(x=>a.keywords.toLowerCase().includes(x))?palScore(q,a.keywords)*.6:-1;return Math.max(l,k)};
// Recent commands, newest first (this browser only).
const PAL_RECENT='palette-recent';
const palRecent=()=>{try{const v=JSON.parse(localStorage.getItem(PAL_RECENT)||'[]');return Array.isArray(v)?v.filter(x=>typeof x==='string').slice(0,5):[]}catch{return []}};
function palRemember(id){try{localStorage.setItem(PAL_RECENT,JSON.stringify([id,...palRecent().filter(x=>x!==id)].slice(0,5)))}catch{}}

const pal={from:null,ctx:null,items:[],sel:0,q:'',seq:0,timer:0,found:null,msgs:null};
function palDialog(){let d=$('#palette');if(d)return d;d=document.createElement('dialog');d.id='palette';d.setAttribute('aria-label','Search and commands');
 d.innerHTML=`<div class="pal-field"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4 4"/></svg><input id="pal-q" type="text" role="combobox" aria-expanded="true" aria-controls="pal-list" aria-autocomplete="list" placeholder="Search or type a command" autocomplete="off" spellcheck="false" enterkeyhint="go"></div><div class="pal-list" id="pal-list" role="listbox" aria-label="Results"></div><div class="pal-foot"><span><kbd>↑</kbd><kbd>↓</kbd> move</span><span><kbd>Enter</kbd> run</span><span><kbd>Esc</kbd> close</span><span><kbd>?</kbd> shortcuts</span></div>`;
 document.body.append(d);const q=d.querySelector('#pal-q');
 q.addEventListener('input',()=>{pal.q=q.value;pal.sel=0;palRender();palFind()});
 q.addEventListener('keydown',e=>{if(e.isComposing||e.keyCode===229)return;
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const n=pal.items.length;if(n){pal.sel=(pal.sel+(e.key==='ArrowDown'?1:-1)+n)%n;palPaint()}return}
  if(e.key==='Enter'){e.preventDefault();palPick(pal.sel);return}
  if(e.key==='Tab'){e.preventDefault();return}  // focus stays in the field while it is open
  if(e.key==='Escape'){e.preventDefault();palClose()}});
 d.addEventListener('cancel',e=>{e.preventDefault();palClose()});
 d.addEventListener('click',e=>{if(e.target===d){palClose();return}const o=e.target.closest('[data-pal]');if(o)palPick(+o.dataset.pal)});
 d.addEventListener('mousemove',e=>{const o=e.target.closest('[data-pal]');if(o&&+o.dataset.pal!==pal.sel){pal.sel=+o.dataset.pal;palPaint(false)}});
 return d}
function palOpen(o){const d=palDialog();if(d.open)return;for(const x of document.querySelectorAll('dialog[open]'))if(x!==d)return;
 pal.todos=!!o?.todos;pal.from=document.activeElement;pal.ctx=kbCtx();pal.q='';pal.sel=0;pal.found=null;pal.msgs=null;pal.done=[];pal.seq++;if(typeof drawerClose==='function')drawerClose();
 const q=d.querySelector('#pal-q');q.value='';d.showModal();q.focus();palRender()}
function palClose(){const d=$('#palette');clearTimeout(pal.timer);pal.seq++;if(d?.open)d.close();if(d?.contains(document.activeElement))document.activeElement.blur();  /* never left in the closed field, or keys would think you type */
 const f=pal.from;pal.from=null;if(f?.isConnected&&f!==document.body)f.focus({preventScroll:true})}
const palToggle=()=>$('#palette')?.open?palClose():palOpen();
function palRows(){const q=pal.q.trim(),ctx=pal.ctx,recent=palRecent(),groups=[],seen=new Set();
 const acts=actsFor(ctx).map(a=>({a,label:actLabel(a,ctx)}));
 if(!q){const rec=recent.map(id=>acts.find(x=>x.a.id===id)).filter(Boolean);rec.forEach(x=>seen.add(x.a.id));if(rec.length)groups.push(['Recent',rec]);
  for(const g of ['This to-do','Actions','Go to']){const xs=acts.filter(x=>x.a.group===g&&!seen.has(x.a.id));if(xs.length)groups.push([g,xs])}}
 else{const scored=acts.map(x=>({...x,s:palMatch(q,x.a,x.label)+(recent.includes(x.a.id)?8-recent.indexOf(x.a.id):0)})).filter(x=>x.s>8).sort((x,y)=>y.s-x.s||!!y.a.keys-!!x.a.keys);  /* a tie goes to the one with its own key: the everyday action (New to-do before New event) */
  for(const g of ['This to-do','Actions','Go to']){const xs=scored.filter(x=>x.a.group===g).slice(0,8);if(xs.length)groups.push([g,xs])}
  if(groups.length>1){const best=g=>g[1][0].s;groups.sort((x,y)=>best(y)-best(x))}
  const cards=(state.suggestions||[]).filter(s=>!closed(s)).map(s=>({s,score:palScore(q,s.title)})).filter(x=>x.score>=40)  /* words, not scattered letters */.sort((x,y)=>y.score-x.score).slice(0,5);
  if(cards.length)groups.push(['To-dos',cards.map(({s})=>({a:{id:'card:'+s.id,run:()=>chatGo(s.id),entity:true},label:s.title,sub:s.scope==='work'?'Work':s.scope==='personal'?'Personal':''}))]);
  // Done cards in their own group under the open ones: the loaded ones and what the Machine found among all of them
  {const seen=new Set(),done=[...(state.suggestions||[]).filter(closed),...pal.done||[]].filter(s=>!seen.has(s.id)&&seen.add(s.id)).map(s=>({s,score:palScore(q,s.title)})).filter(x=>x.score>=40).sort((x,y)=>y.score-x.score).slice(0,5);
   if(done.length)groups.push(['Done',done.map(({s})=>({a:{id:'card:'+s.id,run:()=>{doneExtra.set(s.id,s);cardsMerge();chatGo(s.id)},entity:true},label:s.title,sub:s.scope==='work'?'Work':s.scope==='personal'?'Personal':''}))])}
  for(const [kind,name] of [['person','People'],['org','Organizations'],['project','Projects']]){const xs=(pal.found||[]).filter(n=>n.kind===kind).slice(0,5);
   if(xs.length)groups.push([name,xs.map(n=>({a:{id:'graph:'+n.id,run:()=>{location.hash=graphHash(n.id)},entity:true},label:n.name||n.id,sub:kind==='person'?(n.ids||[])[0]||'':kind==='org'&&n.domain!==n.name?n.domain||'':''}))])}
  // Messages: the top few of everything the Machine read (the results page's own search), then See all results
  if(q.length>=2)groups.push(['Messages',[...(pal.msgs||[]).map(m=>({a:{id:'msg:'+m.id,run:()=>msgOpen(m),entity:true},label:m.title||t('Message'),sub:msgSub(m)})),
   {a:{id:'msg-all',run:()=>msgSearch(q),entity:true},label:t('See all results for “{}”',q),sub:pal.msgs===null?t('Looking…'):''}]])}
 // From the sidebar's Search box: the to-dos first (before typing, the first open ones)
 if(pal.todos){if(!q){const open=(state.suggestions||[]).filter(s=>!closed(s)).slice(0,5);if(open.length)groups.unshift(['To-dos',open.map(s=>({a:{id:'card:'+s.id,run:()=>chatGo(s.id),entity:true},label:s.title,sub:s.scope==='work'?'Work':s.scope==='personal'?'Personal':''}))])}
  else groups.sort((x,y)=>['To-dos','Done'].includes(y[0])-['To-dos','Done'].includes(x[0]))}
 return groups}
function palRender(){const d=$('#palette');if(!d?.open)return;const groups=palRows(),list=d.querySelector('#pal-list');pal.items=[];let html='';
 for(const [g,xs] of groups){html+=`<div class="pal-group" role="presentation">${esc(g)}</div>`;
  for(const x of xs){const i=pal.items.push(x)-1;const keys=x.a.review?'':x.a.keys;
   html+=`<div class="pal-item" role="option" id="pal-o-${i}" data-pal="${i}" aria-selected="false"><span class="pal-label">${esc(x.label)}</span>${x.sub?`<small>${esc(x.sub)}</small>`:''}${keys?`<span class="pal-keys" aria-label="${esc(kbText(keys))}">${kbKeys(keys)}</span>`:''}</div>`}}
 if(!pal.items.length)html=`<p class="pal-empty">${pal.q.trim().length>=2&&pal.found===null?'Looking…':'Nothing matches.'}</p>`;
 list.innerHTML=html;pal.sel=Math.min(pal.sel,Math.max(0,pal.items.length-1));palPaint()}
function palPaint(scroll=true){const d=$('#palette');if(!d)return;const q=d.querySelector('#pal-q');
 for(const o of d.querySelectorAll('[data-pal]'))o.setAttribute('aria-selected',String(+o.dataset.pal===pal.sel));
 const on=d.querySelector(`#pal-o-${pal.sel}`);if(on){q.setAttribute('aria-activedescendant',on.id);if(scroll)on.scrollIntoView({block:'nearest'})}else q.removeAttribute('aria-activedescendant')}
// People, organizations and projects come from the Graph's own search (api/graph?q=), a moment after typing stops;
// an answer to an older query is dropped.
// Messages come from the results page's search (api/events: by meaning and words, every account) on their own, as
// it can take longer: the rest shows first.
function palFind(){clearTimeout(pal.timer);const q=pal.q.trim(),seq=++pal.seq;if(q.length<2){pal.found=[];pal.msgs=[];return}pal.found=null;pal.msgs=null;
 pal.timer=setTimeout(async()=>{let found=[],done=[];const e=encodeURIComponent(q);
  request('api/events?account=all&q='+e).then(r=>Array.isArray(r)?r:[]).catch(()=>[]).then(rows=>{if(seq!==pal.seq||!$('#palette')?.open)return;pal.msgs=rows.slice(0,4);palRender()});
  await Promise.all([request('api/graph?q='+e).then(r=>{found=Array.isArray(r?.found)?r.found:[]}).catch(()=>{}),
   request('api/cards/done?limit=8&q='+e).then(r=>{done=Array.isArray(r?.cards)?r.cards:[]}).catch(()=>{})]);  /* done cards beyond the loaded ones */
  if(seq!==pal.seq||!$('#palette')?.open)return;pal.found=found;pal.done=done;palRender()},180)}
function palPick(i){const x=pal.items[i];if(!x)return;const ctx=pal.ctx;palClose();if(!x.a.entity)palRemember(x.a.id);actRun(x.a,ctx)}

// The shortcut sheet (?), from the same registry.
function keysOpen(){let d=$('#keys-sheet');for(const x of document.querySelectorAll('dialog[open]'))if(x!==d)return;
 if(!d){d=document.createElement('dialog');d.id='keys-sheet';d.setAttribute('aria-labelledby','keys-title');document.body.append(d);d.addEventListener('click',e=>{if(e.target===d)d.close()})}
 const row=(keys,label,more='')=>`<p><span>${esc(label)}</span><span class="keys">${kbKeys(keys)}${more}</span></p>`,ctx={card:null,id:'',chat:false};
 const of=g=>ACTIONS.filter(a=>a.group===g&&a.keys&&!a.review&&!a.each&&!a.alias&&(!a.when||(()=>{try{return a.when(ctx)}catch{return false}})()||g==='This to-do'||g==='Calendar')).map(a=>row(a.keys,a.id==='talk'?'Talk (not on the Calendar)':actLabel(a,ctx))).join('');  // on the Calendar, T is Today
 d.innerHTML=`<form method="dialog"><div class="snooze-heading"><h2 id="keys-title">Keyboard shortcuts</h2><button aria-label="Close">×</button></div></form><div class="keys-sheet">
 <div><h3>General</h3>${row('mod+k','Search and commands','<span class="then">or</span><kbd>/</kbd>')}${of('Actions')}${row('esc','Close a chat or dialog')}</div>
 <div><h3>Go to</h3>${of('Go to')}</div>
 <div><h3>Calendar</h3>${of('Calendar')}${row('←','Previous')}${row('→','Next')}</div>
 <div><h3>Lists and to-dos</h3>${row('j','Next','<span class="then">or</span><kbd>↓</kbd>')}${row('k','Previous','<span class="then">or</span><kbd>↑</kbd>')}${row('enter','Open')}${row('→','Open a folded list')}${row('←','Fold it again')}${of('This to-do')}</div></div>`;
 d.showModal()}

// J/K (or ↓ ↑): the next or previous item in the page's list (cards, events, the Graph's rows); in a chat, the next
// card. On Suggestions the heads of the folded lists are stops too, so a page with every list folded still has
// something to land on: → or Enter opens one, ← folds it again.
const KB_LISTS={inbox:'#suggestions article.card,#suggestions .section-head[data-fold],#suggestions details[id]>summary,#promises-list[open] .promise',events:'#results article',people:'#people-view article,#people-view .person-item',fleet:'#fleet-view article'};
function kbItems(){const sec=[...document.querySelectorAll('main>section')].find(s=>!s.hidden);if(!sec||!KB_LISTS[sec.id])return [];
 // shown: laid out, and not inside a folded list (Chrome still lays out a closed <details>' content, hidden)
 return [...sec.querySelectorAll(KB_LISTS[sec.id])].filter(x=>x.getClientRects().length&&!x.parentElement.closest('article,.person-item')&&!(x.matches('summary')?x.parentElement.parentElement:x).closest('details:not([open])'))}
function kbPick(el,scroll=true){document.querySelector('.kb-on')?.classList.remove('kb-on');kbSel=el||null;if(!el)return;el.classList.add('kb-on');if(!el.hasAttribute('tabindex'))el.tabIndex=-1;el.focus({preventScroll:true});if(scroll)el.scrollIntoView({block:'nearest'})}
// Whether the keyboard is in use: the last thing pressed was a key (or nothing yet, on a fresh page), not a tap or click.
// Only then does a page put focus on its first item and show the ring, so a mouse never sees a ring it didn't ask for.
var kbInput='';addEventListener('keydown',e=>{if(!/^(Shift|Control|Alt|Meta)$/.test(e.key))kbInput='key'},true);addEventListener('pointerdown',()=>{kbInput='pointer'},true);
const kbKeyed=()=>kbInput!=='pointer';var kbLanded=false;
function kbFocus(el,scroll=true){if(!el)return;if(kbKeyed()){kbPick(el,scroll);return}if(!el.hasAttribute('tabindex'))el.tabIndex=-1;el.focus({preventScroll:true})}
// A page's first focus, from the keyboard: the first to-do (else a folded list's head) on Suggestions, the first row of
// a list page, else the page's open tab or first button. Never over a dialog, an open chat or something already focused.
// A retry for a list that is still loading belongs to its page: it stops once another page shows or a newer landing starts,
// so it never takes focus on a page it wasn't for.
var kbLandSeq=0;
function kbLand(n=0,seq=++kbLandSeq,from=null){const a=document.activeElement,sec=[...document.querySelectorAll('main>section')].find(s=>!s.hidden);
 if(n&&(seq!==kbLandSeq||sec!==from))return;
 if(!sec||!kbKeyed()||!matchMedia('(pointer:fine)').matches||document.querySelector('dialog[open]')||chatId&&sec.id==='inbox')return;
 if(a&&a!==document.body&&(!a.closest?.('nav,.app-side')||a.matches?.('input,textarea,select,[contenteditable="true"]')))return;  // never out of a field being typed in, the sidebar's search too
 const xs=kbItems(),first=xs.find(x=>x.matches('article'))||xs[0];if(first){kbPick(first,first.getBoundingClientRect().top>innerHeight-80);return}  // the page stays where it is when the item shows
 if(KB_LISTS[sec.id]&&n<10){setTimeout(()=>kbLand(n+1,seq,sec),200);return}  // the list is still loading
 const shown=x=>x.getClientRects().length&&!x.disabled;
 const t=[...sec.querySelectorAll('[role="tab"][aria-selected="true"]')].find(shown)||[...sec.querySelectorAll('button,a[href],summary,[tabindex="0"]')].find(shown);
 if(t){t.focus({preventScroll:true})}}
function kbMove(step){if(chatId&&!$('#inbox').hidden){const rows=[...document.querySelectorAll('#side-cards a[href^="#chat="]')],i=rows.findIndex(a=>a.getAttribute('href')==='#chat='+chatId),n=rows[i+step];
  if(n)chatGo(n.getAttribute('href').slice(6));return}
 const xs=kbItems();if(!xs.length)return;const a=document.activeElement;if(!kbSel?.isConnected&&xs.includes(a))kbSel=a;  // a redraw that put focus back
 const now=kbSel?.isConnected?xs.indexOf(kbSel):-1;
 const prev=now<0&&kbSel?.id?xs.findIndex(x=>x.id===kbSel.id):now;kbPick(xs[prev<0?(step>0?0:xs.length-1):Math.max(0,Math.min(xs.length-1,prev+step))])}
function kbEnter(){kbLive();const el=kbSel;if(!el?.isConnected||document.activeElement!==el||el.matches('summary'))return false;  // a summary opens itself
 if(el.id?.startsWith('task-')){chatGo(el.id.slice(5));return true}const t=el.querySelector('[data-graph-open],a[href],button');if(t){t.click();return true}el.click();return true}
document.addEventListener('focusin',e=>{const t=e.target;
 if(kbSel&&t!==kbSel&&!kbSel.contains(t)&&!t.closest?.('#palette,#keys-sheet')){kbSel.classList.remove('kb-on');kbSel=null}
 // focus that comes back to an item (a dialog closing, Tab) picks it, so J/K go on from there
 if(t!==kbSel&&t.closest?.('#suggestions')&&kbItems().includes(t)){kbSel=t;if(kbKeyed())t.classList.add('kb-on')}});
// → opens a folded list's head, ← folds it
function kbFold(el,open){if(!el)return false;if(el.matches('summary')){const d=el.parentElement;if(d.open===open)return false;d.open=open;return true}
 if(el.matches('.section-head[data-fold]')){if((el.getAttribute('aria-expanded')==='true')===open)return false;toggleSection(el.dataset.fold);return true}return false}
const kbInChat=()=>!!chatId&&!$('#inbox').hidden;
// Esc closes the open chat, as its Back does; the card it was about gets focus again
function kbChatClose(){const b=document.querySelector('#suggestions [data-chat-back]');if(!b)return false;b.click();return true}
$('#suggestions').addEventListener('keydown',e=>{if(e.key!=='Escape'||e.target.id!=='chat-input'||e.isComposing||e.defaultPrevented)return;e.preventDefault();
 if(e.target.value.trim()){e.target.blur();return}kbChatClose()});  // with words in the box the first Esc only leaves it

// The keys. Never while typing (a field, a text area, contenteditable), during IME composition, or over another dialog.
let kbG=0;
document.addEventListener('keydown',e=>{if(e.defaultPrevented||e.isComposing||e.keyCode===229)return;const key=e.key;
 const mod=KB_MAC?e.metaKey&&!e.ctrlKey:e.ctrlKey&&!e.metaKey;
 if(mod&&!e.altKey&&!e.shiftKey&&key.toLowerCase()==='k'){e.preventDefault();palToggle();return}
 if(e.ctrlKey||e.metaKey||e.altKey||ncTyping(e.target)||document.querySelector('dialog[open]'))return;
 if(kbG&&Date.now()-kbG<1500){kbG=0;const a=actsFor(kbCtx(),true).find(a=>a.keys==='g '+key.toLowerCase()&&!a.review);if(a){e.preventDefault();actRun(a,kbCtx())}return}kbG=0;
 if(key==='g'&&!e.shiftKey){kbG=Date.now();e.preventDefault();return}
 if(key==='/'){e.preventDefault();palOpen();return}
 if(key==='?'){e.preventDefault();keysOpen();return}
 if((key==='j'||key==='k')&&$('#calendar').hidden){e.preventDefault();kbMove(key==='j'?1:-1);return}
 // ↓ ↑ as J K, while the page or a list item has focus (a button in a card keeps its own arrows), not in a chat or the Calendar
 const onItem=()=>{const a=document.activeElement;return !a||a===document.body||a===kbSel||kbItems().includes(a)};
 if((key==='ArrowDown'||key==='ArrowUp')&&!e.shiftKey&&$('#calendar').hidden&&!kbInChat()&&onItem()){e.preventDefault();kbMove(key==='ArrowDown'?1:-1);return}
 if((key==='ArrowRight'||key==='ArrowLeft')&&!e.shiftKey&&kbFold(document.activeElement,key==='ArrowRight')){e.preventDefault();return}
 if(key==='Enter'){if(kbEnter())e.preventDefault();return}
 if(key==='Escape'&&kbInChat()&&!drawerIs()&&kbChatClose()){e.preventDefault();return}
 if(key==='Escape'&&kbSel){kbPick(null);return}
 if(e.shiftKey||key.length!==1)return;
 const ctx=kbCtx(),a=actsFor(ctx).find(a=>a.keys===key.toLowerCase()&&!a.review&&!a.bound);if(a){e.preventDefault();actRun(a,ctx)}});

// The sidebar's Search box has no filter of its own: a click, Enter or a typed letter opens the palette, the to-dos
// first, and the letter starts the search there
{const f=$('#side-find'),go=(text='')=>{palOpen({todos:true});if(text){const q=$('#pal-q');q.value=text;q.dispatchEvent(new Event('input'))}};
 f.addEventListener('click',()=>go());
 f.addEventListener('keydown',e=>{if(e.ctrlKey||e.metaKey||e.altKey||e.isComposing)return;if(e.key==='Enter'){e.preventDefault();e.stopImmediatePropagation();go()}else if(e.key.length===1&&e.key!==' '){e.preventDefault();e.stopImmediatePropagation();go(e.key)}},true)}
// Where the keys show: ⌘K / Ctrl K in Search (on a phone the top bar's search icon), and the quiet hints in tooltips and menus.
{const lab=$('#side-search'),b=document.createElement('button');b.type='button';b.className='kb-open';b.id='pal-open';b.title='Search and commands ('+KB_PAL+')';b.setAttribute('aria-label','Search and commands');b.setAttribute('aria-keyshortcuts',kbAria('mod+k'));
 b.innerHTML=`<kbd>${KB_PAL}</kbd>`;b.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();palOpen()});lab.append(b);
}
const KB_TIPS=[['nav [data-tab="inbox"]','g t'],['nav [data-tab="calendar"]','g c'],['.side-sub a[data-graph-sub="people"]','g p'],['.side-sub a[data-graph-sub="orgs"]','g o'],['.side-sub a[data-graph-sub="projects"]','g j'],['.side-sub a[data-graph-sub="roles"]','g w'],['#tab-fleet','g f'],['nav [data-tab="feedback"]','g l'],['nav [data-tab="health"]','g n'],['#open-settings','g ,']];
for(const [sel,keys] of KB_TIPS){const el=$(sel);if(!el)continue;const name=i18nEnglish(el.querySelector('.nl,.lbl'))||I18N.attrs.get(el)?.['aria-label']?.en||el.getAttribute('aria-label')||'';el.title=name+' ('+kbText(keys)+')';el.dataset.keys=kbText(keys);el.setAttribute('aria-keyshortcuts',kbAria(keys))}
const KB_CARD=[['[data-choice="snooze"]','s'],['[data-choice="complete"]','d'],['[data-rename]','e']];
function kbHints(){for(const [sel,keys] of KB_CARD)for(const b of document.querySelectorAll('#suggestions '+sel)){if(b.dataset.kb)continue;b.dataset.kb=keys;b.setAttribute('aria-keyshortcuts',kbAria(keys));
  b.dataset.kbLabel=kbPart(keys);if(!b.closest('.more-menu')&&!b.title)b.title=i18nEnglish(b)+' ('+kbPart(keys)+')'}}  // in a menu: a quiet key after the label (CSS)
new MutationObserver(()=>{kbHints();kbLive()}).observe($('#suggestions'),{childList:true,subtree:true});kbHints();
window.machineActions={add:actionAdd,list:()=>actsFor(kbCtx()),open:palOpen};
