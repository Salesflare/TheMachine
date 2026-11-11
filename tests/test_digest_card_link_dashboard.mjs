import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The morning digest's Open (notify.compose: #card=<id>&or=chat) shows the to-do in the To-dos list: scrolled into
// view, highlighted and in full. One that isn't on the list as shown (done, snoozed, another scope, or gone) opens
// its chat instead, as the link did before. SHOT_DIR=<folder> saves the opened list at 390 in light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),later=new Date(Date.now()+864e5).toISOString();
const id=n=>n.toString(16).padStart(16,'a');
const TARGET=id(9),DONE=id(20),SNOOZED=id(21),PERSONAL=id(22),GONE=id(23);
const card=(i,title,extra={})=>({id:i,title,body:'Ready for a look.',status:'pending',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1],...extra});
const filler=Array.from({length:9},(_,n)=>card(id(n),'Reply about the quote '+(n+1)));
const status=()=>({suggestions:[...filler,card(TARGET,'Send the signed lease back',{status:'prepared',body:'The lease is signed and ready to go back. '.repeat(12)}),
  card(DONE,'Book the venue',{status:'completed',closed_at:now}),card(SNOOZED,'Renew the parking permit',{status:'snoozed',snoozed_until:later}),
  card(PERSONAL,'Call the plumber',{scope:'personal'})],
 done_counts:{all:1,work:1,personal:0},promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
 review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:[],next:null,total:0}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.SHOT_DIR,errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width:390,height:844},locale:'en-US',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const open=async hash=>{const page=await context.newPage();page.on('pageerror',e=>errors.push(hash+': '+e.message));await page.goto(base+hash);await page.waitForFunction(()=>!!state?.suggestions);return page};
  // An open to-do: the list, with it in view and highlighted, in full; no chat
  let page=await open('#card='+TARGET+'&or=chat');
  const el=page.locator('#task-'+TARGET);
  await page.waitForFunction(i=>document.getElementById('task-'+i)?.classList.contains('flash'),TARGET,{timeout:8000});
  await page.waitForFunction(i=>{const r=document.getElementById('task-'+i).getBoundingClientRect();return r.top>=0&&r.top<innerHeight-80},TARGET,{timeout:8000});
  assert.equal(await page.evaluate(()=>scrollY>0),true,'scrolled to it');
  assert.equal(await page.evaluate(()=>chatId),null,'no chat opens');
  assert.equal(await page.evaluate(()=>location.hash),'','the link is taken off the address');
  assert.equal(await page.evaluate(()=>!document.querySelector('#inbox').hidden),true,'the To-dos list shows');
  assert.equal(await page.evaluate(i=>expandedBodies.has(i),TARGET),true,'shown in full');
  assert.equal(await el.locator('[data-more]').getAttribute('aria-expanded'),'true','its long text open: Show less, not Show more');
  if(shots){await page.waitForTimeout(700);await page.screenshot({path:`${shots}/digest-open-390-${scheme}.png`})}
  await page.close();
  if(scheme==='dark')break;
  // Done, snoozed or gone: its chat, as before (the chat shows "isn't here anymore" for one that is gone)
  for(const other of [DONE,SNOOZED]){page=await open('#card='+other+'&or=chat');
   await page.waitForFunction(i=>chatOpen()?.id===i,other,{timeout:8000});
   assert.equal(await page.evaluate(()=>location.hash),'#chat='+other);await page.close()}
  page=await open('#card='+GONE+'&or=chat');
  await page.waitForFunction(()=>/isn.t here anymore/.test(document.querySelector('#toast')?.textContent||''),null,{timeout:8000});
  await page.close();
  // Another scope than the one shown: its chat, and the owner's Work filter stays
  page=await open('');await page.evaluate(()=>{scopeFilter='work';render()});
  await page.evaluate(i=>{location.hash='#card='+i+'&or=chat'},PERSONAL);
  await page.waitForFunction(i=>chatOpen()?.id===i,PERSONAL,{timeout:8000});
  assert.equal(await page.evaluate(()=>scopeFilter),'work');
  await page.close();
  // Other #card links (a person's page, Open draft) keep revealing it: a done one shows in Done
  page=await open('#card='+DONE);
  await page.locator('#task-'+DONE).waitFor({timeout:8000});
  assert.equal(await page.evaluate(()=>chatId),null);
  await page.close();
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
