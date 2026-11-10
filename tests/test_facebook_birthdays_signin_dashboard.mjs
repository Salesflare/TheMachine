import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Import birthdays from Facebook to-do when the Machine's browser isn't signed in to Facebook: Sign in to Facebook
// opens Facebook's sign-in page in the Machine's browser (connect_site_signin) and the sign-in dialog on it, the way
// LinkedIn and X sign in. Once the dialog is through, the to-do reads again by itself (birthdays_facebook, step read).
// Try again reads again without signing in. Another site's sign-in page never shows in this dialog. All mocked;
// made-up values only.
const dashboard=await dashboardPage();
const SHOTS=process.env.SIGNIN_SHOTS||'';
const now=new Date().toISOString();
const LOGIN={id:'0:fb',host:'www.facebook.com',site:'facebook.com',brand:'Facebook',title:'Log in to Facebook',secure:true,error:'',saved:null,username:true,password:true,code:false};
const OTHER={id:'0:other',host:'login.example.org',site:'example.org',brand:'Example',title:'Sign in',secure:true,error:'',saved:null,username:true,password:true,code:false};
let card,posts=[];
const fresh=()=>{card={id:'fb1',title:'Import birthdays from Facebook',body:'Reads the birthdays on Facebook’s birthdays page once, in The Machine’s browser. Nothing is saved before you say so.',
 status:'pending',scope:'personal',created_at:now,event_ids:[1],owner_step:true,source_line:'Source: your routine Birthdays',facebook_birthdays:{state:'signed_out'}};posts=[]};
const state=()=>({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='connect_site_signin'){res.end(JSON.stringify({opened:true,view:null}));return}
  if(action==='browser_login_pages'){res.end(JSON.stringify({pages:[OTHER,LOGIN]}));return}
  if(action==='browser_login_fill'){res.end(JSON.stringify({result:'done'}));return}
  if(action==='birthdays_facebook'){card={...card,facebook_birthdays:{state:'reading'}};res.end(JSON.stringify({state:'reading'}));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin='http://127.0.0.1:'+server.address().port,errors=[];let browser;
const shot=async(page,name,width,scheme)=>{if(SHOTS)await page.screenshot({path:`${SHOTS}/facebook-${name}-${width}-${scheme}.png`})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,scheme] of [[1440,'light'],[390,'light'],[1440,'dark'],[390,'dark']]){fresh();
  const context=await browser.newContext({viewport:{width,height:width<500?844:900},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(origin+'/?v='+width+scheme);
  const todo=page.locator('#task-fb1');await todo.waitFor();
  assert.equal((await todo.locator('.cl-lead').innerText()).trim(),'The Machine’s browser isn’t signed in to Facebook.');
  const buttons=todo.locator('.cl-acts button');
  assert.deepEqual((await buttons.allInnerTexts()).map(x=>x.trim()),['Sign in to Facebook','Try again']);
  assert.deepEqual(await buttons.evaluateAll(b=>b.map(x=>x.className)),['primary','ghost']);
  assert.equal(await todo.locator('.browser-link').count(),0,'the dialog has Open the browser; the to-do needs no link of its own');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await todo.scrollIntoViewIfNeeded();await shot(page,'todo',width,scheme);
  // Sign in to Facebook: Facebook's sign-in page in the Machine's browser, then the dialog on it, never another site's
  await todo.getByRole('button',{name:'Sign in to Facebook'}).click();
  await page.locator('#signin-user').waitFor({state:'visible'});
  assert.deepEqual(posts.find(p=>p.action==='connect_site_signin'),{action:'connect_site_signin',args:{site:'facebook'}});
  assert.equal(await page.locator('#signin-title').textContent(),'Sign in to Facebook on your Machine');
  assert.ok(await page.locator('#signin-pick').isHidden(),'only Facebook’s page');
  assert.ok(posts.every(p=>p.action!=='birthdays_facebook'),'nothing is read before the sign-in is through');
  await page.locator('#signin-user').fill('someone@example.com');await page.locator('#signin-pass').fill('not-a-real-password');
  await shot(page,'dialog',width,scheme);
  await page.locator('#signin-go').click();
  // Signed in: the dialog closes, says so, and the to-do reads again by itself
  await page.locator('#toast',{hasText:'Signed in to Facebook. Looking there now.'}).waitFor();
  assert.ok(!await page.locator('#signin-dialog').evaluate(d=>d.open));
  assert.equal(posts.find(p=>p.action==='browser_login_fill').args.page,'0:fb');
  await todo.locator('.cl-lead',{hasText:'Reading Facebook’s birthdays page…'}).waitFor();
  assert.deepEqual(posts.filter(p=>p.action==='birthdays_facebook').map(p=>p.args),[{suggestion_id:'fb1',step:'read'}]);
  assert.ok(posts.every(p=>p.action==='browser_login_fill'||!JSON.stringify(p).includes('not-a-real-password')));
  // Try again on a signed-out to-do reads again without the dialog
  card={...card,facebook_birthdays:{state:'signed_out'}};posts=[];await page.evaluate(()=>refresh());
  await todo.getByRole('button',{name:'Try again'}).click();
  await todo.locator('.cl-lead',{hasText:'Reading Facebook’s birthdays page…'}).waitFor();
  assert.deepEqual(posts.map(p=>p.action),['birthdays_facebook']);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('facebook birthdays signin dashboard ok');
}finally{await browser?.close();server.close()}
