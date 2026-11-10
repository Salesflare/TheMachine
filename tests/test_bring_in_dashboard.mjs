import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Learning, What I've learned, Bring these in (bring_in.py): lines of the owner's OpenClaw notes to tick. Nothing is
// kept without a tick, ticks survive a redraw, a kept one lands under Facts or How to do things with "From MEMORY.md",
// the rest can be dismissed, and with nothing to bring in the page shows no trace of it. All mocked and made up;
// SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const at=d=>`2026-10-${String(d).padStart(2,'0')}T09:00:00+00:00`;
const NOTES=[{id:1,file:'MEMORY.md',kind:'preference',text:'Mira at Lumenfold wants every quote as a PDF, never a link.'},
 {id:2,file:'MEMORY.md',kind:'fact',text:'Tomas from the school board only reads messages after 8 pm.'},
 {id:3,file:'MEMORY.md',kind:'rule',text:'Renewal mails name the seat count and the renewal date in the first line.'},
 {id:4,file:'USER.md',kind:'preference',text:'Northwind Freight is the owner’s oldest customer: their mails go first, also when the week is full and everything else has to wait a day.'}];
const FACTS=[{id:21,kind:'fact',text:'Pat leads partnerships at acme.example and prefers a call over long email threads.',created_at:at(22),merged:0},
 {id:8,kind:'draft',text:'For a listing exchange, ask for their listing link before sending ours.',created_at:at(14),merged:0}];
let notes,facts,posts;
const reset=(n=NOTES,f=FACTS)=>{notes=structuredClone(n);facts=structuredClone(f);posts=[]};
reset();
const status=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],
 facts,voices:[],...(notes.length?{bring_in:notes}:{})});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='bring_in_decide'){const keep=args.keep||[],gone=args.dismiss||[];
   for(const n of notes.filter(n=>keep.includes(n.id)))facts.unshift({id:100+n.id,kind:n.kind==='rule'?'draft':'fact',fact_kind:n.kind==='preference'?'preference':null,text:n.text,created_at:at(27),merged:0,source:'notes:'+n.file});
   notes=notes.filter(n=>!keep.includes(n.id)&&!gone.includes(n.id));res.end(JSON.stringify({saved:keep.length,dismissed:gone.length,bring_in:notes}));return}}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[],shots=process.env.SHOTS;let browser;
const open=async(context)=>{const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/#learning=learned');await navClick(page.locator('[data-tab="feedback"]').first());return page};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  reset();
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await open(context);
  const shot=async name=>{if(shots){await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:`${shots}/${name}-${width}-${scheme}.png`})}};
  const bring=page.locator('#facts [data-group="bring"]');await bring.waitFor();
  assert.equal(await page.locator('#facts .learn-group').first().getAttribute('data-group'),'bring');  // on top
  assert.match(await bring.locator('h3').textContent(),/Bring these in\s*4/);
  assert.match(await bring.locator('.learn-head p').textContent(),/From your OpenClaw notes\. Only what you tick is kept\./);
  assert.equal(await bring.locator('[data-bring]').count(),4);
  assert.match(await bring.locator('.list>div').first().textContent(),/Mira at Lumenfold.*From MEMORY\.md/);
  assert.match(await bring.locator('.list>div').nth(3).textContent(),/From USER\.md/);
  assert.equal(await bring.locator('[data-bring]:checked').count(),0);  // nothing ticked for them
  assert.ok(await bring.locator('[data-bring-keep]').isDisabled());
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
  await shot('1-candidates');
  await bring.locator('label').nth(0).click();await bring.locator('label').nth(2).click();
  assert.ok(await bring.locator('[data-bring-keep]').isEnabled());
  await page.evaluate(()=>refresh());await page.waitForTimeout(300);
  assert.deepEqual(await bring.locator('[data-bring]:checked').evaluateAll(xs=>xs.map(x=>x.dataset.bring)),['1','3']);  // a redraw keeps the ticks
  await shot('2-ticked');
  await bring.locator('[data-bring-keep]').click();
  await page.locator('#learned-101').waitFor();
  assert.deepEqual(posts,[{action:'bring_in_decide',args:{keep:[1,3]}}]);
  assert.equal(await bring.locator('[data-bring]').count(),2);
  assert.equal(await bring.locator('[data-bring]:checked').count(),0);
  assert.match(await page.locator('#facts [data-group="facts"] #learned-101').textContent(),/Mira at Lumenfold.*Preference · From MEMORY\.md/);
  assert.match(await page.locator('#facts [data-group="rules"] #learned-103').textContent(),/Renewal mails.*From MEMORY\.md/);
  assert.equal(await page.locator('#learned-101 [data-forget]').count(),1);  // removed like any other
  assert.equal(await page.locator('#learned-21 .fact-meta').count(),0);  // a fact from a note says nothing about notes files
  await shot('3-saved');
  await bring.locator('[data-bring-dismiss]').click();
  await bring.waitFor({state:'detached'});
  assert.deepEqual(posts.at(-1),{action:'bring_in_decide',args:{dismiss:[2,4]}});
  assert.equal(await page.locator('#facts').getByText('Bring these in').count(),0);
  await context.close();
  {// nothing to bring in: no heading, no empty box, no line saying so
   reset([]);const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await open(context);
   await page.locator('#facts [data-group="facts"]').waitFor();
   assert.equal(await page.locator('#facts [data-group="bring"]').count(),0);
   assert.doesNotMatch(await page.locator('#feedback').textContent(),/Bring these in|OpenClaw notes|bring in/i);
   if(shots){await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:`${shots}/4-nothing-to-bring-in-${width}-${scheme}.png`})}
   await context.close();
  }
 }
 {// notes on a Machine that learned nothing yet: What I've learned shows for them alone
  reset(NOTES.slice(0,1),[]);const context=await browser.newContext({viewport:{width:1280,height:800}}),page=await open(context);
  await page.locator('#facts [data-group="bring"]').waitFor();
  assert.equal(await page.locator('#facts .learn-group').count(),1);
  assert.doesNotMatch(await page.locator('#facts').textContent(),/Nothing yet/);
  await page.locator('#facts [data-bring-dismiss]').click();  // nothing ticked: the rest is all of them
  await page.locator('#facts [data-group="bring"]').waitFor({state:'detached'});
  assert.deepEqual(posts.at(-1),{action:'bring_in_decide',args:{dismiss:[1]}});
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('bring in dashboard ok');
}finally{await browser?.close();server.close()}
