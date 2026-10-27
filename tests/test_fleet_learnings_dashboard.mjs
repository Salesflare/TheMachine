import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A Standard Work Fleet: team learnings in its pane (label, where from, Remove for everyone, text never markup), and on
// Sharing the asks that follow the Team Graph with only Always and Never. SHOTS=<folder> also saves screenshots.
const dashboard=await readFile(process.env.DASHBOARD||new URL('../dashboard.html',import.meta.url),'utf8');
const FL='fl_'+'a'.repeat(16),FP='b'.repeat(32);
const rules={relationships:{rule:'always',details:true},meeting:{rule:'always',details:true},handling:{rule:'always',details:false},
 brief:{rule:'always',details:false},anything:{rule:'ask',details:false}};
const two=['always','never'];
const view={on:true,kinds:{relationships:'who knows someone',meeting:'meeting context',handling:'who handles shared emails',brief:'brief facts',anything:'free questions'},
 ask_meetings:true,kind_rules:{relationships:['ask','always','never'],meeting:['ask','always','never'],handling:['ask','always','never'],brief:['ask','always','never'],anything:['ask','never']},
 no_details:['handling','brief','anything'],brief:{every:'day',tell:false},briefs:{},free:[],
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:['relationships','meeting','brief','anything'],
  people:[{member_id:'m',name:'Sam',role:'owner',me:true,email:'sam@acme.example'},{member_id:'p',name:'Pat',role:'member',me:false,email:'pat@acme.example'}],
  members:[{member_id:'p',name:'Pat',rules}],rules,exceptions:{},
  kind_rules:{relationships:two,meeting:two,handling:two,brief:['ask','always','never'],anything:['ask','never']},
  learnings:{on:true,items:[
   {fp:FP,kind:'process',text:'Refund requests are answered from the support inbox with the refund template.',confidence:0.9,source:'team_conversations',mine:true,at:'2026-10-26'},
   {fp:'c'.repeat(32),kind:'routing',text:'Renewal questions go to the account owner, not the support inbox.',confidence:0.8,source:'team_conversations',mine:false,from:'Pat',at:'2026-10-24'},
   {fp:'d'.repeat(32),kind:'style',text:'Replies to new customers open with one line on who the team is.',confidence:0.85,source:'team_conversations',mine:false,from:null,at:'2026-10-20'}]}}],
 waiting:[],asked:[],notices:[],
 log:[{at:'2026-10-26T09:00:00+00:00',direction:'out',fleet:FL,name:'your Fleet',kind:'learning',what:'Refund requests are answered from the support inbox with the refund template.',outcome:'shared with the team, from team conversations'}]};
const calls=[];
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify({suggestions:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}}));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;calls.push(JSON.parse(body));res.end('{"ok":true,"result":{"removed":true}}');return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(view));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const waitCall=async(page,action)=>{for(let i=0;i<150&&!calls.some(c=>c.action===action);i++)await page.waitForTimeout(20);return calls.find(c=>c.action===action)};
const shots=process.env.SHOTS,tag=process.env.SHOT_TAG||'after';
try{
 for(const [w,h] of shots?[[1440,900],[1440,700],[390,844]]:[[1000,900]]){
  const page=await (await browser.newContext({viewport:{width:w,height:h}})).newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await navClick(page.locator('nav [data-tab="fleet"]'));await page.locator('#fleet-view .fleet-box').first().waitFor();
  assert.deepEqual(errors,[]);
  if(shots&&tag==='before'){
   await page.screenshot({path:`${shots}/${tag}-pane-${w}x${h}.png`,fullPage:false});
   await page.locator('[data-fleet-pane="sharing"]').click();await page.locator('.fleet-rules').first().waitFor();
   await page.screenshot({path:`${shots}/${tag}-sharing-${w}x${h}.png`,fullPage:false});continue}
  const box=page.locator('.fleet-learn-box');
  await box.scrollIntoViewIfNeeded();
  assert.equal(await box.locator('article').count(),3);
  const first=await box.locator('article').first().innerText();
  assert.match(first,/^Process\s+Refund requests are answered/);
  assert.match(first,/From team conversations · Shared by your Machine · Oct 26\n/);
  assert.match(await box.locator('article').nth(1).innerText(),/Who handles what\s+Renewal questions go to the account owner/);
  assert.match(await box.locator('article').nth(1).innerText(),/· Pat ·/);
  assert.match(await box.locator('article').nth(2).innerText(),/· A teammate ·/);
  const scroll=await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
  assert.ok(scroll<=0,`no sideways scroll at ${w}: ${scroll}`);
  if(shots)await box.screenshot({path:`${shots}/${tag}-learnings-${w}x${h}.png`});
  if(shots){await box.evaluate(b=>b.scrollIntoView({block:'center'}));await page.screenshot({path:`${shots}/${tag}-pane-${w}x${h}.png`})}
  calls.length=0;await box.locator(`[data-fleet-learn-remove="${FP}"]`).click();
  assert.deepEqual(await waitCall(page,'fleet_learning_remove'),{action:'fleet_learning_remove',args:{fleet:FL,fp:FP}});
  // Sharing: the asks that follow the Team Graph take Always and Never only, with a note on what answers use
  await page.locator('[data-fleet-pane="sharing"]').click();
  const rule=k=>page.locator(`.fleet-rule[data-kind="${k}"][data-member="*"]`);
  await rule('relationships').waitFor();
  for(const k of ['relationships','meeting','handling'])
   assert.deepEqual(await rule(k).locator('input[data-fleet-rule]').evaluateAll(xs=>xs.map(x=>x.value)),two,k);
  assert.deepEqual(await rule('anything').locator('input[data-fleet-rule]').evaluateAll(xs=>xs.map(x=>x.value)),['ask','never']);
  assert.match(await page.locator('.fleet-graph-note').innerText(),/Answers use only what the Team Graph shares with the team/);
  if(shots){await page.locator('.fleet-rules-head').first().scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/${tag}-sharing-${w}x${h}.png`})}
  assert.deepEqual(errors,[]);
  await page.context().close()}
 // Text that got past the server with markup still shows as text, never markup
 view.fleets[0].learnings.items[0].text='Use the <b onmouseover="window.pwned=1">refund</b> template.';
 {const page=await (await browser.newContext({viewport:{width:1000,height:900}})).newPage();
  await page.goto('http://127.0.0.1:'+server.address().port);
  await navClick(page.locator('nav [data-tab="fleet"]'));const box=page.locator('.fleet-learn-box');await box.waitFor();
  assert.equal(await box.locator('b').count(),0);
  assert.match(await box.locator('article').first().innerText(),/Use the <b onmouseover/);
  await page.context().close()}
 // Off: one line says where the switch is
 view.fleets[0].learnings={on:false,items:[]};
 const page=await (await browser.newContext({viewport:{width:1000,height:900}})).newPage();
 await page.goto('http://127.0.0.1:'+server.address().port);
 await navClick(page.locator('nav [data-tab="fleet"]'));await page.locator('.fleet-learn-box').waitFor();
 assert.match(await page.locator('.fleet-learn-box').innerText(),/Off\. Turn it on in Settings, Security\./);
 console.log('fleet learnings dashboard ok');
}finally{await browser.close();server.close()}
