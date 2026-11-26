// An edit to a linked Google Sheet or Slides file (file_writes.py) on its to-do: a sheet's cells before and after, new
// rows and a new tab's cells, a slide's text before and after, a new slide; Review changes opens a dialog that confirms
// that revision only. The Google Docs card offers Allow edits to Sheets and Slides once it reads them. Synthetic data, a
// local fixture server, nothing written.
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
import {quiet,trackRequests,waitForAction} from './page-calls.mjs';
const {chromium}=await import('./browser.mjs');

const dashboard=await dashboardPage();
const sheetId='1234567890abcdef',deckId='0011223344556677',doneId='8899aabbccddeeff';
const SHEET='s'.repeat(44),DECK='p'.repeat(44);
const sheet={kind:'doc_write',op:'edit',label:'Save changes',revision:'1234567890ab',account_id:'docs',provider:'google',file_kind:'sheets',file_id:SHEET,
  doc_title:'Event budget',version:'v1',url:`https://docs.google.com/spreadsheets/d/${SHEET}/edit`,changes:[
   {tab:'Budget',cells:'B2:B3',values:[['1350'],['300']],shown:[{cell:'B2',before:'1,200',after:'1350'}]},
   {tab:'Budget',append:[['Band','800']],row:6,last:['Food','300'],shown:[{cell:'A6',after:'Band'},{cell:'B6',after:'800'}]},
   {tab:'Budget',cells:'C7',values:[['=SUM(B2:B6)']],formulas:true,shown:[{cell:'C7',before:'',after:'=SUM(B2:B6)'}]}]};
const deck={kind:'doc_write',op:'edit',label:'Save changes',revision:'abcdefabcdef',account_id:'docs',provider:'google',file_kind:'slides',file_id:DECK,
  doc_title:'Q4 deck',version:'rev-1',url:`https://docs.google.com/presentation/d/${DECK}/edit`,changes:[
   {slide:2,find:'week 2',replace:'week 3',slide_id:'g2',shown:[{before:'Launch in week 2\nThen rest',after:'Launch in week 3\nThen rest'}]},
   {add_slide:'Risks',body:'Venue\nWeather',at:3}]};
const saved={...deck,revision:'555555555555',state:{status:'sent',message_id:'docwrite:'+DECK,sent_at:new Date().toISOString()}};
const busy={...sheet,revision:'666666666666',state:{status:'sending'}},busyId='7766554433221100';
const docs=(extra)=>({id:'docs',display_name:'Work docs',email:'owner@example.com',service:'docs',transport:'broker',boundary:'work',events:3,recent_events:3,
  last_success:new Date().toISOString(),docs_provider:'google',docs_linked_only:true,own_grant:true,docs_replies:false,docs_writes:['create','edit'],
  docs_files:['sheets','slides'],hosted_signin:'google_docs',...extra});
let connectors=[docs({docs_files_signin:'google_docs_files_write'})];
const card=(id,title,a,extra={})=>({id,title,body:'Drafted the change.',status:'prepared',event_ids:[1],next_action:a,next_actions:[a],
  outcome:JSON.stringify({state:'needs_you',needs:'Check the change and save it'}),scope:'work',created_at:new Date().toISOString(),...extra});
const state=()=>({suggestions:[card(sheetId,'Update the event budget',sheet),card(deckId,'Move the launch in the Q4 deck',deck),
  card(doneId,'Fix the launch week',saved,{status:'completed',outcome:null}),card(busyId,'Add the band to the budget',busy)],
  connectors,manage_url:'https://cp.example/account',suggestion_counts:{prepared:2},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]});
const calls=[],errors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){let b='';for await(const c of req)b+=c;calls.push(JSON.parse(b));res.end(JSON.stringify({status:'queued'}));return}
 res.statusCode=url.pathname.startsWith('/api/')?200:404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOT_DIR;if(shots)await mkdir(shots,{recursive:true});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[390,844,'light'],[1440,900,'dark'],[1440,900,'light'],[390,844,'dark']]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();trackRequests(page);
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.evaluate(()=>refresh());
  const name=`${width}x${height}-${scheme}`;
  // The sheet on its to-do: where, each cell before and after, new rows' cells, a formula said as one
  const task=page.locator(`#task-${sheetId}`);
  await task.waitFor();
  const box=task.locator('.draft.doc-write');
  await box.locator('.fw-t').first().waitFor();  // drawn by its lazy part
  assert.match(await box.locator('.dm').textContent(),/^Edit “Event budget” in Google Sheets · Open the file$/);
  assert.equal(await box.locator('.dm a').getAttribute('href'),sheet.url);
  const first=box.locator('.fw-t').first();
  assert.deepEqual(await first.locator('thead th').allTextContents(),['Cell','Before','After']);
  assert.deepEqual(await first.locator('tbody tr').first().locator('th,td').allTextContents(),['B2','1,200','1350']);
  assert.equal(await first.locator('tbody tr').first().locator('del').textContent(),'1,200');
  assert.equal(await first.locator('tbody tr').count(),1,'a cell that keeps its value is not in the table');
  assert.deepEqual(await box.locator('.fw-t').nth(1).locator('thead th').allTextContents(),['Cell','New']);
  const text=await box.textContent();
  assert.ok(text.includes('New rows in “Budget” after row 5'),text);
  assert.ok(text.includes('Entered as formulas, so they calculate.'),text);
  assert.ok(text.includes('Change 3 of 3'),text);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll at '+name);
  assert.equal(await task.locator(`[data-smart="${sheet.revision}"]`).textContent(),'Review changes');
  if(shots)await task.screenshot({path:`${shots}/sheet-todo-${name}.png`});
  // Review changes: the dialog shows the whole change again; nothing is written before Save
  await task.locator(`[data-smart="${sheet.revision}"]`).click();
  await page.locator('#send-dialog').waitFor({state:'visible'});
  assert.equal(await page.locator('#send-title').textContent(),'Save these changes?');
  assert.equal(await page.locator('#send-confirm').textContent(),'Save');
  const head=await page.locator('#send-head').textContent();
  assert.ok(head.includes('File')&&head.includes('Event budget')&&head.includes('Google Sheets'),head);
  assert.equal(await page.locator('#send-preview .fw-t').count(),3);
  assert.ok((await page.locator('#send-fine').textContent()).includes('only if the file hasn’t changed'));
  assert.equal(calls.filter(c=>c.action==='confirm_action').length,0);
  if(shots)await page.screenshot({path:`${shots}/sheet-dialog-${name}.png`});
  await page.locator('#send-confirm').click();
  await waitForAction(calls,'confirm_action');
  const confirm=calls.find(c=>c.action==='confirm_action');
  assert.equal(confirm.args.suggestion_id,sheetId);assert.equal(confirm.args.revision,sheet.revision);
  calls.length=0;
  await quiet(page);
  // The deck: the slide's text before and after, marked; a new slide's title and body
  const slides=page.locator(`#task-${deckId}`),sbox=slides.locator('.draft.doc-write');
  assert.match(await sbox.locator('.dm').textContent(),/^Edit “Q4 deck” in Google Slides/);
  assert.equal(await sbox.locator('del').first().textContent(),'week 2');
  assert.equal(await sbox.locator('ins').first().textContent(),'week 3');
  const stext=await sbox.textContent();
  assert.ok(stext.includes('Slide 2')&&stext.includes('New slide 3: Risks')&&stext.includes('Weather'),stext);
  if(shots)await slides.screenshot({path:`${shots}/slides-todo-${name}.png`});
  await slides.locator(`[data-smart="${deck.revision}"]`).click();
  await page.locator('#send-dialog').waitFor({state:'visible'});
  assert.ok((await page.locator('#send-head').textContent()).includes('Google Slides'));
  if(shots)await page.screenshot({path:`${shots}/slides-dialog-${name}.png`});
  await page.locator('#send-dialog .snooze-heading button').click();
  assert.equal(calls.filter(c=>c.action==='confirm_action').length,0);
  // While it goes in: the file, not a doc
  const going=await page.locator(`#task-${busyId}`).textContent();
  assert.ok(going.includes('Writing the file…')&&!going.includes('Writing the doc'),going);
  if(shots)await page.locator(`#task-${busyId}`).screenshot({path:`${shots}/sheet-writing-${name}.png`});
  // Saved: what happened, without "You"
  await page.evaluate(()=>{const d=$('#finished-list');if(d&&!d.open){d.open=true;listShow(d)}});
  const done=await page.locator(`#task-${doneId}`).evaluate(n=>n.textContent);
  assert.match(done,/Changes saved in the file( at \d\d:\d\d)?\./);
  assert.ok(!/\bYou (saved|changed|edited)/.test(done));
  // The Google Docs card: reads them, then Allow edits to Sheets and Slides, a hosted sign-in of its own
  await page.evaluate(()=>document.querySelector('nav [data-tab="health"]').click());
  await page.evaluate(()=>showHealthPane('other'));
  const conn=page.locator('[data-conn="docs"]');
  await conn.waitFor();if(await conn.locator('[data-conn-open]').getAttribute('aria-expanded')==='false')await conn.locator('[data-conn-open]').click();
  assert.ok((await conn.textContent()).includes('Reads linked Sheets and Slides.'));
  const allow=conn.locator('button',{hasText:'Allow edits to Sheets and Slides'});
  assert.equal(await allow.getAttribute('data-hosted-reconnect'),'google_docs_files_write');
  if(shots)await conn.screenshot({path:`${shots}/docs-card-${name}.png`});
  connectors=[docs({docs_writes:['create','edit','sheets','slides']})];
  await page.evaluate(()=>refresh());await quiet(page);
  assert.ok((await conn.textContent()).includes('Reads and edits the Sheets and Slides your to-dos link to. Edits wait for your OK.'));
  assert.equal(await conn.locator('button',{hasText:'Allow edits'}).count(),0);
  connectors=[docs({docs_files_signin:'google_docs_files_write'})];
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
