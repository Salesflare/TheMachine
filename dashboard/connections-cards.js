// Disconnected lately (mail_grants.py receipts): a sign-in counts as removed only once Google confirmed the revoke
// (Microsoft and Zoom: once no copy is left here); until then it says why, and The Machine keeps trying.
const SIGNIN_NAME={google:'Google',microsoft:'Microsoft',zoom:'Zoom',salesforce:'Salesforce'};
function renderDisconnected(){const list=state.disconnected||[];setHTML($('#disconnected'),list.length?html`<div class="section-head"><h2>Disconnected lately</h2></div><div class="list disconnected-list">${list.map(r=>{const ok=r.state==='removed';return html`<article style="--c:var(--${ok?'mint':'amber'})"><h3>${r.email}</h3><div class="row">${chip(ok?'Removed, confirmed':`Pending: ${SIGNIN_NAME[r.provider]||'The provider'} hasn’t confirmed. Retrying`,ok?'mint':'amber')}<small>${SIGNIN_NAME[r.provider]||r.provider}</small>${time(r.at)}</div></article>`})}</div>`:html``)}
// The last syncs as bars; none when every one brought nothing and none failed (a row of empty bars says nothing)
function spark(c){const a=[...(c.sync_activity||[])].reverse();if(!a.some(x=>x.signals||x.status!=='success'))return '';const max=Math.max(1,...a.map(x=>x.signals||0));return html`<div class="spark" role="img" aria-label="${(f=>a.length===1?t('Last sync: {} failed',f):t('Last {} syncs: {} failed',a.length,f))(a.filter(x=>x.status!=='success').length)}">${a.map(x=>x.status!=='success'?html`<i class="fail" style="height:100%" title="${date(x.at)} · ${syncError(x.error)}"></i>`:html`<i class="${x.signals?'':'zero'}" style="height:${x.signals?Math.max(18,Math.round(x.signals/max*100)):10}%" title="${date(x.at)} · ${t(['{} signal','{} signals'],x.signals??0)}"></i>`)}</div>`}
// Connections' sub-tabs: the sources by kind, then saved sign-ins and the reviews. A tab with a source that needs
// the owner's help (orange) shows how many (amber ones retry or catch up by themselves); the first such tab opens
// unless one was picked. Like every tab row, a number means something needs you: Sign-ins has none (a saved sign-in never needs anything), Friends only when waiting.
const HEALTH_GROUPS={gmail:'mail',calendar:'mail',outlook:'mail',outlook_calendar:'mail',imap:'mail',slack:'chat',whatsapp:'chat',telegram:'chat',signal:'chat',discord:'chat',teams:'chat'};  // Android sits in Other sources: most phones (iPhones) have no notification feed to give
const healthGroup=s=>HEALTH_GROUPS[s]||'other';
function renderHealthTabs(){const cs=state.connectors||[],bad=g=>cs.filter(c=>healthGroup(c.service)===g&&connectorTone(c)==='orange').length;
 const panes=[['mail','Mail and calendar'],['chat','Chat'],['other','Other sources']].filter(([g])=>cs.some(c=>healthGroup(c.service)===g)).map(([id,label])=>({id,label,badge:bad(id),warn:true}));
 if(!panes.length)panes.push({id:'mail',label:'Sources'});
 panes.push({id:'add',label:'+ Add'});
 if(savedLoginCount||healthPicked&&healthPane==='signins')panes.push({id:'signins',label:'Sign-ins'});panes.push({id:'reviews',label:'Checks'});
 const ids=panes.map(p=>p.id),current=healthPicked&&ids.includes(healthPane)?healthPane:panes.find(p=>p.badge&&p.warn)?.id||(ids.includes(healthPane)?healthPane:ids[0]);
 healthPane=current;const row=$('#health-tabs');setHTML(row,subTabs('Connections','data-health-pane',panes,current));
 for(const el of document.querySelectorAll('#health [data-health-for]'))el.hidden=!el.dataset.healthFor.split(' ').includes(current);
 for(const a of document.querySelectorAll('#connectors>article'))a.hidden=a.dataset.group!==current;if(!$('#health').hidden)tabsShow(row.firstChild);if(current==='add')connectAdd();
 else if(!connectResumed&&!healthPicked&&!$('#health').hidden){connectResumed=true;connectResume().then(found=>{if(found&&!healthPicked){healthPane='add';healthPicked=true;renderHealthTabs();renderConnectRun()}})}}  // measured once the other panes are hidden, never with every source shown at once
// and only while Connections shows: every redraw calls this, and a measure mid-redraw lays out the whole page (some 60 ms
// of each click that redraws). Opening Connections (showTab) calls it again, and measures then.
const BROKER_LINK={gmail:'#google',calendar:'#google',outlook:'#microsoft',outlook_calendar:'#microsoft',zoom:'#source-zoom',stripe:'#source-stripe',slack:'#source-slack',salesforce:'#source-salesforce'};
// Only the latest load draws: opening + Add starts one and connectOpen another, and the earlier answering last would
// draw the grid again over the source connectOpen just picked
let connectAddSeq=0,connectAddLast=Promise.resolve();
// A setup under way (connect_running) resumes at its step, on any device
let connectResumed=false,connectPicking=false;
async function connectResume(){if(connectPicking)return false;try{const r=await connectPost('connect_running');if(!r?.session||connectRun)return false;
 connectRun=r;connectSignin=null;connectForm=null;connectGbrain=null;$('#connect-add').dataset.sig='';connectPoll();return true}catch{return false}}
async function connectAddNow(force){if(connectRun)return;if(!force&&connectList&&Date.now()-connectListAt<60000)return;connectListAt=Date.now();
 const n=++connectAddSeq;  // before the wait: a later call (a forced one from a sign-in's way back) wins over this one
 const box=$('#connect-add');if(!box.childElementCount)setHTML(box,html`<p class="muted">Loading…</p>`);  // a restart's few seconds: not an empty box
 if(await connectResume()){renderConnectRun();return}
 if(n!==connectAddSeq)return;
 const load=connectPost('connect_sources');connectAddLast=load.catch(()=>{});
 try{const list=await load;if(n!==connectAddSeq)return;connectList=list}catch(e){if(n!==connectAddSeq)return;errCaught(e);setHTML($('#connect-add'),html`<p class="error">${e.message}</p>`);return}renderConnectAdd()}
// once the latest load has drawn (connectOpen)
async function connectAddSettled(){for(let n=-1;n!==connectAddSeq;){n=connectAddSeq;await connectAddLast}}
// + Add shows one view at a time in its box: the grid of sources, or one source's sign-in, form, run or GBrain panel.
// Another view than before starts at its top, under the top bar, with focus on it (its first field, else its heading):
// from far down the grid the page would otherwise stay down there, the short view above it and only the footer showing.
// Back to the grid returns to where it was, on the tile it left from (connectGrid, noted on the tap).
let connectGrid=null;
function connectDraw(box,kind,h,focus){const was=box.dataset.view;setHTML(box,h);box.dataset.view=kind;if(was===kind)return;
 if(kind==='grid'){const g=connectGrid;connectGrid=null;if(!g||!was)return;const tile=[...box.querySelectorAll('.connect-source')].find(n=>placeSig(n)===g.sig);
  scrollTo(scrollX,g.y);tile?.focus({preventScroll:true});placeNote();return}
 viewTop(box,focus&&box.querySelector(focus))}
$('#connect-add').addEventListener('click',e=>{const tile=e.target.closest('.connect-sources>button.connect-source');if(tile)connectGrid={y:scrollY,sig:placeSig(tile)}},true);
// The list: Suggested for you first, at most 3 (connect_suggested: only tiles with a signal, never a connected one), each
// with its why; then every source under its group (onboarding.GROUPS), A to Z within it, a suggested one there too, tagged
// Suggested, with what it brings in. Both rows open the same connect. A group with nothing to show is left out.
const CONNECT_GROUPS=[['mail','Mail and calendar'],['chat','Chat'],['meetings','Meetings'],['docs','Docs and files'],['customers','Customers'],['work','Projects and code'],['other','Other']];
const connectWhy=(s,x)=>s.why==='unfinished'?t('Setup didn’t finish'):s.why==='mail'?t(['{} email from {} in 30 days','{} emails from {} in 30 days'],s.count,x.label)
 :s.why==='meetings'?t(['{} {} meeting on your calendar','{} {} meetings on your calendar'],s.count,x.label):s.why==='links'?t(['{} message links to {}','{} messages link to {}'],s.count,x.label):'';
// A row: the source's logo (dashboard/logos/, else a line icon below), its name (and a Suggested tag), why it is
// suggested or what it brings in, never cut off, and › (↗: opens elsewhere). Connected: a check on the icon, still tappable for a second
// account. `note`: a status line of its own (Codex, GBrain).
Object.entries({outlook:ICONS.gmail,outlook_calendar:ICONS.calendar,teams:'<path d="M4 5h11v8H8l-4 3z"/><path d="M15 9h5v8l-3-2h-5v-2"/>',
 zoom:'<rect x="3" y="6" width="12" height="12" rx="2"/><path d="m15 10 6-3v10l-6-3"/>',docs:'<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
 intercom:'<path d="M4 5h16v11H9l-5 4z"/><path d="M8.5 9v3M12 8v5M15.5 9v3"/>',rss:'<path d="M5 19h.01M5 12a7 7 0 0 1 7 7M5 5a14 14 0 0 1 14 14"/>',
 shortcut:'<path d="M6 21V4h12l-3 4 3 4H6"/>',salesforce:'<path d="M7 18a4 4 0 0 1-.6-7.95A5 5 0 0 1 16 8.5a4.5 4.5 0 0 1 1.5 8.75L17 18z"/>',trello:'<rect x="3" y="3" width="18" height="18" rx="2"/><rect x="6.5" y="6.5" width="4" height="10" rx="1"/><rect x="13.5" y="6.5" width="4" height="6" rx="1"/>',
 codex:'<path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 6l-3 12"/>',gbrain:'<circle cx="12" cy="12" r="8"/><path d="M12 4v16M8.5 8.5c2 1 2 2.5 0 3.5s-2 2.5 0 3.5M15.5 8.5c-2 1-2 2.5 0 3.5s2 2.5 0 3.5"/>'})
 .forEach(([k,v])=>{if(!ICONS[k])ICONS[k]=v});
const CONNECT_ICON={google_meet:'zoom',google_docs:'docs',crm:'salesflare'};
// The service's own logo (dashboard/logos, its NOTICE.md), loaded when shown; Machine health is our robot. Else a line icon.
const LOGOS=/^(android|calendar|codex|crm|docs|github|gmail|google_docs|google_meet|intercom|linkedin|outlook|outlook_calendar|rss|salesforce|shortcut|slack|stripe|teams|telegram|trello|whatsapp|x|zoom)$/,
 connectLogo=(x,n=x.name)=>n==='gateway'||LOGOS.test(n)?html`<span class="icon brand${/^(x|github|intercom|codex)$/.test(n)?' mono':''}" aria-hidden="true"><img src="brand/${n==='gateway'?'avatar.png':'logos/'+n+(n==='zoom'?'.png':'.svg')}" alt="" loading="lazy" width="20" height="20"></span>`:icon(CONNECT_ICON[n]||x.service||n);
// Already connected: which account, on the row ("Connected: kris@…"), and on the source's add view a line that this adds
// another connection beside it, with a way to its card. Adding one more stays possible. Its own accounts only (not one a
// teammate shares), matched by service as connect_sources counts them.
const connectHave=x=>x?.connected?(state.connectors||[]).filter(c=>c.service===x.service&&!c.shared_by):[],connectHaveName=c=>c.display_name||c.email||c.id;
function connectHaveLine(x){const have=connectHave(x);return !have.length?'':have.length===1?t('Connected: {}',connectHaveName(have[0])):t(['Connected: {} and {} more','Connected: {} and {} more'],connectHaveName(have[0]),have.length-1)}
function connectHaveNote(x){const have=connectHave(x);if(!have.length)return '';
 return html`<p class="fine connect-note connect-have"><span>${connectHaveLine(x)}</span> <button type="button" class="browser-link" data-connect-card="${have[0].id}">${t('Open its card')}</button><br><span>${t('This adds a new connection. Existing ones stay.')}</span></p>`}
function connectInner(x,why,ext,note=connectHaveLine(x),tag=false){const on=x.connected?html`<span class="cs-on" title="${t('{} connected',x.connected)}" aria-label="${t('{} connected',x.connected)}">✓</span>`:'';
 const line=why?html`<small class="why">${why}</small>`:x.what?html`<small class="what">${x.what}</small>`:'';
 return html`<span class="cs-icon">${connectLogo(x)}${on}</span><span class="cs-text"><span class="cs-head"><b>${x.label}</b>${tag?html`<span class="cs-tag">${t('Suggested')}</span>`:''}</span>${line}${note?html`<small class="count">${note}</small>`:''}</span><span class="cs-go" aria-hidden="true">${ext?'↗':'›'}</span>`}
function connectTile(x,why,tag){const inner=ext=>connectInner(x,why,ext,undefined,tag);
 if(x.hosted_signin&&connectList.manage_url)return html`<button type="button" class="connect-source" data-connect-signin="${x.name}">${inner()}</button>`;
 if(x.account_page&&connectList.manage_url)return html`<a class="connect-source" href="${safeHref(connectList.manage_url+'#'+x.account_page)}" target="_blank" rel="noopener">${inner(true)}</a>`;
 if(x.signin&&!connectList.manage_url)return html`<button type="button" class="connect-source" data-connect-signin="${x.name}">${inner()}</button>`;
 return x.broker?(connectList.manage_url?html`<a class="connect-source" href="${safeHref(connectList.manage_url+(BROKER_LINK[x.service]||'#sources'))}" target="_blank" rel="noopener">${inner(true)}</a>`:''):html`<button type="button" class="connect-source" data-connect="${x.name}">${inner()}</button>`}
function renderConnectAdd(){const box=$('#connect-add');if(connectRun)return renderConnectRun();if(connectSignin)return renderConnectSignin();if(connectForm)return renderConnectForm();if(connectGbrain)return renderGbrain();if(!connectList)return;
 const by=new Map(connectList.sources.map(x=>[x.name,x])),why=new Map();
 for(const s of connectList.suggested||[]){const x=by.get(s.name),w=x&&!x.connected&&why.size<3&&connectWhy(s,x);if(w&&connectTile(x,w))why.set(s.name,w)}  // only one it can show
 // A to Z in each group; a catch-all (last, groups.CATCH_ALL: Other email) after the rest
 const groups=new Map(CONNECT_GROUPS.map(([k])=>[k,[]])),add=(g,label,tile,last)=>{if(tile)(groups.get(g)||groups.get('other')).push([label,tile,!!last])};
 // Teams: one Microsoft sign-in, two tiles. Its chats under Chat, its meeting notes under Meetings as Teams meetings; either
 // one connects both, and both show it connected. Its card on Connections keeps the whole line (connectors/teams.py).
 for(const x of connectList.sources){const teams=x.service==='teams'&&x.group==='chat';
  add(x.group,x.label,connectTile(teams?{...x,what:t('Chats and meeting chats from Teams. Reads only.')}:x,'',why.has(x.name)),x.last);
  if(teams)add('meetings',t('Teams meetings'),connectTile({...x,label:t('Teams meetings'),what:t('Meeting notes and transcripts from Teams. Reads only.')}))}
 add('work','Codex',codexTile());add('other','GBrain',gbrainTile());
 const picks=[...why].map(([n,w])=>connectTile(by.get(n),w));
 const order=new Intl.Collator(I18N.lang||'en',{sensitivity:'base'}),list=(h,tiles,cls='')=>html`<section class="connect-group${cls}"><h4>${h}</h4><div class="connect-sources">${tiles}</div></section>`;
 const rest=CONNECT_GROUPS.map(([k,h])=>{const g=groups.get(k).sort((a,b)=>a[2]-b[2]||order.compare(a[0],b[0]));return g.length?list(t(h),g.map(([,tile])=>tile)):''});
 connectDraw(box,'grid',html`${connectList.saveable||connectList.manage_url?'':html`<p class="sub-note">Pick a source to connect.${html` This service can’t save its settings: use <code>assistant connect</code> in a terminal.`}</p>`}${picks.length?list(t('Suggested for you'),picks,' suggested'):''}${rest}`)}
// Codex (codex_signin.py): its own tile. It signs in with Codex's own device code, shown here: a hosted Machine's control
// plane runs that sign-in on its server (POST /_machine/connect, like GitHub), a self-hosted Machine runs it itself.
const CODEX_DEVICE=/^https:\/\/auth\.openai\.com\/codex\/device[\w/.-]*$/;
const codexSource=()=>({name:'codex',service:'codex',label:'Codex',broker:true,connected:connectList?.codex?.status==='connected'?1:0,...(connectList?.manage_url?{hosted_signin:'codex'}:{signin:'codex'})});
const codexTile=()=>{const c=connectList?.codex;if(!c)return '';
 return html`<button type="button" class="connect-source" data-codex-signin>${connectInner({name:'codex',service:'codex',label:'Codex',what:'Coding to-dos on your ChatGPT plan',connected:c.status==='connected'?1:0},'',false,c.status==='connected'?'Connected':c.status==='signed_out'?'Signed out':'')}</button>`};
const CODEX_TIP=html`<details class="connect-alt"><summary>OpenAI turns the code down?</summary><p>Turn on device code sign-in for Codex in ChatGPT security settings, at the bottom. Then try again.</p><p><a class="browser-link" href="https://chatgpt.com/settings/security" target="_blank" rel="noopener">Open ChatGPT security settings ↗</a></p></details>`;
function codexBody(s,back){const c=connectList?.codex||{},again=html`<div class="actions"><button type="button" class="primary" data-signin-go>Try again</button>${back}</div>`;
 if(s.state==='checking'||s.state==='starting')return html`<p class="muted">Getting a sign-in code from OpenAI…</p>`;
 if(s.state==='code'&&CODEX_DEVICE.test(s.url||''))return html`${connectCodeHTML({kind:'openai',code:s.code,url:s.url})}${CODEX_TIP}`;
 if(s.state==='connecting'||s.state==='code')return html`<p class="muted">Signed in. Connecting it now.</p>`;
 if(s.state==='done')return html`<p class="note sent-ok"><span>Connected.</span> <span>Hand a coding to-do to Codex to use it.</span></p><div class="actions">${back}</div>`;
 if(s.state==='missing')return html`<p>Codex isn’t on this computer yet. Install it in a terminal, then try again.</p><pre class="signin-command">npm install -g @openai/codex</pre><p class="gbrain-links"><button type="button" class="browser-link" data-copy-command="npm install -g @openai/codex">Copy command</button></p>${again}`;
 if(s.state==='failed'||s.state==='stopped')return html`<p class="alert">${s.state==='stopped'?'That sign-in didn’t finish.':s.error||'Not connected.'}</p>${again}${CODEX_TIP}`;
 if(c.status==='connected')return html`<p class="note sent-ok">Codex is signed in. Hand a coding to-do to Codex to use it.</p><div class="actions">${back}</div>`;
 return html`<p class="muted">Hand coding to-dos to Codex, on your ChatGPT plan. OpenAI gives you a code to sign in with.</p><div class="actions"><button type="button" class="primary" data-signin-go>Get a code</button>${back}</div>`}
// Self-hosted: this Machine runs Codex's sign-in (codex_signin) and the form follows it
async function codexGo(s){connectSignin={...s,state:'starting',error:''};$('#connect-add').dataset.sig='';renderConnectSignin();
 try{const r=await connectPost('codex_signin');if(connectSignin?.provider==='codex')connectSignin={...connectSignin,...r}}catch(err){errCaught(err);connectSignin={...connectSignin,state:'failed',error:err.message}}
 $('#connect-add').dataset.sig='';renderConnectSignin();codexPoll()}
function codexPoll(){clearTimeout(signinTimer);const s=connectSignin;if(s?.provider!=='codex'||s.hosted||!['starting','code'].includes(s.state))return;
 signinTimer=setTimeout(async()=>{try{const r=await connectPost('codex_signin_state');if(connectSignin!==s)return;connectSignin={...s,...r};$('#connect-add').dataset.sig='';renderConnectSignin();
  if(r.state==='done'){connectList=null;connectAdd(true)}}catch{}codexPoll()},2000)}
// GBrain: an optional add-on, only on a Machine that runs on its owner's computer. Off until the owner agrees to what
// goes in; the panel shows how to install it, that consent step, or how the sync goes (and turns it off again).
const gbrainTile=()=>connectList?.gbrain?html`<button type="button" class="connect-source" data-gbrain>${connectInner({name:'gbrain',service:'gbrain',label:'GBrain',what:'A memory app for AI tools, on this computer',connected:connectList.gbrain.on?1:0},'',false,connectList.gbrain.on?'On':'')}</button>`:'';
async function gbrainOpen(){connectGbrain={loading:true};$('#connect-add').dataset.sig='';renderGbrain();
 try{connectGbrain=await connectPost('gbrain_status')}catch(e){errCaught(e);connectGbrain={error:e.message}}renderGbrain()}
function renderGbrain(){const g=connectGbrain,box=$('#connect-add'),back=html`<button type="button" data-connect-back>Back</button>`;let body;
 if(g.loading)body=html`<p class="muted">Checking for GBrain…</p>`;
 else if(g.error&&!('on' in g))body=html`<p class="alert">${g.error}</p><div class="actions"><button type="button" data-gbrain-check>Check again</button>${back}</div>`;
 else if(g.on){const pages=g.kept?t('{} pages, {} kept as you edited them',g.pages,g.kept):t(['{} page','{} pages'],g.pages);
  body=html`<p class="sent-ok">Connected</p><dl class="gbrain-facts"><dt>Brain</dt><dd><code>${g.brain||''}</code></dd>${g.version?html`<dt>Version</dt><dd>${g.version}</dd>`:''}<dt>Pages</dt><dd>${pages}</dd><dt>Last sync</dt><dd>${ago(g.last_sync)}</dd>${g.last_error?html`<dt>Problem</dt><dd class="error">${g.last_error}</dd>`:''}</dl>
  <label class="gbrain-check"><input type="checkbox" data-gbrain-work${g.work?' checked':''}${g.saveable?'':' disabled'}><span>Include Work people and companies</span></label>
  <p class="fine muted">Turning off keeps your brain and its pages.</p><div class="actions"><button type="button" data-gbrain-off${g.saveable?'':' disabled'}>Turn off</button>${back}</div>`}
 else if(!g.installed)body=html`<p>GBrain isn’t on this computer yet. Install it in a terminal, then check again.</p><pre class="signin-command">bun install -g github:garrytan/gbrain</pre><p class="gbrain-links"><button type="button" class="browser-link" data-copy-command="bun install -g github:garrytan/gbrain">Copy command</button><a class="browser-link" href="https://github.com/garrytan/gbrain" target="_blank" rel="noopener">About GBrain ↗</a></p><div class="actions"><button type="button" data-gbrain-check>Check again</button>${back}</div>`;
 else body=html`${g.version?html`<p class="muted">${t('Found {} at {}',g.version,g.brain||'')}</p>`:''}<p>What goes into GBrain:</p><ul class="gbrain-list"><li>People and projects from your Graph, with a link back</li><li>What The Machine learned about how you work</li></ul><p>Message text never goes in.</p><p><b>GBrain may send this to its own AI providers.</b></p>
  <label class="gbrain-check"><input type="checkbox" data-gbrain-work-pick><span>Include Work people and companies</span></label><label class="gbrain-check"><input type="checkbox" data-gbrain-consent><span>I agree</span></label>
  ${g.saveable?'':html`<p class="fine muted">${CANT_SAVE}</p>${cantSaveMore('gbrain')}`}<p class="error" role="status">${g.error||''}</p><div class="actions"><button type="button" class="primary" data-gbrain-on disabled>Connect GBrain</button>${back}</div>`;
 const panel=html`<div class="connect-run gbrain-panel"><h3>GBrain</h3>${g.loading||g.on?'':html`<p class="muted">Optional, for developers. Keep your own AI memory app in sync with The Machine.</p><p class="muted">Checks can read your brain to write better to-dos.</p>`}${body}</div>`,sig=JSON.stringify(['gbrain',g]);if(box.dataset.sig===sig)return;box.dataset.sig=sig;connectDraw(box,'gbrain',panel)}
async function gbrainDo(action,args,b){if(b)b.disabled=true;try{connectGbrain=await connectPost(action,args);if(connectList?.gbrain)connectList.gbrain.on=!!connectGbrain.on}catch(e){errCaught(e);if(action==='gbrain_on'){connectGbrain={...connectGbrain,error:e.message}}else toast(e.message,true)}renderGbrain()}
$('#connect-add').addEventListener('click',e=>{const t=e.target;if(t.closest('[data-gbrain]')){gbrainOpen();return}
 if(t.closest('[data-gbrain-check]')){gbrainOpen();return}
 const on=t.closest('[data-gbrain-on]');if(on){gbrainDo('gbrain_on',{consent:$('[data-gbrain-consent]').checked,work:$('[data-gbrain-work-pick]').checked},on);return}
 const off=t.closest('[data-gbrain-off]');if(off){gbrainDo('gbrain_off',{},off);return}
});
$('#connect-add').addEventListener('change',e=>{if(e.target.matches('[data-gbrain-consent]')){const b=$('[data-gbrain-on]');if(b)b.disabled=!e.target.checked||!connectGbrain?.saveable;return}
 if(e.target.matches('[data-gbrain-work]'))gbrainDo('gbrain_work',{on:e.target.checked})});
// `name`, not `source`: the dashboard's requests carry their own `source`. With an account: that one signs in again.
async function connectStart(name,account,form){try{connectRun=await connectPost('connect_start',account?{name,account}:{name,...form});connectForm=null;$('#connect-add').dataset.sig='';renderConnectRun();connectPoll();return true}catch(err){errCaught(err);toast(err.message,true);return false}}
// + Add, one source: everything it asks at once, as the account's setup page does. Its questions and how to get a key
// come from the Machine (onboarding.web_form); Work or Personal is two choices, the company prefilled. Connect runs the
// same steps as before, with these answers; anything they leave open is still asked here, one at a time.
function renderConnectForm(){const x=connectList?.sources.find(v=>v.name===connectForm),box=$('#connect-add');if(!x){connectForm=null;return renderConnectAdd()}
 const f=x.form||{},sig=JSON.stringify(['form',x.name]);if(box.dataset.sig===sig)return;box.dataset.sig=sig;
 const asks=(f.ask||[]).map(([k,q])=>html`<label>${q}<input name="ask" data-key="${k}" type="text" required spellcheck="false" autocomplete="off"></label>`);
 const secret=f.secret?html`${f.token_url?html`<p class="connect-token"><a class="btn-link" href="${safeHref(f.token_url)}" target="_blank" rel="noopener"><span>Get your token</span> ↗</a></p>`:''}<label>${f.secret}<input name="secret" type="password" required autocomplete="off" spellcheck="false"></label>`:'';
 // Folded-away settings (an IMAP mailbox's servers): left empty, the Machine fills them in for the address
 const advanced=f.advanced?.length?html`<details class="connect-alt connect-advanced"><summary>Server settings</summary><p class="fine muted">Filled in for most providers. Change them only if yours says so.</p><div class="connect-advanced-grid">${f.advanced.map(([k,q,o])=>o?html`<label>${q}<select name="ask" data-key="${k}"><option value="">Automatic</option>${o.map(v=>html`<option value="${v}">${v}</option>`)}</select></label>`:html`<label class="${k==='username'?'wide':''}">${q}<input name="ask" data-key="${k}" type="text"${/port$/.test(k)?html` inputmode="numeric" maxlength="5"`:''} spellcheck="false" autocomplete="off"></label>`)}</div></details>`:'';
 const scope=f.scope&&!f.auto?html`<fieldset class="connect-scope"><legend>Work or personal?</legend><label><input type="radio" name="scope" value="work"${f.personal?'':html` checked`}> Work</label><label><input type="radio" name="scope" value="personal"${f.personal?html` checked`:''}> Personal</label></fieldset><label class="connect-company"${f.personal?html` hidden`:''}>Company<input name="company" maxlength="60" value="${f.company||''}"${f.company?html` data-typed="1"`:''} placeholder="Acme" autocomplete="organization"${f.personal?'':html` required`}><small class="fine muted">Working for yourself? Use your business name.</small></label>`:'';
 connectDraw(box,'form',html`<div class="connect-run"><h3>${x.label}</h3>${x.what||f.learn?html`<p class="muted">${x.what||''}${f.learn?html` <a class="learn" href="${safeHref('https://themachine.computer/help/'+encodeURIComponent(f.learn))}" target="_blank" rel="noopener">${t('Learn more')}</a>`:''}</p>`:''}${f.note?html`<p class="fine connect-note">${linkify(f.note)}</p>`:''}${connectHaveNote(x)}<form class="connect-form connect-setup" data-connect-setup="${x.name}" novalidate>${asks}${secret}${advanced}${scope}<p class="error" role="status"></p><div class="actions"><button class="primary">Connect</button><button type="button" data-connect-back>Back</button></div></form></div>`,'input:not([type="radio"]):not([hidden])')}
async function connectSetup(form){const name=form.dataset.connectSetup,err=form.querySelector('.error'),go=form.querySelector('button.primary');
 const missing=[...form.querySelectorAll('input[required]')].find(i=>!i.closest('[hidden]')&&!i.value.trim());if(missing){{const what=(missing.closest('label')?.firstChild?.textContent||'').trim();err.textContent=what?t('Fill in {}.',what):t('Fill this in.')}missing.focus();return}
 const answers={};for(const i of form.querySelectorAll('[name="ask"]'))answers[i.dataset.key]=i.value.trim();
 const scope=form.querySelector('input[name="scope"]:checked')?.value,payload={form:true,answers,secret:form.querySelector('input[name="secret"]')?.value||'',...(scope?{scope,company:scope==='work'&&form.querySelector('input[name="company"]')?.value.trim()||''}:{})};
 err.textContent='';go.disabled=true;if(!await connectStart(name,null,payload))go.disabled=false}
// Sign in with <provider> on a self-hosted Machine: the Machine asks the control plane for a one-time start link,
// signed with its own key, and it opens in a new tab. The token comes back sealed for this Machine, which checks it.
// off: what it says when the control plane has no app for this sign-in (connect_sources signin_off), above the other way
// later: one line under `about` on what to expect while it reads (Slack: its read limit, new messages first)
const SIGNIN_COPY={intercom:{label:'Intercom',about:'Reads your conversations. Replies only after you approve them, as yourself. Never assigns or closes.'},
 salesforce:{label:'Salesforce',about:'Deals, tasks and activity. Changes contact details only if you turn that on.'},
 trello:{label:'Trello',about:'Reads cards, comments and activity on one board you pick next. Never changes anything in Trello.'},
 google:{label:'Google',about:'Gmail and Google Calendar. Sends only emails you approved.',other:'Use your own app',how:'Your own Google Cloud app, step by step.',go:'Set it up',off:'Sign in with {} isn’t available yet. Use your own app instead.'},
 microsoft:{label:'Microsoft',about:'Outlook mail and calendar. Sends only emails you approved.',other:'Use your own app',how:'Your own Microsoft app registration, step by step.',go:'Set it up',off:'Sign in with {} isn’t available yet. Use your own app instead.'},
 github:{label:'GitHub',about:'Review requests, mentions, assignments and failed CI runs. Files issues only when you confirm.'},
 zoom:{label:'Zoom',about:'Your meeting summaries and transcripts. Reads only.',other:'Use your own app',how:'Your own Zoom app, step by step.',go:'Set it up',off:'Sign in with {} isn’t available yet. Use your own app instead.'},
 microsoft_docs:{label:'Microsoft',title:'Microsoft OneDrive',about:'Word, OneDrive and SharePoint. Outlook isn’t needed. Edits wait for your OK.'},
 microsoft_docs_write:{label:'Microsoft',title:'Microsoft OneDrive',about:'Lets The Machine create and edit your Word documents. Each change waits for your OK.'},
 google_meet:{label:'Google',title:'Google Meet',about:'Transcripts and Gemini notes of your meetings. Reads only.'},
 microsoft_teams:{label:'Microsoft',title:'Microsoft Teams',about:'Your chats and meeting chats. Channels and meeting notes need your admin’s OK. Reads only.'},
 google_docs:{label:'Google',title:'Google Docs',about:'Reads and edits the docs you point it to, and makes new ones. Edits wait for your OK.'},
 whatsapp:{label:'WhatsApp',about:'Your WhatsApp chats, as a linked device. Replies only when you press Send on a to-do.'},
 android:{about:'The notifications on your Android phone, through the OpenClaw app.'},
 stripe:{label:'Stripe',about:'Failed payments, disputes, cancellations and new subscriptions. Reads only, never changes anything in Stripe.',other:'Or paste a restricted key',how:'A restricted key with Read on Events, Customers and Account.',go:'Paste a key',off:'Sign in with {} isn’t available yet. Paste a restricted key instead.'},
 slack:{label:'Slack',about:'Your DMs and the channels you’re in. Sends only messages you approved, as yourself.',later:'New messages come in first, older ones gradually.',other:'Or use a Maton API key',how:'Connect Slack in Maton, then paste your Maton API key.',go:'Use Maton',off:'Sign in with {} isn’t available yet. Use a Maton API key instead.'}};
// A work organization that lets only approved apps in: the short link its Microsoft 365 admin approves The Machine with.
// It opens Microsoft's approval page with a fresh signed state on each visit (the control plane's site), so it never expires.
const MS_ADMIN_LINK='https://themachine.computer/m365-admin-consent';
// Teams: its own link, which also approves channels, transcripts and Copilot's meeting notes for the organization
const msAdmin=s=>{const link=s.provider==='microsoft_teams'?MS_ADMIN_LINK+'/teams':s.provider==='microsoft'?MS_ADMIN_LINK:'';return !link?'':html`<div class="connect-admin"><p>Need your admin’s approval? Send them this link.</p><div class="connect-admin-link"><a href="${link}" target="_blank" rel="noopener" translate="no">${link.replace('https://','')}</a><button type="button" data-copy-link="${link}">Copy link</button></div></div>`};
const signinOf=(x,state,command)=>{const hosted=!!(connectList?.manage_url&&x.hosted_signin),p=hosted?x.hosted_signin:x.signin===true?x.service:x.signin;
 return {source:x.name,provider:p,label:SIGNIN_COPY[p]?.label||x.label,own:!x.broker,hosted,another:!!x.connected,state,...(command?{command}:{}),...(!hosted&&x.signin_off?{off:true}:{})}};
// A hosted Machine: Work or Personal here, then Sign in goes to the provider in this tab and comes back to this form.
// Pasting a key or token stays on the account page's tile.
const HOSTED_TILE={google:'#google',microsoft:'#microsoft',microsoft_teams:'#teams',zoom:'#source-zoom',stripe:'#source-stripe',slack:'#source-slack',intercom:'#source-intercom',trello:'#source-trello',github:'#source-github',salesforce:'#source-salesforce'};
// GitHub, WhatsApp and the phone have no provider page to come back from: the Machine gets a code, shown right here
// (GitHub's to type at GitHub, WhatsApp's QR code or pairing code, the OpenClaw app's setup code)
const GITHUB_DEVICE=/^https:\/\/github\.com\/login\/device[\w/.-]*$/;
const NO_SCOPE_SIGNIN=['intercom','android','microsoft_docs','microsoft_docs_write','microsoft_teams','codex'];
const STARTING={github:'Getting a sign-in code from GitHub…',whatsapp:'Getting a code from WhatsApp…',android:'Making a setup code…'};
const qrImg=s=>html`<img class="connect-qr" src="${safeHref('/_machine/connect-qr?s='+encodeURIComponent(s.provider)+'&c='+encodeURIComponent(s.command)+'&v='+encodeURIComponent(String(s.until||'')))}" alt="QR code">`;
function phoneBody(s,back){const h=[];
 if(s.code)h.push(html`<p class="connect-q">In the OpenClaw app on your phone, add a Gateway and scan this code, or copy it and paste it there:</p>${qrImg(s)}<div class="actions"><button type="button" data-copy-command="${s.code}">Copy code</button></div><p class="muted">It works for 10 minutes, once.</p>`);
 for(const q of s.pending||[])h.push(html`<div class="connect-wait"><p>${t('{} asks to pair with your Machine. Is that your phone? Approve only this one.',q.name||t('A phone'))}</p><button type="button" class="primary" data-phone-approve="${q.id}" data-kind="${q.kind}">Approve</button></div>`);
 const p=s.phone;if(p)h.push(html`<p class="note">${!p.connected?t('{} is paired but not connected. Open the OpenClaw app on it.',p.name):!p.notifications?t('{} is connected. Now allow notification access for OpenClaw on the phone.',p.name):t('{} is connected. Adding its notifications…',p.name)}</p>`);
 if(!h.length)h.push(html`<p class="muted">Making a setup code…</p>`);
 return html`${h}<p class="muted">Waiting for your phone. This updates by itself.</p><div class="actions">${back}</div>`}
function hostedSigninBody(s,copy,back){const scope=NO_SCOPE_SIGNIN.includes(s.provider)?'':html`<fieldset class="connect-scope"><legend>Work or personal?</legend><label><input type="radio" name="signin-scope" value="work" checked> Work</label><label><input type="radio" name="signin-scope" value="personal"> Personal</label></fieldset>`;
 if(s.state==='checking')return html`<p class="muted">Working…</p>`;
 if(s.state==='starting')return html`<p class="muted">${STARTING[s.provider]||'Working…'}</p>`;
 if(s.state==='code'&&GITHUB_DEVICE.test(s.url||''))return connectCodeHTML({code:s.code,url:s.url});
 if(s.state==='qr')return html`<p class="connect-q">On your phone, open WhatsApp, then Settings, Linked devices, Link a device, and scan this code:</p>${qrImg(s)}<p class="muted">WhatsApp changes the code every few seconds. This follows it.</p>`;
 if(s.state==='pair'&&s.code)return connectCodeHTML({kind:'pair',code:s.code});
 if(s.state==='phone')return phoneBody(s,back);
 if(s.state==='connecting'&&s.provider==='whatsapp')return html`<p class="signin-status" role="status"><i class="spin" aria-hidden="true"></i><span>${whatsappLinked(s)}</span></p>`;  // the sign-in dialog's spinner
 if(s.state==='stalled')return html`<p class="alert">${s.provider==='whatsapp'&&s.phase&&s.phase!=='code'?'Connecting WhatsApp is taking too long. Try again to pick up where it stopped.':'This is taking longer than it should. Try again.'}</p><div class="actions"><button type="button" class="primary" data-signin-go>Try again</button>${back}</div>`;
 if(s.state==='done'&&s.provider==='whatsapp'){const c=connectCard({account:s.made});return html`<p class="note sent-ok"><span>Connected.</span> <span>${c?'Its card shows your chat history coming in.':'Restarting to start reading it…'}</span></p><div class="actions">${c?html`<button type="button" class="primary" data-connect-card="${c.id}">Open its card</button>`:''}${back}</div>`}
 if(s.state==='connecting'||s.state==='code')return html`<p class="muted">Signed in. Connecting it now.</p>`;
 if(s.state==='done')return html`<p class="note sent-ok"><span>Connected.</span> <span>Restarting to start reading it…</span></p><div class="actions">${back}</div>`;
 if(s.state==='failed'||s.state==='stopped')return html`<p class="alert">${s.state==='stopped'?'That sign-in didn’t finish.':s.error||'Not connected.'}</p><div class="actions"><button type="button" class="primary" data-signin-go>Try again</button>${back}</div>${msAdmin(s)}`;
 if(s.provider==='whatsapp')return html`<p class="muted">${copy.about||''}</p>${scope}<div class="actions"><button type="button" class="primary" data-signin-go>Show the QR code</button>${back}</div><details class="connect-alt"><summary>On your phone? Link with a code instead</summary><label>Your WhatsApp number<br><input type="tel" name="signin-phone" maxlength="24" placeholder="+32 470 12 34 56" autocomplete="off"></label><div class="actions"><button type="button" data-signin-go data-way="code">Get a code</button></div></details>`;
 if(s.provider==='android')return html`<p class="muted">${copy.about||''}</p><ol class="fine"><li>Install OpenClaw from Google Play on your Android phone.</li><li>Press Show a setup code. In the app, add a Gateway and scan it.</li><li>Allow notification access when the app asks.</li><li>In the app’s settings, turn on Forward Notification Events, so notifications come in as they arrive.</li></ol><div class="actions"><button type="button" class="primary" data-signin-go>Show a setup code</button>${back}</div>`;
 const other=copy.other&&s.own&&connectList?.manage_url?html`<p class="fine"><a href="${safeHref(connectList.manage_url+HOSTED_TILE[s.provider])}" target="_blank" rel="noopener"><span>${copy.other}</span> ↗</a></p>`:'';
 return html`<p class="muted">${copy.about||''}</p>${signinLater(copy)}${scope}<div class="actions"><button type="button" class="primary" data-signin-go>Sign in with ${s.label}</button>${back}</div>${msAdmin(s)}${other}`}
const signinLater=copy=>copy.later?html`<p class="muted">${copy.later}</p>`:'';
function hostedSigninGo(s,way){const form=document.createElement('form'),box=$('#connect-add'),add=(name,value)=>{const i=document.createElement('input');i.type='hidden';i.name=name;i.value=value;form.append(i)};
 form.method='post';form.action='/_machine/connect';form.hidden=true;add('source',s.provider);
 if(!NO_SCOPE_SIGNIN.includes(s.provider)){add('scope',box.querySelector('input[name="signin-scope"]:checked')?.value||'work');add('boundary','')}
 if((s.provider==='intercom'||s.provider==='trello')&&s.another)add('another','1');
 if(['microsoft_docs','microsoft_docs_write','microsoft_teams'].includes(s.provider)&&s.email)add('email',s.email);  // Reconnect on its card: that address
 if(s.provider==='whatsapp'&&way==='code'){add('way','code');add('phone',box.querySelector('input[name="signin-phone"]')?.value||'')}
 if(s.provider==='whatsapp'&&s.account)add('account_id',s.account);  // Link again: the one that is not linked any more
 document.body.append(form);form.submit()}
// WhatsApp, linked (the control plane's phase, from the agent's cmd_whatsapp): the Machine connects it right away, after
// other setup work when some runs; the history comes in afterwards and its card counts it. Never a bare "connecting"
// for minutes (2026-11-06: a new owner saw "Signed in. Connecting it now." for almost 6 minutes).
function whatsappLinked(s){
 return s.phase==='queued'?t('Linked. Your Machine finishes another setup step first, then connects WhatsApp.'):t('Linked. Connecting WhatsApp to your Machine.')}
const HOSTED_GOING=['checking','starting','code','qr','pair','phone','connecting'];
// A sign-in that stops moving ends in a message with Try again, never an endless line: no answer from the control plane
// for HOSTED_SILENT_MS, or nothing new (state, step, code) for HOSTED_STILL_MS while connecting; a linked WhatsApp
// connects in about a minute, so HOSTED_LINKED_MS, unless it waits on other setup work. The control plane ends a stalled
// one itself too (cloud worker.expire_whatsapp) and tells ops; this is reported to the error feed as well.
const HOSTED_SILENT_MS=3*60000,HOSTED_STILL_MS=15*60000,HOSTED_LINKED_MS=5*60000;
function hostedStalled(s,now){const going=s.state==='connecting'||s.state==='starting'||s.state==='checking',still=now-(s.moved||s.began||now);
 if(now-(s.answered||s.began||now)>HOSTED_SILENT_MS)return true;
 if(s.provider==='whatsapp'&&s.state==='connecting')return s.phase!=='queued'&&still>HOSTED_LINKED_MS;
 return going&&still>HOSTED_STILL_MS}
function hostedPoll(){clearTimeout(signinTimer);const s=connectSignin;if(!s?.hosted||!HOSTED_GOING.includes(s.state)||!s.command)return;
 if(!s.began)s.began=Date.now();
 signinTimer=setTimeout(async()=>{let r=null;try{r=await request('/_machine/connect-state?s='+encodeURIComponent(s.provider)+'&c='+encodeURIComponent(s.command))}catch{}
  if(connectSignin!==s)return;const now=Date.now();
  if(r){const mark=JSON.stringify([r.state,r.phase,r.code,r.until,r.pending,r.phone]);
   connectSignin={...s,state:r.state,error:r.error,code:r.code,url:r.url,until:r.until,pending:r.pending,phone:r.phone,phase:r.phase,made:r.account,
    answered:now,mark,moved:mark===s.mark?s.moved||s.began:now}}
  if(HOSTED_GOING.includes(connectSignin.state)&&hostedStalled(connectSignin,now)){const at=connectSignin;connectSignin={...at,state:'stalled'};
   try{throw Object.assign(new Error(`${at.provider}: ${at.phase||at.state}`),{name:'ConnectStalled'})}catch(e){errReport(e,'ConnectStalled')}}
  $('#connect-add').dataset.sig='';renderConnectSignin();if(connectSignin.state==='done')setTimeout(()=>{connectList=null;refresh().then(()=>{$('#connect-add').dataset.sig='';if(connectSignin?.state==='done')renderConnectSignin()},()=>{})},8000);hostedPoll()},s.state==='checking'?0:2500)}
// Back from the provider (cloud: open_dashboard to=connect): + Add, that sign-in's form, following how it goes
// c_: the command its callback queued; f_: why the provider's answer was refused, which the account keeps for this form
const ON_DASHBOARD=['github','whatsapp','android','codex'];
async function openConnectLinkNow(){const m=/^#connect=(google|microsoft|microsoft_docs|microsoft_docs_write|microsoft_teams|google_meet|google_docs|zoom|stripe|slack|intercom|trello|github|whatsapp|android|codex|salesforce)(?:\/([cf]_[0-9a-f]{16}|stopped))?$/.exec(location.hash);if(!m||!state.manage_url)return;
 history.replaceState(null,'',location.pathname+location.search);connectRun=null;connectForm=null;showTab('health','add');await connectAdd(true);
 const docs=m[1]==='microsoft_docs_write'&&connectList?.sources.find(v=>v.hosted_signin==='microsoft_docs');  // Allow edits: the Docs source, its own consent
 const x=m[1]==='codex'?connectList?.codex&&codexSource():docs?{...docs,hosted_signin:m[1]}:connectList?.sources.find(v=>v.hosted_signin===m[1]);if(!x||!connectList.manage_url)return;const command=m[2]&&m[2]!=='stopped'?m[2]:'';
 connectSignin=signinOf(x,command.startsWith('f_')?'checking':command?ON_DASHBOARD.includes(m[1])?'starting':'connecting':m[2]?'stopped':'intro',command);$('#connect-add').dataset.sig='';renderConnectSignin();hostedPoll();viewTop($('#connect-add'))}
function renderConnectSignin(){const s=connectSignin,box=$('#connect-add'),paired=connectList?.paired;
 const back=html`<button type="button" data-connect-back>Back</button>`;let body;
 const copy=SIGNIN_COPY[s.provider]||{};
 if(s.provider==='codex')body=codexBody(s,back);  // Codex: its own code, on a hosted or a self-hosted Machine
 else if(s.hosted)body=hostedSigninBody(s,copy,back);  // a hosted Machine: its own form, never the pairing one
 else if(s.state==='started')body=html`<p>Sign in at ${s.label} in the tab that opened. This updates by itself.</p><div class="actions"><button type="button" data-signin-go>Start again</button>${back}</div>`;
 else if(s.state==='connecting')body=html`<p class="muted">Connecting…</p>`;
 else if(s.state==='done')body=html`<p class="note sent-ok">✓ Connected${s.name?' to '+s.name:''}.${s.replies?' Replies go as you, after you approve each one.':''} Restarting to start reading it…</p><div class="actions">${back}</div>`;
 else if(s.state==='failed'||s.state==='stopped')body=html`<p class="alert">${s.state==='stopped'?'That sign-in didn’t finish.':s.error||'Not connected.'}</p><div class="actions"><button type="button" class="primary" data-signin-go>Try again</button>${back}</div>${msAdmin(s)}`;
 // the control plane has no app for it (or refused to start it): no Sign in button, the other way open at once
 else if(s.off&&paired)body=html`<p class="muted">${copy.about||''}</p><p class="note signin-off">${t(s.own&&copy.other&&copy.off||'Sign in with {} isn’t available yet.',s.label)}</p>`;
 else body=html`<p class="muted">${copy.about||''}</p>${signinLater(copy)}${paired?html`<div class="actions"><button type="button" class="primary" data-signin-go>Sign in with ${s.label}</button>${back}</div>${msAdmin(s)}`
  :html`<p>${t(s.own&&copy.other?'Sign in with {} goes through your account on themachine.computer. Pair this Machine with it once, or use your own app below.':'Sign in with {} goes through your account on themachine.computer. Pair this Machine with it once.',s.label)}</p><div class="actions"><button type="button" class="primary" data-connect-pair>Pair this Machine</button>${back}</div>`}`;
 const off=!s.hosted&&s.off&&paired&&s.state==='intro';  // the other way is the way: open, its button first, Back after it
 // Not paired yet: pairing needs an account, so the other way shows open beside it, never folded away as the only way on
 const unpaired=!s.hosted&&!paired&&s.state==='intro';
 const paste=s.hosted||s.state==='done'||s.state==='connecting'||!s.own||!copy.other?'':html`<details class="connect-other"${off||unpaired?html` open`:''}><summary>${copy.other||''}</summary><p>${copy.how||''}</p><div class="actions"><button type="button"${off?html` class="primary"`:''} data-connect="${s.source}">${copy.go||''}</button>${off?back:''}</div></details>`;
 // adding one more next to an account already here, not signing one in again (a reconnect carries its email or account)
 const have=s.another&&s.state==='intro'&&!s.email&&!s.account?connectHaveNote(connectList?.sources.find(v=>v.name===s.source)):'';
 const panel=html`<div class="connect-run connect-signin"><h3>${copy.title||s.label}</h3>${have}${body}${paste}${off&&!paste?html`<div class="actions">${back}</div>`:''}</div>`;
 const sig=JSON.stringify(['signin',s.state,s.source,s.name,s.error,s.replies,paired,s.hosted,s.code,s.until,s.pending,s.phone,s.off,s.phase,!!connectCard({account:s.made}),s.provider==='codex'&&connectList?.codex?.status]);if(box.dataset.sig===sig)return;box.dataset.sig=sig;connectDraw(box,'signin',panel)}
function signinPoll(){clearTimeout(signinTimer);if(!connectSignin||!['started','connecting'].includes(connectSignin.state))return;
 signinTimer=setTimeout(async()=>{try{const r=await connectPost('connect_signin_state',{name:connectSignin.start||connectSignin.source});if(!connectSignin)return;
  if(r.state!=='none')connectSignin={...connectSignin,...r};renderConnectSignin();if(r.state==='done')setTimeout(()=>{connectList=null;refresh()},8000)}catch{}signinPoll()},2500)}
async function signinGo(way){const s=connectSignin;if(!s)return;
 if(s.provider==='codex'&&!s.hosted)return codexGo(s);
 if(s.hosted){if(s.state==='intro')return hostedSigninGo(s,way);connectSignin={...s,state:'intro',error:''};$('#connect-add').dataset.sig='';return renderConnectSignin()}  // Try again: Work or Personal first
 // The tab opens only once there is a start link: one the control plane refuses opens no tab, and the other way shows.
 // Still within the click's few seconds of user activation; a browser that blocks it goes there in this tab instead.
 try{const r=await connectPost('connect_signin',{name:s.start||s.source});
  if(r.state==='unavailable'){const x=connectList?.sources.find(v=>v.name===s.source);if(x)x.signin_off=true;connectSignin={...s,state:'intro',error:'',off:true}}
  else{const tab=window.open('about:blank','_blank');if(tab){tab.opener=null;tab.location.href=r.url}else location.assign(r.url);
   connectSignin={source:s.source,provider:s.provider,start:s.start,label:s.label,own:s.own,state:'started'}}}catch(err){errCaught(err);connectSignin={...s,state:'failed',error:err.message}}
 $('#connect-add').dataset.sig='';renderConnectSignin();signinPoll()}
// The phone's pairing request, shown while its setup code waits: Approve, a POST from this page to the account
async function phoneApprove(b){b.disabled=true;
 try{const r=await fetch('/_machine/connect-approve',{method:'POST',credentials:'same-origin',body:new URLSearchParams({kind:b.dataset.kind,request_id:b.dataset.phoneApprove})});if(!r.ok)throw new Error(t('That did not work. Try again.'))
  toast(t('Approved. Connecting your phone…'))}catch(err){errCaught(err);toast(err.message,true);b.disabled=false}}
// Reconnect on a hosted Machine's card or in Needs you: that provider's sign-in form under + Add, which comes back to it
document.addEventListener('click',async e=>{const b=e.target.closest('[data-hosted-reconnect]');if(!b||!state.manage_url)return;
 connectRun=null;connectForm=null;showTab('health','add');await connectAdd(true);const p=b.dataset.hostedReconnect,x=connectList?.sources.find(v=>v.hosted_signin===p);
 connectSignin={...(x?signinOf(x,'intro'):{source:p,provider:p,label:SIGNIN_COPY[p]?.label||p,own:false,hosted:true,state:'intro'}),...(b.dataset.email?{email:b.dataset.email}:{}),...(p==='whatsapp'&&b.dataset.account?{account:b.dataset.account}:{})};
 $('#connect-add').dataset.sig='';renderConnectSignin();viewTop($('#connect-add'))});
const hostedReconnect=(c,label,cls)=>html`<button type="button" class="${cls}" data-hosted-reconnect="${c.hosted_signin}"${c.email?html` data-email="${c.email}"`:''}${c.service==='whatsapp'?html` data-account="${c.id}"`:''}>${label}</button>`;
// Reconnect on a card or in Needs you: the same steps as + Add, for that account, shown in the + Add pane.
document.addEventListener('click',async e=>{const b=e.target.closest('[data-reconnect]');if(!b)return;
 // a sign-in through the control plane (Docs from Microsoft on a self-hosted Machine): its Sign in step, in the + Add pane.
 // data-signin-source, not data-signin: that one opens the Machine browser's sign-in dialog (connections-signin.js).
 // start: the sign-in it asks for, which may not be the source's own (Allow edits: microsoft_docs_write, not microsoft_docs)
 if(b.dataset.signinSource){const p=b.dataset.signinSource;connectRun=null;connectSignin={source:b.dataset.reconnect,provider:p,start:p,label:SIGNIN_COPY[p]?.label||p,own:false,state:'intro'};
  showHealthPane('add');document.querySelector('nav button[data-tab="health"]')?.click();$('#connect-add').dataset.sig='';await connectAdd(true);
  if(connectSignin?.source===b.dataset.reconnect&&connectList?.sources.find(v=>v.name===b.dataset.reconnect)?.signin_off){connectSignin={...connectSignin,off:true};renderConnectSignin()}
  viewTop($('#connect-add'));return}
 if(connectRun&&connectRun.state==='running'){showHealthPane('add');document.querySelector('nav button[data-tab="health"]')?.click();return}
 b.disabled=true;connectRun=null;if(await connectStart(b.dataset.reconnect,b.dataset.account)){showHealthPane('add');document.querySelector('nav button[data-tab="health"]')?.click();viewTop($('#connect-add'))}b.disabled=false});
document.addEventListener('click',async e=>{const b=e.target.closest('[data-disconnect]');if(!b||!confirm(`Disconnect ${b.dataset.name}? It stops syncing. What it already brought in stays.`))return;
 b.disabled=true;try{const r=await connectPost('connect_remove',{account:b.dataset.disconnect});if(r.restarting)restartSoon();toast(r.restarting?'Disconnected. Restarting…':'Disconnected. Restart the service to stop syncing it.');connectList=null;setTimeout(refresh,r.restarting?8000:500)}catch(err){errCaught(err);toast(err.message,true);b.disabled=false}});
function renderConnectRun(){const r=connectRun,box=$('#connect-add'),q=r.question;
 const head=html`<div class="connect-run"><h3>${r.state==='done'?'✓ ':''}${r.label||''}</h3><ul class="connect-lines">${(r.lines||[]).map(l=>html`<li>${linkify(l)}</li>`)}</ul>`;
 let body='';
 const code=r.state==='running'&&r.code?connectCodeHTML(r.code):'';
 if(r.state==='running'&&r.signin&&!q){const n=SIGNIN_SITES[r.signin]?.name||r.signin;body=html`<p class="connect-q">Sign in to ${n} on your Machine. This goes on by itself once you’re in.</p><div class="actions"><button type="button" class="primary" data-connect-site="${r.signin}">Sign in to ${n}</button></div>`;
  if(connectSiteShown!==r.session){connectSiteShown=r.session;setTimeout(()=>connectSiteSignin(r.signin),0)}}
 else if(code)body=code;
 else if(r.state==='running'&&q){const lead=q.kind==='choose'&&Number.isInteger(q.phone_first)&&(matchMedia('(max-width:560px)').matches||matchMedia('(pointer:coarse)').matches)?q.phone_first:-1,order=q.kind==='choose'?q.options.map((o,i)=>i).sort((a,b)=>(b===lead)-(a===lead)):[];
  const g=q.google&&/^https:\/\/accounts\.google\.com\//.test(q.google.url||'')?q.google:null;
  const field=g?html`<form class="connect-form connect-google" data-connect-form><ol class="connect-steps"><li><span>${t(g.again?'Sign in as {} and allow access again.':'Sign in as {} and allow read-only access.',g.email)}</span><a class="btn-link primary" href="${safeHref(g.url)}" target="_blank" rel="noopener">${t('Open Google')} ↗</a></li><li><label for="connect-answer">${t('Google then shows a page that may not load. Copy its whole address and paste it here.')}</label><input id="connect-answer" type="text" inputmode="url" autocomplete="off" spellcheck="false"></li></ol><div class="actions"><button>Continue</button></div></form>`
   :q.kind==='choose'?html`<div class="connect-choices">${order.map(i=>html`<button type="button"${i===lead?html` class="primary"`:''} data-connect-pick="${i}">${q.options[i]}</button>`)}</div>`:q.kind==='yes'?html`<div class="actions"><button type="button" class="primary" data-connect-pick="yes">Yes</button><button type="button" data-connect-pick="no">No</button></div>`:html`<form class="connect-form" data-connect-form><label for="connect-answer">${q.prompt}</label><input id="connect-answer" ${q.kind==='secret'?html`type="password" autocomplete="off"`:html`type="text"`} value="${q.kind==='secret'?'':q.default||''}" spellcheck="false"${q.resend?html` inputmode="numeric" autocomplete="one-time-code"`:''}><div class="actions"><button class="primary">Continue</button>${q.resend?html`<button type="button" data-connect-resend>${t('Send the code again')}</button>`:''}</div></form>`;
  body=html`${q.kind==='choose'||q.kind==='yes'?html`<p class="connect-q">${q.prompt}</p>`:''}${field}`}
 else if(r.state==='running')body=html`<p class="muted">Working…</p>`;
 else if(r.state==='done'){const c=connectCard(r),line=r.live?(c?'Reading it now. Its card shows how far it is.':'Starting to read it…'):!r.restarting?'Restart the service to start reading it.':c?'Running again. Its card shows how far it is.':r.follow==='slow'?'Taking longer than usual. Its card shows up here once it runs again.':'Restarting to start reading it…';
  const guess=r.guessed?html`<p class="fine connect-guess">${t('Set to {} from its address.',scopeLabel(r.guessed))}${c?html` <button type="button" class="link" data-connect-scope="${c.id}">${t('Change')}</button>`:''}</p>`:'';
  body=html`<p class="note sent-ok"><span>${r.who?t('Connected as {} in {}.',r.who.name,r.who.workspace):r.reconnect?'Signed in again.':'Connected.'}</span> <span>${line}</span></p>${guess}<div class="actions">${c?html`<button type="button" class="primary" data-connect-card="${c.id}">Open its card</button>`:''}<button type="button" data-connect-back>${r.reconnect?'Back':'Add another'}</button></div>`}
 else{const cmd=!state.manage_url&&/(?:^|: )((?:assistant|wacli|gog|gh|openclaw)\b[^;]*)/.exec(r.fix||'');body=html`<p class="alert">${r.error||'Stopped'}${r.fix?'. '+r.fix[0].toUpperCase()+r.fix.slice(1)+'.':''}</p>${cmd?html`<pre class="signin-command">${cmd[1].trim()}</pre><button type="button" class="browser-link" data-copy-command="${cmd[1].trim()}">Copy command</button> `:''}<div class="actions"><button type="button" data-connect="${r.source}"${r.reconnect?html` data-connect-account="${r.reconnect}"`:''}>Try again</button><button type="button" data-connect-back>Back</button></div>`}
 const panel=html`${head}${body}${r.state==='running'?html`<div class="actions"><button type="button" class="ghost" data-connect-stop>Cancel</button></div>`:''}</div>`;
 // A question being answered keeps what was typed: only redraw when something changed.
 const sig=JSON.stringify([r.state,r.lines,q&&q.id,r.error,r.follow,!!connectCard(r),r.signin,r.code]);if(box.dataset.sig===sig)return;box.dataset.sig=sig;connectDraw(box,'run',panel);box.querySelector('#connect-answer')?.focus()}
// After a source is added the running service reads it at once (live), or restarts to: wait until it answers with the new account,
// then move to that account's card, which shows how its first sync goes (the + Add pane says so until then).
const connectCard=r=>r?.account&&(state.connectors||[]).find(c=>c.id===r.account)||null;
function cardShow(id,flash){const c=(state.connectors||[]).find(x=>x.id===id);if(!c)return;showHealthPane(healthGroup(c.service));
 const el=[...document.querySelectorAll('#connectors>article')].find(a=>a.dataset.conn===id);if(!el)return;el.scrollIntoView({block:'center',behavior:'smooth'});
 if(flash){el.classList.add('conn-new');setTimeout(()=>el.classList.remove('conn-new'),4000)}}
// Change on a guessed Work or Personal: its card, with Details open on the choice
function scopeOpen(id){cardShow(id,false);const d=document.getElementById('sync-details-'+id);if(d)d.open=true;setTimeout(()=>document.querySelector(`select[data-scope="${CSS.escape(id)}"]`)?.focus(),300)}
async function connectFollow(run){const start=Date.now();await new Promise(r=>setTimeout(r,run.live?800:6000));
 while(connectRun===run&&Date.now()-start<180000){connectList=null;if(await refresh().catch(()=>false)!==false&&connectCard(run)){renderConnectRun();
   if(healthPane==='add'&&!$('#health').hidden){cardShow(run.account,true);if(run.guessed)scopeOpen(run.account)}return}
  if(Date.now()-start>60000&&run.follow!=='slow'){run.follow='slow';renderConnectRun()}await new Promise(r=>setTimeout(r,2500))}}
// Done, however it got there (a poll, or the last answer finishing it at once): follow the restart once
function connectPoll(){clearTimeout(connectTimer);if(connectRun?.state==='done'&&(connectRun.restarting||connectRun.live)&&!connectRun.followed){connectRun.followed=true;if(connectRun.restarting)restartSoon();connectFollow(connectRun);return}
 if(!connectRun||connectRun.state!=='running')return;connectTimer=setTimeout(async()=>{try{connectRun={...connectRun,...await connectPost('connect_poll',{session:connectRun.session})};renderConnectRun()}
 catch(e){errCaught(e);connectRun={...connectRun,state:'failed',error:e.message};renderConnectRun()}connectPoll()},connectRun.question?3000:1000)}
function connectCodeHTML(c){if(c.kind==='qr'&&Array.isArray(c.matrix))return html`<p class="connect-q">${t('In Telegram on your phone: Settings, Devices, Link Desktop Device. Then scan this code:')}</p>${qrSvg(c.matrix.filter(r=>/^[01]+$/.test(r)))}<p class="muted">${t('The code refreshes by itself.')}</p>`;
 const how=c.kind==='pair'?'In WhatsApp on your phone: Settings, Linked devices, Link a device, then Link with phone number instead. Enter this code:':c.kind==='openai'?'Enter this code at OpenAI to sign in:':'Enter this code at GitHub to sign in:';
 return html`<p class="connect-q">${how}</p><p class="connect-code" translate="no">${c.code}</p><div class="actions code-actions"><button type="button" data-copy-command="${c.code}">Copy code</button>${c.url?html`<a class="btn-link primary" href="${safeHref(c.url)}" target="_blank" rel="noopener">${c.kind==='openai'?'Open OpenAI ↗':'Open GitHub ↗'}</a>`:''}</div><p class="muted">This goes on by itself once you’re in.</p>`}
// LinkedIn or X, while its connect waits for the sign-in: that site's sign-in page opens in the Machine's browser and
// the sign-in dialog fills it from here; once in, the connect goes on by itself within seconds.
async function connectSiteSignin(site){try{await connectPost('connect_site_signin',{site})}catch(err){errCaught(err);toast(err.message,true);return}
 const after=()=>connectPoll();after.says='Signed in. Connecting it now.';openSignin(null,true,null,null,site,after)}
async function connectAnswer(value){const q=connectRun?.question;if(!q)return;try{connectRun={...connectRun,...await connectPost('connect_answer',{session:connectRun.session,question:q.id,value})}}catch(e){errCaught(e);toast(e.message,true)}renderConnectRun();connectPoll()}
$('#connect-add').addEventListener('click',async e=>{const t=e.target;
 if(t.closest('[data-codex-signin]')){connectSignin=signinOf(codexSource(),'intro');$('#connect-add').dataset.sig='';renderConnectSignin();return}
 const signin=t.closest('[data-connect-signin]');if(signin){const x=connectList.sources.find(v=>v.name===signin.dataset.connectSignin);connectSignin=signinOf(x,'intro');$('#connect-add').dataset.sig='';renderConnectSignin();return}
 if(t.closest('[data-signin-go]')){signinGo(t.closest('[data-signin-go]').dataset.way);return}
 if(t.closest('[data-connect-pair]')){aiPairGo(()=>{if(connectList)connectList.paired=true;$('#connect-add').dataset.sig='';if(connectSignin)renderConnectSignin()});return}  // one-click pairing (settings-ai.js, pairing.py)
 const approve=t.closest('[data-phone-approve]');if(approve){phoneApprove(approve);return}
 const start=t.closest('[data-connect]');if(start){connectSignin=null;clearTimeout(signinTimer);
  if(!start.dataset.connectAccount&&connectList?.sources.some(v=>v.name===start.dataset.connect&&v.form)){connectRun=null;connectForm=start.dataset.connect;$('#connect-add').dataset.sig='';renderConnectForm();return}
  start.disabled=true;if(!await connectStart(start.dataset.connect,start.dataset.connectAccount))start.disabled=false;return}
 const site=t.closest('[data-connect-site]');if(site){connectSiteSignin(site.dataset.connectSite);return}
 if(t.closest('[data-connect-resend]')){connectAnswer('again');return}
 const pick=t.closest('[data-connect-pick]');if(pick){const v=pick.dataset.connectPick;connectAnswer(v==='yes'?true:v==='no'?false:+v);return}
 if(t.closest('[data-connect-stop]')&&connectRun){const s=connectRun.session;connectRun=null;clearTimeout(connectTimer);$('#connect-add').dataset.sig='';if(connectList)renderConnectAdd();else connectDraw($('#connect-add'),'grid',html``);
  try{await connectPost('connect_cancel',{session:s})}catch{}connectAdd(true);return}
 const card=t.closest('[data-connect-card]');if(card){cardShow(card.dataset.connectCard,true);return}
 const guess=t.closest('[data-connect-scope]');if(guess){scopeOpen(guess.dataset.connectScope);return}
 if(t.closest('[data-connect-back]')){connectRun=null;connectSignin=null;connectForm=null;connectGbrain=null;clearTimeout(signinTimer);$('#connect-add').dataset.sig='';connectAdd(true)}});
$('#connect-add').addEventListener('submit',e=>{const setup=e.target.closest('[data-connect-setup]');if(setup){e.preventDefault();connectSetup(setup);return}
 if(!e.target.closest('[data-connect-form]'))return;e.preventDefault();connectAnswer($('#connect-answer').value)});
// An empty Company follows the address's domain (onboarding.company_of)
const WEBMAIL=/^(gmail|googlemail|outlook|hotmail|live|msn|yahoo|icloud|me|mac|aol|proton|protonmail|gmx|yandex|zoho|example)$/;
function companyOf(email){const p=String(email||'').split('@')[1]?.toLowerCase().split('.').slice(0,-1)||[];if(p.length>1&&/^(co|com|org|net|ac|gov)$/.test(p[p.length-1]))p.pop();
 const n=p[p.length-1]||'';return !n||WEBMAIL.test(n)?'':n[0].toUpperCase()+n.slice(1)}
$('#connect-add').addEventListener('input',e=>{const i=e.target;if(i.name==='company'){i.dataset.typed=i.value?'1':'';return}
 if(i.dataset.key!=='email')return;const co=i.closest('form')?.querySelector('input[name="company"]');if(co&&!co.dataset.typed)co.value=companyOf(i.value)});
$('#connect-add').addEventListener('change',e=>{if(e.target.name!=='scope')return;const form=e.target.closest('form'),co=form.querySelector('.connect-company'),personal=e.target.value==='personal';
 co.hidden=personal;co.querySelector('input').required=!personal});
// "Connect your own Intercom" on a to-do (also its "not synced" line and the first look's ending): Connections, + Add, at that source. A source that signs in here opens its
// sign-in intro (nothing starts before Continue); one set up on the account page or by questions is shown and focused.
async function connectOpenNow(name){connectPicking=true;try{showTab('health','add');await connectAdd(true)}finally{connectPicking=false}await connectAddSettled();const box=$('#connect-add');
 const item=box.querySelector(`[data-connect-signin="${CSS.escape(name)}"]`);if(item){item.click();viewTop(box);return}
 const x=connectList?.sources.find(v=>v.name===name),el=x&&[...box.querySelectorAll('.connect-source')].find(n=>n.dataset.connect===name||n.querySelector('b')?.textContent.replace(' ↗','')===x.label);
 viewTop(box);if(el){el.classList.add('picked');el.focus()}}
$('#health-tabs').onclick=e=>{const b=e.target.closest('[data-health-pane]');if(b)showHealthPane(b.dataset.healthPane)};
// The first Slack import reads the most active conversations first: the last day, then the week, quiet ones last.
function slackProgress(c){const f=c.first_import,later=f&&f.quiet;
if(!f)return t('{} of {} conversations collected',c.conversations_collected||0,c.conversations||0);
if(f.step==='triage')return t('Finding your most active conversations: {} of {} checked',f.done,f.total);
if(f.step==='recent')return t(later?'Collecting the last 24 hours first: {} of {} active conversations; quiet ones later':'Collecting the last 24 hours first: {} of {} active conversations',f.done,f.total);
if(f.step==='deepen')return t(later?'Now the rest of the week: {} of {} active conversations; quiet ones later':'Now the rest of the week: {} of {} active conversations',f.done,f.total);
return t('Quiet conversations last: {} of {}',f.done,f.total)}
// Signing in again and disconnecting: a hosted machine's account page for Google and Microsoft, else here.
// Docs (connectors/docs.py): its own consent, pressed on the account page (or Add again on a self-hosted Machine)
// What a Docs connection may write (doc_writes.py): a private new doc by itself, an edit only after the owner's OK; or Allow edits to ask for it
const docsWrites=c=>{const line=docsWritesLine(c);return line?html`<p class="muted conn-what conn-writes">${line}</p>`:''};
const docsWritesLine=c=>{if(c.actions===false)return '';const w=c.docs_writes||[],go=c.docs_write_signin&&!c.shared_by?(state.manage_url?hostedReconnect({...c,hosted_signin:c.docs_write_signin},'Allow edits','browser-link'):html`<button type="button" class="browser-link" data-reconnect="docs" data-account="${c.id}" data-signin-source="${c.docs_write_signin}">Allow edits</button>`):'';
 const line=w.includes('edit')?'Creates private docs. Edits docs only after you OK each change.':w.includes('create')?'Creates private docs only you can see until you share them.':go?'Can’t create or edit docs yet.':'';
 return line?html`${t(line)}${go?html` ${go}`:''}`:''};
const docsConnect=c=>c.service!=='docs'||!/docs_not_connected/.test(c.error||'')?'Reconnect':c.docs_provider==='microsoft'?'Connect Microsoft documents':'Connect Google Docs';
function reconnectButton(c,label='Reconnect'){return c.hosted_signin&&state.manage_url?hostedReconnect(c,label,'browser-link'):c.account_page?html`<a class="head-link" href="${safeHref(c.account_page)}" target="_blank" rel="noopener">${label} ↗</a>`:c.connect_name?html`<button type="button" class="browser-link" data-reconnect="${c.connect_name}" data-account="${c.id}"${c.signin?html` data-signin-source="${c.signin}"`:''}>${label}</button>`:''}
// Work (with its company) or Personal: the owner marks each sign-in. Leaving a Work Fleet removes that company's work
// accounts from this Machine (work_removal.py); personal ones stay.
// A company by how the Machine names it (work_or_personal.work_labels): plain Work when its name was only made from a domain
const scopeLabel=b=>{b=String(b||'');const named=/^work:./.test(b)&&Object.prototype.hasOwnProperty.call(state.work_labels||{},b)?String(state.work_labels[b]):'';
 return /^owner:/.test(b)?'':named?named.replace(/^Work(?= · |$)/,t('Work')): /^work:./.test(b)?t('Work')+' · '+b.slice(5):b==='personal:me'||b==='personal'?'Personal':/^personal:./.test(b)?t('Personal')+' · '+b.slice(9):b};
function scopeRow(c){const b=String(c.boundary||'');if(!b||/^owner:/.test(b)||c.service==='gateway')return '';
 const all=[...new Set([...(state.connectors||[]).map(x=>String(x.boundary||'')),b])],cur=b==='personal'?'personal:me':b;
 const opts=[...all.filter(x=>/^work:./.test(x)),...new Set(['personal:me',...all.filter(x=>/^personal:./.test(x))])].map(v=>[v,scopeLabel(v)]).concat([['','Work, another company…']]);
 return html`<p class="conn-scope"><label>Work or personal<select data-scope="${c.id}" data-was="${cur}">${opts.map(([v,l])=>html`<option value="${v}"${v===cur?html` selected`:''}>${l}</option>`)}</select></label>${c.boundary_by==='guess'?html` <small class="muted">Guessed. Pick one to be sure.</small>`:''}</p>`}
document.addEventListener('change',async e=>{const s=e.target.closest('select[data-scope]');if(!s)return;let b=s.value;
 if(!b){const name=(prompt('Company name')||'').trim();if(!name){s.value=s.dataset.was;return}b='work:'+name}
 s.disabled=true;try{const r=await connectPost('connect_scope',{account:s.dataset.scope,boundary:b});if(r.restarting)restartSoon();toast(r.restarting?'Saved. Restarting…':'Saved. Restart the service to use it.');setTimeout(refresh,r.restarting?8000:500)}catch(err){errCaught(err);toast(err.message,true);s.disabled=false;s.value=s.dataset.was}});
function connActions(c){const name=c.display_name||c.email||c.id;
 if(c.shared_by)return html`<p class="note">${t('Shared by {}. Its admins manage it.',c.shared_by)}</p>`;  // shared_connectors.py: no token, no Disconnect here
 if(c.hosted_signin&&state.manage_url)return html`<div class="actions conn-actions">${hostedReconnect(c,docsConnect(c),'ghost')}${c.account_page?html`<a class="btn-link" href="${safeHref(c.account_page)}" target="_blank" rel="noopener">Disconnect ↗</a>`:html`<button type="button" class="ghost danger" data-disconnect="${c.id}" data-name="${name}">Disconnect</button>`}</div>`;  // Disconnect: the account page when it holds the grant
 if(c.account_page)return html`<div class="actions conn-actions"><a class="btn-link" href="${safeHref(c.account_page)}" target="_blank" rel="noopener">Reconnect or disconnect ↗</a></div>`;
 return html`${c.shared_with?html`<p class="note">Shared with ${c.shared_with}.</p>`:''}${c.connect_name?html`<div class="actions conn-actions"><button type="button" class="ghost" data-reconnect="${c.connect_name}" data-account="${c.id}"${c.signin?html` data-signin-source="${c.signin}"`:''}>Reconnect</button><button type="button" class="ghost danger" data-disconnect="${c.id}" data-name="${name}">Disconnect</button></div>`:''}`}
// Salesflare (assistant.py salesflare_progress): what it reads, the round of accounts it is on, Stop or Start, Restart
// for a round that is stuck, and where its API keys are.
// No access to any account (no_access_all) says so with the way out (another key); the counts are one round's.
// Salesflare refusing the feed for the whole team (feed_off) says who can switch it on, instead of counting accounts.
function salesflareBox(c){const v=c.salesflare||{},r=v.round,id=c.id,n=x=>Number(x||0).toLocaleString(DL);
 const line=v.stopped?'Nothing new comes in until you start it.':r?[t('Checked {} of {} accounts so far.',n(r.done),n(r.accounts)),r.stuck?t('Started {}, may be stuck.',ago(r.started)):''].filter(Boolean).join(' '):c.last_success?'':'Finding the accounts with recent emails and meetings…';
 const aside=[v.slow_accounts?t('{} skipped as too slow',n(v.slow_accounts)):'',v.no_access&&!v.no_access_all&&!v.feed_off?t('{} without access',n(v.no_access)):''].filter(Boolean).join(' · ');
 const locked=v.stopped?'':v.feed_off?html`<p class="alert sf-feed-off">${t('Salesflare hasn’t switched on feed access for API keys for your team, so no emails or meetings come in. Salesflare support can switch it on.')}</p>`
  :v.no_access_all?html`<p class="alert sf-locked">${t('Salesflare doesn’t let this API key open these accounts. Use the key of a user who can see them.')}</p>`:'';
 const btn=(act,label)=>html`<button type="button" class="head-link" data-sf-sync="${act}" data-account="${id}">${label}</button>`;
 return html`${locked}${line?html`<p class="note sf-line${r?.stuck&&!v.stopped?' sf-stuck':''}">${line}</p>`:''}${aside?html`<p class="muted sf-aside">${aside}</p>`:''}${
  c.shared_by?'':html`<div class="sf-actions">${v.stopped?btn('start',t('Start (a button)')):btn('stop','Stop')}${btn('restart','Restart sync')}${v.keys_url?html`<a class="head-link" href="${safeHref(v.keys_url)}" target="_blank" rel="noopener">API keys ↗</a>`:''}</div>`}`}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-sf-sync]');if(!b)return;const act=b.dataset.sfSync;
 if(act==='restart'&&!confirm('Restart the Salesflare sync? It drops the round it is on and reads the last week again. Nothing it brought in is lost.'))return;
 b.disabled=true;try{await connectPost('connector_sync',{account:b.dataset.account,do:act});toast(act==='stop'?'Stopped. Nothing new comes in until you start it.':act==='start'?'Started. It reads again in a moment.':'Restarted. It reads the last week again now.');await refresh()}catch(err){errCaught(err);toast(err.message,true)}finally{b.disabled=false}});
// Salesforce, Update contact details (connectors/salesforce.py card, crm_sync.py): off until the owner turns it on, and
// only after they saw what it would change (Show what would change, then Turn on). On, it lists the last contacts it updated.
const sfPreview={};
function crmChanges(items){return html`<ul class="crm-sync-list">${items.map(i=>html`<li><b>${i.name}</b>${i.changes.map(x=>html`<span class="crm-sync-change"><span>${x.label}</span>: ${x.new}${x.old?html` <small class="muted">${t('(was {})',x.old)}</small>`:''}</span>`)}</li>`)}</ul>`}
function crmSyncBox(c){const v=c.crm_sync||{},id=c.id,p=sfPreview[id];if(c.shared_by||v.can_write===false)return'';
 const btn=(act,label,cls='head-link')=>html`<button type="button" class="${cls}" data-crm-sync="${act}" data-account="${id}">${label}</button>`;
 if(v.contact_sync)return html`<div class="crm-sync"><p class="note crm-sync-line">Updates contact details in Salesforce.</p>${(v.contact_updates||[]).length?crmChanges(v.contact_updates):''}${v.contact_failed?html`<details class="crm-sync-refused"><summary class="muted crm-sync-aside">${t(['{} contact not updated: Salesforce refused the change','{} contacts not updated: Salesforce refused the change'],v.contact_failed)}</summary>${(v.contact_refused||[]).length?html`<ul class="crm-sync-list">${v.contact_refused.map(r=>html`<li><b>${r.name}</b><span class="muted">${r.why}</span></li>`)}</ul>`:''}</details>`:''}<div class="sf-actions">${btn('off','Turn off')}</div></div>`;
 if(p)return html`<div class="crm-sync"><p class="note crm-sync-line">${p.length?t(['Turning it on now changes {} contact:','Turning it on now changes {} contacts:'],p.length):'Nothing to change right now. It checks again every few hours.'}</p>${p.length?crmChanges(p):''}<div class="sf-actions">${btn('on','Turn on','primary')}${btn('cancel','Not now')}</div></div>`;
 return html`<div class="crm-sync"><p class="muted crm-sync-line">Update contact details: off. It can keep job titles, phone numbers and LinkedIn links current in Salesforce.</p><div class="sf-actions">${btn('preview','Show what would change')}</div></div>`}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-crm-sync]');if(!b)return;const act=b.dataset.crmSync,id=b.dataset.account;
 if(act==='cancel'){delete sfPreview[id];await refresh();return}
 b.disabled=true;try{const r=await connectPost('connector_contact_sync',{account:id,do:act});
  if(act==='preview')sfPreview[id]=r.changes||[];else delete sfPreview[id];
  if(act!=='preview')toast(act==='on'?'On. It updates these contacts in a moment.':'Off. It no longer changes Salesforce.');await refresh()}catch(err){errCaught(err);toast(err.message,true)}finally{b.disabled=false}});
// Details: where a source's sync is, in words (its saved checkpoint, assistant.py commit_page), never the raw state.
function syncPlain(c){let st={};try{st=JSON.parse(c.state||'{}')||{}}catch{}const out=[];
 if(!c.last_success&&!c.state)return ['Waiting for the first sync. It starts within a few minutes.'];
 if(st.resync_reason||st.mode==='resync')out.push('Reading the last days again to fill a gap.');
 else if(st.mode==='bootstrap')out.push('First read: catching up on the last days.');
 else if(c.last_success&&!c.salesflare?.round&&!c.salesflare?.no_access_all&&!c.salesflare?.feed_off&&!syncFlaky(c))out.push('Caught up. Checks for new items every few minutes.');
 const until=c.salesflare?.synced_until||(/^\d{4}-\d\d-\d\dT/.test(st.watermark||'')?st.watermark:'');if(until)out.push(t('Read up to {}',date(until)));
 if(c.service==='slack'&&c.conversations)out.push(t('{} of {} conversations read at least once',c.conversations_collected||0,c.conversations));
 return out}
// Telegram chats: what it reads, and why it stopped with the way back (log in again, or the owner's own app ID)
function telegramNote(c){const stop=c.error==='telegram_app_blocked'?t('Telegram stopped accepting this Machine’s app ID. Nothing is read or sent. Reconnect with your own app ID from my.telegram.org.')
 :c.error==='telegram_logged_out'?t('Telegram logged this Machine out. Reconnect to keep reading.'):'';
 return stop?html`<p class="alert">${stop} ${reconnectButton(c)}</p>`:''}
// Under Connected, on every card: what it brings in (c.what, the line + Add shows for it) and what it can do, each only
// after the owner's OK (c.acts, assistant.py connector_says). Docs says its own, with Allow edits; who Intercom replies
// as is under Details. One or two short lines, so the cards line up.
const CONN_ACTS={send:'Sends email only after you press Send.',reply:'Replies only after you press Send.',calendar:'Changes events only after you OK them.'};
// With one ability off (abilities.py) it says only what the other does: an action-only one nothing it brings in.
// Teams: what it can't read yet, and why, in one short line (connectors/teams.py missing_by_scope and meeting_events)
function teamsMissing(m){const meet=m.transcripts==='admin'||m.notes==='admin',lines=[];
 if(m.channels==='admin'||meet)lines.push(m.channels==='admin'&&meet?'Channels and meeting notes need your admin’s OK.':meet?'Meeting notes need your admin’s OK.':'Channels need your admin’s OK.');
 if(m.notes==='license')lines.push('Copilot notes need a Copilot license.');
 if(m.transcripts==='blocked')lines.push('Your organization turned off transcripts.');
 return lines}
function connWhat(c){const span=s=>s?html`<span>${t(s)}</span>`:'',signals=c.signals!==false,acts=c.actions!==false;
 if(c.service==='docs'){const narrow=c.docs_linked_only,line=!signals?'Finds and reads docs for your to-dos.':!acts?(narrow?'Opens only docs linked in your mail and the docs it makes.':'Reads comments, mentions, suggestions and shares.'):null;
  if(!signals){const w=docsWritesLine(c);return html`<p class="muted conn-what">${span(line)}${w?html` <span>${w}</span>`:''}</p>`}
  return html`<p class="muted conn-what">${line?span(line):c.docs_provider==='microsoft'?html`${span(c.what)} ${span('Replies stay drafts for you to post in Word.')}`:span(narrow?'Opens only docs linked in your mail and the docs it makes.':'Google Docs. Reads comments, mentions, suggestions and shares. Posts a reply only when you OK it.')}</p>${docsWrites(c)}`}
 if(c.service==='teams'){const lines=teamsMissing(c.teams_missing||{});return html`<p class="muted conn-what">${span(c.what)}${lines.map(l=>html` ${span(l)}`)}</p>`}
 const what=signals?span(c.what):'',act=span(CONN_ACTS[c.acts]);
 return what||act?html`<p class="muted conn-what">${what}${what&&act?' ':''}${act}</p>`:''}
// Brings in signals and Can do things, a switch each under Details, on a connection that has both (assistant.py
// connect_abilities). A chat's replies answer what it brings in, so there only Can do things has one.
// The one left on can't be turned off here: with both off it would do nothing, which is Disconnect.
const ABILITY_LABEL={signals:'Brings in signals',actions:'Can do things'};
function connAbilities(c){const keys=c.ability_switches||[];if(!keys.length||c.shared_by)return '';
 return html`<div class="conn-abilities">${keys.map(k=>{const on=c[k]!==false,last=on&&c[k==='signals'?'actions':'signals']===false;
  return html`<label class="conn-ability"><span>${t(ABILITY_LABEL[k])}</span><button type="button" class="lookup-switch" role="switch" aria-checked="${on}" aria-label="${t(ABILITY_LABEL[k])}" data-ability="${k}" data-account="${c.id}"${last?html` disabled title="${t('Keep one on. To stop it, disconnect it.')}"`:''}></button></label>`})}</div>`}
document.addEventListener('click',async e=>{const b=e.target.closest('button[data-ability]');if(!b||b.disabled)return;
 const c=(state.connectors||[]).find(x=>x.id===b.dataset.account);if(!c)return;
 const next={signals:c.signals!==false,actions:c.actions!==false};next[b.dataset.ability]=b.getAttribute('aria-checked')!=='true';
 b.disabled=true;b.setAttribute('aria-checked',String(next[b.dataset.ability]));
 try{const r=await connectPost('connect_abilities',{account:c.id,...next});Object.assign(c,{signals:r.signals,actions:r.actions});if(r.restarting)restartSoon();toast(r.restarting?'Saved. Restarting…':'Saved. Restart the service to use it.');setTimeout(refresh,r.restarting?8000:500)}
 catch(err){errCaught(err);toast(err.message,true);b.setAttribute('aria-checked',String(!next[b.dataset.ability]));b.disabled=false}});
// The card's three tiles. A calendar counts events: how many it keeps, how many come up in the next 7 days and how many
// were new or changed in the last 24h (as the note above the cards says; its review runs in the background, so no
// "not checked" there)
// A CRM counts the accounts it could open (this round, else the last one) and the emails and meetings it brought in.
const connFigures=(c,unit)=>CALENDAR_SERVICES.includes(c.service)?[[c.total,'events'],[c.upcoming_7d,'next 7 days'],[c.signals_24h,'last 24h']]
 :c.service==='salesflare'?[[c.salesflare?.round?.read??c.salesflare?.last_round?.read,'accounts read'],[c.total,'emails and meetings'],[c.signals_24h,'last 24h']]
 :[[c.total,unit],[c.signals_24h,'last 24h'],[c.pending,'not checked']];
const CALENDAR_SERVICES=['calendar','outlook_calendar'];
// Recent syncs, newest first, in the dashboard's own time style (Today 08:18, the year only when it isn't this one).
// A failed sync that a later one made up for reads calm, without its old Retry time; only a failure that is still
// the latest one shows as an error with when it retries.
const syncRows=list=>{list=list||[];const fixed=list.findIndex(a=>a.status==='success');
 return list.map((a,i)=>{const at=html`<time datetime="${a.at||''}" class="muted">${humanTime(a.at)}</time>`;
  if(a.status==='success')return html`<p>${at} · <span>${a.signals==null?t('Synced'):t('Synced, {} new or changed',a.signals)}</span></p>`;
  if(fixed>=0&&fixed<i)return html`<p>${at} · <span class="muted">${syncError(a.error)}</span></p>`;
  return html`<p>${at} · <span class="error">${syncError(a.error)}</span>${a.retry_at?html` · <span>${t('Retry {}',humanTime(a.retry_at))}</span>`:''}</p>`})};
// How far back its history reaches (older messages kept to search and read, never as to-dos: docs/help/history.md).
// One history line on a card: while WhatsApp's first chat history still counts in (c.history), only that one.
const connBackfill=c=>{const b=c.backfill;if(!b?.back_to||c.service==='whatsapp'&&c.history)return '';const [y,m]=b.back_to.split('-').map(Number),when=localeDate(new Date(y,m-1,1),DL,{month:'long',year:'numeric'});
 return html`<p class="note">${b.done?t('History: back to {}.',when):t('History coming in: back to {} so far.',when)}</p>`};
// Under the name: the kind of source and Work or personal. The Machine's own health (owner:system) has neither to say.
function connSubtitle(c){const kind=c.service==='docs'&&c.docs_provider==='google'?'Google Docs':service(c.service),parts=[kind===(c.display_name||c.email)?'':kind,scopeLabel(c.boundary)].filter(Boolean);
 return parts.length?html`<small>${parts.join(' · ')}</small>`:''}
// A connected source's card shows the same logo as its row in + Add (connectLogo, dashboard/logos): the catalog's name for
// its service (Salesflare is crm there, Google Docs is docs signed in with Google). A catch-all (Other email) keeps its line icon.
const LOGO_NAME={salesflare:'crm'},connLogo=c=>connectLogo({service:c.service},c.service==='docs'&&c.docs_provider==='google'?'google_docs':LOGO_NAME[c.service]||c.service);
function connectorCard(c,open){
const unit={calendar:'events',outlook_calendar:'events',intercom:'conversations',android:'notifications',gateway:'alerts',github:'notifications',stripe:'events',rss:'items',docs:'items',google_meet:'meetings',trello:'card changes',salesforce:'updates'}[c.service]||'messages',tone=connectorTone(c),phone=c.service==='android'?JSON.parse(c.state||'{}'):{},synced=c.signals!==false;
return html`<article data-group="${healthGroup(c.service)}" data-conn="${c.id}"><div class="conn-head">${connLogo(c)}<div><h3>${c.display_name||c.email}</h3>${connSubtitle(c)}</div><span class="state-dot t-${tone}" title="${connectorHealth(c).text}"></span></div>
<p class="connection-status">${connectorHealth(c).text}</p>
${connWhat(c)}
${synced?html`<div class="figures">${connFigures(c,unit).map(([n,label])=>html`<div><b>${(n||0).toLocaleString(DL)}</b><span>${t(label)}</span></div>`)}</div>
${spark(c)}<div class="conn-foot">${c.silent_since?'':html`<small>${c.last_success?htmlT('Last sync {}',time(c.last_success,true)):t('Not synced yet')}</small>`}${c.last_sync_signals==null?'':html`<small title="${t('New or changed messages and events, without duplicates. Last 24h counts when they came in here, not when they were sent.')}">${t('{} in last sync',c.last_sync_signals)}</small>`}</div>`:''}
${c.service==='salesflare'?salesflareBox(c):''}${c.service==='salesforce'?crmSyncBox(c):''}${c.signed_out?html`<p class="alert">Signed out of ${service(c.service)}. ${c.sign_in_url?html`<a class="head-link" href="${safeHref(c.sign_in_url)}" target="_blank" rel="noopener">Sign in again</a>`:c.sign_in_hint?c.sign_in_hint[0].toUpperCase()+c.sign_in_hint.slice(1)+'.':'Sign in again in the browser it reads with.'} <button type="button" class="browser-link" data-signin="${c.id}">Sign in here</button></p>`:c.sign_in_command?html`<p class="alert">${syncError(c.error)}. ${reconnectButton(c)||'Run the command below in a terminal on this computer.'}</p><details class="signin-fallback"${reconnectButton(c)?'':html` open`}><summary>Or use a terminal</summary><pre class="signin-command">${c.sign_in_command}</pre><button type="button" class="browser-link" data-copy-command="${c.sign_in_command}">Copy command</button> <small>It syncs again within a minute after.</small></details>`:c.error&&!connectorHealth(c).resting?html`<p class="alert">${c.error==='android_offline'?'':['slack:HTTP_429','slack_ratelimited'].includes(c.error)?'Slack is taking a short pause. ':syncError(c.error)+'. '}${c.silent_since?t('Nothing new since {}.',date(c.silent_since))+' ':''}${c.error==='android_offline'?'Open the OpenClaw app on the phone.':connectorTone(c)==='orange'?(reconnectButton(c,docsConnect(c))||'Please reconnect this account.'):c.retry_at?t('Next try {}.',ago(c.retry_at)):'Retrying automatically.'}</p>`:''}

${c.service==='slack'?html`<p class="note">${slackProgress(c)}${c.conversation_errors?` · ${t('{} unavailable',c.conversation_errors)}`:''}${c.deferred_threads?` · ${t(['{} thread read waiting for retry','{} thread reads waiting for retry'],c.deferred_threads)}`:''}</p><p class="note">Slack’s limits mean a full round of conversations can take hours.</p>`:''}
${c.service==='android'?html`<p class="note">${phone.transport==='direct_fallback'?'Using direct checks while the notification bridge is unavailable.':'Uses OpenClaw’s notification feed, plus a catch-up check of your phone.'} Checks run at most every 10 minutes, so notifications cleared in between may be missed.${phone.reconciliation_error&&phone.reconciliation_error!==c.error?html`<br><span class="error">Last phone check: ${syncError(phone.reconciliation_error)}</span>`:''}</p>`:''}
${c.service==='whatsapp'&&c.history?html`<p class="note">${t('Bringing in your chat history: {} messages so far.',Number(c.history).toLocaleString(DL))}</p>`:''}
${connBackfill(c)}
${c.service==='telegram'?telegramNote(c):''}
<div class="conn-more">${synced?html`<details id="sync-recent-${c.id}" ${open.has('sync-recent-'+c.id)?html`open`:''}><summary>Recent syncs</summary>${syncRows(c.sync_activity)}${(c.sync_activity||[]).length?'':html`<p>No recent syncs recorded yet.</p>`}</details>`:''}<details id="sync-details-${c.id}" ${open.has('sync-details-'+c.id)?html`open`:''}><summary>Details</summary>${!synced?'':c.failures_24h?html`<p>${t(['{} failed sync in the last 24 hours.','{} failed syncs in the last 24 hours.'],c.failures_24h)}${c.error?'':' '+t('The last sync worked.')}</p>`:html`<p>No failed syncs in the last 24 hours.</p>`}${synced&&c.last_failure?html`<p>${t('Last failure: {}, {}',syncError(c.last_failure.error),humanTime(c.last_failure.at))}</p>`:''}${synced&&c.error&&c.failures?html`<p>${t(['{} failed attempt in a row','{} failed attempts in a row'],c.failures)}</p>`:''}${synced?syncPlain(c).map(l=>html`<p class="conn-plain">${l}</p>`):''}${c.service==='intercom'&&c.replies_as&&c.replies_as!=='you'?html`<p class="conn-plain conn-replies-as">${t('Replies as {}, only after you press Send.',c.replies_as)}</p>`:''}${connAbilities(c)}${photosRow(c)}${scopeRow(c)}${connActions(c)}</details></div></article>`;
}
// The connection cards (a refresh keeps the opened ones open) and the disconnected ones
function drawConnectors(){const expandedSync=new Set([...document.querySelectorAll('#connectors details[open]')].map(d=>d.id));
 setHTML($('#connectors'),html`${[...state.connectors].sort((a,b)=>(a.service==='gateway')-(b.service==='gateway')||!!a.last-!!b.last).map(c=>connectorCard(c,expandedSync))}`);renderDisconnected()}
// Served as a part that loads when first needed (dashboard_parts.LAZY): a page drawn before it came draws Connections
// now (render skipped it; it can't call render, which counts the part in only once this file has run). Inline (the
// tests, the demo) this part runs before shell-render.js, which draws it itself.
if(self.LAZY_FILES?.connections&&drawnWhole)try{drawConnectors();renderHealthTabs()}catch(e){errCaught(e);console.error(e)}
