import assert from 'node:assert/strict';
import {mkdir,readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A connection's history on its card (machine/store/history.py, docs/help/history.md): how far back it reaches once it's
// in ("History: back to November 2025."), "so far" while it comes in, and nothing before it starts. One line, in the
// owner's language, never wider than the card. While WhatsApp's own first chat-history count runs, only that line shows.
// SHOTS=<folder> saves each width and theme.
const dashboard=await dashboardPage();
const at=new Date().toISOString();
const card=(id,service,email,more)=>({id,service,email,display_name:email,boundary:'personal',last_success:at,last_sync_signals:2,sync_activity:[],failures_24h:0,read_window:{},...more});
const connectors=[card('mail','gmail','sam@example.org',{total:5240,signals_24h:18,pending:3,backfill:{back_to:'2025-11',done:true,kept:4180}}),
 card('cal','calendar','sam@example.org',{total:640,signals_24h:4,pending:0,upcoming_7d:9,backfill:{back_to:'2026-03',done:false,kept:210}}),
 card('wa','whatsapp','',{display_name:'WhatsApp',total:412,signals_24h:37,pending:12,history:14717,backfill:{back_to:'2026-05',done:false,kept:900}}),
 card('new','gmail','alex@example.org',{total:31,signals_24h:1,pending:0})];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const notes=page=>page.evaluate(()=>Object.fromEntries([...document.querySelectorAll('#connectors article[data-conn]')].map(a=>[a.dataset.conn,[...a.querySelectorAll('p.note')].map(p=>p.textContent.trim())])));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,mobile] of [[1440,900,false],[1440,700,false],[390,844,true]])for(const scheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}x${height}-${scheme}`;
  await page.goto(base+'/#connections');await page.locator('#connectors article[data-conn="mail"]').waitFor();await page.waitForTimeout(300);
  const n=await notes(page);
  assert.ok(n.mail.includes('History: back to November 2025.'),`${tag} mail: ${n.mail}`);
  assert.ok(n.cal.includes('History coming in: back to March 2026 so far.'),`${tag} calendar: ${n.cal}`);
  assert.deepEqual(n.wa.filter(x=>x.startsWith('History')),[],`${tag}: one history line: WhatsApp's own count while it runs`);
  assert.ok(n.wa.includes('Bringing in your chat history: 14,717 messages so far.'),`${tag} WhatsApp keeps its own count`);
  assert.deepEqual(n.new.filter(x=>x.startsWith('History')),[],tag);
  const fit=await page.evaluate(()=>[...document.querySelectorAll('#connectors article[data-conn] p.note')].every(p=>p.getBoundingClientRect().right<=p.closest('article').getBoundingClientRect().right+1)&&document.documentElement.scrollWidth<=innerWidth);
  assert.ok(fit,`${tag}: fits`);
  if(shots){await page.locator('#connectors article[data-conn="mail"]').scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/history-card-${tag}.png`})}
  await context.close()}
 // In the owner's language
 {const nl=JSON.parse(await readFile(new URL('../i18n/nl.json',import.meta.url),'utf8'));
  const context=await browser.newContext({viewport:{width:1440,height:900},locale:'nl-NL'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#connections');await page.locator('#connectors article[data-conn="mail"]').waitFor();
  await page.evaluate(cat=>i18nUse('nl',cat),nl);await page.getByText('Geschiedenis: terug tot').first().waitFor({timeout:8000});
  const n=await notes(page);assert.ok(n.mail.some(x=>/^Geschiedenis: terug tot \S+ 2025\.$/.test(x)),`nl: ${n.mail}`);
  assert.ok(n.cal.some(x=>/^Geschiedenis komt binnen: tot nu toe terug tot \S+ 2026\.$/.test(x)),`nl: ${n.cal}`);await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('connections history dashboard ok');
