import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, Notifications (notify.py): a switch per kind and channel (Telegram only when it's set up, Email for the
// digest only), saved at once; Preview shows the digest on the page; the page tells the Machine it is in front of the
// owner (notify_active). At 390px the grid stays inside the screen. Nothing is sent: the server here is a fixture.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const prefs={todo:{push:true,telegram:true},result:{push:true,telegram:true},reminder:{push:true,telegram:true},digest:{push:true,telegram:false,email:false}};
let telegram=true;const posts=[];
const view=()=>({prefs,telegram,email:true,push_devices:0,push_ready:true,digest_at:'08:30'});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
  hours:{days:[0,1,2,3,4],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC',saveable:true},notify:view()}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push(action);
  if(action==='notify_set'){prefs[args.kind][args.channel]=args.on;res.end(JSON.stringify(view()));return}
  if(action==='notify_preview'){res.end(JSON.stringify({empty:false,text:'Today\n• 09:30 Planning with the agency'}));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1280,390]){
  telegram=width>500;
  const context=await browser.newContext({viewport:{width,height:900}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
  await navClick(page.locator('#open-settings'));
  await page.locator('#settings-tabs [data-settings-tab="notify"]').click();
  assert.equal(await page.evaluate(()=>location.hash),'#settings/notify');
  assert.equal(await page.locator('#help-link').getAttribute('href'),'https://themachine.computer/help/notifications');
  const cols=await page.locator('#notify-grid .notify-col').allInnerTexts();
  assert.deepEqual(cols,telegram?['Push','Telegram','Email']:['Push','Email']);
  // Email only for the digest: a switch there, a dash elsewhere
  assert.equal(await page.locator('#notify-grid [data-notify-channel="email"]').count(),1);
  assert.equal(await page.locator('#notify-grid .notify-na').count(),3);
  const sw=page.locator('[data-notify-kind="todo"][data-notify-channel="push"]');
  assert.equal(await sw.getAttribute('aria-checked'),'true');
  await sw.click();await page.locator('[data-notify-kind="todo"][data-notify-channel="push"][aria-checked="false"]').waitFor();
  assert.equal(prefs.todo.push,false);prefs.todo.push=true;
  await page.locator('[data-notify-preview]').click();
  await page.locator('#notify-preview:not([hidden])',{hasText:'Planning with the agency'}).waitFor();
  assert.equal(await page.locator('[data-notify-preview]').innerText(),'Hide preview');
  // The digest row changes its time and days in Work hours too; the footnote keeps its distance from the card
  const fine=await page.evaluate(()=>{const f=document.querySelector('#settings-notify .notify-fine'),l=document.querySelector('#notify-more');return f.getBoundingClientRect().top-l.getBoundingClientRect().bottom});
  assert.ok(fine>=16,'footnote spacing '+fine);
  await page.locator('[data-notify-digest]').click();
  assert.equal(await page.evaluate(()=>location.hash),'#settings/hours');
  await page.locator('#settings-tabs [data-settings-tab="notify"]').click();await page.locator('[data-notify-hours]').waitFor();
  await page.locator('[data-notify-hours]').click();
  assert.equal(await page.evaluate(()=>location.hash),'#settings/hours');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'fits '+width);
  await context.close();
 }
 // A page in focus says so (the Machine then holds pushes back).
 const context=await browser.newContext({viewport:{width:1280,height:900}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await page.goto(base);await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
 await page.bringToFront();await page.evaluate(()=>dispatchEvent(new Event('focus')));
 await page.waitForFunction(()=>true);await new Promise(r=>setTimeout(r,500));
 assert.ok(posts.includes('notify_active'),'heartbeat');
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('notify dashboard ok');
