import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A teammate's ask under Suggestions: Always share, Share once and Decline are visible buttons (Never under More); a brief comes
// back every day, so Always share leads there. Several waiting asks of one kind from one teammate: the card says Always covers the others too.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const FL='fl_'+'a'.repeat(16),Q=n=>'q_'+String(n).repeat(16);
const preview='1 company you were in touch with, 0 that went quiet, 1 unanswered email (as hashes), 1 meeting with outside people. Company names, counts and dates only.';
const brief=n=>({id:Q(n),fleet:FL,member_id:'p',name:'Alexandra Longname-Whitfield (alexandra@acme.example)',kind:'brief',status:'waiting',at:'2026-10-2'+n+'T08:00:00+00:00',
 question:`Your brief facts for the day (since 2026-10-2${n})`,draft:{preview}});
const view={on:true,kinds:{relationships:'who knows someone',brief:'brief facts'},kind_rules:{relationships:['ask','always','never'],brief:['ask','always','never']},
 no_details:['brief'],brief:{every:'day',tell:false},briefs:{},free:[],
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:['relationships','brief'],people:[{member_id:'m',name:'Sam',role:'owner',me:true,email:'sam@acme.example'}],members:[],rules:{},exceptions:{}}],
 waiting:[brief(1),brief(2),{id:Q(3),fleet:FL,member_id:'k',name:'Kim',kind:'relationships',status:'waiting',at:'2026-10-21T09:00:00+00:00',question:'Who knows someone at Globex?'}],
 asked:[],log:[],notices:[]};
const calls=[];
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify({suggestions:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:3}}));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;calls.push(JSON.parse(body));res.end('{"ok":true,"result":{"status":"answered"}}');return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(view));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const shots=process.env.SHOTS;
try{
 for(const width of [390,1280]){
  const page=await (await browser.newContext({viewport:{width,height:1000}})).newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  const card=page.locator('#suggestions #fleet-'+Q(1));await card.waitFor();
  assert.deepEqual(errors,[]);
  const labels=c=>c.locator('.actions>button').allInnerTexts();
  assert.deepEqual(await labels(card),['Always share','Share once','Decline']);
  assert.equal(await card.locator('.actions>button.primary').innerText(),'Always share');
  assert.deepEqual(await card.locator('.more-menu button').allTextContents(),['Never share']);
  assert.match(await card.innerText(),/1 company you were in touch with, 0 that went quiet, 1 unanswered email \(as hashes\), 1 meeting with outside/);
  assert.match(await card.innerText(),/Always and Never also cover their future asks like this\./);
  // A one-off question keeps Share once first, with Always share right next to it
  const other=page.locator('#suggestions #fleet-'+Q(3));
  assert.deepEqual(await labels(other),['Share once','Always share','Decline']);
  assert.equal(await other.locator('.fleet-bulk').count(),0);
  // Fits: every button on the card, none cut off, at most two rows
  const fit=await card.locator('.actions').evaluate(a=>{const r=a.getBoundingClientRect(),kids=[...a.children].map(k=>k.getBoundingClientRect());
   return {inside:kids.every(k=>k.left>=r.left-1&&k.right<=r.right+1),rows:new Set(kids.map(k=>Math.round(k.top))).size,clipped:[...a.querySelectorAll('button,summary')].some(b=>b.scrollWidth>b.clientWidth+1)}});
  assert.ok(fit.inside&&!fit.clipped&&fit.rows<=2,JSON.stringify(fit));
  if(shots){await card.scrollIntoViewIfNeeded();await card.screenshot({path:`${shots}/fleet-ask-${width}.png`})}
  // The decision is the same as before: once, always, decline, never, per ask
  if(width===1280){
   calls.length=0;await card.locator('[data-choice-f="always"]').click();
   for(let i=0;i<100&&!calls.length;i++)await page.waitForTimeout(20);
   assert.deepEqual(calls[0],{action:'fleet_decide',args:{id:Q(1),choice:'always'}});
   await page.waitForTimeout(300);
  }else{
   assert.equal(await card.locator('.fleet-bulk').innerText(),'1 more like this waits. Always shares it too.');
  }
  await page.close();
 }
 console.log('fleet ask dashboard: ok');
}finally{await browser.close();server.close()}
