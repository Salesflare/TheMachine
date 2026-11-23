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
// The frame takes the email's own height. Templates tie theirs to the frame's (html,body{height:100%!important},
// min-height:100vh): measured as drawn, the frame stayed as small as it started, or grew with every fit. So html and
// body get their natural height (inline !important outranks the email's own), and the email is measured in a frame of
// no height (no vh to fill), its box holding its place meanwhile so nothing above it scrolls.
frame.addEventListener('load',()=>{reveal();const doc=frame.contentDocument,root=doc?.documentElement;if(!doc?.body)return;doc.addEventListener('click',openMailLink);
 for(const el of [root,doc.body])for(const [k,v] of [['height','auto'],['min-height','0'],['max-height','none'],['overflow','visible']])el.style.setProperty(k,v,'important');
 const fit=()=>{box.style.minHeight=frame.offsetHeight+'px';frame.style.height='0';
  frame.style.height=Math.min(Math.max(root.scrollHeight,doc.body.scrollHeight,80),20000)+'px';box.style.minHeight=''};
 fit();new ResizeObserver(fit).observe(doc.body);doc.addEventListener('load',fit,true);doc.fonts?.ready.then(fit)});
frame.srcdoc=emailDoc(view.html,view.images||{},id,o.event_id,o.local);box.replaceChildren(frame)}
// The dialog with a to-do's messages (openEmail in events-email.js opens it once this part is in), or with one opened
// from anywhere else (ev: {ids, title, raw, local, run}, openOriginal in events-list.js): read the same way, with what was
// said around it. ev.ids: the newest last; several are the new ones of one row, all marked. ev.run: a Graph row that is
// itself a conversation (chatThreadHTML's options), with nothing in it marked.
const eventsFor=(id,ev)=>{const last=ev.ids.at(-1),r=request('api/originals?'+(ev.ids.length>1?`events=${ev.ids}&near=${last}`:'event='+last)).then(({originals:list,around:c})=>{
 const own=new Map(list.map(o=>[o.event_id,Object.assign(o,{own:true,raw:!!ev.raw,local:!!ev.local})])),first=own.get(last)||list[0];own.delete(first?.event_id);
 // the row's other messages take their place in what is around, each as it is when opened (an email's HTML and files)
 const place=l=>l.map(o=>{const m=own.get(o.event_id);own.delete(o.event_id);return m?{...o,...m}:o});
 if(c){c.before=place(c.before);c.after=place(c.after);for(const x of ev.run?[]:c.rest||[]){x.items=[...place(x.before),...x.ids.filter(i=>own.has(i)).map(i=>own.get(i)),...place(x.after)];x.ids.forEach(i=>own.delete(i))}}
 around.set(id,c||null);return first?[first,...own.values()]:[]});originals.set(id,r);return r};
const relatedHTML=(list,id,at)=>list.length?html`<h3 class="email-earlier">${t(['{} related message','{} related messages'],list.length)}</h3>${list.map(o=>html`<details class="email" data-msg="${at(o)}"><summary>${sender(o.from)||kindLabel(o.kind)} · ${localeDate(new Date(o.occurred_at),DL,{day:'numeric',month:'short'})}</summary>${messageHTML(o,id,at(o))}</details>`)}`:'';
async function emailOpen(id,{keep,ev}={}){const s=ev?null:state.suggestions.find(s=>s.id===id),box=$('#email-content'),files=s?draftFilesBlock(s):'';
if(!keep&&!ev)mailDialog(s?.title);
let list;try{[list]=await Promise.all([ev&&!keep?eventsFor(id,ev):originalsFor(id),lazyPart('msgview')])}catch(e){errCaught(e);setHTML(box,html`<p class="muted">${e.message}</p>`);return}
if(!list.length){setHTML(box,html`${files}<p class="muted">The original is no longer available.</p>`);return}
const [first,...rest]=list,near=nearOf(id,list),all=[...list,...near.before,...near.after],at=o=>all.indexOf(o),src=ev?'':id;
if(first.kind==='calendar'&&(ev||!rest.length)&&!first.raw&&!files){openMeeting(first.event_id,(ev||s)?.title);return}  // the meeting itself
// Opened by itself: titled by the message (an email's subject, a chat's conversation), not by the row it was opened from
const shown=ev?ev.run&&ev.title||viewTitle(first)||ev.title||t('Original'):s?.title;if(ev)$('#email-title').textContent=shown;
const mark=ev?t(ev.ids.length>1?'New messages':'This message'):'';
const wire=()=>{box.querySelectorAll('details.email').forEach(d=>{const fill=()=>{if(d.open)fillMessage(d,all[+d.dataset.msg],src)};fill();d.addEventListener('toggle',fill)});
 box.querySelector('[data-convo-earlier]')?.addEventListener('click',e=>showEarlier(id,e.currentTarget,ev))};
const inView=()=>{const main=box.querySelector('.convo-main,.convo-from,.email-main');if(!keep)main?.scrollIntoView({block:main.matches('.email-main')?'start':'center'})};
// A chat: its conversation as one thread, with what was said around it (its other conversations after it); anything else still as related messages
if(isChat(first)){const others=list.filter(o=>!isChat(o)),main=near.main??first.event_id,marks=ev?ev.ids:[main];
 setHTML(box,html`${files}${chatThreads([...list,...near.before,...near.after]).map((c,i)=>chatThreadHTML(c,{main:marks,mark,earlier:near.earlier&&c.some(o=>o.event_id===main),titled:ev&&!ev.run&&!i,...ev?.run}))}${near.rest.map(x=>chatThreadHTML(x.items.map(o=>({...o,thread:x.thread})),{main:marks,mark,plain:x.thread,head:false,titled:!x.thread}))}${relatedHTML(others,src,at)}`);
 wire();inView();return}
// An email: the thread's earlier mail folded above it and the replies below, the opened one open and marked
const threaded=near.before.length||near.after.length||near.earlier;
setHTML(box,html`${files}${near.earlier?earlierButton():''}${near.before.map(o=>emailRow(o,at(o)))}<div class="email${threaded?' email-main':''}" data-msg="0"${threaded?html` aria-label="${mark||t('The message this to-do is about')}"`:''}>${messageHTML(first,src,0,shown)}</div>${near.after.map(o=>emailRow(o,at(o)))}${relatedHTML(rest.filter(o=>!isChat(o)),src,at)}${chatThreads(rest).map(c=>chatThreadHTML(c))}`);
fillMessage(box.querySelector('[data-msg="0"]'),first,src);wire();inView()}
