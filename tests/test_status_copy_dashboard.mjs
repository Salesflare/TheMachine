import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The page works on a copy of the status (shell-tabs.js statusMerge, jsonCopy) and keeps the answer as the server sent
// it (statusRaw), which the next answer's changes are joined onto. The copy is a true deep copy, the same as
// JSON.parse(JSON.stringify()): changing anything in it, however deep, never changes what the page keeps.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[{id:'a1a1a1a1a1a1a1a1',title:'Check the payroll is ready',body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base=`http://127.0.0.1:${server.address().port}/`;
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(base);
 await page.waitForFunction(()=>typeof drawnWhole!=='undefined'&&drawnWhole);
 const out=await page.evaluate(()=>{
  // Every kind of JSON value, nested, plus what JSON.stringify drops or changes
  const make=()=>{const v=JSON.parse('{"__proto__":{"polluted":true},"a":1,"s":"tëxt ✓","n":null,"t":true,"f":false,"z":0,"neg":-1.5,"e":[],"o":{},'+
   '"list":[1,"two",null,{"deep":{"deeper":[{"x":[1,2,{"y":"z"}]}]}},[[3]]],"rows":[{"id":1,"tags":["a"]},{"id":2,"tags":[]}]}');
   v.undef=undefined;v.fn=()=>1;v.list.push(undefined);v.rows[0].gone=undefined;return v};
  const src=make(),want=JSON.parse(JSON.stringify(src)),got=jsonCopy(src);
  // The same keys in the same order and the same values all the way down (not only the same JSON text)
  const equal=(x,y)=>{if(x===null||typeof x!=='object')return Object.is(x,y);if(!y||typeof y!=='object'||Array.isArray(x)!==Array.isArray(y))return false;
   const kx=Object.keys(x),ky=Object.keys(y);return kx.length===ky.length&&kx.every((k,i)=>k===ky[i]&&equal(x[k],y[k]))};
  const res={same:JSON.stringify(got)===JSON.stringify(want)&&equal(got,want),keys:Object.keys(got).join()===Object.keys(want).join(),
   protoOwn:Object.prototype.hasOwnProperty.call(got,'__proto__')&&Object.getPrototypeOf(got)===Object.prototype,polluted:({}).polluted===undefined};
  // No object or list of the copy is one of the source's
  const objs=v=>{const s=new Set();const walk=x=>{if(x&&typeof x==='object'){s.add(x);for(const k of Object.keys(x))walk(x[k])}};walk(v);return s};
  const a=objs(src);res.shared=[...objs(got)].filter(x=>a.has(x)).length;
  // Changing the copy everywhere leaves the source as it was
  const before=JSON.stringify(src);
  const scribble=x=>{if(Array.isArray(x)){x.forEach(scribble);x.push('more');x.reverse()}else if(x&&typeof x==='object'){for(const k of Object.keys(x)){scribble(x[k]);x[k+'_new']=1;if(typeof x[k]!=='object')x[k]='changed'}}};
  scribble(got);res.untouched=JSON.stringify(src)===before;
  // statusMerge: a whole answer, then one with changes joined on; the page's copy changed never reaches statusRaw
  const full={_token:'t1',suggestions:[{id:'x1',title:'One',meta:{n:1}},{id:'x2',title:'Two',meta:{n:2}}],counts:{a:1}};
  const keep=JSON.stringify(full),one=statusMerge(full);one.suggestions[0].meta.n=99;one.suggestions.pop();one.counts.a=7;
  res.fullKept=JSON.stringify(statusRaw)===keep;
  const two=statusMerge({_since:'t1',_token:'t2',suggestions:[{'=':'x1'},{id:'x2',title:'Two again',meta:{n:3}}]});
  res.joined=JSON.stringify(two)===JSON.stringify({_token:'t2',suggestions:[{id:'x1',title:'One',meta:{n:1}},{id:'x2',title:'Two again',meta:{n:3}}],counts:{a:1}});
  const raw=JSON.stringify(statusRaw);two.suggestions[0].meta.n=5;two.suggestions[1].title='x';delete two.counts;
  res.deltaKept=JSON.stringify(statusRaw)===raw;
  return res});
 assert.deepEqual(out,{same:true,keys:true,protoOwn:true,polluted:true,shared:0,untouched:true,fullKept:true,joined:true,deltaKept:true});
 await page.close();
 assert.deepEqual(errors,[]);
 console.log('ok: the status copy is a true deep copy');
}finally{await browser?.close();server.close()}
