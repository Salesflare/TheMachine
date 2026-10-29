import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add, after a source is added (renderConnectRun, connectFollow):
// - While it runs, the pane offers Cancel (not Stop, which on a Salesflare card means stop syncing).
// - Done: the pane says it restarts, waits while the service is away, and once it answers with the new account it moves
//   to that account's card, marked for a moment; the card says what it does before its first sync. Back on + Add the pane
//   says the card shows how far it is, with Open its card.
// - Details on a card are plain lines, never the raw saved state; Recent syncs and the Details lines read in Dutch.
// - Work or personal: "Guessed" only for an account The Machine marked as a guess (boundary_by guess), never for one
//   from before that mark.
const dashboard=await dashboardPage();
const nl=await readFile(new URL('../i18n/nl.json',import.meta.url),'utf8');
const ago=h=>new Date(Date.now()-h*3600e3).toISOString();
const crm={id:'work-crm',service:'salesflare',email:'owner@acme.example',display_name:'CRM',boundary:'work:Acme',boundary_by:'owner',total:0,
 salesflare:{stopped:null,round:null,slow_accounts:0,no_access:0,keys_url:'https://app.salesflare.com/#/settings/apikeys'}};
const mail={id:'work-gmail',service:'gmail',email:'owner@acme.example',boundary:'work:Acme',last_success:ago(0.05),total:40,
 state:JSON.stringify({mode:'incremental',history_id:'991',after:1790966948}),failures_24h:1,last_failure:{at:ago(5),error:'timeout'},
 sync_activity:[{at:ago(0.05),status:'success',signals:3},{at:ago(5),status:'failed',error:'timeout'}]};
const phone={id:'personal-whatsapp',service:'whatsapp',boundary:'personal:whatsapp',last_success:ago(0.1)};  // linked before boundary_by existed
const guessed={id:'home-cal',service:'calendar',email:'me@example.com',boundary:'personal:me',boundary_by:'guess',last_success:ago(0.1)};
const locale=language=>({locale:'en-BE',region:'BE',language,clock:'auto',hour12:false,auto_hour12:false,date_locale:'en-GB',languages:{en:'English',nl:'Nederlands'},saveable:true});
let connectors=[mail,phone,guessed],away=0,polls=0,language='en';
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://x.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/nl.json'){res.end(nl);return}
 if(url.pathname==='/api/status'){if(away>0){away--;res.statusCode=502;res.end('{}');return}
  res.end(JSON.stringify({suggestions:[],promises:[],connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],locale:locale(language)}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,sources:[{name:'salesflare',label:'Salesflare',service:'salesflare',what:'Accounts, contacts, emails and meetings'}]}));return}
  if(action==='connect_start'){res.end(JSON.stringify({session:'s1',state:'running',label:'Salesflare',lines:['Checking the API key']}));return}
  if(action==='connect_poll'){polls++;if(polls<3){res.end(JSON.stringify({state:'running',lines:['Checking the API key']}));return}
   away=2;setTimeout(()=>{connectors=[...connectors,crm]},4000);  // the restart: away for a moment, then back with the new account
   res.end(JSON.stringify({state:'done',lines:['Checking the API key','Connected to Salesflare'],account:'work-crm',restarting:true}));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const errors=[];
try{
 const context=await browser.newContext({viewport:{width:1440,height:900},timezoneId:'Europe/Brussels'}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.waitForFunction(()=>typeof showTab==='function'&&document.querySelector('#connectors article'));
 await page.evaluate(()=>showTab('health'));
 // Details: plain lines, no raw state
 await page.evaluate(()=>showHealthPane('mail'));
 const gmail=page.locator('#connectors article[data-conn="work-gmail"]');
 await gmail.locator('details[id^="sync-details"] summary').click();
 const details=await gmail.locator('details[id^="sync-details"]').innerText();
 assert.doesNotMatch(details,/history_id|\{"|mode/,details);
 assert.equal(await gmail.locator('details[id^="sync-details"] pre').count(),0);
 assert.match(details,/Caught up\. Checks for new items every few minutes\./);
 assert.match(details,/1 failed sync in the last 24 hours\./);
 assert.match(details,/Last failure: Connection timed out, /);
 await gmail.locator('details[id^="sync-recent"] summary').click();
 assert.match(await gmail.locator('details[id^="sync-recent"]').innerText(),/Synced, 3 new or changed/);
 // Guessed only when marked a guess
 await page.evaluate(()=>showHealthPane('chat'));
 assert.doesNotMatch(await page.locator('#connectors article[data-conn="personal-whatsapp"]').innerHTML(),/Guessed/);
 await page.evaluate(()=>showHealthPane('mail'));
 assert.match(await page.locator('#connectors article[data-conn="home-cal"]').innerHTML(),/Guessed\. Pick one to be sure\./);
 // + Add Salesflare: Cancel while running, then the restart, then its card
 await page.evaluate(()=>showHealthPane('add'));
 await page.locator('#connect-add [data-connect="salesflare"]').click();
 await page.locator('#connect-add [data-connect-stop]').waitFor();
 assert.equal(await page.locator('#connect-add [data-connect-stop]').innerText(),'Cancel');
 await page.locator('#connect-add .sent-ok',{hasText:'Restarting to start reading it…'}).waitFor({timeout:8000});
 await page.locator('#connectors article[data-conn="work-crm"].conn-new').waitFor({timeout:20000});
 assert.equal(await page.evaluate(()=>healthPane),'other');
 const card=page.locator('#connectors article[data-conn="work-crm"]');
 assert.ok(await card.isVisible());
 assert.equal(await card.locator('.connection-status').innerText(),'Waiting for first sync');
 assert.equal(await card.locator('.sf-line').innerText(),'Finding the accounts with recent emails and meetings…');
 await card.locator('details[id^="sync-details"] summary').click();
 assert.match(await card.locator('details[id^="sync-details"]').innerText(),/Waiting for the first sync\. It starts within a few minutes\./);
 await page.evaluate(()=>showHealthPane('add'));
 assert.match(await page.locator('#connect-add .sent-ok').innerText(),/^Connected\. Running again\. Its card shows how far it is\.$/);
 await page.locator('#connect-add [data-connect-card]').click();
 assert.equal(await page.evaluate(()=>healthPane),'other');
 // Dutch: Recent syncs and Details lines
 language='nl';await page.reload();await page.waitForFunction(()=>document.documentElement.lang==='nl'&&document.querySelector('#connectors article'));
 await page.evaluate(()=>{showTab('health');showHealthPane('mail')});
 for(const id of ['sync-recent-work-gmail','sync-details-work-gmail'])await page.locator('#'+id+' summary').click();
 const dutch=await page.locator('#connectors article[data-conn="work-gmail"] .conn-more').innerText();
 for(const en of ['Synced, 3 new or changed','failed sync in the last 24 hours','Caught up','Last failure'])assert.ok(!dutch.includes(en),`${en} reads in Dutch: ${dutch}`);
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser.close();server.close()}
console.log('connect follow dashboard ok');
