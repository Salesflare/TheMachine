import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The parts that load when first needed (dashboard_parts.py LAZY), served as the Machine serves them
// (machine/web/serving.py dashboard_files): To-dos draws without them and nothing breaks while they're on their way; the
// rest of the page is drawn once they're in, and then Help and the game work as before. When they can't load, the
// rest is drawn all the same.
const [source,lazy]=JSON.parse(execFileSync('python3',['-c','import json,dashboard_parts;print(json.dumps(dashboard_parts.assemble_split()))'],{encoding:'utf8',maxBuffer:1<<26}));
const named=s=>createHash('sha256').update(s).digest('hex').slice(0,16)+'.js';
const files=Object.fromEntries(Object.entries(lazy).map(([group,script])=>['lazy-'+group+'-'+named(script),script]));
const cut=source.lastIndexOf('<script>\n'),script=source.slice(cut+9,source.lastIndexOf('</script></html>')),main='app-'+named(script);
const lazyNames=Object.fromEntries(Object.keys(files).map(f=>[f.split('-')[1],f]));
const page=(source.slice(0,cut)+`<script>self.LAZY_FILES=${JSON.stringify(lazyNames)}</script><script src="${main}"></script></html>\n`)
 .replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__','s'.repeat(32));
const state={suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}};
let hold=null,refuse=false;const asked=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid'),name=url.pathname.slice(1);
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page);return}
 if(name===main){res.setHeader('Content-Type','text/javascript');res.end(script);return}
 if(files[name]){asked.push(name);if(hold)await hold;if(refuse){res.statusCode=404;res.end('{}');return}res.setHeader('Content-Type','text/javascript');res.end(files[name]);return}
 res.setHeader('Content-Type','application/json');if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname==='/sw.js'?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const wholeDrawn=page=>page.waitForFunction(()=>document.querySelector('#decisions')?.children.length>0);
try{
 assert.deepEqual(Object.keys(lazyNames).sort(),Object.keys(lazy).sort());
 for(const s of Object.values(lazy))assert.ok(!script.includes(s),'a lazy group is not in the main script');
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440]){
  const context=await browser.newContext({viewport:{width,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const p=await context.newPage();p.on('pageerror',e=>errors.push(width+': '+e.message+' '+e.stack));
  // Held back: To-dos draws and the robot takes a poke; the rest waits
  let release;hold=new Promise(r=>release=r);asked.length=0;
  await p.goto(base,{waitUntil:'domcontentloaded'});await p.locator('#suggestions .all-clear .poke').waitFor();
  for(const until=Date.now()+20000;asked.length<Object.keys(files).length;){assert.ok(Date.now()<until,'the parts are asked for once To-dos is drawn');await new Promise(r=>setTimeout(r,50))}
  assert.equal(await p.evaluate(()=>typeof helpOpen+typeof openGame),'undefinedundefined');
  assert.equal(await p.evaluate(()=>document.querySelector('#decisions').children.length),0,'the rest waits for the parts');
  await p.locator('#suggestions .all-clear .poke').click();
  assert.ok((await p.locator('#suggestions .poke-line').innerText()).length>0);
  // In: the rest is drawn, Help opens, and the fourth poke's game plays
  console.log(await p.evaluate(()=>[!!document.getElementById('settings-share'),!!document.querySelector('#settings'),String($)]));
  release();hold=null;await wholeDrawn(p);
  assert.deepEqual(asked.sort(),Object.keys(files).sort(),'each part is asked for once');
  await p.evaluate(()=>document.querySelector('#open-help').click());await p.locator('#help-panel[open]').waitFor();
  await p.evaluate(()=>document.querySelector('#help-panel').close());
  for(let i=0;i<3;i++)await p.locator('#suggestions .all-clear .poke').click();
  await p.locator('#suggestions .all-clear .play').click();await p.locator('#game-dialog[open]').waitFor();
  await context.close();
 }
 // Can't load (offline without a kept copy): the rest is drawn all the same, and the game says so
 {refuse=true;const context=await browser.newContext({viewport:{width:1440,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const p=await context.newPage();p.on('pageerror',e=>errors.push('refused: '+e.message));
  await p.goto(base);await wholeDrawn(p);
  for(let i=0;i<4;i++)await p.locator('#suggestions .all-clear .poke').click();
  await p.locator('#suggestions .all-clear .play').click();
  await p.locator('#toast.show.error',{hasText:'Offline.'}).waitFor();
  assert.equal(await p.locator('#game-dialog[open]').count(),0);
  await context.close();refuse=false}
 assert.deepEqual(errors,[]);
 console.log('ok lazy parts');
}finally{await browser?.close();server.close()}
