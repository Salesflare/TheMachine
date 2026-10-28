import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Help: Ask shows the answer with links to the help pages it used (only themachine.computer/help and the app's code);
// Report a bug sends on Send at once: the form closes and a quiet line says so, while the Machine adds the support
// report (one box, ticked by default) without the owner waiting for it; nothing is lost when it is slow or fails. An
// error toast opens it.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const actions=[];let limit=false,queued=[],cpOk=false,previewMs=0,previewFails=false;  // limit: the control plane said 429, so the Machine keeps the report
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');let body='';
 req.on('data',c=>body+=c);req.on('end',()=>{
  if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
  res.setHeader('Content-Type','application/json');
  if(url.pathname==='/_machine/bug'){actions.push({action:'cp',args:JSON.parse(body)});if(cpOk){res.end('{"id":"r_1"}');return}res.writeHead(429,{'Retry-After':'900'});res.end('{"error":"You sent a few reports just now.","retry_after":900}');return}
  if(url.pathname==='/api/action'&&/"action":"client_error"/.test(body)){res.end('{"ok":true,"counted":0}');return}  // an error report (test_client_errors_dashboard.mjs), not a change
  if(url.pathname==='/api/action'){const {action,args}=JSON.parse(body||'{}');if(action==='bug_queued'){res.end(JSON.stringify({queued}));return}actions.push({action,args,upload:req.headers['x-upload']});
   const later=Math.floor(Date.UTC(2030,0,1,10,55)/1000);
   if(action==='bug_later'||action==='bug_send'&&limit){queued=[{id:'bq_1',what:args.description,next_at:later}];res.end(JSON.stringify({sent:false,queued:true,at:later}));return}
   if(action==='help_ask'&&/comes back/.test(args.question)){res.end(JSON.stringify({answer:'Try a reload.',bug:'I snoozed a to-do until tomorrow.\nI expected it to stay away.\nIt came back within a minute.',sources:[]}));return}
   if(action==='help_ask'){setTimeout(()=>res.end(JSON.stringify({answer:'Press **Snooze**, then pick a time.\n\n- See [Snooze](https://themachine.computer/help/snooze)\n- Not [this](https://evil.example/y)',sources:[{kind:'help',title:'Snooze',url:'https://themachine.computer/help/snooze#snooze-a-to-do'},{kind:'help',title:'Bad',url:'https://evil.example/x'}]})),300);return}
   if(action==='help_article'){res.end(JSON.stringify(args.slug==='gmail'?{slug:'gmail',title:'Gmail',summary:'',body:'## Gmail koppelen\n\nOpen Koppelingen.',anchors:['connect-gmail'],lang:'nl'}
    :{slug:'snooze',title:'Snoozen',summary:'Zet een to-do weg.',body:'Intro.\n\n## Een to-do snoozen\n\nDruk op **Snoozen**. Zie [Gmail](gmail.md#connect-gmail) of [x](javascript:alert(1)).\n\n## Wanneer hij terugkomt\n\n- Op Telegram\n- Als melding',anchors:['snooze-a-to-do','when-it-comes-back'],lang:'nl'}));return}
   if(action==='bug_preview'&&previewFails){res.statusCode=500;res.end('{"error":"boom"}');return}
   if(action==='bug_preview'){setTimeout(()=>res.end(JSON.stringify({parts:{'service-log':['ERROR send failed token=[redacted]']},settings:{model:'openai/gpt-5'},paired:true})),previewMs);return}
   if(action==='bug_send'){res.end(JSON.stringify({sent:true,id:'s_1'}));return}}
  if(url.pathname==='/api/status'){res.end(JSON.stringify({fleet:{on:false}}));return}  // paired with the Network
  res.end(url.pathname==='/api/events'?'[]':'{}')})});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  actions.length=0;
  const phone=width<600,context=await browser.newContext({viewport:{width,height:844},isMobile:phone,hasTouch:phone}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof toast==='function'&&document.querySelector('#open-help'));
  await page.evaluate(()=>document.querySelector('#open-help').click());await page.waitForSelector('#help-panel[open]');
  // One composer like the card chat's: Send waits for text, Enter asks, Shift+Enter is a new line
  assert.equal(await page.isDisabled('#help-go'),true,'nothing to ask yet');
  await page.fill('#help-q','How do I');await page.press('#help-q','Shift+Enter');await page.type('#help-q','snooze a to-do?');
  assert.equal(await page.inputValue('#help-q'),'How do I\nsnooze a to-do?');assert.equal(actions.length,0,'Shift+Enter only adds a line');
  await page.press('#help-q','Enter');
  // While it looks up: the typing dots in the answer's place, not a bordered box
  await page.waitForSelector('#help-log .chat-msg.machine .typing[role=status]');
  await page.waitForSelector('.help-log .chat-files a');
  assert.equal(await page.$eval('#help-log .chat-msg.you .bubble',b=>b.textContent),'How do I\nsnooze a to-do?');
  // The answer as markdown; links in it only to the help pages, any other keeps its words
  const answer=await page.$eval('#help-log .chat-msg.machine .bubble',b=>({bold:b.querySelector('strong')?.textContent,items:b.querySelectorAll('li').length,links:[...b.querySelectorAll('a')].map(a=>a.href),text:b.textContent,tr:b.getAttribute('translate')}));
  assert.equal(answer.bold,'Snooze');assert.equal(answer.items,2);assert.deepEqual(answer.links,['https://themachine.computer/help/snooze']);
  assert.ok(answer.text.includes('Not this'));assert.equal(answer.tr,'no','the page translation leaves the answer alone');
  const links=await page.$$eval('.help-log .chat-files a',as=>as.map(a=>[a.href,a.target,a.rel]));
  assert.deepEqual(links,[['https://themachine.computer/help/snooze#snooze-a-to-do','_blank','noopener']],'only help and code links show');
  assert.equal(actions[0].action,'help_ask');
  // Asked while Help still answers: shows as sent at once, and is answered right after, in order, with the first answer as history
  actions.length=0;
  await page.fill('#help-q','How do I snooze a to-do?');await page.press('#help-q','Enter');
  await page.waitForSelector('#help-log .typing');
  await page.fill('#help-q','And how do I wake it early?');await page.press('#help-q','Enter');
  assert.equal(await page.inputValue('#help-q'),'','the second question left the box');
  assert.deepEqual(await page.$$eval('#help-log .chat-msg.you .bubble',b=>b.slice(-2).map(x=>x.textContent)),['How do I snooze a to-do?','And how do I wake it early?'],'shown as sent');
  await page.waitForFunction(()=>document.querySelectorAll('#help-log .chat-msg.machine .bubble:not(.typing)').length===3&&!document.querySelector('#help-log .typing'));
  assert.deepEqual(actions.map(a=>a.args.question),['How do I snooze a to-do?','And how do I wake it early?'],'one at a time, in order');
  assert.equal(actions[1].args.history.at(-1).role,'assistant','the second gets the first answer as history');
  assert.deepEqual(await page.$$eval('#help-log .chat-msg',m=>m.slice(-4).map(x=>x.classList.contains('you')?'you':'machine')),['you','machine','you','machine'],'each answer under its question');
  actions.length=1;
  assert.equal(await page.$('#help-log [data-help-bug]'),null,'a how-to answer offers no bug report');
  // A bug: the answer ends with Report this bug, which prefills Report a bug to edit; nothing goes before Send
  await page.fill('#help-q','My snoozed to-do comes back at once');await page.press('#help-q','Enter');
  await page.waitForSelector('#help-log [data-help-bug]');assert.equal(await page.$$eval('#help-log [data-help-bug]',b=>b.length),1);
  await page.click('#help-log [data-help-bug]');assert.equal(await page.isHidden('#help-ask-pane'),true);
  assert.equal(await page.inputValue('#bug-what'),'I snoozed a to-do until tomorrow.\nI expected it to stay away.\nIt came back within a minute.');
  assert.equal(await page.isChecked('#bug-diag'),true,'the support report is in by default');
  assert.deepEqual(actions.map(a=>a.action).filter(a=>a!=='support_access'),['help_ask','help_ask'],'nothing sent from the chat');
  await page.fill('#bug-what','');await page.click('[data-help-tab="ask"]');actions.length=1;
  // Report a bug: a click on the tab works (the panel doesn't move under it); one box, ticked, says what it gives
  await page.click('[data-help-tab="bug"]');assert.equal(await page.isHidden('#help-ask-pane'),true);
  assert.equal(await page.$$eval('#bug-form input[type=checkbox]',b=>b.length),1,'one box for the support report and the 24 hours');
  assert.equal(await page.isChecked('#bug-diag'),true);
  assert.match(await page.textContent('#bug-diag-fine'),/read-only logs for 24 hours/);
  // Send: the form closes at once and says Sent; the self-hosted Machine keeps it and adds the support report itself
  await page.fill('#bug-what','The Calendar shows yesterday.');const t0=Date.now();await page.click('#bug-send');
  await page.waitForSelector('#help-panel:not([open])',{state:'attached',timeout:1000});await page.waitForSelector('#toast.show');
  assert.ok(Date.now()-t0<1000,'no waiting for the support report');
  assert.equal(await page.textContent('#toast'),'Sent, thanks. You’ll see it here when it’s fixed.');
  let sent=actions.find(a=>a.action==='bug_send');
  assert.equal(sent.action,'bug_send');assert.equal(sent.upload,'bug-report');
  assert.equal(sent.args.description,'The Calendar shows yesterday.');assert.equal(sent.args.diagnostics,true);assert.equal(sent.args.report,undefined);
  assert.ok(!actions.some(a=>a.action==='bug_preview'),'the page doesn’t build it');
  assert.equal(await page.inputValue('#bug-what'),'','the form starts empty next time');
  // Unticked: no support report and no access
  await page.evaluate(()=>document.querySelector('#open-help').click());await page.click('[data-help-tab="bug"]');
  actions.length=0;await page.evaluate(()=>document.querySelector('#toast').classList.remove('show'));await page.fill('#bug-what','Again.');await page.uncheck('#bug-diag');await page.click('#bug-send');await page.waitForSelector('#help-panel:not([open])',{state:'attached'});
  await page.waitForFunction(n=>document.querySelector('#toast.show'),null);
  assert.equal(actions.find(a=>a.action==='bug_send').args.diagnostics,false,'no report when unticked');
  assert.ok(!actions.some(a=>a.action==='support_access'&&a.args.allow!==undefined),'no access when unticked');
  // A new report has the box ticked again
  await page.evaluate(()=>document.querySelector('#open-help').click());await page.click('[data-help-tab="bug"]');assert.equal(await page.isChecked('#bug-diag'),true);
  await page.keyboard.press('Escape');
  // An error toast offers it, with what it said
  await page.evaluate(()=>toast('Couldn’t save that. Try again.',true));await page.click('#toast [data-bug-report]');
  await page.waitForSelector('#help-panel[open]');
  assert.match(await page.inputValue('#bug-what'),/Couldn’t save that/);
  await page.evaluate(()=>toast('Saved.'));assert.equal(await page.$('#toast [data-bug-report]'),null,'only errors offer it');
  await page.fill('#bug-what','');
  // Hosted: kept on this device first; Sending shows before the slow support report, Sent only after the receipt
  cpOk=true;previewMs=4000;actions.length=0;await page.evaluate(()=>{state.manage_url='https://app.example/setup';localStorage.removeItem('bug-later');bugPage=[];document.querySelector('#toast').classList.remove('show')});
  await page.click('[data-help-tab="bug"]');await page.fill('#bug-what','Hosted report.');const t1=Date.now();await page.click('#bug-send');
  await page.waitForFunction(()=>document.querySelector('#toast.show')?.textContent==='Saved. Sending…');
  assert.ok(!actions.some(a=>a.action==='cp'),'not called Sent before the report and provider receipt');
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('bug-later')).length),1,'kept on the device until it is out');
  await page.waitForFunction(()=>!JSON.parse(localStorage.getItem('bug-later')||'[]').length);
  await page.waitForFunction(()=>document.querySelector('#toast')?.textContent==='Sent, thanks. You’ll see it here when it’s fixed.');
  sent=actions.find(a=>a.action==='cp');assert.equal(sent.args.description,'Hosted report.');assert.deepEqual(sent.args.report.settings,{model:'openai/gpt-5'});
  assert.equal(sent.args.diag,undefined);
  // The support report fails: what the owner wrote still goes, saying so
  previewMs=0;previewFails=true;actions.length=0;
  await page.evaluate(()=>document.querySelector('#open-help').click());await page.click('[data-help-tab="bug"]');await page.fill('#bug-what','Report without its report.');await page.click('#bug-send');
  await page.waitForFunction(()=>!JSON.parse(localStorage.getItem('bug-later')||'[]').length);
  sent=actions.find(a=>a.action==='cp');assert.equal(sent.args.description,'Report without its report.');assert.deepEqual(sent.args.report,{parts:{report:['not built']}});
  previewFails=false;cpOk=false;
  // At the control plane's limit (or offline) the report is never lost: kept on the Machine, said plainly, shown as waiting
  const goesAt=await page.evaluate(()=>fmtHM(Date.UTC(2030,0,1,10,55)));
  for(const hosted of [false,true]){limit=true;queued=[];actions.length=0;await page.evaluate(h=>{state.manage_url=h?'https://app.example/setup':null},hosted);
   await page.evaluate(()=>{document.querySelector('#toast').classList.remove('show');document.querySelector('#open-help').click()});
   await page.click('[data-help-tab="bug"]');await page.fill('#bug-what','Fourth report.');await page.click('#bug-send');
   await page.waitForFunction(at=>document.querySelector('#toast.show')?.textContent===`Saved. It goes out by itself at ${at}.`,goesAt);
   assert.deepEqual(actions.map(a=>a.action).filter(a=>a!=='bug_preview'&&a!=='support_access'),hosted?['cp','bug_later']:['bug_send']);
   if(hosted)assert.equal(actions.at(-1).args.retry_after,900,'the control plane’s Retry-After goes with it');
   await page.evaluate(()=>document.querySelector('#open-help').click());await page.click('[data-help-tab="bug"]');await page.waitForSelector('#bug-queued:not([hidden])');
   assert.equal(await page.textContent('#bug-queued li'),`Fourth report. · Goes out at ${goesAt}`);await page.keyboard.press('Escape')}
  // In another language a help link anywhere opens the article here, in that language, at its heading; a link in it to
  // another article opens that one; Back returns to Ask. Only in English it opens the site.
  await page.evaluate(()=>{I18N.lang='nl';helpBox.close();const a=document.createElement('a');a.href='https://themachine.computer/help/snooze#when-it-comes-back';a.id='help-link-test';a.textContent='Help';document.body.append(a);a.click()});
  await page.waitForSelector('#help-panel[open] #help-read h4');
  assert.equal(await page.isHidden('#help-ask-pane'),true);
  assert.deepEqual(await page.$$eval('#help-read h4',h=>h.map(x=>x.id+' '+x.textContent)),['help-a-snooze-a-to-do Een to-do snoozen','help-a-when-it-comes-back Wanneer hij terugkomt']);
  assert.equal(await page.$eval('#help-read b',b=>b.textContent),'Snoozen');
  assert.equal(await page.$('#help-read a[href^="javascript"]'),null,'only help, https and mailto links');
  assert.equal(await page.getAttribute('#help-read-site','href'),'https://themachine.computer/help/snooze#when-it-comes-back');
  await page.click('#help-read a[data-help-slug="gmail"]');await page.waitForFunction(()=>document.querySelector('#help-read h3')?.textContent==='Gmail');
  assert.deepEqual(actions.filter(a=>a.action==='help_article').map(a=>a.args.slug),['snooze','gmail']);
  await page.click('[data-help-back]');assert.equal(await page.isVisible('#help-ask-pane'),true);assert.equal(await page.isHidden('#help-read-pane'),true);
  await page.evaluate(()=>{I18N.lang='en';helpBox.close();document.getElementById('help-link-test').remove()});
  limit=false;queued=[];await page.evaluate(()=>{state.manage_url=null});
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('help dashboard: ok');
}finally{await browser?.close();server.close()}
