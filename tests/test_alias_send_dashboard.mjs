// From in the review: a small picker when the mailbox may also send as an alias of the owner's (from_options), starting
// at the draft's default; the pick travels with Send now as `sender`. A draft without aliases shows From as plain text
// and sends no `sender`. Also in Dutch and dark, and it fits at 390px. Synthetic data, a local fixture server, nothing
// sent. SHOTS=<folder> saves screenshots.
import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

const dashboard=await dashboardPage();
const nl=await readFile(new URL('../i18n/nl.json',import.meta.url),'utf8'),en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const aliasId='1234567890abcdef',plainId='0011223344556677',aliasRev='1234567890ab',plainRev='abcdefabcdef';
const mailbox='sam@acme.example',alias='partnerships@acme.example';
const body='Hi Casey,\n\nThanks for reaching out. Happy to talk about a partnership. Does Thursday work?\n\nSam';
const subject='Re: Casey (Partner) / Sam (Acme): a partnership idea, the API documentation and the test credits';
const reply={kind:'email',label:'Send reply',revision:aliasRev,account_id:'mail',from:alias,from_options:[mailbox,alias],to:['casey@partner.example'],cc:['alex@partner.example'],bcc:[],
  subject,body,signature:true,thread_id:'abc123',in_reply_to:'<m1@partner.example>'};
const plain={...reply,revision:plainRev,from:mailbox,from_options:undefined,to:['robin@client.example'],subject:'Re: Invoice',body:'Hi Robin,\n\nSent it just now.\n\nSam'};
const card=(id,title,a)=>({id,title,body:'Drafted the reply.',status:'prepared',event_ids:[1],next_action:a,next_actions:[a],
  outcome:JSON.stringify({state:'needs_you',needs:'Check the reply and send it'}),scope:'work',created_at:new Date().toISOString()});
let lang='en';
const languages={en:'English',nl:'Nederlands'};
const calls=[],errors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/nl.json'){res.end(nl);return}
 if(url.pathname==='/i18n/en.json'){res.end(en);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[card(aliasId,'Casey asks about a partnership',reply),card(plainId,'Robin asks for the invoice',plain)],
  connectors:[],suggestion_counts:{prepared:2},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
  locale:{locale:'en-BE',region:'BE',language:lang,language_set:true,clock:'auto',hour12:false,auto_hour12:false,date_locale:lang==='en'?'en-GB':'nl-BE',languages,saveable:true}}));return}
 if(url.pathname==='/api/action'){let b='';for await(const c of req)b+=c;calls.push(JSON.parse(b));res.end(JSON.stringify({status:'queued'}));return}
 res.statusCode=url.pathname.startsWith('/api/')?200:404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const fits=page=>page.evaluate(()=>{const d=document.querySelector('#send-dialog').getBoundingClientRect(),s=document.querySelector('#send-from')?.getBoundingClientRect();
 return document.documentElement.scrollWidth<=innerWidth&&(!s||(s.right<=d.right&&s.left>=d.left&&s.height<=40))});
const open=async(page,id,rev)=>{await page.locator(`#task-${id} [data-smart="${rev}"]`).click();await page.locator('#send-dialog').waitFor({state:'visible'})};
const confirmed=async page=>{for(let i=0;i<100&&!calls.some(c=>c.action==='confirm_action');i++)await page.waitForTimeout(20);
 const c=calls.find(c=>c.action==='confirm_action');calls.length=0;return c};
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,language,scheme] of [[1440,900,'en','light'],[1440,700,'en','light'],[390,844,'en','light'],[1440,900,'nl','dark'],[390,844,'nl','dark']]){
  lang=language;
  const context=await browser.newContext({viewport:{width,height},locale:language==='nl'?'nl-BE':'en-GB',colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  if(language==='nl')await page.locator('html[lang="nl"]').waitFor({state:'attached'}).catch(()=>{});
  await page.evaluate(()=>refresh());
  await page.locator(`#task-${aliasId}`).waitFor();
  // The reply to mail that came to the alias: From is a picker, starting at the alias; nothing goes out before Send now
  await open(page,aliasId,aliasRev);
  const from=page.locator('#send-from');
  await from.waitFor();
  assert.deepEqual(await from.locator('option').allTextContents(),[mailbox,alias]);
  assert.equal(await from.inputValue(),alias);
  assert.equal(await from.getAttribute('aria-label'),language==='nl'?'Versturen vanaf':'Send from');
  assert.equal(await page.locator('#send-head dt').first().textContent(),language==='nl'?'Van':'From');
  assert.equal(calls.filter(c=>c.action==='confirm_action').length,0);
  assert.equal(await fits(page),true,`fits at ${width}x${height}`);
  // The top reads like a compose header: From, To, Cc and Subject share one label column and one value column, the
  // one-line rows are the same height, and the long subject wraps in full (still editable, still one line of text)
  const top=await page.evaluate(()=>{const box=e=>e.getBoundingClientRect(),rows=[...document.querySelectorAll('#send-head>div'),document.querySelector('#send-subject-label')];
   return {labels:rows.map(r=>Math.round(box(r.firstElementChild).left)),values:rows.map(r=>Math.round(box(r.lastElementChild).left)),heights:rows.slice(0,3).map(r=>Math.round(box(r).height)),
    gap:Math.round(box(rows[0].lastElementChild).left-box(rows[0]).left),subject:(s=>({lines:Math.round(s.clientHeight/parseFloat(getComputedStyle(s).lineHeight)),cut:s.scrollHeight>s.clientHeight+1||s.scrollWidth>s.clientWidth+1}))(document.querySelector('#send-subject'))}});
  assert.deepEqual(await page.locator('#send-head dt').allTextContents(),language==='nl'?['Van','Aan','Cc']:['From','To','Cc']);
  assert.equal(new Set(top.labels).size,1,JSON.stringify(top));assert.equal(new Set(top.values).size,1,JSON.stringify(top));
  assert.equal(new Set(top.heights).size,1,JSON.stringify(top));assert.ok(top.gap<=110,'no wide empty label column: '+top.gap);
  assert.equal(await page.locator('#send-subject').inputValue(),subject);assert.equal(top.subject.cut,false,'the subject is not cut off');
  if(width===390)assert.ok(top.subject.lines>=2,'the long subject wraps on a phone');
  await page.locator('#send-subject').press('End');await page.locator('#send-subject').press('Enter');
  await page.locator('#send-subject').evaluate(s=>{s.setRangeText('\nnext',s.value.length,s.value.length,'end');s.dispatchEvent(new Event('input',{bubbles:true}))});
  assert.equal(await page.locator('#send-subject').inputValue(),subject+' next');
  await page.locator('#send-subject').fill(subject);
  if(shots)await page.screenshot({path:`${shots}/from-picker-${language}-${scheme}-${width}x${height}.png`});
  if(shots&&width===390)await page.locator('#send-dialog').screenshot({path:`${shots}/from-picker-dialog-${language}-${scheme}-${width}.png`});
  // The pick stays when the rows are drawn again (Edit, ticking recipients) and goes with the approval
  await from.selectOption(mailbox);
  await page.evaluate(()=>sendHeader(false));
  assert.equal(await page.locator('#send-from').inputValue(),mailbox);
  await page.locator('#send-from').selectOption(alias);
  await page.locator('#send-confirm').click();
  let c=await confirmed(page);
  assert.equal(c.args.revision,aliasRev);assert.equal(c.args.sender,alias);
  // Pick the mailbox address instead
  await page.locator('#send-dialog').evaluate(d=>d.open&&d.close());
  await open(page,aliasId,aliasRev);
  assert.equal(await page.locator('#send-from').inputValue(),alias);  // each review starts at the draft's default
  await page.locator('#send-from').selectOption(mailbox);
  await page.locator('#send-confirm').click();
  c=await confirmed(page);assert.equal(c.args.sender,mailbox);
  // No alias to offer: From is plain text and Send now carries no sender
  await page.locator('#send-dialog').evaluate(d=>d.open&&d.close());
  await open(page,plainId,plainRev);
  assert.equal(await page.locator('#send-from').count(),0);
  assert.equal(await page.locator('#send-head dd').first().textContent(),mailbox);
  await page.locator('#send-confirm').click();
  c=await confirmed(page);assert.equal('sender' in c.args,false);
  if(process.env.VERBOSE)console.log('ok at',width,height,language,scheme);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('alias send dashboard ok');
