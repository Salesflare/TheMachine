// The Graph as a CRM (crm.py, crm_import.py). Filter each list by its own fields (crm.KIND_FILTERS; done on the Machine), an owner from the Work Fleet on each record, one organization
// with several websites (Same organization as…, Add a website…, Split off, Same organization?), and a CSV import with
// a preview and Undo. Filters are kept per list on this device.
var graphOwners=[],graphLastImport=null,crmFilters=(()=>{try{return JSON.parse(localStorage.getItem('graph-filters')||'{}')||{}}catch{return{}}})();
const crmPaneOf=list=>String(list).startsWith('projects')?'projects':list==='orgs'||list==='warmup'?'orgs':'people';
// The Team lists come whole, so their filters (who shared it, organization, state) work here, kept apart from Mine's.
var teamFilters=(()=>{try{return JSON.parse(localStorage.getItem('graph-team-filters')||'{}')||{}}catch{return{}}})();
const crmTeam=()=>!!(graphLocal&&graphListsTeam);
// a filter its list no longer has (saved before) is left out
const CRM_KEYS={people:['owner','tag','org','closeness','last_contact','open_project'],orgs:['owner','tag','industry','specialty','size','country','last_contact','open_project']};
const crmF=pane=>{const f=(crmTeam()?teamFilters:crmFilters)[pane]||{},ok=!crmTeam()&&CRM_KEYS[pane];return ok?Object.fromEntries(Object.entries(f).filter(([k])=>ok.includes(k))):f};
const viaNames=n=>String(n.via||'').replace(/^via\s+/i,'').split(/,\s*|\s+and\s+/).map(x=>x.trim()).filter(Boolean);
const teamSharers=()=>[...new Set(['people','orgs','projects','projects_done'].flatMap(k=>(graphLocal?.[k]||[]).flatMap(viaNames)))].sort((a,b)=>a.localeCompare(b));
function teamKept(list){const items=graphLocal?.[list]||[];if(!crmTeam()||list==='warmup')return items;const f=crmF(crmPaneOf(list)),v=list==='projects'?teamPickOf(items):'all';
 return items.filter(n=>(!f.by||viaNames(n).includes(f.by))&&(!f.org||String(n.org_name||n.org||'').toLowerCase().includes(f.org.toLowerCase()))&&(!f.state||n.state===f.state)&&teamHit(n,v))}
const crmQuery=list=>list==='warmup'?'':Object.entries(crmF(crmPaneOf(list))).filter(([,v])=>v!==''&&v!=null).map(([k,v])=>`&${k}=${encodeURIComponent(v)}`).join('');
const crmKey=(list,sort)=>`graph:${list}:${sort}${crmQuery(list)?':'+crmQuery(list):''}${crmTeam()&&list==='projects'?':'+teamPickOf(graphLocal?.projects||[]):''}`;  /* the team's Mine / Needs me / All is its own page */
const crmCount=pane=>Object.values(crmF(pane)).filter(v=>v!==''&&v!=null).length;
const crmSet=(pane,f)=>{const team=crmTeam(),all=team?teamFilters:crmFilters;all[pane]=Object.fromEntries(Object.entries(f).filter(([,v])=>v!==''&&v!=null));try{localStorage.setItem(team?'graph-team-filters':'graph-filters',JSON.stringify(all))}catch{}graphTabsPaint(pane);if(pane==='projects')boardRedraw()};
const crmBoards=()=>(graphMineBoards||graphBoards||[]).filter(b=>!b.team);
const ownerName=id=>id==='me'?'you':graphOwners.find(m=>m.id===id)?.name||'a teammate';
// The Mine tab is the owner's own Graph, so it has no Mine button (Filter has Owner). The Team tab's projects have
// Mine, Needs me and All, the same choice on the List and the Board.
const crmFilterButton=(pane,cls='')=>{const n=crmCount(pane);return html`<button type="button"${cls?html` class="${cls}"`:''} data-crm-filter="${pane}" aria-haspopup="dialog" aria-label="Filter"><svg class="crm-funnel" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16l-6 7.5V19l-4-2v-4.5z"/></svg><span class="crm-word">Filter</span>${n?html` <span class="badge">${n}</span>`:''}</button>`};
const crmTools=(pane,tab)=>html`<div class="graph-tools">${pane==='projects'&&tab==='projects'&&crmTeam()&&(graphLocal?.projects||[]).length?teamSeg(graphLocal.projects):''}${crmFilterButton(pane)}</div>`;
const CRM_LAST={'30':'In the last 30 days','90':'30 to 90 days ago',older:'Over 90 days ago'},CRM_SIZE={'1-10':'1 to 10','11-50':'11 to 50','51-200':'51 to 200','201-1000':'201 to 1,000','1000+':'Over 1,000'};
const countryName=c=>{try{return new Intl.DisplayNames([I18N.lang||'en'],{type:'region'}).of(String(c).toUpperCase())||c}catch{return c}};
const CRM_STATE={'heating up':'Busier lately',active:'Steady',cooling:'Quieter lately',dormant:'Quiet'};
const CRM_LABEL={waiting:()=>t('No reply in 10+ days'),by:v=>t('Shared by {}',v),state:v=>t('State: {}',t(CRM_STATE[v]||v)),owner:v=>t('Owner: {}',ownerName(v)),tag:v=>t('Tag: {}',v),board:v=>t('Board: {}',crmBoards().find(b=>String(b.id)===String(v))?.name||v),stage:v=>t('Stage: {}',v),org:v=>t('Organization: {}',v),
 value_min:v=>t('Value from {}',money(+v)),value_max:v=>t('Value up to {}',money(+v)),close_from:v=>t('Closes from {}',closeDay(v)),close_to:v=>t('Closes by {}',closeDay(v)),
 closeness:v=>t('Closeness: {}',t(CLOSENESS_UI[v]||v)),last_contact:v=>t('Last contact: {}',i18nLower(t(CRM_LAST[v]||v))),open_project:()=>t('Has an open project'),industry:v=>t('Industry: {}',v),specialty:v=>t('Specialty: {}',v),size:v=>t('Size: {}',t(CRM_SIZE[v]||v)),country:v=>t('Country: {}',countryName(v))};
const crmChips=pane=>html`${Object.entries(crmF(pane)).filter(([k,v])=>CRM_LABEL[k]&&v!=='').map(([k,v])=>html`<span class="chip">${CRM_LABEL[k](v)}</span>`)}`;
const crmActive=pane=>{const on=orEmpty(crmChips(pane));return on?html`<p class="graph-active">${on}<button type="button" class="link" data-crm-clear="${pane}">Clear</button></p>`:''};
const ownerRow=n=>kv('Owner',html`<label class="owner-pick"><select data-owner-pick="${n.id}" aria-label="Owner of ${n.name}"><option value="me"${n.owner?'':html` selected`}>You</option>${graphOwners.map(m=>html`<option value="${m.id}"${n.owner===m.id?html` selected`:''}>${m.name}</option>`)}${n.owner&&!graphOwners.some(m=>m.id===n.owner)?html`<option value="${n.owner}" selected>${n.owner_name||'Not in your Fleet now'}</option>`:''}</select></label>`);
const changeText=c=>c.field==='owner'?`Owner set to ${c.new?.id==='me'?'you':c.new?.name||'a teammate'}`:c.field==='merged'?`Merged in ${c.new?.name||''}`:c.field==='split'?`Split off ${c.new?.name||''}`:c.field==='job'?(c.old?t('Now {}, was {}',jobText(c.new),jobText(c.old)):t('Now {}',jobText(c.new))):c.field==='crm_sync'?crmSyncText(c):'Changed';
/* a new title or company LinkedIn shows (linkedin_connections.py) */
const jobText=j=>j?.title&&j?.company?t('{} at {}',j.title,j.company):j?.title||j?.company||'';
// Update contact details (crm_sync.py): what it changed in the CRM, one line per field
const crmSyncText=c=>{const n=c.new||{},crm=n.crm||'Salesforce';return n.field==='title'?`Updated the job title in ${crm} to ${n.value||''}`:n.field==='phone'?`Updated the phone in ${crm} to ${n.value||''}`:`Updated the LinkedIn link in ${crm}`};
const aliasName=a=>a.startsWith('org:named:')?a.slice(10).replace(/-/g,' '):a.slice(4);
const orgSites=n=>n.aliases?.length?html`<section class="detail-section org-sites"><h4>Websites</h4><ul>${n.domain?html`<li><span>${n.domain}</span></li>`:''}${n.aliases.map(a=>html`<li><span>${aliasName(a)}${a.startsWith('org:named:')?html` <small class="muted">(no website)</small>`:''}</span><button type="button" class="ghost" data-org-split="${a}">Split off</button></li>`)}</ul></section>`:'';
const orgDoubleAsk=n=>html`${(n.doubles||[]).slice(0,2).map(d=>{const o=d.a.id===n.id?d.b:d.a;return html`<div class="same-ask"><p class="graph-sub">Same organization as ${nodeButton(o)}?<br><span class="muted">${d.why}${o.domain?' · '+o.domain:''}</span></p>${pairSaid.has(pairKey('o',o.id,n.id))?pairDone({said:pairSaid.get(pairKey('o',o.id,n.id))}):html`<p class="graph-sub role-row"><button data-org-merge="${o.id}" data-org-into="${n.id}">Same</button><button class="ghost" data-org-apart="${n.id}" data-org-b="${o.id}">Not the same</button></p>`}</div>`})}`;
const orgDoubles=(found,items=pairsSteady('o',found))=>items.length?html`<div class="section-head"><h2>Same organization?</h2><span class="count">${items.filter(s=>!s.said).length}</span><p>Possible doubles. Merge them or keep them apart.</p></div><div class="graph-list" data-pairs="o">${items.map(s=>html`<article class="same-pair" data-pair="${pairKey('o',s.a.id,s.b.id)}"><div class="graph-row">${orgPic(s.a)}${nodeButton(s.a)}<span class="muted">and</span>${orgPic(s.b)}${nodeButton(s.b)}</div><p class="graph-sub">${s.why}${s.a.domain||s.b.domain?html` · <span class="mono">${[s.a.domain,s.b.domain].filter(Boolean).join(', ')}</span>`:''}</p>${s.said?pairDone(s):html`<p class="graph-sub role-row"><button data-org-merge="${s.b.id}" data-org-into="${s.a.id}">Merge</button><button class="ghost" data-org-apart="${s.a.id}" data-org-b="${s.b.id}">Not the same</button></p>`}</article>`)}</div>`:'';
// One dialog for the filter sheet, the import and an organization's Same as… and Add a website…
let crm=null;
const crmHead=t=>html`<div class="snooze-heading"><h2 id="crm-dialog-title">${t}</h2><button type="button" data-crm-close aria-label="Close">×</button></div>`;
const crmFoot=(ok,extra='')=>html`<p class="ed-note warn" data-crm-error role="alert" hidden></p><div class="ed-actions">${extra}<span class="grow"></span><button type="button" class="ghost" data-crm-close>Cancel</button><button class="primary">${ok}</button></div>`;
const crmShow=(wide,tall)=>{const d=$('#crm-dialog');d.classList.toggle('wide',!!wide);d.classList.toggle('tall',!!tall);if(!d.open)d.showModal()};
const crmSay=t=>{const er=$('#crm-form [data-crm-error]');if(er){er.textContent=t;er.hidden=!t}};
const opt=(v,t,on)=>html`<option value="${v}"${on?html` selected`:''}>${t}</option>`;
function crmStages(board,current){const bs=crmBoards(),pick=bs.find(b=>String(b.id)===String(board)),names=[...new Set((pick?[pick]:bs).flatMap(b=>(b.stages||[]).map(s=>s.name)))];return html`${opt('','Any stage',!current)}${names.map(s=>opt(s,s,s===current))}`}
function crmFilterOpen(pane){const f=crmF(pane);crm={mode:'filter',pane};
 if(crmTeam()){setHTML($('#crm-form'),html`${crmHead(t('Filter the team’s {}',i18nLower(t(GRAPH_TABS[pane].label))))}<label class="ed-field">Shared by<select name="by">${opt('','Anyone',!f.by)}${teamSharers().map(m=>opt(m,m,f.by===m))}</select></label>${pane==='people'?html`<label class="ed-field">Organization<input name="org" value="${f.org||''}" placeholder="Name or website" autocomplete="off"></label>`:''}${pane==='projects'?html`<label class="ed-field">State<select name="state">${opt('','Any state',!f.state)}${Object.entries(CRM_STATE).map(([k,t])=>opt(k,t,f.state===k))}</select></label>`:''}${crmFoot('Show results',html`<button type="button" class="ghost" data-crm-clear-all>Clear all</button>`)}`);return crmShow()}
 const pick=(name,label,choices,any='Any')=>html`<label class="ed-field">${label}<select name="${name}">${opt('',any,!f[name])}${choices.map(([v,l])=>opt(v,l,String(f[name]??'').toLowerCase()===String(v).toLowerCase()))}</select></label>`,
  box=(name,label,ph,x='')=>html`<label class="ed-field">${label}<input name="${name}" value="${f[name]??''}" placeholder="${ph}" autocomplete="off"${x}></label>`,
  owner=graphOwners.length?pick('owner','Owner',[['me','You'],...graphOwners.map(m=>[m.id,m.name])],'Anyone'):'',
  tag=graphTags.length?pick('tag','Tag',graphTags.map(x=>[x.tag,x.tag]),'Any tag'):'',
  org=box('org','Organization','Name or website'),
  last=pick('last_contact','Last contact',Object.entries(CRM_LAST).map(([v,l])=>[v,t(l)])),
  open=html`<label class="ed-check"><input type="checkbox" name="open_project" value="1"${f.open_project?html` checked`:''}> Has an open project</label>`,
  fields=pane==='people'?html`<div class="ed-row3">${pick('closeness','Closeness',Object.entries(CLOSENESS_UI).map(([v,l])=>[v,t(l)]))}${last}</div>${org}${owner}${tag}${open}`
  :pane==='orgs'?html`${box('industry','Industry','Any industry',html` maxlength="200"`)}${box('specialty','Specialty','Any specialty',html` maxlength="200"`)}<div class="ed-row3">${pick('size','Size',Object.entries(CRM_SIZE).map(([v,l])=>[v,t(l)]))}${last}</div>${graphCountries.length?pick('country','Country',graphCountries.map(c=>[c,countryName(c)]).sort((a,b)=>a[1].localeCompare(b[1]))):''}${owner}${tag}${open}`
  :html`${owner}${crmBoards().length?html`<div class="ed-row3">${pick('board','Board',crmBoards().map(b=>[b.id,b.name]),'Any board')}<label class="ed-field">Stage<select name="stage">${crmStages(f.board,f.stage)}</select></label></div>`:''}${tag}${org}<div class="ed-row3">${box('value_min','Value from','Any',html` inputmode="decimal"`)}${box('value_max','Value up to','Any',html` inputmode="decimal"`)}</div><div class="ed-row3"><label class="ed-field">Closes from<input name="close_from" type="date" value="${f.close_from||''}"></label><label class="ed-field">Closes by<input name="close_to" type="date" value="${f.close_to||''}"></label></div><label class="ed-check"><input type="checkbox" name="waiting" value="1"${f.waiting?html` checked`:''}> No reply in 10+ days</label>`;
 setHTML($('#crm-form'),html`${crmHead(t('Filter {}',i18nLower(t(GRAPH_TABS[pane].label))))}${fields}${crmFoot('Show results',html`<button type="button" class="ghost" data-crm-clear-all>Clear all</button>`)}`);
 crmShow()}
async function crmImportOpen(pane){crm={mode:'import',kind:pane==='projects'?'project':pane==='orgs'?'org':'person',text:'',name:'',mapping:null,seen:null,check:null,own:false,typeOff:new Set(),fixOff:new Set(),fixOpen:false};crmImportDraw()}
const CRM_FIX_TYPES=['spaces','case','split','email','phone','website','date','value','tags','stage','merge'];
const crmFixArgs=c=>({fixes:{types:c.typeOff.size?CRM_FIX_TYPES.filter(t=>!c.typeOff.has(t)):'all',off:[...c.fixOff]},...(c.check?.state==='done'?{ai_run:c.check.id}:{})});
function crmKept(s,c){const on=(s.fix_types||[]).filter(t=>!c.typeOff.has(t.type));return on.reduce((n,t)=>n+t.count,0)-(s.fixes||[]).filter(f=>c.fixOff.has(f.id)&&!c.typeOff.has(f.type)).length}
function crmFixesHtml(s,c){const by={};for(const f of s.fixes||[])(by[f.type]=by[f.type]||[]).push(f);
 return html`<fieldset><legend>Fixes</legend><div class="crm-fixes">${(s.fix_types||[]).map(t=>html`<details class="crm-fixtype"${c.fixOpen===t.type?html` open`:''} data-type="${t.type}"><summary><input type="checkbox" data-crm-fixtype="${t.type}" aria-label="${t.name}"${c.typeOff.has(t.type)?'':html` checked`}><span>${t.name} <small>${t.count}</small></span></summary><ul>${(by[t.type]||[]).map(f=>html`<li><label><input type="checkbox" data-crm-fix="${f.id}"${c.typeOff.has(t.type)?html` disabled`:''}${c.fixOff.has(f.id)?'':html` checked`}><span class="ba"><s>${f.before}</s> → ${f.after}</span><small>Line ${f.line}${f.field==='row'?'':' · '+f.field_name}${f.ai?' · your model':''}${f.why?': '+f.why:''}</small></label></li>`)}${(by[t.type]||[]).length<t.count?html`<li><small>and ${t.count-(by[t.type]||[]).length} more like these</small></li>`:''}</ul></details>`)}</div></fieldset>`}
function crmImportDraw(){const c=crm,s=c.seen,n=s?s.counts.new+s.counts.match:0,STATUS={new:'New',match:'Matches',skip:'Skipped'},kept=s?crmKept(s,c):0,ck=c.check?.state;
 setHTML($('#crm-form'),html`${crmHead('Import CSV')}<div class="ed-row3"><label class="ed-field">What is in it<select name="kind">${opt('person','People',c.kind==='person')}${opt('org','Organizations',c.kind==='org')}${opt('project','Projects',c.kind==='project')}</select></label><div class="ed-field">File<label class="crm-file"><input name="file" type="file" accept=".csv,.tsv,.txt,text/csv"><span class="crm-file-name">${c.name?c.name:'Choose file'}</span>${c.name?html`<span class="crm-file-change">· <u>Change</u></span>`:''}</label></div></div>${c.name?'':html`<p class="ed-note">A spreadsheet saved as CSV, with a row of headers. It stays on your Machine.</p>`}${ck==='checking'?html`<p class="crm-ai run" role="status">Your model is checking the columns…</p>`:ck==='done'&&s?.ai?html`<p class="crm-ai" role="status">Checked by your model. Change anything below.</p>`:ck==='failed'?html`<p class="crm-ai" role="status">Your model couldn’t check it this time; the columns are guessed from their headers.</p>`:''}${s?html`${s.problem?(ck==='checking'?'':html`<p class="crm-problem">${s.problem}.</p>`):html`<p class="crm-count"><b>${s.counts.new}</b> new · <b>${s.counts.match}</b> match existing · <b>${s.counts.skip}</b> skipped</p>`}${s.fix_total?html`<p class="crm-fixline"><span><b>${s.fix_total} ${s.fix_total===1?'fix':'fixes'} suggested</b>${kept!==s.fix_total?html`, ${kept} kept`:''}</span>·<button type="button" class="link" data-crm-fixes aria-expanded="${!!c.fixOpen}">${c.fixOpen?'Hide':'Review'}</button></p>${c.fixOpen?crmFixesHtml(s,c):''}`:''}<fieldset><legend>Columns</legend><div class="crm-cols">${s.columns.map(col=>html`<div class="crm-col"><span><b title="${col.header}">${col.header}</b><small>${col.samples.join(' · ')||'empty'}</small></span><select data-crm-col="${col.index}" aria-label="${col.header} goes to">${opt('','Skip',!col.field)}${s.fields.map(f=>opt(f.id,f.name,col.field===f.id))}</select>${col.reason?html`<small class="crm-why">${col.reason}</small>`:''}</div>`)}</div></fieldset>${s.problem?'':html`<fieldset><legend>Rows${s.total>s.rows.length?` (first ${s.rows.length} of ${s.total})`:''}</legend><ul class="crm-rows">${s.rows.map(r=>html`<li><span class="n">${r.record.name||r.record.email||'(no name)'}</span><span class="st ${r.status}">${STATUS[r.status]}${r.status==='match'&&r.match_name?' '+r.match_name:''}${r.status==='skip'?': '+(r.why||''):''}</span></li>`)}</ul></fieldset>`}<p class="ed-note">Matches get what the file says; empty cells change nothing. You can undo the last import.</p>`:''}${crmFoot(s?(n?`Import ${n}${kept?` with ${kept} ${kept===1?'fix':'fixes'}`:''}`:'Nothing to import'):'Import')}`);
 const ok=$('#crm-form button.primary');ok.disabled=!n;crmShow(!!(s||c.name),!!c.name)}
const crmUpload=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf,'X-Upload':'graph-import'},body:JSON.stringify({action,args})});
async function crmPreview(){const c=crm;if(!c?.text)return;crmSay('');const seq=c.seq=(c.seq||0)+1;
 try{const s=await crmUpload('graph_import_preview',{kind:c.kind,text:c.text,...(c.mapping?{mapping:c.mapping}:{}),...crmFixArgs(c)});if(crm===c&&seq===c.seq){c.seen=s;crmImportDraw()}}catch(x){errCaught(x);if(seq!==c.seq)return;c.seen=null;crmImportDraw();crmSay(x.message)}}
// The owner's own model looks at the columns and the cells the rules can't read (headers and a few values, on their
// Machine); the rules' guess shows meanwhile, and stays when the model can't run now.
async function crmCheck(){const c=crm;if(!c?.text)return;c.check=null;const key=c.kind+c.text;
 try{const r=await crmUpload('graph_import_ai',{kind:c.kind,text:c.text});if(crm!==c||c.kind+c.text!==key||!r.ai)return;c.check={id:r.run_id,state:'checking'};crmImportDraw();
  for(let i=0;i<120&&crm===c&&c.check?.id===r.run_id;i++){await new Promise(ok=>setTimeout(ok,i<10?1500:3000));if(crm!==c||c.check?.id!==r.run_id)return;
   const st=await graphPost('graph_import_ai_status',{run_id:r.run_id});if(st.status==='starting'||st.status==='running')continue;
   c.check.state=st.status==='ok'?'done':'failed';if(c.check.state==='done'&&!c.own)c.mapping=null;return c.check.state==='done'?crmPreview():crmImportDraw()}
  if(crm===c&&c.check?.id===r.run_id){c.check.state='failed';crmImportDraw()}}catch{if(crm===c&&c.check?.state==='checking'){c.check.state='failed';crmImportDraw()}}}
function crmOrgOpen(mode){const name=$('#people-view .graph-detail>.name-row h3')?.textContent||'';crm={mode,id:graphNode,name,found:new Map()};
 setHTML($('#crm-form'),mode==='org-same'?html`${crmHead('Same organization as…')}<p class="ed-note">${name} and the one you pick become one organization, with their people, projects and notes. Split off undoes it.</p><label class="ed-field">Which organization?<input name="q" list="crm-orgs" placeholder="A name from your Graph" autocomplete="off" maxlength="100"></label><datalist id="crm-orgs"></datalist>${crmFoot('Merge')}`
  :html`${crmHead('Add a website')}<p class="ed-note">One more website of ${name}, like its .io next to its .com. People with an address there join it.</p><label class="ed-field">Website<input name="website" inputmode="url" placeholder="acme.io" autocomplete="off" maxlength="200"></label>${crmFoot('Add')}`);
 crmShow();$('#crm-form input').focus()}
async function crmOrgSearch(q){const seq=crmOrgSearch.seq=(crmOrgSearch.seq||0)+1;if(q.length<2)return;try{const r=await request('api/graph?q='+encodeURIComponent(q));if(seq!==crmOrgSearch.seq||!crm)return;
 const orgs=(r.found||[]).filter(n=>n.kind==='org'&&n.id!==crm.id);for(const o of orgs)crm.found.set(o.name.toLowerCase(),o.id);setHTML($('#crm-orgs'),html`${orgs.map(o=>html`<option value="${o.name}">${o.domain||''}</option>`)}`)}catch{}}
const crmAfter=async(id)=>{graphMineBoards=null;pagerDrop('graph');if(id&&graphNode&&id!==graphNode)return graphOpen(id);await people(graphNode,true)};
$('#crm-form').addEventListener('click',e=>{if(e.target.closest('[data-crm-close]'))$('#crm-dialog').close();
 if(e.target.closest('[data-crm-fixes]')&&crm?.mode==='import'){crm.fixOpen=!crm.fixOpen;crmImportDraw()}
 const sum=e.target.closest('.crm-fixtype>summary');if(sum&&crm?.mode==='import'&&!e.target.closest('input')){e.preventDefault();const t=sum.parentElement.dataset.type;crm.fixOpen=crm.fixOpen===t?true:t;crmImportDraw()}
 if(e.target.closest('[data-crm-clear-all]')&&crm?.mode==='filter'){crmSet(crm.pane,{});$('#crm-dialog').close()}
 if(e.target.closest('[data-crm-clear-all]')&&crm?.mode==='board-stages'){const n=crm.board;$('#crm-dialog').close();boardStagesSet(n,null)}});
$('#crm-form').addEventListener('change',e=>{const c=crm;if(!c)return;
 if(c.mode==='filter'&&e.target.name==='board'){const st=$('#crm-form select[name=stage]');if(st)setHTML(st,crmStages(e.target.value,''))}
 if(c.mode!=='import')return;
 const fresh=()=>{c.mapping=null;c.own=false;c.check=null;c.typeOff.clear();c.fixOff.clear();crmPreview();crmCheck()};
 if(e.target.name==='kind'){c.kind=e.target.value;return fresh()}
 if(e.target.name==='file'){const file=e.target.files?.[0];if(!file)return;if(file.size>8*1024*1024)return crmSay('That file is too big: up to 8 MB.');
  const r=new FileReader();r.onload=()=>{c.text=String(r.result||'');c.name=file.name;fresh()};r.onerror=()=>crmSay('Couldn’t read that file.');r.readAsText(file);return}
 if(e.target.dataset.crmFixtype){c.typeOff[e.target.checked?'delete':'add'](e.target.dataset.crmFixtype);return crmPreview()}
 if(e.target.dataset.crmFix){c.fixOff[e.target.checked?'delete':'add'](e.target.dataset.crmFix);return crmPreview()}
 if(e.target.dataset.crmCol!=null){c.own=true;c.mapping=Object.fromEntries([...$('#crm-form').querySelectorAll('[data-crm-col]')].map(s=>[s.dataset.crmCol,s.value]).filter(([,v])=>v));crmPreview()}});
$('#crm-form').addEventListener('input',e=>{if(crm&&e.target.type!=='file')crmSay('');  /* an error goes once the owner changes what it was about */
 if(crm?.mode==='org-same'&&e.target.name==='q')crmOrgSearch(e.target.value.trim())});
$('#crm-form').addEventListener('submit',async e=>{e.preventDefault();const c=crm,f=e.target;if(!c)return;const v=k=>String(f.elements[k]?.value||'').trim(),btn=f.querySelector('button.primary');crmSay('');
 if(c.mode==='picture')return;
 if(c.mode==='board-stages'){const on=[...f.querySelectorAll('input[name=stage]:checked')].map(x=>x.value);if(!on.length)return crmSay('Pick at least one stage.');const all=f.querySelectorAll('input[name=stage]').length;$('#crm-dialog').close();return boardStagesSet(c.board,on.length===all?null:on)}
 if(c.mode==='fields'){btn.disabled=true;try{await crmFieldsSave(c)}catch(x){errCaught(x);crmSay(x.message)}finally{btn.disabled=false}return}
 if(c.mode==='filter'){const next=Object.fromEntries([...f.elements].filter(x=>x.name&&x.type!=='checkbox').map(x=>[x.name,x.value.trim()]));
  for(const k of ['waiting','open_project'])next[k]=f.elements[k]?.checked?'1':'';
  for(const k of ['value_min','value_max'])if(next[k]&&!/^\d+([.,]\d+)?$/.test(next[k].replace(/[\s€$£]/g,'')))return crmSay('Value: a number, like 12000.');
  crmSet(c.pane,next);$('#crm-dialog').close();return}
 btn.disabled=true;
 try{if(c.mode==='import'){const r=await crmUpload('graph_import_run',{kind:c.kind,text:c.text,name:c.name,...(c.mapping?{mapping:c.mapping}:{...(c.seen?{mapping:Object.fromEntries(c.seen.columns.filter(x=>x.field).map(x=>[x.index,x.field]))}:{})}),...crmFixArgs(c)});$('#crm-dialog').close();
   toast(`Imported: ${r.new} new, ${r.updated} updated${r.skipped?`, ${r.skipped} skipped`:''}.`);$('#toast').append(htmlNodes(html` <button data-crm-undo-import="${r.import_id}" data-now>Undo</button>`));clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),15000);
   return crmAfter()}
  if(c.mode==='org-same'){const id=c.found.get(v('q').toLowerCase());if(!id)return crmSay('Pick an organization from the list.');
   const r=await graphPost('graph_org_merge',{node_id:c.id,into:id});$('#crm-dialog').close();toast('Merged. Split off undoes it.');return crmAfter(r.node_id)}
  if(c.mode==='org-site'){if(!v('website'))return crmSay('Type a website, like acme.io.');const r=await graphPost('graph_org_merge',{node_id:c.id,website:v('website')});$('#crm-dialog').close();toast('Added.');return crmAfter(r.node_id)}}
 catch(x){errCaught(x);crmSay(x.message)}finally{btn.disabled=false}});
$('#crm-dialog').addEventListener('close',e=>{if(!e.currentTarget.open)crm=null});
document.addEventListener('click',async e=>{const t=e.target.closest('[data-crm-filter],[data-crm-clear],[data-crm-import],[data-crm-undo-import],[data-org-split],[data-org-merge],[data-org-apart],[data-org-same],[data-org-site],[data-crm-waiting]');if(!t)return;
 e.preventDefault();e.stopPropagation();t.closest('details')?.removeAttribute('open');
 if(t.dataset.crmFilter)return crmFilterOpen(t.dataset.crmFilter);
 if(t.dataset.crmClear)return crmSet(t.dataset.crmClear,{});
 if(t.dataset.crmImport)return crmImportOpen(t.dataset.crmImport);
 if(t.hasAttribute('data-crm-waiting')){const f={...crmF('projects')};if(f.waiting)delete f.waiting;else f.waiting='1';return crmSet('projects',f)}
 if(t.hasAttribute('data-org-same'))return crmOrgOpen('org-same');
 if(t.hasAttribute('data-org-site'))return crmOrgOpen('org-site');
 t.disabled=true;let gone=null;
 try{if(t.dataset.crmUndoImport){if(!t.hasAttribute('data-now')&&!confirm('Undo the last import? What it added goes, and what it changed goes back.'))return;$('#toast').classList.remove('show');
   await graphPost('graph_import_undo',{import_id:+t.dataset.crmUndoImport});toast('Import undone.');return crmAfter()}
  if(t.dataset.orgSplit){await graphPost('graph_org_split',{alias:t.dataset.orgSplit});toast('Split off.');return crmAfter()}
  // Same organization?: the answer shows on the pair at once and stays (pairAnswer); its people and projects follow in the background rebuild
  if(t.dataset.orgMerge||t.dataset.orgApart)gone=pairAnswer(t.closest('.same-pair,.same-ask'),t.dataset.orgMerge?pairKey('o',t.dataset.orgMerge,t.dataset.orgInto):pairKey('o',t.dataset.orgApart,t.dataset.orgB),t.dataset.orgMerge?'Merged.':'Kept apart.');
  if(t.dataset.orgMerge){const r=await graphPost('graph_org_merge',{node_id:t.dataset.orgMerge,into:t.dataset.orgInto});toast('Merged. Split off undoes it.');return crmAfter(graphNode?r.node_id:null)}
  if(t.dataset.orgApart){await graphPost('graph_org_apart',{a:t.dataset.orgApart,b:t.dataset.orgB});toast('Kept apart.');return crmAfter()}}
 catch(err){errCaught(err);if(gone)gone();toast(err.message,true)}finally{t.disabled=false}},true);
document.addEventListener('change',async e=>{const t=e.target.closest?.('[data-owner-pick]');if(!t)return;t.disabled=true;
 try{await graphPost('graph_owner',{node_id:t.dataset.ownerPick,owner:t.value});toast(t.value==='me'?'You own it.':`${ownerName(t.value)} owns it.`);graphMineBoards=null;await people(graphNode,true)}catch(err){errCaught(err);toast(err.message,true)}finally{t.disabled=false}});

// Pipeline on a board: what is open per stage and what is expected to close per month, from each project's value and
// expected close date (the projects on the board as shown, so Mine counts only the owner's own). One series, so one
// color; every bar carries its label and value as text.
const pipeMonth=k=>{const d=new Date(Math.floor(k/12),k%12,1),y=d.getFullYear()!==new Date().getFullYear();return localeDate(d,DL,{month:'short',...(y?{year:'numeric'}:{})})};
const pipeRow=(label,value,n,max,cls='')=>html`<div class="pipe-row${cls}" title="${label}: ${moneyFull(value)} in ${n} project${n===1?'':'s'}"><span class="pipe-k ell">${label}</span><span class="pipe-bar" aria-hidden="true">${value>0?html`<i style="width:${Math.max(2,Math.round(value/max*100))}%"></i>`:''}</span><span class="pipe-v">${money(value)} <small>${n}</small></span></div>`;
function pipeline(b){if(!b.projects.some(p=>p.value!=null))return '';
 // Open is what can still close: not won or lost, not in the last stage (where Won puts it) nor Stalled or declined
 const main=b.stages.filter(s=>!s.side),wonStage=main.length>1?main.at(-1).name:null,side=new Set(b.stages.filter(s=>s.side).map(s=>s.name));
 const won=p=>p.outcome==='won'||p.stage===wonStage,ps=b.projects.filter(p=>!p.outcome&&!won(p)&&!side.has(p.stage));
 const sum=a=>a.reduce((t,p)=>t+(p.value||0),0),total=sum(ps),now=new Date(),m0=now.getFullYear()*12+now.getMonth();
 const key=d=>{const [y,m]=String(d).split('-').map(Number);return y*12+m-1};
 const wonNow=b.projects.filter(p=>won(p)&&p.value!=null&&p.at&&key(String(p.at).slice(0,7))===m0);
 const stages=main.filter(s=>s.name!==wonStage).map(s=>{const it=ps.filter(p=>p.stage===s.name);return [s.name,sum(it),it.length]});
 const months=new Map(),over=[0,0],none=[0,0],later=[0,0];
 for(const p of ps){const v=p.value||0;if(p.value==null)continue;if(!p.close_date){none[0]+=v;none[1]++;continue}const k=key(p.close_date);
  if(k<m0){over[0]+=v;over[1]++}else if(k>m0+11){later[0]+=v;later[1]++}else{const x=months.get(k)||[0,0];x[0]+=v;x[1]++;months.set(k,x)}}
 const last=Math.max(m0+2,...months.keys()),monthRows=[];for(let k=m0;k<=last;k++){const x=months.get(k)||[0,0];monthRows.push([pipeMonth(k),x[0],x[1]])}
 const max1=Math.max(1,...stages.map(s=>s[1])),max2=Math.max(1,over[0],later[0],...monthRows.map(m=>m[1]));
 return html`<details class="pipeline"${sideStore.get('board-pipeline')==='0'?'':html` open`}><summary><b>Pipeline</b> <span>${money(total)} open in ${ps.filter(p=>p.value!=null).length} with a value</span> ${wonNow.length?html`<span class="pipe-won">Won this month: ${money(sum(wonNow))} in ${wonNow.length}</span>`:''}</summary><div class="pipe-grid"><div class="pipe-block"><h5>Open by stage</h5>${stages.map(s=>pipeRow(s[0],s[1],s[2],max1))}</div><div class="pipe-block"><h5>Expected to close</h5>${over[1]?pipeRow('Overdue',over[0],over[1],max2,' over'):''}${monthRows.map(m=>pipeRow(m[0],m[1],m[2],max2))}${later[1]?pipeRow('Later',later[0],later[1],max2):''}${none[1]?html`<p class="pipe-note">No close date: ${money(none[0])} in ${none[1]}</p>`:''}</div></div></details>`}
document.addEventListener('click',e=>{const d=e.target.closest?.('.pipeline>summary')?.parentElement;if(d)sideStore.set('board-pipeline',d.open?'0':'1')});  /* the owner's pick, not a redraw's */

// Fields and tags (crm_fields.py): the owner's own fields per record type (text, number, date, a choice) and tags.
var graphFields=[],graphTags=[],graphCountries=[];
const FIELD_KIND={person:'people',org:'organizations',project:'projects'};
const fieldShow=f=>f.value==null||f.value===''?html`<span class="muted">Not set</span>`:f.type==='number'?new Intl.NumberFormat().format(+f.value):f.type==='date'?closeDay(f.value):f.value;
const tagMini=n=>n.tags?.length?html`<span class="tag-mini">${n.tags.slice(0,3).map(t=>html`<span class="chip tag-chip">${t}</span>`)}${n.tags.length>3?html`<span class="muted">+${n.tags.length-3}</span>`:''}</span>`:'';
const tagChips=(tags,node)=>html`${(tags||[]).map(t=>html`<span class="chip tag-chip">${t}${node?html`<button type="button" data-tag-remove="${t}" data-tag-node="${node}" aria-label="Remove the tag ${t}">×</button>`:''}</span>`)}`;
const tagsPaint=()=>{const l=$('#crm-tag-list');if(l)setHTML(l,html`${graphTags.map(t=>html`<option value="${t.tag}"></option>`)}`)};
function crmFieldsSection(n){if(n.team_only)return (n.team_fields?.length||n.tags?.length)?html`<section class="detail-section crm-fields"><h4>Fields</h4>${(n.team_fields||[]).map(f=>kv(f.name,fieldShow(f)))}${n.tags?.length?kv('Tags',html`<span class="tag-list">${tagChips(n.tags)}</span>`):''}</section>`:'';
 const fs=n.fields||[],mine=new Set(fs.filter(f=>f.value!=null).map(f=>f.name.toLowerCase())),team=(n.team?.fields||[]).filter(f=>!mine.has(String(f.name).toLowerCase()));
 fieldsOf.set(n.id,fs);
 return html`<section class="detail-section crm-fields"><h4>Fields</h4>${fs.map(f=>kv(f.name,html`<button type="button" class="field-val" data-field-edit="${f.id}" data-field-node="${n.id}" title="Change ${f.name}">${fieldShow(f)}</button>`))}${team.map(f=>kv(f.name,html`${fieldShow(f)}<span class="sub">From your team</span>`))}${kv('Tags',html`<span class="tag-list">${tagChips(n.tags,n.id)}<span class="tag-add" data-tag-node="${n.id}"><input name="tag" list="crm-tag-list" placeholder="+ Tag" maxlength="40" aria-label="Add a tag" enterkeyhint="done" autocomplete="off"></span></span>`)}<p class="graph-sub fields-foot">${n.kind==='person'&&!n.birthday?html`<button type="button" class="link" data-bday-add="${n.id}">${t('Add birthday')}</button>`:''}<button type="button" class="link" data-fields-edit="${n.id}">${fs.length?'Manage fields':'Add a field'}</button></p></section>`}
const fieldInput=(f,v)=>f.type==='choice'?html`<select name="f${f.id}">${opt('','Not set',v==null||v==='')}${(f.choices||[]).map(c=>opt(c,c,c===v))}</select>`
 :f.type==='date'?html`<input name="f${f.id}" type="date" value="${v||''}">`
 :f.type==='number'?html`<input name="f${f.id}" inputmode="decimal" value="${v??''}" autocomplete="off">`
 :html`<input name="f${f.id}" value="${v??''}" maxlength="500" autocomplete="off">`;
async function crmFieldsOpen(node,keep){const n=await request('api/graph?node='+encodeURIComponent(node));const c={mode:'fields',node:n.id,kind:n.kind,name:n.name,fields:n.fields||[],draft:keep||{}};crm=c;
 const fs=c.fields,val=f=>f.id in c.draft?c.draft[f.id]:f.value;
 setHTML($('#crm-form'),html`${crmHead(t('Fields of {}',n.name))}${fs.length?fs.map(f=>html`<div class="crm-field-row"><label class="ed-field">${f.name}${fieldInput(f,val(f))}</label><button type="button" class="link" data-nf-remove="${f.id}" aria-label="Remove the field ${f.name}">Remove</button></div>`)
   :html`<p class="ed-note">No fields for ${FIELD_KIND[n.kind]} yet. A field you add shows on every one of them.</p>`}<details class="crm-newfield"${fs.length?'':html` open`}><summary>New field for ${FIELD_KIND[n.kind]}</summary><div class="ed-row3"><label class="ed-field">Name<input name="nf_name" maxlength="40" autocomplete="off" placeholder="Renewal date"></label><label class="ed-field">Type<select name="nf_type">${opt('text','Text',1)}${opt('number','Number')}${opt('date','Date')}${opt('choice','Choice')}</select></label></div><label class="ed-field" data-nf-choices hidden>Choices<textarea name="nf_choices" rows="3" placeholder="One per line"></textarea></label><p><button type="button" class="ghost" data-nf-add>Add field</button></p></details>${crmFoot('Save')}`);crmShow()}
const crmDraft=()=>Object.fromEntries(((crm?.fields)||[]).map(f=>[f.id,String($('#crm-form').elements['f'+f.id]?.value??'')]));
$('#crm-form').addEventListener('click',async e=>{const c=crm;if(c?.mode!=='fields')return;const add=e.target.closest('[data-nf-add]'),rm=e.target.closest('[data-nf-remove]');if(!add&&!rm)return;e.preventDefault();
 const f=$('#crm-form'),draft=crmDraft();crmSay('');
 try{if(add){add.disabled=true;await graphPost('graph_field_save',{kind:c.kind,name:f.elements.nf_name.value,type:f.elements.nf_type.value,choices:f.elements.nf_choices.value})}
  else{const field=c.fields.find(x=>String(x.id)===rm.dataset.nfRemove);if(!confirm(`Remove the field ${field?.name||''} from every one of your ${FIELD_KIND[c.kind]}? What it holds goes too.`))return;await graphPost('graph_field_delete',{id:+rm.dataset.nfRemove});delete draft[rm.dataset.nfRemove]}
  graphFieldsStale=true;await crmFieldsOpen(c.node,draft)}catch(x){errCaught(x);crmSay(x.message);if(add)add.disabled=false}});
$('#crm-form').addEventListener('change',e=>{if(crm?.mode==='fields'&&e.target.name==='nf_type')$('#crm-form [data-nf-choices]').hidden=e.target.value!=='choice'});
var graphFieldsStale=false;
// A field's value changes in place: click it, change it, Enter or Save keeps it, Escape puts it back, Remove empties it.
const fieldsOf=new Map();
function fieldEditOpen(b){const f=(fieldsOf.get(b.dataset.fieldNode)||[]).find(x=>String(x.id)===b.dataset.fieldEdit);if(!f)return;
 const w=document.createElement('span');w.className='field-inline';w.dataset.fieldNode=b.dataset.fieldNode;w.dataset.fieldId=f.id;
 setHTML(w,html`${fieldInput(f,f.value)}<button type="button" class="primary" data-field-save>Save</button><button type="button" class="ghost" data-field-cancel>Cancel</button>${f.value==null||f.value===''?'':html`<button type="button" class="link" data-field-clear>Remove</button>`}`);
 b.replaceWith(w);const i=w.querySelector('input,select');i.setAttribute('aria-label',f.name);i.focus();i.select?.()}
async function fieldEditSave(w,value){if(w.dataset.busy)return;const f=(fieldsOf.get(w.dataset.fieldNode)||[]).find(x=>String(x.id)===w.dataset.fieldId);const v=String(value??'').trim();
 if(f&&v===String(f.value??''))return people(graphNode,true);w.dataset.busy='1';w.querySelectorAll('button,input,select').forEach(x=>x.disabled=true);
 try{await graphPost('graph_field_set',{node_id:w.dataset.fieldNode,field_id:+w.dataset.fieldId,value:v});pagerDrop('graph');await people(graphNode,true)}
 catch(x){errCaught(x);delete w.dataset.busy;w.querySelectorAll('button,input,select').forEach(x=>x.disabled=false);toast(x.message,true)}}
document.addEventListener('click',e=>{const b=e.target.closest('[data-field-edit]');if(b){e.preventDefault();return fieldEditOpen(b)}
 const w=e.target.closest('.field-inline');if(!w)return;
 if(e.target.closest('[data-field-save]'))return fieldEditSave(w,w.querySelector('input,select').value);
 if(e.target.closest('[data-field-clear]'))return fieldEditSave(w,'');
 if(e.target.closest('[data-field-cancel]'))return people(graphNode,true)});
document.addEventListener('keydown',e=>{const w=e.target.closest?.('.field-inline');if(!w||e.isComposing)return;
 if(e.key==='Enter'&&e.target.matches('input')){e.preventDefault();fieldEditSave(w,e.target.value)}else if(e.key==='Escape'){e.preventDefault();e.stopPropagation();people(graphNode,true)}},true);
document.addEventListener('change',e=>{const w=e.target.closest?.('.field-inline');if(w&&e.target.matches('select'))fieldEditSave(w,e.target.value)});
// The picture: upload one (made small here, before it leaves the browser), pick one found for them, or remove it.
const picSmall=src=>new Promise((ok,no)=>{const im=new Image();im.onload=()=>{const k=Math.min(1,256/Math.max(im.naturalWidth,im.naturalHeight)),c=document.createElement('canvas');c.width=Math.max(1,Math.round(im.naturalWidth*k));c.height=Math.max(1,Math.round(im.naturalHeight*k));
 const g=c.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,c.width,c.height);g.drawImage(im,0,0,c.width,c.height);let q=.85,u=c.toDataURL('image/jpeg',q);while(u.length>60000&&q>.3)u=c.toDataURL('image/jpeg',q-=.15);ok(u)};im.onerror=()=>no(new Error('That isn’t a picture this browser can read.'));im.src=src});
async function picOpen(node){const org=String(node).startsWith('org:'),pic=$('#people-view .graph-detail>.name-row .pic-edit')?.innerHTML||'';crm={mode:'picture',node,org};
 setHTML($('#crm-form'),html`${crmHead('Picture')}<div class="pic-now">${pic}</div><div class="pic-pick"><label class="crm-file"><input name="pic" type="file" accept="image/png,image/jpeg,image/webp,image/gif"><span class="crm-file-name">Upload a picture</span></label></div><fieldset class="pic-found" hidden><legend>Found for ${org?'it':'them'}</legend><div class="pic-grid" data-pic-found></div></fieldset><p class="ed-note warn" data-crm-error role="alert" hidden></p><div class="ed-actions">${/<img/.test(pic)?html`<button type="button" class="ghost danger" data-pic-remove>Remove picture</button>`:''}<span class="grow"></span><button type="button" class="ghost" data-crm-close>Close</button></div>`);
 crmShow();
 try{const r=await graphPost('graph_pictures_found',{node_id:node});if(crm?.node!==node||!r.found?.length)return;const box=$('#crm-form [data-pic-found]');
  setHTML(box,html`${r.found.map((u,i)=>html`<button type="button" class="pic-option" data-pic-found-i="${i}" aria-label="Use this picture"><img src="${u}" alt="" width="56" height="56"></button>`)}`);crm.found=r.found;box.parentElement.hidden=false}catch{}}
async function picSave(args,done){const c=crm;if(!c)return;crmSay('');$('#crm-form').querySelectorAll('button,input').forEach(x=>x.disabled=true);
 try{await graphPost('graph_picture',{node_id:c.node,...args});$('#crm-dialog').close();toast(done);pagerDrop('graph');await people(graphNode,true)}
 catch(x){errCaught(x);crmSay(x.message);$('#crm-form').querySelectorAll('button,input').forEach(x=>x.disabled=false)}}
document.addEventListener('click',e=>{const b=e.target.closest('[data-pic-edit]');if(!b)return;e.preventDefault();picOpen(b.dataset.picEdit)});
$('#crm-form').addEventListener('click',async e=>{const c=crm;if(c?.mode!=='picture')return;
 if(e.target.closest('[data-pic-remove]')){e.preventDefault();return picSave({remove:true},'Removed.')}
 const o=e.target.closest('[data-pic-found-i]');if(o){e.preventDefault();try{picSave({data:await picSmall(c.found[+o.dataset.picFoundI])},'Saved.')}catch(x){errCaught(x);crmSay(x.message)}}});
$('#crm-form').addEventListener('change',e=>{const c=crm;if(c?.mode!=='picture'||e.target.name!=='pic')return;const file=e.target.files?.[0];if(!file)return;
 if(file.size>15*1024*1024)return crmSay('That picture is too big: up to 15 MB.');const r=new FileReader();r.onload=async()=>{try{picSave({data:await picSmall(r.result)},'Saved.')}catch(x){errCaught(x);crmSay(x.message)}};r.readAsDataURL(file)});
async function crmFieldsSave(c){for(const f of c.fields){const now=String($('#crm-form').elements['f'+f.id]?.value??'').trim();if(now===String(f.value??''))continue;
  await graphPost('graph_field_set',{node_id:c.node,field_id:f.id,value:now})}
 $('#crm-dialog').close();toast('Saved.');graphFieldsStale=false;await people(graphNode,true)}
$('#crm-dialog').addEventListener('close',()=>{if(graphFieldsStale){graphFieldsStale=false;people(graphNode,true)}});
document.addEventListener('keydown',async e=>{const i=e.target.closest?.('.tag-add input');if(!i||e.key!=='Enter'||e.isComposing)return;e.preventDefault();const f=i.parentElement,t=i.value.trim();if(!t)return;i.disabled=true;i.blur();
 try{await graphPost('graph_tag',{node_id:f.dataset.tagNode,tag:t,add:true});if(!graphTags.some(x=>x.tag.toLowerCase()===t.toLowerCase())){graphTags.push({tag:t,count:1});tagsPaint()}pagerDrop('graph');await people(graphNode,true)}catch(err){errCaught(err);toast(err.message,true);i.disabled=false}},true);
document.addEventListener('click',async e=>{const t=e.target.closest('[data-tag-remove],[data-fields-edit]');if(!t)return;e.preventDefault();e.stopPropagation();
 try{if(t.dataset.fieldsEdit)return await crmFieldsOpen(t.dataset.fieldsEdit);t.disabled=true;await graphPost('graph_tag',{node_id:t.dataset.tagNode,tag:t.dataset.tagRemove,add:false});pagerDrop('graph');await people(graphNode,true)}catch(err){errCaught(err);toast(err.message,true);t.disabled=false}},true);
$('#people-view').onclick=async e=>{const tab=e.target.closest('[data-graph-pane]');if(tab){showGraphPane(tab.dataset.graphPane);return}if(e.target.closest('[data-ge-more]')){const n=graphTl.page,box=e.target.closest('.graph-timeline'),hidden=box?box.querySelectorAll('.graph-events .graph-event[hidden]').length:0;
  if(n?.timeline&&box){if(n.timeline.next&&hidden<30)graphTlLoad(n.timeline.source||'',true);else{n.timeline.shown=(n.timeline.shown||GRAPH_ROWS)+30;graphTlDraw()}}
  else{for(const x of $('#people-view').querySelectorAll('.graph-events [hidden]'))x.hidden=false;e.target.closest('[data-ge-more]').remove()}return}
 const soonAll=e.target.closest('[data-ge-soon]');if(soonAll){for(const x of soonAll.closest('.ge-soon').querySelectorAll('[hidden]'))x.hidden=false;soonAll.remove();return}
 const tlChip=e.target.closest('[data-tl-source]');if(tlChip){graphTlLoad(tlChip.dataset.tlSource,false);return}if(openEventFrom(e))return;
 const q=e.target.closest('[data-quote-event]');if(q){openEvent(q.dataset.quoteEvent,'');return}
 const qs=e.target.closest('[data-quote-events]');if(qs){openSources(qs.dataset.quoteEvents,qs.textContent);return}
 const shown=e.target.closest('[data-show-person]');if(shown){shown.disabled=true;try{await graphPost('graph_show_person',{identifier:shown.dataset.showPerson});setHTML(shown.parentNode,html`<span class="muted hs-said">Shown as a person.</span>`)}catch(err){errCaught(err);shown.disabled=false;toast(err.message,true)}return}  /* the row stays until the list loads again: the rebuild adds them */
 const undo=e.target.closest('[data-warmup-undo]');if(undo){undo.disabled=true;try{await graphPost('graph_warmup',{domain:undo.dataset.warmupUndo,warmup:false});toast(t('Back in your Graph: {}.',undo.dataset.warmupUndo));await people(graphNode,true)}catch(err){errCaught(err);undo.disabled=false;toast(err.message,true)}return}
 const sameAll=e.target.closest('[data-same-all]');if(sameAll){const pairs=JSON.parse(sameAll.dataset.sameAll);if(!confirm(`Merge ${pairs.length} pairs?`))return;sameAll.disabled=true;
  try{const said=await graphPost('graph_same_all',{pairs});toastUnmerge(said.merged===1?'Merged 1 pair.':`Merged ${said.merged} pairs.`,said.batch);await people(graphNode,true)}catch(err){errCaught(err);sameAll.disabled=false;toast(err.message,true)}return}
 const same=e.target.closest('[data-same]');if(same){const yes=same.dataset.same==='1',box=same.closest('.same-pair,.same-ask');same.disabled=true;
  // the answer on the pair at once, kept through redraws (pairAnswer); the rebuild runs in the background
  const back=box?pairAnswer(box,pairKey('p',same.dataset.a,same.dataset.b),yes?'Merged.':'Kept apart.'):null;
  try{await graphPost('graph_same',{a:same.dataset.a,b:same.dataset.b,same:yes});toast(yes?'Merged.':same.matches('[data-split]')?'Split. Won’t be joined again.':'Kept apart.');await people(graphNode,true)}catch(err){errCaught(err);same.disabled=false;back?.();toast(err.message,true)}return}
 const un=e.target.closest('[data-unrelate]');if(un){un.disabled=true;try{await graphPost('graph_relation',{node_id:un.dataset.unrelate,related_to:un.dataset.relatedTo,relation:''});toast('Removed.');await people(graphNode,true)}catch(err){errCaught(err);un.disabled=false;toast(err.message,true)}return}const del=e.target.closest('[data-person-delete],[data-person-delete-no],[data-person-delete-yes]');if(del){const ask=$('#people-view .person-delete-confirm');
  if(del.matches('[data-person-delete]')){del.closest('details').open=false;const nf=$('#people-view .name-form');if(nf)nf.hidden=true;ask.hidden=false;ask.querySelector('[data-person-delete-no]').focus();return}
  if(del.matches('[data-person-delete-no]')){ask.hidden=true;return}
  del.disabled=true;try{await graphPost('graph_person_delete',{node_id:graphNode});toast('Deleted. Won’t be added again.');graphBack('people')}catch(err){errCaught(err);del.disabled=false;toast(err.message,true)}return}const wrong=e.target.closest('[data-org-wrong],[data-org-lookup]');if(wrong){const w=wrong.matches('[data-org-wrong]');if(w&&!confirm('Clear the looked-up details? This domain won’t be looked up again until you ask.'))return;wrong.disabled=true;try{await graphPost('graph_org_wrong',{node_id:graphNode,wrong:w});const of=$('#people-view .org-form');if(of)orgOpen(of,false);toast(w?'Cleared.':'It will be looked up again soon.');await people(graphNode,true)}catch(err){errCaught(err);wrong.disabled=false;toast(err.message,true)}return}
 const add=e.target.closest('[data-pf-add]');if(add){const list=add.previousElementSibling;list.append(htmlNodes(pfItem(add.dataset.pfAdd,'')));list.lastElementChild.querySelector('input').focus();return}
 const rm=e.target.closest('[data-pf-remove]');if(rm){if(rm.closest('.pf-list-field')?.querySelector('[aria-invalid]'))pfErrClear(rm);const item=rm.closest('.pf-item'),next=item.nextElementSibling||item.previousElementSibling;item.remove();(next?.querySelector('input')||e.target.closest('.pf-list-field')?.querySelector('[data-pf-add]'))?.focus();return}
 if(e.target.closest('[data-org-cancel]')){const f=$('#people-view .org-form');orgOpen(f,false);if(f.matches('.person-form'))people(graphNode,true);return}
 if(e.target.closest('[data-org-edit]')){const f=$('#people-view .org-form');orgOpen(f,true);f.querySelector('input,textarea').focus({preventScroll:true});return}
 if(e.target.closest('[data-name-edit]')){const f=$('#people-view .name-form');f.hidden=!f.hidden;if(!f.hidden){f.elements[0].focus();f.elements[0].select()}return}const crumb=e.target.closest('[data-crumb]');if(crumb){e.preventDefault();graphBack(crumb.dataset.crumb);return}
 const unlink=e.target.closest('[data-fact-unlink]');if(unlink){unlink.disabled=true;try{const r=await graphPost('graph_fact_unlink',{fact_id:Number(unlink.dataset.factUnlink),node_id:graphNode});toast(r.general?t('Moved to Learning, Facts.'):t('Taken off this page.'));await people(graphNode,true)}catch(err){errCaught(err);unlink.disabled=false;toast(err.message,true)}return}
 const forget=e.target.closest('[data-fact-forget]');if(forget){const text=forget.closest('li')?.querySelector('span,.rc-text')?.textContent||'';if(!confirm(t('Remove this everywhere? “{}” It is deleted for good. To keep it as a general fact, choose Not about {} instead.',text,forget.dataset.who)))return;forget.disabled=true;try{await graphPost('forget_fact',{id:Number(forget.dataset.factForget)});toast(t('Removed.'));await people(graphNode,true)}catch(err){errCaught(err);forget.disabled=false;toast(err.message,true)}return}
 const kn=e.target.closest('[data-known-edit],[data-known-add],[data-known-cancel]');if(kn){kn.closest('details')?.removeAttribute('open');const f=kn.closest('form');if(f)f.hidden=true;
  knownEdit=kn.dataset.knownEdit?Number(kn.dataset.knownEdit):null;knownAdd=kn.matches('[data-known-add]')?graphNode:'';await people(graphNode,true);
  const ta=$('#people-view .known-form textarea');if(ta&&!f){ta.focus();ta.setSelectionRange(ta.value.length,ta.value.length)}return}
 const b=e.target.closest('[data-node]');if(b&&b.dataset.node)graphOpen(b.dataset.node)};
$('#people-view').addEventListener('keydown',e=>{if(e.key==='Escape'&&e.target.closest('.known-form'))e.target.closest('form').querySelector('[data-known-cancel]').click()});
$('#people-view').onsubmit=async e=>{const kf=e.target.closest('.known-form');if(kf){e.preventDefault();const text=kf.text.value.trim(),save=kf.querySelector('.primary'),id=Number(kf.dataset.knownSave);save.disabled=true;
  try{await graphPost(id?'edit_fact':'graph_fact_add',id?{id,text}:{node_id:graphNode,text});kf.hidden=true;knownEdit=null;knownAdd='';toast(t('Saved.'));await people(graphNode,true)}catch(err){errCaught(err);save.disabled=false;toast(err.message,true)}return}
 const pf=e.target.closest('.person-form');if(pf){e.preventDefault();const b=$('#people-view [data-org-save]'),fields=personChanged(pf);
  const errs=personCheck(fields);personErrors(pf,errs);if(errs.length)return;if(!Object.keys(fields).length){orgOpen(pf,false);return}
  if(b)b.disabled=true;try{await graphPost('graph_person_edit',{node_id:pf.dataset.nodeId,fields});orgOpen(pf,false);toast('Saved.');await people(graphNode,true)}
  catch(err){errCaught(err);const k=personErrField(err.message);if(k&&k in fields)personErrors(pf,[[k,err.message]]);else toast(err.message,true)}finally{if(b?.isConnected)b.disabled=false}return}
 const o=e.target.closest('.org-form');if(o){e.preventDefault();const b=$('#people-view [data-org-save]');const changed=Object.fromEntries(ORG_FIELDS.map(([k])=>o.elements[k]).filter(f=>f.value.trim()!==f.defaultValue.trim()).map(f=>[f.name,f.value.trim()]));const {name,...fields}=changed;  /* only what the owner changed becomes theirs */
  const r=o.elements.role,role=r&&r.value.trim()!==r.defaultValue.trim()?r.value.trim():undefined;
  const errs=[...orgCheck(changed),...(role&&role.length>60?[['role',`Up to 60 characters (now ${role.length})`]]:[])];orgErrors(o,errs);if(errs.length)return;if(!Object.keys(changed).length&&role===undefined){orgOpen(o,false);return}
  if(b)b.disabled=true;try{if(Object.keys(changed).length)await graphPost('graph_org_edit',{node_id:o.dataset.nodeId,fields,...(name!==undefined?{name}:{})});if(role!==undefined)await graphPost('graph_role',{node_id:o.dataset.nodeId,role});orgOpen(o,false);toast('Saved.');await people(graphNode,true)}
  catch(err){errCaught(err);const k=ORG_FIELDS.find(([k,t])=>new RegExp('^('+t.split(' ')[0]+'|'+k.replace('_url','').replace('_',' ')+')\\b','i').test(err.message))?.[0];if(k&&k in changed)orgErrors(o,[[k,err.message]]);else toast(err.message,true)}finally{if(b?.isConnected)b.disabled=false}return}
 const n=e.target.closest('.name-form');if(n){e.preventDefault();const b=n.querySelector('button');b.disabled=true;try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'graph_rename',args:{node_id:n.dataset.nodeId,name:n.newname.value.trim()}})});n.hidden=true;toast(r.merged?'Joined '+r.name+'.':'Renamed.');await people(r.node_id||graphNode,true)}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}return}};
// Typing searches after a short pause, Enter and Find at once; an empty box is the list again, with no wait.
let graphTyping=0;const graphFind=()=>{clearTimeout(graphTyping);people('')};
$('#people-find').onclick=graphFind;$('#people-query').onkeydown=e=>{if(e.key==='Enter')graphFind()};
$('#people-query').oninput=()=>{clearTimeout(graphTyping);if(!$('#people-query').value.trim()){graphFind();return}graphTyping=setTimeout(()=>people(''),150)};
