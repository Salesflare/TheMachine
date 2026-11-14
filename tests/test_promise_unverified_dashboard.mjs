import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A promise from a sender the owner doesn't know (promises.unknown_sender) is kept and marked: "unverified sender" on
// its row in the Promises list and under the title of its page; one from someone they know has no mark. Its to-do
// says so in its body (written by the server). Nothing is wider than the screen at 390 and 1440, light and dark.
// SHOTS=<folder> saves the row, the page head and the to-do.
process.env.TZ='Europe/Brussels';
const dashboard=await dashboardPage();
const brand={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'};
const day=n=>{const d=new Date();d.setDate(d.getDate()+n);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')};
const ago=d=>new Date(Date.now()-d*864e5).toISOString(),now=new Date().toISOString();
const promises=[
 {id:8,direction:'theirs',who:'Mattias Berg',what:'follow up with the outstanding items',due:day(2),state:'open',made_at:ago(1),check_at:now,unverified:1},
 {id:9,direction:'theirs',who:'Sam Lee',what:'send the signed contract',due:day(3),state:'open',made_at:ago(1),check_at:now,unverified:0}];
const page8={id:8,direction:'theirs',together:0,unverified:1,who:'Mattias Berg',what:promises[0].what,due:day(2),check_at:now,status:'open',state:'open',note:null,made_at:ago(1),event_id:41,
 account_id:'work',created_at:ago(1),updated_at:ago(1),card:null,links:[],history:[{at:ago(1),kind:'said',detail:'gmail.message'},{at:ago(1),kind:'noted'}],source:[]};
const card={id:'a'.repeat(16),title:'Waiting on Mattias Berg: follow up with the outstanding items',status:'pending',created_at:now,event_ids:'[]',
 body:'Unverified: you haven’t written to Mattias Berg before. Promised on Mon, Oct 19 for Wed, Oct 21. Nothing has come in yet, so a short nudge may help.'};
const errors=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(brand[url.pathname]){res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+brand[url.pathname],import.meta.url)));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[card],promises,connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]}}));return}
 if(url.pathname==='/api/promise'){res.end(JSON.stringify(page8));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({people:[],projects:[],orgs:[],quiet:[],new:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
let browser;
const open=async(width,height,scheme)=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));await page.goto(base);await page.locator('#task-'+'a'.repeat(16)).waitFor();return {context,page}};
const fits=(page,where)=>page.evaluate(()=>({page:document.documentElement.scrollWidth,vw:innerWidth})).then(s=>assert.ok(s.page<=s.vw,`${where}: wider than the screen ${JSON.stringify(s)}`));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){const {context,page}=await open(width,height,scheme);
  await page.evaluate(()=>{const l=document.querySelector('#promises-list');if(l)l.open=true});
  assert.deepEqual(await page.locator('#promise-row-8 .promise-unverified').allInnerTexts(),['unverified sender']);
  assert.equal(await page.locator('#promise-row-9 .promise-unverified').count(),0,'someone they know: no mark');
  assert.match(await page.locator('#task-'+'a'.repeat(16)).innerText(),/Unverified: you haven’t written to Mattias Berg before\./);
  await fits(page,`${width} ${scheme} list`);
  if(shots){await page.locator('#promise-row-8').screenshot({path:`${shots}/promise-row-${width}-${scheme}.png`});
   await page.locator('#task-'+'a'.repeat(16)).screenshot({path:`${shots}/promise-todo-${width}-${scheme}.png`})}
  await page.evaluate(()=>{location.hash='#promise/8'});await page.locator('#people-view .promise-page').waitFor();
  assert.match(await page.locator('.promise-page .person-job').innerText(),/^Mattias Berg promised · due .+ · unverified sender$/);
  await fits(page,`${width} ${scheme} page`);
  if(shots)await page.locator('.promise-page .name-row').screenshot({path:`${shots}/promise-page-${width}-${scheme}.png`});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('unverified promises ok');
}finally{await browser?.close();server.close()}
