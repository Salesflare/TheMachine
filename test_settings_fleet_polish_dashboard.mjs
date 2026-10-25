import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from './openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Small layout rules from the screen-by-screen pass:
// - Settings on a desktop: Work hours, the Model panel and the skill search are as wide as the rest of the tab.
// - The Fleet's Team brief row: "Also send it to me" wraps as a whole, never "Also send it to" / "me".
// - An empty Feedback "What you decided" has no timeline line beside "No decisions yet.".
// - The phone drawer says "Updated 10:42", not a bare time.
// - Not in a Fleet: the line says how to join, with a Learn more link.
const dashboard=await readFile(new URL('./dashboard.html',import.meta.url),'utf8');
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440]){
  const phone=width<600,context=await browser.newContext({viewport:{width,height:844},isMobile:phone,hasTouch:phone}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof showSettings==='function'&&typeof fleetBriefSettings==='function');
  // Settings widths
  for(const [tab,sel] of [['hours','#hours'],['model','#model-panel'],['skills','#skills-find']]){
   await page.evaluate(([tab,sel])=>{showSettings(tab);const el=document.querySelector(sel);for(let n=el;n&&n!==document.body;n=n.parentElement)n.hidden=false},[tab,sel]);await page.waitForTimeout(200);
   const w=await page.evaluate(([tab,sel])=>{const el=document.querySelector(sel);for(let n=el;n&&n!==document.body;n=n.parentElement)n.hidden=false;
    const box=el.parentElement.getBoundingClientRect();return {el:Math.round(el.getBoundingClientRect().width),box:Math.round(box.width)}},[tab,sel]);
   assert.ok(Math.abs(w.el-w.box)<=2,`${width} ${tab}: as wide as its tab ${JSON.stringify(w)}`)}
  // The Team brief row
  const brief=await page.evaluate(()=>{const d=document.createElement('div');d.style.cssText='width:300px;font-size:16px';d.innerHTML=fleetBriefSettings({brief:{every:'off'}});document.body.append(d);
   const tell=d.querySelector('#fleet-brief-tell').closest('label'),r=tell.getBoundingClientRect(),line=parseFloat(getComputedStyle(tell).lineHeight)||20;const out={h:r.height,line,text:tell.textContent.trim()};d.remove();return out});
  assert.equal(brief.text,'Also send it to me');assert.ok(brief.h<brief.line*1.6+8,`${width}: "Also send it to me" on one line ${JSON.stringify(brief)}`);
  // An empty timeline has no line
  const tl=await page.evaluate(()=>{const d=document.querySelector('#decisions');d.innerHTML='<p class="muted">No decisions yet.</p>';const cs=getComputedStyle(d,'::before');return {content:cs.content,pad:getComputedStyle(d).paddingLeft}});
  assert.equal(tl.content,'none');assert.equal(tl.pad,'0px');
  // Not in a Fleet
  if(width===390){
   await page.evaluate(()=>{fleetData={on:false};document.querySelector('nav [data-tab="fleet"]').click()});
   const p=page.locator('#fleet-view p.muted').first();await p.waitFor();
   assert.match(await p.textContent(),/^This Machine is not in a Fleet\. Pair it with your account to join your team's\. Learn more$/);
   assert.match(await p.locator('a').getAttribute('href'),/\/help\/fleet$/);
   // The drawer
   await page.evaluate(()=>{document.querySelector('#updated').innerHTML='<span class="lbl">Updated </span>10:42';drawerOpen()});await page.waitForTimeout(400);
   assert.equal(await page.locator('#live .lbl').evaluate(e=>getComputedStyle(e).display),'inline','the drawer says Updated')}
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('settings fleet polish dashboard ok');
}finally{await browser?.close();server.close()}
