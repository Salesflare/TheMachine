import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A card body's link to a result file ("Your [plan](memory/assistant/x.md) is ready") keeps its words: a link that
// opens that file the way Read result does, or plain words when the task doesn't serve that file. Any other link the
// card can't open ([words](notes/x.md), [words](javascript:...)) stays inert text with its words (test_card_links).
const dashboard=await dashboardPage();
const now=new Date().toISOString(),path='memory/assistant/261102-practice-plan.md';
const cards=[
 {id:'a1a1a1a1a1a1a1a1',title:'Pick a practice plan for the choir',status:'prepared',scope:'personal',created_at:now,event_ids:[1],
  body:`Your [practice plan](${path}) is ready. It helps you choose between three rehearsal schedules for Robin and Kai.`,
  result_files:[{name:'261102-practice-plan.md',path}]},
 {id:'b2b2b2b2b2b2b2b2',title:'Check the venue notes',status:'prepared',scope:'work',created_at:now,event_ids:[2],
  body:'See [the old notes](memory/assistant/gone.md) and [the venue page](notes/venue.md), not [this](javascript:alert(1)) or [that](javascript:void).'}];
const opened=[];
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/result'){opened.push(url.searchParams.get('file'));res.end(JSON.stringify({text:'# Practice plan\n\nThree schedules to choose from.'}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const width of [390,1280]){
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  const card=page.locator('#task-a1a1a1a1a1a1a1a1');await card.waitFor();
  const body=card.locator('.body');
  assert.match(await body.innerText(),/^Your practice plan is ready\. It helps you choose/);
  const link=body.locator('button.result-link');
  assert.equal(await link.textContent(),'practice plan');
  assert.equal(await link.getAttribute('data-file'),path);
  if(process.env.SHOT_DIR)await card.screenshot({path:`${process.env.SHOT_DIR}/card-${width}-${scheme}.png`});
  if(scheme==='light'&&width===390){
   // It opens that file the way Read result does
   await link.click();await page.locator('#result-dialog[open]').waitFor();
   assert.equal(opened.at(-1),path);assert.match(await page.locator('#result-content').innerText(),/Three schedules/);
   await page.keyboard.press('Escape');
   // A result file the task doesn't serve: its words, no link. A relative or script link: inert text, words kept.
   const other=page.locator('#task-b2b2b2b2b2b2b2b2 .body');
   assert.equal((await other.innerText()).trim(),'See the old notes and [the venue page](notes/venue.md), not [this](javascript:alert(1)) or [that](javascript:void).');
   assert.equal(await other.locator('a,button').count(),0);
   // The copied text of a result without a file keeps the words too
   assert.equal(await page.evaluate(()=>resultBody(state.suggestions[0])),cards[0].body.replace(`[practice plan](${path})`,'practice plan'));
  }
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('card result link ok');
}finally{await browser?.close();await new Promise(r=>server.close(r))}
