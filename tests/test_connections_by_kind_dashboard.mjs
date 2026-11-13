import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections by kind. On a computer the kinds sit on the left beside the one open; on a phone they are a list of their
// own (with what each holds) and a kind opens as its own page, with "‹ Connections" back. A kind lists its accounts as
// rows (Work or Personal first, then how it is and what came in lately); a row opens its full card. Then "Add another"
// with that kind's sources. Sign-ins and Checks sit below a line. A kind with a source that needs you shows how many and
// opens first; #connections=<kind> and the old #connections=add still land in a kind.
// SHOTS=<folder> saves each width and theme.
const dashboard=await dashboardPage();
const at=new Date().toISOString();
const card=(id,service,group,title,subtitle,more)=>({id,service,group,card_title:title,card_subtitle:subtitle,display_name:title,email:title,boundary:'personal',
 last_success:at,last_sync_signals:2,sync_activity:[],failures_24h:0,read_window:{},total:40,signals_24h:5,pending:0,...more});
const connectors=[card('m1','gmail','mail','sam@example.org','Personal',{signals_24h:18}),card('m2','gmail','mail','sam@work.example','Work',{boundary:'work'}),
 card('c1','calendar','calendar','sam@example.org','Personal',{upcoming_7d:9}),
 card('x1','x','chat','@sam','Personal',{error:'x_signed_out'})];
const S=(name,label,group,extra={})=>({name,service:name,label,group,what:'What '+label+' brings in.',connected:0,broker:false,...extra});
const sources=[S('gmail','Gmail','mail',{connected:2}),S('outlook','Outlook','mail'),S('calendar','Google Calendar','calendar',{connected:1}),
 S('x','X','chat',{connected:1}),S('slack','Slack','chat'),S('zoom','Zoom','meetings')];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,sources,suggested:[],codex:{status:'signed_out'}}));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const look=page=>page.evaluate(()=>{const vis=el=>!!el&&el.getClientRects().length>0;
 return {cats:[...document.querySelectorAll('#health-tabs .conn-cat')].filter(vis).map(b=>({id:b.dataset.healthPane,label:b.querySelector('.ell').textContent,
   sub:vis(b.querySelector('small'))?b.querySelector('small').textContent:null,badge:b.querySelector('.badge')?.textContent||null,on:b.getAttribute('aria-selected')==='true'})),
  line:vis(document.querySelector('.conn-cats-line')),title:vis(document.querySelector('#conn-title'))?document.querySelector('#conn-title').textContent:null,
  back:vis(document.querySelector('[data-conn-back]')),
  rows:[...document.querySelectorAll('#connectors>article')].filter(vis).map(a=>({id:a.dataset.conn,status:a.querySelector('.conn-row small').textContent.replace(/\s+/g,' ').trim(),
   open:vis(a.querySelector('.conn-body'))})),
  add:[...document.querySelectorAll('#connect-add .connect-group')].filter(vis).map(g=>({head:g.querySelector('h4')?.textContent||null,tiles:[...g.querySelectorAll('.connect-source b')].map(b=>b.textContent)})),
  width:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth}});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,mobile] of [[390,844,true],[1440,900,false]])for(const scheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}-${scheme}`,shot=async name=>{if(shots)await page.screenshot({path:`${shots}/${tag}-${name}.png`,fullPage:true})};
  await page.goto(base+'/#connections');
  await page.locator('#health-tabs .conn-cat').first().waitFor();await page.locator('#connect-add .connect-source').first().waitFor({state:'attached'});await page.waitForTimeout(300);
  let v=await look(page);
  assert.deepEqual(v.cats.map(c=>c.label),['Email','Calendar','Chat','Meetings','Projects and code','Checks'],`${tag}: the kinds with a source (Codex: Projects and code), then Checks below the line`);
  // Checks apart: below a line on a computer, its own small card on a phone; every kind shows an icon, one per source
  assert.equal(v.line,!mobile,`${tag}: a line above Checks on a computer`);
  assert.deepEqual(await page.locator('#health-tabs .conn-cats-part').evaluateAll(p=>p.map(x=>x.querySelectorAll('.conn-cat').length)),[5,1],`${tag}: the kinds, then Checks apart`);
  if(mobile)assert.deepEqual(await page.locator('#health-tabs .conn-cat').evaluateAll(b=>b.map(x=>x.querySelectorAll('.conn-logos .icon').length)),[1,1,1,1,1,1],`${tag}: one icon per source, a plain one for a kind without`);
  assert.equal(v.cats.find(c=>c.id==='chat').badge,'1',`${tag}: Chat says one needs you`);
  assert.deepEqual(v.cats.filter(c=>c.badge).map(c=>c.id),['chat'],`${tag}: only a kind that needs you has a number`);
  assert.ok(v.scroll<=v.width,`${tag}: no sideways scroll`);
  if(mobile){
   // the list of kinds, with what each holds; no kind open yet
   assert.deepEqual(v.cats.map(c=>c.sub),['2 connected','sam@example.org','Needs your help','Not connected','Not connected',null],`${tag}: the list says what each kind holds`);
   assert.deepEqual([v.title,v.rows.length,v.back],[null,0,false],`${tag}: on a phone, Connections opens on the list`);
   await shot('list');
   await page.locator('#health-tabs [data-health-pane="mail"]').click();await page.waitForTimeout(200);v=await look(page);
   assert.deepEqual([v.title,v.back,v.cats.length],['Email',true,0],`${tag}: a kind opens as its own page, with a way back`);
  }else{
   // the kind that needs you opens first
   assert.deepEqual([v.title,v.cats.find(c=>c.on)?.id],['Chat','chat'],`${tag}: the kind that needs you opens first`);
   assert.deepEqual(v.rows.map(r=>[r.id,r.open]),[['x1',true]],`${tag}: a card that needs you opens by itself`);
   assert.equal(v.back,false,`${tag}: no way back beside the list`);
   assert.deepEqual(v.cats.map(c=>c.sub),[null,null,null,null,null,null],`${tag}: the list beside a kind is just names`);
   await page.locator('#health-tabs [data-health-pane="mail"]').click();await page.waitForTimeout(200);v=await look(page);
   assert.deepEqual([v.title,v.cats.find(c=>c.on)?.id],['Email','mail'],`${tag}: a kind opens beside the list`);
  }
  // Email: its rows, Work or Personal first, closed; then Add another with its sources
  assert.deepEqual(v.rows.map(r=>[r.id,r.open]),[['m1',false],['m2',false]],`${tag}: Email's rows, A to Z, closed`);
  for(const r of v.rows)assert.match(r.status,/^(Work|Personal) · /,`${tag}: ${r.id} starts with Work or Personal (${r.status})`);
  assert.match(v.rows.find(r=>r.id==='m1').status,/18 last 24h$/,`${tag}: what came in lately`);
  assert.deepEqual(v.add,[{head:'Add another',tiles:['Gmail','Outlook']}],`${tag}: Add another, with Email's sources only`);
  await shot('email');
  // a row opens its full card, and closes it again
  await page.locator('[data-conn-open="m1"]').click();v=await look(page);
  assert.equal(v.rows.find(r=>r.id==='m1').open,true,`${tag}: the row opens its card`);
  assert.equal(await page.locator('#connectors>article[data-conn="m1"] .conn-body .figures').count(),1,`${tag}: the full card, with its figures`);
  assert.equal(await page.locator('[data-conn-open="m1"]').getAttribute('aria-expanded'),'true');
  await shot('card');
  await page.locator('[data-conn-open="m1"]').click();v=await look(page);
  assert.equal(v.rows.find(r=>r.id==='m1').open,false,`${tag}: and closes it again`);
  // a calendar says what is coming, not what came in
  await page.evaluate(()=>showHealthPane('calendar'));v=await look(page);
  assert.match(v.rows[0].status,/^Personal · .*9 next 7 days$/,`${tag}: a calendar counts the next 7 days`);
  // a kind with nothing connected: its sources, no "Add another"
  await page.evaluate(()=>showHealthPane('meetings'));v=await look(page);
  assert.deepEqual([v.rows.length,v.add],[0,[{head:null,tiles:['Zoom']}]],`${tag}: Meetings, nothing connected: just its sources`);
  if(mobile){
   await page.locator('[data-conn-back]').click();await page.waitForTimeout(200);v=await look(page);
   assert.deepEqual([v.title,v.back,v.cats.length],[null,false,6],`${tag}: back goes to the list`);
  }
  // links: a kind, and the old + Add
  await page.goto(base+'/#connections=chat');await page.locator('#health-tabs .conn-cat').first().waitFor({state:'attached'});await page.waitForTimeout(300);v=await look(page);
  assert.equal(v.title,'Chat',`${tag}: #connections=chat opens Chat`);
  await page.goto(base+'/#connections=add');await page.locator('#health-tabs .conn-cat').first().waitFor({state:'attached'});await page.waitForTimeout(300);v=await look(page);
  assert.equal(v.title,mobile?null:'Email',`${tag}: #connections=add opens ${mobile?'the list':'Email'}`);
  // a setup opens in its own kind
  await page.goto(base+'/#connections=mail');await page.locator('#connect-add .connect-source').first().waitFor();
  await page.locator('#connect-add .connect-source',{hasText:'Outlook'}).click();await page.waitForTimeout(300);v=await look(page);
  assert.deepEqual([v.title,v.rows.length],['Email',0],`${tag}: a setup shows in its kind, instead of its rows`);
  assert.ok(['form','run'].includes(await page.locator('#connect-add').getAttribute('data-view')),`${tag}: its setup`);
  await shot('setup');
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('connections by kind dashboard ok');
