import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A self-hosted Machine is reached over its owner's tailnet only, and a phone stops Tailscale in the background: the
// Machine is fine, but the phone can't reach it. When a call gets no answer at all (the link cut, the device online),
// the offline bar says Tailscale may be off on this device, with Open Tailscale on a phone (the Android app opens it
// itself, machinePhone.tailscale; else its store page). A hosted Machine (manage_url), a server's error (a 502) and a
// device without a network keep the plain "Offline" line. shell-network.js, netTs.
const raw=await dashboardPage();
const SCOPE='d4'.repeat(16),iso=new Date().toISOString();
const TS=/Can’t reach your Machine\. Tailscale may be off on this device\./,PLAIN=/^Offline\. Showing what was here at /;
const ANDROID='Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 TheMachineApp/1';
let manage=null,mode='ok';
const status=()=>({suggestions:[{id:'1'.repeat(16),title:'Book the venue',body:'The team asked for a date.',status:'pending',scope:'work',created_at:iso,event_ids:[1]}],
 promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false},ui_version:'v1',manage_url:manage});
const page=()=>raw.replace('__CSRF__','').replaceAll('__UI_VERSION__','v1').replace('__BASE__','/').replace('__CACHE_SCOPE__',SCOPE);
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Cache-Control','no-store');res.setHeader('Connection','close');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(page());return}
 // cut: no answer at all, as with Tailscale off; down: the host answers for a Machine away (an HTML 502)
 if(mode==='cut'){req.socket.destroy();return}
 if(mode==='down'){res.statusCode=502;res.setHeader('Content-Type','text/html');res.end('<h1>502</h1>');return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/session'){res.end(JSON.stringify({csrf:'c'.repeat(64),cache_scope:SCOPE}));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const shots=process.env.SHOTS||'',errors=[];let browser;
const bar=p=>p.evaluate(()=>{const b=document.querySelector('#offline-bar');return b.hidden||!b.offsetParent?'':b.innerText.replace(/\s+/g,' ').trim()});
// One refresh now (as on opening the app), then the page's own check decides: wait for what the bar shows
const barUntil=async(p,re,label)=>{await p.evaluate(()=>refresh().catch(()=>{}));try{await p.waitForFunction(src=>{const b=document.querySelector('#offline-bar');
  return new RegExp(src).test(b.hidden||!b.offsetParent?'':b.innerText.replace(/\s+/g,' ').trim())},re.source,{timeout:30000})}
 catch{throw Error('timed out: '+label+' (bar: '+JSON.stringify(await bar(p))+')')}return bar(p)};
const open=p=>p.evaluate(()=>[...document.querySelectorAll('#offline-bar [data-ts-open]')].map(a=>a.getAttribute('href')));
// A fresh device: online first (the to-dos kept), then the link to the Machine as `how`
async function look({width,height,ua,scheme='dark',hosted=false,how='cut'}){manage=hosted?'https://app.example.invalid/':null;mode='ok';
 const ctx=await browser.newContext({viewport:{width,height},colorScheme:scheme,...(ua?{userAgent:ua,isMobile:true,hasTouch:true}:{})});
 await ctx.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const p=await ctx.newPage();p.on('pageerror',e=>errors.push(e.message));await p.goto(base);await p.locator('#suggestions article[id]').first().waitFor();
 assert.equal(await bar(p),'','no bar while the Machine answers');
 if(how==='device')await ctx.setOffline(true);else mode=how;
 return {ctx,p}}
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});

 // 1. The Android app, a self-hosted Machine, the link cut: the reason, Open Tailscale (its store page) and Try now
 for(const scheme of ['dark','light']){const {ctx,p}=await look({width:390,height:844,ua:ANDROID,scheme});
  const text=await barUntil(p,TS,'the Tailscale line on a phone');
  assert.match(text,/Open Tailscale Try now$/,'Open Tailscale next to Try now');
  assert.deepEqual(await open(p),['https://play.google.com/store/apps/details?id=com.tailscale.ipn']);
  if(shots)await p.screenshot({path:`${shots}/offline-tailscale-390-${scheme}.png`});
  if(scheme==='dark'){
   // With the app's bridge, Open Tailscale opens the app itself and stays on the page
   await p.evaluate(()=>{window.tsAsked=0;window.machinePhone={tailscale:async()=>{window.tsAsked++;return {state:'ok'}}}});
   await p.click('#offline-bar [data-ts-open]');await p.waitForFunction(()=>window.tsAsked>0);
   assert.equal(await p.evaluate(()=>window.tsAsked),1,'the app opens Tailscale');
   assert.equal(p.url(),base,'the page stays');
   // The Machine answers again: the bar goes
   mode='ok';await barUntil(p,/^$/,'the bar goes once the Machine answers')}
  await ctx.close()}

 // 2. A computer's browser: the same line, no button (nothing to open there)
 for(const scheme of ['dark','light']){const {ctx,p}=await look({width:1440,height:900,scheme});
  const text=await barUntil(p,TS,'the Tailscale line on a computer');
  assert.match(text,/Tailscale may be off on this device\. Try now$/);
  assert.deepEqual(await open(p),[],'no Open Tailscale on a computer');
  if(shots)await p.screenshot({path:`${shots}/offline-tailscale-1440-${scheme}.png`});await ctx.close()}

 // 3. Not Tailscale's: a hosted Machine, the host's 502 for a Machine away, the device without a network
 for(const [label,o] of [['hosted',{hosted:true}],['a server error',{how:'down'}],['no network',{how:'device'}]]){
  const {ctx,p}=await look({width:390,height:844,ua:ANDROID,...o});
  const text=await barUntil(p,o.how==='device'?/^Offline\./:PLAIN,label+': the plain line');
  assert.doesNotMatch(text,/Tailscale/,label+': no word of Tailscale');assert.deepEqual(await open(p),[],label+': no Open Tailscale');
  await ctx.close()}
 assert.deepEqual(errors,[]);
 console.log('ok: offline over Tailscale says why, and only there');
}finally{await browser?.close();server.close()}
