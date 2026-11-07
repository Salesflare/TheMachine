import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// api/status as changes (machine/web/status_delta.py): the page sends its last token back and puts the answer together
// again: a part left out stays as it was, a row {"=": id} is that row as before, a changed row replaces it, and a
// token the server no longer knows ends in one whole answer. No network beyond this fake server.
const dashboard=await dashboardPage();
const card=(id,title)=>({id,title,body:'',status:'pending',event_ids:[],scope:'work',created_at:new Date().toISOString()});
const base={suggestions:[card('c1','Reply to Ann'),card('c2','Send the invoice')],connectors:[],suggestion_counts:{pending:2},decisions:[],analyses:[],
 deliveries:[],review_health:{},review_runs:[]};
const asked=[];let answer=()=>({...base,_token:'t1'});
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url.startsWith('/api/status')){const since=new URL(req.url,'http://x').searchParams.get('since');asked.push(since);res.end(JSON.stringify(answer(since)));return}
 if(req.url==='/api/action'){res.end('{}');return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 const page=await (await browser.newContext({viewport:{width:390,height:900}})).newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/');
 await page.waitForFunction(()=>state?.suggestions?.length===2);
 assert.equal(asked[0],null);  // the first ask has no token

 // c1 changed, c2 by id, the rest left out
 answer=since=>since==='t1'?{_token:'t2',_since:'t1',suggestions:[{...card('c1','Reply to Ann today')},{'=':'c2'}]}:{...base,_token:'tx'};
 await page.evaluate(()=>refresh());
 assert.equal(asked.at(-1),'t1');
 const got=await page.evaluate(()=>({titles:state.suggestions.map(s=>s.title),connectors:Array.isArray(state.connectors),token:statusRaw._token}));
 assert.deepEqual(got,{titles:['Reply to Ann today','Send the invoice'],connectors:true,token:'t2'});
 await page.waitForFunction(()=>document.body.textContent.includes('Reply to Ann today'));

 // what the page changes on its copy never reaches the kept answer
 await page.evaluate(()=>{state.suggestions[1].title='changed here'});
 answer=since=>({_token:'t3',_since:since,suggestions:[{'=':'c1'},{'=':'c2'}]});
 await page.evaluate(()=>refresh());
 assert.deepEqual(await page.evaluate(()=>state.suggestions.map(s=>s.title)),['Reply to Ann today','Send the invoice']);

 // an answer for another token (two polls crossed): asked again in full
 const before=asked.length;
 answer=since=>since?{_token:'t9',_since:'t-other'}:{...base,_token:'t4'};
 await page.evaluate(()=>refresh());
 assert.deepEqual(asked.slice(before),['t3',null]);
 assert.deepEqual(await page.evaluate(()=>[state.suggestions.map(s=>s.title),statusRaw._token]),[['Reply to Ann','Send the invoice'],'t4']);
 assert.deepEqual(errors,[]);
 console.log('status delta dashboard ok');
}finally{await browser.close();server.close()}
