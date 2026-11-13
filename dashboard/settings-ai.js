// Settings, Connected AIs (ai_app.py, docs/ai-connections.md): one row per outside AI that reaches this Machine over MCP
// (through the official app, one per app: ai_access.fold), with one line of its access, area, expiry and last use, and
// its Messages switch (off unless turned on: then it reads messages and its changes wait for an OK). Change opens the
// rest: access, area, Extend, Activity (Settings, Activity filtered to it: every call, refused ones too), Turn off now
// (a pause: its sign-ins end, its history stays) and Remove (it and its history go). Add a key for an AI
// that can't sign in by itself (the key shows once). Loads when the tab opens; the owner's dashboard only (AI_ACTIONS).
// This code loads when first needed, with Settings' other panels (dashboard_parts.LAZY); aiView, aiPost and the pairing
// (aiPairGo, used by Connections and General too) are in settings-shared.js.
let aiOpen='',aiEdit='',aiLines={},aiMade=null,aiBusy=false;
const AI_LEVELS=[['off','Off'],['read','Read'],['draft','Read & edit']],AI_AREAS=[['both','Work and Personal'],['work','Work only'],['personal','Personal only']],AI_EXPIRY=[['1d','1 day'],['7d','7 days'],['30d','30 days'],['1y','1 year']];
const aiOptions=(list,now)=>list.map(([v,l])=>`<option value="${v}"${v===now?' selected':''}>${esc(t(l))}</option>`).join('');
const aiDay=v=>localeDate(new Date(v),DL,{day:'numeric',month:'short',year:'numeric'});
async function aiLoad(){if(aiBusy)return;aiBusy=true;try{aiView=await aiPost('ai_connections');renderAi()}catch(e){errCaught(e);notice(e.message,true)}finally{aiBusy=false}}
const aiWord=(list,v)=>t((list.find(([k])=>k===v)||[v,v])[1]);
function aiConnection(c){const both=(aiView.areas||[]).length>1,lines=aiLines[c.id],edit=aiEdit===c.id,open=edit&&aiOpen===c.id;
 const said=c.level==='off'?[t('Off')]:c.expired?[t('Expired')]:[aiWord(AI_LEVELS,c.level),...(both?[aiWord(AI_AREAS,c.area)]:[]),t('until {}',aiDay(c.expires_at))];
 said.push(c.used_at?t('last used {}',ago(c.used_at)):t('not used yet'));if(c.refused)said.push(t(['{} refused','{} refused'],c.refused));
 return `<div class="ai-conn" data-ai="${esc(c.id)}"><span class="grow"><strong translate="no">${esc(c.name)}</strong>${c.kind==='key'?' <span class="alpha">Key</span>':''}${c.official?' <span class="alpha">Official app</span>':''}<small>${said.map(esc).join(' · ')}</small></span>
<span class="ai-end"><span class="ai-msg-label" aria-hidden="true">Messages</span><button type="button" class="lookup-switch" role="switch" aria-checked="${!!c.messages}" aria-label="Messages" title="Reads your email and chats. Its changes then wait for your OK." data-ai-messages></button><button type="button" class="ghost" data-ai-edit aria-expanded="${edit}">Change</button></span></div>${edit?`<div class="ai-edit" data-ai="${esc(c.id)}"><span class="ai-controls"><select data-ai-level aria-label="Access">${aiOptions(AI_LEVELS,c.level)}</select>${both?`<select data-ai-area aria-label="What it can see">${aiOptions(AI_AREAS,c.area)}</select>`:''}<select data-ai-expiry aria-label="For how long"><option value="" selected>${esc(t(c.expired?'Renew for…':'Extend…'))}</option>${aiOptions(AI_EXPIRY,'')}</select></span>
<span class="ai-controls"><button type="button" class="ghost" data-ai-activity aria-expanded="${open}">Activity</button>${c.level!=='off'?'<button type="button" class="ghost" data-ai-off>Turn off now</button>':''}<button type="button" class="ghost" data-ai-remove>Remove</button></span>
<small class="ai-msg-note"><strong>Messages</strong> Reads your email and chats. Its changes then wait for your OK.</small></div>`:''}${open?`<div class="ai-activity">${!lines?`<p class="muted">${esc(t('Loading…'))}</p>`:lines.length?`<ol class="act-list">${actRows(lines)}</ol>`:`<p class="muted">${esc(t('Nothing yet.'))}</p>`}</div>`:''}`}
// After an Undo in an AI's own activity: its lines read again
async function aiActivityReload(){const id=aiOpen;if(!id)return;try{aiLines[id]=(await request('api/activity?kind=ai&actor='+encodeURIComponent(id))).items||[]}catch(err){errCaught(err)}renderAi()}
function renderAi(){const box=$('#settings-ai');if(!box||!aiView)return;const v=aiView,list=v.connections||[],both=(v.areas||[]).length>1;
 const r=v.reach||{};$('#ai-official').innerHTML=aiOfficial(r);const listed=aiAddresses(r);$('#ai-addresses').innerHTML=listed;$('#ai-addresses').hidden=!listed;$('#ai-private-note').hidden=!r.address;
 $('#ai-list').innerHTML=list.length?list.map(aiConnection).join(''):'<div><span class="grow"><small>No AI connected yet.</small></span></div>';
 $('#ai-key-area').hidden=!both;if(!both)$('#ai-key-area').value='both';
 const made=$('#ai-made');made.hidden=!aiMade;made.innerHTML=aiMade?`<span class="grow"><strong>Your new key</strong><small>Copy it now. It won’t show again.</small><code class="ai-url" translate="no">${esc(aiMade)}</code></span><button type="button" class="ghost" data-copy-command="${esc(aiMade)}">Copy</button>`:''}
// Two ways in (ai_app.ai_reach, docs/ai-connections.md). First the official app's listings, Add in ChatGPT and Add in
// Claude (ChatGPT's plugins and Claude's connector directory, both on the shared address: the account signs in and routes
// to a hosted Machine or a paired self-hosted one). They need this Machine on the account with a name and, self-hosted,
// its certificate (r.shared): until then one muted row names both, with one line, above Get your address (aiAddress) or the
// address's state. Folded under Or add it by address (aiAddresses): the shared address and this Machine's own one
// (end to end, docs/ai-connections.md), each with Copy, and the steps to add one by hand. Unpair is in Settings, General,
// Account (settings-general.js), next to Open account: the official apps just work, so pairing has no section here.
const AI_CLAUDE_DIRECTORY='https://claude.ai/directory/the-machine';
const AI_CHATGPT_APP='https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4';
function aiApps(ready){
 if(!ready)return '<div class="ai-later"><span class="grow"><strong translate="no">ChatGPT · Claude</strong><small>Ready once this Machine has its address.</small></span></div>';
 return `<div><span class="grow"><strong translate="no">ChatGPT</strong><small>One click from ChatGPT’s plugins.</small></span><a class="btn-link primary" href="${AI_CHATGPT_APP}" target="_blank" rel="noopener" data-ai-chatgpt>Add in ChatGPT</a></div>`
  +`<div><span class="grow"><strong translate="no">Claude</strong><small>One click from Claude’s directory.</small></span><a class="btn-link primary" href="${AI_CLAUDE_DIRECTORY}" target="_blank" rel="noopener" data-ai-claude>Add in Claude</a></div>`}
function aiOfficial(r){
 if(r.shared)return aiApps(true);
 if(!r.address)return aiApps(false)+aiAddress(r);
 return aiApps(false)+`<div><span class="grow"><strong>Official app</strong>${r.other?'<small>Set it up on your hosted Machine.</small>':r.tls==='missing'?'<small class="alert">Install the cryptography package to use this address.</small>':r.tls==='failed'?'<small class="alert">This address isn’t ready yet. The Machine tries again within the hour.</small>':'<small>Getting this address ready. It takes a few minutes.</small>'}</span></div>`}
function aiAddresses(r){
 return (r.shared?`<div><span class="grow"><strong>Official app</strong><code class="ai-url" translate="no">${esc(r.shared)}</code></span><button type="button" class="ghost" data-copy-command="${esc(r.shared)}">Copy</button></div>`:'')
  +(r.address?aiAddress(r):'')}
// This Machine's own address: https://<name>.mcp.themachine.computer/mcp with Copy (folded); on a self-hosted Machine not
// paired, or whose account has no name yet, Get your address instead (pairing.py: one page on the account, then the
// Fleet starts here by itself). The same button pairs from Connections.
function aiAddress(r){const p=r.pairing;
 if(p&&p.state==='waiting')return `<div><span class="grow"><strong>Confirm on your account</strong><small>${esc(t('Check that the page in the new tab shows {}.',p.code||''))}</small></span>${p.url?`<a class="btn-link ghost" href="${esc(p.url)}" target="_blank" rel="noopener">Open it again</a>`:''}</div>`;
 if(r.address)return `<div><span class="grow"><strong>Your address</strong><code class="ai-url" translate="no">${esc(r.address)}</code>${r.other?'<small>Your hosted Machine answers at this address.</small>':r.tls==='missing'?'<small class="alert">Install the cryptography package to use this address.</small>':r.tls==='getting'?'<small>Getting this address ready. It takes a few minutes.</small>':r.tls==='failed'?'<small class="alert">This address isn’t ready yet. The Machine tries again within the hour.</small>':''}</span><button type="button" class="ghost" data-copy-command="${esc(r.address)}">Copy</button></div>`;
 if(r.hosted)return '<div><span class="grow"><small>This Machine has no name yet.</small></span></div>';
 const gone=p&&p.state==='gone'?'<small class="alert">That didn’t finish. Try again.</small>':'';
 if(r.paired&&r.away)return `<div><span class="grow"><strong>Your address</strong><small>Your account didn’t answer. Try again in a minute.</small></span><button type="button" class="ghost" data-ai-retry>Try again</button></div>`;
 if(r.paired)return `<div><span class="grow"><strong>Pick a name for your address</strong><small>Your account has no name yet. Pick one there.</small>${gone}</span><button type="button" class="primary" data-ai-get>Set up</button></div>`;
 return `<div><span class="grow"><strong>Get your address</strong><small>Pair this Machine with your account and pick a name. It takes a minute.</small>${gone}</span><button type="button" class="primary" data-ai-get>Set up</button></div>`}
$('#ai-official').addEventListener('click',async e=>{
 if(e.target.closest('[data-ai-get]'))aiPairGo();
 else if(e.target.closest('[data-ai-retry]'))try{const r=await aiPost('ai_pair_state',{fresh:true});aiView.reach=r.reach;renderAi()}catch(err){errCaught(err);notice(err.message,true)}});
async function aiDo(action,args,done){try{const r=await aiPost(action,args);if(r.connections){aiView=r}else await aiLoad();renderAi();if(done)notice(t(done))}catch(e){errCaught(e);notice(e.message,true)}}
$('#ai-list').addEventListener('change',e=>{const row=e.target.closest('[data-ai]');if(!row)return;const id=row.dataset.ai;
 if(e.target.matches('[data-ai-level]'))aiDo('ai_change',{id,level:e.target.value},'Saved');
 else if(e.target.matches('[data-ai-area]'))aiDo('ai_change',{id,area:e.target.value},'Saved');
 else if(e.target.matches('[data-ai-expiry]')&&e.target.value)aiDo('ai_change',{id,expiry:e.target.value},'Saved')});
$('#ai-list').addEventListener('click',async e=>{const row=e.target.closest('[data-ai]');if(!row)return;const id=row.dataset.ai,name=(aiView?.connections||[]).find(c=>c.id===id)?.name||'';
 if(e.target.closest('[data-ai-edit]')){aiEdit=aiEdit===id?'':id;aiOpen='';renderAi();return}
 const sw=e.target.closest('[data-ai-messages]');if(sw){const on=sw.getAttribute('aria-checked')!=='true';sw.setAttribute('aria-checked',on);aiDo('ai_change',{id,messages:on},on?'Messages on':'Messages off');return}
 if(e.target.closest('[data-ai-off]'))aiDo('ai_off',{id},'Turned off now');
 else if(e.target.closest('[data-ai-remove]')){if(confirm(t('Remove {}? It can’t reach your Machine until it connects again.',name)))aiDo('ai_remove',{id},'Removed')}
 else if(e.target.closest('[data-ai-activity]')){aiOpen=aiOpen===id?'':id;renderAi();if(aiOpen){try{aiLines[id]=(await request('api/activity?kind=ai&actor='+encodeURIComponent(id))).items||[]}catch(err){errCaught(err);aiLines[id]=[]}renderAi()}}});
$('#ai-key-form').onsubmit=async e=>{e.preventDefault();const f=e.currentTarget,b=f.querySelector('button');b.disabled=true;
 try{const r=await aiPost('ai_key',{name:$('#ai-key-name').value,level:$('#ai-key-level').value,area:$('#ai-key-area').value,expiry:$('#ai-key-expiry').value});aiView=r;aiMade=r.made?.key||null;$('#ai-key-name').value='';renderAi()}
 catch(err){errCaught(err);notice(err.message,true)}finally{b.disabled=false}};
