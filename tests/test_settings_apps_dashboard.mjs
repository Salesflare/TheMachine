import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, Apps (was AIs): The Machine apps on top, iPhone and iPad (App Store) and Android (Google Play), each a link
// to its store in a new tab, then ChatGPT and Claude. A phone's browser shows its own store only; the phone app shows
// neither (no Google Play inside the iPhone app); a Machine without store links shows no section. An old #settings/ai
// link opens Apps. SHOTS=<folder> saves screenshots.
const IOS='https://apps.apple.com/app/id6829875215',PLAY='https://play.google.com/store/apps/details?id=computer.themachine.app';
const IPHONE='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
const ANDROID='Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36';
const dashboard=await dashboardPage();
let store={published:true,ios:IOS,android:PLAY,phones:0};
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],phone_app_store:store}));return}
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
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [name,ua,width,want] of [['computer',null,1440,['ios','android']],['narrow',null,390,['ios','android']],['iphone',IPHONE,390,['ios']],['android',ANDROID,390,['android']],['in-app',IPHONE+' TheMachineApp/1.0',390,[]]])for(const scheme of ['light','dark']){
  store={published:true,ios:IOS,android:PLAY,phones:0};
  const context=await browser.newContext({viewport:{width,height:844},colorScheme:scheme,...(ua?{userAgent:ua}:{})}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#settings/apps');await page.locator('#ai-official a[data-ai-claude]').waitFor();
  assert.equal(await page.locator('#settings-tabs [aria-selected="true"]').innerText(),'Apps');
  assert.deepEqual(await stores(page),want,name);
  assert.equal(await page.locator('#settings-apps').isVisible(),want.length>0,name+': the section');
  for(const k of want){const a=page.locator(`#apps-list [data-app-store="${k}"] a`);
   assert.equal(await a.getAttribute('href'),k==='ios'?IOS:PLAY);assert.equal(await a.getAttribute('target'),'_blank');assert.match(await a.getAttribute('rel'),/noopener/);
   assert.equal((await a.innerText()).trim(),k==='ios'?'App Store':'Google Play');
   const box=await a.boundingBox();assert.ok(box.x>=0&&box.x+box.width<=width,`${name}: ${k} inside the screen`)}
  if(want.length){
   assert.equal(await page.locator('#settings-apps h2').innerText(),'The Machine apps');
   // the apps come first, above ChatGPT and Claude
   const [apps,ai]=await Promise.all(['#settings-apps','#ai-official'].map(s=>page.locator(s).boundingBox()));assert.ok(apps.y<ai.y,name+': apps on top')}
  assert.deepEqual(await page.locator('#ai-official small').allInnerTexts(),['One click from ChatGPT’s plugins.','One click from Claude’s directory.']);
  assert.ok(!(await page.locator('#settings').innerText()).includes('—'),'no em dashes');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${name}: no sideways scroll`);
  if(shots)await page.screenshot({path:`${shots}/apps-${name}-${scheme}.png`,fullPage:true});
  // No store links on this Machine: no section, ChatGPT and Claude stay
  if(name==='computer'&&scheme==='light'){store=null;await page.reload();await page.locator('#ai-official a[data-ai-claude]').waitFor();
   assert.equal(await page.locator('#settings-apps').isVisible(),false);assert.equal(await page.locator('#settings-tabs [aria-selected="true"]').innerText(),'Apps');
   // an old AIs link, and a tab kept from before the rename, open Apps
   store={published:true,ios:IOS,android:PLAY,phones:0};
   await page.evaluate(()=>localStorage.setItem('settings-tab','ai'));await page.goto(base+'/#settings');await page.locator('#apps-list [data-app-store]').first().waitFor();
   assert.equal(await page.locator('#settings-tabs [aria-selected="true"]').innerText(),'Apps');
   await page.goto('about:blank');await page.goto(base+'/#settings/ai');await page.locator('#apps-list [data-app-store]').first().waitFor();
   assert.equal(await page.evaluate(()=>location.hash),'#settings/apps')}
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('settings apps dashboard ok');
