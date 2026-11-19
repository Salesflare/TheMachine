import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A dated note (a trip) in the Calendar. The agenda has it first on each of its days, as "Lisbon trip" with its dates.
// The Week and Month grids draw one band across its days: pieces that join edge to edge, the name only where it starts
// and where a week's row begins (a trip over a weekend wraps to the next row and is named again). It opens the note in
// the Graph. One that ends before the window shows nowhere. CALENDAR_NOTES_SHOT=<dir> also writes screenshots at 390
// and 1440 in light and dark.
// The page's clock is pinned to NOW and every date is built from it: from the real clock, the Lisbon trip (today +2 to +4)
// split over two weeks whenever the test ran on a Thursday or a Friday, and the Week view then had two pieces, not three.
process.env.TZ='Europe/Brussels';
const NOW=new Date('2026-11-16T10:00:00+01:00');  // a Monday: the trip is Wednesday to Friday
const dashboard=await dashboardPage();
const day=n=>{const d=new Date(NOW);d.setDate(d.getDate()+n);d.setHours(12,0,0,0);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')};
const at=(n,h)=>{const d=new Date(NOW);d.setDate(d.getDate()+n);d.setHours(h,0,0,0);return d.toISOString()};
const sat=(()=>{let n=14;while(new Date(day(n)+'T12:00').getDay()!==6)n++;return n})();  // a Saturday two weeks or more out
const notes=[{id:'note:7',kind:'trip',name:'Lisbon',starts:day(2),ends:day(4)},{id:'note:9',kind:'trip',name:'Porto trip',starts:day(sat),ends:day(sat+3)},
 {id:'note:8',kind:'trip',name:'Old trip',starts:day(-40),ends:day(-38)}];
const meetings=[{id:201,account_id:'cal',title:'Pilot review',start:at(3,15),end:at(3,16),all_day:false,location:'',guests:2,url:null}];
const state={suggestions:[],promises:[],connectors:[{id:'cal',email:'owner@example.com',service:'calendar',status:'ok'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]}};
const posts=[];
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.method!=='GET')posts.push(url.pathname);
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/calendar'){const a=url.searchParams.get('from').slice(0,10),b=url.searchParams.get('to').slice(0,10);
  res.end(JSON.stringify({meetings,notes:notes.filter(n=>n.starts<=b&&n.ends>=a)}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const open=async(width,scheme)=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height:mobile?844:900},isMobile:mobile,hasTouch:mobile,locale:'en-GB',timezoneId:'Europe/Brussels',colorScheme:scheme});
 await context.clock.setFixedTime(NOW);
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.goto(base);await page.waitForFunction(()=>typeof showTab==='function');
 await page.evaluate(()=>showTab('calendar'));await page.locator('#calendar-view .cal-item,#calendar-view .cal-chip').first().waitFor();
 await page.waitForFunction(()=>calMeetings!==null&&![...calWeeks.values()].some(w=>w.loading));return {context,page}};
const go=async(page,view,d,count)=>{await page.evaluate(([v,d])=>{location.hash='#calendar?view='+v+'&date='+d},[view,d]);
 await page.waitForFunction(n=>(n==null||document.querySelectorAll('#calendar-view .cal-band').length===n)&&![...calWeeks.values()].some(w=>w.loading),count)};
// The band's pieces by row (their top): each piece's box, and the name it shows
const pieces=(page,href)=>page.locator(`#calendar-view .cal-band[href="${href}"]`).evaluateAll(b=>b.map(x=>{const r=x.getBoundingClientRect();return {top:Math.round(r.top),left:r.left,right:r.right,name:x.textContent.trim()}}));
const joined=(list,what)=>{const rows=new Map();for(const p of list){if(!rows.has(p.top))rows.set(p.top,[]);rows.get(p.top).push(p)}
 for(const row of rows.values()){row.sort((a,b)=>a.left-b.left);for(let i=1;i<row.length;i++)assert.ok(Math.abs(row[i].left-row[i-1].right)<=1,`${what}: the pieces join (${row[i-1].right} → ${row[i].left})`)}
 return [...rows.values()].map(r=>r.map(p=>p.name))};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const {context,page}=await open(390,'light');
 // In the agenda: on each of its three days, first, All day, "Lisbon trip" with its dates; never on a day outside them
 const rows=await page.locator('#calendar-view .cal-block').evaluateAll(b=>b.map(x=>[x.dataset.day||'',[...x.querySelectorAll('.cal-item')].map(r=>r.querySelector('.cal-time').textContent+' | '+r.querySelector('.cal-title').textContent+' | '+(r.querySelector('.cal-sub')?.textContent||''))]));
 const banded=rows.filter(([,r])=>r.some(x=>x.includes('Lisbon trip')));
 assert.equal(banded.length,3,JSON.stringify(rows));
 for(const [,r] of banded){assert.match(r[0],/^All day \| Lisbon trip \| \w{3} \d{1,2} (to|–) \w{3} \d{1,2}$/,JSON.stringify(r))}
 assert.ok(!rows.some(([,r])=>r.some(x=>x.includes('Old trip'))));
 // It opens the note
 assert.equal(await page.locator('#calendar-view a.cal-item.k-note').first().getAttribute('href'),'#graph/note%3A7');
 if(process.env.CALENDAR_NOTES_SHOT){await page.locator('#calendar-view a.k-note').first().scrollIntoViewIfNeeded();await page.screenshot({path:process.env.CALENDAR_NOTES_SHOT+'/cal-note-390-light.png'})}
 await page.locator('#calendar-view a.k-note').first().click();
 await page.waitForFunction(()=>decodeURIComponent(location.hash)==='#graph/note:7');
 await page.goBack();await page.waitForFunction(()=>location.hash.startsWith('#calendar'));
 await context.close();
 // The Week and Month grids on a computer: one band, named once per row; a named piece opens the note
 for(const scheme of ['light','dark']){const {context,page}=await open(1440,scheme);
  await go(page,'week',day(3),3);
  assert.deepEqual(joined(await pieces(page,'#graph/note%3A7'),'week'),[['Lisbon trip','','']]);
  assert.equal(await page.locator('#calendar-view .cal-band .t').count(),0,'no "All day" inside the All day row');
  if(process.env.CALENDAR_NOTES_SHOT)await page.screenshot({path:process.env.CALENDAR_NOTES_SHOT+`/cal-note-1440-${scheme}.png`});
  // Over a weekend in the month: Saturday and Sunday at the end of one row, Monday and Tuesday starting the next
  await page.evaluate(d=>{location.hash='#calendar?view=month&date='+d},day(sat));
  await page.waitForFunction(()=>document.querySelector('#calendar-view .cal-band[href="#graph/note%3A9"]')&&![...calWeeks.values()].some(w=>w.loading));
  assert.deepEqual(joined(await pieces(page,'#graph/note%3A9'),'month'),[['Porto trip',''],['Porto trip','']]);
  if(process.env.CALENDAR_NOTES_SHOT)await page.screenshot({path:process.env.CALENDAR_NOTES_SHOT+`/cal-note-month-1440-${scheme}.png`});
  await page.locator('#calendar-view .cal-band.b-head[href="#graph/note%3A9"]').first().click();
  await page.waitForFunction(()=>decodeURIComponent(location.hash)==='#graph/note:9');
  await context.close()}
 if(process.env.CALENDAR_NOTES_SHOT){const {context,page}=await open(390,'dark');await page.locator('#calendar-view a.k-note').first().scrollIntoViewIfNeeded();
  await page.screenshot({path:process.env.CALENDAR_NOTES_SHOT+'/cal-note-390-dark.png'});
  await go(page,'week',day(3),null);await page.waitForTimeout(300);
  await page.screenshot({path:process.env.CALENDAR_NOTES_SHOT+'/cal-note-week-390-dark.png'});await context.close()}
 assert.deepEqual(posts,[],'viewing is read-only');
 assert.deepEqual(errors,[]);
 console.log('ok calendar notes');
}finally{await browser?.close();server.close()}
