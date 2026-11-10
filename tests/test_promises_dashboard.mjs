import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Promises list on the To-dos page: both directions, due chips, one ⋯ on every one still open with Do it (theirs:
// Nudge), Mark done and Not happening (a to-do one too, its to-do closes with it), and "a to-do now" opens that to-do.
const dashboard=await dashboardPage();
const day=n=>{const d=new Date();d.setDate(d.getDate()+n);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')};
const made=new Date(Date.now()-2*864e5).toISOString(),check=new Date(Date.now()+864e5).toISOString();
let promises=[
 {id:1,direction:'mine',who:'Alex Morgan',what:'send the Q3 deck with the updated pricing for the Globex renewal',due:day(0),state:'open',made_at:made,check_at:check},
 {id:2,direction:'theirs',who:'Sam Lee',what:'send the signed contract',due:day(-1),state:'card',suggestion_id:'c2',made_at:made,check_at:check},
 {id:3,direction:'theirs',who:'Kim',what:'get back about the pilot',due:null,state:'open',made_at:made,check_at:check},
 {id:4,direction:'mine',who:'Old',what:'already kept',due:null,state:'kept',made_at:made,check_at:check}];
const state=()=>({suggestions:[],promises,connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]});
const calls=[],errors=[];let failNext=false;
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(failNext){failNext=false;res.statusCode=400;res.end(JSON.stringify({error:'This promise is no longer open'}));return}
  res.end(call.action==='promise_todo'?JSON.stringify({id:call.args.id,card:'c'+call.args.id,existing:call.args.id===2}):'{"status":"kept"}');return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 const list=page.locator('#promises-list');
 await list.waitFor();
 assert.equal(await list.locator('summary .count').textContent(),'3');  // closed ones stay out
 await list.locator('#promises-head').click();
 assert.deepEqual(await list.locator('.promise-head').allTextContents(),['You promised1','Promised to you2']);
 const text=await list.textContent();
 assert.ok(text.includes('To Alex Morgan: send the Q3 deck')&&text.includes('Due today'));
 assert.ok(text.includes('From Sam Lee: send the signed contract')&&text.includes('a to-do now')&&text.includes('Overdue'));
 assert.ok(text.includes('no date, follow-up')&&!text.includes('no date, checked'));  // check_at is tomorrow: the planned follow-up, not a check that happened
 assert.equal(await list.locator('[data-promise="2"]').count(),2);  // Mark done and Not happening, its to-do closes with it
 // No buttons on the rows: one ⋯ each, its items hidden until it opens
 assert.equal(await list.locator('.promise > button').count(),0);
 assert.equal(await list.locator('details.promise-menu').count(),3);
 assert.equal(await list.locator('[data-promise="1"]').first().isVisible(),false);
 const menu=async id=>{const d=list.locator('.promise').filter({has:page.locator(`[data-promise-todo="${id}"]`)}).locator('details.promise-menu');await d.locator('summary').click();
  return (await d.locator('[role="menuitem"]').allInnerTexts()).map(x=>x.replace(/\s+/g,' ').trim())};
 assert.deepEqual(await menu(1),['Do it Make it a to-do and prepare it','Mark done It was kept','Not happening It won’t happen. Stop tracking it']);
 assert.deepEqual(await menu(3),['Nudge Draft a short follow-up for you to send','Mark done It was kept','Not happening It won’t happen. Stop tracking it']);
 assert.equal(await list.locator('details.promise-menu[open]').count(),1);  // opening one closes the other
 assert.deepEqual((await menu(2))[0],'Nudge Open its to-do');  // a to-do already: Nudge opens it
 await page.keyboard.press('Escape');
 assert.equal(await list.locator('details.promise-menu[open]').count(),0);
 assert.equal(await list.locator('a.promise-todo[href="#chat=c2"]').textContent(),'a to-do now');  // the to-do it is now
 const widths=[];
 for(const width of [320,390,768]){
  await page.setViewportSize({width,height:844});
  const sizes=await page.evaluate(()=>({page:document.documentElement.scrollWidth,viewport:innerWidth,list:document.querySelector('#promises-list').getBoundingClientRect().right}));
  assert.ok(sizes.page<=sizes.viewport&&sizes.list<=sizes.viewport,'overflow at '+width);widths.push({width,...sizes});
  if(process.env.PROMISES_SHOT)await list.screenshot({path:process.env.PROMISES_SHOT+'-'+width+'.png'});
 }
 // Nudge: its to-do is made and prepared on the Machine while the owner stays on the list. A second click while it asks
 // sends nothing more; a toast says a draft is coming, with Open to-do; the row then shows "a to-do now".
 const hashBefore=await page.evaluate(()=>location.hash);
 // A failed ask says why in the toast, on the list, and the item works again
 failNext=true;await menu(3);await list.locator('[data-promise-todo="3"]').click();
 await page.locator('#toast.show.error').waitFor();
 assert.ok((await page.locator('#toast').textContent()).includes('This promise is no longer open'));
 assert.equal(await page.evaluate(()=>location.hash),hashBefore);
 await page.waitForFunction(()=>!document.querySelector('[data-promise-todo="3"]').disabled);
 calls.length=0;await page.evaluate(()=>$('#toast').classList.remove('show'));
 await menu(3);
 await list.locator('[data-promise-todo="3"]').evaluate(b=>{b.click();b.click()});
 for(let i=0;i<100&&!calls.length;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls[0],{action:'promise_todo',args:{id:3}});
 promises=promises.map(p=>p.id===3?{...p,state:'card',suggestion_id:'c3'}:p);
 const toastEl=page.locator('#toast.show');
 await toastEl.waitFor();
 assert.equal((await toastEl.textContent()).trim(),'Drafting a nudge for you to send. Open to-do');
 assert.ok(!(await toastEl.getAttribute('class')).includes('error'));
 assert.equal(await page.evaluate(()=>location.hash),hashBefore);  // no chat, no page change
 assert.ok(await page.locator('#promises-list').evaluate(d=>d.open));
 assert.equal(calls.filter(c=>c.action==='promise_todo').length,1);
 await page.evaluate(()=>refresh());
 assert.equal(await list.locator('a.promise-todo[href="#chat=c3"]').textContent(),'a to-do now');
 if(process.env.PROMISES_SHOT)await page.screenshot({path:process.env.PROMISES_SHOT+'-toast.png'});
 // Open to-do in the toast opens it
 await toastEl.locator('[data-toast-open="c3"]').click();
 await page.waitForFunction(()=>location.hash==='#card=c3');
 await page.evaluate(()=>{location.hash=''});
 if(!await page.locator('#promises-list').evaluate(d=>d.open))await page.locator('#promises-head').click();
 // Nudge on one that is a to-do already ("Open its to-do"): its chat opens, as before
 await menu(2);await list.locator('[data-promise-todo="2"]').click();
 await page.waitForFunction(()=>location.hash==='#chat=c2');
 await page.evaluate(()=>history.back());await page.waitForFunction(()=>location.hash!=='#chat=c2');
 if(!await page.locator('#promises-list').evaluate(d=>d.open))await page.locator('#promises-head').click();
 const n=calls.length;
 await menu(1);await list.locator('[data-promise="1"][data-close="kept"]').click();
 for(let i=0;i<100&&calls.length<=n;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls[n],{action:'promise_close',args:{id:1,status:'kept'}});
 promises=promises.map(p=>p.id===1?{...p,state:'kept'}:p);await page.evaluate(()=>refresh());
 assert.equal(await page.locator('#promises-list summary .count').textContent(),'2');
 assert.ok(await page.locator('#promises-list').evaluate(d=>d.open));  // stays open across refresh
 promises=[];await page.evaluate(()=>refresh());
 assert.equal(await page.locator('#promises-list').count(),0);
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({widths,close_requests:calls.length,page_errors:errors}));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r))}
