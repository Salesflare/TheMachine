import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add on a hosted Machine: a sign-in started here comes back here (the control plane's /open to=connect)
// and the form says how it went: connected, or why the provider's answer was refused (#connect=<provider>/f_..., the
// reason asked from /_machine/connect-state, never read from the address). GitHub, WhatsApp and the phone sign in right
// here: their code shows in the form. Every provider's way back is followed, and Reconnect on a card or in Needs you
// opens the same form, never the account page. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const MANAGE='https://app.example.org/setup';
let states={},asked=[],posted=[],approved=[],connectors=[];
const PROVIDERS=['google','microsoft','microsoft_docs','zoom','stripe','intercom','github','whatsapp','android'];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],manage_url:MANAGE,connectors}));return}
 if(url.pathname==='/_machine/connect-qr'){res.setHeader('Content-Type','image/svg+xml');res.end('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 21 21"><rect width="21" height="21" fill="#fff"/><path d="M0 0h7v7H0zM14 0h7v7h-7zM0 14h7v7H0zM9 9h3v3H9z"/></svg>');return}
 if(url.pathname==='/_machine/connect-approve'){let body='';for await(const b of req)body+=b;approved.push(Object.fromEntries(new URLSearchParams(body)));res.end('{"ok":true}');return}
 if(url.pathname==='/_machine/connect'){let body='';for await(const b of req)body+=b;const form=Object.fromEntries(new URLSearchParams(body));posted.push(form);
  res.statusCode=303;res.setHeader('Location','/#connect='+form.source+'/c_00000000000000cc');res.end();return}
 if(url.pathname==='/_machine/connect-state'){const key=url.searchParams.get('s')+'/'+url.searchParams.get('c');asked.push(key);
  const next=states[key];if(!next){res.statusCode=404;res.end('{"error":"unknown"}');return}res.end(JSON.stringify(Array.isArray(next)?next.length>1?next.shift():next[0]:next));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:MANAGE,sources:[
   {name:'gmail',service:'gmail',label:'Gmail',connected:0,broker:true,hosted_signin:'google'},
   {name:'outlook',service:'outlook',label:'Outlook',connected:1,broker:true,hosted_signin:'microsoft'},
   {name:'docs',service:'docs',label:'Docs',connected:0,broker:false,account_page:'docs',hosted_signin:'microsoft_docs'},
   {name:'github',service:'github',label:'GitHub',what:'Review requests, mentions and failed CI runs.',connected:0,broker:false,hosted_signin:'github'},
   {name:'zoom',service:'zoom',label:'Zoom',what:'Your meetings.',connected:0,broker:true,hosted_signin:'zoom'},
   {name:'stripe',service:'stripe',label:'Stripe',what:'Payments.',connected:0,broker:false,hosted_signin:'stripe'},
   {name:'intercom',service:'intercom',label:'Intercom',connected:0,broker:false,account_page:'source-intercom',hosted_signin:'intercom'},
   {name:'whatsapp',service:'whatsapp',label:'WhatsApp',connected:0,broker:false,hosted_signin:'whatsapp'},
   {name:'android',service:'android',label:'Android phone',connected:0,broker:false,hosted_signin:'android'},
   {name:'slack',service:'slack',label:'Slack',connected:0,broker:false}]}));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const shot=async(page,name)=>{if(shots)await page.screenshot({path:`${shots}/${name}.png`})};
const box=page=>page.locator('#connect-add');
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // every size and theme for screenshots; a desktop and a phone otherwise (the waits are the form's own polling)
 const runs=shots?[['light',1440,900],['light',1440,700],['light',390,844],['dark',1440,900],['dark',390,844]]:[['light',1440,900],['dark',390,844]];
 for(const [scheme,width,height] of runs){const first=scheme==='light'&&width===1440&&height===900;
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}x${height}-${scheme}`;
  // Refused at the provider: the reason, asked from the account for this very form, and Try again
  states={'zoom/f_0123456789abcdef':{state:'failed',error:'Zoom did not accept the sign-in. Connect again.'}};asked=[];
  await page.goto(base+'/#connect=zoom/f_0123456789abcdef');
  await box(page).getByText('Zoom did not accept the sign-in. Connect again.').waitFor({timeout:8000});
  assert.equal(await box(page).locator('h3').innerText(),'Zoom');
  await box(page).getByRole('button',{name:'Try again'}).waitFor();
  assert.ok(asked.includes('zoom/f_0123456789abcdef'));
  assert.equal(new URL(page.url()).hash,'','the address is cleaned up');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`return-failed-${tag}`);
  // Connected: the short note, in the form it was started from
  states={'stripe/c_0123456789abcdef':[{state:'connecting'},{state:'done'}]};
  await page.goto('about:blank');await page.goto(base+'/#connect=stripe/c_0123456789abcdef');
  await box(page).getByText('Connected.').waitFor({timeout:10000});
  assert.equal(await box(page).locator('h3').innerText(),'Stripe');
  await shot(page,`return-connected-${tag}`);
  // Stopped at the provider
  await page.goto('about:blank');await page.goto(base+'/#connect=stripe/stopped');
  await box(page).getByText('That sign-in didn’t finish.').waitFor();
  // GitHub: started on the dashboard, its code right here
  states={'github/c_00000000000000aa':[{state:'starting'},{state:'code',code:'ABCD-1234',url:'https://github.com/login/device'},{state:'code',code:'ABCD-1234',url:'https://github.com/login/device'},
   {state:'connecting'},{state:'done'}]};
  await page.goto('about:blank');await page.goto(base+'/#connect=github/c_00000000000000aa');
  await box(page).getByText('ABCD-1234').waitFor({timeout:10000});
  const open=box(page).getByRole('link',{name:'Open GitHub ↗'});
  assert.equal(await open.getAttribute('href'),'https://github.com/login/device');
  assert.equal(await open.getAttribute('target'),'_blank');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`github-code-${tag}`);
  await box(page).getByText('Connected.').waitFor({timeout:15000});
  // A code with anything but GitHub's own device page: no link to it
  states={'github/c_00000000000000bb':{state:'code',code:'ABCD-1234',url:'https://evil.example/login/device'}};
  await page.goto('about:blank');await page.goto(base+'/#connect=github/c_00000000000000bb');
  await box(page).getByText('Signed in. Connecting it now.').waitFor({timeout:8000});
  assert.equal(await box(page).locator('a[href*="evil"]').count(),0);
  // Anything else in the address is not a sign-in to follow
  asked=[];
  for(const hash of ['#connect=zoom/f_0123456789abcdef/x','#connect=zoom/https://evil.example','#connect=evil/f_0123456789abcdef']){
   await page.goto('about:blank');await page.goto(base+'/'+hash);await page.waitForTimeout(300);
   assert.ok(!(await box(page).innerText()).includes('did not accept'),hash);
  }
  assert.deepEqual(asked,[]);
  // Every provider: back from its sign-in to its own form, connected or with the reason, never the account page
  if(first)for(const p of PROVIDERS){
   const ok='c_00000000000000d1',bad='f_00000000000000d2';
   states={[p+'/'+ok]:{state:'done'},[p+'/'+bad]:{state:'failed',error:'Not signed in: '+p}};
   await page.goto('about:blank');await page.goto(base+'/#connect='+p+'/'+ok);
   await box(page).getByText('Connected.').waitFor({timeout:8000});
   assert.ok(!page.url().includes('app.example.org'),p);
   await page.goto('about:blank');await page.goto(base+'/#connect='+p+'/'+bad);
   await box(page).getByText('Not signed in: '+p).waitFor({timeout:8000});
   await box(page).getByRole('button',{name:'Try again'}).waitFor();
  }
  // WhatsApp: Show the QR code posts to this dashboard only, and the QR code it shows is this command's own
  posted=[];
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await box(page).locator('[data-connect-signin="whatsapp"]').click();
  await box(page).getByRole('button',{name:'Show the QR code'}).waitFor();
  await shot(page,`whatsapp-intro-${tag}`);
  const until=Math.floor(Date.now()/1000)+60;
  states={'whatsapp/c_00000000000000cc':[{state:'starting'},{state:'qr',until},{state:'qr',until},{state:'connecting'},{state:'done'}]};
  await box(page).getByRole('button',{name:'Show the QR code'}).click();
  await page.waitForURL(u=>!u.hash);
  assert.equal(posted.at(-1).source,'whatsapp');
  const qr=box(page).locator('img.connect-qr');await qr.waitFor({timeout:10000});
  assert.match(await qr.getAttribute('src'),/^\/_machine\/connect-qr\?s=whatsapp&c=c_00000000000000cc&v=\d+$/);
  await page.waitForFunction(()=>document.querySelector('img.connect-qr')?.naturalWidth>0);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`whatsapp-qr-${tag}`);
  await box(page).getByText('Connected.').waitFor({timeout:15000});
  // On the phone itself: a code to type, for that number
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await box(page).locator('[data-connect-signin="whatsapp"]').click();
  await box(page).locator('summary').click();
  await box(page).locator('input[name="signin-phone"]').fill('+32 470 12 34 56');
  states={'whatsapp/c_00000000000000cc':{state:'pair',code:'WXYZ-1234'}};
  await box(page).getByRole('button',{name:'Get a code'}).click();
  await box(page).getByText('WXYZ-1234').waitFor({timeout:10000});
  assert.deepEqual([posted.at(-1).way,posted.at(-1).phone],['code','+32 470 12 34 56']);
  // The phone: its setup code, the pairing request to approve, and how the phone is
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await box(page).locator('[data-connect-signin="android"]').click();
  await box(page).getByRole('button',{name:'Show a setup code'}).waitFor();
  assert.equal(await box(page).locator('input[name="signin-scope"]').count(),0,'no Work or Personal for a phone');
  states={'android/c_00000000000000cc':{state:'phone',code:'setup-code-fixture',qr:true,until:Math.floor(Date.now()/1000)+600,
   pending:[{kind:'device',id:'req-000000001',name:'Pixel 9'}],phone:{name:'Pixel 9',connected:false,notifications:false}}};
  await box(page).getByRole('button',{name:'Show a setup code'}).click();
  await box(page).getByRole('button',{name:'Approve'}).waitFor({timeout:10000});
  assert.equal(posted.at(-1).source,'android');
  assert.equal(await box(page).locator('img.connect-qr').count(),1);
  await box(page).getByText('Pixel 9 is paired but not connected. Open the OpenClaw app on it.').waitFor();
  await shot(page,`android-phone-${tag}`);
  approved=[];await box(page).getByRole('button',{name:'Approve'}).click();
  await page.waitForFunction(()=>document.querySelector('#toast')?.textContent.includes('Approved'));
  assert.deepEqual(approved,[{kind:'device',request_id:'req-000000001'}]);
  // Reconnect on a card and in Needs you: the sign-in form here; Disconnect stays on the account page
  connectors=[{id:'acme-outlook',service:'outlook',display_name:'Work Outlook',email:'alex@acme.example',error:'microsoft_signin_expired',failures:3,
   account_page:MANAGE+'#microsoft',hosted_signin:'microsoft',last_success:'2026-10-20T08:00:00+00:00'}];
  await page.goto('about:blank');await page.goto(base+'/');
  const needs=page.locator('#needs-you [data-hosted-reconnect="microsoft"]');await needs.first().waitFor({timeout:10000});
  assert.equal(await page.locator(`#needs-you a[href^="${MANAGE}"]`).count(),0);
  await needs.first().click();
  await box(page).getByRole('button',{name:'Sign in with Microsoft'}).waitFor({timeout:10000});
  await shot(page,`reconnect-form-${tag}`);
  connectors=[];
  // GitHub in + Add: its own form here, never a link to the account page
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await box(page).locator('[data-connect-signin="github"]').click();
  await box(page).getByRole('button',{name:'Sign in with GitHub'}).waitFor();
  assert.equal(await box(page).locator(`a[href^="${MANAGE}"]`).count(),0);
  await shot(page,`github-intro-${tag}`);
  await box(page).getByRole('button',{name:'Back'}).click();
  // + Add: no source links away to the account page any more
  await box(page).locator('[data-connect-signin="android"]').waitFor();
  assert.equal(await box(page).locator(`a[href^="${MANAGE}"]`).count(),0);
  if(first)await shot(page,`add-list-${tag}`);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
