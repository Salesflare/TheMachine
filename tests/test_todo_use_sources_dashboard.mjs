import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdir} from 'node:fs/promises';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A run stuck on messages from another area (preparation_blocked use_event_ids, Store.use_sources): never a dead Stuck.
// The to-do says in one line what is blocked and leads with the one tap that unblocks it, "Use this email for this
// to-do" (these emails, this message); the tap posts card_use_sources, the toast says what was added and the to-do
// carries on (Preparing). A run stuck on something else keeps Stuck and Try again.
// SHOT_DIR=<folder> saves the asking to-do at 390 and 1280, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const fresh=()=>[
 {id:'c3c3c3c3c3c3c3c3',title:'Pay the vendor for the meal vouchers',status:'accepted',scope:'personal',area:'personal',created_at:now,event_ids:[1],
  body:'The vendor needs **$210.88** before it releases the meal vouchers.',preparation_status:'blocked',
  preparation_reason:"Last month's invoice is in your other company's mailbox.",preparation_no_questions:true,preparation_questions:[],
  preparation_use:{n:1,mail:true}},
 {id:'d4d4d4d4d4d4d4d4',title:'Renew the parking permit',status:'accepted',scope:'personal',area:'personal',created_at:now,event_ids:[2],
  body:'The permit runs out on Friday.',preparation_status:'blocked',preparation_reason:'The city portal is down.',
  preparation_no_questions:true,preparation_questions:[]}];
let cards,posts;
const reset=()=>{cards=fresh();posts=[]};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,areas:[{id:'personal',label:'Personal'},{id:'work:Acme',label:'Work',name:'Acme'}],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/action'){const {action,args}=JSON.parse(body||'{}');if(action==='card_use_sources'){posts.push(args);const c=cards.find(x=>x.id===args.suggestion_id);
   Object.assign(c,{preparation_status:'queued',preparation_use:null,preparation_reason:null});
   res.end(JSON.stringify({id:c.id,line:'Added the email to this to-do',resumed:true}));return}}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOT_DIR;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const [width,height] of [[390,844],[1280,900]]){
  reset();
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  const asked=page.locator('#task-c3c3c3c3c3c3c3c3');await asked.waitFor();
  // What is blocked in one line, and the tap that unblocks it leads: Needs your help, not Stuck
  const lead=asked.locator('.actions > button.primary').first();
  assert.equal(await lead.textContent(),'Use this email for this to-do');
  const text=await asked.innerText();
  assert.match(text,/Needs your help/);assert.doesNotMatch(text,/Stuck/);
  assert.match(text,/Last month's invoice is in your other company's mailbox\./);
  if(shots){await page.waitForTimeout(300);await asked.screenshot({path:`${shots}/use-email-${width}-${scheme}.png`})}
  // Stuck on something else: Stuck with Try again, as before
  const other=page.locator('#task-d4d4d4d4d4d4d4d4');
  assert.match(await other.innerText(),/Stuck/);
  assert.equal(await other.locator('.actions > button.primary').first().textContent(),'Try again');
  await lead.click();
  await page.locator('#toast.show').waitFor();
  assert.equal((await page.locator('#toast').innerText()).trim(),'Added the email to this to-do');  // no "You"
  assert.equal(posts.length,1);assert.equal(posts[0].suggestion_id,'c3c3c3c3c3c3c3c3');assert.match(posts[0].decision_id,/^[0-9a-f-]{36}$/);
  await page.waitForFunction(()=>/Preparing/.test(document.querySelector('#task-c3c3c3c3c3c3c3c3')?.innerText||''));
  // Several messages, or not email: the button says so
  cards[0]={...fresh()[0],id:'e5e5e5e5e5e5e5e5',preparation_use:{n:2,mail:false}};
  await page.evaluate(()=>refresh());
  await page.locator('#task-e5e5e5e5e5e5e5e5').waitFor();
  assert.equal(await page.locator('#task-e5e5e5e5e5e5e5e5 .actions > button.primary').first().textContent(),'Use these messages for this to-do');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('use sources dashboard: ok');
}finally{await browser?.close();server.close()}
