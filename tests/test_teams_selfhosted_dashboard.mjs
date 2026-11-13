import assert from 'node:assert/strict';
import {mkdir,readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Connections, + Add on a paired self-hosted Machine: Microsoft Teams shows under Chat and Teams meetings under Meetings,
// one sign-in through the control plane (connect_sources' signin microsoft_teams, test_teams_selfhosted.py). Either
// row opens Sign in with Microsoft, which starts the `teams` sign-in; coming back, it says Connected to Microsoft Teams.
// SHOTS=<folder> saves the list and the sign-in step at 390 and 1440, light and dark.
const dashboard=await dashboardPage();
const S=(name,label,group,what,extra={})=>({name,service:name,label,group,what,connected:0,broker:false,...extra});
const sources=[
 S('gmail','Gmail','mail','Your email, what comes in and what you send.',{connected:1,signin:'google'}),
 S('outlook','Outlook','mail','Your Outlook email, what comes in and what you send.',{signin:'microsoft'}),
 S('calendar','Google Calendar','calendar','Your meetings, so you go in prepared and follow up.',{connected:1,signin:'google'}),
 S('outlook_calendar','Outlook Calendar','calendar','Your Outlook meetings, so you go in prepared and follow up.',{signin:'microsoft'}),
 S('teams','Microsoft Teams','chat','Chats, meeting chats and meeting notes from Teams. Reads only.',{signin:'microsoft_teams'}),
 S('slack','Slack','chat','Your direct messages, mentions and the threads you are in.',{signin:'slack'}),
 S('telegram','Telegram chats','chat','Your Telegram chats and small groups.'),
 S('whatsapp','WhatsApp','chat','Your WhatsApp chats, as a linked device.'),
 S('google_meet','Google Meet','meetings','Meeting transcripts and Gemini notes from Google Meet.',{signin:'google_meet'}),
 S('zoom','Zoom','meetings','Meeting summaries and transcripts from Zoom.',{signin:'zoom'}),
 S('docs','Microsoft OneDrive','docs','Word files: comments, shares, and new docs or edits you approve.',{signin:'microsoft_docs'}),
 S('rss','RSS feed','other','Posts from the feeds you follow.')];
// a few connected cards, so the Connections tabs (Email, Calendar, Chat, ...) show as they do on a real Machine
const now=new Date().toISOString();
const CARD=(id,service,group,display_name)=>({id,service,group,display_name,email:'me@'+id+'.example',transport:'broker',boundary:'personal',events:3,recent_events:1,last_success:now});
const CARDS=[CARD('gmail','gmail','mail','Gmail'),CARD('gcal','calendar','calendar','Google Calendar'),CARD('tg','telegram','chat','Telegram chats')];
const posted=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const logo=/^\/brand\/logos\/([a-z_]+\.(svg|png))$/.exec(url.pathname);  // the logos, so the shots show them
 if(logo){res.setHeader('Content-Type',logo[2]==='svg'?'image/svg+xml':'image/png');res.end(await readFile(new URL('../dashboard/logos/'+logo[1],import.meta.url)));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:CARDS,suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:null,sources,suggested:[],paired:true,pair_url:'https://app.example.org/account?tab=fleet#devices'}));return}
  if(action==='connect_signin'){posted.push(args);res.end(JSON.stringify({url:'about:blank#fixture-start',state:'started'}));return}
  if(action==='connect_signin_state'){res.end(JSON.stringify({state:'started'}));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const read=page=>page.evaluate(()=>[...document.querySelectorAll('#connect-add .connect-group')].map(g=>({head:g.querySelector('h4').textContent,
 tiles:[...g.querySelectorAll('.connect-source')].map(n=>({name:n.querySelector('b').textContent,what:n.querySelector('small.what')?.textContent||null,signin:n.dataset.connectSignin||null}))})));
const settle=page=>page.evaluate(()=>Promise.all([...document.querySelectorAll('#connect-add img')].map(i=>{i.loading='eager';return i.complete?0:new Promise(r=>{i.onload=i.onerror=r})})));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,mobile,scheme] of [[390,844,true,'light'],[390,844,true,'dark'],[1440,900,false,'light'],[1440,900,false,'dark']]){
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:scheme,locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.addInitScript(()=>{window.open=()=>({location:{}})});  // a stand-in tab: the start link would go to the control plane
  const tag=`${width}-${scheme}`;
  await page.goto(base+'/#connections=add');
  await page.locator('#connect-add .connect-group').first().waitFor();
  const groups=await read(page),tile=(h,n)=>groups.find(g=>g.head===h)?.tiles.find(x=>x.name===n);
  assert.deepEqual(groups.filter(g=>g.tiles.some(x=>/Teams/.test(x.name))).map(g=>g.head),['Chat','Meetings'],`${tag}: Teams shows under Chat and Meetings`);
  assert.deepEqual([tile('Chat','Microsoft Teams')?.signin,tile('Meetings','Teams meetings')?.signin],['teams','teams'],`${tag}: both rows are the one Teams sign-in`);
  assert.deepEqual(groups.find(g=>g.head==='Meetings').tiles.map(x=>x.name),['Google Meet','Teams meetings','Zoom']);
  // Read-only, as the calendar rows say it; no meeting notes promised: that admin step is only on a hosted Machine
  assert.deepEqual([tile('Chat','Microsoft Teams').what,tile('Meetings','Teams meetings').what],
   ['Chats and meeting chats from Teams. Read-only.','Meeting chats from Teams. Read-only.'],`${tag}: what the Teams rows bring in`);
  const tabs=await page.evaluate(()=>[...document.querySelectorAll('#health-tabs button')].map(b=>b.textContent.trim()));
  assert.ok(!tabs.some(x=>/^Sources/.test(x))&&['Email','Calendar','Chat'].every(n=>tabs.some(x=>x.startsWith(n))),`${tag}: the tabs are the groups (${tabs.join(', ')})`);
  const wide=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
  assert.ok(wide<=0,`${tag}: no sideways scroll (${wide}px)`);
  if(shots){await settle(page);await page.screenshot({path:`${shots}/add-list-${tag}.png`,fullPage:true})}
  const meetings=page.locator('#connect-add .connect-group').filter({has:page.locator('h4',{hasText:/^Meetings$/})});
  if(shots){await meetings.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/add-meetings-${tag}.png`})}
  // Teams meetings: Sign in with Microsoft, the Teams consent's own step (never pair first: this Machine is paired)
  await meetings.locator('[data-connect-signin="teams"]').click();
  await page.locator('#connect-add .connect-signin').waitFor();
  const step=await page.evaluate(()=>({title:document.querySelector('#connect-add .connect-signin h3')?.textContent,
   about:document.querySelector('#connect-add .connect-signin p.muted')?.textContent,
   go:document.querySelector('#connect-add [data-signin-go]')?.textContent,pair:!!document.querySelector('#connect-add [data-connect-pair]'),
   admin:document.querySelector('#connect-add .connect-admin a')?.getAttribute('href')||null}));
  // the admin link stays: an organization that lets only approved apps in needs it for this sign-in too (the same
  // Microsoft app, and it approves Chat.Read and the sign-in scopes this one asks: cloud tests/test_device_signin.py)
  assert.deepEqual(step,{title:'Microsoft Teams',about:'Your chats and meeting chats. Read-only.',go:'Sign in with Microsoft',pair:false,
   admin:'https://themachine.computer/m365-admin-consent/teams'},`${tag}: Sign in with Microsoft for Teams, no channels or notes promised`);
  if(shots)await page.screenshot({path:`${shots}/add-teams-signin-${tag}.png`,fullPage:!mobile});
  posted.length=0;
  await page.locator('#connect-add [data-signin-go]').click();
  await page.locator('#connect-add .connect-signin',{hasText:'in the tab that opened'}).waitFor();
  assert.deepEqual(posted,[{name:'teams'}],`${tag}: it starts the Teams sign-in through the control plane`);
  // back from Microsoft (the control plane's signed_in_page): Connected to Microsoft Teams
  await page.goto(base+'/#signed-in=microsoft_teams');
  await page.getByText('Connected to Microsoft Teams.').first().waitFor();
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('teams self-hosted dashboard ok');
