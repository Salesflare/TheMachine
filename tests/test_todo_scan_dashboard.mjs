import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do reads at a glance: its title first, then one quiet line (state, who, organization, project, when) instead of a
// pile of chips; the project is a link and changing it sits in More. What matters on a second look (a coding agent's
// result, its files, your note, the source) folds behind one Details, and a done to-do is compact: its title, one line,
// what went out, and Details with Reopen on one row. An open to-do keeps its draft and its first button in sight.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const ago=h=>new Date(Date.now()-h*3600e3).toISOString();
const who=[{id:'p:robin',name:'Robin Example',org:{id:'o:acme',name:'Acme Modular Buildings Developer International'}}];
const project={node_id:'proj:listing',name:'Editorial listing exchange'};
const cards=[
 {id:'a1a1a1a1a1a1a1a1',title:'Reply to Robin about the listing',body:'Robin asks whether both listings are live. They are: the reply confirms it and shares the guide.',status:'prepared',scope:'work',created_at:ago(3),event_ids:[1],
  people:who,project_node:project,project:project.name,source_line:'Source: email from Robin Example · Wed 28 Oct (+1 more)',source_url:'https://mail.example/x',
  outcome:JSON.stringify({state:'needs_you',needs:'check the reply and send it'}),
  next_actions:[{kind:'email',revision:'e1',label:'Send reply',to:['robin@example.com'],subject:'Re: listing',body:'Hi Robin,\n\nBoth listings are live.\n\nAlex',reply:true}]},
 {id:'b1b1b1b1b1b1b1b1',title:'Sam wants a call about the renewal',body:'Sam asks for a 30-minute call next week about the renewal terms and a bigger team plan. Their contract ends on November 15, so the call should be before then.',status:'pending',scope:'personal',created_at:ago(26),event_ids:[2],
  source_line:'Source: email from Sam · Tue 27 Oct'},
 {id:'d1d1d1d1d1d1d1d1',title:'Both listings are live; reply to Robin',body:'Both listings are live. The reply to Robin shares the guide, where the listing appears before the others in the comparison table.',status:'completed',scope:'work',created_at:ago(72),closed_at:ago(2),event_ids:[3],
  people:who,project_node:project,project:project.name,source_line:'Source: email from Robin Example · Wed 28 Oct (+1 more)',source_url:'https://mail.example/x',
  latest_feedback:{choice:'other',feedback:'Then write an email to Robin.',created_at:ago(1)},
  next_actions:[{kind:'email',revision:'e2',label:'Send reply',to:['robin@example.com'],subject:'Re',body:'Hi',state:{status:'sent',sent_at:ago(0.5),message_id:'gmail:1'}}],
  agent_job:{id:'j1',name:'Codex',place:'local',status:'result',turns:2,summary:'Deployed. PR #14 is merged.\n\nThe reply is in reply.md.',files:[{path:'reply.md'},...Array.from({length:12},(_,i)=>({path:`out/f${i}.json`}))]}}];
const actions=[];
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},done_counts:{all:1,work:1,personal:0},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:[],next:null,total:1}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify({projects:[{id:'proj:listing',name:'Editorial listing exchange'},{id:'proj:other',name:'Other'}]}));return}
 if(url.pathname==='/api/action'){actions.push(JSON.parse(body||'{}'));res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1280,390]){
  const context=await browser.newContext({viewport:{width,height:900}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-a1a1a1a1a1a1a1a1').waitFor();
  await page.evaluate(()=>{const d=document.getElementById('finished-list');if(d)d.open=true});
  const open=page.locator('#task-a1a1a1a1a1a1a1a1'),pending=page.locator('#task-b1b1b1b1b1b1b1b1'),done=page.locator('#task-d1d1d1d1d1d1d1d1');
  await done.waitFor();
  // Title first, then the meta line: who, organization and project as quiet links, Work under All, when
  assert.equal(await open.evaluate(a=>a.firstElementChild.tagName),'H3');
  assert.equal(await open.evaluate(a=>a.querySelector(':scope>h3+.meta')!==null),true);
  assert.equal(await open.locator('.meta a.chip.who:not(.org)').getAttribute('href'),'#graph/'+encodeURIComponent('p:robin'));
  assert.equal(await open.locator('.meta a.chip.who.org').getAttribute('href'),'#graph/'+encodeURIComponent('o:acme'));
  assert.equal(await open.locator('.meta a.chip.project-link').getAttribute('href'),'#graph/'+encodeURIComponent('proj:listing'));
  assert.equal(await open.locator('.meta span.chip.scope').innerText(),'Work');
  assert.equal(await open.locator('.meta time').count(),1);
  // No pills: the meta items have no background, and the line is at most two rows even with a long organization on a phone
  assert.equal(await open.locator('.meta a.chip.who.org').evaluate(e=>getComputedStyle(e).backgroundColor),'rgba(0, 0, 0, 0)');
  {const [h,lh]=await open.locator('.card-badges').evaluate(e=>[e.getBoundingClientRect().height,parseFloat(getComputedStyle(e).lineHeight)]);assert.ok(h<=lh*2+4,`meta ${h}px for line ${lh}px`)}
  // The project's picker is not on the card's front: Change project is in More, and it opens the picker
  assert.equal(await open.locator('.project-pick').count(),0);
  await open.locator('.more-actions>summary').click();await open.locator('.more-menu [data-card-project]').click();
  await page.locator('.project-picker select').waitFor();assert.equal(await open.locator('.more-actions').evaluate(d=>d.open),false);
  await page.locator('.project-picker [data-pp="cancel"]').click();
  // Open and needing you: the status line, the draft and the first button stay in sight; the source folds behind Details
  assert.match(await open.locator('.status-line').innerText(),/^Needs you: check the reply/);
  assert.ok(await open.locator('.draft').isVisible());assert.ok(await open.locator('.actions button.primary').first().isVisible());
  assert.equal(await open.locator('.read-original').isVisible(),false);
  await open.locator('.card-foot [data-details]').click();assert.ok(await open.locator('.card-details .read-original').isVisible());
  assert.equal(await open.locator('.card-foot [data-details]').getAttribute('aria-expanded'),'true');
  // A long open body shows two lines and Show more
  assert.equal(await pending.locator('.body').evaluate(e=>e.classList.contains('clamp')&&getComputedStyle(e).getPropertyValue('--lines').trim()),'2');
  assert.equal(await pending.locator('span.chip.scope').innerText(),'Personal');
  // Done: compact. State as a word with a dot, one line of body, the outcome in sight; the agent result, its files, your note
  // and the source behind Details, which shares its row with Chat and Reopen
  assert.equal((await done.locator('.card-badges .chip').first().innerText()).trim(),'Done');
  assert.ok(await done.evaluate(a=>a.classList.contains('is-closed')));
  {const [h,lh]=await done.locator('.body').evaluate(e=>[e.getBoundingClientRect().height,parseFloat(getComputedStyle(e).lineHeight)]);assert.ok(h<=lh+2,`one line: ${h} for ${lh}`)}
  assert.match(await done.locator('.note.sent-ok').innerText(),/^Email sent at \d\d:\d\d\.$/);
  for(const part of ['.agent-result','.agent-files','.saved-feedback','.read-original'])assert.equal(await done.locator(part).first().isVisible(),false,part);
  {const row=await Promise.all(['.card-foot [data-details]','.card-foot a.card-chat-link','.actions button[data-choice="reopen"]'].map(s=>done.locator(s).boundingBox()));
   assert.ok(row.every(b=>b&&Math.abs((b.y+b.height/2)-(row[0].y+row[0].height/2))<12),'Details, Chat and Reopen on one row: '+JSON.stringify(row))}
  assert.ok((await done.boundingBox()).height<(await open.boundingBox()).height/2,'a done to-do is much shorter than an open one');
  await done.locator('.card-foot [data-details]').click();
  for(const part of ['.agent-result','.saved-feedback','.read-original','[data-card-project]'])assert.ok(await done.locator('.card-details '+part).first().isVisible(),part);
  {const [h,lh]=await done.locator('.body').evaluate(e=>[e.getBoundingClientRect().height,parseFloat(getComputedStyle(e).lineHeight)]);if(width<600)assert.ok(h>lh*1.5,'Details shows the whole body')}
  // Details stays open across a refresh
  await page.evaluate(()=>render());assert.ok(await done.locator('.card-details .saved-feedback').isVisible());
  // Under Work the Work word goes: the filter says it
  await page.evaluate(()=>document.querySelector('[data-scope="work"]').click());await page.waitForTimeout(200);
  assert.equal(await page.locator('#task-a1a1a1a1a1a1a1a1 span.chip.scope').count(),0);
  await page.evaluate(()=>document.querySelector('[data-scope="all"]').click());
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  // In the chat, Change project sits in its ⋯ menu; the picker opens in the chat and the menu closes
  if(width>600){await page.goto('http://127.0.0.1:'+server.address().port+'/#chat=a1a1a1a1a1a1a1a1');await page.locator('.chat-layout .chat-head').waitFor();
   await page.locator('#chat-menu>summary').click();await page.locator('#chat-menu [data-card-project]').click();
   await page.locator('.chat-main .project-picker select').waitFor();assert.equal(await page.locator('#chat-menu').evaluate(d=>d.open),false);
   await page.locator('.project-picker [data-pp="cancel"]').click()}
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('To-dos: title first, one meta line, Details folds the rest, done ones compact.');
}finally{await browser?.close();server.close()}
