import assert from 'node:assert/strict';
import {mkdir,readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, AIs: once the official app is ready (reach.shared), Add in ChatGPT and Add in Claude come first, links to
// The Machine's listings in ChatGPT's plugins and Claude's connector directory (one click, nothing to paste) in a new
// tab, on a hosted Machine and a paired self-hosted one alike. Folded under Or add it by address: both addresses with Copy
// and the custom MCP server and connector steps. Not ready yet: both muted without a button, one line, Get your address.
// SHOTS=<folder> saves screenshots.
const DIRECTORY='https://claude.ai/directory/the-machine',SHARED='https://mcp.themachine.computer/mcp';
const CHATGPT='https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4';
const dashboard=await dashboardPage();
let reach={};
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){res.setHeader('Content-Type','image/png');res.end(await readFile(new URL('../brand/app-icon-192.png',import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='ai_connections'){res.end(JSON.stringify({connections:[],areas:['work'],reach}));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const [width,height] of [[1280,800],[390,844]]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  reach={hosted:true,paired:false,name:'pat',address:'https://pat.mcp.themachine.computer/mcp',shared:SHARED};
  await page.goto(base+'/#settings/ai');
  const add=page.locator('#ai-official a[data-ai-claude]');
  await add.waitFor();
  assert.equal(await add.innerText(),'Add in Claude');
  assert.equal(await add.getAttribute('href'),DIRECTORY);
  assert.equal(await add.getAttribute('target'),'_blank');
  assert.match(await add.getAttribute('rel'),/noopener/);
  // Add in ChatGPT (The Machine's published ChatGPT app) and Add in Claude, nothing else on top
  const chatgpt=page.locator('#ai-official a[data-ai-chatgpt]');
  assert.equal(await chatgpt.innerText(),'Add in ChatGPT');
  assert.equal(await chatgpt.getAttribute('href'),CHATGPT);
  assert.equal(await chatgpt.getAttribute('target'),'_blank');
  assert.match(await chatgpt.getAttribute('rel'),/noopener/);
  const rows=await page.locator('#ai-official>div').allInnerTexts();
  assert.equal(rows.length,2);assert.match(rows[0],/ChatGPT/);assert.match(rows[1],/Claude/);
  // Or add it by address, folded: the shared address and the private one with Copy, and the steps by hand
  const fold=page.locator('#ai-fold');
  assert.equal(await fold.locator('summary').innerText(),'Or add it by address');
  assert.equal(await fold.getAttribute('open'),null);
  const folded=await fold.textContent();
  for(const want of [SHARED,'https://pat.mcp.themachine.computer/mcp','Add custom MCP server','Add custom connector','Business and Enterprise'])assert.ok(folded.includes(want),want);
  assert.equal(await page.locator('#ai-fold [data-copy-command]').count(),2);
  assert.ok(await page.locator('#ai-private').isHidden(),'hosted: no private section');
  assert.ok(!(await page.locator('#settings-ai').innerText()).includes('—'),'no em dashes');
  // Fits: the buttons inside the screen, no sideways scroll
  for(const [button,name] of [[add,'Add in Claude'],[chatgpt,'Add in ChatGPT']]){const box=await button.boundingBox();assert.ok(box.x>=0&&box.x+box.width<=width,`${width}: ${name} inside the screen`)}
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${width}: no sideways scroll`);
  if(shots){await page.locator('#settings-ai').screenshot({path:`${shots}/ai-hosted-${width}-${scheme}.png`});
   await fold.locator('summary').click();await page.locator('#settings-ai').screenshot({path:`${shots}/ai-hosted-${width}-${scheme}-open.png`})}
  // A paired self-hosted Machine with its address: the same two buttons (the official app reaches it too), Unpair below
  reach={hosted:false,paired:true,name:'pat',address:'https://pat.mcp.themachine.computer/mcp',tls:'ready',shared:SHARED};
  await page.reload();await page.locator('#ai-official [data-ai-chatgpt]').waitFor();
  assert.equal(await page.locator('#ai-official [data-ai-claude]').count(),1);
  assert.equal(await page.locator('#ai-official>div').count(),2);
  assert.ok(await page.locator('#ai-private').isVisible());
  assert.equal(await page.locator('#ai-address [data-ai-unpair]').count(),1);
  assert.equal(await page.locator('#ai-address [data-copy-command]').count(),0);
  if(shots)await page.locator('#settings-ai').screenshot({path:`${shots}/ai-selfhosted-${width}-${scheme}.png`});
  // Not ready yet (self-hosted, not paired): ChatGPT and Claude muted, no buttons, one line; Get your address is the action
  reach={hosted:false,paired:false,address:null,shared:null};
  await page.reload();await page.locator('#ai-official [data-ai-get]').waitFor();
  assert.equal(await page.locator('#ai-official [data-ai-claude], #ai-official [data-ai-chatgpt]').count(),0);
  assert.equal(await page.locator('#ai-official .btn-link, #ai-official button.primary').count(),1);
  const waiting=await page.locator('#ai-official>div').allInnerTexts();
  // one muted row for both, its one line covering both
  assert.match(waiting[0],/ChatGPT · Claude\nReady once this Machine has its address\./);
  assert.equal((await page.locator('#ai-official').innerText()).split('Ready once this Machine has its address.').length,2,'one line');
  assert.match(waiting[1],/Get your address/);
  // Set up: one line, the size of the other row buttons
  const setup=page.locator('#ai-official [data-ai-get]');assert.equal(await setup.innerText(),'Set up');
  const sb=await setup.boundingBox(),lh=await setup.evaluate(b=>parseFloat(getComputedStyle(b).lineHeight)||20);
  assert.ok(sb.height<lh*2,`${width}: Set up on one line (${sb.height}px)`);assert.ok(sb.x+sb.width<=width,`${width}: Set up inside the screen`);
  assert.ok(await page.locator('#ai-private').isHidden());
  if(shots)await page.locator('#settings-ai').screenshot({path:`${shots}/ai-unpaired-${width}-${scheme}.png`});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ai claude directory dashboard ok');
