// A lazy part (dashboard_parts.LAZY 'msshare'): the milestone's share dialog, which todos-milestone.js msShare loads
// when it opens. On a computer Share opens it straight away (a computer's own share sheet, like Windows', offers little
// for an image); on a phone it's there where no share sheet is. The image (Square or For links), Download image, Copy
// image (or, on a phone, Share image where the clipboard takes no image but a share sheet is there), and the text to
// post. Download is a blob: link, which a browser saves and the phone app takes (a data: link does nothing in a
// WebView); that WebView puts no image on the clipboard, so no Copy image there. What each button did shows in the
// dialog: a toast would sit under it.
const msCopyImage=()=>!msApp()&&isSecureContext&&!!(window.ClipboardItem&&navigator.clipboard?.write);
const msShareImage=()=>!msDesk()&&(msAppSheet()||msWebShare(new File([new Blob(['x'],{type:'image/png'})],'x.png',{type:'image/png'})));
let msWide=false,msShown=null,msShownUrl=null;
const msSay=(text,bad=false)=>{const p=$('#ms-share .ms-said');if(!p)return;p.textContent=text;p.hidden=!text;p.classList.toggle('bad',bad)};
// A copy or share that didn't work says so; on a computer it never falls back to the share sheet
const msNoSheet=async(file,n)=>{if(msDesk()||!await msSheet(file,n))msSay(t('That didn’t work here. Download the image instead.'),true)};
async function msDialog(n){let d=$('#ms-share');
 if(!d){d=document.createElement('dialog');d.id='ms-share';d.setAttribute('aria-labelledby','ms-share-title');document.body.append(d);
  d.addEventListener('click',async e=>{const b=e.target.closest('button');if(e.target===d){d.close();return}if(!b)return;
   if(b.dataset.msSize!=null){msWide=b.dataset.msSize==='wide';msSay('');await msPreview(+d.dataset.n);return}
   if(b.hasAttribute('data-ms-close-share'))return d.close();
   const n=+d.dataset.n,name=msName(n,msWide),file=()=>new File([msShown],name,{type:'image/png'});msSay('');
   if(b.hasAttribute('data-ms-download')){const a=make('a',{href:msShownUrl,download:name});document.body.append(a);a.click();a.remove()}
   else if(b.hasAttribute('data-ms-copy-image')){try{await navigator.clipboard.write([new ClipboardItem({'image/png':msShown})]);msSay(t('Image copied.'))}catch{await msNoSheet(file(),n)}}
   else if(b.hasAttribute('data-ms-share-image'))await msNoSheet(file(),n);
   else if(b.hasAttribute('data-ms-copy-text')){try{await navigator.clipboard.writeText(msPost(n));msSay(t('Copied.'))}catch{msSay(t('Couldn’t copy. Select it and copy it yourself.'),true)}}});
  // closed (×, Esc, a click outside): focus back on the card's Share, which was disabled while the dialog opened
  d.addEventListener('close',()=>{if(msShownUrl)URL.revokeObjectURL(msShownUrl);msShownUrl=null;$('#milestone [data-ms-share]')?.focus()})}
 d.dataset.n=n;msWide=false;
 setHTML(d,html`<div class="snooze-heading"><h2 id="ms-share-title">${t('Share it')}</h2><button type="button" data-ms-close-share aria-label="${t('Close')}" title="${t('Close')}">×</button></div>
<div class="ms-sizes" role="group" aria-label="${t('Size')}"><button type="button" data-ms-size="square" aria-pressed="true">${t('Square')}</button><button type="button" data-ms-size="wide" aria-pressed="false">${t('For links')}</button></div>
<div class="ms-frame"><img class="ms-preview" alt="${t('{} to-dos done',msNum(n))}"></div>
<div class="ms-acts"><button type="button" class="primary" data-ms-download autofocus>${t('Download image')}</button>${msCopyImage()?html`<button type="button" data-ms-copy-image>${t('Copy image')}</button>`:msShareImage()?html`<button type="button" data-ms-share-image>${t('Share image')}</button>`:''}</div>
<p class="ms-said" role="status" hidden></p>
<div class="ms-post"><span>${t('Text to post')}</span><button type="button" class="quiet" data-ms-copy-text>${t('Copy text')}</button><p class="ms-post-text">${msPost(n)}</p></div>`);
 await msPreview(n);d.showModal()}
// The image shown is the one every button uses, made a PNG once, so a tap acts at once (Safari and the phone app
// want the download or copy to follow the tap)
async function msPreview(n){const d=$('#ms-share');msShown=await msBlob(await msImage(n,msWide,msDark()));if(msShownUrl)URL.revokeObjectURL(msShownUrl);
 msShownUrl=URL.createObjectURL(msShown);d.querySelector('.ms-preview').src=msShownUrl;
 d.querySelector('.ms-frame').classList.toggle('wide',msWide);d.querySelectorAll('[data-ms-size]').forEach(b=>b.setAttribute('aria-pressed',String((b.dataset.msSize==='wide')===msWide)))}
