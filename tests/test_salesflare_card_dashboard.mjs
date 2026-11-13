import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// - The Salesflare card says what it brings in (its + Add line), how far its round of accounts is (stuck after a long while), and has Stop
//   (then Start), Restart sync and a link to Salesflare's API keys; Stop posts connector_sync and the card says Stopped.
// - Relative times follow the dashboard's region, not the browser's language: a French browser still reads "3 hours ago".
// - Feedback, What you decided: the cards start on the same left edge as the sections above, at both widths.
// - What's shared, Your connections: another person's calendar read through the owner's sign-in is named for it.
// - A CRM's tiles count accounts read and emails and meetings, not messages; a key that opens no account needs help;
//   a sync that keeps failing says so calmly (amber, no Caught up); a row of empty bars isn't drawn (report s_f0d5d0200384ed92).
// - Salesflare refusing the feed for the whole team: the card says so once, with who can switch it on, not "use another key".
const dashboard=await dashboardPage();
const ago=h=>new Date(Date.now()-h*3600e3).toISOString();
const sf={id:'work-crm',service:'salesflare',what:'Accounts, contacts and deals, so it knows who matters.',email:'owner@acme.example',display_name:'CRM',boundary:'work:Acme',last_success:ago(0.05),total:12,signals_24h:2,pending:0,
 salesflare:{stopped:null,synced_until:ago(5),round:{since:ago(170),started:ago(3),accounts:42,done:12,stuck:true,failing:1},slow_accounts:2,no_access:0,keys_url:'https://app.salesflare.com/#/settings/apikeys'}};
const syncs=(n,fail)=>Array.from({length:n},(_,i)=>({at:ago(i*0.1),status:fail&&i===fail?'failed':'success',signals:0,error:fail&&i===fail?'salesflare:HTTP_504':null}));
const locked={...sf,id:'crm-locked',display_name:'CRM locked',total:0,signals_24h:0,last_sync_signals:0,sync_activity:syncs(12),failures_24h:0,
 salesflare:{stopped:null,synced_until:ago(1),round:null,last_round:{accounts:128,read:0,no_access:128,refused:128,set_aside:0},no_access_all:true,slow_accounts:0,no_access:128,keys_url:sf.salesflare.keys_url}};
const teamOff={...locked,id:'crm-team-off',display_name:'CRM team off',
 salesflare:{...locked.salesflare,last_round:{accounts:14,read:0,no_access:14,refused:14,set_aside:0},no_access_all:false,feed_off:true,no_access:14}};
const flaky={...sf,id:'crm-flaky',display_name:'CRM flaky',total:340,signals_24h:9,sync_activity:syncs(12,3),failures_24h:35,last_failure:{at:ago(0.3),error:'salesflare:HTTP_504'},
 salesflare:{stopped:null,synced_until:ago(1),round:null,last_round:{accounts:128,read:126,no_access:2,refused:2,set_aside:0},no_access_all:false,slow_accounts:0,no_access:2,keys_url:sf.salesflare.keys_url}};
const decisions=[1,2,3].map(i=>({suggestion_id:'c'+i,choice:'complete',source:'dashboard',created_at:ago(i)}));
const state={suggestions:[1,2,3].map(i=>({id:'c'+i,title:'To-do '+i,body:'Made-up.',status:'completed',scope:'work',created_at:ago(i)})),promises:[],connectors:[sf,locked,teamOff,flaky],suggestion_counts:{},decisions,analyses:[],deliveries:[],
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
  await page.evaluate(()=>{showTab('health','other');for(const a of document.querySelectorAll('#connectors>article:not([hidden])'))cardShow(a.dataset.conn)});  // Other, each card open
  const card=page.locator('#connectors article[data-conn="work-crm"]');
  await card.waitFor().catch(async e=>{throw await why(e)});
  assert.equal(await card.locator('.conn-what').innerText(),'Accounts, contacts and deals, so it knows who matters.');
  assert.match(await card.locator('.sf-line').innerText(),/^Checked 12 of 42 accounts so far\. Started 3 hours ago, may be stuck\.$/);
  // Kris's card: no account opens. Tiles fit a CRM, no empty bars, Needs your help with the way out, not Caught up
  const lk=page.locator('#connectors article[data-conn="crm-locked"]');
  assert.deepEqual(await lk.locator('.figures span').allInnerTexts(),['accounts read','emails and meetings','last 24h']);
  assert.deepEqual(await lk.locator('.figures b').allInnerTexts(),['0','0','0']);
  assert.equal(await lk.locator('.spark').count(),0);
  assert.equal(await lk.locator('.connection-status').innerText(),'Needs your help');
  assert.match(await lk.locator('.sf-locked').innerText(),/^Salesflare doesn’t let this API key open these accounts\. Use the key of a user who can see them\.$/);
  assert.equal(await lk.locator('.sf-aside').count(),0);
  assert.doesNotMatch(await lk.locator('.conn-plain').allInnerTexts().then(x=>x.join(' ')),/Caught up/);
  // The team's feed is off at Salesflare: Needs your help, who can switch it on, no count of accounts, no other key
  const off=page.locator('#connectors article[data-conn="crm-team-off"]');
  assert.equal(await off.locator('.connection-status').innerText(),'Needs your help');
  assert.equal(await off.locator('.sf-feed-off').innerText(),'Salesflare hasn’t switched on feed access for API keys for your team, so no emails or meetings come in. Salesflare support can switch it on.');
  assert.equal(await off.locator('.alert').count(),1);
  assert.equal(await off.locator('.sf-locked').count()+await off.locator('.sf-aside').count(),0);
  assert.doesNotMatch(await off.locator('.conn-plain').allInnerTexts().then(x=>x.join(' ')),/Caught up/);
  const offBox=await off.boundingBox(),offNote=await off.locator('.sf-feed-off').boundingBox();
  assert.ok(offNote.x>=offBox.x&&offNote.x+offNote.width<=offBox.x+offBox.width+1,`${width}: the note stays inside the card`);
  // A CRM that keeps failing but gets through: amber and calm, plain words under Details
  const fl=page.locator('#connectors article[data-conn="crm-flaky"]');
  assert.equal(await fl.locator('.connection-status').innerText(),'Connected · Salesflare CRM is slow at times');
  assert.ok(await fl.locator('.state-dot.t-amber').count());
  assert.deepEqual(await fl.locator('.figures b').allInnerTexts(),['126','340','9']);
  assert.equal(await fl.locator('.spark').count(),1);
  assert.equal(await fl.locator('.sf-aside').innerText(),'2 without access');
  const details=await fl.locator('[id^="sync-details-"]').evaluate(d=>{d.open=true;return d.innerText});
  assert.match(details,/35 failed syncs in the last 24 hours\. The last sync worked\./);
  assert.doesNotMatch(details,/Old failures|Caught up/);
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
  // Learning: How it's going and Decisions line up with the tabs above them
  await navClick(page.locator('nav [data-tab="feedback"]'));
  await page.locator('#learn-tab-decisions').click();await page.locator('#decisions article').first().waitFor();
  const edge=await page.evaluate(()=>{const l=e=>Math.round(e.getBoundingClientRect().left);return {head:l(document.querySelector('#learn-tabs')),card:l(document.querySelector('#decisions article'))}});
  await page.locator('#learn-tab-going').click();
  const quality=await page.evaluate(()=>Math.round(document.querySelector('#quality').firstElementChild.getBoundingClientRect().left));
  assert.equal(edge.card,edge.head,`${width}: ${JSON.stringify(edge)}`);assert.equal(quality,edge.head,`${width}: ${JSON.stringify({...edge,quality})}`);
  // Your connections: a partner's calendar is named for it, the owner's own keeps its address
  const html=await page.evaluate(()=>String(sharedHTML({id:'fl',name:'Acme'},{connections:[{id:'w',service:'calendar',email:'owner@acme.example',name:'',company:true,required:true,on:true},
   {id:'p',service:'calendar',email:'owner@acme.example',name:'Robin’s calendar',personal:true}]},{sorted:{},unsorted:0,sent:0,unsure:[],rules:[],records:[],by_hand:[],shared:[],threads:[],waiting:[]})));
  assert.match(html,/Google Calendar · owner@acme\.example<\/span><small class="muted">Required by Acme/);
  assert.match(html,/Google Calendar · Robin’s calendar<\/span><small class="muted">Personal, never shared/);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser.close();server.close()}
console.log('salesflare card dashboard ok');
