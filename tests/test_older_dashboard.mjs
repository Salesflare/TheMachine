import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Older on the dashboard (dashboard/todos-older.js, todos-rows.js isOlder, still_needed.older): an open to-do with nothing
// new for a week leaves For you for Older, folded below it, also in the sidebar. One due soon or with a send on its way
// stays in For you whatever its age. Dismiss all asks once, then marks each Not needed (the to-do's own decide, so the
// learning is the same), and its Undo reopens them all. Made-up to-dos only.
const dashboard=await dashboardPage();
const day=864e5,at=n=>new Date(Date.now()-n*day).toISOString(),posts=[];
const OLD1='a1'.repeat(8),OLD2='b2'.repeat(8),DUE='c3'.repeat(8),SENDING='d4'.repeat(8),FRESH='e5'.repeat(8);
const today=()=>{const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};
let cards;
const reset=()=>{cards=[
 {id:OLD1,title:'Send the brochure',body:'They asked for the brochure.',status:'pending',scope:'work',created_at:at(12),event_ids:[1],older:at(12)},
 {id:OLD2,title:'Pick a paint color',body:'Before the painter comes.',status:'pending',scope:'personal',created_at:at(9),event_ids:[2],older:at(9)},
 {id:DUE,title:'Renew the domain',body:'',status:'pending',scope:'work',created_at:at(10),due:today(),event_ids:[3],older:at(10)},
 {id:SENDING,title:'Reply about the venue',body:'',status:'prepared',scope:'work',created_at:at(10),event_ids:[4],older:at(10),action_status:{status:'queued'}},
 {id:FRESH,title:'Book the venue',body:'',status:'pending',scope:'work',created_at:at(1),event_ids:[5]}]};
reset();
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='decide'){const c=cards.find(x=>x.id===b.args.suggestion_id);if(c)c.status=b.args.choice==='reject'?'rejected':b.args.choice==='undo'?'pending':c.status;res.end(JSON.stringify({status:c?.status}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const decided=()=>posts.filter(p=>p.action==='decide').map(p=>[p.suggestion_id,p.choice,p.feedback]);
const until=async f=>{for(let i=0;i<200&&!f();i++)await new Promise(r=>setTimeout(r,25))};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  posts.length=0;reset();
  const context=await browser.newContext({viewport:{width,height:900},timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+FRESH).waitFor();
  // Fresh first: For you holds the new one and the old ones due soon or sending; the rest wait folded in Older below it
  const forYou=await page.locator('#suggestions>article[id]').evaluateAll(n=>n.map(x=>x.id.slice(5)));
  assert.deepEqual(forYou.sort(),[DUE,SENDING,FRESH].sort());
  const older=page.locator('#older-list');
  assert.equal(await older.getAttribute('open'),null,'folded');
  assert.equal((await page.locator('#older-head').innerText()).replace(/\s+/g,' '),'Older 2');
  assert.equal(await older.locator('article[id]').count(),0,'its rows wait until it opens');
  assert.ok(await page.evaluate(()=>{const s=document.querySelector('#section-foryou'),o=document.querySelector('#older-list'),w=document.querySelector('#finished-list');return !!(s.compareDocumentPosition(o)&Node.DOCUMENT_POSITION_FOLLOWING)&&!!(o.compareDocumentPosition(w)&Node.DOCUMENT_POSITION_FOLLOWING)}),'under For you, above Done');
  if(width>1023){const side=page.locator('.side-head[data-side-fold="older"]');
   assert.equal((await side.innerText()).replace(/\s+/g,' ').trim(),'Older 2');assert.equal(await side.getAttribute('aria-expanded'),'false','folded in the sidebar too')}
  await page.locator('#older-head').click();
  assert.deepEqual(await older.locator('article[id]').evaluateAll(n=>n.map(x=>x.id.slice(5)).sort()),[OLD1,OLD2].sort());
  // Dismiss all asks first; Cancel leaves everything as it was
  await older.getByRole('button',{name:'Dismiss all'}).click();
  assert.match((await older.locator('.older-bar').innerText()).replace(/\s+/g,' '),/^Dismiss 2 to-dos\? Dismiss Cancel$/);
  await older.getByRole('button',{name:'Cancel'}).click();
  await older.getByRole('button',{name:'Dismiss all'}).waitFor();assert.deepEqual(decided(),[]);
  if(width<600){const b=await older.locator('.older-bar').boundingBox(),box=await older.boundingBox();assert.ok(b.x+b.width<=box.x+box.width+1,'the bar fits at phone width')}
  // Confirmed: each one gets the to-do's own Not needed, out of the list at once, with one Undo for all
  await older.getByRole('button',{name:'Dismiss all'}).click();await older.getByRole('button',{name:'Dismiss',exact:true}).click();
  await until(()=>decided().length>=2);
  assert.deepEqual(decided().sort(),[[OLD1,'reject','No longer needed'],[OLD2,'reject','No longer needed']].sort());
  await page.locator('#older-list').waitFor({state:'detached'});
  await page.waitForFunction(()=>document.querySelector('#toast')?.textContent.includes('Marked not needed'));
  assert.deepEqual((await page.locator('#toast [data-undo]').getAttribute('data-undo')).split(',').sort(),[OLD1,OLD2].sort());
  assert.equal(await page.locator('#suggestions>article[id]').count(),3,'For you as it was');
  // Undo reopens them all, back in Older
  await page.locator('#toast [data-undo]').click();
  await until(()=>decided().length>=4);
  assert.deepEqual(decided().slice(2).map(([id,c])=>[id,c]).sort(),[[OLD1,'undo'],[OLD2,'undo']].sort());
  await page.waitForFunction(()=>/^Older\s*2$/.test(document.querySelector('#older-head')?.textContent.trim()||''));
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('older dashboard ok');
}finally{await browser?.close();server.close()}
