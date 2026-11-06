// Reviews while they happen (Connections, above the finished ones; the first look also on Suggestions): what each running
// review is doing, from its own steps, and the next one. Polled every few seconds while one runs; a finished one moves to
// the lists below.
const REVIEW_ACTIVE=['starting','running','recovering'];
const FIRST_LOOK_WAIT={model:'It starts once your main model can run: sign in for it or add a key.',sources:'It starts once a source has brought in its first messages.',settling:'It starts in a few minutes, once the first import settles.',mail:'It starts when your mail is in.',retry:'The last try did not finish; it tries again shortly.',due:'Starting now.'};
const firstLookDays=(fl,run)=>{const hours=run?run.window_hours:fl?.quick&&fl.hours;return hours?Math.max(1,Math.round(hours/24)):fl?.days||7};
function reviewLiveRows(live){const rows=[];const name=id=>{const c=(state.connectors||[]).find(c=>c.id===id);return c?(c.display_name||c.email||id):id};
for(const r of live.runs||[]){const total=r.planned||r.claimed_count||0,done=Math.min(r.done_count||0,total||Infinity);const steps=r.steps||[],[latest,...earlier]=steps;
const what=r.preview||r.promising||r.window_hours?t(r.preview&&!r.auto?'Preview: your last {} days':'First look: your last {} days',firstLookDays(live.first_look,r)):'Reviewing new messages';
rows.push(make('div',{class:'review-live','data-run':r.run_id},chipNode(r.status==='recovering'?'Paused':'Reviewing','amber'),
 make('span',{class:'grow'},what,total?[' · ',make('b',{},`${done} of ${total}`),' signals']:'',(r.account_ids||[]).length?' · '+[...new Set(r.account_ids.map(name))].join(', '):''),timeNode(r.started_at),'\n',
 latest?make('ul',{class:'steps','aria-live':'polite'},make('li',{},latest.title)):make('p',{class:'muted'},'Starting…'),
 earlier.length?make('details',{class:'earlier-steps'},make('summary',{},'Earlier steps'),make('ul',{class:'steps'},earlier.map(x=>make('li',{},x.title)))):'',
 r.preview?make('small',{},'A preview: to-dos show under To-dos, and nothing is sent or done.'):''))}
if(!(live.runs||[]).length&&startsByItself()){if(!setupStep())rows.push(make('div',{class:'review-live queued'},chipNode(aiConnecting()?'Connecting':'Starting','lavender'),make('span',{class:'grow'},setupLine())));return rows}
if(!(live.runs||[]).length&&state.reviews_on===false){const on=turnOn(),fl=live.first_look;
 rows.push(make('div',{class:'review-live queued'},chipNode('Off','orange'),make('span',{class:'grow'},t('Reviews are off.'),fl?.state==='waiting'?` ${t('A first look at your last {} days comes first.',firstLookDays(fl))} ${t(FIRST_LOOK_WAIT[fl.why]||'')}`:''),
  on.url?make('a',{class:'head-link',href:on.url},on.action):make('code',{},'./install.sh --activate')));return rows}
if(!(live.runs||[]).length&&live.queue){const q=live.queue,n=()=>q.waiting.toLocaleString(DL);
 rows.push(make('div',{class:'review-live queued'},chipNode(q.first?'First':'Next','lavender'),
  make('span',{class:'grow'},q.why==='mail'?(q.first?t('First review starts when your mail is in'):t('Next review starts when your new mail is in')):q.first?t(['{} message waiting for its first review','{} messages waiting for their first review'],n()):t(['{} message waiting for the next review','{} messages waiting for the next review'],n())),
  make('small',{},q.why==='mail'?(q.waiting?t(['{} message so far','{} messages so far'],n()):'Importing your mail'):q.why==='mail_in'?'Your mail is in. Starting now':`Starts ${ago(q.starts_at)}`)))}
if(!(live.runs||[]).length&&live.first_look?.state==='waiting')rows.push(make('div',{class:'review-live queued'},chipNode('First look','lavender'),make('span',{class:'grow'},`A first review of your last ${live.first_look.days} days`),make('small',{},FIRST_LOOK_WAIT[live.first_look.why]||'')));
return rows}
// The first look (a review of the last days, right after setup): while there are no cards yet it is the empty
// state itself; once cards come in, a slim progress strip under the counters.
// Also with reviews off (where the first look happens): waiting for it is not "All clear".
// A batch saves what it read at its end, so in between its count moves a signal at a time at the pace the earlier
// batches took (first_dig.pace), one short of its size until it saved; the bar never moves back.
const flSeen=new Map();let flPeak=0,flTotal=0;
// Once this device saw the first look start, a screen drawn from an older copy (a reload while the Machine restarts as
// reviews turn on) never goes back to "Connecting ChatGPT…": it says the first look is on, without a count
const FL_SEEN_KEY='first-look-seen',flSeenAt=()=>{try{return +localStorage.getItem(FL_SEEN_KEY)||0}catch{return 0}};
const flBack=()=>Date.now()-flSeenAt()<36e5&&!state.first_look_done&&(!!aiConnecting()||shownCached||netDown);
function flMark(){if(Date.now()-flSeenAt()<6e4)return;try{localStorage.setItem(FL_SEEN_KEY,String(Date.now()))}catch{}}
function flRunDone(run,pace){const total=run.planned||run.claimed_count||0,real=Math.min(run.done_count||0,total);if(!total)return 0;
 const start=Math.min(flSeen.get(run.run_id)??Infinity,Date.now()-1000*(+run.duration_seconds||0));flSeen.set(run.run_id,start);
 return Math.max(real,Math.min(total-1,Math.floor((Date.now()-start)/1000/Math.max(1,+pace||6))))}
// While it digs (live.first_dig): one bar over the whole week, also between its batches, until it has its to-dos or read the week
function firstLookInfo(live){const run=(live.runs||[]).find(r=>r.preview||r.window_hours||r.promising),fl=live.first_look,dig=live.first_dig;
// read already counts what a running batch saved (its done_count), so only the batch's estimate beyond that is added;
// the total only grows (new mail), so the count never looks like it went back
if(dig&&dig.total){const total=flTotal=Math.max(flTotal,0,+dig.total|0),todos=+dig.todos|0,ahead=run?Math.max(0,flRunDone(run,dig.pace)-(run.done_count||0)):0,done=Math.min(total,Math.max(flPeak,(+dig.read|0)+ahead));flPeak=done;flMark();
 return{title:t('Taking a first look at your last {} days',dig.days||7),done,total,wait:!dig.read&&!run?.done_count?'':todos?t(['Found {} to-do. Reading on.','Found {} to-dos. Reading on.'],todos):t('Nothing for you yet. Reading on.')}}
if(run){const total=run.planned||run.claimed_count||0;flMark();return{title:t('Taking a first look at your last {} days',firstLookDays(fl,run)),done:flRunDone(run,6),total}}
if(startsByItself()&&fl?.state!=='due')return setupStep()?{title:t('Your first to-dos show up here'),wait:false}:flBack()?{title:t('Taking a first look at your last {} days',firstLookDays(fl))}:{title:setupLine(),working:!!aiConnecting()};  // not "All clear" before the first read ends
if((fl?.state==='waiting'&&fl.why!=='model')||fl?.state==='due')return{title:t('A first look at your last {} days starts soon',firstLookDays(fl)),wait:FIRST_LOOK_WAIT[fl.state==='due'?'due':fl.why]||''};return null}
// the counts are whole numbers before they reach the page, whatever the status says
const firstLookBar=i=>{const done=Math.max(0,+i.done|0),total=Math.max(0,+i.total|0);return total?[make('span',{class:'fl-bar',role:'progressbar','aria-label':'Signals reviewed','aria-valuemin':'0','aria-valuemax':total,'aria-valuenow':done},
 make('i',{style:{width:Math.round(100*done/total)+'%'}})),make('span',{class:'fl-count mono'},t('{} of {} signals',done,total))]:[]};
const firstLookInner=i=>[make('img',{class:'sticker',src:'brand/wave.webp','data-blink':'brand/wave-blink.webp','data-look':'brand/wave-look.webp','data-hand':'brand/wave-hand.webp',alt:''}),make('div',{},make('strong',i.working?{class:'backfill-run'}:{},i.title),firstLookBar(i),i.wait===false?'':make('small',{},i.wait||t('To-dos show up here as they come.')))];
// The list's empty state while the first look runs: a place the list fills with firstLookFill once it is on the page
const firstLookEmpty=i=>i?html`<div class="empty all-clear first-look-empty"></div>`:'';
function firstLookFill(){const box=$('#suggestions .first-look-empty'),i=box&&firstLookInfo(state.review_live||{});if(i)box.replaceChildren(...firstLookInner(i))}
// The first look's ending (state.first_look_done): what it read, in counts, so an empty list says what the Machine did,
// with one or two next steps that fit this setup. With to-dos, one line above them. Counts only, never a message.
// Meetings are said with the kinds, so the reviewer's groups list only what the messages were.
const FL_KINDS=[['email',['{} email','{} emails']],['meeting',['{} meeting','{} meetings']],['message',['{} message','{} messages']],['other',['{} other signal','{} other signals']]];
const FL_READ=[['people',['{} from a person','{} from people']],['newsletters',['{} newsletter','{} newsletters']],['notifications',['{} notification','{} notifications']],['other',['{} other','{} other']]];
const flList=(counts,words)=>{const parts=words.filter(([k])=>(+counts?.[k]|0)>0).map(([k,w])=>t(w,+counts[k]|0).replace(/^(\d+) /,'$1\u00a0'));try{return new Intl.ListFormat(I18N.lang||'en',{type:'conjunction'}).format(parts)}catch{return parts.join(', ')}};
const FL_NEXT={calendar:'Connect your calendar',inbox:'Add another inbox',talk:'Talk to me',todo:'Give me a to-do'};
function flNext(d){const steps=[...(d.next||[]).filter(k=>k==='calendar'||k==='inbox'),typeof talkOk==='function'&&talkOk()?'talk':'todo'];return steps.slice(0,2)}
function firstLookEnd(){const d=state.first_look_done;if(!d||d.todos>0)return '';const kinds=flList(d.kinds,FL_KINDS),read=flList(d.read,FL_READ);
 const line=!kinds?t('Nothing came in from the past week yet.'):read?t('Read {} from the past week: {}.',kinds,read):t('Read {} from the past week.',kinds);
 return html`<div class="empty all-clear first-look-end"><img class="sticker" src="brand/wave.webp" alt=""><div><span class="fl-read">${line}</span>${state.reviews_on?html`<small>${t('New mail gets a look as it comes in.')}</small>`:''}</div><div class="fl-next">${flNext(d).map((k,i)=>html`<button type="button" class="${i?'quiet':''}" data-fl-next="${k}">${t(FL_NEXT[k])}</button>`)}</div></div>`}
function firstLookNote(shown){const d=state.first_look_done;if(!d||!d.todos||d.acted||!shown||scopeFilter!=='all')return '';const kinds=flList(d.kinds,FL_KINDS);if(!kinds)return '';
 return html`<p class="first-look-note">${t(['Read {} from the past week and found {} to-do.','Read {} from the past week and found {} to-dos.'],kinds,d.todos)}</p>`}
$('#suggestions').addEventListener('click',e=>{const b=e.target.closest('[data-fl-next]');if(!b)return;const k=b.dataset.flNext;
 if(k==='talk'){talkMain();return}if(k==='todo'){ncOpen();return}showTab('health','add');connectAdd(true)});
function renderFirstLook(live){const i=firstLookInfo(live),el=$('#first-look'),empty=$('#suggestions .all-clear');
if(empty){el.hidden=true;if(i){empty.classList.add('first-look-empty');empty.replaceChildren(...firstLookInner(i))}else if(empty.classList.contains('first-look-empty'))refresh();return}
if(i){el.replaceChildren(make('strong',{},i.title),...firstLookBar(i),i.wait?make('small',{},i.wait):'');el.hidden=false}else el.hidden=true}
// The count ticks between polls: only the bar and its number change, a second at a time
function firstLookTick(){if(document.hidden||!state)return;const i=firstLookInfo(state.review_live||{});if(!i?.total)return;
 for(const box of document.querySelectorAll('#first-look,#suggestions .first-look-empty')){const bar=box.querySelector('.fl-bar'),count=box.querySelector('.fl-count');if(!bar||!count)continue;
  const done=Math.max(0,+i.done|0),total=Math.max(1,+i.total|0);bar.setAttribute('aria-valuenow',done);bar.setAttribute('aria-valuemax',total);bar.firstChild.style.width=Math.round(100*done/total)+'%';count.textContent=t('{} of {} signals',done,total)}}
setInterval(firstLookTick,1000);
function renderReviewLive(){const live=state.review_live||{},rows=reviewLiveRows(live);$('#review-live').replaceChildren(...rows);const none=$('#analyses .no-reviews');if(none)none.hidden=!!rows.length;renderFirstLook(live)}
let reviewWasLive=false,cardWaiting=false;
// While a review runs, or the first look is about to start, look every 5 s; a card a running review just saved shows at once
// A hosted Machine waiting for its AI is looked at too: the sign-in on its setup page ends any moment, and the page
// moves on by itself (a full refresh once the model can run, so reviews turning on shows as well)
const waitingForAI=()=>!!state?.manage_url&&state.reviews_on===false&&state.review_live?.first_look?.why==='model';
const firstLookPending=()=>['due','waiting'].includes(state?.review_live?.first_look?.state)&&state.review_live.first_look.why!=='model'||!!state?.review_live?.first_dig||waitingForAI();
setInterval(async()=>{if(document.hidden||!state||!((state.review_live?.runs||[]).length||reviewWasLive||cardWaiting||firstLookPending()))return;try{const live=await request('api/reviews/live');const running=(live.runs||[]).length;
const before=state.review_live?.cards,fresh=live.cards&&before&&(live.cards.newest!==before.newest||live.cards.count!==before.count);
if(fresh&&!canRefresh()){reviewWasLive=!!running;cardWaiting=true;state.review_live={...live,cards:before};renderReviewLive();return}  // typing: on the next look, also once the review ended
const aiReady=waitingForAI()&&live.first_look?.why!=='model',aiChanged=(live.ai_connecting?.name||null)!==(state.review_live?.ai_connecting?.name||null);
if((!running&&reviewWasLive)||fresh||aiReady){reviewWasLive=!!running;cardWaiting=false;state.review_live=live;refresh();return}cardWaiting=false;reviewWasLive=!!running;state.review_live=live;renderReviewLive();if(aiChanged)renderNeedsYou()}catch(e){}},5000);
