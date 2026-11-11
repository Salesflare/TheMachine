import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Graph and Connections have sub-tabs like Fleet: a pill row over panes. Links open the right one (#graph=orgs,
// #connections=chat, and the old #people and #health), a source that needs attention shows on its sub-tab, section
// heads keep their heading on one line, and every tab has the same column width. Graph's tab has no count (no Who's who);
// a tab shows a number only when something needs the owner (Sign-ins never). At 390px the row scrolls with a fade.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),day=now.slice(0,10);
const person=(n,i)=>({id:'email:p'+i+'@example.org',kind:'person',name:n,strength:3-i/10,closeness:'regular',last_at:day,signals:4,ids:['p'+i+'@example.org']});
let graph={people:['Ann Example','Bo Sample','Cy Test'].map(person),quiet:[],new:[],
 projects:[{id:'project:1',kind:'project',name:'Renewal',state:'active',last_at:day,signals:3,people:['Ann Example']}],
 orgs:[{id:'org:example.org',kind:'org',name:'Example Org',signals:2,last_at:day}],warmup:[]};
const conn=(id,service,extra={})=>({id,service,display_name:id,email:'owner@example.org',boundary:'work',last_success:now,state:'{}',...extra});
const connectors=[conn('mail','gmail'),conn('cal','calendar'),conn('team-chat','slack',{error:'slack_auth_failed'}),conn('wa','whatsapp'),conn('phone','android'),conn('crm','salesflare')];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(graph));return}
 if(url.pathname==='/api/events'){res.end('[]');return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='browser_logins'){res.end(JSON.stringify({logins:[{site:'crm.example.org',username:'owner'}]}));return}}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const tabs=(page,row)=>page.locator(row+' [role=tab]').allInnerTexts();
const selected=(page,row)=>page.locator(row+' [role=tab][aria-selected="true"]').innerText();
const rows=page=>page.locator('.side-sub a:not([hidden])').evaluateAll(a=>a.map(x=>x.querySelector('.nl').textContent+(x.querySelector('.badge').textContent?'\n'+x.querySelector('.badge').textContent:'')));
const lit=page=>page.locator('.side-sub a[aria-current="page"] .nl').textContent();
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1280,height:900}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);
 // Graph: its panes are rows in the sidebar (no pills on the page): People, Organizations, Projects. No Who's who row, and
 // nothing counted on the Graph row.
 await navClick(page.locator('nav [data-tab="people"]'));
 await page.locator('[data-graph-panel="people"]:not([hidden])').waitFor();assert.equal(await page.locator('#people-view [data-graph-pane]').count(),0);
 assert.deepEqual(await rows(page),['People','Organizations','Projects']);
 assert.equal(await page.locator('.side-sub a[data-graph-sub="roles"]').count(),0);
 assert.equal(await page.locator('#badge-people').textContent(),'');
 assert.equal(await lit(page),'People');assert.equal(await page.locator('#page-head .page-title').textContent(),'People');
 await navClick(page.locator('.side-sub a[data-graph-sub="orgs"]'));
 await page.locator('[data-graph-panel="orgs"]:not([hidden])').waitFor();
 assert.equal(await page.locator('#people-view [data-graph-panel="people"]').isHidden(),true);
 // The choice is kept; a link picks one; the old Who's who link opens People.
 await page.goto(base);await navClick(page.locator('nav [data-tab="people"]'));await page.locator('[data-graph-panel="orgs"]:not([hidden])').waitFor();
 assert.equal(await lit(page),'Organizations');
 await page.goto(base+'/#graph=people');await page.locator('[data-graph-panel="people"]:not([hidden])').waitFor();
 await page.goto(base+'/#graph=roles');await page.locator('#people:not([hidden])').waitFor();
 await page.goto(base+'/#graph=projects');await page.locator('[data-graph-panel="projects"]:not([hidden])').waitFor();
 assert.equal(await page.locator('#people').isVisible(),true);assert.equal(await page.evaluate(()=>location.hash),'#graph=projects');  // the pane stays in the address
 // A redraw that ends between a pane link and its hashchange (a busy page) keeps the link: the old pane is not put back
 await page.goto(base+'/#graph=people');await page.locator('[data-graph-panel="people"]:not([hidden])').waitFor();
 await page.evaluate(()=>{location.hash='#graph=projects';graphHashSync()});
 await page.locator('[data-graph-panel="projects"]:not([hidden])').waitFor({timeout:3000});assert.equal(await page.evaluate(()=>location.hash),'#graph=projects');
 // A pane picked on the page (showTab, as the app does) goes in the address, so the next status refresh keeps it
 await page.goto(base+'/#graph=orgs');await page.locator('[data-graph-panel="orgs"]:not([hidden])').waitFor();
 await page.evaluate(()=>showTab('people','projects'));await page.locator('[data-graph-panel="projects"]:not([hidden])').waitFor();
 assert.equal(await page.evaluate(()=>location.hash),'#graph=projects');await page.evaluate(()=>openTabLink());
 assert.equal(await page.locator('[data-graph-panel="projects"]').isVisible(),true);
 await page.goto(base+'/#people');await page.locator('#people:not([hidden])').waitFor();
 // Connections: sources by kind; the one with a failing source shows its count and opens first.
 await page.goto(base);await navClick(page.locator('nav [data-tab="health"]'));await page.locator('#health-tabs [role=tab]').first().waitFor();
 for(let i=0;i<100&&(await tabs(page,'#health-tabs')).length<6;i++)await page.waitForTimeout(20);
 // A number only where something needs you: Chat has a failing source; a saved sign-in needs nothing, so Sign-ins has none
 assert.deepEqual(await tabs(page,'#health-tabs'),['Mail and calendar','Chat\n1','Other sources','+ Add','Sign-ins','Checks']);
 assert.equal(await page.locator('#health-tabs [data-health-pane="signins"] .badge').count(),0);
 assert.equal(await page.locator('#health-tabs [data-health-pane="chat"] .badge.warn').count(),1);
 assert.equal(await selected(page,'#health-tabs'),'Chat\n1');
 assert.deepEqual(await page.locator('#connectors>article:not([hidden]) h3').allInnerTexts(),['team-chat','wa']);
 await page.locator('#health-tabs [data-health-pane="signins"]').click();
 await page.locator('#saved-logins-block').waitFor();assert.equal(await page.locator('#connectors>article:not([hidden])').count(),0);
 assert.equal(await page.locator('#review-summary').isVisible(),false);
 await page.goto(base+'/#connections=reviews');await page.locator('#review-summary').waitFor({state:'attached'});
 for(let i=0;i<100&&await selected(page,'#health-tabs').catch(()=>'')!=='Checks';i++)await page.waitForTimeout(20);
 assert.equal(await selected(page,'#health-tabs'),'Checks');
 // Android is in Other sources; the old phone link opens it.
 await page.goto(base+'/#connections=phone');await page.locator('#connectors>article:not([hidden]) h3',{hasText:'phone'}).waitFor();
 assert.deepEqual(await page.locator('#connectors>article:not([hidden]) h3').allInnerTexts(),['phone','crm']);
 await page.goto(base+'/#health');await page.locator('#health:not([hidden])').waitFor();
 // One column for every tab.
 const widths=[];
 for(const t of ['inbox','events','people','feedback','health']){await page.evaluate(t=>showTab(t),t);await page.waitForTimeout(100);widths.push(await page.locator('#'+t).evaluate(e=>Math.round(e.getBoundingClientRect().width)))}
 // Events opens with the latest signals (here none), never an empty page
 await page.evaluate(()=>showTab('events'));await page.waitForFunction(()=>/No matching messages/.test(document.querySelector('#results').textContent));
 assert.equal(new Set(widths).size,1,widths.join());
 // A phone: the sub-tab row scrolls sideways inside itself, with a fade on the side that has more.
 await page.setViewportSize({width:390,height:844});await page.goto(base+'/#connections=mail');await page.locator('#health-tabs [role=tab]').first().waitFor();
 for(let i=0;i<100&&!(await page.locator('#health-tabs .sub-tabs.more-right').count());i++)await page.waitForTimeout(20);
 assert.equal(await page.locator('#health-tabs .sub-tabs.more-right').count(),1);
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.locator('#health-tabs [data-health-pane="reviews"]').click();
 for(let i=0;i<100&&!(await page.locator('#health-tabs .sub-tabs.more-left').count());i++)await page.waitForTimeout(20);
 assert.equal(await page.locator('#health-tabs .sub-tabs.more-left').count(),1);  // the chosen one scrolled into view
 // Out of sight, Connections' tabs are drawn but not measured: a redraw on another tab never lays the page out for them
 const measured=await page.evaluate(()=>{showTab('inbox');let n=0;const f=tabsShow;tabsShow=(...a)=>{if(a[0]?.closest('#health-tabs'))n++;return f(...a)};try{render()}finally{tabsShow=f}return n});
 assert.equal(measured,0,'no measuring for a hidden Connections');
 assert.deepEqual(errors,[]);
 console.log('sub-tabs dashboard ok');
}finally{await browser?.close();server.close()}
