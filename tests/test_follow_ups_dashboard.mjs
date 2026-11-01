import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Automated follow-ups on the dashboard (follow_ups.py): a board's ready follow-ups are ONE to-do ("3 follow-ups ready
// for …") that opens a fast review: j/k or arrows move, Enter sends (confirm_action), e edits (revise_draft), s skips
// (decide reject), Send all checked sends the checked ones; a project's own follow-up stays a normal to-do. The board
// header says "Follow-ups on, next …" (or "Follow-ups off"), a stage with no-reply projects "Follow them up", a tile "Next follow-up: …", the project page what went out. The settings panel
// for a board and for a project posts follow_up_save. Nothing is wider than the screen. FOLLOW_UPS_SHOT=<dir> writes
// screenshots at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()+n*864e5).toISOString();
const draft=(i,body,extra={})=>({kind:'email',label:'Send',account_id:'work',from:'owner@example.com',to:[`person${i}@client.example`],subject:'Re: Alpha',body,revision:'r'+i,...extra});
const card=(i,project,body,extra={})=>({id:('f'+i).padEnd(16,'0'),title:'Follow up with '+project,body:'No reply for 4 days. Follow-up 1 of at most 3.',status:'prepared',early:1,scope:'work',event_ids:[i],
 created_at:day(-0.1),next_action:draft(i,body),follow_up:{project,project_id:'project:'+i,board:'Alpha testers',group:'board:1',n:1,max:3,channel:'email',auto:false,state:'open'},...extra});
let suggestions,progress=[];
const reset=()=>{progress=[];suggestions=[card(1,'Acme pilot','Hi Sam, did the alpha build install fine on your side? Happy to do a quick call this week.'),
 card(2,'Bolt trial','Hi Kim, here is the short guide I mentioned. Anything blocking you so far?'),
 card(3,'Cobalt rollout','Hi Lee, any first impressions from the team? One question: which inbox did you connect?',{follow_up:{project:'Cobalt rollout',project_id:'project:3',board:'Alpha testers',group:'board:1',n:2,max:3,channel:'email',auto:false,state:'open'}}),
 card(4,'Delta renewal','Hi Ana, checking whether the renewal quote reached you.',{follow_up:{project:'Delta renewal',project_id:'project:4',board:null,group:null,n:1,max:2,channel:'email',auto:false,state:'open'}}),
 {id:'other00000000000',title:'Reply to the venue about Friday',body:'They asked for the final headcount.',status:'pending',scope:'work',event_ids:[9],created_at:day(-0.2)}]};
reset();
const stages=[{name:'Invited'},{name:'Testing'},{name:'Live'},{name:'Stalled or declined',side:true}];
const proj=(i,name,stage,follow_up)=>({id:'project:'+i,name,stage,reason:'they replied to the invite',by:'review',at:day(-3),event_id:100+i,first:false,days:3,no_reply_days:0,org:{name,logo:null},follow_up});
let boardsNow=null;
const boards=[{id:1,name:'Alpha testers',stages,side:true,visibility:'team',follow_ups:{on:true,next_at:day(2)},projects:[
 proj(1,'Acme pilot','Invited',{state:'open',n:1,max:3}),proj(2,'Bolt trial','Testing',{state:'open',n:1,max:3}),proj(5,'Ember labs','Testing',{state:'waiting',next_at:day(2),n:1,max:3}),
 proj(6,'Fjord studio','Invited',{state:'stopped',end:{n:3,moved:0,judged:0,at:day(-1)}}),proj(7,'Grove co','Live')]}];
const detail={id:'project:5',kind:'project',name:'Ember labs',state:'active',strength:1,last_at:day(-2),signals:3,ids:[],links:[],recent:[],around:[],open:{},
 board:{board:'Alpha testers',stage:'Testing',next:null,visibility:null,board_visibility:'team',stages:['Invited','Testing','Live'],moves:[{stage:'Testing',reason:'they installed the build',source:'review',at:day(-6),event_id:105}]},
 follow_up:{on:true,source:'board',next_at:day(2),state:'waiting',n:2,max:3,ends:[],activity:[{n:1,of_max:3,channel:'email',state:'sent',auto:1,created_at:day(-3),closed_at:day(-3)}]}};
const panel=(scope,id)=>scope==='board'?{scope:'board',id:1,name:'Alpha testers',stalled:true,careful:false,channels:['email','linkedin','whatsapp'],
  stages:[{name:'Invited',open:true},{name:'Testing',open:true},{name:'Live',open:false}],workdays_default:true,settings:{on:true,days:3,max_days:7,min:1,max:3,stages:{},channels:null,switch:false,auto:false,stall:null,workdays:null}}
 :{scope:'project',id:+String(id).replace('project:',''),name:'Ember labs',own:false,stalled:true,careful:true,channels:['email'],board:{id:1,name:'Alpha testers',on:true},
  settings:{on:true,days:3,max_days:7,min:1,max:3,stages:{},channels:null,switch:false,auto:false,stall:null}};
let calls=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions,follow_up_progress:progress,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');res.end(JSON.stringify(n?detail:{projects:[],people:[],quiet:[],new:[],orgs:[],boards:boardsNow||boards}));return}
 if(req.method==='POST'&&url.pathname==='/api/action'){const c=JSON.parse(body||'{}');calls.push(c);const a=c.args||{};
  if(c.action==='follow_up_settings'||c.action==='follow_up_save'){const v=panel(a.scope,a.id);if(boardsNow&&a.scope==='board')v.settings.on=false;res.end(JSON.stringify(v));return}
  if(c.action==='revise_draft'){const s=suggestions.find(x=>x.id===a.suggestion_id);s.next_action={...s.next_action,body:a.body,revision:a.revision+'e'};res.end(JSON.stringify({revision:a.revision+'e',body:a.body}));return}
  if(c.action==='confirm_action'){suggestions=suggestions.filter(x=>x.id!==a.suggestion_id);res.end(JSON.stringify({status:'queued'}));return}
  if(c.action==='follow_up_change'){const changing=[];for(const id of a.ids){const s=suggestions.find(x=>x.id===id);if(!s)continue;changing.push({id,revision:s.next_action.revision});
   suggestions=suggestions.map(x=>x.id===id?{...x,status:'instructions',preparation_status:'queued'}:x)}res.end(JSON.stringify({changing,skipped:[]}));return}
  if(c.action==='follow_up_stop'){progress=progress.map(p=>p.batch===a.batch?{...p,going:false,done:p.total,stopped:p.total-p.sent}:p);res.end(JSON.stringify({stopped:1,sent:1}));return}
  if(c.action==='follow_up_end'){suggestions=suggestions.filter(x=>x.id!==a.id);res.end(JSON.stringify({id:a.id,state:'stopped'}));return}
  if(c.action==='follow_up_bring_back'){res.end(JSON.stringify({id:a.id,status:'prepared'}));return}
  if(c.action==='decide'){suggestions=suggestions.filter(x=>x.id!==c.args.suggestion_id);res.end(JSON.stringify({status:'rejected'}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const open=async(width,height,scheme='light')=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',colorScheme:scheme});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));await page.goto(base);
 await page.locator('#suggestions article, #suggestions .all-clear').first().waitFor();return {context,page}};
const toBoard=async page=>{await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());await page.locator('#people-view').waitFor({state:'attached'});
 await page.evaluate(()=>document.querySelector('[data-graph-sub="projects"]').click());await page.locator('#people-view .pboard').first().waitFor()};
const fits=(page,where)=>page.evaluate(()=>({page:document.documentElement.scrollWidth,vw:innerWidth})).then(s=>assert.ok(s.page<=s.vw,`${where}: wider than the screen ${JSON.stringify(s)}`));
const shot=async(page,name,target)=>{if(!process.env.FOLLOW_UPS_SHOT)return;const path=`${process.env.FOLLOW_UPS_SHOT}/${name}.png`;if(target)await target.screenshot({path});else await page.screenshot({path})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 {const {context,page}=await open(1440,900);
  // One to-do for the board's three, the project's own as a normal to-do, and the other to-do as it was
  const group=page.locator('#suggestions .fu-group');await group.waitFor();
  assert.equal(await group.count(),1);
  assert.equal((await group.locator('h3').textContent()).trim(),'3 follow-ups ready for Alpha testers');
  assert.match(await group.locator('.fu-names').textContent(),/^Acme pilot, Bolt trial and Cobalt rollout$/);
  assert.equal(await page.locator('#task-f100000000000000').count(),0);
  assert.equal(await page.locator('#task-f400000000000000').count(),1);
  assert.equal((await page.locator('#badge-inbox').textContent()).trim(),'3');  // the group, Delta's own and the other one
  assert.deepEqual(await page.locator('#side-cards a').evaluateAll(l=>l.map(a=>a.textContent)),['3 follow-ups ready for Alpha testers','Follow up with Delta renewal','Reply to the venue about Friday']);
  assert.match(await page.locator('#suggestions').evaluate(()=>document.querySelector('.app-side, body').textContent),/2 ready for you · 1 to decide/);
  await fits(page,'1440 to-dos');await shot(page,'grouped-todo-1440-light');
  // The fast review: the first is current; j moves, Enter sends it (one confirm_action with its revision)
  calls=[];await group.locator('[data-fu-review]').last().click();
  const dlg=page.locator('#fu-review');await dlg.locator('.fr-item').first().waitFor();
  assert.equal(await dlg.locator('.fr-item').count(),3);
  assert.equal(await dlg.locator('.fr-item.on b').textContent(),'Acme pilot');
  assert.equal((await dlg.locator('[data-fr-all]').textContent()).trim(),'Send all checked (3)');
  await shot(page,'review-1440-light');
  await page.keyboard.press('j');assert.equal(await dlg.locator('.fr-item.on b').textContent(),'Bolt trial');
  await page.keyboard.press('ArrowUp');assert.equal(await dlg.locator('.fr-item.on b').textContent(),'Acme pilot');
  await page.keyboard.press('Enter');await page.waitForFunction(()=>document.querySelectorAll('#fu-review .fr-item').length===2);
  assert.deepEqual(calls.map(c=>[c.action,c.args.suggestion_id,c.args.revision]),[['confirm_action','f100000000000000','r1']]);
  // e edits in place, Ctrl+Enter saves it (revise_draft), and the edited text is what Send sends
  calls=[];assert.equal(await dlg.locator('.fr-item.on b').textContent(),'Bolt trial');
  await page.keyboard.press('e');const box=dlg.locator('.fr-edit');await box.waitFor();await box.fill('Hi Kim, short one: did the guide help?');await shot(page,'review-edit-1440-light');
  await page.keyboard.press('Control+Enter');await dlg.locator('.fr-edit').waitFor({state:'detached'});
  assert.deepEqual(calls.map(c=>c.action),['revise_draft']);assert.match(await dlg.locator('.fr-item.on .fr-body').textContent(),/did the guide help\?/);
  // s skips: the draft stays, unchecked, dimmed and at the bottom, "Skipped" with an Undo; nothing is decided yet
  await page.keyboard.press('k');assert.equal(await dlg.locator('.fr-item.on b').textContent(),'Bolt trial');
  calls=[];await page.keyboard.press('s');await dlg.locator('.fr-item.skipped').waitFor();
  assert.deepEqual(await dlg.locator('.fr-item b').evaluateAll(l=>l.map(b=>b.textContent)),['Cobalt rollout','Bolt trial']);
  assert.equal(await dlg.locator('.fr-item.on b').textContent(),'Cobalt rollout');
  assert.equal(await dlg.locator('.fr-item.skipped [data-fr-check]').isChecked(),false);assert.equal(await dlg.locator('.fr-item.skipped [data-fr-check]').isDisabled(),true);
  assert.equal((await dlg.locator('.fr-item.skipped .fr-state').textContent()).trim(),'SkippedUndo');
  assert.ok(+(await dlg.locator('.fr-item.skipped .fr-body').evaluate(el=>getComputedStyle(el).opacity))<1);
  assert.equal((await dlg.locator('[data-fr-all]').textContent()).trim(),'Send all checked (1)');assert.deepEqual(calls,[]);
  await shot(page,'review-skipped-1440-light');
  // Undo puts it back where it was, checked; s again skips it
  await dlg.locator('[data-fr-unskip]').click();await dlg.locator('.fr-item.skipped').waitFor({state:'detached'});
  assert.deepEqual(await dlg.locator('.fr-item b').evaluateAll(l=>l.map(b=>b.textContent)),['Bolt trial','Cobalt rollout']);
  assert.equal((await dlg.locator('[data-fr-all]').textContent()).trim(),'Send all checked (2)');
  await page.keyboard.press('s');await dlg.locator('.fr-item.skipped').waitFor();
  // Send all checked sends the rest; with only skipped ones left the review closes, and only then is the skip final
  calls=[];await dlg.locator('[data-fr-all]').click();await dlg.waitFor({state:'hidden'});await page.waitForFunction(()=>true);
  await page.waitForTimeout(100);
  assert.deepEqual(calls.filter(c=>c.action!=='client_error').map(c=>[c.action,c.args.suggestion_id,c.args.revision||c.args.choice]),[['confirm_action','f300000000000000','r3'],['decide','f200000000000000','reject']]);
  // The board: "Follow-ups on, next …" in the header, a tile's next follow-up, ready and a round that ended quietly
  reset();await toBoard(page);
  assert.match(await page.locator('.board-sub .fu-state').textContent(),/^Follow-ups on, next \w{3}$/);
  assert.match(await page.locator('.tile[data-node="project:5"] .tile-fu').textContent(),/^Next follow-up: \w{3}$/);
  assert.equal(await page.locator('.tile[data-node="project:1"] .tile-fu').textContent(),'Follow-up ready');
  assert.equal(await page.locator('.tile[data-node="project:6"] .tile-fu').textContent(),'No reply after 3 follow-ups');
  assert.equal(await page.evaluate(()=>fuNoReply(0)),'Follow-ups stopped');  // stopped before any went out
  assert.equal(await page.locator('.tile[data-node="project:7"] .tile-fu').count(),0);
  await fits(page,'1440 board');await shot(page,'board-1440-light');
  // The board's settings panel: both pairs on two rows, stages behind Customize, channels, Stalled, asking first
  calls=[];await page.locator('.board-sub .fu-state').click();const fu=page.locator('#fu-dialog');await fu.locator('[name=days]').waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args.scope,c.args.id]),[['follow_up_settings','board','1']]);
  assert.match(await fu.locator('.fu-row').first().textContent(),/^Wait\s+to\s+days without a reply$/);
  assert.deepEqual(await fu.locator('.fu-row input').evaluateAll(l=>l.map(i=>i.value)),['3','7','1','3']);
  assert.equal(await fu.locator('[name=auto][value=ask]').isChecked(),true);assert.equal(await fu.locator('[name=stall]').isChecked(),true);
  assert.equal(await fu.locator('[name=workdays]').isChecked(),true);  // Only on workdays: on for a Work board until they choose
  assert.equal((await fu.locator('label:has([name=workdays])').textContent()).trim(),'Only on workdays');
  await shot(page,'settings-board-1440-light',fu);
  await fu.locator('[data-fu-custom]').click();assert.equal(await fu.locator('[data-fu-stage]').count(),3);
  assert.deepEqual(await fu.locator('[data-fu-stage]').evaluateAll(l=>l.map(i=>i.checked)),[true,true,false]);
  await fu.locator('[data-fu-sdays="1"]').fill('5');await fu.locator('[name=max]').fill('2');await fu.locator('[name=ch][value=whatsapp]').uncheck();
  await fu.locator('[name=switch]').check();await fu.locator('[name=auto][value=auto]').check();await fu.locator('[name=workdays]').uncheck();
  assert.equal((await fu.locator('.fu-send .fu-note').textContent()).trim(),'Anything unusual still waits for you.');
  await shot(page,'settings-board-custom-1440-light',fu);
  calls=[];await fu.locator('button.primary').click();await fu.waitFor({state:'hidden'});
  const save=calls.find(c=>c.action==='follow_up_save');
  assert.deepEqual(save.args,{scope:'board',id:1,settings:{on:true,days:3,max_days:7,min:1,max:2,channels:['email','linkedin'],switch:true,auto:true,stall:true,workdays:false,
   stages:{Invited:{on:true},Testing:{on:true,days:5},Live:{on:false}}}});
  // A project's page: what went out by itself, and its own panel (Like its board; Careful asks always)
  await page.locator('.tile[data-node="project:5"]').click();await page.locator('.graph-fu').waitFor();
  assert.match(await page.locator('.graph-fu').textContent(),/Next follow-up: \w{3} Follow-ups…/);
  assert.match(await page.locator('.graph-fu ol').textContent(),/Follow-up 1 sent automatically \(Email\)/);
  await shot(page,'project-next-1440-light',page.locator('.graph-detail'));
  calls=[];await page.locator('.graph-fu [data-fu-open]').click();await fu.locator('[name=mode]').first().waitFor();
  assert.equal(await fu.locator('[name=mode][value=board]').isChecked(),true);assert.equal(await fu.locator('[name=days]').isDisabled(),true);
  await fu.locator('[name=mode][value=on]').check();assert.equal(await fu.locator('[name=auto][value=auto]').isDisabled(),true);
  assert.equal((await fu.locator('.fu-send .fu-note').textContent()).trim(),'Careful mode is on, so it always asks.');
  assert.equal(await fu.locator('[name=switch]').count(),0);  // one channel connected: nothing to switch to
  await shot(page,'settings-project-1440-light',fu);
  calls=[];await fu.locator('[name=mode][value=board]').check();await fu.locator('button.primary').click();await fu.waitFor({state:'hidden'});
  assert.deepEqual(calls.find(c=>c.action==='follow_up_save').args,{scope:'project',id:5,settings:{inherit:true}});
  await context.close()}
 // Send all checked went out spaced (30-45 s per mailbox): the board's queued ones are one progress to-do, "Sending 3 of 8…",
 // also after a reload, then "Sent 8"; a project's own follow-up that's ready stays as it was, and nothing is wider than the screen
 for(const [width,height] of [[1440,900],[390,844]]){reset();
  const going=s=>({...s,action_status:{status:'queued'},next_actions:[{...s.next_action,state:{status:'queued'}}]});
  suggestions=suggestions.map(s=>s.follow_up?.group==='board:1'?going(s):s);
  progress=[{group:'board:1',board:'Alpha testers',total:8,done:2,sent:2,going:true,done_at:new Date(Date.now()+4*60e3).toISOString()}];
  const {context,page}=await open(width,height);const sending=page.locator('#suggestions .fu-sending');await sending.waitFor();
  assert.equal(await sending.count(),1);assert.equal(await page.locator('#suggestions .fu-group').count(),0);
  assert.equal((await sending.locator('h3').textContent()).trim(),'Follow-ups for Alpha testers');
  assert.equal((await sending.locator('.fu-progress').textContent()).trim(),'Sending 3 of 8…');
  assert.equal(await sending.locator('[data-fu-dismiss]').count(),0);  // no × while sending
  assert.match((await sending.locator('.fu-spaced').textContent()).trim(),/^Spaced out so they don’t look automated · done around \d{1,2}:\d{2}( [AP]M)?$/);
  assert.equal(await sending.locator('.fu-progress').getAttribute('role'),'status');
  assert.equal(await page.locator('#task-f100000000000000').count(),0);assert.equal(await page.locator('#task-f400000000000000').count(),1);
  assert.equal(await page.locator('#side-cards a').evaluateAll(l=>l.filter(a=>/Alpha testers/.test(a.textContent)).length),0);
  await fits(page,width+' sending');await shot(page,`sending-${width}-light`);
  await page.reload();await sending.waitFor();assert.equal((await sending.locator('.fu-progress').textContent()).trim(),'Sending 3 of 8…');
  progress=[{group:'board:1',board:'Alpha testers',total:8,done:8,sent:8,going:false}];suggestions=suggestions.filter(s=>s.follow_up?.group!=='board:1');
  await page.reload();await sending.waitFor();assert.equal((await sending.locator('.fu-progress').textContent()).trim(),'Sent 8');
  assert.equal(await sending.locator('.fu-bar').count(),0);await shot(page,`sent-${width}-light`);
  progress=[{group:'board:1',board:'Alpha testers',total:8,done:8,sent:7,going:false}];await page.reload();await sending.waitFor();
  assert.equal((await sending.locator('.fu-progress').textContent()).trim(),'Sent 7 of 8');
  // Done: its × dismisses that batch's card, also after a reload; another batch shows again
  progress=[{group:'board:1',board:'Alpha testers',batch:'board:1@b1-'+width,total:8,done:8,sent:8,going:false}];await page.reload();await sending.waitFor();
  const x=sending.locator('[data-fu-dismiss]');assert.equal(await x.getAttribute('aria-label'),'Dismiss');await shot(page,`sent-dismiss-${width}-light`);
  await x.click();await sending.waitFor({state:'detached'});
  await page.reload();await page.locator('#suggestions article').first().waitFor();assert.equal(await page.locator('#suggestions .fu-sending').count(),0);
  progress=[{group:'board:1',board:'Alpha testers',batch:'board:1@b2-'+width,total:3,done:3,sent:3,going:false}];await page.reload();await sending.waitFor();
  assert.equal((await sending.locator('.fu-progress').textContent()).trim(),'Sent 3');
  await context.close()}
 // Held right before it went (a new message in the thread since the draft, or the thread couldn't be checked): the batch says
 // "Sent 5 · 1 held (new message)", the held one is back in the board's to-do with its line, ready to send again; a project's
 // own follow-up that couldn't be checked says so on its to-do. Light and dark, 1440 and 390.
 for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]){reset();
  const held=(s,error)=>({...s,action_status:{status:'blocked',error},next_actions:[{...s.next_action,state:{status:'blocked',error}}]});
  suggestions=suggestions.filter(s=>!['f200000000000000','f300000000000000'].includes(s.id)).map(s=>s.id==='f100000000000000'?held(s,'Not sent: new message in the thread.')
   :s.id==='f400000000000000'?held(s,'Couldn’t check the thread, try again.'):s);
  progress=[{group:'board:1',board:'Alpha testers',total:6,done:6,sent:5,going:false,held:1,held_new:1}];
  const {context,page}=await open(width,height,scheme);const sending=page.locator('#suggestions .fu-sending');await sending.waitFor();
  assert.equal((await sending.locator('.fu-progress').textContent()).trim(),'Sent 5 · 1 held (new message)');
  const group=page.locator('#suggestions .fu-group');assert.equal((await group.locator('h3').textContent()).trim(),'1 follow-up ready for Alpha testers');
  assert.match(await page.locator('#task-f400000000000000').textContent(),/Couldn’t check the thread, try again\./);
  assert.equal(await page.locator('#task-f400000000000000 [data-smart]').count(),1);  // still ready: Send checks again
  await fits(page,width+' held');await shot(page,`held-${width}-${scheme}`);
  await group.locator('button.primary').click();const dlg=page.locator('#fu-review');await dlg.locator('.fr-item').first().waitFor();
  assert.equal((await dlg.locator('.fr-held').textContent()).trim(),'Not sent: new message in the thread.');
  assert.equal(await dlg.locator('[data-fr-send]').isEnabled(),true);
  // A new message in the thread: left out of Send all checked, and its Send is a plain one
  assert.equal(await dlg.locator('[data-fr-check]').isChecked(),false);
  assert.equal((await dlg.locator('[data-fr-all]').textContent()).trim(),'Send all checked (0)');
  assert.equal(await dlg.locator('[data-fr-send]').evaluate(b=>b.classList.contains('primary')),false);
  await fits(page,width+' held review');await shot(page,`held-review-${width}-${scheme}`);
  await page.keyboard.press('Escape');await dlg.waitFor({state:'hidden'});
  // Couldn't check the thread: stays checked, since trying again is the point
  suggestions=suggestions.map(s=>s.id==='f100000000000000'?held(s,'Couldn’t check the thread, try again.'):s);await page.reload();
  await group.locator('button.primary').click();await dlg.locator('.fr-item').first().waitFor();
  assert.equal((await dlg.locator('.fr-held').textContent()).trim(),'Couldn’t check the thread, try again.');
  assert.equal(await dlg.locator('[data-fr-check]').isChecked(),true);
  assert.equal((await dlg.locator('[data-fr-all]').textContent()).trim(),'Send all checked (1)');
  assert.equal(await dlg.locator('[data-fr-send]').evaluate(b=>b.classList.contains('primary')),true);
  await shot(page,`unchecked-review-${width}-${scheme}`);
  progress=[{group:'board:1',board:'Alpha testers',total:3,done:3,sent:1,going:false,held:2,held_new:1}];await page.reload();await sending.waitFor();
  assert.equal((await sending.locator('.fu-progress').textContent()).trim(),'Sent 1 · 2 held');
  await context.close()}
 // Send all checked: a draft with several possible senders goes out from the one it shows ("From …"); only one with no
 // recipient yet (to_options) is left for a send on its own. A queued follow-up whose draft sits in a menu (its state on
 // the draft, no action_status) leaves the ready to-do at once.
 {reset();
  const menu=(s,st)=>{const d={...s.next_action,...(st?{state:{status:st}}:{})};return {...s,next_action:{kind:'menu',actions:[s.next_action]},next_actions:[d]}};
  suggestions=suggestions.map(s=>s.id==='f100000000000000'?{...s,next_action:draft(1,s.next_action.body,{from_options:['owner@example.com','sales@example.com']})}
   :s.id==='f200000000000000'?{...s,next_action:draft(2,s.next_action.body,{to:[],to_options:['kim@other.example','ops@other.example']})}
   :s.id==='f300000000000000'?menu(s,'queued'):s);
  const {context,page}=await open(1440,900);const group=page.locator('#suggestions .fu-group');await group.waitFor();
  assert.equal((await group.locator('h3').textContent()).trim(),'2 follow-ups ready for Alpha testers');  // Cobalt is queued: not ready any more
  await group.locator('button.primary').click();const dlg=page.locator('#fu-review');await dlg.locator('.fr-item').first().waitFor();
  assert.equal(await dlg.locator('.fr-item').count(),2);
  assert.equal((await dlg.locator('.fr-item').first().locator('.fr-to').textContent()).trim(),'To person1@client.example · From owner@example.com');
  calls=[];await dlg.locator('[data-fr-all]').click();await dlg.locator('[data-fr-error]:not([hidden])').waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args.suggestion_id,c.args.sender]),[['confirm_action','f100000000000000',undefined]]);
  assert.equal((await dlg.locator('[data-fr-error]').textContent()).trim(),'1 needs you to pick who gets it: send it on its own.');
  assert.deepEqual(await dlg.locator('.fr-item b').allTextContents(),['Bolt trial']);
  await shot(page,'send-all-from-1440-light');
  // The same menu-shaped follow-up before it's queued is ready again
  await page.keyboard.press('Escape');suggestions=suggestions.map(s=>s.id==='f300000000000000'?menu(card(3,'Cobalt rollout','Hi Lee')):s);await page.reload();
  await group.waitFor();assert.equal((await group.locator('h3').textContent()).trim(),'2 follow-ups ready for Alpha testers');  // Bolt and Cobalt
  await context.close()}
 // Drafts being written: the board's follow-ups are already one to-do ("Follow-ups for …", "Writing 3 follow-ups…"), never
 // one per email in Preparing, the sidebar or a to-do's chat; once one is written it moves to Ready with the rest still writing
 for(const [width,height] of [[1440,900],[1440,700],[390,844]]){reset();
  const writing=s=>s.follow_up?.group==='board:1'?{...s,status:'accepted',next_action:null,preparation_status:'running'}:s;
  suggestions=suggestions.map(writing);
  const {context,page}=await open(width,height);const group=page.locator('#suggestions .fu-group');await group.waitFor();
  assert.equal(await group.count(),1);
  assert.equal((await group.locator('h3').textContent()).trim(),'Follow-ups for Alpha testers');
  assert.equal((await group.locator('.fu-progress').textContent()).trim(),'Writing 3 follow-ups…');
  assert.equal(await group.locator('[data-fu-review]').count(),0);  // nothing to review yet
  assert.equal(await page.locator('#section-preparing .count').textContent(),'1');
  for(const i of [1,2,3])assert.equal(await page.locator(`#task-f${i}00000000000000`).count(),0);
  assert.equal(await page.locator('#side-cards a').evaluateAll(l=>l.filter(a=>/^Follow up with (Acme|Bolt|Cobalt)/.test(a.textContent)).length),0);
  assert.equal((await page.locator('#badge-inbox').textContent()).trim(),'3');
  await fits(page,width+' writing');await shot(page,`writing-${width}x${height}-light`);await group.scrollIntoViewIfNeeded();await shot(page,`writing-card-${width}x${height}-light`,group);
  // A to-do's chat lists the same: the board's follow-ups as one row
  await page.evaluate(()=>{location.hash='#chat=f400000000000000'});await page.locator('.chat-side').waitFor({state:'attached'});
  assert.deepEqual(await page.locator('.chat-side a').evaluateAll(l=>l.map(a=>a.textContent).filter(x=>/Alpha|Acme|Bolt|Cobalt/.test(x))),['Follow-ups for Alpha testers']);
  await shot(page,`writing-chat-${width}x${height}-light`);
  // Its row leads back to the board's to-do
  if(await page.locator('.chat-side [data-fu-card]').isVisible()){await page.locator('.chat-side [data-fu-card]').click();await page.locator('#suggestions .fu-group').waitFor();assert.equal(await page.locator('.chat-side').count(),0)}
  await context.close()}
 {reset();suggestions=suggestions.map(s=>s.id==='f300000000000000'?{...s,status:'accepted',next_action:null,preparation_status:'running'}:s);
  const {context,page}=await open(1440,900);const group=page.locator('#suggestions .fu-group');await group.waitFor();
  assert.equal((await group.locator('h3').textContent()).trim(),'2 follow-ups ready for Alpha testers');
  assert.equal((await group.locator('.fu-progress').textContent()).trim(),'Writing 1 follow-up…');
  assert.equal(await page.locator('#section-preparing').count(),0);await shot(page,'ready-and-writing-card-1440-light',group);
  await group.locator('button.primary').click();const dlg=page.locator('#fu-review');await dlg.locator('.fr-item').first().waitFor();
  assert.equal(await dlg.locator('.fr-item').count(),2);  // only the written ones
  await shot(page,'ready-and-writing-1440-light');await context.close()}
 // One alone is still the board's to-do, and a link to it (its notification) lands there
 {reset();suggestions=suggestions.filter(s=>!['f200000000000000','f300000000000000'].includes(s.id));
  const {context,page}=await open(1440,900);await page.locator('#suggestions .fu-group').waitFor();
  assert.equal((await page.locator('#suggestions .fu-group h3').textContent()).trim(),'1 follow-up ready for Alpha testers');
  assert.equal(await page.locator('#task-f100000000000000').count(),0);
  await page.evaluate(()=>{location.hash='#card=f100000000000000'});await page.waitForFunction(()=>document.querySelector('#suggestions .fu-group.flash'));
  await context.close()}
 // Only follow-ups open (being written, or on their way): their to-do shows, never a blank page; nothing open: All clear
 {reset();suggestions=suggestions.filter(s=>s.follow_up?.group==='board:1').map(s=>({...s,status:'accepted',next_action:null,preparation_status:'running'}));
  const {context,page}=await open(1440,900);await page.locator('#suggestions .fu-group').waitFor();
  assert.equal(await page.locator('#suggestions .all-clear').count(),0);
  suggestions=suggestions.map(s=>({...s,status:'prepared',next_action:draft(1,'Hi'),preparation_status:'done',action_status:{status:'queued'},next_actions:[{...draft(1,'Hi'),state:{status:'queued'}}]}));
  progress=[{group:'board:1',board:'Alpha testers',total:3,done:0,sent:0,going:true}];await page.reload();
  await page.locator('#suggestions .fu-sending').waitFor();assert.equal(await page.locator('#suggestions .all-clear').count(),0);
  progress=[];suggestions=[];await page.reload();await page.locator('#suggestions .all-clear').waitFor();
  await context.close()}
 // The review reads top to bottom: every draft at full height, the list the only thing that scrolls (nothing inside a
 // draft does), the footer in reach; j moves and scrolls the current one into view, a poll keeps where the list is and
 // changes only the draft that changed
 const para='Thanks again for the call last week. I wrote up the notes and the two options we talked about, so the team can pick one before the next sprint starts.';
 const many=n=>Array.from({length:n},(_,i)=>card(10+i,['Acme pilot','Bolt trial','Cobalt rollout','Delta renewal','Ember labs','Fjord studio','Grove co','Harbor works'][i],
  `Hi ${['Sam','Kim','Lee','Ana','Bo','Cy','Di','Ed'][i]},\n\n`+Array.from({length:1+(i*3)%5},()=>para).join('\n\n')+'\n\nRegards,\n\nAlex'));
 const scrollers=page=>page.evaluate(()=>[...document.querySelectorAll('#fu-review, #fu-review *')].filter(el=>{const o=getComputedStyle(el).overflowY;return (o==='auto'||o==='scroll')&&el.scrollHeight>el.clientHeight+1}).map(el=>el.className||el.id));
 const inner=page=>page.evaluate(()=>[...document.querySelectorAll('#fu-review .fr-item, #fu-review .fr-item *')].filter(el=>{const o=getComputedStyle(el).overflowY;return o==='auto'||o==='scroll'||el.scrollHeight>el.clientHeight+1&&o!=='visible'}).map(el=>el.className||el.tagName));
 for(const [width,height] of [[1440,900],[1440,700],[390,844]])for(const scheme of ['light','dark'])for(const n of [3,8]){
  reset();suggestions=[...many(n),...suggestions.filter(s=>!s.follow_up)];const {context,page}=await open(width,height,scheme);
  await page.locator('#suggestions .fu-group button.primary').click();const dlg=page.locator('#fu-review');await dlg.locator('.fr-item').first().waitFor();
  await page.mouse.move(2,2);await shot(page,`review-${n}-${width}x${height}-${scheme}`);
  assert.equal(await dlg.locator('.fr-item').count(),n);await fits(page,`${width}x${height} review ${n}`);
  assert.deepEqual(await inner(page),[],`${width}x${height} ${n}: something inside a draft scrolls`);
  const sc=await scrollers(page);assert.ok(sc.length<=1&&sc.every(c=>c==='fr-list'),`${width}x${height} ${n}: scrollers ${JSON.stringify(sc)}`);
  if(n===8)assert.deepEqual(sc,['fr-list'],`${width}x${height}: the list scrolls`);
  // every draft's text in full, the dialog and its Send all checked on the screen
  assert.deepEqual(await dlg.locator('.fr-body').evaluateAll(l=>l.map(p=>p.scrollHeight<=p.clientHeight+1)),Array(n).fill(true));
  const box=await dlg.evaluate(d=>{const r=d.getBoundingClientRect(),b=d.querySelector('[data-fr-all]').getBoundingClientRect();return {top:r.top,bottom:r.bottom,btop:b.top,bbottom:b.bottom,vh:innerHeight}});
  assert.ok(box.top>=0&&box.bottom<=box.vh+1&&box.btop>=box.top&&box.bbottom<=box.vh,`${width}x${height} ${n}: dialog or footer off screen ${JSON.stringify(box)}`);
  if(width<600)assert.ok(box.bottom-box.top>=box.vh-1,`390 ${n}: the review is a full-height sheet`);
  // Send/Edit/Skip only on the current one (or under the pointer), the checkboxes on every one
  assert.equal(await dlg.locator('.fr-actions').evaluateAll(l=>l.filter(a=>getComputedStyle(a).visibility==='visible').length),1);
  assert.equal(await dlg.locator('[data-fr-check]:visible').count(),n);
  if(n===8){
   // j moves in place (same nodes, no redraw) and brings the current one into view
   const first=await dlg.locator('.fr-list').elementHandle();for(let i=0;i<5;i++)await page.keyboard.press('j');
   assert.equal(await dlg.locator('.fr-item.on b').textContent(),'Fjord studio');
   assert.equal(await page.evaluate(el=>el.isConnected,first),true,'j redrew the list');
   await page.waitForFunction(()=>{const l=document.querySelector('#fu-review .fr-list').getBoundingClientRect(),r=document.querySelector('#fu-review .fr-item.on').getBoundingClientRect();return r.top>=l.top-1&&r.top<l.bottom-20});
   await page.waitForTimeout(400);await shot(page,`review-8-moved-${width}x${height}-${scheme}`);
   if(width>600){const hov=dlg.locator('.fr-item:not(.on)').last();await hov.hover();assert.equal(await hov.locator('.fr-actions').evaluate(a=>getComputedStyle(a).visibility),'visible');await shot(page,`review-8-hover-${width}x${height}-${scheme}`);await page.mouse.move(2,2)}
   // a poll that changes nothing leaves the list alone; one that changes a draft redraws it at the same spot
   const list=dlg.locator('.fr-list');await list.evaluate(l=>{l.scrollTop=Math.min(260,l.scrollHeight-l.clientHeight)});const at=await list.evaluate(l=>l.scrollTop);
   await page.evaluate(()=>refresh());assert.equal(await page.evaluate(el=>el.isConnected,first),true,'a poll with no changes redrew the list');
   suggestions=suggestions.map(s=>s.id==='f130000000000000'?{...s,next_action:{...s.next_action,body:'Hi Ana, a fresh line.',revision:'r13b'}}:s);
   await page.evaluate(()=>refresh());await dlg.locator('.fr-body',{hasText:'a fresh line'}).waitFor();
   assert.equal(await page.evaluate(el=>el.isConnected,first),true,'a changed draft redrew the whole list');assert.ok(Math.abs(await list.evaluate(l=>l.scrollTop)-at)<=1,'the poll moved the list');
   assert.equal(await dlg.locator('.fr-item.on b').textContent(),'Fjord studio')}
  await context.close()}
 // Follow-ups off: the board's line says "Follow-ups off" and opens the same settings; a stage with no-reply projects offers
 // "Follow them up", which opens them with on ticked and that stage on (Live isn't an open stage, so it's customized to on).
 // Not with follow-ups on, not in a stage without no-reply projects, never on a Team board (not theirs to change).
 {const stuck=(i,name,stage)=>({...proj(i,name,stage),no_reply_days:12});
  const off={id:1,name:'Alpha testers',stages,side:true,visibility:'team',follow_ups:{on:false,next_at:null},
   projects:[stuck(1,'Acme pilot','Testing'),stuck(2,'Bolt trial','Testing'),proj(3,'Cobalt rollout','Invited'),stuck(4,'Delta renewal','Live')]};
  const team={id:9,name:'Team pipeline',team:true,stages,visibility:'team',owner_name:'Sam',projects:[stuck(11,'Hollow inc','Testing')]};
  for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]){
   reset();boardsNow=[off];const {context,page}=await open(width,height,scheme);await toBoard(page);
   assert.equal((await page.locator('.board-sub .fu-state').textContent()).trim(),'Follow-ups off');
   await fits(page,width+' board off');await shot(page,`board-off-${width}-${scheme}`);
   if(width>600){
    assert.deepEqual(await page.locator('.lane').evaluateAll(l=>l.map(x=>[x.dataset.lane,x.querySelector('.fu-nudge')?.textContent||''])),
     [['Invited',''],['Testing','Follow them up'],['Live','Follow them up'],['Stalled or declined','']]);
    assert.match(await page.locator('.lane[data-lane="Testing"] .lane-sum').textContent(),/^2 with no reply in 10\+ days · Follow them up$/);
    await shot(page,`lane-nudge-${width}-${scheme}`,page.locator('.lane[data-lane="Testing"]'))}
   else{assert.equal(await page.locator('.lane.on .fu-nudge').count(),0);  // Invited: no no-reply projects
    await page.locator('[data-stage-tab="Testing"]').click();await page.locator('.lane.on[data-lane="Testing"] .fu-nudge').waitFor();
    await fits(page,'390 nudge');await shot(page,`lane-nudge-${width}-${scheme}`)}
   // The line opens the board's settings as they are
   calls=[];await page.locator('.board-sub .fu-state').click();const fu=page.locator('#fu-dialog');await fu.locator('[name=on]').waitFor();
   assert.deepEqual(calls.map(c=>[c.action,c.args.scope,c.args.id]),[['follow_up_settings','board','1']]);
   assert.equal(await fu.locator('[name=on]').isChecked(),false);assert.equal(await fu.locator('[name=days]').isDisabled(),true);
   await page.keyboard.press('Escape');await fu.waitFor({state:'hidden'});
   if(width>600){
    // "Follow them up" in Live: on ticked, Live customized on, the open stages as they were; nothing saved before Save
    calls=[];await page.locator('.lane[data-lane="Live"] .fu-nudge').click();await fu.locator('[data-fu-stage]').first().waitFor();
    assert.deepEqual(calls.map(c=>c.action),['follow_up_settings']);
    assert.equal(await fu.locator('[name=on]').isChecked(),true);
    assert.deepEqual(await fu.locator('[data-fu-stage]').evaluateAll(l=>l.map(i=>i.checked)),[true,true,true]);
    await fits(page,width+' nudge settings');await shot(page,`settings-from-nudge-${width}-${scheme}`,fu);
    calls=[];await fu.locator('button.primary').click();await fu.waitFor({state:'hidden'});
    const save=calls.find(c=>c.action==='follow_up_save');assert.equal(save.args.settings.on,true);
    assert.deepEqual(save.args.settings.stages,{Invited:{on:true},Testing:{on:true},Live:{on:true}});
    // In Testing (an open stage): on ticked, the stages stay "All open stages"
    await page.locator('.lane[data-lane="Testing"] .fu-nudge').click();await fu.locator('[name=on]').waitFor();
    assert.equal(await fu.locator('[name=on]').isChecked(),true);assert.equal(await fu.locator('[data-fu-stage]').count(),0);
    assert.match(await fu.locator('.fu-line').textContent(),/All open stages/);
    await page.keyboard.press('Escape');await fu.waitFor({state:'hidden'})}
   else{calls=[];await page.locator('.lane.on .fu-nudge').click();await fu.locator('[name=on]').waitFor();
    assert.equal(await fu.locator('[name=on]').isChecked(),true);await fits(page,'390 nudge settings');await shot(page,`settings-from-nudge-${width}-${scheme}`);
    await page.keyboard.press('Escape');await fu.waitFor({state:'hidden'})}
   // On: no nudge, the line as before
   boardsNow=[{...off,follow_ups:{on:true,next_at:day(2)}}];await page.reload();await toBoard(page);
   assert.match(await page.locator('.board-sub .fu-state').textContent(),/^Follow-ups on, next \w{3}$/);
   assert.equal(await page.locator('.fu-nudge').count(),0);await shot(page,`board-on-${width}-${scheme}`);
   // A Team board: neither the line nor the nudge
   boardsNow=[team];await page.reload();await toBoard(page);
   assert.equal(await page.locator('.board-sub .fu-state').count(),0);assert.equal(await page.locator('.fu-nudge').count(),0);
   await context.close()}
  boardsNow=null}
 // Change: c (or Change…) opens "What should change?" with the scope (all checked, or only this one); Rewrite asks
 // follow_up_change and sends nothing. Each draft in scope says "Rewriting…" where it is; a poll puts each new text in
 // place (same list, same scroll, still checked) with Undo change, and one that came back unchanged says so. The titles
 // are the project alone (never "<board>: <project>"), and a draft reads as paragraphs with "Regards," over the name.
 for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]){reset();
  suggestions=[...many(3).map((s,i)=>i?s:{...s,follow_up:{...s.follow_up,project:'Alpha testers: Acme pilot',name:'Acme pilot'}}),...suggestions.filter(s=>!s.follow_up)];
  const ids=suggestions.filter(s=>s.follow_up).map(s=>s.id);
  const {context,page}=await open(width,height,scheme);
  await page.locator('#suggestions .fu-group button.primary').click();const dlg=page.locator('#fu-review');await dlg.locator('.fr-item').first().waitFor();
  assert.equal(await dlg.locator('.fr-item b').first().textContent(),'Acme pilot');
  assert.equal((await dlg.locator('.fu-keys').textContent()).trim(),'Keys: j and k move, Enter sends, e edits, s skips, c changes.');
  // The preview is exactly the text that goes, every blank line too ("Regards," a blank line, then the name)
  const shown=await dlg.locator('.fr-item').first().locator('.fr-body').evaluate(el=>({text:el.textContent,inner:el.innerText}));
  assert.equal(shown.text,suggestions.find(s=>s.id===ids[0]).next_action.body);assert.match(shown.inner,/Regards,\n\nAlex$/);
  calls=[];await page.keyboard.press('c');const box=dlg.locator('.fr-change');await box.waitFor();
  assert.equal(await page.evaluate(()=>document.activeElement.id),'fr-change-text');
  assert.equal((await box.locator('.fr-change-q').textContent()).trim(),'What should change?');
  assert.equal(await box.locator('.mic-wrap #fr-change-text').count(),1);
  assert.equal(await box.locator('[name=fr-scope][value=all]').isChecked(),true);
  assert.deepEqual(await box.locator('.fr-scope label').evaluateAll(l=>l.map(x=>x.textContent.trim())),['All checked (3)','Only this one: Acme pilot']);
  // One row of buttons at a time: the Send row is hidden while Change is open, and no draft sends
  assert.equal(await dlg.locator('[data-fr-all]').isVisible(),false);assert.equal(await dlg.locator('.fr-main').isVisible(),false);
  assert.deepEqual(await dlg.locator('[data-fr-send]').evaluateAll(l=>l.map(b=>b.disabled)),[true,true,true]);
  assert.equal((await dlg.locator('button:visible').evaluateAll(l=>l.filter(b=>/Send/.test(b.textContent)&&!b.disabled).length)),0);
  await page.keyboard.type('Shorter, and mention the new pricing page');await fits(page,`${width} change box`);await page.mouse.move(2,2);await shot(page,`change-open-${width}-${scheme}`);
  await page.keyboard.press('Enter');await dlg.locator('.fr-item.rewriting').nth(2).waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args.ids,c.args.text]),[['follow_up_change',ids,'Shorter, and mention the new pricing page']]);
  assert.equal(await box.count(),0);
  assert.deepEqual(await dlg.locator('.fr-state').evaluateAll(l=>l.map(p=>p.textContent.trim())),['Rewriting…','Rewriting…','Rewriting…']);
  assert.equal(await dlg.locator('[data-fr-send]').first().isDisabled(),true);assert.equal(await dlg.locator('[data-fr-all]').isDisabled(),true);
  const list=await dlg.locator('.fr-list').elementHandle();await dlg.locator('.fr-list').evaluate(l=>{l.scrollTop=Math.min(60,l.scrollHeight-l.clientHeight)});
  // the draft at the top of the view, and where it is (the list may get too short to stay scrolled that far)
  const pin=()=>dlg.locator('.fr-list').evaluate(l=>{const t=l.getBoundingClientRect().top,p=[...l.children].find(x=>x.getBoundingClientRect().bottom>t);return {id:p.dataset.fr,top:Math.round(p.getBoundingClientRect().top-t),end:l.scrollTop>=l.scrollHeight-l.clientHeight-1}});
  const at=await pin();
  await page.mouse.move(2,2);await shot(page,`change-rewriting-${width}-${scheme}`);
  // a poll while they're being written, then two come back rewritten and one came back as it was
  await page.evaluate(()=>refresh());await page.waitForTimeout(150);
  suggestions=suggestions.map((s,i)=>!ids.includes(s.id)?s:i<2?{...s,status:'prepared',preparation_status:'done',next_action:{...s.next_action,body:`Hi ${['Sam','Kim'][i]},\n\nShort one: the new pricing page is up. Worth a look?\n\nRegards,\n\nAlex`,revision:s.next_action.revision+'c'}}
   :{...s,status:'prepared',preparation_status:'done'});
  await page.evaluate(()=>refresh());await dlg.locator('[data-fr-undo]').nth(1).waitFor();
  assert.equal(await page.evaluate(el=>el.isConnected,list),true,'a rewrite redrew the whole list');
  {const now=await pin();assert.ok(now.id===at.id&&(Math.abs(now.top-at.top)<=1||now.end),`a rewrite moved the list ${JSON.stringify([at,now])}`)}
  assert.match(await dlg.locator('.fr-item').first().locator('.fr-body').textContent(),/new pricing page/);
  assert.deepEqual(await dlg.locator('.fr-state').evaluateAll(l=>l.map(p=>p.textContent.trim())),['Undo change','Undo change','Couldn’t change this one, try againTry again']);
  assert.deepEqual(await dlg.locator('[data-fr-check]').evaluateAll(l=>l.map(c=>c.checked)),[true,true,true]);
  assert.equal((await dlg.locator('[data-fr-all]').textContent()).trim(),'Send all checked (3)');
  assert.equal(calls.filter(c=>c.action==='confirm_action').length,0,'a Change sent something');
  await fits(page,`${width} change done`);await page.mouse.move(2,2);await shot(page,`change-done-${width}-${scheme}`);
  // Undo change puts the earlier text back (revise_draft with it); Try again asks for that one alone
  calls=[];await dlg.locator('[data-fr-undo]').first().click();await dlg.locator('.fr-item').first().locator('.fr-body',{hasText:'Thanks again'}).waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args.suggestion_id,c.args.revision]),[['revise_draft',ids[0],'r10c']]);assert.match(calls[0].args.body,/^Hi Sam,\n\nThanks again/);
  assert.equal(await dlg.locator('.fr-item').first().locator('.fr-state').count(),0);
  calls=[];await dlg.locator('[data-fr-retry]').click();await dlg.locator('.fr-item').nth(2).locator('.fr-state',{hasText:'Rewriting…'}).waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args.ids,c.args.text]),[['follow_up_change',[ids[2]],'Shorter, and mention the new pricing page']]);
  // Only this one: the current draft alone
  suggestions=suggestions.map(s=>s.id===ids[2]?{...s,status:'prepared',preparation_status:'done',next_action:{...s.next_action,revision:'r12d'}}:s);await page.evaluate(()=>refresh());await dlg.locator('.fr-item').nth(2).locator('[data-fr-undo]').waitFor();
  await dlg.locator('.fr-item').nth(1).click({position:{x:200,y:12}});calls=[];await dlg.locator('[data-fr-change]').click();await box.waitFor();
  await box.locator('[name=fr-scope][value=one]').check();assert.match(await box.locator('.fr-one').textContent(),/^Only this one: Bolt trial$/);
  await box.locator('#fr-change-text').fill('Add a line about Friday');await box.locator('[data-fr-box-go]').click();await dlg.locator('.fr-item.rewriting').first().waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args.ids]),[['follow_up_change',[ids[1]]]]);
  assert.equal(calls.filter(c=>c.action==='confirm_action').length,0);
  await context.close()}
 // Stop sending on the progress to-do: follow_up_stop with the batch, then "Stopped. 1 sent, 11 kept as drafts." (no
 // bar, no button); the kept ones are back as the board's ready to-do
 for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]){reset();
  progress=[{group:'board:1',board:'Alpha testers',batch:'board:1@2026-10-29T09:00:00+00:00',total:12,done:1,sent:1,going:true,held:0,held_new:0,stopped:0,done_at:day(0.005)}];
  const {context,page}=await open(width,height,scheme);const card=page.locator('#suggestions .fu-sending');await card.waitFor();
  assert.equal((await card.locator('.fu-progress').textContent()).trim(),'Sending 2 of 12…');
  const stop=card.locator('[data-fu-stop]');assert.equal((await stop.textContent()).trim(),'Stop sending');
  await fits(page,`${width} sending`);await shot(page,`sending-${width}-${scheme}`,width<600?null:card);
  calls=[];await stop.click();await card.locator('.fu-progress',{hasText:'Stopped'}).waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args.batch]),[['follow_up_stop','board:1@2026-10-29T09:00:00+00:00']]);
  assert.equal((await page.locator('#suggestions .fu-sending .fu-progress').textContent()).trim(),'Stopped. 1 sent, 11 kept as drafts.');
  assert.equal(await page.locator('#suggestions .fu-sending [data-fu-stop]').count(),0);assert.equal(await page.locator('#suggestions .fu-sending .fu-bar').count(),0);
  await fits(page,`${width} stopped`);await shot(page,`stopped-${width}-${scheme}`,width<600?null:page.locator('#suggestions .fu-sending'));
  progress=[{...progress[0],sent:11,stopped:1}];await page.evaluate(()=>refresh());
  assert.equal((await page.locator('#suggestions .fu-sending .fu-progress').textContent()).trim(),'Stopped. 11 sent, 1 kept as a draft.');
  await context.close()}
 // Send never sends a draft other than the one on screen: one that changed under the review (a poll it hadn't drawn yet)
 // is drawn again instead, and the rest go
 {reset();const {context,page}=await open(1440,900);
  await page.locator('#suggestions .fu-group button.primary').click();const dlg=page.locator('#fu-review');await dlg.locator('.fr-item').first().waitFor();
  await page.evaluate(()=>{const s=state.suggestions.find(x=>x.id==='f200000000000000');s.next_action={...s.next_action,body:'Hi Kim, a text not seen yet.',revision:'r2x'}});
  calls=[];await dlg.locator('[data-fr-all]').click();await dlg.locator('[data-fr-error]:not([hidden])').waitFor();
  assert.deepEqual(calls.filter(c=>c.action==='confirm_action').map(c=>c.args.suggestion_id),['f100000000000000','f300000000000000']);
  assert.equal((await dlg.locator('[data-fr-error]').textContent()).trim(),'1 draft changed: read it, then send.');
  assert.match(await dlg.locator('.fr-item').first().locator('.fr-body').textContent(),/not seen yet/);
  await context.close()}
 // Bring back: a skipped follow-up on the project's page (its follow-ups) and on its to-do in Done
 {reset();const was=detail.follow_up.activity;detail.follow_up.activity=[{n:1,of_max:3,channel:'email',state:'skipped',auto:0,created_at:day(-1),closed_at:day(-1),back:'f500000000000000'},...was];
  suggestions=[...suggestions,{...card(5,'Ember labs','Hi Bo, a short follow-up.'),status:'rejected',closed_at:day(-0.5),follow_up:{project:'Ember labs',name:'Ember labs',project_id:'project:5',board:null,group:null,n:1,max:3,channel:'email',auto:false,state:'skipped',back:true}}];
  const {context,page}=await open(1440,900);await toBoard(page);
  await page.locator('.tile[data-node="project:5"]').click();const back=page.locator('.graph-fu [data-fu-back]');await back.waitFor();
  assert.match(await page.locator('.graph-fu li').first().textContent(),/Follow-up 1 skipped · Bring back$/);await shot(page,'bring-back-project-1440-light',page.locator('.graph-fu'));
  calls=[];await back.click();await page.locator('#toast',{hasText:'Back to review.'}).waitFor();
  assert.deepEqual(calls.filter(c=>c.action==='follow_up_bring_back').map(c=>c.args.id),['f500000000000000']);
  await page.goto(base+'#chat=f500000000000000');const b2=page.locator('[data-fu-back="f500000000000000"]:visible').first();await b2.waitFor();
  assert.equal((await b2.textContent()).trim(),'Bring back');
  calls=[];await b2.click();await page.locator('#toast',{hasText:'Back to review.'}).waitFor();
  assert.deepEqual(calls.filter(c=>c.action==='follow_up_bring_back').map(c=>c.args.id),['f500000000000000']);
  detail.follow_up.activity=was;await context.close()}
 // The Machine would stop here: the draft is still there, with why, and unchecked (Send all leaves it); the owner sends
 // it, skips it or picks Stop follow-ups here (follow_up_end), which ends that one without sending. Its to-do says it too.
 for(const [width,height,scheme] of [[1440,900,'light'],[1440,700,'dark'],[390,844,'light']]){reset();
  suggestions=suggestions.map(s=>s.id==='f300000000000000'?{...s,follow_up:{...s.follow_up,advice:'9 unanswered emails since August'}}:s);
  const {context,page}=await open(width,height,scheme);
  await page.locator('#suggestions .fu-group button.primary').click();const dlg=page.locator('#fu-review');await dlg.locator('.fr-item').first().waitFor();
  const item=dlg.locator('.fr-item[data-fr="f300000000000000"]');
  assert.equal((await item.locator('.fr-advice span').textContent()).trim(),'The Machine would stop here: 9 unanswered emails since August');
  assert.equal(await item.locator('[data-fr-check]').isChecked(),false);
  assert.equal((await dlg.locator('[data-fr-all]').textContent()).trim(),'Send all checked (2)');
  assert.equal(await item.locator('[data-fr-send]').getAttribute('class'),'fr-plain');
  await item.click();await item.locator('[data-fr-end]').waitFor();
  await fits(page,`${width} advice`);await shot(page,`advice-review-${width}x${height}-${scheme}`,width<600?null:dlg);
  // While Change is open nothing ends either
  await dlg.locator('[data-fr-change]').click();assert.equal(await item.locator('[data-fr-end]').isDisabled(),true);await dlg.locator('[data-fr-box-cancel]').click();
  calls=[];await item.locator('[data-fr-end]').click();await page.locator('#toast',{hasText:'Follow-ups stopped here.'}).waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args.id]),[['follow_up_end','f300000000000000']]);
  await dlg.locator('.fr-item[data-fr="f300000000000000"]').waitFor({state:'detached'});
  assert.equal(await dlg.locator('.fr-item').count(),2);assert.equal(calls.filter(c=>c.action==='confirm_action').length,0);
  await context.close()}
 {reset();suggestions=suggestions.map(s=>s.id==='f400000000000000'?{...s,follow_up:{...s.follow_up,advice:'No answer to four emails'}}:s);
  const {context,page}=await open(1440,900);const todo=page.locator('#task-f400000000000000');await todo.waitFor();
  assert.match(await todo.textContent(),/The Machine would stop here: No answer to four emails/);await shot(page,'advice-todo-1440-light',todo);
  await context.close()}
 // Done: the board's sent and skipped follow-ups of a day are one row ("13 follow-ups sent for Alpha testers", "2 skipped"),
 // projects' own ones one row per day, a single one stays itself; opening a row lists project, to and when, each linking
 // to its to-do; the sidebar's Find still finds each one. The Suggestions page's Done list folds the same way.
 {const at=(d,m)=>{const x=new Date();x.setDate(x.getDate()+d);x.setHours(9,m,0,0);return x.toISOString()};
  const names=['Acme pilot','Bolt trial','Cobalt rollout','Delta renewal','Ember labs','Fjord studio','Grove co','Harbor works','Iris media','Juno apps','Kite labs','Lumen co','Mesa group','Nova inc','Orbit io'];
  const sent=(i,project,state,group,when)=>({...card(40+i,project,'Hi, a quick follow-up.'),status:state==='sent'?'completed':'rejected',closed_at:when,
   follow_up:{project:group?'Alpha testers: '+project:project,name:project,project_id:'project:'+(40+i),board:group?'Alpha testers':null,group:group?'board:1':null,n:1,max:3,channel:'email',auto:true,state}});
  const done=()=>[...names.map((p,i)=>sent(i,p,i<13?'sent':'skipped','board',at(0,i))),sent(20,'Quartz labs','sent',null,at(0,30)),sent(21,'Raven co','sent',null,at(0,31)),
   sent(22,'Sable inc','sent','board',at(-1,5)),{id:'done000000000000',title:'Send the deck to the board',body:'',status:'completed',scope:'work',event_ids:[8],created_at:at(-1,0),closed_at:at(-1,40)}];
  for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]){reset();suggestions=[...suggestions,...done()];
   const {context,page}=await open(width,height,scheme);
   if(width<600){await page.locator('#drawer-open').click();await page.locator('#side-cards').waitFor()}
   const doneHead=page.locator('#side-cards [data-side-fold=done]');await doneHead.waitFor();
   assert.equal((await doneHead.locator('.count').textContent()).trim(),'19');  // every to-do counts, folded or not
   if(await doneHead.getAttribute('aria-expanded')==='false')await doneHead.click();
   const rows=page.locator('#side-cards .done-fold');await rows.first().waitFor();
   assert.deepEqual(await rows.evaluateAll(l=>l.map(b=>b.textContent.trim())),['2 follow-ups sent','13 follow-ups sent for Alpha testers2 skipped']);
   const doneRows=await page.locator('#side-cards .side-group').last().locator(':scope>a,:scope>.done-fold').evaluateAll(l=>l.map(a=>a.textContent.trim()));
   assert.deepEqual(doneRows,['2 follow-ups sent','13 follow-ups sent for Alpha testers2 skipped','Send the deck to the board','Follow up with Sable inc']);
   await fits(page,`${width} done folded`);await shot(page,`done-side-${width}-${scheme}`,width<600?null:page.locator('.app-side'));
   await rows.nth(1).click();const sub=page.locator('#side-cards .done-fold-list a');await sub.first().waitFor();
   assert.equal(await sub.count(),15);assert.equal(await rows.nth(1).getAttribute('aria-expanded'),'true');
   assert.equal(await page.evaluate(()=>document.activeElement.dataset.doneFold),await page.evaluate(()=>'board:1@'+localDay(new Date())));
   assert.match(await sub.first().textContent(),/^Orbit ioTo person54@client\.example · Skipped$/);  // newest first
   assert.match(await sub.last().textContent(),/^Acme pilotTo person40@client\.example · \d{1,2}:\d\d/);assert.equal(await sub.last().getAttribute('href'),'#chat='+card(40,'','').id);
   await fits(page,`${width} done open`);await shot(page,`done-side-open-${width}-${scheme}`,width<600?null:page.locator('.app-side'));
   if(width>600){await page.locator('#side-find').fill('kite');await page.waitForTimeout(50);
    assert.deepEqual(await page.locator('#side-cards a').evaluateAll(l=>l.map(a=>a.textContent)),['Follow up with Kite labs']);
    await page.locator('#side-find').fill('');await page.locator('#side-find').dispatchEvent('input')}
   if(width<600)await page.keyboard.press('Escape');
   if(width>600){await page.locator('#finished-head').click();const fold=page.locator('#suggestions .fu-done');await fold.first().waitFor();
    assert.deepEqual(await fold.locator('h3').evaluateAll(l=>l.map(h=>h.textContent)),['2 follow-ups sent','13 follow-ups sent for Alpha testers']);assert.equal(await fold.nth(1).locator('.done-fold-n').textContent(),'2 skipped');
    assert.equal(await fold.nth(1).locator('details').getAttribute('open'),null);await fold.nth(1).locator('summary').click();assert.equal(await fold.nth(1).locator('details').getAttribute('open'),'');assert.equal(await fold.nth(1).locator('li').count(),15);
    await fold.nth(1).scrollIntoViewIfNeeded();await fits(page,`${width} done page`);await shot(page,`done-page-${width}-${scheme}`,fold.nth(1))}
   await context.close()}}
 reset();
 // Phone, light and dark: the same pieces fit the screen
 for(const scheme of ['light','dark']){reset();const {context,page}=await open(390,844,scheme);
  await page.locator('#suggestions .fu-group').waitFor();await fits(page,'390 to-dos');await shot(page,`grouped-todo-390-${scheme}`);
  await page.locator('#suggestions .fu-group button.primary').click();await page.locator('#fu-review .fr-item').first().waitFor();await fits(page,'390 review');await shot(page,`review-390-${scheme}`);
  await page.keyboard.press('Escape');await toBoard(page);await fits(page,'390 board');await shot(page,`board-390-${scheme}`);
  await page.locator('.board-sub .fu-state').click();await page.locator('#fu-dialog [name=days]').waitFor();await fits(page,'390 settings');await shot(page,`settings-board-390-${scheme}`);
  await page.locator('#fu-dialog [data-fu-custom]').click();await shot(page,`settings-board-custom-390-${scheme}`);
  await page.keyboard.press('Escape');
  await page.evaluate(()=>document.querySelector('.tile[data-node="project:5"]').click());await page.locator('.graph-fu').waitFor();await fits(page,'390 project');await shot(page,`project-next-390-${scheme}`);
  await page.locator('.graph-fu [data-fu-open]').click();await page.locator('#fu-dialog [name=mode]').first().waitFor();await page.locator('#fu-dialog [name=mode][value=on]').check();await shot(page,`settings-project-390-${scheme}`);
  await context.close()}
 if(process.env.FOLLOW_UPS_SHOT)for(const scheme of ['dark']){reset();const {context,page}=await open(1440,900,scheme);
  await page.locator('#suggestions .fu-group').waitFor();await shot(page,`grouped-todo-1440-${scheme}`);
  await page.locator('#suggestions .fu-group button.primary').click();await page.locator('#fu-review .fr-item').first().waitFor();await shot(page,`review-1440-${scheme}`);
  await page.keyboard.press('Escape');await toBoard(page);await shot(page,`board-1440-${scheme}`);
  await page.locator('.board-sub .fu-state').click();await page.locator('#fu-dialog [name=days]').waitFor();await page.locator('#fu-dialog [data-fu-custom]').click();await shot(page,`settings-board-1440-${scheme}`,page.locator('#fu-dialog'));
  await page.keyboard.press('Escape');await page.locator('.tile[data-node="project:5"]').click();await page.locator('.graph-fu').waitFor();await shot(page,`project-next-1440-${scheme}`,page.locator('.graph-detail'));
  await page.locator('.graph-fu [data-fu-open]').click();await page.locator('#fu-dialog [name=mode]').first().waitFor();await page.locator('#fu-dialog [name=mode][value=on]').check();await shot(page,`settings-project-1440-${scheme}`,page.locator('#fu-dialog'));
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('follow-ups dashboard ok');
}finally{await browser?.close();server.close()}
