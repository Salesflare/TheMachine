import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A person's, organization's or project's page on a phone: one ‹ People (Organizations, Projects) back link in place of
// the section's head and the breadcrumb, the name once (on the page), a 44 px tap target, nothing past the screen even
// with a long name. The link goes back to the list as the back gesture does: the list's place kept, no extra step, so
// the gesture after it leaves the list. A desktop keeps the head and the whole breadcrumb. BACKLINK_SHOT=<dir> writes
// screenshots at 360, 390 and 1440, light and dark, before the checks run.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const LONG='Maximiliane Konstantinopoulou-Vandenberghe';
const person=(i,name)=>({id:'email:p'+i+'@client.example',kind:'person',name,strength:2,closeness:'regular',last_at:day(i%9+1),signals:4,ids:['p'+i+'@client.example'],links:[],recent:[],around:[],open:{}});
const list=Array.from({length:40},(_,i)=>person(i,i===30?LONG:'Person '+String(i).padStart(2,'0')));
const org={id:'org:example.example',kind:'org',name:'Internationale Vereniging voor Duurzame Materiaalwetenschappen',strength:2,last_at:day(1),signals:3,ids:[],links:[],recent:[],around:[],open:{}};
const project={id:'project:1',kind:'project',name:'Battery materials rollout for the second production line',state:'active',strength:2,last_at:day(1),signals:3,ids:[],links:[],recent:[],around:[],open:{},
 project:{node_id:'project:1',name:'Battery materials rollout for the second production line',board_id:1,stage:'Demo',org:'example.example',value:0,notes:'',people:[],archived:false,outcome:null},board:{board:'Sales',stage:'Demo',moves:[]}};
const nodes=Object.fromEntries([...list,org,project].map(n=>[n.id,n]));
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');
  if(n){if(!nodes[n]){res.statusCode=404;res.end('{"error":"Not in the graph"}');return}res.end(JSON.stringify(nodes[n]));return}
  res.end(JSON.stringify({projects:[],people:list,quiet:[],new:[],orgs:[],boards:[],person_names:[],project_names:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',shotDir=process.env.BACKLINK_SHOT,errors=[];let browser;
const open=async(width,colorScheme='light')=>{const mobile=width<600,context=await browser.newContext({viewport:{width,height:844},isMobile:mobile,hasTouch:mobile,colorScheme,locale:'en-US'}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(`${width} ${colorScheme}: ${e.message}`));await page.goto(base);await page.waitForFunction(()=>typeof people==='function');
 await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());await page.locator('#people-view [data-graph-panel="people"] .graph-list').waitFor();
 return {context,page}};
// Opens a person from the list, as a tap does (graphOpen), after scrolling the list down
const openPerson=async(page,id)=>{await page.evaluate(()=>scrollTo(0,600));await page.waitForFunction(()=>scrollY>0);
 await page.evaluate(id=>graphOpen(id),id);await page.locator('#people-view .person-page>.name-row h3').waitFor()};
// The head, the breadcrumb's visible parts, the back link's box, how often the name shows, and what sticks out
const look=(page,name)=>page.evaluate(name=>{const vis=el=>el&&el.checkVisibility(),r=el=>el.getBoundingClientRect();
 const link=document.querySelector('.graph-crumbs>a[data-crumb]:not([data-crumb=""])'),box=link&&r(link);
 const shown=[...document.querySelectorAll('#page-head *,#people-view *')].filter(el=>vis(el)&&el.textContent.trim()===name&&![...el.children].some(c=>c.textContent.trim()===name));
 const vw=document.documentElement.clientWidth,out=[...document.querySelectorAll('#people-view *')].filter(el=>vis(el)&&r(el).width&&(r(el).right>vw+1||r(el).left<-1)).map(el=>el.className||el.tagName);
 return {head:vis(document.querySelector('#page-head')),crumbs:[...document.querySelectorAll('.graph-crumbs>*')].filter(vis).map(el=>el.textContent.trim()),
  link:link&&{text:link.textContent.trim(),before:getComputedStyle(link,'::before').content,w:box.width,h:box.height,left:box.left,right:box.right},names:shown.length,out,wide:document.documentElement.scrollWidth>innerWidth}},name);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 if(shotDir)for(const width of [360,390,1440])for(const scheme of ['light','dark']){const {context,page}=await open(width,scheme);
  await openPerson(page,list[30].id);await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${shotDir}/person-${width}-${scheme}.png`});
  for(const [id,name] of [[org.id,'org'],[project.id,'project']]){await page.evaluate(id=>people(id),id);await page.locator(`.graph-crumbs [aria-current]`,{hasText:nodes[id].name.slice(0,20)}).waitFor({state:'attached'});
   await page.screenshot({path:`${shotDir}/${name}-${width}-${scheme}.png`})}
  await context.close()}
 for(const width of [360,390]){const {context,page}=await open(width),tag=String(width);
  // Person: ‹ People alone, the name once, a 44 px target inside the screen
  await openPerson(page,list[30].id);const scrolled=await page.evaluate(()=>graphScroll),steps=await page.evaluate(()=>history.length);assert.ok(scrolled>0,`${tag}: the list was scrolled`);
  let m=await look(page,LONG);
  assert.equal(m.head,false,`${tag}: no section head on a person's page ${JSON.stringify(m)}`);
  assert.deepEqual(m.crumbs,['People'],`${tag}: only the back link shows ${JSON.stringify(m)}`);
  assert.match(m.link.before,/‹/,`${tag}: the link points back`);
  assert.ok(m.link.h>=44&&m.link.w>=44,`${tag}: a 44 px tap target ${JSON.stringify(m.link)}`);
  assert.ok(m.link.left>=0&&m.link.right<=width,`${tag}: the link is on the screen ${JSON.stringify(m.link)}`);
  assert.equal(m.names,1,`${tag}: the name shows once ${JSON.stringify(m)}`);
  const h=await page.locator('#people-view .person-page>.name-row h3').evaluate(h=>({cut:h.scrollHeight>h.clientHeight+1||h.scrollWidth>h.clientWidth+1,lines:Math.round(h.clientHeight/parseFloat(getComputedStyle(h).lineHeight))}));
  assert.ok(!h.cut&&h.lines===2,`${tag}: a long name shows whole, on two lines ${JSON.stringify(h)}`);
  assert.ok(!m.wide&&!m.out.length,`${tag}: nothing past the screen ${JSON.stringify(m)}`);
  assert.equal(await page.evaluate(()=>document.title),'The Machine · '+LONG,`${tag}: the tab still names the person`);
  // ‹ People goes back to the list where it was, without a new step: the back gesture after it leaves the list
  await page.locator('.graph-crumbs [data-crumb="people"]').click();await page.locator('[data-graph-panel="people"]:not([hidden])').waitFor();
  await page.waitForFunction(y=>Math.abs(scrollY-y)<2,scrolled);
  assert.equal(new URL(page.url()).hash,'#graph=people',tag);assert.equal(await page.evaluate(()=>history.length),steps,`${tag}: no extra step`);
  assert.ok(await page.locator('#page-head').isVisible(),`${tag}: the list has its head again`);
  await page.goForward();await page.locator('#people-view .person-page>.name-row h3').waitFor();
  // The back gesture from the page goes to the list too
  await page.goBack();await page.locator('[data-graph-panel="people"]:not([hidden])').waitFor();assert.equal(new URL(page.url()).hash,'#graph=people',tag);
  // A page reached some other way (a link): ‹ People still opens People
  await page.evaluate(id=>{location.hash='#graph/'+encodeURIComponent(id)},list[2].id);await page.locator('#people-view .person-page>.name-row h3',{hasText:'Person 02'}).waitFor();
  await page.locator('.graph-crumbs [data-crumb="people"]').click();await page.locator('[data-graph-panel="people"]:not([hidden])').waitFor();assert.equal(new URL(page.url()).hash,'#graph=people',tag);
  // Organization and project pages alike
  for(const [n,label] of [[org,'Organizations'],[project,'Projects']]){await page.evaluate(id=>people(id),n.id);await page.locator('.graph-crumbs [aria-current]',{hasText:n.name}).waitFor({state:'attached'});
   m=await look(page,n.name);assert.equal(m.head,false,`${tag} ${label}: no head`);assert.deepEqual(m.crumbs,[label],`${tag} ${label}: only ‹ ${label}`);
   assert.ok(m.link.h>=44,`${tag} ${label}: 44 px`);assert.ok(!m.wide&&!m.out.length,`${tag} ${label}: nothing past the screen ${JSON.stringify(m)}`)}
  await context.close()}
 // A desktop: the head and the whole breadcrumb, as before
 {const {context,page}=await open(1440);await openPerson(page,list[30].id);const m=await look(page,LONG);
  assert.equal(m.head,true,'1440: the section head stays');assert.equal(await page.locator('#page-head .page-title').textContent(),'People');
  assert.deepEqual(m.crumbs,['Graph','›','People','›',LONG],'1440: the whole breadcrumb');assert.equal(m.link.before,'none','1440: no back arrow');
  await page.locator('.graph-crumbs [data-crumb="people"]').click();await page.locator('[data-graph-panel="people"]:not([hidden])').waitFor();
  await page.goBack();await page.locator('#people-view .person-page>.name-row h3').waitFor();  // the breadcrumb is a step of its own there, as before
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('graph back link: ‹ People on a phone (360, 390), the head and breadcrumb on a desktop');
}finally{await browser?.close();server.close()}
