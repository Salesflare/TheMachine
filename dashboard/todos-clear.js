// Go through (For you): one to-do at a time with its whole draft and the card's own actions.
// Send posts the send dialog's confirm (sendConfirmed) for the revision on screen only. Header pace: clear_pace.py.
const CR_MSG=['email','linkedin','slack','x','whatsapp','telegram','signal','intercom','doc_reply'];
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
// Go through's dialog loads when first needed (todos-clear-run.js, dashboard_parts.LAZY 'clearrun').
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-clear-run]');if(b){e.stopPropagation();const key=b.dataset.clearRun;lazyRun('clearrun',()=>openClearRun(key))}},true);
document.addEventListener('keydown',e=>{if(e.target.closest?.('[data-clear-run]')&&(e.key==='Enter'||e.key===' '))e.stopPropagation()},true);
