import assert from 'node:assert/strict';
import {mkdir,readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections: Suggested for you on top, only for the tiles the Machine has a signal for (connect_sources'
// suggested, at most 3, never a connected one), each with its why line; no signal, no section. Then every source in its kind
// (the kinds of Connections, a page each), in the groups' order and A to Z within each, a suggested one there too, tagged Suggested, with what it
// brings in; both rows open the same connect. Teams shows twice: its chats under Chat, Teams meetings under Meetings, one sign-in.
// Salesforce shows its own logo.
// SHOTS=<folder> saves the list at 390 and 1440, light and dark, with and without suggestions.
const dashboard=await dashboardPage();
const S=(name,label,group,what,extra={})=>({name,service:name,label,group,what,connected:0,broker:false,...extra});
const sources=[
 S('android','Android notifications','other','The notifications on your Android phone, through the OpenClaw app.'),
 S('calendar','Google Calendar','calendar','Your meetings, so you go in prepared and follow up.',{connected:1,hosted_signin:'calendar'}),
 S('ics','Calendar link (ICS)','calendar','Any calendar that gives a link. Read-only.',{last:true}),  // catch-alls: last in Calendar, A to Z among them
 S('caldav','Other calendar','calendar','Any CalDAV calendar. Read-only.',{last:true}),
 S('exchange','Exchange Server','calendar','Meetings from your company’s own Exchange Server. Read-only.'),
 S('icloud_calendar','iCloud Calendar','calendar','Meetings from your iCloud calendars. Read-only.'),
 S('proton_calendar','Proton Calendar','calendar','A Proton calendar through its share link. Read-only.'),
 S('crm','Salesflare CRM','customers','Accounts, contacts and deals, so it knows who matters.'),
 S('gateway','Machine health','other',"Your Machine's own log, so it spots its own trouble.",{connected:1}),
 S('imap','Other email','mail','Mail from any other provider, over IMAP.',{last:true}),  // a catch-all: last in its group, not at O
 S('zzz_other','Other things','other','A made-up catch-all in Other.',{last:true}),
 S('gmail','Gmail','mail','Your email, what comes in and what you send.',{connected:1,hosted_signin:'gmail'}),
 S('outlook','Outlook','mail','Your Outlook email, what comes in and what you send.',{hosted_signin:'outlook'}),
 S('outlook_calendar','Outlook Calendar','calendar','Your Outlook meetings, so you go in prepared and follow up.',{hosted_signin:'outlook_calendar'}),
 S('salesforce','Salesforce','customers','Deals, tasks and activity.',{hosted_signin:'salesforce'}),
 S('teams','Microsoft Teams','chat','Chats, meeting chats and meeting notes from Teams. Reads only.',{broker:true,connected:1,hosted_signin:'microsoft_teams'}),
 S('slack','Slack','chat','Your direct messages, mentions and the threads you are in.',{hosted_signin:'slack'}),
 S('telegram','Telegram chats','chat','Your Telegram chats and small groups.'),
 S('whatsapp','WhatsApp','chat','Your WhatsApp chats, as a linked device.'),
 S('docs','Microsoft OneDrive','docs','Word files: comments, shares, and new docs or edits you approve.',{hosted_signin:'docs'}),
 S('google_docs','Google Docs','docs','Reads and edits the Google Docs you point it to, and makes new ones.',{hosted_signin:'google_docs'}),
 S('github','GitHub','work','Review requests, mentions, assignments and failed CI runs.',{hosted_signin:'github'}),
 S('google_meet','Google Meet','meetings','Meeting transcripts and Gemini notes from Google Meet.',{hosted_signin:'google_meet'}),
 S('intercom','Intercom','customers','Customer conversations in your Intercom workspace.',{hosted_signin:'intercom'}),
 S('linkedin','LinkedIn','chat','Your LinkedIn messages.'),
 S('rss','RSS feed','other','Posts from the feeds you follow.'),
 S('shortcut','Shortcut','work','Stories that change state, with their owners and deadlines.'),
 S('stripe','Stripe','customers','Failed payments, disputes, churn and big new subscriptions.',{hosted_signin:'stripe'}),
 S('trello','Trello','work','Card changes, comments and activity on one Trello board.'),
 S('x','X','chat','Your mentions and direct messages on X.'),
 S('zoom','Zoom','meetings','Meeting summaries and transcripts from Zoom.',{broker:true,hosted_signin:'zoom'}),
 S('newthing','Newthing','','A connector with no group of its own.')];
// gmail is connected (dropped), nope is no tile (dropped): four stay, in the order given
const SUGGESTED=[{name:'trello',why:'unfinished',count:0},{name:'stripe',why:'mail',count:12},{name:'zoom',why:'meetings',count:9},
 {name:'gmail',why:'mail',count:40},{name:'nope',why:'mail',count:5},{name:'google_docs',why:'links',count:7}];
let suggested=SUGGESTED;
// Connections, Email and Calendar tabs: A to Z by name, the catch-all cards (Other email; Other calendar, a calendar link)
// after the others, though the config lists them first
const now=new Date().toISOString();
const CARD=(id,service,group,display_name,extra={})=>({id,service,group,display_name,email:'me@'+id+'.example',transport:'broker',boundary:'personal',events:3,recent_events:1,last_success:now,...extra});
const CARDS=[CARD('imap','imap','mail','Other email',{last:true,transport:'imap'}),CARD('gmail','gmail','mail','Gmail'),
 CARD('ics','ics','calendar','Team calendar',{last:true}),CARD('caldav','caldav','calendar','Other calendar',{last:true}),
 CARD('gcal','calendar','calendar','Google Calendar'),CARD('ews','exchange','calendar','Exchange Server')];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const logo=/^\/brand\/logos\/([a-z_]+\.(svg|png))$/.exec(url.pathname);  // the logos, so the shots show them
 if(logo){res.setHeader('Content-Type',logo[2]==='svg'?'image/svg+xml':'image/png');res.end(await readFile(new URL('../dashboard/logos/'+logo[1],import.meta.url)));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:CARDS,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:'https://app.example.org/account',sources,suggested,codex:{status:'signed_out'}}));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
// Suggested for you (on the list of kinds), then each kind's sources as its page shows them, under the kind's name
const read=page=>page.evaluate(()=>{const tiles=g=>[...g.querySelectorAll('.connect-source')].map(n=>({name:n.querySelector('b').textContent,
 why:n.querySelector('small.why')?.textContent||null,tag:n.querySelector('.cs-tag')?.textContent||null,what:n.querySelector('small.what')?.textContent||null,
 on:!!n.querySelector('.cs-on'),signin:n.dataset.connectSignin||null,logo:n.querySelector('.cs-icon img')?.getAttribute('src')||null}));
 const out=[],sug=document.querySelector('#conn-suggested .connect-group.suggested');if(sug?.getClientRects().length)out.push({suggested:true,head:sug.querySelector('h4').textContent,tiles:tiles(sug)});
 for(const b of [...document.querySelectorAll('#health-tabs .conn-cat')].filter(b=>CONNECT_GROUPS.some(([k])=>k===b.dataset.healthPane))){showHealthPane(b.dataset.healthPane);
  out.push({suggested:false,head:b.querySelector('.ell').textContent,tiles:[...document.querySelectorAll('#connect-add .connect-group')].flatMap(tiles)})}
 return out});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,mobile,scheme] of [[390,844,true,'light'],[390,844,true,'dark'],[1440,900,false,'light'],[1440,900,false,'dark']]){
  for(const mode of ['suggested','none']){
   suggested=mode==='suggested'?SUGGESTED:[];
   const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
   await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
   const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
   const tag=`${width}x${height}-${scheme}-${mode}`;
   await page.goto(base+'/#connections=add');
   await page.locator('#connect-add .connect-group').first().waitFor({state:'attached'});await page.locator('#health-tabs .conn-cat').first().waitFor();
   const groups=await read(page);
   const heads=groups.map(g=>g.head);
   const top=groups[0].suggested?groups[0]:null,rest=groups.filter(g=>!g.suggested),tile=(h,n)=>rest.find(g=>g.head===h).tiles.find(x=>x.name===n);
   if(mode==='suggested'){
    assert.equal(top?.head,'Suggested for you',`${tag}: Suggested for you comes first`);
    assert.deepEqual(top.tiles.map(x=>[x.name,x.why,x.tag]),[['Trello','Setup didn’t finish',null],['Stripe','12 emails from Stripe in 30 days',null],
     ['Zoom','9 Zoom meetings on your calendar',null]],`${tag}: at most 3 suggestions with their why, connected and unknown ones left out`);
   }else assert.ok(!groups.some(g=>g.suggested)&&!heads.includes('Suggested for you'),`${tag}: no signal, no Suggested section`);
   assert.deepEqual(rest.map(g=>g.head),['Email','Calendar','Chat','Meetings','Docs and files','Customers','Projects and code','Other'],`${tag}: the groups in order`);
   // every source the list gives shows in a group, a two-group one (Teams) in each
   const shown=new Set(rest.flatMap(g=>g.tiles.map(x=>x.name)));
   for(const x of sources)assert.ok(shown.has(x.label),`${tag}: ${x.label} shows in its kind`);
   assert.deepEqual(rest.filter(g=>g.tiles.some(x=>/Teams/.test(x.name))).map(g=>g.head),['Chat','Meetings'],`${tag}: Teams shows under Chat and Meetings`);
   assert.deepEqual(rest.find(g=>g.head==='Email').tiles.map(x=>x.name),['Gmail','Outlook','Other email'],`${tag}: Email holds the mailboxes, Other email last`);
   assert.deepEqual(rest.find(g=>g.head==='Calendar').tiles.map(x=>x.name),['Exchange Server','Google Calendar','iCloud Calendar','Outlook Calendar','Proton Calendar',
    'Calendar link (ICS)','Other calendar'],`${tag}: Calendar holds every calendar, Exchange Server too, the catch-alls last`);
   assert.equal(tile('Calendar','Exchange Server').logo,'brand/logos/exchange.svg',`${tag}: Exchange Server shows its own logo`);
   assert.deepEqual(['iCloud Calendar','Proton Calendar','Calendar link (ICS)','Other calendar'].map(n=>tile('Calendar',n).logo),
    ['brand/logos/icloud_calendar.svg','brand/logos/proton_calendar.svg',null,null],`${tag}: iCloud and Proton their logos, the catch-alls the calendar line icon`);
   for(const g of rest){const names=g.tiles.map(x=>x.name).filter(n=>!sources.some(s=>s.last&&s.label===n));
    assert.deepEqual(names,[...names].sort((a,b)=>a.localeCompare(b,'en',{sensitivity:'base'})),`${tag}: ${g.head} reads A to Z`);
    assert.ok(g.tiles.every(x=>x.why===null),`${tag}: ${g.head} shows what each brings in, not a why`)}
   const all=rest.flatMap(g=>g.tiles.map(x=>x.name));
   assert.equal(all.length,new Set(all).size,`${tag}: no source shows twice among the groups`);
   const marked=rest.flatMap(g=>g.tiles.filter(x=>x.tag).map(x=>[g.head,x.name,x.tag,!!x.what]));
   assert.deepEqual(marked,mode==='suggested'?[['Meetings','Zoom','Suggested',true],['Customers','Stripe','Suggested',true],['Projects and code','Trello','Suggested',true]]:[],
    `${tag}: each suggested one also stays in its own group, tagged Suggested, with what it brings in`);
   assert.equal(tile('Docs and files','Google Docs').tag,null,`${tag}: a 4th suggestion is a plain row in its group`);
   if(top)for(const x of top.tiles){const g=rest.flatMap(r=>r.tiles).find(y=>y.name===x.name);assert.deepEqual([x.signin,x.logo,x.on],[g.signin,g.logo,g.on],`${tag}: ${x.name} opens the same connect in both places`)}
   assert.deepEqual(rest.find(g=>g.head==='Meetings').tiles.map(x=>x.name),['Google Meet','Teams meetings','Zoom']);
   assert.deepEqual(rest.find(g=>g.head==='Projects and code').tiles.map(x=>x.name),['Codex','GitHub','Shortcut','Trello']);
   // Teams: two tiles, one sign-in, both connected
   const chat=tile('Chat','Microsoft Teams'),meet=tile('Meetings','Teams meetings');
   assert.deepEqual([chat.what,chat.signin,chat.on,meet.what,meet.signin,meet.on],['Chats and meeting chats from Teams. Read-only.','teams',true,
    'Meeting notes and transcripts from Teams. Read-only.','teams',true],`${tag}: Teams chats and Teams meetings share one sign-in`);
   assert.equal(meet.logo,'brand/logos/teams.svg');
   assert.equal(tile('Customers','Salesforce').logo,'brand/logos/salesforce.svg',`${tag}: Salesforce shows its own logo`);
   assert.ok(rest.find(g=>g.head==='Other').tiles.some(x=>x.name==='Newthing'),`${tag}: a source without a known group is under Other`);
   // a catch-all row (the source's `last`) closes its group, after the A to Z rows, in every group that has one
   const lastOf=Object.fromEntries(sources.filter(x=>x.last).map(x=>[x.label,true]));
   for(const g of rest){const names=g.tiles.map(x=>x.name),k=names.findIndex(n=>lastOf[n]);
    if(k>=0)assert.ok(names.slice(k).every(n=>lastOf[n]),`${tag}: ${g.head}: the catch-all rows come last (${names.join(', ')})`)}
   assert.equal(rest.find(g=>g.head==='Email').tiles.at(-1).name,'Other email');
   assert.equal(rest.find(g=>g.head==='Other').tiles.at(-1).name,'Other things');
   if(mode==='none'&&width===1440&&scheme==='light'){
    await page.goto(base+'/#connections');await page.locator('#connectors>article[data-conn="imap"]').waitFor({state:'attached'});
    assert.deepEqual(await page.evaluate(()=>[...document.querySelectorAll('#connectors>article[data-group="mail"]')].map(a=>a.dataset.conn)),['gmail','imap'],'Connections: the catch-all card comes last in its tab');
    assert.deepEqual(await page.evaluate(()=>[...document.querySelectorAll('#connectors>article[data-group="calendar"]')].map(a=>a.dataset.conn)),['ews','gcal','caldav','ics'],
     'Connections: Calendar reads A to Z, the catch-alls last');
    assert.deepEqual(await page.evaluate(()=>[...document.querySelectorAll('#health-tabs .conn-cat .ell')].map(b=>b.textContent.trim())).then(x=>x.slice(0,2)),['Email','Calendar'],
     'Connections: Email and Calendar are kinds of their own');
    assert.equal(await page.evaluate(()=>document.querySelector('#connectors>article[data-conn="ews"] .conn-row .via-ico')?.classList.contains('via-exchange')),true,
     'Connections: the Exchange Server row shows its mark');
    await page.evaluate(()=>[...document.querySelectorAll('#health-tabs button')].find(b=>b.textContent.trim().startsWith('Email'))?.click());await page.locator('#connectors>article[data-conn="imap"]').waitFor();
    if(shots)await page.screenshot({path:`${shots}/connections-mail-${width}-${scheme}.png`,fullPage:true});
    await page.goto(base+'/#connections=add');await page.locator('#connect-add .connect-group').first().waitFor({state:'attached'})}
   // nothing wider than the screen
   const wide=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
   assert.ok(wide<=0,`${tag}: no sideways scroll (${wide}px)`);
   if(shots)await page.evaluate(()=>Promise.all([...document.querySelectorAll('#connect-add img')].map(i=>{i.loading='eager';return i.complete?0:new Promise(r=>{i.onload=i.onerror=r})})));  // every logo in the shot
   if(shots)await page.screenshot({path:`${shots}/${tag}.png`,fullPage:true});
   await context.close()}}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('connect add groups dashboard ok');
