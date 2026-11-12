import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A routine's to-do whose note holds for the routine's next runs too (routine_changes.py): it offers Also change the
// routine; that shows what changes in the routine's words (Now / New, only the part that differs) and saves nothing
// until Change it (routine_change_save), which says "Changed the routine …". Keep it as is drops the offer
// (routine_change_keep). A to-do without an offer, or a closed one, shows none.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const card=(id,more)=>({id,title:'Post on X about the faster search',body:'Search got faster this week.',status:'pending',scope:'work',created_at:now,event_ids:[1],
  source_line:'Source: your routine Check what shipped · Mon, Nov 9',...more});
const cards=[card('rc1',{routine_change:{name:'Check what shipped',old:'',new:'Never use emoji.'}}),
 card('rc2',{routine_change:{name:'Weekly numbers',old:'Keep it under 280 characters.',new:'Keep it under 200 characters.'}}),
 card('rc3',{}),card('rc4',{status:'completed',routine_change:{name:'Check what shipped',old:'',new:'x'}})];
const posted=[];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const b=JSON.parse(body);posted.push(b);
  if(b.action.startsWith('routine_change_'))delete cards.find(c=>c.id===b.args.suggestion_id).routine_change;
  res.end(JSON.stringify(b.action==='routine_change_save'?{saved:true,line:'Changed the routine Check what shipped'}:{kept:true}));return}
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
 const one=page.locator('#task-rc1');await one.waitFor();
 const offer=one.locator('button.rt-offer');
 assert.equal((await offer.innerText()).trim(),'Also change the routine');
 assert.equal(await page.locator('#task-rc3 .rt-offer').count(),0,'no offer: as before');
 assert.equal(await page.locator('.rt-offer').count(),2,'a closed one offers nothing');
 // The offer opens what changes; nothing is saved yet
 await offer.click();
 const confirm=one.locator('.change-editor');await confirm.waitFor();
 assert.equal((await confirm.locator('p').first().innerText()).trim(),'Change the routine Check what shipped?');
 assert.deepEqual(await confirm.locator('.rt-part span').allInnerTexts(),['New']);
 assert.equal(await confirm.locator('ins').innerText(),'Never use emoji.');
 assert.equal(await confirm.locator('del').count(),0,'an addition only: no Now');
 assert.equal(await page.evaluate(()=>document.activeElement?.textContent),'Change it');
 assert.equal(posted.length,0);
 // A change in the words: the old part struck through, the new one under it
 await page.locator('#task-rc2 .rt-offer').click();
 const two=page.locator('#task-rc2 .change-editor');await two.waitFor();
 assert.equal(await two.locator('del').innerText(),'Keep it under 280 characters.');
 assert.equal(await two.locator('ins').innerText(),'Keep it under 200 characters.');
 // Change it saves through the routine's edit path and says so; the offer is gone
 await one.getByRole('button',{name:'Change it'}).click();
 await page.locator('#toast',{hasText:'Changed the routine Check what shipped'}).waitFor();
 assert.deepEqual(posted.at(-1),{action:'routine_change_save',args:{suggestion_id:'rc1'}});
 await page.waitForFunction(()=>!document.querySelector('#task-rc1 .rt-offer,#task-rc1 .change-editor'));
 // Keep it as is drops the offer, the routine as it was
 await page.locator('#task-rc2').getByRole('button',{name:'Keep it as is'}).click();
 await page.waitForFunction(()=>!document.querySelector('#task-rc2 .rt-offer,#task-rc2 .change-editor'));
 assert.deepEqual(posted.at(-1),{action:'routine_change_keep',args:{suggestion_id:'rc2'}});
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
