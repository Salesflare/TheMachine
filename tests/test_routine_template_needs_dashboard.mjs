import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Templates on the Routines page (dashboard/routines-page.js): Spam cleanup on a Machine with no mailbox it may move spam
// in (routine_templates.view needs) still shows, with one short line saying why in place of Add; the others keep Add.
// SHOTS=<dir> saves the page at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
let needs='gmail';const posts=[];
const templates=()=>[{key:'newsletters',name:'Newsletter cleanup',what:'Every morning, one to-do with the past day’s newsletters. Keep or unsubscribe each one.',added:false},
 {key:'spam',name:'Spam cleanup',what:'Every hour, a to-do with any new spam that got through. Mark each one as spam or not.',added:false,...(needs?{needs}:{})},
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
 for(const [width,scheme,kind] of [[1440,'light','gmail'],[390,'dark','gmail'],[1440,'dark','mail'],[390,'light','mail'],[1440,'light',null]]){
  needs=kind;
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme,timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
  const cards=page.locator('#routines-view .rt-tpl');
  await cards.first().waitFor();
  assert.deepEqual(await cards.locator('h3').allInnerTexts(),['Newsletter cleanup','Spam cleanup','Birthdays']);
  const spam=cards.nth(1);
  if(kind){
   assert.equal((await spam.locator('.rt-needs').innerText()).trim(),kind==='gmail'?'Gmail is connected read-only here, so spam can’t be moved.':'Needs a mailbox where spam can be moved, like Outlook.');
   assert.equal(await spam.locator('button').count(),0,'no Add it could not keep');
  }else{
   assert.equal(await spam.locator('.rt-needs').count(),0);
   assert.equal(await spam.locator('[data-rt-tpl="spam"]').count(),1);
  }
  assert.equal(await cards.nth(0).locator('[data-rt-tpl="newsletters"]').count(),1);
  const box=await spam.boundingBox(),line=kind&&await spam.locator('.rt-needs').boundingBox();
  if(line)assert.ok(line.x+line.width<=box.x+box.width+0.5,'the line stays inside its card');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  if(process.env.SHOTS&&kind)await page.screenshot({path:`${process.env.SHOTS}/templates-${kind}-${width}-${scheme}.png`});
  await context.close();
 }
 assert.deepEqual(posts,[]);
 assert.deepEqual(errors,[]);
 console.log('routine template needs ok');
}finally{await browser?.close();server.close()}
