import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// One avatar size per place, whatever it shows: a person's photo, an organization's logo, or either one's letters when
// there is no picture. In a to-do's meta row a photo and a logo sit beside letter fallbacks for a person and an
// organization, and all four measure the same box; the People and Organizations lists match each other too.
// SHOT_DIR=… also saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),day=new Date(Date.now()-864e5).toISOString();
const svg=body=>`<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">${body}</svg>`;
const PICS={a:svg('<rect width="200" height="200" fill="#c9b8a6"/><circle cx="100" cy="80" r="40" fill="#7a5c48"/><path d="M30 200c6-44 34-64 70-64s64 20 70 64z" fill="#3d5a80"/>'),
 b:svg('<rect x="10" y="10" width="180" height="180" rx="44" fill="none" stroke="#1d4ed8" stroke-width="20"/><circle cx="100" cy="100" r="42" fill="#f59e0b"/>')};
const pic=k=>'api/person-photo?p='+k.repeat(32);
const person=(id,name,photo)=>({id:'email:'+id,kind:'person',name,strength:2.1,closeness:'regular',last_at:day,signals:6,ids:[id],usual_gap_days:7,
 quiet:false,role:null,org:'org:'+id.split('@')[1],org_name:null,org_by:'email',profile:photo?{photo}:null,links:[],recent:[],around:[],open:{}});
const org=(id,name,logo)=>({id:'org:'+id,kind:'org',name,domain:id,signals:3,last_at:day,role:null,strength:1,
 profile:{name,industry:'Software Development',...(logo?{logo}:{})},about:'Software Development',links:[],recent:[],around:[]});
const people=[person('lee@brushworks.example','Lee Example',pic('a')),person('kim@globex.example','Kim Example',null)];
const orgs=[org('brushworks.example','Brushworks',pic('b')),org('globex.example','Globex',null)];
const card=(id,p,o)=>({id,title:'Answer the quote question '+id.slice(0,2),body:'They asked about the quote.',status:'pending',created_at:now,event_ids:[1],
 people:[{id:p.id,name:p.name,photo:p.profile?.photo}],source_line:'Source: Email',scope:'work',org_said:true,org_node:{id:o.id,name:o.name,logo:o.profile.logo}});
// A photo beside a letter organization (as reported), a letter person beside a logo, and both pictures
const cards=[card('a1a1a1a1a1a1a1a1',people[0],orgs[1]),card('b1b1b1b1b1b1b1b1',people[1],orgs[0]),card('c1c1c1c1c1c1c1c1',people[0],orgs[0])];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/person-photo'){const p=PICS[url.searchParams.get('p')[0]];if(!p){res.statusCode=404;res.end();return}res.setHeader('Content-Type','image/svg+xml');res.end(p);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{pending:cards.length},decisions:[],analyses:[],deliveries:[],
  review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/graph'){const node=url.searchParams.get('node');res.end(JSON.stringify(node?[...people,...orgs].find(n=>n.id===node):{projects:[],people,quiet:[],new:[],orgs}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
// Each avatar in sight under root: its kind, what fills it, and its outer box
const boxes=(page,root)=>page.evaluate(root=>[...document.querySelectorAll(root)].flatMap(r=>[...r.querySelectorAll('.person-pic,.org-pic')])
 .filter(s=>s.getClientRects().length).map(s=>{const r=s.getBoundingClientRect();
  return {kind:s.classList.contains('org-pic')?'org':'person',fill:s.querySelector('img')?'picture':'letter',w:+r.width.toFixed(2),h:+r.height.toFixed(2)}}),root);
const same=(found,label,want)=>{const at=label+' '+JSON.stringify(found);
 for(const k of want)assert.ok(found.some(x=>x.kind+'/'+x.fill===k),at+': '+k+' in sight');
 assert.equal(new Set(found.map(x=>x.w+'x'+x.h)).size,1,at)};
// A letter avatar also looks its full size: across its middle, every pixel inside the box stands off the row's own
// background on the same side as its fill. A rim that falls back toward the background (a light ring around a fill
// darker than the to-do, as on the dark theme) leaves a disc that reads a size smaller than the photo beside it.
const looks=async(page,reader,sel)=>{const el=page.locator(sel).first(),b=await el.boundingBox(),pad=4;
 const png=await page.screenshot({clip:{x:b.x-pad,y:b.y-pad,width:b.width+2*pad,height:b.height+2*pad}});
 return reader.evaluate(async([src,pad])=>{const i=new Image();i.src='data:image/png;base64,'+src;await i.decode();
  const c=document.createElement('canvas');c.width=i.width;c.height=i.height;const x=c.getContext('2d');x.drawImage(i,0,0);
  const s=devicePixelRatio,box=Math.round(i.width-2*pad*s),y=Math.round(i.height/2),d=x.getImageData(0,y,i.width,1).data;
  const lum=k=>.2126*d[k*4]+.7152*d[k*4+1]+.0722*d[k*4+2],bg=lum(0),fill=lum(Math.round(pad*s+box*.2)),side=Math.sign(fill-bg);
  const on=[...Array(i.width).keys()].filter(k=>side*(lum(k)-bg)>=Math.abs(fill-bg)/2);
  return {fill:+(fill-bg).toFixed(1),visible:on.length?on.at(-1)-on[0]+1:0,box}},[png.toString('base64'),pad])};
const wrong=[];
const check=(...a)=>{try{same(...a)}catch(e){wrong.push(e.message)}};
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const sizes=process.env.SHOT_DIR?[[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]:[[1440,900,'light'],[390,844,'dark']];
 if(process.env.SHOT_DIR)await mkdir(process.env.SHOT_DIR,{recursive:true});
 for(const [width,height,scheme] of sizes){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,deviceScaleFactor:2});
  await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  const settled=()=>page.waitForFunction(()=>[...document.querySelectorAll('.person-pic img,.org-pic img')].every(i=>i.complete&&i.naturalWidth>0));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#task-c1c1c1c1c1c1c1c1 .card-badges .org-pic img').waitFor();await settled();
  if(process.env.SHOT_DIR)for(const id of ['a1a1a1a1a1a1a1a1','b1b1b1b1b1b1b1b1'])
   await page.locator('#task-'+id+' .card-badges').screenshot({path:`${process.env.SHOT_DIR}/meta-${id.slice(0,2)}-${width}-${scheme}.png`});
  check(await boxes(page,'.card-badges'),'meta rows',['person/picture','person/letter','org/picture','org/letter']);
  const reader=await context.newPage();
  for(const sel of ['#task-a1a1a1a1a1a1a1a1 .card-badges .org-pic','#task-b1b1b1b1b1b1b1b1 .card-badges .person-pic']){
   const v=await looks(page,reader,sel);
   // the box is 2 device pixels a CSS pixel; antialiasing may soften one device pixel on each edge
   if(Math.abs(v.fill)<6||v.visible<v.box-2)wrong.push(`${scheme} ${width}: ${sel} reads smaller than its box ${JSON.stringify(v)}`)}
  await reader.close();
  await navClick(page.locator('nav [data-tab="people"]'));
  await page.locator('#people-view article[data-node="email:lee@brushworks.example"] .person-pic img').waitFor();await settled();
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/people-${width}-${scheme}.png`});
  const peopleList=await boxes(page,'#people-view .graph-row');
  await navClick(page.locator('.side-sub a[data-graph-sub="orgs"]'));
  await page.locator('#people-view article[data-node="org:brushworks.example"] .org-pic img').waitFor();await settled();
  if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/orgs-${width}-${scheme}.png`});
  check([...peopleList.filter(x=>x.kind==='person'),...await boxes(page,'#people-view .graph-row')],'lists',['person/picture','person/letter','org/picture','org/letter']);
  assert.deepEqual(errors,[]);
  await context.close();
 }
 assert.deepEqual(wrong,[]);
 console.log('Avatars: one size per place, for photos, logos and letters alike.');
}finally{await browser?.close();server.close()}
