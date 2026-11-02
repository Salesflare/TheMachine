import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// This device: a quiet nudge at the top of Suggestions to install the app (the browser's prompt on Chromium, steps on an
// iPhone, nothing on Firefox) and then to turn on notifications (permission and a subscription from one tap, then a test).
// One at a time, never in the first minute or while setting up; Not now waits 14 days, a second Not now stops it. Settings,
// General, This device has the same controls for good. A page in a frame or without a service worker (the site's demo)
// shows no nudge and never asks for a permission. The browser's install, permission and push parts are stand-ins here.
// SHOTS=<folder> saves light and dark screenshots at 390 and 1440.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
let setupHints=[],handledFirst=true,phoneStore=null;
let connectors=[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}];
const status=()=>({suggestions:[{id:'ab'.repeat(8),title:'Reply to Robin about the garden plan',body:'Robin asked for the dates.',status:'pending',scope:'personal',created_at:now,event_ids:[1]}],
 promises:[],connectors,suggestion_counts:{pending:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],setup_hints:setupHints,handled_first:handledFirst,phone_app_store:phoneStore});
const actions=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/frame'){res.setHeader('Content-Type','text/html');res.end('<!doctype html><iframe src="/" style="width:1200px;height:800px"></iframe>');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/push-key'){res.end(JSON.stringify({key:'B'+'A'.repeat(86)}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);res.end(JSON.stringify(r.action==='push_test'?{sent:true}:{subscribed:r.action==='push_subscribe'}));return}
 // brand/avatar.png is the app icon, as assistant.py serves it (there is no avatar.png file)
 if(/^\/brand\/[\w.-]+\.(png|webp|woff2)$/.test(url.pathname)){try{const f=await readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url));res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':url.pathname.endsWith('.webp')?'image/webp':'font/woff2');res.end(f)}catch{res.statusCode=404;res.end()}return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const UA={
 chrome:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
 android:'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',
 iphone:'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1',
 ipad:'Mozilla/5.0 (iPad; CPU OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1',
 firefox:'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0',
 phoneApp:'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36 TheMachineApp/1'};
// The browser's side, made up: permission, a push subscription, display mode, related apps, and what was asked.
function fakeBrowser(o){
 const log=window.__log=[];
 if(!o.fresh)try{sessionStorage.setItem('device-session',String(Date.now()-120000))}catch{}
 if(o.demo){for(const [owner,name] of [[Navigator.prototype,'serviceWorker'],[window,'PushManager'],[window,'Notification']])try{delete owner[name]}catch{}}
 if(o.noPush){try{delete window.PushManager;delete window.Notification}catch{}}
 if(o.noInstall){try{delete Window.prototype.onbeforeinstallprompt;delete window.onbeforeinstallprompt}catch{}}
 if(window.Notification){let p=o.perm||'default';Object.defineProperty(Notification,'permission',{configurable:true,get:()=>p});
  Notification.requestPermission=async()=>{log.push('requestPermission');if(p==='default')p=o.answer||'granted';return p}}
 const sub=()=>({endpoint:'https://push.example/device-1',toJSON(){return {endpoint:this.endpoint,keys:{p256dh:'B'+'x'.repeat(86),auth:'y'.repeat(22)}}},unsubscribe:async()=>{log.push('unsubscribe');current=null;return true}});
 let current=o.sub?sub():null;
 const reg={pushManager:{getSubscription:async()=>current,subscribe:async()=>{log.push('subscribe');current=sub();return current}}};
 if(navigator.serviceWorker)navigator.serviceWorker.register=async()=>reg;
 const mm=window.matchMedia.bind(window);
 window.matchMedia=q=>{const m=/display-mode: ([\w-]+)/.exec(q);return m?{matches:o.mode===m[1],media:q,addEventListener(){},removeEventListener(){},addListener(){},removeListener(){}}:mm(q)};
 if('related' in o)navigator.getInstalledRelatedApps=async()=>o.related?[{platform:'webapp',url:location.origin+'/manifest.webmanifest'}]:[];
 if(o.iosApp)Object.defineProperty(navigator,'standalone',{configurable:true,value:true});
 if(o.blockStorage)for(const m of ['getItem','setItem','removeItem']){const real=Storage.prototype[m];Storage.prototype[m]=function(k,...v){if(/^(nudge|device|push-off|app-installed)/.test(k))throw new DOMException('blocked','SecurityError');return real.call(this,k,...v)}}
 window.__installPrompt=(outcome='accepted')=>{const e=new Event('beforeinstallprompt',{cancelable:true});e.prompt=async()=>{log.push('prompt')};e.userChoice=Promise.resolve({outcome});dispatchEvent(e)};
}
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const open=async({width=1440,height=900,ua='chrome',scheme='dark',url=base,...o}={})=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,userAgent:UA[ua],colorScheme:scheme,locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await context.addInitScript(fakeBrowser,o);
 const page=await context.newPage();page.on('pageerror',e=>errors.push(ua+' '+width+': '+e.message));
 await page.goto(url);if(url===base){await page.locator('#task-'+'ab'.repeat(8)).waitFor();await ready(page)}return {context,page}};
const ready=page=>page.waitForFunction(()=>(devicePush.checked||!pushOK)&&(!navigator.getInstalledRelatedApps||document.readyState==='complete')).then(()=>page.waitForTimeout(100));
const nudge=page=>page.evaluate(()=>{const el=document.querySelector('#device-nudge');return {kind:el.dataset.kind,shown:!el.hidden&&el.getBoundingClientRect().height>0,text:el.innerText.replace(/\s+/g,' ').trim()}});
const asked=page=>page.evaluate(()=>window.__log);
const stored=(page,k)=>page.evaluate(k=>{const v=localStorage.getItem(k);try{return JSON.parse(v)}catch{return v}},k);
const settings=async page=>{await page.evaluate(()=>showSettings('general'));await page.locator('#device-app').waitFor({state:'attached'});
 return page.evaluate(()=>{const row=id=>{const r=document.querySelector(id);return r.hidden?null:r.innerText.replace(/\s+/g,' ').trim()};
  const vis=s=>{const e=document.querySelector(s);return !!e&&!e.hidden&&e.getBoundingClientRect().height>0};
  return {help:['#device-app','#device-push'].map(id=>document.querySelector(id+' a.learn')?.href),app:row('#device-app'),push:row('#device-push'),toggle:vis('#push-toggle'),test:vis('#push-test'),theme:vis('#theme-toggle'),
   order:[...document.querySelector('#device-app').parentElement.children].map(e=>e.id||e.querySelector('[id]')?.id)}})};
const shot=async(page,name,sel)=>{if(!shots)return;if(sel)await page.locator(sel).evaluate(e=>scrollTo(0,Math.max(0,e.getBoundingClientRect().top+scrollY-120)));else await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(150);await page.screenshot({path:`${shots}/${name}.png`})};
const actionNames=()=>actions.map(a=>a.action).filter(n=>n!=='voice_status');  // Settings, General reads voice input's state
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // The command palette's actions, in one place.
 {const {context,page}=await open();
  assert.deepEqual(await page.evaluate(()=>window.deviceActions.map(a=>[a.id,a.label])),[['install-app','Install app'],['push-on','Turn on notifications'],['push-test','Send test notification']]);
  // In the command palette: what this device can do right now (no install offer yet, notifications not on).
  const pal=()=>page.evaluate(()=>actsFor(kbCtx()).filter(a=>a.group==='Actions').map(a=>a.id).filter(id=>window.deviceActions.some(d=>d.id===id)));
  assert.deepEqual(await pal(),['push-on']);
  await page.evaluate(()=>__installPrompt());assert.deepEqual(await pal(),['install-app','push-on']);
  await context.close()}

 // Chromium on a computer, not installed: the browser's own prompt from the owner's tap, then Installed, for good.
 for(const scheme of ['dark','light']){actions.length=0;
  const {context,page}=await open({scheme});
  assert.equal((await nudge(page)).kind,'push','notifications first');
  await page.evaluate(()=>__installPrompt());assert.equal((await nudge(page)).kind,'push','notifications first, also with an install on offer');
  await page.evaluate(()=>{devicePush.perm='granted';devicePush.sub={toJSON:()=>({endpoint:'https://push.example/device-1'})};deviceRender()});
  let n=await nudge(page);assert.equal(n.kind,'desktop','then the app on this computer');assert.ok(n.shown);
  assert.match(n.text,/Install The Machine/);assert.match(n.text,/Install it and pin it to your taskbar or dock\./);assert.doesNotMatch(n.text,/—|^You/m);
  assert.deepEqual(await asked(page),[],'nothing is asked before a tap');
  if(scheme==='dark'||shots)await shot(page,`install-desktop-1440-${scheme}`);
  // Calm: one card, under the page title, above the cards; it covers nothing.
  const box=await page.evaluate(()=>{const n=document.querySelector('#device-nudge').getBoundingClientRect(),c=document.querySelector('.card').getBoundingClientRect(),h=document.querySelector('#page-head').getBoundingClientRect();return {above:n.bottom<=c.top,under:n.top>=h.bottom-1,count:document.querySelectorAll('.device-nudge').length}});
  assert.deepEqual(box,{above:true,under:true,count:1});
  {const s=await settings(page);assert.match(s.app,/Install app/);assert.deepEqual(s.help,Array(2).fill('https://themachine.computer/help/phone-app'),'both rows link the help article')}await shot(page,`settings-install-1440-${scheme}`,'#device-app');await page.evaluate(()=>document.querySelector('nav [data-tab="inbox"]').click());
  await page.locator('#device-nudge [data-device="install-app"]').click();
  assert.deepEqual(await asked(page),['prompt']);
  await page.evaluate(()=>dispatchEvent(new Event('appinstalled')));
  n=await nudge(page);assert.equal(n.kind,'installed');assert.match(n.text,/Installed/);
  assert.equal(await stored(page,'app-installed'),1);
  const s=await settings(page);assert.match(s.app,/Installed/);assert.doesNotMatch(s.app,/Install app/);
  await page.reload();await page.locator('#task-'+'ab'.repeat(8)).waitFor({state:'attached'});await ready(page);
  await page.evaluate(()=>document.querySelector('nav [data-tab="inbox"]').click());
  assert.equal((await nudge(page)).kind,'push','installed for good: only notifications are left (off again after the reload)');
  await context.close()}

 // Android: the same prompt, with phone words. At 390 the card sits under the top bar.
 for(const scheme of ['dark','light']){const {context,page}=await open({width:390,height:844,ua:'android',scheme,perm:'granted',sub:true});
  await page.evaluate(()=>__installPrompt());const n=await nudge(page);
  assert.equal(n.kind,'android');assert.match(n.text,/Add it to your home screen\. It opens like an app\./);
  const fit=await page.evaluate(()=>{const n=document.querySelector('#device-nudge').getBoundingClientRect(),t=document.querySelector('#topbar').getBoundingClientRect();return {under:n.top>=t.bottom,fits:document.documentElement.scrollWidth<=innerWidth&&n.right<=innerWidth}});
  assert.deepEqual(fit,{under:true,fits:true});
  // The same room under the top bar as the page gets without the card (the first heading's).
  const gap=await page.evaluate(()=>document.querySelector('#device-nudge').getBoundingClientRect().top-document.querySelector('#topbar').getBoundingClientRect().bottom);
  const bare=await page.evaluate(()=>{const n=document.querySelector('#device-nudge');n.style.display='none';const g=document.querySelector('#suggestions>*').getBoundingClientRect().top-document.querySelector('#topbar').getBoundingClientRect().bottom;n.style.display='';return g});
  assert.ok(gap>=24&&Math.abs(gap-bare)<=2,'room under the top bar: '+gap+' vs '+bare);
  await shot(page,`install-android-390-${scheme}`);
  await context.close()}

 // Installed already: the app's own window, or the browser knows it as a related app. No install nudge, Installed in Settings.
 for(const o of [{mode:'standalone'},{mode:'window-controls-overlay'},{mode:'fullscreen'},{related:true},{iosApp:true,ua:'iphone',width:390,height:844}]){
  const {context,page}=await open({...o,perm:'granted',sub:true});
  assert.equal((await nudge(page)).shown,false,JSON.stringify(o));
  assert.match((await settings(page)).app,/Installed/,JSON.stringify(o));
  await context.close()}

 // iPhone in Safari: no prompt and no Web Push in a tab, so the steps, tied to notifications. Notifications wait for the app.
 for(const [ua,width,height] of [['iphone',390,844],['ipad',1440,1000]])for(const scheme of ['dark','light']){
  const {context,page}=await open({width,height,ua,scheme,noPush:true});
  const n=await nudge(page);assert.equal(n.kind,'ios');
  assert.match(n.text,/Add The Machine to your Home Screen/);assert.match(n.text,/Tap Share/);assert.match(n.text,/Tap Add to Home Screen/);
  assert.match(n.text,/Notifications on iPhone and iPad work only from there\./);
  assert.equal(await page.locator('#device-nudge .ios-share').count(),1);assert.equal(await page.locator('#device-nudge [data-device]').count(),0,'no button pretends to install');
  await shot(page,`ios-steps-${width}-${scheme}`);
  const s=await settings(page);assert.match(s.app,/Tap Share ?, then Add to Home Screen/);assert.match(s.push,/add it to your Home Screen first/);
  await context.close()}
 // From the Home Screen app, notifications are next.
 {const {context,page}=await open({width:390,height:844,ua:'iphone',iosApp:true});
  assert.equal((await nudge(page)).kind,'push');await context.close()}

 // Firefox on a computer can't install: no install nudge, only notifications.
 {const {context,page}=await open({ua:'firefox',noInstall:true});
  assert.equal((await nudge(page)).kind,'push');
  assert.match((await settings(page)).app,/This browser can’t install apps/);await context.close()}

 // Notifications, permission "default": one tap asks, subscribes and sends a test so they see it work.
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['dark','light']){actions.length=0;
  const {context,page}=await open({width,height,scheme,mode:'standalone'});
  let n=await nudge(page);assert.equal(n.kind,'push');assert.match(n.text,/Turn on notifications/);assert.match(n.text,/A ping when a to-do needs you, on this device only\./);
  await shot(page,`notifications-${width}-${scheme}`);
  assert.deepEqual(await asked(page),[]);
  if(width===390&&scheme==='light'){
   // Settings, General, This device: App, Notifications, Light mode. Off for now.
   let s=await settings(page);assert.deepEqual(s.order,['device-app','device-push',s.order[2]]);assert.equal(s.theme,true);
   assert.match(s.push,/^Notifications/);assert.equal(s.toggle,true);assert.equal(s.test,false);
   await context.close();continue}
  await page.locator('#device-nudge [data-device="push-on"]').click();
  await page.waitForFunction(()=>document.querySelector('#device-nudge').hidden&&document.querySelector('#toast').textContent.includes('A test is on its way'));
  assert.deepEqual(await asked(page),['requestPermission','subscribe']);
  assert.deepEqual(actionNames(),['push_subscribe','push_test']);assert.equal(actions[1].args.endpoint,'https://push.example/device-1');
  const s=await settings(page);assert.match(s.push,/On for this device/);assert.equal(s.test,true);
  if(width===1440)await shot(page,`settings-this-device-1440-${scheme}`,'#device-app');
  else await shot(page,`settings-this-device-390-${scheme}`,'#device-app');
  await page.locator('#push-test').click();await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('Test sent'));
  assert.deepEqual(actionNames(),['push_subscribe','push_test','push_test']);
  // Off in Settings stays off: no nudge comes back for it.
  await page.locator('#push-toggle').click();await page.waitForFunction(()=>document.querySelector('#push-toggle').getAttribute('aria-pressed')==='false');
  assert.equal(actionNames().at(-1),'push_unsubscribe');assert.equal(await stored(page,'push-off'),1);
  await page.evaluate(()=>{document.querySelector('nav [data-tab="inbox"]').click();deviceRender()});assert.equal((await nudge(page)).shown,false);
  await context.close()}
 // Settings shots with notifications on at 390 light too (the loop above kept that one off).
 if(shots){const {context,page}=await open({width:390,height:844,scheme:'light',mode:'standalone',perm:'granted',sub:true});
  await settings(page);await shot(page,'settings-this-device-390-light','#device-app');await context.close()}

 // Granted, but no subscription on this device: the nudge, and its tap only subscribes.
 {actions.length=0;const {context,page}=await open({mode:'standalone',perm:'granted'});
  assert.equal((await nudge(page)).kind,'push');
  await page.locator('#device-nudge [data-device="push-on"]').click();await page.waitForFunction(()=>document.querySelector('#device-nudge').hidden&&document.querySelector('#toast').textContent.includes('A test is on its way'));
  assert.ok((await asked(page)).includes('subscribe'));assert.deepEqual(actionNames(),['push_subscribe','push_test']);await context.close()}
 // Granted with a subscription: nothing to nudge; the subscription is synced once at start.
 {actions.length=0;const {context,page}=await open({mode:'standalone',perm:'granted',sub:true});
  assert.equal((await nudge(page)).shown,false);assert.deepEqual(actionNames(),['push_subscribe']);await context.close()}
 // Denied: no nagging; Settings says how to allow it again in the site settings.
 {const {context,page}=await open({mode:'standalone',perm:'denied'});
  assert.equal((await nudge(page)).shown,false);
  const s=await settings(page);assert.match(s.push,/Blocked in this browser\. Click the icon left of the address, then allow Notifications\./);assert.equal(s.toggle,false);
  assert.deepEqual(await asked(page),[]);await context.close()}
 // A closed permission prompt counts as Not now.
 {const {context,page}=await open({mode:'standalone',answer:'default'});
  await page.locator('#device-nudge [data-device="push-on"]').click();await page.waitForTimeout(200);
  assert.equal((await nudge(page)).shown,false);assert.equal((await stored(page,'nudge-push')).n,1);await context.close()}

 // Calm: nothing in the first minute of a session, nor while setting up (no source yet).
 {const {context,page}=await open({mode:'standalone',fresh:true});
  assert.equal((await nudge(page)).shown,false,'not in the first minute');
  await page.evaluate(()=>{sessionStorage.setItem('device-session',String(Date.now()-61000))});await page.reload();await page.locator('#task-'+'ab'.repeat(8)).waitFor({state:'attached'});await ready(page);
  assert.equal((await nudge(page)).kind,'push','after the first minute');
  connectors=[];await page.evaluate(()=>refresh());assert.equal((await nudge(page)).shown,false,'not while setting up');
  connectors=[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}];await page.evaluate(()=>refresh());
  assert.equal((await nudge(page)).kind,'push');
  await context.close()}

 // Not now: 14 days, then a day's rest before the next nudge, and a second Not now stops it on this device.
 {const {context,page}=await open({mode:'standalone'});
  await page.evaluate(()=>__installPrompt());assert.equal((await nudge(page)).kind,'push','notifications first, one at a time');
  await page.locator('#device-nudge [data-nudge-later]').click();
  let v=await stored(page,'nudge-push');assert.equal(v.n,1);assert.ok(Math.abs(v.until-Date.now()-14*864e5)<60e3,'14 days');
  assert.equal((await nudge(page)).shown,false,'nothing else the same day');
  await page.evaluate(()=>{localStorage.setItem('nudge-rest','0');deviceRender()});
  assert.equal((await nudge(page)).kind,'desktop','then the app');
  await page.locator('#device-nudge [data-nudge-later]').click();assert.equal((await stored(page,'nudge-install')).n,1);
  // 14 days later, notifications again; a second Not now stops it for good.
  await page.evaluate(()=>{for(const k of ['nudge-install','nudge-push']){const v=JSON.parse(localStorage.getItem(k));v.until=Date.now()-1;localStorage.setItem(k,JSON.stringify(v))}localStorage.setItem('nudge-rest','0');deviceRender()});
  assert.equal((await nudge(page)).kind,'push');
  await page.locator('#device-nudge [data-nudge-later]').click();assert.deepEqual(await stored(page,'nudge-push'),{n:2,stop:true});
  await page.evaluate(()=>{localStorage.setItem('nudge-rest','0');deviceRender()});assert.equal((await nudge(page)).kind,'desktop');
  await page.locator('#device-nudge [data-nudge-later]').click();assert.deepEqual(await stored(page,'nudge-install'),{n:2,stop:true});
  await page.evaluate(()=>{localStorage.setItem('nudge-rest','0');deviceRender()});assert.equal((await nudge(page)).shown,false,'stopped on this device');
  await page.reload();await page.locator('#task-'+'ab'.repeat(8)).waitFor({state:'attached'});await ready(page);await page.evaluate(()=>__installPrompt());
  assert.equal((await nudge(page)).shown,false);
  assert.match((await settings(page)).app,/Install app/,'Settings still has it');
  await context.close()}
 // Storage blocked: the page still works (and the nudge can't remember a Not now, so it still hides on tap).
 {const {context,page}=await open({mode:'standalone',blockStorage:true});
  if((await nudge(page)).shown){await page.locator('#device-nudge [data-nudge-later]').click()}
  await context.close()}

 // What setup left out (state.setup_hints, hosted): after the device ones, one at a time, linked to its setup step.
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['dark','light']){
  setupHints=[{id:'source-github',title:'Connect GitHub?',text:'GitHub mails you often. Connected, I read it directly.',href:'https://app.example.test/setup#source-github',button:'Connect'},
   {id:'codex',title:'Hand coding to-dos to Codex?',text:'It works on your ChatGPT plan.',href:'https://app.example.test/setup#codex',button:'Connect'}];
  const {context,page}=await open({width,height,scheme,mode:'standalone',perm:'granted',sub:true});
  await page.evaluate(()=>{window.__opened=[];window.open=(u,...r)=>{window.__opened.push([u,...r]);return null}});
  let n=await nudge(page);assert.equal(n.kind,'hint:source-github');assert.ok(n.shown);
  assert.match(n.text,/Connect GitHub\? GitHub mails you often\. Connected, I read it directly\./);assert.doesNotMatch(n.text,/—|^You/m);
  await shot(page,`setup-hint-${width}-${scheme}`);
  if(width===390||scheme==='light'){await context.close();continue}
  await page.locator('#device-nudge [data-hint-open]').click();
  assert.deepEqual(await page.evaluate(()=>window.__opened),[['https://app.example.test/setup#source-github','_blank','noopener']]);
  assert.equal((await nudge(page)).shown,false,'opened: it rests');
  await page.evaluate(()=>{localStorage.setItem('nudge-rest','0');const v=JSON.parse(localStorage.getItem('nudge-hint-source-github'));v.until=0;localStorage.setItem('nudge-hint-source-github',JSON.stringify(v));deviceRender()});
  assert.equal((await nudge(page)).kind,'hint:source-github','back after its rest, until GitHub is connected');
  await page.locator('#device-nudge [data-nudge-later]').click();assert.equal((await stored(page,'nudge-hint-source-github')).n,1);
  await page.evaluate(()=>{localStorage.setItem('nudge-rest','0');deviceRender()});assert.equal((await nudge(page)).kind,'hint:codex','then the next one');
  setupHints=[];await page.evaluate(()=>refresh());assert.equal((await nudge(page)).shown,false,'done at setup: gone');
  await context.close()}
 setupHints=[];

 // Only after the owner handled a first to-do: before it, nothing (the first look is the greeting and the work).
 {handledFirst=false;const {context,page}=await open();await page.evaluate(()=>__installPrompt());
  assert.equal((await nudge(page)).shown,false,'no nudge before a first handled to-do');
  handledFirst=true;await page.evaluate(()=>refresh());assert.equal((await nudge(page)).kind,'push','after it, the first one');
  await context.close()}

 // The whole order on a computer, one at a time, each Not now moving to the next after the day's rest: notifications,
 // the app, the phone app (once published), then what setup left out: more sources, Telegram, Codex.
 const HINTS=[{id:'source-github',title:'Connect GitHub?',text:'GitHub mails you often. Connected, I read it directly.',href:'#connect=github',button:'Connect'},
  {id:'telegram',title:'Reminders in Telegram?',text:'Snoozed to-dos come back as a Telegram message too.',href:'https://app.example.test/setup#telegram',button:'Set up'},
  {id:'codex',title:'Hand coding to-dos to Codex?',text:'It works on your ChatGPT plan.',href:'https://app.example.test/setup#codex',button:'Connect'}];
 const STORE={ios:'https://apps.example.test/ios',android:'https://play.example.test/android',page:'https://example.test/app',phones:0};
 const walk=async page=>{const seen=[];for(let i=0;i<10;i++){const n=await nudge(page);if(!n.shown)break;
  assert.equal(await page.locator('.device-nudge:not([hidden])').count(),1,'one at a time');seen.push(n.kind);
  await page.locator('#device-nudge [data-nudge-later]').click();assert.equal((await nudge(page)).shown,false,'Not now: nothing else that day');
  await page.evaluate(()=>{localStorage.setItem('nudge-rest','0');deviceRender()})}return seen};
 for(const flag of [true,false]){setupHints=HINTS;phoneStore=flag?STORE:null;
  const {context,page}=await open({width:1280,height:800});await page.evaluate(()=>__installPrompt());
  assert.deepEqual(await walk(page),['push','desktop',...(flag?['phone-desk']:[]),'hint:source-github','hint:telegram','hint:codex'],flag?'the order':'phone app flag off: no phone app');
  if(flag){const v=await stored(page,'nudge-phone');assert.equal(v.n,1);assert.ok(Math.abs(v.until-Date.now()-14*864e5)<60e3,'the phone app backs off like the rest')}
  await context.close()}

 // A phone's browser with the phone app published: the phone app in the place of installing the web app.
 for(const [ua,o,store] of [['android',{},'https://play.example.test/android'],['iphone',{noPush:true},'https://apps.example.test/ios']]){
  setupHints=HINTS;phoneStore=STORE;const {context,page}=await open({width:390,height:844,ua,...o});
  await page.evaluate(()=>{__installPrompt();window.__opened=[];window.open=(u,...r)=>{window.__opened.push([u,...r]);return null}});
  const seen=await walk(page);
  assert.deepEqual(seen,[...(ua==='android'?['push']:[]),'phone','hint:source-github','hint:telegram','hint:codex'],ua);
  // Get the app opens this phone's store, and the nudge rests.
  await page.evaluate(()=>{localStorage.clear();deviceRender()});if(ua==='android')await page.locator('#device-nudge [data-nudge-later]').click();
  await page.evaluate(()=>{localStorage.setItem('nudge-rest','0');deviceRender()});
  assert.equal((await nudge(page)).kind,'phone');assert.match((await nudge(page)).text,/Get the phone app Notifications, and sharing from any app\./);
  await page.locator('#device-nudge [data-phone-open]').click();
  assert.deepEqual(await page.evaluate(()=>window.__opened),[[store,'_blank','noopener']]);assert.equal((await nudge(page)).shown,false);
  await context.close()}
 // Flag off on a phone: installing the web app, as before.
 {setupHints=[];phoneStore=null;const {context,page}=await open({width:390,height:844,ua:'android',perm:'granted',sub:true});
  await page.evaluate(()=>__installPrompt());assert.equal((await nudge(page)).kind,'android');await context.close()}

 // Done on this device: never shown. Notifications on, running as the installed app, inside the phone app, a phone that
 // has the app already (on a computer), a source connected (the Machine drops its hint).
 phoneStore=STORE;setupHints=[];
 {const {context,page}=await open({mode:'standalone',perm:'granted',sub:true});
  assert.equal((await nudge(page)).kind,'phone-desk','installed here, notifications on: the phone is another device');await context.close()}
 for(const [o,why] of [[{width:390,height:844,ua:'phoneApp',perm:'granted',sub:true},'in the phone app'],
  [{width:390,height:844,ua:'android',mode:'standalone',perm:'granted',sub:true},'the web app on the phone']]){
  const {context,page}=await open(o);assert.equal((await nudge(page)).shown,false,why);await context.close()}
 {phoneStore={...STORE,phones:1};const {context,page}=await open({mode:'standalone',perm:'granted',sub:true});
  assert.equal((await nudge(page)).shown,false,'a phone has the app');
  setupHints=HINTS.slice(1);await page.evaluate(()=>refresh());assert.equal((await nudge(page)).kind,'hint:telegram','GitHub connected: its hint is gone');
  await context.close()}

 // Screenshots of each one, at 390 and 1280, light (and dark for the first).
 if(shots){setupHints=HINTS;phoneStore=STORE;
  const each=[['push',{}],['install',{perm:'granted',sub:true,prompt:true,noPhone:true}],['phone',{perm:'granted',sub:true,mode:'standalone',phoneOnly:true}],
   ['hint-source',{perm:'granted',sub:true,mode:'standalone',skip:['phone']}],['hint-telegram',{perm:'granted',sub:true,mode:'standalone',skip:['phone','hint-source-github']}],
   ['hint-codex',{perm:'granted',sub:true,mode:'standalone',skip:['phone','hint-source-github','hint-telegram']}]];
  for(const [name,{prompt,phoneOnly,noPhone,skip=[],...o}] of each)for(const width of [390,1280])for(const scheme of name==='push'?['light','dark']:['light']){
   phoneStore=noPhone?null:STORE;  // the web app's install on a phone: with the phone app off
   const mobile=width<600,opts={...o,width,height:mobile?844:800,ua:mobile?'android':'chrome',scheme};
   if(phoneOnly&&mobile)delete opts.mode;
   const {context,page}=await open(opts);
   await page.evaluate(skip=>{for(const k of skip)localStorage.setItem('nudge-'+k,JSON.stringify({n:2,stop:true}));deviceRender()},skip);
   if(prompt)await page.evaluate(()=>__installPrompt());
   await shot(page,`order-${name}-${width}-${scheme}`);await context.close()}
  setupHints=[];phoneStore=null}
 setupHints=[];phoneStore=null;handledFirst=true;

 // The site's demo: in a frame, without a service worker, push or notifications. No nudge and nothing asked.
 {const {context,page}=await open({url:base+'frame'});const frame=page.frames().find(f=>f!==page.mainFrame());
  await frame.locator('#task-'+'ab'.repeat(8)).waitFor();await frame.evaluate(()=>{__installPrompt();deviceRender()});
  assert.equal(await frame.evaluate(()=>document.querySelector('#device-nudge').hidden),true);
  assert.deepEqual(await frame.evaluate(()=>window.__log),[]);assert.equal(await frame.evaluate(()=>document.querySelector('#device-app').hidden),true);
  await context.close()}
 {const {context,page}=await open({demo:true});await page.evaluate(()=>{__installPrompt();deviceRender()});
  assert.equal((await nudge(page)).shown,false);assert.deepEqual(await asked(page),[]);await context.close()}

 assert.deepEqual(errors,[]);
 console.log('device nudge dashboard ok');
}finally{await browser?.close();server.close()}
