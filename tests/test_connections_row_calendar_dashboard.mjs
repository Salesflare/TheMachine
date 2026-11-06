import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections on a hosted Machine. The row under the cards: Connect Google, Connect Microsoft and Add another source are
// whole pills (never split over two lines) and the ask for a missing source is its own line under them. A calendar's
// card counts events (kept, next 7 days, last 24h), never messages or "not checked".
// SHOTS=<folder> saves each width and theme.
const dashboard=await dashboardPage();
const at=new Date().toISOString();
const card=(id,service,email,more)=>({id,service,email,display_name:email,boundary:'personal',last_success:at,last_sync_signals:2,sync_activity:[],failures_24h:0,read_window:{},...more});
const connectors=[card('mail','gmail','sam@example.org',{total:1240,signals_24h:18,pending:3}),
 card('cal','outlook_calendar','sam@example.org',{total:52,signals_24h:4,pending:2,upcoming_7d:9}),
 card('gcal','calendar','alex@example.org',{total:31,signals_24h:1,pending:0,upcoming_7d:6})];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],manage_url:'https://app.example.org/account'}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,mobile] of [[360,780,true],[390,844,true],[450,900,true],[1440,900,false]])for(const scheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}-${scheme}`;
  await page.goto(base+'/#connections');
  await page.locator('#connect-more a.manage').first().waitFor();await page.waitForTimeout(300);
  const row=await page.evaluate(()=>{const more=document.querySelector('#connect-more');
   const pills=[...more.querySelectorAll('a.manage')].map(a=>({text:a.textContent,lines:a.getClientRects().length,h:a.getBoundingClientRect().height,bottom:a.getBoundingClientRect().bottom,right:a.getBoundingClientRect().right}));
   const ask=more.querySelector('.connect-ask'),r=ask?.getBoundingClientRect();
   return {pills,ask:ask&&{text:ask.textContent,top:r.top,lines:ask.getClientRects().length},width:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth}});
  assert.deepEqual(row.pills.map(p=>p.text),['Connect Google','Connect Microsoft','Add another source'],tag);
  for(const p of row.pills){assert.equal(p.lines,1,`${tag}: "${p.text}" is one box`);assert.ok(p.h<40,`${tag}: "${p.text}" is one line (${p.h}px)`);assert.ok(p.right<=row.width,`${tag}: "${p.text}" fits`)}
  assert.equal(row.ask?.text,'Missing a source? Ask for it.',tag);
  assert.ok(row.ask.top>=Math.max(...row.pills.map(p=>p.bottom)),`${tag}: the ask is under the pills`);
  assert.ok(row.scroll<=row.width,`${tag}: no sideways scroll (${row.scroll} > ${row.width})`);
  const tiles=await page.evaluate(()=>Object.fromEntries([...document.querySelectorAll('#connectors article[data-conn]')].map(a=>[a.dataset.conn,[...a.querySelectorAll('.figures div')].map(d=>d.textContent.trim().replace(/\s+/,' '))])));
  assert.deepEqual(tiles.cal,['52events','9next 7 days','4last 24h'],`${tag} Outlook Calendar: ${tiles.cal}`);
  assert.deepEqual(tiles.gcal,['31events','6next 7 days','1last 24h'],`${tag} Google Calendar: ${tiles.gcal}`);
  assert.deepEqual(tiles.mail,['1,240messages','18last 24h','3not checked'],`${tag} Gmail: ${tiles.mail}`);
  if(shots){await page.locator('#connectors article[data-conn="cal"]').scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/${tag}-card.png`});
   await page.locator('#connect-more').scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/${tag}-row.png`})}
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('connections row and calendar tiles dashboard ok');
