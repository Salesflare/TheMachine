import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// One avatar shape everywhere: a person's photo and an organization's logo are both circles (base-design.css
// .person-pic,.org-pic), in a to-do's meta row, the People and Organizations lists, their pages and the picture button,
// at every size. A logo that doesn't fill its square sits inside the circle with room to spare, so its corners aren't
// cut off; an app icon that fills its square (.bleed) fills the circle. SHOT_DIR=… also saves screenshots.
const dashboard=await dashboardPage();
// The shape is set once: no other rule on an avatar (or the picture button around one) gives it another corner
const reshaped=[...dashboard.matchAll(/([^{}]*(?:person-pic|org-pic|chip-av|pic-edit)[^{}]*)\{([^{}]*)\}/g)]
 .filter(m=>(m[2].match(/border-radius:[^;]*/g)||[]).some(v=>!/^border-radius:\s*(?:50%|inherit)\s*$/.test(v))).map(m=>m[1].trim()+'{'+m[2]+'}');
assert.deepEqual(reshaped,[]);
const now=new Date().toISOString(),day=new Date(Date.now()-864e5).toISOString();
const svg=body=>`<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">${body}</svg>`;
const PICS={a:svg('<rect width="200" height="200" fill="#c9b8a6"/><circle cx="100" cy="80" r="40" fill="#7a5c48"/><path d="M30 200c6-44 34-64 70-64s64 20 70 64z" fill="#3d5a80"/>'),
 // a mark on a clear background that reaches its square's corners: cut off in a circle without enough padding
 b:svg('<rect x="10" y="10" width="180" height="180" rx="44" fill="none" stroke="#1d4ed8" stroke-width="20"/><circle cx="100" cy="100" r="42" fill="#f59e0b"/>'),
 // an app icon that fills its square
 c:svg('<rect width="200" height="200" fill="#0f766e"/><path d="M55 145 100 55l45 90" fill="none" stroke="#fff" stroke-width="20"/>')};
const pic=k=>'api/person-photo?p='+k.repeat(32);
const person=(id,name,photo)=>({id:'email:'+id,kind:'person',name,strength:2.1,closeness:'regular',last_at:day,signals:6,ids:[id],usual_gap_days:7,
 quiet:false,role:null,org:'org:'+id.split('@')[1],org_name:null,org_by:'email',profile:photo?{photo}:null,links:[],recent:[],around:[],open:{}});
const org=(id,name,logo)=>({id:'org:'+id,kind:'org',name,domain:id,signals:3,last_at:day,role:null,strength:1,
 profile:{name,industry:'Software Development',...(logo?{logo}:{})},about:'Software Development',links:[],recent:[],around:[]});
const people=[person('lee@brushworks.example','Lee Example',pic('a')),person('kim@globex.example','Kim Example',null)];
const orgs=[org('brushworks.example','Brushworks',pic('b')),org('appco.example','Appco',pic('c')),org('globex.example','Globex',null)];
const card=(id,p,o)=>({id,title:'Answer the quote question '+id.slice(0,2),body:'They asked about the quote.',status:'pending',created_at:now,event_ids:[1],
 people:[{id:p.id,name:p.name,photo:p.profile?.photo}],source_line:'Source: Email',scope:'work',org_said:true,org_node:{id:o.id,name:o.name,logo:o.profile.logo}});
const cards=[card('a1a1a1a1a1a1a1a1',people[0],orgs[0]),card('b1b1b1b1b1b1b1b1',people[1],orgs[1]),card('c1c1c1c1c1c1c1c1',people[0],orgs[2])];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/person-photo'){const p=PICS[url.searchParams.get('p')[0]];if(!p){res.statusCode=404;res.end();return}res.setHeader('Content-Type','image/svg+xml');res.end(p);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{pending:cards.length},decisions:[],analyses:[],deliveries:[],
  review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/graph'){const node=url.searchParams.get('node');res.end(JSON.stringify(node?[...people,...orgs].find(n=>n.id===node):{projects:[],people,quiet:[],new:[],orgs}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
// Every avatar in sight: its shape, and how much room a logo has inside the circle
const shapes=page=>page.evaluate(()=>[...document.querySelectorAll('.person-pic,.org-pic')].filter(s=>s.getClientRects().length).map(s=>{
 const r=s.getBoundingClientRect(),cs=getComputedStyle(s),i=s.querySelector('img'),ic=i&&getComputedStyle(i);
 const edit=s.closest('.pic-edit');
 return {kind:s.classList.contains('org-pic')?'org':'person',where:s.closest('[id],article')?.id||s.parentElement.className,w:Math.round(r.width),h:Math.round(r.height),
  radius:cs.borderRadius,clip:cs.overflow,editRadius:edit?getComputedStyle(edit).borderRadius:null,
  img:i?{bleed:i.classList.contains('bleed'),pad:parseFloat(ic.paddingLeft)/r.width,fit:ic.objectFit}:null}}));
// Collected and asserted at the end, so a run with SHOT_DIR saves every view
const wrong=[];
const check=(found,label)=>{try{checkNow(found,label)}catch(e){wrong.push(e.message)}};
const checkNow=(found,label)=>{assert.ok(found.some(x=>x.kind==='org')&&found.some(x=>x.kind==='person'),label+': both kinds in sight '+JSON.stringify(found));
 for(const x of found){const at=label+' '+JSON.stringify(x);
  assert.equal(x.radius,'50%',at);assert.equal(x.clip,'hidden',at);assert.equal(x.w,x.h,at);
  if(x.editRadius!==null)assert.equal(x.editRadius,'50%',at);
  // a logo's square fits inside the circle: padding of at least (1-1/√2)/2 of the width on each side, unless it bleeds
  if(x.kind==='org'&&x.img&&!x.img.bleed){assert.equal(x.img.fit,'contain',at);assert.ok(x.img.pad>=0.146,at)}
  if(x.kind==='org'&&x.img?.bleed)assert.equal(x.img.pad,0,at)}};
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const sizes=process.env.SHOT_DIR?[[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]:[[1440,900,'light'],[390,844,'dark']];
 if(process.env.SHOT_DIR)await mkdir(process.env.SHOT_DIR,{recursive:true});
 for(const [width,height,scheme] of sizes){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,deviceScaleFactor:2});
  await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  const shot=name=>process.env.SHOT_DIR?page.screenshot({path:`${process.env.SHOT_DIR}/${name}-${width}-${scheme}.png`}):null;
  const settled=()=>page.waitForFunction(()=>[...document.querySelectorAll('.person-pic img,.org-pic img')].every(i=>i.complete&&i.naturalWidth>0));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-a1a1a1a1a1a1a1a1 .card-badges .chip-av img').first().waitFor();await settled();
  const meta=await shapes(page);
  if(process.env.SHOT_DIR)await page.locator('#task-a1a1a1a1a1a1a1a1').screenshot({path:`${process.env.SHOT_DIR}/todo-${width}-${scheme}.png`});
  check(meta,'meta row');
  await navClick(page.locator('nav [data-tab="people"]'));
  await page.locator('#people-view article[data-node="email:lee@brushworks.example"] .person-pic img').waitFor();await settled();
  await shot('people');const peopleList=await shapes(page);
  await navClick(page.locator('.side-sub a[data-graph-sub="orgs"]'));
  await page.locator('#people-view article[data-node="org:brushworks.example"] .org-pic img').waitFor();await settled();
  await shot('orgs');check([...peopleList,...await shapes(page)],'lists');
  await page.locator('#people-view article[data-node="org:brushworks.example"] button.node').click();
  await page.locator('.graph-detail .org-pic.big img').waitFor();await settled();
  await shot('org');const orgPage=await shapes(page);
  assert.ok(orgPage.some(x=>x.kind==='org'&&x.w>=36&&x.editRadius!==null),JSON.stringify(orgPage));
  await page.evaluate(()=>{location.hash=graphHash('email:lee@brushworks.example')});
  await page.locator('.graph-detail .person-pic.big img').waitFor();await settled();
  check([...orgPage,...await shapes(page)],'pages');
  assert.deepEqual(errors,[]);
  await context.close();
 }
 assert.deepEqual(wrong,[]);
 console.log('Avatars: people and organizations both round, logos padded to fit the circle.');
}finally{await browser?.close();server.close()}
