import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The dashboard's shell. On a phone the All clear line wraps and nothing is wider than the screen. On a short computer
// screen the whole sidebar scrolls, so Settings stays reachable. The lit Graph row follows the page on screen (a person
// lights People) and goes out with Settings. A person's page keeps the section's head above its breadcrumb. The week
// grid's columns line up under its head also with a scrollbar that takes room, and the grid fills the window so only it scrolls. View in browser on a computer shows
// the Machine's browser in the pane, never a new window.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString(),day=n=>{const d=new Date();d.setDate(d.getDate()+n);return d.toISOString()};
const person={id:'email:ann@example.test',kind:'person',name:'Ann Example',strength:2,closeness:'close',last_at:now,signals:3,ids:['ann@example.test'],links:[],open:{cards:[]},recent:[]};
const card=(id,extra)=>({id,title:'Card '+id,body:'Made-up.',status:'pending',scope:'work',created_at:now,event_ids:[],...extra});
let cards=[],browser_embed=null;const shows=[],errors=[];
const promises=Array.from({length:12},(_,i)=>({id:i+1,direction:'mine',who:'Someone',what:'send the recap '+i,due:null,state:'open',made_at:now,check_at:now}));
const meetings=Array.from({length:5},(_,i)=>{const a=new Date();a.setHours(9+i*2,0,0,0);const b=new Date(a);b.setHours(a.getHours()+1);return {id:i+1,account_id:'cal',title:'Meeting '+i,start:a.toISOString(),end:b.toISOString(),all_day:false,guests:1,url:''}});
const state=()=>({suggestions:cards,promises,connectors:[{id:'cal',service:'calendar',status:'ok'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 browser_link:browser_embed?'https://cp.example/open?to=browser':null,browser_embed});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/graph'){const node=url.searchParams.get('node');res.end(JSON.stringify(node?person:{projects:[],people:[person],quiet:[],new:[],orgs:[]}));return}
 if(url.pathname==='/api/calendar'){res.end(JSON.stringify({meetings,events:meetings}));return}
 if(url.pathname==='/api/action'){const call=JSON.parse(body||'{}');if(call.action==='browser_show'){shows.push(call.args.suggestion_id);res.end('{"shown":true}');return}res.end('{}');return}
 if(url.pathname.startsWith('/browser/')){res.setHeader('Content-Type','text/html');res.end('<body><p id="viewer">viewer</p></body>');return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
let browser;
const open=async(size,extra={})=>{const context=await browser.newContext({viewport:size,...extra});await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(base);await page.waitForFunction(()=>!/Connecting/.test(document.querySelector('#updated')?.textContent||'Connecting'));return page};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage'],ignoreDefaultArgs:['--hide-scrollbars']});
 // A phone, all clear with a long count line: it wraps inside the screen
 cards=[card('a'.repeat(16),{status:'snoozed',snoozed_until:day(2)}),card('b'.repeat(16),{status:'snoozed',snoozed_until:day(3)})];
 let page=await open({width:390,height:844},{isMobile:true,hasTouch:true});
 const sub=page.locator('#page-head .page-sub');await sub.waitFor();
 assert.match(await sub.textContent(),/^All clear · 2 coming back later · 12 promises kept track of$/);
 const box=await sub.boundingBox();assert.ok(box.x>=0&&box.x+box.width<=390,'the line stays on screen');
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
 await page.context().close();
 // A short computer screen: the sidebar scrolls down to Settings
 cards=[];page=await open({width:1440,height:420});
 const side=await page.evaluate(()=>{const s=document.querySelector('#app-side');return {scrolls:s.scrollHeight>s.clientHeight,overflow:getComputedStyle(s).overflowY}});
 assert.ok(side.scrolls&&side.overflow==='auto','the sidebar scrolls when it is taller than the screen');
 await page.locator('#open-settings').scrollIntoViewIfNeeded();await page.locator('#open-settings').click();await page.locator('#settings').waitFor();
 // Graph rows: a person lights People; Settings puts it out; the head stays on the person's page
 await page.setViewportSize({width:1440,height:900});
 await page.locator('.side-sub a[data-graph-sub="people"]').click();await page.locator('#people-view .person-item').first().waitFor();
 await page.locator('#people-view .person-item button.node, #people-view .person-item').first().click();await page.locator('.graph-crumbs').waitFor();
 assert.equal(await page.locator('#page-head').isVisible(),true,'the head stays on a person');
 assert.equal(await page.locator('#page-head .page-title').textContent(),'People');
 assert.deepEqual(await page.locator('.side-sub a[aria-current]').evaluateAll(a=>a.map(x=>x.dataset.graphSub)),['people']);
 await page.locator('#open-settings').click();await page.locator('#settings').waitFor();
 assert.equal(await page.locator('.side-sub a[aria-current]').count(),0,'Settings puts the Graph row out');
 await page.goBack();await page.locator('#people').waitFor();
 assert.deepEqual(await page.locator('.side-sub a[aria-current]').evaluateAll(a=>a.map(x=>x.dataset.graphSub)),['people']);
 // The week grid with a scrollbar that takes room: every column starts where its head does
 await page.locator('nav [data-tab="calendar"]').click();await page.locator('#page-head [data-cal-mode="week"]').click();await page.locator('.cal-tg-body').waitFor();
 const cols=await page.evaluate(()=>['.cal-tg-head','.cal-tg-body'].map(s=>[...document.querySelector(s).children].map(c=>Math.round(c.getBoundingClientRect().left))));
 assert.deepEqual(cols[1],cols[0],'the hours line up under the days');
 const nums=await page.locator('.cal-tg-day b').evaluateAll(bs=>[...new Set(bs.map(b=>Math.round(b.getBoundingClientRect().top)))]);assert.equal(nums.length,1,'every day number on one line, today too');
 await page.waitForFunction(()=>document.documentElement.scrollHeight<=innerHeight);  // only the grid scrolls, not the page
 assert.equal(await page.evaluate(()=>getComputedStyle(document.querySelector('.cal-tg-scroll')).scrollbarWidth),'thin');
 assert.equal(await page.evaluate(()=>calAbreast(7)+','+calAbreast(1)),'2,3','two abreast in a week column, three in a day');
 await page.context().close();
 // View in browser on a computer: the pane, and the task's page in front there; no new window
 browser_embed='/browser/?autoconnect=1&reconnect=1&resize=remote&path=browser/websockify';
 cards=[card('c'.repeat(16),{status:'prepared',smart_actions:[{kind:'open',browser:true,label:'View in browser',revision:1}]})];
 page=await open({width:1440,height:900});
 const link=page.locator('[data-browser-show]').first();
 if(await link.count()){let popup=false;page.context().on('page',()=>{popup=true});
  await link.click();await page.locator('#browser-pane').waitFor();assert.equal(popup,false,'no new window');
  assert.equal(await page.locator('#bp-frame').getAttribute('src'),browser_embed);
  await page.waitForFunction(()=>true);await new Promise(r=>setTimeout(r,300));assert.deepEqual(shows,['c'.repeat(16)])}
 else{  // without the card's button in this fixture, the same click handler from a plain link
  await page.evaluate(()=>{const a=document.createElement('a');a.href='https://cp.example/open?to=browser';a.target='_blank';a.dataset.browserShow='cccccccccccccccc';a.id='vib';a.textContent='View in browser';document.querySelector('main').prepend(a)});
  let popup=false;page.context().on('page',()=>{popup=true});await page.locator('#vib').click();await page.locator('#browser-pane').waitFor();assert.equal(popup,false,'no new window');
  await new Promise(r=>setTimeout(r,300));assert.deepEqual(shows,['c'.repeat(16)])}
 assert.deepEqual(errors,[]);
 console.log('shell layout ok');
}finally{await browser?.close();server.close()}
