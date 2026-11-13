import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Templates on the Routines page (dashboard/routines-page.js): every template card has an action. Spam cleanup with no
// mail account (routine_templates.view needs 'mail') says so in one short line, with Connect mail that opens Connections;
// with any mail account (read-only Gmail too) it has Add like the others. SHOTS=<dir> saves the page at 390 and 1440,
// light and dark.
const dashboard=await dashboardPage();
let needs='mail';const posts=[];
const templates=()=>[{key:'newsletters',name:'Newsletter cleanup',what:'Every morning, one to-do with the past day’s newsletters. Keep or unsubscribe each one.',added:false},
 {key:'spam',name:'Spam cleanup',what:'Every hour, a to-do with any new spam that got through. Mark each one as spam or not.',added:false,...(needs?{needs}:{})},
 {key:'digest',name:'Daily digest',what:'Every morning, the few newsletter pieces worth your time, picked for what you care about.',added:false},
 {key:'birthdays',name:'Birthdays',what:'Every morning, a to-do with a short greeting for each close contact who has a birthday.',added:false}];
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/routines'){res.end(JSON.stringify({routines:[],suggested:[],trying:[],templates:templates()}));return}
 if(req.method==='POST'&&body)posts.push(JSON.parse(body).action);
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,scheme,kind] of [[1440,'light','mail'],[390,'dark','mail'],[1440,'dark',null],[390,'light',null]]){
  needs=kind;
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme,timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
  const cards=page.locator('#routines-view .rt-tpl');
  await cards.first().waitFor();
  assert.deepEqual(await cards.locator('h3').allInnerTexts(),['Newsletter cleanup','Spam cleanup','Daily digest','Birthdays']);
  for(let i=0;i<4;i++){const b=cards.nth(i).locator('button');
   assert.equal(await b.count(),1,'every template card has one action');assert.ok(await b.isVisible()&&await b.isEnabled())}
  const spam=cards.nth(1);
  if(kind){
   assert.equal((await spam.locator('.rt-needs').innerText()).trim(),'Needs a connected mail account.');
   assert.equal((await spam.locator('button').innerText()).trim(),'Connect mail');
   assert.equal(await spam.locator('[data-connect-open]').count(),1,'it opens Connections');
  }else{
   assert.equal(await spam.locator('.rt-needs').count(),0);
   assert.equal(await spam.locator('[data-rt-tpl="spam"]').count(),1);
  }
  const box=await spam.boundingBox(),btn=await spam.locator('button').boundingBox();
  assert.ok(btn.x+btn.width<=box.x+box.width+0.5,'the action stays inside its card');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  if(process.env.SHOTS)await page.screenshot({path:`${process.env.SHOTS}/templates-${kind||'add'}-${width}-${scheme}.png`});
  await context.close();
 }
 assert.deepEqual(posts,[]);
 assert.deepEqual(errors,[]);
 console.log('routine template needs ok');
}finally{await browser?.close();server.close()}
