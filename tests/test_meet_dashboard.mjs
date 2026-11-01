import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Scheduling between Machines (meet_app.py, dashboard/todos-meet.js): a time two Machines agreed is a to-do with Book
// it, Other time and Not needed, each the owner's own tap (meet_decide); after Book it the to-do waits for the other
// person, and the invite goes out once both tapped. The setting sits in the Network pane, its Activity lines under
// Settings. Never scrolls sideways (390px and 1280px, light and dark). Optional SHOT_DIR: screenshots of each.
const dashboard=await dashboardPage();
const SHOTS=process.env.SHOT_DIR||'',now=new Date().toISOString();
const FR='fr_'+'b'.repeat(16);
const proposed=()=>({state:'proposed',role:'asker',name:'Alex Example',minutes:30,video:'Zoom',mine_ok:false,their_ok:false,note:null,
 title:'Meet Alex Example',when:'Tue 3 Nov 14:00',start:'2026-11-03T13:00Z'});
let meet,setting;
const card=()=>({id:'m1',title:meet.title||'Reply to Alex about next week',body:'Alex asked to meet next week.',status:'pending',scope:'work',created_at:now,event_ids:[1],
 source_line:'Source: email from Alex Example',meet});
const fleet=()=>({on:true,kinds:{},kind_rules:{},no_details:[],scoped:[],scopes:{},waiting:[],asked:[],log:[],notices:[],splits:[],
 fleets:[{id:FR,kind:'friends',label:'Friends',name:'Friends',asks:[],people:[{member_id:'fp_me',name:'Sam Doe',me:true}],members:[]}],
 friends:{id:FR,username:'sam',in:[],out:[],blocked:[]},network:{find:true,discoverable:true,asked:true,last:null,people:[],addresses:[]},meet:setting});
const day=(h)=>new Date(Date.now()-h*36e5).toISOString();
const LINES=[{id:'meet:3',kind:'calendar',at:day(1),what:'Meeting booked with Alex Example: Tue 3 Nov 14:00',where:'The Machine Network',outcome:'done',status:'Booked',by:null,todo:{id:'m1',title:'Meet Alex Example'},detail:null},
 {id:'meet:2',kind:'calendar',at:day(2),what:'Time proposed to Alex Example: Tue 3 Nov 14:00',where:'The Machine Network',outcome:'done',status:'Sent',by:null,todo:{id:'m1',title:'Meet Alex Example'},detail:null},
 {id:'meet:1',kind:'calendar',at:day(3),what:'Free times asked by Jo Sample: Mon 2 Nov to Fri 13 Nov',where:'The Machine Network',outcome:'refused',status:'Refused',by:null,todo:null,detail:'No email exchange with them'}];
const calls=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status')return res.end(JSON.stringify({suggestions:[card()],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],connectors:[],fleet:{on:true,waiting:0}}));
 if(url.pathname.startsWith('/api/fleet'))return res.end(JSON.stringify(fleet()));
 if(url.pathname==='/api/activity')return res.end(JSON.stringify({items:LINES,next:null,kinds:['calendar']}));
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='meet_decide'){
   if(call.args.choice==='book'){meet={...meet,mine_ok:true};return res.end(JSON.stringify({state:'proposed'}))}
   if(call.args.choice==='other'){meet={state:'waiting',role:'asker',name:'Alex Example',minutes:30,mine_ok:false,their_ok:false};return res.end(JSON.stringify({state:'waiting'}))}}
  if(call.action==='meet_setting'){setting={...setting,...call.args};return res.end(JSON.stringify(setting))}
  return res.end('{"ok":true}')}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const sideways=page=>page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
try{
 for(const [width,height] of [[1280,900],[390,844]])for(const scheme of ['light','dark']){
  meet=proposed();setting={allow:'freebusy',minutes:30,buffer:10,prefer:'any'};calls.length=0;
  const phone=width<600,context=await browser.newContext({viewport:{width,height},isMobile:phone,hasTouch:phone,colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage(),errors=[],tag=`${width}-${scheme}`;page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  const todo=page.locator('#task-m1');await todo.waitFor();
  assert.equal((await todo.locator('h3').first().textContent()).trim(),'Meet Alex Example');  // the time is the line below, once
  assert.match(await todo.locator('.meet-line').textContent(),/Tue 3 Nov 14:00 · 30 min · Zoom\?/);
  assert.match(await todo.locator('.meet-line').textContent(),/Free for you both\. The invite goes out once you both tap Book it\./);
  assert.deepEqual(await todo.locator('[data-meet-do]').evaluateAll(n=>n.map(x=>x.textContent)),['Book it','Other time','Not needed']);
  assert.ok(await sideways(page)<=0,'no sideways scroll on the to-do');
  if(SHOTS)await todo.screenshot({path:`${SHOTS}/meet-todo-${tag}.png`});
  // Book it: the owner's own tap; nothing else goes, and the to-do then waits for the other person
  await todo.locator('[data-meet-do="book"]').click();
  await page.locator('#toast',{hasText:'Done. Waiting for them to tap Book it.'}).waitFor();
  await todo.locator('.meet-line',{hasText:'Waiting for Alex Example to tap Book it.'}).waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args]),[['meet_decide',{suggestion_id:'m1',choice:'book'}]]);
  assert.equal(await todo.locator('[data-meet-do="book"]').count(),0);
  if(SHOTS)await todo.screenshot({path:`${SHOTS}/meet-booked-waiting-${tag}.png`});
  // Other time: their Machine is asked again
  calls.length=0;await todo.locator('[data-meet-do="other"]').click();
  await page.locator('#toast',{hasText:'Looking for another time.'}).waitFor();
  await todo.locator('.meet-line',{hasText:'Asked Alex Example’s Machine for another time.'}).waitFor();
  assert.deepEqual(calls.map(c=>c.args.choice),['other']);
  // The setting, in the Network pane
  await navClick(page.locator('nav [data-tab="fleet"]'));await page.locator('[data-fleet-pane="network"]').click();
  const box=page.locator('.meet-setting');await box.waitFor();
  assert.equal(await box.locator('[data-meet-pref="allow"]').inputValue(),'freebusy');  // the default
  if(SHOTS){await box.scrollIntoViewIfNeeded();await box.screenshot({path:`${SHOTS}/meet-setting-${tag}.png`})}
  calls.length=0;await box.locator('[data-meet-pref="minutes"]').selectOption('45');
  await page.locator('#toast',{hasText:'Saved.'}).waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args]),[['meet_setting',{minutes:45}]]);
  calls.length=0;await box.locator('[data-meet-pref="allow"]').selectOption('off');
  await page.locator('#toast',{hasText:'Off. Other Machines can’t ask yours.'}).waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args]),[['meet_setting',{allow:'off'}]]);
  await page.waitForFunction(()=>document.querySelector('.meet-setting [data-meet-pref="buffer"]')?.disabled);
  assert.ok(await sideways(page)<=0,'no sideways scroll in the Network pane');
  // Activity: who asked, which window, what slot; no event details
  await page.goto('http://127.0.0.1:'+server.address().port+'/#settings/activity');await page.reload();
  const list=page.locator('#act-list');await list.locator('.act-row').first().waitFor();
  const text=await list.innerText();
  assert.match(text,/Meeting booked with Alex Example: Tue 3 Nov 14:00/);
  assert.match(text,/No email exchange with them/);
  assert.ok(await sideways(page)<=0,'no sideways scroll in Activity');
  if(SHOTS)await page.screenshot({path:`${SHOTS}/meet-activity-${tag}.png`});
  assert.deepEqual(errors,[]);
  await context.close();
 }
 console.log('meet dashboard ok');
}finally{await browser.close();server.close()}
