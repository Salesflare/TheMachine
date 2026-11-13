import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
import {callAfter} from './page-calls.mjs';
const {chromium}=await import('./browser.mjs');

// The To-dos digest row: it says which digest it opens and what that digest counted (the status's digest_row,
// notify.digest_row): "Yesterday evening's digest  33 done, 1 open", the filter's area alone. Opening it shows that
// digest as it went, its name as the title, and sets the row aside on the Machine (digest_row_hide), as its × does.
// Without a recent digest: "Today so far", each area's done today and still open (the area_digest action) to read and
// copy, one Copy per area, the filter's area alone with one Copy; no row when the area has nothing to list. At 1440x900
// and 390x844, light and dark, in one line with no overflow. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const now=new Date().toISOString();
const card=(id,scope,title,extra={})=>({id:id.repeat(16),status:'pending',title,body:'A useful suggestion.',created_at:now,scope,result_files:[],original_urls:[],...extra});
const DIGEST={work:'Done today\n• Send the order form\nStill open\n• Due today: Reply to the supplier\n• Send the quarterly numbers',
 personal:'Still open\n• Book the dentist'};
const day=n=>{const d=new Date();d.setUTCDate(d.getUTCDate()-n);d.setUTCHours(17,45,0,0);return d.toISOString()};
const COUNTS={work:{done:20,open:1},personal:{done:13,open:0}};
const SENT=at=>({kind:'evening',title:'Good evening, 33 to-dos done today',text:'Work\nDone today\n• Send the order form',at,
 blocks:[['h','Work'],['sub','Done today'],['li','Send the order form']],sections:[{area:'work',copy:'Done today\n• Send the order form'}]});
let suggestions,locale,calls,row;
const view=todo_scope=>({locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},todo_scope,saveable:true});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/en.json'){res.end(en);return}
 if(url.pathname==='/api/action'){let body='';req.on('data',c=>body+=c);req.on('end',()=>{const {action,args}=JSON.parse(body);calls.push(action);
  if(action==='area_digest'){res.end(JSON.stringify(DIGEST));return}
  if(action==='digest_sent'){res.end(JSON.stringify(args.kind===row?.kind?SENT(row.at):{}));return}
  if(action==='set_locale'){locale={...locale,...args};res.end(JSON.stringify(locale));return}
  if(action==='digest_row_hide'){row=null;res.end(JSON.stringify({digest_row:null}));return}
  res.end('{}')});return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],digest_row:row,
  hours:{days:[1,2,3,4,5],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC',saveable:true},locale}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const shot=async(page,name)=>{if(shots)await page.screenshot({path:`${shots}/${name}.png`})};
const open=async({width,height,colorScheme})=>{const context=await browser.newContext({viewport:{width,height},colorScheme,timezoneId:'UTC',locale:'en-US'}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await context.grantPermissions(['clipboard-read','clipboard-write'],{origin:base});
 page.on('pageerror',e=>errors.push(e.message));await page.goto(base+'/');await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});return [context,page]};
const entry=page=>page.locator('#suggestions .ad-entry [data-area-digest]'),hideX=page=>page.locator('#suggestions .ad-entry [data-digest-hide]');
const text=async page=>(await entry(page).innerText()).replace(/\s+/g,' ').trim();
const isOpen=page=>page.locator('#area-digest').evaluate(d=>d.open);
const fresh=async page=>{await page.evaluate(()=>refresh());await page.waitForTimeout(300)};
const fits=async(page,width)=>{const box=await entry(page).boundingBox(),first=await page.locator('#suggestions article[id^="task-"]').first().boundingBox();
 assert.ok(box.y+box.height<=first.y,'the row is above the to-dos');
 // one line where it fits, else its counts on a second line under the name, never clipped
 assert.ok(box.height<=(width<500?64:48),`one line, two on a phone at most (${box.height}px)`);
 for(const part of ['b','.ad-count'])assert.equal(await entry(page).locator(part).evaluate(e=>e.scrollWidth<=e.clientWidth+1&&e.getClientRects().length===1),true,`${part} shows whole, in one line`);
 assert.ok(box.x+box.width<=width+0.5,'the row fits the screen');
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'no sideways scroll')};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const colorScheme of ['light','dark']){
  const tag=`${width}-${colorScheme}`;
  suggestions=[card('a','work','Reply to the supplier'),card('b','work','Send the quarterly numbers'),card('c','personal','Book the dentist')];
  // Yesterday evening's digest: its name and its counts, both areas
  locale=view(null);calls=[];row={kind:'evening',at:day(1),counts:COUNTS};
  let [context,page]=await open({width,height,colorScheme});
  await entry(page).waitFor();
  assert.equal(await text(page),'Yesterday evening’s digest 33 done, 1 open ›');
  await fits(page,width);
  await shot(page,`${tag}-evening-row`);
  // Opening it: that digest as it went, named by when it went; the row goes on every device, as with its ×
  const hid=callAfter(page,'digest_row_hide',()=>{});
  assert.deepEqual((await callAfter(page,'digest_sent',()=>entry(page).click())).args,{kind:'evening'});
  await hid;
  const dialog=page.locator('#area-digest');await dialog.locator('.ad-read').waitFor();
  assert.equal(await dialog.locator('h2').innerText(),'Yesterday evening’s digest');
  assert.equal(await page.locator('#suggestions .ad-entry').count(),0,'opened: the row is gone');
  assert.equal(await page.locator('#toast',{hasText:'Hidden until the next digest.'}).count(),0,'opening says nothing');
  await shot(page,`${tag}-evening-open`);
  await dialog.locator('[data-ad-close]').click();
  await fresh(page);assert.equal(await page.locator('#suggestions .ad-entry').count(),0,'still gone after a refresh');
  await context.close();
  // This morning's, with the Work filter: Work's counts alone
  locale=view('work');row={kind:'morning',at:now,counts:{work:{done:0,open:4},personal:{done:0,open:2}}};
  [context,page]=await open({width,height,colorScheme});
  await entry(page).waitFor();
  assert.equal(await text(page),'This morning’s digest 4 open ›');
  await shot(page,`${tag}-morning-work-row`);
  await context.close();
  // Two days back: its weekday
  locale=view(null);row={kind:'evening',at:day(2),counts:{}};
  [context,page]=await open({width,height,colorScheme});
  await entry(page).waitFor();
  assert.equal(await text(page),new Date(day(2)).toLocaleDateString('en-US',{weekday:'long',timeZone:'UTC'})+' evening’s digest ›');
  await context.close();
  // No recent digest: today's so far, both areas, each with its own Copy
  row={kind:'today'};
  [context,page]=await open({width,height,colorScheme});
  await entry(page).waitFor();
  assert.equal(await text(page),'Today so far 3 open ›');
  await fits(page,width);
  await shot(page,`${tag}-today-row`);
  assert.deepEqual((await callAfter(page,'area_digest',()=>entry(page).click())).args,{});
  const d1=page.locator('#area-digest');await d1.locator('.ad-text').first().waitFor();
  assert.equal(await d1.locator('h2').innerText(),'Today so far');
  assert.deepEqual(await d1.locator('h3').allInnerTexts(),['Work','Personal']);
  assert.deepEqual(await d1.locator('.ad-text').allTextContents(),[DIGEST.work,DIGEST.personal]);
  assert.deepEqual(await d1.locator('[data-ad-copy]').allInnerTexts(),['Copy Work','Copy Personal']);
  await shot(page,`${tag}-today-open`);
  await d1.getByRole('button',{name:'Copy Personal'}).click();
  await page.locator('#toast',{hasText:'Copied.'}).waitFor();
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),DIGEST.personal);
  await page.keyboard.press('Escape');assert.equal(await isOpen(page),false,'Escape closes it');
  assert.equal(await page.locator('#suggestions .ad-entry').count(),0,'opened: the row is gone');
  await context.close();
  // Its ×: the row goes at once and the Machine keeps it hidden (every device), through refreshes and a reload
  row={kind:'evening',at:day(1),counts:COUNTS};
  [context,page]=await open({width,height,colorScheme});
  await entry(page).waitFor();
  const r=await page.locator('#suggestions .ad-entry').boundingBox(),x=await hideX(page).boundingBox();
  assert.ok(x.x+x.width<=r.x+r.width+0.5&&x.y>=r.y-0.5&&x.y+x.height<=r.y+r.height+0.5,'the × sits inside the row');
  assert.ok(x.width>=32&&x.height>=32,`the × is big enough to tap (${x.width}x${x.height})`);
  assert.equal(await hideX(page).getAttribute('aria-label'),'Hide until the next digest');
  assert.deepEqual((await callAfter(page,'digest_row_hide',()=>hideX(page).click())).args,{});
  await page.locator('#toast',{hasText:'Hidden until the next digest.'}).waitFor();
  assert.equal(await page.locator('#suggestions .ad-entry').count(),0,'the row is gone');
  assert.equal(await page.locator('#area-digest[open]').count(),0,'the × opens nothing');
  await page.reload();await page.locator('#suggestions article[id^="task-"]').first().waitFor();
  assert.equal(await page.locator('#suggestions .ad-entry').count(),0,'still gone after a reload');
  // the next digest sent: the Machine says so and the row is back
  row={kind:'morning',at:now,counts:COUNTS};await page.evaluate(()=>refresh());await entry(page).waitFor();
  assert.equal(await text(page),'This morning’s digest 33 done, 1 open ›');
  await context.close();
  // Today's, nothing worth listing: the Personal filter with only Work to-dos, or only a Daily digest to read
  suggestions=[card('a','work','Reply to the supplier'),card('d','personal','Daily digest',{digest:{items:[]}})];
  locale=view('personal');row={kind:'today'};[context,page]=await open({width,height,colorScheme});
  await page.locator('#suggestions .scope-note').waitFor();
  assert.equal(await entry(page).count(),0,'no row when the area has nothing to list');
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
