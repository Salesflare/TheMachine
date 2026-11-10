import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A repeating to-do keeps its own way of doing it (recurring.py, method): its chat shows one quiet centered line
// "Saved how to do this next time · Edit · Undo" under the reply. Edit opens the words in place (no other screen) and
// Save keeps them (recurring_method_edit); Cancel leaves them. Undo (recurring_method_undo) marks the line Undone, with
// no buttons. All mocked; RECIPE_CHAT_SHOTS=dir saves phone and desktop screenshots, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),t0=Date.now()-60000;
const card={id:'e2e2e2e2e2e2e2e2',title:'Make the monthly report',body:'The report and the email are ready for you to check.',status:'prepared',scope:'work',created_at:now,event_ids:[1],
 repeats:{series:'s1',rule:{unit:'month',n:1},anchor:'2026-11-02',due:'2026-11-02',missed:0,next:'2026-12-02'}};
const way='1. Take last month’s sheet from the shared folder and fill in the period before the due date.\n2. Keep the file names as the source has them.\n3. Draft one email to the client with both files; you send it.';
let text,undone;const posts=[];
const reset=()=>{text=way;undone=false;posts.length=0};
const items=()=>[
 {kind:'you',text:'Keep the file names as they are, and the period is the month before the due date',at:t0},
 {kind:'reply',text:'Done: the files keep their names and cover last month. The email waits for your Send.',at:t0+2000},
 undone?{kind:'recipe',state:'undone',at:t0+2000}:{kind:'recipe',state:'saved',text,at:t0+2000}];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],
  fleet:{on:false,fleets:[]},facts:[],moved:[]}));return}
 if(url.pathname==='/api/action'){const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='card_chat'){res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k'+posts.length,items:items()}));return}
  if(action==='recurring_method_edit'){text=args.text;undone=false;res.end(JSON.stringify({id:args.suggestion_id,method:{kind:'recipe',state:'saved',text}}));return}
  if(action==='recurring_method_undo'){undone=true;res.end(JSON.stringify({id:args.suggestion_id,method:{kind:'recipe',state:'undone'}}));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;const shots=process.env.RECIPE_CHAT_SHOTS;
const flat=s=>s.replace(/\s*·\s*/g,' · ').replace(/\s+/g,' ').trim();
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  reset();
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/#chat=${card.id}`);
  const log=page.locator('#chat-log'),line=log.locator('.chat-recipe');await line.waitFor();
  // One quiet line under the reply it came from, centered, with Edit and Undo
  const order=await log.locator('.chat-msg,.chat-event,.chat-work').evaluateAll(es=>es.map(e=>e.className));
  const reply=order.findIndex(c=>/chat-msg machine/.test(c)&&!/chat-card/.test(c)),at=order.findIndex(c=>/chat-recipe/.test(c));
  assert.ok(reply>=0&&at===reply+1,'the line follows the reply: '+order.join(' | '));
  assert.equal(flat(await line.innerText()),'Saved how to do this next time · Edit · Undo');
  const [lb,cb]=await Promise.all([line.boundingBox(),log.boundingBox()]);
  assert.ok(Math.abs((lb.x+lb.width/2)-(cb.x+cb.width/2))<12,'centered');
  assert.ok(await line.evaluate(e=>parseFloat(getComputedStyle(e).fontSize)<15),'quiet, small');
  assert.doesNotMatch(await line.innerText(),/^You\b/);
  if(shots){await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:`${shots}/recipe-line-${width}-${scheme}.png`})}
  // Edit: the words in place, ready to change; Cancel leaves them
  await line.getByRole('button',{name:'Edit how to do this next time'}).click();
  const box=log.locator('#recipe-text');await box.waitFor();
  assert.equal(await box.inputValue(),way);
  assert.equal(await page.evaluate(()=>document.activeElement?.id),'recipe-text');
  assert.ok(await page.evaluate(()=>document.scrollingElement.scrollWidth<=document.scrollingElement.clientWidth),'no horizontal scroll at '+width);
  assert.ok(await log.evaluate(e=>e.scrollWidth<=e.clientWidth),'chat log does not overflow sideways at '+width);
  if(shots)await page.screenshot({path:`${shots}/recipe-edit-${width}-${scheme}.png`});
  if(scheme==='light'){
   await log.getByRole('button',{name:'Cancel'}).click();await line.waitFor();
   assert.equal(posts.filter(p=>p.action==='recurring_method_edit').length,0);
   await line.getByRole('button',{name:'Edit how to do this next time'}).click();await box.waitFor();
   await box.fill(way+'\n4. Put the totals in the email’s first line.');
   await log.getByRole('button',{name:'Save'}).click();
   await page.locator('#toast',{hasText:'Saved. The next one follows it.'}).waitFor({state:'attached'});
   assert.deepEqual(posts.filter(p=>p.action==='recurring_method_edit').at(-1),{action:'recurring_method_edit',args:{suggestion_id:card.id,text:way+'\n4. Put the totals in the email’s first line.'}});
   await line.waitFor();assert.equal(await log.locator('#recipe-text').count(),0);
  }else{
   await log.getByRole('button',{name:'Cancel'}).click();await line.waitFor();
   // Undo: the line says so, with no buttons
   await line.getByRole('button',{name:'Undo: Saved how to do this next time'}).click();
   await log.locator('.chat-learned.gone').waitFor();
   assert.deepEqual(posts.filter(p=>p.action==='recurring_method_undo').at(-1),{action:'recurring_method_undo',args:{suggestion_id:card.id}});
   const gone=log.locator('.chat-learned.gone');
   assert.equal(flat(await gone.innerText()),'Saved how to do this next time · Undone');
   assert.equal(await gone.locator('button').count(),0);
   if(shots)await gone.screenshot({path:`${shots}/recipe-undone-${width}.png`});
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('recipe chat dashboard ok');
}finally{await browser?.close();server.close()}
