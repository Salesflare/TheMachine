import assert from 'node:assert/strict';
import {mkdir,readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A trip's page, opened from its band in Calendar (#graph/note:<id>, graph-notes.js): Calendar as its way back, its
// name, kind and dates, and its lines in time order, each with the message it came from. Nothing to edit, and no Notes
// anywhere (no sidebar row, no New note). At 390 and 1440, light and dark, nothing wider than the screen.
// SHOTS=<folder> saves screenshots. Made-up data only.
const dashboard=await dashboardPage();
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const brand={'/brand/avatar.png':'app-icon-192.png','/brand/avatar-blink.png':'avatar-blink.png','/brand/favicon-32.png':'app-icon-192.png'};
const at=new Date().toISOString(),year=new Date().getFullYear();
const line=(id,when,text,from)=>({id,text,at:when,item:'',by:'machine',edited:false,event_id:100+id,fact_id:null,links:[],source:{id:100+id,kind:'gmail.message',title:text,occurred_at:at,from}});
const trip={id:'note:2',kind:'trip',name:'Lisbon',area:'personal',starts:`${year}-12-03`,ends:`${year}-12-06`,by:'machine',updated_at:at,created_at:at,renamed:false,owner_dates:false,dated:true,
 lines:[line(11,`${year}-12-03T07:10`,'Flight LX 2084 Brussels to Lisbon, seat 14A','Example Air'),line(12,`${year}-12-03`,'Hotel Example Garden, 3 nights','Hotel Example Garden'),
  line(13,`${year}-12-06T18:45`,'Flight LX 2087 Lisbon to Brussels','Example Air')],areas:[]};
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'&&url.searchParams.get('node')==='note:2'){res.end(JSON.stringify(trip));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({list_counts:{people:0,quiet:0,new:0,orgs:0,warmup:0,projects:0,projects_done:0},counts:{person:0,org:0,project:0},boards:[],board_suggestions:[]}));return}
 if(url.pathname==='/api/graph/list'){res.end(JSON.stringify({items:[],next:null,total:0}));return}
 if(brand[url.pathname]){res.setHeader('Content-Type','image/png');res.end(await readFile(new URL('../brand/'+brand[url.pathname],import.meta.url)));return}  // as machine/config.py serves it
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const [width,height] of [[1440,900],[390,844]]){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-GB',colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto(base+'#graph/note:2');const head=page.locator('.note-page h3');await head.waitFor();
  assert.equal(await head.textContent(),'Lisbon');
  assert.equal(await page.locator('.note-crumbs a').getAttribute('href'),'#calendar');
  assert.match(await page.locator('.note-page .detail-sub').textContent(),/^Trip · .+ · Kept up to date by The Machine$/);
  assert.deepEqual(await page.locator('.note-lines .note-src button').allTextContents(),['From Example Air','From Hotel Example Garden','From Example Air']);
  assert.equal(await page.locator('.note-page :is(form,[data-note-edit],[data-note-add],details)').count(),0,'nothing to edit');
  assert.equal(await page.locator('[data-graph-sub="notes"],[data-new-what="note"]').count(),0,'no Notes anywhere');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),width+': the page fits');
  await page.waitForFunction(()=>[...document.querySelectorAll('img[src="brand/avatar.png"]')].some(i=>i.offsetWidth&&i.complete&&i.naturalWidth>0));  // the logo, as served
  if(shots)await page.screenshot({path:`${shots}/trip-page-${width}-${scheme}.png`,fullPage:true});
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok trip page');
}finally{await browser?.close();server.close()}
