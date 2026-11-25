import assert from 'node:assert/strict';
import {waitForAction} from './page-calls.mjs';
import {mkdir,readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Mark done where it isn't in sight already (a decision, a draft, a pick): a plain button at the end of the row on a wider
// screen when its line has the room, else at the top of the … (a phone, a narrow card, long labels); one of the two at any
// width, never both, never a second primary, never a second line (todos-cards.js cardActions, actionsSize). It only tops
// the … on a run that stopped to ask, while a teammate has the to-do. The D key, its hint and the chat stay one Mark done.
// SHOTS=<folder> saves the to-dos at 390, 768, 1024 and 1440 in English and German.
const dashboard=await dashboardPage();
const LANGS=['en','de','fr','pt-BR','ru'],cats={};for(const l of LANGS)cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const now=new Date().toISOString(),posts=[];let n=0,lang='en';
const card=(id,x)=>({id,title:'Reply to Priya about the pricing',body:'Priya asked what forty seats would cost.',status:'pending',scope:'work',created_at:now,event_ids:[++n],...x});
const ready=x=>({status:'prepared',preparation_status:'done',body:'It is ready.',...x});
const mail=x=>({kind:'email',revision:'v1',label:'Send to Noor',to:['noor@example.com'],to_name:'Noor',subject:'Contract',body:'Hi Noor',...x});
const needs=(needs,x={})=>JSON.stringify({state:'needs_you',needs,...x});
const CARDS=[
 card('pend',{}),card('early',{status:'accepted',early:true,preparation_status:'queued'}),
 card('draft',ready({next_actions:[mail()]})),
 card('reply',ready({next_actions:[mail({label:'Send reply'})]})),
 card('answered',ready({body:'There are three ways to do it.',outcome:JSON.stringify({state:'answered'})})),
 card('retry',{status:'prepared',body:'It stopped.',preparation_status:'blocked',preparation_error:'timeout',preparation_reason:'The model did not answer.'}),
 card('pick',{title:'2 newsletters: keep or unsubscribe?',scope:'personal',body:'Pick Keep or Unsubscribe.',cleanup:{kind:'newsletters',items:[1,2].map(i=>({n:i,from:'Sender '+i,address:`s${i}@example.com`,title:'Issue',count:1,state:'open',plan:'one_click'}))}}),
 // in sight already, so never added
 card('result',ready({outcome:JSON.stringify({state:'done'})})),
 card('question',ready({body:'Which day?',outcome:needs('Which day works for you?')})),
 card('fix',{scope:'personal',origin:'machine',owner_step:1,machine_log:true,machine_fix:true}),
 card('reconnect',{scope:'personal',origin:'machine',owner_step:1,reconnect:{provider:'gmail',source:'gmail',account:'sam@example.com',email:'sam@example.com'}}),
 card('doc',ready({next_actions:[{kind:'doc_write',op:'create',revision:'d1',label:'Create doc',title:'Plan',url:'https://docs.google.com/document/d/abc/edit',state:{status:'sent'}}]})),
 card('second',{title:'Second-hand chairs',scope:'personal',secondhand:{blocked:'captcha',items:[]}}),
 // kept in the … on purpose
 card('stopped',{status:'prepared',body:'It stopped to ask.',preparation_status:'blocked',preparation_reason:'I need the order number. What is it?'}),
 card('theirs',{status:'accepted',handed:true,preparation_status:'handed',fleet_handoff:{stage:'asked',name:'Pat',request_id:'q1'}})];
// what each shows at 1440: its row, then whether the … has Mark done
const WIDE={pend:['Do it','Ask for changes','Snooze','Mark done'],early:null,draft:['Review and send to Noor','Ask for changes','Snooze','Mark done'],
 reply:['Review and send reply','Ask for changes','Snooze','Mark done'],answered:['Do it','Ask for changes','Snooze','Mark done'],
 retry:null,pick:['Snooze','Mark done']};
const IN_ROW=Object.keys(WIDE),IN_MENU=['stopped','theirs'];
const view=()=>({locale:'en-US',region:'US',language:lang,language_set:true,clock:'auto',hour12:false,auto_hour12:false,date_locale:lang==='en'?'en-US':lang,languages:{en:'English',de:'Deutsch',fr:'Français','pt-BR':'Português (Brasil)',ru:'Русский'},saveable:true});
const state=()=>({suggestions:CARDS,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],
 fleet:{on:true,fleets:[]},locale:view()});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/fonts/')){readFile(new URL('../'+url.pathname.slice(1),import.meta.url)).then(b=>{res.setHeader('Content-Type','font/woff2');res.end(b)},()=>{res.statusCode=404;res.end()});return}
 const cat=/^\/i18n\/(.+)\.json$/.exec(url.pathname);if(cat){res.end(cats[cat[1]]||'{}');return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});if(b.action==='decide'&&b.args.choice==='complete'){res.end(JSON.stringify({status:'completed'}));return}}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/#todos';
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const open=async(width,extra={})=>{const context=await browser.newContext({viewport:{width,height:900},locale:'en-US',...extra});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('#task-pend .actions').waitFor();await page.evaluate(()=>document.fonts.ready);
  if(lang!=='en')await page.waitForFunction(l=>document.documentElement.lang===l,lang);
  for(const s of await page.locator('#suggestions details.group:not([open])>summary').all())await s.click();  // Waiting on others
  await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(r,60)))));
  return {context,page}};
 // Per to-do: the row in sight (its names, lines, primaries), whether its … holds Mark done, how many Mark done in all
 const look=page=>page.evaluate(()=>Object.fromEntries([...document.querySelectorAll('#suggestions article.card')].map(c=>{const a=c.querySelector(':scope>.actions'),seen=x=>getComputedStyle(x).display!=='none';
  if(!a)return [c.id.slice(5),null];
  const kids=[...a.children].filter(x=>x.matches('button,a.open,.more-actions')&&seen(x)),done='[data-choice="complete"]',row=kids.filter(x=>!x.matches('.more-actions'));
  return [c.id.slice(5),{row:row.map(x=>x.textContent.trim()),mark:row.filter(x=>x.matches(done)).map(x=>x.className),menu:[...a.querySelectorAll('.more-menu>'+done)].filter(seen).length,
   menuFirst:[...a.querySelectorAll('.more-menu>button')].filter(seen)[0]?.dataset.choice,lines:new Set(kids.map(x=>Math.round(x.getBoundingClientRect().top))).size,
   primaries:a.querySelectorAll('.primary').length,inside:kids.every(x=>x.getBoundingClientRect().right<=c.getBoundingClientRect().right+.5)}]})));
 const decided=()=>waitForAction(posts,'decide');
 // Rules at every width: one Mark done in sight or in the …, never both; never a second primary; in the row it's one line
 const rules=(all,at)=>{for(const {id} of CARDS){const x=all[id];assert.ok(x,`${at}: ${id} is on the page`);const why=`${at}: ${id} ${JSON.stringify(x)}`;
  assert.equal(x.mark.length+x.menu,1,'one Mark done, '+why);assert.ok(x.primaries<=1,'one lead at most, '+why);assert.ok(x.inside,'nothing sticks out, '+why);
  if(IN_ROW.includes(id)&&x.mark.length){assert.deepEqual(x.mark,['ghost'],'a plain button, '+why);assert.equal(x.lines,1,'one line, '+why)}}};

 // 1. A computer: at the end of the row where it wasn't in sight; what was in sight or kept in the … stays so
 {const {context,page}=await open(1440);const all=await look(page);rules(all,'1440');
  for(const [id,row] of Object.entries(WIDE)){assert.ok(all[id].mark.length,`${id}: Mark done is in the row: ${JSON.stringify(all[id])}`);assert.equal(all[id].row.at(-1),'Mark done',id);
   if(row)assert.deepEqual(all[id].row,row,id)}
  for(const id of IN_MENU)assert.equal(all[id].menu,1,`${id}: Mark done only tops the …: ${JSON.stringify(all[id])}`);
  for(const {id} of CARDS)if(!IN_ROW.includes(id)&&!IN_MENU.includes(id))assert.equal(all[id].mark.length,1,`${id}: in sight as before: ${JSON.stringify(all[id])}`);
  assert.deepEqual(all.result.row,['Mark done','Ask for changes','Snooze']);
  assert.equal(all.second.row[0],'Open');assert.equal(all.fix.row[0],'Do it');
  // Its key hint sits on the button; D closes the to-do, and so does a click on it
  assert.equal(await page.locator('#task-pend .actions>[data-choice="complete"]').getAttribute('title'),'Mark done (D)');
  await page.locator('#task-pend .actions>[data-choice="complete"]').click();
  await decided();assert.deepEqual(posts.filter(p=>p.action==='decide').map(p=>[p.suggestion_id,p.choice]),[['pend','complete']]);posts.length=0;
  await context.close()}

 // 2. The chat has it once, where it was: after Snooze in the ⋯
 {const {context,page}=await open(1440);
  const acts=await page.evaluate(()=>{const p=chatParts(state.suggestions.find(s=>s.id==='pend')),t=document.createElement('template');setHTML(t,p.rest);return [...t.content.querySelectorAll('[data-choice]')].map(b=>b.dataset.choice)});
  assert.deepEqual(acts.filter(c=>['snooze','complete'].includes(c)),['snooze','complete']);
  // A snoozed and a closed to-do have none
  for(const status of ['snoozed','completed','rejected'])assert.ok(!await page.evaluate(status=>String(suggestionCard({...state.suggestions.find(s=>s.id==='pend'),status},'For you')).includes('choice="complete"'),status),status);
  await context.close()}

 // A redraw of its to-do (a poll) keeps the keyboard on it, in the row and, on a phone, in the open …
 for(const [width,sel] of [[1440,'.actions>'],[390,'.more-menu>']]){const {context,page}=await open(width);
  if(width<600)await page.locator('#task-reply .more-actions>summary').click();
  await page.locator(`#task-reply ${sel}[data-choice="complete"]`).focus();const was=CARDS.find(c=>c.id==='reply');was.title+=' again';
  await page.evaluate(()=>refresh(true));await page.locator('#task-reply h3',{hasText:was.title}).waitFor();
  assert.ok(await page.evaluate(sel=>document.activeElement===document.querySelector(`#task-reply ${sel}[data-choice="complete"]`),sel),`focus stays at ${width}`);was.title=was.title.replace(' again','');
  await context.close()}

 // The D key closes the to-do the keyboard is on, wherever its Mark done is, once
 for(const width of [1440,390]){const {context,page}=await open(width);posts.length=0;
  await page.locator('#task-draft .title-link').focus();await page.keyboard.press('d');
  await decided();assert.deepEqual(posts.filter(p=>p.action==='decide').map(p=>[p.suggestion_id,p.choice]),[['draft','complete']],`D at ${width}`);
  await context.close()}

 // 3. Every width, in English and the languages with the longest labels, up to a phone; a width change moves it
 for(const l of LANGS){lang=l;const {context,page}=await open(1440);
  for(const width of [1440,1280,1024,900,768,700,620,561,560,480,390,768,1440]){await page.setViewportSize({width,height:900});
   await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(r,60)))));
   const all=await look(page);rules(all,`${l} ${width}`);
   if(width<=560)for(const id of IN_ROW){assert.equal(all[id].menu,1,`${l} ${width}: ${id} on a phone it is in the …`);if(all[id].menuFirst!=='snooze')assert.equal(all[id].menuFirst,'complete',`${l} ${width}: ${id} at the top of the …`)}
   if(process.env.SAY)console.log(l,width,IN_ROW.map(id=>id+':'+(all[id].mark.length?'row':'menu')+'/'+all[id].lines).join(' '))}
  await context.close()}
 lang='en';

 if(shots)for(const [l,scheme,widths] of [['en','dark',[390,768,1024,1440]],['de','dark',[390,768,1024,1440]],['en','light',[1440]]]){lang=l;
  for(const width of widths){const {context,page}=await open(width,{colorScheme:scheme,...(width<500?{isMobile:true,hasTouch:true}:{})});
   for(const id of ['pend','draft','reply','pick','result'])await page.locator('#task-'+id).screenshot({path:`${shots}/${id}-${width}-${l}-${scheme}.png`});
   if(width<500||width===768){await page.locator('#task-pend .more-actions>summary').click();await page.screenshot({path:`${shots}/menu-${width}-${l}-${scheme}.png`})}
   else await page.screenshot({path:`${shots}/page-${width}-${l}-${scheme}.png`});
   await context.close()}}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('mark done in the row ok');
