import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {scopeClick} from './nav-click.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The To-dos filter (All, Work, Personal) lives on the Machine (locale_prefs todo_scope), so a phone and a computer show
// the same list: a filter a browser kept from before goes to the Machine once and the browser forgets it, a change on
// another device arrives with the next refresh, and a filter that is on says so at the top of the list ("Personal only
// · Show all", "No personal to-dos · Show all" when it hides everything), in the owner's language. The greeting's counts
// ("1 to decide") read translated too. SHOTS=<folder> saves screenshots at 1440x900 and 390x844, en and nl.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const cats={};for(const l of ['en','nl'])cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const now=new Date().toISOString();
const card=(id,scope,title,status='pending')=>({id:id.repeat(16),status,title,body:'A useful suggestion.',created_at:now,scope,result_files:[],original_urls:[]});
let suggestions,locale,saved;
const view=(language,todo_scope)=>({locale:'en-BE',region:'BE',language,language_set:true,clock:'auto',hour12:false,auto_hour12:false,
 date_locale:language==='en'?'en-GB':language+'-BE',languages:{en:'English',nl:'Nederlands'},todo_scope,saveable:true});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const cat=/^\/i18n\/(\w\w)\.json$/.exec(url.pathname);if(cat){res.end(cats[cat[1]]||'{}');return}
 if(url.pathname==='/api/action'){let body='';req.on('data',c=>body+=c);req.on('end',()=>{const {action,args}=JSON.parse(body);
  if(action!=='set_locale'){res.end('{}');return}saved.push(args);if('todo_scope' in args)locale={...locale,todo_scope:args.todo_scope};res.end(JSON.stringify(locale))});return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
  hours:{days:[1,2,3,4,5],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC',saveable:true},locale}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const shot=async(page,name)=>{if(shots)await page.screenshot({path:`${shots}/${name}.png`})};
const open=async({width=1440,height=900,kept=null}={})=>{const context=await browser.newContext({viewport:{width,height},timezoneId:'UTC',locale:'en-US'}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 if(kept)await context.addInitScript(v=>{if(!sessionStorage.getItem('seeded')){sessionStorage.setItem('seeded','1');localStorage.setItem('scope-filter',v)}},kept);
 page.on('pageerror',e=>errors.push(e.message));await page.goto(base+'/');await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});return [context,page]};
const note=page=>page.locator('#suggestions .scope-note');
const shown=page=>page.locator('#suggestions article[id^="task-"]').count();
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 suggestions=[card('a','work','Reply to the supplier'),card('b','work','Send the quarterly numbers'),card('c','personal','Book the dentist')];
 for(const [lang,width,height] of [['en',1440,900],['nl',1440,900],['en',390,844],['nl',390,844]]){
  // A browser that kept Personal from before, on a Machine without a filter yet: the Machine takes it, once.
  locale=view(lang,null);saved=[];
  let [context,page]=await open({width,height,kept:'personal'});
  await page.waitForFunction(()=>document.querySelector('#suggestions .scope-note'));
  await page.waitForFunction(()=>localStorage.getItem('scope-filter')===null);
  assert.deepEqual(saved,[{todo_scope:'personal'}]);assert.equal(locale.todo_scope,'personal');
  if(lang==='nl')await page.waitForFunction(()=>document.documentElement.lang==='nl');
  assert.equal((await note(page).innerText()).replace(/\s+/g,' ').trim(),lang==='nl'?'Alleen privé · Alles tonen':'Personal only · Show all');
  assert.equal(await shown(page),1);
  await shot(page,`${lang}-${width}x${height}-personal`);
  // Another device switches to Work: the next refresh shows it here too.
  locale={...locale,todo_scope:'work'};await page.evaluate(()=>refresh());
  await note(page).getByText(lang==='nl'?'Alleen werk':'Work only',{exact:true}).waitFor();
  assert.equal(await shown(page),2);
  // Greeting counts read in the owner's language.
  if(width>=1440)assert.equal(await page.locator('#page-head .page-sub').innerText(),lang==='nl'?'2 te beslissen':'2 to decide');
  // Show all: the Machine keeps All, and the line goes.
  await note(page).locator('[data-scope="all"]').click();
  await note(page).waitFor({state:'detached'});
  assert.deepEqual(saved.at(-1),{todo_scope:'all'});assert.equal(await shown(page),3);
  await shot(page,`${lang}-${width}x${height}-all`);
  await context.close();
  // A filter that hides everything says so, instead of All clear.
  locale=view(lang,'personal');saved=[];suggestions[2].status='completed';
  [context,page]=await open({width,height});
  if(lang==='nl')await page.waitForFunction(()=>document.documentElement.lang==='nl');
  await note(page).waitFor();
  assert.equal((await note(page).innerText()).replace(/\s+/g,' ').trim(),lang==='nl'?"Geen privé-to-do's · Alles tonen":'No personal to-dos · Show all');
  assert.equal(await page.locator('#suggestions .all-clear').count(),0);
  assert.deepEqual(saved,[],'a Machine that has a filter is never overwritten by a browser');
  await shot(page,`${lang}-${width}x${height}-personal-empty`);
  await context.close();suggestions[2].status='pending';
 }
 // The sidebar's own filter saves on the Machine as well.
 locale=view('en','all');saved=[];
 {const [context,page]=await open();await scopeClick(page,'Work');await note(page).waitFor();
  assert.deepEqual(saved.at(-1),{todo_scope:'work'});assert.equal(await page.evaluate(()=>localStorage.getItem('scope-filter')),null);await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
