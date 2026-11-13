import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
import {callAfter} from './page-calls.mjs';
const {chromium}=await import('./browser.mjs');

// The To-dos digest: one row at the top of the list ("Digest", or "Work digest" / "Personal digest" while a filter is
// on) opens each area's done today and still open (the area_digest action) to read and copy, one Copy per area, the
// filter's area alone with one Copy. No row when the area has nothing to list (only Personal to-dos, Work filter on;
// a Daily digest to read). At 1440x900 and 390x844, light and dark, in one line with no overflow.
// SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const now=new Date().toISOString();
const card=(id,scope,title,extra={})=>({id:id.repeat(16),status:'pending',title,body:'A useful suggestion.',created_at:now,scope,result_files:[],original_urls:[],...extra});
const DIGEST={work:'Done today\n• Send the order form\nStill open\n• Due today: Reply to the supplier\n• Send the quarterly numbers',
 personal:'Still open\n• Book the dentist'};
let suggestions,locale,calls,rowHidden=false;
const view=todo_scope=>({locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},todo_scope,saveable:true});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/en.json'){res.end(en);return}
 if(url.pathname==='/api/action'){let body='';req.on('data',c=>body+=c);req.on('end',()=>{const {action,args}=JSON.parse(body);calls.push(action);
  if(action==='area_digest'){res.end(JSON.stringify(DIGEST));return}
  if(action==='set_locale'){locale={...locale,...args};res.end(JSON.stringify(locale));return}
  if(action==='digest_row_hide'){rowHidden=true;res.end(JSON.stringify({digest_row_hidden:true}));return}
  res.end('{}')});return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],digest_row_hidden:rowHidden,
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
const isOpen=page=>page.locator('#area-digest').evaluate(d=>d.open);
const fresh=async page=>{await page.evaluate(()=>refresh());await page.waitForTimeout(300)};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const colorScheme of ['light','dark']){
  const tag=`${width}-${colorScheme}`;
  suggestions=[card('a','work','Reply to the supplier'),card('b','work','Send the quarterly numbers'),card('c','personal','Book the dentist')];
  locale=view(null);calls=[];
  let [context,page]=await open({width,height,colorScheme});
  // All: one row, "Digest", above the first to-do, in one line that fits
  await entry(page).waitFor();
  assert.equal((await entry(page).innerText()).replace(/\s+/g,' ').trim(),'Digest Done today and still open ›');
  const box=await entry(page).boundingBox(),first=await page.locator('#suggestions article[id^="task-"]').first().boundingBox();
  assert.ok(box.y+box.height<=first.y,'the row is above the to-dos');
  assert.ok(box.height<=48,`one line, not a block (${box.height}px)`);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'no sideways scroll');
  await shot(page,`${tag}-all-row`);
  // It opens both areas, each with its own Copy, the text as the Machine wrote it
  assert.deepEqual((await callAfter(page,'area_digest',()=>entry(page).click())).args,{});
  const dialog=page.locator('#area-digest');await dialog.locator('.ad-text').first().waitFor();
  assert.equal(await dialog.locator('h2').innerText(),'Digest');
  assert.deepEqual(await dialog.locator('h3').allInnerTexts(),['Work','Personal']);
  assert.deepEqual(await dialog.locator('.ad-text').allTextContents(),[DIGEST.work,DIGEST.personal]);
  assert.deepEqual(await dialog.locator('[data-ad-copy]').allInnerTexts(),['Copy Work','Copy Personal']);
  await shot(page,`${tag}-all-open`);
  await dialog.getByRole('button',{name:'Copy Personal'}).click();
  await page.locator('#toast',{hasText:'Copied.'}).waitFor();
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),DIGEST.personal);
  await dialog.locator('[data-ad-close]').click();assert.equal(await isOpen(page),false);
  // Escape and a tap beside the sheet close it too, and a status refresh never opens it again
  await entry(page).click();await dialog.locator('.ad-text').first().waitFor();await page.keyboard.press('Escape');assert.equal(await isOpen(page),false,'Escape closes it');
  await entry(page).click();await dialog.locator('.ad-text').first().waitFor();await page.mouse.click(2,height-2);assert.equal(await isOpen(page),false,'a tap beside it closes it');
  await fresh(page);assert.equal(await isOpen(page),false,'a refresh leaves it closed');
  // Its ×: the row goes at once and the Machine keeps it hidden (every device), through refreshes and a reload
  const row=await page.locator('#suggestions .ad-entry').boundingBox(),x=await hideX(page).boundingBox();
  assert.ok(x.x+x.width<=row.x+row.width+0.5&&x.y>=row.y-0.5&&x.y+x.height<=row.y+row.height+0.5,'the × sits inside the row');
  assert.ok(x.width>=32&&x.height>=32,`the × is big enough to tap (${x.width}x${x.height})`);
  assert.equal(await hideX(page).getAttribute('aria-label'),'Hide until the next digest');
  assert.deepEqual((await callAfter(page,'digest_row_hide',()=>hideX(page).click())).args,{});
  await page.locator('#toast',{hasText:'Hidden until the next digest.'}).waitFor();
  assert.equal(await page.locator('#suggestions .ad-entry').count(),0,'the row is gone');
  await shot(page,`${tag}-all-hidden`);
  await fresh(page);assert.equal(await page.locator('#suggestions .ad-entry').count(),0,'still gone after a refresh');
  await page.reload();await page.locator('#suggestions article[id^="task-"]').first().waitFor();
  assert.equal(await page.locator('#suggestions .ad-entry').count(),0,'still gone after a reload');
  // the next digest sent (or the next day): the Machine says so and the row is back
  rowHidden=false;await page.evaluate(()=>refresh());await entry(page).waitFor();
  await shot(page,`${tag}-all-back`);
  await context.close();
  // The Work filter: "Work digest", Work alone with one Copy
  locale=view('work');[context,page]=await open({width,height,colorScheme});
  await entry(page).waitFor();
  assert.match(await entry(page).innerText(),/^Work digest/);
  await shot(page,`${tag}-work-row`);
  await callAfter(page,'area_digest',()=>entry(page).click());
  const d2=page.locator('#area-digest');await d2.locator('.ad-text').first().waitFor();
  assert.equal(await d2.locator('h2').innerText(),'Work digest');
  assert.equal(await d2.locator('h3').count(),0);
  assert.deepEqual(await d2.locator('.ad-text').allTextContents(),[DIGEST.work]);
  assert.deepEqual(await d2.locator('[data-ad-copy]').allInnerTexts(),['Copy']);
  const sheet=await d2.boundingBox();assert.ok(sheet.x>=0&&sheet.x+sheet.width<=width+0.5,'the sheet fits the screen');
  await shot(page,`${tag}-work-open`);
  await d2.getByRole('button',{name:'Copy',exact:true}).click();
  await page.locator('#toast',{hasText:'Copied.'}).waitFor();
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),DIGEST.work);
  await context.close();
  // Nothing worth listing: the Personal filter with only Work to-dos, or only a Daily digest to read
  suggestions=[card('a','work','Reply to the supplier'),card('d','personal','Daily digest',{digest:{items:[]}})];
  locale=view('personal');[context,page]=await open({width,height,colorScheme});
  await page.locator('#suggestions .scope-note').waitFor();
  assert.equal(await entry(page).count(),0,'no row when the area has nothing to list');
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
