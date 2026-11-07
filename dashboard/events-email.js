// The messages behind each card, read in a dialog. HTML renders in a sandboxed frame:
// no scripts, forms or navigation of the dashboard; links open in a new tab.
const originals=new Map(),emailViews=new Map(),around=new Map();  // around: what was said around a to-do's source message
const fileSize=b=>!b?'':b<1024?b+' B':b<1048576?Math.round(b/1024)+' KB':(b/1048576).toFixed(1)+' MB';
// A mailing list's rewrite as people say it: Google Groups' "'Sam Lee' via Sales" is "Sam Lee via Sales", and a group named
// after its address ("info@acme.com readers") is that address (assistant.group_sender).
const groupSender=v=>{const m=/^'(.+)' via (.+)$/.exec(v);if(!m)return v;const at=/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+/.exec(m[2].trim());return `${m[1].trim()} via ${at?at[0]:m[2].trim()}`};
const sender=v=>groupSender(String(v||'').replace(/\s*<[^>]+>/,'').replace(/^"|"$/g,'').trim())||String(v||'');
const linkify=t=>html`${String(t??'').split(/(https?:\/\/[^\s<>"']+[^\s<>"'.,;:!?)\]])/g).map((x,i)=>i%2?html`<a href="${x}" target="_blank" rel="noreferrer">${x}</a>`:x)}`;
const apiURL=path=>new URL(path,document.baseURI).href;
// Any card built from collected messages can show them, including older cards without a source line.
const eventIds=s=>{try{return Array.isArray(s.event_ids)?s.event_ids:JSON.parse(s.event_ids||'[]')}catch{return []}};
// Each service by its own logo (dashboard.html --i-*): where a to-do came from and what its prepared step goes out on.
// An email or a calendar change by the account's service: Google's own logo; Outlook and the rest the plain envelope.
const svcOf=id=>(state?.connectors||[]).find(c=>c.id===id)?.service||'';
const VIA_NAME={gmail:'Gmail',mail:'Email',slack:'Slack',whatsapp:'WhatsApp',telegram:'Telegram',linkedin:'LinkedIn',x:'X',intercom:'Intercom',gdocs:'Google Docs',file:'Doc',gcal:'Google Calendar',cal:'Calendar',handoff:'Hand off',browser:'Browser',github:'GitHub'};
// On a button that already says what it does, the logo is only a picture (hidden from screen readers).
const viaIco=(k,quiet)=>k?quiet?html`<i class="via-ico via-${k}" aria-hidden="true"></i>`:html`<i class="via-ico via-${k}" role="img" aria-label="${t(VIA_NAME[k]||service(k)||'The source')}" title="${t(VIA_NAME[k]||service(k)||'The source')}"></i>`:'';
const STEP_VIA={slack:'slack',whatsapp:'whatsapp',telegram:'telegram',linkedin:'linkedin',x:'x',intercom:'intercom',handoff:'handoff',finish:'browser'};
// A final step on GitHub that runs with gh or a GitHub MCP server (github_route.py) shows GitHub's logo, else the browser.
const actionVia=a=>a?.kind==='finish'&&['gh','mcp'].includes(a.via)?'github':['email','email_demo'].includes(a?.kind)?(svcOf(a.account_id)==='gmail'?'gmail':'mail'):a?.kind==='calendar'?(svcOf(a.account_id)==='calendar'?'gcal':'cal'):['doc_write','doc_reply'].includes(a?.kind)?(a.provider==='microsoft'?'file':'gdocs'):STEP_VIA[a?.kind]||'';
const cardViaIcon=s=>{const v=(/^Source:\s*([^·\n]+)/i.exec(s.source_line||'')?.[1]||'').trim(),svc=(Array.isArray(s.account_ids)?s.account_ids:(()=>{try{return JSON.parse(s.account_ids||'[]')}catch{return []}})()).map(svcOf);
 if(isEmail(s)||/^(email|gmail|outlook|mail)\b/i.test(v))return (s.original_urls||[]).some(u=>/^https:\/\/mail\.google\.com\//.test(u))||svc.includes('gmail')&&!svc.includes('outlook')?'gmail':'mail';
 const named=[['slack',/^slack\b/i],['whatsapp',/^whatsapp\b/i],['telegram',/^telegram\b/i],['linkedin',/^linkedin\b/i],['x',/^x( message)?\b/i],['intercom',/^intercom\b/i],['gdocs',/^(doc |suggested edit)/i]].find(([,r])=>r.test(v));
 return named?named[0]:/note/i.test(v)?'note':/calendar/i.test(v)?(svc.includes('calendar')?'gcal':'cal'):'chat'};
// A card the owner added has their own words as its only signal until the review links an email: nothing to open yet.
const hasOriginal=s=>Boolean(s.source_line||(!['owner','machine'].includes(s.origin)&&eventIds(s).length)||(s.original_urls||[]).length);  // machine: an update's note, no thread
const isEmail=s=>/^Source: email/.test(s.source_line||'')||(s.original_urls||[]).some(u=>/^https:\/\/(mail\.google\.com|outlook\.(office|office365|live)\.com)\//.test(u));
const originalsFor=id=>{if(!originals.has(id))originals.set(id,request('api/originals?id='+id).then(r=>{around.set(id,r.around||null);return r.originals}).catch(e=>{originals.delete(id);throw e}));return originals.get(id)};
// Dark mode for HTML emails, like Gmail's: light backgrounds turn dark and dark text turns light,
// keeping each color's hue. Images are left alone.
function rgbHsl(r,g,b){r/=255;g/=255;b/=255;const max=Math.max(r,g,b),min=Math.min(r,g,b),l=(max+min)/2;if(max===min)return [0,0,l];const d=max-min,s=l>.5?d/(2-max-min):d/(max+min);const h=max===r?(g-b)/d+(g<b?6:0):max===g?(b-r)/d+2:(r-g)/d+4;return [h*60,s,l]}
function darkenEmail(doc){
const win=doc.defaultView,hsl=(h,s,l,a)=>`hsla(${h.toFixed(0)},${(s*100).toFixed(0)}%,${(l*100).toFixed(0)}%,${a})`;
const parse=c=>{const m=/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/.exec(c||'');return m?[...rgbHsl(+m[1],+m[2],+m[3]),m[4]===undefined?1:+m[4]]:null};
// Email templates can paint the canvas on <html>, not just on their body/tables.
for(const el of [doc.documentElement,doc.body,...doc.body.querySelectorAll('*')]){
if(['IMG','SVG','PICTURE','VIDEO','CANVAS'].includes(el.tagName.toUpperCase()))continue;
const cs=win.getComputedStyle(el),bg=parse(cs.backgroundColor),fg=parse(cs.color),border=parse(cs.borderTopColor);
if(bg&&bg[3]>0&&bg[2]>.45)el.style.setProperty('background-color',hsl(bg[0],bg[1]*.6,.09+(1-bg[2])*.6,bg[3]),'important');
if(fg&&fg[2]<.65)el.style.setProperty('color',hsl(fg[0],fg[1],Math.max(.72,1-fg[2]*.6),fg[3]),'important');
if(border&&border[2]>.6&&parseFloat(cs.borderTopWidth))el.style.setProperty('border-color',hsl(border[0],border[1]*.5,.3,border[3]),'important')}}
const dark=()=>document.documentElement.dataset.theme!=='light';
function emailDoc(html,images,id,ev){
const doc=html.replace(/cid:([^"'\s)>]+)/gi,(m,c)=>{const p=images[c]??images[decodeURIComponent(c)];return p===undefined?m:apiURL(`api/attachment?id=${id}&event=${encodeURIComponent(ev)}&part=${encodeURIComponent(p)}`)});
return `<!doctype html><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src ${location.origin} https: data:; style-src 'unsafe-inline'; font-src https: data:"><meta name="referrer" content="no-referrer"><base target="_blank"><style>${dark()?'html{background:#16191d;color-scheme:dark}body{color:#e6e3dc}a{color:#BCCBA8}':'html{background:#fff}body{color:#202124}'}body{margin:0;padding:18px;font:15px/1.5 system-ui,-apple-system,sans-serif;overflow-wrap:anywhere}img{max-width:100%;height:auto}table{max-width:100%}
</style>`+doc}
// What a source is, when nobody sent it: never the raw kind ("calendar")
const KIND_LABEL={calendar:'Meeting invite',email:'Email',phone:'Phone',signal:'Signal',note:'Note',message:'Message'};
const kindLabel=k=>t(KIND_LABEL[k]||k||'Original');
function messageHTML(o,id,i){
// Details holds the headers, or a signal's technical part (an error's code locations); no toggle when there is neither.
const meta=[[['From',o.from],['To',o.to],['Cc',o.cc]].filter(([,v])=>v).map(([k,v])=>html`<div><span>${k}</span> ${v}</div>`),o.details?html`<pre class="email-tech">${o.details}</pre>`:''].flat();
return html`<div class="email-meta"><div class="email-from"><strong>${sender(o.from)||kindLabel(o.kind)}</strong><time>${fmtDHM(o.occurred_at,{weekday:'short',day:'numeric',month:'short'})}</time></div>${o.title?html`<div class="email-subject">${o.title}</div>`:''}${meta.some(Boolean)?html`<details class="email-headers"><summary>Details</summary>${meta}</details>`:''}</div>${(o.attachments||[]).length?html`<div class="attachments">${o.attachments.map(a=>html`<a class="attachment" href="api/attachment?id=${id}&event=${encodeURIComponent(o.event_id)}&part=${encodeURIComponent(a.part)}" target="_blank" rel="noreferrer">📎 ${a.name}<small>${fileSize(a.size)}</small></a>`)}</div>`:''}<div class="email-body" data-email-body="${i}"><p class="muted">Loading…</p></div>${o.kind==='calendar'&&!o.raw?html`<p class="email-open"><button type="button" class="link" data-open-meeting="${o.event_id}">${t('Notes and transcript')}</button></p>`:''}${o.url&&safeURL(o.url)?html`<p class="email-open"><a href="${o.url}" target="_blank" rel="noreferrer">${o.kind==='calendar'?t(calOpenLabel(o.url)):`Open in ${o.kind==='email'?(/^https:\/\/outlook\./.test(o.url||'')?'Outlook':'Gmail'):['phone','signal'].includes(o.kind)?'app':o.kind} ↗`}</a></p>`:''}`}
async function fillMessage(container,o,id){
const box=container.querySelector('.email-body');if(!box||box.dataset.filled)return;box.dataset.filled='1';
const said=String(o.body||'').replace(/\r\n/g,'\n').split('\n').filter(l=>!(o.kind==='calendar'&&/^Participants: /.test(l))).join('\n').trim();  // an invite's raw guest addresses: the meeting's With has them by name
const text=()=>{setHTML(box,said?html`<div class="email-text">${linkify(said)}</div>`:html`<p class="muted">${t('No description.')}</p>`)};
if(o.kind!=='email'||o.near){text();return}  // a message around the source reads as its stored text
const view=await emailViewFor(id,o.event_id);if(!view.html){text();if(view.failed)emailRetry(container,box,o,id);return}
const frame=document.createElement('iframe');frame.className='email-frame';frame.title='Email';frame.setAttribute('sandbox','allow-same-origin allow-popups allow-popups-to-escape-sandbox');frame.setAttribute('referrerpolicy','no-referrer');
frame.style.visibility='hidden';const reveal=()=>{const doc=frame.contentDocument;if(doc?.body&&dark())try{darkenEmail(doc)}catch{}frame.style.visibility=''};setTimeout(reveal,1500);
frame.addEventListener('load',()=>{reveal();const doc=frame.contentDocument;if(!doc)return;const fit=()=>{frame.style.height=Math.min(Math.max(Math.ceil(doc.body.getBoundingClientRect().height),80),20000)+'px'};fit();new ResizeObserver(fit).observe(doc.body)});
frame.srcdoc=emailDoc(view.html,view.images||{},id,o.event_id);box.replaceChildren(frame)}
// The full email didn't come (Gmail or the Machine didn't answer): the saved text stays, with one line to try again.
// Not when there is no full email to read (an email from another provider): that is the saved text alone.
function emailRetry(container,box,o,id){const p=document.createElement('p');p.className='email-retry muted';
setHTML(p,html`${t('Couldn’t load the full email.')} <button type="button" class="link" data-email-retry>${t('Try again')}</button>`);box.append(p);
p.querySelector('button').onclick=()=>{delete box.dataset.filled;setHTML(box,html`<p class="muted">Loading…</p>`);fillMessage(container,o,id)}}
// Files attached to this card's email draft, as links that open over the Tailscale dashboard.
const draftFileLinks=(id,files)=>html`${(files||[]).map(a=>html`<a class="attachment" href="${'api/draft-attachment?id='+encodeURIComponent(id)+'&sha='+encodeURIComponent(a.sha256)}" target="_blank" rel="noreferrer">📎 ${a.name}<small>${fileSize(a.size)}</small></a>`)}`;
const draftFiles=s=>{const seen=new Set();return taskActions(s).filter(a=>['email','email_demo'].includes(a.kind)).flatMap(a=>a.attachments||[]).filter(a=>!seen.has(a.sha256)&&seen.add(a.sha256))};
const draftFilesBlock=s=>{const files=draftFiles(s);return files.length?html`<div class="draft-files"><h3>Attached to your draft</h3><div class="attachments">${draftFileLinks(s.id,files)}</div></div>`:''};
const emailViewFor=(id,ev)=>{const key=id+':'+ev;if(!emailViews.has(key))emailViews.set(key,request(`api/email?id=${id}&event=${encodeURIComponent(ev)}`).catch(e=>{emailViews.delete(key);return {html:'',failed:e?.status!==404||!!e.retry}}));return emailViews.get(key)};
// Cards on screen read their email ahead, quietly: two at a time when the browser is idle, each card once, the last
// PREFETCH_KEEP kept. Opening one is then instant.
const PREFETCH_KEEP=30,prefetchQueue=[],prefetched=new Set();let prefetching=0;
const idle=f=>(window.requestIdleCallback||(g=>setTimeout(g,200)))(f);
function trim(map){while(map.size>PREFETCH_KEEP)map.delete(map.keys().next().value)}
function prefetchNext(){while(prefetching<2&&prefetchQueue.length){const id=prefetchQueue.shift();prefetching++;
 idle(async()=>{try{const list=await originalsFor(id),first=list[0];if(first?.kind==='email')await emailViewFor(id,first.event_id);trim(originals);trim(emailViews);trim(around)}catch{prefetched.delete(id)}finally{prefetching--;prefetchNext()}})}}
// A to-do's source sits behind Details: the to-do itself coming into sight reads its original ahead.
const prefetchSeen=window.IntersectionObserver?new IntersectionObserver(entries=>{for(const e of entries){if(!e.isIntersecting)continue;prefetchSeen.unobserve(e.target);const id=e.target.dataset.id||e.target.querySelector('[data-original="read"][data-id]')?.dataset.id;
 if(id&&!prefetched.has(id)&&!originals.has(id)){prefetched.add(id);prefetchQueue.push(id)}}prefetchNext()},{rootMargin:'100px'}):null;
let prefetchScan=0;if(prefetchSeen)new MutationObserver(()=>{cancelAnimationFrame(prefetchScan);prefetchScan=requestAnimationFrame(()=>{for(const b of document.querySelectorAll('[data-original="read"][data-id]'))if(!prefetched.has(b.dataset.id))prefetchSeen.observe(b.closest('.card-details')?b.closest('article'):b)})}).observe(document.body,{childList:true,subtree:true});
// Chats (Slack, WhatsApp, Telegram, Intercom and the rest: event_views' chat) read as one thread, oldest first: the
// conversation named once on top, a day line when the day changes, each sender's run of messages under their name and
// time once, a light time inside a run only after a pause. The to-do's own message is tinted when the thread holds more.
// One link opens the whole thread where it lives. Slack's :emoji: codes read as emoji (chatEmoji).
const THREAD_APP={Slack:'Slack',WhatsApp:'WhatsApp',Telegram:'Telegram',Intercom:'Intercom',LinkedIn:'LinkedIn','X message':'X'};
const THREAD_VIA={Slack:'slack',WhatsApp:'whatsapp',Telegram:'telegram',Intercom:'intercom',LinkedIn:'linkedin','X message':'x'};
const isChat=o=>typeof o?.chat==='string';
const chatTitle=o=>o.dm&&o.chat?t('DM with {}',o.chat):o.chat||'';
const THREAD_PAUSE=10*6e4;
function chatThreadHTML(items,{main,names=true,head=true,src,earlier}={}){
const dayOf=at=>{const d=new Date(at);return d.toLocaleDateString(DL,{weekday:'long',day:'numeric',month:'long',...(d.getFullYear()!==new Date().getFullYear()?{year:'numeric'}:{})})};
const msgs=items.flatMap(o=>o.turns?.length?o.turns.map(x=>({...x,kind:o.kind})):[o]).filter(o=>String(o.body||'').trim()||o.photo).sort((a,b)=>Date.parse(a.occurred_at)-Date.parse(b.occurred_at));
const days=[];let prev=null;
for(const o of msgs){const at=Date.parse(o.occurred_at),day=dayOf(at),me=o.from==='You',mark=main!=null&&o.event_id===main&&msgs.length>1;
 if(days.at(-1)?.day!==day){days.push({day,turns:[]});prev=null}
 const turns=days.at(-1).turns,say=html`${o.note?html`<span class="convo-tag">${t('Note')}</span>`:''}${linkify(chatEmoji(String(o.body||'').replace(/\r\n/g,'\n').trim()))}${o.photo?photoThumbs([o.photo]):''}`;
 if(!prev||prev.from!==o.from)turns.push({me,says:[],meta:html`<p class="convo-meta">${!me&&names&&sender(o.from)?html`<b>${sender(o.from)}</b> · `:''}<time datetime="${o.occurred_at}">${fmtHM(at)}</time></p>`});
 else if(at-Date.parse(prev.occurred_at)>=THREAD_PAUSE)turns.at(-1).says.push(html`<p class="convo-at"><time datetime="${o.occurred_at}">${fmtHM(at)}</time></p>`);
 turns.at(-1).says.push(html`<div class="convo-say${mark?' convo-main':''}${o.note?' convo-note':''}"${mark?html` aria-label="${t('The message this to-do is about')}"`:''}>${say}</div>`);prev=o}
const first=items.find(o=>o.event_id===main)||items[0]||{},title=head?chatTitle(first):'',app=THREAD_APP[first.kind]||src;
const url=[first,...[...items].reverse()].find(o=>o?.url&&safeURL(o.url))?.url;
return html`<div class="convo">${title?html`<p class="convo-chat">${viaIco(THREAD_VIA[first.kind],true)}<span>${title}</span></p>`:''}${earlier?earlierButton():''}${days.map(d=>html`<p class="convo-day">${d.day}</p>${d.turns.map(x=>html`<div class="convo-turn${x.me?' me':''}">${x.meta}${x.says}</div>`)}`)}${url?html`<a class="convo-source" href="${url}" target="_blank" rel="noreferrer">${app?t('Open in {} ↗',app):t('Open original')}</a>`:''}</div>`}
// A to-do's chat sources by conversation: the to-do's own conversation first, each one thread.
function chatThreads(list){const by=new Map();for(const o of list.filter(isChat)){const k=o.kind+'\u0000'+o.chat;if(!by.has(k))by.set(k,[]);by.get(k).push(o)}return [...by.values()]}
// A to-do's source opens with what was said around it (api/originals' around, machine/store/conversation.py): the
// messages before it and the replies after it, the source tinted and in view, and a quiet Show earlier for older ones.
const earlierButton=()=>html`<button type="button" class="link convo-earlier" data-convo-earlier>${t('Show earlier')}</button>`;
const nearOf=(id,list)=>{const c=around.get(id);if(!c)return {before:[],after:[]};const have=new Set(list.map(o=>o.event_id)),mark=o=>({...o,near:true}),keep=o=>o.event_id==null||!have.has(o.event_id);
 return {before:c.before.filter(keep).map(mark),after:c.after.filter(keep).map(mark),main:c.event_id,earlier:c.earlier}};
async function showEarlier(id,button){const c=around.get(id),from=c?.before.find(o=>o.event_id!=null)?.event_id??c?.event_id;if(!c||from==null)return;
 button.disabled=true;let r;try{r=(await request(`api/originals?id=${encodeURIComponent(id)}&before=${encodeURIComponent(from)}`)).around}catch(e){button.disabled=false;errCaught(e);toast(e.message,true);return}
 const dialog=$('#email-dialog'),fromEnd=dialog.scrollHeight-dialog.scrollTop;  // what was in view stays in view
 const seen=new Set(c.before.map(o=>o.event_id).filter(v=>v!=null)),live=new Set(c.before.filter(o=>o.event_id==null).map(o=>o.occurred_at+o.from));
 c.before=[...(r?.before||[]).filter(o=>o.event_id==null?!live.has(o.occurred_at+o.from):!seen.has(o.event_id)),...c.before];c.earlier=Boolean(r?.earlier);
 await openEmail(id,{keep:true});dialog.scrollTop=dialog.scrollHeight-fromEnd}
const peek=o=>String(o.body||'').replace(/\s+/g,' ').trim().slice(0,160);  // a folded email's first words, on one line
const emailRow=(o,i)=>html`<details class="email email-near" data-msg="${i}"><summary>${sender(o.from)||kindLabel(o.kind)} · ${new Date(o.occurred_at).toLocaleDateString(DL,{day:'numeric',month:'short'})}${peek(o)?html`<span class="email-peek">${peek(o)}</span>`:''}</summary>${messageHTML(o,'',i)}</details>`;
async function openEmail(id,{keep}={}){const s=state.suggestions.find(s=>s.id===id);const dialog=$('#email-dialog');
if(!keep){$('#email-title').textContent=s?.title||'Original';setHTML($('#email-content'),html`<p class="muted">Loading…</p>`);dialog.showModal()}
let list;try{list=await originalsFor(id)}catch(e){errCaught(e);setHTML($('#email-content'),html`<p class="muted">${e.message}</p>`);return}
if(!list.length){setHTML($('#email-content'),html`${draftFilesBlock(s)}<p class="muted">The original is no longer available.</p>`);return}
const [first,...rest]=list,near=nearOf(id,list),all=[...list,...near.before,...near.after],at=o=>all.indexOf(o);
if(first.kind==='calendar'&&!rest.length&&!draftFiles(s||{}).length){openMeeting(first.event_id,s?.title);return}  // a to-do from a meeting: the meeting itself
const box=$('#email-content'),wire=()=>{box.querySelectorAll('details.email').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)fillMessage(d,all[+d.dataset.msg],id)}));
 box.querySelector('[data-convo-earlier]')?.addEventListener('click',e=>showEarlier(id,e.currentTarget))};
const inView=()=>{if(!keep)box.querySelector('.convo-main,.email-main')?.scrollIntoView({block:box.querySelector('.convo-main')?'center':'start'})};
// A chat to-do: its conversation as one thread, with what was said around it (its other conversations after it); anything else still as related messages
if(isChat(first)){const others=list.filter(o=>!isChat(o)),main=near.main??first.event_id;
 setHTML(box,html`${draftFilesBlock(s)}${chatThreads([...list,...near.before,...near.after]).map(c=>chatThreadHTML(c,{main,earlier:near.earlier&&c.some(o=>o.event_id===main)}))}${others.length?html`<h3 class="email-earlier">${t(['{} related message','{} related messages'],others.length)}</h3>${others.map(o=>html`<details class="email" data-msg="${at(o)}"><summary>${sender(o.from)||kindLabel(o.kind)} · ${new Date(o.occurred_at).toLocaleDateString(DL,{day:'numeric',month:'short'})}</summary>${messageHTML(o,id,at(o))}</details>`)}`:''}`);
 wire();inView();return}
// An email: the thread's earlier mail folded above it and the replies below, the to-do's own one open and marked
const chats=rest.filter(isChat),mails=rest.filter(o=>!isChat(o)),threaded=near.before.length||near.after.length||near.earlier;
setHTML(box,html`${draftFilesBlock(s)}${near.earlier?earlierButton():''}${near.before.map(o=>emailRow(o,at(o)))}<div class="email${threaded?' email-main':''}" data-msg="0"${threaded?html` aria-label="${t('The message this to-do is about')}"`:''}>${messageHTML(first,id,0)}</div>${near.after.map(o=>emailRow(o,at(o)))}${mails.length?html`<h3 class="email-earlier">${t(['{} related message','{} related messages'],mails.length)}</h3>${mails.map(o=>html`<details class="email" data-msg="${at(o)}"><summary>${sender(o.from)||kindLabel(o.kind)} · ${new Date(o.occurred_at).toLocaleDateString(DL,{day:'numeric',month:'short'})}</summary>${messageHTML(o,id,at(o))}</details>`)}`:''}${chatThreads(chats).map(c=>chatThreadHTML(c))}`);
fillMessage(box.querySelector('[data-msg="0"]'),first,id);wire();inView()}
