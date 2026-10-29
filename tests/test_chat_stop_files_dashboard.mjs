import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import zlib from 'node:zlib';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The card chat's composer: Stop takes the place of Send while a reply runs (chat_stop, then the reply so far stays
// marked Stopped), and files join the next message from Add files, a paste or a drop. Each uploads at once
// (chat_upload, X-Upload: chat-file), shows in a tray with its preview and a remove button, and goes with the message
// (decide files). Too big or unknown files say so before anything uploads. The thread shows the files with the message.
// SHOT_DIR=<folder> also saves screenshots; DASHBOARD=<file> runs another dashboard.html (for before shots).
const dashboard=await dashboardPage(process.env.DASHBOARD);
const shotsOnly=!!process.env.DASHBOARD;
const now=new Date().toISOString(),t0=Date.now()-60000,ID='c1c1c1c1c1c1c1c1';
const cards=[{id:ID,title:'Reply to the venue about the dates',body:'They asked for a date.',status:'instructions',scope:'work',created_at:now,event_ids:[1],preparation_status:'running'},
 {id:'c2c2c2c2c2c2c2c2',title:'Renew the passport',body:'It runs out in May.',status:'pending',scope:'personal',created_at:now,event_ids:[2]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
// A small real photo-like PNG (a color gradient), made here
const PNG=(()=>{const w=96,h=64,raw=Buffer.alloc((w*3+1)*h);for(let y=0;y<h;y++)for(let x=0;x<w;x++)raw.set([60+x*2,140+y,110-y],y*(w*3+1)+1+x*3);
 const crc=b=>{let c=~0;for(const v of b){c^=v;for(let k=0;k<8;k++)c=c>>>1^(c&1?0xedb88320:0)}return ~c>>>0};
 const chunk=(t,d)=>{const l=Buffer.alloc(4);l.writeUInt32BE(d.length);const td=Buffer.concat([Buffer.from(t),d]),c=Buffer.alloc(4);c.writeUInt32BE(crc(td));return Buffer.concat([l,td,c])};
 const head=Buffer.alloc(13);head.writeUInt32BE(w,0);head.writeUInt32BE(h,4);head.set([8,2,0,0,0],8);
 return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',head),chunk('IDAT',zlib.deflateSync(raw)),chunk('IEND',Buffer.alloc(0))])})();
const items=[{kind:'source',from:'Sam Lee',via:'email',title:'Dates',text:'Can we do Tuesday instead of Monday?',mine:false,at:t0-5000},
 {kind:'you',text:'Draft a reply that says Tuesday works',at:t0}];
let running=true,stopped=false,sent=null;const actions=[],uploaded={};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/chat-file'){res.setHeader('Content-Type','image/png');res.end(PNG);return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);actions.push({...r,upload:req.headers['x-upload']||null});
  if(r.action==='card_chat'){const list=[...items];
   if(stopped)list.push({kind:'reply',text:'Here is a reply: Hi Sam, Tuesday…',drafts:[],files:[],stopped:true,at:t0+2000});
   if(sent)list.push({kind:'you',text:sent.text,files:sent.files,at:t0+3000});
   res.end(JSON.stringify({session:true,status:running?'running':'blocked',active:running,cursor:null,items:list,live:running?{text:'Here is a reply: Hi Sam, Tuesday'}:null}));return}
  if(r.action==='chat_stop'){running=false;stopped=true;cards[0].preparation_status='blocked';cards[0].preparation_error='stopped';cards[0].preparation_reason='Stopped. Write what to do next, or tap Try again.';res.end('{"stopped":true}');return}
  if(r.action==='chat_upload'){const id='cf_'+String(Object.keys(uploaded).length+1).padStart(20,'0'),type=/\.pdf$/.test(r.args.name)?'application/pdf':'image/png';
   uploaded[id]={id,name:r.args.name,type,size:Buffer.from(r.args.data,'base64').length};res.end(JSON.stringify(uploaded[id]));return}
  if(r.action==='decide'){sent={text:r.args.feedback,files:(r.args.files||[]).map(id=>uploaded[id])};res.end('{"status":"instructions"}');return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const fileOf=(name,mimeType,buffer)=>({name,mimeType,buffer});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,tag] of [[1440,900,'desktop'],[390,844,'phone']]){
  running=true;stopped=false;sent=null;actions.length=0;Object.assign(cards[0],{preparation_status:'running',preparation_error:null,preparation_reason:null});
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',hasTouch:tag==='phone',isMobile:tag==='phone'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const shot=async n=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/${n}-${tag}.png`})};
  await page.goto('http://127.0.0.1:'+server.address().port+'/#chat='+ID);
  await page.locator('#chat-log .chat-live').waitFor();
  await shot(shotsOnly?'before-running':'running');
  if(shotsOnly){await context.close();continue}
  // While the reply runs: Stop instead of Send; typing brings Send back (a new message replaces the run)
  assert.ok(await page.locator('[data-chat-stop]').isVisible());assert.ok(!(await page.locator('[data-chat-send]').isVisible()));
  await page.locator('#chat-input').fill('wait');assert.ok(await page.locator('[data-chat-send]').isVisible());assert.ok(!(await page.locator('[data-chat-stop]').isVisible()));
  await page.locator('#chat-input').fill('');assert.ok(await page.locator('[data-chat-stop]').isVisible());
  await page.locator('[data-chat-stop]').click();
  await page.locator('#chat-log .chat-stopped').waitFor();
  assert.deepEqual(actions.find(a=>a.action==='chat_stop').args,{suggestion_id:ID});
  assert.equal(await page.locator('#chat-log .chat-live').count(),0);
  assert.ok((await page.locator('#chat-log .chat-msg.machine .bubble').allTextContents()).some(t=>t.includes('Here is a reply: Hi Sam, Tuesday…')),'the reply so far stays, cut off');
  // Stopped sits on the reply: right under its text and before the card's choices, not as a line of its own
  const order=await page.locator('#chat-log .chat-stopped').evaluate(n=>{const m=n.closest('.chat-msg');return [...m.children].map(c=>c.className.split(' ')[0])});
  assert.deepEqual(order.slice(0,2),['bubble','chat-noted'],order.join());assert.ok(order.indexOf('chat-options')<0||order.indexOf('chat-options')>1,order.join());
  assert.equal(await page.locator('#chat-log .chat-event',{hasText:'Stopped'}).count(),0);
  assert.ok(await page.locator('[data-chat-send]').isVisible());assert.ok(!(await page.locator('[data-chat-stop]').isVisible()));
  await shot('stopped');
  // Add files: an image and a PDF upload at once and wait in the tray with a preview
  await page.locator('#chat-file').setInputFiles([fileOf('venue.png','image/png',PNG),fileOf('Quote.pdf','application/pdf',Buffer.from('%PDF-1.4\n'+'x'.repeat(30000)))]);
  await page.locator('#chat-tray .chat-att:not(.up)').nth(1).waitFor();
  const ups=actions.filter(a=>a.action==='chat_upload');
  assert.deepEqual(ups.map(a=>[a.upload,a.args.suggestion_id,a.args.name]),[['chat-file',ID,'venue.png'],['chat-file',ID,'Quote.pdf']]);
  assert.equal(Buffer.from(ups[0].args.data,'base64').compare(PNG),0);
  assert.equal(await page.locator('#chat-tray .chat-att.img img').count(),1);
  assert.match(await page.locator('#chat-tray .chat-att:not(.img)').textContent(),/Quote\.pdf\s*29 KB/);
  // Only files is a message too: Send is ready without text
  assert.ok(await page.locator('[data-chat-send]').isEnabled());
  // Too big, or a type it can't read: said at once, nothing uploads
  await page.evaluate(()=>{const dt=new DataTransfer();dt.items.add(new File([new Uint8Array(6*1048576)],'huge.png',{type:'image/png'}));dt.items.add(new File(['<b>x</b>'],'page.html',{type:'text/html'}));
   const input=document.querySelector('#chat-file');input.files=dt.files;input.dispatchEvent(new Event('change',{bubbles:true}))});
  assert.match(await page.locator('#chat-file-error').textContent(),/huge\.png is too big \(6\.0 MB\)\. Images can be up to 5\.0 MB\..*I can’t read page\.html/);
  assert.equal(actions.filter(a=>a.action==='chat_upload').length,2);
  await shot('files');
  // A pasted screenshot joins too; pasted text stays text
  await page.locator('#chat-input').focus();
  await page.evaluate(b64=>{const dt=new DataTransfer();dt.items.add(new File([Uint8Array.from(atob(b64),c=>c.charCodeAt(0))],'image.png',{type:'image/png'}));
   document.querySelector('#chat-input').dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}))},PNG.toString('base64'));
  await page.locator('#chat-tray .chat-att:not(.up)').nth(2).waitFor();
  assert.equal(actions.filter(a=>a.action==='chat_upload').at(-1).args.name,'Pasted image.png');
  // A drop on the chat adds files too, with a hint while dragging
  await page.evaluate(b64=>{const dt=new DataTransfer();dt.items.add(new File([Uint8Array.from(atob(b64),c=>c.charCodeAt(0))],'dropped.png',{type:'image/png'}));
   const at=document.querySelector('#chat-log');at.dispatchEvent(new DragEvent('dragenter',{dataTransfer:dt,bubbles:true,cancelable:true}));
   window.__hint=document.querySelector('.chat-layout').classList.contains('chat-drop');at.dispatchEvent(new DragEvent('drop',{dataTransfer:dt,bubbles:true,cancelable:true}))},PNG.toString('base64'));
  assert.ok(await page.evaluate(()=>window.__hint));
  await page.locator('#chat-tray .chat-att:not(.up)').nth(3).waitFor();
  assert.ok(!(await page.evaluate(()=>document.querySelector('.chat-layout').classList.contains('chat-drop'))));
  // Remove takes one back (and tells the service)
  await page.locator('#chat-tray [data-att-remove]').nth(3).click();
  assert.equal(await page.locator('#chat-tray .chat-att').count(),3);
  assert.equal(actions.filter(a=>a.action==='chat_file_remove').length,1);
  // Send: the files go with the message and show in the thread with it
  await page.locator('#chat-input').fill('Use the date on this photo');
  await page.locator('[data-chat-send]').click();
  await page.locator('#chat-log .chat-msg.you .chat-you-img').first().waitFor();
  const decide=actions.find(a=>a.action==='decide');
  assert.equal(decide.args.feedback,'Use the date on this photo');assert.equal(decide.args.files.length,3);
  assert.equal(await page.locator('#chat-tray').isHidden(),true);
  assert.ok(await page.locator('#chat-log .chat-msg.you .chat-files a.via-file',{hasText:'Quote.pdf'}).isVisible());
  await page.waitForTimeout(400);
  await shot('sent');
  // Nothing sticks out sideways on a phone
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'no sideways scroll');
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('chat stop and files dashboard ok');
