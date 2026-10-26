import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The sign-in dialog says which one-time code the page wants (a text message, an authenticator app, an email, or
// "the code it asks for"), quotes the site's own sentence, offers the page's own "another way" links as buttons and
// keeps the dialog open with the site's words when a code is rejected. All mocked; made-up values only.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const SHOTS=process.env.SIGNIN_SHOTS||'';
const base={id:'0:tab',host:'dashboard.stripe.com',site:'dashboard.stripe.com',brand:'Stripe',secure:true,title:'Verify',username:false,password:false,code:true,error:'',saved:null};
const PAGES={
 sms:{...base,code_kind:'sms',sent_to:'ending in 12',ask:'Two-step authentication · Enter the code we sent to •••• 12.',others:['Resend code','Use authenticator app instead']},
 app:{...base,code_kind:'app',sent_to:'',ask:'Enter the 6-digit code from your authenticator app',others:['Text me a code instead']},
 email:{...base,code_kind:'email',sent_to:'j•••@example.com',ask:'Check your email · We emailed a code to j•••@example.com.',others:[]},
 unknown:{...base,code_kind:'unknown',sent_to:'',ask:'Enter your verification code to continue.',others:[]},
};
let shown='sms';const posts=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='browser_login_pages'){res.end(JSON.stringify({pages:[PAGES[shown]]}));return}
  if(action==='browser_login_choose'){shown='app';res.end(JSON.stringify({result:'next',page:PAGES.app}));return}
  if(action==='browser_login_fill'){res.end(JSON.stringify({result:'still_here',page:{...PAGES.app,error:'That code isn’t right. Try again.'}}));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin='http://127.0.0.1:'+server.address().port,errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1280]){
  const context=await browser.newContext({viewport:{width,height:width<500?844:900}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  for(const kind of ['sms','app','email','unknown']){
   shown=kind;await page.goto(origin+'/?v='+kind+width+'#signin');const d=page.locator('#signin-dialog');await d.waitFor({state:'visible'});await page.locator('#signin-code').waitFor({state:'visible'});
   const title=await page.locator('#signin-title').textContent(),help=await page.locator('#signin-code-help').textContent(),ask=await page.locator('#signin-code-ask').textContent();
   assert.equal(title,{sms:'Stripe sent a code by text message',app:'Code from your authenticator app',email:'Code from your email',unknown:'Enter the code dashboard.stripe.com asks for'}[kind]);
   if(kind==='sms')assert.equal(help,'To your phone ending in 12 (as Stripe shows it).');
   if(kind==='email')assert.equal(help,'Sent to j•••@example.com (as Stripe shows it).');
   if(kind==='unknown')assert.ok(await page.locator('#signin-code-help').isHidden());
   assert.equal(ask,`Stripe says: “${PAGES[kind].ask}”`);
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   if(SHOTS)await page.screenshot({path:`${SHOTS}/signin-code-${kind}-${width}.png`});
  }
  // Another method: the page's own link, clicked in the page; the dialog then asks for that code.
  shown='sms';await page.goto(origin+'/?v=other'+width+'#signin');await page.locator('#signin-others button').first().waitFor();
  assert.deepEqual(await page.locator('#signin-others button').allTextContents(),['Resend code','Use authenticator app instead']);
  await page.getByRole('button',{name:'Use authenticator app instead'}).click();
  await page.locator('#signin-title',{hasText:'Code from your authenticator app'}).waitFor();
  assert.deepEqual(posts.at(-1),{action:'browser_login_choose',args:{page:'0:tab',host:'dashboard.stripe.com',option:'Use authenticator app instead'}});
  // A rejected code: the site's own words, the dialog stays open and the code field empty.
  await page.locator('#signin-code').fill('000000');await page.locator('#signin-go').click();
  await page.locator('#signin-error',{hasText:'Stripe says: “That code isn’t right. Try again.”'}).waitFor();
  assert.ok(await page.locator('#signin-dialog').isVisible());assert.equal(await page.locator('#signin-code').inputValue(),'');
  if(SHOTS)await page.screenshot({path:`${SHOTS}/signin-code-rejected-${width}.png`});
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('signin code dashboard ok');
}finally{await browser?.close();server.close()}
