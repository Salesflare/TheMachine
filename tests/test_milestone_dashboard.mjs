import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
import {callAfter} from './page-calls.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A milestone on done to-dos (todos-milestone.js, state.done_milestone): one card on top of To-dos with the count,
// Share and ×. × marks it seen on the Machine (done_milestone_seen) and it is gone, also on the next opening. Share hands
// the image to the share sheet where there is one, else a dialog with the image in two sizes, Download image and the
// text to post. The image is drawn from the count alone: nothing from the owner's to-dos or name reaches it.
const dashboard=await dashboardPage();
const ROOT=new URL('..',import.meta.url);
const BRAND={'party.webp':'brand/party.webp','party-512.webp':'brand/party-512.webp','serif.woff2':'brand/fonts/source-serif-4-latin.woff2','sans.woff2':'brand/fonts/inter-latin.woff2'};
const now=new Date().toISOString();
const ID='00000000000000a1',SECRET='Reply to Sam Keller about the Acme renewal';
let milestone=null,seen=[];
const cards=[{id:ID,title:SECRET,body:'sam.keller@acme.example asked for pricing.',status:'pending',scope:'work',created_at:now,event_ids:[1]}];
const state=()=>({suggestions:cards,done_milestone:milestone,done_counts:{all:503,work:503,personal:0},whats_new:null,greeting:null,first_tips:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},
 owner_name:'Sam Keller',locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){const f=BRAND[url.pathname.slice(7)];if(!f){res.statusCode=404;res.end();return}
  res.setHeader('Content-Type',f.endsWith('.webp')?'image/webp':'font/woff2');res.end(readFileSync(new URL(f,ROOT)));return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);
  if(b.action==='done_milestone_seen'){seen.push(b.args.count);milestone=null;res.end(JSON.stringify({done_milestone:null}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const base=()=>'http://127.0.0.1:'+server.address().port;
// share: what the page's navigator offers ('none': no Web Share, as on a computer's browser; 'files': a phone's sheet)
const open=async(width,{share='none',motion='no-preference',theme}={})=>{const context=await browser.newContext({viewport:{width,height:844},hasTouch:width<600,reducedMotion:motion});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await context.addInitScript(share=>{
  if(share==='none'){delete Navigator.prototype.share;delete Navigator.prototype.canShare}
  else{Navigator.prototype.canShare=d=>!!d?.files?.length;Navigator.prototype.share=async d=>{window.shared={files:d.files.map(f=>({name:f.name,type:f.type,size:f.size})),text:d.text,url:d.url}}}
  // every word the image gets: the canvas's own text calls
  window.drawn=[];const fill=CanvasRenderingContext2D.prototype.fillText;CanvasRenderingContext2D.prototype.fillText=function(text,...a){window.drawn.push(String(text));return fill.call(this,text,...a)}},share);
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
  {const {context,page}=await open(width);await card(page).waitFor();
   await page.waitForFunction(()=>document.querySelector('#milestone .ms-n')?.textContent==='500');
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
  await page.locator('#milestone [data-ms-share]').click();await page.waitForFunction(()=>window.shared);
  const shared=await page.evaluate(()=>window.shared);
  assert.equal(shared.files.length,1);assert.equal(shared.files[0].name,'the-machine-500-todos.png');assert.equal(shared.files[0].type,'image/png');assert.ok(shared.files[0].size>20000);
  assert.equal(shared.text,'500 to-dos done with The Machine. https://themachine.computer');assert.equal(shared.url,undefined);
  assert.equal(await page.locator('#ms-share[open]').count(),0);assert.equal(await card(page).count(),1);  // shared, not closed: × still says when
  await context.close()}
 // No share sheet: the dialog, with the image in both sizes, Download image and the text to post
 {const {context,page}=await open(1440);await card(page).waitFor();await watchInputs(page);
  await page.locator('#milestone [data-ms-share]').click();const d=page.locator('#ms-share[open]');await d.waitFor();
  const size=()=>page.locator('#ms-share .ms-preview').evaluate(async i=>{await i.decode();return [i.naturalWidth,i.naturalHeight,i.src.slice(0,22)]});
  assert.deepEqual(await size(),[1080,1080,'data:image/png;base64,']);
  await page.locator('#ms-share [data-ms-size="wide"]').click();await page.waitForFunction(()=>document.querySelector('#ms-share .ms-preview').naturalWidth===1200);
  assert.deepEqual(await size(),[1200,630,'data:image/png;base64,']);
  assert.equal(await page.locator('#ms-share .ms-post-text').textContent(),'500 to-dos done with The Machine. https://themachine.computer');
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#ms-share [data-ms-download]').click()]);
  assert.equal(download.suggestedFilename(),'the-machine-500-todos-wide.png');
  // The image's inputs are the count, the size and the theme; its words are the count and fixed text, never the owner's
  const inputs=await page.evaluate(()=>window.inputs);
  assert.ok(inputs.length>=2);for(const i of inputs){assert.equal(i.length,3);assert.equal(i[0],500);assert.equal(typeof i[1],'boolean');assert.equal(typeof i[2],'boolean')}
  const words=[...new Set(await page.evaluate(()=>window.drawn))].sort();
  assert.deepEqual(words,['500','My Machine and I, on a roll.','themachine.computer','to-dos done']);
  const all=JSON.stringify(words);for(const s of ['Sam','Keller','Acme','@',SECRET])assert.ok(!all.includes(s),s);
  await page.keyboard.press('Escape');await d.waitFor({state:'detached'}).catch(()=>{});assert.equal(await page.locator('#ms-share[open]').count(),0);
  assert.equal(await card(page).count(),1);await context.close()}
 // Reduced motion: no pop, no confetti, the number as it is
 {const {context,page}=await open(1440,{motion:'reduce'});await card(page).waitFor();
  assert.equal(await page.locator('#milestone .ms-n').textContent(),'500');
  assert.equal(await page.locator('#milestone .ms-bot img').evaluate(i=>getComputedStyle(i).animationName),'none');
  assert.equal(await page.locator('#milestone .ms-bot i').first().evaluate(i=>getComputedStyle(i).display),'none');
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('milestone ok');
