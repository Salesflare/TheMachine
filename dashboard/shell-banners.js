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
// state.fixed, which the Fleet's hourly look keeps). One quiet line each, until Got it, which closes it on every Machine
// of theirs. Hosted: looked at every 15 minutes.
let fixedList=[],fixedAt=0,fixedGone=new Set();
async function fixedLoad(){if(!state.manage_url){fixedList=(Array.isArray(state.fixed)?state.fixed:[]).filter(f=>f&&f.id&&!fixedGone.has(f.id));renderFixed();return}
 if(Date.now()-fixedAt<9e5)return;fixedAt=Date.now();
 try{const r=await fetch('/_machine/fixed',{credentials:'same-origin',redirect:'manual'});if(!r.ok)return;fixedList=((await r.json()).fixed||[]).filter(f=>!fixedGone.has(f.id))}catch{return}renderFixed()}
// Each banner is built again only when what it says changes (a rebuild would drop focus from its button)
const bannerSet=(b,key,nodes)=>{if(b.dataset.shown!==key){b.replaceChildren(...nodes);b.dataset.shown=key}b.hidden=!nodes.length};
function renderFixed(){const b=$('#fixed-notice');if(!b)return;bannerSet(b,JSON.stringify(fixedList.map(f=>[f.id,f.text])),
 fixedList.map(f=>make('div',{class:'notice-card fixed-notice'},make('span',{},f.text),make('button',{type:'button',class:'head-link','data-fixed':f.id},t('Got it')))));
 if(state?.greeting)b.hidden=true}  // a new owner's first views stay quiet (Store.greeting)
document.addEventListener('click',async e=>{const b=e.target.closest('[data-fixed]');if(!b)return;const id=b.dataset.fixed;fixedGone.add(id);fixedList=fixedList.filter(f=>f.id!==id);renderFixed();
 try{if(state.manage_url)await fetch('/_machine/fixed',{method:'POST',headers:{'Content-Type':'application/json'},credentials:'same-origin',redirect:'manual',body:JSON.stringify({seen:id})});
  else await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'bug_fixed',args:{seen:id}})})}catch{}});
function renderLimitBanner(){const b=$('#limit-banner');if(!b)return;const p=state.model_pause?['model',state.model_pause]:['review',state.review_pause],nodes=p[0]==='model'?limitBanner(p[1]):reviewBanner(p[1]);
 bannerSet(b,JSON.stringify([p,pauseWhen(p[1]?.until),document.documentElement.lang]),nodes)}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-review-now]');if(!b)return;b.disabled=true;
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'review_now',args:{}})});
  state.review_pause=null;renderLimitBanner();notice(t('A check starts in a moment.'))}catch(err){errCaught(err);b.disabled=false;notice(err.message,true)}});
function limitNote(m){if(!m?.limit_reached)return '';return html`<p class="limit-note"><strong>${t(m.chatgpt?'ChatGPT limit reached':'Model limit reached')}</strong>${m.limit_resets_at?t(', resets at {}',clockAt(m.limit_resets_at)):''}${resetAction(m)?html` · ${resetAction(m)}`:''}</p>`}
