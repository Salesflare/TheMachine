// Reviews while they happen (Connections, above the finished ones; the first look also on Suggestions): what each running
// review is doing, from its own steps, and the next one. Polled every few seconds while one runs; a finished one moves to
// the lists below.
const REVIEW_ACTIVE=['starting','running','recovering'];
const FIRST_LOOK_WAIT={model:'It starts once your main model can run: sign in for it or add a key.',sources:'It starts once a source has brought in its first messages.',settling:'It starts in a few minutes, once the first import settles.',mail:'It starts when your mail is in.',retry:'The last try did not finish; it tries again shortly.',due:'Starting now.'};
const firstLookDays=(fl,run)=>{const hours=run?run.window_hours:fl?.quick&&fl.hours;return hours?Math.max(1,Math.round(hours/24)):fl?.days||7};
function reviewLiveRows(live){const rows=[];const name=id=>{const c=(state.connectors||[]).find(c=>c.id===id);return c?(c.display_name||c.email||id):id};
for(const r of live.runs||[]){const total=r.planned||r.claimed_count||0,done=Math.min(r.done_count||0,total||Infinity);const steps=r.steps||[],[latest,...earlier]=steps;
const what=r.preview?t(r.auto?'First look: your last {} days':'Preview: your last {} days',firstLookDays(live.first_look,r)):'Reviewing new messages';
rows.push(make('div',{class:'review-live','data-run':r.run_id},chipNode(r.status==='recovering'?'Waiting for OpenClaw':'Reviewing','amber'),
 make('span',{class:'grow'},what,total?[' · ',make('b',{},`${done} of ${total}`),' signals']:'',(r.account_ids||[]).length?' · '+[...new Set(r.account_ids.map(name))].join(', '):''),timeNode(r.started_at),'\n',
 latest?make('ul',{class:'steps','aria-live':'polite'},make('li',{},latest.title)):make('p',{class:'muted'},'Starting…'),
 earlier.length?make('details',{class:'earlier-steps'},make('summary',{},'Earlier steps'),make('ul',{class:'steps'},earlier.map(x=>make('li',{},x.title)))):'',
 r.preview?make('small',{},'A preview: to-dos show under To-dos, and nothing is sent or done.'):''))}
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
function firstLookInfo(live){const run=(live.runs||[]).find(r=>r.preview||r.window_hours),fl=live.first_look;
if(run){const total=run.planned||run.claimed_count||0;return{title:t('Taking a first look at your last {} days',firstLookDays(fl,run)),done:Math.min(run.done_count||0,total),total}}
if((fl?.state==='waiting'&&fl.why!=='model')||fl?.state==='due')return{title:t('A first look at your last {} days starts soon',firstLookDays(fl)),wait:FIRST_LOOK_WAIT[fl.state==='due'?'due':fl.why]||''};return null}
// the counts are whole numbers before they reach the page, whatever the status says
const firstLookBar=i=>{const done=Math.max(0,+i.done|0),total=Math.max(0,+i.total|0);return total?[make('span',{class:'fl-bar',role:'progressbar','aria-label':'Signals reviewed','aria-valuemin':'0','aria-valuemax':total,'aria-valuenow':done},
 make('i',{style:{width:Math.round(100*done/total)+'%'}})),make('span',{class:'fl-count mono'},`${done} of ${total} signals`)]:[]};
const firstLookInner=i=>[make('img',{class:'sticker',src:'brand/wave.webp',alt:''}),make('div',{},make('strong',{},i.title),firstLookBar(i),make('small',{},i.wait||'To-dos show up here as they come. Nothing is sent.'))];
// The list's empty state while the first look runs: a place the list fills with firstLookFill once it is on the page
const firstLookEmpty=i=>i?'<div class="empty all-clear first-look-empty"></div>':'';
function firstLookFill(){const box=$('#suggestions .first-look-empty'),i=box&&firstLookInfo(state.review_live||{});if(i)box.replaceChildren(...firstLookInner(i))}
function renderFirstLook(live){const i=firstLookInfo(live),el=$('#first-look'),empty=$('#suggestions .all-clear');
if(empty){el.hidden=true;if(i){empty.classList.add('first-look-empty');empty.replaceChildren(...firstLookInner(i))}else if(empty.classList.contains('first-look-empty'))refresh();return}
if(i){el.replaceChildren(make('strong',{},i.title),...firstLookBar(i),i.wait?make('small',{},i.wait):'');el.hidden=false}else el.hidden=true}
function renderReviewLive(){const live=state.review_live||{},rows=reviewLiveRows(live);$('#review-live').replaceChildren(...rows);const none=$('#analyses .no-reviews');if(none)none.hidden=!!rows.length;renderFirstLook(live)}
let reviewWasLive=false,cardWaiting=false;
// While a review runs, or the first look is about to start, look every 5 s; a card a running review just saved shows at once
const firstLookPending=()=>['due','waiting'].includes(state?.review_live?.first_look?.state)&&state.review_live.first_look.why!=='model';
setInterval(async()=>{if(document.hidden||!state||!((state.review_live?.runs||[]).length||reviewWasLive||cardWaiting||firstLookPending()))return;try{const live=await request('api/reviews/live');const running=(live.runs||[]).length;
const before=state.review_live?.cards,fresh=live.cards&&before&&(live.cards.newest!==before.newest||live.cards.count!==before.count);
if(fresh&&!canRefresh()){reviewWasLive=!!running;cardWaiting=true;state.review_live={...live,cards:before};renderReviewLive();return}  // typing: on the next look, also once the review ended
if((!running&&reviewWasLive)||fresh){reviewWasLive=!!running;cardWaiting=false;state.review_live=live;refresh();return}cardWaiting=false;reviewWasLive=!!running;state.review_live=live;renderReviewLive()}catch(e){}},5000);
