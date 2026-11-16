import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A Graph row with a long name: only the name ends in …. The pills beside it (gone quiet, tags, a project's heat) keep
// their full size, their dot stays a round 6 px dot, and nothing runs into the closeness bar or past the row. Checked on
// People, Organizations and Projects at 390 and 1440 wide, light and dark. PILLS_SHOT=<dir> writes screenshots.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()-n*864e5).toISOString();
const person=(i,name,extra={})=>({id:'email:p'+i+'@client.example',kind:'person',name,strength:6,closeness:'close',last_at:day(20+i),usual_gap_days:3,signals:9,ids:['p'+i+'@client.example'],quiet:true,...extra});
const people=[
 person(1,'Bernadette Ravenscroft-Whitfield'),
 person(2,'developer@some-long-company-domain.example'),
 person(3,'Kim Lee'),
 person(4,'Maximilian Featherstonehaugh-Abernathy',{tags:['partner','investor']}),
 person(5,'Alexandria Montgomery-Vanderbilt',{quiet:false,tags:['customer']})];
const LONG_ORG='Hazelbrook Digital Marketing, Development and Growth Consultancy International';
const orgs=[{id:'org:hazelbrook.example',kind:'org',name:LONG_ORG,strength:2,last_at:day(1),signals:8,people:4,tags:['partner','reseller']},{id:'org:puffin.example',kind:'org',name:'Puffin Metrics',strength:1,last_at:day(3),signals:2,people:1}];
const projects=[{id:'project:1',kind:'project',name:'Editorial listing exchange with a very long project name for the autumn',state:'heating up',strength:2,last_at:day(1),signals:5,tags:['q4']},
 {id:'project:2',kind:'project',name:'Short one',state:'cooling',strength:1,last_at:day(4),signals:2}];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({projects,people,quiet:people.filter(p=>p.quiet),new:[],orgs,boards:[],person_names:people.map(p=>({id:p.id,name:p.name})),project_names:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';

// Runs in the page: every row's pills, measured against their text, their dot, the name, the bar and the row
function measure(){const out=[];
 for(const row of document.querySelectorAll('#people-view .sub-pane:not([hidden]) .graph-row')){
  if(!row.checkVisibility())continue;
  const r=row.getBoundingClientRect(),name=row.querySelector(':scope>.node'),bar=row.querySelector(':scope>.graph-bar');
  if(bar&&bar.getBoundingClientRect().right>r.right+0.5)out.push({row:name?.textContent.trim().slice(0,24),chip:'(bar)',barPastRow:true});
  if(name&&name.scrollWidth>name.clientWidth&&name.getBoundingClientRect().width<80)out.push({row:name.textContent.trim().slice(0,24),chip:'(name)',nameGone:Math.round(name.getBoundingClientRect().width)});
  for(const chip of row.querySelectorAll('.chip')){if(!chip.checkVisibility())continue;
   const c=chip.getBoundingClientRect(),dot=getComputedStyle(chip,'::before');
   out.push({row:name?.textContent.trim().slice(0,24),chip:chip.textContent.trim(),cut:chip.scrollWidth>chip.clientWidth+1,
    dot:dot.display==='none'?null:[parseFloat(dot.width),parseFloat(dot.height)],
    wrap:getComputedStyle(chip).whiteSpace,top:Math.round(c.top-r.top),
    intoBar:bar&&Math.abs(c.top-bar.getBoundingClientRect().top)<20?c.right>bar.getBoundingClientRect().left+0.5:false,
    pastRow:c.right>r.right+0.5,overName:name?c.left<name.getBoundingClientRect().right-0.5&&c.top<name.getBoundingClientRect().bottom:false})}}
 return out}
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]])for(const scheme of ['light','dark']){
  const phone=width<600,context=await browser.newContext({viewport:{width,height},isMobile:phone,hasTouch:phone,locale:'en-GB',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));await page.goto(base);
  await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());await page.locator('#people-view').waitFor({state:'attached'});
  for(const pane of ['people','orgs','projects']){
   await page.evaluate(n=>document.querySelector(`[data-graph-sub="${n}"]`).click(),pane);
   await page.locator('#people-view .sub-pane:not([hidden]) .graph-row').first().waitFor();
   // The Graph styles and fonts are in: a row's name may shrink (min-width 0 comes from graph-pages.css)
   await page.waitForFunction(()=>{const n=document.querySelector('#people-view .sub-pane:not([hidden]) .graph-row>.node');return document.fonts.status==='loaded'&&!!n&&getComputedStyle(n).minWidth==='0px'});
   if(process.env.PILLS_SHOT)await page.screenshot({path:`${process.env.PILLS_SHOT}/${pane}-${width}-${scheme}.png`});
   const pills=await page.evaluate(measure),where=`${pane} ${width} ${scheme}`;
   assert.ok(pills.filter(p=>!p.chip.startsWith('(')).length>=(pane==='people'?4:2),`${where}: the pills are there ${JSON.stringify(pills)}`);
   for(const p of pills){const what=`${where} "${p.row}" ${p.chip}: ${JSON.stringify(p)}`;
    assert.ok(!p.barPastRow,`${what}: the closeness bar runs past the row`);
    assert.ok(!p.nameGone,`${what}: the pills leave no room for the name`);
    if(p.chip.startsWith('('))continue;
    assert.equal(p.cut,false,`${what}: the pill is narrower than its text`);
    assert.equal(p.wrap,'nowrap',`${what}: the pill's text wraps`);
    if(p.dot)assert.deepEqual(p.dot,[6,6],`${what}: the dot is squashed`);
    assert.equal(p.intoBar,false,`${what}: the pill runs into the closeness bar`);
    assert.equal(p.pastRow,false,`${what}: the pill runs past the row`);
    assert.equal(p.overName,false,`${what}: the pill sits over the name`)}
   if(pane==='people'){
    // the long names end in …, the short one shows in full; every quiet person has their pill
    const names=await page.$$eval('#people-view .sub-pane:not([hidden]) .graph-row>.node',b=>b.map(x=>({n:x.textContent,cut:x.scrollWidth>x.clientWidth})));
    if(phone)assert.ok(names.find(x=>x.n.startsWith('Bernadette')).cut,`${where}: a long name ends in … ${JSON.stringify(names)}`);
    assert.equal(names.find(x=>x.n==='Kim Lee').cut,false,`${where}: a short name shows in full`);
    assert.equal(pills.filter(p=>p.chip==='gone quiet').length,4,`${where}: every quiet person has the pill`)}}
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('graph row pills: on a long name only the name ends in …; pills and dots keep their size, clear of the bar');
}finally{await browser?.close();server.close()}
