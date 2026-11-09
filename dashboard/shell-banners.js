// The AI sign-in's own limits (ChatGPT: 5 hours and weekly), as OpenClaw reports them; reset times in this browser's time zone.
// The model in Settings: which one, the plan's windows with when each starts over, a reached limit, and the
// usage limit resets (ChatGPT). Readings are cached on the server, never a model call by themselves.
const untilText=t=>{let s=Math.max(60,t-Date.now()/1000|0),d=s/86400|0,h=s%86400/3600|0,m=s%3600/60|0;return d?`${d}d${h?` ${h}h`:''}`:h?`${h}h${m?` ${m}m`:''}`:`${m}m`};
const clockAt=t=>{const r=new Date(t*1000),c=fmtHM(r);return t-Date.now()/1000>86400?`${localeDate(r,DL,{weekday:'short'})} ${c}`:c};
const windowLabel=l=>['Week','168h','7d'].includes(l)?t('Weekly limit'):['Day','24h'].includes(l)?t('Daily limit'):/^\d+h$/.test(l)?t('{}-hour limit',parseInt(l)):l;
function resetAction(m){if(!m)return '';if(m.can_reset)return html`<button type="button" class="ghost" data-model-reset>Use a reset</button>`;
 const href=safeURL(m.usage_page);  // only a web address, never javascript:
 return href?html`<a class="head-link" href="${href}" target="_blank" rel="noopener">${m.resets?'Open ChatGPT':'See resets in ChatGPT'}</a>`:''}
// The banner for a usage limit reached (state.model_pause: window '5h', 'week' or 'limit', until, name); gone when it is null.
// `fallback`: a working fallback model answers meanwhile (assistant.py fallback_covers), so nothing waits: one short line.
const pauseWhen=until=>{const r=+until>Date.now()/1000?new Date(until*1000):null;return r?(r.toDateString()===new Date().toDateString()?fmtHM(r):localeDate(r,DL,{weekday:'short'})+' '+fmtHM(r)):''};
function limitBanner(p){if(!p)return [];if(p.fallback)return [make('span',{},t('{} limit reached, using your fallback.',p.name||'AI'))];const when=pauseWhen(p.until),
 what={'5h':'{} 5-hour limit reached.',week:'{} weekly limit reached.'}[p.window]||'{} usage limit reached.';
 return [make('span',{},make('strong',{},t(what,p.name||'AI')),(when?' '+t('Resets {}.',/^\d/.test(when)?t('at {}',when):when):'')+' '+t('Nothing is lost: The Machine picks up where it left off.'))]}
// Reviews of new signals waiting for the budget (state.review_pause: window '5h' or 'week', until, name), with Review now
function reviewBanner(p){if(!p)return [];const when=pauseWhen(p.until),name=p.name||'AI',week=p.window==='week';
 const line=when?t(week?'Checks wait until {} to save your {} week.':'Checks wait until {} to save your {} 5-hour limit.',when,name):t(week?'Checks wait to save your {} week.':'Checks wait to save your {} 5-hour limit.',name);
 return [make('span',{},line),make('button',{type:'button',class:'head-link','data-review-now':''},t('Check now'))]}
// A bug the owner reported, fixed and running here now: the control plane says so once this Machine runs the fix (its
// cloud/support_fixes.py; hosted through /_machine/fixed with the owner's sign-in, self-hosted through the Network,
// state.fixed, which the Fleet's hourly look keeps). One quiet line each, until it is answered or closed, on every
// Machine of theirs. Hosted: looked at every 15 minutes.
let fixedList=[],fixedAt=0,fixedGone=new Set();
async function fixedLoad(){if(!state.manage_url){fixedList=(Array.isArray(state.fixed)?state.fixed:[]).filter(f=>f&&f.id&&!fixedGone.has(f.id));renderFixed();return}
 if(Date.now()-fixedAt<9e5)return;fixedAt=Date.now();
 try{const r=await fetch('/_machine/fixed',{credentials:'same-origin',redirect:'manual'});if(!r.ok)return;fixedList=((await r.json()).fixed||[]).filter(f=>!fixedGone.has(f.id))}catch{return}renderFixed()}
// Each banner is built again only when what it says changes (a rebuild would drop focus from its button)
const bannerSet=(b,key,nodes)=>{if(b.dataset.shown!==key){b.replaceChildren(...nodes);b.dataset.shown=key}b.hidden=!nodes.length};
// Each asks whether it is really fixed: Works now (kept, closed) or Still not right, which opens a small box for what
// is still off and an optional image (help-panel.js, loaded then), sent as a new report linked to this one
// (support_fixes.answer). × closes it without an answer, as before.
let fixedOpen=null,fixedShot=null;
function renderFixed(){const b=$('#fixed-notice');if(!b)return;bannerSet(b,JSON.stringify([fixedList.map(f=>[f.id,f.text]),fixedOpen,!!fixedShot]),
 fixedList.map(f=>make('div',{class:'notice-card fixed-notice'},make('span',{},f.text),
  make('span',{class:'fixed-ask'},make('button',{type:'button',class:'head-link','data-fixed-works':f.id},t('Works now')),
   make('button',{type:'button',class:'head-link','data-fixed-off':f.id,'aria-expanded':String(fixedOpen===f.id)},t('Still not right'))),
  make('button',{type:'button',class:'fixed-close','data-fixed':f.id,'aria-label':t('Close'),title:t('Close')},'×'),
  fixedOpen===f.id&&typeof fixedForm==='function'?fixedForm(f.id):'')));
 if(state?.greeting)b.hidden=true}  // a new owner's first views stay quiet (Store.greeting)
const fixedDrop=id=>{fixedGone.add(id);fixedList=fixedList.filter(f=>f.id!==id);if(fixedOpen===id){fixedOpen=null;fixedShot=null}renderFixed()};
// Hosted: to its account with the owner's sign-in there; self-hosted: through the Network (bug_fixed). The account's reason as an Error.
async function fixedPost(body){if(state.manage_url){const r=await fetch('/_machine/fixed',{method:'POST',headers:{'Content-Type':'application/json'},credentials:'same-origin',redirect:'manual',body:JSON.stringify(body)});
  if(!r.ok){let d={};try{d=await r.json()}catch{}throw Error(d.error||t('Can’t reach your account right now. Try again.'))}return}
 await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf,...(body.screenshot?{'X-Upload':'bug-report'}:{})},body:JSON.stringify({action:'bug_fixed',args:body})})}
document.addEventListener('click',async e=>{const b=e.target.closest('#fixed-notice button');if(!b)return;const d=b.dataset;
 if(d.fixed){fixedDrop(d.fixed);try{await fixedPost({seen:d.fixed})}catch{}return}
 if(d.fixedWorks){fixedDrop(d.fixedWorks);try{await fixedPost({answer:'works',report:d.fixedWorks})}catch{}return}
 if(d.fixedOff)lazyRun('help',()=>{fixedOpen=fixedOpen===d.fixedOff?null:d.fixedOff;fixedShot=null;renderFixed();$('#fixed-notice textarea')?.focus()})});  // its box: help-panel.js
function renderLimitBanner(){const b=$('#limit-banner');if(!b)return;const p=state.model_pause?['model',state.model_pause]:['review',state.review_pause],nodes=p[0]==='model'?limitBanner(p[1]):reviewBanner(p[1]);
 bannerSet(b,JSON.stringify([p,pauseWhen(p[1]?.until),document.documentElement.lang]),nodes)}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-review-now]');if(!b)return;b.disabled=true;
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'review_now',args:{}})});
  state.review_pause=null;renderLimitBanner();notice(t('A check starts in a moment.'))}catch(err){errCaught(err);b.disabled=false;notice(err.message,true)}});
function limitNote(m){if(!m?.limit_reached)return '';return html`<p class="limit-note"><strong>${t(m.chatgpt?'ChatGPT limit reached':'Model limit reached')}</strong>${m.limit_resets_at?t(', resets at {}',clockAt(m.limit_resets_at)):''}${resetAction(m)?html` · ${resetAction(m)}`:''}</p>`}
// A hosted Machine (it has an account): Report a bug (help-panel.js) and Support access (settings-activity.js) go through its account
const bugHosted=()=>!!state.manage_url;
// Help before its part is in (dashboard_parts.LAZY): it loads, then opens; help-panel.js sets its own click once there
$('#open-help').onclick=()=>lazyRun('help',()=>helpOpen());
