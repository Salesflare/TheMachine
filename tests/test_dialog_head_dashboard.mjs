import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
import {quiet,trackRequests} from './page-calls.mjs';
const {chromium}=await import('./browser.mjs');

// A dialog that scrolls keeps its × and one line of its title on top (shell-sheets.js): at the top of the scroll the whole
// title as ever; once that has scrolled away, one smaller line with an ellipsis, over the dialog's own color. What is
// under it never moves by that, however little it scrolls. The message viewer (a long DM, its own line sticking under
// the title's), a to-do's result and New event's, on a phone, a computer and a short window.
// SHOTS=<folder> saves screenshots at the top and scrolled, in light and dark.
const dashboard=await dashboardPage(),shots=process.env.SHOTS;
const now=new Date().toISOString();
const LONG='Check the privacy documentation of the new data supplier, ask for the missing processing agreement and tell the team by Friday whether the integration can go live';
const SHORT='Call the venue';
const say=(n,from,at)=>({kind:'Slack',from,to:'',cc:'',title:'#DM Kai Moreno: line '+n,occurred_at:at,body:n%4?`Line ${n}, with https://docs.example/page-${n} to look at before we meet again`:`Line ${n}`,clipped:false,url:'https://acme.slack.example/archives/D0/p'+n,event_id:n,chat:'Kai Moreno',dm:true,view:'chat',source:'slack.message',app:'Slack',format:'markdown',attachments:[]});
const at=n=>new Date(Date.UTC(2026,10,3+Math.floor(n/12),9,n%12*3)).toISOString();
const lines=Array.from({length:41},(_,i)=>say(i+1,i%3?'Kai Moreno':'You',at(i+1)));
const cards=[['chat',LONG],['brief',SHORT],['result',LONG]].map(([id,title],i)=>({id:id.padEnd(16,'0'),title,body:'',status:id==='result'?'prepared':'pending',scope:'work',created_at:now,event_ids:[21],source_line:'Source: Slack DM from Kai Moreno',
 ...id==='result'?{result_files:[{name:'result.md',path:'result.md'}],preparation_status:'done'}:{}}));
const RESULT='# What I found\n\n'+Array.from({length:30},(_,i)=>`Paragraph ${i+1}. The supplier answers within two days, keeps its records for seven years and names every processor it uses.`).join('\n\n');
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/originals'){res.end(JSON.stringify({originals:[lines[20]],around:{event_id:21,before:lines.slice(0,20),after:lines.slice(21),earlier:null}}));return}
 if(url.pathname==='/api/result'){res.end(JSON.stringify({text:RESULT}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
// Where the title row, its × and what is under it are. body: how far the content is from where the scroll has it
const look=(page,sel)=>page.evaluate(sel=>{const d=document.querySelector(sel),h=d.querySelector('.snooze-heading'),h2=h.querySelector('h2'),x=[...h.querySelectorAll('button')].at(-1),r=e=>e.getBoundingClientRect(),
  dr=r(d),xr=r(x),tr=r(h2),first=d.querySelector('.convo-day,#result-content,.under'),chat=d.querySelector('.convo-chat'),
  hit=document.elementFromPoint(xr.left+xr.width/2,xr.top+xr.height/2),title=document.elementFromPoint(tr.left+20,r(h).bottom-17);
 return {phone:innerWidth<=560,top:d.scrollTop,height:d.scrollHeight,room:d.scrollHeight-d.clientHeight,sideways:d.scrollWidth-d.clientWidth,line:d.hasAttribute('data-line'),
  head:r(h).bottom-dr.top,x:{top:xr.top-dr.top,bottom:xr.bottom-dr.top,right:dr.right-xr.right,hit:hit===x},title:{height:tr.height,size:parseFloat(getComputedStyle(h2).fontSize),hit:title===h2,cut:h2.scrollWidth>h2.clientWidth,text:h2.textContent,right:tr.right,x:xr.left},
  body:first?r(first).top-dr.top+d.scrollTop:null,chat:chat?{top:r(chat).top-dr.top,bottom:r(chat).bottom-dr.top}:null,headings:d.textContent.split(h2.textContent).length-1}},sel);
const scrollTo=async(page,sel,y)=>{await page.evaluate(([sel,y])=>new Promise(done=>{const d=document.querySelector(sel);d.scrollTop=y;requestAnimationFrame(()=>requestAnimationFrame(done))}),[sel,y]);return look(page,sel)};
async function check(page,sel,{name,title,shot}){
 const rest=await scrollTo(page,sel,0);
 assert.equal(rest.line,false,name+': at the top the title is whole');assert.ok(rest.room>400,name+': it scrolls '+rest.room);
 assert.equal(rest.title.cut,false);assert.ok(rest.x.hit,name+': × at the top');
 await shot(name+'-top');
 // scrolled by little and by much: nothing under the title moves but by the scroll, and × can be clicked all the way
 for(const y of [1,2,4,8,15,25,40,55,70,90,120,200,400,399,120,90,70,40,25,8,1,0]){
  const m=await scrollTo(page,sel,y);
  assert.equal(m.top,y);assert.equal(m.height,rest.height,`${name}: as tall at ${y}`);
  assert.ok(Math.abs(m.body-rest.body)<1,`${name}: what is under the title stays put at ${y}: ${m.body} was ${rest.body}`);
  assert.ok(m.x.hit&&m.x.top>=0,`${name}: × can be clicked at ${y}`);assert.ok(Math.abs(m.x.right-rest.x.right)<1);
 }
 const back=await look(page,sel);assert.deepEqual([back.line,back.title.size,back.title.height,back.head],[false,rest.title.size,rest.title.height,rest.head],name+': at the top again as it was');
 const m=await scrollTo(page,sel,300);
 assert.equal(m.line,true);assert.equal(m.title.text,title);assert.equal(m.headings,1,name+': the title is there once');
 assert.ok(m.title.hit,name+': the title is in view');assert.ok(m.title.height<=36&&m.title.size<rest.title.size,JSON.stringify(m.title));
 assert.equal(m.title.cut,title===LONG);assert.ok(m.title.right<=m.title.x+1,'the title ends before ×');
 assert.ok(m.head<=70,`${name}: one line of room on top, ${m.head}`);assert.equal(m.sideways,0,name+': no sideways scroll');
 const under=m.head+(m.phone?0:8);  // the title row's color goes 8px on under it
 if(m.chat)assert.ok(Math.abs(m.chat.top-under)<=1&&m.chat.top<=under,`${name}: the conversation's line is right under the title's, no gap that shows the text: ${m.chat.top} ${under}`);
 await shot(name+'-scrolled');
 return m}
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const sizes=shots?[[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark'],[1440,500,'dark']]:[[390,844,'dark'],[1440,900,'light'],[1440,500,'dark']];
 for(const [width,height,scheme] of sizes){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:'en-US',timezoneId:'Europe/Brussels',reducedMotion:'reduce'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();trackRequests(page);page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.locator('#task-'+cards[0].id).waitFor();
  const shot=async name=>{if(shots)await page.screenshot({path:`${shots}/${name}-${width}x${height}-${scheme}.png`})};
  const viewer=async c=>{await page.evaluate(id=>openEmail(id),c.id);await page.locator('#email-content .convo-say').first().waitFor()};
  // the message viewer: opens on the to-do's own message, so already scrolled
  await viewer(cards[0]);await page.waitForFunction(()=>document.querySelector('#email-dialog').scrollTop>200);await quiet(page);
  const main=await page.evaluate(()=>[document.querySelector('.convo-main').getBoundingClientRect().top,document.querySelector('.convo-chat').getBoundingClientRect().bottom]);
  assert.ok(main[0]>=main[1],'the to-do\'s message is not under the title');
  await check(page,'#email-dialog',{name:'viewer',title:LONG,shot});
  // a link reached with the keyboard isn't left behind the title and the conversation's line
  await page.locator('#email-content a').nth(14).focus();
  for(let i=0;i<9;i++){await page.keyboard.press('Shift+Tab');await quiet(page,undefined,{frames:3});
   const f=await page.evaluate(()=>{const a=document.activeElement,r=a.getBoundingClientRect();return {tag:a.tagName,top:r.top,under:document.querySelector('.convo-chat').getBoundingClientRect().bottom}});
   assert.ok(f.tag!=='A'||f.top>=f.under-1,'focused, behind the title: '+JSON.stringify(f))}
  // × closes it from there, and the next one opens with its own title whole
  await scrollTo(page,'#email-dialog',300);await page.locator('#email-dialog .snooze-heading button').click();
  assert.equal(await page.locator('#email-dialog').evaluate(d=>d.open),false);
  await viewer(cards[1]);await check(page,'#email-dialog',{name:'viewer-short-title',title:SHORT,shot});
  await page.keyboard.press('Escape');assert.equal(await page.locator('#email-dialog').evaluate(d=>d.open),false,'Esc closes it');
  // a result
  await page.evaluate(id=>openResult(id),cards[2].id);await page.locator('#result-dialog[open]').waitFor();
  await check(page,'#result-dialog',{name:'result',title:LONG,shot});
  // a window that changes width, scrolled: the title row is measured again
  await scrollTo(page,'#result-dialog',300);
  if(width===1440){await page.setViewportSize({width:700,height});await quiet(page);await check(page,'#result-dialog',{name:'result-narrower',title:LONG,shot:async()=>{}});await page.setViewportSize({width,height})}
  await page.evaluate(()=>document.querySelector('#result-dialog').close());
  // any other dialog with the shared title row, its own form around all of it: one that scrolls by only a few pixels
  await page.evaluate(title=>{const d=document.querySelector('#cal-dialog');d.querySelector('h2').textContent=title;
   d.querySelector('form').replaceChildren(d.querySelector('.snooze-heading'),Object.assign(document.createElement('div'),{className:'under'}));d.showModal()},LONG);
  const by=async n=>page.evaluate(n=>{const d=document.querySelector('#cal-dialog'),u=d.querySelector('.under');u.style.height='';u.style.height=0;u.style.height=d.clientHeight<innerHeight*.9?innerHeight-d.offsetHeight-24+n+'px':0;return d.scrollHeight-d.clientHeight},n);
  for(const n of [3,10,30,60]){const room=await by(n);if(width>560)assert.ok(room>0,'it scrolls by '+room);
   const rest=await scrollTo(page,'#cal-dialog',0);
   for(let y=0;y<=rest.room;y+=3){const m=await scrollTo(page,'#cal-dialog',y);assert.equal(m.height,rest.height);assert.ok(Math.abs(m.body-rest.body)<1,`by ${room}, at ${y}`);assert.ok(m.x.hit,`by ${room}, at ${y}: ×`)}}
  await page.evaluate(()=>document.querySelector('#cal-dialog').close());
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('dialog head dashboard ok');
}finally{await browser?.close();server.close()}
