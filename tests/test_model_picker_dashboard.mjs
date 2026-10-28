import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The model and thinking pickers (chat_model.py) under a to-do chat's message box, in Help and in Settings, Model: each
// is a button that opens the app's own menu, not the browser's list. The chosen item has a check and Ultra's cost is a
// second line. The menu opens up when the trigger is low on the screen and fits a phone. Arrows, Home and End move,
// Enter picks, Escape closes, and the focus goes back to the trigger. A pick saves what it saved before
// (chat_model_set, chat_model_default; Help keeps it for its own chat). SHOT_DIR=<folder> saves the open menus at
// 1440x900 and 390x844, light and dark.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const now=new Date().toISOString(),id='c2c2c2c2c2c2c2c2';
const cards=[{id,title:'Send the quote for the shop order',body:'The order is ready to quote.',status:'prepared',scope:'personal',created_at:now,event_ids:[1]}];
const LEVELS=['low','medium','high','xhigh','max','ultra'];
let chatModel={models:[{ref:'openai/example-sol',name:'Example Sol',levels:LEVELS,default:'low'},{ref:'openai/example-mini',name:'Example mini',levels:['low','medium'],default:'low'}],
 known:true,main:{model:'openai/example-sol',thinking:'low'},default:{model:'openai/example-sol',thinking:'low'},saved:{}};
let own=null;const posts=[];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},chat_model:chatModel});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'done',active:false,items:[{kind:'you',text:'Can you draft the quote?',at:Date.now()-60000},{kind:'reply',text:'Drafted it.',at:Date.now()-30000}],cursor:null,model:own}));return}
  if(r.action==='chat_model_set'){posts.push(r);own={model:r.args.model,thinking:r.args.thinking};res.end(JSON.stringify({model:own}));return}
  if(r.action==='chat_model_default'){posts.push(r);chatModel={...chatModel,default:{model:r.args.model,thinking:r.args.thinking},saved:{model:r.args.model,thinking:r.args.thinking}};res.end(JSON.stringify(chatModel));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',SHOTS=process.env.SHOT_DIR;if(SHOTS)await mkdir(SHOTS,{recursive:true});
const errors=[];let browser;
const menu=page=>page.evaluate(()=>{const m=document.querySelector('#cm-menu');if(!m||m.hidden)return null;const r=m.getBoundingClientRect();
 return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,role:m.getAttribute('role'),items:[...m.querySelectorAll('[role=menuitemradio]')].map(b=>({value:b.dataset.cmValue,checked:b.getAttribute('aria-checked'),text:b.querySelector('span').textContent,hint:b.querySelector('small')?.textContent||''})),
  focused:document.activeElement?.dataset?.cmValue||null}});
const focused=page=>page.evaluate(()=>{const a=document.activeElement;return a?.dataset?.cmPick?a.dataset.cmKind+':'+a.dataset.cmPick:a?.dataset?.cmValue||a?.tagName})
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [w,h,phone] of [[1440,900,false],[390,844,true]])for(const scheme of ['dark','light']){
  own=null;posts.length=0;chatModel={...chatModel,default:{model:'openai/example-sol',thinking:'low'},saved:{}};
  const context=await browser.newContext({viewport:{width:w,height:h},isMobile:phone,hasTouch:phone,deviceScaleFactor:phone?2:1,colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.addInitScript(s=>{try{localStorage.setItem('theme',s)}catch{}},scheme);
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'#chat='+id);await page.locator('#chat-model [data-cm-pick="think"]').waitFor();await page.waitForTimeout(400);
  const tag=`${w}-${scheme}`;
  // No native pickers and no separator dot
  assert.equal(await page.locator('#chat-model select').count(),0,'no native select under the box');
  assert.equal((await page.locator('#chat-model').innerText()).replace(/\s+/g,' ').trim(),'Example Sol Low thinking');
  // The thinking menu, by keyboard: it opens up (the box is at the bottom), on the chosen item, with Ultra's cost on a second line
  const think=page.locator('#chat-model [data-cm-pick="think"]');await think.focus();await page.keyboard.press('Enter');
  let m=await menu(page);assert.ok(m,'Enter opens the menu');assert.equal(m.role,'menu');
  assert.equal(await think.getAttribute('aria-expanded'),'true');
  const tb=await think.boundingBox();assert.ok(m.bottom<=tb.y,`the menu opens up above the trigger: ${JSON.stringify({m,tb})}`);
  assert.ok(m.left>=8&&m.right<=w-8,`the menu fits the screen: ${JSON.stringify(m)}`);
  assert.deepEqual(m.items.map(i=>i.value),LEVELS);assert.equal(m.focused,'low');
  assert.deepEqual(m.items.filter(i=>i.checked==='true').map(i=>i.value),['low']);
  const ultra=m.items.find(i=>i.value==='ultra');assert.equal(ultra.text,'Ultra thinking');assert.equal(ultra.hint,'Slower, uses more of your plan');
  if(SHOTS)await page.screenshot({path:`${SHOTS}/chat-think-${tag}.png`,...(phone?{}:{clip:{x:Math.max(0,tb.x-260),y:Math.max(0,m.top-30),width:720,height:Math.min(h,tb.y+tb.height+40)-Math.max(0,m.top-30)}})});
  await page.keyboard.press('ArrowDown');assert.equal((await menu(page)).focused,'medium');
  await page.keyboard.press('End');assert.equal((await menu(page)).focused,'ultra');
  await page.keyboard.press('ArrowDown');assert.equal((await menu(page)).focused,'low','the arrows wrap around');
  await page.keyboard.press('ArrowUp');await page.keyboard.press('Home');await page.keyboard.press('ArrowDown');await page.keyboard.press('ArrowDown');assert.equal((await menu(page)).focused,'high');
  // Escape closes, the focus is back on the trigger, nothing saved
  await page.keyboard.press('Escape');assert.equal(await menu(page),null);assert.equal(await focused(page),'chat:think');assert.equal(posts.length,0);
  assert.equal(await think.getAttribute('aria-expanded'),'false');
  if(SHOTS&&!phone)await page.screenshot({path:`${SHOTS}/chat-focus-${tag}.png`,clip:{x:Math.max(0,tb.x-260),y:tb.y-80,width:720,height:120}});
  // ArrowDown on the trigger opens it too; Enter picks and saves this chat's own pick
  await page.keyboard.press('ArrowDown');await page.keyboard.press('ArrowDown');await page.keyboard.press('Enter');
  await page.waitForFunction(()=>document.querySelector('#chat-model').textContent.includes('Medium thinking'));
  assert.deepEqual(posts.map(p=>[p.action,p.args]),[['chat_model_set',{suggestion_id:id,model:'openai/example-sol',thinking:'medium'}]]);
  assert.equal(await focused(page),'chat:think','the focus stays on the trigger after a pick');
  // The model menu by pointer: a check on the chosen model; picking the mini keeps the nearest level it has
  await page.locator('#chat-model [data-cm-pick="model"]').click();m=await menu(page);
  assert.deepEqual(m.items.map(i=>[i.text,i.checked]),[['Example Sol','true'],['Example Mini','false']]);
  if(SHOTS)await page.screenshot({path:`${SHOTS}/chat-model-${tag}.png`,...(phone?{}:{clip:{x:Math.max(0,tb.x-260),y:Math.max(0,m.top-30),width:720,height:Math.min(h,tb.y+tb.height+40)-Math.max(0,m.top-30)}})});
  await page.locator('#cm-menu [data-cm-value="openai/example-mini"]').click();
  await page.waitForFunction(()=>document.querySelector('#chat-model').textContent.includes('Example Mini'));
  assert.deepEqual(posts.at(-1).args,{suggestion_id:id,model:'openai/example-mini',thinking:'medium'});
  // A click outside closes without saving
  await page.locator('#chat-model [data-cm-pick="think"]').click();assert.ok(await menu(page));const n=posts.length;
  await page.mouse.click(10,10);assert.equal(await menu(page),null);assert.equal(posts.length,n);
  // Settings, Model: the same menu over the default, saved with chat_model_default
  await page.goto(base+'#settings/model');await page.locator('#model-chats [data-cm-pick="think"]').waitFor();
  assert.equal(await page.locator('#model-chats select').count(),0,'no native select in Settings');
  const st=page.locator('#model-chats [data-cm-pick="think"]');await st.scrollIntoViewIfNeeded();await st.click();m=await menu(page);
  assert.equal(m.focused,'low');const sb=await st.boundingBox();assert.ok(m.left>=8&&m.right<=w-8);
  if(SHOTS)await page.screenshot({path:`${SHOTS}/settings-think-${tag}.png`});
  await page.locator('#cm-menu [data-cm-value="high"]').click();
  await page.waitForFunction(()=>document.querySelector('#model-chats [data-cm-pick="think"]').textContent.includes('High thinking'));
  assert.deepEqual(posts.at(-1),{action:'chat_model_default',args:{model:'openai/example-sol',thinking:'high'}});
  // Help: inside its dialog, the menu opens in the dialog, Escape closes the menu and not Help
  await page.evaluate(()=>{document.querySelector('#settings').hidden=true;helpOpen('ask')});await page.locator('#help-model [data-cm-pick="think"]').waitFor();
  const ht=page.locator('#help-model [data-cm-pick="think"]');await ht.focus();await page.keyboard.press('Enter');m=await menu(page);assert.ok(m);
  assert.ok(await page.evaluate(()=>document.querySelector('#cm-menu').matches(':popover-open')),'the menu is a popover, above the Help dialog');
  {const r=await page.evaluate(()=>{const m=document.querySelector('#cm-menu').getBoundingClientRect(),x=m.left+m.width/2,y=m.top+8;return document.elementFromPoint(x,y)?.closest('#cm-menu')?true:false});assert.ok(r,'the top of the menu is not cut off by the dialog')}
  if(SHOTS)await page.screenshot({path:`${SHOTS}/help-think-${tag}.png`});
  await page.keyboard.press('Escape');assert.equal(await menu(page),null);assert.ok(await page.evaluate(()=>document.querySelector('#help-panel').open),'Escape closes only the menu');
  assert.equal(await focused(page),'help:think');
  const before=posts.length;await page.keyboard.press('ArrowDown');await page.keyboard.press('End');await page.keyboard.press('Enter');
  await page.waitForFunction(()=>document.querySelector('#help-model').textContent.includes('Ultra thinking'));
  assert.equal(posts.length,before,'Help keeps its pick for its own chat');assert.deepEqual(await page.evaluate(()=>helpModel),{model:'openai/example-sol',thinking:'ultra'});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('model picker dashboard ok');
}finally{await browser?.close();server.close()}
