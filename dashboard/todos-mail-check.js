// After a check that saw new messages (state.mail_check, check_now.mail_check), from every source it read (email,
// chats, phone notifications, the rest): one line above the to-dos, "Checked 13 messages at 16:11 · nothing needs you",
// so new messages with no to-do read as checked, not as broken. A tap opens one row per thread or chat: its source's
// one-color mark (todos-logos.js: Gmail or Outlook by its account, a phone notification by its app), who, the subject or first words, and its new to-do (held until when, if it waits) or the
// check's reason it needed nothing; a row opens its newest message in the message viewer (openEvent).
// A lazy part (dashboard_parts.LAZY): shell-render.js mailCheckSlot loads it only while state.mail_check read something,
// and draws the list again once it's in (lazyRun).
let mailCheckOpen=false;
// When a held to-do comes: [tomorrow?, the time, or a weekday and the time]
const heldAt=v=>{const d=new Date(v),tm=new Date();tm.setDate(tm.getDate()+1);
 return localDay(d)===localDay(tm)?[true,fmtHM(d)]:[false,localDay(d)===localDay(new Date())?fmtHM(d):localeDate(d,DL,{weekday:'short'})+' '+fmtHM(d)]};
// What it read, one total in a neutral word whatever the sources: never longer than the email-only line was, so it stays
// one line on a phone in every language; the list's icons say which source each row came from
const mailCheckRead=m=>t(['Checked {} message at {}','Checked {} messages at {}'],m.read,checkClock(m.at));
function mailCheckLine(m){const [tmw,when]=m.held&&m.held_until?heldAt(m.held_until):[],
 held=when?t(tmw?['{} to-do held until tomorrow {}','{} to-dos held until tomorrow {}']:['{} to-do held until {}','{} to-dos held until {}'],m.held,when):'';
 return [mailCheckRead(m),m.todos?(held&&m.held===m.todos?'':t(['{} new to-do','{} new to-dos'],m.todos)):t('nothing needs you'),held].filter(Boolean).join(' · ')}
function mailCheckWhy(r){if(r.todo){const [tmw,when]=r.held_until?heldAt(r.held_until):[];
  return html`<span class="mc-why mc-todo"><b>${when?t(tmw?'Held until tomorrow {}':'Held until {}',when):t('New to-do')}</b> <span translate="no">${r.todo}</span></span>`}
 return r.later?html`<span class="mc-why">${t('Read again in the next check')}</span>`:r.why?html`<span class="mc-why" translate="no">${r.why}</span>`:''}
// Read like an inbox: the source's icon, who (a person, or an app by name; a Slack DM with no name yet as "Slack DM"),
// how many new messages when more than one (the rows add up to the line's total), the subject or first words in a quieter
// color, and the time. An email always names its sender and subject (Unknown sender when a chat or update has nothing).
function mailCheckRow(r){const mail=!r.source||r.source==='email',who=(r.from&&sender(r.from))||(r.dm?t('Slack DM'):mail||!r.subject?t('Unknown sender'):''),what=r.subject||(mail?t('(no subject)'):''),at=checkClock(r.at);
 const body=html`<span class="mc-top"><span class="mc-who">${r.kind?html`<span class="mc-src"><span class="icon">${markIco(sourceMark(r.kind,r.account,r.app))}</span></span>`:''}${who?html`<b translate="no">${who}</b>`:''}${r.n>1?html`<span class="mc-n" title="${t(['{} message','{} messages'],r.n)}"> (${r.n})</span>`:''} <span class="mc-what" translate="no">${what}</span></span>${at?html`<time class="mc-at">${at}</time>`:''}</span>${mailCheckWhy(r)}`;
 return html`<li>${r.event!=null?html`<button type="button" class="mc-row" data-mc-event="${r.event}">${body}</button>`:body}</li>`}
// The first MC_SHOWN rows, the rest behind "Show N more": every thread the check read can be seen
const MC_SHOWN=10;let mailCheckAll=false;
function mailCheckBlock(){const m=state?.mail_check;if(!m?.read||chatOpen()||firstLookInfo(state.review_live||{}))return '';
 const rows=m.threads||[],hidden=mailCheckAll||rows.length<=MC_SHOWN+1?0:rows.length-MC_SHOWN;
 return html`<div class="mail-check"><button type="button" class="mc-line" data-mail-check aria-expanded="${mailCheckOpen}">${raw(CHEVRON)}<span>${mailCheckLine(m)}</span></button>${mailCheckOpen?html`<ul class="mc-list">${(hidden?rows.slice(0,MC_SHOWN):rows).map(mailCheckRow)}${hidden?html`<li class="mc-more"><button type="button" class="mc-all" data-mc-all>${t('Show {} more',hidden)}</button></li>`:m.more?html`<li class="mc-more">${t(['And {} more thread','And {} more threads'],m.more)}</li>`:''}</ul>`:''}</div>`}
document.addEventListener('click',e=>{const row=e.target.closest('#suggestions [data-mc-event]');if(!row)return;
 // the subject while it loads; the viewer then titles it by the message itself (an email's subject, a chat's name)
 openEvent(row.dataset.mcEvent,row.querySelector('.mc-what')?.textContent.trim()||'')});
document.addEventListener('click',e=>{const b=e.target.closest('#suggestions [data-mail-check],#suggestions [data-mc-all]');if(!b)return;
 const all=b.hasAttribute('data-mc-all');if(all)mailCheckAll=true;else{mailCheckOpen=!mailCheckOpen;mailCheckAll=false}
 const box=b.closest('.mail-check'),next=mailCheckBlock();if(!box||!next)return;box.replaceWith(htmlNodes(next));
 // after Show more, focus moves to the first row it showed
 (all?document.querySelectorAll('#suggestions .mc-list > li')[MC_SHOWN]?.querySelector('button'):$('#suggestions [data-mail-check]'))?.focus()});
