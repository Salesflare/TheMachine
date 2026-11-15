import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A Home line that points to a to-do (a bill): under its words, where it came from and "Open the to-do", which opens
// that to-do (#card=). A line whose to-do is gone shows no link. At 390 the link stays on one line; nothing is wider
// than the screen.
const dashboard=await dashboardPage();
const at=new Date().toISOString();
const note={id:'note:4',kind:'home',name:'Bills and subscriptions',area:'personal',starts:null,ends:null,by:'machine',updated_at:at,parent:null,depth:0,children:0,
 lines:[{id:1,text:'Example Energy: a bill every month',at:'2026-11-03',item:'bill',by:'machine',edited:false,event_id:7,fact_id:null,links:[],data:{todo:'0a1b2c3d4e5f6071'},todo:'0a1b2c3d4e5f6071',
         source:{id:7,kind:'gmail.message',title:'Your Example Energy bill',occurred_at:at}},
        {id:2,text:'Example Water: a bill every three months',at:'2026-09-18',item:'bill',by:'machine',edited:false,event_id:null,fact_id:null,links:[],data:{todo:'s-gone'}}]};
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'&&url.searchParams.has('node')){res.end(JSON.stringify({...note,path:[],created_at:at,renamed:false,owner_dates:false,dated:false,children:[],linked_from:[],tree:[{...note,lines:2}]}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({list_counts:{people:0,quiet:0,new:0,orgs:0,warmup:0,projects:0,projects_done:0},counts:{person:0,org:0,project:0},boards:[],board_suggestions:[],notes:[{...note,lines:2}]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-GB'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(width+': '+e.message));await page.goto(base+'#graph/note%3A4');
  await page.locator('.note-lines li').nth(1).waitFor();
  const rows=await page.locator('.note-lines li').evaluateAll(l=>l.map(x=>({src:x.querySelector('.note-src')?.textContent.trim()||'',href:x.querySelector('.note-src a')?.getAttribute('href')||null,
   tall:x.querySelector('.note-src a')?x.querySelector('.note-src a').getClientRects().length:0})));
  assert.deepEqual(rows.map(r=>[r.src,r.href]),[['From Your Example Energy bill · Open the to-do','#card=0a1b2c3d4e5f6071'],['',null]],width+': '+JSON.stringify(rows));
  assert.equal(rows[0].tall,1,width+': "Open the to-do" on one line');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),width+': fits');
  await page.locator('.note-src a').click();
  await page.waitForFunction(()=>location.hash==='#card=0a1b2c3d4e5f6071');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok notes to-do link');
}finally{await browser?.close();server.close()}
