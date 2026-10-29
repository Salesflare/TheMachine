import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Error reports (error_feed.py): an uncaught error or unhandled rejection in the dashboard's own code is posted as
// client_error with its type, message and place (function and line); another origin's script, the Machine being away
// and a repeat within a minute are not; nothing once the owner turned reports off; the Settings switch. All mocked,
// nothing leaves the test. SHOTS=dir saves screenshots.
// The page's own code, as the browser sees it: a static inline script at the page's own address (a script added later
// reads as <anonymous>, and the dashboard never adds one)
const own=`<script>function renderBoom(){const card=null;return card.title}
async function loadNope(){throw new RangeError('Nope for sam@example.com')}
function renderAgain(){return null.x}
addEventListener('test-boom',()=>{setTimeout(renderBoom);setTimeout(renderBoom)});addEventListener('test-nope',()=>{loadNope()});addEventListener('test-again',()=>setTimeout(renderAgain))</script>`;
const dashboard=(await dashboardPage()).replace(/<\/html>\s*$/,own+'</html>');
let view,posts;
const reset=on=>{view={offer:true,vote:true,errors:on,network:true,ask:null,last_shared:null};posts=[]};
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],voices:[],facts:[],team_learnings:view}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='set_error_reports'){view={...view,errors:args.on};res.end(JSON.stringify({team_learnings:view}));return}
  if(action==='client_error'){res.end(JSON.stringify({ok:true,counted:args.errors.length}));return}}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,shots=process.env.SHOTS;let browser;
const reports=()=>posts.filter(p=>p.action==='client_error').flatMap(p=>p.args.errors);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // On: an error in the page's own code goes, once
 reset(true);
 let context=await browser.newContext({viewport:{width:1440,height:900}}),page=await context.newPage();
 const unexpected=[];page.on('pageerror',e=>{if(!/reading 'title'|^Nope|reading 'x'|^away$/.test(e.message))unexpected.push(e.message)});
 await page.goto(base+'/');await page.locator('#suggestions').waitFor();await page.waitForTimeout(800);
 await page.evaluate(()=>{dispatchEvent(new Event('test-boom'));dispatchEvent(new Event('test-nope'))});
 await page.evaluate(()=>{const s=document.createElement('script');s.src='data:text/javascript,function elsewhere(){null.x}elsewhere()';document.body.append(s)});
 await page.evaluate(()=>setTimeout(()=>{throw Object.assign(Error('away'),{offline:true})}));
 await page.waitForTimeout(2600);
 const got=reports();
 assert.equal(got.length,2,JSON.stringify(got));
 const boom=got.find(e=>e.kind==='TypeError'),nope=got.find(e=>e.kind==='RangeError');
 assert.deepEqual({file:boom.file,function:boom.function},{file:'dashboard.html',function:'renderBoom'});
 assert.ok(boom.line>0&&/null/.test(boom.message),JSON.stringify(boom));
 assert.deepEqual({file:nope.file,function:nope.function},{file:'dashboard.html',function:'loadNope'});
 assert.equal(nope.message,'Nope for sam@example.com','the page sends the raw message; the service normalizes it (test_error_feed.py)');
 assert.deepEqual(unexpected,[]);
 // The Settings switch: on, and turning it off posts set_error_reports
 await navClick(page.locator('#open-settings'));await page.locator('#settings-tabs [data-settings-tab="security"]').click();
 const sw=page.locator('#share-errors');await sw.waitFor();
 assert.equal(await sw.getAttribute('aria-checked'),'true');
 const row=page.locator('#settings-share');
 assert.match(await row.textContent(),/Send error reports.*Never your messages, names or addresses\./s);
 for(const [w,h] of [[1440,900],[1440,700],[390,844]]){
  await page.setViewportSize({width:w,height:h});await sw.scrollIntoViewIfNeeded();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+w);
  if(shots)await page.screenshot({path:`${shots}/settings-errors-${w}x${h}.png`});
 }
 await page.setViewportSize({width:1440,height:900});
 await sw.click();await page.locator('#share-errors[aria-checked="false"]').waitFor();
 assert.deepEqual(posts.at(-1),{action:'set_error_reports',args:{on:false}});
 // Off: nothing is posted
 const before=reports().length;
 await page.evaluate(()=>dispatchEvent(new Event('test-again')));
 await page.waitForTimeout(2600);
 assert.equal(reports().length,before,'nothing once reports are off');
 await context.close();
 console.log('error reports dashboard ok');
}finally{await browser?.close();server.close()}
