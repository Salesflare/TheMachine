import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The meeting view's rows, the Where and Invite suggestions and the skill dialog's notes and buttons build with
// html``: names, addresses, places and skill ids with markup in them stay text, and the dialog takes html`` only.
const dashboard=await dashboardPage(),en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const server=createServer((req,res)=>{const u=new URL(req.url,'http://x');res.setHeader('Content-Type','application/json');
 if(u.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(u.pathname==='/i18n/en.json'){res.end(en);return}
 if(u.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_runs:[]}));return}
 if(!u.pathname.startsWith('/api/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const BAD='<img src=x onerror="window.hit=1">"\'';
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 await page.goto('http://127.0.0.1:'+server.address().port+'/');
 await page.waitForFunction(()=>typeof calView==='function'&&typeof calSuggest==='function'&&typeof lookOpen==='function'&&typeof html==='function');

 // The meeting view: a guest, a known guest, an organization and a project, each with markup in its name
 const view=await page.evaluate(BAD=>{calView({id:'e1',title:BAD,start:'2026-03-02T10:00:00Z',end:'2026-03-02T11:00:00Z',location:BAD,
   with:[{name:BAD,email:'sam@example.com'},{name:'Kim '+BAD,email:'kim@example.com',node_id:'p"1'}],guests:3,
   orgs:[{node_id:'o1',name:BAD}],projects:[{node_id:'j1',name:BAD}]});
  const rows=document.querySelector('#cal-v-rows');document.querySelector('#cal-view').close();
  return {img:rows.querySelectorAll('img').length,who:[...rows.querySelectorAll('.cal-v-who')].map(e=>[e.textContent,e.title||e.querySelector('a')?.title||'']),
   links:[...rows.querySelectorAll('a')].map(a=>[a.getAttribute('href'),a.querySelector('svg')?1:0,a.textContent]),hit:window.hit||0}},BAD);
 assert.equal(view.img,0,'no markup from the meeting');
 assert.deepEqual(view.who,[[BAD+' sam@example.com','sam@example.com'],['Kim '+BAD,'kim@example.com'],['and 1 more','']]);
 assert.deepEqual(view.links,[['#graph/p%221',1,'Kim '+BAD],['#graph/o1',1,BAD],['#graph/j1',1,BAD]],'chips keep their icon, the name is text');

 // A suggestion list: the label and detail are text, the footer link stays a link
 const sug=await page.evaluate(async BAD=>{const input=document.createElement('input'),list=document.createElement('ul');list.id='t-sug';document.body.append(input,list);
  calSuggest(input,list,async()=>[{label:BAD,detail:BAD}],p=>html`<span>${p.label}</span><small>${p.detail}</small>`,()=>{},()=>html`<li class="foot"><a href="https://example.com/">Map</a></li>`);
  input.value='ab';input.dispatchEvent(new Event('input'));await new Promise(r=>setTimeout(r,500));
  return {img:list.querySelectorAll('img').length,span:list.querySelector('button span')?.textContent,small:list.querySelector('button small')?.textContent,foot:list.querySelectorAll('li.foot a').length,id:list.querySelector('button')?.id}},BAD);
 assert.deepEqual(sug,{img:0,span:BAD,small:BAD,foot:1,id:'t-sug-0'});

 // The skill dialog: notes are text, buttons built with html`` keep the id whole, a plain string is refused
 const look=await page.evaluate(BAD=>{lookOpen('T','from',[[BAD,true],null,[BAD]],'body',html`<button type="button" data-hub-install="${BAD}">Install</button>`);
  const notes=document.querySelector('#skill-look-notes'),acts=document.querySelector('#skill-look-actions');
  const got={img:notes.querySelectorAll('img').length+acts.querySelectorAll('img').length,notes:[...notes.children].map(li=>[li.className,li.textContent]),
   id:acts.querySelector('[data-hub-install]')?.dataset.hubInstall};
  let refused=false;try{lookOpen('T','from',[],'body','<b>x</b>')}catch(e){refused=e instanceof TypeError}
  document.querySelector('#skill-look').close();
  return {...got,refused,hit:window.hit||0}},BAD);
 assert.deepEqual(look,{img:0,notes:[['warn',BAD],['',BAD]],id:BAD,refused:true,hit:0});
 assert.equal(view.hit,0);
 assert.deepEqual(errors,[]);
 console.log('ok meeting view, suggestions and skill dialog keep markup as text');
}finally{await browser?.close();server.close()}
