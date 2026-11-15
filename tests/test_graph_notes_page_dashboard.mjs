import assert from 'node:assert/strict';
import {mkdir,readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A note's written page (note_writer.py): a summary and short sections above its lines, each bullet ending in the
// numbers of the lines it stands on; a number goes to that line, and the lines are numbered as Sources. The Notes list
// shows a page's summary under the note's name, and a folder's overview (folder_overview.py) under the folder's; the
// folder's page shows that overview, each sentence naming the notes under it it stands on, each a link. At 390 and 1440, light and dark, nothing wider than the screen.
// SHOTS=<folder> saves screenshots. Made-up data only.
const dashboard=await dashboardPage();
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const brand={'/brand/avatar.png':'app-icon-192.png','/brand/avatar-blink.png':'avatar-blink.png','/brand/favicon-32.png':'app-icon-192.png'};
const at=new Date().toISOString(),year=new Date().getFullYear();
const note=(n,name,depth,parent,children=0,lines=0,about)=>({id:'note:'+n,kind:n===2?'topic':'note',name,area:'work:Example',starts:null,ends:null,by:n===2?'machine':'owner',updated_at:at,lines,parent,depth,children,...(about?{about}:{})});
const WORK='The office move is on track for the end of January, with only the movers’ date left. Two designer profiles wait for your pick.';
const overview={summary:{text:WORK,sources:[{id:'note:2',name:'Office move'},{id:'note:3',name:'Hiring a designer'}]},
 now:[{text:'Give Example Movers a Saturday before 20 January.',sources:[{id:'note:2',name:'Office move'}]},{text:'Pick one of the two designer profiles Ana sent on Monday.',sources:[{id:'note:3',name:'Hiring a designer'}]}],at};
const notes=[note(1,'Work',0,null,2,0,WORK),note(2,'Office move',1,'note:1',0,4,'Moving the team to the new office on Example Street by the end of January. The lease is signed; the movers still need a date.'),
 note(3,'Hiring a designer',1,'note:1',0,2),note(4,'Home',0,null,0,3)];
const line=(id,day,text,from)=>({id,text,at:`${day.startsWith('12')?year-1:year}-${day}`,item:'conversation',by:'machine',edited:false,event_id:100+id,fact_id:null,links:[],source:{id:100+id,kind:'gmail.message',title:text,occurred_at:`${year}-${day}T09:00:00Z`,from}});
const lines=[line(11,'01-14','Office move: the movers’ quote','Example Movers'),line(12,'01-09','Lease for Example Street, signed','Example Realty'),
 line(13,'01-06','Desks and chairs for the new office','Example Furniture'),line(14,'12-18','Office move: options','Ana Ramos')];
const page={summary:{text:'Moving the team to the new office on Example Street by the end of January. The lease is signed; the movers still need a date.',sources:[12,11]},
 facts:[{text:'The new office is at 12 Example Street, second floor, for 18 people.',sources:[12]},{text:'Example Movers quoted €2,400 for a Saturday move.',sources:[11]}],
 decisions:[{text:'Ana picked Example Street over the two other options.',sources:[14]}],
 open:[{text:'You owe Example Movers a moving date; they hold Saturdays until 20 January.',sources:[11]},{text:'Desks: waiting on Example Furniture’s delivery date.',sources:[13]}],
 timeline:[{date:`${year-1}-12-18`,text:'Ana sent three office options.',sources:[14]},{date:`${year}-01-09`,text:'Lease signed for Example Street.',sources:[12]},{date:`${year}-01-14`,text:'Movers sent their quote.',sources:[11]}],at};
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'&&url.searchParams.has('node')){const x=notes.find(n=>n.id===url.searchParams.get('node'));const own=x.id==='note:2';
  res.end(JSON.stringify({...x,lines:own?lines:[],path:x.parent?[{id:x.parent,name:'Work'}]:[],created_at:at,renamed:false,owner_dates:false,dated:false,children:notes.filter(c=>c.parent===x.id),linked_from:[],tree:notes,...(own?{page}:{}),...(x.id==='note:1'?{overview}:{})}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({list_counts:{people:0,quiet:0,new:0,orgs:0,warmup:0,projects:0,projects_done:0},counts:{person:0,org:0,project:0},boards:[],board_suggestions:[],notes}));return}
 if(url.pathname==='/api/graph/list'){res.end(JSON.stringify({items:[],next:null,total:0}));return}
 if(brand[url.pathname]){res.setHeader('Content-Type','image/png');res.end(await readFile(new URL('../brand/'+brand[url.pathname],import.meta.url)));return}  // as machine/config.py serves it
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const [width,height] of [[1440,900],[390,844]]){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-GB',colorScheme:scheme}),page_=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page_.on('pageerror',e=>errors.push(width+': '+e.message));
  // The list: the summary under the name, two lines at most
  await page_.goto(base+'#graph=notes');await page_.locator('[data-note-fold="note:1"]').click();
  const about=page_.locator('.note-item[data-node="note:2"] .note-about');await about.waitFor();
  assert.match(await about.textContent(),/^Moving the team/);
  assert.ok(await about.evaluate(e=>e.getBoundingClientRect().height<=parseFloat(getComputedStyle(e).lineHeight)*2+1),width+': two lines at most');
  assert.equal(await page_.locator('.note-item[data-node="note:3"] .note-about').count(),0,'no page: no summary');
  assert.match(await page_.locator('.note-item[data-node="note:1"] .note-about').textContent(),/^The office move is on track/,'a folder: its overview');
  assert.ok(await page_.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),width+': the list fits');
  await page_.waitForFunction(()=>[...document.querySelectorAll('img[src="brand/avatar.png"]')].some(i=>i.offsetWidth&&i.complete&&i.naturalWidth>0));  // the logo, as served
  if(shots)await page_.screenshot({path:`${shots}/notes-list-${width}-${scheme}.png`});
  // The page: summary, sections in order, numbered sources
  await page_.goto(base+'#graph/note:2');const written=page_.locator('.note-written');await written.waitFor();
  assert.deepEqual(await written.locator('h4').allTextContents(),['Key facts','Decisions','Open items','Timeline','Sources']);
  assert.deepEqual(await page_.locator('.note-summary .note-cite').allTextContents(),['2','1'],'the summary cites lines 2 and 1');
  assert.deepEqual(await page_.locator('.note-lines .note-num').allTextContents(),['1','2','3','4']);
  assert.equal(await page_.locator('.note-timeline time').count(),3);
  assert.ok(await page_.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),width+': the page fits');
  if(shots)await page_.screenshot({path:`${shots}/note-page-${width}-${scheme}.png`,fullPage:true});
  // A number goes to its line
  await page_.locator('.note-bullets .note-cite[data-note-cite="13"]').click();
  await page_.waitForFunction(()=>document.querySelector('#note-line-13')?.classList.contains('note-flash'));
  await page_.waitForFunction(()=>{const r=document.querySelector('#note-line-13').getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight},null,{timeout:3000});  // the line is in view
  // A folder: its overview names the notes under it, each a link to that note, and no "Nothing in this note yet"
  await page_.goto(base+'#graph/note:1');const over=page_.locator('.note-overview');await over.waitFor();
  assert.equal(await over.locator('.note-summary').evaluate(e=>e.firstChild.textContent),WORK);
  assert.deepEqual(await over.locator('.note-summary .note-cite-name').allTextContents(),['Office move','Hiring a designer']);
  assert.equal(await over.locator('.note-bullets li').count(),2);
  assert.equal(await page_.locator('.note-page .note-empty').count(),0);
  assert.ok(await page_.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),width+': the folder fits');
  assert.ok(await page_.locator('.note-kids .note-item[data-node="note:2"]').evaluate(e=>{const s=e.querySelector('small');return s.getBoundingClientRect().height<=parseFloat(getComputedStyle(s).lineHeight)+1}),
   width+': a row with a summary under this one keeps its count on one line');
  await page_.evaluate(()=>document.activeElement?.blur());
  if(shots)await page_.screenshot({path:`${shots}/note-folder-${width}-${scheme}.png`,fullPage:true});
  await over.locator('.note-bullets .note-cite-name',{hasText:'Hiring a designer'}).click();
  await page_.locator('.note-page h3',{hasText:'Hiring a designer'}).waitFor();
  // No page: the lines only, not numbered
  await page_.goto(base+'#graph/note:3');await page_.locator('.note-page h3').waitFor();
  assert.equal(await page_.locator('.note-written').count(),0);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok notes page');
}finally{await browser?.close();server.close()}
