import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The Salesforce card, Update contact details (connectors/salesforce.py card, crm_sync.py): off, it offers Show what would
// change; that posts connector_contact_sync preview and lists the changes, with Turn on and Not now; on, it lists the
// contacts it updated, and Turn off. A connection a Fleet shares has no box. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const ago=h=>new Date(Date.now()-h*3600e3).toISOString();
const change=(field,label,nw,old)=>({field,label,new:nw,old,from:'LinkedIn'});
const sf={id:'salesforce-work',service:'salesforce',what:'Deals, tasks and activity from Salesforce, on people and projects.',email:'owner@acme.example',
 boundary:'work:Acme',last_success:ago(0.05),total:30,signals_24h:3,pending:0,crm_sync:{contact_sync:false,contact_updates:[],contact_failed:0,linkedin_field:'LinkedIn__c',can_write:true}};
const preview=[{name:'Avery Example',email:'avery@example.org',changes:[change('title','Job title','VP Sales','Sales Director')]},
 {name:'Sam Sample',email:'sam@example.net',changes:[change('phone','Phone','+32 470 00 00 00',null),change('linkedin_url','LinkedIn','https://linkedin.com/in/sam-sample',null)]}];
const state={suggestions:[],promises:[],connectors:[sf],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]};
const calls=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://x.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='connector_contact_sync'){const d=call.args.do;
   if(d==='on')sf.crm_sync={...sf.crm_sync,contact_sync:true,contact_updates:preview.map(p=>({...p,at:ago(0.1)})),contact_failed:1,contact_refused:[{name:'Robin Placeholder',why:'A rule in Salesforce refused it'}]};
   if(d==='off')sf.crm_sync={...sf.crm_sync,contact_sync:false};
   res.end(JSON.stringify({ok:true,do:d,...(d==='preview'?{changes:preview}:{}),crm:sf.crm_sync}));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const errors=[];
try{
 for(const [width,scheme] of [[1440,'light'],[390,'dark'],...(shots?[[1440,'dark'],[390,'light']]:[])]){
  sf.crm_sync={...sf.crm_sync,contact_sync:false,contact_updates:[],contact_failed:0};
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.waitForFunction(()=>typeof showTab==='function'&&document.querySelector('#connectors article'));
  await page.evaluate(()=>showTab('health','other'));
  const card=page.locator('#connectors article',{hasText:'Salesforce'}).first();
  await card.waitFor();
  const shot=async name=>{if(shots)await card.screenshot({path:`${shots}/salesforce-${name}-${width}-${scheme}.png`})};
  const inside=async()=>{const box=await card.boundingBox(),b=await card.locator('.crm-sync').boundingBox();
   assert.ok(b.x>=box.x&&b.x+b.width<=box.x+box.width+1,`${width}: the box stays inside the card`);
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${width}: no sideways scroll`)};
  // Off
  assert.match(await card.locator('.crm-sync-line').innerText(),/^Update contact details: off\./);
  await inside();await shot('off');
  // Show what would change
  await card.locator('[data-crm-sync="preview"]').click();
  await card.locator('[data-crm-sync="on"]').waitFor();
  assert.deepEqual(calls.at(-1),{action:'connector_contact_sync',args:{account:'salesforce-work',do:'preview'}});
  assert.equal(await card.locator('.crm-sync-line').innerText(),'Turning it on now changes 2 contacts:');
  assert.match(await card.locator('.crm-sync-list').innerText(),/Avery Example[\s\S]*VP Sales[\s\S]*\(was Sales Director\)/);
  await inside();await shot('preview');
  // Turn on: it lists what it updated
  await card.locator('[data-crm-sync="on"]').click();
  await card.locator('[data-crm-sync="off"]').waitFor();
  assert.equal(calls.at(-1).args.do,'on');
  assert.equal(await card.locator('.crm-sync-line').innerText(),'Updates contact details in Salesforce.');
  const refused=card.locator('.crm-sync-refused');
  assert.equal(await refused.locator('summary').innerText(),'1 contact not updated: Salesforce refused the change');
  await refused.locator('summary').click();
  assert.match(await refused.innerText(),/Robin Placeholder[\s\S]*A rule in Salesforce refused it/);
  assert.match(await card.innerText(),/30\s*updates/);
  await inside();await shot('on');
  // Turn off
  await card.locator('[data-crm-sync="off"]').click();
  await card.locator('[data-crm-sync="preview"]').waitFor();
  assert.equal(calls.at(-1).args.do,'off');
  await context.close();
 }
 // A connection a Fleet shares only reads: no box
 const context=await browser.newContext({viewport:{width:1440,height:900}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.waitForFunction(()=>typeof crmSyncBox==='function');
 assert.equal(await page.evaluate(c=>String(crmSyncBox(c)),{...sf,shared_by:'Acme'}),'');
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser.close();server.close()}
console.log('salesforce card dashboard ok');
