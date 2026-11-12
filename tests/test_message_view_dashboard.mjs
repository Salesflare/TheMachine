import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {createServer} from 'node:http';
import {fileURLToPath} from 'node:url';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The message viewer, opened from a row of "Checked N messages" the way the owner opens it, for one made-up message of
// every source kind (tests/test_message_view.py SAMPLES, through the real service): each reads in its own view, says
// every text once (title, header, Details and body), shows no raw ids, Unix times, link brackets or markdown syntax,
// an email names its sender and To by name with Details for the addresses, a chat has its turns by who said them, a
// GitHub issue its repo, state and real author, a notification its app and text once, and code scrolls inside the dialog.
// MESSAGE_VIEW_SHOTS=dir saves a screenshot of each; MESSAGE_VIEW_PAGE=<other dashboard.html> and MESSAGE_VIEW_DATA=<json>
// only take them (a before set).
const root=new URL('../',import.meta.url);
const py=`import sys,tempfile
sys.path[:0]=['.','tests']
import test_message_view as m
with tempfile.TemporaryDirectory() as folder:
    print(m.dump(folder))`;
let data;
if(process.env.MESSAGE_VIEW_DATA)data=JSON.parse(await (await import('node:fs/promises')).readFile(process.env.MESSAGE_VIEW_DATA,'utf8'));
else{const run=spawnSync(process.env.PYTHON||(process.platform==='win32'?'python':'python3'),['-c',py],{cwd:fileURLToPath(root),encoding:'utf8'});
 assert.equal(run.status,0,run.stderr);data=JSON.parse(run.stdout)}
const other=process.env.MESSAGE_VIEW_PAGE,dashboard=await dashboardPage(other||undefined),shots=process.env.MESSAGE_VIEW_SHOTS;
const only=process.env.MESSAGE_VIEW_KINDS?.split(',');
const kinds=Object.keys(data).filter(k=>!only||only.includes(k));
const NOW=Date.parse('2026-11-10T16:20:00Z');
const SOURCE=k=>({email:'email',chat:'chat',notification:'notification'}[data[k].view]||'update');
const threads=kinds.map(k=>({from:data[k].from||data[k].app_name||'',subject:data[k].title,source:SOURCE(k),kind:k,event:data[k].event_id,at:data[k].occurred_at}))
 .concat({from:'nobody@unknown.example',subject:'Hello',source:'email',kind:'gmail.message',event:999999,at:new Date(Date.parse('2026-11-10T16:00:00Z')).toISOString()});  // no name known anywhere
const state={suggestions:[{id:'a1'.repeat(8),title:'Send the export fix notes',body:'',status:'pending',scope:'work',created_at:new Date(NOW-6e5).toISOString(),event_ids:[]}],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{last_completed:new Date(NOW-9*6e4).toISOString()},review_runs:[],review_live:{runs:[]},connectors:[],
 check:{reviewed:new Date(NOW-9*6e4).toISOString(),waiting:0},fleet:{on:false,fleets:[]},
 mail_check:{at:new Date(NOW-9*6e4).toISOString(),read:threads.length,counts:{email:threads.length},todos:0,held:0,held_until:null,more:0,threads},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'24',hour12:false,auto_hour12:false,date_locale:'en-US',languages:{en:'English'},saveable:true}};
const byEvent=Object.fromEntries(Object.values(data).map(o=>[String(o.event_id),o]));
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/originals'){const o=byEvent[url.searchParams.get('event')];res.end(JSON.stringify({originals:o?[o]:[]}));return}
 if(url.pathname==='/api/email'){res.statusCode=404;res.end('{}');return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const norm=s=>String(s).toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim();
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const sizes=shots?[[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]:[[390,844,'dark'],[1440,900,'light']];
 for(const [width,height,scheme] of sizes){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.clock.setFixedTime(NOW);
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/`);
  const line=page.locator('#suggestions .mail-check .mc-line');await line.waitFor();await line.click();await page.locator('#suggestions [data-mc-event]').first().waitFor();
  if(await page.locator('#suggestions [data-mc-all]').count())await page.locator('#suggestions [data-mc-all]').click();
  const dialog=page.locator('#email-dialog'),box=page.locator('#email-content');
  // the list behind it names people too: the name alone, the address only when no name is known
  const whos=await page.locator('#suggestions .mc-who b').allInnerTexts();  assert.ok(whos.length&&whos.every(w=>!/[<>]/.test(w)),`a sender row shows an address next to its name: ${JSON.stringify(whos)}`);
  for(const {from} of threads){const named=/^(.+?)\s*<[^>]+>$/.exec(from);if(named)assert.ok(whos.includes(named[1].replace(/^"|"$/g,'')),`${from} is not named in the list`)}
  assert.ok(whos.includes('nobody@unknown.example'),'no name known: the address');
  for(const k of kinds){const o=data[k];
   if(await dialog.evaluate(d=>d.open))await dialog.evaluate(d=>d.close());
   await page.locator(`#suggestions [data-mc-event="${o.event_id}"]`).click();
   await box.locator('.convo-say,.email-text,.msg-md,.email-meta').first().waitFor();await page.waitForTimeout(120);
   if(shots)await page.screenshot({path:`${shots}/${other?'before':'after'}-${k}-${width}x${height}-${scheme}.png`});
   if(other)continue;
   const title=(await page.locator('#email-title').innerText()).trim(),text=await box.innerText();
   // every visible line once: the title, the header lines, each paragraph or chat turn
   const parts=[title,...await box.locator('.email-from strong,.email-to,.email-subject,.msg-note-title,.msg-why,.email-text p,.msg-md>p,.msg-md li,.convo-say').allInnerTexts()].map(norm).filter(s=>s.length>2);
   assert.equal(parts.length,new Set(parts).size,`${k} says something twice: ${JSON.stringify(parts)}`);
   assert.doesNotMatch(title+'\n'+text,/(?<!\d)1[5-9]\d{8}(?!\d)|<[@#!][A-Z0-9^]|<https?:|\*\*|```|\]\(https?:|\b[UWC]0[A-Z0-9]{8,10}\b|conversation_attribute|why you got it|^\[[\w.-]+\]/m,`${k} shows raw syntax or ids`);
   assert.ok(title.length>0&&!title.endsWith('…'),k);
   // "Open in …" sits left, under the content, for every kind
   const open=box.locator('.read-original').last();
   if(await open.count())assert.ok(await open.evaluate(a=>{const b=document.getElementById('email-content'),r=b.getBoundingClientRect();return Math.abs(a.getBoundingClientRect().left-r.left-parseFloat(getComputedStyle(b).paddingLeft))<=2}),`${k}: the open link is not left-aligned`);
   // nothing widens the dialog: long code scrolls inside it
   assert.ok(await dialog.evaluate(d=>d.scrollWidth<=d.clientWidth+1),`${k} widens the dialog`);
   if(o.view==='email'){assert.equal(await box.locator('.email-addr').count(),1,k);assert.equal(title,o.title,k)}
   if(o.view==='chat')assert.ok(await box.locator('.convo-say').count()>=1,k);
  }
  if(!other){const shown=k=>kinds.includes(k)?data[k]:undefined;  // only the kinds this run shows
   // The CRM email: subject as the title once, the sender by name with the address quiet, "to Dana, Mira", headers out of the text
   const crm=shown('salesflare.email');if(crm){
    await dialog.evaluate(d=>d.close());await page.locator(`#suggestions [data-mc-event="${crm.event_id}"]`).click();await box.locator('.email-text').waitFor();
    assert.equal(await page.locator('#email-title').innerText(),'Checking in on your setup');
    assert.equal(await box.locator('.email-who').innerText(),'Sam Rivera sam@client.example');
    assert.equal(await box.locator('.email-to').innerText(),'to Dana, Mira');
    assert.doesNotMatch(await box.locator('.email-text').innerText(),/^(From|To):/m);
    assert.equal(await box.locator('.email-text p').count(),3,'paragraphs');
    assert.equal(await box.locator('.email-headers').count(),1);await box.locator('.email-headers summary').click();
    assert.match(await box.locator('.email-headers').innerText(),/Dana Reyes <dana@team\.example>/);
    assert.doesNotMatch(await box.locator('.email-headers').innerText(),/From/);
    assert.equal(await box.locator('.email-open a').innerText(),'Open in Salesflare ↗')}
   // Intercom: the customer on one side, the team named on the other, the bot marked, no system parts, via Facebook
   const ic=shown('intercom.conversation');if(ic){
    await dialog.evaluate(d=>d.close());await page.locator(`#suggestions [data-mc-event="${ic.event_id}"]`).click();await box.locator('.convo-say').first().waitFor();
    assert.equal(await page.locator('#email-title').innerText(),'Jordan Lake');
    assert.match(await box.locator('.convo-chat').innerText(),/Intercom\s*via Facebook/);
    assert.equal(await box.locator('.convo-say').count(),4);
    assert.deepEqual(await box.locator('.convo-turn').evaluateAll(ts=>ts.map(t=>t.classList.contains('me'))),[false,true,true,false]);
    assert.match(await box.locator('.convo-turn.me').first().innerText(),/Fin Bot/);
    assert.doesNotMatch(await box.innerText(),/^Facebook$|assignment|Jordan Lake\nFacebook/m)}
   // GitHub: the title without [repo], repo #number, state, the commenting bot marked, the comment first, the issue folded
   const gh=shown('github.notification');if(gh){
    await dialog.evaluate(d=>d.close());await page.locator(`#suggestions [data-mc-event="${gh.event_id}"]`).click();await box.locator('.msg-md').first().waitFor();
    assert.equal(await page.locator('#email-title').innerText(),'Exports stop at 10,000 rows when the report has filters');
    assert.match(await box.locator('.email-from').innerText(),/acme\/widgets #812\s*Open/);
    assert.match(await box.locator('.email-to').innerText(),/^Comment by sweeper\s*Bot$/);
    assert.match(await box.locator('.email-open a').getAttribute('class'),/\bvia-github\b/,'the link has GitHub\'s own icon');
    assert.equal(await box.locator('.msg-why').innerText(),'You opened it');
    await box.locator('.msg-context summary').click();
    assert.equal(await box.locator('.msg-context pre.md-code').count(),1);assert.equal(await box.locator('.msg-context ol li').count(),2);
    assert.equal(await box.locator('.msg-context code').first().innerText(),'export --all')}
   // Slack: the person, not the channel; links without brackets; names for mentions; emoji
   const sl=shown('slack.message');if(sl){
    await dialog.evaluate(d=>d.close());await page.locator(`#suggestions [data-mc-event="${sl.event_id}"]`).click();await box.locator('.convo-say').first().waitFor();
    assert.equal(await page.locator('#email-title').innerText(),'#development-planning');
    assert.match(await box.locator('.convo-meta').innerText(),/^Rowan Vale ·/);
    assert.equal(await box.locator('.convo-say a[href="https://tracker.example/b/12"]').innerText(),'the board');
    assert.match(await box.locator('.convo-say').innerText(),/🗓️.*@Kit Navarro.*@someone on Slack/s);
    assert.equal(await box.locator('.convo-say strong').innerText(),'Ship it');assert.equal(await box.locator('.convo-say del').innerText(),'maybe');
    assert.match(await box.locator('.convo-source').getAttribute('class'),/\bvia-slack\b/,'the link has Slack\'s own icon')}
   // An address sent without a name: the name the Graph knows, the address only when none is known
   const bare=shown('gmail.message#bare');if(bare){
    await dialog.evaluate(d=>d.close());await page.locator(`#suggestions [data-mc-event="${bare.event_id}"]`).click();await box.locator('.email-text').waitFor();
    assert.match(await box.locator('.email-who').innerText(),/^Avery Stone\s+avery@booths\.example$/);
    assert.equal(await box.locator('.email-to').innerText(),'to Robin, nobody@unknown.example')}
   // A phone notification: the app and its text once
   const n=shown('android.notification');if(n){
    await dialog.evaluate(d=>d.close());await page.locator(`#suggestions [data-mc-event="${n.event_id}"]`).click();await box.locator('.email-meta').waitFor();
    assert.equal(await page.locator('#email-title').innerText(),'Your daily digest is ready');
    assert.equal(await box.locator('.msg-app').innerText(),'Medium');assert.equal(await box.locator('.email-headers').count(),0)}
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('message view dashboard ok');
