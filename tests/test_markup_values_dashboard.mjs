import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Values from the status that the page writes as markup: the first look's counts are whole numbers and the usage
// page is a web address, whatever the status says. The first look with real counts and the ChatGPT link still show.
const dashboard=await dashboardPage(),en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const server=createServer((req,res)=>{const u=new URL(req.url,'http://x');res.setHeader('Content-Type','application/json');
 if(u.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(u.pathname==='/i18n/en.json'){res.end(en);return}
 if(u.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_runs:[]}));return}
 if(!u.pathname.startsWith('/api/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof firstLookBar==='function'&&typeof resetAction==='function');
 const got=await page.evaluate(()=>{const parse=html=>{const t=document.createElement('template');t.innerHTML=html;return t.content};
  const bar=parse(firstLookBar({done:'3"><img src=x onerror=alert(1)>',total:'8"><b>'})),text=parse(firstLookBar({done:'3',total:'8'})),good=parse(firstLookBar({done:3,total:12}));
  const link=parse(resetAction({usage_page:'javascript:alert(1)',resets:1})),real=parse(resetAction({usage_page:'https://chatgpt.com/codex/settings/usage'}));
  return {hostile:bar.querySelectorAll('img,b').length,hostileText:bar.textContent,text:text.textContent,good:good.textContent,width:good.querySelector('i').style.width,
   now:good.querySelector('[role=progressbar]').getAttribute('aria-valuenow'),link:link.querySelectorAll('a').length,real:real.querySelector('a')?.href}});
 assert.equal(got.hostile,0,'no markup from the counts');
 assert.equal(got.hostileText,'','a count that is no number shows no bar');
 assert.equal(got.text,'3 of 8 signals');
 assert.deepEqual([got.good,got.width,got.now],['3 of 12 signals','25%','3']);
 assert.equal(got.link,0,'no javascript: link');
 assert.equal(got.real,'https://chatgpt.com/codex/settings/usage');
 assert.deepEqual(errors,[]);
 console.log('ok first look counts and the usage link');
}finally{await browser?.close();server.close()}
