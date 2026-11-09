import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Routines page (dashboard/routines-page.js): one short line when there are none, Run now in sight and the rest in the
// ⋯ menu, Stop only on a second tap (the menu stays open for it), and a result that is text, never markup. A suggestion
// from an old OpenClaw job shows its preview, folded, with Add and No thanks; Turn off the old job? asks before anything happens.
// A new one is tried first (a test run, nothing sent or kept): its result shows when it is ready, then Add, Change or Cancel.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),posts=[],ID='c3'.repeat(16);
const routine=()=>({id:ID,name:'Sum up my deals',instructions:'Sum up my deals',rule:{unit:'week',n:1},anchor:'2026-11-09',at:'09:00',state:'on',next_due:'2026-11-16',
 runs:[{id:'r1',state:'ready',started_at:now,result:'**Fernwave** asked <img src=x onerror="window.__xss=1">\n- week of 2026-11-02',used:['Deal <b>notes</b>']}]});
const SID='d4'.repeat(16),suggestion=()=>({...routine(),id:SID,name:'Failed payments',instructions:'List customers whose payment failed',state:'suggested',next_due:null,
 runs:[{id:'r2',state:'ready',started_at:now,result:'**Halyard**: card declined'}]});
const TID='e5'.repeat(16),tryOne=words=>({...routine(),id:TID,name:words,instructions:words,state:'trying',next_due:null,runs:[],test:{id:'t1',state:'running',started_at:now}});
let list=[],suggested=[],trying=[];
const all=()=>JSON.stringify({routines:list,suggested,trying});
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/routines'){res.end(all());return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='routine_try'){if(b.args.id===ID)list=list.map(r=>({...r,test:{id:'t2',state:'ready',started_at:now,trial:b.args.words,result:'**Tried** it',got:!!b.args.steps?.get}}));else trying=[tryOne(b.args.words)];res.end(all());return}
  if(b.action==='routine_edit'){list=list.map(r=>({...r,steps:b.args.steps,...(b.args.name?{name:b.args.name}:{})}));res.end(all());return}
  if(b.action==='routine_state'&&b.args.id===TID){trying=[];res.end(all());return}
  if(b.action==='routine_accept'){list=[...list,{...suggestion(),state:'on'}];suggested=[];res.end(JSON.stringify({routines:list,suggested}));return}
  if(b.action==='routine_old_job'){list=list.map(r=>({...r,old_job:false}));res.end(JSON.stringify({routines:list,suggested}));return}
  if(b.action==='routine_state'&&b.args.id===SID){suggested=[];res.end(JSON.stringify({routines:list,suggested}));return}
  if(b.action==='routine_state'){list=b.args.to==='stop'?[]:list.map(r=>({...r,state:b.args.to==='pause'?'paused':'on'}));res.end(JSON.stringify({routines:list}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const sent=name=>posts.filter(p=>p.action===name);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1100,390]){
  posts.length=0;list=[];suggested=[];trying=[];
  const context=await browser.newContext({viewport:{width,height:900},timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
  // None yet: the input and one short line
  await page.locator('#routines-view .rt-empty').waitFor();
  assert.equal((await page.locator('#routines-view .rt-empty').innerText()).trim(),'No routines yet');
  assert.equal(await page.locator('#rt-words').getAttribute('placeholder'),'Every Monday, sum up my deals');
  // A long routine wraps and the box grows with it, up to about six lines, then scrolls; on a phone Add sits under it
  const words=page.locator('#rt-words'),one=(await words.boundingBox()).height;
  await words.fill('Every Friday at 4, look at what shipped this week in the project repository and sum it up in three short lines in the style of the earlier posts.');
  const grown=(await words.boundingBox()).height;assert.ok(grown>one*1.5,`the box grows (${one} -> ${grown})`);
  await words.fill('line\n'.repeat(20));const tall=(await words.boundingBox()).height;
  assert.ok(tall<one*7&&await words.evaluate(x=>x.scrollHeight>x.clientHeight),`it stops at about six lines and scrolls (${tall})`);
  const add=await page.locator('.rt-new>button').boundingBox(),box=await words.boundingBox();
  if(width<600)assert.ok(add.y>=box.y+box.height,'Add under the box on a phone');else assert.ok(add.x>=box.x+box.width,'Add beside it');
  // Shift+Enter is a new line; Enter tries it (the whole text, then the box empties)
  await words.fill('Sum up my deals');await words.press('Shift+Enter');assert.equal(await words.inputValue(),'Sum up my deals\n');assert.equal(sent('routine_try').length,0);
  await words.press('Enter');await page.waitForFunction(()=>!document.querySelector('#rt-words').value);
  assert.deepEqual(sent('routine_try'),[{action:'routine_try',words:'Sum up my deals'}]);assert.equal((await words.boundingBox()).height,one);
  // Its test run first: running, then its result without a reload; not one of your routines until Add
  const tc=page.locator(`.rt-try[data-rt="${TID}"]`);await tc.waitFor();
  assert.match(await tc.locator('.rt-run-head').innerText(),/^Test run\s+Running…$/);
  assert.deepEqual(await tc.locator('.actions>button').evaluateAll(n=>n.map(x=>x.textContent)),['Add','Change','Cancel']);
  assert.equal((await page.locator('#routines-view .rt-empty').innerText()).trim(),'No routines yet');
  trying=[{...trying[0],test:{...trying[0].test,state:'ready',result:'**3 deals** went quiet.'}}];
  await tc.locator('.rt-result strong').waitFor({timeout:8000});
  // Change: its words with Try it and Cancel (the card's buttons wait); Try it runs the new words once
  await tc.locator('[data-rt-do="change"]').click();const cw=tc.locator('.rt-form textarea');
  assert.equal(await cw.inputValue(),'Sum up my deals');assert.equal(await tc.locator('.actions').isVisible(),false);
  assert.deepEqual(await tc.locator('.rt-form-acts>button').evaluateAll(n=>n.map(x=>x.textContent)),['Try it','Cancel']);
  await cw.fill('Sum up my open deals');await cw.press('Enter');await tc.locator('.rt-form').waitFor({state:'detached'});
  assert.deepEqual(sent('routine_try').at(-1),{action:'routine_try',id:TID,words:'Sum up my open deals'});
  // Cancel: never kept
  await tc.locator('[data-rt-do="no"]').click();await tc.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_state'),[{action:'routine_state',id:TID,to:'stop'}]);posts.length=0;
  list=[routine()];await page.evaluate(()=>routinesView(true));
  const card=page.locator(`[data-rt="${ID}"]`);await card.waitFor();
  // The result is text with bold, never markup
  assert.equal(await card.locator('.rt-result strong').innerText(),'Fernwave');
  assert.equal(await page.evaluate(()=>window.__xss),undefined);
  // Markdown as in the chat (a real list), dates as the owner reads them
  assert.equal(await card.locator('.rt-result li').innerText(),'week of Nov 2');
  // The owner's skills it followed, by name (text, never markup)
  assert.equal(await card.locator('.rt-used').innerText(),'Used: Deal <b>notes</b>');
  // Run now in sight; Edit, Change when, Pause and Stop in the ⋯ menu
  assert.deepEqual(await card.locator('.actions>button').evaluateAll(n=>n.map(x=>x.textContent)),['Run now']);
  assert.equal(await card.locator('.more-menu').isVisible(),false);
  await card.locator('.more-actions>summary').click();
  assert.deepEqual(await card.locator('.more-menu>button').evaluateAll(n=>n.map(x=>x.textContent)),['Edit','Change when','Pause','Advanced: script steps','Stop']);
  const menu=await card.locator('.more-menu').boundingBox();assert.ok(menu.x>=0&&menu.x+menu.width<=width,'the menu fits the screen');
  // Change when: the menu closes so it never covers the field; Cancel and Esc leave it, Save changes this routine (never adds one)
  await card.locator('[data-rt-do="when"]').click();const when=card.locator('.rt-form[data-rt-form="when"] input');
  assert.equal(await card.locator('.more-menu').isVisible(),false);assert.equal(await when.evaluate(x=>x===document.activeElement),true);
  assert.deepEqual(await card.locator('.rt-form-acts>button').evaluateAll(n=>n.map(x=>x.textContent)),['Save','Cancel']);
  await card.locator('[data-rt-cancel]').click();assert.equal(await card.locator('.rt-form').count(),0);
  await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="when"]').click();await when.press('Escape');assert.equal(await card.locator('.rt-form').count(),0);
  await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="when"]').click();await page.locator('#routines-view>.fine').click();
  assert.equal(await card.locator('.rt-form').count(),0,'a click outside leaves it');
  await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="when"]').click();await when.fill('Every weekday at 8');await when.press('Enter');
  for(let i=0;i<60&&!sent('routine_when').length;i++)await page.waitForTimeout(50);
  assert.deepEqual(sent('routine_when'),[{action:'routine_when',id:ID,words:'Every weekday at 8'}]);assert.equal(sent('routine_try').length,0);
  // Edit: the routine's words in a growing box; Save sends them
  await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="edit"]').click();const edit=card.locator('.rt-form[data-rt-form="edit"] textarea');
  assert.equal(await edit.inputValue(),'Sum up my deals');await edit.fill('Sum up my won deals');
  assert.deepEqual(await card.locator('.rt-form-acts>button').evaluateAll(n=>n.map(x=>x.textContent)),['Save','Try it','Cancel']);
  // Try it: the new words' test run in the form, the routine as it was; the form and its words stay
  await card.locator('[data-rt-try]').click();await card.locator('.rt-form .rt-result strong').waitFor();
  assert.deepEqual(sent('routine_try'),[{action:'routine_try',id:ID,words:'Sum up my won deals'}],'no script steps unless Advanced shows them');
  assert.match(await card.locator('.rt-form .rt-run-head').innerText(),/^Test run\s+Nothing sent or saved$/);
  assert.equal(await card.locator('.rt-body').isVisible(),false,'the card\'s own result waits while Edit is open');
  assert.equal(await card.locator('.rt-what').isVisible(),false,'its words show once, in the box');
  assert.equal(await edit.inputValue(),'Sum up my won deals');
  await card.locator('.rt-form .primary').click();
  for(let i=0;i<60&&!sent('routine_edit').length;i++)await page.waitForTimeout(50);
  assert.deepEqual(sent('routine_edit'),[{action:'routine_edit',id:ID,words:'Sum up my won deals'}],'its script steps stay as they are');
  // Script steps: never in Edit by default; Advanced in the ... menu shows them, empty, with no made-up commands
  await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="edit"]').click();
  assert.equal(await card.locator('.rt-form .rt-steps').count(),0,'Edit is the routine\'s words only');
  await card.locator('[data-rt-cancel]').click();await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="steps"]').click();await card.locator('.rt-form[data-rt-form="edit"] .rt-steps').waitFor();
  assert.equal(await card.locator('.rt-steps legend').innerText(),'Advanced: script steps');
  assert.deepEqual(await card.locator('[data-step]').evaluateAll(n=>n.map(x=>[x.value,x.placeholder])),[['',''],['',''],['',''],['','']]);
  assert.equal(await page.evaluate(()=>document.activeElement.dataset.step),'get');
  await card.locator('[data-step="get"]').fill('python3 ~/scripts/deals.py --open');await card.locator('[data-step="cwd"]').fill('~/scripts');
  await card.locator('[data-step="timeout"]').fill('90');await card.locator('[data-step="check"]').fill('python3 ~/scripts/check.py');
  const steps={get:{command:'python3 ~/scripts/deals.py --open',cwd:'~/scripts',timeout:'90'},check:{command:'python3 ~/scripts/check.py'}};
  await card.locator('[data-rt-try]').click();await card.locator('.rt-form .rt-result strong').waitFor();
  assert.deepEqual(sent('routine_try').at(-1),{action:'routine_try',id:ID,words:'Sum up my deals',steps});
  assert.match(await card.locator('.rt-form .rt-run-head').innerText(),/^Test run\s+Nothing sent or saved · Got data$/);
  assert.equal(await card.locator('[data-step="get"]').inputValue(),'python3 ~/scripts/deals.py --open','what is typed stays');
  await card.locator('.rt-form .primary').click();
  for(let i=0;i<60&&sent('routine_edit').length<2;i++)await page.waitForTimeout(50);
  assert.deepEqual(sent('routine_edit').at(-1),{action:'routine_edit',id:ID,words:'Sum up my deals',steps});
  await card.locator('.rt-step').first().waitFor();
  assert.deepEqual(await card.locator('.rt-step').evaluateAll(n=>n.map(x=>x.textContent)),['Get data python3 ~/scripts/deals.py --open','Check python3 ~/scripts/check.py']);
  // A routine with script steps: Edit shows them, filled in
  await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="edit"]').click();
  assert.equal(await card.locator('.rt-form [data-step="get"]').inputValue(),'python3 ~/scripts/deals.py --open');
  await card.locator('[data-rt-cancel]').click();
  // Its name, in the title's place above the schedule line: Cancel keeps both as they were, Save sends a new name with the words
  await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="edit"]').click();const nm=card.locator('.rt-form .rt-name');
  assert.equal(await nm.inputValue(),'Sum up my deals');assert.equal(await card.locator('h3').isVisible(),false,'one title: the field');
  const [nb,wb,eb]=await Promise.all([nm.boundingBox(),card.locator('.rt-when').boundingBox(),card.locator('.rt-form textarea').boundingBox()]);
  assert.ok(nb.y+nb.height<=wb.y+1&&wb.y+wb.height<=eb.y+1,'name, then when, then the words');
  assert.equal(await page.evaluate(()=>document.activeElement.tagName),'TEXTAREA','the words have the focus, as before');
  await nm.fill('Deals digest');await card.locator('[data-rt-cancel]').click();
  assert.equal(await card.locator('h3').innerText(),'Sum up my deals');assert.equal(sent('routine_edit').length,2,'Cancel saves nothing');
  await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="edit"]').click();
  assert.equal(await nm.inputValue(),'Sum up my deals','Cancel took the typed name back');
  await nm.fill('  Deals digest ');await nm.press('Enter');
  for(let i=0;i<60&&sent('routine_edit').length<3;i++)await page.waitForTimeout(50);
  assert.deepEqual(sent('routine_edit').at(-1),{action:'routine_edit',id:ID,words:'Sum up my deals',steps,name:'Deals digest'});
  await card.locator('h3').waitFor();assert.equal(await card.locator('h3').innerText(),'Deals digest');
  // The Machine's own recipe: under Advanced only, read-only
  list=list.map(r=>({...r,steps:undefined,recipe:['gh pr list --repo acme/widgets --state merged --search merged:>={days_ago:7}']}));await page.evaluate(()=>routinesView(true));
  await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="edit"]').click();
  assert.equal(await card.locator('.rt-form .rt-recipe').count(),0,'Edit stays the routine\'s words');
  await card.locator('[data-rt-cancel]').click();await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="steps"]').click();
  assert.deepEqual(await card.locator('.rt-recipe code').evaluateAll(n=>n.map(x=>x.textContent)),['gh pr list --repo acme/widgets --state merged --search merged:>={days_ago:7}']);
  assert.equal(await card.locator('.rt-recipe :is(input,textarea,button)').count(),0,'read-only');
  await card.locator('[data-rt-cancel]').click();
  // Didn't work: what the script said, as text
  list=list.map(r=>({...r,runs:[{id:'r3',state:'failed',started_at:now,why:'Get data didn’t work.',detail:'<b>no such report</b>'}]}));await page.evaluate(()=>routinesView(true));
  assert.equal(await card.locator('.rt-detail').innerText(),'<b>no such report</b>');
  await card.locator('.more-actions>summary').click();
  // Stop: the first tap asks, and the menu stays open for the second
  await card.locator('[data-rt-do="stop"]').click();
  assert.equal(await card.locator('[data-rt-do="stop"]').innerText(),'Stop for good?');
  assert.equal(await card.locator('.more-menu').isVisible(),true);assert.equal(sent('routine_state').length,0);
  await card.locator('[data-rt-do="stop"]').click();await card.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_state'),[{action:'routine_state',id:ID,to:'stop'}]);
  // A suggestion: folded to its preview with Show more, Add and No thanks in sight; nothing happens before a tap
  suggested=[suggestion()];await page.evaluate(()=>routinesView(true));
  const s=page.locator(`.rt-sugg [data-rt="${SID}"]`);await s.waitFor();
  assert.equal(await s.locator('.rt-body').getAttribute('class'),'rt-body clamp');
  await s.locator('[data-more]').click();assert.equal(await s.locator('.rt-body').getAttribute('class'),'rt-body');assert.equal(await s.locator('[data-more]').innerText(),'Show less');
  assert.equal(await s.locator('.rt-result strong').innerText(),'Halyard');
  assert.deepEqual(await s.locator('.actions>button').evaluateAll(n=>n.map(x=>x.textContent)),['Add','No thanks']);
  await s.locator('[data-rt-do="no"]').click();await s.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_state').at(-1),{action:'routine_state',id:SID,to:'stop'});
  // Suggested first, then Your routines, then Paused (only when there are paused ones, with Resume in sight)
  suggested=[suggestion()];list=[{...routine(),state:'paused'}];await page.evaluate(()=>routinesView(true));
  await page.locator('.rt-paused').waitFor();
  assert.deepEqual(await page.locator('#routines-view h2').evaluateAll(n=>n.map(x=>x.textContent)),['Suggested','Paused']);
  assert.deepEqual(await page.locator(`.rt-paused [data-rt="${ID}"] .actions>button`).evaluateAll(n=>n.map(x=>x.textContent)),['Resume']);
  list=[];await page.evaluate(()=>routinesView(true));
  await page.locator(`.rt-sugg [data-rt="${SID}"] [data-rt-do="accept"]`).click();
  await page.locator(`.rt-mine [data-rt="${SID}"]`).waitFor();
  assert.deepEqual(sent('routine_accept'),[{action:'routine_accept',id:SID}]);
  assert.equal(await page.locator('.rt-sugg').count(),0);
  assert.deepEqual(await page.locator('#routines-view h2').evaluateAll(n=>n.map(x=>x.textContent)),['Your routines']);
  // A week of good runs: Turn off the old job? Only a tap turns it off
  list=list.map(r=>({...r,old_job:true}));await page.evaluate(()=>routinesView(true));
  const old=page.locator(`[data-rt="${SID}"] .rt-old`);await old.waitFor();
  assert.deepEqual(await old.locator('button').evaluateAll(n=>n.map(x=>x.textContent)),['Turn it off','Keep it']);
  assert.equal(sent('routine_old_job').length,0);
  await old.locator('[data-rt-old="off"]').click();await old.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_old_job'),[{action:'routine_old_job',id:SID,choice:'off'}]);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('routines dashboard ok');
}finally{await browser?.close();server.close()}
