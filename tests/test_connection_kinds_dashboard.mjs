import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections by kind: every connected source shows in its kind's list at the top, also one with no card of its own
// there (Codex; Google Docs on the owner's Google sign-in, which opens that card), and Disconnected lately shows each
// removed account under its own kind only (a Google account under Email, Slack under Chat, nothing under Other).
// The OneDrive row has OneDrive's one-color mark. SHOTS=<dir> saves each kind at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const at=new Date().toISOString(),week=new Date(Date.now()-7*86400e3).toISOString();
const card=(id,service,group,title,sub,extra={})=>({id,service,group,display_name:title,card_title:title,card_subtitle:sub,boundary:'work:Acme',
 total:120,signals_24h:4,last_success:at,sync_activity:[],...extra});
const connectors=[card('g','gmail','mail','alex@acme.example','Work · acme.example'),card('d','docs','docs','alex@contoso.example','Personal',{docs_provider:'microsoft'}),
 card('gh','github','work','Alex Example','Work'),card('tr','trello','work','Launch Board','Work'),card('sl','slack','chat','Acme','Work'),
 card('gw','gateway','other','Machine health','',{signals:false})];
const disconnected=[{card_title:'old@gmail.example',card_subtitle:'Google account',mark:'google',provider_name:'Google',group:'mail',state:'removed',at:week},
 {card_title:'Slack',card_subtitle:'',mark:'slack',provider_name:'Slack',group:'chat',state:'removed',at:week}];
const src=(name,group,label,connected=0,more={})=>({name,service:name,group,label,connected,what:label+' things.',...more});
const sources=[src('gmail','mail','Gmail',1),src('docs','docs','Microsoft OneDrive',1),src('google_docs','docs','Google Docs',1,{via:['g']}),
 src('github','work','GitHub',1),src('trello','work','Trello',1),src('shortcut','work','Shortcut'),src('slack','chat','Slack',1),
 src('gateway','other','Machine health',1),src('rss','other','RSS feed')];
const server=createServer(async(req,res)=>{
 const logo=/^\/brand\/(logos\/(?:mono\/)?[a-z_]+\.(?:svg|png))$/.exec(req.url);
 if(logo||req.url==='/brand/avatar.png'){const f=logo?'dashboard/'+logo[1]:'brand/app-icon-192.png';
  try{res.setHeader('Content-Type',f.endsWith('.svg')?'image/svg+xml':'image/png');res.end(await readFile(new URL('../'+f,import.meta.url)))}catch{res.statusCode=404;res.end()}return}
 res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url.startsWith('/api/status')){res.end(JSON.stringify({suggestions:[],promises:[],connectors,disconnected,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:null,paired:true,codex:{status:'connected'},gbrain:{on:false},sources,suggested:[]}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
// the rows the open kind shows at the top, and those of Disconnected lately
const rows=page=>page.evaluate(()=>({top:[...document.querySelectorAll('#connectors>article')].filter(a=>!a.hidden).map(a=>a.querySelector('.conn-name').textContent),
 gone:[...document.querySelectorAll('#disconnected article')].filter(a=>a.offsetParent).map(a=>a.querySelector('.conn-name').textContent),
 ticks:document.querySelectorAll('#connect-add .connect-source .cs-on').length}));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const runs=shots?[[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]:[[1440,900,'light'],[390,844,'dark']];
 for(const [width,height,scheme] of runs){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  const open=async kind=>{await page.goto(base+'/#connections='+kind);await page.locator('#connect-add .connect-source').first().waitFor();await page.waitForTimeout(300)};
  const want={docs:[['alex@contoso.example','alex@acme.example'],[]],work:[['Alex Example','Launch Board','Codex'],[]],mail:[['alex@acme.example'],['old@gmail.example']],
   chat:[['Acme'],['Slack']],other:[['Machine health'],[]]};
  for(const [kind,[top,gone]] of Object.entries(want)){
   await open(kind);const r=await rows(page);
   assert.deepEqual(r.top,top,kind+': every connected source in the list at the top');
   assert.ok(r.top.length>=r.ticks,kind+': each ticked source to add has its row at the top');
   assert.deepEqual(r.gone,gone,kind+': only its own disconnected accounts');
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
   if(shots&&kind!=='chat')await page.screenshot({path:`${shots}/connections-${kind}-${width}-${scheme}.png`,fullPage:true});
  }
  // OneDrive's own one-color mark on its row; Google Docs with Google Docs' mark, opening the Google sign-in's card
  await open('docs');
  const marks=await page.evaluate(()=>[...document.querySelectorAll('#connectors>article:not([hidden]) .icon .via-ico')].map(i=>i.className));
  assert.deepEqual(marks,['via-ico via-docs','via-ico via-google_docs']);
  await page.locator('#connectors>article.conn-extra [data-connect-card="g"]').click();
  await page.locator('#connectors>article[data-conn="g"] .conn-body:not([hidden])').waitFor();
  // Codex: its row opens its sign-in panel
  await open('work');await page.locator('#connectors>article.conn-extra [data-codex-signin]').click();
  assert.equal(await page.locator('#connect-add h3').innerText(),'Codex');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('connection kinds ok');
}finally{await browser?.close();server.close()}
