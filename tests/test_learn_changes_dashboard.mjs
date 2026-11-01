import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Learning, Changes (learning_loop.py): what the learning loop changed, why, with Undo; an
// undone one stays, marked. All mocked; SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const t=d=>`2026-10-${String(d).padStart(2,'0')}T09:00:00+00:00`;
let changes,posts;
const reset=()=>{posts=[];changes=[
 {id:3,at:t(25),kind:'voice',channel:'Email',text:'English: Hi + first name\nShort paragraphs\nPlain words, no "kindly"',before:'English: Hi + first name\nShort paragraphs',why:'Two edits took "kindly" out.',undone:false},
 {id:2,at:t(25),kind:'fact',channel:null,text:'Vendor newsletters never need a to-do.',before:'Vendor newsletters can wait a week.',why:'Dismissed three of them this week.',undone:false},
 {id:1,at:t(24),kind:'draft',channel:null,text:'Thank people once, at the end, not in every line.',before:null,why:'A chat correction said so.',undone:true}]};
reset();
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],
  voices:[{channel:'Email',text:changes[0].undone?changes[0].before:changes[0].text,updated_at:t(25)}],
  facts:[{id:9,kind:'fact',text:'Vendor newsletters never need a to-do.',created_at:t(25),merged:0}],learning_changes:changes}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='learning_undo'){changes=changes.map(c=>c.id===args.id?{...c,undone:true}:c);res.end(JSON.stringify({undone:args.id}));return}}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[],shots=process.env.SHOTS;let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  reset();
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#learning=changes');
  await navClick(page.locator('[data-tab="feedback"]').first());
  // its own tab on Learning, between What I've learned and Decisions; What I've learned no longer lists them
  const block=page.locator('#learn-changes');await block.locator('.change-row').first().waitFor();
  assert.deepEqual(await page.locator('#learn-tabs [role="tab"]').allTextContents(),['What I’ve learned','Changes','How it’s going']);
  assert.equal(await page.locator('#learn-tab-changes').getAttribute('aria-selected'),'true');
  assert.equal(await page.locator('#facts [data-group="changes"]').count(),0);
  assert.deepEqual(await block.locator('.change-row strong').allTextContents(),['Email: how you write','Fact changed','Rule added']);
  assert.match(await block.locator('.change-row').first().textContent(),/Two edits took "kindly" out\./);
  assert.equal(await block.locator('[data-learn-undo]').count(),2);  // an undone one has no Undo
  assert.match(await block.locator('.change-row.undone').textContent(),/Undone/);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
  if(shots){await page.evaluate(()=>document.fonts.ready);await page.locator('#learn-pane-changes').screenshot({path:`${shots}/learn-changes-${width}-${scheme}.png`})}
  if(scheme==='light'){
   await block.locator('[data-learn-undo="3"]').click();
   await page.locator('#toast',{hasText:'Undone.'}).waitFor({state:'attached'});
   assert.deepEqual(posts.at(-1),{action:'learning_undo',args:{id:3}});
   await page.locator('#learn-changes [data-learn-undo="3"]').waitFor({state:'detached'});
   assert.equal(await page.locator('#learn-changes .change-row.undone').count(),2);
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('learn changes dashboard ok');
}finally{await browser?.close();server.close()}
