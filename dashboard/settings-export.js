// Settings, Export (machine/app/export.py, docs/help/moving.md): the ways to take what The Machine knows somewhere else,
// one row each, and Import below them. Read when General opens (settingsSync) and every 2 s while something runs.
// EXPORT_OPTIONS is the extension point: each way out is one entry, {id, order, title, note, shown(v), actions(v),
// body(v), line(v)?, go(what, el, v)?}, where v is export_status's answer. actions() is the row's buttons, body() what
// shows under the row (both html``), line() a second line that says more than note (its state). A click on [data-export-go="<id>:<what>"] calls the option's go(what, el, v). exportOption(o) adds or
// replaces one by id; learn is an optional Learn more link after the note. Knowledge for another AI is the second entry.
var exportView=null,exportBusy=false,exportForm=false,exportTimer=null,importUp=null,importAsk=false;  // var: settingsSync may run first
const EXPORT_OPTIONS=[];
function exportOption(o){const i=EXPORT_OPTIONS.findIndex(x=>x.id===o.id);if(i>=0)EXPORT_OPTIONS[i]=o;else EXPORT_OPTIONS.push(o);
 EXPORT_OPTIONS.sort((a,b)=>(a.order||0)-(b.order||0));if(exportView)renderExport()}
const exportCall=(action,args={})=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
const exportWhen=iso=>{const d=new Date(iso);return isNaN(d)?'':d.toLocaleString(DL,{weekday:'short',month:'short',day:'numeric',hour:'numeric',minute:'2-digit'})};
const exportDay=iso=>{const d=new Date(iso);return isNaN(d)?'':d.toLocaleDateString(DL,{weekday:'short',month:'short',day:'numeric'})};
// A part as a line: its name and how many items or files it has
const exportPart=p=>html`<li><span>${t(p.label)}</span><small>${p.rows?t(['{} item','{} items'],p.rows.toLocaleString(DL)):p.files?t(['{} file','{} files'],p.files.toLocaleString(DL)):''}</small></li>`;
function exportContents(v){const parts=v.parts||[],not=v.not_exported||[];
 return html`${parts.length?html`<div class="export-detail"><strong>${t('In it')}</strong><ul class="export-parts">${parts.map(exportPart)}</ul></div>`:''}${not.length?html`<details class="export-detail export-not"><summary>${t(['Not in it: {} thing','Not in it: {} things'],not.length)}</summary><ul>${not.map(n=>html`<li><span>${t(n.what)}</span><small>${t(n.why)}</small></li>`)}</ul></details>`:''}`}

// Everything: one encrypted file to move to another computer or to keep (moving.export). Hosted: the account page makes it.
exportOption({id:'everything',order:10,title:'Everything',note:'To move to another computer, or to keep.',shown:()=>true,
 actions(v){if(v.hosted)return raw(acctGo({actions:['data'],hop:true},'data'));const e=v.export;
  if(e?.state==='running')return'';if(e?.state==='ready')return html`<a class="btn-link primary" href="${'api/export-download?id='+encodeURIComponent(e.id)}" download data-export-download>${t('Download')}</a><button type="button" class="quiet" data-export-go="everything:delete">${t('Delete')}</button>`;
  return exportForm?'':html`<button type="button" class="head-link" data-export-go="everything:form">${t(e?.state==='failed'?'Try again':'Export')}</button>`},
 line(v){const e=v.export;if(v.hosted||!e)return'';
  if(e.state==='running')return e.bytes?t('Exporting… {} so far.',e.size):t('Exporting…');
  if(e.state==='failed')return e.error;
  return t('Ready, {}. Kept until {}.',e.size,exportWhen(e.until))},
 body(v){const e=v.export;if(v.hosted)return'';
  if(exportForm&&e?.state!=='running')return html`<form class="export-form" id="export-form"><label><span>${t('Passphrase')}</span><input type="password" id="export-pass" autocomplete="new-password" minlength="10" placeholder="${t('Optional, at least 10 characters')}"></label><small>${t('Without one, you get an export code.')}</small><label class="export-check"><input type="checkbox" id="export-keys"><span>${t('Include keys and tokens')}<small>${t('Saves connecting your sources again. Needs a passphrase.')}</small></span></label><div class="actions"><button type="submit" class="primary">${t('Start export')}</button><button type="button" class="ghost" data-export-go="everything:cancel">${t('Cancel')}</button></div></form>`;
  if(e?.state!=='ready')return'';
  const code=e.code?html`<div class="export-code"><strong>${t('Export code')}</strong><code translate="no">${e.code}</code><small>${t('Write it down. The import needs it, and it isn’t shown again after a restart.')}</small></div>`:e.with_code?html`<small class="export-fine">${t('It opens with the export code shown when it was made.')}</small>`:'';
  return html`${code}${e.includes_keys?html`<small class="export-fine">${t('Keys and tokens are in it. Keep the file safe.')}</small>`:''}${exportContents(e)}`},
 async go(what){if(what==='form'||what==='cancel'){exportForm=what==='form';renderExport();if(exportForm)$('#export-pass')?.focus();return}
  if(what==='delete'){exportView=await exportCall('export_delete');renderExport()}}});
// Knowledge for another AI (machine/app/knowledge_export.py, docs/knowledge-export.md): Export opens its options,
// message text and private and Careful content, both off, and an optional passphrase. Download packs it on the Machine
// (action knowledge_export) and fetches the file once by its token; nothing is kept on the device.
var know={open:false,messages:false,private:false,note:''};
const knowSwitch=(key,title,note)=>html`<div class="export-opt"><span class="grow"><strong>${t(title)}</strong><small>${t(note)}</small></span><button type="button" class="lookup-switch" role="switch" aria-checked="${String(know[key])}" aria-label="${t(title)}" data-export-go="${'knowledge:'+key}"></button></div>`;
exportOption({id:'knowledge',order:20,title:'Knowledge for another AI',note:'People, facts, rules, how-tos and open to-dos, in plain files any AI can read.',learn:'https://themachine.computer/help/knowledge-export',shown:()=>true,
 actions:()=>html`<button type="button" class="head-link" aria-expanded="${String(know.open)}" data-export-go="knowledge:toggle">${t(know.open?'Cancel':'Export')}</button>`,
 body:()=>know.open?html`${knowSwitch('messages','Message text','Off: only where each thing came from, and when.')}${knowSwitch('private','Private and Careful','Only-you projects, private threads and Careful Fleets.')}<div class="export-opt"><span class="grow"><strong>${t('Passphrase')}</strong><small>${t('Optional. Encrypts the file, at least 10 characters.')}</small></span><input type="password" id="knowledge-pass" autocomplete="new-password" aria-label="${t('Passphrase')}"></div><div class="export-opt"><span class="grow" aria-live="polite">${know.note}</span><button type="button" data-export-go="knowledge:download">${t('Download')}</button></div>`:'',
 async go(what){if(what==='toggle'){know={...know,open:!know.open,note:''};renderExport();return}
  if(what==='messages'||what==='private'){know[what]=!know[what];renderExport();return}
  const pass=$('#knowledge-pass')?.value||'';if(pass&&pass.length<10){know.note=t('Pick a passphrase of at least {} characters, or none.',10);renderExport();return}
  know.note=t('Packing it…');renderExport();
  try{const r=await exportCall('knowledge_export',{messages:know.messages,private:know.private,passphrase:pass});
   const res=await fetch('api/knowledge-export?token='+encodeURIComponent(r.token),{cache:'no-store'});if(!res.ok)throw Error(t('That export is gone. Export it again.'));
   const a=document.createElement('a');a.href=URL.createObjectURL(await res.blob());a.download=r.name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),60000);
   if($('#knowledge-pass'))$('#knowledge-pass').value='';know.note=pass?t('Downloaded. Keep the passphrase: without it the file can’t be opened.'):t('Downloaded.')}
  catch(err){errCaught(err);know.note=err.message}renderExport()}});

function exportImport(v){const i=v.import,up=importUp;
 if(up)return html`<div><span class="grow"><strong>${t('Import')}</strong><small>${t('Uploading… {}%',up.pct)}</small></span></div>`;
 if(!i)return html`<div><span class="grow"><strong>${t('Import')}</strong><small>${t('Bring in an export from another Machine.')}</small></span><button type="button" class="head-link" data-import-pick>${t('Choose file')}</button></div>`;
 if(i.state==='uploaded')return html`<div><span class="grow"><strong>${t('Import')}</strong><small translate="no">${i.name} · ${i.size}</small></span><button type="button" class="quiet" data-import-discard>${t('Discard')}</button></div><div class="export-body"><form class="export-form" id="import-form"><label><span>${t('Passphrase or export code')}</span><input type="password" id="import-pass" autocomplete="off" required></label>${i.error?html`<small class="export-error" role="alert">${i.error}</small>`:''}<div class="actions"><button type="submit" class="primary">${t('Open')}</button></div></form></div>`;
 if(i.state==='checking')return html`<div><span class="grow"><strong>${t('Import')}</strong><small>${t('Opening and checking the export…')}</small></span></div>`;
 if(i.state==='imported'){const sends=i.sends?html`<small>${t(['{} send that was waiting is held. Nothing goes out until you send it again.','{} sends that were waiting are held. Nothing goes out until you send them again.'],i.sends)}</small>`:'',
   boards=i.boards?html`<small>${t(['Follow-ups are paused on {} board. Resume them on the board.','Follow-ups are paused on {} boards. Resume them on the board.'],i.boards)}</small>`:'';
  return html`<div data-import-done><span class="grow"><strong>${t('Imported')}</strong><small>${t('The export from {} is in place.',exportDay(i.created_at))}</small></span><button type="button" class="head-link" data-import-discard>${t('Done')}</button></div>${i.reconnect||sends||boards?html`<div class="export-body"><div class="export-detail">${i.reconnect?html`<small>${t('Some sources need you to sign in again.')}</small>`:''}${sends}${boards}</div></div>`:''}`}
 const head=html`<div><span class="grow"><strong>${t('Import')}</strong><small>${t('An export from {}, checked and ready.',exportDay(i.created_at))}</small></span>${i.state==='confirmed'?'':html`<button type="button" class="quiet" data-import-discard>${t('Discard')}</button>`}</div>`;
 const replaces=i.replaces?html`<small class="export-fine">${t('It replaces what this Machine has now. A copy of that is kept first.')}</small>`:'';
 if(i.state==='confirmed')return html`${head}<div class="export-body"><small aria-live="polite">${t(v.hosted?'Importing. The Machine restarts with it in a few minutes.':'Importing. The Machine restarts with it in a minute or two.')}</small></div>`;
 const failed=i.error?html`<small class="export-error" role="alert">${t(i.error)}</small>`:'';
 let finish;
 if(v.hosted)finish=html`<div class="export-detail">${replaces}<div class="actions"><button type="button" class="primary" data-import-confirm>${t('Import now')}</button></div><small class="export-fine">${t('The Machine restarts with it. That takes a few minutes.')}</small></div>`;
 else if(v.restart&&importAsk&&i.replaces)finish=html`<div class="export-detail export-ask" role="group" aria-label="${t('Replace with this export')}"><small>${t('It replaces what this Machine has now. A copy of that is kept first.')}</small><div class="actions"><button type="button" class="primary" data-import-confirm>${t('Replace')}</button><button type="button" class="quiet" data-import-ask="no">${t('Cancel')}</button></div></div>`;
 else if(v.restart)finish=html`<div class="export-detail">${failed}<div class="actions">${i.replaces?html`<button type="button" class="primary" data-import-ask="yes">${t('Replace with this export')}</button>`:html`<button type="button" class="primary" data-import-confirm>${t('Import now')}</button>`}</div><small class="export-fine">${t('The Machine restarts with it. That takes a minute or two.')}</small></div>`;
 else finish=html`<div class="export-detail">${failed}<small>${t('To finish, run these on this computer:')}</small><pre class="export-commands" translate="no">${(v.commands||[]).join('\n')}</pre>${replaces}</div>`;
 return html`${head}<div class="export-body">${exportContents(i)}${finish}</div>`}
function renderExport(){const box=$('#settings-export'),list=$('#export-list'),v=exportView;if(!box)return;box.hidden=false;
 if(!v){setHTML(list,html`<div><span class="grow"><small>${t('Loading…')}</small></span></div>`);return}
 const rows=EXPORT_OPTIONS.filter(o=>o.shown(v)).map(o=>{const n=o.line?.(v);
  const b=o.body(v);return html`<div data-export-option="${o.id}"><span class="grow"><strong>${t(o.title)}</strong><small>${n||t(o.note)}${o.learn&&!n?html` <a class="learn" href="${o.learn}" target="_blank" rel="noopener">${t('Learn more')}</a>`:''}</small></span>${o.actions(v)}</div>${b&&String(b)?html`<div class="export-body">${b}</div>`:''}`});
 const typed=$('#export-pass')?.value,keys=$('#export-keys')?.checked,code=$('#import-pass')?.value,kp=$('#knowledge-pass')?.value;  // a re-render keeps what was typed
 setHTML(list,html`${rows}${exportImport(v)}`);
 if(typed&&$('#export-pass'))$('#export-pass').value=typed;if(keys&&$('#export-keys'))$('#export-keys').checked=true;if(code&&$('#import-pass'))$('#import-pass').value=code;if(kp&&$('#knowledge-pass'))$('#knowledge-pass').value=kp;
 clearTimeout(exportTimer);if((v.export?.state==='running'||v.import?.state==='checking'||v.import?.state==='confirmed'&&!v.hosted)&&!$('#settings').hidden)exportTimer=setTimeout(()=>loadExport(true),v.import?.state==='confirmed'?3000:2000)}
async function loadExport(force){if(exportBusy||(!force&&exportView&&Date.now()-(exportView.at||0)<15000))return;exportBusy=true;if(!exportView)renderExport();
 try{exportView={...await exportCall('export_status'),at:Date.now()}}catch(e){if(!restartDue())errCaught(e);if(!exportView){exportBusy=false;return}}finally{exportBusy=false}renderExport()}  // restarting for an import: quiet until it answers again
const exportSet=v=>{exportView={...v,at:Date.now()};renderExport()};
$('#settings-export').addEventListener('click',async e=>{const go=e.target.closest('[data-export-go]'),el=e.target.closest('button');
 try{if(go){const [id,what]=go.dataset.exportGo.split(':');const o=EXPORT_OPTIONS.find(x=>x.id===id);if(o?.go){go.disabled=true;await o.go(what,go,exportView)}}
  else if(el?.matches('[data-import-pick]'))$('#import-file').click();
  else if(el?.matches('[data-import-discard]')){el.disabled=true;importAsk=false;exportSet(await exportCall('import_discard'))}
  else if(el?.matches('[data-import-ask]')){importAsk=el.dataset.importAsk==='yes';renderExport();$(importAsk?'.export-ask [data-import-confirm]':'[data-import-ask]')?.focus()}
  else if(el?.matches('[data-import-confirm]')){el.disabled=true;const r=await exportCall('import_confirm');importAsk=false;if(r.restarting)restartSoon();exportSet(r)}}
 catch(err){errCaught(err);notice(err.message,true);if(go||el)(go||el).disabled=false}});
$('#settings-export').addEventListener('submit',async e=>{e.preventDefault();const f=e.target,b=f.querySelector('[type=submit]');b.disabled=true;
 try{if(f.id==='export-form'){const pass=$('#export-pass').value,keys=$('#export-keys').checked;
   if(keys&&!pass)throw Error(t('Keys and tokens need a passphrase you pick.'));
   const r=await exportCall('export_start',{passphrase:pass||null,keys});exportForm=false;exportSet({...exportView,export:r.export})}
  else if(f.id==='import-form')exportSet(await exportCall('import_stage',{passphrase:$('#import-pass').value}))}
 catch(err){errCaught(err);notice(err.message,true);b.disabled=false}});
// The export file goes up as it is (never read into the page), with how far it got; the Machine writes it to disk as it comes
$('#import-file').addEventListener('change',e=>{const file=e.target.files[0];e.target.value='';if(!file)return;
 const x=new XMLHttpRequest();importUp={pct:0};renderExport();
 x.upload.onprogress=p=>{if(p.lengthComputable){importUp={pct:Math.floor(p.loaded*100/p.total)};renderExport()}};
 x.onload=()=>{importUp=null;let d=null;try{d=JSON.parse(x.responseText)}catch{}if(x.status===200&&d)exportSet(d);else{notice(d?.error||t('The upload didn’t finish. Try again.'),true);renderExport()}};
 x.onerror=()=>{importUp=null;notice(t('The upload didn’t finish. Try again.'),true);renderExport()};
 x.open('POST','api/import-upload');x.setRequestHeader('X-CSRF-Token',csrfLive||csrf);x.setRequestHeader('X-File-Name',encodeURIComponent(file.name));x.send(file)});
