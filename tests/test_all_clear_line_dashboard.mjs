import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// An empty list is the robot and one line in its voice, and they are the check's status (state.check, todos-check.js
// checkNow), so they never disagree with it: asleep with "All caught up." (the wording changes per
// day, not per render); awake and looking while a check or a review runs, also one the button didn't start; back
// asleep once it ends. No count line over it and no check line or Check now in the head: a small Check now shows under
// the line only when the line asks for it (the first check, a failed or a late one) or after a tap on the line, with
// Details for Connections, Checks. Before any review it says "I’ll add something when it’s useful.". Also in Dutch.
// SHOTS=<folder> saves screenshots at 1440x900 and 390x844, light and dark, asleep and checking.
const dashboard=await dashboardPage();
const cats={};for(const l of ['en','nl'])cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const DAY=Date.UTC(2026,9,28,12,0,0);
let reviewHealth,check,language,promises=[],reviewLive=null;const actions=[];
const MAIL=[{id:'work-gmail',service:'gmail',display_name:'Work mail',status:'ok',last_success:new Date(DAY).toISOString()}];let connectors=MAIL;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){const f=url.pathname.startsWith('/brand/fonts/')||url.pathname.endsWith('.webp')?url.pathname.slice(1):'brand/app-icon-192.png';
  readFile(new URL('../'+f,import.meta.url)).then(b=>{res.setHeader('Content-Type',f.endsWith('.woff2')?'font/woff2':f.endsWith('.webp')?'image/webp':'image/png');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const cat=/^\/i18n\/(\w\w)\.json$/.exec(url.pathname);if(cat){res.end(cats[cat[1]]||'{}');return}
 if(url.pathname==='/api/action'){const a=JSON.parse(body||'{}');actions.push(a.action);if(a.action==='check_now'){check={...check,phase:'reading'};res.end(JSON.stringify({started:true,check}));return}res.end('{}');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises,connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],
  review_health:reviewHealth,review_runs:[],...(check?{check}:{}),...(reviewLive?{review_live:reviewLive}:{}),locale:{locale:'en-BE',region:'BE',language,language_set:true,clock:'auto',hour12:false,auto_hour12:false,
  date_locale:language==='en'?'en-US':'nl-BE',languages:{en:'English',nl:'Nederlands'},saveable:true}}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const open=async({width=1440,height=900,scheme='light',time=DAY}={})=>{
 const context=await browser.newContext({viewport:{width,height},timezoneId:'UTC',locale:'en-US',colorScheme:scheme,isMobile:width<600,hasTouch:width<600}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));await page.clock.setFixedTime(time);await page.goto(base+'/');
 await page.locator('#suggestions .all-clear .poke-line').waitFor();
 if(language==='nl')await page.waitForFunction(()=>document.documentElement.lang==='nl');
 return [context,page]};
const line=async page=>(await page.locator('#suggestions .all-clear .poke-line').innerText()).replace(/ /g,' ');
// The pose, not a blink: the closed-eyes frame shows for about 150ms now and then
const pose=async page=>{await page.waitForFunction(()=>!document.querySelector('#suggestions .all-clear img.sleepy')?.getAttribute('src').includes('-blink'));
 return page.locator('#suggestions .all-clear img.sleepy').evaluate(i=>i.getAttribute('src'))};
const quiet=async(page,why)=>{
 assert.equal(await page.locator('#page-head .page-sub').count(),0,why+': no count line over the robot');
 assert.equal(await page.locator('#page-head .check-now').count(),0,why+': nothing about the check in the head');
 assert.ok(!/Checked|next by|Checking/.test(await page.locator('#page-head').innerText()),why)};
const OK=['All caught up.','All quiet. Back to my nap.','Clean slate. Time for a nap.'],BUSY=['Snooping around your messages…','Rummaging through the new stuff…'];
const done=(m=52)=>({reviewed:new Date(DAY-m*60000).toISOString(),waiting:0,reviewing:false,reading:false,phase:null});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // Before any review: the fallback.
 language='en';reviewHealth={total:0,pending:3};check=null;
 let [context,page]=await open();
 assert.equal(await line(page),'I’ll add something when it’s useful.');
 await context.close();
 // Checked: asleep, one line, nothing else; the same line all day, another one the next day.
 reviewHealth={total:10817,pending:0,last_completed:new Date(DAY-52*60000).toISOString()};promises=[{id:1,direction:'mine',who:'Someone',what:'send it',due:null,state:'open'}];
 const seen=new Set();
 for(let d=0;d<3;d++){
  check={...done(),reviewed:new Date(DAY+d*864e5-52*60000).toISOString()};[context,page]=await open({time:DAY+d*864e5});
  const text=await line(page);assert.ok(OK.includes(text),text);await quiet(page,'asleep');
  assert.ok(!/nothing needs you|check|peek|snoop/i.test(text),'never repeats the mail check line: '+text);
  assert.equal(await pose(page),'brand/sleepy.webp');assert.equal(await page.locator('#suggestions .all-clear .check-row').count(),0,'no Check now by default');
  await page.evaluate(()=>refresh());assert.equal(await line(page),text,'same wording within a day');
  seen.add(text);await context.close();
 }
 assert.equal(seen.size,3,'a different line on each of three days');
 // A tap on the line: Check now and Details, which opens Connections, Checks
 check=done();[context,page]=await open();
 await page.locator('#suggestions .all-clear [data-clear-more]').click();
 assert.deepEqual(await page.locator('#suggestions .all-clear .check-row button').allInnerTexts(),['Check now','Details']);
 await page.locator('#suggestions .all-clear [data-check-details]').click();await page.locator('#health').waitFor();
 assert.equal(await page.evaluate(()=>healthPane),'reviews');
 await context.close();
 // A review running that the button didn't start (the usual rhythm): awake, and the line says so, not "All caught up."
 check={...done(0),reviewing:true};[context,page]=await open();
 assert.ok(BUSY.includes(await line(page)),await line(page));assert.equal(await pose(page),'brand/wave-look.webp');await quiet(page,'checking');
 assert.equal(await page.locator('#suggestions .all-clear .check-row').count(),0,'nothing to press while it runs');
 // ...it ends: asleep again on the next refresh
 check=done(0);await page.evaluate(()=>refresh());
 assert.ok(OK.includes(await line(page)));assert.equal(await pose(page),'brand/sleepy.webp');
 await context.close();
 // With new messages counted: how many
 check={...done(3),phase:'reviewing',waiting:7};[context,page]=await open();
 assert.equal(await line(page),'Nosing through 7 new messages…');await context.close();
 // A failed check, a late one, the first one still to come: the line says it, with a small Check now under it
 for(const [c,h,want,img] of [[done(30),{worker:{status:'error',review_saved:false}},/^(Tripped over something\. That check failed\.|Oops, that check went sideways\.)$/,'brand/sad.webp'],
  [{...done(40),waiting:5,next_review:new Date(DAY-15*60000).toISOString()},{},/^(Dozed off|Overslept a little)\. Last look at 11:20\.$/,'brand/sleepy.webp'],
  [{waiting:0,reviewing:false,reading:false,phase:null},{},/^Haven’t snooped around yet\.$/,'brand/sleepy.webp']]){
  check=c;reviewHealth={...reviewHealth,...h};[context,page]=await open();
  assert.match(await line(page),want);assert.equal(await pose(page),img);
  assert.deepEqual(await page.locator('#suggestions .all-clear .check-row button').allInnerTexts(),['Check now']);
  delete reviewHealth.worker;await context.close()}
 // Someone new, mail in, the first review on its way by itself: what it reads and about when the first to-dos come
 // (review_live.first_eta), awake and looking, and no Check now to press. Without the estimate: the line from before.
 for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]){
  check={waiting:55,reviewing:false,reading:false,phase:null,soon:true};reviewLive={runs:[],first_look:null,first_dig:null,cards:{count:0,newest:null},first_eta:11};
  [context,page]=await open({width,height,scheme});
  assert.equal(await line(page),'Nosing through 55 new messages. First to-dos in about 11 min.');
  assert.equal(await pose(page),'brand/wave-look.webp');
  assert.equal(await page.locator('#suggestions .all-clear .check-row button').count(),0,'nothing to press: it starts by itself');
  if(shots)await page.screenshot({path:`${shots}/first-eta-${width}-${scheme}.png`});
  await context.close()}
 reviewLive={runs:[],cards:{count:0,newest:null},first_eta:null};[context,page]=await open();
 assert.equal(await line(page),'Haven’t snooped around yet.');await context.close();reviewLive=null;
 // Check now under a late line: awake at once, nothing new after: the line says so, then back to all clear
 check={...done(40),waiting:5,next_review:new Date(DAY-15*60000).toISOString()};[context,page]=await open();
 await page.locator('#suggestions .all-clear [data-check-now]').click();
 await page.waitForFunction(()=>document.querySelector('#suggestions .all-clear img.sleepy').getAttribute('src')==='brand/wave-look.webp');
 assert.ok(BUSY.includes(await line(page))||/^Nosing through 5/.test(await line(page)));assert.deepEqual(actions.filter(a=>a==='check_now'),['check_now']);
 check=done(0);await page.evaluate(()=>refresh());await page.waitForFunction(()=>/Nothing new/.test(document.querySelector('#suggestions .poke-line').textContent));
 assert.equal(await line(page),'Snooped around. Nothing new.');assert.equal(await pose(page),'brand/sleepy.webp');
 await context.close();
 // Dutch.
 language='nl';check=done();
 [context,page]=await open();
 assert.ok(['Helemaal bij.','Alles rustig. Terug naar mijn dutje.','Schone lei. Tijd voor een dutje.'].includes(await line(page)),await line(page));
 await context.close();
 // Nothing connected yet (a new Machine): the line says so, never that a check found nothing, and Check now has
 // nothing to read; while a check runs it still says that. In every size and theme.
 language='en';connectors=[];
 for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']])for(const [name,c] of [['first',null],['checked',done()]]){
  check=c;[context,page]=await open({width,height,scheme});
  assert.equal(await line(page),'Nothing connected yet, so there’s nothing to read.');
  assert.equal(await page.locator('#suggestions [data-check-now], #page-head [data-check-now]').count(),0,'no Check now with nothing to read');
  if(shots&&name==='checked')await page.screenshot({path:`${shots}/nothing-connected-${width}-${scheme}.png`});
  await context.close()}
 check={...done(0),phase:'reading'};[context,page]=await open();assert.ok(BUSY.includes(await line(page)),await line(page));await context.close();
 connectors=MAIL;
 if(shots){language='en';
  for(const scheme of ['light','dark'])for(const [width,height] of [[1440,900],[390,844]])for(const [name,c] of [['asleep',done()],['checking',{...done(0),phase:'reviewing',waiting:7}]]){
   check=c;[context,page]=await open({width,height,scheme});await page.screenshot({path:`${shots}/all-clear-${name}-${width}-${scheme}.png`});await context.close()}}
 assert.deepEqual(errors,[]);
 console.log('all-clear line ok');
}finally{await browser?.close();server.close()}
