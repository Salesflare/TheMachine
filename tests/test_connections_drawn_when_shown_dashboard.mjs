import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A refresh with another tab on screen leaves the Connections cards be (drawing them cost every To-dos refresh a
// render); the moment Connections shows again they are drawn from the latest refresh, before it paints. With
// Connections on screen a refresh draws them at once, and an opened card stays open through it.
const dashboard=await dashboardPage();
const at=new Date().toISOString();
const card=(id,name)=>({id,service:'gmail',group:'mail',display_name:name,card_title:name,card_subtitle:'Work',boundary:'work:Acme',total:10,signals_24h:1,last_success:at,sync_activity:[]});
let connectors=[card('a','alex@acme.example')];
const server=createServer((req,res)=>{
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');
 if(req.url.startsWith('/api/status')){res.end(JSON.stringify({suggestions:[],promises:[],connectors,disconnected:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){
  connectors=[card('a','alex@acme.example')];
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#connections=mail');
  await page.locator('#connectors article[data-conn="a"]').waitFor();
  await page.evaluate(()=>{window.draws=0;const draw=window.drawConnectors;window.drawConnectors=()=>{window.draws++;draw()}});
  const names=()=>page.evaluate(()=>[...document.querySelectorAll('#connectors>article[data-conn]')].map(a=>a.dataset.conn));

  // To-dos on screen: a refresh leaves the cards be
  await page.evaluate(()=>document.querySelector('nav [data-tab="inbox"]').click());
  connectors=[card('a','alex@acme.example'),card('b','sam@contoso.example')];
  await page.evaluate(()=>refresh());await page.evaluate(()=>refresh());
  assert.equal(await page.evaluate(()=>draws),0,'not drawn while hidden');
  assert.deepEqual(await names(),['a']);

  // Connections shows: drawn from the latest refresh, before the next frame
  const shown=await page.evaluate(async()=>{document.querySelector('nav [data-tab="health"]').click();await Promise.resolve();
   return {draws,names:[...document.querySelectorAll('#connectors>article[data-conn]')].map(a=>a.dataset.conn),
    visible:[...document.querySelectorAll('#connectors>article[data-conn]')].filter(a=>!a.hidden).length}});
  assert.equal(shown.draws,1,'drawn once on showing');
  assert.deepEqual(shown.names,['a','b']);
  assert.equal(shown.visible,2,'both under Email');
  await page.evaluate(()=>{document.querySelector('nav [data-tab="inbox"]').click();document.querySelector('nav [data-tab="health"]').click()});
  assert.equal(await page.evaluate(()=>draws),1,'nothing new: not drawn again');

  // Connections on screen: a refresh draws at once, and an opened card stays open
  await page.evaluate(()=>{const d=document.querySelector('#sync-details-a');if(d)d.open=true});
  connectors=[card('a','alex@acme.example'),card('b','sam@contoso.example'),card('c','robin@example.org')];
  await page.evaluate(()=>refresh());
  assert.ok(await page.evaluate(()=>draws)>1,'drawn on the refresh');
  assert.deepEqual(await names(),['a','c','b']);
  assert.ok(await page.evaluate(()=>!document.querySelector('#sync-details-a')||document.querySelector('#sync-details-a').open),'an opened card stays open');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('connections drawn when shown ok');
}finally{await browser?.close();server.close()}
