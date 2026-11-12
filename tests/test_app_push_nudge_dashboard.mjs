import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The phone app with its notifications off (never asked, said no, or off in the phone's settings): one short line at the
// top of the home screen, Turn on (the phone's question) or Open settings once the phone won't ask, and an X that keeps
// it away 7 days. On a first sign-in the phone asks once by itself, with nothing shown before it. Never in a browser.
// The app's side (window.machinePhone, mobile/www/inject.js) is a stand-in. SHOT_DIR=<folder> saves both states at 390.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
let devices=[];
const status=()=>({suggestions:[{id:'ab'.repeat(8),title:'Reply to Robin about the garden plan',body:'Robin asked for the dates.',status:'pending',scope:'personal',created_at:now,event_ids:[1]}],
 promises:[],connectors:[{id:'mail',service:'gmail',email:'owner@example.org',display_name:'Mail',status:'ok'}],suggestion_counts:{pending:1},decisions:[],analyses:[],deliveries:[],
 review_health:{},review_runs:[],handled_first:true,notify:{app_push_ready:true,prefs:{},app_devices:devices,push_devices:devices.length}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status()));return}
 if(/^\/brand\/[\w.-]+\.png$/.test(url.pathname)){try{res.setHeader('Content-Type','image/png');res.end(await readFile(new URL('..'+(url.pathname==='/brand/avatar.png'?'/brand/app-icon-192.png':url.pathname),import.meta.url)))}catch{res.statusCode=404;res.end()}return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const APP='Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36 TheMachineApp/1';
const shots=process.env.SHOT_DIR,errors=[];let browser;
// the phone: what it says now, and what its question answers
const phone=()=>{window.__asks=[];const s=()=>sessionStorage.getItem('fake-push')||'prompt';
 localStorage.setItem('machine-app-push',JSON.stringify({id:'dev_1'}));
 window.machinePhone={state:async()=>s(),settings:async()=>{window.__asks.push('settings');return {state:'ok'}},
  pushOn:async()=>{window.__asks.push('pushOn');const a=sessionStorage.getItem('fake-answer')||'off';if(a==='blocked')sessionStorage.setItem('fake-push','blocked');return a}}};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const ctx=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,userAgent:APP});
 await ctx.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await ctx.addInitScript(phone);
 const page=await ctx.newPage();page.on('pageerror',e=>errors.push(e.message));
 const nudge=page.locator('#device-nudge[data-kind="app-push"]');
 // First sign-in: the phone asks by itself, once; said no, the line shows
 await page.goto(base);await nudge.waitFor();
 assert.deepEqual(await page.evaluate(()=>window.__asks),['pushOn']);
 assert.equal((await nudge.innerText()).split('\n')[0],'Get a ping when something needs you.');
 assert.equal(await nudge.locator('[data-app-on]').innerText(),'Turn on');
 {const b=await nudge.boundingBox(),top=await page.locator('#inbox').boundingBox();assert.ok(b.y-top.y<80,'at the top of the home screen');
  const x=await nudge.locator('[data-nudge-x]').boundingBox();assert.ok(x.x+x.width<=390&&x.width>=36,JSON.stringify(x))}
 if(shots){await page.screenshot({path:shots+'/app-push-turn-on-390.png'});await page.emulateMedia({colorScheme:'dark'});await new Promise(r=>setTimeout(r,600));await page.screenshot({path:shots+'/app-push-turn-on-390-dark.png'});await page.emulateMedia({colorScheme:'light'})}
 // Back again: no question by itself; Turn on asks, and a No for good turns it into Open settings
 await page.reload();await nudge.waitFor();assert.deepEqual(await page.evaluate(()=>window.__asks),[]);
 await page.evaluate(()=>sessionStorage.setItem('fake-answer','blocked'));
 await nudge.locator('[data-app-on]').click();await nudge.locator('[data-app-settings]').waitFor();
 assert.equal(await nudge.locator('[data-app-settings]').innerText(),'Open settings');
 if(shots){await page.screenshot({path:shots+'/app-push-open-settings-390.png'});await page.emulateMedia({colorScheme:'dark'});await new Promise(r=>setTimeout(r,600));await page.screenshot({path:shots+'/app-push-open-settings-390-dark.png'});await page.emulateMedia({colorScheme:'light'})}
 await nudge.locator('[data-app-settings]').click();
 assert.deepEqual(await page.evaluate(()=>window.__asks),['pushOn','settings']);
 // X: gone for 7 days, also after a reload; then back
 await nudge.locator('[data-nudge-x]').click();await nudge.waitFor({state:'detached'});assert.equal(await page.locator('#device-nudge').isHidden(),true);
 await page.reload();await page.locator('.card').first().waitFor();await new Promise(r=>setTimeout(r,400));
 assert.equal(await page.locator('#device-nudge').isHidden(),true);
 const wait=await page.evaluate(()=>+localStorage.getItem('nudge-app-push')-Date.now());assert.ok(Math.abs(wait-7*864e5)<6e4,String(wait));
 await page.evaluate(()=>localStorage.setItem('nudge-app-push',String(Date.now()-1)));await page.reload();await nudge.waitFor();
 // On for this phone: no line
 await page.evaluate(()=>sessionStorage.setItem('fake-push','granted'));devices=[{id:'dev_1',label:'Pixel 9'}];
 await page.reload();await page.locator('.card').first().waitFor();await new Promise(r=>setTimeout(r,400));
 assert.equal(await page.locator('#device-nudge').isHidden(),true);
 assert.deepEqual(await page.evaluate(()=>window.__asks),[]);
 devices=[];
 // A phone's browser (not the app): never this line, never the question
 const web=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 await web.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const w=await web.newPage();w.on('pageerror',e=>errors.push(e.message));await w.goto(base);await w.locator('.card').first().waitFor();await new Promise(r=>setTimeout(r,400));
 assert.equal(await w.locator('#device-nudge[data-kind="app-push"]').count(),0);
 await web.close();await ctx.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('app push nudge dashboard ok');
