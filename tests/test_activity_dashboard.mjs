import assert from 'node:assert/strict';
import {mkdir, readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, Activity (activity_log.py, settings-activity.js): one list of everything The Machine did, newest first and
// by day, each line with what, how it went, when, where and who started it, and its to-do. The filter shows the kinds
// this Machine has, or only what was refused or blocked; Show more reads the next page; a line's to-do opens even once
// it's done (api/cards/done?id=). Read-only: no line has anything that changes what The Machine may do.
// At 1440x900, 1440x700 and 390x844 the page stays inside the screen. All mocked. SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const day=(d,h)=>new Date(Date.now()-d*86400000).toISOString().slice(0,11)+h+':00+00:00';
const TODO={id:'a1b2c3d4e5f60718',title:'Reply to Robin about the renewal and the new pricing for next year'};
const LINES=[
 {id:'messages:j1',kind:'messages',at:day(0,'09:12'),what:'Email to Robin: Renewal pricing',where:'Gmail · sam@acme.example',outcome:'done',status:'Sent',by:'After your OK',todo:TODO},
 {id:'messages:j2',kind:'messages',at:day(0,'08:40'),what:'WhatsApp message to Kim',where:'WhatsApp',outcome:'refused',status:'Blocked',by:'Approved by voice',todo:null,detail:'The number changed since the draft.'},
 {id:'docs:j3',kind:'docs',at:day(1,'16:05'),what:'New doc: Q4 plan',where:'Google Docs · sam@acme.example',outcome:'done',status:'Created',by:'After your OK',todo:null},
 {id:'fleet:7',kind:'fleet',at:day(1,'11:30'),what:'From Kim: Who is joining the Acme review?',where:'Fleet',outcome:'done',status:'Answered',by:null,todo:null},
 {id:'connections:added:slack',kind:'connections',at:day(2,'10:00'),what:'Connection added',where:'Slack · acme.slack.com',outcome:'done',status:'Added',by:null,todo:null}];
const MORE=[{id:'fixes:j9',kind:'fixes',at:day(9,'07:00'),what:'Fix merged',where:'The Machine',outcome:'done',status:'Merged',by:'By itself',todo:null}];
const asked=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],voices:[],facts:[]}));return}
 if(url.pathname==='/api/activity'){asked.push(url.search);const kind=url.searchParams.get('kind'),outcome=url.searchParams.get('outcome'),cursor=+url.searchParams.get('cursor')||0;
  let items=[...LINES,...MORE].filter(x=>(!kind||kind.split(',').includes(x.kind))&&(!outcome||x.outcome===outcome));
  const page=cursor?items.slice(LINES.length):items.slice(0,kind||outcome?items.length:LINES.length);
  res.end(JSON.stringify({items:page,next:!cursor&&!kind&&!outcome?LINES.length:null,kinds:['messages','docs','fleet','connections','fixes']}));return}
 if(url.pathname==='/api/cards/done'){asked.push('done?'+url.searchParams.get('id'));res.end(JSON.stringify({cards:url.searchParams.get('id')===TODO.id?[{...TODO,status:'done',body:'Done.',closed_at:day(0,'09:13'),event_ids:[],account_ids:[]}]:[],next:null,total:1}));return}
 res.end(url.pathname==='/api/events'?'[]':'{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[1440,700],[390,844]])for(const scheme of ['light','dark']){
  asked.length=0;
  const phone=width<600,context=await browser.newContext({viewport:{width,height},isMobile:phone,hasTouch:phone,colorScheme:scheme}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#settings/activity');
  const list=page.locator('#act-list');await list.locator('.act-row').first().waitFor();
  assert.equal(await page.locator('#settings-tabs [data-settings-tab="activity"]').getAttribute('aria-selected'),'true');
  // Newest first, by day, each line with what, how it went, when, where and who
  assert.equal(await list.locator('.act-row').count(),5);
  assert.deepEqual((await list.locator('.act-day').allInnerTexts()).slice(0,2),['Today','Yesterday']);
  const first=await list.locator('.act-row').first().innerText();
  for(const part of ['Email to Robin: Renewal pricing','Sent','Gmail · sam@acme.example','After your OK'])assert.ok(first.includes(part),part);
  assert.ok(await list.locator('.act-row.act-refused .act-status').first().isVisible(),'a blocked line says so');
  assert.equal(await list.locator('.act-row').nth(1).locator('.act-status').textContent(),'Blocked');
  // Read-only: nothing on a line changes what The Machine may do
  assert.equal(await list.locator('button:not(.act-todo)').count(),0);
  // The filter: the kinds this Machine has, then Refused or blocked
  const options=await page.locator('#act-filter option').allInnerTexts();
  assert.deepEqual(options,['Everything','Messages','Docs','Fixes','Fleet','Connections','Refused or blocked']);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${width}: no sideways scroll`);
  const todo=await list.locator('.act-todo').first().boundingBox();assert.ok(todo.x+todo.width<=width,'a long to-do title stays inside');
  if(shots)await page.screenshot({path:`${shots}/activity-${width}x${height}-${scheme}.png`});
  if(scheme==='dark')continue;
  // Show more: the next page, after what's there
  await page.click('#act-more');await list.locator('.act-row').nth(5).waitFor();
  assert.ok(asked.includes('?&cursor=5'),JSON.stringify(asked));assert.ok(await page.locator('#act-more').isHidden());
  // Refused or blocked: only what didn't go
  await page.selectOption('#act-filter','refused');await page.waitForFunction(()=>document.querySelectorAll('#act-list .act-row').length===1);
  assert.ok(asked.includes('?outcome=refused'));
  assert.match(await list.innerText(),/The number changed since the draft\./);
  if(shots)await page.screenshot({path:`${shots}/activity-refused-${width}x${height}.png`});
  // One kind
  await page.selectOption('#act-filter','docs');await page.waitForFunction(()=>document.querySelector('#act-list .act-row')?.innerText.includes('Q4 plan')&&document.querySelectorAll('#act-list .act-row').length===1);
  assert.ok(asked.includes('?kind=docs'));
  // A line's to-do opens, even once it's done
  await page.selectOption('#act-filter','');await list.locator('.act-todo').first().waitFor();
  await list.locator('.act-todo').first().click();
  await page.waitForFunction(id=>document.querySelector('#settings').hidden&&location.hash==='#chat='+id,TODO.id);
  if(shots)await page.screenshot({path:`${shots}/activity-todo-open-${width}x${height}.png`});
  assert.ok(asked.includes('done?'+TODO.id));
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('activity dashboard ok');
}finally{await browser?.close();server.close()}
