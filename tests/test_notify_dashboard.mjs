import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, Notifications (notify.py): a switch per kind and channel (Telegram only when it's set up, Email for every
// kind), saved at once; Preview shows the digest on the page; Work hours sit in the same tab. The page tells the Machine
// whether it is in use, like Slack: visible, in focus and touched in the last 10 minutes; in the background or idle it
// is not (notify_active). At 390px the grid stays inside the screen. Nothing is sent: the server here is a fixture.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const prefs={todo:{push:true,telegram:true,email:true},result:{push:true,telegram:true,email:true},reminder:{push:true,telegram:true,email:true},digest:{push:true,telegram:false,email:true}};
let telegram=true;const posts=[],beats=[];
const view=()=>({prefs,telegram,email:true,push_devices:0,push_ready:true,digest_at:'08:30'});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
  hours:{days:[0,1,2,3,4],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC',saveable:true},notify:view()}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push(action);beats.push(action==='notify_active'?args:null);
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
  // Email for every kind, no dashes
  assert.equal(await page.locator('#notify-grid [data-notify-channel="email"]').count(),4);
  assert.equal(await page.locator('#notify-grid .notify-na').count(),0);
  const sw=page.locator('[data-notify-kind="todo"][data-notify-channel="email"]');
  assert.equal(await sw.getAttribute('aria-checked'),'true');
  await sw.click();await page.locator('[data-notify-kind="todo"][data-notify-channel="email"][aria-checked="false"]').waitFor();
  assert.equal(prefs.todo.email,false);prefs.todo.email=true;
  await page.locator('[data-notify-preview]').click();
  await page.locator('#notify-preview:not([hidden])',{hasText:'Planning with the agency'}).waitFor();
  assert.equal(await page.locator('[data-notify-preview]').innerText(),'Hide preview');
  // Preview sits in the digest row of the grid; the card below is only This device
  assert.equal(await page.locator('#notify-grid [data-notify-preview]').count(),1);
  assert.deepEqual(await page.locator('#notify-more strong').allInnerTexts(),['This device']);
  // Work hours are in this tab now, right under it: no second tab, no Change buttons that jump away
  assert.equal(await page.locator('#settings-tabs [data-settings-tab="hours"]').count(),0);
  assert.equal(await page.locator('#hours').isVisible(),true);
  assert.equal(await page.locator('[data-notify-hours],[data-notify-digest]').count(),0);
  const gap=await page.evaluate(()=>{const f=document.querySelector('#settings-notify .notify-fine'),l=document.querySelector('#notify-more'),h=document.querySelector('#hours');
   return {fine:f.getBoundingClientRect().top-l.getBoundingClientRect().bottom,below:h.getBoundingClientRect().top>f.getBoundingClientRect().bottom}});
  assert.ok(gap.fine>=16,'footnote spacing '+gap.fine);assert.ok(gap.below,'hours below the grid');
  if(process.env.SHOTS)await page.screenshot({path:`${process.env.SHOTS}/notify-${width}.png`,fullPage:true});
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'fits '+width);
  await context.close();
 }
 // Presence, like Slack: in use (visible, focused, touched) says active; the window losing focus says away at once;
 // ten minutes without input says away too, with how long it was idle; touching it again says active.
 const context=await browser.newContext({viewport:{width:1280,height:900}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await page.clock.install();beats.length=0;
 await page.goto(base);await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
 await page.bringToFront();await page.evaluate(()=>{document.hasFocus=()=>true;dispatchEvent(new Event('focus'))});
 const lastBeat=async()=>{await page.waitForTimeout(50);await new Promise(r=>setTimeout(r,150));return beats.filter(Boolean).at(-1)};
 assert.equal((await lastBeat())?.active,true,'in use');
 await page.evaluate(()=>{document.hasFocus=()=>false;dispatchEvent(new Event('blur'))});
 assert.equal((await lastBeat())?.active,false,'in the background');
 await page.evaluate(()=>{document.hasFocus=()=>true;dispatchEvent(new Event('focus'))});
 assert.equal((await lastBeat())?.active,true,'back');
 await page.clock.runFor(11*60e3);  // focused, but nobody touched it for eleven minutes
 const idle=await lastBeat();
 assert.equal(idle?.active,false,'idle');assert.ok(idle.idle>=600,'idle seconds '+idle.idle);
 await page.mouse.move(40,40);await page.mouse.move(60,60);
 assert.equal((await lastBeat())?.active,true,'touched again');
 const id=beats.filter(Boolean)[0].client;assert.match(id,/^[a-z0-9]{1,16}$/);assert.ok(beats.filter(Boolean).every(b=>b.client===id));
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('notify dashboard ok');
