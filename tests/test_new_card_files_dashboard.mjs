import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import zlib from 'node:zlib';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Files on a new to-do (New to-do, chat_files.py): the paperclip (on a phone the file picker, with the camera), a pasted
// screenshot or a drop on the form adds them. Each uploads at once under the form's draft key (chat_upload with draft,
// X-Upload: chat-file) and waits in a tray with a remove button; too big or unknown files say so before anything
// uploads, and a refused upload says why. Adding the to-do sends the draft key and the file ids with card_new; closing
// the form takes the uploads back. The card shows its files, and its chat shows them with the owner's own words.
// SHOT_DIR=<folder> also saves screenshots; DASHBOARD=<file> runs another dashboard.html (for before shots).
const dashboard=await dashboardPage(process.env.DASHBOARD);
const shotsOnly=!!process.env.DASHBOARD;
const now=new Date().toISOString(),NEW='ab'.repeat(8);
const PNG=(()=>{const w=96,h=64,raw=Buffer.alloc((w*3+1)*h);for(let y=0;y<h;y++)for(let x=0;x<w;x++)raw.set([60+x*2,140+y,110-y],y*(w*3+1)+1+x*3);
 const crc=b=>{let c=~0;for(const v of b){c^=v;for(let k=0;k<8;k++)c=c>>>1^(c&1?0xedb88320:0)}return ~c>>>0};
 const chunk=(t,d)=>{const l=Buffer.alloc(4);l.writeUInt32BE(d.length);const td=Buffer.concat([Buffer.from(t),d]),c=Buffer.alloc(4);c.writeUInt32BE(crc(td));return Buffer.concat([l,td,c])};
 const head=Buffer.alloc(13);head.writeUInt32BE(w,0);head.writeUInt32BE(h,4);head.set([8,2,0,0,0],8);
 return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',head),chunk('IDAT',zlib.deflateSync(raw)),chunk('IEND',Buffer.alloc(0))])})();
let cards,actions,uploaded;
const reset=()=>{cards=[{id:'c1'.repeat(8),title:'Renew the passport',body:'It runs out in May.',status:'pending',scope:'personal',created_at:now,event_ids:[2]}];actions=[];uploaded={}};reset();
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/chat-file'){res.setHeader('Content-Type','image/png');res.end(PNG);return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);if(r.action!=='card_chat')actions.push({...r,upload:req.headers['x-upload']||null});
  if(r.action==='chat_upload'){if(r.args.name==='refused.pdf'){res.statusCode=400;res.end(JSON.stringify({error:'I can’t read that type of file. Add an image, a PDF, a text or an Office file.'}));return}
   const id='cf_'+String(Object.keys(uploaded).length+1).padStart(20,'0'),type=/\.pdf$/.test(r.args.name)?'application/pdf':'image/png';
   uploaded[id]={id,name:r.args.name,type,size:Buffer.from(r.args.data,'base64').length};res.end(JSON.stringify(uploaded[id]));return}
  if(r.action==='card_new'){const files=(r.args.files||[]).map(id=>uploaded[id]);
   cards.unshift({id:NEW,title:r.args.text,body:'',status:'pending',scope:'work',created_at:now,event_ids:[9],origin:'owner',owner_words:r.args.text,...(files.length?{files}:{})});
   res.end(JSON.stringify({id:NEW,status:'pending',title:r.args.text,...(files.length?{files}:{})}));return}
  if(r.action==='card_chat'){const c=cards.find(x=>x.id===r.args.suggestion_id);
   res.end(JSON.stringify({session:false,active:false,cursor:null,items:[{kind:'source',from:'You',via:'note',title:c.title,text:c.owner_words||c.body,mine:true,at:Date.now()-60000,...(c.files?{files:c.files}:{})}]}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const ups=()=>actions.filter(a=>a.action==='chat_upload');
const fileOf=(name,mimeType,buffer)=>({name,mimeType,buffer});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,tag] of [[1440,900,'desktop'],[1440,700,'short'],[390,844,'phone']]){reset();const phone=width<600;
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',hasTouch:phone,isMobile:phone});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(tag+': '+e.message));
  const shot=async n=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/${n}-${tag}.png`})};
  await page.goto(base);await page.locator('#task-'+'c1'.repeat(8)).waitFor();
  await page.evaluate(()=>ncOpen());const dialog=page.locator('#new-card');await dialog.waitFor();
  if(shotsOnly){await page.locator('#nc-text').fill('Check the venue quote against the brief');await shot('before-new');await context.close();continue}
  // The paperclip opens the file picker (on a phone: files, photos or the camera); every type the chat takes
  assert.ok(await page.locator('#nc-attach').isVisible());
  assert.equal(await page.locator('#nc-file').getAttribute('accept'),await page.evaluate(()=>CHAT_ACCEPT));
  const chooser=page.waitForEvent('filechooser');await page.locator('#nc-attach').click();
  await (await chooser).setFiles([fileOf('Whiteboard.png','image/png',PNG),fileOf('Quote.pdf','application/pdf',Buffer.from('%PDF-1.4\n'+'x'.repeat(30000)))]);
  await page.locator('#nc-tray .chat-att:not(.up)').nth(1).waitFor();
  const draft=ups()[0].args.draft;assert.match(draft,/^[0-9a-f]{16}$/);
  assert.deepEqual(ups().map(a=>[a.upload,a.args.draft,a.args.suggestion_id,a.args.name]),[['chat-file',draft,undefined,'Whiteboard.png'],['chat-file',draft,undefined,'Quote.pdf']]);
  assert.equal(Buffer.from(ups()[0].args.data,'base64').compare(PNG),0);
  assert.equal(await page.locator('#nc-tray .chat-att.img img').count(),1);
  assert.match(await page.locator('#nc-tray .chat-att:not(.img)').textContent(),/Quote\.pdf\s*29 KB/);
  // Too big or a type it can't read: said at once, in plain words, nothing uploads
  await page.evaluate(()=>{const dt=new DataTransfer();dt.items.add(new File([new Uint8Array(6*1048576)],'huge.png',{type:'image/png'}));
   dt.items.add(new File([new Uint8Array(11*1048576)],'huge.pdf',{type:'application/pdf'}));dt.items.add(new File(['<b>x</b>'],'page.html',{type:'text/html'}));
   const input=document.querySelector('#nc-file');input.files=dt.files;input.dispatchEvent(new Event('change',{bubbles:true}))});
  assert.match(await page.locator('#nc-error').textContent(),/huge\.png is too big \(6\.0 MB\)\. Images can be up to 5\.0 MB\. huge\.pdf is too big \(11\.0 MB\)\. Files can be up to 10\.0 MB\. I can’t read page\.html/);
  assert.equal(ups().length,2);
  // One the Machine refuses: why, and it leaves the tray
  await page.locator('#nc-file').setInputFiles([fileOf('refused.pdf','application/pdf',Buffer.from('%PDF-1.4'))]);
  await page.locator('#nc-error',{hasText:'refused.pdf: I can’t read that type of file'}).waitFor();
  assert.equal(await page.locator('#nc-tray .chat-att').count(),2);
  // A pasted screenshot joins; a drop on the form too, with a hint while dragging
  await page.locator('#nc-text').focus();
  await page.evaluate(b64=>{const dt=new DataTransfer();dt.items.add(new File([Uint8Array.from(atob(b64),c=>c.charCodeAt(0))],'image.png',{type:'image/png'}));
   document.querySelector('#nc-text').dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}))},PNG.toString('base64'));
  await page.locator('#nc-tray .chat-att:not(.up)').nth(2).waitFor();
  assert.equal(ups().at(-1).args.name,'Pasted image.png');
  await page.evaluate(b64=>{const dt=new DataTransfer();dt.items.add(new File([Uint8Array.from(atob(b64),c=>c.charCodeAt(0))],'dropped.png',{type:'image/png'}));
   const at=document.querySelector('#nc-text');at.dispatchEvent(new DragEvent('dragenter',{dataTransfer:dt,bubbles:true,cancelable:true}));
   window.__hint=getComputedStyle(document.querySelector('.nc-drop-hint')).display!=='none';at.dispatchEvent(new DragEvent('drop',{dataTransfer:dt,bubbles:true,cancelable:true}))},PNG.toString('base64'));
  assert.ok(await page.evaluate(()=>window.__hint),'a hint while dragging');
  await page.locator('#nc-tray .chat-att:not(.up)').nth(3).waitFor();
  // A sixth file: up to five
  await page.locator('#nc-file').setInputFiles([fileOf('one.pdf','application/pdf',Buffer.from('%PDF-1.4 1')),fileOf('two.pdf','application/pdf',Buffer.from('%PDF-1.4 2'))]);
  await page.locator('#nc-tray .chat-att:not(.up)').nth(4).waitFor();
  assert.match(await page.locator('#nc-error').textContent(),/A to-do can carry up to 5 files\./);
  assert.equal(await page.locator('#nc-tray .chat-att').count(),5);
  // × takes one back, and tells the Machine (under the same draft key)
  await page.locator('#nc-tray [data-nc-remove]').nth(4).click();
  assert.equal(await page.locator('#nc-tray .chat-att').count(),4);
  const removed=actions.filter(a=>a.action==='chat_file_remove');assert.equal(removed.length,1);assert.equal(removed[0].args.draft,draft);
  // Nothing is saved before it's added; the form fits the screen
  assert.equal(actions.filter(a=>a.action==='card_new').length,0);
  await page.locator('#nc-text').fill('Check the venue quote against the brief');
  const box=await dialog.boundingBox();assert.ok(box.y>=0&&box.y+box.height<=height+1,`the form fits (${box.y}+${box.height} in ${height})`);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'no sideways scroll');
  await shot('new-files');
  // Add: the draft key and the files go with card_new
  await page.locator('#nc-add').click();await dialog.waitFor({state:'hidden'});
  const made=actions.find(a=>a.action==='card_new').args;
  assert.equal(made.draft,draft);assert.deepEqual(made.files,Object.keys(uploaded).slice(0,4),'the four left in the tray, in order');
  assert.equal(actions.filter(a=>a.action==='chat_file_remove').length,1,'the added files are kept');
  // The card shows its files; its chat shows them with the owner's own words
  const card=page.locator('#task-'+NEW);await card.waitFor();
  await card.locator('.card-files a',{hasText:'Quote.pdf'}).waitFor();
  assert.equal(await card.locator('.card-files a').count(),4);
  assert.match(await card.locator('.card-files a',{hasText:'Quote.pdf'}).getAttribute('href'),/^api\/chat-file\?id=cf_/);
  await card.scrollIntoViewIfNeeded();await shot('card-files');
  await page.evaluate(id=>chatGo(id),NEW);
  await page.locator('#chat-log .chat-source.you .chat-you-img').first().waitFor();
  assert.ok(await page.locator('#chat-log .chat-source.you .chat-files a',{hasText:'Quote.pdf'}).isVisible());
  await page.waitForTimeout(300);await shot('chat-files');
  // Closed without adding: its uploads are taken back
  await page.evaluate(()=>ncOpen());await dialog.waitFor();
  await page.locator('#nc-file').setInputFiles([fileOf('Later.pdf','application/pdf',Buffer.from('%PDF-1.4 later'))]);
  await page.locator('#nc-tray .chat-att:not(.up)').first().waitFor();
  await page.keyboard.press('Escape');await dialog.waitFor({state:'hidden'});
  for(let i=0;i<100&&actions.filter(a=>a.action==='chat_file_remove').at(-1).args.id!==Object.keys(uploaded).at(-1);i++)await new Promise(r=>setTimeout(r,50));
  assert.equal(actions.filter(a=>a.action==='chat_file_remove').at(-1).args.id,Object.keys(uploaded).at(-1),'closing takes its upload back');
  await page.evaluate(()=>ncOpen());assert.equal(await page.locator('#nc-tray .chat-att').count(),0,'a new form starts empty');
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('new card files dashboard ok');
