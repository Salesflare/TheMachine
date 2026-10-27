import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A teammate's ask under Suggestions: Share once, Always share and Decline are visible buttons (Never under More). A brief
// ask is never a to-do: it waits quietly in its Fleet's pane (Brief requests), the latest per teammate, with Share once first and no nudge toward Always.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const FL='fl_'+'a'.repeat(16),Q=n=>'q_'+String(n).repeat(16);
const preview='1 company you were in touch with, 0 that went quiet, 1 unanswered email, 1 meeting with outside people. Company names, counts and dates only.';
const brief=n=>({id:Q(n),fleet:FL,member_id:'p',name:'Alexandra Longname-Whitfield (alexandra@acme.example)',kind:'brief',status:'waiting',at:'2026-10-2'+n+'T08:00:00+00:00',
 question:`Your brief facts for the day (since 2026-10-2${n})`,draft:{preview,counts:{touched:1,quiet:0,unanswered:1,meetings:1}}});
const view={on:true,kinds:{relationships:'who knows someone',brief:'brief facts'},kind_rules:{relationships:['ask','always','never'],brief:['ask','always','never']},
 no_details:['brief'],brief:{every:'day',tell:false},briefs:{},free:[],
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:['relationships','brief'],people:[{member_id:'m',name:'Sam',role:'owner',me:true,email:'sam@acme.example'}],members:[],rules:{},exceptions:{}}],
 waiting:[brief(1),{...brief(2),member_id:'k2',name:'Kim'},{id:Q(3),fleet:FL,member_id:'k',name:'Kim',kind:'relationships',status:'waiting',at:'2026-10-21T09:00:00+00:00',question:'Who knows someone at Globex?'}],
 asked:[],log:[],notices:[]};
const calls=[];
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify({suggestions:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:1}}));return}
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
  const other=page.locator('#suggestions #fleet-'+Q(3));await other.waitFor();
  assert.deepEqual(errors,[]);
  const labels=c=>c.locator('.actions>button').allInnerTexts();
  // A one-off question: Share once first, Always share right next to it
  assert.deepEqual(await labels(other),['Share once','Always share','Decline']);
  assert.deepEqual(await other.locator('.more-menu button').allTextContents(),['Never share']);
  assert.match(await other.innerText(),/Always and Never also cover their future asks like this\./);
  // No brief card under Suggestions, and the badge doesn't count them
  assert.equal(await page.locator('#suggestions [id^="fleet-q_"]').count(),1);
  assert.doesNotMatch(await page.locator('#suggestions').innerText(),/brief facts/);
  assert.equal(await page.locator('#badge-inbox').textContent(),'1');
  // The Fleet tab: one quiet box, a row per ask, the same four choices
  await page.evaluate(()=>document.querySelector('#tab-fleet').click());
  const box=page.locator('#fleet-view .fleet-brief-asks');await box.waitFor();
  assert.match(await box.locator('h3').innerText(),/Brief requests\s*2/);
  const row=box.locator('#fleet-'+Q(1));
  assert.deepEqual(await row.locator('button').allInnerTexts(),['Share once','Always share','Decline','Never']);
  assert.equal(await row.locator('button.primary').innerText(),'Share once');
  assert.match(await row.innerText(),/Daily brief · Companies: 1 · Went quiet: 0 · Unanswered emails: 1 · Meetings with outside people: 1/);
  assert.doesNotMatch(await box.innerText(),/hashes/);
  const fit=await box.evaluate(b=>{const r=b.getBoundingClientRect();return {inside:[...b.querySelectorAll('button')].every(k=>{const x=k.getBoundingClientRect();return x.left>=r.left-1&&x.right<=r.right+1}),clipped:[...b.querySelectorAll('button')].some(k=>k.scrollWidth>k.clientWidth+1),wide:document.documentElement.scrollWidth>innerWidth}});
  assert.ok(fit.inside&&!fit.clipped&&!fit.wide,JSON.stringify(fit));
  if(shots){await box.scrollIntoViewIfNeeded();await box.screenshot({path:`${shots}/fleet-brief-asks-${width}.png`})}
  // The decision is the same as before: once, always, decline, never, per ask
  if(width===1280){
   calls.length=0;await row.locator('[data-choice-f="always"]').click();
   for(let i=0;i<100&&!calls.length;i++)await page.waitForTimeout(20);
   assert.deepEqual(calls[0],{action:'fleet_decide',args:{id:Q(1),choice:'always'}});
   await page.waitForTimeout(300);
  }
  await page.close();
 }
 console.log('fleet ask dashboard: ok');
}finally{await browser.close();server.close()}
