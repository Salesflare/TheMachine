import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Same person? and Same organization?, tapped through fast: Merge on one row, then the next, while the Machine is still
// saving the first. Every redraw in between (the first answer's, a poll's) came from a Machine that hadn't stored the
// later answers yet, so tapped pairs came back with their buttons, and rows jumped under the finger as answered ones
// went. Now an answered pair keeps its place with its answer, and the rows below it never move. A slow Machine here:
// each answer is stored only when its reply goes out. On a phone and a desktop.
// Then the answered pairs go: a few seconds after the last tap, and at once on leaving People and coming back. They
// stayed for good, with a count of 0 over rows that only said Merged., as long as the dashboard stayed open: People
// opened from the menu was a quiet refresh, which kept every answered row. A list with nothing left to ask goes too.
// SAME_SHOT=<dir> writes screenshots of the answered lists and of the lists after, light and dark.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const node=(kind,id,name,extra={})=>({id,kind,name,strength:2,last_at:day(1),signals:3,ids:[],links:[],recent:[],around:[],open:{},...extra});
const person=(i,domain)=>node('person','person:p'+i+domain,'Person '+'ABCD'[i],{ids:['email:p'+i+'@'+domain+'.example']});
const org=(i,domain)=>node('org','org:'+domain+i+'.example','Org '+'ABCD'[i],{domain:domain+i+'.example'});
let state,calls;
const reset=()=>{calls=[];state={people:[0,1,2,3].map(i=>({a:person(i,'one'),b:person(i,'two'),why:'Same name'})),
 orgs:[0,1,2,3].map(i=>({a:org(i,'one'),b:org(i,'two'),why:'Same name'}))}};
const pause=ms=>new Promise(r=>setTimeout(r,ms));
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){const b=JSON.parse(body);calls.push(b);await pause(700);  // stored when the reply goes
  if(b.action==='graph_same')state.people=state.people.filter(s=>!(s.a.id===b.args.a&&s.b.id===b.args.b));
  if(b.action==='graph_org_merge')state.orgs=state.orgs.filter(s=>s.b.id!==b.args.node_id);
  res.end(JSON.stringify(b.action==='graph_org_merge'?{node_id:b.args.into}:{ok:true}));return}
 if(url.pathname==='/api/graph/list'){res.end(JSON.stringify({items:[],next:null,total:0}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({list_counts:{people:0,quiet:0,new:0,work:0,personal:0,orgs:0,warmup:0,projects:0,projects_done:0},counts:{},
  people:[],orgs:[],projects:[],boards:[],owners:[],same_person:state.people,org_doubles:state.orgs,person_names:[],project_names:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',shotDir=process.env.SAME_SHOT,errors=[];let browser;
const until=async(test,what)=>{for(const end=Date.now()+20000;!test()&&Date.now()<end;)await pause(50);assert.ok(test(),what)};
// Watches the list from inside the page: a tapped pair with its buttons again, or the last row (never tapped) moving
const watch=(page,buttons)=>page.evaluate(sel=>{window.seen={back:[],moved:[]};const last=()=>document.querySelector(sel.last)?.closest('.same-pair')?.getBoundingClientRect().top;
 const top=last(),gone=new Set();window.seenStop=setInterval(()=>{for(const b of sel.tapped){const on=document.querySelector(b)?.checkVisibility();if(!on)gone.add(b);else if(gone.has(b))seen.back.push(b)}
  const now=last();if(now===undefined||Math.abs(now-top)>1)seen.moved.push(now)},15)},buttons);
const seen=async page=>page.evaluate(()=>{clearInterval(seenStop);return {back:[...new Set(seen.back)],moved:seen.moved.length}});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440])for(const scheme of shotDir?['light','dark']:['light']){const mobile=width<600,tag=String(width);
  const context=await browser.newContext({viewport:{width,height:844},isMobile:mobile,hasTouch:mobile,locale:'en-GB',colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(tag+': '+e.message));page.on('dialog',d=>d.accept());
  const press=l=>mobile?l.tap():l.click();
  for(const list of ['people','orgs']){reset();
   await page.goto(base);await page.waitForFunction(()=>typeof people==='function');
   await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());
   if(list==='orgs')await page.evaluate(()=>document.querySelector('[data-graph-sub="orgs"]').click());
   const panel=`#people-view [data-graph-panel="${list}"]`,pairs=state[list];
   const merge=i=>list==='people'?`${panel} [data-same="1"][data-a="${pairs[i].a.id}"]`:`${panel} [data-org-merge="${pairs[i].b.id}"]`;
   await page.locator(merge(3)).waitFor();
   await watch(page,{tapped:[0,1,2].map(merge),last:merge(3)});
   for(const i of [0,1,2]){await press(page.locator(merge(i)));await pause(150)}  // the next tap while the last is saving
   const action=list==='people'?'graph_same':'graph_org_merge';
   await until(()=>calls.filter(c=>c.action===action).length===3,list+': three merges sent');
   await pause(1200);  // every reply in, and the redraws after them (still before the answered pairs go)
   const got=await seen(page);
   assert.deepEqual(got.back,[],`${list} ${tag}: a merged pair came back with its buttons`);
   assert.equal(got.moved,0,`${list} ${tag}: the rows under the finger moved`);
   assert.equal(await page.locator(`${panel} .same-pair`).count(),4,`${list} ${tag}: answered pairs keep their place`);
   assert.deepEqual(await page.locator(`${panel} .same-pair .role-row .muted`).allTextContents(),['Merged.','Merged.','Merged.']);
   assert.equal(await page.locator(`${panel} .section-head .count`).first().textContent(),'1',`${list} ${tag}: the count is the open pairs`);
   if(shotDir)await page.screenshot({path:`${shotDir}/${list}-${tag}-${scheme}.png`});
   // A few seconds after the last answer the answered pairs go by themselves; the pair still open keeps its buttons
   await page.locator(`${panel} .same-pair`).nth(1).waitFor({state:'detached',timeout:6000});
   assert.equal(await page.locator(`${panel} .same-pair`).count(),1,`${list} ${tag}: answered pairs go after a moment`);
   assert.equal(await page.locator(merge(3)).count(),1);
   // The last one: answered, then To-dos and back to People from the menu (a quiet refresh) before it settles. The pair
   // is gone at once, and with nothing left to ask so is the list's heading and its count of 0
   await press(page.locator(merge(3)));await until(()=>calls.filter(c=>c.action===action).length===4,list+': the fourth merge sent');
   await page.locator(`${panel} .pair-said`).waitFor();
   if(shotDir)await page.screenshot({path:`${shotDir}/${list}-${tag}-${scheme}-last.png`});
   state[list].unshift(pairs[3]);  // a Machine that still lists it (a slow rebuild) never brings it back
   await page.evaluate(()=>document.querySelector('nav [data-tab="inbox"]').click());
   await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());
   if(list==='orgs')await page.evaluate(()=>document.querySelector('[data-graph-sub="orgs"]').click());
   assert.equal(await page.locator(`${panel} .same-pair`).count(),0,`${list} ${tag}: an answered pair stays after leaving People`);
   await pause(1200);  // the quiet refresh in
   assert.equal(await page.locator(`${panel} .same-pair`).count(),0,`${list} ${tag}: a late list brought an answered pair back`);
   assert.equal(await page.locator(`${panel} .section-head h2`).filter({hasText:/^Same/}).count(),0,`${list} ${tag}: nothing left to ask, the heading stays`);
   if(shotDir)await page.screenshot({path:`${shotDir}/${list}-${tag}-${scheme}-after.png`});
   // Once the Machine no longer lists it, the answer is forgotten: a pair that is asked again later shows its buttons
   state[list]=state[list].filter(s=>s!==pairs[3]);await page.evaluate(()=>people(null));
   state[list]=[pairs[3]];await page.evaluate(()=>people(null));
   assert.equal(await page.locator(merge(3)).count(),1,`${list} ${tag}: asked again later`)}
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('same pair taps dashboard ok');
}finally{await browser?.close();server.close()}
