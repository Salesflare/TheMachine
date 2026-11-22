import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A usage limit reset offered above the to-dos (dashboard/todos-reset-nudge.js, state.reset_nudge from
// ModelPacingApp.reset_nudge): one quiet line while a window holds work back and resets are left, with Settings' own
// Use a reset (its confirm first; a cancel posts nothing) and × to hide it until that window resets. Gone without resets
// and in a to-do's chat. A fake server answers: no account is reached and no reset is ever used.
const dashboard=await dashboardPage();
const NOW=Date.parse('2026-11-09T16:20:00Z'),at=m=>new Date(NOW+m*6e4).toISOString(),until=NOW/1000+3*86400;
const week={window:'week',used:92,until,name:'ChatGPT',resets:2,reached:false};
const posted=[];
const state=()=>({suggestions:[{id:'a1'.repeat(8),title:'Answer about API limits',body:'',status:'prepared',scope:'work',created_at:at(-10),event_ids:[1]}],
 promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{last_completed:at(-9)},review_runs:[],review_live:{runs:[]},connectors:[],
 check:{reviewed:at(-9),waiting:0},reset_nudge:week,model_status:{chatgpt:true,can_reset:true,resets:{available:2,credits:[]},windows:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'12',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){let body='';req.on('data',c=>body+=c);req.on('end',()=>{posted.push(JSON.parse(body));res.end('{"outcome":"reset"}')});return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440]){
  const context=await browser.newContext({viewport:{width,height:844},locale:'en-US',timezoneId:'UTC'});
  await context.clock.setFixedTime(NOW);
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');
  const line=page.locator('#suggestions .reset-nudge');await line.waitFor();
  const show=n=>page.evaluate(n=>{state.reset_nudge=n;render();const l=document.querySelector('#suggestions .reset-nudge');
   return l?{text:l.querySelector('span').textContent.trim(),wide:document.documentElement.scrollWidth>innerWidth,rows:Math.round(l.getBoundingClientRect().height)}:null},n);
  let r=await show(week);
  assert.equal(r.text,'ChatGPT weekly limit 92% used. Preparing is slowed. 2 resets left.');
  assert.ok(!r.wide,`${width}: no sideways scroll`);
  assert.equal(await line.locator('[data-model-reset]').innerText(),'Use a reset');
  r=await show({...week,window:'5h',used:70,resets:1});
  assert.equal(r.text,'ChatGPT 5-hour limit 70% used. Preparing is slowed. 1 reset left.');
  r=await show({...week,reached:true});  // the limit banner above says it is reached
  assert.equal(r.text,'2 resets left.');
  assert.equal(await show(null),null,'nothing without a nudge');
  assert.equal(await show({...week,resets:0}),null,'nothing new without resets');
  // Use a reset is Settings' own: its confirm first, never a reset on its own
  await show(week);
  page.once('dialog',d=>{assert.match(d.message(),/^This uses 1 of your 2 resets\./);d.dismiss()});
  await page.click('#suggestions .reset-nudge [data-model-reset]');
  await page.waitForTimeout(100);
  assert.deepEqual(posted,[],'a cancel posts nothing');
  page.once('dialog',d=>d.accept());
  await page.click('#suggestions .reset-nudge [data-model-reset]');
  await page.waitForFunction(()=>/Usage reset/.test(document.body.innerText));
  assert.equal(posted.pop().action,'model_reset');
  // × hides it for that window's period, in this browser; the next period shows it again
  await show(week);await page.click('#suggestions [data-reset-nudge-x]');
  assert.equal(await page.locator('#suggestions .reset-nudge').count(),0);
  assert.equal(await show(week),null,'stays hidden for the same period');
  assert.equal(await show({...week,used:97}),null,'also as it fills up');
  assert.ok(await show({...week,until:until+7*86400}),'a new period shows it again');
  assert.ok(await show({...week,window:'5h',until:NOW/1000+3600}),'another window shows it');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('reset nudge dashboard ok');
}finally{await browser?.close();server.close()}
