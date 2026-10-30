import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Send learnings automatically (team_learnings.set_auto, auto_send, shared, withdraw): the offer's "Send automatically
// from now on" tick goes with Send, never the email; the Settings switch under Offer to share learnings, held off by a
// Careful Work Fleet; and Fleet, Activity lists exactly what was sent, with Withdraw. All mocked, nothing leaves the
// test. SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const CASE={given:'a first reply to a customer who has not heard of the owner yet',when:'the owner opens the draft',then:'the draft says who the owner is before the ask'};
const ask=()=>({id:'tl_1',created_at:'2026-10-27T09:00:00+00:00',error:null,items:[
 {n:1,text:'Drafts for people who don’t know the context yet should introduce it first.',example:'A first email to a new supplier opens with who we are.',area:'drafts',taken:'',log:null,use_cases:[CASE]},
 {n:2,text:'Snoozed newsletters should not come back as to-dos.',example:'',area:'other',taken:'',log:null,use_cases:[]}]});
const SHARED=[{id:'tl_1',n:1,text:'Drafts for people who don’t know the context yet should introduce it first.',example:'A first email to a new supplier opens with who we are.',area:'drafts',use_cases:[CASE],log:'',named:false,auto:false,at:'2026-10-27T10:00:00+00:00',withdrawn_at:null},
 {id:'tl_0',n:2,text:'Meeting notes need the decisions on top.',example:'',area:'other',use_cases:[],log:'KeyError: missing key\n  at notes.py:40 build',named:false,auto:true,at:'2026-10-26T10:00:00+00:00',withdrawn_at:null},
 {id:'tl_0',n:1,text:'Calendar invites from the team should not become to-dos.',example:'',area:'calendar',use_cases:[],log:'',named:false,auto:true,at:'2026-10-26T10:00:00+00:00',withdrawn_at:'2026-10-26T12:00:00+00:00'}];
const FL='fl_'+'a'.repeat(16);
const fleet={on:true,kinds:{},ask_meetings:false,kind_rules:{},no_details:[],brief:{every:'off'},briefs:{},free:[],waiting:[],asked:[],notices:[],
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:[],people:[{member_id:'m',name:'Sam',role:'owner',me:true,email:'sam@acme.example'}],members:[],rules:{},exceptions:{},kind_rules:{}}],
 log:[{at:'2026-10-26T09:00:00+00:00',direction:'out',fleet:FL,name:'your Fleet',kind:'meeting',what:'Who is joining the Acme review?',outcome:'answered'}]};
let view,posts;
const reset=(more={})=>{view={offer:true,vote:true,vote_mode:'on',network:true,auto:false,auto_careful:false,ask:ask(),last_shared:null,shared:SHARED.map(s=>({...s})),...more};posts=[]};
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],voices:[],
  facts:[],team_learnings:view,fleet:{on:true,waiting:0}}));return}
 if(url.pathname.startsWith('/api/fleet')){res.end(JSON.stringify(fleet));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='learnings_share'){view={...view,ask:null,auto:!!args.auto,last_shared:{at:'2026-10-27T10:00:00+00:00',count:args.items.length}};res.end(JSON.stringify({status:'sent',count:args.items.length,team_learnings:view}));return}
  if(action==='set_learnings_auto'){view={...view,auto:args.on};res.end(JSON.stringify({auto:args.on,team_learnings:view}));return}
  if(action==='set_learnings_offer'){view={...view,offer:args.on,auto:args.on&&view.auto};res.end(JSON.stringify({team_learnings:view}));return}
  if(action==='learnings_withdraw'){view={...view,shared:view.shared.map(s=>s.id===args.id&&s.n===args.n?{...s,withdrawn_at:'2026-10-27T11:00:00+00:00'}:s)};res.end(JSON.stringify({status:'withdrawn',team_learnings:view}));return}}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,errors=[],shots=process.env.SHOTS;let browser;
const shot=async(loc,name)=>{if(shots){await loc.page().evaluate(()=>document.fonts.ready);await loc.screenshot({path:`${shots}/${name}.png`})}};
const noScroll=async(page,width)=>assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
const security=async page=>{await navClick(page.locator('#open-settings'));await page.locator('#settings-tabs [data-settings-tab="security"]').click();await page.locator('#share-offer').waitFor()};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390])for(const scheme of ['light','dark']){
  reset();
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  page.on('dialog',d=>d.accept());
  await page.goto(base+'/#feedback');
  await navClick(page.locator('[data-tab="feedback"]').first());
  const box=page.locator('#share-learnings');
  await box.locator('.share-ask [data-share="open"]').click();
  // The offer: Send automatically is off by default (asking each time is the default), next to Add my email
  const tick=box.locator('#share-auto-tick');
  assert.equal(await tick.isChecked(),false,'asking each time is the default');
  assert.match(await box.locator('.share-auto-fine').textContent(),/Your email never goes by itself\./);
  await tick.check();
  await noScroll(page,width);
  await shot(box.locator('.share-panel'),`offer-${width}-${scheme}`);
  await box.locator('[data-share="send"]').click();
  await page.locator('#toast',{hasText:'Sent 2 learnings. New ones go automatically now.'}).waitFor({state:'attached'});
  assert.equal(posts.length,1);assert.equal(posts[0].action,'learnings_share');
  assert.equal(posts[0].args.auto,true);assert.equal(posts[0].args.named,false,'the email never comes with it');
  // Settings, Security: the switch sits under Offer to share learnings and shows it on
  await security(page);
  const sw=page.locator('#share-auto');
  assert.equal(await page.locator('#share-auto-row').isVisible(),true);
  assert.equal(await sw.getAttribute('aria-checked'),'true');
  await noScroll(page,width);
  await shot(page.locator('#settings-share'),`settings-${width}-${scheme}`);
  if(scheme==='light'){
   await sw.click();await page.locator('#share-auto[aria-checked="false"]').waitFor();
   assert.deepEqual(posts.at(-1),{action:'set_learnings_auto',args:{on:false}});
   await sw.click();await page.locator('#share-auto[aria-checked="true"]').waitFor();
   assert.deepEqual(posts.at(-1),{action:'set_learnings_auto',args:{on:true}});
   // Offer off: the switch goes with it
   await page.locator('#share-offer').click();await page.locator('#share-auto-row').waitFor({state:'hidden'});
   await page.locator('#share-offer').click();await page.locator('#share-auto-row').waitFor();
   assert.equal(await sw.getAttribute('aria-checked'),'false','turning the offer back on asks each time again');
  }
  // Fleet, Activity: exactly what was sent, how, and Withdraw for those not withdrawn
  await navClick(page.locator('nav [data-tab="fleet"]'));await page.locator('#fleet-view .fleet-box').first().waitFor();
  await page.locator('[data-fleet-pane="activity"]').click();
  const sent=page.locator('.tl-shared');await sent.waitFor();
  assert.equal(await sent.locator('h3').textContent(),'Sent to The Machine team');
  assert.equal(await sent.locator('article').count(),3);
  assert.match(await sent.locator('article').nth(0).innerText(),/Sent after your OK/);
  assert.match(await sent.locator('article').nth(1).innerText(),/Sent automatically/);
  assert.match(await sent.locator('article').nth(2).innerText(),/Withdrawn Oct 26/);
  assert.equal(await sent.locator('[data-tl-withdraw]').count(),2,'no Withdraw on one already withdrawn');
  await noScroll(page,width);
  await shot(sent,`activity-${width}-${scheme}`);
  if(scheme==='light'){
   await sent.locator('article').nth(1).locator('[data-tl-withdraw]').click();
   await page.locator('#toast',{hasText:'Withdrawn. The team no longer sees it.'}).waitFor({state:'attached'});
   assert.deepEqual(posts.at(-1),{action:'learnings_withdraw',args:{id:'tl_0',n:2}});
   await page.locator('.tl-shared [data-tl-withdraw]').nth(1).waitFor({state:'detached'});
  }
  await context.close();
 }
 // A Careful Work Fleet: no tick in the offer, the switch off and held, with why
 reset({auto_careful:true});
 const context=await browser.newContext({viewport:{width:1440,height:900}}),page=await context.newPage();
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/#feedback');await navClick(page.locator('[data-tab="feedback"]').first());
 await page.locator('#share-learnings [data-share="open"]').click();
 assert.equal(await page.locator('#share-auto-tick').count(),0);
 await security(page);
 assert.equal(await page.locator('#share-auto').isDisabled(),true);
 assert.equal(await page.locator('#share-auto-note').textContent(),'A Careful Work Fleet keeps asking each time.');
 await shot(page.locator('#settings-share'),'settings-careful-1440-light');
 await context.close();
 assert.deepEqual(errors,[]);
 console.log('team learnings auto dashboard ok');
}finally{await browser?.close();server.close()}
