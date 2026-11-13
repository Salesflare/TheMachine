import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The AI's real check (model_check.py) before the first look: while it hasn't answered, the first look says it starts
// once the AI answers a short test; when it failed, one short line and the provider's own error behind Details. On a
// hosted Machine the needs-you line sends the owner back to the AI step. Made-up fixtures, nothing sent.
const dashboard=await dashboardPage(),shots=process.env.FIRST_LOOK_AI_CHECK_SHOTS;
const FAILED='Your AI didn’t answer a short test. Sign in again or use another AI.',WAITS='It starts once your AI answers a short test.';
const ERROR='401 Unauthorized: OAuth token has expired. Run claude login.',manage='https://example.invalid/setup';
let look=null,hosted=false;
const live=()=>({runs:[],queue:null,first_look:look});
const state=()=>({suggestions:[],promises:[],connectors:[{id:'work',display_name:'Work mail',service:'gmail'}],suggestion_counts:{},decisions:[],
 analyses:[],deliveries:[],review_health:{},review_runs:[],reviews_on:false,review_live:live(),first_look_done:null,...(hosted?{manage_url:manage}:{})});
const errors=[];
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/reviews/live'){res.end(JSON.stringify(live()));return}
 if(url.pathname==='/api/action'){res.end(JSON.stringify({sources:[]}));return}
 if(shots&&/^\/brand\/[\w.-]+\.(webp|png)$/.test(url.pathname)){readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url)).then(b=>{res.setHeader('Content-Type','image/'+url.pathname.split('.').pop());res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const sizes=shots?[[390,844],[1440,900]]:[[390,844]],schemes=shots?['light','dark']:['light'];
 for(const [width,height] of sizes)for(const colorScheme of schemes){
  hosted=false;look={state:'waiting',why:'model_check',days:7,quick:true,hours:168};
  const context=await browser.newContext({viewport:{width,height},colorScheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const empty=()=>page.locator('#suggestions .first-look-empty').innerText();
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.waitForFunction(k=>document.querySelector('#suggestions .first-look-empty')?.textContent.includes(k),WAITS);
  assert.equal(await page.locator('#suggestions .fl-detail').count(),0);  // nothing failed yet
  // The check failed: the short line, the provider's own words folded under Details
  look={...look,error:ERROR,checked_at:new Date().toISOString()};await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(k=>document.querySelector('#suggestions .first-look-empty')?.textContent.includes(k),FAILED);
  assert.ok(!(await empty()).includes(WAITS));
  const detail=page.locator('#suggestions .fl-detail');
  assert.equal(await detail.locator('summary').innerText(),'Details');
  assert.equal(await detail.locator('p').isVisible(),false);
  await detail.locator('summary').click();
  assert.equal(await detail.locator('p').innerText(),ERROR);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(shots)await page.screenshot({path:`${shots}/dashboard-failed-${width}-${colorScheme}.png`});
  // Hosted: back to the AI step on the setup page, where the same error shows
  hosted=true;await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(k=>document.querySelector('#needs-you')?.textContent.includes(k),FAILED);
  assert.equal(await page.locator('#needs-you a',{hasText:'Pick your AI'}).getAttribute('href'),manage+'#model');
  await page.waitForFunction(k=>document.querySelector('#suggestions .first-look-empty')?.textContent.includes(k),WAITS);  // said once, up top
  assert.equal(await page.locator('#suggestions .fl-detail').count(),1);
  if(shots)await page.screenshot({path:`${shots}/dashboard-hosted-${width}-${colorScheme}.png`});
  // It answered (signed in again): the first look is due
  hosted=false;look={state:'due',days:7,quick:true,hours:168};await page.evaluate(async()=>{await refresh()});
  await page.waitForFunction(()=>/Starting now/.test(document.querySelector('#suggestions .first-look-empty')?.textContent||''));
  assert.equal(await page.locator('#suggestions .fl-detail').count(),0);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('first look ai check dashboard ok');
