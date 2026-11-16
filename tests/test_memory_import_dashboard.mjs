import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Import from another AI (learning-import.js, memory_import.py): a row on the setup to-do and on Learning opens one
// dialog; Copy prompt, paste, Review; the review ticks new lines, lets each be edited, shows a fact that disagrees
// next to the current one (the current one picked until the owner picks the new), says what was left out, and Import
// sends only what was picked. A kept line says where it came from on Learning. All mocked and made up; SHOTS=dir saves
// screenshots.
const dashboard=await dashboardPage();
const PROMPT='I’m moving to a new assistant. List what you know about me.\n\n## About me\n## Preferences\n\nReply with one code block and nothing else.';
const ANSWER='```\n## About me\n- Lives in Ghent.\n- Has a dog called Pixel.\n## Preferences\n- Prefers tea over coffee.\n```';
const REVIEW={from:'chatgpt',token:'t0k3n',known:1,secrets:2,permissions:1,more:false,judged:true,items:[
 {n:1,text:'Has a dog called Pixel.',area:'about',kind:'fact'},
 {n:2,text:'Runs sales at Lumenfold, a small software company.',area:'work',kind:'fact'},
 {n:3,text:'Prefers tea over coffee, without sugar.',area:'preferences',kind:'preference',conflict:{id:7,text:'Drinks coffee black every morning.'}},
 {n:4,text:'Runs on Tuesday and Thursday mornings.',area:'routines',kind:'fact'}]};
const now=new Date().toISOString();
let facts,posts,memory,live=null,todos=true;
const reset=()=>{live=null;todos=true;facts=[{id:7,kind:'fact',text:'Drinks coffee black every morning.',created_at:now,merged:0}];posts=[];memory=false};
reset();
const status=()=>({suggestions:todos?[{id:'ab'.repeat(8),title:'Reply to Robin about the garden plan',body:'Robin asked for the dates.',status:'pending',scope:'personal',created_at:now,event_ids:[1]}]:[],
 promises:[],suggestion_counts:{pending:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:live||{runs:[]},
 connectors:[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}],facts,voices:[],
 setup_card:{closed:false,dismissed:[],phones:0,whatsapp:false,calendar:true,mail_accounts:1,add:'google',more:true,memory}});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='memory_import_prompt'){res.end(JSON.stringify({prompt:PROMPT,assistants:['chatgpt','claude','gemini']}));return}
  if(action==='memory_import_review'){res.end(JSON.stringify({...REVIEW,from:args.from}));return}
  if(action==='memory_import_save'){let id=50;
   for(const p of args.picks){if(p.replace)facts=facts.filter(f=>f.id!==7);
    facts.unshift({id:++id,kind:'fact',fact_kind:p.kind==='preference'?'preference':'fact',text:p.text,created_at:now,merged:0,source:'import:'+args.from,
     kept_at:p.text===REVIEW.items.find(i=>i.n===p.n).text?null:now})}
   memory=true;res.end(JSON.stringify({saved:args.picks.length,replaced:args.picks.filter(p=>p.replace).length,skipped:0}));return}}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[],shots=process.env.SHOTS;let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  reset();
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,permissions:['clipboard-read','clipboard-write']}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  const shot=async(name,el)=>{if(shots){await page.evaluate(()=>document.fonts.ready);await (el||page).screenshot({path:`${shots}/${name}-${width}-${scheme}.png`})}};
  await page.goto('http://127.0.0.1:'+server.address().port+'/#todos');
  // the setup to-do: one optional row, right after the calendar, closed with its × like any other
  const row=page.locator('#setup-card [data-step="memory"]');await row.waitFor();
  assert.match(await row.textContent(),/Import what another AI knows\s*Import/);
  assert.equal(await row.locator('[data-setup-dismiss="memory"]').count(),1);
  assert.equal(await page.locator('#setup-card .setup-row').first().getAttribute('data-step'),'memory');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
  await shot('1-setup-step');
  // the dialog: pick, copy the prompt, paste, Review
  await row.locator('[data-setup-go="memory"]').click();
  const d=page.locator('#memory-import');await d.locator('.mi-prompt').getByText('moving to a new assistant').waitFor();
  assert.ok(await d.locator('[data-mi-review]').isDisabled());
  await d.locator('.mi-pill').filter({hasText:'Claude'}).click();
  assert.match(await d.locator('.mi-step').first().textContent(),/send it in Claude\./);
  await d.locator('.mi-pill').filter({hasText:'ChatGPT'}).click();
  await d.locator('[data-mi-copy]').click();
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),PROMPT);
  await d.locator('#mi-text').fill(ANSWER);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await shot('2-paste');
  await d.locator('[data-mi-review]').click();
  await d.locator('.mi-list').waitFor();
  assert.deepEqual(posts.find(p=>p.action==='memory_import_review'),{action:'memory_import_review',args:{from:'chatgpt',text:ANSWER}});
  // new lines ticked, the one that disagrees keeps the current fact until the owner picks
  assert.equal(await d.locator('[data-mi-tick]:checked').count(),3);
  const conflict=d.locator('.mi-conflict');
  assert.match(await conflict.textContent(),/These disagree\. Pick one\.\s*Now\s*Drinks coffee black every morning\.\s*From ChatGPT\s*Prefers tea over coffee/);
  assert.equal(await conflict.locator('[value="keep"]').isChecked(),true);
  assert.match(await d.locator('.mi-left').textContent(),/Left out 1 you already told me · 2 looked like passwords or numbers · 1 tried to grant a permission/);
  assert.match(await d.textContent(),/context, never permission/);
  assert.equal(await d.locator('[data-mi-save]').textContent(),'Import 3 lines');
  assert.ok(await page.evaluate(()=>{const b=document.querySelector('#memory-import').getBoundingClientRect();return b.left>=0&&b.right<=innerWidth}),'the dialog fits at '+width);
  await shot('3-review');
  // untick one, edit one, pick the new side of the conflict
  await d.locator('[data-mi-tick="4"]').uncheck();
  await d.locator('[data-mi-edit="2"]').fill('Runs sales at Lumenfold.');
  await conflict.locator('.mi-side').nth(1).click();
  assert.equal(await d.locator('[data-mi-save]').textContent(),'Import 3 lines');
  await shot('4-picked');
  await d.locator('[data-mi-save]').click();
  await d.waitFor({state:'hidden'});
  assert.deepEqual(posts.find(p=>p.action==='memory_import_save').args,{from:'chatgpt',token:'t0k3n',picks:[
   {n:1,text:'Has a dog called Pixel.',kind:'fact'},{n:2,text:'Runs sales at Lumenfold.',kind:'fact'},
   {n:3,text:'Prefers tea over coffee, without sugar.',kind:'preference',replace:true}]});
  await page.locator('#setup-card [data-step="memory"]').waitFor({state:'detached'});  // done: it leaves the to-do
  // Learning: where each came from; an unedited one is context only
  await page.goto('http://127.0.0.1:'+server.address().port+'/#learning=learned');await navClick(page.locator('[data-tab="feedback"]').first());
  const imp=page.locator('#facts>.learn-import');await imp.waitFor();
  assert.match(await imp.textContent(),/Import from another AI\s*ChatGPT, Claude or Gemini\. You pick what stays\.\s*Import/);
  const pixel=page.locator('#facts .fact-row').filter({hasText:'Has a dog called Pixel.'});
  assert.match(await pixel.locator('.fact-meta').textContent(),/^Imported from ChatGPT, \w{3} \d{1,2} · Context only until you edit it$/);
  const sales=page.locator('#facts .fact-row').filter({hasText:'Runs sales at Lumenfold.'});
  assert.match(await sales.locator('.fact-meta').textContent(),/^Imported from ChatGPT, \w{3} \d{1,2}$/);  // edited on the review: their own
  assert.match(await page.locator('#facts .fact-row').filter({hasText:'Prefers tea'}).locator('.fact-meta').textContent(),/^Preference · Imported from ChatGPT/);
  assert.equal(await page.locator('#facts').getByText('Drinks coffee black').count(),0);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await shot('5-learning');
  await imp.locator('[data-memory-import]').click();
  await d.locator('#mi-text').waitFor();
  assert.equal(await d.locator('#mi-text').inputValue(),'');  // a fresh paste after an import
  await d.locator('[data-mi-close]').first().click();await d.waitFor({state:'hidden'});
  await context.close();
 }
 {// while the first look waits (the setup to-do hides then): one quiet, optional button, gone once something is imported
  reset();todos=false;live={runs:[],queue:null,first_look:{state:'waiting',why:'settling',days:7,waiting:30}};
  const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#todos');
  const b=page.locator('#suggestions .first-look-empty .fl-import');await b.waitFor();
  assert.equal(await b.textContent(),'While you wait: import what another AI knows');
  assert.equal(await page.locator('#setup-card .setup-row').count(),0);
  await b.click();await page.locator('#memory-import #mi-text').waitFor();
  await context.close();
 }
 {// a new Machine without facts: What I've learned shows for its Import alone
  reset();facts=[];const context=await browser.newContext({viewport:{width:1280,height:800}}),page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#learning=learned');await navClick(page.locator('[data-tab="feedback"]').first());
  await page.locator('#facts>.learn-import').waitFor();
  assert.match(await page.locator('#facts').textContent(),/Nothing yet/);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('memory import dashboard ok');
}finally{await browser?.close();server.close()}
