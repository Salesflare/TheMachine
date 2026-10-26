import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Checkboxes, radios and sliders take the app green in both themes, never the browser's default blue: the board
// editor's Who sees it, the Share sheet's people, settings toggles.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const colorScheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width:390,height:800},colorScheme}),page=await context.newPage();
  await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof showTab==='function');
  const got=await page.evaluate(()=>{const probe=document.createElement('span');probe.style.color='var(--c-accent)';document.body.append(probe);
   const want=getComputedStyle(probe).color,out={want};for(const t of ['checkbox','radio','range']){const i=document.createElement('input');i.type=t;document.body.append(i);out[t]=getComputedStyle(i).accentColor}return out});
  for(const t of ['checkbox','radio','range'])assert.equal(got[t],got.want,`${colorScheme} ${t} in the app green`);
  await context.close();
 }
 console.log('accent dashboard ok');
}finally{await browser?.close();server.close()}
