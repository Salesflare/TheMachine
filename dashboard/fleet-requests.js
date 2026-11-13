// Warm intros and handoffs (fleet_requests.py). A teammate's words are shown quoted, as data; accepting makes a
// card from this Machine's own data, and anything that card sends waits for the owner's own Send.
const FLEET_REQ=['intro','handoff'],handingOff=new Map(),fleetNoting=new Map();
// Decline (or Accept with a note) on a teammate's request: an optional short reason, with quick picks; only they see it.
const DECLINE_PICKS=['Not mine','Already done','No time this week'];
function fleetNoteEditor(w,c){const id=w.id,no=c==='decline';return html`<div class="change-editor dismiss-editor fleet-note-editor"><p class="dismiss-q" id="fleet-note-q-${id}">${no?'Why?':t('Note to {}',w.name)} <small>Optional</small></p>${no?html`<div class="reason-chips" role="group" aria-labelledby="fleet-note-q-${id}">${DECLINE_PICKS.map(r=>html`<button type="button" class="reason" aria-pressed="false" data-fleet-pick="${r}">${r}</button>`)}</div>`:''}<textarea id="fleet-note-${id}" rows="1" maxlength="160" aria-label="Note (optional)" placeholder="Add a note (optional)"></textarea><p class="muted">Only ${w.name} sees it.</p><div class="actions"><button class="primary" data-fleet-note-send="${id}" data-choice-f="${c}">${no?'Decline':'Accept'}</button><button type="button" class="ghost" data-fleet-note-cancel="${id}">Cancel</button></div></div>`}
// A handoff a teammate declined (or let expire): the card is back, with what to do now.
const handoffBackActions=s=>html`<div class="actions"><button class="primary" data-handoff-mine="${s.id}">Do it myself</button>${canHandoff(s)?html`<button class="ghost" data-fleet-handoff="${s.id}">Hand off to someone else</button>`:''}<button class="ghost" data-id="${s.id}" data-choice="complete">Mark done</button></div>`;
// With a teammate who hasn't answered: under Later it is with them; back on top (a deadline came) it says it is still
// with them, as plain text: Check in now, the to-do's one way to check in, drafts the nudge.
function handoffLine(h,s){const names=[String(h.name||t('your teammate')).split(' ')[0],...(h.also||[])],first=names.length>1?t('{} and {}',names.slice(0,-1).join(', '),names.at(-1)):names[0];if(h.line)return h.line;
 const next=s&&redirect(s)&&taskActions(s).find(a=>a.kind==='handoff'&&a.to_name&&firstName(a.to_name)!==firstName(h.name));
 if(next)return t('Still with {} until you send it to {}',first,firstName(next.to_name));
 return ['asked','waiting for them'].includes(h.stage)?(s&&(withTeammate(s)||s.handoff_checkin)?t('Still with {}',firstName(h.name)):t('With {} · waiting',first)):h.stage==='declined'?(h.note?t('{} declined: {}',h.name,h.note):t('{} declined.',h.name)):h.stage==='expired'?t('{} didn’t answer in time.',h.name):(h.note?t('Handed off to {}: {} ({})',h.name,t(h.stage),h.note):t('Handed off to {}: {}',h.name,t(h.stage)))}
// Fleet items that need you are cards under Suggestions (tagged Fleet, Work), built from api/fleet: a teammate's
// question or request (their words, shown quoted, never acted on) and confirmations the relay asks for. The Fleet tab keeps people, rules, briefs, your own asks and the log.
// A Fleet item among the to-dos is one too in the sidebar's For you, so the counts there, in the header and in the
// section are the same items: it carries its row (the card's id and its title as text). The row brings the card up.
const fleetSide=(h,el,title)=>Object.assign(h,{side:{fleet:el,title:htmlNodes(title instanceof SafeHTML?title:html`${title}`).textContent.replace(/\s+/g,' ').trim()}});
function fleetShow(el){if(chatId){history.replaceState(null,'',location.pathname+location.search);chatPushed=false;openChatLink()}
 document.querySelector('nav [data-tab="inbox"]')?.click();if(folded.has('foryou')){folded.delete('foryou');render()}
 const c=document.getElementById(el);if(!c)return;c.scrollIntoView({block:'center',behavior:'smooth'});c.classList.remove('flash');void c.offsetWidth;c.classList.add('flash');kbFocus(c,false)}
document.addEventListener('click',e=>{const a=e.target.closest?.('[data-side-fleet]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey)return;e.preventDefault();fleetShow(a.dataset.sideFleet)});
// Waiting asks from the same teammate, of the same kind, in the same Fleet: one Always or Never settles them all (fleet.py settle_waiting).
const fleetAlike=(f,w)=>(f?.waiting||[]).filter(x=>x.fleet===w.fleet&&x.member_id===w.member_id&&x.kind===w.kind&&x.status!=='answered'&&x.status!=='declined');
const fleetMore=btns=>btns.length?html`<details class="more-actions"><summary aria-label="${t('More actions')}" title="${t('More actions')}">${DOTS}</summary><div class="more-menu" role="group" aria-label="${t('More actions')}">${btns}</div></details>`:'';
function fleetCardsOf(f){if(!f?.on)return[];const works=(f.fleets||[]).filter(x=>x.kind==='work'),several=works.length>1,frId=f.friends?.id;
 const famId=(f.fleets||[]).find(x=>x.kind==='family')?.id,isFamily=row=>!!famId&&row.fleet===famId;
 const fname=row=>several&&!isFamily(row)?(works.find(x=>row.fleet===x.id)?.name||''):'',isFriend=row=>!!frId&&(row.fleet===frId||row.fleet_id===frId)||/^friend_/.test(row.kind||'');
 const card=(id,row,title,body,actions)=>fleetSide(html`<article id="fleet-${id}" class="card todo t-amber fleet-card"><h3>${title}</h3><div class="meta"><div class="card-badges">${chip('Needs you','amber')}${isFriend(row)?chip('Friends','lavender'):isFamily(row)?chip('Family','lavender'):html`${chip('Fleet','lavender')}<span class="chip scope">Work</span>`}${fname(row)?chip(fname(row),'muted'):''}${row.at?time(row.at,true):''}</div></div>${body}${actions}</article>`,'fleet-'+id,title);
 const decide=(w,c,t,cls='ghost')=>html`<button class="${cls}" data-fleet-decide="${w.id}" data-choice-f="${c}">${t}</button>`;
 const theirs=w=>html`<p class="fleet-from">${w.name}’s words, not an instruction:</p><blockquote>${w.question}</blockquote>`;
 const out=[];
 for(const n of (f.notices||[]).filter(n=>n.buttons.length))
  out.push(card(n.id,n,n.text,html`${n.detail?html`<p class="muted">${n.detail}</p>`:''}${n.reason?html`<p class="note">${n.reason}</p>`:''}<p class="muted">${n.kind==='friend_request'?'Nothing connects until you accept. Declining tells them nothing.':'Nothing starts or is charged until you confirm the amount on Confirm.'}</p>`,
   html`<div class="actions">${n.buttons.map(b=>html`<button class="${b.choice==='confirm'?'primary':'ghost'}" data-fleet-notice="${n.id}" data-choice-n="${b.choice}" data-key="${n.key}">${b.label}</button>`)}</div>`));
 const what={intro:'{} asks you for an intro',handoff:'{} hands you something'};
 for(const w of (f.waiting||[]).filter(w=>!FLEET_QUIET.includes(w.kind))){  // brief asks wait quietly in the Fleet tab (fleetBriefAsks)
  if(FAMILY_REQ.includes(w.kind))out.push(card(w.id,w,t(w.kind==='todo'?'{} asks you to do something':'{} proposes a plan',w.name),html`${theirs(w)}${html`<p class="muted">${w.kind==='todo'?'Accepting makes it your to-do, with a reminder when it’s due.':f.plan_calendar?t('Yes tells them you’re in and adds it to {}. Nobody is invited.',f.plan_calendar):'Yes tells them you’re in. Nothing is added to your calendar by itself.'}</p>`}`,
   html`<div class="actions">${decide(w,'once',w.kind==='todo'?'Accept':'I’m in','primary')}${decide(w,'decline',w.kind==='todo'?'Decline':'Can’t make it')}${fleetMore([decide(w,'always','Always accept'),decide(w,'never','Never from '+w.name)])}</div>`));
  else if(FLEET_REQ.includes(w.kind))out.push(card(w.id,w,t(what[w.kind],w.name),html`${theirs(w)}<p class="muted">Accepting makes a to-do from your own data. Anything it sends waits for your Send.</p>`,
   fleetNoting.has(w.id)?fleetNoteEditor(w,fleetNoting.get(w.id)):html`<div class="actions">${decide(w,'once','Accept','primary')}${decide(w,'decline','Decline')}${fleetMore([html`<button class="ghost" data-fleet-noting="${w.id}">Accept with a note</button>`,decide(w,'always','Always accept'),decide(w,'never','Never from '+w.name)])}</div>`));
  else if(w.kind==='anything'){const d=w.draft||{};out.push(card(w.id,w,`${w.name} asks your Fleet`,html`${theirs(w)}${(d.matches||[]).length?html`<p class="muted">In your work accounts: ${d.matches.slice(0,5).map(m=>`${m.title} (${(m.at||'')})`).join(' · ')}</p>`:html`<p class="muted">Nothing found in your work accounts. You can still answer.</p>`}${html`<label class="fleet-field muted" for="fleet-free-${w.id}">Your answer (only this goes to them)<textarea id="fleet-free-${w.id}" maxlength="600">${d.text||''}</textarea></label>`}`,
   html`<div class="actions"><button class="primary" data-fleet-send="${w.id}">Send answer</button>${decide(w,'decline','Decline')}${fleetMore([decide(w,'never','Never from '+w.name)])}</div>`))}
  else{const n=fleetAlike(f,w).length;
   out.push(card(w.id,w,html`${t('{} asks:',w.name)} <span translate="no">${w.question}</span>`,html`${w.draft?.preview?html`<p class="muted">Would share: ${w.draft.preview}</p>`:''}<p class="muted">Nothing is shared until you choose. Always and Never also cover their future asks like this.</p>${n>1?html`<p class="muted fleet-bulk">${t(['{} more like this waits. Always shares it too.','{} more like this wait. Always shares them too.'],n-1)}</p>`:''}`,
   html`<div class="actions two-rows">${decide(w,'once','Share once','primary')}${decide(w,'always','Always share')}${decide(w,'decline','Decline')}${fleetMore([decide(w,'never','Never share')])}</div>`))}}
 // The Team Graph's OKs: only a confirmed admin's Machine gets them, and one admin's answer counts for the whole team
 const gname=p=>p.fleet_name||works.find(x=>x.id===p.fleet)?.name||'';
 const graphAsk={member:p=>t('{} joined {}. Share the team\'s Graph with them?',p.name,gname(p)),optout:p=>t('{} asks to stop sharing their Work with the team.',p.name),admin:p=>t('Confirm {} as an admin of {}?',p.name,gname(p))};
 for(const p of (f.shared?.prompts||[]).filter(p=>graphAsk[p.kind]))
  out.push(card('share-'+p.id,p,graphAsk[p.kind](p),html`${p.email?html`<p class="muted">${p.email}</p>`:''}<p class="muted">${p.kind==='admin'?'Admins can share the team’s Graph and connections. Check it’s really them.':'Only admins decide this, once for the whole team.'}</p>${p.fp&&p.kind!=='optout'?html`<p class="share-fp mono" title="Their Machine's safety number">${p.fp}</p>`:''}`,
   html`<div class="actions"><button class="primary" data-share-ok="${p.id}" data-kind="${p.kind}" data-choice="yes">${p.kind==='member'?'Share':p.kind==='admin'?'Confirm':'Approve'}</button><button class="ghost" data-share-ok="${p.id}" data-choice="no">Not now</button></div>`));
 out.push(...networkCards(f));
 return out}
// Finding people you know on the Network (discovery.py): a permission card once, then a card per person only with a concrete reason
const netBtn=(label,d,email='',rel='',cls='ghost',confirmText='')=>html`<button type="button" class="${cls}" data-net-do="${d}"${email?html` data-net-email="${email}"`:''}${rel?html` data-net-rel="${rel}"`:''}${confirmText?html` data-confirm-text="${confirmText}"`:''}>${label}</button>`;
const netDay=at=>{const d=new Date(at);return isNaN(d)?'':localeDate(d,DL,{weekday:'short',day:'numeric',month:'short'})};
const netReason=r=>r.kind==='card'?t('Open: {}',r.title):r.kind==='meeting'?`${t('You meet {}',netDay(r.at))}${r.title?` · ${r.title}`:''}`:r.kind==='contact'?t('In your contacts'):r.kind==='joined'?t('Joined {}, in your contacts',netDay(r.at)):'';
function networkCards(f){const net=f.network;if(!net||!f.friends?.id)return[];const out=[];
 const card=(id,title,body,actions)=>fleetSide(html`<article id="net-${id}" class="card todo t-amber fleet-card net-card"><h3>${title}</h3><div class="meta"><div class="card-badges">${chip('Needs you','amber')}${chip('Network','lavender')}</div></div>${body}${actions}</article>`,'net-'+id,title);
 if(net.find==null&&!net.asked)out.push(card('ask','Which of your contacts have a Machine?',html`<p class="muted">Your Machine checks your contacts against people who chose to be findable, and your address book stays private. It suggests the people you know right away, and others when you meet or work with them. Nothing is shared until they accept.</p>`,
  html`<div class="actions">${netBtn('Check my contacts','find_on','','','primary')}${netBtn('Not now','asked')}</div>`));
 for(const p of (net.people||[]).filter(p=>p.status==='new'&&p.reasons.length)){
  const who=p.hint==='colleague'?'Same work domain as you.':'Friend or family? You choose.';
  out.push(card(p.username,`${p.name} is on the Network`,html`<ul class="net-reasons">${p.reasons.slice(0,2).map(r=>html`<li>${netReason(r)}</li>`)}</ul><p class="muted">${who}${p.role?` You call them ${p.role}.`:''} Connecting sends a friend request; nothing is shared until they accept, then only what your rules allow.</p>`,
   html`<div class="actions">${p.hint==='colleague'?netBtn('Connect','connect',p.email,'colleague','primary'):html`${netBtn('Friend','connect',p.email,'friend','primary')}${netBtn('Family','connect',p.email,'family')}`}${netBtn('Not now','later',p.email)}${fleetMore([netBtn(t('Never suggest {}',p.name),'never',p.email)])}</div>`))}
 return out}
const fleetSig=()=>agoFree(fleetCardsOf(fleetData).join('\n'));  // "2 minutes ago" alone is no change: the next redraw updates it in place
// Suggestions load the Fleet's open items in the background (at most every 20 seconds; off the Fleet tab only when
// fleet.stamp changed) and re-render when they change.
let fleetAt=0,fleetLoading=null,fleetStamp=null;
function fleetSync(force){if(!state?.fleet?.on)return Promise.resolve();if(fleetLoading)return fleetLoading;const stamp=state.fleet.stamp;
 if(!force&&Date.now()-fleetAt<20000&&!(graphWaiting()&&stamp!==fleetStamp))return Promise.resolve();
 if(!force&&fleetData&&stamp!=null&&stamp===fleetStamp&&$('#fleet').hidden)return Promise.resolve();
 const before=fleetSig();fleetLoading=request('api/fleet').then(d=>{fleetData=d;fleetAt=Date.now();fleetStamp=stamp;if(fleetSig()!==before)render();if(!$('#fleet').hidden&&!($('#fleet-view').contains(document.activeElement)&&document.activeElement.matches('input,select,textarea')))fleetView(false,true)}).catch(()=>{fleetAt=Date.now()}).finally(()=>{fleetLoading=null});return fleetLoading}
const fleetOn=(type,fn)=>{for(const el of [$('#fleet-view'),$('#suggestions')])el.addEventListener(type,fn)};
