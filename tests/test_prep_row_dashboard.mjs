import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A preparing to-do's status row (Preparing… and its clock, the browser links, the latest step, the live look at the
// browser) fits a phone: it wraps instead of pushing the page wider than the screen (2026-10-29: "Preparing… 2:14
// Sign in here Open the browser › Pu…" ran off a 390px screen). Sign in shows only while the run waits on a sign-in
// right now; a run that's past it, still on the browser, offers only Open the browser. The row is there only while
// the run is going: done, or not running, it's gone, links and all.
const dashboard=await dashboardPage();
const ID='a1a1a1a1a1a1a1a1';
const PNG='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
const card={id:ID,title:'The partner’s setup guide is ready for review',body:'The article update is drafted, with the partner link preserved.',
 status:'accepted',scope:'work',created_at:new Date().toISOString(),event_ids:[1],preparation_status:'running',preparation_retried:true,
 preparation_started_at:new Date(Date.now()-134000).toISOString(),
 preparation_browser:{since:new Date(Date.now()-60000).toISOString(),page:'https://help.example.com/articles/1',sign_in:false,link:'https://machine.example/browser/vnc.html?autoconnect=1'}};
const STEPS=[{title:'Publishing the article section in the help center editor with the link kept'}];
let progress;
const state=()=>({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/progress'){res.end(JSON.stringify(progress));return}
 if(url.pathname==='/api/peek'){res.end(JSON.stringify({on:true,image:PNG}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.PREP_ROW_SHOTS;  // a folder: also save what each size looks like
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[360,780],[1440,900]])for(const scheme of ['dark','light']){
  Object.assign(card,{status:'accepted',preparation_status:'running'});card.preparation_browser.sign_in=false;
  progress={status:'running',steps:STEPS,peek:true,browser:card.preparation_browser};
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,isMobile:width<500,hasTouch:width<500});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);const row=page.locator(`#task-${ID} .prep`);await row.waitFor();
  await page.locator(`#task-${ID} .steps li`).waitFor({timeout:15000});
  await page.locator(`#task-${ID} .peek-thumb img`).waitFor({timeout:15000});
  const at=`${width}x${height} ${scheme}`;
  // Past any sign-in, still on the browser: Open the browser, no Sign in
  assert.equal(await row.getByRole('link',{name:'Open the browser'}).count(),1,at);
  assert.equal(await row.locator('[data-signin]').count(),0,at);
  assert.ok(!(await row.innerText()).includes('Sign in'),at);
  // Nothing is wider than the screen: not the page, not the row, not a link in it
  const fits=async what=>{const fit=await page.evaluate(id=>{const card=document.getElementById('task-'+id).getBoundingClientRect();
    const wide=[...document.querySelectorAll(`#task-${id} .prep, #task-${id} .prep *`)].filter(n=>n.getBoundingClientRect().right>card.right+0.5).map(n=>n.className||n.tagName);
    return {page:document.documentElement.scrollWidth,view:innerWidth,wide}},ID);
   assert.ok(fit.page<=fit.view,`${what}: page ${fit.page}px wide on a ${fit.view}px screen`);
   assert.deepEqual(fit.wide,[],what)};
  await fits(at);
  if(shots)await page.locator(`#task-${ID}`).screenshot({path:`${shots}/prep-row-${width}-${scheme}.png`});
  // Waiting on a sign-in right now: Sign in shows, and still fits
  card.preparation_browser.sign_in=true;progress={...progress,browser:card.preparation_browser};await page.evaluate(()=>refresh());
  await row.getByRole('button',{name:'Sign in',exact:true}).waitFor({timeout:15000});
  await fits(at+' with Sign in');
  if(shots&&scheme==='dark')await page.locator(`#task-${ID}`).screenshot({path:`${shots}/prep-row-${width}-signin.png`});
  // Done: the whole row goes, links and all
  Object.assign(card,{status:'prepared',preparation_status:'done'});delete card.preparation_browser;progress={status:'done',steps:[]};
  await page.evaluate(()=>refresh());await row.waitFor({state:'detached',timeout:9000});
  assert.equal(await page.locator(`#task-${ID} .browser-link`).count(),0,at);
  assert.equal(await page.locator(`#task-${ID} .elapsed`).count(),0,at);
  card.preparation_browser={since:new Date().toISOString(),page:'https://help.example.com/articles/1',sign_in:false,link:'https://machine.example/browser/vnc.html?autoconnect=1'};
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('prep row ok');
