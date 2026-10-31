import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Recurring to-dos on the dashboard (dashboard/todos-repeat.js): one short line on a repeating to-do (with "missed 1"),
// Repeat and Skip this one under More, the Repeat box (a rhythm, Custom… and Stop repeating), Repeats in New to-do,
// "repeat this every month" in the to-do's chat, and the one-time "Make this a recurring to-do?". Nothing is sent.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),posts=[],R1='a1'.repeat(8),P1='b2'.repeat(8);
// Monday 2 November 2026: the first Monday of its month
const cards=[{id:R1,title:'Run payroll',body:'Every first Monday.',status:'pending',scope:'work',created_at:now,event_ids:[1],due:'2026-11-02',
  repeats:{series:'s1',rule:{unit:'month',n:1,nth:1},anchor:'2026-11-02',due:'2026-11-02',missed:1,next:'2026-12-07'}},
 {id:P1,title:'Water the plants',body:'',status:'pending',scope:'personal',created_at:now,event_ids:[2],due:'2026-11-02'}];
let offer={key:'fact:7',title:'Send the board update',rule:{unit:'month',n:1},anchor:'2026-11-05'};
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 recurring_offer:offer,locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='card_repeat'){const rule=b.args.repeat==='none'||/stop/i.test(b.args.words||'')?null:b.args.repeat||{unit:'month',n:1};
   res.end(JSON.stringify({id:b.args.suggestion_id,repeats:rule&&{rule,anchor:'2026-11-02',due:'2026-11-02',missed:0}}));return}
  if(b.action==='card_repeat_skip'){res.end(JSON.stringify({id:b.args.suggestion_id,next:'2026-12-07'}));return}
  if(b.action==='repeat_read'){res.end(JSON.stringify(/2 weeks/.test(b.args.text)?{rule:{unit:'week',n:2},anchor:'2026-11-02'}:{rule:null}));return}
  if(b.action==='recurring_offer'){offer=null;res.end(JSON.stringify({key:b.args.key,made:null}));return}
  if(b.action==='card_chat'){res.end(JSON.stringify({session:false,active:false,status:null,items:[],cursor:null}));return}
  if(b.action==='card_new'){res.end(JSON.stringify({id:'n1',repeats:b.args.repeat?{rule:b.args.repeat,anchor:'2026-11-02'}:undefined}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const sent=name=>posts.filter(p=>p.action===name);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1100,390]){
  posts.length=0;offer={key:'fact:7',title:'Send the board update',rule:{unit:'month',n:1},anchor:'2026-11-05'};
  const context=await browser.newContext({viewport:{width,height:900},timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+R1).waitFor();
  // One short line on the to-do, and nothing on one that doesn't repeat
  assert.equal((await page.locator('#task-'+R1+' .chip.repeat').innerText()).trim(),'Repeats monthly on the first Monday · missed 1');
  assert.equal(await page.locator('#task-'+P1+' .chip.repeat').count(),0);
  if(width<600){const box=await page.locator('#task-'+R1).boundingBox(),chip=await page.locator('#task-'+R1+' .chip.repeat').boundingBox();assert.ok(chip.x+chip.width<=box.x+box.width+1,'the line fits the to-do at phone width')}
  // More: Change repeat and Skip this one while it repeats; Repeat on one that doesn't
  const menu=id=>page.locator(`#task-${id} .more-menu>button`).evaluateAll(n=>n.map(x=>x.textContent.trim()));
  assert.ok((await menu(R1)).includes('Change repeat')&&(await menu(R1)).includes('Skip this one'));
  assert.ok((await menu(P1)).includes('Repeat')&&!(await menu(P1)).includes('Skip this one'));
  // The Repeat box: the rhythms from the to-do's date, the current one pressed, Custom… and Stop repeating
  await page.locator('#task-'+R1+' .chip.repeat').click();const box=page.locator('#task-'+R1+' .repeat-picker');await box.waitFor();
  assert.deepEqual(await box.locator('.rp-list button').evaluateAll(n=>n.map(x=>x.textContent)),
   ['Daily','Weekdays','Weekly on Monday','Monthly on day 2','Monthly on the first Monday','Yearly on November 2','Custom…']);
  assert.equal(await box.locator('[aria-pressed="true"]').innerText(),'Monthly on the first Monday');
  await box.getByText('Stop repeating').click();await box.waitFor({state:'detached'});
  assert.deepEqual(sent('card_repeat').at(-1),{action:'card_repeat',suggestion_id:R1,repeat:'none'});
  // Repeat on a to-do: Custom… reads the words, Enter sets it
  await page.locator('#task-'+P1+' .more-actions summary').click();await page.locator('#task-'+P1+' .more-menu [data-repeat]').click();
  const pbox=page.locator('#task-'+P1+' .repeat-picker');await pbox.waitFor();await pbox.getByText('Custom…').click();
  await pbox.locator('.rp-custom input').fill('every 2 weeks');await pbox.getByText('Repeats every 2 weeks on Monday').waitFor();await pbox.locator('.rp-custom input').press('Enter');
  await pbox.waitFor({state:'detached'});assert.deepEqual(sent('card_repeat').at(-1).repeat,{unit:'week',n:2});
  // Skip this one
  await page.locator('#task-'+R1+' .more-actions summary').click();await page.locator('#task-'+R1+' [data-repeat-skip]').click();
  await page.getByText('Skipped. The next one comes Mon, Dec 7.').waitFor();assert.equal(sent('card_repeat_skip').at(-1).suggestion_id,R1);
  // The one-time suggestion: No thanks posts the answer and it is gone
  const line=page.locator('.repeat-offer');await line.waitFor();assert.match(await line.innerText(),/Make this a recurring to-do\?\s*Send the board update · Repeats monthly on day 5/);
  await line.getByText('No thanks').click();await line.waitFor({state:'detached'});
  assert.deepEqual(sent('recurring_offer').at(-1),{action:'recurring_offer',key:'fact:7',choice:'no',scope:null});
  // New to-do: Repeats, a rhythm, and it goes with the to-do
  await page.locator('body').click({position:{x:5,y:5}});await page.keyboard.press('n');await page.locator('#nc-text').waitFor();
  await page.locator('#nc-text').fill('Back up the laptop');await page.locator('#nc-chips [data-nc="repeat"]').click();
  await page.locator('#nc-pick [data-rp="0"]').click();assert.match(await page.locator('#nc-chips [data-nc="repeat"]').innerText(),/^Repeats daily/);
  await page.locator('#nc-add').click();await page.locator('#new-card').waitFor({state:'hidden'});
  assert.deepEqual(sent('card_new').at(-1).repeat,{unit:'day',n:1});
  assert.equal(sent('card_new').filter(p=>p.text==='Back up the laptop').length,1);
  // Its chat: "repeat this every month" sets it at once and is not sent on as a chat message
  await page.locator('#task-'+P1+' .card-foot a.card-chat-link').click();const input=page.locator('#chat-input');await input.waitFor();
  const before=sent('card_repeat').length;await input.fill('repeat this every month');await input.press('Enter');
  await page.waitForFunction(n=>true,before);await page.getByText('Repeats monthly on day 2.').first().waitFor();
  assert.equal(sent('card_repeat').at(-1).words,'repeat this every month');assert.deepEqual(posts.filter(p=>p.action!=='card_repeat'&&JSON.stringify(p).includes('every month')),[],'not sent on as a chat message');assert.equal(await input.inputValue(),'');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('recurring dashboard ok');
}finally{await browser?.close();server.close()}
