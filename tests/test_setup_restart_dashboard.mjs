import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A new owner's setup restarts the app a few times (a source added, reviews turned on). The hosted Machine answers
// meanwhile with JSON {"restarting": true, "setting_up": ...} and Retry-After: 2. The dashboard then says "Setting up…"
// (or "Your Machine is restarting." later on), never the sad "I can't reach the assistant", and is back 2 seconds
// later, not after a back-off of 5 to 30 seconds. A plain 502 (no JSON) is still Offline.
const raw=await dashboardPage(),sw=await readFile(new URL('../sw.js',import.meta.url),'utf8');
const py=await readFile(new URL('../assistant.py',import.meta.url),'utf8');
const BRAND=Object.fromEntries([...py.slice(py.indexOf('BRAND_ASSETS = {'),py.indexOf('}',py.indexOf('BRAND_ASSETS = {'))).matchAll(/'\/brand\/([\w.-]+)': ROOT \/ '([\w./-]+)'/g)].map(m=>[m[1],m[2]]));
const SCOPE='b2'.repeat(16),iso=new Date().toISOString(),shots=process.env.SHOTS||'';
const page=()=>raw.replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__',SCOPE);
const card={id:'1'.repeat(16),title:'Reply to Robin about the plan',body:'Robin asked for the numbers.',status:'pending',scope:'work',created_at:iso,event_ids:[1]};
let mode='setup',live={runs:[]},statusCalls=0;
const status=()=>({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:live,
 connectors:[],fleet:{on:false},ui_version:'v1'});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page());return}
 if(url.pathname==='/sw.js'){res.setHeader('Content-Type','text/javascript');res.end(sw);return}
 if(url.pathname==='/api/status')statusCalls++;
 if(mode!=='ok'&&url.pathname.startsWith('/api/')){
  if(mode==='down'){res.statusCode=502;res.setHeader('Content-Type','text/plain');res.end('');return}
  res.statusCode=502;res.setHeader('Retry-After','2');res.end(JSON.stringify({error:'The Machine is restarting',restarting:true,setting_up:mode==='setup'}));return}
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:SCOPE}));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){res.end('{"ok":true,"counted":0}');return}
 const brand=url.pathname.startsWith('/brand/')&&BRAND[url.pathname.slice(7)];
 if(brand){res.setHeader('Content-Type',brand.endsWith('.webp')?'image/webp':'image/png');res.end(await readFile(new URL('../'+brand,import.meta.url)));return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const until=async(p,fn,arg,label,timeout=15000)=>{try{await p.waitForFunction(fn,arg,{timeout})}catch{throw Error('timed out: '+label)}};
const bar=p=>p.evaluate(()=>{const b=document.querySelector('#offline-bar');return b.hidden||!b.offsetParent?'':b.innerText.replace(/\s+/g,' ').trim()});
const empty=p=>p.evaluate(()=>document.querySelector('#suggestions .empty')?.textContent.trim()||'');
const shoot=async(p,name)=>{if(!shots)return;for(const [w,h] of [[1440,900],[1440,700],[390,844]]){await p.setViewportSize({width:w,height:h});await p.waitForTimeout(800);await p.screenshot({path:`${shots}/${name}-${w}x${h}.png`})}await p.setViewportSize({width:1440,height:900})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},serviceWorkers:'block'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const tab=await context.newPage();tab.on('pageerror',e=>errors.push(e.message));

 // 1. The very first load lands in a setup restart: "Setting up…", not the sad Offline page
 await tab.goto(base);
 await until(tab,()=>/Back in a moment/.test(document.querySelector('#suggestions')?.textContent||''),null,'the empty state says back in a moment');
 assert.equal(await empty(tab),'Back in a moment.');
 assert.match(await bar(tab),/^Setting up…/);
 assert.doesNotMatch(await tab.evaluate(()=>document.querySelector('#suggestions').textContent+document.querySelector('#offline-bar').textContent+document.querySelector('#updated').textContent),/can’t reach|every 30 seconds|Offline/);
 await shoot(tab,'first-load-setting-up');

 // 2. Back 2 seconds later (Retry-After), not after 5 to 30
 const calls=statusCalls;await tab.waitForTimeout(2600);
 assert.ok(statusCalls>calls,'tried again within Retry-After');
 mode='ok';const back=Date.now();
 await tab.locator('#suggestions article[id]').first().waitFor({timeout:4000});
 assert.ok(Date.now()-back<3500,'back within a couple of seconds');
 assert.equal(await bar(tab),'','no banner once it answers');

 // 3. A restart later in setup (an AI connecting): the page knows, the Machine doesn't say: still "Setting up…"
 live={runs:[],ai_connecting:{name:'ChatGPT',since:iso}};await tab.evaluate(()=>refresh());
 mode='restart';await tab.evaluate(()=>refresh());
 await until(tab,()=>!document.querySelector('#offline-bar').hidden,null,'the banner');
 assert.match(await bar(tab),/^Setting up…/);
 assert.ok(await tab.locator('#suggestions article[id]').count(),'the to-dos stay');
 await shoot(tab,'restart-during-setup');

 // 4. A restart once setup is over: says the Machine is restarting
 mode='ok';live={runs:[]};await tab.evaluate(()=>refresh());await until(tab,()=>document.querySelector('#offline-bar').hidden,null,'banner gone');
 mode='restart';await tab.evaluate(()=>refresh());
 await until(tab,()=>!document.querySelector('#offline-bar').hidden,null,'the banner');
 assert.match(await bar(tab),/^Your Machine is restarting\./);

 // 5. A plain 502 (no JSON: the Machine away) is still Offline
 mode='down';await tab.evaluate(()=>refresh());
 await until(tab,()=>/^Offline/.test(document.querySelector('#offline-bar').innerText),null,'Offline');
 assert.deepEqual(errors,[]);
 console.log('setup restart dashboard: ok');
}finally{await browser?.close();server.close()}
