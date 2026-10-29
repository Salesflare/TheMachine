import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Automated follow-ups on the dashboard (follow_ups.py): a board's ready follow-ups are ONE to-do ("3 follow-ups ready
// for …") that opens a fast review: j/k or arrows move, Enter sends (confirm_action), e edits (revise_draft), s skips
// (decide reject), Send all checked sends the checked ones; a project's own follow-up stays a normal to-do. The board
// header says "Follow-ups on, next …", a tile "Next follow-up: …", the project page what went out. The settings panel
// for a board and for a project posts follow_up_save. Nothing is wider than the screen. FOLLOW_UPS_SHOT=<dir> writes
// screenshots at 390 and 1440, light and dark.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const day=n=>new Date(Date.now()+n*864e5).toISOString();
const draft=(i,body,extra={})=>({kind:'email',label:'Send',account_id:'work',from:'owner@example.com',to:[`person${i}@client.example`],subject:'Re: Alpha',body,revision:'r'+i,...extra});
const card=(i,project,body,extra={})=>({id:('f'+i).padEnd(16,'0'),title:'Follow up on '+project,body:'No reply for 4 days. Follow-up 1 of at most 3.',status:'prepared',early:1,scope:'work',event_ids:[i],
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
const boards=[{id:1,name:'Alpha testers',stages,side:true,visibility:'team',follow_ups:{on:true,next_at:day(2)},projects:[
 proj(1,'Acme pilot','Invited',{state:'open',n:1,max:3}),proj(2,'Bolt trial','Testing',{state:'open',n:1,max:3}),proj(5,'Ember labs','Testing',{state:'waiting',next_at:day(2),n:1,max:3}),
 proj(6,'Fjord studio','Invited',{state:'stopped',end:{n:3,moved:0,judged:0,at:day(-1)}}),proj(7,'Grove co','Live')]}];
const detail={id:'project:5',kind:'project',name:'Ember labs',state:'active',strength:1,last_at:day(-2),signals:3,ids:[],links:[],recent:[],around:[],open:{},
 board:{board:'Alpha testers',stage:'Testing',next:null,visibility:null,board_visibility:'team',stages:['Invited','Testing','Live'],moves:[{stage:'Testing',reason:'they installed the build',source:'review',at:day(-6),event_id:105}]},
 follow_up:{on:true,source:'board',next_at:day(2),state:'waiting',n:2,max:3,ends:[],activity:[{n:1,of_max:3,channel:'email',state:'sent',auto:1,created_at:day(-3),closed_at:day(-3)}]}};
const panel=(scope,id)=>scope==='board'?{scope:'board',id:1,name:'Alpha testers',stalled:true,careful:false,channels:['email','linkedin','whatsapp'],
  stages:[{name:'Invited',open:true},{name:'Testing',open:true},{name:'Live',open:false}],settings:{on:true,days:3,max_days:7,min:1,max:3,stages:{},channels:null,switch:false,auto:false,stall:null}}
 :{scope:'project',id:+String(id).replace('project:',''),name:'Ember labs',own:false,stalled:true,careful:true,channels:['email'],board:{id:1,name:'Alpha testers',on:true},
  settings:{on:true,days:3,max_days:7,min:1,max:3,stages:{},channels:null,switch:false,auto:false,stall:null}};
let calls=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions,follow_up_progress:progress,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');res.end(JSON.stringify(n?detail:{projects:[],people:[],quiet:[],new:[],orgs:[],boards}));return}
 if(req.method==='POST'&&url.pathname==='/api/action'){const c=JSON.parse(body||'{}');calls.push(c);const a=c.args||{};
  if(c.action==='follow_up_settings'||c.action==='follow_up_save'){res.end(JSON.stringify(panel(a.scope,a.id)));return}
  if(c.action==='revise_draft'){const s=suggestions.find(x=>x.id===a.suggestion_id);s.next_action={...s.next_action,body:a.body,revision:a.revision+'e'};res.end(JSON.stringify({revision:a.revision+'e',body:a.body}));return}
  if(c.action==='confirm_action'){suggestions=suggestions.filter(x=>x.id!==a.suggestion_id);res.end(JSON.stringify({status:'queued'}));return}
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
 await page.locator('#suggestions article').first().waitFor();return {context,page}};
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
  assert.deepEqual(await page.locator('#side-cards a').evaluateAll(l=>l.map(a=>a.textContent)),['3 follow-ups ready for Alpha testers','Follow up on Delta renewal','Reply to the venue about Friday']);
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
  await page.keyboard.press('e');const box=dlg.locator('.fr-edit');await box.waitFor();await box.fill('Hi Kim, short one: did the guide help?');
  await page.keyboard.press('Control+Enter');await dlg.locator('.fr-edit').waitFor({state:'detached'});
  assert.deepEqual(calls.map(c=>c.action),['revise_draft']);assert.match(await dlg.locator('.fr-item.on .fr-body').textContent(),/did the guide help\?/);
  // s skips (Not needed), and unchecking leaves one out of Send all checked
  await page.keyboard.press('j');calls=[];await page.keyboard.press('s');await page.waitForFunction(()=>document.querySelectorAll('#fu-review .fr-item').length===1);
  assert.deepEqual(calls.map(c=>[c.action,c.args.choice,c.args.suggestion_id]),[['decide','reject','f300000000000000']]);
  calls=[];await dlg.locator('[data-fr-all]').click();await dlg.waitFor({state:'hidden'});
  assert.deepEqual(calls.map(c=>[c.action,c.args.suggestion_id,c.args.revision]),[['confirm_action','f200000000000000','r2e']]);
  // The board: "Follow-ups on, next …" in the header, a tile's next follow-up, ready and a round that ended quietly
  reset();await toBoard(page);
  assert.match(await page.locator('.board-sub .fu-state').textContent(),/^Follow-ups on, next \w{3}$/);
  assert.match(await page.locator('.tile[data-node="project:5"] .tile-fu').textContent(),/^Next follow-up: \w{3}$/);
  assert.equal(await page.locator('.tile[data-node="project:1"] .tile-fu').textContent(),'Follow-up ready');
  assert.equal(await page.locator('.tile[data-node="project:6"] .tile-fu').textContent(),'No reply after 3 follow-ups');
  assert.equal(await page.locator('.tile[data-node="project:7"] .tile-fu').count(),0);
  await fits(page,'1440 board');await shot(page,'board-1440-light');
  // The board's settings panel: both pairs on two rows, stages behind Customize, channels, Stalled, asking first
  calls=[];await page.locator('.board-sub .fu-state').click();const fu=page.locator('#fu-dialog');await fu.locator('[name=days]').waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args.scope,c.args.id]),[['follow_up_settings','board','1']]);
  assert.match(await fu.locator('.fu-row').first().textContent(),/^Wait\s+to\s+days without a reply$/);
  assert.deepEqual(await fu.locator('.fu-row input').evaluateAll(l=>l.map(i=>i.value)),['3','7','1','3']);
  assert.equal(await fu.locator('[name=auto][value=ask]').isChecked(),true);assert.equal(await fu.locator('[name=stall]').isChecked(),true);
  await shot(page,'settings-board-1440-light',fu);
  await fu.locator('[data-fu-custom]').click();assert.equal(await fu.locator('[data-fu-stage]').count(),3);
  assert.deepEqual(await fu.locator('[data-fu-stage]').evaluateAll(l=>l.map(i=>i.checked)),[true,true,false]);
  await fu.locator('[data-fu-sdays="1"]').fill('5');await fu.locator('[name=max]').fill('2');await fu.locator('[name=ch][value=whatsapp]').uncheck();
  await fu.locator('[name=switch]').check();await fu.locator('[name=auto][value=auto]').check();
  assert.equal((await fu.locator('.fu-send .fu-note').textContent()).trim(),'Anything unusual still waits for you.');
  await shot(page,'settings-board-custom-1440-light',fu);
  calls=[];await fu.locator('button.primary').click();await fu.waitFor({state:'hidden'});
  const save=calls.find(c=>c.action==='follow_up_save');
  assert.deepEqual(save.args,{scope:'board',id:1,settings:{on:true,days:3,max_days:7,min:1,max:2,channels:['email','linkedin'],switch:true,auto:true,stall:true,
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
  progress=[{group:'board:1',board:'Alpha testers',total:8,done:2,sent:2,going:true}];
  const {context,page}=await open(width,height);const sending=page.locator('#suggestions .fu-sending');await sending.waitFor();
  assert.equal(await sending.count(),1);assert.equal(await page.locator('#suggestions .fu-group').count(),0);
  assert.equal((await sending.locator('h3').textContent()).trim(),'Follow-ups for Alpha testers');
  assert.equal((await sending.locator('.fu-progress').textContent()).trim(),'Sending 3 of 8…');
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
  await context.close()}
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
