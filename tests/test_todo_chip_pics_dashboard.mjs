import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's chips show who and which organization it is about with their photo or logo when the Graph has one
// (graph.node_picture): a photo only when saved on this Machine, a logo also as an https link. Without one, or with any
// other link, the chip keeps its icon. A picture never makes the chip taller.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const PHOTO='api/person-photo?p='+'a'.repeat(32),LOGO='api/person-photo?p='+'b'.repeat(32);
// A made-up 1x1 PNG
const PNG=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==','base64');
const card=(id,person,extra)=>({id,title:'Answer the quote question '+id.slice(0,2),body:'They asked about the quote.',status:'pending',created_at:now,event_ids:[1],
 people:[person],source_line:'Source: Email',scope:'work',...extra});
const cards=[
 card('a1a1a1a1a1a1a1a1',{id:'email:lee@brushworks.example',name:'Lee Example',photo:PHOTO},{org_said:true,org_node:{id:'org:brushworks.example',name:'Brushworks',logo:LOGO}}),
 card('b1b1b1b1b1b1b1b1',{id:'email:pat@bigcorp.example',name:'Pat Example',org:{id:'org:bigcorp.example',name:'Bigcorp',logo:'https://logo.invalid/b.png'}}),
 card('c1c1c1c1c1c1c1c1',{id:'email:kim@globex.example',name:'Kim Example',photo:'https://media.invalid/k.jpg'},
  {org_said:true,org_node:{id:'org:globex.example',name:'Globex',logo:'javascript:alert(1)'}})];
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/person-photo'){res.setHeader('Content-Type','image/png');res.end(PNG);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{pending:cards.length},decisions:[],analyses:[],deliveries:[],
  review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1280,390]){
  const context=await browser.newContext({viewport:{width,height:900}});
  const outside=[];
  await context.route('**/*',route=>{const host=new URL(route.request().url()).hostname;if(host==='127.0.0.1')return route.continue();outside.push(host);return route.abort()});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
  const pic=async(id,org)=>{const chip=page.locator(`#task-${id} .card-badges a.chip.who${org?'.org':':not(.org)'}`);
   return {img:await chip.locator('.chip-pic img').getAttribute('src').catch(()=>null),icon:await chip.locator('svg.ci').count(),h:Math.round((await chip.boundingBox()).height)}};
  const lee=await pic('a1a1a1a1a1a1a1a1'),brush=await pic('a1a1a1a1a1a1a1a1',true);
  assert.equal(lee.img,PHOTO);assert.equal(brush.img,LOGO);
  await page.waitForFunction(()=>[...document.querySelectorAll('#task-a1a1a1a1a1a1a1a1 .chip-pic img')].every(i=>i.complete&&i.naturalWidth>0));
  assert.equal((await pic('b1b1b1b1b1b1b1b1')).img,null);  // no photo: the person icon
  assert.equal((await pic('b1b1b1b1b1b1b1b1',true)).img,'https://logo.invalid/b.png');  // a logo link, as the Graph's lists show it
  const kim=await pic('c1c1c1c1c1c1c1c1'),globex=await pic('c1c1c1c1c1c1c1c1',true);
  assert.equal(kim.img,null);assert.equal(kim.icon,1);  // a photo link from elsewhere is never loaded
  assert.equal(globex.img,null);assert.equal(globex.icon,1);
  assert.equal(lee.h,kim.h);assert.equal(brush.h,globex.h);  // a picture never makes the chip taller
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  assert.ok(!outside.includes('media.invalid'));
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('To-dos: who and which organization show their photo or logo when the Graph has one.');
}finally{await browser?.close();server.close()}
