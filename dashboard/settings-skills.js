// Skills (skills.py): the owner's how-tos, written to OpenClaw's workspace; shared ones are read here and installed by the owner.
let skillsKey='',skillEditing=null,skillSharing=null;
const skillAct=async(action,args)=>{const v=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});if(v&&v.skills)state.skills=v;skillsKey='';renderSkills();renderNeedsYou();return v};
function skillMeta(s){if(s.status==='incoming')return `${esc(t(s.update?'Update by {} · version {}':'Shared by {} · version {}',s.author||t('a teammate'),s.version))}${s.note?` · <span translate="no">“${esc(s.note)}”</span>`:''}`;
 if(s.status==='proposed')return (s.update?'Update proposed by your Machine':'Proposed by your Machine')+(s.note?`: ${esc(s.note)}`:'');
 const bits=[];if(s.status==='off')bits.push('Off');if(s.imported)bits.push(`Imported from ${{claude:'Claude',chatgpt:'ChatGPT'}[s.imported.from]||'elsewhere'}`);if(s.origin==='shared')bits.push(`From ${esc(s.author||'a teammate')}, version ${s.version}`);
 if(s.shares?.length)bits.push(t('Shared: {}',s.shares.map(x=>`${esc(x.name)} ${esc(x.status)}`).join(', ')));if(s.changed)bits.push('Changed since you shared it');return bits.join(' · ')}
function skillRow(s,targets){const wait=s.status==='incoming'||s.status==='proposed',meta=skillMeta(s);
 // A proposed update opens its before and after; Update skill there is the only way it changes the skill.
 const buttons=s.status==='proposed'&&s.update?`<button type="button" class="primary" data-skill-update="${s.id}" data-settings>Update</button><button type="button" class="ghost" data-skill-decide="dismiss" data-id="${s.id}">Dismiss</button>`
  :wait?`<button type="button" class="ghost" data-skill-read="${s.id}">Read</button><button type="button" class="primary" data-skill-decide="${s.status==='incoming'?'install':'approve'}" data-id="${s.id}">${s.status==='incoming'?'Install':'Approve'}</button><button type="button" class="ghost" data-skill-decide="${s.status==='incoming'?'decline':'dismiss'}" data-id="${s.id}">${s.status==='incoming'?'Decline':'Dismiss'}</button>`
  :`<button type="button" class="ghost" data-skill-edit="${s.id}">Edit</button>${targets.length?`<button type="button" class="ghost" data-skill-share="${s.id}">${s.changed?'Share again':'Share'}</button>`:''}<button type="button" class="ghost" data-skill-toggle="${s.id}" data-on="${s.status==='off'?1:0}">${s.status==='off'?'Turn on':'Turn off'}</button>`;
 const plain=meta.replace(/<[^>]*>/g,'').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'");
 return `<div class="${wait?'skill-wait':s.status==='off'?'skill-off':''}" data-skill="${s.id}"><span class="grow"><strong title="${esc(s.name)}">${esc(s.name)}</strong><small>${esc(s.description)}</small>${meta?`<small class="skill-meta" title="${esc(plain)}">${meta}</small>`:''}${s.status==='proposed'?skillRelated(s.related)+skillStale(s.update):''}${s.notes?.length?`<details class="skill-notes"><summary>From ${s.notes.length} of your notes</summary><ul>${s.notes.map(n=>`<li>${esc(n)}</li>`).join('')}</ul></details>`:''}</span><span class="skill-buttons">${buttons}</span></div>`}
function renderSkills(){const v=state.skills,box=$('#settings-skills');if(!box)return;box.hidden=!v;if(!v)return;const key=JSON.stringify(v);if(key===skillsKey)return;skillsKey=key;
 $('#skills-list').innerHTML=v.skills.map(s=>skillRow(s,v.targets||[])).join('')||'<div class="muted">No skills yet.</div>';
 $('#skill-example').hidden=v.skills.length>0;
 for(const id of ['#skills-find','#skills-yours-head','#skills-hub'])$(id).hidden=!v.openclaw;renderSkillHints();
 if(v.openclaw&&!installedView)loadInstalled();filterSkills()}
// Everything else OpenClaw has (skills.py Catalog): shown read-only. On/off is OpenClaw's own setting; a ClawHub skill
// is installed with OpenClaw's own command, only by the owner's tap after reading it.
let installedView=null,installedLoading=false,lookShown=null;
const skillCall=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
async function loadInstalled(refresh=false){if(installedLoading)return;installedLoading=true;
 try{installedView=await skillCall('skill_installed',{refresh})}catch(err){errCaught(err);installedView={installed:[],error:err.message}}finally{installedLoading=false}renderInstalled()}
const SKILL_GROUPS=[['workspace','Workspace'],['bundled','Bundled with OpenClaw'],['other','Other']];
function installedRow(i){const meta=[i.state==='ready'?'<span class="skill-ready">Ready</span>':i.state==='off'?'Off':i.state==='blocked'?'Not allowed for this agent':'Needs setup'];
 if(i.needs&&i.state!=='ready'&&i.needs!=='Not allowed for this agent')meta.push(esc(i.needs));if(i.group==='other')meta.push(esc(i.source));
 return `<div class="${i.state==='ready'?'':'skill-off'}" data-installed="${esc(i.name)}"><span class="grow"><strong title="${esc(i.name)}">${i.emoji?esc(i.emoji)+' ':''}${esc(i.name)}</strong><small>${esc(i.description)}</small><small class="skill-meta">${meta.join(' · ')}</small></span><span class="skill-buttons"><button type="button" class="ghost" data-installed-read="${esc(i.name)}">Read</button>${i.toggle?`<button type="button" class="ghost" data-installed-toggle="${esc(i.name)}" data-on="${i.on?0:1}">${i.on?'Turn off':'Turn on'}</button>`:''}</span></div>`}
function renderInstalled(){const box=$('#skills-installed'),v=installedView;if(!box)return;if(!v||!state.skills?.openclaw){box.innerHTML='';return}
 const items=(v.installed||[]).filter(i=>i.group!=='yours'),open=new Set([...box.querySelectorAll('details[open]')].map(d=>d.dataset.group));if(!box.innerHTML)open.add('workspace');
 box.innerHTML=(v.error?`<p class="fine">Couldn’t read OpenClaw’s skills just now: ${esc(v.error)}</p>`:'')+SKILL_GROUPS.map(([g,label])=>{const list=items.filter(i=>i.group===g);if(!list.length)return '';
  return `<details class="skills-group" data-group="${g}"${open.has(g)?' open':''}><summary>${label} <small>${list.filter(i=>i.state==='ready').length} of ${list.length} ready</small></summary><div class="list settings-list skills-list">${list.map(installedRow).join('')}</div></details>`}).join('')
  +`<p class="fine">As OpenClaw has them${v.checked_at?', '+esc(ago(v.checked_at)):''}. Only read here. <button type="button" class="link" id="skills-refresh">Check again</button></p>`;
 filterSkills()}
// One search over names and descriptions, yours and OpenClaw's.
function filterSkills(){const q=($('#skills-filter')?.value||'').trim().toLowerCase();
 for(const row of document.querySelectorAll('#skills-list>[data-skill],#skills-installed [data-installed]')){const text=[...row.querySelectorAll('strong,small:not(.skill-meta)')].map(e=>e.textContent).join(' ').toLowerCase();row.hidden=!!q&&!text.includes(q)}
 for(const d of document.querySelectorAll('#skills-installed details')){const any=[...d.querySelectorAll('[data-installed]')].some(r=>!r.hidden);d.hidden=!!q&&!any;if(q&&any)d.open=true}}
$('#skills-filter').addEventListener('input',filterSkills);
// "There's a skill for this": the agent judged that a skill would clearly help with a card. Quiet, dismissable.
const hintFor=id=>(state.skills?.hints||[]).find(h=>String(h.suggestion_id)===String(id));
const skillHintNote=s=>{const h=!closed(s)&&hintFor(s.id);return h?`<p class="note skill-hint">There’s a skill for this: <button type="button" class="link" data-hint-look="${esc(h.id)}">${esc(h.name)}</button>${h.kind==='clawhub'?' on ClawHub':''}. <button type="button" class="link" data-hint-dismiss="${esc(h.id)}">Not now</button></p>`:''};
function renderSkillHints(){const hints=state.skills?.hints||[],box=$('#skills-hints');box.hidden=!hints.length;
 box.innerHTML=hints.length?`<h3 class="skills-head">Suggested for your to-dos</h3><div class="list settings-list skills-list">${hints.map(h=>`<div data-hint="${esc(h.id)}"><span class="grow"><strong title="${esc(h.name)}">${esc(h.name)}</strong><small>${esc(h.why)}</small><small class="skill-meta">${h.kind==='clawhub'?'Third-party, on ClawHub':'Installed, not ready yet'}</small></span><span class="skill-buttons"><button type="button" class="ghost" data-hint-look="${esc(h.id)}">Look</button><button type="button" class="ghost" data-hint-dismiss="${esc(h.id)}">Not now</button></span></div>`).join('')}</div>`:''}
function lookOpen(title,from,notes,body,actions){$('#skill-look-title').textContent=title;$('#skill-look-from').textContent=from;$('#skill-look-error').textContent='';
 $('#skill-look-notes').innerHTML=notes.filter(Boolean).map(([text,warn])=>`<li${warn?' class="warn"':''}>${esc(text)}</li>`).join('');$('#skill-look-body').textContent=body;$('#skill-look-actions').innerHTML=actions;
 if(!$('#skill-look').open)$('#skill-look').showModal();$('#skill-look-body').scrollTop=0}
async function lookInstalled(name,why=''){const d=await skillCall('skill_installed_get',{name});if(!installedView)await loadInstalled();const i=(installedView?.installed||[]).find(x=>x.name===name)||{};lookShown={kind:'installed',name};
 lookOpen(d.name,`${d.source}. ${d.state==='ready'?'Ready.':d.state==='off'?'Off.':'Not ready yet.'} Only read here: its files stay as they are.`,
  [why&&[t('Why: {}',why)],d.needs&&d.state!=='ready'&&[d.needs,true],...(d.install_steps||[]).map(x=>[t('OpenClaw can set it up: {}',x)])],d.body,
  (i.toggle?`<button type="button" class="${i.on?'ghost':'primary'}" data-look-toggle="${esc(name)}" data-on="${i.on?0:1}">${i.on?'Turn off':'Turn on'}</button>`:'')+'<button type="button" class="ghost" data-look-close>Close</button>')}
async function lookHub(ref,why=''){$('#hub-status').textContent='';const d=await skillCall('skill_hub_get',{ref});lookShown={kind:'clawhub',...d};
 lookOpen(d.name,`Third-party, from ClawHub: by @${d.owner}, version ${d.version}. Not written or checked by The Machine.`,
  [why&&[t('Why: {}',why)],d.flagged&&['ClawHub flagged this skill.',true],d.code?.length&&[`It comes with ${d.code.length} script or code file${d.code.length>1?'s':''} (${d.code.slice(0,3).join(', ')}${d.code.length>3?', …':''}) your agent could run.`,true],
   d.install_steps&&['It has install steps: OpenClaw may install tools for it.',true],d.asks_keys&&['It asks for keys or settings.',true],
   d.scan&&[`ClawHub’s scan: ${d.scan}${d.scan_warnings?', with warnings':''}.${d.scan_summary?' '+d.scan_summary:''}`,d.scan!=='clean'||d.scan_warnings],
   ['Once installed, your Machine can use it in any task, like your other skills.']],d.body,
  `<button type="button" class="primary" data-hub-install="${esc(d.ref)}">Install</button><a class="btn-link ghost" href="${esc(safeURL(d.url))}" target="_blank" rel="noopener">On ClawHub ↗</a><button type="button" class="ghost" data-look-close>Close</button>`)}
async function hintLook(id){const h=(state.skills?.hints||[]).find(x=>x.id===id);if(!h)return;return h.kind==='clawhub'?lookHub(h.skill,h.why):lookInstalled(h.skill,h.why)}
async function hintDismiss(id){const v=await skillCall('skill_hint_dismiss',{id});if(v?.skills)state.skills=v;skillsKey='';renderSkills();render()}
function hubRow(r){const meta=['Third-party',`@${esc(r.owner)}`,`${Number(r.downloads||0).toLocaleString(DL)} downloads`];if(r.official)meta.push('Official');if(r.suspicious)meta.push('Flagged');
 return `<div data-hub="${esc(r.ref)}"><span class="grow"><strong title="${esc(r.name)}">${esc(r.name)}</strong><small>${esc(r.summary)}</small><small class="skill-meta">${meta.join(' · ')}</small></span><span class="skill-buttons">${r.installed?'<span class="fine">Installed</span>':`<button type="button" class="ghost" data-hub-read="${esc(r.ref)}">Read</button>`}</span></div>`}
$('#hub-search').addEventListener('submit',async e=>{e.preventDefault();const q=$('#hub-query').value.trim();if(!q)return;$('#hub-go').disabled=true;$('#hub-status').textContent='Searching ClawHub…';
 try{const v=await skillCall('skill_hub_search',{query:q});$('#hub-results').innerHTML=v.results.map(hubRow).join('');$('#hub-status').textContent=v.results.length?'':'Nothing found on ClawHub.'}
 catch(err){errCaught(err);$('#hub-status').textContent=err.message}finally{$('#hub-go').disabled=false}});
document.addEventListener('click',async e=>{const t=e.target.closest('[data-hint-look],[data-hint-dismiss],[data-installed-read],[data-installed-toggle],[data-hub-read],[data-hub-install],[data-look-toggle],[data-look-close],#skills-refresh');if(!t)return;
 const err=m=>$('#skill-look').open?$('#skill-look-error').textContent=m:notice(m);
 try{if(t.id==='skills-refresh'){t.disabled=true;await loadInstalled(true);return}
  if(t.dataset.lookClose!==undefined){$('#skill-look').close();return}
  if(t.dataset.hintLook)return await hintLook(t.dataset.hintLook);
  if(t.dataset.hintDismiss){t.disabled=true;await hintDismiss(t.dataset.hintDismiss);return}
  if(t.dataset.installedRead)return await lookInstalled(t.dataset.installedRead);
  if(t.dataset.hubRead)return await lookHub(t.dataset.hubRead);
  const toggle=t.dataset.installedToggle||t.dataset.lookToggle;
  if(toggle){t.disabled=true;installedView=await skillCall('skill_installed_toggle',{name:toggle,on:t.dataset.on==='1'});renderInstalled();if($('#skill-look').open)$('#skill-look').close();
   notice(t.dataset.on==='1'?'Turned on in OpenClaw.':'Turned off in OpenClaw.');refresh();return}
  if(t.dataset.hubInstall){const d=lookShown;if(!d||d.ref!==t.dataset.hubInstall)return;t.disabled=true;t.textContent='Installing…';
   const v=await skillCall('skill_hub_install',{ref:d.ref,version:d.version,sha:d.sha});installedView=v;renderInstalled();$('#skill-look').close();
   for(const row of document.querySelectorAll(`#hub-results [data-hub="${CSS.escape(d.ref)}"] .skill-buttons`))row.innerHTML='<span class="fine">Installed</span>';
   notice(v.differs?'Installed, but what OpenClaw installed differs from what you read. Check it under Workspace.':'Installed. Your Machine can use it from its next task.');refresh();return}
 }catch(error){errCaught(error);t.disabled=false;if(t.dataset.hubInstall)t.textContent='Install';err(error.message)}});
function skillEditor(skill){skillEditing=skill?.id||null;$('#skill-share').hidden=true;$('#skill-editor-title').textContent=skill?.id?'Edit skill':'New skill';
 $('#skill-name').value=skill?.name||'';$('#skill-description').value=skill?.description||'';$('#skill-body').value=skill?.body||'';$('#skill-error').textContent='';$('#skill-delete').hidden=!skill?.id;
 $('#skill-editor').hidden=false;$('#skill-editor').scrollIntoView({block:'center',behavior:'smooth'});$('#skill-name').focus({preventScroll:true})}
function skillShare(id){const v=state.skills,s=v.skills.find(x=>x.id===id);if(!s)return;skillSharing=id;$('#skill-editor').hidden=true;$('#skill-share-title').textContent=`Share “${s.name}”`;
 const opts=[];for(const t of v.targets||[]){if(t.kind==='friends'){for(const m of t.members)opts.push([`${t.fleet}|${m.member_id}`,`Friend: ${m.name}`])}else{opts.push([`${t.fleet}|`,`${t.name}: everyone`]);for(const m of t.members)opts.push([`${t.fleet}|${m.member_id}`,`${t.name}: ${m.name}`])}}
 $('#skill-share-to').innerHTML=opts.map(([val,label])=>`<option value="${esc(val)}">${esc(label)}</option>`).join('');$('#skill-share-note').value='';$('#skill-share-error').textContent='';$('#skill-share').hidden=false;$('#skill-share').scrollIntoView({block:'center',behavior:'smooth'})}
async function skillRead(id){const s=state.skills.skills.find(x=>x.id===id);if(!s)return;const d=$('#skill-read');$('#skill-read-error').textContent='';
 try{const full=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'skill_get',args:{id}})});
  $('#skill-read-title').textContent=s.name;$('#skill-read-from').textContent=s.status==='incoming'?`${s.update?'An update to a skill you have, from':'From'} ${s.author||'a teammate'}, version ${s.version}. Read it before you install. It can’t change what your Machine may do.`:'Proposed by your Machine from repeated work. It stays off until you approve it.';
  $('#skill-read-description').textContent=t('When: {}',s.description);$('#skill-read-body').textContent=full.body;
  const yes=s.status==='incoming'?'install':'approve',no=s.status==='incoming'?'decline':'dismiss';
  $('#skill-read-actions').innerHTML=`<button type="button" class="primary" data-skill-decide="${yes}" data-id="${s.id}">${s.status==='incoming'?'Install':'Approve'}</button><button type="button" class="ghost" data-skill-decide="${no}" data-id="${s.id}">${s.status==='incoming'?'Decline':'Dismiss'}</button>`;
  d.showModal()}catch(err){errCaught(err);notice(err.message)}}
$('#settings-skills').addEventListener('click',async e=>{const t=e.target.closest('button');if(!t)return;
 try{if(t.id==='skill-new')return skillEditor(null);
  if(t.id==='skill-example')return skillEditor(await skillAct('skill_example',{}));
  if(t.id==='skill-import-open'){$('#skill-editor').hidden=true;$('#skill-share').hidden=true;$('#skill-import').hidden=false;importNote();$('#skill-import').scrollIntoView({block:'start',behavior:'smooth'});return}
  if(t.id==='skill-cancel'){$('#skill-editor').hidden=true;return}
  if(t.id==='skill-share-cancel'){$('#skill-share').hidden=true;return}
  if(t.id==='skill-delete'){if(!confirm('Delete this skill? Your Machine stops using it.'))return;await skillAct('skill_delete',{id:skillEditing});$('#skill-editor').hidden=true;notice('Skill deleted.');return}
  if(t.dataset.skillEdit){const full=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'skill_get',args:{id:t.dataset.skillEdit}})});return skillEditor(full)}
  if(t.dataset.skillShare)return skillShare(t.dataset.skillShare);
  if(t.dataset.skillToggle){t.disabled=true;await skillAct('skill_toggle',{id:t.dataset.skillToggle,on:t.dataset.on==='1'});return}
  if(t.dataset.skillRead)return skillRead(t.dataset.skillRead);
  if(t.dataset.skillDecide){t.disabled=true;const c=t.dataset.skillDecide;await skillAct('skill_decide',{id:t.dataset.id,choice:c});if($('#skill-read').open)$('#skill-read').close();notice({install:'Installed. Your Machine uses it from now on.',approve:'Approved. Your Machine uses it from now on.',decline:'Declined.',dismiss:'Dismissed.'}[c]);return}
 }catch(err){errCaught(err);t.disabled=false;($('#skill-editor').hidden?notice:m=>$('#skill-error').textContent=m)(err.message)}});
$('#skill-editor').addEventListener('submit',async e=>{e.preventDefault();$('#skill-save').disabled=true;
 try{await skillAct('skill_save',{id:skillEditing||'',name:$('#skill-name').value,description:$('#skill-description').value,body:$('#skill-body').value});$('#skill-editor').hidden=true;notice('Skill saved. Your Machine uses it from now on.')}
 catch(err){errCaught(err);$('#skill-error').textContent=err.message}finally{$('#skill-save').disabled=false}});
$('#skill-share').addEventListener('submit',async e=>{e.preventDefault();const [fleetRef,member]=$('#skill-share-to').value.split('|');$('#skill-share-send').disabled=true;
 try{const v=await skillAct('skill_share',{id:skillSharing,fleet:fleetRef,...(member?{to:[member]}:{}),note:$('#skill-share-note').value});$('#skill-share').hidden=true;notice(t(v.sent===1?'Sent. They read it and decide.':'Sent to {}. They read it and decide.',v.sent))}
 catch(err){errCaught(err);$('#skill-share-error').textContent=err.message}finally{$('#skill-share-send').disabled=false}});
// Import from Claude or ChatGPT (skills.py Importer): listed for the owner to tick. Only instructions come in; a
// skill that needs its scripts can be installed in OpenClaw instead, after reading it, like ClawHub.
let importView=null,importTimer=null,importShown=null;
// A short list first: Recommended, then Yours; the rest in closed groups with counts; what can't come in last.
const IMPORT_GROUPS=[['project','In your projects'],['vendor','From vendors'],['builtin','Built in']],IMPORT_SITES={claude:'Claude',chatgpt:'ChatGPT'},IMPORT_YOURS=8;
const IMPORT_LABELS={local:'This computer',claude:'claude.ai',chatgpt:'ChatGPT'},IMPORT_BUSY={claude:1,chatgpt:1};
const IMPORT_STATES={starting:'starting…',looking:'looking…',error:'couldn’t check',signed_out:'not signed in',unavailable:'couldn’t reach it'};
let importPicked=new Set(),importOpen=new Set(),importAll=false,importPending=new Set();
const importCall=(action,args,upload=false)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf,...(upload?{'X-Upload':'skill-import'}:{})},body:JSON.stringify({action,args})});
const importFrom=()=>document.querySelector('input[name="import-from"]:checked')?.value||'claude';
// How to get one out by hand, per site: what the owner clicks there (Settings > Skills > Import, Or bring one in yourself).
const IMPORT_HOW={chatgpt:'In ChatGPT: Skills, Installed, a skill’s ⋯ menu, Download. Upload the .zip here.',claude:'In Claude: Customize, Skills, open your skill and download it as a .skill file. Upload it here.'};
// The source picked above Find my skills: where it looks, and the how-to for bringing one in by hand.
function importNote(){const site=importFrom(),name=IMPORT_SITES[site];$('#import-find-note').textContent=t(state.skills?.import_local===false?'Looks in your {} account.':'Looks on this computer and in your {} account.',name);$('#import-how').textContent=IMPORT_HOW[site]}
const plural=(n,word)=>`${n} ${word}${n===1?'':'s'}`;
// After an import the row says so (with a way to see it), never "Can't import". One already here is info, with Replace
// when it is the owner's own; only a license or an OpenClaw name clash is a real "can't".
const importHere=i=>!i.done&&!i.blocked&&i.duplicate==='Already in your skills';
const importCant=i=>!i.done&&!importHere(i)&&!!(i.blocked||i.duplicate);
// What else stayed out besides scripts: named when it is one or two files, else counted.
function importLeftOut(i){const rest=(i.left_out||[]).slice(i.script_count?1:0);if(!rest.length)return '';
 const more=rest.reduce((n,e)=>{const m=/^and (\d+) more files$/.exec(e);return n+(m?+m[1]:1)},0);
 return more<=2?t('Left out: {}',rest.map(e=>e.startsWith('the end of')?'end of SKILL.md':e.replace(/ \(.*$/,'').split('/').pop()).join(', ')):t(['{} other file left out','{} other files left out'],more)}
function importRow(i){const no=importNo(i),here=importHere(i),id='imp-'+i.key.replace(/[^a-z0-9]/gi,'_').slice(-60)+i.key.length;
 const meta=[`From ${esc(i.from_label)}`,esc(i.source)];if(i.script_count)meta.push(i.depends?`Needs its ${plural(i.script_count,'script')}`:t(['{} script left out','{} scripts left out'],i.script_count));
 const out=importLeftOut(i);if(out)meta.push(esc(out));if(i.references?.length)meta.push(plural(i.references.length,'reference')+' included');if(i.licence)meta.push(esc(t('License: {}',i.licence)));
 const note=i.done?`<small class="import-ok">✓ ${esc(i.done)}</small>`:here?`<small class="import-here">Already in your skills${i.existing?.same?', unchanged':''}</small>`:no?`<small class="import-no">${esc(i.blocked||i.duplicate)}</small>`:'';
 const view=i.done?i.skill_id:here?i.existing?.id:'';
 const buttons=(i.done?'':`<button type="button" class="ghost" data-import-read="${esc(i.key)}">Read</button>`)+(view?`<button type="button" class="ghost" data-import-view="${esc(view)}">View</button>`:'')
  +(here&&i.existing?.replaceable&&!i.existing.same?`<button type="button" class="ghost" data-import-replace="${esc(i.key)}">Replace</button>`:'');
 const tick=i.done?'<span class="tick" aria-hidden="true">✓</span>':`<span class="tick"><input type="checkbox" id="${esc(id)}" value="${esc(i.key)}"${no?' disabled':''} aria-label="Import ${esc(i.name)}"></span>`;
 return `<div class="${importCant(i)?'skill-off':''}" data-import="${esc(i.key)}">${tick}<span class="grow"><strong><label for="${esc(id)}">${esc(i.name)}</label></strong><small>${esc(i.description)}</small>${i.recommended&&!no?`<small class="import-why">Recommended${i.why?': '+esc(i.why):''}</small>`:''}<small>${meta.join(' · ')}</small>${note}</span><span class="skill-buttons">${buttons}</span></div>`}
const importNo=i=>!!(i.blocked||i.duplicate||i.done);
function importSection(key,label,rows,open,count=rows.length){if(!rows.length)return '';const list=`<div class="list settings-list skills-list import-list">${rows.map(importRow).join('')}</div>`;
 return open?`<h4 class="skills-head">${label} <small class="fine">${count}</small></h4>${list}`:`<details class="import-group" data-group="${key}"${importOpen.has(key)?' open':''}><summary>${label} <small>${count}</small></summary>${list}</details>`}
function renderImport(){const v=importView,list=$('#import-list'),status=$('#import-status'),search=$('#import-search');
 if(!v){list.innerHTML='';$('#import-go').hidden=true;status.textContent='';$('#import-signin').hidden=true;search.hidden=true;return}
 const items=v.items||[],keys=new Set(items.filter(i=>!importNo(i)).map(i=>i.key));importPicked=new Set([...importPicked].filter(k=>keys.has(k)));
 const q=search.value.trim().toLowerCase();search.hidden=items.length<=IMPORT_YOURS&&!q;
 if(q){const hits=items.filter(i=>[i.name,i.description,i.source].some(x=>String(x||'').toLowerCase().includes(q))).sort((a,b)=>importNo(a)-importNo(b));
  list.innerHTML=hits.length?importSection('search',plural(hits.length,'match').replace('matchs','matches'),hits,true):'<p class="fine">No skill matches that.</p>'}
 else{const ok=items.filter(i=>!importNo(i)),rec=ok.filter(i=>i.recommended),yours=ok.filter(i=>!i.recommended&&i.group==='yours').sort((a,b)=>b.key.includes(':account:')-a.key.includes(':account:'));
  const shown=importAll?yours:yours.slice(0,IMPORT_YOURS);
  list.innerHTML=importSection('done','Imported',items.filter(i=>i.done),true)+importSection('recommended','Recommended',rec,true)+importSection('yours','Yours',shown,true,yours.length)
   +(yours.length>shown.length?`<button type="button" class="ghost import-more" id="import-all">Show all ${yours.length}</button>`:'')
   +IMPORT_GROUPS.map(([g,label])=>importSection(g,label,ok.filter(i=>!i.recommended&&i.group===g),false)).join('')
   +importSection('here','Already in your skills',items.filter(importHere),items.length<=IMPORT_YOURS)
   +importSection('no','Can’t import',items.filter(importCant),false)}
 for(const box of list.querySelectorAll('input[type=checkbox]'))box.checked=importPicked.has(box.value)&&!box.disabled;
 const notes=[],b=v.browser||{},running=v.finding?.status==='running';
 // Each place it looks, with its own state; the spinner only while one is still being read.
 const src=v.sources||[],busy=src.some(x=>IMPORT_BUSY[x.key]!==undefined&&(x.state==='starting'||x.state==='looking')),prog=$('#import-progress');
 prog.hidden=!src.length;prog.innerHTML=src.map(x=>{const on=x.state==='starting'||x.state==='looking',ok=x.state==='done';
  return `<span class="import-src ${on?'on':ok?'ok':'off'}">${on?'<i class="spin" aria-hidden="true"></i>':ok?'<b aria-hidden="true">✓</b>':''}<strong>${IMPORT_LABELS[x.key]||x.key}</strong> ${esc(ok?(x.found?`${x.found} found`:'none found'):IMPORT_STATES[x.state]||x.state)}</span>`}).join('');
 const picked=items.filter(i=>i.recommended&&!importNo(i)).length;
 // An account that gave nothing: exactly where it looked and why, and the way to bring one in by hand.
 const missed=busy?[]:src.filter(x=>IMPORT_BUSY[x.key]!==undefined&&!x.found&&x.state!=='signed_out');
 if(busy)notes.push(items.length?'Showing what’s in so far. More can still come in.':'Looking…');
 else if(running&&src.length)notes.push('Picking the ones for your work…');
 else if(src.length&&items.length)notes.push(`Found ${plural(items.length,'skill')}, ${picked||'none'} picked for your work.`);
 else if(v.finding?.status==='error')notes.push('Couldn’t check your accounts this time.');
 if(!items.length&&!busy&&!running)notes.push('No skills found.');
 for(const x of missed)notes.push(`${IMPORT_LABELS[x.key]}: looked in ${x.where?x.where.replace(/^https:\/\//,''):IMPORT_LABELS[x.key]}, ${x.detail||(x.state==='done'?'none you made yourself':IMPORT_STATES[x.state]||x.state)}.`);
 if(missed.length){$('#import-own').open=true;$('#import-how').textContent=missed.map(x=>IMPORT_HOW[x.key]).join(' ')}
 for(const e of (v.errors||[]).slice(0,3))notes.push('Skipped '+e);
 status.textContent=notes.join(' ');status.className=v.finding?.status==='error'&&!busy?'warn':'';
 // A signed-out account: a clear step to sign in on the Machine, and the search carries on there by itself.
 const out=Object.keys(IMPORT_SITES).filter(k=>b[k]==='signed_out'&&!importPending.has(k));
 $('#import-signin').innerHTML=out.map(k=>`<div><span class="grow"><strong>Sign in to ${IMPORT_SITES[k]}</strong><small>Your Machine is signed out of ${IMPORT_SITES[k]}, so your skills there aren’t listed yet.</small></span><button type="button" class="primary" data-import-signin="${k}">Sign in</button></div>`).join('');
 $('#import-signin').hidden=!out.length;
 $('#import-go').hidden=!items.some(i=>!importNo(i));importCount();
 clearTimeout(importTimer);if(running)importTimer=setTimeout(async()=>{try{importView=await importCall('skill_import_status',{token:v.token});renderImport()}
  catch(err){errCaught(err);$('#import-progress').hidden=true;$('#import-status').textContent=err.message;$('#import-status').className='warn'}},5000);
 else if(importPending.size)importLookAgain()}
function importCount(){const n=importPicked.size;$('#import-go').disabled=!n;$('#import-go').textContent=n?`Import selected (${n})`:'Import selected'}
// After signing in: the same list, and a look in just that account (once the turn that may still run is done).
async function importLookAgain(){if(!importView||importView.finding?.status==='running')return;const sites=[...importPending];importPending.clear();
 try{importView=await importCall('skill_import_find',{token:importView.token,sites});renderImport()}
 catch(err){errCaught(err);$('#import-status').textContent=err.message;$('#import-status').className='warn'}}
async function importSignin(site){try{await importCall('skill_import_signin',{site})}catch(err){errCaught(err);$('#import-status').textContent=err.message;$('#import-status').className='warn';return}
 openSignin(null,true,null,null,site,()=>{importPending.add(site);renderImport();if(importView?.finding?.status!=='running')importLookAgain()})}
const toBase64=buf=>{const bytes=new Uint8Array(buf);let out='';for(let i=0;i<bytes.length;i+=0x8000)out+=String.fromCharCode(...bytes.subarray(i,i+0x8000));return btoa(out)};
async function importUpload(data){$('#import-status').textContent='Reading it…';$('#import-status').className='';
 try{importView=await importCall('skill_import_upload',{from:importFrom(),data},true);renderImport()}catch(err){errCaught(err);$('#import-status').textContent=err.message;$('#import-status').className='warn'}}
$('#import-zip').addEventListener('change',async e=>{const f=e.target.files[0];e.target.value='';if(!f)return;
 if(f.size>6*1024*1024){$('#import-status').textContent='That file is too big (6 MB at most).';return}
 await importUpload({name:f.name,zip:toBase64(await f.arrayBuffer())})});
$('#import-folder').addEventListener('change',async e=>{const picked=[...e.target.files];e.target.value='';if(!picked.length)return;
 const files=picked.filter(f=>!(f.webkitRelativePath||f.name).split('/').some(p=>p.startsWith('.')||p==='node_modules'));let total=0;
 for(const f of files)total+=f.size;if(total>6*1024*1024){$('#import-status').textContent='That folder is too big (6 MB at most).';return}
 const root=(files[0]?.webkitRelativePath||'').split('/')[0]||'Folder';
 await importUpload({name:root,files:await Promise.all(files.slice(0,300).map(async f=>({path:f.webkitRelativePath||f.name,data:toBase64(await f.arrayBuffer())})))})});
async function importRead(key){const d=await importCall('skill_import_read',{token:importView.token,key});importShown=d;
 const notes=[[`From ${d.from_label}: ${d.source}`],d.blocked&&[d.blocked,true],(d.done||d.duplicate)&&[d.done||d.duplicate,!(d.done||d.existing)],
  d.script_count&&[d.depends?`It needs its ${plural(d.script_count,'script')} (${d.scripts.join(', ')}${d.script_count>d.scripts.length?', …':''}). Imported, it is instructions only and says so; installed in OpenClaw, its scripts come with it and your agent could run them.`:`Its ${plural(d.script_count,'script')} stay out; the instructions don’t need them.`,d.depends],
  d.references?.length&&[t('Included: {}',d.references.join(', '))],(d.left_out||[]).length&&[t('Left out: {}',d.left_out.join(', '))],
  ...(d.flags||[]).map(f=>[f,true]),d.licence&&[t('License: {}',d.licence)]];
 const no=d.blocked||d.duplicate;
 lookOpen(d.name,'What would come in, as your own skill. Read it first: it was written elsewhere.',notes,d.body,
  (no?(!d.done&&d.existing?.replaceable&&!d.existing.same?`<button type="button" class="primary" data-import-one="${esc(d.key)}" data-replace="1">Replace yours</button>`:''):`<button type="button" class="primary" data-import-one="${esc(d.key)}">Import</button>`)+(d.installable?`<button type="button" class="ghost" data-import-install="${esc(d.key)}">Install in OpenClaw with its scripts</button>`:'')+(d.url?`<a class="btn-link ghost" href="${esc(safeURL(d.url))}" target="_blank" rel="noopener">Source ↗</a>`:'')+'<button type="button" class="ghost" data-look-close>Close</button>')}
async function importRun(keys,replace=false){const v=await importCall('skill_import_run',{token:importView.token,keys,...(replace?{replace:true}:{})});for(const k of keys)importPicked.delete(k);importView=v.list;state.skills=v;skillsKey='';renderSkills();renderImport();
 const done=v.results.filter(r=>r.status==='imported'||r.status==='replaced'),skipped=v.results.filter(r=>!done.includes(r)),swapped=done.filter(r=>r.status==='replaced').length;
 const text=(done.length?`${swapped===done.length?'Replaced':'Imported'} ${plural(done.length,'skill')}. Your Machine uses ${done.length===1?'it':'them'} from now on.`:'Nothing imported.')+(skipped.length?` Skipped: ${skipped.map(r=>`${r.name||r.key} (${r.reason})`).join(', ')}.`:'');
 $('#import-status').textContent=text;$('#import-status').className='';notice(text)}
// View: the skill in your list, scrolled to and marked for a moment.
function skillShow(id){const f=$('#skills-filter');if(f&&f.value){f.value='';filterSkills()}const row=document.querySelector(`#skills-list [data-skill="${CSS.escape(id)}"]`);if(!row)return;
 row.scrollIntoView({block:'center',behavior:'smooth'});row.classList.add('skill-flash');setTimeout(()=>row.classList.remove('skill-flash'),2400)}
$('#skill-import').addEventListener('change',e=>{if(e.target.matches('#import-list input[type=checkbox]')){e.target.checked?importPicked.add(e.target.value):importPicked.delete(e.target.value);importCount()}});
$('#import-search').addEventListener('input',()=>renderImport());
$('#skill-import').addEventListener('change',e=>{if(e.target.name==='import-from')importNote()});
$('#skill-import').addEventListener('toggle',e=>{const g=e.target.dataset?.group;if(g)e.target.open?importOpen.add(g):importOpen.delete(g)},true);
$('#skill-import').addEventListener('click',async e=>{const t=e.target.closest('button');if(!t)return;
 try{if(t.id==='import-find'){t.disabled=true;$('#import-status').textContent='Looking…';$('#import-status').className='';importAll=false;importPending.clear();importView=await importCall('skill_import_find',{sites:[importFrom()]});$('#import-own').open=false;renderImport();$('#skill-import').scrollIntoView({block:'nearest'});return}
  if(t.id==='import-zip-pick')return $('#import-zip').click();
  if(t.id==='import-folder-pick')return $('#import-folder').click();
  if(t.id==='import-paste-open'){$('#import-paste').hidden=false;$('#import-paste-text').focus();return}
  if(t.id==='import-paste-go'){importView=await importCall('skill_import_paste',{from:importFrom(),text:$('#import-paste-text').value});$('#import-paste').hidden=true;$('#import-paste-text').value='';renderImport();return}
  if(t.id==='import-close'){$('#skill-import').hidden=true;clearTimeout(importTimer);return}
  if(t.dataset.importRead)return await importRead(t.dataset.importRead);
  if(t.id==='import-go'){t.disabled=true;await importRun([...importPicked]);return}
  if(t.id==='import-all'){importAll=true;renderImport();return}
  if(t.dataset.importView)return skillShow(t.dataset.importView);
  if(t.dataset.importReplace){t.disabled=true;await importRun([t.dataset.importReplace],true);return}
  if(t.dataset.importSignin)return await importSignin(t.dataset.importSignin);
 }catch(err){errCaught(err);$('#import-status').textContent=err.message;$('#import-status').className='warn'}finally{if(t.id==='import-find')t.disabled=false}});
document.addEventListener('click',async e=>{const t=e.target.closest('[data-import-one],[data-import-install]');if(!t||!importShown)return;
 try{t.disabled=true;if(t.dataset.importOne){await importRun([t.dataset.importOne],t.dataset.replace==='1');$('#skill-look').close();return}
  const v=await importCall('skill_import_install',{token:importView.token,key:importShown.key,sha:importShown.sha});importView=v.list;renderImport();installedView=v;renderInstalled();$('#skill-look').close();
  notice('Installed in OpenClaw with its scripts. It shows under Workspace.');refresh()}
 catch(err){errCaught(err);t.disabled=false;$('#skill-look-error').textContent=err.message}});
