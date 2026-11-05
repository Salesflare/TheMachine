import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Read photos (whatsapp_images.py) on the dashboard: a to-do from a WhatsApp photo shows it as a thumbnail, its chat
// shows it in the message, a tap opens it large and Escape closes it; only this Machine's own photos (inline data: or
// api/whatsapp-photo) ever reach an <img>. The WhatsApp connection has Read photos, then Also in personal chats, and
// each posts whatsapp_photos with both. A made-up 1x1 PNG; no WhatsApp.
const PNG='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
const now=new Date().toISOString(),ID='wp_0123456789abcdef0123';
const card={id:'c1',title:'Pay the boiler repair by November 14',body:'Robin sent a photo of the invoice.',status:'pending',scope:'personal',created_at:now,event_ids:[7],
 source_line:'Source: WhatsApp from Robin Morgan',photos:[{id:ID,src:PNG,alt:'An invoice from Hollis Heating.'},{id:'../../etc/passwd'},{id:'wp_x',src:'javascript:alert(1)'}]};
const original={kind:'WhatsApp',from:'Robin Morgan',to:'',cc:'',title:'Robin Morgan',occurred_at:now,body:'',event_id:7,chat:'Robin Morgan',photo:{id:ID,alt:'An invoice from Hollis Heating.'}};
let photos={read:false,personal:false,read_count:0,work_connection:false};const posted=[];
const connector=()=>({id:'home-whatsapp',service:'whatsapp',display_name:'WhatsApp',boundary:'personal:me',total:3,signals_24h:1,pending:0,photos});
const dashboard=await dashboardPage();
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[connector()],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/originals'){res.end(JSON.stringify({originals:[original]}));return}
 if(url.pathname==='/api/whatsapp-photo'){res.setHeader('Content-Type','image/png');res.end(Buffer.from(PNG.split(',')[1],'base64'));return}
 if(url.pathname==='/api/action'&&req.method==='POST'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);
  if(action==='whatsapp_photos'){posted.push(args);photos={...photos,read:args.read,personal:args.personal};res.end(JSON.stringify(photos));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]]){
  photos={read:false,personal:false,read_count:0,work_connection:false};posted.length=0;
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',isMobile:width<500,hasTouch:width<500});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.locator('#task-c1').waitFor();
  // The to-do: one thumbnail, its own photo only
  const thumbs=page.locator('#task-c1 button.wa-photo');assert.equal(await thumbs.count(),1);
  assert.equal(await thumbs.locator('img').getAttribute('src'),PNG);
  assert.equal(await thumbs.locator('img').getAttribute('alt'),'An invoice from Hollis Heating.');
  assert.equal(await thumbs.getAttribute('aria-label'),'Open the photo');
  // A tap opens it large, Escape closes it, and the closed view takes no taps
  await thumbs.click();const view=page.locator('#wa-photo-view');await view.waitFor();
  assert.equal(await view.evaluate(d=>d.open),true);assert.equal(await view.locator('img').getAttribute('src'),PNG);
  await page.keyboard.press('Escape');assert.equal(await view.evaluate(d=>d.open),false);
  assert.equal(await view.evaluate(d=>getComputedStyle(d).display),'none');
  // Its chat: the photo in the message (from the Machine, not inline), a tap opens it over the chat
  await page.evaluate(()=>openEmail('c1'));const say=page.locator('#email-content .convo-say button.wa-photo');await say.waitFor();
  assert.equal(await say.locator('img').getAttribute('src'),'api/whatsapp-photo?id='+ID);
  await say.click();assert.equal(await view.evaluate(d=>d.open),true);await page.keyboard.press('Escape');
  assert.equal(await page.locator('#email-dialog').evaluate(d=>d.open),true);
  await page.keyboard.press('Escape');
  // The connection: Read photos off by default; on, then Also in personal chats
  await page.evaluate(()=>{location.hash='#connections'});await page.locator('[data-health-pane="chat"]').first().click().catch(()=>{});
  const read=page.locator('[data-wa-photos="home-whatsapp"][data-field="read"]');await read.waitFor();
  assert.equal(await read.getAttribute('aria-checked'),'false');
  assert.equal(await page.locator('[data-wa-photos][data-field="personal"]').count(),0);
  assert.match(await page.locator('[data-conn="home-whatsapp"] .wa-read').innerText(),/Read photos\s+Reads receipts, screenshots and documents in work chats\./);
  await read.click();await page.waitForFunction(()=>document.querySelector('[data-wa-photos][data-field="personal"]'));
  assert.deepEqual(posted[0],{account:'home-whatsapp',read:true,personal:false});
  await page.locator('[data-wa-photos][data-field="personal"]').click();await page.waitForFunction(()=>/all chats/.test(document.querySelector('[data-conn="home-whatsapp"]').innerText));
  assert.deepEqual(posted[1],{account:'home-whatsapp',read:true,personal:true});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth),'no sideways scroll');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok whatsapp photos dashboard');
}finally{await browser?.close();server.close()}
