import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do's project picker (More > Change project) and the other boxes that open inside a to-do (Not needed, Ask for
// changes, Snooze) fit inside the to-do at phone width: a long project name never pushes the box off the screen, and
// the picker's buttons sit in one even row. SHOTS=<folder> saves screenshots of the picker.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),long='Editorial listing exchanges: Forecastio';
const cards=[{id:'p1',title:'Salesflare inclusion for Forecastio',body:'Draft the listing pitch.',status:'pending',scope:'work',created_at:now,event_ids:[1],
  project:long,project_node:{node_id:'project:edx',name:long}}];
const projects=[{id:'project:edx',name:long},{id:'project:q4',name:'Q4 partner program and reseller onboarding for the Benelux region'},{id:'project:x',name:'Hiring'}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:false,auto_hour12:false,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({projects}));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
// Everything inside the box stays inside the to-do, and the page never scrolls sideways
const fits=(page,sel)=>page.evaluate(sel=>{const box=document.querySelector(sel),card=box.closest('.card'),c=card.getBoundingClientRect(),out=[];
 for(const el of [box,...box.querySelectorAll('*')]){const r=el.getBoundingClientRect();if(!r.width)continue;
  if(r.left<c.left-0.5||r.right>c.right+0.5)out.push(`${el.tagName}.${el.className} ${Math.round(r.left)}-${Math.round(r.right)} outside ${Math.round(c.left)}-${Math.round(c.right)}`)}
 if(document.documentElement.scrollWidth>innerWidth)out.push('page scrolls sideways: '+document.documentElement.scrollWidth);return out},sel);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:'dark'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-p1').waitFor();
  const card=page.locator('#task-p1');
  // The project picker, holding the long name
  await card.locator('.more-actions>summary').click();await card.locator('[data-card-project]').click();
  const picker=card.locator('.project-picker');await picker.locator('select').waitFor();
  assert.equal(await picker.locator('select').inputValue(),'project:edx');
  if(process.env.SHOTS){await picker.scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.SHOTS}/project-picker-${width}.png`})}
  assert.deepEqual(await fits(page,'#task-p1 .project-picker'),[],`project picker at ${width}`);
  // Save, No project and Cancel: one row, the same height
  const btns=await picker.locator('.actions>button').evaluateAll(n=>n.map(b=>{const r=b.getBoundingClientRect();return [Math.round(r.top),Math.round(r.height)]}));
  assert.equal(btns.length,3);assert.equal(new Set(btns.map(String)).size,1,`picker buttons in one row at ${width}: ${JSON.stringify(btns)}`);
  // A longer choice still fits; the select never grows past the box
  await picker.locator('select').selectOption('project:q4');
  assert.deepEqual(await fits(page,'#task-p1 .project-picker'),[],`project picker, longer name, at ${width}`);
  await picker.locator('[data-pp="cancel"]').click();assert.equal(await picker.count(),0);
  // Not needed
  await card.getByRole('button',{name:'Not needed',exact:true}).click();await card.locator('.dismiss-editor').waitFor();
  assert.deepEqual(await fits(page,'#task-p1 .dismiss-editor'),[],`not needed at ${width}`);
  await card.locator('.dismiss-editor').getByRole('button',{name:'Cancel'}).click();await card.locator('.dismiss-editor').waitFor({state:'detached'});
  // Snooze
  await card.getByRole('button',{name:'Snooze',exact:true}).click();await page.waitForTimeout(200);
  const snooze=await page.evaluate(()=>{const c=document.querySelector('#task-p1').getBoundingClientRect();return [...document.querySelectorAll('#task-p1 *')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&(r.right>c.right+0.5||r.left<c.left-0.5)}).map(e=>e.tagName+'.'+e.className)});
  assert.deepEqual(snooze,[],`snooze at ${width}`);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('project picker fit ok');
