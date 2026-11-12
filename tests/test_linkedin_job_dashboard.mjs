// A new title or company LinkedIn shows (linkedin_connections.py) is a dated line in the person's timeline: "Now Head of
// Sales at Acme, was Sales Lead at Acme", in their language, and the line fits at 390px. Since when they're connected
// shows under their LinkedIn link. Light and dark, English and Dutch. Made-up people, a local fixture server, nothing sent. SHOTS=<folder> saves screenshots.
import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

const dashboard=await dashboardPage();
const nl=await readFile(new URL('../i18n/nl.json',import.meta.url),'utf8'),en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const bo={id:'email:bo@acme.example',kind:'person',name:'Bo Tamsin',strength:2,last_at:day(1),signals:3,ids:['bo@acme.example'],emails:[{value:'bo@acme.example',by:'messages'}],links:[],recent:[],around:[],open:{},side:'work',
 profile:{title:'Head of Sales',company:'Acme',linkedin_url:'https://www.linkedin.com/in/bo-tamsin/',linkedin_since:'2021-03-04',sources:{title:{from:'LinkedIn',at:day(2).slice(0,10),own:true},company:{from:'LinkedIn',at:day(2).slice(0,10),own:true}}},
 changes:[{field:'job',old:{title:'Sales Lead',company:'Acme'},new:{title:'Head of Sales',company:'Acme',via:'LinkedIn'},at:day(2)},
  {field:'job',new:{company:'Acme',via:'LinkedIn'},at:day(40)}]};
let lang='en';
const languages={en:'English',nl:'Nederlands'},errors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/nl.json'){res.end(nl);return}
 if(url.pathname==='/i18n/en.json'){res.end(en);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
  locale:{locale:'en-BE',region:'BE',language:lang,language_set:true,clock:'auto',hour12:false,auto_hour12:false,date_locale:lang==='en'?'en-GB':'nl-BE',languages,saveable:true}}));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');
  if(n){res.end(JSON.stringify({...bo,owners:[]}));return}
  res.end(JSON.stringify({list_counts:{people:1,quiet:0,new:0,work:1,personal:0,orgs:0,warmup:0,projects:0,projects_done:0},counts:{},people:[bo],orgs:[],projects:[],boards:[],owners:[],person_names:[],project_names:[]}));return}
 if(url.pathname==='/api/graph/list'){res.end(JSON.stringify({items:[bo],next:null,total:1}));return}
 res.statusCode=url.pathname.startsWith('/api/')?200:404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,language,scheme] of [[1440,900,'en','light'],[390,844,'en','light'],[1440,900,'en','dark'],[390,844,'en','dark'],[1440,900,'nl','light'],[390,844,'nl','dark']]){
  lang=language;
  const mobile=width<600,context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:language==='nl'?'nl-BE':'en-GB',colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  if(language==='nl')await page.locator('html[lang="nl"]').waitFor({state:'attached'}).catch(()=>{});
  await page.waitForFunction(()=>typeof graphOpen==='function');
  await page.evaluate(()=>{document.querySelector('nav [data-tab="people"]').click();graphOpen('email:bo@acme.example')});
  const lines=page.locator('#people-view .ge-change h4');
  await lines.first().waitFor();
  await page.waitForFunction(want=>document.querySelector('#people-view .ge-change h4')?.textContent===want,
   language==='nl'?'Nu Head of Sales bij Acme, was Sales Lead bij Acme':'Now Head of Sales at Acme, was Sales Lead at Acme');
  assert.deepEqual(await lines.allTextContents(),language==='nl'?['Nu Head of Sales bij Acme, was Sales Lead bij Acme','Nu Acme']:['Now Head of Sales at Acme, was Sales Lead at Acme','Now Acme']);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll at '+width);
  if(shots){await lines.first().scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/job-change-${width}-${language}-${scheme}.png`})}
  const li=page.locator('#people-view .person-contact .kv',{has:page.locator('a[href*="linkedin.com/in/bo-tamsin"]')});
  assert.equal((await li.locator('small').textContent()).toLowerCase(),language==='nl'?'verbonden sinds mrt 2021':'connected since mar 2021');
  if(shots){await li.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/connected-since-${width}-${language}-${scheme}.png`})}
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('linkedin job dashboard ok');
}finally{await browser?.close();server.close()}
