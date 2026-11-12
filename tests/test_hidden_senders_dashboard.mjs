import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Hidden senders: under People, a quiet entry with how many mailings the Graph left out. Their list loads only when it
// opens, each with its reason, and Show as a person tells the Machine to count that address from now on: the row says
// so and stays until the list loads again. On a phone and a desktop.
// HIDDEN_SHOT=<dir> writes screenshots of the open list, light and dark.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const person=(id,name)=>({id,kind:'person',name,strength:2,last_at:day(1),signals:3,ids:[id],links:[],recent:[],around:[],open:{}});
const HIDDEN=[{id:'email:pat@growth.example',address:'pat@growth.example',name:'Pat Vos',why:'list',mails:4,last_at:day(2)},
 {id:'email:lee@moss.example',address:'lee@moss.example',name:'Lee Moss',why:'reply_to',mails:1,last_at:day(5)},
 {id:'email:community@paperbox.example',address:'community@paperbox.example',name:'Paperbox',why:'company',mails:25,last_at:day(9)}];
let calls,lists;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){calls.push(JSON.parse(body));res.end(JSON.stringify({identifier:JSON.parse(body).args.identifier,shown:true}));return}
 if(url.pathname==='/api/graph/list'){const list=url.searchParams.get('list');lists.push(list);
  res.end(JSON.stringify(list==='hidden_senders'?{items:HIDDEN,next:null,total:3}:list==='people'?{items:[person('email:ann@client.example','Ann Lee'),person('email:bo@client.example','Bo Ray')],next:null,total:2}:{items:[],next:null,total:0}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({list_counts:{people:2,quiet:0,new:0,work:0,personal:0,orgs:0,warmup:0,projects:0,projects_done:0},counts:{},
  people:[],orgs:[],projects:[],boards:[],owners:[],same_person:[],org_doubles:[],hidden_senders:3,person_names:[],project_names:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',shotDir=process.env.HIDDEN_SHOT,errors=[];let browser;
const pause=ms=>new Promise(r=>setTimeout(r,ms));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440])for(const scheme of shotDir?['light','dark']:['light']){const mobile=width<600,tag=String(width);calls=[];lists=[];
  const context=await browser.newContext({viewport:{width,height:844},isMobile:mobile,hasTouch:mobile,locale:'en-GB',colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(tag+': '+e.message));
  const press=l=>mobile?l.tap():l.click();
  await page.goto(base);await page.waitForFunction(()=>typeof people==='function');
  await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());
  const entry=page.locator('#people-view [data-graph-panel="people"] details.hidden-senders');
  await entry.locator('summary').waitFor();
  assert.equal((await entry.locator('summary').textContent()).replace(/\s+/g,' ').trim(),'Hidden senders (3)',`${tag}: the entry and its count`);
  await page.locator('#people-view article[data-node="email:ann@client.example"]').waitFor();
  await pause(300);
  assert.ok(!lists.includes('hidden_senders'),`${tag}: the list loads only when it opens`);
  assert.equal(await entry.evaluate(d=>d.open),false,`${tag}: closed at first`);
  assert.equal(await entry.locator('.graph-note').isVisible(),false,`${tag}: the explainer shows when it opens`);
  await press(entry.locator('summary'));
  await entry.locator('.hidden-sender').nth(2).waitFor();
  assert.deepEqual((await entry.locator('.hidden-sender .graph-sub:not(.role-row)').allTextContents()).map(s=>s.split(' · ').slice(0,2).join(' · ')),
   ['Sent to a list · 4 emails','Replies go elsewhere · 1 email','Sent as a company · 25 emails']);
  const box=await entry.boundingBox(),view=page.viewportSize();
  assert.ok(box.x>=0&&box.x+box.width<=view.width+1,`${tag}: the list fits the page`);
  await press(entry.locator('[data-show-person="email:lee@moss.example"]'));
  await entry.locator('.hidden-sender').nth(1).locator('.hs-said').waitFor();
  const indent=sel=>entry.locator(sel).evaluate(el=>Math.round(el.getBoundingClientRect().left));
  assert.equal(await indent('.hidden-sender:nth-child(2) .hs-said'),await indent('.hidden-sender:nth-child(3) .hs-show'),`${tag}: done and to-do line up`);
  if(mobile)assert.equal(await indent('.hidden-sender:nth-child(3) .hs-show'),await indent('.hidden-sender:nth-child(3) strong'),`${tag}: under the line, with the name`);
  assert.deepEqual(calls.map(c=>[c.action,c.args.identifier]),[['graph_show_person','email:lee@moss.example']]);
  assert.equal(await entry.locator('.hidden-sender').count(),3,`${tag}: the row stays, with what was done`);
  assert.equal(await entry.locator('[data-show-person]').count(),2);
  // The top bar stays at the top of the screen, wherever the page is scrolled
  await entry.evaluate(d=>d.scrollIntoView({block:'start'}));await pause(200);
  const bar=await page.evaluate(()=>[...document.querySelectorAll('header,.topbar,.mobile-bar')].filter(e=>e.checkVisibility()&&getComputedStyle(e).position.match(/fixed|sticky/)).map(e=>Math.round(e.getBoundingClientRect().top)));
  assert.ok(bar.every(top=>top<=0),`${tag}: the top bar stays on top: ${bar}`);
  if(shotDir)await page.screenshot({path:`${shotDir}/hidden-senders-${tag}-${scheme}.png`});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('hidden senders dashboard ok');
}finally{await browser?.close();server.close()}
