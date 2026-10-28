import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// X and LinkedIn read only in set hours (read_window from the server). Outside them a source says when it reads again,
// never "Waiting for a fresh sync", and isn't counted; once its hours open, staleness counts from the opening. A busy
// browser left over from the last read rests too; signed out still needs the owner. SHOTS=<dir> saves screenshots.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const hour=3600e3,ago=h=>new Date(Date.now()-h*hour).toISOString(),soon=new Date(Date.now()+2*hour);
soon.setMinutes(0,0,0);const again=soon.toISOString(),clock=String(soon.getHours()).padStart(2,'0')+':00';
const base={boundary:'work',poll_seconds:3600,last_success:ago(9)};
const connectors=[
 {...base,id:'me-x',service:'x',display_name:'Own X',read_window:{hours:[7,23],reads_again_at:again}},
 {...base,id:'brand-x',service:'x',display_name:'Brand X',poll_seconds:10800,last_success:ago(11),read_window:{hours:[7,23],reads_again_at:again}},
 {...base,id:'li',service:'linkedin',display_name:'Work LinkedIn',error:'linkedin_browser_busy',retry_at:again,read_window:{hours:[7,22],reads_again_at:again}},
 // hours opened 20 minutes ago: last night's read is not stale yet
 {...base,id:'early-x',service:'x',display_name:'Early X',read_window:{hours:[7,23],opened_at:ago(1/3)}},
 // the page was left open past the opening: the stale clock starts there
 {...base,id:'past-x',service:'x',display_name:'Past X',read_window:{hours:[7,23],reads_again_at:ago(1/3)}},
 // no read hours: nine hours without a read is stale
 {...base,id:'gh',service:'github',display_name:'GitHub',poll_seconds:600,read_window:null},
 {...base,id:'li2',service:'linkedin',display_name:'Own LinkedIn',error:'linkedin_signed_out',signed_out:true,read_window:{hours:[7,22],reads_again_at:again}}];
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],connectors}));return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of process.env.SHOTS?[[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]:[[1440,900,'light']]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#badge-health').filter({hasText:/\d/}).waitFor({state:'attached'});
  assert.equal(await page.locator('#badge-health').textContent(),'1');  // only the signed-out one
  await page.evaluate(()=>{const b=document.querySelector('nav [data-tab="health"]');if(typeof drawerOpen==='function'&&!b.checkVisibility())drawerOpen();b.click()});
  const status=async name=>(await page.locator('#connectors article',{hasText:name}).locator('.connection-status').textContent()).trim();
  await page.locator('#health-tabs [data-health-pane="other"]').click();
  for(const name of ['Own X','Brand X','Work LinkedIn'])assert.equal(await status(name),'Reads again at '+clock,name);
  assert.equal(await page.locator('#connectors article',{hasText:'Work LinkedIn'}).locator('.alert').count(),0);  // no busy-browser alert while it rests
  assert.equal(await status('Early X'),'Connected');
  assert.equal(await status('Past X'),'Connected');
  assert.equal(await status('GitHub'),'Waiting for a fresh sync');
  assert.match(await status('Own LinkedIn'),/Signed out of LinkedIn/);
  if(process.env.SHOTS){await page.locator('#connectors article',{hasText:'Own X'}).scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.SHOTS}/read-hours-${width}-${scheme}.png`})}
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({page_errors:errors}));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r))}
