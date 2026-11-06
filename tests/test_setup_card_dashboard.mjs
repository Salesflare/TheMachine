import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {execFileSync} from 'node:child_process';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The setup to-do at the top of To-dos (dashboard/setup-card.js): one small card, "Get more out of The Machine", a row per
// step (the phone app, notifications, WhatsApp, the app on this computer, another account, more connections, then what
// setup left out), at most 5, each with one button that does the step, ticked once done, closed for good with its ×
// (setup_dismiss, kept on the Machine so every device agrees). Rows show only where they apply. From the first visit,
// once the first look is done; never in a frame but the site's demo. Settings, General, This device keeps the controls.
// The browser's install, permission and push parts are stand-ins here. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
// Real codes for the store links (qr.py, as assistant.phone_app_nudge makes them)
const codes=JSON.parse(execFileSync('python3',['-c','import json,qr;print(json.dumps([qr.encode(u) for u in ("https://apps.example.test/ios","https://play.example.test/android","https://example.test/app")]))'],{cwd:new URL('..',import.meta.url)}).toString());
const STORE={ios:'https://apps.example.test/ios',android:'https://play.example.test/android',phones:0,qr_ios:codes[0],qr_android:codes[1]};
const FRESH={closed:false,dismissed:[],phones:0,whatsapp:false,mail_accounts:1,add:'google',more:false};
let setupHints=[],phoneStore=STORE,setup={...FRESH},manage='https://app.example.test/setup',firstLook=null;
let connectors=[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}];
const status=()=>({suggestions:[{id:'ab'.repeat(8),title:'Reply to Robin about the garden plan',body:'Robin asked for the dates.',status:'pending',scope:'personal',created_at:now,event_ids:[1]}],
 promises:[],connectors,suggestion_counts:{pending:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:firstLook||{runs:[]},
 setup_hints:setupHints,phone_app_store:phoneStore,setup_card:setup,...(manage?{manage_url:manage}:{})});
const actions=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/frame'){res.setHeader('Content-Type','text/html');res.end('<!doctype html><iframe src="/" style="width:1200px;height:800px"></iframe>');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/push-key'){res.end(JSON.stringify({key:'B'+'A'.repeat(86)}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);
  // the Machine keeps a closed row (assistant.setup_dismiss): every device gets it with its next state
  // + Add's list, with the two sources the setup to-do opens there
  if(r.action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:manage||null,paired:!manage,sources:[{name:'whatsapp',label:'WhatsApp',service:'whatsapp',hosted_signin:'whatsapp',what:'Your chats.'},
   {name:'google',label:'Google',service:'gmail',hosted_signin:'google',what:'Mail and calendar.'}]}));return}
  if(r.action==='setup_dismiss'){const step=r.args.step;setup=step==='card'?{...setup,closed:true}:{...setup,dismissed:[...new Set([...setup.dismissed,step])].sort()};res.end(JSON.stringify({setup_card:setup}));return}
  res.end(JSON.stringify(r.action==='push_test'?{sent:true}:{subscribed:r.action==='push_subscribe'}));return}
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
// The setup to-do as shown: whether it is, its title line, and each row [step, label, button or 'done']
const card=page=>page.evaluate(()=>{const el=document.querySelector('#setup-card');const shown=!!el&&!el.hidden&&el.getBoundingClientRect().height>0;
 return {shown,head:shown?el.querySelector('.setup-head').innerText.replace(/\s+/g,' ').trim():'',
  rows:shown?[...el.querySelectorAll('.setup-row')].map(r=>[r.dataset.step,r.querySelector('.setup-label').textContent,r.classList.contains('done')?'done':r.querySelector('.setup-go').textContent]):[]}});
const steps=async page=>(await card(page)).rows.map(r=>r[0]);
const asked=page=>page.evaluate(()=>window.__log);
const stored=(page,k)=>page.evaluate(k=>{const v=localStorage.getItem(k);try{return JSON.parse(v)}catch{return v}},k);
const settings=async page=>{await page.evaluate(()=>showSettings('general'));await page.locator('#device-app').waitFor({state:'attached'});
 return page.evaluate(()=>{const row=id=>{const r=document.querySelector(id);return r.hidden?null:r.innerText.replace(/\s+/g,' ').trim()};
  const vis=s=>{const e=document.querySelector(s);return !!e&&!e.hidden&&e.getBoundingClientRect().height>0};
  return {help:['#device-app','#device-push'].map(id=>document.querySelector(id+' a.learn')?.href),app:row('#device-app'),push:row('#device-push'),toggle:vis('#push-toggle'),test:vis('#push-test'),theme:vis('#theme-toggle'),
   order:[...document.querySelector('#device-app').parentElement.children].map(e=>e.id||e.querySelector('[id]')?.id)}})};
const shot=async(page,name,sel)=>{if(!shots)return;if(sel)await page.locator(sel).evaluate(e=>scrollTo(0,Math.max(0,e.getBoundingClientRect().top+scrollY-120)));else await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(150);await page.screenshot({path:`${shots}/${name}.png`})};
const actionNames=()=>actions.map(a=>a.action).filter(n=>n!=='voice_status');  // Settings, General reads voice input's state
const reset=()=>{setupHints=[];phoneStore=STORE;setup={...FRESH};manage='https://app.example.test/setup';firstLook=null;actions.length=0};
const fits=async(page,why)=>assert.ok(await page.evaluate(()=>{const c=document.querySelector('#setup-card').getBoundingClientRect();return document.documentElement.scrollWidth<=innerWidth&&c.left>=0&&c.right<=innerWidth}),why+': fits the screen');
const opened=page=>page.evaluate(()=>{window.__opened=[];window.open=(u,...r)=>{window.__opened.push([u,...r]);return null}});
const copy=/—|^You/m;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // The command palette's actions, in one place.
 {reset();const {context,page}=await open();
  assert.deepEqual(await page.evaluate(()=>window.deviceActions.map(a=>[a.id,a.label])),[['install-app','Install app'],['push-on','Turn on notifications'],['push-test','Send test notification']]);
  const pal=()=>page.evaluate(()=>actsFor(kbCtx()).filter(a=>a.group==='Actions').map(a=>a.id).filter(id=>window.deviceActions.some(d=>d.id===id)));
  assert.deepEqual(await pal(),['push-on']);
  await page.evaluate(()=>__installPrompt());assert.deepEqual(await pal(),['install-app','push-on']);
  await context.close()}

 // A computer (Chromium), hosted, nothing done: from the first visit, one card above the to-dos with five rows in order.
 for(const scheme of ['light','dark']){reset();
  const {context,page}=await open({scheme});await page.evaluate(()=>__installPrompt());
  const c=await card(page);assert.ok(c.shown);
  assert.equal(c.head,'Get more out of The Machine 0 of 5 done');
  assert.deepEqual(c.rows,[['phone','Get the phone app','Get it'],['push','Turn on notifications','Turn on'],['whatsapp','Connect WhatsApp','Connect'],
   ['install','Install on this computer','Install'],['account','Add another Google account','Add']],'at most 5, in order: more connections waits');
  assert.doesNotMatch(c.head+c.rows.flat().join(' '),copy);
  assert.deepEqual(await asked(page),[],'nothing is asked before a tap');
  const box=await page.evaluate(()=>{const n=document.querySelector('#setup-card').getBoundingClientRect(),c=document.querySelector('.card').getBoundingClientRect(),h=document.querySelector('#page-head').getBoundingClientRect();
   return {above:n.bottom<=c.top,under:n.top>=h.bottom-1,count:document.querySelectorAll('.setup-card:not([hidden])').length,nudge:document.querySelector('#device-nudge').hidden,rows:[...document.querySelectorAll('.setup-row')].map(r=>Math.round(r.getBoundingClientRect().height))}});
  const {rows,...where}=box;assert.deepEqual(where,{above:true,under:true,count:1,nudge:true});assert.ok(rows.every(h=>h>=44&&h<=48),'tight rows: '+rows);
  await shot(page,`setup-1440-${scheme}`);
  await context.close()}

 // Each button does its step. Notifications: the browser's question from the tap, a subscription and a test; the row ticks.
 {reset();setup={...FRESH,dismissed:['phone']};const {context,page}=await open({mode:'standalone'});await opened(page);
  assert.deepEqual((await card(page)).rows.map(r=>r[2]==='done'?r[0]+' done':r[0]),['push','whatsapp','install done','account','connect'],'running as the installed app: ticked');
  await page.locator('[data-setup-go="push"]').click();
  await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('A test is on its way'));
  assert.deepEqual(await asked(page),['requestPermission','subscribe']);assert.deepEqual(actionNames(),['push_subscribe','push_test']);
  let c=await card(page);assert.deepEqual(c.rows[0],['push','Turn on notifications','done']);assert.equal(c.head,'Get more out of The Machine 2 of 5 done');
  // WhatsApp, another account and more connections open their own form under Connections
  for(const [step,hash] of [['whatsapp','#connect=whatsapp'],['account','#connect=google'],['connect','#connections=add']]){
   const seen=page.evaluate(()=>new Promise(r=>addEventListener('hashchange',()=>r(location.hash||history.state||''),{once:true})));
   await page.locator(`[data-setup-go="${step}"]`).click();
   const got=await seen;assert.ok([hash,''].includes(got),step+' '+got);
   assert.equal(await page.evaluate(()=>document.querySelector('#health').hidden),false,step+': Connections opens');
   if(step!=='connect')await page.waitForFunction(p=>connectSignin?.provider===p,step==='whatsapp'?'whatsapp':'google');  // its own sign-in, right there
   await page.evaluate(()=>{document.querySelector('nav [data-tab="inbox"]').click()})}
  await context.close()}
 // Installing: the browser's own prompt from the tap, then the row is ticked.
 {reset();const {context,page}=await open();await page.evaluate(()=>__installPrompt());
  await page.locator('[data-setup-go="install"]').click();assert.deepEqual(await asked(page),['prompt']);
  await page.evaluate(()=>dispatchEvent(new Event('appinstalled')));
  assert.deepEqual((await card(page)).rows[3],['install','Install on this computer','done']);
  assert.match((await settings(page)).app,/Installed/);await context.close()}

 // A row's ×: closed on the Machine, the next step fills its place, and it stays closed on another device.
 {reset();const {context,page}=await open();await page.evaluate(()=>__installPrompt());
  await page.locator('[data-setup-dismiss="whatsapp"]').click();
  await page.waitForFunction(()=>!document.querySelector('[data-step="whatsapp"]'));
  assert.deepEqual(actions.filter(a=>a.action==='setup_dismiss'),[{action:'setup_dismiss',args:{step:'whatsapp'}}]);
  assert.deepEqual(await steps(page),['phone','push','install','account','connect']);
  const other=await open({width:390,height:844,ua:'android',scheme:'light'});
  assert.ok(!(await steps(other.page)).includes('whatsapp'),'closed on the desktop: closed on the phone too');await other.context.close();
  // The card's ×: all of it, for good, everywhere
  await page.locator('[data-setup-close]').click();await page.waitForFunction(()=>document.querySelector('#setup-card').hidden);
  assert.deepEqual(actions.filter(a=>a.action==='setup_dismiss').at(-1),{action:'setup_dismiss',args:{step:'card'}});
  await page.reload();await page.locator('#task-'+'ab'.repeat(8)).waitFor({state:'attached'});await ready(page);
  assert.equal((await card(page)).shown,false,'closed for good');
  assert.match((await settings(page)).app,/^App /,'Settings still has the controls');
  await context.close()}

 // Partly done: what the Machine knows (a phone has the app, a second account) and this device (notifications on) ticks.
 for(const [width,height,scheme,ua] of [[1440,900,'light','chrome'],[1440,900,'dark','chrome'],[390,844,'light','android'],[390,844,'dark','android']]){reset();
  setup={...FRESH,phones:1,mail_accounts:2};
  const {context,page}=await open({width,height,scheme,ua,perm:'granted',sub:true});if(width>600)await page.evaluate(()=>__installPrompt());
  const c=await card(page);
  assert.deepEqual(c.rows.map(r=>r[2]==='done'?r[0]+' done':r[0]),width>600?['phone done','push done','whatsapp','install','account done']:['phone done','push done','whatsapp','account done','connect'],width+'');
  assert.equal(c.head,'Get more out of The Machine 3 of 5 done');
  await fits(page,width+' partly done');await shot(page,`setup-partly-${width}-${scheme}`);
  await context.close()}
 // Everything done: the card goes away.
 {reset();setup={...FRESH,phones:1,mail_accounts:2,whatsapp:true,more:true};const {context,page}=await open({mode:'standalone',perm:'granted',sub:true});
  assert.equal((await card(page)).shown,false);await context.close()}

 // The phone app on a computer: Get it opens a QR code in the row, one per store until the store redirect is live
 // (phone_app_store.qr), then one code with both stores beside it. Never a help article.
 for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']])for(const one of [false,true]){reset();
  phoneStore=one?{ios:STORE.ios,android:STORE.android,phones:0,qr:codes[2]}:STORE;
  const {context,page}=await open({width,height,scheme,perm:'granted',sub:true});
  await page.locator('[data-setup-go="phone"]').click();
  const qr=await page.evaluate(()=>{const q=document.querySelector('.setup-qr');return {codes:q.querySelectorAll('svg.connect-qr').length,stores:[...q.querySelectorAll('a.store-badge')].map(a=>[a.textContent,a.href]),
   help:!!document.querySelector('#setup-card a[href*="help"]'),open:document.querySelector('[data-setup-go="phone"]').getAttribute('aria-expanded')}});
  assert.deepEqual(qr,{codes:one?1:2,stores:[['App Store',STORE.ios],['Google Play',STORE.android]],help:false,open:'true'});
  assert.deepEqual(actionNames().filter(n=>n!=='push_subscribe'),[],'nothing is opened or sent');
  await fits(page,width+' QR');await shot(page,`setup-qr${one?'-one':''}-${width}-${scheme}`,'#setup-card');
  await page.locator('[data-setup-go="phone"]').click();assert.equal(await page.locator('.setup-qr').count(),0,'Get it again folds it');
  await context.close()}

 // A phone's browser: the phone app opens this phone's store; no installing the web app on a phone.
 for(const [ua,o,store] of [['android',{},STORE.android],['iphone',{noPush:true},STORE.ios]]){reset();
  const {context,page}=await open({width:390,height:844,ua,...o});await opened(page);await page.evaluate(()=>__installPrompt());
  assert.deepEqual(await steps(page),ua==='android'?['phone','push','whatsapp','account','connect']:['phone','whatsapp','account','connect'],ua+': no install row'+(ua==='iphone'?', no push in a Safari tab':''));
  await page.locator('[data-setup-go="phone"]').click();
  assert.deepEqual(await page.evaluate(()=>window.__opened),[[store,'_blank','noopener']]);
  await fits(page,ua);await context.close()}
 // Inside the phone app: neither the phone app, nor the browser's notifications, nor installing.
 {reset();const {context,page}=await open({width:390,height:844,ua:'phoneApp'});
  assert.deepEqual(await steps(page),['whatsapp','account','connect']);await context.close()}
 // Firefox can't install: no install row.
 {reset();const {context,page}=await open({ua:'firefox',noInstall:true});
  assert.deepEqual(await steps(page),['phone','push','whatsapp','account','connect']);await context.close()}
 // Notifications blocked or turned off in Settings: no row for them.
 for(const o of [{perm:'denied'},{off:true}]){reset();const {context,page}=await open({mode:'standalone',...o});
  if(o.off){await page.evaluate(()=>{localStorage.setItem('push-off','1');deviceRender()})}
  assert.ok(!(await steps(page)).includes('push'),JSON.stringify(o));await context.close()}
 // Self-hosted: WhatsApp and another account sign in from a terminal there, so only the rows the dashboard can do.
 {reset();manage='';const {context,page}=await open({mode:'standalone'});
  assert.deepEqual(await steps(page),['phone','push','install','connect']);await context.close()}
 // Microsoft mail: another Microsoft account
 {reset();setup={...FRESH,add:'microsoft'};const {context,page}=await open({mode:'standalone'});
  assert.deepEqual((await card(page)).rows.find(r=>r[0]==='account'),['account','Add another Microsoft account','Add']);await context.close()}

 // What setup left out (state.setup_hints) fills in after the steps, linked to its setup step.
 {reset();setup={...FRESH,phones:1,whatsapp:true,dismissed:['account','install']};manage='https://app.example.test/setup';
  setupHints=[{id:'source-github',title:'Connect GitHub?',text:'GitHub mails you often.',href:'https://app.example.test/setup#source-github',button:'Connect'}];
  const {context,page}=await open({mode:'standalone',perm:'granted',sub:true});await opened(page);
  assert.deepEqual(await steps(page),['phone','push','whatsapp','connect','hint-source-github']);
  await page.locator('[data-setup-go="hint-source-github"]').click();
  assert.deepEqual(await page.evaluate(()=>window.__opened),[['https://app.example.test/setup#source-github','_blank','noopener']]);
  await page.locator('[data-setup-dismiss="hint-source-github"]').click();await page.waitForFunction(()=>!document.querySelector('[data-step="hint-source-github"]'));
  assert.deepEqual(actions.filter(a=>a.action==='setup_dismiss').at(-1),{action:'setup_dismiss',args:{step:'hint-source-github'}});
  await context.close()}

 // From the first visit, but never while setting up: no source yet, or the first look still running.
 {reset();connectors=[];const {context,page}=await open();
  assert.equal((await card(page)).shown,false,'no source yet');
  connectors=[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}];await page.evaluate(()=>refresh());
  assert.equal((await card(page)).shown,true,'right away, no first Do it needed');
  await context.close()}

 // Storage blocked: the page still works.
 {reset();const {context,page}=await open({mode:'standalone',blockStorage:true});assert.ok((await card(page)).shown);await context.close()}

 // The site's demo: in a frame, without a service worker. No card unless the demo gives fixed rows (setup_card.demo);
 // then those rows, and their buttons do nothing.
 {reset();const {context,page}=await open({url:base+'frame'});const frame=page.frames().find(f=>f!==page.mainFrame());
  await frame.locator('#task-'+'ab'.repeat(8)).waitFor();await frame.evaluate(()=>{__installPrompt();deviceRender()});
  assert.equal(await frame.evaluate(()=>document.querySelector('#setup-card').hidden),true);
  assert.deepEqual(await frame.evaluate(()=>window.__log),[]);
  setup={demo:true,rows:[{id:'phone',done:true},{id:'push'},{id:'whatsapp'},{id:'install',done:true},{id:'account'}]};
  await frame.evaluate(()=>refresh());await frame.locator('#setup-card:not([hidden])').waitFor();
  assert.equal(await frame.evaluate(()=>document.querySelector('.setup-head').innerText.replace(/\s+/g,' ').trim()),'Get more out of The Machine 2 of 5 done');
  actions.length=0;await frame.locator('[data-setup-go="push"]').click();await frame.locator('[data-setup-dismiss="whatsapp"]').click();
  assert.deepEqual(actionNames(),[]);assert.deepEqual(await frame.evaluate(()=>window.__log),[],'nothing asked');
  await context.close()}

 // Settings, General, This device: the same controls for good.
 {reset();const {context,page}=await open({mode:'standalone',perm:'denied'});
  const s=await settings(page);assert.match(s.app,/Installed/);assert.match(s.push,/Blocked in this browser\. Click the icon left of the address, then allow Notifications\./);
  await context.close()}

 assert.deepEqual(errors,[]);
 console.log('setup card dashboard ok');
}finally{await browser?.close();server.close()}
