import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A new owner's hello (Store.greeting): "Hi Alex" as the title, with who has waited longest on them linked to that
// to-do ("Ria has been waiting on your reply since Thursday."), just "Hi Alex" while nothing is ready, the tagline once
// it is over. On a phone too. The list leads with the to-do the hello names (the same line.card), its section first,
// and the Needs you box stays away while the hello shows. Made-up people.
const dashboard=await dashboardPage(),en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const NOW=Date.UTC(2026,9,31,12,0,0);  // a Saturday
let greeting,cards=[],skills,connectors=[];
const now=new Date(NOW).toISOString();
const LIST=[{id:'aaaaaaaaaaaaaaa1',title:'Reply to Sam about pricing',body:'Asked.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[1]},
 {id:'aaaaaaaaaaaaaaa2',title:'Send Noor the contract',body:'Draft ready.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[2]},
 {id:'aaaaaaaaaaaaaaa3',title:'Answer Ria about the proposal',body:'Asked.',status:'pending',scope:'work',created_at:now,event_ids:[3]}];
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/en.json'){res.end(en);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({fixed:cards.length?[{id:'f1',text:'Fixed: the Projects tab now opens.'}]:[],suggestions:cards,promises:[],connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_runs:[],greeting,skills}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,errors=[];
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const head=async(width=1280)=>{
 const context=await browser.newContext({viewport:{width,height:800},timezoneId:'UTC',locale:'en-US'}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));await page.clock.setFixedTime(NOW);await page.goto(base+'/');
 await page.locator('#page-head .page-title').waitFor();if(cards.length)await page.locator('#suggestions article[id^="task-"]').first().waitFor();
 const out=await page.evaluate(()=>{const h=document.querySelector('#page-head'),a=h.querySelector('.page-hello a');
  const first=document.querySelector('#suggestions article[id^="task-"]');
  return {first:first?.id.slice(5)||'',firstSection:document.querySelector('#suggestions .section-head h2')?.textContent||'',needsYou:!!document.querySelector('#needs-you li:not([hidden])')&&!document.querySelector('#needs-you').hidden,needs:[...document.querySelectorAll('#needs-you li:not([hidden]) span')].map(x=>x.textContent),reconnects:document.querySelectorAll('#needs-you li:not([hidden]) :is(a,button)').length,fixed:!document.querySelector('#fixed-notice').hidden,
   title:h.querySelector('.page-title').textContent,line:a?.textContent||'',href:a?.getAttribute('href')||'',titleShown:h.querySelector('.page-title').getBoundingClientRect().width>1}});
 await context.close();return out};
try{
 greeting={name:'Alex',line:{person:'Ria',since:new Date(Date.UTC(2026,9,29,9)).toISOString(),card:'0123456789abcdef'}};
 let h=await head();
 assert.equal(h.title,'Hi Alex');assert.equal(h.line,'Ria has been waiting on your reply since Thursday.');assert.equal(h.href,'#card=0123456789abcdef');
 h=await head(390);assert.ok(h.titleShown,'the hello shows on a phone');assert.equal(h.line,'Ria has been waiting on your reply since Thursday.');
 greeting.line.since=new Date(NOW-26*3600e3).toISOString();assert.equal((await head()).line,'Ria has been waiting on your reply since yesterday.');
 greeting.line.since=new Date(NOW-9*864e5).toISOString();assert.equal((await head()).line,'Ria has been waiting on your reply for over a week.');
 greeting={name:'Alex'};h=await head();assert.equal(h.title,'Hi Alex');assert.equal(h.line,'');  // nothing ready yet
 // The list leads with the hello's to-do, also when it needs a decision and prepared ones would come first, and Needs you stays away
 cards=LIST;skills={waiting:1};
 for(const lead of LIST){greeting={name:'Alex',line:{person:'Ria',since:new Date(NOW-30*3600e3).toISOString(),card:lead.id}};h=await head();
  assert.equal(h.first,h.href.slice(6),'the first to-do is the one the hello names');assert.equal(h.first,lead.id);
  assert.equal(h.firstSection,'For you');assert.equal(h.needsYou,false);assert.equal(h.fixed,false)}
 // A signed-out connection still shows: on day one it means the Machine can't work. The waiting skill stays away.
 connectors=[{id:'work',service:'gmail',display_name:'alex@example.com',signed_out:true}];h=await head();
 assert.deepEqual(h.needs,['Signed out of Email (alex@example.com).']);
 if(process.env.SHOTS){const c=await browser.newContext({viewport:{width:390,height:844},timezoneId:'UTC',locale:'en-US',colorScheme:'light',deviceScaleFactor:2}),p=await c.newPage();
  await c.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());await p.clock.setFixedTime(NOW);await p.goto(base+'/');
  await p.locator('#needs-you li').first().waitFor();await p.waitForTimeout(500);await p.screenshot({path:process.env.SHOTS+'/greeting-signed-out-390-light.png'});await c.close()}
 // One line per account, not per service: Gmail and Calendar share one Google sign-in, so one Reconnect restores both
 const expired='google_signin_expired_run_gog_auth_add';
 connectors=['gmail','calendar'].map(s=>({id:s,service:s,display_name:'alex@example.com',email:'alex@example.com',error:expired}));h=await head();
 assert.deepEqual(h.needs,['Sign in to Google again. alex@example.com']);assert.equal(h.reconnects,1);
 connectors.push({id:'other',service:'gmail',display_name:'sam@example.com',email:'sam@example.com',error:expired});
 assert.deepEqual((await head()).needs,['Sign in to Google again. alex@example.com','Sign in to Google again. sam@example.com']);
 greeting=null;connectors=connectors.slice(0,2);h=await head();
 assert.equal(h.needs.filter(x=>x.startsWith('Sign in to')).length,1,'also after the hello');
 greeting={name:'Alex',line:{person:'Ria',since:new Date(NOW-30*3600e3).toISOString(),card:LIST[0].id}};
 connectors=[];
 greeting=null;h=await head();assert.equal(h.first,LIST[0].id);assert.equal(h.firstSection,'For you');assert.equal(h.needsYou,true,'Needs you is back once the hello is over');assert.equal(h.fixed,true);
 cards=[];skills=undefined;
 greeting=null;h=await head();assert.notEqual(h.title,'Hi Alex');assert.ok(h.title.length>3);  // over: the tagline
 assert.deepEqual(errors,[]);
 console.log('greeting ok');
}finally{await browser.close();server.close()}
