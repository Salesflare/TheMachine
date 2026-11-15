import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A Home line that points to a to-do (a bill): under its words, who its message came from (not the mail's subject) and
// "Open the to-do", which opens that to-do itself (#card=…&or=chat: a done one, a paid bill, opens in its chat). A
// line whose to-do is gone shows no link. At 390 the link stays on one line, nothing is wider than the screen, and the
// breadcrumb shows the path up to the note it is under (Notes › Home).
const dashboard=await dashboardPage();
const at=new Date().toISOString();
const note={id:'note:4',kind:'home',name:'Bills and subscriptions',area:'personal',starts:null,ends:null,by:'machine',updated_at:at,parent:'note:1',depth:1,children:0,
 lines:[{id:1,text:'Example Energy: a bill every month',at:'2026-11-03',item:'bill',by:'machine',edited:false,event_id:7,fact_id:null,links:[],data:{todo:'0a1b2c3d4e5f6071'},todo:'0a1b2c3d4e5f6071',
         source:{id:7,kind:'gmail.message',title:'Your Example Energy bill',from:'Example Energy',occurred_at:at}},
        {id:2,text:'Example Water: a bill every three months',at:'2026-09-18',item:'bill',by:'machine',edited:false,event_id:null,fact_id:null,links:[],data:{todo:'s-gone'}},
        // brought in once from the owner's OpenClaw memory pages (memory_seed.py): the page it came from
        {id:3,text:'The internet contract with Example Fiber runs until June 2027.',at:'2026-03-02',item:'',by:'memory',edited:false,event_id:null,fact_id:null,links:[],data:{memory:'memory/home/bills.md'}}]};
const paid={id:'0a1b2c3d4e5f6071',title:'Pay the Example Energy bill',body:'The Example Energy bill, paid.',status:'completed',scope:'personal',
 created_at:at,updated_at:at,completed_at:at,event_ids:[7],account_ids:['home'],evidence:[],next_actions:[]};
const home={id:'note:1',kind:'note',name:'Home',area:'personal',starts:null,ends:null,by:'owner',updated_at:at,parent:null,depth:0,children:1,lines:0};
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 // the paid bill: a done to-do past what the status sends, asked for by its id (doneFetch). Without it the chat
 // closes again as "isn't here anymore", and #chat= would only show for a moment (a race on a slow runner)
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:url.searchParams.get('id')==='0a1b2c3d4e5f6071'?[paid]:[]}));return}
 if(url.pathname==='/api/graph'&&url.searchParams.has('node')){res.end(JSON.stringify({...note,path:[{id:'note:1',name:'Home'}],created_at:at,renamed:false,owner_dates:false,dated:false,children:[],linked_from:[],tree:[home,{...note,lines:2}]}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({list_counts:{people:0,quiet:0,new:0,orgs:0,warmup:0,projects:0,projects_done:0},counts:{person:0,org:0,project:0},boards:[],board_suggestions:[],notes:[home,{...note,lines:2}]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-GB'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(width+': '+e.message));await page.goto(base+'#graph/note%3A4');
  await page.locator('.note-lines li').nth(2).waitFor();
  if(process.env.SHOTS)await page.screenshot({path:`${process.env.SHOTS}/note-memory-line-${width}.png`,fullPage:true});
  const rows=await page.locator('.note-lines li').evaluateAll(l=>l.map(x=>({src:x.querySelector('.note-src')?.textContent.trim()||'',href:x.querySelector('.note-src a')?.getAttribute('href')||null,
   tall:x.querySelector('.note-src a')?x.querySelector('.note-src a').getClientRects().length:0})));
  assert.deepEqual(rows.map(r=>[r.src,r.href]),[['From Example Energy · Open the to-do','#card=0a1b2c3d4e5f6071&or=chat'],['',null],['From memory/home/bills.md',null]],width+': '+JSON.stringify(rows));
  assert.equal(rows[0].tall,1,width+': "Open the to-do" on one line');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),width+': fits');
  const back=await page.locator('#people-view .graph-crumbs>a').evaluateAll(l=>l.filter(a=>a.getClientRects().length).map(a=>[a.textContent.trim(),a.getAttribute('href')]));
  if(mobile)assert.deepEqual(back,[['Notes','#graph=notes'],['Home','#graph/note%3A1']],'a phone shows the path: Notes › Home');
  else assert.deepEqual(back.map(x=>x[0]),['Graph','Notes','Home'],'the breadcrumb');
  await page.locator('.note-src a').click();
  await page.waitForFunction(()=>location.hash==='#chat=0a1b2c3d4e5f6071');  // not on the list (done): its chat
  await page.waitForTimeout(300);
  assert.equal(await page.evaluate(()=>location.hash),'#chat=0a1b2c3d4e5f6071',width+': the chat stays open');
  assert.equal(errors.filter(e=>e.startsWith(width+':')).length,0,width+': no page errors');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok notes to-do link');
}finally{await browser?.close();server.close()}
