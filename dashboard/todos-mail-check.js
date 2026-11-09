// After a check that saw new email (state.mail_check, check_now.mail_check): one line above the to-dos, "Checked 12 new
// emails at 16:11 · nothing needs you", so new mail with no to-do reads as checked, not as broken. A tap opens one row
// per thread: who, the subject, and its new to-do (held until when, if it waits) or the check's reason it needed nothing.
// A lazy part (dashboard_parts.LAZY): shell-render.js mailCheckSlot loads it only while state.mail_check has email, and
// draws the list again once it's in (lazyRun).
let mailCheckOpen=false;
// When a held to-do comes: [tomorrow?, the time, or a weekday and the time]
const heldAt=v=>{const d=new Date(v),tm=new Date();tm.setDate(tm.getDate()+1);
 return localDay(d)===localDay(tm)?[true,fmtHM(d)]:[false,localDay(d)===localDay(new Date())?fmtHM(d):localeDate(d,DL,{weekday:'short'})+' '+fmtHM(d)]};
function mailCheckLine(m){const [tmw,when]=m.held&&m.held_until?heldAt(m.held_until):[],
 held=when?t(tmw?['{} to-do held until tomorrow {}','{} to-dos held until tomorrow {}']:['{} to-do held until {}','{} to-dos held until {}'],m.held,when):'';
 return [t(['Checked {} new email at {}','Checked {} new emails at {}'],m.emails,checkClock(m.at)),
  m.todos?(held&&m.held===m.todos?'':t(['{} new to-do','{} new to-dos'],m.todos)):t('nothing needs you'),held].filter(Boolean).join(' · ')}
function mailCheckWhy(r){if(r.todo){const [tmw,when]=r.held_until?heldAt(r.held_until):[];
  return html`<p class="mc-why mc-todo"><b>${when?t(tmw?'Held until tomorrow {}':'Held until {}',when):t('New to-do')}</b> <span translate="no">${r.todo}</span></p>`}
 return r.later?html`<p class="mc-why">${t('Read again in the next check')}</p>`:r.why?html`<p class="mc-why" translate="no">${r.why}</p>`:''}
const mailCheckRow=r=>html`<li><p class="mc-who"><b translate="no">${r.from||t('Unknown sender')}</b> <span translate="no">${r.subject||t('(no subject)')}</span></p>${mailCheckWhy(r)}</li>`;
function mailCheckBlock(){const m=state?.mail_check;if(!m?.emails||chatOpen()||firstLookInfo(state.review_live||{}))return '';
 return html`<div class="mail-check"><button type="button" class="mc-line" data-mail-check aria-expanded="${mailCheckOpen}">${raw(CHEVRON)}<span>${mailCheckLine(m)}</span></button>${mailCheckOpen?html`<ul class="mc-list">${m.threads.map(mailCheckRow)}${m.more?html`<li class="mc-more">${t(['And {} more thread','And {} more threads'],m.more)}</li>`:''}</ul>`:''}</div>`}
document.addEventListener('click',e=>{const b=e.target.closest('#suggestions [data-mail-check]');if(!b)return;mailCheckOpen=!mailCheckOpen;
 const box=b.closest('.mail-check'),next=mailCheckBlock();if(!box||!next)return;box.replaceWith(htmlNodes(next));$('#suggestions [data-mail-check]')?.focus()});
