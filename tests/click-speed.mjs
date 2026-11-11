// The dashboard's most common clicks, timed from the click to the painted frame that shows its answer (vision: "every
// click answers in about 100 ms"). The page runs on made-up data: tests/click-speed-fixture.json, recorded from the
// sandbox (sandbox/run.py --state busy), served back by a small fixture server that answers every call after LATENCY ms,
// as a Machine across the network would. Each run loads a fresh page, then clicks through them all once.
//
//   node tests/click-speed.mjs                         15 runs at 1440x900, and at 390x844 with the CPU 4x slower
//   node tests/click-speed.mjs --runs 21 --only "Do it,Done" --json out.json
//   node tests/click-speed.mjs --record http://127.0.0.1:8870   record the fixture again from a running sandbox
//
// A click's time: from its pointerdown (the event's own timestamp) to the end of the first frame in which its answer
// shows (the open chat, the closed to-do, the dialog, the tab's content...), measured in the page with
// requestAnimationFrame and a task after it. tests/test_click_speed_dashboard.mjs checks them against
// tests/click-speed-baseline.json.
import {createServer} from 'node:http';
import {readFile, writeFile} from 'node:fs/promises';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

export const FIXTURE=new URL('./click-speed-fixture.json',import.meta.url);
export const LATENCY=40;
export const BASELINE=new URL('./click-speed-baseline.json',import.meta.url);
export const SIZES={desk:{width:1440,height:900,throttle:1},phone:{width:390,height:844,throttle:4}};

// What a call is called in the fixture: the path with its query, a status poll without its token, an action by name
const keyOf=(method,url,body)=>{if(url.pathname==='/api/action'){let a='';try{a=JSON.parse(body||'{}').action||''}catch{}return 'action:'+a}
 if(url.pathname==='/api/status')return url.searchParams.has('since')?'status-since':'status';
 return 'get:'+url.pathname+url.search};

// Serves the page, and the fixture's answers (or the sandbox's, while recording: record is its address)
export async function fixtureServer({record=null,latency=LATENCY,source}={}){
 const page=await dashboardPage(source),fixture=record?{now:Date.now(),calls:{}}:JSON.parse(await readFile(FIXTURE,'utf8'));
 const server=createServer(async(req,res)=>{const chunks=[];for await(const c of req)chunks.push(c);const body=Buffer.concat(chunks).toString('utf8');
  const url=new URL(req.url,'http://fixture.invalid');
  if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page);return}
  if(!url.pathname.startsWith('/api/')){res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('');return}
  const key=keyOf(req.method,url,body);let answer;
  if(record){const r=await fetch(record+url.pathname+url.search,{method:req.method,headers:{'Content-Type':req.headers['content-type']||'application/json','X-CSRF-Token':req.headers['x-csrf-token']||''},body:req.method==='POST'?body:undefined});
   answer={status:r.status,type:r.headers.get('content-type')||'application/json',body:await r.text()};
   if(key!=='status-since'&&!(key in fixture.calls)&&r.status===200)fixture.calls[key]=answer}
  else{const since=url.searchParams.get('since');
   // Nothing new since the last poll: the page keeps what it has
   answer=key==='status-since'?{status:200,type:'application/json',body:JSON.stringify({_since:since,_token:since})}
    :fixture.calls[key]||{status:200,type:'application/json',body:'{}'};
   if(key==='action:decide'){const a=JSON.parse(body).args||{};answer={status:200,type:'application/json',body:JSON.stringify({status:{accept:'accepted',complete:'completed',reject:'rejected',snooze:'snoozed',other:'pending'}[a.choice]||'pending',snoozed_until:null})}}}
  await new Promise(r=>setTimeout(r,latency));
  res.statusCode=answer.status;res.setHeader('Content-Type',answer.type);res.end(answer.body)});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 return {url:'http://127.0.0.1:'+server.address().port+'/',fixture,close:()=>new Promise(r=>server.close(r)),save:()=>writeFile(FIXTURE,JSON.stringify(fixture))}}

// In the page: arms the next click. ready is the answer it waits for, checked each frame (requestAnimationFrame). The
// time is the end of the first frame that shows it: its style and layout are done at once there (what that frame's
// paint would do), and when the frame ran long, the browser's own record of it (a long animation frame, which ends
// with its paint) says when it ended. A task queued from that frame could run before the paint's end is seen (a redraw
// the page puts off until after its paint), so no timer marks the end.
export const ARM=ready=>`(()=>{const m=window.__click={t0:null,at:null,frame:null,frames:[]};const ready=${ready};
 addEventListener('pointerdown',e=>{if(m.t0===null)m.t0=e.timeStamp},{capture:true,once:true});
 m.po=new PerformanceObserver(l=>{for(const e of l.getEntries())m.frames.push([e.startTime,e.startTime+e.duration])});m.po.observe({type:'long-animation-frame'});
 const tick=()=>{let ok=false;try{ok=m.t0!==null&&ready()}catch{}
  if(ok){m.frame=performance.now();document.documentElement.getBoundingClientRect();m.at=performance.now();setTimeout(()=>m.done=true,200);return}requestAnimationFrame(tick)};requestAnimationFrame(tick)})()`;
export const TOOK=`(()=>{const m=window.__click;m.po.takeRecords().forEach(e=>m.frames.push([e.startTime,e.startTime+e.duration]));m.po.disconnect();
 const f=m.frames.find(([a,b])=>a<=m.frame&&m.frame<=b);return Math.round(Math.max(m.at,f?f[1]:0)-m.t0)})()`;

const visible=sel=>`(()=>{const e=document.querySelector(${JSON.stringify(sel)});return !!e&&e.getClientRects().length>0})`;
const phone=page=>page.evaluate(()=>!matchMedia('(min-width:1024px)').matches);
// Below 1024px the sidebar is a drawer: open it first (not timed), as a person would
async function side(page){if(await phone(page)&&!await page.evaluate(()=>document.documentElement.dataset.drawer==='open')){
 await page.evaluate(()=>drawerOpen());await page.waitForFunction(()=>!document.querySelector('#app-side')?.getAnimations().length)}}
const calm=page=>page.waitForFunction(()=>!document.querySelector('#app-side')?.getAnimations().length&&!document.querySelector('dialog[open]'));

// The clicks, in the order a run makes them. prep: what comes before (not timed); target: what is clicked; ready: its
// answer. Each to-do clicked is one that has that button, picked in the page (the page's state is the fixture's every
// run). The target is scrolled into view first, and the click comes once the scroll has settled (a tap that ends a
// scroll opens no chat).
const shown=sel=>`[...document.querySelectorAll(${JSON.stringify(sel)})].find(e=>e.getClientRects().length)`;
export const CLICKS=[
 {name:'Open a to-do',prep:async(p,ids)=>{ids.open=await p.evaluate(`${shown('#suggestions article.card a.card-chat-link')}?.closest('article').id.slice(5)`)},
  target:async(p,ids)=>await phone(p)?p.locator(`#task-${ids.open} a.card-chat-link`):p.locator(`#side-cards a[href="#chat=${ids.open}"]`),
  ready:ids=>`()=>!!document.querySelector('.chat-layout[data-chat="${ids.open}"] #chat-input')`},
 {name:'Close it',target:p=>p.locator('.chat-layout [data-chat-back]'),ready:()=>`()=>!document.querySelector('.chat-layout')&&!!${shown('#suggestions article.card')}`},
 {name:'Do it',prep:async(p,ids)=>{ids.doit=await p.evaluate(`${shown('#suggestions article.card .actions button[data-choice=accept]')}?.dataset.id`)},
  target:(p,ids)=>p.locator(`#task-${ids.doit} .actions button[data-choice=accept]:visible`).first(),
  ready:ids=>`()=>{const b=document.querySelector('#task-${ids.doit} .actions button[data-choice=accept]');const t=document.querySelector('#toast');return !b||!b.getClientRects().length||(t&&t.classList.contains('show'))}`},
 {name:'Done',prep:async(p,ids)=>{
   ids.done=await p.evaluate(id=>[...document.querySelectorAll('#suggestions article.card')].find(c=>c.getClientRects().length&&c.querySelector('button[data-choice=complete]')&&c.id.slice(5)!==id)?.id.slice(5),ids.doit);
   const b=p.locator(`#task-${ids.done} button[data-choice=complete]`).first();if(!await b.isVisible()){const m=p.locator(`#task-${ids.done} .more-actions summary`).first();await m.scrollIntoViewIfNeeded();await p.waitForTimeout(400);await m.click()}await b.waitFor({state:'visible'})},
  target:(p,ids)=>p.locator(`#task-${ids.done} button[data-choice=complete]:visible`).first(),
  ready:ids=>`()=>{const c=document.querySelector('#suggestions article#task-${ids.done}');return !c||!c.getClientRects().length}`},
 {name:'Snooze',prep:async(p,ids)=>{ids.snooze=await p.evaluate(`${shown('#suggestions article.card .actions button[data-choice=snooze]')}?.dataset.id`)},
  target:(p,ids)=>p.locator(`#task-${ids.snooze} .actions button[data-choice=snooze]:visible`).first(),ready:()=>`()=>document.querySelector('#snooze-dialog')?.open&&document.querySelector('#snooze-dialog').getClientRects().length>0`,
  after:async p=>{await p.keyboard.press('Escape');await calm(p)}},
 {name:'Work/Personal filter',prep:side,target:p=>p.locator('#side-cards [data-scope="work"]'),
  ready:()=>`()=>document.querySelector('#side-cards [data-scope="work"]')?.getAttribute('aria-pressed')==='true'&&[...document.querySelectorAll('#suggestions article.card')].filter(c=>c.getClientRects().length).every(c=>state.suggestions.find(s=>'task-'+s.id===c.id)?.scope!=='personal')`,
  after:async p=>{await p.evaluate(()=>scopeSet('all'));if(await p.evaluate(()=>document.documentElement.dataset.drawer==='open'))await p.keyboard.press('Escape');await calm(p)}},
 {name:'Search open',target:async p=>p.locator(await phone(p)?'#find-open':'#side-find'),ready:()=>`()=>{const q=document.querySelector('#pal-q');return !!q&&q.closest('dialog')?.open&&document.activeElement===q}`,
  after:async p=>{await p.keyboard.press('Escape');await calm(p)}},
 ...[['Calendar','calendar','#calendar-view .cal-week, #calendar-view .cal-day, #calendar-view article, #calendar-view .cal-grid'],
  ['Graph','people','#people-view article, #people-view .graph-list, #people-view .person-head'],
  ['Routines','routines','#routines-view article, #routines-view .routine, #routines-view section'],
  ['To-dos','inbox','#suggestions article.card']].map(([name,tab,content])=>({name:'Tab '+name,prep:side,target:p=>p.locator(`#app-side nav [data-tab="${tab}"]`),
  ready:()=>`()=>{const s=document.querySelector('#${tab}');return !!s&&!s.hidden&&s.getClientRects().length>0&&[...s.querySelectorAll(${JSON.stringify(content)})].some(e=>e.getClientRects().length)}`,
  after:calm})),
 {name:'Send a chat message',prep:async(p,ids)=>{await p.evaluate(id=>{location.hash='chat='+id},ids.open);await p.locator('#chat-input').waitFor();await p.waitForTimeout(300);
   await p.locator('#chat-input').fill('Can you check the numbers once more?')},
  target:p=>p.locator('[data-chat-send]'),ready:()=>`()=>[...document.querySelectorAll('#chat-log *')].some(e=>e.childElementCount===0&&e.textContent.includes('Can you check the numbers once more?'))`,
  after:async p=>{await p.locator('.chat-layout [data-chat-back]').click();await calm(p)}},
];

// Once the page has scrolled no more for SETTLE ms (a target scrolled into view, also smoothly): at least that, at most
// 2 s. Longer than the page's own wait (a tap within 250 ms of a scroll ends that scroll and opens no chat, see
// dashboard/todos-chat-compose.js), or on a quiet, fast computer the tap on a to-do's Chat link comes too soon after
// the scroll that brought it into view and opens nothing.
export const SETTLE=400;
const settled=page=>page.evaluate(settle=>new Promise(done=>{let last=performance.now();const t0=last,on=()=>{last=performance.now()};
 addEventListener('scroll',on,{capture:true,passive:true});
 const tick=()=>{const now=performance.now();if(now-last>=settle||now-t0>2000){removeEventListener('scroll',on,{capture:true});done()}else requestAnimationFrame(tick)};
 requestAnimationFrame(tick)}),SETTLE);

// One run on a fresh page: each click's time in ms (null when it didn't answer in 10 s)
async function run(context,url,{only,throttle}){
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 const cdp=await context.newCDPSession(page);await cdp.send('Emulation.setCPUThrottlingRate',{rate:throttle});
 await page.goto(url);await page.locator('#suggestions article.card').first().waitFor({timeout:60000});
 await page.waitForLoadState('networkidle');await page.waitForTimeout(1500);
 const out={},ids={};
 for(const c of CLICKS){if(only&&!only.includes(c.name))continue;
  try{await c.prep?.(page,ids);const target=await c.target(page,ids);await target.scrollIntoViewIfNeeded();await settled(page);
   await page.evaluate(ARM(c.ready(ids)));await target.click();
   await page.waitForFunction(()=>window.__click.done,null,{timeout:10000});out[c.name]=await page.evaluate(TOOK)}
  catch(e){out[c.name]=null;errors.push(c.name+': '+e.message.split('\n')[0]);if(process.env.CLICK_SPEED_SHOTS)await page.screenshot({path:process.env.CLICK_SPEED_SHOTS+'/'+c.name.replace(/\W+/g,'-')+'.png'}).catch(()=>{})}
  try{await c.after?.(page)}catch{}await page.waitForTimeout(250)}
 await page.close();return {out,errors}}

// How fast this computer is right now, at a size's CPU speed: a fixed piece of work (build a list of 2,000 rows as markup,
// put it in, lay it out, take it away) on a blank page, the median of 5, in ms. A run's click times are compared with
// the baseline's as measured against this, so a slower or busier computer doesn't read as a slower page.
async function calibrate(context,throttle){const page=await context.newPage();
 const cdp=await context.newCDPSession(page);await cdp.send('Emulation.setCPUThrottlingRate',{rate:throttle});
 await page.setContent('<!doctype html><style>.r{display:flex;gap:8px;padding:4px}.r:nth-child(odd) b{color:#555}</style><body></body>');
 const ms=await page.evaluate(()=>{const a=[];for(let k=0;k<5;k++){const t=performance.now();
  const rows=[];for(let i=0;i<2000;i++)rows.push(`<div class="r"><b>Row ${i}</b><span>${'word '.repeat(i%9+3)}</span><i>${new Date(2026,0,1+i%28).toLocaleDateString('en-US')}</i></div>`);
  const box=document.createElement('div');box.innerHTML=rows.join('');document.body.append(box);box.getBoundingClientRect();getComputedStyle(box.lastChild).color;box.remove();
  a.push(performance.now()-t)}a.sort((x,y)=>x-y);return a[2]});
 await page.close();return ms}

export const median=a=>{const s=a.filter(x=>x!=null).sort((x,y)=>x-y);return s.length?s.length%2?s[(s.length-1)/2]:(s[s.length/2-1]+s[s.length/2])/2:null};

// runs: fresh pages per size; returns {size: {click: [ms...]}}, each size's calibration (ms) and the errors seen. compare: another dashboard.html (a
// checkout's) to time as well, its runs taking turns with this one's (so a busy computer slows both alike), under
// "<size> compare".
export async function measure({runs=15,sizes=Object.keys(SIZES),only=null,latency=LATENCY,record=null,compare=null,log=()=>{}}={}){
 const servers=[await fixtureServer({record,latency})],errors=[];let browser;const times={},calibration={};
 if(compare)servers.push(await fixtureServer({latency,source:compare}));
 try{browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
  for(const size of sizes){const {width,height,throttle}=SIZES[size];
   const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',serviceWorkers:'block'});
   await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
   // The fixture's clock: the page's dates are the recording's, moved to now
   await context.addInitScript(at=>{const D=Date,off=at-D.now();class FixtureDate extends D{constructor(...a){super(...(a.length?a:[D.now()+off]))}static now(){return D.now()+off}}globalThis.Date=FixtureDate},servers[0].fixture.now);
   const speed=[];
   for(let i=0;i<runs;i++){speed.push(await calibrate(context,throttle));for(const [n,srv] of servers.entries()){const key=n?size+' compare':size,r=await run(context,srv.url,{only,throttle});
    errors.push(...r.errors.map(e=>key+': '+e));times[key]??={};
    for(const [k,v] of Object.entries(r.out))(times[key][k]??=[]).push(v);log(key,i+1,JSON.stringify(r.out))}}
   calibration[size]=Math.round(median(speed));log(size,'calibration',calibration[size]);await context.close()}
  if(record)await servers[0].save()}
 finally{await browser?.close();for(const srv of servers)await srv.close()}
 return {times,calibration,errors}}

if(import.meta.url===`file://${process.argv[1]}`){
 const argv=process.argv.slice(2),opt=k=>{const i=argv.indexOf('--'+k);return i<0?null:argv[i+1]};
 const record=opt('record');
 const {times,calibration,errors}=await measure({runs:+(opt('runs')||(record?1:15)),only:opt('only')?.split(','),record:record?.replace(/\/$/,''),sizes:opt('sizes')?.split(','),compare:opt('compare'),log:(...a)=>console.error(...a)});
 const names=[...new Set(Object.values(times).flatMap(t=>Object.keys(t)))];
 console.log('click'.padEnd(24)+Object.keys(times).map(s=>(s+' median').padStart(14)+'  p90').join(''));
 for(const n of names)console.log(n.padEnd(24)+Object.keys(times).map(s=>{const a=times[s][n]||[],q=[...a].filter(x=>x!=null).sort((x,y)=>x-y);
  return String(median(a)??'-').padStart(14)+String(q.length?q[Math.min(q.length-1,Math.floor(q.length*.9))]:'-').padStart(6)}).join(''));
 if(errors.length)console.log('errors:\n '+[...new Set(errors)].join('\n '));
 if(opt('json'))await writeFile(opt('json'),JSON.stringify({times,calibration}));
 // --baseline: these medians become tests/click-speed-baseline.json (after a change that makes a click faster or slower on purpose)
 if(argv.includes('--baseline'))await writeFile(BASELINE,JSON.stringify(Object.fromEntries(Object.entries(calibration).map(([size,c])=>[size,{calibration:c,clicks:Object.fromEntries(Object.entries(times[size]).map(([k,v])=>[k,median(v)]))}])),null,1)+'\n')}
