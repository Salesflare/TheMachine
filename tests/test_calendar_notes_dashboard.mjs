import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A dated note (a trip) in the Calendar: a band in the All day strip of every day it covers, in the agenda and in the
// Week grid, with its dates, and it opens the note in the Graph. One that ends before the window shows nowhere.
// CALENDAR_NOTES_SHOT=<dir> also writes screenshots at 390 and 1440 in light and dark.
process.env.TZ='Europe/Brussels';
const dashboard=await dashboardPage();
const day=n=>{const d=new Date();d.setDate(d.getDate()+n);d.setHours(12,0,0,0);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')};
const at=(n,h)=>{const d=new Date();d.setDate(d.getDate()+n);d.setHours(h,0,0,0);return d.toISOString()};
const notes=[{id:'note:7',kind:'trip',name:'Lisbon trip',starts:day(2),ends:day(4)},{id:'note:8',kind:'trip',name:'Old trip',starts:day(-40),ends:day(-38)}];
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
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.goto(base);await page.waitForFunction(()=>typeof showTab==='function');
 await page.evaluate(()=>showTab('calendar'));await page.locator('#calendar-view .cal-item,#calendar-view .cal-chip').first().waitFor();
 await page.waitForFunction(()=>calMeetings!==null&&![...calWeeks.values()].some(w=>w.loading));return {context,page}};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const {context,page}=await open(390,'light');
 // In the agenda: on each of its three days, first, All day, with its dates; never on a day outside them
 const rows=await page.locator('#calendar-view .cal-block').evaluateAll(b=>b.map(x=>[x.dataset.day||'',[...x.querySelectorAll('.cal-item')].map(r=>r.querySelector('.cal-time').textContent+' | '+r.querySelector('.cal-title').textContent+' | '+(r.querySelector('.cal-sub')?.textContent||''))]));
 const banded=rows.filter(([,r])=>r.some(x=>x.includes('Lisbon trip')));
 assert.equal(banded.length,3,JSON.stringify(rows));
 for(const [,r] of banded){assert.match(r[0],/^All day \| Lisbon trip \| Trip · \w{3} \d{1,2} (to|–) \w{3} \d{1,2}$/,JSON.stringify(r))}
 assert.ok(!rows.some(([,r])=>r.some(x=>x.includes('Old trip'))));
 // It opens the note
 assert.equal(await page.locator('#calendar-view a.cal-item.k-note').first().getAttribute('href'),'#graph/note%3A7');
 if(process.env.CALENDAR_NOTES_SHOT){await page.locator('#calendar-view a.k-note').first().scrollIntoViewIfNeeded();await page.screenshot({path:process.env.CALENDAR_NOTES_SHOT+'/cal-note-390-light.png'})}
 await page.locator('#calendar-view a.k-note').first().click();
 await page.waitForFunction(()=>decodeURIComponent(location.hash)==='#graph/note:7');
 await page.goBack();await page.waitForFunction(()=>location.hash.startsWith('#calendar'));
 await context.close();
 // In the Week grid on a computer: a chip in each of its days' All day strip
 for(const scheme of ['light','dark']){const {context,page}=await open(1440,scheme);
  await page.evaluate(d=>{location.hash='#calendar?view=week&date='+d},day(3));
  await page.locator('#calendar-view .cal-chip.k-note').first().waitFor();
  assert.equal(await page.locator('#calendar-view .cal-chip.k-note').count(),3,'a band on each of its days in the Week grid');
  if(process.env.CALENDAR_NOTES_SHOT)await page.screenshot({path:process.env.CALENDAR_NOTES_SHOT+`/cal-note-1440-${scheme}.png`});
  // And in the month
  await page.evaluate(d=>{location.hash='#calendar?view=month&date='+d},day(3));
  await page.waitForFunction(()=>document.querySelectorAll('#calendar-view .k-note').length===3);
  await context.close()}
 if(process.env.CALENDAR_NOTES_SHOT){const {context,page}=await open(390,'dark');await page.locator('#calendar-view a.k-note').first().scrollIntoViewIfNeeded();
  await page.screenshot({path:process.env.CALENDAR_NOTES_SHOT+'/cal-note-390-dark.png'});await context.close()}
 assert.deepEqual(posts,[],'viewing is read-only');
 assert.deepEqual(errors,[]);
 console.log('ok calendar notes');
}finally{await browser?.close();server.close()}
