import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Omarchy theme (settings-omarchy.js): without Omarchy the row stays hidden; with it, the switch paints the theme's
// colors, follows a theme switch without a reload, starts in them after a reload and gives the page back when off.
const dashboard=await dashboardPage();
const tokyo={name:'tokyo-night',mode:'dark',colors:{accent:'#7aa2f7',background:'#1a1b26',foreground:'#a9b1d6',dark_background:'#16161e',blue:'#7aa2f7',magenta:'#bb9af7',yellow:'#e0af68',orange:'#ff9e64'}};
const latte={name:'catppuccin-latte',mode:'light',colors:{accent:'#1e66f5',background:'#eff1f5',foreground:'#4c4f69'}};
let theme={};
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');res.end(url.pathname==='/api/omarchy-theme'?JSON.stringify(theme):url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const look=page=>page.evaluate(()=>{const r=document.documentElement,s=getComputedStyle(r);
 return {omarchy:r.dataset.omarchy||null,theme:r.dataset.theme,bg:s.getPropertyValue('--c-bg').trim(),row:!$('#omarchy-row').hidden,
  on:$('#omarchy-switch').getAttribute('aria-checked'),light:!$('#theme-toggle').closest('div').hidden}});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1280,height:800},colorScheme:'dark'}),page=await context.newPage();
 const ready=()=>page.waitForFunction(()=>typeof showTab==='function');
 await page.goto(base);await ready();await page.waitForTimeout(300);
 let got=await look(page);
 assert.equal(got.row,false,'no Omarchy: no row');assert.equal(got.omarchy,null);assert.equal(got.bg,'#1b1c1f','the dashboard’s own dark page');

 theme=tokyo;await page.reload();await ready();await page.waitForFunction(()=>!$('#omarchy-row').hidden);
 got=await look(page);assert.equal(got.on,'false','offered, off until picked');assert.equal(got.omarchy,null);assert.equal(got.light,true);

 await page.evaluate(()=>$('#omarchy-switch').click());
 got=await look(page);
 assert.deepEqual([got.omarchy,got.theme,got.bg,got.on,got.light],['tokyo-night','dark','#1a1b26','true',false],'on: the theme’s colors, Light mode hidden');

 theme=latte;  // a theme switch in Omarchy: the page follows by itself
 await page.waitForFunction(()=>document.documentElement.dataset.omarchy==='catppuccin-latte',null,{timeout:6000});
 got=await look(page);assert.deepEqual([got.theme,got.bg],['light','#eff1f5'],'follows the switch, light included');

 await page.reload();
 const first=await page.evaluate(()=>[document.documentElement.dataset.omarchy,getComputedStyle(document.documentElement).getPropertyValue('--c-bg').trim()]);
 assert.deepEqual(first,['catppuccin-latte','#eff1f5'],'a reload starts in the theme');
 await ready();

 await page.evaluate(()=>$('#omarchy-switch').click());
 got=await look(page);
 assert.deepEqual([got.omarchy,got.theme,got.bg,got.on,got.light],[null,'dark','#1b1c1f','false',true],'off: the page’s own theme back');

 theme={};await page.reload();await ready();await page.waitForTimeout(300);
 got=await look(page);assert.equal(got.row,false,'Omarchy gone: no row');
 await context.close();

 // A phone never asks
 const phone=await browser.newContext({viewport:{width:390,height:844},userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148'});
 const asked=[];const p2=await phone.newPage();p2.on('request',r=>{if(r.url().includes('omarchy-theme'))asked.push(r.url())});
 theme=tokyo;await p2.goto(base);await p2.waitForFunction(()=>typeof showTab==='function');await p2.waitForTimeout(300);
 assert.equal(asked.length,0,'a phone doesn’t ask');assert.equal(await p2.evaluate(()=>$('#omarchy-row').hidden),true);
 console.log('omarchy dashboard ok');
}finally{await browser?.close();server.close()}
