import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A handoff waiting on a teammate whose Machine can't notify them (no phone, Telegram or email on there): the sender's
// card says so under "With Kim", with their first name only, and the Fleet tab's Handoffs box says it on the row. Once
// their Machine can ping them (no_ping gone) neither line shows. At 390px and 1440px; SHOTS=<dir> saves screenshots.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const FL='fl_'+'a'.repeat(16),CARD='c'.repeat(16),at=h=>new Date(Date.now()-h*3600e3).toISOString();
const card=noPing=>({id:CARD,title:'Confirmed contact owner and tag leaks need engineering follow-up',body:'Asked Kim: can you pick this up today and coordinate the fixes?',
 status:'snoozed',snoozed_until:new Date(Date.now()+2*864e5).toISOString(),scope:'work',created_at:at(30),event_ids:[1],next_actions:[],
 fleet_handoff:{name:'Kim Lee',stage:'waiting for them',asked:'Can you pick this up today and coordinate the fixes?',...(noPing?{no_ping:true}:{})},handoff_wait:{name:'Kim Lee'}});
const view=noPing=>({on:true,kinds:{handoff:'handoffs'},ask_meetings:false,waiting:[],intro_offers:[],splits:[],log:[],notices:[],
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:['handoff'],people:[{member_id:'m',name:'Sam Doe',role:'owner',me:true},{member_id:'k',name:'Kim Lee',role:'member'}],
  members:[{member_id:'k',name:'Kim Lee',rules:{}}],rules:{},exceptions:{}}],
 asked:[{id:'q_'+'1'.repeat(16),fleet:FL,member_id:'k',name:'Kim Lee',kind:'handoff',context:'handoff:'+CARD,status:'waiting',at:at(2),answered_at:at(2),
  question:'Can you take this on: Confirmed contact owner and tag leaks need engineering follow-up? Their summary: “Can you pick this up today?”',answer:null,...(noPing?{no_ping:true}:{})}]});
let noPing=true;
const server=createServer((req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify({suggestions:[card(noPing)],connectors:[],suggestion_counts:{snoozed:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}}));return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(view(noPing)));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const shots=process.env.SHOTS;
try{
 for(const [width,height] of [[390,844],[1440,900],[1440,700]]){for(const np of [true,false]){
  noPing=np;const tag=`${width}x${height}-${np?'no-ping':'pings'}`;
  const page=await (await browser.newContext({viewport:{width,height}})).newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#later-list>summary').click();
  const later=page.locator('#later-list #task-'+CARD);await later.waitFor();
  assert.match(await later.innerText(),/With Kim/);
  const line=later.locator('.no-ping');
  if(np){
   assert.equal(await line.innerText(),'Kim won’t get a ping. Let them know.',tag);  // first name, never the full one
   const [note,ping]=await Promise.all([later.locator('.note.fleet').first(),line].map(l=>l.evaluate(e=>e.getBoundingClientRect().top)));
   assert.ok(ping>note,`${tag}: under the handoff line`);
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${tag}: no sideways scroll`);
  }else assert.equal(await line.count(),0,tag);
  if(shots)await later.screenshot({path:`${shots}/card-${tag}.png`});
  await navClick(page.locator('nav [data-tab="fleet"]'));
  const hos=page.locator('.fleet-handoffs');await hos.waitFor();
  assert.equal(await hos.locator('.fleet-ho .chip').first().innerText(),np?'Waiting, they won’t get a ping':'Waiting for an answer',tag);
  if(shots)await hos.screenshot({path:`${shots}/fleet-${tag}.png`});
  assert.deepEqual(errors,[]);
  await page.context().close()}}
 console.log('handoff no-ping dashboard: ok');
}finally{await browser.close();server.close()}
