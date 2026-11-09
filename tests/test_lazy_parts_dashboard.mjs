import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The parts that load when first needed (dashboard_parts.py LAZY), served as the Machine serves them
// (machine/web/serving.py dashboard_files): the page loads and is drawn whole without them (the load event doesn't wait
// for them), and they're fetched after that. Calendar, Learning and Help opened while they're on their way open once
// they're in, and then Help, the game, Calendar and Learning work as before. The Graph's rules are in before its pages
// draw, and the Fleet tab draws once its views are in. Settings opened while its panels are on their way opens once
// they're in, drawn. A link straight to Calendar opens it once its part is in. When they can't load, the rest is drawn
// all the same, and Calendar, the Graph, Settings, the Fleet, Connections and the game say so. Connections draws once
// its views are in, its cards too.
const [source,lazy]=JSON.parse(execFileSync('python3',['-c','import json,dashboard_parts;print(json.dumps(dashboard_parts.assemble_split()))'],{encoding:'utf8',maxBuffer:1<<26}));
const named=s=>createHash('sha256').update(s).digest('hex').slice(0,16)+'.js';
const files=Object.fromEntries(Object.entries(lazy).map(([group,script])=>['lazy-'+group+'-'+named(script),script]));
const cut=source.lastIndexOf('<script>\n'),script=source.slice(cut+9,source.lastIndexOf('</script></html>')),main='app-'+named(script);
const lazyNames=Object.fromEntries(Object.keys(files).map(f=>[f.split('-')[1],f]));
const page=(source.slice(0,cut)+`<script>self.LAZY_FILES=${JSON.stringify(lazyNames)}</script><script src="${main}"></script></html>\n`)
 .replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__','s'.repeat(32));
const state={suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}],fleet:{on:false,fleets:[]}};
// holdOnly: only the part a block is about waits (a browser asks for at most 6 at a time from one host, so with the
// others held too, that part might never be asked for)
let hold=null,holdOnly=null,refuse=false;const asked=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid'),name=url.pathname.slice(1);
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page);return}
 if(name===main){res.setHeader('Content-Type','text/javascript');res.end(script);return}
 if(files[name]){asked.push(name);if(hold&&(!holdOnly||name.startsWith(holdOnly)))await hold;if(refuse){res.statusCode=404;res.end('{}');return}res.setHeader('Content-Type','text/javascript');res.end(files[name]);return}
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
  // Held back: the page loads (the load event doesn't wait for them) and is drawn whole, then asks for each of them
  let release;hold=new Promise(r=>release=r);asked.length=0;
  await p.goto(base,{waitUntil:'load'});await wholeDrawn(p);
  // (held, a browser asks for at most 6 at a time from one host: the rest are asked for as those come in)
  for(const until=Date.now()+20000;asked.length<Math.min(6,Object.keys(files).length);){assert.ok(Date.now()<until,'the parts are asked for once the page is drawn');await new Promise(r=>setTimeout(r,50))}
  assert.equal(await p.evaluate(()=>typeof helpOpen+typeof openGame+typeof pjOpen),'undefinedundefinedundefined');
  const graphRules=()=>p.evaluate(()=>[document.querySelector('style[data-lazy-css="graph-pages.css"]').textContent.includes('.graph-list{'),getComputedStyle(document.body.appendChild(Object.assign(document.createElement('div'),{className:'graph-list'}))).display]);
  assert.deepEqual(await graphRules(),[false,'block']);
  await p.locator('#suggestions .all-clear .poke').click();
  assert.ok((await p.locator('#suggestions .poke-line').innerText()).length>0);
  // Calendar, Learning and Help opened while their parts are on their way: they open once the parts are in
  await p.evaluate(()=>showTab('calendar'));assert.equal(await p.locator('#calendar-view').innerHTML(),'');
  await p.evaluate(()=>showTab('feedback'));assert.equal(await p.locator('#learn-tabs').innerHTML(),'');
  await p.evaluate(()=>showTab('people'));assert.equal(await p.locator('#people-view').innerHTML(),'');
  await p.evaluate(()=>showTab('health'));assert.equal(await p.locator('#health-tabs').innerHTML(),'');assert.equal(await p.locator('#connectors').innerHTML(),'');
  // The Fleet's data in, its tab's views wait for their part
  await p.evaluate(()=>{fleetData={on:false,fleets:[]};fleetShown=fleetView(false,true)});assert.equal(await p.locator('#fleet-view').innerHTML(),'');
  await p.evaluate(()=>showTab('calendar'));await p.evaluate(()=>document.querySelector('#open-help').click());
  release();hold=null;holdOnly=null;
  // #help-panel is made by Help's part: until it's in, there's none (the check waits, it doesn't throw). Settings has a
  // block of its own below: opened here too, whichever part came last would decide what shows.
  await p.waitForFunction(()=>document.querySelector('#calendar-view').children.length>0&&document.querySelector('#learn-tabs').children.length>0&&document.querySelector('#help-panel')?.open&&document.querySelector('#people-view').innerHTML!==''&&document.querySelector('#fleet-view').textContent.includes('not in a Fleet')&&document.querySelector('#health-tabs').children.length>0&&document.querySelector('#connectors').children.length>0);
  assert.deepEqual(await graphRules(),[true,'grid']);
  await p.evaluate(()=>{document.querySelector('#help-panel').close();showTab('inbox')});
  // In: Help opens, and the fourth poke's game plays
  assert.deepEqual(asked.sort(),Object.keys(files).sort(),'each part is asked for once');
  await p.evaluate(()=>document.querySelector('#open-help').click());await p.locator('#help-panel[open]').waitFor();
  await p.evaluate(()=>document.querySelector('#help-panel').close());
  for(let i=0;i<3;i++)await p.locator('#suggestions .all-clear .poke').click();
  await p.locator('#suggestions .all-clear .play').click();await p.locator('#game-dialog[open]').waitFor();
  await context.close();
 }
 // A link straight to Calendar, its part held back: Calendar opens once the part is in
 {let release;hold=new Promise(r=>release=r);holdOnly='lazy-calendar-';asked.length=0;const context=await browser.newContext({viewport:{width:390,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const p=await context.newPage();p.on('pageerror',e=>errors.push('link: '+e.message+' '+e.stack));
  await p.goto(base+'#calendar',{waitUntil:'domcontentloaded'});
  for(const until=Date.now()+20000;!asked.some(n=>n.startsWith('lazy-calendar-'));){assert.ok(Date.now()<until,'the calendar part is asked for');await new Promise(r=>setTimeout(r,50))}
  release();hold=null;holdOnly=null;await p.waitForFunction(()=>!document.querySelector('#calendar').hidden&&document.querySelector('#calendar-view').children.length>0);
  await context.close()}
 // Settings opened while its panels are on their way: it opens on Writing once they're in
 {let release;hold=new Promise(r=>release=r);holdOnly='lazy-settings-';asked.length=0;const context=await browser.newContext({viewport:{width:390,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const p=await context.newPage();p.on('pageerror',e=>errors.push('settings: '+e.message+' '+e.stack));
  await p.goto(base,{waitUntil:'load'});await wholeDrawn(p);
  for(const until=Date.now()+20000;!asked.some(n=>n.startsWith('lazy-settings-'));){assert.ok(Date.now()<until,'the settings part is asked for');await new Promise(r=>setTimeout(r,50))}
  await p.evaluate(()=>showSettings('writing'));assert.equal(await p.locator('#settings').isHidden(),true);assert.equal(await p.locator('#voices').innerHTML(),'');
  release();hold=null;holdOnly=null;await p.waitForFunction(()=>!document.querySelector('#settings').hidden&&settingsNow==='writing'&&document.querySelector('#voices').innerHTML!=='');
  await context.close()}
 // A link straight to Settings, Writing, its panels held back: Settings opens on Writing once they're in
 {let release;hold=new Promise(r=>release=r);holdOnly='lazy-settings-';asked.length=0;const context=await browser.newContext({viewport:{width:1440,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const p=await context.newPage();p.on('pageerror',e=>errors.push('settings link: '+e.message+' '+e.stack));
  await p.goto(base+'#settings/writing',{waitUntil:'domcontentloaded'});
  for(const until=Date.now()+20000;!asked.some(n=>n.startsWith('lazy-settings-'));){assert.ok(Date.now()<until,'the settings part is asked for');await new Promise(r=>setTimeout(r,50))}
  assert.equal(await p.locator('#settings').isHidden(),true);
  release();hold=null;holdOnly=null;await p.waitForFunction(()=>!document.querySelector('#settings').hidden&&settingsNow==='writing'&&document.querySelector('#voices').innerHTML!=='');
  await context.close()}
 // A link straight to someone in the Graph, its part held back: the Graph opens on them, and draws them once the part is in
 {let release;hold=new Promise(r=>release=r);asked.length=0;const context=await browser.newContext({viewport:{width:1440,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const p=await context.newPage();p.on('pageerror',e=>errors.push('graph link: '+e.message+' '+e.stack));
  await p.goto(base+'#graph/person%3Aada%40example.com',{waitUntil:'domcontentloaded'});
  for(const until=Date.now()+20000;!asked.some(n=>n.startsWith('lazy-graph-'));){assert.ok(Date.now()<until,'the graph part is asked for');await new Promise(r=>setTimeout(r,50))}
  assert.equal(await p.evaluate(()=>graphLoadedAt),0);
  release();hold=null;holdOnly=null;await p.waitForFunction(()=>!document.querySelector('#people').hidden&&graphNode==='person:ada@example.com'&&graphLoadedAt>0);
  await context.close()}
 // Can't load (offline without a kept copy): the rest is drawn all the same, and the game says so
 {refuse=true;const context=await browser.newContext({viewport:{width:1440,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const p=await context.newPage();p.on('pageerror',e=>errors.push('refused: '+e.message));
  await p.goto(base);await wholeDrawn(p);
  for(let i=0;i<4;i++)await p.locator('#suggestions .all-clear .poke').click();
  await p.locator('#suggestions .all-clear .play').click();
  await p.locator('#toast.show.error',{hasText:'Offline.'}).waitFor();
  assert.equal(await p.locator('#game-dialog[open]').count(),0);
  await p.evaluate(()=>{document.querySelector('#toast').className='';showTab('calendar')});
  await p.locator('#toast.show.error',{hasText:'Offline.'}).waitFor();
  await p.evaluate(()=>{document.querySelector('#toast').className='';showTab('people')});
  await p.locator('#toast.show.error',{hasText:'Offline.'}).waitFor();
  await p.evaluate(()=>{document.querySelector('#toast').className='';document.querySelector('#open-settings').click()});
  await p.locator('#toast.show.error',{hasText:'Offline.'}).waitFor();assert.equal(await p.locator('#settings').isHidden(),true);
  await p.evaluate(()=>{document.querySelector('#toast').className='';showTab('health')});
  await p.locator('#toast.show.error',{hasText:'Offline.'}).waitFor();assert.equal(await p.locator('#health-tabs').innerHTML(),'');
  await p.evaluate(()=>{fleetData={on:false,fleets:[]};return fleetView(false,true)});assert.equal(await p.locator('#fleet-view .error').innerText(),'Offline.');
  await context.close();refuse=false}
 assert.deepEqual(errors,[]);
 console.log('ok lazy parts');
}finally{await browser?.close();server.close()}
