import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// One count for For you: the header ("5 to-dos for you"), the stat tile, the For you section and the sidebar's For you all
// count the same items, Fleet asks among them. The sidebar once left the Fleet asks out (header 4, sidebar 2). The
// Fleet asks (a teammate waits) come before the prepared to-do, the ones that need a decision after it. A Fleet ask's
// sidebar row brings its card up, also from an open chat. Made-up data.
const dashboard=await dashboardPage(process.env.PAGE);
const FL='fl_'+'c'.repeat(16);
const card=(id,title,status)=>({id:id.repeat(16).slice(0,16),title,body:'Made-up to-do.',status,scope:'work',event_ids:[],created_at:new Date(Date.now()-36e5).toISOString()});
const cards=[card('a','Reply to Sam about the pilot','prepared'),card('b','Pick a date for the board call','pending'),card('c','Approve the new logo','pending')];
const graph={fleet:FL,name:'Acme',admin:true,confirmed:true,prompts:[],off:null,waiting:0,week:null,teammates:2,started:true,paused:null,require:[],connections:[],people:[],new_devices:[],sending:0};
const fleet={on:true,kinds:{},kind_rules:{},no_details:[],scoped:[],scopes:{},asked:[],log:[],notices:[],
 waiting:[{id:'w1',kind:'relationships',fleet:FL,member_id:'q',name:'Robin Vale',question:'Who knows someone at Initech?',at:new Date().toISOString()}],
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:[],people:[{member_id:'me',name:'Olive Park',role:'owner',me:true,email:'olive@acme.example'}],members:[],rules:{},exceptions:{}}],
 shared:{prompts:[{id:'p0',kind:'member',fleet:FL,fleet_name:'Acme',name:'Rae Moss',email:'rae@acme.example',fp:'ab12 cd34 ef56 ab12 cd34 ef56'}],shares:[],accounts:[],can_share:[],graph:[graph]}};
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status')return res.end(JSON.stringify({suggestions:cards,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},fleet:{on:true,waiting:2}}));
 if(url.pathname==='/api/graph')return res.end(JSON.stringify({projects:[],quiet:[],new:[],orgs:[],boards:[],people:[],sharing:[graph]}));
 if(url.pathname==='/api/fleet')return res.end(JSON.stringify(fleet));
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 for(const [width,height] of [[1440,900],[390,844]]){
  const context=await browser.newContext({viewport:{width,height},serviceWorkers:'block',locale:'en-US'}),page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');
  await page.locator('#suggestions #fleet-share-p0').waitFor();await page.locator('#suggestions #fleet-w1').waitFor();
  await page.waitForFunction(()=>/5 to-dos for you/.test(document.querySelector('.page-sub')?.textContent||''));
  const counts=await page.evaluate(()=>({header:+/(\d+) to-dos for you/.exec(document.querySelector('.page-sub').textContent)[1],
   tile:+document.querySelector('#suggestion-stats [data-fold-tile="foryou"] b').textContent,section:+document.querySelector('#section-foryou .count').textContent,
   side:+document.querySelector('#side-cards [data-side-fold="foryou"] .count').textContent,
   rows:[...document.querySelectorAll('#side-cards [data-side-fold="foryou"]~a')].map(a=>a.textContent.trim())}));
  assert.deepEqual({header:counts.header,tile:counts.tile,section:counts.section,side:counts.side},{header:5,tile:5,section:5,side:5},width+': '+JSON.stringify(counts));
  assert.equal(counts.rows.length,5,JSON.stringify(counts.rows));
  const at=t=>counts.rows.findIndex(r=>r.includes(t));
  assert.ok(Math.max(at('Rae Moss'),at('Robin Vale'))<at('Reply to Sam')&&at('Reply to Sam')<Math.min(at('Pick a date'),at('Approve the new logo')),
   'Fleet asks, then prepared, then the rest: '+JSON.stringify(counts.rows));
  assert.ok(counts.rows.includes('Rae Moss joined Acme. Share the team\'s Graph with them?'),JSON.stringify(counts.rows));
  assert.ok(counts.rows.includes('Robin Vale asks: Who knows someone at Initech?'),JSON.stringify(counts.rows));
  // From an open chat: the Fleet ask's row closes the chat and brings its card up, focused
  await page.evaluate(id=>{location.hash='#chat='+id},cards[1].id);await page.locator('body.chat-open').waitFor({state:'attached'});
  if(width<1024)await page.evaluate(()=>drawerOpen());
  await page.locator('#side-cards [data-side-fleet="fleet-w1"]').click();
  await page.waitForFunction(()=>document.activeElement?.id==='fleet-w1');
  assert.equal(await page.locator('body.chat-open').count(),0,'the chat closed');
  // it glides there (a smooth scroll), from where the chat's to-do was
  await page.waitForFunction(()=>{const r=document.querySelector('#fleet-w1').getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight},null,{timeout:5000}).catch(()=>{});
  const box=await page.locator('#fleet-w1').boundingBox();assert.ok(box&&box.y<height&&box.y+box.height>0,'the card is on screen');
  assert.deepEqual(errors,[]);
  await context.close();
 }
 console.log('todo counts dashboard ok');
}finally{await browser.close();server.close()}
