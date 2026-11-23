import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import {createServer} from 'node:http';
import {fileURLToPath} from 'node:url';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A message opened from a list reads like a to-do's: the check's WhatsApp row with two new messages opens its chat, what
// was said before and between them, both marked; a Slack row with a thread reply its DM and that thread; an email its
// thread, the opened one open between the folded ones; and the same from the Graph (one message, a run, an email). Show
// earlier pages it, nothing is marked as read, the dialog is in the middle of the window, and its title is said once.
// Answers come from the real handler (tests/test_message_context.py dump_opened, made-up messages).
// MESSAGE_OPENED_SHOTS=dir saves screenshots.
const root=new URL('../',import.meta.url);
const py=`import sys,tempfile
sys.path[:0]=['.','tests']
import test_message_context as c
with tempfile.TemporaryDirectory() as folder:
    print(c.dump_opened(folder))`;
const run=spawnSync(process.env.PYTHON||(process.platform==='win32'?'python':'python3'),['-c',py],{cwd:fileURLToPath(root),encoding:'utf8'});
assert.equal(run.status,0,run.stderr);
const data=JSON.parse(run.stdout),answers=Object.fromEntries(Object.values(data).map(v=>[v.query,v]));
const NOW=Date.parse('2026-11-04T15:00:00Z'),at=m=>new Date(NOW-m*6e4).toISOString();
const ids=q=>(/events=([\d,]+)/.exec(q)||/event=(\d+)/.exec(q))[1],last=q=>+ids(q).split(',').at(-1);
const row=(k,rest)=>({event:last(data[k].query),...(ids(data[k].query).includes(',')?{n:ids(data[k].query).split(',').length,ids:ids(data[k].query)}:{}),...rest});
const rows={two:row('two',{from:'Bo Lindqvist',subject:'Perfect, I’ll leave it by the gate',source:'chat',kind:'whatsapp.message',at:at(30)}),
 threads:row('threads',{from:'Kai Moreno',subject:'Let me know if you need the tester’s device details',source:'chat',kind:'slack.message',at:at(90)}),
 mail:row('mail',{from:'Avery Stone',subject:'Booth for the spring fair',source:'email',kind:'gmail.message',at:at(120)})};
const read=Object.values(rows).reduce((n,r)=>n+(r.n||1),0);
const state={suggestions:[{id:'a1'.repeat(8),title:'Send the launch notes',body:'',status:'pending',scope:'work',created_at:at(10),event_ids:[]}],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],
 review_health:{last_completed:at(9)},review_runs:[],review_live:{runs:[]},connectors:[],check:{reviewed:at(9),waiting:0},fleet:{on:false,fleets:[]},
 mail_check:{at:at(9),read,counts:{chat:read-1,email:1},todos:0,held:0,held_until:null,more:0,threads:Object.values(rows)},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'24',hour12:false,auto_hour12:false,date_locale:'en-US',languages:{en:'English'},saveable:true}};
const runIds=ids(data.run.query).split(',').map(Number),day=t=>`2026-11-04T${t}:00Z`;
const person={id:'wa:3247000001',kind:'person',name:'Bo Lindqvist',strength:2,closeness:'close',last_at:day('08:22'),signals:9,ids:['+3247000001'],links:[],open:{cards:[]},log:[],
 recent:[{id:runIds[1],account_id:'home-wa',kind:'whatsapp.message',occurred_at:day('08:22'),title:'Garden club',from:'Bo Lindqvist',from_me:false,preview:'Perfect, I’ll leave it by the gate',thread:'home-wa:whatsapp.message:g'},
  {id:runIds[0],account_id:'home-wa',kind:'whatsapp.message',occurred_at:day('08:20'),title:'Garden club',from:'You',from_me:true,preview:'I can pick it up Friday evening',thread:'home-wa:whatsapp.message:g'},
  {id:last(data.mail.query),account_id:'work',kind:'gmail.message',occurred_at:day('08:45'),title:'Booth for the spring fair',from:'Avery Stone',from_me:false,preview:'Lighting is 300 extra.'},
  {id:last(data.dm.query),account_id:'work-slack',kind:'slack.message',occurred_at:day('06:00'),title:'#DM Kai Moreno: Great',from:'Kai Moreno',from_me:false,dm:true,preview:'Great, thanks'}].sort((a,b)=>b.occurred_at.localeCompare(a.occurred_at))};
const dashboard=await dashboardPage(),shots=process.env.MESSAGE_OPENED_SHOTS;
let asked=[],posted=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')?person:{projects:[],people:[person],quiet:[],new:[],orgs:[]}));return}
 if(url.pathname==='/api/originals'){const q=decodeURIComponent(url.search.slice(1));asked.push(q);const a=answers[q];
  if(!a){res.statusCode=404;res.end('{"error":"Original not available"}');return}
  res.end(JSON.stringify({originals:a.originals,around:a.around}));return}
 if(url.pathname==='/api/email'){res.end('{"html":""}');return}
 if(req.method==='POST'){posted.push(url.pathname)}
 const mark=url.pathname.match(/^\/brand\/logos\/mono\/([a-z0-9_-]+)\.svg$/);  // the sources' one-color marks, as the Machine serves them
 if(mark){try{res.setHeader('Content-Type','image/svg+xml');res.end(readFileSync(new URL(`../dashboard/logos/mono/${mark[1]}.svg`,import.meta.url)))}catch{res.statusCode=404;res.end()}return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const sizes=shots?[[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark'],[2560,1300,'light']]:[[390,844,'dark'],[1440,900,'light'],[2560,1300,'light']];
 for(const [width,height,scheme] of sizes){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US',timezoneId:'UTC'});
  await context.clock.setFixedTime(NOW);
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const dialog=page.locator('#email-dialog'),box=page.locator('#email-content'),title=page.locator('#email-title');
  const shot=async name=>{if(shots)await page.screenshot({path:`${shots}/${name}-${width}x${height}-${scheme}.png`})};
  const close=async()=>{await dialog.evaluate(d=>d.close())};
  const says=()=>box.locator('.convo-say').evaluateAll(l=>l.map(e=>(e.querySelector('.convo-said')||e).innerText.trim()));
  const inView=n=>n.evaluate(e=>{const r=e.getBoundingClientRect(),d=e.closest('dialog').getBoundingClientRect();return r.top>=d.top&&r.bottom<=d.bottom+1});
  // in the middle of the window, wherever the page's content column sits
  const centered=async()=>{const r=await dialog.evaluate(d=>{const b=d.getBoundingClientRect();return {x:(b.left+b.right)/2,y:(b.top+b.bottom)/2,w:b.width}});
   assert.ok(Math.abs(r.x-width/2)<=8,  // the page keeps a scrollbar's width free on the right
`the dialog is in the middle at ${width}: ${JSON.stringify(r)}`);if(width>560)assert.ok(Math.abs(r.y-height/2)<=1,`and from top to bottom: ${JSON.stringify(r)}`)};
  await page.goto(`http://127.0.0.1:${server.address().port}/`);
  const line=page.locator('#suggestions .mail-check .mc-line');await line.waitFor();
  assert.deepEqual(asked,[],'nothing is read before a tap');
  await line.click();await page.locator('#suggestions [data-mc-event]').first().waitFor();
  const tap=async k=>{asked=[];await page.locator('#suggestions [data-mc-event]').nth(Object.keys(rows).indexOf(k)).click();await box.locator('.convo-say,.email-text').first().waitFor();await page.waitForFunction(()=>!document.querySelector('#email-content').getAnimations({subtree:true}).length)};
  const closed=()=>page.waitForFunction(()=>!document.querySelector('#email-dialog').open);
  // WhatsApp, two new messages: the chat before them, the owner's own between, both new ones marked under one line
  await tap('two');await shot('check-whatsapp');
  assert.deepEqual(asked,[data.two.query]);
  assert.deepEqual(await says(),['Who has the long ladder?','Mine is in the shed, happy to lend it','Can someone bring it Saturday at 9?','I can pick it up Friday evening','Perfect, I’ll leave it by the gate']);
  assert.deepEqual(await box.locator('.convo-main .convo-said').allInnerTexts(),['Can someone bring it Saturday at 9?','Perfect, I’ll leave it by the gate']);
  assert.deepEqual(await box.locator('.convo-this').allInnerTexts(),['New messages']);
  assert.equal(await box.locator('.convo-main').first().getAttribute('aria-label'),'New messages');
  assert.equal(await title.innerText(),'Garden club');assert.equal((await box.innerText()).split('Garden club').length,1,'the title is said once');
  assert.ok(await inView(box.locator('.convo-main').first()),'the first new one is in view');
  assert.ok(await dialog.evaluate(d=>d.scrollWidth<=d.clientWidth+1),'no sideways scroll');
  await centered();await close();await closed();
  // Slack, two in the DM and a reply in a thread: the DM, then that thread under its own line, every new one marked
  await tap('threads');await shot('check-slack');
  assert.deepEqual(asked,[data.threads.query]);
  assert.deepEqual(await box.locator('.convo-main').allInnerTexts(),['Great, thanks 🙏','Let me know if you need the tester’s device details','Testers list attached in this thread']);
  assert.deepEqual(await box.evaluate(n=>[...n.querySelectorAll('.convo-thread,.convo-say')].slice(-3).map(e=>e.matches('.convo-thread')?'thread':'say')),['thread','say','say']);
  assert.equal(await title.innerText(),'DM with Kai Moreno');
  assert.doesNotMatch(await box.innerText(),/Standup|beta build/);await centered();await close();await closed();
  // An email: its thread folded around it, the opened one open and marked
  await tap('mail');await shot('check-email');
  assert.deepEqual(asked,[data.mail.query]);
  assert.ok(await box.evaluate(n=>{const k=[...n.children].map(c=>c.matches('.email-main')?'main':c.matches('details.email-near')?'near':'');return k.join(',')==='near,near,main,near'}),'in thread order');
  assert.equal(await box.locator('.email-main').getAttribute('aria-label'),'This message');
  assert.equal(await title.innerText(),'Booth for the spring fair');assert.equal((await box.locator('.email-main').innerText()).includes('Booth for the spring fair'),false,'the subject is said once');
  await centered();await close();await closed();
  // The Graph: a run of a chat, one Slack message, an email
  await page.goto(`http://127.0.0.1:${server.address().port}/#graph/wa%3A3247000001`);await page.locator('.graph-events .graph-event').first().waitFor();
  const graph=async(sel)=>{asked=[];await page.locator(`.graph-events .graph-event${sel}`).first().click();await box.locator('.convo-say,.email-text').first().waitFor();await page.waitForFunction(()=>!document.querySelector('#email-content').getAnimations({subtree:true}).length)};
  await graph('[data-events]');await shot('graph-run');
  assert.deepEqual(asked,[data.run.query]);
  assert.equal((await says()).length,5,'the run with what was said before it');assert.equal(await box.locator('.convo-main').count(),0,'a conversation marks none');
  assert.equal(await title.innerText(),'Garden club');assert.ok(await inView(box.locator('.convo-from').first()),'it opens on the run');
  await close();await closed();
  await graph(`[data-event="${last(data.dm.query)}"]`);await shot('graph-slack');
  assert.deepEqual(asked,[data.dm.query]);
  assert.equal(await box.locator('.convo-main').innerText(),'Great, thanks 🙏');assert.deepEqual(await box.locator('.convo-this').allInnerTexts(),['This message']);
  assert.ok((await says()).length>5&&await inView(box.locator('.convo-main')));
  const n=(await says()).length;await box.locator('[data-convo-earlier]').click();await box.locator('.convo-say',{hasText:'beta build'}).waitFor();
  assert.deepEqual(asked,[data.dm.query,data.dm_earlier.query],'Show earlier pages the opened conversation');
  assert.equal((await says()).length,n+1);assert.equal(await box.locator('.convo-main').count(),1);assert.equal(await box.locator('[data-convo-earlier]').count(),0);await centered();
  await close();await closed();
  await graph(`[data-event="${last(data.mail.query)}"]`);await shot('graph-email');
  assert.equal(await box.locator('details.email-near').count(),3);await centered();
  await close();asked=[];await context.close();
 }
 assert.deepEqual(errors,[]);assert.deepEqual(posted,[],'reading one changes nothing');
 console.log('message opened dashboard ok');
}finally{await browser?.close();server.close()}
