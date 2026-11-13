import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {createServer} from 'node:http';
import {fileURLToPath} from 'node:url';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's chat sources read as one clean thread: the conversation named once on top, the messages oldest first,
// each sender's run under their name and time once, every text once (no "#DM name: text" preview line over it), no
// per-message Details or collapsible groups, one Open in Slack for the thread, Slack :emoji: as emoji, and the to-do's
// own message tinted when more came after it. WhatsApp and Intercom read the same way; an email still reads as an
// email. Originals come from the real service (tests/test_chat_thread.py's made-up fixture).
// CHAT_THREAD_SHOTS=dir saves screenshots; CHAT_THREAD_PAGE=<other dashboard.html> only takes them (a before set).
const root=new URL('../',import.meta.url);
const py=`import sys,tempfile
sys.path[:0]=['.','tests']
import test_chat_thread as c
with tempfile.TemporaryDirectory() as folder:
    print(c.dump(folder))`;
const run=spawnSync(process.env.PYTHON||(process.platform==='win32'?'python':'python3'),['-c',py],{cwd:fileURLToPath(root),encoding:'utf8'});
assert.equal(run.status,0,run.stderr);
const data=JSON.parse(run.stdout);
const other=process.env.CHAT_THREAD_PAGE,dashboard=await dashboardPage(other||undefined),shots=process.env.CHAT_THREAD_SHOTS;
const now=new Date().toISOString();
const SRC={slack:'Source: Slack DM from Rowan Vale',whatsapp:'Source: WhatsApp from Milo Grant',wamedia:'Source: WhatsApp from Sasha Brook',wa1on1:'Source: WhatsApp from Robin Hale',intercom:'Source: Intercom from Juno Park',email:'Source: email from Avery Stone'};
const TITLE={slack:'Move the warmup tool billing to the company card',whatsapp:'Tell the climbing crew if you drive on Saturday',wamedia:'Get the chalk and tape for Saturday',wa1on1:'Order the lamp Robin sent',intercom:'Resend the October invoice to Harbor',email:'Reply to Avery about the booth quote'};
const cards=Object.entries(data).map(([k,v])=>({id:v.id,title:TITLE[k],body:'',status:'pending',scope:'work',created_at:now,event_ids:v.originals.map(o=>o.event_id),source_line:SRC[k]}));
const byId=Object.fromEntries(Object.values(data).map(v=>[v.id,v.originals]));
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/originals'){const id=url.searchParams.get('id'),ev=url.searchParams.get('event');
  res.end(JSON.stringify({originals:id?byId[id]:Object.values(byId).flat().filter(o=>String(o.event_id)===ev)}));return}
 if(url.pathname==='/api/email'){res.end(JSON.stringify({html:''}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const sizes=shots?[[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]:[[390,844,'dark'],[1440,900,'light']];
 for(const [width,height,scheme] of sizes){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.locator('#task-'+data.slack.id).waitFor();
  const box=page.locator('#email-content');
  const open=async k=>{await page.evaluate(id=>{const d=document.querySelector('#email-dialog');if(d.open)d.close();return openEmail(id)},data[k].id);await box.locator('.convo-say,.email-text,.email-frame,.email').first().waitFor()};
  const shot=async k=>{if(shots)await page.screenshot({path:`${shots}/${other?'before':'after'}-${k}-${width}x${height}-${scheme}.png`})};
  for(const k of ['slack','whatsapp','intercom','email']){await open(k);await page.waitForTimeout(150);await shot(k);
   if(k==='slack'&&width===390&&shots){await box.evaluate(n=>n.closest('dialog').scrollTop=1e5);await shot('slack-end')}}
  if(other){await context.close();continue}
  // Slack DM: the conversation once, five texts once each, in time order, no preview line, Details or groups
  await open('slack');
  assert.equal(await box.locator('.convo-chat').innerText(),'DM with Rowan Vale');
  assert.equal(await box.locator('.convo-chat .via-ico.via-slack').count(),1);
  assert.deepEqual(await box.locator('.convo-say').allInnerTexts(),['I just noticed we pay for the mail warmup tool with my personal credit card 🙃',
   'Could we move it to the company card asap?','Also worth checking what it costs per month','And whether we still need it 👍🏼','Will look at it tomorrow morning.']);
  assert.equal(await box.locator('.email-subject,.email-headers,details,.email-earlier').count(),0);
  assert.doesNotMatch(await box.innerText(),/#DM|:upside_down_face:|:\+1:|Details|related message/);
  // Rowan's four messages are one run under their name and time once; a light time only after a pause
  const turns=box.locator('.convo-turn');assert.equal(await turns.count(),2);
  assert.equal(await turns.nth(0).locator('.convo-meta').innerText(),'Rowan Vale · 18:56');
  assert.deepEqual(await turns.nth(0).locator('.convo-at').allInnerTexts(),['19:15','19:31']);
  assert.equal(await turns.nth(1).getAttribute('class'),'convo-turn me');assert.equal(await turns.nth(1).locator('.convo-meta').innerText(),'19:40');
  assert.equal(await box.locator('.convo-day').count(),1);
  // The to-do's own message is first, not last: tinted, and said so to screen readers
  const main=box.locator('.convo-main');assert.equal(await main.count(),1);
  assert.match(await main.innerText(),/personal credit card/);assert.equal(await main.getAttribute('aria-label'),'The message this to-do is about');
  assert.equal(await main.evaluate(n=>getComputedStyle(n).borderLeftStyle),'solid');
  // One link for the thread, the to-do's own message
  const link=box.locator('a.convo-source');assert.equal(await link.count(),1);
  assert.equal(await link.innerText(),'Open in Slack ↗');assert.equal(await link.getAttribute('href'),'https://acme.slack.example/archives/D0ROWAN/p1');
  // No horizontal scroll at any width
  assert.ok(await box.evaluate(n=>n.closest('dialog').scrollWidth<=n.closest('dialog').clientWidth+1),'no sideways scroll');
  // WhatsApp group: the chat's name once, each sender's run under their name; the to-do's message mid-thread is tinted
  await open('whatsapp');
  assert.equal(await box.locator('.convo-chat span[translate]').innerText(),'Climbing crew');assert.equal(await box.locator('.convo-chat .convo-app').innerText(),'WhatsApp');
  // a messenger reads like its app: names over the other side's runs, the owner's bubbles on the right, each bubble its time
  assert.equal(await box.locator('.convo.convo-im').count(),1);
  assert.deepEqual(await box.locator('.convo-meta').allInnerTexts(),['Sasha Brook','Milo Grant']);
  assert.deepEqual(await box.locator('.convo-say .convo-t').allInnerTexts(),['09:02','09:05','09:06','09:30']);
  const [left,right]=await Promise.all(['.convo-turn:not(.me) .convo-say','.convo-turn.me .convo-say'].map(s=>box.locator(s).first().boundingBox()));
  assert.ok(right.x+right.width>left.x+left.width+40,'the owner\'s bubble sits on the right');
  assert.match(await box.locator('.convo-main').innerText(),/^Me! 10:00/);
  assert.equal(await box.locator('.convo-main').evaluate(n=>n.previousElementSibling.textContent),'This to-do');
  assert.equal(await box.locator('a.convo-source').count(),0,'no link when the source has none');
  // A photo and a file without their own words are chips, never "Sent image"; links read as what they are
  await open('wamedia');
  assert.deepEqual(await box.locator('.convo-media').allInnerTexts(),['Photo','File']);
  assert.doesNotMatch(await box.innerText(),/Sent image|Sent document|https:\/\//);
  assert.match(await box.locator('.convo-say-media').first().innerText(),/^Photo\s*09:40$/);
  assert.deepEqual(await box.locator('.convo-link-name').allInnerTexts(),['Climbing chalk bag large','Finger tape roll white']);
  assert.deepEqual(await box.locator('.convo-link-site').allInnerTexts(),['shop.example','shop.example','wall.example/routes/north']);
  assert.deepEqual(await box.locator('a.convo-link').evaluateAll(as=>as.map(a=>a.getAttribute('href'))),['https://shop.example/nl/p/climbing-chalk-bag-large/9300001/','https://www.shop.example/nl/p/finger-tape-roll-white/9300002/','https://wall.example/routes/north']);
  assert.match(await box.locator('.convo-main .convo-said').innerText(),/^Chalk and tape from here:/);
  // A 1:1 names nobody over the bubbles (the line on top names the person); a link bubble is one surface, its time inside
  await open('wa1on1');
  assert.equal(await box.locator('.convo-chat span[translate]').innerText(),'Robin Hale');assert.equal(await box.locator('.convo-meta').count(),0);
  const bubble=box.locator('.convo-say-link'),[b,card,tm]=await Promise.all([bubble,bubble.locator('.convo-link'),bubble.locator('.convo-t')].map(l=>l.boundingBox()));
  assert.equal(await bubble.locator('.convo-link').evaluate(n=>getComputedStyle(n).backgroundColor),'rgba(0, 0, 0, 0)');
  assert.ok(tm.x+tm.width<=b.x+b.width&&tm.y+tm.height<=b.y+b.height&&card.x+card.width<=b.x+b.width,'the link fills its bubble, the time inside it');
  // Intercom: one conversation, its turns; the event-only parts left out, an internal note marked
  await open('intercom');
  assert.equal(await box.locator('.convo-chat').innerText(),'Juno Park');
  assert.deepEqual(await box.locator('.convo-meta').allInnerTexts(),['Juno Park · 11:50','Kit Navarro · 11:55','Juno Park · 12:08']);
  assert.equal(await box.locator('.convo-say').count(),4);assert.equal(await box.locator('.convo-note .convo-tag').innerText(),'NOTE');
  assert.match(await box.locator('.convo-say').last().innerText(),/books 🙏$/);
  assert.equal(await box.locator('.convo-main').count(),0,'the whole conversation is the to-do\'s');
  assert.equal(await box.locator('a.convo-source').innerText(),'Open in Intercom ↗');
  // An email reads as before: sender, subject, To, the text, Open in Gmail; no Details when To is a bare address
  // already shown in full (the message viewer says nothing twice: tests/test_message_view_dashboard.mjs)
  await open('email');await box.locator('.email-text').waitFor();
  assert.equal(await box.locator('.convo').count(),0);
  assert.equal(await box.locator('.email-from strong').innerText(),'Avery Stone <avery@booths.example>'.replace(/\s*<[^>]+>/,''));
  assert.equal(await box.locator('.email-subject').innerText(),'Quote for the booth');
  assert.equal(await box.locator('.email-to').innerText(),'to owner@example.com');assert.equal(await box.locator('.email-headers').count(),0);
  // A single Slack message opened from Messages reads the same way: its text once
  await page.evaluate(ev=>openEvent(String(ev),'x'),data.slack.originals[1].event_id);await box.locator('.convo-say').waitFor();
  assert.deepEqual(await box.locator('.convo-say').allInnerTexts(),['Could we move it to the company card asap?']);
  // the chat names the dialog, the app heads the thread (the message viewer's chat view)
  assert.equal(await page.locator('#email-title').innerText(),'DM with Rowan Vale');assert.equal(await box.locator('.convo-chat').innerText(),'Slack');assert.equal(await box.locator('.convo-main').count(),0);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log(other?'chat thread before shots taken':'chat thread dashboard ok');
}finally{await browser?.close();server.close()}
