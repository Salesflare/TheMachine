import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Learning, Decisions: every row is titled with its to-do, also an older done one that is past the suggestions list
// (the server sends the title with the decision), never with the to-do's id; its time is in the sans font, like
// Changes. Changes: the why line under a change says "you". All mocked; SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const ago=m=>new Date(Date.now()-m*60000).toISOString();
const status=()=>({suggestions:[{id:'b2c3d4e5f6a7b8c9',title:'Reply to Ana about the venue',body:'Ana asked which room.',status:'pending',created_at:ago(300)}],promises:[],suggestion_counts:{},analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],
 decisions:[
  {id:'d1',suggestion_id:'48a9a3c08f304bdc',title:'Ana accepts the revised venue wording',choice:'complete',source:'assistant',feedback:'Sent: Send reply',created_at:ago(1)},
  {id:'d2',suggestion_id:'48a9a3c08f304bdc',title:'Ana accepts the revised venue wording',choice:'send',source:'dashboard',created_at:ago(2)},
  {id:'d3',suggestion_id:'b2c3d4e5f6a7b8c9',choice:'accept',source:'dashboard',created_at:ago(120)},
  {id:'d4',suggestion_id:'0f1e2d3c4b5a6978',title:'',choice:'reject',source:'dashboard',created_at:ago(240)}],
 facts:[{id:9,kind:'fact',text:'You prefer to meet online with Northwind.',created_at:ago(60),merged:0}],
 learning_changes:[{id:1,at:ago(60),kind:'fact',channel:null,text:'You prefer to meet online with Northwind.',before:null,why:'You corrected the Northwind coffee to-do: “can we have it online”.',undone:false}]});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[],shots=process.env.SHOTS;let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1280,800],[390,844]])for(const scheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#learning=decisions');
  await navClick(page.locator('[data-tab="feedback"]').first());
await page.locator('#learn-tab-decisions').click();
  const box=page.locator('#decisions');await box.locator('article').first().waitFor();
  assert.deepEqual(await box.locator('article h3').allTextContents(),
   ['Ana accepts the revised venue wording','Ana accepts the revised venue wording','Reply to Ana about the venue','To-do']);
  assert.doesNotMatch(await box.textContent(),/[0-9a-f]{16}/,'no to-do id as a title');
  const font=await box.locator('article').first().evaluate(a=>{const f=e=>getComputedStyle(e).fontFamily;return {time:f(a.querySelector('time')),via:f(a.querySelector('.row small')),mono:a.querySelector('time').classList.contains('mono')}});
  assert.equal(font.mono,false);assert.equal(font.time,font.via,'the time is in the sans font, like the rest of the row');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
  if(shots){await page.evaluate(()=>document.fonts.ready);await page.locator('#learn-pane-decisions').screenshot({path:`${shots}/decisions-${width}-${scheme}.png`})}
  await page.locator('#learn-tab-changes').click();
  const row=page.locator('#learn-changes .change-row').first();await row.waitFor();
  assert.match(await row.textContent(),/You corrected the Northwind coffee to-do/);
  if(shots){await page.evaluate(()=>document.fonts.ready);await page.locator('#learn-pane-changes').screenshot({path:`${shots}/changes-${width}-${scheme}.png`})}
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('learning decisions dashboard ok');
}finally{await browser?.close();server.close()}
