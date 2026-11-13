import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A briefing before a meeting (meeting_prep.py) is a normal to-do: its title, two lines of its briefing with Show more,
// then every part with its label (Who, Last contact, Open promises, Open questions, Decide or bring). The meeting's own
// details link to it under To-do, and a tap opens its chat. Nothing is wider than the screen, at 1440 and 390, light
// and dark. MEETING_PREP_SHOT=<dir> writes the to-do and the meeting's details.
const dashboard=await dashboardPage();
const brand={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'};
const NOW=Date.parse('2026-11-09T09:00:00+01:00'),now=new Date(NOW).toISOString();
const ID='c'.repeat(16),TITLE='Prepare for the Globex pilot review';
const PARTS=[['Who:','Sam Rivera, head of operations at Globex.'],['Last contact:','Sam asked on Nov 5 whether the pilot can start in December.'],
 ['Open promises:','Promised Sam the pilot plan by Tuesday.'],['Open questions:','Who signs the order form on their side.'],
 ['Decide or bring:','The pilot plan; decide on the start date.']];
const card={id:ID,title:TITLE,body:PARTS.map(([k,v])=>`**${k}** ${v}`).join('\n\n'),status:'pending',scope:'work',created_at:now,event_ids:[41,43],
 source_line:'Source: calendar · Tue, Nov 10 (+1 more)',expires_at:'2026-11-10T09:00:00+00:00',origin:'review'};
const meeting={id:41,account_id:'work',title:'Pilot review with Globex',start:'2026-11-10T09:00:00Z',end:'2026-11-10T10:00:00Z',all_day:false,location:'https://meet.google.com/abc-defg-hij',
 guests:1,with:[{name:'Sam Rivera',email:'sam@globex.example',node_id:'email:sam@globex.example'}],people:['Sam Rivera'],shared:null,url:null};
const notes={event_id:41,title:meeting.title,start:meeting.start,end:meeting.end,notes:null,transcript:null,zoom:null,google_meet:null,writing:null};
const errors=[];
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(brand[url.pathname]){res.setHeader('Content-Type',url.pathname.endsWith('.png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+brand[url.pathname],import.meta.url)));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[card],promises:[],connectors:[{id:'work',email:'owner@example.com',service:'calendar',status:'ok'}],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/meeting'){res.end(JSON.stringify({meeting}));return}
 if(url.pathname==='/api/meeting-notes'){res.end(JSON.stringify(notes));return}
 if(url.pathname==='/api/calendar'){res.end(JSON.stringify({meetings:[meeting],calendars:[]}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.MEETING_PREP_SHOT;
const fits=page=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await context.clock.install({time:NOW});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto(base);const todo=page.locator('#task-'+ID);await todo.locator('.body').waitFor();
  assert.equal(await todo.locator('h3').innerText(),TITLE);
  // Short by default: the first lines, then Show more opens the whole briefing, each part with its label in bold
  const more=todo.locator('button.more[data-more]');assert.equal(await more.innerText(),'Show more');
  assert.ok(await todo.locator('.body.clamp').count(),'the briefing starts folded');
  await more.click();await todo.locator('.body:not(.clamp)').waitFor();
  const parts=await todo.locator('.body p').evaluateAll(ps=>ps.map(p=>[p.querySelector('strong')?.textContent||'',p.textContent.replace(/^[^:]*:\s*/,'')]));
  assert.deepEqual(parts,PARTS);
  const box=await todo.boundingBox();assert.ok(box.x>=0&&box.x+box.width<=width+1,'the to-do fits the screen');
  assert.ok(await fits(page),'no sideways scroll');
  if(shots){await todo.scrollIntoViewIfNeeded();await page.screenshot({path:`${shots}/todo-${width}-${scheme}.png`})}
  // The meeting's details link to its to-do; a tap opens that to-do's chat
  await page.evaluate(()=>openMeeting(41,''));await page.locator('#cal-view[open]').waitFor();
  const link=page.locator('#cal-v-rows [data-cal-todo]');
  assert.equal(await link.innerText(),TITLE);
  assert.equal(await link.evaluate(a=>a.closest('div').querySelector('dt').textContent),'To-do');
  assert.ok(await page.evaluate(()=>{const d=document.querySelector('#cal-view');return d.scrollWidth<=d.clientWidth+1}),'the details fit');
  if(shots){await page.waitForTimeout(150);await page.screenshot({path:`${shots}/meeting-${width}-${scheme}.png`})}
  await link.click();
  await page.waitForFunction(id=>location.hash==='#chat='+id,ID);
  assert.equal(await page.locator('#cal-view').evaluate(d=>d.open),false);
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
