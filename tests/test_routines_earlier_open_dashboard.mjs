import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Another routine running leaves an opened one alone (dashboard/routines-page.js rtFull, rtDetails): the looks every few
// seconds while it runs redraw only the card that changed. Earlier, Show more and the ⋯ menu stay open on the others, and
// stay open when their own card is drawn again; an Edit form keeps its words. Earlier kept closing on every look.
const dashboard=await dashboardPage();
const now=Date.now(),ago=d=>new Date(now-d*864e5).toISOString(),A='a1'.repeat(16),B='b2'.repeat(16);
const LONG='**Fernwave**: release notes drafted and sent to the team.\n'.repeat(5);
let aRuns=[{id:'a3',state:'ready',started_at:ago(0),result:LONG},{id:'a2',state:'ready',started_at:ago(7),result:'**Two things shipped**: the new board and faster search.'},
 {id:'a1',state:'nothing',started_at:ago(14),why:'Nothing shipped this week.'}];
let bRuns=[{id:'b1',state:'ready',started_at:ago(1),result:'Five new leads from the web form.'}],looks=0;
const routine=(id,name,instructions,runs)=>({id,name,instructions,rule:{unit:'week',n:1},anchor:'2026-11-13',at:'16:00',state:'on',next_due:'2026-11-13',runs});
const all=()=>JSON.stringify({routines:[routine(A,'Shipped this week','Check what shipped in the project repository and write a short post',aRuns),
 routine(B,'New leads','Every Friday, list the new leads from the web form',bRuns)],suggested:[],trying:[]});
const state={suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/routines'){looks++;res.end(all());return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);if(b.action==='routine_run_now'&&b.args.id===B)bRuns=[{id:'b'+(bRuns.length+1),state:'running',started_at:ago(0)},...bRuns];res.end(all());return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[],shots=process.env.SHOTS_DIR;let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of shots?[[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]:[[390,844,'light'],[1440,900,'dark']]){
  aRuns=aRuns.slice(-3);bRuns=bRuns.slice(-1);
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,...(width<600?{isMobile:true,hasTouch:true}:{})});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.clock.install();
  await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
  const a=page.locator(`[data-rt="${A}"]`),b=page.locator(`[data-rt="${B}"]`),earlier=a.locator('details.rt-earlier');await a.waitFor();
  // Show more, then Earlier on A; B runs, with several looks while it does
  await a.locator('button.more').click();await earlier.locator('summary').click();
  assert.equal(await earlier.evaluate(d=>d.open),true);
  await a.evaluate(x=>{x._same=1});
  await b.locator('[data-rt-do="now"]').click();await b.locator('.rt-body>.rt-run .rt-state.rt-running').waitFor();
  const before=looks;
  for(let i=0;i<4;i++){await page.clock.runFor(4100);await page.waitForTimeout(120)}
  assert.ok(looks-before>=3,'it looked again while B ran');
  assert.equal(await earlier.evaluate(d=>d.open),true,'Earlier stays open while another routine runs');
  assert.equal(await a.evaluate(x=>x._same),1,'the card next to a running one is not drawn again');
  assert.equal(await a.locator('button.more').getAttribute('aria-expanded'),'true','Show more stays open');
  if(shots){await a.locator('.rt-body').evaluate(x=>x.scrollIntoView({block:'start'}));await page.waitForTimeout(100);await page.screenshot({path:`${shots}/earlier-open-${width}-${scheme}.png`})}
  // B is done; A's own card changes too (a new run): drawn again, with Earlier still open and the ⋯ menu as it was
  bRuns=[{...bRuns[0],state:'ready',result:'Two new leads from the web form.'},...bRuns.slice(1)];
  aRuns=[{id:'a4',state:'ready',started_at:ago(0),result:'**One thing shipped**: dark mode.'},...aRuns];
  await page.clock.runFor(4100);await page.waitForTimeout(150);
  await page.evaluate(()=>routinesView(true));await b.locator('.rt-body>.rt-run .rt-state.rt-ready').waitFor();
  assert.equal(await a.locator('.rt-earlier .rt-run').count(),3,'A shows its new run');
  assert.equal(await earlier.evaluate(d=>d.open),true,'Earlier opens again when its own card is drawn again');
  // An Edit form on A keeps its words while B runs again (on its schedule: a click outside closes the form on a computer)
  await a.locator('.more-actions>summary').click();await a.locator('[data-rt-do="edit"]').click();
  const words='Check what shipped in the project repository and write a short, playful post';
  await a.locator('.rt-form textarea').fill(words);
  bRuns=[{id:'b'+(bRuns.length+1),state:'running',started_at:ago(0)},...bRuns];
  await page.evaluate(()=>routinesView(true));await b.locator('.rt-body>.rt-run .rt-state.rt-running').waitFor();
  for(let i=0;i<3;i++){await page.clock.runFor(4100);await page.waitForTimeout(120)}
  assert.equal(await a.locator('.rt-form textarea').inputValue(),words,'the form keeps its words');
  assert.equal(await earlier.evaluate(d=>d.open),true);
  await a.locator('[data-rt-cancel]').click();
  assert.equal(await earlier.evaluate(d=>d.open),true,'closing the form keeps Earlier open');
  // Closed again by hand: a look leaves it closed
  await earlier.locator('summary').click();await page.waitForTimeout(50);
  await page.evaluate(()=>routinesView(true));await page.waitForTimeout(200);
  assert.equal(await earlier.evaluate(d=>d.open),false,'closed stays closed');
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
