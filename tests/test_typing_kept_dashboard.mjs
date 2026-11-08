import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Typing in a to-do's Ask for changes box while a status poll redraws the to-do (its text changed): the box stays the
// same element, focused, with its text and caret, so a phone keyboard keeps its session (spell check doesn't drop out).
// Free-text boxes ask for spell check and sentence capitals. Invented fixture data, no network beyond this fake server.
const dashboard=await dashboardPage();
const shots=process.env.SHOTS||'';
const card={id:'k1',status:'prepared',event_ids:[1],scope:'work',created_at:new Date().toISOString(),title:'Write to Robin about the pilot',body:'Drafted a reply to Robin.'};
const state={suggestions:[card],connectors:[],suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:false,waiting:0}};
const server=createServer((req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url.startsWith('/api/status')){res.end(JSON.stringify(state));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const free=async(loc,what)=>assert.deepEqual(await loc.evaluate(x=>[x.getAttribute('spellcheck'),x.getAttribute('autocapitalize')]),['true','sentences'],what);
try{
 for(const [width,height] of [[390,844],[1440,900]])for(const colorScheme of ['light','dark']){
  card.body='Drafted a reply to Robin.';
  const context=await browser.newContext({viewport:{width,height},isMobile:width<600,hasTouch:width<600,colorScheme}),page=await context.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  const c=page.locator('#task-k1');await c.waitFor();
  const ask=c.getByRole('button',{name:'Ask for changes',exact:true,includeHidden:true}).first();
  if(await ask.isVisible())await ask.click();else await ask.evaluate(x=>x.click());
  const box=page.locator('#feedback-k1');await box.waitFor();
  await free(box,`${width} ${colorScheme}: Ask for changes`);
  await box.click();await box.pressSequentially('move MCP to the');
  await box.evaluate(x=>{x.dataset.mark='typed';x.setSelectionRange(5,5)});
  // A poll brings a change to this to-do while the box has focus
  card.body='Drafted a reply to Robin. Checked the pilot dates.';
  await page.evaluate(()=>refresh());
  await page.waitForFunction(()=>/Checked the pilot dates/.test(document.querySelector('#task-k1')?.textContent||''));
  const kept=await page.evaluate(()=>{const b=document.getElementById('feedback-k1');return {same:b?.dataset.mark==='typed',focused:document.activeElement===b,value:b?.value,caret:[b?.selectionStart,b?.selectionEnd],one:document.querySelectorAll('#feedback-k1').length}});
  assert.deepEqual(kept,{same:true,focused:true,value:'move MCP to the',caret:[5,5],one:1},`${width} ${colorScheme}: the box someone types in is never replaced`);
  await free(box,`${width} ${colorScheme}: still asks for spell check after the redraw`);
  // The rest of the to-do still redraws and works: Cancel closes the editor
  if(shots){await c.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/typing-kept-${width}-${colorScheme}.png`})}
  await c.getByRole('button',{name:'Cancel',exact:true}).click();await box.waitFor({state:'detached'});
  // A redraw that doesn't touch a typed field still swaps the to-do as before
  card.body='Drafted a reply to Robin.';await page.evaluate(()=>refresh());
  await page.waitForFunction(()=>!/Checked the pilot dates/.test(document.querySelector('#task-k1')?.textContent||''));
  assert.deepEqual(errors,[]);
  await context.close()}
 // The other free-text boxes ask the same: chat, a new to-do, Ask for changes in the send dialog
 assert.match(dashboard,/id="nc-text" spellcheck="true" autocapitalize="sentences"/);
 assert.match(dashboard,/id="chat-input" spellcheck="true" autocapitalize="sentences"/);
 assert.match(dashboard,/id="send-ask-text" spellcheck="true" autocapitalize="sentences"/);
 console.log('typing kept dashboard: ok');
}finally{await browser.close();server.close()}
