import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// New card and Rename on the dashboard. New card: a row under Find a to-do on a computer, "+" in the top bar on a
// phone, C, "new" in Find a to-do, and the palette (Ctrl/⌘K) then "new"; one field, optional Work/Personal, due date, person and email; Enter adds it
// with card_new and nothing else (no send). Rename: the sidebar row (⋯, double click, right click, long press on a
// phone), the chat's title and header menu, and the card (More, and a click on its title on a computer only).
// Optimistic, Esc cancels, empty keeps the old title, markup stays text, a failure puts the old title back.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString();
const id=n=>(n+'').padStart(2,'0').repeat(8);
const base0=()=>[
 {id:id(1),title:'Send Sam the signed contract',body:'Sam asked on Monday.',status:'pending',scope:'work',created_at:now,event_ids:[1]},
 {id:id(2),title:'Deck for Pat',title_suggested:'Send Pat the Q4 deck',body:'Pat wants the deck before Friday.',status:'pending',scope:'work',created_at:now,event_ids:[2]},
 {id:id(3),title:'Book the dentist',body:'',status:'pending',scope:'personal',created_at:now,event_ids:[3],origin:'owner',owner_words:'Book the dentist'},
 {id:id(4),title:'Reply to Sam about the contract',body:'Sam asked again.',status:'pending',scope:'work',created_at:now,event_ids:[4],origin:'owner',owner_words:'sam contract thing',merge_offer:JSON.stringify({card_id:id(1)})},
 {id:id(5),title:'Plan the offsite',body:'',status:'completed',scope:'work',created_at:now,event_ids:[5]}];
let cards,actions,failRename=false;
const reset=()=>{cards=base0();actions=[];failRename=false};reset();
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const chat=sid=>({session:true,status:'ok',active:false,cursor:'k1',items:[{kind:'event',text:'Renamed',at:Date.now()}]});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({found:[{id:'email:pat@acme.example',kind:'person',name:'Pat Doe',ids:['pat@acme.example']},{id:'org:acme.example',kind:'org',name:'Acme',domain:'acme.example'}]}));return}
 if(url.pathname==='/api/events'){const all=[{id:7,kind:'gmail.message',title:'Contract draft',metadata:{from:'Sam Lee <sam@client.example>'},body:''},{id:8,kind:'calendar.event',title:'Contract call',metadata:{},body:''},{id:9,kind:'slack.message',title:'contract?',metadata:{},body:''}];
  res.end(JSON.stringify(url.searchParams.get('kind')==='email'?all.filter(e=>e.kind==='gmail.message'):all));return}  // the server filters: kind=email
 if(url.pathname==='/api/action'){const r=JSON.parse(body);if(r.action!=='card_chat')actions.push(r);
  if(r.action==='card_new'){const c={id:'ab'.repeat(8),title:r.args.text.slice(0,90),body:'',status:'pending',scope:r.args.scope||'work',created_at:now,event_ids:[9],origin:'owner',owner_words:r.args.text,due:r.args.due};cards.unshift(c);res.end(JSON.stringify({id:c.id,status:'pending',title:c.title}));return}
  if(r.action==='card_rename'){if(failRename){res.statusCode=400;res.end(JSON.stringify({error:'Keep the title under 200 characters'}));return}
   const c=cards.find(x=>x.id===r.args.suggestion_id);if(r.args.reset){c.title=c.title_suggested;c.title_suggested=null}else{c.title_suggested=c.title_suggested??c.title;c.title=r.args.title}res.end(JSON.stringify({id:c.id,title:c.title}));return}
  res.end(JSON.stringify(r.action==='card_chat'?chat(r.args?.suggestion_id):{}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const open=async(width,height)=>{const mobile=width<600;reset();
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.goto(base);await page.locator('#task-'+id(1)).waitFor();return {context,page}};
const sent=name=>actions.filter(a=>a.action===name);
const shot=async(page,what)=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/after-${what}-${page.viewportSize().width}.png`})};
const until=async(f,what)=>{for(let i=0;i<50;i++){if(await f())return;await new Promise(r=>setTimeout(r,60))}assert.fail('timed out: '+what)};
const renameTo=async(page,text)=>{const input=page.locator('.rename-box input');await input.waitFor();await input.fill(text);await input.press('Enter');await page.locator('.rename-box').waitFor({state:'detached'})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // The read of "Friday", "in 2 weeks", "24 Oct": from a Thursday
 {const {context,page}=await open(1440,900);
  const due=await page.evaluate(()=>{const t=new Date(2026,9,22),f=x=>{const d=ncDue(x,t);return d?ncISO(d):null};return ['friday','Thursday','in 2 weeks','tomorrow','24 Oct','oct 2','24/10','2026-11-03','next week','in a month','by friday','soonish','next Fri','3 Nov','fri next week','next week monday'].map(f)});
  assert.deepEqual(due,['2026-10-23','2026-10-29','2026-11-05','2026-10-23','2026-10-24','2027-10-02','2026-10-24','2026-11-03','2026-10-26','2026-11-22','2026-10-23',null,'2026-10-23','2026-11-03','2026-10-30','2026-10-26']);
  // Times too, from Thursday 10:30, and the same in the app's other languages; a bare "9" needs a day
  const timed=await page.evaluate(()=>{const t=new Date(2026,9,22,10,30),p=n=>String(n).padStart(2,'0'),f=x=>{const d=ncDue(x,t);return d?ncISO(d)+(d.timed?' '+p(d.getHours())+':'+p(d.getMinutes()):''):null};
   return ['in 2 hours','15:00','2pm','now','tomorrow 9','fri at 3pm','9am','in 30 min','tonight','9','over 2 uur','morgen 9u','nu','vrijdag','morgen om 15:30','demain 14h','dans 2 heures','morgen um 9 Uhr','mañana a las 9','en 2 horas','domani alle 15',"tra un'ora",'amanhã às 9','24 oktober'].map(f)});
  assert.deepEqual(timed,['2026-10-22 12:30','2026-10-22 15:00','2026-10-22 14:00','2026-10-22 10:30','2026-10-23 09:00','2026-10-23 15:00','2026-10-23 09:00','2026-10-22 11:00','2026-10-22 18:00',null,
   '2026-10-22 12:30','2026-10-23 09:00','2026-10-22 10:30','2026-10-23','2026-10-23 15:30','2026-10-23 14:00','2026-10-22 12:30','2026-10-23 09:00','2026-10-23 09:00','2026-10-22 12:30','2026-10-23 15:00','2026-10-22 11:30','2026-10-23 09:00','2026-10-24']);
  assert.equal(await page.evaluate(()=>{const d=new Date(2026,9,22,15,0);return ncAt(d).slice(0,19)}),'2026-10-22T15:00:00');
  await context.close()}
 {const {context,page}=await open(1440,900);
  // The row sits under Find a to-do, above the tabs; the phone's "+" is not shown on a computer
  const y=s=>page.locator(s).evaluate(n=>n.getBoundingClientRect().top);
  assert.ok(await page.locator('#side-new').isVisible());assert.ok(!(await page.locator('#new-card-top').isVisible()));
  assert.ok(await y('#side-search')<await y('#side-new')&&await y('#side-new')<await y('nav'),'New card is between Find a to-do and the tabs');
  await page.locator('#side-new').click();const dialog=page.locator('#new-card');await dialog.waitFor();
  assert.equal(await page.evaluate(()=>document.activeElement.id),'nc-text');assert.equal(await page.locator('#nc-text').getAttribute('placeholder'),'What needs doing?');
  // Shift+Enter is a new line; the chips are optional: Work, Due, a person and an email
  await page.locator('#nc-text').type('Send Pat the signed contract');await page.keyboard.press('Shift+Enter');await page.keyboard.type('and the deck');
  await page.locator('[data-nc="work"]').click();assert.equal(await page.locator('[data-nc="work"]').getAttribute('aria-pressed'),'true');
  await page.locator('[data-nc="due"]').click();await page.locator('#nc-find').fill('friday');assert.match(await page.locator('#nc-read').textContent(),/^Due Fri, \w{3} \d+ Enter sets it$/);
  await page.locator('#nc-find').fill('whenever');assert.equal(await page.locator('#nc-read').textContent(),'I can’t read that yet. Try 15:00, in 2 hours or Friday.');
  await page.locator('#nc-find').fill('15:00');assert.match(await page.locator('#nc-read').textContent(),/^Due \w{3}, \w{3} \d+ 15:00 Enter sets it$/);
  await page.locator('#nc-find').fill('friday');await page.locator('#nc-find').press('Enter');assert.match(await page.locator('#nc-chips').textContent(),/Due Fri/);
  // A tap on the read date sets it too; the calendar button picks one
  await page.locator('[data-nc="due"]').click();await page.locator('#nc-find').fill('3 Nov');await page.locator('#nc-read [data-nc-set]').click();
  assert.match(await page.locator('#nc-chips').textContent(),/Due Tue, Nov 3/);
  // The calendar icon opens quick picks like Snooze's, and Choose date
  await page.locator('[data-nc="due"]').click();await page.locator('#nc-cal').click();
  assert.deepEqual(await page.locator('#nc-quick [data-nc-quick]').allInnerTexts(),['2 hours','Tomorrow · 9:00','3 days · 9:00','1 week · 9:00']);
  await shot(page,'due-quick');
  await page.locator('[data-nc-quick="tomorrow"]').click();assert.match(await page.locator('#nc-chips').textContent(),/Due \w{3}, \w{3} \d+ 09:00/);
  await page.locator('[data-nc="due"]').click();await page.locator('#nc-cal').click();assert.equal(await page.locator('#nc-pick input[type="date"]').count(),1,'a date picker');
  {const d=new Date(Date.now()+10*864e5),iso=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
   await page.locator('#nc-date').fill(iso);assert.match(await page.locator('#nc-chips').textContent(),new RegExp('Due \\w{3}, \\w{3} '+d.getDate()+'\\b'))}
  await page.locator('[data-nc="due"]').click();await page.locator('#nc-find').fill('friday');await page.locator('#nc-find').press('Enter');
  await page.locator('[data-nc="about"]').click();await page.locator('#nc-find').fill('Pat');await page.locator('[data-nc-hit="0"]').waitFor();await page.locator('[data-nc-hit="0"]').click();
  await page.locator('[data-nc="attach"]').click();await page.locator('#nc-find').fill('contract');await page.locator('[data-nc-hit="0"]').waitFor();
  assert.equal(await page.locator('[data-nc-hit]').count(),1,'only emails can be attached (it asks for kind=email)');await page.locator('#nc-find').press('Enter');
  assert.match(await page.locator('#nc-chips').textContent(),/Pat Doe.*Contract draft/);
  assert.equal(actions.length,0,'nothing is saved before Enter');
  await page.locator('#nc-text').press('Enter');await dialog.waitFor({state:'hidden'});
  assert.equal(actions.length,1,'one action: card_new, and no send');const made=sent('card_new')[0].args;
  assert.equal(made.text,'Send Pat the signed contract\nand the deck');assert.equal(made.scope,'work');assert.deepEqual([made.about,made.attach],[['email:pat@acme.example'],[7]]);
  assert.equal(new Date(made.due+'T12:00:00').getDay(),5,'due on a Friday');assert.equal(made.due_at,null,'a day, no time');
  // The fresh card shows like any other, with Added by you in quiet text
  const fresh=page.locator('#task-'+'ab'.repeat(8));await fresh.waitFor();assert.match(await fresh.locator('.meta-side').textContent(),/^Added by you/);
  assert.match(await fresh.locator('.actions').textContent(),/Do it/);
  // C opens it, not while typing; Esc closes; "new" in Find a to-do or the palette opens it too
  await page.locator('body').press('c');await dialog.waitFor();await page.keyboard.press('Escape');await dialog.waitFor({state:'hidden'});
  await page.locator('#side-find').fill('c');assert.ok(!(await dialog.isVisible()),'C in a field types a c');await page.locator('#side-find').fill('');
  await page.locator('#side-find').fill('new');assert.match(await page.locator('#side-new').getAttribute('class'),/hit/);await page.locator('#side-find').press('Enter');await dialog.waitFor();
  assert.equal(await page.locator('#side-find').inputValue(),'');await page.keyboard.press('Escape');await dialog.waitFor({state:'hidden'});
  await page.locator('body').press('ControlOrMeta+k');await page.locator('#palette').waitFor();await page.keyboard.type('new');await page.keyboard.press('Enter');await dialog.waitFor();
  // An empty field adds nothing
  await page.locator('#nc-text').press('Enter');assert.equal(sent('card_new').length,1);await page.keyboard.press('Escape');
  // The merge offer asks, and only a tap merges
  const own=page.locator('#task-'+id(4));assert.ok(!(await own.textContent()).includes('sam contract thing'),'their words stay in the chat, not under the title');
  assert.match(await own.locator('.merge-offer').textContent(),/Looks like the same as “Send Sam the signed contract”\. Merge\?/);
  await own.locator('[data-merge="yes"]').click();await until(()=>sent('card_merge').length===1,'merge');assert.deepEqual([sent('card_merge')[0].args.suggestion_id,sent('card_merge')[0].args.merge],[id(4),true]);

  // Rename from the sidebar: the ⋯ on hover, a right click, a double click
  const row=n=>page.locator(`#side-cards a[href="#chat=${id(n)}"]`);
  await row(1).hover();const more=page.locator('.row-more');await more.waitFor();await more.click();await page.locator('.row-menu [data-row-rename]').click();
  assert.equal(await page.locator('.rename-box input').inputValue(),'Send Sam the signed contract');await renameTo(page,'  Contract   for Sam ');
  assert.equal(await row(1).textContent(),'Contract for Sam','saved at once');await until(()=>sent('card_rename').length===1,'rename');
  assert.deepEqual(sent('card_rename')[0].args.title,'Contract for Sam');assert.equal(await page.locator('#task-'+id(1)+' h3').textContent(),'Contract for Sam');
  await row(3).click({button:'right'});await page.locator('.row-menu [data-row-rename]').click();await page.locator('.rename-box input').press('Escape');
  assert.equal(sent('card_rename').length,1,'Esc cancels');
  await row(3).dblclick();await renameTo(page,'   ');assert.equal(sent('card_rename').length,1,'empty keeps the old title');assert.equal(await row(3).textContent(),'Book the dentist');
  await row(3).dblclick();await renameTo(page,'<img src=x onerror=alert(1)> & co');await until(()=>sent('card_rename').length===2,'markup rename');
  assert.equal(await row(3).textContent(),'<img src=x onerror=alert(1)> & co');assert.equal(await page.locator('#side-cards img,#suggestions h3 img').count(),0,'markup stays text');
  // A failure puts the old title back and says why
  failRename=true;await row(1).dblclick();await renameTo(page,'Something else');await page.locator('#toast.error').waitFor();
  assert.match(await page.locator('#toast').textContent(),/under 200/);assert.equal(await row(1).textContent(),'Contract for Sam');failRename=false;
  // From the card: More → Rename, and a click on the title (on a computer) edits it instead of opening the chat
  // (a double click opened that chat too, like a click does) back to the cards
  await page.locator('nav [data-tab="inbox"]').click();await page.locator('#suggestions .chat-layout').waitFor({state:'detached'});
  await page.locator('#task-'+id(2)+' .more-actions summary').click();await page.locator('#task-'+id(2)+' [data-rename]').click();
  await page.locator('.rename-reset').waitFor();// a renamed card offers its suggested title
await page.locator('.rename-reset').click();
  await until(()=>sent('card_rename').some(a=>a.args.reset),'reset');assert.equal(await page.locator('#task-'+id(2)+' h3').textContent(),'Send Pat the Q4 deck');
  await page.locator('#task-'+id(1)+' h3 .title-link').click();await renameTo(page,'Sam: contract');assert.equal(await page.locator('#suggestions .chat-layout').count(),0,'no chat opened');
  await until(()=>sent('card_rename').length===5,'title click');
  // Done cards rename too (the sidebar's Done list)
  await page.locator('[data-side-fold="done"]').click();await row(5).dblclick();await renameTo(page,'Offsite in May');await until(()=>sent('card_rename').length===6,'done');
  // From the chat: a click on the title, and Rename in the header menu
  await row(3).click();await page.locator('#chat-log').waitFor();await page.locator('.chat-title').click();await renameTo(page,'Dentist');
  await until(()=>sent('card_rename').length===7,'chat title');assert.equal(await page.locator('.chat-title').textContent(),'Dentist');
  await page.locator('#chat-menu summary').click();await page.locator('#chat-menu [data-rename]').click();await renameTo(page,'Dentist, Tuesday');
  await until(()=>sent('card_rename').length===8,'chat menu');assert.equal(await page.locator('.chat-title').textContent(),'Dentist, Tuesday');
  assert.ok(sent('card_rename').every(a=>/^[0-9a-f-]{36}$/.test(a.args.decision_id)));
  await context.close()}
 // Phone: "+" in the top bar, the title tap still opens the card, a long press in the chat's list, the chat title
 {const {context,page}=await open(390,844);
  assert.ok(await page.locator('#new-card-top').isVisible());assert.ok(!(await page.locator('#side-new').isVisible()));
  const plus=await page.locator('#new-card-top').boundingBox();assert.ok(plus.x+plus.width<=390&&plus.width>=32,'the + fits');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'nothing wider than the screen');
  await page.locator('#new-card-top').tap();await page.locator('#new-menu [data-new-what="card"]').tap();await page.locator('#new-card').waitFor();await page.waitForFunction(()=>!document.querySelector('#new-card').getAnimations().length);  // slid up, also on a busy machine
  {const b=await page.locator('#new-card').boundingBox();assert.ok(Math.abs(b.y+b.height-844)<=1&&b.x<=1&&b.width>=389,'on a phone the composer is a bottom sheet');}
  await page.locator('#nc-text').fill('Call Sam back');
  await page.locator('#nc-add').tap();await page.locator('#new-card').waitFor({state:'hidden'});assert.equal(sent('card_new')[0].args.text,'Call Sam back');
  // New card is in the drawer too: the row opens the composer and closes the drawer
  await page.locator('#drawer-open').tap();await page.locator('#side-new').waitFor();await page.waitForTimeout(400);await page.locator('#side-new').tap();
  await page.locator('#new-card').waitFor();assert.notEqual(await page.evaluate(()=>document.documentElement.dataset.drawer),'open','the drawer closes');
  await page.locator('#new-card form button[aria-label="Close"]').tap();await page.locator('#new-card').waitFor({state:'hidden'});
  await page.waitForTimeout(800);await page.locator('#task-'+id(1)+' h3 .title-link').tap();await page.locator('#chat-log').waitFor();assert.equal(await page.locator('.rename-box').count(),0,'a tap opens the card');
  // All tasks as a person reaches it: open the menu, then tap (an open menu is never redrawn under the tap)
  await page.locator('#chat-menu summary').tap();await page.locator('#chat-menu [data-chat-drawer]').tap();const link=page.locator(`#side-cards a[href="#chat=${id(2)}"]`);await link.waitFor();
  await page.waitForTimeout(500);const box=await link.boundingBox();const cdp=await context.newCDPSession(page);
  const touch=(type,points)=>cdp.send('Input.dispatchTouchEvent',{type,touchPoints:points});
  await touch('touchStart',[{x:box.x+20,y:box.y+box.height/2}]);await page.waitForTimeout(650);await touch('touchEnd',[]);
  await page.locator('.row-menu [data-row-rename]').tap();await renameTo(page,'Deck');await until(()=>sent('card_rename').length===1,'long press');
  assert.equal(await page.locator('.chat-title').textContent(),'Send Sam the signed contract','still on the same chat');
  if(await page.evaluate(()=>document.documentElement.dataset.drawer==='open'))await page.locator('#side-toggle').tap();  // the list is the app's drawer on a phone
  await page.waitForFunction(()=>document.documentElement.dataset.drawer!=='open');await page.waitForTimeout(500);
  await page.locator('.chat-title').tap();await renameTo(page,'Contract');await until(()=>sent('card_rename').length===2,'phone chat title');
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('new card dashboard ok');
