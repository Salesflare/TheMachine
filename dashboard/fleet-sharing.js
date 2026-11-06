// What's shared (shared_graph.overview): one place per Work Fleet with counts, what went and why, Share these?, and what stays private.
// Loaded when its pane opens; every list item is the owner's own mail, shown as text.
// The consent an admin gives before the team's Graph starts, or before the Fleet requires its members' Work email or
// calendar: short and plain, with who is responsible. Resolves true on the OK.
function shareConsent(title,points,fine,ok){const d=$('#share-consent');$('#share-consent-title').textContent=title;
 setHTML($('#share-consent-body'),html`<ul>${points.map(x=>html`<li>${x}</li>`)}</ul>${fine?html`<p class="fleet-fine">${fine}</p>`:''}`);$('#share-consent-ok').textContent=ok;
 return new Promise(done=>{d.returnValue='';d.addEventListener('close',()=>done(d.returnValue==='ok'),{once:true});d.showModal()})}
const SHARE_ON_POINTS=name=>[`Each member's Machine shares Work contacts, projects and client email threads, with attachments, with the confirmed Machines in ${name}.`,
 'Personal, sensitive and automated mail never goes. Each person looks it over before their first share and can keep anything private.',
 'Teammates keep what they got. Unshare and Turn off can remove it from their Machines.'];
const sharedFleetName=fleet=>(fleetData?.fleets||[]).find(x=>x.id===fleet)?.name||'this Fleet';
const sharedWhen=at=>{if(!at)return 'soon';const d=new Date(at);return isNaN(d)||d<=new Date()?'soon':'from '+d.toLocaleDateString(DL,{weekday:'short'})+' '+fmtHM(d)};
let sharedData={},sharedShown={};
// What the sharing review sorted the Work threads into (shared_graph), each with where it goes; the title says what it is
const SHARED_TILES=[['client','Client','goes to the team','Threads with clients and partners'],['sensitive','Sensitive','not shared','Deals, HR, legal, health, money or security'],
 ['unsure','Not sure','you choose','Could be client work. Stays with you until you choose.'],['personal','Personal','not shared','Personal mail'],
 ['internal','Internal','not shared','Threads with only your colleagues on them'],['other','Not client','not shared','Receipts, alerts, newsletters and other mail']];
function sharedStatus(g,d){
 if(!g)return 'Sharing starts once your Machine is confirmed in this Fleet.';
 if(g.paused?.default)return 'Off. It\'s experimental, so it starts off until an admin turns it on.';
 if(g.paused)return t('Off for everyone, turned off by {}. Nothing new goes.',g.paused.by)+(g.paused.removed?' '+t('What went was removed from the team\'s Machines.'):'');
 if(!g.confirmed)return 'Nothing goes until an admin confirms your Machine.';
 if(g.off==='off')return 'Your Work isn\'t shared now. What went before stays with the team.';
 if(g.teammates===0)return 'Nothing goes until a teammate\'s Machine is confirmed.';
 if(!g.started)return 'Starts within the hour. Keep anything private first.';
 return 'On. Client threads go about an hour after they\'re sorted.'}
const sharedTitle=x=>x.event_id?html`<button type="button" class="shared-read ell" data-shared-read="${x.event_id}" title="${x.title}">${x.title||'(no subject)'}</button>`:html`<span class="ell" title="${x.title}">${x.title||'(no subject)'}</span>`;
const sharedRow=(x,act)=>html`<li class="shared-row"><span class="grow">${sharedTitle(x)}<small class="muted">${[x.why,x.at&&shortDay(x.at)].filter(Boolean).join(' · ')}</small></span>${act}</li>`;
const sharedAsking={};  // the admin's open "Turn off sharing for everyone?" per Fleet: it stays open through a reload
const CONN_LABEL={gmail:'Gmail',outlook:'Outlook',calendar:'Google Calendar',outlook_calendar:'Outlook Calendar',slack:'Slack',salesflare:'Salesflare',whatsapp:'WhatsApp',intercom:'Intercom',linkedin:'LinkedIn',x:'X',telegram:'Telegram'};
function sharedHTML(work,g,d){const n=x=>Number(x||0).toLocaleString(DL),fleet=work.id;
 const h=[html`<div class="fleet-box shared-status"><h3>${t('What\'s shared with {}',work.name)}</h3><p class="sub">${t(sharedStatus(g,d))}</p>`];
 const on=!g?.paused;
 if(g)h.push(html`<div class="shared-switch"><span class="grow"><strong>Share the Graph in this Fleet</strong><span class="exp-tag">Experimental</span><small>${[t(on?'On for everyone.':'Off for everyone.'),t('New and still changing.'),g.admin?'':t('Only an admin can change this.')].filter(Boolean).join(' ')}</small></span><button type="button" class="lookup-switch" role="switch" aria-checked="${on}" aria-label="Share the Graph in this Fleet" data-graph-switch="${fleet}"${g.admin?'':html` disabled`}></button></div>${g.admin&&on?html`<div class="shared-off-ask"${sharedAsking[work.id]?'':html` hidden`}><p><strong>Turn off sharing for everyone?</strong></p><p class="fleet-fine muted">Nothing new goes. What went stays on teammates' Machines, unless you remove it. Someone may have read it already.</p><div class="actions"><button type="button" class="primary" data-graph-pause="${fleet}" data-on="1">Turn off</button><button type="button" class="ghost" data-graph-pause="${fleet}" data-on="1" data-remove="1">Turn off and remove shared data</button><button type="button" class="ghost" data-off-cancel>Cancel</button></div></div>`:''}`);
 const req=g?.require||[],REQ={mail:'Work email',calendar:'Work calendar'};
 if(g?.admin)h.push(html`<div class="shared-require"><strong>Required by the Fleet</strong><small>Members can't turn these off. Threads they keep private stay private.</small>${Object.entries(REQ).map(([k,l])=>html`<label><input type="checkbox" data-graph-require="${k}" data-fleet="${fleet}"${req.includes(k)?html` checked`:''}> ${l}</label>`)}</div>`);
 else if(req.length)h.push(html`<p class="fleet-fine">${t(req.length>1?'{} requires your Work email and Work calendar.':req[0]==='mail'?'{} requires your Work email.':'{} requires your Work calendar.',work.name)} ${t('They belong to the company. Threads you keep private stay private.')}</p>`);
 h.push(html`<div class="shared-tiles">${SHARED_TILES.map(([k,label,hint,about])=>html`<div class="shared-tile" title="${t(about)}"><b>${n(d.sorted[k])}</b><span>${t(label)}</span><small>${t(hint)}</small></div>`)}<div class="shared-tile"><b>${n(d.unsorted)}</b><span>Not sorted yet</span><small>stays with you</small></div><div class="shared-tile sent"><b>${n(d.sent)}</b><span>Sent</span><small>threads the team has</small></div></div></div>`);
 const conns=g?.connections||[];
 if(conns.length)h.push(html`<div class="fleet-box shared-conns"><h3>Your connections</h3><p class="sub">${t('What feeds {}\'s Graph. {}\'s Work starts on. Other companies\' start off. Personal never goes.',work.name,work.name)}</p><ul class="list shared-list">${conns.map(c=>html`<li class="shared-row"><span class="grow"><span class="ell">${CONN_LABEL[c.service]||(c.service?service(c.service):'Connection')}${c.name||c.email?' · '+(c.name||c.email):''}</span><small class="muted">${c.personal?t('Personal, never shared'):c.required?t('Required by {}',work.name):t(c.company?'Work':c.on?'Other company, shared':'Other company, not shared')}</small></span>${c.personal?'':html`<button type="button" class="lookup-switch" role="switch" aria-checked="${!!c.on}" aria-label="${t('Share {}',c.email||c.service)}" data-graph-conn="${c.id}" data-fleet="${fleet}"${c.required?html` disabled`:''}></button>`}</li>`)}</ul></div>`);
 const pv=d.preview;
 if(pv&&g&&!g.started)h.push(html`<div class="fleet-box shared-first"><h3>Before the first share</h3><p class="sub">${pv.threads?t(['{} client thread with these organizations goes to the team. Keep any private first.','{} client threads with these organizations go to the team. Keep any private first.'],pv.threads):t('No client threads to share yet.')}</p>${pv.orgs.length?html`<ul class="list shared-list">${pv.orgs.map(o=>sharedRow({title:o.name,why:t(['{} thread','{} threads'],o.threads)},html`<button type="button" class="ghost" data-shared-rule="${o.key}" data-name="${o.name}" data-choice="private">Keep private</button>`))}</ul>${pv.more?html`<p class="fleet-fine muted">${t('And {} more.',pv.more)}</p>`:''}`:''}<div class="actions"><button type="button" class="ghost" data-graph-start="${fleet}">Share now</button></div><p class="fleet-fine muted">It goes by itself within the hour. Nothing to confirm.</p></div>`);
 h.push(html`<details class="fleet-box shared-how"${g?.started?'':html` open`}><summary><h3>How sharing works</h3></summary><dl class="shared-facts">${[
  ['Goes','Work records and client threads, with attachments.'],
  ['Sensitive','Deals, HR and hiring, legal, health, money, security. Nothing of it goes.'],
  ['Never','Personal mail, receipts, alerts and newsletters, internal threads with only colleagues, and what you keep private.'],
  ['Not sure','Stays with you until you choose.'],
  ['Shared boards','The people you pick get each project\'s full timeline: email, meetings, Intercom, chats, to-dos and moves.'],
  ['Who sees it',t('Confirmed Machines in {}. The Network can\'t read it.',work.name)],
  ['Someone leaves','They get nothing new. What they had stays.']].map(([k,v])=>html`<div><dt>${t(k)}</dt><dd>${t(v)}</dd></div>`)}</dl><p class="fleet-fine"><a class="learn" href="${HELP}team-graph" target="_blank" rel="noopener">Learn more</a></p></details>`);
 if(d.unsure.length)h.push(sharedAskHTML(d));
 const shown=sharedShown[work.id]||20,list=d.threads;
 h.push(html`<div class="fleet-box shared-out"><h3>${g?.started?'Shared':'Goes within the hour'} <span class="count">${n(d.shared+d.waiting)}</span></h3>${list.length?html`<ul class="list shared-list">${list.slice(0,shown).map(x=>sharedRow(x,html`<button type="button" class="ghost" data-shared-set="${x.event_id}" data-share="only_you"${g?.started?'':html` data-before="1"`}>${g?.started?'Unshare':'Keep private'}</button>`))}</ul>${list.length>shown||d.more?html`<button type="button" class="quiet" data-shared-more="${fleet}">Show more</button>`:''}`:html`<p class="muted">Nothing yet.</p>`}</div>`);
 const rules=d.rules.map(r=>html`<li class="shared-row"><span class="grow"><span class="ell">${r.name||r.key}</span><small class="muted">${r.choice==='private'?'Always only you':'Always share client threads'} · ${r.key}</small></span><button type="button" class="ghost" data-shared-rule="${r.key}" data-choice="none">Remove</button></li>`);
 const recs=d.records.map(r=>html`<li class="shared-row"><span class="grow"><span class="ell">${r.name}</span><small class="muted">${({org:'Organization',person:'Person',project:'Project'})[r.kind]||'Record'} and its threads</small></span><button type="button" class="ghost" data-shared-record="${r.node_id}">Share again</button></li>`);
 const hand=d.by_hand.map(x=>sharedRow(x.shared_with?.length?{...x,why:t('Only you and {}',namesLine(x.shared_with))}:x,html`<button type="button" class="ghost" data-shared-set="${x.event_id}" data-share="team">Share</button>`));
 h.push(html`<div class="fleet-box shared-kept"><h3>Kept private</h3>${rules.length||recs.length||hand.length?html`<ul class="list shared-list">${rules}${recs}${hand}</ul>`:html`<p class="muted">Nothing yet. Tap Team or Only you on any thread in the Graph.</p>`}</div>`);
 const ST={sharing:'Sharing',not_started:'Not shared yet',off:'Stopped, with an admin\'s OK',removed:'Taken out'};
 if(g?.admin)h.push(html`<div class="fleet-box shared-people"><h3>Teammates</h3><p class="sub">Who shares with ${work.name}. Only an admin sees this.</p>${(g.people||[]).length?html`<ul class="list shared-list">${g.people.map(p=>html`<li class="shared-row"><span class="grow"><span class="ell">${p.name}</span><small class="muted">${ST[p.state]||''}</small></span>${p.state==='removed'?html`<button type="button" class="ghost" data-graph-remove="${p.member}" data-back="1">Share again</button>`:html`<button type="button" class="ghost" data-graph-remove="${p.member}">Take out</button>`}</li>`)}</ul>`:''}</div>`);
 return html`${h}`}
// Share these?: what the review was unsure of, in groups of the same kind (shared_graph.unsure_groups), each with the
// choice the review suggests first. One tap decides a group; open it to leave threads out and choose for them later.
// Share with team goes to everyone in the Fleet; Share with… only to the teammates picked (sensitive ones too).
const SHARE_PICK={team:'Share with team',people:'Share with…',private:'Keep private'},sharedGroupOpen=new Set();  // groups the owner opened stay open through a reload
document.addEventListener('toggle',e=>{const d=e.target;if(d?.classList?.contains('shared-group-list')){const k=d.closest('.shared-group')?.dataset.sharedGroup??'';d.open?sharedGroupOpen.add(k):sharedGroupOpen.delete(k)}},true);
function sharedAskHTML(d){const who=(d.teammates||[]).length,groups=d.groups?.length?d.groups:[{name:'',suggest:null,count:d.unsure.length}];
 return html`<div class="fleet-box shared-ask"><h3>Share these?</h3><p class="sub">Not sure these are client work. They stay with you until you choose.</p><p class="fleet-fine muted">Share with team goes to everyone in the Fleet. Share with… goes only to the teammates you pick.</p>${groups.map(g=>{
  const rows=d.unsure.filter(x=>(x.group||'')===g.name);if(!rows.length)return '';
  const order=[...(g.suggest?[g.suggest]:[]),...['team','people','private'].filter(k=>k!==g.suggest)].filter(k=>k!=='people'||who);
  return html`<section class="shared-group" data-shared-group="${g.name}"><div class="shared-group-head"><strong class="ell">${g.name||t('Other threads')}</strong><span class="count">${Number(g.count).toLocaleString(DL)}</span></div>${g.suggest?html`<small class="muted shared-suggest">${t('Suggested: {}',t(SHARE_PICK[g.suggest]))}</small>`:''}<div class="actions">${order.map(k=>html`<button type="button" class="${k===g.suggest?'primary':'ghost'}" data-shared-many="${k}">${t(SHARE_PICK[k])}</button>`)}</div><details class="shared-group-list"${sharedGroupOpen.has(g.name)?html` open`:''}><summary>${t(['Show {} thread','Show {} threads'],rows.length)}</summary><ul class="list shared-list">${rows.map(x=>html`<li class="shared-row shared-pick"><input type="checkbox" checked value="${x.event_id}" data-shared-pick aria-label="${x.title||'(no subject)'}"><span class="grow">${sharedTitle(x)}<small class="muted">${[x.company||x.with,shortDay(x.at)].filter(Boolean).join(' · ')}</small></span></li>`)}</ul></details></section>`})}</div>`}
// Share with… for the picked threads of one group: the teammates chosen get them, nobody else on the team.
function sharedPeopleOpen(fleet,ids){const people=sharedData[fleet]?.teammates||[];
 spOpen({title:t(['Share {} thread with…','Share {} threads with…'],ids.length),action:'graph_share_many',args:{event_ids:ids,share:'people'},chosen:[],people,
  line:who=>t('Goes to {} only, also if sensitive. Not to the rest of the team.',who),
  done:who=>t(['Shared {} thread with {} only.','Shared {} threads with {} only.'],ids.length,who),after:()=>sharedLoad(fleet,true)})}
async function sharedLoad(fleet,quiet){const el=$('#fleet-view').querySelector(`[data-shared-fleet="${CSS.escape(fleet)}"]`);if(!el)return;
 const work=(fleetData?.fleets||[]).find(x=>x.id===fleet),g=(fleetData?.shared?.graph||[]).find(s=>s.fleet===fleet);
 const paint=()=>{setHTML(el,sharedHTML(work,g,sharedData[fleet]))};
 if(sharedData[fleet]&&quiet)paint();
 try{sharedData[fleet]=await request('api/graph?view=shared&fleet='+encodeURIComponent(fleet));paint()}catch(err){errCaught(err);setHTML(el,html`<p class="error">${err.message}</p>`)}}
function sharedOpen(fleet){document.querySelector('nav [data-tab="fleet"]').click();fleetShown.then(()=>{const view=$('#fleet-view'),pane=fleet?'shared-'+fleet:view.querySelector('[data-pane^="shared-"]')?.dataset.pane;if(!pane||!view.querySelector(`[data-pane="${CSS.escape(pane)}"]`))return toast('Sharing starts once you are in a Work Fleet.');showFleetPane(pane);view.scrollIntoView({block:'start',behavior:'smooth'})})}
// #shared=<fleet> from the weekly recap or a thread's marker: that Fleet's What's shared.
function openSharedLink(){const m=/^#shared=(fl_[0-9a-f]{16})$/.exec(location.hash);if(!m||!state.fleet?.on)return;history.replaceState(null,'',location.pathname+location.search);sharedOpen(m[1])}
// A connection's switch moves at once; the Machine saves it behind, and a failed save moves it back.
const graphConnBusy={};
async function graphConnFlip(b,fleet){const id=b.dataset.graphConn,on=b.getAttribute('aria-checked')!=='true';if(graphConnBusy[id])return;graphConnBusy[id]=true;
 const c=((fleetData?.shared?.graph||[]).find(s=>s.fleet===fleet)?.connections||[]).find(x=>x.id===id),was=c?.on;
 const set=v=>{if(c)c.on=v;const sw=b.isConnected?b:$('#fleet-view').querySelector(`[data-graph-conn="${CSS.escape(id)}"]`);if(sw)sw.setAttribute('aria-checked',String(!!v))};
 set(on);
 try{await graphPost('graph_connection',{fleet,account:id,on});toast(on?'Shared with the team.':'Not shared any more. Teammates\' Machines delete what it shared.')}
 catch(err){errCaught(err);set(was);toast(err.message,true)}
 finally{delete graphConnBusy[id]}}
fleetOn('click',async e=>{const go=e.target.closest('[data-shared-go]');if(go){e.preventDefault();showFleetPane('shared-'+go.dataset.sharedGo);return}
 const op=e.target.closest('[data-shared-open]');if(op){sharedOpen(op.dataset.sharedOpen);return}
 const more=e.target.closest('[data-shared-more]');if(more){const f=more.dataset.sharedMore;sharedShown[f]=(sharedShown[f]||20)+50;sharedLoad(f,true);return}
 const b=e.target.closest('[data-shared-set],[data-shared-many],[data-shared-rule],[data-shared-record],[data-graph-start],[data-graph-pause],[data-graph-switch],[data-off-cancel],[data-graph-conn],[data-graph-all],[data-graph-rekey-no],[data-graph-remove]');if(!b)return;
 const pane=b.closest('[data-shared-fleet]'),fleet=pane?.dataset.sharedFleet||b.dataset.fleet||b.dataset.graphStart||b.dataset.graphPause||b.dataset.graphSwitch||b.dataset.graphAll;
 const ask=b.closest('.fleet-box')?.querySelector('.shared-off-ask');
 if(b.dataset.graphSwitch&&b.getAttribute('aria-checked')==='true'){sharedAsking[fleet]=true;if(ask){ask.hidden=false;ask.querySelector('button')?.focus()}return}
 if(b.matches('[data-off-cancel]')){sharedAsking[fleet]=false;if(ask)ask.hidden=true;return}
 if(b.dataset.graphPause)sharedAsking[fleet]=false;
 if(b.dataset.graphPause&&b.dataset.remove&&!confirm('Remove everything shared in this Fleet from all Machines? Each person looks it over again before anything goes.'))return;
 if(b.dataset.graphRemove&&!b.dataset.back&&!confirm('Take them out of the team\'s Graph? Nothing new goes to their Machine. What they have stays with them.'))return;
 if(b.dataset.graphSwitch&&!await shareConsent(`Share the Graph in ${sharedFleetName(fleet)}?`,SHARE_ON_POINTS(sharedFleetName(fleet)),
   `As an admin, you confirm ${sharedFleetName(fleet)} may share this Work mail and has told its people. It's experimental: you can turn it off for everyone at any time.`,'Turn on'))return;
 if(b.dataset.graphRekeyNo&&!confirm('Not their Machine? It never gets the team\'s Graph. Tell them, so they can check their account.'))return;
 if(b.dataset.graphConn){graphConnFlip(b,fleet);return}
 b.disabled=true;
 try{let msg='Saved.';
  if(b.dataset.sharedSet){const to=b.dataset.share;const r=await graphPost('graph_share',{event_id:Number(b.dataset.sharedSet),share:to});msg=to==='team'?'Shared with your team.':b.dataset.before?'Kept private. It won\'t go.':'Unshared. Teammates\' Machines delete their copy. Someone may have read it already.';const s=r?.suggest||r?.result?.suggest;if(s)sharePopSuggest(b,s)}
  else if(b.dataset.sharedMany){const ids=[...(b.closest('.shared-group')||pane).querySelectorAll('[data-shared-pick]:checked')].map(i=>Number(i.value));const to=b.dataset.sharedMany;
   if(to==='people'){b.disabled=false;sharedPeopleOpen(fleet,ids);return}
   await graphPost('graph_share_many',{event_ids:ids,share:to==='team'?'team':'only_you'});msg=to==='team'?t('Shared {} with your team.',ids.length):t('Kept {} private.',ids.length)}
  else if(b.dataset.sharedRule){const c=b.dataset.choice;await graphPost('graph_rule',{key:b.dataset.sharedRule,choice:c,name:b.dataset.name||''});msg=c==='none'?'Rule removed.':`Threads with ${b.dataset.name||b.dataset.sharedRule} stay with you.`}
  else if(b.dataset.sharedRecord){await graphPost('graph_private',{node_id:b.dataset.sharedRecord,private:false});msg='Shared with your team again.'}
  else if(b.dataset.graphStart){await graphPost('graph_start',{fleet});msg='Shared. Client threads go to the team now.'}
  else if(b.dataset.graphPause){const remove=!!b.dataset.remove;await graphPost('graph_pause',{fleet,on:true,remove});msg=remove?'Sharing is off. Teammates\' Machines delete what they got.':'Sharing is off for everyone.'}
  else if(b.dataset.graphSwitch){await graphPost('graph_pause',{fleet,on:false});msg='Sharing is on for everyone.'}
  else if(b.dataset.graphAll){const box=b.closest('.fleet-box'),asks=[...(box?.querySelectorAll('[data-share-ok][data-kind="member"]')||[])].map(x=>x.closest('article')),n=asks.length,row=b.closest('.actions');
   asks.forEach(x=>x.hidden=true);if(row)row.replaceWith(htmlNodes(graphSendingLine(n)));
   try{const r=await graphPost('graph_share_all',{fleet});const done=r.done??r.result?.done??0;if(done)graphSent[fleet]=done;msg=done?'':'Nobody is waiting for it now.'}catch(err){errCaught(err);asks.forEach(x=>x.hidden=false);box?.querySelector('.graph-sending')?.remove();throw err}}
  else if(b.dataset.graphRemove){const back=!!b.dataset.back;await graphPost('graph_remove',{fleet,member:b.dataset.graphRemove,back});msg=back?'They get the team\'s Graph again.':'Taken out. Nothing new goes to them.'}
  else if(b.dataset.graphRekeyNo){await graphPost('graph_rekey_no',{fleet,member:b.dataset.graphRekeyNo});msg='Not shared with that Machine.'}
  if(msg)toast(msg);if(pane)await sharedLoad(fleet,true);if(b.dataset.graphStart||b.dataset.graphPause||b.dataset.graphSwitch||b.dataset.graphAll||b.dataset.graphRekeyNo||b.dataset.graphRemove){await fleetView(true);if(b.dataset.graphAll)graphSendingWatch();if(pane)await sharedLoad(fleet,true)}}catch(err){errCaught(err);b.disabled=false;if(b.isConnected)b.textContent=b.dataset.label||b.textContent;toast(err.message,true)}});
fleetOn('change',async e=>{const t=e.target;if(!t.matches?.('[data-graph-require]'))return;const box=t.closest('.shared-require'),fleet=t.dataset.fleet;
 if(t.checked){const what=t.dataset.graphRequire==='mail'?'Work email':'Work calendar',name=sharedFleetName(fleet);
  if(!await shareConsent(`Require everyone's ${what}?`,[`Members can't turn off their ${name} ${what} for the team's Graph. They see that ${name} requires it.`,
   'Personal, sensitive and automated mail still never goes, and anyone can keep a thread private.',
   ...((fleetData?.shared?.graph||[]).find(x=>x.fleet===fleet)?.paused?.default?[`This turns on sharing in ${name}.`]:[])],
   `Only accounts on ${name}'s own domains. As an admin, you confirm ${name} has told its people.`,'Require it')){t.checked=false;return}}
 const require=[...box.querySelectorAll('[data-graph-require]:checked')].map(i=>i.dataset.graphRequire);
 try{await graphPost('graph_policy',{fleet,require});toast(require.length?'Required for everyone in the Fleet.':'Nothing required.');await sharedLoad(fleet,true)}catch(err){errCaught(err);t.checked=!t.checked;toast(err.message,true)}});
fleetOn('change',e=>{const t=e.target,box=t.closest?.('.shared-group');if(!box||!t.matches('[data-shared-pick]'))return;
 const any=!!box.querySelector('[data-shared-pick]:checked');for(const x of box.querySelectorAll('[data-shared-many]'))x.disabled=!any});
// A thread's marker opens why it is or isn't shared, the switch, and a way to What's shared. After a switch that repeats
// itself with one company, it asks once whether to make that a rule.
function sharePopClose(){$('#share-pop')?.remove()}
function sharePopAt(anchor,body){sharePopClose();const p=document.createElement('div');p.id='share-pop';p.className='share-pop';p.setAttribute('role','dialog');p.setAttribute('aria-label','Sharing');setHTML(p,body);document.body.append(p);
 const r=anchor?.getBoundingClientRect?.();if(r&&r.width){const w=Math.min(300,innerWidth-32);p.style.width=w+'px';p.style.left=Math.max(16,Math.min(r.right-w,innerWidth-w-16))+'px';const below=r.bottom+6+p.offsetHeight<innerHeight;p.style.top=(below?r.bottom+6:Math.max(16,r.top-6-p.offsetHeight))+'px'}else p.classList.add('floating');
 p.querySelector('button')?.focus();return p}
function sharePop(chip){const s=JSON.parse(chip.dataset.share||'{}'),on=graphSharing.find(x=>x.confirmed),fleet=on?.fleet,before=on?.started===false;const team=s.share==='team';
 sharePopAt(chip,html`<p class="share-pop-why">${s.why||(team?'Shared with your team':'Only you')}</p>${s.people?.length?html`<p class="share-pop-why">Shared with ${namesLine(s.people)}</p>`:''}${s.fixed?'':html`<div class="actions"><button type="button" class="${team?'ghost':'primary'}" data-pop-set="${chip.dataset.shareEvent}" data-share="${team?'only_you':'team'}"${before?html` data-before="1"`:''}>${team?(before?'Keep private':'Unshare'):'Share with the team'}</button>${!team&&graphTeammates.length?html`<button type="button" class="ghost" data-pop-people="${chip.dataset.shareEvent}">Share with…</button>`:''}</div>`}${team&&!s.fixed&&!before?html`<p class="fleet-fine muted">Unsharing deletes teammates' copies. Someone may have read it already.</p>`:''}${fleet?html`<p class="fleet-fine"><a href="#shared=${fleet}">See what's shared</a></p>`:''}`)}
function sharePopSuggest(anchor,sug){const priv=sug.choice==='private';
 sharePopAt(anchor||$('#toast'),html`<p>${priv?`Always keep threads with ${sug.name} private?`:`Always share client threads with ${sug.name}?`}</p><div class="actions"><button type="button" class="primary" data-pop-rule="${sug.key}" data-name="${sug.name}" data-choice="${priv?'private':'team'}">Yes</button><button type="button" class="ghost" data-pop-close>No</button></div>`)}
document.addEventListener('click',async e=>{const p=$('#share-pop');if(!p)return;
 if(!p.contains(e.target)){if(!e.target.closest('[data-share-event]'))sharePopClose();return}
 if(e.target.closest('[data-pop-close]')||e.target.closest('a'))return sharePopClose();
 const pp=e.target.closest('[data-pop-people]');if(pp){const c=document.querySelector(`[data-share-event="${pp.dataset.popPeople}"]`);sharePopClose();threadShareOpen(pp.dataset.popPeople,JSON.parse(c?.dataset.share||'{}').people);return}
 const b=e.target.closest('[data-pop-set],[data-pop-rule]');if(!b)return;b.disabled=true;
 try{if(b.dataset.popSet){const to=b.dataset.share,r=await graphPost('graph_share',{event_id:Number(b.dataset.popSet),share:to});toast(to==='team'?'Shared with your team.':b.dataset.before?'Kept private. It won\'t go.':'Unshared. Teammates\' Machines delete their copy. Someone may have read it already.');
   const s=r?.suggest||r?.result?.suggest;if(s)sharePopSuggest(document.querySelector(`[data-share-event="${b.dataset.popSet}"]`),s);else sharePopClose();await people(graphNode,true)}
  else{const c=b.dataset.choice;await graphPost('graph_rule',{key:b.dataset.popRule,choice:c,name:b.dataset.name});sharePopClose();toast(c==='private'?`Threads with ${b.dataset.name} stay with you.`:`Client threads with ${b.dataset.name} go to the team.`);await people(graphNode,true)}}
 catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&$('#share-pop'))sharePopClose()});
