import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections, Other sources: The Machine's own log reads as Machine health, last in the tab, with no internal names on
// its card (no OpenClaw, no gateway, no owner:system line, no account id) and still its counts and Details. Another
// source keeps its kind and Work or personal under its name. SHOTS=<folder> saves each width.
const dashboard=await dashboardPage();
const at=new Date().toISOString();
const card=(id,service,display_name,boundary,more)=>({id,service,email:'',display_name,boundary,last_success:at,last_sync_signals:2,sync_activity:[],failures_24h:0,read_window:{},total:40,signals_24h:3,pending:1,...more});
const connectors=[card('openclaw-gateway','gateway','Machine health','owner:system',{what:'Your Machine’s own log, so it spots its own trouble.'}),
 card('news','rss','Product news','work:Acme',{what:'Posts from the feeds you follow.'})];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,mobile] of [[1440,900,false],[1440,700,false],[390,844,true]]){
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#connections');
  const health=page.locator('#connectors article[data-conn="openclaw-gateway"]');await health.waitFor();await page.waitForTimeout(300);
  assert.deepEqual(await page.locator('#connectors article:not([hidden])').evaluateAll(a=>a.map(x=>x.dataset.conn)),['news','openclaw-gateway'],'Machine health comes last');
  assert.equal(await health.locator('h3').innerText(),'Machine health');
  assert.equal(await health.locator('.conn-head small').count(),0,'no kind or owner line under it');
  const text=await health.innerText();
  assert.doesNotMatch(text,/openclaw|gateway|owner:|system/i,text);
  assert.deepEqual(await health.locator('.figures span').allInnerTexts(),['alerts','last 24h','not checked']);
  assert.equal(await health.locator('details summary').filter({hasText:'Details'}).count(),1);
  assert.equal(await page.locator('#connectors article[data-conn="news"] .conn-head small').innerText(),'Feed · Work · Acme');
  if(shots){await health.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/after-${width}x${height}.png`})}
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('connections machine health dashboard ok');
