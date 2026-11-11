import assert from 'node:assert/strict';
import {mkdir, readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A fact the owner asked their chat to forget (forget_learned, activity_log.py's memory lines): Settings, Activity shows
// "Forgot: ..." with Undo, the filter names it Learning, and Undo sends learning_undo with the change's id, the same
// Undo as Learning, Changes; once undone the line says so and has no Undo. At 1440x900 and 390x844, light and dark.
// All mocked. SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const NOW=new Date('2026-06-10T15:00:00Z');
const LINE={id:'memory:7',kind:'memory',at:'2026-06-10T14:20:00+00:00',what:'Forgot: You moved to Ghent last spring.',where:null,outcome:'done',status:'Done',by:'Asked in chat',todo:null,undo:{action:'learning_undo',id:7}};
const OTHER={id:'connections:added:slack',kind:'connections',at:'2026-06-09T10:00:00+00:00',what:'Connection added',where:'Slack · acme.slack.com',outcome:'done',status:'Added',by:null,todo:null};
let undone=false;const posts=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],voices:[],facts:[]}));return}
 if(url.pathname==='/api/activity'){const line=undone?{...LINE,outcome:'undone',status:'Undone',undo:null}:LINE;
  res.end(JSON.stringify({items:[line,OTHER],next:null,kinds:['connections','memory']}));return}
 if(url.pathname==='/api/action'&&req.method==='POST'){let body='';for await(const c of req)body+=c;const call=JSON.parse(body);posts.push(call);
  if(call.action==='learning_undo')undone=true;res.end(JSON.stringify({undone:call.args.id}));return}
 res.end(url.pathname==='/api/events'?'[]':'{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  undone=false;posts.length=0;
  const phone=width<600,context=await browser.newContext({viewport:{width,height},isMobile:phone,hasTouch:phone,colorScheme:scheme,timezoneId:'UTC'}),page=await context.newPage();
  await context.clock.setFixedTime(NOW);
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#settings/activity');
  const list=page.locator('#act-list'),row=list.locator('.act-row').first();await row.waitFor();
  const text=await row.innerText();
  for(const part of ['Forgot: You moved to Ghent last spring.','Done','Asked in chat'])assert.ok(text.includes(part),part);
  assert.ok(!/^You/.test(await row.locator('.act-what').innerText()),'the event line never starts with You');
  assert.deepEqual(await page.locator('#act-filter option').allInnerTexts(),['Everything','Connections','Learning','Refused or blocked']);
  const undo=row.locator('[data-act-undo]');assert.equal(await undo.innerText(),'Undo');
  const box=await undo.boundingBox();assert.ok(box.x+box.width<=width,'Undo stays inside');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${width}: no sideways scroll`);
  if(shots)await page.screenshot({path:`${shots}/forget-activity-${width}x${height}-${scheme}.png`});
  await undo.click();
  await page.waitForFunction(()=>document.querySelector('#act-list .act-row')?.innerText.includes('Undone'));
  assert.deepEqual(posts.filter(p=>p.action==='learning_undo'),[{action:'learning_undo',args:{id:7}}]);
  assert.equal(await list.locator('.act-row').first().locator('[data-act-undo]').count(),0);
  if(shots)await page.screenshot({path:`${shots}/forget-activity-undone-${width}x${height}-${scheme}.png`});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('chat forget dashboard ok');
}finally{await browser?.close();server.close()}
