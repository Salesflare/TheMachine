import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Open in Gmail (settings-device.js gmailIntent). Every Gmail message has one link, /mail/u/?authuser=<address>#all/<id>,
// on a computer and a phone alike (no mobile-site link any more). Android's browser keeps such a link to itself, so
// there a click opens it as an intent for the Gmail app, with the link itself as the fallback when Gmail isn't
// installed. The phone app hands links to Android itself (MachineShellPlugin.openOutside), and an iPhone or a computer
// opens the link as it is. Made-up mail; nothing is sent and nothing leaves 127.0.0.1.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const GMAIL='https://mail.google.com/mail/u/?authuser=owner%40example.com#all/18c0ffee00000002';
const INTENT='intent://mail.google.com/mail/u/?authuser=owner%40example.com#all/18c0ffee00000002#Intent;scheme=https;package=com.google.android.gm;'
 +'S.browser_fallback_url='+encodeURIComponent(GMAIL)+';end';
const cards=[{id:'m1',title:'Check the account notice',body:'A notice about the account.',status:'pending',scope:'work',created_at:now,event_ids:[7],source_line:'Email from Example Cloud · Thu 12 Nov'}];
const state={suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}};
const original={kind:'email',view:'email',source:'gmail.message',event_id:7,from:'Example Cloud <hello@cloud.example>',to:'owner@example.com',
 occurred_at:now,title:'Account notice',body:'Hello,\n\nA notice about the account.',url:GMAIL};
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/originals'){res.end(JSON.stringify({originals:[original]}));return}
 if(url.pathname==='/api/email'){res.statusCode=404;res.end(JSON.stringify({error:'Email not available'}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const ANDROID='Mozilla/5.0 (Linux; Android 15; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36';
const IPHONE='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [name,ua,intent] of [['android browser',ANDROID,true],['android app',ANDROID+' TheMachineApp/1',false],['iphone',IPHONE,false],['computer',null,false]]){
  const phone=Boolean(ua);
  const context=await browser.newContext({viewport:phone?{width:390,height:844}:{width:1440,height:900},locale:'en-US',
   ...(ua?{userAgent:ua,isMobile:true,hasTouch:true}:{})});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-m1').waitFor();
  await page.locator('#task-m1 .read-original').first().click();
  const link=page.locator('#email-content .email-open a');await link.waitFor();
  assert.equal(await link.getAttribute('href'),GMAIL,`${name}: one link on every device`);
  assert.equal(await page.evaluate(u=>gmailIntent(u),GMAIL),INTENT);
  // the dashboard's own handler runs first; this one, added last, sees what it did and keeps the page here
  await page.evaluate(()=>{window.seen=null;addEventListener('click',e=>{if(e.target.closest('.email-open a')){window.seen=e.defaultPrevented;e.preventDefault()}})});
  await link.click();
  assert.equal(await page.evaluate(()=>window.seen),intent,`${name}: ${intent?'opened as an intent for the Gmail app':'opened as it is'}`);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('gmail app link ok');
