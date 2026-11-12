import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// "Turn on Newsletter cleanup?" above the to-dos (dashboard/todos-repeat.js, routine_offers.py): this week's count and
// what the template does, Turn it on or No thanks; only one offer at a time, a recurring one first. Made-up data; nothing is sent.
// SHOTS=<dir>: also saves the line at each size, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),posts=[],C1='c3'.repeat(8);
const cards=[{id:C1,title:'Reply to the venue about the date',body:'They asked for a second option.',status:'pending',scope:'work',created_at:now,event_ids:[1]}];
const WHAT='Every morning, one to-do with the past day’s newsletters. Keep or unsubscribe each one.';
let offer,recurring;
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 recurring_offer:recurring,routine_offer:offer,locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='routine_offer'){offer=null;res.end(JSON.stringify({key:b.args.key,added:b.args.choice==='yes'?'r1':null}));return}
  if(b.action==='recurring_offer'){recurring=null;res.end(JSON.stringify({key:b.args.key,made:null}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const sent=name=>posts.filter(p=>p.action===name);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of process.env.SHOTS?['light','dark']:['light']){
  posts.length=0;offer={key:'newsletters',n:38,name:'Newsletter cleanup',what:WHAT};recurring={key:'fact:7',title:'Send the board update',rule:{unit:'month',n:1},anchor:'2026-11-05'};
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+C1).waitFor();
  // a recurring offer goes first: one offer at a time
  await page.locator('.repeat-offer').first().waitFor();assert.equal(await page.locator('.routine-offer').count(),0);
  await page.locator('.repeat-offer').getByText('No thanks').click();
  const line=page.locator('.routine-offer');await line.waitFor();
  assert.equal((await line.locator('p').innerText()).replace(/\s+/g,' ').trim(),'Turn on Newsletter cleanup? 38 newsletters this week. '+WHAT);
  assert.deepEqual(await line.locator('button').evaluateAll(n=>n.map(x=>x.textContent)),['Turn it on','No thanks']);
  const box=await line.boundingBox();assert.ok(box.x>=0&&box.x+box.width<=width+1,'the line fits the page');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'no sideways scroll');
  if(process.env.SHOTS){await page.mouse.move(1,height-1);await page.screenshot({path:`${process.env.SHOTS}/offer-${width}-${scheme}.png`})}
  if(width<600){await line.getByText('No thanks').click();await line.waitFor({state:'detached'});
   assert.deepEqual(sent('routine_offer').at(-1),{action:'routine_offer',key:'newsletters',choice:'no'})}
  else{await line.getByText('Turn it on').click();await line.waitFor({state:'detached'});await page.getByText('Routine added').first().waitFor();
   assert.deepEqual(sent('routine_offer').at(-1),{action:'routine_offer',key:'newsletters',choice:'yes'})}
  // Spam cleanup's own words; none for a key the page doesn't know
  offer={key:'spam',n:7,name:'Spam cleanup',what:'Every hour, a to-do with any new spam that got through. Mark each one as spam or not.'};
  await page.evaluate(()=>refresh());await line.waitFor();
  assert.match(await line.innerText(),/Turn on Spam cleanup\?\s*7 mails moved to spam by hand this week\./);
  if(process.env.SHOTS)await page.screenshot({path:`${process.env.SHOTS}/offer-spam-${width}-${scheme}.png`});
  offer={key:'other',n:3,name:'x',what:'x'};await page.evaluate(()=>refresh());await line.waitFor({state:'detached'});
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('routine offer dashboard ok');
}finally{await browser?.close();server.close()}
