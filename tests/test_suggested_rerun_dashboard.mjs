import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdir} from 'node:fs/promises';
import {join} from 'node:path';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A suggested routine (routines.py) before Add: Edit and Change when in its ⋯ menu, like any routine (no Try it: Run
// again is on the card), and Run again runs its words now. The button waits while it runs (one run per press), and the
// new result shows in place of the preview. Add and No thanks stay.
//   SHOTS=<folder> also saves each step at 390 and 1440, light and dark.
const SHOTS=process.env.SHOTS;if(SHOTS)await mkdir(SHOTS,{recursive:true});
const dashboard=await dashboardPage();
const posts=[],SID='f6'.repeat(16),SUNDAY='2026-11-08T07:00:00Z',now=new Date().toISOString();
const WORDS='Sum up what moved in my deals and mail since yesterday, for the standup.';
const NEW='Sum up what moved in my deals and mail since the last workday, for the standup.';
const suggestion=()=>({id:SID,name:'Daily standup',instructions:WORDS,from_openclaw:true,rule:{unit:'weekday',n:1},anchor:'2026-11-09',at:'09:00',state:'suggested',
 next_due:null,steps:{},runs:[{id:'s1',state:'nothing',started_at:SUNDAY,why:'Nothing moved since yesterday.',used:[]}],test:null});
let suggested;
const reset=()=>{suggested=[suggestion()];posts.length=0};reset();
const all=()=>JSON.stringify({routines:[],suggested,trying:[],templates:[]});
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/routines'){res.end(all());return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='routine_edit'){suggested=suggested.map(r=>({...r,instructions:b.args.words,...(b.args.name?{name:b.args.name}:{})}));res.end(all());return}
  if(b.action==='routine_run_now'){suggested=suggested.map(r=>({...r,test:{id:'t1',state:'running',started_at:now,used:[]}}));res.end(all());return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const sent=name=>posts.filter(p=>p.action===name).map(({action,...p})=>p);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440])for(const scheme of SHOTS?['light','dark']:['light']){reset();const mobile=width<500;
  const context=await browser.newContext({viewport:{width,height:mobile?844:900},colorScheme:scheme,timezoneId:'Europe/Brussels',...(mobile?{isMobile:true,hasTouch:true}:{})});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const shot=async name=>{if(SHOTS)await page.screenshot({path:join(SHOTS,`${name}-${width}-${scheme}.png`)})};
  await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
  // The card: its Sunday preview, Add, Run again and No thanks in sight, Edit and Change when in the ⋯ menu
  const card=page.locator(`.rt-sugg article[data-rt="${SID}"]`);await card.waitFor();
  assert.deepEqual(await card.locator('.actions>button').evaluateAll(n=>n.map(x=>x.textContent)),['Add','Run again','No thanks']);
  assert.equal((await card.locator('.rt-state').innerText()).trim(),'Nothing new');
  const acts=await card.locator('.actions').boundingBox(),box=await card.boundingBox();
  assert.ok(acts.x+acts.width<=box.x+box.width+1,'the buttons fit the card');
  await shot('suggested-card');
  await card.locator('.more-actions>summary').click();
  assert.deepEqual(await card.locator('.more-menu>button').evaluateAll(n=>n.map(x=>x.textContent)),['Edit','Change when']);
  await card.locator('[data-rt-do="edit"]').click();
  // Edit: its name and words, Save and Cancel; no Try it here
  const form=card.locator('.rt-form');await form.waitFor();
  assert.equal(await form.locator('.rt-name').inputValue(),'Daily standup');
  assert.equal(await form.locator('textarea').inputValue(),WORDS);
  assert.deepEqual(await form.locator('.rt-form-acts>button').evaluateAll(n=>n.map(x=>x.textContent)),['Save','Cancel']);
  await form.locator('textarea').fill(NEW);
  await shot('suggested-editing');
  await form.locator('.primary').click();await form.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_edit'),[{id:SID,words:NEW}]);
  assert.equal((await card.locator('.rt-what').innerText()).trim(),NEW);
  assert.equal(sent('routine_run_now').length,0);  // saving never runs it by itself
  // Run again: one press, one run; the button waits while it runs
  await card.locator('[data-rt-do="now"]').click();
  await card.locator('.rt-state.rt-running').waitFor();
  assert.deepEqual(sent('routine_run_now'),[{id:SID}]);
  assert.equal(await card.locator('[data-rt-do="now"]').isDisabled(),true);
  await page.locator('#toast').waitFor({state:'hidden',timeout:8000}).catch(()=>{});
  await shot('suggested-running');
  // Its result, in place of the preview
  suggested=suggested.map(r=>({...r,test:{id:'t1',state:'ready',started_at:now,used:[],result:'- **Halyard** moved to Proposal; they want a call Thursday\n- **Fernwave** signed the renewal\n- 2 new leads from the site form'}}));
  await page.evaluate(()=>routinesView(true));
  await card.locator('.rt-state.rt-ready').waitFor();
  assert.equal(await card.locator('.rt-run').count(),1);
  assert.equal(await card.locator('[data-rt-do="now"]').isDisabled(),false);
  assert.equal(await card.locator('.rt-result strong').first().innerText(),'Halyard');
  await shot('suggested-result');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('suggested rerun dashboard ok');
}finally{await browser?.close();server.close()}
