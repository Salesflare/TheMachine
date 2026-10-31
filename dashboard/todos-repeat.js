// Recurring to-dos (recurring.py, docs/help/recurring.md): a to-do that comes back on a rhythm. One short line on the
// to-do ("Repeats monthly on the first Monday", and "missed 1" when dates passed while it stayed open); Repeat and Skip
// this one in its More menu; Repeats in New to-do; "repeat this every month" or "stop repeating" in its chat; and the
// one-time "Make this a recurring to-do?" above the list. Nothing is made or sent without the owner's tap.
const REPEAT_ICON='<svg class="ci" viewBox="0 0 24 24" aria-hidden="true"><path d="M17 3.5l3 3-3 3M20 6.5H8.5A4.5 4.5 0 0 0 4 11v.5M7 20.5l-3-3 3-3M4 17.5h11.5A4.5 4.5 0 0 0 20 13v-.5"/></svg>';
const REPEAT_NTH={1:'Repeats monthly on the first {}',2:'Repeats monthly on the second {}',3:'Repeats monthly on the third {}',4:'Repeats monthly on the fourth {}','-1':'Repeats monthly on the last {}'};
const REPEAT_NTH_OPTION={1:'Monthly on the first {}',2:'Monthly on the second {}',3:'Monthly on the third {}',4:'Monthly on the fourth {}','-1':'Monthly on the last {}'};
const rpDate=iso=>new Date(String(iso).slice(0,10)+'T12:00');
const rpWeekday=d=>d.toLocaleDateString(DL,{weekday:'long'});
const rpMonthDay=d=>d.toLocaleDateString(DL,{day:'numeric',month:'long'});
// Which weekday of its month a day is: 1 to 4, or -1 for a fifth one (always the last)
const rpNth=d=>d.getDate()>28?-1:Math.floor((d.getDate()-1)/7)+1;
function repeatText(rule,anchor){if(!rule)return '';const d=rpDate(anchor),n=rule.n||1,wd=rpWeekday(d);
 if(rule.unit==='weekday')return t('Repeats on weekdays');
 if(rule.unit==='day')return n===1?t('Repeats daily'):t('Repeats every {} days',n);
 if(rule.unit==='week')return n===1?t('Repeats weekly on {}',wd):t('Repeats every {} weeks on {}',n,wd);
 if(rule.unit==='year')return t('Repeats yearly on {}',rpMonthDay(d));
 if(n>1)return t('Repeats every {} months',n);
 return rule.nth!=null?t(REPEAT_NTH[rule.nth],wd):t('Repeats monthly on day {}',d.getDate())}
// The choices, from the date the to-do is for (its due date, else today): the weekday, day and date come from it
function repeatOptions(base){const d=rpDate(base),wd=rpWeekday(d),nth=rpNth(d);
 return [[{unit:'day',n:1},t('Daily')],[{unit:'weekday',n:1},t('Weekdays')],[{unit:'week',n:1},t('Weekly on {}',wd)],
  [{unit:'month',n:1},t('Monthly on day {}',d.getDate())],[{unit:'month',n:1,nth},t(REPEAT_NTH_OPTION[nth],wd)],[{unit:'year',n:1},t('Yearly on {}',rpMonthDay(d))]]}
const rpSame=(a,b)=>!!a&&!!b&&a.unit===b.unit&&(a.n||1)===(b.n||1)&&(a.nth??null)===(b.nth??null);
// The to-do's one line: a quiet chip that opens Repeat
const repeatChip=s=>{const r=s.repeats;if(!r||closed(s))return '';const text=repeatText(r.rule,r.anchor)+(r.missed?' · '+t('missed {}',r.missed):'');
 return `<button type="button" class="chip scope repeat${r.missed?' missed':''}" data-repeat="${esc(s.id)}" title="${esc(t('Change how it repeats'))}">${REPEAT_ICON}<span>${esc(text)}</span></button>`};
// More: Repeat (or Change repeat), and Skip this one while it repeats
const repeatMore=s=>closed(s)?'':`<button type="button" class="ghost" data-repeat="${esc(s.id)}">${s.repeats?'Change repeat':'Repeat'}</button>${s.repeats?`<button type="button" class="ghost" data-repeat-skip="${esc(s.id)}">Skip this one</button>`:''}`;
async function repeatPost(action,args){return request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})})}
// Custom…: a rhythm in words ("every 2 weeks", "every last Friday"), read by the Machine; Enter or the line sets it
function repeatCustom(box,set){const wrap=box.querySelector('.rp-custom'),input=wrap.querySelector('input'),read=wrap.querySelector('.nc-read');let timer,got=null;
 wrap.hidden=false;input.focus();
 const look=async()=>{const q=input.value.trim();got=null;if(q.length<3){read.textContent='';return}
  try{const r=await repeatPost('repeat_read',{text:/^(every|each)\b/i.test(q)?q:'every '+q});if(input.value.trim()!==q)return;
   if(r.rule){got=r;const b=document.createElement('button'),k=document.createElement('small');b.type='button';b.className='link';b.dataset.rpSet='';b.textContent=repeatText(r.rule,r.anchor);k.textContent=t('Enter sets it');read.replaceChildren(b,' ',k)}
   else read.textContent=t('I can’t read that yet. Try every 2 weeks or every last Friday.')}catch(e){errCaught(e)}};
 input.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(look,250)});
 input.addEventListener('keydown',async e=>{if(e.key!=='Enter'||e.isComposing)return;e.preventDefault();clearTimeout(timer);if(!got)await look();if(got)set(got.rule,got.anchor)});
 read.addEventListener('click',e=>{if(e.target.closest('[data-rp-set]')&&got)set(got.rule,got.anchor)})}
const rpListHTML=(base,cur)=>`<div class="rp-list" role="group" aria-label="${esc(t('How often'))}">${repeatOptions(base).map(([r,label],i)=>`<button type="button" data-rp="${i}" aria-pressed="${rpSame(r,cur)}">${esc(label)}</button>`).join('')}<button type="button" data-rp="custom">${esc(t('Custom…'))}</button></div><div class="rp-custom" hidden><input type="text" autocomplete="off" aria-label="${esc(t('How often?'))}" placeholder="${esc(t('Every 2 weeks, every last Friday'))}"><p class="nc-read" aria-live="polite"></p></div>`;
// More > Repeat on a to-do: a small box in the to-do, like Change project
function repeatPick(id,anchor){const s=(state.suggestions||[]).find(x=>x.id===id);if(!s||closed(s))return;document.querySelector('.repeat-picker')?.remove();
 const r=s.repeats,base=r?.due||s.due||localDay(new Date());
 const box=document.createElement('div');box.className='project-picker repeat-picker';box.setAttribute('role','dialog');box.setAttribute('aria-label',t('Repeat'));
 box.innerHTML=`<p class="rp-head">${REPEAT_ICON}<span>${esc(r?repeatText(r.rule,r.anchor):t('Repeat this to-do'))}</span></p>${rpListHTML(base,r?.rule)}<div class="actions">${r?`<button type="button" class="ghost" data-rp-act="stop">${esc(t('Stop repeating'))}</button>`:''}<button type="button" class="quiet" data-rp-act="cancel">${esc(t('Cancel'))}</button></div>`;
 anchor.closest('details.more-actions,details.chat-menu')?.removeAttribute('open');(anchor.closest('.card')||anchor.closest('.chat-main')||document.body).appendChild(box);box.querySelector('button[aria-pressed="true"],button')?.focus();
 const set=async(rule,repeat=rule)=>{box.querySelectorAll('button').forEach(b=>b.disabled=true);
  try{const got=await repeatPost('card_repeat',{suggestion_id:id,repeat});const x=(state.suggestions||[]).find(y=>y.id===id);if(x)x.repeats=got.repeats||undefined;box.remove();
   toast(got.repeats?repeatText(got.repeats.rule,got.repeats.anchor)+'.':t('Stopped repeating.'));if(typeof render==='function')render();refresh()}
  catch(err){errCaught(err);box.querySelectorAll('button').forEach(b=>b.disabled=false);toast(err.message,true)}};
 box.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();box.remove()}});
 box.onclick=e=>{const b=e.target.closest('[data-rp],[data-rp-act]');if(!b)return;
  if(b.dataset.rpAct==='cancel'){box.remove();return}if(b.dataset.rpAct==='stop'){set(null,'none');return}
  if(b.dataset.rp==='custom'){repeatCustom(box,rule=>set(rule));return}set(repeatOptions(base)[+b.dataset.rp][0])}}
async function repeatSkip(id,b){if(b)b.disabled=true;b?.closest('details')?.removeAttribute('open');
 try{const got=await repeatPost('card_repeat_skip',{suggestion_id:id});toast(got.next?t('Skipped. The next one comes {}.',rpDate(got.next).toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'})):t('Skipped.'));await refresh()}
 catch(err){errCaught(err);if(b)b.disabled=false;toast(err.message,true)}}
document.addEventListener('click',e=>{const b=e.target.closest('[data-repeat]');if(b){e.preventDefault();repeatPick(b.dataset.repeat,b);return}
 const k=e.target.closest('[data-repeat-skip]');if(k){e.preventDefault();repeatSkip(k.dataset.repeatSkip,k)}});
// New to-do's Repeats chip and its choices (new-todo.js): from the due date when one is set, else today
const ncRepeatBase=()=>ncISO(nc.due||new Date());
const ncRepeatChip=()=>nc.repeat?`<button type="button" class="set" data-nc="repeat">${esc(repeatText(nc.repeat,ncRepeatBase()))}<span class="x" data-nc-drop="repeat:0" aria-label="${esc(t('Doesn’t repeat'))}">×</span></button>`:`<button type="button" data-nc="repeat" aria-expanded="${nc.pick==='repeat'}">${esc(t('Repeats'))}</button>`;
function ncRepeatPick(box){box.innerHTML=rpListHTML(ncRepeatBase(),nc.repeat);
 const set=rule=>{nc.repeat=rule;ncPick(null);$('#nc-text').focus()};
 box.querySelector('[data-rp]')?.focus();
 box.querySelector('.rp-list').addEventListener('click',e=>{const b=e.target.closest('[data-rp]');if(!b)return;if(b.dataset.rp==='custom'){repeatCustom(box,rule=>set(rule));return}set(repeatOptions(ncRepeatBase())[+b.dataset.rp][0])});
 box.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopPropagation();ncPick(null);$('#nc-text').focus()}})}
// A due date moved after "Monthly on the first Monday": the same kind of day from the new date
function ncRepeatFollow(){if(nc.repeat?.nth!=null&&nc.due)nc.repeat={...nc.repeat,nth:rpNth(nc.due)}}
// The to-do's chat: "repeat this every first Monday", "make it repeat monthly", "stop repeating" set it at once
const REPEAT_SAID=/^\s*(?:please\s+)?(?:(?:make|let|have)\s+(?:this|it)\s+)?(?:repeat|recur)(?:s|ing)?\b|^\s*(?:please\s+)?(?:stop|don'?t|do not)\s+(?:repeat|recurr?)/i;
async function repeatFromChat(s,text){if(!REPEAT_SAID.test(text)||closed(s))return false;
 try{const got=await repeatPost('card_repeat',{suggestion_id:s.id,words:text});toast(got.repeats?repeatText(got.repeats.rule,got.repeats.anchor)+'.':t('Stopped repeating.'));await refresh();return true}
 catch(err){errCaught(err);toast(err.message,true);return 'kept'}}
// "Make this a recurring to-do?": asked once, above the list, for what a learned note or a rhythm in done to-dos shows
const repeatOfferLine=()=>{const o=state.recurring_offer;if(!o||chatOpen())return '';
 return `<div class="repeat-offer" role="group" aria-label="${esc(t('Make this a recurring to-do?'))}"><p>${REPEAT_ICON}<span><b>${esc(t('Make this a recurring to-do?'))}</b> <span translate="no">${esc(o.title)}</span> · ${esc(repeatText(o.rule,o.anchor))}</span></p><div class="actions"><button type="button" class="ghost" data-rp-offer="yes">${esc(t('Make it recurring'))}</button><button type="button" class="quiet" data-rp-offer="no">${esc(t('No thanks'))}</button></div></div>`};
document.addEventListener('click',async e=>{const b=e.target.closest('[data-rp-offer]');const o=state.recurring_offer;if(!b||!o)return;e.preventDefault();b.disabled=true;
 try{const got=await repeatPost('recurring_offer',{key:o.key,choice:b.dataset.rpOffer,scope:scopeFilter==='work'||scopeFilter==='personal'?scopeFilter:null});state.recurring_offer=null;
  if(got.made){toast(repeatText(o.rule,o.anchor)+'.');await refresh()}else render()}
 catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
