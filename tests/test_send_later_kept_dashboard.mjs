import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Send later and what someone typed (dashboard/todos-send-later.js, dashboard/todos-kept.js) together, at 1440 and 390: a
// scheduled message is no longer kept, an edited draft as little as a new email, also when scheduling it fails after it was
// saved; the picker over it loses nothing, and closing the picker isn't closing the message. With something typed, Send now,
// Send later, Ask for changes and Discard each fit on one line: one row in English at 1440, two by two on a phone and in
// longer languages, never three and a lonely one. SHOTS=<folder>: screenshots.
const raw=await dashboardPage(),CSRF='c'.repeat(64),now=new Date().toISOString(),shots=process.env.SHOTS||'';
const page_=()=>raw.replace('__CSRF__',CSRF).replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__','a1'.repeat(16));
// The day's translations may not have these yet
const cats={};for(const [l,x] of [['de','Später senden'],['fr','Envoyer plus tard']])cats[l]=JSON.stringify({...JSON.parse(await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8')),'Send later':x});
const BRAND={'/brand/avatar.png':'app-icon-192.png','/brand/serif.woff2':'fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'fonts/inter-latin.woff2'};  // the real width of the words
const E='1'.repeat(16),T='5'.repeat(16),N='7'.repeat(16),rev=n=>n.repeat(12);
const card=(id,title,x)=>({id,title,body:'Text.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[1],...x});
const mail=(n,x)=>({kind:'email',revision:rev(n),label:'Send',from:'me@acme.example',from_options:['me@acme.example'],...x});
let cards,posts=[],fail='',lang='en';
const reset=()=>{posts=[];fail='';cards=[
 card(E,'Reply to Sam',{next_actions:[mail('a',{to:['sam@client.example'],to_name:'Sam',subject:'Plan',body:'Hi Sam,\n\nHere is the plan.\n\nAlex'})]}),
 card(T,'Ask Robin',{status:'pending',body:'Robin runs it: [robin@venue.example](mailto:robin@venue.example).'})]};
const status=()=>({suggestions:cards,promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},fleet:{on:false,fleets:[]},hours:{timezone:'UTC',morning:'09:00'},
 ...(lang==='en'?{}:{locale:{locale:lang+'-BE',region:'BE',language:lang,language_set:true,clock:'auto',hour12:false,auto_hour12:false,date_locale:lang+'-BE',languages:{en:'English',de:'Deutsch',fr:'Français'},saveable:true}})});
const server=createServer(async(req,res)=>{let b='';for await(const x of req)b+=x;const u=new URL(req.url,'http://x'),say=(x,code=200)=>{res.statusCode=code;res.end(JSON.stringify(x))};res.setHeader('Content-Type','application/json');
 if(u.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page_());return}
 const file=BRAND[u.pathname];if(file){res.setHeader('Content-Type',file.endsWith('.png')?'image/png':'font/woff2');res.end(await readFile(new URL('../brand/'+file,import.meta.url)));return}
 if(u.pathname==='/api/session')return say({csrf:CSRF,cache_scope:'a1'.repeat(16)});
 if(u.pathname==='/api/status')return say(status());
 const cat=/^\/i18n\/(\w\w)\.json$/.exec(u.pathname);if(cat){res.end(cats[cat[1]]||'{}');return}
 if(u.pathname==='/api/action'){const {action,args:a}=JSON.parse(b||'{}'),s=cards.find(x=>x.id===a?.suggestion_id);posts.push([action,a]);
  if(fail===action)return say({error:'It can’t be scheduled now.'},409);
  if(action==='compose_from')return say({from:[{account_id:'w',from:'me@acme.example',area:'Work'}],default:'me@acme.example',to_name:'Robin'});
  if(action==='compose_email'){cards.push(card(N,'Email Robin',{next_actions:[mail('7',{to:a.to?[a.to]:[],subject:a.subject,body:a.body})]}));return say({suggestion_id:N,revision:rev('7'),from_options:[]})}
  if(action==='revise_draft'){const d=s.next_actions[0];Object.assign(d,{revision:rev('f'),body:a.body,...(a.subject?{subject:a.subject}:{})});return say({revision:d.revision,body:d.body,subject:d.subject})}
  if(action==='confirm_action'&&a.later){Object.assign(s,{status:'snoozed',snoozed_until:a.later,resume_status:'prepared',send_later:{send_at:a.later,n:1,revisions:[a.revision],until:a.later}});return say({status:'scheduled',send_at:a.later})}
  if(action==='send_later_cancel'){Object.assign(s,{status:'prepared',snoozed_until:null});delete s.send_later;return say({status:'canceled'})}}
 res.statusCode=u.pathname.startsWith('/brand/')||u.pathname==='/sw.js'?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',errors=[];
const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const kept=(p,n)=>p.waitForFunction(async n=>(await localCache.read('kept'))?.value?.length===n||!n&&!(await localCache.read('kept'))?.value?.length,n,{polling:100});
const ready=p=>p.locator('#suggestions article[id]').first().waitFor();
const shut=async p=>{await p.locator('#send-dialog[open]').waitFor({state:'hidden'});await p.evaluate(()=>ktRun)};
const said=(p,text)=>p.waitForFunction(x=>document.querySelector('#toast').textContent.replace(/\s+/g,' ').includes(x),text);
const sends=()=>posts.filter(x=>/^(confirm_action|compose_email|revise_draft)$/.test(x[0]));
const smart=async p=>{await p.evaluate(x=>openSend(x,taskActions(state.suggestions.find(s=>s.id===x))[0].revision),E);await p.locator('#send-dialog[open]').waitFor()};
const type=async(p,text)=>{await p.locator('#send-rich-body').click();await p.keyboard.press('Control+End');await p.keyboard.type(text)};
const compose=async p=>{await p.goto(base+'#card='+T);await p.locator('a[href="mailto:robin@venue.example"]').first().click();await p.locator('#send-dialog[open]').waitFor();await p.fill('#send-subject','The room');await type(p,'Is the room free on Friday?')};
const pick=async p=>{await p.locator('#send-later').click();await p.locator('#snooze-dialog[open] [data-snooze]').first().waitFor()};
const later=async p=>{await pick(p);await p.locator('#snooze-dialog [data-snooze]').first().click()};
const shot=async(p,name)=>{if(shots)await p.screenshot({path:`${shots}/${name}-${p.viewportSize().width}.png`,animations:'disabled'})};
// Every button that shows: its label on one line, inside the button, the button inside the dialog and at least 44px high
const fits=async(p,labels,name,rows)=>{const got=await p.evaluate(async()=>{await document.fonts.ready;if(!document.fonts.check('600 15px Inter'))throw Error('no font');const d=document.querySelector('#send-dialog').getBoundingClientRect();
  return[...document.querySelectorAll('#send-act button')].filter(x=>x.checkVisibility()).map(x=>{const r=document.createRange();r.selectNodeContents(x);const t=r.getBoundingClientRect(),o=x.getBoundingClientRect();
   return{label:x.innerText,lines:new Set([...r.getClientRects()].map(c=>Math.round(c.top))).size,room:Math.min(t.left-o.left,o.right-t.right),top:Math.round(o.top),inside:o.left>=d.left&&o.right<=d.right&&o.bottom<=innerHeight+.5,height:o.height}})});
 assert.deepEqual(got.map(x=>x.label),labels,name);for(const x of got)assert.ok(x.lines===1&&x.room>=8&&x.inside&&x.height>=44,name+' '+JSON.stringify(x));
 if(rows)assert.deepEqual(Object.values(Object.groupBy(got,x=>x.top)).map(x=>x.length),rows,name)};
try{
 for(const [width,height] of [[1440,900],[390,844]]){reset();lang='en';
  const c=await b.newContext({viewport:{width,height},hasTouch:width<500,isMobile:width<500,locale:'en-US',timezoneId:'UTC'});await c.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
  const p=await c.newPage();p.setDefaultTimeout(15000);p.on('pageerror',e=>errors.push(width+': '+e.message));

  // A new email, typed and scheduled: not kept, no row above the to-dos, not open again after a reload
  await compose(p);await kept(p,1);await fits(p,['Send now','Send later','Discard'],'new email');await shot(p,'11-typed-new');
  // The picker over it: closing that closes only that, and the text stays as typed
  await pick(p);await p.keyboard.press('Escape');await p.locator('#snooze-dialog[open]').waitFor({state:'hidden'});
  assert.equal(await p.locator('#send-dialog[open]').count(),1);assert.match(await p.locator('#send-rich-body').innerText(),/free on Friday/);await kept(p,1);assert.deepEqual(sends(),[]);
  await later(p);await shut(p);await said(p,'Sends ');await kept(p,0);
  assert.deepEqual(sends().map(x=>x[0]),['compose_email','confirm_action']);assert.ok(sends()[1][1].later);
  assert.doesNotMatch(await p.locator('#toast').innerText(),/Kept/);
  await p.goto(base);await p.reload();await ready(p);await p.evaluate(async()=>{await ktReady;ktBack();await fetch('/api/session')});
  await p.waitForFunction(id=>state.suggestions?.find(s=>s.id===id)?.send_later,N);assert.equal(await p.locator('.kept-row,#send-dialog[open]').count(),0);

  // One kept first (Esc), brought back, then scheduled: the row goes
  reset();await compose(p);await p.keyboard.press('Escape');await shut(p);await kept(p,1);await p.goto(base);await p.locator('.kept-row',{hasText:'Unsent email to Robin'}).waitFor();
  await p.locator('.kept-row [data-kept-go]').click();await p.waitForFunction(()=>document.querySelector('#send-subject').value==='The room');
  await later(p);await shut(p);await kept(p,0);await p.locator('.kept-row').waitFor({state:'detached'});
  // It couldn't be scheduled: it waits in its to-do, and isn't an unsent email beside it
  reset();await compose(p);fail='confirm_action';await later(p);await shut(p);await said(p,'Not sent. The email waits in a to-do.');await kept(p,0);await p.locator('.kept-row').waitFor({state:'detached'});
  // It couldn't be saved: the composer stays open with what was typed, kept
  reset();await compose(p);fail='compose_email';await later(p);await p.locator('#send-error',{hasText:'It can’t be scheduled now.'}).waitFor();assert.match(await p.locator('#send-rich-body').innerText(),/free on Friday/);
  await kept(p,1);await p.locator('#send-cancel').click();await shut(p);await kept(p,0);

  // A draft, edited: the four buttons fit; scheduled, it goes out as edited and nothing is kept on it
  reset();await p.goto(base);await ready(p);await smart(p);await fits(p,['Send now','Send later','Ask for changes'],'as drafted');
  await type(p,' PS see you.');await kept(p,1);await fits(p,['Send now','Send later','Ask for changes','Discard'],'edited',width<500?[2,2]:[4]);await shot(p,'12-edited');
  await later(p);await shut(p);await said(p,'Sends ');await kept(p,0);
  assert.deepEqual(sends().map(x=>x[0]),['revise_draft','confirm_action']);assert.match(sends()[0][1].body,/PS see you/);assert.equal(sends()[1][1].revision,rev('f'));
  await p.waitForFunction(id=>state.suggestions.find(s=>s.id===id).send_later,E);  // the status that schedules it is in
  assert.equal(await p.locator('.kept-mark').count(),0,'nothing kept on a scheduled to-do');
  // Canceled: the draft is the edited one, without a mark
  await p.evaluate(id=>lazyRun('sendlater',()=>laterAct('send-cancel',id)),E);await said(p,'Canceled.');await p.waitForFunction(id=>state.suggestions.find(s=>s.id===id).status==='prepared',E);
  assert.equal(await p.locator('.kept-mark').count(),0);await smart(p);assert.match(await p.locator('#send-rich-body').innerText(),/PS see you/);assert.equal(await p.locator('#send-cancel').textContent(),'Cancel');
  // Edited, then Discard: the draft as it was, not sent
  await type(p,' More.');await kept(p,1);await p.locator('#send-cancel').click();await shut(p);await said(p,'Discarded.');await kept(p,0);
  // It can't be scheduled: the edit is saved in the draft, the message says why and stays open
  reset();await p.goto(base);await ready(p);await smart(p);await type(p,' Later.');await kept(p,1);fail='confirm_action';await later(p);
  await p.locator('#send-error',{hasText:'It can’t be scheduled now.'}).waitFor();await kept(p,0);assert.match(await p.locator('#send-rich-body').innerText(),/Later\./);await c.close();

  // The longer languages
  for(const [l,said3] of [['de',['Jetzt senden','Später senden','Änderungen anfragen','Verwerfen']],['fr',['Envoyer maintenant','Envoyer plus tard','Demander des modifications','Supprimer']]]){reset();lang=l;
   const c=await b.newContext({viewport:{width,height},hasTouch:width<500,isMobile:width<500,locale:l,timezoneId:'UTC'});await c.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
   const p=await c.newPage();p.setDefaultTimeout(15000);p.on('pageerror',e=>errors.push(width+' '+l+': '+e.message));
   await p.goto(base);await ready(p);await p.waitForFunction(l=>document.documentElement.lang===l,l);await smart(p);await p.locator('#send-later',{hasText:said3[1]}).waitFor();await shot(p,'13-drafted-'+l);await fits(p,said3.slice(0,3),l+' as drafted');
   await type(p,' PS.');await kept(p,1);await p.locator('#send-cancel',{hasText:said3[3]}).waitFor();await shot(p,'14-edited-'+l);await fits(p,said3,l+' edited',[2,2]);await c.close()}
 }
 assert.deepEqual(errors,[]);
}finally{await b.close();server.close()}
