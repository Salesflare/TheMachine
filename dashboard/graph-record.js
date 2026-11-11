// What someone (or an organization) is to you: said by you, or read by a review in a message, shown with the line it came from.
// It applies as read; Edit sets it in your words.
const quoteLine=(id,quote,event)=>quote?html`<span class="role-why">“${quote}”${event?html` <button class="link" data-quote-event="${event}">Read</button>`:''}</span>`:'';
// The review's quote is markup (html``), never a plain string, so its Read button shows as a button.
const roleKv=n=>kv('To you',n.role?html`<b>${cap(n.role)}</b>${n.role_by==='review'?html`<span class="sub">A review read it in your messages${n.role_quote?html`: ${quoteLine(n.id,n.role_quote,n.role_event_id)}`:''}</span>`:''}`:html`<span class="muted">Not known yet</span>`,'','kv-role');
// Where someone works: from their work email or a source (a headline, a signature, their words), with that line.
const orgSaid=n=>n.org_by==='email'?'from their work email':n.org_by==='owner'?'you set it':n.org_by==='review'?`from ${n.org_via==='LinkedIn headline'?'their LinkedIn headline':'their '+(n.org_via||'message')}${n.org_at?', '+day(n.org_at):''}`:'';
// The owner's own details for an organization: they win over the service's, and "Wrong company" drops a bad match for good.
const ORG_FIELDS=[['name','Name',100],['website','Website',200],['linkedin_url','LinkedIn',200],['industry','Industry',120],['size','Size (people)',40],['location','Location',120],['founded','Founded',4],['about','About',600],['notes','Notes',4000]];
// The owner's own notes on a person or organization, as typed (lines kept).
const notesSection=t=>t?html`<section class="detail-section record-notes"><h4>Notes</h4><p>${t}</p></section>`:'';
// No maxlength or pattern: a looked-up value can be longer than the owner may type, and Save would block silently.
// Only what the owner changed is checked (orgCheck), the error under its field.
const ORG_GROUPS=[['Profile',['name','industry','size','location','founded','about']],['Contact',['website','linkedin_url']],['Notes',['notes']]];
const ORG_WIDTH={industry:'w-mid',size:'w-mid',location:'w-mid',founded:'w-short'};
const orgField=(k,t,v)=>html`<label class="pf-field ${ORG_WIDTH[k]||''}"><span>${t}</span>${k==='about'||k==='notes'?html`<textarea name="${k}" rows="4" aria-describedby="org-err-${k}"${k==='notes'?html` aria-label="Notes"`:''}>${v||''}</textarea>`:html`<input name="${k}" value="${v??''}" aria-describedby="org-err-${k}" autocomplete="off"${k==='founded'?html` inputmode="numeric"`:''}${k==='name'?html` placeholder="Leave empty to use the name from their messages"`:''}>`}<small class="field-error" id="org-err-${k}"></small></label>`;
const orgForm=n=>{const p=n.profile||{},v={...p,name:n.name,size:p.size||(p.employees?String(p.employees):'')},label=Object.fromEntries(ORG_FIELDS.map(([k,t])=>[k,t]));
 return html`<form class="org-form pf-form" id="org-form" data-node-id="${n.id}" novalidate hidden>${ORG_GROUPS.map(([g,ks])=>html`<fieldset><legend>${g}</legend>${ks.map(k=>orgField(k,label[k],v[k]))}</fieldset>`)}<fieldset><legend>With you</legend><label class="pf-field w-mid"><span>What it is to you</span><input name="role" value="${n.role||''}" placeholder="e.g. accounting firm, customer" aria-describedby="org-err-role" autocomplete="off"><small class="field-error" id="org-err-role"></small></label></fieldset><p class="graph-sub muted pf-note">Your edits stay. Empty a field to use the looked-up value again.</p>${n.profile&&Object.keys(n.profile).some(k=>k!=='website')&&!n.wrong?html`<p class="org-buttons"><button type="button" class="ghost" data-org-wrong>Wrong company, clear details</button></p>`:''}</form>`};
const orgActions=n=>html`<span class="org-actions"><button class="ghost" data-proj-new-here>New project</button><button class="ghost" data-org-edit>Edit</button><button type="button" class="ghost" data-org-cancel>Cancel</button><button type="submit" form="org-form" class="primary" data-org-save>Save</button><details class="fact-menu person-menu"><summary aria-label="More for this organization" title="More">⋯</summary><div class="fact-menu-list" role="menu"><button type="button" role="menuitem" data-card-here>New to-do</button><button type="button" role="menuitem" data-org-same>Same organization as…</button><button type="button" role="menuitem" data-org-site>Add a website…</button>${n.manual?html`<button type="button" role="menuitem" class="danger" data-org-delete>Delete…</button>`:''}</div></details></span>`;
// What the server would refuse, for the fields the owner changed only: [field, message] pairs.
const orgCheck=changed=>ORG_FIELDS.flatMap(([k,,max])=>{const t=changed[k];if(!t)return[];
 if(k==='founded')return /^(1[5-9]\d\d|20\d\d)$/.test(t)?[]:[[k,'A year, like 2014']];return t.length>max?[[k,`Up to ${max} characters (now ${t.length})`]]:[]});
const orgOpen=(f,open)=>{const a=f.closest('.graph-detail');f.hidden=!open;if(a){const cs=getComputedStyle(a);a.style.setProperty('--org-pt',cs.paddingTop);a.style.setProperty('--org-px',cs.paddingLeft);a.classList.toggle('org-editing',open)}if(!open){f.reset();f.matches('.person-form')?personErrors(f,[]):orgErrors(f,[])}orgStuck()};
// The editing header, once stuck under the top bar: square corners and a solid backing, so nothing shows under it.
const orgStuck=()=>{const h=document.querySelector('#people-view .graph-detail.org-editing>.name-row');if(h)h.classList.toggle('stuck',h.getBoundingClientRect().top<=parseFloat(getComputedStyle(h).top)+1)};
addEventListener('scroll',orgStuck,{passive:true});
// A field's error goes as soon as the owner edits it, not only on the next Save
const pfErrClear=el=>{const list=el.closest('.pf-list-field');  /* a list of phones or emails shares one error */
 if(list){for(const i of list.querySelectorAll('[aria-invalid]'))i.removeAttribute('aria-invalid');const m=list.querySelector('.field-error');if(m)m.textContent='';return}
 el.removeAttribute('aria-invalid');for(const id of (el.getAttribute('aria-describedby')||'').split(' ')){const m=id&&document.getElementById(id);if(m)m.textContent=''}};
document.addEventListener('input',e=>{const el=e.target;if(el.getAttribute?.('aria-invalid')==='true'&&el.closest('.pf-form'))pfErrClear(el)});
const orgErrors=(f,errs)=>{for(const k of [...ORG_FIELDS.map(([k])=>k),'role']){const el=f.elements[k];if(!el)continue;const m=errs.find(([x])=>x===k);if(m)el.setAttribute('aria-invalid','true');else el.removeAttribute('aria-invalid');f.querySelector('#org-err-'+k).textContent=m?m[1]:''}
 const first=errs.length&&f.elements[errs[0][0]];if(first){first.focus({preventScroll:true});first.scrollIntoView({block:'center'})}};
// A person's page: photo, name, title · organization, place, how you're in touch; then Contact, With you, Related, and
// how identities were joined. Edit opens one form; the owner's word wins over look-ups and stays through merges and
// Undo (graph.person_edit).
const COUNTRY=c=>{try{return /^[A-Z]{2}$/.test(c)?new Intl.DisplayNames([],{type:'region'}).of(c):c}catch{return c}};
const personPlace=n=>{const p=n.profile||{};return p.location||[p.city,COUNTRY(p.country)].filter(Boolean).join(', ')};
// Facts their connectors read (their Slack, X or LinkedIn, a contact, the CRM) come first; hover says where from.
const FACT_FROM=p=>{const s=Object.values(p.sources||{}).map(x=>x.from);return s.length?'From '+[...new Set(s)].join(', '):''};
const localTime=tz=>{try{if(!tz)return'';const at=z=>fmtHM(Date.now(),{timeZone:z}),theirs=at(tz);return theirs===at(undefined)?'':t('{} their time',theirs)}catch{return''}};  /* only when their clock differs from the owner's */
// A person's title and organization as one line: "CTO · Acme", or the one that's there (never "CTO at Acme": a title
// can be a relationship). As person_line on the Machine.
const jobLine=(title,org)=>[title,org].filter(Boolean).join(' · ');
const personJob=n=>{if(n.kind!=='person')return'';const p=n.profile||{},org=n.org&&n.org_name?html`<button class="node" data-node="${n.org}" title="${n.org_name}">${n.org_name}</button>`:p.company?p.company:'';
 const title=p.title||(!org&&n.headline)||'',job=orEmpty(html`${[title,org].filter(Boolean).map((x,i)=>html`${i?' · ':''}${x}`)}`),place=[personPlace(n),localTime(p.timezone)].filter(Boolean).join(' · '),from=FACT_FROM(p);
 return html`${job?html`<p class="person-job">${job}</p>`:''}${place?html`<p class="person-place"${from?html` title="${from}"`:''}>${place}</p>`:''}`};
const talkEvery=g=>{const d=Math.round(g);return d<=1?'Talk daily':d<=4?'Talk every few days':d<=10?'Talk weekly':d<=20?'Talk every couple of weeks':d<=45?'Talk monthly':'Talk now and then'};
// How you're in touch: the last contact as a <time> whose hover has its exact date; capitalized when it comes first
const lastLine=(n,first)=>htmlT(n.seen_only?(first?'Last seen {}':'last seen {}'):first?'Last contact {}':'last contact {}',sinceTime(n.last_at));
const relLine=n=>{const gap=n.quiet?'Gone quiet':n.usual_gap_days?talkEvery(n.usual_gap_days):'',parts=[gap,n.last_at?lastLine(n,!gap):'',n.next_meeting?(gap||n.last_at?String:cap)('next meeting '+day(n.next_meeting)):''].filter(Boolean);
 return parts.length?html`${parts.map((x,i)=>html`${i?' · ':''}${x}`)}`:''};
// Phones and emails as the server lists them (the messages', less what the owner took off, plus what they added).
const personContacts=n=>({phones:n.phones||(n.ids||[]).filter(i=>/^\+\d/.test(i)).map(value=>({value,by:'messages'})),emails:n.emails||(n.ids||[]).filter(i=>i.includes('@')).map(value=>({value,by:'messages'}))});
const breakable=t=>html`${String(t).split('@').map((x,i)=>i?html`@<wbr>${x}`:x)}`;
const kv=(k,v,acts='',cls='')=>html`<div class="kv${cls?' '+cls:''}"><span class="k">${k}</span><span class="v">${v}</span>${acts?html`<span class="acts">${acts}</span>`:''}</div>`;
const copyBtn=(t,what)=>html`<button type="button" class="ghost" data-copy-command="${t}" aria-label="Copy ${what}">Copy</button>`;
const liShort=u=>u.replace(/^https?:\/\/(www\.)?/,'').replace(/\/$/,'');
function personContact(n){const c=personContacts(n),p=n.profile||{};
 const rows=[...c.phones.map(x=>kv('Phone',html`<a href="tel:${x.value.replace(/[^\d+]/g,'')}">${phoneShown(x.value)}</a>`,copyBtn(x.value,'phone number'))),
  ...c.emails.map(x=>kv('Email',html`<a href="mailto:${x.value}">${breakable(x.value)}</a>${bounceNote(x.bounced_at)}`,copyBtn(x.value,'email address')))];
 const liLink=/^https:\/\/([a-z]{2,3}\.)?linkedin\.com\//.test(p.linkedin_url||''),liSince=/^\d{4}-\d\d-\d\d$/.test(p.linkedin_since||'')?t('Connected since {}',localeDate(new Date(p.linkedin_since+'T12:00'),DL,{month:'short',year:'numeric'})):'';  /* linkedin_connections.py */
 if(liLink||liSince)rows.push(kv('LinkedIn',html`${liLink?html`<a href="${safeHref(p.linkedin_url)}" target="_blank" rel="noreferrer">${breakable(liShort(p.linkedin_url))} ↗</a>`:''}${liLink&&liSince?html`<br>`:''}${liSince?html`<small class="muted">${liSince}</small>`:''}`));
 if(/^[A-Za-z0-9_]{1,15}$/.test(p.x||''))rows.push(kv('X',html`<a href="https://x.com/${p.x}" target="_blank" rel="noreferrer">@${p.x} ↗</a>`));
 if(/^https?:\/\/[^\s]+$/.test(p.website||''))rows.push(kv('Website',html`<a href="${safeHref(p.website)}" target="_blank" rel="noreferrer">${breakable(liShort(p.website))} ↗</a>`));
 if(n.birthday&&!n.team_only)rows.push(bdayRow(n));
 const also=[...new Set((n.ids||[]).filter(i=>!i.includes('@')&&!/^\+\d/.test(i)&&!(p.x&&i==='@'+p.x)))];const slack=n.slack_links||[];if(also.length)rows.push(kv('Also on',html`${also.map((a,i)=>html`${i?' · ':''}${a==='Slack'&&slack.length?slack.map((l,j)=>html`${j?' · ':''}<a href="${safeHref(l.url)}" target="_blank" rel="noreferrer" title="Open in Slack">${l.label} ↗</a>`):a}`)}`));
 return rows.length?html`<section class="detail-section person-contact"><h4>Contact</h4>${rows}</section>`:''}
// Birthday (person_birthday.py): the one the Birthdays routine reads, with where it came from. Edit sets or corrects it
// in the row: a month and a day, the year when known. Without one, Fields offers Add birthday, which opens the same row.
const BDAY_FROM={google:'From Google contacts',google_calendar:'From Google Calendar',facebook:'From Facebook',notes:'From your notes',owner:'Added by you'};
const bdayDate=(b,o)=>localeDate(new Date(b.year||2000,b.month-1,b.day,12),DL,{day:'numeric',month:'long',...(b.year?{year:'numeric'}:{}),...o});
function bdayAge(b){if(!b.year)return null;const now=new Date(),age=now.getFullYear()-b.year-((now.getMonth()+1)*100+now.getDate()<b.month*100+b.day?1:0);return age>=0?age:null}
const bdayFrom=s=>BDAY_FROM[s]?t(BDAY_FROM[s]):t('From {}',cap(String(s||'')));
function bdayRow(n){const b=n.birthday,age=bdayAge(b);return kv(t('Birthday'),html`<span class="bday">${bdayDate(b)}${age!=null?html` · <span class="bday-age">${t('age {}',age)}</span>`:''}</span><span class="sub">${bdayFrom(b.source)}</span>`,html`<button type="button" class="ghost" data-bday-edit="${n.id}" data-bday="${b.value}">${t('Edit')}</button>`,'bday-row')}
const bdayDayFirst=()=>{try{const p=new Intl.DateTimeFormat(DL,{day:'numeric',month:'long'}).formatToParts(new Date(2000,11,9));return p.findIndex(x=>x.type==='day')<p.findIndex(x=>x.type==='month')}catch{return true}};
function bdayEditor(node,value){const m=/^(\d{4}|-)-(\d\d)-(\d\d)$/.exec(value||''),month=m?+m[2]:0,day=m?+m[3]:'',year=m&&m[1]!=='-'?m[1]:'';
 const d=html`<input name="day" inputmode="numeric" maxlength="2" value="${day}" placeholder="${t('Day')}" aria-label="${t('Day')}" autocomplete="off">`,
  mo=html`<select name="month" aria-label="${t('Month')}"><option value=""${month?'':html` selected`}>${t('Month')}</option>${Array.from({length:12},(_,i)=>html`<option value="${i+1}"${month===i+1?html` selected`:''}>${localeDate(new Date(2000,i,1,12),DL,{month:'long'})}</option>`)}</select>`;
 return html`<span class="bday-edit" data-bday-node="${node}"><span class="bday-fields">${bdayDayFirst()?html`${d}${mo}`:html`${mo}${d}`}<input name="year" inputmode="numeric" maxlength="4" value="${year}" placeholder="${t('Year (optional)')}" aria-label="${t('Year (optional)')}" autocomplete="off"></span><small class="field-error" role="alert"></small><span class="bday-btns"><button type="button" class="primary" data-bday-save>${t('Save')}</button><button type="button" class="ghost" data-bday-cancel>${t('Cancel')}</button>${m?html`<button type="button" class="ghost" data-bday-remove>${t('Remove')}</button>`:''}</span></span>`}
function bdayOpen(node,value){const view=$('#people-view .person-view');if(!view)return;let row=view.querySelector('.bday-row');
 if(!row){let sec=view.querySelector('.person-contact');if(!sec){sec=htmlNodes(html`<section class="detail-section person-contact"><h4>${t('Contact')}</h4></section>`).firstElementChild;const at=view.querySelector('.person-about');at?at.before(sec):view.append(sec)}
  row=htmlNodes(kv(t('Birthday'),'','','bday-row')).firstElementChild;const also=[...sec.querySelectorAll('.kv')].find(k=>k.querySelector('.k')?.textContent===t('Also on'));also?also.before(row):sec.append(row)}
 for(const b of view.querySelectorAll('[data-bday-add]'))b.hidden=true;row.querySelector('.acts')?.remove();setHTML(row.querySelector('.v'),bdayEditor(node,value));row.classList.add('editing');(row.querySelector('select[name=month]').value?row.querySelector('input[name=day]'):row.querySelector('select,input')).focus()}
function bdayCheck(w){const v=k=>String(w.querySelector(`[name=${k}]`).value||'').trim(),month=+v('month'),day=+v('day'),year=v('year');
 if(!month||!/^\d{1,2}$/.test(v('day')))return[t('Pick a month and a day'),month?'day':'month'];
 if(year&&!/^\d{4}$/.test(year))return[t('Year: four digits, like 1990'),'year'];
 if(new Date(+year||2000,month-1,day).getDate()!==day)return[t('That day isn’t in that month'),'day'];
 if(year&&(+year<1900||+year>new Date().getFullYear()))return[t('Year: not in the future, from 1900'),'year'];
 return[null,{month,day,year}]}
async function bdaySave(w,remove){if(w.dataset.busy)return;const say=m=>{w.querySelector('.field-error').textContent=m||''};let args={remove:true};
 if(!remove){const [err,got]=bdayCheck(w);if(err){say(err);const i=w.querySelector(`[name=${got}]`);i.setAttribute('aria-invalid','true');i.focus();return}args=got}
 w.dataset.busy='1';w.querySelectorAll('button,input,select').forEach(x=>x.disabled=true);
 try{await graphPost('graph_birthday',{node_id:w.dataset.bdayNode,...args});toast(remove?t('Removed.'):t('Saved.'));await people(graphNode,true)}
 catch(x){errCaught(x);delete w.dataset.busy;w.querySelectorAll('button,input,select').forEach(x=>x.disabled=false);say(x.message)}}
document.addEventListener('click',e=>{const open=e.target.closest('[data-bday-edit],[data-bday-add]');if(open){e.preventDefault();return bdayOpen(open.dataset.bdayEdit||open.dataset.bdayAdd,open.dataset.bday||'')}
 const w=e.target.closest('.bday-edit');if(!w)return;
 if(e.target.closest('[data-bday-save]'))return bdaySave(w,false);
 if(e.target.closest('[data-bday-remove]'))return bdaySave(w,true);
 if(e.target.closest('[data-bday-cancel]'))return people(graphNode,true)});
document.addEventListener('input',e=>{const w=e.target.closest?.('.bday-edit');if(w){w.querySelector('.field-error').textContent='';w.querySelectorAll('[aria-invalid]').forEach(i=>i.removeAttribute('aria-invalid'))}});
document.addEventListener('keydown',e=>{const w=e.target.closest?.('.bday-edit');if(!w||e.isComposing)return;
 if(e.key==='Enter'&&e.target.matches('input,select')){e.preventDefault();bdaySave(w,false)}else if(e.key==='Escape'){e.preventDefault();e.stopPropagation();people(graphNode,true)}},true);
function personAbout(n){const rows=[],f=n.fleet,work=f?.in?.find(x=>x.kind==='work');
 rows.push(roleKv(n));
 if(n.side)rows.push(kv('Type',n.side==='work'?'Work contact':'Personal contact'));
 if(f?.in?.length)rows.push(kv('Network',html`<span class="fleet-mark">${[...new Set(f.in.map(x=>x.kind==='work'&&x.fleet_name?`${x.label} (${x.fleet_name})`:x.label)),f.machine?'Has a Machine':''].filter(Boolean).join(' · ')}</span>`,html`<button type="button" class="ghost" data-fleet-member="${f.in[0].member_id}">See in Fleet</button>${work?html`<button type="button" class="ghost" data-fleet-free="${work.fleet}">Ask your Fleet</button>`:''}`));
 else if(f?.machine)rows.push(kv('Network',html`<span class="fleet-mark">${[t('Has a Machine'),f.network?.requested?t('Friend request sent'):''].filter(Boolean).join(' · ')}</span>`,
  f.network?.can_add?html`<button type="button" class="ghost" data-person-friend="${f.network.hint==='colleague'?'colleague':'friend'}" data-net-email="${f.network.email}">${t('Add as a friend')}</button>`:'','kv-under'));  // found on the Network, in no Fleet together
 else if(n.invite)rows.push(kv('Network',html`<span class="fleet-mark">${t('No Machine found')}</span>${n.invite.family?html`<span class="sub mi-family">${inviteFamilyGo(n.invite.family)}</span>`:''}`,html`<button type="button" class="ghost" data-machine-invite="${JSON.stringify({...n.invite,node:n.id})}">${t('Invite to The Machine')}</button>`,'kv-under'));  // no Machine the owner knows of
 if(f?.named)rows.push(kv('Name',html`<span class="fleet-named">From your ${work?'Fleet':f.in[0].kind==='family'?'Family':'Friends'}. Your messages say “${n.name_from_messages||''}”.</span>`,html`<button type="button" class="ghost" data-fleet-keep="${n.name}">Keep</button>`));
 if(graphOwners.length)rows.push(ownerRow(n));
 return html`<section class="detail-section person-about"><h4>With you</h4>${rows}</section>`}
// People, Projects and Organizations linked to a page, each its own section (person and organization pages alike).
const detailGroups=(n,group)=>html`${n.relations?.length?html`<section class="detail-section"><h4>How they’re related</h4><div class="relations">${n.relations.map(r=>html`<div class="graph-sub relation"><span>${r.a_name} is ${r.relation} ${r.b_name}</span><button class="ghost" data-unrelate="${r.a}" data-related-to="${r.b}">Remove</button></div>`)}</div></section>`:''}${[['person','People'],['project','Projects'],['org','Organizations']].map(([k,t])=>group(k).length?html`<section class="detail-section"><h4>${t}</h4><div class="graph-links">${group(k).map(nodeButton)}</div></section>`:'')}`;
// A person's ⋯ menu: Delete permanently… (rarely needed), which opens its own confirm step under the header.
const personMenu=html`<details class="fact-menu person-menu"><summary aria-label="More for this person" title="More">⋯</summary><div class="fact-menu-list" role="menu"><button type="button" role="menuitem" data-proj-new-here>New project</button><button type="button" role="menuitem" data-card-here>New to-do</button><button type="button" role="menuitem" data-same-as>Same person as…</button><button type="button" role="menuitem" class="danger" data-person-delete>Delete permanently…</button></div></details>`;
const personActions=html`<span class="org-actions"><button class="ghost" data-org-edit>Edit</button><button type="button" class="ghost" data-org-cancel>Cancel</button><button type="submit" form="org-form" class="primary" data-org-save>Save</button>${personMenu}</span>`;
// The edit form: fields as long as what goes in them, grouped as the page is. Only what the owner changed is sent.
const PERSON_LIMITS={name:100,title:120,org:100,location:120,linkedin_url:200,role:60,notes:4000};
const pfField=(k,label,value,{hint='',placeholder='',cls='',type='text',mode=''}={})=>html`<label class="pf-field ${cls}"><span>${label}</span><input name="${k}" type="${type}" value="${value||''}"${placeholder?html` placeholder="${placeholder}"`:''}${mode?html` inputmode="${mode}"`:''} aria-describedby="pe-err-${k}" autocomplete="off">${hint?html`<small class="muted">${hint}</small>`:''}<small class="field-error" id="pe-err-${k}"></small></label>`;
const pfItem=(kind,v)=>html`<div class="pf-item"><input name="${kind}" type="${kind==='phones'?'tel':'email'}" value="${v}" aria-label="${kind==='phones'?'Phone':'Email'}"${kind==='phones'?html` inputmode="tel"`:''} autocomplete="off"><button type="button" class="ghost" data-pf-remove aria-label="Remove">✕</button></div>`;
const pfList=(kind,label,items)=>html`<div class="pf-field pf-list-field ${kind==='phones'?'w-phone':'w-email'}"><span>${label}</span><div class="pf-list" data-kind="${kind}" data-was="${items.join('\n')}">${items.map(v=>pfItem(kind,v))}</div><button type="button" class="ghost pf-add" data-pf-add="${kind}">+ Add ${kind==='phones'?'phone':'email'}</button><small class="field-error" id="pe-err-${kind}"></small></div>`;
function personForm(n){const p=n.profile||{},c=personContacts(n),said=orgSaid(n),side=n.side||'';
 return html`<form class="org-form pf-form person-form" id="org-form" data-node-id="${n.id}" novalidate hidden>
 <fieldset><legend>Profile</legend>${pfField('name','Name',n.name,{placeholder:'Leave empty to use the name from their messages'})}${pfField('title','Title',p.title)}${pfField('org','Organization',n.org_name||'',{hint:said?cap(said.replace(/<[^>]+>/g,''))+(n.org_by==='review'&&n.org_quote?`: “${n.org_quote}”`:''):'',placeholder:'Where do they work? e.g. Acme',cls:'w-mid'})}${pfField('location','Location',p.location||personPlace(n),{placeholder:'e.g. Ghent, Belgium',cls:'w-mid'})}${pfField('linkedin_url','LinkedIn',p.linkedin_url,{placeholder:'linkedin.com/in/…',type:'url'})}</fieldset>
 <fieldset><legend>Contact</legend>${pfList('phones','Phone',c.phones.map(x=>x.value))}${pfList('emails','Email',c.emails.map(x=>x.value))}</fieldset>
 <fieldset><legend>With you</legend>${pfField('role','What they are to you',n.role||'',{placeholder:'e.g. accountant, sister, investor',cls:'w-mid'})}<div class="pf-field"><span id="pf-side-l">Type</span><div class="pf-seg" role="radiogroup" aria-labelledby="pf-side-l" data-was="${side}">${[['work','Work'],['personal','Personal']].map(([v,t])=>html`<label><input type="radio" name="side" value="${v}"${side===v?html` checked`:''}><span>${t}</span></label>`)}</div><small class="field-error" id="pe-err-side"></small></div><label class="pf-field"><span>Notes</span><textarea name="notes" rows="4" aria-describedby="pe-err-notes">${n.notes||''}</textarea><small class="field-error" id="pe-err-notes"></small></label></fieldset>
 <p class="graph-sub muted pf-note">Your edits stay, also when their details are looked up again. Empty a field to use the looked-up value again.</p></form>`}
const pfValues=(f,kind)=>[...f.querySelectorAll(`.pf-list[data-kind="${kind}"] input`)].map(i=>i.value.trim()).filter(Boolean);
// What the owner changed, as the server takes it: {field: value}. Lists are sent whole, as they are now.
function personChanged(f){const out=Object.create(null);  // only the fixed field names below; no prototype to write through
 for(const k of Object.keys(PERSON_LIMITS)){const el=f.elements[k];if(el&&el.value.trim()!==el.defaultValue.trim())out[k]=el.value.trim()}
 for(const kind of ['phones','emails']){const now=pfValues(f,kind),was=f.querySelector(`.pf-list[data-kind="${kind}"]`).dataset.was.split('\n').filter(Boolean);if(now.join('\n')!==was.join('\n'))out[kind]=now}
 const side=f.querySelector('input[name=side]:checked')?.value||'',seg=f.querySelector('.pf-seg');if(side!==seg.dataset.was)out.side=side;return out}
const PHONE_RE=/^\+?[\d\s().-]{6,40}$/,EMAIL_RE=/^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const personCheck=ch=>Object.entries(ch).flatMap(([k,v])=>k==='phones'?v.filter(x=>!PHONE_RE.test(x)).slice(0,1).map(x=>[k,`${x} is not a phone number`]):k==='emails'?v.filter(x=>!EMAIL_RE.test(x)).slice(0,1).map(x=>[k,`${x} is not an email address`]):PERSON_LIMITS[k]&&v.length>PERSON_LIMITS[k]?[[k,`Up to ${PERSON_LIMITS[k]} characters (now ${v.length})`]]:[]);
function personErrors(f,errs){for(const el of f.querySelectorAll('.field-error')){const k=el.id.slice(7),m=errs.find(([x])=>x===k);el.textContent=m?m[1]:'';
  for(const i of f.querySelectorAll(k==='phones'||k==='emails'?`.pf-list[data-kind="${k}"] input`:`[name="${k}"]`))m?i.setAttribute('aria-invalid','true'):i.removeAttribute('aria-invalid')}
 const first=errs.length&&f.querySelector(`[name="${errs[0][0]}"][aria-invalid]`);if(first){first.focus({preventScroll:true});first.scrollIntoView({block:'center'})}}
// Which field a server message is about.
const personErrField=m=>/^Notes/.test(m)?'notes':/phone/i.test(m)?'phones':/email/i.test(m)?'emails':/Work or Personal/.test(m)?'side':/LinkedIn/.test(m)?'linkedin_url':/^Title/.test(m)?'title':/^Location/.test(m)?'location':/role/i.test(m)?'role':/^org\b|organi[sz]ation/i.test(m)?'org':/name/i.test(m)?'name':'';
// About you: the owner's own record. Their addresses (aliases too) and numbers, never a person in the Graph: a search, a
// New person or an import with one of them comes here. Not shared as a record, so no Keep private.
function aboutYouPage(n){const rows=[...(n.phones||[]).map(x=>kv('Phone',html`<a href="tel:${x.value.replace(/[^\d+]/g,'')}">${phoneShown(x.value)}</a>`)),
  ...(n.emails||[]).map(x=>kv('Email',html`${breakable(x.value)}${x.by?html`<span class="sub">${x.by}</span>`:''}`))];
 return html`<div class="graph-crumbs" role="navigation" aria-label="Breadcrumb"><a href="#graph" data-crumb="">Graph</a><span aria-hidden="true">›</span><span aria-current="page">About you</span></div><article class="graph-detail person-page about-you"><div class="name-row">${personPic({name:n.owner_name||'You'},true)}<div class="person-head"><h3>About you</h3>${n.owner_name?html`<p class="person-job">${n.owner_name}</p>`:''}</div></div><div class="person-view"><p class="graph-sub person-bio">Your own addresses and numbers. They’re always you, never someone in your Graph.</p>${rows.length?html`<section class="detail-section person-contact"><h4>Yours</h4>${rows}</section>`:''}<p class="graph-sub role-row"><button type="button" class="link" data-about-addresses>Change them in Settings</button>${n.can_share?html`<button type="button" class="ghost" data-contact-share="me">Share my contact</button>`:''}</p></div></article>`}
document.addEventListener('click',e=>{if(!e.target.closest('[data-about-addresses]'))return;e.preventDefault();showSettings('account');requestAnimationFrame(()=>$('#settings-addresses')?.scrollIntoView({block:'start'}))});
// The summary on top of a person's page (person_summary.py): who they are to you, where things stand, what is open
// both ways. Each line links its sources: a message or meeting by its date, a promise or your note; a line you wrote
// needs none. Your edit wins: a later rewrite waits under it as a suggested update, Use it or Keep mine.
// One chip per source: one day's messages share a chip with their count; notes and promises one each.
const sumChips=sources=>{const out=[],days=new Map(),notes=[],promises=[];
 for(const s of sources){if(s.type==='event'){const k=localDay(new Date(s.at));if(!days.has(k)){days.set(k,[]);out.push(days.get(k))}days.get(k).push(s)}
  else if(s.type==='fact'){if(!notes.length)out.push(notes);notes.push(s)}else if(s.type==='promise'){if(!promises.length)out.push(promises);promises.push(s)}}
 return out.map(g=>{const s=g[0],n=g.length;
  if(s.type==='event'){if(n===1)return html`<button type="button" class="link" data-quote-event="${s.id}" title="${t('Read the message')}">${shortDay(s.at)}</button>`;
   const count=g.every(x=>/calendar|meeting/.test(x.kind||''))?t(['{} meeting','{} meetings'],n):t(['{} message','{} messages'],n);
   return html`<button type="button" class="link" data-quote-events="${g.map(x=>x.id).join(',')}" title="${t('Read the messages')}">${shortDay(s.at)} · ${count}</button>`}
  if(s.type==='promise')return html`<a href="${promiseHref(s)}">${n===1?t('Promise'):t(['{} promise','{} promises'],n)}</a>`;
  return html`<span title="${g.map(x=>x.text).join('\n')}">${n===1?t('Your note'):t(['{} note','{} notes'],n)}</span>`})};
const sumLines=lines=>html`<ul class="summary-lines">${lines.map(l=>html`<li><span class="sl-text" translate="no">${l.text}</span> <span class="sl-src">${l.by?t('AI: {}',l.by):sumChips(l.sources).map((x,i)=>html`${i?' · ':''}${x}`)}</span></li>`)}</ul>`;
const personSummary=n=>{const s=n.summary;if(!s?.lines?.length)return '';
 return html`<section class="detail-section person-summary" data-summary-node="${n.id}"><div class="summary-head"><h4>Summary</h4><button type="button" class="link" data-summary-edit>Edit</button></div>${sumLines(s.lines)}<p class="graph-sub summary-meta">${s.by==='owner'?t('Edited by you'):t('Updated {}',shortDay(s.at))}</p>${s.proposal?html`<div class="summary-proposal"><p class="graph-sub"><b>Suggested update</b></p>${sumLines(s.proposal)}<p class="role-row"><button type="button" data-summary-op="use">Use it</button><button type="button" class="ghost" data-summary-op="keep">Keep mine</button></p></div>`:''}<form class="summary-form" hidden><textarea name="lines" rows="5" maxlength="1500" aria-label="${t('Summary, one line each')}">${s.lines.map(l=>l.text).join('\n')}</textarea><p class="role-row"><button>Save</button><button type="button" class="ghost" data-summary-cancel>Cancel</button>${s.by==='owner'?html`<button type="button" class="link" data-summary-op="reset">Let The Machine write it</button>`:''}</p><p class="graph-sub field-error" role="alert" hidden></p></form></section>`};
const summaryPost=async(box,args)=>{const err=box.querySelector('.field-error');try{await graphPost('graph_summary',{node_id:box.dataset.summaryNode,...args});const f=box.querySelector('.summary-form');if(f)f.hidden=true;box.classList.remove('editing');await people(graphNode,true)}  /* the form closes first: a quiet refresh never redraws over an open one */
 catch(x){errCaught(x);if(err){err.textContent=x.message;err.hidden=false}else toast(x.message,true)}};
document.addEventListener('click',e=>{const box=e.target.closest('.person-summary');if(!box)return;const f=box.querySelector('.summary-form');
 if(e.target.closest('[data-summary-edit]')){f.hidden=false;box.classList.add('editing');const ta=f.elements.lines;ta.focus();ta.setSelectionRange(ta.value.length,ta.value.length);return}
 if(e.target.closest('[data-summary-cancel]')){f.hidden=true;box.classList.remove('editing');return}
 const op=e.target.closest('[data-summary-op]');if(op){op.disabled=true;summaryPost(box,{op:op.dataset.summaryOp}).finally(()=>{op.disabled=false})}});
document.addEventListener('submit',e=>{const f=e.target.closest('.summary-form');if(!f)return;e.preventDefault();const box=f.closest('.person-summary'),b=f.querySelector('button:not([type])');b.disabled=true;
 summaryPost(box,{op:'edit',lines:f.elements.lines.value.split('\n').map(x=>x.trim()).filter(Boolean)}).finally(()=>{b.disabled=false})});
function personPage(n,group,sub){return html`<article class="graph-detail person-page"><div class="name-row">${picEdit(n,personPic(n,true))}<div class="person-head"><h3 title="${n.name}">${n.name}</h3>${personJob(n)}</div>${personActions}</div>${personForm(n)}${deleteRow(n)}<div class="person-view">${n.bio?.text?html`<p class="graph-sub person-bio" title="${'From '+n.bio.from+', '+n.bio.at}">${n.bio.text}</p>`:''}${relLine(n)?html`<p class="person-rel detail-sub">${relLine(n)}</p>`:''}${personSummary(n)}${notesSection(n.notes)}${personContact(n)}${personAbout(n)}${crmFieldsSection(n)}${detailGroups(n,group)}${fleetAskRow(n)}${sameAsk(n)}${joinedRow(n)}</div></article>`}
const orgSite=n=>{const w=n.profile?.website;return /^https?:\/\/[^\s]+$/.test(w||'')?w:/^[a-z0-9.-]+\.[a-z]{2,}$/i.test(n.domain||'')?'https://'+n.domain:''};
const hostOf=u=>{try{return new URL(u).hostname.replace(/^www\./,'')}catch{return liShort(u)}};
function orgContact(n){const p=n.profile||{},site=orgSite(n),rows=[];
 if(site)rows.push(kv('Website',html`<a href="${safeHref(site)}" target="_blank" rel="noreferrer" title="${site}">${hostOf(site)} ↗</a>`));
 if(/^https:\/\/([a-z]{2,3}\.)?linkedin\.com\//.test(p.linkedin_url||''))rows.push(kv('LinkedIn',html`<a href="${safeHref(p.linkedin_url)}" target="_blank" rel="noreferrer">${breakable(liShort(p.linkedin_url))} ↗</a>`));
 return rows.length?html`<section class="detail-section person-contact"><h4>Contact</h4>${rows}</section>`:''}
const orgAbout=n=>html`<section class="detail-section person-about"><h4>With you</h4>${roleKv(n)}${graphOwners.length?ownerRow(n):''}</section>`;
const orgRel=n=>{const parts=[n.signals?t(['{} person','{} people'],n.signals):'',n.last_at?lastLine(n,!n.signals):''].filter(Boolean);return parts.length?html`${parts.map((x,i)=>html`${i?' · ':''}${x}`)}`:''};
function orgPage(n,group){const p=n.profile||{};return html`<article class="graph-detail person-page org-page"><div class="name-row">${picEdit(n,orgPic(n,true))}<div class="person-head"><h3 title="${n.name}">${n.name}</h3>${n.about?html`<p class="person-job">${n.about}</p>`:''}</div>${orgActions(n)}</div>${orgForm(n)}<div class="person-view">${p.about?html`<p class="graph-sub person-bio org-about">${p.about}</p>`:''}${orgRel(n)?html`<p class="person-rel detail-sub">${orgRel(n)}</p>`:''}${orgWrongRow(n)}${orgDoubleAsk(n)}${notesSection(n.profile?.notes)}${orgContact(n)}${orgSites(n)}${orgAbout(n)}${orgProjects(n)}${crmFieldsSection(n)}${detailGroups(n,group)}${fleetAskRow(n)}</div></article>`}
// An organization's projects, open ones first, each with where it stands
const orgProjects=n=>n.projects?.length?html`<section class="detail-section org-projects"><h4>Projects</h4><ul>${n.projects.map(p=>html`<li${p.open?'':html` class="done"`}><button type="button" class="inline-node" data-node="${p.id}" title="${p.name}">${p.name}</button><small class="muted">${p.outcome==='won'?'Won':p.outcome==='lost'?'Lost':p.archived?'Archived':p.stage?p.stage+(p.board?' on '+p.board:''):'No board'}</small></li>`)}</ul></section>`:'';
const deleteRow=n=>n.kind!=='person'?'':html`<div class="person-delete"><div class="person-delete-confirm" hidden><p>Delete ${n.name} and everything The Machine knows about them? This can’t be undone.</p><p class="muted">Won’t be added again.</p><div class="row"><button class="danger-solid" data-person-delete-yes>Delete</button><button class="ghost" data-person-delete-no>Cancel</button></div></div></div>`;
const orgWrongRow=n=>n.wrong?html`<p class="graph-sub role-row"><span class="muted">Looked-up details cleared: they were another company’s.</span><button class="ghost" data-org-lookup>Look it up again</button></p>`:'';
// Same person? The graph joins identities only on strong evidence (the same name on one message, the same LinkedIn
// profile, their number in their own mail); a likely match is a quiet question here and in People: Merge or Not the
// same, which is remembered. Joined identities list why, each with Undo (it splits them for good).
// Same person? and Same organization?: an answered pair shows its answer instead of the buttons for a moment
// (PAIR_SHOW_MS), then fades and leaves the list; the list's heading goes with the last pair. Leaving People, another
// list and opening the list again take answered pairs away at once. A redraw from before the Machine stored the answer
// (another tap's, a poll's, a slow rebuild's) never brings a pair back: an answered pair a late list still has stays
// hidden, and once the Machine's list no longer has it, its answer is forgotten. pairSaid: key -> answer.
const pairSaid=new Map(),pairRows={p:[],o:[]},pairTimers=new Map(),PAIR_SHOW_MS=1200;
const pairKey=(k,a,b)=>k+':'+[a,b].sort().join('|');
function pairsSteady(k,items){const fresh=new Map((items||[]).map(s=>[pairKey(k,s.a.id,s.b.id),s]));
 const rows=pairRows[k].filter(([key])=>fresh.has(key)||pairSaid.has(key)).map(([key,s])=>[key,fresh.get(key)||s]),have=new Set(rows.map(r=>r[0]));
 for(const [key,s] of fresh)if(!have.has(key)&&!pairSaid.has(key))rows.push([key,s]);pairRows[k]=rows;
 for(const key of pairSaid.keys())if(key.startsWith(k+':')&&!fresh.has(key)&&!have.has(key))pairSaid.delete(key);
 return rows.map(([key,s])=>pairSaid.has(key)?{...s,said:pairSaid.get(key)}:s)}
// Answered pairs (all of them, or the one key) leave the lists: their rows, and a list's heading when none is left
function pairsSettle(only){for(const [key,t] of pairTimers)if(!only||key===only){clearTimeout(t);pairTimers.delete(key)}
 const gone=key=>pairSaid.has(key)&&(!only||key===only);for(const k of ['p','o'])pairRows[k]=pairRows[k].filter(([key])=>!gone(key));
 for(const list of [$('#people-view'),graphKept?.f].flatMap(v=>v?[...v.querySelectorAll('.graph-list[data-pairs]')]:[])){  /* the lists shown, and the ones a search put aside */
  for(const row of list.querySelectorAll('.same-pair[data-pair]'))if(gone(row.dataset.pair))row.remove();
  const left=list.querySelectorAll('.same-pair').length,head=list.previousElementSibling?.matches('.section-head')?list.previousElementSibling:null;
  if(!left){head?.remove();list.remove()}else if(left<2)head?.querySelector('.same-all')?.remove()}}
// The answer on the row at once, its buttons back if saving it failed; a moment later the row fades and goes
function pairAnswer(box,key,said){pairSaid.set(key,said);clearTimeout(pairTimers.get(key));
 pairTimers.set(key,setTimeout(()=>{for(const r of document.querySelectorAll('#people-view .same-pair[data-pair]'))if(r.dataset.pair===key)r.classList.add('pair-leaving');
  pairTimers.set(key,setTimeout(()=>pairsSettle(key),250))},PAIR_SHOW_MS));
 const row=box?.querySelector('.role-row'),was=row&&[...row.childNodes];if(row)row.replaceChildren(make('span',{class:'muted pair-said'},said));
 const head=box?.closest('.graph-list[data-pairs]')?.previousElementSibling?.querySelector('.count');if(head)head.textContent=Math.max(0,+head.textContent-1);
 return ()=>{clearTimeout(pairTimers.get(key));pairTimers.delete(key);pairSaid.delete(key);box?.classList.remove('pair-leaving');if(row)row.replaceChildren(...was);if(head)head.textContent=+head.textContent+1}}
const pairDone=s=>html`<p class="graph-sub role-row"><span class="muted pair-said">${s.said}</span></p>`;
const sameAsk=n=>html`${(n.same||[]).filter(s=>s.name).map(s=>html`<div class="same-ask"><p class="graph-sub">Same person as ${nodeButton({id:s.id,name:s.name})}?<br><span class="muted">${sameWhy(s.why)}${s.from?html` · <span class="mono">${s.from}</span>`:''}</span></p>${pairSaid.has(pairKey('p',n.id,s.id))?pairDone({said:pairSaid.get(pairKey('p',n.id,s.id))}):html`<p class="graph-sub role-row"><button data-same="1" data-a="${n.id}" data-b="${s.id}">Merge</button><button class="ghost" data-same="0" data-a="${n.id}" data-b="${s.id}">Not the same</button></p>`}</div>`)}`;
const joinedRow=n=>n.joined?.length?html`<details class="joined"><summary class="graph-sub">Joined from ${n.ids?.length||n.joined.length+1} identities</summary>${n.joined.map(j=>html`<div class="graph-sub relation"><span><span class="mono">${j.a_shown}</span> and <span class="mono">${j.b_shown}</span> · <span class="muted">${j.why}</span></span><button class="ghost" data-same="0" data-a="${j.a}" data-b="${j.b}" data-split>Undo</button></div>`)}</details>`:'';
const sameList=(found,items=pairsSteady('p',found),open=items.filter(s=>!s.said))=>html`${contactsInList()}${items.length?html`<div class="section-head"><h2>Same person?</h2><span class="count">${open.length}</span>${items.length>1?html`<button type="button" class="ghost same-all${open.length>1?'':' spent'}" data-same-all="${JSON.stringify(open.map(s=>[s.a.id,s.b.id]))}" ${open.length>1?'':'disabled'}>Merge all</button>`:''}<p>Possible doubles. Merge them or keep them apart.</p></div><div class="graph-list" data-pairs="p">${items.map(s=>html`<article class="same-pair" data-pair="${pairKey('p',s.a.id,s.b.id)}"><div class="graph-row">${personPic(s.a)}${nodeButton(s.a)}<span class="muted">and</span>${personPic(s.b)}${nodeButton(s.b)}</div><p class="graph-sub">${s.why} · <span class="mono">${[s.a.ids?.[0],s.b.ids?.[0]].filter(Boolean).join(', ')}</span></p>${s.said?pairDone(s):html`<p class="graph-sub role-row"><button data-same="1" data-a="${s.a.id}" data-b="${s.b.id}">Merge</button><button class="ghost" data-same="0" data-a="${s.a.id}" data-b="${s.b.id}">Not the same</button></p>`}</article>`)}</div>`:''}`;
// Sharing a contact (contact_share.py): from a person's page (⋯, Share contact…) or About you (Share my contact), to one
// teammate, friend or Family member. Pick the fields, look at exactly what goes, then Send. A Personal or private
// contact needs one more tick. Contacts shared here wait under People: Add (or add to the person you have) or Dismiss.
let cs=null,graphContactsIn=[];
const csFields=o=>[...o.emails.map(v=>['emails',v,'Email']),...o.phones.map(v=>['phones',v,'Phone']),...(o.org?[['org',o.org,'Organization']]:[]),...(o.role?[['role',o.role,'Role']]:[])];
const csPick=()=>{const f=$('#contact-share-form'),pick={emails:[],phones:[]};for(const i of f.querySelectorAll('[data-cs-field]:checked')){const k=i.dataset.csField;k==='org'||k==='role'?pick[k]=true:pick[k].push(i.value)}return pick};
const csWhere=t=>t.kind==='work'?`${t.where}`:t.where;
const csLands=k=>k==='work'?'It shows in their Graph, marked shared by you, for them to add or dismiss.':'It shows as a suggestion to add, for them to add or dismiss.';
function csDraw(){const f=$('#contact-share-form'),o=cs.options,t=o.targets,head=html`<div class="snooze-heading"><h2 id="contact-share-title">${cs.own?'Share my contact':'Share '+o.name}</h2><button type="button" data-cs-close aria-label="Close">×</button></div>`;
 if(cs.preview){const p=cs.preview;setHTML(f,html`${head}<p class="sp-line">${p.to} gets exactly this:</p><div class="cs-card">${p.rows.map(r=>kv(r.label,r.label==='Note'?`“${r.value}”`:r.value))}</div><p class="fleet-fine">${csLands(p.kind)} Encrypted for their Machine only.</p><p class="ed-note warn" data-cs-error role="alert" hidden></p><div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-cs-back>Back</button><button class="primary">Send</button></div>`);return}
 const sent=(cs.sent||[]).slice(0,3).map(s=>`${s.name}: ${s.state}`).join(' · ');
 setHTML(f,html`${head}<label class="ed-field">To<select data-cs-to>${t.map((x,i)=>html`<option value="${i}"${i===cs.to?html` selected`:''}>${x.name} · ${csWhere(x)}</option>`)}</select></label><fieldset class="sp-people cs-fields"><legend>What goes</legend><label><input type="checkbox" checked disabled> <span class="cs-row"><span class="muted">Name</span><span class="cs-v">${o.name}</span></span></label>${csFields(o).map(([k,v,l])=>html`<label><input type="checkbox" data-cs-field="${k}" value="${v}"${cs.on.has(k+'|'+v)?html` checked`:''}> <span class="cs-row"><span class="muted">${l}</span><span class="cs-v">${v}</span></span></label>`)}</fieldset><label class="ed-field">Why you two should talk <small>(optional)</small><input data-cs-note maxlength="300" value="${cs.note}" placeholder="You both work on onboarding"></label>${o.confirm?html`<label class="cs-confirm"><input type="checkbox" data-cs-confirm${cs.confirmed?html` checked`:''}> <span>${o.confirm==='personal'?'This is a Personal contact. Share it anyway.':'You keep this contact private. Share it anyway.'}</span></label>`:''}${sent?html`<p class="fleet-fine">Shared before: ${sent}</p>`:''}<p class="ed-note warn" data-cs-error role="alert" hidden></p><div class="ed-actions"><span class="grow"></span><button type="button" class="ghost" data-cs-close>Cancel</button><button class="primary"${o.confirm&&!cs.confirmed?html` disabled`:''}>Preview</button></div>`)}
async function csOpen(source){try{const o=await graphPost('fleet_contact_options',{node:source});if(!o.targets.length){toast('Join a Fleet or add a friend first.',true);return}
 cs={source,own:!!o.own,options:o,sent:o.sent,to:0,note:'',confirmed:false,preview:null,on:new Set(o.emails.slice(0,1).map(v=>'emails|'+v).concat(o.org?['org|'+o.org]:[]))};
 csDraw();const d=$('#contact-share');if(!d.open)d.showModal();d.querySelector('select')?.focus()}catch(e){errCaught(e);toast(e.message,true)}}
function csSync(){const f=$('#contact-share-form');if(!cs||cs.preview)return;cs.to=+f.querySelector('[data-cs-to]').value;cs.note=f.querySelector('[data-cs-note]').value;cs.confirmed=!!f.querySelector('[data-cs-confirm]')?.checked;
 cs.on=new Set([...f.querySelectorAll('[data-cs-field]:checked')].map(i=>i.dataset.csField+'|'+i.value));const b=f.querySelector('button.primary');if(b)b.disabled=!!cs.options.confirm&&!cs.confirmed}
$('#contact-share-form').addEventListener('change',csSync);$('#contact-share-form').addEventListener('input',csSync);
$('#contact-share-form').addEventListener('click',e=>{if(e.target.closest('[data-cs-close]'))$('#contact-share').close();if(e.target.closest('[data-cs-back]')){cs.preview=null;csDraw()}});
$('#contact-share-form').addEventListener('submit',async e=>{e.preventDefault();if(!cs)return;const f=e.currentTarget,btn=f.querySelector('button.primary'),err=f.querySelector('[data-cs-error]'),t=cs.options.targets[cs.to];btn.disabled=true;
 const args={node:cs.source,fleet:t.fleet,member_id:t.member_id,note:cs.note};
 try{if(!cs.preview){cs.pick=csPick();cs.preview=await graphPost('fleet_contact_preview',{...args,pick:cs.pick});csDraw();f.querySelector('button.primary').focus();return}
  const r=await graphPost('fleet_contact_send',{...args,pick:cs.pick,shown:cs.preview.digest,confirmed:cs.confirmed});$('#contact-share').close();toast(`Sent to ${r.to}.`)}
 catch(x){errCaught(x);err.textContent=x.message;err.hidden=false;btn.disabled=false}});
$('#contact-share').addEventListener('close',()=>{cs=null});
document.addEventListener('click',e=>{const b=e.target.closest('[data-contact-share]');if(!b)return;b.closest('details')?.removeAttribute('open');if(b.dataset.contactShare)csOpen(b.dataset.contactShare)});
// On a person's page: Share contact… in ⋯ when someone can get it, and "Shared by" when a share made or joined them.
function contactMarks(view,n){const list=view.querySelector('.person-page .person-menu .fact-menu-list');if(list&&n.can_share&&!list.querySelector('[data-contact-share]')){const item=document.createElement('button');item.type='button';item.setAttribute('role','menuitem');item.dataset.contactShare=n.id;item.textContent='Share contact…';list.prepend(item)}const m=n.shared_by,pv=view.querySelector('.person-page .person-view');
 if(m&&pv&&!pv.querySelector('.person-shared'))pv.prepend(htmlNodes(html`<p class="graph-sub person-shared">${m.kind==='work'?'Shared by':'Suggested by'} ${m.by}${m.note?`: “${m.note}”`:''}</p>`))}
// On a person's page, for someone found on the Network, in no Fleet, Family or Friends with the owner and with no open
// request (graph.network_marks): Add as a friend next to "Has a Machine", and Add as family in ⋯. Each sends what the
// Suggestions card's Connect sends: an ordinary friend request, nothing connects until they accept.
function friendMarks(view,n){const net=n.fleet?.network,list=view.querySelector('.person-page .person-menu .fact-menu-list');if(!net?.can_add||net.hint==='colleague'||!list||list.querySelector('[data-person-friend]'))return;
 const b=document.createElement('button');b.type='button';b.setAttribute('role','menuitem');b.dataset.personFriend='family';b.dataset.netEmail=net.email;b.textContent=t('Add as family');list.prepend(b)}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-person-friend]');if(!b)return;const page=b.closest('.person-page')||document;b.closest('details')?.removeAttribute('open');
 const all=()=>page.querySelectorAll('[data-person-friend]');all().forEach(x=>x.disabled=true);
 try{await fleetPost('fleet_network',{do:'connect',email:b.dataset.netEmail,relation:b.dataset.personFriend});all().forEach(x=>x.remove());
  const mark=page.querySelector('.person-about .fleet-mark');if(mark)mark.textContent=t('Has a Machine')+' · '+t('Friend request sent');
  toast(t('Friend request sent'));refresh()}catch(err){errCaught(err);all().forEach(x=>x.disabled=false);toast(err.message,true)}});
// Invite to The Machine, for someone with no Machine the owner knows of (family_invites.person_invite). With a mailbox
// that can send, the invite is a ready to-do on their page (person_invite_draft) and opens in the send dialog every
// email uses (openSend): nothing goes out until Send there. Without one: the words, to Copy or Open in email in the
// owner's own email app. Invite to your Family (when it fits) is on the page, under No Machine found.
const INVITE_SITE='https://themachine.computer';
const inviteWords=v=>({subject:t('Have a look at The Machine'),body:[v.first?t('Hi {},',v.first):t('Hi,'),t('I use The Machine, an AI assistant that turns my email and chats into to-dos and prepares the work. I think you would like it: {}',INVITE_SITE)].join('\n\n')});
function inviteFamilyGo(f){if(!state.manage_url)return html`<a class="link" href="${safeHref(f.url)}" target="_blank" rel="noopener">${t('Invite to your Family')}</a>`;
 return html`<form method="post" action="/_machine/account-hop" class="inline"><input type="hidden" name="to" value="family_invite"><input type="hidden" name="email" value="${f.email}"><input type="hidden" name="name" value="${f.name||''}"><button class="link">${t('Invite to your Family')}</button></form>`}
let machineInvite=null;
function machineInviteOpen(v){machineInvite=v;const w=inviteWords(v),d=$('#machine-invite'),mail=v.email?'mailto:'+encodeURIComponent(v.email)+'?subject='+encodeURIComponent(w.subject)+'&body='+encodeURIComponent(w.body):'';
 setHTML(d,html`<div class="snooze-heading"><h2 id="machine-invite-title">${t('Invite {} to The Machine',v.first||v.name||t('them'))}</h2><button type="button" data-mi-close aria-label="Close">×</button></div>
 <p class="fleet-fine">${t('What they get. Nothing is sent from here.')}</p>
 <div class="mi-preview">${v.email?html`<p class="muted">${t('To: {}',v.email)}</p>`:''}<p class="muted">${t('Subject: {}',w.subject)}</p>${w.body.split('\n\n').map(p=>html`<p>${p}</p>`)}</div>
 <p class="fleet-fine">${t('Once they have a Machine, Add as a friend shows here.')}</p>
 <div class="ed-actions"><span class="grow"></span><button type="button" class="${mail?'ghost':'primary'}" data-mi-copy>${t('Copy')}</button>${mail?html`<button type="button" class="primary" data-mi-mail="${mail}">${t('Open in email')}</button>`:''}</div>`);
 if(!d.open)d.showModal();d.querySelector(mail?'[data-mi-mail]':'[data-mi-copy]')?.focus()}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-machine-invite]');if(!b)return;let v;try{v=JSON.parse(b.dataset.machineInvite)}catch{return}
 if(!v.send){machineInviteOpen(v);return}
 b.disabled=true;try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'person_invite_draft',args:{node_id:v.node}})});
  await refresh();openSend(r.suggestion_id,r.revision)}catch(err){errCaught(err);toast(err.message,true)}finally{b.disabled=false}});
$('#machine-invite').addEventListener('click',async e=>{const d=$('#machine-invite');if(e.target===d||e.target.closest('[data-mi-close]')){d.close();return}
 const m=e.target.closest('[data-mi-mail]');if(m){location.href=m.dataset.miMail;d.close();return}
 if(e.target.closest('[data-mi-copy]')&&machineInvite){try{await navigator.clipboard.writeText(inviteWords(machineInvite).body);toast(t('Copied.'))}catch(err){errCaught(err);toast(t('Couldn’t copy automatically. Select the text to copy it.'),true)}}});
// Shared with you: at the top of People, until Add or Dismiss.
const contactsInList=()=>graphContactsIn.length?html`<div class="section-head"><h2>Shared with you</h2><span class="count">${graphContactsIn.length}</span><p>Contacts sent to you. Add them to your Graph or dismiss them.</p></div><div class="graph-list contacts-in">${graphContactsIn.map(c=>html`<article class="contact-in"><div class="graph-row">${personPic({name:c.card.name})}<strong>${c.card.name}</strong></div><p class="graph-sub">${c.kind==='work'?`Shared by ${c.from}`:`${c.from} suggests you add ${c.card.own?'them':'this contact'}`}${c.card.own?' · their own contact':''} · ${c.where}</p><p class="graph-sub muted">${c.rows.filter(r=>!['Name','Note'].includes(r.label)).map(r=>r.value).join(' · ')||'Name only'}</p>${c.card.note?html`<p class="graph-sub">“${c.card.note}”</p>`:''}${c.existing?html`<p class="graph-sub muted">You have ${c.existing.name}. Add puts what’s new on their page.</p>`:''}<p class="graph-sub role-row"><button data-contact-in="add" data-id="${c.id}">Add</button><button class="ghost" data-contact-in="dismiss" data-id="${c.id}">Dismiss</button></p></article>`)}</div>`:'';
document.addEventListener('click',async e=>{const b=e.target.closest('[data-contact-in]');if(!b)return;b.disabled=true;try{const r=await graphPost('fleet_contact_decide',{id:b.dataset.id,choice:b.dataset.contactIn});
 graphContactsIn=graphContactsIn.filter(c=>c.id!==b.dataset.id);toast(r.status==='dismissed'?'Dismissed.':r.status==='merged'?`Added to ${r.name}.`:`Added ${r.name}.`);await people(graphNode,true)}catch(x){errCaught(x);b.disabled=false;toast(x.message,true)}});
// Domains a review read as an email warm-up tool's traffic: out of the graph, listed here with Undo.
// Hidden senders: mail a mailing system sent (to a list, replies asked elsewhere, a company's own name) adds nobody to
// People until the owner writes back (mail_senders.py). A quiet entry under People lists them, a page at a time when it
// opens; Show as a person counts that address for good, from the next build.
const HIDDEN_WHY={list:'Sent to a list',reply_to:'Replies go elsewhere',company:'Sent as a company'};
const hiddenRow=h=>html`<article class="hidden-sender"><div class="hs-text"><strong>${h.name}</strong><p class="graph-sub">${t(HIDDEN_WHY[h.why]||'')} · ${t(['{} email','{} emails'],h.mails)} · <span class="mono">${h.address}</span></p></div><p class="hs-act"><button type="button" class="quiet hs-show" data-show-person="${h.id}">Show as a person</button></p></article>`;
const hiddenSenders=n=>n>0?(pager('graph:hidden_senders',cursor=>request('api/graph/list?list=hidden_senders&cursor='+encodeURIComponent(cursor)).then(r=>({items:r.items,next:r.next,total:r.total})),hiddenRow),html`<details class="hidden-senders"><summary class="graph-sub muted">Hidden senders <span class="count">(${n})</span></summary><p class="graph-note muted">Newsletters, receipts and other mailings. They show up once you write to them.</p>${pagerSlot('graph:hidden_senders','','graph-list')}</details>`):'';
const warmupList=items=>items?.length?html`<details class="warmup"><summary class="graph-sub">Hidden as warm-up (${items.length})</summary><p class="graph-sub muted">Mail from email warm-up tools, kept out of your Graph.</p>${items.map(w=>html`<div class="graph-sub relation"><span>${w.name||w.domain}${w.name&&w.name!==w.domain?html` <span class="muted">${w.domain}</span>`:''}</span><button class="ghost" data-warmup-undo="${w.domain}">Undo</button></div>`)}</details>`:'';
const openBetween=n=>{const o=n.open||{},row=(label,p)=>html`<div class="promise"><span class="grow">${label}: <a class="promise-link" href="${promiseHref(p)}">${p.what}</a>${p.due?html`<small>due ${day(p.due)}</small>`:''}</span><button data-promise="${p.id}" data-close="kept">Mark done</button><button class="ghost" data-promise="${p.id}" data-close="dropped">Not happening</button></div>`;
 const rows=[...(o.you_promised||[]).map(p=>row('You promised',p)),...(o.they_promised||[]).map(p=>row(n.kind==='person'?'They promised':p.who+' promised',p)),
  ...(o.cards||[]).map(c=>html`<div class="promise"><span class="grow">To-do: <a href="#card=${c.id}" translate="no">${c.title}</a>${c.due?html`<small>due ${day(c.due)}</small>`:''}</span></div>`)];
 return rows.length?html`<div class="section-head"><h2>Open between you</h2><span class="count">${rows.length}</span></div><article class="graph-open">${rows}</article>`:''};
// What is known about them: the facts about this person, organization or project live on its page (a fact's subject,
// never who sent the message it came up in). Each has a menu: Edit in place, Not about them (it is a general fact again,
// in Learning, Facts), Remove (deletes it everywhere). Add keeps one more in the owner's own words.
const shortName=n=>n.kind==='person'?String(n.name||'').split(/\s+/)[0]||n.name:n.name;
let knownAdd='';  // the record whose Add form is open
const knownForm=(attr,who,text='')=>html`<form class="known-form" ${attr}><textarea name="text" maxlength="240" rows="2" required aria-label="${t('What you know about {}',who)}" placeholder="${text?'':t('What you know about {}',who)}">${text}</textarea><span class="known-acts"><button type="button" class="quiet" data-known-cancel>${t('Cancel')}</button><button class="primary">${t('Save')}</button></span></form>`;
const knownAbout=n=>{const k=n.open?.known||[],who=shortName(n),adding=knownAdd===n.id;
 const row=f=>knownEdit===f.id?html`<li>${knownForm(html`data-known-save="${f.id}"`,who,f.text)}</li>`:html`<li><span>${f.text}${factMeta(f)}</span><details class="fact-menu"><summary aria-label="${t('Options for this fact')}" title="${t('Options')}">⋯</summary><div class="fact-menu-list" role="menu"><button type="button" role="menuitem" data-known-edit="${f.id}">${t('Edit')}</button><button type="button" role="menuitem" data-fact-unlink="${f.id}">${t('Not about {}',who)}<small>${t('Keeps it as a general fact')}</small></button><button type="button" role="menuitem" class="danger" data-fact-forget="${f.id}" data-who="${who}">${t('Remove')}<small>${t('Deletes it everywhere')}</small></button></div></details></li>`;
 return html`<div class="section-head graph-known-head"><h2>${t('Known about {}',who)}</h2>${k.length?html`<span class="count">${k.length}</span>`:''}${adding?'':html`<button type="button" class="quiet known-add" data-known-add aria-label="${t('Add something you know about {}',who)}">${t('Add')}</button>`}</div>${adding?knownForm('data-known-new',who):''}${k.length?html`<ul class="graph-known">${k.map(row)}</ul>`:''}`};
// Recent changes (record_log.py), folded above the Timeline; each ⋯ has the page's own fix. rcOpen keeps it open on redraws.
let rcOpen='';
const RC_SHOWN=3;
const rcDay=v=>{const d=new Date(v);return localeDate(d,DL,{day:'numeric',month:'short',...(d.getFullYear()!==new Date().getFullYear()?{year:'numeric'}:{})})};
const RC_SIDE={work:'Marked as a Work contact',personal:'Marked as a Personal contact'},RC_AI={details:'Details changed',crm:'Fields or tags changed',summary:'Summary line added'};
function rcText(n,x){switch(x.kind){
 case 'role':return t('Role: {}',cap(x.role));
 case 'role_fix':return t('Role: {}, corrected from {}',cap(x.role),x.was);
 case 'org':return t('Works at {}',x.org);
 case 'member':return t('{} works here',x.name);
 case 'relation':return t('{} is {} {}',x.a_name,x.relation,x.b_name);
 case 'joined':return t('Joined with {}',x.shown);
 case 'side':return t(RC_SIDE[x.side]||'');
 case 'move':return t('Moved to {}',x.stage);
 case 'done':return x.deal?t('Marked won'):t('Project marked done');
 case 'reopened':return t('Reopened: Done when changed');
 case 'ai':return x.parts.map(p=>t(RC_AI[p]||'')).filter(Boolean).join(' · ')+(x.undone?' · '+t('undone'):'');
 default:return x.text||''}}
function rcSource(s){if(!s)return'';
 if(s.type==='event'){const brand=!['email','meeting','message'].includes(s.via),label=s.via==='meeting'?t('A meeting'):s.via==='email'?(s.from?t('Email from {}',s.from):s.mine?t('Your email'):t('An email')):
   brand?(s.from?t('{} message from {}',s.via,s.from):s.mine?t('Your {} message',s.via):t('A {} message',s.via)):(s.from?t('Message from {}',s.from):s.mine?t('Your message'):t('A message'));
  return html`<button type="button" class="link" data-quote-event="${s.id}" title="${t('Read the message')}">${label}</button>`}
 if(s.type==='note')return s.card?html`<a href="#card=${s.card}" title="${s.title||''}">${t('Your note')}</a>`:t('Your note');
 if(s.type==='ai')return s.name?t('From {}',s.name):'';
 if(s.type==='quote')return html`<span translate="no">“${s.text}”</span>`;
 return s.via==='LinkedIn headline'?t('Their LinkedIn headline'):''}
function rcMenu(n,x){const a=x.act||{},who=shortName(n),items=[];
 if(x.kind==='fact')items.push(html`<button type="button" role="menuitem" data-fact-unlink="${x.fact}">${t('Not about {}',who)}<small>${t('Keeps it as a general fact')}</small></button>`,html`<button type="button" role="menuitem" class="danger" data-fact-forget="${x.fact}" data-who="${who}">${t('Remove')}<small>${t('Deletes it everywhere')}</small></button>`);
 if(a.edit)items.push(html`<button type="button" role="menuitem" data-org-edit>${t('Edit')}</button>`);
 if(a.unrelate)items.push(html`<button type="button" role="menuitem" data-unrelate="${a.unrelate[0]}" data-related-to="${a.unrelate[1]}">${t('Remove')}</button>`);
 if(a.split)items.push(html`<button type="button" role="menuitem" data-same="0" data-a="${a.split[0]}" data-b="${a.split[1]}" data-split>${t('Undo')}<small>${t('Splits them for good')}</small></button>`);
 if(a.reopen)items.push(html`<button type="button" role="menuitem" data-rc-reopen="${a.reopen}">${t('Undo')}<small>${t('Opens it again')}</small></button>`);
 if(a.stage)items.push(html`<button type="button" role="menuitem" data-rc-stage="${a.stage}">${t('Undo')}<small>${t('Back to {}',a.stage)}</small></button>`);
 if(a.ai_undo)items.push(html`<button type="button" role="menuitem" data-rc-ai-undo="${a.ai_undo}">${t('Undo')}</button>`);
 return items.length?html`<details class="fact-menu rc-menu"><summary aria-label="${t('Options for this change')}" title="${t('Options')}">⋯</summary><div class="fact-menu-list" role="menu">${items}</div></details>`:''}
const recentLog=n=>{const log=n.log||[];if(!log.length)return'';
 return html`<section class="record-log" id="record-log"><details class="rc-fold"${rcOpen===n.id?html` open`:''}><summary class="graph-sub"><span>${t('Recent changes')}</span> <span class="count">${log.length}</span></summary><ul class="rc-list">${log.map((x,i)=>{const src=rcSource(x.source);
  return html`<li${i>=RC_SHOWN?html` hidden`:''}><time datetime="${x.at}">${rcDay(x.at)}</time><span class="rc-text">${rcText(n,x)}</span>${x.was?html`<small class="rc-was">${t('Was: {}',x.was)}</small>`:''}${src?html`<small class="rc-src">${src}</small>`:''}${rcMenu(n,x)}</li>`})}</ul>${log.length>RC_SHOWN?html`<button type="button" class="ghost rc-more" data-rc-more>${t('Show more')}</button>`:''}</details></section>`};
$('#people-view').addEventListener('click',async e=>{const box=e.target.closest('.record-log');if(!box)return;
 if(e.target.closest('[data-rc-more]')){for(const li of box.querySelectorAll('.rc-list li[hidden]'))li.hidden=false;e.target.closest('[data-rc-more]').remove();return}
 const item=e.target.closest('.rc-menu [role=menuitem]');if(item)item.closest('details').open=false;
 const back=e.target.closest('[data-rc-stage]');if(back){back.disabled=true;try{await graphPost('graph_stage',{node_id:graphNode,stage:back.dataset.rcStage});toast(t('Moved back to {}.',back.dataset.rcStage));await people(graphNode,true)}catch(err){errCaught(err);back.disabled=false;toast(err.message,true)}return}
 const reopen=e.target.closest('[data-rc-reopen]');if(reopen){reopen.disabled=true;try{await graphPost('project_outcome',{node_id:reopen.dataset.rcReopen,outcome:null,reason:''});toast(t('Reopened.'));await people(graphNode,true)}catch(err){errCaught(err);reopen.disabled=false;toast(err.message,true)}return}
 const ai=e.target.closest('[data-rc-ai-undo]');if(ai){ai.disabled=true;try{await sharePost('ai_undo',{id:+ai.dataset.rcAiUndo});toast(t('Undone.'));await people(graphNode,true)}catch(err){errCaught(err);ai.disabled=false;toast(err.message,true)}}},true);
$('#people-view').addEventListener('toggle',e=>{if(e.target.matches?.('.rc-fold'))rcOpen=e.target.open?graphNode:''},true);
// The timeline on a person, project or organization: every source in one list by day, each row its source, who wrote it,
// when, and the start of the text; cards, promises and project moves among them. Filter by source; Show more loads more.
const GRAPH_SOURCE={docs:html`<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/>`,intercom:html`<path d="M5 5h14v10H9l-4 4z"/>`,zoom:html`<rect x="3" y="7" width="12" height="10" rx="2"/><path d="m15 11 6-3v8l-6-3z"/>`,
 telegram:html`<path d="m3 11 18-7-3 16-6-5-3 4v-6z"/>`,card:html`<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 9h8M8 13h5"/>`,
 promise:html`<path d="m5 12 4 4 10-10"/>`,move:html`<path d="M4 12h14M13 6l6 6-6 6"/>`};
const graphSource=k=>k==='salesflare.email'?'gmail':k==='salesflare.meeting'?'calendar':kindService(k);
const sourceIcon=(k,type)=>{const s=type&&type!=='event'?type:graphSource(k);return GRAPH_SOURCE[s]?html`<span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24">${GRAPH_SOURCE[s]}</svg></span>`:icon(s)};
const SOURCE_NAME={gmail:'Email',salesflare:'Email',calendar:'Calendar',whatsapp:'WhatsApp',slack:'Slack',intercom:'Intercom',linkedin:'LinkedIn',android:'Phone',x:'X',github:'GitHub',stripe:'Stripe',zoom:'Zoom',telegram:'Telegram',docs:'Docs'};
const TL_SOURCES={email:'Email',meetings:'Meetings',intercom:'Intercom',chats:'Chats',cards:'To-dos',projects:'Projects',other:'Other'};
const dayLabel=d=>{const t=new Date(),y=new Date(t),m=new Date(t);y.setDate(t.getDate()-1);m.setDate(t.getDate()+1);const same=(a,b)=>a.toDateString()===b.toDateString();return same(d,t)?'Today':same(d,y)?'Yesterday':same(d,m)?'Tomorrow':localeDate(d,DL,{weekday:'short',day:'numeric',month:'short',...(d.getFullYear()!==t.getFullYear()?{year:'numeric'}:{})})};
// A run of chat messages in one conversation (same thread, same day, under half an hour apart) is one row.
const GRAPH_GAP=30*6e4,GRAPH_ROWS=15;
const graphRuns=rows=>{const out=[];for(const e of rows){const run=out[out.length-1],prev=run?.at(-1);
  if(e.thread&&prev?.thread===e.thread&&new Date(prev.occurred_at).toDateString()===new Date(e.occurred_at).toDateString()&&Math.abs(Date.parse(prev.occurred_at)-Date.parse(e.occurred_at))<GRAPH_GAP)run.push(e);else out.push([e])}return out};
const graphTime=d=>fmtHM(d);
// The page's timeline as loaded so far: its source filter, the rows shown and the cursor of the next page.
let graphTl={node:'',source:'',shown:GRAPH_ROWS,next:null,sources:null,items:null,loading:false};
const PROMISE_STATE={open:'Open',carded:'Open',kept:'Done',dropped:'Dropped',answered:'Done'};
const tlRow=(n,e,later)=>{const d=new Date(e.occurred_at),t=html`<time datetime="${e.occurred_at}">${graphTime(d)}</time>`,mark=(label,c)=>html`<span class="chip ge-state" style="--c:var(${c})">${label}</span>`;
 if(e.type==='card')return html`<article class="graph-event ge-item" data-tl="card" tabindex="0" aria-label="To-do: ${e.title}"${later}>${sourceIcon('',e.type)}<div class="ge-main"><div class="ge-head"><h4 title="${e.title}" translate="no"><a href="#card=${e.id}">${e.title}</a></h4>${mark(e.done?'Done':'Open',e.done?'--faint':'--mint')}${t}</div><p class="ge-preview">To-do</p></div></article>`;
 if(e.type==='promise'){const who=e.mine?'You promised':n.kind==='person'?'They promised':`${shortName({kind:'person',name:e.who})||'They'} promised`;
  return html`<article class="graph-event ge-item" data-tl="promise" tabindex="0" aria-label="${who}: ${e.what}"${later}>${sourceIcon('',e.type)}<div class="ge-main"><div class="ge-head"><h4>${who}</h4>${mark(PROMISE_STATE[e.status]||'Open',PROMISE_STATE[e.status]==='Open'||!PROMISE_STATE[e.status]?'--mint':'--faint')}${t}</div><p class="ge-preview"><a class="promise-link" href="${promiseHref(e)}">${e.what}</a></p></div></article>`}
 if(e.type==='move')return html`<article class="graph-event ge-item" data-tl="move" tabindex="0" aria-label="${e.project}: ${e.stage}"${later}>${sourceIcon('',e.type)}<div class="ge-main"><div class="ge-head"><h4 title="${e.project}"><a href="${graphHash(e.project_id)}">${e.project}</a></h4>${t}</div><p class="ge-preview">Moved to ${e.stage}</p></div></article>`;
 return ''};
const tlLink=e=>/^docs\./.test(e.kind||'')&&e.source_url?html`<a class="ge-link" href="${safeHref(e.source_url)}" target="_blank" rel="noopener">Open the doc</a>`:e.kind==='intercom.conversation'&&e.source_url?html`<a class="ge-link" href="${safeHref(e.source_url)}" target="_blank" rel="noopener">Open in Intercom</a>`:e.kind==='zoom.summary'&&e.source_url?html`<a class="ge-link" href="${safeHref(e.source_url)}" target="_blank" rel="noopener">Summary</a>`:'';
// A meeting opens in its details (openMeeting); one with notes or a transcript says so on its row
const meetingAttr=e=>e.kind==='calendar.event'?' data-meeting':e.meeting_id?html` data-meeting="${e.meeting_id}"`:'';
const meetingMarks=e=>e.kind==='calendar.event'?orEmpty(html`${[e.notes&&'Notes',e.transcript&&'Transcript'].filter(Boolean).map(x=>html`<span class="chip ge-mark">${t(x)}</span>`)}`):'';
const soonRow=(n,e,later)=>{if(e.type&&e.type!=='event')return tlRow(n,e,later);const d=new Date(e.occurred_at),src=SOURCE_NAME[graphSource(e.kind)]||'';
 return html`<article class="graph-event" data-event="${e.id}"${meetingAttr(e)} tabindex="0" aria-label="${src?t(src)+': ':''}${e.title}"${later}>${sourceIcon(e.kind)}<div class="ge-main"><div class="ge-head"><h4 title="${e.title}" translate="no">${e.title}</h4><time datetime="${e.occurred_at}">${dayLabel(d)+' · '+(e.all_day?'All day':graphTime(d))}</time></div>${e.preview||meetingMarks(e)?html`<p class="ge-preview">${meetingMarks(e)}${e.preview||''}</p>`:''}</div></article>`};
// What teammates shared (n.team) is in the Timeline, under Mine · Team; a thread opens like an own one.
let tlWhose=sideStore.get('tl-whose')||'team';
const TEAM_KIND={meetings:'calendar.event',intercom:'intercom.conversation',chats:'slack.message'};
const teamItems=(n,src)=>{const x=n.team;return x&&tlWhose==='team'?[...(src?[]:x.timeline.map(l=>({team:'line',occurred_at:l.at,line:l.line,via:l.via}))),...x.threads.filter(r=>!src||src===r.kind).map(r=>({...r,team:'thread',occurred_at:r.at}))]:[]};
const whoseSwitch=n=>n.team&&(n.team.timeline.length||n.team.threads.length)?html`<div class="view-mode ge-whose" role="group" aria-label="Whose">${[['mine','Mine'],['team','Team']].map(([v,l])=>html`<button type="button" data-tl-whose="${v}" aria-pressed="${v===tlWhose}">${l}</button>`)}</div>`:'';
const teamRow=(e,d,later)=>{const line=e.team==='line',kind=TEAM_KIND[e.kind]||'gmail.message',head=line?e.line:e.subject||t('(no subject)');
 return html`<article class="graph-event ge-team${line?' ge-change':''}"${line?'':html` data-team-thread="${e.id}" data-title="${head}" tabindex="0" aria-label="${t(SOURCE_NAME[graphSource(kind)])}: ${head}"`}${later}>${line?html`<span class="ge-dot" aria-hidden="true">•</span>`:sourceIcon(kind)}<div class="ge-main"><div class="ge-head"><h4>${head}</h4><span class="ge-meta">${e.messages>1?t(['{} message','{} messages'],e.messages)+' · ':''}${String(e.occurred_at).length>10?graphTime(d)+' · ':''}${t('via {}',e.via)}</span></div>${!line&&e.preview?html`<p class="ge-preview">${e.from?html`<b>${shortName({kind:'person',name:e.from})||e.from}: </b>`:''}${e.preview}</p>`:''}</div></article>`};
const teamFiles=(id,fs)=>fs.length?html`<ul class="team-files">${fs.map(x=>html`<li>${x.file&&!x.waiting?html`<a href="api/team-file?thread=${encodeURIComponent(id)}&file=${x.file}" download>${x.name}</a>`:html`<span>${x.name}</span>`}<small class="muted">${x.not_shared?'not shared (Careful)':x.too_large?'too large to share':x.waiting?'on its way':fileSize(x.size)}</small></li>`)}</ul>`:'';
async function openTeamThread(id,title){const box=$('#email-content');$('#email-title').textContent=title||t('Conversation');setHTML(box,html`<p class="muted">Loading…</p>`);if(!$('#email-dialog').open)$('#email-dialog').showModal();
 let th;try{th=await request('api/graph?thread='+encodeURIComponent(id))}catch(err){errCaught(err);setHTML(box,html`<p class="muted">${err.message}</p>`);return}
 const list=(th.messages||[]).map(m=>({kind:'email',near:true,from:m.from,to:m.to,cc:m.cc,occurred_at:m.at,body:m.body,files:m.attachments||[]}));
 setHTML(box,html`${list.map((o,i)=>html`<div class="email" data-msg="${i}">${messageHTML(o,'',i)}${teamFiles(id,o.files)}</div>`)}`);
 box.querySelectorAll('.email').forEach(d=>fillMessage(d,list[+d.dataset.msg],''))}
const graphEvents=(n,title='Timeline')=>{if(n.head_only)return html`<section class="graph-timeline"><div class="section-head"><h2>${title}</h2></div><p class="pager-loading" role="status">Loading…</p></section>`;  /* the head came first; the timeline is on its way */
 const soon=Date.now(),tl=n.timeline,all=[...(n.recent||[]).map(e=>e.occurred_at?e:{...e,occurred_at:e.at}),...(tl?.source?[]:(n.changes||[]).map(c=>({change:changeText(c),occurred_at:c.at}))),...teamItems(n,tl?.source)].sort((a,b)=>Date.parse(b.occurred_at)-Date.parse(a.occurred_at)).filter(e=>!(Date.parse(e.occurred_at)>soon));
 /* Coming up apart, soonest first; the timeline itself strictly back in time from now */
 const up=[...(tl?.upcoming||[]),...(n.recent||[]).filter(e=>Date.parse(e.occurred_at||e.at)>soon&&!(tl?.upcoming||[]).some(u=>u.id===e.id))].map(e=>e.occurred_at?e:{...e,occurred_at:e.at}).sort((a,b)=>Date.parse(a.occurred_at)-Date.parse(b.occurred_at));
 const chips=tl?.sources&&Object.keys(tl.sources).length>1?subTabs('Show','data-tl-source',[{id:'',label:'All'},...Object.keys(TL_SOURCES).filter(k=>tl.sources[k]).map(k=>({id:k,label:TL_SOURCES[k]}))],tl.source||''):'';
 const sw=whoseSwitch(n),head=count=>html`<div class="section-head"><h2>${title}</h2>${count?html`<span class="count">${count}</span>`:''}${sw}</div>`;if(sw)graphTl.page=n;
 const soonBox=up.length?html`<div class="ge-soon"><h3 class="ge-day">Coming up</h3><div class="ge-group">${up.map((e,i)=>soonRow(n,e,i>=GE_SOON?' hidden':''))}</div>${up.length>GE_SOON?html`<button type="button" class="ghost ge-more" data-ge-soon>Show all upcoming</button>`:''}</div>`:'';
 if(!all.length)return tl||up.length||sw?html`<section class="graph-timeline">${head(0)}${chips}${soonBox}${all.length||up.length?'':html`<p class="graph-sub muted ge-empty">Nothing here yet.</p>`}</section>`:'';
 let last='',h='';const shown=tl?Math.max(GRAPH_ROWS,tl.shown||0):GRAPH_ROWS;
 const runs=graphRuns(all);
 runs.forEach((run,i)=>{const e=run[0],d=new Date(e.occurred_at),label=dayLabel(d),later=i>=shown?' hidden':'';
  if(label!==last){h=html`${h}${html`${last?html`</div>`:''}<h3 class="ge-day"${later}>${label}</h3><div class="ge-group">`}`;last=label}
  if(e.team){h=html`${h}${teamRow(e,d,later)}`;return}
  if(e.change){h=html`${h}${html`<article class="graph-event ge-change"${later}><span class="ge-dot" aria-hidden="true">•</span><div class="ge-main"><div class="ge-head"><h4>${e.change}</h4><time datetime="${e.occurred_at}">${graphTime(d)}</time></div></div></article>`}`;return}
  if(e.type&&e.type!=='event'){h=html`${h}${tlRow(n,e,later)}`;return}
  const chat=e.dm||e.title===n.name&&e.from,src=SOURCE_NAME[graphSource(e.kind)]||'';
  if(e.thread&&(run.length>1||chat||e.title!==n.name)){  /* a conversation, newest first: e is the last message, run.at(-1) the first */
   const first=new Date(run.at(-1).occurred_at),many=run.length>1,span=graphTime(first)===graphTime(d)?graphTime(d):rangeText(graphTime(first),graphTime(d));
   const own=chat&&!e.place&&n.kind==='person';  /* one to one with this page's person: no title, the page says who */
   const with_=t('{} with {} (a chat)',t(src||'Chat'),shortName(n.kind==='person'?n:{kind:'person',name:e.from_me?run.find(m=>!m.from_me)?.from||e.title:e.from||e.title})),head=e.place||(chat?with_:e.title);
   const said=m=>html`<b>${m.from_me?'You':shortName({kind:'person',name:m.from||(n.kind==='person'?n.name:'')})||'Them'}: </b>${m.preview||''}`,lines=orEmpty(html`${run.slice(0,2).reverse().map(m=>html`<li>${said(m)}</li>`)}`);
   const meta=html`<span class="ge-meta"><time datetime="${first.toISOString()}">${many?`${run.length} messages · `:''}${span}</time></span>`;
   h=html`${h}${html`<article class="graph-event" data-event="${e.id}"${many?html` data-events="${run.map(m=>m.id).reverse().join(',')}" data-title="${head}" data-src="${src}"${own?'':html` data-group`}`:''} tabindex="0" aria-label="${own?with_:(src?t(src)+': ':'')+t(head)}${many?', '+t(['{} message','{} messages'],run.length):''}"${later}>${sourceIcon(e.kind)}<div class="ge-main"><div class="ge-head">${own?'':html`<h4 title="${e.title}">${head}</h4>`}${meta}${shareChip(e)}</div>${many?html`<ul class="ge-lines">${lines}</ul>`:e.preview?html`<p class="ge-preview">${said(e)}</p>`:''}${run.some(m=>m.probable)?html`<p class="ge-note">Probably part of it</p>`:''}</div></article>`}`;return}
  const head=e.place||(chat?(e.from_me?'You':e.from||(n.kind==='person'?n.name:e.title)):e.title);
  const by=!chat&&e.from&&!['calendar.event','zoom.summary','meeting.notes'].includes(e.kind)?(e.from_me?'You':e.from)+': ':'';
  const state=e.state?html`<span class="chip ge-state" style="--c:var(${e.state==='open'?'--mint':'--faint'})">${e.state==='open'?'Open':'Closed'}</span>`:'';
  h=html`${h}${html`<article class="graph-event" data-event="${e.id}"${meetingAttr(e)} tabindex="0" aria-label="${src?t(src)+': ':''}${t(head)}"${later}>${sourceIcon(e.kind)}<div class="ge-main"><div class="ge-head"><h4 title="${e.title}">${head}</h4>${state}<time datetime="${e.occurred_at}">${e.all_day?'All day':graphTime(d)}</time>${shareChip(e)}</div>${e.preview||meetingMarks(e)?html`<p class="ge-preview">${meetingMarks(e)}${by?html`<b>${by}</b>`:''}${e.preview||''}</p>`:''}${tlLink(e)?html`<p class="ge-note">${tlLink(e)}</p>`:''}${e.probable?html`<p class="ge-note">Probably part of it</p>`:''}</div></article>`}`});
 const more=runs.length>shown||tl?.next;
 return html`<section class="graph-timeline">${head(tl?(tl.source?tl.sources?.[tl.source]:tl.total)||runs.length:runs.length)}${chips}${soonBox}<div class="graph-events">${h}</div></div>${more?html`<button type="button" class="ghost ge-more" data-ge-more>Show more</button>`:''}</section>`};
// Show more: the rows already here first, then the next page; a source chip reloads the list for that source.
async function graphTlLoad(source,more){const n=graphTl.page;if(!n||graphTl.loading)return;graphTl.loading=true;
 try{const tl=n.timeline||{};const cursor=more?tl.next:'';const got=await request('api/graph/timeline?node='+encodeURIComponent(n.id)+'&source='+encodeURIComponent(source)+(cursor?'&cursor='+encodeURIComponent(cursor):''));
  if(graphTl.page!==n)return;n.recent=more?[...n.recent,...got.items]:got.items;n.timeline={...tl,next:got.next,sources:got.sources,total:got.total,upcoming:more?tl.upcoming:(got.upcoming||[]),source,shown:more?(tl.shown||GRAPH_ROWS)+30:GRAPH_ROWS};graphTlDraw()}
 catch(err){errCaught(err);toast(err.message,true)}finally{graphTl.loading=false}}
function graphTlDraw(){const box=$('#people-view .graph-timeline'),n=graphTl.page;if(!box||!n)return;const tmp=document.createElement('div');setHTML(tmp,graphEvents(n));box.replaceWith(tmp.firstElementChild);
 for(const p of $('#people-view').querySelectorAll('.graph-timeline .ge-preview'))p.classList.toggle('fade',p.scrollHeight>p.clientHeight+1)}
const teamMode=()=>teamOn()&&graphTeam;
const shareChip=e=>{const s=e.share;if(!s)return '';const t=s.share==='team'?'Team':s.people?.length?s.people[0]+(s.people.length>1?' +'+(s.people.length-1):''):'Only you';
 return html`<button type="button" class="share-chip${s.share==='team'||s.people?.length?html` on`:''}" data-share-event="${e.id}" data-share="${JSON.stringify({share:s.share,fixed:!!s.fixed,why:s.why||'',people:s.people||[]})}" title="${s.why}" aria-haspopup="dialog" aria-label="${t}: ${s.why}">${t}</button>`};
const shareNote=list=>html`${(list||[]).filter(s=>s.confirmed).map(s=>html`<p class="share-note muted">${s.off==='off'?`Your Work isn't shared with ${s.name} now.`:s.teammates===0?`Sharing starts once ${s.admin?'you OK':'an admin OKs'} a teammate's Machine. Personal never.`:!s.started?`Work goes to ${s.name} within the hour. Personal never.`:`Work is shared with ${s.name}. Personal never.`} <a href="#shared=${s.fleet}">See what's shared</a></p>`)}`;
const privateRow=n=>n.keep_private===undefined||n.team_only?'':html`<div class="keep-private"><button type="button" class="ghost" data-keep-private="${n.id}" data-private="${n.keep_private?'0':'1'}">${n.keep_private?'Share with the team again':'Keep private'}</button><small class="muted">${n.keep_private?'Only you see this and its threads.':n.shared_with_team?'Shared with your team.':'Not shared with your team yet.'}</small></div>`;
const askForm=(p,about)=>html`<details class="team-ask"><summary>Ask ${p.name||'them'}</summary><form class="team-ask-form" data-fleet="${p.fleet}" data-member="${p.member}" data-about="${about}"><textarea name="note" rows="2" maxlength="1000" aria-label="What to ask ${p.name||'them'}">Can you tell me where things stand with ${about}?</textarea><button class="primary">Ask</button></form></details>`;
const teamAsks=n=>{const people=(n.team?.people||[]).filter(p=>!p.left);return people.length?html`<div class="team-asks">${people.slice(0,3).map(p=>askForm(p,n.name))}</div>`:''};
const teamDetail=n=>{const [paneId,paneName]=GRAPH_KIND_PANE[n.kind]||GRAPH_KIND_PANE.person;
 const org=n.org_name&&n.org?html`<button class="node" data-node="${n.org}" title="${n.org_name}">${n.org_name}</button>`:n.org_name;  /* its organization's page, when this Machine has it */
 const sub=[n.role&&t(cap(n.role)),org,n.kind==='project'&&n.stage?n.board+': '+t(n.stage):'',n.last_at?htmlT('last contact {}',sinceTime(n.last_at)):''].filter(Boolean).flatMap((x,i)=>i?[' · ',x]:[x]);
 return html`<div class="graph-crumbs" role="navigation" aria-label="Breadcrumb"><a href="#graph" data-crumb="">Graph</a><span aria-hidden="true">›</span><a href="#graph=${paneId}" data-crumb="${paneId}">${paneName}</a><span aria-hidden="true">›</span><span aria-current="page">${n.name}</span></div><article class="graph-detail"><div class="name-row"><h3>${n.name}</h3></div><p class="graph-sub">${sub}</p>${projAbout(n)}${n.next?html`<p class="graph-sub">Next: ${n.next}</p>`:''}${crmFieldsSection(n)}${teamAsks(n)}</article>${graphEvents(n)}`};
const heldPane=items=>items?.length?html`<div class="section-head"><h2>Held back this week</h2><span class="count">${items.length}</span><p>Your team sees only that these exist, or nothing.</p></div><div class="graph-list">${items.map(x=>html`<article class="held-row"><div class="graph-row"><span class="ell" title="${x.title}">${x.title||'(no subject)'}</span>${shareChip({id:x.event_id,share:{share:'only_you',fixed:false,why:x.why}})}</div><p class="graph-sub">${[x.with,shortDay(x.at),x.why].filter(Boolean).join(' · ')}</p></article>`)}</div>`:html`<div class="empty all-clear"><div><strong>Nothing held back this week.</strong>Work went to your team as usual.</div></div>`;
$('#people-view').addEventListener('click',async e=>{
 const chip=e.target.closest('[data-share-event]');if(chip){e.stopPropagation();e.preventDefault();if($('#share-pop')?.dataset.for===chip.dataset.shareEvent)return sharePopClose();sharePop(chip);$('#share-pop').dataset.for=chip.dataset.shareEvent;return}
 const kp=e.target.closest('[data-keep-private]');if(kp){kp.disabled=true;const on=kp.dataset.private==='1';try{await graphPost('graph_private',{node_id:kp.dataset.keepPrivate,private:on});toast(on?'Kept private.':'Shared with your team again.');await people(graphNode,true)}catch(err){errCaught(err);kp.disabled=false;toast(err.message,true)}return}
},true);
const teamOpen=r=>openTeamThread(r.dataset.teamThread,r.dataset.title);
$('#people-view').addEventListener('click',e=>{const w=e.target.closest('[data-tl-whose]');if(w){tlWhose=w.dataset.tlWhose;sideStore.set('tl-whose',tlWhose);graphTlDraw();return}
 const r=e.target.closest('[data-team-thread]');if(r){e.stopPropagation();teamOpen(r)}},true);
$('#people-view').addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.matches?.('[data-team-thread]'))teamOpen(e.target)});
$('#people-view').addEventListener('submit',async e=>{const f=e.target.closest('.team-ask-form');if(!f)return;e.preventDefault();e.stopPropagation();const b=f.querySelector('button');b.disabled=true;
 try{await graphPost('graph_ask',{fleet:f.dataset.fleet,member_id:f.dataset.member,about:f.dataset.about,note:f.elements.note.value});toast('Asked.');f.closest('details').open=false}catch(err){errCaught(err);toast(err.message,true)}finally{b.disabled=false}},true);
$('#page-head').addEventListener('click',e=>{const b=e.target.closest('[data-graph-team]');if(!b)return;graphTeam=b.dataset.graphTeam==='team';sideStore.set('graph-team',graphTeam?'team':'mine');pageHead();people('')});
