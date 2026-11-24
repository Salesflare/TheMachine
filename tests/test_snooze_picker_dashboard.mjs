import assert from 'node:assert/strict';
import {mkdir,readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The Snooze picker says which to-do it is for (its title, at most two lines) and when that is due, and offers a moment
// before the deadline when the Machine has one (snooze_due, machine/cards.py); any other time stays the owner's to pick.
// The toast then says until when, in the device's time zone and the owner's language, from every way in (the card, the
// S key, a row's menu, a notification's button). Made-up to-dos; nothing is sent. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const nl=await readFile(new URL('../i18n/nl.json',import.meta.url),'utf8'),en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const A='a1'.repeat(8),B='b2'.repeat(8),NOW='2026-11-17T11:00:00Z',BACK='2026-11-18T07:00:00Z',BEFORE='2026-11-19T07:00:00+00:00';  // a Tuesday noon in Brussels
const LONG='Send the bakery on the corner the quote for the spring menu, with the prices per tray and the delivery days they asked about twice';
let actions=[],lang='en';
const choices=[['2h','2 hours'],['tomorrow','Tomorrow · 8:00'],['3d','3 days · 8:00'],['1w','1 week · 8:00']];
const status=()=>({suggestions:[
  {id:A,title:LONG,body:'They asked for prices.',status:'pending',scope:'work',created_at:NOW,event_ids:[1],due:'2026-11-20',snooze_choices:choices,snooze_due:[BEFORE,'Before it’s due · Thu 8:00']},
  {id:B,title:'Ask the landlord about the boiler',body:'It made a noise again.',status:'pending',scope:'personal',created_at:NOW,event_ids:[2],snooze_choices:choices}],
 promises:[],connectors:[],suggestion_counts:{pending:2},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],reminders:{telegram:false,push:1},
 locale:{locale:'en-BE',region:'BE',language:lang,language_set:true,clock:'auto',hour12:false,auto_hour12:false,date_locale:lang==='en'?'en-GB':'nl-BE',languages:{en:'English',nl:'Nederlands'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/nl.json'){res.end(nl);return}
 if(url.pathname==='/i18n/en.json'){res.end(en);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push(r);
  res.end(JSON.stringify(r.action==='decide'?{status:'snoozed',snoozed_until:r.args.snoozed_until||BACK}:{}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const said=async page=>{await page.waitForFunction(()=>document.querySelector('#toast').classList.contains('show'));return page.evaluate(()=>document.querySelector('#toast').firstChild.textContent.trim())};
const open=async({width=1440,height=900,scheme='light',zone='Europe/Brussels'}={})=>{const mobile=width<600;actions=[];
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-GB',timezoneId:zone});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await context.clock.setFixedTime(new Date(NOW));
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+' '+scheme+': '+e.message));
 await page.goto(base);await page.locator('#task-'+A).waitFor();return {context,page}};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900],[1440,700]])for(const scheme of ['light','dark']){const {context,page}=await open({width,height,scheme});
  await page.evaluate(id=>openSnooze(id),A);await page.locator('#snooze-dialog[open]').waitFor();
  const look=await page.evaluate(()=>{const d=document.querySelector('#snooze-dialog'),t=document.querySelector('#snooze-for>span'),c=document.querySelector('#snooze-for .chip'),dr=d.getBoundingClientRect(),tr=t.getBoundingClientRect(),first=d.querySelector('[data-snooze]').getBoundingClientRect();
   return {title:t.textContent,lines:Math.round(t.clientHeight/parseFloat(getComputedStyle(t).lineHeight)),cut:t.scrollHeight>t.clientHeight,inside:tr.left>=dr.left+8&&tr.right<=dr.right-8,due:c?.textContent,chipIn:c&&c.getBoundingClientRect().right<=dr.right,above:c.getBoundingClientRect().bottom<=first.top,wide:d.scrollWidth<=d.clientWidth,
    described:d.getAttribute('aria-describedby'),rows:[...d.querySelectorAll('[data-snooze]')].map(b=>b.textContent)}});
  assert.deepEqual(look,{title:LONG,lines:2,cut:true,inside:true,due:'Due Friday',chipIn:true,above:true,wide:true,described:'snooze-for',rows:[...choices.map(x=>x[1]),'Before it’s due · Thu 8:00']});
  if(shots)await page.screenshot({path:`${shots}/picker-${width}x${height}-${scheme}.png`});
  // The month keeps naming it
  await page.locator('#snooze-custom').click();assert.ok(await page.locator('#snooze-for').isVisible());
  if(shots)await page.screenshot({path:`${shots}/picker-month-${width}x${height}-${scheme}.png`});
  await page.locator('#snooze-back').click();
  await page.locator('#snooze-dialog [data-snooze]').last().click();
  assert.equal(await said(page),'Snoozed until Thursday 08:00. I’ll send you a notification.');
  const sent=actions.find(a=>a.action==='decide').args;assert.deepEqual([sent.choice,sent.snoozed_until,sent.snooze_option],['snooze',BEFORE,undefined]);
  if(shots)await page.screenshot({path:`${shots}/toast-${width}x${height}-${scheme}.png`,animations:'disabled'});
  // Another one: its own title, no due left over
  await page.evaluate(id=>openSnooze(id),B);
  assert.deepEqual(await page.locator('#snooze-for>*').allTextContents(),['Ask the landlord about the boiler']);
  await page.locator('#snooze-dialog [data-snooze="tomorrow"]').click();
  assert.equal(await said(page),'Snoozed until tomorrow 08:00. I’ll send you a notification.');
  await context.close()}
 // The S key and a notification's quick button say the same
 {const {context,page}=await open();
  for(let i=0;i<4&&await page.evaluate(()=>document.activeElement.id)!=='task-'+B;i++)await page.keyboard.press('j');
  await page.keyboard.press('s');await page.locator('#snooze-dialog[open]').waitFor();
  assert.equal(await page.locator('#snooze-for>span').textContent(),'Ask the landlord about the boiler');
  await page.locator('#snooze-dialog [data-snooze="1w"]').click();
  assert.equal(await said(page),'Snoozed until tomorrow 08:00. I’ll send you a notification.');
  await page.evaluate(()=>document.querySelector('#toast').classList.remove('show'));
  await page.evaluate(id=>quickRun(id,'snooze'),A);
  assert.equal(await said(page),'Snoozed until tomorrow 08:00. I’ll send you a notification.');
  await context.close()}
 // A device in another time zone says its own time; another language says it whole
 {const {context,page}=await open({zone:'America/New_York'});
  await page.evaluate(id=>openSnooze(id),B);await page.locator('#snooze-dialog [data-snooze="tomorrow"]').click();
  assert.equal(await said(page),'Snoozed until 02:00. I’ll send you a notification.');  // before 03:00 is still the owner's today
  await context.close()}
 lang='nl';{const {context,page}=await open({width:390,height:844});
  await page.locator('html[lang="nl"]').waitFor({state:'attached'});
  await page.evaluate(id=>openSnooze(id),A);await page.locator('#snooze-dialog [data-snooze]').last().click();
  assert.equal(await said(page),'Gesnoozed tot donderdag 08:00. Ik stuur je een melding.');
  if(shots)await page.screenshot({path:`${shots}/toast-390-nl.png`,animations:'disabled'});
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('snooze picker ok');
