// This device: notifications on and the app installed. A quiet nudge at the top of Suggestions (one at a time, in order:
// notifications, the app, the phone app, what setup left out) and the controls in Settings, General, This device. Every browser prompt comes from the owner's own tap, and a
// page in a frame (the site's demo) or without a service worker never shows a nudge.
const pushOK='serviceWorker' in navigator&&'PushManager' in window&&'Notification' in window;
// iPhone/iPad: Web Push exists only in the Home Screen app (iOS 16.4+), never in a Safari tab.
const iosTab=/iPhone|iPad|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
const iosHint='On iPhone and iPad: tap Share, then Add to Home Screen. Open The Machine from there to turn on notifications.';
const keyBytes=k=>Uint8Array.from(atob(k.replace(/-/g,'+').replace(/_/g,'/')+'='.repeat((4-k.length%4)%4)),c=>c.charCodeAt(0));
const pushPost=(action,sub)=>{const j=sub.toJSON();return request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args:{endpoint:j.endpoint,keys:j.keys}})})};
const devStore={get:k=>{try{return localStorage.getItem(k)}catch{return null}},set:(k,v)=>{try{if(v==null)localStorage.removeItem(k);else localStorage.setItem(k,v)}catch{}}};
const DEV=(()=>{const ua=navigator.userAgent;let framed=true;try{framed=window.top!==window}catch{}
 return {phoneApp:/ TheMachineApp\//.test(ua),ios:iosTab,android:/Android/.test(ua),mobile:iosTab||/Android|Mobi/.test(ua),framed,chromium:'onbeforeinstallprompt' in window,
  macSafari:!iosTab&&/Macintosh/.test(ua)&&/Version\/(1[7-9]|[2-9]\d)\b.*Safari/.test(ua)&&!/Chrome|Chromium|CriOS|Edg|Firefox|FxiOS|OPR/.test(ua)}})();
const nudgeable=!DEV.framed&&'serviceWorker' in navigator;
const inApp=()=>['standalone','fullscreen','window-controls-overlay'].some(m=>matchMedia(`(display-mode: ${m})`).matches)||navigator.standalone===true;
let installEvt=null,relatedInstalled=false,justInstalled=false;
const appInstalled=()=>inApp()||relatedInstalled||devStore.get('app-installed')==='1';
// What installing looks like here: the browser's own prompt (Chromium), steps (iPhone, Safari on a Mac), or nothing (Firefox).
function installKind(){if(!nudgeable)return null;if(installEvt)return DEV.mobile?'android':'desktop';if(appInstalled())return null;return DEV.ios?'ios':DEV.macSafari?'mac':null}
addEventListener('beforeinstallprompt',e=>{e.preventDefault();installEvt=e;deviceRender()});
// Installed (from the nudge, Settings or the browser's own menu): a small Installed in the card's place, or a toast.
let installedNoted=false;
function noteInstalled(){installEvt=null;devStore.set('app-installed','1');if(installedNoted)return deviceRender();installedNoted=true;
 if(['desktop','android'].includes(nudgeBox.dataset.kind)){justInstalled=true;setTimeout(()=>{justInstalled=false;deviceRender()},8000)}else toast('Installed. The Machine is in your apps now.');deviceRender()}
addEventListener('appinstalled',noteInstalled);
if(nudgeable&&navigator.getInstalledRelatedApps)navigator.getInstalledRelatedApps().then(a=>{relatedInstalled=a.length>0;deviceRender()}).catch(()=>{});
async function appInstall(){const e=installEvt;if(!e){toast(DEV.ios?iosHint:'Find Install in the browser’s menu.');return}
 e.prompt();let outcome='dismissed';try{({outcome}=await e.userChoice)}catch{}if(outcome==='accepted')noteInstalled();else{installEvt=null;deviceRender()}return outcome==='accepted'}
// Notifications: the browser's permission and this device's subscription. Off in Settings stays off: no nudge after it.
const devicePush={perm:pushOK?Notification.permission:'unsupported',sub:null,checked:false};
const pushOn=()=>devicePush.perm==='granted'&&!!devicePush.sub;
const pushWanted=()=>pushOK&&devicePush.checked&&devStore.get('push-off')!=='1'&&(devicePush.perm==='default'||(devicePush.perm==='granted'&&!devicePush.sub));
async function pushCheck(sync=false){if(!pushOK)return deviceRender();try{const reg=await navigator.serviceWorker.register('sw.js');devicePush.sub=await reg.pushManager.getSubscription();devicePush.perm=Notification.permission;
 if(pushOn()&&sync)await pushPost('push_subscribe',devicePush.sub)}catch{}devicePush.checked=true;deviceRender()}
const blockedHint=()=>DEV.ios?'In the Settings app: Notifications, The Machine.':DEV.macSafari?'In Safari: Settings, Websites, Notifications.':DEV.mobile?'Tap the icon left of the address, then Permissions, Notifications.':'Click the icon left of the address, then allow Notifications.';
async function pushEnable(){if(!pushOK){toast(DEV.ios?iosHint:'This browser can’t show notifications.',true);return false}
 // The permission prompt first, while the tap still counts (Safari asks for that).
 const perm=await Notification.requestPermission();devicePush.perm=perm;
 if(perm!=='granted'){deviceRender();toast(perm==='denied'?t('Notifications are blocked.')+' '+blockedHint():'Notifications stay off for now.',perm==='denied');return false}
 try{const reg=await navigator.serviceWorker.register('sw.js');let sub=await reg.pushManager.getSubscription();
  if(!sub){const {key}=await request('api/push-key');sub=await reg.pushManager.subscribe({userVisibleOnly:true,applicationServerKey:keyBytes(key)})}
  await pushPost('push_subscribe',sub);devicePush.sub=sub;devStore.set('push-off',null)}catch(e){errCaught(e);toast(e.message,true);return false}finally{deviceRender()}
 await pushTest('Notifications on. A test is on its way.');return true}
async function pushDisable(){try{const reg=await navigator.serviceWorker.register('sw.js'),sub=await reg.pushManager.getSubscription();if(sub){await pushPost('push_unsubscribe',sub);await sub.unsubscribe()}
 devicePush.sub=null;devStore.set('push-off','1');toast('Notifications off')}catch(e){errCaught(e);toast(e.message,true)}finally{deviceRender()}}
async function pushTest(done='Test sent. It shows up in a moment.'){if(!pushOn()){toast('Turn on notifications first.',true);return false}
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'push_test',args:{endpoint:devicePush.sub.toJSON().endpoint}})});toast(done);return true}
 catch(e){errCaught(e);toast(e.message,true);return false}}
// The device actions in one place, for a command palette or anything else that lists actions.
const DEVICE_ACTIONS=window.deviceActions=[
 {id:'install-app',label:'Install app',available:()=>!!installEvt||(!appInstalled()&&(DEV.ios||DEV.macSafari)),run:appInstall},
 {id:'push-on',label:'Turn on notifications',available:()=>pushOK&&!pushOn()&&devicePush.perm!=='denied',run:pushEnable},
 {id:'push-test',label:'Send test notification',available:pushOn,run:()=>pushTest()}];
const deviceRun=id=>DEVICE_ACTIONS.find(a=>a.id===id)?.run();
// Calm: nothing before the owner handled a first to-do (state.handled_first), in the first minute of a session or while
// setting up; Not now waits 14 days, a second Not now stops it on this device, and after any Not now the next nudge waits
// a day. The order: 1 notifications, 2 the app on this computer, 3 the phone app (state.phone_app_store, only once it is
// published; on a phone's browser it takes the place of 2), 4 what setup left out, once it is relevant
// (state.setup_hints, hosted only: more sources, Telegram, Codex), linked to its step. Done on this device: skipped.
const NUDGE_WAIT=14*864e5,NUDGE_REST=864e5;
const sessionStart=(()=>{const now=Date.now();try{const s=+sessionStorage.getItem('device-session');if(s&&s<=now)return s;sessionStorage.setItem('device-session',String(now))}catch{}return now})();
const nudgeState=k=>{try{return JSON.parse(devStore.get('nudge-'+k))||{}}catch{return {}}};
const nudgeQuiet=k=>{const v=nudgeState(k);return !!v.stop||(v.until||0)>Date.now()};
function nudgeLater(k){const v=nudgeState(k),n=(v.n||0)+1;devStore.set('nudge-'+k,JSON.stringify(n>=2?{n,stop:true}:{n,until:Date.now()+NUDGE_WAIT}));devStore.set('nudge-rest',String(Date.now()+NUDGE_REST));deviceRender()}
const settingUp=()=>!state?.suggestions||!(state.connectors||[]).length||!!firstLookInfo(state.review_live||{});
// The phone app: on a phone's browser, its store; on a computer, the page with both until a phone has it. Never in the
// app itself, nor on a phone where The Machine runs as an installed web app already.
function phoneKind(){const p=state?.phone_app_store;if(!p||DEV.phoneApp)return null;
 if(DEV.mobile)return inApp()||appInstalled()?null:(DEV.ios?p.ios:DEV.android?p.android:null)?'phone':null;return p.page&&!p.phones?'phone-desk':null}
const phoneLink=k=>{const p=state?.phone_app_store||{},u=k==='phone'?(DEV.ios?p.ios:p.android):p.page;return /^https:\/\//.test(u||'')?u:null};
function nudgeKind(){if(!nudgeable)return null;if(justInstalled)return 'installed';
 if(!state?.handled_first||Date.now()-sessionStart<6e4||settingUp()||+devStore.get('nudge-rest')>Date.now())return null;
 if(pushWanted()&&!nudgeQuiet('push'))return 'push';
 const ph=phoneKind(),phone=ph&&!nudgeQuiet('phone')?ph:null;
 if(!(DEV.mobile&&ph)){const k=installKind();if(k&&!nudgeQuiet('install'))return k}
 if(phone)return phone;
 const h=(state.setup_hints||[]).find(h=>h&&h.id&&!nudgeQuiet('hint-'+h.id));return h?'hint:'+h.id:null}
const hintOf=k=>String(k).startsWith('hint:')?(state.setup_hints||[]).find(h=>'hint:'+h.id===k):null;
const nudgeKey=k=>String(k).startsWith('hint:')?'hint-'+k.slice(5):k==='push'?'push':String(k).startsWith('phone')?'phone':'install';
const NUDGE_ICON='<img class="nudge-icon" src="brand/app-icon-192.png" alt="" width="36" height="36">';
const SHARE_ICON='<svg class="ios-share" viewBox="0 0 24 24" role="img" aria-label="Share"><path d="M12 14V3.5M8.2 7.2 12 3.4l3.8 3.8"/><path d="M8.5 10H7a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2h-1.5"/></svg>';
function nudgeHTML(k){const later=html`<button type="button" class="ghost" data-nudge-later>Not now</button>`,text=(t,s)=>html`${raw(NUDGE_ICON)}<div class="nudge-text"><strong>${t}</strong>${s}</div>`;
 if(k==='installed')return text('Installed',html`<span>The Machine is in your apps now.</span>`);
 const hint=hintOf(k);if(hint)return html`${text(hint.title,html`<span>${hint.text}</span>`)}<div class="nudge-act"><button type="button" class="primary" data-hint-open>${hint.button||'Open'}</button>${later}</div>`;
 if(k==='phone'||k==='phone-desk')return html`${text(k==='phone'?'Get the phone app':'Get The Machine on your phone',k==='phone'?html`<span>Notifications, and sharing from any app.</span>`:html`<span>For iPhone and Android, with notifications.</span>`)}<div class="nudge-act"><button type="button" class="primary" data-phone-open>Get the app</button>${later}</div>`;
 if(k==='desktop'||k==='android')return html`${text('Install The Machine',k==='desktop'?html`<span>Install it and pin it to your taskbar or dock.</span>`:html`<span>Add it to your home screen. It opens like an app.</span>`)}<div class="nudge-act"><button type="button" class="primary" data-device="install-app">Install</button>${later}</div>`;
 if(k==='ios')return html`${text('Add The Machine to your Home Screen',html`<ol class="nudge-steps"><li>Tap Share ${raw(SHARE_ICON)}</li><li>Tap Add to Home Screen</li></ol><span>Notifications on iPhone and iPad work only from there.</span>`)}<div class="nudge-act">${later}</div>`;
 if(k==='mac')return html`${text('Add The Machine to your Dock',html`<span>In Safari’s menu bar: File, then Add to Dock.</span>`)}<div class="nudge-act">${later}</div>`;
 return html`${text('Turn on notifications',html`<span>A ping when a to-do needs you, on this device only.</span>`)}<div class="nudge-act"><button type="button" class="primary" data-device="push-on">Turn on</button>${later}</div>`}
const nudgeBox=(()=>{const el=document.createElement('div');el.id='device-nudge';el.className='notice-card device-nudge';el.setAttribute('role','region');el.setAttribute('aria-label','This device');el.hidden=true;el.dataset.kind='';
 $('#inbox').prepend(el);el.onclick=async e=>{const b=e.target.closest('button');if(!b)return;const k=el.dataset.kind;
  if(b.matches('[data-nudge-later]')){nudgeLater(nudgeKey(k));return}
  // a setup hint opens its step on the setup page; it rests a day, and goes for good once that step is done
  // the phone app opens its store (or the page with both) and rests the same way
  if(b.matches('[data-hint-open],[data-phone-open]')){const h=hintOf(k),u=b.matches('[data-phone-open]')?phoneLink(k):h?.href;if(u&&/^https:\/\//.test(u))window.open(u,'_blank','noopener');else if(h&&/^#connect(?:=[a-z_]+|ions=add)$/.test(u))location.hash=u;devStore.set('nudge-'+nudgeKey(k),JSON.stringify({...nudgeState(nudgeKey(k)),until:Date.now()+NUDGE_REST}));devStore.set('nudge-rest',String(Date.now()+NUDGE_REST));deviceRender();return}
  // A closed prompt counts as Not now, so it doesn't come straight back.
  b.disabled=true;try{const ok=await deviceRun(b.dataset.device);if(!ok&&(k==='push'?devicePush.perm==='default':true))nudgeLater(k==='push'?'push':'install')}finally{b.disabled=false;deviceRender()}};return el})();
// Settings, General, This device: App, Notifications (with Send a test), Light mode.
const deviceRows=(()=>{const theme=$('#theme-toggle').closest('.settings-list>div'),list=theme.parentElement,pushRow=$('#push-toggle').closest('.settings-list>div');
 const app=document.createElement('div');app.id='device-app';app.innerHTML='<span class="grow"><strong>App</strong><small></small></span><span class="device-act"></span>';
 pushRow.id='device-push';pushRow.querySelector('strong').textContent='Notifications';
 const test=document.createElement('button');test.type='button';test.className='ghost';test.id='push-test';test.textContent='Send a test';test.hidden=true;$('#push-toggle').before(test);
 test.onclick=async()=>{test.disabled=true;try{await pushTest()}finally{test.disabled=false}};
 list.prepend(app);list.insertBefore(pushRow,theme);return {app,push:pushRow}})();
// The help article for both rows (docs/help/phone-app.md on themachine.computer/help).
const DEVICE_HELP=' <a class="learn" href="https://themachine.computer/help/phone-app" target="_blank" rel="noopener">Learn more</a>';
function deviceSettings(){const {app}=deviceRows,small=app.querySelector('small'),act=app.querySelector('.device-act'),set=(el,html)=>{if(el.dataset.html!==html){el.innerHTML=html;el.dataset.html=html}};
 app.hidden=!nudgeable;
 if(installEvt){set(small,(DEV.mobile?'Opens like an app, from your home screen.':'Pin it to your taskbar or dock.')+DEVICE_HELP);set(act,'<button type="button" data-device="install-app">Install app</button>')}
 else if(appInstalled()){set(small,'Installed on this device.'+DEVICE_HELP);set(act,'<span class="device-done">Installed</span>')}
 else{set(small,(DEV.ios?`Tap Share ${SHARE_ICON}, then Add to Home Screen.`:DEV.macSafari?'In Safari’s menu bar: File, then Add to Dock.':DEV.chromium?'Find Install in the browser’s menu, or the icon in the address bar.':'This browser can’t install apps. Chrome, Edge and Safari can.')+DEVICE_HELP);set(act,'')}
 const b=$('#push-toggle'),note=deviceRows.push.querySelector('small'),on=pushOn(),blocked=pushOK&&devicePush.perm==='denied';
 b.hidden=!(pushOK?!blocked:iosTab&&!navigator.standalone);b.title=!pushOK?iosHint:on?'Notifications on':'Turn on notifications';b.setAttribute('aria-pressed',String(on));
 $('#push-test').hidden=!on;
 const text=!pushOK?(iosTab?'On iPhone and iPad, add it to your Home Screen first: Share, then Add to Home Screen.':'This browser can’t show notifications.'):blocked?t('Blocked in this browser.')+' '+blockedHint():on?'On for this device. One per to-do, even without Telegram.':'One per to-do, even without Telegram.';
 set(note,esc(text)+DEVICE_HELP);note.classList.toggle('device-blocked',blocked)}
function deviceRender(){const k=nudgeKind()||'',el=nudgeBox;if(el.dataset.kind!==k){el.dataset.kind=k;setHTML(el,k?nudgeHTML(k):html``);el.hidden=!k}deviceSettings();renderNotify();phoneAppRender()}
// Settings, General, Phone app: how the mobile app finds this Machine (phone_app in assistant.py). Hosted or on The
// Machine Network: it signs in with the account. Self-hosted and not on the Network: the same line, and folded under
// "Not on the Network?" a QR code of the app's connect link and the address to type in. Not shown in the app itself,
// which says once when its notifications can't work (off The Machine Network).
// The mobile app's push on this phone: {id} once the app handed the Machine its token (www/inject.js), {id:null}
// before that, null outside the app
// In the app: whether the phone will still ask about notifications (machinePhone, mobile/www/inject.js); checked again
// when the owner comes back (from the phone's settings)
let phonePush='';
async function phonePushCheck(){const p=window.machinePhone;if(!p)return;let s='';try{s=await p.state('push')}catch{}if(s!==phonePush){phonePush=s;renderNotify()}}
function phoneAppPush(){if(!document.documentElement.classList.contains('in-app'))return null;
 try{const k=JSON.parse(localStorage.getItem('machine-app-push')||'null');return {id:typeof k?.id==='string'?k.id:null}}catch{return {id:null}}}
function phoneAppRender(){const p=state?.notify?.phone_app,inApp=document.documentElement.classList.contains('in-app');let row=$('#device-phone');
 if(inApp&&state?.notify&&!state.notify.app_push_ready&&!devStore.get('app-push-network')){devStore.set('app-push-network',1);toast(t('Notifications in the app need The Machine Network. The app works without them.'))}
 const html=!p||inApp||!(p.hosted||p.url)?'':p.hosted?`<span class="grow"><strong>Phone app</strong><small>${esc(t('The app signs in with your account.'))}</small></span>`:
  `<span class="grow"><strong>Phone app</strong><small>${esc(t('The app signs in with your account on The Machine Network.'))}</small><details class="connect-alt phone-own"><summary>${esc(t('Not on the Network?'))}</summary><small>${esc(t('Install the app, then scan this with the phone’s camera.'))}</small>${p.qr?.length?qrSvg(p.qr):''}<small>${t('Or enter this address in the app: {}','<code class="phone-url">'+esc(p.url)+'</code>')}</small></details></span>`;
 if(!html){row?.remove();return}  // only there when there is something to show
 if(!row){row=document.createElement('div');row.id='device-phone';deviceRows.app.after(row)}
 if(row.dataset.html!==html){row.innerHTML=html;row.dataset.html=html}}
deviceRows.app.onclick=e=>{const b=e.target.closest('[data-device]');if(b)deviceRun(b.dataset.device)};
$('#push-toggle').onclick=async()=>{const b=$('#push-toggle');if(!pushOK){toast(iosHint);return}b.disabled=true;try{if(pushOn())await pushDisable();else await pushEnable()}finally{b.disabled=false}};
setTimeout(deviceRender,Math.max(0,sessionStart+6e4-Date.now())+50);
document.addEventListener('visibilitychange',()=>{if(!document.hidden){pushCheck();phonePushCheck()}});
addEventListener('machinephone',()=>{phonePush='';renderNotify()});  // the app's part came in after this page drew
pushCheck(true);
// A notification opens its link in this page: only the part after # changes, so nothing reloads
if(pushOK)navigator.serviceWorker.addEventListener('message',e=>{if(!e.data?.open)return;const u=new URL(e.data.open,location.href);
 if(u.origin!==location.origin||u.pathname!==location.pathname||u.search!==location.search){location.href=u.href;return}if(u.hash!==location.hash)location.hash=u.hash;else dispatchEvent(new HashChangeEvent('hashchange'))});
// Settings, Notifications (notify.py): each kind by channel, this device, the digest time and quiet hours. The app
// icon's badge counts the to-dos that need the owner. While this page is in front of them, it tells the Machine so no
// push goes out (a heartbeat a minute; the Machine forgets it after two).
const NOTIFY_KINDS=[['todo','New to-dos','A reply, a request, anything urgent'],['result','Results and questions','Ready to approve, stuck, a Fleet question'],
 ['reminder','Reminders','Snoozes and waits coming back'],['digest','Morning digest','Meetings, what’s due, what came in overnight']];
const NOTIFY_COLS={push:'Push',telegram:'Telegram',email:'Email'};
const notifyPost=(action,args={})=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
const notifyHM=t=>{try{return fmtHM('2000-01-01T'+t)}catch{return t}};
function renderNotify(){const n=state?.notify,box=$('#settings-notify');
 const waiting=(state?.suggestions||[]).filter(x=>['pending','prepared'].includes(x.status)).length;
 try{if(navigator.setAppBadge){if(waiting)navigator.setAppBadge(waiting).catch(()=>{});else navigator.clearAppBadge().catch(()=>{})}}catch{}
 if(!box||!n){if(box)box.hidden=true;return}box.hidden=false;
 const cols=['push',...(n.telegram?['telegram']:[]),...(n.email?['email']:[])],grid=$('#notify-grid');
 grid.style.setProperty('--notify-cols',cols.length);
 // the digest row's line: its time (set in Work hours below) and Preview, shown on the page, nothing sent
 const h=state.hours||{},digest=`<span>Work days at ${esc(notifyHM(h.digest_at||n.digest_at||'08:30'))}</span><span aria-hidden="true"> · </span><button type="button" class="notify-link" data-notify-preview>${$('#notify-preview').hidden?'Preview':'Hide preview'}</button>`;
 const cell=(kind,label,ch)=>{const p=n.prefs[kind]||{};if(!(ch in p))return `<span class="notify-cell" role="cell"><span class="notify-na">–</span></span>`;
  return `<span class="notify-cell" role="cell"><button type="button" class="lookup-switch" role="switch" aria-checked="${!!p[ch]}" aria-label="${esc(label+': '+NOTIFY_COLS[ch])}" data-notify-kind="${kind}" data-notify-channel="${ch}"></button></span>`};
 const html=`<div class="notify-row" role="row"><span role="columnheader"></span>${cols.map(c=>`<span class="notify-col" role="columnheader">${NOTIFY_COLS[c]}</span>`).join('')}</div>`+
  NOTIFY_KINDS.map(([k,label,hint])=>`<div class="notify-row" role="row"><span role="rowheader"><strong>${label}</strong><small>${k==='digest'?digest:hint}</small></span>${cols.map(c=>cell(k,label,c)).join('')}</div>`).join('');
 if(grid.dataset.html!==html){grid.innerHTML=html;grid.dataset.html=html}
 // In the mobile app this device is the phone: its own push (www/inject.js keeps the id app_push_register gave it),
 // not the web's, which a WebView doesn't have. It turns on with the phone's notifications for the app.
 const phone=phoneAppPush(),mine=phone&&(n.app_devices||[]).find(p=>p.id===phone.id);
 const on=phone?!!mine:pushOn(),can=!phone&&pushOK&&devicePush.perm!=='denied';
 // The app: Turn on asks the phone; once it won't ask again, Open settings (the app's page there). An app from before: a line
 const app=phone&&n.app_push_ready?(!window.machinePhone?(mine?'':'old'):phonePush==='blocked'?'blocked':mine&&phonePush!=='prompt'?'':'off'):'';
 if(phone&&window.machinePhone&&!phonePush)phonePushCheck();
 const device=phone?(app==='blocked'?'Notifications are off for The Machine.':app==='off'?'Push is off here.':mine?'Push is on here.':!n.app_push_ready?'Notifications in the app need The Machine Network. The app works without them.':app==='off'?'Push is off here.':'To get notifications, allow them for The Machine in the phone’s settings.')
  :on?'Push is on here.':!can?'This browser can’t show push here.':n.push_devices?t(['Push is off here, on for {} other device.','Push is off here, on for {} other devices.'],n.push_devices):'Push is off here.';
 // Phones with the mobile app (notify.py, app_push): each with Remove, which stops its notifications
 const phones=(n.app_devices||[]).filter(p=>p!==mine).map(p=>`<div><span class="grow"><strong>${esc(p.label)}</strong><small>Phone with the app</small></span><button type="button" data-app-remove="${esc(p.id)}">Remove</button></div>`).join('');
 const more=`<div><span class="grow"><strong>This device</strong><small>${esc(device)}</small></span>${mine&&!app?`<button type="button" class="ghost" data-app-test="${esc(mine.id)}">Send a test</button>`:''}${!on&&can?'<button type="button" data-device="push-on">Turn on</button>':''}${app==='blocked'?'<button type="button" data-app-settings>Open settings</button>':app==='off'?'<button type="button" data-app-on>Turn on</button>':''}</div>`+phones;
 const m=$('#notify-more');if(m.dataset.html!==more){m.innerHTML=more;m.dataset.html=more}}
$('#settings-notify').addEventListener('click',async e=>{const sw=e.target.closest('[data-notify-kind]');
 if(sw){const on=sw.getAttribute('aria-checked')!=='true';sw.disabled=true;
  try{state.notify=await notifyPost('notify_set',{kind:sw.dataset.notifyKind,channel:sw.dataset.notifyChannel,on});renderNotify()}catch(err){errCaught(err);toast(err.message,true)}finally{sw.disabled=false}return}
 const test=e.target.closest('[data-app-test]');if(test){test.disabled=true;
  try{await notifyPost('push_test',{app_device:test.dataset.appTest});toast('Test sent. It shows up in a moment.')}catch(err){errCaught(err);toast(err.message,true)}finally{test.disabled=false}return}
 if(e.target.closest('[data-app-settings]')){window.machinePhone?.settings().catch(()=>{});return}
 const ask=e.target.closest('[data-app-on]');if(ask){ask.disabled=true;
  try{const r=await window.machinePhone.pushOn();if(r==='on'){phonePush='granted';toast('Push is on here.');await refresh();renderNotify()}else if(r==='blocked'){phonePush='blocked';renderNotify()}}catch(err){errCaught(err);toast(err.message,true)}finally{ask.disabled=false}return}
 const rm=e.target.closest('[data-app-remove]');if(rm){rm.disabled=true;
  try{await notifyPost('app_push_unregister',{id:rm.dataset.appRemove});state.notify.app_devices=(state.notify.app_devices||[]).filter(p=>p.id!==rm.dataset.appRemove);state.notify.push_devices=Math.max(0,(state.notify.push_devices||1)-1);toast('Removed');renderNotify()}catch(err){errCaught(err);toast(err.message,true)}finally{rm.disabled=false}return}
 const d=e.target.closest('[data-device]');if(d){d.disabled=true;try{await deviceRun(d.dataset.device)}finally{d.disabled=false;renderNotify()}return}
 const pv=e.target.closest('[data-notify-preview]');if(pv){const out=$('#notify-preview');if(!out.hidden){out.hidden=true;renderNotify();return}pv.disabled=true;
  try{const r=await notifyPost('notify_preview');out.textContent=r.empty?'Nothing for a digest right now.':r.text;out.hidden=false;renderNotify()}catch(err){errCaught(err);toast(err.message,true)}finally{pv.disabled=false}}});
