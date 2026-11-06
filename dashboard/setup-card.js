// The setup to-do at the top of To-dos, "Get more out of The Machine": one small card with a row per step, in this order:
// the phone app, notifications, WhatsApp, the app on this computer, another mail account, more connections, then what
// setup left out once it is relevant (state.setup_hints). At most SETUP_MAX rows; each has one button that does the step
// itself, ticks off once done, and closes for good with its × (setup_dismiss, kept on the Machine so every device
// agrees); the card's own × closes all of it. A row shows only where it applies: no phone app inside it, no
// notifications where this browser can't have them, no installing on a phone or in Firefox, WhatsApp and another
// account only on a hosted Machine (their sign-in runs there). From the first visit, once the first look is done; never
// in a frame, except the site's demo (setup_card.demo: fixed rows, buttons that do nothing).
// Loaded before settings-device.js, whose deviceRender() draws it (setupRender).
const SETUP_MAX=5;
const SETUP_ICON={
 phone:'<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>',
 push:'<path d="M6.5 16.5V11a5.5 5.5 0 0 1 11 0v5.5l1.5 2h-14z"/><path d="M10.2 20.5a2 2 0 0 0 3.6 0"/>',
 whatsapp:'<path d="M4.5 19.5l1.2-3.6a7.8 7.8 0 1 1 2.6 2.5z"/><path d="M9.5 9.2c.2 2.4 2.6 4.9 5.2 5.3l1-1.2-1.6-.9-.8.7c-1-.4-1.9-1.3-2.3-2.3l.7-.8-.9-1.6z"/>',
 install:'<rect x="3" y="4" width="18" height="12.5" rx="2"/><path d="M8.5 20h7M12 16.5V20"/>',
 account:'<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="m3.5 7.5 8.5 6 8.5-6"/>',
 connect:'<path d="M9 3v4.5M15 3v4.5M7 7.5h10V11a5 5 0 0 1-10 0z"/><path d="M12 16v5"/>',
 hint:'<path d="M12 3.5v3M12 17.5v3M3.5 12h3M17.5 12h3M6 6l2 2M16 16l2 2M6 18l2-2M16 8l2-2"/>',
 done:'<circle cx="12" cy="12" r="9"/><path d="m8 12.3 2.8 2.8L16.2 9.6"/>'};
const setupSvg=k=>raw(`<svg class="setup-ic" viewBox="0 0 24 24" aria-hidden="true">${SETUP_ICON[k]||SETUP_ICON.hint}</svg>`);
// Store marks (simple-icons, CC0)
const STORE_APPLE='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg>';
const STORE_PLAY='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22.018 13.298l-3.919 2.218-3.515-3.493 3.543-3.521 3.891 2.202a1.49 1.49 0 0 1 0 2.594zM1.337.924a1.486 1.486 0 0 0-.112.568v21.017c0 .217.045.419.124.6l11.155-11.087L1.337.924zm12.207 10.065l3.258-3.238L3.45.195a1.466 1.466 0 0 0-.946-.179l11.04 10.973zm0 2.067l-11 10.933c.298.036.612-.016.906-.183l13.324-7.54-3.23-3.21z"/></svg>';
let setupQR=false;  // the phone row's QR code, open on a computer
// The phone's own store on a phone's browser; null where there is none (a phone that is neither iPhone nor Android)
const setupStore=()=>{const p=state?.phone_app_store||{},u=DEV.ios?p.ios:DEV.android?p.android:'';return /^https:\/\//.test(u||'')?u:null};
// [{id, done, hint?}] in order, the rows that apply here and aren't closed
function setupRows(){const s=state?.setup_card;if(!s)return [];
 if(s.demo)return (s.rows||[]).filter(r=>SETUP_ICON[r?.id]).slice(0,SETUP_MAX).map(r=>({id:r.id,done:!!r.done}));
 const closed=new Set(s.dismissed||[]),hosted=!!state.manage_url,p=state.phone_app_store,rows=[];
 const add=(id,applies,done,hint)=>{if(applies&&!closed.has(id))rows.push({id,done:!!done,...(hint?{hint}:{})})};
 add('phone',!!p&&!DEV.phoneApp&&(DEV.mobile?!!setupStore():!!(p.ios||p.android)),s.phones>0);
 add('push',!DEV.phoneApp&&(pushOn()||pushOK&&devicePush.checked&&devicePush.perm!=='denied'&&devStore.get('push-off')!=='1'),pushOn());
 add('whatsapp',hosted,s.whatsapp);
 add('install',!DEV.mobile&&!DEV.phoneApp&&nudgeable&&(appInstalled()||!!installEvt||DEV.chromium||DEV.macSafari),appInstalled());
 add('account',hosted,s.mail_accounts>=2);
 add('connect',true,s.more);
 for(const h of state.setup_hints||[])if(h?.id&&/^[a-z0-9-]{1,40}$/.test(h.id))add('hint-'+h.id,true,false,h);
 return rows.slice(0,SETUP_MAX)}
const setupLabel=r=>r.hint?r.hint.title:r.id==='account'?(state.setup_card?.add==='microsoft'?'Add another Microsoft account':'Add another Google account'):
 {phone:'Get the phone app',push:'Turn on notifications',whatsapp:'Connect WhatsApp',install:'Install on this computer',connect:'Add more connections'}[r.id];
const setupButton=r=>r.hint?r.hint.button||'Open':{phone:'Get it',push:'Turn on',whatsapp:'Connect',install:'Install',account:'Add',connect:'Browse'}[r.id];
// On a computer: a QR code that opens the right store on the phone (one, or one per store before the redirect is live)
function setupQRHTML(){const p=state?.phone_app_store||{},rows=v=>Array.isArray(v)?v.filter(r=>/^[01]+$/.test(r)):[];
 const badge=(u,mark,name)=>/^https:\/\//.test(u||'')?html`<a class="store-badge" href="${safeHref(u)}" target="_blank" rel="noopener">${raw(mark)}<span>${name}</span></a>`:'';
 const ios=badge(p.ios,STORE_APPLE,'App Store'),android=badge(p.android,STORE_PLAY,'Google Play');
 const each=[[p.qr_ios,ios],[p.qr_android,android]].filter(([q,b])=>rows(q).length&&b);
 const codes=rows(p.qr).length?html`<div class="setup-codes">${qrSvg(rows(p.qr))}<div class="setup-badges">${ios}${android}</div></div>`:
  each.length?html`<div class="setup-codes">${each.map(([q,b])=>html`<div class="setup-code">${qrSvg(rows(q))}${b}</div>`)}</div>`:'';
 // no code at all (a Machine from before): the two store links alone
 return html`<div class="setup-qr">${codes||html`<div class="setup-codes">${ios}${android}</div>`}${codes?html`<small>Scan with your phone’s camera.</small>`:''}</div>`}
function setupHTML(rows){const done=rows.filter(r=>r.done).length,desk=!DEV.mobile;
 return html`<div class="setup-head"><strong>Get more out of The Machine</strong><span class="setup-count">${t('{} of {} done',done,rows.length)}</span><button type="button" class="setup-x" data-setup-close aria-label="Close" title="Close"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7L7 17"/></svg></button></div><ul class="setup-rows">${
  rows.map(r=>html`<li class="setup-row${r.done?' done':''}" data-step="${r.id}">${setupSvg(r.done?'done':r.hint?'hint':r.id)}<span class="setup-label">${setupLabel(r)}</span>${r.done?'':html`<button type="button" class="setup-go" data-setup-go="${r.id}"${r.id==='phone'&&desk?html` aria-expanded="${setupQR}"`:''}>${setupButton(r)}</button><button type="button" class="setup-x" data-setup-dismiss="${r.id}" aria-label="Dismiss" title="Dismiss"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7L7 17"/></svg></button>`}${
   r.id==='phone'&&desk&&setupQR&&!r.done?setupQRHTML():''}</li>`)}</ul>`}
function setupBox(){let el=$('#setup-card');if(el)return el;
 el=document.createElement('div');el.id='setup-card';el.className='setup-card';el.setAttribute('role','region');el.setAttribute('aria-label','Get more out of The Machine');el.hidden=true;
 const nudge=$('#device-nudge');if(nudge)nudge.after(el);else $('#inbox').prepend(el);
 el.addEventListener('click',setupClick);return el}
function setupRender(){const s=state?.setup_card,el=setupBox();
 const rows=!s||s.closed||settingUp()||(DEV.framed&&!s.demo)?[]:setupRows();
 const show=rows.some(r=>!r.done),h=show?String(setupHTML(rows)):'';
 if(el.dataset.html!==h){setHTML(el,show?raw(h):html``);el.dataset.html=h}el.hidden=!show}
async function setupDismiss(step){const s=state.setup_card;if(step==='card')s.closed=true;else s.dismissed=[...new Set([...(s.dismissed||[]),step])];setupRender();
 if(s.demo)return;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'setup_dismiss',args:{step}})});
  if(r?.setup_card)state.setup_card=r.setup_card}catch(e){errCaught(e);toast(e.message,true)}setupRender()}
async function setupClick(e){const b=e.target.closest('button');if(!b)return;const s=state?.setup_card;if(!s)return;
 if(b.matches('[data-setup-close]'))return setupDismiss('card');
 if(b.matches('[data-setup-dismiss]'))return setupDismiss(b.dataset.setupDismiss);
 const step=b.dataset.setupGo;if(!step)return;
 if(step==='phone'&&!DEV.mobile){setupQR=!setupQR;setupRender();return}  // the QR code opens right in the row
 if(s.demo)return;  // the site's demo: nothing happens
 const row=setupRows().find(r=>r.id===step),hint=row?.hint;
 if(hint){const u=String(hint.href||'');if(/^https:\/\//.test(u))window.open(u,'_blank','noopener');else if(/^#connect(?:=[a-z_]+|ions=add)$/.test(u))location.hash=u;return}
 if(step==='phone'){const u=setupStore();if(u)window.open(u,'_blank','noopener');return}
 if(step==='whatsapp'){location.hash='#connect=whatsapp';return}
 if(step==='account'){location.hash='#connect='+(s.add==='microsoft'?'microsoft':'google');return}
 if(step==='connect'){location.hash='#connections=add';return}
 b.disabled=true;
 try{if(step==='push')await pushEnable();else if(step==='install'){if(installEvt)await appInstall();else toast(DEV.macSafari?'In Safari’s menu bar: File, then Add to Dock.':'Find Install in the browser’s menu.')}}
 finally{b.disabled=false;setupRender()}}
