import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
import {callAfter} from './page-calls.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// What's new (shell-whats-new.js, state.whats_new): one small dialog a moment after the dashboard opens. One entry: its
// title, its text, Close and a button that opens it. Several: one short list with a quiet link each. Closing it any
// way marks it seen on the Machine (whats_new_seen). Never over another dialog, an open to-do or the hello, and at
// most once per opening.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const ROUTINES={id:'routines',title:'Routines run work for you',text:'Tell The Machine what to do and how often.',action:{label:'Open Routines',run:'go-routines'}};
const SEARCH={id:'ask',title:'Search answers questions',text:'Type a question into Search.',action:{label:'Open Search',run:'search'}};
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
const open=async(width,hash='')=>{const context=await browser.newContext({viewport:{width,height:800}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base()+'/'+hash);await page.locator('#task-'+ID).first().waitFor({state:'attached'});return {context,page}};
const dialog=page=>page.locator('#whats-new[open]');
const tried=page=>page.waitForFunction(()=>wnTried).then(()=>page.waitForTimeout(900));  // its moment (600 ms) has passed
const tab=page=>page.evaluate(()=>[...document.querySelectorAll('main>section')].find(s=>!s.hidden)?.id);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  // One entry: title, text, Close on the left and its button on the right, small and inside the screen
  news={entries:[ROUTINES]};seen=0;
  {const {context,page}=await open(width);await dialog(page).waitFor();
   assert.equal(await page.locator('#whats-new h2').textContent(),ROUTINES.title);
   assert.equal(await page.locator('#whats-new p').textContent(),ROUTINES.text);
   assert.deepEqual(await page.locator('#whats-new button').allTextContents(),['Close','Open Routines']);
   const box=await dialog(page).boundingBox();
   assert.ok(box.width<=420&&box.x>=16&&box.x+box.width<=width-16&&box.height<320,JSON.stringify(box));
   assert.ok(Math.abs(box.x+box.width/2-width/2)<10&&box.y>100,'centered: '+JSON.stringify(box));
   // Its button closes it, marks it seen and opens the feature
   assert.deepEqual(await callAfter(page,'whats_new_seen',()=>page.locator('#whats-new [data-wn-run]').click()),{action:'whats_new_seen',args:{}});
   assert.equal(await dialog(page).count(),0);assert.equal(await tab(page),'routines');
   // Once per opening: nothing more on a later status
   news={entries:[SEARCH]};await page.evaluate(()=>refresh());await page.waitForTimeout(900);assert.equal(await dialog(page).count(),0);
   await context.close()}
  // Several: one list, in the order given, a quiet link each; Close marks them seen
  news={entries:[ROUTINES,SEARCH,PLAIN]};seen=0;
  {const {context,page}=await open(width);await dialog(page).waitFor();
   assert.equal(await page.locator('#whats-new h2').textContent(),'What’s new');
   assert.deepEqual(await page.locator('#whats-new .wn-list b').allTextContents(),[ROUTINES.title,SEARCH.title,PLAIN.title]);
   assert.deepEqual(await page.locator('#whats-new button').allTextContents(),['Open Routines','Open Search','Close']);
   const box=await dialog(page).boundingBox();assert.ok(box.x>=16&&box.x+box.width<=width-16&&box.y>=0&&box.y+box.height<=800,JSON.stringify(box));
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   await callAfter(page,'whats_new_seen',()=>page.locator('#whats-new [data-wn-close]').click());
   assert.equal(await dialog(page).count(),0);assert.equal(seen,1);
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
  news={entries:[PLAIN]};
  {const {context,page}=await open(width);await dialog(page).waitFor();
   assert.deepEqual(await page.locator('#whats-new button').allTextContents(),['Close']);
   await callAfter(page,'whats_new_seen',()=>page.keyboard.press('Escape'));assert.equal(await dialog(page).count(),0);
   await context.close()}
 }
 // Nothing to tell: no dialog, not even built
 news=null;
 {const {context,page}=await open(1440);await page.waitForTimeout(1200);assert.equal(await page.locator('#whats-new').count(),0);await context.close()}
 // Never over another dialog: it waits for the next opening, and nothing is marked seen
 news={entries:[ROUTINES]};seen=0;
 {const {context,page}=await open(1440);await page.evaluate(()=>palOpen());await tried(page);
  assert.equal(await dialog(page).count(),0);assert.ok(await page.evaluate(()=>document.querySelector('#palette').open));
  await page.keyboard.press('Escape');await page.evaluate(()=>refresh());await page.waitForTimeout(900);assert.equal(await dialog(page).count(),0);
  assert.equal(seen,0);await context.close()}
 // Nor over an open to-do (its chat), while typing, or during the hello of someone's first views
 {const {context,page}=await open(1440,'#chat='+ID);await tried(page);assert.equal(await page.evaluate(()=>chatId),ID);assert.equal(await dialog(page).count(),0);await context.close()}
 {const {context,page}=await open(1440);await page.evaluate(()=>{const i=document.createElement('textarea');i.id='typing';document.body.append(i);i.focus()});await tried(page);
  assert.equal(await dialog(page).count(),0);await context.close()}
 greeting={name:'Sam'};
 {const {context,page}=await open(1440);await tried(page);assert.equal(await dialog(page).count(),0);await context.close()}
 greeting=null;assert.equal(seen,0);
 // The next opening shows it
 {const {context,page}=await open(1440);await dialog(page).waitFor();await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('whats new ok');
