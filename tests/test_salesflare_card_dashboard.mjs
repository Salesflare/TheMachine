import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// - The Salesflare card says what it brings in (its + Add line), how far its round of accounts is (stuck after a long while), and has Stop
//   (then Start), Restart sync and a link to Salesflare's API keys; Stop posts connector_sync and the card says Stopped.
// - Relative times follow the dashboard's region, not the browser's language: a French browser still reads "3 hours ago".
// - Feedback, What you decided: the cards start on the same left edge as the sections above, at both widths.
// - What's shared, Your connections: another person's calendar read through the owner's sign-in is named for it.
const dashboard=await dashboardPage();
const ago=h=>new Date(Date.now()-h*3600e3).toISOString();
const sf={id:'work-crm',service:'salesflare',what:'Accounts, contacts and deals, so it knows who matters.',email:'owner@acme.example',display_name:'CRM',boundary:'work:Acme',last_success:ago(0.05),total:12,signals_24h:2,pending:0,
 salesflare:{stopped:null,synced_until:ago(5),round:{since:ago(170),started:ago(3),accounts:42,done:12,stuck:true,failing:1},slow_accounts:2,no_access:0,keys_url:'https://app.salesflare.com/#/settings/apikeys'}};
const decisions=[1,2,3].map(i=>({suggestion_id:'c'+i,choice:'complete',source:'dashboard',created_at:ago(i)}));
const state={suggestions:[1,2,3].map(i=>({id:'c'+i,title:'To-do '+i,body:'Made-up.',status:'completed',scope:'work',created_at:ago(i)})),promises:[],connectors:[sf],suggestion_counts:{},decisions,analyses:[],deliveries:[],
 review_health:{},review_runs:[],locale:{locale:'en-BE',region:'BE',language:'en',clock:'auto',hour12:false,auto_hour12:false,date_locale:'en-GB',languages:{en:'English'},saveable:true}};
const calls=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://x.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='connector_sync'){sf.salesflare={...sf.salesflare,stopped:call.args.do==='stop'?new Date().toISOString():null};res.end(JSON.stringify({ok:true}));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const errors=[];
try{
 for(const width of [1440,390]){
  sf.salesflare.stopped=null;
  const context=await browser.newContext({viewport:{width,height:900},locale:'fr-FR',timezoneId:'Europe/Brussels'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));const logged=[];page.on('console',m=>{if(m.type()==='error'&&!/font|OTS|MIME|Manifest|Failed to load resource/i.test(m.text()))logged.push(m.text())});
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.waitForFunction(()=>typeof DL==='string'&&DL==='en-GB');
  assert.equal(await page.evaluate(h=>ago(new Date(Date.now()-h*3600e3).toISOString()),3),'3 hours ago');
  assert.equal(await page.evaluate(()=>ago(new Date(Date.now()+864e5*2).toISOString())),'in 2 days');
  // The Salesflare card
  // When this times out on CI the first refresh failed to draw; say what the page said, so the next failure names its cause
  const why=async e=>new Error(`${width}: ${e.message}\npage errors: ${JSON.stringify(errors)}\nconsole errors: ${JSON.stringify(logged)}\npage: ${await page.evaluate(()=>JSON.stringify({notice:document.querySelector('#notice')?.textContent,refreshFailed,tab:document.querySelector('main>section:not([hidden])')?.id,healthPane,connectors:document.querySelectorAll('#connectors article').length})).catch(x=>x.message)}`);
  await page.waitForFunction(()=>typeof showTab==='function'&&document.querySelector('#connectors article')).catch(async e=>{throw await why(e)});
  await page.evaluate(()=>showTab('health','other'));
  const card=page.locator('#connectors article',{hasText:'Salesflare CRM'});
  await card.waitFor().catch(async e=>{throw await why(e)});
  assert.equal(await card.locator('.conn-what').innerText(),'Accounts, contacts and deals, so it knows who matters.');
  assert.match(await card.locator('.sf-line').innerText(),/^Reading 12 of 42 accounts\. Started 3 hours ago, may be stuck\.$/);
  assert.equal(await card.locator('.sf-aside').innerText(),'2 skipped as too slow');
  assert.equal(await card.locator('a.head-link').getAttribute('href'),'https://app.salesflare.com/#/settings/apikeys');
  assert.equal(await card.locator('a.head-link').getAttribute('target'),'_blank');
  const box=await card.boundingBox(),acts=await card.locator('.sf-actions').boundingBox();
  assert.ok(acts.x>=box.x&&acts.x+acts.width<=box.x+box.width+1,`${width}: the buttons stay inside the card`);
  await card.locator('[data-sf-sync="stop"]').click();
  await card.locator('[data-sf-sync="start"]').waitFor();
  assert.deepEqual(calls.at(-1),{action:'connector_sync',args:{account:'work-crm',do:'stop'}});
  assert.equal(await card.locator('.connection-status').innerText(),'Stopped');
  page.once('dialog',d=>d.dismiss());await card.locator('[data-sf-sync="restart"]').click();  // Restart asks first
  await page.waitForTimeout(200);assert.equal(calls.at(-1).args.do,'stop');
  // Feedback: the decisions line up with the sections above
  await navClick(page.locator('nav [data-tab="feedback"]'));
  await page.locator('#decisions article').first().waitFor();
  const edge=await page.evaluate(()=>{const l=e=>Math.round(e.getBoundingClientRect().left);return {head:l(document.querySelector('#feedback .section-head h2')),card:l(document.querySelector('#decisions article')),quality:l(document.querySelector('#quality').firstElementChild)}});
  assert.equal(edge.card,edge.head,`${width}: ${JSON.stringify(edge)}`);assert.equal(edge.quality,edge.head,`${width}: ${JSON.stringify(edge)}`);
  // Your connections: a partner's calendar is named for it, the owner's own keeps its address
  const html=await page.evaluate(()=>sharedHTML({id:'fl',name:'Acme'},{connections:[{id:'w',service:'calendar',email:'owner@acme.example',name:'',company:true,required:true,on:true},
   {id:'p',service:'calendar',email:'owner@acme.example',name:'Robin’s calendar',personal:true}]},{sorted:{},unsorted:0,sent:0,unsure:[],rules:[],records:[],by_hand:[],shared:[],threads:[],waiting:[]}));
  assert.match(html,/Google Calendar · owner@acme\.example<\/span><small class="muted">Required by Acme/);
  assert.match(html,/Google Calendar · Robin’s calendar<\/span><small class="muted">Personal, never shared/);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser.close();server.close()}
console.log('salesflare card dashboard ok');
