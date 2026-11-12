import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A to-do's source email when Gmail doesn't answer (/api/email refuses with retry): the viewer shows the saved text,
// one short "Couldn't load the full email. Try again" line and Open in Gmail, never "Loading…" for good. Try again
// reads it once more and shows the full email. An email with no full copy (refused without retry) is its saved text
// alone, with no retry line. EMAIL_RETRY_SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[{id:'m1',title:'Answer the rate limit question',body:'They asked about the limit.',status:'pending',scope:'work',created_at:now,event_ids:[7],source_line:'Email from Sam Example · Sat 7 Nov'},
 {id:'m2',title:'Reply about the invoice',body:'They asked for the invoice.',status:'pending',scope:'work',created_at:now,event_ids:[8],source_line:'Email from Sam Example · Sat 7 Nov'}];
const state={suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}};
const original=ev=>({kind:'email',event_id:ev,from:'Sam Example <sam@client.example>',to:'owner@example.com',occurred_at:now,title:'Rate limit on the contacts endpoint?',
 body:'Is there a rate limit on the contacts endpoint?',url:'https://mail.google.com/mail/u/0/#all/abc'+ev});
let gmailUp=false;const asked={7:0,8:0};
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/originals'){res.end(JSON.stringify({originals:[original(url.searchParams.get('id')==='m1'?7:8)]}));return}
 if(url.pathname==='/api/email'){const ev=+url.searchParams.get('event');asked[ev]++;
  if(ev===8){res.statusCode=404;res.end(JSON.stringify({error:'Email not available'}));return}
  if(!gmailUp){res.statusCode=404;res.end(JSON.stringify({error:'Email not available',retry:true}));return}
  res.end(JSON.stringify({html:'<p>The full email, with its <b>formatting</b>.</p>',images:{}}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;const shots=process.env.EMAIL_RETRY_SHOTS,errors=[];
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){gmailUp=false;
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-m1').waitFor();
  await page.locator('#task-m1 .read-original').first().click();
  const content=page.locator('#email-content'),retry=content.locator('.email-retry');
  await retry.waitFor({timeout:10000});
  assert.equal((await retry.innerText()).trim(),'Couldn’t load the full email. Try again');
  assert.match(await content.locator('.email-body').innerText(),/Is there a rate limit on the contacts endpoint\?/,'the saved text shows');
  assert.doesNotMatch(await content.innerText(),/Loading…/);
  const gmail=content.locator('.email-open a');
  assert.equal(await gmail.innerText(),'Open in Gmail ↗');
  assert.equal(await gmail.getAttribute('href'),'https://mail.google.com/mail/u/0/#all/abc7');
  if(shots)await page.screenshot({path:`${shots}/email-retry-${width}x${height}.png`});
  // Gmail answers again: Try again shows the full email, and the retry line goes
  gmailUp=true;await retry.locator('button').click();
  await content.locator('iframe.email-frame').waitFor();
  const frame=page.frameLocator('#email-content iframe.email-frame');
  assert.match(await frame.locator('body').innerText(),/The full email, with its formatting\./);
  assert.equal(await content.locator('.email-retry').count(),0);
  assert.equal(await gmail.getAttribute('href'),'https://mail.google.com/mail/u/0/#all/abc7');
  if(shots)await page.screenshot({path:`${shots}/email-retried-${width}x${height}.png`});
  await page.keyboard.press('Escape');
  // An email with no full copy: its saved text, no retry line
  await page.locator('#task-m2 .read-original').first().click();
  await page.waitForFunction(()=>/Is there a rate limit/.test(document.querySelector('#email-content .email-body')?.innerText||''));
  assert.ok(asked[8]>0);
  assert.equal(await content.locator('.email-retry').count(),0);
  assert.equal(await content.locator('.email-open a').getAttribute('href'),'https://mail.google.com/mail/u/0/#all/abc8');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('Source email: a Gmail failure shows the saved text, a retry line and Open in Gmail; Try again loads it.');
}finally{await browser?.close();server.close()}
