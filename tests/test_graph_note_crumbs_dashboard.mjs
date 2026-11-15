import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A note's breadcrumb shows its whole path, each level a link, and not its own title (the heading right under it):
// Graph › Notes › Kids on a wide screen, in place of the page head (one path), with the note's area still under it. A phone keeps it on one line, Notes › Kids, and folds the notes in between
// into a ⋯ menu (Notes › ⋯ › Activities), no › after the last crumb, with long names shortened, never wider than the screen. Browser back
// returns to the note it came from, and Notes goes back to the list.
const dashboard=(await dashboardPage()).replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__','s'.repeat(32));  // a crumb is a plain link: it opens under the page's base
const at=new Date().toISOString();
const LONG='After-school activities and the clubs they go to on weekdays';
const TITLE='Swimming lessons at the pool every Wednesday afternoon, with the kit list and the forms for the new term';
const row=(id,name,parent,depth,children=0,lines=0)=>({id,kind:'note',name,area:'personal',starts:null,ends:null,by:'machine',updated_at:at,parent,depth,children,lines});
const tree=[row('note:1','Kids',null,0,2),row('note:2','Doctors and care','note:1',1,0,2),row('note:3',LONG,'note:1',1,1),row('note:4',TITLE,'note:3',2,0,1)];
const paths={'note:1':[],'note:2':[{id:'note:1',name:'Kids'}],'note:3':[{id:'note:1',name:'Kids'}],'note:4':[{id:'note:1',name:'Kids'},{id:'note:3',name:LONG}]};
const page_=id=>({...tree.find(x=>x.id===id),path:paths[id],areas:[{id:'personal',label:'Personal'},{id:'work',label:'Work'}],created_at:at,renamed:false,owner_dates:false,dated:false,linked_from:[],tree,
 children:tree.filter(x=>x.parent===id),lines:[{id:1,text:'Example line',at:null,item:null,by:'machine',edited:false,event_id:null,fact_id:null,links:[],data:{}}]});
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'&&url.searchParams.has('node')){const id=url.searchParams.get('node');res.end(JSON.stringify(paths[id]?page_(id):{}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({list_counts:{people:0,quiet:0,new:0,orgs:0,warmup:0,projects:0,projects_done:0},counts:{person:0,org:0,project:0,note:4},boards:[],board_suggestions:[],notes:tree}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',errors=[];let browser;
// What a person sees of the breadcrumb: its visible links and … (in order), its height, and whether all of it fits
const seen=page=>page.evaluate(()=>{const c=document.querySelector('#people-view .note-crumbs'),box=c.getBoundingClientRect();
 const vis=el=>{const r=el.getBoundingClientRect();return r.width>2&&r.height>2&&getComputedStyle(el).visibility!=='hidden'};
 return {crumbs:[...c.querySelectorAll('a,summary')].filter(el=>vis(el)&&!el.closest('.fact-menu-list')).map(el=>el.textContent.trim()),height:Math.round(box.height),
  inside:[...c.querySelectorAll('a,summary')].filter(vis).every(el=>el.getBoundingClientRect().right<=innerWidth+0.5),fits:document.documentElement.scrollWidth<=innerWidth,
  here:vis(c.querySelector('[aria-current="page"]')),seps:[...c.querySelectorAll('span[aria-hidden]')].filter(el=>vis(el)&&!el.closest('.crumb-here')).length,title:document.querySelector('#people-view .note-page h3').textContent,
  titleWhole:(h=>h.scrollWidth<=h.clientWidth+1)(document.querySelector('#people-view .note-page h3')),tab:document.title,
  head:vis(document.querySelector('#page-head')),sub:document.querySelector('#people-view .note-page .detail-sub')?.textContent||''}});
const open=async(page,id,title)=>{await page.goto(base+'#graph/'+encodeURIComponent(id));await page.locator('#people-view .note-page h3',{hasText:title.slice(0,20)}).waitFor()};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){const mobile=width<600,tag=String(width);
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(tag+': '+e.message));
  // Two levels deep: the path up to the note it is under, and the note's title once, as the heading
  await open(page,'note:2','Doctors and care');let s=await seen(page);
  assert.deepEqual(s.crumbs,mobile?['Notes','Kids']:['Graph','Notes','Kids'],tag+': '+JSON.stringify(s));
  assert.equal(s.seps,s.crumbs.length-1,tag+': a › between crumbs, none after the last');
  assert.ok(!s.here&&s.title==='Doctors and care'&&s.tab.includes('Doctors and care'),tag+': the title shows once, as the heading, and names the tab');
  assert.ok(!s.head,tag+': the trail takes the page head\'s place: the path shows once');
  assert.equal(s.sub,'Personal · Kept up to date by The Machine',tag+': the area still shows');
  assert.ok(s.fits&&s.inside,tag+': fits');if(mobile)assert.ok(s.height<=48,tag+': one line '+s.height);
  // Deeper, with long names: a wide screen shows every level; a phone folds the middle into … and shortens the rest
  await open(page,'note:4',TITLE);s=await seen(page);
  assert.deepEqual(s.crumbs,mobile?['Notes','⋯',LONG]:['Graph','Notes','Kids',LONG],tag+': '+JSON.stringify(s.crumbs));
  assert.equal(s.seps,s.crumbs.length-1,tag+': a › between crumbs, none after the last');
  assert.ok(s.fits&&s.inside&&s.titleWhole,tag+': nothing wider than the screen, and the long title shows whole');
  if(mobile){assert.ok(s.height<=48,tag+': one line '+s.height);
   await page.locator('.note-crumbs .crumb-fold summary').click();
   const menu=page.locator('.note-crumbs .crumb-fold .fact-menu-list a');assert.deepEqual(await menu.allTextContents(),['Kids']);
   assert.ok(await page.evaluate(()=>{const r=document.querySelector('.note-crumbs .crumb-fold .fact-menu-list').getBoundingClientRect();return r.left>=0&&r.right<=innerWidth}),tag+': the menu stays on screen');
   await menu.first().click();await page.locator('#people-view .note-page h3',{hasText:'Kids'}).waitFor();
   assert.equal(new URL(page.url()).hash,'#graph/note%3A1');
   await page.goBack();await page.locator('#people-view .note-page h3',{hasText:TITLE.slice(0,20)}).waitFor()}
  // The note it is under, then back
  await page.locator('.note-crumbs a.note-up').click();await page.locator('#people-view .note-page h3',{hasText:LONG.slice(0,20)}).waitFor();
  assert.equal(new URL(page.url()).hash,'#graph/note%3A3',tag);
  await page.goBack();await page.locator('#people-view .note-page h3',{hasText:TITLE.slice(0,20)}).waitFor();
  assert.equal(new URL(page.url()).hash,'#graph/note%3A4',tag+': back returns to the note');
  // Notes: the list
  await page.locator('.note-crumbs a[data-crumb="notes"]').click();await page.locator('[data-graph-panel="notes"]:not([hidden])').waitFor();
  assert.equal(errors.filter(e=>e.startsWith(tag+':')).length,0,tag+': no page errors');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok note breadcrumbs');
}finally{await browser?.close();server.close()}
