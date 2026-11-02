import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdir} from 'node:fs/promises';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Moving a to-do to another area (todo_areas.py): More shows "Move to Work" on a Personal to-do, the tap moves it
// (the Work chip shows), the toast's Undo moves it back. A run that asked for the move (preparation_move_to) gets it as
// the to-do's lead button, never moved without the tap. With several companies, Change area opens a picker.
// SHOT_DIR=<folder> also saves the More menu and the to-do right after a move, at 390 and 1280, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const fresh=()=>[
 {id:'a1a1a1a1a1a1a1a1',title:'Ask the billing tool why zero invoices still go out',status:'instructions',scope:'personal',area:'personal',created_at:now,event_ids:[1],
  body:'Robin still gets a monthly invoice of 0 euros. The reply to Robin is drafted.',people:[{id:'wa:1',name:'Robin Vale'}],
  preparation_status:'blocked',preparation_reason:'The email to the billing tool has to come from your work address.',preparation_no_questions:true,preparation_questions:[]},
 {id:'b2b2b2b2b2b2b2b2',title:'Send the venue the signed form',status:'instructions',scope:'personal',area:'personal',created_at:now,event_ids:[2],
  body:'The form is filled in and ready to send.',preparation_status:'blocked',preparation_reason:'This has to go out from your work mailbox.',
  preparation_no_questions:true,preparation_questions:[],preparation_move_to:'work:Acme'}];
let cards,areas,posts;
const reset=(many=false)=>{cards=fresh();posts=[];areas=[{id:'personal',label:'Personal'},{id:'work:Acme',label:many?'Work at Acme':'Work'},...(many?[{id:'work:Beta',label:'Work at Beta'}]:[])]};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,areas,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/action'){const {action,args}=JSON.parse(body||'{}');if(action==='card_move'){posts.push(args);const c=cards.find(x=>x.id===args.suggestion_id);
   const to=args.undo?'personal':args.area,resumed=!args.undo&&c.preparation_move_to===to;
   Object.assign(c,{area:to,scope:to==='personal'?'personal':'work'},resumed?{preparation_status:'queued',preparation_move_to:null,preparation_reason:null}:{});
   res.end(JSON.stringify({id:c.id,area:to,decision_id:args.decision_id,resumed}));return}}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOT_DIR;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const width of [390,1280]){
  reset();
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  const card=page.locator('#task-a1a1a1a1a1a1a1a1');await card.waitFor();
  // A Personal to-do: More has Move to Work; the state stays Stuck with Try again (its run asked nothing)
  await card.locator('details.more-actions summary').click();
  const item=card.locator('.more-menu [data-card-move]');
  assert.equal(await item.textContent(),'Move to Work');assert.equal(await item.getAttribute('data-area'),'work:Acme');
  if(shots)await card.screenshot({path:`${shots}/more-menu-${width}-${scheme}.png`});
  await item.click();
  await page.locator('#toast.show').waitFor();
  assert.match(await page.locator('#toast').innerText(),/^Moved to Work\s+Undo$/);
  assert.deepEqual({area:posts[0].area,id:posts[0].suggestion_id},{area:'work:Acme',id:'a1a1a1a1a1a1a1a1'});
  await page.waitForFunction(()=>document.querySelector('#task-a1a1a1a1a1a1a1a1 .more-menu [data-card-move]')?.textContent==='Move to Personal');
  if(shots){await page.waitForTimeout(700);await page.screenshot({path:`${shots}/after-move-${width}-${scheme}.png`})}  // the to-do with Work on it, and the toast's Undo
  // Undo on the toast moves it back
  await page.locator('#toast [data-move-undo]').click();
  await page.waitForFunction(()=>document.querySelector('#task-a1a1a1a1a1a1a1a1 .more-menu [data-card-move]')?.textContent==='Move to Work');
  assert.equal(posts[1].undo,posts[0].decision_id);
  // A run that asked for the move: its lead button, Needs your help; tapping it carries on (Preparing)
  const asked=page.locator('#task-b2b2b2b2b2b2b2b2');
  const lead=asked.locator('.actions > button.primary').first();
  assert.equal(await lead.textContent(),'Move to Work');
  assert.match(await asked.innerText(),/Needs your help/);
  if(shots)await asked.screenshot({path:`${shots}/asked-${width}-${scheme}.png`});
  await lead.click();
  await page.waitForFunction(()=>/Preparing/.test(document.querySelector('#task-b2b2b2b2b2b2b2b2')?.innerText||''));
  await context.close()}
 // Several companies: Change area opens a picker with the other areas
 reset(true);
 const context=await browser.newContext({viewport:{width:390,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 const card=page.locator('#task-a1a1a1a1a1a1a1a1');await card.waitFor();
 await card.locator('details.more-actions summary').click();
 await card.locator('.more-menu [data-card-area]').click();
 const picker=card.locator('.area-picker');await picker.waitFor();
 assert.deepEqual(await picker.locator('option').allTextContents(),['Work at Acme','Work at Beta']);
 if(shots)await card.screenshot({path:`${shots}/change-area-390-light.png`});
 await picker.locator('select').selectOption('work:Beta');await picker.locator('[data-ap="move"]').click();
 await page.locator('#toast.show').waitFor();
 assert.match(await page.locator('#toast').innerText(),/^Moved to Work at Beta/);
 assert.equal(posts[0].area,'work:Beta');
 await context.close();
 assert.deepEqual(errors,[]);
 console.log('todo move area ok');
}finally{await browser?.close();await new Promise(r=>server.close(r))}
