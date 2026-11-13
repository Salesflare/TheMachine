import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {createServer} from 'node:http';
const {chromium}=await import('./browser.mjs');

// The page's own script (app-<hash>.js, served as the Machine serves it: machine/web/serving.py dashboard_files) that
// doesn't come, as on a computer that just woke up with its link still down: never a blank or half-drawn page. The page
// says "The page didn’t load" (in the owner's language from the kept catalog) with Try again, tries again by itself once
// the device is online, and a normal load never shows it.
const [source,lazy]=JSON.parse(execFileSync('python3',['-c','import json,dashboard_parts;print(json.dumps(dashboard_parts.assemble_split()))'],{encoding:'utf8',maxBuffer:1<<26}));
const named=s=>createHash('sha256').update(s).digest('hex').slice(0,16)+'.js';
const files=Object.fromEntries(Object.entries(lazy).map(([group,script])=>['lazy-'+group+'-'+named(script),script]));
const cut=source.lastIndexOf('<script>\n'),script=source.slice(cut+9,source.lastIndexOf('</script></html>')),main='app-'+named(script);
const lazyNames=Object.fromEntries(Object.keys(files).map(f=>[f.split('-')[1],f]));
const page=(source.slice(0,cut)+`<script>self.LAZY_FILES=${JSON.stringify(lazyNames)}</script><script src="${main}"></script></html>\n`)
 .replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__','s'.repeat(32));
const iso=new Date().toISOString();
const state={suggestions:[{id:'1'.repeat(16),title:'Reply to Robin about the plan',body:'Robin asked for the numbers.',status:'pending',scope:'work',created_at:iso,event_ids:[1]}],
 promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false},ui_version:'v1'};
// what the main script does: 'ok', 'error' (the Machine's 503 while it restarts) or 'drop' (the link breaks mid-answer)
let mode='ok';const asked={page:0,main:0};
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid'),name=url.pathname.slice(1);res.setHeader('Cache-Control','no-store');
 if(url.pathname==='/'){asked.page++;res.setHeader('Content-Type','text/html');res.end(page);return}
 if(name===main){asked.main++;
  if(mode==='error'){res.statusCode=503;res.setHeader('Content-Type','application/json');res.end('{"restarting":true}');return}
  if(mode==='drop'){res.writeHead(200,{'Content-Type':'text/javascript','Content-Length':String(script.length)});res.write(script.slice(0,1000));setTimeout(()=>res.destroy(),30);return}
  res.setHeader('Content-Type','text/javascript');res.end(script);return}
 if(files[name]){res.setHeader('Content-Type','text/javascript');res.end(files[name]);return}
 res.setHeader('Content-Type','application/json');if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:'s'.repeat(32)}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname==='/sw.js'?404:200;res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
// its words, when it covers the whole window (a page half drawn behind it would still read as broken)
const shown=p=>p.evaluate(()=>{const b=document.querySelector('#load-failed'),r=b.getBoundingClientRect();
 if(b.hidden)return '';if(r.left>0||r.top>0||r.right<innerWidth-20||r.bottom<innerHeight-20)return 'not covering: '+JSON.stringify(r);  /* less a scrollbar */
 return b.innerText.replace(/\s+/g,' ').trim()});
const drawn=p=>p.locator('#suggestions article[id]').first().waitFor({timeout:15000});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440]){
  const context=await browser.newContext({viewport:{width,height:width<500?844:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const p=await context.newPage();p.on('pageerror',e=>errors.push(width+': '+e.message));

  // 1. A normal load: the to-dos, never the notice
  mode='ok';await p.goto(base,{waitUntil:'load'});await drawn(p);
  assert.equal(await shown(p),'',width+': a normal load never shows it');
  assert.equal(await p.evaluate(()=>self.appStarted),true);

  // 2. The script fails (503, then a dropped link): the notice over the whole window, not a blank page
  for(const how of ['error','drop']){
   mode=how;await p.goto(base,{waitUntil:'load'});
   await p.waitForFunction(()=>!document.querySelector('#load-failed').hidden,null,{timeout:10000});
   assert.equal(await shown(p),'The page didn’t load Try again',width+' '+how+': what happened and Try again');
   assert.equal(await p.evaluate(()=>self.appStarted),undefined,how+': the script never ran')}

  // 3. Try again, once the Machine answers: the page itself, drawn
  mode='ok';await p.click('#load-failed button');await drawn(p);
  assert.equal(await shown(p),'',width+': gone once the page loaded');

  // 4. Back online after a wake: tried again by itself, no tap
  mode='error';await context.setOffline(false);await p.goto(base,{waitUntil:'load'});
  await p.waitForFunction(()=>!document.querySelector('#load-failed').hidden,null,{timeout:10000});
  const before=asked.page;mode='ok';await context.setOffline(true);await context.setOffline(false);
  await drawn(p);assert.ok(asked.page>before,'the page asked for again once online');
  assert.equal(await shown(p),'');

  // 5. In the owner's language, from the catalog kept on this device (the main script, which loads catalogs, never came)
  await p.evaluate(()=>localStorage.setItem('i18n',JSON.stringify({lang:'nl',ver:'v1',en:{},cat:{'The page didn’t load':'De pagina laadde niet','Try again':'Opnieuw proberen'}})));
  mode='error';await p.goto(base,{waitUntil:'load'});
  await p.waitForFunction(()=>!document.querySelector('#load-failed').hidden,null,{timeout:10000});
  assert.equal(await shown(p),'De pagina laadde niet Opnieuw proberen',width+': in the kept language');
  await p.evaluate(()=>localStorage.removeItem('i18n'));
  await context.close()}
 assert.deepEqual(errors.filter(e=>!/Failed to load|Load failed|NetworkError|net::/.test(e)),[]);
 console.log('ok: the page never stays blank when its script doesn’t load');
}finally{await browser?.close();server.close()}
