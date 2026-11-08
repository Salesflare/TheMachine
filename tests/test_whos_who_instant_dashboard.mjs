import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Who's who, ✓ Right: the role is gone at the tap (within 100 ms), not after the Machine saved it, and stays gone when a
// refresh that started before the save draws the old list. A failed save brings it back with what went wrong. All are
// right does the same for every role. All names are made up.
const dashboard=await dashboardPage();
const role=(id,kind,name,r)=>({id,kind,name,role:r,quote:null,event_id:null,set_at:'2026-11-01'});
let whos=[role('email:pat@client.example','person','Pat Doe','CFO at Client Ltd'),role('email:lee@other.example','person','Lee Park','accountant'),
 role('org:client.example','org','Client Ltd','customer'),role('email:kim@shop.example','person','Kim Lane','supplier')];
const calls=[],errors=[];let hold=null,fail=false;
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{pending:0},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],graph_waiting:whos.length}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')?{}:{projects:[],people:[],quiet:[],new:[],orgs:[],whos_who:whos,waiting:whos.length,warmup:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='graph_role'){if(hold)await hold;
   if(fail){res.statusCode=400;res.end(JSON.stringify({error:'Couldn’t save that role.'}));return}
   whos=whos.filter(w=>w.id!==call.args.node_id)}
  res.end('{}');return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
// Taps a button and says how long until the page shows it gone (the next frame), and what it shows then
const tap=(page,sel)=>page.evaluate(async sel=>{const b=document.querySelector(sel),t0=performance.now();b.click();
 await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
 return {ms:performance.now()-t0,shown:[...document.querySelectorAll('#people-view .whos')].filter(a=>a.checkVisibility()).map(a=>a.dataset.whos),
  count:document.querySelector('#people-view [data-graph-panel="roles"] .count')?.textContent||'',badge:document.querySelector('#badge-people').textContent}},sel);
const shown=page=>page.evaluate(()=>[...document.querySelectorAll('#people-view .whos')].filter(a=>a.checkVisibility()).map(a=>a.dataset.whos));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await navClick(page.locator('nav [data-tab="people"]'));
 await navClick(page.locator('.side-sub a[data-graph-sub="roles"]'));
 await page.locator('#people-view .whos').first().waitFor();

 // ✓ Right while the Machine takes its time to save: gone at once, the counts one less
 let release;hold=new Promise(r=>release=r);
 let at=await tap(page,'[data-role-confirm="email:pat@client.example"]');
 assert.ok(at.ms<100,`Right shows within 100 ms: ${at.ms} ms`);
 assert.deepEqual(at.shown,['email:lee@other.example','org:client.example','email:kim@shop.example']);
 assert.equal(at.count,'3');assert.equal(at.badge,'3');
 assert.equal(await page.locator('#toast').textContent(),'Confirmed: CFO at Client Ltd.');
 // A refresh and a status poll that land before the save still have it: it stays gone
 await page.evaluate(()=>people(graphNode,true));
 await page.evaluate(()=>refresh(true));
 assert.deepEqual(await shown(page),['email:lee@other.example','org:client.example','email:kim@shop.example']);
 assert.equal(await page.locator('#badge-people').textContent(),'3');
 release();hold=null;
 for(let i=0;i<100&&whos.length!==3;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls.at(-1),{action:'graph_role',args:{node_id:'email:pat@client.example',role:'CFO at Client Ltd'}});
 for(let i=0;i<100&&(await shown(page)).length!==3;i++)await page.waitForTimeout(20);
 assert.deepEqual(await shown(page),['email:lee@other.example','org:client.example','email:kim@shop.example']);

 // A save that fails: gone at the tap, back when the answer says it failed, with why
 fail=true;hold=new Promise(r=>release=r);
 at=await tap(page,'[data-role-confirm="org:client.example"]');
 assert.ok(at.ms<100,`Right shows within 100 ms: ${at.ms} ms`);
 assert.deepEqual(at.shown,['email:lee@other.example','email:kim@shop.example']);
 release();hold=null;
 await page.locator('#toast.error',{hasText:'Couldn’t save that role.'}).waitFor();
 for(let i=0;i<100&&(await shown(page)).length!==3;i++)await page.waitForTimeout(20);
 assert.deepEqual(await shown(page),['email:lee@other.example','org:client.example','email:kim@shop.example']);
 assert.equal(await page.locator('#people-view [data-graph-panel="roles"] .count').textContent(),'3');
 fail=false;

 // All are right: every one gone at once, saved one by one after
 hold=new Promise(r=>release=r);
 page.once('dialog',d=>d.accept());
 at=await tap(page,'[data-role-all]');
 assert.ok(at.ms<100,`All are right shows within 100 ms: ${at.ms} ms`);
 assert.deepEqual(at.shown,[]);assert.equal(at.badge,'');
 release();hold=null;
 for(let i=0;i<150&&whos.length;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls.filter(c=>c.action==='graph_role').slice(-3).map(c=>c.args.node_id),['email:lee@other.example','org:client.example','email:kim@shop.example']);
 const rolesRowHidden=()=>page.locator('.side-sub a[data-graph-sub="roles"]').evaluate(a=>a.hidden);
 for(let i=0;i<100&&!await rolesRowHidden();i++)await page.waitForTimeout(20);
 assert.equal(await rolesRowHidden(),true);
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
