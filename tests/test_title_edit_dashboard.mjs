import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Editing a to-do's title: the field that opens over it wraps and grows, so the whole title reads while it is edited. On
// the card it has the title's own lines, size and place (phone, computer, right to left, dark) and nothing on the card
// moves; in the chat's header and the sidebar, where a long title is cut to one line, the field shows it whole. A title
// stays one paragraph: Enter saves, a pasted line break is a space. Invented fixture data, no network beyond this server.
const dashboard=await dashboardPage();
const id=n=>(n+'').padStart(2,'0').repeat(8),now=new Date().toISOString();
const LONG='Send the warehouse KPI pre-read for Robin before the planning call';
const base0=()=>[{id:id(1),title:LONG,body:'Robin asked on Monday.',status:'pending',scope:'work',created_at:now,event_ids:[1]},
 {id:id(2),title:'Book the dentist',body:'',status:'pending',scope:'personal',created_at:now,event_ids:[2]}];
let cards=base0(),renamed=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const path=new URL(req.url,'http://fixture.invalid').pathname;res.setHeader('Content-Type','application/json');
 if(path==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(path==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(path==='/api/action'){const r=JSON.parse(body);if(r.action==='card_rename'){renamed.push(r.args.title);const c=cards.find(x=>x.id===r.args.suggestion_id);c.title=r.args.title}
  res.end(JSON.stringify(r.action==='card_chat'?{session:true,status:'ok',active:false,cursor:'k1',items:[]}:{}));return}
 res.statusCode=path.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const FIELD='.rename-box textarea, .rename-box input';
// The lines of a title as they break on screen, and where they are; the card's other parts, to see nothing moves
const shown=(page,sel)=>page.evaluate(sel=>{const el=document.querySelector(sel),w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),lines=[];let n;
 while(n=w.nextNode())for(let i=0;i<n.data.length;i++){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+1);const b=r.getBoundingClientRect();if(!b.width&&!b.height)continue;
  const last=lines.at(-1);if(last&&Math.abs(last.y-b.y)<4){last.text+=n.data[i];last.left=Math.min(last.left,b.left);last.right=Math.max(last.right,b.right)}else lines.push({text:n.data[i],y:b.y,h:b.height,left:b.left,right:b.right})}
 return lines.map(l=>({...l,text:l.text.trim()}))},sel);
// The field's own lines, read from a twin of it: the same box and type, its text as plain text
const field=page=>page.evaluate(FIELD=>{const i=document.querySelector(FIELD),c=getComputedStyle(i),r=i.getBoundingClientRect(),d=document.createElement('div');
 for(const k of ['direction','textAlign','fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','wordBreak','padding','borderWidth','boxSizing'])d.style[k]=c[k];
 Object.assign(d.style,{position:'fixed',left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px',whiteSpace:i.matches('input')?'pre':'pre-wrap',overflowWrap:'break-word',overflow:'hidden',borderStyle:'solid',zIndex:99});
 d.id='twin';d.textContent=i.value;document.body.append(d);return {tag:i.tagName,name:i.getAttribute('aria-label'),dir:c.direction,bg:c.backgroundColor,size:c.fontSize,left:r.left,right:r.right,top:r.top,bottom:r.bottom,cut:i.scrollWidth>i.clientWidth+1||i.scrollHeight>i.clientHeight+1,sel:[i.selectionStart,i.selectionEnd],value:i.value}},FIELD);
const twin=async page=>{const l=await shown(page,'#twin');await page.evaluate(()=>document.querySelector('#twin').remove());return l};
const places=page=>page.evaluate(n=>[...document.querySelectorAll(`#task-${n} :is(h3,.meta,.body,.actions,.card-foot),#task-${n}`)].map(x=>{const r=x.getBoundingClientRect();return [r.left,r.top,r.width,r.height].map(Math.round).join()}),id(1));
const shot=async(page,what)=>{if(process.env.SHOT_DIR)await page.screenshot({path:`${process.env.SHOT_DIR}/${what}.png`})};
const gone=page=>page.locator('.rename-box').waitFor({state:'detached'});
const saved=async(title,what)=>{for(let i=0;i<60&&renamed.at(-1)!==title;i++)await new Promise(r=>setTimeout(r,50));assert.equal(renamed.at(-1),title,what)};
const near=(a,b,by,what)=>assert.ok(Math.abs(a-b)<=by,`${what}: ${a} is not ${b}`);
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const errors=[];
const open=async(width,height,colorScheme,dir)=>{cards=base0();renamed=[];const mobile=width<600;
 const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme,locale:'en-US'});
 await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);await page.locator('#task-'+id(1)).waitFor();await page.evaluate(()=>document.fonts.ready);
 if(dir)await page.evaluate(dir=>{document.documentElement.dir=dir},dir);
 return {context,page}};
// A tap counts once the page has stopped scrolling
const tap=async(page,sel)=>{await page.waitForFunction(()=>Date.now()-chatScrolledAt>300);const l=page.locator(sel);await (page.viewportSize().width<600?l.tap():l.click());await page.locator(FIELD).waitFor()};
const TITLE='#task-'+id(1)+' h3 .title-link';
try{
 for(const [width,height,theme,dir] of [[390,844,'light'],[390,844,'dark'],[390,844,'light','rtl'],[1440,900,'light'],[1440,900,'dark'],[1440,900,'light','rtl']]){
  const {context,page}=await open(width,height,theme,dir),at=`${width} ${theme} ${dir||'ltr'}`,name=`${width}-${theme}${dir?'-'+dir:''}`;
  await page.locator(TITLE).scrollIntoViewIfNeeded();await shot(page,`card-${name}-0-title`);
  const was=await places(page),title=await shown(page,TITLE);
  await tap(page,TITLE);await shot(page,`card-${name}-1-editing`);
  const f=await field(page),lines=await twin(page);
  assert.equal(f.name,'To-do title',at);assert.deepEqual(f.sel,[0,LONG.length],at+': all of it selected, as ever');
  assert.equal(f.cut,false,at+': nothing of the title is cut off');
  assert.equal(f.size,await page.locator(TITLE).evaluate(x=>getComputedStyle(x).fontSize),at);
  assert.equal(f.dir,dir||'ltr',at);
  assert.deepEqual(lines.map(l=>l.text),title.map(l=>l.text),at+': the same lines as the title');
  if(width===390)assert.ok(title.length>1,'the title takes more than one line here');
  for(const [n,l] of lines.entries())for(const k of ['y',dir?'right':'left'])near(l[k],title[n][k],.6,`${at}: line ${n+1} ${k}`);
  assert.deepEqual(await places(page),was,at+': nothing on the card moves');
  assert.ok(f.left>=0&&f.right<=width&&f.top<title[0].y&&f.bottom>title.at(-1).y+title.at(-1).h-2,at+': it covers the title and stays on the screen');
  // It grows with what is typed and never gets smaller than the title it covers
  await page.keyboard.press('End');await page.keyboard.type(', and ask about the new loading dock and the two extra shifts for next week so it is all in one place');
  const g=await field(page);await page.evaluate(()=>document.querySelector('#twin').remove());await shot(page,`card-${name}-2-longer`);
  assert.equal(g.cut,false,at+': longer, still all of it');assert.ok(g.bottom>f.bottom,at+': grown');near(g.top,f.top,1,at+': grown down');assert.deepEqual(await places(page),was,at+': nothing moves while it grows');
  await page.locator(FIELD).fill('x');const x=await field(page);await page.evaluate(()=>document.querySelector('#twin').remove());
  assert.ok(x.bottom>title.at(-1).y+title.at(-1).h-2,at+': short, still over the whole old title');
  // Escape cancels
  await page.keyboard.press('Escape');await gone(page);assert.deepEqual(renamed,[],at);assert.deepEqual(await shown(page,TITLE).then(l=>l.map(x=>x.text)),title.map(l=>l.text));
  // A pasted line break is a space, the caret stays where it was, and Enter saves one line
  await tap(page,TITLE);await page.locator(FIELD).fill('Call Robin');await page.evaluate(FIELD=>{const i=document.querySelector(FIELD);i.setSelectionRange(5,5)},FIELD);
  await page.evaluate(()=>document.execCommand('insertText',false,'back\nand\r\nask '));
  const p=await field(page);await page.evaluate(()=>document.querySelector('#twin').remove());
  assert.deepEqual([p.value,p.sel],['Call back and ask Robin',[18,18]],at);
  await page.keyboard.press('Enter');await gone(page);await saved('Call back and ask Robin',at+': Enter saves');
  // Shift+Enter saves too, and a phone keyboard that sends only its line break
  await tap(page,TITLE);await page.locator(FIELD).fill('Two');await page.keyboard.press('Shift+Enter');await gone(page);await saved('Two',at);
  await tap(page,TITLE);await page.locator(FIELD).fill('Three');await page.locator(FIELD).evaluate(i=>i.dispatchEvent(new InputEvent('beforeinput',{inputType:'insertLineBreak',bubbles:true,cancelable:true})));
  await gone(page);await saved('Three',at);
  // Leaving the field saves
  await tap(page,TITLE);await page.locator(FIELD).fill('Four');await page.locator(FIELD).evaluate(i=>i.blur());await gone(page);await saved('Four',at);
  // The list still updates under an open field, and the field stays
  await tap(page,TITLE);await page.locator(FIELD).fill('Five');assert.equal(await page.evaluate(()=>canRefresh()),true,at);
  cards[1].title='Book the dentist for May';await page.evaluate(()=>refresh());await page.waitForFunction(n=>document.querySelector(`#task-${n} h3`).textContent==='Book the dentist for May',id(2));
  assert.equal(await page.locator(FIELD).inputValue(),'Five',at);await page.keyboard.press('Escape');await gone(page);
  await context.close()}
 // Where a long title is cut to one line, the field shows it whole, from the line it is on: the chat's header, the sidebar
 for(const [width,height,theme] of [[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]){
  const {context,page}=await open(width,height,theme),at=`${width} ${theme}`;
  if(width===1440)cards[0].title=LONG+' and the notes from the last two calls with the site leads, the open questions on the dock and everything left';
  await page.evaluate(()=>refresh());
  {const row=page.locator(`#side-cards a[href="#chat=${id(1)}"]`);await page.evaluate(()=>scrollTo(0,0));
   if(width===390){await page.locator('#drawer-open').tap();await row.waitFor();await page.waitForFunction(()=>!document.getAnimations().some(a=>a.playState==='running'&&a.effect?.target?.closest?.('.app-side')))}
   await row.evaluate(x=>{const r=x.getBoundingClientRect();x.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,button:2,clientX:r.left+30,clientY:r.top+8}))});await page.locator('.row-menu [data-row-rename]').click();await page.locator(FIELD).waitFor();
   const b=await row.boundingBox(),f=await field(page),lines=await twin(page),text=await shown(page,`#side-cards a[href="#chat=${id(1)}"]`);await shot(page,`sidebar-${width}-${theme}`);
   assert.equal(f.cut,false,at+': sidebar');assert.ok(lines.length>1,at+': its title is longer than the sidebar is wide');near(lines[0].y,text[0].y,.6,at+': sidebar line');near(lines[0].left,text[0].left,.6,at+': sidebar text');
   assert.ok(f.right<=b.x+b.width+2,at+': as wide as the sidebar row');await page.keyboard.press('Escape');await gone(page)}
  await page.evaluate(n=>{location.hash='chat='+n},id(1));await page.locator('.chat-title').waitFor();await page.locator('#chat-log').waitFor();
  await page.waitForFunction(()=>!document.getAnimations().some(a=>a.playState==='running'&&a.effect?.target?.closest?.('.app-side')));  // the drawer closed
  await shot(page,`chat-${width}-${theme}-0-title`);await tap(page,'.chat-title');await shot(page,`chat-${width}-${theme}-1-editing`);
  const f=await field(page),lines=await twin(page),text=await shown(page,'.chat-title');
  assert.equal(f.cut,false,at+': chat header');near(lines[0].y,text[0].y,.6,at+': chat line');near(lines[0].left,text[0].left,.6,at+': chat text');
  assert.ok(width===1440||lines.length>1,at+': longer than the header is wide');assert.ok(f.left>=0&&f.right<=width,at);
  // Turned around, the field follows the title's new width
  if(width===390){await page.setViewportSize({width:844,height:390});await page.waitForTimeout(200);const t=await field(page);await page.evaluate(()=>document.querySelector('#twin').remove());assert.equal(t.cut,false,at+': turned');assert.ok(t.right-t.left>f.right-f.left,at+': turned, wider')}
  await page.keyboard.press('Escape');await gone(page);await context.close()}
 assert.deepEqual(errors,[]);
 console.log('title edit: the field wraps over the title, on the card, in the chat and in the sidebar');
}finally{await browser.close();server.close()}
