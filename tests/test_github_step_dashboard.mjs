// A final step on GitHub (filing an issue): the to-do says how it runs (GitHub's gh tool as the signed-in login, or the
// browser when GitHub isn't connected, with Connect GitHub), the Confirm review repeats it, and nothing runs before
// Confirm. Made-up data, a local fixture server, nothing reaches GitHub. SHOT_DIR=<folder> saves screenshots.
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

const dashboard=await dashboardPage();
const viaGh='1234567890abcdef',viaBrowser='fedcba0987654321',ghRev='aaaaaaaaaaaa',brRev='bbbbbbbbbbbb';
const preview='Repository: example-org/example-app\nLabel: BUG\n\nExport button does nothing on mobile\n\nSteps: open Settings, tap Export. Nothing happens.';
const step={kind:'finish',label:'Submit GitHub issue',url:'https://github.com/example-org/example-app/issues/new',instructions:'File it.',preview};
const gh={...step,revision:ghRev,via:'gh',via_login:'sam-example',attachments:[{name:'export-button.png',sha256:'c'.repeat(64),size:120000,type:'image/png'}]};
const browserStep={...step,revision:brRev,via:'browser'};
const card=(id,title,a)=>({id,title,body:'The issue is ready to file.',status:'prepared',event_ids:[1],next_action:a,next_actions:[a],
  outcome:JSON.stringify({state:'needs_you',needs:'Confirm filing the issue'}),scope:'work',created_at:new Date().toISOString()});
const state=()=>({suggestions:[card(viaGh,'File the export bug',gh),card(viaBrowser,'File the login bug',browserStep)],
  connectors:[],suggestion_counts:{prepared:2},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]});
const calls=[],errors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){let b='';for await(const c of req)b+=c;const call=JSON.parse(b);calls.push(call);
  res.end(JSON.stringify(call.action==='connect_sources'?{sources:[{name:'github',label:'GitHub',service:'github',signin:true,what:'Review requests, mentions, assignments and failed CI runs.'}],saveable:true,paired:true}:{status:'queued'}));return}
 res.statusCode=url.pathname.startsWith('/api/')?200:404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOT_DIR;if(shots)await mkdir(shots,{recursive:true});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,700],[1440,900]]){
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.evaluate(()=>refresh());
  // gh signed in: the to-do says it runs with gh as that login, and that the screenshot goes in through the browser
  const ghCard=page.locator(`#task-${viaGh}`);await ghCard.waitFor();
  assert.equal(await ghCard.locator('.draft-why').textContent(),'Runs with GitHub’s gh tool as sam-example. Files go in through your Machine’s browser.');
  assert.equal(await ghCard.locator('.draft .dm .via-ico').getAttribute('aria-label'),'GitHub');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll at '+width);
  if(shots)await ghCard.screenshot({path:`${shots}/github-gh-card-${width}x${height}.png`});
  // Nothing GitHub connected: it says the browser plainly, with the one step that connects GitHub
  const brCard=page.locator(`#task-${viaBrowser}`);
  assert.equal(await brCard.locator('.draft-why').textContent(),'GitHub isn’t connected, so this runs in your Machine’s browser. Connect GitHub');
  assert.equal(await brCard.locator('.draft .dm .via-ico').getAttribute('aria-label'),'Browser');
  if(shots)await brCard.screenshot({path:`${shots}/github-browser-card-${width}x${height}.png`});
  // Confirm's review says it too; nothing runs before Confirm
  await ghCard.locator(`[data-smart="${ghRev}"]`).click();
  await page.locator('#send-dialog').waitFor({state:'visible'});
  assert.match(await page.locator('#send-head').textContent(),/HowRuns with GitHub’s gh tool as sam-example\./);
  assert.equal(calls.filter(c=>c.action==='confirm_action').length,0);
  if(shots)await page.locator('#send-dialog').screenshot({path:`${shots}/github-gh-confirm-${width}x${height}.png`});
  await page.locator('#send-confirm').click();
  for(let i=0;i<100&&!calls.some(c=>c.action==='confirm_action');i++)await page.waitForTimeout(20);
  const confirm=calls.find(c=>c.action==='confirm_action');
  assert.equal(confirm.args.suggestion_id,viaGh);assert.equal(confirm.args.revision,ghRev);
  calls.length=0;
  await brCard.locator('.draft-why a[data-connect-open="github"]').click();
  await page.locator('#connect-add .connect-signin').waitFor({state:'visible'});
  assert.deepEqual(calls.filter(c=>c.action==='confirm_action'),[]);
  if(shots)await page.screenshot({path:`${shots}/github-connect-${width}x${height}.png`});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
