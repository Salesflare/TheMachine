// This device: notifications on and the app installed, with the controls in Settings, General, This device. The steps
// to get there are rows of the setup to-do at the top of To-dos (setup-card.js). Every browser prompt comes from the
// owner's own tap. Inside the phone app, one quiet line at the top when its notifications are off (#device-nudge).
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
// A phone: by its user agent, or a small touch screen asking for desktop sites. There the phone app is a store link.
const onPhone=()=>{if(DEV.mobile)return true;try{return matchMedia('(pointer: coarse)').matches&&Math.min(screen.width,screen.height)<600}catch{return false}};
const inApp=()=>['standalone','fullscreen','window-controls-overlay'].some(m=>matchMedia(`(display-mode: ${m})`).matches)||navigator.standalone===true;
let installEvt=null,relatedInstalled=false;
// Seen as the app: kept, as a tab can't tell. An install offer: not installed.
if(inApp())devStore.set('app-installed','1');
const appInstalled=()=>inApp()||!installEvt&&(relatedInstalled||devStore.get('app-installed')==='1');
// Installing here: the browser's prompt (Chromium), steps (iPhone, Mac Safari) or nothing (Firefox).
function installKind(){if(!nudgeable)return null;if(installEvt)return DEV.mobile?'android':'desktop';if(appInstalled())return null;return DEV.ios?'ios':DEV.macSafari?'mac':null}
addEventListener('beforeinstallprompt',e=>{e.preventDefault();installEvt=e;devStore.set('app-installed',null);deviceRender()});
// Installed (setup to-do, Settings or the browser's menu): a toast, once.
let installedNoted=false;
function noteInstalled(){installEvt=null;devStore.set('app-installed','1');if(!installedNoted){installedNoted=true;toast('Installed. The Machine is in your apps now.')}deviceRender()}
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
// Still setting up: no state yet, no source yet, or the first look running. The setup to-do waits for it.
const settingUp=()=>!state?.suggestions||!(state.connectors||[]).length||!!firstLookInfo(state.review_live||{});
// The phone app with its notifications off (never asked, said no, or off in the phone's settings): one short line at
// the top, Turn on (the phone's question, or Open settings once it won't ask) and an X that keeps it away 7 days. On a
// first sign-in the phone asks once by itself, right after the dashboard loads, with nothing before it.
const APP_PUSH_REST=7*864e5;
function appPushOff(){const phone=phoneAppPush(),n=state?.notify;if(!phone||!window.machinePhone||!n?.app_push_ready||!['granted','prompt','blocked'].includes(phonePush))return false;
 return phonePush!=='granted'||!(n.app_devices||[]).some(p=>p.id===phone.id)}
let appPushAsking=false;
async function appPushOn(){appPushAsking=true;try{const r=await window.machinePhone.pushOn();phonePush=r==='on'?'granted':r==='blocked'?'blocked':'prompt';if(r==='on'){toast(t('Push is on here.'));await refresh()}}
 catch(err){errCaught(err)}finally{appPushAsking=false;deviceRender()}}
function appPushFirst(){if(appPushAsking||phonePush!=='prompt'||!appPushOff()||devStore.get('app-push-asked'))return;devStore.set('app-push-asked','1');appPushOn()}
// Only the phone app's own notification line here; every other step is a row of the setup to-do (setup-card.js).
function nudgeKind(){return !DEV.framed&&appPushOff()&&!appPushAsking&&!(+devStore.get('nudge-app-push')>Date.now())?'app-push':null}
const SHARE_ICON='<svg class="ios-share" viewBox="0 0 24 24" role="img" aria-label="Share"><path d="M12 14V3.5M8.2 7.2 12 3.4l3.8 3.8"/><path d="M8.5 10H7a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2h-1.5"/></svg>';
// How to install from this browser when it has no prompt to show (This device here, and Computer in Settings, Apps)
const installSteps=()=>DEV.ios?html`Tap Share ${raw(SHARE_ICON)}, then Add to Home Screen.`:DEV.macSafari?'In Safari’s menu bar: File, then Add to Dock.':DEV.chromium?'Find Install in the browser’s menu, or the icon in the address bar.':'This browser can’t install apps. Chrome, Edge and Safari can.';
const nudgeHTML=()=>html`<div class="nudge-text"><strong>Get a ping when something needs you.</strong></div><div class="nudge-act">${phonePush==='blocked'?html`<button type="button" class="primary" data-app-settings>Open settings</button>`:html`<button type="button" class="primary" data-app-on>Turn on</button>`}<button type="button" class="nudge-x" data-nudge-x aria-label="Close" title="Close"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7L7 17"/></svg></button></div>`;
const nudgeBox=(()=>{const el=document.createElement('div');el.id='device-nudge';el.className='notice-card device-nudge';el.setAttribute('role','region');el.setAttribute('aria-label','This device');el.hidden=true;el.dataset.kind='';
 $('#inbox').prepend(el);el.onclick=async e=>{const b=e.target.closest('button');if(!b)return;
  if(b.matches('[data-nudge-x]')){devStore.set('nudge-app-push',String(Date.now()+APP_PUSH_REST));deviceRender();return}
  if(b.matches('[data-app-settings]')){window.machinePhone?.settings().catch(()=>{});return}
  if(b.matches('[data-app-on]')){b.disabled=true;await appPushOn()}};return el})();
// Settings, General, This device: App, Notifications (with Send a test), Light mode.
const deviceRows=(()=>{const theme=$('#theme-toggle').closest('.settings-list>div'),list=theme.parentElement,pushRow=$('#push-toggle').closest('.settings-list>div');
 const app=document.createElement('div');app.id='device-app';setHTML(app,html`<span class="grow"><strong>App</strong><small></small></span><span class="device-act"></span>`);
 pushRow.id='device-push';pushRow.querySelector('strong').textContent='Notifications';
 const test=document.createElement('button');test.type='button';test.className='ghost';test.id='push-test';test.textContent='Send a test';test.hidden=true;$('#push-toggle').before(test);
 test.onclick=async()=>{test.disabled=true;try{await pushTest()}finally{test.disabled=false}};
 list.prepend(app);list.insertBefore(pushRow,theme);return {app,push:pushRow}})();
// The help article for both rows (docs/help/phone-app.md on themachine.computer/help).
const DEVICE_HELP=html` <a class="learn" href="https://themachine.computer/help/phone-app" target="_blank" rel="noopener">Learn more</a>`;
// setHTML, only when the markup changed (a redraw would close an open details or move the focus)
const putHTML=(el,h)=>{const s=String(h);if(el.dataset.html!==s){setHTML(el,h);el.dataset.html=s}};
function deviceSettings(){const {app}=deviceRows,small=app.querySelector('small'),act=app.querySelector('.device-act'),set=putHTML;
 app.hidden=!nudgeable;
 if(installEvt){set(small,html`${DEV.mobile?'Opens like an app, from your home screen.':'Pin it to your taskbar or dock.'}${DEVICE_HELP}`);set(act,html`<button type="button" data-device="install-app">Install app</button>`)}
 else if(appInstalled()){set(small,html`${'Installed on this device.'}${DEVICE_HELP}`);set(act,html`<span class="device-done">Installed</span>`)}
 else{set(small,html`${installSteps()}${DEVICE_HELP}`);set(act,html``)}
 const b=$('#push-toggle'),note=deviceRows.push.querySelector('small'),on=pushOn(),blocked=pushOK&&devicePush.perm==='denied';
 b.hidden=!(pushOK?!blocked:iosTab&&!navigator.standalone);b.title=!pushOK?iosHint:on?'Notifications on':'Turn on notifications';b.setAttribute('aria-pressed',String(on));
 $('#push-test').hidden=!on;
 const text=!pushOK?(iosTab?'On iPhone and iPad, add it to your Home Screen first: Share, then Add to Home Screen.':'This browser can’t show notifications.'):blocked?t('Blocked in this browser.')+' '+blockedHint():on?'On for this device. One per to-do, even without Telegram.':'One per to-do, even without Telegram.';
 set(note,html`${text}${DEVICE_HELP}`);note.classList.toggle('device-blocked',blocked)}
function deviceRender(){appPushFirst();const k=nudgeKind()||'',el=nudgeBox,h=k&&k+phonePush;if(el.dataset.h!==h){el.dataset.h=h;el.dataset.kind=k;setHTML(el,k?nudgeHTML():html``);el.hidden=!k}deviceSettings();if(lazyIn('settings'))renderNotify();phoneAppRender();setupRender();if(lazyIn('settings'))appsRender()}
// The mobile app's push on this phone: {id} once the app handed the Machine its token (www/inject.js), {id:null}
// before that, null outside the app
// In the app: whether the phone will still ask about notifications (machinePhone, mobile/www/inject.js); checked again
// when the owner comes back (from the phone's settings)
let phonePush='';
async function phonePushCheck(){const p=window.machinePhone;if(!p)return;let s='';try{s=await p.state('push')}catch{}if(s!==phonePush){phonePush=s;deviceRender()}}
function phoneAppPush(){if(!document.documentElement.classList.contains('in-app'))return null;
 try{const k=JSON.parse(localStorage.getItem('machine-app-push')||'null');return {id:typeof k?.id==='string'?k.id:null}}catch{return {id:null}}}
// In the mobile app: says once when its notifications can't work (off The Machine Network). How the app finds this
// Machine (sign-in, or a code off the Network) is in Settings, Apps (appsSignIn in settings-apps.js).
function phoneAppRender(){if(!document.documentElement.classList.contains('in-app'))return;
 if(state?.notify&&!state.notify.app_push_ready&&!devStore.get('app-push-network')){devStore.set('app-push-network',1);toast(t('Notifications in the app need The Machine Network. The app works without them.'))}}
deviceRows.app.onclick=e=>{const b=e.target.closest('[data-device]');if(b)deviceRun(b.dataset.device)};
$('#push-toggle').onclick=async()=>{const b=$('#push-toggle');if(!pushOK){toast(iosHint);return}b.disabled=true;try{if(pushOn())await pushDisable();else await pushEnable()}finally{b.disabled=false}};
document.addEventListener('visibilitychange',()=>{if(!document.hidden){pushCheck();phonePushCheck()}});
addEventListener('machinephone',()=>{phonePush='';if(lazyIn('settings'))renderNotify()});  // the app's part came in after this page drew
pushCheck(true);
// A notification opens its link in this page: only the part after # changes, so nothing reloads
if(pushOK)navigator.serviceWorker.addEventListener('message',e=>{if(!e.data?.open)return;const u=new URL(e.data.open,location.href);
 if(u.origin!==location.origin||u.pathname!==location.pathname||u.search!==location.search){location.href=u.href;return}if(u.hash!==location.hash)location.hash=u.hash;else dispatchEvent(new HashChangeEvent('hashchange'))});
const notifyPost=(action,args={})=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
