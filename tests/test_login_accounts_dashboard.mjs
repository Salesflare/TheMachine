import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Saved sign-ins with several accounts per site, Import from a password manager, and the sign-in dialog picking the
// to-do's account or asking once which one. Made-up sign-ins only; no password value ever reaches the page.
// SHOTS=<folder> saves 1440 and 390 shots, light and dark: the list, Import's two steps and the dialog.
const dashboard=await dashboardPage();
const LEAK='fixture-pass-9Kw4';
const TASK='0123456789abcdef';
const logins=[
 {id:'a1a1a1a1a1a1a1a1',site:'shop.tidewell.example',origin:'https://shop.tidewell.example',account:'Personal',username:'sam@home.example',saved_at:'2026-03-04T09:00:00+00:00',password_saved:true,password:LEAK},
 {id:'b2b2b2b2b2b2b2b2',site:'shop.tidewell.example',origin:'https://shop.tidewell.example',account:'Work',username:'sam@acme.example',saved_at:'2026-02-11T09:00:00+00:00',password_saved:true},
 {id:'c3c3c3c3c3c3c3c3',site:'portal.example.com',origin:'https://portal.example.com',account:'Default',username:'test-user',saved_at:'2025-12-01T09:00:00+00:00',password_saved:true}];
const review={token:'tok-1',kind:'1password',manager:'1Password',skipped:1,rows:[
 {key:'k1',title:'Tidewell',site:'shop.tidewell.example',origin:'https://shop.tidewell.example',username:'sam@acme.example',saved:['Work']},
 {key:'k2',title:'Example',site:'billing.example.net',origin:'https://billing.example.net',username:'finance@example.net',saved:[]},
 {key:'k3',title:'Router',site:'portal.example.com',origin:'https://portal.example.com',username:'admin',saved:[]}]};
const accounts=logins.slice(0,2).map(({id,account,username})=>({id,account,username}));
let pick=null;const calls=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('.png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[]}));return}
 if(url.pathname==='/api/progress'){res.end(JSON.stringify({status:'blocked'}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);calls.push([action,args]);
  if(action==='browser_logins'){res.end(JSON.stringify({logins}));return}
  if(action==='browser_login_rename'){const l=logins.find(x=>x.id===args.id);l.account=args.account;res.end(JSON.stringify({renamed:true}));return}
  if(action==='browser_login_import'){
   if(args.do==='tools'){res.end(JSON.stringify({tools:{'1password':'ready',lastpass:'missing'}}));return}
   if(args.do==='file'||args.do==='tool'){res.end(JSON.stringify(review));return}
   if(args.do==='keep'){res.end(JSON.stringify({kept:args.keys.length}));return}
   res.end(JSON.stringify({dropped:true}));return}
  if(action==='browser_login_open'){res.end(JSON.stringify({site:'shop.tidewell.example',kind:'password'}));return}
  if(action==='browser_login_pages'){res.end(JSON.stringify({pages:[{id:'0:tab',site:'shop.tidewell.example',host:'shop.tidewell.example',origin:'https://shop.tidewell.example',username:true,password:true,code:false,accounts,saved:{username:accounts[0].username},pick,side:'Work'}],walls:[]}));return}
  if(action==='browser_login_fill'){res.end(JSON.stringify({result:'next',page:{id:'0:tab',site:'shop.tidewell.example',host:'shop.tidewell.example',username:false,password:false,code:true}}));return}}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const csv='Title,Url,Username,Password,OTPAuth,Favorite,Archived,Tags,Notes\nTidewell,https://shop.tidewell.example,sam@acme.example,'+LEAK+',,false,false,,\n';
const clean=async(page,where)=>{const html=await page.content();assert.ok(!html.includes(LEAK),'no password value on the page: '+where);
 assert.ok(!/—/.test(await page.locator('body').innerText()),'no em dashes: '+where);
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll: '+where)};
const shot=async(page,name,width,scheme)=>{if(shots)await page.screenshot({path:`${shots}/${name}-${width}-${scheme}.png`})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,ignoreDefaultArgs:['--hide-scrollbars'],args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  // The list: one row per account, the account named where a site has several.
  await page.goto(base+'/#connections=signins');await page.locator('#saved-logins .saved-login').nth(1).waitFor();
  // one row per site; its accounts underneath, each labeled; a short host is never cut short
  assert.equal(await page.locator('#saved-logins .saved-login').count(),2);
  const shop=page.locator('#saved-logins .saved-login.many');
  assert.deepEqual((await shop.locator('.login-acct .login-user').allTextContents()).map(s=>s.replace(/\u00a0/g,' ')),['sam@home.example · Personal','sam@acme.example · Work']);
  assert.equal(await shop.locator('.login-acct button').count(),2);
  assert.ok(await page.locator('#saved-logins strong').evaluateAll(s=>s.every(x=>x.scrollWidth<=x.clientWidth)),'a site name is never cut short');
  // a sign-in moved over as Default: its side is set right there
  assert.deepEqual(await page.locator('#saved-logins [data-login-side] option').allInnerTexts(),['Default','Work','Personal']);
  await clean(page,'list');
  await page.evaluate(()=>scrollTo(0,Math.max(0,document.querySelector('#health-tabs').getBoundingClientRect().top+scrollY-24)));
  await shot(page,'signins-accounts',width,scheme);
  calls.length=0;await page.locator('#saved-logins [data-login-side]').selectOption('Personal');
  await page.locator('#saved-logins [data-login-side]').waitFor({state:'detached'});
  assert.deepEqual(calls.find(([a])=>a==='browser_login_rename')[1],{id:'c3c3c3c3c3c3c3c3',account:'Personal'});
  assert.match((await page.locator('#saved-logins').textContent()).replace(/\u00a0/g,' '),/test-user · Personal/);
  logins[2].account='Default';
  // Import: where from (1Password signed in, LastPass not installed), then the review.
  calls.length=0;
  await page.locator('#logins-import').click();
  await page.locator('#login-import [data-li-tool="lastpass"][disabled]').waitFor();
  assert.match(await page.locator('#login-import').innerText(),/Not installed on this computer/);
  assert.ok(await page.locator('#login-import [data-li-tool="1password"]:not([disabled])').count());
  await clean(page,'import');await shot(page,'import-from',width,scheme);
  await page.locator('#login-import [data-li-file]').setInputFiles({name:'export.csv',mimeType:'text/csv',buffer:Buffer.from(csv)});
  await page.locator('#login-import [data-li-key]').nth(2).waitFor();
  assert.match(await page.locator('#login-import .li-lead').innerText(),/3 sign-ins found in 1Password\. 1 without a secure web address left out\./);
  assert.equal(await page.locator('#login-import [data-li-keep]').innerText(),'Keep 3 sign-ins');
  await page.locator('#login-import [data-li-account]').selectOption('Work');
  assert.match(await page.locator('#login-import .li-row').first().innerText(),/Replaces the saved Work sign-in/);
  await page.locator('#login-import [data-li-key="k3"]').uncheck();
  assert.equal(await page.locator('#login-import [data-li-keep]').innerText(),'Keep 2 sign-ins');
  await clean(page,'review');await shot(page,'import-review',width,scheme);
  await page.locator('#login-import [data-li-keep]').click();
  await page.locator('#login-import').waitFor({state:'hidden'});
  const keep=calls.find(([a,x])=>a==='browser_login_import'&&x.do==='keep')[1];
  assert.deepEqual([keep.token,keep.keys,keep.account],['tok-1',['k1','k2'],'Work']);
  assert.match(await page.locator('#toast').innerText(),/Kept 2 sign-ins\./);
  // The sign-in dialog for a to-do: two accounts and none picked, so it asks once which one.
  pick=null;calls.length=0;
  await page.goto('about:blank');await page.goto(base+'/#signin-for='+TASK);
  await page.locator('#signin-saved button').nth(1).waitFor();
  assert.match(await page.locator('#signin-saved').innerText(),/Which account for this to-do\?/);
  assert.deepEqual(await page.locator('#signin-saved button').allInnerTexts(),['Sign in as sam@home.example · Personal','Sign in as sam@acme.example · Work']);
  assert.deepEqual(await page.locator('#signin-account option').allInnerTexts(),['Work','Personal','Other name…']);
  assert.equal(await page.locator('#signin-account').inputValue(),'Work','starts at the to-do’s own side');
  const sizes=await page.locator('#signin-saved button').evaluateAll(bs=>bs.map(b=>{const r=b.getBoundingClientRect();return [Math.round(r.left),Math.round(r.width),Math.round(r.height)].join()}));
  assert.equal(new Set(sizes).size,1,'the account buttons are one size: '+sizes.join(' / '));
  const formW=await page.locator('#signin-user').evaluate(e=>Math.round(e.getBoundingClientRect().width));
  assert.equal(Number(sizes[0].split(',')[1]),formW,'full width');
  await page.locator('#signin-account').selectOption('');
  assert.ok(await page.locator('#signin-account-name').isVisible(),'Other name… asks for one');
  await page.locator('#signin-account').selectOption('Work');
  await clean(page,'dialog');await shot(page,'signin-ask',width,scheme);
  await page.locator('#signin-saved button',{hasText:'Work'}).click();
  await page.locator('#signin-code-row:not([hidden])').waitFor();
  const fill=calls.find(([a])=>a==='browser_login_fill')[1];
  assert.deepEqual([fill.use_saved,fill.suggestion_id],['b2b2b2b2b2b2b2b2',TASK]);
  // Picked for this to-do: that one account, with Other account for the rest.
  pick='b2b2b2b2b2b2b2b2';
  await page.goto('about:blank');await page.goto(base+'/#signin-for='+TASK);
  await page.locator('#signin-saved button.primary').waitFor();
  assert.equal(await page.locator('#signin-saved button.primary').innerText(),'Sign in as sam@acme.example · Work');
  assert.ok(!/Which account/.test(await page.locator('#signin-saved').innerText()));
  await shot(page,'signin-picked',width,scheme);
  await page.locator('#signin-saved [data-login-other]').click();
  assert.equal(await page.locator('#signin-saved button').count(),2);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('login accounts dashboard ok');
}finally{await browser?.close();server.close()}
