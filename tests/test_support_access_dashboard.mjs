import assert from 'node:assert/strict';
import {mkdir, readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, Security, Support access on a self-hosted Machine: shown once it is paired (the app answers support_access),
// the switch goes through the app, and hidden when it isn't paired (the app refuses).
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
let paired=true,until=null;const actions=[];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');let body='';
 req.on('data',c=>body+=c);req.on('end',()=>{
  if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
  res.setHeader('Content-Type','application/json');
  if(url.pathname==='/api/action'){const {action,args}=JSON.parse(body||'{}');actions.push({action,args});
   if(action==='support_access'){
    if(!paired){res.statusCode=400;res.end(JSON.stringify({error:'This Machine isn’t linked to an account.'}));return}
    if(args.allow!==undefined)until=args.allow?new Date(Date.now()+86400000).toISOString():null;
    res.end(JSON.stringify({until,hours:24,accesses:until?[{at:new Date().toISOString(),what:'The Machine team: read the settings'}]:[]}));return}}
  res.end(url.pathname==='/api/events'?'[]':'{}')})});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[1440,700],[390,844]]){
  paired=true;until=null;actions.length=0;
  const phone=width<600,context=await browser.newContext({viewport:{width,height},isMobile:phone,hasTouch:phone}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof showSettings==='function'&&typeof supportAccessLoad==='function');
  await page.evaluate(()=>showSettings('security'));
  await page.waitForSelector('#settings-support:not([hidden])');
  assert.equal(await page.textContent('#sa-state'),'Off');
  assert.equal(await page.textContent('#sa-toggle'),'Allow for 24 hours');
  await page.click('#sa-toggle');await page.waitForFunction(()=>document.querySelector('#sa-toggle').textContent==='Turn off');
  assert.ok((await page.textContent('#sa-state')).startsWith('On until'));
  assert.ok((await page.textContent('#sa-log')).includes('The Machine team: read the settings'));
  assert.deepEqual(actions.map(a=>a.args),[{},{allow:true}],'the switch goes through the app');
  await page.evaluate(()=>document.querySelector('#settings-support').scrollIntoView({block:'center'}));
  if(shots)await page.screenshot({path:`${shots}/self-hosted-support-access-${width}x${height}.png`});
  const box=await page.$eval('#settings-support',el=>{const r=el.getBoundingClientRect();return {right:r.right,scroll:document.documentElement.scrollWidth}});
  assert.ok(box.right<=width&&box.scroll<=width,`${width}: fits ${JSON.stringify(box)}`);
  await page.click('#sa-toggle');await page.waitForFunction(()=>document.querySelector('#sa-toggle').textContent==='Allow for 24 hours');
  assert.equal(actions.at(-1).args.allow,false);
  // Not paired: the app refuses, the section stays hidden
  paired=false;await page.evaluate(()=>supportAccessLoad(true));await page.waitForFunction(()=>document.querySelector('#settings-support').hidden);
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('support access dashboard ok');
