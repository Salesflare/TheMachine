import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do waits on a sign-in; the owner signs in in the browser and the service carries the run on by itself
// (watch_sign_ins). The card shows that within seconds, without a tap. Continue on a card drawn before that is no
// error (2026-10-27: "Try again is available only for a blocked preparation" as a toast). Closing the Browser pane
// asks the service to look at once. A card closed meanwhile says so, not as an error. SHOTS=<folder> saves shots.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const ID='aaaaaaaaaaaaaaa1';
const REASON='Example is signed out; sign in on the example login tab in the browser, then tap Continue.';
let prep='blocked',checks=0,resumeOnCheck=false,closed=false,signedIn=false;const posts=[];
const card=()=>({id:ID,title:'Check the outage at home',body:'I can look at the provider’s status page.',status:closed?'completed':prep==='done'?'prepared':'accepted',scope:'personal',
 created_at:new Date().toISOString(),event_ids:[1],preparation_status:prep,preparation_signed_in:signedIn&&prep!=='blocked',preparation_started_at:prep==='blocked'?null:new Date().toISOString(),
 ...(prep==='blocked'?{preparation_reason:REASON,preparation_browser:{sign_in:true,page:'https://www.example.com/login',since:new Date().toISOString(),link:'https://machine.example/view'}}:{})});
const state=()=>({suggestions:[card()],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],
 fleet:{on:false,fleets:[]},browser_link:'https://machine.example/view',browser_embed:'/browser/'});
const server=createServer(async(req,res)=>{let body='';for await(const b of req)body+=b;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/progress'){res.end(JSON.stringify({status:prep,steps:[],browser:null,peek:false}));return}
 if(url.pathname==='/browser/'){res.setHeader('Content-Type','text/html');res.end('<body><p id="viewer">viewer</p></body>');return}
 if(url.pathname==='/api/action'){const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='browser_login_check'){checks++;if(resumeOnCheck&&prep==='blocked'){prep='queued';signedIn=true;res.end(JSON.stringify({resumed:[ID]}));return}res.end(JSON.stringify({resumed:[]}));return}
  if(action==='browser_focus'){res.end(JSON.stringify({shown:true}));return}
  if(action==='decide'&&args.choice==='retry'){  // as Store._decide answers it
   if(prep==='blocked'&&!closed){prep='queued';res.end(JSON.stringify({status:'accepted',retrying:true}));return}
   if(!closed){res.end(JSON.stringify({status:card().status,already:prep==='done'?'done':'running'}));return}
   res.end(JSON.stringify({status:'completed',duplicate:true,skipped:true,reason:'stale_retry',already:'closed'}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const toast=page=>page.locator('#toast.show');
const starting=page=>page.locator('.note',{hasText:'Signed in. I’ll start shortly.'}).first().waitFor({timeout:8000});  // queued: what the card shows next
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [w,h] of [[1440,900],[1440,700],[390,844]]){
  prep='blocked';closed=false;resumeOnCheck=false;signedIn=false;
  const context=await browser.newContext({viewport:{width:w,height:h},timezoneId:'UTC'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);
  const go=page.locator(`button[data-id="${ID}"][data-choice="retry"]`);await go.waitFor({timeout:15000});
  assert.equal((await go.innerText()).trim(),'Continue');
  if(shots)await page.screenshot({path:`${shots}/1-blocked-${w}x${h}.png`});
  // His state: the service already carried on, the card is still the one drawn before. Continue: no error.
  prep='queued';signedIn=true;
  await go.click();
  await toast(page).filter({hasText:'Already carrying on with it.'}).waitFor({timeout:8000});
  assert.equal(await page.locator('#toast').evaluate(t=>t.classList.contains('error')),false,'not an error');
  await starting(page);
  assert.equal(await go.count(),0,'no Continue left on a card that carries on');
  if(shots)await page.screenshot({path:`${shots}/2-stale-continue-${w}x${h}.png`});
  // Back to waiting; the owner signs in elsewhere and taps nothing: the card shows it carried on within seconds.
  prep='blocked';await page.evaluate(()=>refresh());await go.waitFor();
  prep='queued';signedIn=true;
  await toast(page).filter({hasText:'Signed in. Carrying on with it.'}).waitFor({timeout:8000});
  await starting(page);
  if(shots)await page.screenshot({path:`${shots}/3-carried-on-by-itself-${w}x${h}.png`});
  if(w>=1024){
   // Open the browser on the card shows the pane; closing it looks at once and the card carries on.
   prep='blocked';await page.evaluate(()=>refresh());await go.waitFor();
   const open=page.locator(`[data-browser-focus="${ID}"]`).first();
   const pages=context.pages().length;await open.click();
   await page.locator('#browser-pane').waitFor();assert.equal(context.pages().length,pages,'the pane, not a new tab');
   resumeOnCheck=true;const before=checks;
   await page.locator('#toast.show').waitFor({state:'detached',timeout:10000});  // the last step's toast is gone first
   await page.locator('#bp-close').click();
   for(const t=Date.now();checks===before&&Date.now()-t<8000;)await page.waitForTimeout(100);
   assert.ok(checks>before,'closing the pane asked the service to look');
   await toast(page).filter({hasText:'Signed in. Carrying on with it.'}).waitFor({timeout:8000});
   await starting(page);
   if(shots)await page.screenshot({path:`${shots}/4-pane-closed-${w}x${h}.png`});
  }
  // A to-do closed meanwhile (on the phone): the stale Continue says so in plain words and the card redraws.
  prep='blocked';await page.evaluate(()=>refresh());await go.waitFor();
  closed=true;
  await go.click();
  await toast(page).filter({hasText:'Nothing is waiting to try again here.'}).waitFor({timeout:8000});
  assert.equal(await page.locator('#toast').evaluate(t=>t.classList.contains('error')),false,'a stale tap, not an error');
  await page.waitForFunction(id=>!document.querySelector(`button[data-id="${id}"][data-choice="retry"]`),ID,{timeout:8000});
  if(shots)await page.screenshot({path:`${shots}/5-closed-${w}x${h}.png`});
  const text=await page.locator('body').innerText();
  assert.ok(!/available only for a blocked preparation/.test(text));
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('signin resume dashboard ok');
}finally{await browser?.close();server.close()}
