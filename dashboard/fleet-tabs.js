// Handoffs in one Work Fleet: the ones you handed to a teammate (asked, from fleet_out, as on the card's own line) and the
// ones a teammate hands you that wait under Suggestions. Open first; accepted and done ones after, quieter, three shown.
const HO_Q=/^Can you take this on: ([\s\S]*?)\? Their summary: “([\s\S]*?)”([\s\S]*)$/;
function fleetHandoffs(f,work,inFleet){const cards=new Set((state?.suggestions||[]).map(s=>s.id));
 const what=q=>{const m=HO_Q.exec(q||'');return m?[m[1]+(m[2]?`: “${m[2]}”`:''),m[3].trim()].filter(Boolean).join(' '):String(q||'')};
 const stage=a=>{const [st,...note]=String(a.answer||'').split(': ');const n=note.join(': ');
  if(a.withdrawn)return['Taken back','muted',true];
  if(['asked','waiting'].includes(a.status))return[a.no_ping?t('Waiting, they won’t get a ping'):t(a.delivered===false?'Waiting for an answer, not delivered yet':'Waiting for an answer'),'amber',false];
  if(a.status==='expired')return['No answer in time','orange',false];
  if(a.status==='declined'||st==='declined')return['Declined','orange',false,n];
  if(st==='done')return['Done','muted',true];
  if(st.startsWith('accepted'))return[st==='accepted'?'Accepted':'Accepted with a change','mint',true,n];
  return[st||a.status,'muted',true,n]};
 const rows=[
  ...(f.waiting||[]).filter(w=>w.kind==='handoff'&&inFleet(w,work)).map(w=>({who:'From '+w.name,text:what(w.question),st:['Waits for you','amber',false],at:w.at,href:/^q_[a-f0-9]{16}$/.test(w.id)?'#fleet='+w.id:''})),
  ...(f.asked||[]).filter(a=>a.kind==='handoff'&&inFleet(a,work)).map(a=>{const card=String(a.context||'').slice(8);return{who:'To '+a.name,text:what(a.question),st:stage(a),at:a.answered_at||a.at,href:cards.has(card)?'#card='+card:''}})];
 if(!rows.length)return'';
 const open=rows.filter(r=>!r.st[2]),quiet=rows.filter(r=>r.st[2]),shown=3;
 const row=(r,k)=>{const more=r.st[2]&&k>=shown,text=r.text+(r.st[3]?` · “${r.st[3].replace(/^“|”$/g,'')}”`:'');
  return html`<li class="fleet-ho${r.href?html` tap`:''}${r.st[2]?html` quiet`:''}${more?html` fleet-ho-more`:''}"${more?html` hidden`:''}${r.href?html` tabindex="0" role="link" aria-label="${t('{}: open the to-do',r.who)}" data-ho-go="${r.href}"`:''}><div class="fleet-ho-top"><strong>${r.who}</strong>${chip(r.st[0],r.st[1])}</div><p class="fleet-ho-sum" title="${text}">${time(r.at,true)} · ${text}</p></li>`};
 return html`<div class="fleet-box fleet-handoffs"><h3>Handoffs</h3><ul class="fleet-ho-list">${open.map(row)}${quiet.map(row)}</ul>${quiet.length>shown?html`<button type="button" class="quiet fleet-brief-show" data-ho-more>Show ${quiet.length-shown} more</button>`:''}</div>`}
// Ask for an intro, folded under the answer that offers it
const fleetIntro=o=>html`<details class="fleet-intro"><summary>Ask for an intro</summary><form class="fleet-ask fleet-intro-form" data-fleet="${o.fleet}" data-member="${o.member_id}" data-about="${o.about}"><input name="note" maxlength="300" placeholder="Why, in a line (optional; they see it)" aria-label="Why"><button>Ask</button></form></details>`;
function fleetIntroOffers(f,work,inFleet,shown=new Set()){const offers=(f.intro_offers||[]).filter(o=>inFleet(o,work)&&!shown.has(o.ask_id));
 return offers.length?html`<div class="list">${offers.map(o=>html`<article><p>${htmlT('{} knows someone at {}.',html`<strong>${o.name}</strong>`,o.label||o.about)}</p>${fleetIntro(o)}</article>`)}</div>`:''}
// Fleet, Family and Friends members in the Graph, from what the Network directory already shows every member (graph.with_fleet).
const inGraph=p=>p?.graph_node?html` <a href="#people" class="fp-graph" data-graph-open="${p.graph_node}" title="Open ${p.label||p.name||'them'} in your Graph" aria-label="Open ${p.label||p.name||'them'} in your Graph">Profile</a>`:'';  // their page in the owner's own Graph; the Team Graph is the box below
// What a Fleet costs, leaving it and starting one stay on the account (quotes, confirmations, Stripe), each its own
// focused step there: hosted, a one-time hop (/_machine/account-hop) carrying which Fleet; paired, a link that opens the
// account in a new tab, signing in there (this Machine's token opens nothing). Hidden in the phone app ([data-buy]).
const FLEET_PARTS={fleet_costs:'costs',fleet_leave:'leave',fleet_start:'start',fleet_settings:'settings'};
function fleetAcctGo(to,label,fleet=''){
 if(state.manage_url)return html`<form method="post" action="/_machine/account-hop" class="inline"><input type="hidden" name="to" value="${to}">${fleet?html`<input type="hidden" name="fleet" value="${fleet}">`:''}<button class="fleet-acct-link">${label}</button></form>`;
 if(!/^https:\/\//.test(state.account_url||''))return'';
 return html`<a class="fleet-acct-link" href="${state.account_url}?tab=fleet&part=${FLEET_PARTS[to]}${fleet?'&fleet='+fleet:''}" target="_blank" rel="noopener">${label} ↗</a>`}
// Under each Fleet's name, in its pane and in Manage (or Friends, while there is no Fleet): its costs, its settings, starting another, leaving it
function fleetAcct(x,start){const go=fleetAcctGo('fleet_start',start);if(!go)return'';
 return html`<div class="fleet-acct" data-buy>${/^fl_[0-9a-f]{16}$/.test(x?.id||'')?html`${fleetAcctGo('fleet_costs','What it costs',x.id)}${fleetAcctGo('fleet_settings','Fleet settings',x.id)}${go}<span class="fleet-leave">${fleetAcctGo('fleet_leave','Leave this Fleet',x.id)}</span>`:go}</div>`}
const familyWhen=v=>{const d=new Date(String(v).length<=10?v+'T12:00':v);if(isNaN(d))return v;return (String(v).length<=10?localeDate(d,DL,{weekday:'short',day:'numeric',month:'short'}):fmtDHM(d,{weekday:'short',day:'numeric',month:'short'}))};
// A datetime-local value with this browser's offset, so every Machine reads the same moment.
const familyMoment=v=>{if(!v)return '';const off=-new Date(v).getTimezoneOffset(),a=Math.abs(off);return `${v.slice(0,16)}${off<0?'-':'+'}${String(Math.floor(a/60)).padStart(2,'0')}:${String(a%60).padStart(2,'0')}`};
function familySection(f,family){const fam=f.family||{free:[],todos:[],plans:[],mine:[]},people=(family.people||[]).filter(p=>!p.me),today=new Date().toISOString().slice(0,10);
 // The family in a People box, as a Work Fleet's
 const who=html`<div class="fleet-box"><h3>People</h3><ul class="fleet-people">${(family.people||[]).map(p=>html`<li id="fleet-m-${p.member_id||''}"><div class="fp-name"><strong>${p.label||p.name}</strong>${p.me?html`<span class="fp-tag">you</span>`:''}${inGraph(p)}</div>${p.answers_with?html`<small class="fp-meta">${p.answers_with}</small>`:''}</li>`)}</ul></div>`;
 if(!people.length)return html`<div id="fleet-family" class="family">${who}${manageInvite(family,'Nobody else yet. Invite your family from your account page.')}</div>`;
 const opts=html`${people.map(p=>html`<option value="${p.member_id}">${p.name}</option>`)}`,latest=fam.free[0];
 const stage={accepted:'accepted',declined:'declined',done:'done',asked:'asked','waiting for them':'waiting'};
 let h=html`<div id="fleet-family" class="family">${who}`;
 h=html`${h}${html`<div class="fleet-box family-free"><h3>When are we all free?</h3><form class="fleet-ask family-free-form"><input type="date" name="start" required value="${today}" aria-label="From"><select name="days" aria-label="For">${[1,2,3,7,14].map(d=>html`<option value="${d}"${d===7?html` selected`:''}>${t(['{} day','{} days'],d)}</option>`)}</select><button class="primary">Ask everyone</button></form>${latest?html`<p class="muted">${t('{} of {} calendars',latest.answered+1,latest.asked+1)}${latest.waiting.length?' · '+t('waiting for {}',latest.waiting.join(', ')):''}</p>${latest.slots.length?html`<div class="family-slots">${latest.slots.map(s=>html`<span class="chip">${s.text}</span>`)}</div>`:html`<p class="muted">No common free time, 8:00 to 21:00.</p>`}`:html`<p class="muted">Shares busy times only, never what. Finds free hours between 8:00 and 21:00.</p>`}</div>`}`;
 h=html`${h}${html`<div class="fleet-box family-todos"><h3>To-dos</h3><form class="fleet-ask family-todo-form"><select name="member" aria-label="For">${opts}</select><input name="title" maxlength="120" required placeholder="${t('Pick up the groceries')}" aria-label="What"><input type="date" name="due" aria-label="Due (optional)"><button>Ask</button></form>${(fam.mine||[]).length?html`<p class="family-sub">Yours</p><ul class="family-list">${fam.mine.map(x=>html`<li>${x.title} <small class="muted">· ${t('from {}',x.name)}${x.due?' · '+familyWhen(x.due):''}${x.stage==='waiting'?' · '+t('waits for you in To-dos'):''}</small></li>`)}</ul>`:''}${fam.todos.length?html`<p class="family-sub">Asked</p><ul class="family-list">${fam.todos.map(x=>html`<li>${x.title} <small class="muted">· ${x.name} · ${t(stage[x.stage]||x.stage)}${x.due?' · '+familyWhen(x.due):''}</small></li>`)}</ul>`:''}</div>`}`;
 h=html`${h}${html`<div class="fleet-box family-plans"><h3>Plans</h3><form class="fleet-ask family-event-form"><input name="title" maxlength="120" required placeholder="${t('Dinner at grandma’s')}" aria-label="What"><input type="datetime-local" name="start" required aria-label="When"><input name="place" maxlength="120" placeholder="Where (optional)" aria-label="Where"><button>Propose to everyone</button></form>${fam.plans.length?html`<ul class="family-list">${fam.plans.map(p=>html`<li><strong>${p.title}</strong> <small class="muted">· ${familyWhen(p.start)}${p.place?' · '+p.place:''}</small><br><small>${[p.yes.length?t('In: {}',p.yes.join(', ')):'',p.no.length?t('Can’t: {}',p.no.join(', ')):'',p.waiting.length?html`<span class="muted">${t('Waiting: {}',p.waiting.join(', '))}</span>`:''].filter(Boolean).join(' · ')}</small> <a class="family-cal" href="${safeHref(p.link)}" target="_blank" rel="noopener">Add to my calendar</a></li>`)}</ul>`:html`<p class="muted">Each says yes or no on their Machine. Nothing is added to a calendar by itself.</p>`}</div>`}`;
 return html`${h}</div>`}
fleetOn('submit',async e=>{const t=e.target,act=t.classList.contains('family-free-form')?'family_free':t.classList.contains('family-todo-form')?'family_todo':t.classList.contains('family-event-form')?'family_event':'';if(!act)return;e.preventDefault();
 const v=n=>t.elements[n]?.value.trim()||'',args=act==='family_free'?{start:v('start'),days:Number(v('days'))}:act==='family_todo'?{member_id:v('member'),title:v('title'),due:v('due')}:{title:v('title'),start:familyMoment(v('start')),place:v('place')};
 try{await fleetPost(act,args);if(act!=='family_free')t.reset();toast({family_free:'Asked everyone. Free times show here as they answer.',family_todo:'Asked. It shows as accepted once they take it.',family_event:'Proposed. Yes and no show here.'}[act]);await fleetView()}catch(err){errCaught(err);toast(err.message,true)}});
// Friends (friends.py): add by username, requests both ways, your friends with the Machine they answer with, asking them,
// and your rules per friend (the same rule component as teammates). Friends see nothing of your Fleets.
const friendBtn=(label,attrs,cls='ghost',confirmText='')=>html`<button type="button" class="${cls}" ${attrs}${confirmText?html` data-confirm-text="${confirmText}"`:''}>${label}</button>`;
const friendBusy=a=>(a.busy||[]).length?a.busy.slice(0,12).map(([s,e])=>{return `${fmtDHM(s.replace('Z',':00Z'),{weekday:'short',day:'numeric',month:'short'})}–${fmtHM(e.replace('Z',':00Z'))}`}).join(' · ')+(a.busy.length>12?' · …':''):t('free the whole time');
// Your rules for friends: under Sharing with the Fleets' rules, the same component: one rule for all, exceptions per friend.
function friendRules(f){const fr=f.friends,group=fr&&f.fleets.find(x=>x.id===fr.id);if(!group||!(group.members||[]).length)return'';
 return fleetRules(group,f,true,t('your friends'))}
function friendsSection(f,notices){const fr=f.friends,group=fr&&f.fleets.find(x=>x.id===fr.id);if(!fr||!group)return'';
 const id=x=>x,people=(group.people||[]).filter(p=>!p.me),asked=f.asked.filter(a=>a.fleet===fr.id);
 let h=html`<div id="fleet-friends"><div class="fleet-pane-head"><h2>Friends</h2></div><p class="muted fleet-pane-sub">${fr.username?htmlT('Your username: {}. Friends add you by it.',html`<strong>${fr.username}</strong>`):t('Choose your username on your account page first.')} ${t('They ask your Machine under your rules (Sharing) and see nothing of your Fleets.')}</p>`;
 h=html`${h}${html`<div class="fleet-box"><h3>Add a friend</h3><form class="fleet-ask friend-add-form"><input name="username" maxlength="30" autocapitalize="none" autocomplete="off" spellcheck="false" placeholder="${t('Their exact username')}" aria-label="Their username"><button class="primary">Send friend request</button></form><p class="muted">Nothing connects until they accept.</p></div>`}`;
 if(fr.in.length)h=html`${h}${html`<div class="fleet-box"><h3>Waiting for you</h3><ul class="fleet-people">${fr.in.map((r,n)=>html`<li class="fp-row fp-wrap"><span class="fp-who">${htmlT('{} wants to be friends.',html`<strong>${r.name}</strong>`)}</span><span class="actions fleet-yn">${friendBtn('Accept',html`data-friend-do="accept" data-friend-id="${id(r.id)}"`,n?'':'primary')}${friendBtn('Decline',html`data-friend-do="decline" data-friend-id="${id(r.id)}"`)}${friendBtn('Block',html`data-friend-do="block" data-friend-id="${id(r.id)}"`,'ghost','Block them? They are not told; their requests are dropped from now on.')}</span></li>`)}</ul></div>`}`;
 if(fr.out.length)h=html`${h}${html`<div class="fleet-box"><h3>Your requests</h3><ul class="fleet-people">${fr.out.map(r=>html`<li class="fp-row"><span class="fp-who"><strong>${r.username}</strong> <small class="muted">· ${t('waiting')}</small></span><span class="actions">${friendBtn('Withdraw',html`data-friend-do="withdraw" data-friend-id="${id(r.id)}"`)}</span></li>`)}</ul></div>`}`;
 if(people.length){h=html`${h}${html`<div class="fleet-box"><h3>Your friends</h3><ul class="fleet-people">${people.map(p=>html`<li class="fp-row" id="fleet-m-${p.member_id||''}"><span class="fp-who"><strong>${p.label||p.name}</strong>${inGraph(p)}${p.answers_with?html`<br><small class="muted">${p.answers_with}</small>`:''}</span><span class="actions">${friendBtn('Remove',html`data-friend-do="remove" data-friend-member="${id(p.member_id)}"`,'ghost',t('Remove {}? Your Machines stop asking each other.',p.name))}${friendBtn('Block',html`data-friend-do="block" data-friend-member="${id(p.member_id)}"`,'ghost',t('Block {}? They are not told; their requests are dropped from now on.',p.name))}</span></li>`)}</ul></div>`}`;
  h=html`${h}${html`<div class="fleet-box friend-asks"><h3>Ask your friends</h3><h4 class="fleet-sub">Who knows someone there</h4><form class="fleet-ask fleet-ask-form" data-fleet="${fr.id}"><input name="about" maxlength="120" placeholder="Company, domain, email or name" aria-label="Ask your friends who knows someone at"><button class="primary">Ask your friends</button></form>`}`;
  h=html`${h}${html`<h4 class="fleet-sub">When they are busy</h4><form class="fleet-ask friend-avail-form"><label>Friend<select name="member">${people.map(p=>html`<option value="${id(p.member_id)}">${p.name}</option>`)}</select></label><label>From<input type="date" name="start" required value="${new Date().toISOString().slice(0,10)}"></label><label>For<select name="days">${[1,2,3,5,7,14].map(d=>html`<option value="${d}"${d===3?html` selected`:''}>${t(['{} day','{} days'],d)}</option>`)}</select></label><button>Ask</button></form><p class="muted fleet-fine">They share busy times only, never what, under their rules for you.</p>`}`;
  h=html`${h}${fleetIntroOffers(f,group,(row,x)=>row.fleet===x.id)}`;
  if(asked.length)h=html`${h}${html`<div class="list">${asked.map(a=>html`<article><p><strong>${a.name}</strong> · ${a.question}</p><p class="muted">${a.status==='answered'?(a.kind==='availability'?t('Busy: {}',friendBusy(a)):a.answer):a.status==='waiting'?t('Waiting for them to allow it'):a.status==='asked'?t(a.delivered===false?'Not delivered yet':'Asked'):t(a.status)}</p></article>`)}</div>`}`;
  h=html`${h}${html`</div>`}`}
 else h=html`${h}${html`<p class="muted">No friends yet.</p>`}`;
 if(fr.blocked.length)h=html`${h}${html`<div class="fleet-box"><h3>Blocked</h3><div class="list">${fr.blocked.map(b=>html`<article><p>${b.name}</p><div class="actions">${friendBtn('Unblock',html`data-friend-do="unblock" data-friend-member="${id(b.member_id)}"`)}</div></article>`)}</div></div>`}`;
 const lately=notices.filter(n=>/^friend_/.test(n.kind)&&!n.buttons.length).slice(0,5);
 if(lately.length)h=html`${h}${html`<div class="fleet-box"><h3>Lately</h3><ul class="list">${lately.map(n=>html`<li>${n.text}${n.outcome?html` <span class="muted">→ ${n.outcome}</span>`:''}</li>`)}</ul></div>`}`;
 return html`${h}</div>`}
fleetOn('click',async e=>{const b=e.target.closest('[data-friend-do]');if(!b)return;if(b.dataset.confirmText&&!confirm(b.dataset.confirmText))return;b.disabled=true;
 try{await fleetPost('fleet_friend',{do:b.dataset.friendDo,id:b.dataset.friendId||'',member_id:b.dataset.friendMember||''});
  toast({accept:'You are friends now.',decline:'Declined. They are not told.',block:'Blocked.',withdraw:'Withdrawn.',remove:'Removed.',unblock:'Unblocked.'}[b.dataset.friendDo]||'Done.');await fleetView();await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
fleetOn('submit',async e=>{const t=e.target;if(t.classList.contains('friend-add-form')){e.preventDefault();const username=t.elements.username.value.trim();if(!username)return;
  try{await fleetPost('fleet_friend',{do:'add',username});t.reset();toast('Request sent. It waits until they accept.');await fleetView()}catch(err){errCaught(err);toast(err.message,true)}}
 else if(t.classList.contains('friend-avail-form')){e.preventDefault();
  try{await fleetPost('fleet_availability',{member_id:t.elements.member.value,start:t.elements.start.value,days:Number(t.elements.days.value)});toast('Asked. Their busy times show here.');await fleetView()}catch(err){errCaught(err);toast(err.message,true)}}});
fleetOn('submit',async e=>{if(!e.target.classList.contains('fleet-free-form'))return;e.preventDefault();const text=e.target.elements.text.value.trim();if(!text)return;
 try{await fleetPost('fleet_free',{text,fleet:e.target.dataset.fleet});e.target.reset();toast('Asked your Fleet. Answers show here as they come.');await fleetView()}catch(err){errCaught(err);toast(err.message,true)}});
fleetOn('submit',async e=>{if(!e.target.classList.contains('fleet-ask-form'))return;e.preventDefault();const about=e.target.elements.about.value.trim();if(!about)return;
 try{await fleetPost('fleet_ask',{kind:'relationships',question:{about},fleet:e.target.dataset.fleet});e.target.reset();toast(/^fr_/.test(e.target.dataset.fleet||'')?'Asked your friends.':'Asked your Fleet.');await fleetView()}catch(err){errCaught(err);toast(err.message,true)}});
$('#fleet-view').addEventListener('click',e=>{const pane=e.target.closest('[data-fleet-pane]');if(pane){showFleetPane(pane.dataset.fleetPane);if(/^#fleet(\/|$)/.test(location.hash))history.replaceState(null,'',location.pathname+location.search+'#fleet/'+fleetPane);return}if(e.target.closest('[data-tab-go]'))document.querySelector('nav [data-tab="inbox"]').click()});
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-ex-rule],[data-fleet-ex-clear]');if(!b)return;b.disabled=true;
 try{const member=b.dataset.fleetExClear||b.closest('.fleet-ex-pick').querySelector('[data-fleet-ex-member]').value;
  await fleetPost('fleet_rule',{fleet:b.dataset.fleet,member_id:member,kind:b.dataset.kind,...(b.dataset.fleetExClear?{clear:true}:{rule:b.dataset.fleetExRule})});toast(b.dataset.fleetExClear?'Back to the rule for everyone.':'Saved.');await fleetView()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
// Connect Stripe for the team (self-hosted): Connections, + Add, at its Sign in with Stripe. Shared from the Fleet tab after.
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-connect]');if(!b)return;connectRun=null;showTab('health','add');await connectAdd(true);
 const x=connectList?.sources.find(v=>v.service===b.dataset.fleetConnect);if(!x)return;
 if(x.signin){connectSignin={source:x.name,provider:x.signin===true?x.service:x.signin,label:SIGNIN_COPY.stripe.label,own:!x.broker,state:'intro',...(x.signin_off?{off:true}:{})};$('#connect-add').dataset.sig='';renderConnectSignin()}
 viewTop($('#connect-add'))});
fleetOn('click',async e=>{const o=e.target.closest('[data-graph-optout]');if(!o)return;const off=o.dataset.off==='1';o.disabled=true;  /* the Shared Graph: asking an admin to stop, or sharing again */
 try{const r=await fleetPost('graph_optout',{fleet:o.dataset.graphOptout,off});toast(off?(r.off==='off'?'Not shared now.':'Asked an admin.'):'Shared with the team again.');await fleetView()}catch(err){errCaught(err);o.disabled=false;toast(err.message,true)}});
fleetOn('click',e=>{const b=e.target.closest('[data-shared-read]');if(b)openEvent(b.dataset.sharedRead,b.textContent)});
fleetOn('change',async e=>{const t=e.target.closest('[data-net-addr],[data-net-toggle]');if(!t)return;t.disabled=true;
 try{await fleetPost('fleet_network',{do:t.dataset.netToggle||(t.checked?'address_on':'address_off'),...(t.dataset.netToggle?{}:{email:t.dataset.netAddr})});await fleetView()}catch(err){errCaught(err);t.checked=!t.checked;toast(err.message,true)}finally{t.disabled=false}});
fleetOn('submit',async e=>{const t=e.target;if(t.classList.contains('fleet-intro-form')){e.preventDefault();
  try{await fleetPost('fleet_intro',{fleet:t.dataset.fleet,member_id:t.dataset.member,about:t.dataset.about,note:t.elements.note.value.trim()});toast('Asked. This tab shows how it goes.');await fleetView()}catch(err){errCaught(err);toast(err.message,true)}}});
fleetOn('submit',async e=>{const t=e.target;if(!t.matches('.share-form,.share-replace'))return;e.preventDefault();const btn=t.querySelector('button:not([type=button])');btn.disabled=true;
 try{if(t.matches('.share-form')){const r=await fleetPost('fleet_share',{fleet:t.dataset.fleet,account:t.dataset.account,members:[...t.querySelectorAll('input[name=m]:checked:not(:disabled)')].map(i=>i.value)});toast(`Shared with ${r.shared_with} ${r.shared_with===1?'Machine':'Machines'}.`)}
  else{await fleetPost('fleet_share_replace',{fleet:t.dataset.fleet,service:t.dataset.service,token:t.elements.token.value.trim()});t.elements.token.value='';toast('Replaced. Teammates get the new one.')}
  await fleetView()}catch(err){errCaught(err);btn.disabled=false;toast(err.message,true)}});
fleetOn('change',async e=>{const t=e.target;try{
 const b=t.closest('.fleet-rule');let res;
 if(t.dataset.fleetRule)res=await fleetPost('fleet_rule',{fleet:t.dataset.fleet,member_id:t.dataset.fleetRule,kind:t.dataset.kind,rule:t.value});
 else if(t.dataset.fleetDetails)res=await fleetPost('fleet_rule',{fleet:t.dataset.fleet,member_id:t.dataset.fleetDetails,kind:t.dataset.kind,details:t.value==='1'});
 else if(t.dataset.scope&&b)res=await fleetPost('fleet_rule',{fleet:b.dataset.fleet,member_id:b.dataset.member,kind:b.dataset.kind,scope:fleetScopeOf(b)});
 else if(t.id==='fleet-meetings')await fleetPost('fleet_meetings',{on:t.checked});else if(t.id==='fleet-brief-every')await fleetPost('fleet_brief',{every:t.value});else if(t.id==='fleet-brief-tell')await fleetPost('fleet_brief',{tell:t.checked});else if(t.dataset?.fleetBriefShare){await fleetPost('fleet_rule',{fleet:t.dataset.fleetBriefShare,member_id:'*',kind:'brief',rule:t.checked?'always':'never'});toast(t.checked?'Brief facts on.':'Brief facts off. Nothing goes to their briefs.');await fleetView();return}else return;res=res?.result||res;if(b&&res?.rule){const sc=b.querySelector('.fleet-scope')?res.scope:null;b.querySelector('.fleet-preview').textContent=fleetPreview(b.dataset.name,b.dataset.kind,res,sc,!!b.dataset.wide);if(b.dataset.wide&&t.dataset.fleetRule){await fleetView();return toast('Saved.')}
  if(sc){b.querySelector('.fleet-scope-now').textContent=fleetScopeText(sc)?' ('+fleetScopeText(sc)+')':'';if(t.dataset.scope&&t.type!=='checkbox')t.value=sc[t.dataset.scope].join(', ')}}toast('Saved.')}catch(err){errCaught(err);toast(err.message,true);await fleetView()}});
// Answers to your free questions show as they arrive, while the Fleet tab is open and you aren't typing in it.
setInterval(()=>{if(!$('#fleet').hidden&&!$('#fleet-view').contains(document.activeElement)&&(fleetData?.free||[]).some(q=>q.answers.some(x=>x.state==='waiting')))fleetView()},30000);
// The Network pane (its cards under To-dos stay in fleet-requests.js): drawn only with the Fleet tab, so its styles load with it
function networkSection(f){const net=f.network;if(!net||!f.friends?.id)return'';
 // Laid out like a Settings tab: a row per switch (label, one short line, the switch), then Scheduling, then Leave apart at the bottom
 const sw=(on,label,doOn,doOff,note)=>html`<div class="net-row"><span class="grow"><strong>${label}</strong>${note?html`<small>${note}</small>`:''}</span><input type="checkbox" class="lookup-switch" role="switch" aria-label="${label}" data-net-toggle="${on?doOff:doOn}"${on?html` checked`:''}></div>`;
 const rest=(net.people||[]).filter(p=>p.status==='new'&&!p.reasons.length||p.status==='later'),waiting=(net.people||[]).filter(p=>p.status==='requested');
 const addrs=net.discoverable?(net.addresses||[]):[];
 const findNote=net.find&&net.last?t('Suggests people you know. Last checked {}.',netDay(net.last)):t('Suggests people you know.');
 const seenNote=!net.discoverable?t('Nobody can find you now.'):!addrs.length?'':t('Only the addresses below find you.');
 const addrTags=a=>[a.account?t('Sign-in email'):'',a.on&&!a.findable?t('(not yet)'):'',a.shared?t('Shared address'):'',a.phone&&a.source!=='config'?t(a.source==='whatsapp'?'WhatsApp':'About you'):''].filter(Boolean);
 // The sign-in email always finds them: it says so instead of a switch that can't move
 const addrRow=a=>{const shown=a.phone?phoneShown(a.email):a.email,tags=addrTags(a);
  return html`<li class="net-addr"><span class="grow"><span class="net-addr-at">${shown}</span>${tags.length?html`<small>${tags.map(x=>html`<span>${x}</span>`)}</small>`:''}</span>${a.account?html`<span class="net-fixed">${t('Always on')}</span>`:html`<input type="checkbox" class="lookup-switch" role="switch" aria-label="${shown}" data-net-addr="${a.email}"${a.on?html` checked`:''}>`}</li>`};
 let h=html`<div id="fleet-network"><div class="section-head"><h2>Network</h2><p>See which of your contacts have a Machine, and let people who know you find you. Your address book is never revealed. <a class="learn" href="${HELP}friends#find-people-you-know" target="_blank" rel="noopener">Learn more</a></p></div><div class="list settings-list net-list net-switches">${sw(!!net.find,'Check which of my contacts have a Machine','find_on','find_off',findNote)}${sw(!!net.discoverable,(net.addresses||[]).some(a=>a.phone)?'Let people who have my email or number find me':'Let people who have my email find me','discoverable_on','discoverable_off',seenNote)}${addrs.length?html`<div class="net-addrs"><span class="net-addrs-head">Findable by</span><ul>${addrs.map(addrRow)}</ul></div>`:''}</div>`;
 if(rest.length)h=html`${h}${html`<h3 class="net-sub">Your contacts with a Machine</h3><ul class="fleet-people list net-people">${rest.map(p=>html`<li class="fp-row"><span class="fp-who"><strong>${p.name}</strong> <small class="muted">@${p.username}</small></span><span class="actions">${p.hint==='colleague'?netBtn('Connect','connect',p.email,'colleague'):html`${netBtn('Friend','connect',p.email,'friend')}${netBtn('Family','connect',p.email,'family')}`}${netBtn('Never','never',p.email)}</span></li>`)}</ul>`}`;
 if(waiting.length)h=html`${h}${html`<p class="muted net-waiting">Waiting for ${waiting.map(p=>p.name).join(', ')} to accept.</p>`}`;
 h=html`${h}${meetSetting(f.meet)}`;
 h=html`${h}${html`<div class="acct-danger net-leave">${netBtn('Leave the Network','leave','','','acct-quiet','Leave the Network? Every friendship ends and nobody can find you. Your Fleets stay.')}</div></div>`}`;
 return h}
// The Fleet tab drawn from fleetData (fleetView in fleet-shared.js fetches it first, and loads this part).
function fleetDraw(view){const f=fleetData;if(!f.on){view._fleetHTML=null;setHTML(view,html`<p class="muted">This Machine is not in a Fleet. Pair it with your account to join your team's. <a href="${HELP}fleet" target="_blank" rel="noopener">Learn more</a></p>`);return}
 // Several Work Fleets: each its own section, with its own people, rules and Ask; questions go to one Fleet at a time.
 const works=f.fleets.filter(x=>x.kind==='work'),family=f.fleets.find(x=>x.kind==='family'),several=works.length>1;
 const inFleet=(row,x)=>row.fleet===x.id||(!several&&row.fleet===x.kind),fleetName=row=>several?(works.find(x=>inFleet(row,x))?.name||''):'';
 // Who is who: each member with the Machine they answer with and their account email, so two people with one name stay apart.
 const who=x=>{const groups=[];for(const p of x.people||[]){const k=p.name+'|'+(p.email||''),g=groups.find(g=>g.k===k);g?g.list.push(p):groups.push({k,list:[p]})}  // one person with several Machines: the name once
  return groups.length?html`<ul class="fleet-people">${groups.map(({list})=>{const p=list[0],tag=t=>html`<span class="fp-tag">${t}</span>`,many=list.length>1;
   return html`<li id="fleet-m-${p.member_id||''}"><div class="fp-name"><strong>${p.name}</strong>${list.some(m=>m.me)?tag('you'):''}${list.some(m=>m.role==='owner')?tag('Owner'):''}${list.some(m=>m.role==='admin')?tag('Admin'):''}${inGraph(list.find(m=>m.graph_node))}</div>${many?html`<small class="fp-meta">${p.email||''}</small>${list.map(m=>html`<small class="fp-meta fp-machine">${m.answers_with||''}${m.me?tag('this Machine'):''}</small>`)}`
     :html`<small class="fp-meta">${[p.email,p.answers_with].filter(Boolean).join(' · ')}</small>`}</li>`})}</ul>`:''};
 const box=(title,sub,body,cls='')=>html`<div class="fleet-box${cls?' '+cls:''}"><h3>${title}</h3>${sub?html`<p class="sub">${sub}</p>`:''}${body}</div>`;
 const head=(x,count)=>html`<div class="fleet-pane-head"><h2 class="ell">${x.name}</h2><span class="chip"><span class="ct">${x.label}</span></span>${count?html`<span class="muted">${count} ${count===1?'person':'people'}</span>`:''}</div>`;
 const people=x=>box('People','',html`${who(x)}${x.members.length||(x.people||[]).some(p=>!p.me)?'':manageInvite(x,'Nobody else yet. Invite teammates from your account page.')}`);
 // One view at a time: each Work Fleet, Friends, Family, Sharing (every rule in one place) and Activity, as pills.
 const panes=[];
 const notices=f.notices||[],asking=notices.filter(n=>n.buttons.length),told=notices.filter(n=>!n.buttons.length&&!/^friend_/.test(n.kind));
 const noticeCard=n=>html`<article id="fleet-${n.id}"><p>${n.text}</p>${n.detail?html`<p class="muted">${n.detail}</p>`:''}${n.outcome?html`<p class="muted">→ ${n.outcome}</p>`:''}${n.reason?html`<p class="note">${n.reason}</p>`:''}${n.buttons.length?html`<div class="actions">${n.buttons.map(b=>html`<button${b.choice==='confirm'?html` class="primary"`:''} data-fleet-notice="${n.id}" data-choice-n="${b.choice}" data-key="${n.key}">${b.label}</button>`)}</div>`:''}<p><small class="mono">${fmtDHM(n.at,{day:'numeric',month:'short'})}</small></p></article>`;
 const offerOf=new Map((f.intro_offers||[]).map(o=>[o.ask_id,o]));
 for(const work of works){const asked=f.asked.filter(a=>inFleet(a,work)&&a.kind!=='handoff');  // handoffs have their own box
  let h=html`<div id="fleet-${work.id}">${head(work,(work.people||[]).length)}${fleetAcct(work,'Start another Fleet')}${people(work)}${fleetShared(f,work)}`;
  if(work.members.length){
   h=html`${h}${box('Who knows someone?','Their Machines say how well they know someone there and when they last talked. Names only if they allow it.',
    html`${html`<form class="fleet-ask fleet-ask-form" data-fleet="${work.id}"><input name="about" maxlength="120" placeholder="Company, domain, email or name" aria-label="Who knows someone at"><button class="primary">Ask ${several?work.name:'the Fleet'}</button></form>`}${asked.length?html`<div class="list">${[...new Set(asked.map(a=>a.question))].map(q=>html`<article><p class="muted">${q}</p>${asked.filter(a=>a.question===q).map(a=>html`<p><strong>${a.name}</strong> · ${a.status==='answered'?a.answer:a.status==='waiting'?'Waiting for them to allow it':a.status==='asked'?(a.delivered===false?'Not delivered yet':'Asked'):a.status}</p>${offerOf.has(a.id)?fleetIntro(offerOf.get(a.id)):''}`)}</article>`)}</div>`:''}${fleetIntroOffers(f,work,inFleet,new Set(asked.map(a=>a.id)))}`)}`;
   h=html`${h}${html`${fleetHandoffs(f,work,inFleet)}${box('Ask anything','',fleetFree(f,work,several))}${fleetLearnings(work)}`}`}
  else h=html`${h}${fleetIntroOffers(f,work,inFleet)}`;
  h=html`${h}${fleetBriefAsks(f,work,inFleet)}`;
  panes.push({id:'fleet-'+work.id,label:work.name,html:html`${h}${html`</div>`}`,at:work.joined_at});
  if((f.shared?.graph||[]).some(s=>s.fleet===work.id))panes.push({id:'shared-'+work.id,label:several?`What's shared · ${work.name}`:'What\'s shared',html:html`<div class="shared-view" data-shared-fleet="${work.id}"><p class="muted">Loading…</p></div>`,at:work.joined_at})}
 if(family)panes.push({id:'family',label:family.name||'Family',html:html`${head(family,(family.people||[]).length)}${fleetAcct(family,'Start another Fleet')}${familySection(f,family)}`,at:family.joined_at});
 // Every Fleet together, Work and Family, by when you joined or made it (the directory's order when it doesn't say); then Friends, Network, Sharing.
 const listed=p=>f.fleets.findIndex(x=>p.id.replace(/^shared-/,'fleet-')===(x.kind==='family'?'family':'fleet-'+x.id))+(/^shared-/.test(p.id)?.5:0);
 panes.sort((a,b)=>a.at&&b.at&&a.at!==b.at?(a.at<b.at?-1:1):listed(a)-listed(b));
 {const manage=managePane(f);if(manage)panes.push({id:'manage',label:'Manage',badge:manageWaiting(f),html:manage})}  // fleet-manage.js
 const fr=f.friends,friendsHtml=friendsSection(f,notices);
 if(friendsHtml)panes.push({id:'friends',label:'Friends',badge:(fr?.in||[]).length,html:works.length||family?friendsHtml:html`${friendsHtml}${fleetAcct(null,'Start a Fleet')}`});
 {const net=networkSection(f);if(net)panes.push({id:'network',label:'Network',html:net})}
 // Sharing: every rule in one place. What the three choices mean, once, at the top; per kind a plain question and an example.
 const friendsToo=!!fr&&(f.fleets.find(x=>x.id===fr.id)?.members||[]).length,rulesOf=works.filter(x=>x.members.length),familyToo=!!family&&family.members.length;
 if(rulesOf.length||friendsToo||familyToo){
  let h=html`<dl class="fleet-legend" role="note">${[['Ask me first','You choose each time'],['Always','Answered by itself'],['Never','They get “no”'],['Names','Whether they hear who']].map(([t,d])=>html`<div><dt>${t}</dt><dd>${d}</dd></div>`)}</dl><p class="muted fleet-never">Never email content, never what your meetings are about. <a class="learn" href="${HELP}sharing-rules" target="_blank" rel="noopener">Learn more</a></p>`;
  for(const work of rulesOf)h=html`${h}${fleetRules(work,f,several)}`;
  h=html`${h}${friendRules(f)}`;
  if(familyToo)h=html`${h}${fleetRules(family,f,true,'your family')}`;
  h=html`${h}${box('Meetings and brief','',html`<label class="fleet-option"><input type="checkbox" id="fleet-meetings"${f.ask_meetings?html` checked`:''}><span>${rulesOf.length?t(several?(friendsToo?'Ask my Work Fleets, and a friend who is in the meeting, about the outside people in my meetings this week':'Ask my Work Fleets about the outside people in my meetings this week'):(friendsToo?'Ask my Work Fleet, and a friend who is in the meeting, about the outside people in my meetings this week':'Ask my Work Fleet about the outside people in my meetings this week')):t('Ask a friend who is in one of my meetings this week about the other people in it')}<small class="muted">They see those email addresses.</small></span></label>${rulesOf.length?fleetBriefSettings(f):''}`,'fleet-settings')}`;
  panes.push({id:'sharing',label:'Sharing',html:h})}
 panes.push({id:'activity',label:'Activity',html:html`${told.length?box('Lately','Who joined, asked for a hosted Machine, had one started, or left.',html`<div class="list">${told.map(noticeCard)}</div>`):''}${actEmbed()}`});
 const current=panes.some(p=>p.id===fleetPane)?fleetPane:panes[0].id;
 let body=f.off?pageNotice('The Network is off for now. Nothing is asked or answered.'):'';
 {const todo=fleetCardsOf(f).length;if(todo)body=html`${body}${pageNotice(t(['One Fleet item waits for you under To-dos.','{} Fleet items wait for you under To-dos.'],todo),'Show',{'tab-go':'inbox'},'fleet-todo')}`}
 body=html`${body}${html`<div class="fleet-tabs" role="tablist" aria-label="Fleet">${panes.map(p=>html`<button type="button" role="tab" data-fleet-pane="${p.id}" aria-selected="${p.id===current}"><span class="ell">${p.label}</span>${p.badge?html` <span class="badge">${p.badge}</span>`:''}</button>`)}</div>`}`;
 // A slot for suggested connections (people already on the Network you may know), filled by its own feature.
 body=html`${body}${html`<div id="fleet-discover" class="fleet-discover"></div>`}`;
 body=html`${body}${html`${panes.map(p=>html`<div class="fleet-pane" role="tabpanel" data-pane="${p.id}"${p.id===current?'':html` hidden`}>${p.html}</div>`)}`}`;
 // Leave unchanged forms in place: a completed background request must not swallow a click.
 if(view._fleetHTML===String(body)){actEmbedFill();return}
 const drafts=[...view.querySelectorAll('form')].map(form=>({key:form.className+'|'+(form.dataset.fleet||''),values:[...form.elements].filter(e=>e.name&&['INPUT','TEXTAREA'].includes(e.tagName)).map(e=>[e.name,e.value])}));
 setHTML(view,body);view._fleetHTML=String(body);actEmbedFill();
 if(/^shared-/.test(current))sharedLoad(current.slice(7),true);
 for(const draft of drafts){const form=[...view.querySelectorAll('form')].find(f=>f.className+'|'+(f.dataset.fleet||'')===draft.key);if(form)for(const [name,value]of draft.values){const input=form.elements.namedItem(name);if(input&&'value'in input)input.value=value}}
}
function meetSetting(m){if(!m)return'';
 const opt=(key,value,label)=>html`<option value="${value}"${String(m[key])===String(value)?html` selected`:''}>${label}</option>`;
 // A Settings-style row per choice: the label on the left, its select on the right, all selects one width
 const sel=(key,label,options)=>html`<label class="meet-pref"><span class="grow"><strong>${label}</strong></span><select data-meet-pref="${key}"${key!=='allow'&&key!=='brand'&&m.allow==='off'?html` disabled`:''}>${options}</select></label>`;
 return html`<div class="meet-setting"><div class="section-head"><h2>Scheduling with other Machines</h2><p>When someone with a Machine asks to meet, your Machines find a time. Only free or busy is shared, and nothing is booked until you both tap Book it. <a class="learn" href="${HELP}friends#scheduling-with-other-machines" target="_blank" rel="noopener">Learn more</a></p></div><div class="list settings-list net-list meet-prefs">${
  sel('allow','What other Machines may ask mine',[opt('allow','freebusy','Free/busy for scheduling'),opt('allow','off','Off')])}${
  sel('minutes','Meeting length',[15,30,45,60,90].map(n=>opt('minutes',n,t('{} min',n))))}${
  sel('buffer','Buffer',[0,5,10,15,30].map(n=>opt('buffer',n,n?t('{} min',n):'None')))}${
  sel('prefer','Preferred times',[opt('prefer','any','Any time'),opt('prefer','morning','Mornings'),opt('prefer','afternoon','Afternoons')])}${
  sel('brand','Footer on booking links',[opt('brand',true,'On'),opt('brand',false,'Off')])}</div></div>`}
