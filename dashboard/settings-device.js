// This device: the app installed and notifications on. A quiet nudge at the top of Suggestions (one at a time, install
// first) and the controls in Settings, General, This device. Every browser prompt comes from the owner's own tap, and a
// page in a frame (the site's demo) or without a service worker never shows a nudge.
const pushOK='serviceWorker' in navigator&&'PushManager' in window&&'Notification' in window;
// iPhone/iPad: Web Push exists only in the Home Screen app (iOS 16.4+), never in a Safari tab.
const iosTab=/iPhone|iPad|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
const iosHint='On iPhone and iPad: tap Share, then Add to Home Screen. Open The Machine from there to turn on notifications.';
const keyBytes=k=>Uint8Array.from(atob(k.replace(/-/g,'+').replace(/_/g,'/')+'='.repeat((4-k.length%4)%4)),c=>c.charCodeAt(0));
const pushPost=(action,sub)=>{const j=sub.toJSON();return request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args:{endpoint:j.endpoint,keys:j.keys}})})};
const devStore={get:k=>{try{return localStorage.getItem(k)}catch{return null}},set:(k,v)=>{try{if(v==null)localStorage.removeItem(k);else localStorage.setItem(k,v)}catch{}}};
const DEV=(()=>{const ua=navigator.userAgent;let framed=true;try{framed=window.top!==window}catch{}
 return {ios:iosTab,android:/Android/.test(ua),mobile:iosTab||/Android|Mobi/.test(ua),framed,chromium:'onbeforeinstallprompt' in window,
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
// Calm: nothing in the first minute of a session or while setting up; Not now waits 14 days, a second Not now stops it on
// this device, and after any Not now the next nudge waits a day. After the device ones: what setup left out, once it
// is relevant (state.setup_hints, hosted only: a source whose mail keeps coming, Telegram, Codex), linked to its step.
const NUDGE_WAIT=14*864e5,NUDGE_REST=864e5;
const sessionStart=(()=>{const now=Date.now();try{const s=+sessionStorage.getItem('device-session');if(s&&s<=now)return s;sessionStorage.setItem('device-session',String(now))}catch{}return now})();
const nudgeState=k=>{try{return JSON.parse(devStore.get('nudge-'+k))||{}}catch{return {}}};
const nudgeQuiet=k=>{const v=nudgeState(k);return !!v.stop||(v.until||0)>Date.now()};
function nudgeLater(k){const v=nudgeState(k),n=(v.n||0)+1;devStore.set('nudge-'+k,JSON.stringify(n>=2?{n,stop:true}:{n,until:Date.now()+NUDGE_WAIT}));devStore.set('nudge-rest',String(Date.now()+NUDGE_REST));deviceRender()}
const settingUp=()=>!state?.suggestions||!(state.connectors||[]).length||!!firstLookInfo(state.review_live||{});
function nudgeKind(){if(!nudgeable)return null;if(justInstalled)return 'installed';
 if(Date.now()-sessionStart<6e4||settingUp()||+devStore.get('nudge-rest')>Date.now())return null;
 const k=installKind();if(k&&!nudgeQuiet('install'))return k;
 if(pushWanted()&&!nudgeQuiet('push'))return 'push';
 const h=(state.setup_hints||[]).find(h=>h&&h.id&&!nudgeQuiet('hint-'+h.id));return h?'hint:'+h.id:null}
const hintOf=k=>String(k).startsWith('hint:')?(state.setup_hints||[]).find(h=>'hint:'+h.id===k):null;
const nudgeKey=k=>String(k).startsWith('hint:')?'hint-'+k.slice(5):k==='push'?'push':'install';
const NUDGE_ICON='<img class="nudge-icon" src="brand/app-icon-192.png" alt="" width="36" height="36">';
const SHARE_ICON='<svg class="ios-share" viewBox="0 0 24 24" role="img" aria-label="Share"><path d="M12 14V3.5M8.2 7.2 12 3.4l3.8 3.8"/><path d="M8.5 10H7a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2h-1.5"/></svg>';
function nudgeHTML(k){const later='<button type="button" class="ghost" data-nudge-later>Not now</button>',text=(t,s)=>`${NUDGE_ICON}<div class="nudge-text"><strong>${t}</strong>${s}</div>`;
 if(k==='installed')return text('Installed','<span>The Machine is in your apps now.</span>');
 const hint=hintOf(k);if(hint)return text(esc(hint.title),`<span>${esc(hint.text)}</span>`)+`<div class="nudge-act"><button type="button" class="primary" data-hint-open>${esc(hint.button||'Open')}</button>${later}</div>`;
 if(k==='desktop'||k==='android')return text('Install The Machine',k==='desktop'?'<span>Install it and pin it to your taskbar or dock.</span>':'<span>Add it to your home screen. It opens like an app.</span>')+`<div class="nudge-act"><button type="button" class="primary" data-device="install-app">Install</button>${later}</div>`;
 if(k==='ios')return text('Add The Machine to your Home Screen',`<ol class="nudge-steps"><li>Tap Share ${SHARE_ICON}</li><li>Tap Add to Home Screen</li></ol><span>Notifications on iPhone and iPad work only from there.</span>`)+`<div class="nudge-act">${later}</div>`;
 if(k==='mac')return text('Add The Machine to your Dock','<span>In Safari’s menu bar: File, then Add to Dock.</span>')+`<div class="nudge-act">${later}</div>`;
 return text('Turn on notifications','<span>A ping when a to-do needs you, on this device only.</span>')+`<div class="nudge-act"><button type="button" class="primary" data-device="push-on">Turn on</button>${later}</div>`}
const nudgeBox=(()=>{const el=document.createElement('div');el.id='device-nudge';el.className='notice-card device-nudge';el.setAttribute('role','region');el.setAttribute('aria-label','This device');el.hidden=true;el.dataset.kind='';
 $('#inbox').prepend(el);el.onclick=async e=>{const b=e.target.closest('button');if(!b)return;const k=el.dataset.kind;
  if(b.matches('[data-nudge-later]')){nudgeLater(nudgeKey(k));return}
  // a setup hint opens its step on the setup page; it rests a day, and goes for good once that step is done
  if(b.matches('[data-hint-open]')){const h=hintOf(k);if(h&&/^https:\/\//.test(h.href))window.open(h.href,'_blank','noopener');else if(h&&/^#connect(?:=[a-z_]+|ions=add)$/.test(h.href))location.hash=h.href;devStore.set('nudge-'+nudgeKey(k),JSON.stringify({...nudgeState(nudgeKey(k)),until:Date.now()+NUDGE_REST}));devStore.set('nudge-rest',String(Date.now()+NUDGE_REST));deviceRender();return}
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
function deviceRender(){const k=nudgeKind()||'',el=nudgeBox;if(el.dataset.kind!==k){el.dataset.kind=k;el.innerHTML=k?nudgeHTML(k):'';el.hidden=!k}deviceSettings();renderNotify()}
deviceRows.app.onclick=e=>{const b=e.target.closest('[data-device]');if(b)deviceRun(b.dataset.device)};
$('#push-toggle').onclick=async()=>{const b=$('#push-toggle');if(!pushOK){toast(iosHint);return}b.disabled=true;try{if(pushOn())await pushDisable();else await pushEnable()}finally{b.disabled=false}};
setTimeout(deviceRender,Math.max(0,sessionStart+6e4-Date.now())+50);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)pushCheck()});
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
 const on=pushOn(),can=pushOK&&devicePush.perm!=='denied';
 const device=on?'Push is on here.':!can?'This browser can’t show push here.':n.push_devices?t(['Push is off here, on for {} other device.','Push is off here, on for {} other devices.'],n.push_devices):'Push is off here.';
 const more=`<div><span class="grow"><strong>This device</strong><small>${esc(device)}</small></span>${!on&&can?'<button type="button" data-device="push-on">Turn on</button>':''}</div>`;
 const m=$('#notify-more');if(m.dataset.html!==more){m.innerHTML=more;m.dataset.html=more}}
$('#settings-notify').addEventListener('click',async e=>{const sw=e.target.closest('[data-notify-kind]');
 if(sw){const on=sw.getAttribute('aria-checked')!=='true';sw.disabled=true;
  try{state.notify=await notifyPost('notify_set',{kind:sw.dataset.notifyKind,channel:sw.dataset.notifyChannel,on});renderNotify()}catch(err){errCaught(err);toast(err.message,true)}finally{sw.disabled=false}return}
 const d=e.target.closest('[data-device]');if(d){d.disabled=true;try{await deviceRun(d.dataset.device)}finally{d.disabled=false;renderNotify()}return}
 const pv=e.target.closest('[data-notify-preview]');if(pv){const out=$('#notify-preview');if(!out.hidden){out.hidden=true;renderNotify();return}pv.disabled=true;
  try{const r=await notifyPost('notify_preview');out.textContent=r.empty?'Nothing for a digest right now.':r.text;out.hidden=false;renderNotify()}catch(err){errCaught(err);toast(err.message,true)}finally{pv.disabled=false}}});
