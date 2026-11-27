import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// What I've learned, Your profile: the lines the profile turn wrote into USER.md (state.profile), each with what it is,
// first on the page; Edit and Remove send the row's exact line (profile_line_edit / profile_line_remove), and a page
// with only a profile still counts as learned. Made-up fixtures, all mocked; PROFILE_SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const start=[
 {label:'Role',text:'Runs a small garden shop with two colleagues',line:'- Role: Runs a small garden shop with two colleagues'},
 {label:'Tone',text:'Short and warm; first names; no exclamation marks',line:'- Tone: Short and warm; first names; no exclamation marks'},
 {label:'Languages',text:'English: customers; Dutch: family',line:'- Languages: English: customers; Dutch: family'},
 {label:'What matters',text:'Robin: the main plant supplier',line:'- Robin: the main plant supplier'},
 {label:'Leave alone',text:'Weekly deals digests',line:'- Weekly deals digests'}];
let profile=structuredClone(start);const posts=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},connectors:[],review_runs:[],voices:[],facts:[],profile}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='profile_line_edit')profile=profile.map(p=>p.line===args.line?{...p,text:args.text,line:p.line.replace(p.text,args.text)}:p);
  if(action==='profile_line_remove')profile=profile.filter(p=>p.line!==args.line);
  res.end(JSON.stringify({profile}));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;const shots=process.env.PROFILE_SHOTS;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  profile=structuredClone(start);
  const context=await browser.newContext({viewport:{width,height:900}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#learning=learned');
  await navClick(page.locator('[data-tab="feedback"]').first());
  const learned=page.locator('#facts'),group=learned.locator('[data-group="profile"]');
  await group.waitFor();
  // Only a profile: the page still shows what was learned, the profile first
  assert.equal(await learned.locator('.learn-group').first().getAttribute('data-group'),'profile');
  assert.equal(await group.locator('h3').textContent(),'Your profile 5');
  assert.deepEqual(await group.locator('.fact-row strong').allTextContents(),['Role','Tone','Languages','What matters','Leave alone']);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
  if(shots){await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:`${shots}/profile-${width}.png`})}
  if(width===1440){
   // Edit opens the words in place; Save sends the row's exact line with the new words (row n's id is ~n, below a fact's)
   await group.locator('[data-edit-fact="-2"]').click();
   const box=group.locator('#learned--2 textarea');assert.equal(await box.inputValue(),start[1].text);
   await box.fill('Warm, first names');
   if(shots)await page.screenshot({path:`${shots}/profile-${width}-edit.png`});
   await group.locator('#learned--2 [type=submit]').click();
   await page.locator('#toast',{hasText:'Saved.'}).waitFor({state:'attached'});
   assert.deepEqual(posts.at(-1),{action:'profile_line_edit',args:{line:start[1].line,text:'Warm, first names'}});
   await group.locator('#learned--2 textarea').waitFor({state:'detached'});
   await group.locator('#learned--2 .grow',{hasText:'Tone Warm, first names'}).waitFor();
  }else{
   await group.locator('[data-edit-fact="-5"]').click();
   await group.locator('#learned--5 [data-forget="-5"]').click();
   await page.locator('#toast',{hasText:'Removed.'}).waitFor({state:'attached'});
   assert.deepEqual(posts.at(-1),{action:'profile_line_remove',args:{line:start[4].line}});
   await learned.locator('[data-group="profile"] h3',{hasText:'Your profile 4'}).waitFor();
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('learned profile dashboard ok');
}finally{await browser?.close();server.close()}
