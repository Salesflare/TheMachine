import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Who sees a board, on its header (shared_graph.team_boards, graph.boards): the owner's own board says Shared with the
// team and how many of its projects stay with them (kept private, or someone on them is Personal), each with a lock; a
// teammate's says whose it is and whether the whole team has it or only chosen teammates. Look-alike projects of a
// teammate fold into one row that reads as a group ("Pilot review: …", 5 alike projects). A tile's newest line never
// says an older stage than the one it is in. A teammate's project opens under Projects with its organization linked.
// TEAM_BOARDS_SHOT=<dir> writes screenshots (TEAM_BOARDS_LANG=nl for Dutch).
const dashboard=await dashboardPage();
const LANG=process.env.TEAM_BOARDS_LANG||'en',SHOTS=process.env.TEAM_BOARDS_SHOT;
const cats={};for(const l of ['en','nl'])cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const FL='fl_'+'c'.repeat(16),day=n=>new Date(Date.now()-n*864e5).toISOString();
const sharing=[{fleet:FL,name:'Acme',admin:false,confirmed:true,prompts:[],off:null,waiting:0,week:null,teammates:2,started:true,paused:null,require:[],connections:[],people:[],new_devices:[]}];
const stages=[{name:'Invited'},{name:'Trying it'},{name:'Feedback'},{name:'Up and running'},{name:'Stalled or declined',side:true}];
const proj=(i,name,stage,extra={})=>({id:'project:'+i,name,stage,reason:'they said yes to a trial',by:'review',at:day(3),event_id:100+i,next:null,first:false,days:3,no_reply_days:0,org:null,...extra});
const mine=[{id:1,name:'Pilot program',visibility:'team',stages,stuck:0,maybes:[],held:2,shared_with:[],
 projects:[proj(1,'Pilot review: Paperkite','Invited'),proj(2,'Pilot review: Bramblebox','Invited',{held:true}),proj(3,'Pilot review: Quillfeather','Trying it'),proj(4,'Pilot review: Fernwave','Up and running',{held:true})]}];
const team=(i,name,stage,extra={})=>({id:'team:project:'+String(i).padStart(32,'0'),name,stage,reason:'they said yes to a trial',by:'review',at:day(5),first:false,days:5,org:null,team_only:true,owner_name:'Ada',fleet:FL,via:'via Ada',yours:false,needs_you:false,...extra});
const pilots=['Paperkite','Bramblebox','Quillfeather','Otterly Mail','Fernwave','Copperleaf'];
const teamBoards=[
 {name:'Pilot program',stages,team:true,stuck:0,by:['Ada'],seen:'team',projects:[...pilots.map((n,i)=>team(i+1,'Pilot review: '+n,'Invited',{line:'Email: Re: Pilot for '+n,line_at:day(6+i)})),
  team(20,'Lanternfish','Trying it',{at:day(2),line:'Moved to Invited: agreed to try it',line_at:day(9)}),team(21,'Mossgate','Feedback',{org:{name:'Mossgate',logo:null}})]},
 {name:'Acquisition talks',stages:[{name:'Contacted'},{name:'Interested'},{name:'Stalled or declined',side:true}],team:true,stuck:0,by:['Ada'],seen:'people',
  projects:[team(30,'Buyer talks: Northfund','Contacted'),team(31,'Buyer talks: Globex','Interested')]}];
const teamDetail={id:'team:project:'+'3'.padStart(32,'0'),kind:'project',name:'Buyer talks: Northfund',role:null,team_only:true,links:[],recent:[],probable_ids:[],last_at:day(2),
 strength:1,closeness:'regular',signals:0,org_name:'Northfund',org:'team:org:'+'9'.repeat(32),state:'active',stage:'Contacted',board:'Acquisition talks',next:null,team_fields:[],tags:[],
 team:{via:'via Ada',people:[{fleet:FL,member:'m_ada',name:'Ada',score:1,left:false}],timeline:[{at:day(2),line:'Bo agreed to the terms',via:'Ada'}],threads:[{id:FL+':m_ada:'+'e'.repeat(32),subject:'Re: Terms',at:day(2),messages:2,via:'Ada',from:'Bo Lind',preview:'Here are the terms.'}],fields:[],tags:[]}};
const locale={locale:'en-BE',region:'BE',language:LANG,language_set:true,clock:'auto',hour12:false,auto_hour12:false,date_locale:LANG==='en'?'en-GB':LANG+'-BE',languages:{en:'English',nl:'Nederlands'},saveable:true};
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const cat=/^\/i18n\/(\w\w(?:-[A-Z]{2})?)\.json$/.exec(url.pathname);if(cat)return res.end(cats[cat[1]]||'{}');
 if(url.pathname==='/api/status')return res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0},locale}));
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');if(n)return res.end(JSON.stringify(teamDetail));
  if(url.searchParams.get('thread'))return res.end(JSON.stringify({subject:'Re: Terms',at:day(2),via:'Ada',messages:[{at:day(3),from:'Ada <ada@acme.example>',body:'Can you send the terms?',attachments:[]},{at:day(2),from:'Bo <bo@northfund.example>',body:'Here are the terms.',attachments:[]}]}));
  if(url.searchParams.get('view')==='team')return res.end(JSON.stringify({team:true,people:[],orgs:[],projects:[],quiet:[],new:[],boards:teamBoards,sharing,counts:{person:0,org:0,project:10}}));
  return res.end(JSON.stringify({people:[],orgs:[],projects:[],quiet:[],new:[],boards:mine,sharing,teammates:[{fleet:FL,member:'m_ada',name:'Ada'}]}))}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const open=async(width,height,scheme)=>{const mobile=width<600,context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-GB',colorScheme:scheme});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));await page.goto(base);
 if(LANG!=='en')await page.waitForFunction(l=>document.documentElement.lang===l,LANG);
 await page.evaluate(()=>{sideStore.set('projects-view','board');document.querySelector('nav [data-tab="people"]').click()});await page.locator('#people-view').waitFor({state:'attached'});
 await page.evaluate(()=>document.querySelector('[data-graph-sub="projects"]').click());
 await page.locator('#people-view .proj-board:not([hidden]) .pboard').waitFor();return {context,page}};
const toTeam=async page=>{await page.locator('#page-head [data-graph-team="team"]').click();await page.locator('#people-view .board-sub',{hasText:/Ada/}).waitFor()};
const fits=(page,where)=>page.evaluate(()=>({page:document.documentElement.scrollWidth,vw:innerWidth})).then(s=>assert.ok(s.page<=s.vw,`${where}: wider than the screen ${JSON.stringify(s)}`));
const shot=async(page,name)=>{if(SHOTS)await page.screenshot({path:`${SHOTS}/${name}.png`,fullPage:true})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [w,h] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){const {context,page}=await open(w,h,scheme);
  // The owner's own board: shared with the team, two stay with the owner, each with a lock
  const sub=await page.locator('.board-sub').textContent();
  if(LANG==='en'){assert.match(sub,/^Shared with the team · 2 stay with you · 4 projects · a check moves them as your messages come in$/);
   assert.equal(await page.locator('.tile .tile-held').count(),2)}
  await fits(page,w+' mine');await shot(page,`owner-board-${w}-${scheme}`);
  // A teammate's board: whose it is and that the team has it; look-alikes fold into one row that says it is a group
  await toTeam(page);
  const tsub=await page.locator('.board-sub').textContent();
  if(LANG==='en'){assert.match(tsub,/^Ada's board, shared with the team · 8 projects · a check moves them as the team's messages come in$/);
   const group=page.locator('.lane[data-lane="Invited"] .tile-group');
   assert.equal((await group.locator('summary .tile-name').textContent()).trim(),'Pilot review: …');
   assert.match(await group.locator('summary .tile-why').textContent(),/^6 alike projects · newest Paperkite, /);
   // A move newer than the newest line: the tile says the move, not the older stage
   assert.match(await page.locator('.tile[data-node$="020"] .tile-why').textContent(),/^Moved to Trying it: they said yes to a trial · /)}
  else assert.match(tsub,/^Bord van Ada, gedeeld met het team · .* · een check verplaatst ze naarmate er berichten van het team binnenkomen$/);
  await fits(page,w+' team');await shot(page,`teammate-board-${w}-${scheme}`);
  // A board shared by name: says so, with a lock
  await page.evaluate(()=>{const b=document.querySelector('[data-board="Acquisition talks"]')||document.querySelector('.board-pick');if(b.tagName==='SELECT'){b.value='Acquisition talks';b.dispatchEvent(new Event('change',{bubbles:true}))}else b.click()});
  await page.locator('.board-title',{hasText:'Acquisition talks'}).waitFor({state:'attached'});
  if(LANG==='en')assert.match(await page.locator('.board-sub').textContent(),/^Ada shared this board with you · 2 projects/);
  await fits(page,w+' by name');await shot(page,`teammate-shared-by-name-${w}-${scheme}`);
  // A teammate's project opens under Projects, its organization a link; what the team shared is in its Timeline, with
  // Mine · Team, each line saying who it came from, and a shared thread opens like an own one
  await page.locator('.tile[data-node$="030"]').click();await page.locator('.graph-detail h3',{hasText:'Northfund'}).waitFor();
  assert.equal(await page.locator(`.graph-detail .graph-sub button.node[data-node="${teamDetail.org}"]`).count(),1);
  if(w>600)assert.equal(await page.locator('nav .side-sub a[aria-current="page"]').getAttribute('data-graph-sub'),'projects');
  assert.equal(await page.locator('.team-block').count(),0);assert.equal(await page.locator('.graph-detail .team-ask').count(),1);
  const tl=page.locator('.graph-timeline');assert.equal(await tl.locator('.ge-whose button').count(),2);
  assert.equal(await tl.locator('.ge-whose [aria-pressed="true"]').getAttribute('data-tl-whose'),'team');
  assert.match(await tl.locator('.ge-team.ge-change').innerText(),LANG==='en'?/Bo agreed to the terms\s+\d\d:\d\d · via Ada/:/via Ada/);
  assert.match(await tl.locator('[data-team-thread]').innerText(),LANG==='en'?/Re: Terms\s+2 messages · \d\d:\d\d · via Ada/:/2 berichten · .* · via Ada/);
  assert.match(await tl.locator('[data-team-thread] .ge-preview').innerText(),/^Bo: Here are the terms\.$/);  // a preview like own mail
  await fits(page,w+' project');await page.mouse.move(0,0);await shot(page,`teammate-project-${w}-${scheme}`);
  await tl.locator('[data-team-thread]').click();await page.locator('#email-dialog[open] .email-text',{hasText:'Here are the terms.'}).waitFor();
  if(scheme==='light')await shot(page,`teammate-thread-${w}-${scheme}`);
  await page.keyboard.press('Escape');await page.locator('#email-dialog[open]').waitFor({state:'detached'});
  await tl.locator('[data-tl-whose="mine"]').click();await page.locator('.graph-timeline .ge-whose [data-tl-whose="mine"][aria-pressed="true"]').waitFor();
  assert.equal(await page.locator('.graph-timeline .ge-team').count(),0);
  await page.locator('.graph-timeline [data-tl-whose="team"]').click();await page.locator('.graph-timeline .ge-team').first().waitFor();
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('team boards dashboard ok');
}finally{await browser?.close();server.close()}
