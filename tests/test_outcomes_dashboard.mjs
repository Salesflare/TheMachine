import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Done when (machine/store/outcomes.py): the result that closes a to-do is one row under its Details, never a line on the
// to-do itself (its title says it already). One waiting for that result after a Send sits under Waiting on others.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[
 {id:'o1',title:'Get the order form signed',body:'Sam asked for the order form.',status:'pending',scope:'work',created_at:now,event_ids:[1],done_when:'Sam signed the order form'},
 {id:'o2',title:'Book the venue',body:'Done when the venue confirms the booking.',status:'pending',scope:'work',created_at:now,event_ids:[2],done_when:'the venue confirms the booking'},
 {id:'o3',title:'Chase the quote',body:'Sent the request to Sam.',status:'prepared',scope:'work',created_at:now,event_ids:[3],done_when:'Sam sent the quote',
  outcome:JSON.stringify({state:'waiting',waiting_on:'Sam',until:new Date(Date.now()+2*864e5).toISOString()})},
 {id:'o4',title:'Send the contract',body:'Sent.',status:'completed',scope:'work',created_at:now,closed_at:now,event_ids:[4],done_when:'Alex signed the contract'}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  const context=await browser.newContext({viewport:{width,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-o1').waitFor();
  const row=id=>page.locator('#task-'+id+' .card-fields div').filter({hasText:'Done when'});
  for(const id of ['o1','o2','o3','o4'])assert.equal(await page.locator('#task-'+id+' > p').filter({hasText:/Done when/}).count(),0,id);  // not on the face
  assert.equal(await row('o1').locator('dd').textContent(),'Sam signed the order form');
  assert.equal(await page.locator('#details-o1').isHidden(),true);  // folded until Details opens
  // Waiting for its result after the Send: under Waiting on others, the row under its Details
  assert.equal(await page.locator('#waiting-list #task-o3').count(),1);
  assert.equal(await row('o3').locator('dd').textContent(),'Sam sent the quote');
  if(process.env.OUTCOMES_SHOT){await page.locator('#waiting-list').evaluate(d=>{d.open=true});await page.locator('#task-o1 .details-toggle').click();await page.locator('#details-o1').waitFor();
   for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});await page.waitForTimeout(400);await page.screenshot({path:`${process.env.OUTCOMES_SHOT}/done-when-${width}-${scheme}.png`,fullPage:width===390})}}
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
