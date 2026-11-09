import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdir} from 'node:fs/promises';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A run that needs a source that isn't connected (preparation_blocked connect): never a dead Stuck, and never a trip
// into settings. The to-do says in one plain line what it couldn't read and leads with Connect Slack, which opens Slack
// in Connections; Try again stays beside it for after. SHOT_DIR=<folder> saves it at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[
 {id:'f6f6f6f6f6f6f6f6',title:'Hand the Halvorsen homepage to Leo',status:'instructions',scope:'work',area:'work:Studio',created_at:now,event_ids:[1],
  body:'Leo has two homepage directions ready for Halvorsen.',preparation_status:'blocked',
  preparation_reason:"Slack isn't connected, so I can't read Leo's reply. Connect it and I'll pick this up.",
  preparation_no_questions:true,preparation_questions:[],preparation_connect:'slack'}];
const posts=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,areas:[{id:'work:Studio',label:'Work',name:'Studio'}],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/action'){const {action}=JSON.parse(body||'{}');posts.push(action);
  if(action==='connect_sources'){res.end(JSON.stringify({sources:[{name:'slack',service:'slack',label:'Slack',group:'chat',connected:0,broker:false,form:null}],manage_url:null,saveable:true}));return}}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOT_DIR;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const [width,height] of [[390,844],[1440,900]]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  const card=page.locator('#task-f6f6f6f6f6f6f6f6');await card.waitFor();
  const lead=card.locator('.actions > button.primary').first();
  assert.equal(await lead.textContent(),'Connect Slack');
  const text=await card.innerText();
  assert.match(text,/Needs your help/);assert.doesNotMatch(text,/Stuck/);
  assert.match(text,/Slack isn't connected, so I can't read Leo's reply\. Connect it and I'll pick this up\./);
  assert.doesNotMatch(text,/settings|OpenClaw|browser access|tap Try again/i);  // it carries on by itself once connected
  assert.equal(await card.locator('.actions > button[data-choice="retry"]:visible').count(),0);  // no second lead beside Connect
  assert.ok(await card.locator('[data-choice="retry"]').count()>=1);  // Try again stays in the menu as a fallback
  if(shots){await page.waitForTimeout(300);await card.screenshot({path:`${shots}/connect-slack-${width}-${scheme}.png`})}
  await lead.click();
  await page.waitForFunction(()=>location.hash.startsWith('#health')||document.querySelector('nav [data-tab="health"]')?.classList.contains('active'));
  assert.ok(posts.includes('connect_sources'));  // the Add list, with Slack in it
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('connect from a stuck to-do: ok');
}finally{await browser?.close();server.close()}
