import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Stop in the Browser view: on a computer, the Browser pane's header has Stop (with the to-do's title beside Browser)
// only while a to-do's run is on the browser (api/browser-now; the one on the tab in front comes first). One click
// stops it with the chat's own stop (chat_stop, via the browser), with no question first. On a phone (and in the
// viewer's own tab) the viewer has the same Stop at the top. SHOTS=<folder> keeps pictures for a look.
const shots=process.env.SHOTS||'';if(shots)await mkdir(shots,{recursive:true});
const dashboard=await dashboardPage();
const view=await readFile(new URL('../deploy/browser/machine-view.js',import.meta.url),'utf8');
const ID='aaaaaaaaaaaaaaa1',OTHER='bbbbbbbbbbbbbbb2';
let working=[];const posts=[];
const card={id:ID,title:'Pay the venue invoice',body:'Paying it on the venue’s site.',status:'accepted',preparation_status:'running',scope:'work',created_at:new Date().toISOString(),event_ids:[1]};
const state=()=>({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},
 browser_link:'https://cp.example/open?to=browser',browser_embed:'/browser/'});
// A stand-in noVNC for the viewer: a screen of the browser's window, nothing to connect to
const ui=`const container=document.getElementById('noVNC_container'),canvas=container.querySelector('canvas');
const d={width:1000,height:700,scale:1,clipViewport:true,_viewportLoc:{x:0,y:0,w:1000,h:700},viewportChangeSize(w,h){},viewportChangePos(){}};
const rfb={_display:d,_canvas:canvas,_rfbConnectionState:'connected',scaleViewport:false,clipViewport:true,_screenSize:()=>({w:container.clientWidth,h:container.clientHeight}),
 _fixScrollbars(){},_setClippingViewport(){},_sendMouse(){},_updateClip(){},_updateScale(){}};export default {rfb};`;
const viewer=`<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>html,body{margin:0;height:100%;overflow:hidden;background:#000}#noVNC_container{position:fixed;inset:0}
canvas{position:absolute;inset:0;width:100%;height:100%;background:linear-gradient(#f1f3f4 0 64px,#fff 64px)}</style>
<script type="module" src="machine-view.js"></script></head><body><div id="noVNC_container"><canvas></canvas></div></body></html>`;
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');
 const send=(type,text)=>{res.setHeader('Content-Type',type);res.end(text)};
 if(url.pathname==='/')return send('text/html',dashboard);
 if(url.pathname==='/api/status')return send('application/json',JSON.stringify(state()));
 if(url.pathname==='/api/browser-now')return send('application/json',JSON.stringify({working,waiting:[],lang:'en'}));
 if(url.pathname==='/api/session')return send('application/json',JSON.stringify({csrf:'token'}));
 if(url.pathname==='/api/action'&&req.method==='POST'){const a=JSON.parse(body);if(a.action==='chat_stop'){posts.push({...a,csrf:req.headers['x-csrf-token']});working=working.filter(w=>w.id!==a.args.suggestion_id)}
  return send('application/json',JSON.stringify(a.action==='chat_stop'?{stopped:true}:{}))}
 if(url.pathname==='/browser/')return send('text/html',viewer);
 if(url.pathname==='/browser/machine-view.js')return send('text/javascript',view);
 if(url.pathname==='/browser/app/ui.js')return send('text/javascript',ui);
 if(url.pathname==='/browser/region')return send('application/json',JSON.stringify({region:{x:0,y:0,w:1,h:1}}));
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/browser/')?404:200;send('application/json','{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[],asked=[];let browser;
const open=async(ctx)=>{const p=await ctx.newPage();p.on('pageerror',e=>errors.push(e.message));p.on('dialog',d=>{asked.push(d.message());d.dismiss()});return p};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const route=ctx=>ctx.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 const context=await browser.newContext({viewport:{width:1440,height:900}});await route(context);
 // Nothing on the browser: no Stop
 const page=await open(context);await page.goto(base);await page.locator('#open-browser').click();await page.locator('#browser-pane').waitFor();
 await page.waitForTimeout(500);
 assert.equal(await page.locator('#bp-stop').isHidden(),true);assert.equal(await page.locator('#bp-job').isHidden(),true);
 // A run on the browser: Stop shows, in the header, with its to-do's title beside Browser; the one in front first
 working=[{id:ID,title:'Pay the venue invoice',step:'Filling in the payment form'},{id:OTHER,title:'Book the room',step:'Opening the booking page'}];
 const stop=page.locator('#bp-stop');await stop.waitFor({timeout:6000});
 assert.equal((await stop.textContent()).trim(),'Stop');
 assert.equal(await page.locator('#bp-job').textContent(),'Pay the venue invoice');
 assert.equal(await stop.getAttribute('aria-label'),'Stop “Pay the venue invoice”');
 {const s=await stop.boundingBox(),f=await page.locator('#bp-frame').boundingBox();
  assert.ok(s.y+s.height<=f.y&&s.x+s.width<=1440&&s.height>=30,'in the header, above the browser, big enough to hit '+JSON.stringify(s))}
 if(shots)await page.screenshot({path:shots+'/pane-stop-1440x900.png'});
 // One click: the chat's stop for that to-do, from the browser; no question first; gone at once
 await stop.click();await stop.waitFor({state:'hidden'});
 assert.deepEqual(posts.map(p=>[p.action,p.args]),[['chat_stop',{suggestion_id:ID,via:'browser'}]]);assert.deepEqual(asked,[]);
 // The other run is on the browser still: Stop is for it now
 await page.waitForFunction(()=>!document.querySelector('#bp-stop').hidden&&document.querySelector('#bp-job').textContent==='Book the room',null,{timeout:6000});
 assert.equal(await stop.isDisabled(),false);
 if(shots)await page.screenshot({path:shots+'/pane-stop-after-1440x900.png'});
 // It ends by itself: Stop goes
 working=[];await stop.waitFor({state:'hidden',timeout:6000});
 // Short window: still in reach
 working=[{id:ID,title:'Pay the venue invoice',step:null}];await page.setViewportSize({width:1440,height:700});await stop.waitFor({timeout:6000});
 if(shots)await page.screenshot({path:shots+'/pane-stop-1440x700.png'});
 // Narrow window (under the top bar): the header keeps Stop on one line
 await page.setViewportSize({width:900,height:700});await page.waitForTimeout(300);
 {const s=await stop.boundingBox(),h=await page.locator('.bp-head').boundingBox();assert.ok(s.x>=0&&s.x+s.width<=900&&s.y>=h.y&&s.y+s.height<=h.y+h.height,JSON.stringify([s,h]))}
 if(shots)await page.screenshot({path:shots+'/pane-stop-900x700.png'});
 // Leaving the pane stops looking
 await page.locator('#bp-close').click();await page.locator('#browser-pane').waitFor({state:'hidden'});
 await context.close();
 // The phone: the viewer's own tab has Stop at the top, the same stop
 posts.length=0;working=[{id:OTHER,title:'Book the room',step:'Opening the booking page'}];
 const phone=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});await route(phone);
 const v=await open(phone);await v.goto(base+'/browser/?frame=window');
 const vs=v.locator('#machine-stop');await vs.waitFor({timeout:8000});
 assert.equal((await vs.textContent()).trim(),'Stop');assert.equal(await vs.getAttribute('aria-label'),'Stop “Book the room”');
 {const b=await vs.boundingBox();assert.ok(b.y<60&&b.x>=0&&b.x+b.width<=390&&b.height>=36,'at the top, in reach '+JSON.stringify(b))}
 if(shots)await v.screenshot({path:shots+'/viewer-stop-390x844.png'});
 await vs.tap();await vs.waitFor({state:'hidden',timeout:6000});
 assert.deepEqual(posts.map(p=>[p.action,p.args,p.csrf]),[['chat_stop',{suggestion_id:OTHER,via:'browser'},'token']]);assert.deepEqual(asked,[]);
 if(shots)await v.screenshot({path:shots+'/viewer-after-390x844.png'});
 // Nothing on the browser: no Stop in the viewer
 const idle=await open(phone);await idle.goto(base+'/browser/?frame=window');await idle.waitForTimeout(1200);
 assert.equal(await idle.locator('#machine-stop').isHidden(),true);
 await phone.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('browser stop dashboard ok');
