import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Settings in tabs: Account, General, Notifications (with Work hours), Writing, Skills, Apps (the phone apps and connected AIs), Model, each part of Settings in one. A Machine linked
// to a control plane account (hosted, or self-hosted and paired) gets Account first (test_account_dashboard.mjs); one
// with no account has none. A tab with nothing to show is
// left out. Links open a tab (#settings/skills, #settings=model), the URL follows the tab, and the last tab is kept.
// On a desktop (1440x900, 1440x700) every tab shows in full, none cut off at an edge, a second row if they don't fit. On a
// phone (390) it scrolls sideways with a fade at its edge, the open tab scrolled into view. The page stays inside the screen.
const dashboard=await dashboardPage();
const hours={days:[0,1,2,3,4],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC',saveable:true};
let hosted=true,paired=false,model=true,addrs=false;
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],hours,
  signatures:[{account_id:'mail',email:'owner@example.org',service:'gmail',html:'<b>Owner</b>',source:'detected',saveable:true}],skills:{skills:[],waiting:0,targets:[],folder:'skills/the-machine'},
  ...(model?{model_usage:[],model_status:{model:'openai/example-model',provider:'openai',windows:[],checked_at:new Date().toISOString()}}:{}),
  ...(hosted?{manage_url:'https://account.example/setup',account_url:'https://account.example/account'}:{}),...(paired?{fleet:{on:true,waiting:0},account_url:'https://app.themachine.computer/account'}:{}),
  ...(addrs?{own_addresses:{yours:[{address:'owner@example.org',sources:['Connected']}],maybe:[],team:[],not_mine:[],domains:[{domain:'example.org'}]}}:{})}));return}
 if(url.pathname==='/_machine/support-access'){res.end(JSON.stringify({until:new Date(Date.now()+36e5).toISOString(),hours:24,accesses:[]}));return}  // on: Settings, Security shows it
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const tabs=page=>page.locator('#settings-tabs>:not([hidden])').allInnerTexts();
const selected=page=>page.locator('#settings-tabs [aria-selected="true"]').innerText();
const visible=(page,sel)=>page.locator(sel).isVisible();
// The footer's Help goes to the help article for what's on screen
const help=page=>page.locator('#help-link').getAttribute('href'),HELP='https://themachine.computer/help/';
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[1440,700],[390,900]]){
  hosted=true;model=true;
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
  await navClick(page.locator('#open-settings'));await page.locator('#settings-tabs [data-settings-tab="account"]:not([hidden])').waitFor();
  // hosted: Security holds Support access while it's on; it shows once opening Settings has asked for its state, so wait for it
  await page.locator('#settings-tabs [data-settings-tab="security"]:not([hidden])').waitFor();
  assert.deepEqual(await tabs(page),['Account','General','Security','Activity','Notifications','Writing','Skills','Apps','Model']);
  // Account first, a tab like the others; General has this device, and no account card (it's in Account now).
  assert.equal(await selected(page),'Account');assert.equal(await page.evaluate(()=>location.hash),'#settings/account');
  assert.equal(await visible(page,'#settings-acct'),true);assert.equal(await visible(page,'#theme-toggle'),false);
  await page.locator('#settings-tabs [data-settings-tab="general"]').click();
  assert.equal(await visible(page,'#theme-toggle'),true);assert.equal(await visible(page,'#settings-account'),false);assert.equal(await visible(page,'#settings-acct'),false);
  for(const sel of ['#hours','#signatures','#settings-skills','#model-panel'])assert.equal(await visible(page,sel),false,sel);
  // Language and region: its dropdowns share one width and the same left and right edge
  const loc=await page.evaluate(()=>[...new Set([...document.querySelectorAll('.locale-list select')].filter(s=>s.checkVisibility()).map(s=>{const r=s.getBoundingClientRect();return Math.round(r.left)+'-'+Math.round(r.right)}))]);
  assert.ok(loc.length<=1,`Language and region's dropdowns line up at ${width}px: ${loc}`);
  assert.equal(await help(page),HELP+'settings');
  // Each tab shows its own part.
  for(const [tab,sel] of [['notify','#hours'],['writing','#signatures'],['writing','#settings-voices'],['skills','#settings-skills'],['model','#model-panel']]){
   await page.locator(`#settings-tabs [data-settings-tab="${tab}"]`).click();
   assert.equal(await visible(page,sel),true,sel);assert.equal(await visible(page,'#theme-toggle'),false);
   assert.equal(await page.evaluate(()=>location.hash),'#settings/'+tab);
   assert.equal(await help(page),HELP+({notify:'notifications'}[tab]||tab))}
  // The pills are one height and one row inside the screen, the open tab in full. On a desktop every tab shows (in a
  // longer language they take a second row); on a phone the row scrolls sideways.
  const row=await page.evaluate(()=>{const bar=document.querySelector('#settings-tabs'),box=bar.getBoundingClientRect(),r=[...bar.children].filter(e=>!e.hidden).map(e=>e.getBoundingClientRect()),
   inside=x=>x.left>=box.left-.5&&x.right<=box.right+.5;
   return {top:new Set(r.map(x=>Math.round(x.top))).size,height:new Set(r.map(x=>Math.round(x.height))).size,fits:document.documentElement.scrollWidth<=innerWidth,overflow:getComputedStyle(bar).overflowX,
    open:inside(bar.querySelector('[aria-selected="true"]').getBoundingClientRect()),all:r.every(inside)}});
  const desk=width>=1024;
  // (a desktop may take a second row: that depends on the fonts it has)
  assert.deepEqual({...row,top:desk?Math.min(row.top,1):row.top},{top:1,height:1,fits:true,overflow:desk?'visible':'auto',open:true,all:desk},`${width}x${height} `+JSON.stringify(row));
  if(desk)assert.ok(row.top<=2,'at most two rows of tabs at '+width);
  if(process.env.SHOTS)await page.screenshot({path:`${process.env.SHOTS}/settings-tabs-${width}x${height}.png`});
  // The last tab is kept; a link opens another; leaving Settings drops the link.
  await page.reload();await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});await page.locator('#settings:not([hidden])').waitFor();
  assert.equal(await selected(page),'Model');
  await navClick(page.locator('nav [data-tab="feedback"]'));assert.equal(await page.evaluate(()=>location.hash),'');assert.equal(await help(page),HELP+'dashboard');
  await navClick(page.locator('#open-settings'));assert.equal(await selected(page),'Model');
  await page.goto(base+'/#settings/skills');await page.locator('#settings-skills:visible').waitFor();assert.equal(await selected(page),'Skills');
  await page.goto(base+'/#settings=hours');await page.locator('#hours:visible').waitFor();assert.equal(await selected(page),'Notifications');  // an old Work hours link
  await page.goto(base+'/#settings/ai');await page.locator('#settings-ai:visible').waitFor();assert.equal(await selected(page),'Apps');  // an old AIs link
  assert.equal(await page.evaluate(()=>location.hash),'#settings/apps');assert.equal(await help(page),HELP+'ai-connections');
  await page.evaluate(()=>{location.hash='#settings/writing'});await page.locator('#signatures:visible').waitFor();
  assert.equal(await page.locator('#settings').isVisible(),true);
  // On your own computer: no Account tab, and a tab with nothing in it (no model reported) is left out.
  hosted=false;model=false;await page.goto('about:blank');await page.goto(base+'/#settings/model');await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});await page.locator('#settings:not([hidden])').waitFor();
  assert.deepEqual(await tabs(page),['General','Activity','Notifications','Writing','Skills','Apps']);
  assert.equal(await selected(page),'General');assert.equal(await visible(page,'#settings-cloud'),true);
  // Self-hosted but paired with the Network: the Account tab too.
  paired=true;await page.goto('about:blank');await page.goto(base+'/#settings');await page.locator('#settings-tabs [data-settings-tab="account"]:not([hidden])').waitFor();
  assert.equal(await tabs(page).then(t=>t[0]),'Account');
  // Fleet's rows are rows like the others: a bold label and a control on the right
  await page.locator('#settings-tabs [data-settings-tab="general"]').click();await page.locator('#settings-fleet-rules:visible').waitFor();
  assert.deepEqual(await page.evaluate(()=>[...document.querySelectorAll('#settings-fleet .settings-list>div')].filter(r=>r.checkVisibility()).map(r=>{const s=r.querySelector(':scope>.grow>strong'),c=r.querySelector(':scope>:is(button,select)');return !!s&&!!c&&c.getBoundingClientRect().left>=s.getBoundingClientRect().right-1}).every(Boolean)),true);
  paired=false;
  // On your own computer with addresses found: an Account tab, and the account in short (Join the Network) first in it,
  // not also at the end of General
  addrs=true;await page.goto('about:blank');await page.goto(base+'/#settings/account');await page.locator('#settings-addresses:visible').waitFor();
  assert.equal(await tabs(page).then(t=>t[0]),'Account');assert.equal(await visible(page,'#settings-cloud'),true);
  assert.equal(await page.evaluate(()=>[...document.querySelectorAll('#settings>[data-stab="account"]:not([hidden])')].map(x=>x.id).join()),'settings-account-block,settings-addresses,settings-domains');
  await page.locator('#settings-tabs [data-settings-tab="general"]').click();assert.equal(await visible(page,'#settings-cloud'),false);
  addrs=false;
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('settings tabs dashboard ok');
}finally{await browser?.close();server.close()}
