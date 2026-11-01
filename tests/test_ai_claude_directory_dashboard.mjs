import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, AIs: once the official app is ready (reach.shared), Add in Claude comes first, a link to The Machine's
// listing in Claude's connector directory (one click, nothing to paste) in a new tab, above the shared address with
// Copy. The Claude steps start from it; the custom connector stays as the other way. Not ready yet: no Add in Claude,
// Get your address instead. SHOTS=<folder> saves screenshots.
const DIRECTORY='https://claude.ai/directory/connectors/the-machine',SHARED='https://mcp.themachine.computer/mcp';
const dashboard=await dashboardPage();
let reach={};
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
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
  // Add in Claude comes before the shared address, which keeps its Copy
  const rows=await page.locator('#ai-official>div').allInnerTexts();
  assert.equal(rows.length,2);assert.match(rows[0],/Claude/);assert.match(rows[1],/Official app/);assert.ok(rows[1].includes(SHARED));
  const how=await page.locator('#settings-ai .ai-how').innerText();
  assert.match(how,/Press Add in Claude, then Connect\./);
  assert.match(how,/Add custom connector/);
  assert.ok(!(await page.locator('#settings-ai').innerText()).includes('—'),'no em dashes');
  // Fits: the button inside the screen, no sideways scroll
  const box=await add.boundingBox();assert.ok(box.x>=0&&box.x+box.width<=width,`${width}: Add in Claude inside the screen`);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${width}: no sideways scroll`);
  if(shots){await page.locator('#settings-ai').scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/ai-claude-${width}-${scheme}.png`,fullPage:false});
   await page.locator('#settings-ai').screenshot({path:`${shots}/ai-claude-${width}-${scheme}-section.png`})}
  // Not ready yet (self-hosted, not paired): no Add in Claude, Get your address instead
  reach={hosted:false,paired:false,address:null,shared:null};
  await page.reload();await page.locator('#ai-official [data-ai-get]').waitFor();
  assert.equal(await page.locator('#ai-official [data-ai-claude]').count(),0);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ai claude directory dashboard ok');
