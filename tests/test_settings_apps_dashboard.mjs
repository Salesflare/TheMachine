import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {execFileSync} from 'node:child_process';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Settings, Apps (was AIs): The Machine apps on top, iPhone and iPad (App Store) and Android (Google Play), each a link
// to its store in a new tab, then ChatGPT and Claude. A phone's browser shows its own store only; the phone app shows
// neither (no Google Play inside the iPhone app); a Machine without store links shows no section. An old #settings/ai
// link opens Apps. A computer's browser also gets Computer (installing the dashboard from the browser, This device's own
// prompt and steps): Install when the browser offers it, the browser's steps when not, and nothing on a phone, in the
// phone app or once it runs as the installed app. One browser, one page per device: light and dark are the same page with its color scheme switched.
// Under the stores, how the phone app signs in (state.notify.phone_app): with the account when hosted or on The Machine
// Network; off the Network, folded under "Not on the Network?", a code to scan (not on a phone) and the address to type.
// This is the one place for the phone app: Settings, General, This device has no Phone app row.
// Every wait is for the page's own state (the status in, the rows drawn), never a fixed time. SHOTS=<folder> saves screenshots.
const IOS='https://apps.apple.com/app/id6829875215',PLAY='https://play.google.com/store/apps/details?id=computer.themachine.app';
const IPHONE='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
const ANDROID='Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36';
const MAC_SAFARI='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15';
const CHROME_STEPS='Find Install in the browser’s menu, or the icon in the address bar.',SAFARI_STEPS='In Safari’s menu bar: File, then Add to Dock.';
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
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],phone_app_store:store,notify:{app_push_ready:true,prefs:{},app_devices:[],push_devices:0,phone_app:phoneApp}}));return}
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
const computer=page=>page.locator('#apps-list [data-app-computer]').evaluateAll(rows=>rows.map(r=>r.dataset.appComputer));
// What a Chromium browser hands the page when it offers to install: the dashboard keeps it for its own Install button
const offerInstall=page=>page.evaluate(()=>{const e=new Event('beforeinstallprompt',{cancelable:true});window.__prompted=0;
 e.prompt=()=>{window.__prompted++};e.userChoice=Promise.resolve({outcome:'accepted'});dispatchEvent(e)});
const selected=page=>page.locator('#settings-tabs [aria-selected="true"]').innerText();
// A fresh load of url, ready once this load's status is drawn (the store rows come with it) and the AIs' part is in
async function open(page,url){await page.goto('about:blank');await page.goto(url);
 await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});await page.locator('#ai-official a[data-ai-claude]').waitFor()}
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [name,ua,width,want] of [['computer',null,1440,['ios','android']],['narrow',null,390,['ios','android']],['iphone',IPHONE,390,['ios']],['android',ANDROID,390,['android']],['in-app',IPHONE+' TheMachineApp/1.0',390,[]]]){
  store=STORE;
  const context=await browser.newContext({viewport:{width,height:844},...(ua?{userAgent:ua}:{})}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await open(page,base+'/#settings/apps');
  for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});
   assert.equal(await selected(page),'Apps');
   assert.deepEqual(await stores(page),want,name);
   assert.deepEqual(await computer(page),['computer','narrow'].includes(name)?['steps']:[],name+': Computer');
   if(['computer','narrow'].includes(name)){assert.equal(await page.locator('#apps-list [data-app-computer] strong').innerText(),'Computer');
    assert.equal(await page.locator('#apps-list [data-app-computer] small').innerText(),CHROME_STEPS)}
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
   assert.deepEqual(await page.locator('#ai-official small').allInnerTexts(),['One click from ChatGPT’s plugins.','One click from Claude’s directory.']);
   // how the app signs in, under the stores; nothing without a store (inside the app)
   assert.equal(await page.locator('#apps-signin').isVisible(),want.length>0,name+': sign-in line');
   if(want.length)assert.equal(await page.locator('#apps-signin').innerText(),SIGNIN);
   assert.ok(!(await page.locator('#settings').innerText()).includes('—'),'no em dashes');
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${name}: no sideways scroll`);
   if(shots)await page.screenshot({path:`${shots}/apps-${name}-${scheme}.png`,fullPage:true})}
  if(name==='computer'){
   // No store links on this Machine: Computer alone, ChatGPT and Claude stay
   store=null;await open(page,base+'/#settings/apps');
   assert.equal(await stores(page).then(r=>r.length),0);assert.deepEqual(await computer(page),['steps']);assert.equal(await page.locator('#settings-apps').isVisible(),true);assert.equal(await selected(page),'Apps');
   // The browser offers to install: Install opens its own prompt, and once installed the row goes
   await offerInstall(page);await page.locator('#apps-list [data-app-computer="install"] button',{hasText:/^Install$/}).click();
   await page.locator('#apps-list [data-app-computer]').waitFor({state:'detached'});
   assert.equal(await page.evaluate(()=>window.__prompted),1);assert.equal(await page.locator('#settings-apps').isVisible(),false);
   await page.locator('#toast.show',{hasText:'Installed.'}).waitFor();
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
 // Computer, per browser, at both widths and in both color schemes: Chromium with the install offered (Install), Safari
 // on a Mac (its menu's steps), and the installed app itself (no row)
 store=STORE;
 for(const [name,ua] of [['chrome',null],['safari',MAC_SAFARI],['installed',null]])for(const width of [1440,390]){
  const context=await browser.newContext({viewport:{width,height:844},...(ua?{userAgent:ua}:{})}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  if(name==='installed')await page.addInitScript(()=>Object.defineProperty(Navigator.prototype,'standalone',{get:()=>true}));
  page.on('pageerror',e=>errors.push(e.message));
  await open(page,base+'/#settings/apps');
  if(name==='chrome'){await offerInstall(page);await page.locator('#apps-list [data-app-computer="install"]').waitFor()}
  for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});
   assert.deepEqual(await stores(page),['ios','android'],name);
   if(name==='installed'){assert.deepEqual(await computer(page),[],name);continue}
   const row=page.locator('#apps-list [data-app-computer]');
   assert.equal(await row.locator('strong').innerText(),'Computer');
   if(name==='chrome'){assert.equal(await row.locator('small').innerText(),'Pin it to your taskbar or dock.');
    const b=row.locator('button');assert.equal(await b.innerText(),'Install');const box=await b.boundingBox();assert.ok(box.x>=0&&box.x+box.width<=width,`${name} ${width}: Install inside the screen`)}
   else{assert.equal(await row.locator('small').innerText(),SAFARI_STEPS);assert.equal(await row.locator('button').count(),0)}
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${name} ${width}: no sideways scroll`);
   if(shots)await page.locator('#settings-apps').screenshot({path:`${shots}/apps-computer-${name}-${width}-${scheme}.png`})}
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('settings apps dashboard ok');
