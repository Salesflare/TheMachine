import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Import birthdays from Facebook to-do's preview with friends nobody in the Graph has (todos-facebook-people.js,
// birthdays_facebook.add): how many, a few names, and Add them as people next to Save, which stays the main button.
// Add sends one step; the to-do then says how many it added, with Undo there and on the toast. With no Save, Add is the
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
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,scheme] of [[1440,'light'],[390,'light'],[1440,'dark'],[390,'dark']]){fresh();
  const context=await browser.newContext({viewport:{width,height:width<500?844:900},colorScheme:scheme,...(width<500?{isMobile:true,hasTouch:true,deviceScaleFactor:2}:{})}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const shot=async name=>{if(SHOTS){await todo.scrollIntoViewIfNeeded();await page.screenshot({path:`${SHOTS}/facebook-people-${name}-${width}-${scheme}.png`})}};
  await page.goto(origin+'/?v='+width+scheme);
  const todo=page.locator('#task-fb1');await todo.waitFor();
  // The preview: the others after the matched ones, a few of their names, Add them as people next to Save
  const others=todo.locator('.cl-fine',{hasText:'aren’t in your Graph'});await others.waitFor();
  assert.match(await text(others),/^1,?199 others aren’t in your Graph\.$/);
  assert.match(await text(todo.locator('.cl-fine',{hasText:'Ines Ivers'})),/^Ines Ivers, Jules Jessup, .*Pia Pell and 1,?191 more$/);
  const fines=await todo.locator('.cl-fine').allInnerTexts();
  assert.ok(fines.findIndex(x=>x.includes('Skipped'))<fines.findIndex(x=>x.includes('aren’t in your Graph')),'after the matched and skipped ones');
  const buttons=todo.locator('.cl-acts button');
  assert.deepEqual((await buttons.allInnerTexts()).map(x=>x.trim()),['Save 96 birthdays','Add them as people','Import again']);
  assert.deepEqual(await buttons.evaluateAll(b=>b.map(x=>x.className)),['primary','ghost','ghost'],'Save stays the main button');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll at '+width);
  await shot('preview');
  // Add: one step for all of them; the to-do and the toast say how many, each with Undo
  await todo.getByRole('button',{name:'Add them as people'}).click();
  await page.locator('#toast',{hasText:'people to your Graph.'}).waitFor();
  assert.deepEqual(posts.map(p=>p.args),[{suggestion_id:'fb1',step:'add'}]);
  const added=todo.locator('.cl-fine',{hasText:'Added'});await added.waitFor();
  assert.match(await text(added),/^Added 1,?199 people to your Graph\.$/);
  assert.equal(await todo.getByRole('button',{name:'Add them as people'}).count(),0,'added once');
  assert.deepEqual((await buttons.allInnerTexts()).map(x=>x.trim()),['Save 96 birthdays','Undo','Import again'],'Undo takes Add’s place');
  assert.equal(await page.locator('#toast [data-fbp="undo_add"]').count(),1);
  await shot('added');
  // Undo on the to-do: exactly those go again, and Add is back
  await todo.locator('.cl-acts').getByRole('button',{name:'Undo'}).click();
  await page.locator('#toast',{hasText:'Undone.'}).waitFor();
  await todo.getByRole('button',{name:'Add them as people'}).waitFor();
  assert.deepEqual(posts.map(p=>p.args.step),['add','undo_add']);
  // Undo on the toast does the same
  await todo.getByRole('button',{name:'Add them as people'}).click();
  await page.locator('#toast [data-fbp="undo_add"]').click();
  await page.locator('#toast',{hasText:'Undone.'}).waitFor();
  assert.deepEqual(posts.map(p=>p.args.step),['add','undo_add','add','undo_add']);
  // Nobody matched: no count line (the to-do says none are in the Graph), and Add is the main button
  fresh(preview({matched:0,new:0,shown:[],more:0,ambiguous:[]}));await page.evaluate(()=>refresh());
  await todo.locator('.cl-end',{hasText:'None of them are in your Graph yet'}).waitFor();
  assert.equal(await todo.locator('.cl-fine',{hasText:'aren’t in your Graph'}).count(),0);
  assert.deepEqual(await todo.locator('.cl-acts button').evaluateAll(b=>b.map(x=>[x.textContent.trim(),x.className])),[['Add them as people','primary'],['Import again','ghost']]);
  await shot('none-matched');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('facebook people dashboard ok');
}finally{await browser?.close();server.close()}
