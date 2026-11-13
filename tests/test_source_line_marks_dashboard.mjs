import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {createServer} from 'node:http';
import {fileURLToPath} from 'node:url';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's source line shows the icon of the message it names, for every kind a line can name (tests/test_source_line_marks.py
// builds one to-do per kind through the real service, each with an older Gmail email as "+1 more" and a Gmail link among
// its originals). "WhatsApp to Robin Example · Thu 12 Nov (+6 more)" once wore Gmail's mark from an email among the six.
// SOURCE_MARK_SHOTS=dir saves the reported to-do at 390 and 1440, light and dark; SOURCE_MARK_PAGE=<other dashboard.html>
// takes them from that page (a before set) without the checks.
const root=new URL('../',import.meta.url);
const py=`import sys,tempfile
sys.path[:0]=['.','tests']
import test_source_line_marks as m
with tempfile.TemporaryDirectory() as folder:
    print(m.dump(folder))`;
const run=spawnSync(process.env.PYTHON||(process.platform==='win32'?'python':'python3'),['-c',py],{cwd:fileURLToPath(root),encoding:'utf8'});
assert.equal(run.status,0,run.stderr);
const data=JSON.parse(run.stdout),other=process.env.SOURCE_MARK_PAGE,shots=process.env.SOURCE_MARK_SHOTS;
const dashboard=await dashboardPage(other||undefined);
const now=new Date().toISOString();
const cards=data.cards.map(c=>({...c,title:c.id==='owner-wa'?'Correct the charge for the order':'To-do '+c.id,body:'Something to look at.',status:'pending',scope:'work',created_at:now}));
const state={suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:data.connectors,fleet:{on:false,fleets:[]}};
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname.startsWith('/brand/logos/mono/')){const f=new URL('dashboard/logos/mono/'+url.pathname.split('/').pop(),root);
  try{res.setHeader('Content-Type','image/svg+xml');res.end(await (await import('node:fs/promises')).readFile(f))}catch{res.statusCode=404;res.end()}return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 if(shots){
  for(const scheme of ['light','dark'])for(const [w,h] of [[390,844],[1440,900]]){
   const context=await browser.newContext({viewport:{width:w,height:h},colorScheme:scheme,deviceScaleFactor:2});
   await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
   const page=await context.newPage();await page.goto('http://127.0.0.1:'+server.address().port);
   const card=page.locator('#task-owner-wa');await card.waitFor();await card.scrollIntoViewIfNeeded();await page.waitForTimeout(400);
   await card.screenshot({path:`${shots}/source-line-${w}-${scheme}.png`});await context.close()}
 }
 if(!other){
  const context=await browser.newContext({viewport:{width:390,height:844}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-owner-wa').waitFor();
  const shown=await page.evaluate(ids=>ids.map(id=>{const e=document.querySelector(`#task-${CSS.escape(id)} .read-original`);
   return {id,via:e&&[...e.classList].find(c=>c.startsWith('via-'))?.slice(4),label:e?.getAttribute('aria-label'),line:e?.textContent.trim()}}),cards.map(c=>c.id));
  const marks=await page.evaluate(cs=>Object.fromEntries(cs.map(c=>[c.id,sourceMark(c.kind,c.account_ids[0],c.kind==='android.notification'?'com.whatsapp':'')])),cards);
  const MAIL=new Set(['gmail.message','fleet.email']);
  for(const s of shown){const c=cards.find(x=>x.id===s.id);
   assert.ok(s.via,`${c.kind}: its source line shows a mark`);
   assert.notEqual(s.via,'source',`${c.kind}: a mark of its own, never the neutral one (add it to todos-logos.js)`);
   if(!MAIL.has(c.kind)){
    assert.ok(!['gmail','outlook','mail'].includes(s.via),`${c.kind}: "${s.line}" wears ${s.via}, the mark of the email among its other messages`);
    assert.equal(s.label,'Read message',c.kind)}
   // (an email on an account the page doesn't list reads Gmail or Outlook by its links; a Fleet brief shows the hand-off)
   if(!['fleet.brief','gmail.message'].includes(c.kind))assert.equal(s.via,marks[s.id]==='imap'?'mail':marks[s.id],`${c.kind}: the mark of the message the line names`)}
  const by=id=>shown.find(s=>s.id===id).via;
  assert.deepEqual(['owner-wa','reordered'].map(by),['whatsapp','whatsapp']);
  assert.equal(by(cards.find(c=>c.kind==='android.notification').id),'whatsapp','a phone notification by its app');
  assert.equal(by(cards.find(c=>c.kind==='fleet.brief').id),'handoff');
  assert.equal(by(cards.find(c=>c.kind==='slack.message').id),'slack');
  assert.equal(by(cards.find(c=>c.kind==='gmail.message').id),'gmail');
  // a to-do saved before the server named its message: the line's words still win over an email among the originals
  await page.evaluate(()=>{const s=state.suggestions.find(x=>x.id==='owner-wa');delete s.source_mark;window.__via=cardViaIcon(s);window.__mail=isEmail(s)});
  assert.deepEqual(await page.evaluate(()=>[window.__via,window.__mail]),['whatsapp',false]);
  console.log(`Source line marks: ${shown.length} to-dos, every kind by the message its line names.`);
 }
}finally{await browser?.close();server.close()}
