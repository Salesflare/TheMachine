import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A new owner's hello (Store.greeting): "Hi Alex" as the title, with who has waited longest on them linked to that
// to-do ("Ria has been waiting on your reply since Thursday."), just "Hi Alex" while nothing is ready, the tagline once
// it is over. On a phone too. Made-up people.
const dashboard=await dashboardPage(),en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const NOW=Date.UTC(2026,9,31,12,0,0);  // a Saturday
let greeting;
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/en.json'){res.end(en);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_runs:[],greeting}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,errors=[];
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const head=async(width=1280)=>{
 const context=await browser.newContext({viewport:{width,height:800},timezoneId:'UTC',locale:'en-US'}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));await page.clock.setFixedTime(NOW);await page.goto(base+'/');
 await page.locator('#page-head .page-title').waitFor();
 const out=await page.evaluate(()=>{const h=document.querySelector('#page-head'),a=h.querySelector('.page-hello a');
  return {title:h.querySelector('.page-title').textContent,line:a?.textContent||'',href:a?.getAttribute('href')||'',titleShown:h.querySelector('.page-title').getBoundingClientRect().width>1}});
 await context.close();return out};
try{
 greeting={name:'Alex',line:{person:'Ria',since:new Date(Date.UTC(2026,9,29,9)).toISOString(),card:'0123456789abcdef'}};
 let h=await head();
 assert.equal(h.title,'Hi Alex');assert.equal(h.line,'Ria has been waiting on your reply since Thursday.');assert.equal(h.href,'#card=0123456789abcdef');
 h=await head(390);assert.ok(h.titleShown,'the hello shows on a phone');assert.equal(h.line,'Ria has been waiting on your reply since Thursday.');
 greeting.line.since=new Date(NOW-26*3600e3).toISOString();assert.equal((await head()).line,'Ria has been waiting on your reply since yesterday.');
 greeting.line.since=new Date(NOW-9*864e5).toISOString();assert.equal((await head()).line,'Ria has been waiting on your reply for over a week.');
 greeting={name:'Alex'};h=await head();assert.equal(h.title,'Hi Alex');assert.equal(h.line,'');  // nothing ready yet
 greeting=null;h=await head();assert.notEqual(h.title,'Hi Alex');assert.ok(h.title.length>3);  // over: the tagline
 assert.deepEqual(errors,[]);
 console.log('greeting ok');
}finally{await browser.close();server.close()}
