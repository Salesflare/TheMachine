import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {runInNewContext} from 'node:vm';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Fleet tab, Family: when everyone is free, to-dos and plans in one compact pane; a member's to-do or plan waits as a
// Family card under To-dos with Accept and Decline; the Family's rules sit under Sharing. Never scrolls sideways.
const dashboard=await dashboardPage();
const FL='fl_'+'a'.repeat(16),FAM='fl_'+'f'.repeat(16),FL2='fl_'+'c'.repeat(16),FR='fr_'+'b'.repeat(16);
const r=rule=>({rule,details:false});
const view={on:true,kinds:{relationships:'who knows someone',availability:'free/busy times',todo:'to-dos',event:'family plans',question:'questions'},ask_meetings:false,
 person_rules:{question:['ask','always','never']},
 kind_rules:{question:['ask','never'],relationships:['ask','always','never'],availability:['ask','always','never'],todo:['ask','always','never'],event:['ask','always','never']},
 no_details:['availability','todo','event','question'],scoped:[],scopes:{},
 // As the directory lists them: Work first, then friends, then the Family. The tabs go by when each was joined.
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',joined_at:'2026-03-01T09:00:00Z',asks:['relationships'],people:[{member_id:'m',name:'Sam Doe',me:true}],members:[]},
  {id:FL2,kind:'work',label:'Work Fleet',name:'Beta',joined_at:'2026-08-01T09:00:00Z',asks:['relationships'],people:[{member_id:'m2',name:'Sam Doe',me:true}],members:[]},
  {id:FR,kind:'friends',label:'Friends',name:'Friends',asks:[],people:[{member_id:'fp_me',name:'Sam Doe',me:true}],members:[],rules:{},exceptions:{}},
  {id:FAM,kind:'family',joined_at:'2026-05-01T09:00:00Z',label:'Family Fleet',name:'Home',asks:['availability','todo','event','question'],rules:{availability:r('always'),todo:r('ask'),event:r('ask'),question:r('ask')},exceptions:{},
   people:[{member_id:'fm_me',name:'Sam Doe',me:true},{member_id:'fm_robin',name:'Robin',answers_with:'Hosted: robin.example.test'},{member_id:'fm_alex',name:'Alex'}],
   members:[{member_id:'fm_robin',name:'Robin',rules:{availability:r('always'),todo:r('ask'),event:r('ask')}},{member_id:'fm_alex',name:'Alex',rules:{availability:r('always'),todo:r('ask'),event:r('ask')}}]}],
 family:{id:FAM,free:[{id:'t1',at:'2026-10-20T10:00:00Z',start:'2026-10-24',days:7,known:1,asked:2,waiting:['Alex'],unknown:[null],
   slots:[{from:'2026-10-24T08:00+02:00',until:'2026-10-24T11:00+02:00',text:'Sat 24 Oct 08:00–11:00'}]}],
  todos:[{id:'t2',title:'Buy milk',name:'Alex',stage:'accepted',due:'2026-10-24'}],
  plans:[{id:'t3',title:'Dinner at grandma’s with a rather long name that should wrap nicely',start:'2026-10-25T18:00+02:00',place:'Grandma’s',yes:['Robin'],no:[],waiting:['Alex'],link:'https://calendar.google.com/calendar/render?action=TEMPLATE&text=Dinner'}],
  mine:[{id:'t4',title:'Pick up Sam',name:'Robin',stage:'accepted',due:'2026-10-21'}],
  ask:true,questions:[{id:'t5',at:'2026-10-20T10:00:00Z',name:'Robin',question:'Any news about the carpet?',state:'answered',answer:'It comes on Thursday.'},{id:'t9',at:'2026-10-20T11:00:00Z',name:'Robin',question:'When is the bin day?',state:'answered',answer:'On Monday.',auto:true},
   {id:'t6',at:'2026-10-19T10:00:00Z',name:'Alex',question:'When does the plumber come?',state:'waiting'},{id:'t7',at:'2026-10-15T10:00:00Z',name:'Alex',question:'Did the school write?',state:'none'},
   {id:'t8',at:'2026-10-14T10:00:00Z',name:'Alex Moss',question:'Is the bike ready?',state:'old'}]},
 waiting:[{id:'q_'+'3'.repeat(16),fleet:FAM,member_id:'fm_robin',name:'Robin',kind:'question',question:'“Any <b>news</b> about the carpet?”',status:'waiting',at:'2026-10-20T12:00:00Z',
   draft:{state:'ready',text:'It ships on Thursday.',sources:[{id:41,kind:'gmail.message',title:'Your order is on its way',from:'Rugs & More',at:'2026-10-19T09:00:00Z'}]}},
  {id:'q_'+'4'.repeat(16),fleet:FAM,member_id:'fm_alex',name:'Alex',kind:'question',question:'“What did the bank say?”',status:'waiting',at:'2026-10-20T12:30:00Z',draft:{state:'aside'}},
  ...['5','6'].map(n=>({id:'q_'+n.repeat(16),fleet:FAM,member_id:'fm_robin',name:'Robin',kind:'question',question:'“When does the plumber come?”',status:'waiting',at:'2026-10-20T12:40:00Z',
   draft:{state:'ready',text:'Friday at 9.',goes:n==='5'?'2026-10-20T14:20:00+00:00':'',sources:[{id:42,kind:'gmail.message',title:'Your visit',from:'Pipes',at:'2026-10-19T09:00:00Z'}]}})),
{id:'q_'+'1'.repeat(16),fleet:FAM,member_id:'fm_robin',name:'Robin',kind:'todo',question:'To-do: Pick up the kids, due Fri 23 Oct',status:'waiting',at:'2026-10-20T10:00:00Z'},
  {id:'q_'+'2'.repeat(16),fleet:FAM,member_id:'fm_alex',name:'Alex',kind:'event',question:'Plan: Zoo trip, Sun 25 Oct',status:'waiting',at:'2026-10-20T11:00:00Z'}],
 plan_calendar:'Home calendar',  // "I'm in" adds a plan to the owner's own calendar (family.py)
 friends:{id:FR,username:'sam',in:[],out:[],blocked:[]},
 asked:[],log:[],notices:[]};
const calls=[];
const landed=async action=>{for(let i=0;i<100&&!calls.some(c=>c.action===action);i++)await new Promise(r=>setTimeout(r,50))};  // the call lands, also on a busy runner
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify({suggestions:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:1}}));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  res.end(JSON.stringify(call.action==='fleet_decide'&&call.args.id==='q_'+'2'.repeat(16)?{status:'answered',card_id:'c1',calendar:{name:'Home calendar',id:call.args.id}}:{ok:true}));return}
 if(req.url.startsWith('/api/activity')){res.end(JSON.stringify({kinds:['fleet'],next:null,items:[{id:'fleet:1',kind:'fleet',at:'2026-10-20T12:00:00Z',what:'Robin asked your Machine',where:'Home',outcome:'done',status:'Answered by itself',
  detail:'Sent: “Friday at 9.” · From: Your visit',undo:{action:'family_question_ask_first',id:'q_'+'7'.repeat(16)}}]}));return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(view));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 for(const [scheme,width] of [['dark',390],['light',1000]]){
  const page=await (await browser.newContext({viewport:{width,height:900},colorScheme:scheme})).newPage();
  // Each family form redraws the Fleet view after its call: the next form is filled only after that, or the redraw drops it
  const acted=async(click,action)=>{const back=page.waitForResponse(r=>r.url().includes('/api/fleet'));await click();await landed(action);await back;await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>r())))};
  const errors=[];page.on('pageerror',e=>errors.push(e.message));let dialogs=0;page.on('dialog',d=>{dialogs++;d.accept()});
  await page.goto('http://127.0.0.1:'+server.address().port);
  // A member's to-do waits under To-dos, as a Family card
  const card=page.locator('#fleet-q_'+'1'.repeat(16));await card.waitFor();
  assert.match(await card.innerText(),/Family/);assert.doesNotMatch(await card.innerText(),/Work/);
  assert.match(await card.innerText(),/Robin asks you to do something/);
  calls.length=0;await card.locator('[data-choice-f="once"]').click();await landed('fleet_decide');
  assert.deepEqual(calls.at(-1),{action:'fleet_decide',args:{id:'q_'+'1'.repeat(16),choice:'once'}});
  // A question: their words quoted as text, the messages the draft comes from, and the answer to edit, all before Send
  const ask=page.locator('#fleet-q_'+'3'.repeat(16));await ask.waitFor();const asked=await ask.innerText();
  for(const want of [/Robin asks your Machine/,/Any <b>news<\/b> about the carpet\?/,/From your messages/,/Your order is on its way/,/Rugs & More/,/only this goes to them/])assert.match(asked,want);
  assert.equal(await ask.locator('[data-choice-f="always"],[data-choice-f="once"]').count(),0);
  await ask.locator('[data-fleet-source="41"]').click();await page.locator('#email-dialog[open]').waitFor();await page.keyboard.press('Escape');
  await ask.locator('textarea').fill('Thursday!');calls.length=0;await ask.locator('[data-fleet-send]').click();await landed('fleet_decide');
  assert.deepEqual(calls.at(-1),{action:'fleet_decide',args:{id:'q_'+'3'.repeat(16),choice:'once',text:'Thursday!'}});
  // One set aside shows only its words: nothing on what was found, or that nothing was
  const quiet=page.locator('#fleet-q_'+'4'.repeat(16)),set=await quiet.innerText();assert.match(set,/What did the bank say/);assert.doesNotMatch(set,/draft|found|private|messages/i);assert.equal(await quiet.locator('textarea').inputValue(),'');
  // One that goes by itself says when, beside its messages, with Stop; the first letter changed stops it too
  const held=page.locator('#fleet-q_'+'5'.repeat(16));assert.match(await held.innerText(),/Goes by itself at \d/);assert.match(await held.innerText(),/Your visit/);assert.match(await held.locator('.primary').innerText(),/Send now/);
  calls.length=0;await held.locator('[data-fleet-stop]').click();await landed('fleet_decide');
  assert.deepEqual(calls.at(-1),{action:'fleet_decide',args:{id:'q_'+'5'.repeat(16),choice:'stop'}});
  const later=page.locator('#fleet-q_'+'6'.repeat(16));assert.match(await later.innerText(),/Goes by itself, after a notification/);
  calls.length=0;await later.locator('textarea').pressSequentially('No. ');await landed('fleet_decide');
  assert.deepEqual(calls.filter(c=>c.action==='fleet_decide'),[{action:'fleet_decide',args:{id:'q_'+'6'.repeat(16),choice:'stop'}}]);
  // A plan: I'm in says which calendar it goes on, nobody invited; the toast's Undo takes the event off again
  const plan=page.locator('#fleet-q_'+'2'.repeat(16));await plan.waitFor();
  assert.match(await plan.innerText(),/Alex proposes a plan/);assert.match(await plan.innerText(),/adds it to Home calendar\. Nobody is invited\./);
  await plan.locator('[data-choice-f="once"]').click();const undo=page.locator('#toast [data-plan-undo]');await undo.waitFor();
  assert.match(await page.locator('#toast').innerText(),/Answered\. Added to Home calendar\./);
  calls.length=0;await undo.click();await landed('family_plan_undo');
  assert.deepEqual(calls.find(c=>c.action==='family_plan_undo'),{action:'family_plan_undo',args:{id:'q_'+'2'.repeat(16)}});
  await page.locator('#toast',{hasText:'Removed from your calendar.'}).waitFor();  // after the answer, also on a busy runner
  await navClick(page.locator('nav [data-tab="fleet"]'));await page.locator('.fleet-tabs').waitFor();
  // Every Fleet together, Work and Family, by when it was joined; then Friends, Sharing and Activity
  assert.deepEqual(await page.locator('.fleet-tabs [data-fleet-pane]').allInnerTexts(),['Acme','Home','Beta','Friends','Sharing','Activity']);
  await page.locator('[data-fleet-pane="family"]').click();await page.locator('#fleet-family').waitFor();
  const fam=page.locator('#fleet-family'),text=await fam.innerText();
  for(const want of [/When are we all free/,/Sat 24 Oct 08:00–11:00/,/waiting for Alex/,/Buy milk/,/Pick up Sam/,/In: Robin/,/Add to my calendar/])assert.match(text,want);
  assert.doesNotMatch(text,/Coming later/);
  assert.equal(await fam.locator('a.family-cal').first().getAttribute('href'),view.family.plans[0].link);
  for(const want of [/Ask someone’s Machine/,/It comes on Thursday\./,/No answer yet/,/No answer\n/,/Alex’s Machine needs an update first\./])assert.match(text,want);
  // The asker sees which answer went by itself, and only that one
  assert.deepEqual(await fam.locator('.family-answer',{hasText:'Answered by itself'}).allInnerTexts(),['On Monday. · Answered by itself']);
  await fam.locator('.family-question-form [name=member]').selectOption('fm_alex');await fam.locator('.family-question-form [name=text]').fill('Is the bike ready?');await acted(()=>fam.locator('.family-question-form button').click(),'family_question');
  assert.deepEqual(calls.at(-1),{action:'family_question',args:{member_id:'fm_alex',text:'Is the bike ready?'}});
  await fam.locator('.family-free-form [name=start]').fill('2026-10-24');await acted(()=>fam.locator('.family-free-form button').click(),'family_free');
  assert.deepEqual(calls.at(-1),{action:'family_free',args:{start:'2026-10-24',days:7}});
  await fam.locator('.family-todo-form [name=title]').fill('Groceries');await fam.locator('.family-todo-form [name=due]').fill('2026-10-23');await acted(()=>fam.locator('.family-todo-form button').click(),'family_todo');
  assert.deepEqual(calls.at(-1),{action:'family_todo',args:{member_id:'fm_robin',title:'Groceries',due:'2026-10-23'}});
  await fam.locator('.family-event-form [name=title]').fill('Zoo');await fam.locator('.family-event-form [name=start]').fill('2026-10-26T10:00');await acted(()=>fam.locator('.family-event-form button').click(),'family_event');
  const ev=calls.at(-1);assert.equal(ev.action,'family_event');assert.match(ev.args.start,/^2026-10-26T10:00[+-]\d{2}:\d{2}$/);
  // The Family's rules: under Sharing, the same three pills per kind
  const sharing=page.locator('[data-pane="sharing"]');
  for(const k of ['availability','todo','event'])assert.equal(await sharing.locator(`.fleet-rule[data-fleet="${FAM}"][data-kind="${k}"] [data-fleet-rule]`).count(),3,k);
  const rule=sharing.locator(`.fleet-rule[data-fleet="${FAM}"][data-kind="question"]`);assert.deepEqual(await rule.locator('[data-fleet-rule]').evaluateAll(x=>x.map(i=>i.value)),['ask','never']);
  assert.match(await rule.innerText(),/Only what you send goes/);
  // Always for one person only, with what it does
  await page.locator('.fleet-tabs [data-fleet-pane="sharing"]').click();await rule.locator('.fleet-ex-add summary').click();assert.match(await rule.innerText(),/Always: ordinary answers go by themselves.* ask you first, but it can miss one\./);
  await rule.locator('[data-fleet-ex-member]').selectOption('fm_robin');calls.length=0;await acted(()=>rule.locator('[data-fleet-ex-rule="always"]').click(),'fleet_rule');
  assert.deepEqual(calls.find(c=>c.action==='fleet_rule'),{action:'fleet_rule',args:{fleet:FAM,member_id:'fm_robin',kind:'question',rule:'always'}});
  // Activity: an answer that went by itself, with the way back
  await page.locator('.fleet-tabs [data-fleet-pane="activity"]').click();const line=page.locator('.act-embed .act-row').first();await line.waitFor();
  assert.match(await line.innerText(),/Answered by itself/);calls.length=0;await line.getByRole('button',{name:'Ask me first'}).click();await landed('family_question_ask_first');
  assert.deepEqual(calls.find(c=>c.action==='family_question_ask_first'),{action:'family_question_ask_first',args:{id:'q_'+'7'.repeat(16)}});
  const fits=await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
  assert.ok(fits,`${scheme} ${width}px scrolls sideways`);
  // A notification's Stop opens the to-do and stops it at once, without asking again
  calls.length=0;dialogs=0;await page.goto('about:blank');await page.goto('http://127.0.0.1:'+server.address().port+'/#fleet=q_'+'5'.repeat(16)+'&choice=stop');await landed('fleet_decide');
  assert.deepEqual(calls.find(c=>c.action==='fleet_decide'),{action:'fleet_decide',args:{id:'q_'+'5'.repeat(16),choice:'stop'}});assert.equal(dialogs,0);
  // The phone app's tap, and Stop from a service worker of before (no choice in the link): the to-do opens with Stop on it
  for(const link of ['#chat=fleet-q_'+'5'.repeat(16),'#fleet=q_'+'5'.repeat(16)]){calls.length=0;await page.goto('about:blank');await page.goto('http://127.0.0.1:'+server.address().port+'/'+link);
   await page.locator('#fleet-q_'+'5'.repeat(16)+'.flash').waitFor();assert.ok(await page.locator('#fleet-q_'+'5'.repeat(16)+' [data-fleet-stop]').isVisible());assert.equal(calls.filter(c=>c.action==='fleet_decide').length,0)}
  assert.deepEqual(errors,[]);
 }
 // sw.js hands a notification's Stop on as the link's choice
 const heard={},scope='https://machine.example/',opened=[];
 runInNewContext(readFileSync(new URL('../sw.js',import.meta.url),'utf8'),{self:{addEventListener:(n,f)=>heard[n]=f,registration:{scope},location:{href:scope+'sw.js',origin:'https://machine.example'},
  clients:{matchAll:async()=>[],openWindow:async u=>opened.push(u)}},URL,Date,crypto,caches:{},console});
 for(const action of ['stop','']){let done;heard.notificationclick({action,notification:{close(){},tag:'fleet-q_'+'5'.repeat(16),data:{url:scope+'#fleet=q_'+'5'.repeat(16)}},waitUntil:p=>done=p});await done}
 assert.deepEqual(opened,[scope+'#fleet=q_'+'5'.repeat(16)+'&choice=stop',scope+'#fleet=q_'+'5'.repeat(16)]);
 console.log('family dashboard: ok');
}finally{await browser.close();server.close()}
