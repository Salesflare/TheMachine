import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The dashboard's Browser pane frames the Machine's browser window to fit the pane: on first open, after a resize,
// in and out of Full size, and when the pane is shown again after the viewer reconnected while another view was open
// (the frame stays loaded at size 0 then). That last one used to come back zoomed to 100% with only a corner of the
// window showing in the bottom right, the rest covered, until Full size. A zoom set by hand stays, and never leaves
// the window out of reach. The viewer is deploy/browser/machine-view.js on a stand-in noVNC that behaves like the real
// one where it matters: a screen box that is 0x0 while hidden, a canvas centered in it, a viewport resized on each size
// change of that box (a ResizeObserver), and a new connection object on a reconnect.
const dashboard=await dashboardPage();
const view=await readFile(new URL('../deploy/browser/machine-view.js',import.meta.url),'utf8');
// A 4K desktop at 150% (2560x1440 points) with the Machine's browser on its right half, the dashboard's own window on its left
const region={x:1287/2560,y:38/1440,w:1261/2560,h:1390/1440};
const ui=`const W=3840,H=2160,R=${JSON.stringify(region)};
const pic=document.createElement('canvas');pic.width=W;pic.height=H;{const g=pic.getContext('2d');
 g.fillStyle='#4b5563';g.fillRect(0,0,W,H);g.fillStyle='#e5e7eb';g.fillRect(18,57,1890,2085);g.fillStyle='#9ca3af';g.fillRect(18,57,300,2085);
 const x=R.x*W,y=R.y*H,w=R.w*W,h=R.h*H;g.fillStyle='#fff';g.fillRect(x,y,w,h);g.fillStyle='#dee1e6';g.fillRect(x,y,w,120);
 g.fillStyle='#1a73e8';g.fillRect(x+60,y+220,w-120,90);g.fillStyle='#111';g.font='bold 110px sans-serif';g.fillText('Machine browser',x+60,y+500);
 g.strokeStyle='#e11d48';g.lineWidth=12;g.strokeRect(x+6,y+6,w-12,h-12)}
const container=document.getElementById('noVNC_container');
function connect(){
 container.querySelector('.screen')?.remove();
 const screen=document.createElement('div');screen.className='screen';container.append(screen);
 const canvas=document.createElement('canvas');screen.append(canvas);const vp={x:0,y:0,w:W,h:H};let scale=1;
 const draw=()=>{canvas.getContext('2d').drawImage(pic,vp.x,vp.y,vp.w,vp.h,0,0,vp.w,vp.h)};
 const d={width:W,height:H,clipViewport:false,_viewportLoc:vp,get scale(){return scale},set scale(v){scale=v;this._rescale()},
  _rescale(){canvas.style.width=Math.round(vp.w*scale)+'px';canvas.style.height=Math.round(vp.h*scale)+'px'},
  viewportChangeSize(w,h){w=Math.min(Math.floor(w),W);h=Math.min(Math.floor(h),H);if(vp.w===w&&vp.h===h)return;vp.w=w;vp.h=h;canvas.width=w;canvas.height=h;
   this.viewportChangePos(0,0);this._rescale()},  // as noVNC: the position first, the visible size after
  viewportChangePos(dx,dy){vp.x=Math.max(0,Math.min(W-vp.w,Math.floor(vp.x+dx)));vp.y=Math.max(0,Math.min(H-vp.h,Math.floor(vp.y+dy)));draw()}};
 const rfb={_display:d,_canvas:canvas,_screen:screen,_rfbConnectionState:'connected',scaleViewport:false,clipViewport:false,
  _screenSize(){return {w:screen.offsetWidth,h:screen.offsetHeight}},_fixScrollbars(){},_setClippingViewport(){},_sendMouse(){},
  _updateClip(){const s=this._screenSize();d.viewportChangeSize(s.w,s.h)},_updateScale(){}};
 new ResizeObserver(()=>requestAnimationFrame(()=>{rfb._updateClip();rfb._updateScale()})).observe(screen);
 d.viewportChangeSize(W,H);return rfb}
const UI={rfb:connect(),closeControlbar(){}};
window.reconnect=()=>{UI.rfb=connect()};
// Where the browser's window shows in the pane, and what the cover leaves open
window.look=()=>{const r=UI.rfb,d=r._display,v=d._viewportLoc,c=r._canvas.getBoundingClientRect();
 const box=[c.left+(R.x*W-v.x)*d.scale,c.top+(R.y*H-v.y)*d.scale,R.w*W*d.scale,R.h*H*d.scale];
 const m=[...document.querySelectorAll('.machine-view-mask')].map(e=>e.hidden?null:e.getBoundingClientRect());
 const hole=m.every(Boolean)?[m[3].right,m[0].bottom,m[1].left-m[3].right,m[2].top-m[0].bottom]:null;
 return {w:innerWidth,h:innerHeight,scale:d.scale,box,hole}};
export default UI;`;
const page=`<!doctype html><html><head><style>html,body{margin:0;height:100%;overflow:hidden;background:#313131}
#noVNC_container{position:fixed;inset:0}.screen{display:flex;width:100%;height:100%;overflow:hidden}.screen canvas{margin:auto;flex-shrink:0}</style>
<script type="module" src="machine-view.js"></script></head><body><div id="noVNC_container"></div></body></html>`;
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],
 fleet:{on:false,fleets:[]},browser_link:'https://cp.example/open?to=browser',browser_embed:'/browser/'});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');
 const send=(type,body)=>{res.setHeader('Content-Type',type);res.end(body)};
 if(url.pathname==='/')return send('text/html',dashboard);
 if(url.pathname==='/api/status')return send('application/json',JSON.stringify(state()));
 if(url.pathname==='/api/browser-now')return send('application/json',JSON.stringify({working:[],waiting:[],lang:'en'}));
 if(url.pathname==='/browser/')return send('text/html',page);
 if(url.pathname==='/browser/machine-view.js')return send('text/javascript',view);
 if(url.pathname==='/browser/app/ui.js')return send('text/javascript',ui);
 if(url.pathname==='/browser/defaults.json')return send('application/json',JSON.stringify({frame:'window'}));
 if(url.pathname==='/browser/region')return send('application/json',JSON.stringify({region}));
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;send('application/json','{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS||'';const errors=[];let browser;
const near=(a,b,by=2)=>Math.abs(a-b)<=by;
const viewer=p=>p.frames().find(f=>f.url().endsWith('/browser/'));
// The window fits the pane (its whole width or height), shows whole, sits in the middle across, and the cover leaves
// exactly the window open
async function fits(p,why){
 const f=viewer(p);await f.waitForFunction(()=>window.look&&document.querySelector('.machine-view-mask:not([hidden])'));
 await p.waitForTimeout(250);const l=await f.evaluate(()=>window.look());const [x,y,w,h]=l.box,say=why+' '+JSON.stringify(l);
 const want=l.h>l.w?l.w/(region.w*3840):Math.min(l.w/(region.w*3840),l.h/(region.h*2160));
 assert.ok(Math.abs(l.scale-want)<1e-3,'framed for the pane: '+say);
 assert.ok(x>=-2&&y>=-2&&x+w<=l.w+2&&y+h<=l.h+2,'the whole window shows: '+say);
 assert.ok(near(w,l.w)||near(h,l.h),'it fills the pane across or down: '+say);
 assert.ok(near(x,l.w-x-w),'it sits in the middle across: '+say);
 assert.ok(l.hole&&l.hole.every((v,i)=>near(v,[x,y,w,h][i])),'the cover leaves the window open, nothing else: '+say);
 return l}
const shoot=async(p,name)=>{if(shots)await p.screenshot({path:`${shots}/browser-pane-fit-${name}.png`})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [W,H] of [[2000,1080],[1440,900],[390,844]]){
  const size=W+'x'+H,context=await browser.newContext({viewport:{width:W,height:H}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const p=await context.newPage();p.on('pageerror',e=>errors.push(size+': '+e.message));
  await p.goto(base);
  const open=async()=>{if(W<1024&&await p.locator('#drawer-open').isVisible())await p.locator('#drawer-open').click();await p.locator('#open-browser').click();await p.locator('#browser-pane').waitFor()};
  const away=async()=>{await p.locator('#bp-close').click();await p.locator('#browser-pane').waitFor({state:'hidden'})};
  // First open
  await open();await fits(p,size+' first open');await shoot(p,size+'-open');
  // Full size and back
  await p.locator('#bp-full').click();await fits(p,size+' full size');await shoot(p,size+'-full');
  await p.locator('#bp-full').click();await fits(p,size+' out of full size');
  // Another view, the viewer reconnects meanwhile (at size 0), then Browser again: Jeroen's case
  await away();await viewer(p).evaluate(()=>window.reconnect());await p.waitForTimeout(800);
  await open();await fits(p,size+' shown again after a reconnect');await shoot(p,size+'-reconnected');
  // Hidden and shown again without a reconnect: still framed
  await away();await p.waitForTimeout(300);await open();await fits(p,size+' shown again');
  // The window resized: framed for the new size
  await p.setViewportSize({width:Math.round(W*.8),height:Math.round(H*.9)});await fits(p,size+' resized');
  await p.setViewportSize({width:W,height:H});await fits(p,size+' resized back');
  // Zoomed in by hand: the zoom stays across hiding, the cover still follows the picture, and Browser window frames again
  await viewer(p).locator('#machine-view-bar [data-v="in"]').click();await p.waitForTimeout(200);
  const zoomed=await viewer(p).evaluate(()=>window.look());
  await away();await viewer(p).evaluate(()=>window.reconnect());await p.waitForTimeout(500);await open();
  await fits(p,size+' a reconnect frames again, also after a zoom');
  await viewer(p).locator('#machine-view-bar [data-v="in"]').click();await away();await p.waitForTimeout(300);await open();await p.waitForTimeout(300);
  const kept=await viewer(p).evaluate(()=>window.look());
  assert.ok(Math.abs(kept.scale-zoomed.scale)<1e-3,size+' a zoom by hand stays: '+JSON.stringify([zoomed,kept]));
  {const [x,y,w,h]=kept.box,open=[Math.max(0,x),Math.max(0,y),x+w-Math.max(0,x),y+h-Math.max(0,y)];
   assert.ok(kept.hole&&kept.hole.every((v,i)=>near(v,open[i])),size+' the cover follows the zoomed picture: '+JSON.stringify(kept))}
  await viewer(p).locator('#machine-view-bar [data-v="whole"]').click();await viewer(p).locator('#machine-view-bar [data-v="whole"]').click();
  await fits(p,size+' Browser window after a zoom');
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('browser pane fit dashboard ok');
