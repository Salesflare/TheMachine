import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections, Checks: messages the checks put off twice (review_last_look.py) under Set aside, closed by default, each
// with what it waits for (one more look on a day, closed after it, or left as is), and its title opens the message. No
// list when nothing is set aside. SHOT_DIR: screenshots at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()+n*864e5).toISOString();
let list=[{id:11,kind:'gmail.message',title:'Question about the renewal terms for next year',at:day(-2),state:'look',look_at:day(1)},
 {id:12,kind:'intercom.conversation',title:'Login issue on the mobile app',at:day(-5),state:'look',look_at:day(-1)},
 {id:13,kind:'gmail.message',title:'Partnership idea',at:day(-6),state:'closed',look_at:null},
 {id:14,kind:'gmail.message',title:'Your weekly digest',at:day(-4),state:'left',look_at:null}];
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_runs:[],
 review_health:{total:240,pending:3,set_aside:list.length,last_completed:day(0),...(list.length?{set_aside_list:list}:{})},
 connectors:[{id:'gmail',email:'pat@example.com',service:'gmail'}]});
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,errors=[];
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]])for(const colorScheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height},colorScheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#connections=reviews');
  const box=page.locator('#set-aside');
  await box.waitFor();
  assert.equal(await box.evaluate(e=>e.open),false);  // quiet: closed until opened
  assert.match(await page.locator('#review-summary').textContent(),/4 set aside/);
  await box.locator('summary').click();
  const rows=page.locator('#set-aside-list .sa-row');
  assert.equal(await rows.count(),4);
  const lines=await rows.locator('small').allTextContents();
  assert.match(lines[0],/^One more look on /);
  assert.deepEqual(lines.slice(1),['One more look with the next check','Closed after one more look','Left as is: no sign it needs you']);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`no sideways scroll at ${width}`);
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/set-aside-${width}-${colorScheme}.png`,fullPage:false});
  await rows.first().locator('button').click();  // the title opens the message in the dashboard's own viewer
  await page.locator('#email-dialog[open]').waitFor();
  assert.equal(await page.locator('#email-title').textContent(),list[0].title);
  await context.close()}
 // nothing set aside: no list
 list=[];
 const context=await browser.newContext({viewport:{width:390,height:844}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/#connections=reviews');await page.locator('#review-summary').waitFor();
 await page.waitForFunction(()=>document.querySelector('#review-summary').textContent.includes('waiting'));
 assert.equal(await page.locator('#set-aside').evaluate(e=>e.hidden),true);
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('set aside dashboard ok');
