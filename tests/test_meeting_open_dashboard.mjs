import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A meeting opens in the Calendar's own details wherever it is: a row on a person's timeline, a result in Events, a
// to-do's source, a "Read" link. Those details have its Notes and Transcript (and Generate notes), never the raw
// "Original" with a lowercase "calendar" heading and a list of addresses; the invite itself is one tap away under
// Original invite. A timeline row says when the meeting has notes or a transcript. Nothing is wider than the screen.
// MEETING_OPEN_SHOT=<dir> writes the timeline and the opened meeting at 1440x900 and 390x844, light and dark.
const dashboard=await dashboardPage();
const brand={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'};
const now=new Date();now.setHours(12,0,0,0);const daysAgo=d=>new Date(now-d*864e5).toISOString();
const board={id:41,account_id:'work',title:'Board meeting Q3',start:daysAgo(1),end:new Date(Date.parse(daysAgo(1))+2*36e5).toISOString(),all_day:false,location:'HQ',rooms:['Falconheavy room'],guests:3,
 with:[{name:'Lou Marsh',email:'lou@globex.example',node_id:'email:lou@globex.example'},{name:'Bo Lane',email:'bo@globex.example'}],people:['Lou Marsh','Bo Lane'],
 url:'https://calendar.google.com/calendar/event?eid=board',shared:null,notes:{by:'machine',at:daysAgo(1),chars:80},transcript:{by:'owner',at:daysAgo(1),chars:60}};
const notes={event_id:41,title:board.title,start:board.start,end:board.end,notes:{id:7,text:'## Decisions\n\n- Hire two engineers in Q1',by:'machine',at:daysAgo(1),chars:40,next_offset:null},
 transcript:{id:8,text:'Lou: The numbers look good.\nBo: Agreed.',by:'owner',at:daysAgo(1),chars:40,next_offset:null,minutes:95},zoom:null,google_meet:null,writing:null};
const invite={kind:'calendar',from:'',to:'',cc:'',title:'Board meeting Q3',occurred_at:board.start,
 body:'Quarterly numbers and the hiring plan.\nHQ\nParticipants: owner@example.com, lou@globex.example, falconheavy_room@cloudgroup.example, bo@globex.example, bo.lane@home.example',
 clipped:false,url:'https://calendar.google.com/calendar/event?eid=board',event_id:41,attachments:[]};
const timeline=[
 {id:41,type:'event',account_id:'work',kind:'calendar.event',source:'meetings',occurred_at:daysAgo(1),title:'Board meeting Q3',preview:'With Bo Lane · HQ',notes:true,transcript:true},
 {id:42,type:'event',account_id:'work',kind:'calendar.event',source:'meetings',occurred_at:daysAgo(2),title:'Coffee',preview:'With Bo Lane'},
 {id:43,type:'event',account_id:'work',kind:'gmail.message',source:'email',occurred_at:daysAgo(3),title:'The numbers',from:'Lou Marsh',preview:'Here they are.'},
 {id:44,type:'event',account_id:'work',kind:'meeting.notes',source:'meetings',occurred_at:daysAgo(4),title:'Board meeting Q3',preview:'Decisions: hire two engineers.',meeting_id:41}];
const lou=()=>({id:'email:lou@globex.example',kind:'person',name:'Lou Marsh',strength:2,closeness:'close',last_at:daysAgo(1),signals:3,ids:['lou@globex.example'],links:[],open:{},
 recent:timeline,timeline:{next:null,sources:{meetings:3,email:1},total:4}});
const card={id:'b'.repeat(16),title:'Send the board follow-ups',body:'Made-up to-do.',status:'pending',scope:'work',created_at:daysAgo(1),event_ids:[41],source_line:'Source: meeting · Board meeting Q3',origin:'review'};
const asked=[],errors=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');asked.push(url.pathname+url.search);
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(brand[url.pathname]){res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+brand[url.pathname],import.meta.url)));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[card],promises:[],connectors:[{id:'work',email:'owner@example.com',service:'calendar',status:'ok'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]}}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')?lou():{projects:[],people:[lou()],quiet:[],new:[],orgs:[]}));return}
 if(url.pathname==='/api/graph/timeline'){res.end(JSON.stringify({items:timeline,next:null,sources:{meetings:3,email:1},total:4}));return}
 // Coffee (42) can't be read as a meeting: its invite opens instead
 if(url.pathname==='/api/meeting'){const id=Number(url.searchParams.get('event'));res.end(JSON.stringify({meeting:id===41?board:null}));return}
 if(url.pathname==='/api/meeting-notes'){res.end(JSON.stringify(notes));return}
 if(url.pathname==='/api/originals'){const ev=url.searchParams.get('event');
  res.end(JSON.stringify({originals:url.searchParams.get('id')?[invite]:ev==='42'?[{...invite,title:'Coffee',event_id:42,body:'Participants: owner@example.com, bo@globex.example'}]:ev==='43'?[{kind:'email',from:'Lou Marsh',title:'The numbers',occurred_at:daysAgo(3),body:'Here they are.',event_id:43,attachments:[]}]:[invite]}));return}
 if(url.pathname==='/api/events'){res.end(JSON.stringify([{id:41,account_id:'work',kind:'calendar.event',occurred_at:daysAgo(1),title:'Board meeting Q3',body:invite.body,metadata:{source_url:invite.url}}]));return}
 if(url.pathname==='/api/calendar'){res.end(JSON.stringify({meetings:[],calendars:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
let browser;
const open=async(width,height,scheme='dark')=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',colorScheme:scheme});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.clock.install({time:now});await page.goto(base+'#graph/'+encodeURIComponent('email:lou@globex.example'));await page.locator('.graph-timeline').waitFor();return {context,page}};
const meetingShown=async page=>{await page.locator('#cal-view[open]').waitFor();await page.waitForFunction(()=>calNote?.data);await page.waitForTimeout(150)};
const fits=page=>page.evaluate(()=>{const d=document.querySelector('#cal-view');return {dialog:d.scrollWidth<=d.clientWidth+1,page:document.documentElement.scrollWidth<=innerWidth}}).then(f=>assert.deepEqual(f,{dialog:true,page:true}));
const close=page=>page.evaluate(()=>{for(const d of document.querySelectorAll('dialog[open]'))d.close()});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 {const {context,page}=await open(1440,900);
  // The row says the meeting has notes and a transcript; one without says nothing
  const row=page.locator('.graph-event[data-event="41"]');
  assert.deepEqual(await row.locator('.ge-mark').allTextContents(),['Notes','Transcript']);
  assert.equal(await page.locator('.graph-event[data-event="42"] .ge-mark').count(),0);
  assert.equal(await page.locator('.graph-event[data-event="43"]').getAttribute('data-meeting'),null);
  // A tap on it: the meeting's details with its notes and transcript, not the raw original
  await row.click();await meetingShown(page);
  assert.equal(await page.locator('#email-dialog').evaluate(d=>d.open),false);
  assert.equal(await page.locator('#cal-v-title').textContent(),'Board meeting Q3');
  assert.match(await page.locator('#cal-v-notes-body').textContent(),/Hire two engineers/);
  assert.equal(await page.locator('#cal-v-tr-h').textContent(),'Transcript · 1h 35m');
  // With: names, the room under Where, no addresses as people
  const rows=await page.locator('#cal-v-rows').textContent();
  assert.match(rows,/Lou Marsh/);assert.match(rows,/Falconheavy room/);assert.doesNotMatch(rows,/falconheavy_room@/);
  await fits(page);
  // The invite itself is one tap away: a readable heading, its description, no raw list of addresses
  await page.locator('#cal-v-orig').click();await page.locator('#email-dialog[open] .email-text').waitFor();
  const heading=await page.locator('#email-content .email-from strong').textContent();
  assert.equal(heading,'Meeting invite');assert.notEqual(heading,'calendar');
  const text=await page.locator('#email-content').textContent();
  assert.match(text,/Quarterly numbers and the hiring plan/);assert.doesNotMatch(text,/Participants:|falconheavy_room@/);
  assert.equal(await page.locator('#email-content .email-open a').textContent(),'Open in Google Calendar ↗');
  assert.equal(await page.locator('#email-content [data-open-meeting]').count(),0);  // no way round in a circle
  await close(page);
  // A meeting that can't be read as one: its invite, still with a readable heading
  await page.locator('.graph-event[data-event="42"]').click();await page.locator('#email-dialog[open] .email-from').waitFor();
  assert.equal(await page.locator('#cal-view').evaluate(d=>d.open),false);
  assert.equal(await page.locator('#email-content .email-from strong').textContent(),'Meeting invite');
  assert.equal(await page.locator('#email-content .email-text').count(),0);assert.match(await page.locator('#email-content').textContent(),/No description\./);
  await close(page);
  // Email still opens in the reader
  await page.locator('.graph-event[data-event="43"]').click();await page.locator('#email-dialog[open] .email-text').waitFor();
  assert.equal(await page.locator('#cal-view').evaluate(d=>d.open),false);await close(page);
  // The meeting's notes on their own row: the meeting
  await page.locator('.graph-event[data-event="44"]').click();await meetingShown(page);
  assert.equal(await page.locator('#cal-v-title').textContent(),'Board meeting Q3');await close(page);
  // A "Read" link that only knows the signal's id: the meeting too
  await page.evaluate(()=>openEvent('41',''));await meetingShown(page);
  assert.equal(await page.locator('#email-dialog').evaluate(d=>d.open),false);await close(page);
  // A to-do whose source is the meeting: the meeting
  await page.evaluate(id=>openEmail(id),card.id);await meetingShown(page);
  assert.equal(await page.locator('#email-dialog').evaluate(d=>d.open),false);await close(page);
  // Events: a meeting found there opens the same way
  await page.evaluate(()=>showTab('events'));await page.locator('#results article[data-event="41"]').waitFor();
  assert.notEqual(await page.locator('#results article[data-event="41"]').getAttribute('data-meeting'),null);
  await page.locator('#results article[data-event="41"] h3').click();await meetingShown(page);await close(page);
  await context.close()}
 const dir=process.env.MEETING_OPEN_SHOT;
 if(dir)for(const scheme of ['light','dark'])for(const [w,h] of [[1440,900],[1440,700],[390,844]]){const {context,page}=await open(w,h,scheme);
  await page.locator('.graph-event[data-event="41"]').scrollIntoViewIfNeeded();
  await page.screenshot({path:`${dir}/timeline-${w}x${h}-${scheme}.png`});
  await page.locator('.graph-event[data-event="41"]').click();await meetingShown(page);await fits(page);
  await page.screenshot({path:`${dir}/meeting-${w}x${h}-${scheme}.png`});
  await page.locator('#cal-v-orig').click();await page.locator('#email-dialog[open] .email-text').waitFor();await page.waitForTimeout(100);
  await page.screenshot({path:`${dir}/invite-${w}x${h}-${scheme}.png`});await context.close()}
 assert.deepEqual(errors,[]);
 console.log('meeting open dashboard ok');
}finally{await browser?.close();server.close()}
