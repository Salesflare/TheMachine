import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A person's summary sits on top of their page, under the line on how you're in touch: a few lines, each with its
// sources (a message by its date, a promise, your note). Edit opens the lines as one field; Save sends them as lines.
// While your edit holds, a rewrite shows as a suggested update with Use it and Keep mine. No summary, no section.
// At 390 and 1440 (900 and 700 high), light and dark. SHOT_DIR=… saves screenshots.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()+n*864e5).toISOString();
const LINES=[
 {kind:'who',text:'Runs the Northwind academy; a partner on the alloy course.',sources:[{type:'event',id:41,kind:'email',at:day(-20)},{type:'fact',id:7,text:'Leads the Northwind academy'}]},
 {kind:'now',text:'Course dates agreed for spring; the venue is still open.',sources:[{type:'event',id:42,kind:'meeting',at:day(-3)}]},
 {kind:'open',text:'You owe them the draft program by Friday.',sources:[{type:'promise',id:9,open:true}]},
];
const fresh=()=>({id:'email:mara.ellison@eu.northwind.example',kind:'person',name:'Mara Ellison',strength:4.2,closeness:'close',last_at:day(-1),signals:180,
 ids:['mara.ellison@eu.northwind.example'],usual_gap_days:2,quiet:false,role:'partner',role_by:'owner',org:'org:eu.northwind.example',org_name:'Northwind',
 org_by:'email',side:'work',edited:[],phones:[],emails:[{value:'mara.ellison@eu.northwind.example',by:'messages'}],profile:{title:'Academy lead'},
 links:[],recent:[],around:[],open:{},summary:{lines:LINES,by:'machine',at:day(-1)}});
let person=fresh();const calls=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')?person:{projects:[],people:[person],quiet:[],new:[],orgs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  const a=call.args;
  if(a.op==='edit')person={...person,summary:{lines:a.lines.map(text=>({kind:'',text,sources:[{type:'owner'}]})),by:'owner',at:day(0),
   proposal:[{kind:'now',text:'Course dates agreed; the venue is booked.',sources:[{type:'event',id:43,kind:'email',at:day(0)}]}]}};
  if(a.op==='keep')person={...person,summary:{...person.summary,proposal:undefined}};
  res.end(JSON.stringify({summary:person.summary}));return}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 if(process.env.SHOT_DIR)await mkdir(process.env.SHOT_DIR,{recursive:true});
 for(const [width,height,scheme] of [[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,700,'dark']]){
  person=fresh();calls.length=0;
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,deviceScaleFactor:width<500?2:1,timezoneId:'America/New_York'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#graph/'+encodeURIComponent(person.id));
  const card=page.locator('#people-view .person-page');await card.waitFor();
  const tag=`${width}x${height} ${scheme}`,box=card.locator('.person-summary');
  // On top, right under the line on how you're in touch.
  assert.equal(await card.locator('.detail-section h4').first().textContent(),'Summary',tag);
  assert.equal(await box.evaluate(e=>e.previousElementSibling?.classList.contains('person-rel')),true);
  assert.deepEqual(await box.locator('.summary-lines .sl-text').allTextContents(),LINES.map(l=>l.text));
  // Each line traces to its sources: a message opens by its date, a promise links, a note shows its text.
  const first=box.locator('.summary-lines li').first();
  assert.equal(await first.locator('[data-quote-event="41"]').count(),1);
  assert.equal(await first.locator('span[title="Leads the Northwind academy"]').textContent(),'Your note');
  assert.equal(await box.locator('a[href="#promise/9"]').textContent(),'Promise');
  assert.equal(await box.locator('.sl-text[translate="no"]').count(),3,'model text is never machine-translated');
  assert.match(await box.locator('.summary-meta').textContent(),/^Updated \w+, \w+ \d+$/);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll at '+tag);
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/summary-${width}x${height}-${scheme}.png`});
  // Edit: the lines as one field; Cancel sends nothing.
  await box.locator('[data-summary-edit]').click();
  const ta=box.locator('textarea[name=lines]');await ta.waitFor();
  assert.equal(await ta.inputValue(),LINES.map(l=>l.text).join('\n'));
  assert.ok(!(await box.locator('.summary-lines').first().isVisible()),'the lines step aside while editing');
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/summary-edit-${width}x${height}-${scheme}.png`});
  await box.locator('[data-summary-cancel]').click();assert.equal(calls.length,0);
  assert.ok(await box.locator('.summary-lines').first().isVisible());
  // Save sends the lines, blank ones left out; the owner's version shows with the suggested update under it.
  await box.locator('[data-summary-edit]').click();
  await ta.fill('Runs the Northwind academy.\n\n  Spring course, venue open.  ');
  await box.locator('.summary-form button:not([type])').click();
  await card.locator('.summary-proposal').waitFor();
  assert.deepEqual(calls[0],{action:'graph_summary',args:{node_id:person.id,op:'edit',lines:['Runs the Northwind academy.','Spring course, venue open.']}});
  const after=card.locator('.person-summary');
  assert.equal(await after.locator('.summary-meta').textContent(),'Edited by you');
  assert.equal(await after.locator('.summary-proposal b').textContent(),'Suggested update');
  assert.deepEqual(await after.locator('.summary-proposal [data-summary-op]').allTextContents(),['Use it','Keep mine']);
  assert.equal(await after.locator('[data-summary-op="reset"]').textContent(),'Let The Machine write it');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll with a proposal at '+tag);
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/summary-proposal-${width}x${height}-${scheme}.png`});
  await after.locator('[data-summary-op="keep"]').click();
  await card.locator('.summary-proposal').waitFor({state:'detached'});
  assert.deepEqual(calls[1],{action:'graph_summary',args:{node_id:person.id,op:'keep'}});
  // No summary yet: no section at all.
  person={...fresh(),summary:null};
  await page.evaluate(()=>people(graphNode,true));await card.locator('.person-summary').waitFor({state:'detached'});
  assert.deepEqual(errors,[]);await context.close();
 }
 console.log('person summary dashboard ok');
}finally{await browser?.close();server.close()}
