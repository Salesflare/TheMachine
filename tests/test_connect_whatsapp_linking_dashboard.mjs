import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Linking WhatsApp on a hosted Machine, after the QR code: connected within a minute, every step says where it is and
// never sits on one line for longer than it should. Account (the Machine connects it), queued (other setup work first),
// done (its card to open), then the card counts the history WhatsApp keeps sending. A link that stops moving, or a
// control plane that stops answering, ends in a message with Try again, and the page reports it to the error feed.
// 2026-11-06: a new owner saw "Signed in. Connecting it now." for almost 6 minutes. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const MANAGE='https://app.example.org/setup',COMMAND='whatsapp/c_00000000000000cc';
let answer=null,reports=[],connectors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],manage_url:MANAGE}));return}
 if(url.pathname==='/_machine/connect-state'){const a=typeof answer==='function'?answer():answer;
  if(!a){res.statusCode=502;res.end('{"error":"down"}');return}res.end(JSON.stringify(a));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);
  if(action==='client_error'){reports.push(...(args?.errors||[]));res.end('{"ok":true}');return}
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:MANAGE,sources:[
   {name:'whatsapp',service:'whatsapp',label:'WhatsApp',connected:0,broker:false,hosted_signin:'whatsapp'}]}));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const shot=async(page,name)=>{if(shots)await page.screenshot({path:`${shots}/${name}.png`})};
const box=page=>page.locator('#connect-add');
const ACCOUNT='Linked. Connecting WhatsApp to your Machine.';
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const runs=shots?[['light',1440,900],['light',1440,700],['light',390,844],['dark',390,844]]:[['light',1440,900],['dark',390,844]];
 for(const [scheme,width,height] of runs){const tag=`${width}x${height}-${scheme}`;
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const open=async()=>{await page.goto('about:blank');await page.goto(base+'/#connect='+COMMAND)};
  // Linked: the Machine connects it, after other setup work when some runs
  connectors=[];answer={state:'connecting',phase:'account',since:1};
  await open();
  await box(page).getByText(ACCOUNT).waitFor({timeout:8000});
  assert.equal(await box(page).getByText('Signed in. Connecting it now.').count(),0,'no bare connecting line for WhatsApp');
  assert.equal(await box(page).getByText('5 minutes').count(),0,'no fixed wait');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`whatsapp-account-${tag}`);
  answer={state:'connecting',phase:'queued'};
  await box(page).getByText('Linked. Your Machine finishes another setup step first, then connects WhatsApp.').waitFor({timeout:8000});
  await shot(page,`whatsapp-queued-${tag}`);
  // a control plane that sends no phase says the same as account
  answer={state:'connecting'};
  await box(page).getByText(ACCOUNT).waitFor({timeout:8000});
  // done: connected, and once its card is there, a button to it
  answer={state:'done',account:'personal-whatsapp'};
  await box(page).getByText('Connected.').waitFor({timeout:8000});
  await box(page).getByText('Restarting to start reading it…').waitFor();
  connectors=[{id:'personal-whatsapp',service:'whatsapp',display_name:'WhatsApp',last_success:new Date().toISOString(),total:412,signals_24h:37,pending:412,history:14717}];
  await box(page).getByRole('button',{name:'Open its card'}).waitFor({timeout:20000});
  await box(page).getByText('Its card shows your chat history coming in.').waitFor();
  await shot(page,`whatsapp-done-${tag}`);
  // its card, while the history comes in: the count so far; gone once it stops growing (assistant.whatsapp_history)
  await box(page).getByRole('button',{name:'Open its card'}).click();
  const card=page.locator('article').filter({hasText:'Bringing in your chat history'});
  await card.getByText('Bringing in your chat history: 14,717 messages so far.').waitFor({timeout:8000});
  await card.scrollIntoViewIfNeeded();
  await shot(page,`whatsapp-card-first-sync-${tag}`);
  connectors=[{...connectors[0],history:null}];
  for(let i=0;i<40&&await page.getByText('Bringing in your chat history').count();i++)await page.waitForTimeout(500);
  assert.equal(await page.getByText('Bringing in your chat history').count(),0,'no count once the first sync is done');
  await context.close();
 }
 // Stalls, on a clock of the page's own: a linked WhatsApp still connecting after 5 minutes, nothing new for 15 minutes
 // in other steps, or no answer for 3 minutes. Waiting on other setup work is not a stall (the cloud ends it at 30).
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.clock.install();
 const open=async()=>{await page.goto('about:blank');await page.goto(base+'/#connect='+COMMAND)};
 const wait=async(text)=>{for(let i=0;i<200;i++){if(await box(page).getByText(text).count())return;await page.clock.runFor(1000)}assert.fail('never showed: '+text)};
 answer={state:'connecting',phase:'account',since:1};reports=[];
 await open();
 await wait(ACCOUNT);
 await page.clock.runFor(4*60000);  // slow, still answering: still waiting
 assert.equal(await box(page).getByText('Connecting WhatsApp is taking too long').count(),0);
 await page.clock.runFor(90000);
 await wait('Connecting WhatsApp is taking too long. Try again to pick up where it stopped.');
 await box(page).getByRole('button',{name:'Try again'}).waitFor();
 await shot(page,'whatsapp-stalled-1440x900-light');
 const polls=async()=>{let n=0;const count=r=>{if(r.url().includes('/_machine/connect-state'))n++};page.on('request',count);await page.clock.runFor(30000);page.off('request',count);return n};
 assert.equal(await polls(),0,'a stalled link is not asked again and again');
 for(let i=0;i<20&&!reports.some(r=>r.kind==='ConnectStalled');i++)await page.clock.runFor(1000);
 assert.ok(reports.some(r=>r.kind==='ConnectStalled'&&r.message==='whatsapp: account'),'reported to the error feed: '+JSON.stringify(reports));
 // waiting on other setup work: the page keeps following, the cloud bounds it
 answer={state:'connecting',phase:'queued'};
 await open();
 await wait('Linked. Your Machine finishes another setup step first');
 await page.clock.runFor(20*60000);
 assert.equal(await box(page).getByText('Connecting WhatsApp is taking too long').count(),0,'queued is not stalled');
 // the control plane stops answering: after 3 minutes, Try again
 answer={state:'connecting',phase:'account'};
 await open();
 await wait('Linked. Connecting WhatsApp to your Machine.');
 answer=null;
 await page.clock.runFor(2*60000);
 assert.equal(await box(page).getByText('Connecting WhatsApp is taking too long').count(),0);
 await page.clock.runFor(90000);
 await wait('Connecting WhatsApp is taking too long. Try again');
 // before the code: the same when its answers stop
 answer={state:'starting'};
 await open();
 await wait('Getting a code from WhatsApp…');
 answer=null;
 await page.clock.runFor(4*60000);
 await wait('This is taking longer than it should. Try again.');
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
