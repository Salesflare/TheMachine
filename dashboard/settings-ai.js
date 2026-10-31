// Settings, Connected AIs (ai_app.py, docs/ai-connections.md): each outside AI that reaches this Machine over MCP, with its
// access, area and expiry, Turn off now, Remove and its activity (Settings, Activity filtered to it: every call,
// refused ones too); Add a key for an AI
// that can't sign in by itself (the key shows once). Loads when the tab opens; the owner's dashboard only (AI_ACTIONS).
var aiView=null;let aiOpen='',aiLines={},aiMade=null,aiBusy=false;
const aiPost=(action,args={})=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
const AI_LEVELS=[['off','Off'],['read','Read'],['draft','Read & draft']],AI_AREAS=[['both','Work and Personal'],['work','Work only'],['personal','Personal only']],AI_EXPIRY=[['1d','1 day'],['7d','7 days'],['30d','30 days'],['1y','1 year']];
const aiOptions=(list,now)=>list.map(([v,l])=>`<option value="${v}"${v===now?' selected':''}>${esc(t(l))}</option>`).join('');
const aiDay=v=>new Date(v).toLocaleDateString(DL,{day:'numeric',month:'short',year:'numeric'});
async function aiLoad(){if(aiBusy)return;aiBusy=true;try{aiView=await aiPost('ai_connections');renderAi()}catch(e){errCaught(e);notice(e.message,true)}finally{aiBusy=false}}
function aiConnection(c){const both=(aiView.areas||[]).length>1,state=c.level==='off'?t('Off'):c.expired?t('Expired'):t('Until {}',aiDay(c.expires_at));
 const used=c.used_at?t('Last used {}',ago(c.used_at)):t('Not used yet'),calls=t(['{} call','{} calls'],c.calls)+(c.refused?', '+t(['{} refused','{} refused'],c.refused):'');
 const lines=aiLines[c.id],open=aiOpen===c.id;
 return `<div class="ai-conn" data-ai="${esc(c.id)}"><span class="grow"><strong translate="no">${esc(c.name)}</strong>${c.kind==='key'?' <span class="alpha">Key</span>':''}<small>${esc(state)} · ${esc(used)} · ${esc(calls)}</small></span>
<span class="ai-controls"><select data-ai-level aria-label="Access">${aiOptions(AI_LEVELS,c.level)}</select>${both?`<select data-ai-area aria-label="What it can see">${aiOptions(AI_AREAS,c.area)}</select>`:''}<select data-ai-expiry aria-label="For how long"><option value="" selected>${esc(t(c.expired?'Renew for…':'Extend…'))}</option>${aiOptions(AI_EXPIRY,'')}</select>
<button type="button" class="ghost" data-ai-activity aria-expanded="${open}">Activity</button>${c.level!=='off'?'<button type="button" class="ghost" data-ai-off>Turn off now</button>':''}<button type="button" class="ghost" data-ai-remove>Remove</button></span></div>${open?`<div class="ai-activity">${!lines?`<p class="muted">${esc(t('Loading…'))}</p>`:lines.length?`<ol class="act-list">${actRows(lines)}</ol>`:`<p class="muted">${esc(t('Nothing yet.'))}</p>`}</div>`:''}`}
function renderAi(){const box=$('#settings-ai');if(!box||!aiView)return;const v=aiView,list=v.connections||[],both=(v.areas||[]).length>1;
 $('#ai-address').innerHTML=v.mcp_url?`<div><span class="grow"><strong>Address for AIs</strong><small>Add it in the AI as a custom connector or MCP server.</small>${v.hosted?'':'<small>Only devices in your tailnet reach it.</small>'}<code class="ai-url" translate="no">${esc(v.mcp_url)}</code></span><button type="button" class="ghost" data-copy-command="${esc(v.mcp_url)}">Copy</button></div>`:'<div><span class="grow"><small>This Machine has no dashboard address yet.</small></span></div>';
 $('#ai-list').innerHTML=list.length?list.map(aiConnection).join(''):'<div><span class="grow"><small>No AI connected yet.</small></span></div>';
 $('#ai-key-area').hidden=!both;if(!both)$('#ai-key-area').value='both';
 const made=$('#ai-made');made.hidden=!aiMade;made.innerHTML=aiMade?`<span class="grow"><strong>Your new key</strong><small>Copy it now. It won’t show again.</small><code class="ai-url" translate="no">${esc(aiMade)}</code></span><button type="button" class="ghost" data-copy-command="${esc(aiMade)}">Copy</button>`:''}
async function aiDo(action,args,done){try{const r=await aiPost(action,args);if(r.connections){aiView=r}else await aiLoad();renderAi();if(done)notice(t(done))}catch(e){errCaught(e);notice(e.message,true)}}
$('#ai-list').addEventListener('change',e=>{const row=e.target.closest('[data-ai]');if(!row)return;const id=row.dataset.ai;
 if(e.target.matches('[data-ai-level]'))aiDo('ai_change',{id,level:e.target.value},'Saved');
 else if(e.target.matches('[data-ai-area]'))aiDo('ai_change',{id,area:e.target.value},'Saved');
 else if(e.target.matches('[data-ai-expiry]')&&e.target.value)aiDo('ai_change',{id,expiry:e.target.value},'Saved')});
$('#ai-list').addEventListener('click',async e=>{const row=e.target.closest('[data-ai]');if(!row)return;const id=row.dataset.ai,name=row.querySelector('strong')?.textContent||'';
 if(e.target.closest('[data-ai-off]'))aiDo('ai_off',{id},'Turned off now');
 else if(e.target.closest('[data-ai-remove]')){if(confirm(t('Remove {}? It can’t reach your Machine until it connects again.',name)))aiDo('ai_remove',{id},'Removed')}
 else if(e.target.closest('[data-ai-activity]')){aiOpen=aiOpen===id?'':id;renderAi();if(aiOpen){try{aiLines[id]=(await request('api/activity?kind=ai&actor='+encodeURIComponent(id))).items||[]}catch(err){errCaught(err);aiLines[id]=[]}renderAi()}}});
$('#ai-key-form').onsubmit=async e=>{e.preventDefault();const f=e.currentTarget,b=f.querySelector('button');b.disabled=true;
 try{const r=await aiPost('ai_key',{name:$('#ai-key-name').value,level:$('#ai-key-level').value,area:$('#ai-key-area').value,expiry:$('#ai-key-expiry').value});aiView=r;aiMade=r.made?.key||null;$('#ai-key-name').value='';renderAi()}
 catch(err){errCaught(err);notice(err.message,true)}finally{b.disabled=false}};
