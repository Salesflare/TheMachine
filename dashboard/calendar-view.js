// Calendar: an agenda that runs on through the days (later ones load as you scroll down, earlier ones as you scroll up
// or tap Earlier days), and on a computer also the calendar week, Monday to Sunday, as seven columns. It holds the
// meetings from the connected calendars, each with its card if one is about it, cards due or coming back that day,
// handoff check-ins and promises with a date. Read-only: viewing sends or changes nothing. A row opens its card's chat,
// the promise's page, or the meeting in its own calendar. Meetings load one calendar week (Monday to Monday) per ask
// and are kept for a minute. Today, ‹ › and the view switch stay on top; t, ← → (or k j), a and w do the same. The
// address holds the view and its week (#calendar?view=week&date=2026-10-26), so back and forward work.
const CAL_BACK=26,CAL_AHEAD=52;  // how many weeks the agenda runs back and ahead of this one
let calCals=[],calWeeks=new Map(),calMeetings=null,calReturn=false,calRouting=false,calBusy=null,calMoreFailed={},calUp=false,calLastY=0;
let calMode=['week','month'].includes(sideStore.get('cal-mode'))?sideStore.get('cal-mode'):'agenda';
const calMid=d=>{const x=new Date(d);x.setHours(0,0,0,0);return x};
const calAdd=(d,n)=>{const x=new Date(d);x.setDate(x.getDate()+n);x.setHours(0,0,0,0);return x};  // by calendar days, also over a clock change
const calOf=k=>{const [y,m,d]=String(k).split('-').map(Number);return new Date(y,m-1,d)};
const calMonday=d=>{const x=calMid(d);return calAdd(x,-((x.getDay()+6)%7))};
const calDay=n=>calAdd(calMid(new Date()),n);
const calFirst=d=>new Date(d.getFullYear(),d.getMonth(),1);
// The week on show (its Monday), the month (its 1st), a phone's three days (the first), and the agenda's days [from, to)
let calAt=calMonday(new Date()),calMonth=calFirst(new Date()),calStart=calDay(0),calFrom=calDay(0),calTo=calDay(7);
const calList=()=>calMode==='agenda',calThree=()=>calMode==='week'&&!DESK.matches;
const calMonthDays=m=>[calMonday(m),calAdd(calMonday(new Date(m.getFullYear(),m.getMonth()+1,0)),7)];  // Monday on or before the 1st to the Monday after the last Sunday
const calRange=()=>calMode==='month'?calMonthDays(calMonth):calMode==='week'?(DESK.matches?[calAt,calAdd(calAt,7)]:[calStart,calAdd(calStart,3)]):[calFrom,calTo];
const calMondays=(from,to)=>{const out=[];for(let d=calMonday(from);d<to;d=calAdd(d,7))out.push(d);return out};
function calFetchWeek(mon,force){const k=localDay(mon),w=calWeeks.get(k);if(w?.loading)return w.loading;
 if(w&&!w.failed&&!force&&Date.now()-w.at<60000)return Promise.resolve();
 const q='from='+encodeURIComponent(mon.toISOString())+'&to='+encodeURIComponent(calAdd(mon,7).toISOString());
 // Each week read is kept on the device too (encrypted, like the cards), so the Calendar opens offline with what it had
 const loading=request('api/calendar?'+q).then(r=>{if(Array.isArray(r?.calendars))calCals=r.calendars;calWeeks.set(k,{meetings:Array.isArray(r?.meetings)?r.meetings:[],failed:false,at:Date.now()});localCache.put('cal:'+k,r)})
  .catch(async e=>{if(e?.offline){const mine=w?.meetings&&!w.failed,hit=mine?null:await localCache.read('cal:'+k);
   if(mine||hit){if(hit){if(Array.isArray(hit.value?.calendars)&&!calCals?.length)calCals=hit.value.calendars;staleMark(hit.at)}
    calWeeks.set(k,{meetings:mine?w.meetings:Array.isArray(hit.value?.meetings)?hit.value.meetings:[],failed:false,at:0});return}}
   calWeeks.set(k,{meetings:w?.meetings||[],failed:true,at:Date.now()})}).finally(calUnion);
 calWeeks.set(k,{meetings:w?.meetings||null,failed:!!w?.failed,at:w?.at||0,loading});return loading}
// Every loaded week's meetings, each once (one that runs over a Monday comes in both weeks)
function calUnion(){const seen=new Set(),all=[];let any=false;for(const w of calWeeks.values()){if(!w.meetings)continue;any=true;for(const m of w.meetings)if(!seen.has(m.id)){seen.add(m.id);all.push(m)}}calMeetings=any?all:null}
const calFailedIn=(a,b)=>calMondays(a,b).some(d=>calWeeks.get(localDay(d))?.failed);
function calFetch(force){const [a,b]=calRange(),weeks=[...calMondays(a,b)],now=calMonday(new Date());if(!weeks.some(d=>+d===+now))weeks.push(now);return Promise.all(weeks.map(d=>calFetchWeek(d,force)))}
async function calendarView(force){calRender();await calFetch(force);calRender()}
// Everything with a date in [from, to), by local day ('overdue' for due dates already past, when today is in it)
function calItems(from=calDay(0),to=calDay(1)){const days=[];for(let d=calMid(from);d<to;d=calAdd(d,1))days.push(localDay(d));
 const week=new Set(days),today=localDay(new Date()),withToday=week.has(today),now=Date.now(),out=[],seen=new Set();
 const open=(state.suggestions||[]).filter(s=>!closed(s)),cardFor=id=>open.find(s=>eventIds(s).map(Number).includes(Number(id)));
 // Someone else's event on a calendar shared with the owner shows, marked as theirs, and never carries a card
 for(const m of calMeetings||[]){const s=m.shared?null:cardFor(m.id),a=new Date(m.start),b0=new Date(m.end);if(isNaN(a))continue;const b=isNaN(b0)||b0<=a?new Date(a.getTime()+1):b0;
  // All day, or a day or more (a trip): on every day it covers, as All day with its dates, never as times
  if(m.all_day||b-a>=864e5){const first=localDay(a),last=localDay(new Date(b-1)),span=first!==last?[first,last]:null;
   for(const k of days){const d=calOf(k);if(a<calAdd(d,1)&&b>d)out.push({day:k,kind:'meeting',allDay:true,at:0,m,s,span,promises:[]})}if(s)seen.add(s.id);continue}
  let day=localDay(a);if(day<days[0]&&b>from)day=days[0];if(!week.has(day))continue;if(s)seen.add(s.id);  // one still going at the start shows on the first day
  out.push({day,kind:'meeting',at:a.getTime(),m,s,past:b.getTime()<now,promises:[]})}
 for(const s of open){if(seen.has(s.id))continue;
  if(s.status==='snoozed'&&s.snoozed_until){const d=new Date(s.snoozed_until),day=localDay(d);if(week.has(day))out.push({day,kind:s.handoff_wait?'checkin':'back',at:d.getTime(),s});continue}
  if(s.due&&!(looksDone(s)&&s.due<today)&&(s.due<today?withToday:week.has(s.due)))out.push({day:s.due<today?'overdue':s.due,kind:'due',at:-1,s})}
 // One row per promise: said by both sides it is a plan made together, shown as the owner's ("With …"); one about a
 // meeting that day with the same person rides on that meeting's row
 const said=new Map();for(const p of state.promises||[]){if(p.state!=='open'||!p.due||!(p.due<today?withToday:week.has(p.due)))continue;
  const k=[p.who,p.what].map(v=>calNorm(v).split(/\s+/).join(' ')).join('\n'),was=said.get(k);
  if(!was){said.set(k,{...p});continue}if(was.direction!==p.direction)was.together=true;if(p.direction==='mine')Object.assign(was,{...p,together:was.together||p.together})}
 for(const p of said.values()){const on=p.due>=today&&out.find(it=>it.kind==='meeting'&&!it.m.shared&&it.day===p.due&&calWith(p,it.m));
  if(on)on.promises.push(p);else out.push({day:p.due<today?'overdue':p.due,kind:'promise',at:-1,p})}
 out.sort((x,y)=>(x.allDay?-2:x.at)-(y.allDay?-2:y.at));return {days,items:out}}
const calNorm=v=>String(v||'').normalize('NFKD').replace(/\p{M}/gu,'').toLowerCase().trim();
const calWords=v=>calNorm(v).split(/[^\p{L}\p{N}]+/u).filter(w=>w.length>1);
// The promise's person is in the meeting: named in its title, or a guest (by name or address)
function calWith(p,m){const who=calWords(p.who);if(!who.length)return false;const full=who.join(' ');
 return [m.title,...(m.people||[])].some(t=>{const w=calWords(t);return w.join(' ').includes(full)||w.includes(who[0])&&who[0].length>2})}
const calSaid=p=>p.together?t('With {}',p.who):p.direction==='mine'?t('Promised to {}',p.who):t('{} promised',p.who);
const CAL_CARD={prepared:['Prep ready','mint'],accepted:['Preparing','lavender'],instructions:['Preparing','lavender'],pending:['To-do','amber'],snoozed:['To-do','muted']};
const calShort=k=>{const d=new Date(k+'T12:00');return d.toLocaleDateString(DL,{weekday:'short'})+' '+d.getDate()};  // Sat 24
// "09:45 to 10:30" in English; in another language a dash, as its calendars write it (09:45–10:30, ma 26 – wo 28)
const rangeText=(a,b)=>I18N.lang==='en'?a+' to '+b:a+(/\s/.test(a+b)?' – ':'–')+b;
function calParts(it){const hm=v=>humanHM(new Date(v)),late=it.day==='overdue';
 if(it.kind==='meeting'){const m=it.m,c=it.s&&CAL_CARD[it.s.status],a=new Date(m.start),b=new Date(m.end),
   when=it.allDay?(it.span?rangeText(calShort(it.span[0]),calShort(it.span[1])):''):!(b>a)?'':rangeText(hm(a),(localDay(b)!==localDay(a)?calShort(localDay(b))+' ':'')+hm(b));
  return {time:it.allDay?'All day':hm(m.start),title:m.title,owner:m.shared?m.shared+'’s':'',sub:[when,m.location,...(m.rooms||[]),m.guests?t(['{} guest','{} guests'],m.guests):'',m.notes?t('Notes'):'',m.transcript?t('Transcript'):''].filter(Boolean).join(' · '),
   said:(it.promises||[]).map(p=>calSaid(p)+': '+p.what),
   href:it.s?'#chat='+it.s.id:'',edit:!it.s&&m.edit?m.id:'',view:!it.s&&!m.edit?m.id:'',badge:c?chip(c[0],c[1]):'',prep:c?c[0]:'',tone:m.shared?'theirs':it.s?'prep t-'+(c?c[1]:'muted'):'meeting'}}
 if(it.kind==='promise'){const p=it.p;return {time:late?calShort(p.due):'Due',title:p.what,sub:calSaid(p),href:promiseHref(p),tone:late?'late':'promise'}}
 const s=it.s;if(it.kind==='checkin')return {time:hm(s.snoozed_until),title:t('Check in with {}',s.handoff_wait.name),sub:t('If no answer')+' · '+s.title,href:'#chat='+s.id,tone:'back'};
 if(it.kind==='back')return {time:hm(s.snoozed_until),title:s.title,sub:'Comes back',href:'#chat='+s.id,tone:'back'};
 return {time:late?calShort(s.due):'Due',title:s.title,sub:calCardWho(s),href:'#chat='+s.id,tone:late?'late':'due'}}
// Who a due card is with, never its status: the person it waits on, or the promise it came from
function calCardWho(s){let w={};try{w=JSON.parse(s.awaiting||'{}')||{}}catch{}const name=s.handoff_wait?.name||w.name;if(name)return t('Waiting on {}',name);
 const p=(state.promises||[]).find(p=>p.suggestion_id===s.id);return p?calSaid(p):''}
function calRow(it){const x=calParts(it),tag=x.href||x.edit||x.view?'a':'div',attrs=x.href?` href="${esc(x.href)}"`:x.edit?` role="button" tabindex="0" data-cal-edit="${esc(x.edit)}"`:x.view?` role="button" tabindex="0" data-cal-view="${esc(x.view)}"`:'';
 return `<${tag} class="cal-item k-${x.tone}${it.past?' past':''}"${attrs}><span class="cal-time">${esc(x.time)}</span><span class="cal-dot" aria-hidden="true"></span><span class="cal-main"><span class="cal-title">${x.owner?`<span class="cal-owner">${esc(x.owner)}</span> `:''}<span translate="no">${esc(x.title)}</span></span>${x.sub||x.prep?`<span class="cal-sub">${x.prep?`<span class="cal-prep">${esc(x.prep)}${x.sub?' · ':''}</span>`:''}${esc(x.sub)}</span>`:''}${(x.said||[]).map(t=>`<span class="cal-sub cal-said">${esc(t)}</span>`).join('')}</span><span class="cal-end">${x.badge||''}${x.href||x.edit||x.view?'<span class="cal-go" aria-hidden="true">›</span>':''}</span></${tag}>`}
function calChip(it){const x=calParts(it),tag=x.href||x.edit||x.view?'a':'div',attrs=x.href?` href="${esc(x.href)}"`:x.edit?` role="button" tabindex="0" data-cal-edit="${esc(x.edit)}"`:x.view?` role="button" tabindex="0" data-cal-view="${esc(x.view)}"`:'';
 return `<${tag} class="cal-chip k-${x.tone}${it.past?' past':''}"${attrs} title="${esc([x.owner,x.title].filter(Boolean).join(' ')+(x.sub?' · '+x.sub:'')+(x.said||[]).map(t=>' · '+t).join(''))}"><span class="t">${esc(x.owner||x.time)}</span><span class="n" translate="no">${esc(x.title)}</span></${tag}>`}
const calDate=k=>calOf(k).toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'});  // Sat, Oct 24
const calMon=d=>d.toLocaleDateString(DL,{month:'short'}).replace(/\.$/,'');
// A run of days as "Oct 26 – Nov 1, 2026" (the year once, or on both sides when it changes)
function calSpan(a,n=7){const b=calAdd(a,n-1),y=', '+b.getFullYear();
 if(I18N.lang!=='en')try{return new Intl.DateTimeFormat(DL,{day:'numeric',month:'short',year:'numeric'}).formatRange(a,b)}catch{}
 return a.getFullYear()!==b.getFullYear()?`${calMon(a)} ${a.getDate()}, ${a.getFullYear()} – ${calMon(b)} ${b.getDate()}, ${b.getFullYear()}`:
  a.getMonth()!==b.getMonth()?`${calMon(a)} ${a.getDate()} – ${calMon(b)} ${b.getDate()}${y}`:`${calMon(b)} ${a.getDate()} – ${b.getDate()}${y}`}
const calMonthName=m=>m.toLocaleDateString(DL,{month:'long',year:'numeric'});
const calLabel=()=>calMode==='month'?calMonthName(calMonth):calThree()?calSpan(calStart,3):calSpan(calAt);
const calStepName=()=>calMode==='month'?'month':calThree()?'days':'week';
// On the current period: this week, this month, or three days that hold today
function calOnNow(){const t=calDay(0);return calMode==='month'?+calMonth===+calFirst(t):calThree()?calStart<=t&&t<calAdd(calStart,3):+calAt===+calMonday(t)}
const CAL_VIEWS=[['agenda','Agenda','a'],['week','Week','w'],['month','Month','m']];
function calHead(){const step=calStepName(),[prev,next]=step==='month'?[t('Previous month'),t('Next month')]:step==='days'?[t('Previous days'),t('Next days')]:[t('Previous week'),t('Next week')];  /* whole words per step: "Previous {}" can't agree in gender */
 return `<div class="cal-head"><h2 class="page-title">Calendar</h2><div class="cal-nav"><button type="button" class="cal-today${calOnNow()?' now':''}" data-cal-go="0" title="Today (t)">Today</button>`+
  `<button type="button" class="cal-step" data-cal-go="-1" aria-label="${esc(prev)}" title="${esc(prev)} (←)">‹</button><button type="button" class="cal-step" data-cal-go="1" aria-label="${esc(next)}" title="${esc(next)} (→)">›</button>`+
  `<span class="cal-range">${esc(calLabel())}</span></div><div class="cal-mode" role="group" aria-label="View">${CAL_VIEWS.map(([v,t,k])=>`<button type="button" data-cal-mode="${v}" aria-pressed="${calMode===v}" title="${t} (${k})">${t}</button>`).join('')}</div>${calCals.length?'<button type="button" class="ghost head-new cal-new" data-cal-new title="New event">+ New event</button>':''}</div>`}
const calHash=()=>'#calendar?view='+calMode+'&date='+localDay(calMode==='month'?calMonth:calThree()?calStart:calAt);
function calPush(replace){const h=calHash();if(location.hash===h)return;history[replace?'replaceState':'pushState'](null,'',location.pathname+location.search+h)}
const calName=k=>{const t=localDay(new Date());return k===t?'Today':k===localDay(calDay(1))?'Tomorrow':k===localDay(calDay(-1))?'Yesterday':calOf(k).toLocaleDateString(DL,{weekday:'long'})};
// A manual one (under "A clear week") loads only on a tap: loading by itself there found nothing again and again, and
// the button flashed between Loading and Later days
const calMoreRow=(dir,manual)=>{const end=dir==='up'?calFrom<=calAdd(calMonday(new Date()),-7*CAL_BACK):calTo>=calAdd(calMonday(new Date()),7*CAL_AHEAD);if(end)return '';
 return `<div class="cal-more" data-cal-more="${dir}"${manual?' data-cal-manual':''}><button type="button" class="quiet">${calMoreFailed[dir]?'Couldn’t load. Try again':dir==='up'?'Show earlier days':'Later days'}</button></div>`};
// The sticky header's bottom edge: rows under it are out of sight
const calEdge=()=>{const h=$('#page-head');return h&&!h.hidden?Math.max(0,h.getBoundingClientRect().bottom):0};
function calAnchor(box){const edge=calEdge();for(const el of box.querySelectorAll('.cal-block[data-day]')){const r=el.getBoundingClientRect();if(r.bottom>edge)return {day:el.dataset.day,top:r.top}}return null}
const calWeekday=k=>calOf(k).toLocaleDateString(DL,{weekday:'short'}).replace(/[,.]/g,'');
function calDayBlock(k,list,late,today){const name=calName(k),date=calDate(k);
 return (k===today?late:'')+`<section class="cal-block${list.length?'':' cal-empty'}" data-day="${k}" aria-label="${esc(name+' '+date)}"><h3 class="cal-day"><span>${esc(name)}</span><small>${esc(/^(Today|Tomorrow|Yesterday)$/.test(name)?date:date.replace(/^\S+\s/,''))}</small>${list.length?`<span class="count">${list.length}</span>`:'<span class="cal-none">Nothing planned</span>'}</h3>${list.map(calRow).join('')}</section>`}
// Week as a time grid: hours down the side, a column per day, each meeting a block as long as it lasts; ones that
// overlap share the width. All day, and dates without a time (due cards, promises), sit in a strip on top. A line
// marks now on today. A computer shows the calendar week; a phone three days, swiped through.
const calHourLabel=h=>H12?`${h%12||12} ${h<12?'AM':'PM'}`:String(h).padStart(2,'0')+':00';  // 01:00 or 1 AM, by Settings
const CAL_HOUR=68,CAL_MIN=30;  // px an hour, so half an hour holds two lines; a block is never shorter than that
function calMins(v,k){const d=new Date(v),day=localDay(d);return day<k?0:day>k?1440:d.getHours()*60+d.getMinutes()}  // local clock time, so a day with a clock change still lines up
// Lay a day's timed items out like a paper calendar: ones that really overlap share the width, as many abreast as
// keep a readable width (a third of the column and room for a word, so up to three; one on a phone), and the rest become "+N" (which opens the day in the agenda). One that only touches the one before because blocks
// have a minimum height sits a little to the right, on top, keeping the full width.
function calLay(list,k,abreast=1){const ev=list.map(it=>{let s,e;if(it.kind==='meeting'){s=calMins(it.m.start,k);const end=new Date(it.m.end);e=!isNaN(end)&&end>new Date(it.m.start)?calMins(it.m.end,k):s+30}else{s=calMins(it.at,k);e=s+30}
  s=Math.min(s,1440-CAL_MIN);e=Math.min(1440,Math.max(e,s+1));return {it,s,e,ve:Math.min(1440,Math.max(e,s+CAL_MIN)),ind:0}}).sort((a,b)=>a.s-b.s||b.e-a.e);
 const shown=[],more=[];let group=[],end=-1;
 const flush=()=>{if(!group.length)return;const cols=[];for(const x of group){let c=cols.findIndex(e=>e<=x.s);if(c<0){c=cols.length;cols.push(0)}cols[c]=x.e;x.col=c}
  const max=abreast,n=Math.min(max,cols.length),hid=group.filter(x=>x.col>=max);for(const x of group)if(x.col<max){x.n=n;x.rail=hid.length>0;shown.push(x)}
  if(hid.length)more.push({s:Math.min(...hid.map(x=>x.s)),n:hid.length});group=[]};
 for(const x of ev){if(group.length&&x.s>=end){flush();end=-1}group.push(x);end=Math.max(end,x.e)}flush();
 for(const x of shown)for(const y of shown){if(y===x)break;if(y.s<x.s&&x.s<y.ve&&x.s>=y.e&&(x.n===1||y.n===1||x.col===y.col))x.ind=Math.max(x.ind,y.ind+1)}
 return {shown,more}}
// A block: its start time, then its title, on as many lines as it has room for (two at least)
function calBlock(b){const x=calParts(b.it),tag=x.href||x.edit||x.view?'a':'div',attrs=x.href?` href="${esc(x.href)}"`:x.edit?` role="button" tabindex="0" data-cal-edit="${esc(x.edit)}"`:x.view?` role="button" tabindex="0" data-cal-view="${esc(x.view)}"`:'',h=(b.ve-b.s)*CAL_HOUR/60-2,off=b.ind*12,rail=b.rail?(DESK.matches?26:20):0;
 return `<${tag} class="cal-blk k-${x.tone}${b.it.past?' past':''}${b.n>1?' side':''}"${attrs} style="top:${b.s*CAL_HOUR/60}px;height:${h}px;left:calc(${b.col} * (100% - ${rail}px) / ${b.n} + ${off}px);width:calc((100% - ${rail}px) / ${b.n} - ${3+off}px);z-index:${1+b.ind};--lines:${Math.max(2,Math.floor((h-4)/14))}" title="${esc([x.time,x.owner,x.title].filter(Boolean).join(' ')+(x.sub?' · '+x.sub:'')+(x.said||[]).map(t=>' · '+t).join(''))}"><span class="c"><span class="t">${esc(x.time)}</span> <span class="n">${x.owner?esc(x.owner)+' ':''}<span translate="no">${esc(x.title)}</span></span></span></${tag}>`}
const calMoreBlock=(m,k)=>`<button type="button" class="cal-tg-more" data-cal-open="${k}" style="top:${m.s*CAL_HOUR/60}px" aria-label="${esc(t('{} more, open the day',m.n))}">+${m.n}</button>`;
// How many overlapping items sit side by side in a day's column: each keeps a third of the column and at least 56px
function calAbreast(n){if(!DESK.matches)return 1;const box=$('#calendar-view');let w=box?.clientWidth||0;if(!w)w=innerWidth-($('#app-side')?.offsetWidth||0)-112;
 return Math.max(1,Math.min(3,Math.floor((w-48)/n/56)))}
function calTimeGrid(days,byDay,today){const n=days.length,nowMin=new Date().getHours()*60+new Date().getMinutes(),abreast=calAbreast(n);
 const cols=days.map(k=>{const list=byDay(k);return {k,strip:list.filter(i=>i.allDay||i.at<0),lay:calLay(list.filter(i=>!i.allDay&&i.at>=0),k,abreast)}}),strip=cols.some(c=>c.strip.length);
 const head=`<div class="cal-tg-head">${'<span></span>'+cols.map(c=>`<div class="cal-tg-day${c.k===today?' today':''}${c.k<today?' gone':''}" data-day="${c.k}"><span>${c.k===today?'Today':esc(calWeekday(c.k))}</span><b>${calOf(c.k).getDate()}</b></div>`).join('')}</div>`;
 const top=strip?`<div class="cal-tg-strip"><span class="cal-tg-label">All day</span>${cols.map(c=>`<div class="cal-tg-cell">${c.strip.map(calChip).join('')}</div>`).join('')}</div>`:'';
 const hours=[...Array(23)].map((_,h)=>`<span style="top:${(h+1)*CAL_HOUR}px">${calHourLabel(h+1)}</span>`).join('');
 return `<div class="cal-tg" style="--n:${n};--hour:${CAL_HOUR}px">${head}${top}<div class="cal-tg-scroll"><div class="cal-tg-body"><div class="cal-tg-hours" aria-hidden="true">${hours}</div>${cols.map(c=>`<div class="cal-tg-col${c.k===today?' today':''}" data-col="${c.k}">${c.k===today?`<i class="cal-now" style="top:${nowMin*CAL_HOUR/60}px" aria-hidden="true"></i>`:''}${c.lay.shown.map(calBlock).join('')}${c.lay.more.map(m=>calMoreBlock(m,c.k)).join('')}</div>`).join('')}</div></div></div>`}
// Month: the calendar month, Monday on or before the 1st to Sunday on or after the last; days of the months around it
// step back. A computer shows up to three items a day and "+N more"; a phone shows dots, and a tap lists that day.
let calPick='';
function calMonthGrid(days,byDay,today){const m=calMonth.getMonth(),phone=!DESK.matches;
 if(!calPick||calOf(calPick).getMonth()!==m||!days.includes(calPick))calPick=localDay(calOnNow()?calDay(0):calMonth);
 const head=`<div class="cal-mg-head">${days.slice(0,7).map(k=>`<span>${esc(calWeekday(k))}</span>`).join('')}</div>`;
 const cells=days.map(k=>{const d=calOf(k),list=byDay(k),cls=`cal-mday${d.getMonth()!==m?' out':''}${k===today?' today':''}${k<today?' gone':''}`;
  if(phone)return `<button type="button" class="${cls}${k===calPick?' picked':''}" data-cal-pick="${k}" aria-label="${esc(calDate(k)+(list.length?', '+list.length:''))}" aria-pressed="${k===calPick}"><b>${d.getDate()}</b><span class="cal-dots">${list.slice(0,3).map(i=>`<i class="k-${calParts(i).tone}"></i>`).join('')}</span></button>`;
  return `<div class="${cls}" data-day="${k}"><button type="button" class="cal-mnum" data-cal-open="${k}" aria-label="${esc(calDate(k))}">${d.getDate()}</button>${list.slice(0,3).map(calChip).join('')}${list.length>3?`<button type="button" class="cal-mmore" data-cal-open="${k}">${esc(t('+{} more',list.length-3))}</button>`:''}</div>`}).join('');
 return `<div class="cal-mg${phone?' dots':''}">${head}<div class="cal-mg-days">${cells}</div></div>`+(phone?calDayBlock(calPick,byDay(calPick),'',''):'')}
function calRender(){const box=$('#calendar-view');if(!box||!state)return;const list=calList(),[from,to]=calRange(),{days,items}=calItems(from,to),byDay=k=>items.filter(i=>i.day===k),late=byDay('overdue'),today=localDay(new Date());
 $('#calendar').classList.toggle('week',!list);
 const cals=(state.connectors||[]).some(c=>['calendar','outlook_calendar'].includes(c.service)),failed=calFailedIn(from,to);
 // No calendar yet: a button that connects one (Connections, + Add, at Google or Outlook Calendar, by the mail connected)
 const connect=cls=>`<button type="button" class="${cls}" data-connect-open="${(state.connectors||[]).some(c=>c.service==='outlook')?'outlook_calendar':'calendar'}">${esc(t('Connect your calendar'))}</button>`;
 const note=failed?'<p class="cal-note">Meetings couldn’t load. To-dos and promises are here.</p>':!cals?`<p class="cal-note cal-connect"><span>No calendar connected, so no meetings yet.</span>${connect('ghost')}</p>`:'';
 const lateBlock=late.length?`<section class="cal-block late" aria-label="Overdue"><h3 class="cal-day"><span>Overdue</span><span class="count">${late.length}</span></h3>${late.map(calRow).join('')}</section>`:'';
 let html='';
 if(calMode==='month')html=lateBlock+calMonthGrid(days,byDay,today);
 else if(!list)html=lateBlock+calTimeGrid(days,byDay,today);
 else if(!items.length&&!cals&&!failed)html=`<div class="all-clear cal-clear"><img src="brand/avatar.png" alt="" width="64" height="64"><div><strong>No calendar yet</strong><span>Connect one to see your meetings here, with due to-dos and promises.</span></div>${connect('primary')}</div>`;
 else if(!items.length&&calMeetings&&!failed)html=`<div class="all-clear cal-clear"><img src="brand/avatar.png" alt="" width="64" height="64"><div><strong>A clear week</strong><span>Meetings, due to-dos and promises show here.</span></div></div>`+calMoreRow('down',true);
 else html=calMoreRow('up')+days.map((k,i)=>(i&&calOf(k).getDay()===1?`<p class="cal-wk">${esc(calSpan(calOf(k)))}</p>`:'')+calDayBlock(k,byDay(k),lateBlock,today)).join('')+calMoreRow('down');
 if(!(list&&!items.length&&!cals))html+=note;if(!calMeetings&&!items.length&&cals)html='<p class="cal-note">Loading…</p>';
 // Earlier days coming in above, or a week's meetings arriving, never move what is on screen; the time grid keeps its hour
 const keep=list&&!$('#calendar').hidden?calAnchor(box):null,pane=box.querySelector('.cal-tg-scroll'),hash=calHash(),y=pane&&calGridShown===hash?pane.scrollTop:null;
 if(box.innerHTML!==html){box.innerHTML=html;if(keep){const el=box.querySelector(`[data-day="${keep.day}"]`),d=el?el.getBoundingClientRect().top-keep.top:0;if(Math.abs(d)>.5)scrollBy(0,d)}calObserve(box)}
 const p=box.querySelector('.cal-tg-scroll');calFill(p);if(p){if(y!=null)p.scrollTop=y;else if(calMeetings&&p.clientHeight){p.scrollTop=calFirstHour(box,p.clientHeight/CAL_HOUR)*CAL_HOUR;calGridShown=hash}}  // a hidden pane can't scroll: wait until it shows
 calBadge();pageHead()}
// The time grid opens a little before the range's first timed meeting, or 08:00 when that is earlier; later in
// the day the now line stays in view. Also on ‹ › and Today
let calGridShown='';
// On a desktop the time grid fills the window down to its bottom edge, with the footer still in view, so more hours
// show at once and only the grid scrolls (a very short window scrolls the page too); the phone keeps its own height
function calFill(p){if(!p)return;if(!DESK.matches){p.style.maxHeight='';return}const top=p.getBoundingClientRect().top+scrollY;
 if(!p.clientHeight&&!top)return;const h=Math.max(320,Math.round(innerHeight-top-16));p.style.maxHeight=h+'px';
 const over=document.documentElement.scrollHeight-innerHeight;if(over>0)p.style.maxHeight=Math.max(320,p.clientHeight-over)+'px'}
let calSized=0;addEventListener('resize',()=>{if($('#calendar').hidden)return;cancelAnimationFrame(calSized);calSized=requestAnimationFrame(()=>{if(calMode!=='month'&&!calList())calRender();calFill($('#calendar-view .cal-tg-scroll'))})});
function calFirstHour(box,shown=8){const tops=[...box.querySelectorAll('.cal-blk')].map(b=>parseFloat(b.style.top)/CAL_HOUR).filter(t=>t>=0);
 let h=Math.max(0,Math.min(8,...tops)-.5);const now=box.querySelector('.cal-now');
 if(now){const n=parseFloat(now.style.top)/CAL_HOUR;if(n>h+shown-.5)h=Math.max(0,n-Math.min(2,shown/3))}
 return Math.min(h,Math.max(0,24-shown))}
// The row's count: what is on today, also before the Calendar is opened (its meetings come once, a moment after the start)
function calBadge(){if(!state)return;const {items}=calItems(),n=items.filter(i=>i.day===localDay(new Date())).length,b=$('#badge-calendar');if(b&&b.textContent!==(n?String(n):''))b.textContent=n?String(n):''}
setTimeout(()=>calFetch().then(calBadge),2000);
setInterval(()=>{if(!$('#calendar').hidden&&!calList())calRender()},60000);  // the now line moves on
// More days: a week at a time, below as you near the end, above as you scroll up to the top; a tap does it too, and
// is the way back when a week couldn't load
async function calMore(dir){if(calBusy)return calBusy;const up=dir==='up',a=up?calMonday(calAdd(calFrom,-1)):calTo,b=up?calFrom:calAdd(calMonday(calTo),7);  // up to a Monday, on to the next
 if(!calMoreRow(dir))return;const btn=$(`#calendar-view [data-cal-more="${dir}"] button`);if(btn){btn.disabled=true;btn.textContent='Loading…'}
 calBusy=(async()=>{await Promise.all(calMondays(a,b).map(d=>calFetchWeek(d)));calMoreFailed[dir]=calFailedIn(a,b);if(!calMoreFailed[dir]){if(up)calFrom=a;else calTo=b}calRender()})().finally(()=>{calBusy=null});return calBusy}
const calIO=window.IntersectionObserver?new IntersectionObserver(es=>{for(const e of es){const dir=e.target.dataset.calMore;if(!e.isIntersecting||calMoreFailed[dir]||dir==='up'&&!calUp)continue;calMore(dir)}},{rootMargin:'300px 0px'}):null;
function calObserve(box){if(!calIO)return;calIO.disconnect();box.querySelectorAll('[data-cal-more]:not([data-cal-manual])').forEach(el=>calIO.observe(el))}
const calUpSeen=()=>{const el=$('#calendar-view [data-cal-more="up"]');return el&&el.getBoundingClientRect().bottom>-300};
// Which way the agenda moves, and its week in the header and the address as it scrolls
let calScrollTick=0,calUrlTimer=0;
addEventListener('scroll',()=>{if($('#calendar').hidden||calScrollTick)return;calScrollTick=requestAnimationFrame(()=>{calScrollTick=0;const y=scrollY;calUp=y<calLastY;calLastY=y;if(!calList())return;
 const top=calAnchor($('#calendar-view'));if(!top)return;const mon=calMonday(calOf(top.day));if(+mon===+calAt)return;calAt=mon;pageHead();clearTimeout(calUrlTimer);calUrlTimer=setTimeout(()=>{if(!$('#calendar').hidden)calPush(true)},300)})},{passive:true});
// At the very top a page can't scroll up, so a wheel or a pull down there asks for earlier days; on a phone's three
// days a sideways swipe moves three days on or back
let calTouch=null;
addEventListener('wheel',e=>{if(e.deltaY<0&&!$('#calendar').hidden&&calList()&&calUpSeen()){calUp=true;calMore('up')}},{passive:true});
addEventListener('touchstart',e=>{const t=e.touches[0];calTouch=t?{x:t.clientX,y:t.clientY,grid:!!e.target.closest?.('.cal-tg')}:null},{passive:true});
addEventListener('touchmove',e=>{if(!calTouch||$('#calendar').hidden||!calList())return;if(e.touches[0].clientY-calTouch.y>40&&calUpSeen()){calTouch=null;calUp=true;calMore('up')}},{passive:true});
addEventListener('touchend',e=>{const t=e.changedTouches[0],s=calTouch;calTouch=null;if(!s?.grid||!t||$('#calendar').hidden||!calThree())return;const dx=t.clientX-s.x,dy=t.clientY-s.y;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)*1.5)calGo(dx<0?1:-1)},{passive:true});
// Bring a day to the top of the agenda, under the header (Today brings Overdue along when there is one). The first day
// on show opens the page at its top, as the Calendar opens from the nav: else Week or Month and back sat 66px higher. When the
// days after it are too few to fill the screen, the next week loads first: else the page ends before the day is at
// the top, and the header and the address go back to the week above.
async function calScrollTo(day){const k=localDay(day),h=$('#page-head');
 const find=()=>{let el=$('#calendar-view').querySelector(`.cal-block[data-day="${k}"]`);if(el&&k===localDay(new Date())){const prev=el.previousElementSibling;if(prev?.classList.contains('late'))el=prev}return el};
 const want=el=>{const off=h&&!h.hidden?h.offsetHeight+(parseFloat(getComputedStyle(h).top)||0):0;return Math.max(0,scrollY+el.getBoundingClientRect().top-off-8)};
 let el=find();for(let i=0;el&&i<3&&want(el)>document.documentElement.scrollHeight-innerHeight&&!calMoreFailed.down&&calMoreRow('down');i++){await calMore('down');el=find()}
 if(!el)return;calLastY=el.parentElement.querySelector('.cal-block')===el?0:want(el);calUp=false;scrollTo({top:calLastY})}
// The day a view is about: today when it is on show, else the period's first day
function calFocus(){const t=calDay(0);if(calOnNow())return t;return calMode==='month'?calMonth:calThree()?calStart:calAt}
const calSetAll=day=>{calAt=calMonday(day);calMonth=calFirst(day);calStart=calMid(day)};
// Draw the period on show. The agenda keeps its days when the week is next to them, or starts again from it, and
// brings the day to the top.
async function calShowNow(day){if(calList()){const mon=calAt,thisWeek=+mon===+calMonday(new Date());day=day||(thisWeek?calDay(0):mon);const end=calAdd(calMonday(day),7);
  if(day<calAdd(calFrom,-7)||day>calTo){calFrom=day;calTo=calAdd(day,7)}else{if(day<calFrom)calFrom=day;if(end>calTo)calTo=end}calMoreFailed={}}
 if(!calList()&&scrollY)scrollTo({top:0});calRender();await calFetch();calRender();if(calList())await calScrollTo(day)}
function calGo(n){if(calMode==='month')calMonth=n?new Date(calMonth.getFullYear(),calMonth.getMonth()+n,1):calFirst(new Date());
 else if(calThree())calStart=n?calAdd(calStart,3*n):calDay(0);
 else calAt=n?calAdd(calAt,7*n):calMonday(new Date());
 calGridShown='';calPush();return calShowNow()}  // Today on today's range opens at its first meeting again
// Switching views keeps the period: Month after a week shows that week's month, Week after a month its first week
function calSetMode(v,day){if(calMode===v&&!day)return;const at=day||calFocus();calMode=v;sideStore.set('cal-mode',v);calSetAll(at);calPush();return calShowNow(day)}
// Back and forward, and a shared link: #calendar?view=week&date=2026-10-26
function calRoute(){const m=/^#calendar\?(.*)$/.exec(location.hash);if(!m)return;const q=new URLSearchParams(m[1]),v=q.get('view'),k=q.get('date')||'';
 const d=/^\d{4}-\d{2}-\d{2}$/.test(k)&&!isNaN(calOf(k))?calOf(k):calDay(0);if(CAL_VIEWS.some(([x])=>x===v))calMode=v;
 if($('#calendar').hidden){calRouting=true;try{showTab('calendar')}finally{calRouting=false}}
 calSetAll(d);calShowNow()}
addEventListener('popstate',calRoute);addEventListener('hashchange',calRoute);setTimeout(calRoute);
// The arrows move the period on a computer; t, k j, a, w and m are with the shared shortcuts (actionAdd, below)
const CAL_KEYS={arrowleft:()=>calGo(-1),arrowright:()=>calGo(1)};
addEventListener('keydown',e=>{if($('#calendar').hidden||e.ctrlKey||e.metaKey||e.altKey||e.isComposing||e.defaultPrevented||drawerIs()||document.querySelector('dialog[open]')||e.target.closest?.('textarea,input,select,[contenteditable]'))return;
 const f=CAL_KEYS[e.key.toLowerCase()];if(f){e.preventDefault();f()}});
// A row opens its card's chat (back returns here), the promise's page, or the meeting in a new tab. In Month a day
// opens in the agenda (a computer) or lists below (a phone). The view is remembered on this device, and the Calendar
// always opens on the current period.
$('#calendar').addEventListener('click',e=>{const ed=e.target.closest('[data-cal-edit],[data-cal-view]');if(ed){e.preventDefault();calOpen(ed);return}
 const more=e.target.closest('[data-cal-more] button');if(more){const dir=more.parentElement.dataset.calMore;calMoreFailed[dir]=false;calUp=dir==='up';calMore(dir);return}
 const pick=e.target.closest('[data-cal-pick]');if(pick){calPick=pick.dataset.calPick;calRender();return}
 const day=e.target.closest('[data-cal-open]');if(day){calSetMode('agenda',calOf(day.dataset.calOpen));return}
 const a=e.target.closest('a[href^="#"]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey)return;const href=a.getAttribute('href');e.preventDefault();
 if(href.startsWith('#chat=')){calReturn=true;chatGo(href.slice(6));return}
 if(href.startsWith('#promise/')){calPush(true);location.hash=href;return}  // back returns to this period of the Calendar
 if(href==='#connections')showTab('health')});
$('#page-head').addEventListener('click',e=>{if(e.target.closest('[data-cal-new]')){calEditor();return}const b=e.target.closest('[data-cal-mode],[data-cal-go]');if(!b)return;if(b.dataset.calMode)calSetMode(b.dataset.calMode);else calGo(Number(b.dataset.calGo))});
// New event and changing one: only on a calendar the owner can write (their own, or one shared with them to change),
// and only a meeting without other people on it. What the form shows is what changes, on the owner's tap; nobody is
// invited or told. A tap that is retried (no answer) is the same change, never a second event.
let calEdit=null;
const calPad=n=>String(n).padStart(2,'0'),calHM=d=>calPad(d.getHours())+':'+calPad(d.getMinutes());
// The browser's own clock as an offset, so 16:00 stays 16:00 here
const calIso=(day,hm)=>{const d=new Date(day+'T'+hm+':00');if(isNaN(d))return '';const o=-d.getTimezoneOffset(),a=Math.abs(o);return day+'T'+hm+':00'+(o<0?'-':'+')+calPad(Math.floor(a/60))+':'+calPad(a%60)};
function calAllDay(on){$('#cal-f-allday').checked=on;for(const el of document.querySelectorAll('#cal-dialog .cal-f-time'))el.hidden=on;document.querySelector('#cal-dialog .cal-f-until').hidden=false;$('#cal-end-label').textContent=on?'Last day':'End date'}
// New event from anywhere (the "+" menu, the palette): the calendars it can add to come with the Calendar's answer
async function calNew(){if(!calCals.length){const a=new Date();try{const r=await request('api/calendar?from='+encodeURIComponent(a.toISOString())+'&to='+encodeURIComponent(new Date(a.getTime()+864e5).toISOString()));if(Array.isArray(r?.calendars))calCals=r.calendars}catch{}}
 if(!calCals.length){toast('No calendar you can change yet. See Connections.',true);return}calEditor()}
// An event that can't be changed here (someone else's, with guests, or on a calendar only to read): its details in the
// app, and its own calendar one link away. Looking changes nothing.
const calOpenLabel=url=>{let h='';try{h=new URL(url).hostname}catch{}return /(^|\.)google\.com$/.test(h)?'Open in Google Calendar ↗':/(^|\.)(outlook\.(com|office\.com|office365\.com|live\.com)|office\.com|live\.com)$/.test(h)?'Open in Outlook ↗':'Open in its calendar ↗'};
function calView(m){const a=new Date(m.start),b0=new Date(m.end),b=isNaN(b0)||b0<=a?new Date(a.getTime()+1):b0,long=d=>d.toLocaleDateString(DL,{weekday:'long',day:'numeric',month:'long'});
 const allDay=m.all_day||b-a>=864e5,last=new Date(b-1),when=allDay?(localDay(last)!==localDay(a)?rangeText(long(a),long(last)):long(a))+' · '+t('All day')
  :long(a)+', '+rangeText(humanHM(a),(localDay(b)!==localDay(a)?long(b)+', ':'')+humanHM(b));
 const where=[m.location,...(m.rooms||[])].filter(Boolean).join(' · ');  // a booked meeting room is where, not who
 const rows=[['When',when],...(where?[['Where',where]]:[]),...(m.shared?[['Calendar',t('{}’s calendar',m.shared)]]:[]),
  ...(m.guests&&!(m.with||m.people)?.length?[['With',t(['{} guest','{} guests'],m.guests)]]:[])];
 // With: the name (from the invite or the Graph) with its address muted beside it, or the address alone
 const met=(m.with||(m.people||[]).map(p=>p.includes('@')?{name:'',email:p}:{name:p,email:''})).slice(0,6),more=Math.max(m.guests||0,(m.with||m.people||[]).length)-met.length;
 // A guest the Graph knows opens their page; the organizations and projects it's on open theirs
 const withHtml=met.map(w=>{const label=w.name?esc(w.name)+(w.email?` <span class="cal-v-mail">${esc(w.email)}</span>`:''):esc(w.email);
   return w.node_id?`<span class="cal-v-who cal-v-known"><a class="chip scope who" href="${esc(graphHash(w.node_id))}"${w.email?` title="${esc(w.email)}"`:''}>${CHIP_ICON.person}<span>${esc(w.name||w.email)}</span></a></span>`
    :`<span class="cal-v-who"${w.email?` title="${esc(w.email)}"`:''}>${label}</span>`}).join('')
  +(more>0?`<span class="cal-v-who cal-v-mail">${esc(t('and {} more',more))}</span>`:'');
 $('#cal-v-title').textContent=m.title||t('(No title)');
 $('#cal-v-rows').innerHTML=rows.map(([k,v])=>`<div><dt>${esc(t(k))}</dt><dd>${esc(v)}</dd></div>`).join('')+(met.length?`<div><dt>${esc(t('With'))}</dt><dd class="cal-v-with">${withHtml}</dd></div>`:'')
  +[['Organization','Organizations','org',m.orgs],['Project','Projects','project',m.projects]].filter(r=>r[3]?.length).map(([one,many,icon,list])=>
   `<div><dt>${esc(t(list.length>1?many:one))}</dt><dd class="cal-v-links">${list.map(n=>`<a class="chip scope who" href="${esc(graphHash(n.node_id))}">${CHIP_ICON[icon]}<span>${esc(n.name)}</span></a>`).join('')}</dd></div>`).join('');
 const open=$('#cal-v-open');open.hidden=!m.url;if(m.url){open.href=m.url;open.textContent=t(calOpenLabel(m.url))}
 $('#cal-v-orig').onclick=()=>openOriginal(m.id,m.title,true);
 calNotesOpen(m);if(!$('#cal-view').open)$('#cal-view').showModal();calNotesFit()}
// A meeting's two records (meeting_notes.py): Notes (a summary, decisions, action items) first and open, then its
// Transcript (what was said), folded until opened. Each is the one added to the meeting, by the owner here (pasted, or a
// file) or by a Do it run, and the meeting app's that matches it, marked From Zoom or From Google Meet: both show when both are there, and neither
// replaces the other. Reading is a GET; Save and Remove change only that field, never the other, and reviews use them
// for the meeting's follow-ups. Remove asks twice.
let calNote=null;
const CAL_NOTES_FILE=2e6;
const CAL_FIELDS={
 notes:{api:'notes',empty:'No notes yet.',failed:'Notes couldn’t load.',hint:'Paste notes: a summary, decisions, action items. Markdown works.',
  write:'Write or paste the notes first.',saved:'Notes saved.',removed:'Notes removed.',sure:'Remove notes?',
  saveErr:'Couldn’t save the notes. Try again.',removeErr:'Couldn’t remove the notes. Try again.',big:'That file is too big for notes.'},
 tr:{api:'transcript',empty:'No transcript yet.',failed:'The transcript couldn’t load.',hint:'Paste the transcript: what was said, word for word.',
  write:'Write or paste the transcript first.',saved:'Transcript saved.',removed:'Transcript removed.',sure:'Remove the transcript?',
  saveErr:'Couldn’t save the transcript. Try again.',removeErr:'Couldn’t remove the transcript. Try again.',big:'That file is too big for a transcript.'}};
// How long a transcript runs, in the page's language: 2h 04m or 45m in English; elsewhere the short units (30 min,
// 2 uur 04 min), since the narrow ones read as meters there (30 m)
function calRunTime(min){const d=/^en\b/i.test(DL)?'narrow':'short',f=(unit,v,o={})=>new Intl.NumberFormat(DL,{style:'unit',unit,unitDisplay:d,...o}).format(v),h=Math.floor(min/60);
 return h?f('hour',h)+' '+f('minute',min%60,{minimumIntegerDigits:2}):f('minute',min)}
async function calNotesOpen(m){const me={m,data:null,editing:{notes:false,tr:false},open:false,failed:false,tries:0};calNote=me;
 for(const f in CAL_FIELDS){$('#cal-v-'+f+'-text').value='';$('#cal-v-'+f+'-error').textContent=''}calNotesShow();calNotesLoad(me)}
// A read that fails (The Machine restarting, the network gone for a moment) tries again by itself, 2, 4, 8 and 16 s later,
// and at once when the window gets the focus or the network is back. Only then the line says it couldn't load, with Try again.
const CAL_NOTES_RETRY=[2e3,4e3,8e3,16e3];let calNotesRetry=0;
async function calNotesLoad(me){clearTimeout(calNotesRetry);me.loading=true;let d=null;try{d=await request('api/meeting-notes?event='+encodeURIComponent(me.m.id))}catch{}me.loading=false;
 if(calNote!==me||me.data)return;if(d){me.data=d;me.failed=false;calNotesShow();calNotesFit();calNotesPoll();return}
 const wait=CAL_NOTES_RETRY[me.tries++];if(wait==null||!$('#cal-view').open){me.failed=true;calNotesShow();return}
 calNotesRetry=setTimeout(()=>{if(calNote===me&&$('#cal-view').open)calNotesLoad(me)},wait)}
// Try again, the focus back after it gave up, or the network back: a fresh round of tries
function calNotesAgain(){const n=calNote;if(!n||n.data||n.loading||!$('#cal-view').open)return;n.tries=0;n.failed=false;calNotesShow();calNotesLoad(n)}
addEventListener('focus',()=>{if(calNote?.failed)calNotesAgain()});addEventListener('online',calNotesAgain);
$('#cal-view').addEventListener('click',e=>{if(e.target.closest('[data-cal-notes-retry]'))calNotesAgain()});
$('#cal-view').addEventListener('close',()=>{if(!$('#cal-view').open)clearTimeout(calNotesRetry)});  // a close event can come after it opened again
// While The Machine writes the notes, the open dialog looks again every few seconds; closed, it stops (the writing goes on)
const calWriting=d=>['queued','running','waiting'].includes(d?.writing?.status);
let calNotesTimer=0;
function calNotesPoll(){clearTimeout(calNotesTimer);const n=calNote;if(!calWriting(n?.data))return;
 calNotesTimer=setTimeout(async()=>{if(calNote!==n||!$('#cal-view').open)return;let d=null;try{d=await request('api/meeting-notes?event='+encodeURIComponent(n.m.id))}catch{}
  if(calNote!==n)return;if(d){const had=!!n.data.notes;n.data=d;if(d.notes&&!had){calNotesMark(n.m,calNotesMarks(d));toast('Notes written.')}if(!n.editing.notes){calNotesShow();calNotesFit()}}calNotesPoll()},3000)}
// A transcript reads as it was written, line by line; notes are Markdown
// The meeting apps whose notes and transcripts match a meeting: the block's id, and its key in the API
const CAL_APPS=[['zoom','zoom'],['meet','google_meet']];
const calNotesHtml=(f,text)=>f==='tr'?esc(text):chatMarkdown(text);
function calNotesShow(){const n=calNote,d=n?.data,ready=!!d;
 for(const [f,c] of Object.entries(CAL_FIELDS)){const added=d?.[c.api],editing=!!n?.editing[f],q=id=>$('#cal-v-'+f+'-'+id);
  q('by').textContent=added&&!editing?t(added.by==='owner'?'Added by you · {}':added.written_from==='transcript'?'Written by The Machine · {}':'Added by The Machine · {}',t(humanDay(new Date(added.at)))):'';
  const body=q('body');body.hidden=!added||editing;body.classList.remove('all','cut');body.classList.toggle('plain',f==='tr');body.innerHTML=added&&!editing?calNotesHtml(f,added.text):'';q('more').hidden=true;
  // The meeting app's (Zoom, Google Meet) under the owner's own and its buttons; alone, above Add
  const nact=q('in').querySelector('.cal-v-nact');let after=nact,app=null;
  for(const [k,api] of CAL_APPS){const x=d?.[api]?.[c.api],z=q(k),zb=q(k+'-body');app=app||x;if(added){after.after(z);after=z}else nact.before(z);
   z.hidden=!x||editing;zb.classList.remove('all','cut');zb.classList.toggle('plain',f==='tr');zb.innerHTML=x&&!editing?calNotesHtml(f,x.text):'';q(k+'-more').hidden=true;
   const zl=q(k+'-open'),url=x?.url||d?.[api]?.url;zl.hidden=!url;if(url)zl.href=url}
  const none=q('none');none.hidden=editing||!!added||!!app||!(ready||n?.failed);none.textContent=t(n?.failed?c.failed:c.empty);if(n?.failed)none.insertAdjacentHTML('beforeend',` <button type="button" class="cal-v-retry" data-cal-notes-retry>${esc(t('Try again'))}</button>`);
  // Generate notes: a transcript and no notes at all (the owner's or the meeting app's). It runs on The Machine, so the
  // line says how it goes when the dialog opens again (meeting_writer.py)
  if(f==='notes'){const w=d?.writing,busy=calWriting(d),can=ready&&!added&&!app&&!editing&&!!(d.transcript||CAL_APPS.some(([,api])=>d[api]?.transcript));
   q('gen').hidden=!can||busy;const wl=q('writing');wl.hidden=!can||!w;wl.classList.toggle('busy',busy);
   wl.textContent=!w?'':busy?t(w.status==='waiting'?'Writing notes once your usage limit resets.':'Writing notes…'):t('Couldn’t write the notes. Try again.');
   if(can&&w)none.hidden=true}
  q('form').hidden=!editing;
  for(const [id,on] of [['add',ready&&!added&&!editing],['edit',!!added&&!editing],['remove',!!added&&!editing],['save',editing],['file',ready&&!added&&!editing||editing],['cancel',editing]])q(id).hidden=!on;
  const rm=q('remove');rm.classList.remove('sure');rm.textContent=t('Remove');
  if(f==='tr'){// Folded while it has something to show: its title says how long it runs
   const has=!!(added||app),open=!has||editing||!!n?.open,min=added?.minutes||app?.minutes;
   q('h').textContent=has&&min?t('Transcript · {}',calRunTime(min)):t('Transcript');
   const tg=q('toggle');tg.setAttribute('aria-expanded',String(open));tg.disabled=!has||editing;q('show').hidden=!has||editing;q('show').textContent=t(open?'Hide':'Show');
   q('in').hidden=!open;if(!open)q('by').textContent=''}}}
// Long text shows its start, with Show all
function calNotesFit(){for(const b of document.querySelectorAll('#cal-view .cal-v-nb')){const more=b.nextElementSibling;
 if(b.classList.contains('all'))continue;if(b.hidden||!b.offsetParent){more.hidden=true;continue}
 const cut=b.scrollHeight>b.clientHeight+4;b.classList.toggle('cut',cut);more.hidden=!cut}}
for(const more of document.querySelectorAll('#cal-view .cal-v-more'))more.onclick=()=>{const b=more.previousElementSibling;b.classList.add('all');b.classList.remove('cut');more.hidden=true};
$('#cal-v-tr-toggle').onclick=()=>{if(!calNote)return;calNote.open=!calNote.open;calNotesShow();calNotesFit()};
function calNotesEdit(f,text){if(!calNote?.data)return;calNote.editing[f]=true;calNotesShow();const box=$('#cal-v-'+f+'-text');box.placeholder=t(CAL_FIELDS[f].hint);
 box.value=text??(calNote.data[CAL_FIELDS[f].api]?.text||'');$('#cal-v-'+f+'-error').textContent='';box.focus()}
async function calNotesSend(args){const n=calNote;if(!n)return null;
 return request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf,'X-Upload':'meeting-notes'},body:JSON.stringify({action:'meeting_notes',args:{event_id:n.m.id,...args}})})}
const calNotesMarks=d=>Object.fromEntries(['notes','transcript'].map(k=>[k,d?.[k]?{by:d[k].by,at:d[k].at,chars:d[k].chars}:undefined]));
function calNotesMark(m,marks){Object.assign(m,marks);for(const w of calWeeks.values())for(const x of w.meetings||[])if(x.id===m.id)Object.assign(x,marks);calRender()}
for(const [f,c] of Object.entries(CAL_FIELDS)){const q=id=>$('#cal-v-'+f+'-'+id);
 q('add').onclick=()=>calNotesEdit(f,'');
 q('edit').onclick=async()=>{const x=calNote?.data?.[c.api];if(x&&x.next_offset!=null){try{calNote.data=await request('api/meeting-notes?event='+encodeURIComponent(calNote.m.id))}catch{}}calNotesEdit(f)};
 q('cancel').onclick=()=>{if(!calNote)return;calNote.editing[f]=false;calNotesShow();calNotesFit()};
 // A file goes into the field it was picked in, as it is: nothing moves to the other field
 q('file').querySelector('input').onchange=async e=>{const file=e.target.files?.[0];e.target.value='';if(!file||!calNote)return;
  if(file.size>CAL_NOTES_FILE){toast(c.big,true);return}let text='';try{text=await file.text()}catch{toast('That file couldn’t be read.',true);return}
  if(calNote.editing[f]){const box=q('text');box.value=box.value.trim()?box.value.replace(/\s+$/,'')+'\n\n'+text:text}else calNotesEdit(f,text)};
 q('save').onclick=async e=>{const n=calNote,text=q('text').value;if(!n)return;if(!text.trim()){q('error').textContent=t(c.write);return}
  const b=e.currentTarget;b.disabled=true;try{await calNotesSend({field:c.api,text});n.data=await request('api/meeting-notes?event='+encodeURIComponent(n.m.id));n.editing[f]=false;
   calNotesMark(n.m,calNotesMarks(n.data));if(calNote===n){calNotesShow();calNotesFit()}toast(c.saved)}
  catch(err){errCaught(err);q('error').textContent=err.message||t(c.saveErr)}finally{b.disabled=false}};
 q('remove').onclick=async e=>{const n=calNote,b=e.currentTarget;if(!n)return;if(!b.classList.contains('sure')){b.classList.add('sure');b.textContent=t(c.sure);return}
  b.disabled=true;try{await calNotesSend({field:c.api,remove:true});n.data={...n.data,[c.api]:null};calNotesMark(n.m,calNotesMarks(n.data));if(calNote===n){calNotesShow();calNotesFit()}toast(c.removed)}
  catch(err){errCaught(err);toast(err.message||c.removeErr,true)}finally{b.disabled=false}}}
$('#cal-v-notes-gen').onclick=async e=>{const n=calNote,b=e.currentTarget;if(!n?.data)return;b.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'meeting_notes_write',args:{event_id:n.m.id}})});
  n.data={...n.data,writing:r.writing};if(calNote===n){calNotesShow();calNotesFit();calNotesPoll()}}
 catch(err){errCaught(err);toast(err.message||'Couldn’t write the notes. Try again.',true)}finally{b.disabled=false}};
for(const b of document.querySelectorAll('#cal-view [data-cal-close]'))b.onclick=()=>$('#cal-view').close();
$('#cal-v-rows').addEventListener('click',e=>{if(e.target.closest('a[href^="#graph"]'))$('#cal-view').close()});
// An event the owner can change opens its form; its notes are one tap away from there
$('#cal-f-notes').onclick=()=>{const m=calEdit?.m;if(!m)return;$('#cal-dialog').close();calView(m)};
function calOpen(el){if(el.dataset.calEdit){calEditor(Number(el.dataset.calEdit));return}const m=(calMeetings||[]).find(x=>x.id===Number(el.dataset.calView));if(m)calView(m)}
function calEditor(id){const m=id?(calMeetings||[]).find(x=>x.id===id):null;if(id&&!m?.edit)return;
 const sel=$('#cal-f-cal'),mine=m?calCals.filter(c=>c.id===m.account_id):calCals;if(!mine.length){toast('That calendar can’t be changed here.',true);return}
 sel.innerHTML=mine.map(c=>`<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('');sel.disabled=!!m||mine.length<2;
 const last=sideStore.get('cal-new-cal');if(!m&&mine.some(c=>c.id===last))sel.value=last;
 calEdit={id:m?.id||null,m,request:crypto.randomUUID(),sure:false};calGuests.length=0;$('#cal-f-invite').value='';calWhere.close();calInvite.close();
 $('#cal-dlg-title').textContent=m?'Change event':'New event';$('#cal-f-save').textContent=m?'Save':'Add';$('#cal-f-delete').hidden=!m;$('#cal-f-delete').textContent='Delete';$('#cal-f-delete').classList.remove('sure');
 $('#cal-f-title').value=m?m.title:'';$('#cal-f-where').value=m?m.location||'':'';$('#cal-f-notes').value='';$('#cal-f-notes-label').hidden=!!m;$('#cal-f-error').textContent='';
 $('#cal-f-notes').hidden=!m;$('#cal-f-notes').textContent=t(m?.notes?'See notes':'Add notes');
 $('#cal-f-open').hidden=!m?.url;if(m?.url){$('#cal-f-open').href=m.url;$('#cal-f-open').textContent=t(calOpenLabel(m.url))}
 if(m&&m.edit.all_day){$('#cal-f-date').value=m.edit.start;$('#cal-f-until').value=m.edit.end;$('#cal-f-start').value='09:00';$('#cal-f-end').value='10:00';calAllDay(true)}
 else{const now=new Date(),a=m?new Date(m.edit.start):new Date(now.getFullYear(),now.getMonth(),now.getDate()+(now.getHours()>=22?1:0),now.getHours()>=22?9:now.getHours()+1),b=m?new Date(m.edit.end):new Date(a.getTime()+36e5);
  const day=m?localDay(a):(calList()||calMode==='month'?localDay(a):localDay(calOnNow()?a:calMode==='week'&&!calThree()?calAt:calStart));
  $('#cal-f-date').value=day;$('#cal-f-start').value=calHM(a);$('#cal-f-end').value=calHM(b);$('#cal-f-until').value=m?localDay(b):day;calAllDay(false)}
 calEdit.before=calFormValues();calEdit.day=$('#cal-f-date').value;calGuestsShow();
 $('#cal-dialog').showModal();if(!m)$('#cal-f-title').focus()}
// Invite: only on the owner's own calendar. Who gets an invite is listed above the button, and the button says how
// many ("Add and invite 2"): Google sends the invitations on that tap, never before and never without it.
const calGuests=[],calEmail=v=>/^[^@\s<>(),;:"[\]]{1,64}@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$/.test(v);
function calGuestsShow(){const c=calCals.find(c=>c.id===(calEdit?.m?calEdit.m.account_id:$('#cal-f-cal').value)),can=!!c?.invite;
 if(!can)calGuests.length=0;$('#cal-f-invite-wrap').hidden=!can;
 $('#cal-f-guests').innerHTML=calGuests.map(g=>`<span class="cal-guest" role="listitem" title="${esc(g.email)}"><span>${esc(g.name||g.email)}</span><button type="button" data-guest="${esc(g.email)}" aria-label="Don’t invite ${esc(g.name||g.email)}">×</button></span>`).join('');
 const n=calGuests.length,m=calEdit?.m,fine=$('#cal-f-fine');
 $('#cal-f-save').textContent=n?(m?'Save and invite ':'Add and invite ')+n:m?'Save':'Add';
 fine.textContent=n?t('Invites go to {}.',calGuests.map(g=>g.email).join(', ')):m?'Only this event changes. Nobody gets an update.':'Nobody is invited.';fine.classList.toggle('cal-inviting',!!n)}
function calGuestAdd(g){const email=String(g.email||'').trim().toLowerCase();if(!calEmail(email))return false;
 if(!calGuests.some(x=>x.email===email))calGuests.push({email,name:g.name||''});$('#cal-f-invite').value='';calGuestsShow();return true}
// Suggestions under a field, as you type (a moment after the last key): arrows and Enter pick one, Escape closes them
function calSuggest(input,list,ask,render,pick,foot=()=>''){let timer=0,seq=0,items=[],at=-1;
 const show=()=>{list.innerHTML=items.map((it,i)=>`<li><button type="button" role="option" tabindex="-1" id="${list.id}-${i}" aria-selected="${i===at}" data-i="${i}">${render(it)}</button></li>`).join('')+foot(items);
  list.hidden=!items.length;input.setAttribute('aria-expanded',String(!!items.length));if(at>=0)input.setAttribute('aria-activedescendant',list.id+'-'+at);else input.removeAttribute('aria-activedescendant')};
 const close=()=>{clearTimeout(timer);seq++;items=[];at=-1;show()};
 input.addEventListener('input',()=>{clearTimeout(timer);const q=input.value.trim(),n=++seq;if(q.length<2){items=[];at=-1;show();return}
  timer=setTimeout(async()=>{let found=[];try{found=await ask(q)}catch{}if(n===seq){items=found;at=-1;show()}},300)});
 input.addEventListener('keydown',e=>{if(e.key==='Escape'&&items.length){e.preventDefault();close();return}if(!items.length)return;
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();at=e.key==='ArrowDown'?Math.min(at+1,items.length-1):Math.max(at-1,-1);show()}
  else if(e.key==='Enter'&&at>=0){e.preventDefault();e.stopImmediatePropagation();pick(items[at]);close()}});
 input.addEventListener('blur',()=>setTimeout(()=>{if(document.activeElement!==input)close()},200));
 list.addEventListener('pointerdown',e=>e.preventDefault());
 list.addEventListener('click',e=>{const b=e.target.closest('[data-i]');if(!b)return;pick(items[Number(b.dataset.i)]);close();input.focus()});
 return {close}}
// Where: places the owner used before and organizations in their Graph first, then addresses from OpenStreetMap
// (Photon). The Machine looks those up itself with only the typed text; the page never talks to the map service.
const calWhere=calSuggest($('#cal-f-where'),$('#cal-f-where-sug'),
 async q=>(await request('api/places?q='+encodeURIComponent(q))).places||[],
 p=>`<span>${esc(p.label)}</span>${p.detail?`<small>${esc(p.detail)}</small>`:''}`,p=>{$('#cal-f-where').value=p.value},
 items=>items.some(p=>p.source==='map')?'<li class="cal-sug-osm" role="presentation">Addresses © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener" tabindex="-1">OpenStreetMap</a></li>':'');
const calInvite=calSuggest($('#cal-f-invite'),$('#cal-f-invite-sug'),
 async q=>{const typed=q.toLowerCase(),r=((await request('api/invitees?q='+encodeURIComponent(q))).people||[]).filter(p=>!calGuests.some(g=>g.email===p.email));
  return calEmail(typed)&&!r.some(p=>p.email===typed)&&!calGuests.some(g=>g.email===typed)?[{email:typed,name:''},...r]:r},
 p=>p.name?`<span>${esc(p.name)}</span><small>${esc(p.email)}</small>`:`<span>${esc(p.email)}</span>`,calGuestAdd);
$('#cal-f-invite').addEventListener('keydown',e=>{const v=e.target.value.trim();
 if((e.key==='Enter'||e.key===','||e.key===';')&&v){e.preventDefault();if(calGuestAdd({email:v}))calInvite.close();else $('#cal-f-error').textContent='That isn’t an email address.'}
 else if(e.key==='Backspace'&&!e.target.value&&calGuests.length){calGuests.pop();calGuestsShow()}});
$('#cal-f-invite').addEventListener('paste',e=>{const words=(e.clipboardData?.getData('text')||'').split(/[\s,;<>]+/).filter(calEmail);if(words.length>1){e.preventDefault();for(const w of words)calGuestAdd({email:w})}});
$('#cal-f-guests').addEventListener('click',e=>{const b=e.target.closest('[data-guest]');if(!b)return;const i=calGuests.findIndex(g=>g.email===b.dataset.guest);if(i>=0)calGuests.splice(i,1);calGuestsShow();$('#cal-f-invite').focus()});
$('#cal-f-cal').addEventListener('change',calGuestsShow);
function calFormValues(){const all=$('#cal-f-allday').checked,day=$('#cal-f-date').value;
 return {title:$('#cal-f-title').value.trim(),location:$('#cal-f-where').value.trim(),notes:$('#cal-f-notes').value.trim(),all_day:all,
  start:all?day:calIso(day,$('#cal-f-start').value),end:all?($('#cal-f-until').value||day):calIso($('#cal-f-until').value||day,$('#cal-f-end').value)}}
async function calSave(op){const v=calFormValues(),e=calEdit,err=$('#cal-f-error');err.textContent='';
 if(op!=='delete'&&$('#cal-f-invite').value.trim()&&!$('#cal-f-invite-wrap').hidden){err.textContent='Add or clear the address under Invite.';$('#cal-f-invite').focus();return}
 if(op!=='delete'){if(!v.title){err.textContent='Give it a title.';return}if(!v.start||!v.end){err.textContent='Pick a date and times.';return}
  if(v.all_day?v.end<v.start:new Date(v.end)<=new Date(v.start)){err.textContent='It ends before it starts.';return}}
 const args={request_id:e.request,op};
 if(op==='create')Object.assign(args,{calendar:$('#cal-f-cal').value},v);
 else{args.event=e.id;if(op==='update'){const b=e.before;for(const k of ['title','location'])if(v[k]!==b[k])args[k]=v[k];
  if(v.start!==b.start||v.end!==b.end||v.all_day!==b.all_day)Object.assign(args,{start:v.start,end:v.end,all_day:v.all_day});
  if(calGuests.length)Object.assign(args,{guests:calGuests.map(g=>g.email),invite:calGuests.length});
  if(Object.keys(args).length<=3){$('#cal-dialog').close();return}}}
 if(op==='create'&&calGuests.length)Object.assign(args,{guests:calGuests.map(g=>g.email),invite:calGuests.length});
 const btn=op==='delete'?$('#cal-f-delete'):$('#cal-f-save');btn.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'calendar_write',args})});
  if(r.status!=='done'){err.textContent=r.error||'That didn’t go through.';return}
  if(op==='create')sideStore.set('cal-new-cal',args.calendar);
  $('#cal-dialog').close();{const cal=r.calendar||t('the calendar'),o=CAL_DID[op]?op:'update';toast(r.invited?t(CAL_DID_INV[o],cal,r.invited):t(CAL_DID_DOT[o],cal))}
  for(const ms of [2500,8000])setTimeout(()=>{if(!$('#calendar').hidden)calendarView(true)},ms)}
 catch(x){errCaught(x);err.textContent=x.message}finally{btn.disabled=false}}
$('#cal-form').addEventListener('input',()=>{$('#cal-f-error').textContent=''});
$('#cal-form').addEventListener('submit',e=>{e.preventDefault();calSave(calEdit?.id?'update':'create')});
$('#cal-f-allday').onchange=e=>{calAllDay(e.target.checked);if(e.target.checked&&$('#cal-f-until').value<$('#cal-f-date').value)$('#cal-f-until').value=$('#cal-f-date').value};
$('#cal-f-date').onchange=()=>{const date=$('#cal-f-date').value,until=$('#cal-f-until');if(until.value===calEdit?.day||until.value<date)until.value=date;if(calEdit)calEdit.day=date};
$('#cal-f-start').onchange=()=>{const a=$('#cal-f-start').value,b=$('#cal-f-end').value;if(a&&(!b||b<=a)){const [h,mi]=a.split(':').map(Number),t=Math.min(h*60+mi+60,23*60+55);$('#cal-f-end').value=calPad(Math.floor(t/60))+':'+calPad(t%60)}};
$('#cal-f-delete').onclick=()=>{const b=$('#cal-f-delete');if(!calEdit?.sure){calEdit.sure=true;b.textContent='Delete it';b.classList.add('sure');return}calSave('delete')};
for(const b of document.querySelectorAll('#cal-dialog [data-cal-close]'))b.onclick=()=>$('#cal-dialog').close();
$('#calendar').addEventListener('keydown',e=>{const ed=e.target.closest?.('[data-cal-edit],[data-cal-view]');if(ed&&(e.key==='Enter'||e.key===' ')){e.preventDefault();calOpen(ed)}});
