import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Not needed and Snooze answer at once, as Mark done does (decideAtOnce): the to-do leaves the list before the Machine
// answers, the save goes behind it, and a refused save puts the to-do back with the error. Not needed shows "Marked not
// needed" with Undo at once; Snooze closes its dialog at once and says when it comes back once the save landed. Offline
// they wait on the device as before (test_offline_dashboard). No network beyond this fake server.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),A='a1'.repeat(8),B='b2'.repeat(8),C='c3'.repeat(8),D='d4'.repeat(8);
const cards={};
const reset=()=>{for(const [id,title] of [[A,'Send Robin the garden dates'],[B,'Book the car service'],[C,'Pay the plumber'],[D,'Water the plants']])
 cards[id]={id,title,body:'A made-up to-do.',status:'pending',scope:'personal',created_at:now,event_ids:[1]}};
reset();
const status=()=>({suggestions:Object.values(cards),promises:[],connectors:[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}],
 suggestion_counts:{pending:4},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],reminders:{telegram:true,push:0}});
const decides=[];let delay=0,refuse=false,answered=0;  // answered: decide answers sent back
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);if(r.action!=='decide'){res.end('{}');return}const {suggestion_id:id,choice}=r.args,s=cards[id];decides.push([id,choice]);
  await new Promise(ok=>setTimeout(ok,delay));res.on('finish',()=>answered++);
  if(refuse){res.statusCode=400;res.end(JSON.stringify({error:'This to-do changed meanwhile'}));return}
  if(choice==='reject'){s.prev=s.status;s.status='rejected';s.closed_at=new Date().toISOString();res.end(JSON.stringify({status:'rejected'}));return}
  if(choice==='undo'){s.status=s.prev||'pending';res.end(JSON.stringify({status:s.status,undone:true}));return}
  if(choice==='snooze'){s.prev=s.status;s.status='snoozed';s.snoozed_until=new Date(Date.now()+864e5).toISOString();res.end(JSON.stringify({status:'snoozed',snoozed_until:s.snoozed_until}));return}
  res.end('{}');return}
 if(/^\/brand\/[\w.-]+\.(png|webp|woff2)$/.test(url.pathname)){try{const f=await readFile(new URL('..'+url.pathname,import.meta.url));res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':url.pathname.endsWith('.webp')?'image/webp':'font/woff2');res.end(f)}catch{res.statusCode=404;res.end()}return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
// on the open list: drawn, not snoozed (Later) and not done
const shown=(page,id)=>page.evaluate(id=>{const n=document.querySelector('#suggestions article#task-'+id);return !!n&&n.getClientRects().length>0&&!n.closest('#finished-list')&&n.dataset.status!=='snoozed'},id);
const toast=page=>page.evaluate(()=>{const t=document.querySelector('#toast');return t.classList.contains('show')?t.textContent.replace(/\s+/g,' ').trim():''});
const back=(page,id)=>page.waitForFunction(id=>{const n=document.querySelector('#suggestions article#task-'+id);return n&&n.getClientRects().length>0&&!n.closest('#finished-list')},id,{timeout:10000});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){reset();decides.length=0;delay=0;refuse=false;const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:'light',locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto(base);await page.locator('#task-'+A).waitFor();
  // Not needed, the Machine slow: the to-do leaves and "Marked not needed · Undo" shows before the save is back
  delay=3000;
  await page.locator(`#task-${A} [data-choice="reject"]`).evaluate(b=>b.click());await page.locator(`#task-${A} [data-choice="dismiss-typed"]`).waitFor();
  let n0=answered;await page.locator(`#task-${A} [data-choice="dismiss-typed"]`).evaluate(b=>b.click());
  assert.ok(!await shown(page,A),'not needed: the to-do left at once');
  assert.equal(await toast(page),'Marked not needed Undo');assert.equal(answered,n0,'before the save landed');
  // Undo right away waits for the save, then undoes
  await page.locator('#toast [data-undo]').click();
  await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('Reopened.'),null,{timeout:10000});
  assert.deepEqual(decides,[[A,'reject'],[A,'undo']]);await back(page,A);
  // A refused Not needed: the to-do comes back as it was, with the error
  delay=300;refuse=true;decides.length=0;
  await page.locator(`#task-${B} [data-choice="reject"]`).evaluate(b=>b.click());await page.locator(`#task-${B} [data-choice="dismiss-typed"]`).evaluate(b=>b.click());
  assert.ok(!await shown(page,B));
  await page.waitForFunction(()=>document.querySelector('#toast.error')?.textContent.includes('This to-do changed meanwhile'),null,{timeout:10000});
  await back(page,B);assert.equal(cards[B].status,'pending');
  // Snooze, the Machine slow: the dialog closes and the to-do leaves at once; the message says when it is back once saved
  delay=3000;refuse=false;decides.length=0;
  await page.evaluate(id=>openSnooze(id),C);n0=answered;await page.locator('#snooze-dialog [data-snooze]').first().evaluate(b=>b.click());
  assert.equal(await page.evaluate(()=>document.querySelector('#snooze-dialog').open),false,'the dialog closed at once');
  assert.ok(!await shown(page,C),'snooze: the to-do left at once');assert.equal(answered,n0,'before the save landed');
  await page.locator('#toast [data-unsnooze]').waitFor({timeout:10000});
  assert.match(await toast(page),/^Snoozed\. I’ll remind you on Telegram\. Undo/);
  assert.deepEqual(decides,[[C,'snooze']]);assert.ok(!await shown(page,C),'still snoozed after the refresh');
  // A refused snooze: back on the list, with the error
  delay=300;refuse=true;decides.length=0;
  await page.evaluate(id=>openSnooze(id),D);await page.locator('#snooze-dialog [data-snooze]').first().evaluate(b=>b.click());
  assert.ok(!await shown(page,D));
  await page.waitForFunction(()=>document.querySelector('#toast.error')?.textContent.includes('This to-do changed meanwhile'),null,{timeout:10000});
  await back(page,D);assert.equal(cards[D].status,'pending');
  await context.close()}
 // INSTANT_SHOT=<dir>: the list at 1440 and 390, light and dark, with one to-do just marked not needed
 if(process.env.INSTANT_SHOT)for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]){reset();delay=1500;refuse=false;const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();await page.goto(base);await page.locator('#task-'+A).waitFor();
  await page.locator(`#task-${A} [data-choice="reject"]`).evaluate(b=>b.click());await page.locator(`#task-${A} [data-choice="dismiss-typed"]`).evaluate(b=>b.click());
  await page.waitForTimeout(200);await page.screenshot({path:`${process.env.INSTANT_SHOT}/todos-not-needed-${width}-${scheme}.png`});await page.waitForTimeout(1500);await context.close()}
 assert.deepEqual(errors,[]);
 console.log('instant not needed and snooze dashboard ok');
}finally{await browser?.close();server.close()}
