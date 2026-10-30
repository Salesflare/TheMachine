// A source with read hours (X, LinkedIn: read_window from the server) rests outside them: it says when it reads again,
// not that it's stale (a busy browser left from its last read waits quietly too), and once its hours open its staleness
// counts from the opening, not from last night's read.
function connectorHealth(c){
const w=c.read_window,again=w?.reads_again_at&&Date.parse(w.reads_again_at)>Date.now()?w.reads_again_at:null,
 resting={tone:'mint',text:again&&t('Reads again at {}',fmtHM(again)),resting:true};
if(c.salesflare?.stopped)return {tone:'muted',text:'Stopped'};
if(c.error==='docs_not_connected')return {tone:'orange',text:'Waiting for your OK to read docs'};
if(c.error&&/_signed_out$/.test(c.error))return {tone:'orange',text:'Signed out of '+service(c.service)};
if(TELEGRAM_STOP[c.error])return {tone:'orange',text:TELEGRAM_STOP[c.error]};
if(c.error){const help=/(auth|unauthor|forbidden|permission|invalid_grant|signin_expired|HTTP_40[13])/.test(c.error);return help?{tone:'orange',text:'Needs your help'}:c.last_success&&again?resting:{tone:'amber',text:'Reconnecting automatically'}}
if(!c.last_success)return {tone:'muted',text:'Waiting for first sync'};
if(again)return resting;
const since=Math.max(Date.parse(c.last_success),Date.parse(w?.reads_again_at||w?.opened_at||'')||0);
if(Date.now()-since>Math.max(900000,(c.poll_seconds||300)*3000))return {tone:'amber',text:'Waiting for a fresh sync'};
if(c.service==='slack'&&(c.conversation_errors||c.deferred_threads))return {tone:'amber',text:'Connected · some conversations waiting'};
return {tone:'mint',text:'Connected'}
}
function connectorTone(c){return connectorHealth(c).tone}
// Disconnected lately (mail_grants.py receipts): a sign-in counts as removed only once Google confirmed the revoke
// (Microsoft and Zoom: once no copy is left here); until then it says why, and The Machine keeps trying.
const SIGNIN_NAME={google:'Google',microsoft:'Microsoft',zoom:'Zoom'};
function renderDisconnected(){const list=state.disconnected||[];$('#disconnected').innerHTML=list.length?`<div class="section-head"><h2>Disconnected lately</h2></div><div class="list disconnected-list">${list.map(r=>{const ok=r.state==='removed';return `<article style="--c:var(--${ok?'mint':'amber'})"><h3>${esc(r.email)}</h3><div class="row">${chip(ok?'Removed, confirmed':`Pending: ${SIGNIN_NAME[r.provider]||'The provider'} hasn’t confirmed. Retrying`,ok?'mint':'amber')}<small>${esc(SIGNIN_NAME[r.provider]||r.provider)}</small>${time(r.at)}</div></article>`}).join('')}</div>`:''}
function spark(c){const a=[...(c.sync_activity||[])].reverse();if(!a.length)return '';const max=Math.max(1,...a.map(x=>x.signals||0));return `<div class="spark" role="img" aria-label="${esc((f=>a.length===1?t('Last sync: {} failed',f):t('Last {} syncs: {} failed',a.length,f))(a.filter(x=>x.status!=='success').length))}">${a.map(x=>x.status!=='success'?`<i class="fail" style="height:100%" title="${esc(date(x.at))} · ${esc(syncError(x.error))}"></i>`:`<i class="${x.signals?'':'zero'}" style="height:${x.signals?Math.max(18,Math.round(x.signals/max*100)):10}%" title="${esc(date(x.at))} · ${esc(t(['{} signal','{} signals'],x.signals??0))}"></i>`).join('')}</div>`}
// Connections' sub-tabs: the sources by kind, then saved sign-ins and the reviews. A tab with a source that needs
// the owner's help (orange) shows how many (amber ones retry or catch up by themselves); the first such tab opens
// unless one was picked. Like every tab row, a number means something needs you: Sign-ins has none (a saved sign-in never needs anything), Who's who and Friends only when waiting.
const HEALTH_GROUPS={gmail:'mail',calendar:'mail',outlook:'mail',outlook_calendar:'mail',slack:'chat',whatsapp:'chat',telegram:'chat',signal:'chat',discord:'chat',teams:'chat'};  // Android sits in Other sources: most phones (iPhones) have no notification feed to give
const healthGroup=s=>HEALTH_GROUPS[s]||'other';
let healthPane=(localStorage.getItem('health-pane')||'').replace(/^phone$/,'other'),healthPicked=false,savedLoginCount=0;
function renderHealthTabs(){const cs=state.connectors||[],bad=g=>cs.filter(c=>healthGroup(c.service)===g&&connectorTone(c)==='orange').length;
 const panes=[['mail','Mail and calendar'],['chat','Chat'],['other','Other sources']].filter(([g])=>cs.some(c=>healthGroup(c.service)===g)).map(([id,label])=>({id,label,badge:bad(id),warn:true}));
 if(!panes.length)panes.push({id:'mail',label:'Sources'});
 panes.push({id:'add',label:'+ Add'});
 if(savedLoginCount||healthPicked&&healthPane==='signins')panes.push({id:'signins',label:'Sign-ins'});panes.push({id:'reviews',label:'Reviews'});
 const ids=panes.map(p=>p.id),current=healthPicked&&ids.includes(healthPane)?healthPane:panes.find(p=>p.badge&&p.warn)?.id||(ids.includes(healthPane)?healthPane:ids[0]);
 healthPane=current;const row=$('#health-tabs');row.innerHTML=subTabs('Connections','data-health-pane',panes,current);
 for(const el of document.querySelectorAll('#health [data-health-for]'))el.hidden=!el.dataset.healthFor.split(' ').includes(current);
 for(const a of document.querySelectorAll('#connectors>article'))a.hidden=a.dataset.group!==current;tabsShow(row.firstChild);if(current==='add')connectAdd()}  // measured once the other panes are hidden, never with every source shown at once
// Connections, Add: every source this install can add, set up right here with the same steps as `assistant connect`;
// its questions show one at a time. On a hosted machine Google, Microsoft, Zoom, Stripe, Intercom and Trello sign in right
// here too (hosted_signin): a POST to /_machine/connect starts the account's own sign-in for it, and the provider comes
// back to this page (#connect=<provider>/<command>), where the form follows the connecting. Others with a tile on the
// account page (GitHub, WhatsApp) link to it. On a self-hosted
// one such a source signs in through The Machine's own app (fleet.py connect_start), once this Machine is paired with
// an account, and its row follows how that goes; pasting a key stays, folded away, where the service has one (Intercom and
// Trello sign in only).
let connectList=null,connectListAt=0,connectRun=null,connectTimer=0,connectSignin=null,signinTimer=0,connectForm=null,connectSiteShown=null,connectGbrain=null;
const BROKER_LINK={gmail:'#google',calendar:'#google',outlook:'#microsoft',outlook_calendar:'#microsoft',zoom:'#source-zoom',stripe:'#source-stripe',slack:'#source-slack'};
const connectPost=(action,args={})=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
async function connectAdd(force){if(connectRun)return;if(!force&&connectList&&Date.now()-connectListAt<60000)return;connectListAt=Date.now();
 try{connectList=await connectPost('connect_sources')}catch(e){errCaught(e);$('#connect-add').innerHTML=`<p class="error">${esc(e.message)}</p>`;return}renderConnectAdd()}
// + Add shows one view at a time in its box: the grid of sources, or one source's sign-in, form, run or GBrain panel.
// Another view than before starts at its top, under the top bar, with focus on it (its first field, else its heading):
// from far down the grid the page would otherwise stay down there, the short view above it and only the footer showing.
// Back to the grid returns to where it was, on the tile it left from (connectGrid, noted on the tap).
let connectGrid=null;
function connectDraw(box,kind,html,focus){const was=box.dataset.view;box.innerHTML=html;box.dataset.view=kind;if(was===kind)return;
 if(kind==='grid'){const g=connectGrid;connectGrid=null;if(!g||!was)return;const tile=[...box.querySelectorAll('.connect-source')].find(n=>placeSig(n)===g.sig);
  scrollTo(scrollX,g.y);tile?.focus({preventScroll:true});placeNote();return}
 viewTop(box,focus&&box.querySelector(focus))}
$('#connect-add').addEventListener('click',e=>{const tile=e.target.closest('.connect-sources>button.connect-source');if(tile)connectGrid={y:scrollY,sig:placeSig(tile)}},true);
function renderConnectAdd(){const box=$('#connect-add');if(connectRun)return renderConnectRun();if(connectSignin)return renderConnectSignin();if(connectForm)return renderConnectForm();if(connectGbrain)return renderGbrain();if(!connectList)return;
 const items=connectList.sources.map(x=>{const more=x.connected?`<small class="count">${x.connected} connected</small>`:'',what=x.what?`<small>${esc(x.what)}</small>`:'';
  if(x.hosted_signin&&connectList.manage_url)return `<button type="button" class="connect-source" data-connect-signin="${esc(x.name)}"><b>${esc(x.label)}</b>${what}${more}</button>`;
  if(x.account_page&&connectList.manage_url)return `<a class="connect-source" href="${esc(connectList.manage_url+'#'+x.account_page)}" target="_blank" rel="noopener"><b>${esc(x.label)} ↗</b>${what}${more}</a>`;
  if(x.signin&&!connectList.manage_url)return `<button type="button" class="connect-source" data-connect-signin="${esc(x.name)}"><b>${esc(x.label)}</b>${what}${more}</button>`;
  return x.broker?(connectList.manage_url?`<a class="connect-source" href="${esc(connectList.manage_url+(BROKER_LINK[x.service]||'#sources'))}" target="_blank" rel="noopener"><b>${esc(x.label)} ↗</b>${what}${more}</a>`:''):`<button type="button" class="connect-source" data-connect="${esc(x.name)}"><b>${esc(x.label)}</b>${what}${more}</button>`}).join('');
 connectDraw(box,'grid',`<p class="sub-note">Pick a source to connect.${connectList.saveable||connectList.manage_url?'':' This service can’t save its settings: use <code>assistant connect</code> in a terminal.'}</p><div class="connect-sources">${items}${codexTile()}${gbrainTile()}</div>`)}
// Codex (codex_signin.py): its own tile. It signs in with Codex's own device code, shown here: a hosted Machine's control
// plane runs that sign-in on its server (POST /_machine/connect, like GitHub), a self-hosted Machine runs it itself.
const CODEX_DEVICE=/^https:\/\/auth\.openai\.com\/codex\/device[\w/.-]*$/;
const codexSource=()=>({name:'codex',service:'codex',label:'Codex',broker:true,connected:connectList?.codex?.status==='connected'?1:0,...(connectList?.manage_url?{hosted_signin:'codex'}:{signin:'codex'})});
const codexTile=()=>{const c=connectList?.codex;if(!c)return '';
 const now=c.status==='connected'?'<small class="count">Connected</small>':c.status==='signed_out'?'<small class="count">Signed out</small>':'';
 return `<button type="button" class="connect-source" data-codex-signin><b>Codex</b><small>Coding to-dos on your ChatGPT plan</small>${now}</button>`};
const CODEX_TIP='<details class="connect-alt"><summary>OpenAI turns the code down?</summary><p>Turn on device code sign-in for Codex in ChatGPT security settings, at the bottom. Then try again.</p><p><a class="browser-link" href="https://chatgpt.com/settings/security" target="_blank" rel="noopener">Open ChatGPT security settings ↗</a></p></details>';
function codexBody(s,back){const c=connectList?.codex||{},again=`<div class="actions"><button type="button" class="primary" data-signin-go>Try again</button>${back}</div>`;
 if(s.state==='checking'||s.state==='starting')return '<p class="muted">Getting a sign-in code from OpenAI…</p>';
 if(s.state==='code'&&CODEX_DEVICE.test(s.url||''))return connectCodeHTML({kind:'openai',code:s.code,url:s.url})+CODEX_TIP;
 if(s.state==='connecting'||s.state==='code')return '<p class="muted">Signed in. Connecting it now.</p>';
 if(s.state==='done')return `<p class="note sent-ok"><span>Connected.</span> <span>Hand a coding to-do to Codex to use it.</span></p><div class="actions">${back}</div>`;
 if(s.state==='missing')return '<p>Codex isn’t on this computer yet. Install it in a terminal, then try again.</p><pre class="signin-command">npm install -g @openai/codex</pre><p class="gbrain-links"><button type="button" class="browser-link" data-copy-command="npm install -g @openai/codex">Copy command</button></p>'+again;
 if(s.state==='failed'||s.state==='stopped')return `<p class="alert">${esc(s.state==='stopped'?'That sign-in didn’t finish.':s.error||'Not connected.')}</p>${again}${CODEX_TIP}`;
 if(c.status==='connected')return `<p class="note sent-ok">Codex is signed in. Hand a coding to-do to Codex to use it.</p><div class="actions">${back}</div>`;
 return `<p class="muted">Hand coding to-dos to Codex, on your ChatGPT plan. OpenAI gives you a code to sign in with.</p><div class="actions"><button type="button" class="primary" data-signin-go>Get a code</button>${back}</div>`}
// Self-hosted: this Machine runs Codex's sign-in (codex_signin) and the form follows it
async function codexGo(s){connectSignin={...s,state:'starting',error:''};$('#connect-add').dataset.sig='';renderConnectSignin();
 try{const r=await connectPost('codex_signin');if(connectSignin?.provider==='codex')connectSignin={...connectSignin,...r}}catch(err){errCaught(err);connectSignin={...connectSignin,state:'failed',error:err.message}}
 $('#connect-add').dataset.sig='';renderConnectSignin();codexPoll()}
function codexPoll(){clearTimeout(signinTimer);const s=connectSignin;if(s?.provider!=='codex'||s.hosted||!['starting','code'].includes(s.state))return;
 signinTimer=setTimeout(async()=>{try{const r=await connectPost('codex_signin_state');if(connectSignin!==s)return;connectSignin={...s,...r};$('#connect-add').dataset.sig='';renderConnectSignin();
  if(r.state==='done'){connectList=null;connectAdd(true)}}catch{}codexPoll()},2000)}
// GBrain: an optional add-on, only on a Machine that runs on its owner's computer. Off until the owner agrees to what
// goes in; the panel shows how to install it, that consent step, or how the sync goes (and turns it off again).
const gbrainTile=()=>connectList?.gbrain?`<button type="button" class="connect-source" data-gbrain><b>GBrain</b><small>A memory app for AI tools, on this computer</small>${connectList.gbrain.on?'<small class="count">On</small>':''}</button>`:'';
async function gbrainOpen(){connectGbrain={loading:true};$('#connect-add').dataset.sig='';renderGbrain();
 try{connectGbrain=await connectPost('gbrain_status')}catch(e){errCaught(e);connectGbrain={error:e.message}}renderGbrain()}
function renderGbrain(){const g=connectGbrain,box=$('#connect-add'),back='<button type="button" data-connect-back>Back</button>';let body;
 if(g.loading)body='<p class="muted">Checking for GBrain…</p>';
 else if(g.error&&!('on' in g))body=`<p class="alert">${esc(g.error)}</p><div class="actions"><button type="button" data-gbrain-check>Check again</button>${back}</div>`;
 else if(g.on){const pages=g.kept?t('{} pages, {} kept as you edited them',g.pages,g.kept):t(['{} page','{} pages'],g.pages);
  body=`<p class="sent-ok">Connected</p><dl class="gbrain-facts"><dt>Brain</dt><dd><code>${esc(g.brain||'')}</code></dd>${g.version?`<dt>Version</dt><dd>${esc(g.version)}</dd>`:''}<dt>Pages</dt><dd>${esc(pages)}</dd><dt>Last sync</dt><dd>${esc(ago(g.last_sync))}</dd>${g.last_error?`<dt>Problem</dt><dd class="error">${esc(g.last_error)}</dd>`:''}</dl>
  <label class="gbrain-check"><input type="checkbox" data-gbrain-work${g.work?' checked':''}${g.saveable?'':' disabled'}><span>Include Work people and companies</span></label>
  <p class="fine muted">Turning off keeps your brain and its pages.</p><div class="actions"><button type="button" data-gbrain-off${g.saveable?'':' disabled'}>Turn off</button>${back}</div>`}
 else if(!g.installed)body=`<p>GBrain isn’t on this computer yet. Install it in a terminal, then check again.</p><pre class="signin-command">bun install -g github:garrytan/gbrain</pre><p class="gbrain-links"><button type="button" class="browser-link" data-copy-command="bun install -g github:garrytan/gbrain">Copy command</button><a class="browser-link" href="https://github.com/garrytan/gbrain" target="_blank" rel="noopener">About GBrain ↗</a></p><div class="actions"><button type="button" data-gbrain-check>Check again</button>${back}</div>`;
 else body=`${g.version?`<p class="muted">${esc(t('Found {} at {}',g.version,g.brain||''))}</p>`:''}<p>What goes into GBrain:</p><ul class="gbrain-list"><li>People and projects from your Graph, with a link back</li><li>What The Machine learned about how you work</li></ul><p>Message text never goes in.</p><p><b>GBrain may send this to its own AI providers.</b></p>
  <label class="gbrain-check"><input type="checkbox" data-gbrain-work-pick><span>Include Work people and companies</span></label><label class="gbrain-check"><input type="checkbox" data-gbrain-consent><span>I agree</span></label>
  ${g.saveable?'':'<p class="fine muted">Change this in config.json (gbrain) on this computer.</p>'}<p class="error" role="status">${esc(g.error||'')}</p><div class="actions"><button type="button" class="primary" data-gbrain-on disabled>Connect GBrain</button>${back}</div>`;
 const html=`<div class="connect-run gbrain-panel"><h3>GBrain</h3>${g.loading||g.on?'':'<p class="muted">Optional, for developers. Keep your own AI memory app in sync with The Machine.</p><p class="muted">Reviews can read your brain to write better to-dos.</p>'}${body}</div>`,sig=JSON.stringify(['gbrain',g]);if(box.dataset.sig===sig)return;box.dataset.sig=sig;connectDraw(box,'gbrain',html)}
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
 const asks=(f.ask||[]).map(([k,q])=>`<label>${esc(q)}<input name="ask" data-key="${esc(k)}" type="text" required spellcheck="false" autocomplete="off"></label>`).join('');
 const secret=f.secret?`<label>${esc(f.secret)}<input name="secret" type="password" required autocomplete="off" spellcheck="false"></label>`:'';
 const scope=f.scope?`<fieldset class="connect-scope"><legend>Work or personal?</legend><label><input type="radio" name="scope" value="work"${f.personal?'':' checked'}> Work</label><label><input type="radio" name="scope" value="personal"${f.personal?' checked':''}> Personal</label></fieldset><label class="connect-company"${f.personal?' hidden':''}>Company<input name="company" maxlength="60" value="${esc(f.company||'')}" placeholder="Acme" autocomplete="organization"${f.personal?'':' required'}></label>`:'';
 connectDraw(box,'form',`<div class="connect-run"><h3>${esc(x.label)}</h3>${x.what||f.learn?`<p class="muted">${esc(x.what||'')}${f.learn?` <a class="learn" href="https://themachine.computer/help/${encodeURIComponent(f.learn)}" target="_blank" rel="noopener">${esc(t('Learn more'))}</a>`:''}</p>`:''}${f.note?`<p class="fine connect-note">${linkify(f.note)}</p>`:''}<form class="connect-form connect-setup" data-connect-setup="${esc(x.name)}" novalidate>${asks}${secret}${scope}<p class="error" role="status"></p><div class="actions"><button class="primary">Connect</button><button type="button" data-connect-back>Back</button></div></form></div>`,'input:not([type="radio"]):not([hidden])')}
async function connectSetup(form){const name=form.dataset.connectSetup,err=form.querySelector('.error'),go=form.querySelector('button.primary');
 const missing=[...form.querySelectorAll('input[required]')].find(i=>!i.closest('[hidden]')&&!i.value.trim());if(missing){{const what=(missing.closest('label')?.firstChild?.textContent||'').trim();err.textContent=what?t('Fill in {}.',what):t('Fill this in.')}missing.focus();return}
 const answers={};for(const i of form.querySelectorAll('input[name="ask"]'))answers[i.dataset.key]=i.value.trim();
 const scope=form.querySelector('input[name="scope"]:checked')?.value,payload={form:true,answers,secret:form.querySelector('input[name="secret"]')?.value||'',...(scope?{scope,company:scope==='work'&&form.querySelector('input[name="company"]')?.value.trim()||''}:{})};
 err.textContent='';go.disabled=true;if(!await connectStart(name,null,payload))go.disabled=false}
// Sign in with <provider> on a self-hosted Machine: the Machine asks the control plane for a one-time start link,
// signed with its own key, and it opens in a new tab. The token comes back sealed for this Machine, which checks it.
// off: what it says when the control plane has no app for this sign-in (connect_sources signin_off), above the other way
const SIGNIN_COPY={intercom:{label:'Intercom',about:'Reads your conversations. Replies only after you approve them, as yourself. Never assigns or closes.'},
 trello:{label:'Trello',about:'Reads cards, comments and activity on one board you pick next. Never changes anything in Trello.'},
 google:{label:'Google',about:'Gmail and Google Calendar. Sends only emails you approved.',other:'Use your own app',how:'Your own Google Cloud app, step by step.',go:'Set it up',off:'Sign in with {} isn’t available yet. Use your own app instead.'},
 microsoft:{label:'Microsoft',about:'Outlook mail and calendar. Sends only emails you approved.',other:'Use your own app',how:'Your own Microsoft app registration, step by step.',go:'Set it up',off:'Sign in with {} isn’t available yet. Use your own app instead.'},
 github:{label:'GitHub',about:'Review requests, mentions, assignments and failed CI runs. Reads only.'},
 zoom:{label:'Zoom',about:'Your meeting summaries and transcripts. Reads only.',other:'Use your own app',how:'Your own Zoom app, step by step.',go:'Set it up',off:'Sign in with {} isn’t available yet. Use your own app instead.'},
 microsoft_docs:{label:'Microsoft',title:'Microsoft Word',about:'Word, OneDrive and SharePoint, for an Outlook address you connected. Reads only.'},
 microsoft_docs_write:{label:'Microsoft',title:'Microsoft Word',about:'Lets The Machine create and edit your Word documents. Each change waits for your OK.'},
 google_meet:{label:'Google',title:'Google Meet',about:'Transcripts and Gemini notes of your meetings. Reads only.'},
 whatsapp:{label:'WhatsApp',about:'Your WhatsApp chats, as a linked device. Replies only when you press Send on a to-do.'},
 android:{about:'The notifications on your Android phone, through the OpenClaw app.'},
 stripe:{label:'Stripe',about:'Failed payments, disputes, cancellations and new subscriptions. Reads only, never changes anything in Stripe.',other:'Or paste a restricted key',how:'A restricted key with Read on Events, Customers and Account.',go:'Paste a key',off:'Sign in with {} isn’t available yet. Paste a restricted key instead.'},
 slack:{label:'Slack',about:'Your DMs and the channels you’re in. Sends only messages you approved, as yourself.',other:'Or use a Maton API key',how:'Connect Slack in Maton, then paste your Maton API key.',go:'Use Maton',off:'Sign in with {} isn’t available yet. Use a Maton API key instead.'}};
// A work organization that lets only approved apps in: the short link its Microsoft 365 admin approves The Machine with.
// It opens Microsoft's approval page with a fresh signed state on each visit (the control plane's site), so it never expires.
const MS_ADMIN_LINK='https://themachine.computer/m365-admin-consent';
const msAdmin=s=>s.provider!=='microsoft'?'':`<div class="connect-admin"><p>Need your admin’s approval? Send them this link.</p><div class="connect-admin-link"><a href="${MS_ADMIN_LINK}" target="_blank" rel="noopener" translate="no">${MS_ADMIN_LINK.replace('https://','')}</a><button type="button" data-copy-link="${MS_ADMIN_LINK}">Copy link</button></div></div>`;
const signinOf=(x,state,command)=>{const hosted=!!(connectList?.manage_url&&x.hosted_signin),p=hosted?x.hosted_signin:x.signin===true?x.service:x.signin;
 return {source:x.name,provider:p,label:SIGNIN_COPY[p]?.label||x.label,own:!x.broker,hosted,another:!!x.connected,state,...(command?{command}:{}),...(!hosted&&x.signin_off?{off:true}:{})}};
// A hosted Machine: Work or Personal here, then Sign in goes to the provider in this tab and comes back to this form.
// Pasting a key or token stays on the account page's tile.
const HOSTED_TILE={google:'#google',microsoft:'#microsoft',zoom:'#source-zoom',stripe:'#source-stripe',slack:'#source-slack',intercom:'#source-intercom',trello:'#source-trello',github:'#source-github'};
// GitHub, WhatsApp and the phone have no provider page to come back from: the Machine gets a code, shown right here
// (GitHub's to type at GitHub, WhatsApp's QR code or pairing code, the OpenClaw app's setup code)
const GITHUB_DEVICE=/^https:\/\/github\.com\/login\/device[\w/.-]*$/;
const NO_SCOPE_SIGNIN=['intercom','android','microsoft_docs','microsoft_docs_write','codex'];
const STARTING={github:'Getting a sign-in code from GitHub…',whatsapp:'Getting a code from WhatsApp…',android:'Making a setup code…'};
const qrImg=s=>`<img class="connect-qr" src="/_machine/connect-qr?s=${encodeURIComponent(s.provider)}&amp;c=${encodeURIComponent(s.command)}&amp;v=${encodeURIComponent(String(s.until||''))}" alt="QR code">`;
function phoneBody(s,back){let html='';
 if(s.code)html+=`<p class="connect-q">In the OpenClaw app on your phone, add a Gateway and scan this code, or copy it and paste it there:</p>${qrImg(s)}<div class="actions"><button type="button" data-copy-command="${esc(s.code)}">Copy code</button></div><p class="muted">It works for 10 minutes, once.</p>`;
 for(const q of s.pending||[])html+=`<div class="connect-wait"><p>${esc(t('{} asks to pair with your Machine. Is that your phone? Approve only this one.',q.name||t('A phone')))}</p><button type="button" class="primary" data-phone-approve="${esc(q.id)}" data-kind="${esc(q.kind)}">Approve</button></div>`;
 const p=s.phone;if(p)html+=`<p class="note">${esc(!p.connected?t('{} is paired but not connected. Open the OpenClaw app on it.',p.name):!p.notifications?t('{} is connected. Now allow notification access for OpenClaw on the phone.',p.name):t('{} is connected. Adding its notifications…',p.name))}</p>`;
 if(!html)html='<p class="muted">Making a setup code…</p>';
 return html+`<p class="muted">Waiting for your phone. This updates by itself.</p><div class="actions">${back}</div>`}
function hostedSigninBody(s,copy,back){const scope=NO_SCOPE_SIGNIN.includes(s.provider)?'':'<fieldset class="connect-scope"><legend>Work or personal?</legend><label><input type="radio" name="signin-scope" value="work" checked> Work</label><label><input type="radio" name="signin-scope" value="personal"> Personal</label></fieldset>';
 if(s.state==='checking')return '<p class="muted">Working…</p>';
 if(s.state==='starting')return `<p class="muted">${esc(STARTING[s.provider]||'Working…')}</p>`;
 if(s.state==='code'&&GITHUB_DEVICE.test(s.url||''))return connectCodeHTML({code:s.code,url:s.url});
 if(s.state==='qr')return `<p class="connect-q">On your phone, open WhatsApp, then Settings, Linked devices, Link a device, and scan this code:</p>${qrImg(s)}<p class="muted">WhatsApp changes the code every few seconds. This follows it.</p>`;
 if(s.state==='pair'&&s.code)return connectCodeHTML({kind:'pair',code:s.code});
 if(s.state==='phone')return phoneBody(s,back);
 if(s.state==='connecting'||s.state==='code')return '<p class="muted">Signed in. Connecting it now.</p>';
 if(s.state==='done')return `<p class="note sent-ok"><span>Connected.</span> <span>Restarting to start reading it…</span></p><div class="actions">${back}</div>`;
 if(s.state==='failed'||s.state==='stopped')return `<p class="alert">${esc(s.state==='stopped'?'That sign-in didn’t finish.':s.error||'Not connected.')}</p><div class="actions"><button type="button" class="primary" data-signin-go>Try again</button>${back}</div>${msAdmin(s)}`;
 if(s.provider==='whatsapp')return `<p class="muted">${esc(copy.about||'')}</p>${scope}<div class="actions"><button type="button" class="primary" data-signin-go>Show the QR code</button>${back}</div><details class="connect-alt"><summary>On your phone? Link with a code instead</summary><label>Your WhatsApp number<br><input type="tel" name="signin-phone" maxlength="24" placeholder="+32 470 12 34 56" autocomplete="off"></label><div class="actions"><button type="button" data-signin-go data-way="code">Get a code</button></div></details>`;
 if(s.provider==='android')return `<p class="muted">${esc(copy.about||'')}</p><ol class="fine"><li>Install OpenClaw from Google Play on your Android phone.</li><li>Press Show a setup code. In the app, add a Gateway and scan it.</li><li>Allow notification access when the app asks.</li></ol><div class="actions"><button type="button" class="primary" data-signin-go>Show a setup code</button>${back}</div>`;
 const other=copy.other&&s.own&&connectList?.manage_url?`<p class="fine"><a href="${esc(connectList.manage_url+HOSTED_TILE[s.provider])}" target="_blank" rel="noopener"><span>${esc(copy.other)}</span> ↗</a></p>`:'';
 return `<p class="muted">${esc(copy.about||'')}</p>${scope}<div class="actions"><button type="button" class="primary" data-signin-go>Sign in with ${esc(s.label)}</button>${back}</div>${msAdmin(s)}${other}`}
function hostedSigninGo(s,way){const form=document.createElement('form'),box=$('#connect-add'),add=(name,value)=>{const i=document.createElement('input');i.type='hidden';i.name=name;i.value=value;form.append(i)};
 form.method='post';form.action='/_machine/connect';form.hidden=true;add('source',s.provider);
 if(!NO_SCOPE_SIGNIN.includes(s.provider)){add('scope',box.querySelector('input[name="signin-scope"]:checked')?.value||'work');add('boundary','')}
 if((s.provider==='intercom'||s.provider==='trello')&&s.another)add('another','1');
 if(['microsoft_docs','microsoft_docs_write'].includes(s.provider)&&s.email)add('email',s.email);  // Reconnect on its card: that address
 if(s.provider==='whatsapp'&&way==='code'){add('way','code');add('phone',box.querySelector('input[name="signin-phone"]')?.value||'')}
 if(s.provider==='whatsapp'&&s.account)add('account_id',s.account);  // Link again: the one that is not linked any more
 document.body.append(form);form.submit()}
const HOSTED_GOING=['checking','starting','code','qr','pair','phone','connecting'];
function hostedPoll(){clearTimeout(signinTimer);const s=connectSignin;if(!s?.hosted||!HOSTED_GOING.includes(s.state)||!s.command)return;
 signinTimer=setTimeout(async()=>{try{const r=await request('/_machine/connect-state?s='+encodeURIComponent(s.provider)+'&c='+encodeURIComponent(s.command));if(connectSignin!==s)return;
  connectSignin={...s,state:r.state,error:r.error,code:r.code,url:r.url,until:r.until,pending:r.pending,phone:r.phone};$('#connect-add').dataset.sig='';renderConnectSignin();if(r.state==='done')setTimeout(()=>{connectList=null;refresh()},8000)}catch{}hostedPoll()},s.state==='checking'?0:2500)}
// Back from the provider (cloud: open_dashboard to=connect): + Add, that sign-in's form, following how it goes
// c_: the command its callback queued; f_: why the provider's answer was refused, which the account keeps for this form
const ON_DASHBOARD=['github','whatsapp','android','codex'];
async function openConnectLink(){const m=/^#connect=(google|microsoft|microsoft_docs|microsoft_docs_write|google_meet|zoom|stripe|intercom|trello|github|whatsapp|android|codex)(?:\/([cf]_[0-9a-f]{16}|stopped))?$/.exec(location.hash);if(!m||!state.manage_url)return;
 history.replaceState(null,'',location.pathname+location.search);connectRun=null;connectForm=null;showTab('health','add');await connectAdd(true);
 const docs=m[1]==='microsoft_docs_write'&&connectList?.sources.find(v=>v.hosted_signin==='microsoft_docs');  // Allow edits: the Docs source, its own consent
 const x=m[1]==='codex'?connectList?.codex&&codexSource():docs?{...docs,hosted_signin:m[1]}:connectList?.sources.find(v=>v.hosted_signin===m[1]);if(!x||!connectList.manage_url)return;const command=m[2]&&m[2]!=='stopped'?m[2]:'';
 connectSignin=signinOf(x,command.startsWith('f_')?'checking':command?ON_DASHBOARD.includes(m[1])?'starting':'connecting':m[2]?'stopped':'intro',command);$('#connect-add').dataset.sig='';renderConnectSignin();hostedPoll();viewTop($('#connect-add'))}
function renderConnectSignin(){const s=connectSignin,box=$('#connect-add'),paired=connectList?.paired;
 const back='<button type="button" data-connect-back>Back</button>';let body;
 const copy=SIGNIN_COPY[s.provider]||{};
 if(s.provider==='codex')body=codexBody(s,back);  // Codex: its own code, on a hosted or a self-hosted Machine
 else if(s.hosted)body=hostedSigninBody(s,copy,back);  // a hosted Machine: its own form, never the pairing one
 else if(s.state==='started')body=`<p>Sign in at ${esc(s.label)} in the tab that opened. This updates by itself.</p><div class="actions"><button type="button" data-signin-go>Start again</button>${back}</div>`;
 else if(s.state==='connecting')body='<p class="muted">Connecting…</p>';
 else if(s.state==='done')body=`<p class="note sent-ok">✓ Connected${s.name?' to '+esc(s.name):''}.${s.replies?' Replies go as you, after you approve each one.':''} Restarting to start reading it…</p><div class="actions">${back}</div>`;
 else if(s.state==='failed'||s.state==='stopped')body=`<p class="alert">${esc(s.state==='stopped'?'That sign-in didn’t finish.':s.error||'Not connected.')}</p><div class="actions"><button type="button" class="primary" data-signin-go>Try again</button>${back}</div>${msAdmin(s)}`;
 // the control plane has no app for it (or refused to start it): no Sign in button, the other way open at once
 else if(s.off&&paired)body=`<p class="muted">${esc(copy.about||'')}</p><p class="note signin-off">${esc(t(s.own&&copy.other&&copy.off||'Sign in with {} isn’t available yet.',s.label))}</p>`;
 else body=`<p class="muted">${esc(copy.about||'')}</p>`+(paired?`<div class="actions"><button type="button" class="primary" data-signin-go>Sign in with ${esc(s.label)}</button>${back}</div>${msAdmin(s)}`
  :`<p>To sign in here, pair this Machine with your account first.</p><div class="actions"><a class="btn-link primary" href="${esc(connectList.pair_url)}" target="_blank" rel="noopener">Pair this Machine first ↗</a>${back}</div>`);
 const off=!s.hosted&&s.off&&paired&&s.state==='intro';  // the other way is the way: open, its button first, Back after it
 const paste=s.hosted||s.state==='done'||s.state==='connecting'||!s.own||!copy.other?'':`<details class="connect-other"${off?' open':''}><summary>${esc(copy.other||'')}</summary><p>${esc(copy.how||'')}</p><div class="actions"><button type="button"${off?' class="primary"':''} data-connect="${esc(s.source)}">${esc(copy.go||'')}</button>${off?back:''}</div></details>`;
 const html=`<div class="connect-run connect-signin"><h3>${esc(copy.title||s.label)}</h3>${body}${paste}${off&&!paste?`<div class="actions">${back}</div>`:''}</div>`;
 const sig=JSON.stringify(['signin',s.state,s.source,s.name,s.error,s.replies,paired,s.hosted,s.code,s.until,s.pending,s.phone,s.off,s.provider==='codex'&&connectList?.codex?.status]);if(box.dataset.sig===sig)return;box.dataset.sig=sig;connectDraw(box,'signin',html)}
function signinPoll(){clearTimeout(signinTimer);if(!connectSignin||!['started','connecting'].includes(connectSignin.state))return;
 signinTimer=setTimeout(async()=>{try{const r=await connectPost('connect_signin_state',{name:connectSignin.source});if(!connectSignin)return;
  if(r.state!=='none')connectSignin={...connectSignin,...r};renderConnectSignin();if(r.state==='done')setTimeout(()=>{connectList=null;refresh()},8000)}catch{}signinPoll()},2500)}
async function signinGo(way){const s=connectSignin;if(!s)return;
 if(s.provider==='codex'&&!s.hosted)return codexGo(s);
 if(s.hosted){if(s.state==='intro')return hostedSigninGo(s,way);connectSignin={...s,state:'intro',error:''};$('#connect-add').dataset.sig='';return renderConnectSignin()}  // Try again: Work or Personal first
 // The tab opens only once there is a start link: one the control plane refuses opens no tab, and the other way shows.
 // Still within the click's few seconds of user activation; a browser that blocks it goes there in this tab instead.
 try{const r=await connectPost('connect_signin',{name:s.source});
  if(r.state==='unavailable'){const x=connectList?.sources.find(v=>v.name===s.source);if(x)x.signin_off=true;connectSignin={...s,state:'intro',error:'',off:true}}
  else{const tab=window.open('about:blank','_blank');if(tab){tab.opener=null;tab.location.href=r.url}else location.assign(r.url);
   connectSignin={source:s.source,provider:s.provider,label:s.label,own:s.own,state:'started'}}}catch(err){errCaught(err);connectSignin={...s,state:'failed',error:err.message}}
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
const hostedReconnect=(c,label,cls)=>`<button type="button" class="${cls}" data-hosted-reconnect="${esc(c.hosted_signin)}"${c.email?` data-email="${esc(c.email)}"`:''}${c.service==='whatsapp'?` data-account="${esc(c.id)}"`:''}>${esc(label)}</button>`;
// Reconnect on a card or in Needs you: the same steps as + Add, for that account, shown in the + Add pane.
document.addEventListener('click',async e=>{const b=e.target.closest('[data-reconnect]');if(!b)return;
 // a sign-in through the control plane (Docs from Microsoft on a self-hosted Machine): its Sign in step, in the + Add pane
 if(b.dataset.signin){const p=b.dataset.signin;connectRun=null;connectSignin={source:b.dataset.reconnect,provider:p,label:SIGNIN_COPY[p]?.label||p,own:false,state:'intro'};
  showHealthPane('add');document.querySelector('nav button[data-tab="health"]')?.click();$('#connect-add').dataset.sig='';await connectAdd(true);
  if(connectSignin?.source===b.dataset.reconnect&&connectList?.sources.find(v=>v.name===b.dataset.reconnect)?.signin_off){connectSignin={...connectSignin,off:true};renderConnectSignin()}
  viewTop($('#connect-add'));return}
 if(connectRun&&connectRun.state==='running'){showHealthPane('add');document.querySelector('nav button[data-tab="health"]')?.click();return}
 b.disabled=true;connectRun=null;if(await connectStart(b.dataset.reconnect,b.dataset.account)){showHealthPane('add');document.querySelector('nav button[data-tab="health"]')?.click();viewTop($('#connect-add'))}b.disabled=false});
document.addEventListener('click',async e=>{const b=e.target.closest('[data-disconnect]');if(!b||!confirm(`Disconnect ${b.dataset.name}? It stops syncing. What it already brought in stays.`))return;
 b.disabled=true;try{const r=await connectPost('connect_remove',{account:b.dataset.disconnect});toast(r.restarting?'Disconnected. Restarting…':'Disconnected. Restart the service to stop syncing it.');connectList=null;setTimeout(refresh,r.restarting?8000:500)}catch(err){errCaught(err);toast(err.message,true);b.disabled=false}});
function renderConnectRun(){const r=connectRun,box=$('#connect-add'),q=r.question;
 const head=`<div class="connect-run"><h3>${r.state==='done'?'✓ ':''}${esc(r.label||'')}</h3><ul class="connect-lines">${(r.lines||[]).map(l=>`<li>${linkify(l)}</li>`).join('')}</ul>`;
 let body='';
 const code=r.state==='running'&&r.code?connectCodeHTML(r.code):'';
 if(r.state==='running'&&r.signin&&!q){const n=SIGNIN_SITES[r.signin]?.name||r.signin;body=`<p class="connect-q">Sign in to ${esc(n)} on your Machine. This goes on by itself once you’re in.</p><div class="actions"><button type="button" class="primary" data-connect-site="${esc(r.signin)}">Sign in to ${esc(n)}</button></div>`;
  if(connectSiteShown!==r.session){connectSiteShown=r.session;setTimeout(()=>connectSiteSignin(r.signin),0)}}
 else if(code)body=code;
 else if(r.state==='running'&&q){const lead=q.kind==='choose'&&Number.isInteger(q.phone_first)&&(matchMedia('(max-width:560px)').matches||matchMedia('(pointer:coarse)').matches)?q.phone_first:-1,order=q.kind==='choose'?q.options.map((o,i)=>i).sort((a,b)=>(b===lead)-(a===lead)):[];
  const field=q.kind==='choose'?`<div class="connect-choices">${order.map(i=>`<button type="button"${i===lead?' class="primary"':''} data-connect-pick="${i}">${esc(q.options[i])}</button>`).join('')}</div>`:q.kind==='yes'?`<div class="actions"><button type="button" class="primary" data-connect-pick="yes">Yes</button><button type="button" data-connect-pick="no">No</button></div>`:`<form class="connect-form" data-connect-form><label for="connect-answer">${esc(q.prompt)}</label><input id="connect-answer" ${q.kind==='secret'?'type="password" autocomplete="off"':'type="text"'} value="${esc(q.kind==='secret'?'':q.default||'')}" spellcheck="false"${q.resend?' inputmode="numeric" autocomplete="one-time-code"':''}><div class="actions"><button class="primary">Continue</button>${q.resend?`<button type="button" data-connect-resend>${esc(t('Send the code again'))}</button>`:''}</div></form>`;
  body=(q.kind==='choose'||q.kind==='yes'?`<p class="connect-q">${esc(q.prompt)}</p>`:'')+field}
 else if(r.state==='running')body='<p class="muted">Working…</p>';
 else if(r.state==='done'){const c=connectCard(r),line=!r.restarting?'Restart the service to start reading it.':c?'Running again. Its card shows how far it is.':r.follow==='slow'?'Taking longer than usual. Its card shows up here once it runs again.':'Restarting to start reading it…';
  body=`<p class="note sent-ok"><span>${r.reconnect?'Signed in again.':'Connected.'}</span> <span>${line}</span></p><div class="actions">${c?`<button type="button" class="primary" data-connect-card="${esc(c.id)}">Open its card</button>`:''}<button type="button" data-connect-back>${r.reconnect?'Back':'Add another'}</button></div>`}
 else{const cmd=!state.manage_url&&/(?:^|: )((?:assistant|wacli|gog|gh|openclaw)\b[^;]*)/.exec(r.fix||'');body=`<p class="alert">${esc(r.error||'Stopped')}${r.fix?'. '+esc(r.fix[0].toUpperCase()+r.fix.slice(1))+'.':''}</p>${cmd?`<pre class="signin-command">${esc(cmd[1].trim())}</pre><button type="button" class="browser-link" data-copy-command="${esc(cmd[1].trim())}">Copy command</button> `:''}<div class="actions"><button type="button" data-connect="${esc(r.source)}"${r.reconnect?` data-connect-account="${esc(r.reconnect)}"`:''}>Try again</button><button type="button" data-connect-back>Back</button></div>`}
 const html=head+body+(r.state==='running'?`<div class="actions"><button type="button" class="ghost" data-connect-stop>Cancel</button></div>`:'')+'</div>';
 // A question being answered keeps what was typed: only redraw when something changed.
 const sig=JSON.stringify([r.state,r.lines,q&&q.id,r.error,r.follow,!!connectCard(r),r.signin,r.code]);if(box.dataset.sig===sig)return;box.dataset.sig=sig;connectDraw(box,'run',html);box.querySelector('#connect-answer')?.focus()}
// After a source is added the service restarts to start reading it: wait until it answers again with the new account,
// then move to that account's card, which shows how its first sync goes (the + Add pane says so until then).
const connectCard=r=>r?.account&&(state.connectors||[]).find(c=>c.id===r.account)||null;
function cardShow(id,flash){const c=(state.connectors||[]).find(x=>x.id===id);if(!c)return;showHealthPane(healthGroup(c.service));
 const el=[...document.querySelectorAll('#connectors>article')].find(a=>a.dataset.conn===id);if(!el)return;el.scrollIntoView({block:'center',behavior:'smooth'});
 if(flash){el.classList.add('conn-new');setTimeout(()=>el.classList.remove('conn-new'),4000)}}
async function connectFollow(run){const start=Date.now();await new Promise(r=>setTimeout(r,6000));
 while(connectRun===run&&Date.now()-start<180000){connectList=null;if(await refresh().catch(()=>false)&&connectCard(run)){renderConnectRun();
   if(healthPane==='add'&&!$('#health').hidden)cardShow(run.account,true);return}
  if(Date.now()-start>60000&&run.follow!=='slow'){run.follow='slow';renderConnectRun()}await new Promise(r=>setTimeout(r,2500))}}
function connectPoll(){clearTimeout(connectTimer);if(!connectRun||connectRun.state!=='running')return;connectTimer=setTimeout(async()=>{try{connectRun={...connectRun,...await connectPost('connect_poll',{session:connectRun.session})};renderConnectRun();
 if(connectRun.state==='done'&&connectRun.restarting)connectFollow(connectRun)}catch(e){errCaught(e);connectRun={...connectRun,state:'failed',error:e.message};renderConnectRun()}connectPoll()},connectRun.question?3000:1000)}
// A code the connect shows to sign in with: GitHub's device sign-in, or WhatsApp's pairing code for Linked devices.
// A QR code the Machine sends as rows of 0 and 1 (Telegram's login), drawn here: no image from anywhere else.
function qrSvg(rows){const n=rows.length,q=2,size=n+2*q;let d='';rows.forEach((r,y)=>{for(let x=0;x<r.length;x++)if(r[x]==='1')d+=`M${x+q} ${y+q}h1v1h-1z`});
 return `<svg class="connect-qr" viewBox="0 0 ${size} ${size}" role="img" aria-label="${esc(t('QR code'))}" shape-rendering="crispEdges"><rect width="${size}" height="${size}" fill="#fff"/><path d="${d}" fill="#000"/></svg>`}
function connectCodeHTML(c){if(c.kind==='qr'&&Array.isArray(c.matrix))return `<p class="connect-q">${esc(t('In Telegram on your phone: Settings, Devices, Link Desktop Device. Then scan this code:'))}</p>${qrSvg(c.matrix.filter(r=>/^[01]+$/.test(r)))}<p class="muted">${esc(t('The code refreshes by itself.'))}</p>`;
 const how=c.kind==='pair'?'In WhatsApp on your phone: Settings, Linked devices, Link a device, then Link with phone number instead. Enter this code:':c.kind==='openai'?'Enter this code at OpenAI to sign in:':'Enter this code at GitHub to sign in:';
 return `<p class="connect-q">${how}</p><p class="connect-code" translate="no">${esc(c.code)}</p><div class="actions code-actions"><button type="button" data-copy-command="${esc(c.code)}">Copy code</button>${c.url?`<a class="btn-link primary" href="${esc(c.url)}" target="_blank" rel="noopener">${c.kind==='openai'?'Open OpenAI ↗':'Open GitHub ↗'}</a>`:''}</div><p class="muted">This goes on by itself once you’re in.</p>`}
// LinkedIn or X, while its connect waits for the sign-in: that site's sign-in page opens in the Machine's browser and
// the sign-in dialog fills it from here; once in, the connect goes on by itself within seconds.
async function connectSiteSignin(site){try{await connectPost('connect_site_signin',{site})}catch(err){errCaught(err);toast(err.message,true);return}
 const after=()=>connectPoll();after.says='Signed in. Connecting it now.';openSignin(null,true,null,null,site,after)}
async function connectAnswer(value){const q=connectRun?.question;if(!q)return;try{connectRun={...connectRun,...await connectPost('connect_answer',{session:connectRun.session,question:q.id,value})}}catch(e){errCaught(e);toast(e.message,true)}renderConnectRun();connectPoll()}
$('#connect-add').addEventListener('click',async e=>{const t=e.target;
 if(t.closest('[data-codex-signin]')){connectSignin=signinOf(codexSource(),'intro');$('#connect-add').dataset.sig='';renderConnectSignin();return}
 const signin=t.closest('[data-connect-signin]');if(signin){const x=connectList.sources.find(v=>v.name===signin.dataset.connectSignin);connectSignin=signinOf(x,'intro');$('#connect-add').dataset.sig='';renderConnectSignin();return}
 if(t.closest('[data-signin-go]')){signinGo(t.closest('[data-signin-go]').dataset.way);return}
 const approve=t.closest('[data-phone-approve]');if(approve){phoneApprove(approve);return}
 const start=t.closest('[data-connect]');if(start){connectSignin=null;clearTimeout(signinTimer);
  if(!start.dataset.connectAccount&&connectList?.sources.some(v=>v.name===start.dataset.connect&&v.form)){connectRun=null;connectForm=start.dataset.connect;$('#connect-add').dataset.sig='';renderConnectForm();return}
  start.disabled=true;if(!await connectStart(start.dataset.connect,start.dataset.connectAccount))start.disabled=false;return}
 const site=t.closest('[data-connect-site]');if(site){connectSiteSignin(site.dataset.connectSite);return}
 if(t.closest('[data-connect-resend]')){connectAnswer('again');return}
 const pick=t.closest('[data-connect-pick]');if(pick){const v=pick.dataset.connectPick;connectAnswer(v==='yes'?true:v==='no'?false:+v);return}
 if(t.closest('[data-connect-stop]')&&connectRun){try{connectRun={...connectRun,...await connectPost('connect_cancel',{session:connectRun.session})}}catch{}renderConnectRun();connectPoll();return}
 const card=t.closest('[data-connect-card]');if(card){cardShow(card.dataset.connectCard,true);return}
 if(t.closest('[data-connect-back]')){connectRun=null;connectSignin=null;connectForm=null;connectGbrain=null;clearTimeout(signinTimer);$('#connect-add').dataset.sig='';connectAdd(true)}});
$('#connect-add').addEventListener('submit',e=>{const setup=e.target.closest('[data-connect-setup]');if(setup){e.preventDefault();connectSetup(setup);return}
 if(!e.target.closest('[data-connect-form]'))return;e.preventDefault();connectAnswer($('#connect-answer').value)});
$('#connect-add').addEventListener('change',e=>{if(e.target.name!=='scope')return;const form=e.target.closest('form'),co=form.querySelector('.connect-company'),personal=e.target.value==='personal';
 co.hidden=personal;co.querySelector('input').required=!personal});
// "Connect your own Intercom" on a to-do: Connections, + Add, at that source. A source that signs in here opens its
// sign-in intro (nothing starts before Continue); one set up on the account page or by questions is shown and focused.
async function connectOpen(name){showTab('health','add');await connectAdd(true);const box=$('#connect-add');
 const item=box.querySelector(`[data-connect-signin="${CSS.escape(name)}"]`);if(item){item.click();viewTop(box);return}
 const x=connectList?.sources.find(v=>v.name===name),el=x&&[...box.querySelectorAll('.connect-source')].find(n=>n.dataset.connect===name||n.querySelector('b')?.textContent.replace(' ↗','')===x.label);
 viewTop(box);if(el){el.classList.add('picked');el.focus()}}
document.addEventListener('click',e=>{const a=e.target.closest('[data-connect-open]');if(!a)return;e.preventDefault();connectOpen(a.dataset.connectOpen)});
function showHealthPane(id){healthPane=id;healthPicked=true;localStorage.setItem('health-pane',id);renderHealthTabs()}
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
// What a Docs connection may write, each only after the owner's OK (doc_writes.py), or Allow edits to ask for it
const docsWrites=c=>{const w=c.docs_writes||[],go=c.docs_write_signin&&!c.shared_by?(state.manage_url?hostedReconnect({...c,hosted_signin:c.docs_write_signin},'Allow edits','browser-link'):`<button type="button" class="browser-link" data-reconnect="docs" data-account="${esc(c.id)}" data-signin="${esc(c.docs_write_signin)}">Allow edits</button>`):'';
 const line=w.includes('edit')?'Creates and edits docs only after you OK each change.':w.includes('create')?'Creates new docs only after you OK them.':go?'Can’t create or edit docs yet.':'';
 return line?`<p class="muted conn-what conn-writes">${esc(t(line))}${go?' '+go:''}</p>`:''};
const docsConnect=c=>c.service!=='docs'||!/docs_not_connected/.test(c.error||'')?'Reconnect':c.docs_provider==='microsoft'?'Connect Microsoft documents':'Connect Google Docs';
function reconnectButton(c,label='Reconnect'){return c.hosted_signin&&state.manage_url?hostedReconnect(c,label,'browser-link'):c.account_page?`<a class="head-link" href="${esc(c.account_page)}" target="_blank" rel="noopener">${label} ↗</a>`:c.connect_name?`<button type="button" class="browser-link" data-reconnect="${esc(c.connect_name)}" data-account="${esc(c.id)}"${c.signin?` data-signin="${esc(c.signin)}"`:''}>${label}</button>`:''}
// Work (with its company) or Personal: the owner marks each sign-in. Leaving a Work Fleet removes that company's work
// accounts from this Machine (work_removal.py); personal ones stay.
const scopeLabel=b=>{b=String(b||'');return /^work:./.test(b)?t('Work')+' · '+b.slice(5):b==='personal:me'||b==='personal'?'Personal':/^personal:./.test(b)?t('Personal')+' · '+b.slice(9):b};
function scopeRow(c){const b=String(c.boundary||'');if(!b||/^owner:/.test(b)||c.service==='gateway')return '';
 const all=[...new Set([...(state.connectors||[]).map(x=>String(x.boundary||'')),b])],cur=b==='personal'?'personal:me':b;
 const opts=[...all.filter(x=>/^work:./.test(x)),...new Set(['personal:me',...all.filter(x=>/^personal:./.test(x))])].map(v=>[v,scopeLabel(v)]).concat([['','Work, another company…']]);
 return `<p class="conn-scope"><label>Work or personal<select data-scope="${esc(c.id)}" data-was="${esc(cur)}">${opts.map(([v,l])=>`<option value="${esc(v)}"${v===cur?' selected':''}>${esc(l)}</option>`).join('')}</select></label>${c.boundary_by==='guess'?' <small class="muted">Guessed. Pick one to be sure.</small>':''}</p>`}
document.addEventListener('change',async e=>{const s=e.target.closest('select[data-scope]');if(!s)return;let b=s.value;
 if(!b){const name=(prompt('Company name')||'').trim();if(!name){s.value=s.dataset.was;return}b='work:'+name}
 s.disabled=true;try{const r=await connectPost('connect_scope',{account:s.dataset.scope,boundary:b});toast(r.restarting?'Saved. Restarting…':'Saved. Restart the service to use it.');setTimeout(refresh,r.restarting?8000:500)}catch(err){errCaught(err);toast(err.message,true);s.disabled=false;s.value=s.dataset.was}});
function connActions(c){const name=esc(c.display_name||c.email||c.id);
 if(c.shared_by)return `<p class="note">${esc(t('Shared by {}. Its admins manage it.',c.shared_by))}</p>`;  // shared_connectors.py: no token, no Disconnect here
 if(c.hosted_signin&&state.manage_url)return `<div class="actions conn-actions">${hostedReconnect(c,docsConnect(c),'ghost')}${c.account_page?`<a class="btn-link" href="${esc(c.account_page)}" target="_blank" rel="noopener">Disconnect ↗</a>`:`<button type="button" class="ghost danger" data-disconnect="${esc(c.id)}" data-name="${name}">Disconnect</button>`}</div>`;  // Disconnect: the account page when it holds the grant
 if(c.account_page)return `<div class="actions conn-actions"><a class="btn-link" href="${esc(c.account_page)}" target="_blank" rel="noopener">Reconnect or disconnect ↗</a></div>`;
 return (c.shared_with?`<p class="note">Shared with ${esc(c.shared_with)}.</p>`:'')+(c.connect_name?`<div class="actions conn-actions"><button type="button" class="ghost" data-reconnect="${esc(c.connect_name)}" data-account="${esc(c.id)}"${c.signin?` data-signin="${esc(c.signin)}"`:''}>Reconnect</button><button type="button" class="ghost danger" data-disconnect="${esc(c.id)}" data-name="${name}">Disconnect</button></div>`:'')}
// Salesflare (assistant.py salesflare_progress): what it reads, the round of accounts it is on, Stop or Start, Restart
// for a round that is stuck, and where its API keys are.
function salesflareBox(c){const v=c.salesflare||{},r=v.round,id=esc(c.id),n=x=>Number(x||0).toLocaleString(DL);
 const line=v.stopped?'Nothing new comes in until you start it.':r?`Reading ${n(r.done)} of ${n(r.accounts)} accounts.${r.stuck?` Started ${ago(r.started)}, may be stuck.`:''}`:c.last_success?'':'Finding the accounts with recent emails and meetings…';
 const aside=[v.slow_accounts?`${n(v.slow_accounts)} skipped as too slow`:'',v.no_access?`${n(v.no_access)} without access`:''].filter(Boolean).join(' · ');
 const btn=(act,label)=>`<button type="button" class="head-link" data-sf-sync="${act}" data-account="${id}">${label}</button>`;
 return `${line?`<p class="note sf-line${r?.stuck&&!v.stopped?' sf-stuck':''}">${esc(line)}</p>`:''}${aside?`<p class="muted sf-aside">${esc(aside)}</p>`:''}`
  +(c.shared_by?'':`<div class="sf-actions">${v.stopped?btn('start',t('Start (a button)')):btn('stop','Stop')}${btn('restart','Restart sync')}${v.keys_url?`<a class="head-link" href="${esc(v.keys_url)}" target="_blank" rel="noopener">API keys ↗</a>`:''}</div>`)}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-sf-sync]');if(!b)return;const act=b.dataset.sfSync;
 if(act==='restart'&&!confirm('Restart the Salesflare sync? It drops the round it is on and reads the last week again. Nothing it brought in is lost.'))return;
 b.disabled=true;try{await connectPost('connector_sync',{account:b.dataset.account,do:act});toast(act==='stop'?'Stopped. Nothing new comes in until you start it.':act==='start'?'Started. It reads again in a moment.':'Restarted. It reads the last week again now.');await refresh()}catch(err){errCaught(err);toast(err.message,true)}finally{b.disabled=false}});
// Details: where a source's sync is, in words (its saved checkpoint, assistant.py commit_page), never the raw state.
function syncPlain(c){let st={};try{st=JSON.parse(c.state||'{}')||{}}catch{}const out=[];
 if(!c.last_success&&!c.state)return ['Waiting for the first sync. It starts within a few minutes.'];
 if(st.resync_reason||st.mode==='resync')out.push('Reading the last days again to fill a gap.');
 else if(st.mode==='bootstrap')out.push('First read: catching up on the last days.');
 else if(c.last_success)out.push('Caught up. Checks for new items every few minutes.');
 const until=c.salesflare?.synced_until||(/^\d{4}-\d\d-\d\dT/.test(st.watermark||'')?st.watermark:'');if(until)out.push(t('Read up to {}',date(until)));
 if(c.service==='slack'&&c.conversations)out.push(t('{} of {} conversations read at least once',c.conversations_collected||0,c.conversations));
 return out}
// Telegram chats: what it reads, and why it stopped with the way back (log in again, or the owner's own app ID)
function telegramNote(c){const stop=c.error==='telegram_app_blocked'?t('Telegram stopped accepting this Machine’s app ID. Nothing is read or sent. Reconnect with your own app ID from my.telegram.org.')
 :c.error==='telegram_logged_out'?t('Telegram logged this Machine out. Reconnect to keep reading.'):'';
 return `${stop?`<p class="alert">${esc(stop)} ${reconnectButton(c)}</p>`:''}`}
// Under Connected, on every card: what it brings in (c.what, the line + Add shows for it) and what it can do, each only
// after the owner's OK (c.acts, assistant.py connector_says). Docs says its own, with Allow edits; who Intercom replies
// as is under Details. One or two short lines, so the cards line up.
const CONN_ACTS={send:'Sends email only after you press Send.',reply:'Replies only after you press Send.',calendar:'Changes events only after you OK them.'};
function connWhat(c){const span=s=>s?`<span>${esc(t(s))}</span>`:'';
 if(c.service==='docs')return `<p class="muted conn-what">${c.docs_provider==='microsoft'?span(c.what)+' '+span('Replies stay drafts for you to post in Word.'):span('Google Docs. Reads comments, mentions, suggestions and shares. Posts a reply only when you OK it.')}</p>${docsWrites(c)}`;
 const act=span(CONN_ACTS[c.acts]);
 return c.what||act?`<p class="muted conn-what">${span(c.what)}${c.what&&act?' ':''}${act}</p>`:''}
function connectorCard(c,open){
const unit={calendar:'events',intercom:'conversations',android:'notifications',gateway:'alerts',github:'notifications',stripe:'events',rss:'items',docs:'items',google_meet:'meetings',trello:'card changes'}[c.service]||'messages',tone=connectorTone(c);
return `<article data-group="${healthGroup(c.service)}" data-conn="${esc(c.id)}"><div class="conn-head">${icon(c.service)}<div><h3>${esc(c.display_name||c.email)}</h3><small>${c.service==='docs'&&c.docs_provider==='google'?'Google Docs':service(c.service)} · ${esc(scopeLabel(c.boundary))}</small></div><span class="state-dot t-${tone}" title="${esc(connectorHealth(c).text)}"></span></div>
<p class="connection-status">${esc(connectorHealth(c).text)}</p>
${connWhat(c)}
<div class="figures"><div><b>${(c.total??0).toLocaleString(DL)}</b><span>${esc(t(unit))}</span></div><div><b>${c.signals_24h||0}</b><span>last 24h</span></div><div><b>${c.pending||0}</b><span>not reviewed</span></div></div>
${spark(c)}<div class="conn-foot"><small>${c.last_success?t('Last sync {}',time(c.last_success,true)):t('Not synced yet')}</small>${c.last_sync_signals==null?'':`<small title="${esc(t('New or changed messages and events, without duplicates. Last 24h counts when they came in here, not when they were sent.'))}">${esc(t('{} in last sync',c.last_sync_signals))}</small>`}</div>
${c.service==='salesflare'?salesflareBox(c):''}${c.signed_out?`<p class="alert">Signed out of ${esc(service(c.service))}. ${c.sign_in_url?`<a class="head-link" href="${esc(c.sign_in_url)}" target="_blank" rel="noopener">Sign in again</a>`:esc(c.sign_in_hint?c.sign_in_hint[0].toUpperCase()+c.sign_in_hint.slice(1)+'.':'Sign in again in the browser it reads with.')} <button type="button" class="browser-link" data-signin="${esc(c.id)}">Sign in here</button></p>`:c.sign_in_command?`<p class="alert">${esc(syncError(c.error))}. ${reconnectButton(c)||'Run the command below in a terminal on this computer.'}</p><details class="signin-fallback"${reconnectButton(c)?'':' open'}><summary>Or use a terminal</summary><pre class="signin-command">${esc(c.sign_in_command)}</pre><button type="button" class="browser-link" data-copy-command="${esc(c.sign_in_command)}">Copy command</button> <small>It syncs again within a minute after.</small></details>`:c.error&&!connectorHealth(c).resting?`<p class="alert">${['slack:HTTP_429','slack_ratelimited'].includes(c.error)?'Slack is taking a short pause.':esc(syncError(c.error))+'.'} ${connectorTone(c)==='orange'?(reconnectButton(c,docsConnect(c))||'Please reconnect this account.'):c.retry_at?esc(t('Next try {}.',ago(c.retry_at))):'Retrying automatically.'}</p>`:''}

${c.service==='slack'?`<p class="note">${slackProgress(c)}${c.conversation_errors?` · ${t('{} unavailable',c.conversation_errors)}`:''}${c.deferred_threads?` · ${t(['{} thread read waiting for retry','{} thread reads waiting for retry'],c.deferred_threads)}`:''}</p><p class="note">Slack’s limits mean a full round of conversations can take hours.</p>`:''}
${c.service==='android'?`<p class="note">${JSON.parse(c.state||'{}').transport==='direct_fallback'?'Using direct checks while the notification bridge is unavailable.':'Uses OpenClaw’s notification feed, plus a catch-up check of your phone.'} Checks run at most every 10 minutes, so notifications cleared in between may be missed.${JSON.parse(c.state||'{}').reconciliation_error?`<br><span class="error">Last phone check: ${esc(syncError(JSON.parse(c.state||'{}').reconciliation_error))}</span>`:''}</p>`:''}
${c.service==='telegram'?telegramNote(c):''}
<div class="conn-more"><details id="sync-recent-${esc(c.id)}" ${open.has('sync-recent-'+c.id)?'open':''}><summary>Recent syncs</summary>${(c.sync_activity||[]).map(a=>`<p><span class="mono muted">${esc(date(a.at))}</span> · ${a.status==='success'?`<span>${esc(a.signals==null?t('Synced'):t('Synced, {} new or changed',a.signals))}</span>`:`<span class="error">${esc(syncError(a.error))}</span>`+(a.retry_at?` · <span>${esc(t('Retry {}',date(a.retry_at)))}</span>`:'')}</p>`).join('')||'<p>No recent syncs recorded yet.</p>'}</details><details id="sync-details-${esc(c.id)}" ${open.has('sync-details-'+c.id)?'open':''}><summary>Details</summary>${c.failures_24h?`<p>${esc(t(['{} failed sync in the last 24 hours. Old failures don’t affect a connection that recovered.','{} failed syncs in the last 24 hours. Old failures don’t affect a connection that recovered.'],c.failures_24h))}</p>`:'<p>No failed syncs in the last 24 hours.</p>'}${c.last_failure?`<p>${esc(t('Last failure: {}, {}',syncError(c.last_failure.error),date(c.last_failure.at)))}</p>`:''}${c.error&&c.failures?`<p>${esc(t(['{} failed attempt in a row','{} failed attempts in a row'],c.failures))}</p>`:''}${syncPlain(c).map(l=>`<p class="conn-plain">${esc(l)}</p>`).join('')}${c.service==='intercom'&&c.replies_as&&c.replies_as!=='you'?`<p class="conn-plain conn-replies-as">${esc(t('Replies as {}, only after you press Send.',c.replies_as))}</p>`:''}${scopeRow(c)}${connActions(c)}</details></div></article>`;
}
