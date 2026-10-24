import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from './openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Events opens with the latest signals, newest first by when they arrived or happened, the way a person's timeline
// reads: meetings still to come never sit on top of the list but apart under Coming up, soonest first, three at a
// time. The Machine lists upcoming meetings first (reviews want them); the page sorts them out.
const dashboard=await readFile(new URL('./dashboard.html',import.meta.url),'utf8');
const shots=process.env.SHOTS||'';
const at=h=>new Date(Date.now()+h*36e5).toISOString();
const ev=(id,kind,title,h)=>({id,account_id:'mail',kind,title,body:title,occurred_at:at(h),metadata:{}});
const events=[ev(1,'calendar.event','Board meeting',30),ev(2,'calendar.event','Standup',2),ev(3,'calendar.event','Offsite',100),ev(4,'calendar.event','Dinner',200),
 ev(5,'gmail.message','Invoice question',-1),ev(6,'gmail.message','Old thread',-50),ev(7,'calendar.event','Yesterday call',-20),ev(8,'slack.message','Just now',-0.1)];
let asked=0;
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[{id:'mail',service:'gmail',display_name:'mail',email:'owner@example.org',boundary:'work',state:'{}'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/events'){asked++;res.end(JSON.stringify(url.searchParams.get('q')==='none'?[]:events));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1280,390]){
  const context=await browser.newContext({viewport:{width,height:900},isMobile:width<600,locale:'en-US'}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));asked=0;
  await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof showTab==='function');
  await page.evaluate(()=>showTab('events'));
  await page.locator('#results article').first().waitFor();
  assert.equal(asked,1,'opening Events asks once for the latest');
  const titles=sel=>page.locator(sel).evaluateAll(a=>a.filter(x=>!x.hidden).map(x=>x.querySelector('h3').textContent));
  assert.deepEqual(await titles('#results .ev-soon article'),['Standup','Board meeting','Offsite'],'coming up: soonest first, three shown');
  assert.equal(await page.locator('#results .ev-soon .ge-day').textContent(),'Coming up');
  assert.deepEqual(await titles('#results>article'),['Just now','Invoice question','Yesterday call','Old thread'],'the list: newest first, nothing to come');
  if(shots)await page.screenshot({path:`${shots}/events-${width}.png`});
  await page.locator('[data-ev-soon]').click();
  assert.deepEqual(await titles('#results .ev-soon article'),['Standup','Board meeting','Offsite','Dinner']);
  assert.equal(await page.locator('[data-ev-soon]').count(),0);
  // Going back to Events keeps the list; a search with no match says so
  await page.evaluate(()=>showTab('inbox'));await page.evaluate(()=>showTab('events'));assert.equal(asked,1);
  await page.fill('#query','none');await page.press('#query','Enter');
  await page.waitForFunction(()=>/No matching signals/.test(document.querySelector('#results').textContent));
  assert.equal(await page.locator('#results .ev-soon').count(),0);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'fits '+width);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('events dashboard ok');
}finally{await browser?.close();server.close()}
