import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// An HTML email opened from a routine's to-do (Newsletter cleanup) reads whole (dashboard/events-email-frame.js).
// Newsletter templates tie their height to the frame's: html,body{height:100%!important} kept the frame as small as it
// started, the text cut off under its edge; min-height:100vh made it grow with every fit. The frame now takes the
// email's own height, for a long newsletter, a short one, one with a dark background of its own, and a plain-text one.
// Made-up mail; nothing is sent. EMAIL_FIT_SHOTS=dir saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const para=n=>Array.from({length:n},(_,i)=>`<p>Note ${i+1}: what to sow this week, how deep, and what the frost means for the beds by the fence.</p>`).join('');
const MAIL={
 // a long newsletter whose template pins html and body to the frame, with a full-height wrapper
 101:`<!DOCTYPE html><html><head><style>html,body{height:100%!important;margin:0!important;padding:0!important}.wrap{min-height:100vh;background:#f4f1ea}</style></head>`+
  `<body><div class="wrap"><table width="100%" role="presentation"><tr><td style="padding:24px;color:#2b2b2b"><h1>This week in the garden</h1>${para(24)}<p id="last">See you next week.</p></td></tr></table></div></body></html>`,
 // a short one, the same template
 102:`<html><head><style>html,body{height:100%!important}body{overflow:hidden}</style></head><body><p>A quick note: the seed swap moved to Saturday.</p><p id="last">That's all.</p></body></html>`,
 // its own dark background and light text, a table as tall as the screen at least
 103:`<html style="height:100%"><head><style>body{height:100%!important;margin:0}.sky{min-height:100vh}</style></head><body style="background:#0f1115;color:#e8e8e8">`+
  `<table class="sky" width="100%" bgcolor="#0f1115" role="presentation"><tr><td style="padding:24px"><h1 style="color:#fff">Night sky digest</h1>${para(14)}<p id="last" style="color:#9ab">Clear skies.</p></td></tr></table></body></html>`};
const TEXT={104:'Hello,\n\nThe plain-text edition: no pictures this week.\n\nSee you next week.'};
const items=[[101,'Long newsletter'],[102,'Short newsletter'],[103,'Dark newsletter'],[104,'Plain-text newsletter']];
const card={id:'cl1',title:'4 newsletters: keep or unsubscribe?',status:'pending',scope:'work',created_at:now,event_ids:[1],body:'Pick Keep or Unsubscribe for each one, then confirm.',
 cleanup:{kind:'newsletters',items:items.map(([ev,from],i)=>({n:i+1,from,address:`news${i}@letters.example`,title:'This week',event:ev,count:1,state:'open',plan:'one_click'}))}};
const state={suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}};
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');const ev=+url.searchParams.get('event'),from=items.find(i=>i[0]===ev)?.[1];
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 if(url.pathname==='/api/originals'){res.end(JSON.stringify({originals:from?[{kind:'email',view:'email',source:'gmail.message',event_id:ev,from:`${from} <news@letters.example>`,
  to:'owner@example.com',occurred_at:now,title:'This week',body:TEXT[ev]||'This week in the garden.',url:'https://mail.google.com/mail/u/#all/18c0ffee0000000'+ev%10}]:[]}));return}
 if(url.pathname==='/api/email'){res.end(JSON.stringify({html:MAIL[ev]||'',images:{}}));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.EMAIL_FIT_SHOTS,errors=[];
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[390,844,'dark'],[390,844,'light'],[1440,900,'light'],[1440,900,'dark']]){
  const phone=width<600;
  const context=await browser.newContext({viewport:{width,height},locale:'en-US',timezoneId:'Europe/Brussels',colorScheme:scheme,...(phone?{isMobile:true,hasTouch:true}:{})});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-cl1').waitFor();
  for(const [ev,from] of items){
   await page.locator(`[data-cl-open="${ev}"]`).click();
   if(MAIL[ev]){
    await page.frameLocator('#email-dialog iframe.email-frame').locator('#last').waitFor({state:'attached'});
    await page.waitForFunction(()=>document.querySelector('#email-dialog iframe.email-frame')?.style.visibility==='');
    // down to its last line inside the frame, and no taller than the email (no growing with each fit), a few frames on
    const fit=await page.evaluate(async()=>{for(let i=0;i<6;i++)await new Promise(requestAnimationFrame);
     const f=document.querySelector('#email-dialog iframe.email-frame'),d=f.contentDocument;
     return {frame:f.getBoundingClientRect().height,last:d.getElementById('last').getBoundingClientRect().bottom}});
    assert.ok(fit.frame>=fit.last,`${width} ${scheme} ${from}: the email is cut at ${fit.frame}px, its last line ends at ${fit.last}px`);
    assert.ok(fit.frame<=fit.last+80,`${width} ${scheme} ${from}: the frame is ${fit.frame}px for an email that ends at ${fit.last}px`);
   }else await page.locator('#email-dialog .email-text').getByText('See you next week.').waitFor();
   const name=`${shots}/email-fit-${from.split(' ')[0].toLowerCase()}-${width}-${scheme}`;
   if(shots){await page.screenshot({path:name+'.png'});await page.locator('#email-dialog').evaluate(d=>d.scrollTop=d.scrollHeight);await page.screenshot({path:name+'-end.png'})}
   await page.keyboard.press('Escape');await page.locator('#email-dialog').waitFor({state:'hidden'});
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('email frame fit ok');
