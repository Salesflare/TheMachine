import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Offline and on a spotty link (a plane's wifi): the app opens with the last to-dos, chat and Calendar from the device,
// a banner says it is offline and since when, the owner's own decisions (Not needed, Snooze, Mark done, a chat
// message) wait on the device with Cancel and go by themselves, in order and once each, when the Machine answers
// again (also through 5xx hiccups), a typed chat message survives a reload, and Send to other people never waits:
// it says it is offline. docs/architecture.md, "On the device".
const raw=await readFile(new URL('../dashboard.html',import.meta.url),'utf8'),sw=await readFile(new URL('../sw.js',import.meta.url),'utf8');
// The brand files as assistant.py serves them (BRAND_ASSETS), so offline must look the same as online
const py=await readFile(new URL('../assistant.py',import.meta.url),'utf8');
const BRAND=Object.fromEntries([...py.slice(py.indexOf('BRAND_ASSETS = {'),py.indexOf('}',py.indexOf('BRAND_ASSETS = {'))).matchAll(/'\/brand\/([\w.-]+)': ROOT \/ '([\w./-]+)'/g)].map(m=>[m[1],m[2]]));
const swBrand=JSON.parse(/const BRAND = (\[[^\]]*\])/.exec(sw)[1].replace(/'/g,'"'));
assert.deepEqual([...swBrand].sort(),Object.keys(BRAND).sort(),'sw.js keeps every brand file assistant.py serves');
const CSRF='c'.repeat(64),SCOPE='a1'.repeat(16),now=new Date(),iso=now.toISOString();
const A='1'.repeat(16),B='2'.repeat(16),C='3'.repeat(16);
const card=(id,title)=>({id,title,body:'Robin asked for the numbers.',status:'pending',scope:'work',created_at:iso,event_ids:[1]});
const cards=[card(A,'Reply to Robin about the plan'),card(B,'Book the venue'),card(C,'Send the slides')];
const shots=process.env.SHOTS||'';
const page=()=>raw.replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__',SCOPE);
const status=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[{service:'calendar',account_id:'cal',status:'ok'}],fleet:{on:false},ui_version:'v1'});
const meetingAt=new Date(now);meetingAt.setHours(15,0,0,0);
let mode='ok',flaky=0;const decided=new Map(),order=[],posts=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page());return}
 if(url.pathname==='/sw.js'){res.setHeader('Content-Type','text/javascript');res.end(sw);return}
 if(mode==='down'&&url.pathname.startsWith('/api/')){res.statusCode=502;res.end('{"error":"down"}');return}
 if(mode==='restarting'&&url.pathname.startsWith('/api/')){res.statusCode=503;res.setHeader('Retry-After','2');res.end('{"error":"restarting","restarting":true}');return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:CSRF,cache_scope:SCOPE}));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/calendar'){res.end(JSON.stringify({calendars:[{id:'cal',name:'Work'}],meetings:[{id:'m1',title:'Plan review with Robin',start:meetingAt.toISOString(),end:new Date(+meetingAt+36e5).toISOString(),account_id:'cal'}]}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');posts.push({action:r.action,csrf:req.headers['x-csrf-token'],args:r.args});
  // A spotty link: the answer is lost on the way back after the Machine saved it, so the same change comes again
  if(r.action==='decide'){const id=r.args.decision_id;if(!decided.has(id)){decided.set(id,r.args);order.push(r.args.choice+':'+r.args.suggestion_id)}
   if(flaky>0){flaky--;res.statusCode=502;res.end('{}');return}res.end(JSON.stringify({status:'ok',duplicate:false}));return}
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k1',items:[{kind:'reply',text:'Drafted the numbers for Robin.',at:Date.now()}]}));return}
  res.end('{}');return}
 const brand=url.pathname.startsWith('/brand/')&&BRAND[url.pathname.slice(7)];
 if(brand){res.setHeader('Content-Type',brand.endsWith('.woff2')?'font/woff2':brand.endsWith('.webp')?'image/webp':'image/png');res.setHeader('Cache-Control','no-cache');res.end(await readFile(new URL('../'+brand,import.meta.url)));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const until=async(p,fn,arg,label,timeout=15000)=>{try{await p.waitForFunction(fn,arg,{timeout})}catch{throw Error('timed out: '+label)}};
// waitForFunction takes a promise as true at once: an async check is polled here
const poll=async(p,fn,arg,label,timeout=15000)=>{const end=Date.now()+timeout;while(Date.now()<end){if(await p.evaluate(fn,arg).catch(()=>false))return;await p.waitForTimeout(100)}throw Error('timed out: '+label)};
// Every image on the page drew (none broken), and the sidebar's line says offline like the bar
const imagesOk=p=>p.evaluate(()=>[...document.images].filter(i=>i.isConnected&&i.getAttribute('src')&&i.offsetParent&&!(i.complete&&i.naturalWidth>0)).map(i=>i.getAttribute('src')));
const bar=p=>p.evaluate(()=>{const b=document.querySelector('#offline-bar');return b.hidden||!b.offsetParent?'':b.innerText.replace(/\s+/g,' ').trim()});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const tab=await context.newPage();tab.on('pageerror',e=>errors.push(e.message));

 // 1. Online: the cards, a chat and this week's Calendar are read once and kept on the device
 await tab.goto(base);await tab.locator('#suggestions article[id]').first().waitFor();
 assert.equal(await bar(tab),'','no banner while online');
 await tab.evaluate(()=>navigator.serviceWorker.ready);
 await tab.evaluate(()=>document.querySelector('nav [data-tab="calendar"]').click());
 await tab.locator('#calendar',{hasText:'Plan review with Robin'}).first().waitFor();
 await poll(tab,async()=>!!(await localCache.read('cal:'+localDay(calMonday(new Date())))),null,'the week is kept');
 await tab.goto(base+'#chat='+'1'.repeat(16));await tab.locator('#chat-log',{hasText:'Drafted the numbers for Robin.'}).waitFor();
 await poll(tab,async()=>!!(await localCache.read('chat:'+'1'.repeat(16)))&&!!(await localCache.read('status')),null,'chat and cards kept');
 await until(tab,()=>!!navigator.serviceWorker.controller,null,'the service worker controls the page');

 // 2. A typed chat message survives a reload (kept encrypted on the device, never in plain storage)
 await tab.fill('#chat-input','Use the Q3 numbers, not Q2');
 await poll(tab,async()=>(await localCache.read('chat-drafts'))?.value?.[location.hash.slice(6)]==='Use the Q3 numbers, not Q2',null,'the draft is kept');
 assert.ok(!JSON.stringify(await tab.evaluate(()=>({...localStorage,...sessionStorage}))).includes('Q3 numbers'),'never in plain storage');
 await tab.reload();await tab.locator('#chat-log',{hasText:'Drafted the numbers for Robin.'}).waitFor();
 await until(tab,()=>document.querySelector('#chat-input')?.value==='Use the Q3 numbers, not Q2',null,'the draft is back after a reload');

 // 3. The plane's wifi drops: the app reopens from the device, the banner says so and since when
 await context.setOffline(true);await tab.reload();
 await tab.locator('#chat-log',{hasText:'Drafted the numbers for Robin.'}).waitFor();
 await until(tab,()=>{const b=document.querySelector('#offline-bar');return !b.hidden&&/^Offline\. Showing what was here at \d\d:\d\d\./.test(b.textContent)},null,'the offline banner');
 assert.equal(await tab.evaluate(()=>document.querySelector('#chat-input').value),'Use the Q3 numbers, not Q2','the draft is there offline too');
 assert.deepEqual(await imagesOk(tab),[],'offline, every image comes from the device');

 // 4. A chat message sent offline waits, marked, and the box is free again; nothing reached the Machine
 const before=posts.length;
 await tab.click('[data-chat-send]');
 await tab.locator('#chat-log .outbox-msg',{hasText:'Use the Q3 numbers, not Q2'}).waitFor();
 assert.match(await tab.locator('#chat-log .outbox-msg').innerText(),/Sends when you’re back online/);
 assert.equal(await tab.evaluate(()=>document.querySelector('#chat-input').value),'','the box is empty for the next message');
 assert.match(await bar(tab),/1 change waits to send\./);
 if(shots){await tab.screenshot({path:`${shots}/offline-chat-1440.png`})}

 // 5. To-dos: Not needed and Snooze offline wait on their to-do with Cancel; Cancel takes one back
 await tab.goto(base+'#');await tab.evaluate(()=>{history.replaceState(null,'',location.pathname);openChatLink()});
 await tab.locator(`#task-${B}`).waitFor();
 await tab.evaluate(id=>document.querySelector(`#task-${id} [data-choice="reject"]`).click(),B);
 await tab.locator(`#task-${B} [data-choice="dismiss-typed"]`).click();
 await tab.locator(`#task-${B} .outbox-wait`,{hasText:'Not needed saves when you’re back online.'}).waitFor();
 await tab.evaluate(id=>saveDecision(id,'complete'),C);
 await tab.locator(`#task-${C} .outbox-wait`,{hasText:'Done saves when you’re back online.'}).waitFor();
 assert.match(await bar(tab),/3 changes wait to send\./);
 assert.match(await tab.locator('#updated').innerText(),/^Offline · updated \d\d:\d\d$/,'the sidebar says offline too, after the to-dos redrew');
 assert.ok(await tab.locator('#live.stale').count(),'with the bar\'s dot');
 assert.equal(await tab.locator('#toast.show').count(),0,'the line on the to-do says it; no toast over the bar');
 assert.deepEqual(await imagesOk(tab),[]);
 if(shots){await tab.screenshot({path:`${shots}/offline-todos-1440.png`})}
 await tab.locator(`#task-${C} [data-outbox-cancel]`).click();
 await until(tab,id=>!document.querySelector(`#task-${id} .outbox-wait`),C,'Cancel takes it back');
 assert.match(await bar(tab),/2 changes wait to send\./);
 assert.equal(posts.length,before,'nothing went while offline');
 // Waiting changes survive a reload (kept encrypted with the rest)
 await tab.reload();await tab.locator(`#task-${B} .outbox-wait`).waitFor();
 assert.match(await bar(tab),/2 changes wait to send\./);

 // 6. Calendar offline: this week's meetings from the device, not "couldn't load"
 await tab.evaluate(()=>document.querySelector('nav [data-tab="calendar"]').click());
 await tab.locator('#calendar',{hasText:'Plan review with Robin'}).first().waitFor();
 assert.ok(!/Meetings couldn’t load/.test(await tab.locator('#calendar').innerText()));
 await tab.evaluate(()=>document.querySelector('nav [data-tab="inbox"]').click());

 // 7. Send to other people never waits: it says it is offline, and nothing is queued
 await tab.evaluate(()=>{sendTask='1'.repeat(16);sendRevision='r1';sendDraft={kind:'linkedin',body:'Hi'};$('#send-editor').hidden=true;$('#send-recipients').hidden=true;$('#send-dialog').showModal()});
 await tab.click('#send-confirm');
 await until(tab,()=>/^Offline\. Send again when you’re back online\.$/.test(document.querySelector('#send-error').textContent),null,'Send says offline');
 assert.equal(await tab.evaluate(()=>outbox.items.length),2,'a send is never queued');
 await tab.evaluate(()=>$('#send-dialog').close());

 // 8. Back, but spotty: the first answers are lost (502). The changes go again by themselves with the same ids, in the
 // order they were made, and each is saved once; then the banner goes
 flaky=2;await context.setOffline(false);
 await until(tab,()=>outbox.items.length===0,null,'the waiting changes went',30000);
 assert.deepEqual(order,['other:'+A,'reject:'+B],'in order, once each');
 const ids=posts.filter(p=>p.action==='decide').map(p=>p.args.decision_id);
 assert.ok(ids.length>new Set(ids).size,'sent again after a lost answer, with the same decision_id');
 assert.ok(posts.filter(p=>p.action==='decide').every(p=>p.csrf===CSRF),'with the CSRF token');
 assert.equal(decided.get(ids.find(i=>i.startsWith('chat-'))).feedback,'Use the Q3 numbers, not Q2');
 await until(tab,()=>document.querySelector('#offline-bar').hidden,null,'the banner goes once live again');
 await until(tab,()=>/^Updated \d\d:\d\d$/.test(document.querySelector('#updated').innerText)&&!document.querySelector('#live.stale'),null,'the sidebar is live again');

 // 9. The Machine restarting: the banner says that, and a change waits for it
 mode='restarting';await tab.evaluate(()=>refresh());
 assert.match(await bar(tab),/^Your Machine is restarting\./);
 await tab.evaluate(id=>saveDecision(id,'complete'),C);
 assert.match(await bar(tab),/1 change waits to send\./);
 mode='ok';await tab.evaluate(()=>refresh());
 await until(tab,()=>outbox.items.length===0&&document.querySelector('#offline-bar').hidden,null,'sent after the restart',30000);
 assert.equal(order.at(-1),'complete:'+C);

 // 10. Phone and desktop, light and dark, really offline (the page from the device): every image there, the banner fits,
 // the waiting line keeps Cancel beside its words, nothing covers the banner
 for(const [w,h,scheme] of [[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]){const ctx=await browser.newContext({viewport:{width:w,height:h},isMobile:w<600,hasTouch:w<600,colorScheme:scheme});
  await ctx.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const p=await ctx.newPage();p.on('pageerror',e=>errors.push(e.message));await p.goto(base);await p.locator('#suggestions article[id]').first().waitFor();
  await poll(p,async()=>!!(await localCache.read('status')),null,'kept');
  await p.evaluate(()=>navigator.serviceWorker.ready);await poll(p,async()=>(await (await caches.open('tm-assets-1')).keys()).length>=16,null,'the brand files are kept up front');
  await p.reload();await until(p,()=>!!navigator.serviceWorker.controller,null,'controlled');await poll(p,async()=>!!(await (await caches.open('tm-shell-2')).match(location.origin+'/')),null,'the page is kept');
  await ctx.setOffline(true);await p.reload();await p.locator('#suggestions article[id]').first().waitFor();
  await until(p,()=>!document.querySelector('#offline-bar').hidden,null,'banner');
  await p.evaluate(id=>document.querySelector(`#task-${id} [data-choice="reject"]`).click(),B);await p.locator(`#task-${B} [data-choice="dismiss-typed"]`).click();
  await p.locator(`#task-${B} .outbox-wait`).waitFor();await p.waitForTimeout(300);
  const m=await p.evaluate(id=>{const line=document.querySelector(`#task-${id} .outbox-wait`),c=line.querySelector('button').getBoundingClientRect(),words=line.querySelector('.nowrap').getClientRects(),last=words[words.length-1],b=document.querySelector('#offline-bar').getBoundingClientRect(),
   toast=document.querySelector('#toast.show')?.getBoundingClientRect();
   return {scroll:document.documentElement.scrollWidth,width:innerWidth,bar:b.width,cancelBeside:Math.abs(c.top-[...line.querySelector('span').getClientRects()].at(-1).top)<8&&[...line.querySelector('span').getClientRects()].at(-1).left<c.left-20,covered:!!toast&&toast.top<b.bottom&&toast.bottom>b.top}},B);
  assert.ok(m.scroll<=m.width,`${w}: no sideways scroll ${JSON.stringify(m)}`);assert.ok(m.bar>0&&m.bar<=w);
  assert.ok(m.cancelBeside,`${w}: Cancel stays beside the words ${JSON.stringify(m)}`);assert.ok(!m.covered,`${w}: nothing covers the banner`);
  assert.deepEqual(await imagesOk(p),[],`${w} ${scheme}: no broken image offline`);
  if(!(w<1024))assert.match(await p.locator('#updated').innerText(),/^Offline · updated \d\d:\d\d$/);
  if(shots)await p.screenshot({path:`${shots}/offline-${w}-${scheme}.png`});
  await p.evaluate(()=>{for(const x of [...outbox.items])outboxCancel(x.id)});await ctx.close()}

 assert.deepEqual(errors,[]);
 console.log('offline dashboard ok');
}finally{await browser?.close();server.close()}
