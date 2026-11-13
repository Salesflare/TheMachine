import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The last check of new messages above the to-dos (dashboard/todos-mail-check.js, state.mail_check, made by check_now.mail_check):
// "Checked 12 messages at 16:11 · nothing needs you", a to-do held until later, and on a tap one row per thread with
// who, the subject and its to-do or the review's reason. Every source the check read counts, in one total no longer
// than the email-only line was (one line on a phone in every language); each row has its source's icon and opens its
// message in the viewer.
// Made-up names; nothing is sent.
const dashboard=await dashboardPage();
const NOW=Date.parse('2026-11-09T16:20:00Z'),at=m=>new Date(NOW+m*6e4).toISOString();
const em=(from,subject,event,rest)=>({from,subject,source:'email',kind:'gmail.message',event,...rest});
const quiet={at:at(-9),read:12,counts:{email:12},todos:0,held:0,held_until:null,more:0,threads:[
 em('Robin Vale','Re: Trial seats',11,{why:'Only cc’d, Robin is answering'}),
 em('Yara Oak','Re: Coffee next week',12,{why:'Coffee already set for Thursday 10:00'}),
 em('Fieldnote Weekly','This week in tools',13),
 em('Lee Ash','Invoice question',14,{later:true})]};
const mixed={...quiet,read:13,counts:{email:9,chat:4},threads:[
 {from:'Noor Pell',subject:'Did anyone finish chapter 4?',source:'chat',kind:'whatsapp.message',event:21,why:'Group chat chatter, nothing asked of you'},
 {from:'Rae Fenn',subject:'Lunch moved to 13:00',source:'chat',kind:'slack.message',event:22,why:'Team lunch moved, nothing to do'},
 em('Yara Oak','Re: Coffee next week',12,{why:'Coffee already set for Thursday 10:00',account:'work-outlook'}),
 {from:'',subject:'',source:'chat',kind:'telegram.message',event:23}]};
const many={...mixed,read:15,counts:{email:9,chat:4,notification:2},threads:[...mixed.threads,
 {from:'Medium',subject:'Your daily read',source:'notification',kind:'android.notification',event:32,app:'com.medium.reader',why:'A reading list, nothing to do'},
 {from:'Parcels',subject:'Parcel: Delivered to your door',source:'notification',kind:'android.notification',event:31,app:'com.example.parcels',why:'A delivery notice, the parcel is in'}]};
const busy={...quiet,todos:2,held:1,held_until:'2026-11-10T08:30:00Z',more:3,threads:[
 em('Mila Under','Pricing for our team',15,{todo:'Send Mila annual pricing',held_until:'2026-11-10T08:30:00Z'}),
 em('Jonah Kett','API limits',16,{todo:'Answer Jonah about API limits'}),...quiet.threads]};
const opened=[];
let mail=quiet;
const state=()=>({suggestions:[{id:'a1'.repeat(8),title:'Answer Jonah about API limits',body:'',status:'prepared',scope:'work',created_at:at(-10),event_ids:[1]}],
 promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{last_completed:at(-9)},review_runs:[],review_live:{runs:[]},connectors:[{id:'work-outlook',service:'outlook',email:'pat@example.com'}],
 check:{reviewed:at(-9),waiting:0},mail_check:mail,
 locale:{locale:'en-GB',region:'GB',language:'en',language_set:true,clock:'24',hour12:false,auto_hour12:false,date_locale:'en-GB',languages:{en:'English'},saveable:true}});
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/originals'&&url.searchParams.get('event')){const id=url.searchParams.get('event');opened.push(id);
  res.end(JSON.stringify({originals:[{id:+id,kind:'whatsapp',title:'Book club',body:'Did anyone finish chapter 4?',from:'Noor Pell',occurred_at:at(-30),metadata:{chat_name:'Book club',sender_display:'Noor Pell'}}]}));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},locale:'en-GB',timezoneId:'UTC'});
 await context.clock.setFixedTime(NOW);
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port+'/');
 const line=page.locator('#suggestions .mail-check .mc-line');await line.waitFor();
 assert.equal((await line.innerText()).trim(),'Checked 12 messages at 16:11 · nothing needs you');
 assert.equal(await line.getAttribute('aria-expanded'),'false');
 assert.equal(await page.locator('#suggestions .mc-list').count(),0,'folded until tapped');
 // A tap: one row per thread, its reason or nothing when the check gave none worth showing
 await line.click();await page.locator('#suggestions .mc-list').waitFor();
 assert.equal(await page.locator('#suggestions .mail-check .mc-line').getAttribute('aria-expanded'),'true');
 const rows=()=>page.locator('#suggestions .mc-list li').evaluateAll(n=>n.map(li=>li.innerText.replace(/\s+/g,' ').trim()));
 assert.deepEqual(await rows(),['Robin Vale Re: Trial seats Only cc’d, Robin is answering','Yara Oak Re: Coffee next week Coffee already set for Thursday 10:00',
  'Fieldnote Weekly This week in tools','Lee Ash Invoice question Read again in the next check']);
 const box=await page.locator('#suggestions .mail-check').boundingBox();assert.ok(box.x+box.width<=390,'fits a phone');
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=390),'no sideways scroll on a phone');
 // New to-dos, one held for the morning: the line says until when, and so does its row
 mail=busy;await page.evaluate(()=>refresh());
 await page.waitForFunction(()=>/new to-do/.test(document.querySelector('#suggestions .mc-line')?.textContent||''));
 assert.equal((await page.locator('#suggestions .mc-line').innerText()).trim(),'Checked 12 messages at 16:11 · 2 new to-dos · 1 to-do held until tomorrow 08:30');
 assert.deepEqual((await rows()).slice(0,2),['Mila Under Pricing for our team Held until tomorrow 08:30 Send Mila annual pricing','Jonah Kett API limits New to-do Answer Jonah about API limits']);
 assert.equal((await rows()).at(-1),'And 3 more threads');
 // All new to-dos held: the held line alone
 mail={...busy,todos:1,more:0};await page.evaluate(()=>refresh());
 await page.waitForFunction(()=>!/new to-dos/.test(document.querySelector('#suggestions .mc-line')?.textContent||''));
 assert.equal((await page.locator('#suggestions .mc-line').innerText()).trim(),'Checked 12 messages at 16:11 · 1 to-do held until tomorrow 08:30');
 // Every source it read: one total, each row with its source's icon (the to-dos' own) and its reason
 mail=mixed;await page.evaluate(()=>refresh());
 await page.waitForFunction(()=>/13 messages/.test(document.querySelector('#suggestions .mc-line')?.textContent||''));
 assert.equal((await page.locator('#suggestions .mc-line').innerText()).trim(),'Checked 13 messages at 16:11 · nothing needs you');
 assert.deepEqual(await rows(),['Noor Pell Did anyone finish chapter 4? Group chat chatter, nothing asked of you','Rae Fenn Lunch moved to 13:00 Team lunch moved, nothing to do',
  'Yara Oak Re: Coffee next week Coffee already set for Thursday 10:00','Unknown sender']);
 // each row's source by its one-color mark (todos-logos.js), mail by the account it came in on
 const marks=()=>page.locator('#suggestions .mc-list li .mc-src .via-ico').evaluateAll(n=>n.map(i=>[...i.classList].find(c=>c!=='via-ico')));
 assert.deepEqual(await marks(),['via-whatsapp','via-slack','via-outlook','via-telegram'],'a source mark on every row');
 const mark=await page.locator('#suggestions .mc-list li .mc-src .via-ico').first().evaluate(i=>{const s=getComputedStyle(i);return [s.width,s.maskImage||s.webkitMaskImage]});
 assert.equal(mark[0],'14px');assert.match(mark[1],/brand\/logos\/mono\/whatsapp\.svg/);
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=390),'no sideways scroll on a phone with icons');
 // A tap on a row opens its message in the viewer
 await page.locator('#suggestions [data-mc-event="21"]').click();
 await page.locator('#email-dialog[open]').waitFor();
 // the dialog opens before its request reaches this server: check what was asked once the message shows
 await page.waitForFunction(()=>/chapter 4/.test(document.querySelector('#email-content')?.textContent||''));
 assert.deepEqual(opened,['21']);
 await page.keyboard.press('Escape');await page.locator('#email-dialog[open]').waitFor({state:'detached'});
 // Many sources: still one total, the detail is in the list
 mail=many;await page.evaluate(()=>refresh());
 await page.waitForFunction(()=>/15 messages/.test(document.querySelector('#suggestions .mc-line')?.textContent||''));
 assert.equal((await page.locator('#suggestions .mc-line').innerText()).trim(),'Checked 15 messages at 16:11 · nothing needs you');
 assert.equal((await rows()).at(-1),'Parcels Parcel: Delivered to your door A delivery notice, the parcel is in');
 // a phone notification by the app that posted it when it's a known brand, else the phone
 assert.deepEqual((await marks()).slice(-2),['via-medium','via-android']);
 // Never longer than the email-only line was, in any language, and one line on a phone: every catalog's
 // "Checked … messages" is no longer than its "Checked … new emails", and the whole line fits at 390
 const fill=(s,...v)=>v.reduce((o,x)=>o.replace('{}',x),s);
 const lines=[];
 for(const lang of ['en','de','es','fr','it','nl','pt-BR','zh-CN','ja','ko','ru']){
  const cat=JSON.parse(await readFile(new URL(`../i18n/${lang}.json`,import.meta.url),'utf8'));
  const now=cat['Checked {} messages at {}'],was=cat['Checked {} new emails at {}'];
  for(const form of Object.keys(was))assert.ok(now[form].length<=was[form].length,`${lang} ${form}: "${now[form]}" is longer than "${was[form]}"`);
  lines.push([lang,fill(now.other,13,'08:41')+' · '+(typeof cat['nothing needs you']==='string'?cat['nothing needs you']:'nothing needs you')]);
 }
 const heights=await page.evaluate(lines=>{const span=document.querySelector('#suggestions .mc-line span'),b=span.closest('.mc-line'),kept=span.textContent;
  const out=lines.map(([lang,text])=>{span.textContent=text;return [lang,text,b.getBoundingClientRect().height]});span.textContent=kept;return out},lines);
 const one=heights[0][2];
 for(const [lang,text,h] of heights)assert.ok(h<=one+1,`${lang} wraps at 390: "${text}" (${h}px, one line is ${one}px)`);
 // A long check reads like an inbox and hides nothing: the first 10 rows, "Show N more" for the rest, a row's new
 // messages as "(3)" so the rows add up to the line's total, the time, and a Slack DM with no name yet as "Slack DM"
 const long={...quiet,read:16,counts:{email:12,chat:4},threads:[
  {from:'',dm:true,subject:'Will check tonight',source:'chat',kind:'slack.message',event:41,at:at(-20)},
  {from:'Noor Pell',n:3,subject:'Bringing snacks on Friday',source:'chat',kind:'whatsapp.message',event:42,at:at(-25)},
  ...Array.from({length:11},(_,i)=>em('Sender '+i,'Note '+i,50+i,{at:at(-30-i)})),
  {from:'LinkedIn',subject:'Ola Brisk sent you a message',source:'notification',kind:'android.notification',event:70,at:at(-60)}]};
 assert.equal(long.threads.reduce((n,r)=>n+(r.n||1),0),long.read,'the fixture adds up');
 mail=long;await page.evaluate(()=>refresh());
 await page.waitForFunction(()=>/16 messages/.test(document.querySelector('#suggestions .mc-line')?.textContent||''));
 assert.equal(await page.locator('#suggestions .mc-list li .mc-row').count(),10,'the first 10');
 assert.equal((await rows()).at(-1),'Show 4 more');
 assert.equal((await rows())[0],'Slack DM Will check tonight 16:00');
 assert.equal((await rows())[1],'Noor Pell (3) Bringing snacks on Friday 15:55');
 assert.ok(!(await rows()).some(r=>/\bU0[A-Z0-9]{6,}|com\.\w+\.\w+/.test(r)),'never an id or a package name');
 const whoColor=await page.evaluate(()=>{const r=document.querySelector('#suggestions .mc-row');return [getComputedStyle(r.querySelector('.mc-who b')).color,getComputedStyle(r.querySelector('.mc-what')).color]});
 assert.notEqual(whoColor[0],whoColor[1],'the words are quieter than who');
 await page.locator('#suggestions [data-mc-all]').click();
 await page.waitForFunction(()=>document.querySelectorAll('#suggestions .mc-list li .mc-row').length===14);
 assert.equal((await rows()).at(-1),'LinkedIn Ola Brisk sent you a message 15:20');
 assert.equal(await page.evaluate(()=>document.activeElement?.dataset.mcEvent),'58','focus on the first row it showed');
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=390),'no sideways scroll with times');
 // folded and opened again: the first 10 again
 await page.locator('#suggestions .mc-line').click();await page.locator('#suggestions .mc-line').click();
 assert.equal(await page.locator('#suggestions .mc-list li .mc-row').count(),10);
 // No check with new messages in the last hours: no line
 mail=null;await page.evaluate(()=>refresh());await page.locator('#suggestions .mail-check').waitFor({state:'detached'});
 // A thread's words are data: markup in them stays text
 mail={...quiet,threads:[{from:'<img src=x onerror="window.__xss=1">',subject:'<b>x</b>',why:'<img src=x onerror="window.__xss=1"> was here'}]};
 await page.evaluate(()=>refresh());await page.locator('#suggestions .mc-list li').waitFor();
 assert.equal(await page.evaluate(()=>window.__xss),undefined);
 assert.deepEqual(errors,[]);
 console.log('ok: the last check of new email says what it found and why');
}finally{await browser?.close();server.close()}
