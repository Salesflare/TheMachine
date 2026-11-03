import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A send held for a new message in the thread ("Not sent: new message in the thread."): the to-do shows that message
// (who, when, a few words), Read it opens it, and Redo for this message opens Ask for changes with the ask written.
// Invented fixture data, no network beyond this fake server.
const dashboard=await dashboardPage();
const shots=process.env.SHOTS||'';
const at=new Date(Date.now()-40*60000).toISOString();
const email={kind:'email',label:'Send reply',revision:'e00000000001',account_id:'work',from:'owner@acme.example',to:['robin@client.example'],subject:'Pilot',
 body:'Hi Robin,\n\nSam pointed me to you about the pilot. Could we start next week?\n\nBest,\nAlex',
 state:{status:'blocked',error:'Not sent: new message in the thread.',held_by:{event_id:42,from:'Sam Rivera',mine:false,at,snippet:'Thanks! We start Monday. Could you send the slides first, and copy Robin from the pilot team so they can plan the kickoff call…'}}};
const bare={...email,revision:'e00000000002',state:{status:'blocked',error:'Not sent: new message in the thread.',held_by:{event_id:null,from:'',mine:false,at,snippet:''}}};
const base={status:'prepared',event_ids:[1],scope:'work',created_at:new Date().toISOString(),body:'Drafted a new email to Robin.'};
const cards=[{...base,id:'c1',title:'Write to Robin about the pilot',next_actions:[email]},{...base,id:'c2',title:'Write to Kim about the trial',next_actions:[bare]}];
const state={suggestions:cards,connectors:[],suggestion_counts:{prepared:2},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:false,waiting:0}};
const asked=[];
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify(state));return}
 if(req.url.startsWith('/api/originals')){asked.push(req.url);res.end(JSON.stringify({originals:[]}));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 for(const [width,height] of [[390,844],[1440,900]]){
  const context=await browser.newContext({viewport:{width,height},isMobile:width<600,hasTouch:width<600}),page=await context.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  const card=page.locator('#task-c1');await card.waitFor();
  const held=card.locator('.held-by');await held.waitFor();
  assert.equal(await card.locator('p.note',{hasText:'Not sent'}).innerText(),'Not sent: new message in the thread.');
  assert.match(await held.locator('.held-who').innerText(),/^Sam Rivera · \S/);
  assert.match(await held.locator('.held-snip').innerText(),/^Thanks! We start Monday\./);
  const box=await held.boundingBox(),cardBox=await card.boundingBox();
  assert.ok(box.x>=cardBox.x-1&&box.x+box.width<=cardBox.x+cardBox.width+1,`${width}: inside the to-do`);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${width}: no sideways scroll`);
  const snip=await held.locator('.held-snip').evaluate(n=>({h:n.getBoundingClientRect().height,line:parseFloat(getComputedStyle(n).lineHeight)||18}));
  assert.ok(snip.h<=snip.line*2+2,`${width}: the snippet stays at two lines ${JSON.stringify(snip)}`);
  if(shots){await card.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/held-message-${width}.png`})}
  // Without a collected copy or a name: when it came, no Read it, and the redo still asks plainly
  const bareHeld=page.locator('#task-c2 .held-by');
  assert.equal(await bareHeld.locator('[data-held-read]').count(),0);
  assert.match(await bareHeld.locator('.held-who').innerText(),/^\S/);
  // Read it opens the message in the reader
  await held.locator('[data-held-read]').click();
  await page.locator('#email-dialog[open]').waitFor();
  await page.evaluate(()=>document.querySelector('#email-dialog').close());
  // Redo for this message: Ask for changes, prefilled
  await held.locator('[data-held-redo]').click();
  const box2=page.locator('#feedback-c1');await box2.waitFor();
  assert.equal(await box2.inputValue(),'Redo the draft for the new message from Sam Rivera.');
  if(shots){await page.locator('#task-c1').scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/held-message-redo-${width}.png`})}
  await page.locator('#task-c2 [data-held-redo]').click();
  assert.equal(await page.locator('#feedback-c2').inputValue(),'Redo the draft for the new message.');
  assert.deepEqual(errors,[]);
  await context.close()}
 assert.ok(asked.includes('/api/originals?event=42'),'the reader asked for that message '+asked);
 console.log('held message dashboard: ok');
}finally{await browser.close();server.close()}
