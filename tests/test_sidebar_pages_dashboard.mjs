import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The sidebar's pages (made-up data): To-dos (was Suggestions), Learning (was Feedback) with its tabs, and Messages
// (was Events) reached from search, not from a sidebar row. Old links and keys keep working: #suggestions, #feedback,
// #events, G then S, B and E. The palette's Messages group asks api/events like the results page; See all results opens
// that page with the words in its field. How it's going says what each number means, and plainly when there is too little.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const ago=d=>new Date(Date.now()-d*864e5).toISOString();
const ev=(id,title,from)=>({id,account_id:'mail',kind:'gmail.message',title,body:title,occurred_at:ago(id/10),metadata:{from}});
const EVENTS=[ev(1,'Invoice 4821 overdue','Robin Example <robin@acme.example>'),ev(2,'Invoice paid','billing@acme.example'),ev(3,'Invoice copy','Pat Doe <pat@acme.example>'),ev(4,'Invoice question','Sam Roe <sam@acme.example>'),ev(5,'Invoice again','Kim <kim@acme.example>')];
const week=(i,w,d)=>({start:ago(7*(7-i)).slice(0,10),worth_it:w,dismissed:d,open:0,hit_rate:w+d?Math.round(100*w/(w+d)):null,do_it:0,first_time_rate:null,finished_rate:null,changes:i===5?['Skip vendor newsletters']:[]});
const QUALITY={cards:12,worth_it:9,dismissed:3,open:2,hit_rate:75,do_it:4,first_time_rate:75,finished_rate:100,sent_as_written:3,sent_edited:1,
 previous:{hit_rate:60,first_time_rate:75,finished_rate:null},notes:{},by_source:{Email:{worth_it:8,dismissed:2},Slack:{worth_it:1,dismissed:1},WhatsApp:{worth_it:0,dismissed:0}},
 trend:{daily:[],weekly:[0,1,2,3,4,5,6,7].map(i=>i<5?week(i,0,0):week(i,3+i,2))}};
let data,queries;
const base0=()=>({suggestions:[{id:'aa'.repeat(8),title:'Send Sam the contract',body:'',status:'pending',scope:'work',created_at:now,event_ids:[1]}],promises:[],
 connectors:[{id:'mail',service:'gmail',display_name:'mail',email:'owner@example.org',boundary:'work',state:'{}'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],
 review_health:{},review_runs:[],review_live:{runs:[]},fleet:{on:false,fleets:[]},quality:QUALITY,
 facts:[{id:9,kind:'fact',text:'Vendor newsletters never need a to-do.',created_at:now,merged:0}],learning_changes:[]});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(data));return}
 if(url.pathname==='/api/events'){const q=url.searchParams.get('q')||'';queries.push([url.searchParams.get('account'),q]);res.end(JSON.stringify(q?EVENTS.filter(e=>e.title.toLowerCase().includes(q.toLowerCase())):EVENTS));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('q')==null?{counts:{}}:{found:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const open=async(width,height,hash='',patch={})=>{data={...base0(),...patch};queries=[];
 const mobile=width<600,context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.goto(base+hash);await page.locator('#task-'+'aa'.repeat(8)).waitFor({state:'attached'});await page.waitForTimeout(150);return {context,page}};
const shown=page=>page.evaluate(()=>[...document.querySelectorAll('main>section')].find(s=>!s.hidden)?.id);
const learnTabs=page=>page.locator('#learn-tabs [role="tab"]').allTextContents();
const learnPane=page=>page.evaluate(()=>[...document.querySelectorAll('#feedback [data-learn-pane]')].filter(p=>!p.hidden).map(p=>p.dataset.learnPane));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // The rows: To-dos first, no Messages row, Learning with its book icon; the sidebar's own list has no second "To-dos" heading
 {const {context,page}=await open(1440,900);
  assert.deepEqual(await page.evaluate(()=>[...document.querySelectorAll('.app-side nav [data-tab]')].filter(b=>b.offsetHeight).map(b=>b.querySelector('.nl').textContent)),['To-dos','Calendar','Graph','Learning','Connections']);
  assert.equal(await page.title(),'The Machine · To-dos');
  assert.equal(await page.locator('#side-cards .side-label').innerText(),'All\nWork\nPersonal');
  assert.equal(await page.locator('#side-cards .side-label').getAttribute('aria-label'),'To-dos');
  // Old and new links
  for(const [hash,tab] of [['#todos','inbox'],['#messages','events'],['#learning','feedback'],['#suggestions','inbox'],['#events','events'],['#feedback','feedback']]){
   await page.evaluate(h=>{location.hash='';location.hash=h},hash);await page.waitForTimeout(80);assert.equal(await shown(page),tab,hash)}
  assert.equal(await page.locator('#page-head .page-title').textContent(),'Learning');
  // G then a letter, the old letters too; the ? sheet lists only the new ones
  for(const [keys,tab] of [['gt','inbox'],['gl','feedback'],['gs','inbox'],['gb','feedback'],['ge','events']]){
   await page.locator('body').click({position:{x:700,y:5}});for(const k of keys)await page.keyboard.press(k);await page.waitForTimeout(80);assert.equal(await shown(page),tab,keys)}
  await page.keyboard.press('?');await page.locator('#keys-sheet,dialog[open]').first().waitFor();
  const sheet=await page.locator('dialog[open]').innerText();assert.match(sheet,/To-dos/);assert.match(sheet,/Learning/);assert.doesNotMatch(sheet,/Suggestions|Feedback/);
  await page.keyboard.press('Escape');
  await context.close()}
 // The palette's Messages: two letters or more, at most four, who by name only; See all results opens the results page with the words
 {const {context,page}=await open(1440,900);
  await page.keyboard.press('Control+k');await page.locator('#palette').waitFor();await page.keyboard.type('i');await page.waitForTimeout(400);
  assert.ok(!(await page.locator('#pal-list .pal-group').allTextContents()).includes('Messages'),'not on one letter');
  await page.keyboard.type('nvoice');await page.locator('#pal-list .pal-item',{hasText:'Invoice 4821 overdue'}).waitFor();
  assert.deepEqual(queries.at(-1),['all','invoice']);
  const rows=await page.evaluate(()=>{const g=[...document.querySelectorAll('#pal-list .pal-group')].find(x=>x.textContent==='Messages');const out=[];for(let n=g.nextElementSibling;n&&!n.matches('.pal-group');n=n.nextElementSibling)out.push(n.querySelector('.pal-label').textContent);return out});
  assert.deepEqual(rows,['Invoice 4821 overdue','Invoice paid','Invoice copy','Invoice question','See all results for “invoice”']);
  assert.match(await page.locator('#pal-list .pal-item',{hasText:'Invoice 4821 overdue'}).innerText(),/Robin Example/);
  assert.doesNotMatch(await page.locator('#pal-list .pal-item',{hasText:'Invoice 4821 overdue'}).innerText(),/robin@acme/);
  await page.locator('#pal-list .pal-item',{hasText:'See all results'}).click();
  await page.waitForFunction(()=>!document.querySelector('#palette')?.open);assert.equal(await shown(page),'events');
  assert.equal(await page.locator('#query').inputValue(),'invoice');assert.equal(await page.locator('#page-head .page-title').textContent(),'Messages');
  await page.locator('#events-list,#events').getByText('Invoice copy').first().waitFor();
  // A message from the palette opens in the reader
  await page.keyboard.press('Control+k');await page.keyboard.type('invoice paid');await page.locator('#pal-list .pal-item',{hasText:'Invoice paid'}).first().waitFor();
  await page.locator('#pal-list .pal-item',{hasText:'Invoice paid'}).first().click();await page.waitForFunction(()=>!document.querySelector('#palette')?.open);
  await context.close()}
 // On a phone the top bar's search icon opens the same palette, Messages included
 {const {context,page}=await open(390,844);
  await page.locator('#find-open').click();await page.locator('#palette').waitFor();await page.keyboard.type('invoice');
  await page.locator('#pal-list .pal-item',{hasText:'See all results for “invoice”'}).waitFor();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await context.close()}
 // Learning's tabs: a tab with nothing is left out; Team only while something waits; the last one opened comes back
 {const {context,page}=await open(1440,900,'#learning');
  assert.deepEqual(await learnTabs(page),['How it’s going','What I’ve learned']);assert.deepEqual(await learnPane(page),['going']);
  // How it's going: what each number means, compared with the 30 days before; the weekly bars once two weeks have decisions
  const going=await page.locator('#quality').innerText();
  assert.match(going,/Last 30 days\. Higher is better\./);
  assert.match(going,/Worth it\s+75%\s+Of 12 to-dos you decided: acted on, not dismissed\s+Up from 60% the 30 days before/);
  assert.match(going,/First try\s+75%\s+Of 4 to-dos started with Do it: no correction needed\s+Same as the 30 days before/);
  assert.match(going,/Sent as is\s+75%\s+Of 4 drafts sent: no edit or Change first/);
  assert.match(going,/Worth it, week by week/);assert.equal(await page.locator('#quality .bars [role="listitem"]').count(),8);
  assert.match(await page.locator('#quality .bars [role="listitem"]').nth(7).getAttribute('aria-label'),/^Week of .+: 83% worth it, 12 decided$/);
  assert.match(going,/Rules changed that week/);
  assert.match(going,/Worth it per source\s+Where to-dos came from, and how many you acted on of those you decided\.\s+Source\s+Acted on\s+Email\s+8 of 10 80%/);
  assert.match(going,/WhatsApp\s+None decided yet/);
  await page.locator('#learn-tab-learned').click();assert.deepEqual(await learnPane(page),['learned']);
  await page.reload();await page.locator('#task-'+'aa'.repeat(8)).waitFor({state:'attached'});
  await page.locator('.app-side nav [data-tab="feedback"]').click();assert.deepEqual(await learnPane(page),['learned'],'the last tab opened');
  await context.close()}
 {const {context,page}=await open(1440,900,'#learning=team',{decisions:[{id:1,created_at:now,choice:'reject',title:'Newsletter',note:'not needed'}],
   learning_changes:[{id:3,at:now,kind:'fact',text:'Prefers calls after 10:00.',before:null,why:null,undone:false}],
   team_learnings:{offer:true,vote:true,vote_mode:'ask',network:true,ask:null,votes_waiting:[{id:'c1',text:'Group meeting prep into one to-do.',example:null,vote:'up',reason:'Fits.',use_case:null}],shared:[]}});
  assert.deepEqual(await learnTabs(page),['How it’s going','What I’ve learned','Changes','Decisions','Team 1']);assert.deepEqual(await learnPane(page),['team']);
  assert.equal(await page.locator('#learn-tab-team').getAttribute('aria-selected'),'true');
  await page.evaluate(()=>{location.hash='#learning=changes'});await page.waitForFunction(()=>!document.querySelector('#learn-pane-changes').hidden);
  assert.match(await page.locator('#learn-changes').innerText(),/Prefers calls after 10:00\./);
  await context.close()}
 // Too little to show: one plain line and no tab row
 {const {context,page}=await open(390,844,'#learning',{quality:{cards:0,by_source:{},previous:{},trend:{daily:[],weekly:[]}},facts:[]});
  assert.equal((await page.locator('#quality').innerText()).trim(),'Not enough to-dos yet. These numbers start once you decide on a few.');
  assert.ok(await page.locator('#learn-tabs').isHidden());
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('sidebar pages dashboard ok');
}finally{await browser?.close();server.close()}
