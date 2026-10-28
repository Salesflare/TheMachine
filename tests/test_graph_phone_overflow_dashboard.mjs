import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Nothing on the Graph's People, Organizations and Projects pages runs past the screen or out of its box on a 360 px
// phone: List and Board, Mine and Team, the "could belong here" box with one project (no tick box: Add and Leave out
// under the text, inside the box) and with several, the filter / stages / new project row, stage chips, tiles with a long
// organization name (it ends in …), and the order, board and tile menus once open. OVERFLOW_SHOT=<dir> writes screenshots.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const LONG_ORG='Hazelbrook Digital Marketing, Development and Growth Consultancy International';
const stages=[{name:'Invited'},{name:'Trying it'},{name:'Feedback received'},{name:'Validated'},{name:'Stalled',side:true}];
const proj=(i,name,stage,extra={})=>({id:'project:'+i,name:'Alpha testing: '+name,stage,reason:'asked for an invite and a follow-up about pricing',by:'review',at:day(2),event_id:100+i,days:2,no_reply_days:i===1?12:0,org:{name,node_id:'org:'+i,logo:null},...extra});
const mineBoards=()=>[
 {id:1,name:'Alpha testers for the new release',stages,default:true,stuck:1,projects:[proj(1,'Keep Productive','Invited'),proj(2,LONG_ORG,'Invited',{value:12000}),proj(3,'Quillfeather','Trying it')],
  maybes:[{id:'project:9',name:'Investor trial invitations for the autumn round',why:'planned investor trial invitations on October 28; individual testers not identified'}]},
 {id:2,name:'Editorial listing exchanges',stages,stuck:0,projects:[proj(4,'Saffron Sync','Invited')],
  maybes:[{id:'project:10',name:'Tinker Lane',why:'asked about pricing once'},{id:'project:11',name:'Acme acquisition talks',why:'several buyers in one',split:7},{id:'org:puffin.example',name:'Puffin Metrics',why:'an intro call, no demo yet'}]}];
const teamBoards=()=>[{name:'Alpha testers for the new release',stages,stuck:0,team:true,
 projects:[{...proj(1,'Keep Productive','Invited'),yours:true,mine:true,owner_name:'Sam Doe'},{...proj(5,LONG_ORG,'Invited'),yours:false,owner_name:'Kim Lee'},{...proj(6,'Bramblebox','Trying it'),yours:false,owner_name:'Tom Ray'}]}];
const FL='fl_'+'c'.repeat(16);
const sharing=[{fleet:FL,name:'Acme',admin:true,confirmed:true,prompts:[],off:null,waiting:0,week:null,teammates:2,started:true,paused:null,require:['mail'],connections:[],people:[],new_devices:[]}];
const person=(i,name,extra={})=>({id:'email:p'+i+'@client.example',kind:'person',name,strength:3-i%3,closeness:'regular',last_at:day(i),signals:4,ids:['p'+i+'@client.example'],...extra});
const people=[person(1,'Ada Lovelace',{role:'Sales Manager Precious Metals',org_name:LONG_ORG}),person(2,'Grace Hopper'),person(3,'Kimberly Montgomery-Vanderbilt',{role:'Customer success manager at a very long company name'})];
const orgs=[{id:'org:hazelbrook.example',kind:'org',name:LONG_ORG,strength:2,last_at:day(1),signals:8,people:4,domain:'hazelbrook.example'},{id:'org:puffin.example',kind:'org',name:'Puffin Metrics',strength:1,last_at:day(3),signals:2,people:1}];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}}));return}
 if(url.pathname==='/api/graph'){const team=url.searchParams.get('view')==='team';
  res.end(JSON.stringify(team?{team:true,held:[],people,orgs,projects:[],boards:teamBoards(),sharing,quiet:[],new:[]}
   :{projects:[{id:'project:1',kind:'project',name:'Keep Productive',strength:1,last_at:day(2),signals:3}],people,quiet:[],new:[],orgs,boards:mineBoards(),sharing,person_names:people.map(p=>({id:p.id,name:p.name})),project_names:[]}));return}
 if(url.pathname==='/api/fleet'){res.end(JSON.stringify({on:true,fleets:[],shared:{prompts:[],shares:[],accounts:[],can_share:[],graph:sharing}}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';

// Runs in the page: what sticks out past the screen, or past a box that cuts it off without an ellipsis
function outside(){const vw=document.documentElement.clientWidth,out=[];
 if(document.documentElement.scrollWidth>vw+1)out.push(`the page is ${document.documentElement.scrollWidth}px wide`);
 const name=el=>el.tagName.toLowerCase()+(el.className&&typeof el.className==='string'?'.'+el.className.trim().split(/\s+/).slice(0,2).join('.'):'')+` "${el.textContent.trim().replace(/\s+/g,' ').slice(0,30)}"`;
 const scroller=el=>{for(let p=el.parentElement;p&&p!==document.body;p=p.parentElement){const o=getComputedStyle(p).overflowX;if(o==='auto'||o==='scroll')return true}return false};
 const bad=[];
 for(const el of document.querySelectorAll('#page-head *, #people-view *')){
  if(!el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})||el.closest('details:not([open]) > :not(summary)')||scroller(el))continue;
  const r=el.getBoundingClientRect();if(!r.width||!r.height)continue;
  let why='';  // text that a box ends in … on purpose is fine
  for(let p=el.parentElement;p&&p!==document.body;p=p.parentElement){const s=getComputedStyle(p);if(s.overflowX==='visible')continue;
   if(s.textOverflow==='ellipsis'){why=null;break}const c=p.getBoundingClientRect();if(!why&&(r.right>c.right+1||r.left<c.left-1))why=`cut off by ${name(p)}`}
  if(why===null)continue;if(r.right>vw+1)why=`reaches ${Math.round(r.right)}px`;else if(r.left<-1)why=`starts at ${Math.round(r.left)}px`;
  if(why)bad.push([el,why])}
 for(const [el,why] of bad.filter(([e])=>!bad.some(([p])=>p===e.parentElement)).slice(0,6))out.push(`${name(el)} ${why}`);
 return out}
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,scheme] of [[360,'light'],[360,'dark']]){
  const context=await browser.newContext({viewport:{width,height:780},isMobile:true,hasTouch:true,locale:'en-GB',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));await page.goto(base);
  const shot=async name=>{if(process.env.OVERFLOW_SHOT)await page.screenshot({path:`${process.env.OVERFLOW_SHOT}/${name}-${width}-${scheme}.png`})};
  const fits=async where=>assert.deepEqual(await page.evaluate(outside),[],`${width} ${scheme} ${where}: runs past the screen or its box`);
  const settle=()=>page.waitForTimeout(150);
  // open a menu with a tap, check it, close it again
  const menu=async(sel,where)=>{const s=page.locator(sel).filter({visible:true}).first();await s.scrollIntoViewIfNeeded();await s.click();await settle();
   assert.equal(await s.evaluate(x=>x.parentElement.open),true,`${where} opens`);await fits(where+' open');await shot(where.replace(/\W+/g,'-'));await s.evaluate(x=>{x.parentElement.open=false})};
  await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());await page.locator('#people-view').waitFor({state:'attached'});
  const sub=async name=>{await page.evaluate(n=>document.querySelector(`[data-graph-sub="${n}"]`).click(),name);await page.locator('#people-view .sub-pane:not([hidden])').first().waitFor();await settle()};
  const whose=async v=>{await page.locator(`#page-head [data-graph-team="${v}"]`).click();await page.locator(`#page-head [data-graph-team="${v}"][aria-pressed="true"]`).waitFor();await page.waitForLoadState('networkidle');await settle()};
  for(const pane of ['people','orgs']){await sub(pane);
   for(const v of ['mine','team']){await whose(v);await fits(`${pane} ${v}`);await shot(`${pane}-${v}`)}
   await whose('mine');await menu('#people-view .graph-sort>summary',`${pane} order menu`);
   // the order menu opens toward the screen, not past its left edge
  }
  await sub('projects');
  for(const v of ['mine','team']){await whose(v);
   for(const mode of ['list','board']){await page.locator(`#page-head [data-proj-view="${mode}"]`).click();await settle();
    await page.evaluate(()=>{for(const d of document.querySelectorAll('.board-fits'))d.open=true});await settle();
    await fits(`projects ${v} ${mode}`);await shot(`projects-${v}-${mode}`)}}
  await whose('mine');
  // One project could belong here: no tick box, the name and why get the box's width, Add and Leave out sit under them inside it
  const box=page.locator('.board-fits');await box.scrollIntoViewIfNeeded();
  assert.match(await box.locator('summary').textContent(),/1 project could belong here/);
  const row=await box.locator('li').evaluate(li=>{const b=li.closest('.board-fits').getBoundingClientRect(),t=li.querySelector('.fit-text').getBoundingClientRect(),
   btn=[...li.querySelectorAll('.fit-acts button')].map(x=>x.getBoundingClientRect());return {box:[b.left,b.right],text:[t.left,t.right,t.bottom],buttons:btn.map(r=>[r.left,r.right,r.top])}});
  for(const [l,r,top] of row.buttons)assert.ok(l>=row.box[0]&&r<=row.box[1]&&top>=row.text[2]-2,`Add and Leave out under the text, inside the box ${JSON.stringify(row)}`);
  assert.ok(row.text[1]-row.text[0]>(row.box[1]-row.box[0])*0.8,`the text gets the box's width ${JSON.stringify(row)}`);
  await shot('projects-fits-one');
  await menu('#people-view .board-menu>summary','board menu');
  await menu('#people-view .tile-menu>summary','tile menu');
  // A long organization name on a tile ends in … inside it
  const org=await page.locator('.tile-org .inline-node',{hasText:'Hazelbrook'}).first().evaluate(b=>({cut:b.scrollWidth>b.clientWidth,right:b.getBoundingClientRect().right,tile:b.closest('.tile').getBoundingClientRect().right,ellipsis:getComputedStyle(b).textOverflow}));
  assert.ok(org.cut&&org.ellipsis==='ellipsis'&&org.right<=org.tile,`a long organization name ends in … inside its tile ${JSON.stringify(org)}`);
  // Several to review: the tick boxes, Select all and the bulk buttons stay inside the box too
  await page.evaluate(()=>{const s=document.querySelector('.board-pick');s.value='Editorial listing exchanges';s.dispatchEvent(new Event('change',{bubbles:true}))});
  await page.locator('.board-fits summary',{hasText:'3 projects could belong here'}).waitFor();
  await page.evaluate(()=>{for(const d of document.querySelectorAll('.board-fits'))d.open=true});await settle();
  await fits('projects several to review');await page.locator('.board-fits').scrollIntoViewIfNeeded();await shot('projects-fits-several');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('graph phone overflow: People, Organizations and Projects fit a 360 px screen, menus and the review box included');
}finally{await browser?.close();server.close()}
