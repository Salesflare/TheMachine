import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections, Disconnected lately (names.disconnected_rows): rows like the connected ones above, each with its
// provider's mark, its name and kind and when it was removed, in the page's own font; a pending one says why. It fits a
// phone. SHOTS=<dir> also saves screenshots at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const brand={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'};
const at=new Date().toISOString(),earlier=new Date(Date.now()-3*3600e3).toISOString(),week=new Date(Date.now()-7*86400e3).toISOString();
const connectors=[{id:'g',service:'gmail',group:'mail',display_name:'alex@acme.example',card_title:'alex@acme.example',card_subtitle:'Work',boundary:'work:Acme',total:812,signals_24h:14,last_success:at,sync_activity:[]},
 {id:'o',service:'outlook',group:'mail',display_name:'sam@contoso.example',card_title:'sam@contoso.example',card_subtitle:'Personal',boundary:'personal:me',total:240,signals_24h:3,last_success:at,sync_activity:[]}];
const row=(card_title,card_subtitle,mark,provider_name,when,state='removed')=>({card_title,card_subtitle,mark,provider_name,at:when,state,group:mark==='slack'?'chat':'mail'});
const disconnected=[row('alex.long.address@subsidiary.acme-holdings.example','Google account','google','Google',at,'pending'),
 row('robin@contoso.example','Microsoft account','microsoft','Microsoft',earlier),row('old@acme.example','Google account','google','Google',week),row('Slack','','slack','Slack',week)];
const server=createServer(async(req,res)=>{
 const logo=/^\/brand\/(logos\/(?:mono\/)?[a-z_]+\.(?:svg|png))$/.exec(req.url),file=brand[req.url]||(logo?'dashboard/'+logo[1]:'');
 if(file){try{res.setHeader('Content-Type',file.endsWith('.png')?'image/png':file.endsWith('.svg')?'image/svg+xml':'font/woff2');res.end(await readFile(new URL('../'+file,import.meta.url)))}catch{res.statusCode=404;res.end()}return}
 res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url.startsWith('/api/status')){res.end(JSON.stringify({suggestions:[],promises:[],connectors,disconnected,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[1440,900,'light'],[390,844,'light'],...(process.env.SHOTS?[[1440,900,'dark'],[390,844,'dark']]:[])]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#connections=mail');  // under Email, also on a phone
  const block=page.locator('#disconnected');await block.locator('article').first().waitFor();
  const rows=await block.locator('article').evaluateAll(a=>a.map(x=>x.innerText.replace(/\s+/g,' ').trim()));
  assert.equal(rows.length,3,'Slack shows under Chat, not here');
  assert.match(rows[0],/Google account · Pending: Google hasn’t confirmed\. Retrying/);
  assert.match(rows[1],/^robin@contoso\.example Microsoft account · Removed \d+ hours? ago$/);
  assert.match(rows[2],/^old@acme\.example Google account · Removed 7 days ago$/);
  // like the connected rows: the same row, its mark, the page's own font for when, nothing of a chip
  const look=await page.evaluate(()=>{const r=document.querySelector('#disconnected .conn-row'),c=document.querySelector('#connectors .conn-row');
   const box=e=>e.getBoundingClientRect(),when=document.querySelectorAll('#disconnected time')[1];
   return {icon:!!r.querySelector('.icon .via-ico'),chip:!!document.querySelector('#disconnected .chip'),
    left:[box(r.querySelector('.icon')).left-box(r).left,box(c.querySelector('.icon')).left-box(c).left],
    font:[getComputedStyle(when).fontFamily,getComputedStyle(r.querySelector('small')).fontFamily],mono:when.classList.contains('mono')}});
  assert.ok(look.icon,'the provider’s mark');assert.ok(!look.chip,'no chip');assert.ok(!look.mono,'not monospace');
  assert.equal(look.left[0],look.left[1],'icons line up with the rows above');assert.equal(look.font[0],look.font[1]);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  if(process.env.SHOTS){await block.scrollIntoViewIfNeeded();await page.waitForTimeout(300);await page.screenshot({path:`${process.env.SHOTS}/connections-disconnected-${width}-${scheme}.png`,fullPage:width<500})}
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('disconnected ok');
}finally{await browser?.close();server.close()}
