import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add, GBrain: one optional tile, only when the Machine says so (self-hosted, or already on). Not
// installed shows how to install it; installed asks first (what goes in, that GBrain may send it to its own AI
// providers) and "Connect GBrain" stays off until the owner agrees; connected shows the brain, the sync and Turn off.
// Without connect_sources' gbrain (a hosted Machine) there's no tile at all. SHOTS=<folder> saves screenshots.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
let calls=[],tile=true,state;
const OFF={on:false,installed:true,work:false,linked:null,saveable:true,version:'gbrain 0.60.479.0',brain:'/home/owner/.gbrain'};
const ON={...OFF,on:true,linked:'machine',pages:42,kept:2,last_sync:new Date(Date.now()-5*60000).toISOString(),last_error:null};
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);calls.push({action,args});
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:null,paired:true,sources:[{name:'trello',service:'trello',label:'Trello',what:'Your boards.',connected:0,broker:false}],...(tile?{gbrain:{on:!!state.on}}:{})}));return}
  if(action==='gbrain_status'){res.end(JSON.stringify(state));return}
  if(action==='gbrain_on'){if(args.consent!==true){res.statusCode=400;res.end(JSON.stringify({error:'Agree to what goes into GBrain first'}));return}state={...ON,work:args.work===true,pages:0,kept:0,last_sync:null};res.end(JSON.stringify(state));return}
  if(action==='gbrain_work'){state={...state,work:args.on===true};res.end(JSON.stringify(state));return}
  if(action==='gbrain_off'){state={...OFF};res.end(JSON.stringify(state));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const sizes=[[1440,900],[1440,700],[390,844]];
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const [width,height] of sizes){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}x${height}-${scheme}`,pane=page.locator('#connect-add');
  const shot=async name=>{if(shots)await page.screenshot({path:`${shots}/${name}-${tag}.png`})};
  const clean=async()=>{const text=await pane.innerText();assert.ok(!text.includes('—'),'no em dashes');assert.doesNotMatch(text,/\bcard\b/i);
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll')};
  const go=async()=>{await page.goto('about:blank');await page.goto(base+'/#connections=add');await pane.locator('.connect-source').first().waitFor()};

  // a hosted Machine: no tile, nothing asked
  tile=false;state={...OFF};calls=[];await go();
  assert.equal(await pane.locator('[data-gbrain]').count(),0);
  assert.ok(!calls.some(c=>c.action.startsWith('gbrain')),'nothing asked of GBrain when it is not offered');
  tile=true;

  // not installed: how to install it, Check again
  state={...OFF,installed:false,version:undefined,brain:undefined};await go();
  await shot('tile');
  assert.equal(await pane.locator('[data-gbrain] .count').count(),0);
  await pane.locator('[data-gbrain]').click();await pane.locator('[data-gbrain-check]').waitFor();
  assert.match(await pane.innerText(),/bun install -g github:garrytan\/gbrain/);
  await clean();await shot('not-installed');
  state={...OFF};await pane.locator('[data-gbrain-check]').click();await pane.locator('[data-gbrain-consent]').waitFor();

  // consent: what goes in, AI providers, Connect only after agreeing
  const text=await pane.innerText();
  assert.match(text,/Never message text/);assert.match(text,/its own AI providers/);
  assert.equal(await pane.locator('[data-gbrain-on]').isDisabled(),true);
  await clean();await shot('consent');
  await pane.locator('[data-gbrain-work-pick]').check();await pane.locator('[data-gbrain-consent]').check();
  assert.equal(await pane.locator('[data-gbrain-on]').isDisabled(),false);
  await pane.locator('[data-gbrain-on]').click();await pane.locator('[data-gbrain-off]').waitFor();
  assert.deepEqual(calls.find(c=>c.action==='gbrain_on').args,{consent:true,work:true});
  assert.equal(await pane.locator('[data-gbrain-work]').isChecked(),true);

  // connected: brain, version, pages, last sync, Turn off keeps the brain
  state={...ON};await go();
  assert.equal(await pane.locator('[data-gbrain] .count').innerText(),'On');
  await pane.locator('[data-gbrain]').click();await pane.locator('[data-gbrain-off]').waitFor();
  const on=await pane.innerText();
  assert.match(on,/Connected/);assert.match(on,/\/home\/owner\/\.gbrain/);assert.match(on,/42 pages, 2 kept as you edited them/);assert.match(on,/keeps your brain/);
  await clean();await shot('connected');
  await pane.locator('[data-gbrain-work]').check();
  await page.waitForFunction(()=>document.querySelector('[data-gbrain-work]')?.checked);
  await new Promise(r=>setTimeout(r,300));
  assert.deepEqual(calls.filter(c=>c.action==='gbrain_work').at(-1)?.args,{on:true});
  await pane.locator('[data-gbrain-off]').click();await pane.locator('[data-gbrain-consent]').waitFor();
  assert.ok(calls.some(c=>c.action==='gbrain_off'));
  assert.equal(await pane.locator('[data-gbrain-consent]').isChecked(),false,'turning on again asks again');

  // Back returns to the list
  await pane.locator('[data-connect-back]').click();await pane.locator('[data-gbrain]').waitFor();
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok');
}finally{await browser?.close();server.close()}
