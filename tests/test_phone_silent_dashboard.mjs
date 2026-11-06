import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The notification feed answers while the phone is offline: the server marks the phone card android_offline with
// silent_since (assistant.py silent_failure). The card says "Phone disconnected" with its fix, and Needs you says what to
// do, not "sign in again". Another source that goes silent while failing reads as reconnecting. SHOTS=<dir> saves shots.
const dashboard=await dashboardPage();
const hour=3600e3,ago=h=>new Date(Date.now()-h*hour).toISOString();
const connectors=[
 {id:'phone',service:'android',boundary:'personal',display_name:'Pixel',poll_seconds:15,last_success:ago(0.01),error:'android_offline',silent_since:ago(40),total:5000,signals_24h:0,state:JSON.stringify({transport:'existing_feed_with_reconciliation',reconciliation_error:'android_offline'}),
  sync_activity:[{at:ago(0.01),status:'success',signals:0},{at:ago(0.1),status:'failed',error:'android_offline'},{at:ago(0.2),status:'success',signals:0}]},
 {id:'feed',service:'rss',boundary:'work',display_name:'News',poll_seconds:300,last_success:ago(0.05),error:'timeout',silent_since:ago(6),total:900,signals_24h:3},
 {id:'gh',service:'github',boundary:'work',display_name:'GitHub',poll_seconds:600,last_success:ago(0.05),total:40}];
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],connectors}));return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of process.env.SHOTS?[[1440,900,'light'],[1440,700,'dark'],[390,844,'light']]:[[1440,900,'light']]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#badge-health').filter({hasText:/\d/}).waitFor({state:'attached'});
  assert.equal(await page.locator('#badge-health').textContent(),'1');  // the phone needs the owner
  const needs=(await page.locator('#needs-you').textContent());
  assert.match(needs,/Pixel is not connected\. Open the OpenClaw app on it\./);
  assert.doesNotMatch(needs,/sign in/i);
  await page.evaluate(()=>{const b=document.querySelector('nav [data-tab="health"]');if(typeof drawerOpen==='function'&&!b.checkVisibility())drawerOpen();b.click()});
  const card=name=>page.locator('#connectors article',{hasText:name});
  await page.locator('#health-tabs [data-health-pane="other"]').click();
  assert.equal((await card('News').locator('.connection-status').textContent()).trim(),'Reconnecting automatically');  // silent while failing: not green
  assert.match(await card('News').locator('.alert').textContent(),/Nothing new since/);
  assert.equal((await card('GitHub').locator('.connection-status').textContent()).trim(),'Connected');
  assert.equal((await card('Pixel').locator('.connection-status').textContent()).trim(),'Phone disconnected');
  assert.equal(await card('Pixel').locator('.state-dot.t-orange').count(),1);
  const alert=(await card('Pixel').locator('.alert').textContent()).trim();
  assert.match(alert,/^Nothing new since .+\. Open the OpenClaw app on the phone\.$/);
  assert.doesNotMatch(await card('Pixel').locator('.note').first().textContent(),/Last phone check/);  // said once, in the alert
  for(const name of ['Pixel','News'])assert.doesNotMatch(await card(name).textContent(),/Last sync|Not synced yet/,name);  // silent: no "just now" next to the warning
  assert.match(await card('GitHub').textContent(),/Last sync/);
  if(process.env.SHOTS){await card('Pixel').scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.SHOTS}/phone-silent-${width}x${height}-${scheme}.png`})}
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({page_errors:errors}));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r))}
