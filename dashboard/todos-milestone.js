// A milestone on done to-dos (state.done_milestone, machine/store/done_milestones.py): one small card on top of To-dos,
// "500 to-dos done", the party mascot popping in with a burst of confetti and the number counting up (under 2 s; still
// with reduced motion), Share and ×. × marks it seen on the Machine (done_milestone_seen), so it shows once per level.
// Share draws an image on the device (msImage: a canvas, nothing uploaded) and hands it to the phone's or app's share
// sheet (Web Share with the file); where there is none, a small dialog has Download image, Copy image and the text to
// post. Nothing is ever posted for them. The image holds the count and fixed words only: never a name, a to-do or an
// address. A lazy part (dashboard_parts.LAZY 'milestone'): shell-render.js milestoneSlot loads it only while one is due.
const MS_SITE='themachine.computer',MS_URL='https://themachine.computer';
const MS_X='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7L7 17"/></svg>';
const MS_SHARE='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V3m-4 4 4-4 4 4M5 11v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-8"/></svg>';
const msNum=n=>{try{return new Intl.NumberFormat(DL).format(n)}catch{return String(n)}};
const msLine=n=>n<100?t('Off to a flying start.'):n<1000?t('That’s a lot off your plate.'):t('Look at that momentum.');
const msBrag=()=>t('My Machine and I, on a roll.');  // the image's line: the owner's own words when they post it
const msPost=n=>t('{} to-dos done with The Machine.',msNum(n))+' '+MS_URL;
const msStill=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
const msDark=()=>(document.documentElement.dataset.theme||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))==='dark';
function milestoneCard(){const n=+state?.done_milestone?.count;if(!n)return '';const f=msNum(n);
 return html`<section id="milestone" class="ms-card" aria-labelledby="ms-title"><div class="ms-bot" aria-hidden="true"><img src="brand/party.webp" alt="" width="76" height="76">${raw('<i></i>'.repeat(12))}</div>
<div class="ms-text"><h2 id="ms-title" translate="no">${htmlT('{} to-dos done',html`<b class="ms-n" data-ms-to="${n}">${f}</b>`)}</h2><p translate="no">${msLine(n)}</p></div>
<button type="button" class="primary ms-share" data-ms-share>${raw(MS_SHARE)}${t('Share')}</button><button type="button" class="ms-x" data-ms-close aria-label="${t('Close')}" title="${t('Close')}">${raw(MS_X)}</button></section>`}
// The number counts up as the mascot lands (about 0.9 s), once per card; with reduced motion it just shows
function msCount(){const b=document.querySelector('#milestone .ms-n:not([data-ms-done])');if(!b)return;b.dataset.msDone='';if(msStill())return;
 const to=+b.dataset.msTo,start=performance.now(),ms=900,w=b.getBoundingClientRect().width;b.style.minWidth=w+'px';
 const step=now=>{const k=Math.min(1,(now-start)/ms),e=1-Math.pow(1-k,3);b.textContent=msNum(Math.round(to*e));if(k<1&&b.isConnected)requestAnimationFrame(step);else{b.textContent=msNum(to);b.style.minWidth=''}};
 requestAnimationFrame(step)}
new MutationObserver(msCount).observe($('#suggestions'),{childList:true});msCount();
// The image: a bold block of the brand's color, the number huge, the party mascot big, the wordmark and the site.
// Square (1080) for a feed, wide (1200x630) for a link preview; light or dark like the dashboard. Its only inputs are
// the count, the size and the theme; every word on it is fixed text in the owner's language.
const MS_WORDMARK=['M20 40v-7h7v-7h7v7h7v7M49 40v-7h7v-7h7v7h7v7M37 52v6h14v-6',[90,'M0 0H28M14 0V40'],[133,'M0 0V40M28 0V40M0 20H28'],[176,'M28 0H0V40H28M0 20H23'],
 [236,'M0 40V0L14 21L28 0V40'],[279,'M0 40L14 0L28 40M6 24H22'],[322,'M28 3Q0 -8 0 20Q0 48 28 37'],[365,'M0 0V40M28 0V40M0 20H28'],[408,'M4 0H24M14 0V40M4 40H24'],
 [451,'M0 40V0L28 40V0'],[494,'M28 0H0V40H28M0 20H23']];
const MS_THEME={dark:{bg:['#40366a','#1f1b33'],glow:'#c7b5e259',num:'#ffd76b',ink:'#f5e5bf',soft:'#e6deefcc',chip:'#ffffff14',bits:['#ffd76b','#bccba8','#c7b5e2','#eca45b','#f5e5bf']},
 light:{bg:['#ffe07f','#ffcf4d'],glow:'#ffffff80',num:'#1d1d1b',ink:'#1d1d1b',soft:'#1d1d1bb3',chip:'#1d1d1b12',bits:['#4e6b34','#5e4f86','#b0561a','#ffffff','#1d1d1b']}};
let msArt=null;
const msBot=()=>msArt??=new Promise((ok,no)=>{const im=new Image();im.crossOrigin='anonymous';im.onload=()=>ok(im);im.onerror=()=>{msArt=null;no(new Error(t('Couldn’t make the image. Try again in a moment.')))};im.src='brand/party-512.webp'});
const msFont=(w,px,fam)=>`${w} ${px}px ${fam==='serif'?'"Source Serif 4",Georgia,serif':'Inter,system-ui,sans-serif'}`;
// The largest size up to px at which text fits in width
function msFit(c,text,w,px,fam,max){c.font=msFont(w,px,fam);const m=c.measureText(text).width;return m>max?Math.floor(px*max/m):px}
function msWordmark(c,x,y,w,color){const k=w/502;c.save();c.translate(x-20*k,y-26*k);c.scale(k,k);c.strokeStyle=color;c.lineWidth=4.4;c.lineCap=c.lineJoin='round';
 for(const p of MS_WORDMARK){c.save();if(Array.isArray(p))c.translate(p[0],30);c.stroke(new Path2D(Array.isArray(p)?p[1]:p));c.restore()}c.restore()}
// Confetti from a fixed seed: the same image for the same count
function msBits(c,th,W,H,n,keep){let s=n*9301+49297;const r=()=>(s=(s*9301+49297)%233280)/233280;
 for(let i=0;i<34;i++){const x=36+r()*(W-72),y=36+r()*(H-72),w=10+r()*16,h=w*(.45+r()*.3),a=r()*Math.PI;if(keep(x,y))continue;
  c.save();c.translate(x,y);c.rotate(a);c.fillStyle=th.bits[i%th.bits.length];c.globalAlpha=.85;c.beginPath();c.roundRect(-w/2,-h/2,w,h,3);c.fill();c.restore()}}
async function msImage(n,wide,dark){const th=MS_THEME[dark?'dark':'light'],W=wide?1200:1080,H=wide?630:1080;
 await Promise.all([document.fonts?.load(msFont(750,200,'serif')),document.fonts?.load(msFont(650,60,'sans'))]).catch(()=>{});
 const bot=await msBot(),cv=document.createElement('canvas');cv.width=W;cv.height=H;const c=cv.getContext('2d');
 const g=c.createLinearGradient(0,0,W*.4,H);g.addColorStop(0,th.bg[0]);g.addColorStop(1,th.bg[1]);c.fillStyle=g;c.fillRect(0,0,W,H);
 const f=msNum(n),words=t('{} to-dos done',f),rest=words.replace(f,'').trim(),line=msBrag();
 const bs=wide?520:540,bx=wide?W-bs-28:(W-bs)/2,by=wide?(H-bs)/2+10:136,pad=wide?72:80;
 const glow=c.createRadialGradient(bx+bs/2,by+bs/2,10,bx+bs/2,by+bs/2,bs*.66);glow.addColorStop(0,th.glow);glow.addColorStop(1,th.glow.slice(0,7)+'00');c.fillStyle=glow;c.fillRect(0,0,W,H);
 msBits(c,th,W,H,n,(x,y)=>Math.hypot(x-(bx+bs/2),y-(by+bs/2))<bs*.36||(wide?x<bx-10:y>by+bs-30||y<130));
 const mark=wide?250:280;msWordmark(c,pad,wide?66:74,mark,th.ink);
 c.save();c.translate(bx+bs/2,by+bs/2);c.rotate(-.06);c.drawImage(bot,-bs/2,-bs/2,bs,bs);c.restore();
 // the site in a chip: under the words on the wide one, across from the wordmark on the square one
 c.font=msFont(600,wide?28:30,'sans');const sw=c.measureText(MS_SITE).width,ch=wide?52:56,cx=wide?pad:W-pad-sw-44,cy=wide?H-pad-ch+8:(74+mark*44/502/2)-ch/2;
 c.fillStyle=th.chip;c.beginPath();c.roundRect(cx,cy,sw+44,ch,ch/2);c.fill();c.fillStyle=th.ink;c.fillText(MS_SITE,cx+22,cy+ch/2+(wide?10:11));
 const max=wide?bx-pad-20:W-2*pad,x=wide?pad:W/2;c.textAlign=wide?'left':'center';
 c.fillStyle=th.num;c.font=msFont(750,msFit(c,f,750,wide?250:280,'serif',max),'serif');c.fillText(f,x-(wide?6:0),wide?330:by+bs+196);
 c.fillStyle=th.ink;c.font=msFont(700,msFit(c,rest,700,wide?62:66,'sans',max),'sans');c.fillText(rest,x,wide?412:by+bs+282);
 c.fillStyle=th.soft;c.font=msFont(500,msFit(c,line,500,32,'sans',max),'sans');c.fillText(line,x,wide?470:by+bs+338);
 return cv}
const msBlob=cv=>new Promise((ok,no)=>cv.toBlob(b=>b?ok(b):no(new Error(t('Couldn’t make the image. Try again in a moment.'))),'image/png'));
const msName=(n,wide)=>`the-machine-${n}-todos${wide?'-wide':''}.png`;
// Share: the phone's or app's own share sheet with the square image, or the dialog where there is none
let msReady=null;
async function msShare(btn){const n=+state?.done_milestone?.count,dark=msDark();if(!n)return;btn.disabled=true;
 try{const blob=(msReady?.n===n&&msReady.dark===dark&&await msReady.blob)||await msBlob(await msImage(n,false,dark)),file=new File([blob],msName(n,false),{type:'image/png'});
  if(navigator.canShare?.({files:[file]})){try{await navigator.share({files:[file],text:msPost(n)})}catch(e){if(e.name!=='AbortError')await msDialog(n)}}
  else await msDialog(n)}
 catch(e){errCaught(e);toast(e.message,true)}finally{btn.disabled=false}}
// The dialog: the image (Square or For links), Download image, Copy image where the browser can, and the text to post
const msCopyImage=()=>!!(window.ClipboardItem&&navigator.clipboard?.write);
let msWide=false,msShown=null;
async function msDialog(n){let d=$('#ms-share');
 if(!d){d=document.createElement('dialog');d.id='ms-share';d.setAttribute('aria-labelledby','ms-share-title');document.body.append(d);
  d.addEventListener('click',async e=>{const b=e.target.closest('button');if(e.target===d){d.close();return}if(!b)return;
   if(b.dataset.msSize!=null){msWide=b.dataset.msSize==='wide';await msPreview(+d.dataset.n);return}
   if(b.hasAttribute('data-ms-close-share'))return d.close();
   try{if(b.hasAttribute('data-ms-download')){const a=make('a',{href:msShown.toDataURL('image/png'),download:msName(+d.dataset.n,msWide)});document.body.append(a);a.click();a.remove()}
    else if(b.hasAttribute('data-ms-copy-image')){await navigator.clipboard.write([new ClipboardItem({'image/png':msBlob(msShown)})]);toast(t('Image copied.'))}
    else if(b.hasAttribute('data-ms-copy-text')){await navigator.clipboard.writeText(msPost(+d.dataset.n));toast(t('Copied.'))}}
   catch(err){errCaught(err);toast(t('Couldn’t copy. Select it and copy it yourself.'),true)}})}
 d.dataset.n=n;msWide=false;
 setHTML(d,html`<button type="button" class="ms-x" data-ms-close-share aria-label="${t('Close')}" title="${t('Close')}">${raw(MS_X)}</button><h2 id="ms-share-title">${t('Share it')}</h2>
<div class="ms-sizes" role="group" aria-label="${t('Size')}"><button type="button" data-ms-size="square" aria-pressed="true">${t('Square')}</button><button type="button" data-ms-size="wide" aria-pressed="false">${t('For links')}</button></div>
<div class="ms-frame"><img class="ms-preview" alt="${t('{} to-dos done',msNum(n))}"></div>
<div class="ms-acts"><button type="button" class="primary" data-ms-download>${t('Download image')}</button>${msCopyImage()?html`<button type="button" data-ms-copy-image>${t('Copy image')}</button>`:''}</div>
<div class="ms-post"><span>${t('Text to post')}</span><button type="button" class="quiet" data-ms-copy-text>${t('Copy text')}</button><p class="ms-post-text">${msPost(n)}</p></div>`);
 await msPreview(n);d.showModal()}
async function msPreview(n){const d=$('#ms-share');msShown=await msImage(n,msWide,msDark());d.querySelector('.ms-preview').src=msShown.toDataURL('image/png');
 d.querySelector('.ms-frame').classList.toggle('wide',msWide);d.querySelectorAll('[data-ms-size]').forEach(b=>b.setAttribute('aria-pressed',String((b.dataset.msSize==='wide')===msWide)))}
// × : seen on the Machine, for every device; the card goes once it says so
$('#suggestions').addEventListener('click',async e=>{
 const s=e.target.closest('[data-ms-share]');if(s){msShare(s);return}
 const x=e.target.closest('[data-ms-close]');if(!x)return;const n=+state?.done_milestone?.count;x.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'done_milestone_seen',args:{count:n}})});
  state.done_milestone=r.done_milestone??null;render()}catch(err){errCaught(err);x.disabled=false;toast(err.message,true)}});
// The square image is drawn ahead, once the card is in, so Share opens the sheet at once (a share must follow the tap)
(self.requestIdleCallback||setTimeout)(()=>{const n=+state?.done_milestone?.count,dark=msDark();if(n)msReady={n,dark,blob:msImage(n,false,dark).then(msBlob).catch(()=>null)}},{timeout:3000});
