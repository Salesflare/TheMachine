import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdir,readFile} from 'node:fs/promises';
import {join,basename} from 'node:path';
import {fileURLToPath} from 'node:url';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Daily digest (reading_digest.py): a template under Templates; its routine's card shows the topics it picks for
// (More of, Less of), each removable, one field to add; its to-do lists each pick with why it matters, its mail to open,
// More or Less like this (one tap, a second takes it back), and has no Do it.
//   SHOTS=<folder> also saves each step at 390 and 1440, light and dark.
const SHOTS=process.env.SHOTS;if(SHOTS)await mkdir(SHOTS,{recursive:true});
const dashboard=await dashboardPage();
const now=new Date().toISOString(),posts=[];
const TEMPLATES=()=>[{key:'newsletters',name:'Newsletter cleanup',what:'Every morning, one to-do with the past day’s newsletters. Keep or unsubscribe each one.',added:false},
 {key:'digest',name:'Daily digest',what:'Every morning, the few newsletter pieces worth your time, picked for what you care about.',added:false}];
const INTERESTS=()=>({more:[{topic:'Heat pumps',source:'owner'},{topic:'Farm robots',source:'learned'},{topic:'Small business finance',source:'learned'}],less:[{topic:'Crypto',source:'learned'}]});
const routine=()=>({id:'a1'.repeat(16),name:'Daily digest',template:'digest',instructions:'Read my newsletters since the last run and pick the few pieces most worth my time, for what I care about. Put them in one to-do, each with one line on why it matters and a link to the original.',
 rule:{unit:'day',n:1},anchor:'2026-11-09',at:'07:30',state:'on',next_due:'2026-11-13',interests,runs:[{id:'r1',state:'ready',started_at:now,result:'Read 24 newsletters, picked 3.'}]});
const digest=()=>({id:'dg1',title:'Daily digest: 3 worth reading',status:'pending',scope:'personal',created_at:now,event_ids:[1],
 body:'Picked from your newsletters for what you care about.\n\n- Climate Brief: Heat pumps beat gas in cold towns',
 routine:{id:'a1'.repeat(16),name:'Daily digest',live:true,act:null},
 digest:{items:[
  {n:0,from:'Climate Brief',title:'Heat pumps beat gas in cold towns',why:'New field data from towns colder than yours, with running costs.',topic:'Heat pumps',event:11,url:'https://mail.google.com/mail/u/?authuser=owner@example.com#all/m1',feedback:null},
  {n:1,from:'Robot Letters',title:'Small arms for small farms',why:'A gripper for soft fruit now costs under a used tractor.',topic:'Farm robots',event:12,url:'https://mail.google.com/mail/u/?authuser=owner@example.com#all/m2',feedback:null},
  {n:2,from:'Ledger Notes',title:'What lenders ask small firms this winter',why:'Three questions banks now ask before a credit line.',topic:'Small business finance',event:null,url:'https://mail.google.com/mail/u/?authuser=owner@example.com#all/m3',feedback:null}]}});
let templates,cards,interests,list;
const ORIGINALS={11:{kind:'email',event_id:11,from:'Climate Brief <brief@climate.example>',to:'owner@example.com',occurred_at:now,title:'Heat pumps beat gas in cold towns',body:'Field data from twelve towns.'}};
const reset=()=>{templates=TEMPLATES();interests=INTERESTS();cards=[digest()];list=[];posts.length=0};reset();
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const routines=()=>JSON.stringify({routines:list.map(r=>({...r,interests})),suggested:[],trying:[],templates});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/routines'){res.end(routines());return}
 if(url.pathname==='/api/originals'){const o=ORIGINALS[url.searchParams.get('event')];res.end(JSON.stringify({originals:o?[o]:[]}));return}
 if(url.pathname==='/api/email'){res.end(JSON.stringify({html:'<p>Field data from twelve towns.</p>'}));return}
 if(url.pathname.startsWith('/brand/')){try{const f=basename(url.pathname)==='avatar.png'?'app-icon-192.png':basename(url.pathname);res.setHeader('Content-Type',f.endsWith('.png')?'image/png':f.endsWith('.webp')?'image/webp':'application/octet-stream');res.end(await readFile(fileURLToPath(new URL('../brand/'+f,import.meta.url))))}catch{res.statusCode=404;res.end()}return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='routine_template'){templates=templates.map(x=>x.key===b.args.key?{...x,added:true}:x);list=[routine()];res.end(routines());return}
  if(b.action==='digest_interest'){const a=b.args;for(const k of ['more','less'])interests[k]=interests[k].filter(x=>x.topic.toLowerCase()!==String(a.topic).toLowerCase());
   if(!a.remove)interests[a.kind].push({topic:a.topic,source:'owner'});res.end(JSON.stringify({saved:true,interests}));return}
  if(b.action==='digest_feedback'){res.end(JSON.stringify({saved:true,interests}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const text=async l=>(await l.innerText()).replace(/\s+/g,' ').trim();
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440])for(const scheme of SHOTS?['light','dark']:['light']){reset();const mobile=width<500;
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme,...(mobile?{isMobile:true,hasTouch:true}:{})});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const shot=async name=>{if(SHOTS)await page.screenshot({path:join(SHOTS,`${name}-${width}-${scheme}.png`)})};
  await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
  // Templates: Daily digest with Add; added, its card shows the topics
  const tpl=page.locator('#routines-view article.rt-tpl');await tpl.first().waitFor();
  assert.deepEqual(await tpl.locator('h3').allInnerTexts(),['Newsletter cleanup','Daily digest']);
  await tpl.nth(1).scrollIntoViewIfNeeded();await shot('digest-template');
  await tpl.nth(1).locator('[data-rt-tpl="digest"]').click();
  await page.locator('.toast',{hasText:'Routine added'}).waitFor();
  const card=page.locator('#routines-view article[data-rt]').first();await card.locator('.dg-int').waitFor();
  assert.equal(await text(card.locator('.dg-line').first()),'More of Heat pumps × Farm robots × Small business finance ×');
  assert.equal(await text(card.locator('.dg-line').nth(1)),'Less of Crypto ×');
  assert.equal(await card.locator('.dg-chip.learned').count(),3,'learned topics look different from the owner’s own');
  await card.scrollIntoViewIfNeeded();await shot('digest-routine');
  // remove one, add one (Enter adds), to Less of
  await card.locator('[data-dg-drop="Farm robots"]').click();
  await page.waitForFunction(()=>!document.querySelector('[data-dg-drop="Farm robots"]'));
  await card.locator('.dg-add-in').fill('Celebrity news');await card.locator('.dg-add-kind').selectOption('less');await card.locator('.dg-add-in').press('Enter');
  await page.locator('#routines-view [data-dg-drop="Celebrity news"]').waitFor();
  assert.deepEqual(posts.filter(p=>p.action==='digest_interest'),[{action:'digest_interest',topic:'Farm robots',remove:true},{action:'digest_interest',topic:'Celebrity news',kind:'less'}]);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
  // The to-do: a row per pick, why, More or Less like this; no Do it
  await page.goto('http://127.0.0.1:'+server.address().port+'/#todos');
  const todo=page.locator('#task-dg1');await todo.locator('.dg-row').first().waitFor();
  assert.equal(await todo.locator('.dg-row').count(),3);
  assert.equal(await text(todo.locator('.dg-row').first().locator('.dg-why')),'New field data from towns colder than yours, with running costs.');
  assert.equal(await todo.getByRole('button',{name:'Do it',exact:true}).count(),0,'a digest has no Do it');
  assert.equal(await text(todo.locator('.card-badges .chip').first()),'To read','a digest is calm reading, not Needs you');
  assert.equal(await page.locator('#badge-inbox').textContent(),'','a digest is not counted as needing the owner');
  assert.equal(await todo.locator('[data-dg-open]').count(),2,'only a pick with a kept mail opens it');
  assert.equal(await todo.locator('a.dg-out').count(),3,'every pick from a mail links to it');
  assert.equal(await text(todo.locator('button.primary[data-choice="complete"]')),'Done','Done finishes a digest');
  await todo.locator('[data-dg="dg1"][data-dg-n="0"][data-dg-to="more"]').click();
  assert.equal(await todo.locator('[data-dg-n="0"][data-dg-to="more"]').getAttribute('aria-pressed'),'true');
  await todo.locator('[data-dg="dg1"][data-dg-n="1"][data-dg-to="less"]').click();
  await todo.scrollIntoViewIfNeeded();await shot('digest-todo');
  await todo.locator('[data-dg="dg1"][data-dg-n="1"][data-dg-to="less"]').click();  // a second tap takes it back
  assert.equal(await todo.locator('[data-dg-n="1"][data-dg-to="less"]').getAttribute('aria-pressed'),'false');
  assert.deepEqual(posts.filter(p=>p.action==='digest_feedback').map(p=>[p.item,p.feedback]),[[0,'more'],[1,'less'],[1,'']]);
  await todo.locator('[data-dg-open="11"]').click();
  await page.frameLocator('#email-dialog iframe.email-frame').getByText('Field data from twelve towns.').waitFor();
  await page.keyboard.press('Escape');await page.locator('#email-dialog').waitFor({state:'hidden'});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('daily digest dashboard ok');
}finally{await browser?.close();server.close()}
