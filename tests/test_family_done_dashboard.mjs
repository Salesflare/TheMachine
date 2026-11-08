import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Already did this (Fleet.handled_round, family.DONE): an open to-do someone in the Family closed as done gets one quiet
// line, who and when, with Done and Still needed. It stays open; Still needed sends family_still_needed and the line goes.
// A kept one, a closed one or one without a day shows nothing. Made-up data. SHOTS=<dir> saves 390/1440, light/dark.
const dashboard=await dashboardPage(process.env.PAGE);
const FAM='fl_'+'f'.repeat(16);
const at='2026-11-07T18:30:00+00:00',robin={name:'Robin',member_id:'fm_robin',fleet:FAM,at};
const card=(id,title,extra)=>({id:id.repeat(16).slice(0,16),title,body:'Made-up to-do.',status:'pending',scope:'personal',event_ids:[],created_at:new Date(Date.now()-36e5).toISOString(),...extra});
const fresh=()=>[card('a','Pay the parking statement',{done_elsewhere:JSON.stringify(robin)}),
 card('b','Order the school photos',{done_elsewhere:JSON.stringify({...robin,name:''})}),
 card('c','Sign the trip form',{done_elsewhere:JSON.stringify({...robin,kept:true})}),
 card('d','Book the dentist',{done_elsewhere:JSON.stringify({...robin,at:''})}),
 card('e','Renew the library card')];
let cards=fresh();const posts=[];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.method==='POST'){let body='';req.on('data',c=>body+=c);req.on('end',()=>{const b=JSON.parse(body||'{}');posts.push({path:url.pathname,...b});
  if(b.action==='family_still_needed'){const s=cards.find(x=>x.id===b.args.suggestion_id);s.done_elsewhere=JSON.stringify({...robin,kept:true});return res.end('{"kept":true}')}
  res.end('{}')});return}
 if(url.pathname==='/api/status')return res.end(JSON.stringify({suggestions:cards,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]}}));
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const id=c=>c.repeat(16).slice(0,16);
try{
 for(const [width,height] of [[1440,900],[390,844]])for(const colorScheme of process.env.SHOTS?['light','dark']:['light']){
  cards=fresh();posts.length=0;
  const context=await browser.newContext({viewport:{width,height},serviceWorkers:'block',locale:'en-US',colorScheme}),page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');
  await page.locator(`#task-${id('a')} .done-elsewhere`).waitFor();
  const line=await page.locator(`#task-${id('a')} .done-elsewhere`).innerText();
  assert.match(line,/^Robin did this · Sat, Nov 7/,line);
  assert.match(await page.locator(`#task-${id('b')} .done-elsewhere`).innerText(),/^Someone in your Family did this · /);
  for(const c of ['c','d','e'])assert.equal(await page.locator(`#task-${id(c)} .done-elsewhere`).count(),0,c);
  const box=await page.locator(`#task-${id('a')} .done-elsewhere`).boundingBox();assert.ok(box.x>=0&&box.x+box.width<=width,'fits: '+JSON.stringify(box));
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  if(process.env.SHOTS){await page.locator(`#task-${id('a')}`).scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.SHOTS}/done-elsewhere-${width}-${colorScheme}.png`})}
  await page.locator(`#task-${id('a')} [data-done-keep]`).click();
  await page.waitForFunction(i=>!document.querySelector(`#task-${i} .done-elsewhere`),id('a'));
  assert.deepEqual(posts.filter(p=>p.action==='family_still_needed').map(p=>p.args),[{suggestion_id:id('a')}]);
  assert.equal(await page.locator(`#task-${id('a')}`).count(),1,'still on the list');
  assert.deepEqual(errors,[]);
  await context.close();
 }
 console.log('family done dashboard ok');
}finally{await browser.close();server.close()}
