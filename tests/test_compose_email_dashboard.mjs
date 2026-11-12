// A click on an email address opens the composer, not the mail app (todos-compose.js, docs/help/email-composer.md):
// the send dialog every draft uses, titled New email, From (a picker of the owner's mailboxes, the one compose_from
// picked first, grouped by area) and To (their name and address), an empty subject and message with the formatting
// tools. Send asks for a subject and a message first, then makes the draft (compose_email) and confirms exactly that
// revision, with the picked alias as sender. Escape closes it and nothing is posted; a modifier click keeps the mailto;
// a link in a to-do's text opens it too; without a mailbox that can send it stays a mailto. Open in email is there.
// At 1440, 800 and 390, light and dark. Made-up data, a local fixture server, nothing sent. SHOTS=<folder> saves shots.
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()+n*864e5).toISOString();
const sam='sam.lee@client.example',work='owner@acme.example',alias='partners@acme.example',home='owner@mail.example';
const person={id:'email:'+sam,kind:'person',name:'Sam Lee',strength:3,closeness:'close',last_at:day(-2),signals:40,ids:[sam],usual_gap_days:7,quiet:false,
 org:'org:client.example',org_name:'Client Co',org_by:'email',side:'work',side_by:null,edited:[],phones:[],emails:[{value:sam,by:'messages'}],
 profile:{title:'Head of Operations',company:'Client Co'},links:[],recent:[],around:[],open:{},joined:[]};
const todo={id:'1234567890abcdef',title:'Ask Robin about the venue',body:'Robin runs the venue: [robin@venue.example](mailto:robin@venue.example).',status:'pending',
 event_ids:[1],scope:'work',created_at:day(-1)};
let mailboxes=true;const calls=[];
const offer=to=>to===sam?{from:[{account_id:'work',from:work,area:'Work'},{account_id:'work',from:alias,area:'Work'},{account_id:'home',from:home,area:'Personal'}],default:work,to_name:'Sam Lee',node_id:person.id}
 :{from:[{account_id:'home',from:home,area:'Personal'},{account_id:'work',from:work,area:'Work'}],default:home,to_name:'',node_id:null};
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[todo],promises:[],connectors:[],suggestion_counts:{pending:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')?person:{projects:[],people:[person],quiet:[],new:[],orgs:[]}));return}
 if(url.pathname==='/api/action'){let b='';for await(const c of req)b+=c;const call=JSON.parse(b);calls.push(call);
  if(call.action==='compose_from'){res.end(JSON.stringify(mailboxes?offer(call.args.to):{from:[],to_name:'',node_id:null}));return}
  if(call.action==='compose_email'){res.end(JSON.stringify({suggestion_id:'aaaaaaaaaaaaaaaa',revision:'bbbbbbbbbbbb',from_options:[work,alias]}));return}
  res.end(JSON.stringify({status:'queued'}));return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const posted=name=>calls.filter(c=>c.action===name);
const waitFor=async(page,name)=>{for(let i=0;i<150&&!posted(name).length;i++)await page.waitForTimeout(20);return posted(name)[0]};
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[800,900,'light'],[800,900,'dark'],[390,844,'light'],[390,844,'dark']]){
  const tag=`${width}-${scheme}`;calls.length=0;mailboxes=true;
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,deviceScaleFactor:width<500?2:1}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(tag+': '+e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#graph/'+encodeURIComponent(person.id));
  const link=page.locator(`.person-page .person-contact a[href="mailto:${sam}"]`);await link.waitFor();
  if(shots)await page.screenshot({path:`${shots}/compose-1-person-${tag}.png`});
  // A modifier click keeps the link's own mailto: no composer
  await link.click({modifiers:['Control']}).catch(()=>{});await page.waitForTimeout(100);
  assert.equal(posted('compose_from').length,0,tag);assert.equal(await page.locator('#send-dialog').evaluate(d=>d.open),false);
  // A plain click: the composer, ready to write
  await link.click();
  const dialog=page.locator('#send-dialog');await dialog.waitFor({state:'visible'});
  assert.deepEqual(posted('compose_from').map(c=>c.args),[{to:sam}]);
  assert.equal(await page.locator('#send-title').textContent(),'New email');
  assert.deepEqual(await page.locator('#send-head dt').allTextContents(),['From','To']);
  assert.equal(await page.locator('#send-from>span').textContent(),work);
  assert.equal((await page.locator('#send-head dd').nth(1).textContent()).trim(),`Sam Lee <${sam}>`);
  assert.equal(await page.locator('#send-subject').inputValue(),'');assert.equal(await page.locator('#send-rich').isVisible(),true);
  assert.equal(await page.locator('#send-confirm').textContent(),'Send');
  for(const hidden of ['#send-edit','#send-ask-open','#send-recipients','#send-files','#send-preview'])assert.equal(await page.locator(hidden).isVisible(),false,hidden);
  assert.equal(await page.locator('#send-mailapp a').textContent(),'Open in email');
  assert.equal(await page.evaluate(()=>document.activeElement?.id),'send-subject');
  const fits=await page.evaluate(()=>{const d=document.querySelector('#send-dialog').getBoundingClientRect();return document.documentElement.scrollWidth<=innerWidth&&d.left>=0&&d.right<=innerWidth+0.5&&d.bottom<=innerHeight+0.5});
  assert.equal(fits,true,'fits at '+tag);
  if(shots)await page.screenshot({path:`${shots}/compose-2-open-${tag}.png`});
  // Send without a subject or a message: it says what's missing, posts nothing
  await page.locator('#send-confirm').click();
  assert.equal(await page.locator('#send-error').textContent(),'Add a subject first.');
  await page.locator('#send-subject').fill('Lunch next week');await page.locator('#send-confirm').click();
  assert.equal(await page.locator('#send-error').textContent(),'Write the message first.');
  assert.equal(posted('compose_email').length+posted('confirm_action').length,0);
  // The From picker: the owner's mailboxes, grouped by area, the current one ticked
  await page.locator('#send-from').click();const menu=page.locator('#cm-menu');await menu.waitFor({state:'visible'});
  assert.deepEqual(await menu.locator('[role=menuitemradio]>span').allTextContents(),[work,alias,home]);
  assert.deepEqual(await menu.locator('.cm-group').allTextContents(),['Work','Personal']);
  await menu.locator(`[data-cm-value="${alias}"]`).click();await menu.waitFor({state:'hidden'});
  assert.equal(await page.locator('#send-from>span').textContent(),alias);
  await page.locator('#send-rich-body').click();
  await page.keyboard.type('Hi Sam,');await page.keyboard.press('Enter');await page.keyboard.press('Enter');
  await page.keyboard.type('Does Thursday work for ');await page.keyboard.press('Control+b');await page.keyboard.type('lunch');await page.keyboard.press('Control+b');
  await page.keyboard.type('?');await page.keyboard.press('Enter');await page.keyboard.press('Enter');await page.keyboard.type('Alex');
  if(shots)await page.screenshot({path:`${shots}/compose-3-filled-${tag}.png`});
  assert.equal(posted('compose_email').length,0,'nothing goes before Send');
  await page.locator('#send-confirm').click();
  const made=await waitFor(page,'compose_email'),sent=await waitFor(page,'confirm_action');
  assert.deepEqual({...made.args,body:undefined},{to:sam,account_id:'work',subject:'Lunch next week',body:undefined});
  assert.match(made.args.body,/^Hi Sam,\n\nDoes Thursday work for \*\*lunch\*\*\?\n\nAlex$/);
  assert.equal(sent.args.suggestion_id,'aaaaaaaaaaaaaaaa');assert.equal(sent.args.revision,'bbbbbbbbbbbb');assert.equal(sent.args.sender,alias);
  assert.ok(calls.indexOf(made)<calls.indexOf(sent));
  await dialog.waitFor({state:'hidden'});
  // Escape closes it and nothing is posted; a new one starts empty
  calls.length=0;await link.click();await dialog.waitFor({state:'visible'});
  await page.locator('#send-subject').fill('Draft');await page.keyboard.press('Escape');await dialog.waitFor({state:'hidden'});
  await link.click();await dialog.waitFor({state:'visible'});assert.equal(await page.locator('#send-subject').inputValue(),'');
  await page.locator('#send-dialog .snooze-heading button').click();await dialog.waitFor({state:'hidden'});
  assert.equal(posted('compose_email').length+posted('confirm_action').length,0);
  // A to-do's own Review and send still works as before afterwards (no compose state left)
  await page.waitForFunction(()=>!sendDraft?.compose&&$('#send-mailapp').hidden,null,{timeout:3000});
  // A link in a to-do's text opens it too, From on the default for that address
  await page.goto('http://127.0.0.1:'+server.address().port+'/#card='+todo.id);
  const inText=page.locator(`a[href="mailto:robin@venue.example"]`).first();await inText.waitFor();
  calls.length=0;await inText.click();await dialog.waitFor({state:'visible'});
  assert.equal(await page.locator('#send-from>span').textContent(),home);
  assert.equal((await page.locator('#send-head dd').nth(1).textContent()).trim(),'robin@venue.example');
  await page.keyboard.press('Escape');await dialog.waitFor({state:'hidden'});
  // No mailbox that can send: the address stays a mailto (the composer doesn't open)
  mailboxes=false;calls.length=0;await inText.click();await waitFor(page,'compose_from');await page.waitForTimeout(150);
  assert.equal(await dialog.evaluate(d=>d.open),false);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('compose email dashboard ok');
