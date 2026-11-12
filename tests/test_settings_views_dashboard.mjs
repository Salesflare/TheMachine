import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// What only Settings shows (signatures, the people lookup, the owner's addresses, Model's agents) is no longer built for
// every status: Settings asks api/settings when it opens, at most every 15 seconds while open. A page load without
// Settings never asks; a status poll keeps what Settings got; a status that still carries them (an older Machine) wins.
const dashboard=await dashboardPage();
const views={signatures:[{account_id:'mail',email:'owner@example.org',service:'gmail',html:'<b>Owner Sig</b>',source:'detected',saveable:true}],
 lookups:{people_available:true,people:true},own_addresses:null,agents_settings:null};
let old=false;
const state=()=>({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
 ...(old?{signatures:[{...views.signatures[0],html:'<b>From the status</b>'}]}:{})});
const asked=[];
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');asked.push(url.pathname);res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status')return res.end(JSON.stringify(state()));
 if(url.pathname==='/api/settings')return res.end(JSON.stringify(views));
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const settingsAsks=()=>asked.filter(p=>p==='/api/settings').length;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 const origin='http://127.0.0.1:'+server.address().port;
 // 1. A load and polls without Settings: never asked
 await page.goto(origin);await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
 await page.evaluate(async()=>{await refresh(true)});await page.waitForTimeout(300);
 assert.equal(settingsAsks(),0,'no Settings, no api/settings: '+asked.join(' '));
 // 2. Opening Settings asks once, and Writing shows the signature from it
 await navClick(page.locator('#open-settings'));
 await page.locator('#settings-tabs [data-settings-tab="writing"]:not([hidden])').waitFor();
 await page.locator('#settings-tabs [data-settings-tab="writing"]').click();
 await page.locator('#signatures .sig-form[data-account="mail"]').waitFor();  // its signature, in a frame of its own
 assert.equal(settingsAsks(),1);
 // 3. Status polls while it is open: the signature stays, and api/settings is not asked again within 15 seconds
 for(let i=0;i<3;i++){await page.evaluate(async()=>{await refresh(true)});await page.waitForTimeout(150)}
 assert.equal(await page.locator('#signatures .sig-form[data-account="mail"]').isVisible(),true,'kept over polls');
 assert.equal(await page.evaluate(()=>state.signatures?.[0]?.html),'<b>Owner Sig</b>');
 assert.equal(settingsAsks(),1,'at most every 15 seconds');
 // 4. 15 seconds on: asked again
 await page.evaluate(()=>{setViews.at=0;settingsSync()});await page.waitForTimeout(300);
 assert.equal(settingsAsks(),2);
 // 5. A status that carries them (an older Machine): the status's wins
 old=true;await page.evaluate(async()=>{await refresh(true);setViews.at=0;settingsSync()});await page.waitForTimeout(400);
 assert.equal(await page.evaluate(()=>state.signatures[0].html),'<b>From the status</b>');
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
