// Check now (check_now.py), in the To-dos page head: when messages were last checked and when the next check is due, and
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
// One signal while it runs: the line says what it does; the button only greys out with a small spinner. Busy too while
// a check or a first import runs that the button didn't start (the first look, the usual rhythm): a press adds nothing
// then. During the first look its panel says what it does, so the line stays empty.
function checkHead(){const c=state?.check;if(!c||shownCached)return '';const busy=!!(c.phase||c.reviewing||c.reading),first=!c.phase&&firstLookInfo(state.review_live||{}),line=first?'':checkLine(c);
 // bare: no line, so on a narrow screen the button stays on the hello's row instead of a row of its own
 return html`<div class="check-now${line?'':' bare'}"><small class="check-line" role="status">${line}</small><button type="button" class="check-btn${busy?' busy':''}" data-check-now${busy?html` disabled aria-busy="true"`:''}>${busy?html`<span class="spin" aria-hidden="true"></span>`:''}${t('Check now')}</button></div>`}
// The head and the all-clear line ("Peeked at everything…", hidden while a check runs) follow the check at once.
function checkDraw(){pageHead();const l=$('#suggestions .all-clear .poke-line');if(l&&!pokeLine)l.textContent=clearLine()}
// The result stays in the head's line for a few seconds, where the press was: a toast would cover a to-do on a phone.
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
