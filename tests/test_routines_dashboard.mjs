import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Routines page (dashboard/routines-page.js): one short line when there are none, Run now in sight and the rest in the
// ⋯ menu, Stop only on a second tap (the menu stays open for it), and a result that is text, never markup.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),posts=[],ID='c3'.repeat(16);
const routine=()=>({id:ID,name:'Sum up my deals',instructions:'Sum up my deals',rule:{unit:'week',n:1},anchor:'2026-11-09',at:'09:00',state:'on',next_due:'2026-11-16',
 runs:[{id:'r1',state:'ready',started_at:now,result:'**Fernwave** asked <img src=x onerror="window.__xss=1">'}]});
let list=[];
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/routines'){res.end(JSON.stringify({routines:list}));return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='routine_state'){list=b.args.to==='stop'?[]:list.map(r=>({...r,state:b.args.to==='pause'?'paused':'on'}));res.end(JSON.stringify({routines:list}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const sent=name=>posts.filter(p=>p.action===name);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1100,390]){
  posts.length=0;list=[];
  const context=await browser.newContext({viewport:{width,height:900},timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
  // None yet: the input and one short line
  await page.locator('#routines-view .rt-empty').waitFor();
  assert.equal((await page.locator('#routines-view .rt-empty').innerText()).trim(),'No routines yet');
  assert.equal(await page.locator('#rt-words').getAttribute('placeholder'),'Every Monday, sum up my deals');
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
  // Stop: the first tap asks, and the menu stays open for the second
  await card.locator('[data-rt-do="stop"]').click();
  assert.equal(await card.locator('[data-rt-do="stop"]').innerText(),'Stop for good?');
  assert.equal(await card.locator('.more-menu').isVisible(),true);assert.equal(sent('routine_state').length,0);
  await card.locator('[data-rt-do="stop"]').click();await card.waitFor({state:'detached'});
  assert.deepEqual(sent('routine_state'),[{action:'routine_state',id:ID,to:'stop'}]);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('routines dashboard ok');
}finally{await browser?.close();server.close()}
