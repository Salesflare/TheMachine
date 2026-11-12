import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A chat message shows in the chat as soon as it's sent, not once the Machine has saved it (a slow decide here). Should
// the Machine not take it, it leaves the chat and goes back in the message box, and the reason shows.
const raw=await dashboardPage();
const SCOPE='a1'.repeat(16),iso=new Date().toISOString(),A='1'.repeat(16),SLOW=1500;
const cards=[{id:A,title:'Reply to Robin about the plan',body:'Robin asked for the numbers.',status:'pending',scope:'work',created_at:iso,event_ids:[1]}];
let refuse=false;const said=[];
const page=()=>raw.replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__',SCOPE);
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page());return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:SCOPE}));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_runs:[],connectors:[],fleet:{on:false},ui_version:'v1'}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  if(r.action==='decide'){said.push(r.args?.feedback);await new Promise(r=>setTimeout(r,SLOW));
   if(refuse){res.statusCode=400;res.end(JSON.stringify({error:'That to-do changed. Use its current buttons.'}));return}
   res.end(JSON.stringify({status:'instructions'}));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
// Sends text and says how long until it shows in the chat (ms), or null when it doesn't within the Machine's time
const send=(tab,text)=>tab.evaluate(async text=>{const t=document.querySelector('#chat-input');t.value=text;t.dispatchEvent(new Event('input',{bubbles:true}));
 const t0=performance.now();document.querySelector('[data-chat-send]').click();
 const shows=()=>[...document.querySelectorAll('#chat-log *')].some(e=>!e.childElementCount&&e.textContent.includes(text));
 while(!shows()&&performance.now()-t0<1000)await new Promise(r=>requestAnimationFrame(r));
 return shows()?Math.round(performance.now()-t0):null},text);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const tab=await context.newPage();tab.on('pageerror',e=>errors.push(e.message));
 await tab.goto('http://127.0.0.1:'+server.address().port+'/#chat='+A);await tab.locator('#chat-input').waitFor();

 const ms=await send(tab,'Use the March numbers');
 assert.ok(ms!=null&&ms<SLOW/2,`the message showed after ${ms} ms, not before the Machine saved it (${SLOW} ms)`);
 assert.equal(await tab.locator('#chat-input').inputValue(),'','the box empties at once');
 await tab.waitForFunction(()=>!document.querySelector('[data-chat-send]').disabled||chat?.active);

 // A second message while the first is still being saved: typed into the freed box and sent with the keys, it goes
 // right after the first (nothing typed meanwhile is lost)
 await tab.waitForTimeout(SLOW+500);await send(tab,'First');
 await tab.locator('#chat-input').fill('Second');await tab.locator('#chat-input').press('Control+Enter');
 await tab.waitForFunction(()=>[...document.querySelectorAll('#chat-log *')].some(e=>!e.childElementCount&&e.textContent.includes('Second')),null,{timeout:SLOW*3});
 await tab.waitForTimeout(SLOW*2+300);
 assert.deepEqual(said.slice(-2),['First','Second'],'both messages reach the Machine, in order');
 assert.equal(await tab.locator('#chat-input').inputValue(),'','the box stays empty');
 // What's typed while a message is being saved stays in the box once the Machine has it
 await send(tab,'Third');await tab.locator('#chat-input').fill('Not sent yet');await tab.waitForTimeout(SLOW+500);
 assert.equal(await tab.locator('#chat-input').inputValue(),'Not sent yet','a draft typed meanwhile is kept');
 await tab.locator('#chat-input').fill('');

 // Refused: the message leaves the chat, is back in the box, and the reason shows
 refuse=true;await tab.waitForTimeout(300);
 await tab.evaluate(()=>{const b=document.querySelector('[data-chat-send]');b.disabled=false;b.hidden=false});
 assert.ok(await send(tab,'Make it shorter')!=null,'shown at once');
 await tab.waitForFunction(()=>document.querySelector('#chat-input').value==='Make it shorter',null,{timeout:SLOW*3});
 assert.equal(await tab.evaluate(()=>[...document.querySelectorAll('#chat-log *')].some(e=>!e.childElementCount&&e.textContent.includes('Make it shorter'))),false,'gone from the chat');
 assert.match(await tab.locator('#toast').textContent(),/That to-do changed/);
 assert.deepEqual(errors,[]);
 console.log('chat send at once dashboard ok');
}finally{await browser?.close();server.close()}
