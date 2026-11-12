import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's text shows Show more and the fade over its last line only when more than one line of it would be cut off
// (Show more takes about a line itself). A summary that fills one line more than its 2, or a ready draft one more than its
// 3, shows whole: no Show more, no fade. One word more and both come back. Checked at 1440 and 390 wide, at 1x and 1.5x display scaling (fractional pixels), light and dark, and again
// after the page gets narrower. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const words=('Peter cannot come on the eleventh, and they ask when he can come instead. He already promised to confirm another day; '+
 'there is no replacement date yet, so the painting waits until he answers and the room stays as it is for now. ').repeat(4).trim().split(' ');
const mail=(id,body)=>({kind:'email',revision:'r-'+id,label:'Send',to:['robin@example.invalid'],to_name:'Robin',subject:'Re: Painting',body});
let fit={body:60,draft:80},extra=1;  // words that fill the summary's 2 lines and the draft's 3, plus one line, measured per width below
const cards=()=>[
 {id:'fitbody',title:'Wait for the painting date',body:words.slice(0,fit.body).join(' '),status:'pending',scope:'personal',created_at:now,event_ids:[1]},
 {id:'cutbody',title:'Wait for the other date',body:words.slice(0,fit.body+1).join(' '),status:'pending',scope:'personal',created_at:now,event_ids:[2]},
 {id:'fitdraft',title:'Reply about the painting',body:'They asked for a new date.',status:'prepared',scope:'personal',created_at:now,event_ids:[3],next_actions:[mail('fitdraft',words.slice(0,fit.draft).join(' '))]},
 {id:'cutdraft',title:'Reply about the other date',body:'They asked for a new date.',status:'prepared',scope:'personal',created_at:now,event_ids:[4],next_actions:[mail('cutdraft',words.slice(0,fit.draft+extra).join(' '))]}];
const state=()=>({suggestions:cards(),promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
// The most words that still fit `lines` lines in this text box (its own wrapping, read from the line boxes the text makes)
const most=(el,{words,lines})=>{const lh=parseFloat(getComputedStyle(el).lineHeight),n=k=>{el.textContent=words.slice(0,k).join(' ');return Math.round(el.getBoundingClientRect().height/lh)};
 let lo=1,hi=words.length;while(lo<hi){const m=Math.ceil((lo+hi)/2);if(n(m)<=lines)lo=m;else hi=m-1}return lo};
const look=(page,id)=>page.locator('#task-'+id).evaluate(c=>{const masked=el=>!!el&&getComputedStyle(el).maskImage!=='none'&&getComputedStyle(el).webkitMaskImage!=='none';
 const db=c.querySelector('.draft .db'),body=c.querySelector('.body');
 return {more:[...c.querySelectorAll('button.more')].filter(b=>b.checkVisibility()).map(b=>b.textContent),fade:masked(body)||masked(db)}});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scale of [1,1.5])for(const scheme of ['light','dark']){const mobile=width<600,why=`${width}@${scale}x ${scheme}`;
  const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:scale,isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(why+': '+e.message));
  const open=async()=>{await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-cutdraft').waitFor();await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(200)};
  // Measure how many words fill the boxes and one line more at this width (the text itself, no clamp), then draw the to-dos with exactly that
  fit={body:60,draft:80};extra=1;await open();
  const body=await page.locator('#task-cutbody .body').evaluate((b,a)=>{b.classList.remove('clamp');const p=b.querySelector('p');return (0,eval)(a.most)(p,{words:a.words,lines:3})},{most:most.toString(),words});
  const draft=await page.locator('#task-cutdraft .draft .db').evaluate((d,a)=>{d.closest('.draft').classList.remove('clamp');const p=d.querySelector('div,p')||d;return (0,eval)(a.most)(p,{words:a.words,lines:4})},{most:most.toString(),words});
  // (a ready draft of 4 lines still shows whole, and on a phone 4 lines is short: there, a longer one folds)
  fit={body,draft};extra=mobile?20:1;await open();
  const fb=await look(page,'fitbody'),cb=await look(page,'cutbody'),fd=await look(page,'fitdraft'),cd=await look(page,'cutdraft');
  if(shots)await page.screenshot({path:`${shots}/clamp-${width}-${scale}x-${scheme}.png`,fullPage:true});
  assert.deepEqual(fb,{more:[],fade:false},why+': a summary one line over its 2 shows whole');
  assert.deepEqual(cb,{more:['Show more'],fade:true},why+': one word more is cut');
  assert.deepEqual(fd,{more:[],fade:false},why+': a draft one line over its 3 shows whole');
  assert.deepEqual(cd,{more:['Show more'],fade:true},why+': one word more is cut');
  // Show more still opens it whole, and Show less folds it again
  await page.locator('#task-cutbody button.more').click();assert.deepEqual(await look(page,'cutbody'),{more:['Show less'],fade:false},why+': opened');
  await page.locator('#task-cutbody button.more').click();assert.deepEqual(await look(page,'cutbody'),{more:['Show more'],fade:true},why+': folded');
  // Narrower: what fit at this width no longer does, and is measured again
  if(!mobile){await page.setViewportSize({width:640,height});await page.waitForTimeout(200);
   assert.deepEqual(await look(page,'fitbody'),{more:['Show more'],fade:true},why+': narrower, cut');
   await page.setViewportSize({width,height});await page.waitForTimeout(200);
   assert.deepEqual(await look(page,'fitbody'),{more:[],fade:false},why+': wide again, whole')}
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
