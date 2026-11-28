import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Every dialog's ×, the ones built only when opened too: it reads (4.5) in both themes, and on a phone takes a 44 px tap
// (shell-sheets.js) that reaches no other control: every point of that reach that isn't the × itself holds none.
// SHOT_DIR=<folder> also saves screenshots; DASHBOARD=<file> runs another dashboard.html.
const dashboard=await dashboardPage(process.env.DASHBOARD),SHOTS=process.env.SHOT_DIR;
const state={suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}};
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end(url.pathname==='/api/status'?JSON.stringify(state):'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
// The dialogs that have their own opener or title row, as the app draws them. Any other dialog of the page that is
// drawn from data gets the shared title row with a field right under it, the closest a control ever comes.
const OPEN={'keys-sheet':()=>keysShow(),'new-card':()=>ncOpen(),'help-panel':()=>helpOpen(),
 'whats-new':()=>whatsNewOpen({entries:[{art:'mail',title:'Ask anything',text:'Find an answer in your messages.'},{title:'Export',text:'Take it with you.'}]}),
 'memory-import':()=>{setHTML(miDialog(),html`${miHead('Bring in what it knows')}<textarea></textarea>`)},
 'crm-dialog':()=>{setHTML(document.querySelector('#crm-form'),html`${crmHead('Import')}<input>`)},
 'project-dialog':()=>{setHTML(document.querySelector('#project-form'),html`${pjHead('New project')}<input>`)},
 'split-dialog':()=>{setHTML(document.querySelector('#split-form'),html`${splHead('Split')}<input>`)}};
const LATER=['ms-share','area-digest','login-import'];
const look=(page,id)=>page.evaluate(id=>{const d=document.getElementById(id),x=d.querySelector('.snooze-heading>button:last-child,.wn-x'),r=x.getBoundingClientRect();
 const cv=document.createElement('canvas').getContext('2d',{willReadFrequently:true});
 const over=list=>{cv.clearRect(0,0,1,1);for(const v of list){cv.fillStyle=v;cv.fillRect(0,0,1,1)}return [...cv.getImageData(0,0,1,1).data].slice(0,3)};
 const back=[];for(let e=x;e;e=e.parentElement)back.unshift(getComputedStyle(e).backgroundColor);
 const cx=r.x+r.width/2,cy=r.y+r.height/2,reach={x:0,y:0},others=new Set();
 const at=(px,py)=>{const e=document.elementFromPoint(px,py);return e===x};
 // the tap's reach, sideways and up and down, through the middle
 for(let i=-40;i<=40;i++){if(at(cx+i,cy))reach.x++;if(at(cx,cy+i))reach.y++}
 // what else is a control and touches that reach
 const a=getComputedStyle(x,'::after'),p=n=>a.content==='none'?0:-parseFloat(a[n]);
 const box={l:r.left-p('left'),t:r.top-p('top'),r:r.right+p('right'),b:r.bottom+p('bottom')};
 for(const e of d.querySelectorAll('button,a[href],input,select,textarea,summary,[contenteditable],[tabindex],label')){if(e===x||!e.getClientRects().length)continue;
  const q=e.getBoundingClientRect();if(q.left<box.r&&q.right>box.l&&q.top<box.b&&q.bottom>box.t)others.add(e.outerHTML.slice(0,90))}
 return {color:over([...back,getComputedStyle(x).color]),back:over(back),reach,others:[...others],on:box.l>=0&&box.t>=0&&box.r<=innerWidth}},id);
const lum=([r,g,b])=>{const f=v=>(v/=255)<=.04045?v/12.92:((v+.055)/1.055)**2.4;return .2126*f(r)+.7152*f(g)+.0722*f(b)};
const contrast=(a,b)=>{const [x,y]=[lum(a),lum(b)].sort((m,n)=>n-m);return (x+.05)/(y+.05)};
const errors=[],wrong=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const colorScheme of ['dark','light']){
  const phone=width<600,context=await browser.newContext({viewport:{width,height},colorScheme,locale:'en-US',isMobile:phone,hasTouch:phone,reducedMotion:'reduce'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.waitForFunction(()=>document.querySelector('#phone-sheets'));
  const ids=await page.evaluate(later=>{for(const id of later)if(!document.getElementById(id))document.body.append(Object.assign(document.createElement('dialog'),{id}));
   return [...document.querySelectorAll('dialog[id]')].map(d=>d.id).filter(id=>!['palette','wa-photo-view','share-consent'].includes(id))},LATER);
  const all=[...new Set([...ids,...Object.keys(OPEN)])];assert.ok(all.length>25,'the dialogs of the page: '+all);
  for(const id of all){
   if(OPEN[id])await page.evaluate(OPEN[id]);
   await page.evaluate(id=>{const d=document.getElementById(id);if(!d.parentElement.offsetParent&&d.parentElement!==document.body)document.body.append(d);  // one in a page that isn't shown
    if(!d.querySelector('.snooze-heading,.wn-x')){const f=d.querySelector('form')||d;f.innerHTML='<div class="snooze-heading"><h2>A title</h2><button type="button" aria-label="Close">×</button></div><label class="ed-field">Name<input></label>'}
    for(const e of d.querySelectorAll('#peek-stop'))e.hidden=false;
    if(!d.open)d.showModal();d.scrollTop=0},id);
   await page.mouse.move(2,height-2);await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
   const s=await look(page,id),tag=`${id} ${width} ${colorScheme} ${JSON.stringify(s)}`;
   if(process.env.LIST)console.log(id.padEnd(16),width,colorScheme.padEnd(5),contrast(s.color,s.back).toFixed(2),`${s.reach.x}x${s.reach.y}`,s.others.join(' '));
   if(contrast(s.color,s.back)<4.5)wrong.push('reads: '+tag);
   if(phone&&(s.reach.x<44||s.reach.y<44))wrong.push('44 px: '+tag);
   if(s.others.length||!s.on)wrong.push('room: '+tag);
   if(SHOTS)await page.screenshot({path:`${SHOTS}/close-${id}-${width}-${colorScheme}.png`});
   await page.evaluate(id=>document.getElementById(id).close(),id)}
  await context.close()}
 assert.deepEqual(wrong,[],'\n'+wrong.join('\n'));
 assert.deepEqual(errors,[]);
 console.log('ok dialog close reach');
}finally{await browser?.close();server.close()}
