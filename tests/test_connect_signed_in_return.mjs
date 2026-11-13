import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A self-hosted Machine's sign-in (fleet.py connect_start) comes back from the account's callback to this dashboard as
// #signed-in=<source>, or #signed-in=<source>/again for an account it had: Connections opens and says it worked, the
// address is cleaned up, and anything else after #signed-in= shows nothing. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
  connectors:[{id:'work-outlook',service:'outlook',display_name:'Outlook',email:'dee@example.com',status:'ok'}]}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const runs=shots?[['light',1440,900],['light',1440,700],['light',390,844],['dark',1440,900]]:[['light',1440,900]];
 for(const [scheme,width,height] of runs){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const toast=page.locator('#toast');
  await page.goto(base+'/#signed-in=microsoft/again');
  await toast.getByText('Reconnected to Microsoft.').waitFor({timeout:8000});
  await page.locator('#health').waitFor({state:'visible'});
  assert.equal(new URL(page.url()).hash,'','the address is cleaned up');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  if(shots)await page.screenshot({path:`${shots}/signed-in-again-${width}x${height}-${scheme}.png`});
  await page.goto('about:blank');await page.goto(base+'/#signed-in=google');
  await toast.getByText('Connected to Google.').waitFor({timeout:8000});
  if(shots&&width===1440&&height===900)await page.screenshot({path:`${shots}/signed-in-first-${width}x${height}-${scheme}.png`});
  // not a source it knows: Connections, no word about anything
  await page.goto('about:blank');await page.goto(base+'/#signed-in=evil');
  await page.locator('#health').waitFor({state:'visible'});
  assert.ok(!/Connected to|Reconnected to/.test(await toast.innerText().catch(()=>'')));
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
