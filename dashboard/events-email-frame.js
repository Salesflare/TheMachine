// A lazy part (dashboard_parts.LAZY 'emailframe'): an email's HTML in its sandboxed frame. events-email.js fillMessage
// loads it through lazyPart('emailframe') when a message is first read.
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
