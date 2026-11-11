import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
import {callAfter} from './page-calls.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// What's new (shell-whats-new.js, state.whats_new): one small dialog a moment after the dashboard opens. One entry: its
// picture on top, its title, its text with a button that opens it, × and Done. Several: one per view, with dots, Back
// and Next in the same place on every view (and the arrow keys and a swipe), Done in Next's place on the last; an entry's
// own button stays in its text, never the main one. Closing it any way, on any view, marks
// it seen on the Machine (whats_new_seen). Never over another dialog, an open to-do or the hello, and at most once per
// opening.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const ROUTINES={id:'routines',title:'Routines run work for you',text:'Tell The Machine what to do and how often.',action:{label:'Open Routines',run:'go-routines'},art:'routines'};
const SEARCH={id:'ask',title:'Search answers questions',text:'Type a question into Search.',action:{label:'Open Search',run:'search'},art:'search'};
const PLAIN={id:'plain',title:'Faster first load',text:'The dashboard opens sooner.',action:null};
const ID='00000000000000a1';let news=null,greeting=null,seen=0;
const cards=[{id:ID,title:'Reply to Sam about pricing',body:'Sam asked for pricing.',status:'pending',scope:'work',created_at:now,event_ids:[1]}];
const state=()=>({suggestions:cards,whats_new:news,greeting,first_tips:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);
  if(b.action==='whats_new_seen'){seen++;news=null;res.end(JSON.stringify({whats_new:null}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const base=()=>'http://127.0.0.1:'+server.address().port;
const open=async(width,hash='')=>{const context=await browser.newContext({viewport:{width,height:800},hasTouch:width<600});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base()+'/'+hash);await page.locator('#task-'+ID).first().waitFor({state:'attached'});return {context,page}};
const dialog=page=>page.locator('#whats-new[open]');
const tried=page=>page.waitForFunction(()=>wnTried).then(()=>page.waitForTimeout(900));  // its moment (600 ms) has passed
const acts=page=>page.locator('#whats-new .wn-acts button').allTextContents();
const shown=page=>page.locator('#whats-new .wn-view.on h2').textContent();
const runs=page=>page.locator('#whats-new .wn-view.on [data-wn-run]').allTextContents();
const at=async(page,sel)=>{const b=await page.locator('#whats-new .wn-acts '+sel).boundingBox();return [Math.round(b.x),Math.round(b.y),Math.round(b.width)]};
const swipe=(page,dx)=>page.evaluate(dx=>{const d=document.querySelector('#whats-new'),r=d.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2;
 const t=(cx)=>new Touch({identifier:1,target:d,clientX:cx,clientY:y});
 d.dispatchEvent(new TouchEvent('touchstart',{touches:[t(x)],changedTouches:[t(x)],bubbles:true}));
 d.dispatchEvent(new TouchEvent('touchend',{touches:[],changedTouches:[t(x+dx)],bubbles:true}))},dx);
const tab=page=>page.evaluate(()=>[...document.querySelectorAll('main>section')].find(s=>!s.hidden)?.id);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  // One entry: its picture edge to edge on top, title, text with its button, × and Done, small and inside the screen
  news={entries:[ROUTINES]};seen=0;
  {const {context,page}=await open(width);await dialog(page).waitFor();
   assert.equal(await page.locator('#whats-new h2').textContent(),ROUTINES.title);
   assert.equal(await page.locator('#whats-new p').textContent(),ROUTINES.text);
   assert.deepEqual(await acts(page),['Done']);assert.deepEqual(await runs(page),['Open Routines']);
   assert.equal(await page.locator('#whats-new .wn-x').getAttribute('aria-label'),'Close');
   assert.equal(await page.locator('#whats-new .wn-dots').count(),0);
   const box=await dialog(page).boundingBox(),pic=await page.locator('#whats-new .wn-arts').boundingBox();
   assert.ok(box.width<=480&&box.x>=16&&box.x+box.width<=width-16&&box.height<440,JSON.stringify(box));
   assert.ok(Math.abs(box.x+box.width/2-width/2)<10&&box.y>100,'centered: '+JSON.stringify(box));
   assert.ok(Math.abs(pic.x-box.x)<1&&Math.abs(pic.width-box.width)<1&&Math.abs(pic.y-box.y)<1,'picture on top, edge to edge: '+JSON.stringify([pic,box]));
   assert.ok(width>600?pic.height>=160&&pic.height<=200:Math.abs(pic.height-140)<=10,'picture height '+pic.height);
   assert.ok(await page.locator('#whats-new .wn-art.on svg rect').count()>3,'the routines picture is drawn');
   // Its button closes it, marks it seen and opens the feature
   assert.deepEqual(await callAfter(page,'whats_new_seen',()=>page.locator('#whats-new [data-wn-run]').click()),{action:'whats_new_seen',args:{}});
   assert.equal(await dialog(page).count(),0);assert.equal(await tab(page),'routines');
   // Once per opening: nothing more on a later status
   news={entries:[SEARCH]};await page.evaluate(()=>refresh());await page.waitForTimeout(900);assert.equal(await dialog(page).count(),0);
   await context.close()}
  // Several: one per view in the order given, dots under the picture, Back from the second view and Next until the last,
  // where Done takes Next's place. Each in the same place on every view; an entry's own button stays in its text. One
  // size from view to view; stepping marks nothing seen.
  news={entries:[ROUTINES,PLAIN,SEARCH]};seen=0;
  {const {context,page}=await open(width);await dialog(page).waitFor();
   assert.equal(await shown(page),ROUTINES.title);
   assert.equal(await page.locator('#whats-new .wn-dots button').count(),3);
   assert.equal(await page.locator('#whats-new .wn-dots button.on[aria-current]').getAttribute('aria-label'),ROUTINES.title);
   assert.equal(await page.locator('#whats-new .wn-art').count(),3);  // PLAIN has none: the stand-in, so the size holds
   assert.deepEqual(await acts(page),['Next']);assert.deepEqual(await runs(page),['Open Routines']);
   const next=await at(page,'.primary');
   const box=await dialog(page).boundingBox();assert.ok(box.x>=16&&box.x+box.width<=width-16&&box.y>=0&&box.y+box.height<=800,JSON.stringify(box));
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   // Next by keyboard keeps focus on the main button
   await page.locator('#whats-new [data-wn-go].primary').focus();await page.keyboard.press('Enter');
   assert.equal(await shown(page),PLAIN.title);assert.deepEqual(await acts(page),['Back','Next']);assert.deepEqual(await runs(page),[]);
   assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Next');
   assert.deepEqual(await at(page,'.primary'),next);const back=await at(page,'.ghost');
   await page.keyboard.press('ArrowRight');assert.equal(await shown(page),SEARCH.title);
   assert.deepEqual(await acts(page),['Back','Done']);assert.deepEqual(await runs(page),['Open Search']);
   assert.deepEqual(await at(page,'.primary'),next);assert.deepEqual(await at(page,'.ghost'),back);  // Done where Next was
   assert.equal(await page.locator('#whats-new [data-wn-run].primary').count(),0);
   await page.keyboard.press('ArrowRight');assert.equal(await shown(page),SEARCH.title);  // the last stays the last
   await page.keyboard.press('ArrowLeft');assert.equal(await shown(page),PLAIN.title);
   await page.locator('#whats-new .wn-acts .ghost').click();assert.equal(await shown(page),ROUTINES.title);
   assert.deepEqual(await acts(page),['Next']);
   await page.locator('#whats-new .wn-dots button').last().click();assert.equal(await shown(page),SEARCH.title);
   if(width<600){await swipe(page,120);assert.equal(await shown(page),PLAIN.title);await swipe(page,-120);assert.equal(await shown(page),SEARCH.title);
    await swipe(page,20);assert.equal(await shown(page),SEARCH.title)}  // a small move is no swipe
   await page.locator('#whats-new .wn-dots button').first().click();assert.equal(await shown(page),ROUTINES.title);
   assert.deepEqual(await dialog(page).boundingBox(),box);
   assert.equal(seen,0);
   // × (at 390) or Esc (at 1440) on any view marks all of them seen
   await callAfter(page,'whats_new_seen',()=>width>600?page.keyboard.press('Escape'):page.locator('#whats-new .wn-x').click());
   assert.equal(await dialog(page).count(),0);assert.equal(seen,1);
   await context.close()}
  // Done on the last view closes it and marks it seen
  news={entries:[ROUTINES,SEARCH]};seen=0;
  {const {context,page}=await open(width);await dialog(page).waitFor();
   await page.locator('#whats-new .wn-acts .primary').click();assert.deepEqual(await acts(page),['Back','Done']);
   await callAfter(page,'whats_new_seen',()=>page.locator('#whats-new .wn-acts .primary').click());
   assert.equal(await dialog(page).count(),0);assert.equal(seen,1);
   await context.close()}
  // An entry's own button on an earlier view opens it and closes the notice
  news={entries:[ROUTINES,SEARCH]};
  {const {context,page}=await open(width);await dialog(page).waitFor();
   await callAfter(page,'whats_new_seen',()=>page.locator('#whats-new .wn-view.on [data-wn-run="go-routines"]').click());
   assert.equal(await dialog(page).count(),0);assert.equal(await tab(page),'routines');
   await context.close()}
  // Search's entry opens Search; Esc closes it and marks it seen as well
  news={entries:[SEARCH]};
  {const {context,page}=await open(width);await dialog(page).waitFor();
   await callAfter(page,'whats_new_seen',()=>page.locator('#whats-new [data-wn-run="search"]').click());
   await page.locator('#palette[open]').waitFor();await page.keyboard.press('Escape');
   await context.close()}
  // Settings' entry opens that tab of Settings
  news={entries:[{id:'export',title:'Take everything with you',text:'Export everything.',action:{label:'Open Settings',run:'go-settings-general'}}]};
  {const {context,page}=await open(width);await dialog(page).waitFor();
   await callAfter(page,'whats_new_seen',()=>page.locator('#whats-new [data-wn-run]').click());
   await page.waitForFunction(()=>!document.querySelector('#settings').hidden&&settingsTab==='general');
   await context.close()}
  // A morning's pick of five (the most it holds): five dots, inside the screen, Done on the fifth; a sixth is never shown
  news={entries:[ROUTINES,PLAIN,SEARCH,{...PLAIN,id:'p4',title:'Four'},{...PLAIN,id:'p5',title:'Five'},{...PLAIN,id:'p6',title:'Six'}]};
  {const {context,page}=await open(width);await dialog(page).waitFor();
   assert.equal(await page.locator('#whats-new .wn-dots button').count(),5);
   const box=await dialog(page).boundingBox();assert.ok(box.x>=16&&box.x+box.width<=width-16&&box.y>=0&&box.y+box.height<=800,JSON.stringify(box));
   await page.locator('#whats-new .wn-dots button').last().click();assert.equal(await shown(page),'Five');assert.deepEqual(await acts(page),['Back','Done']);
   await callAfter(page,'whats_new_seen',()=>page.locator('#whats-new .wn-acts .primary').click());
   await context.close()}
  // No picture and no button: text, × and Done only
  news={entries:[PLAIN]};
  {const {context,page}=await open(width);await dialog(page).waitFor();
   assert.deepEqual(await page.locator('#whats-new button').allTextContents(),['×','Done']);
   assert.equal(await page.locator('#whats-new .wn-arts').count(),0);
   await callAfter(page,'whats_new_seen',()=>page.keyboard.press('Escape'));assert.equal(await dialog(page).count(),0);
   await context.close()}
 }
 // Nothing to tell: no dialog, not even built
 news=null;
 {const {context,page}=await open(1440);await page.waitForTimeout(1200);assert.equal(await page.locator('#whats-new').count(),0);await context.close()}
 // Never over another dialog: it waits for the next opening, and nothing is marked seen
 // (news comes with a refresh after the other dialog is up: a slow first load can't let it in before)
 news=null;seen=0;
 {const {context,page}=await open(1440);await page.evaluate(()=>palOpen());news={entries:[ROUTINES]};await page.evaluate(()=>refresh());await tried(page);
  assert.equal(await dialog(page).count(),0);assert.ok(await page.evaluate(()=>document.querySelector('#palette').open));
  await page.keyboard.press('Escape');await page.evaluate(()=>refresh());await page.waitForTimeout(900);assert.equal(await dialog(page).count(),0);
  assert.equal(seen,0);await context.close()}
 // Nor over an open to-do (its chat), while typing, or during the hello of someone's first views
 {const {context,page}=await open(1440,'#chat='+ID);await tried(page);assert.equal(await page.evaluate(()=>chatId),ID);assert.equal(await dialog(page).count(),0);await context.close()}
 news=null;{const {context,page}=await open(1440);await page.evaluate(()=>{const i=document.createElement('textarea');i.id='typing';document.body.append(i);i.focus()});
  news={entries:[ROUTINES]};await page.evaluate(()=>refresh());await tried(page);
  assert.equal(await dialog(page).count(),0);await context.close()}
 greeting={name:'Sam'};
 {const {context,page}=await open(1440);await tried(page);assert.equal(await dialog(page).count(),0);await context.close()}
 greeting=null;assert.equal(seen,0);
 // The next opening shows it
 {const {context,page}=await open(1440);await dialog(page).waitFor();await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('whats new ok');
