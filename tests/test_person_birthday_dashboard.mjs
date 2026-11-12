import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A person's Birthday (person_birthday.py): a row under Contact, "December 9, 1990 · age 35" with where it came from,
// and Edit in the row (a month and a day, the year optional; a day that isn't in its month says so and sends nothing).
// Without one, no row: Add birthday under Fields opens the same row. Removing takes it off. At 390 and 1440, light and
// dark. SHOT_DIR=… saves screenshots. Made-up people only.
const dashboard=await dashboardPage();
const day=n=>new Date(Date.now()+n*864e5).toISOString();
const fresh=birthday=>({id:'email:sam.rivera@mail.example',kind:'person',name:'Sam Rivera',strength:3.4,closeness:'close',last_at:day(-1),signals:40,
 ids:['+15550100','sam.rivera@mail.example'],usual_gap_days:3,role:'friend',role_by:'owner',side:'personal',edited:[],
 phones:[{value:'+15550100',by:'messages'}],emails:[{value:'sam.rivera@mail.example',by:'messages'}],profile:{},fields:[],tags:[],
 links:[],recent:[],around:[],open:{},...(birthday?{birthday}:{})});
const GOOGLE={value:'1990-12-09',month:12,day:9,year:1990,source:'google',at:'2026-11-01'};
let person=fresh(GOOGLE);const calls=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
  locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')?person:{projects:[],people:[person],quiet:[],new:[],orgs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='graph_birthday'){const a=call.args;
   if(a.remove){delete person.birthday}else{const year=a.year?+a.year:null;person.birthday={value:year?`${year}-${String(a.month).padStart(2,'0')}-${String(a.day).padStart(2,'0')}`:`--${String(a.month).padStart(2,'0')}-${String(a.day).padStart(2,'0')}`,month:a.month,day:a.day,year,source:'owner',at:'2026-11-10'}}}
  res.end('{}');return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;const shots=process.env.SHOT_DIR;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 if(shots)await mkdir(shots,{recursive:true});
 for(const [width,height,scheme] of [[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]){
  person=fresh(GOOGLE);calls.length=0;const tag=`${width}-${scheme}`;
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,deviceScaleFactor:width<500?2:1,isMobile:width<500,hasTouch:width<500}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const shot=async name=>{if(shots){await page.locator('#people-view .person-contact').scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/birthday-${name}-${tag}.png`})}};
  const wide=async()=>assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll at '+tag);
  await page.goto('http://127.0.0.1:'+server.address().port+'/#graph/'+encodeURIComponent(person.id));
  const card=page.locator('#people-view .person-page');await card.waitFor();
  // The row: the date in the owner's order, the age with the year, where it came from, Edit
  const row=card.locator('.person-contact .bday-row');
  assert.deepEqual(await card.locator('.person-contact .kv .k').allTextContents(),['Phone','Email','Birthday']);
  assert.equal(await row.locator('.bday').textContent(),`December 9, 1990 · age ${new Date().getFullYear()-1990-(new Date().getMonth()===11&&new Date().getDate()>=9?0:1)}`);
  assert.equal(await row.locator('.sub').textContent(),'From Google contacts');
  assert.equal(await card.locator('[data-bday-add]').count(),0,'no Add birthday when there is one');
  await wide();await shot('row');
  // Edit: month and day filled, the year optional; a day not in its month says so and sends nothing
  await row.locator('[data-bday-edit]').click();
  const ed=row.locator('.bday-edit');await ed.waitFor();
  assert.equal(await ed.locator('[name=month]').inputValue(),'12');assert.equal(await ed.locator('[name=day]').inputValue(),'9');assert.equal(await ed.locator('[name=year]').inputValue(),'1990');
  assert.deepEqual(await ed.locator('input,select').evaluateAll(els=>els.map(e=>e.name)),['month','day','year'],'en-US: the month first');
  await ed.locator('[name=month]').selectOption('2');await ed.locator('[name=day]').fill('30');await ed.locator('[name=year]').fill('');
  await ed.locator('[data-bday-save]').click();
  assert.equal(await ed.locator('.field-error').textContent(),'That day isn’t in that month');assert.equal(calls.length,0);
  await wide();await shot('error');
  await ed.locator('[name=day]').fill('29');
  assert.equal(await ed.locator('.field-error').textContent(),'','typing clears the error');
  await shot('editing');
  await ed.locator('[name=day]').press('Enter');
  await page.locator('#toast',{hasText:'Saved.'}).waitFor();
  assert.deepEqual(calls[0],{action:'graph_birthday',args:{node_id:person.id,month:2,day:29,year:''}});
  await card.locator('.bday-row .bday',{hasText:'February 29'}).waitFor();
  assert.equal(await card.locator('.bday-row .bday').textContent(),'February 29','no year, no age');
  assert.equal(await card.locator('.bday-row .sub').textContent(),'Added by you');
  // Escape leaves it as it was
  await card.locator('.bday-row [data-bday-edit]').click();await card.locator('.bday-edit [name=day]').fill('3');await card.locator('.bday-edit [name=day]').press('Escape');
  await card.locator('.bday-row .bday').waitFor();assert.equal(calls.length,1);
  // Remove: no row; Add birthday under Fields opens the same row, empty
  await card.locator('.bday-row [data-bday-edit]').click();await card.locator('.bday-edit [data-bday-remove]').click();
  await page.locator('#toast',{hasText:'Removed.'}).waitFor();assert.deepEqual(calls[1].args,{node_id:person.id,remove:true});
  await card.locator('[data-bday-add]').waitFor();
  assert.equal(await card.locator('.bday-row').count(),0);
  assert.deepEqual(await card.locator('.crm-fields .fields-foot button').allTextContents(),['Add birthday','Add a field']);
  if(shots){await card.locator('.crm-fields').scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/birthday-empty-${tag}.png`})}
  await card.locator('[data-bday-add]').click();
  const add=card.locator('.person-contact .bday-row .bday-edit');await add.waitFor();
  assert.equal(await add.locator('[name=month]').inputValue(),'');assert.ok(!(await card.locator('[data-bday-add]').isVisible()),'Add birthday steps aside while the row is open');assert.equal(await add.locator('[data-bday-remove]').count(),0);
  await add.locator('[data-bday-save]').click();assert.equal(await add.locator('.field-error').textContent(),'Pick a month and a day');
  await wide();await shot('add');
  await add.locator('[name=month]').selectOption('12');await add.locator('[name=day]').fill('9');await add.locator('[data-bday-save]').click();
  await card.locator('.bday-row .bday',{hasText:'December 9'}).waitFor();
  assert.deepEqual(calls[2].args,{node_id:person.id,month:12,day:9,year:''});
  assert.deepEqual(errors,[]);await context.close();
 }
 // Day first where the owner's dates read that way
 const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();person=fresh(GOOGLE);
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await page.goto('http://127.0.0.1:'+server.address().port+'/#graph/'+encodeURIComponent(person.id));await page.locator('#people-view .bday-row').waitFor();
 await page.evaluate(()=>{DL='en-GB'});await page.evaluate(()=>people(graphNode,true));await page.locator('#people-view .bday-row .bday',{hasText:'9 December 1990'}).waitFor();
 await page.locator('#people-view [data-bday-edit]').click();
 assert.deepEqual(await page.locator('.bday-edit').locator('input,select').evaluateAll(els=>els.map(e=>e.name)),['day','month','year']);
 await context.close();
 console.log('person birthday dashboard ok');
}finally{await browser?.close();server.close()}
