import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// What a Fleet costs, leaving it and starting one are focused steps on the account (quotes, confirmations, Stripe).
// The Fleet tab links to them in a quiet row under each Fleet's name: on a hosted Machine a one-time hop (/_machine/account-hop) that
// carries which Fleet, on a paired one a link to the account in a new tab, without an account none at all. A hosted
// Machine's Family invite suggestion hops too, with who, after marking it used. Hidden in the phone app ([data-buy]).
// SHOTS=<folder> saves the hosted to-do's invite line.
const dashboard=await dashboardPage();
const FL='fl_'+'a'.repeat(16),FA='fl_'+'c'.repeat(16),FR='fr_'+'b'.repeat(16),at='2026-10-20T08:00:00+00:00';
const view={on:true,kinds:{},kind_rules:{},no_details:[],scoped:[],scopes:{},intro_offers:[],waiting:[],asked:[],log:[],notices:[],free:[],briefs:{},
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:[],joined_at:at,people:[{member_id:'m',name:'Sam Doe',role:'owner',me:true}],members:[],rules:{},exceptions:{}},
  {id:FA,kind:'family',label:'Family Fleet',name:'Does',asks:[],joined_at:at,people:[{member_id:'m2',name:'Sam Doe',role:'owner',me:true}],members:[],rules:{},exceptions:{}},
  {id:FR,kind:'friends',label:'Friends',name:'Friends',asks:[],people:[{member_id:'fp_me',name:'Sam Doe',me:true}],members:[],rules:{},exceptions:{}}],
 friends:{id:FR,username:'sam',in:[],out:[],blocked:[]}};
const URL_='https://app.example.test/account?tab=fleet&invite=family&to=sasha%40mail.example&name=Sasha+Lane#fleet';
const card={id:'c1',title:'Who picks up the kids on Wednesday?',body:'Sasha asked who does the school run.',status:'pending',scope:'personal',
 created_at:new Date().toISOString(),event_ids:[1],owner_step:true,
 family_invite:{name:'Sasha Lane',first:'Sasha',question:'Invite Sasha?',line:'Your Machines can sort this out without you asking each other.',url:URL_}};
let mode='hosted';const calls=[],hops=[];
const status=()=>({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:true,waiting:0,family_invites:true},
 manage_url:mode==='hosted'?'https://app.example.test/setup':null,account_url:mode==='none'?null:'https://app.example.test/account'});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){calls.push(JSON.parse(body||'{}'));res.end('{"ok":true}');return}
 if(url.pathname==='/_machine/account-hop'){hops.push(Object.fromEntries(new URLSearchParams(body)));res.setHeader('Content-Type','text/html');res.end('<p>hop</p>');return}
 if(url.pathname.startsWith('/api/fleet')){res.end(JSON.stringify(view));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const open=async(context,width)=>{const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-c1').waitFor();
 await page.waitForFunction(()=>!document.querySelector('nav [data-tab="fleet"]')?.hidden);
 await page.evaluate(()=>document.querySelector('nav [data-tab="fleet"]').click());await page.locator('#fleet-view .fleet-tabs').waitFor();
 return page};
const pane=(page,id)=>page.locator(`#fleet-view .fleet-pane[data-pane="${id}"]`);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1280,390]){
  const context=await browser.newContext({viewport:{width,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  // Hosted: forms that hop, each carrying its own Fleet
  mode='hosted';let page=await open(context,width);
  const work=pane(page,'fleet-'+FL);
  assert.deepEqual(await work.locator('.fleet-acct button').allInnerTexts(),['What it costs','Fleet settings','Start another Fleet','Leave this Fleet']);
  assert.deepEqual(await work.locator('.fleet-acct form').evaluateAll(fs=>fs.map(f=>[f.getAttribute('action'),f.elements.to.value,f.elements.fleet?.value||''])),
   [['/_machine/account-hop','fleet_costs',FL],['/_machine/account-hop','fleet_settings',FL],['/_machine/account-hop','fleet_start',''],['/_machine/account-hop','fleet_leave',FL]]);
  assert.equal(await pane(page,'family').locator('.fleet-acct input[name="fleet"]').first().getAttribute('value'),FA);
  assert.equal(await work.locator('.fleet-acct').getAttribute('data-buy'),'');  // the phone app hides it
  assert.ok(await work.locator('.fleet-pane-head + .fleet-acct').count());  // right under the Fleet's name
  assert.ok(await page.evaluate(()=>[...document.querySelectorAll('.fleet-acct')].every(r=>r.scrollWidth<=r.clientWidth)));
  assert.equal(await pane(page,'friends').locator('.fleet-acct').count(),0);  // in a Fleet already: not under Friends
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.evaluate(id=>document.querySelector(`[data-fleet-pane="fleet-${id}"]`).click(),FL);
  hops.length=0;await work.locator('.fleet-acct button',{hasText:'What it costs'}).click();await page.waitForURL(/account-hop/);
  assert.deepEqual(hops,[{to:'fleet_costs',fleet:FL}]);
  // The Family invite suggestion: marked used, then the hop with who
  page=await open(context,width);await page.evaluate(()=>document.querySelector('nav [data-tab="inbox"]').click());
  if(process.env.SHOTS)await page.locator('#task-c1').screenshot({path:`${process.env.SHOTS}/hosted-invite-card-${width}.png`});
  calls.length=0;hops.length=0;await page.locator('#task-c1 .family-invite [data-family-invite="open"]').click();await page.waitForURL(/account-hop/);
  assert.deepEqual(calls,[{action:'family_invite',args:{suggestion_id:'c1',do:'open'}}]);
  assert.deepEqual(hops,[{to:'family_invite',email:'sasha@mail.example',name:'Sasha Lane'}]);
  // Paired: links to each step of the account, in a new tab
  mode='paired';page=await open(context,width);
  assert.deepEqual(await pane(page,'fleet-'+FL).locator('.fleet-acct a').evaluateAll(as=>as.map(a=>[a.textContent,a.getAttribute('href'),a.target])),
   [['What it costs ↗',`https://app.example.test/account?tab=fleet&part=costs&fleet=${FL}`,'_blank'],
    ['Fleet settings ↗',`https://app.example.test/account?tab=fleet&part=settings&fleet=${FL}`,'_blank'],
    ['Start another Fleet ↗','https://app.example.test/account?tab=fleet&part=start','_blank'],
    ['Leave this Fleet ↗',`https://app.example.test/account?tab=fleet&part=leave&fleet=${FL}`,'_blank']]);
  assert.equal(await page.locator('#task-c1 .family-invite a[data-family-invite="open"]').getAttribute('href'),URL_);
  // No account: nothing to link to
  mode='none';page=await open(context,width);
  assert.equal(await page.locator('#fleet-view .fleet-acct').count(),0);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('fleet account steps dashboard ok');
