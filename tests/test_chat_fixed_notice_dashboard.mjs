import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The Fixed lines ("Works now" / "Still not right") belong on the to-do list, above every view. Inside a to-do's chat they
// once stayed in the page under the phone's fixed chat column and showed through it, drawn over the messages. In a chat
// they don't show at all, on a phone or a computer, light or dark, and nothing of the banner box sits over the thread;
// back on the list they are there again. The phone's chat column is opaque, so a page element under it never shows through,
// and a usage limit stays in view above the chat, clear of the header and the messages. Made-up to-dos and lines.
const dashboard=await dashboardPage(),en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const now=new Date().toISOString(),ID='c1c1c1c1c1c1c1c1',j=JSON.stringify;
const cards=[{id:ID,title:'Update the registered address',body:'b',status:'prepared',scope:'work',created_at:now,event_ids:[1]},
 {id:'c2c2c2c2c2c2c2c2',title:'Renew the passport',body:'b',status:'pending',scope:'personal',created_at:now,event_ids:[2]}];
const fixed=[{id:'f1',text:'Fixed: the Projects tab now opens on the first tap. Thanks for reporting it.'},
 {id:'f2',text:'Fixed: connection cards now show account names instead of ids.'}];
let pause=null;
const state=()=>({model_pause:pause,fixed,suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const items=[{kind:'reply',text:'Found the record and filled in the new address. It is ready to save; the existing record has not been overwritten.',at:Date.now()-300000},
 {kind:'you',text:'can you fix the capitalization first',at:Date.now()-240000},
 {kind:'reply',text:'Corrected the street name in the prepared form. Saving still waits for your confirmation.',at:Date.now()-180000}];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/en.json'){res.end(en);return}
 if(url.pathname==='/api/status'){res.end(j(state()));return}
 if(url.pathname==='/api/action'&&JSON.parse(body||'{}').action==='card_chat'){res.end(j({session:true,status:'ok',active:false,cursor:'k',items}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,errors=[];let browser;
const hit=(a,b)=>a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]])for(const theme of ['light','dark'])for(const limit of [false,true]){
  pause=limit?{window:'5h',until:Math.floor(Date.now()/1000)+3*3600,name:'ChatGPT'}:null;
  const phone=width<500,context=await browser.newContext({viewport:{width,height},deviceScaleFactor:phone?3:1,isMobile:phone,hasTouch:phone,colorScheme:theme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.addInitScript(t=>{try{localStorage.setItem('theme',t)}catch{}},theme);
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));const at=`${width} ${theme}${limit?' limit':''}`;
  // On the list: the Fixed lines show
  await page.goto(base+'/');await page.locator('#fixed-notice .fixed-notice').first().waitFor();
  assert.ok(await page.locator('#fixed-notice').isVisible(),'the Fixed lines show on the list: '+at);
  // In the chat: they don't, and no banner box covers a message; a usage limit stays in view, clear of the chat
  await page.goto(base+'/#chat='+ID);await page.locator('h2.chat-title').waitFor();await page.locator('.chat-log .chat-msg.you').waitFor();
  await page.waitForTimeout(300);
  const m=await page.evaluate(()=>{const R=n=>{const r=n.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,w:r.width,h:r.height}};
   const shown=n=>{const r=n.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(n).visibility!=='hidden'};
   // A page element left under the phone's fixed chat column must not show through it
   const main=document.querySelector('.chat-main'),probe=document.createElement('div');probe.id='under-probe';probe.textContent='under';probe.style.cssText='height:2000px;background:#f0f';
   document.querySelector('main').prepend(probe);const c=R(main),x=(c.left+c.right)/2,y=(c.top+c.bottom)/2,stack=document.elementsFromPoint(x,y);
   const under=stack.includes(probe)&&stack.indexOf(probe)>stack.findIndex(n=>main.contains(n)||n===main),bg=getComputedStyle(main).backgroundColor;probe.remove();
   const lim=document.querySelector('#limit-banner');
   return {notices:[...document.querySelectorAll('#fixed-notice .fixed-notice,#fixed-notice button')].filter(shown).map(R),
    box:shown(document.querySelector('#banners'))&&!shown(lim)?[R(document.querySelector('#banners'))]:[],
    limit:shown(lim)?R(lim):null,head:R(document.querySelector('.chat-head')),fixed:getComputedStyle(main).position==='fixed',under,bg,
    msgs:[...document.querySelectorAll('.chat-log>*')].filter(shown).map(R)}});
  if(process.env.SHOTS)await page.screenshot({path:`${process.env.SHOTS}/chat-fixed-${width}-${theme}${limit?'-limit':''}.png`});
  assert.ok(m.msgs.length>=3,'the thread shows: '+at);
  assert.deepEqual(m.notices,[],'no Fixed line in a to-do chat: '+at);
  assert.deepEqual(m.box,[],'no empty banner box over the chat: '+at);
  for(const n of [...m.notices,...m.box])for(const x of m.msgs)assert.ok(!hit(n,x),'nothing of the banners over a message: '+at);
  if(phone){assert.ok(m.fixed&&m.under,'a page element is under the phone chat column: '+at+' '+j(m));
   const a=m.bg.match(/rgba?\(([^)]*)\)/)[1].split(/[ ,\/]+/).filter(Boolean);assert.ok(a.length===3||+a[3]===1,'the chat column is opaque ('+m.bg+'): '+at)}
  if(limit){assert.ok(m.limit,'the usage limit stays in view in the chat: '+at);
   assert.ok(m.limit.bottom<=m.head.top+0.5,'the usage limit sits above the chat header: '+at+' '+j(m));
   for(const x of m.msgs)assert.ok(!hit(m.limit,x),'the usage limit is clear of the messages: '+at)}
  else assert.equal(m.limit,null);
  // Back on the list they are there again
  await page.goto(base+'/');await page.locator('#fixed-notice .fixed-notice').first().waitFor();
  assert.ok(await page.locator('#fixed-notice').isVisible(),'the Fixed lines are back on the list: '+at);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('chat fixed notice ok');
}finally{await browser?.close();server.close()}
