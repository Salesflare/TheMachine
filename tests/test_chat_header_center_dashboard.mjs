import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The to-do chat's header: the back chevron sits on the title's center line, not below it. Measured with the page's own
// font (Inter, served as the service serves it), on a phone and a computer, light and dark: the chevron's box center and
// the title text's center (a Range on its text, not the heading's box) are at most 1px apart, and ⋯ is on the same line.
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
  const m=await page.evaluate(()=>{const q=s=>document.querySelector(s),c=r=>r.top+r.height/2,t=q('.chat-title'),g=document.createRange();
   g.selectNodeContents([...t.childNodes].find(n=>n.nodeType===3));
   return {inter:document.fonts.check('600 16px Inter'),theme:document.documentElement.dataset.theme,title:c(g.getBoundingClientRect()),back:c(q('.chat-back svg').getBoundingClientRect()),menu:c(q('.chat-menu>summary svg').getBoundingClientRect())}});
  const at=`${width} ${theme}: ${j(m)}`;
  assert.ok(m.inter,'the page has its own font: '+at);assert.equal(m.theme,theme);
  assert.ok(Math.abs(m.back-m.title)<=1,'the back chevron is on the title\'s center line: '+at);
  assert.ok(Math.abs(m.menu-m.back)<=0.5,'⋯ is on the same line: '+at);
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
