// One to-do on its own (?compact=1#card=<id>, dashboard/todos-compact.js), for a small window another app frames: only
// that to-do, with the dashboard's own buttons, Send check and Snooze picker; what leads out opens the whole dashboard in
// a new window; Escape closes what is open here and is otherwise left to the app; the page's title says how the to-do
// stands; nothing of it reaches the whole dashboard. Also as the Machine serves it, with its part in a file of its own.
// Synthetic data, a local fixture server, nothing sent. SHOTS=<folder> saves screenshots.
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {fileURLToPath} from 'node:url';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

const at=html=>html.replaceAll('__BASE__','/').replaceAll('__CSRF__','').replaceAll('__UI_VERSION__','v1').replaceAll('__CACHE_SCOPE__','');
const whole=at(await dashboardPage()),sw=await readFile(new URL('../sw.js',import.meta.url),'utf8');
// As served: the first load, and each group's part in a file (dashboard_parts.assemble_split)
const [first,parts]=JSON.parse(execFileSync('python3',['-c','import sys,json;sys.path.insert(0,sys.argv[1]);import dashboard_parts as d;'+
 'print(json.dumps(d.assemble_split()))',fileURLToPath(new URL('..',import.meta.url))],{encoding:'utf8',maxBuffer:1<<26}));
const MAIL='1234567890abcdef',ASK='0011223344556677',DONE='8899aabbccddeeff',GONE='ffffffffffffffff',rev='1234567890ab',now=new Date().toISOString();
const reply={kind:'email',label:'Send reply',revision:rev,account_id:'mail',from:'sam@acme.example',to:['casey@partner.example'],cc:[],bcc:[],subject:'Re: Pricing',
 body:'Hi Casey,\n\nThe price is the same for 25 seats.\n\nSam',signature:false,thread_id:'abc123',in_reply_to:'<m1@partner.example>'};
const base={scope:'work',created_at:now,event_ids:[1]};
let list;
const reset=()=>{list=[{...base,id:MAIL,title:'Reply to Casey about pricing',body:'Drafted the reply.',status:'prepared',next_action:reply,next_actions:[reply],
   outcome:JSON.stringify({state:'needs_you',needs:'Check the reply and send it'})},
  {...base,id:ASK,title:'Tell Robin about Saturday',body:'Robin asked.',status:'pending'},
  {...base,id:DONE,title:'Book the venue',body:'Booked.',status:'completed',completed_at:now,updated_at:now}]};
const posts=[],errors=[];let mode='ok',served=whole;
const status=()=>({suggestions:list,connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:false},
 whats_new:{id:'x',items:[{id:'a',title:'Something new',text:'It is new.'}]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(served);return}
 const lazy=url.pathname.match(/^\/lazy-(\w+)\.js$/);
 if(lazy){if(mode==='nopart'&&lazy[1]==='compact'){res.statusCode=404;res.end();return}res.setHeader('Content-Type','text/javascript');res.end(parts[lazy[1]]||'');return}
 if(url.pathname.startsWith('/api/')&&mode==='down'){res.statusCode=502;res.end('{}');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:'',compact:1}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');if(r.action!=='client_error')posts.push(r);
  if(r.action==='decide'){const s=list.find(x=>x.id===r.args.suggestion_id);if(r.args.choice==='complete')Object.assign(s,{status:'completed',completed_at:now});
   if(r.args.choice==='snooze')Object.assign(s,{status:'snoozed',snoozed_until:r.args.until||r.args.snoozed_until||new Date(Date.now()+864e5).toISOString()});
   res.end(JSON.stringify({decision_id:'d1',id:'d1',status:s.status}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/api/')?200:404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const home='http://127.0.0.1:'+server.address().port+'/',one=id=>home+'?compact=1#card='+id;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
let browser;
const titled=(p,want)=>p.waitForFunction(w=>document.title===w,want,{timeout:15000}).catch(async()=>{throw Error('title: wanted '+want+', is '+await p.title())});
async function open(address,{width=340,height=620,dark=false}={}){
 const context=await browser.newContext({viewport:{width,height},colorScheme:dark?'dark':'light',locale:'en-GB',serviceWorkers:'block'}),page=await context.newPage();
 await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await context.addInitScript(()=>{window.__badge=0;navigator.setAppBadge=navigator.clearAppBadge=async()=>{__badge++};window.__keys=[];addEventListener('keydown',e=>setTimeout(()=>__keys.push(e.key+' '+e.defaultPrevented)),true)});
 await page.goto(address);return page}
const shown=page=>page.evaluate(()=>[...document.querySelectorAll('.topbar,.app-side,.site-footer,#update-float,main>*,#inbox>*')].filter(x=>x.id!=='toast'&&x.checkVisibility()&&x.offsetHeight).map(x=>x.id||x.className));
const newWindow=async(page,go)=>{const [w]=await Promise.all([page.context().waitForEvent('page',{timeout:10000}),go()]);await w.waitForURL(/./);const u=w.url();await w.close();return u};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});

 // 1. Only that to-do, at every width of the window, light and dark; its background is opaque and one color
 for(const [width,dark] of [[300,false],[340,true],[400,false],[480,true]]){reset();
  const page=await open(one(MAIL),{width,dark});await titled(page,'open: Reply to Casey about pricing');
  assert.deepEqual(await shown(page),['inbox','suggestions'],'nothing but the to-do');
  assert.equal(await page.locator('#suggestions article[id]').count(),1);
  assert.ok(await page.locator('#suggestions').innerText().then(x=>/The price is the same for 25 seats/.test(x)),'with its draft');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'fits at '+width);
  assert.equal(await page.evaluate(()=>getComputedStyle(document.body).backgroundColor),dark?'rgb(35, 36, 40)':'rgb(255, 255, 255)');
  assert.equal(await page.evaluate(()=>document.querySelectorAll('dialog[open]').length),0,'no What’s new, no tour');
  assert.equal(await page.evaluate(()=>__badge),0,'the app’s badge is the whole dashboard’s');
  if(shots)await page.screenshot({path:`${shots}/compact-${width}-${dark?'dark':'light'}.png`});
  await page.context().close()}

 // 2. The Send check is the dashboard's own: nothing goes out before Send now; Escape closes it and is not the app's then
 reset();posts.length=0;let page=await open(one(MAIL));await titled(page,'open: Reply to Casey about pricing');
 await page.locator(`#task-${MAIL} [data-smart="${rev}"]`).click();await page.locator('#send-dialog').waitFor({state:'visible'});
 assert.ok(await page.evaluate(()=>document.querySelector('#send-dialog').getBoundingClientRect().right<=innerWidth));
 assert.deepEqual(posts.filter(p=>p.action==='confirm_action'),[]);
 await page.keyboard.press('Escape');await page.locator('#send-dialog').waitFor({state:'hidden'});
 await page.waitForFunction(()=>__keys.length);assert.equal(await page.evaluate(()=>__keys.at(-1)),'Escape true');
 await page.evaluate(()=>document.activeElement.blur());
 await page.keyboard.press('Escape');await page.waitForFunction(()=>__keys.length>1);assert.equal(await page.evaluate(()=>__keys.at(-1)),'Escape false','nothing open: left to the app');
 assert.deepEqual(posts.filter(p=>p.action==='confirm_action'),[]);
 // a menu too
 await page.locator(`#task-${MAIL} .more-actions summary`).click();await page.keyboard.press('Escape');
 await page.waitForFunction(()=>!document.querySelector('.more-actions[open]')&&__keys.at(-1)==='Escape true');
 // the whole dashboard's keys do nothing here
 for(const k of ['/','?','n','t','Control+k'])await page.keyboard.press(k);
 assert.equal(await page.evaluate(()=>document.querySelectorAll('dialog[open]').length),0);

 // 3. What leads out opens the whole dashboard in a new window, without compact; the to-do stays
 assert.equal(await newWindow(page,()=>page.evaluate(()=>showSettings('general'))),home+'#settings/general');
 assert.ok((await newWindow(page,()=>page.evaluate(()=>{location.hash='#calendar'}))).startsWith(home+'#calendar'));
 assert.equal(await newWindow(page,()=>page.evaluate(id=>chatGo(id),ASK)),home+'#chat='+ASK);
 assert.equal(await newWindow(page,async()=>{await page.evaluate(()=>{const a=document.createElement('a');a.href='#graph/org%3A1';a.textContent='Org';document.querySelector('#suggestions article').append(a);a.click()})}),home+'#graph/org%3A1');
 assert.equal(page.url(),one(MAIL));assert.equal(await page.locator('#task-'+MAIL).count(),1);

 // 4. Another to-do by its address, in the same page; reload and its chat keep the mode
 await page.evaluate(id=>{location.hash='#card='+id},ASK);await titled(page,'open: Tell Robin about Saturday');
 await page.reload();await titled(page,'open: Tell Robin about Saturday');assert.deepEqual(await shown(page),['inbox','suggestions']);
 await page.evaluate(id=>{location.hash='#chat='+id},ASK);await page.waitForFunction(()=>document.body.classList.contains('chat-open'));
 await page.reload();await page.waitForFunction(()=>document.body.classList.contains('chat-open'));await titled(page,'open: Tell Robin about Saturday');
 assert.equal(await page.evaluate(()=>self.COMPACT),'compact');
 await page.evaluate(id=>{location.hash='#card='+id},ASK);await page.waitForFunction(()=>!document.body.classList.contains('chat-open'));

 // 5. How it ends: done, snoozed, not here anymore
 await page.locator(`#task-${ASK} [data-choice="complete"]`).first().evaluate(b=>b.click());await titled(page,'done: Tell Robin about Saturday');
 for(let i=0;i<200&&!posts.some(p=>p.action==='decide');i++)await page.waitForTimeout(25);
 assert.equal(posts.filter(p=>p.action==='decide').length,1);await page.locator('#toast [data-undo]').waitFor();
 await page.context().close();
 reset();page=await open(one(DONE));await titled(page,'done: Book the venue');await page.context().close();
 reset();list[1].status='snoozed';list[1].snoozed_until=new Date(Date.now()+864e5).toISOString();page=await open(one(ASK));await titled(page,'snoozed: Tell Robin about Saturday');await page.context().close();
 reset();page=await open(one(GONE));await titled(page,'gone:');assert.equal((await page.locator('#suggestions').innerText()).trim(),'That to-do isn’t here anymore.');await page.context().close();
 // Not reachable, then back; signed out: one line
 reset();mode='down';page=await open(one(MAIL));await titled(page,'offline:');mode='ok';await page.evaluate(()=>refresh());await titled(page,'open: Reply to Casey about pricing');
 await page.evaluate(()=>cacheGone('out'));await page.waitForFunction(()=>/^signed-out:/.test(document.title));
 assert.equal((await page.locator('#suggestions').innerText()).trim(),'Signed out. Sign in again to see your Machine.');

 // 6. The whole dashboard is as ever, also in the same browser after it
 assert.deepEqual(await page.evaluate(()=>Object.keys(localStorage).filter(k=>/^skeleton|scope|view|side/.test(k))),[],'no kept shape or view');
 for(const address of [home,home+'#card='+MAIL,home+'?compact=0#card='+MAIL]){await page.goto('about:blank');await page.goto(address);await page.locator('#suggestions article[id]').nth(1).waitFor();
  assert.equal(await page.evaluate(()=>[self.COMPACT,document.documentElement.matches('.compact,.one-todo'),document.querySelector('base')?.target||''].join()),',false,');assert.ok(!/^open:/.test(await page.title()))}
 // Never in a frame (the site's demo runs in one)
 await page.goto('about:blank');await page.goto(home);await page.evaluate(u=>{const f=document.createElement('iframe');f.id='f';f.src=u;document.body.append(f)},one(MAIL));
 await page.frameLocator('#f').locator('#suggestions article[id]').nth(1).waitFor({state:'attached'});
 assert.equal(await page.frames()[1].evaluate(()=>!!self.COMPACT),false);
 await page.context().close();

 // 7. As served: its part is a file of its own, fetched at once and only here; nothing of the whole page shows before it;
 // without it, the page says it didn't load
 assert.ok(!first.includes('function oneDraw('),'not in the first load');assert.ok(parts.compact.includes('function oneDraw('));
 {const cut=first.lastIndexOf('<script>\n');served=at(first.slice(0,cut)+'<script>self.LAZY_FILES='+JSON.stringify(Object.fromEntries(Object.keys(parts).map(g=>[g,'lazy-'+g+'.js'])))+'</script>'+first.slice(cut))}
 reset();page=await open(one(MAIL));await titled(page,'open: Reply to Casey about pricing');assert.deepEqual(await shown(page),['inbox','suggestions']);await page.context().close();
 mode='nopart';page=await open(one(MAIL));await page.locator('#load-failed').waitFor({state:'visible'});
 assert.equal(await page.evaluate(()=>getComputedStyle(document.querySelector('main')).visibility),'hidden');await page.context().close();mode='ok';

 // 8. The kept copy of the page opens this too (sw.js)
 assert.match(sw,/url\.search === '\?compact=1'/);
 assert.deepEqual(errors,[]);
 console.log('compact to-do: ok');
}finally{await browser?.close();server.close()}
