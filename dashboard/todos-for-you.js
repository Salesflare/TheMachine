// Which to-dos stand where on To-dos, and in which order (For you first), from the status alone: no page, no markup, and
// nothing else of the dashboard but what is named here. Another page can run this file as it is, with its own t, SafeHTML,
// TODO, SENDS, state and fuGroupCard: the desktop robot's box does (desktop/), so both show the same list.
const localDay=d=>[d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-');
const closed=s=>TODO.CLOSED.includes(s.status);
// The open lists' order (For you, Waiting on others; the sidebar the same): what is overdue or due by
// tomorrow first, then the rest; each newest first by when it was added, the time its to-do shows. A tie (one review
// made them together) goes to the one about the people closest to you (weight), then the id. A to-do a new signal
// reopened was added when it came back (reopened_at, Store.card_views), not weeks before.
const dueSoon=s=>{if(!s.due)return false;const at=s.due_at?Date.parse(s.due_at):NaN;if(!isNaN(at)&&at<Date.now())return true;const t=new Date();t.setDate(t.getDate()+1);return s.due<=localDay(t)};
const cameIn=s=>s.reopened_at||s.created_at,addedAt=s=>Date.parse(cameIn(s))||0;
const openOrder=(a,b)=>dueSoon(b)-dueSoon(a)||addedAt(b)-addedAt(a)||(b.weight||0)-(a.weight||0)||String(a.id).localeCompare(String(b.id));
// For you: due by tomorrow, a Fleet ask, a board's follow-ups, the rest, each in openOrder. Prepared, Needs you and
// Preparing… are only chips: the order reads the to-do's own fields, so a run starting or ending never moves it.
const plainTodo=x=>!!x&&typeof x==='object'&&!(x instanceof SafeHTML);
function forYouList(ready,needs){const rank=(x,fleet)=>!plainTodo(x)?(fleet?1:2):dueSoon(x)?0:3,all=[...ready.map(x=>[x,rank(x)]),...needs.map(x=>[x,rank(x,1)])];
 return [0,1,2,3].flatMap(r=>{const l=all.filter(([,k])=>k===r).map(([x])=>x);return r%3?l:l.sort(openOrder)})}
// A to-do that looks done already: its run found it done, or a later message suggests it's handled (LOOKS_DONE_SQL in
// assistant.py). It waits in one quiet group above Done (lookDoneList), is never late and never counts as waiting for
// you. Only you close it.
// Its run's saved outcome ({} when none or unreadable), and the state it says (already_done, waiting, answered…)
const outOf=s=>{try{return JSON.parse(s.outcome||'{}')||{}}catch{return {}}},outState=s=>outOf(s).state;
const looksDone=s=>!closed(s)&&s.status!=='snoozed'&&(!!s.handled_hint||s.status==='prepared'&&outState(s)==='already_done');
// Waiting on others: its run found a step still open on someone else's side (outcome waiting: a review, merge, deploy, a
// reply). Nothing is ready for you there, so it sits in its own folded group above Coming back later and never counts.
// A new message on it (assistant.py update_card) makes it an open to-do again. Same rule as waits_on_others().
const waitsOnOthers=s=>!closed(s)&&s.status==='prepared'&&!looksDone(s)&&outState(s)==='waiting';
const taskActions=s=>{const choices=s?.next_actions||(s?.next_action?.kind==='menu'?s.next_action.actions:s?.next_action?[s.next_action]:[]);const ready=choices.some(a=>[...SENDS,'email_demo','merge','finish','handoff','calendar','doc_write','linear'].includes(a.kind));return choices.filter(a=>a.kind!=='prepare'||(!ready&&!/^Draft (shorter|longer|another|alternative|follow-up)\b/i.test(a.label||'')))};
// Under way or done, so no Send. An unconfirmed send checked long enough (retry_ok) may be sent again by the owner.
const sendBusy=a=>['queued','sending','sent','uncertain','local_preparation','paused','undoing','undone'].includes(a?.status)&&!a?.retry_ok;
// A Daily digest (todos-digest.js) and a meeting briefing (meeting_prep.py) are only for reading: To read, calm, not
// counted as needing the owner; Done leads, then Snooze and Not needed. A briefing's promises and questions have their own to-dos.
const toRead=s=>(!!s.digest||!!s.briefing)&&s.status==='pending';
// A cleanup to-do with every row decided: finished, like a ready result
const cleanupSettled=s=>!!s.cleanup?.items?.length&&!closed(s)&&s.status==='pending'&&s.cleanup.items.every(i=>!/^(open|working)$/.test(i.state));
// Prepared with nothing ready to approve, only a need of the owner's (needs_owner, machine/cards.py): Needs you too
const needsDecision=s=>s.status==='pending'&&!s.digest&&!s.briefing&&!cleanupSettled(s)||s.needs_owner||(!closed(s)&&s.status!=='snoozed'&&s.preparation_status==='blocked');
// An open to-do's chip in For you: needs (Needs you), ready (Prepared), read (To read) or preparing (Preparing…). All sit in For you.
const placeOf=s=>needsDecision(s)?'needs':toRead(s)?'read':s.status==='prepared'||cleanupSettled(s)?'ready':'preparing';
const DRAFT_KINDS=[...SENDS,'email_demo','handoff','finish','calendar','doc_write','linear'];
// Still needed? (still_needed.py): a to-do untouched for a week asks once, with the weekly recap's Not needed and Keep. Not needed is
// the to-do's own Not needed (with its Undo); Keep never asks again. Unanswered a week more, it folds into Coming back later (setAside).
// Its line on the to-do is drawn by the lazy part 'older' (todos-older.js stillNeeded), the old to-dos' part.
const stillAsks=s=>!!s.still_needed&&!closed(s)&&s.status!=='snoozed'&&!looksDone(s)&&!waitsOnOthers(s);
const setAside=s=>stillAsks(s)&&!!s.still_needed.folded;
// Older (still_needed.older): nothing new on it for a week, not urgent, not due soon and no send on its way. It waits in
// Older under For you, where Dismiss all closes them all (todos-older.js); a new message or a tap of the owner's brings it back.
const isOlder=s=>!!s.older&&!dueSoon(s)&&!fuBusy(s);
// The board's follow-ups as one to-do: "8 follow-ups ready for <board>" once one is written, else
// "Follow-ups for <board>", in For you either way. Each is in it from the start, also alone: never a to-do of its own in any list, so a board
// with follow-ups on is one to-do to review, not one per email. While drafts are written it says "Writing 3 follow-ups…".
// One that got stuck (needs the owner's help) stays a to-do of its own. A project's own follow-up (not grouped) is a
// normal to-do. Follow-ups on their way in a batch (spaced 30-45 s per mailbox) show as one progress to-do per board
// instead (fuSendingCard).
// Queued or on its way: out of the ready to-do at once. A follow-up's draft can sit in a menu, so its own state counts too.
const fuBusy=s=>sendBusy(s.action_status)||taskActions(s).some(a=>DRAFT_KINDS.includes(a.kind)&&sendBusy(a.state));
function fuSplit(ready,needs){fuGroups.clear();const groups={},member=s=>typeof s!=='string'&&!(s instanceof SafeHTML)&&s.follow_up?.group&&s.follow_up.state==='open'&&!fuBusy(s)&&!needsDecision(s);
 const batch=new Set((state.follow_up_progress||[]).filter(p=>p.going).map(p=>p.group||'own')),inBatch=s=>s.follow_up&&fuBusy(s)&&batch.has(s.follow_up.group||'own');
 for(const s of [...ready,...needs])if(member(s))(groups[s.follow_up.group]??=[]).push(s);
 const grouped=new Set(Object.values(groups).flat().map(s=>s.id)),cards=Object.entries(groups).map(([g,l])=>[l.some(s=>s.status==='prepared'),fuGroupCard(g,l)]);
 const out=list=>list.filter(s=>typeof s==='string'||s instanceof SafeHTML||!grouped.has(s.id));
 return {ready:[...cards.filter(([r])=>r).map(([,c])=>c),...cards.filter(([r])=>!r).map(([,c])=>c),...out(ready).filter(s=>!inBatch(s))],needs:out(needs)}}
// The sidebar lists a board's group as one row that opens the review
const fuGroups=new Map();
function fuSide(items){return items.map(x=>fuGroups.has(x)?fuGroups.get(x):x)}
const fuGroupTitle=all=>{const n=all.filter(s=>s.status==='prepared').length,board=all[0].follow_up.board||'';return n?t(['{} follow-up ready for {}','{} follow-ups ready for {}'],n,board):t('Follow-ups for {}',board)};
// The Fleet's items that need the owner, in their order: what each is, its own row and its title.
const FLEET_QUIET=['brief'],FAMILY_REQ=['todo','event'],FLEET_REQ=['intro','handoff'];
function fleetRows(f){if(!f?.on)return[];const out=[],add=(kind,row,title,id='fleet-'+row.id)=>out.push({kind,id,row,title}),net=f.network;
 for(const n of (f.notices||[]).filter(n=>n.buttons.length))add('notice',n,n.text);
 // Brief asks wait quietly in the Fleet tab (fleetBriefAsks)
 for(const w of (f.waiting||[]).filter(w=>!FLEET_QUIET.includes(w.kind)))
  FAMILY_REQ.includes(w.kind)?add('family',w,t(w.kind==='todo'?'{} asks you to do something':'{} proposes a plan',w.name))
  :FLEET_REQ.includes(w.kind)?add('request',w,t(w.kind==='intro'?'{} asks you for an intro':'{} hands you something',w.name))
  :w.kind==='question'?add('free',w,t('{} asks your Machine',w.name)):w.kind==='anything'?add('free',w,`${w.name} asks your Fleet`)
  :add('ask',w,`${t('{} asks:',w.name)} ${w.question}`);
 // The Team Graph's OKs: only a confirmed admin's Machine gets them, and one admin's answer counts for the whole team
 const gname=p=>p.fleet_name||(f.fleets||[]).find(x=>x.kind==='work'&&x.id===p.fleet)?.name||'';
 const graphAsk={member:p=>t('{} joined {}. Share the team\'s Graph with them?',p.name,gname(p)),optout:p=>t('{} asks to stop sharing their Work with the team.',p.name),admin:p=>t('Confirm {} as an admin of {}?',p.name,gname(p))};
 for(const p of (f.shared?.prompts||[]).filter(p=>graphAsk[p.kind]))add('graph',p,graphAsk[p.kind](p),'fleet-share-'+p.id);
 // Finding people you know on the Network (discovery.py): a permission card once, then one per person, only with a concrete reason
 if(net&&f.friends?.id){if(net.find==null&&!net.asked)add('netask',net,'Which of your contacts have a Machine?','net-ask');
  for(const p of (net.people||[]).filter(p=>p.status==='new'&&p.reasons.length))add('net',p,`${p.name} is on the Network`,'net-'+p.username)}
 return out}
// All, Work or Personal (state.locale.todo_scope)
const scopeShown=(list,scope)=>list.filter(s=>scope==='all'||s.scope===scope);
// The lists of To-dos, from the to-dos shown (Work or Personal alone, or all) and the Fleet's items.
function todoLists(shown,fleet=[],lead){
 const outstanding=shown.filter(s=>!closed(s)&&s.status!=='snoozed').sort(openOrder),later=shown.filter(s=>s.status==='snoozed'),finished=shown.filter(closed);
 const lookDone=outstanding.filter(looksDone),waitingOn=outstanding.filter(waitsOnOthers),open=outstanding.filter(s=>!looksDone(s)&&!waitsOnOthers(s)&&!setAside(s));
 // Still needed? without an answer: folded into Coming back later, under its own heading
 later.push(...outstanding.filter(setAside));
 // Nothing new on it for a week (isOlder): out of For you into Older below it; still open, so the badge counts it
 const older=open.filter(isOlder),young=open.filter(s=>!isOlder(s));
 // For you: prepared, needing the owner and still preparing alike (placeOf is only its chip)
 const needs=[...fleet,...young.filter(s=>placeOf(s)==='needs')],ready=young.filter(s=>placeOf(s)!=='needs');
 const leadFirst=l=>{const i=lead?l.findIndex(s=>s?.id===lead):-1;if(i>0)l.unshift(...l.splice(i,1));return l};
 // a board's follow-ups are one to-do (fuGroupCard)
 const fuv=fuSplit(ready,needs);
 fuv.foryou=leadFirst(forYouList(fuv.ready,fuv.needs));
 return {outstanding,later,finished,lookDone,waitingOn,open,older,needs,ready,fuv,leadFirst}}
// A snooze whose time has passed is over, whatever the Machine's last answer said. When the next one ends.
function wakeDue(list){const now=Date.now();let next=Infinity;for(const s of list||[]){if(s.status!=='snoozed'||!s.snoozed_until||s.send_later)continue;const at=Date.parse(s.snoozed_until);
  if(at<=now)Object.assign(s,{status:TODO.OPEN_NOT_SNOOZED.includes(s.resume_status)?s.resume_status:'pending',snoozed_until:null,resume_status:null});else next=Math.min(next,at)}
 return next}
const statusRow=x=>x&&typeof x==='object'&&!Array.isArray(x)&&Object.keys(x).length===1&&'='in x;
// The whole answer again from the one held (with its _token) and the changes since it; null when they don't fit
// (another token, a row it doesn't have). Also the Graph tab's overview (deltaGet).
function deltaJoin(held,r){if(!held||r._since!==held._token)return null;
 const out={...held};for(const k of r._gone||[])delete out[k];
 for(const[k,v]of Object.entries(r)){if(k==='_since'||k==='_gone')continue;
  if(Array.isArray(v)&&v.some(statusRow)){const was=new Map((held[k]||[]).map(x=>[typeof x?.id+':'+x?.id,x]));out[k]=v.map(x=>statusRow(x)?was.get(typeof x['=']+':'+x['=']):x);if(out[k].includes(undefined))return null}
  else out[k]=v}
 return out}
