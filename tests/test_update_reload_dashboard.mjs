import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// An open dashboard never reloads under someone using it. A new release (the server's page differs from this one)
// waits until the page is hidden, or nobody touched it for a few minutes, and never while something is typed in any
// field or a dialog is open; meanwhile an "Update ready" pill loads it at a press. A restart of the Machine alone (same
// page) only reconnects. A data refresh keeps the typed text, the focus and the place on the page. A notification's
// link opens in the page without reloading it.
const raw=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString(),id='a1a1a1a1a1a1a1a1';
let served='v1',current='v1',staleOnce=null,body='Robin asked for the numbers.',down=false;
const cards=()=>[{id,title:'Reply to Robin about the plan',body,status:'pending',scope:'work',created_at:now,event_ids:[1]},
 ...Array.from({length:12},(_,n)=>({id:String.fromCharCode(98+n%5).repeat(2)+String(n).padStart(14,'0'),title:'Another to-do '+n,body:'Some words. '.repeat(30),status:'pending',scope:'work',created_at:now,event_ids:[n+2]}))];
const status=()=>({suggestions:cards(),promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false},ui_version:current});
const hits={page:0,status:0};
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');
 if(url.pathname==='/'){hits.page++;const v=staleOnce||served;staleOnce=null;res.setHeader('Content-Type','text/html');res.end(raw.replace('__CSRF__','c'.repeat(64)).replaceAll('__UI_VERSION__',v).replace('__BASE__','/').replace('__CACHE_SCOPE__','s'.repeat(32)));return}
 if(url.pathname==='/api/status'){hits.status++;if(down){res.statusCode=503;res.setHeader('Retry-After','1');res.end('{"error":"restarting","restarting":true}');return}res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:'s'.repeat(32)}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
// A release: the Machine serves a new page from now on
const release=v=>{served=current=v};
const until=async(fn,label,ms=10000)=>{const t=Date.now();while(!(await fn())){if(Date.now()-t>ms)throw Error('timed out: '+label);await new Promise(r=>setTimeout(r,100))}};
const setHidden=(p,hidden)=>p.evaluate(h=>{Object.defineProperty(document,'hidden',{get:()=>h,configurable:true});Object.defineProperty(document,'visibilityState',{get:()=>h?'hidden':'visible',configurable:true});document.dispatchEvent(new Event('visibilitychange'))},hidden);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:700},colorScheme:'dark',locale:'en-US',timezoneId:'Europe/Brussels'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.clock.install();
 const open=async()=>{await page.goto(base);await page.locator(`#suggestions article[id="task-${id}"]`).waitFor({timeout:8000}).catch(async e=>{console.log(errors,(await page.locator("#suggestions").innerHTML()).slice(0,1500));throw e})};
 const mark=()=>page.evaluate(()=>{window.__same=1});const same=()=>page.evaluate(()=>window.__same===1).catch(()=>false);
 const wiggle=async()=>{await page.mouse.move(400+Math.random()*200,300);await page.mouse.move(700,320)};
 // Doing something on the page: a key (the pointer only passing over it is not use, see 9.)
 const use=async()=>{await wiggle();await page.keyboard.press('Shift')};
 const refreshNow=()=>page.evaluate(()=>refresh());

 // 1. Someone is reading: the release shows the pill, the page stays as it is (also minutes later while they use it)
 await open();await mark();await use();
 release('v2');await refreshNow();
 assert.ok(await page.locator('#update-ready').isVisible(),'the Update ready pill shows');
 assert.equal(await page.locator('#update-ready').innerText(),'Update ready');
 for(let i=0;i<6;i++){await page.clock.fastForward(40e3);await use();await refreshNow()}  // 4 minutes of use
 assert.ok(await same(),'no reload while the page is in use');

 // 2. A data refresh keeps the place on the page, the typed text and the focus; a draft holds the update back, also idle and hidden
 const draft=page.locator(`#feedback-${id}`);
 if(!await draft.isVisible())await page.locator(`article[id="task-${id}"] button[data-choice="change"]`).first().evaluate(b=>b.click());
 await draft.evaluate(t=>{t.value='Half a reply to Robin';t.dispatchEvent(new Event('input',{bubbles:true}))});
 await draft.evaluate(t=>t.blur());await page.evaluate(()=>scrollTo(0,400));const y=await page.evaluate(()=>scrollY);
 body='Robin asked again, with a deadline.';await refreshNow();
 await until(()=>page.locator(`article[id="task-${id}"]`).innerText().then(t=>t.includes('with a deadline')),'the new data is drawn');
 assert.equal(await draft.inputValue(),'Half a reply to Robin','the draft stays through a data refresh');
 {const y2=await page.evaluate(()=>scrollY);assert.ok(y>300&&Math.abs(y2-y)<2,`the page stays at the same place (${y} -> ${y2})`)}
 // focus and caret on a field the redraw replaced
 await page.evaluate(()=>{const i=document.createElement('input');i.id='focus-probe';i.value='abcdef';document.querySelector('#suggestions').prepend(i);i.focus();i.setSelectionRange(2,4)});
 await page.evaluate(()=>focusKept(()=>{const o=document.getElementById('focus-probe'),n=o.cloneNode();n.value=o.value;o.replaceWith(n)}));
 assert.deepEqual(await page.evaluate(()=>[document.activeElement.id,document.activeElement.selectionStart,document.activeElement.selectionEnd]),['focus-probe',2,4],'focus and caret are kept');
 await page.evaluate(()=>{document.getElementById('focus-probe').remove();document.activeElement?.blur()});
 await page.clock.fastForward(4*60e3);await page.clock.runFor(16e3);
 assert.ok(await same(),'idle, but a draft is there: no reload');
 await setHidden(page,true);await page.clock.runFor(16e3);
 assert.ok(await same(),'hidden, but a draft is there: no reload');
 assert.equal(await draft.inputValue(),'Half a reply to Robin');

 // 3. Hidden with nothing typed: the new version loads, and the page comes back on its tab
 await draft.evaluate(t=>{t.value='';t.dispatchEvent(new Event('input',{bubbles:true}))});
 const pages=hits.page;await page.locator('nav button[data-tab="feedback"]').click({force:true}).catch(()=>page.evaluate(()=>document.querySelector('nav button[data-tab="feedback"]')?.click()));
 const loaded=page.waitForEvent('load');await page.clock.runFor(16e3);await loaded;
 assert.equal(hits.page,pages+1,'the page loaded once more');
 assert.equal(await page.evaluate(()=>UI_VERSION),'v2','the new version runs');
 await until(()=>page.evaluate(()=>!document.querySelector('#feedback').hidden),'back on the same tab');
 assert.ok(!await page.locator('#update-ready').isVisible(),'no pill after the update');

 // 4. Idle for a few minutes (visible), nothing typed: the new version loads
 await page.evaluate(()=>document.querySelector('nav button[data-tab="inbox"]').click());await mark();await wiggle();
 release('v3');await refreshNow();assert.ok(await same());
 const idle=page.waitForEvent('load');await page.clock.fastForward(3*60e3+1000);await page.clock.runFor(16e3);await idle;
 assert.equal(await page.evaluate(()=>UI_VERSION),'v3','idle: the new version runs');

 // 5. Coming back to the page counts as use: the update does not land right as someone returns
 await page.locator(`#suggestions article[id="task-${id}"]`).waitFor();await mark();await wiggle();
 await setHidden(page,true);release('v4');await page.clock.fastForward(10*60e3);await setHidden(page,false);await refreshNow();
 assert.ok(await same(),'no reload on returning to the page');
 assert.ok(await page.locator('#update-ready').isVisible());
 // the pill loads it at a press
 const pressed=page.waitForEvent('load');await page.locator('#update-ready').click();await pressed;
 assert.equal(await page.evaluate(()=>UI_VERSION),'v4','the pill loads the new version');

 // 6. A dialog open: no reload, also idle and hidden
 await page.locator(`#suggestions article[id="task-${id}"]`).waitFor();await mark();
 await page.evaluate(()=>document.querySelector('#snooze-dialog').showModal());
 release('v5');await page.evaluate(()=>{state.ui_version='v5';uiVersionCheck()});await page.clock.fastForward(5*60e3);await setHidden(page,true);await page.clock.runFor(16e3);
 assert.ok(await same(),'no reload with a dialog open');
 await page.evaluate(()=>document.querySelector('#snooze-dialog').close());await setHidden(page,false);
 await page.locator('#update-ready').click();await page.waitForEvent('load');

 // 7. A restart of the Machine alone (same page): it reconnects quietly, the draft and the place stay
 await page.locator(`#suggestions article[id="task-${id}"]`).waitFor();await mark();await wiggle();
 if(!await draft.isVisible())await page.locator(`article[id="task-${id}"] button[data-choice="change"]`).first().evaluate(b=>b.click());
 await draft.evaluate(t=>{t.value='Typed before the restart';t.dispatchEvent(new Event('input',{bubbles:true}));t.blur()});
 down=true;await refreshNow();
 await until(()=>page.locator('#updated').innerText().then(t=>/Restarting/.test(t)),'says it is restarting');
 down=false;body='After the restart.';
 for(let i=0;i<4&&!(await page.locator(`article[id="task-${id}"]`).innerText()).includes('After the restart');i++){await page.clock.runFor(31e3);await new Promise(r=>setTimeout(r,200))}
 await until(()=>page.locator(`article[id="task-${id}"]`).innerText().then(t=>t.includes('After the restart')),'reconnected');
 assert.ok(await same(),'a restart does not reload the page');
 assert.ok(!await page.locator('#update-ready').isVisible(),'no pill: nothing new to load');
 assert.equal(await draft.inputValue(),'Typed before the restart');

 // 8. A notification's link opens in the page, without reloading it
 const before=hits.page;
 await page.evaluate(u=>navigator.serviceWorker?.dispatchEvent(new MessageEvent('message',{data:{open:u}})),base+'#events');
 await until(()=>page.evaluate(()=>location.hash==='#events'||!document.querySelector('#events')?.hidden),'the link opened');
 assert.ok(await same(),'a notification link does not reload');assert.equal(hits.page,before);

 // 9. A window in the background (a desktop app's window while another one has the focus): the pointer passing over it
 // is not use, and the new version loads once nobody did anything in it for 45 s
 await page.evaluate(()=>{location.hash='';document.querySelector('nav button[data-tab="inbox"]').click()});await page.locator(`#suggestions article[id="task-${id}"]`).waitFor();
 await draft.evaluate(t=>{t.value='';t.dispatchEvent(new Event('input',{bubbles:true}))});  // nothing typed (7. was sent)
 await mark();await use();await page.evaluate(()=>{document.hasFocus=()=>false});
 release('v5a');await refreshNow();assert.ok(await same(),'not at once');
 await page.clock.fastForward(20e3);await wiggle();await page.clock.runFor(16e3);assert.ok(await same(),'not within 45 s of the last use');
 const away=page.waitForEvent('load');await page.clock.fastForward(20e3);await wiggle();await page.clock.runFor(16e3);await away;
 assert.equal(await page.evaluate(()=>UI_VERSION),'v5a','a background window loads the new version');
 // in front, the same pointer moves keep it (the case of someone reading): see 1.
 await page.locator(`#suggestions article[id="task-${id}"]`).waitFor();

 // 10. An older copy the app opened with (nobody did anything in it yet): it takes the new version at once, also as the
 // window opens under the pointer and gets the focus (a desktop app's window)
 const fresh=await context.newPage();fresh.on('pageerror',e=>errors.push(e.message));staleOnce='v5';release('v6');
 await fresh.addInitScript(()=>addEventListener('DOMContentLoaded',()=>{dispatchEvent(new Event('focus'));document.dispatchEvent(new PointerEvent('pointermove',{bubbles:true}))}));
 await fresh.goto(base);await fresh.waitForURL(base);await until(()=>fresh.evaluate(()=>UI_VERSION).then(v=>v==='v6').catch(()=>false),'just opened: updates at once');
 await fresh.close();
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({page_errors:errors,hits}));
}finally{await browser?.close();server.close()}
