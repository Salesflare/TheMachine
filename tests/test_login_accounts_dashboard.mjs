import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
import {callAfter} from './page-calls.mjs';
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
 {id:'c3c3c3c3c3c3c3c3',site:'portal.example.com',origin:'https://portal.example.com',account:'Default',username:'test-user',saved_at:'2025-12-01T09:00:00+00:00',password_saved:true},
 {id:'d4d4d4d4d4d4d4d4',site:'sso.northwind.example',origin:'https://sso.northwind.example',account:'Work',username:'',saved_at:'2026-01-20T09:00:00+00:00',password_saved:true},
 {id:'e5e5e5e5e5e5e5e5',site:'webmail.example.org',origin:'https://webmail.example.org',account:'Personal',username:'sam.home@example.org',saved_at:'2025-11-02T09:00:00+00:00',password_saved:false}];
const review={token:'tok-1',kind:'1password',manager:'1Password',skipped:1,rows:[
 {key:'k1',title:'Tidewell',site:'shop.tidewell.example',origin:'https://shop.tidewell.example',username:'sam@acme.example',saved:['Work']},
 {key:'k2',title:'Example',site:'billing.example.net',origin:'https://billing.example.net',username:'finance@example.net',saved:[]},
 {key:'k3',title:'Router',site:'portal.example.com',origin:'https://portal.example.com',username:'admin',saved:[]}]};
const accounts=logins.slice(0,2).map(({id,account,username})=>({id,account,username}));
let pick=null,twoStep=false,tools={},exportReady=false,browserLink=null;const calls=[];
const tidewell={id:'0:tab',site:'shop.tidewell.example',host:'shop.tidewell.example',origin:'https://shop.tidewell.example',code:false};
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('.png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 // the Machine's browser in the live view: a made-up page, never a real password manager's
 if(url.pathname==='/view/'){res.setHeader('Content-Type','text/html');res.end('<body style="margin:0;background:#1f2329;color:#ddd;font:16px sans-serif;display:grid;place-items:center;height:100vh">Example vault: Export</body>');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({...(browserLink?{browser_link:browserLink}:{}),suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[]}));return}
 if(url.pathname==='/api/progress'){res.end(JSON.stringify({status:'blocked'}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);calls.push([action,args]);
  if(action==='browser_logins'){res.end(JSON.stringify({logins}));return}
  if(action==='browser_login_rename'){const l=logins.find(x=>x.id===args.id);l.account=args.account;res.end(JSON.stringify({renamed:true}));return}
  if(action==='browser_login_import'){
   if(args.do==='tools'){res.end(JSON.stringify({tools}));return}
   if(args.do==='export'){res.end(JSON.stringify({watch:'w-1',view:null,page:'https://vault.example.invalid/export'}));return}
   if(args.do==='export_check'){res.end(JSON.stringify(exportReady?{...review,manager:'LastPass',state:'review'}:{state:'waiting'}));return}
   if(args.do==='file'||args.do==='tool'){res.end(JSON.stringify(review));return}
   if(args.do==='keep'){res.end(JSON.stringify({kept:args.keys.length}));return}
   res.end(JSON.stringify({dropped:true}));return}
  if(action==='browser_login_open'){res.end(JSON.stringify({site:'shop.tidewell.example',kind:'password'}));return}
  if(action==='browser_login_pages'&&twoStep){res.end(JSON.stringify({pages:[{...tidewell,username:true,password:false,accounts:[],pick:null,side:'Work'}],walls:[]}));return}
  if(action==='browser_login_fill'&&twoStep&&args.username){res.end(JSON.stringify({result:'next',page:{...tidewell,username:false,password:true}}));return}
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
  await page.goto(base+'/#connections=signins');await page.locator('#saved-logins .saved-login').nth(3).waitFor();
  // one row per site; its accounts underneath; a short host is never cut short
  assert.equal(await page.locator('#saved-logins .saved-login').count(),4);
  const shop=page.locator('#saved-logins .saved-login.many');
  assert.deepEqual(await shop.locator('.login-acct .login-user').allTextContents(),['sam@home.example','sam@acme.example']);
  assert.equal(await shop.locator('.login-acct button').count(),2);
  assert.ok(await page.locator('#saved-logins strong').evaluateAll(s=>s.every(x=>x.scrollWidth<=x.clientWidth)),'a site name is never cut short');
  if(width===390)assert.ok(await shop.locator('.login-user').evaluateAll(us=>us.every(u=>u.scrollWidth<=u.clientWidth)),'both accounts fit a phone row');
  // every account says which one it is: its username, or that none is saved; never a line that starts with a separator
  const text=await page.locator('#saved-logins').innerText();
  assert.match(text,/No username saved/);
  assert.ok(!/(^|\n)\s*·/.test(text),'no dangling separator: '+text);
  // every account's side is a menu that stays changeable; Default reads as a question; a name the site's other
  // account has is greyed out
  const sides=page.locator('#saved-logins [data-login-side]');
  assert.equal(await sides.count(),5);
  assert.deepEqual(await sides.evaluateAll(s=>s.map(x=>x.value)),['Personal','Work','Default','Work','Personal']);
  assert.deepEqual(await page.locator('[data-login-side="c3c3c3c3c3c3c3c3"] option').allInnerTexts(),['Work or personal?','Work','Personal']);
  assert.deepEqual(await page.locator('[data-login-side="a1a1a1a1a1a1a1a1"] option[disabled]').allInnerTexts(),['Work']);
  // the password line sits under the menu, never cut short and never past the row
  for(const m of await page.locator('#saved-logins .login-meta').all()){
   const [cut,right,row]=await m.evaluate(x=>{const p=x.querySelector('.login-pass span');return [p.scrollWidth>p.clientWidth,p.getBoundingClientRect().right,x.closest('.saved-login').getBoundingClientRect().right]});
   assert.ok(!cut&&right<=row,'the password line is whole: '+JSON.stringify([cut,right,row]))}
  await clean(page,'list');
  await page.evaluate(()=>scrollTo(0,Math.max(0,document.querySelector('#health-tabs').getBoundingClientRect().top+scrollY-24)));
  await shot(page,'signins-accounts',width,scheme);
  // the open menu: a native one isn't in a screenshot, so for the shot only it shows as a list box
  if(shots){const l=page.locator('[data-login-side="d4d4d4d4d4d4d4d4"]');await l.evaluate(s=>{s.size=3;s.style.position='relative';s.style.zIndex=2});
   await shot(page,'signins-menu',width,scheme);await l.evaluate(s=>{s.size=0;s.style.cssText=''})}
  // Default gets a side, and a side set before changes again (a wrong mark is undone), back to not set too
  for(const [id,to,i] of [['c3c3c3c3c3c3c3c3','Personal',2],['d4d4d4d4d4d4d4d4','Personal',3],['d4d4d4d4d4d4d4d4','Default',3]]){calls.length=0;
   await page.locator(`[data-login-side="${id}"]`).selectOption(to);
   await page.waitForFunction(([id,to])=>{const s=document.querySelector(`[data-login-side="${id}"]`);return s&&!s.disabled&&s.value===to},[id,to]);
   assert.deepEqual(calls.find(([a])=>a==='browser_login_rename')[1],{id,account:to});assert.equal(logins[i].account,to)}
  logins[2].account='Default';logins[3].account='Work';
  // Import: where from. Every option leads somewhere: 1Password's op signed in on the Machine, the rest export in
  // the Machine's browser; nothing greyed out.
  calls.length=0;tools={'1password':'ready',lastpass:'missing'};exportReady=false;
  await page.locator('#logins-import').click();
  await page.locator('#login-import [data-li-go="1password"]',{hasText:'Signed in on this Machine'}).waitFor();
  assert.deepEqual(await page.locator('#login-import [data-li-go]').evaluateAll(bs=>bs.map(b=>b.dataset.liGo)),['lastpass','1password','bitwarden','chrome']);
  assert.equal(await page.locator('#login-import [data-li-go][disabled]').count(),0,'no dead ends');
  assert.match(await page.locator('[data-li-go="lastpass"]').innerText(),/Export in your Machine’s browser/);
  assert.ok(!/this computer/.test(await page.locator('#login-import').innerText()),'the Machine, not "this computer"');
  await clean(page,'import');await shot(page,'import-from',width,scheme);
  // LastPass: its export page opens in the Machine's browser, the steps say what to do there, and the file it
  // downloads comes back as the review
  await page.locator('[data-li-go="lastpass"]').click();
  await page.locator('#login-import .li-wait').waitFor();
  assert.deepEqual(calls.find(([a,x])=>a==='browser_login_import'&&x.do==='export')[1],{do:'export',manager:'lastpass'});
  assert.match(await page.locator('#login-import').innerText(),/Export from LastPass[\s\S]*Open Advanced Options, then Export\.[\s\S]*Waiting for the export file…/);
  assert.equal(await page.locator('#login-import [data-li-browser].primary').count(),1,'no live view here: Open the browser leads');
  await clean(page,'export');await shot(page,'import-export',width,scheme);
  exportReady=true;
  await page.locator('#login-import [data-li-key]').nth(2).waitFor();
  assert.match(await page.locator('#login-import .li-lead').innerText(),/3 sign-ins found in LastPass\./);
  await page.locator('#login-import [data-li-back]').click();
  // With the live view on this address, the export page shows right in the sheet
  browserLink='/view/';exportReady=false;await page.evaluate(async()=>{await refresh()});
  await page.locator('[data-li-go="bitwarden"]').click();
  await page.locator('#login-import .li-view iframe').waitFor();
  await page.frameLocator('#login-import .li-view iframe').locator('body').waitFor();
  await clean(page,'export view');await shot(page,'import-export-view',width,scheme);
  // Back sends the stop without waiting on its answer: wait for that call to be answered, not a fixed time
  const stop=await callAfter(page,c=>c.action==='browser_login_import'&&c.args?.do==='export_stop',()=>page.locator('#login-import [data-li-back]').click());
  assert.deepEqual(stop.args,{do:'export_stop',watch:'w-1'},'Back stops the export');
  browserLink=null;await page.evaluate(async()=>{await refresh()});
  // 1Password without op: its app's export file, picked right there
  tools={};await page.locator('[data-li-close]').click();await page.locator('#logins-import').click();
  await page.locator('#login-import [data-li-go="1password"]',{hasText:'Export from the 1Password app'}).waitFor();
  await page.locator('[data-li-go="1password"]').click();
  await page.locator('#login-import .li-steps').waitFor();
  assert.match(await page.locator('#login-import').innerText(),/In the 1Password app on a computer, choose File, then Export\./);
  await clean(page,'1password app');await shot(page,'import-1password',width,scheme);
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
  // A two-step sign-in: the username on its own page, then the password. Save for next time at the password step
  // keeps the username typed before (save_username), and never types it into the page again.
  twoStep=true;calls.length=0;
  await page.goto('about:blank');await page.goto(base+'/#signin-for='+TASK);
  await page.locator('#signin-user-row:not([hidden])').waitFor();
  await page.locator('#signin-user').fill('sam@acme.example');await page.locator('#signin-go').click();
  await page.locator('#signin-pass-row:not([hidden])').waitFor();
  assert.ok(await page.locator('#signin-user-row').isHidden());
  await page.locator('#signin-save').check();await page.locator('#signin-pass').fill('two-step-pass');await page.locator('#signin-go').click();
  await page.waitForFunction(()=>!document.querySelector('#signin-go').disabled);
  const [first,second]=calls.filter(([a])=>a==='browser_login_fill').map(([,x])=>x);
  assert.equal(first.username,'sam@acme.example');
  assert.deepEqual([second.username,second.save_username,second.save,second.password],[undefined,'sam@acme.example',true,'two-step-pass']);
  twoStep=false;
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('login accounts dashboard ok');
}finally{await browser?.close();server.close()}
