import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Where the Calendar starts. A calendar's first read goes a week back from when it was connected, so before that day
// nothing came in, and empty days there would read as "nothing planned". The agenda stops there: one muted line at its
// top says where the calendar starts ("a week before you joined" when it came with the start), and no Show earlier days.
// Week and Month say it over a period that holds days before it. A clear week after the start, or no calendar read yet
// (starts: null), says nothing. Once its history is in, the line says where the history starts. Nothing is wider than the screen at 390 and 1440, and viewing sends nothing.
// The clock is fixed on Tuesday 27 October 2026; the calendar starts on Friday 23 October.
// CALENDAR_SHOT=<dir> also writes screenshots.
process.env.TZ='Europe/Brussels';
const dashboard=await dashboardPage();
const brand={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'};
const NOW=new Date('2026-10-27T12:00:00+01:00'),START='2026-10-23';
const at=(days,h,m=0)=>{const d=new Date(NOW);d.setDate(d.getDate()+days);d.setHours(h,m,0,0);return d};
const iso=d=>d.toISOString(),now=iso(NOW);
// Made-up meetings from the start on, none in the week of 2 November (a clear week, no edge)
const meetings=[];for(let n=-4;n<=20;n+=1)if(n%2===0&&!(n>=6&&n<=12))meetings.push({id:2000+n,account_id:'cal',title:`Sync ${n<0?'before':'after'} ${Math.abs(n)}`,start:iso(at(n,10)),end:iso(at(n,10,30)),all_day:false,location:'',guests:2,url:'https://calendar.example/e/'+n});
const cards=[{id:'b'.repeat(16),title:'Send the revised quote',body:'Made-up card.',status:'pending',scope:'work',created_at:now,event_ids:[],due:'2026-10-27'}];
let calls=[],asks=[],starts={day:START,joined:true};const errors=[];
const state=()=>({suggestions:cards,promises:[],connectors:[{id:'cal',service:'calendar',status:'ok'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(brand[url.pathname]){res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+brand[url.pathname],import.meta.url)));return}
 if(url.pathname==='/api/action'&&/"action":"client_error"/.test(body)){res.end('{"ok":true,"counted":0}');return}
 if(req.method!=='GET')calls.push(url.pathname+' '+body);
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/calendar'){const a=new Date(url.searchParams.get('from')),b=new Date(url.searchParams.get('to'));asks.push([a,b]);
  res.end(JSON.stringify({meetings:meetings.filter(m=>new Date(m.start)<b&&new Date(m.end)>a),calendars:[],starts}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
let browser;
const open=async(width,height,scheme='light',hash='')=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme});
 await context.clock.setFixedTime(NOW);
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));await page.goto(base+hash);return {context,page}};
const toCal=async page=>{await page.locator('#task-'+cards[0].id).waitFor();await page.evaluate(()=>showTab('calendar'));await page.locator('#calendar-view [data-day]').first().waitFor();await page.waitForFunction(()=>document.querySelectorAll('#calendar-view .cal-item').length>2)};
const line=page=>page.evaluate(()=>[...document.querySelectorAll('#calendar-view .cal-start')].map(e=>e.textContent));
const days=page=>page.evaluate(()=>[...document.querySelectorAll('#calendar-view [data-day]')].map(e=>e.dataset.day));
const fits=(page,where)=>page.evaluate(()=>({page:document.documentElement.scrollWidth,vw:innerWidth})).then(s=>assert.ok(s.page<=s.vw,`${where}: wider than the screen ${JSON.stringify(s)}`));
const SAID='Your calendar starts Fri, Oct 23, a week before you joined.';
// The agenda: earlier days up to the start, then the line instead of Show earlier days, and no further asks
async function toStart(page){await page.locator('[data-cal-more="up"] button').click();await page.locator('#calendar-view .cal-start').waitFor();await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(200)}
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [w,h] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){const {context,page}=await open(w,h,scheme);await toCal(page);
  assert.deepEqual(await line(page),[],'today is after the start: no line yet');assert.equal(await page.locator('[data-cal-more="up"]').count(),1);
  await toStart(page);
  assert.deepEqual(await line(page),[SAID]);assert.equal(await page.locator('[data-cal-more="up"]').count(),0,'no earlier days to show');
  const d=await days(page);assert.equal(d[0],START,'the agenda starts on the first day that came in: '+d);
  const top=await page.evaluate(()=>[document.querySelector('.cal-start').getBoundingClientRect().bottom,document.querySelector('#calendar-view [data-day]').getBoundingClientRect().top]);
  assert.ok(top[0]<=top[1],'the line sits above the first day');
  const n=asks.length;await page.evaluate(()=>dispatchEvent(new WheelEvent('wheel',{deltaY:-400})));await page.waitForTimeout(300);assert.equal(asks.length,n,'nothing earlier is asked for');
  await fits(page,`agenda ${w} ${scheme}`);
  if(process.env.CALENDAR_SHOT)await page.screenshot({path:`${process.env.CALENDAR_SHOT}/agenda-${w}-${scheme}.png`});
  // Week: the week that holds the start says it; the clear week after it says nothing
  await page.evaluate(()=>{location.hash='#calendar?view=week&date=2026-10-19'});await page.locator('.cal-tg').waitFor();
  if(w>600){assert.deepEqual(await line(page),[SAID],'the week before the start');
   if(process.env.CALENDAR_SHOT)await page.screenshot({path:`${process.env.CALENDAR_SHOT}/week-${w}-${scheme}.png`})}
  await page.evaluate(()=>{location.hash='#calendar?view=week&date=2026-11-02'});await page.waitForFunction(()=>document.querySelector('.cal-range')?.textContent.includes('Nov'));
  assert.deepEqual(await line(page),[],'a clear week after the start is just clear');
  await page.evaluate(()=>{location.hash='#calendar?view=month&date=2026-10-01'});await page.locator('.cal-mg').waitFor();assert.deepEqual(await line(page),[SAID],'October holds the start');
  await page.evaluate(()=>{location.hash='#calendar?view=month&date=2026-12-01'});await page.waitForFunction(()=>document.querySelector('.cal-range')?.textContent.includes('Dec'));assert.deepEqual(await line(page),[]);
  await fits(page,`month ${w} ${scheme}`);
  await context.close()}
 // Connected later than the start: the line says only where it starts
 {starts={day:START,joined:false};const {context,page}=await open(1440,900);await toCal(page);await toStart(page);
  assert.deepEqual(await line(page),['Your calendar starts Fri, Oct 23.']);await context.close()}
 // Its history is in (docs/help/history.md): the line says where that starts, a year back, with the year
 {starts={day:'2025-10-27',joined:false,history:true};const {context,page}=await open(1440,900);await toCal(page);
  await page.evaluate(()=>{location.hash='#calendar?view=month&date=2025-10-01'});await page.locator('.cal-mg').waitFor();
  await page.waitForFunction(()=>document.querySelector('.cal-range')?.textContent.includes('2025'));
  assert.deepEqual(await line(page),['Your calendar history starts October 27, 2025.']);  // US order in US English
  await page.evaluate(()=>{DL='en-GB';calRender()});assert.deepEqual(await line(page),['Your calendar history starts 27 October 2025.'],'the owner\'s date format');
  await context.close()}
 // No calendar read yet: no line, and earlier days load as before
 {starts=null;const {context,page}=await open(1440,900);await toCal(page);await page.locator('[data-cal-more="up"] button').click();
  await page.waitForFunction(()=>document.querySelector('#calendar-view [data-day]').dataset.day<'2026-10-27');
  assert.deepEqual(await line(page),[]);assert.equal(await page.locator('[data-cal-more="up"]').count(),1,'earlier days still load');await context.close()}
 assert.deepEqual(calls,[],'viewing sends nothing');
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log(JSON.stringify({asks:asks.length,posts:calls.length,page_errors:errors}));
