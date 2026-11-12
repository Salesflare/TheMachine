import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A ready to-do with a draft is short: its summary and the first 3 lines of the draft (blank lines left out), then one
// Show more that opens the summary and the draft together. "Nothing goes out until you approve it." is said once, in the
// Ready header, never on each to-do. Every button stays. At 1440x900 two such to-dos fit a screen, at 390 about one and
// a half. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const letter=['Hi Robin,','','For 25 seats on annual billing it is 29 a seat a month, so 8,700 for the year. Moving to 40 seats later keeps the same price per seat.','',
 'Onboarding is included from 10 seats: two live sessions for your team and a call with your admin.','','Would Thursday or Friday suit for a short call to walk through it?','','Best,','Alex'].join('\n');
const summary='They want annual pricing for 25 seats, maybe 40 next year, and whether onboarding is included. They decide this month, and they asked twice already, so a short clear answer helps. Their finance team signs off on the first of the month, and the admin wants the onboarding dates before then.';
const mail=(id,body)=>({kind:'email',revision:'r-'+id,label:'Send',to:['robin@example.invalid'],to_name:'Robin',subject:'Re: Pricing',body});
const cards=[
 {id:'long1',title:'Reply to Robin about pricing',body:summary,status:'prepared',scope:'work',created_at:now,event_ids:[1],next_actions:[mail('long1',letter)]},
 {id:'long2',title:'Reply to Kim about the renewal',body:summary,status:'prepared',scope:'work',created_at:now,event_ids:[2],next_actions:[mail('long2',letter)]},
 {id:'brief',title:'Tell Sam the weekend works',body:'Sam asked which weekend suits.',status:'prepared',scope:'personal',created_at:now,event_ids:[3],next_actions:[mail('brief','The 12th works for me.\n\nAlex')]},
 {id:'decide',title:'Book the car service',body:'Robin asked to book it before Friday.',status:'pending',scope:'personal',created_at:now,event_ids:[4]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-long1').waitFor();await page.waitForTimeout(300);
  const why=`${width} ${scheme}`;
  // Said once, in the header
  assert.equal(await page.locator('#section-foryou .section-note').textContent(),'Nothing goes out until you approve it.',why);
  assert.equal(await page.locator('#suggestions .status-line',{hasText:'Nothing goes out'}).count(),0,why+': not on each to-do');
  assert.equal(await page.locator('#suggestions .section-note').count(),1,why+': only For you says it');
  // The long one: the summary and 3 draft lines, one Show more for both
  const card=page.locator('#task-long1');
  const look=()=>card.evaluate(c=>{const db=c.querySelector('.draft .db'),lh=parseFloat(getComputedStyle(db).lineHeight);
   return {draft:c.querySelector('.draft').classList.contains('clamp'),body:c.querySelector('.body').classList.contains('clamp'),more:[...c.querySelectorAll('button.more')].map(b=>b.textContent),
    lines:Math.round(db.clientHeight/lh),blank:[...db.children].filter(d=>d.matches(':has(>br:only-child)')).every(d=>getComputedStyle(d).display==='none')}});
  let l=await look();
  assert.deepEqual({...l,lines:l.lines<=3},{draft:true,body:true,more:['Show more'],lines:true,blank:true},why);
  assert.equal(await card.locator('.card-foot>button.more:first-child').count(),1,why+': Show more leads the row under the draft');
  const h=Math.round((await card.boundingBox()).height);
  assert.ok(mobile?h<=height/1.4:h<=(height-60)/2,`${why}: short enough, ${h}px`);
  // Every button stays: send, Ask for changes, Snooze, the … menu, Details, Read result, Copy draft, Chat
  for(const sel of ['.actions button.primary[data-smart]','[data-choice="change"]','[data-choice="snooze"]','.more-actions>summary','[data-details]','[data-result="read"]','[data-result="copy"]','.chat-link,[data-chat-open],a[href^="#chat="]'])
   assert.ok(await card.locator(sel).count()>=1,why+': '+sel);
  if(shots)await page.screenshot({path:`${shots}/cards-short-${width}-${scheme}.png`});
  await card.locator('button.more').click();
  l=await look();assert.equal(l.draft,false,why);assert.equal(l.body,false,why);assert.deepEqual(l.more,['Show less']);assert.ok(l.lines>3,why+': the whole draft');
  await card.locator('button.more').click();
  l=await look();assert.equal(l.draft,true);assert.equal(l.body,true);
  // A draft of a few lines shows whole, with no Show more
  assert.equal(await page.locator('#task-brief .draft.clamp').count(),0,why);
  assert.equal(await page.locator('#task-brief button.more').count(),0,why);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),why+': no sideways scroll');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('card short dashboard: ok');
}finally{await browser?.close();server.close()}
