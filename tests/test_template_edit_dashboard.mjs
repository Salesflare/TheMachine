import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdir} from 'node:fs/promises';
import {join} from 'node:path';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A template's routine (routine_templates.py) on the Routines page: its card shows its words, and Edit and Advanced are in
// its ⋯ menu like any routine's, with its name in the title's place. Once its words changed, Edit offers Back to the
// template, which puts them back in one tap. A new one on trial names itself in Change, like Edit.
//   SHOTS=<folder> also saves each step at 390 and 1440, light and dark.
const SHOTS=process.env.SHOTS;if(SHOTS)await mkdir(SHOTS,{recursive:true});
const dashboard=await dashboardPage();
const now=new Date().toISOString(),posts=[],ID='a1'.repeat(16),TID='b2'.repeat(16);
const WORDS='Find the newsletters and mailing list emails that came in since the last run, one per sender. Put them in one to-do where I pick Keep or Unsubscribe for each.';
const NEW='Find the newsletters since the last run, but leave out the ones about gardening. Put them in one to-do where I pick Keep or Unsubscribe for each.';
const routine=()=>({id:ID,name:'Newsletter cleanup',instructions:WORDS,template:'newsletters',edited:false,rule:{unit:'day',n:1},anchor:'2026-11-09',at:'07:30',state:'on',
 next_due:'2026-11-11',steps:{},runs:[{id:'r1',state:'ready',started_at:now,result:'Made a to-do with 3 newsletters.',used:[]}]});
const trial=()=>({id:TID,name:'Sum up my deals',instructions:'Sum up my deals',rule:{unit:'week',n:1},anchor:'2026-11-09',at:'09:00',state:'trying',next_due:null,runs:[],
 test:{id:'t1',state:'ready',started_at:now,result:'**Fernwave** is waiting on a quote'}});
let list,trying;
const reset=()=>{list=[routine()];trying=[];posts.length=0};reset();
const all=()=>JSON.stringify({routines:list,suggested:[],trying,templates:[{key:'newsletters',name:'Newsletter cleanup',what:'x',added:true}]});
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/routines'){res.end(all());return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='routine_edit'){list=list.map(r=>b.args.back?{...r,instructions:WORDS,edited:false,steps:{}}:{...r,instructions:b.args.words,edited:b.args.words!==WORDS,...(b.args.name?{name:b.args.name}:{})});res.end(all());return}
  if(b.action==='routine_try'){trying=trying.map(r=>({...r,instructions:b.args.words,...(b.args.name?{name:b.args.name}:{})}));res.end(all());return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const sent=name=>posts.filter(p=>p.action===name).map(({action,...p})=>p);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440])for(const scheme of SHOTS?['light','dark']:['light']){reset();const mobile=width<500;
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme,...(mobile?{isMobile:true,hasTouch:true}:{})});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const shot=async name=>{if(SHOTS)await page.screenshot({path:join(SHOTS,`${name}-${width}-${scheme}.png`)})};
  await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
  // The card: its words, and Edit in the ⋯ menu
  const card=page.locator(`#routines-view article[data-rt="${ID}"]`);await card.waitFor();
  assert.equal((await card.locator('.rt-what').innerText()).trim(),WORDS);
  await shot('template-card');
  await card.locator('.more-actions>summary').click();
  assert.deepEqual(await card.locator('.more-menu>button').evaluateAll(n=>n.map(x=>x.textContent)),['Edit','Change when','Pause','Advanced: script steps','Stop']);
  await card.locator('[data-rt-do="edit"]').click();
  // Edit: its name in the title's place and its words; no Back while they are the template's own
  const form=card.locator('.rt-form');await form.waitFor();
  assert.equal(await form.locator('.rt-name').inputValue(),'Newsletter cleanup');
  assert.equal(await form.locator('textarea').inputValue(),WORDS);
  assert.equal(await form.locator('[data-rt-back]').count(),0);
  await shot('template-edit');
  // A rename alone sends only the name with the same words
  await form.locator('.rt-name').fill('My newsletters');await form.locator('.primary').click();await form.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_edit'),[{id:ID,words:WORDS,name:'My newsletters'}]);
  assert.equal((await card.locator('h3').innerText()).trim(),'My newsletters');
  // New words: saved as they are; the card shows them, and Edit now offers Back to the template
  await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="edit"]').click();
  await form.locator('textarea').fill(NEW);await form.locator('.primary').click();await form.waitFor({state:'detached'});
  assert.equal((await card.locator('.rt-what').innerText()).trim(),NEW);
  await shot('template-saved');
  await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="edit"]').click();
  const back=form.locator('[data-rt-back]');await back.waitFor();
  assert.equal((await back.innerText()).trim(),'Back to the template');
  const acts=await form.locator('.rt-form-acts').boundingBox(),cardBox=await card.boundingBox();
  assert.ok(acts.x+acts.width<=cardBox.x+cardBox.width+1,'the buttons fit the card');
  await shot('template-back');
  await back.click();await form.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_edit').at(-1),{id:ID,back:true});
  assert.equal((await card.locator('.rt-what').innerText()).trim(),WORDS);
  // A new one on trial: Change has its name too, sent only when changed
  trying=[trial()];await page.evaluate(()=>routinesView(true));
  const tc=page.locator(`#routines-view article[data-rt="${TID}"]`);await tc.waitFor();
  await tc.locator('[data-rt-do="change"]').click();
  const tf=tc.locator('.rt-form');await tf.waitFor();
  assert.equal(await tf.locator('.rt-name').inputValue(),'Sum up my deals');
  await tf.locator('textarea').fill('Sum up my won deals');await tf.locator('.primary').click();await tf.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_try').at(-1),{id:TID,words:'Sum up my won deals'});
  await tc.locator('[data-rt-do="change"]').click();await tf.waitFor();
  await tf.locator('.rt-name').fill('Deals digest');await tf.locator('.primary').click();await tf.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_try').at(-1),{id:TID,words:'Sum up my won deals',name:'Deals digest'});
  assert.equal((await tc.locator('h3').innerText()).trim(),'Deals digest');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('template edit dashboard ok');
}finally{await browser?.close();server.close()}
