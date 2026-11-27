import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {execFileSync} from 'node:child_process';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Settings, Apps (was AIs): The Machine apps on top, iPhone and iPad (App Store) and Android (Google Play), each a link
// to its store in a new tab, then ChatGPT and Claude. A phone's browser shows its own store only; the phone app shows
// neither (no Google Play inside the iPhone app); a Machine without store links shows no section. An old #settings/ai
// link opens Apps. A computer's browser also gets the desktop app (state.desktop_app, as machine/delivery/desk.py app()
// makes it from the browser's User-Agent): Windows, Mac and Linux, each a Download link in a new tab, this computer's
// filled and marked This computer, Linux with a line on its .deb and PKGBUILD; nothing on a phone, in the phone app or
// in the desktop app. Installing the dashboard from the browser is in Settings, General, This device only. One browser,
// one page per device: light and dark are the same page with its color scheme switched.
// Under the stores, how the phone app signs in (state.notify.phone_app): with the account when hosted or on The Machine
// Network; off the Network, folded under "Not on the Network?", a code to scan (not on a phone) and the address to type.
// This is the one place for the phone app: Settings, General, This device has no Phone app row.
// Every wait is for the page's own state (the status in, the rows drawn), never a fixed time. SHOTS=<folder> saves screenshots.
const IOS='https://apps.apple.com/app/id6829875215',PLAY='https://play.google.com/store/apps/details?id=computer.themachine.app';
const IPHONE='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
const ANDROID='Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36';
const MAC_SAFARI='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15';
const WINDOWS_EDGE='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0';
const LINUX_FIREFOX='Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0';
const CHROMEBOOK='Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36';
// The desktop app as the Machine hands it to a browser with this User-Agent (desk.app), once per agent
const deskFor=new Map(),desktopApp=ua=>{if(!deskFor.has(ua))deskFor.set(ua,JSON.parse(execFileSync('python3',['-c','import json,sys;from machine.delivery import desk;print(json.dumps(desk.app(sys.argv[1])))',ua||''],{cwd:new URL('..',import.meta.url)}).toString()));return deskFor.get(ua)};
const DL='https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-';
const DESK_FILES={windows:DL+'setup.exe',mac:DL+'mac.zip',linux:DL+'x86_64.AppImage'};
const STORE={published:true,ios:IOS,android:PLAY,phones:0};
const OWN='https://machine.example.ts.net/',OWN_LINK='computer.themachine.app://connect?u='+encodeURIComponent(OWN);
// A real code for the connect link (qr.py, as push.phone_app makes it)
const OWN_QR=JSON.parse(execFileSync('python3',['-c','import json,qr,sys;print(json.dumps(qr.encode(sys.argv[1])))',OWN_LINK],{cwd:new URL('..',import.meta.url)}).toString());
const HOSTED={hosted:true},SELF={hosted:false,url:OWN,link:OWN_LINK,qr:OWN_QR};
const SIGNIN='The app signs in with your account.',SIGNIN_NET='The app signs in with your account on The Machine Network.';
const dashboard=await dashboardPage();
let store=STORE,phoneApp=HOSTED;
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({desktop_app:desktopApp(req.headers['user-agent']),suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],phone_app_store:store,notify:{app_push_ready:true,prefs:{},app_devices:[],push_devices:0,phone_app:phoneApp}}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='ai_connections'){res.end(JSON.stringify({connections:[],areas:['work'],reach:{hosted:true,shared:'https://mcp.themachine.computer/mcp',address:'https://pat.mcp.themachine.computer/mcp'}}));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const stores=page=>page.locator('#apps-list [data-app-store]').evaluateAll(rows=>rows.map(r=>r.dataset.appStore));
const desks=page=>page.locator('#apps-list [data-app-desk]').evaluateAll(rows=>rows.map(r=>r.dataset.appDesk));
// Each desktop app row: [system, its name, its lines, its link's text, href, filled (not .alt)]
const deskRows=page=>page.locator('#apps-list [data-app-desk]').evaluateAll(rows=>rows.map(r=>{const a=r.querySelector('a.store-badge');
 return [r.dataset.appDesk,r.querySelector('strong').innerText,[...r.querySelectorAll('small')].map(s=>s.innerText),a.innerText.trim(),a.getAttribute('href'),!a.classList.contains('alt'),a.target,a.rel]}));
// What a Chromium browser hands the page when it offers to install: the dashboard keeps it for its own Install button
const offerInstall=page=>page.evaluate(()=>{const e=new Event('beforeinstallprompt',{cancelable:true});window.__prompted=0;
 e.prompt=()=>{window.__prompted++};e.userChoice=Promise.resolve({outcome:'accepted'});dispatchEvent(e)});
const selected=page=>page.locator('#settings-tabs [aria-selected="true"]').innerText();
// A fresh load of url, ready once this load's status is drawn (the store rows come with it) and the AIs' part is in
async function open(page,url){await page.goto('about:blank');await page.goto(url);
 await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});await page.locator('#ai-official a[data-ai-claude]').waitFor()}
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // The desktop app's window (window.machineDesktop): an app already, with notifications and downloads of its own
 {store=STORE;const context=await browser.newContext({viewport:{width:1024,height:640}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.addInitScript(()=>Object.defineProperty(window,'machineDesktop',{value:Object.freeze({version:1})}));
  await open(page,base+'/#settings/apps');
  assert.deepEqual(await stores(page),['ios','android']);assert.deepEqual(await desks(page),[],'no desktop app inside it');
  assert.deepEqual(await page.evaluate(()=>[document.querySelector('#device-app').hidden,document.querySelector('#device-push').hidden]),[true,true]);
  await page.evaluate(()=>{location.hash='#settings/notify'});
  const more=page.locator('#notify-more');await more.waitFor();
  assert.equal(await more.innerText(),'This device\nChoose in the app’s Settings: the robot or notifications.');assert.equal(await more.locator('button').count(),0);
  for(const scheme of shots?['light','dark']:[]){await page.emulateMedia({colorScheme:scheme});await more.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/desktop-notifications-${scheme}.png`})}
  for(const [detail,text] of [[{saved:'a.pdf'},'Saved to Downloads'],[{failed:'a.pdf'},'Couldn’t save it.']]){
   await page.evaluate(d=>dispatchEvent(new CustomEvent('machinedesktop',{detail:d})),detail);
   await page.locator('#toast.show',{hasText:text}).waitFor()}
  await context.close()}
 for(const [name,ua,width,want] of [['computer',null,1440,['ios','android']],['narrow',null,390,['ios','android']],['iphone',IPHONE,390,['ios']],['android',ANDROID,390,['android']],['in-app',IPHONE+' TheMachineApp/1.0',390,[]]]){
  store=STORE;
  const context=await browser.newContext({viewport:{width,height:844},...(ua?{userAgent:ua}:{})}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await open(page,base+'/#settings/apps');
  for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});
   assert.equal(await selected(page),'Apps');
   assert.deepEqual(await stores(page),want,name);
   // a computer (this headless browser says Linux): the three systems, Linux its own
   assert.deepEqual(await desks(page),['computer','narrow'].includes(name)?['windows','mac','linux']:[],name+': desktop app');
   if(['computer','narrow'].includes(name)){
    assert.deepEqual((await deskRows(page)).map(r=>r.slice(0,6)),[['windows','Windows',[],'Download',DESK_FILES.windows,false],['mac','Mac',[],'Download',DESK_FILES.mac,false],
     ['linux','Linux',['This computer','Also a .deb and a PKGBUILD. Learn more'],'Download',DESK_FILES.linux,true]],name);
    assert.equal(await page.locator('#apps-list [data-app-desk="linux"] a.learn').getAttribute('href'),'https://themachine.computer/help/desktop-app#linux');
    for(const box of await page.locator('#apps-list [data-app-desk] a.store-badge').evaluateAll(as=>as.map(a=>a.getBoundingClientRect().toJSON())))assert.ok(box.x>=0&&box.right<=width,`${name}: Download inside the screen`)}
   assert.equal(await page.locator('#settings-apps').isVisible(),want.length>0||['computer','narrow'].includes(name),name+': the section');
   for(const k of want){const a=page.locator(`#apps-list [data-app-store="${k}"] a`);
    assert.equal(await a.getAttribute('href'),k==='ios'?IOS:PLAY);assert.equal(await a.getAttribute('target'),'_blank');assert.match(await a.getAttribute('rel'),/noopener/);
    assert.equal((await a.innerText()).trim(),k==='ios'?'App Store':'Google Play');
    const box=await a.boundingBox();assert.ok(box.x>=0&&box.x+box.width<=width,`${name}: ${k} inside the screen`)}
   if(want.length){
    assert.equal(await page.locator('#settings-apps .section-head p').innerText(),'Your to-dos on your phone and computer, with a ping when something needs you.');
    assert.equal(await page.locator('#settings-apps h2').innerText(),'The Machine apps');
    // the apps come first, above ChatGPT and Claude
    const [apps,ai]=await Promise.all(['#settings-apps','#ai-official'].map(s=>page.locator(s).boundingBox()));assert.ok(apps.y<ai.y,name+': apps on top')}
   assert.deepEqual(await page.locator('#ai-official small').allInnerTexts(),['One click from ChatGPT’s plugins.','One click from Claude’s directory.','In Claude, add it under Customize, Skills.']);
   // the skill: the claude.ai zip each desktop release carries
   assert.equal(await page.locator('#ai-official a[data-ai-skill]').getAttribute('href'),'https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-skill.zip');
   // how the app signs in, under the stores; nothing without a store (inside the app)
   assert.equal(await page.locator('#apps-signin').isVisible(),want.length>0,name+': sign-in line');
   if(want.length)assert.equal(await page.locator('#apps-signin').innerText(),SIGNIN);
   assert.ok(!(await page.locator('#settings').innerText()).includes('—'),'no em dashes');
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${name}: no sideways scroll`);
   if(shots)await page.screenshot({path:`${shots}/apps-${name}-${scheme}.png`,fullPage:true})}
  if(name==='computer'){
   // No store links on this Machine: the desktop app alone, ChatGPT and Claude stay
   store=null;await open(page,base+'/#settings/apps');
   assert.equal(await stores(page).then(r=>r.length),0);assert.deepEqual(await desks(page),['windows','mac','linux']);assert.equal(await page.locator('#settings-apps').isVisible(),true);assert.equal(await selected(page),'Apps');
   // Installing from the browser offers nothing here: Install app in Settings, General, This device opens its prompt
   await offerInstall(page);await page.evaluate(()=>{location.hash='#settings/general'});
   await page.locator('#device-app button',{hasText:/^Install app$/}).click();
   await page.locator('#toast.show',{hasText:'Installed.'}).waitFor();assert.equal(await page.evaluate(()=>window.__prompted),1);
   await page.evaluate(()=>{location.hash='#settings/apps'});await page.locator('#apps-list [data-app-desk]').first().waitFor();
   assert.equal(await page.locator('#apps-list button').count(),0,'no Install in Apps');
   await page.evaluate(()=>localStorage.removeItem('app-installed'));
   // a tab kept from before the rename, and an old AIs link, open Apps
   store=STORE;await page.evaluate(()=>localStorage.setItem('settings-tab','ai'));await open(page,base+'/#settings');
   assert.equal(await selected(page),'Apps');assert.deepEqual(await stores(page),want);
   await open(page,base+'/#settings/ai');assert.equal(await selected(page),'Apps');
   await page.waitForFunction(()=>location.hash==='#settings/apps')}
  await context.close();
 }
 // Self-hosted, off The Machine Network: the Network line, and folded under it the code and the address. A phone's
 // browser gets the address only (it can't scan its own screen). Shots with the fold open.
 for(const [name,ua,width] of [['computer',null,1440],['narrow',null,390],['iphone',IPHONE,390]]){
  store=STORE;phoneApp=SELF;
  const context=await browser.newContext({viewport:{width,height:844},...(ua?{userAgent:ua}:{})}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await open(page,base+'/#settings/apps');
  const note=page.locator('#apps-signin');
  assert.equal(await note.locator('details').getAttribute('open'),null,name+': folded');
  assert.equal((await note.innerText()).split('\n')[0],SIGNIN_NET);
  await note.locator('summary',{hasText:'Not on the Network?'}).click();
  assert.equal(await note.locator('code.phone-url').innerText(),OWN);
  assert.equal(await note.locator('svg').count(),name==='iphone'?0:1,name+': the code');
  if(name!=='iphone')assert.ok((await note.innerText()).includes('Install the app, then scan this with the phone’s camera.'));
  for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${name}: no sideways scroll`);
   if(shots)await page.locator('#settings-apps').screenshot({path:`${shots}/apps-self-hosted-${name}-${scheme}.png`})}
  await context.close();
 }
 // Settings, General: This device has no Phone app row (Apps has it), hosted or not
 for(const app of [HOSTED,SELF])for(const width of [1440,390]){
  store=STORE;phoneApp=app;
  const context=await browser.newContext({viewport:{width,height:844}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#settings/general');await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
  await page.locator('#settings h2',{hasText:/^This device$/}).waitFor();assert.equal(await selected(page),'General');
  for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});
   assert.equal(await page.locator('#device-phone').count(),0,'no Phone app row');
   const text=await page.locator('#settings').innerText();
   for(const gone of ['Phone app','Get the app','The app signs in','Not on the Network?'])assert.ok(!text.includes(gone),`General: no ${gone}`);
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`general ${width}: no sideways scroll`);
   if(shots&&app===HOSTED)await page.screenshot({path:`${shots}/general-${width}-${scheme}.png`,fullPage:true})}
  await context.close();
 }
 phoneApp=HOSTED;
 // The desktop app per system, at both widths and in both color schemes: Windows (Edge), a Mac (Safari) and Linux
 // (Firefox) each fill their own and mark it This computer; a Chromebook (no desktop app for it) and the dashboard
 // installed from the browser get all three, none marked
 store=STORE;
 const MARK=['This computer'],MORE='Also a .deb and a PKGBUILD. Learn more';
 for(const [name,ua,mine] of [['windows',WINDOWS_EDGE,'windows'],['mac',MAC_SAFARI,'mac'],['linux',LINUX_FIREFOX,'linux'],['chromebook',CHROMEBOOK,null],['installed',WINDOWS_EDGE,'windows']])for(const width of [1440,390]){
  const context=await browser.newContext({viewport:{width,height:844},userAgent:ua}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  if(name==='installed')await page.addInitScript(()=>Object.defineProperty(Navigator.prototype,'standalone',{get:()=>true}));
  page.on('pageerror',e=>errors.push(e.message));
  await open(page,base+'/#settings/apps');
  for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});
   assert.deepEqual(await stores(page),['ios','android'],name);
   const rows=await deskRows(page);
   assert.deepEqual(rows.map(r=>[r[0],r[2],r[5]]),[['windows',mine==='windows'?MARK:[],mine==='windows'],['mac',mine==='mac'?MARK:[],mine==='mac'],['linux',mine==='linux'?[...MARK,MORE]:[MORE],mine==='linux']],name);
   for(const r of rows){assert.equal(r[4],DESK_FILES[r[0]]);assert.equal(r[3],'Download');assert.equal(r[6],'_blank');assert.match(r[7],/noopener/)}
   for(const box of await page.locator('#apps-list [data-app-desk] a.store-badge').evaluateAll(as=>as.map(a=>a.getBoundingClientRect().toJSON())))assert.ok(box.x>=0&&box.right<=width,`${name} ${width}: Download inside the screen`);
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${name} ${width}: no sideways scroll`);
   if(shots)await page.locator('#settings-apps').screenshot({path:`${shots}/apps-desktop-${name}-${width}-${scheme}.png`})}
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('settings apps dashboard ok');
