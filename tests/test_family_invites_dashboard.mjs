import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Inviting family at the right moment (family_invites.py): a family to-do carries a quiet "Invite Sasha?" line. Invite
// is a link to the account page's prefilled invite form (a new tab; nothing is sent from here) and marks it used; Not
// now posts family_invite later. Settings, Fleet has the switch. SHOTS=<folder> saves screenshots, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const URL_='https://app.example.test/account?tab=fleet&invite=family&to=sasha%40mail.example&name=Sasha+Lane#invites-fl_ffffffffffffffff';
const cards=[{id:'c1',title:'Who picks up the kids on Wednesday?',body:'Sasha asked who does the school run on Wednesday. Your calendar has a client call until 16:00.',
 status:'pending',scope:'personal',created_at:now,event_ids:[1],owner_step:true,
 family_invite:{name:'Sasha Lane',first:'Sasha',email:'sasha@mail.example',question:'Invite Sasha?',line:'Your Machines can sort this out without you asking each other.',url:URL_}},
 {id:'c2',title:'Reply to Kim about the invoice',body:'Kim asks for the invoice again.',status:'pending',scope:'work',created_at:now,event_ids:[2]}];
let switchOn=true;
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:true,waiting:0,family_invites:switchOn}});
const calls=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const j=JSON.parse(body||'{}');calls.push(j);if(j.action==='family_invite_setting'){switchOn=j.args.on;res.end(JSON.stringify({on:switchOn}));return}res.end('{"ok":true}');return}
 if(url.pathname.startsWith('/api/fleet')){res.end(JSON.stringify({on:true,fleets:[],waiting:[],asked:[],log:[],notices:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const width of [1280,390]){
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-c1').waitFor();
  const note=page.locator('#task-c1 .note.family-invite');
  assert.equal((await note.innerText()).replace(/\s+/g,' ').trim(),'Invite Sasha? Your Machines can sort this out without you asking each other. Invite Not now');
  assert.equal(await page.locator('#task-c2 .family-invite').count(),0);  // only the to-do that carries one
  const link=note.locator('[data-family-invite="open"]');
  assert.equal(await link.getAttribute('href'),URL_);assert.equal(await link.getAttribute('target'),'_blank');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(process.env.SHOTS){await page.locator('#task-c1').scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.SHOTS}/todo-${width}-${scheme}.png`});
   await page.locator('#task-c1').screenshot({path:`${process.env.SHOTS}/todo-card-${width}-${scheme}.png`})}
  calls.length=0;await note.locator('[data-family-invite="later"]').click();await page.waitForTimeout(200);
  assert.deepEqual(calls[0],{action:'family_invite',args:{suggestion_id:'c1',do:'later'}});
  // Invite: the new tab opens from the link itself; the dashboard only records the tap
  calls.length=0;const opened=context.waitForEvent('page');await link.click();const tab=await opened;await tab.close().catch(()=>{});await page.waitForTimeout(200);
  assert.deepEqual(calls[0],{action:'family_invite',args:{suggestion_id:'c1',do:'open'}});
  // Settings, Fleet: the switch
  await page.evaluate(()=>{location.hash='settings';});await page.waitForTimeout(300);
  const sw=page.locator('#family-invite-switch');
  if(await sw.isVisible()){assert.equal(await sw.getAttribute('aria-checked'),'true');
   if(process.env.SHOTS)await page.locator('#settings-fleet').screenshot({path:`${process.env.SHOTS}/setting-${width}-${scheme}.png`});calls.length=0;await sw.click();await page.waitForTimeout(200);
   assert.deepEqual(calls[0],{action:'family_invite_setting',args:{on:false}});assert.equal(await sw.getAttribute('aria-checked'),'false');
   await sw.click();await page.waitForTimeout(200)}
  else assert.equal(await sw.count(),1);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('family invites dashboard ok');
