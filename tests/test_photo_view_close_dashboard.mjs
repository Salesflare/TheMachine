import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import zlib from 'node:zlib';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// An image opened large (events-photos.js): its × reads in both themes, at rest, hovered, pressed and with the focus
// ring, over a light image, a dark image and the black backdrop (it lies half over the image's corner), and takes a
// 44 px tap. In dark mode it was near-black on a dark circle: its color was a token the page doesn't have. A picture
// that can't load shows its words, which read on their white too. Made-up images.
// SHOT_DIR=<folder> also saves screenshots; DASHBOARD=<file> runs another dashboard.html (for before shots).
const dashboard=await dashboardPage(process.env.DASHBOARD),SHOTS=process.env.SHOT_DIR;
const png=(w,h,rgb)=>{const raw=Buffer.alloc((w*3+1)*h);for(let y=0;y<h;y++)for(let x=0;x<w;x++)raw.set(rgb,y*(w*3+1)+1+x*3);
 const chunk=(t,d)=>{const l=Buffer.alloc(4),c=Buffer.alloc(4),td=Buffer.concat([Buffer.from(t),d]);l.writeUInt32BE(d.length);c.writeUInt32BE(zlib.crc32(td));return Buffer.concat([l,td,c])};
 const head=Buffer.alloc(13);head.writeUInt32BE(w,0);head.writeUInt32BE(h,4);head.set([8,2,0,0,0],8);
 return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',head),chunk('IDAT',zlib.deflateSync(raw)),chunk('IEND',Buffer.alloc(0))])};
// light and dark: an ordinary picture; small: a thumbnail of one; tall: up to the edges it may have; gone: doesn't load
const IMAGES={light:png(700,620,[250,250,247]),dark:png(700,620,[16,17,20]),small:png(90,60,[250,250,247]),tall:png(390,1400,[250,250,247]),gone:null};
const names=Object.keys(IMAGES),idOf=n=>'cf_'+String(names.indexOf(n)+1).padStart(20,'0');
const card={id:'c1'.repeat(8),title:'Check the venue quote',body:'It came with pictures.',status:'pending',scope:'work',created_at:new Date().toISOString(),event_ids:[2],
 files:names.map(n=>({id:idOf(n),name:'The '+n+' picture.png',type:'image/png',size:2000}))};
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/chat-file'){const image=IMAGES[names.find(n=>idOf(n)===url.searchParams.get('id'))];
  if(!image){res.statusCode=404;res.end();return}res.setHeader('Content-Type','image/png');res.end(image);return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
// What the button looks like now, as plain numbers: colors as [r,g,b,a], whatever way the browser writes them
const look=page=>page.evaluate(()=>{const c=document.createElement('canvas').getContext('2d',{willReadFrequently:true});
 const rgba=v=>{c.clearRect(0,0,1,1);c.fillStyle=v;c.fillRect(0,0,1,1);return [...c.getImageData(0,0,1,1).data]};
 const b=document.querySelector('#wa-photo-view .wa-photo-close'),s=getComputedStyle(b),r=b.getBoundingClientRect();
 // how far from its middle a tap still lands on it
 const at=(x,y)=>b.contains(document.elementFromPoint(x,y)),x=r.x+r.width/2,y=r.y+r.height/2;
 return {color:rgba(s.color),back:rgba(s.backgroundColor),edge:parseFloat(s.borderTopWidth)?rgba(s.borderTopColor):null,opacity:+s.opacity,
  outline:s.outlineStyle==='none'||!parseFloat(s.outlineWidth)?null:rgba(s.outlineColor),
  shadow:s.boxShadow==='none'?[]:(s.boxShadow.match(/(?:rgba?|color)\([^)]*\)/g)||[]).map(rgba),
  box:[r.x,r.y,r.right,r.bottom],hit:[[-21,0],[21,0],[0,-21],[0,21]].every(([dx,dy])=>at(x+dx,y+dy))}});
const lum=([r,g,b])=>{const f=v=>(v/=255)<=.04045?v/12.92:((v+.055)/1.055)**2.4;return .2126*f(r)+.7152*f(g)+.0722*f(b)};
const contrast=(a,b)=>{const [x,y]=[lum(a),lum(b)].sort((m,n)=>n-m);return (x+.05)/(y+.05)};
// What can lie under the button: a light image, a dark image, the backdrop
const UNDER={light:[255,255,255],dark:[16,17,20],backdrop:[4,4,4]};
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const colorScheme of ['dark','light']){
  const phone=width<600,context=await browser.newContext({viewport:{width,height},colorScheme,locale:'en-US',isMobile:phone,hasTouch:phone});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.locator('#task-'+card.id).waitFor();
  assert.equal(await page.evaluate(()=>document.documentElement.dataset.theme||(matchMedia('(prefers-color-scheme:light)').matches?'light':'dark')),colorScheme);
  const thumb=n=>page.locator(`#task-${card.id} button.wa-photo[data-photo$="${idOf(n)}"]`),view=page.locator('#wa-photo-view'),close=view.locator('.wa-photo-close');
  for(const name of names){
   const tag=`${name}-${width}-${colorScheme}`;
   const shot=async state=>{if(SHOTS)await page.screenshot({path:`${SHOTS}/${tag}-${state}.png`})};
   const reads=(state,s)=>{const is=`${tag} ${state}: ${JSON.stringify(s)}`;
    assert.equal(s.opacity,1,is);assert.equal(s.back[3],255,'a solid circle, so what lies under never shows through: '+is);
    assert.ok(contrast(s.color,s.back)>=4.5,`the cross on its circle (${contrast(s.color,s.back).toFixed(2)}): `+is);
    for(const [under,rgb] of Object.entries(UNDER))assert.ok(Math.max(contrast(s.back,rgb),s.edge?contrast(s.edge,rgb):0)>=3,`the circle's edge on the ${under}: `+is)};
   const shown=()=>page.waitForFunction(gone=>{const i=document.querySelector('#wa-photo-view[open] img');return i&&i.complete&&(gone||i.naturalWidth)},name==='gone');
   await thumb(name).click();await shown();await page.mouse.move(2,height-2);await shot('rest');
   // At rest, whole on the screen, with room for a thumb
   let s=await look(page);reads('rest',s);
   assert.ok(s.box[0]>=0&&s.box[1]>=0&&s.box[2]<=width&&s.box[3]<=height,`${tag} on the screen: ${s.box}`);
   assert.ok(s.hit,tag+': a tap up to 21 px from its middle lands on it');
   if(phone)assert.ok(s.box[2]-s.box[0]>=44&&s.box[3]-s.box[1]>=44,`${tag} 44 px: ${s.box}`);
   // The words of one that can't load, on its white
   const words=await view.locator('img').evaluate(i=>{const s=getComputedStyle(i);return [s.color,s.backgroundColor].map(v=>v.match(/[\d.]+/g).map(Number))});
   assert.ok(contrast(...words)>=4.5,`${tag} its words: ${JSON.stringify(words)}`);
   // Hovered, then pressed (the colors ease in)
   const settled=()=>close.evaluate(b=>Promise.all(b.getAnimations().map(a=>a.finished)));
   if(!phone){await close.hover();await settled();await shot('hover');reads('hover',await look(page));
    await page.mouse.down();await settled();await shot('pressed');reads('pressed',await look(page));
    await page.mouse.move(2,height-2);await page.mouse.up()}
   if(!await view.evaluate(d=>d.open))await thumb(name).click();
   // By keyboard: a ring that shows on light and on dark
   await page.keyboard.press('Escape');await view.waitFor({state:'hidden'});await thumb(name).focus();await page.keyboard.press('Enter');await shown();
   await page.keyboard.press('Tab');await close.focus();await settled();
   assert.ok(await close.evaluate(b=>b.matches(':focus-visible')),tag);await shot('focus');
   s=await look(page);reads('focus',s);const ring=[s.outline,...s.shadow].filter(c=>c?.[3]===255);
   for(const [under,rgb] of Object.entries(UNDER))assert.ok(ring.some(c=>contrast(c,rgb)>=3),`${tag} the focus ring on the ${under}: ${JSON.stringify(s)}`);
   // The × closes it
   await close.click();assert.equal(await view.evaluate(d=>d.open),false)}
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok photo view close');
}finally{await browser?.close();server.close()}
