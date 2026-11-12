import assert from 'node:assert/strict';
import {mkdir,readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections, the tabs of connected sources: each card shows the same colored logo as its row in + Add (connectLogo,
// dashboard/logos), by the catalog's name for its service (Salesflare: crm, Google Docs: docs signed in with Google),
// and none is a broken image. Each card sits on the tab of its source's group (the status's group, as in + Add). A catch-all (Other email) keeps its line icon; Machine health shows the robot.
// Made-up data, a local fixture server. SHOTS=<folder> saves each tab at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
// each source's group as the status gives it (views.source_group, the same as + Add): its tab is Mail and calendar, Chat or Other
const GROUP={gmail:'mail',calendar:'mail',outlook:'mail',outlook_calendar:'mail',imap:'mail',slack:'chat',teams:'chat',whatsapp:'chat',telegram:'chat',
 linkedin:'chat',x:'chat',zoom:'meetings',google_meet:'meetings',docs:'docs',salesflare:'customers',salesforce:'customers',stripe:'customers',
 intercom:'customers',github:'work',trello:'work',shortcut:'work'};
const TAB={mail:'Mail and calendar',chat:'Chat'};
const C=(id,service,name,extra={})=>({id,service,group:GROUP[service]||'other',display_name:name,email:id+'@example.org',transport:'broker',boundary:'work',events:12,recent_events:3,last_success:now,...extra});
// card id -> the logo file it must show (null: its line icon)
const CARDS=[
 [C('gmail','gmail','Gmail'),'logos/gmail.svg'],[C('calendar','calendar','Google Calendar'),'logos/calendar.svg'],
 [C('outlook','outlook','Outlook'),'logos/outlook.svg'],[C('outlook_calendar','outlook_calendar','Outlook Calendar'),'logos/outlook_calendar.svg'],
 [C('imap','imap','Other email',{last:true,transport:'imap'}),null],
 [C('slack','slack','Slack'),'logos/slack.svg'],[C('teams','teams','Microsoft Teams'),'logos/teams.svg'],[C('whatsapp','whatsapp','WhatsApp'),'logos/whatsapp.svg'],
 [C('telegram','telegram','Telegram chats'),'logos/telegram.svg'],
 [C('linkedin','linkedin','LinkedIn'),'logos/linkedin.svg'],[C('x','x','X'),'logos/x.svg'],[C('zoom','zoom','Zoom'),'logos/zoom.png'],
 [C('google_meet','google_meet','Google Meet'),'logos/google_meet.svg'],[C('docs','docs','Microsoft OneDrive'),'logos/docs.svg'],
 [C('gdocs','docs','Google Docs',{docs_provider:'google'}),'logos/google_docs.svg'],[C('crm','salesflare','Salesflare CRM'),'logos/crm.svg'],
 [C('salesforce','salesforce','Salesforce'),'logos/salesforce.svg'],[C('stripe','stripe','Stripe'),'logos/stripe.svg'],
 [C('intercom','intercom','Intercom'),'logos/intercom.svg'],[C('github','github','GitHub'),'logos/github.svg'],
 [C('trello','trello','Trello'),'logos/trello.svg'],[C('shortcut','shortcut','Shortcut'),'logos/shortcut.svg'],
 [C('android','android','Android notifications'),'logos/android.svg'],[C('rss','rss','RSS feed'),'logos/rss.svg'],
 [C('gateway','gateway','Machine health'),'avatar.png']];
const BRAND={'avatar.png':'../brand/app-icon-192.png'};
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const logo=/^\/brand\/(logos\/[a-z_]+\.(svg|png)|avatar\.png)$/.exec(url.pathname);
 if(logo){const file=BRAND[logo[1]]||'../dashboard/'+logo[1];res.setHeader('Content-Type',file.endsWith('.svg')?'image/svg+xml':'image/png');
  try{res.end(await readFile(new URL(file,import.meta.url)))}catch{res.statusCode=404;res.end()}return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:CARDS.map(([c])=>c),suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,mobile] of [[390,844,true],[1440,900,false]])for(const scheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}-${scheme}`;
  await page.goto(base+'/#connections');
  await page.locator('#connectors>article[data-conn="gmail"]').waitFor({state:'attached'});
  for(const [pane,file] of [['Mail and calendar','mail'],['Chat','chat'],['Other sources','other']]){
   await page.evaluate(p=>[...document.querySelectorAll('#health-tabs button')].find(b=>b.textContent.trim().startsWith(p))?.click(),pane);
   // every logo loaded, also the ones below the fold
   const seen=await page.evaluate(()=>Promise.all([...document.querySelectorAll('#connectors>article:not([hidden])')].map(async a=>{const i=a.querySelector('.conn-head img');
    if(i){i.loading='eager';if(!i.complete)await new Promise(r=>{i.onload=i.onerror=r})}
    return [a.dataset.conn,i?i.getAttribute('src'):null,i?i.naturalWidth>0:null]})));
   assert.ok(seen.length>0,`${tag}: ${pane} shows its cards`);
   // a card's tab is its source's group: LinkedIn and X on Chat, a meeting, CRM or work tool on Other sources
   assert.deepEqual(seen.map(([id])=>id).sort(),CARDS.filter(([c])=>(TAB[c.group]||'Other sources')===pane).map(([c])=>c.id).sort(),`${tag}: ${pane} holds its group's cards`);
   for(const [id,src,ok] of seen){const want=CARDS.find(([c])=>c.id===id)[1];
    assert.equal(src,want&&'brand/'+want,`${tag}: ${id} shows ${want||'its line icon'}`);
    if(src)assert.ok(ok,`${tag}: ${id}'s logo is not a broken image`)}
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${tag}: ${pane}: no sideways scroll`);
   if(shots)await page.screenshot({path:`${shots}/cards-${file}-${tag}.png`,fullPage:true})}
  const all=await page.evaluate(()=>[...document.querySelectorAll('#connectors>article')].map(a=>a.dataset.conn));
  assert.deepEqual([...all].sort(),CARDS.map(([c])=>c.id).sort(),`${tag}: every card is on a tab`);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('connection card logos dashboard ok');
}finally{await browser?.close();server.close()}
