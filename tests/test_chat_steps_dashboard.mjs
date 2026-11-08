import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A run's steps in a to-do's chat ("Checked 30 things", unfolded): each kind of step is one row with how many times,
// never 30 rows of "Using the browser" / "Running a command", and nothing in the list is cut off at the left edge
// on a phone (numbers from 10 on lost their first digit). A list from an older Machine (plain titles, one per step)
// folds the same way, in the same words (its vague "Working" has no row). This Machine's says how many steps the run
// took in all (more than the 30 an older Machine kept), its rows in the owner's language, with the site a browser step was on.
// SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage(process.env.DASHBOARD);
const ID='e1e1e1e1e1e1e1e1',t0=Date.now()-3600000;
// The run on the phone: the browser and a command in turn, then the assistant's own checks
const older=[...Array.from({length:21},(_,n)=>n%2?'Running a command':'Using the browser'),
 'Checking the assistant','Running a command','Checking the assistant','Working','Running a command','Checking the assistant','Running a command','Checking the assistant','Running a command'];
const items=()=>[{kind:'you',text:'Can you order the New Year letters?',at:t0},
 {kind:'steps',steps:older,at:t0+1000},
 {kind:'reply',text:'Found the order page. The letters are in the cart.',at:t0+2000},
 {kind:'you',text:'Go ahead',at:t0+3000},
 {kind:'steps',count:58,steps:[{line:['Used the browser on {}','shop.example.com'],n:30},{line:['Ran a command'],n:20},{line:['Looked things up in The Machine'],n:5},{line:['Checked open to-dos'],n:2}],at:t0+4000},
 {kind:'reply',text:'Ordered.',at:t0+5000}];
let language='en';
const card={id:ID,title:'Order the New Year letters before Friday',body:'The shop closes orders Friday.',status:'prepared',scope:'personal',created_at:new Date(t0).toISOString(),event_ids:[1]};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const cat=/^\/i18n\/(\w\w(?:-[A-Z]{2})?)\.json$/.exec(url.pathname);if(cat){res.end(await readFile(new URL(`../i18n/${cat[1]}.json`,import.meta.url),'utf8').catch(()=>'{}'));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},
  ...(language!=='en'?{locale:{locale:'en-BE',region:'BE',language,language_set:true,clock:'auto',hour12:false,auto_hour12:false,date_locale:language+'-BE',saveable:true}}:{})}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body);
  if(r.action==='card_chat'){res.end(JSON.stringify({session:true,status:'ok',active:false,cursor:'k',items:items()}));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
// What each row shows, and whether any part of it (its marker included) lies left of the chat or outside its list
const rows=fold=>fold.evaluate(d=>{const log=document.querySelector('#chat-log').getBoundingClientRect(),list=d.querySelector('ol,ul');
 return [...list.children].map((li,i)=>{const cs=getComputedStyle(li),r=li.getBoundingClientRect();let marker=0;
  if(cs.display==='list-item'&&cs.listStyleType!=='none'){const m=document.createElement('span');m.style.cssText='position:absolute;visibility:hidden;white-space:pre;font:'+cs.font;
   m.textContent=(i+1)+'. ';document.body.append(m);marker=m.getBoundingClientRect().width;m.remove()}
  return {text:li.innerText.replace(/\s+/g,' ').trim(),left:r.left-marker,logLeft:log.left,room:parseFloat(getComputedStyle(list).paddingInlineStart),marker,right:r.right,logRight:log.right}})});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[320,700],[1440,900]])for(const colorScheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height},colorScheme,locale:'en-US',hasTouch:width<500,isMobile:width<500});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#chat='+ID);await page.locator('#chat-input').waitFor();
  const folds=page.locator('#chat-log .chat-steps');await folds.first().waitFor();
  assert.equal(await folds.count(),2);
  for(let n=0;n<2;n++){await folds.nth(n).locator('summary').click();await page.waitForFunction(n=>document.querySelectorAll('#chat-log .chat-steps')[n]?.open,n)}
  assert.deepEqual(await folds.locator('summary').allInnerTexts(),['Checked 30 things','Checked 58 things']);
  // The older list: one row per kind, with how many times
  const old=await rows(folds.nth(0));
  assert.deepEqual(old.map(r=>r.text),['Used the browser · 11','Ran a command · 14','Looked things up in The Machine · 4'],'runs fold into one row each, said as now, no Working row');
  // This Machine's list: in plain words, with the site
  const now=await rows(folds.nth(1));
  assert.deepEqual(now.map(r=>r.text),['Used the browser on shop.example.com · 30','Ran a command · 20','Looked things up in The Machine · 5','Checked open to-dos · 2']);
  // Nothing cut off: every row and its marker (if it has one) inside the chat, and the marker fits its room
  for(const r of [...old,...now]){
   assert.ok(r.left>=r.logLeft-0.5,`"${r.text}" starts inside the chat at ${width}: ${r.left} < ${r.logLeft}`);
   assert.ok(r.marker<=r.room+0.5,`"${r.text}": its marker (${r.marker}px) fits the list's room (${r.room}px) at ${width}`);
   assert.ok(r.right<=r.logRight+0.5,`"${r.text}" ends inside the chat at ${width}`);
  }
  assert.ok(await page.evaluate(()=>document.scrollingElement.scrollWidth<=document.scrollingElement.clientWidth),'no sideways scroll at '+width);
  if(shots&&width!==320){await page.evaluate(()=>document.fonts.ready);await folds.nth(0).scrollIntoViewIfNeeded();
   await page.screenshot({path:`${shots}/chat-steps-${width}-${colorScheme}.png`})}
  await context.close();
 }
 // In the owner's language: the summary and this Machine's rows are translated, the site stays as it is
 {language='nl';const context=await browser.newContext({viewport:{width:390,height:844},locale:'nl-BE'}),page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#chat='+ID);await page.waitForFunction(()=>document.documentElement.lang==='nl');const fold=page.locator('#chat-log .chat-steps').nth(1);await fold.waitFor();await fold.locator('summary').click();
  const got=(await rows(fold)).map(r=>r.text);
  assert.equal(got[0],'Gebruikte de browser op shop.example.com · 30');
  assert.equal(got[1],'Voerde een opdracht uit · 20');
  assert.equal(await fold.locator('summary').innerText(),'58 dingen nagekeken');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('chat steps dashboard ok');
}finally{await browser?.close();server.close()}
