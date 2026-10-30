import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Fast for to-do chats (chat_model.py): a checkbox item at the end of a to-do chat's model menu, off by default. On,
// the model button says Fast. A model without a fast option (Claude through a Claude plan here) keeps the item,
// disabled with why, and runs at the standard speed. Help and Settings, Model have no Fast. SHOT_DIR=<folder> saves the
// open menu and the composer at 1440x900 and 390x844.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),id='f4f4f4f4f4f4f4f4';
const cards=[{id,title:'Send the quote for the shop order',body:'The order is ready to quote.',status:'prepared',scope:'personal',created_at:now,event_ids:[1]}];
const models=[{ref:'openai/example-sol',name:'Example Sol',levels:['low','medium','high'],default:'medium',fast:true},
 {ref:'anthropic/example-opus',name:'Example Opus',levels:['low','medium','high'],default:'medium',fast:true},
 {ref:'claude-cli/example-opus',name:'Example Opus (plan)',levels:['low','medium','high'],default:'medium',fast:false}];
let chatModel,own;const posts=[];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},chat_model:chatModel});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'done',active:false,items:[{kind:'you',text:'Can you draft the quote?',at:Date.now()-60000},{kind:'reply',text:'Drafted it.',at:Date.now()-30000}],cursor:null,model:own}));return}
  if(r.action==='chat_fast_set'){posts.push(r);chatModel={...chatModel,fast:r.args.fast};res.end(JSON.stringify(chatModel));return}
  if(r.action==='chat_model_set'){posts.push(r);own={model:r.args.model,thinking:r.args.thinking};res.end(JSON.stringify({model:own}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',SHOTS=process.env.SHOT_DIR;if(SHOTS)await mkdir(SHOTS,{recursive:true});
const errors=[];let browser;
const fastItem=page=>page.evaluate(()=>{const m=document.querySelector('#cm-menu');if(!m||m.hidden)return null;const b=m.querySelector('[data-cm-fast]');if(!b)return 'none';
 const r=b.getBoundingClientRect(),mr=m.getBoundingClientRect();
 return {role:b.getAttribute('role'),checked:b.getAttribute('aria-checked'),disabled:b.getAttribute('aria-disabled'),text:b.querySelector('span').textContent,hint:b.querySelector('small').textContent,
  last:[...m.querySelectorAll('button')].at(-1)===b,inside:r.left>=mr.left&&r.right<=mr.right+1&&r.bottom<=mr.bottom+1,fits:mr.left>=8&&mr.right<=innerWidth-8&&mr.top>=8&&mr.bottom<=innerHeight-8,
  group:b.parentElement.getAttribute('aria-label')}});
const pill=page=>page.evaluate(()=>document.querySelector('#chat-model').innerText.replace(/\s+/g,' ').trim());
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [w,h,phone] of [[1440,900,false],[390,844,true]])for(const scheme of ['dark','light']){
  chatModel={models,known:true,main:{model:'openai/example-sol',thinking:'medium'},default:{model:'openai/example-sol',thinking:'medium'},saved:{},fast:false};own=null;posts.length=0;
  const context=await browser.newContext({viewport:{width:w,height:h},isMobile:phone,hasTouch:phone,deviceScaleFactor:phone?2:1,colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.addInitScript(s=>{try{localStorage.setItem('theme',s)}catch{}},scheme);
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'#chat='+id);await page.locator('#chat-model [data-cm-pick="model"]').waitFor();await page.waitForTimeout(400);
  const tag=`${w}x${h}-${scheme}`,model=page.locator('#chat-model [data-cm-pick="model"]');
  // Off by default: no Fast on the button; the item is last in the model menu, unchecked, with its cost
  assert.equal(await pill(page),'Example Sol Medium thinking');
  await model.click();let f=await fastItem(page);
  assert.deepEqual([f.role,f.checked,f.disabled,f.text,f.hint,f.last,f.group],['menuitemcheckbox','false',null,'Fast','Quicker replies, at a higher cost',true,'Speed']);
  assert.ok(f.inside&&f.fits,'the menu with Fast fits the screen: '+JSON.stringify(f));
  if(SHOTS)await page.screenshot({path:`${SHOTS}/fast-menu-off-${tag}.png`});
  // On, by pointer: saved with chat_fast_set, the button says Fast, the item has its check
  await page.locator('#cm-menu [data-cm-fast]').click();
  await page.waitForFunction(()=>document.querySelector('#chat-model .cm-fast-on'));
  assert.deepEqual(posts.map(p=>[p.action,p.args]),[['chat_fast_set',{fast:true}]]);
  assert.equal(await pill(page),'Example Sol Fast Medium thinking');
  if(SHOTS)await page.screenshot({path:`${SHOTS}/fast-composer-on-${tag}.png`});
  await model.click();assert.equal((await fastItem(page)).checked,'true');
  // By keyboard: End reaches Fast, Enter turns it off again
  await page.keyboard.press('End');assert.equal(await page.evaluate(()=>document.activeElement.hasAttribute('data-cm-fast')),true);
  await page.keyboard.press('Enter');await page.waitForFunction(()=>!document.querySelector('#chat-model .cm-fast-on'));
  assert.deepEqual(posts.at(-1).args,{fast:false});
  // Claude with an API key: Fast too
  await model.click();await page.locator('#cm-menu [data-cm-fast]').click();await page.waitForFunction(()=>document.querySelector('#chat-model .cm-fast-on'));
  await model.click();await page.locator('#cm-menu [data-cm-value="anthropic/example-opus"]').click();
  await page.waitForFunction(()=>document.querySelector('#chat-model [data-cm-pick="model"]').title==='anthropic/example-opus');
  assert.equal(await pill(page),'Example Opus Fast Medium thinking');
  // Claude through a plan: no fast option, the item is disabled with why, a tap does nothing, no Fast on the button
  await model.click();await page.locator('#cm-menu [data-cm-value="claude-cli/example-opus"]').click();
  await page.waitForFunction(()=>document.querySelector('#chat-model [data-cm-pick="model"]').title==='claude-cli/example-opus');
  assert.equal(await page.locator('#chat-model .cm-fast-on').count(),0);
  await model.click();f=await fastItem(page);
  assert.deepEqual([f.checked,f.disabled,f.hint],['false','true','Not offered for this model']);
  if(SHOTS)await page.screenshot({path:`${SHOTS}/fast-menu-unsupported-${tag}.png`});
  const n=posts.length;await page.locator('#cm-menu [data-cm-fast]').click({force:true});await page.waitForTimeout(200);assert.equal(posts.length,n,'a disabled Fast saves nothing');
  await page.keyboard.press('Escape');
  // Settings, Model and Help: no Fast
  await page.goto(base+'#settings/model');await page.locator('#model-chats [data-cm-pick="model"]').waitFor();
  const sm=page.locator('#model-chats [data-cm-pick="model"]');await sm.scrollIntoViewIfNeeded();await sm.click();
  assert.equal(await fastItem(page),'none','no Fast in Settings');await page.keyboard.press('Escape');
  await page.evaluate(()=>{document.querySelector('#settings').hidden=true;helpOpen('ask')});await page.locator('#help-model [data-cm-pick="model"]').waitFor();
  await page.locator('#help-model [data-cm-pick="model"]').click();assert.equal(await fastItem(page),'none','no Fast in Help');
  assert.equal(await page.locator('#help-model .cm-fast-on').count(),0);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('chat fast dashboard ok');
}finally{await browser?.close();server.close()}
