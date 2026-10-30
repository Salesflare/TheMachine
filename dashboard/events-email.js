// The messages behind each card, read in a dialog. HTML renders in a sandboxed frame:
// no scripts, forms or navigation of the dashboard; links open in a new tab.
const originals=new Map(),emailViews=new Map();
const fileSize=b=>!b?'':b<1024?b+' B':b<1048576?Math.round(b/1024)+' KB':(b/1048576).toFixed(1)+' MB';
const sender=v=>String(v||'').replace(/\s*<[^>]+>/,'').replace(/^"|"$/g,'').trim()||String(v||'');
const linkify=t=>esc(t).replace(/https?:\/\/[^\s<]+[^\s<.,;:!?)\]'"]/g,u=>`<a href="${u}" target="_blank" rel="noreferrer">${u}</a>`);
const apiURL=path=>new URL(path,document.baseURI).href;
// Any card built from collected messages can show them, including older cards without a source line.
const eventIds=s=>{try{return Array.isArray(s.event_ids)?s.event_ids:JSON.parse(s.event_ids||'[]')}catch{return []}};
const cardViaIcon=s=>{const v=/^Source:\s*([^·\n]+)/i.exec(s.source_line||'')?.[1]||'';return isEmail(s)?'mail':/note/i.test(v)?'note':/calendar/i.test(v)?'cal':/^(email|gmail|outlook|mail)/i.test(v.trim())?'mail':'chat'};
// A card the owner added has their own words as its only signal until the review links an email: nothing to open yet.
const hasOriginal=s=>Boolean(s.source_line||(s.origin!=='owner'&&eventIds(s).length)||(s.original_urls||[]).length);
const isEmail=s=>/^Source: email/.test(s.source_line||'')||(s.original_urls||[]).some(u=>/^https:\/\/(mail\.google\.com|outlook\.(office|office365|live)\.com)\//.test(u));
const originalsFor=id=>{if(!originals.has(id))originals.set(id,request('api/originals?id='+id).then(r=>r.originals).catch(e=>{originals.delete(id);throw e}));return originals.get(id)};
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
const meta=[['From',o.from],['To',o.to],['Cc',o.cc]].filter(([,v])=>v).map(([k,v])=>`<div><span>${k}</span> ${esc(v)}</div>`).join('')+(o.details?`<pre class="email-tech">${esc(o.details)}</pre>`:'');
return `<div class="email-meta"><div class="email-from"><strong>${esc(sender(o.from)||kindLabel(o.kind))}</strong><time>${esc(fmtDHM(o.occurred_at,{weekday:'short',day:'numeric',month:'short'}))}</time></div>${o.title?`<div class="email-subject">${esc(o.title)}</div>`:''}${meta?`<details class="email-headers"><summary>Details</summary>${meta}</details>`:''}</div>${(o.attachments||[]).length?`<div class="attachments">${o.attachments.map(a=>`<a class="attachment" href="api/attachment?id=${id}&event=${encodeURIComponent(o.event_id)}&part=${encodeURIComponent(a.part)}" target="_blank" rel="noreferrer">📎 ${esc(a.name)}<small>${esc(fileSize(a.size))}</small></a>`).join('')}</div>`:''}<div class="email-body" data-email-body="${i}"><p class="muted">Loading…</p></div>${o.kind==='calendar'&&!o.raw?`<p class="email-open"><button type="button" class="link" data-open-meeting="${esc(o.event_id)}">${esc(t('Notes and transcript'))}</button></p>`:''}${o.url&&safeURL(o.url)?`<p class="email-open"><a href="${esc(o.url)}" target="_blank" rel="noreferrer">${o.kind==='calendar'?esc(t(calOpenLabel(o.url))):`Open in ${o.kind==='email'?(/^https:\/\/outlook\./.test(o.url||'')?'Outlook':'Gmail'):['phone','signal'].includes(o.kind)?'app':esc(o.kind)} ↗`}</a></p>`:''}`}
async function fillMessage(container,o,id){
const box=container.querySelector('.email-body');if(!box||box.dataset.filled)return;box.dataset.filled='1';
const said=String(o.body||'').replace(/\r\n/g,'\n').split('\n').filter(l=>!(o.kind==='calendar'&&/^Participants: /.test(l))).join('\n').trim();  // an invite's raw guest addresses: the meeting's With has them by name
const text=()=>{box.innerHTML=said?`<div class="email-text">${linkify(said)}</div>`:`<p class="muted">${esc(t('No description.'))}</p>`};
if(o.kind!=='email'){text();return}
const view=await emailViewFor(id,o.event_id);if(!view.html){text();return}
const frame=document.createElement('iframe');frame.className='email-frame';frame.title='Email';frame.setAttribute('sandbox','allow-same-origin allow-popups allow-popups-to-escape-sandbox');frame.setAttribute('referrerpolicy','no-referrer');
frame.style.visibility='hidden';const reveal=()=>{const doc=frame.contentDocument;if(doc?.body&&dark())try{darkenEmail(doc)}catch{}frame.style.visibility=''};setTimeout(reveal,1500);
frame.addEventListener('load',()=>{reveal();const doc=frame.contentDocument;if(!doc)return;const fit=()=>{frame.style.height=Math.min(Math.max(Math.ceil(doc.body.getBoundingClientRect().height),80),20000)+'px'};fit();new ResizeObserver(fit).observe(doc.body)});
frame.srcdoc=emailDoc(view.html,view.images||{},id,o.event_id);box.replaceChildren(frame)}
// Files attached to this card's email draft, as links that open over the Tailscale dashboard.
const draftFileLinks=(id,files)=>(files||[]).map(a=>`<a class="attachment" href="api/draft-attachment?id=${encodeURIComponent(id)}&sha=${encodeURIComponent(a.sha256)}" target="_blank" rel="noreferrer">📎 ${esc(a.name)}<small>${esc(fileSize(a.size))}</small></a>`).join('');
const draftFiles=s=>{const seen=new Set();return taskActions(s).filter(a=>['email','email_demo'].includes(a.kind)).flatMap(a=>a.attachments||[]).filter(a=>!seen.has(a.sha256)&&seen.add(a.sha256))};
const draftFilesBlock=s=>{const files=draftFiles(s);return files.length?`<div class="draft-files"><h3>Attached to your draft</h3><div class="attachments">${draftFileLinks(s.id,files)}</div></div>`:''};
const emailViewFor=(id,ev)=>{const key=id+':'+ev;if(!emailViews.has(key))emailViews.set(key,request(`api/email?id=${id}&event=${encodeURIComponent(ev)}`).catch(()=>{emailViews.delete(key);return {html:''}}));return emailViews.get(key)};
// Cards on screen read their email ahead, quietly: two at a time when the browser is idle, each card once, the last
// PREFETCH_KEEP kept. Opening one is then instant.
const PREFETCH_KEEP=30,prefetchQueue=[],prefetched=new Set();let prefetching=0;
const idle=f=>(window.requestIdleCallback||(g=>setTimeout(g,200)))(f);
function trim(map){while(map.size>PREFETCH_KEEP)map.delete(map.keys().next().value)}
function prefetchNext(){while(prefetching<2&&prefetchQueue.length){const id=prefetchQueue.shift();prefetching++;
 idle(async()=>{try{const list=await originalsFor(id),first=list[0];if(first?.kind==='email')await emailViewFor(id,first.event_id);trim(originals);trim(emailViews)}catch{prefetched.delete(id)}finally{prefetching--;prefetchNext()}})}}
// A to-do's source sits behind Details: the to-do itself coming into sight reads its original ahead.
const prefetchSeen=window.IntersectionObserver?new IntersectionObserver(entries=>{for(const e of entries){if(!e.isIntersecting)continue;prefetchSeen.unobserve(e.target);const id=e.target.dataset.id||e.target.querySelector('[data-original="read"][data-id]')?.dataset.id;
 if(id&&!prefetched.has(id)&&!originals.has(id)){prefetched.add(id);prefetchQueue.push(id)}}prefetchNext()},{rootMargin:'100px'}):null;
let prefetchScan=0;if(prefetchSeen)new MutationObserver(()=>{cancelAnimationFrame(prefetchScan);prefetchScan=requestAnimationFrame(()=>{for(const b of document.querySelectorAll('[data-original="read"][data-id]'))if(!prefetched.has(b.dataset.id))prefetchSeen.observe(b.closest('.card-details')?b.closest('article'):b)})}).observe(document.body,{childList:true,subtree:true});
async function openEmail(id){const s=state.suggestions.find(s=>s.id===id);const dialog=$('#email-dialog');$('#email-title').textContent=s?.title||'Original';$('#email-content').innerHTML='<p class="muted">Loading…</p>';dialog.showModal();
let list;try{list=await originalsFor(id)}catch(e){errCaught(e);$('#email-content').innerHTML=`<p class="muted">${esc(e.message)}</p>`;return}
if(!list.length){$('#email-content').innerHTML=draftFilesBlock(s)+'<p class="muted">The original is no longer available.</p>';return}
const [first,...rest]=list;
if(first.kind==='calendar'&&!rest.length&&!draftFiles(s||{}).length){openMeeting(first.event_id,s?.title);return}  // a to-do from a meeting: the meeting itself
$('#email-content').innerHTML=draftFilesBlock(s)+`<div class="email" data-msg="0">${messageHTML(first,id,0)}</div>`+(rest.length?`<h3 class="email-earlier">${t(['{} related message','{} related messages'],rest.length)}</h3>`+rest.map((o,i)=>`<details class="email" data-msg="${i+1}"><summary>${esc(sender(o.from)||kindLabel(o.kind))} · ${esc(new Date(o.occurred_at).toLocaleDateString(DL,{day:'numeric',month:'short'}))}</summary>${messageHTML(o,id,i+1)}</details>`).join(''):'');
fillMessage($('#email-content [data-msg="0"]'),first,id);
$('#email-content').querySelectorAll('details.email').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)fillMessage(d,list[+d.dataset.msg],id)}))}
