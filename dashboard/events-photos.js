// WhatsApp photos the Machine read (whatsapp_images.py): a thumbnail where its message shows (a to-do, its chat,
// Messages), and a tap opens it large in its own dialog over the rest. Small ones come inline (data:), the rest from
// api/whatsapp-photo; only those two, never another link. On a WhatsApp connection: Read photos (off until the owner
// turns it on, work chats) and Also in personal chats. Its own style sheet (dashboard.html stays small enough to scan).
document.head.append(Object.assign(document.createElement('style'),{id:'wa-photos',textContent:`
.wa-photos{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 2px}
.wa-photo{display:block;padding:0;border:1px solid var(--border);border-radius:10px;background:var(--sunken);overflow:hidden;cursor:zoom-in;width:112px;height:112px;min-height:0;line-height:0}
.wa-photo img{width:100%;height:100%;object-fit:cover;display:block}
.wa-photo:focus-visible{outline:2px solid var(--mint);outline-offset:2px}
.convo-say .wa-photos{margin:6px 0 2px}.convo-say .wa-photo{width:180px;height:auto;max-height:240px}.convo-say .wa-photo img{height:auto;max-height:240px}
.wa-reads{display:grid;gap:6px;margin:8px 0}.wa-read{display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:.85rem;color:var(--muted);cursor:pointer}
.wa-read small{display:block;font-size:var(--fs-xs,.78rem);color:var(--muted);opacity:.85}.wa-read .lookup-switch{min-height:0;box-shadow:inset 0 0 0 1px var(--border)}.wa-read .lookup-switch[aria-checked=true]{background:var(--mint)}
#wa-photo-view{border:0;padding:0;background:transparent;width:fit-content;max-width:min(94vw,1100px);max-height:92vh;overflow:visible}
#wa-photo-view::backdrop{background:rgba(0,0,0,.82)}
#wa-photo-view img{display:block;max-width:min(94vw,1100px);max-height:88vh;object-fit:contain;border-radius:8px;background:#fff}
#wa-photo-view .wa-photo-close{position:absolute;top:-14px;right:-14px;width:36px;height:36px;min-height:0;border-radius:50%;border:0;background:var(--surface,#fff);color:var(--ink,#111);font-size:1.3rem;line-height:1;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.3)}
@media(max-width:560px){#wa-photo-view:not(#palette):not(#new-card){inset:0;width:100%;max-width:100%;height:100dvh;max-height:100dvh;margin:0;padding:0;border-radius:0;background:rgba(0,0,0,.92)}
 #wa-photo-view[open]:not(#palette):not(#new-card){display:flex;align-items:center;justify-content:center}#wa-photo-view img{max-width:100vw;max-height:84dvh;border-radius:0}#wa-photo-view .wa-photo-close{top:calc(env(safe-area-inset-top,0px) + 10px);right:12px}}
`}));
const PHOTO_DATA=/^data:image\/(?:jpeg|png|webp);base64,[A-Za-z0-9+/]+=*$/;
const photoSrc=p=>PHOTO_DATA.test(p?.src||'')?p.src:/^wp_[0-9a-f]{20}$/.test(p?.id||'')?'api/whatsapp-photo?id='+p.id:'';
const photoThumb=p=>{const u=photoSrc(p);return u?html`<button type="button" class="wa-photo" data-photo="${u}" data-alt="${p.alt||''}" aria-label="${t('Open the photo')}"><img src="${u}" alt="${p.alt||t('Photo')}" loading="lazy" decoding="async"></button>`:''};
const photoThumbs=list=>(list||[]).some(photoSrc)?html`<div class="wa-photos">${list.slice(0,4).map(photoThumb)}</div>`:'';
function openPhoto(u,alt){let d=$('#wa-photo-view');
 if(!d){d=Object.assign(document.createElement('dialog'),{id:'wa-photo-view'});d.setAttribute('aria-label',t('Photo'));document.body.append(d);
  d.addEventListener('click',e=>{if(e.target===d||e.target.closest('[data-photo-close]'))d.close()})}
 if(!PHOTO_DATA.test(u)&&!/^api\/whatsapp-photo\?id=wp_[0-9a-f]{20}$/.test(u))return;
 setHTML(d,html`<button type="button" class="wa-photo-close" data-photo-close aria-label="${t('Close the photo')}">×</button><img src="${u}" alt="${alt||t('Photo')}">`);d.showModal();d.querySelector('[data-photo-close]').focus()}
document.addEventListener('click',e=>{const b=e.target.closest?.('button.wa-photo');if(!b)return;e.preventDefault();e.stopPropagation();openPhoto(b.dataset.photo,b.dataset.alt)},true);
// The WhatsApp connection's switches, under Details like its other switches (whatsapp_images_app.whatsapp_photos_action):
// Read photos (work chats), then Also in personal chats once it is on. Plain rows: the label, the switch.
function photosRow(c){const p=c.photos;if(c.service!=='whatsapp'||!p||c.shared_by)return '';
 const row=(field,on,label,note)=>html`<label class="wa-read"><span>${t(label)}${note?html`<small>${t(note)}</small>`:''}</span><button type="button" class="lookup-switch" role="switch" aria-checked="${on?'true':'false'}" aria-label="${t(label)}" data-wa-photos="${c.id}" data-field="${field}"></button></label>`;
 return html`<div class="wa-reads">${row('read',p.read,'Read photos','Reads receipts, screenshots and documents in work chats.')}${p.read?row('personal',p.personal,'Also in personal chats',''):''}</div>`}
document.addEventListener('click',async e=>{const b=e.target.closest?.('[data-wa-photos]');if(!b||b.disabled)return;
 const c=(state.connectors||[]).find(x=>x.id===b.dataset.waPhotos),p={...(c?.photos||{})};p[b.dataset.field]=b.getAttribute('aria-checked')!=='true';if(!p.read)p.personal=false;
 b.disabled=true;try{const r=await connectPost('whatsapp_photos',{account:b.dataset.waPhotos,read:!!p.read,personal:!!p.personal});if(c)c.photos=r.result||r;b.setAttribute('aria-checked',p[b.dataset.field]?'true':'false');toast(t('Saved'));setTimeout(refresh,300)}
 catch(err){errCaught(err);toast(err.message,true)}finally{b.disabled=false}});
