// A doc write on a to-do (doc_writes.py): an edit shows each paragraph before and after, a new doc shows in full, and
// Review changes / Review and create open a dialog that confirms that revision only. The Docs card says what it may
// write and offers Allow edits. Synthetic data, a local fixture server, nothing written.
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

const dashboard=await dashboardPage();
const editId='1234567890abcdef',newId='0011223344556677',doneId='8899aabbccddeeff';
const edit={kind:'doc_write',op:'edit',label:'Save changes',revision:'1234567890ab',account_id:'docs',provider:'microsoft',file_id:'d1!i1',
  doc_title:'Q4 pricing',version:'c1',url:'https://contoso.sharepoint.example/q4',changes:[
   {find:'week 2',replace:'week 3',before:'We launch the new seat price in week 2, after the review.',after:'We launch the new seat price in week 3, after the review.'},
   {after:'Pricing',insert:'## Renewals\nRenewals before December keep the old seat price.',before:'Pricing'},
   {append:'Owner: sales ops'}]};
const create={kind:'doc_write',op:'create',label:'Create doc',revision:'abcdefabcdef',account_id:'docs',provider:'google',account_name:'owner@example.com',
  title:'Launch notes',body:'# Launch notes\nThe launch moves to week 3.\n## Next steps\nTell the partners on Friday.'};
const saved={...edit,revision:'555555555555',state:{status:'sent',message_id:'docwrite:d1!i1',sent_at:new Date().toISOString()}};
const docs=(extra)=>({id:'docs',display_name:'Work docs',email:'owner@example.com',service:'docs',transport:'broker',boundary:'work',events:3,recent_events:3,
  last_success:new Date().toISOString(),docs_provider:'microsoft',docs_replies:false,docs_writes:[],...extra});
let connectors=[docs({docs_write_signin:'microsoft_docs_write',connect_name:'docs'})];
const card=(id,title,a,extra={})=>({id,title,body:'Drafted the change.',status:'prepared',event_ids:[1],next_action:a,next_actions:[a],
  outcome:JSON.stringify({state:'needs_you',needs:'Check the change and save it'}),scope:'work',created_at:new Date().toISOString(),...extra});
const state=()=>({suggestions:[card(editId,'Move the launch in Q4 pricing',edit),card(newId,'Write up the launch notes',create),
  card(doneId,'Fix the owner line',saved,{status:'completed',outcome:null})],
  connectors,suggestion_counts:{prepared:2},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]});
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
 for(const [width,height,scheme] of [[390,844,'light'],[1440,900,'dark'],[1440,700,'light']]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.evaluate(()=>refresh());
  const name=`${width}x${height}`;
  // The edit on its to-do: where, and each paragraph before and after, what goes struck through, what comes marked
  const task=page.locator(`#task-${editId}`);
  await task.waitFor();
  const box=task.locator('.draft.doc-write');
  assert.match(await box.locator('.dm').textContent(),/^Edit “Q4 pricing” in Word/);
  assert.equal(await box.locator('del').first().textContent(),'week 2');
  assert.equal(await box.locator('ins').first().textContent(),'week 3');
  assert.equal(await box.locator('.dw-h2').textContent(),'Renewals');
  assert.ok((await box.textContent()).includes('Add at the end'));
  assert.equal(await task.locator(`[data-smart="${edit.revision}"]`).textContent(),'Review changes');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll at '+name);
  if(shots)await task.screenshot({path:`${shots}/edit-todo-${name}.png`});
  // Review changes: the dialog shows the whole change again; nothing is written before Save
  await task.locator(`[data-smart="${edit.revision}"]`).click();
  await page.locator('#send-dialog').waitFor({state:'visible'});
  assert.equal(await page.locator('#send-title').textContent(),'Save these changes?');
  assert.equal(await page.locator('#send-confirm').textContent(),'Save');
  assert.ok((await page.locator('#send-head').textContent()).includes('Q4 pricing'));
  assert.equal(await page.locator('#send-preview del').count(),1);
  assert.ok(await page.locator('#send-editor').isHidden()&&await page.locator('#send-edit').isHidden(),'no editing a doc write here');
  assert.ok((await page.locator('#send-fine').textContent()).includes('only if the doc hasn’t changed'));
  assert.equal(calls.filter(c=>c.action==='confirm_action').length,0);
  if(shots)await page.screenshot({path:`${shots}/edit-dialog-${name}.png`});
  await page.locator('#send-confirm').click();
  for(let i=0;i<100&&!calls.some(c=>c.action==='confirm_action');i++)await page.waitForTimeout(20);
  const confirm=calls.find(c=>c.action==='confirm_action');
  assert.equal(confirm.args.suggestion_id,editId);assert.equal(confirm.args.revision,edit.revision);
  calls.length=0;
  await page.waitForTimeout(400);  // the confirm's refresh draws the to-dos again
  // A new doc: all of it, headings as headings; Review and create, then Create
  const fresh=page.locator(`#task-${newId}`);
  assert.match(await fresh.locator('.draft.doc-write .dm').textContent(),/^New doc in Google Docs/);
  assert.equal(await fresh.locator('.dw-h1').first().textContent(),'Launch notes');
  assert.ok((await fresh.locator('.draft.doc-write').textContent()).includes('Tell the partners on Friday.'));
  if(shots)await fresh.screenshot({path:`${shots}/create-todo-${name}.png`});
  await fresh.locator(`[data-smart="${create.revision}"]`).click();
  await page.locator('#send-dialog').waitFor({state:'visible'});
  assert.equal(await page.locator('#send-title').textContent(),'Create this doc?');
  assert.equal(await page.locator('#send-confirm').textContent(),'Create');
  if(shots)await page.screenshot({path:`${shots}/create-dialog-${name}.png`});
  await page.locator('#send-cancel').click();
  assert.equal(calls.filter(c=>c.action==='confirm_action').length,0);
  // Saved: what happened, without "You"
  const text=await page.locator(`#task-${doneId}`).evaluate(n=>n.textContent);
  assert.match(text,/Changes saved in the doc( at \d\d:\d\d)?\./);
  assert.ok(!/\bYou (saved|changed|edited)/.test(text));
  // The Docs card: what it may write, and Allow edits until it may
  await page.evaluate(()=>document.querySelector('nav [data-tab="health"]').click());
  await page.evaluate(()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.textContent.trim()==='Other sources')?.click());
  const conn=page.locator('[data-conn="docs"]');
  await conn.waitFor();
  assert.ok((await conn.textContent()).includes('Can’t create or edit docs yet.'));
  const allow=conn.locator('button',{hasText:'Allow edits'});
  assert.equal(await allow.getAttribute('data-signin'),'microsoft_docs_write');
  if(shots)await conn.screenshot({path:`${shots}/docs-card-${name}.png`});
  connectors=[docs({docs_writes:['create','edit']})];
  await page.evaluate(()=>refresh());await page.waitForTimeout(200);
  assert.ok((await conn.textContent()).includes('Creates and edits docs only after you OK each change.'));
  assert.equal(await conn.locator('button',{hasText:'Allow edits'}).count(),0);
  connectors=[docs({docs_write_signin:'microsoft_docs_write',connect_name:'docs'})];
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
