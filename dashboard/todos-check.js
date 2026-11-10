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
function checkLine(c){ const last=checkClock(c.reviewed),next=c.waiting&&!c.soon&&c.next_review&&new Date(c.next_review)>Date.now()?checkClock(c.next_review):'',soon=c.waiting&&!next;
 const line=last?(next?t('Checked {} · next by {}',last,next):soon?t('Checked {} · next soon',last):t('Checked {}',last))
  :next?t('Next check by {}',next):soon?t('Next check soon'):'';
 return c.waiting?[line,t('{} new (a message)',c.waiting).replace(/ /g,'\u00a0')].filter(Boolean).join(' · '):line}
// The robot's lines, 2 or 3 per state, one per day (sayToday). The 'ok' ones never repeat the mail check line over
// the list ("Checked 6 new emails at 14:10 · nothing needs you", todos-mail-check.js): no checking, no "nothing needs you".
const CLEAR_SAY={busy:['Snooping around your messages…','Rummaging through the new stuff…'],ok:['All caught up.','All quiet. Back to my nap.','Clean slate. Time for a nap.'],
 late:['Dozed off. Last look at {}.','Overslept a little. Last look at {}.'],failed:['Tripped over something. That check failed.','Oops, that check went sideways.'],first:['Haven’t snooped around yet.']};
const sayToday=(k,...v)=>{const day=Math.floor((Date.now()-new Date().getTimezoneOffset()*6e4)/864e5);return t(CLEAR_SAY[k][day%CLEAR_SAY[k].length],...v)};
// While it runs, the head and the robot say the same, in the robot's voice: how many new messages when known.
function checkBusyLine(c){return c.waiting?t(['Nosing through {} new message…','Nosing through {} new messages…'],c.waiting):sayToday('busy')}
// The check's state, from state.check alone, so everything that shows it agrees: 'busy' while a check, a review or a
// first import runs (whoever started it: the button, the usual rhythm, the first look), 'said' for a few seconds after a
// press ended, 'first' before the first check, 'failed', 'late' (messages wait well past the next check's time), or
// 'ok'. line: the head's words for it (while it runs, the robot's own); nothing for 'ok' (the details are on
// Connections, Checks).
const LATE=10*6e4;
function checkNow(){const c=state?.check;if(!c||shownCached)return null;
 if(c.phase||c.reviewing||c.reading)return {kind:'busy',line:checkBusyLine(c)};
 if(Date.now()<checkSaid)return {kind:'said',line:checkResult(c)};
 if(!c.reviewed)return {kind:'first',line:checkLine(c)};
 const w=state.review_health?.worker;
 if(w&&!w.review_saved&&!['ok','starting','running','recovering'].includes(w.status))return {kind:'failed',line:t('The last check failed.')};
 if(c.waiting&&c.next_review&&Date.now()-new Date(c.next_review)>LATE)return {kind:'late',line:t('Last checked {}. The next check is late.',checkClock(c.reviewed))};
 return {kind:'ok',line:''}}
function checkBusy(){return checkNow()?.kind==='busy'}
// The button: never while a check runs (a press adds nothing then; the line says it runs).
function checkButton(){return html`<button type="button" class="check-btn quiet" data-check-now>${t('Check now')}</button>`}
// The head, with to-dos open: one small line only while it runs (no button then: a press adds nothing), just after a
// press, or when a check failed or is late, with Check now. Otherwise only a quiet Check now on a computer (none on a phone). During the first look its panel says
// what runs. With nothing open the robot says it instead (clearLine), so the head has none of it.
function checkHead(){const n=checkNow();if(!n||readsNothing()||$('#suggestions .all-clear .clear-check'))return '';
 const line=['busy','said','failed','late'].includes(n.kind)&&!(n.kind==='busy'&&!state.check.phase&&firstLookInfo(state.review_live||{}))?n.line:'';
 return html`<div class="check-now${line?'':' bare calm'}"><small class="check-line" role="status">${line}</small>${n.kind==='busy'?'':checkButton()}</div>`}
// All clear: the robot and its one line are the check's status, in its own voice. Asleep when all is well; awake and
// looking while a check runs; what a press found for a few seconds; and for the first check, a failed or a late one a
// line with a small Check now under it. The wording changes per day, not per render. Before anything was ever read
// (no check state), all clear would only mean nothing has come in yet.
// Before the very first to-do: what it reads and about when the first to-dos come (review_live.first_eta, the timing
// the setup page uses too), so someone new sees it is on its way, not a button to press. 0 when it isn't known.
const firstEta=()=>{const l=state?.review_live,m=+l?.first_eta|0;return m>0&&m<600&&!l?.cards?.count?m:0};
const firstEtaLine=()=>firstEta()&&+state.check?.waiting>0?t(['Nosing through {} new message. First to-dos in about {} min.','Nosing through {} new messages. First to-dos in about {} min.'],+state.check.waiting|0,firstEta()):'';
// Nothing that brings messages in is connected yet (a new Machine): an empty list means that, never a check that
// found nothing, and Check now has nothing to read. The Machine's own health row (gateway) brings in nothing.
const readsNothing=()=>!!state?.connectors&&!state.connectors.some(c=>c.service!=='gateway'&&c.signals!==false);
function clearLine(){const n=checkNow(),c=state?.check,say=k=>sayToday(k,checkClock(c?.reviewed));
 if(readsNothing()&&n?.kind!=='busy')return t('Nothing connected yet, so there’s nothing to read.');
 if(n&&['first','busy'].includes(n.kind)&&firstEtaLine())return firstEtaLine();
 if(!n)return state?.review_health?.last_completed?say('ok'):t('I’ll add something when it’s useful.');
 if(n.kind==='busy')return n.line;
 if(n.kind==='said')return c.found?n.line:t('Snooped around. Nothing new.');
 return say(n.kind)}
function clearPose(){const k=checkNow()?.kind;return k==='busy'||k==='first'&&firstEtaLine()?'brand/wave-look.webp':k==='failed'?'brand/sad.webp':'brand/sleepy.webp'}
// Under the line: Check now when the line asks for it; on 'ok' a tap on the line shows Check now and Details (clearOpen).
let clearOpen=false;
function clearCheck(){const n=checkNow();if(!n||readsNothing()||n.kind==='busy'||n.kind==='said'||n.kind==='ok'&&!clearOpen||n.kind==='first'&&firstEtaLine())return '';
 return html`<div class="check-row">${checkButton()}${n.kind==='ok'?html`<button type="button" class="quiet check-more" data-check-details>${t('Details')}</button>`:''}</div>`}
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
// Inbox zero: poke the sleeping robot a few times; the fourth poke offers a round of Catch the Zzz (todos-game.js).
const POKES=['Mmh… five more minutes.','I’m up! Nothing needs you right now.','Still nothing. That’s the dream.','Okay, okay. Fancy a round of Catch the Zzz?'],POKE_MORE=['Boop.','Hey, that tickles.','Zzz… oh, it’s you.','I was dreaming of an empty inbox. Oh wait.',
'Inbox zero. I peaked.','Shh. I’m defragmenting.','Rebooting… just kidding.','I run on electricity and your approval.','Please hold. Your poke is important to us.',
'404: tasks not found.','I’m not lazy, I’m in energy-saving mode.','Five more minutes. Robot minutes.','You poke, I wake. That’s the deal.',
'My to-do list is a haiku. Empty.','Reply all? Never heard of her.','I dreamt in binary again.','Low battery. High spirits.',
'Nobody needs you. In the nicest way.','I’m counting sheep. Electric ones.','Unsubscribe from poking?','Achievement unlocked: poked the robot.'];
let pokes=0,pokeLine='',pokeAwake=false,pokeTimer;
// The game is offered on the fourth poke, when the robot suggests it, not before.
const PLAY_AFTER=POKES.length,PLAY_BUTTON=html`<button class="play" type="button">▶ Play a mini game <small>Catch the Zzz · 20s</small></button>`;
function poke(){if(pokes<POKES.length)pokeLine=POKES[pokes];else{let next;do next=POKE_MORE[Math.floor(Math.random()*POKE_MORE.length)];while(next===pokeLine);pokeLine=next}pokes++;pokeAwake=true;localStorage.setItem('pokes-total',(+localStorage.getItem('pokes-total')||0)+1);$('#suggestions .poke-hint')?.remove();if(pokes>=PLAY_AFTER&&!$('#suggestions .all-clear .play'))$('#suggestions .all-clear')?.append(htmlNodes(PLAY_BUTTON));
const img=$('#suggestions .all-clear img.sleepy'),line=$('#suggestions .poke-line');if(line)line.textContent=pokeLine;if(img){img.src='brand/wave.webp';img.classList.remove('wobble');void img.offsetWidth;img.classList.add('wobble')}
clearTimeout(pokeTimer);pokeTimer=setTimeout(()=>{pokeAwake=false;pokeLine='';const i=$('#suggestions .all-clear img.sleepy'),l=$('#suggestions .poke-line');if(i)i.src=clearPose();if(l)l.textContent=clearLine()},6000)}
// All clear's line and pose follow the check (clearLine, clearPose above).
// Until the first poke, the robot sometimes mumbles a hint, so people find out they can;
// not on a fresh install, where "all clear" only means nothing has come in yet. Once you've poked
// three times (counted on this device), it hints at most once a week.
const POKE_HINTS=['Don’t poke the robot.','Please don’t poke me.','Zzz… no poking.'];
function pokeHint(){const b=$('#suggestions .all-clear .poke');if(!b||pokes||document.hidden||b.querySelector('.poke-hint')||!(state.suggestions||[]).some(closed))return;
if(+localStorage.getItem('pokes-total')>=3&&Date.now()-(+localStorage.getItem('poke-hint-at')||0)<7*864e5)return;localStorage.setItem('poke-hint-at',Date.now());
const h=document.createElement('span');h.className='poke-hint';h.setAttribute('aria-hidden','true');h.textContent=POKE_HINTS[Math.floor(Math.random()*POKE_HINTS.length)];b.append(h);setTimeout(()=>h.remove(),3400)}
setTimeout(pokeHint,4000);setInterval(()=>{if(Math.random()<.4)pokeHint()},25000);
$('#suggestions').addEventListener('click',e=>{if(e.target.closest('.all-clear .poke'))poke();else if(e.target.closest('.all-clear .play'))lazyRun('game',()=>openGame())});  // the game loads when first needed (todos-game.js)
