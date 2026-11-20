// A sent to-do names what went out ("Telegram message sent."), for every kind of message a to-do can send (SENDS,
// machine/kinds.py): a new send kind adds its message id here, so it can't fall back to "Email sent". Telegram's own
// to-do line: tests/test_sent_lines.py. Made-up data, a local fixture server, nothing sent. 390 and 1440;
// SHOT_DIR=<folder> saves screenshots of a sent Telegram to-do.
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

const dashboard=await dashboardPage();
// a message id each kind's send returns, and the line its sent to-do shows
const SENT={
 email:['<m1@mail.example>','Email sent.'],
 linkedin:['urn:li:msg:1','LinkedIn message sent.'],
 slack:['slack:C1:1700000000.0001','Slack message sent.'],
 x:['xdm:1','X message sent.'],
 whatsapp:['whatsapp:3EB0AA','WhatsApp message sent.'],
 telegram:['telegram:42:7','Telegram message sent at {}.'],
 signal:['signal:chat1:1700000000000','Signal message sent.'],
 intercom:['intercom:9:1','Sent as Alex in Intercom.'],
 teams:['teams:19:a1b2c3@unq.gbl.spaces:m2','Teams message sent.'],
 doc_reply:['doc:c1:r1','Reply posted in the doc.'],
};
const sentAt=new Date(Date.now()-20*60e3).toISOString();
const id=i=>(i.toString(16)+'0'.repeat(16)).slice(0,16);
const kinds=Object.keys(SENT);
const cards=kinds.map((kind,i)=>({id:id(i+1),title:kind==='telegram'?'Confirm Thursday with Sam':'Reply to Sam ('+kind+')',body:'Drafted a reply.',
 status:'completed',scope:'work',created_at:sentAt,closed_at:sentAt,event_ids:[i+1],
 next_actions:[{kind,label:'Send reply',revision:'r'+i,to_name:'Sam Example',as_name:'Alex',body:'Thursday works, see you then.',
  state:{status:'sent',message_id:SENT[kind][0],...(kind==='telegram'?{sent_at:sentAt}:{})}}]}));
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},done_counts:{all:cards.length,work:cards.length,personal:0},decisions:[],
 analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:[],next:null,total:cards.length}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOT_DIR;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]]){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  // every kind the app can send has its line here
  assert.deepEqual([...await page.evaluate(()=>SENDS)].sort(),[...kinds].sort(),'a new send kind adds its message id and sent line to SENT');
  await page.evaluate(()=>{const d=$('#finished-list');if(d&&!d.open){d.open=true;listShow(d)}});
  const hm=await page.evaluate(at=>fmtHM(at,{timeZone:state?.hours?.timezone||undefined}),sentAt);
  for(const [i,kind] of kinds.entries()){
   const task=page.locator('#task-'+id(i+1));await task.waitFor();
   const note=(await task.locator('.note.sent-ok').innerText()).trim();
   assert.equal(note,SENT[kind][1].replace('{}',hm),kind);
   if(kind!=='email')assert.doesNotMatch(await task.innerText(),/Email sent/,kind);
   assert.doesNotMatch(await task.innerText(),/\bYou (sent|replied|posted)/,kind);
  }
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll at '+width);
  if(shots){const task=page.locator('#task-'+id(kinds.indexOf('telegram')+1));await task.scrollIntoViewIfNeeded();
   await task.screenshot({path:`${shots}/telegram-sent-${width}.png`});await page.screenshot({path:`${shots}/telegram-sent-page-${width}.png`})}
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('sent lines dashboard ok');
