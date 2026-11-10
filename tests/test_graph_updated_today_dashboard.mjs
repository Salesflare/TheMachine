import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// What The Machine updated today (graph_updates.py): one quiet line on top of People and Projects ("Updated 2 people
// today"), none on a list it didn't touch, a still dot on each row and board tile it changed, and the line opens what
// changed; a name there opens its page with Recent changes open. Nothing animates.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),day=now.slice(0,10);
const person=(i,marked)=>({id:'email:p'+i+'@example.org',kind:'person',name:'Person '+i,strength:3-i/10,closeness:'regular',last_at:day,signals:4,ids:['p'+i+'@example.org'],...(marked?{updated_at:now}:{})});
const project={id:'project:1',kind:'project',name:'Example rollout',state:'active',last_at:day,signals:3,people:[]};
const graph={list_counts:{people:3,quiet:0,new:0,work:0,personal:0,orgs:1,warmup:0,projects:1,projects_done:0},counts:{person:3,org:1,project:1},
 boards:[{id:1,name:'Pilots',stages:[{name:'Talking'},{name:'Live'}],projects:[{...project,stage:'Live',days:0}]}],
 updated_today:{since:day+'T00:00:00+00:00',people:{count:2,items:[{id:'email:p0@example.org',name:'Person 0',at:now,change:{kind:'role',role:'head of ops'}},
  {id:'email:p2@example.org',name:'Person 2',at:now,change:{kind:'fact',text:'Prefers calls in the morning'}}]},
  orgs:{count:0,items:[]},projects:{count:1,ids:['project:1'],items:[{id:'project:1',name:'Example rollout',at:now,change:{kind:'move',stage:'Live'}}]}}};
const lists={people:[person(0,true),person(1,false),person(2,true)],orgs:[{id:'org:co.example',kind:'org',name:'Example Co',signals:2,last_at:day}],projects:[{...project,updated_at:now}]};
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph/list'){res.end(JSON.stringify({items:lists[url.searchParams.get('list')]||[],next:null}));return}
 if(url.pathname==='/api/graph'&&url.searchParams.get('node')){res.end(JSON.stringify({...person(0),links:[],timeline:null,log:[{kind:'role',role:'head of ops',at:now}]}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(graph));return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){
  const phone=width<600,context=await browser.newContext({viewport:{width,height},isMobile:phone,hasTouch:phone}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  const base='http://127.0.0.1:'+server.address().port;
  await page.goto(base+'/#graph=people');
  await page.locator('[data-graph-panel="people"] article[data-node]').first().waitFor();
  const line=page.locator('[data-graph-panel="people"] .graph-today');
  assert.equal((await line.locator('summary').textContent()).trim(),'Updated 2 people today');
  assert.equal(await line.evaluate(d=>d.open),false);
  // The marked rows: Person 0 and Person 2, not Person 1; the dot holds still
  assert.deepEqual(await page.$$eval('[data-graph-panel="people"] article[data-node]',a=>a.filter(x=>x.querySelector('.today-mark')).map(x=>x.dataset.node)),['email:p0@example.org','email:p2@example.org']);
  assert.equal(await page.locator('[data-graph-panel="people"] article .today-mark').first().getAttribute('aria-label'),'Updated today');
  assert.deepEqual(await page.$$eval('.today-mark',m=>[...new Set(m.map(x=>getComputedStyle(x).animationName))]),['none']);
  // No line where nothing changed today
  await page.goto(base+'/#graph=orgs');await page.locator('[data-graph-panel="orgs"]:not([hidden])').waitFor();
  assert.equal(await page.locator('[data-graph-panel="orgs"] .graph-today').count(),0);
  // Projects: the line, and the board tile carries the mark too
  await page.goto(base+'/#graph=projects');await page.locator('[data-graph-panel="projects"]:not([hidden])').waitFor();
  assert.equal((await page.locator('[data-graph-panel="projects"] .graph-today summary').textContent()).trim(),'Updated 1 project today');
  assert.equal(await page.locator('.tile[data-node="project:1"] .today-mark').count(),1);
  // Open the line: what changed, by name; a name opens its page with Recent changes open
  await page.goto(base+'/#graph=people');await line.locator('summary').waitFor();
  await line.locator('summary').click();
  assert.deepEqual(await line.locator('.today-list button').allTextContents(),['Person 0','Person 2']);
  assert.deepEqual(await line.locator('.today-what').allTextContents(),['Role: Head of ops','Prefers calls in the morning']);
  await line.locator('[data-today-open="email:p0@example.org"]').click();
  await page.waitForSelector('#people.graph-on-node');
  await page.locator('.rc-fold[open]').waitFor();
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('graph updated today dashboard: ok');
}finally{await browser?.close();server.close()}
