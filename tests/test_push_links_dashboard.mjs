import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Where a tapped notification lands. The phone app opens the dashboard at #chat=<the push's tag> (mobile/www/inject.js;
// Android without a tag for several at once: the kind), the web push at its url. Each kind opens its own view, never a
// to-do chat that isn't there: a to-do its chat, the morning and evening digest that digest, the team brief To-dos (its lines are
// to-dos there), a Fleet question its card, a Fleet notice its line, the week's recap and a test To-dos. Each case starts
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
const DIGESTS={morning:{kind:'morning',title:'Morning, 1 due today',text:'• Reply to the venue about the date',sections:[],at:now},
 evening:{kind:'evening',title:'Good evening, 21 to-dos done today',text:'Work\nDone today\n• Send the invoice\n• +20 more\n• +2 meetings',
  blocks:[['h','Work'],['sub','Done today'],['li','Send the invoice'],['more','+20 more'],['more','+2 meetings']],sections:[{area:'work',copy:'Done today\n• Send the invoice'}],at:now}};
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:true,waiting:1,fleets:fleetView.fleets}});
// A Machine slow to answer the status: the tapped view still opens at once. Each status read is logged with when it
// started, so one still sleeping from an earlier load (its page long gone) never counts for the next.
let slow=0;const statuses=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){const s={at:Date.now(),done:false};statuses.push(s);if(slow)await new Promise(r=>setTimeout(r,slow));res.end(JSON.stringify(state()));s.done=true;return}
 if(url.pathname==='/api/fleet'){res.end(JSON.stringify(fleetView));return}
 if(url.pathname==='/api/calendar'){res.end(JSON.stringify({calendars:[],meetings:[]}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  if(r.action==='digest_sent'){res.end(JSON.stringify(DIGESTS[r.args.kind]));return}
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
  // on screen: waits for the page itself to show it (busy CI machines included), then says where it was if it never did
  const landed=async(sel,why)=>{if(await page.waitForFunction(s=>{const el=document.querySelector(s);if(!el)return false;const r=el.getBoundingClientRect();return !el.closest('[hidden]')&&r.height>0&&r.bottom>0&&r.top<innerHeight},sel,{timeout:15000}).then(()=>true,()=>false))return;assert.fail(`${label} ${why}: ${sel} is not on screen (at ${new URL(page.url()).hash}) `+JSON.stringify(await page.locator(sel).first().evaluate(el=>({r:el.getBoundingClientRect().toJSON(),h:!!el.closest("[hidden]"),hid:el.closest("[hidden]")?.id,ih:innerHeight})).catch(e=>String(e))))};
  const tab=async name=>page.evaluate(n=>!document.getElementById(n).hidden,name);
  // somewhere else first: the to-do's chat open, the Fleet tab on the other pane
  const elsewhere=async()=>{await page.evaluate(id=>{location.hash='chat='+id},TODO);await landed(`.chat-layout[data-chat="${TODO}"] .chat-title`,'the chat to start from')};
  // a digest: To-dos with that digest open on top, as it went, then closed for the next case
  // one kept before it had blocks (the morning here) reads as its text; one with them as headings, subheads and a list
  const sent=async(kind,why)=>{const blocks=DIGESTS[kind].blocks;await landed(blocks?'#area-digest .ad-read':'#area-digest .ad-text',why);assert.ok(await tab('inbox'));
   assert.equal(await page.locator('#area-digest h2').innerText(),DIGESTS[kind].title);
   if(!blocks)assert.equal(await page.locator('#area-digest .ad-text').textContent(),DIGESTS[kind].text);
   else{// the overflow and the meetings close the list, muted, never loose lines beside it; "to-dos" never breaks
    assert.deepEqual(await page.evaluate(()=>[...document.querySelector('#area-digest .ad-read').children].map(e=>e.matches('ul')?['ul',[...e.children].map(li=>[li.className,li.textContent])]:[e.className,e.textContent])),
     [['ad-area','Work'],['ad-sub','Done today'],['ul',[['','Send the invoice'],['ad-more','+20 more'],['ad-more','+2 meetings']]]],why);
    assert.equal(await page.locator('#area-digest h2 .ad-nw').innerText(),'to-dos');
    assert.equal(await page.locator('#area-digest h2 .ad-nw').evaluate(e=>getComputedStyle(e).whiteSpace),'nowrap');
    const muted=await page.locator('#area-digest li.ad-more').first().evaluate(e=>getComputedStyle(e).color),plain=await page.locator('#area-digest .ad-list li').first().evaluate(e=>getComputedStyle(e).color);
    assert.notEqual(muted,plain,'the +N more line is muted')}
   await page.evaluate(()=>document.querySelector('#area-digest').close())};
  const tap=async tag=>{await elsewhere();await page.evaluate(t=>{location.hash='chat='+t},tag)};  // what inject.js does with a tapped push
  await page.goto(base);await page.locator('#task-'+TODO).waitFor();
  const cases=[
   ['a new to-do, a result, a reminder',TODO,async()=>{await landed(`.chat-layout[data-chat="${TODO}"] .chat-title`,'the to-do');assert.equal(new URL(page.url()).hash,'#chat='+TODO)}],
   ['the morning','digest',async()=>{await sent('morning','the morning digest')}],
   ['the evening','evening',async()=>{await sent('evening','the evening digest')}],
   ['the team brief',`fleet-brief-${FL2}`,async()=>{await landed('#suggestions','To-dos');assert.ok(await tab('inbox'))}],
   ['the team brief from an older Machine','fleet-brief',async()=>{await landed('#suggestions','To-dos');assert.ok(await tab('inbox'))}],
   ['a Fleet question',`fleet-${Q}`,async()=>{await landed(`#fleet-${Q}`,'the question’s card');assert.ok(await tab('inbox'))}],
   ['a Fleet notice',`fleet-${N}`,async()=>{await landed(`#fleet-${N}`,'the notice');assert.ok(await tab('fleet'))}],
   ['several Fleet questions (Android: the kind)','fleet',async()=>{await landed('#fleet-view .fleet-pane:not([hidden])','the Fleet tab')}],
   ['the week’s recap','recap-2026-W45',async()=>{await landed('#suggestions','To-dos');assert.ok(await tab('inbox'));assert.equal(await page.locator('.chat-layout').count(),0)}],
   ['a test','push-test',async()=>{await landed('#suggestions','To-dos');assert.equal(await page.locator('.chat-layout').count(),0)}],
   ['several new to-dos (Android: the kind)','todo',async()=>{await landed('#suggestions','To-dos');assert.equal(await page.locator('.chat-layout').count(),0)}]];
  for(const [what,tag,check] of cases){
   await tap(tag);await check();
   assert.doesNotMatch(new URL(page.url()).hash,/^#chat=(?![a-f0-9]{16}$)/,`${label} ${what}: no chat link left that isn't a to-do`);
   if(shots&&['digest',`fleet-brief-${FL2}`,`fleet-${Q}`,'recap-2026-W45'].includes(tag)){await page.waitForTimeout(400);await page.screenshot({path:`${shots}/${label}-${tag.replace(/_.*/,'')}.png`})}}
  // the web push's and Telegram's own links: the brief's (#fleet-brief=<fleet>) opens To-dos too
  await elsewhere();
  await page.evaluate(fl=>{location.hash='fleet-brief='+fl},FL2);await landed('#suggestions','the web brief link');assert.ok(await tab('inbox'));
  assert.equal(new URL(page.url()).hash,'#todos');
  // the web push's and the email's digest links
  for(const kind of ['morning','evening']){await elsewhere();await page.evaluate(k=>{location.hash='digest='+k},kind);await sent(kind,`the web ${kind} link`)}
  // a tap that starts the app: the page loads with the tag already in its address
  await page.goto(base+'#chat=digest');await sent('morning','the morning on a cold start');
  await page.goto(base+'#digest=evening');await sent('evening','the evening email link on a cold start');
  await page.goto(base+'#chat=fleet-brief-'+FL);await landed('#suggestions','the brief on a cold start');
  // A slow status (a big Machine): the tapped view opens at once, its own data fills it, the to-dos come later
  slow=12000;
  for(const [hash,sel,why] of [['#chat=digest','#area-digest .ad-text','the morning'],['#chat=fleet','#fleet-view .fleet-pane:not([hidden])','the Fleet tab']]){
   await page.evaluate(()=>localStorage.setItem('fleet-pane','sharing'));
   await page.goto('about:blank');const t0=Date.now();await page.goto(base+hash,{waitUntil:'domcontentloaded'});await landed(sel,why+' before the status');
   assert.ok(Date.now()-t0<slow-1000,`${label} ${why}: on screen in ${Date.now()-t0} ms, not after the status`);
   assert.equal(statuses.filter(s=>s.at>=t0&&s.done).length,0,`${label} ${why}: the status hasn't come yet`)}
  slow=0;
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('push links dashboard ok');
