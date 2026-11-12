import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The Promises heading on the To-dos list looks like the other folded sections' (Done / dismissed here): the same
// serif font and size, the same indent, the count at the right edge. Light and dark, at 390 and on a desktop.
const dashboard=await dashboardPage();
const made=new Date(Date.now()-2*864e5).toISOString(),check=new Date(Date.now()+864e5).toISOString();
const promises=[{id:1,direction:'mine',who:'Alex Morgan',what:'send the Q3 deck',due:null,state:'open',made_at:made,check_at:check},
 {id:2,direction:'theirs',who:'Sam Lee',what:'send the signed contract',due:null,state:'open',made_at:made,check_at:check}];
const state=()=>({suggestions:[],promises,connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
const look=sel=>{const s=document.querySelector(sel),cs=getComputedStyle(s),title=s.querySelector('span:not(.count)'),count=s.querySelector('.count');
 const ts=getComputedStyle(title),cc=getComputedStyle(count),r=s.getBoundingClientRect();
 return {font:ts.fontFamily,size:ts.fontSize,weight:ts.fontWeight,display:cs.display,titleLeft:Math.round(title.getBoundingClientRect().left-r.left),
  countRight:Math.round(r.right-count.getBoundingClientRect().right),countFont:cc.fontFamily,countBg:cc.backgroundColor}};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const width of [390,1280]){
  const context=await browser.newContext({viewport:{width,height:844},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#promises-list>summary').waitFor();await page.locator('#finished-list>summary').waitFor();
  const promisesHead=await page.evaluate(look,'#promises-list>summary'),doneHead=await page.evaluate(look,'#finished-list>summary');
  assert.deepEqual(promisesHead,doneHead,`${scheme} ${width}`);
  assert.ok(promisesHead.countRight<40,`the count sits at the right edge (${scheme} ${width})`);
  if(process.env.SHOTS){await page.locator('#promises-list').scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.SHOTS}/promises-head-${width}-${scheme}.png`})}
  assert.deepEqual(errors,[]);
  await context.close();
 }
 console.log('promises heading: ok');
}finally{await browser?.close();server.close()}
