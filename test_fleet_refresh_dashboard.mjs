import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from './openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');
const dashboard=await readFile(new URL('./dashboard.html',import.meta.url),'utf8');
const FL='fl_'+'a'.repeat(16),rules={relationships:{rule:'ask',details:false}};
let view={on:true,kinds:{relationships:'who knows someone'},fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Example',asks:[],people:[],members:[{member_id:'p',name:'Pat',rules}],rules,exceptions:{}}],waiting:[],asked:[],free:[],briefs:{},log:[],notices:[]};
const pending=[],calls=[];let hold=false;
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');return res.end(dashboard)}
 if(req.url==='/api/status')return res.end(JSON.stringify({suggestions:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}}));
 if(req.url.startsWith('/api/fleet')){const body=JSON.stringify(view);if(hold)return pending.push(()=>res.end(body));return res.end(body)}
 if(req.url==='/api/action'){let body='';for await(const part of req)body+=part;calls.push(JSON.parse(body));return res.end('{"ok":true}')}
 res.statusCode=404;res.end('{}');});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try {
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.locator('nav [data-tab="fleet"]').click();await page.locator('.fleet-free-form').waitFor();
 await page.locator('.fleet-free-form input').fill('Anyone know a good notary?');
 await page.evaluate(()=>{window.originalForm=document.querySelector('.fleet-free-form');});
 await page.evaluate(()=>fleetView());
 assert.equal(await page.evaluate(()=>window.originalForm===document.querySelector('.fleet-free-form')),true,'unchanged response replaced the active form');
 assert.equal(await page.locator('.fleet-free-form input').inputValue(),'Anyone know a good notary?');
 // Changed data keeps the owner draft too, without stale requests overwriting a newer response.
 hold=true;view={...view,fleets:[{...view.fleets[0],name:'Old name'}]};
 await page.evaluate(()=>{void fleetView();});await page.waitForFunction(()=>true);for(let i=0;i<100&&pending.length<1;i++)await page.waitForTimeout(10);
 assert.equal(pending.length,1);
 view={...view,fleets:[{...view.fleets[0],name:'Latest name'}]};
 await page.evaluate(()=>{void fleetView(true);});for(let i=0;i<100&&pending.length<2;i++)await page.waitForTimeout(10);
 assert.equal(pending.length,2);pending[1]();await page.locator('.fleet-pane-head h2',{hasText:/^Latest name$/}).waitFor();pending[0]();
 await page.waitForTimeout(50);
 assert.equal(await page.locator('.fleet-free-form input').inputValue(),'Anyone know a good notary?');
 assert.equal(await page.locator('.fleet-pane-head h2',{hasText:/^Old name$/}).count(),0);
 hold=false;await page.locator('.fleet-free-form button').click();
 for(let i=0;i<100&&!calls.length;i++)await page.waitForTimeout(10);
 assert.deepEqual(calls,[{action:'fleet_free',args:{text:'Anyone know a good notary?',fleet:FL}}]);
 const connected=view;view={on:false};await page.evaluate(()=>fleetView());
 await page.getByText(/^This Machine is not in a Fleet\./).waitFor();
 view=connected;await page.evaluate(()=>fleetView());await page.locator('.fleet-free-form').waitFor();
 assert.deepEqual(errors,[]);console.log('Fleet refresh: unchanged form, draft preservation, latest response, reconnect and exact submit passed.');
}finally{await browser.close();server.close()}
