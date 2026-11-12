import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// People's search after a merge: two records of one name were merged, the dashboard said Merged., and the same search
// still showed both. A search kept the rows it loaded for as long as the dashboard was open; an edit now asks again.
// MERGE_SHOT=<dir> writes the search before and after the merge, at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString().slice(0,10);
const person=(id,extra)=>({id,kind:'person',name:'Robin Vale',strength:1,last_at:day(1),signals:2,ids:[],links:[],edited:[],joined:[],...extra});
const work=person('email:robin@client.example',{ids:['robin@client.example'],role:'customer',emails:[{value:'robin@client.example',by:'messages'}],closeness:'close'});
const phone=person('wa:15550100',{ids:['+15550100'],phones:[{value:'+15550100',by:'messages'}],closeness:'occasional'});
let merged=false;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){const b=JSON.parse(body);if(b.action==='graph_same'&&b.args.same)merged=true;res.end(JSON.stringify({ok:true}));return}
 if(url.pathname==='/api/graph/list'){res.end(JSON.stringify({items:[],next:null,total:0}));return}
 if(url.pathname==='/api/graph'&&url.searchParams.get('q')){
  const one={...work,ids:['+15550100','robin@client.example'],phones:phone.phones};
  res.end(JSON.stringify({found:merged?[one]:[work,phone],next:null}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({list_counts:{people:2,quiet:0,new:0,work:0,personal:0,orgs:0,warmup:0,projects:0,projects_done:0},counts:{},
  people:[],orgs:[],projects:[],boards:[],owners:[],same_person:[],org_doubles:[],person_names:[],project_names:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',shotDir=process.env.MERGE_SHOT,errors=[];let browser;
const rows=page=>page.locator('#people-view .graph-found [data-node]').evaluateAll(els=>[...new Set(els.map(e=>e.dataset.node))]);
const until=async(page,n,what)=>{for(const end=Date.now()+10000;(await rows(page)).length!==n&&Date.now()<end;)await new Promise(r=>setTimeout(r,50));assert.equal((await rows(page)).length,n,what)};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440])for(const scheme of shotDir?['light','dark']:['light']){const tag=`${width}-${scheme}`;merged=false;
  const context=await browser.newContext({viewport:{width,height:844},isMobile:width<600,locale:'en-GB',colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(tag+': '+e.message));
  await page.goto(base);await page.waitForFunction(()=>typeof people==='function');
  await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());
  await page.fill('#people-query','robin v');await page.click('#people-find');
  await until(page,2,tag+': both records before the merge');
  if(shotDir)await page.screenshot({path:`${shotDir}/search-${tag}-before.png`});
  await page.evaluate(()=>graphPost('graph_same',{a:'email:robin@client.example',b:'wa:15550100',same:true}));
  await page.click('#people-find');  // the same search again
  await until(page,1,tag+': one record after the merge, not the rows from before it');
  assert.deepEqual(await rows(page),['email:robin@client.example']);
  if(shotDir)await page.screenshot({path:`${shotDir}/search-${tag}-after.png`});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('people search after merge dashboard ok');
}finally{await browser?.close();server.close()}
