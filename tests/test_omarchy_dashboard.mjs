import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Omarchy theme (settings-omarchy.js): without Omarchy the row stays hidden. On the Omarchy computer itself (`here`)
// it is on by default; elsewhere off until picked. On, it paints the theme's colors, follows a theme switch without a
// reload (asking with the ETag: 304s until it changes), starts in them after a reload, and an explicit off is kept.
const dashboard=await dashboardPage();
const tokyo={name:'tokyo-night',mode:'dark',colors:{accent:'#7aa2f7',background:'#1a1b26',foreground:'#a9b1d6',dark_background:'#16161e',blue:'#7aa2f7',magenta:'#bb9af7',yellow:'#e0af68',orange:'#ff9e64'}};
const latte={name:'catppuccin-latte',mode:'light',colors:{accent:'#1e66f5',background:'#eff1f5',foreground:'#4c4f69'}};
let theme={},here=true,version=1;const seen={200:0,304:0};
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/omarchy-theme'&&theme.colors){const tag=`"t${version}-${+here}"`;
  if(req.headers['if-none-match']===tag){seen[304]++;res.writeHead(304,{ETag:tag});res.end();return}
  seen[200]++;res.writeHead(200,{'Content-Type':'application/json',ETag:tag});res.end(JSON.stringify({...theme,here}));return}
 res.setHeader('Content-Type','application/json');res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const look=page=>page.evaluate(()=>{const r=document.documentElement,s=getComputedStyle(r);
 return {omarchy:r.dataset.omarchy||null,theme:r.dataset.theme,bg:s.getPropertyValue('--c-bg').trim(),row:!$('#omarchy-row').hidden,
  on:$('#omarchy-switch').getAttribute('aria-checked'),light:!$('#theme-toggle').closest('div').hidden}});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const open=async()=>{const context=await browser.newContext({viewport:{width:1280,height:800},colorScheme:'dark'});return [context,await context.newPage()]};
 const ready=page=>page.waitForFunction(()=>typeof showTab==='function');

 // Without Omarchy: nothing
 let [context,page]=await open();
 await page.goto(base);await ready(page);await page.waitForTimeout(300);
 let got=await look(page);
 assert.equal(got.row,false,'no Omarchy: no row');assert.equal(got.omarchy,null);assert.equal(got.bg,'#1b1c1f','the dashboard’s own dark page');

 // On the Omarchy computer itself: on by default
 theme=tokyo;await page.reload();await ready(page);
 await page.waitForFunction(()=>document.documentElement.dataset.omarchy==='tokyo-night');
 got=await look(page);
 assert.deepEqual([got.row,got.on,got.theme,got.bg,got.light],[true,'true','dark','#1a1b26',false],'on by default here, Light mode hidden');

 // Follows a theme switch: 304s while nothing changes, then the new colors without a reload
 const before={...seen};await page.waitForTimeout(4500);
 assert.ok(seen[304]-before[304]>=1&&seen[200]===before[200],'unchanged: only 304s');
 theme=latte;version++;
 await page.waitForFunction(()=>document.documentElement.dataset.omarchy==='catppuccin-latte',null,{timeout:6000});
 got=await look(page);assert.deepEqual([got.theme,got.bg],['light','#eff1f5'],'follows the switch, light included');

 await page.reload();
 const first=await page.evaluate(()=>[document.documentElement.dataset.omarchy,getComputedStyle(document.documentElement).getPropertyValue('--c-bg').trim()]);
 assert.deepEqual(first,['catppuccin-latte','#eff1f5'],'a reload starts in the theme');
 await ready(page);

 // An explicit off is kept, also after a reload
 await page.evaluate(()=>$('#omarchy-switch').click());
 got=await look(page);
 assert.deepEqual([got.omarchy,got.theme,got.bg,got.on,got.light],[null,'dark','#1b1c1f','false',true],'off: the page’s own theme back');
 await page.reload();await ready(page);await page.waitForFunction(()=>!$('#omarchy-row').hidden);await page.waitForTimeout(300);
 got=await look(page);assert.deepEqual([got.omarchy,got.on],[null,'false'],'off stays off');
 await context.close();

 // Another computer: offered, off until picked
 here=false;[context,page]=await open();
 await page.goto(base);await ready(page);await page.waitForFunction(()=>!$('#omarchy-row').hidden);await page.waitForTimeout(300);
 got=await look(page);assert.deepEqual([got.on,got.omarchy,got.light],['false',null,true],'another device: off by default');
 await page.evaluate(()=>$('#omarchy-switch').click());
 got=await look(page);assert.deepEqual([got.omarchy,got.on],['catppuccin-latte','true'],'picked: on');
 theme={};await page.reload();await ready(page);await page.waitForTimeout(300);
 got=await look(page);assert.deepEqual([got.row,got.omarchy],[false,null],'Omarchy gone: no row, no colors');
 await context.close();

 // A phone never asks
 const phone=await browser.newContext({viewport:{width:390,height:844},userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148'});
 const asked=[];const p2=await phone.newPage();p2.on('request',r=>{if(r.url().includes('omarchy-theme'))asked.push(r.url())});
 theme=tokyo;here=true;await p2.goto(base);await ready(p2);await p2.waitForTimeout(300);
 assert.equal(asked.length,0,'a phone doesn’t ask');assert.equal(await p2.evaluate(()=>$('#omarchy-row').hidden),true);
 console.log('omarchy dashboard ok');
}finally{await browser?.close();server.close()}
