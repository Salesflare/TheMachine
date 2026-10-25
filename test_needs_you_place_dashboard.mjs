import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from './openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// "Needs you" shows everything on Suggestions, and elsewhere only what belongs to that tab: a signed-out source on
// Connections, waiting skills on Settings › Skills, nothing on other tabs. Settings › General says in plain words that
// more settings live on the Machine; the terminal commands on Connections sit behind a closed disclosure. Seven Fleet
// tabs fit a desktop column.
const dashboard=await readFile(new URL('./dashboard.html',import.meta.url),'utf8');
const ok=new Date().toISOString(),later=new Date(Date.now()+6e5).toISOString();
const linkedin={id:'work-linkedin',service:'linkedin',boundary:'work',display_name:'Work LinkedIn',error:'linkedin_signed_out',error_at:ok,retry_at:later,signed_out:true};
const skills={skills:[{id:'sk_in',name:'Answer pricing questions',description:'When a customer asks what something costs',status:'incoming',origin:'shared',version:1,author:'Pat',note:'',
 waiting:1,targets:[],folder:'skills/the-machine'}],waiting:1};
const server=createServer((req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
   connectors:[linkedin],skills}));return}
 if(url.pathname==='/api/events'){res.end('[]');return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const shown=page=>page.evaluate(()=>{const b=document.querySelector('#needs-you');return b.hidden||!b.offsetParent?[]:[...b.querySelectorAll('li')].filter(l=>!l.hidden).map(l=>l.dataset.home)});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.locator('#needs-you li',{hasText:'Signed out of LinkedIn'}).waitFor();
 assert.deepEqual(await shown(page),['health','settings:skills']);
 await page.evaluate(()=>document.querySelector('[data-tab="health"]').click());await page.waitForTimeout(200);
 assert.deepEqual(await shown(page),['health']);
 await page.evaluate(()=>document.querySelector('[data-tab="events"]').click());await page.waitForTimeout(200);
 assert.deepEqual(await shown(page),[]);
 await page.evaluate(()=>showSettings('skills'));await page.locator('#settings-skills').waitFor();await page.waitForTimeout(200);
 assert.deepEqual(await shown(page),['settings:skills']);
 await page.evaluate(()=>showSettings('general'));await page.waitForTimeout(300);
 assert.deepEqual(await shown(page),[]);
 // General: plain words and a help link, no file names or commands.
 const more=page.locator('#settings-more');
 assert.match(await more.textContent(),/More settings live on this Machine\. Learn more/);
 assert.doesNotMatch(await more.textContent(),/config\.json|assistant |doctor/);
 assert.equal(await more.locator('a').getAttribute('href'),'https://themachine.computer/help/settings#on-this-machine');
 // Connections: the commands wait behind "Set up from the terminal", closed.
 await page.evaluate(()=>document.querySelector('[data-tab="health"]').click());
 const cli=page.locator('#connect-more details.connect-cli');
 await cli.waitFor({state:'attached'});
 assert.equal(await cli.locator('summary').textContent(),'Set up from the terminal');
 assert.equal(await cli.evaluate(d=>d.open),false);
 assert.match(await cli.textContent(),/assistant connect gmail/);
 // Desktop: seven Fleet tabs (with a badge) fit the column without scrolling.
 await page.setViewportSize({width:1440,height:900});await page.waitForTimeout(200);
 const fit=await page.evaluate(()=>{const host=[...document.querySelectorAll('main>section')].find(x=>!x.hidden),t=document.createElement('div');t.className='fleet-tabs';
  t.innerHTML=["Lumen Labs","What's shared","Morgans",'Friends <span class="badge">1</span>','Network','Sharing','Activity'].map(l=>`<button type="button">${l}</button>`).join('');
  host.prepend(t);const r=[t.scrollWidth,t.clientWidth];t.remove();return r});
 assert.ok(fit[0]<=fit[1],'Fleet tabs overflow: '+fit);
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({page_errors:errors}));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r))}
