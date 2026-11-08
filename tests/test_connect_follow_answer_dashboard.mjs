import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add, when the last answer finishes the connect at once (pasting the address Google sent you to):
// the pane still follows the restart and moves to the new account's card once the Machine is back, instead of saying
// "Restarting to start reading it…" for good (a newcomer waited over a minute on it, agent users 2026-11-08).
const dashboard=await dashboardPage();
const gmail={id:'work-gmail',service:'gmail',email:'jules@example.com',boundary:'work:Studio',boundary_by:'owner',total:0};
let connectors=[],away=0;
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://x.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){if(away>0){away--;res.statusCode=502;res.end('{}');return}
  res.end(JSON.stringify({suggestions:[],promises:[],connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,sources:[{name:'salesflare',label:'Salesflare',service:'salesflare',what:'Accounts'}]}));return}
  if(action==='connect_start'){res.end(JSON.stringify({session:'s1',state:'running',label:'Gmail',lines:['Open this address'],
   question:{id:'q1',kind:'ask',prompt:'The address Google sent you to'}}));return}
  if(action==='connect_answer'){away=2;setTimeout(()=>{connectors=[gmail]},3000);  // the restart, then back with the account
   res.end(JSON.stringify({state:'done',lines:['✓ Gmail connected'],account:'work-gmail',restarting:true,question:null}));return}
  if(action==='connect_poll'){res.end(JSON.stringify({state:'done',lines:['✓ Gmail connected'],account:'work-gmail',restarting:true}));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const errors=[];
try{
 const context=await browser.newContext({viewport:{width:1440,height:900}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.waitForFunction(()=>typeof showTab==='function'&&typeof connectStart==='function');
 await page.evaluate(()=>{showTab('health');showHealthPane('add');connectStart('gmail')});
 await page.locator('#connect-answer').fill('http://127.0.0.1:1/oauth2/callback?code=x&state=y');
 await page.locator('[data-connect-form] button.primary').click();
 await page.locator('#connect-add .sent-ok',{hasText:'Restarting to start reading it…'}).waitFor({timeout:8000});
 await page.locator('#connectors article[data-conn="work-gmail"].conn-new').waitFor({timeout:20000});
 await page.evaluate(()=>showHealthPane('add'));
 assert.match(await page.locator('#connect-add .sent-ok').innerText(),/^Connected\. Running again\. Its card shows how far it is\.$/);
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser.close();server.close()}
console.log('connect follow after the last answer ok');
