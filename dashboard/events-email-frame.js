// A lazy part (dashboard_parts.LAZY 'emailframe'): the messages dialog and an email's HTML in its sandboxed frame.
// events-email.js loads it through lazyPart('emailframe') when a to-do's messages are first opened.
// Dark mode for HTML emails, like Gmail's: light backgrounds turn dark and dark text turns light,
// keeping each color's hue. Images keep the light background they were drawn on behind their transparent parts, so a
// dark logo on a see-through background stays readable.
function rgbHsl(r,g,b){r/=255;g/=255;b/=255;const max=Math.max(r,g,b),min=Math.min(r,g,b),l=(max+min)/2;if(max===min)return [0,0,l];const d=max-min,s=l>.5?d/(2-max-min):d/(max+min);const h=max===r?(g-b)/d+(g<b?6:0):max===g?(b-r)/d+2:(r-g)/d+4;return [h*60,s,l]}
function darkenEmail(doc){
const win=doc.defaultView,hsl=(h,s,l,a)=>`hsla(${h.toFixed(0)},${(s*100).toFixed(0)}%,${(l*100).toFixed(0)}%,${a})`;
const parse=c=>{const m=/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/.exec(c||'');return m?[...rgbHsl(+m[1],+m[2],+m[3]),m[4]===undefined?1:+m[4]]:null};
// Email templates can paint the canvas on <html>, not just on their body/tables.
// Each element's own light background, as the email drew it; an email that paints none was drawn on white.
const light=new Map([[doc.documentElement,'#fff']]),ours=win.getComputedStyle(doc.documentElement).backgroundColor;  // ours: the frame's dark canvas (emailDoc)
for(const el of [doc.documentElement,doc.body,...doc.body.querySelectorAll('*')]){
if(['IMG','SVG','PICTURE','VIDEO','CANVAS'].includes(el.tagName.toUpperCase())){
 if(el.tagName.toUpperCase()==='IMG'){let p=el.parentElement;while(p&&!light.has(p))p=p.parentElement;el.style.setProperty('background-color',p?light.get(p):'#fff','important');el.style.setProperty('border-radius','4px')}
 continue}
const cs=win.getComputedStyle(el),bg=parse(cs.backgroundColor),fg=parse(cs.color),border=parse(cs.borderTopColor);
if(bg&&bg[3]>0&&bg[2]>.45){light.set(el,cs.backgroundColor);el.style.setProperty('background-color',hsl(bg[0],bg[1]*.6,.09+(1-bg[2])*.6,bg[3]),'important')}
else if(bg&&bg[3]>0&&cs.backgroundColor!==ours)light.set(el,'');  // a dark background of its own: images on it need nothing behind them
if(fg&&fg[2]<.65)el.style.setProperty('color',hsl(fg[0],fg[1],Math.max(.72,1-fg[2]*.6),fg[3]),'important');
if(border&&border[2]>.6&&parseFloat(cs.borderTopWidth))el.style.setProperty('border-color',hsl(border[0],border[1]*.5,.3,border[3]),'important')}}
const dark=()=>document.documentElement.dataset.theme!=='light';
// local: nothing from outside loads (a mail opened from Spam cleanup: a tracking pixel would tell the sender the address is live)
function emailDoc(html,images,id,ev,local){
const doc=html.replace(/cid:([^"'\s)>]+)/gi,(m,c)=>{const p=images[c]??images[decodeURIComponent(c)];return p===undefined?m:apiURL(`api/attachment?id=${id}&event=${encodeURIComponent(ev)}&part=${encodeURIComponent(p)}`)});
return `<!doctype html><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src ${location.origin}${local?'':' https:'} data:; style-src 'unsafe-inline'; font-src${local?'':' https:'} data:"><meta name="referrer" content="no-referrer"><base target="_blank"><style>${dark()?'html{background:#16191d;color-scheme:dark}body{color:#e6e3dc}a{color:#BCCBA8}':'html{background:#fff}body{color:#202124}'}body{margin:0;padding:18px;font:15px/1.5 system-ui,-apple-system,sans-serif;overflow-wrap:anywhere}html,body{height:auto!important;min-height:0!important}img{max-width:100%;height:auto}table{max-width:100%}
</style>`+doc}
// A link in an email opens outside: a new tab, or the phone's browser in the app. The app's WebView has no windows, so
// a new-tab link goes to the top page, which the frame's sandbox (no top navigation) blocks: the dashboard opens it.
// Only http(s) and mailto, never the dashboard's own addresses; no opener, no referrer.
const mailLink=h=>{try{const u=new URL(h);return /^(https?|mailto):$/.test(u.protocol)&&u.origin!==location.origin?u.href:''}catch{return ''}};
function openMailLink(e){const a=e.target.closest?.('a[href]');if(!a||e.button||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;
 if(/^#/.test(a.getAttribute('href')))return;  // a jump inside the email
 e.preventDefault();const url=mailLink(a.href);
 if(url)Object.assign(document.createElement('a'),{href:url,target:'_blank',rel:'noopener noreferrer'}).click()}
function emailFrame(box,view,o,id){
const frame=document.createElement('iframe');frame.className='email-frame';frame.title='Email';frame.setAttribute('sandbox','allow-same-origin allow-popups allow-popups-to-escape-sandbox');frame.setAttribute('referrerpolicy','no-referrer');
frame.style.visibility='hidden';const reveal=()=>{const doc=frame.contentDocument;if(doc?.body&&dark())try{darkenEmail(doc)}catch{}frame.style.visibility=''};setTimeout(reveal,1500);
frame.addEventListener('load',()=>{reveal();const doc=frame.contentDocument;if(!doc)return;doc.addEventListener('click',openMailLink);const fit=()=>{frame.style.height=Math.min(Math.max(Math.ceil(doc.documentElement.getBoundingClientRect().height),80),20000)+'px'};fit();new ResizeObserver(fit).observe(doc.body)});
frame.srcdoc=emailDoc(view.html,view.images||{},id,o.event_id,o.local);box.replaceChildren(frame)}
// The dialog with a to-do's messages (openEmail in events-email.js opens it once this part is in)
async function emailOpen(id,{keep}={}){const s=state.suggestions.find(s=>s.id===id);const dialog=$('#email-dialog');
if(!keep){$('#email-title').textContent=s?.title||'Original';setHTML($('#email-content'),html`<p class="muted">Loading…</p>`);dialog.showModal()}
let list;try{[list]=await Promise.all([originalsFor(id),lazyPart('msgview')])}catch(e){errCaught(e);setHTML($('#email-content'),html`<p class="muted">${e.message}</p>`);return}
if(!list.length){setHTML($('#email-content'),html`${draftFilesBlock(s)}<p class="muted">The original is no longer available.</p>`);return}
const [first,...rest]=list,near=nearOf(id,list),all=[...list,...near.before,...near.after],at=o=>all.indexOf(o);
if(first.kind==='calendar'&&!rest.length&&!draftFiles(s||{}).length){openMeeting(first.event_id,s?.title);return}  // a to-do from a meeting: the meeting itself
const box=$('#email-content'),wire=()=>{box.querySelectorAll('details.email').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)fillMessage(d,all[+d.dataset.msg],id)}));
 box.querySelector('[data-convo-earlier]')?.addEventListener('click',e=>showEarlier(id,e.currentTarget))};
const inView=()=>{if(!keep)box.querySelector('.convo-main,.email-main')?.scrollIntoView({block:box.querySelector('.convo-main')?'center':'start'})};
// A chat to-do: its conversation as one thread, with what was said around it (its other conversations after it); anything else still as related messages
if(isChat(first)){const others=list.filter(o=>!isChat(o)),main=near.main??first.event_id;
 setHTML(box,html`${draftFilesBlock(s)}${chatThreads([...list,...near.before,...near.after]).map(c=>chatThreadHTML(c,{main,earlier:near.earlier&&c.some(o=>o.event_id===main)}))}${others.length?html`<h3 class="email-earlier">${t(['{} related message','{} related messages'],others.length)}</h3>${others.map(o=>html`<details class="email" data-msg="${at(o)}"><summary>${sender(o.from)||kindLabel(o.kind)} · ${localeDate(new Date(o.occurred_at),DL,{day:'numeric',month:'short'})}</summary>${messageHTML(o,id,at(o))}</details>`)}`:''}`);
 wire();inView();return}
// An email: the thread's earlier mail folded above it and the replies below, the to-do's own one open and marked
const chats=rest.filter(isChat),mails=rest.filter(o=>!isChat(o)),threaded=near.before.length||near.after.length||near.earlier;
setHTML(box,html`${draftFilesBlock(s)}${near.earlier?earlierButton():''}${near.before.map(o=>emailRow(o,at(o)))}<div class="email${threaded?' email-main':''}" data-msg="0"${threaded?html` aria-label="${t('The message this to-do is about')}"`:''}>${messageHTML(first,id,0,s?.title)}</div>${near.after.map(o=>emailRow(o,at(o)))}${mails.length?html`<h3 class="email-earlier">${t(['{} related message','{} related messages'],mails.length)}</h3>${mails.map(o=>html`<details class="email" data-msg="${at(o)}"><summary>${sender(o.from)||kindLabel(o.kind)} · ${localeDate(new Date(o.occurred_at),DL,{day:'numeric',month:'short'})}</summary>${messageHTML(o,id,at(o))}</details>`)}`:''}${chatThreads(chats).map(c=>chatThreadHTML(c))}`);
fillMessage(box.querySelector('[data-msg="0"]'),first,id);wire();inView()}
