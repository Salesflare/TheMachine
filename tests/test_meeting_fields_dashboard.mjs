import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A meeting's details in the Calendar show its two records apart (meeting_notes.py): Notes first and open, then its
// Transcript folded under "Transcript · 2h 03m" until Show. Each shows what was added to the meeting and the meeting
// app's, marked From Zoom or From Google Meet, both when both are there. Add, Upload, Edit and Remove change only their own field: a transcript
// saved under Transcript is sent as field transcript, and nothing is moved between the two. Nothing is wider than
// the screen. MEETING_SHOT=<dir> writes the dialog at 1440x900, 1440x700 and 390x844 in light and dark.
process.env.TZ='Europe/Brussels';
const dashboard=await dashboardPage();
const brand={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'};
const at=(days,h,m=0)=>{const d=new Date();d.setDate(d.getDate()+days);d.setHours(h,m,0,0);return d};
const iso=d=>d.toISOString(),now=iso(new Date());
const turns=Array.from({length:42},(_,i)=>`[${Math.floor(i*3/60)}:${String(i*3%60).padStart(2,'0')}:00] Speaker ${i%2+1}: ${i%2?'Agreed, let’s take that to the next board.':'We went through the quarter’s numbers and the hiring plan.'}`).join('\n');
const meetings=[
 {id:201,account_id:'cal',title:'Board meeting Q4',start:iso(at(0,10)),end:iso(at(0,12)),all_day:false,location:'Room 2',guests:3,
  with:[{name:'Dana Board',email:'dana@board.example'},{name:'Sam Investor',email:'sam@fund.example'}],url:'https://calendar.google.com/calendar/event?eid=board',
  notes:{by:'machine',at:now,chars:120},transcript:{by:'machine',at:now,chars:turns.length}},
 {id:202,account_id:'cal',title:'Pilot call with Northwind',start:iso(at(0,15)),end:iso(at(0,15,45)),all_day:false,location:'Zoom',guests:1,url:null},
 {id:204,account_id:'cal',title:'Quarterly planning',start:iso(at(0,13)),end:iso(at(0,15,15)),all_day:false,location:'Room 4',guests:2,url:null,transcript:{by:'owner',at:now,chars:turns.length}},
 {id:203,account_id:'cal',title:'Design review',start:iso(at(0,16)),end:iso(at(0,17)),all_day:false,location:'Google Meet',guests:2,url:null,notes:{by:'owner',at:now,chars:30}}];
const owned={
 201:{notes:{id:9,text:'## Decisions\n\n- Hire two engineers in Q1\n- Budget approved as proposed\n\n## Action items\n\n- Dana sends the updated deck by Friday\n- Sam shares the term sheet draft',by:'machine',at:now,chars:120,next_offset:null},
      transcript:{id:10,text:turns,by:'machine',at:now,chars:turns.length,next_offset:null,minutes:123},
      zoom:{notes:{id:11,title:'Board meeting Q4',text:'**Summary**\n\nThe board reviewed Q3 results and approved the hiring plan.',chars:70,next_offset:null},transcript:null,url:'https://us02web.zoom.us/doc/board'}},
 203:{notes:{id:30,text:'Ask Robin for the final mockups.',by:'owner',at:now,chars:32,next_offset:null},transcript:null,zoom:null,
      google_meet:{notes:{id:31,title:'Meeting notes',text:'### Summary\n\nThe team picked the second layout and moves the launch to next week.',chars:80,next_offset:null,url:'https://docs.google.com/document/d/notes-doc/edit'},
       transcript:{id:32,title:'Meeting transcript',text:'Robin: The second layout reads better.\nAlex: Agreed, let’s move the launch.',chars:75,next_offset:null,minutes:52,truncated:false,url:'https://docs.google.com/document/d/tr-doc/edit'},url:'https://docs.google.com/document/d/notes-doc/edit'}},
 204:{notes:null,transcript:{id:40,text:turns,by:'owner',at:now,chars:turns.length,next_offset:null,minutes:135},zoom:null,google_meet:null,writing:null},
 202:{notes:null,transcript:null,zoom:{notes:{id:12,title:'Pilot call',text:'Northwind starts the pilot on Monday.',chars:36,next_offset:null},transcript:{id:13,title:'Pilot call',text:'Robin: We can start Monday.\nOwner: Great, I’ll send the plan.',chars:60,next_offset:null,minutes:44,truncated:false},url:null}}};
let posts=[];const notes201={...owned[201].notes};
const state=()=>({suggestions:[{id:'a'.repeat(16),title:'Prep the board follow-ups',body:'Made-up card.',status:'pending',scope:'work',created_at:now,event_ids:[]}],promises:[],connectors:[{id:'cal',email:'owner@example.com',service:'calendar',status:'ok'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(brand[url.pathname]){res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+brand[url.pathname],import.meta.url)));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/calendar'){res.end(JSON.stringify({meetings}));return}
 if(url.pathname==='/api/meeting-notes'){const id=Number(url.searchParams.get('event'));const m=meetings.find(x=>x.id===id);res.end(JSON.stringify({event_id:id,title:m.title,start:m.start,end:m.end,...owned[id]}));return}
 if(url.pathname==='/api/action'){const r=JSON.parse(body||'{}');if(r.action==='meeting_notes'){posts.push({...r.args,upload:req.headers['x-upload']});
   const a=r.args,o=owned[a.event_id],key=a.field==='transcript'?'transcript':'notes';
   o[key]=a.remove?null:{id:20,text:a.text,by:'owner',at:now,chars:a.text.length,next_offset:null,...(key==='transcript'?{minutes:2}:{})};res.end(JSON.stringify({event_id:a.event_id,field:key}));return}
  if(r.action==='meeting_notes_write'){posts.push({action:r.action,...r.args});const o=owned[r.args.event_id];o.writing={status:'running',done:1,total:4,until:null,error:null};
   res.end(JSON.stringify({event_id:r.args.event_id,writing:o.writing}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
const open=async(width,height,scheme='dark')=>{const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
 await page.goto(base);await page.evaluate(()=>showTab('calendar'));await page.waitForFunction(()=>calMeetings!==null&&![...calWeeks.values()].some(w=>w.loading));return {context,page}};
const view=async(page,id)=>{await page.evaluate(id=>calView(calMeetings.find(m=>m.id===id)),id);await page.waitForFunction(()=>calNote?.data);await page.waitForTimeout(100)};
const shown=(page,sel)=>page.locator(sel).isVisible();
const fits=page=>page.evaluate(()=>{const d=document.querySelector('#cal-view');return {dialog:d.scrollWidth<=d.clientWidth+1,page:document.documentElement.scrollWidth<=innerWidth}}).then(f=>assert.deepEqual(f,{dialog:true,page:true}));
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 {const {context,page}=await open(1440,900);
  // The Calendar says a meeting has notes and a transcript
  assert.match(await page.locator('#calendar-view').textContent(),/Notes · Transcript/);
  await view(page,201);
  // Notes first and open: the added notes, and Zoom's below them, marked From Zoom
  const order=await page.locator('#cal-view section').evaluateAll(s=>s.map(x=>x.id));assert.deepEqual(order,['cal-v-notes','cal-v-tr']);
  assert.ok(await shown(page,'#cal-v-notes-body'));assert.match(await page.locator('#cal-v-notes-body').textContent(),/Hire two engineers/);
  assert.match(await page.locator('#cal-v-notes-by').textContent(),/^Added by The Machine · /);
  assert.ok(await shown(page,'#cal-v-notes-zoom'));assert.equal(await page.locator('#cal-v-notes-zoom .cal-v-from').textContent(),'From Zoom');
  assert.match(await page.locator('#cal-v-notes-zoom-body').textContent(),/approved the hiring plan/);
  assert.equal(await page.locator('#cal-v-notes-zoom-open').getAttribute('href'),'https://us02web.zoom.us/doc/board');
  assert.ok(!await shown(page,'#cal-v-notes-none'));
  // The transcript folded: its length in the title, Show opens it, its lines kept as written
  assert.equal(await page.locator('#cal-v-tr-h').textContent(),'Transcript · 2h 03m');
  // Other languages write the short units: 30 min, not 30 m
  assert.deepEqual(await page.evaluate(()=>{const was=DL,out=[];for(const l of ['nl-NL','de-DE','fr-FR','es-ES','it-IT','pt-BR'])DL=l,out.push(calRunTime(30));DL='nl-NL';out.push(calRunTime(124));DL=was;return out.map(x=>x.replace(/\s/g,' '))}),
   ['30 min','30 Min.','30 min','30 min','30 min','30 min','2 uur 04 min']);
  assert.equal(await page.locator('#cal-v-tr-toggle').getAttribute('aria-expanded'),'false');
  assert.ok(!await shown(page,'#cal-v-tr-body'));assert.equal(await page.locator('#cal-v-tr-show').textContent(),'Show');
  assert.ok(!await shown(page,'#cal-v-tr-edit'));
  await fits(page);
  if(process.env.MEETING_SHOT)for(const scheme of ['dark','light']){await page.emulateMedia({colorScheme:scheme});await page.waitForTimeout(300);await page.screenshot({path:`${process.env.MEETING_SHOT}/meeting-1440x900-${scheme}-folded.png`})}
  await page.emulateMedia({colorScheme:'dark'});
  await page.locator('#cal-v-tr-toggle').click();
  assert.equal(await page.locator('#cal-v-tr-toggle').getAttribute('aria-expanded'),'true');assert.equal(await page.locator('#cal-v-tr-show').textContent(),'Hide');
  assert.ok(await shown(page,'#cal-v-tr-body'));
  assert.equal(await page.locator('#cal-v-tr-body').evaluate(b=>getComputedStyle(b).whiteSpace),'pre-wrap');
  assert.match(await page.locator('#cal-v-tr-body').textContent(),/^\[0:00:00\] Speaker 1: We went through/);
  assert.ok(await shown(page,'#cal-v-tr-more'),'a long transcript shows its start, with Show all');
  assert.ok(!await shown(page,'#cal-v-tr-zoom'),'no Zoom transcript for this meeting');
  await fits(page);
  if(process.env.MEETING_SHOT)for(const scheme of ['dark','light']){await page.emulateMedia({colorScheme:scheme});await page.waitForTimeout(300);await page.screenshot({path:`${process.env.MEETING_SHOT}/meeting-1440x900-${scheme}-open.png`})}
  // Remove the transcript (asks twice): only the transcript is sent, notes stay
  await page.locator('#cal-v-tr-remove').click();assert.equal(await page.locator('#cal-v-tr-remove').textContent(),'Remove the transcript?');
  await page.locator('#cal-v-tr-remove').click();await page.waitForFunction(()=>!calNote.data.transcript);
  assert.deepEqual(posts.at(-1),{event_id:201,field:'transcript',remove:true,upload:'meeting-notes'});
  assert.ok(await shown(page,'#cal-v-notes-body'));
  assert.equal(await page.locator('#cal-v-tr-h').textContent(),'Transcript');assert.ok(await shown(page,'#cal-v-tr-none'));
  assert.equal(await page.locator('#cal-v-tr-none').textContent(),'No transcript yet.');
  // Add one back: pasted under Transcript, it is saved as the transcript, even when it reads like notes
  await page.locator('#cal-v-tr-add').click();assert.match(await page.locator('#cal-v-tr-text').getAttribute('placeholder'),/word for word/);
  await page.locator('#cal-v-tr-text').fill('## Summary\n\n- Short call');await page.locator('#cal-v-tr-save').click();
  await page.waitForFunction(()=>calNote.data.transcript);
  assert.deepEqual(posts.at(-1),{event_id:201,field:'transcript',text:'## Summary\n\n- Short call',upload:'meeting-notes'});
  assert.equal(owned[201].notes.text.startsWith('## Decisions'),true,'notes untouched');
  // Notes are saved as notes
  await page.locator('#cal-v-notes-edit').click();await page.locator('#cal-v-notes-text').fill('[0:01] Speaker 1: hi');await page.locator('#cal-v-notes-save').click();
  await page.waitForFunction(()=>calNote.data.notes?.by==='owner');
  assert.equal(posts.at(-1).field,'notes');assert.equal(await page.locator('#cal-v-notes-by').textContent().then(t=>t.startsWith('Added by you')),true);
  await page.keyboard.press('Escape');
  // Zoom's alone: both fields show it, marked From Zoom, with Add to put the owner's own next to it
  await view(page,202);
  assert.ok(!await shown(page,'#cal-v-notes-body'));assert.ok(await shown(page,'#cal-v-notes-zoom'));assert.ok(await shown(page,'#cal-v-notes-add'));
  assert.ok(!await shown(page,'#cal-v-notes-zoom-open'));
  assert.equal(await page.locator('#cal-v-tr-h').textContent(),'Transcript · 44m');
  await page.locator('#cal-v-tr-toggle').click();assert.ok(await shown(page,'#cal-v-tr-zoom'));assert.match(await page.locator('#cal-v-tr-zoom-body').textContent(),/Robin: We can start Monday\./);
  assert.ok(await shown(page,'#cal-v-tr-add'));
  // Alone, Zoom's comes before Add; under the owner's own, after its buttons
  assert.ok(await page.evaluate(()=>!!($('#cal-v-tr-zoom').compareDocumentPosition($('#cal-v-tr-add'))&Node.DOCUMENT_POSITION_FOLLOWING)));
  await fits(page);
  if(process.env.MEETING_SHOT)await page.screenshot({path:`${process.env.MEETING_SHOT}/meeting-1440x900-zoom-only.png`});
  await page.keyboard.press('Escape');
  // Google Meet's: Gemini's notes under the owner's own notes and their buttons, the transcript in Transcript, each
  // marked From Google Meet and opening its own Google Doc
  await view(page,203);
  assert.ok(await shown(page,'#cal-v-notes-body'));assert.match(await page.locator('#cal-v-notes-body').textContent(),/final mockups/);
  assert.ok(await shown(page,'#cal-v-notes-meet'));assert.ok(!await shown(page,'#cal-v-notes-zoom'));
  assert.equal(await page.locator('#cal-v-notes-meet .cal-v-from').textContent(),'From Google Meet');
  assert.match(await page.locator('#cal-v-notes-meet-body').textContent(),/second layout/);
  assert.equal(await page.locator('#cal-v-notes-meet-open').getAttribute('href'),'https://docs.google.com/document/d/notes-doc/edit');
  assert.ok(await page.evaluate(()=>!!($('#cal-v-notes-edit').compareDocumentPosition($('#cal-v-notes-meet'))&Node.DOCUMENT_POSITION_FOLLOWING)));
  assert.equal(await page.locator('#cal-v-tr-h').textContent(),'Transcript · 52m');
  await page.locator('#cal-v-tr-toggle').click();assert.ok(await shown(page,'#cal-v-tr-meet'));assert.ok(await shown(page,'#cal-v-tr-add'));
  assert.match(await page.locator('#cal-v-tr-meet-body').textContent(),/Robin: The second layout/);
  assert.equal(await page.locator('#cal-v-tr-meet-open').getAttribute('href'),'https://docs.google.com/document/d/tr-doc/edit');
  await fits(page);
  if(process.env.MEETING_SHOT)for(const scheme of ['dark','light']){await page.emulateMedia({colorScheme:scheme});await page.waitForTimeout(300);await page.screenshot({path:`${process.env.MEETING_SHOT}/meeting-1440x900-${scheme}-meet.png`})}
  await context.close()}
 // Generate notes: only on a meeting with a transcript and no notes. It runs on The Machine: the dialog says it writes,
 // shows it again when opened later, and shows the notes when they are there, marked as The Machine's
 {const {context,page}=await open(1440,900,'light');
  for(const id of [201,202,203]){await view(page,id);assert.ok(!await shown(page,'#cal-v-notes-gen'),'no Generate notes on meeting '+id);await page.keyboard.press('Escape')}
  await view(page,204);
  assert.ok(await shown(page,'#cal-v-notes-gen'));assert.equal(await page.locator('#cal-v-notes-gen').textContent(),'Generate notes');
  assert.ok(await shown(page,'#cal-v-notes-add'));assert.ok(await shown(page,'#cal-v-notes-file'));
  assert.equal(await page.locator('#cal-v-tr-h').textContent(),'Transcript · 2h 15m');
  await fits(page);
  if(process.env.MEETING_SHOT)await page.screenshot({path:`${process.env.MEETING_SHOT}/generate-1440x900-light-ready.png`});
  await page.locator('#cal-v-notes-gen').click();
  await page.waitForFunction(()=>!$('#cal-v-notes-writing').hidden);
  assert.deepEqual(posts.at(-1),{action:'meeting_notes_write',event_id:204});
  assert.equal(await page.locator('#cal-v-notes-writing').textContent(),'Writing notes…');
  assert.ok(!await shown(page,'#cal-v-notes-gen'));assert.ok(!await shown(page,'#cal-v-notes-none'));
  if(process.env.MEETING_SHOT)await page.screenshot({path:`${process.env.MEETING_SHOT}/generate-1440x900-light-writing.png`});
  // Closed and opened again: it still says so (the service writes on)
  await page.keyboard.press('Escape');await view(page,204);
  assert.equal(await page.locator('#cal-v-notes-writing').textContent(),'Writing notes…');
  // A usage limit: it says it waits for it
  owned[204].writing={status:'waiting',done:2,total:4,until:Date.now()/1000+3600,error:null};
  await page.waitForFunction(()=>/usage limit/.test($('#cal-v-notes-writing').textContent),null,{timeout:8000});
  // Done: the notes show, marked as written by The Machine, and Generate is gone
  owned[204].writing=null;owned[204].notes={id:41,text:'## Summary\n\nThe plan for next quarter is set.\n\n## Decisions\n\n- Two hires in Q1\n\n## Action items\n\n- **Dana**: send the budget by Friday',
   by:'machine',written_from:'transcript',at:now,chars:110,next_offset:null};
  await page.waitForFunction(()=>!$('#cal-v-notes-body').hidden,null,{timeout:8000});
  assert.match(await page.locator('#cal-v-notes-by').textContent(),/^Written by The Machine · /);
  assert.match(await page.locator('#cal-v-notes-body').textContent(),/send the budget by Friday/);
  assert.ok(!await shown(page,'#cal-v-notes-gen'));assert.ok(!await shown(page,'#cal-v-notes-writing'));
  assert.match(await page.locator('#toast').textContent(),/Notes written\./);
  await fits(page);
  if(process.env.MEETING_SHOT)await page.screenshot({path:`${process.env.MEETING_SHOT}/generate-1440x900-light-done.png`});
  // It failed: it says so, and Generate notes is there again
  owned[204].notes=null;owned[204].writing={status:'failed',done:0,total:1,until:null,error:'model'};
  await page.keyboard.press('Escape');await view(page,204);
  assert.equal(await page.locator('#cal-v-notes-writing').textContent(),'Couldn’t write the notes. Try again.');assert.ok(await shown(page,'#cal-v-notes-gen'));
  owned[204].writing=null;
  await context.close()}
 for(const [w,h,scheme] of [[1440,900,'dark'],[1440,700,'dark'],[390,844,'light'],[390,844,'dark']]){const {context,page}=await open(w,h,scheme);
  owned[204].writing={status:'running',done:1,total:4,until:null,error:null};
  await view(page,204);await fits(page);
  if(process.env.MEETING_SHOT)await page.screenshot({path:`${process.env.MEETING_SHOT}/generate-${w}x${h}-${scheme}-writing.png`});
  owned[204].writing=null;await page.keyboard.press('Escape');await view(page,204);await fits(page);
  assert.ok(await shown(page,'#cal-v-notes-gen'));
  if(process.env.MEETING_SHOT)await page.screenshot({path:`${process.env.MEETING_SHOT}/generate-${w}x${h}-${scheme}-ready.png`});
  await context.close()}
 for(const [w,h] of [[1440,700],[390,844]])for(const scheme of ['dark','light']){const {context,page}=await open(w,h,scheme);
  owned[201].transcript={id:10,text:turns,by:'machine',at:now,chars:turns.length,next_offset:null,minutes:123};owned[201].notes={...notes201};
  await view(page,201);await fits(page);
  if(process.env.MEETING_SHOT&&w<600){await page.evaluate(()=>$('#cal-view').close());await view(page,203);await page.locator('#cal-v-tr-toggle').click();await fits(page);
   await page.screenshot({path:`${process.env.MEETING_SHOT}/meeting-${w}x${h}-${scheme}-meet.png`});await page.evaluate(()=>$('#cal-view').close());await view(page,201)}
  if(process.env.MEETING_SHOT){await page.screenshot({path:`${process.env.MEETING_SHOT}/meeting-${w}x${h}-${scheme}-folded.png`});
   await page.locator('#cal-v-tr-toggle').click();await page.waitForTimeout(100);await page.locator('#cal-v-tr-h').scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.MEETING_SHOT}/meeting-${w}x${h}-${scheme}-open.png`})}
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('ok meeting fields dashboard');
}finally{await browser?.close();server.close()}
