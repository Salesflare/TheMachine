import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// An open to-do shows where it came from on the to-do itself (not under Details), with that service's logo, and its
// draft box leads with the logo of where the draft goes: Gmail for a Gmail account, the envelope for Outlook, Slack,
// a handoff. A step with no draft box above it carries the logo on its button instead; a to-do with nothing to send
// has none. A closed to-do keeps its source under Details.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[
 {id:'mail',title:'Answer Jacob',body:'They ask for a reply.',status:'prepared',scope:'work',created_at:now,event_ids:[1,2],account_ids:['work-gmail'],source_line:'Source: email from Jacob · Thu 5 Nov (+1 more)',
  next_action:{kind:'email',account_id:'work-gmail',to:['team@example.com'],subject:'Re: The list',label:'Send',body:'Hi Jacob,\n\nThanks.',revision:'r1'}},
 {id:'outlook',title:'Answer Mila',body:'Pricing.',status:'prepared',scope:'work',created_at:now,event_ids:[3],account_ids:['work-outlook'],source_line:'Source: email from Mila · Thu 5 Nov',
  next_action:{kind:'email',account_id:'work-outlook',to:['mila@example.com'],subject:'Re: Pricing',label:'Send',body:'Hi Mila',revision:'r2'}},
 {id:'slack',title:'Reply in #support',body:'Duplicate reminders.',status:'prepared',scope:'work',created_at:now,event_ids:[4],account_ids:['work-slack'],source_line:'Source: Slack from #support · Thu 5 Nov',
  next_action:{kind:'slack',account_id:'work-slack',to_name:'#support',label:'Reply in #support',body:'Looking into it.',revision:'r3'}},
 {id:'handoff',title:'Hand the renewal to Sam',body:'Sam owns it.',status:'prepared',scope:'work',created_at:now,event_ids:[5],source_line:'Source: WhatsApp from Robin · Thu 5 Nov',
  next_action:{kind:'handoff',to_name:'Sam Rivera',label:'Hand off'}},
 {id:'none',title:'Call the garage',body:'They close at 17:00.',status:'prepared',scope:'personal',created_at:now,event_ids:[6],source_line:'Source: Telegram from Sam · Thu 5 Nov',
  outcome:JSON.stringify({state:'needs_you',needs:'call them'})},
 // A meeting's notes lead (meeting_mail.py): a notes logo and the meeting, even with the notes mail among its originals
 {id:'notes',title:'Send the board the revised budget',body:'Agreed in the board meeting.',status:'pending',scope:'work',created_at:now,event_ids:[8,9],account_ids:['work-gmail'],
  source_line:'Source: notes from Board meeting Q4 · Wed 28 Oct (+1 more)',original_urls:['https://mail.google.com/mail/u/0/#all/abc']},
 {id:'done',title:'Sent the quote',body:'Done.',status:'completed',scope:'work',created_at:now,event_ids:[7],source_line:'Source: Slack from #sales · Wed 4 Nov'}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[{id:'work-gmail',service:'gmail'},{id:'work-outlook',service:'outlook'},{id:'work-slack',service:'slack'}],fleet:{on:true,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  const context=await browser.newContext({viewport:{width,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-mail').waitFor();
  const info=id=>page.locator('#task-'+id).evaluate(c=>{const src=c.querySelector(':scope>.card-source .read-original'),dm=c.querySelector('.draft .dm>.via-ico'),btn=c.querySelector('.actions .primary');
   return {src:src&&{via:[...src.classList].find(k=>k.startsWith('via-')),text:src.textContent,visible:src.getBoundingClientRect().height>0,beforeDraft:!c.querySelector('.draft')||!!(src.compareDocumentPosition(c.querySelector('.draft'))&Node.DOCUMENT_POSITION_FOLLOWING)},
    inDetails:!!c.querySelector('.card-details .card-source'),draft:dm&&{cls:dm.className,label:dm.getAttribute('aria-label')},button:btn&&{ico:btn.querySelector('.via-ico')?.className||'',hidden:btn.querySelector('.via-ico')?.getAttribute('aria-hidden')||'',text:btn.textContent}}});
  const mail=await info('mail');
  assert.deepEqual(mail.src&&[mail.src.via,mail.src.visible,mail.src.beforeDraft],['via-gmail',true,true],JSON.stringify(mail));
  assert.ok(mail.src.text.startsWith('Email from Jacob'),mail.src.text);
  assert.equal(mail.inDetails,false);
  assert.deepEqual(mail.draft,{cls:'via-ico via-gmail',label:'Gmail'});
  assert.equal(mail.button.ico,'',mail.button.text);  // the draft above already shows where it goes
  assert.deepEqual((await info('outlook')).draft,{cls:'via-ico via-mail',label:'Email'});
  const slack=await info('slack');
  assert.equal(slack.src.via,'via-slack');assert.deepEqual(slack.draft,{cls:'via-ico via-slack',label:'Slack'});
  const hand=await info('handoff');
  assert.equal(hand.src.via,'via-whatsapp');assert.equal(hand.draft,null);
  assert.deepEqual([hand.button.ico,hand.button.hidden,hand.button.text],['via-ico via-handoff','true','Review handoff to Sam']);
  const none=await info('none');
  assert.equal(none.src.via,'via-telegram');assert.equal(none.draft,null);assert.equal(none.button.ico,'');
  const notes=await info('notes');
  assert.equal(notes.src.via,'via-note',JSON.stringify(notes));assert.ok(notes.src.text.startsWith('Notes from Board meeting Q4'),notes.src.text);
  // The source opens the original, as it did under Details
  assert.equal(await page.locator('#task-mail>.card-source [data-original="read"]').count(),1);
  // Every logo has its picture (a mask), in both places
  for(const sel of ['#task-slack .draft .dm>.via-ico','#task-mail>.card-source .read-original'])
   assert.match(await page.locator(sel).evaluate((e,p)=>getComputedStyle(e,p).maskImage||getComputedStyle(e,p).webkitMaskImage,sel.endsWith('original')?'::before':null),/^url\("data:image\/svg/,sel);
  await context.close();
 }
 // A closed to-do keeps its source under Details (compact)
 const context=await browser.newContext({viewport:{width:1280,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/#done');await page.locator('#task-mail').waitFor();
 await page.evaluate(()=>{state.suggestions=state.suggestions.map(s=>s.id==='mail'?{...s,status:'completed'}:s);render()});
 await page.locator('#task-mail').waitFor({state:'attached'});
 assert.equal(await page.locator('#task-mail>.card-source').count(),0);
 assert.equal(await page.locator('#task-mail .card-details .card-source').count(),1);
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
