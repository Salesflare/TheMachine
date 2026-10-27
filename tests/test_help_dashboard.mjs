import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Help: Ask shows the answer with links to the help pages it used (only themachine.computer/help and the app's code);
// Report a bug shows everything that goes before anything goes, and sends only on Send; an error toast opens it.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const actions=[];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');let body='';
 req.on('data',c=>body+=c);req.on('end',()=>{
  if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
  res.setHeader('Content-Type','application/json');
  if(url.pathname==='/api/action'){const {action,args}=JSON.parse(body||'{}');actions.push({action,args,upload:req.headers['x-upload']});
   if(action==='help_ask'&&/comes back/.test(args.question)){res.end(JSON.stringify({answer:'Try a reload.',bug:'I snoozed a to-do until tomorrow.\nI expected it to stay away.\nIt came back within a minute.',sources:[]}));return}
   if(action==='help_ask'){setTimeout(()=>res.end(JSON.stringify({answer:'Press **Snooze**, then pick a time.\n\n- See [Snooze](https://themachine.computer/help/snooze)\n- Not [this](https://evil.example/y)',sources:[{kind:'help',title:'Snooze',url:'https://themachine.computer/help/snooze#snooze-a-to-do'},{kind:'help',title:'Bad',url:'https://evil.example/x'}]})),300);return}
   if(action==='bug_preview'){res.end(JSON.stringify({parts:{'service-log':['ERROR send failed token=[redacted]']},settings:{model:'openai/gpt-5'},paired:true}));return}
   if(action==='bug_send'){res.end(JSON.stringify({sent:true,id:'s_1'}));return}}
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
  assert.equal(await page.$('#help-log [data-help-bug]'),null,'a how-to answer offers no bug report');
  // A bug: the answer ends with Report this bug, which prefills Report a bug to edit; nothing goes before Send
  await page.fill('#help-q','My snoozed to-do comes back at once');await page.press('#help-q','Enter');
  await page.waitForSelector('#help-log [data-help-bug]');assert.equal(await page.$$eval('#help-log [data-help-bug]',b=>b.length),1);
  await page.click('#help-log [data-help-bug]');assert.equal(await page.isHidden('#help-ask-pane'),true);
  assert.equal(await page.inputValue('#bug-what'),'I snoozed a to-do until tomorrow.\nI expected it to stay away.\nIt came back within a minute.');
  assert.equal(await page.isChecked('#bug-diag'),true,'the support report is in by default');
  assert.deepEqual(actions.map(a=>a.action),['help_ask','help_ask'],'nothing sent from the chat');
  await page.fill('#bug-what','');await page.click('[data-help-tab="ask"]');actions.length=1;
  // Report a bug: a click on the tab works (the panel doesn't move under it), Review shows all, nothing goes before Send
  await page.click('[data-help-tab="bug"]');assert.equal(await page.isHidden('#help-ask-pane'),true);
  await page.fill('#bug-what','The Calendar shows yesterday.');await page.click('#bug-next');
  await page.waitForSelector('#bug-review:not([hidden])');
  const shown=await page.textContent('#bug-sent');
  assert.ok(shown.includes('The Calendar shows yesterday.'));
  assert.deepEqual(await page.$$eval('.bug-parts li',l=>l.map(x=>x.textContent)),['Recent app errors (1 line)','Settings, without keys or what anyone wrote'],'a short summary');
  assert.equal(await page.isVisible('.bug-all pre'),false,'the full text waits behind Show everything');
  await page.click('.bug-all summary');const all=await page.textContent('.bug-all pre');
  for(const part of ['token=[redacted]','openai/gpt-5'])assert.ok(all.includes(part),'everything shows '+part);
  assert.deepEqual(actions.map(a=>a.action),['help_ask','bug_preview'],'nothing sent before Send');
  await page.click('#bug-send');await page.waitForSelector('#bug-done:not([hidden])');
  const sent=actions.at(-1);
  assert.equal(sent.action,'bug_send');assert.equal(sent.upload,'bug-report');
  assert.equal(sent.args.description,'The Calendar shows yesterday.');assert.deepEqual(sent.args.report.settings,{model:'openai/gpt-5'});
  await page.keyboard.press('Escape');
  // Unticked, the report stays home
  await page.evaluate(()=>document.querySelector('#open-help').click());await page.click('[data-help-tab="bug"]');
  await page.fill('#bug-what','Again.');await page.uncheck('#bug-diag');await page.click('#bug-next');await page.waitForSelector('#bug-review:not([hidden])');
  await page.click('#bug-send');await page.waitForSelector('#bug-done:not([hidden])');
  assert.equal(actions.at(-1).args.report??null,null,'no report when unticked');
  await page.keyboard.press('Escape');
  // An error toast offers it, with what it said
  await page.evaluate(()=>toast('Couldn’t save that. Try again.',true));await page.click('#toast [data-bug-report]');
  await page.waitForSelector('#help-panel[open]');
  assert.match(await page.inputValue('#bug-what'),/Couldn’t save that/);
  await page.evaluate(()=>toast('Saved.'));assert.equal(await page.$('#toast [data-bug-report]'),null,'only errors offer it');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('help dashboard: ok');
}finally{await browser?.close();server.close()}
