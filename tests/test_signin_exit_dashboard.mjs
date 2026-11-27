import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A listed site's sign-in while the owner's desktop app (with browsing through it on) is away (machine/browser_exit.py):
// the dialog asks to open it (Open the app: the desktop app's own link, never clicked here), with a quiet Sign in
// without it (a short sheet on a phone); once the app connects it turns into the sign-in by itself. Without `exit` in the answer (no desktop app, or it's off) the form shows as today. All mocked.
const dashboard=await dashboardPage();
const SHOTS=process.env.SIGNIN_SHOTS||'';
const LOGIN={id:'0:tab',host:'www.linkedin.com',site:'linkedin.com',brand:'LinkedIn',secure:true,error:'',saved:null,title:'LinkedIn Login',username:true,password:true,code:false};
let away='LinkedIn';const posts=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='browser_login_pages'){res.end(JSON.stringify({pages:[LOGIN],walls:[],...(away?{exit:away}:{})}));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin='http://127.0.0.1:'+server.address().port,errors=[];let browser;
const shot=async(page,name,width,scheme)=>{if(SHOTS)await page.screenshot({path:`${SHOTS}/exit-${name}-${width}-${scheme}.png`})};
const ASK='So LinkedIn sees you signing in from home, not from a server.',TITLE='Sign in to LinkedIn on your Machine';
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,scheme] of [[1440,'light'],[390,'light'],[1440,'dark'],[390,'dark']]){
  const context=await browser.newContext({viewport:{width,height:width<500?844:900},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.clock.install();
  // Away: the notice, and no form, until the owner picks the Machine.
  away='LinkedIn';
  await page.goto(origin+'/?v='+width+scheme+'#signin-site=linkedin');
  await page.locator('#signin-status-text',{hasText:ASK}).waitFor();
  assert.ok(await page.locator('#signin-direct').isVisible());
  assert.equal(await page.locator('#signin-direct').textContent(),'Sign in without it');
  assert.equal(await page.locator('#signin-direct').getAttribute('class'),'ghost');
  assert.ok(await page.locator('#signin-app').isVisible());
  assert.equal(await page.locator('#signin-app').textContent(),'Open the app');
  assert.equal(await page.locator('#signin-app').getAttribute('class'),'primary');
  assert.equal(await page.evaluate(()=>SIGNIN_APP),'computer.themachine.desktop://open');
  assert.ok((await page.locator('#signin-status-text').textContent()).endsWith('It goes on by itself once the app is open.'));
  assert.equal(await page.locator('#signin-title').textContent(),'Open The Machine on your computer');
  assert.ok(await page.locator('#signin-fine').isHidden());
  assert.ok(await page.locator('#signin-user').isHidden());
  assert.ok(await page.locator('#signin-browser').isHidden());
  await page.clock.runFor(30000);  // it keeps asking, it doesn't give up
  assert.ok(await page.locator('#signin-direct').isVisible());
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  const box=await page.locator('#signin-dialog').boundingBox();  // a phone gets a short sheet at the bottom
  if(width<500)assert.ok(box.height<400&&Math.abs(box.y+box.height-844)<2,JSON.stringify(box));
  await shot(page,'away',width,scheme);
  await page.locator('#signin-direct').click();
  await page.clock.runFor(3000);
  await page.locator('#signin-user').waitFor({state:'visible'});
  assert.ok(await page.locator('#signin-direct').isHidden());
  assert.ok(await page.locator('#signin-app').isHidden());
  assert.equal(await page.locator('#signin-title').textContent(),TITLE);
  // Away, then the app connects: the form shows by itself.
  await page.locator('#signin-dialog button[aria-label="Close sign-in"]').click();
  away='LinkedIn';
  await page.goto(origin+'/?again='+width+scheme+'#signin-site=linkedin');
  await page.locator('#signin-status-text',{hasText:ASK}).waitFor();
  away='';await page.clock.runFor(3000);
  await page.locator('#signin-user').waitFor({state:'visible'});
  assert.ok(await page.locator('#signin-direct').isHidden());
  assert.equal(await page.locator('#signin-title').textContent(),TITLE);
  await context.close();
 }
 // A phone has no desktop app: no Open the app there, Sign in without it stays.
 {const context=await browser.newContext({viewport:{width:390,height:844},userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));away='LinkedIn';
  await page.goto(origin+'/?phone#signin-site=linkedin');
  await page.locator('#signin-status-text',{hasText:ASK}).waitFor();
  assert.ok(await page.locator('#signin-direct').isVisible());
  assert.ok(await page.locator('#signin-app').isHidden());
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('signin exit dashboard ok');
}finally{await browser?.close();server.close()}
