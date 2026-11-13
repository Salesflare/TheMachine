import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections, a card's Recent syncs and Last failure:
// - Times read like the rest of the dashboard: Today 08:18, Yesterday 21:06, in the card's own font, never "12 Nov 2026,
//   08:18" in a monospace font, and no year for this year (the Retry time too).
// - A failed sync that a later sync made up for reads calm (no error color, no stale Retry time); a failure that is
//   still the latest sync stays an error with when it retries.
// SHOTS=<folder> also saves the card at 390 and 1440 wide, light and dark.
const dashboard=await dashboardPage();
const now=new Date(),at=(days,h,m)=>{const d=new Date(now);d.setDate(d.getDate()-days);d.setHours(h,m,0,0);return d.toISOString()};
const today=now.getHours()>=9?0:1;  // a morning that has already passed today (else yesterday's)
const linkedin={id:'work-linkedin',service:'linkedin',display_name:'work-linkedin',boundary:'work:Acme',boundary_by:'owner',
 last_success:at(today,8,18),total:3,signals_24h:1,pending:0,failures_24h:4,last_failure:{at:at(today,8,3),error:'linkedin_read_timeout'},
 backfill:{back_to:'2026-08'},
 sync_activity:[{at:at(today,8,18),status:'success',signals:0},
  {at:at(today,8,3),status:'failed',error:'linkedin_read_timeout',retry_at:at(today,8,18)},
  {at:at(today,7,46),status:'failed',error:'linkedin_read_timeout',retry_at:at(today,8,1)},
  {at:at(today+1,21,6),status:'success',signals:0},{at:at(today+1,19,48),status:'failed',error:'linkedin_read_timeout',retry_at:at(today+1,20,3)},
  {at:at(today+1,19,31),status:'failed',error:'linkedin_read_timeout',retry_at:at(today+1,19,46)},{at:at(today+1,18,29),status:'success',signals:0}]};
// still failing: its latest sync failed
const x={id:'work-x',service:'x',display_name:'work-x',boundary:'work:Acme',boundary_by:'owner',last_success:at(today+1,20,0),total:12,
 error:'x_browser_busy',failures:1,failures_24h:1,last_failure:{at:at(today,8,5),error:'x_browser_busy'},
 sync_activity:[{at:at(today,8,5),status:'failed',error:'x_browser_busy',retry_at:at(today,8,20)},{at:at(today+1,20,0),status:'success',signals:2}]};
const locale={locale:'en-BE',region:'BE',language:'en',clock:'auto',hour12:false,auto_hour12:false,date_locale:'en-GB',languages:{en:'English'},saveable:true};
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://x.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[linkedin,x],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],locale}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const errors=[];
const open=async(width,scheme)=>{
 const context=await browser.newContext({viewport:{width,height:width<500?844:900},deviceScaleFactor:width<500?2:1,colorScheme:scheme,timezoneId:Intl.DateTimeFormat().resolvedOptions().timeZone||'UTC'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.waitForFunction(()=>typeof showTab==='function'&&document.querySelector('#connectors article'));
 await page.evaluate(()=>{showTab('health');cardShow('work-x');cardShow('work-linkedin')});  // their kind, both cards open
 const card=page.locator('#connectors article[data-conn="work-linkedin"]');
 await card.locator('details[id^="sync-recent"] summary').click();
 await card.locator('details[id^="sync-details"] summary').click();
 return {context,page,card}};
try{
 const {context,page,card}=await open(1440,'light');
 const recent=card.locator('details[id^="sync-recent"]'),rows=recent.locator('p');
 const text=await recent.innerText(),year=String(now.getFullYear());
 assert.equal(await rows.count(),7,text);
 assert.ok(!text.includes(year),'no year for this year: '+text);
 assert.match(await rows.nth(0).innerText(),new RegExp('^'+(today?'Yesterday':'Today')+' 08:18 · Synced, 0 new or changed$'));
 assert.equal(await recent.locator('.mono').count(),0,'times in the card font, not monospace');
 assert.equal(await recent.locator('time').first().getAttribute('datetime'),linkedin.sync_activity[0].at);
 // made up for by a later sync: calm, without its old Retry time
 for(const i of [1,2,4,5]){const row=rows.nth(i);
  assert.equal(await row.locator('.error').count(),0,await row.innerText());
  assert.doesNotMatch(await row.innerText(),/Retry/);
  assert.match(await row.innerText(),/LinkedIn was slow to answer/)}
 assert.match(await card.locator('details[id^="sync-details"]').innerText(),new RegExp('Last failure: LinkedIn was slow to answer, '+(today?'Yesterday':'Today')+' 08:03'));
 // still failing: an error, with when it retries, in the same short style
 const xcard=page.locator('#connectors article[data-conn="work-x"]');
 await xcard.locator('details[id^="sync-recent"] summary').click();
 const latest=xcard.locator('details[id^="sync-recent"] p').first();
 assert.equal(await latest.locator('.error').count(),1);
 assert.match(await latest.innerText(),new RegExp('^'+(today?'Yesterday':'Today')+' 08:05 · The browser was busy with another read · Retry '+(today?'Yesterday':'Today')+' 08:20$'));
 await context.close();
 if(process.env.SHOTS)for(const width of [390,1440])for(const scheme of ['light','dark']){
  const {context,card}=await open(width,scheme);
  await card.screenshot({path:`${process.env.SHOTS}/sync-times-${width}-${scheme}.png`});await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser.close();server.close()}
