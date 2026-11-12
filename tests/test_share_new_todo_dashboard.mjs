import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Share to The Machine (the phone app's share sheet and "Open with", and the installed web app's share_target): what
// was shared opens New to-do with it, for the owner to check. A PDF alone is enough: Add works without words, and
// card_new carries the file (the Machine reads its text and fills the to-do in). From the installed web app, sw.js
// takes the shared post, keeps it on the device and opens the dashboard at #share=<id>; the page asks for it once.
// Nothing is added before the owner taps Add. All files and words are made up.
// SHOT_DIR=<folder> also saves screenshots; DASHBOARD=<file> runs another dashboard.html (for before shots).
const dashboard=await dashboardPage(process.env.DASHBOARD);
const shotsOnly=!!process.env.DASHBOARD;
const root=new URL('..',import.meta.url);
const sw=await readFile(new URL('sw.js',root),'utf8'),manifest=await readFile(new URL('manifest.webmanifest',root),'utf8');
const now=new Date().toISOString(),NEW='ab'.repeat(8);
const PDF=Buffer.from('%PDF-1.4\n1 0 obj<</Length 60>>stream\nBT (Invoice 4471, made up: EUR 255.00 due 20 Nov) Tj ET\nendstream endobj\n'+'%'.repeat(2000));
let cards,actions,uploaded;
const reset=()=>{cards=[{id:'c1'.repeat(8),title:'Renew the passport',body:'It runs out in May.',status:'pending',scope:'personal',created_at:now,event_ids:[2]}];actions=[];uploaded={}};reset();
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
let posted=0;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/sw.js'){res.setHeader('Content-Type','text/javascript');res.end(sw);return}
 if(url.pathname==='/manifest.webmanifest'){res.setHeader('Content-Type','application/manifest+json');res.end(manifest);return}
 if(url.pathname==='/share-target'){posted++;res.statusCode=303;res.setHeader('Location','./');res.end();return}  // only when sw.js didn't take it
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);if(r.action!=='card_chat')actions.push(r);
  if(r.action==='chat_upload'){const id='cf_'+String(Object.keys(uploaded).length+1).padStart(20,'0');
   uploaded[id]={id,name:r.args.name,type:/\.pdf$/.test(r.args.name)?'application/pdf':'text/plain',size:Buffer.from(r.args.data,'base64').length,data:r.args.data};res.end(JSON.stringify(uploaded[id]));return}
  if(r.action==='card_new'){const files=(r.args.files||[]).map(id=>uploaded[id]);
   cards.unshift({id:NEW,title:r.args.text||files[0]?.name.replace(/\.pdf$/,''),body:'',status:'pending',scope:'work',created_at:now,event_ids:[9],origin:'owner',owner_words:r.args.text,files});
   res.end(JSON.stringify({id:NEW,status:'pending',title:cards[0].title,files}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,tag] of [[1440,900,'desktop'],[1440,700,'short'],[390,844,'phone']]){reset();const phone=width<600;
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',hasTouch:phone,isMobile:phone});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(tag+': '+e.message));
  const shot=async n=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/${n}-${tag}.png`})};
  await page.goto(base);await page.locator('#task-'+'c1'.repeat(8)).waitFor();
  const dialog=page.locator('#new-card');
  // The phone app hands over a PDF with no words (Open with, or Share from a files app)
  await page.evaluate(b64=>machineShare({text:'',files:[new File([Uint8Array.from(atob(b64),c=>c.charCodeAt(0))],'Invoice 4471.pdf',{type:'application/pdf'})]}),PDF.toString('base64'));
  await dialog.waitFor();
  await page.locator('#nc-tray .chat-att:not(.up)').first().waitFor();
  if(shotsOnly){await page.waitForTimeout(200);await shot('before-share-pdf');await context.close();continue}
  assert.equal(await page.locator('#nc-text').inputValue(),'');
  assert.match(await page.locator('#nc-tray').textContent(),/Invoice 4471\.pdf/);
  assert.equal(await page.locator('#nc-add').isDisabled(),false,'a file alone is enough to add it');
  assert.equal(actions.filter(a=>a.action==='card_new').length,0,'nothing is added by itself');
  await page.waitForTimeout(400);const box=await dialog.boundingBox();assert.ok(box.y>=0&&box.y+box.height<=height+1,`the form fits (${box.y}+${box.height} in ${height})`);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'no sideways scroll');
  await page.waitForTimeout(200);await shot('share-pdf');
  // Taking the file back leaves nothing to add
  await page.locator('#nc-tray [data-nc-remove]').click();
  assert.equal(await page.locator('#nc-add').isDisabled(),true);
  await page.locator('#nc-file').setInputFiles([{name:'Invoice 4471.pdf',mimeType:'application/pdf',buffer:PDF}]);
  await page.locator('#nc-tray .chat-att:not(.up)').first().waitFor();
  await page.locator('#nc-add').click();await dialog.waitFor({state:'hidden'});
  const made=actions.find(a=>a.action==='card_new').args;
  assert.equal(made.text,'');assert.equal(made.files.length,1);assert.equal(uploaded[made.files[0]].name,'Invoice 4471.pdf');
  assert.equal(Buffer.from(uploaded[made.files[0]].data,'base64').compare(PDF),0,'the file as it was shared');
  await page.locator('#task-'+NEW).waitFor();
  // The installed web app: Share posts to share-target; sw.js keeps it on the device and opens New to-do with it
  await page.evaluate(async()=>{await navigator.serviceWorker.register('sw.js');await navigator.serviceWorker.ready});
  await page.reload();await page.waitForFunction(()=>!!navigator.serviceWorker.controller);
  await page.locator('#task-'+NEW).waitFor();
  const before=actions.length;
  await page.evaluate(b64=>{const f=document.createElement('form');f.method='POST';f.action='share-target';f.enctype='multipart/form-data';
   const add=(name,value)=>{const i=document.createElement('input');i.name=name;i.value=value;f.append(i)};add('title','Venue quote');add('text','Venue quote https://example.com/quote');
   const i=document.createElement('input');i.type='file';i.name='files';const dt=new DataTransfer();dt.items.add(new File([Uint8Array.from(atob(b64),c=>c.charCodeAt(0))],'Quote.pdf',{type:'application/pdf'}));i.files=dt.files;f.append(i);
   document.body.append(f);f.submit()},PDF.toString('base64'));
  await page.waitForURL(u=>u.pathname==='/'&&!u.hash);
  await dialog.waitFor();
  await page.locator('#nc-tray .chat-att:not(.up)').first().waitFor();
  assert.equal(posted,0,'the worker took the post; nothing reached the Machine but the upload');
  assert.equal(await page.locator('#nc-text').inputValue(),'Venue quote https://example.com/quote');
  const up=actions.slice(before).filter(a=>a.action==='chat_upload');assert.deepEqual(up.map(a=>a.args.name),['Quote.pdf']);
  assert.equal(actions.slice(before).filter(a=>a.action==='card_new').length,0,'nothing is added by itself');
  await page.waitForTimeout(200);await shot('share-target');
  // Handed over once: the same link again opens nothing, and the device keeps nothing of it
  const id=await page.evaluate(()=>caches.open('tm-share').then(c=>c.keys()).then(k=>k.length));assert.equal(id,0);
  await page.keyboard.press('Escape');await dialog.waitFor({state:'hidden'});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('share to new to-do dashboard ok');
