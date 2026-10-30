import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {createServer} from 'node:http';
import {fileURLToPath} from 'node:url';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// An email reply in a to-do's chat: mail sync stores it with a "[Quoted earlier messages: …]" line for the model
// between the new text and the quoted history (assistant.trim_quoted_history). People never see that line: each
// email shows its new text, its quoted history folded under it as "Earlier messages", and More/Less and Read the
// thread work as before. The chat and the originals come from the real service (tests/test_quoted_marker.py's
// fixture: two emails from Sam, the later one quoting the first). QUOTED_SHOTS=dir saves screenshots.
const root=new URL('../',import.meta.url);
const py=`import json,sys,tempfile
sys.path[:0]=['.','tests']
import test_quoted_marker as q
with tempfile.TemporaryDirectory() as folder:
    app,sid,bodies=q.fixture(folder)
    with app.store.connect() as db:
        owner,_=app.card_chat_service(db,sid)
    print(json.dumps({'sid':sid,'bodies':bodies,'items':owner,'originals':app.originals(sid)}))`;
const run=spawnSync(process.env.PYTHON||(process.platform==='win32'?'python':'python3'),['-c',py],{cwd:fileURLToPath(root),encoding:'utf8'});
assert.equal(run.status,0,run.stderr);
const data=JSON.parse(run.stdout);
assert.ok(data.bodies.every(b=>b.includes('[Quoted earlier messages:')),'the stored bodies carry the model marker');
const MARK=/Quoted earlier messages|separate signals|characters kept/;
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const card={id:data.sid,title:'Reply to Sam',body:'Sam sent the link details.',status:'pending',scope:'work',created_at:now,event_ids:[1,2],source_line:'Source: email from Sam Z'};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/originals'){res.end(JSON.stringify({originals:data.originals}));return}
 if(url.pathname==='/api/email'){res.end(JSON.stringify({html:''}));return}
 if(url.pathname==='/api/action'){const {action}=JSON.parse(body||'{}');
  if(action==='card_chat'){res.end(JSON.stringify({session:false,status:'ok',active:false,cursor:'k',items:data.items}));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;const shots=process.env.QUOTED_SHOTS;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[1440,900,'dark'],[1440,700,'light'],[390,844,'dark']]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/#chat=${card.id}`);
  const log=page.locator('#chat-log'),sources=log.locator('.chat-source');await sources.nth(1).waitFor();
  const shot=async n=>{if(shots)await page.screenshot({path:`${shots}/quoted-${n}-${width}x${height}.png`})};
  // Two emails, each its own new text; no marker anywhere in the chat
  assert.equal(await sources.count(),2);
  assert.doesNotMatch(await log.innerText(),MARK);
  assert.match(await sources.nth(1).locator('.say').innerText(),/^For ABC exchange, here is the alternative\./);
  // Each one's quoted history is folded under it, apart from the new text and closed
  for(const n of [0,1]){const fold=sources.nth(n).locator('details.chat-quoted');
   assert.equal(await fold.count(),1);assert.equal(await fold.getAttribute('open'),null);
   assert.equal((await fold.locator('summary').innerText()).replace(/\s*[›‹]\s*$/,''),'Earlier messages');
   assert.ok(!(await fold.locator('.chat-quoted-text').isVisible()),'history hidden until opened');
   assert.ok(await sources.nth(n).evaluate(m=>m.querySelector('details.chat-quoted').getBoundingClientRect().top>=m.querySelector('.say').getBoundingClientRect().bottom),'under the new text')}
  await log.evaluate(n=>n.scrollTop=0);await shot('closed');
  // More and Less on the long first email
  const more=sources.nth(0).locator('.chat-more');assert.equal(await more.innerText(),'More');
  await more.click();await page.waitForFunction(()=>document.querySelector('#chat-log .chat-source .chat-more')?.textContent==='Less');
  assert.ok(await sources.nth(0).locator('.chat-clamp.open').count());
  // Opening the later email's history shows the first email quoted, and stays open when the chat paints again
  const later=sources.nth(1).locator('details.chat-quoted');await later.locator('summary').click();
  await later.locator('.chat-quoted-text').waitFor();
  assert.match(await later.locator('.chat-quoted-text').innerText(),/Sam Z <sam@example\.net> wrote:[\s\S]*Here are my link details/);
  await page.evaluate(()=>paintChat());
  assert.equal(await sources.nth(1).locator('details.chat-quoted').getAttribute('open'),'');
  assert.equal(await sources.nth(0).locator('.chat-more').innerText(),'Less');
  assert.doesNotMatch(await log.innerText(),MARK);
  await shot('open');
  await sources.nth(0).locator('.chat-more').click();await page.waitForFunction(()=>document.querySelector('#chat-log .chat-source .chat-more')?.textContent==='More');
  // Read the thread, once under the last email: the dialog shows the emails without the marker
  const read=log.locator('[data-original="read"]');assert.equal(await read.count(),1);
  await read.click();await page.locator('#email-dialog .email-text').first().waitFor();
  assert.doesNotMatch(await page.locator('#email-content').innerText(),MARK);
  assert.match(await page.locator('#email-content').innerText(),/Here are my link details/);
  await shot('thread');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('quoted history dashboard ok');
}finally{await browser?.close();server.close()}
