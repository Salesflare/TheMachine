import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// + Add, Exchange Server or Other email: an address on Microsoft 365 swaps the password for Sign in with Microsoft, which
// opens the Outlook Calendar (or Outlook) sign-in as it is (connect_address_signin, machine/app/connect.py). An address
// on the company's own server, or no answer, keeps the password form as it was. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
let calls=[];
const CLOUD='alex@cloudco.test',OWN='alex@acme.test';
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);calls.push({action,args});
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:null,paired:true,sources:[
   {name:'exchange',service:'exchange',label:'Exchange Server',what:'Meetings from your company’s own Exchange Server. Read-only.',connected:0,broker:false,
    form:{ask:[['email','Email address']],secret:'Password',scope:true,company:'',learn:'exchange',advanced:[['username','Username (DOMAIN\\name)'],['ews_url','Exchange server']]}},
   {name:'imap',service:'imap',label:'Other email',what:'Any mailbox with IMAP.',connected:0,broker:false,
    form:{ask:[['email','Email address']],secret:'Password',scope:true,company:'',learn:'imap',advanced:[['username','Username'],['imap_host','IMAP server']]}},
   {name:'outlook',service:'outlook',label:'Outlook',what:'Your email.',connected:0,broker:false,signin:'microsoft',form:{ask:[],secret:null,scope:true,auto:true,company:''}},
   {name:'outlook_calendar',service:'outlook_calendar',label:'Outlook Calendar',what:'Your meetings.',connected:0,broker:false,signin:'microsoft',form:{ask:[],secret:null,scope:true,auto:true,company:''}}]}));return}
  if(action==='connect_address_signin'){const on=args.email===CLOUD;
   // the Machine looks a while; an address on the company's own server finds nothing
   await new Promise(r=>setTimeout(r,150));res.end(JSON.stringify({signin:on?{exchange:'outlook_calendar',imap:'outlook'}[args.name]:null}));return}
  if(action==='connect_signin_state'){res.end(JSON.stringify({state:'idle'}));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const open=async(page,name)=>{await page.goto('about:blank');await page.goto(base+'/#connections=other');await page.locator(`#connect-add [data-connect="${name}"]`).click();await page.locator(`#connect-add form[data-connect-setup="${name}"]`).waitFor()};
const looked=()=>calls.filter(c=>c.action==='connect_address_signin').map(c=>c.args);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const [width,height] of [[1440,900],[390,844]]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}-${scheme}`,pane=page.locator('#connect-add'),form=pane.locator('form[data-connect-setup]');
  const password=pane.locator('input[name="secret"]'),ms=pane.getByRole('button',{name:'Sign in with Microsoft'});
  const snap=async name=>{if(shots)await page.screenshot({path:`${shots}/${name}-${tag}.png`})};
  calls=[];
  // Exchange Server, an address on Microsoft 365: no password, Sign in with Microsoft in its place
  await open(page,'exchange');
  await snap('exchange-before');
  assert.ok(await password.isVisible());
  await pane.locator('input[data-key="email"]').fill(CLOUD);
  await ms.waitFor();
  assert.equal(await password.isVisible(),false,'no password for Microsoft 365');
  assert.equal(await pane.getByRole('button',{name:'Connect',exact:true}).isVisible(),false);
  assert.equal(await pane.locator('.connect-advanced').isVisible(),false);
  const says=await pane.locator('.connect-ms').innerText();
  assert.equal(says,`${CLOUD} is on Microsoft 365, so no password is needed.`);
  assert.ok(!says.includes('—'),'no em dashes');
  assert.deepEqual(looked(),[{name:'exchange',email:CLOUD}],'looked up once, after typing stopped');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await snap('exchange-microsoft');
  // Another address: the password comes back (the company's own server)
  await pane.locator('input[data-key="email"]').fill(OWN);
  await page.waitForFunction(()=>document.querySelector('#connect-add form')?.dataset.looked==='alex@acme.test');
  assert.ok(await password.isVisible(),'the password form stays for a company’s own server');
  assert.equal(await ms.isVisible(),false);
  assert.equal(await pane.locator('.connect-ms').isVisible(),false);
  // Back on Microsoft 365, Sign in with Microsoft opens the Outlook Calendar sign-in as it is
  await pane.locator('input[data-key="email"]').fill(CLOUD);
  await ms.waitFor();
  await ms.click();
  await pane.locator('form[data-connect-setup]').waitFor({state:'detached'});
  await pane.getByText('Outlook mail and calendar. Sends only emails you approved.').waitFor();  // the Microsoft sign-in's own intro
  assert.ok(await ms.isVisible());
  assert.equal(calls.filter(c=>c.action==='connect_signin').length,0,'nothing starts before its own Sign in');
  assert.equal(calls.filter(c=>c.action==='connect_start').length,0,'no password connect started');
  await snap('exchange-signin');
  // Other email: the same, to Outlook; Enter goes to the sign-in too
  await open(page,'imap');
  await pane.locator('input[data-key="email"]').fill(CLOUD);
  await ms.waitFor();
  await snap('imap-microsoft');
  await pane.locator('input[data-key="email"]').press('Enter');
  await pane.locator('form[data-connect-setup]').waitFor({state:'detached'});
  assert.equal(calls.filter(c=>c.action==='connect_start').length,0);
  assert.deepEqual(looked().at(-1),{name:'imap',email:CLOUD});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('connect microsoft instead dashboard ok');
