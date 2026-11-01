// Settings, Connected AIs (ai_app.py, docs/ai-connections.md): each outside AI that reaches this Machine over MCP, with its
// access, area and expiry, its Messages switch (off unless turned on: then it reads messages and its changes wait for an
// OK), Turn off now, Remove and its activity (Settings, Activity filtered to it: every call,
// refused ones too); Add a key for an AI
// that can't sign in by itself (the key shows once). Loads when the tab opens; the owner's dashboard only (AI_ACTIONS).
var aiView=null;let aiOpen='',aiLines={},aiMade=null,aiBusy=false,aiPairTimer=0,aiPairUntil=0;
const aiPost=(action,args={})=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
const AI_LEVELS=[['off','Off'],['read','Read'],['draft','Read & edit']],AI_AREAS=[['both','Work and Personal'],['work','Work only'],['personal','Personal only']],AI_EXPIRY=[['1d','1 day'],['7d','7 days'],['30d','30 days'],['1y','1 year']];
const aiOptions=(list,now)=>list.map(([v,l])=>`<option value="${v}"${v===now?' selected':''}>${esc(t(l))}</option>`).join('');
const aiDay=v=>new Date(v).toLocaleDateString(DL,{day:'numeric',month:'short',year:'numeric'});
async function aiLoad(){if(aiBusy)return;aiBusy=true;try{aiView=await aiPost('ai_connections');renderAi()}catch(e){errCaught(e);notice(e.message,true)}finally{aiBusy=false}}
function aiConnection(c){const both=(aiView.areas||[]).length>1,state=c.level==='off'?t('Off'):c.expired?t('Expired'):t('Until {}',aiDay(c.expires_at));
 const used=c.used_at?t('Last used {}',ago(c.used_at)):t('Not used yet'),calls=t(['{} call','{} calls'],c.calls)+(c.refused?', '+t(['{} refused','{} refused'],c.refused):'');
 const lines=aiLines[c.id],open=aiOpen===c.id;
 return `<div class="ai-conn" data-ai="${esc(c.id)}"><span class="grow"><strong translate="no">${esc(c.name)}</strong>${c.kind==='key'?' <span class="alpha">Key</span>':''}${c.official?' <span class="alpha">Official app</span>':''}<small>${esc(state)} · ${esc(used)} · ${esc(calls)}</small></span>
<span class="ai-controls"><select data-ai-level aria-label="Access">${aiOptions(AI_LEVELS,c.level)}</select>${both?`<select data-ai-area aria-label="What it can see">${aiOptions(AI_AREAS,c.area)}</select>`:''}<select data-ai-expiry aria-label="For how long"><option value="" selected>${esc(t(c.expired?'Renew for…':'Extend…'))}</option>${aiOptions(AI_EXPIRY,'')}</select>
<button type="button" class="ghost" data-ai-activity aria-expanded="${open}">Activity</button>${c.level!=='off'?'<button type="button" class="ghost" data-ai-off>Turn off now</button>':''}<button type="button" class="ghost" data-ai-remove>Remove</button></span>
<span class="ai-msg"><span class="grow"><strong>Messages</strong><small>Reads your email and chats. Its changes then wait for your OK.</small></span><button type="button" class="lookup-switch" role="switch" aria-checked="${!!c.messages}" aria-label="Messages" data-ai-messages></button></span></div>${open?`<div class="ai-activity">${!lines?`<p class="muted">${esc(t('Loading…'))}</p>`:lines.length?`<ol class="act-list">${actRows(lines)}</ol>`:`<p class="muted">${esc(t('Nothing yet.'))}</p>`}</div>`:''}`}
// After an Undo in an AI's own activity: its lines read again
async function aiActivityReload(){const id=aiOpen;if(!id)return;try{aiLines[id]=(await request('api/activity?kind=ai&actor='+encodeURIComponent(id))).items||[]}catch(err){errCaught(err)}renderAi()}
function renderAi(){const box=$('#settings-ai');if(!box||!aiView)return;const v=aiView,list=v.connections||[],both=(v.areas||[]).length>1;
 const r=v.reach||{};$('#ai-official').innerHTML=aiOfficial(r);$('#ai-private').hidden=!r.address;$('#ai-address').innerHTML=r.address?aiAddress(r):'';
 $('#ai-list').innerHTML=list.length?list.map(aiConnection).join(''):'<div><span class="grow"><small>No AI connected yet.</small></span></div>';
 $('#ai-key-area').hidden=!both;if(!both)$('#ai-key-area').value='both';
 const made=$('#ai-made');made.hidden=!aiMade;made.innerHTML=aiMade?`<span class="grow"><strong>Your new key</strong><small>Copy it now. It won’t show again.</small><code class="ai-url" translate="no">${esc(aiMade)}</code></span><button type="button" class="ghost" data-copy-command="${esc(aiMade)}">Copy</button>`:''}
// Two ways in (ai_app.ai_reach, docs/ai-connections.md): the official app first, Add in Claude (The Machine's listing in
// Claude's connector directory, which uses the shared address) above one shared address for every Machine
// (r.shared) with Copy, the account signing in and routing; then this Machine's private address, end to end. Both need
// this Machine on the account with a name: until then the official app's place shows Get your address (aiAddress).
const AI_CLAUDE_DIRECTORY='https://claude.ai/directory/connectors/the-machine';
function aiOfficial(r){
 if(r.shared)return `<div><span class="grow"><strong translate="no">Claude</strong><small>Add The Machine from Claude’s directory in one click.</small></span><a class="btn-link primary" href="${AI_CLAUDE_DIRECTORY}" target="_blank" rel="noopener" data-ai-claude>Add in Claude</a></div><div><span class="grow"><strong>Official app</strong><code class="ai-url" translate="no">${esc(r.shared)}</code></span><button type="button" class="ghost" data-copy-command="${esc(r.shared)}">Copy</button></div>`;
 if(!r.address)return aiAddress(r);
 return `<div><span class="grow"><strong>Official app</strong>${r.other?'<small>Set it up on your hosted Machine.</small>':r.tls==='missing'?'<small class="alert">Install the cryptography package to use this address.</small>':r.tls==='failed'?'<small class="alert">This address isn’t ready yet. The Machine tries again within the hour.</small>':'<small>Getting this address ready. It takes a few minutes.</small>'}</span></div>`}
// The private address: https://<name>.mcp.themachine.computer/mcp with Copy; on a self-hosted Machine not paired, or
// whose account has no name yet, Get your address instead (pairing.py: one page on the account, then the Fleet starts
// here by itself); Unpair on a paired self-hosted one. The same button pairs from Connections.
function aiAddress(r){const p=r.pairing;
 if(p&&p.state==='waiting')return `<div><span class="grow"><strong>Confirm on your account</strong><small>${esc(t('Check that the page in the new tab shows {}.',p.code||''))}</small></span>${p.url?`<a class="btn-link ghost" href="${esc(p.url)}" target="_blank" rel="noopener">Open it again</a>`:''}</div>`;
 if(r.address)return `<div><span class="grow"><strong>Your address</strong><code class="ai-url" translate="no">${esc(r.address)}</code>${r.other?'<small>Your hosted Machine answers at this address.</small>':r.tls==='missing'?'<small class="alert">Install the cryptography package to use this address.</small>':r.tls==='getting'?'<small>Getting this address ready. It takes a few minutes.</small>':r.tls==='failed'?'<small class="alert">This address isn’t ready yet. The Machine tries again within the hour.</small>':''}</span><button type="button" class="ghost" data-copy-command="${esc(r.address)}">Copy</button></div>`+(r.paired&&!r.hosted?aiPaired():'');
 if(r.hosted)return '<div><span class="grow"><small>This Machine has no name yet.</small></span></div>';
 const gone=p&&p.state==='gone'?'<small class="alert">That didn’t finish. Try again.</small>':'';
 if(r.paired&&r.away)return `<div><span class="grow"><strong>Your address</strong><small>Your account didn’t answer. Try again in a minute.</small></span><button type="button" class="ghost" data-ai-retry>Try again</button></div>`+aiPaired();
 if(r.paired)return `<div><span class="grow"><strong>Pick a name for your address</strong><small>Your account has no name yet. Pick one there.</small>${gone}</span><button type="button" class="primary" data-ai-get>Get your address</button></div>`+aiPaired();
 return `<div><span class="grow"><strong>Get your address</strong><small>Pair this Machine with your account and pick a name. It takes a minute.</small>${gone}</span><button type="button" class="primary" data-ai-get>Get your address</button></div>`}
const aiPaired=()=>'<div><span class="grow"><strong>Paired with your account</strong><small>Unpair to stop your account and AIs from reaching this Machine.</small></span><button type="button" class="ghost" data-ai-unpair>Unpair</button></div>';
// Get your address (and Pair this Machine in Connections): the tab opens within the click, then goes to the account's
// page once it is known; a browser that blocks it goes there in this tab. Then ai_pair_state every 2.5 s, up to 10 minutes.
async function aiPairGo(done){const tab=window.open('','_blank');
 try{const r=await aiPost('ai_pair_start',{});if(tab&&!tab.closed){tab.opener=null;tab.location.href=r.url}else location.href=r.url;
  if(aiView){aiView.reach={...(aiView.reach||{}),pairing:r.code?{url:r.url,code:r.code,state:'waiting'}:null};renderAi()}
  aiPairUntil=Date.now()+600000;aiPairPoll(done)}
 catch(e){if(tab)tab.close();errCaught(e);notice(e.message,true)}}
function aiPairPoll(done){clearTimeout(aiPairTimer);if(Date.now()>aiPairUntil)return;
 aiPairTimer=setTimeout(async()=>{let r;try{r=await aiPost('ai_pair_state',{fresh:true})}catch{return aiPairPoll(done)}
  if(aiView){aiView.reach=r.reach;renderAi()}
  if(done&&(r.state==='paired'||r.reach?.paired)){done(r);done=null}
  if(r.reach?.address)return notice(t('Your address is ready'));
  if(r.state!=='gone')aiPairPoll(done)},2500)}
for(const box of ['#ai-official','#ai-address'])$(box).addEventListener('click',async e=>{
 if(e.target.closest('[data-ai-get]'))aiPairGo();
 else if(e.target.closest('[data-ai-retry]'))try{const r=await aiPost('ai_pair_state',{fresh:true});aiView.reach=r.reach;renderAi()}catch(err){errCaught(err);notice(err.message,true)}
 else if(e.target.closest('[data-ai-unpair]')){if(confirm(t('Unpair this Machine? Your Fleet and sign-ins through your account stop until you pair it again.')))aiDo('ai_unpair',{},'Unpaired')}});
async function aiDo(action,args,done){try{const r=await aiPost(action,args);if(r.connections){aiView=r}else await aiLoad();renderAi();if(done)notice(t(done))}catch(e){errCaught(e);notice(e.message,true)}}
$('#ai-list').addEventListener('change',e=>{const row=e.target.closest('[data-ai]');if(!row)return;const id=row.dataset.ai;
 if(e.target.matches('[data-ai-level]'))aiDo('ai_change',{id,level:e.target.value},'Saved');
 else if(e.target.matches('[data-ai-area]'))aiDo('ai_change',{id,area:e.target.value},'Saved');
 else if(e.target.matches('[data-ai-expiry]')&&e.target.value)aiDo('ai_change',{id,expiry:e.target.value},'Saved')});
$('#ai-list').addEventListener('click',async e=>{const row=e.target.closest('[data-ai]');if(!row)return;const id=row.dataset.ai,name=row.querySelector('strong')?.textContent||'';
 const sw=e.target.closest('[data-ai-messages]');if(sw){const on=sw.getAttribute('aria-checked')!=='true';sw.setAttribute('aria-checked',on);aiDo('ai_change',{id,messages:on},on?'Messages on':'Messages off');return}
 if(e.target.closest('[data-ai-off]'))aiDo('ai_off',{id},'Turned off now');
 else if(e.target.closest('[data-ai-remove]')){if(confirm(t('Remove {}? It can’t reach your Machine until it connects again.',name)))aiDo('ai_remove',{id},'Removed')}
 else if(e.target.closest('[data-ai-activity]')){aiOpen=aiOpen===id?'':id;renderAi();if(aiOpen){try{aiLines[id]=(await request('api/activity?kind=ai&actor='+encodeURIComponent(id))).items||[]}catch(err){errCaught(err);aiLines[id]=[]}renderAi()}}});
$('#ai-key-form').onsubmit=async e=>{e.preventDefault();const f=e.currentTarget,b=f.querySelector('button');b.disabled=true;
 try{const r=await aiPost('ai_key',{name:$('#ai-key-name').value,level:$('#ai-key-level').value,area:$('#ai-key-area').value,expiry:$('#ai-key-expiry').value});aiView=r;aiMade=r.made?.key||null;$('#ai-key-name').value='';renderAi()}
 catch(err){errCaught(err);notice(err.message,true)}finally{b.disabled=false}};
