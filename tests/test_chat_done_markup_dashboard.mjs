import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do's text in the chat and on the Done list stays text: the card the chat takes its pieces from (chatParts),
// the chat's own updates (chatMount, chatPatch), a Done card that looks done (lookDoneCard) and the pages a long list
// loads (pager), and the to-do list they sit in, all go through html``, so markup in a title, a body or a loaded row never becomes elements.
const EVIL='<img src=x onerror="window.pwned=1">"\'&<b>';
const card={id:'c1',title:'Reply '+EVIL,body:'**'+EVIL+'**\n\nAsk '+EVIL+' about [x](javascript:alert(1))',status:'prepared',created_at:'2026-11-01T09:00:00Z',source:'gmail',actions:[]};
const later={...card,id:'c2',status:'snoozed',snoozed_until:'2099-01-05T09:00:00Z'};
const dashboard=await dashboardPage(),en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const server=createServer((req,res)=>{const u=new URL(req.url,'http://x');res.setHeader('Content-Type','application/json');
 if(u.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(u.pathname==='/i18n/en.json'){res.end(en);return}
 if(u.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[card,later],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_runs:[]}));return}
 if(!u.pathname.startsWith('/api/')){res.statusCode=404;res.end();return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 await page.goto('http://127.0.0.1:'+server.address().port+'/');
 await page.waitForFunction(()=>typeof chatParts==='function'&&typeof lookDoneCard==='function'&&typeof pager==='function'&&state?.suggestions?.length);
 const got=await page.evaluate(async([EVIL,card])=>{
  const bad=n=>n.querySelectorAll('img,script,a[href^="javascript"]').length+n.querySelectorAll('b').length;
  const frag=h=>htmlNodes(h),wrap=h=>{const d=document.createElement('div');d.append(htmlNodes(h));return d};
  const out={};
  // the to-do list itself: Ready, Coming back later with its day heading, Done, all drawn with html``
  const list=$('#suggestions');out.list=[bad(list),list.querySelector('#later-list')?.textContent.includes('Reply '+EVIL)??false,list.querySelectorAll('#later-list .day-head').length,!!list.querySelector('#finished-list'),list.textContent.includes('Reply '+EVIL)];
  // chatParts: the chat's pieces of the card
  const s=state.suggestions[0],p=chatParts(s);
  out.parts=Object.entries(p).filter(([,v])=>v instanceof SafeHTML||Array.isArray(v)).map(([k,v])=>[k,bad(wrap(html`${v}`))]);
  out.partsText=wrap(html`${p.intro}`).textContent.includes('Ask '+EVIL);
  // chatMount: the first draw, then an update of the same chat
  const layout=x=>html`<div class="chat-layout" data-chat="c1"><div class="chat-side"><p>${x}</p></div><div id="chat-log"><p>${x}</p></div><textarea id="chat-input"></textarea></div>`;
  const box=$('#suggestions');chatMount('c1',layout(EVIL));const first=bad(box);chatMount('c1',layout(EVIL+'2'));
  out.mount=[first,bad(box),box.querySelector('#chat-log').textContent];
  // chatPatch: only changed nodes are swapped, and they come from html``
  const el=document.createElement('div');chatPatch(el,html`<p>${EVIL}</p><p>same</p>`);chatPatch(el,html`<p>${EVIL+'!'}</p><p>same</p>`);
  out.patch=[bad(el),el.textContent];
  // lookDoneCard: the card is changed through the DOM, its text stays text
  const ld=wrap(lookDoneCard({...card,status:'prepared'}));
  out.lookDone=[bad(ld),ld.textContent.includes(EVIL),ld.querySelector('[data-ld-not]')?.dataset.ldNot??null];
  // pager: rows a page loads, appended to the rows already there, or the whole list drawn again
  const rows=[{id:'r1',t:EVIL},{id:'r2',t:EVIL+'2'}];
  const host=document.createElement('div');document.body.append(host);
  setHTML(host,html`${pagerSlot('t:a')}${pagerSlot('t:b')}`);
  let n=0;const load=async()=>({items:[rows[n++]],next:n<2?String(n):null});
  pager('t:a',load,x=>html`<p>${x.t}</p>`);pagerMount(host);await pagerMore('t:a');await pagerMore('t:a');
  n=0;pager('t:b',load,null,items=>html`${items.map(x=>html`<p>${x.t}</p>`)}`);pagerMount(host);await pagerMore('t:b');await pagerMore('t:b');
  const a=host.querySelector('[data-pager="t:a"] .pager-rows'),b=host.querySelector('[data-pager="t:b"] .pager-rows');
  out.pager=[bad(host),a.children.length,a.textContent,b.children.length,b.textContent];
  // the DOM helpers: a text node is written escaped, a change made through the DOM stays text
  out.helpers=[String(nodeHTML(document.createTextNode(EVIL),null)),bad(wrap(htmlEdit(html`<p>x</p>`,c=>{c.querySelector('p').textContent=EVIL}))),wrap(html`<i>${EVIL}</i>`).textContent];
  out.pwned=window.pwned||0;host.remove();return out},[EVIL,card]);
 assert.deepEqual(got.list,[0,true,1,true,true],'the to-do list');
 for(const [k,v] of got.parts)assert.equal(v,0,'chatParts '+k+': no markup from the card');
 assert.ok(got.partsText,'the card body reads as text in the chat');
 assert.deepEqual(got.mount,[0,0,EVIL+'2'],'chatMount');
 assert.deepEqual(got.patch,[0,EVIL+'!same'],'chatPatch');
 assert.deepEqual(got.lookDone,[0,true,'c1'],'lookDoneCard');
 assert.deepEqual(got.pager,[0,2,EVIL+EVIL+'2',2,EVIL+EVIL+'2'],'pager');
 assert.deepEqual(got.helpers,['&lt;img src=x onerror=&quot;window.pwned=1&quot;&gt;&quot;&#39;&amp;&lt;b&gt;',0,EVIL],'nodeHTML, htmlEdit, htmlNodes');
 assert.equal(got.pwned,0);
 assert.deepEqual(errors,[]);
 console.log('ok chat and Done markup stays text');
}finally{await browser?.close();server.close()}
