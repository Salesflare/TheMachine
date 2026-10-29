import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A meeting's notes and transcript that fail to load (The Machine restarting) load again by themselves: 2, 4, 8 and
// 16 s later, and at once when the window gets the focus or the network is back. Only after that the dialog says it
// couldn't load, with Try again. Once loaded, Generate notes is back. RETRY_SHOT=<dir> writes the failed dialog at
// 1440x900 and 390x844 in light and dark.
process.env.TZ='Europe/Brussels';
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const brand={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'};
const at=(h,m=0)=>{const d=new Date();d.setHours(h,m,0,0);return d.toISOString()},now=new Date().toISOString();
const meetings=[{id:204,account_id:'cal',title:'Quarterly planning',start:at(13),end:at(15,15),all_day:false,location:'Room 4',guests:2,url:null,transcript:{by:'owner',at:now,chars:60}}];
const notes={notes:null,transcript:{id:40,text:'Robin: Let’s plan the quarter.\nAlex: Agreed.',by:'owner',at:now,chars:60,next_offset:null,minutes:45},zoom:null,google_meet:null,writing:null};
let failing=0,reads=0;  // failing: how many reads fail from now on (Infinity: all)
const state=()=>({suggestions:[],promises:[],connectors:[{id:'cal',email:'owner@example.com',service:'calendar',status:'ok'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(brand[url.pathname]){res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+brand[url.pathname],import.meta.url)));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/calendar'){res.end(JSON.stringify({meetings}));return}
 if(url.pathname==='/api/meeting-notes'){reads++;if(failing>0){failing--;res.statusCode=500;res.end('{"error":"Something went wrong."}');return}
  const m=meetings[0];res.end(JSON.stringify({event_id:m.id,title:m.title,start:m.start,end:m.end,...notes}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const until=async(fn,label,ms=8000)=>{const t=Date.now();while(!(await fn())){if(Date.now()-t>ms)throw Error('timed out: '+label);await new Promise(r=>setTimeout(r,50))}};
const open=async(width,height,scheme='light')=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));await page.clock.install();
 await page.goto(base);await page.evaluate(()=>showTab('calendar'));await page.waitForFunction(()=>calMeetings!==null&&![...calWeeks.values()].some(w=>w.loading));return {context,page}};
const view=page=>page.evaluate(()=>calView(calMeetings.find(m=>m.id===204)));
const shown=(page,sel)=>page.locator(sel).isVisible();
const idle=page=>until(()=>page.evaluate(()=>!calNote?.loading),'the read is back');
// The next try: the timer runs, then its read comes back
const step=async(page,ms)=>{const r=reads;await page.clock.runFor(ms);await until(()=>reads>r,'tried again');await idle(page)};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 {const {context,page}=await open(1440,900);
  // 1. Two failed reads, then it loads: the failure is never shown, and Generate notes is there
  failing=2;reads=0;await view(page);await until(()=>reads>=1,'first read');await idle(page);
  assert.ok(!await shown(page,'#cal-v-tr-none'),'no failure line while it tries again');
  await step(page,2000);assert.ok(!await page.evaluate(()=>!!calNote.data));
  await step(page,4000);await until(()=>page.evaluate(()=>!!calNote.data),'loaded on the third read');
  assert.equal(reads,3);assert.ok(await shown(page,'#cal-v-notes-gen'),'Generate notes is back');
  assert.ok(!await shown(page,'[data-cal-notes-retry]'));
  await page.evaluate(()=>$('#cal-view').close());

  // 2. Every read fails: four more tries (2, 4, 8, 16 s), then the line with Try again; no more tries after that
  failing=Infinity;reads=0;await view(page);await until(()=>reads>=1,'first read');await idle(page);
  for(const ms of [2000,4000,8000,16000])await step(page,ms);
  assert.equal(reads,5,'one read and four tries');
  await until(()=>shown(page,'#cal-v-tr-none'),'the failure shows');
  assert.match(await page.locator('#cal-v-tr-none').innerText(),/^The transcript couldn’t load\. Try again$/);
  assert.ok(!await shown(page,'#cal-v-notes-gen'),'no Generate notes without the data');
  await page.clock.runFor(60e3);assert.equal(reads,5,'it stops trying by itself');
  if(process.env.RETRY_SHOT)await page.locator('#cal-view').screenshot({path:process.env.RETRY_SHOT+'/retry-failed-1440x900-light.png'});
  // Try again: it loads
  failing=0;await page.locator('#cal-v-tr-none [data-cal-notes-retry]').click();
  await until(()=>page.evaluate(()=>!!calNote.data),'Try again loads it');
  assert.ok(await shown(page,'#cal-v-notes-gen'));assert.ok(!await shown(page,'#cal-v-tr-none'));
  await page.evaluate(()=>$('#cal-view').close());

  // 3. Failed, then the window gets the focus again: it loads at once
  failing=5;reads=0;await view(page);await until(()=>reads>=1,'first read');await idle(page);for(const ms of [2000,4000,8000,16000])await step(page,ms);
  await until(()=>shown(page,'#cal-v-tr-none'),'failed');failing=0;
  await page.evaluate(()=>dispatchEvent(new Event('focus')));await until(()=>page.evaluate(()=>!!calNote.data),'focus loads it');
  await page.evaluate(()=>$('#cal-view').close());

  // 4. Waiting for the next try, the network comes back: it loads at once
  failing=1;reads=0;await view(page);await until(()=>reads>=1,'first read');await idle(page);
  await page.evaluate(()=>dispatchEvent(new Event('online')));await until(()=>page.evaluate(()=>!!calNote.data),'online loads it');
  assert.equal(reads,2);
  // closed: nothing tries any more
  failing=Infinity;await page.evaluate(()=>$('#cal-view').close());await view(page);await until(()=>reads>=3,'read');await idle(page);await page.evaluate(()=>$('#cal-view').close());
  const r=reads;await page.clock.runFor(60e3);assert.equal(reads,r,'a closed dialog does not try again');
  await context.close()}
 if(process.env.RETRY_SHOT)for(const [w,h,scheme] of [[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]){const {context,page}=await open(w,h,scheme);
  failing=Infinity;reads=0;await view(page);await until(()=>reads>=1,'read');await idle(page);for(const ms of [2000,4000,8000,16000])await step(page,ms);
  await until(()=>shown(page,'#cal-v-tr-none'),'failed');await page.screenshot({path:`${process.env.RETRY_SHOT}/retry-failed-${w}x${h}-${scheme}.png`});await context.close()}
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({page_errors:errors}));
}finally{await browser?.close();server.close()}
