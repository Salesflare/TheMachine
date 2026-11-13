import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
import {callAfter} from './page-calls.mjs';
const {chromium}=await import('./browser.mjs');

// A milestone on done to-dos (todos-milestone.js, state.done_milestone): one card on top of To-dos with the count,
// Share and ×. × marks it seen on the Machine (done_milestone_seen) and it is gone, also on the next opening. Share hands
// the image to a phone's share sheet where there is one (Web Share, or the phone app's own); on a computer (a fine
// pointer), even one with a share sheet, or where there is none, a dialog (todos-milestone-share.js) with the image in
// two sizes, Download image (a blob: link, which a browser saves and the phone app takes), Copy image or Share image,
// and the text to post. Each button says what it did inside the dialog, and its × stays in reach on a phone. The image is drawn from the count alone: nothing from the owner's to-dos or name reaches it.
const ROOT=new URL('..',import.meta.url);
// The page goes with the Machine's own policy (PAGE_CSP): without it, a blob: image the Machine blocks showed here all the same
const pageCsp=()=>{const m=readFileSync(new URL('machine/web/handler.py',ROOT),'utf8').match(/^PAGE_CSP = \(((?:\s*"[^"]*")+)\)/m);
 if(!m)throw new Error('machine/web/handler.py: no PAGE_CSP');return [...m[1].matchAll(/"([^"]*)"/g)].map(x=>x[1]).join('')};
const dashboard=await dashboardPage(),CSP=pageCsp();
const BRAND={'party.webp':'brand/party.webp','party-512.webp':'brand/party-512.webp','serif.woff2':'brand/fonts/source-serif-4-latin.woff2','sans.woff2':'brand/fonts/inter-latin.woff2'};
const now=new Date().toISOString();
const ID='00000000000000a1',SECRET='Reply to Sam Keller about the Acme renewal';
let milestone=null,seen=[],slowArt=0;
const cards=[{id:ID,title:SECRET,body:'sam.keller@acme.example asked for pricing.',status:'pending',scope:'work',created_at:now,event_ids:[1]}];
const state=()=>({suggestions:cards,done_milestone:milestone,done_counts:{all:503,work:503,personal:0},whats_new:null,greeting:null,first_tips:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},
 owner_name:'Sam Keller',locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.setHeader('Content-Security-Policy',CSP);res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){const f=BRAND[url.pathname.slice(7)];if(!f){res.statusCode=404;res.end();return}
  if(slowArt&&f.endsWith('party-512.webp'))await new Promise(r=>setTimeout(r,slowArt));  // a phone on a slow line
  res.setHeader('Content-Type',f.endsWith('.webp')?'image/webp':'font/woff2');res.end(readFileSync(new URL(f,ROOT)));return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);
  if(b.action==='done_milestone_seen'){seen.push(b.args.count);milestone=null;res.end(JSON.stringify({done_milestone:null}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const base=()=>'http://127.0.0.1:'+server.address().port;
// share: what the page's navigator offers ('none': no Web Share, as on a computer's browser; 'files': a phone's sheet)
const open=async(width,{share='none',motion='no-preference',theme,app,clip=true,canvas,counts}={})=>{const context=await browser.newContext({viewport:{width,height:844},hasTouch:width<600,reducedMotion:motion});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 // counts: every number the count-up shows, with each frame's time 50 ms before the frame is asked for, the way a
 // frame already under way hands its own start time
 if(counts)await context.addInitScript(()=>{window.counts=[];const raf=window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame=f=>{const at=performance.now();return raf(()=>f(at-50))};
  new MutationObserver(()=>{const b=document.querySelector('#milestone .ms-n');if(b&&window.counts.at(-1)!==b.textContent)window.counts.push(b.textContent)})
   .observe(document,{childList:true,subtree:true,characterData:true})});
 await context.addInitScript(share=>{
  if(share==='none'){delete Navigator.prototype.share;delete Navigator.prototype.canShare}
  else{Navigator.prototype.canShare=d=>!!d?.files?.length;Navigator.prototype.share=async d=>{window.shared={files:d.files.map(f=>({name:f.name,type:f.type,size:f.size})),text:d.text,url:d.url}}}
  // every word the image gets: the canvas's own text calls
  window.drawn=[];const fill=CanvasRenderingContext2D.prototype.fillText;CanvasRenderingContext2D.prototype.fillText=function(text,...a){window.drawn.push(String(text));return fill.call(this,text,...a)}},share);
 // app: the phone app's hooks (mobile/www/inject.js): 'old' only takes downloads, 'new' also has the share sheet
 if(app)await context.addInitScript(app=>{window.saved=[];window.appShared=[];window.__machineFiles=(href,name)=>window.saved.push([href,name]);
  document.addEventListener('click',e=>{const a=e.target.closest?.('a[download]');if(a&&a.href.startsWith('blob:'+location.origin+'/')){e.preventDefault();window.saved.push([a.href.slice(0,5),a.getAttribute('download')])}},true);
  if(app==='new')window.__machineShareFile=async(blob,name)=>{window.appShared.push({name,type:blob.type,size:blob.size});return true}},app);
 // clip: what the clipboard does with an image (true: takes it; false: refuses, as a browser without the permission)
 await context.addInitScript(clip=>{window.clipped=[];if(!navigator.clipboard)return;
  navigator.clipboard.write=async items=>{if(!clip)throw new DOMException('Write permission denied.','NotAllowedError');for(const i of items)window.clipped.push(i.types.join())};
  navigator.clipboard.writeText=async text=>{window.clipped.push(text)}},clip);
 // canvas 'old': a canvas without roundRect, as on a phone's browser before Chrome 99 or Safari 16
 if(canvas==='old')await context.addInitScript(()=>{delete CanvasRenderingContext2D.prototype.roundRect;delete Path2D.prototype.roundRect});
 if(theme)await context.addInitScript(theme=>{try{localStorage.setItem('theme',theme)}catch{}},theme);
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base()+'/');await page.locator('#task-'+ID).first().waitFor({state:'attached'});return {context,page}};
const card=page=>page.locator('#milestone');
// msImage's own inputs, for each image made: what it was asked to draw from
const watchInputs=page=>page.evaluate(()=>{window.inputs=[];const made=msImage;msImage=(...a)=>{window.inputs.push(a);return made(...a)}});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  // Due: the card on top of To-dos, inside the screen, with the count, a line, Share and ×
  milestone={count:500};seen=[];
  {const {context,page}=await open(width,{counts:true});await card(page).waitFor();
   await page.waitForFunction(()=>document.querySelector('#milestone .ms-n')?.textContent==='500');
   // The count-up: from 0 up to 500, never below 0, never back down, never past it, even when the first frame's
   // time is earlier than when the count was asked for (as browsers hand it)
   // (the first is the card as drawn, 500, before the count starts)
   const counts=(await page.evaluate(()=>window.counts.map(c=>+c.replace(/\D/g,'')*(c.trim().startsWith('-')||c.includes('−')?-1:1)))).slice(1);
   assert.ok(counts.length>2,JSON.stringify(counts));
   assert.ok(counts.every((c,i)=>c>=0&&c<=500&&(!i||c>=counts[i-1])),JSON.stringify(counts));
   assert.equal(counts.at(-1),500);
   assert.equal((await page.locator('#milestone h2').textContent()).trim(),'500 to-dos done');
   assert.equal(await page.locator('#milestone p').textContent(),'That’s a lot off your plate.');
   assert.deepEqual(await page.locator('#milestone button').evaluateAll(b=>b.map(x=>x.textContent||x.getAttribute('aria-label'))),['Share','Close']);
   const box=await card(page).boundingBox(),list=await page.locator('#suggestions').boundingBox();
   assert.ok(box.x>=list.x-1&&box.x+box.width<=list.x+list.width+1&&box.x+box.width<=width&&box.height<(width<600?170:120),JSON.stringify(box));
   assert.ok(await page.evaluate(()=>document.querySelector('#suggestions').firstElementChild.id==='milestone'));
   // ×: seen on the Machine with its level, and gone
   assert.deepEqual(await callAfter(page,'done_milestone_seen',()=>page.locator('#milestone [data-ms-close]').click()),{action:'done_milestone_seen',args:{count:500}});
   await card(page).waitFor({state:'detached'});assert.deepEqual(seen,[500]);
   await page.evaluate(()=>refresh());await page.waitForTimeout(300);assert.equal(await card(page).count(),0);
   await context.close()}
  // Closed stays closed: the next opening has none
  {const {context,page}=await open(width);await page.waitForTimeout(600);assert.equal(await card(page).count(),0);
   assert.equal(await page.evaluate(()=>lazyIn('milestone')&&typeof milestoneCard),'function');  // (inline here; served, it isn't even loaded)
   await context.close()}
 }
 // A share sheet (a phone, the installed app): Share hands it the square image and the text with the link, nothing else
 milestone={count:500};
 {const {context,page}=await open(390,{share:'files'});await card(page).waitFor();await watchInputs(page);
  assert.equal(await page.evaluate(()=>matchMedia('(pointer: coarse)').matches),true);
  await page.locator('#milestone [data-ms-share]').click();await page.waitForFunction(()=>window.shared);
  const shared=await page.evaluate(()=>window.shared);
  assert.equal(shared.files.length,1);assert.equal(shared.files[0].name,'the-machine-500-todos.png');assert.equal(shared.files[0].type,'image/png');assert.ok(shared.files[0].size>20000);
  assert.equal(shared.text,'500 to-dos done with The Machine. https://themachine.computer');assert.equal(shared.url,undefined);
  assert.equal(await page.locator('#ms-share[open]').count(),0);assert.equal(await card(page).count(),1);  // shared, not closed: × still says when
  await context.close()}
 // No share sheet: the dialog, with the image in both sizes, Download image and the text to post
 {const {context,page}=await open(1440);await card(page).waitFor();await watchInputs(page);
  await page.locator('#milestone [data-ms-share]').click();const d=page.locator('#ms-share[open]');await d.waitFor();
  const size=()=>page.locator('#ms-share .ms-preview').evaluate(async i=>{await i.decode();return [i.naturalWidth,i.naturalHeight,i.src.slice(0,5)]});
  assert.deepEqual(await size(),[1080,1080,'blob:']);
  await page.locator('#ms-share [data-ms-size="wide"]').click();await page.waitForFunction(()=>document.querySelector('#ms-share .ms-preview').naturalWidth===1200);
  assert.deepEqual(await size(),[1200,630,'blob:']);
  assert.equal(await page.locator('#ms-share .ms-post-text').textContent(),'500 to-dos done with The Machine. https://themachine.computer');
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#ms-share [data-ms-download]').click()]);
  assert.equal(download.suggestedFilename(),'the-machine-500-todos-wide.png');
  assert.ok(download.url().startsWith('blob:'),download.url());  // a data: link does nothing in a phone's WebView
  // Copy image and Copy text: on the clipboard, and said inside the dialog (a toast would sit under it)
  const said=()=>page.locator('#ms-share .ms-said').evaluate(p=>p.hidden?'':p.textContent);
  await page.locator('#ms-share [data-ms-copy-image]').click();await page.waitForFunction(()=>window.clipped.length===1);
  assert.deepEqual(await page.evaluate(()=>window.clipped),['image/png']);assert.equal(await said(),'Image copied.');
  await page.locator('#ms-share [data-ms-copy-text]').click();await page.waitForFunction(()=>window.clipped.length===2);
  assert.equal(await page.evaluate(()=>window.clipped[1]),'500 to-dos done with The Machine. https://themachine.computer');assert.equal(await said(),'Copied.');
  // The image's inputs are the count, the size and the theme; its words are the count and fixed text, never the owner's
  const inputs=await page.evaluate(()=>window.inputs);
  assert.ok(inputs.length>=2);for(const i of inputs){assert.equal(i.length,3);assert.equal(i[0],500);assert.equal(typeof i[1],'boolean');assert.equal(typeof i[2],'boolean')}
  const words=[...new Set(await page.evaluate(()=>window.drawn))].sort();
  assert.deepEqual(words,['500','My Machine and I, on a roll.','themachine.computer','to-dos done']);
  const all=JSON.stringify(words);for(const s of ['Sam','Keller','Acme','@',SECRET])assert.ok(!all.includes(s),s);
  await page.keyboard.press('Escape');await d.waitFor({state:'detached'}).catch(()=>{});assert.equal(await page.locator('#ms-share[open]').count(),0);
  assert.equal(await card(page).count(),1);await context.close()}
 // A computer whose browser has a share sheet (Windows' Chrome and Edge): the dialog all the same, never the sheet,
 // Download image first and focused, Copy image and no Share image; Esc closes it and focus is back on Share
 {const {context,page}=await open(1440,{share:'files'});await card(page).waitFor();
  assert.equal(await page.evaluate(()=>matchMedia('(pointer: fine)').matches),true);
  await page.locator('#milestone [data-ms-share]').click();const d=page.locator('#ms-share[open]');await d.waitFor();
  assert.equal(await page.evaluate(()=>window.shared),undefined);
  assert.equal(await page.locator('#ms-share .ms-preview').evaluate(async i=>{await i.decode();return i.naturalWidth}),1080);
  assert.deepEqual(await page.locator('#ms-share .ms-acts button').evaluateAll(b=>b.map(x=>x.textContent)),['Download image','Copy image']);
  assert.equal(await page.evaluate(()=>document.activeElement?.hasAttribute('data-ms-download')),true);
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#ms-share [data-ms-download]').click()]);
  assert.equal(download.suggestedFilename(),'the-machine-500-todos.png');
  await page.locator('#ms-share [data-ms-copy-image]').click();await page.waitForFunction(()=>window.clipped.length===1);
  assert.equal(await page.evaluate(()=>window.shared),undefined);
  await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.querySelector('#ms-share[open]'));
  await page.waitForFunction(()=>document.activeElement?.hasAttribute('data-ms-share'),null,{timeout:3000});
  await context.close()}
 // ... and when its clipboard refuses the image, it says so in the dialog instead of opening the sheet
 {const {context,page}=await open(1440,{share:'files',clip:false});await card(page).waitFor();
  await page.locator('#milestone [data-ms-share]').click();await page.locator('#ms-share[open]').waitFor();
  await page.locator('#ms-share [data-ms-copy-image]').click();await page.waitForFunction(()=>!document.querySelector('#ms-share .ms-said').hidden);
  assert.equal(await page.locator('#ms-share .ms-said').textContent(),'That didn’t work here. Download the image instead.');
  assert.equal(await page.evaluate(()=>window.shared),undefined);await context.close()}
 // A phone: the dialog is the whole screen, its × on the title's row (below the phone's status bar, env(safe-area-inset-top)) and closing it; a refused copy says so in the dialog
 {const {context,page}=await open(390,{clip:false});await card(page).waitFor();
  await page.locator('#milestone [data-ms-share]').click();const d=page.locator('#ms-share[open]');await d.waitFor();
  const x=await page.locator('#ms-share [data-ms-close-share]').boundingBox(),title=await page.locator('#ms-share-title').boundingBox();
  assert.ok(x.y>=8&&x.x+x.width<=390&&x.width>=24&&Math.abs((x.y+x.height/2)-(title.y+title.height/2))<12,JSON.stringify([x,title]));
  await page.locator('#ms-share [data-ms-copy-image]').click();
  await page.waitForFunction(()=>!document.querySelector('#ms-share .ms-said').hidden);
  assert.equal(await page.locator('#ms-share .ms-said').textContent(),'That didn’t work here. Download the image instead.');
  assert.ok(await page.locator('#ms-share .ms-said').isVisible());
  await page.locator('#ms-share [data-ms-close-share]').click();await page.waitForFunction(()=>!document.querySelector('#ms-share[open]'));
  assert.equal(await card(page).count(),1);await context.close()}
 // The phone app (its WebView has no Web Share and puts no image on the clipboard): Share goes to the app's own sheet;
 // an app from before that gets the dialog with Download image, which the app takes as a blob: link, and no Copy image
 {const {context,page}=await open(390,{app:'new'});await card(page).waitFor();
  await page.locator('#milestone [data-ms-share]').click();await page.waitForFunction(()=>window.appShared.length===1);
  const got=(await page.evaluate(()=>window.appShared))[0];assert.equal(got.name,'the-machine-500-todos.png');assert.equal(got.type,'image/png');assert.ok(got.size>20000);
  assert.equal(await page.locator('#ms-share[open]').count(),0);
  await page.evaluate(()=>msDialog(500));await page.locator('#ms-share[open]').waitFor();
  assert.deepEqual(await page.locator('#ms-share .ms-acts button').evaluateAll(b=>b.map(x=>x.textContent)),['Download image','Share image']);
  await page.locator('#ms-share [data-ms-share-image]').click();await page.waitForFunction(()=>window.appShared.length===2);
  await page.locator('#ms-share [data-ms-download]').click();await page.waitForFunction(()=>window.saved.length===1);
  assert.deepEqual(await page.evaluate(()=>window.saved),[['blob:','the-machine-500-todos.png']]);
  await context.close()}
 {const {context,page}=await open(390,{app:'old'});await card(page).waitFor();
  await page.locator('#milestone [data-ms-share]').click();await page.locator('#ms-share[open]').waitFor();
  assert.deepEqual(await page.locator('#ms-share .ms-acts button').evaluateAll(b=>b.map(x=>x.textContent)),['Download image']);
  await page.locator('#ms-share [data-ms-download]').click();await page.waitForFunction(()=>window.saved.length===1);
  assert.deepEqual(await page.evaluate(()=>window.saved),[['blob:','the-machine-500-todos.png']]);
  // the app reads the link's file with fetch (mobile/www/inject.js give), which the page's policy lets through
  assert.deepEqual(await page.evaluate(()=>fetch(msShownUrl).then(r=>r.blob()).then(b=>[b.type,b.size>20000])),['image/png',true]);
  await context.close()}
 // A phone with no share sheet, on a slow line (the mascot comes in late): the dialog's image shows, loaded and not
 // broken, in both sizes, light and dark, under the Machine's own policy
 slowArt=700;
 for(const theme of ['light','dark']){const {context,page}=await open(390,{theme});await card(page).waitFor();
  await page.locator('#milestone [data-ms-share]').click();await page.locator('#ms-share[open]').waitFor();
  const shown=()=>page.waitForFunction(()=>{const i=document.querySelector('#ms-share .ms-preview');return i?.complete&&i.naturalWidth>0&&[i.naturalWidth,i.naturalHeight]},null,{timeout:8000}).then(h=>h.jsonValue());
  assert.deepEqual(await shown(),[1080,1080]);
  await page.locator('#ms-share [data-ms-size="wide"]').click();await page.waitForFunction(()=>document.querySelector('#ms-share .ms-preview').naturalWidth===1200,null,{timeout:8000});
  assert.deepEqual(await shown(),[1200,630]);
  await page.locator('#ms-share [data-ms-size="square"]').click();await page.waitForFunction(()=>document.querySelector('#ms-share .ms-preview').naturalWidth===1080,null,{timeout:8000});
  assert.deepEqual(await shown(),[1080,1080]);
  await context.close()}
 slowArt=0;
 // An older phone browser, whose canvas has no roundRect ("c.roundRect is not a function"): the image still draws, in
 // both sizes, its rounded confetti and the site's chip made from arcTo
 {const {context,page}=await open(390,{canvas:'old'});await card(page).waitFor();
  assert.equal(await page.evaluate(()=>typeof CanvasRenderingContext2D.prototype.roundRect),'undefined');
  const drawn=await page.evaluate(()=>{let k=0;const a=CanvasRenderingContext2D.prototype.arcTo;CanvasRenderingContext2D.prototype.arcTo=function(...x){k++;return a.apply(this,x)};
   return msImage(500,false,false).then(cv=>{CanvasRenderingContext2D.prototype.arcTo=a;return [k,cv.width,cv.height]})});
  assert.ok(drawn[0]>=8&&drawn[0]%4===0&&drawn[1]===1080&&drawn[2]===1080,JSON.stringify(drawn));  // the chip and the confetti, 4 corners each
  await page.locator('#milestone [data-ms-share]').click();await page.locator('#ms-share[open]').waitFor();
  const size=()=>page.locator('#ms-share .ms-preview').evaluate(async i=>{await i.decode();return [i.naturalWidth,i.naturalHeight]});
  assert.deepEqual(await size(),[1080,1080]);
  await page.locator('#ms-share [data-ms-size="wide"]').click();await page.waitForFunction(()=>document.querySelector('#ms-share .ms-preview').naturalWidth===1200);
  assert.deepEqual(await size(),[1200,630]);
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#ms-share [data-ms-download]').click()]);
  assert.equal(download.suggestedFilename(),'the-machine-500-todos-wide.png');
  await context.close()}
 // Reduced motion: no pop, no confetti, the number as it is
 {const {context,page}=await open(1440,{motion:'reduce'});await card(page).waitFor();
  assert.equal(await page.locator('#milestone .ms-n').textContent(),'500');
  assert.equal(await page.locator('#milestone .ms-bot img').evaluate(i=>getComputedStyle(i).animationName),'none');
  assert.equal(await page.locator('#milestone .ms-bot i').first().evaluate(i=>getComputedStyle(i).display),'none');
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('milestone ok');
