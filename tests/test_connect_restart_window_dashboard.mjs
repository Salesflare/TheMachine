import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections, + Add, opened while the Machine restarts (a source connected from the account page restarted it, and the
// page came back during those seconds): the host answers every call with its restart note (502, JSON restarting,
// Retry-After 2). The pane waits quietly ("Loading…", the calm "restarting" bar over the page) and then shows the
// sources as normal, the new one marked connected, never "Can’t reach your Machine". A real outage (a plain 502, no
// restart note) still says so. In Dutch, as the teammate saw it (2026-11-10). SHOTS=<dir> keeps screenshots.
const dashboard=await dashboardPage(),nl=await readFile(new URL('../i18n/nl.json',import.meta.url),'utf8');
const py=await readFile(new URL('../machine/config.py',import.meta.url),'utf8');
const BRAND=Object.fromEntries([...py.slice(py.indexOf('BRAND_ASSETS = {'),py.indexOf('}',py.indexOf('BRAND_ASSETS = {'))).matchAll(/'\/brand\/([\w.-]+)': ROOT \/ '([\w./-]+)'/g)].map(m=>[m[1],m[2]]));
const shots=process.env.SHOTS||'',ago=h=>new Date(Date.now()-h*3600e3).toISOString();
const mail={id:'work-gmail',service:'gmail',email:'owner@acme.example',boundary:'work:Acme',last_success:ago(0.05),total:40,sync_activity:[{at:ago(0.05),status:'success',signals:3}]};
const intercom={id:'work-intercom',service:'intercom',display_name:'Acme support',boundary:'work:Acme',boundary_by:'owner',total:0};
const locale={locale:'nl-BE',region:'BE',language:'nl',clock:'auto',hour12:false,auto_hour12:false,date_locale:'nl-BE',languages:{en:'English',nl:'Nederlands'},saveable:true};
let mode='ok',connectors=[mail],sourceCalls=0;
const sources=()=>({saveable:true,manage_url:'https://app.example/setup',sources:[
 {name:'gmail',label:'Gmail',service:'gmail',group:'mail',what:'Mail',broker:true,connected:1},
 {name:'intercom',label:'Intercom',service:'intercom',group:'customers',what:'Conversations',hosted_signin:true,connected:connectors.includes(intercom)?1:0},
 {name:'rss',label:'RSS',service:'rss',group:'other',what:'Feeds'}]});
const server=createServer(async(req,res)=>{let body='';for await(const b of req)body+=b;const url=new URL(req.url,'http://x.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/nl.json'){res.end(nl);return}
 const file=url.pathname.match(/^\/brand\/logos\/([\w-]+\.(?:svg|png))$/)?.[1]||(url.pathname.startsWith('/brand/')&&BRAND[url.pathname.slice(7)]);  // for the screenshots
 if(file){try{res.setHeader('Content-Type',file.endsWith('.svg')?'image/svg+xml':file.endsWith('.webp')?'image/webp':'image/png');res.end(await readFile(new URL((file.includes('/')?'../':'../dashboard/logos/')+file,import.meta.url)))}catch{res.statusCode=404;res.end()}return}
 if(url.pathname.startsWith('/api/')&&mode==='restart'){res.statusCode=502;res.setHeader('Retry-After','2');res.end(JSON.stringify({error:'The Machine is restarting',restarting:true,setting_up:false}));return}
 if(url.pathname.startsWith('/api/')&&mode==='down'){res.statusCode=502;res.setHeader('Content-Type','text/html');res.end('<html>Bad gateway</html>');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],locale,manage_url:'https://app.example/setup'}));return}
 if(url.pathname==='/api/action'){const {action}=JSON.parse(body||'{}');
  if(action==='connect_sources'){sourceCalls++;res.end(JSON.stringify(sources()));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const errors=[],SAD=/niet bereikbaar|Can’t reach|reach your Machine/;
const pane=p=>p.locator('#connect-add').innerText();
const bar=p=>p.evaluate(()=>{const b=document.querySelector('#offline-bar');return b.hidden||!b.offsetParent?'':b.innerText.replace(/\s+/g,' ').trim()});
async function open(scheme,width){
 const context=await browser.newContext({viewport:{width,height:width<500?844:900},colorScheme:scheme,timezoneId:'Europe/Brussels',locale:'nl-BE'}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);
 await page.waitForFunction(()=>typeof showTab==='function'&&document.documentElement.lang==='nl'&&document.querySelector('#connectors article'));
 await page.evaluate(()=>showTab('health'));
 return {context,page}}
const shoot=async(p,name)=>{if(shots)await p.screenshot({path:`${shots}/${name}.png`})};
try{
 for(const [scheme,width] of [['light',1440],['dark',1440],['light',390],['dark',390]]){
  mode='ok';connectors=[mail];sourceCalls=0;
  const {context,page}=await open(scheme,width);
  // The restart: the account page's connect saved Intercom and the service is away for a few seconds
  mode='restart';
  await page.evaluate(()=>{connectList=null;showHealthPane('customers')});  // Intercom's kind
  await page.waitForFunction(()=>/Laden…/.test(document.querySelector('#connect-add').innerText),null,{timeout:5000});
  await page.waitForFunction(()=>!document.querySelector('#offline-bar').hidden,null,{timeout:6000});
  assert.equal(await bar(page),'Je Machine start opnieuw op.','the calm restart bar, no Try now');
  assert.doesNotMatch(await pane(page),SAD);
  await page.waitForTimeout(2500);  // still away: still waiting, still no error
  assert.doesNotMatch(await pane(page),SAD);
  assert.equal(sourceCalls,0);
  await shoot(page,`during-${width}-${scheme}`);
  // Back, with the new account: the sources as normal, Intercom marked connected, the bar gone
  connectors=[mail,intercom];mode='ok';
  await page.locator('#connect-add .connect-source').first().waitFor({timeout:8000});
  const tile=page.locator('#connect-add [data-connect-signin="intercom"]');
  assert.equal(await tile.locator('.cs-on').count(),1,'Intercom shows as connected');
  assert.doesNotMatch(await pane(page),SAD);
  await page.waitForFunction(()=>document.querySelector('#offline-bar').hidden,null,{timeout:8000});
  await page.waitForTimeout(400);
  await shoot(page,`after-${width}-${scheme}`);
  await context.close()}

 // A real outage (no restart note) is not waited out: the pane says so, as before
 const {context,page}=await open('light',1440);
 mode='down';
 await page.evaluate(()=>{connectList=null;showHealthPane('customers')});  // Intercom's kind
 await page.waitForFunction(()=>/niet bereikbaar/.test(document.querySelector('#connect-add').innerText),null,{timeout:6000});
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser.close();server.close()}
console.log('connect restart window dashboard ok');
