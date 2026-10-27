import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Working on a to-do: Ask for changes says what it changes and keeps Review and send in reach; editing a draft shows plain
// text (links read "words (address)") and sends the links back as links; who it is about opens their page; one a teammate
// has can go to someone else; and one that is preparing stays where it was, at a steady height.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString(),posts=[];
const BODY='Hi Noor,\n\nThe price is **€29** a seat. See [the pricing page](https://example.com/pricing).\n\nAlex';
const cards=[{id:'r1',title:'Send Noor the pricing',body:'Draft ready.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[2],
  people:[{id:'email:noor@example.com',name:'Noor Haddad',org:{id:'org:example.com',name:'Example Co'}}],
  next_actions:[{kind:'email',revision:'v1',label:'Send to Noor',to:['noor@example.com'],to_name:'Noor',from:'alex@example.com',subject:'Pricing',body:BODY}]},
 {id:'k1',title:'Fix the export',body:'Kim has it.',status:'snoozed',scope:'work',created_at:now,event_ids:[3],snoozed_until:new Date(Date.now()+3*864e5).toISOString(),
  fleet_handoff:{name:'Kim Lee',stage:'asked'},handoff_wait:{name:'Kim Lee'}},
 {id:'p1',title:'Book the venue',body:'They hold the date until Friday.',status:'pending',scope:'work',created_at:now,event_ids:[4]},
 {id:'p2',title:'Answer the survey',body:'A short one.',status:'pending',scope:'work',created_at:now,event_ids:[5]}];
let steps=[];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],
 fleet:{on:true,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/progress'){res.end(JSON.stringify({status:'running',steps}));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='revise_draft'){res.end(JSON.stringify({revision:'v2'}));return}
  if(b.action==='fleet_handoff_draft'){res.end(JSON.stringify({suggestion_id:b.args.suggestion_id,fleets:[{id:'f1',name:'Work',members:[{member_id:'m1',name:'Kim Lee'},{member_id:'m2',name:'Sam Ray'}]}],title:'Fix the export',summary:'Kim has it.'}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const shot=async(page,what,width)=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/after-${what}-${width>600?'desktop':'phone'}.png`})};
 for(const width of [1440,390]){
  posts.length=0;Object.assign(cards[2],{status:'pending',preparation_status:undefined,preparation_started_at:undefined});steps=[];
  const context=await browser.newContext({viewport:{width,height:width>600?900:844}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-r1').waitFor();
  const r1=page.locator('#task-r1');
  // Ask for changes says what it changes; a decision's says it does it differently
  await r1.locator('.more-actions>summary').click();
  const change=r1.locator('[data-choice="change"]');
  assert.equal(await change.innerText(),'Ask for changes');assert.equal(await change.getAttribute('title'),'Tell me what to change in the draft, and I redo it');
  await page.locator('#task-p1 .more-actions>summary').click();
  assert.equal(await page.locator('#task-p1 [data-choice="change"]').innerText(),'Do it differently');
  await page.mouse.click(2,2);
  // In the change editor, Review and send stays in reach
  await r1.locator('.more-actions>summary').click();await change.click();
  await r1.getByText('What should I change?').waitFor();
  const send=r1.locator('.change-editor [data-smart="v1"]');
  assert.equal(await send.innerText(),'Review and send to Noor');
  assert.ok(await send.isVisible());await shot(page,'change-editor',width);
  // Its preview shows the link as a link; Edit shows plain text, no Markdown
  await send.click();await page.locator('#send-dialog[open]').waitFor();
  assert.equal(await page.locator('#send-preview a').getAttribute('href'),'https://example.com/pricing');
  assert.doesNotMatch(await page.locator('#send-preview').innerText(),/\]\(|\[the/);
  // Review and send opens in the editor, with Ask for changes beside Send now
  assert.ok(await page.locator('#send-body').isVisible(),'the draft opens ready to edit');
  assert.ok(await page.locator('#send-ask-open').isVisible(),'Ask for changes is in the dialog');
  // Opening it sends nothing: no confirm_action and no "Sending" toast until Send now
  assert.equal(posts.filter(p=>p.action==='confirm_action'||p.action==='revise_draft').length,0,'nothing is sent before Send now');
  assert.equal(await page.locator('#toast.show',{hasText:'Sending your approved draft'}).count(),0);await shot(page,'send-edit-first',width);
  const edited=await page.locator('#send-body').inputValue();
  assert.equal(edited,'Hi Noor,\n\nThe price is €29 a seat. See the pricing page (https://example.com/pricing).\n\nAlex');
  // Untouched: sent as drafted, no revision
  await page.locator('#send-confirm').click();await page.locator('#send-dialog').waitFor({state:'hidden'});
  assert.equal(posts.filter(p=>p.action==='revise_draft').length,0);assert.equal(posts.filter(p=>p.action==='confirm_action').at(-1).revision,'v1');
  // Edited: the link goes back as a link
  await page.locator('#task-r1 [data-smart="v1"]').first().click();await page.locator('#send-dialog[open]').waitFor();
  await page.locator('#send-body').fill(edited.replace('Alex','Thanks,\nAlex'));await page.locator('#send-confirm').click();await page.locator('#send-dialog').waitFor({state:'hidden'});
  assert.equal(posts.filter(p=>p.action==='revise_draft').at(-1).body,'Hi Noor,\n\nThe price is €29 a seat. See [the pricing page](https://example.com/pricing).\n\nThanks,\nAlex');
  // and what is sent is exactly the edited text: the revision saved from it, then Send now confirms that revision
  {const i=posts.findLastIndex(p=>p.action==='revise_draft'),j=posts.findLastIndex(p=>p.action==='confirm_action');assert.ok(i>=0&&j===i+1,'revise then confirm');assert.equal(posts[j].revision,'v2')}
  // Ask for changes inside the dialog: the instruction saves as the to-do's Change, and the dialog closes
  await page.locator('#task-r1 [data-smart="v1"]').first().click();await page.locator('#send-dialog[open]').waitFor();
  await page.locator('#send-ask-open').click();await page.locator('#send-ask-text').fill('Make it shorter');
  await shot(page,'send-ask',width);
  await page.locator('#send-ask-save').click();await page.locator('#send-dialog').waitFor({state:'hidden'});
  const asked=posts.filter(p=>p.action==='decide').at(-1);assert.equal(asked.choice,'other');assert.equal(asked.feedback,'Make it shorter');
  // Who it is about: a chip that opens their page, and their organization's
  const who=r1.locator('a.chip.who:not(.org)');
  assert.equal(await who.getAttribute('href'),'#graph/'+encodeURIComponent('email:noor@example.com'));
  assert.equal((await who.first().innerText()).trim(),width>600?'Noor Haddad':'Noor');
  assert.equal(await r1.locator('a.chip.who.org').getAttribute('href'),'#graph/'+encodeURIComponent('org:example.com'));
  assert.equal((await r1.locator('a.chip.who.org').innerText()).trim(),'Example Co');
  // A teammate has it: one state (With Kim · waiting), Take it back and Hand off to someone else in sight
  const k1=page.locator('#task-k1');
  if(!await k1.isVisible())await page.locator('#later-list>summary').click();await k1.waitFor();
  assert.match(await k1.locator('.note.fleet').innerText(),/With Kim · waiting/);
  assert.equal(await k1.locator('.actions>[data-handoff-take-back]').innerText(),'Take it back');
  const re=k1.locator('.actions>[data-fleet-handoff]');assert.equal(await re.innerText(),'Hand off to someone else');
  await k1.locator('[data-handoff-take-back]').click();await page.waitForFunction(()=>!document.querySelector('[data-handoff-take-back]:disabled'));
  assert.deepEqual(posts.filter(p=>p.action==='fleet_handoff_take_back').at(-1),{action:'fleet_handoff_take_back',suggestion_id:'k1'});
  await re.click();const form=k1.locator('.fleet-handoff-form');await form.waitFor();
  assert.ok(await form.locator('input[value="f1|m2"]').isChecked(),'the form starts on someone who does not have it yet');
  await k1.getByText('Take it back from Kim').waitFor();
  assert.ok(await k1.locator('input[name="replace"]').isChecked());await k1.scrollIntoViewIfNeeded();await shot(page,'reassign',width);
  // Preparing: it stays in its section, and its steps keep one height from the start
  Object.assign(cards[2],{status:'accepted',preparation_status:'running',preparation_started_at:now});
  await page.evaluate(()=>refresh());await page.locator('#task-p1 .prep .steps').waitFor();
  assert.ok(await page.evaluate(()=>!document.getElementById('section-preparing')&&!!(document.getElementById('section-needs').compareDocumentPosition(document.getElementById('task-p1'))&Node.DOCUMENT_POSITION_FOLLOWING)),
   'it stays under Needs your decision while it prepares');
  const tall=()=>page.locator('#task-p1').evaluate(n=>Math.round(n.getBoundingClientRect().height));
  const before=await tall();
  steps=[{title:'Checking the venue’s calendar'},{title:'Reading the contract, a long step title that would wrap onto a second line on a phone'},{title:'Drafting the reply'}];
  await page.waitForFunction(()=>document.querySelectorAll('#task-p1 .steps li').length===3,null,{timeout:10000});
  await page.waitForTimeout(200);await page.locator('#task-p1').scrollIntoViewIfNeeded();await shot(page,'preparing',width);assert.equal(await tall(),before,'the to-do keeps its height while steps come in');
  Object.assign(cards[2],{status:'prepared',preparation_status:'done'});
  await page.evaluate(()=>refresh());
  assert.ok(await page.evaluate(()=>{const r=document.getElementById('section-ready'),t=document.getElementById('task-p1');return !!(r&&t&&r.compareDocumentPosition(t)&Node.DOCUMENT_POSITION_FOLLOWING)}),'ready: then it moves to Ready');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('to-do edit ok');
