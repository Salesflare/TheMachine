import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The to-do chat's header: the back chevron sits on the title's center line, not below it, as the eye sees it. Measured on
// the pixels, with the page's own font (Inter, served as the service serves it), on a phone and a computer, light and dark:
// a screenshot of the header is read back through a canvas, and the chevron's ink center (its top and bottom inked rows)
// is at most 0.5px from the center of the title's first capital (cap height to baseline). Boxes and line boxes don't
// count: they carry the font's ascent and descent, which browsers round differently. ⋯ is on the chevron's line.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),ID='c1c1c1c1c1c1c1c1',j=JSON.stringify;
const cards=[{id:ID,title:'Check and charge the balance of the account',body:'b',status:'prepared',scope:'work',created_at:now,event_ids:[1]},
 {id:'c2c2c2c2c2c2c2c2',title:'Renew the passport',body:'b',status:'pending',scope:'personal',created_at:now,event_ids:[2]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const brand={'/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(brand[url.pathname]){res.setHeader('Content-Type','font/woff2');res.end(await readFile(new URL('../'+brand[url.pathname],import.meta.url)));return}
 if(url.pathname==='/api/status'){res.end(j(state()));return}
 if(url.pathname==='/api/action'&&JSON.parse(body||'{}').action==='card_chat'){res.end(j({session:true,status:'ok',active:false,cursor:'k',items:[{kind:'reply',text:'Done it.',at:Date.now()-60000}]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]])for(const theme of ['light','dark']){
  const phone=width<500,context=await browser.newContext({viewport:{width,height},deviceScaleFactor:phone?3:1,isMobile:phone,hasTouch:phone,colorScheme:theme,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.addInitScript(t=>{try{localStorage.setItem('theme',t)}catch{}},theme);
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#chat='+ID);await page.locator('h2.chat-title').waitFor();
  await page.evaluate(()=>document.fonts.ready);
  const m=await page.evaluate(()=>{const q=s=>document.querySelector(s),t=q('.chat-title'),g=document.createRange(),R=n=>n.getBoundingClientRect();
   g.setStart([...t.childNodes].find(n=>n.nodeType===3),0);g.setEnd(g.startContainer,1);const f=g.getBoundingClientRect(),a=R(q('.chat-back svg')),d=R(q('.chat-menu>summary svg'));
   return {inter:document.fonts.check('600 16px Inter'),theme:document.documentElement.dataset.theme,letter:[f.left,f.right],arrow:[a.left,a.right],top:a.top-6,height:a.height+12,menu:d.top+d.height/2-(a.top+a.height/2),fade:t.classList.contains('fade')}});
  const s=phone?3:1,clip={x:m.arrow[0]-4,y:m.top,width:m.letter[1]-m.arrow[0]+8,height:m.height};
  const png=await page.screenshot({clip,scale:'device'});
  const ink=await page.evaluate(async({src,regions})=>{const img=new Image();img.src=src;await img.decode();const c=document.createElement('canvas');c.width=img.width;c.height=img.height;
   const g=c.getContext('2d');g.drawImage(img,0,0);const d=g.getImageData(0,0,c.width,c.height).data,px=(x,y)=>{const i=(y*c.width+x)*4;return [d[i],d[i+1],d[i+2]]},out={};
   for(const [name,[x0,x1]] of Object.entries(regions)){const bg=px(0,0),cov=[];
    for(let y=0;y<c.height;y++){let v=0;for(let x=Math.max(0,Math.floor(x0));x<Math.min(c.width,Math.ceil(x1));x++){const p=px(x,y);v=Math.max(v,Math.abs(p[0]-bg[0])+Math.abs(p[1]-bg[1])+Math.abs(p[2]-bg[2]))}cov.push(v)}
    const max=Math.max(...cov),n=cov.map(v=>v/max),rows=n.flatMap((v,i)=>v>0.06?[i]:[]),a=rows[0],b=rows.at(-1);
    out[name]=((a+1-n[a])+(b+n[b]))/2}  // the inked rows' middle, the edge rows counted by how much ink they carry
   return out},{src:'data:image/png;base64,'+png.toString('base64'),regions:{arrow:[(m.arrow[0]-clip.x)*s,(m.arrow[1]-clip.x)*s],cap:[(m.letter[0]-clip.x)*s+0.5,(m.letter[1]-clip.x)*s-0.5]}});
  const at=`${width} ${theme}: ${j({...m,ink})}`,off=(ink.arrow-ink.cap)/s;
  assert.ok(m.inter,'the page has its own font: '+at);assert.equal(m.theme,theme);
  assert.ok(Math.abs(off)<=0.5,`the back chevron's ink is on the title's capitals' center line (${off.toFixed(2)}px): `+at);
  assert.ok(Math.abs(m.menu)<=0.5,'⋯ is on the same line: '+at);
  if(!phone)assert.equal(m.fade,false,'a title that fits does not fade (its trimmed box is no reason to): '+at);
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
