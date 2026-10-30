import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A hosted setup page sends the owner here (#signin-site=linkedin) to sign in to LinkedIn on their Machine: a dialog
// titled so, that site's sign-in only. After the password LinkedIn waits on its app: the dialog says to approve it
// there and keeps checking (Continue looks at once); once in, it says setup connects by itself. All mocked, made-up
// credentials only. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const form={host:'www.linkedin.com',secure:true,title:'LinkedIn Login',username:true,password:true,code:false,id:'0:li',site:'linkedin.com',saved:null};
let watched=0,approved=false;
const posts=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='browser_login_pages'&&args.watch){watched++;res.end(JSON.stringify(approved?{state:'done',resumed:[]}:{state:'waiting'}));return}
  if(action==='browser_login_pages'){res.end(JSON.stringify({pages:[{...form,host:'example.org',site:'example.org',id:'0:other'},form]}));return}
  if(action==='browser_login_fill'){res.end(JSON.stringify({result:'approve',page:{id:'0:li',host:'www.linkedin.com',site:'linkedin.com'}}));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/#signin-site=linkedin');
 const dialog=page.locator('#signin-dialog');
 await page.locator('#signin-user').waitFor({state:'visible',timeout:15000});
 assert.equal(await page.locator('#signin-title').textContent(),'Sign in to LinkedIn on your Machine');
 assert.ok(await page.evaluate(()=>document.querySelector('#signin-dialog').matches(':modal')),'a modal dialog over the page');
 assert.ok(await page.locator('#signin-pick').isHidden(),'only the LinkedIn sign-in, not another site’s');
 if(shots)await dialog.screenshot({path:`${shots}/signin-linkedin.png`});
 await page.locator('#signin-user').fill('test-user@example.invalid');
 await page.locator('#signin-pass').fill('not-a-real-password');
 await page.locator('#signin-go').click();
 await page.locator('#signin-status-text').filter({hasText:'Approve the sign-in in your LinkedIn app, then press Continue.'}).waitFor({timeout:5000});
 assert.ok(await page.locator('#signin-continue').isVisible(),'Continue is the next step');
 assert.ok(await page.locator('#signin-user').isHidden()&&await page.locator('#signin-error').textContent()==='','nothing to type, no error');
 if(shots)await dialog.screenshot({path:`${shots}/signin-approve.png`});
 await page.locator('#signin-continue').click();  // not approved yet: says so and keeps checking
 await page.locator('#signin-status-text').filter({hasText:'Not approved yet'}).waitFor({timeout:5000});
 assert.ok(await dialog.isVisible());
 const before=watched;await page.waitForTimeout(3500);assert.ok(watched>before,'keeps checking by itself');
 approved=true;
 await page.locator('#signin-title').filter({hasText:'Signed in to LinkedIn'}).waitFor({timeout:6000});
 assert.match(await page.locator('#signin-status-text').textContent(),/connects LinkedIn by itself/);
 if(shots)await dialog.screenshot({path:`${shots}/signin-done.png`});
 const sent=JSON.stringify(posts.filter(p=>p.action!=='browser_login_fill'));
 assert.ok(!sent.includes('not-a-real-password'),'the password went to the fill only');
 assert.ok(posts.filter(p=>p.args?.watch).every(p=>p.args.watch==='0:li'&&p.args.host==='www.linkedin.com'));
 assert.deepEqual(errors,[]);
 console.log('signin approve dashboard ok');
}finally{await browser?.close();server.close()}
