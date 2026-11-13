import assert from 'node:assert/strict';
import {mkdir,readFile} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections, the kinds of connected sources: each row shows its source's one-color mark (todos-logos.js, dashboard/logos/mono),
// Google Docs by docs signed in with Google, a catch-all its plain line icon (Other email: the envelope), and every brand's mark
// is a file there. Each card sits under the kind of its source's group (the status's group, as in + Add). A catch-all (Other email) keeps its line icon; Machine health shows the robot.
// Made-up data, a local fixture server. SHOTS=<folder> saves each kind at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
// each source's group as the status gives it (views.source_group, the same as + Add): its kind on Connections
const GROUP={gmail:'mail',calendar:'calendar',outlook:'mail',outlook_calendar:'calendar',imap:'mail',exchange:'calendar',icloud_calendar:'calendar',
 proton_calendar:'calendar',ics:'calendar',caldav:'calendar',slack:'chat',teams:'chat',whatsapp:'chat',telegram:'chat',signal:'chat',
 linkedin:'chat',x:'chat',zoom:'meetings',google_meet:'meetings',docs:'docs',salesflare:'customers',salesforce:'customers',stripe:'customers',
 intercom:'customers',github:'work',trello:'work',shortcut:'work'};
const KIND={mail:'Email',calendar:'Calendar',chat:'Chat',meetings:'Meetings',docs:'Docs and files',customers:'Customers',work:'Projects and code',other:'Other'};
const C=(id,service,name,extra={})=>({id,service,group:GROUP[service]||'other',display_name:name,email:id+'@example.org',transport:'broker',boundary:'work',events:12,recent_events:3,last_success:now,...extra});
// card id -> the mark it must show (.via-<mark>)
const CARDS=[
 [C('gmail','gmail','Gmail'),'gmail'],[C('calendar','calendar','Google Calendar'),'calendar'],
 [C('outlook','outlook','Outlook'),'outlook'],[C('outlook_calendar','outlook_calendar','Outlook Calendar'),'outlook_calendar'],
 [C('imap','imap','Other email',{last:true,transport:'imap'}),'mail'],
 [C('ews','exchange','Exchange Server',{transport:'ews'}),'exchange'],[C('icloud','icloud_calendar','iCloud Calendar',{transport:'caldav'}),'icloud_calendar'],
 [C('proton','proton_calendar','Proton Calendar',{transport:'ics'}),'proton_calendar'],
 [C('ics','ics','Calendar link (ICS)',{last:true,transport:'ics'}),'cal'],[C('caldav','caldav','Other calendar',{last:true,transport:'caldav'}),'cal'],
 [C('slack','slack','Slack'),'slack'],[C('teams','teams','Microsoft Teams'),'teams'],[C('whatsapp','whatsapp','WhatsApp'),'whatsapp'],
 [C('telegram','telegram','Telegram chats'),'telegram'],[C('signal','signal','Signal chats'),'signal'],
 [C('linkedin','linkedin','LinkedIn'),'linkedin'],[C('x','x','X'),'x'],[C('zoom','zoom','Zoom'),'zoom'],
 [C('google_meet','google_meet','Google Meet'),'google_meet'],[C('docs','docs','Microsoft OneDrive'),'docs'],
 [C('gdocs','docs','Google Docs',{docs_provider:'google'}),'google_docs'],[C('crm','salesflare','Salesflare CRM'),'salesflare'],
 [C('salesforce','salesforce','Salesforce'),'salesforce'],[C('stripe','stripe','Stripe'),'stripe'],
 [C('intercom','intercom','Intercom'),'intercom'],[C('github','github','GitHub'),'github'],
 [C('trello','trello','Trello'),'trello'],[C('shortcut','shortcut','Shortcut'),'shortcut'],
 [C('android','android','Android notifications'),'android'],[C('rss','rss','RSS feed'),'rss'],
 [C('gateway','gateway','Machine health'),'gateway']];
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
  for(const [file,pane] of Object.entries(KIND)){
   await page.evaluate(k=>document.querySelector(`#health-tabs button.conn-cat[data-health-pane="${k}"]`).click(),file);
   assert.equal(await page.locator(`#health-tabs button.conn-cat[data-health-pane="${file}"] .ell`).textContent(),pane,`${tag}: the ${pane} kind`);
   // every logo loaded, also the ones below the fold
   const seen=await page.evaluate(()=>Promise.all([...document.querySelectorAll('#connectors>article:not([hidden])')].map(async a=>{const i=a.querySelector('.conn-row>.icon>.via-ico');
    return [a.dataset.conn,i?[...i.classList].find(c=>c.startsWith('via-')&&c!=='via-ico').slice(4):null,i?getComputedStyle(i).maskImage!=='none':null]})));
   assert.ok(seen.length>0,`${tag}: ${pane} shows its cards`);
   // a card's kind is its source's group: LinkedIn and X under Chat, Zoom under Meetings, a group without a kind under Other
   assert.deepEqual(seen.map(([id])=>id).sort(),CARDS.filter(([c])=>(KIND[c.group]?c.group:'other')===file).map(([c])=>c.id).sort(),`${tag}: ${pane} holds its group's cards`);
   for(const [id,mark,ok] of seen){const want=CARDS.find(([c])=>c.id===id)[1];
    assert.equal(mark,want,`${tag}: ${id} shows the ${want} mark`);assert.ok(ok,`${tag}: ${id}'s mark is drawn`);
    if(!['mail','cal'].includes(want))assert.ok(existsSync(new URL(`../dashboard/logos/mono/${want}.svg`,import.meta.url)),`${tag}: ${want} has its mark file`)}
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${tag}: ${pane}: no sideways scroll`);
   if(shots)await page.screenshot({path:`${shots}/cards-${file}-${tag}.png`,fullPage:true})}
  const all=await page.evaluate(()=>[...document.querySelectorAll('#connectors>article')].map(a=>a.dataset.conn));
  assert.deepEqual([...all].sort(),CARDS.map(([c])=>c.id).sort(),`${tag}: every card is under a kind`);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('connection card logos dashboard ok');
}finally{await browser?.close();server.close()}
