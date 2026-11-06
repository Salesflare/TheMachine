import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, Apps, Connected AIs: one row per AI (the server folds an official app's sign-ins into one: ai_access.fold),
// with its name, its tag and one line (access, area, end date, last use), the Messages switch and Change on the row.
// Change opens access, area, Extend, Activity, Turn off now and Remove; nothing of that shows before. Fits a phone.
const dashboard=await dashboardPage();
const soon=new Date(Date.now()+365*86400e3).toISOString(),hour=new Date(Date.now()-20*60e3).toISOString();
const connections=[{id:'aic_gpt',name:'ChatGPT',kind:'oauth',official:true,level:'draft',area:'both',expires_at:soon,expired:false,used_at:hour,messages:true,calls:6,refused:0},
 {id:'aic_claude',name:'Claude',kind:'oauth',official:true,level:'read',area:'work',expires_at:soon,expired:false,used_at:null,messages:false,calls:0,refused:0}];
const asked=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/activity'){res.end(JSON.stringify({items:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);asked.push([action,args]);
  res.end(JSON.stringify({connections,areas:['work','personal'],reach:{}}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1280,800],[390,844]]){
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#settings/ai');
  const rows=page.locator('#ai-list .ai-conn');await rows.first().waitFor();
  assert.equal(await rows.count(),2);
  const gpt=rows.nth(0);
  assert.match(await gpt.locator('small').innerText(),/^Read & edit · Work and Personal · until .+ · last used 20 minutes ago$/);
  assert.match(await rows.nth(1).locator('small').innerText(),/^Read · Work only · until .+ · not used yet$/);
  assert.equal(await gpt.locator('.alpha').innerText().then(s=>s.toLowerCase()),'official app');
  // On the row: the Messages switch and Change, nothing else
  assert.equal(await gpt.locator('[data-ai-messages]').getAttribute('aria-checked'),'true');
  assert.deepEqual(await gpt.locator('button').evaluateAll(b=>b.map(x=>x.textContent.trim())),['','Change']);
  assert.equal(await page.locator('#ai-list select, #ai-list [data-ai-off], #ai-list [data-ai-remove], #ai-list [data-ai-activity]').count(),0);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${width}: no sideways scroll`);
  // Change: its controls, for that AI only
  await gpt.locator('[data-ai-edit]').click();
  const edit=page.locator('#ai-list .ai-edit');await edit.waitFor();
  assert.equal(await edit.getAttribute('data-ai'),'aic_gpt');
  assert.equal(await edit.locator('select').count(),3);
  assert.deepEqual(await edit.locator('button').allInnerTexts(),['Activity','Turn off now','Remove']);
  assert.equal(await page.locator('#ai-list [data-ai-edit][aria-expanded="true"]').count(),1);
  await edit.locator('[data-ai-level]').selectOption('read');
  await new Promise(r=>setTimeout(r,200));
  assert.deepEqual(asked.at(-1),['ai_change',{id:'aic_gpt',level:'read'}]);
  await page.locator('#ai-list [data-ai="aic_gpt"] [data-ai-activity]').click();await page.locator('#ai-list .ai-activity').waitFor();
  assert.ok(!(await page.locator('#settings-ai').innerText()).includes('—'),'no em dashes');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${width}: no sideways scroll, open`);
  // The switch works on the row, Change again closes it
  await rows.nth(1).locator('[data-ai-messages]').click();await new Promise(r=>setTimeout(r,200));
  assert.deepEqual(asked.at(-1),['ai_change',{id:'aic_claude',messages:true}]);
  await page.locator('#ai-list [data-ai="aic_gpt"] [data-ai-edit]').click();
  assert.equal(await page.locator('#ai-list .ai-edit, #ai-list .ai-activity').count(),0);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('ok');
}finally{await browser?.close();server.close()}
