import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's chips show who and which organization it is about with their photo or logo when the Graph has one
// (enrichment.node_picture): a photo only when saved on this Machine, a logo also as an https link. A photo is a round,
// cover-cropped circle with a ring; a logo sits on a white tile. Without one, with any other link, when it fails to load,
// or when a logo wouldn't read this small (white on transparent, a wide wordmark), the chip shows the initials instead,
// never a broken image. A picture never makes the chip taller.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const PHOTO='api/person-photo?p='+'a'.repeat(32),LOGO='api/person-photo?p='+'b'.repeat(32),GONE='api/person-photo?p='+'c'.repeat(32);
const svg=body=>`<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">${body}</svg>`;
const PICS={a:svg('<rect width="200" height="200" fill="#c9b8a6"/><circle cx="100" cy="80" r="40" fill="#7a5c48"/>'),
 b:svg('<circle cx="100" cy="100" r="70" fill="#f59e0b"/><circle cx="100" cy="100" r="30" fill="#fff"/>')};
const REMOTE={'/white.svg':svg('<path d="M40 150 100 40l60 110z" fill="none" stroke="#fff" stroke-width="16"/>'),
 '/wide.svg':'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="110"><rect width="480" height="110" fill="#0f766e"/></svg>',
 '/app.svg':svg('<rect width="200" height="200" fill="#2563eb"/><path d="M60 140 100 55l40 85" fill="none" stroke="#fff" stroke-width="18"/>')};
const card=(id,person,extra)=>({id,title:'Answer the quote question '+id.slice(0,2),body:'They asked about the quote.',status:'pending',created_at:now,event_ids:[1],
 people:[person],source_line:'Source: Email',scope:'work',...extra});
const org=(id,name,logo)=>({org_said:true,org_node:{id:'org:'+id,name,logo}});
const cards=[
 card('a1a1a1a1a1a1a1a1',{id:'email:lee@brushworks.example',name:'Lee Example',photo:PHOTO},org('brushworks.example','Brushworks',LOGO)),
 card('b1b1b1b1b1b1b1b1',{id:'email:pat@bigcorp.example',name:'Pat Example',photo:GONE},org('bigcorp.example','Bigcorp','https://logos.test/white.svg')),
 card('c1c1c1c1c1c1c1c1',{id:'email:kim@globex.example',name:'Kim Example',photo:'https://media.invalid/k.jpg'},org('globex.example','Globex','javascript:alert(1)')),
 card('d1d1d1d1d1d1d1d1',{id:'email:ash@wideco.example',name:'Ash Example'},org('wideco.example','Wideco','https://logos.test/wide.svg')),
 card('e1e1e1e1e1e1e1e1',{id:'email:jo@appco.example',name:'Jo Example'},org('appco.example','Appco','https://logos.test/app.svg'))];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/person-photo'){const p=PICS[url.searchParams.get('p')[0]];if(!p){res.statusCode=404;res.end();return}res.setHeader('Content-Type','image/svg+xml');res.end(p);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{pending:cards.length},decisions:[],analyses:[],deliveries:[],
  review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,scheme] of [[1280,'light'],[390,'dark']]){
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme});
  const outside=[],remote=[];
  await context.route('**/*',route=>{const u=new URL(route.request().url());
   if(u.hostname==='logos.test'){remote.push({path:u.pathname,referer:route.request().headers()['referer']});return route.fulfill({status:200,contentType:'image/svg+xml',headers:{'Access-Control-Allow-Origin':'*'},body:REMOTE[u.pathname]})}
   if(u.hostname==='127.0.0.1')return route.continue();outside.push(u.hostname);return route.abort()});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
  const chip=(id,isOrg)=>page.locator(`#task-${id} .card-badges a.chip.who${isOrg?'.org':':not(.org)'}`);
  // Settled: every chip picture loaded or taken off
  await page.waitForFunction(()=>[...document.querySelectorAll('.card-badges .chip-av img')].every(i=>i.complete&&i.naturalWidth>0)&&!document.querySelector('#task-b1b1b1b1b1b1b1b1 .chip-av img'));
  const pic=async(id,isOrg)=>{const c=chip(id,isOrg);return {img:await c.locator('.chip-av img').count()?await c.locator('.chip-av img').getAttribute('src'):null,
   text:await c.locator('.chip-av').getAttribute('data-i'),h:Math.round((await c.boundingBox()).height),broken:await c.locator('img').evaluateAll(l=>l.some(i=>!i.naturalWidth))}};
  const lee=await pic('a1a1a1a1a1a1a1a1'),brush=await pic('a1a1a1a1a1a1a1a1',true);
  assert.equal(lee.img,PHOTO);assert.equal(brush.img,LOGO);
  const look=await chip('a1a1a1a1a1a1a1a1').locator('.chip-av').evaluate(s=>{const i=s.querySelector('img'),r=s.getBoundingClientRect(),cs=getComputedStyle(i);
   return {w:r.width,h:r.height,round:getComputedStyle(s).borderRadius,fit:cs.objectFit,clip:getComputedStyle(s).overflow,ring:getComputedStyle(s,'::after').boxShadow}});
  assert.equal(look.w,look.h);assert.equal(look.round,'50%');assert.equal(look.fit,'cover');assert.equal(look.clip,'hidden');assert.ok(look.ring.includes('inset'),look.ring);
  assert.equal(await chip('a1a1a1a1a1a1a1a1',true).locator('img').evaluate(i=>getComputedStyle(i).objectFit),'contain');
  const pat=await pic('b1b1b1b1b1b1b1b1'),big=await pic('b1b1b1b1b1b1b1b1',true);
  assert.deepEqual([pat.img,pat.text],[null,'PE']);  // the photo failed: their initials
  assert.deepEqual([big.img,big.text],[null,'B']);  // white on transparent doesn't read: the initial
  const kim=await pic('c1c1c1c1c1c1c1c1'),globex=await pic('c1c1c1c1c1c1c1c1',true);
  assert.deepEqual([kim.img,kim.text],[null,'KE']);  // a photo link from elsewhere is never loaded
  assert.deepEqual([globex.img,globex.text],[null,'G']);
  assert.deepEqual([(await pic('d1d1d1d1d1d1d1d1',true)).img,(await pic('d1d1d1d1d1d1d1d1')).text],[null,'AE']);  // a wide wordmark: the initial
  const app=await pic('e1e1e1e1e1e1e1e1',true);
  assert.equal(app.img,'https://logos.test/app.svg');  // an app icon fills its tile, no padding
  assert.equal(await chip('e1e1e1e1e1e1e1e1',true).locator('img').evaluate(i=>i.classList.contains('bleed')),true);
  for(const p of [lee,brush,pat,big,kim,globex,app])assert.equal(p.broken,false);
  assert.equal(new Set([lee.h,brush.h,pat.h,big.h,kim.h,globex.h,app.h]).size,1);  // a picture never makes the chip taller
  assert.ok(remote.length&&remote.every(r=>!r.referer),JSON.stringify(remote));
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  assert.ok(!outside.includes('media.invalid'));
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('To-dos: who and which organization show a crisp photo or logo, else their initials.');
}finally{await browser?.close();server.close()}
