import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Small things in the dashboard's shell, measured the way they look. Week or Month and back to Agenda opens the agenda
// where the Calendar opens from the nav (it sat 66px higher). On a computer window of any height the to-do list has
// no scroll box of its own: the whole sidebar scrolls as one column, as the phone's drawer. A board's ⋯ sits on the middle of its
// name. A Feedback row keeps its text and Edit and Remove on one middle line, also when the text wraps. Opening a person
// on the Graph keeps the head (its count, + New person) until the person's page is there. SHELL_SHOTS=<dir> saves shots.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),shotDir=process.env.SHELL_SHOTS,errors=[];
const card=i=>({id:String(i).padStart(16,'0'),title:'To-do number '+i+' with a longer title',body:'Made-up.',status:i%3?'pending':'prepared',scope:'work',created_at:now,event_ids:[]});
const meetings=Array.from({length:4},(_,i)=>{const a=new Date();a.setHours(9+i*2,0,0,0);const b=new Date(a);b.setHours(a.getHours()+1);return {id:i+1,account_id:'cal',title:'Meeting '+i,start:a.toISOString(),end:b.toISOString(),all_day:false,guests:1,url:''}});
const person={id:'email:ann@example.test',kind:'person',name:'Ann Example',strength:2,closeness:'close',last_at:now,signals:3,ids:['ann@example.test'],links:[],open:{cards:[]},recent:[]};
const stages=[{name:'Discovery'},{name:'Demo'},{name:'Won'}];
const boards=[{id:1,name:'Sales',stages,default:true,stuck:0,maybes:[],projects:[{id:'project:1',name:'Umicore',stage:'Demo',by:'owner',at:now,days:1,no_reply_days:0,org:{name:'Umicore',logo:null}}]}];
const facts=[{id:2,kind:'fact',text:'The team meets on Mondays at 10:00.',created_at:now,merged:0},
 {id:1,kind:'fact',text:'A long fact that wraps: when a partner asks for a co-marketing slot, check the shared calendar first and propose two dates in the same week, never more than three weeks out, and say which one suits best.',created_at:now,merged:0}];
let cards=[],nodeWait=0;
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],connectors:[{id:'cal',service:'calendar',status:'ok'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},facts,voices:[]}));return}
 if(url.pathname==='/api/calendar'){res.end(JSON.stringify({meetings,events:meetings,calendars:[]}));return}
 if(url.pathname==='/api/graph'){const node=url.searchParams.get('node');if(node){await new Promise(r=>setTimeout(r,nodeWait));res.end(JSON.stringify(person));return}
  res.end(JSON.stringify({projects:[],people:[person],quiet:[],new:[],orgs:[],whos:[],boards,person_names:[],project_names:[],counts:{person:1,org:0,project:1}}));return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
let browser;
const open=async size=>{const context=await browser.newContext({viewport:size,locale:'en-GB'});await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(base);await page.waitForFunction(()=>!/Connecting/.test(document.querySelector('#updated')?.textContent||'Connecting'));return page};
const shot=async(page,name)=>{if(shotDir)await page.screenshot({path:`${shotDir}/${name}.png`})};
const mid=r=>r.top+r.height/2;
// The whole sidebar scrolls as one column, the to-do list without a box of its own, and its bottom (Help, Settings) comes
// into view: on a short window, a laptop's app window (900 to 1000 high) and a tall one alike.
const sideOneColumn=async size=>{const tag=size.width+'x'+size.height;
 cards=Array.from({length:Math.ceil(size.height/16)},(_,i)=>card(i+1));const page=await open(size);await page.locator('#side-cards a').first().waitFor();
 // Each group's Show more, so a tall window has more rows than fit
 for(let i=0;i<4;i++){const more=page.locator('#side-cards button',{hasText:'Show more'});if(!await more.count())break;await more.first().click()}
 const side=await page.evaluate(()=>{const s=document.querySelector('#app-side'),l=document.querySelector('#side-cards');
  return {sideScrolls:s.scrollHeight>s.clientHeight+1,listScrolls:l.scrollHeight>l.clientHeight+1,listOverflow:getComputedStyle(l).overflowY}});
 assert.equal(side.listScrolls,false,`${tag}: the to-do list has no scroll box of its own ${JSON.stringify(side)}`);
 assert.equal(side.listOverflow,'visible',`${tag}: the to-do list never scrolls on its own`);
 assert.equal(side.sideScrolls,true,`${tag}: the whole sidebar scrolls`);await shot(page,`side-top-${tag}`);
 await page.mouse.move(120,size.height/2);await page.mouse.wheel(0,8000);await page.waitForTimeout(400);
 const end=await page.evaluate(()=>{const h=document.querySelector('#help-link-side, .app-side .head-side>.settings-link:last-child, #open-settings')?.getBoundingClientRect();return {bottom:h&&h.bottom,vh:innerHeight,page:scrollY}});
 assert.ok(end.bottom<=end.vh,`${tag}: the bottom of the sidebar comes into view ${JSON.stringify(end)}`);
 assert.equal(end.page,0,`${tag}: scrolling the sidebar leaves the page where it was`);await shot(page,`side-scrolled-${tag}`);
 // Folded to its icons, the hidden list takes no room: nothing to scroll
 await page.evaluate(()=>{document.documentElement.dataset.side='collapsed'});await page.waitForTimeout(100);
 assert.equal(await page.evaluate(()=>{const s=document.querySelector('#app-side');return s.scrollHeight>s.clientHeight+1}),false,`${tag}: the folded sidebar does not scroll`);
 await page.context().close()};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage'],ignoreDefaultArgs:['--hide-scrollbars']});
 for(const size of [{width:1440,height:900},{width:1440,height:700},{width:1280,height:650}]){
  const tag=size.width+'x'+size.height;
  // The agenda: from the nav, then Week and back, Month and back: the same place every time
  cards=[];let page=await open(size);
  const at=()=>page.evaluate(()=>{const k=new Date(),day=k.getFullYear()+'-'+String(k.getMonth()+1).padStart(2,'0')+'-'+String(k.getDate()).padStart(2,'0');
   const b=document.querySelector(`#calendar-view .cal-block[data-day="${day}"]`);return {y:Math.round(scrollY),top:b&&Math.round(b.getBoundingClientRect().top)}});
  await page.locator('nav [data-tab="calendar"]').click();await page.locator('#calendar-view .cal-block').first().waitFor();await page.waitForTimeout(300);
  const first=await at();assert.ok(first.top!==null,'today is in the agenda');await shot(page,`agenda-first-${tag}`);
  for(const v of ['week','month']){await page.locator(`#page-head [data-cal-mode="${v}"]`).click();await page.locator(v==='week'?'#calendar-view .cal-tg-body':'#calendar-view .cal-mg').first().waitFor();await page.waitForTimeout(300);
   await page.locator('#page-head [data-cal-mode="agenda"]').click();await page.waitForTimeout(500);
   assert.deepEqual(await at(),first,`${tag}: Agenda after ${v} sits where it opened`)}
  await shot(page,`agenda-back-${tag}`);
  // Back from Week by the browser's own Back: the same place too
  await page.locator('#page-head [data-cal-mode="week"]').click();await page.waitForTimeout(300);await page.goBack();await page.waitForTimeout(600);
  assert.deepEqual(await at(),first,`${tag}: Back to Agenda sits where it opened`);
  await page.context().close();

  // The sidebar with many to-dos: at any window height one column scrolls (no box of its own for the list)
  await sideOneColumn(size);
 }
 // A laptop's app window and a tall window: the same one column. No display-mode rule may give the list its own box
 // in the installed app, which opens in its own window.
 for(const size of [{width:1280,height:1000},{width:1440,height:1300},{width:1100,height:600}])await sideOneColumn(size);
 assert.doesNotMatch(dashboard,/@media[^{]*display-mode/,'the installed app has no layout of its own');
 // A board's ⋯ on the middle of its name; Feedback rows on one middle line; the Graph head until the person is there
 cards=[];const page=await open({width:1440,height:900});
 await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());await page.locator('#people-view').waitFor({state:'attached'});
 await page.evaluate(()=>document.querySelector('[data-graph-sub="projects"]').click());await page.locator('#people-view .proj-board:not([hidden]) .board-title').waitFor();
 const dots=await page.evaluate(()=>{const t=document.querySelector('#people-view .board-title').getBoundingClientRect(),s=document.querySelector('#people-view .board-menu>summary'),g=(s.querySelector('svg')||s).getBoundingClientRect();
  // the ink of the dots: the svg's circles, or the glyph's own box for a text ⋯ (its dots sit on the baseline)
  const ink=s.querySelector('svg circle')?.getBoundingClientRect();let glyph=null;if(!ink){const c=document.createElement('canvas').getContext('2d');const cs=getComputedStyle(s);c.font=`${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;const m=c.measureText(s.textContent.trim());
   const r=document.createRange();r.selectNodeContents(s);const box=r.getBoundingClientRect();const base=box.top+(box.height+m.fontBoundingBoxAscent-m.fontBoundingBoxDescent)/2;glyph={top:base-m.actualBoundingBoxAscent,height:m.actualBoundingBoxAscent+m.actualBoundingBoxDescent}}
  const d=ink||glyph;return {title:t.top+t.height/2,dots:d.top+d.height/2}});
 assert.ok(Math.abs(dots.dots-dots.title)<=2,`the board's ⋯ sits on the middle of its name ${JSON.stringify(dots)}`);await shot(page,'board-dots');
 // Graph: open a person while the page loads slowly; the head stays as it was until the page is drawn
 await page.evaluate(()=>document.querySelector('[data-graph-sub="people"]').click());await page.locator('#people-view [data-node]:visible').first().waitFor();await page.waitForTimeout(300);
 const head=()=>page.evaluate(()=>{const h=document.querySelector('#page-head');return {text:h.textContent.replace(/\s+/g,' ').trim(),height:h.offsetHeight}});
 const before=await head();nodeWait=800;
 await page.locator('#people-view [data-node]:visible').first().click();await page.waitForTimeout(300);
 assert.equal(await page.locator('.graph-crumbs').count(),0,'the person is still loading');
 assert.deepEqual(await head(),before,'the head stays until the person is there');
 await page.locator('.graph-crumbs').waitFor();assert.equal(await page.locator('#page-head .page-title').textContent(),'People');nodeWait=0;
 // Feedback: each fact's text, Edit and Remove share one middle line, one line or several
 await page.evaluate(()=>document.querySelector('nav [data-tab="feedback"]').click());await page.locator('#facts .fact-row').first().waitFor();
 const rows=await page.locator('#facts .fact-row').evaluateAll(rs=>rs.map(r=>{const t=r.querySelector('.grow').getBoundingClientRect(),b=[...r.querySelectorAll('.learn-acts button')].map(x=>x.getBoundingClientRect());const line=parseFloat(getComputedStyle(r.querySelector('.grow')).lineHeight);
  return {lines:Math.round(t.height/line),text:t.top+t.height/2,buttons:b.map(x=>x.top+x.height/2)}}));
 assert.ok(rows.some(r=>r.lines>1)&&rows.some(r=>r.lines===1),'one short fact and one that wraps '+JSON.stringify(rows));
 for(const r of rows)for(const b of r.buttons)assert.ok(Math.abs(b-r.text)<=1.5,`Edit and Remove on the middle of the text ${JSON.stringify(r)}`);
 await page.locator('#facts .fact-row').last().scrollIntoViewIfNeeded();await shot(page,'feedback-rows');
 assert.deepEqual(errors,[]);
 console.log('shell details ok');
}finally{await browser?.close();server.close()}
