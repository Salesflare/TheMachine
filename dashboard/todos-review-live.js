// Reviews while they happen (Connections, above the finished ones; the first look also on Suggestions): what each running
// review is doing, from its own steps, and the next one. Polled every few seconds while one runs; a finished one moves to
// the lists below.
const REVIEW_ACTIVE=['starting','running','recovering'];
const FIRST_LOOK_WAIT={model:'It starts once your main model can run: sign in for it or add a key.',sources:'It starts once a source has brought in its first messages.',settling:'It starts in a few minutes, once the first import settles.',mail:'It starts when your mail is in.',retry:'The last try did not finish; it tries again shortly.',due:'Starting now.'};
// A first look whose tries keep failing (first_look.failing / first_dig.failing: tries in a row that failed, from the
// third on, as FIRST_LOOK_TRIES) says so in one line instead of "tries again shortly" or "Reading on"
const FL_KEEPS_FAILING=3,flFailing=f=>(+f?.failing|0)>=FL_KEEPS_FAILING;
const flWait=fl=>fl?.why==='retry'&&flFailing(fl)?t('The last tries did not finish. Still trying.'):t(FIRST_LOOK_WAIT[fl?.why]||'');
const firstLookDays=(fl,run)=>{const hours=run?run.window_hours:fl?.quick&&fl.hours;return hours?Math.max(1,Math.round(hours/24)):fl?.days||7};
function reviewLiveRows(live){const rows=[];const name=id=>{const c=(state.connectors||[]).find(c=>c.id===id);return c?(c.display_name||c.email||id):id};
for(const r of live.runs||[]){const total=r.planned||r.claimed_count||0,done=Math.min(r.done_count||0,total||Infinity);const steps=r.steps||[],[latest,...earlier]=steps;
const what=r.preview||r.promising||r.window_hours?t(r.preview&&!r.auto?'Preview: your last {} days':'First look: your last {} days',firstLookDays(live.first_look,r)):'Checking new messages';
rows.push(make('div',{class:'review-live','data-run':r.run_id},chipNode(r.status==='recovering'?'Paused':'Checking','amber'),
 make('span',{class:'grow'},what,total?[' · ',make('b',{},`${done} of ${total}`),' signals']:'',(r.account_ids||[]).length?' · '+[...new Set(r.account_ids.map(name))].join(', '):''),timeNode(r.started_at),'\n',
 latest?make('ul',{class:'steps','aria-live':'polite'},make('li',{},latest.title)):make('p',{class:'muted'},'Starting…'),
 earlier.length?make('details',{class:'earlier-steps'},make('summary',{},'Earlier steps'),make('ul',{class:'steps'},earlier.map(x=>make('li',{},x.title)))):'',
 r.preview?make('small',{},'A preview: to-dos show under To-dos, and nothing is sent or done.'):''))}
if(!(live.runs||[]).length&&startsByItself()){if(!setupStep())rows.push(make('div',{class:'review-live queued'},chipNode(aiConnecting()?'Connecting':'Starting','lavender'),make('span',{class:'grow'},setupLine())));return rows}
if(!(live.runs||[]).length&&state.reviews_on===false){const on=turnOn(),fl=live.first_look;
 rows.push(make('div',{class:'review-live queued'},chipNode('Off','orange'),make('span',{class:'grow'},t('Checks are off.'),fl?.state==='waiting'?` ${t('A first look at your last {} days comes first.',firstLookDays(fl))} ${flWait(fl)}`:''),
  on.url?make('a',{class:'head-link',href:on.url},on.action):make('code',{},'./install.sh --activate')));return rows}
if(!(live.runs||[]).length&&live.queue){const q=live.queue,n=()=>q.waiting.toLocaleString(DL);
 rows.push(make('div',{class:'review-live queued'},chipNode(q.first?'First':'Next','lavender'),
  make('span',{class:'grow'},q.why==='mail'?(q.first?t('First check starts when your mail is in'):t('Next check starts when your new mail is in')):q.first?t(['{} message waiting for its first check','{} messages waiting for their first check'],n()):t(['{} message waiting for the next check','{} messages waiting for the next check'],n())),
  make('small',{},q.why==='mail'?(q.waiting?t(['{} message so far','{} messages so far'],n()):'Importing your mail'):q.why==='mail_in'?'Your mail is in. Starting now':`Starts ${ago(q.starts_at)}`)))}
if(!(live.runs||[]).length&&live.first_look?.state==='waiting')rows.push(make('div',{class:'review-live queued'},chipNode('First look','lavender'),make('span',{class:'grow'},`A first check of your last ${live.first_look.days} days`),make('small',{},flWait(live.first_look))));
return rows}
// The first look (a review of the last days, right after setup): while there are no cards yet it is the empty
// state itself; once cards come in, a slim progress strip under the counters.
// Also with reviews off (where the first look happens): waiting for it is not "All clear".
// A batch saves what it read at its end. In between only the bar moves, at the pace the earlier batches took
// (first_dig.pace), one signal short of the batch until it saved, and never back. The number in the line is what its
// batches saved, never a guess: a count ticking up a signal every few seconds said "Reading 11 of 132" while nothing
// had been read yet, and its sliver of a bar looked stuck (2026-11-09). The line names the batch in hand instead.
const flSeen=new Map();let flPeak=0,flTotal=0,flRead=0;
const flInt=v=>Math.max(0,+v|0),flLeft=run=>run?Math.max(0,(run.planned||run.claimed_count||0)-(run.done_count||0)):0;
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
if(dig&&dig.total){const total=flTotal=Math.max(flTotal,0,+dig.total|0),todos=+dig.todos|0,ahead=run?Math.max(0,flRunDone(run,dig.pace)-(run.done_count||0)):0,read=flRead=Math.min(total,Math.max(flRead,flInt(dig.read))),done=Math.min(total,Math.max(flPeak,read+ahead));flPeak=done;flMark();
 const first=todos===1&&typeof dig.first?.title==='string'&&dig.first.title.trim();
 return{title:t('Taking a first look at your last {} days',dig.days||7),done,read,batch:Math.min(flLeft(run),total-read),total,unit:dig.unit,first:!!first&&!(!run&&dig.failing),names:Array.isArray(dig.names)?dig.names.filter(n=>typeof n==='string'&&n.trim()):[],
  wait:!run&&dig.failing?(flFailing(dig)?t('The last tries did not finish. Still trying.'):t(FIRST_LOOK_WAIT.retry)):first?t('First one’s in: {}. Still reading…',first):!dig.read&&!run?.done_count?'':todos?t(['Found {} to-do. Reading on.','Found {} to-dos. Reading on.'],todos):t('Nothing for you yet. Reading on.')}}
// A batch still ending after the first look stopped digging (first_look_done) is not a new count: its own "9 of 40" after
// "30 of 132" looked like it went back (2026-11-09); the ending's line says what it read
if(run&&state.first_look_done&&!(run.started_at>state.first_look_done.at))return null;
if(run){const total=run.planned||run.claimed_count||0;flMark();return{title:t('Taking a first look at your last {} days',firstLookDays(fl,run)),done:flRunDone(run,6),read:Math.min(total,flInt(run.done_count)),batch:flLeft(run),total}}
if(startsByItself()&&fl?.state!=='due')return setupStep()?{title:t('Your first to-dos show up here'),wait:false}:flBack()?{title:t('Taking a first look at your last {} days',firstLookDays(fl))}:{title:setupLine(),working:!!aiConnecting()};  // not "All clear" before the first read ends
if((fl?.state==='waiting'&&fl.why!=='model')||fl?.state==='due')return{title:t('A first look at your last {} days starts soon',firstLookDays(fl)),wait:fl.state==='due'?t(FIRST_LOOK_WAIT.due):flWait(fl)};return null}
// the counts are whole numbers before they reach the page, whatever the status says
// How far it read, in the robot's voice (messages when not every source is mail). read is what its batches saved
// (i.read; a bar drawn without one reads its done), batch the size of the one it reads now: "Reading the first 20 of 132
// emails…", then "Read 20 of 132 emails. Reading the next 40…", and "Reading 60 of 132 emails…" between two batches
const FL_COUNT={email:['Reading {} of {} emails…','Reading the first {} of {} emails…','Read {} of {} emails. Reading the next {}…',['Reading {} email…','Reading {} emails…']],
 message:['Reading {} of {} messages…','Reading the first {} of {} messages…','Read {} of {} messages. Reading the next {}…',['Reading {} message…','Reading {} messages…']]};
const flReadOf=i=>Math.min(flInt(i.done),flInt(i.read??i.done));
function flCount(i){const w=FL_COUNT[i.unit==='email'?'email':'message'],n=v=>v.toLocaleString(DL),total=flInt(i.total),read=flReadOf(i),batch=Math.min(flInt(i.batch),total-read);
 return read?batch?t(w[2],n(read),n(total),n(batch)):t(w[0],n(read),n(total)):batch&&batch<total?t(w[1],n(batch),n(total)):t(w[3],total===1?1:n(total))}
// The bar is where it is by now (i.done: what was read plus the time the batch in hand has taken), its value what was read
const firstLookBar=i=>{const done=flInt(i.done),total=flInt(i.total);return total?[make('span',{class:'fl-bar'+(i.batch?' fl-on':''),role:'progressbar','aria-label':'Signals checked','aria-valuemin':'0','aria-valuemax':total,'aria-valuenow':flReadOf(i)},
 make('i',{style:{width:Math.round(100*done/total)+'%'}})),make('span',{class:'fl-count'},flCount(i))]:[]};
// Who it reads about (first_dig.names: the owner's own people and organizations, never a word of a message), one more
// every few seconds up to three, so they show up as it finds them
let flNamesAt=0;
function flNames(i){const names=(i.names||[]).slice(0,3);if(!names.length){flNamesAt=0;return ''}flNamesAt||=Date.now();
 const shown=names.slice(0,Math.min(names.length,1+Math.floor((Date.now()-flNamesAt)/4000)));let list;
 try{list=new Intl.ListFormat(I18N.lang||'en',{type:'conjunction'}).format(shown)}catch{list=shown.join(', ')}return t('Bumped into {} so far.',list)}
const flNamesNode=i=>{const line=flNames(i);return line?make('span',{class:'fl-names',translate:'no'},line):''};
const firstLookInner=i=>[make('img',{class:'sticker',src:'brand/wave.webp','data-blink':'brand/wave-blink.webp','data-look':'brand/wave-look.webp','data-hand':'brand/wave-hand.webp',alt:''}),make('div',{},make('strong',i.working?{class:'backfill-run'}:{},i.title),firstLookBar(i),flNamesNode(i),i.wait===false?'':make('small',{},i.wait||(firstEta()?t('First to-dos in about {} min.',firstEta()):t('To-dos show up here as they come.'))))];
// The list's empty state while the first look runs: a place the list fills with firstLookFill once it is on the page
const firstLookEmpty=i=>i?html`<div class="empty all-clear first-look-empty"></div>`:'';
function firstLookFill(){const box=$('#suggestions .first-look-empty'),i=box&&firstLookInfo(state.review_live||{});if(i)box.replaceChildren(...firstLookInner(i))}
// The first look's ending (state.first_look_done): what it read, in counts, so an empty list says what the Machine did,
// with one or two next steps that fit this setup. With to-dos, one line above them. Counts only, never a message.
// Meetings are said with the kinds, so the reviewer's groups list only what the messages were.
const FL_KINDS=[['email',['{} email','{} emails']],['meeting',['{} meeting','{} meetings']],['message',['{} message','{} messages']],['other',['{} other signal','{} other signals']]];
const FL_READ=[['people',['{} from a person','{} from people']],['newsletters',['{} newsletter','{} newsletters']],['notifications',['{} notification','{} notifications']],['other',['{} other','{} other']]];
const flList=(counts,words)=>{const parts=words.filter(([k])=>(+counts?.[k]|0)>0).map(([k,w])=>t(w,+counts[k]|0).replace(/^(\d+) /,'$1\u00a0'));try{return new Intl.ListFormat(I18N.lang||'en',{type:'conjunction'}).format(parts)}catch{return parts.join(', ')}};
// Concrete offers first, never an empty ask while there is one: a source that mails the owner often (d.connect, "Connect
// Slack"), the setup steps that fit; then one question to ask (Search's ask), else Talk or a to-do of their own.
const FL_NEXT={calendar:'Connect your calendar',inbox:'Add another inbox',ask:'Ask what changed this week',talk:'Talk to me',todo:'Give me a to-do'};
function flNext(d){const steps=[...(d.connect||[]).map(c=>({key:'connect',service:c.service,label:t('Connect {}',c.label)})),
  ...(d.next||[]).filter(k=>k==='calendar'||k==='inbox').map(k=>({key:k,label:t(FL_NEXT[k])}))];
 const last=typeof palAskable==='function'&&palAskable()?'ask':typeof talkOk==='function'&&talkOk()?'talk':'todo';
 return [...steps,{key:last,label:t(FL_NEXT[last])}].slice(0,2)}
// Where what it learned lives
const flLearned=()=>html`<a class="link fl-learned" href="#learning=learned">${t('See what I’ve learned')}</a>`;
function firstLookEnd(){const d=state.first_look_done;if(!d||d.todos>0)return '';const kinds=flList(d.kinds,FL_KINDS),read=flList(d.read,FL_READ);
 const line=!kinds?t('Nothing came in from the past week yet.'):read?t('Read {} from the past week: {}.',kinds,read):t('Read {} from the past week.',kinds);
 return html`<div class="empty all-clear first-look-end"><img class="sticker" src="brand/wave.webp" alt=""><div><span class="fl-read">${line}</span>${state.reviews_on?html`<small>${t('New mail gets a look as it comes in.')}</small>`:''}${flLearned()}</div><div class="fl-next">${flNext(d).map((x,i)=>x.service?html`<button type="button" class="${i?'quiet':''}" data-connect-open="${x.service}">${x.label}</button>`:html`<button type="button" class="${i?'quiet':''}" data-fl-next="${x.key}">${x.label}</button>`)}</div></div>`}
function firstLookNote(shown){const d=state.first_look_done;if(!d||!d.todos||d.acted||!shown||scopeFilter!=='all')return '';const kinds=flList(d.kinds,FL_KINDS);if(!kinds)return '';
 return html`<p class="first-look-note">${t(['Read {} from the past week and found {} to-do.','Read {} from the past week and found {} to-dos.'],kinds,d.todos)} ${flLearned()}</p>`}
$('#suggestions').addEventListener('click',e=>{const b=e.target.closest('[data-fl-next]');if(!b)return;const k=b.dataset.flNext;
 if(k==='talk'){talkMain();return}if(k==='todo'){ncOpen();return}if(k==='ask'){palOpen();pal.hint={q:t('what changed this week?')};palTry();return}showTab('health','add');connectAdd(true)});
function renderFirstLook(live){const i=firstLookInfo(live),el=$('#first-look'),empty=$('#suggestions .all-clear');
if(empty){el.hidden=true;if(i){empty.classList.add('first-look-empty');empty.replaceChildren(...firstLookInner(i))}else if(empty.classList.contains('first-look-empty'))refresh();return}
if(i){el.replaceChildren(make('strong',{},i.title),...firstLookBar(i),flNamesNode(i),i.wait?make('small',i.first?{class:'fl-first'}:{},i.wait):'');el.hidden=false}else el.hidden=true}
// The bar moves between polls: only the bar, its line and the names found change, a second at a time
function firstLookTick(){if(document.hidden||!state)return;const i=firstLookInfo(state.review_live||{});if(!i?.total)return;
 for(const box of document.querySelectorAll('#first-look,#suggestions .first-look-empty')){const bar=box.querySelector('.fl-bar'),count=box.querySelector('.fl-count');if(!bar||!count)continue;
  const done=flInt(i.done),total=Math.max(1,flInt(i.total)),said=flCount(i);bar.classList.toggle('fl-on',!!i.batch);bar.setAttribute('aria-valuenow',flReadOf(i));bar.setAttribute('aria-valuemax',total);bar.firstChild.style.width=Math.round(100*done/total)+'%';if(count.textContent!==said)count.textContent=said;
  const names=box.querySelector('.fl-names'),line=flNames(i);if(names&&line&&names.textContent!==line)names.textContent=line;else if(!names&&line)count.after(flNamesNode(i))}}
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
