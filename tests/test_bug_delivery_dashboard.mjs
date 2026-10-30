import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');
const dashboard=await dashboardPage();
let release,fast=false;
const server=createServer((req,res)=>{let body='';req.on('data',c=>body+=c);req.on('end',()=>{
 const path=new URL(req.url,'http://fixture.invalid').pathname;
 if(path==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');
 if(path==='/_machine/bug'){const send=()=>res.end(JSON.stringify({sent:true}));if(fast)send();else release=send;return}
 if(path==='/api/status'){res.end(JSON.stringify({manage_url:'https://fixture.invalid/setup',fleet:{on:false}}));return}
 if(path==='/api/action'){const action=JSON.parse(body||'{}').action;
  res.end(JSON.stringify(action==='bug_queued'?{queued:[]}:action==='support_access'?{until:null,hours:24,accesses:[]}:{}));return}
 res.end(path==='/api/events'?'[]':'{}')})});
await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
try{browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(fast of [false,true]){const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();
  await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>state.manage_url);
  await page.evaluate(()=>helpOpen('bug'));await page.fill('#bug-what','Synthetic delayed report');await page.uncheck('#bug-diag');await page.click('#bug-send');
  if(!fast){await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('Saved. Sending'));
   assert.ok(!(await page.textContent('#toast')).includes('Sent, thanks'));release()}
  await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('Sent, thanks'));await context.close()}
}finally{await browser?.close();server.close()}
console.log('hosted bug report distinguishes saved from delivered, including immediate receipts');
