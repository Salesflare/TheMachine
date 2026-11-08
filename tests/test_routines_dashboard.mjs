import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Routines page (dashboard/routines-page.js): one short line when there are none, Run now in sight and the rest in the
// ⋯ menu, Stop only on a second tap (the menu stays open for it), and a result that is text, never markup. A suggestion
// from an old OpenClaw job shows its preview with Add and No thanks; Turn off the old job? asks before anything happens.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),posts=[],ID='c3'.repeat(16);
const routine=()=>({id:ID,name:'Sum up my deals',instructions:'Sum up my deals',rule:{unit:'week',n:1},anchor:'2026-11-09',at:'09:00',state:'on',next_due:'2026-11-16',
 runs:[{id:'r1',state:'ready',started_at:now,result:'**Fernwave** asked <img src=x onerror="window.__xss=1">'}]});
const SID='d4'.repeat(16),suggestion=()=>({...routine(),id:SID,name:'Failed payments',instructions:'List customers whose payment failed',state:'suggested',next_due:null,
 runs:[{id:'r2',state:'ready',started_at:now,result:'**Halyard**: card declined'}]});
let list=[],suggested=[];
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/routines'){res.end(JSON.stringify({routines:list,suggested}));return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
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
  posts.length=0;list=[];suggested=[];
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
  // Shift+Enter is a new line; Enter adds (the whole text, then the box empties)
  await words.fill('Sum up my deals');await words.press('Shift+Enter');assert.equal(await words.inputValue(),'Sum up my deals\n');assert.equal(sent('routine_new').length,0);
  await words.press('Enter');await page.waitForFunction(()=>!document.querySelector('#rt-words').value);
  assert.deepEqual(sent('routine_new'),[{action:'routine_new',words:'Sum up my deals'}]);assert.equal((await words.boundingBox()).height,one);
  list=[routine()];await page.evaluate(()=>routinesView(true));
  const card=page.locator(`[data-rt="${ID}"]`);await card.waitFor();
  // The result is text with bold, never markup
  assert.equal(await card.locator('.rt-result strong').innerText(),'Fernwave');
  assert.equal(await page.evaluate(()=>window.__xss),undefined);
  // Run now in sight; Change when, Pause and Stop in the ⋯ menu
  assert.deepEqual(await card.locator('.actions>button').evaluateAll(n=>n.map(x=>x.textContent)),['Run now']);
  assert.equal(await card.locator('.more-menu').isVisible(),false);
  await card.locator('.more-actions>summary').click();
  assert.deepEqual(await card.locator('.more-menu>button').evaluateAll(n=>n.map(x=>x.textContent)),['Change when','Pause','Stop']);
  const menu=await card.locator('.more-menu').boundingBox();assert.ok(menu.x>=0&&menu.x+menu.width<=width,'the menu fits the screen');
  // Change when changes this routine, never adds a new one
  await card.locator('[data-rt-do="when"]').click();await card.locator('.rt-when-form input').fill('Every weekday at 8');await card.locator('.rt-when-form input').press('Enter');
  for(let i=0;i<60&&!sent('routine_when').length;i++)await page.waitForTimeout(50);
  assert.deepEqual(sent('routine_when'),[{action:'routine_when',id:ID,words:'Every weekday at 8'}]);assert.equal(sent('routine_new').length,1);
  if(!await card.locator('.more-menu').isVisible())await card.locator('.more-actions>summary').click();
  // Stop: the first tap asks, and the menu stays open for the second
  await card.locator('[data-rt-do="stop"]').click();
  assert.equal(await card.locator('[data-rt-do="stop"]').innerText(),'Stop for good?');
  assert.equal(await card.locator('.more-menu').isVisible(),true);assert.equal(sent('routine_state').length,0);
  await card.locator('[data-rt-do="stop"]').click();await card.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_state'),[{action:'routine_state',id:ID,to:'stop'}]);
  // A suggestion: its preview, Add and No thanks; nothing happens before a tap
  suggested=[suggestion()];await page.evaluate(()=>routinesView(true));
  const s=page.locator(`.rt-sugg [data-rt="${SID}"]`);await s.waitFor();
  assert.equal(await s.locator('.rt-result strong').innerText(),'Halyard');
  assert.deepEqual(await s.locator('.actions>button').evaluateAll(n=>n.map(x=>x.textContent)),['Add','No thanks']);
  await s.locator('[data-rt-do="no"]').click();await s.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_state').at(-1),{action:'routine_state',id:SID,to:'stop'});
  suggested=[suggestion()];await page.evaluate(()=>routinesView(true));
  await page.locator(`.rt-sugg [data-rt="${SID}"] [data-rt-do="accept"]`).click();
  await page.locator(`#routines-view>[data-rt="${SID}"]`).waitFor();
  assert.deepEqual(sent('routine_accept'),[{action:'routine_accept',id:SID}]);
  assert.equal(await page.locator('.rt-sugg').count(),0);
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
