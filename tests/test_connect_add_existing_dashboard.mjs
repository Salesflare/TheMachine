import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections, + Add, for a source already connected: its row says which account ("Connected: <it>", or the first and
// how many more), and its add view says in one line that this adds a new connection, with a way to the existing one's
// card. Connecting another stays possible. A teammate's shared connection doesn't count; a reconnect of an account
// (it carries its email) says nothing of the kind. SHOTS=<folder> saves the list and the form at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const S=(name,service,label,group,what,extra={})=>({name,service,label,group,what,connected:0,broker:false,...extra});
const sources=[
 S('crm','salesflare','Salesflare CRM','customers','Accounts, contacts and deals, so it knows who matters.',{connected:1,
  form:{secret:'Salesflare API key',scope:true,company:'Acme'}}),
 S('gmail','gmail','Gmail','mail','Your email, what comes in and what you send.',{connected:2,hosted_signin:'gmail'}),
 S('slack','slack','Slack','chat','Your direct messages, mentions and the threads you are in.',{hosted_signin:'slack'}),
 S('stripe','stripe','Stripe','customers','Failed payments, disputes, churn and big new subscriptions.',{hosted_signin:'stripe'}),
 S('zoom','zoom','Zoom','meetings','Meeting summaries and transcripts from Zoom.',{connected:1,hosted_signin:'zoom'})];
const connectors=[
 {id:'acme-crm',service:'salesflare',email:'jamie@acme.example',display_name:'jamie@acme.example',status:'ok',last_success:new Date().toISOString()},
 {id:'acme-gmail',service:'gmail',email:'jamie@acme.example',status:'ok',last_success:new Date().toISOString()},
 {id:'home-gmail',service:'gmail',email:'jamie.lee@mail.example',status:'ok',last_success:new Date().toISOString()},
 // named only after its provider: the row says its card's title (machine/names.py account_card), never "Zoom" again
 {id:'acme-zoom',service:'zoom',email:'jamie@acme.example',display_name:'Zoom',card_title:'jamie@acme.example',card_subtitle:'Work',status:'ok',last_success:new Date().toISOString()},
 {id:'team-stripe',service:'stripe',display_name:'Acme Stripe',shared_by:'Robin Vale',status:'ok',last_success:new Date().toISOString()}];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors,manage_url:'https://app.example.org/account',suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:'https://app.example.org/account',sources,suggested:[]}));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const rows=page=>page.evaluate(()=>Object.fromEntries([...document.querySelectorAll('#connect-add .connect-source')].map(n=>[n.querySelector('b').textContent,
 {have:n.querySelector('small.count')?.textContent||null,check:!!n.querySelector('.cs-on')}])));
const back=async page=>{await page.locator('#connect-add [data-connect-back]').first().click();await page.locator('#connect-add .connect-group').first().waitFor()};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,mobile,scheme] of [[390,844,true,'light'],[390,844,true,'dark'],[1440,900,false,'light'],[1440,900,false,'dark']]){
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}x${height}-${scheme}`;
  await page.goto(base+'/#connections=add');
  await page.locator('#connect-add .connect-group').first().waitFor();
  const list=await rows(page);
  assert.deepEqual(list['Salesflare CRM'],{have:'Connected: jamie@acme.example',check:true},`${tag}: a connected source names its account`);
  assert.deepEqual(list['Gmail'],{have:'Connected: jamie@acme.example and 1 more',check:true},`${tag}: two accounts: the first and how many more`);
  assert.deepEqual(list['Zoom'],{have:'Connected: jamie@acme.example',check:true},`${tag}: named as its card is, never the provider again`);
  assert.deepEqual(list['Slack'],{have:null,check:false},`${tag}: a source not connected says nothing of the kind`);
  assert.deepEqual(list['Stripe'],{have:null,check:false},`${tag}: a teammate's shared connection is not one of the owner's own`);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)<=0,`${tag}: no sideways scroll`);
  if(shots)await page.screenshot({path:`${shots}/${tag}-list.png`,fullPage:true});
  // its form: one line that this adds a new one, a way to the existing card, and Connect still there
  await page.locator('#connect-add .connect-source',{hasText:'Salesflare CRM'}).click();
  const note=page.locator('#connect-add .connect-have');await note.waitFor();
  assert.equal((await note.innerText()).replace(/\s+/g,' ').trim(),'Connected: jamie@acme.example Open its card This adds a new connection. Existing ones stay.');
  assert.ok(await page.locator('#connect-add form[data-connect-setup="crm"] button.primary').isEnabled(),`${tag}: connecting another stays possible`);
  if(shots)await page.screenshot({path:`${shots}/${tag}-form.png`});
  await note.locator('[data-connect-card]').click();
  await page.locator('#connectors>article[data-conn="acme-crm"]').waitFor({state:'visible',timeout:5000});
  // a sign-in source: the same line above its sign-in
  await page.goto(base+'/?again=1#connections=add');await page.locator('#connect-add .connect-group').first().waitFor();
  await page.locator('#connect-add .connect-source',{hasText:'Gmail'}).click();
  await page.locator('#connect-add .connect-signin').waitFor();
  assert.match(await page.locator('#connect-add .connect-have').textContent(),/Connected: jamie@acme\.example and 1 more/,`${tag}: Gmail's sign-in says one is there`);
  await back(page);
  // a source not connected: no such line
  await page.locator('#connect-add .connect-source',{hasText:'Slack'}).click();
  await page.locator('#connect-add .connect-signin').waitFor();
  assert.equal(await page.locator('#connect-add .connect-have').count(),0,`${tag}: nothing about an existing one when there is none`);
  await context.close()}
 // Reconnect on Gmail's card (it carries the account's email): signs that one in again, no "adds a new connection" line
 {const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#connections=add');await page.locator('#connect-add .connect-group').first().waitFor();
  await page.evaluate(()=>{const b=document.createElement('button');b.dataset.hostedReconnect='gmail';b.dataset.email='jamie@acme.example';document.body.append(b);b.click()});await page.locator('#connect-add .connect-signin').waitFor();
  assert.equal(await page.locator('#connect-add .connect-have').count(),0,'a reconnect is not a new connection');
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('connect add existing dashboard ok');
