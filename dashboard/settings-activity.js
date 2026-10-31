// Settings, Activity (activity_log.py, help: activity): one list of everything The Machine did, newest first, by day.
// Read-only: each line says what, when, where and who started it, and links to its to-do; a learning sent to The Machine
// team keeps its Withdraw, and a line with undo (a connected AI's Graph change) its Undo. The filter picks one kind, or what was refused or blocked. Fleet, Activity is this same list
// for the Fleet and learnings (actEmbed). Support access's looks come from Settings, Security (saData), added by time.
const ACT_KINDS=[['messages','Messages'],['docs','Docs'],['calendar','Calendar'],['web','Steps on the web'],['fixes','Fixes'],['agents','Coding agents'],['fleet','Fleet'],['learnings','Learnings'],['skills','Skills'],['graph','Graph'],['connections','Connections'],['access','Support access'],['ai','Connected AIs']];
const act={filter:'',items:[],next:null,kinds:[],busy:false,error:false,at:0,seq:0},actFleet={items:null,at:0,busy:false};
SETTINGS_OF['settings-activity']='activity';HELP_FOR.activity='activity';
{const d=document.createElement('div');d.id='settings-activity';
 d.innerHTML=`<div class="section-head"><h2>Activity</h2><p>Everything The Machine did for you, newest first. <a class="learn" href="${HELP}activity" target="_blank" rel="noopener">Learn more</a></p></div><div class="act-bar"><select id="act-filter" aria-label="Show"></select></div><ol class="act-list" id="act-list" aria-live="polite"></ol><button type="button" class="ghost act-more" id="act-more" hidden>Show more</button>`;
 $('#settings-support').after(d)}
// Support access's looks (hosted: the control plane; self-hosted: through the Fleet), as lines of this list
const actLooks=()=>(saData?.accesses||[]).map(a=>({id:'access:'+a.at,kind:'access',at:a.at,what:t(a.what),outcome:a.refused?'refused':'done',status:a.refused?t('Refused'):'',where:null,by:null,todo:null}));
function actShown(){if(Date.now()-act.at>30000&&!act.busy)actLoad()}
async function actLoad(more){const f=act.filter,seq=++act.seq;act.busy=true;actDraw();
 const q=f==='refused'?'outcome=refused':f?'kind='+encodeURIComponent(f):'';
 try{const r=f==='access'?{items:[],next:null,kinds:act.kinds}:await request('api/activity?'+q+(more&&act.next!=null?'&cursor='+act.next:''));if(seq!==act.seq)return;
  act.items=more?[...act.items,...(r.items||[])]:r.items||[];act.next=r.next??null;act.kinds=r.kinds||act.kinds;act.at=Date.now();act.error=false}
 catch(e){errCaught(e);if(seq===act.seq)act.error=true}
 finally{if(seq===act.seq){act.busy=false;actDraw()}}}
// One line: what, its outcome, then when · where · who started it; its to-do; a learning's Withdraw and what went
function actRow(x){const meta=[fmtHM(x.at),x.where,x.by].filter(Boolean).map(esc).join(' · '),sent=x.sent||{};
 const what=[sent.example?`<p>${esc(t('Example: {}',sent.example))}</p>`:'',...(sent.use_cases||[]).map(c=>`<p class="fine">${esc(c)}</p>`),sent.log?`<pre>${esc(sent.log)}</pre>`:''].join('');
 return `<li class="act-row act-${esc(x.outcome||'done')}"><div class="act-top"><span class="act-what">${esc(x.what)}</span>${x.status?`<span class="act-status">${esc(x.status)}</span>`:''}</div><small class="act-meta">${meta}</small>`
  +(x.detail?`<small class="act-meta">${esc(x.detail)}</small>`:'')+(what?`<details class="act-sent"><summary>${esc(t('What was sent'))}</summary>${what}</details>`:'')
  +(x.todo||x.withdraw||actUndoable(x)?`<div class="act-acts">${x.todo?`<button type="button" class="link act-todo" data-act-todo="${esc(x.todo.id)}"><span class="ell">${esc(t('To-do: {}',x.todo.title||t('(no title)')))}</span></button>`:''}${x.withdraw?`<button type="button" class="ghost" data-tl-withdraw="${esc(x.withdraw.id)}" data-n="${esc(x.withdraw.n)}">${esc(t('Withdraw'))}</button>`:''}${actUndoable(x)?`<button type="button" class="ghost" data-act-undo="${esc(x.undo.action)}" data-id="${esc(x.undo.id)}">${esc(t('Undo'))}</button>`:''}</div>`:'')+'</li>'}
// Undo on a line: the action it names takes it back (only the ones listed here, each an owner's dashboard action)
const ACT_UNDO=new Set(['ai_undo']),actUndoable=x=>!!x.undo&&ACT_UNDO.has(x.undo.action);
async function actUndo(b){if(!ACT_UNDO.has(b.dataset.actUndo))return;b.disabled=true;
 try{await sharePost(b.dataset.actUndo,{id:+b.dataset.id});toast(t('Undone.'));actChanged();if(typeof aiActivityReload==='function')aiActivityReload()}
 catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}}
document.addEventListener('click',e=>{const u=e.target.closest('[data-act-undo]');if(u)actUndo(u)});
function actRows(items){let day='',h='';for(const x of items){const d=new Date(x.at);if(isNaN(d))continue;const k=localDay(d);if(k!==day){day=k;h+=`<li class="act-day">${esc(t(humanDay(d)))}</li>`}h+=actRow(x)}return h}
// Lines by time: the page's own, and Support access's looks back to the oldest line loaded (all of them at the end)
function actMerged(items,next,filter){const looks=['','access','refused'].includes(filter)?actLooks().filter(x=>filter!=='refused'||x.outcome==='refused'):[];
 const oldest=next==null||!items.length?'':items.at(-1).at,keep=looks.filter(x=>!oldest||Date.parse(x.at)>=Date.parse(oldest));
 return [...items,...keep].sort((a,b)=>Date.parse(b.at)-Date.parse(a.at))}
function actDraw(){const list=$('#act-list');if(!list)return;const sel=$('#act-filter'),looks=actLooks();
 const kinds=new Set([...act.kinds,...(looks.length?['access']:[]),...(act.filter&&act.filter!=='refused'?[act.filter]:[])]);
 const opts=`<option value="">${esc(t('Everything'))}</option>`+ACT_KINDS.filter(([k])=>kinds.has(k)).map(([k,l])=>`<option value="${k}">${esc(t(l))}</option>`).join('')+`<option value="refused">${esc(t('Refused or blocked'))}</option>`;
 if(sel._opts!==opts){sel.innerHTML=opts;sel._opts=opts}sel.value=act.filter;
 const items=actMerged(act.items,act.next,act.filter);
 list.innerHTML=items.length?actRows(items):`<li class="act-empty muted">${esc(act.error?t('Can’t load the activity right now.'):act.busy?t('Loading…'):act.filter?t('Nothing like this yet.'):t('Nothing yet. What The Machine does for you shows here.'))}</li>`;
 $('#act-more').hidden=act.next==null;$('#act-more').disabled=act.busy}
$('#act-filter').onchange=e=>{act.filter=e.target.value;act.items=[];act.next=null;actLoad()};
$('#act-more').onclick=()=>actLoad(true);
// A to-do from a line: one on the list opens at once; a done one is read first (api/cards/done?id=)
async function actOpenTodo(id){if(state.suggestions?.some(s=>s.id===id)){chatGo(id);return}
 try{const r=await request('api/cards/done?id='+encodeURIComponent(id)),c=(r?.cards||[]).find(c=>c.id===id);if(!c){toast(t('That to-do is no longer here.'),true);return}doneExtra.set(c.id,c);cardsMerge();chatGo(c.id)}
 catch(e){errCaught(e);toast(e.message,true)}}
// Withdraw, here as in Fleet, Activity: the team no longer sees it, and both lists read again
async function actWithdraw(b){if(!confirm(t('Withdraw this learning? The team no longer sees it.')))return;b.disabled=true;
 try{const r=await sharePost('learnings_withdraw',{id:b.dataset.tlWithdraw,n:+b.dataset.n});if(r?.team_learnings)state.team_learnings=r.team_learnings;toast(t('Withdrawn. The team no longer sees it.'));actChanged()}
 catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}}
function actChanged(){act.at=0;actFleet.at=0;if(settingsNow==='activity'&&!$('#settings').hidden)actLoad();if(!$('#fleet').hidden)actFleetLoad()}
$('#settings-activity').addEventListener('click',e=>{const todo=e.target.closest('[data-act-todo]');if(todo){actOpenTodo(todo.dataset.actTodo);return}
 const w=e.target.closest('[data-tl-withdraw]');if(w)actWithdraw(w)});
// Fleet, Activity: this list for the Fleet and learnings. fleetView compares its HTML, so the box is a fixed shell and
// its lines are filled in place (actEmbedFill), after each fleetView render and after each read.
function actEmbed(){if(Date.now()-actFleet.at>30000&&!actFleet.busy)actFleetLoad();
 return `<div class="fleet-box act-embed"><h3>${esc(t('What your Machine asked, answered and shared'))}</h3><p class="sub">${esc(t('Questions to and from teammates, and learnings sent to The Machine team.'))} <button type="button" class="link" data-act-all>${esc(t('All activity'))}</button></p><div class="act-embed-body"></div></div>`}
function actEmbedFill(){const body=$('#fleet-view .act-embed-body');if(!body)return;const items=actFleet.items;
 const html=items==null?`<p class="muted">${esc(t('Loading…'))}</p>`:items.length?`<ol class="act-list">${actRows(items)}</ol>`:`<p class="muted">${esc(t('Nothing yet.'))}</p>`;
 if(body._html!==html){body.innerHTML=html;body._html=html}}
async function actFleetLoad(){actFleet.busy=true;try{const r=await request('api/activity?kind=fleet,learnings');actFleet.items=r.items||[];actFleet.at=Date.now()}
 catch(e){errCaught(e);if(actFleet.items==null){actFleet.items=[];actFleet.at=Date.now()}}finally{actFleet.busy=false;actEmbedFill()}}
$('#fleet-view').addEventListener('click',e=>{if(e.target.closest('[data-act-all]')){act.filter='';act.at=0;showSettings('activity');return}const todo=e.target.closest('.act-embed [data-act-todo]');if(todo){actOpenTodo(todo.dataset.actTodo);return}
 const w=e.target.closest('.act-embed [data-tl-withdraw]');if(w)actWithdraw(w)});
