import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The owner asks in a to-do's chat to rename it; the run saves the new title and its reply says so. The chat's heading
// and the sidebar row show the new title with that reply, from the chat's own read (card_chat carries the title), not
// only once the to-do list is read again: the list here keeps the old title until the run ends. Synthetic data only.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),t0=Date.now()-600000;
const ID='a1a1a1a1a1a1a1a1',OLD='Send the statements to the bookkeeper',NEW='Gather and send the statements by Tuesday';
let title=OLD,renamed=false,listReads=0;
const card=()=>({id:ID,title:OLD,body:'The reply went out; the files are still to send.',status:'instructions',scope:'work',created_at:now,event_ids:[1],preparation_status:'running'});
const state=()=>({suggestions:[card(),{id:'b2b2b2b2b2b2b2b2',title:'Answer the venue',body:'x',status:'pending',scope:'work',created_at:now,event_ids:[2]}],
 promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]}});
const items=()=>[{kind:'you',text:'Rename it to "'+NEW+'"',at:t0},...(renamed?[{kind:'reply',text:'Renamed the task.',at:t0+2000}]:[])];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){listReads++;res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');
  // The run is still going (active): the list isn't read again on its account
  if(r.action==='card_chat'&&r.args.suggestion_id===ID){res.end(JSON.stringify({session:true,status:'running',active:true,cursor:'k'+renamed,title,title_suggested:renamed?OLD:null,items:items()}));return}
  if(r.action==='card_chat'){res.end(JSON.stringify({session:false,active:false,items:[],title:'Answer the venue',title_suggested:null}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+ID).waitFor();
 await page.evaluate(id=>{location.hash='chat='+id},ID);await page.locator('.chat-title').waitFor();
 const row=page.locator(`#side-cards a[href="#chat=${ID}"]`);
 assert.equal((await page.locator('.chat-title').textContent()).trim(),OLD);
 // The run saves the rename and replies
 title=NEW;renamed=true;const reads=listReads;
 await page.waitForFunction(()=>/Renamed the task/.test(document.querySelector('#chat-log')?.textContent||''));
 await page.waitForFunction(t=>document.querySelector('.chat-title')?.textContent.trim()===t,NEW,{timeout:3000});
 assert.equal((await row.textContent()).trim(),NEW);
 assert.equal(listReads,reads,'shown from the chat read, without waiting for the list');
 // Reset to the suggested title is offered: the earlier one waits there
 assert.equal(await page.evaluate(id=>state.suggestions.find(s=>s.id===id).title_suggested,ID),OLD);
 // Another chat's read never touches this to-do
 await page.evaluate(()=>{location.hash='chat=b2b2b2b2b2b2b2b2'});await page.waitForFunction(()=>document.querySelector('.chat-title')?.textContent.trim()==='Answer the venue');
 assert.equal((await row.textContent()).trim(),NEW);
 await context.close();
 assert.deepEqual(errors,[])}
finally{await browser?.close();server.close()}
console.log('chat rename ok');
