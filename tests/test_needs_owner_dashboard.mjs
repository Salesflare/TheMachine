import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Prepared or Needs you: a to-do says Prepared only with a draft or result to approve. One whose run ended needing the
// owner, with nothing ready (needs_owner in its view, machine/cards.py), says Needs you in amber, with what it needs on
// its status line, and the list's "Nothing goes out until you approve it." note leaves it out. Made-up data.
// SHOTS=<folder> saves the list at 1440x900 and 390x844, light and dark.
const dashboard=await dashboardPage(process.env.PAGE);
const NOW=Date.UTC(2026,10,5,10,0,0),h=n=>new Date(NOW-n*3600e3).toISOString();
const card=(id,title,status,created_at,more={})=>({id:id.repeat(16).slice(0,16),title,body:'Made-up to-do.',status,scope:'work',event_ids:[],created_at,...more});
const DRAFT={kind:'email',label:'Send reply',account_id:'work',to:['pat@example.com'],subject:'Re: Pilot',body:'Hi Pat,\n\nThursday works.\n\nAlex',revision:'r1'};
const NEED='Which of the two quotes should it accept?';
let ready=true;
const cards=()=>[
 card('q','Pick a quote for the new printer','prepared',h(1),{outcome:JSON.stringify({state:'needs_you',needs:NEED}),needs_owner:NEED}),
 ...(ready?[card('r','Reply to Pat about the pilot','prepared',h(2),{outcome:JSON.stringify({state:'needs_you',needs:'check the draft and send it'}),next_actions:[DRAFT]})]:[])];
const state=()=>({suggestions:cards(),promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){readFile(new URL('../'+(url.pathname.startsWith('/brand/fonts/')?url.pathname.slice(1):'brand/app-icon-192.png'),import.meta.url)).then(b=>{res.setHeader('Content-Type',url.pathname.endsWith('.woff2')?'font/woff2':'image/png');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,errors=[],shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const sel=c=>'#task-'+c.repeat(16).slice(0,16);
const chip=(page,c)=>page.locator(sel(c)+' .card-badges .chip').first();
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){
  ready=true;
  const context=await browser.newContext({viewport:{width,height},timezoneId:'Europe/Brussels',locale:'en-US'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));await page.clock.setFixedTime(NOW);
  await page.goto(base+'/');await page.locator('#section-foryou').waitFor();
  // Needs you: the chip, its amber tone, and the reason from the run's own outcome
  assert.equal(await chip(page,'q').textContent(),'Needs you');
  assert.match(await page.locator(sel('q')).getAttribute('class'),/\bt-amber\b/);
  assert.match(await page.locator(sel('q')).textContent(),/Needs you: Which of the two quotes should it accept\?/);
  // Prepared: a ready draft keeps its label and tone
  assert.equal(await chip(page,'r').textContent(),'Prepared');
  assert.doesNotMatch(await page.locator(sel('r')).getAttribute('class'),/\bt-amber\b/);
  assert.equal(await page.locator('#section-foryou .section-note').count(),1,'one ready draft: the approve note shows');
  if(shots)for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});await page.evaluate(()=>Promise.all(document.getAnimations().map(x=>x.finished)));await page.screenshot({path:`${shots}/needs-you-${width}-${scheme}.png`})}
  await page.emulateMedia({colorScheme:'light'});
  // Only a Needs you one left: nothing to approve, so no approve note
  ready=false;await page.evaluate(()=>refresh());await page.locator(sel('r')).waitFor({state:'detached'});
  assert.equal(await page.locator(sel('r')).count(),0);
  assert.equal(await page.locator('#section-foryou .section-note').count(),0,'nothing ready: no approve note');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('needs owner ok');
}finally{await browser?.close();server.close()}
