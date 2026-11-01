// The Fleet: what teammates' Machines said, the questions waiting for you, your rules per teammate, and the log of both directions.
const fleetPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
const FLEET_RULE={ask:'Ask me first',always:'Always answer',never:'Never'};
// One Fleet rule, the same for every kind: Ask me first | Always | Never, how much they hear, Only about… and an example of
// what that teammate would get, from made-up sample data. A new kind gets all of it; FLEET_KIND_UI gives it its own words
// (how: the two "how much" choices; sees(company, withNames): what an answer says; ask(name): what Ask me first does).
const FLEET_SEG={ask:'Ask me first',always:'Always',never:'Never'};
const FLEET_SEG_HINT={ask:'You see each question and choose',always:'Answered by itself, without asking you',never:'They get “no”'};
const FLEET_KIND_Q={todo:'“Can you pick up the kids Friday?”',event:'“Dinner at grandma’s Sunday?”',relationships:'“Who knows someone at Acme?”',meeting:'“Who’s this guest in our meeting?”',handling:'“Who’s on this email we both got?”',
 intro:'“Can you introduce me?”',handoff:'“Can you take this over?”',availability:'“When are you busy?”',followup:'“Will you take your part of the follow-ups?”',brief:'“What did you see this week?”'};
const FLEET_KIND_UI={
 relationships:{how:['Without names','With names'],sees:(c,d)=>d?t('3 people at {} know them, one well: Ann Lee (well), Bob Ray',c):t('3 people at {} know them, one well',c)},
 meeting:{how:['Without names','Names and promises'],sees:(c,d)=>d?t('their guest from {}: a close contact, 1 open promise each way, with name and promises',c):t('their guest from {}: a close contact, 1 open promise each way',c)},
 handling:{sees:()=>'that you’re on an email you both got (a code, never the email)',ask:()=>'Nothing goes out; the to-do offers “Tell them you’re on it”.'},
 intro:{sees:()=>'“accepted”, then “sent” once you send the intro your Machine drafts',ask:()=>'You see each intro asked of you; nothing is drafted or sent without you.'},
 handoff:{sees:()=>'“accepted”, then “done” when you finish the to-do',ask:()=>'You see each handoff with its summary, to accept or decline.'},
 availability:{sees:()=>'your busy times on those days, never what or with whom'},
 followup:{sees:()=>'that you took your part of a meeting’s follow-ups',ask:()=>'You see your part of a meeting’s follow-ups to accept, change or decline.'},
 todo:{sees:()=>'“accepted”, then “done” when you finish it',ask:()=>'You see each to-do to accept or decline.'},
 event:{sees:()=>'“is in” or “can’t make it”; never your calendar',ask:()=>'You see each plan to say yes or no. Nothing is added to your calendar by itself.'}};
const fleetFirst=n=>String(n||'').trim().split(/[\s(]/)[0]||'They';
const fleetScopeText=sc=>sc?[sc.only.length?t('only {}',sc.only.join(', ')):'',sc.never.length?t('not {}',sc.never.join(', ')):'',sc.work_only?'':t('personal accounts too')].filter(Boolean).join('; '):'';
// The example under a rule, from made-up data. wide: the rule of a whole Fleet ("they"), else one person's.
function fleetPreview(name,k,r,sc,wide){const ui=FLEET_KIND_UI[k]||{},c=sc?.only?.[0]||((sc?.never||[]).some(t=>/acme/i.test(t))?'Globex':'Acme'),sees=ui.sees?t(ui.sees(c,r.details)):'';
 const who=fleetFirst(name);
 let out=r.rule==='never'?(wide?t('They get “no”.'):t('{} gets “no”.',who)):r.rule==='always'?(sees?(wide?t('They get, without asking you: {}.',sees):t('{} gets, without asking you: {}.',who,sees)):t('Answered without asking you.'))
  :ui.ask?t(ui.ask()):sees?(wide?t('Asked first; if you answer, they get: {}.',sees):t('Asked first; if you answer, {} gets: {}.',who,sees)):t('Asked first, every time.');
 const scope=fleetScopeText(sc);return t('Example: {}',out)+(scope?` (${cap(scope)}.)`:'')}
// A Careful Work Fleet (security_levels.py): no Always, no names, work accounts only. A looser own choice is kept, shown as it applies.
function fleetRule(work,f,m,k,r,wide){const id=`${work.id}-${m.member_id}-${k}`.replace(/[^\w-]/g,''),ui=FLEET_KIND_UI[k]||{},rules=work.kind_rules?.[k]||f.kind_rules?.[k]||['ask','always','never'];
 const lock=work.security==='careful';if(lock)r={...r,rule:r.rule==='always'?'ask':r.rule,details:false};
 const sc=(f.scoped||[]).includes(k)?{only:[],never:[],work_only:true,...(f.scopes?.[work.id]?.[m.member_id]?.[k]||{}),...(lock?{work_only:true}:{})}:null,whom=wide?'everyone':m.name;
 const off=(attr,v)=>lock&&((attr==='fleet-rule'&&v==='always')||(attr==='fleet-details'&&v==='1'));
 const seg=(attr,opts,cur,label)=>`<div class="seg" role="radiogroup" aria-label="${esc(label)}">${opts.map(([v,l])=>`<label${off(attr,v)?' title="Off in a Careful Fleet"':attr==='fleet-rule'&&FLEET_SEG_HINT[v]?` title="${esc(FLEET_SEG_HINT[v])}"`:''}><input type="radio" name="${attr}-${id}" value="${v}" data-fleet="${esc(work.id)}" data-${attr}="${esc(m.member_id)}" data-kind="${k}"${cur===v?' checked':''}${off(attr,v)?' disabled':''}><span>${esc(l)}</span></label>`).join('')}</div>`;
 const noHow=[...(f.no_details||['handling']),...FLEET_REQ].includes(k);
 const how=noHow?'':seg('fleet-details',[['0',ui.how?.[0]||'Without names'],['1',ui.how?.[1]||'With names']],r.details?'1':'0',`How much ${whom} hears: ${f.kinds[k]}`);
 const scope=sc?`<details class="fleet-scope"><summary>Only about…<span class="muted fleet-scope-now">${fleetScopeText(sc)?' ('+esc(fleetScopeText(sc))+')':''}</span></summary><label>Only about<input data-scope="only" value="${esc(sc.only.join(', '))}" placeholder="acme.com, Globex" aria-label="Only about, for ${esc(whom)}: ${esc(f.kinds[k])}"></label><small class="muted">Companies, domains or names, with commas. Empty: anything. Anything else asks you first.</small><label>Never about<input data-scope="never" value="${esc(sc.never.join(', '))}" placeholder="Initech, rival.example" aria-label="Never about, for ${esc(whom)}: ${esc(f.kinds[k])}"></label><label class="fleet-scope-work"><input type="checkbox" data-scope="work_only"${sc.work_only?' checked':''}${lock?' disabled':''}> Only people from your work accounts</label></details>`:'';
 let ex='';
 if(wide){const own=(work.exceptions||{})[k]||[],free=work.members.filter(x=>!own.some(e=>e.member_id===x.member_id));
  const pills=own.map(e=>`<span class="fleet-ex">${esc(e.name)}: ${esc([t(FLEET_SEG[e.rule]||e.rule),!noHow&&e.details!==r.details?t(e.details?'with names':'without names'):'',e.own_scope?t('own Only about'):''].filter(Boolean).join(', '))}<button type="button" data-fleet-ex-clear="${esc(e.member_id)}" data-fleet="${esc(work.id)}" data-kind="${k}" aria-label="${esc(t('Remove the exception for {}',e.name))}" title="Back to the rule for everyone">×</button></span>`).join('');
  const add=free.length?`<details class="fleet-ex-add"><summary>Different for someone? Add an exception</summary><span class="fleet-ex-pick"><select data-fleet-ex-member aria-label="Who">${free.map(x=>`<option value="${esc(x.member_id)}">${esc(x.name)}</option>`).join('')}</select>${rules.filter(v=>v!==r.rule&&!off('fleet-rule',v)).map(v=>`<button type="button" class="ghost" data-fleet-ex-rule="${v}" data-fleet="${esc(work.id)}" data-kind="${k}">${esc(FLEET_SEG[v])}</button>`).join('')}</span></details>`:'';
  ex=pills||add?`<div class="fleet-ex-row">${pills}${add}</div>`:''}
 return `<div class="fleet-rule" data-fleet="${esc(work.id)}" data-member="${esc(m.member_id)}" data-kind="${k}" data-name="${esc(m.name)}"${wide?' data-wide="1"':''}><div class="fleet-rule-kind">${esc(cap(f.kinds[k]))}${FLEET_KIND_Q[k]?`<small>${esc(FLEET_KIND_Q[k])}</small>`:''}</div><div class="fleet-rule-set">${seg('fleet-rule',rules.map(v=>[v,FLEET_SEG[v]]),r.rule,t('{}, for {}',t(cap(f.kinds[k])),whom==='everyone'?t('everyone'):whom))}${how}${scope}<p class="fleet-preview muted">${esc(fleetPreview(m.name,k,r,sc,wide))}</p>${ex}</div></div>`}
// A Fleet's rules: one per kind of question for everyone in it, with exceptions for someone in particular.
// whom: who the rules are for in the heading ("your friends"); else the Fleet's name when there are several.
const fleetRules=(work,f,several,whom)=>`<div class="fleet-rules-head"><h3>${esc(whom?t('What your Machine answers {}',t(whom)):several?t('What your Machine answers in {}',work.name):t('What your Machine answers'))}</h3><p class="muted">${esc(whom?t('One rule per kind of question, for all {}.',t(whom)):t('One rule per kind of question, for everyone in {}.',several?work.name:t('your Fleet')))}</p>${work.security==='careful'?`<p class="fleet-careful">${esc(work.name||'This Fleet')} is Careful: answers wait for you and leave out names. <a class="learn" href="https://themachine.computer/help/security-levels" target="_blank" rel="noopener">Learn more</a></p>`:work.kind==='work'&&work.kind_rules?.relationships?.length===2?`<p class="muted fleet-graph-note">Answers use only what the Team Graph shares with the team. Never private or personal. <a class="learn" href="${HELP}team-graph" target="_blank" rel="noopener">Learn more</a></p>`:''}</div><div class="fleet-rules fleet-mate">${Object.entries(work.rules||{}).filter(([k])=>k!=='brief').map(([k,r])=>fleetRule(work,f,{member_id:'*',name:'everyone'},k,r,true)).join('')}</div>`;  // brief facts: their own switch (fleetBriefShare)
const fleetScopeOf=b=>({only:b.querySelector('[data-scope="only"]').value,never:b.querySelector('[data-scope="never"]').value,work_only:b.querySelector('[data-scope="work_only"]').checked});
// The team brief (what the Fleet saw) and free questions, per Work Fleet. A teammate's free question and answers are their own words: shown as text, never acted on.
const fleetDay=at=>esc(fmtDHM(at,{day:'numeric',month:'short'}));
// Shared connectors (shared_connectors.py): what this Fleet shares, OKs this Machine's owner gives, and sharing one.
function fleetShared(f,work){const v=f.shared||{},mine=(v.prompts||[]).filter(p=>p.fleet===work.id),shares=(v.shares||[]).filter(s=>s.fleet===work.id);
 const can=(v.can_share||[]).find(c=>c.fleet===work.id),own=(v.accounts||[]).filter(a=>!shares.some(s=>s.service===a.service&&s.label));
 const ask={recipient:p=>`Share ${esc(svcName(p.service))} with ${esc(p.name)}'s Machine?`,rekey:p=>`${esc(p.name)}'s Machine has new keys. Share ${esc(svcName(p.service))} again?`,
  admin:p=>`Confirm ${esc(p.name)} as an admin of ${esc(p.fleet_name)}?`,member:p=>`${esc(p.name)} joined ${esc(p.fleet_name||work.name)}. Share the team's Graph with them?`,optout:p=>`${esc(p.name)} asks to stop sharing their Work with the team.`,successor:p=>`If you delete your account, ${esc(p.name)} owns ${esc(p.fleet_name)}. Confirm them?`,
  replace:p=>`${esc(p.name)} left ${esc(p.fleet_name)}. Replace the ${esc(svcName(p.service))} access so it stops working on their Machine.`};
 const yes={recipient:'Share',rekey:'Share',admin:'Confirm',successor:'Confirm',member:'Share',optout:'Approve'};
 const card=p=>`<article id="share-${esc(p.id)}"><p>${(ask[p.kind]||(()=>''))(p)}</p>${p.email?`<p class="muted">${esc(p.email)}</p>`:''}${p.fp&&p.kind!=='replace'&&p.kind!=='optout'?`<p class="share-fp mono" title="Their Machine's safety number">${esc(p.fp)}</p>`:''}`+
  (p.kind==='replace'?`<form class="share-replace" data-fleet="${esc(p.fleet)}" data-service="${esc(p.service)}"><input name="token" type="password" autocomplete="off" placeholder="New access token" aria-label="New access token" required><div class="actions"><button class="primary">Replace</button><button type="button" class="ghost" data-share-ok="${esc(p.id)}" data-choice="no">Later</button></div></form>`
   :`<div class="actions"><button class="primary" data-share-ok="${esc(p.id)}" data-kind="${esc(p.kind)}" data-choice="yes">${yes[p.kind]}</button><button class="ghost" data-share-ok="${esc(p.id)}" data-choice="no">Not now</button></div>`)+'</article>';
 const row=s=>s.unconfirmed?`<p class="muted">Not confirmed yet: ${s.unconfirmed.map(esc).join(', ')}</p>`:`<article><p><strong>${esc(s.label)}</strong>${s.workspace?' · '+esc(s.workspace):''}</p><p class="muted">${s.admin?`${esc(t('Shared by {}',s.by||t('an admin')))}${s.held_by.length?' · '+esc(t('Held by {}',s.held_by.join(', '))):''}`:`${esc(t('Shared by {}',s.by||work.name))} · ${esc(t('Reads only'))}${s.have?'':' · '+esc(t('Waiting for an admin\'s Machine'))}`}</p>${s.mine&&s.service==='stripe'?'<p class="muted">Your Machine renews their access every hour. While it is off, their Stripe pauses.</p>':''}${s.admin?`<div class="actions"><button class="ghost danger" data-share-stop="${esc(s.service)}" data-fleet="${esc(work.id)}">Stop sharing</button></div>`:''}</article>`;
 // One Share per service this Machine has connected (its first account of each). Stripe goes to everyone by default.
 const can_send=own.filter(a=>!a.blocked),firsts=can_send.filter((a,i)=>can_send.findIndex(b=>b.service===a.service)===i);  // a Maton key opens more than Stripe: never sent
 const form=can?firsts.map(a=>`<details class="share-new"><summary>Share ${esc(a.label)}${a.workspace?' · '+esc(a.workspace):''}</summary><form class="share-form" data-fleet="${esc(work.id)}" data-account="${esc(a.id)}"><p class="muted">${esc(SHARE_NOTE[a.service]||SHARE_NOTE.intercom)}</p>${can.members.map(m=>`<label class="share-pick"><input type="checkbox" name="m" value="${esc(m.member_id)}"${m.confirmed?' checked disabled':a.service==='stripe'&&m.keys?' checked':''}${m.keys?'':' disabled'}> ${esc(m.name)} <small class="muted">${esc(m.confirmed?'admin':m.email||'')}${m.keys?'':' · needs an update'}</small></label>`).join('')}<div class="actions"><button class="primary">Share</button></div></form></details>`).join('')
  +(!shares.some(s=>s.service==='stripe')&&!firsts.some(a=>a.service==='stripe')?fleetConnectStripe(own.some(a=>a.blocked&&a.service==='stripe')):''):'';
 const graphAsks=mine.filter(p=>p.kind==='member'||p.kind==='optout'),conn=mine.filter(p=>p.kind!=='member'&&p.kind!=='optout');  /* the Shared Graph's own OKs (shared_graph.py) */
 const g=(v.graph||[]).find(s=>s.fleet===work.id&&s.confirmed);
 const ownGraph=g?`<article class="graph-own"><p>${g.off==='off'?'Your Work isn\'t shared with the team. What went before stays with them.':g.off==='asked'?'Asked an admin to stop sharing your Work. It stays on until they approve.':g.teammates===0?`Your Work goes to the team once ${g.admin?'you OK':'an admin OKs'} a teammate's Machine.`:g.paused?'Sharing is off in this Fleet.':g.started===false?'Your Work goes to the team within the hour. Keep anything private first.':'Your Work is shared with the team.'}${(g.require||[]).length?` ${esc(work.name)} requires your ${g.require.map(k=>({mail:'Work email',calendar:'Work calendar'})[k]).join(' and ')}.`:''}</p><div class="actions">${g.off?`<button type="button" class="ghost" data-graph-optout="${esc(work.id)}" data-off="0">${g.off==='off'?'Share again':'Keep sharing'}</button>`:''}<button type="button" class="ghost" data-shared-open="${esc(work.id)}">Choose connections</button></div></article>`:'';
 const joins=graphAsks.filter(p=>p.kind==='member'),sending=g?.sending?graphSendingLine(g.sending):'';if(sending&&!graphSendingWatch.t)graphSendingWatch.t=setTimeout(()=>fleetView(true).then(graphSendingWatch),4000);const all=joins.length>1?`<div class="actions"><button type="button" class="primary" data-graph-all="${esc(work.id)}">Share with all ${joins.length}</button></div>`:'';
 const devices=(g?.new_devices||[]).map(d=>`<article><p>${esc(d.name||'A teammate')} has a new Machine. It gets the team's Graph ${esc(sharedWhen(d.from))}.</p><p class="share-fp mono" title="Their Machine's safety number">${esc(d.fp||'')}</p><div class="actions"><button type="button" class="ghost danger" data-graph-rekey-no="${esc(d.member)}" data-fleet="${esc(work.id)}">Not theirs</button></div></article>`).join('');
 const see=g?`<p class="fleet-fine"><a href="#shared=${esc(work.id)}" data-shared-go="${esc(work.id)}">See what's shared</a></p>`:'';
 const graphBox=graphAsks.length||ownGraph||devices||sending?`<div class="fleet-box"><h3>Team Graph</h3><p class="muted">Work records and client threads, shared in the Fleet. Personal never.</p>${sending}${all}<div class="list">${graphAsks.map(card).join('')}${devices}${ownGraph}</div>${see}</div>`:'';
 if(!conn.length&&!shares.length&&!form)return graphBox;
 return graphBox+`<div class="fleet-box"><h3>Shared connections</h3>${conn.length?`<div class="list">${conn.map(card).join('')}</div>`:''}${shares.length?`<div class="list">${shares.map(row).join('')}</div>`:''}${form}</div>`}
const svcName=s=>({intercom:'Intercom',stripe:'Stripe'})[s]||s||'it';
const SHARE_NOTE={intercom:'Use a dedicated Intercom app with read permissions only. Admins get it. Tick who else does.',
 stripe:'Teammates read failed payments, disputes and cancellations. Nobody changes anything in Stripe. Untick who shouldn’t.'};
// An admin without Stripe here: connect it once for the team (hosted: the account page signs it in; else Connections, + Add)
const fleetConnectStripe=blocked=>`<article class="share-connect"><p><strong>Stripe for the team</strong></p>${blocked?'<p class="muted">Your Stripe connection here can’t be shared: its key opens more than Stripe.</p>':''}<p class="muted">Connect it once. Teammates’ Machines read it, read only.</p><div class="actions">${state.manage_url?`<a class="btn-link" href="${esc(state.manage_url)}#source-stripe" target="_blank" rel="noopener">Connect Stripe ↗</a>`:'<button type="button" data-fleet-connect="stripe">Connect Stripe</button>'}</div></article>`;
// Share: the OK is signed at once; sealing the team's Graph for them runs after (shared_connectors.graph_soon). One line while it does.
const graphSendingLine=n=>`<p class="graph-sending" role="status"><i class="spin" aria-hidden="true"></i>Sharing with ${n}…</p>`;
const graphSent={};  // fleet: how many Share with all shared with, to say so once the line is gone
function graphSendingWatch(){const list=(fleetData?.shared?.graph)||[];let busy=false;
 for(const g of list){if(g.sending)busy=true;else if(graphSent[g.fleet]){toast(`Shared with ${graphSent[g.fleet]}.`);delete graphSent[g.fleet]}}
 clearTimeout(graphSendingWatch.t);graphSendingWatch.t=busy?setTimeout(()=>fleetView(true).then(graphSendingWatch),4000):0}
function fleetBrief(f,work){const b=(f.briefs||{})[work.id];if(!b)return'';const items=b.items||[],n=b.shown||5;
 const line=(i,k)=>`<li class="fleet-brief-item${k>=n?' fleet-brief-more':''}"${k>=n?' hidden':''}><span class="fleet-brief-line"><strong title="${esc(i.title)}">${esc(i.title)}</strong><small class="muted">${esc(i.why)}</small></span><span class="fleet-brief-do">${i.open?`<a class="fleet-brief-open" href="${esc(safeURL(i.open))}" target="_blank" rel="noopener">Open</a>`:''}${i.ask?`<button type="button" class="ghost" data-brief-ask="${esc(i.ask)}" data-fleet="${esc(work.id)}">Ask</button>`:''}<button type="button" class="quiet" data-brief-hide="${esc(i.key)}" data-fleet="${esc(work.id)}">Not needed</button></span></li>`;
 return `<article class="fleet-brief" id="fleet-brief-${esc(work.id)}"><p><strong>What the Fleet saw</strong> <small class="muted">${fleetDay(b.built_at)}</small></p>${items.length?`<ul class="fleet-brief-list">${items.map(line).join('')}</ul>${items.length>n?`<button type="button" class="quiet fleet-brief-show" data-brief-more>Show ${items.length-n} more</button>`:''}`:'<p class="muted">Nothing that needs the team.</p>'}</article>`}
// Teammates' brief asks (fleet.py QUIET): never a to-do. One quiet box in their Fleet's pane, the latest ask per teammate
// (older ones expire), with the same choices as before. Nothing is shared until the owner picks one; unanswered, they expire.
const FLEET_QUIET=['brief'];
// What an answer would share, as counts (an ask from before counts came along: its preview line)
const briefCounts=d=>{const c=d?.counts;if(!c)return d?.preview?[d.preview.replace(/ \(as hashes\)/,'')]:[];
 return [['Companies: {}',c.touched],['Went quiet: {}',c.quiet],['Unanswered emails: {}',c.unanswered],['Meetings with outside people: {}',c.meetings]].map(([k,n])=>k.replace('{}',n))};
function fleetBriefAsks(f,work,inFleet){const asks=(f.waiting||[]).filter(w=>w.kind==='brief'&&inFleet(w,work));if(!asks.length)return'';
 const decide=(w,c,label,cls='ghost')=>`<button type="button" class="${cls}" data-fleet-decide="${esc(w.id)}" data-choice-f="${c}">${esc(label)}</button>`;
 const row=w=>`<li class="fleet-brief-item" id="fleet-${esc(w.id)}"><span class="fleet-brief-line"><strong>${esc(w.name)}</strong><small class="muted">${[/for the week/.test(w.question)?'Weekly brief':'Daily brief',...briefCounts(w.draft)].map(esc).join(' · ')}</small></span><span class="fleet-brief-do">${decide(w,'once','Share once','primary')}${decide(w,'always','Always share')}${decide(w,'decline','Decline')}${decide(w,'never','Never')}</span></li>`;
 return `<div class="fleet-box fleet-brief-asks"><h3>Brief requests <span class="count">${asks.length}</span></h3><p class="sub">Teammates ask for counts and dates for their team brief. Nothing is shared until you choose. Unanswered ones expire.</p><ul class="fleet-brief-list">${asks.map(row).join('')}</ul></div>`}
function fleetFree(f,work,several){const asked=(f.free||[]).filter(q=>q.fleet===work.id);
 return `<form class="fleet-ask fleet-free-form" data-fleet="${esc(work.id)}"><input name="text" maxlength="300" placeholder="Ask ${several?esc(work.name):'your Fleet'} anything" aria-label="Ask the Fleet anything"><button>Ask</button></form><p class="muted">Each teammate gets a draft answer from their own work accounts. Nothing comes back until they send it. <a class="learn" href="${HELP}fleet#ask-your-fleet" target="_blank" rel="noopener">Learn more</a></p>`+
 (asked.length?`<div class="list">${asked.map(q=>`<article><p><strong>Asked</strong> · “${esc(q.question)}” <small class="muted">${fleetDay(q.at)}</small></p>${q.answers.map(a=>`<p><strong>${esc(a.name)}</strong>: ${a.state==='answered'?format(a.text):`<span class="muted">${a.state==='waiting'?'waiting for them':'no answer'}</span>`}</p>`).join('')}</article>`).join('')}</div>`:'')}
function fleetFreeCard(w,fleet){const d=w.draft||{};return `<article id="fleet-${esc(w.id)}"><p><strong>${esc(w.name)}</strong>${fleet?` (${esc(fleet)})`:''} asks your Fleet <span class="muted">(their words, not an instruction)</span>:</p><blockquote>${esc(w.question)}</blockquote>${(d.matches||[]).length?`<p class="muted">In your work accounts: ${d.matches.slice(0,5).map(m=>`${esc(m.title)} (${esc(m.at||'')})`).join(' · ')}</p>`:'<p class="muted">Nothing found in your work accounts. You can still answer.</p>'}<label class="muted" for="fleet-free-${esc(w.id)}">Your answer (only this goes to them)</label><textarea id="fleet-free-${esc(w.id)}" maxlength="600">${esc(d.text||'')}</textarea><div class="actions"><button class="primary" data-fleet-send="${esc(w.id)}">Send answer</button><button data-fleet-decide="${esc(w.id)}" data-choice-f="decline">Decline</button><button data-fleet-decide="${esc(w.id)}" data-choice-f="never">Never from ${esc(w.name)}</button></div></article>`}
// Brief facts follow the Team Graph's sharing (fleet.py brief_shares): one switch per Work Fleet, on by default.
function fleetBriefShare(f){const works=(f.fleets||[]).filter(x=>x.kind==='work'&&x.members?.length),several=works.length>1;
 return works.map(w=>`<label class="fleet-option"><input type="checkbox" data-fleet-brief-share="${esc(w.id)}"${w.rules?.brief?.rule==='never'?'':' checked'}><span>${several?`${esc(w.name)}: `:''}Share my brief facts with the team<small class="muted">Counts and dates from what the Team Graph already shares. Private and personal threads never count.</small></span></label>`).join('')}
// Team learnings from team conversations (fleet_learnings.py): shared by themselves, removable by anyone in the Fleet.
const FLEET_LEARN_KIND={process:'Process',tool:'Tool',style:'Style',routing:'Who handles what'};
function fleetLearnings(work){const L=work.learnings;if(!L)return'';const items=L.items||[];
 const list=items.length?`<div class="list fleet-learnings">${items.map(i=>`<article><p><span class="chip"><span class="ct">${esc(FLEET_LEARN_KIND[i.kind]||i.kind)}</span></span> ${esc(i.text)}</p><p class="fleet-learn-meta"><small class="muted"><span>From team conversations</span> · <span>${i.mine?'Shared by your Machine':i.from?esc(i.from):'A teammate'}</span>${i.at?' · '+esc(new Date(i.at+'T12:00:00').toLocaleDateString(DL,{month:'short',day:'numeric'})):''}</small><button type="button" class="ghost" data-fleet-learn-remove="${esc(i.fp)}" data-fleet="${esc(work.id)}">Remove</button></p></article>`).join('')}</div>`
  :`<p class="muted">${L.on?'Nothing yet. Your Machine looks once a day.':'Off. Turn it on in Settings, Security.'}</p>`;
 return `<div class="fleet-box fleet-learn-box"><h3>Team learnings</h3><p class="sub">How the team works, from conversations the Team Graph shares. Never names or customer details. <a class="learn" href="${HELP}fleet#team-learnings" target="_blank" rel="noopener">Learn more</a></p>${list}</div>`}
function fleetBriefSettings(f){const b=f.brief||{every:'off'};return fleetBriefShare(f)+`<p class="fleet-brief-row"><label>Team brief: <select id="fleet-brief-every">${[['off','Off'],['day','Daily'],['week','Weekly']].map(([v,l])=>`<option value="${v}"${b.every===v?' selected':''}>${l}</option>`).join('')}</select></label> <label><input type="checkbox" id="fleet-brief-tell"${b.tell?' checked':''}> Also send it to me</label><small class="muted" title="On work days at your morning time: quiet companies, shared ones, unanswered inbound and shared meetings.">Quiet accounts, shared inbound and meetings. Counts and dates only.</small></p>`}
// Warm intros, handoffs and shared follow-ups (fleet_requests.py). A teammate's words are shown quoted, as data; accepting makes a
// card from this Machine's own data, and anything that card sends waits for the owner's own Send.
const FLEET_REQ=['intro','handoff','followup'],handingOff=new Map(),fleetNoting=new Map();
// Decline (or Accept with a note) on a teammate's request: an optional short reason, with quick picks; only they see it.
const DECLINE_PICKS=['Not mine','Already done','No time this week'];
function fleetNoteEditor(w,c){const id=esc(w.id),no=c==='decline';return`<div class="change-editor dismiss-editor fleet-note-editor"><p class="dismiss-q" id="fleet-note-q-${id}">${no?'Why?':esc(t('Note to {}',w.name))} <small>Optional</small></p>${no?`<div class="reason-chips" role="group" aria-labelledby="fleet-note-q-${id}">${DECLINE_PICKS.map(r=>`<button type="button" class="reason" aria-pressed="false" data-fleet-pick="${esc(r)}">${esc(r)}</button>`).join('')}</div>`:''}<textarea id="fleet-note-${id}" rows="1" maxlength="160" aria-label="Note (optional)" placeholder="Add a note (optional)"></textarea><p class="muted">Only ${esc(w.name)} sees it.</p><div class="actions"><button class="primary" data-fleet-note-send="${id}" data-choice-f="${c}">${no?'Decline':'Accept'}</button><button type="button" class="ghost" data-fleet-note-cancel="${id}">Cancel</button></div></div>`}
// A handoff a teammate declined (or let expire): the card is back, with what to do now.
const handoffBackActions=s=>`<div class="actions"><button class="primary" data-handoff-mine="${esc(s.id)}">Do it myself</button>${canHandoff(s)?`<button class="ghost" data-fleet-handoff="${esc(s.id)}">Hand off to someone else</button>`:''}<button class="ghost" data-id="${s.id}" data-choice="complete">Mark done</button></div>`;
// With a teammate who hasn't answered: under Later it is with them; back on top (a deadline came) it asks for a check-in.
function handoffLine(h,s){const names=[String(h.name||t('your teammate')).split(' ')[0],...(h.also||[])],first=names.length>1?t('{} and {}',names.slice(0,-1).join(', '),names.at(-1)):names[0];if(h.line)return esc(h.line);
 const next=s&&redirect(s)&&taskActions(s).find(a=>a.kind==='handoff'&&a.to_name&&firstName(a.to_name)!==firstName(h.name));
 if(next)return esc(t('Still with {} until you send it to {}',first,firstName(next.to_name)));
 return ['asked','waiting for them'].includes(h.stage)?(s&&withTeammate(s)?`${esc(t('Still with {}',firstName(h.name)))} · <a class="link" href="#chat=${esc(s.id)}" title="Open the chat">${esc(t('check in?'))}</a>`:esc(t('With {} · waiting',first))):h.stage==='declined'?esc(h.note?t('{} declined: {}',h.name,h.note):t('{} declined.',h.name)):h.stage==='expired'?esc(t('{} didn’t answer in time.',h.name)):esc(h.note?t('Handed off to {}: {} ({})',h.name,t(h.stage),h.note):t('Handed off to {}: {}',h.name,t(h.stage)))}
// Fleet items that need you are cards under Suggestions (tagged Fleet, Work), built from api/fleet: a teammate's
// question or request (their words, shown quoted, never acted on), a meeting's follow-ups to split, and confirmations
// the relay asks for. The Fleet tab keeps people, rules, briefs, your own asks and the log.
const splitDay=v=>{const d=new Date(String(v).length<=10?v+'T12:00':v);return isNaN(d)?String(v):d.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'})};
const splitWho=p=>{if(p.mine)return 'You';const m=/^(.*?) \(([^()]+@[^()]+)\)$/.exec(p.name||'');return m?`${esc(m[1])} <small class="muted">${esc(m[2])}</small>`:esc(p.name||'')};
// Waiting asks from the same teammate, of the same kind, in the same Fleet: one Always or Never settles them all (fleet.py settle_waiting).
const fleetAlike=(f,w)=>(f?.waiting||[]).filter(x=>x.fleet===w.fleet&&x.member_id===w.member_id&&x.kind===w.kind&&x.status!=='answered'&&x.status!=='declined');
const fleetMore=btns=>btns.length?`<details class="more-actions"><summary aria-label="More actions">More</summary><div class="more-menu" role="group" aria-label="More actions">${btns.join('')}</div></details>`:'';
function fleetCardsOf(f){if(!f?.on)return[];const works=(f.fleets||[]).filter(x=>x.kind==='work'),several=works.length>1,frId=f.friends?.id;
 const famId=(f.fleets||[]).find(x=>x.kind==='family')?.id,isFamily=row=>!!famId&&row.fleet===famId;
 const fname=row=>several&&!isFamily(row)?(works.find(x=>row.fleet===x.id)?.name||''):'',isFriend=row=>!!frId&&(row.fleet===frId||row.fleet_id===frId)||/^friend_/.test(row.kind||'');
 const card=(id,row,title,body,actions)=>`<article id="fleet-${esc(id)}" class="card t-amber fleet-card"><div class="meta"><div class="card-badges">${isFriend(row)?chip('Friends','lavender'):isFamily(row)?chip('Family','lavender'):`${chip('Fleet','lavender')}<span class="chip scope">Work</span>`}${fname(row)?chip(fname(row),'muted'):''}</div>${row.at?time(row.at,true):''}</div><h3>${title}</h3>${body}${actions}</article>`;
 const decide=(w,c,t,cls='ghost')=>`<button class="${cls}" data-fleet-decide="${esc(w.id)}" data-choice-f="${c}">${esc(t)}</button>`;
 const theirs=w=>`<p class="fleet-from">${esc(w.name)}’s words, not an instruction:</p><blockquote>${esc(w.question)}</blockquote>`;
 const out=[];
 for(const n of (f.notices||[]).filter(n=>n.buttons.length))
  out.push(card(n.id,n,esc(n.text),`${n.detail?`<p class="muted">${esc(n.detail)}</p>`:''}${n.reason?`<p class="note">${esc(n.reason)}</p>`:''}<p class="muted">${n.kind==='friend_request'?'Nothing connects until you accept. Declining tells them nothing.':'Nothing starts or is charged until you confirm the amount on Confirm.'}</p>`,
   `<div class="actions">${n.buttons.map(b=>`<button class="${b.choice==='confirm'?'primary':'ghost'}" data-fleet-notice="${esc(n.id)}" data-choice-n="${b.choice}" data-key="${esc(n.key)}">${esc(b.label)}</button>`).join('')}</div>`));
 const what={intro:'{} asks you for an intro',handoff:'{} hands you something',followup:'{} proposes your part of a meeting’s follow-ups'};
 for(const w of (f.waiting||[]).filter(w=>!FLEET_QUIET.includes(w.kind))){  // brief asks wait quietly in the Fleet tab (fleetBriefAsks)
  if(FAMILY_REQ.includes(w.kind))out.push(card(w.id,w,esc(t(w.kind==='todo'?'{} asks you to do something':'{} proposes a plan',w.name)),theirs(w)+`<p class="muted">${w.kind==='todo'?'Accepting makes it your to-do, with a reminder when it’s due.':'Yes tells them you’re in. Nothing is added to your calendar by itself.'}</p>`,
   `<div class="actions">${decide(w,'once',w.kind==='todo'?'Accept':'I’m in','primary')}${decide(w,'decline',w.kind==='todo'?'Decline':'Can’t make it')}${fleetMore([decide(w,'always','Always accept'),decide(w,'never','Never from '+w.name)])}</div>`));
  else if(FLEET_REQ.includes(w.kind))out.push(card(w.id,w,esc(t(what[w.kind],w.name)),theirs(w)+(w.kind==='followup'?`<label class="fleet-field muted" for="fleet-part-${esc(w.id)}">Or change your part<input id="fleet-part-${esc(w.id)}" maxlength="200" placeholder="Your part, as you’ll do it"></label>`:'')+'<p class="muted">Accepting makes a to-do from your own data. Anything it sends waits for your Send.</p>',
   fleetNoting.has(w.id)?fleetNoteEditor(w,fleetNoting.get(w.id)):`<div class="actions">${decide(w,'once','Accept','primary')}${w.kind==='followup'?`<button class="ghost" data-fleet-adjust="${esc(w.id)}">Accept my change</button>`:''}${decide(w,'decline','Decline')}${fleetMore([`<button class="ghost" data-fleet-noting="${esc(w.id)}">Accept with a note</button>`,decide(w,'always','Always accept'),decide(w,'never','Never from '+w.name)])}</div>`));
  else if(w.kind==='anything'){const d=w.draft||{};out.push(card(w.id,w,`${esc(w.name)} asks your Fleet`,theirs(w)+((d.matches||[]).length?`<p class="muted">In your work accounts: ${d.matches.slice(0,5).map(m=>`${esc(m.title)} (${esc(m.at||'')})`).join(' · ')}</p>`:'<p class="muted">Nothing found in your work accounts. You can still answer.</p>')+`<label class="fleet-field muted" for="fleet-free-${esc(w.id)}">Your answer (only this goes to them)<textarea id="fleet-free-${esc(w.id)}" maxlength="600">${esc(d.text||'')}</textarea></label>`,
   `<div class="actions"><button class="primary" data-fleet-send="${esc(w.id)}">Send answer</button>${decide(w,'decline','Decline')}${fleetMore([decide(w,'never','Never from '+w.name)])}</div>`))}
  else{const n=fleetAlike(f,w).length;
   out.push(card(w.id,w,`${esc(t('{} asks:',w.name))} <span translate="no">${esc(w.question)}</span>`,`${w.draft?.preview?`<p class="muted">Would share: ${esc(w.draft.preview)}</p>`:''}<p class="muted">Nothing is shared until you choose. Always and Never also cover their future asks like this.</p>${n>1?`<p class="muted fleet-bulk">${esc(t(['{} more like this waits. Always shares it too.','{} more like this wait. Always shares them too.'],n-1))}</p>`:''}`,
   `<div class="actions">${decide(w,'once','Share once','primary')+decide(w,'always','Always share')}${decide(w,'decline','Decline')}${fleetMore([decide(w,'never','Never share')])}</div>`))}}
 for(const sp of (f.splits||[]).filter(x=>x.status==='proposed'))
  out.push(card('split-'+sp.id,{...sp,at:null},`${esc(sp.title||'A meeting')} <small class="muted">${esc(splitDay(sp.day||''))}</small>`,
   `<p class="fleet-from">Follow-ups of a meeting with Fleet teammates. Split who does what; nothing goes until you send it.</p><details class="split-why"><summary>Why you?</summary>One Machine proposes the split, so nobody follows up twice: the organizer’s, or else the one longest in the Fleet.</details>${sp.notes?`<p class="split-note">Filled in from the ${esc(sp.notes)} notes. Check it before you send.</p>`:''}`,
   `<form class="fleet-split-form" data-split="${esc(sp.id)}"><div class="split-parts">${sp.parts.map(p=>`<label class="split-part${p.from_notes?' suggested':''}"><span class="split-who">${splitWho(p)}</span><input id="split-${esc(sp.id)}-${esc(p.member_id)}" name="${esc(p.member_id)}" maxlength="200" value="${esc(p.what||'')}" placeholder="${p.mine?'Your follow-up':'Their follow-up (leave empty for none)'}"></label>`).join('')}</div><div class="actions"><button class="primary">Send the split</button><button type="button" class="ghost" data-split-dismiss="${esc(sp.id)}">Not needed</button></div></form>`));
 // The Team Graph's OKs: only a confirmed admin's Machine gets them, and one admin's answer counts for the whole team
 const gname=p=>p.fleet_name||works.find(x=>x.id===p.fleet)?.name||'';
 const graphAsk={member:p=>esc(t('{} joined {}. Share the team\'s Graph with them?',p.name,gname(p))),optout:p=>esc(t('{} asks to stop sharing their Work with the team.',p.name)),admin:p=>esc(t('Confirm {} as an admin of {}?',p.name,gname(p)))};
 for(const p of (f.shared?.prompts||[]).filter(p=>graphAsk[p.kind]))
  out.push(card('share-'+p.id,p,graphAsk[p.kind](p),`${p.email?`<p class="muted">${esc(p.email)}</p>`:''}<p class="muted">${p.kind==='admin'?'Admins can share the team’s Graph and connections. Check it’s really them.':'Only admins decide this, once for the whole team.'}</p>${p.fp&&p.kind!=='optout'?`<p class="share-fp mono" title="Their Machine's safety number">${esc(p.fp)}</p>`:''}`,
   `<div class="actions"><button class="primary" data-share-ok="${esc(p.id)}" data-kind="${esc(p.kind)}" data-choice="yes">${p.kind==='member'?'Share':p.kind==='admin'?'Confirm':'Approve'}</button><button class="ghost" data-share-ok="${esc(p.id)}" data-choice="no">Not now</button></div>`));
 out.push(...networkCards(f));
 return out}
// Finding people you know on the Network (discovery.py): a permission card once, then a card per person only with a concrete reason
const netBtn=(label,d,email='',rel='',cls='ghost',confirmText='')=>`<button type="button" class="${cls}" data-net-do="${d}"${email?` data-net-email="${esc(email)}"`:''}${rel?` data-net-rel="${rel}"`:''}${confirmText?` data-confirm-text="${esc(confirmText)}"`:''}>${esc(label)}</button>`;
const netDay=at=>{const d=new Date(at);return isNaN(d)?'':d.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'})};
const netReason=r=>r.kind==='card'?esc(t('Open: {}',r.title)):r.kind==='meeting'?`${esc(t('You meet {}',netDay(r.at)))}${r.title?` · ${esc(r.title)}`:''}`:r.kind==='contact'?t('In your contacts'):r.kind==='joined'?esc(t('Joined {}, in your contacts',netDay(r.at))):'';
function networkCards(f){const net=f.network;if(!net||!f.friends?.id)return[];const out=[];
 const card=(id,title,body,actions)=>`<article id="net-${esc(id)}" class="card t-amber fleet-card net-card"><div class="meta"><div class="card-badges">${chip('Network','lavender')}</div></div><h3>${title}</h3>${body}${actions}</article>`;
 if(net.find==null&&!net.asked)out.push(card('ask','Which of your contacts have a Machine?',`<p class="muted">Your Machine checks your contacts against people who chose to be findable, and your address book stays private. It suggests the people you know right away, and others when you meet or work with them. Nothing is shared until they accept.</p>`,
  `<div class="actions">${netBtn('Check my contacts','find_on','','','primary')}${netBtn('Not now','asked')}</div>`));
 for(const p of (net.people||[]).filter(p=>p.status==='new'&&p.reasons.length)){
  const who=p.hint==='colleague'?'Same work domain as you.':'Friend or family? You choose.';
  out.push(card(p.username,`${esc(p.name)} is on the Network`,`<ul class="net-reasons">${p.reasons.slice(0,2).map(r=>`<li>${netReason(r)}</li>`).join('')}</ul><p class="muted">${who}${p.role?` You call them ${esc(p.role)}.`:''} Connecting sends a friend request; nothing is shared until they accept, then only what your rules allow.</p>`,
   `<div class="actions">${p.hint==='colleague'?netBtn('Connect','connect',p.email,'colleague','primary'):netBtn('Friend','connect',p.email,'friend','primary')+netBtn('Family','connect',p.email,'family')}${netBtn('Not now','later',p.email)}${fleetMore([netBtn(t('Never suggest {}',p.name),'never',p.email)])}</div>`))}
 return out}
function networkSection(f){const net=f.network;if(!net||!f.friends?.id)return'';
 const sw=(on,label,doOn,doOff)=>`<label class="net-switch"><input type="checkbox" data-net-toggle="${on?doOff:doOn}"${on?' checked':''}> ${esc(label)}</label>`;
 const rest=(net.people||[]).filter(p=>p.status==='new'&&!p.reasons.length||p.status==='later'),waiting=(net.people||[]).filter(p=>p.status==='requested');
 let h=`<div id="fleet-network"><div class="section-head"><h2>Network</h2><p>See which of your contacts have a Machine, and let people who know you find you. Your address book is never revealed. <a class="learn" href="${HELP}friends#find-people-you-know" target="_blank" rel="noopener">Learn more</a></p></div><div class="net-switches">${sw(!!net.find,'Check which of my contacts have a Machine','find_on','find_off')}${sw(!!net.discoverable,'Let people who have my email find me','discoverable_on','discoverable_off')}</div>`;
 if(net.default_at&&net.discoverable)h+=`<p class="muted net-default"><span>${esc(t('Now findable by people who have your email.'))}</span>${netBtn('Turn off','discoverable_off')}</p>`;  // turned on by default, not by the owner
 const addrs=net.discoverable?(net.addresses||[]):[];
 if(addrs.length)h+=`<div class="net-addrs"><span class="muted">Findable by</span>${addrs.map(a=>`<label class="net-switch"${a.account?' title="Your account email"':''}><input type="checkbox" data-net-addr="${esc(a.email)}"${a.on?' checked':''}${a.account?' disabled':''}> ${esc(a.email)}${a.on&&!a.findable?' <small class="muted">(not yet)</small>':''}${a.shared?` <small class="muted">${esc(t('Shared address'))}</small>`:''}</label>`).join('')}</div>`;
 if(net.find&&net.last)h+=`<p class="muted">${esc(t('Last checked {}. Checks every 15 minutes for new contacts and people who just joined.',netDay(net.last)))}</p>`;
 if(rest.length)h+=`<h3>Your contacts with a Machine</h3><ul class="fleet-people">${rest.map(p=>`<li class="fp-row"><span class="fp-who"><strong>${esc(p.name)}</strong> <small class="muted">@${esc(p.username)}</small></span><span class="actions">${p.hint==='colleague'?netBtn('Connect','connect',p.email,'colleague'):netBtn('Friend','connect',p.email,'friend')+netBtn('Family','connect',p.email,'family')}${netBtn('Never','never',p.email)}</span></li>`).join('')}</ul>`;
 if(waiting.length)h+=`<p class="muted">Waiting for ${waiting.map(p=>esc(p.name)).join(', ')} to accept.</p>`;
 h+=meetSetting(f.meet);
 h+=`<p>${netBtn('Leave the Network','leave','','','ghost','Leave the Network? Every friendship ends and nobody can find you. Your Fleets stay.')}</p></div>`;
 return h}
const fleetSig=()=>JSON.stringify(fleetCardsOf(fleetData));
// Suggestions load the Fleet's open items in the background (at most every 20 seconds) and re-render when they change.
let fleetAt=0,fleetLoading=null;
function fleetSync(force){if(!state?.fleet?.on)return Promise.resolve();if(fleetLoading)return fleetLoading;if(!force&&Date.now()-fleetAt<20000)return Promise.resolve();
 const before=fleetSig();fleetLoading=request('api/fleet').then(d=>{fleetData=d;fleetAt=Date.now();if(fleetSig()!==before)render();if(!$('#fleet').hidden&&!($('#fleet-view').contains(document.activeElement)&&document.activeElement.matches('input,select,textarea')))fleetView(false,true)}).catch(()=>{fleetAt=Date.now()}).finally(()=>{fleetLoading=null});return fleetLoading}
const fleetOn=(type,fn)=>{for(const el of [$('#fleet-view'),$('#suggestions')])el.addEventListener(type,fn)};
// What's shared (shared_graph.overview): one place per Work Fleet with counts, what went and why, Share these?, and what stays private.
// Loaded when its pane opens; every list item is the owner's own mail, shown as text.
// The consent an admin gives before the team's Graph starts, or before the Fleet requires its members' Work email or
// calendar: short and plain, with who is responsible. Resolves true on the OK.
function shareConsent(title,points,fine,ok){const d=$('#share-consent');$('#share-consent-title').textContent=title;
 $('#share-consent-body').innerHTML=`<ul>${points.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>${fine?`<p class="fleet-fine">${esc(fine)}</p>`:''}`;$('#share-consent-ok').textContent=ok;
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
const sharedTitle=x=>x.event_id?`<button type="button" class="shared-read ell" data-shared-read="${esc(x.event_id)}" title="${esc(x.title)}">${esc(x.title||'(no subject)')}</button>`:`<span class="ell" title="${esc(x.title)}">${esc(x.title||'(no subject)')}</span>`;
const sharedRow=(x,act)=>`<li class="shared-row"><span class="grow">${sharedTitle(x)}<small class="muted">${esc([x.why,x.at&&shortDay(x.at)].filter(Boolean).join(' · '))}</small></span>${act}</li>`;
const sharedAsking={};  // the admin's open "Turn off sharing for everyone?" per Fleet: it stays open through a reload
const CONN_LABEL={gmail:'Gmail',outlook:'Outlook',calendar:'Google Calendar',outlook_calendar:'Outlook Calendar',slack:'Slack',salesflare:'Salesflare',whatsapp:'WhatsApp',intercom:'Intercom',linkedin:'LinkedIn',x:'X',telegram:'Telegram'};
function sharedHTML(work,g,d){const n=x=>Number(x||0).toLocaleString(DL),fleet=esc(work.id);
 let h=`<div class="fleet-box shared-status"><h3>${esc(t('What\'s shared with {}',work.name))}</h3><p class="sub">${esc(t(sharedStatus(g,d)))}</p>`;
 const on=!g?.paused;
 if(g)h+=`<div class="shared-switch"><span class="grow"><strong>Share the Graph in this Fleet</strong><span class="exp-tag">Experimental</span><small>${esc([t(on?'On for everyone.':'Off for everyone.'),t('New and still changing.'),g.admin?'':t('Only an admin can change this.')].filter(Boolean).join(' '))}</small></span><button type="button" class="lookup-switch" role="switch" aria-checked="${on}" aria-label="Share the Graph in this Fleet" data-graph-switch="${fleet}"${g.admin?'':' disabled'}></button></div>${g.admin&&on?`<div class="shared-off-ask"${sharedAsking[work.id]?'':' hidden'}><p><strong>Turn off sharing for everyone?</strong></p><p class="fleet-fine muted">Nothing new goes. What went stays on teammates' Machines, unless you remove it. Someone may have read it already.</p><div class="actions"><button type="button" class="primary" data-graph-pause="${fleet}" data-on="1">Turn off</button><button type="button" class="ghost" data-graph-pause="${fleet}" data-on="1" data-remove="1">Turn off and remove shared data</button><button type="button" class="ghost" data-off-cancel>Cancel</button></div></div>`:''}`;
 const req=g?.require||[],REQ={mail:'Work email',calendar:'Work calendar'};
 if(g?.admin)h+=`<div class="shared-require"><strong>Required by the Fleet</strong><small>Members can't turn these off. Threads they keep private stay private.</small>${Object.entries(REQ).map(([k,l])=>`<label><input type="checkbox" data-graph-require="${k}" data-fleet="${fleet}"${req.includes(k)?' checked':''}> ${l}</label>`).join('')}</div>`;
 else if(req.length)h+=`<p class="fleet-fine">${esc(t(req.length>1?'{} requires your Work email and Work calendar.':req[0]==='mail'?'{} requires your Work email.':'{} requires your Work calendar.',work.name))} ${esc(t('They belong to the company. Threads you keep private stay private.'))}</p>`;
 h+=`<div class="shared-tiles">${SHARED_TILES.map(([k,label,hint,about])=>`<div class="shared-tile" title="${esc(t(about))}"><b>${n(d.sorted[k])}</b><span>${esc(t(label))}</span><small>${esc(t(hint))}</small></div>`).join('')}<div class="shared-tile"><b>${n(d.unsorted)}</b><span>Not sorted yet</span><small>stays with you</small></div><div class="shared-tile sent"><b>${n(d.sent)}</b><span>Sent</span><small>threads the team has</small></div></div></div>`;
 const conns=g?.connections||[];
 if(conns.length)h+=`<div class="fleet-box shared-conns"><h3>Your connections</h3><p class="sub">${esc(t('What feeds {}\'s Graph. {}\'s Work starts on. Other companies\' start off. Personal never goes.',work.name,work.name))}</p><ul class="list shared-list">${conns.map(c=>`<li class="shared-row"><span class="grow"><span class="ell">${esc(CONN_LABEL[c.service]||(c.service?service(c.service):'Connection'))}${c.name||c.email?' · '+esc(c.name||c.email):''}</span><small class="muted">${esc(c.personal?t('Personal, never shared'):c.required?t('Required by {}',work.name):t(c.company?'Work':c.on?'Other company, shared':'Other company, not shared'))}</small></span>${c.personal?'':`<button type="button" class="lookup-switch" role="switch" aria-checked="${!!c.on}" aria-label="${esc(t('Share {}',c.email||c.service))}" data-graph-conn="${esc(c.id)}" data-fleet="${fleet}"${c.required?' disabled':''}></button>`}</li>`).join('')}</ul></div>`;
 const pv=d.preview;
 if(pv&&g&&!g.started)h+=`<div class="fleet-box shared-first"><h3>Before the first share</h3><p class="sub">${esc(pv.threads?t(['{} client thread with these organizations goes to the team. Keep any private first.','{} client threads with these organizations go to the team. Keep any private first.'],pv.threads):t('No client threads to share yet.'))}</p>${pv.orgs.length?`<ul class="list shared-list">${pv.orgs.map(o=>sharedRow({title:o.name,why:t(['{} thread','{} threads'],o.threads)},`<button type="button" class="ghost" data-shared-rule="${esc(o.key)}" data-name="${esc(o.name)}" data-choice="private">Keep private</button>`)).join('')}</ul>${pv.more?`<p class="fleet-fine muted">${esc(t('And {} more.',pv.more))}</p>`:''}`:''}<div class="actions"><button type="button" class="ghost" data-graph-start="${fleet}">Share now</button></div><p class="fleet-fine muted">It goes by itself within the hour. Nothing to confirm.</p></div>`;
 h+=`<details class="fleet-box shared-how"${g?.started?'':' open'}><summary><h3>How sharing works</h3></summary><dl class="shared-facts">${[
  ['Goes','Work records and client threads, with attachments.'],
  ['Sensitive','Deals, HR and hiring, legal, health, money, security. Nothing of it goes.'],
  ['Never','Personal mail, receipts, alerts and newsletters, internal threads with only colleagues, and what you keep private.'],
  ['Not sure','Stays with you until you choose.'],
  ['Shared boards','The people you pick get each project\'s full timeline: email, meetings, Intercom, chats, to-dos and moves.'],
  ['Who sees it',t('Confirmed Machines in {}. The Network can\'t read it.',work.name)],
  ['Someone leaves','They get nothing new. What they had stays.']].map(([k,v])=>`<div><dt>${esc(t(k))}</dt><dd>${esc(t(v))}</dd></div>`).join('')}</dl><p class="fleet-fine"><a class="learn" href="${HELP}team-graph" target="_blank" rel="noopener">Learn more</a></p></details>`;
 if(d.unsure.length)h+=sharedAskHTML(d);
 const shown=sharedShown[work.id]||20,list=d.threads;
 h+=`<div class="fleet-box shared-out"><h3>${g?.started?'Shared':'Goes within the hour'} <span class="count">${n(d.shared+d.waiting)}</span></h3>${list.length?`<ul class="list shared-list">${list.slice(0,shown).map(x=>sharedRow(x,`<button type="button" class="ghost" data-shared-set="${x.event_id}" data-share="only_you"${g?.started?'':' data-before="1"'}>${g?.started?'Unshare':'Keep private'}</button>`)).join('')}</ul>${list.length>shown||d.more?`<button type="button" class="quiet" data-shared-more="${fleet}">Show more</button>`:''}`:'<p class="muted">Nothing yet.</p>'}</div>`;
 const rules=d.rules.map(r=>`<li class="shared-row"><span class="grow"><span class="ell">${esc(r.name||r.key)}</span><small class="muted">${r.choice==='private'?'Always only you':'Always share client threads'} · ${esc(r.key)}</small></span><button type="button" class="ghost" data-shared-rule="${esc(r.key)}" data-choice="none">Remove</button></li>`).join('');
 const recs=d.records.map(r=>`<li class="shared-row"><span class="grow"><span class="ell">${esc(r.name)}</span><small class="muted">${esc(({org:'Organization',person:'Person',project:'Project'})[r.kind]||'Record')} and its threads</small></span><button type="button" class="ghost" data-shared-record="${esc(r.node_id)}">Share again</button></li>`).join('');
 const hand=d.by_hand.map(x=>sharedRow(x.shared_with?.length?{...x,why:t('Only you and {}',namesLine(x.shared_with))}:x,`<button type="button" class="ghost" data-shared-set="${x.event_id}" data-share="team">Share</button>`)).join('');
 h+=`<div class="fleet-box shared-kept"><h3>Kept private</h3>${rules||recs||hand?`<ul class="list shared-list">${rules}${recs}${hand}</ul>`:'<p class="muted">Nothing yet. Tap Team or Only you on any thread in the Graph.</p>'}</div>`;
 const ST={sharing:'Sharing',not_started:'Not shared yet',off:'Stopped, with an admin\'s OK',removed:'Taken out'};
 if(g?.admin)h+=`<div class="fleet-box shared-people"><h3>Teammates</h3><p class="sub">Who shares with ${esc(work.name)}. Only an admin sees this.</p>${(g.people||[]).length?`<ul class="list shared-list">${g.people.map(p=>`<li class="shared-row"><span class="grow"><span class="ell">${esc(p.name)}</span><small class="muted">${ST[p.state]||''}</small></span>${p.state==='removed'?`<button type="button" class="ghost" data-graph-remove="${esc(p.member)}" data-back="1">Share again</button>`:`<button type="button" class="ghost" data-graph-remove="${esc(p.member)}">Take out</button>`}</li>`).join('')}</ul>`:''}</div>`;
 return h}
// Share these?: what the review was unsure of, in groups of the same kind (shared_graph.unsure_groups), each with the
// choice the review suggests first. One tap decides a group; open it to leave threads out and choose for them later.
// Share with team goes to everyone in the Fleet; Share with… only to the teammates picked (sensitive ones too).
const SHARE_PICK={team:'Share with team',people:'Share with…',private:'Keep private'},sharedGroupOpen=new Set();  // groups the owner opened stay open through a reload
document.addEventListener('toggle',e=>{const d=e.target;if(d?.classList?.contains('shared-group-list')){const k=d.closest('.shared-group')?.dataset.sharedGroup??'';d.open?sharedGroupOpen.add(k):sharedGroupOpen.delete(k)}},true);
function sharedAskHTML(d){const who=(d.teammates||[]).length,groups=d.groups?.length?d.groups:[{name:'',suggest:null,count:d.unsure.length}];
 return `<div class="fleet-box shared-ask"><h3>Share these?</h3><p class="sub">Not sure these are client work. They stay with you until you choose.</p><p class="fleet-fine muted">Share with team goes to everyone in the Fleet. Share with… goes only to the teammates you pick.</p>${groups.map(g=>{
  const rows=d.unsure.filter(x=>(x.group||'')===g.name);if(!rows.length)return '';
  const order=[...(g.suggest?[g.suggest]:[]),...['team','people','private'].filter(k=>k!==g.suggest)].filter(k=>k!=='people'||who);
  return `<section class="shared-group" data-shared-group="${esc(g.name)}"><div class="shared-group-head"><strong class="ell">${esc(g.name||t('Other threads'))}</strong><span class="count">${Number(g.count).toLocaleString(DL)}</span></div>${g.suggest?`<small class="muted shared-suggest">${esc(t('Suggested: {}',t(SHARE_PICK[g.suggest])))}</small>`:''}<div class="actions">${order.map(k=>`<button type="button" class="${k===g.suggest?'primary':'ghost'}" data-shared-many="${k}">${esc(t(SHARE_PICK[k]))}</button>`).join('')}</div><details class="shared-group-list"${sharedGroupOpen.has(g.name)?' open':''}><summary>${esc(t(['Show {} thread','Show {} threads'],rows.length))}</summary><ul class="list shared-list">${rows.map(x=>`<li class="shared-row shared-pick"><input type="checkbox" checked value="${esc(x.event_id)}" data-shared-pick aria-label="${esc(x.title||'(no subject)')}"><span class="grow">${sharedTitle(x)}<small class="muted">${esc([x.company||x.with,shortDay(x.at)].filter(Boolean).join(' · '))}</small></span></li>`).join('')}</ul></details></section>`}).join('')}</div>`}
// Share with… for the picked threads of one group: the teammates chosen get them, nobody else on the team.
function sharedPeopleOpen(fleet,ids){const people=sharedData[fleet]?.teammates||[];
 spOpen({title:t(['Share {} thread with…','Share {} threads with…'],ids.length),action:'graph_share_many',args:{event_ids:ids,share:'people'},chosen:[],people,
  line:who=>t('Goes to {} only, also if sensitive. Not to the rest of the team.',who),
  done:who=>t(['Shared {} thread with {} only.','Shared {} threads with {} only.'],ids.length,who),after:()=>sharedLoad(fleet,true)})}
async function sharedLoad(fleet,quiet){const el=$('#fleet-view').querySelector(`[data-shared-fleet="${CSS.escape(fleet)}"]`);if(!el)return;
 const work=(fleetData?.fleets||[]).find(x=>x.id===fleet),g=(fleetData?.shared?.graph||[]).find(s=>s.fleet===fleet);
 const paint=()=>{el.innerHTML=sharedHTML(work,g,sharedData[fleet])};
 if(sharedData[fleet]&&quiet)paint();
 try{sharedData[fleet]=await request('api/graph?view=shared&fleet='+encodeURIComponent(fleet));paint()}catch(err){errCaught(err);el.innerHTML=`<p class="error">${esc(err.message)}</p>`}}
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
   asks.forEach(x=>x.hidden=true);if(row)row.outerHTML=graphSendingLine(n);
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
function sharePopAt(anchor,html){sharePopClose();const p=document.createElement('div');p.id='share-pop';p.className='share-pop';p.setAttribute('role','dialog');p.setAttribute('aria-label','Sharing');p.innerHTML=html;document.body.append(p);
 const r=anchor?.getBoundingClientRect?.();if(r&&r.width){const w=Math.min(300,innerWidth-32);p.style.width=w+'px';p.style.left=Math.max(16,Math.min(r.right-w,innerWidth-w-16))+'px';const below=r.bottom+6+p.offsetHeight<innerHeight;p.style.top=(below?r.bottom+6:Math.max(16,r.top-6-p.offsetHeight))+'px'}else p.classList.add('floating');
 p.querySelector('button')?.focus();return p}
function sharePop(chip){const s=JSON.parse(chip.dataset.share||'{}'),on=graphSharing.find(x=>x.confirmed),fleet=on?.fleet,before=on?.started===false;const team=s.share==='team';
 sharePopAt(chip,`<p class="share-pop-why">${esc(s.why||(team?'Shared with your team':'Only you'))}</p>${s.people?.length?`<p class="share-pop-why">Shared with ${esc(namesLine(s.people))}</p>`:''}${s.fixed?'':`<div class="actions"><button type="button" class="${team?'ghost':'primary'}" data-pop-set="${esc(chip.dataset.shareEvent)}" data-share="${team?'only_you':'team'}"${before?' data-before="1"':''}>${team?(before?'Keep private':'Unshare'):'Share with the team'}</button>${!team&&graphTeammates.length?`<button type="button" class="ghost" data-pop-people="${esc(chip.dataset.shareEvent)}">Share with…</button>`:''}</div>`}${team&&!s.fixed&&!before?'<p class="fleet-fine muted">Unsharing deletes teammates\' copies. Someone may have read it already.</p>':''}${fleet?`<p class="fleet-fine"><a href="#shared=${esc(fleet)}">See what's shared</a></p>`:''}`)}
function sharePopSuggest(anchor,sug){const priv=sug.choice==='private';
 sharePopAt(anchor||$('#toast'),`<p>${priv?`Always keep threads with ${esc(sug.name)} private?`:`Always share client threads with ${esc(sug.name)}?`}</p><div class="actions"><button type="button" class="primary" data-pop-rule="${esc(sug.key)}" data-name="${esc(sug.name)}" data-choice="${priv?'private':'team'}">Yes</button><button type="button" class="ghost" data-pop-close>No</button></div>`)}
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
  return`<li class="fleet-ho${r.href?' tap':''}${r.st[2]?' quiet':''}${more?' fleet-ho-more':''}"${more?' hidden':''}${r.href?` tabindex="0" role="link" aria-label="${esc(t('{}: open the to-do',r.who))}" data-ho-go="${esc(r.href)}"`:''}><div class="fleet-ho-top"><strong>${esc(r.who)}</strong>${chip(r.st[0],r.st[1])}</div><p class="fleet-ho-sum" title="${esc(text)}">${time(r.at,true)} · ${esc(text)}</p></li>`};
 return`<div class="fleet-box fleet-handoffs"><h3>Handoffs</h3><ul class="fleet-ho-list">${open.map(row).join('')}${quiet.map(row).join('')}</ul>${quiet.length>shown?`<button type="button" class="quiet fleet-brief-show" data-ho-more>Show ${quiet.length-shown} more</button>`:''}</div>`}
function fleetIntroOffers(f,work,inFleet){const offers=(f.intro_offers||[]).filter(o=>inFleet(o,work));
 return offers.length?`<div class="list">${offers.map(o=>`<article><p>${t('{} knows someone at {}.',`<strong>${esc(o.name)}</strong>`,esc(o.about))}</p><form class="fleet-ask fleet-intro-form" data-fleet="${esc(o.fleet)}" data-member="${esc(o.member_id)}" data-about="${esc(o.about)}"><input name="note" maxlength="300" placeholder="Why, in a line (optional; they see it)" aria-label="Why"><button class="primary">Ask ${esc(o.name)} for an intro</button></form></article>`).join('')}</div>`:''}
// Back from a check-in while a teammate still has it: no Do it (that would prepare it all over again); Mark done leads
const withTeammate=s=>!closed(s)&&s.status!=='snoozed'&&!s.handled_hint&&['asked','waiting for them'].includes(s.fleet_handoff?.stage)&&!redirect(s);
// A new handoff text on a card a teammate still has (the owner asked to hand it to someone else): it waits for their review.
const redirect=s=>!closed(s)&&s.status!=='snoozed'&&['asked','waiting for them'].includes(s.fleet_handoff?.stage)&&taskActions(s).some(a=>a.kind==='handoff');
const firstName=n=>String(n||'').split(' ')[0];
// A handoff that didn't go out to "Pat’s Machine" (Pat Lee): said with a first name, like the chat's lines
const handoffMachine=n=>n&&n!=='A teammate'?t('{}’s Machine',String(n).split(' ')[0]):t('a teammate’s Machine');
const handoffFailed=s=>s.fleet_handoff_failed&&!s.fleet_handoff&&!closed(s)?`<p class="note fleet handoff-failed" role="alert">${esc(t('Handoff didn’t go out to {}',handoffMachine(s.fleet_handoff_failed.name)))} · <button type="button" class="link" data-fleet-handoff="${esc(s.id)}">Try again</button></p>`:'';
// Their Machine can't notify them (no phone, Telegram or email on): said under the handoff while it waits on them
const noPing=s=>s.fleet_handoff?.no_ping&&!closed(s)?`<p class="note fleet no-ping" role="status">${esc(t('{} won’t get a ping. Let them know.',firstName(s.fleet_handoff.name)))}</p>`:'';
function fleetHandoff(s){const contact=s.handoff_contact?`<p class="note handoff-contact">${esc(t('Contact: {}',s.handoff_contact))}</p>`:'';
 if(handoffFailed(s))return contact+handoffFailed(s);
 if(s.handoff_silent&&!s.fleet_handoff&&!closed(s))return contact+`<p class="note fleet silent-note">${esc(s.handoff_silent.line)} · <button type="button" class="link" data-handoff-not-mine="${esc(s.id)}">Not mine</button></p>`;  // theirs by what they did; one tap undoes it
 if(s.handoff_mail&&!s.fleet_handoff)return contact+mailHandoff(s);
 if(contact&&!s.fleet_handoff)return contact;
 if(s.fleet_handoff)return`<p class="note${s.fleet_handoff.back?'':' handled'} fleet">${handoffLine(s.fleet_handoff,s)}</p>${noPing(s)}${s.handoff_wait&&s.snoozed_until?`<p class="checkin-line" title="${esc(date(s.snoozed_until))}">${esc(checkinLabel(s))}</p>`:''}`;  // also once it is done
 if(closed(s)||!state?.fleet?.on||s.scope!=='work')return'';
 if(s.fleet_handoff)return`<p class="note handled fleet">${esc(t('Handed off to {}: {}',s.fleet_handoff.name,t(s.fleet_handoff.stage)))}</p>`;
 return''}  // the Hand off button sits with the card's other buttons (cardActions); its form with the other editors
// Hand off to a teammate: the same calm sheet as Hand to Codex / Claude Code (.agent-sheet). Who, then what they are
// asked to do as editable lead text, what goes along as chips with a quiet ×, an optional note.
function handoffEditor(s){const d=handingOff.get(s.id);if(!d||closed(s))return'';const id=esc(s.id),mail=d.to==='email';
 const opts=[...d.who.map(([f,m,n])=>[f+'|'+m,n]),['email','By email']];
 const pick=opts.length<=4?`<span class="agent-switch" role="radiogroup" aria-label="Hand off to">${opts.map(([v,n])=>`<label><input type="radio" name="to" value="${esc(v)}"${d.to===v?' checked':''}><span>${esc(n)}</span></label>`).join('')}</span>`
  :`<select name="to" class="handoff-pick" aria-label="Hand off to">${opts.map(([v,n])=>`<option value="${esc(v)}"${d.to===v?' selected':''}>${esc(n)}</option>`).join('')}</select>`;
 const name=mail?t('them'):esc((d.who.find(([f,m])=>f+'|'+m===d.to)||[])[2]||t('them'));
 const x=(what,attr)=>`<button type="button" class="chip-x" ${attr} aria-label="Leave out ${esc(what)}" title="Leave out">×</button>`;
 const chips=mail?'':[...(d.contact&&d.with_contact!==false?[`<span class="agent-get"><i class="via-ico via-link" aria-hidden="true"></i>${esc(t('Contact: {}',d.contact))}${x(d.contact,'data-handoff-drop="contact"')}</span>`]:[]),
  ...(d.sources||[]).map((v,n)=>d.dropped?.includes(n)?'':`<span class="agent-get"><i class="via-ico via-${v.kind==='email'?'mail':'chat'}" aria-hidden="true"></i>${esc(v.label)}${x(v.label,`data-handoff-drop="${n}"`)}</span>`)].join('');
 const had=!mail&&['asked','waiting for them'].includes(s.fleet_handoff?.stage)&&(d.who.find(([f,m])=>f+'|'+m===d.to)||[])[2]!==s.fleet_handoff.name?[firstName(s.fleet_handoff.name),...(s.fleet_handoff.also||[])].join(' and '):'';
 const back=had?`<label class="handoff-back"><input type="checkbox" name="replace"${d.replace===false?'':' checked'}> Take it back from ${esc(had)}</label>`:'';
 return`<form class="fleet-handoff-form agent-sheet" data-card="${id}"><div class="agent-sheet-head"><span class="agent-sheet-title">Hand off to</span>${pick}</div><input type="hidden" name="title" value="${esc(d.title)}">
 ${mail?`<input name="email" type="email" class="handoff-email" maxlength="254" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="handoff-team-${id}" value="${esc(d.email||'')}" placeholder="Their email" aria-label="Their email" required><ul class="cal-sug handoff-sug" id="handoff-team-${id}" role="listbox" aria-label="Teammates" hidden></ul>`:''}
 <textarea name="task" class="agent-note handoff-task" rows="1" maxlength="1000" aria-label="What they are asked to do">${esc(d.task??d.summary)}</textarea>${!mail&&chips?`<div class="agent-gets" aria-label="Goes along">${chips}</div>`:''}
 <textarea name="note" class="agent-note" rows="1" maxlength="600" placeholder="${esc(t('Add a note for {}',name))}" aria-label="${esc(t('Add a note for {}',name))}">${esc(d.note||'')}</textarea>${mail?mailParts(d):''}${back}
 <div class="agent-sheet-foot"><button type="button" class="ghost" data-handoff-cancel="${id}">Cancel</button><button class="primary">${mail?'Prepare email':'Hand off'}</button></div></form>`}
// By email: what goes in the email (handoff_mail.parts), each ticked until the owner unticks it. Only what the Team Graph
// shares with the team is offered; the email then waits on the to-do for the owner to read and send.
function mailParts(d){const p=d.parts,off=d.off||new Set();if(!p)return`<p class="agent-what">${esc(t('You read it on the to-do before it goes.'))}</p>`;
 const row=(k,html)=>`<label class="handoff-part"><input type="checkbox" data-handoff-part="${esc(k)}"${off.has(k)?'':' checked'}><span>${html}</span></label>`;
 const ico=k=>`<i class="via-ico via-${k}" aria-hidden="true"></i>`;
 const rows=[...p.lines.map(x=>row(x.key,esc(x.key==='due'?t('Due {}',tpDay(x.due)):x.text))),...(p.draft?[row('draft',ico('mail')+esc(t('Draft ready to send: {}',p.draft.subject)))]:[]),
  ...p.links.map(x=>row(x.key,ico('link')+esc(x.title||x.url))),...p.files.map(x=>row(x.key,ico('file')+esc(x.name))),row('take',esc(t('Take this on in your own Machine')))];
 return`<fieldset class="handoff-parts"><legend>${esc(t('Goes in the email'))}</legend>${rows.join('')}</fieldset>${p.shared?'':`<p class="agent-what">${esc(t('Personal and Only you content stays out.'))}</p>`}<p class="agent-what">${esc(t('You read it on the to-do before it goes.'))}</p>`}
// On the to-do once it went out: who has it, and the promise to track until it's done.
function mailHandoff(s){const m=s.handoff_mail;if(!m)return'';const first=firstName(m.name),led=s.task_page?.lead&&s.task_page.state!=='offered';
 return`${led?'':`<p class="note handled fleet">${esc(t('Handed to {} by email',m.name))}</p>`}${m.promise?`<p class="checkin-line handoff-promise">${esc(m.promise==='kept'?t('{} took this on',first):t('{} takes this on',first))}</p>`:''}`}
// Hand off by email: teammates at the owner's company first (api/invitees team: the Graph's people on its domains,
// then what is typed completed with each domain).
{let timer=0,seq=0;const sugOf=t=>t.parentElement?.querySelector('.handoff-sug'),hide=t=>{const l=sugOf(t);if(l){l.hidden=true;l.innerHTML=''}t.setAttribute('aria-expanded','false')};
 document.addEventListener('input',e=>{const t=e.target;if(!t.matches?.('.handoff-email'))return;const list=sugOf(t),q=t.value.trim();clearTimeout(timer);const n=++seq;if(!list)return;if(q.length<2){hide(t);return}
  timer=setTimeout(async()=>{let found=[];try{found=(await request('api/invitees?team=1&q='+encodeURIComponent(q))).people||[]}catch{}if(n!==seq)return;found=found.filter(p=>p.email!==q.toLowerCase());
   list.innerHTML=found.map(p=>`<li><button type="button" role="option" tabindex="-1" data-team-email="${esc(p.email)}" data-team-name="${esc(p.name||'')}">${p.name?`<span>${esc(p.name)}</span><small>${esc(p.email)}</small>`:`<span>${esc(p.email)}</span>`}</button></li>`).join('');
   list.hidden=!found.length;t.setAttribute('aria-expanded',String(!!found.length))},250)});
 document.addEventListener('pointerdown',e=>{if(e.target.closest?.('.handoff-sug'))e.preventDefault()});
 document.addEventListener('click',e=>{const b=e.target.closest?.('[data-team-email]');if(!b)return;const t=b.closest('form')?.querySelector('.handoff-email');if(!t)return;seq++;t.value=b.dataset.teamEmail;hide(t);t.focus();
  const d=handingOff.get(t.form?.dataset.card);if(d)Object.assign(d,{email:t.value,picked:{email:t.value,name:b.dataset.teamName||''}})});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&e.target.matches?.('.handoff-email')&&!sugOf(e.target)?.hidden){e.preventDefault();e.stopPropagation();seq++;hide(e.target)}},true);
 document.addEventListener('focusout',e=>{const t=e.target;if(t.matches?.('.handoff-email'))setTimeout(()=>{if(document.activeElement!==t){seq++;hide(t)}},200)})}
// Hand to Claude Code / Hand to Codex (agent_jobs.py): the owner reads and edits the brief; the card then follows the job:
// Sent, Running (or Waiting for their computer), a Result to mark done, ask changes on or hand off again, or Failed.
const agentEditing=new Map(),agentAsking=new Set(),AGENT_ACTIVE=['sent','running','waiting'];
const agentTools=()=>state?.agent_tools||[];
const agentWhere=x=>x.place==='device'?t('Runs on {}, with the Codex signed in there.',x.device):agentWhereElse(x);
const agentWhereElse=x=>x.place==='cloud'?t('Runs in Codex cloud, not on your computer.'):x.place==='remote'?t('Runs in your Claude session on {}.',x.device):t('Runs on this computer with your own {} setup.',x.name);
const canAgent=s=>!closed(s)&&s.status!=='snoozed'&&agentTools().length>0&&!AGENT_ACTIVE.includes(s.agent_job?.status)&&!agentOpen(s);
const agentOpen=s=>{const j=s.agent_job;return!!j&&!closed(s)&&!j.outcome&&['result','failed'].includes(j.status)};
const agentCancel=j=>`<div class="actions"><button class="ghost" data-agent-cancel="${esc(j.id)}">Cancel</button></div>`;
// A Codex thread opens on this computer: from the owner's other devices through the Codex app's remote connection (hostId).
const onMachine=()=>['localhost','127.0.0.1','[::1]','::1'].includes(location.hostname);
const agentHref=j=>j.url_elsewhere&&/^codex:\/\/threads\/[0-9a-f-]{36}\?hostId=/.test(j.url_elsewhere)&&!onMachine()?j.url_elsewhere:j.url;
// Its label is built in the owner's language here (translate="no": the page doesn't read it again). While The Machine's
// own Codex runs the turn the Codex app can't open the thread yet (it says it can't find it): the link says so instead.
const agentApp=j=>j.app_name?t('Open in {}',j.app_name):t('Open');
const AGENT_LATER='Codex is still on it here. It opens in the Codex app when it’s done.';
const agentLink=j=>j.url&&/^(https:\/\/|codex:\/\/threads\/)/.test(j.url)?`<a class="agent-app" href="${esc(agentHref(j))}" target="_blank" rel="noreferrer" translate="no" aria-label="${esc(agentApp(j))}"${j.opens_later?` data-later title="${esc(t(AGENT_LATER))}"`:''}><span class="agent-app-long">${esc(agentApp(j))}</span><span class="agent-app-short">${esc(t('Open'))}</span> ↗</a>`:'';
document.addEventListener('click',e=>{if(e.target.closest?.('a.agent-app[data-later]')){e.preventDefault();toast(t(AGENT_LATER))}});
// A result's header keeps one row: when "Open in Codex" no longer fits next to the tool's name it reads "Open" (the
// name is already on the left). Measured per header as its width changes, not at a fixed screen width.
// A wider header tries the long label again; any other change (a late font, new text) only ever shortens it, so it can't flip back and forth.
const agentHeadWraps=h=>{const a=h.querySelector('a.agent-app'),n=h.firstElementChild;return !!a&&a!==n&&a.getBoundingClientRect().top>=n.getBoundingClientRect().bottom-1};
function agentHeadSize(h,width){if(width!==undefined&&h._fitW!==width){h._fitW=width;h.classList.remove('tight')}if(!h.classList.contains('tight')&&agentHeadWraps(h))h.classList.add('tight')}
const agentHeadFit=new ResizeObserver(rows=>{for(const {target:h,contentRect:r} of rows)agentHeadSize(h,r.width)});
// A header drawn anew is fitted before it is painted, so a refresh never shows it wrapped first and then pulls the card up
new MutationObserver(()=>{for(const h of document.querySelectorAll('.agent-result .agent-head:not([data-fit])')){h.dataset.fit='';agentHeadSize(h);agentHeadFit.observe(h)}}).observe(document.body,{childList:true,subtree:true});
const agentHeadsFit=()=>{for(const h of document.querySelectorAll('.agent-result .agent-head[data-fit]'))agentHeadSize(h)};
document.fonts?.ready.then(agentHeadsFit);document.fonts?.addEventListener?.('loadingdone',agentHeadsFit);
// A job's follow-up goes to the same session: the card's Change asks the agent while its result is open.
const agentAsk=s=>agentOpen(s)&&s.agent_job.can_follow_up;
const agentFile=(j,f)=>`<a class="agent-file" href="api/agent-file?job=${encodeURIComponent(j.id)}&path=${encodeURIComponent(f.path)}" target="_blank" rel="noreferrer">${esc(f.path.split('/').pop())}</a>`;
// The agent's own words, as text: a link to one of its files is that file's chip, other local paths are just their name,
// markdown marks go. Never a path on this computer.
function agentText(j,text){const chips=[],files=j.files||[];
 const fileFor=t=>{const name=String(t).split(/[\\/]/).pop();return files.find(f=>f.path===t||f.path.split('/').pop()===name)};
 let t=String(text||'').replace(/\r/g,'').replace(/\[([^\]\n]+)\]\(([^)\s]+)\)/g,(m,label,target)=>{if(/^https?:/.test(target))return m;const f=fileFor(target);if(f){chips.push(agentFile(j,f));return '\u0002'+(chips.length-1)+'\u0003'}return label})
  .replace(/`([^`\n]+)`/g,'$1').replace(/^#{1,6}\s+/gm,'').replace(/^\s*[*-]\s+/gm,'• ')
  .replace(/(^|[\s(])(?:~|\/(?:home|Users|tmp|var|root|data|mnt|opt|srv))(?:\/[^\s/)]+)*\/([^\s/)]+)/g,'$1$2');
 return t.trim().split(/\n\s*\n/).filter(Boolean).map(p=>`<p>${format(p).replace(/\n/g,'<br>')}</p>`).join('').replace(/\u0002(\d+)\u0003/g,(m,i)=>chips[i])}
// Which of a job's files to show as chips: the ones its answer names, else what it made for the owner. Housekeeping
// (.pid, .log, lock and scratch files, dot folders) only shows under Details. At most AGENT_CHIPS, then "+N more".
const AGENT_CHIPS=3,AGENT_NOISE=/(^|\/)(\.[^/]*|node_modules|__pycache__|tmp|temp|scratch|cache|logs?)(\/|$)|\.(pid|log|lock|tmp|temp|swp|swo|bak|orig|out|err)$|~$/i;
function agentPick(paths,text){const said=String(text||''),named=paths.filter(f=>said.includes(f)||said.includes(f.split('/').pop()));
 const shown=(named.length?named:paths.filter(f=>!AGENT_NOISE.test(f))).slice(0,AGENT_CHIPS);return {shown,hidden:paths.length-shown.length}}
const agentMoreFiles=n=>n?`<button type="button" class="agent-file agent-morefiles" data-agent-files>+${n} more</button>`:'';
const agentAllFiles=(j,paths,label=true)=>`<div class="agent-allfiles">${label?'<p class="muted">All files</p>':''}<div class="agent-files">${paths.map(f=>agentFile(j,{path:f})).join('')}</div></div>`;
// The result in one line: its first paragraph, cut at a sentence when long. The rest folds behind Details.
function agentLine(text){const first=String(text||'').trim().split(/\n\s*\n/)[0]||'';if(first.length<=240)return first;const cut=first.slice(0,240),end=Math.max(cut.lastIndexOf('. '),cut.lastIndexOf('! '),cut.lastIndexOf('? '));return end>80?cut.slice(0,end+1):cut.replace(/\s+\S*$/,'')+'…'}
const agentTools2=(s,j,retry)=>`<div class="agent-tools">${retry?`<button data-agent-retry="${esc(j.id)}">Try again</button>`:''}<button data-agent-again="${esc(s.id)}">Hand off again</button><button data-agent-aside="${esc(j.id)}">Hide</button></div>`;
function agentBlock(s){const j=s.agent_job;if(!j||['set_aside','again'].includes(j.outcome)||(closed(s)&&j.status!=='result'))return'';
 const who=esc(j.name),cloud=j.place==='cloud',since=j.started_at||j.updated_at;
 if(j.status==='sent')return`<div class="agent-job"><p class="note">${t(cloud?'Sent to {} in Codex cloud. Starting soon.':'Sent to {}. Starting soon.',who)}</p>${agentCancel(j)}</div>`;
 if(j.status==='waiting')return`<div class="agent-job"><p class="note">${esc(t('Sent. Waiting for {}.',j.device||t('your computer')))} ${agentLink(j)}</p>${agentCancel(j)}</div>`;
 if(j.status==='running')return`<div class="agent-job"><p class="note">${t(cloud?'{} is working on it in Codex cloud':'{} is working on it',who)} · <span class="elapsed" data-since="${esc(since)}">${elapsed(since)}</span> ${agentLink(j)}</p>${j.progress?`<p class="muted agent-progress">${esc(j.progress)}</p>`:''}${agentCancel(j)}</div>`;
 if(j.status==='failed'&&j.error_kind==='busy')return`<div class="agent-job"><p class="note">${esc(j.error)} ${agentLink(j)}</p>${closed(s)?'':agentTools2(s,j,true)}</div>`;
 if(j.status==='failed')return`<div class="agent-job"><p class="note failed">${t('{} stopped: {}',who,`<span class="agent-error">${esc(j.error||t('it did not finish'))}</span>`)} ${agentLink(j)}</p>${closed(s)?'':agentTools2(s,j,true)}</div>`;
 if(j.status==='cancelled')return closed(s)?'':`<div class="agent-job"><p class="note">${t('{}: canceled.',who)}</p></div>`;
 const line=agentLine(j.summary),rest=String(j.summary||'').trim().length>line.length+2;
 const files=(j.files||[]).filter(f=>!(j.draft_updated&&f.path==='draft.md'));
 const lineHtml=agentText(j,line),own=files.filter(f=>!lineHtml.includes(agentFile(j,f))).map(f=>f.path);  // a file already in the line is not repeated
 const pick=agentPick(own,j.summary);
 const chips=pick.shown.length||pick.hidden?`<div class="agent-files">${pick.shown.map(f=>agentFile(j,{path:f})).join('')}${agentMoreFiles(pick.hidden)}</div>`:'';
 const diff=j.has_diff?`<details class="agent-diff" data-agent-diff="${esc(j.id)}"><summary>Show changes</summary><pre></pre></details>`:'';
 const more=rest||diff||pick.hidden?`<details class="agent-more"><summary>Details</summary>${rest?`<div class="agent-text">${agentText(j,j.summary)}</div>`:''}${pick.hidden?agentAllFiles(j,own):''}${diff}</details>`:'';
 return`<div class="agent-job draft agent-result" role="group" aria-label="${esc(t('{} result',j.name))}"><div class="agent-head"><span class="dm">${who}${j.place==='cloud'?' (Codex cloud)':''}${j.turns>1?' · '+t('after your changes'):''}</span>${agentLink(j)}</div><div class="agent-line agent-text">${lineHtml}</div>${j.draft_updated?`<p class="muted agent-progress">Updated the draft below. Send it when it reads right.</p>`:''}${chips}${more}${closed(s)?'':agentTools2(s,j,false)}</div>`}
// Hand to Codex / Claude Code: a compact sheet (in the chat it takes the message box's place). One plain line of what it
// will do, small chips for what it gets (never links), an optional note; the whole job only behind "See the full job".
const agentToolName=t=>t.place==='cloud'?t.name+' cloud':t.name;
const AGENT_GETS={mail:'mail',chat:'chat',draft:'note',file:'file',link:'link'};
function agentEditor(s){const d=agentEditing.get(s.id);if(!d||closed(s))return'';const t=agentTools().find(x=>x.id===d.tool)||agentTools()[0];if(!t)return'';
 const n=esc(agentToolName(t)),id=esc(s.id);
 const pick=agentTools().length>1?`<span class="agent-switch" role="radiogroup" aria-label="Hand to">${agentTools().map(x=>`<label title="${esc(agentWhere(x))}"><input type="radio" name="tool" value="${esc(x.id)}"${x.id===t.id?' checked':''}><span>${esc(agentToolName(x))}</span></label>`).join('')}</span>`
  :`<input type="hidden" name="tool" value="${esc(t.id)}"><span class="agent-one" title="${esc(agentWhere(t))}">${n}</span>`;
 const gets=(d.gets||[]).map(g=>`<span class="agent-get"><i class="via-ico via-${AGENT_GETS[g.kind]||'file'}" aria-hidden="true"></i>${esc(g.label)}</span>`).join('');
 return`<form class="agent-form agent-sheet" data-card="${id}"><div class="agent-sheet-head"><span class="agent-sheet-title">Hand to</span>${pick}</div>
 ${d.line?`<p class="agent-what">${esc(d.line)}</p>`:''}${gets?`<div class="agent-gets" aria-label="What it gets">${gets}</div>`:''}
 <textarea id="agent-note-${id}" name="note" class="agent-note" rows="1" maxlength="4000" placeholder="${esc(window.t('Add a note for {}',n))}" aria-label="${esc(window.t('Add a note for {}',n))}">${esc(d.note||'')}</textarea>
 <details class="agent-full" data-agent-full="${id}"${d.full?' open':''}><summary>See the full job</summary><textarea id="agent-brief-${id}" name="brief" maxlength="12000" spellcheck="false" aria-label="The full job">${esc(d.brief)}</textarea></details>
 <div class="agent-sheet-foot"><button type="button" class="ghost" data-agent-edit-cancel="${id}">Cancel</button><button class="primary">Hand off</button></div></form>`}
function agentAskEditor(s){if(!agentAsking.has(s.id)||!s.agent_job)return'';
 return`<div class="change-editor"><label for="agent-ask-${esc(s.id)}">What should ${esc(s.agent_job.name)} change? <small>Goes to the ${esc(s.agent_job.name)} job</small></label><textarea id="agent-ask-${esc(s.id)}" maxlength="4000" placeholder="Ctrl+Enter sends"></textarea><div class="actions"><button class="primary" data-agent-ask-send="${esc(s.id)}">Send</button><button class="ghost" data-agent-ask-cancel="${esc(s.id)}">Cancel</button></div></div>`}
const agentPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
async function agentHand(id,tool,b){if(b)b.disabled=true;try{const d=await agentPost('agent_draft',{suggestion_id:id});agentEditing.set(id,{tool,brief:d.brief,line:d.line,gets:d.gets,note:''});render();if(chatId)paintChat();document.getElementById('agent-note-'+id)?.focus()}catch(err){errCaught(err);toast(err.message,true)}finally{if(b)b.disabled=false}}
$('#suggestions').addEventListener('click',async e=>{const t=e.target;let b;
 if(b=t.closest('[data-agent-hand]'))return agentHand(b.dataset.card,b.dataset.agentHand,b);
 if(b=t.closest('[data-agent-files]')){const d=b.closest('.agent-job,.chat-msg')?.querySelector('details.agent-more');if(d){d.open=true;d.querySelector('.agent-allfiles')?.scrollIntoView({block:'nearest'})}return}
 if(b=t.closest('[data-agent-again]')){const s=state.suggestions.find(x=>x.id===b.dataset.agentAgain);return agentHand(b.dataset.agentAgain,s?.agent_job?.tool,b)}
 if(b=t.closest('[data-agent-edit-cancel]')){agentEditing.delete(b.dataset.agentEditCancel);render();if(chatId)$('#chat-input')?.focus();return}
 if(b=t.closest('[data-agent-ask]')){agentAsking.add(b.dataset.agentAsk);render();document.getElementById('agent-ask-'+b.dataset.agentAsk)?.focus();return}
 if(b=t.closest('[data-agent-ask-cancel]')){agentAsking.delete(b.dataset.agentAskCancel);render();return}
 if(b=t.closest('[data-agent-ask-send]'))return agentAskSend(b.dataset.agentAskSend,b);
 const act=[['agentCancel','agent_cancel','Canceled.'],['agentRetry','agent_retry','Sent again.'],['agentAside','agent_outcome','']].find(([k])=>t.closest(`[data-${k.replace(/[A-Z]/g,c=>'-'+c.toLowerCase())}]`));
 if(act){b=t.closest(`[data-${act[0].replace(/[A-Z]/g,c=>'-'+c.toLowerCase())}]`);b.disabled=true;try{await agentPost(act[1],{job_id:b.dataset[act[0]],...(act[1]==='agent_outcome'?{outcome:'set_aside'}:{})});if(act[2])toast(act[2]);await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}}});
async function agentAskSend(id,b){const s=state.suggestions.find(x=>x.id===id),box=document.getElementById('agent-ask-'+id);if(!s?.agent_job||!box?.value.trim())return;if(b)b.disabled=true;
 try{await agentPost('agent_follow_up',{job_id:s.agent_job.id,text:box.value.trim()});agentAsking.delete(id);box.value='';toast('Sent to '+s.agent_job.name+'.');await refresh()}catch(err){errCaught(err);if(b)b.disabled=false;toast(err.message,true)}}
$('#suggestions').addEventListener('keydown',e=>{const box=e.target.closest('textarea[id^="agent-ask-"]');if(box&&e.key==='Enter'&&(e.ctrlKey||e.metaKey)){e.preventDefault();agentAskSend(box.id.slice(10))}});
$('#suggestions').addEventListener('input',e=>{const f=e.target.closest('.agent-form');const d=f&&agentEditing.get(f.dataset.card);if(!d)return;
 if(e.target.name==='tool'){d.tool=e.target.value;const t=agentTools().find(x=>x.id===d.tool),n=t?agentToolName(t):'';const note=f.elements.note;note.placeholder=note.ariaLabel=window.t('Add a note for {}',n)}
 else if(e.target.name==='note')d.note=e.target.value;else d.brief=f.elements.brief.value});
$('#suggestions').addEventListener('toggle',e=>{const x=e.target;if(!x.matches?.('[data-agent-full]'))return;const d=agentEditing.get(x.dataset.agentFull);if(d)d.full=x.open},true);
$('#suggestions').addEventListener('submit',async e=>{const f=e.target;if(!f.classList.contains('agent-form'))return;e.preventDefault();const id=f.dataset.card,d=agentEditing.get(id),b=f.querySelector('button.primary');if(!d)return;b.disabled=true;
 try{const j=await agentPost('agent_send',{suggestion_id:id,tool:f.elements.tool?.value||d.tool,brief:f.elements.brief.value,note:f.elements.note?.value.trim()||''});agentEditing.delete(id);f.elements.brief.value='';toast('Sent to '+j.name+'.');await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#suggestions').addEventListener('toggle',async e=>{const d=e.target;if(!d.matches?.('[data-agent-diff]')||!d.open)return;const pre=d.querySelector('pre');if(pre.textContent)return;
 try{const r=await fetch('api/agent-diff?job='+encodeURIComponent(d.dataset.agentDiff),{credentials:'same-origin'});pre.textContent=r.ok?await r.text():'The changes are not available.'}catch{pre.textContent='The changes are not available.'}},true);
// While a job runs, follow it every few seconds with the small /api/agent-jobs, not the whole status.
setInterval(async()=>{if(document.hidden||!(state?.suggestions||[]).some(s=>AGENT_ACTIVE.includes(s.agent_job?.status)))return;
 try{const r=await request('api/agent-jobs');let changed=false,ended=false;for(const s of state.suggestions){const j=r.jobs?.[s.id];if(!j||JSON.stringify(j)===JSON.stringify(s.agent_job))continue;if(AGENT_ACTIVE.includes(s.agent_job?.status)&&!AGENT_ACTIVE.includes(j.status))ended=true;s.agent_job=j;changed=true}
 if(ended)await refresh();else if(changed&&!document.querySelector('#suggestions :is(textarea,select,input):focus'))render()}catch{}},4000);
// In a to-do's Details: the team learnings its draft followed, each with Remove (gone for the whole Fleet).
const teamLearningsUsed=s=>(s.team_learnings_used||[]).map(l=>`<p class="note fleet fleet-learn-used">${esc(t('Used a team learning: {}',String(l.text||'').replace(/<[^>]*>/g,'')))} <button type="button" class="link" data-fleet-learn-remove="${esc(l.fp)}" data-fleet="${esc(l.fleet)}">${esc(t('Remove'))}</button></p>`).join('');
function fleetNote(s){if(closed(s))return fleetHandoff(s);const h=s.fleet_holder;let out='';
 if(h?.offer)out+=`<p class="note fleet">${esc(h.offer.join(', '))} also got this email. <button type="button" class="link" data-fleet-take="${esc(s.id)}">Tell them you’re on it</button></p>`;
 else if(h?.name&&!h.mine)out+=`<p class="note handled fleet">${esc(h.name)} is on it. <button type="button" class="link" data-fleet-take="${esc(s.id)}">I’ll handle it</button></p>`;
 if(s.fleet_context?.length)out+=`<p class="note fleet">From your Fleet: ${s.fleet_context.map(esc).join(' · ')}</p>`;
 if(s.fleet_split)out+=`<p class="note fleet">Follow-ups split in your Fleet: ${esc(s.fleet_split)}</p>`;return out+fleetHandoff(s)}
// Fleet, Family and Friends members in the Graph, from what the Network directory already shows every member (graph.with_fleet).
const inGraph=p=>p?.graph_node?` <a href="#people" class="fp-graph" data-graph-open="${esc(p.graph_node)}" title="Open ${esc(p.label||p.name||'them')} in your Graph" aria-label="Open ${esc(p.label||p.name||'them')} in your Graph">Profile</a>`:'';  // their page in the owner's own Graph; the Team Graph is the box below
const fleetGroups=n=>[...new Set((n.fleet?.in||[]).map(x=>({work:'Fleet',family:'Family',friends:'Friend'})[x.kind]||x.label))].join(' · ');
const fleetLine=n=>[n.fleet?.machine?'Has a Machine':'',...(n.fleet?.in||[]).map(x=>x.kind==='work'&&x.fleet_name?`${x.label} (${x.fleet_name})`:x.label)].filter(Boolean).join(' · ');
const fleetChip=n=>n.fleet?`<span class="chip fleet-chip" style="--c:var(--mint)" title="${esc(fleetLine(n))}"><span class="ct">${esc(fleetGroups(n))}</span></span>`:'';
function fleetAskRow(n){if(!state?.fleet?.on||!['person','org'].includes(n.kind)||n.fleet?.in?.some(x=>x.kind==='work'))return'';const about=n.kind==='org'?(n.domain||n.name):/^email:/.test(n.id)?n.id.slice(6):n.name;
 return `<p class="graph-sub detail-fleet-ask"><button type="button" class="link" data-fleet-ask="${esc(about)}">Ask the Fleet who knows ${esc(n.name||about)}</button></p>`}
let fleetData=null,fleetShown=Promise.resolve(),fleetViewVersion=0,fleetPane=localStorage.getItem('fleet-pane')||'';
// The Fleet tab shows one view at a time; switching is instant (no reload) and remembered.
function showFleetPane(id){const view=$('#fleet-view');if(!view.querySelector(`[data-pane="${CSS.escape(id)}"]`))return;fleetPane=id;localStorage.setItem('fleet-pane',id);
 for(const b of view.querySelectorAll('[data-fleet-pane]'))b.setAttribute('aria-selected',b.dataset.fleetPane===id);
 for(const p of view.querySelectorAll('.fleet-pane'))p.hidden=p.dataset.pane!==id;
 if(/^shared-/.test(id))sharedLoad(id.slice(7),true)}
const fleetReveal=el=>{const p=el?.closest('.fleet-pane');if(p&&p.hidden)showFleetPane(p.dataset.pane)};
// #fleet=<question> from a phone notification or Telegram: the Fleet tab at that question; &choice= asks to confirm it.
function openFleetLink(){if(/^#fleet-brief=fl_[0-9a-f]{16}$/.test(location.hash))history.replaceState(null,'','#fleet');const m=/^#fleet(?:=((?:q|fn)_[a-f0-9]{16})(?:&choice=(once|decline))?)?$/.exec(location.hash);if(!m||!state.fleet?.on)return;
 history.replaceState(null,'',location.pathname+location.search);const card=/^q_/.test(m[1]||'');document.querySelector(`nav [data-tab="${card?'inbox':'fleet'}"]`).click();
 (card?fleetSync(true):fleetShown).then(()=>{const c=m[1]&&document.getElementById('fleet-'+m[1]);if(!c)return;fleetReveal(c);c.scrollIntoView({block:'center',behavior:'smooth'});c.classList.remove('flash');void c.offsetWidth;c.classList.add('flash');
  const w=m[2]&&fleetData?.waiting.find(x=>x.id===m[1]);if(w&&confirm(`${m[2]==='once'?'Share once':'Decline'}? ${w.name} asks: ${w.question}`))c.querySelector(`[data-choice-f="${m[2]}"]`)?.click()})}
async function fleetView(refresh=false,cached=false){const view=$('#fleet-view'),before=fleetSig(),version=++fleetViewVersion;if(!cached||!fleetData)try{const next=await request('api/fleet'+(refresh?'?refresh=1':''));if(version!==fleetViewVersion)return;fleetData=next;fleetAt=Date.now();if(state&&fleetSig()!==before)render()}catch(e){errCaught(e);if(version===fleetViewVersion){view._fleetHTML=null;view.innerHTML=`<p class="error">${esc(e.message)}</p>`}return}
 const f=fleetData;if(!f.on){view._fleetHTML=null;view.innerHTML=`<p class="muted">This Machine is not in a Fleet. Pair it with your account to join your team's. <a href="${HELP}fleet" target="_blank" rel="noopener">Learn more</a></p>`;return}
 // Several Work Fleets: each its own section, with its own people, rules and Ask; questions go to one Fleet at a time.
 const works=f.fleets.filter(x=>x.kind==='work'),family=f.fleets.find(x=>x.kind==='family'),several=works.length>1;
 const inFleet=(row,x)=>row.fleet===x.id||(!several&&row.fleet===x.kind),fleetName=row=>several?(works.find(x=>inFleet(row,x))?.name||''):'';
 // Who is who: each member with the Machine they answer with and their account email, so two people with one name stay apart.
 const who=x=>{const groups=[];for(const p of x.people||[]){const k=p.name+'|'+(p.email||''),g=groups.find(g=>g.k===k);g?g.list.push(p):groups.push({k,list:[p]})}  // one person with several Machines: the name once
  return groups.length?`<ul class="fleet-people">${groups.map(({list})=>{const p=list[0],tag=t=>`<span class="fp-tag">${t}</span>`,many=list.length>1;
   return `<li id="fleet-m-${esc(p.member_id||'')}"><div class="fp-name"><strong>${esc(p.name)}</strong>${list.some(m=>m.me)?tag('you'):''}${list.some(m=>m.role==='owner')?tag('owner'):''}${inGraph(list.find(m=>m.graph_node))}</div>`+
    (many?`<small class="fp-meta">${esc(p.email||'')}</small>${list.map(m=>`<small class="fp-meta fp-machine">${esc(m.answers_with||'')}${m.me?tag('this Machine'):''}</small>`).join('')}`
     :`<small class="fp-meta">${[p.email,p.answers_with].filter(Boolean).map(esc).join(' · ')}</small>`)+'</li>'}).join('')}</ul>`:''};
 const box=(title,sub,body,cls='')=>`<div class="fleet-box${cls?' '+cls:''}"><h3>${title}</h3>${sub?`<p class="sub">${sub}</p>`:''}${body}</div>`;
 const head=(x,count)=>`<div class="fleet-pane-head"><h2 class="ell">${esc(x.name)}</h2><span class="chip"><span class="ct">${esc(x.label)}</span></span>${count?`<span class="muted">${count} ${count===1?'person':'people'}</span>`:''}</div>`;
 const people=x=>box('People','',who(x)+(x.members.length||(x.people||[]).some(p=>!p.me)?'':'<p class="muted">Nobody else yet. Invite teammates from your account page.</p>'));
 // One view at a time: each Work Fleet, Friends, Family, Sharing (every rule in one place) and Activity, as pills.
 const panes=[];
 const notices=f.notices||[],asking=notices.filter(n=>n.buttons.length),told=notices.filter(n=>!n.buttons.length&&!/^friend_/.test(n.kind));
 const noticeCard=n=>`<article id="fleet-${esc(n.id)}"><p>${esc(n.text)}</p>${n.detail?`<p class="muted">${esc(n.detail)}</p>`:''}${n.outcome?`<p class="muted">→ ${esc(n.outcome)}</p>`:''}${n.reason?`<p class="note">${esc(n.reason)}</p>`:''}${n.buttons.length?`<div class="actions">${n.buttons.map(b=>`<button${b.choice==='confirm'?' class="primary"':''} data-fleet-notice="${esc(n.id)}" data-choice-n="${b.choice}" data-key="${esc(n.key)}">${esc(b.label)}</button>`).join('')}</div>`:''}<p><small class="mono">${esc(fmtDHM(n.at,{day:'numeric',month:'short'}))}</small></p></article>`;
 for(const work of works){const asked=f.asked.filter(a=>inFleet(a,work)&&a.kind!=='handoff');  // handoffs have their own box
  let h=`<div id="fleet-${esc(work.id)}">`+head(work,(work.people||[]).length)+people(work)+fleetShared(f,work);
  if(work.members.length){
   h+=box('Who knows someone?','Their Machines say how well they know someone there and when they last talked. Names only if they allow it.',
    `<form class="fleet-ask fleet-ask-form" data-fleet="${esc(work.id)}"><input name="about" maxlength="120" placeholder="Company, domain, email or name" aria-label="Who knows someone at"><button class="primary">Ask ${several?esc(work.name):'the Fleet'}</button></form>`+fleetIntroOffers(f,work,inFleet)
    +(asked.length?`<div class="list">${asked.map(a=>`<article><p><strong>${esc(a.name)}</strong> · ${esc(a.question)}</p><p class="muted">${esc(a.status==='answered'?a.answer:a.status==='waiting'?'Waiting for them to allow it':a.status==='asked'?(a.delivered===false?'Not delivered yet':'Asked'):a.status)}</p></article>`).join('')}</div>`:''));
   h+=fleetHandoffs(f,work,inFleet)+fleetBrief(f,work)+box('Ask anything','',fleetFree(f,work,several))+fleetLearnings(work)}
  else h+=fleetIntroOffers(f,work,inFleet);
  h+=fleetBriefAsks(f,work,inFleet);
  panes.push({id:'fleet-'+work.id,label:work.name,html:h+'</div>',at:work.joined_at});
  if((f.shared?.graph||[]).some(s=>s.fleet===work.id))panes.push({id:'shared-'+work.id,label:several?`What's shared · ${work.name}`:'What\'s shared',html:`<div class="shared-view" data-shared-fleet="${esc(work.id)}"><p class="muted">Loading…</p></div>`,at:work.joined_at})}
 if(family)panes.push({id:'family',label:family.name||'Family',html:head(family,(family.people||[]).length)+familySection(f,family),at:family.joined_at});
 // Every Fleet together, Work and Family, by when you joined or made it (the directory's order when it doesn't say); then Friends, Network, Sharing.
 const listed=p=>f.fleets.findIndex(x=>p.id.replace(/^shared-/,'fleet-')===(x.kind==='family'?'family':'fleet-'+x.id))+(/^shared-/.test(p.id)?.5:0);
 panes.sort((a,b)=>a.at&&b.at&&a.at!==b.at?(a.at<b.at?-1:1):listed(a)-listed(b));
 const fr=f.friends,friendsHtml=friendsSection(f,notices);
 if(friendsHtml)panes.push({id:'friends',label:'Friends',badge:(fr?.in||[]).length,html:friendsHtml});
 {const net=networkSection(f);if(net)panes.push({id:'network',label:'Network',html:net})}
 // Sharing: every rule in one place. What the three choices mean, once, at the top; per kind a plain question and an example.
 const friendsToo=!!fr&&(f.fleets.find(x=>x.id===fr.id)?.members||[]).length,rulesOf=works.filter(x=>x.members.length),familyToo=!!family&&family.members.length;
 if(rulesOf.length||friendsToo||familyToo){
  let h=`<dl class="fleet-legend" role="note">${[['Ask me first','You choose each time'],['Always','Answered by itself'],['Never','They get “no”'],['Names','Whether they hear who']].map(([t,d])=>`<div><dt>${t}</dt><dd>${d}</dd></div>`).join('')}</dl><p class="muted fleet-never">Never email content, never what your meetings are about. <a class="learn" href="${HELP}sharing-rules" target="_blank" rel="noopener">Learn more</a></p>`;
  for(const work of rulesOf)h+=fleetRules(work,f,several);
  h+=friendRules(f);
  if(familyToo)h+=fleetRules(family,f,true,'your family');
  h+=box('Meetings and brief','',`<label class="fleet-option"><input type="checkbox" id="fleet-meetings"${f.ask_meetings?' checked':''}><span>${esc(rulesOf.length?t(several?(friendsToo?'Ask my Work Fleets, and a friend who is in the meeting, about the outside people in my meetings this week':'Ask my Work Fleets about the outside people in my meetings this week'):(friendsToo?'Ask my Work Fleet, and a friend who is in the meeting, about the outside people in my meetings this week':'Ask my Work Fleet about the outside people in my meetings this week')):t('Ask a friend who is in one of my meetings this week about the other people in it'))}<small class="muted">They see those email addresses.</small></span></label>${rulesOf.length?fleetBriefSettings(f):''}`,'fleet-settings');
  panes.push({id:'sharing',label:'Sharing',html:h})}
 panes.push({id:'activity',label:'Activity',html:(told.length?box('Lately','Who joined, asked for a hosted Machine, had one started, or left.',`<div class="list">${told.map(noticeCard).join('')}</div>`):'')
  // What the Machine asked, answered and shared: Settings, Activity's list for the Fleet and learnings (settings-activity.js)
  +actEmbed()});
 const current=panes.some(p=>p.id===fleetPane)?fleetPane:panes[0].id;
 let html=f.off?pageNotice('The Network is off for now. Nothing is asked or answered.'):'';
 {const todo=fleetCardsOf(f).length;if(todo)html+=pageNotice(t(['One Fleet item waits for you under To-dos.','{} Fleet items wait for you under To-dos.'],todo),'Show',{'tab-go':'inbox'},'fleet-todo')}
 html+=`<div class="fleet-tabs" role="tablist" aria-label="Fleet">${panes.map(p=>`<button type="button" role="tab" data-fleet-pane="${esc(p.id)}" aria-selected="${p.id===current}"><span class="ell">${esc(p.label)}</span>${p.badge?` <span class="badge">${p.badge}</span>`:''}</button>`).join('')}</div>`;
 // A slot for suggested connections (people already on the Network you may know), filled by its own feature.
 html+='<div id="fleet-discover" class="fleet-discover"></div>';
 html+=panes.map(p=>`<div class="fleet-pane" role="tabpanel" data-pane="${esc(p.id)}"${p.id===current?'':' hidden'}>${p.html}</div>`).join('');
 // Leave unchanged forms in place: a completed background request must not swallow a click.
 if(view._fleetHTML===html){actEmbedFill();return}
 const drafts=[...view.querySelectorAll('form')].map(form=>({key:form.className+'|'+(form.dataset.fleet||''),values:[...form.elements].filter(e=>e.name&&['INPUT','TEXTAREA'].includes(e.tagName)).map(e=>[e.name,e.value])}));
 view.innerHTML=html;view._fleetHTML=html;actEmbedFill();
 if(/^shared-/.test(current))sharedLoad(current.slice(7),true);
 for(const draft of drafts){const form=[...view.querySelectorAll('form')].find(f=>f.className+'|'+(f.dataset.fleet||'')===draft.key);if(form)for(const [name,value]of draft.values){const input=form.elements.namedItem(name);if(input&&'value'in input)input.value=value}}
}
// Family (family.py): when everyone is free, to-dos for one another and plans to say yes or no to. Self-contained:
// its forms post family_free, family_todo and family_event; what waits for you is a card under Suggestions.
const FAMILY_REQ=['todo','event'];
const familyWhen=v=>{const d=new Date(String(v).length<=10?v+'T12:00':v);if(isNaN(d))return esc(v);return esc(String(v).length<=10?d.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'}):fmtDHM(d,{weekday:'short',day:'numeric',month:'short'}))};
// A datetime-local value with this browser's offset, so every Machine reads the same moment.
const familyMoment=v=>{if(!v)return '';const off=-new Date(v).getTimezoneOffset(),a=Math.abs(off);return `${v.slice(0,16)}${off<0?'-':'+'}${String(Math.floor(a/60)).padStart(2,'0')}:${String(a%60).padStart(2,'0')}`};
function familySection(f,family){const fam=f.family||{free:[],todos:[],plans:[],mine:[]},people=(family.people||[]).filter(p=>!p.me),today=new Date().toISOString().slice(0,10);
 const who=`<ul class="fleet-people">${(family.people||[]).map(p=>`<li id="fleet-m-${esc(p.member_id||'')}"><strong>${esc(p.label||p.name)}</strong>${p.me?' <span class="muted">(you)</span>':''}${inGraph(p)}<br><small class="muted">${esc(p.answers_with||'')}</small></li>`).join('')}</ul>`;
 if(!people.length)return `<div id="fleet-family" class="family">${who}<p class="muted">Nobody else yet. Invite your family from your account page.</p></div>`;
 const opts=people.map(p=>`<option value="${esc(p.member_id)}">${esc(p.name)}</option>`).join(''),latest=fam.free[0];
 const stage={accepted:'accepted',declined:'declined',done:'done',asked:'asked','waiting for them':'waiting'};
 let h=`<div id="fleet-family" class="family">${who}`;
 h+=`<div class="fleet-box family-free"><h3>When are we all free?</h3><form class="fleet-ask family-free-form"><input type="date" name="start" required value="${today}" aria-label="From"><select name="days" aria-label="For">${[1,2,3,7,14].map(d=>`<option value="${d}"${d===7?' selected':''}>${esc(t(['{} day','{} days'],d))}</option>`).join('')}</select><button class="primary">Ask everyone</button></form>`
  +(latest?`<p class="muted">${esc(t('{} of {} calendars',latest.answered+1,latest.asked+1))}${latest.waiting.length?' · '+esc(t('waiting for {}',latest.waiting.join(', '))):''}</p>${latest.slots.length?`<div class="family-slots">${latest.slots.map(s=>`<span class="chip">${esc(s.text)}</span>`).join('')}</div>`:'<p class="muted">No common free time, 8:00 to 21:00.</p>'}`:'<p class="muted">Shares busy times only, never what. Finds free hours between 8:00 and 21:00.</p>')+'</div>';
 h+=`<div class="fleet-box family-todos"><h3>To-dos</h3><form class="fleet-ask family-todo-form"><select name="member" aria-label="For">${opts}</select><input name="title" maxlength="120" required placeholder="${esc(t('Pick up the groceries'))}" aria-label="What"><input type="date" name="due" aria-label="Due (optional)"><button>Ask</button></form>`
  +((fam.mine||[]).length?`<p class="family-sub">Yours</p><ul class="family-list">${fam.mine.map(x=>`<li>${esc(x.title)} <small class="muted">· ${esc(t('from {}',x.name))}${x.due?' · '+familyWhen(x.due):''}${x.stage==='waiting'?' · '+esc(t('waits for you in To-dos')):''}</small></li>`).join('')}</ul>`:'')
  +(fam.todos.length?`<p class="family-sub">Asked</p><ul class="family-list">${fam.todos.map(x=>`<li>${esc(x.title)} <small class="muted">· ${esc(x.name)} · ${esc(t(stage[x.stage]||x.stage))}${x.due?' · '+familyWhen(x.due):''}</small></li>`).join('')}</ul>`:'')+'</div>';
 h+=`<div class="fleet-box family-plans"><h3>Plans</h3><form class="fleet-ask family-event-form"><input name="title" maxlength="120" required placeholder="${esc(t('Dinner at grandma’s'))}" aria-label="What"><input type="datetime-local" name="start" required aria-label="When"><input name="place" maxlength="120" placeholder="Where (optional)" aria-label="Where"><button>Propose to everyone</button></form>`
  +(fam.plans.length?`<ul class="family-list">${fam.plans.map(p=>`<li><strong>${esc(p.title)}</strong> <small class="muted">· ${familyWhen(p.start)}${p.place?' · '+esc(p.place):''}</small><br><small>${[p.yes.length?esc(t('In: {}',p.yes.join(', '))):'',p.no.length?esc(t('Can’t: {}',p.no.join(', '))):'',p.waiting.length?`<span class="muted">${esc(t('Waiting: {}',p.waiting.join(', ')))}</span>`:''].filter(Boolean).join(' · ')}</small> <a class="family-cal" href="${esc(p.link)}" target="_blank" rel="noopener">Add to my calendar</a></li>`).join('')}</ul>`:'<p class="muted">Each says yes or no on their Machine. Nothing is added to a calendar by itself.</p>')+'</div>';
 return h+'</div>'}
fleetOn('submit',async e=>{const t=e.target,act=t.classList.contains('family-free-form')?'family_free':t.classList.contains('family-todo-form')?'family_todo':t.classList.contains('family-event-form')?'family_event':'';if(!act)return;e.preventDefault();
 const v=n=>t.elements[n]?.value.trim()||'',args=act==='family_free'?{start:v('start'),days:Number(v('days'))}:act==='family_todo'?{member_id:v('member'),title:v('title'),due:v('due')}:{title:v('title'),start:familyMoment(v('start')),place:v('place')};
 try{await fleetPost(act,args);if(act!=='family_free')t.reset();toast({family_free:'Asked everyone. Free times show here as they answer.',family_todo:'Asked. It shows as accepted once they take it.',family_event:'Proposed. Yes and no show here.'}[act]);await fleetView()}catch(err){errCaught(err);toast(err.message,true)}});
// Friends (friends.py): add by username, requests both ways, your friends with the Machine they answer with, asking them,
// and your rules per friend (the same rule component as teammates). Friends see nothing of your Fleets.
const friendBtn=(label,attrs,cls='ghost',confirmText='')=>`<button type="button" class="${cls}" ${attrs}${confirmText?` data-confirm-text="${esc(confirmText)}"`:''}>${esc(label)}</button>`;
const friendBusy=a=>(a.busy||[]).length?a.busy.slice(0,12).map(([s,e])=>{return `${fmtDHM(s.replace('Z',':00Z'),{weekday:'short',day:'numeric',month:'short'})}–${fmtHM(e.replace('Z',':00Z'))}`}).join(' · ')+(a.busy.length>12?' · …':''):t('free the whole time');
// Your rules for friends: under Sharing with the Fleets' rules, the same component: one rule for all, exceptions per friend.
function friendRules(f){const fr=f.friends,group=fr&&f.fleets.find(x=>x.id===fr.id);if(!group||!(group.members||[]).length)return'';
 return fleetRules(group,f,true,t('your friends'))}
function friendsSection(f,notices){const fr=f.friends,group=fr&&f.fleets.find(x=>x.id===fr.id);if(!fr||!group)return'';
 const id=x=>esc(x),people=(group.people||[]).filter(p=>!p.me),asked=f.asked.filter(a=>a.fleet===fr.id);
 let h=`<div id="fleet-friends"><div class="fleet-pane-head"><h2>Friends</h2></div><p class="muted fleet-pane-sub">${fr.username?t('Your username: {}. Friends add you by it.',`<strong>${esc(fr.username)}</strong>`):esc(t('Choose your username on your account page first.'))} ${esc(t('They ask your Machine under your rules (Sharing) and see nothing of your Fleets.'))}</p>`;
 h+=`<div class="fleet-box"><h3>Add a friend</h3><form class="fleet-ask friend-add-form"><input name="username" maxlength="30" autocapitalize="none" autocomplete="off" spellcheck="false" placeholder="${esc(t('Their exact username'))}" aria-label="Their username"><button class="primary">Send friend request</button></form><p class="muted">Nothing connects until they accept.</p></div>`;
 if(fr.in.length)h+=`<div class="fleet-box"><h3>Waiting for you</h3><ul class="fleet-people">${fr.in.map(r=>`<li class="fp-row fp-wrap"><span class="fp-who">${t('{} wants to be friends.',`<strong>${esc(r.name)}</strong>`)}</span><span class="actions">${friendBtn('Accept',`data-friend-do="accept" data-friend-id="${id(r.id)}"`,'primary')}${friendBtn('Decline',`data-friend-do="decline" data-friend-id="${id(r.id)}"`)}${friendBtn('Block',`data-friend-do="block" data-friend-id="${id(r.id)}"`,'ghost','Block them? They are not told; their requests are dropped from now on.')}</span></li>`).join('')}</ul></div>`;
 if(fr.out.length)h+=`<div class="fleet-box"><h3>Your requests</h3><ul class="fleet-people">${fr.out.map(r=>`<li class="fp-row"><span class="fp-who"><strong>${esc(r.username)}</strong> <small class="muted">· ${esc(t('waiting'))}</small></span><span class="actions">${friendBtn('Withdraw',`data-friend-do="withdraw" data-friend-id="${id(r.id)}"`)}</span></li>`).join('')}</ul></div>`;
 if(people.length){h+=`<div class="fleet-box"><h3>Your friends</h3><ul class="fleet-people">${people.map(p=>`<li class="fp-row" id="fleet-m-${esc(p.member_id||'')}"><span class="fp-who"><strong>${esc(p.label||p.name)}</strong>${inGraph(p)}${p.answers_with?`<br><small class="muted">${esc(p.answers_with)}</small>`:''}</span><span class="actions">${friendBtn('Remove',`data-friend-do="remove" data-friend-member="${id(p.member_id)}"`,'ghost',t('Remove {}? Your Machines stop asking each other.',p.name))}${friendBtn('Block',`data-friend-do="block" data-friend-member="${id(p.member_id)}"`,'ghost',t('Block {}? They are not told; their requests are dropped from now on.',p.name))}</span></li>`).join('')}</ul></div>`;
  h+=`<div class="fleet-box friend-asks"><h3>Ask your friends</h3><h4 class="fleet-sub">Who knows someone there</h4><form class="fleet-ask fleet-ask-form" data-fleet="${esc(fr.id)}"><input name="about" maxlength="120" placeholder="Company, domain, email or name" aria-label="Ask your friends who knows someone at"><button class="primary">Ask your friends</button></form>`;
  h+=`<h4 class="fleet-sub">When they are busy</h4><form class="fleet-ask friend-avail-form"><label>Friend<select name="member">${people.map(p=>`<option value="${id(p.member_id)}">${esc(p.name)}</option>`).join('')}</select></label><label>From<input type="date" name="start" required value="${new Date().toISOString().slice(0,10)}"></label><label>For<select name="days">${[1,2,3,5,7,14].map(d=>`<option value="${d}"${d===3?' selected':''}>${esc(t(['{} day','{} days'],d))}</option>`).join('')}</select></label><button>Ask</button></form><p class="muted fleet-fine">They share busy times only, never what, under their rules for you.</p>`;
  h+=fleetIntroOffers(f,group,(row,x)=>row.fleet===x.id);
  if(asked.length)h+=`<div class="list">${asked.map(a=>`<article><p><strong>${esc(a.name)}</strong> · ${esc(a.question)}</p><p class="muted">${esc(a.status==='answered'?(a.kind==='availability'?t('Busy: {}',friendBusy(a)):a.answer):a.status==='waiting'?t('Waiting for them to allow it'):a.status==='asked'?t(a.delivered===false?'Not delivered yet':'Asked'):t(a.status))}</p></article>`).join('')}</div>`;
  h+='</div>'}
 else h+='<p class="muted">No friends yet.</p>';
 if(fr.blocked.length)h+=`<div class="fleet-box"><h3>Blocked</h3><div class="list">${fr.blocked.map(b=>`<article><p>${esc(b.name)}</p><div class="actions">${friendBtn('Unblock',`data-friend-do="unblock" data-friend-member="${id(b.member_id)}"`)}</div></article>`).join('')}</div></div>`;
 const lately=notices.filter(n=>/^friend_/.test(n.kind)&&!n.buttons.length).slice(0,5);
 if(lately.length)h+=`<div class="fleet-box"><h3>Lately</h3><ul class="list">${lately.map(n=>`<li>${esc(n.text)}${n.outcome?` <span class="muted">→ ${esc(n.outcome)}</span>`:''}</li>`).join('')}</ul></div>`;
 return h+'</div>'}
fleetOn('click',async e=>{const b=e.target.closest('[data-friend-do]');if(!b)return;if(b.dataset.confirmText&&!confirm(b.dataset.confirmText))return;b.disabled=true;
 try{await fleetPost('fleet_friend',{do:b.dataset.friendDo,id:b.dataset.friendId||'',member_id:b.dataset.friendMember||''});
  toast({accept:'You are friends now.',decline:'Declined. They are not told.',block:'Blocked.',withdraw:'Withdrawn.',remove:'Removed.',unblock:'Unblocked.'}[b.dataset.friendDo]||'Done.');await fleetView();await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
fleetOn('submit',async e=>{const t=e.target;if(t.classList.contains('friend-add-form')){e.preventDefault();const username=t.elements.username.value.trim();if(!username)return;
  try{await fleetPost('fleet_friend',{do:'add',username});t.reset();toast('Request sent. It waits until they accept.');await fleetView()}catch(err){errCaught(err);toast(err.message,true)}}
 else if(t.classList.contains('friend-avail-form')){e.preventDefault();
  try{await fleetPost('fleet_availability',{member_id:t.elements.member.value,start:t.elements.start.value,days:Number(t.elements.days.value)});toast('Asked. Their busy times show here.');await fleetView()}catch(err){errCaught(err);toast(err.message,true)}}});
fleetOn('click',async e=>{const b=e.target.closest('[data-net-do]');if(!b)return;if(b.dataset.confirmText&&!confirm(b.dataset.confirmText))return;b.disabled=true;
 try{await fleetPost('fleet_network',{do:b.dataset.netDo,email:b.dataset.netEmail||'',relation:b.dataset.netRel||''});
  toast({find_on:'On. Your Machine checks your contacts privately.',asked:'Okay. Turn it on any time in the Fleet tab.',connect:'Request sent. It waits until they accept.',later:'Hidden for now.',never:'Won’t suggest them again.',leave:'You left the Network.'}[b.dataset.netDo]||'Done.');await fleetView();await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
fleetOn('change',async e=>{const t=e.target.closest('[data-net-addr]');if(!t)return;t.disabled=true;
 try{await fleetPost('fleet_network',{do:t.checked?'address_on':'address_off',email:t.dataset.netAddr});await fleetView()}catch(err){errCaught(err);t.checked=!t.checked;toast(err.message,true)}finally{t.disabled=false}});
fleetOn('change',async e=>{const t=e.target.closest('[data-net-toggle]');if(!t)return;t.disabled=true;
 try{await fleetPost('fleet_network',{do:t.dataset.netToggle});await fleetView()}catch(err){errCaught(err);t.checked=!t.checked;toast(err.message,true)}finally{t.disabled=false}});
fleetOn('keydown',e=>{const go=(e.key==='Enter'||e.key===' ')&&e.target.matches?.('[data-ho-go]')&&e.target;if(go){e.preventDefault();location.hash=go.dataset.hoGo}});
fleetOn('click',async e=>{const more=e.target.closest('[data-brief-more]');if(more){more.closest('.fleet-brief').querySelectorAll('.fleet-brief-more').forEach(li=>li.hidden=false);more.remove();return}
 const hoMore=e.target.closest('[data-ho-more]');if(hoMore){hoMore.closest('.fleet-handoffs').querySelectorAll('.fleet-ho-more').forEach(li=>li.hidden=false);hoMore.remove();return}
 const hoGo=e.target.closest('[data-ho-go]');if(hoGo){location.hash=hoGo.dataset.hoGo;return}  // the whole row opens its card
 const ask=e.target.closest('[data-brief-ask]');if(ask){const input=document.querySelector(`.fleet-free-form[data-fleet="${CSS.escape(ask.dataset.fleet)}"] input[name=text]`);if(!input)return;input.value=ask.dataset.briefAsk;input.focus();input.scrollIntoView({block:'center',behavior:'smooth'});return}
 const hide=e.target.closest('[data-brief-hide]');if(!hide)return;hide.disabled=true;
 try{await fleetPost('fleet_brief_hide',{fleet:hide.dataset.fleet,key:hide.dataset.briefHide});hide.closest('li').remove();toast('Hidden from this brief.');await fleetView()}catch(err){errCaught(err);hide.disabled=false;toast(err.message,true)}});
fleetOn('submit',async e=>{if(!e.target.classList.contains('fleet-free-form'))return;e.preventDefault();const text=e.target.elements.text.value.trim();if(!text)return;
 try{await fleetPost('fleet_free',{text,fleet:e.target.dataset.fleet});e.target.reset();toast('Asked your Fleet. Answers show here as they come.');await fleetView()}catch(err){errCaught(err);toast(err.message,true)}});
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-send]');if(!b)return;const text=document.getElementById('fleet-free-'+b.dataset.fleetSend)?.value.trim();if(!text){toast('Write an answer first, or decline.',true);return}b.disabled=true;
 try{await fleetPost('fleet_decide',{id:b.dataset.fleetSend,choice:'once',text});toast('Sent.');await fleetView();await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
fleetOn('submit',async e=>{if(!e.target.classList.contains('fleet-ask-form'))return;e.preventDefault();const about=e.target.elements.about.value.trim();if(!about)return;
 try{await fleetPost('fleet_ask',{kind:'relationships',question:{about},fleet:e.target.dataset.fleet});e.target.reset();toast(/^fr_/.test(e.target.dataset.fleet||'')?'Asked your friends.':'Asked your Fleet.');await fleetView()}catch(err){errCaught(err);toast(err.message,true)}});
$('#fleet-view').addEventListener('click',e=>{const pane=e.target.closest('[data-fleet-pane]');if(pane){showFleetPane(pane.dataset.fleetPane);return}if(e.target.closest('[data-tab-go]'))document.querySelector('nav [data-tab="inbox"]').click()});
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-notice]');if(!b)return;b.disabled=true;
 try{const r=await fleetPost('fleet_notice_decide',{id:b.dataset.fleetNotice,choice:b.dataset.choiceN,key:b.dataset.key});
  const fr=/^friend/.test(fleetData?.notices?.find(n=>n.id===b.dataset.fleetNotice)?.kind||'');
  toast(r.status==='confirmed'?(fr?'Accepted. You are friends now.':'Confirmed. Their Machine is starting.'):r.status==='declined'?(fr?'Declined. They are not told.':'Declined. Nothing was started or charged.'):r.reason,r.status==='stale'||r.status==='changed');await fleetView();await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-learn-remove]');if(!b)return;b.disabled=true;  // gone for the whole Fleet, for good
 try{await fleetPost('fleet_learning_remove',{fleet:b.dataset.fleet,fp:b.dataset.fleetLearnRemove});toast(t('Removed for the whole team.'));if(b.closest('#suggestions'))await refresh();else await fleetView()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-ex-rule],[data-fleet-ex-clear]');if(!b)return;b.disabled=true;
 try{const member=b.dataset.fleetExClear||b.closest('.fleet-ex-pick').querySelector('[data-fleet-ex-member]').value;
  await fleetPost('fleet_rule',{fleet:b.dataset.fleet,member_id:member,kind:b.dataset.kind,...(b.dataset.fleetExClear?{clear:true}:{rule:b.dataset.fleetExRule})});toast(b.dataset.fleetExClear?'Back to the rule for everyone.':'Saved.');await fleetView()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
const fleetRedraw=()=>{render();if(!$('#fleet').hidden)fleetView(false,true)};
// Connect Stripe for the team (self-hosted): Connections, + Add, at its Sign in with Stripe. Shared from the Fleet tab after.
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-connect]');if(!b)return;connectRun=null;showTab('health','add');await connectAdd(true);
 const x=connectList?.sources.find(v=>v.service===b.dataset.fleetConnect);if(!x)return;
 if(x.signin){connectSignin={source:x.name,provider:x.signin===true?x.service:x.signin,label:SIGNIN_COPY.stripe.label,own:!x.broker,state:'intro',...(x.signin_off?{off:true}:{})};$('#connect-add').dataset.sig='';renderConnectSignin()}
 viewTop($('#connect-add'))});
fleetOn('click',async e=>{const p=e.target.closest('[data-fleet-pick]');if(p){const on=p.getAttribute('aria-pressed')!=='true';for(const r of p.parentElement.children)r.setAttribute('aria-pressed','false');p.setAttribute('aria-pressed',String(on));return}
 const o=e.target.closest('[data-fleet-noting],[data-fleet-note-cancel]');if(o){if(o.dataset.fleetNoting)fleetNoting.set(o.dataset.fleetNoting,'once');else fleetNoting.delete(o.dataset.fleetNoteCancel);fleetRedraw();return}
 const n=e.target.closest('[data-fleet-note-send]');if(!n)return;const box=n.closest('.fleet-note-editor'),id=n.dataset.fleetNoteSend;
 const note=[box?.querySelector('.reason[aria-pressed="true"]')?.dataset.fleetPick,(box?.querySelector('textarea')?.value||'').trim()].filter(Boolean).join(': ').slice(0,160);n.disabled=true;
 try{const r=await fleetPost('fleet_decide',{id,choice:n.dataset.choiceF,...(note?{note}:{})});fleetNoting.delete(id);toast((r.status==='answered'?'Accepted.':'Declined.')+(note?' They see your note.':''));await fleetView();await refresh()}catch(err){errCaught(err);n.disabled=false;toast(err.message,true)}});
fleetOn('click',async e=>{const o=e.target.closest('[data-graph-optout]');if(!o)return;const off=o.dataset.off==='1';o.disabled=true;  /* the Shared Graph: asking an admin to stop, or sharing again */
 try{const r=await fleetPost('graph_optout',{fleet:o.dataset.graphOptout,off});toast(off?(r.off==='off'?'Not shared now.':'Asked an admin.'):'Shared with the team again.');await fleetView()}catch(err){errCaught(err);o.disabled=false;toast(err.message,true)}});
fleetOn('click',e=>{const b=e.target.closest('[data-shared-read]');if(b)openEvent(b.dataset.sharedRead,b.textContent)});
fleetOn('click',async e=>{const b=e.target.closest('[data-share-ok],[data-share-stop]');if(!b)return;
 if(b.dataset.shareStop&&!confirm('Stop sharing it? Every teammate\'s Machine loses access to it.'))return;b.disabled=true;
 const member=b.dataset.kind==='member',card=member?b.closest('article'):null,label=b.textContent;if(member)b.textContent='Sharing…';
 try{if(b.dataset.shareStop){await fleetPost('fleet_share_stop',{fleet:b.dataset.fleet,service:b.dataset.shareStop});toast('Stopped sharing.')}
  else{const r=await fleetPost('fleet_share_ok',{id:b.dataset.shareOk,choice:b.dataset.choice});if(card)card.hidden=true;toast(r.done?(b.dataset.kind==='optout'?'Approved. Their Work stops going to the team.':'Done. Their Machine gets it next.'):'Okay.')}
  await fleetView();if(member)graphSendingWatch()}catch(err){errCaught(err);b.disabled=false;if(member)b.textContent=label;toast(err.message,true)}});
fleetOn('submit',async e=>{const t=e.target;if(!t.matches('.share-form,.share-replace'))return;e.preventDefault();const btn=t.querySelector('button.primary');btn.disabled=true;
 try{if(t.matches('.share-form')){const r=await fleetPost('fleet_share',{fleet:t.dataset.fleet,account:t.dataset.account,members:[...t.querySelectorAll('input[name=m]:checked:not(:disabled)')].map(i=>i.value)});toast(`Shared with ${r.shared_with} ${r.shared_with===1?'Machine':'Machines'}.`)}
  else{await fleetPost('fleet_share_replace',{fleet:t.dataset.fleet,service:t.dataset.service,token:t.elements.token.value.trim()});t.elements.token.value='';toast('Replaced. Teammates get the new one.')}
  await fleetView()}catch(err){errCaught(err);btn.disabled=false;toast(err.message,true)}});
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-decide]');if(!b)return;
 if(b.dataset.choiceF==='decline'&&FLEET_REQ.includes(fleetData?.waiting?.find(x=>x.id===b.dataset.fleetDecide)?.kind)){fleetNoting.set(b.dataset.fleetDecide,'decline');fleetRedraw();return}
 b.disabled=true;
 try{const r=await fleetPost('fleet_decide',{id:b.dataset.fleetDecide,choice:b.dataset.choiceF});toast(r.status==='answered'?'Answered.':'Declined.');await fleetView();await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
fleetOn('change',async e=>{const t=e.target;try{
 const b=t.closest('.fleet-rule');let res;
 if(t.dataset.fleetRule)res=await fleetPost('fleet_rule',{fleet:t.dataset.fleet,member_id:t.dataset.fleetRule,kind:t.dataset.kind,rule:t.value});
 else if(t.dataset.fleetDetails)res=await fleetPost('fleet_rule',{fleet:t.dataset.fleet,member_id:t.dataset.fleetDetails,kind:t.dataset.kind,details:t.value==='1'});
 else if(t.dataset.scope&&b)res=await fleetPost('fleet_rule',{fleet:b.dataset.fleet,member_id:b.dataset.member,kind:b.dataset.kind,scope:fleetScopeOf(b)});
 else if(t.id==='fleet-meetings')await fleetPost('fleet_meetings',{on:t.checked});else if(t.id==='fleet-brief-every')await fleetPost('fleet_brief',{every:t.value});else if(t.id==='fleet-brief-tell')await fleetPost('fleet_brief',{tell:t.checked});else if(t.dataset?.fleetBriefShare){await fleetPost('fleet_rule',{fleet:t.dataset.fleetBriefShare,member_id:'*',kind:'brief',rule:t.checked?'always':'never'});toast(t.checked?'Brief facts on.':'Brief facts off. Nothing goes to their briefs.');await fleetView();return}else return;res=res?.result||res;if(b&&res?.rule){const sc=b.querySelector('.fleet-scope')?res.scope:null;b.querySelector('.fleet-preview').textContent=fleetPreview(b.dataset.name,b.dataset.kind,res,sc,!!b.dataset.wide);if(b.dataset.wide&&t.dataset.fleetRule){await fleetView();return toast('Saved.')}
  if(sc){b.querySelector('.fleet-scope-now').textContent=fleetScopeText(sc)?' ('+fleetScopeText(sc)+')':'';if(t.dataset.scope&&t.type!=='checkbox')t.value=sc[t.dataset.scope].join(', ')}}toast('Saved.')}catch(err){errCaught(err);toast(err.message,true);await fleetView()}});
// Answers to your free questions show as they arrive, while the Fleet tab is open and you aren't typing in it.
setInterval(()=>{if(!$('#fleet').hidden&&!$('#fleet-view').contains(document.activeElement)&&(fleetData?.free||[]).some(q=>q.answers.some(x=>x.state==='waiting')))fleetView()},30000);
fleetOn('submit',async e=>{const t=e.target;if(t.classList.contains('fleet-intro-form')){e.preventDefault();
  try{await fleetPost('fleet_intro',{fleet:t.dataset.fleet,member_id:t.dataset.member,about:t.dataset.about,note:t.elements.note.value.trim()});toast('Asked. This tab shows how it goes.');await fleetView()}catch(err){errCaught(err);toast(err.message,true)}}
 else if(t.classList.contains('fleet-split-form')){e.preventDefault();const items={};for(const i of t.querySelectorAll('input'))items[i.name]=i.value.trim();
  try{await fleetPost('fleet_split',{id:t.dataset.split,items});toast('Sent. Each teammate sees their part.');await fleetView();await refresh()}catch(err){errCaught(err);toast(err.message,true)}}});
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-adjust],[data-split-dismiss]');if(!b)return;b.disabled=true;
 try{if(b.dataset.splitDismiss)await fleetPost('fleet_split_dismiss',{id:b.dataset.splitDismiss});
  else{const text=document.getElementById('fleet-part-'+b.dataset.fleetAdjust)?.value.trim();if(!text){b.disabled=false;toast('Write your part first.',true);return}
   await fleetPost('fleet_split_adjust',{id:b.dataset.fleetAdjust,text});toast('Accepted with your change.')}
  await fleetView();await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#suggestions').addEventListener('click',async e=>{const c=e.target.closest('[data-handoff-cancel]');if(c){handingOff.delete(c.dataset.handoffCancel);render();return}
 const drop=e.target.closest('[data-handoff-drop]'),dd=drop&&handingOff.get(drop.closest('form').dataset.card);
 if(dd){const v=drop.dataset.handoffDrop;if(v==='contact')dd.with_contact=false;else dd.dropped=[...(dd.dropped||[]),+v];render();return}
 const b=e.target.closest('[data-fleet-handoff]');if(!b)return;b.disabled=true;
 try{const [d,parts]=await Promise.all([fleetPost('fleet_handoff_draft',{suggestion_id:b.dataset.fleetHandoff}),fleetPost('fleet_handoff_email_parts',{suggestion_id:b.dataset.fleetHandoff}).catch(()=>null)]);const who=d.fleets.flatMap(x=>x.members.map(m=>[x.id,m.member_id,d.fleets.length>1?`${m.name} (${x.name})`:m.name]));
  const card=(state?.suggestions||[]).find(x=>x.id===d.suggestion_id),h=card?.fleet_handoff,has=h&&['asked','waiting for them'].includes(h.stage)?[firstName(h.name),...(h.also||[])]:[];
  const pickFirst=who.find(([,,n])=>!has.includes(firstName(n)))||who[0];  // handing it on: someone who doesn't have it yet
  handingOff.set(d.suggestion_id,{...d,who,parts,off:new Set(parts&&!parts.take?['take']:[]),to:pickFirst?pickFirst[0]+'|'+pickFirst[1]:'email'});render()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#suggestions').addEventListener('input',e=>{const t=e.target.closest('.fleet-handoff-form');const d=t&&handingOff.get(t.dataset.card);if(!d)return;
 const part=e.target.dataset?.handoffPart;if(part){d.off=d.off||new Set();e.target.checked?d.off.delete(part):d.off.add(part);return}
 const moved=d.to!==t.elements.to.value||(t.elements.replace&&d.replace!==t.elements.replace.checked);Object.assign(d,{to:t.elements.to.value,email:t.elements.email?t.elements.email.value:d.email,task:t.elements.task.value,note:t.elements.note.value,...(t.elements.replace?{replace:t.elements.replace.checked}:{})});if(moved)render()});
$('#suggestions').addEventListener('submit',async e=>{const t=e.target;if(!t.classList.contains('fleet-handoff-form'))return;e.preventDefault();const [fleet,member_id]=t.elements.to.value.split('|'),d=handingOff.get(t.dataset.card)||{};
 const parts=[t.elements.task.value.trim(),t.elements.note.value.trim()].filter(Boolean),summary=parts.map((x,n)=>n<parts.length-1&&!/[.!?…]$/.test(x)?x+'.':x).join(' ');  // as plain sentences
 if(t.elements.to.value==='email'){const p=d.parts,off=d.off||new Set(),keep=p?[...p.lines,...p.links,...p.files,...(p.draft?[p.draft]:[])].map(x=>x.key).filter(k=>!off.has(k)):null;
  try{await fleetPost('fleet_handoff_email',{suggestion_id:t.dataset.card,email:t.elements.email.value.trim(),title:t.elements.title.value.trim(),summary,...(p?{keep,take:!off.has('take')}:{}),...(d.picked?.email===t.elements.email.value.trim()&&d.picked.name?{name:d.picked.name}:{})});
  handingOff.delete(t.dataset.card);toast('Your email is ready on the to-do. Read it, then send it yourself.');await refresh()}catch(err){errCaught(err);toast(err.message,true)}return}
 try{await fleetPost('fleet_handoff',{suggestion_id:t.dataset.card,fleet,member_id,title:t.elements.title.value.trim(),summary,contact:d.contact&&d.with_contact!==false?d.contact:'',sources:(d.sources||[]).map((_,n)=>n).filter(n=>!d.dropped?.includes(n)),...(t.elements.replace?{replace:t.elements.replace.checked}:{})});
  handingOff.delete(t.dataset.card);toast('Handed off. The to-do shows how it goes.');await refresh()}catch(err){errCaught(err);toast(err.message,true)}});
// Settings > Fleet: the "Take this on in your own Machine" line in handoff emails (on by default)
$('#settings-take-line').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await fleetPost('fleet_handoff_take_line',{on});if(state.fleet)state.fleet.take_line=r.take_line;b.setAttribute('aria-checked',String(r.take_line));notice(r.take_line?'Handoff emails offer their own Machine.':'Handoff emails leave out their own Machine.')}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
