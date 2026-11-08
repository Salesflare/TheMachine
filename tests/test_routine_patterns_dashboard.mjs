import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A routine suggested from what the owner does (routine_patterns.py) says what was seen at the end of its rhythm line
// ("Weekly on Monday · 8:00 AM · Asked 4 times in a row"), in the owner's language; a suggestion from an OpenClaw job has none.
// Its preview renders as Markdown, a real list.
// The section's line names OpenClaw only when every suggestion came from it. SHOTS=<folder> also saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),SID='e5'.repeat(16),OID='f6'.repeat(16);
const pattern={id:SID,name:'Monday tickets',instructions:'Sum up the open support tickets from the past week',rule:{unit:'week',n:1},anchor:'2026-11-09',at:'08:00',
 state:'suggested',next_due:null,from_openclaw:false,why:{kind:'ask',n:4},
 runs:[{id:'r1',state:'ready',started_at:now,result:'**3 open tickets**, 1 urgent: login fails on the phone app.\n- 2 waiting on a reply\n- 1 new since Friday'}]};
const openclaw={...pattern,id:OID,name:'Dev summary',instructions:'Sum up what each developer shipped',from_openclaw:true,why:null,runs:[]};
let suggested=[pattern],language='en';
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:language==='nl'?'nl-BE':'en-US',region:'US',language,language_set:true,clock:'auto',hour12:language==='en',auto_hour12:true,date_locale:language==='nl'?'nl-BE':'en-US',languages:{en:'English',nl:'Nederlands'},saveable:true}});
const catalog=async lang=>(await import('node:fs/promises')).readFile(new URL(`../i18n/${lang}.json`,import.meta.url),'utf8');
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/routines'){res.end(JSON.stringify({routines:[],suggested}));return}
 const lang=url.pathname.match(/\/i18n\/([a-zA-Z-]+)\.json$/);if(lang){res.end(await catalog(lang[1]));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]])for(const scheme of ['light','dark']){
  suggested=[pattern];
  const context=await browser.newContext({viewport:{width,height},timezoneId:'Europe/Brussels',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
  const s=page.locator(`.rt-sugg [data-rt="${SID}"]`);await s.waitFor();
  assert.match(await s.locator('.rt-when').innerText(),/ · Asked 4 times in a row$/);
  assert.equal(await s.locator('.rt-run li').count(),2,'the preview list renders as a list');
  assert.equal(await page.locator('.rt-sugg>.fine').innerText(),'Each one ran once to show you.');
  const box=await s.boundingBox();assert.ok(box.x>=0&&box.x+box.width<=width,'the suggestion fits the screen');
  if(process.env.SHOTS)await page.screenshot({path:`${process.env.SHOTS}/pattern-${width}-${scheme}.png`,fullPage:true});
  if(width===390&&scheme==='light'){
   // An OpenClaw suggestion says nothing extra; with only those, the section names OpenClaw
   suggested=[openclaw];await page.evaluate(()=>routinesView(true));
   await page.locator(`.rt-sugg [data-rt="${OID}"]`).waitFor();
   assert.doesNotMatch(await page.locator('.rt-when').innerText(),/in a row|every week|a week/);
   assert.equal(await page.locator('.rt-sugg>.fine').innerText(),'From your OpenClaw jobs. Each one ran once to show you.');
   // Every kind words its own line
   for(const [why,line] of [[{kind:'sent',n:5},'Sent 5 times in a row'],[{kind:'mail',n:3},'3 senders every week'],
                            [{kind:'slack',n:40},'About 40 messages a week']]){
    suggested=[{...pattern,why}];await page.evaluate(()=>routinesView(true));
    await page.locator(`.rt-sugg [data-rt="${SID}"]`).waitFor();
    assert.ok((await page.locator('.rt-when').innerText()).endsWith(' · '+line),line);
   }
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('routine pattern suggestions ok');
}finally{await browser?.close();server.close()}
