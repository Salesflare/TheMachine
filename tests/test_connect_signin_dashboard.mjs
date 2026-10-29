import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add on a self-hosted Machine: Intercom signs in through The Machine's own app once this Machine is
// paired (a one-time start link in a new tab, then its row follows how it goes); not paired, it says pair first.
// Intercom and Trello sign in only: no token to paste. Google, Microsoft and Zoom the same way, with their own app folded away (Use your
// own app). One the control plane has no app for (Stripe here) shows the other way at once, and one it refuses anyway
// opens no tab: it says so and opens that other way. SHOTS=<folder> saves screenshots.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
let paired=true,state='started',calls=[],refuse=false;
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/connect/start/'+'A'.repeat(32)){res.setHeader('Content-Type','text/html');res.end('<title>Intercom</title>consent');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);calls.push(action);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:null,paired,pair_url:'https://app.example.org/account?tab=fleet#devices',sources:[
   {name:'intercom',service:'intercom',label:'Intercom',what:'Customer conversations in your Intercom workspace.',connected:0,broker:false,account_page:'source-intercom',signin:true},
   {name:'trello',service:'trello',label:'Trello',what:'Card changes, comments and activity on one Trello board.',connected:0,broker:false,account_page:'source-trello',signin:'trello'},
   {name:'gmail',service:'gmail',label:'Gmail',what:'Your email.',connected:0,broker:false,signin:'google'},
   {name:'calendar',service:'calendar',label:'Google Calendar',what:'Your meetings.',connected:0,broker:false,signin:'google'},
   {name:'outlook',service:'outlook',label:'Outlook',what:'Your Outlook email.',connected:0,broker:false,signin:'microsoft'},
   {name:'zoom',service:'zoom',label:'Zoom',what:'Your meetings.',connected:0,broker:false,signin:'zoom'},
   {name:'docs',service:'docs',label:'Docs',what:'Comments and shares on your docs.',connected:0,broker:true,signin:'microsoft_docs'},
   {name:'stripe',service:'stripe',label:'Stripe',what:'Payments and subscriptions.',connected:0,broker:false,signin:'stripe',signin_off:true},
   {name:'github',service:'github',label:'GitHub',connected:0,broker:false}]}));return}
  if(action==='connect_signin'){assert.ok(['intercom','trello','gmail','docs'].includes(args.name));if(refuse){res.end(JSON.stringify({state:'unavailable'}));return}res.end(JSON.stringify({url:base+'/connect/start/'+'A'.repeat(32),state:'started'}));return}
  if(action==='connect_signin_state'){res.end(JSON.stringify(state==='done'?{state:'done',name:'Example Support',replies:true}:state==='done-google'?{state:'done',name:'dee@acme.example'}:state==='done-trello'?{state:'done',name:'Trello'}:{state}));return}
  if(action==='connect_start'){res.end(JSON.stringify({session:'s1',state:'running',label:'Intercom',lines:[],question:{id:'q1',kind:'secret',prompt:'Intercom access token'}}));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const shot=async(page,name)=>{if(shots)await page.locator('#connect-add').screenshot({path:`${shots}/${name}.png`})};
const pageShot=async(page,name)=>{if(shots){await page.locator('#connect-add').scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/${name}.png`})}};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['dark','light'])for(const [width,height] of [[1440,900],[1440,700],[390,844],[320,700]]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}x${height}-${scheme}`;
  paired=true;state='started';calls=[];
  await page.goto(base+'/#connections=add');
  await page.locator('#connect-add [data-connect-signin="intercom"]').click();
  const go=page.getByRole('button',{name:'Sign in with Intercom'});
  await go.waitFor();
  assert.match(await page.locator('#connect-add').innerText(),/Reads your conversations\. Replies only after you approve them, as yourself\. Never assigns or closes\./);
  assert.equal(await page.locator('#connect-add details.connect-other').count(),0,'no token to paste: Sign in with Intercom only');
  assert.ok(!(await page.locator('#connect-add').innerText()).includes('—'),'no em dashes');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`add-intercom-${tag}`);
  const [tab]=await Promise.all([context.waitForEvent('page'),go.click()]);
  await tab.waitForURL(/\/connect\/start\//);
  assert.equal(await tab.evaluate(()=>window.opener),null,'the sign-in tab has no way back into the dashboard');
  await tab.close();
  await page.getByText('Sign in at Intercom in the tab that opened').waitFor();
  await shot(page,`add-intercom-waiting-${tag}`);
  state='done';
  await page.getByText('Connected to Example Support.').waitFor({timeout:8000});
  assert.match(await page.locator('#connect-add').innerText(),/Replies go as you, after you approve each one\./);
  assert.equal(await page.locator('#connect-add details.connect-other').count(),0);
  await shot(page,`add-intercom-connected-${tag}`);
  // Trello: the same, read only, the board picked after signing in
  state='started';
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await page.locator('#connect-add [data-connect-signin="trello"]').click();
  const trello=page.getByRole('button',{name:'Sign in with Trello'});
  await trello.waitFor();
  assert.match(await page.locator('#connect-add').innerText(),/Reads cards, comments and activity on one board you pick next\. Never changes anything in Trello\./);
  assert.equal(await page.locator('#connect-add details.connect-other').count(),0,'no key or token to paste');
  assert.ok(!(await page.locator('#connect-add').innerText()).includes('—'),'no em dashes');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`add-trello-${tag}`);await pageShot(page,`page-trello-${tag}`);
  const [ttab]=await Promise.all([context.waitForEvent('page'),trello.click()]);
  await ttab.waitForURL(/\/connect\/start\//);await ttab.close();
  await page.getByText('Sign in at Trello in the tab that opened').waitFor();
  state='done-trello';
  await page.getByText('Connected to Trello.').waitFor({timeout:8000});
  await shot(page,`add-trello-connected-${tag}`);await pageShot(page,`page-trello-connected-${tag}`);
  // Not paired: pair first, on the account page; no token to paste instead
  paired=false;
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await page.locator('#connect-add [data-connect-signin="intercom"]').click();
  const pair=page.getByRole('link',{name:'Pair this Machine first ↗'});
  await pair.waitFor();
  assert.equal(await pair.getAttribute('href'),'https://app.example.org/account?tab=fleet#devices');
  assert.equal(await pair.getAttribute('target'),'_blank');
  assert.equal(await page.getByRole('button',{name:'Sign in with Intercom'}).count(),0);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  assert.equal(await page.locator('#connect-add details.connect-other').count(),0);
  await shot(page,`add-intercom-not-paired-${tag}`);
  // Google: Gmail and Calendar in one sign-in, with its own app folded away
  paired=true;state='started';
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await page.locator('#connect-add [data-connect-signin="gmail"]').click();
  const google=page.getByRole('button',{name:'Sign in with Google'});
  await google.waitFor();
  assert.match(await page.locator('#connect-add').innerText(),/Gmail and Google Calendar\. Sends only emails you approved\./);
  assert.equal(await page.locator('#connect-add details.connect-other summary').innerText(),'Use your own app');
  assert.equal(await page.locator('#connect-add details.connect-other').getAttribute('open'),null);
  assert.ok(!(await page.locator('#connect-add').innerText()).includes('—'),'no em dashes');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`add-google-${tag}`);
  const [gtab]=await Promise.all([context.waitForEvent('page'),google.click()]);
  await gtab.close();
  await page.getByText('Sign in at Google in the tab that opened').waitFor();
  await shot(page,`add-google-waiting-${tag}`);
  state='done-google';
  await page.getByText('Connected to dee@acme.example.').waitFor({timeout:8000});
  assert.doesNotMatch(await page.locator('#connect-add').innerText(),/Replies go as you/);
  await shot(page,`add-google-connected-${tag}`);
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await page.locator('#connect-add [data-connect-signin="zoom"]').click();
  await page.getByRole('button',{name:'Sign in with Zoom'}).waitFor();
  assert.match(await page.locator('#connect-add').innerText(),/Reads only\./);
  await page.locator('#connect-add details.connect-other summary').click();
  await shot(page,`add-zoom-own-app-${tag}`);
  // Docs on a Microsoft address: its own consent, signed in with Microsoft through The Machine's app; no own app to fold away
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await page.locator('#connect-add [data-connect-signin="docs"]').click();
  await page.getByRole('button',{name:'Sign in with Microsoft'}).waitFor();
  assert.equal(await page.locator('#connect-add h3').innerText(),'Docs');
  assert.match(await page.locator('#connect-add').innerText(),/Word, OneDrive and SharePoint, for an Outlook address you connected\. Reads only\./);
  assert.equal(await page.locator('#connect-add details.connect-other').count(),0);
  // Stripe, which the control plane has no app for: no Sign in button, pasting a restricted key open at once
  let opened=0;context.on('page',()=>opened++);
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await page.locator('#connect-add [data-connect-signin="stripe"]').click();
  await page.getByText('Sign in with Stripe isn’t available yet. Paste a restricted key instead.').waitFor();
  assert.equal(await page.getByRole('button',{name:'Sign in with Stripe'}).count(),0);
  assert.notEqual(await page.locator('#connect-add details.connect-other').getAttribute('open'),null,'the paste form is open');
  assert.ok(await page.getByRole('button',{name:'Paste a key'}).isVisible());
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`add-stripe-unavailable-${tag}`);await pageShot(page,`page-stripe-unavailable-${tag}`);
  // Intercom refused anyway (the list was not known): no tab opens or closes; the line, and Back
  refuse=true;calls=[];
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await page.locator('#connect-add [data-connect-signin="intercom"]').click();
  await page.getByRole('button',{name:'Sign in with Intercom'}).click();
  await page.getByText('Sign in with Intercom isn’t available yet.').waitFor();
  assert.equal(opened,0,'no tab for a refused start');
  assert.ok(calls.includes('connect_signin'));
  assert.equal(await page.getByRole('button',{name:'Sign in with Intercom'}).count(),0);
  assert.equal(await page.getByRole('button',{name:'Try again'}).count(),0);
  assert.equal(await page.locator('#connect-add details.connect-other').count(),0);
  assert.ok(await page.locator('#connect-add').getByRole('button',{name:'Back'}).isVisible());
  await shot(page,`add-intercom-refused-${tag}`);await pageShot(page,`page-intercom-refused-${tag}`);
  refuse=false;
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await shot(page,`add-list-${tag}`);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
