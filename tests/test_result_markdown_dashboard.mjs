import assert from 'node:assert/strict';
import {mkdir,readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Read result shows a Markdown file (.md) as the chat does (chatMarkdown): headings, lists and bold drawn,
// never a literal "#", and markup in the file stays text. A plain-text file stays as written. Made-up data.
// SHOTS=<folder> saves the dialog at 1440x900 and 390x844.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const card=(id,title,more)=>({id:id.repeat(16),title,status:'prepared',scope:'work',created_at:now,event_ids:[1],
 body:'Finished. Mark it done if it looks right.',
 outcome:JSON.stringify({state:'done'}),...more});
const MD='# Garden studio homepage: working proposal\n\nInternal draft, not ready to send.\n\n## Two directions\n\n### Direction 1: quiet and editorial\n\nA warm off-white palette, a large serif headline and one strong photo.\n\n### Direction 2: bold and structured\n\n- Dark navy and a tighter grid\n- **Project tiles** up front\n\nA tag <img src=x onerror="window.hit=1"> stays text.';
const TXT='# not a heading in a text file\nSecond line.';
const cards=[card('a','Draft the garden studio homepage proposal',{result_files:[{name:'garden-studio-proposal.md',path:'memory/assistant/garden-studio-proposal.md'}]}),
 card('b','Write the meeting notes',{result_files:[{name:'notes.txt',path:'memory/assistant/notes.txt'}]})];
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}}));return}
 if(url.pathname==='/api/result'){res.end(JSON.stringify({text:url.searchParams.get('file').endsWith('.md')?MD:TXT}));return}
 // the app's own images and fonts, as it serves them (assistant.BRAND_ASSETS), so the shots show every image
 const asset={'/brand/avatar.png':'/brand/app-icon-192.png','/brand/serif.woff2':'/brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'/brand/fonts/inter-latin.woff2'}[url.pathname]||url.pathname;
 if(/^\/brand\/[\w.-]+\.(png|webp|svg|woff2)$/.test(url.pathname)){const ext=url.pathname.split('.').pop();
  try{const body=await readFile(new URL('..'+asset,import.meta.url));res.setHeader('Content-Type',{png:'image/png',webp:'image/webp',svg:'image/svg+xml',woff2:'font/woff2'}[ext]);res.end(body)}catch{res.statusCode=404;res.end()}return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[],shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:'light',locale:'en-US'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-'+'a'.repeat(16)).waitFor();
  const content=page.locator('#result-content');
  const open=async c=>{await page.evaluate(id=>openResult(id),c.repeat(16));await page.locator('#result-dialog[open]').waitFor()};
  const close=()=>page.evaluate(()=>document.querySelector('#result-dialog').close());
  // A Markdown file: headings drawn (as bold lines, like the chat), lists as lists, no literal marks
  await open('a');
  await page.waitForFunction(()=>[...document.images].every(i=>i.complete));
  assert.deepEqual(await page.evaluate(()=>[...document.images].filter(i=>i.getClientRects().length&&!i.naturalWidth).map(i=>i.src)),[],'every image shown loaded');
  if(shots)await page.screenshot({path:`${shots}/result-md-${width}.png`});
  const text=await content.innerText();
  assert.doesNotMatch(text,/^#/m,'no literal heading marks');
  assert.match(text,/Direction 1: quiet and editorial/);
  assert.equal(await content.locator('strong',{hasText:'Two directions'}).count(),1,'a heading shows as a bold line');
  assert.equal(await content.locator('li').count(),2,'a list is a list');
  // its markup stays text: no element made from the file, nothing ran
  assert.equal(await content.locator('img').count(),0);assert.match(text,/<img src=x/);
  assert.equal(await page.evaluate(()=>window.hit),undefined);
  // Copy draft still copies the file as written
  assert.equal(await page.evaluate(()=>resultText),MD);
  await close();
  // A plain-text file stays as written
  await open('b');
  if(shots)await page.screenshot({path:`${shots}/result-txt-${width}.png`});
  assert.match(await content.innerText(),/^# not a heading in a text file/m);
  assert.equal(await content.locator('strong').count(),0);
  await close();
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('result markdown ok');
}finally{await browser?.close();await new Promise(r=>server.close(r))}
