import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import {createServer} from 'node:http';
import {fileURLToPath} from 'node:url';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's source message opens with what was said around it: in a Slack DM the same day's messages before it and the
// replies after it, the to-do's own message tinted and in view, and a quiet Show earlier that adds older ones above
// without moving what is on screen; a WhatsApp group the same; an email thread its earlier mail folded above the
// to-do's email and the reply folded below. Originals come from the real service (tests/test_message_context.py's
// made-up fixture). MESSAGE_CONTEXT_SHOTS=dir saves screenshots at 390 and 1440, light and dark.
const root=new URL('../',import.meta.url);
const py=`import sys,tempfile
sys.path[:0]=['.','tests']
import test_message_context as c
with tempfile.TemporaryDirectory() as folder:
    print(c.dump(folder))`;
const run=spawnSync(process.env.PYTHON||(process.platform==='win32'?'python':'python3'),['-c',py],{cwd:fileURLToPath(root),encoding:'utf8'});
assert.equal(run.status,0,run.stderr);
const data=JSON.parse(run.stdout);
const dashboard=await dashboardPage(),shots=process.env.MESSAGE_CONTEXT_SHOTS;
const now=new Date().toISOString();
const SRC={slack:'Source: Slack DM from Kai Moreno',whatsapp:'Source: WhatsApp from Garden club',email:'Source: email from Avery Stone',thread:'Source: Slack DM from Rui Costa'};
const TITLE={slack:'Look into the missing bug report to-do',whatsapp:'Pick up the ladder from Bo on Friday',email:'Tell Avery if the booth lighting is a go',thread:'Log the release blocker'};
const cards=Object.entries(data).map(([k,v])=>({id:v.id,title:TITLE[k],body:'',status:'pending',scope:'work',created_at:now,event_ids:v.originals.map(o=>o.event_id),source_line:SRC[k]}));
// The thread reply's to-do is ready with a link to its own message (the review's "Open original discussion"): that one
// reads it here, in the viewer; a link elsewhere still leaves
const own=data.thread.originals[0].url;
Object.assign(cards.find(c=>c.id===data.thread.id),{status:'prepared',body:'Rui answered your four points.',original_urls:[own],
 next_action:{kind:'menu',actions:[{kind:'open',url:own+'?thread_ts=1',label:'Open original discussion',revision:1},{kind:'open',url:'https://docs.example/spec',label:'Open the spec',revision:2}]},
 next_actions:[{kind:'open',url:own+'?thread_ts=1',label:'Open original discussion',revision:1},{kind:'open',url:'https://docs.example/spec',label:'Open the spec',revision:2}]});
const byId=Object.fromEntries(Object.values(data).map(v=>[v.id,v]));
const asked=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/originals'){const v=byId[url.searchParams.get('id')],before=url.searchParams.get('before');
  if(before){asked.push(before);res.end(JSON.stringify(String(v.earlier?.from)===before?{around:v.earlier.around}:{error:'Original not available'}));return}
  res.end(JSON.stringify({originals:v.originals,around:v.around}));return}
 if(url.pathname==='/api/email'){res.end(JSON.stringify({html:''}));return}
 const mark=url.pathname.match(/^\/brand\/logos\/mono\/([a-z0-9-]+)\.svg$/);  // the sources' one-color marks, as the Machine serves them
 if(mark){try{res.setHeader('Content-Type','image/svg+xml');res.end(readFileSync(new URL(`../dashboard/logos/mono/${mark[1]}.svg`,import.meta.url)))}catch{res.statusCode=404;res.end()}return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const sizes=shots?[[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark'],[1440,700,'light']]:[[390,844,'dark'],[1440,900,'light'],[1440,500,'dark']];  // 500 high: the thread scrolls
 for(const [width,height,scheme] of sizes){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.locator('#task-'+data.slack.id).waitFor();
  const box=page.locator('#email-content'),dialog=page.locator('#email-dialog');
  const open=async k=>{await page.evaluate(id=>{const d=document.querySelector('#email-dialog');if(d.open)d.close();return openEmail(id)},data[k].id);await box.locator('.convo-say,.email-text').first().waitFor();await page.waitForTimeout(150)};
  const shot=async name=>{if(shots)await page.screenshot({path:`${shots}/${name}-${width}x${height}-${scheme}.png`})};
  // Slack DM: today's five before the to-do's message, it, and the two replies; not yesterday's, another channel or a thread
  await open('slack');await shot('slack');
  assert.equal(await box.locator('.convo-chat').innerText(),'DM with Kai Moreno');
  const said=await box.locator('.convo-say').allInnerTexts();
  assert.deepEqual(said,['Quick one about the bug reports from the phone app','A tester says the report button does nothing on Android','No to-do showed up for it on our side either',
   'Odd. Did they send a screenshot?','Yes, it shows the form filled in and then nothing','I’ll have an agent dig into it','Great, thanks 🙏','Let me know if you need the tester’s device details']);
  assert.doesNotMatch(await box.innerText(),/beta build|Standup|Testers list/);
  const main=box.locator('.convo-main');assert.equal(await main.count(),1);assert.equal(await main.innerText(),'I’ll have an agent dig into it');
  assert.equal(await main.getAttribute('aria-label'),'The message this to-do is about');
  assert.ok(await main.evaluate(n=>{const r=n.getBoundingClientRect(),d=n.closest('dialog').getBoundingClientRect();return r.top>=d.top&&r.bottom<=d.bottom}),'the to-do\'s message is in view');
  assert.equal(await box.locator('a.convo-source').innerText(),'Open in Slack ↗');
  assert.equal(await box.locator('a.convo-source').getAttribute('href'),data.slack.originals[0].url,'the link opens the to-do\'s own message');
  assert.ok(await box.evaluate(n=>n.closest('dialog').scrollWidth<=n.closest('dialog').clientWidth+1),'no sideways scroll');
  if(width<=560)assert.equal(await dialog.evaluate(d=>Math.round(d.getBoundingClientRect().width)),width,'on a phone the sheet is the full width, no scrollbar gutter beside it');
  // Show earlier: yesterday's message above, the day line with it, the screen where it was, then no more button
  const earlier=box.locator('[data-convo-earlier]');assert.equal(await earlier.innerText(),'Show earlier');
  if(width===390){await dialog.evaluate(d=>d.scrollTop=0);await shot('slack-top')}
  await earlier.scrollIntoViewIfNeeded();  // where the click happens: Playwright scrolls to the button first
  const mainTop=await main.evaluate(n=>n.getBoundingClientRect().top),scrolls=await dialog.evaluate(d=>d.scrollHeight>d.clientHeight+1);
  await earlier.click();await box.locator('.convo-say',{hasText:'beta build'}).waitFor();
  assert.equal((await box.locator('.convo-say').allInnerTexts())[0],'Did the beta build go out to the testers yet?');
  assert.equal(await box.locator('.convo-day').count(),2);assert.equal(await earlier.count(),0);
  // A thread that already scrolled keeps its place; one that fit moves down at most by what was added
  const after=await box.locator('.convo-main').evaluate(n=>n.getBoundingClientRect().top);
  if(scrolls)assert.ok(Math.abs(after-mainTop)<2,'what was on screen stays put '+[width,height,mainTop,after]);else assert.ok(after>=mainTop-40,'the older message lands above');
  if(width===390){await dialog.evaluate(d=>d.scrollTop=0);await shot('slack-earlier')}
  // WhatsApp group: the chat's run before the to-do's message and the reply after it, nothing from another account
  await open('whatsapp');await shot('whatsapp');
  assert.equal(await box.locator('.convo-chat').innerText(),'Garden club');
  assert.equal(await box.locator('.convo-say').count(),5);assert.equal(await box.locator('.convo-main').innerText(),'I can pick it up Friday evening');
  assert.doesNotMatch(await box.innerText(),/Work chat/);assert.equal(await box.locator('[data-convo-earlier]').count(),0);
  // Email thread: the two earlier emails folded above, the to-do's own open and marked, the reply folded below
  await open('email');await box.locator('.email-text').waitFor();await shot('email');
  const rows=box.locator('details.email-near');assert.equal(await rows.count(),3);
  assert.deepEqual((await rows.locator(':scope>summary').allInnerTexts()).map(x=>x.split(' · ')[0]),['Avery Stone','You','You']);
  const mail=box.locator('.email-main');assert.match(await mail.innerText(),/Lighting is 300 extra/);
  assert.ok(await box.evaluate(n=>{const k=[...n.children].map(c=>c.matches('.email-main')?'main':c.matches('details.email-near')?'near':'');return k.join(',')==='near,near,main,near'}),'in thread order');
  await rows.first().locator(':scope>summary').click();await rows.first().locator('.email-text').waitFor();
  assert.match(await rows.first().locator('.email-text').innerText(),/2,400 for three days/);
  if(shots){await shot('email-open')}
  // A reply in a thread opens with what it answers: the questions before the thread, the answers that start it, then itself
  await open('thread');await shot('thread');
  const lists=await box.locator('.convo-say').allInnerTexts();
  assert.equal(lists.length,4);assert.match(lists[0],/^Four questions about the digest/);assert.match(lists[2],/^(1\. )?yes, in notifications/);  // a numbered list may draw its numbers itself
  assert.match(await box.locator('.convo-main').innerText(),/release blocker/);assert.doesNotMatch(await box.innerText(),/lunch at noon/);
  // In thread starts the thread after the channel's messages; the to-do's own bubble lines up with the other incoming ones
  assert.deepEqual(await box.evaluate(n=>[...n.querySelectorAll('.convo-thread,.convo-say')].map(e=>e.matches('.convo-thread')?'thread':'say')),['say','say','thread','say','say']);
  const lefts=await box.locator('.convo-turn:not(.me) .convo-say').evaluateAll(l=>l.map(e=>Math.round(e.getBoundingClientRect().left)));
  assert.equal(new Set(lefts).size,1,`incoming bubbles start at ${lefts}`);
  // each sender's initials sit in a circle, and the app's mark shows next to the conversation and on Open in Slack
  assert.equal(await box.locator('.convo-av').first().getAttribute('data-av'),'RC');
  assert.equal(await box.locator('.convo-av').first().evaluate(e=>getComputedStyle(e).borderRadius),'50%');
  await page.waitForFunction(()=>[...document.querySelectorAll('#email-content .convo-chat .via-ico')].some(e=>getComputedStyle(e).maskImage.includes('slack')));
  if(width===390){await dialog.evaluate(d=>d.scrollTop=0);await shot('thread-top')}
  await dialog.evaluate(d=>d.close());
  // The card's link to its own conversation opens the viewer, not Slack; Open in Slack stays at the viewer's foot
  const card=page.locator('#task-'+data.thread.id);await card.scrollIntoViewIfNeeded();
  const here=card.locator('[data-original="read"]',{hasText:'Open original discussion'});
  if(!await here.isVisible())await card.locator('details.more-actions>summary').click();
  if(width===390){await page.waitForTimeout(400);await shot('thread-menu')}
  assert.equal(await here.evaluate(n=>n.tagName),'BUTTON');assert.doesNotMatch(await here.innerText(),/↗/);
  assert.equal(await card.locator('a[href="https://docs.example/spec"]').count(),1,'a link elsewhere still opens outside');
  await here.click();await box.locator('.convo-main').waitFor();await page.waitForTimeout(150);
  assert.equal(await dialog.evaluate(d=>d.open),true);assert.equal(await box.locator('a.convo-source').innerText(),'Open in Slack ↗');
  await shot('thread-from-menu');await dialog.evaluate(d=>d.close());
  await context.close();
 }
 assert.deepEqual(errors,[]);
 assert.ok(asked.length>0,'Show earlier asked the Machine');
 console.log('message context dashboard ok');
}finally{await browser?.close();server.close()}
