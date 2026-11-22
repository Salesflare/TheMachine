import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// "Sent. Moved to Done." belongs to the to-do that went, and says so only once it really went (made-up data, nothing
// is sent). It stood over another to-do's unsent draft: the send dialog opened with the earlier notice still up, a
// send that landed while that dialog was open said it over it, and a toast that had faded stayed in the page's text
// (opacity only), so it read as part of what came next. And a to-do that closed while its send was still queued said
// "Sent". SHOTS=<folder> saves screenshots, light and dark.
const dashboard=await dashboardPage();
const at=h=>new Date(Date.now()-h*36e5).toISOString();
const id=n=>(n+'').padStart(2,'0').repeat(8);
const draft=(n,rev,to)=>({id:id(n),title:['','Confirm the workshop date','Thank the printer','Answer the caterer'][n],body:'Drafted a reply.',status:'prepared',scope:'work',created_at:at(n),event_ids:[n],
 next_actions:[{kind:'email',label:'Send reply',revision:rev,to:[to+'@example.org'],to_name:to,subject:'Re: your note',body:'Hi '+to+', thanks.'}]});
let cards,going,stuck;
const reset=()=>{cards=[draft(1,'ab12cd34ef56','Sam'),draft(2,'ba21dc43fe65','Kim'),draft(3,'cc33dd44ee55','Ari')];going=new Map();stuck=new Set()};
// A send takes a moment: the next status read still says sending, the one after it closes the to-do. One that is stuck
// stays queued while the to-do closes for another reason.
function settle(){for(const [cid,n] of going){const c=cards.find(x=>x.id===cid),a=c.next_actions[0];
 if(stuck.has(cid)){a.state={status:'queued'};Object.assign(c,{status:'completed',closed_at:new Date().toISOString()});continue}
 if(n>0){a.state={status:'sending'};going.set(cid,n-1);continue}going.delete(cid);a.state={status:'sent'};Object.assign(c,{status:'completed',closed_at:new Date().toISOString()})}}
const state=()=>{settle();return {suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},done_counts:{all:0}}};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:[],next:null,total:0}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({counts:{}}));return}
 if(url.pathname==='/api/events'){res.end('[]');return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);
  if(r.action==='confirm_action'){going.set(r.args.suggestion_id,1);res.end('{}');return}
  res.end(JSON.stringify(r.action==='card_chat'?{session:true,status:'ok',active:false,cursor:'k1',items:[]}:{}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const SENT=/Sent\. Moved to Done/;
const review=async(page,n,rev)=>{await page.locator(`#task-${id(n)} [data-smart="${rev}"]`).click();await page.locator('#send-dialog').waitFor({state:'visible'})};
const pageText=page=>page.evaluate(()=>document.body.innerText);
const refreshTwice=page=>page.evaluate(async()=>{await refresh();await refresh()});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[1440,900,'light'],[390,844,'dark'],...shots?[[1440,900,'dark'],[390,844,'light']]:[]]){reset();const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+id(1)).waitFor();
  // The first one goes and says so, with Open for it
  await review(page,1,'ab12cd34ef56');await page.locator('#send-confirm').click();
  await page.waitForFunction(()=>/Moved to Done/.test(document.querySelector('#toast.show')?.textContent||''),null,{timeout:15000});
  assert.equal(await page.locator('#toast [data-toast-open]').getAttribute('data-toast-open'),id(1));
  // Reviewing the next draft: the earlier notice goes, and is nowhere in the page's text over that draft
  await review(page,2,'ba21dc43fe65');
  await page.waitForFunction(()=>!document.querySelector('#toast.show'));
  await page.waitForFunction(()=>getComputedStyle(document.querySelector('#toast')).visibility==='hidden');  // past the fade
  assert.doesNotMatch(await pageText(page),SENT);
  if(shots)await page.screenshot({path:`${shots}/sent-next-draft-${width}-${scheme}.png`});
  // A send that lands while another draft is open says nothing over it; once that closes, it says where its own to-do went
  await page.keyboard.press('Escape');await page.locator('#send-dialog').waitFor({state:'hidden'});
  await review(page,2,'ba21dc43fe65');await page.locator('#send-confirm').click();await page.locator('#send-dialog').waitFor({state:'hidden'});
  await review(page,3,'cc33dd44ee55');
  await refreshTwice(page);
  assert.equal(cards.find(c=>c.id===id(2)).status,'completed');
  assert.doesNotMatch(await pageText(page),SENT);
  await page.keyboard.press('Escape');await page.locator('#send-dialog').waitFor({state:'hidden'});
  await page.evaluate(()=>refresh());
  await page.waitForFunction(()=>/Moved to Done/.test(document.querySelector('#toast.show')?.textContent||''),null,{timeout:15000});
  assert.equal(await page.locator('#toast [data-toast-open]').getAttribute('data-toast-open'),id(2));
  if(shots)await page.screenshot({path:`${shots}/sent-own-todo-${width}-${scheme}.png`});
  // A to-do that closed while its send was still queued never says Sent
  stuck.add(id(3));
  await review(page,3,'cc33dd44ee55');await page.locator('#send-confirm').click();await page.locator('#send-dialog').waitFor({state:'hidden'});
  await refreshTwice(page);
  assert.equal(cards.find(c=>c.id===id(3)).status,'completed');
  assert.notEqual(await page.evaluate(()=>document.querySelector('#toast.show [data-toast-open]')?.dataset.toastOpen),id(3));
  assert.doesNotMatch(await page.evaluate(()=>document.querySelector('#toast.show')?.textContent||''),/Sent/);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
