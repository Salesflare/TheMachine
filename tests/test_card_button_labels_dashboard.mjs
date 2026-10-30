import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do's buttons show their labels as text. The Update label of a skill proposal carries the skill's own name
// (assistant.skill_labels), which can be any text, also from an imported skill: markup in it stays inert words.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),name='<img src=x onerror="window.pwned=1">';
const cards=[{id:'s1',title:'Update a skill with 3 notes',body:'These notes fit a skill.',status:'pending',scope:'work',created_at:now,event_ids:[1],
 labels:{accept:'Update '+name,reject:'Not now'},skill_proposal:{name,notes:['a','b','c'],body:'Do it this way.'}}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1280,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-s1').waitFor();
 const accept=page.locator('#task-s1 button[data-choice="accept"]');
 assert.equal(await accept.textContent(),'Update '+name);
 assert.equal(await page.locator('#task-s1 img[src="x"]').count(),0);
 await page.waitForTimeout(300);
 // Ids and links that reach the card, its chat and the side list stay inside their attributes, and the browser link
 // opens only http(s): anything else is the plain Open the browser button.
 const odd='x" onmouseover="window.pwned=2';
 const parsed=await page.evaluate(odd=>{const read=html=>{const t=document.createElement('template');t.innerHTML=html;return t.content};
  const card=read(suggestionCard({...state.suggestions[0],id:odd,labels:{},skill_proposal:null},'To decide'));
  const btn=card.querySelector('button[data-choice="reject"]');
  const side=read(sideRow({id:odd,title:'Side'},''));
  const bad=read(browserLink('s1',{link:'javascript:window.pwned=3'})),good=read(browserLink('s1',{link:'https://example.com/tab'}));
  return {btn:btn&&[btn.dataset.id,btn.getAttribute('onmouseover')],side:[side.querySelector('a').getAttribute('href'),side.querySelector('[onmouseover]')],
   bad:[bad.querySelectorAll('a').length,bad.querySelectorAll('button[data-browser-focus]').length],good:good.querySelector('a')?.getAttribute('href')}},odd);
 assert.deepEqual(parsed,{btn:[odd,null],side:['#chat='+odd,null],bad:[0,1],good:'https://example.com/tab'});
 assert.equal(await page.evaluate(()=>window.pwned),undefined);
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('card button labels dashboard ok');
