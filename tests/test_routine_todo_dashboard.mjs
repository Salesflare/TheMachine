import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do a routine made (its draft, routines_app.py routine_draft_todo; machine/store/views.py routine_view): its source line
// says it is the routine's ("From your routine Check what shipped"), the name a link that opens that routine on the Routines
// page, in view and marked; its lead button names the step (Post it), not Do it. A routine gone from the page: its name, no
// link.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),ID='c3'.repeat(16),OTHER='e5'.repeat(16);
const cards=[{id:'rt1',title:'Post on X about the faster search',body:'Search is faster now: results show as you type.',status:'pending',scope:'work',created_at:now,event_ids:[1],
  source_line:'Source: your routine Check what shipped · Mon, Nov 9',routine:{id:ID,name:'Check what shipped',live:true},labels:{accept:'Post it'}},
 {id:'rt2',title:'Email the team this week’s numbers',body:'Signups are up 12% this week.',status:'pending',scope:'work',created_at:now,event_ids:[2],
  source_line:'Source: your routine Weekly numbers · Mon, Nov 9',routine:{id:OTHER,name:'Weekly numbers',live:false}}];
const routine=(id,name)=>({id,name,instructions:name,rule:{unit:'week',n:1},anchor:'2026-11-09',at:'09:00',state:'on',next_due:'2026-11-16',runs:[]});
const routines=[...Array.from({length:6},(_,i)=>routine(String(i).repeat(32),'Routine '+(i+1))),routine(ID,'Check what shipped')];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/routines'){res.end(JSON.stringify({routines,suggested:[],trying:[]}));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 const card=page.locator('#task-rt1');await card.waitFor();
 assert.match(await card.locator('.card-source .source').innerText(),/^From your routine Check what shipped · Mon,? (Nov 9|9 Nov)$/);
 assert.equal(await card.locator('.card-source .read-original').count(),0,'the draft is the to-do itself: no original to read');
 assert.equal(await card.locator('.card-source a.rt-link').getAttribute('href'),'#routines/'+ID);
 assert.equal((await card.locator('.actions>button.primary').first().innerText()).trim(),'Post it');
 // A routine gone from the page: its name, no link; no step named: Do it
 const gone=page.locator('#task-rt2');
 assert.match(await gone.locator('.card-source .source').innerText(),/^From your routine Weekly numbers · /);
 assert.equal(await gone.locator('.card-source a').count(),0);
 assert.equal((await gone.locator('.actions>button.primary').first().innerText()).trim(),'Do it');
 // The link opens the Routines page with that routine in view, marked
 await card.locator('a.rt-link').click();
 const mine=page.locator(`#routines-view article[data-rt="${ID}"]`);await mine.waitFor();
 await page.waitForFunction(id=>document.querySelector(`article[data-rt="${id}"]`)?.classList.contains('rt-found'),ID);
 assert.equal(await page.evaluate(()=>location.hash),'#routines');
 assert.equal(await page.evaluate(id=>document.activeElement?.dataset.rt,ID),ID);
 const box=await mine.boundingBox();assert.ok(box.y>=0&&box.y+box.height/2<=844,'in view');
 // A link to a routine that isn't there says so
 await page.evaluate(id=>{location.hash='#routines/'+id},OTHER);
 await page.locator('.toast',{hasText:'That routine is gone'}).waitFor();
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
