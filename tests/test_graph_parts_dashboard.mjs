import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Graph comes in parts so a click paints at once. A person's page draws its head (api/graph?node=…&part=head) while
// the timeline is still on its way, then the whole page in the same place. The Projects board draws first and its
// follow-up lines (api/graph/follow-ups) come after it. GRAPH_PARTS_SHOT=<dir> writes screenshots.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const person={id:'person:a',kind:'person',name:'Ada Lovelace',strength:2,last_at:day(1),signals:3,ids:[],links:[],around:[],open:{},profile:{title:'Head of procurement'}};
const event={id:7,kind:'gmail.message',type:'event',title:'Pricing for the pilot',occurred_at:day(1),from:'Ada Lovelace',preview:'Could you send the pricing?'};
const stages=[{name:'Invited'},{name:'Testing'},{name:'Live'}];
const boards=[{id:1,name:'Alpha testers',stages,side:false,visibility:'team',projects:[{id:'project:5',name:'Ember labs',stage:'Testing',reason:'they installed it',
 by:'review',at:day(3),event_id:105,first:false,days:3,no_reply_days:0,org:{name:'Ember labs',logo:null}}]}];
// Ada's whole page waits until the test lets it go. Only hers: a record fetched ahead (a pointer over a board tile, which
// under load can come late) answers at once, so it never takes the place of hers in the queue.
const held=[],release=()=>{for(const r of held.splice(0))r()};let wholeAsked=0,headAsked=0,fuAsked=0;
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph/follow-ups'){fuAsked++;res.end(JSON.stringify({boards:{1:{on:true,next_at:null}},projects:{'project:5':{state:'paused'}}}));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');
  if(n&&url.searchParams.get('part')==='head'){headAsked++;res.end(JSON.stringify({...person,recent:[],owners:[],head_only:true}));return}
  if(n&&n!==person.id){res.end(JSON.stringify({id:n,kind:'project',name:'Ember labs',ids:[],links:[],around:[],open:{}}));return}
  if(n){wholeAsked++;await new Promise(r=>held.push(r));res.end(JSON.stringify({...person,recent:[event],timeline:{items:[],upcoming:[],sources:{email:1}}}));return}
  res.end(JSON.stringify({projects:[],people:[],quiet:[],new:[],orgs:[],boards,person_names:[],project_names:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',shotDir=process.env.GRAPH_PARTS_SHOT,errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[1440,900,'light'],[390,844,'dark'],...(shotDir?[[1440,900,'dark'],[390,844,'light']]:[])]){
  const mobile=width<600,tag=`${width}-${scheme}`;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(tag+': '+e.message));
  // The board first, its follow-up line after
  await page.goto(base+'#graph=projects');await page.locator('#people-view .pboard').first().waitFor();
  await page.locator('#people-view .fu-state',{hasText:'Follow-ups on'}).waitFor();
  assert.ok(fuAsked>0,tag);
  await page.locator('#people-view .tile-fu',{hasText:'Paused'}).waitFor();
  if(shotDir)await page.screenshot({path:`${shotDir}/board-${tag}.png`});
  // A quiet refresh (each poll) draws the board once, with the follow-ups it was last given: not without them and again
  const fu=fuAsked,redraws=await page.evaluate(async()=>{let n=0;const real=boardRedraw;window.boardRedraw=()=>{n++;real()};
   try{await people(graphNode,true)}finally{window.boardRedraw=real}return n});
  assert.deepEqual([redraws,fuAsked-fu],[0,0],tag);
  assert.equal(await page.locator('#people-view .tile-fu',{hasText:'Paused'}).count(),1,tag);
  // A person: the head while the whole page is held back, then the timeline in the same place
  const heads=headAsked;await page.evaluate(()=>{people('person:a')});  // not awaited: the whole page is held back
  await page.locator('#people-view .person-page').waitFor();
  assert.ok(headAsked>heads&&held.length>0,tag);
  assert.match(await page.locator('#people-view').innerText(),/Ada Lovelace/,tag);
  await page.locator('#people-view .graph-timeline .pager-loading').waitFor();
  if(shotDir)await page.screenshot({path:`${shotDir}/head-${tag}.png`});
  await page.evaluate(()=>scrollTo({top:40}));const before=await page.evaluate(()=>scrollY);
  release();
  await page.locator('#people-view .graph-timeline',{hasText:'Pricing for the pilot'}).waitFor();
  assert.equal(await page.locator('#people-view .graph-timeline .pager-loading').count(),0,tag);
  assert.equal(await page.evaluate(()=>scrollY),before,`the whole page keeps the reader's place ${tag}`);
  if(shotDir)await page.screenshot({path:`${shotDir}/whole-${tag}.png`});
  // A quiet refresh asks only for the whole page
  const h2=headAsked,w2=wholeAsked;const quiet=page.evaluate(()=>people(graphNode,true));quiet.catch(()=>{});
  for(const end=Date.now()+10000;!held.length&&Date.now()<end;)await page.waitForTimeout(25);release();await quiet;
  assert.deepEqual([headAsked-h2,wholeAsked-w2],[0,1],tag);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('graph parts: the board then its follow-ups, a person\'s head then the whole page in place, a quiet refresh asks once');
}finally{await browser?.close();server.close()}
