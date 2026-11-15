import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The Notes list is one card with a row per note, like a list, not a stack of cards: a note's own notes sit a step in
// under its caret, the caret folds them, and a row with notes under it still opens its own page. At 390 and 1440,
// nothing wider than the screen.
const dashboard=await dashboardPage();
const at=new Date().toISOString();
const note=(n,name,depth,parent,children=0,lines=0)=>({id:'note:'+n,kind:'note',name,area:'personal',starts:null,ends:null,by:'owner',updated_at:at,lines,parent,depth,children});
const notes=[note(1,'Home',0,null,1),note(2,'Dishwasher',1,'note:1',0,2),note(3,'Garden',0,null,0,1)];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'&&url.searchParams.has('node')){const x=notes.find(n=>n.id===url.searchParams.get('node'));
  res.end(JSON.stringify({...x,lines:[],path:[],created_at:at,renamed:false,owner_dates:false,dated:false,children:notes.filter(c=>c.parent===x.id),linked_from:[],tree:notes}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({list_counts:{people:0,quiet:0,new:0,orgs:0,warmup:0,projects:0,projects_done:0},counts:{person:0,org:0,project:0},boards:[],board_suggestions:[],notes}));return}
 if(url.pathname==='/api/graph/list'){res.end(JSON.stringify({items:[],next:null,total:0}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-GB'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(width+': '+e.message));await page.goto(base+'#graph=notes');
  await page.locator('.note-tree .note-item').nth(1).waitFor();
  // One card: the rows have no card of their own
  const look=await page.evaluate(()=>{const tree=document.querySelector('.note-tree'),s=getComputedStyle(tree),rows=[...tree.querySelectorAll('.note-item')];
   return {card:s.borderTopWidth!=='0px'&&s.backgroundColor!=='rgba(0, 0, 0, 0)',rowCards:rows.filter(r=>{const c=getComputedStyle(r);return c.borderTopLeftRadius!=='0px'||c.boxShadow!=='none'}).length,
    gaps:rows.slice(1).map((r,i)=>Math.round(r.getBoundingClientRect().top-rows[i].getBoundingClientRect().bottom)),names:rows.map(r=>r.querySelector('.node').textContent.trim())}});
  assert.ok(look.card,width+': the list is one card');assert.equal(look.rowCards,0,width+': no card per row');assert.ok(look.gaps.every(g=>g===0),width+': rows touch '+look.gaps);
  // Folded at first; the caret shows Dishwasher a step in
  assert.deepEqual(look.names,['Home','Garden']);
  await page.click('[data-note-fold="note:1"]');await page.locator('.note-item[data-node="note:2"]').waitFor();
  const x=id=>page.locator(`.note-item[data-node="${id}"] .node`).evaluate(e=>e.getBoundingClientRect().left);
  assert.ok(await x('note:2')-await x('note:1')>=20,width+': a note under another sits a step in');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),width+': fits');
  // The row with notes under it opens its own page
  await page.locator('.note-item[data-node="note:1"] .node').click();
  await page.waitForFunction(()=>decodeURIComponent(location.hash)==='#graph/note:1');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok notes tree');
}finally{await browser?.close();server.close()}
