import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Tapping the avatar on a person's or an organization's page opens the Picture dialog, which shows that avatar big:
// the picture when there is one (with Remove picture), the initials when not. It once showed the avatar's markup as
// text (the page's innerHTML went into html`` as a string). No view on the way may show avatar markup as text either.
// SHOT_DIR=… also saves screenshots.
const dashboard=await dashboardPage();
const day=new Date(Date.now()-864e5).toISOString();
const PIC='<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" fill="#c9b8a6"/><circle cx="100" cy="80" r="40" fill="#7a5c48"/><path d="M30 200c6-44 34-64 70-64s64 20 70 64z" fill="#3d5a80"/></svg>';
const LOGO='<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" fill="#0f766e"/><path d="M55 145 100 55l45 90" fill="none" stroke="#fff" stroke-width="20"/></svg>';
const person=(id,name,photo)=>({id:'email:'+id,kind:'person',name,strength:2.1,closeness:'regular',last_at:day,signals:6,ids:[id],usual_gap_days:7,
 quiet:false,role:null,org:'org:'+id.split('@')[1],org_name:null,org_by:'email',profile:photo?{photo}:null,links:[],recent:[],around:[],open:{}});
const org=(id,name,logo)=>({id:'org:'+id,kind:'org',name,domain:id,signals:3,last_at:day,role:null,strength:1,
 profile:{name,industry:'Software Development',...(logo?{logo}:{})},about:'Software Development',links:[],recent:[],around:[]});
const people=[person('lee@brushworks.example','Lee Example','api/person-photo?p='+'a'.repeat(32)),person('kim@globex.example','Kim Example',null)];
const orgs=[org('brushworks.example','Brushworks','api/person-photo?p='+'b'.repeat(32))];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/person-photo'){res.setHeader('Content-Type','image/svg+xml');res.end(url.searchParams.get('p')[0]==='b'?LOGO:PIC);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{pending:0},decisions:[],analyses:[],deliveries:[],
  review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/graph'){const node=url.searchParams.get('node');res.end(JSON.stringify(node?[...people,...orgs].find(n=>n.id===node):{projects:[],people,quiet:[],new:[],orgs}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
// Markup shown as text anywhere on the page or in an open dialog
const markupAsText=page=>page.evaluate(()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),hits=[];
 for(let n;(n=w.nextNode());)if(/<(?:span|img|div|button)\b|&lt;/.test(n.data)&&n.parentElement?.checkVisibility())hits.push(n.data.slice(0,120));return hits});
const dialog=page=>page.evaluate(()=>{const d=document.querySelector('#crm-dialog'),now=d.querySelector('.pic-now'),pic=now.querySelector('.person-pic,.org-pic'),img=pic?.querySelector('img'),r=pic?.getBoundingClientRect();
 return {open:d.open,text:now.textContent.trim(),kind:pic?.classList.contains('org-pic')?'org':pic?'person':null,initials:pic?.dataset.i,w:Math.round(r?.width||0),
  img:img?{loaded:img.complete&&img.naturalWidth>0,w:Math.round(img.getBoundingClientRect().width)}:null,remove:!!d.querySelector('[data-pic-remove]')}});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const sizes=process.env.SHOT_DIR?[[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]:[[390,844,'light']];
 if(process.env.SHOT_DIR)await mkdir(process.env.SHOT_DIR,{recursive:true});
 for(const [width,height,scheme] of sizes){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,deviceScaleFactor:2});
  await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await navClick(page.locator('nav [data-tab="people"]'));
  await page.locator('#people-view article[data-node="email:lee@brushworks.example"]').waitFor();
  assert.deepEqual(await markupAsText(page),[],'people list');
  const open=async(id,name,want)=>{
   await page.evaluate(id=>{location.hash=graphHash(id)},id);
   await page.locator(`.graph-detail [data-pic-edit="${id}"]`).waitFor();
   assert.deepEqual(await markupAsText(page),[],name+' page');
   await page.locator(`.graph-detail [data-pic-edit="${id}"]`).click();
   await page.locator('#crm-dialog[open] .pic-now').waitFor();
   if(want.img)await page.waitForFunction(()=>[...document.querySelectorAll('#crm-dialog .pic-now img')].every(i=>i.complete&&i.naturalWidth>0));
   const got=await dialog(page),at=`${name} ${width} ${scheme} `+JSON.stringify(got);
   assert.deepEqual(await markupAsText(page),[],at);
   assert.ok(got.open&&got.kind===want.kind&&got.w===72,at);  // the avatar itself, big
   if(want.img)assert.ok(got.img?.loaded&&got.img.w===72&&got.remove&&got.text==='',at);
   else assert.ok(!got.img&&!got.remove&&got.initials===want.initials,at);
   if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/picture-${name}-${width}-${scheme}.png`});
   await page.locator('#crm-dialog .ed-actions [data-crm-close]').click();await page.locator('#crm-dialog[open]').waitFor({state:'detached'})};
  await open('email:lee@brushworks.example','photo',{kind:'person',img:true});
  await open('email:kim@globex.example','initials',{kind:'person',img:false,initials:'KE'});
  await open('org:brushworks.example','logo',{kind:'org',img:true});
  assert.deepEqual(errors,[]);
  await context.close();
 }
 console.log('Picture dialog: the avatar shows big, as a picture or initials, never as markup text.');
}finally{await browser?.close();server.close()}
