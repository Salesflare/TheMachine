import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// An open to-do's blocks under its title row (the status line, the summary, Show more, Based on, the source line, the
// Preparing line, a job, draft or send box, the Details row, the buttons) sit one even gap apart, whichever of them are
// there (2026-11-06: the Preparing line sat flush under the source line and under a short summary, the rest had gaps).
// Every state (preparing with and without a source line or Show more, ready with a draft, sending, needs a decision,
// stuck, a coding agent at work) at 390 and 1440px, light and dark. SHOTS=<folder> saves each to-do at each size.
const dashboard=await dashboardPage();
const en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const now=new Date().toISOString(),ago=new Date(Date.now()-41000).toISOString();
const long='Formatting is fixed. The revised second-place placement is ready to apply to the listing, and the reply with the new arrival date is drafted. '.repeat(3);
const mail={kind:'email',revision:'v1',label:'Send to Jacob',to:['jacob@example.com'],to_name:'Jacob',subject:'Listing',body:'Hi Jacob,\n\nThe listing is updated. It arrives on Tuesday.\n\nBest'};
const cards=[
 {id:'prep-src',title:'Prepare the listing and answer the arrival date request',body:long,status:'accepted',scope:'work',created_at:now,event_ids:[1],
  source_line:'Source: email from Jacob · Fri 6 Nov (+4 more)',preparation_status:'running',preparation_started_at:ago},
 {id:'prep-short',title:'Cancel the streaming subscription',body:'Cancel the streaming subscription',status:'accepted',scope:'work',origin:'owner',created_at:now,
  preparation_status:'running',preparation_started_at:ago},
 {id:'ready',title:'Answer Jacob',body:'The reply is drafted.',status:'prepared',scope:'work',created_at:now,event_ids:[2],preparation_status:'done',
  source_line:'Source: email from Jacob · Thu 5 Nov',next_actions:[mail]},
 {id:'sending',title:'Send Noor the contract',body:'Draft ready.',status:'prepared',scope:'work',created_at:now,event_ids:[3],preparation_status:'done',
  source_line:'Source: email from Noor · Thu 5 Nov',next_actions:[{...mail,to:['noor@example.com'],to_name:'Noor',state:{status:'sending'}}]},
 {id:'decide',title:'Reply to Priya about the pricing for forty seats',body:long,status:'pending',scope:'work',created_at:now,event_ids:[4],
  based_on:{event_id:4,who:'Priya',where:null,kind:'email',at:'2026-11-04T11:37:44+00:00',url:null},source_line:'Source: email from Priya · Wed 4 Nov'},
 {id:'decide-bare',title:'Pick up the parcel at the post office',body:'It waits there until Friday.',status:'pending',scope:'personal',origin:'owner',created_at:now},
 {id:'stuck',title:'Book the train for Saturday',body:'Find a train to the city on Saturday morning.',status:'accepted',scope:'personal',created_at:now,event_ids:[5],
  source_line:'Source: email from Sam · Tue 3 Nov',preparation_status:'blocked',preparation_reason:'The booking site asked for a sign-in.',preparation_details:'login required'},
 {id:'job',title:'Fix the export button',body:'The export button does nothing on a phone.',status:'prepared',scope:'work',created_at:now,event_ids:[6],preparation_status:'done',
  source_line:'Source: email from Robin · Mon 2 Nov',agent_job:{id:'j1',status:'running',name:'Codex',started_at:ago,progress:'Reading the code'}}];
const server=createServer(async(req,res)=>{for await(const c of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname.startsWith('/brand/')){readFile(new URL('../'+(url.pathname.startsWith('/brand/fonts/')?url.pathname.slice(1):'brand/app-icon-192.png'),import.meta.url)).then(b=>{res.setHeader('Content-Type',url.pathname.endsWith('.woff2')?'font/woff2':'image/png');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/en.json'){res.end(en);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]}}));return}
 if(url.pathname==='/api/progress'){res.end(JSON.stringify({status:'running',steps:[{title:'Save the placement update with the new date'}]}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[],report=[];let browser;
// The gaps between an open to-do's blocks from its badge row down: each block's box to the next one's
const gaps=id=>document.querySelector('#task-'+id)&&(()=>{const card=document.querySelector('#task-'+id);
 const kids=[...card.children].filter(x=>{const c=getComputedStyle(x);return c.display!=='none'&&c.position!=='absolute'&&x.getBoundingClientRect().height>0});
 const boxes=[];for(const x of kids){const r=x.getBoundingClientRect();
  if(x.matches('.send-progress')&&boxes.length){boxes.at(-1).bottom=r.bottom;continue}  // a send's bar hugs its line: one block with it
  boxes.push({x,top:r.top,bottom:r.bottom})}
 const from=boxes.findIndex(b=>b.x.classList.contains('meta'));
 return boxes.slice(from).map((b,i,a)=>({name:b.x.tagName.toLowerCase()+(b.x.className?'.'+String(b.x.className).trim().split(/\s+/)[0]:''),
  gap:i?Math.round(b.top-a[i-1].bottom):null}))})();
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['dark','light'])for(const width of [390,1440]){
  const phone=width<600,context=await browser.newContext({viewport:{width,height:phone?844:900},colorScheme:scheme,isMobile:phone,hasTouch:phone});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-prep-src .actions').waitFor();await page.evaluate(()=>document.fonts.ready);
  await page.locator('#task-prep-src [data-steps] li').waitFor({timeout:8000}).catch(()=>{});
  for(const {id} of cards){
   const at=`${id} at ${width}px ${scheme}`,blocks=await page.evaluate(gaps,id);
   assert.ok(blocks,`${at}: the to-do is missing`);
   const say=blocks.map(b=>(b.gap==null?'':`[${b.gap}] `)+b.name).join(' ');report.push(`${at}: ${say}`);
   const seen=[...new Set(blocks.slice(1).map(b=>b.gap))];
   assert.ok(seen.length===1&&seen[0]>=8,`${at}: the gaps between its blocks are not even: ${say}`);
   if(shots)for(let i=0;i<5;i++)try{await page.locator(`#task-${id}`).screenshot({path:`${shots}/${id}-${width}-${scheme}.png`,timeout:3000});break}catch(e){if(i===4)throw e}  // a refresh may redraw it mid-shot
  }
  // One gap for every to-do at a size
  const all=new Set();for(const {id} of cards)for(const b of (await page.evaluate(gaps,id)).slice(1))all.add(b.gap);
  assert.equal(all.size,1,`${width}px ${scheme}: to-dos use different gaps: ${[...all]}`);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close();if(process.env.RHYTHM_REPORT)console.log(report.join('\n'))}
console.log('card rhythm dashboard ok');
