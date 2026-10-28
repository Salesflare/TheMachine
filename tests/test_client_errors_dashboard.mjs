import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Error reports from the dashboard, the whole way (error_feed.py, docs/help/error-reports.md): a bug in the page's own
// code that a try caught and showed (most of the page runs inside one: before this, only what reached window.onerror
// was reported, and that was close to nothing), a window error, an unhandled rejection, the service worker's errors
// and failed shell updates, and failed API calls (5xx and timeouts, never 4xx, restarts or the query) go from the page
// to api/action client_error; the real app (assistant.py) records them and builds the batch for the Network, and what
// it sends carries no name, address or query.
const root=new URL('..',import.meta.url);
const dashboard=await readFile(new URL('dashboard.html',root),'utf8');
const posted=[];
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 let body='';req.on('data',c=>body+=c);req.on('end',()=>{
  if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
  if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_runs:[]}));return}
  if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64)}));return}
  if(url.pathname==='/api/boom'){res.statusCode=500;res.end(JSON.stringify({error:'boom for sam.lee@globex.example'}));return}
  if(url.pathname==='/api/graph/node/4f2c9a'){res.statusCode=504;res.setHeader('Content-Type','text/html');res.end('<h1>Gateway Timeout</h1>');return}
  if(url.pathname==='/api/away'){res.statusCode=502;res.setHeader('Content-Type','text/html');res.end('<h1>Bad Gateway</h1>');return}
  if(url.pathname==='/api/restarting'){res.statusCode=503;res.end(JSON.stringify({error:'restarting',restarting:true}));return}
  if(url.pathname==='/api/refused'){res.statusCode=400;res.end(JSON.stringify({error:'Pick a date'}));return}
  if(url.pathname==='/api/action'){const d=JSON.parse(body||'{}');
   if(d.action==='client_error'){posted.push(...d.args.errors);res.end('{"ok":true,"counted":1}');return}
   if(d.action==='decide'){res.statusCode=502;res.end(JSON.stringify({error:'model down'}));return}}
  res.end('{}')})});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext();const page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await page.goto(base+'/');await page.waitForFunction(()=>typeof errCaught==='function'&&state.suggestions);
 await page.evaluate(async()=>{
  // A render bug inside refresh(): it catches it and shows a notice; it is reported all the same
  const keep=deviceRender;deviceRender=()=>$('[[Sam Lee');await refresh();deviceRender=keep;
  // A window error and an unhandled rejection, both in the page's own code ($), one with an address in its message
  setTimeout($,0,'[[window');Promise.resolve('[[sam.lee@globex.example').then($);
  // A thrown Error is the page's own message to the owner, not a bug; a failed fetch is the network
  errCaught(new Error('Pick a date for Sam Lee'));errCaught(new TypeError('Failed to fetch'));
  // Failed calls: a 5xx the Machine answered, a gateway timeout, a failed action; not the Machine away, restarting or a refusal
  for(const [path,options] of [['api/boom?q=sam.lee@globex.example'],['api/graph/node/4f2c9a'],['api/away'],['api/restarting'],['api/refused'],
   ['api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'decide',args:{note:'for Sam Lee'}})}]])
   await request(path,options).catch(()=>{});
  // The service worker's report, as sw.js posts it to the page
  navigator.serviceWorker.dispatchEvent(new MessageEvent('message',{data:{swError:{kind:'ShellUpdateFailed',message:'HTTP 500',function:'shell',line:0}}}));
 });
 await page.waitForFunction(()=>!errQueue.length&&errCount>=7,null,{timeout:10000});await page.waitForTimeout(500);
 await context.close();
}finally{await browser?.close();server.close()}

const of=(f)=>posted.filter(f);
assert.equal(of(x=>x.file==='dashboard.html').length,3,JSON.stringify(posted));
assert.ok(of(x=>x.file==='dashboard.html').every(x=>x.function==='$'&&x.kind==='SyntaxError'&&x.line>0));
assert.ok(!posted.some(x=>/Pick a date|Failed to fetch/.test(x.message||'')),'a message to the owner and the network are not bugs');
assert.deepEqual(of(x=>'api' in x).map(x=>[x.api,x.action,x.status]),[['boom','',500],['graph/node/4f2c9a','','timeout'],['action','decide',502]]);
assert.ok(!JSON.stringify(of(x=>'api' in x)).includes('globex'),'never the query or what was sent');
assert.deepEqual(of(x=>x.file==='sw.js'),[{kind:'ShellUpdateFailed',message:'HTTP 500',file:'sw.js',function:'shell',line:0}]);

// sw.js itself: a shell update the Machine answered with a 5xx, and an error in the worker, go to an open page
const sw=await readFile(new URL('sw.js',root),'utf8');const swPosts=[],listeners={};
const self={location:{origin:'https://m.example'},registration:{scope:'https://m.example/'},navigator:{onLine:true},
 addEventListener:(t,f)=>(listeners[t]=f),clients:{matchAll:async()=>[{postMessage:m=>swPosts.push(m)}],claim:async()=>{}}};
const ctx=vm.createContext({self,URL,Response,Headers,Promise,Date,String,Error,setTimeout,AbortSignal,
 caches:{open:async()=>({match:async()=>null,put:async()=>{}}),keys:async()=>[],delete:async()=>true},
 fetch:async()=>new Response('<h1>Bad Gateway</h1>',{status:502,headers:{'Content-Type':'text/html'}})});
vm.runInContext(sw,ctx,{filename:'https://m.example/sw.js'});
const waits=[];await listeners.fetch({request:{method:'GET',mode:'navigate',url:'https://m.example/'},respondWith:p=>waits.push(p),waitUntil:p=>waits.push(p)});
await Promise.all(waits);await new Promise(r=>setTimeout(r,20));
const boom=new TypeError('x.y is undefined');boom.stack='TypeError: x.y is undefined\n    at keepShell (https://m.example/sw.js:42:7)';
listeners.error({error:boom});await new Promise(r=>setTimeout(r,20));
assert.deepEqual(JSON.parse(JSON.stringify(swPosts)),[{swError:{kind:'ShellUpdateFailed',message:'HTTP 502',function:'shell',line:0}},
 {swError:{kind:'TypeError',message:'x.y is undefined',function:'keepShell',line:42}}]);

// And the app: record_client in the real action, then the batch the Network gets
const py=`
import importlib.util, json, sys, tempfile, sqlite3
from pathlib import Path
sys.path.insert(0, '.')
spec = importlib.util.spec_from_file_location('client_errors_assistant', 'assistant.py'); a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import error_feed
app = object.__new__(a.App); app.store = a.Store(Path(tempfile.mkdtemp()) / 'e.sqlite'); app.fleet = None; app.config = {'accounts': []}
print(json.dumps(app.action('client_error', {'errors': json.load(sys.stdin)})))
with app.store.connect() as db:
    print(json.dumps(error_feed.batch(db, names=['sam lee', 'sam', 'lee'])))
`;
const run=spawnSync(process.env.PYTHON||(process.platform==='win32'?'python':'python3'),['-c',py],{cwd:fileURLToPath(root),input:JSON.stringify(posted),encoding:'utf8'});
assert.equal(run.status,0,run.stderr);
const [answer,batch]=run.stdout.trim().split('\n').map(l=>JSON.parse(l));
assert.equal(answer.counted,7);
const sent=batch.signatures.map(s=>[s.source,s.kind,s.where.replace(/:\d+$/,''),s.message]).sort();
assert.deepEqual(sent,[
 ['api','HTTP500','api:boom',''],
 ['api','HTTP502','api:action.decide',''],
 ['api','Timeout','api:graph.node.<id>',''],
 ['dashboard','SyntaxError','dashboard.html:$','Failed to execute "…" on "Document": "…" is not a valid selector.'],
 ['sw','ShellUpdateFailed','sw.js:shell','HTTP internal server error']]);
assert.equal(batch.signatures.find(s=>s.source==='dashboard').total,3,'three of the same bug, one signature');
for(const secret of ['Sam','Lee','sam.lee','globex','4f2c9a','Pick a date','model down'])assert.ok(!JSON.stringify(batch).includes(secret),secret);
console.log('client errors ok');
