import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A message search comes in two steps (made-up data): the keyword matches at once (api/events&words=1), the full
// search (by meaning too) when it is done. The rows shown stay where they are and keep the keyboard, the ones the full
// search leaves out go, and its others come in under them: in the end the same messages as the full search alone.
const dashboard=await dashboardPage();
const ev=(id,title)=>({id,account_id:'mail',kind:'gmail.message',title,body:title,occurred_at:'2026-01-0'+(id%9+1)+'T10:00:00Z',metadata:{from:'Sam <sam@example.org>'}});
const A=ev(1,'Contract draft'),B=ev(2,'Signed contract'),C=ev(3,'Contract typo'),D=ev(4,'Agreement for the deal'),E=ev(5,'Paperwork to sign'),F=ev(6,'Legal review');
const WORDS=[A,B,C],FULL=[B,D,A,E,F];  // C: a keyword hit the full search ranks out
let gate,open,asked=[],statusGo;
// The first status (with the owner's dates: Fri 2 Jan, not Fri, Jan 2) comes after the keyword matches, as a cold one can
const statusHeld=new Promise(r=>statusGo=r);
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){await statusHeld;res.end(JSON.stringify({locale:{locale:'en-BE',date_locale:'en-GB',hour12:false,language:'en',language_set:true},suggestions:[],promises:[],connectors:[{id:'mail',service:'gmail',display_name:'mail',email:'owner@example.org',boundary:'work',state:'{}'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/events'){const q=url.searchParams.get('q')||'',words=url.searchParams.get('words')==='1';asked.push([q,words]);
  if(!q){res.end('[]');return}
  if(words){res.end(JSON.stringify(WORDS));return}
  await gate;res.end(JSON.stringify(FULL));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({found:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1280,height:900},locale:'en-US'}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>typeof palFind==='function'&&typeof msgSearch==='function');
 // The palette: the keyword matches first, See all results still looking; the keyboard on the second one
 gate=new Promise(r=>open=r);
 await page.keyboard.press('Control+k');await page.locator('#palette').waitFor();await page.keyboard.type('contract');
 const msgs=()=>page.evaluate(()=>[...document.querySelectorAll('#pal-list .pal-item')].map(o=>o.querySelector('.pal-label').textContent).filter(l=>!/See all results/.test(l)));
 const subs=()=>page.evaluate(()=>[...document.querySelectorAll('#pal-list .pal-item small')].map(s=>s.textContent).filter(s=>/Sam/.test(s)));
 const owners=list=>list.every(s=>/ · (Today|Yesterday|[A-Z][a-z]{2} \d{1,2} [A-Z][a-z]{2}) \d\d:\d\d$/.test(s));  // Fri 2 Jan 11:00
 // The keyword matches wait for the owner's date format: nothing drawn in the US one before the status is in
 await page.waitForFunction(()=>performance.getEntriesByType('resource').some(e=>/words=1/.test(e.name)&&e.responseEnd>0));
 await page.evaluate(()=>new Promise(r=>setTimeout(r,200)));
 assert.deepEqual(await msgs(),[],'no keyword rows before the date format is known');
 statusGo();
 await page.waitForFunction(()=>/Signed contract/.test(document.querySelector('#pal-list').textContent));
 assert.deepEqual(await msgs(),['Contract draft','Signed contract','Contract typo']);
 const early=await subs();assert.equal(early.length,3);assert.ok(owners(early),'the keyword step in the owner\'s date format: '+early);
 assert.match(await page.locator('#pal-list .pal-item').last().textContent(),/Looking/);
 await page.keyboard.press('ArrowDown');const on=await page.locator('#pal-list [aria-selected="true"] .pal-label').textContent();
 // The full search: what stays keeps its place and the keyboard, the left-out one goes, the rest under them
 open();await page.waitForFunction(()=>/Agreement for the deal/.test(document.querySelector('#pal-list').textContent));
 assert.deepEqual(await msgs(),['Contract draft','Signed contract','Agreement for the deal','Paperwork to sign'],'the full search\'s top four');
 assert.equal(await page.locator('#pal-list [aria-selected="true"] .pal-label').textContent(),on,'the keyboard stays on its row');
 assert.doesNotMatch(await page.locator('#pal-list .pal-item').last().textContent(),/Looking/);
 const late=await subs();assert.ok(owners(late),'the full search in the same format: '+late);
 assert.equal(late[0],early[0],'a row reads the same in both steps');
 await page.keyboard.press('Escape');
 // The results page: the same two steps; the rows shown are the same rows, not drawn again
 gate=new Promise(r=>open=r);
 await page.evaluate(()=>msgSearch('contract'));await page.waitForFunction(()=>document.querySelectorAll('#results article').length===3);
 const titles=()=>page.locator('#results article h3').allTextContents();
 assert.deepEqual(await titles(),['Contract draft','Signed contract','Contract typo']);
 await page.evaluate(()=>{for(const a of document.querySelectorAll('#results article'))a.dataset.first='1'});
 open();await page.waitForFunction(()=>/Legal review/.test(document.querySelector('#results').textContent));
 assert.deepEqual(await titles(),['Contract draft','Signed contract','Agreement for the deal','Paperwork to sign','Legal review']);
 assert.equal(await page.locator('#results article[data-first]').count(),2,'the rows shown stay as they were');
 // An older search's answer never lands on a newer one
 gate=new Promise(r=>open=r);
 await page.evaluate(()=>msgSearch('contract'));await page.waitForFunction(()=>document.querySelectorAll('#results article').length===3);
 await page.evaluate(()=>msgSearch(''));open();await page.waitForFunction(()=>/No matching messages/.test(document.querySelector('#results').textContent));
 await page.evaluate(()=>new Promise(r=>setTimeout(r,200)));
 assert.equal(await page.locator('#results article').count(),0);
 assert.ok(asked.some(([q,w])=>q==='contract'&&w)&&asked.some(([q,w])=>q==='contract'&&!w));
 assert.ok(!asked.some(([q,w])=>!q&&w),'no keyword step for the newest list');
 assert.deepEqual(errors,[]);
 await context.close();
 console.log('search two-step dashboard ok');
}finally{await browser?.close();server.close()}
