import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// An HTML email reads whole in the viewer (dashboard/events-email-frame.js). A template that sets height:100% on its
// <html>, <body> and wrapper made the frame as tall as the frame itself (120px): only the header logo showed, never
// the text. The frame now takes the email's own height. In dark mode a logo drawn dark on a see-through background
// keeps the light background it was drawn on, as Gmail shows it. And "Open in Gmail" on a phone opens the
// conversation on Gmail's mobile site in the right account (views.event_views phone_url); a desktop keeps the desktop
// link. Made-up mail; nothing is sent. EMAIL_FRAME_SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const DESKTOP='https://mail.google.com/mail/u/?authuser=owner%40example.com#all/18c0ffee00000002';
const PHONE='https://mail.google.com/mail/mu/mp/?authuser=owner%40example.com#cv/All%20Mail/18c0ffee00000001';
const cards=[{id:'m1',title:'Check the account notice',body:'A notice about the account.',status:'pending',scope:'work',created_at:now,event_ids:[7],source_line:'Email from Example Cloud · Thu 12 Nov'}];
const state={suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}};
const original={kind:'email',view:'email',source:'gmail.message',event_id:7,from:'Example Cloud <hello@cloud.example>',to:'owner@example.com',
 occurred_at:now,title:'Account notice: a change to your sign-in',body:'Hello,\n\nA change to your sign-in.',url:DESKTOP,phone_url:PHONE};
// A dark wordmark on a transparent background, like a mail's header logo
const logo='data:image/svg+xml,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="160" height="40"><text x="0" y="30" font-size="28" font-family="sans-serif" fill="#111">Example</text></svg>');
const para=n=>Array.from({length:n},(_,i)=>`<p>Paragraph ${i+1} of the notice: what changed, what it means for the account and what to do next.</p>`).join('');
const mail=`<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">`+
 `<html style="height:100%" dir="ltr" lang="en"><head><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><style></style></head>`+
 `<body style="padding:0;margin:0;height:100%"><div style="padding:48px 16px 80px;margin:0;height:100%;background-color:#f6f9fc">`+
 `<table align="center" width="100%" border="0" cellPadding="0" cellSpacing="0" role="presentation" style="max-width:640px"><tbody><tr style="width:100%"><td>`+
 `<a href="https://www.example.org" style="display:block;margin:0 auto 24px;width:fit-content"><img id="logo" src="${logo}" style="display:block;border:none;height:40px"></a>`+
 `<table align="center" width="100%" role="presentation" style="background-color:#ffffff;border-radius:8px;padding:24px"><tbody><tr style="width:100%"><td>`+
 `<p>Hello,</p><p><strong>What happened</strong></p>${para(8)}<ul><li><strong>Your name</strong></li><li><strong>Your email address</strong></li></ul>`+
 `<p id="last">The Example Cloud team</p></td></tr></tbody></table></td></tr></tbody></table></div></body></html>`;
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/originals'){res.end(JSON.stringify({originals:[original]}));return}
 if(url.pathname==='/api/email'){res.end(JSON.stringify({html:mail,images:{}}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.EMAIL_FRAME_SHOTS,errors=[];
const IPHONE='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]){
  const phone=width<600;
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme,...(phone?{userAgent:IPHONE,isMobile:true,hasTouch:true}:{})});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-m1').waitFor();
  await page.locator('#task-m1 .read-original').first().click();
  const frame=page.frameLocator('#email-content iframe.email-frame');
  await frame.locator('#last').waitFor({state:'attached'});
  await page.waitForFunction(()=>document.querySelector('#email-content iframe.email-frame')?.style.visibility==='');
  await page.waitForTimeout(300);
  // the whole email, down to its last line, inside the frame: the frame is as tall as what the email draws
  const fit=await page.evaluate(()=>{const f=document.querySelector('#email-content iframe.email-frame'),d=f.contentDocument;
   return {frame:f.getBoundingClientRect().height,last:d.getElementById('last').getBoundingClientRect().bottom}});
  assert.ok(fit.frame>=fit.last&&fit.frame>400,`${width} ${scheme}: the email is cut at ${fit.frame}px, its last line ends at ${fit.last}px`);
  // dark mode: the logo keeps a light background behind it; light mode leaves it as the email drew it
  const behind=await frame.locator('#logo').evaluate(img=>getComputedStyle(img).backgroundColor);
  const rgb=(/rgba?\((\d+), (\d+), (\d+)/.exec(behind)||[]).slice(1).map(Number);
  if(scheme==='dark')assert.ok(rgb.length&&Math.min(...rgb)>200,`dark mode: the logo has ${behind} behind it`);
  else assert.match(behind,/rgba\(0, 0, 0, 0\)|transparent/);
  // Open in Gmail: the mobile site's conversation on a phone, the desktop link on a computer
  assert.equal(await page.locator('#email-content .email-open a').getAttribute('href'),phone?PHONE:DESKTOP);
  assert.equal(await page.locator('#email-content .email-open a').innerText(),'Open in Gmail ↗');
  if(shots)await page.screenshot({path:`${shots}/email-frame-${width}-${scheme}.png`,fullPage:false});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('email frame layout ok');
