import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add, one source: one short form like the account's setup page (onboarding.web_form), not a question at
// a time with "work:Main" typed in. Work with its company or Personal as two choices, a key as a password field, then
// Connect. LinkedIn waits for its sign-in on the Machine and opens it; GitHub and WhatsApp show a code to enter.
// SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
let calls=[],run={};
const RUNS={
 linkedin:{session:'s1',state:'running',label:'LinkedIn',lines:['Checking LinkedIn in the Machine’s browser'],signin:'linkedin'},
 trello:{session:'s2',state:'done',label:'Trello',lines:['Connected Trello, saving it as trello (Work · Acme)'],account:'trello',restarting:false},
 github:{session:'s3',state:'running',label:'GitHub',lines:[],code:{kind:'device',code:'ABCD-1234',url:'https://github.com/login/device'}},
 whatsapp:{session:'s4',state:'running',label:'WhatsApp',lines:[],code:{kind:'pair',code:'K7PQ-2M9X'}}};
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);calls.push({action,args});
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:null,paired:true,sources:[
   {name:'linkedin',service:'linkedin',label:'LinkedIn',what:'Your LinkedIn messages.',connected:0,broker:false,form:{ask:[],secret:null,scope:true,company:'Acme',browser:'linkedin'}},
   {name:'trello',service:'trello',label:'Trello',what:'Your boards.',connected:0,broker:false,form:{ask:[['board','Trello board URL']],secret:'Trello API key',scope:true,company:'Acme',note:'Get a key at https://trello.com/app-key'}},
   {name:'github',service:'github',label:'GitHub',what:'Your repositories.',connected:0,broker:false,form:{ask:[],secret:null,scope:true,company:'Acme'}},
   {name:'whatsapp',service:'whatsapp',label:'WhatsApp',what:'Your chats.',connected:0,broker:false,form:{ask:[['phone','Your WhatsApp phone number, with its country code (+32 470 12 34 56)']],secret:null,scope:true,personal:true}}]}));return}
  if(action==='connect_start'){run=RUNS[args.name];res.end(JSON.stringify(run));return}
  if(action==='connect_poll'){res.end(JSON.stringify(run));return}
  if(action==='browser_login_pages'){res.end(JSON.stringify({pages:[{id:'0:li',host:'www.linkedin.com',site:'www.linkedin.com',brand:'LinkedIn',title:'Sign in',username:true,password:true,code:false,saved:null}]}));return}
  if(action==='connect_site_signin'){res.end(JSON.stringify({opened:true,view:null}));return}
  if(action==='connect_stop'){run={...run,state:'failed',error:'Stopped'};res.end(JSON.stringify(run));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const shot=async(page,name)=>{if(shots)await page.locator('#connect-add').screenshot({path:`${shots}/${name}.png`})};
const open=async(page,name)=>{await page.goto('about:blank');await page.goto(base+'/#connections=add');await page.locator(`#connect-add [data-connect="${name}"]`).click();await page.locator(`#connect-add form[data-connect-setup="${name}"]`).waitFor()};
const started=()=>calls.filter(c=>c.action==='connect_start').at(-1)?.args;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['dark','light'])for(const [width,height] of [[1440,900],[390,844]]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>{errors.push(e.message);if(process.env.STACK)console.log(e.stack)});
  const tag=`${width}-${scheme}`,pane=page.locator('#connect-add');
  calls=[];
  // LinkedIn: Work with the company filled in, or Personal; never a "work:Main" text field or a console command
  await open(page,'linkedin');
  assert.equal(await pane.locator('input[name="scope"][value="work"]').isChecked(),true);
  assert.equal(await pane.locator('input[name="company"]').inputValue(),'Acme');
  const text=await pane.innerText();
  assert.doesNotMatch(text,/work:|console|openclaw|assistant connect/i);
  assert.ok(!text.includes('—'),'no em dashes');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`form-linkedin-${tag}`);
  await pane.locator('input[name="scope"][value="personal"]').check();
  assert.equal(await pane.locator('.connect-company').isHidden(),true);
  await pane.locator('input[name="scope"][value="work"]').check();
  await pane.locator('input[name="company"]').fill('');
  await pane.getByRole('button',{name:'Connect'}).click();
  assert.equal(await pane.locator('form .error').innerText(),'Fill in Company.');
  assert.equal(calls.filter(c=>c.action==='connect_start').length,0);
  await pane.locator('input[name="company"]').fill('Acme');
  await pane.getByRole('button',{name:'Connect'}).click();
  await pane.getByText('Sign in to LinkedIn on your Machine. This goes on by itself once you’re in.').waitFor();
  assert.deepEqual(started(),{name:'linkedin',form:true,answers:{},secret:'',scope:'work',company:'Acme'});
  await page.waitForFunction(()=>true);await new Promise(r=>setTimeout(r,300));
  assert.deepEqual(calls.filter(c=>c.action==='connect_site_signin').map(c=>c.args),[{site:'linkedin'}],'the sign-in opens by itself, once');
  const dialog=page.locator('#signin-dialog');await dialog.waitFor();
  assert.match(await dialog.innerText(),/LinkedIn/);
  if(shots)await page.screenshot({path:`${shots}/form-linkedin-signin-dialog-${tag}.png`});
  await page.keyboard.press('Escape');
  await shot(page,`form-linkedin-signin-${tag}`);
  await pane.getByRole('button',{name:'Cancel'}).click();
  // Trello: its board and key in one go, the key as a password; Personal sends no company
  await open(page,'trello');
  assert.equal(await pane.locator('input[name="secret"]').getAttribute('type'),'password');
  assert.match(await pane.locator('.connect-note').innerText(),/trello\.com\/app-key/);
  await shot(page,`form-trello-${tag}`);
  await pane.locator('input[data-key="board"]').fill('https://trello.com/b/abc/sales');
  await pane.locator('input[name="secret"]').fill('k'.repeat(32));
  await pane.locator('input[name="scope"][value="personal"]').check();
  await pane.getByRole('button',{name:'Connect'}).click();
  await pane.getByText('Connected.').waitFor();
  assert.deepEqual(started(),{name:'trello',form:true,answers:{board:'https://trello.com/b/abc/sales'},secret:'k'.repeat(32),scope:'personal',company:''});
  assert.ok(!(await pane.innerText()).includes('k'.repeat(32)),'the key is not shown back');
  // GitHub: a device code to enter at GitHub, with a link there
  await open(page,'github');
  await pane.getByRole('button',{name:'Connect'}).click();
  await pane.locator('.connect-code').waitFor();
  assert.equal(await pane.locator('.connect-code').innerText(),'ABCD-1234');
  assert.equal(await pane.getByRole('link',{name:'Open GitHub ↗'}).getAttribute('href'),'https://github.com/login/device');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`form-github-code-${tag}`);
  await pane.getByRole('button',{name:'Cancel'}).click();
  // WhatsApp: personal to start with, the phone number, then the pairing code for Linked devices
  await open(page,'whatsapp');
  assert.equal(await pane.locator('input[name="scope"][value="personal"]').isChecked(),true);
  await shot(page,`form-whatsapp-${tag}`);
  await pane.locator('input[data-key="phone"]').fill('+32 470 00 00 00');
  await pane.getByRole('button',{name:'Connect'}).click();
  await pane.locator('.connect-code').waitFor();
  assert.match(await pane.innerText(),/Link with phone number instead\. Enter this code:\s+K7PQ-2M9X/);
  assert.equal(await pane.getByRole('link',{name:'Open GitHub ↗'}).count(),0);
  await shot(page,`form-whatsapp-code-${tag}`);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('connect form dashboard ok');
