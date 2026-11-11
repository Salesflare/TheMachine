// The Fleet's shared part: what to-do cards, the Graph and Settings use from the Fleet (its data, asks on cards, links,
// sharing pop-ups and the handlers for Fleet markup on to-dos). The Fleet tab's own views (fleet-rules, -sharing, -tabs
// and -manage) load when first needed (dashboard_parts.LAZY); fleetView() fetches the Fleet and draws the tab once they're in.
// The Fleet: what teammates' Machines said, the questions waiting for you, your rules per teammate, and the log of both directions.
const fleetPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
// Share: the OK is signed at once; sealing the team's Graph for them runs after (shared_connectors.graph_soon). One line while it does.
const graphSendingLine=n=>html`<p class="graph-sending" role="status"><i class="spin" aria-hidden="true"></i>Sharing with ${n}…</p>`;
const graphSent={};  // fleet: how many Share with all shared with, to say so once the line is gone
function graphSendingWatch(){const list=(fleetData?.shared?.graph)||[];let busy=false;
 for(const g of list){if(g.sending)busy=true;else if(graphSent[g.fleet]){toast(`Shared with ${graphSent[g.fleet]}.`);delete graphSent[g.fleet]}}
 clearTimeout(graphSendingWatch.t);graphSendingWatch.t=busy?setTimeout(()=>fleetView(true).then(graphSendingWatch),4000):0}
// Teammates' brief asks (fleet.py QUIET): never a to-do. One quiet box in their Fleet's pane, the latest ask per teammate
// (older ones expire), with the same choices as before. Nothing is shared until the owner picks one; unanswered, they expire.
const FLEET_QUIET=['brief'];
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
let sharedData={},sharedShown={};
const sharedAsking={};  // the admin's open "Turn off sharing for everyone?" per Fleet: it stays open through a reload
// Share with… for the picked threads of one group: the teammates chosen get them, nobody else on the team.
function sharedPeopleOpen(fleet,ids){const people=sharedData[fleet]?.teammates||[];
 lazyRun('graph',()=>spOpen({title:t(['Share {} thread with…','Share {} threads with…'],ids.length),action:'graph_share_many',args:{event_ids:ids,share:'people'},chosen:[],people,
  line:who=>t('Goes to {} only, also if sensitive. Not to the rest of the team.',who),
  done:who=>t(['Shared {} thread with {} only.','Shared {} threads with {} only.'],ids.length,who),after:()=>sharedLoad(fleet,true)}))}
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
 if(b.dataset.graphRemove&&!b.dataset.back&&!confirm('Take them out of the team\'s Graph? Nothing new goes to their Machine, and what the team shared with them is removed from it.'))return;
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
 const pp=e.target.closest('[data-pop-people]');if(pp){const c=document.querySelector(`[data-share-event="${pp.dataset.popPeople}"]`);sharePopClose();const had=JSON.parse(c?.dataset.share||'{}').people;lazyRun('graph',()=>threadShareOpen(pp.dataset.popPeople,had));return}
 const b=e.target.closest('[data-pop-set],[data-pop-rule]');if(!b)return;b.disabled=true;
 try{if(b.dataset.popSet){const to=b.dataset.share,r=await graphPost('graph_share',{event_id:Number(b.dataset.popSet),share:to});toast(to==='team'?'Shared with your team.':b.dataset.before?'Kept private. It won\'t go.':'Unshared. Teammates\' Machines delete their copy. Someone may have read it already.');
   const s=r?.suggest||r?.result?.suggest;if(s)sharePopSuggest(document.querySelector(`[data-share-event="${b.dataset.popSet}"]`),s);else sharePopClose();await graphPeople(graphNode,true)}
  else{const c=b.dataset.choice;await graphPost('graph_rule',{key:b.dataset.popRule,choice:c,name:b.dataset.name});sharePopClose();toast(c==='private'?`Threads with ${b.dataset.name} stay with you.`:`Client threads with ${b.dataset.name} go to the team.`);await graphPeople(graphNode,true)}}
 catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&$('#share-pop'))sharePopClose()});
const fleetGroups=n=>[...new Set((n.fleet?.in||[]).map(x=>({work:'Fleet',family:'Family',friends:'Friend'})[x.kind]||x.label))].join(' · ');
const fleetLine=n=>[n.fleet?.machine?'Has a Machine':'',...(n.fleet?.in||[]).map(x=>x.kind==='work'&&x.fleet_name?`${x.label} (${x.fleet_name})`:x.label)].filter(Boolean).join(' · ');
const fleetChip=(n,where)=>n.fleet?.in?.length?html`<span class="chip fleet-chip${where?' fleet-chip-'+where:''}" style="--c:var(--mint)" title="${fleetLine(n)}"><span class="ct">${fleetGroups(n)}</span></span>`:'';
function fleetAskRow(n){if(!state?.fleet?.on||!['person','org'].includes(n.kind)||n.fleet?.in?.some(x=>x.kind==='work'))return'';const about=n.kind==='org'?(n.domain||n.name):/^email:/.test(n.id)?n.id.slice(6):n.name;
 return html`<p class="graph-sub detail-fleet-ask"><button type="button" class="link" data-fleet-ask="${about}">Ask the Fleet who knows ${n.name||about}</button></p>`}
let fleetData=null,fleetShown=Promise.resolve(),fleetViewVersion=0,fleetPane=localStorage.getItem('fleet-pane')||'';
// The Fleet tab shows one view at a time; switching is instant (no reload) and remembered.
function showFleetPane(id){const view=$('#fleet-view');if(!view.querySelector(`[data-pane="${CSS.escape(id)}"]`))return;fleetPane=id;localStorage.setItem('fleet-pane',id);
 for(const b of view.querySelectorAll('[data-fleet-pane]'))b.setAttribute('aria-selected',b.dataset.fleetPane===id);
 for(const p of view.querySelectorAll('.fleet-pane'))p.hidden=p.dataset.pane!==id;
 if(/^shared-/.test(id))sharedLoad(id.slice(7),true)}
const fleetReveal=el=>{const p=el?.closest('.fleet-pane');if(p&&p.hidden)showFleetPane(p.dataset.pane)};
async function fleetView(refresh=false,cached=false){const view=$('#fleet-view'),before=fleetSig(),version=++fleetViewVersion;if(!cached||!fleetData)try{const stamp=state?.fleet?.stamp,next=await request('api/fleet'+(refresh?'?refresh=1':''));if(version!==fleetViewVersion)return;fleetData=next;fleetAt=Date.now();fleetStamp=stamp;if(state?.suggestions&&fleetSig()!==before)render()}catch(e){errCaught(e);if(version===fleetViewVersion){view._fleetHTML=null;setHTML(view,html`<p class="error">${e.message}</p>`)}return}
 // the tab's views load when first needed (dashboard_parts.LAZY): drawn once they're in, an error in place of them offline
 if(!lazyIn('fleet'))try{await lazyPart('fleet');if(version!==fleetViewVersion)return}catch(e){if(version===fleetViewVersion){view._fleetHTML=null;setHTML(view,html`<p class="error">${e.message}</p>`)}return}
 fleetDraw(view)}
// Family (family.py): when everyone is free, to-dos for one another and plans to say yes or no to. Self-contained:
// its forms post family_free, family_todo and family_event; what waits for you is a card under Suggestions.
const FAMILY_REQ=['todo','event'];
fleetOn('click',async e=>{const b=e.target.closest('[data-net-do]');if(!b)return;if(b.dataset.confirmText&&!confirm(b.dataset.confirmText))return;b.disabled=true;
 try{const r=await fleetPost('fleet_network',{do:b.dataset.netDo,email:b.dataset.netEmail||'',relation:b.dataset.netRel||''});
  toast(r?.status==='connected'?'Already friends. Nothing was sent.':{find_on:'On. Your Machine checks your contacts privately.',asked:'Okay. Turn it on any time in the Fleet tab.',connect:'Request sent. It waits until they accept.',later:'Hidden for now.',never:'Won’t suggest them again.',leave:'You left the Network.'}[b.dataset.netDo]||'Done.');await fleetView();await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
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
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-send]');if(!b)return;const text=document.getElementById('fleet-free-'+b.dataset.fleetSend)?.value.trim();if(!text){toast('Write an answer first, or decline.',true);return}b.disabled=true;
 try{await fleetPost('fleet_decide',{id:b.dataset.fleetSend,choice:'once',text});toast('Sent.');await fleetView();await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-notice]');if(!b)return;b.disabled=true;
 try{const r=await fleetPost('fleet_notice_decide',{id:b.dataset.fleetNotice,choice:b.dataset.choiceN,key:b.dataset.key});
  const fr=/^friend/.test(fleetData?.notices?.find(n=>n.id===b.dataset.fleetNotice)?.kind||'');
  toast(r.status==='confirmed'?(fr?'Accepted. You are friends now.':'Confirmed. Their Machine is starting.'):r.status==='declined'?(fr?'Declined. They are not told.':'Declined. Nothing was started or charged.'):r.reason,r.status==='stale'||r.status==='changed');await fleetView();await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-learn-remove]');if(!b)return;b.disabled=true;  // gone for the whole Fleet, for good
 try{await fleetPost('fleet_learning_remove',{fleet:b.dataset.fleet,fp:b.dataset.fleetLearnRemove});toast(t('Removed for the whole team.'));if(b.closest('#suggestions'))await refresh();else await fleetView()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
const fleetRedraw=()=>{render();if(!$('#fleet').hidden)fleetView(false,true)};
fleetOn('click',async e=>{const p=e.target.closest('[data-fleet-pick]');if(p){const on=p.getAttribute('aria-pressed')!=='true';for(const r of p.parentElement.children)r.setAttribute('aria-pressed','false');p.setAttribute('aria-pressed',String(on));return}
 const o=e.target.closest('[data-fleet-noting],[data-fleet-note-cancel]');if(o){if(o.dataset.fleetNoting)fleetNoting.set(o.dataset.fleetNoting,'once');else fleetNoting.delete(o.dataset.fleetNoteCancel);fleetRedraw();return}
 const n=e.target.closest('[data-fleet-note-send]');if(!n)return;const box=n.closest('.fleet-note-editor'),id=n.dataset.fleetNoteSend;
 const note=[box?.querySelector('.reason[aria-pressed="true"]')?.dataset.fleetPick,(box?.querySelector('textarea')?.value||'').trim()].filter(Boolean).join(': ').slice(0,160);n.disabled=true;
 try{const r=await fleetPost('fleet_decide',{id,choice:n.dataset.choiceF,...(note?{note}:{})});fleetNoting.delete(id);toast((r.status==='answered'?'Accepted.':'Declined.')+(note?' They see your note.':''));await fleetView();await refresh()}catch(err){errCaught(err);n.disabled=false;toast(err.message,true)}});
fleetOn('click',async e=>{const b=e.target.closest('[data-share-ok],[data-share-stop]');if(!b)return;
 if(b.dataset.shareStop&&!confirm('Stop sharing it? Every teammate\'s Machine loses access to it.'))return;b.disabled=true;
 const member=b.dataset.kind==='member',card=member?b.closest('article'):null,label=b.textContent;if(member)b.textContent='Sharing…';
 try{if(b.dataset.shareStop){await fleetPost('fleet_share_stop',{fleet:b.dataset.fleet,service:b.dataset.shareStop});toast('Stopped sharing.')}
  else{const r=await fleetPost('fleet_share_ok',{id:b.dataset.shareOk,choice:b.dataset.choice});if(card)card.hidden=true;toast(r.done?(b.dataset.kind==='optout'?'Approved. Their Work stops going to the team.':'Done. Their Machine gets it next.'):'Okay.')}
  await fleetView();if(member)graphSendingWatch()}catch(err){errCaught(err);b.disabled=false;if(member)b.textContent=label;toast(err.message,true)}});
fleetOn('click',async e=>{const b=e.target.closest('[data-fleet-decide]');if(!b)return;
 if(b.dataset.choiceF==='decline'&&FLEET_REQ.includes(fleetData?.waiting?.find(x=>x.id===b.dataset.fleetDecide)?.kind)){fleetNoting.set(b.dataset.fleetDecide,'decline');fleetRedraw();return}
 b.disabled=true;
 try{const r=await fleetPost('fleet_decide',{id:b.dataset.fleetDecide,choice:b.dataset.choiceF});if(r.calendar)toastPlanUndo(r.calendar);else toast(r.status==='answered'?'Answered.':'Declined.');await fleetView();await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
// "I'm in" put the plan on the owner's own calendar (family.py): Undo takes the event off again; their yes stays.
function toastPlanUndo(c){toast(t('Answered. Added to {}.',c.name));$('#toast').append(htmlNodes(html` <button type="button" data-plan-undo="${c.id}">${t('Undo')}</button>`));clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),15000)}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-plan-undo]');if(!b)return;b.disabled=true;
 try{await fleetPost('family_plan_undo',{id:b.dataset.planUndo});toast(t('Removed from your calendar.'));await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
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
// #fleet=<question> from a phone notification or Telegram: the Fleet tab at that question; &choice= asks to confirm it.
// #fleet-brief=<fleet> (the brief's notification; without a Fleet, a phone's older wakeup): the Fleet tab at that team brief, in its pane
// #fleet and #fleet/<pane> (#fleet/sharing, #fleet/activity) are links to the tab: they stay in the address, as #todos does.
function openFleetLink(){const brief=/^#fleet-brief(?:=(fl_[0-9a-f]{16}))?$/.exec(location.hash),sub=/^#fleet\/([a-z0-9_-]{1,40})$/.exec(location.hash),m=brief||sub?[]:/^#fleet(?:=((?:q|fn)_[a-f0-9]{16})(?:&choice=(once|decline))?)?$/.exec(location.hash),card=/^q_/.test(m?.[1]||''),tab=sub||m&&!brief&&!m[1];
 // before the status comes (a tapped notification on a slow start): the Fleet tab at once, its own data fills it; a question's card waits for its to-dos
 if(!m||(card||state.suggestions)&&!state.fleet?.on)return;
 if(!tab)history.replaceState(null,'',location.pathname+location.search);else if(!$('#fleet').hidden&&(!sub||sub[1]===fleetPane))return;  // on screen already: a refresh leaves it be
 if(card||$('#fleet').hidden)document.querySelector(`nav [data-tab="${card?'inbox':'fleet'}"]`).click();
 (card?fleetSync(true):fleetShown).then(()=>{if(sub){showFleetPane(sub[1]);return}const c=brief?brief[1]&&document.getElementById('fleet-brief-'+brief[1])||$('#fleet-view .fleet-brief'):m[1]&&document.getElementById('fleet-'+m[1]);if(!c)return;fleetReveal(c);c.scrollIntoView({block:'center',behavior:'smooth'});c.classList.remove('flash');void c.offsetWidth;c.classList.add('flash');
  const w=m[2]&&fleetData?.waiting.find(x=>x.id===m[1]);if(w&&confirm(`${m[2]==='once'?'Share once':'Decline'}? ${w.name} asks: ${w.question}`))c.querySelector(`[data-choice-f="${m[2]}"]`)?.click()})}
// A shared pane is in the tab's views, which load when first needed: until they're in there is none to fill.
function sharedLoad(fleet,quiet){if(lazyIn('fleet'))return sharedFill(fleet,quiet)}
