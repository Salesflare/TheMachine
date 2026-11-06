import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Based on (assistant.based_on_views): a to-do whose draft follows someone else's input in another message, like a
// teammate's suggestion in a Slack thread, shows one quiet line under its body that opens that message: "Based on Robin in
// #support · Wed, Nov 4". No based_on, no line. It opens that message here, in Read message (Open in Slack sits inside),
// never Slack or Gmail straight away. Also in Dutch. SHOTS=<folder> saves screenshots at 1440x900, 1440x700 and 390x844,
// light and dark, with a to-do from an email and one from a chat next to it.
const dashboard=await dashboardPage();
const cats={};for(const l of ['en','nl'])cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const now=new Date().toISOString();
const cards=[
 {id:'b1',title:'Offer the reporter the bounty',body:'Drafted a $20 bounty offer, the lowest one, as Robin suggested.',status:'prepared',scope:'work',created_at:now,event_ids:[1,2,3],
  source_line:'Source: Intercom from Alex Reporter · Wed 4 Nov (+2 more)',account_ids:['ic'],original_urls:['https://app.intercom.example/c/1'],
  based_on:{event_id:3,who:'Robin',where:'#support',kind:'Slack',at:'2026-11-04T11:37:44+00:00',url:'https://acme.slack.com/archives/C0SUPPORT1/p1793792264759699'}},
 {id:'b2',title:'Answer Kim about the invoice',body:'Kim asked for a copy.',status:'pending',scope:'work',created_at:now,event_ids:[4],source_line:'Source: email from Kim Lee · Tue 3 Nov'},
 {id:'b3',title:'Reply to Noor',body:'Noor asked about the plan, as Jo said.',status:'pending',scope:'work',created_at:now,event_ids:[5,6],source_line:'Source: email from Noor · Tue 3 Nov (+1 more)',
  based_on:{event_id:6,who:null,where:null,kind:'email',at:'2026-11-03T09:00:00+00:00',url:null}},
 {id:'b4',title:'Fix meeting-note syncing when Intercom has duplicate emails',body:'Zapier reports meeting notes failing to sync when two Intercom contacts share an email.',status:'pending',scope:'work',created_at:now,event_ids:[7],
  source_line:'Source: email from Zapier Alerts via info@acme.example · Fri 6 Nov',account_ids:['gm'],original_urls:['https://mail.google.com/mail/u/0/#all/1'],based_on:null},
 {id:'b5',title:'Answer Sam in #ops',body:'Sam asked who picks up the renewal.',status:'pending',scope:'work',created_at:now,event_ids:[8],
  source_line:'Source: Slack from Sam Lee · Thu 5 Nov',account_ids:['sl'],original_urls:['https://acme.slack.com/archives/C0OPS/p1'],based_on:null}];
const originals={3:{event_id:3,kind:'Slack',chat:'#support',from:'Robin Example',occurred_at:'2026-11-04T11:37:44+00:00',body:'Lowest bounty is fine',
 url:'https://acme.slack.com/archives/C0SUPPORT1/p1793792264759699'}};
let language='en';
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){readFile(new URL('../'+(url.pathname.startsWith('/brand/fonts/')?url.pathname.slice(1):'brand/app-icon-192.png'),import.meta.url)).then(b=>{res.setHeader('Content-Type',url.pathname.endsWith('.woff2')?'font/woff2':'image/png');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const cat=/^\/i18n\/(\w\w)\.json$/.exec(url.pathname);if(cat){res.end(cats[cat[1]]||'{}');return}
 if(url.pathname==='/api/originals'){const o=originals[url.searchParams.get('event')];res.end(JSON.stringify({originals:o?[o]:[]}));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],
  review_health:{},review_runs:[],review_live:{runs:[]},fleet:{on:false,fleets:[]},locale:{locale:'en-BE',region:'BE',language,language_set:true,clock:'auto',hour12:false,auto_hour12:false,
  date_locale:language==='en'?'en-US':'nl-BE',languages:{en:'English',nl:'Nederlands'},saveable:true}}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const open=async({width=1440,height=900,scheme='light'}={})=>{
 const context=await browser.newContext({viewport:{width,height},timezoneId:'UTC',locale:'en-US',colorScheme:scheme}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));await page.goto(base+'/');await page.locator('#task-b1').waitFor();
 if(language==='nl')await page.waitForFunction(()=>document.documentElement.lang==='nl');
 return [context,page]};
const line=(page,id)=>page.locator(`#task-${id} .based-on`).evaluateAll(n=>n.map(x=>x.textContent.replace(/\s+/g,' ').trim()));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[1440,700],[390,844]]){
  const [context,page]=await open({width,height});
  assert.deepEqual(await line(page,'b1'),['Based on Robin in #support · Wed, Nov 4']);
  assert.deepEqual(await line(page,'b2'),[],'no based_on: no line');
  assert.deepEqual(await line(page,'b3'),['Based on a message · Tue, Nov 3']);
  assert.equal(await page.locator('#task-b1 .based-on a, #task-b3 .based-on a').count(),0,'never a link out to Slack or Gmail');
  assert.equal(await page.locator('#task-b1 .based-on button[data-held-read="3"]').count(),1,'it opens that message here');
  assert.equal(await page.locator('#task-b3 .based-on button[data-held-read="6"]').count(),1);
  assert.deepEqual(await line(page,'b4'),[],'the source line names the message: one line, no Based on');
  // Both open the message here, so neither carries the ↗ of a link out (that stays on Open in Slack inside)
  for(const id of ['b1','b4'])assert.ok(!/↗/.test(await page.locator(`#task-${id} :is(.based-on,.card-source)`).evaluateAll(n=>n.map(x=>x.textContent).join(''))),'no ↗ on '+id);
  // Right under the body, above the draft and the source line, never wider than the to-do
  const order=await page.locator('#task-b1').evaluate(c=>{const y=s=>c.querySelector(s)?.getBoundingClientRect().top??-1;return [y('.body'),y('.based-on'),y('.card-source')]});
  assert.ok(order[0]<order[1]&&order[1]<order[2],'under the body, above the source: '+order);
  const fits=await page.locator('#task-b1 .based-on').evaluate(n=>n.getBoundingClientRect().right<=n.closest('.card').getBoundingClientRect().right+1);
  assert.ok(fits,'inside the to-do at '+width);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'no sideways scroll at '+width);
  if(width===1440&&height===900){  // In app: Read message with that message, its Open in Slack inside
   await page.locator('#task-b1 .based-on button').click();
   const dialog=page.locator('#email-dialog');await dialog.locator('.convo').waitFor();
   assert.match(await dialog.textContent(),/Lowest bounty is fine/);
   assert.equal(await dialog.locator('a.convo-source').getAttribute('href'),'https://acme.slack.com/archives/C0SUPPORT1/p1793792264759699');
   assert.match(await dialog.locator('a.convo-source').textContent(),/Open in Slack ↗/);
   if(shots)await page.screenshot({path:`${shots}/based-on-opened-${width}x${height}.png`});
   await page.keyboard.press('Escape');
  }
  await context.close();
  if(shots&&height!==700)for(const scheme of ['light','dark']){
   const [c2,p2]=await open({width,height,scheme});
   for(const [id,name] of [['b4','email-source'],['b5','chat-source'],['b1','based-on']])await p2.locator('#task-'+id).screenshot({path:`${shots}/${name}-${width}x${height}-${scheme}.png`});
   await c2.close()}
 }
 language='nl';
 {const [context,page]=await open({width:390,height:844});
  assert.deepEqual(await line(page,'b1'),['Op basis van Robin in #support · wo 4 nov']);
  if(shots)await page.locator('#task-b1').screenshot({path:`${shots}/based-on-nl-390x844.png`});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('based on ok');
}finally{await browser?.close();server.close()}
