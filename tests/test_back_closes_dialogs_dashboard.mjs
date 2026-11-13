import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// On a phone, back (the gesture, the button, the app's back) closes the open dialog or sheet and the page stays: the
// same address, no reload. Nested dialogs close one at a time, topmost first. One closed with its × takes its history
// step back off, so the next back is a real one. A dialog a push link opened (#digest=…) closes the same way. A to-do's
// menu sheet closes too. On a computer, opening a dialog adds no history step.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const card={id:'a1b2c3d4e5f60718',title:'Reply about the partnership',body:'Draft ready.',status:'pending',scope:'work',created_at:now,event_ids:[2]};
const state={suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}};
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const errors=[];
const open=(page,sel)=>page.evaluate(sel=>!!document.querySelector(sel)?.open,sel);
// history.back() as the gesture does it (its popstate is the dialogs' own: the page's other handlers sit it out)
const back=async page=>{await page.evaluate(()=>history.back());await page.waitForTimeout(250)};
const settle=page=>page.waitForTimeout(150);
async function phone(){
 const ctx=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'en-US'});
 await ctx.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 const page=await ctx.newPage();page.on('pageerror',e=>errors.push(e.message));return {ctx,page}}
try{
 {const {ctx,page}=await phone();
  await page.goto(base);await page.locator('#task-'+card.id).waitFor();
  await page.evaluate(()=>{window.stayed=1});const href=await page.evaluate(()=>location.href);
  // one dialog: back closes it, the page stays
  await page.evaluate(id=>openSnooze(id),card.id);assert.ok(await open(page,'#snooze-dialog'));
  await back(page);await settle(page);
  assert.equal(await open(page,'#snooze-dialog'),false,'back closes the dialog');
  assert.equal(await page.evaluate(()=>location.href),href);assert.equal(await page.evaluate(()=>window.stayed),1,'no reload');
  assert.ok(await page.locator('#task-'+card.id).isVisible());
  // closed with its ×: the next back is a real one (the step it left is skipped), to the address before
  await page.evaluate(()=>history.pushState(null,'','?p=1'));
  await page.evaluate(id=>openSnooze(id),card.id);assert.ok(await page.evaluate(()=>history.state?.layer>0));
  await page.locator('#snooze-dialog .snooze-heading button').first().click();await settle(page);
  assert.equal(await open(page,'#snooze-dialog'),false);
  await back(page);await settle(page);
  assert.equal(await page.evaluate(()=>location.href),href,'one back leaves the page the dialog was on');assert.equal(await page.evaluate(()=>window.stayed),1);
  // nested: one at a time, topmost first
  await page.evaluate(id=>{openSnooze(id);document.querySelector('#result-dialog').showModal()},card.id);
  assert.ok(await open(page,'#snooze-dialog')&&await open(page,'#result-dialog'));
  await back(page);await settle(page);
  assert.equal(await open(page,'#result-dialog'),false,'the top one closes first');assert.ok(await open(page,'#snooze-dialog'),'the one under it stays');
  await back(page);await settle(page);
  assert.equal(await open(page,'#snooze-dialog'),false);
  assert.equal(await page.evaluate(()=>location.href),href);assert.equal(await page.evaluate(()=>window.stayed),1);
  // a to-do's menu, a sheet on a phone
  await page.locator(`#task-${card.id} .more-actions>summary`).click();await settle(page);
  assert.ok(await open(page,`#task-${card.id} .more-actions`));
  await back(page);await settle(page);
  assert.equal(await open(page,`#task-${card.id} .more-actions`),false,'back closes the menu sheet');
  // what the phone app asks first: closes the top one, and says when there was nothing
  await page.evaluate(id=>openSnooze(id),card.id);
  assert.equal(await page.evaluate(()=>machineBack()),true);await settle(page);
  assert.equal(await open(page,'#snooze-dialog'),false);assert.equal(await page.evaluate(()=>machineBack()),false);
  await ctx.close()}
 // a push link opens the morning digest: back closes it and stays on the page
 {const {ctx,page}=await phone();
  await page.goto(base+'#digest=morning');await page.locator('#area-digest[open]').waitFor();await settle(page);
  await page.evaluate(()=>{window.stayed=1});
  await back(page);await settle(page);
  assert.equal(await open(page,'#area-digest'),false,'back closes the digest');
  assert.equal(await page.evaluate(()=>location.pathname+location.hash),'/');assert.equal(await page.evaluate(()=>window.stayed),1);
  assert.ok(await page.locator('#task-'+card.id).isVisible());
  await ctx.close()}
 // a computer: no history step, as before
 {const ctx=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
  await ctx.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
  const page=await ctx.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('#task-'+card.id).waitFor();
  const len=await page.evaluate(()=>history.length);
  await page.evaluate(id=>openSnooze(id),card.id);assert.ok(await open(page,'#snooze-dialog'));
  assert.equal(await page.evaluate(()=>history.length),len);assert.equal(await page.evaluate(()=>history.state?.layer),undefined);
  await ctx.close()}
 assert.deepEqual(errors,[]);
 console.log('ok');
}finally{await browser.close();server.close()}
