import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Fleet › Manage (dashboard/fleet-manage.js). Self-hosted (no manage_url): read only, the people and their roles and a
// link to that Fleet's settings step on the account in a new tab, and nothing that changes anything. Hosted: the control plane's
// answer (/_machine/fleet) with role, remove and invite; a change goes there as JSON from this page, and one that touches
// a price ({confirm}) shows Review and confirm, a form to /_machine/account-hop (to=fleet_confirm) with the change's
// fields. Invite people in an empty People box opens the view. Under each Fleet's name, hosted and self-hosted, the quiet
// link row of its pane, with Fleet settings: a hop (to=fleet_settings) with that Fleet's id, or that step in a new tab.
const dashboard=await dashboardPage();
const FL='fl_'+'a'.repeat(16),ACCOUNT='https://app.example.test/account';
const fleet={on:true,kinds:{},kind_rules:{},no_details:[],scoped:[],scopes:{},intro_offers:[],waiting:[],asked:[],log:[],notices:[],free:[],briefs:{},
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:[],people:[{member_id:'m',name:'Sam Doe',role:'owner',me:true,email:'sam@acme.example'}],members:[],rules:{},exceptions:{}}]};
const manage={mail:true,fleets:[{id:FL,name:'Acme',kind:'work',role:'owner',free:false,invite_days:7,max_batch:50,network:5,plans:[{plan:'standard',amount:20,gb:4}],
 members:[{id:'fm_1',name:'Sam Doe',email:'sam@acme.example',role:'owner',you:true,machine:'',seat:null,roles:[],remove:false,resize:null},
  {id:'fm_2',name:'Pat Lee',email:'pat@acme.example',role:'member',you:false,machine:'',seat:null,roles:['owner','admin'],remove:true,resize:null}],
 invites:[{id:'fi_1',status:'open',name:'',email:'kim@acme.example',joined:'',plan:'own',until:'2026-11-13T09:00:00Z',at:'2026-11-13T09:00:00Z',link:'https://app.example.test/join/x',mail:'sent'}],
 joins:[{id:'jr_1',name:'Lou Park',email:'lou@acme.example',via:'domain'}]}]};
let hosted=false;const posts=[];
// the post a click sends, once it reaches the stand-in control plane (no fixed wait: a busy runner takes longer)
const posted=async(page,what)=>{for(let i=0;i<200&&posts.at(-1)?.do!==what;i++)await page.waitForTimeout(25);return posts.at(-1)};
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify({suggestions:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0},account_url:ACCOUNT,...(hosted?{manage_url:'http://127.0.0.1/account'}:{})}));return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(fleet));return}
 if(req.url==='/_machine/fleet'){
  if(!hosted){res.statusCode=503;res.end('{"error":"Offline"}');return}
  if(req.method==='POST'){let body='';for await(const c of req)body+=c;const d=JSON.parse(body);posts.push({...d,origin:req.headers.origin});
   res.end(JSON.stringify(d.do==='remove'?{confirm:{title:'Remove Pat Lee?',what:'remove',form:{member:'fm_2'}},...manage}:{ok:true,...manage}));return}
  res.end(JSON.stringify(manage));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const url='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 // Self-hosted: read only
 let page=await (await browser.newContext({viewport:{width:390,height:900}})).newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(url);await navClick(page.locator('nav [data-tab="fleet"]'));await page.locator('.fleet-tabs').waitFor();
 assert.match(await page.locator('#fleet-view .fleet-box').first().innerText(),/Nobody else yet\./);
 await page.locator('[data-manage-open]').click();
 assert.equal(await page.locator('.fleet-pane:not([hidden])').getAttribute('data-pane'),'manage');
 const link=page.locator('#manage-'+FL+' a.button');
 assert.equal(await link.getAttribute('href'),ACCOUNT+'?tab=fleet&part=settings&fleet='+FL);
 assert.equal(await link.getAttribute('target'),'_blank');
 assert.equal(await page.locator('#manage-'+FL+' [data-manage-do], #manage-'+FL+' select, #manage-'+FL+' textarea').count(),0);
 assert.deepEqual(await page.locator('#manage-'+FL+' .manage-head + .fleet-acct a').evaluateAll(as=>as.map(a=>[a.textContent,a.getAttribute('href')])).then(r=>r.slice(0,2)),
  [['What it costs ↗',ACCOUNT+'?tab=fleet&part=costs&fleet='+FL],['Fleet settings ↗',ACCOUNT+'?tab=fleet&part=settings&fleet='+FL]]);  // under its name
 assert.match(await page.locator('#manage-'+FL).innerText(),/Owner/);
 assert.deepEqual(errors,[]);await page.context().close();
 // Hosted: the control plane's view, changes from this page
 hosted=true;page=await (await browser.newContext({viewport:{width:1000,height:900}})).newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(url);await navClick(page.locator('nav [data-tab="fleet"]'));await page.locator('.fleet-tabs').waitFor();
 await page.locator('[data-fleet-pane="manage"]').click();await page.locator('[data-manage-role="fm_2"]').waitFor();
 assert.match(await page.locator('[data-fleet-pane="manage"]').innerText(),/Manage\s*1/);  // the join request waits
 await page.locator('[data-manage-do="join-approve"]').click();
 assert.deepEqual(await posted(page,'join-approve'),{do:'join-approve',fleet:FL,member:'',plan:'',invite:'',request:'jr_1',origin:url});
 assert.equal(await page.locator('.manage-invite-form').count(),0);  // behind Invite people until asked
 await page.locator('[data-manage-invite]').click();
 await page.locator('.manage-invite-form textarea').fill('a@acme.example\nb@acme.example');
 // Invite stays put when the emails box loses focus (the press on Invite blurs it): it moved up and the click missed
 // (measured from the form's top: the box scrolls into view smoothly meanwhile)
 const inviteAt=()=>page.locator('.manage-invite-form button.primary').evaluate(b=>b.getBoundingClientRect().top-b.form.getBoundingClientRect().top),typed=await inviteAt();
 await page.locator('.manage-invite-form textarea').blur();await page.waitForTimeout(250);assert.equal(await inviteAt(),typed,'Invite stays where it was');
 await page.locator('.manage-invite-form button.primary').click();
 assert.deepEqual(await posted(page,'invite'),{do:'invite',fleet:FL,emails:'a@acme.example\nb@acme.example',plan:'own',mail:true,origin:url});
 await page.locator('[data-manage-do="remove"][data-member="fm_2"]').click();
 const form=page.locator('.manage-confirm form');await form.waitFor();
 assert.equal(await form.getAttribute('action'),'/_machine/account-hop');
 const fields=await form.locator('input[type=hidden]').evaluateAll(xs=>Object.fromEntries(xs.map(x=>[x.name,x.value])));
 assert.deepEqual(fields,{to:'fleet_confirm',what:'remove',member:'fm_2'});
 assert.match(await page.locator('.manage-confirm').innerText(),/Remove Pat Lee\?/);
 assert.equal(await page.locator('.manage-person:has([data-member="fm_2"]) .manage-confirm').count(),1);  // under the row it is about
 await page.locator('[data-manage-cancel]').click();assert.equal(await page.locator('.manage-confirm').count(),0);
 const settings=page.locator('#manage-'+FL+' .manage-head + .fleet-acct form',{hasText:'Fleet settings'});
 assert.equal(await settings.getAttribute('action'),'/_machine/account-hop');
 assert.deepEqual(await settings.locator('input[type=hidden]').evaluateAll(xs=>Object.fromEntries(xs.map(x=>[x.name,x.value]))),{to:'fleet_settings',fleet:FL});
 assert.equal((await settings.innerText()).trim(),'Fleet settings');
 assert.deepEqual(errors,[]);
}finally{await browser.close();server.close()}
console.log('ok');
