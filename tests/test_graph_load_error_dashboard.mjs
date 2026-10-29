import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A person's page that fails to load (the service answers 500) says so with Try again instead of staying empty, in the
// owner's language; Try again loads it. A quiet refresh that fails keeps the page that is shown. LOAD_ERROR_SHOT=<dir>
// writes screenshots.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const person={id:'person:a',kind:'person',name:'Ada Lovelace',strength:2,last_at:day(1),signals:3,ids:[],links:[],recent:[],around:[],open:{},profile:{title:'Head of procurement'}};
let fail=true,asked=0,lang='en';
const localeView=()=>({locale:'en-BE',region:'BE',language:lang,language_set:true,clock:'auto',hour12:false,auto_hour12:false,date_locale:lang==='en'?'en-US':lang+'-BE',languages:{en:'English',nl:'Nederlands'},saveable:true});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const cat=/^\/i18n\/([a-zA-Z-]+)\.json$/.exec(url.pathname);if(cat){try{res.end(await readFile(new URL(`../i18n/${cat[1]}.json`,import.meta.url)))}catch{res.statusCode=404;res.end('{}')}return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],locale:localeView()}));return}
 if(url.pathname==='/api/graph'){const n=url.searchParams.get('node');if(n){asked++;if(fail){res.statusCode=500;res.end(JSON.stringify({error:'Something went wrong on your Machine. Try again.'}));return}res.end(JSON.stringify(person));return}
  res.end(JSON.stringify({projects:[],people:[],quiet:[],new:[],orgs:[],whos:[],boards:[],person_names:[],project_names:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',shotDir=process.env.LOAD_ERROR_SHOT,errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,language,text,retry] of [[1440,900,'en','Couldn’t load this page.','Try again'],[1440,700,'nl','Deze pagina kon niet laden.','Opnieuw proberen'],[390,844,'en','Couldn’t load this page.','Try again']]){
  fail=true;lang=language;const mobile=width<600,tag=`${width}x${height}-${language}`;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(tag+': '+e.message));
  await page.goto(base+'#graph/person%3Aa');  // straight to a person's page, as a link or the back button opens it
  const box=page.locator('#people-view .graph-load-failed');await box.waitFor();
  // The page can draw before the owner's language has loaded; it then swaps its text in place
  await box.locator('strong',{hasText:text}).waitFor().catch(()=>{});
  assert.equal((await box.locator('strong').textContent()).trim(),text,`the error reads in the owner's language ${tag}`);
  assert.equal((await box.locator('[data-graph-retry]').textContent()).trim(),retry,tag);
  assert.ok(!/restarting/i.test(await page.locator('body').innerText()),`a failed page never says the Machine is restarting ${tag}`);
  if(shotDir)await page.screenshot({path:`${shotDir}/after-error-${tag}.png`});
  fail=false;await box.locator('[data-graph-retry]').click();
  await page.locator('#people-view .person-page').waitFor();assert.equal(await page.locator('#people-view .graph-load-failed').count(),0,tag);
  if(shotDir)await page.screenshot({path:`${shotDir}/after-retry-${tag}.png`});
  // A quiet refresh (after a change elsewhere) that fails keeps the page that is shown
  fail=true;const before=asked;await page.evaluate(()=>people(graphNode,true));
  for(const end=Date.now()+20000;asked===before&&Date.now()<end;)await page.waitForTimeout(50);assert.ok(asked>before,tag);await page.waitForTimeout(200);  // and its failed answer is in
  assert.equal(await page.locator('#people-view .person-page').count(),1,`a failed quiet refresh keeps the page ${tag}`);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('graph load error: a page that fails says so with Try again in the owner\'s language, Try again loads it, a quiet refresh keeps the page');
}finally{await browser?.close();server.close()}
