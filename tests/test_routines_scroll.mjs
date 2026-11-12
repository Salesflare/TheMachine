import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The Routines page stays put while you edit (dashboard/routines-page.js rtPatch, rtKeep): on a phone, scrolled down to a
// routine under long suggestions, Edit's Try it and the refreshes while its test runs only change that test run. Nothing
// above moves the form, even when a card above changes; a rebuild once the form closes keeps the card on screen in place.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),ID='c3'.repeat(16),LONG='**Fernwave**: release notes drafted.\n'.repeat(14);
const sugg=(i,result=LONG)=>({id:String(i).repeat(32),name:'Daily standup '+i,instructions:'Every weekday at 13:00, sum up the team standup from chat and calendar.',
 rule:{unit:'weekday',n:1},anchor:'2026-11-09',at:'13:00',state:'suggested',next_due:null,runs:[{id:'s'+i,state:'ready',started_at:now,result}]});
let suggested=[sugg(1),sugg(2)],test=null;
const mine=()=>({id:ID,name:'Shipped this week',instructions:'Check what shipped in the project repository and write a short post',rule:{unit:'week',n:1},
 anchor:'2026-11-13',at:'16:00',state:'on',next_due:'2026-11-13',runs:[{id:'r1',state:'ready',started_at:now,result:'**Three things shipped**.'}],test});
const all=()=>JSON.stringify({routines:[mine()],suggested,trying:[]});
const state={suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}};
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/routines'){res.end(all());return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);if(b.action==='routine_try')test={id:'t1',state:'running',started_at:now,trial:b.args.words};res.end(all());return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,colorScheme:'dark'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
 const card=page.locator(`[data-rt="${ID}"]`);await card.waitFor();
 // Open the long suggestions' Show more, so the routine sits far down; then Edit it, scrolled so its form ends the screen
 for(const m of await page.locator('.rt-sugg [data-more]').all())await m.click();
 await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="edit"]').click();
 await card.locator('.rt-form textarea').fill('Check what shipped in the project repository and write a short, playful post');
 await page.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));  // the end of the page, where a shorter page clamps
 const at=async()=>page.evaluate(()=>({y:scrollY,form:Math.round(document.querySelector('.rt-form').getBoundingClientRect().top)}));
 await card.locator('[data-rt-try]').click();await card.locator('.rt-form .rt-run').waitFor();
 await page.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));const before=await at();assert.ok(before.y>800,`scrolled down to the routine (${before.y})`);
 assert.match(await card.locator('.rt-form .rt-run-head').innerText(),/^Test run\s+Running…$/);
 // A refresh while it runs (the 4 s look, or any other): nothing moves; only the test run changes
 const words=await card.locator('.rt-form textarea').elementHandle();
 await page.evaluate(()=>routinesView(true));await page.waitForTimeout(100);
 assert.deepEqual(await at(),before,'a refresh while it runs keeps the page still');
 assert.equal(await words.evaluate(x=>x.isConnected),true,'the form is the same one, never rebuilt');
 // The run is ready, and a card above changes meanwhile: still nothing moves, the result shows in the form
 test={...test,state:'ready',result:'**Two things shipped** this week.'};suggested=[sugg(1,'**Short** now.'),sugg(2)];
 await page.evaluate(()=>routinesView(true));await card.locator('.rt-form .rt-result strong').waitFor();
 assert.deepEqual(await at(),before,'its result arriving keeps the page still');
 assert.equal(await card.locator('.rt-form textarea').inputValue(),'Check what shipped in the project repository and write a short, playful post');
 assert.equal(await card.locator('[data-rt-try]').isDisabled(),false);
 // Cancel: the page catches up now (the shorter card above), and the routine stays where it was on screen
 const top=await card.evaluate(x=>Math.round(x.getBoundingClientRect().top));
 await card.locator('[data-rt-cancel]').click();
 assert.equal(await page.locator('.rt-sugg article').first().locator('.rt-result').innerText(),'Short now.','rebuilt once the form closed');
 assert.ok(Math.abs(await card.evaluate(x=>Math.round(x.getBoundingClientRect().top))-top)<=1,'the routine stays where it was on screen');
 await context.close();
 assert.deepEqual(errors,[]);
 console.log('routines scroll ok');
}finally{await browser?.close();server.close()}
