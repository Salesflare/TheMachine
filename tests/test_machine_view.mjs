import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The dashboard's viewer of the Machine's browser (deploy/browser/machine-view.js, frame=window) on a stand-in noVNC.
// It frames the browser's front window. When the pane is wider than that window, the screen around it (other windows,
// often a dashboard with its own sidebar) is covered, so it never looks like the pane slips under the nav. When the pane
// changes size (the sidebar folds, the window is resized) the window is framed again. Whole screen shows everything.
const view=await readFile(new URL('../deploy/browser/machine-view.js',import.meta.url),'utf8');
// noVNC's parts that machine-view.js uses: a 2000x1000 screen, a viewport that stays on it, a canvas of the viewport's size
const ui=`const container=document.getElementById('noVNC_container'),canvas=container.querySelector('canvas');
const d={width:2000,height:1000,scale:1,clipViewport:true,_viewportLoc:{x:0,y:0,w:2000,h:1000},
 viewportChangeSize(w,h){const v=this._viewportLoc;v.w=Math.min(w,this.width);v.h=Math.min(h,this.height);this.viewportChangePos(0,0)},
 viewportChangePos(dx,dy){const v=this._viewportLoc;v.x=Math.max(0,Math.min(this.width-v.w,v.x+dx));v.y=Math.max(0,Math.min(this.height-v.h,v.y+dy));paint()}};
function paint(){const v=d._viewportLoc;canvas.style.width=v.w*d.scale+'px';canvas.style.height=v.h*d.scale+'px'}
const rfb={_display:d,_canvas:canvas,_rfbConnectionState:'connected',scaleViewport:false,clipViewport:true,_screenSize:()=>({w:container.clientWidth,h:container.clientHeight}),
 _fixScrollbars(){paint()},_setClippingViewport(){},_sendMouse(){},_updateClip(){},_updateScale(){}};
addEventListener('resize',()=>{rfb._updateClip();rfb._updateScale()});  // as noVNC does on its own
export default {rfb};`;
const page=`<!doctype html><html><head><style>html,body{margin:0;height:100%;overflow:hidden;background:#000}#noVNC_container{position:fixed;inset:0}canvas{position:absolute;left:0;top:0;background:#fff}</style>
<script type="module" src="machine-view.js"></script></head><body><div id="noVNC_container"><canvas></canvas></div></body></html>`;
const region={x:.5,y:0,w:.5,h:.5};let lang='en';  // the dashboard's language, from its /api/browser-now  // the browser's window: the screen's top right quarter, 1000x500
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');
 const send=(type,body)=>{res.setHeader('Content-Type',type);res.end(body)};
 if(url.pathname==='/browser/')return send('text/html',page);
 if(url.pathname==='/browser/machine-view.js')return send('text/javascript',view);
 if(url.pathname==='/browser/app/ui.js')return send('text/javascript',ui);
 if(url.pathname==='/api/browser-now')return send('application/json',JSON.stringify({working:[],waiting:[],lang}));
 if(url.pathname==='/i18n/nl.json')return send('application/json',await readFile(new URL('../i18n/nl.json',import.meta.url),'utf8'));
 if(url.pathname==='/browser/region')return send('application/json',JSON.stringify({region}));
 res.statusCode=404;res.end()});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/browser/?frame=window',errors=[];let browser;
// What shows on the pane: the window's box, and the boxes that cover the rest
const look=p=>p.evaluate(()=>{const masks=[...document.querySelectorAll('.machine-view-mask')].filter(m=>!m.hidden&&m.offsetWidth&&m.offsetHeight).map(m=>{const r=m.getBoundingClientRect();return [r.left,r.top,r.width,r.height].map(Math.round)});
 return {masks,w:innerWidth,h:innerHeight}});
// Whether a point of the pane is covered
const covered=(l,x,y)=>l.masks.some(([a,b,w,h])=>x>=a&&x<a+w&&y>=b&&y<b+h);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1000,height:300}});const p=await context.newPage();p.on('pageerror',e=>errors.push(e.message));
 await p.goto(base);await p.waitForTimeout(1200);
 // A wide pane: the window fits its height (300px tall, 600px wide) in the middle; the screen beside it is covered
 let l=await look(p);
 assert.ok(covered(l,100,150)&&covered(l,900,150),'the screen beside the window is covered '+JSON.stringify(l));
 assert.ok(!covered(l,210,10)&&!covered(l,500,150)&&!covered(l,790,290),'the window itself shows, in the middle '+JSON.stringify(l));
 const box=await p.evaluate(()=>{const r=document.querySelector('canvas').getBoundingClientRect();return [Math.round(r.left),Math.round(r.width)]});
 assert.equal(box[0]+400,200,'the window starts 200px in: the picture moved over '+JSON.stringify(box));
 // The pane changes size (the sidebar folds): framed again, still only the window
 await p.setViewportSize({width:800,height:600});await p.waitForTimeout(500);
 l=await look(p);
 assert.ok(!covered(l,10,10)&&!covered(l,790,390),'the window fills the new width '+JSON.stringify(l));
 assert.ok(covered(l,400,500),'below the window is covered '+JSON.stringify(l));
 // Whole screen: nothing covered
 await p.locator('#machine-view-bar [data-v="whole"]').click();await p.waitForTimeout(200);
 l=await look(p);assert.deepEqual(l.masks,[],'Whole screen shows everything');
 // In a Dutch dashboard its own buttons and note read Dutch, from the dashboard's catalog (no English left among them)
 lang='nl';const q=await context.newPage();q.on('pageerror',e=>errors.push(e.message));
 await q.goto(base);await q.waitForTimeout(800);
 const words=await q.evaluate(()=>({whole:document.querySelector('[data-v="whole"]').textContent,in:document.querySelector('[data-v="in"]').getAttribute('aria-label'),
  out:document.querySelector('[data-v="out"]').title,title:document.querySelector('#machine-note strong').textContent,ok:document.querySelector('#machine-note button').textContent}));
 assert.deepEqual(words,{whole:'Hele scherm',in:'Inzoomen',out:'Uitzoomen',title:'De eigen browser van je Machine',ok:'Begrepen'});
 assert.deepEqual(errors,[]);
 console.log('machine view ok');
}finally{await browser?.close();server.close()}
