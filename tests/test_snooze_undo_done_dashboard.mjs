import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Snooze and Mark done answer at once. The Snooze message has Undo, which brings the to-do back (accept on a snoozed
// to-do, as Unsnooze), and only while it is still snoozed. Mark done closes the to-do on screen before the Machine
// answers, with "Marked done" and Undo; Undo tapped before the save landed waits for it, then undoes; a refused save
// puts the to-do back with the error. No network beyond this fake server.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),A='a1'.repeat(8),B='b2'.repeat(8),C='c3'.repeat(8);
const cards={};
const reset=()=>{for(const [id,title] of [[A,'Send Robin the garden dates'],[B,'Book the car service'],[C,'Pay the plumber']])
 cards[id]={id,title,body:'A made-up to-do.',status:'pending',scope:'personal',created_at:now,event_ids:[1]}};
reset();
const status=()=>({suggestions:Object.values(cards),promises:[],connectors:[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}],
 suggestion_counts:{pending:3},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],reminders:{telegram:true,push:0}});
const decides=[];let doneDelay=0,refuse=false;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);if(r.action!=='decide'){res.end('{}');return}const {suggestion_id:id,choice}=r.args,s=cards[id];decides.push([id,choice,Date.now()]);
  if(choice==='complete'){await new Promise(ok=>setTimeout(ok,doneDelay));if(refuse){res.statusCode=400;res.end(JSON.stringify({error:'Mark done only an open item'}));return}
   s.prev=s.status;s.status='completed';s.closed_at=new Date().toISOString();res.end(JSON.stringify({status:'completed'}));return}
  if(choice==='undo'){s.status=s.prev||'pending';res.end(JSON.stringify({status:s.status,undone:true}));return}
  if(choice==='snooze'){s.prev=s.status;s.status='snoozed';s.snoozed_until=new Date(Date.now()+864e5).toISOString();res.end(JSON.stringify({status:'snoozed',snoozed_until:s.snoozed_until}));return}
  if(choice==='accept'){s.status=s.status==='snoozed'?s.prev:'accepted';s.snoozed_until=null;res.end(JSON.stringify({status:s.status}));return}
  res.end('{}');return}
 if(/^\/brand\/[\w.-]+\.(png|webp|woff2)$/.test(url.pathname)){try{const f=await readFile(new URL('..'+url.pathname,import.meta.url));res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':url.pathname.endsWith('.webp')?'image/webp':'font/woff2');res.end(f)}catch{res.statusCode=404;res.end()}return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const shown=(page,id)=>page.evaluate(id=>{const n=document.querySelector('#suggestions article#task-'+id);return !!n&&n.getClientRects().length>0&&!n.closest('#finished-list')},id);
const toast=page=>page.evaluate(()=>{const t=document.querySelector('#toast');return t.classList.contains('show')?t.textContent.replace(/\s+/g,' ').trim():''});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){reset();decides.length=0;doneDelay=0;refuse=false;const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:'light',locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto(base);await page.locator('#task-'+A).waitFor();
  // Snooze, then Undo: the to-do is back on the list, and the Machine was asked to unsnooze it (accept on a snoozed one)
  await page.evaluate(id=>openSnooze(id),A);await page.locator('#snooze-dialog [data-snooze]').first().click();
  await page.locator('#toast [data-unsnooze]').waitFor();
  assert.equal(await page.locator('#toast button').first().getAttribute('data-unsnooze'),A,'Undo leads the snooze message');
  await page.locator('#toast [data-unsnooze]').click();
  await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('Back on the list.'));
  assert.deepEqual(decides.map(([id,c])=>[id,c]),[[A,'snooze'],[A,'accept']]);
  assert.ok(await shown(page,A),'the to-do is back');
  // Undo on a snooze that is no longer one (brought back meanwhile) asks for nothing: never an accept on an open to-do
  await page.evaluate(id=>openSnooze(id),A);await page.locator('#snooze-dialog [data-snooze]').first().click();await page.locator('#toast [data-unsnooze]').waitFor();
  cards[A].status='pending';await page.evaluate(()=>refresh());decides.length=0;
  await page.locator('#toast [data-unsnooze]').click();
  await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('It isn’t snoozed anymore.'));
  assert.deepEqual(decides,[]);
  // Mark done, the Machine slow: the to-do leaves and "Marked done · Undo" shows before the save is back
  doneDelay=1500;
  const t0=Date.now();await page.locator(`#task-${B} [data-choice="complete"]`).evaluate(b=>b.click());
  assert.ok(!await shown(page,B),'the to-do left at once');
  assert.equal(await toast(page),'Marked done Undo');assert.ok(Date.now()-t0<1000,'before the save landed');
  // Undo right away: it waits for the save, then undoes, and the to-do is back
  await page.locator('#toast [data-undo]').click();
  await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('Reopened.'),null,{timeout:10000});
  assert.deepEqual(decides.map(([id,c])=>[id,c]),[[B,'complete'],[B,'undo']]);
  assert.ok(await shown(page,B),'the to-do is back after Undo');
  // A refused save: the to-do comes back as it was, with the error
  doneDelay=300;refuse=true;await page.locator(`#task-${C} [data-choice="complete"]`).evaluate(b=>b.click());
  assert.ok(!await shown(page,C));
  await page.waitForFunction(()=>document.querySelector('#toast.error')?.textContent.includes('Mark done only an open item'),null,{timeout:10000});
  await page.waitForFunction(id=>{const n=document.querySelector('#suggestions article#task-'+id);return n&&n.getClientRects().length>0},C);
  assert.equal(cards[C].status,'pending');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('snooze undo and instant done dashboard ok');
}finally{await browser?.close();server.close()}
