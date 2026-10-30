import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A ready card whose run worked on a page in the Machine's browser opens that page there (View in browser), not in
// your own browser: the link is the browser's viewer and the click asks the service to bring the task's tab to the
// front. A link the run added to that site does the same. A final click left to you says so in the status line, and
// then the page leads instead of Mark done. #browser-for=<task> (from Telegram) does it and goes on to the viewer.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[
 {id:'aaaaaaaaaaaaaaa1',title:'Get the quarterly report ready',body:'Filled in the report.',status:'prepared',scope:'work',created_at:now,event_ids:[1],
  outcome:JSON.stringify({state:'your_step',step:'submit'}),browser_view:{label:'View in browser',site:'portal.example'}},
 {id:'aaaaaaaaaaaaaaa2',title:'Check the grant form',body:'Saved a draft.',status:'prepared',scope:'work',created_at:now,event_ids:[2],outcome:JSON.stringify({state:'done'}),
  next_actions:[{kind:'open',label:'Open draft report',url:'https://my.example/#browser-for=aaaaaaaaaaaaaaa2',browser:true,site:'grants.example',revision:'r1'},
                {kind:'open',label:'Open guidelines',url:'https://docs.example/guide',revision:'r2'}]},
 {id:'aaaaaaaaaaaaaaa3',title:'Look up the venue hours',body:'Open 9 to 5.',status:'prepared',scope:'work',created_at:now,event_ids:[3],outcome:JSON.stringify({state:'done'})}];
let viewer='https://my.example/browser/vnc.html?autoconnect=1';
const shown=[];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},browser_link:viewer});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const a=JSON.parse(body);if(a.action==='browser_show'){shown.push(a.args.suggestion_id);res.end(JSON.stringify({shown:true,opened:false,site:'portal.example',view:viewer?'/viewer-landed':null}));return}}
 if(url.pathname==='/viewer-landed'){res.setHeader('Content-Type','text/html');res.end('<p id="landed">viewer</p>');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1280,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);await page.locator('#task-aaaaaaaaaaaaaaa1').waitFor();
 // Left for you to submit: the status line says so, View in browser leads, Mark done does not
 assert.deepEqual(await page.locator('#task-aaaaaaaaaaaaaaa1 .status-line').allTextContents(),['Ready for you to check and submit.']);
 const view=page.locator('#task-aaaaaaaaaaaaaaa1 a[data-browser-show]');
 assert.equal(await view.textContent(),'View in browser ↗');
 assert.equal(await view.getAttribute('href'),viewer);
 assert.ok((await view.getAttribute('class')).includes('primary'));
 assert.notEqual(await page.locator('#task-aaaaaaaaaaaaaaa1 [data-choice="complete"]').getAttribute('class'),'primary');
 assert.ok(!(await page.locator('#task-aaaaaaaaaaaaaaa1').innerText()).includes('Finished'));
 // The click opens the viewer in a new tab and asks for the task's own tab in front
 const [popup]=await Promise.all([context.waitForEvent('page'),view.click()]);await popup.close();
 await page.waitForFunction(()=>true);await new Promise(r=>setTimeout(r,200));
 assert.deepEqual(shown,['aaaaaaaaaaaaaaa1']);
 // The run's own link to that site goes through the Machine's browser too; another link stays a plain link
 const own=page.locator('#task-aaaaaaaaaaaaaaa2 a[data-browser-show]');
 assert.equal(await own.count(),1);assert.equal(await own.textContent(),'Open draft report ↗');assert.equal(await own.getAttribute('href'),viewer);
 assert.equal(await page.locator('#task-aaaaaaaaaaaaaaa2 a.open:not([data-browser-show])').getAttribute('href'),'https://docs.example/guide');
 assert.equal(await page.locator('#task-aaaaaaaaaaaaaaa2 a:has-text("View in browser")').count(),0);  // said once
 assert.deepEqual(await page.locator('#task-aaaaaaaaaaaaaaa2 .status-line').allTextContents(),['Finished. Mark it done if it looks right.']);
 // No browser work: no link
 assert.equal(await page.locator('#task-aaaaaaaaaaaaaaa3 [data-browser-show]').count(),0);
 // Without a viewer the click only brings the tab to the front, and says so
 viewer=null;await page.reload();await page.locator('#task-aaaaaaaaaaaaaaa1').waitFor();
 assert.equal(await page.locator('#task-aaaaaaaaaaaaaaa1 a[data-browser-show]').getAttribute('href'),'#');
 await page.locator('#task-aaaaaaaaaaaaaaa1 a[data-browser-show]').click();
 await page.locator('#toast.show').waitFor();assert.match(await page.locator('#toast').textContent(),/in front in your Machine’s browser/);
 assert.equal(page.url(),base+'/');
 // From Telegram: #browser-for=<task> shows it and goes on to the viewer
 viewer='https://my.example/browser/vnc.html';
 const fresh=await context.newPage();fresh.on('pageerror',e=>errors.push(e.message));await fresh.goto(base+'/#browser-for=aaaaaaaaaaaaaaa2');await fresh.locator('#landed').waitFor();
 assert.deepEqual(shown,['aaaaaaaaaaaaaaa1','aaaaaaaaaaaaaaa1','aaaaaaaaaaaaaaa2']);
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('browser view dashboard ok');
