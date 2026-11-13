import assert from 'node:assert/strict';
import {mkdir,readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections: a company reads as the Machine names it (api/status work_labels, work_or_personal.work_labels). A name
// made from a domain (work:Moreaudesign for moreaudesign.io) reads plain Work, never the domain capitalized; a real
// one keeps it (Work · Initech Corp); its Details choice reads the same. SHOTS=<folder> saves each width and scheme.
const dashboard=await dashboardPage();
const at=new Date().toISOString();
const card=(id,service,email,display_name,boundary)=>({id,service,email,display_name,boundary,last_success:at,last_sync_signals:2,sync_activity:[],failures_24h:0,read_window:{},total:40,signals_24h:3,pending:1});
const connectors=[card('moreau-gmail','gmail','jules@moreaudesign.io','jules@moreaudesign.io','work:Moreaudesign'),
 card('initech-trello','trello','','Initech board','work:Initech Corp')];
let labels={'work:Moreaudesign':'Work','work:Initech Corp':'Work · Initech Corp'};
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(/^\/brand\/[\w.-]+\.(png|webp|woff2)$/.test(url.pathname)){try{const f=await readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url));res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':url.pathname.endsWith('.webp')?'image/webp':'font/woff2');res.end(f)}catch{res.statusCode=404;res.end()}return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors,work_labels:labels,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
// the company as its Details choice reads it; the card's own subtitle is the Machine's (test_card_names.py)
const sub=(page,id)=>page.locator(`select[data-scope="${id}"]`).evaluate(s=>s.selectedOptions[0].textContent);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const [width,height,mobile] of [[1440,900,false],[390,844,true]]){
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#connections=other');  // no group in the fixture: Other
  const mail=page.locator('#connectors article[data-conn="moreau-gmail"]');await mail.waitFor();await page.waitForTimeout(300);
  assert.equal(await sub(page,'moreau-gmail'),'Work');  // never the kind again (machine/names.py account_card)
  assert.equal(await sub(page,'initech-trello'),'Work · Initech Corp');
  assert.doesNotMatch(await page.locator('#connectors').innerText(),/Moreaudesign/,'no capitalized domain anywhere on the cards');
  if(shots){await mail.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/card-${width}-${scheme}.png`})}
  await context.close()}
 // Two companies both made from a domain: each reads its domain as it is, so they stay apart
 labels={'work:Moreaudesign':'Work · moreaudesign.io','work:Initech Corp':'Work · initech.dev'};
 const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'}),page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await page.goto(base+'/#connections');await page.locator('#connectors article[data-conn="moreau-gmail"]').waitFor();
 assert.equal(await sub(page,'moreau-gmail'),'Work · moreaudesign.io');
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('work label dashboard ok');
