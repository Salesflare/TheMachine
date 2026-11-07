import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A link to a tab (#fleet, #todos, #messages, #graph, #learning, #connections) or a part of one (#fleet/sharing,
// #settings/notify, #graph=orgs) opens it on the first load and on a hash change, and stays in the address, so a
// reload after a quiet update (which puts back the tab the page was on, but only without a link) still lands there.
// A tap on another tab drops the link. A link that does something on a tab (#learning=changes, #connections=add)
// still goes once handled, so the same link works twice.
const dashboard=await dashboardPage();
const FL='fl_'+'a'.repeat(16),rules={relationships:{rule:'ask',details:false}};
const view={on:true,kinds:{relationships:'who knows someone'},fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Example',asks:[],people:[],members:[{member_id:'p',name:'Pat',rules}],rules,exceptions:{}}],waiting:[],asked:[],free:[],briefs:{},log:[],notices:[]};
const hours={days:[0,1,2,3,4],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC',saveable:true};
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');return res.end(dashboard)}
 if(req.url==='/api/status')return res.end(JSON.stringify({suggestions:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],hours,fleet:{on:true,waiting:0}}));
 if(req.url.startsWith('/api/fleet'))return res.end(JSON.stringify(view));
 res.statusCode=404;res.end('{}');});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const shown=page=>page.evaluate(()=>[...document.querySelectorAll('main>section')].filter(s=>!s.hidden).map(s=>s.id).join());
const fleetPaneOn=page=>page.evaluate(()=>document.querySelector('#fleet-view [data-fleet-pane][aria-selected="true"]')?.dataset.fleetPane||'');
const loaded=page=>page.waitForFunction(()=>!!state?.suggestions);
const links=[['#fleet','fleet'],['#todos','inbox'],['#messages','events'],['#graph','people'],['#learning','feedback'],['#connections','health'],['#settings/notify','settings']];
try{
 const errors=[];
 for(const [hash,section] of links){
  const page=await browser.newPage();page.on('pageerror',e=>errors.push(hash+': '+e.message));
  await page.goto(base+hash);await loaded(page);
  await page.waitForFunction(s=>[...document.querySelectorAll('main>section')].some(x=>x.id===s&&!x.hidden),section);
  assert.equal(await shown(page),section,hash+' opens its tab on the first load');
  const kept=await page.evaluate(()=>location.hash);
  assert.ok(kept===hash||hash==='#graph'&&kept==='#graph=people',hash+' stays in the address, got '+kept);
  if(hash==='#settings/notify')assert.equal(await page.evaluate(()=>settingsNow),'notify');
  await page.evaluate(()=>refresh());assert.equal(await shown(page),section,'a refresh keeps '+hash);
  await page.close()}
 const page=await browser.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);await loaded(page);assert.equal(await shown(page),'inbox');
 // on a hash change, also to a part of a tab
 await page.evaluate(()=>{location.hash='#fleet'});await page.waitForFunction(()=>!document.getElementById('fleet').hidden);
 assert.equal(await page.evaluate(()=>location.hash),'#fleet');
 await page.evaluate(()=>{location.hash='#fleet/sharing'});await page.waitForFunction(()=>document.querySelector('#fleet-view [data-fleet-pane="sharing"][aria-selected="true"]'));
 assert.equal(await page.evaluate(()=>location.hash),'#fleet/sharing');
 await page.locator('#fleet-view [data-fleet-pane="activity"]').click();
 assert.equal(await page.evaluate(()=>location.hash),'#fleet/activity','the address follows the Fleet pane');
 await page.evaluate(()=>refresh());assert.equal(await fleetPaneOn(page),'activity','a refresh keeps the pane');
 await page.evaluate(()=>{location.hash='#messages'});await page.waitForFunction(()=>!document.getElementById('events').hidden);
 // a link that does something on its tab goes once handled, so the same link works again
 await page.evaluate(()=>{location.hash='#learning=changes'});await page.waitForFunction(()=>!document.getElementById('feedback').hidden);
 assert.equal(await page.evaluate(()=>location.hash),'');
 await page.evaluate(()=>{location.hash='#settings/notify'});await page.waitForFunction(()=>!document.getElementById('settings').hidden&&settingsNow==='notify');
 // another tab tapped: the link goes, and a refresh doesn't pull the page back
 await page.evaluate(()=>{location.hash='#fleet'});await page.waitForFunction(()=>!document.getElementById('fleet').hidden);
 await page.locator('nav [data-tab="inbox"]').click();
 assert.equal(await page.evaluate(()=>location.hash),'');await page.evaluate(()=>refresh());assert.equal(await shown(page),'inbox');
 await page.close();
 // a deep link on a fresh load: #fleet/<pane>
 const deep=await browser.newPage();deep.on('pageerror',e=>errors.push(e.message));
 await deep.goto(base+'#fleet/sharing');await loaded(deep);
 await deep.waitForFunction(()=>document.querySelector('#fleet-view [data-fleet-pane="sharing"][aria-selected="true"]'));
 assert.equal(await deep.evaluate(()=>location.hash),'#fleet/sharing');await deep.close();
 // the reload after a quiet update puts back the tab it was on only when the address has no link
 const ctx=await browser.newContext();const upd=await ctx.newPage();upd.on('pageerror',e=>errors.push(e.message));
 await upd.addInitScript(()=>{if(!sessionStorage.getItem('seeded')){sessionStorage.setItem('seeded','1');sessionStorage.setItem('tm-update-view',JSON.stringify({at:Date.now(),tab:'inbox',y:0}))}});
 await upd.goto(base+'#fleet');await loaded(upd);await upd.waitForTimeout(300);
 assert.equal(await shown(upd),'fleet','#fleet after a quiet update');assert.equal(await upd.evaluate(()=>location.hash),'#fleet');
 await ctx.close();
 assert.deepEqual(errors,[]);console.log('Tab links: every tab, #fleet/<pane> and #settings/notify on load and on a hash change, kept in the address passed.');
}finally{await browser.close();server.close()}
