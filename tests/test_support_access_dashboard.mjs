import assert from 'node:assert/strict';
import {mkdir, readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Support access on a self-hosted Machine: given where it's needed, with the support report in Report a bug (one box,
// ticked by default; unticked gives nothing), through the app and only after Send; Settings, Security shows it only
// while it's on, with each look and Turn off. Not offered when the Machine isn't paired (the app refuses).
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
    res.end(JSON.stringify({until,hours:24,accesses:until?[{at:new Date().toISOString(),what:'The Machine team: read the settings'}]:[]}));return}
   if(action==='bug_preview'){res.end(JSON.stringify({paired:true,parts:[],settings:{}}));return}
   if(action==='bug_send'){res.end(JSON.stringify({sent:true}));return}
   if(action==='bug_queued'){res.end(JSON.stringify({queued:[]}));return}}
  if(url.pathname==='/api/status'){res.end(JSON.stringify(paired?{fleet:{on:false}}:{}));return}
  res.end(url.pathname==='/api/events'?'[]':'{}')})});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[1440,700],[390,844]]){
  paired=true;until=null;actions.length=0;
  const phone=width<600,context=await browser.newContext({viewport:{width,height},isMobile:phone,hasTouch:phone}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof showSettings==='function'&&typeof supportAccessLoad==='function'&&!!state.fleet);
  // Off: nothing in Settings
  await page.evaluate(()=>showSettings('security'));await page.waitForFunction(()=>saData&&!saData.error);
  assert.ok(await page.$eval('#settings-support',el=>el.hidden),'no standing switch while it is off');
  // Report a bug: one box, ticked by default; unticked, sending gives no access
  await page.evaluate(()=>{document.querySelector('#settings').hidden=true;helpOpen('bug')});await page.waitForFunction(()=>/24 hours/.test(document.querySelector('#bug-diag-fine').textContent));
  assert.equal(await page.isChecked('#bug-diag'),true);
  await page.fill('#bug-what','The list is empty');await page.uncheck('#bug-diag');await page.click('#bug-send');await page.waitForSelector('#toast.show');
  assert.equal(actions.filter(a=>a.action==='support_access'&&a.args.allow!==undefined).length,0,'no access unless ticked');
  // Ticked: it turns on only after Send, and the Sent line says until when, quietly
  await page.evaluate(()=>{document.querySelector('#toast').classList.remove('show');helpOpen('bug')});
  await page.fill('#bug-what','Still empty');assert.equal(await page.isChecked('#bug-diag'),true);if(shots)await page.screenshot({path:`${shots}/self-hosted-support-access-ask-${width}x${height}.png`});
  assert.equal(until,null,'nothing before Send');
  await page.click('#bug-send');await page.waitForSelector('#toast .toast-fine');
  assert.deepEqual(actions.filter(a=>a.action==='support_access'&&a.args.allow!==undefined).map(a=>a.args),[{allow:true}],'through the app, after Send');
  assert.ok(actions.findIndex(a=>a.action==='bug_send'&&a.args.diagnostics)<actions.findIndex(a=>a.args?.allow===true));
  assert.match(await page.textContent('#toast .toast-fine'),/^Support can look until /);
  if(shots)await page.screenshot({path:`${shots}/self-hosted-support-access-sent-${width}x${height}.png`});
  // While it's on: no box in Report a bug; Settings shows it with each look and Turn off
  await page.evaluate(()=>helpOpen('bug'));await page.waitForTimeout(150);assert.equal(await page.textContent('#bug-diag-fine'),'Versions, checks and recent errors. No messages, keys or addresses.','already on: the box adds only the report');
  await page.evaluate(()=>{document.querySelector('#help-panel').close();showSettings('security')});
  await page.waitForSelector('#settings-support:not([hidden])');
  assert.equal(await page.textContent('#sa-toggle'),'Turn off');
  assert.ok((await page.textContent('#sa-state')).startsWith('On until'));
  assert.ok((await page.textContent('#sa-log')).includes('The Machine team: read the settings'));
  await page.evaluate(()=>document.querySelector('#settings-support').scrollIntoView({block:'center'}));
  if(shots)await page.screenshot({path:`${shots}/self-hosted-support-access-${width}x${height}.png`});
  const box=await page.$eval('#settings-support',el=>{const r=el.getBoundingClientRect();return {right:r.right,scroll:document.documentElement.scrollWidth}});
  assert.ok(box.right<=width&&box.scroll<=width,`${width}: fits ${JSON.stringify(box)}`);
  await page.click('#sa-toggle');await page.waitForFunction(()=>document.querySelector('#settings-support').hidden);
  assert.equal(actions.at(-1).args.allow,false);
  // On again, then not paired after all: the app refuses, the section hides
  await page.evaluate(()=>supportAccessSet(true));await page.waitForSelector('#settings-support:not([hidden])');
  paired=false;await page.evaluate(()=>supportAccessLoad(true));await page.waitForFunction(()=>document.querySelector('#settings-support').hidden);
  // Not paired: it doesn't ask at all
  const asked=actions.length;await page.evaluate(()=>{state.fleet=undefined;supportAccessLoad(true)});assert.equal(actions.length,asked);assert.ok(await page.$eval('#settings-support',el=>el.hidden));
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('support access dashboard ok');
