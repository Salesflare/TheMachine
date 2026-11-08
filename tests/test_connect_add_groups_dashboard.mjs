import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add: Suggested for you on top, only for the tiles the Machine has a signal for (connect_sources'
// suggested), each with its why line and never a connected one; then every other source under its group's header, in
// the groups' order and A to Z within each, a suggested one not repeated there. No signal: no Suggested section at all.
// SHOTS=<folder> saves the list at 390 and 1440, light and dark, with and without suggestions.
const dashboard=await dashboardPage();
const S=(name,label,group,what,extra={})=>({name,service:name,label,group,what,connected:0,broker:false,...extra});
const sources=[
 S('android','Android notifications','other','The notifications on your Android phone, through the OpenClaw app.'),
 S('calendar','Google Calendar','mail','Your meetings, so you go in prepared and follow up.',{connected:1,hosted_signin:'calendar'}),
 S('crm','Salesflare CRM','customers','Accounts, contacts and deals, so it knows who matters.'),
 S('gateway','Machine health','other',"Your Machine's own log, so it spots its own trouble.",{connected:1}),
 S('gmail','Gmail','mail','Your email, what comes in and what you send.',{connected:1,hosted_signin:'gmail'}),
 S('outlook','Outlook','mail','Your Outlook email, what comes in and what you send.',{hosted_signin:'outlook'}),
 S('outlook_calendar','Outlook Calendar','mail','Your Outlook meetings, so you go in prepared and follow up.',{hosted_signin:'outlook_calendar'}),
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
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:'https://app.example.org/account',sources,suggested,codex:{status:'signed_out'}}));return}
  res.end('{}');return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const read=page=>page.evaluate(()=>[...document.querySelectorAll('#connect-add .connect-group')].map(g=>({suggested:g.classList.contains('suggested'),
 head:g.querySelector('h4').textContent,tiles:[...g.querySelectorAll('.connect-source')].map(n=>({name:n.querySelector('b').textContent.replace(' ↗',''),
 why:n.querySelector('small.why')?.textContent||null}))})));
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
   await page.locator('#connect-add .connect-group').first().waitFor();
   const groups=await read(page);
   const heads=groups.map(g=>g.head);
   if(mode==='suggested'){
    assert.ok(groups[0].suggested,`${tag}: Suggested for you comes first`);
    assert.equal(groups[0].head,'Suggested for you');
    assert.deepEqual(groups[0].tiles,[{name:'Trello',why:'Setup didn’t finish'},{name:'Stripe',why:'12 emails from Stripe in 30 days'},
     {name:'Zoom',why:'9 Zoom meetings on your calendar'},{name:'Google Docs',why:'7 messages link to Google Docs'}],`${tag}: the suggestions with their why, connected and unknown ones left out`);
   }else assert.ok(!groups.some(g=>g.suggested)&&!heads.includes('Suggested for you'),`${tag}: no signal, no Suggested section`);
   const rest=groups.filter(g=>!g.suggested);
   assert.deepEqual(rest.map(g=>g.head),['Mail and calendar','Chat','Meetings','Docs and files','Customers','Projects and code','Other'],`${tag}: the groups in order`);
   for(const g of rest){const names=g.tiles.map(x=>x.name);
    assert.deepEqual(names,[...names].sort((a,b)=>a.localeCompare(b,'en',{sensitivity:'base'})),`${tag}: ${g.head} reads A to Z`);
    assert.ok(g.tiles.every(x=>x.why===null),`${tag}: ${g.head} shows what each brings in, not a why`)}
   const all=rest.flatMap(g=>g.tiles.map(x=>x.name));
   if(mode==='suggested')for(const n of ['Trello','Stripe','Zoom','Google Docs'])assert.ok(!all.includes(n),`${tag}: ${n} is not repeated under its group`);
   else assert.deepEqual(rest.find(g=>g.head==='Meetings').tiles.map(x=>x.name),['Google Meet','Zoom']);
   assert.deepEqual(rest.find(g=>g.head==='Projects and code').tiles.map(x=>x.name),mode==='suggested'?['Codex','GitHub','Shortcut']:['Codex','GitHub','Shortcut','Trello']);
   assert.ok(rest.find(g=>g.head==='Other').tiles.some(x=>x.name==='Newthing'),`${tag}: a source without a known group is under Other`);
   // nothing wider than the screen
   const wide=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
   assert.ok(wide<=0,`${tag}: no sideways scroll (${wide}px)`);
   if(shots)await page.screenshot({path:`${shots}/${tag}.png`,fullPage:true});
   await context.close()}}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('connect add groups dashboard ok');
