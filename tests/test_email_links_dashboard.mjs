import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A link in a to-do's source email opens outside the dashboard: a new tab on a desktop, the phone's browser in the
// app. The phone app's WebView has no windows, so a target=_blank link goes to the top page, which the email's
// sandbox (no top navigation) used to block: the tap did nothing. Blink's supportsMultipleWindows=false is that
// WebView. Only http(s) and mailto links open, without opener or referrer; javascript: and the dashboard's own
// addresses never do. EMAIL_LINKS_SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const LINK='https://www.example.org/blog/post';
const cards=[{id:'m1',title:'Read the article',body:'They sent a link.',status:'pending',scope:'work',created_at:now,event_ids:[7],source_line:'Email from Sam Example · Mon 2 Nov'}];
const state={suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}};
const original={kind:'email',event_id:7,from:'Sam Example <sam@client.example>',to:'owner@example.com',occurred_at:now,title:'Re: The article',
 body:'Here is the article.',url:'https://mail.google.com/mail/u/0/#all/abc7'};
const mail=`<p>Hi,</p><p>Here it is: <a href="${LINK}">${LINK}</a></p>`+
 `<p>Regards,<br>Sam</p><p><a id="bad" href="javascript:parent.document.title='hacked'">Not a real link</a> <a id="own" href="/api/status">Own</a></p>`;
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/originals'){res.end(JSON.stringify({originals:[original]}));return}
 if(url.pathname==='/api/email'){res.end(JSON.stringify({html:mail,images:{}}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let desktop;const shots=process.env.EMAIL_LINKS_SHOTS,errors=[];
const launch=args=>chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage',...args]});
async function open(browser,width,height,colorScheme,app){
 const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',colorScheme});
 // The app: links the top page opens are taken, as the app's WebView takes them, and not opened here
 if(app)await context.addInitScript(()=>{if(window!==top)return;window.__taken=[];const click=HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click=function(){if(this.target==='_blank'&&!this.href.startsWith(location.origin)){__taken.push({href:this.href,rel:this.rel});return}return click.call(this)}});
 const outside=[];
 await context.route('**/*',route=>{const r=route.request();if(new URL(r.url()).hostname==='127.0.0.1')return route.continue();
  outside.push({url:r.url(),nav:r.isNavigationRequest(),referer:r.headers().referer});
  return route.fulfill({status:200,contentType:'text/html',body:'<!doctype html><title>Outside</title><p>Outside</p>'})});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-m1').waitFor();
 await page.locator('#task-m1 .read-original').first().click();
 const frame=page.frameLocator('#email-content iframe.email-frame');
 await frame.locator(`a[href="${LINK}"]`).waitFor();
 await page.waitForFunction(()=>document.querySelector('#email-content iframe.email-frame')?.style.visibility==='');
 return {context,page,frame,outside}}
try{
 desktop=await launch([]);
 // Only http(s) and mailto links leave the email, never the dashboard's own addresses
 {const {context,page}=await open(desktop,1440,900,'light');
  const check=await page.evaluate(()=>[mailLink('https://a.example/x'),mailLink('http://a.example/'),mailLink('mailto:sam@client.example'),
   mailLink('javascript:alert(1)'),mailLink('data:text/html,hi'),mailLink(location.origin+'/api/status'),mailLink('not a url')]);
  assert.deepEqual(check,['https://a.example/x','http://a.example/','mailto:sam@client.example','','','','']);
  await context.close()}
 // Desktop: a new tab, no opener, no referrer; the dashboard stays where it was
 for(const [width,height,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]){
  const {context,page,frame,outside}=await open(desktop,width,height,scheme);
  if(shots)await page.screenshot({path:`${shots}/email-links-${width}-${scheme}.png`});
  const [tab]=await Promise.all([context.waitForEvent('page'),frame.locator(`a[href="${LINK}"]`).click()]);
  await tab.waitForLoadState();
  assert.equal(tab.url(),LINK);
  assert.equal(await tab.evaluate(()=>window.opener),null,'no opener');
  assert.equal(outside.find(o=>o.url===LINK)?.referer,undefined,'no referrer');
  assert.match(page.url(),/^http:\/\/127\.0\.0\.1:/);
  await tab.close();
  // javascript: and the dashboard's own address do nothing
  const pages=context.pages().length;
  await frame.locator('#bad').click();await frame.locator('#own').click();await page.waitForTimeout(300);
  assert.equal(context.pages().length,pages);assert.notEqual(await page.title(),'hacked');
  await context.close()}
 // The phone app: the tap reaches the top page as a new-tab link without opener or referrer, nothing opens in the app
 {const {context,page,frame}=await open(desktop,390,844,'dark',true);
  const pages=context.pages().length;
  await frame.locator(`a[href="${LINK}"]`).click();
  assert.deepEqual(await page.evaluate(()=>__taken),[{href:LINK,rel:'noopener noreferrer'}]);
  await frame.locator('#bad').click();await page.waitForTimeout(300);
  assert.equal((await page.evaluate(()=>__taken)).length,1);assert.equal(context.pages().length,pages);
  assert.doesNotMatch(await page.locator('#email-content iframe.email-frame').getAttribute('sandbox'),/allow-top-navigation|allow-scripts/);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('Email links: a new tab on a desktop, the top page in the app; only http(s) and mailto, no opener or referrer.');
}finally{await desktop?.close();server.close()}
