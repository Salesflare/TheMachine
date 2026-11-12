import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// On a computer Browser shows the Machine's browser in the main area beside the sidebar (from 1024px) or under the top
// bar (a narrower window, like the desktop app on half a screen), with Full size, Open in new tab and close. The
// Browser row is the active one; another row, back and close leave it, and the viewer stays loaded meanwhile. On a
// phone, or without a viewer on the dashboard's own address, it stays a new tab.
const dashboard=await dashboardPage();
let embed='/browser/';const loads=[];
const card={id:'aaaaaaaaaaaaaaa1',title:'Reply to the venue',body:'Drafted a reply.',status:'prepared',scope:'work',created_at:new Date().toISOString(),event_ids:[1]};
const state=()=>({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},
 browser_link:'https://cp.example/open?to=browser',browser_embed:embed});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/browser/'){loads.push(url.pathname);res.setHeader('Content-Type','text/html');res.end('<body style="background:#123"><p id="viewer">viewer</p></body>');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);const row=page.locator('#open-browser');await row.waitFor();
 await row.click();
 const pane=page.locator('#browser-pane');await pane.waitFor();
 assert.equal(await page.locator('#bp-frame').getAttribute('src'),'/browser/');
 await page.frameLocator('#bp-frame').locator('#viewer').waitFor();
 assert.equal(await row.getAttribute('aria-current'),'page');
 assert.equal(await page.locator('nav button.active').count(),0);
 assert.equal(await page.locator('#inbox').isHidden(),true);
 assert.equal(await page.locator('#bp-tab').getAttribute('href'),'https://cp.example/open?to=browser');
 assert.equal(await page.locator('#bp-tab').getAttribute('target'),'_blank');
 assert.ok(page.url().endsWith('#browser'));
 const box=await page.locator('#bp-frame').boundingBox(),side=await page.locator('#app-side').boundingBox();
 assert.ok(box.x>=side.x+side.width-1&&box.height>800,'fills the main area beside the sidebar');
 // Another row leaves it; the viewer is not loaded again when it comes back
 await page.locator('nav [data-tab="feedback"]').click();
 assert.equal(await pane.isHidden(),true);assert.equal(await page.locator('#feedback').isHidden(),false);
 assert.equal(await row.getAttribute('aria-current'),'false');assert.ok(!page.url().includes('#browser'));
 await row.click();await pane.waitFor();assert.deepEqual(loads,['/browser/']);
 // Back returns to the view before
 await page.goBack();await pane.waitFor({state:'hidden'});assert.equal(await page.locator('#feedback').isHidden(),false);
 // Close too
 await row.click();await pane.waitFor();await page.locator('#bp-close').click();await pane.waitFor({state:'hidden'});
 assert.equal(await page.locator('#feedback').isHidden(),false);assert.equal(await row.getAttribute('aria-current'),'false');
 // Leaving through another row spends no Back: the one before it leaves the dashboard
 const hist=await context.newPage();hist.on('pageerror',e=>errors.push(e.message));await hist.goto('about:blank');await hist.goto(base);await hist.locator('#open-browser').click();
 await hist.locator('#browser-pane').waitFor();await hist.locator('nav [data-tab="feedback"]').click();await hist.waitForFunction(()=>!location.hash);
 await hist.goBack();assert.equal(hist.url(),'about:blank');
 // A computer's window made narrower while it is open: the pane stays, under the top bar, and fills what is left
 await hist.goto(base);await hist.locator('#open-browser').click();await hist.locator('#browser-pane').waitFor();
 await hist.setViewportSize({width:900,height:700});await new Promise(r=>setTimeout(r,300));
 assert.equal(await hist.locator('#browser-pane').isVisible(),true);
 {const f=await hist.locator('#bp-frame').boundingBox(),top=await hist.locator('.topbar').boundingBox();
  assert.ok(f.y>=top.y+top.height-1&&f.width===900&&Math.abs(f.y+f.height-700)<=1,JSON.stringify(f))}
 // Full size: the whole window, over the top bar; again goes back
 await hist.locator('#bp-full').click();assert.equal(await hist.locator('#bp-full').getAttribute('aria-pressed'),'true');
 {const p=await hist.locator('#browser-pane').boundingBox();assert.deepEqual([p.x,p.y,p.width,p.height],[0,0,900,700])}
 assert.equal(await hist.locator('#bp-full').textContent(),'Exit full size');
 await hist.locator('#bp-full').click();assert.equal(await hist.evaluate(()=>'bpFull' in document.documentElement.dataset),false);
 // Leaving it ends Full size
 await hist.locator('#bp-full').click();await hist.locator('#bp-close').click();await hist.locator('#browser-pane').waitFor({state:'hidden'});
 assert.equal(await hist.evaluate(()=>'bpFull' in document.documentElement.dataset),false);await hist.close();
 // Opened in a narrow window: the pane too, from the drawer, never a new tab or window
 const narrow=await browser.newContext({viewport:{width:900,height:700}});await narrow.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const n=await narrow.newPage();n.on('pageerror',e=>errors.push(e.message));await n.goto(base);await n.locator('#drawer-open').click();
 await n.locator('#open-browser').click();await n.locator('#browser-pane').waitFor();assert.equal(narrow.pages().length,1);
 assert.equal(await n.evaluate(()=>document.documentElement.dataset.drawer||''),'');await narrow.close();
 // Settings from the pane, then Back: the pane again
 const set=await context.newPage();set.on('pageerror',e=>errors.push(e.message));await set.goto(base);await set.locator('#open-browser').click();await set.locator('#browser-pane').waitFor();
 await set.locator('#open-settings').click();await set.locator('#settings').waitFor();assert.equal(await set.locator('#browser-pane').isHidden(),true);
 await set.goBack();await set.locator('#browser-pane').waitFor();assert.equal(await set.locator('#settings').isHidden(),true);
 assert.equal(await set.locator('#open-browser').getAttribute('aria-current'),'page');await set.close();
 // From a chat: a refresh while the pane is open keeps the chat, and Back shows it
 const ch=await context.newPage();ch.on('pageerror',e=>errors.push(e.message));await ch.goto(base+'/#chat=aaaaaaaaaaaaaaa1');await ch.locator('.chat-head').waitFor();
 await ch.locator('#open-browser').click();await ch.locator('#browser-pane').waitFor();
 await ch.evaluate(()=>refresh());await new Promise(r=>setTimeout(r,300));
 assert.equal(await ch.evaluate(()=>chatId),'aaaaaaaaaaaaaaa1');
 await ch.goBack();await ch.locator('.chat-head').waitFor();assert.ok(ch.url().endsWith('#chat=aaaaaaaaaaaaaaa1'));
 assert.equal(await ch.locator('#browser-pane').isHidden(),true);await ch.close();
 // A link straight to #browser opens it
 const deep=await context.newPage();deep.on('pageerror',e=>errors.push(e.message));await deep.goto(base+'/#browser');await deep.locator('#browser-pane').waitFor();await deep.close();
 // A phone keeps the new tab
 const phone=await browser.newContext({viewport:{width:390,height:800},isMobile:true,hasTouch:true});await phone.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const p2=await phone.newPage();p2.on('pageerror',e=>errors.push(e.message));await p2.goto(base);await p2.locator('#open-settings').waitFor({state:'attached'});  // in the drawer on a phone
 await p2.evaluate(()=>document.querySelector('#open-browser').click());await new Promise(r=>setTimeout(r,300));
 assert.equal(await p2.locator('#browser-pane').isHidden(),true);await phone.close();
 // The dashboard installed on a phone has no tabs either: the pane, never the account's handoff (browser_link). On
 // Android the installed app took that handoff's way back to the Machine's address into itself and started over at its
 // splash screen, so the browser never showed. Android's installed app (display-mode) and iOS's home screen one.
 for(const how of ['android','ios']){
  const inst=await browser.newContext({viewport:{width:390,height:800},isMobile:true,hasTouch:true});await inst.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await inst.addInitScript(ios=>{if(ios){Object.defineProperty(navigator,'standalone',{configurable:true,value:true});return}
   const mm=window.matchMedia.bind(window);window.matchMedia=q=>/display-mode: *standalone/.test(q)?{matches:true,media:q,addEventListener(){},removeEventListener(){},addListener(){},removeListener(){}}:mm(q)},how==='ios');
  const p3=await inst.newPage();p3.on('pageerror',e=>errors.push(e.message));const left=[];p3.on('framenavigated',f=>{if(f===p3.mainFrame())left.push(f.url())});
  await p3.goto(base);await p3.locator('#open-settings').waitFor({state:'attached'});
  await p3.evaluate(()=>document.querySelector('#open-browser').click());await p3.locator('#browser-pane').waitFor();
  await p3.frameLocator('#bp-frame').locator('#viewer').waitFor();
  assert.equal(inst.pages().length,1,how);assert.ok(left.every(u=>u.startsWith(base)),how+' '+left.join(' '));
  {const f=await p3.locator('#bp-frame').boundingBox();assert.ok(f.width===390&&f.height>600,how+' '+JSON.stringify(f))}
  assert.equal(await p3.locator('#bp-tab').isHidden(),true,how);
  // A to-do's View in Machine browser too
  await p3.locator('#bp-close').click();await p3.locator('#browser-pane').waitFor({state:'hidden'});
  await p3.evaluate(()=>{const a=document.createElement('a');a.href='https://cp.example/open?to=browser';a.target='_blank';a.dataset.browserShow='aaaaaaaaaaaaaaa1';a.textContent='View';document.body.append(a);a.click()});
  await p3.locator('#browser-pane').waitFor();assert.equal(inst.pages().length,1,how);
  await inst.close()}
 // No viewer on the dashboard's own address: a new tab, also on a computer
 embed=null;await page.reload();await row.waitFor();
 const [tab]=await Promise.all([context.waitForEvent('page'),row.click()]);await tab.close();
 assert.equal(await pane.isHidden(),true);
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('browser pane dashboard ok');
