import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A result that leaves the owner a step on a page (needs_you, with only links): the link is the lead button, in sight, and
// Mark done stays beside it, never the lead on something that hasn't happened (todos-cards.js cardActions). A finished result
// with a link, one already handled elsewhere, and one with a send keep their own lead, and so does an errand only the
// owner can do, a question, a draft to copy, a new run that stopped and one a teammate has.
const dashboard=await dashboardPage(),now=new Date().toISOString();
const todo=(id,outcome,next_actions,extra={})=>({id,title:'Post about the faster search',body:'The post is ready.',status:'prepared',scope:'work',created_at:now,event_ids:[1],outcome:JSON.stringify(outcome),next_actions,...extra});
const link={kind:'open',revision:'o1',label:'Open the forum',url:'https://forum.example.com/new'},NEEDS={state:'needs_you',needs:'Review and publish the post'};
const cards=[
 todo('left',NEEDS,[link]),
 todo('two',NEEDS,[link,{kind:'open',revision:'o2',label:'Open the guide',url:'https://forum.example.com/guide'}]),
 todo('fin',{state:'done'},[link]),
 todo('mine',NEEDS,[{...link,label:'Open in Maps'}],{owner_step:1}),
 todo('gone',NEEDS,[link],{handled_hint:JSON.stringify({reason:'It was posted this morning',event_ids:[],at:now})}),
 todo('ask',{state:'needs_you',needs:'Which account should it go out from?'},[link]),
 todo('copy',NEEDS,[link],{body:'The draft is ready.',result_files:[{index:0,name:'post.md',size:10}]}),
 todo('stopped',NEEDS,[link],{preparation_status:'blocked',preparation_error:'The run stopped',preparation_reason:'The run stopped'}),
 todo('mate',NEEDS,[link],{fleet_handoff:{stage:'asked',name:'Ann Baker'}}),
 todo('tab',NEEDS,[{kind:'open',revision:'b1',label:'Open in the browser',browser:true}]),
 todo('send',NEEDS,[link,{kind:'email',revision:'e1',label:'Send',to:['a@example.com'],subject:'Search',body:'Hi'}])];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const colorScheme of ['light','dark'])for(const width of [1440,390]){
  const context=await browser.newContext({colorScheme,viewport:{width,height:900},...(width<500?{isMobile:true,hasTouch:true}:{})});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#todos');
  await page.locator('#task-left').waitFor();
  const row=id=>page.locator('#task-'+id+' .actions').first(),why=`at ${width}`;
  const lead=async id=>(await row(id).locator(':scope>button.primary,:scope>a.primary').allInnerTexts()).map(x=>x.replace('↗','').trim());
  for(const id of ['left','two']){
   assert.deepEqual(await lead(id),['Open the forum'],`${id}: the link leads ${why}`);
   assert.equal(await row(id).locator(':scope>a.primary').getAttribute('href'),link.url);
   assert.ok(await page.locator(`#task-${id} [data-choice="complete"]`).count(),`${id}: Mark done is still there ${why}`)}
  assert.deepEqual(await lead('fin'),['Mark done'],`a finished result ${why}`);
  assert.deepEqual(await lead('mine'),['Mark done'],`an errand of their own, with a link to look at ${why}`);
  assert.equal(await page.locator('#task-gone a.primary').count(),0,`already handled: the link doesn’t lead ${why}`);
  // ones another step leads keep it: only the link of a result left to the owner is promoted
  for(const id of ['ask','copy','stopped','mate','tab'])assert.equal(await page.locator(`#task-${id} a.doc-open`).count(),0,`${id}: the link doesn’t lead ${why}`);
  assert.deepEqual(await lead('copy'),['Copy draft'],`a draft to copy ${why}`);
  assert.ok(!(await lead('mate')).includes('Open the forum'),`a teammate has it ${why}`);
  assert.deepEqual(await lead('tab'),['Mark done'],`a page in The Machine’s browser ${why}`);
  assert.deepEqual(await lead('send'),['Review and send'],`a send leads ${why}`);
  if(process.env.SHOTS)await page.locator('#task-left').screenshot({path:`${process.env.SHOTS}/open-lead-${width}-${colorScheme}.png`});
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
