import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add, scrolled far down the grid of sources: a tile's own view (a sign-in, a form, a run) is much
// shorter than the grid. It starts at its top, just under the top bar, with focus on it; the page never stays down where
// the grid was (only the footer showing). Back returns to the grid where it was, on the tile it left from.
// SHOTS=<folder> saves screenshots of the grid scrolled down and of each view right after the tap.
const dashboard=await dashboardPage();
const filler=Array.from({length:18},(_,n)=>({name:'src'+n,service:'src'+n,label:'Source '+(n+1),what:'Messages and activity from source '+(n+1)+'.',connected:0,broker:false,signin:'trello'}));
const sources=[...filler,
 {name:'trello',service:'trello',label:'Trello',what:'Card changes, comments and activity on one Trello board.',connected:0,broker:false,signin:'trello'},
 {name:'shortcut',service:'shortcut',label:'Shortcut',what:'Stories and comments in your Shortcut workspace.',connected:0,broker:false,form:{ask:[],secret:'Shortcut API token',scope:true,company:'Acme'}},
 {name:'google_meet',service:'google_meet',label:'Google Meet',what:'Transcripts and Gemini notes of your meetings.',connected:0,broker:false,signin:'google_meet'}];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:null,paired:true,pair_url:'https://app.example.org/account',sources}));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
// Where the view's heading sits against the top bar, and what has focus
const where=page=>page.evaluate(()=>{const box=document.querySelector('#connect-add'),h=box.querySelector('h3'),bar=document.querySelector('.topbar'),
 b=bar&&getComputedStyle(bar).display!=='none'?bar.getBoundingClientRect().bottom:0,r=h.getBoundingClientRect();
 return {top:r.top,bottom:r.bottom,bar:b,inner:innerHeight,focusIn:box.contains(document.activeElement),y:scrollY}});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,mobile,scheme] of [[390,844,true,'dark'],[390,844,true,'light'],[1440,900,false,'light'],[1440,700,false,'dark']]){
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}x${height}-${scheme}`;
  await page.goto(base+'/#connections=add');
  await page.locator('#connect-add [data-connect-signin="google_meet"]').waitFor();
  for(const [name,sel,heading] of [['google-meet','[data-connect-signin="google_meet"]','Google Meet'],['trello','[data-connect-signin="trello"]','Trello'],['shortcut','[data-connect="shortcut"]','Shortcut']]){
   // Far down the grid, the tile near the bottom of the screen
   await page.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));await page.waitForTimeout(200);
   const tile=page.locator('#connect-add '+sel);
   const gridY=await page.evaluate(()=>scrollY);
   if(height<=844)assert.ok(gridY>200,`${tag}: the grid is taller than the window (scrollY ${gridY})`);
   if(shots&&name!=='shortcut')await page.screenshot({path:`${shots}/${tag}-grid-scrolled.png`});
   if(mobile)await tile.tap();else await tile.click();
   await page.locator('#connect-add h3',{hasText:heading}).waitFor();
   // the place keeper and a late layout get their frames first
   await page.waitForTimeout(400);
   const w=await where(page);
   assert.ok(w.top>=w.bar-1,`${tag} ${name}: its heading is not under the top bar (${w.top} < ${w.bar})`);
   assert.ok(w.bottom<=w.inner*.5,`${tag} ${name}: its heading shows near the top (bottom ${w.bottom} of ${w.inner})`);
   assert.ok(w.focusIn,`${tag} ${name}: focus moved into the view`);
   if(shots&&name!=='shortcut')await page.screenshot({path:`${shots}/${tag}-${name}-open.png`});
   // Back: the grid where it was, on that tile
   await page.locator('#connect-add [data-connect-back]').first().click();
   await page.locator('#connect-add .connect-sources').waitFor();await page.waitForTimeout(300);
   const back=await page.evaluate(sel=>({y:scrollY,focused:document.activeElement===document.querySelector('#connect-add '+sel)}),sel);
   assert.ok(Math.abs(back.y-gridY)<=2,`${tag} ${name}: Back returns to where the grid was (${back.y} vs ${gridY})`);
   assert.ok(back.focused,`${tag} ${name}: Back puts focus on the tile it left from`)}
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('connect add scroll dashboard ok');
