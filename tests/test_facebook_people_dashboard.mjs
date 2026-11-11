import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Import birthdays from Facebook to-do's preview with friends nobody in the Graph has (todos-facebook-people.js,
// birthdays_facebook.add): how many, a few names, and Add … as personal contacts next to Save, which stays the main
// button. Counts carry the locale's thousands separator, and a ghost button that starts a wrapped row lines up with the
// row's left edge. Add sends one step; the to-do then says how many it added, with Undo there and on the toast. With no Save, Add is the
// main button. At 390 and 1440, light and dark. SHOTS=<folder> saves screenshots. All mocked; made-up names only.
const dashboard=await dashboardPage();
const SHOTS=process.env.SHOTS||'';
const now=new Date().toISOString();
const MATCHED=['Ada Arden','Bram Brook','Cleo Calloway','Dov Dunmore','Esme Ellery','Finn Fairbank','Gia Garrow','Hugo Hollis'];
const OTHERS=['Ines Ivers','Jules Jessup','Kai Kestrel','Lena Lowell','Milo Marsh','Nora Northam','Otto Orrin','Pia Pell'];
let card,posts=[];
const preview=(extra={})=>({state:'preview',found:1312,matched:112,new:96,shown:MATCHED.map((name,i)=>({id:'email:p'+i+'@mail.example',name,date:`--0${1+i%9}-1${i}`})),
 more:104,ambiguous:['Quin Quarry'],unmatched:1199,capped:false,missing:[],others:1199,others_shown:OTHERS,added:0,...extra});
const fresh=(f=preview())=>{card={id:'fb1',title:'Import birthdays from Facebook',body:'',status:'pending',scope:'personal',created_at:now,event_ids:[1],owner_step:true,
 source_line:'Source: your routine Birthdays',facebook_birthdays:f};posts=[]};
const state=()=>({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='birthdays_facebook'&&args.step==='add'){const n=card.facebook_birthdays.others;card={...card,facebook_birthdays:{...card.facebook_birthdays,added:n}};res.end(JSON.stringify({state:'preview',added:n}));return}
  if(action==='birthdays_facebook'&&args.step==='undo_add'){const n=card.facebook_birthdays.added;card={...card,facebook_birthdays:{...card.facebook_birthdays,added:0}};res.end(JSON.stringify({state:'preview',undone:n}));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin='http://127.0.0.1:'+server.address().port,errors=[];let browser;
const text=async l=>(await l.innerText()).replace(/\s+/g,' ').trim();
const ADD='Add 1,199 as personal contacts';
// each button that starts a row of a .cl-acts: how far its label is from the to-do's left edge (0 for every one)
const rowStarts=l=>l.evaluateAll(rows=>rows.flatMap(row=>{const left=row.getBoundingClientRect().left;let top=-1;return [...row.querySelectorAll('button')].flatMap(b=>{const r=b.getBoundingClientRect();if(r.top<=top+1)return [];top=r.top;
 const range=document.createRange();range.selectNodeContents(b);const label=b.classList.contains('ghost')?range.getBoundingClientRect().left:r.left;return [label-left]})}));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,scheme] of [[1440,'light'],[390,'light'],[1440,'dark'],[390,'dark']]){fresh();
  const context=await browser.newContext({viewport:{width,height:width<500?844:900},colorScheme:scheme,...(width<500?{isMobile:true,hasTouch:true,deviceScaleFactor:2}:{})}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const shot=async name=>{if(SHOTS){await todo.scrollIntoViewIfNeeded();if(width<500)await todo.locator('.fb-others').evaluate(e=>e.scrollIntoView({block:'center'}));await page.screenshot({path:`${SHOTS}/facebook-people-${name}-${width}-${scheme}.png`})}};
  await page.goto(origin+'/?v='+width+scheme);
  const todo=page.locator('#task-fb1');await todo.waitFor();
  // The preview: the others after the matched ones, a few of their names, Add … as personal contacts next to Save
  const others=todo.locator('.cl-fine',{hasText:'aren’t in your Graph'});await others.waitFor();
  assert.equal(await text(todo.locator('.cl-lead')),'Found 1,312 birthdays on Facebook.');
  assert.equal(await text(others),'1,199 Facebook friends aren’t in your Graph yet.');
  assert.match(await text(todo.locator('.cl-fine',{hasText:'Ines Ivers'})),/^Ines Ivers, Jules Jessup, .*Pia Pell and 1,191 more$/);
  assert.equal(await text(todo.locator('.cl-fine',{hasText:'already in your Graph'})),'112 are already in your Graph.');
  assert.equal(await text(todo.locator('.cl-fine',{hasText:'already have a birthday'})),'16 of them already have a birthday.','why 96 of 112');
  // the friends are a block of their own, below a line, with the note right under their button
  assert.equal(await todo.locator('.fb-others.fb-sep').count(),1);
  const note=todo.locator('.fb-others .cl-acts + .cl-fine');
  assert.equal(await text(note),'With their birthday. Reminders only come for people you write to.','under the buttons');
  const fines=await todo.locator('.cl-fine').allInnerTexts();
  assert.ok(fines.findIndex(x=>x.includes('Skipped'))<fines.findIndex(x=>x.includes('aren’t in your Graph')),'after the matched and skipped ones');
  const buttons=todo.locator('.cl-acts button');
  assert.deepEqual((await buttons.allInnerTexts()).map(x=>x.trim()),['Save 96 birthdays',ADD,'Import again']);
  assert.deepEqual(await buttons.evaluateAll(b=>b.map(x=>x.className)),['primary','','ghost'],'Save stays the main button, Add has a border, Import again is quiet');
  assert.deepEqual(await todo.locator('.fb-others button').allInnerTexts(),[ADD]);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll at '+width);
  const starts=await rowStarts(todo.locator('.cl-acts'));assert.ok(starts.every(x=>Math.abs(x)<0.5),'every row starts at the left edge: '+starts);
  await shot('preview');
  // Add: one step for all of them; the to-do and the toast say how many, each with Undo
  await todo.getByRole('button',{name:ADD}).click();
  await page.locator('#toast',{hasText:'Added 1,199 personal contacts.'}).waitFor();
  assert.deepEqual(posts.map(p=>p.args),[{suggestion_id:'fb1',step:'add'}]);
  const added=todo.locator('.cl-fine',{hasText:'Added'});await added.waitFor();
  assert.equal(await text(added),'Added 1,199 personal contacts.');
  assert.equal(await note.count(),0,'no note once added');
  assert.equal(await todo.getByRole('button',{name:ADD}).count(),0,'added once');
  assert.deepEqual((await buttons.allInnerTexts()).map(x=>x.trim()),['Save 96 birthdays','Undo','Import again'],'Undo takes Add’s place');
  assert.equal(await page.locator('#toast [data-fbp="undo_add"]').count(),1);
  await shot('added');
  // Undo on the to-do: exactly those go again, and Add is back
  await todo.locator('.cl-acts').getByRole('button',{name:'Undo'}).click();
  await page.locator('#toast',{hasText:'Undone.'}).waitFor();
  await todo.getByRole('button',{name:ADD}).waitFor();
  assert.deepEqual(posts.map(p=>p.args.step),['add','undo_add']);
  // Undo on the toast does the same
  await todo.getByRole('button',{name:ADD}).click();
  await page.locator('#toast [data-fbp="undo_add"]').click();
  await page.locator('#toast',{hasText:'Undone.'}).waitFor();
  assert.deepEqual(posts.map(p=>p.args.step),['add','undo_add','add','undo_add']);
  // Nobody matched: no matched block and no line above the friends, and Add is the main button
  fresh(preview({matched:0,new:0,shown:[],more:0,ambiguous:[]}));await page.evaluate(()=>refresh());
  await todo.locator('.fb-others:not(.fb-sep)').waitFor();
  assert.equal(await todo.locator('.cl-fine',{hasText:/already in your Graph|None of them/}).count(),0);
  assert.deepEqual(await todo.locator('.cl-acts button').evaluateAll(b=>b.map(x=>[x.textContent.trim(),x.className])),[[ADD,'primary'],['Import again','ghost']]);
  await shot('none-matched');
  // Profile pictures for matched people without a photo: a line above Save; with every birthday known, Save is for them
  fresh(preview({photos:3}));await page.evaluate(()=>refresh());
  await todo.locator('.cl-fine',{hasText:'no photo yet'}).waitFor();
  assert.equal(await text(todo.locator('.cl-fine',{hasText:'no photo yet'})),'3 of them have no photo yet: Save adds their Facebook pictures.');
  assert.deepEqual((await todo.locator('.cl-acts button').allInnerTexts()).map(x=>x.trim()),['Save 96 birthdays',ADD,'Import again']);
  fresh(preview({new:0,photos:1}));await page.evaluate(()=>refresh());
  await todo.getByRole('button',{name:'Save 1 picture'}).waitFor();
  assert.equal(await text(todo.locator('.cl-fine',{hasText:'no photo yet'})),'1 of them has no photo yet: Save adds their Facebook picture.');
  assert.deepEqual(await todo.locator('.cl-acts button').evaluateAll(b=>b.map(x=>[x.textContent.trim(),x.className])),[['Save 1 picture','primary'],[ADD,''],['Import again','ghost']]);
  await shot('pictures');
  fresh({state:'saved',saved:0,photos:3,people:[],more:0,others:0,others_shown:[],added:0});await page.evaluate(()=>refresh());
  await todo.locator('.cl-lead',{hasText:'Added 3 profile pictures.'}).waitFor();
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('facebook people dashboard ok');
}finally{await browser?.close();server.close()}
