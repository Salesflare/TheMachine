import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from './openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// On a phone the toast never covers buttons (a card's actions at the bottom of the screen, the chat box): it moves just
// above them, or to the top under the bar when buttons fill the bottom of the screen, and back down for the next one when nothing is in the way. On a desktop it stays where it is. The send
// confirm (Confirm / Edit / Cancel) is a bottom sheet on a phone, like the other editors.
const dashboard=await readFile(new URL('./dashboard.html',import.meta.url),'utf8');
const shots=process.env.SHOTS||'';
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const rect=(page,sel)=>page.evaluate(s=>{const r=document.querySelector(s).getBoundingClientRect();return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,width:r.width}},sel);
const shown=page=>page.waitForFunction(()=>{const t=document.querySelector('#toast');return t.classList.contains('show')&&getComputedStyle(t).opacity==='1'});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440]){
  const phone=width<600,context=await browser.newContext({viewport:{width,height:844},isMobile:phone,hasTouch:phone}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof toast==='function');
  // Placement must not wait for a frame: a throttled frame can otherwise leave the visible toast over buttons.
  if(phone){await page.evaluate(()=>toast('Initial.'));await shown(page);const fit=await page.evaluate(()=>{const native=requestAnimationFrame;window.requestAnimationFrame=()=>0;
   const d=document.createElement('div');d.id='instant-bar';d.style.cssText='position:fixed;left:0;right:0;bottom:10px;display:flex;padding:0 16px';
   d.innerHTML='<button style="flex:1;height:44px">Do it</button>';document.body.append(d);
   try{toast('Saved.');const t=document.querySelector('#toast').getBoundingClientRect(),b=d.getBoundingClientRect();return t.bottom<=b.top}
   finally{window.requestAnimationFrame=native;d.remove()}});assert.equal(fit,true,'toast placement does not depend on the next animation frame')}
  // A row of buttons where the toast would go, like an open card's actions
  await page.evaluate(()=>{const d=document.createElement('div');d.id='bar';d.style.cssText='position:fixed;left:0;right:0;bottom:10px;display:flex;gap:8px;padding:0 16px;z-index:1';
   d.innerHTML='<button style="flex:1;height:44px">Do it</button><button style="flex:1;height:44px">Snooze</button>';document.body.append(d);toast('Handed off. The card shows how it goes.')});
  await shown(page);const t=await rect(page,'#toast'),bar=await rect(page,'#bar');
  if(width<1024)assert.ok(t.bottom<=bar.top,`${width}: the toast sits above the buttons ${JSON.stringify({t,bar})}`);
  else assert.ok(t.bottom>bar.top,'desktop: the toast stays put');
  if(shots)await page.screenshot({path:`${shots}/toast-lift-${width}.png`});
  // Buttons filling the bottom of the screen (a card with its Why chips, note and Decline): the toast goes to the top
  if(width<1024){await page.evaluate(()=>{const d=document.querySelector('#bar');d.style.cssText+=';flex-direction:column;height:360px;gap:4px';d.innerHTML=Array.from({length:7},(_,i)=>`<button style="height:44px">B${i}</button>`).join('');toast('Declined. They see your note.')});
   await shown(page);await page.waitForTimeout(250);const t2=await rect(page,'#toast'),bar2=await rect(page,'#bar'),top=await rect(page,'#topbar');
   assert.ok(t2.bottom<=bar2.top&&t2.top>=top.bottom-1&&t2.top<844*.5,`${width}: near the top, under the bar ${JSON.stringify({t2,bar2,top})}`);
   if(shots)await page.screenshot({path:`${shots}/toast-top-${width}.png`});
   // A card right under the top bar: the toast covers neither its header line, its title nor its buttons
   await page.evaluate(()=>{const a=document.createElement('article');a.className='card';a.id='topcard';a.style.cssText=`position:fixed;left:16px;right:16px;top:${document.querySelector('#topbar').getBoundingClientRect().bottom+4}px;z-index:1;margin:0`;
    a.innerHTML='<div class="meta"><div class="card-badges"><span class="chip scope">Work</span></div><span>3 hours ago</span></div><h3>Rotate the shared webhook secret</h3><p>A short body line.</p><button>Do it</button>';document.body.append(a);toast('Declined. They see your note.')});
   await shown(page);await page.waitForTimeout(250);const t3=await rect(page,'#toast'),over=await page.evaluate(t=>[...document.querySelectorAll('#topcard>.meta,#topcard>h3,#topcard>p,#topcard button,#bar button')].filter(e=>{const r=e.getBoundingClientRect();return r.bottom>t.top&&r.top<t.bottom}).map(e=>e.textContent),t3);
   assert.deepEqual(over,[],`${width}: the toast covers no header line, title or button`);
   if(shots)await page.screenshot({path:`${shots}/toast-card-${width}.png`});await page.evaluate(()=>document.querySelector('#topcard').remove())}
  // Nothing in the way: back at its usual place
  await page.evaluate(()=>{document.querySelector('#bar').remove();toast('Saved.')});await shown(page);await page.waitForTimeout(250);
  const again=await rect(page,'#toast');assert.ok(844-again.bottom<40,`${width}: back near the bottom (${844-again.bottom})`);
  // The send confirm: a bottom sheet on a phone
  await page.evaluate(()=>{const d=document.querySelector('#send-dialog');d.showModal()});
  const d=await rect(page,'#send-dialog');
  if(phone){assert.equal(Math.round(d.width),width,'full width');assert.ok(Math.abs(d.bottom-844)<2,'at the bottom')}
  else assert.ok(d.width<width-100,'desktop: a centered dialog');
  if(shots)await page.screenshot({path:`${shots}/send-sheet-${width}.png`});
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('toast lift dashboard ok');
}finally{await browser?.close();server.close()}
