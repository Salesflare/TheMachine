import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A routine's to-do whose chat message holds for the routine's next runs (routine_changes.py) offers Also change the
// routine in its chat too, not only on the card: the same offer (routineChangeBlock, the card's data and actions) right
// under the reply of the run that made it, before the owner's next message. It opens Now / New in place, saves only on
// Change it (routine_change_save), and the chat then says "Changed the routine …" (no "You"). Keep it as is
// (routine_change_keep) drops it. A one-off message (no offer) shows nothing. All mocked;
// ROUTINE_CHANGE_CHAT_SHOTS=dir saves phone and desktop screenshots, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),t0=Date.now()-120000;
const offer={name:'Ship notes on X',old:'Read what was merged today.',new:'Read everything merged since the last post. Lead with what people can do now, not speed tweaks.',at:t0+3000};
const card=(id,more)=>({id,title:'Post on X about what shipped',body:'A post about this week’s changes is ready.',status:'prepared',scope:'work',created_at:now,event_ids:[1],
 source_line:'Source: your routine Ship notes on X',...more});
let cards,saved,posts=[];
const reset=()=>{cards=[card('f1f1f1f1f1f1f1f1',{routine_change:offer}),card('f2f2f2f2f2f2f2f2',{})];saved=false;posts.length=0};
const items=id=>[
 {kind:'you',text:'Did it look at everything since the last post, or only today?',at:t0},
 {kind:'reply',text:'Only today. I redid the post with everything since the last one, and led with what people can do now.',at:t0+5000},
 {kind:'you',text:'Thanks',at:t0+60000},
 {kind:'reply',text:'Glad it helps.',at:t0+62000},
 ...(saved&&id==='f1f1f1f1f1f1f1f1'?[{kind:'event',text:'Changed the routine Ship notes on X',mine:true,at:Date.now()}]:[])];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],
  fleet:{on:false,fleets:[]},facts:[],moved:[]}));return}
 if(url.pathname==='/api/action'){const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='card_chat'){res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k'+posts.length,items:items(args.suggestion_id)}));return}
  if(action.startsWith('routine_change_')){delete cards.find(c=>c.id===args.suggestion_id).routine_change;saved=action==='routine_change_save';
   res.end(JSON.stringify(saved?{saved:true,line:'Changed the routine Ship notes on X'}:{kept:true}));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;const shots=process.env.ROUTINE_CHANGE_CHAT_SHOTS;
const order=log=>log.locator('.chat-msg,.chat-event').evaluateAll(es=>es.map(e=>e.className+'|'+e.textContent.trim().slice(0,30)));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  reset();
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/#chat=f1f1f1f1f1f1f1f1`);
  const log=page.locator('#chat-log'),line=log.locator('.chat-routine-change');await line.waitFor();
  // Under the reply that made it, before the owner's next message; the panel above the chat has no second copy
  const rows=await order(log),at=rows.findIndex(c=>/chat-routine-change/.test(c));
  assert.match(rows[at-1],/chat-msg machine.*\|Only today/,'under its reply: '+rows.join(' / '));
  assert.match(rows[at+1],/chat-msg you.*\|Thanks/,'before the next message: '+rows.join(' / '));
  assert.equal(await page.locator('[data-rt-change]').count(),1);
  const offerButton=line.getByRole('button',{name:'Also change the routine'});
  assert.ok(await offerButton.isVisible());
  assert.doesNotMatch(await line.innerText(),/^You\b/);
  assert.ok(await page.evaluate(()=>document.scrollingElement.scrollWidth<=document.scrollingElement.clientWidth),'no horizontal scroll at '+width);
  if(shots){await page.evaluate(()=>document.fonts.ready);await line.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/routine-change-chat-${width}-${scheme}.png`})}
  // Open: Now / New in place, nothing saved yet, the panel above stays without it
  await offerButton.click();
  const confirm=line.locator('.change-editor');await confirm.waitFor();
  assert.equal((await confirm.locator('p').first().innerText()).trim(),'Change the routine Ship notes on X?');
  assert.equal(await confirm.locator('del').innerText(),offer.old);
  assert.equal(await confirm.locator('ins').innerText(),offer.new);
  assert.equal(await page.evaluate(()=>document.activeElement?.textContent),'Change it');
  assert.equal(await page.locator('.chat-panel [data-rt-change]').count(),0,'one copy: in the thread');
  assert.equal(posts.filter(p=>p.action.startsWith('routine_change_')).length,0);
  assert.ok(await page.evaluate(()=>document.scrollingElement.scrollWidth<=document.scrollingElement.clientWidth),'no horizontal scroll at '+width);
  assert.ok(await log.evaluate(e=>e.scrollWidth<=e.clientWidth),'chat log does not overflow sideways at '+width);
  if(shots){await confirm.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/routine-change-chat-open-${width}-${scheme}.png`})}
  if(scheme==='light'){
   // Change it: saved through the card's action, and the chat says so
   await confirm.getByRole('button',{name:'Change it'}).click();
   await log.locator('.chat-event',{hasText:'Changed the routine Ship notes on X'}).waitFor();
   assert.deepEqual(posts.filter(p=>p.action.startsWith('routine_change_')),[{action:'routine_change_save',args:{suggestion_id:'f1f1f1f1f1f1f1f1'}}]);
   assert.equal(await log.locator('.chat-routine-change').count(),0);
   if(shots)await page.screenshot({path:`${shots}/routine-change-chat-saved-${width}.png`});
  }else{
   await confirm.getByRole('button',{name:'Keep it as is'}).click();
   await page.waitForFunction(()=>!document.querySelector('.chat-routine-change'));
   assert.deepEqual(posts.filter(p=>p.action.startsWith('routine_change_')),[{action:'routine_change_keep',args:{suggestion_id:'f1f1f1f1f1f1f1f1'}}]);
   assert.equal(await log.locator('.chat-event',{hasText:'Changed the routine'}).count(),0);
  }
  // A one-off message: no offer in its chat
  await page.goto(`http://127.0.0.1:${server.address().port}/#chat=f2f2f2f2f2f2f2f2`);
  await log.locator('.chat-msg',{hasText:'Glad it helps.'}).waitFor();
  assert.equal(await page.locator('[data-rt-change]').count(),0);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('routine change chat dashboard ok');
}finally{await browser?.close();server.close()}
