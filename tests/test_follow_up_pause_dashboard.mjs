import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Pause and Resume for follow-ups (follow_ups.pause, follow_up_pause): a paused board says "Follow-ups on" with a small
// "Paused" chip and no next date, its tiles show the chip, and the settings panel has Pause (with an optional day to
// resume on) or Resume, applied at once without Save. A project held by its board's pause says so and resumes on the
// board. Names are escaped. Nothing is wider than the screen. FOLLOW_UPS_SHOT=<dir> writes screenshots at 1440x900 and
// 390x844.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()+n*864e5).toISOString();
const stages=[{name:'Invited'},{name:'Testing'},{name:'Live'},{name:'Stalled or declined',side:true}];
let pause={scope:'board',at:day(-1),until:null};
const proj=(i,name,stage,follow_up)=>({id:'project:'+i,name,stage,reason:'they replied to the invite',by:'review',at:day(-3),event_id:100+i,first:false,days:3,no_reply_days:0,org:{name,logo:null},follow_up});
const boards=()=>[{id:1,name:'Alpha testers',stages,side:true,visibility:'team',follow_ups:{on:true,next_at:null,pause},projects:[
 proj(1,'Acme <b>pilot</b>','Invited',pause?{state:'paused',n:1,max:3,pause}:{state:'waiting',next_at:day(2),n:1,max:3}),
 proj(2,'Bolt trial','Testing',{state:'open',n:1,max:3,pause})]}];
const settings={on:true,days:3,max_days:7,min:1,max:3,stages:{},channels:null,switch:false,auto:false,stall:null};
const panel=(scope,id)=>scope==='board'?{scope:'board',id:1,name:'Alpha testers',stalled:true,careful:false,channels:['email'],
  stages:[{name:'Invited',open:true},{name:'Testing',open:true},{name:'Live',open:false}],settings,pause}
 :{scope:'project',id:+String(id).replace('project:',''),name:'Acme <b>pilot</b>',own:false,stalled:true,careful:false,channels:['email'],board:{id:1,name:'Alpha testers',on:true},settings,pause};
const detail={id:'project:1',kind:'project',name:'Acme <b>pilot</b>',state:'active',strength:1,last_at:day(-2),signals:3,ids:[],links:[],recent:[],around:[],open:{},
 board:{board:'Alpha testers',stage:'Invited',next:null,visibility:null,board_visibility:'team',stages:['Invited','Testing','Live'],moves:[]},
 get follow_up(){return {on:true,source:'board',next_at:null,state:pause?'paused':'waiting',n:1,max:3,ends:[],activity:[],pause}}};
let calls=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],follow_up_progress:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');res.end(JSON.stringify(n?detail:{projects:[],people:[],quiet:[],new:[],orgs:[],boards:boards()}));return}
 if(req.method==='POST'&&url.pathname==='/api/action'){const c=JSON.parse(body||'{}');calls.push(c);const a=c.args||{};
  if(c.action==='follow_up_pause'){pause=a.paused?{scope:a.scope,at:new Date().toISOString(),until:a.until||null}:null;res.end(JSON.stringify(panel(a.scope,a.id)));return}
  if(c.action==='follow_up_settings'){res.end(JSON.stringify(panel(a.scope,a.id)));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const open=async(width,height)=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));await page.goto(base);
 await page.locator('#suggestions article, #suggestions .all-clear').first().waitFor();return {context,page}};
const toBoard=async page=>{await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());await page.locator('#people-view').waitFor({state:'attached'});
 await page.evaluate(()=>document.querySelector('[data-graph-sub="projects"]').click());await page.locator('#people-view .pboard').first().waitFor()};
const fits=(page,where)=>page.evaluate(()=>({page:document.documentElement.scrollWidth,vw:innerWidth})).then(s=>assert.ok(s.page<=s.vw,`${where}: wider than the screen ${JSON.stringify(s)}`));
const shot=async(page,name,target)=>{if(!process.env.FOLLOW_UPS_SHOT)return;const path=`${process.env.FOLLOW_UPS_SHOT}/${name}.png`;if(target)await target.screenshot({path});else await page.screenshot({path})};
const actions=()=>calls.filter(c=>c.action==='follow_up_pause').map(c=>c.args);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){pause={scope:'board',at:day(-1),until:null};calls=[];
  const {context,page}=await open(width,height);await toBoard(page);
  // The board: "Follow-ups on" and a Paused chip, no next date; the paused tile shows the chip; the open one stays ready
  assert.equal((await page.locator('.board-sub .fu-state').textContent()).trim(),'Follow-ups on');
  assert.equal((await page.locator('.board-sub .fu-chip').textContent()).trim(),'Paused');
  assert.equal((await page.locator('.tile[data-node="project:1"] .tile-fu').textContent()).trim(),'Paused');
  assert.equal((await page.locator('.tile[data-node="project:2"] .tile-fu').textContent()).trim(),'Follow-up ready');
  assert.equal(await page.locator('.tile[data-node="project:1"] b').count(),0);  // the name is text, never markup
  await fits(page,width+' board');await shot(page,`pause-board-${width}`);
  // The board's panel: paused until resumed, Resume applies at once (no Save)
  await page.locator('.board-sub .fu-state').click();const fu=page.locator('#fu-dialog');await fu.locator('[data-fu-resume]').waitFor();
  assert.deepEqual((await fu.locator('.fu-pause > *').allTextContents()).map(x=>x.trim()),['Paused','Until you resume','Resume']);
  await fits(page,width+' panel');await shot(page,`pause-panel-paused-${width}`,fu);
  await fu.locator('[data-fu-resume]').click();await fu.locator('[data-fu-pause]').waitFor();
  assert.deepEqual(actions(),[{scope:'board',id:1,paused:false}]);
  assert.ok(await fu.isVisible());assert.equal(calls.some(c=>c.action==='follow_up_save'),false);
  assert.match(await fu.locator('.fu-pause + .fu-note').textContent(),/^No new follow-ups or sends while paused\. Open to-dos stay\./);
  await shot(page,`pause-panel-running-${width}`,fu);
  // Pause with a day to resume on: sent as that day's start, local time
  const until=new Date(Date.now()+3*864e5),ymd=[until.getFullYear(),String(until.getMonth()+1).padStart(2,'0'),String(until.getDate()).padStart(2,'0')].join('-');
  await fu.locator('[name=fu-until]').fill(ymd);await fu.locator('[data-fu-pause]').click();await fu.locator('[data-fu-resume]').waitFor();
  const sent=actions().at(-1);assert.equal(sent.paused,true);assert.equal(sent.until,new Date(ymd+'T00:00').toISOString());
  assert.match(await fu.locator('.fu-pause-when').textContent(),/^Until \w{3}, \w{3} \d{1,2}$/);
  await page.keyboard.press('Escape');await fu.waitFor({state:'hidden'});
  // A project held by its board's pause: says so, no Resume of its own; its page shows the chip
  pause={scope:'board',at:day(-1),until:null};await page.evaluate(()=>document.querySelector('.tile[data-node="project:1"]').click());await page.locator('.graph-fu').waitFor();
  assert.equal((await page.locator('.graph-fu .fu-chip').textContent()).trim(),'Paused');
  await fits(page,width+' project');await shot(page,`pause-project-${width}`);
  await page.locator('.graph-fu [data-fu-open]').click();await fu.locator('.fu-pause').waitFor();
  assert.equal((await fu.locator('.fu-pause-when').textContent()).trim(),'With its board');
  assert.equal(await fu.locator('[data-fu-resume],[data-fu-pause]').count(),0);
  assert.equal(await fu.locator('.fu-for b').count(),0);
  await shot(page,`pause-panel-project-${width}`,fu);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('follow-up pause dashboard ok');
}finally{await browser?.close();server.close()}
