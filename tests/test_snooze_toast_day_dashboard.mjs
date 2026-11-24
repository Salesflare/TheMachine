import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The Snoozed toast says the day the to-do comes back as the snooze buttons mean it. The owner's day starts at 03:00
// (machine/cards.py snooze_time): Tomorrow pressed at 01:41 is 08:00 that same calendar morning, and the toast said
// "today at 08:00" under a "Tomorrow" button. And it shows only once a time is picked: an earlier to-do's toast goes
// when the picker opens for another one. Made-up to-dos, Brussels time; nothing is sent. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const A='a1'.repeat(8),B='b2'.repeat(8);
let until,now,actions;
const status=()=>({suggestions:[
  {id:A,title:'Send the bakery the menu quote',body:'They asked for prices.',status:'pending',scope:'work',created_at:now,event_ids:[1]},
  {id:B,title:'Ask the landlord about the boiler',body:'It made a noise again.',status:'pending',scope:'personal',created_at:now,event_ids:[2]}],
 promises:[],connectors:[],suggestion_counts:{pending:2},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],reminders:{telegram:false,push:0}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);
  res.end(JSON.stringify(r.action==='decide'?{status:'snoozed',snoozed_until:until}:{}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const line=page=>page.evaluate(()=>{const t=document.querySelector('#toast');return t.classList.contains('show')?t.firstChild.textContent.trim():null});
// Brussels is UTC+1 in November
const CASES=[
 ['2026-11-17T00:41:00Z','2026-11-17T07:00:00Z','Snoozed until tomorrow 08:00. It’ll be back here then.'],  // 01:41: Tomorrow is this calendar morning
 ['2026-11-17T11:00:00Z','2026-11-18T07:00:00Z','Snoozed until tomorrow 08:00. It’ll be back here then.'],  // noon: the next day
 ['2026-11-17T11:00:00Z','2026-11-17T13:00:00Z','Snoozed until 14:00. It’ll be back here then.'],     // in 2 hours
 ['2026-11-17T01:30:00Z','2026-11-17T04:30:00Z','Snoozed until tomorrow 05:30. It’ll be back here then.']]; // 02:30, 3 hours on: past 03:00, the owner's next day
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [clock,back,said] of CASES){now=clock;until=back;actions=[];
  const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-GB',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.clock.setFixedTime(new Date(clock));
  const page=await context.newPage();page.on('pageerror',e=>errors.push(clock+': '+e.message));
  await page.goto(base);await page.locator('#task-'+A).waitFor();
  await page.evaluate(id=>openSnooze(id),A);await page.locator('#snooze-dialog [data-snooze="tomorrow"]').click();
  await page.waitForFunction(()=>document.querySelector('#toast').classList.contains('show'));
  assert.equal(await line(page),said,clock+' → '+back);
  await context.close()}
 // Shown only after a time is picked: the picker for another to-do hides the earlier one's toast, light and dark, phone and computer
 for(const [width,height,scheme] of [[390,844,'light'],[1440,900,'dark'],[390,844,'dark'],[1440,900,'light']]){const mobile=width<600;
  now='2026-11-17T00:41:00Z';until='2026-11-17T07:00:00Z';actions=[];
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-GB',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.clock.setFixedTime(new Date(now));
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto(base);await page.locator('#task-'+A).waitFor();
  await page.evaluate(id=>openSnooze(id),A);await page.locator('#snooze-dialog [data-snooze="tomorrow"]').click();
  await page.waitForFunction(()=>document.querySelector('#toast').classList.contains('show'));
  if(shots)await page.screenshot({path:`${shots}/snooze-toast-${width}-${scheme}.png`});
  await page.evaluate(id=>openSnooze(id),B);await page.locator('#snooze-dialog').waitFor();
  assert.equal(await line(page),null,'no Snoozed toast over the picker before a time is picked');
  if(shots){await page.waitForFunction(()=>getComputedStyle(document.querySelector('#toast')).visibility==='hidden'||getComputedStyle(document.querySelector('#toast')).opacity==='0');await page.screenshot({path:`${shots}/snooze-picker-${width}-${scheme}.png`})}
  await page.locator('#snooze-dialog [data-snooze="tomorrow"]').click();
  await page.waitForFunction(()=>document.querySelector('#toast').classList.contains('show'));
  assert.equal(await page.locator('#toast [data-unsnooze]').getAttribute('data-unsnooze'),B,'the toast is the one just picked');
  assert.equal(actions.filter(r=>r.action==='decide').length,2);
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
