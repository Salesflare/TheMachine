// Go through (For you): one to-do at a time with its whole draft and the card's own actions.
// Send posts the send dialog's confirm (sendConfirmed) for the revision on screen only. Header pace: clear_pace.py.
const CR_MSG=['email','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply'];
const crDraft=s=>taskActions(s).find(a=>DRAFT_KINDS.includes(a.kind)&&!['handoff','email_demo'].includes(a.kind)&&!sendBusy(a.state||s.action_status)&&!(a.kind==='finish'&&(a.state||s.action_status)?.status==='done')&&!docMade(s,a));
// 'send', 'dialog' (the send dialog decides), 'do', or '' (left out: also a result that asks the owner something, which
// takes an answer and not a tap, so it is in neither the header's time nor the run)
function crKind(s){if(!s||!state.suggestions.includes(s)||closed(s)||s.status==='snoozed'||looksDone(s)||waitsOnOthers(s)||s.handled_hint||ownerStep(s)||withTeammate(s)||s.review_in||s.preparation_status==='blocked')return '';
 if(s.status==='pending')return s.skill_proposal?.update?'':'do';
 const a=s.status==='prepared'&&!needsAsk(s)&&crDraft(s);if(!a)return '';
 return CR_MSG.includes(a.kind)&&!a.to_options?.length&&(a.from_options||[]).length<2&&!movedLine(a)&&!(a.to||[]).some(x=>a.bounced?.[String(x).toLowerCase()])?'send':'dialog'}
const crList=(v,key)=>(v[key]||[]).filter(s=>plainTodo(s)&&crKind(s));
const crPace=()=>+state?.clear_pace||30;
let crFuv=null;
function clearHead(key,v){if(key!=='foryou')return '';crFuv=v;const n=crList(v,key).length,min=Math.max(1,Math.ceil(n*crPace()/60));if(!n)return '';
 return html`<span class="clear-time">${t('about {} min',min)}</span>${n>1?html`<button type="button" class="clear-go" data-clear-run="${key}">${t('Go through')}</button>`:''}`}
let cr=null;  // {ids, at, n, sent, done, started, busy, asking}
function crDialog(){let d=$('#clear-run');if(d)return d;d=make('dialog',{id:'clear-run',class:'clear-run','aria-label':t('Go through'),tabindex:'-1'});document.body.append(d);
 d.addEventListener('close',()=>{cr=null;d.replaceChildren();render()});
 d.addEventListener('click',crClick);d.addEventListener('keydown',crKey);return d}
function openClearRun(key){const ids=crFuv?crList(crFuv,key).map(s=>s.id):[];if(!ids.length)return;cr={ids,at:0,sent:0,done:0,started:Date.now()};const d=crDialog();crDraw();if(!d.open)d.showModal();d.focus()}
const crNow=()=>{while(cr&&cr.at<cr.ids.length&&!crKind(state.suggestions.find(s=>s.id===cr.ids[cr.at])))cr.at++;return cr&&state.suggestions.find(s=>s.id===cr.ids[cr.at])};
const crClock=ms=>{const s=Math.round(ms/1000);return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')};
function crDraw(error=''){const d=crDialog(),s=crNow();
 if(!s){const took=crClock(Date.now()-cr.started);
  setHTML(d,html`<div class="cr-end"><p class="cr-done">${cr.sent?t(['{} reply out in {}','{} replies out in {}'],cr.sent,took):cr.done?t(['{} to-do cleared in {}','{} to-dos cleared in {}'],cr.done,took):t('Nothing cleared.')}</p><button type="button" class="primary" data-cr="close">${t('Back to the list')}</button></div>`);
  d.querySelector('[data-cr="close"]').focus();return}
 const kind=crKind(s),a=kind==='do'?null:crDraft(s),left=cr.ids.length;
 const go=t(kind==='do'?'Do it':CR_MSG.includes(a.kind)?'Send':sendLabel(a));
 const k=v=>html`<kbd class="cr-key" aria-hidden="true">${v}</kbd>`;
 setHTML(d,html`<div class="cr-top"><span class="cr-pos">${t('{} of {}',cr.at+1,left)}</span><button type="button" class="cr-x" data-cr="close" aria-label="${t('Close')}">×</button></div>
 <div class="cr-main"><h2 class="cr-title" translate="no">${s.title}</h2>${a?html`<div class="cr-draft">${draftBox(s,a,'')}</div>`:html`<div class="cr-body" translate="no">${format(s.body||'')}</div>`}</div>
 ${cr.asking?html`<div class="cr-ask"><textarea id="cr-ask" spellcheck="true" autocapitalize="sentences" rows="3" placeholder="${t('Tell me what to change (Ctrl+Enter saves)')}" aria-label="${t('Ask for changes')}"></textarea><div class="cr-acts"><button type="button" class="primary" data-cr="ask-save">${t('Send changes')}</button><button type="button" data-cr="ask-back">${t('Back')}</button></div></div>`:''}
 <p class="cr-error" role="alert">${error}</p>
 <div class="cr-acts"${cr.asking?html` hidden`:''}><button type="button" class="primary" data-cr="go" data-id="${s.id}" data-rev="${a?.revision||''}">${go}${k('Enter')}</button><button type="button" data-cr="ask">${t('Ask for changes')}</button><button type="button" data-cr="snooze">${t('Snooze')}${k('S')}</button><button type="button" data-cr="skip">${t('Skip')}${k('→')}</button></div>`);
 d.querySelector('.cr-main').scrollTop=0;if(cr.asking)$('#cr-ask').focus();else d.focus()}
function crAfter(dialog,id,sent){$(dialog).addEventListener('close',async()=>{if(!cr)return;await refresh().catch(()=>{});
 if(crKind(state.suggestions.find(s=>s.id===id))){crDraw();return}sent?cr.sent++:cr.done++;cr.at++;crDraw()},{once:true})}
async function crAct(what){if(!cr||cr.busy)return;const s=crNow();if(!s)return;const id=s.id,kind=crKind(s);
 if(what==='skip'){cr.at++;crDraw();return}
 if(what==='snooze'){openSnooze(id);crAfter('#snooze-dialog',id,false);return}
 if(what==='ask'){cr.asking=true;crDraw();return}
 if(what==='ask-back'){cr.asking=false;crDraw();return}
 const run=async(f,sent)=>{cr.busy=true;try{await f();cr.asking=false;sent?cr.sent++:cr.done++;cr.at++;await refresh().catch(()=>{});crDraw()}catch(e){errCaught(e);crDraw(e.offline&&!e.slow?t('Offline. Send again when you’re back online.'):e.message)}finally{if(cr)cr.busy=false}};
 if(what==='ask-save'){const text=$('#cr-ask')?.value.trim();if(!text){$('#cr-ask')?.focus();return}return run(()=>saveDecision(id,'other',text),false)}
 if(what!=='go')return;
 if(kind==='do')return run(()=>saveDecision(id,'accept'),false);
 // Only the draft on screen goes
 const shown=$('#clear-run [data-cr="go"]')?.dataset.rev,a=crDraft(s),box=$('#clear-run .draft[data-rev]');
 if(!shown||a?.revision!==shown||(box&&box.dataset.rev!==shown)){crDraw(t('That draft changed. Review the current result.'));return}
 if(kind==='dialog'){openSend(id,shown);crAfter('#send-dialog',id,true);return}
 return run(()=>sendConfirmed(id,shown,a.kind),true)}
function crClick(e){const b=e.target.closest('[data-cr]');if(!b)return;if(b.dataset.cr==='close'){$('#clear-run').close();return}crAct(b.dataset.cr)}
function crKey(e){if(!cr||e.altKey||e.isComposing||[...document.querySelectorAll('dialog[open]')].some(x=>x.id!=='clear-run'))return;
 if(e.target.id==='cr-ask'){if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)){e.preventDefault();crAct('ask-save')}return}
 if(e.ctrlKey||e.metaKey)return;
 if(e.target.closest?.('button,a,textarea,input,select')&&e.key==='Enter')return;
 if(!crNow()){if(e.key==='Enter'){e.preventDefault();$('#clear-run').close()}return}
 const what={Enter:'go',s:'snooze',S:'snooze',ArrowRight:'skip'}[e.key];if(what){e.preventDefault();crAct(what)}}
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-clear-run]');if(b){e.stopPropagation();openClearRun(b.dataset.clearRun)}},true);
document.addEventListener('keydown',e=>{if(e.target.closest?.('[data-clear-run]')&&(e.key==='Enter'||e.key===' '))e.stopPropagation()},true);
