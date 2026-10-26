import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Promises list on the Suggestions tab: both directions, due chips, Done/Drop for open ones only.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const day=n=>{const d=new Date();d.setDate(d.getDate()+n);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')};
const made=new Date(Date.now()-2*864e5).toISOString(),check=new Date(Date.now()+864e5).toISOString();
let promises=[
 {id:1,direction:'mine',who:'Alex Morgan',what:'send the Q3 deck with the updated pricing for the Globex renewal',due:day(0),state:'open',made_at:made,check_at:check},
 {id:2,direction:'theirs',who:'Sam Lee',what:'send the signed contract',due:day(-1),state:'card',made_at:made,check_at:check},
 {id:3,direction:'theirs',who:'Kim',what:'get back about the pilot',due:null,state:'open',made_at:made,check_at:check},
 {id:4,direction:'mine',who:'Old',what:'already kept',due:null,state:'kept',made_at:made,check_at:check}];
const state=()=>({suggestions:[],promises,connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]});
const calls=[],errors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;calls.push(JSON.parse(body));res.end('{"status":"kept"}');return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 const list=page.locator('#promises-list');
 await list.waitFor();
 assert.equal(await list.locator('summary .count').textContent(),'3');  // closed ones stay out
 await list.locator('summary').click();
 assert.deepEqual(await list.locator('.promise-head').allTextContents(),['You promised1','Promised to you2']);
 const text=await list.textContent();
 assert.ok(text.includes('To Alex Morgan: send the Q3 deck')&&text.includes('Due today'));
 assert.ok(text.includes('From Sam Lee: send the signed contract')&&text.includes('a to-do now')&&text.includes('Overdue'));
 assert.ok(text.includes('no date, checked'));
 assert.equal(await list.locator('[data-promise="2"]').count(),0);  // its card handles it
 const widths=[];
 for(const width of [320,390,768]){
  await page.setViewportSize({width,height:844});
  const sizes=await page.evaluate(()=>({page:document.documentElement.scrollWidth,viewport:innerWidth,list:document.querySelector('#promises-list').getBoundingClientRect().right}));
  assert.ok(sizes.page<=sizes.viewport&&sizes.list<=sizes.viewport,'overflow at '+width);widths.push({width,...sizes});
  if(process.env.PROMISES_SHOT)await list.screenshot({path:process.env.PROMISES_SHOT+'-'+width+'.png'});
 }
 await list.locator('[data-promise="1"][data-close="kept"]').click();
 for(let i=0;i<100&&!calls.length;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls[0],{action:'promise_close',args:{id:1,status:'kept'}});
 promises=promises.map(p=>p.id===1?{...p,state:'kept'}:p);await page.evaluate(()=>refresh());
 assert.equal(await page.locator('#promises-list summary .count').textContent(),'2');
 assert.ok(await page.locator('#promises-list').evaluate(d=>d.open));  // stays open across refresh
 promises=[];await page.evaluate(()=>refresh());
 assert.equal(await page.locator('#promises-list').count(),0);
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({widths,close_requests:calls.length,page_errors:errors}));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r))}
