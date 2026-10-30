// Docs on a paired self-hosted Machine: Allow edits and Reconnect on the Docs card open the + Add sign-in step, never
// the Machine browser's sign-in dialog (#signin-dialog, connections-signin.js [data-signin]), and Allow edits starts the
// edits sign-in (microsoft_docs_write), not the read one. Synthetic data, a local fixture server, nothing signed in.
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

const dashboard=await dashboardPage();
const docs={id:'docs',display_name:'Word documents',email:'owner@example.com',service:'docs',transport:'broker',boundary:'work',events:3,recent_events:3,
  last_success:new Date().toISOString(),docs_provider:'microsoft',docs_replies:false,docs_writes:[],connect_name:'docs',signin:'microsoft_docs',
  docs_write_signin:'microsoft_docs_write'};
const state=()=>({suggestions:[],connectors:[docs],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]});
const calls=[],errors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){let b='';for await(const c of req)b+=c;const call=JSON.parse(b);calls.push(call);
  if(call.action==='connect_sources'){res.end(JSON.stringify({sources:[{name:'docs',service:'docs',label:'Docs',signin:'microsoft_docs'}],manage_url:null,paired:true}));return}
  if(call.action==='connect_signin'){res.end(JSON.stringify({state:'unavailable'}));return}  // no tab opens in the test
  if(call.action==='connect_signin_state'){res.end(JSON.stringify({state:'none'}));return}
  res.end(JSON.stringify({status:'queued'}));return}
 res.statusCode=url.pathname.startsWith('/api/')?200:404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.evaluate(()=>refresh());
 const open=async()=>{
  await page.evaluate(()=>document.querySelector('nav [data-tab="health"]').click());
  await page.evaluate(()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.textContent.trim()==='Other sources')?.click());
  const conn=page.locator('[data-conn="docs"]');await conn.waitFor();return conn};
 for(const [label,start] of [['Allow edits','microsoft_docs_write'],['Reconnect','microsoft_docs']]){
  const conn=await open();
  const button=conn.locator('button',{hasText:label}).first();
  if(!await button.isVisible())await conn.evaluate(n=>n.querySelectorAll('details').forEach(d=>d.open=true));  // Details
  assert.equal(await button.getAttribute('data-signin'),null,label+' carries no browser sign-in attribute');
  assert.equal(await button.getAttribute('data-signin-source'),start);
  calls.length=0;
  await button.click();
  await page.locator('#connect-add .connect-signin').waitFor();
  await page.waitForTimeout(300);
  assert.equal(await page.evaluate(()=>document.querySelector('#signin-dialog')?.open||false),false,label+' never opens the browser sign-in dialog');
  await page.locator('#connect-add [data-signin-go]').click();
  await page.waitForTimeout(300);
  const asked=calls.filter(c=>c.action==='connect_signin').map(c=>c.args.name);
  assert.deepEqual(asked,[start],label+' starts '+start);
  assert.equal(await page.evaluate(()=>document.querySelector('#signin-dialog')?.open||false),false);
  await page.evaluate(()=>document.querySelector('#connect-add [data-connect-back]')?.click());
 }
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
