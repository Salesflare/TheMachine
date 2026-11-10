// A lazy part (dashboard_parts.LAZY 'split'): graph-boards.js opens it through lazyRun('split'), nothing until it's in.
// Split up (project_split.py): a project that mixes several pieces of work becomes 2 to 4 projects. One model turn per
// click proposes them, each with a name, a line on what it is and its threads, to-dos and people; the owner renames a
// part, moves an item to another part, keeps it here or takes it off, and confirms. Only then are the projects made, on
// the same board and stage, seen by the same people. The page's "Split up on …" line, and the toast, undo it.
let spl=null;
const SPLIT_KIND={thread:'Thread',todo:'To-do',person:'Person'};
const spHead=s=>html`<div class="snooze-heading"><h2 id="split-dialog-title">${s}</h2><button type="button" data-split-close aria-label="Close">×</button></div>`;
const spWhere=k=>{const i=spl.parts.findIndex(p=>p.items.includes(k));return i>=0?'p'+i:spl.drop.includes(k)?'drop':'stay'};
const spName=(p,i)=>p.name.trim()||t('Project {}',i+1);
function spRow(k){const x=spl.items[k];if(!x)return '';const at=spWhere(k);
 return html`<li><span class="psplit-text"><small class="psplit-kind">${t(SPLIT_KIND[x.kind])}${x.probable?' · '+t('probably'):''}</small><b translate="no" title="${x.label}">${x.label}</b>${x.sub||x.at?html`<small translate="no">${[x.sub,x.at?shortDay(x.at):''].filter(Boolean).join(' · ')}</small>`:''}</span><select data-split-item="${k}" aria-label="${t('Where {} goes',x.label)}">${spl.parts.map((p,i)=>html`<option value="p${i}"${at==='p'+i?html` selected`:''}>${spName(p,i)}</option>`)}<option value="stay"${at==='stay'?html` selected`:''}>${t('Stays here')}</option>${x.probable?'':html`<option value="drop"${at==='drop'?html` selected`:''}>${t('Take off')}</option>`}</select></li>`}
const spList=keys=>keys.length?html`<ul class="psplit-items">${keys.map(spRow)}</ul>`:html`<p class="psplit-none">${t('Nothing here')}</p>`;
function spDraw(){const s=spl,f=$('#split-form');
 if(s.state==='loading'){setHTML(f,html`${spHead(t('Split up {}',s.name))}<p class="psplit-wait" role="status">${t('Reading what’s on it…')}</p><div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-split-close>Cancel</button></div>`);return}
 if(s.state==='one'){setHTML(f,html`${spHead(t('Split up {}',s.name))}<p class="ed-note">${t('It reads as one project. Nothing to split.')}</p><div class="ed-actions"><span class="grow"></span><button type="button" class="primary" data-split-close>Close</button></div>`);return}
 const all=Object.keys(s.items),stay=all.filter(k=>spWhere(k)==='stay'),drop=all.filter(k=>spWhere(k)==='drop'),n=s.parts.filter(p=>p.items.length).length;
 setHTML(f,html`${spHead(t('Split up {}',s.name))}<p class="ed-note">${t('Nothing changes until you confirm.')}</p><div class="psplit-parts">${s.parts.map((p,i)=>html`<section class="psplit-part"><label class="ed-field">${t('Project {}',i+1)}<input name="split-name" data-split-part="${i}" maxlength="60" value="${p.name}" autocomplete="off"></label>${p.about?html`<p class="psplit-about" translate="no">${p.about}</p>`:''}${spList(p.items)}</section>`)}${stay.length?html`<section class="psplit-part psplit-rest"><h3>${t('Stays on {}',s.name)}</h3>${spList(stay)}</section>`:''}${drop.length?html`<section class="psplit-part psplit-rest"><h3>${t('Taken off')}</h3>${spList(drop)}</section>`:''}</div><p class="ed-note warn" data-split-error role="alert" hidden></p><div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-split-close>Cancel</button><button class="primary"${n?'':html` disabled`}>${t(['Split into {} project','Split into {} projects'],n)}</button></div>`)}
async function spOpen(node,name){spl={node,name,state:'loading',parts:[],drop:[],items:{}};spDraw();const d=$('#split-dialog');if(!d.open)d.showModal();
 try{const r=await graphPost('project_split',{op:'propose',node_id:node});if(!spl||spl.node!==node)return;
  spl={...spl,name:r.name||name,items:r.items||{},parts:(r.parts||[]).map(p=>({name:p.name,about:p.about||'',items:[...p.items]})),state:(r.parts||[]).length?'ready':'one'};spDraw();$('#split-form [name="split-name"]')?.focus()}
 catch(err){errCaught(err);if(d.open)d.close();toast(err.message,true)}}
async function spUndo(b,id){b.disabled=true;try{const r=await graphPost('project_split',{op:'undo',split_id:+id});$('#toast').classList.remove('show');toast(t('{} is back as it was.',r.name));graphMineBoards=null;
 if(graphNode!==r.node_id){graphNode=r.node_id;history.replaceState(null,'',graphHash(r.node_id))}await people(graphNode,true)}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}}
$('#split-form').addEventListener('change',e=>{const s=e.target.closest('[data-split-item]');if(!s||!spl)return;const k=s.dataset.splitItem;
 for(const p of spl.parts)p.items=p.items.filter(x=>x!==k);spl.drop=spl.drop.filter(x=>x!==k);
 if(s.value.startsWith('p'))spl.parts[+s.value.slice(1)].items.push(k);else if(s.value==='drop')spl.drop.push(k);spDraw();$(`#split-form [data-split-item="${CSS.escape(k)}"]`)?.focus()});
$('#split-form').addEventListener('input',e=>{const i=e.target.dataset?.splitPart;if(i==null||!spl)return;spl.parts[+i].name=e.target.value;
 for(const o of $('#split-form').querySelectorAll(`option[value="p${i}"]`))o.textContent=spName(spl.parts[+i],+i)});
$('#split-form').addEventListener('click',e=>{if(e.target.closest('[data-split-close]'))$('#split-dialog').close()});
$('#split-form').addEventListener('submit',async e=>{e.preventDefault();if(!spl||spl.state!=='ready')return;const err=$('#split-form [data-split-error]'),btn=e.submitter||$('#split-form button.primary');
 const parts=spl.parts.filter(p=>p.items.length);if(parts.some(p=>!p.name.trim())){err.textContent=t('Give each new project a name.');err.hidden=false;return}
 btn.disabled=true;try{const r=await graphPost('project_split',{op:'apply',node_id:spl.node,parts:parts.map(p=>({name:p.name.trim(),about:p.about,items:p.items})),drop:spl.drop});
  $('#split-dialog').close();graphMineBoards=null;await people(graphNode,true);toast(t(['Split into {} project.','Split into {} projects.'],r.projects.length));
  $('#toast').append(htmlNodes(html` <button type="button" data-split-undo="${r.split_id}">Undo</button>`));clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),10000)}
 catch(x){errCaught(x);err.textContent=x.message;err.hidden=false;btn.disabled=false}});
$('#split-dialog').addEventListener('close',()=>{spl=null});
// On the project's page while Undo holds: what it was split into (each a link), or what it was split from
const splitLine=n=>{const s=n.split;if(!s||n.team_only)return '';const undo=html` · <button type="button" class="link" data-split-undo="${s.id}">Undo</button>`;
 return s.into?html`<p class="graph-sub psplit-line">${t('Split up on {}:',shortDay(s.at))} ${s.into.map((p,i)=>html`${i?', ':''}<button type="button" class="inline-node" data-node="${p.node_id}" translate="no">${p.name}</button>`)}${undo}</p>`
  :html`<p class="graph-sub psplit-line">${t('Split from {} on {}',s.from.name,shortDay(s.at))}${undo}</p>`};
