import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A catch-all project's page (project_spread.py): "Mixes 30 separate contacts, 26 never answered." with Split up… and
// Keep as one. Split up shows one project per contact who answered and the rest taken off; with only messages nobody
// answered, the button says Take them off. Keep as one posts op keep. Made-up names. At 390 and 1440.
// SHOT_DIR=… saves screenshots.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const fresh=()=>({id:'project:7',kind:'project',name:'Beta program',strength:1,last_at:day(1),signals:34,state:'active',ids:[],links:[],recent:[],around:[],open:{},
 about:null,split:null,spread:{groups:30,one_way:26},
 project:{node_id:'project:7',name:'Beta program',board_id:null,stage:null,org:null,value:null,close_date:null,notes:'',people:[],archived:false,outcome:null,outcome_reason:null}});
const items={'g:org:brightpath.example':{kind:'thread',label:'Brightpath',sub:'2 conversations',at:day(9)},
 'g:org:dunewave.example':{kind:'thread',label:'Dunewave',sub:'1 conversation',at:day(4)},
 'g:none':{kind:'thread',label:'Messages nobody answered',sub:'26 conversations',at:day(1)}};
let proposal,node=fresh();const calls=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')?node:{projects:[],people:[],quiet:[],new:[],orgs:[],boards:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);const a=call.args;
  if(a.op==='propose'){res.end(JSON.stringify(proposal));return}
  if(a.op==='keep'){node={...node,spread:null};res.end(JSON.stringify({kept:30}));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 if(process.env.SHOT_DIR)await mkdir(process.env.SHOT_DIR,{recursive:true});
 const shot=async(page,name)=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/${name}.png`})};
 const fits=(page,tag)=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth).then(ok=>assert.ok(ok,'no sideways scroll at '+tag));
 for(const [width,height] of [[390,844],[1440,900]]){
  node=fresh();calls.length=0;const tag=`${width}x${height}`;
  proposal={node_id:'project:7',name:'Beta program',parts:[{name:'Brightpath',items:['g:org:brightpath.example']},{name:'Dunewave',items:['g:org:dunewave.example']}],drop:['g:none'],items};
  const context=await browser.newContext({viewport:{width,height},timezoneId:'America/New_York'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#graph/'+encodeURIComponent(node.id));
  const card=page.locator('#people-view .graph-detail'),line=card.locator('.proj-spread');await line.waitFor();
  assert.equal((await line.textContent()).replace(/\s+/g,' ').trim(),'Mixes 30 separate contacts, 26 never answered. Split up… · Keep as one');
  await fits(page,tag);await shot(page,`spread-line-${tag}`);
  // Split up: one project per contact who answered, the rest taken off
  await line.locator('[data-proj-split]').click();
  const form=page.locator('#split-form');await form.locator('.psplit-part').first().waitFor();
  assert.deepEqual(await form.locator('[name="split-name"]').evaluateAll(a=>a.map(i=>i.value)),['Brightpath','Dunewave']);
  assert.equal((await form.locator('.psplit-rest h3').textContent()).trim(),'Taken off');
  assert.equal((await form.locator('button.primary').textContent()).trim(),'Split into 2 projects');
  await fits(page,tag+' preview');await shot(page,`spread-split-${tag}`);
  await form.locator('button.ghost[data-split-close]').click();await form.waitFor({state:'hidden'});
  // Nobody answered at all: the button takes them off
  proposal={...proposal,parts:[],items:{'g:none':items['g:none']}};
  await line.locator('[data-proj-split]').click();await form.locator('.psplit-rest').waitFor();
  const go=form.locator('button.primary');
  assert.equal((await go.textContent()).trim(),'Take them off');assert.equal(await go.isDisabled(),false);
  await form.locator('button.ghost[data-split-close]').click();await form.waitFor({state:'hidden'});
  // Keep as one
  await line.locator('[data-proj-keep]').click();await line.waitFor({state:'detached'});
  assert.deepEqual(calls.at(-1),{action:'project_split',args:{op:'keep',node_id:'project:7'}});
  assert.deepEqual(errors,[]);await context.close();
 }
 console.log('project spread dashboard ok');
}finally{await browser?.close();server.close()}
