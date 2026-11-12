import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Settings, Account: the first tab on a Machine linked to a control plane account. Hosted, the control plane answers on
// the dashboard's own host (/_machine/account, the owner's sign-in there) and each button is a POST to
// /_machine/account-hop in this same tab, which opens that part of the account signed in, as a focused step that leads
// back here (a hosted Machine has no account dashboard besides this tab). Self-hosted and paired, this
// Machine asks (api/account) and the buttons are links. Sign out stays (hosted). Not linked: no Account tab, and General
// keeps "Join the Network". Self-hosted and paired, Unpair this Machine is the first quiet way out (ai_unpair; it was a
// section of its own in Settings, Apps). Made-up data only. Set SHOTS=<dir> for screenshots.
const dashboard=await dashboardPage();
const hours={days:[0,1,2,3,4],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC'};
const CP='https://account.example';
const hostedSummary={email:'alex@example.org',hop:true,
 plan:{name:'Standard',price:'€10 a month, excl. VAT, early adopter price (was €25)',status:'active',status_text:'Active',trial_end:null,cancel_at:null},
 next_invoice:{date:'2026-11-20',amount:'€10, excl. VAT'},
 server:{size:'4 GB memory',region:'Europe, the Netherlands',status:'Running'},
 connections:[{service:'Google',email:'alex@example.org'},{service:'Microsoft',email:'alex@work.example'}],
 fleets:[{name:'Example Co',kind:'work',role:'owner',people:4,seats:3}],
 actions:['account','fleet','plan','portal','cancel','connections','overview','username','security','data','delete','support','friends'],
 name:'alex.themachine.example',security:{recovery:9,passkeys:2,phones:1},friends:{on:true,waiting:1},export:{ready:false,until:null},
 links:{account:CP+'/account',fleet:CP+'/account?tab=fleet',plan:CP+'/account?tab=overview#status',portal:CP+'/account?tab=billing',cancel:CP+'/account/cancel',connections:CP+'/setup#sources'}};
const APP='https://app.themachine.computer';
const pairedSummary={on:true,email:'sam@example.org',hop:false,plan:null,next_invoice:null,server:null,connections:[],
 fleets:[{name:'Family',kind:'family',role:'member',people:3}],actions:['account','fleet','security','friends','delete','network'],
 security:{recovery:10,passkeys:1,phones:0},friends:{on:true,waiting:2},username:'sam-k',
 network:{on:true,status:'active',until:null,price:'€4/month, excl. VAT'},
 links:{account:APP+'/account',fleet:APP+'/account?tab=fleet&focus=1',security:APP+'/account?tab=security&focus=1',
  friends:APP+'/account?tab=friends&focus=1',delete:APP+'/account?tab=data&focus=1#wipe',network:APP+'/account?tab=billing&focus=1#network-sub'}};
let mode='hosted',fail=false;const hops=[],posts=[],asked=[],actions=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/_machine/logout'){posts.push(req.method);res.writeHead(303,{Location:'/bye'});res.end();return}
 if(url.pathname==='/_machine/account-hop'){let body='';for await(const c of req)body+=c;hops.push([req.method,body]);res.setHeader('Content-Type','text/html');res.end('<p>Account page</p>');return}
 if(url.pathname.startsWith('/brand/')){res.setHeader('Content-Type','image/png');res.end(await readFile(new URL('../brand/app-icon-192.png',import.meta.url)));return}  // as the app serves them (assistant.BRAND_ASSETS)
 if(url.pathname==='/bye'){res.setHeader('Content-Type','text/html');res.end('<p>Signed out</p>');return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/_machine/account'){asked.push('cp');if(fail){res.writeHead(401);res.end('{"error":"signed out"}');return}res.end(JSON.stringify(hostedSummary));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action}=JSON.parse(body);actions.push(action);
  if(action==='ai_unpair')mode='none';res.end(JSON.stringify({connections:[],areas:['work'],reach:{hosted:false,paired:false}}));return}
 if(url.pathname==='/api/account'){asked.push('machine');res.end(JSON.stringify(mode==='paired'?pairedSummary:{on:false}));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],hours,
  skills:{skills:[],waiting:0,targets:[],folder:'skills/the-machine'},model_usage:[],model_status:{model:'openai/example-model',provider:'openai',windows:[],checked_at:new Date().toISOString()},
  signatures:[{account_id:'mail',email:'alex@example.org',service:'gmail',html:'<b>Alex</b>',source:'detected',saveable:true}],
  ...(mode==='hosted'?{manage_url:CP+'/setup',account_url:CP+'/account'}:{}),...(mode==='paired'?{fleet:{on:true,waiting:0},account_url:'https://app.themachine.computer/account'}:{})}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const text=(page,sel)=>page.locator(sel).innerText();
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440])for(const scheme of ['light','dark']){
  mode='hosted';fail=false;
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
  await navClick(page.locator('#open-settings'));await page.locator('#acct-list [data-acct-go="plan"]').waitFor();
  // A normal tab, the first one, and open by default
  assert.deepEqual((await page.locator('#settings-tabs>:not([hidden])').allInnerTexts())[0],'Account');
  assert.equal(await page.locator('#settings-tabs [aria-selected="true"]').innerText(),'Account');
  assert.equal(await page.locator('#settings-tabs a').count(),0);  // no link out any more
  assert.equal(await text(page,'#acct-email'),'alex@example.org');
  const list=await text(page,'#acct-list');
  for(const bit of ['Standard','Active','€10 a month, excl. VAT, early adopter price (was €25)','Next invoice','Fri, Nov 20','€10, excl. VAT','4 GB memory · Europe, the Netherlands','Google: alex@example.org','Microsoft: alex@work.example','Example Co','Owner · 4 people · 3 seats',
   'alex.themachine.example','1 friend request waiting','Two-factor on · 9 recovery codes left · 2 passkeys · 1 phone signed in','Export everything to run it on your own computer.'])
   assert.ok(list.includes(bit),bit);
  assert.ok(!/—/.test(list));
  // Every part of the account is here, each change a POST to the hop in this same tab (a focused step that comes back);
  // no Open account: there is no account dashboard to open. Sign out stays
  const forms=await page.locator(':is(#settings-acct,#settings-acct-end) form[action="/_machine/account-hop"]').evaluateAll(fs=>fs.map(f=>[f.method,f.target,f.querySelector('[name=to]').value]));
  assert.deepEqual(forms.map(f=>f[2]).sort(),['cancel','connections','data','delete','fleet','friends','overview','plan','portal','security','username']);
  assert.ok(forms.every(f=>f[0]==='post'&&f[1]===''));
  assert.equal(await page.locator('#settings-acct [data-acct-go="account"]').count(),0);
  assert.equal(await page.locator('#settings-acct form[action="/_machine/logout"]').count(),1);
  // Sign out at the account's head; Cancel and Delete are quiet text links at the very end of the tab, after Your
  // addresses: easy to find, not equal-weight buttons. Reporting a problem is Help's, not here
  assert.equal(await page.locator('#acct-out form[action="/_machine/logout"]').count(),1);
  assert.equal(await page.locator('#acct-danger .acct-quiet[data-acct-go="cancel"]').count(),1);
  assert.equal(await page.locator('#acct-danger .acct-quiet[data-acct-go="delete"]').count(),1);
  assert.equal(await page.locator('#settings [data-acct-unpair]').count(),0);  // a hosted Machine stays on the account
  assert.equal(await page.locator('#settings-acct-end').isVisible(),true);
  assert.equal(await page.evaluate(()=>[...document.querySelectorAll('#settings>:not([hidden])')].filter(x=>x.dataset.stab==='account').at(-1).id),'settings-acct-end');
  assert.equal(await page.locator('#settings [data-acct-report]').count(),0);
  // No Security tab here: this Machine sends no security levels, and support access shows only while it's on
  assert.deepEqual((await page.locator('#settings-tabs>:not([hidden])').allInnerTexts()),['Account','General','Activity','Notifications','Writing','Skills','Apps','Model']);
  assert.equal(await page.locator('#settings-account-block').isHidden(),true);  // General no longer says "on your account page"
  const fits=await page.evaluate(()=>{const r=document.querySelector('#acct-list').getBoundingClientRect();
   return document.documentElement.scrollWidth<=innerWidth&&[...document.querySelectorAll(':is(#settings-acct,#settings-acct-end) :is(button,a)')].every(b=>{const x=b.getBoundingClientRect();return x.right<=innerWidth&&x.left>=0})});
  assert.equal(fits,true);
  if(process.env.SHOTS)await page.screenshot({path:`${process.env.SHOTS}/account-hosted-${width}-${scheme}.png`,fullPage:true});
  if(width===390&&scheme==='light'){
   await Promise.all([page.waitForURL(base+'/_machine/account-hop'),page.locator('#acct-list [data-acct-go="portal"]').click()]);
   assert.equal(hops.at(-1)[0],'POST');assert.equal(hops.at(-1)[1],'to=portal');
   await page.goto(base);await navClick(page.locator('#open-settings'));await page.locator('#acct-list [data-acct-go="plan"]').waitFor();
   // Read once a minute, not on every look
   const before=asked.length;await page.locator('#settings-tabs [data-settings-tab="general"]').click();await page.locator('#settings-tabs [data-settings-tab="account"]').click();
   assert.equal(asked.length,before);
   await page.locator('#settings-acct form[action="/_machine/logout"] button').click();await page.waitForURL(base+'/bye');assert.deepEqual(posts,['POST']);
   // Signed out at the control plane: a short note and the account link, nothing broken
   fail=true;await page.goto(base);await navClick(page.locator('#open-settings'));await page.locator('#acct-list',{hasText:'Can’t reach your account'}).waitFor();
   assert.equal(await page.locator('#acct-foot a[href="https://account.example/account"]').count(),0);  // no account dashboard to send them to
   // Self-hosted and paired: this Machine asks, links instead of hops, no Sign out
   mode='paired';fail=false;await page.goto('about:blank');await page.goto(base+'/#settings/account');await page.locator('#acct-list',{hasText:'Family'}).waitFor();
   assert.equal(asked.at(-1),'machine');
   assert.equal(await page.locator(':is(#settings-acct,#settings-acct-end) form[action="/_machine/account-hop"]').count(),0);
   // The account's own parts too (counts only), each a link to that part of the account, a focused step there
   assert.deepEqual(await page.locator('#settings-acct a[data-acct-go]').evaluateAll(as=>as.map(a=>[a.dataset.acctGo,a.getAttribute('href'),a.target])),
    [['network',APP+'/account?tab=billing&focus=1#network-sub','_blank'],['fleet',APP+'/account?tab=fleet&focus=1','_blank'],['friends',APP+'/account?tab=friends&focus=1','_blank'],
     ['security',APP+'/account?tab=security&focus=1','_blank'],['account',APP+'/account','_blank']]);
   // Network for Friends (an older paid one): its state in short; stopping it and the card are on the account's Billing part
   assert.ok((await text(page,'#acct-list')).includes('Network for Friends\n€4/month, excl. VAT · The Network is free now, so you can stop this'));
   pairedSummary.network={on:true,status:'past_due',until:'2026-11-30',price:'€4/month, excl. VAT'};
   await page.goto('about:blank');await page.goto(base+'/#settings/account');await page.locator('#acct-list',{hasText:'Stops on'}).waitFor();
   assert.ok((await text(page,'#acct-list')).includes('Payment is being retried · Stops on Mon, Nov 30'));
   pairedSummary.network={on:true,status:'active',until:null,price:'€4/month, excl. VAT'};
   assert.equal(await page.locator('#settings-acct form[action="/_machine/logout"]').count(),0);
   const paired=await text(page,'#acct-list');
   for(const bit of ['Member · 3 people','Username','sam-k','2 friend requests waiting','Two-factor on · 10 recovery codes left · 1 passkey'])
    assert.ok(paired.includes(bit),bit);
   assert.ok(!/Address|Your data|phone signed in/.test(paired));
   // Delete account is the quiet way out at the very end, a link too (the Machine on this computer stays)
   assert.deepEqual(await page.locator('#acct-danger a[data-acct-go]').evaluateAll(as=>as.map(a=>[a.dataset.acctGo,a.getAttribute('href'),a.target])),
    [['delete',APP+'/account?tab=data&focus=1#wipe','_blank']]);
   // Unpair this Machine: the first quiet way out, a button here (it works without the account); asks first, then the
   // Machine is off the account and General offers Join the Network again
   assert.deepEqual(await page.locator('#acct-danger>*').evaluateAll(xs=>xs.map(x=>x.dataset.acctUnpair!==undefined?'unpair':x.dataset.acctGo)),['unpair','delete']);
   const unpair=page.locator('#acct-danger button.acct-quiet[data-acct-unpair]');assert.equal(await unpair.innerText(),'Unpair this Machine');
   page.once('dialog',d=>d.dismiss());await unpair.click();await page.waitForTimeout(100);assert.ok(!actions.includes('ai_unpair'),'nothing without OK');
   page.once('dialog',d=>{assert.match(d.message(),/^Unpair this Machine\?/);d.accept()});await unpair.click();
   await page.locator('#settings-cloud:not([hidden])',{hasText:'Join the Network'}).waitFor();assert.deepEqual(actions.filter(a=>a==='ai_unpair'),['ai_unpair']);
   // Not linked: no Account tab; General keeps the Network card
   mode='none';await page.goto('about:blank');await page.goto(base+'/#settings');await page.locator('#settings-cloud:not([hidden])').waitFor();
   assert.equal(await page.locator('#settings-tabs [data-settings-tab="account"]').isHidden(),true);
   assert.equal(await page.locator('#settings-tabs [aria-selected="true"]').innerText(),'General');
  }
  // Self-hosted and paired, at every size: Unpair this Machine fits next to Delete account
  mode='paired';await page.goto('about:blank');await page.goto(base+'/#settings/account');await page.locator('#acct-danger [data-acct-unpair]').waitFor();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth&&[...document.querySelectorAll('#acct-danger>*')].every(b=>{const x=b.getBoundingClientRect();return x.right<=innerWidth&&x.left>=0})),`${width}: fits`);
  if(process.env.SHOTS)await page.screenshot({path:`${process.env.SHOTS}/account-paired-${width}-${scheme}.png`,fullPage:true});
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('account dashboard ok');
}finally{await browser?.close();server.close()}
