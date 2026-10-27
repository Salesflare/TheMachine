import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The dashboard's view of a desktop (deploy/browser/machine-view.js) frames the browser's window for the size it has.
// When that size changes (the window or the dashboard's pane resized, Full size, the pane shown again) it frames it
// again, so the view keeps filling the pane instead of staying at the old, smaller zoom. Zoomed in by hand, the zoom
// stays. noVNC's connection object is a stand-in here: a 3840x2160 screen with the browser on its right half.
const view=await readFile(new URL('../deploy/browser/machine-view.js',import.meta.url),'utf8');
const ui=`const display={width:3840,height:2160,scale:1,clipViewport:false,_viewportLoc:{x:0,y:0,w:0,h:0},
 viewportChangeSize(w,h){this._viewportLoc.w=Math.min(w,this.width);this._viewportLoc.h=Math.min(h,this.height)},
 viewportChangePos(dx,dy){const v=this._viewportLoc;v.x=Math.max(0,Math.min(this.width-v.w,v.x+dx));v.y=Math.max(0,Math.min(this.height-v.h,v.y+dy))}};
const rfb={_rfbConnectionState:'connected',_display:display,_canvas:document.createElement('canvas'),_screenSize(){return {w:innerWidth,h:innerHeight}},
 _fixScrollbars(){},_setClippingViewport(){},_sendMouse(){}};
window.display=display;export default {rfb,closeControlbar(){}};`;
const page='<!doctype html><html><body><div id="noVNC_container"></div><script type="module" src="machine-view.js"></script></body></html>';
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/vnc.html'){res.setHeader('Content-Type','text/html');res.end(page);return}
 if(url.pathname==='/machine-view.js'){res.setHeader('Content-Type','text/javascript');res.end(view);return}
 if(url.pathname==='/app/ui.js'){res.setHeader('Content-Type','text/javascript');res.end(ui);return}
 if(url.pathname==='/region'){res.setHeader('Content-Type','application/json');res.end(JSON.stringify({region:{x:0.5,y:0,w:0.5,h:1}}));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1000,height:600}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const p=await context.newPage();p.on('pageerror',e=>errors.push(e.message));
 await p.goto(base+'/vnc.html?frame=window');
 const scale=()=>p.evaluate(()=>window.display.scale);
 const near=(a,b)=>Math.abs(a-b)<1e-3;
 // The window, 1920x2160 on the screen, fits the height of a 1000x600 view
 await p.waitForFunction(()=>window.display?.scale!==1);
 assert.ok(near(await scale(),600/2160),String(await scale()));
 // A bigger pane: framed again for it, so it fills it
 await p.setViewportSize({width:1600,height:1000});
 await p.waitForFunction(()=>Math.abs(window.display.scale-1000/2160)<1e-3,null,{timeout:3000});
 // Zoomed in by hand: a new size keeps that zoom
 await p.click('#machine-view-bar [data-v="in"]');const zoomed=await scale();assert.ok(near(zoomed,1000/2160*1.4));
 await p.setViewportSize({width:1500,height:900});await p.waitForTimeout(400);assert.ok(near(await scale(),zoomed));
 // The window again (from Whole screen): framed for this size
 await p.click('#machine-view-bar [data-v="whole"]');await p.click('#machine-view-bar [data-v="whole"]');await p.waitForTimeout(200);
 assert.ok(near(await scale(),900/2160),String(await scale()));
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('machine view resize ok');
