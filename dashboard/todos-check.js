// Check now (check_now.py), in the To-dos page head or under the all-clear robot: a line when the check matters, and
// a button that reads every source now and starts a check of what came in, whatever the time of day. One check at a
// time: a press while one runs, or just after it ended, shows that one. While it runs the page looks every few seconds;
// when it ends the line says what it found. The phone app loads this same dashboard; chat runs `assistant check`.
let checkFollowing=false,checkSaid=0;  // checkSaid: until when the line says what the last check found
const checkClock=v=>{const d=v?new Date(v):null;return d&&!isNaN(d)?fmtHM(d):''};
const checkResult=c=>c?.found?t(['Checked. {} new to-do.','Checked. {} new to-dos.'],c.found):t('Checked. Nothing new.');
// The head says what the owner cares about: when messages were last checked for to-dos, when the next check is due
// (soon, once the batch is nearly full) and how many new ones wait: "Checked 21:10 · next by 21:26 · 2 new". Sources are read every few minutes in
// between.
function checkLine(c){if(c.phase||c.reviewing||c.reading)return t(c.phase==='reading'||!c.phase&&!c.reviewing?'Reading sources…':'Checking messages…');
 if(Date.now()<checkSaid)return checkResult(c);
 const last=checkClock(c.reviewed),next=c.waiting&&!c.soon&&c.next_review&&new Date(c.next_review)>Date.now()?checkClock(c.next_review):'',soon=c.waiting&&!next;
 const line=last?(next?t('Checked {} · next by {}',last,next):soon?t('Checked {} · next soon',last):t('Checked {}',last))
  :next?t('Next check by {}',next):soon?t('Next check soon'):'';
 return c.waiting?[line,t('{} new (a message)',c.waiting).replace(/ /g,'\u00a0')].filter(Boolean).join(' · '):line}
// The check's state, from state.check alone, so everything that shows it agrees: 'busy' while a check, a review or a
// first import runs (whoever started it: the button, the usual rhythm, the first look), 'said' for a few seconds after a
// press ended, 'first' before the first check, 'failed', 'late' (messages wait well past the next check's time), or
// 'ok'. line: the head's plain words for it; nothing for 'ok' (the details are on Connections, Checks). The robot says
// it in its own voice (clearLine).
const LATE=10*6e4;
function checkNow(){const c=state?.check;if(!c||shownCached)return null;
 if(c.phase||c.reviewing||c.reading)return {kind:'busy',line:checkLine(c)};
 if(Date.now()<checkSaid)return {kind:'said',line:checkResult(c)};
 if(!c.reviewed)return {kind:'first',line:checkLine(c)};
 const w=state.review_health?.worker;
 if(w&&!w.review_saved&&!['ok','starting','running','recovering'].includes(w.status))return {kind:'failed',line:t('The last check failed.')};
 if(c.waiting&&c.next_review&&Date.now()-new Date(c.next_review)>LATE)return {kind:'late',line:t('Last checked {}. The next check is late.',checkClock(c.reviewed))};
 return {kind:'ok',line:''}}
function checkBusy(){return checkNow()?.kind==='busy'}
// The button: while it runs it only greys out with a small spinner; a press adds nothing then.
function checkButton(quiet){const busy=checkBusy();return html`<button type="button" class="check-btn${quiet?' quiet':''}${busy?' busy':''}" data-check-now${busy?html` disabled aria-busy="true"`:''}>${busy?html`<span class="spin" aria-hidden="true"></span>`:''}${t('Check now')}</button>`}
// The head, with to-dos open: one small line only while it runs, just after a press, or when a check failed or is late,
// with Check now. Otherwise only a quiet Check now on a computer (none on a phone). During the first look its panel says
// what runs. With nothing open the robot says it instead (clearLine), so the head has none of it.
function checkHead(){const n=checkNow();if(!n||$('#suggestions .all-clear .clear-check'))return '';
 const line=['busy','said','failed','late'].includes(n.kind)&&!(n.kind==='busy'&&!state.check.phase&&firstLookInfo(state.review_live||{}))?n.line:'';
 return html`<div class="check-now${line?'':' bare calm'}"><small class="check-line" role="status">${line}</small>${checkButton(true)}</div>`}
// All clear: the robot and its one line are the check's status, in its own voice. Asleep when all is well; awake and
// looking while a check runs; what a press found for a few seconds; and for the first check, a failed or a late one a
// line with a small Check now under it. The wording changes per day, not per render. Before anything was ever read
// (no check state), all clear would only mean nothing has come in yet.
const CLEAR_SAY={busy:['Snooping around your messages…','Rummaging through the new stuff…'],ok:['Snooped around. Nothing needs you.','Peeked at everything. Nothing needs you.','All quiet. Back to my nap.'],
 late:['Dozed off. Last look at {}.','Overslept a little. Last look at {}.'],failed:['Tripped over something. That check failed.','Oops, that check went sideways.'],first:['Haven’t snooped around yet.']};
function clearLine(){const n=checkNow(),c=state?.check,day=Math.floor((Date.now()-new Date().getTimezoneOffset()*6e4)/864e5),say=k=>t(CLEAR_SAY[k][day%CLEAR_SAY[k].length],checkClock(c?.reviewed));
 if(!n)return state?.review_health?.last_completed?say('ok'):t('I’ll add something when it’s useful.');
 if(n.kind==='busy')return c.waiting?t(['Nosing through {} new message…','Nosing through {} new messages…'],c.waiting):say('busy');
 if(n.kind==='said')return c.found?n.line:t('Snooped around. Nothing new.');
 return say(n.kind)}
function clearPose(){const k=checkNow()?.kind;return k==='busy'?'brand/wave-look.webp':k==='failed'?'brand/sad.webp':'brand/sleepy.webp'}
// Under the line: Check now when the line asks for it; on 'ok' a tap on the line shows Check now and Details (clearOpen).
let clearOpen=false;
function clearCheck(){const n=checkNow();if(!n||n.kind==='busy'||n.kind==='said'||n.kind==='ok'&&!clearOpen)return '';
 return html`<div class="check-row">${checkButton(true)}${n.kind==='ok'?html`<button type="button" class="quiet check-more" data-check-details>${t('Details')}</button>`:''}</div>`}
document.addEventListener('click',e=>{const m=e.target.closest('#suggestions .all-clear [data-clear-more]');
 if(m){clearOpen=!clearOpen;m.setAttribute('aria-expanded',clearOpen);checkDraw();return}
 if(e.target.closest('#suggestions .all-clear [data-check-details]')){showTab('health');showHealthPane('reviews')}});
// The head and the all-clear (its robot, line and Check now) follow the check at once.
function checkDraw(){pageHead();const k=$('#suggestions .all-clear .clear-check');if(k)setHTML(k,clearCheck());
 const l=$('#suggestions .all-clear .poke-line'),i=$('#suggestions .all-clear img.sleepy');if(l&&!pokeLine)l.textContent=clearLine();
 if(i&&!pokeAwake){i.src=clearPose();i.alt=t(checkBusy()?'The Machine checking':'The Machine resting')}}
// The result stays where the press was for a few seconds (the head's line or the robot's): a toast would cover a to-do
// on a phone.
function checkSay(){checkSaid=Date.now()+8000;checkDraw();setTimeout(checkDraw,8100)}
async function checkFollow(){if(checkFollowing)return;checkFollowing=true;const until=Date.now()+35*6e4;
 try{while(state?.check?.phase&&Date.now()<until){await new Promise(r=>setTimeout(r,3000));await refreshWhenReady()}}
 finally{checkFollowing=false}
 if(!state?.check?.phase)checkSay()}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-check-now]');if(!b||b.disabled)return;b.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'check_now',args:{}})});
  if(!r?.check){toast(checkResult(null));b.disabled=false;return}
  state.check=r.check;if(r.check.phase){checkDraw();checkFollow()}else checkSay()}
 catch(err){errCaught(err);b.disabled=false;notice(err.message,true)}});
