import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A list redrawn while the reader is far down it keeps the page's height a moment (placeKeep). A chat opened within that
// moment is a new place: the held height goes, so on a computer the page stays put and only the thread scrolls.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=Array.from({length:30},(_,n)=>({id:(n+'').padStart(2,'0').repeat(8),title:'Card number '+n,body:'Some text for card '+n+'.',status:'pending',scope:'work',created_at:now,event_ids:[n+1]}));
const state={suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}};
const history={session:true,status:'ok',active:false,cursor:'k1',items:Array.from({length:40},(_,n)=>({kind:'reply',text:'Reply '+n,at:Date.now()-100000+n*1000}))};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);res.end(JSON.stringify(r.action==='card_chat'?history:{}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const how of ['link','tap']){
  const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('#task-'+cards[0].id).waitFor();
  // Far down a long list, then the list is drawn anew: more above where the reader is, less below it
  const held=await page.evaluate(async()=>{const tail=document.createElement('div');tail.className='tail-probe';tail.style.height='3000px';$('#inbox').append(tail);
   scrollTo(0,1e6);const y=scrollY;
   const top=document.createElement('div');top.style.height='600px';$('#suggestions').prepend(top);tail.style.height='1000px';
   await null;return {y,mh:document.body.style.minHeight}});
  assert.ok(held.y>2000&&held.mh,`the redrawn list keeps the page's height a moment (${JSON.stringify(held)})`);
  // A chat opens right then, from a link or from the list
  if(how==='link')await page.goto(base+'#chat='+cards[1].id);
  else await page.evaluate(id=>chatGo(id),cards[1].id);
  await page.locator('#chat-log').waitFor();
  const open=await page.evaluate(()=>{scrollTo(0,1e6);return {y:scrollY,mh:document.body.style.minHeight}});
  assert.deepEqual(open,{y:0,mh:''},`the open chat (${how}) keeps the page put on a computer`);
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('place hold chat dashboard ok');
