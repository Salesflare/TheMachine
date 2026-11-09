import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The last check of new email above the to-dos (dashboard/todos-mail-check.js, state.mail_check from check_now.mail_check):
// "Checked 12 new emails at 16:11 · nothing needs you", a to-do held until later, and on a tap one row per thread with
// who, the subject and its to-do or the review's reason. Made-up names; nothing is sent.
const dashboard=await dashboardPage();
const NOW=Date.parse('2026-11-09T16:20:00Z'),at=m=>new Date(NOW+m*6e4).toISOString();
const quiet={at:at(-9),emails:12,todos:0,held:0,held_until:null,more:0,threads:[
 {from:'Robin Vale',subject:'Re: Trial seats',why:'Only cc’d, Robin is answering'},
 {from:'Yara Oak',subject:'Re: Coffee next week',why:'Coffee already set for Thursday 10:00'},
 {from:'Fieldnote Weekly',subject:'This week in tools'},
 {from:'Lee Ash',subject:'Invoice question',later:true}]};
const busy={...quiet,todos:2,held:1,held_until:'2026-11-10T08:30:00Z',more:3,threads:[
 {from:'Mila Under',subject:'Pricing for our team',todo:'Send Mila annual pricing',held_until:'2026-11-10T08:30:00Z'},
 {from:'Jonah Kett',subject:'API limits',todo:'Answer Jonah about API limits'},...quiet.threads]};
let mail=quiet;
const state=()=>({suggestions:[{id:'a1'.repeat(8),title:'Answer Jonah about API limits',body:'',status:'prepared',scope:'work',created_at:at(-10),event_ids:[1]}],
 promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{last_completed:at(-9)},review_runs:[],review_live:{runs:[]},connectors:[],
 check:{reviewed:at(-9),waiting:0},mail_check:mail,
 locale:{locale:'en-GB',region:'GB',language:'en',language_set:true,clock:'24',hour12:false,auto_hour12:false,date_locale:'en-GB',languages:{en:'English'},saveable:true}});
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},locale:'en-GB',timezoneId:'UTC'});
 await context.clock.setFixedTime(NOW);
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/');
 const line=page.locator('#suggestions .mail-check .mc-line');await line.waitFor();
 assert.equal((await line.innerText()).trim(),'Checked 12 new emails at 16:11 · nothing needs you');
 assert.equal(await line.getAttribute('aria-expanded'),'false');
 assert.equal(await page.locator('#suggestions .mc-list').count(),0,'folded until tapped');
 // A tap: one row per thread, its reason or nothing when the check gave none worth showing
 await line.click();await page.locator('#suggestions .mc-list').waitFor();
 assert.equal(await page.locator('#suggestions .mail-check .mc-line').getAttribute('aria-expanded'),'true');
 const rows=()=>page.locator('#suggestions .mc-list li').evaluateAll(n=>n.map(li=>li.innerText.replace(/\s+/g,' ').trim()));
 assert.deepEqual(await rows(),['Robin Vale Re: Trial seats Only cc’d, Robin is answering','Yara Oak Re: Coffee next week Coffee already set for Thursday 10:00',
  'Fieldnote Weekly This week in tools','Lee Ash Invoice question Read again in the next check']);
 const box=await page.locator('#suggestions .mail-check').boundingBox();assert.ok(box.x+box.width<=390,'fits a phone');
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=390),'no sideways scroll on a phone');
 // New to-dos, one held for the morning: the line says until when, and so does its row
 mail=busy;await page.evaluate(()=>refresh());
 await page.waitForFunction(()=>/new to-do/.test(document.querySelector('#suggestions .mc-line')?.textContent||''));
 assert.equal((await page.locator('#suggestions .mc-line').innerText()).trim(),'Checked 12 new emails at 16:11 · 2 new to-dos · 1 to-do held until tomorrow 08:30');
 assert.deepEqual((await rows()).slice(0,2),['Mila Under Pricing for our team Held until tomorrow 08:30 Send Mila annual pricing','Jonah Kett API limits New to-do Answer Jonah about API limits']);
 assert.equal((await rows()).at(-1),'And 3 more threads');
 // All new to-dos held: the held line alone
 mail={...busy,todos:1,more:0};await page.evaluate(()=>refresh());
 await page.waitForFunction(()=>!/new to-dos/.test(document.querySelector('#suggestions .mc-line')?.textContent||''));
 assert.equal((await page.locator('#suggestions .mc-line').innerText()).trim(),'Checked 12 new emails at 16:11 · 1 to-do held until tomorrow 08:30');
 // No check with new email in the last hours: no line
 mail=null;await page.evaluate(()=>refresh());await page.locator('#suggestions .mail-check').waitFor({state:'detached'});
 // A thread's words are data: markup in them stays text
 mail={...quiet,threads:[{from:'<img src=x onerror="window.__xss=1">',subject:'<b>x</b>',why:'<img src=x onerror="window.__xss=1"> was here'}]};
 await page.evaluate(()=>refresh());await page.locator('#suggestions .mc-list li').waitFor();
 assert.equal(await page.evaluate(()=>window.__xss),undefined);
 assert.deepEqual(errors,[]);
 console.log('ok: the last check of new email says what it found and why');
}finally{await browser?.close();server.close()}
