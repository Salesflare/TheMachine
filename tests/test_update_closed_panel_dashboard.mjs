import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A quiet update is held back only by text someone typed and hasn't saved or sent. A closed panel never holds it back:
// a send panel that still has a sent email's subject and body (the page filled them in, nobody typed them) lets the
// new version load, and closing the send panel empties it. Typed text in an open to-do still holds it back.
const raw=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString(),id='a1a1a1a1a1a1a1a1';
let served='v1',current='v1';
const status=()=>({suggestions:[{id,title:'Reply to Robin about the plan',body:'Robin asked for the numbers.',status:'pending',scope:'work',created_at:now,event_ids:[1]}],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false},ui_version:current});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(raw.replace('__CSRF__','c'.repeat(64)).replaceAll('__UI_VERSION__',served).replace('__BASE__','/').replace('__CACHE_SCOPE__','s'.repeat(32)));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:'s'.repeat(32)}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const setHidden=(p,hidden)=>p.evaluate(h=>{Object.defineProperty(document,'hidden',{get:()=>h,configurable:true});Object.defineProperty(document,'visibilityState',{get:()=>h?'hidden':'visible',configurable:true});document.dispatchEvent(new Event('visibilitychange'))},hidden);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:700},locale:'en-US',timezoneId:'Europe/Brussels'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.clock.install();
 await page.goto(base);await page.locator(`#suggestions article[id="task-${id}"]`).waitFor({timeout:8000});
 await page.mouse.move(400,300);await page.keyboard.press('Shift');
 await page.evaluate(()=>{window.__same=1});const same=()=>page.evaluate(()=>window.__same===1).catch(()=>false);

 // 1. The send panel the way the page fills it for an email, then closed after Send: nothing stays in it
 await page.evaluate(()=>{const d=document.querySelector('#send-dialog');d.showModal();document.querySelector('#send-subject').value='Numbers for Q4';
  document.querySelector('#send-body').value='Hi Robin';document.querySelector('#send-rich-body').innerHTML='<p>Hi Robin, here they are.</p>'});
 assert.ok(await page.evaluate(()=>pageInUse()),'an open panel holds the update back');
 await page.evaluate(()=>document.querySelector('#send-dialog').close());
 for(let i=0;i<50&&await page.evaluate(()=>document.querySelector('#send-subject').value);i++)await new Promise(r=>setTimeout(r,20));  // the close event comes a moment later
 assert.deepEqual(await page.evaluate(()=>['#send-subject','#send-body','#send-ask-text'].map(s=>document.querySelector(s).value).concat(document.querySelector('#send-rich-body').innerHTML)),['','','',''],'closing the send panel empties it');
 assert.equal(await page.evaluate(()=>pageInUse()),false,'nothing in use once the panel closed');

 // 2. A closed panel that still holds text (filled by the page, or left from before) is not typing
 await page.evaluate(()=>{document.querySelector('#send-subject').value='Numbers for Q4';document.querySelector('#send-rich-body').innerHTML='<p>Sending your approved draft…</p>'});
 assert.equal(await page.evaluate(()=>typedSomewhere()),false,'text in a closed panel does not count');

 // 3. Typed and not saved in an open to-do still counts
 const draft=page.locator(`#feedback-${id}`);
 if(!await draft.isVisible())await page.locator(`article[id="task-${id}"] button[data-choice="change"]`).first().evaluate(b=>b.click());
 await draft.evaluate(t=>{t.value='Half a reply';t.dispatchEvent(new Event('input',{bubbles:true}))});
 assert.equal(await page.evaluate(()=>typedSomewhere()),true,'real typing counts');
 served=current='v2';await page.evaluate(()=>refresh());
 assert.ok(await page.locator('#update-ready').isVisible(),'the pill shows');
 await setHidden(page,true);await page.clock.runFor(16e3);
 assert.ok(await same(),'typing in a to-do holds the update back');

 // 4. That typing gone, the closed panel's leftovers don't hold it: the new version loads
 await draft.evaluate(t=>{t.value='';t.dispatchEvent(new Event('input',{bubbles:true}))});
 const loaded=page.waitForEvent('load');await page.clock.runFor(16e3);await loaded;
 assert.equal(await page.evaluate(()=>UI_VERSION),'v2','the new version loads');
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({page_errors:errors}));
}finally{await browser?.close();server.close()}
