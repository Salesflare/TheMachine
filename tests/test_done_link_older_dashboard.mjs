import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The status sends only the Done list's first page of done to-dos. A chat or card link to an older done one (a
// notification, Activity) asks the Machine for that one to-do and opens it, instead of "That to-do isn't here
// anymore". A link to one that is really gone still says so, after asking once.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),old=new Date(Date.now()-20*864e5).toISOString();
const OPEN='a1a1a1a1a1a1a1a1',OLD='b2b2b2b2b2b2b2b2',GONE='c3c3c3c3c3c3c3c3';
const card=(id,title,status,at)=>({id,title,body:'Ready.',status,preparation_status:'ok',scope:'work',created_at:at,event_ids:[1],...(status==='completed'?{closed_at:at}:{})});
const status=()=>({suggestions:[card(OPEN,'Check the payroll is ready','prepared',now)],done_counts:{all:40,work:40,personal:0},promises:[],suggestion_counts:{},decisions:[],
 analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const asked=[];
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/cards/done'){const id=url.searchParams.get('id');if(id)asked.push(id);
  res.end(JSON.stringify(id===OLD?{cards:[card(OLD,'Send the signed lease back','completed',old)],next:null,total:1}:id?{cards:[],next:null,total:0}:{cards:[],next:null,total:40}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const open=async hash=>{const page=await context.newPage();page.on('pageerror',e=>errors.push(hash+': '+e.message));await page.goto(base+hash);await page.waitForFunction(()=>!!state?.suggestions);return page};
 // A chat link to an older done one: asked for, and its chat opens
 let page=await open('#chat='+OLD);
 await page.waitForFunction(id=>chatOpen()?.id===id,OLD,{timeout:8000});
 assert.equal(await page.evaluate(()=>location.hash),'#chat='+OLD,'the chat stays on its link');
 assert.doesNotMatch(await page.locator('#toast').textContent(),/isn.t here/,'no "isn\'t here anymore" for one that is only older');
 await page.evaluate(()=>refresh());
 assert.equal(await page.evaluate(()=>chatOpen()?.id),OLD,'a poll keeps it');
 assert.deepEqual(asked,[OLD],'asked for once');
 await page.close();
 // A card link to it shows the card
 page=await open('#card='+OLD);
 await page.locator('#task-'+OLD).waitFor({timeout:8000});
 await page.close();
 // One that is really gone: asked once, then the short line as before
 asked.length=0;page=await open('#chat='+GONE);
 await page.waitForFunction(()=>/isn.t here anymore/.test(document.querySelector('#toast')?.textContent||''),null,{timeout:8000});
 assert.equal(await page.evaluate(()=>location.hash),'');
 assert.deepEqual(asked,[GONE]);
 await page.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
