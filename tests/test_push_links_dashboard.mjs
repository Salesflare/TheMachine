import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Where a tapped notification lands. The phone app opens the dashboard at #chat=<the push's tag> (mobile/www/inject.js;
// Android without a tag for several at once: the kind), the web push at its url. Each kind opens its own view, never a
// to-do chat that isn't there: a to-do its chat, the morning the Calendar's agenda, the team brief that Fleet's brief in
// its pane, a Fleet question its card, a Fleet notice its line, the week's recap and a test To-dos. Each case starts
// somewhere else (a chat open, another Fleet pane), and every target must be on screen.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),FL='fl_'+'a'.repeat(16),FL2='fl_'+'b'.repeat(16),Q='q_'+'1'.repeat(16),N='fn_'+'2'.repeat(16),TODO='a1a1a1a1a1a1a1a1';
const cards=[{id:TODO,title:'Reply to the venue about the date',body:'They offer the 14th.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1]}];
const rules={relationships:{rule:'ask',details:false},brief:{rule:'always',details:false},anything:{rule:'ask',details:false}};
const work=(id,name,mate)=>({id,kind:'work',label:'Work Fleet',name,asks:['relationships','brief','anything'],
 people:[{member_id:'me',name:'Sam',role:'owner',me:true,email:'sam@'+name.toLowerCase()+'.example'},{member_id:mate,name:mate,role:'member',me:false,email:mate.toLowerCase()+'@'+name.toLowerCase()+'.example'}],
 members:[{member_id:mate,name:mate,rules}],rules,exceptions:{}});
const brief=title=>({text:'Your Fleet this week',built_at:now,shown:5,items:[{key:'k:'+title,title,why:'5 days, nobody answered',ask:'',open:''}]});
const fleetView={on:true,kinds:{relationships:'who knows someone',brief:'brief facts',anything:'free questions'},ask_meetings:false,
 kind_rules:{relationships:['ask','always','never'],brief:['ask','always','never'],anything:['ask','never']},no_details:['brief','anything'],brief:{every:'week',tell:true},
 briefs:{[FL]:brief('Globex is waiting for a reply'),[FL2]:brief('Initech went quiet')},free:[],
 fleets:[work(FL,'Acme','Pat'),work(FL2,'Northwind','Kim')],
 waiting:[{id:Q,fleet:FL,member_id:'Pat',name:'Pat',kind:'relationships',status:'waiting',at:now,question:'Who knows someone at Globex?'}],
 asked:[],log:[],notices:[{id:N,fleet:FL2,kind:'seat_confirmed',text:'Your Machine was confirmed in Northwind.',buttons:[]}]};
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:true,waiting:1,fleets:fleetView.fleets}});
let slow=0,statusDone=0;  // a Machine slow to answer the status: the tapped view still opens at once
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){if(slow)await new Promise(r=>setTimeout(r,slow));res.end(JSON.stringify(state()));statusDone++;return}
 if(url.pathname==='/api/fleet'){res.end(JSON.stringify(fleetView));return}
 if(url.pathname==='/api/calendar'){res.end(JSON.stringify({calendars:[],meetings:[]}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k',items:[{kind:'reply',text:'The draft is ready.',at:Date.now()}]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.PUSH_LINK_SHOTS||'';
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [label,viewport] of [['phone',{width:390,height:844}],['desktop',{width:1440,height:900}]]){
  const context=await browser.newContext({viewport,locale:'en-US',...(label==='phone'?{isMobile:true,hasTouch:true}:{})});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const shown=sel=>page.locator(sel).first().evaluate(el=>{const r=el.getBoundingClientRect();return !el.closest('[hidden]')&&r.height>0&&r.bottom>0&&r.top<innerHeight});
  const landed=async(sel,why)=>{for(let i=0;i<100;i++){if(await page.locator(sel).count()&&await shown(sel))return;await page.waitForTimeout(50)}assert.fail(`${label} ${why}: ${sel} is not on screen (at ${new URL(page.url()).hash}) `+JSON.stringify(await page.locator(sel).first().evaluate(el=>({r:el.getBoundingClientRect().toJSON(),h:!!el.closest("[hidden]"),hid:el.closest("[hidden]")?.id,ih:innerHeight})).catch(e=>String(e))))};
  const tab=async name=>page.evaluate(n=>!document.getElementById(n).hidden,name);
  // somewhere else first: the to-do's chat open, the Fleet tab on the other pane
  const elsewhere=async()=>{await page.evaluate(id=>{location.hash='chat='+id},TODO);await landed(`.chat-layout[data-chat="${TODO}"] .chat-title`,'the chat to start from')};
  const tap=async tag=>{await elsewhere();await page.evaluate(t=>{location.hash='chat='+t},tag)};  // what inject.js does with a tapped push
  await page.goto(base);await page.locator('#task-'+TODO).waitFor();
  const cases=[
   ['a new to-do, a result, a reminder',TODO,async()=>{await landed(`.chat-layout[data-chat="${TODO}"] .chat-title`,'the to-do');assert.equal(new URL(page.url()).hash,'#chat='+TODO)}],
   ['the morning','digest',async()=>{await landed('#calendar','the Calendar');assert.ok(await tab('calendar'));assert.match(new URL(page.url()).hash,/^#calendar\?(.*&)?view=agenda/)}],
   ['the team brief',`fleet-brief-${FL2}`,async()=>{await landed(`#fleet-brief-${FL2}`,'that Fleet’s brief');assert.ok(await tab('fleet'))}],
   ['the team brief from an older Machine','fleet-brief',async()=>{await landed('#fleet-view .fleet-brief','a brief');assert.ok(await tab('fleet'))}],
   ['a Fleet question',`fleet-${Q}`,async()=>{await landed(`#fleet-${Q}`,'the question’s card');assert.ok(await tab('inbox'))}],
   ['a Fleet notice',`fleet-${N}`,async()=>{await landed(`#fleet-${N}`,'the notice');assert.ok(await tab('fleet'))}],
   ['several Fleet questions (Android: the kind)','fleet',async()=>{await landed('#fleet-view .fleet-pane:not([hidden])','the Fleet tab')}],
   ['the week’s recap','recap-2026-W45',async()=>{await landed('#suggestions','To-dos');assert.ok(await tab('inbox'));assert.equal(await page.locator('.chat-layout').count(),0)}],
   ['a test','push-test',async()=>{await landed('#suggestions','To-dos');assert.equal(await page.locator('.chat-layout').count(),0)}],
   ['several new to-dos (Android: the kind)','todo',async()=>{await landed('#suggestions','To-dos');assert.equal(await page.locator('.chat-layout').count(),0)}]];
  for(const [what,tag,check] of cases){
   if(tag.startsWith('fleet-brief'))await page.evaluate(()=>localStorage.setItem('fleet-pane','sharing'));  // the brief's pane isn't the one last open
   await tap(tag);await check();
   assert.doesNotMatch(new URL(page.url()).hash,/^#chat=(?![a-f0-9]{16}$)/,`${label} ${what}: no chat link left that isn't a to-do`);
   if(shots&&['digest',`fleet-brief-${FL2}`,`fleet-${Q}`,'recap-2026-W45'].includes(tag)){await page.waitForTimeout(400);await page.screenshot({path:`${shots}/${label}-${tag.replace(/_.*/,'')}.png`})}}
  // the web push's own links: the brief's (#fleet-brief=<fleet>) opens that brief in its pane too
  await page.evaluate(()=>localStorage.setItem('fleet-pane','sharing'));await elsewhere();
  await page.evaluate(fl=>{location.hash='fleet-brief='+fl},FL2);await landed(`#fleet-brief-${FL2}`,'the web brief link');
  await elsewhere();await page.evaluate(()=>{location.hash='calendar?view=agenda'});await landed('#calendar','the web morning link');
  // a tap that starts the app: the page loads with the tag already in its address
  await page.goto(base+'#chat=digest');await landed('#calendar','the morning on a cold start');
  await page.goto(base+'#chat=fleet-brief-'+FL);await landed(`#fleet-brief-${FL}`,'the brief on a cold start');
  // A slow status (a big Machine): the tapped view opens at once, its own data fills it, the to-dos come later
  slow=6000;
  for(const [hash,sel,why] of [['#chat=digest','#calendar','the morning'],[`#chat=fleet-brief-${FL2}`,`#fleet-brief-${FL2}`,'the brief'],['#chat=fleet','#fleet-view .fleet-pane:not([hidden])','the Fleet tab']]){
   await page.evaluate(()=>localStorage.setItem('fleet-pane','sharing'));
   await page.goto('about:blank');const t0=Date.now(),before=statusDone;await page.goto(base+hash,{waitUntil:'domcontentloaded'});await landed(sel,why+' before the status');
   assert.ok(Date.now()-t0<slow-1000,`${label} ${why}: on screen in ${Date.now()-t0} ms, not after the status`);
   assert.equal(statusDone,before,`${label} ${why}: the status hasn't come yet`)}
  slow=0;
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('push links dashboard ok');
