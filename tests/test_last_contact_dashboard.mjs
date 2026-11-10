import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
import {navClick} from './nav-click.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Last contact (and last signal) reads as people say it (sinceWhen, settings-models.js): just now, 5 minutes ago,
// 3 hours ago on the same day, yesterday, 3 days ago up to a week, then a short date in the owner's date order, the
// year only when it isn't this one. A day without a time of day never claims hours: today. Every language through
// Intl, and the exact date in the hover (sinceTitle). On People and Organizations rows and a person's page.
// SHOT_DIR=… saves screenshots.
const dashboard=await dashboardPage();
const person=(n,name,last_at,extra={})=>({id:'email:p'+n+'@example.test',kind:'person',name,strength:3-n/4,closeness:'regular',last_at,signals:5,ids:['p'+n+'@example.test'],
 usual_gap_days:7,quiet:false,role:null,profile:null,links:[],recent:[],around:[],open:{},...extra});
const people=[person(1,'Ada Lovelace','2026-11-10T14:59:30+01:00',{role:'customer'}),person(2,'Grace Hopper','2026-11-10T12:10:00+01:00'),person(3,'Alan Turing','2026-11-10'),
 person(4,'Edsger Dijkstra','2026-11-09'),person(5,'Barbara Liskov','2026-11-07T09:00:00Z',{closeness:'occasional'}),person(6,'Donald Knuth','2026-10-29'),person(7,'Frances Allen','2025-12-24')];
const orgs=[{id:'org:lumen.example',kind:'org',name:'Lumen',strength:3,last_at:'2026-11-09T16:00:00+01:00',signals:4},{id:'org:north.example',kind:'org',name:'North',strength:2,last_at:'2026-10-02',signals:2}];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const node=url.searchParams.get('node');res.end(JSON.stringify(node?people.find(p=>p.id===node):{projects:[],people,quiet:[],new:[],orgs}));return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({timezoneId:'Europe/Brussels',locale:'en-US'}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await page.clock.setFixedTime(new Date('2026-11-10T15:00:00+01:00'));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.waitForFunction(()=>typeof sinceWhen==='function');
 const say=(loc,vals)=>page.evaluate(([loc,vals])=>{DL=loc;return vals.map(v=>sinceWhen(v))},[loc,vals]);
 const cases=[
  ['2026-11-10T14:59:30+01:00','just now'],
  ['2026-11-10T14:55:00+01:00','5 minutes ago'],
  ['2026-11-10T12:00:00+01:00','3 hours ago'],
  ['2026-11-10T00:30:00+01:00','14 hours ago'],
  ['2026-11-10','today'],                       // only the day is known: no hours
  ['2026-11-09T23:30:00+01:00','yesterday'],    // before midnight, more than an hour ago
  ['2026-11-09','yesterday'],
  ['2026-11-07T09:00:00Z','3 days ago'],
  ['2026-11-04','6 days ago'],
  ['2026-11-03','Nov 3'],                       // a week or more: the date
  ['2026-01-02T10:00:00Z','Jan 2'],
  ['2025-12-24','Dec 24, 2025'],                // another year: with the year
  ['2026-11-12','Nov 12'],                      // ahead (a clock off): the date, never "in 2 days"
  ['','never']];
 assert.deepEqual(await say('en-US',cases.map(c=>c[0])),cases.map(c=>c[1]));
 assert.deepEqual(await say('en-GB',['2026-11-03','2025-12-24','2026-11-09']),['3 Nov','24 Dec 2025','yesterday']);  // day first
 const some=['2026-11-10T12:00:00+01:00','2026-11-10','2026-11-09','2026-11-07','2026-11-03'];
 assert.deepEqual(await say('nl-BE',some),['3 uur geleden','vandaag','gisteren','3 dagen geleden','3 nov']);
 assert.deepEqual(await say('fr-FR',some),['il y a 3 heures','aujourd’hui','hier','il y a 3 jours','3 nov.']);
 assert.deepEqual(await say('de-DE',some),['vor 3 Stunden','heute','gestern','vor 3 Tagen','3. Nov.']);
 // ("just now" is the catalog's, as in ago())
 // The exact date on hover: the day, and the time when it's known
 assert.deepEqual(await page.evaluate(()=>{DL='en-US';H12=false;return [sinceTitle('2026-11-09'),sinceTitle('2026-11-10T12:00:00+01:00'),sinceTitle('')]}),
  ['Monday, November 9, 2026','Tuesday, November 10, 2026, 12:00','']);
 assert.equal(await page.evaluate(()=>{DL='en-US';return String(sinceTime('2026-11-09'))}),'<time datetime="2026-11-09" title="Monday, November 9, 2026">yesterday</time>');
 assert.equal(await page.evaluate(()=>String(sinceTime(null))),'never');
 // In a sentence: the catalog's words around it, the <time> kept
 assert.equal(await page.evaluate(()=>{DL='en-US';return String(htmlT('last contact {}',sinceTime('2026-11-07')))}),'last contact <time datetime="2026-11-07" title="Saturday, November 7, 2026">3 days ago</time>');
 await context.close();
 // On the page: People rows, Organizations rows and a person's page, at 390 and 1440, light and dark
 for(const [width,height,scheme] of process.env.SHOT_DIR?[[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]:[[390,844,'light']]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,deviceScaleFactor:width<500?2:1,timezoneId:'Europe/Brussels',locale:'en-US'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.clock.setFixedTime(new Date('2026-11-10T15:00:00+01:00'));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await navClick(page.locator('nav [data-tab="people"]'));
  await navClick(page.locator('.side-sub a[data-graph-sub="people"]'));
  const row=id=>page.locator(`#people-view article[data-node="${id}"] .graph-sub time`);
  await row(people[0].id).waitFor();
  assert.deepEqual(await page.locator('#people-view article.person-item .graph-sub time').allTextContents(),['just now','2 hours ago','today','yesterday','3 days ago','Oct 29','Dec 24, 2025']);
  assert.equal(await row(people[3].id).getAttribute('title'),'Monday, November 9, 2026');
  assert.match(await page.locator(`#people-view article[data-node="${people[0].id}"] .graph-sub`).textContent(),/^Customer · last contact just now · usually every 7 days · p1@example\.test$/);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  if(process.env.SHOT_DIR){await mkdir(process.env.SHOT_DIR,{recursive:true});await page.screenshot({path:`${process.env.SHOT_DIR}/people-${width}-${scheme}.png`})}
  await navClick(page.locator('.side-sub a[data-graph-sub="orgs"]'));
  await page.locator('#people-view article[data-node="org:lumen.example"] time').waitFor();
  assert.deepEqual(await page.locator('#people-view article[data-node^="org:"] time').allTextContents(),['yesterday','Oct 2']);
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/orgs-${width}-${scheme}.png`});
  await page.goto('http://127.0.0.1:'+server.address().port+'/#graph/'+encodeURIComponent(people[4].id));
  await page.locator('.graph-detail .person-rel time').waitFor();
  assert.equal(await page.locator('.graph-detail .person-rel').textContent(),'Talk weekly · last contact 3 days ago');
  assert.equal(await page.locator('.graph-detail .person-rel time').getAttribute('title'),'Saturday, November 7, 2026, 10:00');
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/person-${width}-${scheme}.png`});
  assert.deepEqual(errors,[]);
  await context.close();
 }
 console.log('last contact ok');
}finally{await browser?.close();server.close()}
