import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// LinkedIn's sign-in from a hosted setup page (#signin-site=linkedin): the password, then the code LinkedIn emails,
// with the code field left alone while the owner types; LinkedIn going back to the start says so with the form to try
// again; a robot check goes to the browser itself; an approval that never comes offers Try again, which starts
// LinkedIn's sign-in page afresh. All mocked; made-up values only.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const SHOTS=process.env.SIGNIN_SHOTS||'';
const base={id:'0:tab',host:'www.linkedin.com',site:'linkedin.com',brand:'LinkedIn',secure:true,error:'',saved:null};
const LOGIN={...base,title:'LinkedIn Login',username:true,password:true,code:false};
const PIN={...base,title:'Security Verification',username:false,password:false,code:true,code_kind:'email',sent_to:'j•••@example.com',
 ask:'Let’s do a quick security check · The verification code has been sent to j•••@example.com.',others:['Resend code']};
let next=[];const posts=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='browser_login_pages'&&args.watch){res.end(JSON.stringify({state:'waiting'}));return}
  if(action==='browser_login_pages'){res.end(JSON.stringify({pages:[LOGIN]}));return}
  if(action==='browser_login_fill'){res.end(JSON.stringify(next.shift()));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin='http://127.0.0.1:'+server.address().port,errors=[];let browser;
const shot=async(page,name,width,scheme)=>{if(SHOTS)await page.screenshot({path:`${SHOTS}/linkedin-${name}-${width}-${scheme}.png`})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,scheme] of [[1440,'light'],[390,'light'],[1440,'dark'],[390,'dark']]){
  const context=await browser.newContext({viewport:{width,height:width<500?844:900},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.clock.install();
  await page.goto(origin+'/?v='+width+scheme+'#signin-site=linkedin');
  await page.locator('#signin-user').waitFor({state:'visible'});
  assert.equal(await page.locator('#signin-title').textContent(),'Sign in to LinkedIn on your Machine');
  await shot(page,'password',width,scheme);
  // The password, then the code LinkedIn emailed.
  next=[{result:'next',page:PIN}];
  await page.locator('#signin-user').fill('someone@example.com');await page.locator('#signin-pass').fill('not-a-real-password');await page.locator('#signin-go').click();
  await page.locator('#signin-code').waitFor({state:'visible'});
  assert.equal(await page.locator('#signin-title').textContent(),'Code from your email');
  assert.equal(await page.locator('#signin-code-help').textContent(),'Sent to j•••@example.com (as LinkedIn shows it).');
  assert.equal(await page.locator('#signin-fine').textContent(),'This goes straight into the page in your Machine’s browser. The assistant never sees it. For anything else, open the browser.');
  // Typing the code: nothing in the dialog redraws or empties it while LinkedIn's email comes in.
  await page.locator('#signin-code').fill('42');await page.clock.runFor(65000);
  assert.equal(await page.locator('#signin-code').inputValue(),'42');
  assert.ok(await page.locator('#signin-code').evaluate(e=>document.activeElement===e));
  await page.locator('#signin-code').fill('424242');
  await shot(page,'code',width,scheme);
  // LinkedIn goes back to the start after the code: it stopped this sign-in. Said so, with the form to try again.
  next=[{result:'blocked',page:LOGIN}];await page.locator('#signin-go').click();
  await page.locator('#signin-error',{hasText:'LinkedIn went back to the start, so it stopped this sign-in. Wait a minute, then try again.'}).waitFor();
  assert.ok(await page.locator('#signin-pass').isVisible());
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await shot(page,'blocked',width,scheme);
  // A robot check after the password: the browser itself, never "approve it in your app".
  next=[{result:'captcha',page:{id:'0:tab',host:'www.linkedin.com',site:'linkedin.com'}}];
  await page.locator('#signin-pass').fill('not-a-real-password');await page.locator('#signin-go').click();
  await page.locator('#signin-status-text',{hasText:'LinkedIn wants a quick check that you’re not a robot.'}).waitFor();
  assert.ok(await page.locator('#signin-retry').isVisible());
  await shot(page,'captcha',width,scheme);
  // Approve in the app, and nothing comes: after two minutes, Try again, which opens LinkedIn's sign-in afresh.
  await page.locator('#signin-retry').click();await page.locator('#signin-user').waitFor({state:'visible'});
  next=[{result:'approve',page:{id:'0:tab',host:'www.linkedin.com',site:'linkedin.com'}}];
  await page.locator('#signin-user').fill('someone@example.com');await page.locator('#signin-pass').fill('not-a-real-password');await page.locator('#signin-go').click();
  await page.locator('#signin-status-text',{hasText:'Approve the sign-in in your LinkedIn app'}).waitFor();
  assert.ok(await page.locator('#signin-retry').isHidden());
  for(let i=0;i<45&&await page.locator('#signin-retry').isHidden();i++)await page.clock.runFor(3100);
  await page.locator('#signin-status-text',{hasText:'LinkedIn hasn’t moved on. If it stopped the sign-in, press Try again.'}).waitFor();
  assert.deepEqual([await page.locator('#signin-retry').getAttribute('class'),await page.locator('#signin-continue').getAttribute('class')],['primary','ghost']);
  await shot(page,'stalled',width,scheme);
  const before=posts.length;await page.locator('#signin-retry').click();await page.locator('#signin-user').waitFor({state:'visible'});
  assert.deepEqual(posts.slice(before).find(p=>p.action==='connect_site_signin'),{action:'connect_site_signin',args:{site:'linkedin',fresh:true}});
  // Nothing typed reaches anything but the sign-in itself.
  assert.ok(posts.every(p=>p.action==='browser_login_fill'||!JSON.stringify(p).includes('not-a-real-password')));
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('signin linkedin dashboard ok');
}finally{await browser?.close();server.close()}
