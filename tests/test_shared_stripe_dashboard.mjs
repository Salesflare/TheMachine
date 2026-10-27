import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Stripe for the team on the Fleet tab (shared_connectors.py): an admin without Stripe gets Connect Stripe, which opens
// Connections, + Add at Sign in with Stripe; with it connected, Share Stripe ticks everyone; once shared, the admin reads
// that their Machine renews it and a member reads who shared it, read only. Never scrolls sideways.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const FL='fl_'+'b'.repeat(16);
const members=[{member_id:'a',name:'Ada Park',email:'ada@acme.example',role:'admin',keys:true,confirmed:true},
 {member_id:'k',name:'Kim Lee',email:'kim@acme.example',role:'member',keys:true,confirmed:false},
 {member_id:'r',name:'Robin Vale',email:'robin@acme.example',role:'member',keys:false,confirmed:false}];
const base=()=>({on:true,kinds:{},kind_rules:{},no_details:[],scoped:[],scopes:{},
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:[],people:[{member_id:'m',name:'Sam Doe',role:'owner',me:true,email:'sam@acme.example'},
  ...members.map(m=>({member_id:m.member_id,name:m.name,role:m.role,email:m.email}))],
  members:members.map(m=>({member_id:m.member_id,name:m.name,rules:{}})),rules:{},exceptions:{}}],waiting:[],asked:[],log:[],notices:[],
 shared:{prompts:[],shares:[],accounts:[],can_share:[{fleet:FL,name:'Acme',members}]}});
let view=base();
const calls=[];
const connectors=[{id:'stripe-acme',service:'stripe',display_name:'Acme Billing',boundary:'work:Acme',total:4,signals_24h:1,pending:0,shared_by:'Acme',last_success:new Date().toISOString(),sync_activity:[]}];
const sources=[{name:'stripe',service:'stripe',label:'Stripe',what:'Failed payments, disputes, churn and big new subscriptions.',signin:'stripe'},
 {name:'intercom',service:'intercom',label:'Intercom',what:'Customer conversations in your Intercom workspace.',signin:'intercom'}];
const brand={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'};
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(brand[req.url]){res.setHeader('Content-Type',req.url.endsWith('.png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+brand[req.url],import.meta.url)));return}
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url.startsWith('/api/status'))return res.end(JSON.stringify({suggestions:[],connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}}));
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='connect_sources')return res.end(JSON.stringify({sources,manage_url:null,saveable:true,paired:true,pair_url:'https://app.example/pair'}));
  if(call.action==='fleet_share'){view.shared.shares=[{fleet:FL,fleet_name:'Acme',service:'stripe',label:'Stripe',workspace:'Acme Billing',by:'Sam Doe',held_by:[],mine:true,have:true,admin:true}];view.shared.accounts=[];return res.end(JSON.stringify({ok:true,shared_with:2}))}
  return res.end(JSON.stringify({ok:true,done:true}))}
 if(req.url.startsWith('/api/fleet'))return res.end(JSON.stringify(view));
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const shots=process.env.SHARED_SHOTS;
const box=page=>page.locator('.fleet-box').filter({hasText:'Shared connectors'});
const shot=async(page,name,size)=>{if(shots){await box(page).scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/${name}-${size}.png`})}};
try{
 for(const [width,height] of [[390,844],[1440,900],[1440,700]]){
  const size=`${width}x${height}`;
  view=base();calls.length=0;
  const page=await (await browser.newContext({viewport:{width,height}})).newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await navClick(page.locator('nav [data-tab="fleet"]'));
  // An admin without Stripe: connect it once for the team
  await box(page).locator('.share-connect',{hasText:'Stripe for the team'}).waitFor();
  await shot(page,'fleet-connect-stripe',size);
  await box(page).locator('[data-fleet-connect="stripe"]').click();
  await page.locator('#connect-add .connect-signin h3',{hasText:'Stripe'}).waitFor();
  assert.match(await page.locator('#connect-add').innerText(),/Reads only, never changes anything in Stripe/);
  assert.match(await page.locator('#connect-add').innerText(),/Sign in with Stripe/);
  assert.match(await page.locator('#connect-add .connect-other summary').innerText(),/Or paste a restricted key/);
  if(shots){await page.locator('#connect-add').scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/connections-signin-stripe-${size}.png`})}
  // Connected: Share Stripe, everyone with keys ticked, admins fixed
  view.shared.accounts=[{id:'billing',service:'stripe',label:'Stripe',workspace:'Acme Billing'}];
  await navClick(page.locator('nav [data-tab="fleet"]'));await page.evaluate(()=>fleetView());
  await box(page).locator('.share-new summary',{hasText:'Share Stripe'}).click();
  assert.equal(await box(page).locator('.share-connect').count(),0);
  assert.match(await box(page).locator('.share-form .muted').first().innerText(),/Nobody changes anything in Stripe/);
  assert.deepEqual(await box(page).locator('.share-pick input').evaluateAll(l=>l.map(i=>[i.value,i.checked,i.disabled])),
   [['a',true,true],['k',true,false],['r',false,true]]);
  await shot(page,'fleet-share-stripe',size);
  await box(page).locator('.share-form button.primary').click();
  await box(page).locator('article',{hasText:'Your Machine renews their access every hour'}).waitFor();
  assert.deepEqual(calls.findLast(c=>c.action==='fleet_share'),{action:'fleet_share',args:{fleet:FL,account:'billing',members:['k']}});
  await page.waitForFunction(()=>!document.querySelector('#toast.show'));
  if(shots)await page.waitForTimeout(800);  // the toast fades out
  await shot(page,'fleet-stripe-shared-admin',size);
  // A member: who shared it, read only, nothing to change
  view.shared={prompts:[],shares:[{fleet:FL,fleet_name:'Acme',service:'stripe',label:'Stripe',workspace:'Acme Billing',by:'Sam Doe',held_by:[],mine:false,have:true,admin:false}],accounts:[],can_share:[]};
  await page.evaluate(()=>fleetView());
  await box(page).locator('article',{hasText:'Shared by Sam Doe · Reads only'}).waitFor();
  assert.equal(await box(page).locator('button').count(),0);
  await shot(page,'fleet-stripe-member',size);
  const card=await page.evaluate(c=>connActions(c),connectors[0]);
  assert.match(card,/Shared by Acme/);assert.doesNotMatch(card,/Disconnect|Reconnect/);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  assert.deepEqual(errors,[]);
  await page.context().close()}
 console.log('shared Stripe dashboard: ok');
}finally{await browser.close();server.close()}
