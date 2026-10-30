// A model id as people say it: "acme/lm-2.5-swift" reads "LM-2.5 Swift", "acme/sonnet-4-5-20250929" reads
// "Sonnet 4.5" (no release date, version parts joined with dots); the id itself shows on hover.
const modelName=id=>{const parts=String(id||'').split('/').pop().replace(/[-_](\d{8}|\d{4}-\d{2}-\d{2})$/,'').replace(/[-_]latest$/i,'').split(/[-_ :]+/).filter(Boolean),words=[];
 for(const w of parts){const p=words[words.length-1];if(words.length>1&&/^\d+(\.\d+)*$/.test(p)&&/^\d{1,2}$/.test(w))words[words.length-1]=p+'.'+w;else words.push(w)}let out='';
 words.forEach((w,i)=>{const word=i===0&&/^[a-z]{1,3}$/i.test(w)?w.toUpperCase():/^\d/.test(w)?w:w[0].toUpperCase()+w.slice(1);out+=i===0?word:(i===1&&/^[A-Z]{1,3}$/.test(out)&&/^\d/.test(w)?'-':' ')+word});return out};
function renderModelPanel(){const m=state.model_status,box=$('#settings-model');if(!box)return;box.hidden=!m&&!state.chat_model?.models?.length;if(!m)return;const now=Date.now()/1000,bg=state.chat_model?.background||m.model;
 const head=`<div class="list settings-list"><div><span class="grow"><strong title="${esc(bg||'')}">${esc(modelName(bg)||'Model unknown')}</strong><small>${esc([t('Background work'),m.chatgpt?t('Signed in with ChatGPT'):m.claude_plan?t('Uses your Claude plan'):m.provider,m.plan?t('plan: {}',m.plan):''].filter(Boolean).join(' · '))}</small></span><small class="model-checked" title="${esc(m.checked_at?fmtDHM(m.checked_at,{day:'numeric',month:'short'}):'')}">${esc(t('Updated {}',ago(m.checked_at)))}</small></div></div>`;
 const bars=(m.windows||[]).filter(w=>!(w.reset&&w.reset<now)).map(w=>`<div class="usage${w.used>=100?' full':''}"><span>${esc(t('{}: {}% used',windowLabel(w.label),+w.used|0))}${w.reset?' · '+esc(t('resets in {}',untilText(w.reset))):''}</span><progress max="100" value="${+w.used|0}">${+w.used|0}%</progress></div>`).join('')||'<p class="muted">No usage windows reported yet.</p>';
 const r=m.resets,expiry=r?.credits?.find(c=>c.expires)?.expires;
 // Resets this computer can't count (no Codex CLI signed in to the same account, as on a hosted Machine): no
 // "unknown" count, only the way to ChatGPT's usage page; a team plan's resets are under its workspace there.
 const team=/team|business|enterprise|edu/i.test(m.plan||''),resets=r?`<div class="list settings-list"><div><span class="grow"><strong>${esc(t('Resets available: {}',r.available))}</strong><small>${esc(r.available?t('A reset starts your ChatGPT usage limits over.')+(expiry?' '+t('The first one expires {}.',new Date(expiry*1000).toLocaleDateString(DL,{month:'short',day:'numeric',year:'numeric'})):''):t('Your plan has no usage limit resets right now.'))}</small></span>${resetAction(m)}</div></div>`
  :m.usage_page?`<div class="list settings-list"><div><span class="grow"><strong>Usage limit resets</strong><small>${esc(t(team?'ChatGPT shows them under your team workspace.':'ChatGPT shows them.'))}</small></span>${resetAction(m)}</div></div>`:'';
 $('#model-panel').innerHTML=head+limitNote(m)+(m.claude_plan?(m.windows||[]).length?bars:'':bars+resets)}
// The model and thinking level chats use (chat_model.py): Settings, Model sets the default; the pill under a to-do
// chat's or Help's message box sets that chat's own. Only what the sign-in offers, each model with its own levels.
const THINKING={off:'No thinking',minimal:'Minimal thinking',low:'Low thinking',medium:'Medium thinking',high:'High thinking',xhigh:'Extra high thinking',adaptive:'Adaptive thinking',max:'Max thinking',ultra:'Ultra thinking'};
// In the menu only, as a second line: Ultra runs helpers alongside, so it says what it costs
const THINK_HINT={ultra:'Slower, uses more of your plan'};
const LEVEL_ORDER=Object.keys(THINKING),CHEV='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 10l5 5 5-5"/></svg>';
const cmEntry=ref=>(state.chat_model?.models||[]).find(m=>m.ref===ref);
// The supported level nearest the one asked for (OpenClaw maps the same way)
function cmNearest(level,levels){if(!levels?.length)return level||null;if(levels.includes(level))return level;const at=LEVEL_ORDER.includes(level)?LEVEL_ORDER.indexOf(level):2,d=x=>Math.abs(LEVEL_ORDER.indexOf(x)-at);
 return levels.reduce((a,b)=>d(b)<d(a)||d(b)===d(a)&&LEVEL_ORDER.indexOf(b)>LEVEL_ORDER.indexOf(a)?b:a)}
// What a chat runs with: its own pick over the default for chats over OpenClaw's own (chat_model.resolve)
function cmResolve(own){const cm=state.chat_model;if(!cm)return null;const p={...(cm.saved||{}),...(own||{})};
 let model=p.model||cm.main?.model;if(cm.known&&!cmEntry(model))model=cm.main?.model;const e=cmEntry(model);
 return {model,thinking:cmNearest(p.thinking||cm.main?.thinking||e?.default,e?.levels)}}
function cmCurrent(kind){const cm=state.chat_model;if(kind==='default')return cm?.default;if(kind==='help')return helpModel?cmResolve(helpModel):cm?.help||cm?.default;return cmResolve(chat?.model)}
// A picker is a button that opens the app's menu (cmMenu) with what it can pick: [{value,label,hint,group}]
function cmChoices(which,cur){if(which==='think')return (cmEntry(cur.model)?.levels||[]).map(l=>({value:l,label:THINKING[l]||l,hint:THINK_HINT[l]}));
 const ms=state.chat_model?.models||[],many=new Set(ms.map(m=>m.ref.split('/')[0])).size>1,one=ref=>({value:ref,label:modelName(ref),group:many?ref.split('/')[0]:'',name:true});
 // Each provider once, its models under it, in the order the Gateway first lists each provider
 const order=[...new Set(ms.map(m=>m.ref.split('/')[0]))],sorted=[...ms].sort((a,b)=>order.indexOf(a.ref.split('/')[0])-order.indexOf(b.ref.split('/')[0]));
 return [...(cur.model&&!cmEntry(cur.model)?[{...one(cur.model),group:''}]:[]),...sorted.map(m=>one(m.ref))]}
const cmTrigger=(kind,which,label,cls,extra='',after='')=>`<button type="button" class="${cls}" data-cm-pick="${which}" data-cm-kind="${kind}" aria-haspopup="menu" aria-expanded="false"${extra}><span>${esc(label)}</span>${after}${CHEV}</button>`;
// Fast (chat_model.py): the person's own choice for to-do chats only, off by default, at the end of a chat's model menu.
// Only a model the Gateway says has a fast option takes it; for any other the item stays, disabled, with why.
const cmFastOk=ref=>!!cmEntry(ref)?.fast,cmFastShown=(kind,cur)=>kind==='chat'&&!!state.chat_model?.fast&&cmFastOk(cur?.model);
const cmFastItem=cur=>{const ok=cmFastOk(cur.model),on=!!state.chat_model?.fast&&ok;
 return `<div class="cm-speed" role="group" aria-label="${esc(t('Speed'))}"><button type="button" role="menuitemcheckbox" aria-checked="${on}" data-cm-fast${ok?'':' aria-disabled="true"'}>${CM_CHECK}<span>${esc(t('Fast'))}</span><small>${esc(t(ok?'Quicker replies, at a higher cost':'Not offered for this model'))}</small></button></div>`};
async function cmFastSave(on){try{state.chat_model=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'chat_fast_set',args:{fast:on}})});cmPaint('chat')}
 catch(err){errCaught(err);toast(err.message,true);cmPaint('chat')}}
// The pill: "Model  Thinking", each part a quiet button over the menu; a to-do chat's model says Fast when it runs fast
function cmPill(kind){const cm=state.chat_model,cur=cmCurrent(kind);if(!cm?.known||!cm.models.length||!cur?.model)return '';const levels=cmEntry(cur.model)?.levels||[];
 return cmTrigger(kind,'model',modelName(cur.model),'model-pick',` title="${esc(cur.model)}" translate="no"`,cmFastShown(kind,cur)?`<span class="cm-fast-on" translate="yes">${esc(t('Fast'))}</span>`:'')
  +(levels.length>1&&cur.thinking?cmTrigger(kind,'think',THINKING[cur.thinking]||cur.thinking,'model-pick'):'')}
// Repainted with the state and the chat, never while its menu is open; a focused picker keeps the focus
function cmSwap(box,h){if(cmOpen?.box===box||box.dataset.html===h)return;const f=document.activeElement?.closest?.('[data-cm-pick]'),had=f&&box.contains(f)?f.dataset.cmPick:null;
 box.dataset.html=h;box.innerHTML=h;if(had)box.querySelector(`[data-cm-pick="${had}"]`)?.focus({preventScroll:true})}
function cmPaint(kind){const box=$(kind==='help'?'#help-model':'#chat-model');if(box)cmSwap(box,cmPill(kind))}
function renderChatModel(){const cm=state.chat_model,box=$('#model-chats');if(!box||cmOpen?.box===box)return;box.hidden=!cm?.known||!cm.models.length;if(box.hidden)return;
 const cur=cm.default||{},levels=cmEntry(cur.model)?.levels||[];
 cmSwap(box,`<div class="section-head"><h3>Chats</h3><p>What to-do chats and Help use. Each chat can pick its own under its message box.</p></div><div class="list settings-list"><div><span class="grow"><strong>Model</strong><small>Only models your sign-in offers.</small></span>${cmTrigger('default','model',modelName(cur.model),'select-like',' translate="no"')}</div>`
  +(levels.length>1?`<div><span class="grow"><strong>Thinking</strong><small>More thinking is slower and uses more of your plan.</small></span>${cmTrigger('default','think',THINKING[cur.thinking]||cur.thinking||'','select-like')}</div>`:'')+'</div>')}
// Saves a pick: Settings' default, Help's own (for this Help chat only) or the open to-do chat's own
async function cmSave(kind,which,value){const cur=cmCurrent(kind)||{};
 const next=which==='model'?{model:value,thinking:cmNearest(cur.thinking,cmEntry(value)?.levels)}:{model:cur.model,thinking:value};
 const post=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
 try{if(kind==='help'){helpModel=next;cmPaint('help');return}
  if(kind==='default'){state.chat_model=await post('chat_model_default',next);renderChatModel();cmPaint('chat');notice(t('Saved.'));return}
  const s=chatOpen();if(!s)return;const r=await post('chat_model_set',{suggestion_id:s.id,...next});if(chat)chat.model=r.model;cmPaint('chat')}
 catch(err){errCaught(err);toast(err.message,true);renderChatModel();cmPaint(kind==='help'?'help':'chat')}}
// The menu: one at a time, a popover above the page and Help's dialog, below the trigger or above it when that has more room;
// arrows, Home and End move, Enter or a tap picks, Escape or Tab closes, and the focus goes back to the trigger.
let cmOpen=null;
// Below when it fits there or there's fair room (it scrolls); else above, in a dialog under the dialog's title when that
// leaves fair room; else wherever there's more room
function cmPlace(m,b){m.style.cssText='';const r=b.getBoundingClientRect(),gap=6,h=m.offsetHeight,fair=Math.min(h,160),below=innerHeight-r.bottom-gap-8,above=r.top-gap-8,
  head=b.closest('dialog[open]')?.querySelector('h2,h3')?.parentElement,under=r.top-gap-Math.max(8,head?head.getBoundingClientRect().bottom+4:8),
  up=below<fair&&(under>=fair||above>below),room=!up?below:under>=fair?under:above;
 m.style.minWidth=Math.max(200,Math.round(r.width))+'px';m.style.maxHeight=Math.max(120,Math.floor(room))+'px';
 if(up)m.style.bottom=Math.round(innerHeight-r.top+gap)+'px';else m.style.top=Math.round(r.bottom+gap)+'px';
 m.style.left=Math.round(Math.max(8,Math.min(r.left,innerWidth-m.offsetWidth-8)))+'px'}
const CM_CHECK='<svg class="cm-check" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
function cmMenuClose(focus){const m=$('#cm-menu');if(!m||m.hidden)return;if(m.matches?.(':popover-open'))m.hidePopover();m.hidden=true;const o=cmOpen;cmOpen=null;if(!o)return;
 const b=o.box.querySelector(`[data-cm-pick="${o.which}"]`);b?.setAttribute('aria-expanded','false');if(focus)b?.focus({preventScroll:true})}
function cmMenuOpen(b,last){const kind=b.dataset.cmKind,which=b.dataset.cmPick,cur=cmCurrent(kind)||{},sel=which==='model'?cur.model:cur.thinking,box=b.closest('#chat-model,#help-model,#model-chats');
 let m=$('#cm-menu');if(!m){m=document.createElement('div');m.id='cm-menu';m.className='fact-menu-list cm-menu';m.setAttribute('role','menu');m.hidden=true;if(m.showPopover)m.popover='manual'}
 // In the trigger's dialog (outside a modal dialog nothing takes the focus), as a popover so the dialog never clips it
 const host=b.closest('dialog[open]')||document.body;if(m.parentNode!==host)host.append(m);m.setAttribute('aria-label',which==='model'?'Model':'Thinking');
 // A provider's models sit in a group under its heading, so a heading never reads as the line under the model above it
 const item=c=>`<button type="button" role="menuitemradio" aria-checked="${c.value===sel}" data-cm-value="${esc(c.value)}"${c.name?' translate="no"':''}>${CM_CHECK}<span>${esc(c.label)}</span>${c.hint?`<small>${esc(c.hint)}</small>`:''}</button>`;
 const groups=[];for(const c of cmChoices(which,cur)){const g=groups.at(-1);if(g&&g.name===c.group)g.items.push(c);else groups.push({name:c.group,items:[c]})}
 m.innerHTML=groups.map((g,i)=>g.name?`<div class="cm-section" role="group" aria-labelledby="cm-g-${i}"><p class="cm-group" id="cm-g-${i}" translate="no">${esc(g.name)}</p>${g.items.map(item).join('')}</div>`:g.items.map(item).join('')).join('')+(kind==='chat'&&which==='model'?cmFastItem(cur):'');
 cmOpen={box,kind,which};b.setAttribute('aria-expanded','true');m.hidden=false;if(m.showPopover&&!m.matches(':popover-open'))m.showPopover();cmPlace(m,b);
 const items=[...m.querySelectorAll('[role=menuitemradio],[role=menuitemcheckbox]')];(last?items.at(-1):items.find(i=>i.getAttribute('aria-checked')==='true')||items[0])?.focus({preventScroll:true})}
document.addEventListener('click',e=>{const b=e.target.closest('[data-cm-pick]');
 if(b){e.preventDefault();const same=cmOpen&&cmOpen.box.contains(b)&&cmOpen.which===b.dataset.cmPick;cmMenuClose(false);if(!same)cmMenuOpen(b);return}
 const f=e.target.closest('#cm-menu [data-cm-fast]');if(f){e.preventDefault();if(f.getAttribute('aria-disabled')==='true')return;const on=f.getAttribute('aria-checked')!=='true';cmMenuClose(true);cmFastSave(on);return}
 const it=e.target.closest('#cm-menu [data-cm-value]');if(it){e.preventDefault();const o=cmOpen,v=it.dataset.cmValue,was=it.getAttribute('aria-checked')==='true';cmMenuClose(true);if(o&&!was)cmSave(o.kind,o.which,v);return}
 if(cmOpen&&!e.target.closest('#cm-menu'))cmMenuClose(false)});
document.addEventListener('keydown',e=>{const b=e.target.closest?.('[data-cm-pick]');
 if(b&&(e.key==='ArrowDown'||e.key==='ArrowUp')){e.preventDefault();cmMenuClose(false);cmMenuOpen(b,e.key==='ArrowUp');return}
 const m=$('#cm-menu');if(!cmOpen||!m||m.hidden||!m.contains(e.target))return;const items=[...m.querySelectorAll('[role=menuitemradio],[role=menuitemcheckbox]')],i=items.indexOf(document.activeElement);
 if(e.key==='Escape'){e.preventDefault();e.stopPropagation();cmMenuClose(true);return}
 if(e.key==='Tab'){cmMenuClose(true);return}
 const to={ArrowDown:(i+1)%items.length,ArrowUp:(i-1+items.length)%items.length,Home:0,End:items.length-1}[e.key];if(to!==undefined){e.preventDefault();items[to].focus()}},true);
addEventListener('resize',()=>cmMenuClose(false));// A thread that scrolls under the box (a reply streaming in) moves the menu along with its trigger
document.addEventListener('scroll',e=>{const m=$('#cm-menu');if(!cmOpen||!m||m.contains(e.target))return;const b=cmOpen.box.querySelector(`[data-cm-pick="${cmOpen.which}"]`);if(b?.isConnected)cmPlace(m,b);else cmMenuClose(false)},true);
async function modelAction(action,args){try{const d=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args:args||{}})});
 if(d.model_status)state.model_status=d.model_status;if(d.model_usage)state.model_usage=d.model_usage;renderModelUsage();return d}catch(err){errCaught(err);notice(err.message,true)}}
document.addEventListener('click',async e=>{
 const b=e.target.closest('[data-model-reset]');if(!b)return;const n=state.model_status?.resets?.available||0;
 if(!confirm(t(['This uses 1 of your {} reset. Your ChatGPT usage limits start over now.','This uses 1 of your {} resets. Your ChatGPT usage limits start over now.'],n)))return;b.disabled=true;
 const d=await modelAction('model_reset',{key:crypto.randomUUID()});b.disabled=false;if(!d)return;
 notice(t(({reset:'Usage reset. Your limits start over now.',nothingToReset:'Nothing to reset right now; no reset was used.',noCredit:'No reset was available.',alreadyRedeemed:'That reset was already used.'})[d.outcome]||'Done.'))});
function renderModelUsage(){const now=Date.now()/1000,label=l=>['Week','168h','7d'].includes(l)?t('Weekly'):['Day','24h'].includes(l)?t('Daily'):/^\d+h$/.test(l)?t('{}-hour limit',parseInt(l)):l;
renderModelPanel();renderChatModel();cmPaint('chat');renderLimitBanner();$('#model-usage').innerHTML=limitNote(state.model_status)+(state.model_usage||[]).map(p=>p.windows.filter(w=>!(w.reset<now)).map(w=>{const r=w.reset?new Date(w.reset*1000):null,when=r?t(', resets {}',(w.reset-now>86400?r.toLocaleDateString(DL,{weekday:'short'})+' ':'')+fmtHM(r)):'';
return `<div class="usage"><span>${esc(t('{}: {}% used',p.name+' '+label(w.label),+w.used|0))}${esc(when)}</span><progress max="100" value="${+w.used|0}">${+w.used|0}%</progress></div>`}).join('')).join('')}
const ago=v=>{if(!v)return t('Not yet');const s=(new Date(v)-Date.now())/1000,a=Math.abs(s),f=new Intl.RelativeTimeFormat(DL,{numeric:'auto'});for(const[u,n]of[['day',86400],['hour',3600],['minute',60]])if(a>=n)return f.format(Math.round(s/n),u);return a<45?t('just now'):f.format(Math.round(s/60),'minute')};
const time=(v,plain)=>`<time class="${plain?'':'mono '}muted" datetime="${esc(v||'')}" title="${esc(date(v))}">${esc(ago(v))}</time>`;
const calendarDate=v=>new Date(v+'T12:00:00').toLocaleDateString(DL,{month:'short',day:'numeric',year:'numeric'});
// A signal's time as people say it: Today 08:46, Yesterday 17:20, Wed, Oct 21 09:00 (the year only when it isn't this
// one), no seconds; a meeting as a range, Tomorrow 10:46 to 11:46
const humanDay=d=>{const t=new Date(),k=localDay(d),off=n=>{const x=new Date(t);x.setDate(t.getDate()+n);return localDay(x)};return k===off(0)?'Today':k===off(-1)?'Yesterday':k===off(1)?'Tomorrow':d.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short',...(d.getFullYear()!==t.getFullYear()?{year:'numeric'}:{})})};
const humanHM=d=>fmtHM(d);
const humanTime=v=>{const d=new Date(v);return !v||isNaN(d)?'':humanDay(d)+' '+humanHM(d)};
const when=e=>{if(e.kind!=='calendar.event')return humanTime(e.occurred_at);if(e.metadata.all_day)return humanDay(new Date(e.metadata.start.date+'T12:00:00'))+' · '+t('All day');const a=new Date(e.occurred_at),b=new Date(e.metadata.end_at);return isNaN(b)?humanTime(e.occurred_at):rangeText(humanTime(e.occurred_at),localDay(a)===localDay(b)?humanHM(b):humanTime(e.metadata.end_at))};
// Card text: [words](https://...) and bare web addresses become links (a long one shows its domain), only http(s) and
// mailto; everything else stays escaped text. format also highlights **values**; linkText is for technical text.
const TEXT_LINK=/\[([^\[\]\n]{1,200})\]\(((?:https?:\/\/|mailto:)[^\s()<>]{1,2000})\)|\bhttps?:\/\/[^\s<>()\[\]"'`]{1,2000}/gi;
const linkable=u=>{try{return ['https:','http:','mailto:'].includes(new URL(u).protocol)}catch{return false}};
const shortURL=u=>{if(u.length<=40)return u;try{return new URL(u).hostname.replace(/^www\./,'')}catch{return u}};
const richText=(v,bold)=>{const found=[];let h=esc(String(v??'').replace(/[\u0000\u0001]/g,'').replace(TEXT_LINK,(m,t,u)=>{let url=u||m,tail='';
 if(!u){tail=(/[.,;:!?'"]+$/.exec(url)||[''])[0];url=url.slice(0,url.length-tail.length)}if(!linkable(url))return m;
 found.push(`<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(t??shortURL(url))}</a>`);return '\u0000'+(found.length-1)+'\u0001'+tail}));
 if(bold)h=h.replace(/\*\*([^*]+)\*\*/g,(m,t)=>t.replace(/\u0000\d+\u0001/g,'x').length<=24?`<strong class="nb">${t}</strong>`:`<strong>${t}</strong>`);
 return h.replace(/\u0000(\d+)\u0001/g,(m,i)=>found[i])};
const format=v=>richText(v,true),linkText=v=>richText(v,false);
// Card bodies: a fully bold first line is a small subtitle under the title, blank lines make paragraphs, long bodies fold behind Show more.
const expandedBodies=new Set(),expandedDetails=new Set();
// Rows drawn from a list's kept HTML (the Done pages) open again the Details that were open
function detailsSync(root){for(const b of root.querySelectorAll('[data-details]')){const open=expandedDetails.has(b.dataset.details),p=b.closest('article')?.querySelector(':scope>.card-details');b.setAttribute('aria-expanded',open);if(p)p.hidden=!open}}
document.addEventListener('click',e=>{const b=e.target.closest('[data-details]');if(!b)return;const id=b.dataset.details,open=!expandedDetails.has(id);open?expandedDetails.add(id):expandedDetails.delete(id);
 b.setAttribute('aria-expanded',open);const p=b.closest('article')?.querySelector(':scope>.card-details');if(p)p.hidden=!open});
// Another open card named by its exact title links to it.
// Only in plain text: never inside a tag or an existing link.
const cardLinks=(html,s)=>(state.suggestions||[]).filter(o=>o.id!==s.id&&!closed(o)&&o.title.length>=12).sort((a,b)=>b.title.length-a.title.length).reduce((h,o)=>{const t=esc(o.title);return h.includes(t)?h.split(/(<a\b[\s\S]*?<\/a>|<[^>]*>)/).map((part,i)=>i%2?part:part.split(t).join(`<a class="card-link" href="#card=${esc(o.id)}">${t}</a>`)).join(''):h},html);
// A confirmed step that didn't go through says so in one line instead of the earlier result (step_stopped in assistant.py).
// Handed off and with them: the card's body is what was asked; the suggestion to hand it off stays in the chat.
const askedBody=s=>{const h=s.fleet_handoff;return h?.asked&&!h.back&&['asked','waiting for them','accepted','accepted with a change'].includes(h.stage)&&!redirect(s)?`<div class="body clamp handoff-asked" style="--lines:2" title="${esc(h.asked)}" translate="no"><p>${esc(t('Asked {}:',firstName(h.name)))} ${esc(h.asked)}</p></div>`:''};
// A skill from notes (skill_clusters in assistant.py) or proposed in Settings (skills.py): a new one, maybe related to one
// you have, or an Update to one of yours: the whole skill rewritten as one, shown before and after with what changed marked.
const skillNotesList=p=>`<ul>${p.notes.map(n=>`<li>${esc(n)}</li>`).join('')}</ul>`;
const skillRuns=(runs,fallback)=>(runs||[['same',fallback]]).map(([k,t])=>k==='added'?`<ins>${esc(t)}</ins>`:k==='removed'?`<del>${esc(t)}</del>`:`<span>${esc(t)}</span>`).join('\n');
const skillBeforeAfter=u=>`<div><h4>Before</h4><pre class="skill-body">${skillRuns(u.changes?.before,u.before)}</pre></div><div><h4>After</h4><pre class="skill-body">${skillRuns(u.changes?.after,u.after)}</pre></div>`;
const skillStale=u=>u?.stale?`<p class="note">${esc(u.skill)} changed after this was suggested, so it can’t be applied. The next suggestion starts from the new version.</p>`:'';
const skillRelated=r=>r?`<p class="skill-related">Related to <strong>${esc(r.name)}</strong>: ${esc(r.relation)}</p>`:'';
function skillProposal(s){const p=s.skill_proposal;if(!p)return '';
 if(p.update)return `${skillStale(p.update)}<details class="skill-notes"><summary>Read the change and ${p.notes.length} notes</summary><div class="skill-ba">${skillBeforeAfter(p.update)}</div>${skillNotesList(p)}</details>`;
 return `${skillRelated(p.related)}<details class="skill-notes"><summary>Read skill instructions and ${p.notes.length} notes</summary><p><strong>${esc(p.name)}</strong></p><div>${format(p.body).replace(/\n/g,'<br>')}</div>${skillNotesList(p)}</details>`}
// Update <skill>: its before and after first; only Update skill there changes it (reviewed names what was shown).
let skillUpdating=null;
function skillUpdateOpen(u,from,send){if(!u){toast('That skill is gone.',true);return}if(u.stale){toast(`${u.skill} changed after this was suggested.`,true);return}
 skillUpdating={review:u.review,skill:u.skill,send};$('#skill-update-title').textContent=t('Update {}?',u.skill);$('#skill-update-from').textContent=from;
 $('#skill-update-ba').innerHTML=skillBeforeAfter(u);$('#skill-update-error').textContent='';$('#skill-update-ok').disabled=false;
 if(!$('#skill-update').open)$('#skill-update').showModal();
 for(const b of $('#skill-update-ba').querySelectorAll('.skill-body')){const c=b.querySelector('ins,del');b.scrollTop=c?Math.max(0,c.offsetTop-b.offsetTop-24):0}}  // each side opens at its first change
document.addEventListener('click',e=>{const b=e.target.closest('[data-skill-update]');if(!b)return;e.preventDefault();e.stopPropagation();const id=b.dataset.skillUpdate;
 if(b.dataset.settings!==undefined){const s=state.skills?.skills.find(x=>x.id===id);skillUpdateOpen(s?.update,'Your Machine rewrote it with what it learned. Nothing else changes.',review=>skillAct('skill_decide',{id,choice:'approve',reviewed:review}));return}
 const s=state.suggestions.find(x=>x.id===id);
 skillUpdateOpen(s?.skill_proposal?.update,`Merges what ${s?.skill_proposal?.notes.length} notes taught. Nothing else changes.`,
  async review=>{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'decide',args:{suggestion_id:id,choice:'accept',feedback:'',decision_id:crypto.randomUUID(),reviewed:review}})});await refresh()})},true);
{$('#skill-update-cancel').onclick=()=>$('#skill-update').close();
 $('#skill-update-ok').onclick=async()=>{const u=skillUpdating;if(!u)return;const ok=$('#skill-update-ok');ok.disabled=true;
  try{await u.send(u.review);$('#skill-update').close();skillUpdating=null;toast('Updated '+u.skill+'.')}
  catch(err){errCaught(err);ok.disabled=false;$('#skill-update-error').textContent=err.message}}}
